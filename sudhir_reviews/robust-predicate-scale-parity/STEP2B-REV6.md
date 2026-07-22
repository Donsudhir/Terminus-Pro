# TASK-RPSP-001 Step 2b — Revision 6

Date: 2026-07-19

## Changes

- CM-007: `tests/test.sh` uses `cd /tests && PYTHONSAFEPATH=1 python -m pytest … --confcutdir=/tests`.
- `task.toml`: `difficulty = "medium"`; removed `mcp_servers`.
- Dockerfile: final-layer `asciinema --version` (CM-001 hygiene).

## Preflight

`./scripts/check-task.sh sudhir_tasks/active/robust-predicate-scale-parity` — PASS
(static PASS, dockerfile PASS, collapse 0 FAIL / 2 WARN justified in STEP3B-REV5).

## Harbor

| Run | Job | Mean |
| --- | --- | --- |
| oracle 1x | `jobs/2026-07-19__13-23-56` | 1.000 |
| nop 1x | `jobs/2026-07-19__13-24-49` | 0.000 |

## CM-007 shadow probe (Docker, root, attacks planted)

Image: `robust-predicate-scale-parity__3cgp7a6__env-main:latest`

| Invocation | Result |
| --- | --- |
| Vulnerable `cd /app && python -m pytest …/tests/test_outputs.py` with `/app/pytest.py` + `/conftest.py` | rc=0 (bypass) |
| Fixed `cd /tests && PYTHONSAFEPATH=1 python -m pytest --confcutdir=/tests …` with same plants | rc=1; real tests collected |
| Fixed `/tests/test.sh` without oracle | reward=0 |
| Oracle `solve.sh` then fixed `/tests/test.sh` with same plants | reward=1; 12 passed |

## Next

Step 4: oracle 10x, fresh NOP, package, approve, re-upload to `fcee6e2e-…`.
Tighten platform rubric lines to output/artifact criteria on resubmit.
