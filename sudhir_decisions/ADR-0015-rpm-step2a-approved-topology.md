# ADR-0015: Approve the RPM Mixed-Language Columnar Topology

- Status: Accepted
- Date: 2026-07-19
- Task ID: TASK-RPM-001
- Related: ADR-0008, ADR-0010, ADR-0013, ADR-0014

## Context

The next task should expand portfolio coverage beyond scientific-computing and
build/dependency work while remaining hard-only, deterministic, offline, and
non-Python-primary. The captured `rowgroup-prune-mirage` idea originally read as
three independent database bugs. CM-010 requires more than a mechanically valid
Step 2a shape: the fix boundaries must resist absorption and each causal stage
must reduce uncertainty.

A six-scope uniqueness audit found no semantic collision. The nearest local
archive, `hybrid-search-latency`, grades retrieval quality and resource counters,
not correctness equivalence across columnar plans and storage generations.
Official Parquet and ORC documentation confirms that null validity, page/row-group
statistics, dictionary coding, and selective skipping form real correctness
contracts.

## Decision

1. Approve `rowgroup-prune-mirage` for construction as TASK-RPM-001 in category
   `data-processing`, using Rust and C++ for the agent-facing system and Python
   only for the verifier.
2. Realize one historical validity-authority migration across exactly three
   selected fix boundaries:
   - Rust fresh-summary production (`rust/src/ember/fold.rs::tilt_a`),
   - C++ archived selective admission (`cpp/src/harbor/veil.cpp::turn_b`),
   - C++ batch-lane evaluation (`cpp/src/lattice/rill.cpp::sweep_c`).
3. Preserve immutable archived stores and independently validate generated fresh
   stores. A reader-only or writer-only repair is not sufficient.
4. Retain selective reads and batch execution on healthy controls. Disabling an
   optimized path is not a valid repair.
5. Follow the exact v2 authoring inventory and construction manifest in
   `sudhir_ideas/specs/rowgroup-prune-mirage.md`. Any added, removed, renamed, or
   relocated task file or fix symbol requires a spec amendment before continuing.
6. Require exact single-location ablations for the committed overlapping 5/12
   subsets before Step 2b can be called complete.

## Evidence

- Six-scope uniqueness dossier:
  `sudhir_research/TASK-RPM-001-RESEARCH.md`.
- Step 2a attempt 1: 0 FAIL / 0 WARN, evidence contract v3.
- Strict v2 spec lint: PASS.
- Independent CM-010 attack: planner fallback, producer-only repair, batch-only
  repair, and causal-stage skipping all leave observable failures.

## Consequences

- Construction is unblocked only after the registry records uniqueness PASS and
  Step 2a GO.
- The custom format stays deliberately small: integer/string columns, fixed
  pages, count/sum, equality/range/null predicates, no joins, no full SQL parser,
  and no live service.
- The C++/Rust split must remain failure-bearing, not decorative.
- Tests grade answers, artifact semantics, and stable work counters, not source
  shape, self-reported success, or solver process.
- A task that cannot preserve the committed ablation topology or fit the bounded
  environment must return to Step 2a rather than grow into benchmark theater.
