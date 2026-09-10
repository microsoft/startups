#!/usr/bin/env python3
"""Emit a CodeQL matrix for languages present in the repository."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


LANGUAGES = {
    "c-cpp": {
        "suffixes": {".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx"},
        "build-mode": "none",
        "runner": "ubuntu-latest",
    },
    "csharp": {
        "suffixes": {".cs"},
        "build-mode": "none",
        "runner": "ubuntu-latest",
    },
    "go": {
        "suffixes": {".go"},
        "build-mode": "autobuild",
        "runner": "ubuntu-latest",
    },
    "java-kotlin": {
        "suffixes": {".java", ".kt", ".kts"},
        "build-mode": "none",
        "runner": "ubuntu-latest",
    },
    "javascript-typescript": {
        "suffixes": {
            ".cjs",
            ".cts",
            ".es",
            ".es6",
            ".htm",
            ".html",
            ".js",
            ".jsx",
            ".mjs",
            ".mts",
            ".ts",
            ".tsx",
            ".vue",
            ".xhtm",
            ".xhtml",
            ".xsjs",
            ".xsjslib",
        },
        "build-mode": "none",
        "runner": "ubuntu-latest",
    },
    "python": {
        "suffixes": {".py"},
        "build-mode": "none",
        "runner": "ubuntu-latest",
    },
    "ruby": {
        "suffixes": {".rb"},
        "build-mode": "none",
        "runner": "ubuntu-latest",
    },
    "rust": {
        "suffixes": {".rs"},
        "build-mode": "none",
        "runner": "ubuntu-latest",
    },
    "swift": {
        "suffixes": {".swift"},
        "build-mode": "autobuild",
        "runner": "macos-latest",
    },
}
IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "bin",
    "build",
    "dist",
    "node_modules",
    "obj",
    "vendor",
}


def detect_languages(root: Path) -> list[dict[str, str]]:
    detected: set[str] = set()
    has_kotlin = False
    for current_root, directories, files in os.walk(root):
        directories[:] = [
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        ]
        for filename in files:
            suffix = Path(filename).suffix.lower()
            has_kotlin = has_kotlin or suffix in {".kt", ".kts"}
            for language, configuration in LANGUAGES.items():
                if suffix in configuration["suffixes"]:
                    detected.add(language)
    matrix = []
    for language, configuration in LANGUAGES.items():
        if language not in detected:
            continue
        build_mode = configuration["build-mode"]
        if language == "java-kotlin" and has_kotlin:
            build_mode = "autobuild"
        matrix.append(
            {
                "language": language,
                "build-mode": build_mode,
                "runner": configuration["runner"],
            }
        )
    return matrix


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    matrix = json.dumps({"include": detect_languages(args.root.resolve())})
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as stream:
            stream.write(f"matrix={matrix}\n")
            stream.write(
                f"has-languages={'true' if json.loads(matrix)['include'] else 'false'}\n"
            )
    else:
        print(matrix)


if __name__ == "__main__":
    main()
