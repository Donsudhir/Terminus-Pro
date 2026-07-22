#!/bin/bash
set -euo pipefail

ROOT="${VAULT_HOME:-/app}"
"$ROOT/bin/inspect"
"$ROOT/bin/vaultctl" audit
