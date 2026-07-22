# Pre-upload checklist (REV-2)

Reason: Step 3b generalization: generated fresh CSVs, removed test-side internal-authority narration, and added repeated-report byte verification.

Walk COMMON_MISTAKES and WHAT_WORKED before packaging. Tick every item (`[x]`)
or mark N/A with `[x]` and a note. `sudhir_task.py package` refuses unchecked
`- [ ]` lines unless `--force`.

- [x] COMMON_MISTAKES preventions reviewed for this task type
- [x] CM-007: test.sh uses `cd /tests` + PYTHONSAFEPATH + `--confcutdir`
- [x] CM-006: behavioral tests / rubric cover claimed contracts
- [x] Harbor evidence recorded (`sudhir_task.py evidence …`)
- [x] Platform feedback capture is N/A; this new task has not been submitted
- [x] Form paste fields stored (DIFFICULTY.md, SOLUTION.md, VERIFICATION.md, RUBRIC.md)
- [x] Zip SHA will be recorded by package

READY_FOR_PACKAGE: yes
