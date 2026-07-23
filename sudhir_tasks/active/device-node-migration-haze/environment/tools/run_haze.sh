#!/usr/bin/env bash
set -euo pipefail
cd /app
mkdir -p /app/output /app/var/stage
exec /app/bin/haze "$@"
