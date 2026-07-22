# ADR-0018: Task Idea Proposal Check Before Uniqueness

- Status: Accepted
- Date: 2026-07-21
- Task ID: Repository-wide
- Related: ADR-0008, ADR-0010, ADR-0012, ADR-0016, WW-013

## Context

The Snorkel submission UI provides a Task Idea Proposal check before task
creation. It requires a 2–5 sentence summary, one category, 5–10 associated
skills, and 3–6 task tags. This inexpensive check can reject or redirect an idea
before uniqueness research, Step 2a, construction, or Harbor work consumes time.

The repository previously began with `idea new`, a six-scope uniqueness dossier,
and Step 2a. It did not model the platform proposal result, persist the exact
four fields, or guarantee that future agents stopped for Check feedback.

Sudhir also established a reusable inspiration ladder: real issues and bug
trackers, SWE-bench patterns, Terminal-Bench research, Unix/DevOps sources,
release notes, community signals, and systems books. These sources are valuable
for realism but create copying, category, saturation, and benchmark-contamination
risks unless their role is explicit.

## Decision

1. For the single candidate selected to enter task creation, the first external
   gate is the Snorkel Task Idea Proposal check.
2. The agent outputs only the four paste-ready fields first and then stops:
   Task Idea Summary, Idea Category, Associated Skills, and Task Tags.
3. After Check feedback returns, the idea receives a permanent idea record and
   the exact fields, verdict, feedback, evidence, inspiration provenance, and
   reuse boundary are stored under `sudhir_ideas/proposals/` and in the registry.
4. Proposal PASS is required before uniqueness PASS, Step 2a GO, or task
   registration. Existing established work is labeled `not-recorded` rather
   than retroactively blocked or given invented evidence.
5. Proposal PASS is only an early platform signal. It does not imply current
   eligibility, uniqueness, Step 2a GO, hard difficulty, solvability, approval,
   submission readiness, or acceptance.
6. Failed proposals are revised and rechecked or retained as rejected records;
   slugs and failed families are not silently recycled.
7. `web/idea-inspiration-sources.md` is read for every new proposal. Sources
   provide symptoms, environment shapes, and design principles only. Issue
   prose, benchmark instances, patches, tests, and copyrighted exercises are not
   copied. Current category/structure blocks and six-scope uniqueness override
   source popularity.

## Consequences

- Cheap platform feedback happens before expensive local validation.
- The generated board exposes proposal status independently from uniqueness and
  later platform outcome.
- Existing captured-but-unvalidated ideas must complete the proposal check
  before recording future uniqueness PASS.
- Bulk seed banks remain optional inspiration tools; selecting a seed never
  bypasses the four-field check.

## Rollback

A superseding ADR may demote the proposal check to advisory if the platform
removes or materially changes the form. Existing proposal evidence remains
readable. Rollback must not infer PASS for pending/failed proposals or delete
failed idea provenance.
