#!/bin/bash
set -euo pipefail

OUT_DIR=/app/output
STAGE="$OUT_DIR/stage"
PAYLOAD="$OUT_DIR/payload"
REPORT="$OUT_DIR/probe_report.json"
ALPHA=/app/vendor/alpha
BRAVO=/app/vendor/bravo
CHARLIE=/app/vendor/charlie

mkdir -p "$OUT_DIR" "$STAGE" /app/bin
make -C /app/mod_common

rm -rf "$STAGE"
mkdir -p "$STAGE"

/app/bin/knit_main "$ALPHA" "$BRAVO" "$STAGE"
/app/bin/lane_main "$BRAVO" "$CHARLIE" "$STAGE/lane.rsp"
/app/bin/seal_main "$STAGE" "unused" "$STAGE/seal.flags"

# Compile against the staged include tree.
gcc -c -isystem "$STAGE/include" -o "$STAGE/payload.o" /app/src/payload.c

# Link: CRT from stage, response fragments from lane/seal, tag object from lane.
mapfile -t LANE_ARGS < "$STAGE/lane.rsp"
mapfile -t SEAL_ARGS < "$STAGE/seal.flags"

gcc -nostdlib \
  "${SEAL_ARGS[@]}" \
  "$STAGE/payload.o" \
  "$STAGE/lane.rsp.tag.o" \
  "${LANE_ARGS[@]}" \
  "$STAGE/lib/crtn.o" \
  -o "$PAYLOAD"

chmod +x "$PAYLOAD"

# Ledger via seal (json mode) after the artifact exists.
/app/tools/run_probes.sh "$PAYLOAD" "$REPORT"
