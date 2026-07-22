#!/usr/bin/env bash
set -euo pipefail
cd /app
/app/scripts/build.sh
probe=/tmp/geometry-lab-smoke.json
rm -f "$probe"
GEOMLAB_OUTPUT="$probe" /app/bin/geomlab
test -s "$probe"
rm -f "$probe"
