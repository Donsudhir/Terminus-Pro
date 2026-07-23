# Harbor evidence — musl-sysroot-splice REV-3

Instruction-only CM-002 wording fix (ledger vs LANE_TAG stdout). No solution/test/env logic edits.

| Kind | Job | Mean |
| --- | --- | --- |
| oracle 1x | `jobs/2026-07-23__00-49-18` | 1.0 |
| NOP | `jobs/2026-07-23__00-49-51` | 0.0 |
| oracle 10x | `jobs/2026-07-23__01-03-41` | 1.0 (10/10, 0 exceptions) |
| post-10x NOP | `jobs/2026-07-23__01-07-53` | 0.0 |

Note: snap Docker still denies compose-down kill; trials themselves scored cleanly with expanded address pools + serial `-n 1`.

- `oracle_1x`: job `2026-07-23__00-49-18` mean=1.0 at 2026-07-22T19:37:52Z (jobs/2026-07-23__00-49-18)

- `nop`: job `2026-07-23__00-49-51` mean=0.0 at 2026-07-22T19:37:52Z (jobs/2026-07-23__00-49-51)

- `oracle_10x`: job `2026-07-23__01-03-41` mean=1.0 at 2026-07-22T19:37:52Z (jobs/2026-07-23__01-03-41)
