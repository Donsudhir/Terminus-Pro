# Pre-upload checklist (REV-8)

Reason: reviewer FNV-1a digest documentation, hash-locked verifier deps, schema_version + runtime.conf step tests

Walk COMMON_MISTAKES and WHAT_WORKED before packaging. Tick every item (`[x]`)
or mark N/A with `[x]` and a note. `sudhir_task.py package` refuses unchecked
`- [ ]` lines unless `--force`.

- [x] COMMON_MISTAKES preventions reviewed for this task type (CM-024 digest boundary)
- [x] CM-007: test.sh uses `cd /tests` + PYTHONSAFEPATH + `--confcutdir` (or N/A)
- [x] CM-016: test.sh writes early `reward.txt=0` after mkdir
- [x] CM-006: behavioral tests / rubric cover claimed contracts (or N/A)
- [x] CM-024: FNV-1a closed-object digest documented; hash-locked verifier deps; config tests
- [x] Harbor evidence recorded (`sudhir_task.py evidence …`) — oracle 1x `jobs/2026-07-23__00-46-04` mean 1.0; NOP `jobs/2026-07-23__00-46-35` mean 0.0; oracle 10x `jobs/2026-07-23__00-56-36` mean 1.0 (10/10)
- [x] Platform feedback captured in FEEDBACK.md when Needs Revision
- [x] Form paste fields stored (DIFFICULTY.md, SOLUTION.md, VERIFICATION.md, RUBRIC.md) + DSV-HUMANIZER-AUDIT.json
- [x] Zip SHA will be recorded by package

READY_FOR_PACKAGE: yes
