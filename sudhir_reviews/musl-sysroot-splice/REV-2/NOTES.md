# REV-2 notes — musl-sysroot-splice

## Reviewer ask (CM-006)

Verifier must prove fully static **musl** built through helpers — not merely
`No INTERP` or helper-name string presence in `build_payload.sh`.

## Changes

- Replaced string-only `test_entrypoint_wires_assembly_helpers` with:
  - `test_entrypoint_runs_stubbed_helpers_not_comments` (failing stubs; make
    cannot silently rebuild them)
  - `test_public_stage_matches_live_knit_pack_seal` (stage == live helper I/O)
  - `test_payload_uses_staged_musl_inputs` (bravo `libc.a` digest == image musl,
    `-static` + staged CRT, `strings` contains `musl`, no INTERP)
- Hardened `tests/test.sh` for CM-007 (`cd /tests` + `PYTHONSAFEPATH` +
  `--confcutdir=/tests`)

## Harbor evidence

| Kind | Job | Mean |
| --- | --- | --- |
| oracle 1x | `jobs/2026-07-19__14-50-19` | 1.0 |
| NOP | `jobs/2026-07-19__14-50-58` | 0.0 |
| oracle 10x | `jobs/2026-07-19__14-58-38` | 1.0 |
| post-10x NOP | `jobs/2026-07-19__15-03-08` | 0.0 |

Zip: `sudhir_tasks_ready_to_submit/musl-sysroot-splice.zip`
(mirror `Task_Ready_To_Submit/musl-sysroot-splice.zip`)
SHA-256: `5739b009e19f822817ceb48fa98f7142b9f41928a0b14d68016a02450ecc9ee6`

Re-upload to Snorkel submission `29a821f1`. Paste DIFFICULTY/SOLUTION/VERIFICATION/RUBRIC from this REV folder (difficulty/solution unchanged from prior form text).
