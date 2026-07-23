# Idea: AEAD Epoch Bound Drift

- Idea ID: `IDEA-0039`
- Slug: `aead-epoch-bound-drift`
- Category: security
- Languages: c, rust, go
- Created: 2026-07-22T21:16:45Z
- Proposal check: pending
- Proposal form: `sudhir_ideas/proposals/aead-epoch-bound-drift.md`
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A local sealed-object store rewraps records across key epochs and verifies tags before open. After a routine epoch advance, some historical records open with the wrong binding, some valid records fail verification, and a shallow tag-valid counter stays mostly green. Freshly written current-epoch records must keep working, and deliberately corrupted controls must stay rejected. Restore open/rewrap behavior so epoch lineage, associated data binding, and reject/accept controls all agree.

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
