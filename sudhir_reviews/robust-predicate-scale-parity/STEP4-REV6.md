# TASK-RPSP-001 Step 4 — Revision 6

Date: 2026-07-19

## Scope

CM-007 grader integrity fix plus non-blocking `task.toml` / Dockerfile hygiene.
See `STEP2B-REV6.md` and `EDIT_LEDGER.md`.

## Evidence

| Gate | Result | Path / note |
| --- | --- | --- |
| check-task / static / dockerfile / integrity | PASS | checksum current after rev6 edits |
| collapse | 0 FAIL / 2 WARN | RC6 + GX9 justified in `STEP3B-REV5.md` |
| Harbor oracle 10x (`-k 10 -n 2`) | **10/10 mean 1.0**, 0 errors | `jobs/2026-07-19__13-29-21` |
| Harbor NOP (post-10x) | **mean 0.0** | `jobs/2026-07-19__13-31-57` |
| CM-007 Docker shadow probe | PASS | vuln rc=0; fixed+attacks reward=0; oracle+attacks reward=1 |
| validate_submission_zip | PASS | archive root clean |
| approve_task | PASS (mechanical WARN = collapse) | `--skip-verifier-health` |

## Archive

- Canonical: `sudhir_tasks_ready_to_submit/robust-predicate-scale-parity.zip`
- Mirror: `Task_Ready_To_Submit/robust-predicate-scale-parity.zip`
- SHA-256: `002571487962e397b1123130703819916a52e67e53d5c0cb2302bb27d999c9a8`

Zip includes CM-007 `tests/test.sh`, `difficulty = "medium"`, and
`asciinema --version` in the Dockerfile.

## Upload

Re-upload to Snorkel submission `fcee6e2e-1c89-476f-aa10-5932a474ef97`.
On the platform form, prefer output/artifact rubric lines over process-only
criteria (reviewer non-blocking note).
