# REV-2 notes — resolver-closure-drift

Opened: 2026-07-19T16:07:31Z

Reason: Platform EASY (opus 100%/gpt5 80%); QC behavior_in_task_description on build-report; Legacy* history leak; AutoEval build FAILED

## Changes

### A. Instruction + contract (CM-002 / QC)
- Documented `/app/output/build-report.json` with boolean `success` and integer `members` (lock tuple count on success).
- Moved `build-report.json` from `internal_harness_files` to `user_visible_outputs`; added `[structured_outputs.build_report]` with `success` / `members` instruction_checks.
- Softened history guidance: history has independently valid compatibility lines; merged tool must preserve both; no "release notes define expected selections" answer-table invitation.
- Emphasized `/app/bin/rebuild-forge` after every source edit.
- Kept lockfile sorting contract; added symptom that equivalent archive/root reorderings must not change lock bytes.

### B. Rename enum leaks (CM-008)
- `VaneKind::LegacyAlpha` / `LegacyBeta` → `HeldPin` / `HeldLane` in bootstrap base + oracle `solve.sh`.
- `RejectCode::Legacy` → `RejectCode::Held`.
- Profile TOML strings `alpha` / `beta` / `mixed` unchanged.

### C. Bury history answer tables (CM-008)
- `alpha.patch` / `beta.patch` / `merge.patch`: parent tests and release notes no longer embed exact lock triples.
- Softened commit messages in alpha/beta/merge descriptors.
- Trimmed `docs/architecture.md` so it no longer maps Vane→Admitted→Trellis as a solver recipe.

### D. Languages (CM-011)
- `task.toml` `languages = ["rust"]` only; added `rust` tag.

### E. Optional harden
- Softened walk error `"no admissible candidate"` → `"resolution stalled"`.
- Oracle quay sort path unchanged.

### F. Dockerfile (CM-001)
- Early-layer + mid-layer `command -v asciinema` / `asciinema --version` retained; final-layer verify kept. No `/usr/bin/python3` repoint.

## Validation (this revision)
- Bootstrap `rebuild_repo.py` applies cleanly.
- `./scripts/check-task.sh` Phase A/B/C PASS (collapse 0 FAIL / 0 WARN / 23 PASS; dockerfile_check PASS).
- `python3 sudhir_task.py gates resolver-closure-drift`: static/dockerfile/collapse/integrity all PASS.
- Leak scan: no `LegacyAlpha`/`LegacyBeta` under environment/ or solution/; no answer triples in release notes/parent tests.
- Harbor oracle 1x: `2026-07-19__21-41-45` mean=1.0 (compose-down permission warning on cleanup; trial reward 1.0).
- Harbor NOP: first attempt `2026-07-19__21-45-10` errored (Docker Hub DNS for `docker/dockerfile:1`); retry `2026-07-19__21-45-38` reward=0.0.
- Not packaged (await parent).
