#!/bin/bash
# Operator preflight — confirms vendor roots exist.
set -euo pipefail
for d in /app/vendor/alpha /app/vendor/bravo /app/vendor/charlie; do
  test -d "$d"
done
echo "preflight: vendor roots present"
