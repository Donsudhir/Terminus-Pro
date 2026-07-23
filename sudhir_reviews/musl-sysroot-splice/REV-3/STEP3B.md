# Step 3b — musl-sysroot-splice REV-3

Instruction-only CM-002 wording fix. Collapse WARNs are unchanged from REV-2
and remain PASS-with-justification:

| Signal | Verdict | Justification |
| --- | --- | --- |
| RC1/RC2 | PASS-with-justification | Oracle still repairs knit/pack/seal; predictability is inherent to named helpers already required by instruction. |
| CR1/CR2/CR8 | PASS-with-justification | Legacy task without construction manifest; frontier still 3 roots. |
| GX1 | PASS-with-justification | No new oracle comments; vocab-anywhere WARN pre-existing. |
| GX7 | PASS-with-justification | Path literals for helper bins are exercised by behavioral stub tests; instruction names `build_payload.sh` entrypoint. |
| dockerfile apt_hygiene | PASS-with-justification | Pre-existing two apt transactions for session tools vs build toolchain; not touched this REV. |
| agent.timeout_sec WARN | PASS-with-justification | Pre-existing budget; not part of this revision ask. |
