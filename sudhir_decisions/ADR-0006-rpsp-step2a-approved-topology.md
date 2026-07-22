# ADR-0006: Approve the RPSP Distributed Scientific Topology

- Status: Accepted
- Date: 2026-07-18
- Task ID: TASK-RPSP-001
- Supersedes: the provisional Step 2a-only scope in ADR-0002

## Context

ADR-0002 selected Robust Predicate Scale Parity for Step 2a but deliberately blocked construction. The Gold Harness is now green, the repository corpus has been audited, authoritative numerical and interoperability sources have been reviewed, and the current validation schema recorded a complete 0-F/0-W attempt.

Three distributed fix topologies were compared. A purely numerical certificate chain was vulnerable to reference-copy collapse. A pure symmetry-convention chain had strong geometry but weaker numerical breadth. The selected chain combines exact numerical decisions with project-specific status, lifecycle, and representation boundaries.

## Decision

TASK-RPSP-001 is approved to enter construction with this fixed topology:

1. `native/series.c::eval_band` owns conservative fast-decision certification.
2. `host/plate.rs::map_state` preserves the native refinement-required state.
3. `host/frame.rs::clear_frame` rebuilds magnitude context per independent input.
4. `analysis/pack.f90::fold_rows` preserves orientation parity while canonicalizing and folding incidence.

The task remains:

- primary category `scientific-computing`;
- C, Rust, and Fortran;
- deterministic, offline, and single-container;
- bounded to small dyadic point sets and brute-force tetrahedron enumeration;
- verified with exact rational determinant signs, affine-equivalent connectivity, handedness, adjacency, incidence, topology, and byte determinism;
- exposed through a symptoms-only public instruction.

Construction must begin with all four selected locations present. Changing the topology, deleting a language's scored role, exceeding the 0.34 test-concentration cap, or requiring an unbounded exact-arithmetic implementation requires a new Step 2a attempt or a superseding ADR.

## Evidence

- Validation attempt: 1
- Mechanical score: 0 FAIL, 0 WARN
- Strict v2 authoring-spec lint: PASS
- Discovery budget: 4
- Candidate topologies: 3
- Selected locations: 4
- Planned tests: 12
- Per-location concentration: 4/12 = 0.3333
- Corpus audit: 157 archives plus active tasks, no semantic collision
- Evidence file: `sudhir_ideas/specs/robust-predicate-scale-parity-attempt-1-evidence.json`
- Authoring spec: `sudhir_ideas/specs/robust-predicate-scale-parity.md`
- Reviewer appendix: `sudhir_ideas/specs/robust-predicate-scale-parity-reviewer.md`

## Consequences

### Positive

- Construction is mechanically unblocked.
- The task has one bounded scientific invariant across three necessary languages.
- Public reference code cannot solve the complete task unchanged.
- Test expectations can be derived exactly rather than stored as answer-shaped fixtures.

### Costs and risks

- Construction must provide a healthy exact-refinement scaffold.
- Dyadic fixtures need careful exact nondegeneracy checks.
- The Fortran layer must remain scientifically substantive and ABI-correct.
- NOP and location-ablation runs must prove the intended test distribution rather than merely documenting it.

## Next action

Create the Step 2b construction plan and initial canonical task snapshot under `sudhir_tasks/active/robust-predicate-scale-parity/`, then run cheap gates, oracle once, and NOP before paper review.
