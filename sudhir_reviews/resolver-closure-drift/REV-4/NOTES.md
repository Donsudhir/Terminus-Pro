# REV-4 notes — resolver-closure-drift

Opened: 2026-07-22T03:14:50Z
Implemented: 2026-07-22

## Why the submission failed

QC `behavior_in_task_description` FAIL (blocking for acceptance). Instruction
named lock/report schema and vaguely referenced “two edge-case behaviors,” but
tests graded profile modes, preview/withdrawn admission, constraint syntax,
named edge cases, and generated-package generalization.

Also UI AutoEval banner FAILED (CM-019 class — re-eval after content fix).

## REV-4 fix (CM-002 / CM-018)

- Expanded `instruction.md` with normative contracts for:
  - profiles plain/alpha/beta/mixed and admission semantics
  - preview and withdrawn catalog attributes
  - five-field constraint form `name:low:high:channel:exact-code`
  - named edge cases: alpha preview selection; beta retained withdrawn under exact pin
  - generated package names/ranges follow the same rules
- Expanded `/app/repo/docs/architecture.md` as cited grading reference
- Softened temporal connectives so GX6 stays PASS (0 connectives)
- Did not name fix files or paste fixture lock tuples

## Mistakes remembered

- CM-002 recurrence on RCD (REV-2 had build-report gap; REV-4 is full admission/profile gap)
- CM-019: empty difficulty / AutoEval FAILED may still be infra; fix content first then re-eval

## Gate / Harbor evidence

- `check-task.sh` PASS; `sudhir_task.py gates` static/dockerfile/collapse/integrity PASS
- oracle 1x `2026-07-22__08-46-44` mean=1.0
- nop `2026-07-22__08-48-12` mean=0.0
- oracle 10x `2026-07-22__08-49-12` mean=1.0 Pass@10=1.0
- Package sha256=`9693fcdbbf78f2bfe48c8f51c17e4650a6c0442f95af35c4a3ce0bea61fc5e98`

## Upload

1. Replace zip with `sudhir_tasks_ready_to_submit/resolver-closure-drift.zip`
2. Paste REV-4 DIFFICULTY / SOLUTION / VERIFICATION / RUBRIC (body text under the `#` headers)
3. Re-run platform AutoEval / difficulty (prior FAILED banner may be CM-019 throttling)
