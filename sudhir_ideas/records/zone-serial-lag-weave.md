# Idea: Stale Zone Serial Weave

- Idea ID: `IDEA-0013`
- Slug: `zone-serial-lag-weave`
- Category: system-administration
- Languages: TBD (candidate: python, shell, c)
- Created: 2026-07-19T10:56:27Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

Authoritative and caching DNS layers inside one container serve stale or inconsistent answers after zone regeneration; serial arithmetic, negative caching, and transfer hooks each hold part of the coherence invariant.

## Structural archetype

Staleness/coherence incident: multiple serving layers must converge after a publish event; the verifier grades post-publish answer coherence, not any single component. No other portfolio idea uses the cache-coherence shape.

## Novelty fingerprint

- Domain/system: an offline DNS estate in one container — a zone generator, an authoritative daemon (logical primary + secondary roots), and a resolver cache, wired by transfer/notify hooks.
- Failure mechanism: RFC 1982 serial-number wraparound arithmetic mishandled by the generator, a notify hook that fires before the zone file is durably swapped, and negative-cache TTL policy that pins NXDOMAIN past regeneration — three partial owners of one coherence invariant.
- Distributed fix topology: generator serial logic, transfer/notify hook ordering, and resolver negative-caching configuration/logic must change together; any single fix leaves a reproducible stale window.
- Verifier/invariant surface: post-regeneration answer coherence across all query paths (fresh names resolve, deleted names expire on schedule, serial monotonicity holds across wrap), with a healthy control zone that must remain untouched.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): no DNS/zone-coherence idea exists in the local portfolio; nearest internal shapes are generic config-repair tasks, which this differs from by requiring serial arithmetic reasoning and ordering repair, not knob setting.
- Structural differentiator: coherence is an emergent property of three subsystems; there is no single config block whose correction passes the matrix.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision). Full six-scope audit (157 archives, upstream corpus, external research) TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must find that the generator computes serials with plain integer comparison (breaking at wrap), that the notify hook races the atomic rename of the zone file, and that negative answers are cached under a policy that ignores SOA MINIMUM changes.
- Synthesize: no daemon or script owns coherence; the invariant spans generator, transfer hooks, and cache policy.
- Diagnose: symptoms are "some names stay stale or NXDOMAIN after publishing"; nothing names serials, hooks, or negative caching.
- Navigate coupling: fixing serial arithmetic alone makes transfers fire more often and widens the rename race; fixing the hook alone leaves wrapped serials refusing transfer; fixing cache TTLs alone masks staleness until the next wrap.
- Reason beyond training: RFC 1982 wraparound plus notify/rename ordering plus negative-cache semantics is a systems-composition problem, not a textbook zone-file exercise.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. Serial comparison in the zone generator is plain-integer, so post-wrap serials are treated as older — secondaries silently refuse the new zone.
2. The publish path renames the zone file after the notify hook fires, so a fast transfer reads the old file deterministically (hook ordering, not timing luck).
3. The resolver caches NXDOMAIN using a stale SOA MINIMUM captured at startup, pinning deleted-name behavior past regeneration.
4. Fix locations: generator serial module, publish/notify hook script ordering, resolver negative-cache handling — three distinct roots.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): hidden environment/process state (primary); log interpretation and evidence triage; infrastructure diagnosis.
- Causal chain (4-8 dependent stages): (1) reproduce stale answers for the failing zone; (2) query authoritative vs cache paths to localize which layer is stale; (3) inspect transfer logs to find refused transfers; (4) discover serial wrap in zone history; (5) fix serial arithmetic, observe the rename/notify ordering failure now dominates; (6) fix publish ordering, observe deleted names still resolve NXDOMAIN-stale; (7) repair negative-cache policy and verify the full matrix.
- Heterogeneous evidence surfaces (>= 3): daemon logs, zone files + serial history artifacts, hook scripts, resolver cache dumps/runtime queries, configuration.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "cache TTLs are just too long" — falsified by querying the authoritative path directly and seeing stale data there too; H2 "the generator never wrote the new zone" — falsified by inspecting the on-disk zone file post-publish.
- Failing scenario and healthy control: one zone crosses the serial wrap and fails; a sibling zone below the wrap keeps working and must remain correct after the fix (blocks broad "flush everything" patches).
- Meaningful-action estimate (20-100, no busywork): ~40-70 (queries per layer, log triage, hook tracing, three coordinated edits, matrix verification).
- Determinism strategy: no wall-clock races — hook ordering is a deterministic sequencing bug; TTL behavior is driven by a virtual clock/epoch counter in the harness, offline and single-container.
- Domain and why this is not trivia: tests DNS operations engineering (serial discipline, publish atomicity, cache coherence), not recall of one RFC sentence; the RFC 1982 rule is discoverable from observed refusal behavior.

## Symptoms-only instruction sketch

"After the nightly zone publish, some services still resolve to hosts that were removed weeks ago, and some newly added names return NXDOMAIN for hours. Other zones publish fine. Make publishing coherent: after a publish completes, every query path must serve the new data on schedule, and the healthy zones must keep working."

## Decision notes

Captured 2026-07-19 during portfolio expansion. Nearest internal neighbor: none (first DNS-domain idea). Anti-trivialization watchpoints for Step 2a: the fix must not collapse into "restart the resolver" (the wrap refusal persists across restarts) and instruction nouns (serial, notify, cache) must not name fix-path symbols.
