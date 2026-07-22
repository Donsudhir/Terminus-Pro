#!/bin/bash
# CI wrapper — rebuilds stage tools then invokes the assembly entrypoint.
set -euo pipefail
make -C /app/mod_common
exec /app/tools/build_payload.sh
