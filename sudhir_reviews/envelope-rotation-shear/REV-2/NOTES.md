# REV-2 notes — envelope-rotation-shear

Opened from Snorkel reviewer feedback on REV-1 upload.

## Fixes applied

1. **CM-015 rubric** — Rewrote UI paste to `Agent …, ±N` with ±5/±3/±2 tiers and four negatives (positives sum 27).
2. **CM-016 reward** — `echo 0 > /logs/verifier/reward.txt` immediately after `mkdir -p /logs/verifier` in `tests/test.sh`; skeleton + task-creation template updated.
3. **CM-017 golang pin** — Loosened `golang-go=2:1.19~1` to unpinned `golang-go`.
4. **CM-002 instruction** — Stated get-fail-on-substitute without recover, maintain re-encrypts older records, recover handles prior history.

## Harbor evidence (post-edit)

| Kind | Job | Mean |
| --- | --- | --- |
| oracle 1x | `2026-07-19__22-29-43` | 1.0 |
| NOP | `2026-07-19__22-31-21` | 0.0 |
| oracle 10x | `2026-07-19__22-31-51` | 1.0 (10/10) |

## Package

- Zip: `sudhir_tasks_ready_to_submit/envelope-rotation-shear.zip`
- SHA-256: `2b36c843d8c0e602c4aed178e2533f022300f6908aa60b1cea3b9dfac7aecb90`
- approve: PASS (collapse RC8 WARN — justify if asked)

## Next

- Re-upload zip to Snorkel.
- Paste REV-2 DIFFICULTY / SOLUTION / VERIFICATION / RUBRIC (Agent…, ±N format).
