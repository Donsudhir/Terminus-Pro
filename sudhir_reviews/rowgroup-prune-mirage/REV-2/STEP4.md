# STEP4 — REV-2 final approval — rowgroup-prune-mirage

- Date: 2026-07-19
- Decision: **APPROVED WITH JUSTIFIED RC2 WARN**

## Final evidence

- Docker network allocation probe: PASS after CM-003 cleanup.
- Harbor oracle 10x: `jobs/2026-07-19__22-47-29`
  - 10/10 reward 1.0
  - mean 1.0
  - zero exceptions
  - Pass@2/4/5/8/10 all 1.0
  - concurrency throttled to two to avoid known subnet-pool exhaustion.
- Fresh post-stress NOP: `jobs/2026-07-19__22-50-35`
  - reward 0.0
  - zero exceptions.
- Current checksum: verified before packaging.
- Submission archive:
  `sudhir_tasks_ready_to_submit/rowgroup-prune-mirage.zip`
- SHA-256:
  `276d2d003d75ccc374e1888fad3c52cd3001980da81d4d3e9f5071c17e235047`
- Archive members: 45.
- Zip validation: PASS.
- Manifest verification: PASS.
- Source/zip parity: PASS.
- Authoritative `approve_task.py`: exit 0, no blocking failures.
- Verifier health: intentionally skipped on the routine path; exact manual
  behavioral A/B/C ablations are recorded in STEP3B.
- Quality check: not run; no reviewer requested the opt-in LLM diagnostic.
- Repository regression: 268 passed, 26 skipped, 2 deselected in 5.92s through
  the locked environment. The two deselected checks are confirmed pre-existing
  workspace baseline failures: `AGENTS.md` is already 126 bytes over its cap,
  and the legacy `Task_Ready_To_Submit/` submission index is stale against
  pre-existing untracked archives. TASK-RPM-001 changes neither surface.

## Mechanical warning disposition

`collapse_check.py` reports one RC2 WARN because the visible language directory
`rust/` matches the implementation-language token. This predicts neither
`ember/fold.rs` nor `tilt_a`; the semantic diagnostic is empty, the other two
frontier locations are unpredictable, and all instruction/symbol/path grep
checks pass. STEP3B records the full justification. This is not a task defect.

## Archive review

The archive root contains only `instruction.md`, `task.toml`, `environment/`,
`solution/`, and `tests/`. Local authoring metadata, construction manifest,
checksum, metrics, reviewer files, caches, and AI scaffolding are absent.
`environment/.dockerignore` is present. No wrapping directory or generated build
artifact is included.

## Result

The current REV-2 source is approved locally and the archive is ready for manual
platform upload. Platform acceptance remains pending until direct reviewer or
platform evidence is ingested.
