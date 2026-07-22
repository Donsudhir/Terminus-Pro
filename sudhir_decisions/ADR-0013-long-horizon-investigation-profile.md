# ADR-0013: Long-Horizon Investigation Profile for New Tasks

- Status: Accepted
- Date: 2026-07-19
- Task ID: Repository-wide
- Related: ADR-0007, ADR-0008, ADR-0010

## Context

The existing hard-only profile requires symptoms-only instructions, hidden
discoveries, distributed fix locations, and outcome verification. It does not
require those discoveries to form one causal investigation, represent
competing hypotheses, span heterogeneous evidence surfaces, or include healthy
controls. Idea generation already mentions long-horizon state and misleading
sources of truth, but the treatment is incomplete and conflicts with the
blocked `debugging` category in some web prompts.

The requested direction targets weaknesses seen in long production workflows:
state loss, premature symptom patches, stale documentation, partial failures,
log triage, races, performance, history, infrastructure, SQL, security, and
domain-rich enterprise systems. Forcing all of them into every task would
create incoherent and over-engineered tasks.

## Decision

1. Adopt `sudhir_knowledge/LONG_HORIZON_TASK_PHILOSOPHY.md` as the default
   design doctrine for ideas initialized after this ADR.
2. Add a local-only `investigation_profile` to Step 2a evidence. New validation
   loops require it; pre-existing loop state and historical evidence remain
   compatible.
3. Require two to four selected weakness areas, a four-to-eight-stage causal
   chain, at least three heterogeneous evidence surfaces, at least two
   competing hypotheses with falsifiers, failing and healthy-control scenarios,
   a deterministic strategy, a domain non-trivia statement, and an estimated
   20-100 meaningful-action horizon.
4. Treat the action horizon as an authoring estimate, not a task reward or a
   command-count gate.
5. Keep `debugging` and `software-engineering` blocked as primary categories.
   Route investigation-shaped ideas through the allowed category matching the
   real intellectual core.
6. Keep planning order, tool selection, and recovery behavior outside outcome
   tests. They may become advisory trajectory diagnostics only when reliable
   traces are available.
7. Do not add runtime substrate gates in this rollout. First collect evidence
   from new Step 2a profiles and pilot tasks; promote recurring, mechanically
   checkable failures through the existing CNI process.

## Consequences

- New ideas must show a coherent investigation architecture before construction.
- Existing active and submitted tasks are not invalidated.
- Idea banks become more diverse across agent weakness areas without turning
  each task into an eighteen-part checklist.
- The framework gains a measurable long-horizon design target while preserving
  deterministic, single-container, offline, outcome-based grading.
- Future runtime or trajectory checks require evidence from pilots rather than
  speculative framework growth.