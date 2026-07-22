# Pre-upload checklist (REV-3)

Reason: Platform QC FAIL repaired — schema/file disclosure (CM-002 / CM-018).

Walk COMMON_MISTAKES and WHAT_WORKED before packaging. Tick every item (`[x]`)
or mark N/A with `[x]` and a note. `sudhir_task.py package` refuses unchecked
`- [ ]` lines unless `--force`.

- [x] COMMON_MISTAKES preventions reviewed for this task type (CM-002, CM-018, CM-007)
- [x] CM-007: test.sh uses `cd /tests` + PYTHONSAFEPATH + `--confcutdir`
- [x] CM-006: behavioral tests / rubric cover claimed contracts
- [x] CM-018: normative report-schema.md + inline JSON keys + `data.store` named
- [x] Harbor evidence recorded (`sudhir_task.py evidence …`)
- [x] Platform feedback captured in FEEDBACK.md when Needs Revision
- [x] Form paste fields stored (DIFFICULTY.md, SOLUTION.md, VERIFICATION.md, RUBRIC.md)
- [x] Zip SHA will be recorded by package

READY_FOR_PACKAGE: yes
