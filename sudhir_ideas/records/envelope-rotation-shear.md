# Idea: Envelope Rotation Shear

- Idea ID: `IDEA-0022`
- Slug: `envelope-rotation-shear`
- Category: security
- Languages: Go
- Created: 2026-07-19T10:58:41Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A key-rotation sweep left part of a secrets store undecryptable; the solver must first forensically recover the lost secrets from store internals, then make rotation safe and idempotent to run again.

## Structural archetype

Recover-then-fix: the task has two ordered deliverables — a forensic recovery of data the buggy mutation damaged (possible only by discovering redundant state the store keeps internally), and a repaired mutation that is provably idempotent on re-run. The recovery half cannot be skipped and cannot be done by the fixed code alone. No other portfolio idea grades forensic data recovery.

## Novelty fingerprint

- Domain/system: an envelope-encryption secrets store — key-encryption-key (KEK) generations, per-secret wrapped data keys, AAD-bound ciphertext records, a rotation sweeper, and a compaction backlog that retains superseded records.
- Failure mechanism: the sweeper re-wrapped data keys under the new KEK but wrote AAD that still names the old key generation for records in one shard-naming scheme; independently, the KDF truncates scope names at a fixed boundary so two long scope names collide into one derived context.
- Distributed fix topology: AAD construction in the sweeper, KDF context derivation, and the decrypt path's generation resolution must be repaired coherently; the recovery additionally requires discovering that pre-rotation wrapped copies survive in the compaction backlog.
- Verifier/invariant surface: every secret decrypts to its original plaintext (recovery correctness); re-running rotation changes nothing (idempotence); colliding-scope fixtures now isolate; tampered and cross-generation forgeries still reject.

## Collision audit

All six required scopes were searched on 2026-07-19: idea registry, active
tasks, archived tasks, 159 submission archives (content-level instruction
scan), upstream Terminal-Bench corpora, and current external research.

- Closest analogue: Terminal-Bench 3 `crash-safe-vault` (PR #1127 / discussion
  #1122), a specified single-module crash-safe vault implementation.
- Structural differentiator: this task starts after a completed damaging
  mutation in an existing multi-module envelope store. It requires forensic
  recovery from retained superseded state, project-specific key-lineage repair,
  strict forgery rejection, and idempotent re-rotation. The analogue grades
  crash linearizability of newly implemented operations.
- Internal neighbours: `offline-trust-chain-skew` grades trust verdicts;
  `sanitizer-parser-rift` grades parser agreement. Neither shares the
  recover-then-fix archetype or envelope-store mechanism.
- Evidence: `sudhir_research/TASK-ERS-001-RESEARCH.md` plus RFC 5116, RFC
  5869, Google Cloud KMS envelope-encryption guidance, and the cited TB3 PR.
- Result: no semantic collision found; uniqueness PASS is recorded in the
  registry. This does not imply Step 2a GO.

## Why it is hard (five hardness axes)

- Discover: the solver must reconstruct the failure boundary (which records, why those), find that AAD binds the stale generation only for one shard-naming scheme, uncover the KDF truncation collision, and — critically — discover the compaction backlog as recovery material.
- Synthesize: decryptability is a function of KEK lineage, AAD content, derived context, and record placement; the failure set is the intersection of two independent bugs, which resists single-cause thinking.
- Diagnose: symptoms are "a subset of secrets fail authentication since the maintenance window"; nothing names AAD, KDF, shards, or the backlog.
- Navigate coupling: "fixing" decrypt to tolerate stale-generation AAD would accept forged cross-generation records (the adversarial controls fail); recovery via the backlog only works before compaction is triggered, and the repaired sweeper must handle both recovered and originally-healthy records identically.
- Reason beyond training: envelope-encryption repair with AAD lineage and derivation-collision analysis over a bespoke store layout is professional applied-crypto engineering, not a pattern-matched recipe — the safe path (recover from redundancy, never weaken verification) must be reasoned, not recalled.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. Failing records share one shard-naming scheme; for those shards the sweeper wrote new wraps but stale-generation AAD — provable by dumping record headers across shards.
2. Two long scope names derive identical KDF contexts because of a truncation boundary — provable with the store's own derivation tool against fixture scopes.
3. Pre-rotation wrapped copies survive in the compaction backlog and are sufficient to recover every damaged secret — discoverable only by inspecting store internals beneath the documented API.
4. Fix locations: sweeper AAD construction, KDF context derivation, decrypt-path generation resolution (plus the one-shot recovery procedure) — three code roots and a forensic artifact.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): security reasoning (primary); hidden environment/filesystem state; long-horizon causal debugging.
- Causal chain (4-8 dependent stages): (1) characterize which secrets fail and extract the shard-scheme pattern; (2) dump headers and attribute failures to stale-generation AAD; (3) falsify "KEK lost" by unwrapping a healthy record under each KEK generation; (4) discover the backlog retains pre-rotation wraps; (5) recover damaged secrets from backlog material; (6) repair sweeper AAD and the KDF truncation (found while explaining why two scopes cross-fail); (7) re-run rotation, prove idempotence and forgery rejection.
- Heterogeneous evidence surfaces (>= 3): binary record headers/store files, sweeper logs, key-generation metadata, the store's CLI tooling output, code.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "the old KEK was destroyed prematurely" — falsified by successfully unwrapping healthy records under every archived generation; H2 "ciphertext corruption on disk" — falsified by intact integrity of the wrapped-key fields and the pattern following shard naming, not storage geometry.
- Failing scenario and healthy control: one shard-naming scheme's records fail plus two colliding scopes; all other shards decrypt fine and must be byte-untouched by recovery and re-rotation (blocks "re-encrypt the world" approaches, which also fail idempotence checks).
- Meaningful-action estimate (20-100, no busywork): ~45-80 (failure-set characterization, header forensics, hypothesis falsification, backlog discovery, recovery, three repairs, idempotent re-run).
- Determinism strategy: all key material, records, and sweeper state are fixtures; no clocks or entropy at solve time (deterministic nonce derivation in the harness); single container, offline.
- Domain and why this is not trivia: tests key-lineage forensics and safe-mutation design; the crypto primitives are standard — the reasoning about lineage, binding, and recovery is the work.

## Symptoms-only instruction sketch

"Since last week's maintenance window, some services can't read their secrets — authentication failures, always the same subset. Two unrelated teams also report reading each other's values. Recover every secret to its correct value, make the maintenance procedure safe to run again (running it twice must change nothing), and don't weaken tamper rejection — the audit fixtures must still be refused."

## Decision notes

Captured 2026-07-19; reshaped to the recover-then-fix archetype in the same-day template review. Step 2a watchpoints: recovery must be impossible via "decrypt leniently" (forgery controls), and the backlog must be genuine store infrastructure with a plausible retention purpose, not a planted treasure chest.
