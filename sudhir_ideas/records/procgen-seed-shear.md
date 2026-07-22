# Idea: Procgen Seed Shear

- Idea ID: `IDEA-0029`
- Slug: `procgen-seed-shear`
- Category: games
- Languages: TBD
- Created: 2026-07-19T10:58:41Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

Procedurally regenerated worlds differ from their originals at region borders for some seeds; RNG consumption order, neighbor sampling, and generation-cache invalidation interact across the pipeline.

## Novelty fingerprint

Not completed — idea rejected before uniqueness research.

## Collision audit

- Closest analogue: `lockstep-replay-fray` (IDEA-0020), same repository, same day.
- Structural differentiator: none sufficient. Both ideas are the deterministic-regeneration-divergence archetype in the games domain (ordering contracts + RNG stream consumption + divergence bisection). A new domain surface (procgen vs replay) is not a structural difference under the super-uniqueness gate.
- Evidence: portfolio archetype review of 2026-07-19 (see `sudhir_ideas/records/lockstep-replay-fray.md`).

## Decision notes

REJECTED 2026-07-19 during the same-day portfolio template review: structural duplicate of lockstep-replay-fray. Per registry policy the slug is never reused. The games-category slot was refilled with the archetype-distinct `save-lineage-exhume` (IDEA-0031, legacy-format migration/recovery).
