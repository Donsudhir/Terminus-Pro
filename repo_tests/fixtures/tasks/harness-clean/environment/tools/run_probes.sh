#!/bin/bash
# Runs the payload under qemu-user and asks seal_main to write the ledger.
set -euo pipefail

PAYLOAD=${1:?payload}
REPORT=${2:?report}
QEMU=${QEMU:-qemu-x86_64}

if ! command -v "$QEMU" >/dev/null 2>&1; then
  QEMU=""
fi

TMP_OUT=$(mktemp)
if [[ -n "$QEMU" ]]; then
  "$QEMU" "$PAYLOAD" >"$TMP_OUT" 2>/dev/null || true
else
  "$PAYLOAD" >"$TMP_OUT" 2>/dev/null || true
fi

# seal_main json mode: a=payload path, b=captured stdout path, out=report
/app/bin/seal_main "$PAYLOAD" "$TMP_OUT" "$REPORT"
rm -f "$TMP_OUT"
