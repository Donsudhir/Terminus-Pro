# Idea: Save Lineage Exhume

- Idea ID: `IDEA-0031`
- Slug: `save-lineage-exhume`
- Category: games
- Languages: TBD (candidate: c++ or rust)
- Created: 2026-07-19T11:08:20Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

After an engine upgrade, players' old save files crash the loader or load with corrupted state; a migration path must load every historical save generation faithfully, and the meaning of some old fields is recoverable only from artifacts and replayed game logic.

## Structural archetype

Legacy-format migration/recovery: the input is a graveyard of undocumented historical format generations, and the deliverable is a loader/migrator whose correctness is judged by *semantic* outcomes — migrated saves must behave identically under scripted gameplay replay, not merely parse. Reconstructing lost format semantics from artifacts is a shape no other portfolio idea uses (distinct from resolver-closure-drift's commit archaeology: here there is no history to read, only binary strata to excavate).

## Novelty fingerprint

- Domain/system: a game engine's save system — binary save files spanning four format generations, a loader with partial version handling, checksum validation, a string-intern table, quest/inventory state, and a scripted headless gameplay harness.
- Failure mechanism: generation-2 saves wrote one section in origin-platform endianness while the loader assumes little-endian; generation-3 appended the intern table after a checksum-covered region so strict validation rejects valid saves; generation-4 silently changed quest-bitfield semantics without bumping the version number.
- Distributed fix topology: section decoding (endianness detection), checksum-region handling, and versionless semantic detection for the bitfield live in different loader stages; each alone still fails a distinct save cohort.
- Verifier/invariant surface: every archive save loads and passes scripted-gameplay semantic checks (inventory usable, quests progress correctly); migrated saves round-trip stably; deliberately corrupted saves are still rejected.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): lockstep-replay-fray (IDEA-0020) is the other games idea but grades replay determinism of a live simulation; this grades semantic fidelity of data migration across dead formats. procgen-seed-shear was rejected as a lockstep duplicate; this replacement was chosen specifically for archetype distance.
- Structural differentiator: the central skill is binary-format archaeology plus semantic inference (what did this bitfield *mean* in v4-era gameplay?), verified behaviorally through replayed game logic.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must detect the endianness stratum (only some g2 saves, by origin platform), find why strict checksums reject valid g3 saves, and infer the g4 bitfield re-versioning from gameplay-behavior evidence — three buried facts with no documentation.
- Synthesize: correct migration composes format detection, integrity semantics, and gameplay meaning; the loader, the checksum module, and the quest system must be understood together.
- Diagnose: symptoms are "old saves crash or load weird"; crash saves, reject saves, and silently-wrong saves have three different causes the solver must separate.
- Navigate coupling: relaxing checksum validation to admit g3 saves must not admit the corrupted-save controls; endianness auto-detection must not misfire on g4 saves whose bytes coincidentally pattern-match; the bitfield reinterpretation changes quest state that the other fixes' test saves also exercise.
- Reason beyond training: there is no spec to implement — the ground truth lives in binary strata and replayed behavior, the inverse of LLM-friendly spec-transcription work.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. Generation-2 saves from one platform family store a section big-endian; detectable via field-plausibility analysis across the save archive, not via any header flag.
2. Generation-3 grew the file after the checksum-covered region; the checksum is valid for the region it was defined over — provable by recomputing region-wise, explaining why "corrupt" saves play fine on old builds (bundled player reports say so).
3. Generation-4 changed quest-bitfield meaning without a version bump; recoverable by replaying bundled era-tagged sessions and observing which interpretation yields consistent quest progression.
4. Fix locations: section decoder, checksum-region validator, quest-state interpreter (plus migration writer) — distinct loader stages.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): long-horizon causal debugging (primary); hidden state in binary artifacts; ambiguous production symptoms.
- Causal chain (4-8 dependent stages): (1) triage the save archive into crash / rejected / silently-wrong cohorts; (2) hex-level analysis of a crash save reveals implausible field values, leading to the endianness stratum; (3) fix decoding, rejected cohort remains, recompute checksums region-wise and discover the g3 growth; (4) scope validation to the covered region while keeping corrupt controls rejected; (5) silently-wrong cohort remains, replay era-tagged sessions to infer the bitfield re-versioning; (6) implement versionless semantic detection; (7) migrate the archive, verify scripted-gameplay semantics and round-trip stability.
- Heterogeneous evidence surfaces (>= 3): binary save files, loader/crash logs, bundled player-report documents, scripted gameplay replay outputs, code.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "saves are bit-rotted" — falsified by region-wise checksum validity and old-build compatibility notes; H2 "one loader refactor broke everything" — falsified by cohort analysis showing three independent failure signatures spanning different generations.
- Failing scenario and healthy control: g2-platform, g3, and g4-era saves fail differently; generation-1 and current-generation saves load correctly and must remain byte-stable through migration (blocks rewrite-the-loader approaches that regress the live format), and corrupted-save controls must stay rejected (blocks validation gutting).
- Meaningful-action estimate (20-100, no busywork): ~50-85 (cohort triage, hex forensics, region checksum analysis, behavioral inference replays, three fixes plus migrator, full-archive verification).
- Determinism strategy: fixed save archive, headless scripted replays with seeded simulation, no wall clock; single container, offline.
- Domain and why this is not trivia: binary-format archaeology with behaviorally-verified semantics is real (and expensive) engineering — games, medical devices, and file-format rescue all pay for it; no single obscure fact unlocks it.

## Symptoms-only instruction sketch

"Since the engine upgrade, veteran players are furious: some old saves crash on load, some are refused as corrupt even though they worked last month, and some load but items vanish or quests reset. The archive has saves from every era plus a few known-bad ones. Make every legitimate save load and play correctly under the archived test sessions; the known-bad saves must still be refused."

## Decision notes

Captured 2026-07-19 as the archetype-distinct replacement for the rejected procgen-seed-shear. Step 2a watchpoints: semantic checks must run through scripted gameplay (behavioral, CM-006), the endianness stratum must be detectable from content plausibility rather than a hidden flag (no hidden-instance guessing — the cohort structure is discoverable), and corrupt controls keep validation honest.
