# Long-Horizon Investigation Task Philosophy

## Purpose and scope

This is the default design doctrine for ideas captured after ADR-0013. It does
not retroactively invalidate approved, active, submitted, or grandfathered
work. It strengthens the existing hard-only, symptoms-only, distributed-fix
profile; it does not replace it.

A Terminus task should resemble one coherent production investigation. The
solver reconstructs state, tests assumptions, follows a causal chain, repairs
coupled boundaries, and verifies the complete outcome. Difficulty must come
from reasoning and coordination, not hidden trivia, arbitrary volume, or a
required ritual.

## Mandatory profile for new ideas

Every new Step 2a attempt must pre-commit an investigation profile with:

1. **Two to four weakness areas.** One is primary; the others reinforce the
   same incident. Never force all weakness areas into one task.
2. **A four-to-eight-stage causal chain.** Each finding must unlock the next
   investigation stage. A bundle of independent bugs is not a chain.
3. **At least three heterogeneous evidence surfaces.** Examples include code,
   runtime state, logs, configuration, documentation, database state, build
   artifacts, metrics, Git history artifacts, filesystem state, and network
   captures. Volume alone does not count.
4. **At least two plausible competing hypotheses.** Each must have a
   deterministic falsifier available to the solver. The task must not require
   the solver to make a prescribed wrong edit.
5. **A conditional-failure matrix.** Include at least one failing scenario and
   one nearby healthy control so broad symptom patches cannot pass.
6. **An estimated 20-100 meaningful terminal actions.** This is an authoring
   estimate and later calibration signal, never a verifier requirement. File
   reads, experiments, builds, queries, and checks count when they reduce
   uncertainty; repeated busywork does not.
7. **A deterministic reproduction strategy.** The task remains offline,
   single-container, repeatable, and non-UI. Timing luck and external services
   are forbidden.
8. **A domain-reasoning statement.** Explain why the task tests engineering in
   its domain rather than one obscure standard fact or vocabulary lookup.

The existing requirements still apply: a realistic existing system, a
symptoms-only public instruction, at least three non-trivial discoveries, at
least three coordinated fix locations, no single dominant test locus, and
outcome-based verification.

## Weakness-area portfolio

The weakness areas are a portfolio matrix, not per-task requirements:

- long-horizon causal debugging;
- misleading or conflicting documentation;
- multi-component or logical multi-repository reasoning;
- rare and conditional failures;
- hidden environment, process, filesystem, or terminal state;
- log interpretation and evidence triage;
- ambiguous production symptoms;
- race conditions and asynchronous ordering;
- measured performance and memory work;
- long-context state retention;
- tool selection;
- Git and history reasoning;
- infrastructure diagnosis;
- SQL and execution-plan investigation;
- security reasoning;
- cross-system refactoring;
- investigate-plan-implement-verify discipline;
- recovery from disproven hypotheses.

A healthy idea bank covers the matrix over time. A normal task selects only
what forms one believable incident.

## Three enforcement layers

### Task properties

Step 2a mechanically validates the investigation profile. Step 2b and the
verifier validate declared substrates and final behavior where practical.
Tests grade the resulting system, not the solver's command history.

### Portfolio dimensions

Weakness areas and domain substrates are local authoring metadata. They guide
idea-bank balance and reviewer attention. Do not invent unsupported platform
categories or subcategories for them.

### Trajectory diagnostics

Planning order, tool choice, repeated work, first-edit timing, and recovery from
a wrong hypothesis can only be assessed from agent trajectories. They may be
reported diagnostically when traces are available, but they must not affect the
task reward or be inspected by task tests.

## Construction patterns

- **Misleading documentation:** the stale claim must be plausible,
  historically explainable, and falsifiable by a deterministic experiment.
  Never use arbitrary lies or make documentation the only source of truth.
- **Logical multi-repository systems:** model independent components as
  separate roots inside one container. If Git history matters, reconstruct it
  at image-build time from bundled offline commits or patches; do not ship
  repository metadata that packaging excludes.
- **Race conditions:** use barriers, seeded schedulers, or explicit hooks. Do
  not use sleep-based races.
- **Partial failures:** test a narrow trigger plus neighboring healthy controls,
  restart/replay behavior, and a broad-fix counterexample.
- **Logs:** use several realistic sources with a small causal signal. Do not set
  byte, line-count, or noise quotas.
- **Performance:** preserve correctness first and compare stable work metrics,
  ratios, allocations, or generously bounded repeated measurements. Avoid a
  fragile one-shot wall-clock threshold.
- **Healthcare and enterprise domains:** ship valid, version-pinned synthetic
  fixtures. The hard part should be indexing, ordering, identity, migration,
  concurrency, integrity, or performance across a real pipeline, not recalling
  one FHIR field, HL7 segment, DICOM tag, ICD code, or SNOMED identifier.

## Anti-overengineering rules

Reject or simplify a candidate when:

- its weakness areas do not reinforce one incident;
- causal stages can be solved independently or in any order;
- the action estimate comes from repetitive commands or repository size;
- one grep, one config edit, or one standard recipe collapses the work;
- misleading documentation makes the task unfair rather than investigatory;
- a deterministic local harness cannot reproduce the claimed race or failure;
- a process requirement is being smuggled into outcome tests;
- domain terminology contributes obscurity but no engineering reasoning.

## Category policy

`debugging` and `software-engineering` remain blocked primary categories. The
investigation profile is cross-category: choose the allowed category describing
the task's actual intellectual core, such as system administration, security,
scientific computing, data processing, build and dependency management, or
machine learning. Do not disguise a generic repair task with an allowed label.

## Success criterion

The profile succeeds when agents fail for informative reasons: losing causal
state, trusting the wrong authority, stopping after a partial repair, choosing
a weak experiment, or verifying too shallowly. It fails when agents lose to
volume, trivia, flaky timing, hidden-instance guessing, or author-created
confusion.