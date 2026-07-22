# TASK-RPSP-001 Step 2a Plan

- Status: Completed with GO
- Task: `robust-predicate-scale-parity`
- Category: `scientific-computing`
- Languages: C, Rust, Fortran
- Construction allowed: Yes, under ADR-0006

## Goal

Produce a mechanically valid authoring specification, reviewer appendix, and structured evidence record proving that Robust Predicate Scale Parity is unique, bounded, scientifically substantive, deterministic, and resistant to one-pass or reference-copy collapse.

## Work order

1. Confirm the Gold Harness and canonical Sudhir roots.
2. Audit all active tasks and 157 submission archives for semantic collisions.
3. Research robust predicate correctness, compiler floating-point semantics, C/Rust/Fortran interoperability, and exact-verification strategies.
4. Draft and mechanically preflight a symptoms-only public instruction.
5. Enumerate the five hardness axes, all 21 anti-trivialization checks, and six rubric axes.
6. Commit at least four hidden discoveries and three distinct candidate fix topologies.
7. Select one topology with four distributed locations and a 0.34 test-concentration cap.
8. Complete the naming pass, construction manifest, 12-test plan, and exhaustive initial file commitments.
9. Initialize and record the Step 2a loop under `sudhir_ideas/specs`.
10. Save only the paths returned by the loop and run strict finalize lint.
11. Record GO or STOP in status, ADRs, logs, research, and the knowledge graph.

## Acceptance criteria

- Uniqueness audit finds no robust-predicate or tetrahedral-topology collision.
- Public instruction classifies `symptoms-only` with zero triggered specificity families.
- Public instruction passes the causal-connective disclosure check.
- Structured evidence derives score 0 FAIL and 0 WARN.
- Discovery budget contains at least four non-trivial facts.
- Topology enumeration contains three alternatives, each spanning at least three locations.
- Selected construction manifest contains four fix locations across C, Rust, and Fortran.
- Twelve planned tests are covered with each selected location controlling 4/12 tests, ratio 0.3333 under cap 0.34.
- Authoring spec passes strict v2 lint.
- No files are created under `sudhir_tasks/active/` during Step 2a.

## Outcome

- Attempt 1: 0 FAIL, 0 WARN
- Strict v2 lint: PASS
- Finalize: exit 0
- Full repository regression: 239 passed, 26 skipped
- Submission parity: current for 157 validated archives
- Decision: GO to Step 2b under ADR-0006
