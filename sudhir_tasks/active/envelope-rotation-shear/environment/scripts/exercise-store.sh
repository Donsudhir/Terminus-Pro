#!/bin/bash
set -euo pipefail

ROOT="${VAULT_HOME:-/app}"
"$ROOT/scripts/reset-fixture.sh"
"$ROOT/bin/vaultctl" recover
"$ROOT/bin/vaultctl" maintain
"$ROOT/bin/vaultctl" maintain
"$ROOT/bin/vaultctl" audit
