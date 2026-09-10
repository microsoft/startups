#!/usr/bin/env python3
"""Scan repository content for public-release safety risks."""

from __future__ import annotations

import argparse
import fnmatch
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable, Iterator


MAX_FILE_SIZE = 10 * 1024 * 1024
CONFIG_PATH = ".github/content-safety-allowlist.json"
SUPPRESSION = re.compile(
    r"content-safety:\s*allow\s+([A-Z0-9_]+)\s+--\s+(.{8,})",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Finding:
    rule: str
    category: str
    path: str
    line: int
    message: str


@dataclass(frozen=True)
class Rule:
    rule: str
    category: str
    pattern: re.Pattern[str]
    message: str
    suppressible: bool = True


RULES = (
    Rule(
        "SECRET_PRIVATE_KEY",
        "secrets",
        re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"),
        "Private key material must never be committed.",
        False,
    ),
    Rule(
        "SECRET_KNOWN_TOKEN",
        "secrets",
        re.compile(
            r"\b(?:"
            r"github_pat_[A-Za-z0-9_]{40,255}|"
            r"gh[pousr]_[A-Za-z0-9]{36,255}|"
            r"AKIA[0-9A-Z]{16}|"
            r"xox[baprs]-[A-Za-z0-9-]{20,}|"
            r"sk-(?:proj-)?[A-Za-z0-9_-]{32,}"
            r")\b"
        ),
        "A value matching a known credential format was found.",
        False,
    ),
    Rule(
        "SECRET_CONNECTION_STRING",
        "secrets",
        re.compile(
            r"(?i)\b(?:AccountKey|SharedAccessSignature|Password)\s*="
            r"\s*[^;<\s$][^;\s]{15,}"
        ),
        "A connection string appears to contain embedded credentials.",
        False,
    ),
    Rule(
        "SECRET_JWT",
        "secrets",
        re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
        "A JSON Web Token was found.",
        False,
    ),
    Rule(
        "PRIVACY_EMAIL",
        "privacy",
        re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
        "An email address needs confirmation that it is approved for public use.",
    ),
    Rule(
        "PRIVACY_SSN",
        "privacy",
        re.compile(r"\b(?!000|666|9\d\d)\d{3}[- ]\d{2}[- ]\d{4}\b"),
        "A value resembling a US Social Security number was found.",
        False,
    ),
    Rule(
        "PRIVACY_PHONE",
        "privacy",
        re.compile(r"(?<!\d)(?:\+1[\s.-]?)?\([2-9]\d{2}\)[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)"),
        "A value resembling a personal phone number was found.",
    ),
    Rule(
        "PRIVACY_LOCAL_PATH",
        "privacy",
        re.compile(
            r"(?i)(?:"
            r"[A-Z]:\\Users\\(?!user(?:name)?\\|runneradmin\\|public\\)[^\\\r\n]+\\|"
            r"/" r"Users/(?!user(?:name)?/|runner/|shared/)[^/\r\n]+/|"
            r"/" r"home/(?!user(?:name)?/|runner/|root/)[^/\r\n]+/"
            r")"
        ),
        "A local user path may disclose a person's account name.",
    ),
    Rule(
        "CONFIDENTIAL_MARKING",
        "confidentiality",
        re.compile(
            r"(?i)\b(?:"
            r"(?:microsoft|company|customer|highly|strictly)\s+confidential|"
            r"internal\s+only|do\s+not\s+distribute|"
            r"privileged\s+and\s+confidential"
            r")\b"
        ),
        "Content marked confidential or internal cannot be published without review.",
    ),
    Rule(
        "CONFIDENTIAL_INTERNAL_URL",
        "confidentiality",
        re.compile(
            r"(?i)https?://[^\s)\]>]*(?:"
            r"microsoft(?:-my)?\.sharepoint\.com|"
            r"microsoft\.sharepoint-df\.com|"
            r"msit\.powerbi\.com|"
            r"icm\.ad\.msft\.net"
            r")[^\s)\]>]*"
        ),
        "An internal Microsoft URL was found in public content.",
    ),
    Rule(
        "RAI_SAFETY_DISABLED",
        "responsible-ai",
        re.compile(
            r"(?i)\b(?:content[_ -]?filter(?:ing)?|guardrails?|safety[_ -]?(?:filter|setting)s?)"
            r"\s*[:=]\s*[\"']?(?:false|off|none|disabled|0)\b"
        ),
        "AI safety controls appear to be disabled; document and review the justification.",
    ),
    Rule(
        "RAI_HIGH_IMPACT_USE",
        "responsible-ai",
        re.compile(
            r"(?i)\b(?:"
            r"emotion\s+recognition|social\s+scoring|predictive\s+policing|"
            r"biometric\s+identification|"
            r"autonomous\s+(?:hiring|credit|medical|legal)\s+decision"
            r")\b"
        ),
        "A high-impact AI use case requires an explicit Responsible AI review.",
    ),
)

SECRET_ASSIGNMENT = re.compile(
    r"""(?ix)
    \b(?:api[_-]?key|client[_-]?secret|access[_-]?token|auth[_-]?token|
    password|passwd|account[_-]?key)\b
    ["']?\s*[:=]\s*
    ["']?([A-Za-z0-9+/_.=-]{20,})["']?
    """
)
UUID = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-"
    r"[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"
)
UUID_CONTEXT = re.compile(
    r"(?i)\b(?:subscription|tenant|client|object|account)[_-]?(?:id|identifier)?\b"
)
CARD_CANDIDATE = re.compile(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")
SAFE_SECRET_TERMS = (
    "example",
    "sample",
    "dummy",
    "placeholder",
    "changeme",
    "replace",
    "your_",
    "your-",
    "fake",
    "test",
)
RISKY_FILENAMES = {
    ".env",
    "credentials.json",
    "service-account.json",
    "id_rsa",
    "id_ed25519",
}
RISKY_SUFFIXES = {".p12", ".pfx", ".jks", ".keystore", ".har", ".pcap", ".dmp"}


def load_config(root: Path) -> dict[str, object]:
    path = root / CONFIG_PATH
    if not path.exists():
        return {"allow": {}}
    with path.open(encoding="utf-8") as stream:
        config = json.load(stream)
    if not isinstance(config.get("allow", {}), dict):
        raise ValueError(f"{CONFIG_PATH}: 'allow' must be an object")
    return config


def repository_files(root: Path) -> list[Path]:
    command = [
        "git",
        "-C",
        str(root),
        "ls-files",
        "--cached",
        "--others",
        "--exclude-standard",
        "-z",
    ]
    result = subprocess.run(command, capture_output=True, check=False)
    if result.returncode == 0:
        names = result.stdout.decode("utf-8", errors="surrogateescape").split("\0")
        return [root / name for name in names if name]

    return [
        path
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    ]


def matches_any(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def path_allowed(rule: str, path: str, config: dict[str, object]) -> bool:
    if rule.startswith("SECRET_"):
        return False
    allowed = config.get("allow", {})
    assert isinstance(allowed, dict)
    patterns = allowed.get(rule, [])
    return isinstance(patterns, list) and matches_any(path, patterns)


def suppression_for(lines: list[str], index: int, rule: str) -> bool:
    for candidate in (lines[index], lines[index - 1] if index > 0 else ""):
        match = SUPPRESSION.search(candidate)
        if match and match.group(1).upper() == rule:
            return True
    return False


def shannon_entropy(value: str) -> float:
    if not value:
        return 0.0
    frequencies = {character: value.count(character) for character in set(value)}
    return -sum(
        (count / len(value)) * math.log2(count / len(value))
        for count in frequencies.values()
    )


def looks_like_placeholder(value: str) -> bool:
    lowered = value.lower().strip()
    normalized = lowered.strip("\"'<>[]{}()")
    return (
        normalized in SAFE_SECRET_TERMS
        or normalized.startswith(("your_", "your-", "example_", "example-"))
        or normalized.endswith(("_placeholder", "-placeholder"))
        or "${" in value
        or "{{" in value
        or "<" in value
        or len(set(value)) < 5
        or shannon_entropy(value) < 3.2
    )


def luhn_valid(candidate: str) -> bool:
    digits = [int(character) for character in candidate if character.isdigit()]
    if not 13 <= len(digits) <= 19 or len(set(digits)) == 1:
        return False
    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def add_finding(
    findings: list[Finding],
    config: dict[str, object],
    finding: Finding,
) -> None:
    if not path_allowed(finding.rule, finding.path, config):
        findings.append(finding)


def scan_notebook(
    path: Path,
    relative_path: str,
    config: dict[str, object],
) -> list[Finding]:
    findings: list[Finding] = []
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        add_finding(
            findings,
            config,
            Finding(
                "NOTEBOOK_INVALID",
                "privacy",
                relative_path,
                1,
                "Notebook is not valid UTF-8 JSON and cannot be checked safely.",
            ),
        )
        return findings

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        if cell.get("outputs") or cell.get("execution_count") is not None:
            add_finding(
                findings,
                config,
                Finding(
                    "NOTEBOOK_OUTPUT",
                    "privacy",
                    relative_path,
                    1,
                    "Clear notebook outputs and execution counts before publishing.",
                ),
            )
            break
    return findings


def scan_text(
    text: str,
    relative_path: str,
    config: dict[str, object],
) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()

    for index, line in enumerate(lines):
        line_number = index + 1
        for rule in RULES:
            if not rule.pattern.search(line):
                continue
            if path_allowed(rule.rule, relative_path, config):
                continue
            if rule.suppressible and suppression_for(lines, index, rule.rule):
                continue
            findings.append(
                Finding(rule.rule, rule.category, relative_path, line_number, rule.message)
            )

        assignment = SECRET_ASSIGNMENT.search(line)
        if assignment and not looks_like_placeholder(assignment.group(1)):
            add_finding(
                findings,
                config,
                Finding(
                    "SECRET_ASSIGNMENT",
                    "secrets",
                    relative_path,
                    line_number,
                    "A high-entropy value appears to be assigned to a credential field.",
                ),
            )

        if UUID_CONTEXT.search(line):
            for identifier in UUID.findall(line):
                if (
                    identifier.lower() != "00000000-0000-0000-0000-000000000000"
                    and not suppression_for(lines, index, "PRIVACY_CLOUD_IDENTIFIER")
                ):
                    add_finding(
                        findings,
                        config,
                        Finding(
                            "PRIVACY_CLOUD_IDENTIFIER",
                            "privacy",
                            relative_path,
                            line_number,
                            "A cloud/account identifier needs confirmation that it is synthetic.",
                        ),
                    )
                    break

        for candidate in CARD_CANDIDATE.findall(line):
            if (
                luhn_valid(candidate)
                and not suppression_for(lines, index, "PRIVACY_PAYMENT_CARD")
            ):
                add_finding(
                    findings,
                    config,
                    Finding(
                        "PRIVACY_PAYMENT_CARD",
                        "privacy",
                        relative_path,
                        line_number,
                        "A value matching a payment-card checksum was found.",
                    ),
                )
                break

    return findings


def scan_file(
    path: Path,
    root: Path,
    config: dict[str, object],
) -> list[Finding]:
    relative_path = path.relative_to(root).as_posix()
    findings: list[Finding] = []
    try:
        size = path.lstat().st_size
    except OSError as error:
        return [
            Finding(
                "FILE_UNREADABLE",
                "repository",
                relative_path,
                1,
                f"File metadata could not be read: {error}",
            )
        ]

    lower_name = path.name.lower()
    is_environment_file = lower_name == ".env" or lower_name.startswith(".env.")
    is_safe_environment_template = lower_name.endswith(
        (".example", ".sample", ".template")
    )
    if (
        (lower_name in RISKY_FILENAMES or is_environment_file)
        and not is_safe_environment_template
    ) or path.suffix.lower() in RISKY_SUFFIXES:
        add_finding(
            findings,
            config,
            Finding(
                "RISKY_FILE_TYPE",
                "privacy",
                relative_path,
                1,
                "This file type commonly contains credentials or captured private data.",
            ),
        )

    if size > MAX_FILE_SIZE:
        add_finding(
            findings,
            config,
            Finding(
                "LARGE_FILE",
                "repository",
                relative_path,
                1,
                f"File is larger than {MAX_FILE_SIZE // (1024 * 1024)} MiB; review before publishing.",
            ),
        )

    if path.suffix.lower() == ".ipynb":
        findings.extend(scan_notebook(path, relative_path, config))

    try:
        data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
    except OSError as error:
        findings.append(
            Finding(
                "FILE_UNREADABLE",
                "repository",
                relative_path,
                1,
                f"File content could not be read: {error}",
            )
        )
        return findings

    if b"\0" in data[:8192]:
        return findings
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return findings
    findings.extend(scan_text(text, relative_path, config))
    return findings


def scan_repository(root: Path) -> list[Finding]:
    config = load_config(root)
    findings: list[Finding] = []
    for path in repository_files(root):
        findings.extend(scan_file(path, root, config))
    return sorted(findings, key=lambda item: (item.path, item.line, item.rule))


def escape_annotation(value: str) -> str:
    return (
        value.replace("%", "%25")
        .replace("\r", "%0D")
        .replace("\n", "%0A")
        .replace(":", "%3A")
        .replace(",", "%2C")
    )


def print_findings(findings: Iterable[Finding], github_annotations: bool) -> None:
    for finding in findings:
        if github_annotations:
            print(
                f"::error file={escape_annotation(finding.path)},"
                f"line={finding.line},title={finding.rule}::"
                f"{escape_annotation(finding.message)}"
            )
        else:
            print(
                f"{finding.path}:{finding.line}: {finding.rule} "
                f"[{finding.category}] {finding.message}"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        type=Path,
        help="Repository root (default: current directory)",
    )
    parser.add_argument(
        "--github-annotations",
        action="store_true",
        help="Emit GitHub workflow annotations",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    try:
        findings = scan_repository(root)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"content-safety: configuration error: {error}", file=sys.stderr)
        return 2

    if findings:
        print_findings(findings, args.github_annotations)
        print(f"Content safety scan failed with {len(findings)} finding(s).")
        return 1

    print("Content safety scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
