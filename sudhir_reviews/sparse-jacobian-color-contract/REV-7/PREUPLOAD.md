# Pre-upload checklist (REV-7)

Reason: CM-019 CodeExecution FAILED / ThrottlingException; timeout+memory hedge and re-upload for difficulty remeasure

Walk COMMON_MISTAKES and WHAT_WORKED before packaging. Tick every item (`[x]`)
or mark N/A with `[x]` and a note. `sudhir_task.py package` refuses unchecked
`- [ ]` lines unless `--force`.

- [x] COMMON_MISTAKES preventions reviewed for this task type
- [x] CM-007: test.sh uses `cd /tests` + PYTHONSAFEPATH + `--confcutdir` (or N/A)
- [x] CM-016: test.sh writes early `reward.txt=0` after mkdir
- [x] CM-006: behavioral tests / rubric cover claimed contracts (or N/A)
- [x] CM-019: diagnosed empty difficulty before CM-008; Fast static siblings PASS
- [x] Harbor evidence recorded (`sudhir_task.py evidence …`) — oracle 1x `jobs/2026-07-21__06-59-26` mean 1.0; NOP `jobs/2026-07-21__07-00-10` mean 0.0; oracle 10x `jobs/2026-07-21__07-00-53` mean 1.0
- [x] Platform feedback captured in FEEDBACK.md when Needs Revision
- [x] Form paste fields stored (DIFFICULTY.md, SOLUTION.md, VERIFICATION.md, RUBRIC.md)
- [x] Zip SHA will be recorded by package

READY_FOR_PACKAGE: yes
