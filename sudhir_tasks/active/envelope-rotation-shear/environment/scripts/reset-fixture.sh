#!/bin/bash
set -euo pipefail

ROOT="${VAULT_HOME:-/app}"
rm -rf "$ROOT/var"
mkdir -p "$ROOT/var/live" "$ROOT/var/segments" "$ROOT/var/logs" "$ROOT/output"
cp "$ROOT"/fixtures/live/catalog.json "$ROOT/var/live/catalog.json"
cp "$ROOT"/fixtures/live/slice-*.bin "$ROOT/var/live/"
cp "$ROOT"/fixtures/segments/chunk-*.bin "$ROOT/var/segments/"
cp "$ROOT"/fixtures/logs/operations.ndjson "$ROOT/var/logs/operations.ndjson"
rm -f "$ROOT/output/recovery.json" "$ROOT/output/recovery.json.next"
rm -f "$ROOT"/var/live/*.next "$ROOT"/var/live/*.restore
