# TASK-RPM-001 — rowgroup-prune-mirage — Super-Uniqueness Dossier

- Idea: `rowgroup-prune-mirage` (IDEA-0017)
- Category: data-processing
- Languages: Rust and C++ (pytest is verifier-only)
- Archetype: execution-plan forensics over a split producer/consumer storage contract
- Research date: 2026-07-19
- Verdict: **no semantic collision found across the six required scopes**

## Novelty fingerprint

1. **Domain/system:** an existing mixed-language columnar store. Rust ingests and
   compacts versioned pages; C++ plans selective reads and executes row-at-a-time
   and batch scan paths. Persisted page summaries, validity state, per-page
   dictionaries, plan traces, and query results are all observable.
2. **Failure mechanism:** one historical null-representation migration is only
   half-complete. The producer derives page summaries from the value plane before
   applying validity, the planner evaluates persisted bounds with a different
   null domain, and one batch kernel applies validity after predicate selection.
   Mixed-generation compaction is the narrow trigger; ordinary current-format
   pages are the healthy control.
3. **Distributed fix topology:** producer summary construction, selective-plan
   admission, and batch predicate evaluation have different input authorities
   and live in Rust plus two C++ module roots. Archived stores cannot be rewritten,
   while fresh stores must carry correct summaries, so no reader-only or
   writer-only repair satisfies the complete matrix.
4. **Verifier/invariant surface:** correct and identical aggregates under every
   supported plan; archived mixed-generation stores remain readable; fresh
   ingests persist valid summaries; healthy data still uses page skipping and
   batch execution and reads fewer pages than its full-scan control.

## Collision audit — all six scopes

### 1. Idea registry (31 ideas)

Scanned `sudhir_progress/registry.json`, `sudhir_ideas/IDEA_INDEX.md`, and all
records on 2026-07-19. `changefeed-splice-skew` is the nearest database-domain
idea, but it grades crash/resume convergence of change application. It has no
optimizer, persisted page-summary, plan-equivalence, or split scan-path surface.
`feature-skew-horizon` concerns temporal ML leakage. **No semantic collision.**

### 2. Active tasks

Scanned `sudhir_tasks/active/` and compatibility `tasks/` (four task roots in
both views). Existing work covers geometric predicates, sparse sensitivities,
musl toolchain staging, and dependency resolution. Content search found no
row-group, page-summary, selective-plan, columnar, dictionary, or split-scan
incident. **No collision.**

### 3. Archived tasks

`sudhir_tasks/archived/` contains zero task roots on 2026-07-19. **No collision.**

### 4. Submission archives (159 local zips)

Content-scanned all zips under `Task_Ready_To_Submit/` and
`sudhir_tasks_ready_to_submit/` for `columnar`, `row.?group`, `zone.?map`,
`prun(e|ing)`, `vectorized`, `predicate rewrite`, `dictionary encod`,
`page stat`, and `query plan` on 2026-07-19. Most hits were unrelated helper
names or ordinary list pruning. The closest substantive hit was
`hybrid-search-latency.zip`, where `filter_prune_hits` is a retrieval-efficiency
counter inside a vector-search replay. It grades latency/quality guardrails,
not persisted column summaries, SQL-like predicate semantics, or equality of
row and batch plans. `feature-store-forensics.zip` grades feature snapshot,
cache, and replay lineage. `urban-rideshare-equilibrium.zip` uses `zone_map` as
fixture terminology. **No semantic collision.**

### 5. Upstream/local corpus surfaces

Scanned the unpacked compatibility task corpus, submission index, task names,
and all solver-facing text available in this workspace. No task combines a
mixed-generation columnar format, validity migration, persisted min/max page
summaries, selective pruning, and row-versus-batch plan equivalence. The nearest
broad class is database replay/recovery, whose graded object is state convergence
rather than query-plan independence. **No semantic collision.**

### 6. Current external technical research

Official sources retrieved 2026-07-19:

- Apache Parquet, *Nulls*,
  https://parquet.apache.org/docs/file-format/nulls/ . Nullity is encoded
  separately through definition levels and null values are not encoded in the
  data stream. This grounds the distinction between validity and value planes.
- Apache Parquet, *Page Index*,
  https://parquet.apache.org/docs/file-format/pageindex/ . Per-page lower and
  upper bounds permit selective page skipping, and their ordering semantics are
  part of the file metadata contract.
- Apache ORC, *ORC Specification v1*,
  https://orc.apache.org/specification/ORCv1/ . ORC records a PRESENT stream,
  per-row-group statistics, `hasNull`, dictionary encodings, and uses statistics
  for predicate pushdown. The specification explicitly notes that multi-stream
  index positions are error-prone.

These sources establish the engineering realism but are not benchmark tasks.
A public-web task search was not treated as authoritative beyond the repository's
curated 159-archive corpus; no collision claim is inferred from absence alone.

## Closest analogue and structural difference

- **Closest analogue:** local `hybrid-search-latency.zip`.
- **Shared surface:** both retain a fast selective path and expose work counters.
- **Structural difference:** the analogue repairs retrieval batching, caching,
  shard targeting, and resource counters. TASK-RPM-001 reconstructs one
  versioned null contract across a storage producer, persisted summaries, a
  selective planner, and two execution kernels, then proves answer equivalence
  without retiring fast paths.
- **Why this is not a rename or language swap:** the graded object differs.
  Retrieval quality/latency can be correct with one selected path; this task
  quantifies over every equivalent query plan and over both archived and newly
  produced storage artifacts.

## Independent CM-010 semantic attack

### Can one fix location absorb another?

- A planner-only full scan cannot pass healthy controls that require selective
  reads and it cannot repair fresh persisted summaries inspected independently.
- A producer-only repair cannot change immutable archived mixed-generation
  stores and cannot stop the batch kernel from treating invalid lanes as values.
- A batch-only mask cannot restore pages the planner already skipped.
- A shared-reader redesign is a valid alternative, but it still requires edits
  at the producer artifact boundary and at both planner/executor call sites; it
  does not reduce the task to one location.

### Can a causal stage be skipped?

- Plan forcing is needed to separate selective-read loss from batch-lane leakage.
- Artifact inspection is needed to distinguish writer metadata from planner
  interpretation; answers alone leave both hypotheses live.
- Fresh ingest is needed to prove the producer side, while archived stores prove
  backward compatibility.
- Healthy selective controls are needed to reject the otherwise-valid broad
  workaround of disabling fast paths.

The stages are therefore uncertainty-reducing, not a bundle of optional bug
searches.

## Authoritative technical implications

- Validity is an independent authority. Sentinel-shaped data can be legitimate;
  a consumer cannot infer nullity from value bytes after a format adds explicit
  validity.
- Persisted bounds are executable correctness metadata when a planner uses them
  to skip pages. A writer and reader must agree on both value ordering and null
  semantics.
- A fast scan kernel may use a different implementation while remaining
  semantically equivalent to the row path. Tests should compare outcomes and
  stable work counters, not source structure.

## Construction feasibility and anti-collapse risks

- Scope is intentionally small: signed integer amount, dictionary-coded region,
  count/sum aggregates, equality/range/null predicates, fixed-size pages, and
  four plan modes. No joins, group-by, SQL parser, compression library, or live
  database service.
- Rust owns persisted page production and compaction; C++ owns planning and
  execution. Python is verifier-only, satisfying ADR-0014/CM-011.
- The instruction names one rebuild command and one end-to-end audit command.
  It describes plan-independent outcomes and fast-path preservation, not null
  sentinels, validity maps, bounds, dictionaries, or fix locations.
- Generated fresh inputs plus immutable archived stores block hardcoded answers
  and rewrite-everything repairs. Healthy work counters block disabling page
  skipping or batch scans.
- Tests parse produced artifacts and run binaries behaviorally; they do not grep
  source or trust self-reported status alone (CM-006).

## Uniqueness verdict

**PASS for the super-uniqueness gate.** The closest analogue and all six search
scopes are recorded. The failure mechanism, distributed topology, causal
investigation, and verifier invariant are materially distinct. This permits
Step 2a validation only; it does not itself authorize construction.
