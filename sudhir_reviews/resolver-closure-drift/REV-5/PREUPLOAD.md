# Pre-upload checklist (REV-5)

Reason: CM-008 EASY opus80/gpt5100; harden veil+quay so sill-only cannot pass; keep QC contracts

Walk COMMON_MISTAKES and WHAT_WORKED before packaging. Tick every item (`[x]`)
or mark N/A with `[x]` and a note. `sudhir_task.py package` refuses unchecked
`- [ ]` lines unless `--force`.

- [x] COMMON_MISTAKES preventions reviewed for this task type
- [x] CM-007: test.sh uses `cd /tests` + PYTHONSAFEPATH + `--confcutdir` (or N/A)
- [x] CM-006: behavioral tests / rubric cover claimed contracts (or N/A)
- [x] Harbor evidence recorded (`sudhir_task.py evidence …`) — oracle 1x `2026-07-23__00-23-05`, nop `2026-07-23__00-23-53`, oracle 10x `2026-07-23__01-11-53`
- [x] Platform feedback captured in FEEDBACK.md when Needs Revision
- [x] Form paste fields stored (DIFFICULTY.md, SOLUTION.md, VERIFICATION.md, RUBRIC.md)
- [x] Zip SHA will be recorded by package
- [x] Strict Humanizer DSV audit stored and current

READY_FOR_PACKAGE: yes

DSV_HUMANIZER_REQUIRED: yes
