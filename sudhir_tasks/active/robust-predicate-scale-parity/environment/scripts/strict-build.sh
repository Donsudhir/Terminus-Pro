#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 2 ]]; then
    echo "usage: strict-build.sh BUILD_DIR BIN_DIR" >&2
    exit 2
fi
cd /app
make \
    BUILD_DIR="$1" \
    BIN_DIR="$2" \
    CFLAGS="-std=c11 -O0 -fno-fast-math -ffp-contract=off -Wall -Wextra -Werror" \
    FFLAGS="-O0 -Wall -Wextra -Werror" \
    RUSTFLAGS="-C opt-level=0 -C debuginfo=0" \
    all
