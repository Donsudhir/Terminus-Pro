# Idea: Input Ring Physics Desync

- Idea ID: `IDEA-0034`
- Slug: `input-ring-physics-desync`
- Category: games
- Languages: c++, rust
- Created: 2026-07-22T21:16:44Z
- Proposal check: pending
- Proposal form: `sudhir_ideas/proposals/input-ring-physics-desync.md`
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A headless game simulation records inputs and claims deterministic replay. Fresh live sessions look fine, but replays of the same seed diverge in entity state digests after a few hundred ticks, while a short healthy-control replay stays bit-stable. Tick-count overlays remain green. Restore determinism so failing replays match the recorded outcome digests without breaking the short healthy controls or accepting approximate physics.

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
