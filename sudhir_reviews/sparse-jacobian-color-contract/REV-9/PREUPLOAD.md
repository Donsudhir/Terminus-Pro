# Pre-upload checklist (REV-9)

Reason: CM-019 AutoEval CodeExecution FAILED again (tb_check + difficulty_check empty logs); no human content feedback

Walk COMMON_MISTAKES and WHAT_WORKED before packaging. Tick every item (`[x]`)
or mark N/A with `[x]` and a note. `sudhir_task.py package` refuses unchecked
`- [ ]` lines unless `--force`.

- [ ] COMMON_MISTAKES preventions reviewed for this task type
- [ ] CM-007: test.sh uses `cd /tests` + PYTHONSAFEPATH + `--confcutdir` (or N/A)
- [ ] CM-006: behavioral tests / rubric cover claimed contracts (or N/A)
- [ ] Harbor evidence recorded (`sudhir_task.py evidence …`)
- [ ] Platform feedback captured in FEEDBACK.md when Needs Revision
- [ ] Form paste fields stored (DIFFICULTY.md, SOLUTION.md, VERIFICATION.md, RUBRIC.md)
- [ ] Strict Humanizer DSV audit stored and current
- [ ] Zip SHA will be recorded by package

DSV_HUMANIZER_REQUIRED: yes
READY_FOR_PACKAGE: no
