# Pre-upload checklist (REV-1)

Reason: Initial construction REV-1 for gates, DSV, package

Walk COMMON_MISTAKES and WHAT_WORKED before packaging. Tick every item (`[x]`)
or mark N/A with `[x]` and a note. `sudhir_task.py package` refuses unchecked
`- [ ]` lines unless `--force`.

- [x] COMMON_MISTAKES preventions reviewed for this task type
- [x] CM-007: test.sh uses `cd /tests` + PYTHONSAFEPATH + `--confcutdir` (or N/A)
- [x] CM-006: behavioral tests / rubric cover claimed contracts (or N/A)
- [x] Harbor evidence recorded (`sudhir_task.py evidence …`)
- [x] Platform feedback captured in FEEDBACK.md when Needs Revision (N/A — first package)
- [x] Form paste fields stored (DIFFICULTY.md, SOLUTION.md, VERIFICATION.md, RUBRIC.md)
- [x] Strict Humanizer DSV audit stored and current
- [x] Zip SHA will be recorded by package

DSV_HUMANIZER_REQUIRED: yes
READY_FOR_PACKAGE: yes
