# Platform feedback — REV-5 remeasure / form revision intake (2026-07-19)

Source: Snorkel d9082cd8 difficulty summary after REV-5 zip upload.

## Difficulty
- ❌ EASY — requires ≥ MEDIUM
- Status: ✅ Solvable (all tests passed by at least one agent run)
- terminus-claude-opus-4-8: 80.0% (4/5)
- terminus-gpt5-5: 80.0% (4/5)
- nop: 0.0% (0/1); oracle: 100.0% (3/3)

## Failure breakdown
- nop: 1 other
- terminus-claude-opus-4-8: 1 other
- terminus-gpt5-5: 1 other

## Unit tests
Soft only (9/10): test_k02, test_k04, test_k05, test_k11. Rest 10/10.

## Instruction sufficiency
❌ FAIL on one trial class (probe-direction underspecification callout)

## Analysis on Agent Failures (instruction-sufficiency job)
- 2 trials, 0 passed (all-or-nothing reward 0.0) despite ~11/13 tests each
- Trial 2a3PvTN: invented probe direction [0.5, 0.75, 1.0, 1.25] instead of bundled [1.0, 0.5, 0.25, 2.0] (k02/k04)
- Trial q5xBwpB: unsolicited floor_pow2() on step; needed literal ref * 1e-6 * 0.5
- Hack check clean
- Recommendation from platform: name bundled probe directions in instruction; one failure was over-engineering

## Authoring / form goal
Revise DIFFICULTY + SOLUTION pastes to defend MEDIUM: multi-authority conjunction + last-mile exact contracts + all-or-nothing collapse from ~85% tests to 0 reward. Do not frame as easy near-miss.
