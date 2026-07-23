# resolver-closure-drift Edit Ledger

## 2026-07-19T13:42:02Z — Revision 1

- evidence capture

## 2026-07-19T16:07:31Z — Revision 2

- Platform EASY (opus 100%/gpt5 80%); QC behavior_in_task_description on build-report; Legacy* history leak

## 2026-07-19T21:45:38Z — Revision 2 harden applied

- Documented build-report schema; moved to user_visible_outputs + structured checks
- Renamed LegacyAlpha/LegacyBeta → HeldPin/HeldLane; RejectCode::Legacy → Held
- Buried lock triples in history release notes/parent tests; softened descriptors + architecture.md
- languages=["rust"]; softened walk error; Dockerfile early asciinema verify (CM-001)
- Gates PASS; Harbor oracle `2026-07-19__21-41-45` mean=1.0; NOP `2026-07-19__21-45-38` reward=0.0
- CM-008 Seen: RCD `4d74fca0` REV-1 EASY

## 2026-07-20T11:48:42Z — Revision 3

- Rubric CM-015: Agent format + third negative; optional branch nudge in instruction

## 2026-07-20T11:51:47Z — Revision 3 applied + packaged

- Soft instruction nudge: repository branches hold the two compatibility lines
- UI rubric: 8 positives (sum 23) + 4 negatives (−5/−5/−3/−3), Agent…, ±N
- Did not name wire/lock.rs or declare sorting as a second known defect
- Gates PASS (static/dockerfile/collapse/integrity); approve PASS; zip validated
- Package `sudhir_tasks_ready_to_submit/resolver-closure-drift.zip` sha256=`6d1f0ec9db7d97a6cdff940332133775a298bb9d6ada24d074d6e427abcac48f` (77 members)
- CM-015 Seen bumped; TASK-RCD-001 + FAILURE-CM-015 HIT edge in knowledge graph
- Docker cleaned after package

## 2026-07-22T03:14:50Z — Revision 4

- QC behavior_in_task_description: disclose profile/preview/withdrawn/constraint contracts

## 2026-07-22T03:25:00Z — Revision 4 applied + packaged

- Instruction + `/app/repo/docs/architecture.md`: profiles plain/alpha/beta/mixed, preview/withdrawn, five-field constraints, named edge cases, generated-package generalization (CM-002)
- GX6 kept at 0 connectives; collapse 0 FAIL / 0 WARN; check-task + gates PASS
- Harbor: oracle 1x `2026-07-22__08-46-44` mean=1.0; nop `2026-07-22__08-48-12` mean=0.0; oracle 10x `2026-07-22__08-49-12` mean=1.0 Pass@10=1.0
- Package `sudhir_tasks_ready_to_submit/resolver-closure-drift.zip` sha256=`9693fcdbbf78f2bfe48c8f51c17e4650a6c0442f95af35c4a3ce0bea61fc5e98` (77 members)
- CM-002 Seen bumped for RCD `4d74fca0` REV-4; Docker cleaned after package

## 2026-07-22T18:51:42Z — Revision 5

- CM-008 EASY opus80/gpt5100; harden veil+quay so sill-only cannot pass; keep QC contracts

## 2026-07-23T00:30:00Z — Revision 5 hardening (in progress)

- Platform EASY: opus 80% / gpt5 100% after REV-4 QC disclosure
- Closed HeldPin/HeldLane admission shortcut in broken sill; quay always reverse-sorts
- Did not name sort as a second known bug (instruction-sufficiency suggestion rejected for CM-008)
- Harbor oracle 1x + nop PASS; oracle 10x blocked by CM-003 (permission-denied container stop / subnet pools)
- Next: `sudo snap restart docker` (or host Docker restart), then `harbor run … -a oracle -k 10 -n 1`, package

## 2026-07-23T01:20:00Z — Revision 5 packaged

- Oracle 10x clean after Docker restart: `2026-07-23__01-11-53` mean=1.0
- Package `sudhir_tasks_ready_to_submit/resolver-closure-drift.zip`
- DSV Humanizer audit PASS; PREUPLOAD complete
