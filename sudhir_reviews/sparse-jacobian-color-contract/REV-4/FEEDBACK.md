# Platform feedback — REV-4 intake (post REV-3 upload)

Source: Snorkel d9082cd8 + difficulty_check_artifact_sjcc.zip (2026-07-19)

## Difficulty
- ❌ EASY — requires at least MEDIUM
- terminus-claude-opus-4-8: 100% (5/5)
- terminus-gpt5-5: 80% (4/5)
- nop 0%, oracle 100% (3/3)
- Solvable: yes

## Unit tests
All 10/10 except test_k04 at 9/10.

## Instruction sufficiency
✅ PASS (structural-coefficient wording from REV-3 held)

## Failure analysis (gpt5 miss)
Agent fixed shared-gauge / determinism / ledger but emitted scale-contaminated
sensitivities (coeff×scale) on k04. Near-miss ~12/13. No hacking.

## Diagnosis for REV-4
REV-3 A/D bury failed: frontier agents rewrite host `pick_entry` / evaluate path
to copy declared term coefficients, bypassing FD+coloring. CM-008 hit again.
Need operator-level sensitivity ≠ raw term numbers + deeper locus bury.

## Follow-up UI (2026-07-19 ~20:25)

Screenshot still shows Difficulty ❌ EASY (opus 100% / gpt5 80%), solvable,
AutoEval FAILED banner (treat as CM-004 unless difficulty stats absent).
Snorkel Language dropdown was set to Python — that is form mislabel; task
agent stack is Rust/C/Fortran. Standing policy ADR-0014/CM-011 recorded so
future *new* tasks never use Python-primary agent languages.
