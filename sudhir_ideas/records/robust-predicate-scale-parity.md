# Idea: Robust Predicate Scale Parity

- Idea ID: `IDEA-0008`
- Historical task ID: `TASK-RPSP-001`
- Slug: `robust-predicate-scale-parity`
- Category: scientific-computing
- Languages: rust, c, fortran
- Created: 2026-07-18T20:55:36Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A near-degenerate geometric computation pipeline produces different topology under mathematically equivalent translations or scaling.

## Novelty fingerprint

- Domain/system: near-degenerate geometric topology under affine-equivalent inputs.
- Failure mechanism: adaptive numerical certification, uncertainty propagation, retained magnitude state, and row-fold parity diverge across language boundaries.
- Distributed fix topology: four coordinated locations across native C evaluation, Rust host state, Rust frame lifecycle, and Fortran packing.
- Verifier/invariant surface: exact determinant signs, local Delaunay validity, inversion absence, affine topology parity, and deterministic reports.

## Collision audit

Searched the idea registry, active and archived tasks, 157 submission archives,
the available upstream corpus, and current external technical references.

- Closest analogue: a conventional robust-predicate or exact-geometric-kernel repair task.
- Structural differentiator: replacing one predicate implementation is insufficient; the solver must reconcile certification, ABI state, lifecycle retention, and topology packing across three languages.
- Evidence: `sudhir_research/TASK-RPSP-001-RESEARCH.md` and `sudhir_ideas/specs/robust-predicate-scale-parity-attempt-1-evidence.json`.
- Result: no semantic collision found; uniqueness PASS is recorded in the registry.

## Why it is hard (five hardness axes)

- Discover: the public symptoms do not expose the four numerical and lifecycle defects.
- Synthesize: C certification, Rust state/ABI handling, and Fortran topology folding must agree.
- Diagnose: equivalent inputs drift in topology, but the instruction does not identify a cause or fix site.
- Navigate coupling: each isolated correction leaves a separate invariant family failing; no location controls a majority of tests.
- Reason beyond training: the task combines exact geometric reasoning with compiler, FFI, lifecycle, and representation semantics rather than a standard predicate recipe.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. The fast-decision certificate does not match the arithmetic semantics used by the native evaluator.
2. A native uncertainty state collapses at the cross-language boundary.
3. Magnitude context survives or resets at the wrong lifecycle boundary.
4. A Fortran row fold changes topology parity.

The approved topology distributes these discoveries over four locations and twelve tests, with each location controlling 4/12 tests.

## Symptoms-only instruction sketch

The canonical public contract is preserved in the approved authoring spec. It describes inconsistent signs, topology, invariance, and deterministic report behavior without naming the four causes above.

## Decision notes

- Step 2a attempt 1: GO, 0 FAIL and 0 WARN.
- Strict v2 authoring-spec finalize: PASS.
- Construction was executed and the task was submitted; current platform state is tracked separately from idea approval in the registry.
- Platform evaluation or solvability signals must not be rewritten as final acceptance.
