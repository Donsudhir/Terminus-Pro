# envelope-rotation-shear — REV-3 Step 4

- Date: 2026-07-19
- Decision: **APPROVED WITH DOCUMENTED WARNINGS**
- Task language: Go only; Python is verifier infrastructure and must not be selected as the platform language

## Evidence

| Gate | Result | Evidence |
| --- | --- | --- |
| Spec lint | PASS | amended authoring spec |
| Static checks | PASS | REV-3 current tree |
| Dockerfile checks | PASS | REV-3 current tree |
| Collapse | WARN | 0 FAIL, 2 justified WARN, 21 PASS |
| Integrity | PASS | 57-file checksum verified |
| Oracle 1x | 1.0 | `jobs/2026-07-19__23-51-22` |
| NOP pre-review | 0.0 | `jobs/2026-07-19__23-52-55` |
| Oracle 10x | 10/10, 0 exceptions | `jobs/2026-07-19__23-56-00` |
| Post-stress NOP | 0.0 | `jobs/2026-07-19__23-58-50` |
| PREUPLOAD | PASS | `PREUPLOAD.md` |
| Zip validation | PASS | package driver |
| Manifest verification | PASS | approval gate |
| Source/zip parity | PASS | approval gate |
| Authoritative approval | PASS | no blocking failures |

## Infrastructure retry

The first high-concurrency stress attempt, `jobs/2026-07-19__23-55-03`, completed eight oracle trials at reward 1.0 and produced two Docker setup exceptions before verifier execution. Both exceptions were `all predefined address pools have been fully subnetted`, the known CM-003 host condition. No test failed. After task-scoped Docker cleanup and a successful network-allocation probe, the full stress was rerun at concurrency two and passed 10/10 with zero exceptions. Only `2026-07-19__23-56-00` is final oracle stress evidence.

## Warning adjudication

- **RC8:** four oracle targets are evenly distributed across four roots at 25% each. The WARN comes from short pre-fix typed-boundary files, not concentration. CR2, RC7, and GX3 confirm distribution and substantive work.
- **GX6:** three connectives in 245 words describe observed timing and public behavior. RC6 remains symptoms-only and no internal cause, algorithm, authority representation, or patch site is disclosed.

Both warnings are fully justified in `STEP3B.md`; padding code or weakening the now-complete instruction would be incorrect.

## Package

- Archive: `sudhir_tasks_ready_to_submit/envelope-rotation-shear.zip`
- SHA-256: `670cac18709eecf34f899ce83125694e6fb93701940ec77453a40b5c65c50e4e`
- Members: 55
- Archive root: `instruction.md`, `task.toml`, `environment/`, `solution/`, `tests/`

## Upload instruction

Re-upload this archive and paste the REV-3 form fields. Select **Go** as the platform language. Do not select Python merely because pytest exists under `tests/`.
