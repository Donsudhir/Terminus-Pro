#!/usr/bin/env bash
set -euo pipefail
cd /app
mkdir -p /app/output
exec /app/bin/partlab "$@"
