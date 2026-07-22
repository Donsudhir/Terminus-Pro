#!/usr/bin/env bash
# Source this file before running the harness in Sudhir's canonical workspace.
if [[ -n ${BASH_SOURCE[0]:-} ]]; then
	SOURCE_PATH="${BASH_SOURCE[0]}"
elif [[ -n ${ZSH_VERSION:-} ]]; then
	SOURCE_PATH="${(%):-%N}"
else
	SOURCE_PATH="$0"
fi
ROOT="$(cd "$(dirname "$SOURCE_PATH")/.." && pwd)"
if [[ -x "$ROOT/.venv/bin/python" ]]; then
	PYTHON_BIN="$ROOT/.venv/bin/python"
else
	PYTHON_BIN="python3"
fi
ROOT_EXPORTS="$($PYTHON_BIN -c '
import shlex
import sys
sys.path.insert(0, sys.argv[1])
import root_adapter
for key, value in root_adapter.ROOTS.environment().items():
    print(f"export {key}={shlex.quote(value)}")
' "$ROOT")" || return 1
eval "$ROOT_EXPORTS"
unset ROOT_EXPORTS PYTHON_BIN
unset ROOT SOURCE_PATH
