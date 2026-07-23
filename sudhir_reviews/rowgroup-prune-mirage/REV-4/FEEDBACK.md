# Platform feedback — rowgroup-prune-mirage (fac356b4) — 2026-07-22

Source: `stb submissions feedback fac356b4-6394-4023-b296-30308827b30e`
Assignment state: NEEDS_REVISION
Zip on platform: rowgroup-prune-mirage (folder); difficulty MEDIUM after REV-4 reupload.

## Revision Notes (blocking)

This task is a banned shape under every honest reading, so it cannot be accepted as is. The instruction says to repair the system, and environment/cpp/src/harbor/veil.cpp line 20 carries a clear planted bug, the ternary reads b.op == Op::Equal ? b.x : b.x with both branches identical, which is debugging. Beyond that seeded defect the three supplied modules are missing the real mixed-generation logic, so the oracle rewrites environment/rust/src/ember/fold.rs, veil.cpp and environment/cpp/src/lattice/rill.cpp to add generation, origin-lane and liveness-marker handling. Building out a query operator and storage engine graded by functional behavior is software-engineering, and the category field is data-processing, all three of which are banned and blocked for net-new submissions. The reward comes from the loam audit output matching expected rows and totals, that is candidate code behavior, not a domain invariant recomputed by an independent oracle. Please redesign this around a genuine reasoning or derivation task with a neutral stub and a domain-invariant verifier, under an active non-banned category. Instruction length, rubric structure, writeups and determinism are otherwise fine.

## Difficulty (non-blocking relative to shape)

Difficulty: MEDIUM. Solvable. Claude 80% (4/5), GPT-5.5 40% (2/5). Oracle 100%, NOP 0%.
Instruction sufficiency: FAIL — convergent agent miss on veil.cpp RegionEqual/legacy conservatism (test_p14).

## QC

All quality_check axes PASS (behavior, schema, file refs, anti-cheat, etc.).

## Local classification

Primary blocker: banned shape (debugging flypaper + SE/query-engine construction + data-processing category + functional/candidate-code grading). Not a small instruction patch.
Secondary: remove identical ternary; instruction salience for region_eq if a redesign still keeps this mechanism (unlikely to clear acceptance alone).
In-flight data-processing exemption does not override the reviewer's shape/verifier redesign demand.
