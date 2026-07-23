# Idea: KV Cache Layout Serve Rift

- Idea ID: `IDEA-0035`
- Slug: `kv-cache-layout-serve-rift`
- Category: machine-learning
- Languages: c++, rust
- Created: 2026-07-22T21:16:44Z
- Proposal check: pending
- Proposal form: `sudhir_ideas/proposals/kv-cache-layout-serve-rift.md`
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

An offline inference stack loads exported weights and serves greedy decode for fixed prompts. Training-side export checks pass and short prompts match golden token sequences, but longer prompts diverge while cache-hit counters and latency summaries still look healthy. Short-prompt controls must remain unchanged. Make long-prompt decode match the golden sequences without breaking short controls or inventing a new model architecture.

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
