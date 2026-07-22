# Pre-upload checklist (REV-2)

Reason: Snorkel Needs Revision: rubric format/severity, reward initial write, golang apt pin, instruction grading contracts

Walk COMMON_MISTAKES and WHAT_WORKED before packaging. Tick every item (`[x]`)
or mark N/A with `[x]` and a note. `sudhir_task.py package` refuses unchecked
`- [ ]` lines unless `--force`.

- [x] COMMON_MISTAKES preventions reviewed for this task type (CM-002/015/016/017 applied)
- [x] CM-007: test.sh uses `cd /tests` + PYTHONSAFEPATH + `--confcutdir` (or N/A)
- [x] CM-006: behavioral tests / rubric cover claimed contracts (or N/A)
- [x] Harbor evidence recorded (`sudhir_task.py evidence …`) — oracle_1x `2026-07-19__22-29-43` 1.0; nop `2026-07-19__22-31-21` 0.0; oracle_10x `2026-07-19__22-31-51` 1.0
- [x] Platform feedback captured in FEEDBACK.md when Needs Revision
- [x] Form paste fields stored (DIFFICULTY.md, SOLUTION.md, VERIFICATION.md, RUBRIC.md)
- [x] Zip SHA will be recorded by package

READY_FOR_PACKAGE: yes
