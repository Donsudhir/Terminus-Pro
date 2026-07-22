# Pre-upload checklist (REV-1)

Reason: ingest submission_ecea3323.json

Walk COMMON_MISTAKES and WHAT_WORKED before packaging. Tick every item (`[x]`)
or mark N/A with `[x]` and a note. `sudhir_task.py package` refuses unchecked
`- [ ]` lines unless `--force`.

- [ ] COMMON_MISTAKES preventions reviewed for this task type
- [ ] CM-007: test.sh uses `cd /tests` + PYTHONSAFEPATH + `--confcutdir` (or N/A)
- [ ] CM-006: behavioral tests / rubric cover claimed contracts (or N/A)
- [ ] Harbor evidence recorded (`sudhir_task.py evidence …`)
- [ ] Platform feedback captured in FEEDBACK.md when Needs Revision
- [ ] Form paste fields stored (DIFFICULTY.md, SOLUTION.md, VERIFICATION.md, RUBRIC.md)
- [ ] Zip SHA will be recorded by package

READY_FOR_PACKAGE: no
