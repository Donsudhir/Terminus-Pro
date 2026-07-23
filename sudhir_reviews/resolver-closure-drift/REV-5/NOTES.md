# REV-5 notes — resolver-closure-drift

Opened/implemented: 2026-07-23

## Why EASY

REV-4 QC disclosure + two shortcuts:
1. Agents could admit HeldPin/HeldLane under Mixed without fixing veil classification.
2. Broken quay ordered by serial; alder/birch/cedar/elm selection was already ascending, so sill-only agents often passed sorted() checks. Odd seeds even flipped reverse-sort back to ascending.

Instruction-sufficiency said "name the sort bug" — **rejected** (would worsen EASY). Kept sort as format contract; hardened code instead (CM-008).

## Hardening applied

- `sill.rs`: HeldPin/HeldLane always Context — requires veil to emit Alpha/Beta kinds.
- `quay.rs`: always emit reverse bytewise (name, version, source-id); no salt flip.
- Instruction: kept QC nouns (profiles, preview/withdrawn, constraint form, named edge cases, generated neighbors); slightly tightened prose.

## Harbor

- oracle 1x `2026-07-23__00-23-05` mean=1.0
- nop `2026-07-23__00-23-53` mean=0.0
- oracle 10x `2026-07-23__00-24-31`: 5 rewards@1.0 + 5 RuntimeError (CM-003 docker pool / permission-denied stop). Pass@10 reported 1.0 among completed trials. **Need `sudo snap restart docker` (or equivalent) then re-run 10x with `-n 1` before claiming Step 4 PASS.**

## Do not

- Do not add "lock writer also has a sort bug" to instruction.

## Harbor (complete)

- oracle 1x `2026-07-23__00-23-05` mean=1.0
- nop `2026-07-23__00-23-53` mean=0.0
- oracle 10x `2026-07-23__01-11-53` mean=1.0 Pass@10=1.0 (after Docker restart)
- Package sha256 recorded by package command
