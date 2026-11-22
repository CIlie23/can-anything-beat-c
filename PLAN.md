# Project plan

This repository benchmarks implementations of a shared test specification across C,
C++, Rust, Zig, Go, and Goose.

## Work items

- Define benchmark specifications in `tests/<test>/SPEC.md`.
- Add equivalent implementations in each language directory.
- Configure benchmark sizes, the random seed, and compiler flags in `config.toml`.
- Run benchmarks with `scripts/run.py`.
- Record one CSV file per device under `results/raw/`.
- Verify result integrity with `scripts/check_checksums.py`.
- Record setup and environment details in `devices/<device>.md`.
