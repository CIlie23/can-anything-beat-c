#!/usr/bin/env python3
"""Print SHA-256 checksums for raw benchmark CSV files."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as csv_file:
        for chunk in iter(lambda: csv_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="CSV files to check (defaults to results/raw/*.csv)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=root,
        help="Repository root used for relative paths",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    files = args.files
    if not files:
        files = sorted((root / "results" / "raw").glob("*.csv"))

    if not files:
        print("No CSV files found.", file=sys.stderr)
        return 0

    for supplied_path in files:
        path = supplied_path if supplied_path.is_absolute() else root / supplied_path
        if not path.is_file():
            print(f"error: missing file: {supplied_path}", file=sys.stderr)
            return 1
        try:
            relative_path = path.resolve().relative_to(root)
        except ValueError:
            relative_path = path
        print(f"{sha256(path)}  {relative_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
