# can-anything-beat-c

## Setup: Windows 11 (MSYS2)

Run everything in the **MSYS2 UCRT64** shell, not PowerShell.

1. Install MSYS2 (msys2.org), open "MSYS2 UCRT64", then:
   ```bash
   pacman -S mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-clang \
             mingw-w64-ucrt-x86_64-cmake git make python
   ```
2. Install on Windows: Rust (rustup), Go, hyperfine (`winget install hyperfine`).
3. Zig **0.17.1**: download the Windows zip from ziglang.org, extract it, and
   add the folder to `PATH` (in MSYS2: `export PATH=$PATH:/c/tools/zig` in `~/.bashrc`).
4. Goose at the commit in `config.toml`: clone, `git checkout <commit>`,
   `cmake -B build -DCMAKE_BUILD_TYPE=Release -G "MSYS Makefiles"`,
   `cmake --build build -j`. Set `GOOSE_BIN` to the built `goose.exe`.
5. `scripts/check_startup.sh` → expect `ALL OK`.
6. `scripts/device_info.sh ryzen-win "Setup 1: Ryzen 7 4800H, Windows 11"`
