# Idea: Columnar Prune Mirage

- Idea ID: `IDEA-0017`
- Slug: `rowgroup-prune-mirage`
- Category: data-processing
- Languages: rust, c++ (python verifier-only)
- Created: 2026-07-19T10:58:40Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

An existing mixed-language columnar store returns different answers for the
same query depending on its execution plan after a historical null-format
migration; archived stores, new writers, selective planning, and row/batch
execution must agree without retiring the fast paths.

## Structural archetype

Execution-plan forensics over one split producer/consumer contract: a historical
validity representation changed while persisted value planes remained backward
compatible. Rust production, C++ selective planning, and C++ batch execution
each retained a different partial model. The verifier grades archived and fresh
artifacts under every equivalent plan while proving that selective reads and
batch execution remain active on healthy data.

## Novelty fingerprint

- Domain/system: a Rust page writer/compactor and C++ planner/executor over a
	small versioned columnar format with persisted page bounds, explicit validity,
	per-page dictionaries, row scans, batch scans, and structured plan counters.
- Failure mechanism: one historical validity migration is half-applied. The
	producer derives summaries from the value plane before validity, the planner
	interprets persisted bounds under a different null domain, and one batch
	kernel applies validity after predicate selection.
- Distributed fix topology: producer summary construction, selective-plan
	admission, and batch predicate evaluation live at different typed authorities
	across Rust and two C++ roots. Archived stores cannot be rewritten, while
	generated fresh stores must persist correct summaries.
- Verifier/invariant surface: correct identical aggregates for archived and
	generated cases under every supported plan; independently valid fresh
	summaries; healthy cases still choose page skipping and batch execution and
	read fewer pages than full scans.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue: `Task_Ready_To_Submit/hybrid-search-latency.zip`, which has
	a selective retrieval path and work counters but grades retrieval quality,
	batching, caching, and latency rather than columnar artifact semantics or
	plan-independent query answers.
- Structural differentiator: the graded object is equivalence of every supported
	execution plan across immutable historical stores and newly produced stores,
	with the same validity authority carried through producer, planner, and
	executor boundaries.
- Evidence paths and retrieval dates: six-scope dossier in
	`sudhir_research/TASK-RPM-001-RESEARCH.md`, retrieved/scanned 2026-07-19;
	31 ideas, four active/compatibility roots, zero archived roots, and 159 local
	submission archives audited.

## Why it is hard (five hardness axes)

- Discover: plan forcing separates selective-read loss from batch-lane leakage;
	artifact inspection then reveals the producer-side validity disagreement.
- Synthesize: correct behavior spans a versioned producer artifact, persisted
	summaries, planner admission, and two execution kernels. No component carries
	the complete authority.
- Diagnose: the public symptom is that equivalent plans produce different
	business totals only for some historical stores; it does not name validity,
	bounds, dictionaries, or source locations.
- Navigate coupling: a producer-only fix cannot change archived stores; a
	planner-only full scan fails healthy selective-read controls; a batch-only
	mask cannot recover pages already skipped.
- Reason beyond training: standard null, min/max, and vectorization recipes do
	not determine this project's mixed-generation authority handoff. The solver
	must reconstruct it from artifacts and plan behavior.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. Mixed-generation pages retain enough origin/validity evidence to distinguish
	historical null placeholders from legitimate equal-valued rows; the data is
	not corrupt.
2. Fresh persisted page summaries include invalid lanes because their producer
	reads value bytes before the authoritative validity plane.
3. The selective planner evaluates archived bounds under a value domain that is
	inconsistent with the format generation and page-local dictionary evidence.
4. One batch predicate kernel selects lanes before applying validity, while the
	row path applies validity first.
5. Fix locations: Rust producer fold, C++ planner admission, and C++ batch lane
	evaluation in three module roots.

## Long-horizon investigation profile (new ideas)

- Weakness areas (primary first): SQL/execution-plan investigation;
	multi-component reasoning; partial failures; mistake recovery.
- Causal chain: (1) reproduce a plan-dependent total; (2) force the four plan
	combinations and split selective versus batch symptoms; (3) inspect page
	artifacts and validity coverage, falsifying random corruption; (4) repair
	fresh producer summaries, then verify archived failures remain; (5) align
	selective admission for archived pages; (6) isolate and repair batch lane
	validity; (7) sweep archived, generated, and healthy controls.
- Heterogeneous evidence surfaces: structured plan metrics, persisted page and
	summary artifacts, runtime query results, build/configuration, and code.
- Competing hypotheses: random artifact corruption is falsified by stable page
	checksums and correct full-row reads; broken plan forcing is falsified by
	healthy cases whose selected modes and page counts match requests.
- Failing scenario and healthy control: mixed-generation stores fail by plan;
	current-format sentinel-free and legitimate-sentinel stores remain correct and
	must continue using selective/batch paths.
- Meaningful-action estimate: 48-72 genuine actions.
- Determinism strategy: fixed archived stores, deterministic generated CSV
	inputs, frozen page size and cost policy, no threads or clocks, single offline
	container.
- Domain and why this is not trivia: the task tests storage-format evolution,
	query planning, and execution semantics, not recall of one SQL or file-format
	fact.

## Symptoms-only instruction sketch

"Finance and support pulled the same archived orders through the supported
execution modes and got different totals. Repair the system under /app so every
equivalent mode returns the same correct result for archived and newly ingested
cases. Keep selective reads and batch execution working on the healthy cases;
turning either fast path off is not a fix."

## Decision notes

Captured 2026-07-19; six-scope uniqueness audit completed 2026-07-19. The
independent CM-010 attack rejected the original three-independent-bug framing
and replaced it with one historical validity contract. Step 2a still must prove
the exact public contract, naming pass, non-substitutable typed boundaries, and
flipping-point concentration before construction.
