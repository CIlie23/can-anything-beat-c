#!/usr/bin/env bash
# Builds and runs the empty startup program in all six languages.
cd "$(dirname "$0")/.." || exit 1
EXT=""; case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) EXT=".exe";; esac
S=tests/startup
GOOSE="${GOOSE_DIR:-$HOME/goose}/build/goose"
mkdir -p $S/{c,cpp,zig,go,goose}/bin

build_c()     { gcc -O3 $S/c/main.c -o $S/c/bin/startup; }
build_cpp()   { g++ -O3 $S/cpp/main.cpp -o $S/cpp/bin/startup; }
build_rust()  { (cd $S/rust && cargo build --release); }
build_zig()   { zig build-exe $S/zig/main.zig -O ReleaseFast -femit-bin=$S/zig/bin/startup; }
build_go()    { go build -o $S/go/bin/startup $S/go/main.go; }
build_goose() { "$GOOSE" -o $S/goose/startup.c --standalone $S/goose/main.goose \
                && gcc -O3 $S/goose/startup.c -o $S/goose/bin/startup -lm -pthread; }

fail=0
run() { # name, binary
  if build_$1 >/tmp/startup_$1.log 2>&1 && $2; then echo "OK    $1"
  else echo "FAIL  $1  (log: /tmp/startup_$1.log)"; fail=1; fi
}
run c     $S/c/bin/startup
run cpp   $S/cpp/bin/startup
run rust  $S/rust/target/release/startup_rust
run zig   $S/zig/bin/startup
run go    $S/go/bin/startup
run goose $S/goose/bin/startup
[ $fail = 0 ] && echo "ALL OK" || echo "SOME FAILED"
exit $fail
