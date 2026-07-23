# Idea: Device Node Migration Haze

- Idea ID: `IDEA-0033`
- Slug: `device-node-migration-haze`
- Category: system-administration
- Languages: c, rust
- Created: 2026-07-22T21:16:44Z
- Proposal check: pending
- Proposal form: `sudhir_ideas/proposals/device-node-migration-haze.md`
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A host migration tool copies a service root between staging trees and reports success from file counts and exit codes. After cutover, device-backed services fail to open required nodes, lose expected major/minor identity, or bind the wrong path, while ordinary file bytes look intact. A non-device healthy control tree still migrates cleanly. Make device nodes, permissions, and service open paths match the pre-migration contract, keep the file-only control green, and leave deliberately broken device fixtures rejected.

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
