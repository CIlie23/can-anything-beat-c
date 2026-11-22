#!/usr/bin/env python3
"""Discover benchmarks and provide a common benchmark runner entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:  # pragma: no cover - Python 3.10 and earlier
    tomllib = None


LANGUAGES = ("c", "cpp", "rust", "zig", "go", "goose")


def load_config(path: Path) -> dict:
    if tomllib is None:
        raise RuntimeError("Python 3.11 or newer is required to read config.toml")
    with path.open("rb") as config_file:
        return tomllib.load(config_file)


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=root / "config.toml")
    parser.add_argument("--test", help="Test name under tests/")
    parser.add_argument(
        "--language",
        choices=LANGUAGES,
        help="Run only implementations for this language",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the layout and print the planned runs",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent.parent
    if not args.config.is_absolute():
        args.config = root / args.config

    try:
        config = load_config(args.config)
    except (OSError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    tests_dir = root / "tests"
    test_names = (
        [args.test]
        if args.test
        else sorted(path.name for path in tests_dir.iterdir() if path.is_dir())
    )

    for test_name in test_names:
        test_dir = tests_dir / test_name
        if not test_dir.is_dir():
            print(f"error: unknown test: {test_name}", file=sys.stderr)
            return 1
        for language in LANGUAGES:
            if args.language and language != args.language:
                continue
            if not (test_dir / language).is_dir():
                print(
                    f"error: missing implementation directory: "
                    f"tests/{test_name}/{language}",
                    file=sys.stderr,
                )
                return 1
            if args.dry_run:
                print(f"{test_name}/{language}")

    if not args.dry_run:
        print(
            "Benchmark implementation is ready; add implementations and "
            "recorded devices to execute runs."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
