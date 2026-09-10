from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


SCRIPT_DIRECTORY = Path(__file__).parent


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIRECTORY / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


content_safety = load_module("content_safety", "content_safety.py")
language_detection = load_module(
    "detect_codeql_languages", "detect_codeql_languages.py"
)


class ContentSafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        config_path = self.root / ".github"
        config_path.mkdir()
        (config_path / "content-safety-allowlist.json").write_text(
            json.dumps({"allow": {}}),
            encoding="utf-8",
        )
        self.config = content_safety.load_config(self.root)

    def tearDown(self) -> None:
        self.directory.cleanup()

    def scan(self, relative_path: str, value: str):
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        return content_safety.scan_file(path, self.root, self.config)

    def test_placeholder_secret_is_allowed(self) -> None:
        findings = self.scan("sample.py", 'api_key = "<your-api-key>"\n')
        self.assertEqual([], findings)

    def test_high_entropy_secret_assignment_is_rejected(self) -> None:
        value = "n8Vx2Qp7Lm4Zr9Ty6Kc3Wd5Hs8Fj1"
        findings = self.scan("sample.py", f'client_secret = "{value}"\n')
        self.assertIn("SECRET_ASSIGNMENT", {finding.rule for finding in findings})

    def test_confidential_marking_can_be_suppressed_with_reason(self) -> None:
        marking = "Micro" + "soft Confidential"
        findings = self.scan(
            "policy.md",
            "<!-- content-safety: allow CONFIDENTIAL_MARKING -- "
            "explains the public scanning policy -->\n"
            f"{marking}\n",
        )
        self.assertNotIn(
            "CONFIDENTIAL_MARKING", {finding.rule for finding in findings}
        )

    def test_private_key_cannot_be_suppressed(self) -> None:
        header = "-----BEGIN " + "PRIVATE KEY-----"
        findings = self.scan(
            "key.txt",
            "<!-- content-safety: allow SECRET_PRIVATE_KEY -- synthetic fixture -->\n"
            f"{header}\n",
        )
        self.assertIn("SECRET_PRIVATE_KEY", {finding.rule for finding in findings})

    def test_secret_cannot_be_allowed_by_path(self) -> None:
        self.config["allow"] = {"SECRET_ASSIGNMENT": ["sample.py"]}
        value = "n8Vx2Qp7Lm4Zr9Ty6Kc3Wd5Hs8Fj1"
        findings = self.scan("sample.py", f'client_secret = "{value}"\n')
        self.assertIn("SECRET_ASSIGNMENT", {finding.rule for finding in findings})

    def test_comment_does_not_turn_real_secret_into_placeholder(self) -> None:
        value = "n8Vx2Qp7Lm4Zr9Ty6Kc3Wd5Hs8Fj1"
        findings = self.scan(
            "sample.py", f'client_secret = "{value}"  # test environment\n'
        )
        self.assertIn("SECRET_ASSIGNMENT", {finding.rule for finding in findings})

    def test_quoted_json_secret_assignment_is_rejected(self) -> None:
        value = "n8Vx2Qp7Lm4Zr9Ty6Kc3Wd5Hs8Fj1"
        findings = self.scan("settings.json", f'{{"password": "{value}"}}\n')
        self.assertIn("SECRET_ASSIGNMENT", {finding.rule for finding in findings})

    def test_disabled_ai_safety_control_is_rejected(self) -> None:
        unsafe_setting = "guard" + "rails = false"
        findings = self.scan("ai-config.yml", f"{unsafe_setting}\n")
        self.assertIn("RAI_SAFETY_DISABLED", {finding.rule for finding in findings})

    def test_notebook_outputs_are_rejected(self) -> None:
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": 1,
                    "outputs": [{"output_type": "stream", "text": ["private output"]}],
                    "source": ["print('hello')"],
                }
            ]
        }
        findings = self.scan("demo.ipynb", json.dumps(notebook))
        self.assertIn("NOTEBOOK_OUTPUT", {finding.rule for finding in findings})

    def test_cloud_identifier_is_rejected_in_context(self) -> None:
        identifier = "8d319c9b-5a70-4c67-9f2c-364f48fc9091"
        findings = self.scan("config.yml", f"subscription_id: {identifier}\n")
        self.assertIn(
            "PRIVACY_CLOUD_IDENTIFIER", {finding.rule for finding in findings}
        )

    def test_cloud_identifier_can_be_suppressed_with_reason(self) -> None:
        identifier = "8d319c9b-5a70-4c67-9f2c-364f48fc9091"
        findings = self.scan(
            "config.yml",
            "# content-safety: allow PRIVACY_CLOUD_IDENTIFIER -- synthetic docs ID\n"
            f"subscription_id: {identifier}\n",
        )
        self.assertNotIn(
            "PRIVACY_CLOUD_IDENTIFIER", {finding.rule for finding in findings}
        )

    def test_email_address_is_rejected(self) -> None:
        address = "person" + "@example.com"
        findings = self.scan("sample.md", f"Contact {address}\n")
        self.assertIn("PRIVACY_EMAIL", {finding.rule for finding in findings})


class LanguageDetectionTests(unittest.TestCase):
    def test_detects_supported_languages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "app.py").write_text("print('hello')\n", encoding="utf-8")
            (root / "web.ts").write_text("export {};\n", encoding="utf-8")
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            self.assertEqual(
                [
                    {
                        "language": "javascript-typescript",
                        "build-mode": "none",
                        "runner": "ubuntu-latest",
                    },
                    {
                        "language": "python",
                        "build-mode": "none",
                        "runner": "ubuntu-latest",
                    },
                ],
                language_detection.detect_languages(root),
            )

    def test_kotlin_uses_autobuild_and_swift_uses_macos(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "App.kt").write_text("fun main() {}\n", encoding="utf-8")
            (root / "App.swift").write_text("print(\"hello\")\n", encoding="utf-8")
            self.assertEqual(
                [
                    {
                        "language": "java-kotlin",
                        "build-mode": "autobuild",
                        "runner": "ubuntu-latest",
                    },
                    {
                        "language": "swift",
                        "build-mode": "autobuild",
                        "runner": "macos-latest",
                    },
                ],
                language_detection.detect_languages(root),
            )

    def test_detects_supported_web_source_extensions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "App.vue").write_text("<template></template>\n", encoding="utf-8")
            self.assertEqual(
                [
                    {
                        "language": "javascript-typescript",
                        "build-mode": "none",
                        "runner": "ubuntu-latest",
                    }
                ],
                language_detection.detect_languages(root),
            )


if __name__ == "__main__":
    unittest.main()
