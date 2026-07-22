# TASK-ERS-001 — envelope-rotation-shear — Super-Uniqueness Dossier

- Idea: `envelope-rotation-shear` (IDEA-0022)
- Category: security
- Archetype: recover-then-fix (forensic data recovery from internal store redundancy, then idempotent repair of the damaging mutation)
- Research date: 2026-07-19
- Verdict: **no semantic collision found** across all six required scopes

## Novelty fingerprint (four parts)

1. **Domain/system:** an envelope-encryption secrets store — KEK generations, per-secret wrapped data keys, AAD-bound records, a rotation sweeper, and a compaction backlog retaining superseded records.
2. **Failure mechanism:** the rotation sweeper re-wrapped data keys under the new KEK but wrote stale-generation AAD for one shard-naming scheme; independently, KDF scope-name truncation collides two long scopes into one derived context. The damaged set is the intersection/union of two independent bugs.
3. **Distributed fix topology:** sweeper AAD construction + KDF context derivation + decrypt-path generation resolution, plus a one-shot forensic recovery sourced from the compaction backlog. No single location clears the matrix; "decrypt leniently" is blocked by forgery controls.
4. **Verifier/invariant surface:** all secrets decrypt to original plaintexts (recovery); rotation re-run is a no-op (idempotence); colliding scopes isolate; tampered/cross-generation forgeries still reject.

## Collision audit — all six scopes

### 1. Idea registry (31 ideas)

Scanned `sudhir_progress/registry.json` / `IDEA_INDEX.md` 2026-07-19. Only other security ideas: `offline-trust-chain-skew` (adversarial verdict matrix over trust decisions — different graded object, no cryptographic store) and `sanitizer-parser-rift` (parser differential). No key-rotation, envelope-encryption, KDF, or recovery idea. **No collision.**

### 2. Active tasks

`sudhir_tasks/active/`: robust-predicate-scale-parity (geometry), sparse-jacobian-color-contract (sparse derivatives), musl-sysroot-splice (toolchain staging). `tasks/`: plus journal-compaction-replay (leaderboard triage over DuckDB replay), mothlight-courier-replay-triage, driftlens-calibrate-api. **No collision.**

### 3. Archived tasks / submission archives (159 zips)

Extracted every `instruction.md` (`/tmp/subm_instr`, 2026-07-19) and content-searched: `encrypt|cipher|aad|nonce|key deriv|kdf|hkdf|master key|unwrap|rewrap|hsm|key rotation|envelope|kms|secret|vault`. Hits: `post-quantum-pki-migration-matrix-repair` and `pqc-rollout-advisor` (PQC migration wire-format/rollout planning — no envelope store, no recovery), `corpus-boundary-guard` (retrieval content scanning), `barrel-cooperage-rotation-ledger` (physical barrel rotation, whiskey mass-balance). None involves envelope encryption, key lineage, AAD binding, or data recovery from a damaged store. **No collision.**

### 4. Upstream corpus (Terminal-Bench public)

TB2.0 public task list (tbench.ai, retrieved 2026-07-19): crypto-adjacent
entries are `feal-differential-cryptanalysis` and
`feal-linear-cryptanalysis` (cipher attacks), plus `db-wal-recovery` /
laude PR #744 "Database recovery with encrypted WAL" (recover one artifact
by identifying a basic XOR cipher). None repairs an existing envelope store,
reconstructs KEK/AAD lineage, or recovers records from superseded store state.

Terminal-Bench 3 PR #1127 / discussion #1122, `crash-safe-vault`, is the
closest public task found. It asks the solver to implement one Python vault
module from an explicit durability/security contract: WAL framing, commit
markers, snapshot replacement, audit-chain reconciliation, capabilities, and
crash injection. Its dominant archetype is blank-canvas crash-safe store
construction. This idea instead presents an existing multi-module store after
a completed damaging mutation; the solver must infer two hidden lineage
defects, recover data from legitimate retained redundancy, preserve strict
authentication, and make the existing sweep idempotent. Mechanism, topology,
investigation, and verifier surface are materially different. **No semantic
collision.**

### 5. Current external research

Searches performed 2026-07-19:

- `"terminal-bench" OR "tbench" task envelope encryption AAD key rotation
  re-wrap recovery benchmark agent 2026`
- `Terminal-Bench task list 2026 secrets store key rotation encryption
  recovery task benchmark`

Results returned general Terminal-Bench documentation, TB2 cryptanalysis/WAL
tasks, and the TB3 `crash-safe-vault` proposal above. No result combined
forensic recovery of a partially rotated envelope store, AAD-generation
lineage, KDF-context collision, retained superseded wraps, and idempotent
re-rotation. **No collision found in current public search.**

### 6. Structural-neighbour check

The nearest *engineering* analogue is a production KMS rotation incident.
That shared domain is not enough to collide: ordinary rotation tasks re-wrap
healthy keys or implement a rotation recipe. Here, rotation has already
damaged records, the documented API cannot recover them, weakening
authentication is explicitly invalid, and the successful path depends on
discovering retained pre-rotation wraps in an unrelated compaction subsystem.

## Closest analogue and structural difference

- **Closest analogue:** TB3 `crash-safe-vault` (PR #1127 / discussion #1122).
- **Structural difference:** `crash-safe-vault` implements a specified,
  single-module durability protocol under injected crashes. This task
  diagnoses and repairs a pre-existing, multi-module envelope-encryption
  system after an already-completed mutation; it requires forensic recovery
  from superseded internal state and preserves strict rejection semantics.
- **Why a rename/language swap cannot explain the difference:** the two tasks
  quantify over different executions and artifacts. One grades crash
  linearizability of newly implemented operations; the other grades recovered
  historical plaintexts, key-lineage isolation, strict forgery rejection, and
  idempotence of a repaired mutation.

## Authoritative technical grounding

### AEAD associated data

Source: RFC 5116, *An Interface and Algorithms for Authenticated Encryption*,
https://www.rfc-editor.org/rfc/rfc5116 (retrieved 2026-07-19).

Associated data is authenticated but not encrypted. Decryption must use the
same associated data used by encryption; mismatched generation/scope metadata
therefore produces deterministic authentication failure. The implication is
that "accept either old or new AAD" is not a safe repair: it weakens the
binding the store relies on.

### HKDF context separation

Source: RFC 5869, *HMAC-based Extract-and-Expand Key Derivation Function*,
https://www.rfc-editor.org/rfc/rfc5869 (retrieved 2026-07-19).

HKDF's `info` field binds derived keys to application context. Truncating
distinct logical scope names into the same context defeats domain separation.
The task need not require remembering RFC vocabulary; the collision is
deterministically discoverable with the bundled derivation probe.

### Envelope-encryption rotation

Source: Google Cloud KMS envelope-encryption guidance,
https://cloud.google.com/kms/docs/envelope-encryption (retrieved 2026-07-19).

Envelope systems encrypt data with data-encryption keys and protect those keys
with a key-encryption key. Rotation commonly re-wraps protected data keys
rather than re-encrypting every payload. This grounds the store topology while
leaving the project-specific generation binding and recovery path to be
discovered.

## Construction feasibility and anti-collapse risks

- The backlog is ordinary compaction input retained for rollback/audit, not a
  planted answer file. It contains wrapped historical records, never plaintext
  or expected-output tables.
- The instruction reports authentication failures, cross-scope reads,
  recovery, re-run stability, and tamper rejection. It does not mention AAD,
  HKDF, truncation, shard naming, or compaction backlog.
- A copied crypto recipe cannot solve the incident. The cryptographic
  primitives already work; project-specific lineage metadata and store state
  are wrong.
- At least three roots remain necessary: sweep/re-wrap, context derivation,
  read/generation resolution. Recovery uses a fourth store-history root.
- Tests must regenerate behavior through the store CLI and verify recovered
  plaintext properties plus rejection/idempotence. They must not grade helper
  names, ciphertext bytes, or a fixed representation.
- Healthy records and forgery controls block "decrypt leniently", "re-encrypt
  everything", "restore one answer file", and "skip rotation" shortcuts.

## Uniqueness verdict

**PASS for the super-uniqueness gate.** Six required scopes were searched.
The nearest analogue is recorded and materially different in domain
mechanism, distributed topology, investigation shape, and verifier invariant.
This verdict permits Step 2a validation only; it is not Step 2a GO and does
not permit construction.