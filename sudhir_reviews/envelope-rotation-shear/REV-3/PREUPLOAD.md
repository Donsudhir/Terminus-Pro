# Pre-upload checklist (REV-3)

Reason: Platform difficulty MEDIUM because task metadata included Python despite a Go-only agent-facing core; agent analysis also found an instruction-sufficiency gap around preserving namespace-consistent generated reads while rejecting substitutions.

Walk COMMON_MISTAKES and WHAT_WORKED before packaging. Tick every item (`[x]`)
or mark N/A with `[x]` and a note. `sudhir_task.py package` refuses unchecked
`- [ ]` lines unless `--force`.

- [x] COMMON_MISTAKES preventions reviewed: CM-002 paired healthy/adversarial contract; CM-003 controlled concurrency; CM-006 behavioral checks; CM-007 verifier hardening; CM-011 Go-only agent language; CM-015/016/017 remain satisfied
- [x] CM-007: `tests/test.sh` uses `cd /tests`, `PYTHONSAFEPATH=1`, and `--confcutdir=/tests`
- [x] CM-006: public reads, recovery inventory, byte preservation, idempotence, tamper, and substitution are behaviorally tested; REV-3 rubric covers both generated-read and rejection sides
- [x] Harbor evidence recorded: oracle 1x `2026-07-19__23-51-22` = 1.0; oracle 10x `2026-07-19__23-56-00` = 10/10; post-stress NOP `2026-07-19__23-58-50` = 0.0
- [x] Platform feedback captured in `FEEDBACK.md`
- [x] Form paste fields stored in `DIFFICULTY.md`, `SOLUTION.md`, `VERIFICATION.md`, and `RUBRIC.md`
- [x] Package driver will record and verify the new zip SHA and member parity

READY_FOR_PACKAGE: yes
