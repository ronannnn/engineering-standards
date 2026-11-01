#!/usr/bin/env python3
"""从 git diff --name-only -z 的路径流选择现存需求目录。"""

from pathlib import Path, PurePosixPath
import re
import sys


def select_runs(root: Path, paths: list[str]) -> list[str]:
    result = set()
    base = (root / "docs/engineering").resolve()
    for value in paths:
        path = PurePosixPath(value)
        parts = path.parts
        if len(parts) < 4 or parts[:2] != ("docs", "engineering"):
            continue
        slug = parts[2]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or ".." in parts:
            continue
        target = root / "docs/engineering" / slug
        if target.is_dir() and target.resolve().parent == base:
            result.add(f"docs/engineering/{slug}")
    return sorted(result)


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    paths = sys.stdin.buffer.read().decode("utf-8", errors="surrogateescape").split("\0")
    for directory in select_runs(root, paths):
        print(directory)
