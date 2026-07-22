# TASK-SJCC-001 Research and Uniqueness Record

- Date: 2026-07-19
- Slug: `sparse-jacobian-color-contract`
- Status: uniqueness passed; Step 2a in progress
- Confidence: High for uniqueness; medium-high for construction feasibility until Step 2b

## Corpus uniqueness

### Idea registry

Compared against every idea in `sudhir_progress/registry.json` and `sudhir_ideas/records/`.

- Reserved scientific backlog (`certified-enclosure-drift`, `krylov-orthogonality-loss`, `llvm-numerical-contract-drift`, `reproducible-reduction-parity`) covers enclosure arithmetic, Krylov orthogonality, compiler numerical contracts, and reduction ordering — not sparse Jacobian compression.
- `robust-predicate-scale-parity` covers near-degenerate geometric predicates and tetrahedral topology, not finite-difference Jacobian estimation.
- No idea title, summary, or fingerprint mentions Jacobian coloring, CPR compression, or structurally orthogonal column partitions.

### Active and archived tasks

- Active: only `robust-predicate-scale-parity` (geometry predicates).
- Archived: empty.
- Upstream `tasks/` tree (`driftlens-calibrate-api`, `journal-compaction-replay`, `mothlight-courier-replay-triage`, `musl-sysroot-splice`) has zero matches for Jacobian, graph coloring, finite-difference compression, or CSR unpack contracts.

### Submission archives (157)

Stem audit for jacobian/color/finite-diff/CSR/seed/hessian terms found no semantic collisions.

- `matrix` appears only in PKI and plugin-ABI repair titles.
- `residual` appears only in `magnetometer-kalman-residual-debug` (filtering, not Jacobian estimation).
- Zip content scan of `instruction.md` / `task.toml` / README surfaces for `jacobian`, `graph color`, `finite diff`, `csr`, `Curtis`, and `Coleman` returned **zero hits**.

### Upstream corpus / index

`repo_tests/fixtures/submission_index.json` and the local `tasks/` corpus contain no Jacobian-coloring scientific tasks.

Conclusion: sparse finite-difference Jacobian estimation via structurally orthogonal column partitions, with metamorphic permutation/resume/scale parity, is unoccupied in this repository.

## Authoritative sources

### Curtis–Powell–Reid sparse Jacobian estimation

Source: https://doi.org/10.1093/imamat/13.1.117 (Curtis, Powell, Reid, 1974)

- Sparse Jacobians can be estimated with far fewer residual evaluations by grouping structurally orthogonal columns.
- Each group is probed with one seed vector; nonzero entries are recovered by unpacking the compressed difference.

Implication: compression correctness is a scientific invariant, not a cosmetic packing choice.

### Coleman–Moré graph coloring formulation

Source: https://doi.org/10.1137/0720013

- Structurally orthogonal column partitions correspond to a graph coloring problem on the column intersection graph.
- Ordering affects the produced coloring even when the chromatic number is fixed.
- Practical matrices are often unsymmetric; symmetry assumptions are unsafe.

Implication: treating a pattern as numerically or structurally symmetric is a real failure mode with deterministic metamorphic tests.

### Gebremedhin–Manne–Pothen survey

Source: https://doi.org/10.1137/s0036144504444711 and https://cscapes.cs.purdue.edu/coloringpage/abstracts/sirev.pdf

- Distance-1 / distance-2 coloring models unify Jacobian and Hessian estimation.
- Finite differences and automatic differentiation share the same partition/unpack contract.
- Incorrect partitions produce plausible dense-looking compressed vectors that unpack to wrong sparse matrices.

Implication: `J` and `J·v` parity under permutation and resume are strong verifier properties.

### Coleman–Garbow–Moré ACM TOMS software

Source: https://doi.org/10.1145/1271.1610 and Algorithm 618

- Production Fortran packages separate partition determination (`DSM`) from finite-difference estimation (`FDJS`).
- The partition is an input to estimation; a stale or resumed plan can silently reuse the wrong seed roster.

Implication: plan lifecycle and seed hygiene are legitimate cross-module defects, not harness trivia.

## Selected scientific story

A mixed-language residual sensitivity pipeline must keep four coordinated authorities consistent:

1. a C partitioner that only groups truly structurally orthogonal unknowns;
2. a Rust plan/seed boundary that clears and restores probe rosters without leakage;
3. a Rust magnitude/step policy scoped to the current independent residual batch;
4. a Fortran unpack/reindex stage whose sparse orientation matches the compression layout.

Observable failures are incompatible packed sensitivity reports and directional products across equivalent batches. Causes stay out of the public instruction.

## Closest analogue and differentiator

- Closest analogue: a textbook CPR/Coleman–Moré sparse Jacobian coloring exercise, or the reserved Krylov orthogonality idea.
- Differentiator: the solver must reconcile partition orthogonality, seed/plan lifecycle, scale policy, and unpack orientation across C, Rust, and Fortran. Dropping in a reference coloring routine cannot satisfy the distributed metamorphic contract.

## Risks

- A pure “implement CPR from a paper” collapse if the scaffold is blank-canvas; mitigate with an existing multi-module pipeline and distributed seeded defects.
- Golden dense Jacobians as answer keys; mitigate with independent directional probes and exact/rational residual families where feasible.
- Prompt nouns like `jacobian`/`color` on the fix path; mitigate with opaque symbols and a naming pass.
- Single-knob ε widening; mitigate by coupling scale policy to partition and unpack tests under the flipping-point contract.
