# Idea: Unit Order Eclipse

- Idea ID: `IDEA-0030`
- Slug: `unit-order-eclipse`
- Category: system-administration
- Languages: TBD (candidate: shell, python, c)
- Created: 2026-07-19T10:58:41Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

After enabling one new service, unrelated services are sometimes missing after boot; the init graph contains a silently-dropped dependency edge, a stale adopted socket, and an instance-name collision that only certain enablement combinations expose.

## Structural archetype

Boot-graph diagnosis: the system-under-repair is a dependency *graph resolution process* (an init/service manager simulation), and failures are emergent graph properties — cycles broken silently, state adopted across generations, name collisions — surfaced only under specific enablement matrices. The verifier grades boot convergence across the matrix. No other portfolio idea grades emergent graph-resolution behavior.

## Novelty fingerprint

- Domain/system: a single-container init estate — unit files with ordering/requirement edges, a generator script that synthesizes environment files and drop-ins, socket-activation units, template units with instance escaping, and a deterministic boot simulator with full transaction logs.
- Failure mechanism: a generator-written file is consumed by a unit ordered *before* the generator effectively runs, creating a cycle the manager resolves by silently dropping an edge (which edge depends on the enablement set); a socket unit adopts a stale socket from a service that failed post-start, so the successor never binds properly; two template instances escape to the same internal name and shadow each other.
- Distributed fix topology: generator scheduling/placement, socket lifecycle handling, and instance-escaping (or unit naming) must all change; each alone still fails a different enablement combination.
- Verifier/invariant surface: for every enablement matrix entry, boot converges to the full expected unit set with correct service behavior (probed via each service's health command), and the previously-healthy profile boots unchanged.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): zone-serial-lag-weave and rotated-tail-ledger share the sysadmin category but grade answer coherence and delivery accounting respectively; nothing in the portfolio grades init-graph resolution. No systemd/boot idea found in local scan.
- Structural differentiator: the causal chain runs through *how the manager resolves an inconsistent graph*, so the solver must reason about transaction logs and ordering-cycle policy, not just unit-file contents — a grep of unit files does not reveal which edge got dropped for a given enablement set.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must find the generator-induced cycle (visible only in transaction logs as a dropped edge that moves between boots), the stale-socket adoption, and the escaping collision — three graph-level facts no single file states.
- Synthesize: the boot outcome is a function of the whole graph plus generator output plus prior-boot state; understanding one missing service requires the manager's resolution semantics, not one unit file.
- Diagnose: symptoms are "sometimes service X is just absent after boot, since we enabled Y"; which service is absent varies by enablement combination, so pattern-matching one repro misleads.
- Navigate coupling: reordering the generator naively creates a new cycle through the socket unit; fixing the socket lifecycle exposes the instance collision (both instances now try to bind); the fixes must respect the graph globally, and the healthy profile pins what must not move.
- Reason beyond training: generic systemd knowledge says cycles are reported loudly; this manager's silent-drop policy (realistic — systemd does delete jobs to break cycles) must be discovered from its logs, and the interaction with generator timing is genuinely non-textbook.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. The boot transaction log shows the manager silently dropping a different ordering edge per enablement set — the graph has a cycle through a generator-produced file's consumer, provable by correlating dropped-edge lines with generator output timing.
2. A socket unit adopts the previous generation's file descriptor when its service failed after start; the successor "listens" on a dead socket — provable from socket-state dumps across simulated boot generations.
3. Two template instance names escape to one internal identity, so enabling both shadows one — provable by enumerating the manager's internal unit table.
4. Fix locations: generator scheduling/output placement, socket-unit lifecycle handling, template naming/escaping — three distinct mechanisms.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): hidden environment/process state (primary); infrastructure diagnosis; log interpretation and evidence triage.
- Causal chain (4-8 dependent stages): (1) reproduce a missing-service boot from the matrix; (2) read transaction logs and find the silently-dropped edge; (3) trace the cycle to the generator-consumed file and fix scheduling; (4) matrix still fails elsewhere — socket-state dumps reveal stale adoption; (5) fix socket lifecycle; (6) two instances now conflict — discover the escaping collision in the unit table; (7) repair naming and converge the full matrix plus the healthy profile.
- Heterogeneous evidence surfaces (>= 3): boot transaction logs, unit files and drop-ins, generator script and its outputs, socket/process state dumps, the manager's internal unit-table listing.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "the new service's unit file is just wrong" — falsified by disabling it and reproducing absence with a different enablement pair; H2 "services crash after starting" — falsified by transaction logs showing the jobs were never scheduled.
- Failing scenario and healthy control: specific enablement combinations lose services deterministically; the default profile boots completely and must remain identical in unit set and ordering (blocks mass-reordering hacks — the healthy profile's transaction log is part of the graded surface via behavior probes).
- Meaningful-action estimate (20-100, no busywork): ~40-70 (matrix repros, transaction-log analysis, three graph-level fixes, full-matrix convergence).
- Determinism strategy: the boot simulator schedules deterministically (no real init, no timers); "boot generations" are explicit simulator steps; single container, offline.
- Domain and why this is not trivia: tests dependency-graph resolution reasoning and init-system state lifecycle — daily infrastructure engineering — not memorization of one directive.

## Symptoms-only instruction sketch

"Since we rolled out the new agent service, machines sometimes come up missing services — not always the same ones, and never on the standard profile. Ops has captured the enablement combinations that misbehave. Make every captured profile boot to its complete, working service set, without changing how the standard profile boots."

## Decision notes

Captured 2026-07-19; fingerprinted same day. Step 2a watchpoints: the simulator must be bespoke enough that memorized systemd behavior doesn't shortcut discovery (its cycle policy is in its logs, not in man pages), while remaining realistic; healthy-profile invariance is behavioral, not a log-text lock (CM-006/WW-002).
