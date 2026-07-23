#!/bin/bash
set -euo pipefail

mkdir -p /app/output
go run /app/environment/scripts/compute_replay_audit.go \
  /app/output/conflict_windows.json \
  /app/output/replay_manifest.tsv
