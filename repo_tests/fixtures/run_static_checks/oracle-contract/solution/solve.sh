#!/usr/bin/env bash
set -euo pipefail
cmake -S /app -B /app/build -D TB_TIMELINE_MODE=1 -D TB_REEXEC_MODE=1
cmake --build /app/build
install -m 0755 /app/build/netplay_matrix /app/bin/netplay_matrix
