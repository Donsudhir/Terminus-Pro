# Task Idea Proposal — domain-halo-digest-rift

Generated: 2026-07-23T13:10:14Z
Platform check: PASSED
Evidence: chat-2026-07-23 Sudhir confirmed Snorkel Task Idea Proposal Check feedback PASS

## Paste-ready fields

### Task Idea Summary

A partitioned PDE-like solver (C numerical kernels with a Rust partition orchestrator) looks healthy after a domain repartition: local residuals and per-rank norms stay within tolerance, and the orchestrator marks halo exchange synced. Global field digests and cross-rank checksums still diverge from a never-repartitioned twin on the same case, while fresh non-repartition runs must remain stable and byte-stable. Restore correct ghost-layer packing, shared-face ownership, and reduction ordering so repartitioned and twin trajectories agree on global digests and reduction contracts without hard-coding one partition map.

### Idea Category

Scientific Computing

Normalized local category: `scientific-computing`

### Associated Skills

domain decomposition, halo exchange / ghost layers, parallel reduction ordering, mixed-language numerics (Rust + C), partitioned PDE solvers, floating-point checksum / field digests, deterministic scientific verification, partition ownership contracts

### Task Tags

halo-exchange, domain-decomposition, repartition, scientific-computing, field-digests, rust-c

## Check feedback

User-reported Check feedback PASS (chat-2026-07-23). Detailed platform rubric axes not pasted; treating as proposal=passed per Sudhir confirmation.

## Inspiration provenance

- Source type: scientific computing / partitioned solver incident pattern
- Source reference: Domain halo exchange + global reduce digest drift after repartition (inspiration only; 2026-07-23)
- Reuse boundary: Inspired by post-repartition local-green / global-digest-wrong failure shape; no PETSc/Trilinos/deal.II patches or tests copied; distinct from AMG coarsening, sparse Jacobian coloring, and mesh-checkpoint operator reuse.
