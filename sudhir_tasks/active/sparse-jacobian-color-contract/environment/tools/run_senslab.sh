#!/usr/bin/env bash
set -euo pipefail
cd /app
make all
mkdir -p output
/app/bin/senslab
