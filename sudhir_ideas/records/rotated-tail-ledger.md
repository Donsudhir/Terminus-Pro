# Idea: Rotated Tail Ledger

- Idea ID: `IDEA-0021`
- Slug: `rotated-tail-ledger`
- Category: system-administration
- Languages: TBD (candidate: go or python, shell)
- Created: 2026-07-19T10:58:40Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A log-shipping pipeline loses and duplicates events around file rotation; the solver must make delivery exactly-once under a battery of staged rotation regimes and prove it by reconciliation against an application-side ledger.

## Structural archetype

Exactly-once reconciliation under staged fault fixtures: the verifier replays scripted rotation storms (rename, copytruncate, size-burst, restart-mid-rotation) and grades a reconciliation between shipped events and the source-of-truth ledger — zero loss, zero duplication. The graded object is a delivery-accounting invariant across fault regimes, which no other portfolio idea uses.

## Novelty fingerprint

- Domain/system: a single-container log estate — an event-producing application with its own delivery ledger, a rotation daemon with per-service config, a tailer/shipper with persisted offsets, and a downstream store.
- Failure mechanism: tailer offsets keyed by path instead of file identity (replays or skips across rotation); rotation configured copytruncate for one service while the shipper assumes rename semantics — and the runbook asserts rename for all services; dedup keys built from second-rounded timestamps merge distinct events under burst load.
- Distributed fix topology: offset persistence identity, rotation-regime handling (or config reconciliation with correct semantics), and dedup key construction must all change; each alone still fails a different rotation regime in the matrix.
- Verifier/invariant surface: per-regime reconciliation (counts and content) between application ledger and downstream store, including restart-mid-rotation replays; the healthy low-volume service must stay exact.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): zone-serial-lag-weave (IDEA-0013) shares the sysadmin category but grades post-publish coherence of answers; this grades exactly-once accounting under fault injection — different invariant and investigation. The archived journal-compaction-replay task is WAL-compaction correctness inside one store; this is cross-process delivery accounting; noted as nearest archive neighbor for the full audit.
- Structural differentiator: correctness is an accounting identity over fault schedules, established by reconciliation tooling, not output equality of one program.
- Evidence paths and retrieval dates: local registry + active-task + submission-stem scan 2026-07-19 (no collision; journal-compaction-replay noted as distinct). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must find the path-keyed offsets, the copytruncate/rename semantic mismatch (against a runbook that says otherwise), and the timestamp-rounded dedup key — each visible only under a specific rotation regime.
- Synthesize: loss and duplication emerge from the interaction of rotation timing, offset identity, and dedup; no component is individually wrong-looking.
- Diagnose: symptoms are daily count mismatches after busy days; the pipeline has no error logs — everything "succeeds."
- Navigate coupling: keying offsets by inode fixes rename but *breaks* copytruncate (inode persists, offset now points past truncation); the solver must handle both regimes or reconcile config with true semantics, and the dedup fix must not start merging legitimate retransmissions the offset fix introduces.
- Reason beyond training: file-identity semantics across rotation regimes (inode reuse, truncation, fingerprinting) interacting with delivery accounting is systems reasoning, not a stock recipe — naive "use inode" answers fail the matrix.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. Offsets are keyed by path, so a rename rotation makes the tailer re-read the new file from the old offset — provable by regime-isolated replays.
2. One service rotates by copytruncate although the runbook claims rename fleet-wide; the shipper's resume logic silently skips the truncated region — the runbook claim is historically explainable (config drifted after the runbook was written) and falsifiable from rotation daemon state.
3. The dedup key rounds timestamps to seconds, merging distinct burst events — provable by ledger-vs-store content diffs on the burst fixture.
4. Fix locations: offset store (file-identity), shipper resume/regime logic, dedup key builder — three components.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): log interpretation and evidence triage (primary); hidden environment/process state; misleading documentation.
- Causal chain (4-8 dependent stages): (1) reconcile a failing day to characterize loss vs duplication per service; (2) replay the rename regime and catch the offset replay; (3) fix identity, replay copytruncate regime, catch the skip, falsify the runbook; (4) handle both regimes; (5) reconcile again, find burst-window merges, isolate the dedup key; (6) fix dedup; (7) run the full regime matrix with restarts and reconcile exactly.
- Heterogeneous evidence surfaces (>= 3): application ledger database, shipper offset files and logs, rotation daemon configuration and state, runbook documentation, downstream store contents.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "the downstream store drops writes" — falsified by store-side write logs matching what the shipper actually sent; H2 "the application ledger over-counts" — falsified by replaying the fixture generator whose emission schedule is known.
- Failing scenario and healthy control: high-volume rotating services fail under specific regimes; a low-volume service that never rotates during the window stays exact and must remain untouched by the fix (blocks "resend everything and dedup harder" hacks — its ledger has no duplicates to hide behind).
- Meaningful-action estimate (20-100, no busywork): ~40-70 (reconciliations, per-regime replays, three fixes with interaction handling, matrix verification).
- Determinism strategy: rotation storms are scripted schedules driven by the harness (no timers); file events, bursts, and restarts happen at fixed points; single container, offline.
- Domain and why this is not trivia: tests delivery-semantics engineering (file identity, resume logic, idempotence keys) that SRE teams are paid for; no single obscure fact unlocks it.

## Symptoms-only instruction sketch

"After busy days, the analytics store disagrees with the application's own ledger — some days short, some days over. Quiet services always match. Make the pipeline deliver every event exactly once through the archived rotation schedules, including when the shipper restarts mid-rotation, and show the reconciliation coming out exact."

## Decision notes

Captured 2026-07-19; sharpened to the exactly-once-reconciliation archetype in the same-day template review. Step 2a watchpoints: regime fixtures must be schedule-driven (no sleep races, per philosophy doc), and the runbook's false claim must be plausible config drift, not an arbitrary lie.
