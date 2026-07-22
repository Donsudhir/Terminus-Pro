# Idea: Sparse Jacobian Color Contract

- Slug: `sparse-jacobian-color-contract`
- Internal ID: `TASK-SJCC-001`
- Category: scientific-computing
- Languages: c, rust, fortran
- Created: 2026-07-18T21:00:32Z
- Updated: 2026-07-19

## Problem in one line

A mixed-language residual sensitivity pipeline estimates sparse packed derivatives by compressing directional probes through a structurally orthogonal partition, then unpacking; equivalent permutations, resumed probe plans, and scale-equivalent batches produce incompatible packed matrices and directional products.

## Why it is hard (five hardness axes)

- Discover: The solver must recover that the partitioner assumes unsafe structural symmetry, that probe seeds leak across plan resume, that step magnitude is cached across independent batches, and that unpack uses the opposite sparse orientation from compression.
- Synthesize: Correctness spans a C partition/seed engine, Rust plan and magnitude authorities, a Fortran unpack/reindex stage, and a residual kernel — no module owns the full invariant.
- Diagnose: The instruction reports incompatible packed sensitivity and directional products, not “fix the coloring” or “clear the seed roster.”
- Navigate coupling: Fixing only the partition, only seed hygiene, only step policy, or only unpack still fails other metamorphic batches.
- Reason beyond training: Reference CPR coloring cannot repair the project-specific plan lifecycle, magnitude scoping, and Fortran orientation contract.

## Uniqueness (vs TB2, TB3, Snorkel Edition 1, 157 archives)

Verified 2026-07-19 across idea registry, active/archived tasks, 157 submission archives (stem + instruction content), upstream `tasks/`, and external literature. No sparse-Jacobian / graph-coloring / CPR-compression collision. Closest analogue is a textbook CPR exercise or reserved Krylov orthogonality; differentiator is the four-location cross-language metamorphic contract. Evidence: `sudhir_research/TASK-SJCC-001-RESEARCH.md`.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. Partitioner treats structurally symmetric patterns as numerically safe groups — `native/lane.c::mix_cols`.
2. Resumed probe plans reuse uncleared seed slots across partition boundaries — `host/vault.rs::bind_slot`.
3. Absolute step magnitude is derived from a residual norm cached at first plan build and reused after rescaling — `host/gauge.rs::reset_span`.
4. Compression packs by one sparse orientation; unpack reads the other — `analysis/knit.f90::merge_slots`.

## Symptoms-only instruction sketch

The residual lab under `/app` rebuilds a compressed sensitivity report from bundled residual batches. Ordinary batches look healthy, but equivalent batches that only permute unknowns, resume from a saved probe plan, or match directional probes can disagree on reconstructed packed entries and matrix-vector products. Scale-changed but algebraically equivalent batches also leave support mismatches or disagreement between the emitted packed matrix and the audit summary.

Correct the scientific pipeline so `/app/output/sensitivity_report.json` is deterministic and consistent for every bundled batch and its equivalent variants. Rebuild and run through `/app/bin/senslab`. Do not replace bundled inputs or hand-write the report.
