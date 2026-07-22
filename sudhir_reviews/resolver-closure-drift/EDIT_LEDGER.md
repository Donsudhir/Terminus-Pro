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
