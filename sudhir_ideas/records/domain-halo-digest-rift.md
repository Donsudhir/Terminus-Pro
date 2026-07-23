# Idea: Domain Halo Digest Rift

- Idea ID: `IDEA-0041`
- Slug: `domain-halo-digest-rift`
- Category: scientific-computing
- Languages: Rust, C
- Created: 2026-07-23T13:10:08Z
- Proposal check: pending
- Proposal form: `sudhir_ideas/proposals/domain-halo-digest-rift.md`
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A partitioned PDE-like solver (C numerical kernels with a Rust partition orchestrator) looks healthy after a domain repartition: local residuals and per-rank norms stay within tolerance, and the orchestrator marks halo exchange synced. Global field digests and cross-rank checksums still diverge from a never-repartitioned twin on the same case, while fresh non-repartition runs must remain stable and byte-stable. Restore correct ghost-layer packing, shared-face ownership, and reduction ordering so repartitioned and twin trajectories agree on global digests and reduction contracts without hard-coding one partition map.

## Novelty fingerprint

- Domain/system: TODO — required before this idea can be approved.
- Failure mechanism: TODO — required before this idea can be approved.
- Distributed fix topology: TODO — required before this idea can be approved.
- Verifier/invariant surface: TODO — required before this idea can be approved.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue: TODO — required before this idea can be approved.
- Structural differentiator: TODO — required before this idea can be approved.
- Evidence paths and retrieval dates: TODO — required before this idea can be approved.

## Why it is hard (five hardness axes)

- Discover: TODO — required before this idea can be approved.
- Synthesize: TODO — required before this idea can be approved.
- Diagnose: TODO — required before this idea can be approved.
- Navigate coupling: TODO — required before this idea can be approved.
- Reason beyond training: TODO — required before this idea can be approved.

## Hidden discoveries (>= 3) and fix locations (>= 3)

TODO — required before this idea can be approved.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): TODO — required before this idea can be approved.
- Causal chain (4-8 dependent stages): TODO — required before this idea can be approved.
- Heterogeneous evidence surfaces (>= 3): TODO — required before this idea can be approved.
- Competing hypotheses and deterministic falsifiers (>= 2): TODO — required before this idea can be approved.
- Failing scenario and healthy control: TODO — required before this idea can be approved.
- Meaningful-action estimate (20-100, no busywork): TODO — required before this idea can be approved.
- Determinism strategy: TODO — required before this idea can be approved.
- Domain and why this is not trivia: TODO — required before this idea can be approved.

## Symptoms-only instruction sketch

TODO — required before this idea can be approved.

## Decision notes

Status changes are append-only in the registry history. Put durable technical rationale
here, but never claim uniqueness, GO, submission, or acceptance without evidence.
