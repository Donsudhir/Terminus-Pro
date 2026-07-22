# TASK-RPSP-001 Step 4 Final Evidence

- Date: 2026-07-18
- Revision: 4
- Decision: APPROVED
- Mechanical status: PASS
- Submission state: Ready to upload; not yet marked submitted

## Prerequisites

- Step 2a: GO, 0 FAIL / 0 WARN
- Step 2b: PASS
- Step 3b: CLEAN
- Current checksum: verified
- Static and Dockerfile gates: PASS
- Collapse: 0 FAIL / 0 WARN / 23 PASS
- Final task edit after oracle stress: none

## Oracle 10x

Evidence: `jobs/2026-07-18__23-30-19/result.json`

- Scheduled trials: 10
- Completed trials: 10
- Errored trials: 0
- Retries: 0
- Mean reward: 1.0
- Reward 1.0 count: 10
- Pass@2, Pass@4, Pass@5, Pass@8, Pass@10: 1.0
- Concurrency: `-k 10 -n 10`

This is the first Step 4 stress evidence valid for revision 4. The earlier RUN-0005 stress was correctly marked stale after Step 3b task edits.

## Fresh NOP

Evidence: `jobs/2026-07-18__23-31-33/result.json`

- Completed trials: 1
- Errored trials: 0
- Mean reward: 0.0
- Reward 0.0 count: 1

## Final archive

- Path: `sudhir_tasks_ready_to_submit/robust-predicate-scale-parity.zip`
- SHA-256: `17a0eb184ef35e43a0d6474da4ca7367a931de0e456b378534e1d9310bd6797d`
- Bytes: 29,677
- Members: 42
- Layout: standard, files at archive root
- Root entries: `instruction.md`, `task.toml`, `environment/`, `solution/`, `tests/`
- `environment/.dockerignore`: present
- Wrapping folder: none
- Forbidden root files: none
- Forbidden members: none
- AI-scaffolding filenames: none
- Authoring-only files: excluded

Manual member inspection confirmed every shipped file is task material. `output_contract.toml`, `construction_manifest.json`, quality waivers, checksums, metrics, caches, and reviewer records are absent.

## Source and zip parity

- Packaged source files: 42
- Zip files: 42
- Missing in zip: none
- Extra in zip: none
- Content mismatches: none
- Source and zip manifests: match
- Zip basename and task directory: match

## Approval gate

Authoritative machine-readable gate result:

- `approved`: true
- `decision`: PASS
- `mechanical_status`: PASS
- blocking failures: none
- warnings: none
- checksum: PASS
- static: PASS
- collapse: PASS
- zip validation: PASS
- manifest verification: PASS
- source/zip match: PASS
- verifier-health: SKIPPED by explicit clean routine-path opt-out
- quality adjudication: PASS, not required

## Repository certification

- Ruff: PASS
- Pytest: 241 passed, 26 skipped
- Canonical task checksum: verified
- Legacy submission index: current for 157 archives
- Stale RPSP containers: none
- Git whitespace check: PASS

## Infrastructure disposition

Harbor trials completed and recorded correct rewards, but the machine's Snap Docker daemon denied compose teardown. This remained an infrastructure cleanup issue, not a task exception. Containers were terminated through their internal process trees and unused task networks were pruned after the stress run.

## Final decision

APPROVED and ready to upload. Do not edit the task or rebuild the archive before upload. Any edit invalidates this evidence and requires preflight, oracle 1x, NOP, Step 3b review, oracle 10x, fresh NOP, package, and approval again.
