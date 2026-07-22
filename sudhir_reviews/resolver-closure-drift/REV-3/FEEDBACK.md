# REV-3 reviewer feedback — resolver-closure-drift

Task UID: 4d74fca0-684f-4ace-a1c2-db55737f6c9a
Slug: resolver-closure-drift
Captured: 2026-07-20 (chat paste)

## Human reviewer (blocking)

Task itself holds up: difficulty numbers back the author (weaker eval model clears 3/5 while oracle stays clean); environment, tests, and oracle check out. Only send-back is the rubric (quick mechanical fixes).

1. Rubric needs at least three negative criteria (saw two: hand-write lockfile; tamper tests/reward). Add at least one more undesirable behavior (e.g. network calls or writing outputs by hand outside the tool).
2. Rubric lines must start with `Agent` and end with `, <score>` — not score-first bullets.

Minor (optional): one short instruction sentence nudging solvers toward repository branches as where the two compatibility behaviors live, without giving the fix away.

## Platform difficulty / solvability (same round)

Difficulty: MEDIUM
Status: Solvable (all tests passed by at least one agent run)

Agent Performance:
- terminus-claude-opus-4-8: 100.0% (5/5)
- terminus-gpt5-5: 60.0% (3/5)

Reference: nop 0.0% (0/1); oracle 100.0% (3/3)

Unit tests: r01–r04,r07,r08,r12 = 10/10; r05,r06,r09–r11 = 8/10

## Instruction-sufficiency analysis (advisory)

Two failed trials fixed profile compatibility in `sill.rs` but missed lock sort order in `wire/lock.rs` (5/12 tests). Trials disagree on whether the sort contract was already clear. Human send-back did **not** require naming a second defect or the writer path; keep sort as stated contract and do not over-hint.

## Resolution plan (REV-3)

- Rewrite UI rubric to CM-015 / `TASK_PROPOSAL_RUBRIC.md` shape; ≥3 negatives; mixed severity.
- Optional soft branch nudge in `instruction.md` only.
- Do not name `wire/lock.rs` or declare sorting as a second known bug.
