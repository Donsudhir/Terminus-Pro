# FEEDBACK — mesh-checkpoint-operator-skew REV-2

Source: Platform Fast Static Checks / CodeBuild (2026-07-22 ~21:56 UTC)

## Hard FAIL

- `ruff` F841: `tests/test_outputs.py:36` local `buf` assigned but never used.
- Aggregate: `Static checks failed with 4 error(s)` (ruff summary lines + F841).

## WARN (non-blocking / carve-out)

- Template detection: possible match `native_replay_reconciliation_divergence` (0.85) — human review note only.
- Dockerfile build toolchain / `make -C` in runtime image — known false positive when agent must compile at runtime; keep single-stage.
- `pip install` lockfile probe looked for `requirements.txt` (or other lock names); task used `verifier-requirements.txt` only — added `requirements.txt` alias.
- `internet_requirement/parse_error` — parse noise; `allow_internet=false` and no download commands.

## Fix applied

Removed unused `buf`; added `environment/requirements.txt` hash-lock alias; re-ran preflight + oracle 1x + NOP + oracle 10x + post-10x NOP.
