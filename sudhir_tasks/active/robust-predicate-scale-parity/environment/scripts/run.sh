#!/usr/bin/env bash
set -euo pipefail
cd /app
make all
mkdir -p /app/output
exec /app/bin/geomlab
