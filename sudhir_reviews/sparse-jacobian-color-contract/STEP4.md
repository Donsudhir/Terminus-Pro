# TASK-SJCC-001 Step 4 Final Evidence

- Date: 2026-07-19
- Revision: 1
- Decision: APPROVED
- Mechanical status: PASS
- Submission state: Ready to upload; not yet marked submitted

## Prerequisites

- Step 2a: GO, 0 FAIL / 0 WARN
- Step 2b: PASS
- Step 3b: CLEAN (`STEP3B.md`)
- Current checksum: verified at package time
- Static and Dockerfile gates: PASS
- Collapse: 0 FAIL / 0 WARN / 23 PASS
- Final task edit after oracle stress: removed root-owned `tests/.pytest_cache` / `__pycache__` only (Harbor artifacts); no source logic change

## Oracle 10x

Evidence: `jobs/2026-07-19__03-05-27/result.json`

Command: `harbor run -p sudhir_tasks/active/sparse-jacobian-color-contract -a oracle -k 10 -n 1`

| Metric | Value |
| --- | --- |
| Scheduled trials | 10 |
| Completed trials | 10 |
| Errored trials | 0 |
| Mean reward | 1.0 |
| Reward 1.0 count | 10 |
| Pass@2…Pass@10 | 1.0 |
| Concurrency | `-k 10 -n 1` |

Compose teardown still logs snap `permission denied` on container stop (CM-003); trial rewards completed with zero exceptions.

Prior failed attempt `jobs/2026-07-19__03-02-26` is superseded (daemon collapse).

## Fresh NOP

Evidence: `jobs/2026-07-19__03-10-32/result.json`

| Metric | Value |
| --- | --- |
| Completed trials | 1 |
| Errored trials | 0 |
| Mean reward | 0.0 |
| Reward 0.0 count | 1 |

## Final archive

- Path: `sudhir_tasks_ready_to_submit/sparse-jacobian-color-contract.zip`
- SHA-256: `9c5b0e5e6658fc95cc4eb854eeffb8f3ff04afa60f2458b759e6e789c04c63f2`
- Members: 43
- Layout: standard, files at archive root
- Root entries: `instruction.md`, `task.toml`, `environment/`, `solution/`, `tests/`
- `environment/.dockerignore`: present
- Forbidden / AI-scaffolding / authoring-only files: none

## Source and zip parity

- Source/zip match: PASS (after removing leaked pytest cache from `tests/`)
- Zip basename matches task directory

## Approval gate

- `approved`: true
- `decision`: PASS
- `mechanical_status`: PASS
- blocking failures: none
- verifier_health: skipped (opt-in; not required)

Command: `python3 sudhir_task.py package sparse-jacobian-color-contract`

## Pre-upload checklist (CM ledger)

- [x] Final Dockerfile layer runs `asciinema --version`
- [x] No `/usr/bin/python3` symlink repoint after asciinema apt
- [x] Test-invoked `SENSLAB_*` and `--mode-echo` documented in instruction
- [x] collapse_check PASS, 0 WARN
- [x] Oracle 1x / 10x / NOP recorded
- [x] Network probe OK before 10x
- [ ] Platform upload + ingest (pending)

## Next

Upload `sudhir_tasks_ready_to_submit/sparse-jacobian-color-contract.zip` to Snorkel, then:

```bash
python3 sudhir_task.py phase sparse-jacobian-color-contract submitted
# place export in sudhir_snorkel/inbox/ and:
python3 sudhir_task.py ingest
```
