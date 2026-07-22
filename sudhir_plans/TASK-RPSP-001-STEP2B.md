# TASK-RPSP-001 Step 2b Construction Plan

- Date: 2026-07-18
- Status: Completed with PASS
- Canonical task root: `sudhir_tasks/active/robust-predicate-scale-parity`
- Approved spec: `sudhir_ideas/specs/robust-predicate-scale-parity.md`
- Governing decision: ADR-0006
- Baseline branch/head: `main` at `3384fcb`
- Starting worktree: 81 existing changed or untracked entries; task root absent

## Scope

Construct the complete standard single-container task approved in Step 2a, then complete only the Step 2b gate chain: preflight, oracle once, and NOP. Do not run the Step 4 oracle stress, final packaging, approval, or submission-output generation.

## Construction sequence

1. Create the standard task metadata, output contract, symptoms-only instruction, local construction manifest, and edit ledger.
2. Create a compile-at-runtime environment using a digest-pinned canonical Rust base with C, Fortran, Python verifier, tmux, and asciinema dependencies installed at image build time.
3. Implement the healthy dyadic parser, exact C refinement, bounded tetrahedron enumeration, stable JSON writer, adjacency/topology logic, and all substantive decoys.
4. Seed only the four approved baseline defects at:
   - `native/series.c::eval_band`
   - `host/plate.rs::map_state`
   - `host/frame.rs::clear_frame`
   - `analysis/pack.f90::fold_rows`
5. Implement twelve opaque property tests using exact rational arithmetic and generated affine variants.
6. Implement a deterministic oracle that substantively repairs exactly the four selected locations and rebuilds/runs the pipeline.
7. Confirm discovery budget and solver-visible discoverability manually.
8. Run the canonical Step 2b preflight against the Sudhir task root.
9. Run Harbor oracle once and NOP, without the Step 4 10x stress.
10. Save compact evidence, update status, logs, and knowledge graph, then stop for Step 3b review.

## Design boundaries

- Standard task, no milestones, no UI, no compose, no network.
- C provides conservative fast certification plus supplied exact integer refinement.
- Rust provides parsing, FFI state handling, per-input coordinate context, bounded enumeration, adjacency, and deterministic report generation.
- Fortran provides parity-preserving row canonicalization and incidence totals.
- Small dyadic point sets keep exact test arithmetic and exhaustive enumeration bounded.
- Expected values are derived in verifier code, not stored in solver-visible fixtures.
- `construction_manifest.json` is added at task root because the canonical Sudhir path is outside legacy `tasks/`; it is authoring-only and excluded from packaging.
- The approved source-tree `environment/output/.gitkeep` commitment is superseded by current package-hygiene policy, which forbids precomputed output directories under `environment/`. Runtime creates `/app/output` instead.

## Acceptance criteria

- At least 20 substantive files under `environment/`, excluding Dockerfile and compose.
- Static checks: PASS.
- Dockerfile checks: no blocking finding.
- Collapse stack: no FAIL; symptoms-only instruction retained.
- Packaging preview and checksum sentinel: PASS.
- Oracle sanity: 1.0 on one run.
- NOP baseline: 0.0.
- No task source outside the canonical Sudhir task root.
- No Step 4 packaging or 10x oracle run.

## Outcome

- Task source: 47 files, 36 environment files excluding Dockerfile/compose
- Integrity-tracked files: 44
- Static: PASS with no warning
- Dockerfile: PASS
- Collapse: 0 FAIL, 0 WARN, 23 PASS
- Packaging preview: PASS
- Oracle: local 12/12 and Harbor 1.0 with zero errors
- NOP: local 0/12 and Harbor 0.0 with zero errors
- Location ablations: A, B, C, and D each fail exactly their declared four tests
- Registry: revision 2, phase `review`
- Full repository regression: Ruff PASS, pytest 240 passed and 26 skipped
- Final archive: not created
- Next action: Step 3b paper review
