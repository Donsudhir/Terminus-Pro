# Idea: Sealed Policy Ambient Leak

- Idea ID: `IDEA-0038`
- Slug: `sealed-policy-ambient-leak`
- Category: security
- Languages: c, rust
- Created: 2026-07-22T21:16:45Z
- Proposal check: pending
- Proposal form: `sudhir_ideas/proposals/sealed-policy-ambient-leak.md`
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

An offline privilege helper applies a sealed local policy, drops privileges, then performs sealed-path file operations for callers. After a policy reload and session restore, some callers still succeed on paths the sealed policy should deny, while others are denied incorrectly even though the policy text looks current. Surface health checks only count allow/deny totals and stay green. Make sealed-path enforcement and restored sessions agree so denied and allowed controls match the intended policy outcomes without weakening healthy allow cases.

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
