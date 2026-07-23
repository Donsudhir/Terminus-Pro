# Pre-upload checklist (REV-2)

Reason: REV-1 Step 3b paper review after Step 2b PASS

Walk COMMON_MISTAKES and WHAT_WORKED before packaging. Tick every item (`[x]`)
or mark N/A with `[x]` and a note. `sudhir_task.py package` refuses unchecked
`- [ ]` lines unless `--force`.

- [x] COMMON_MISTAKES preventions reviewed for this task type
- [x] CM-007: test.sh uses `cd /tests` + PYTHONSAFEPATH + `--confcutdir` (or N/A)
- [x] CM-006: behavioral tests / rubric cover claimed contracts (or N/A)
- [x] Harbor evidence recorded (`sudhir_task.py evidence …`)
- [x] Platform feedback captured in FEEDBACK.md when Needs Revision
- [x] Form paste fields stored (DIFFICULTY.md, SOLUTION.md, VERIFICATION.md, RUBRIC.md)
- [x] Strict Humanizer DSV audit stored and current
- [x] Zip SHA will be recorded by package

DSV_HUMANIZER_REQUIRED: yes
READY_FOR_PACKAGE: yes

Notes:
- Platform feedback N/A (not yet submitted).
- Collapse WARNs justified in REV-2/STEP3B.md.
- Harbor: oracle 1x `2026-07-23__04-11-07` mean=1.0; NOP `2026-07-23__04-11-57` mean=0.0; oracle 10x `2026-07-23__04-13-43` mean=1.0 Pass@10=1.0.
