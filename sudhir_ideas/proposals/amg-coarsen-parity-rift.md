# Task Idea Proposal — amg-coarsen-parity-rift

Generated: 2026-07-22T21:16:45Z
Platform check: PASSED
Evidence: chat-2026-07-23 Snorkel Task Idea Proposal Check feedback pasted by Sudhir

## Paste-ready fields

### Task Idea Summary

An algebraic multigrid preconditioner produces different convergence curves and fine-grid solution digests when the same matrix is presented under two equivalent reorderings. Smoothness indicators and coarse-size summaries can look fine while the solution drifts past tolerance versus a fixed healthy ordering control. Repair hierarchy construction and apply so both orderings meet the same residual and solution-digest contracts without hard-coding one permutation.

### Idea Category

Scientific Computing

Normalized local category: `scientific-computing`

### Associated Skills

algebraic multigrid, sparse matrix reordering, smoother/coarse-grid coupling, iterative solver diagnostics, Fortran/C++/Rust numerics, residual-based verification, deterministic linear-algebra pipelines

### Task Tags

amg, multigrid, sparse-matrix, reordering, iterative-solvers

## Check feedback

Similarity PASS. Idea quality PASS (Decision: Accept; Verifiable: Accept; Well-specified: Uncertain; Solvable: Accept; Difficult: Accept; Interesting: Accept; Outcome-verified: Accept). Category alignment FAIL (selected scientific; suggested debugging) — non-blocking. Metadata similarity PASS.

## Inspiration provenance

- Source type: scientific computing / solver incident pattern
- Source reference: AMG coarsening parity under equivalent reorderings (inspiration only; distinct from sparse-jacobian-color-contract; 2026-07-23)
- Reuse boundary: Inspired by order-dependent AMG drift with healthy smoothness bait; no PETSc/Hypre patches or tests copied.
