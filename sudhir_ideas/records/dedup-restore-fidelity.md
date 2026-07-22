# Idea: Dedup Restore Fidelity

- Idea ID: `IDEA-0027`
- Slug: `dedup-restore-fidelity`
- Category: system-administration
- Languages: TBD (candidate: go or c, shell)
- Created: 2026-07-19T10:58:41Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

Restores from a deduplicating backup store silently diverge from the source for trees containing hardlinks, sparse regions, and extended attributes; the solver must make backup-restore round trips faithful across a filesystem-feature matrix without breaking the store's deduplication guarantees.

## Structural archetype

Round-trip fidelity matrix: the graded object is an identity function — restore(backup(tree)) must equal the tree, byte-wise and metadata-wise, across a matrix of filesystem features, while store-level properties (dedup ratios, garbage-collection safety) must simultaneously hold. Grading a transformation's faithfulness against structural corpora is a shape no other portfolio idea uses.

## Novelty fingerprint

- Domain/system: a content-defined-chunking backup tool — chunker, object/chunk index, metadata catalog, restore materializer, and a garbage collector — with fixture corpora (hardlink farms, sparse VM images, xattr/ACL trees).
- Failure mechanism: the chunk index conflates identical content that must remain distinct at restore because per-file metadata context differs; the sparse-region map is recorded against pre-compression offsets but applied post-decompression; the hardlink table is keyed by device/inode captured from an intermediate staging copy rather than the source.
- Distributed fix topology: index identity semantics, sparse-map offset space, and hardlink capture point sit in three components; each alone leaves a distinct fidelity failure class, and a careless index fix destroys deduplication (caught by store-property checks).
- Verifier/invariant surface: byte- and metadata-exact restores across the corpus matrix; dedup ratio preserved on the dedup-heavy corpus; garbage collection after partial deletes never corrupts remaining restores.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): envelope-rotation-shear (IDEA-0022) also involves a storage system but grades forensic recovery of damaged data; here nothing is lost — the transformation itself is unfaithful. rotated-tail-ledger grades delivery accounting. No backup/restore idea exists in the portfolio.
- Structural differentiator: the solver must reason about which identities the store may merge (content) versus which it must preserve (structure/metadata) — an ontology question, not a bug hunt with one answer per symptom.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must find the identity conflation in the index, the offset-space mismatch in sparse maps, and the staging-copy inode capture — each manifesting as a different corruption signature discoverable only by structured round-trip experiments.
- Synthesize: fidelity spans chunking, indexing, cataloging, materialization, and GC; the failure signatures at restore time are far from their causes at backup time.
- Diagnose: symptoms are "restored VMs won't boot and some restored trees are subtly wrong"; the tool reports success everywhere.
- Navigate coupling: fixing index identity naively (key by file) destroys deduplication and fails store-property checks; fixing the sparse offset space changes chunk boundaries, which interacts with the index fix; hardlink fidelity depends on both.
- Reason beyond training: content-defined chunking is known lore, but the identity ontology (what may merge vs what must survive) across metadata contexts, sparse encoding, and link structure is a design problem specific to this store's layout.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. Restored files with identical content share one catalog entry whose metadata is last-writer-wins — provable by round-tripping two same-content files with different xattrs.
2. Sparse maps use pre-compression offsets applied after decompression, corrupting every hole beyond the first compressed boundary — provable with a crafted sparse fixture.
3. Hardlink groups are computed on a staging copy whose inodes differ from source, splitting or merging link groups — provable by comparing link topology before and after round trip.
4. Fix locations: chunk/catalog index semantics, sparse-map encoder or applier, hardlink capture stage — three components.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): hidden environment/filesystem state (primary); multi-component reasoning; tool selection.
- Causal chain (4-8 dependent stages): (1) reproduce a failed VM restore and diff restored trees structurally; (2) classify three distinct corruption signatures; (3) trace metadata clobbering to index identity conflation; (4) design an identity scheme that preserves dedup (store-property checks force this); (5) trace hole corruption to the offset-space mismatch; (6) trace link-topology drift to the staging capture; (7) round-trip the full matrix plus GC-after-delete scenarios.
- Heterogeneous evidence surfaces (>= 3): filesystem trees (structural diffs), binary store objects and indexes, catalog database, tool logs, GC state.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "storage-media corruption" — falsified by store checksums all passing; H2 "restore-target filesystem lacks features" — falsified by round-tripping onto the identical filesystem the fixtures came from.
- Failing scenario and healthy control: hardlinked, sparse, and xattr-bearing corpora corrupt; the plain-file corpus round-trips exactly and must continue to, with its dedup ratio intact (blocks "store every file whole with its own metadata" — that fails the dedup-ratio property).
- Meaningful-action estimate (20-100, no busywork): ~45-75 (structural diffing, signature classification, three isolations, identity redesign, matrix + GC verification).
- Determinism strategy: fixture trees are generated with fixed inodes/ordering by the harness; no timestamps in graded comparisons except those the tool must preserve (fixed values); single container, offline.
- Domain and why this is not trivia: tests storage-system identity ontology and filesystem-feature semantics — core infrastructure engineering — not recall of one syscall flag.

## Symptoms-only instruction sketch

"Disaster-recovery drills keep failing: restored virtual machines won't boot, and some restored project trees behave differently from the originals even though every file's content looks right at a glance. Plain document folders restore perfectly. Make restores faithful for everything in the drill archive — and the store must keep deduplicating as well as it does today, including after old backups are pruned."

## Decision notes

Captured 2026-07-19; fingerprinted same day. Step 2a watchpoints: the dedup-ratio and GC-safety property checks are what keep the identity fix honest — without them the task collapses to "copy trees verbatim"; fixture corpora must be harness-generated for inode determinism.
