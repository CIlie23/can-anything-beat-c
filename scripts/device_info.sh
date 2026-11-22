#!/usr/bin/env bash
# usage: scripts/device_info.sh <device-name> ["short description"]
name="${1:?usage: device_info.sh <device-name> [description]}"
desc="${2:-}"
out="devices/$name.md"
mkdir -p devices

v() { command -v "$1" >/dev/null 2>&1 && "$@" 2>&1 | head -1 || echo "not installed"; }

cpu=$(lscpu 2>/dev/null | sed -n 's/^Model name: *//p' | head -1)
[ -z "$cpu" ] && cpu=$(grep -m1 -i -E 'model name|hardware' /proc/cpuinfo | sed 's/.*: *//')
ram=$(awk '/MemTotal/ {printf "%.1f GiB", $2/1048576}' /proc/meminfo)
os=$( (. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME") || uname -o )
goose_dir="${GOOSE_DIR:-$HOME/goose}"

{
  echo "# $name"
  [ -n "$desc" ] && echo && echo "$desc"
  echo
  echo "- Date recorded: $(date +%F)"
  echo "- CPU: ${cpu:-unknown}"
  echo "- Arch: $(uname -m), logical cores: $(nproc 2>/dev/null || echo ?)"
  echo "- RAM: $ram"
  echo "- OS: $os, kernel $(uname -r)"
  echo "- GCC: $(v gcc --version)"
  echo "- Clang: $(v clang --version)"
  echo "- Rust: $(v rustc --version)"
  echo "- Zig: $(v zig version)"
  echo "- Go: $(v go version)"
  echo "- hyperfine: $(v hyperfine --version)"
  echo "- Goose commit: $(git -C "$goose_dir" rev-parse HEAD 2>/dev/null || echo 'not installed')"
} > "$out"
echo "wrote $out"
