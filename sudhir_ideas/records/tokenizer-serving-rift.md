# Idea: Train Serve Token Rift

- Idea ID: `IDEA-0016`
- Slug: `tokenizer-serving-rift`
- Category: machine-learning
- Languages: TBD (candidate: python, rust)
- Created: 2026-07-19T10:58:40Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A served text classifier collapses on specific input classes although offline evaluation is clean; the model card's preprocessing claims are wrong, and only the shipped artifacts can prove what training actually did.

## Structural archetype

Misleading-documentation investigation: authoritative-looking documentation makes historically plausible but false claims; the solver must distrust prose, run deterministic experiments on artifacts (vocab, merges, saved tensors, corpus samples), and align the serving path with reconstructed truth. No other portfolio idea makes documentation-falsification the primary axis.

## Novelty fingerprint

- Domain/system: an ML inference stack — trained model weights, tokenizer artifacts (vocab, merges, manifest), a model card, saved training-batch tensors, and a serving text pipeline.
- Failure mechanism: the model card claims NFC normalization but the training corpus was NFKC-case-folded by a preprocessing flag added after the card was written; serving inserts special tokens before truncation while training truncated first; the shipped merges file predates the shipped vocab (manifest hash mismatch).
- Distributed fix topology: serving normalizer, sequence-assembly (truncation/special-token order), and artifact manifest/loader must all change; each alone leaves a measurable failure class.
- Verifier/invariant surface: served predictions must match reference outputs on probe suites (mixed-script, long-input, and ligature/width classes), and reconstructed token IDs must equal the saved training tensors for bundled samples.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): no tokenizer/serving idea in the local portfolio; nearest internal shape is feature-skew-horizon (IDEA-0024), which is temporal-leakage in feature stores — different failure ontology (future-information flow vs documentation falsity) and different verifier surface.
- Structural differentiator: truth is recoverable only from binary artifacts and saved tensors, never from any document in the repo — the inverse of spec-implementation tasks.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must establish, against the model card's explicit claims, what normalization the corpus actually received, in what order truncation happened, and that the merges file is stale — all from artifact forensics.
- Synthesize: the correct serving pipeline is the composition of three reconstructed facts; no document or module states it.
- Diagnose: symptoms are per-class accuracy collapse in serving only; nothing points at preprocessing, and the obvious authority (the card) actively misleads.
- Navigate coupling: fixing normalization alone shifts token boundaries and makes the truncation-order bug *worse* on long inputs; the manifest fix changes token IDs, invalidating any hardcoded workaround from earlier steps.
- Reason beyond training: the artifacts are bespoke; a stock "use the library tokenizer" answer cannot reproduce this model's actual training-time behavior.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. Vocabulary statistics (absence of precomposed forms, folded-case frequencies) prove NFKC+casefold, contradicting the card's NFC claim — historically explainable by a preprocessing flag added after the card was written (visible in bundled changelog artifacts).
2. Saved training tensors show truncation happened before special-token insertion; serving does the reverse, so long inputs lose the final classification token.
3. The manifest records a merges hash that does not match the shipped merges file; the matching file exists in the artifact archive under a version directory.
4. Fix locations: serving normalizer, sequence assembler, artifact manifest/loader — distinct roots.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): misleading or conflicting documentation (primary); log/artifact evidence triage; recovery from disproven hypotheses.
- Causal chain (4-8 dependent stages): (1) reproduce the per-class collapse with the bundled probe suite; (2) verify weights integrity to eliminate the "corrupt model" hypothesis; (3) diff served token IDs against saved training tensors — the card-faithful pipeline does not reproduce them; (4) prove NFKC+casefold from vocab statistics; (5) fix normalization, find long-input class still failing, prove truncation order from tensor lengths; (6) fix assembly, find residual rare-token failures, prove merges staleness from the manifest; (7) align all three and sweep probes.
- Heterogeneous evidence surfaces (>= 3): model card and changelog documents, binary tokenizer artifacts, saved training tensors, serving logs, code.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "weights corrupted in export" — falsified by checksum plus clean offline eval through the training-side pipeline; H2 "serving runtime numeric drift" — falsified by bit-identical logits when token IDs are forced equal.
- Failing scenario and healthy control: mixed-script, ligature, and long inputs fail; plain ASCII short inputs pass everywhere and must keep passing (blocks "re-tokenize everything differently" hacks).
- Meaningful-action estimate (20-100, no busywork): ~40-65 (probe runs, tensor diffing, vocab statistics, three aligned fixes, sweep).
- Determinism strategy: frozen weights, fixtures, and probe suites; no sampling — argmax classification only; single container, offline.
- Domain and why this is not trivia: tests empirical ML-systems forensics — establishing ground truth about a training pipeline from its artifacts — not recall of Unicode trivia; every needed fact is derivable in-container.

## Symptoms-only instruction sketch

"Offline evaluation of the bundled classifier is clean, but the serving endpoint misclassifies chunks of real traffic — reports cluster around non-Latin text and very long documents. The team insists preprocessing matches the model card. Make served predictions correct for the archived traffic suites without retraining; short plain-text traffic must keep its current behavior."

## Decision notes

Captured 2026-07-19; reshaped to the misleading-documentation archetype in the same-day template review. Step 2a watchpoints: the stale card claims must stay historically explainable (changelog shows the flag landing after the card) per the philosophy doc's fairness rule, and the card must not be the *only* wrong authority nor the tests' target — outcome tests grade served behavior.
