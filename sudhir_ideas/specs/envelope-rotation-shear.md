### Decision
GO — Attempt 1 replacement. One stable authority-lineage invariant now connects maintenance binding, scoped context, strict opening, and predecessor validation; twelve neutral tests distribute at 4/12 per typed boundary.

### Revision 3 amendment — 2026-07-19
The agent-facing implementation language is Go only. Python is verifier infrastructure and is not task-language metadata. The public contract now states both sides of the generated-namespace invariant: valid live records in newly introduced service namespaces remain directly readable without recovery, while intact cross-namespace substitutions still fail without recovery. This is an observable clarification already exercised by the verifier; it does not require one internal compatibility algorithm, add an oracle location, or change the selected topology.

### Revision 4 amendment — 2026-07-21
Platform instruction-sufficiency analysis showed agents guessing between public-service namespace binding and an alternate rewritten label for generated live frames. The public contract now states, still without naming internal helpers: (1) generated live records sealed under the same public `<service>` name as their namespace binding must open via `get` without recovery; (2) maintenance must keep that public-service binding consistent and must not rewrite active matching-service records; (3) satisfying generated reads must not make foreign substituted records readable, and rejecting substitutions must not make matching-service generated records unreadable. No oracle location or topology change.

### Metadata
- version: 2
- Task name: envelope-rotation-shear
- Title: Envelope Rotation Recovery
- Category: security
- Languages: ["go"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["envelope-encryption", "key-rotation", "forensics", "data-recovery", "go"]
- Milestones: 0

## Authoring Brief

### Public contract
Write a concise two-paragraph `instruction.md` that reports a post-maintenance incident: stable authentication failures affect the same protected records and some service namespaces return namespace values they do not own. It must direct the solver to repair the existing system, recover every affected secret through `/app/bin/vaultctl recover`, preserve healthy records byte-for-byte, read values through `/app/bin/vaultctl get <service> <secret>`, and neither replace the bundled corpus nor bypass authentication. It must state that valid live records for newly introduced service namespaces remain readable without invoking recovery—including records sealed under that same public `<service>` name as their namespace binding—while intact records substituted across service namespaces fail without invoking recovery. It must also state that maintenance keeps that public-service namespace binding consistent, does not rewrite active matching-service records, and that generated-read success must not imply opening foreign substitutions (and substitution rejection must not break matching-service generated reads).

The instruction must state that recovery writes `/app/output/recovery.json` as a JSON object with one `recovered` array whose array items use string `service` and `secret` fields; the array lists every affected service/secret identity once and no healthy identity. It must also require `/app/bin/vaultctl maintain` to be safe and byte-stable on a second run, `/app/bin/vaultctl audit` to preserve namespace isolation and reject tampered records and substituted records, and the same behavior across a clean reset, additional generated namespaces, and later maintenance cycles. Keep this as observable contract prose: do not name an algorithm, internal authority representation, historical location, cause, patch site, threshold, or repair order.

### Failure topology
The environment is an existing envelope-encrypted record service whose primitive encryption and key-wrapping wrappers are healthy. Every protected transition is supposed to carry one stable authority identity from the public namespace and record identity through frame binding, scoped key context, authenticated opening, and historical predecessor validation. The incident exists because those typed consumers no longer preserve one representation of that identity.

This is one coupled lineage failure, not independent bugs. A future-write repair cannot recover damaged state; a context-only repair leaves stored bindings inconsistent; a permissive opener accepts cross-authority substitutions; and a predecessor search is unsafe until it validates the same complete identity used by writes and reads. Recovery and future maintenance therefore require four coordinated boundaries.

### Investigation architecture
Use four reinforcing weakness areas: security reasoning, hidden terminal/filesystem state, long-horizon causal diagnosis, and multi-component reasoning. The intended seven-stage progression is: characterize the shared authority boundary; correlate logs and protected headers; falsify key loss and random corruption; trace the identity through typed consumers; discover and validate one authoritative predecessor per affected record; repair all four boundaries; then run the complete recovery, maintenance, read, and audit workflow. Evidence spans code, logs, filesystem state, runtime observations, and configuration. The deterministic offline investigation is estimated at 52 meaningful terminal actions; that estimate is authoring evidence, never a scored process requirement.

### Environment shape
- `cmd/` provides the documented `vaultctl` workflow and a source-visible diagnostic binary whose output reports neutral observations rather than causes.
- `conductor/` owns maintenance planning, protected-frame creation, and commit flow.
- `tenant/` owns namespace input handling and scoped operation context.
- `aperture/` owns authenticated opening and rejection behavior.
- `ledger/` owns compaction indexes, protected segments, and ordinary historical operations.
- `model/`, `keyring/`, and `crypto/` provide typed identities, frame encoding, deterministic key generations, and healthy standard-library primitive wrappers.
- `config/`, `docs/`, `fixtures/live/`, `fixtures/segments/`, and `fixtures/logs/` provide realistic policy, operator context, protected state, ordinary segment data, and incident traces without plaintext answers.
- `scripts/` resets deterministic state and invokes ordinary public workflows.

### Required artifacts
- A standard non-milestone task with `instruction.md`, `task.toml`, `output_contract.toml`, `construction_manifest.json`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`.
- `output_contract.toml` declares `/app/output/recovery.json` as the sole user-visible output, JSON format, with instruction checks for `recovered`, `service`, and `secret`; `/app/bin/inspect` is internal diagnostic infrastructure.
- A digest-pinned, single-container, offline Go environment with `.dockerignore`, no compose file, no UI, and no runtime downloads.
- At least 20 substantive environment files; the exhaustive first-draft list appears under Initial Draft Commitments.
- Two compiled binaries: `/app/bin/vaultctl` for the complete public workflow and `/app/bin/inspect` for deterministic neutral observations used to test hypotheses. No hidden flag or environment override is required by scored tests.
- Deterministic protected live state, segment data, logs, keyring material, and policy fixtures. No plaintext backup, expected-value table, corrected record, golden recovery output, or answer-shaped fixture may be solver-visible.
- Twelve opaque scored tests plus neutral test-owned case generation for additional namespaces and maintenance cycles.
- An oracle whose real semantic delta is 130–190 non-boilerplate lines across only the four committed functions. Every added branch must perform required encoding, validation, rejection, or predecessor-selection work; no padding or cosmetic rewrite counts.

### Test plan
1. `test_e01` starts from a healthy control, runs maintenance, and verifies all public reads and protected bytes remain correct; multiple valid implementations: yes; chain-dependent: no.
2. `test_e02` creates a neutral set of generated service identities and verifies their values remain isolated; multiple valid implementations: yes; chain-dependent: no.
3. `test_e03` exercises valid current and historical authority cases without recovery and requires strict matching reads; multiple valid implementations: yes; chain-dependent: no.
4. `test_e04` creates an additional damaged case through neutral fixture setup, runs public recovery, and verifies its original value through the public read path; multiple valid implementations: yes; chain-dependent: no.
5. `test_e05` hashes complete healthy state after first and second maintenance runs and requires exact byte equality; multiple valid implementations: yes; chain-dependent: no.
6. `test_e06` exercises a broad neutral matrix of generated service labels and requires general isolation without exposing the internal trigger in names, docstrings, or setup APIs; multiple valid implementations: yes; chain-dependent: no.
7. `test_e07` modifies authenticated bytes and substitutes intact records across public authority cases, requiring rejection; multiple valid implementations: yes; chain-dependent: no.
8. `test_e08` verifies that `recovery.json` contains each affected `service`/`secret` identity once, contains no healthy identity, and accompanies unchanged healthy-record hashes; multiple valid implementations: yes; chain-dependent: no.
9. `test_e09` performs an independent reset, then `recover → maintain → maintain → get/audit`; it verifies restored values, exact second-run state, healthy preservation, isolation, and rejection; multiple valid implementations: yes; chain-dependent: no.
10. `test_e10` recovers multiple neutral generated service identities and verifies each receives its own original value; multiple valid implementations: yes; chain-dependent: no.
11. `test_e11` is a strict non-recovery authority test: valid current and historical records open only for their matching public identity and intact substitutions reject; multiple valid implementations: yes; chain-dependent: no.
12. `test_e12` creates new records under generated service identities, runs maintenance twice, and verifies isolation plus byte stability; multiple valid implementations: yes; chain-dependent: no.

Every test creates or resets its own state. Test names, helper APIs, docstrings, fixture labels, and assertion messages remain mechanism-neutral: they must not contain or describe a prefix boundary, representation loss, historical storage location, predecessor source, or intended patch. Assertions target public plaintext properties, the documented recovery schema, exact healthy and complete-state bytes, identity sets, isolation, and rejection; they do not inspect source text or require the oracle's representation.

### Drafting guardrails
Keep `instruction.md` at symptom and outcome level while documenting all four commands and the minimal recovery schema. Use the committed paths, symbols, signatures, and typed boundaries verbatim; do not introduce another top-level symbol on the oracle frontier. Baseline bodies must be plausible production implementations, not TODOs. No bug/fix/intentionally-wrong comments, answer constants, corrected fixtures, permissive compatibility reads, scenario-only branches, CLI bypasses, mechanism-bearing test helpers, or diagnostic output that names a cause or patch site. Protected segment data must serve ordinary compaction and audit behavior before the incident.

### Triviality Ledger
- **Accept multiple authority representations:** blocked by `test_e07`, `test_e09`, and `test_e11`, which require strict rejection of intact cross-authority substitutions.
- **Restore a bundled answer file:** blocked because no plaintext or expected recovery artifact exists and `test_e04` plus `test_e10` create additional damaged cases.
- **Copy all historical records into live state:** blocked by exact affected-identity inventory checks, authority validation, and unchanged healthy-record hashes.
- **Re-encrypt everything:** blocked by healthy-byte preservation and exact second-run state equality.
- **Repair only future maintenance writes:** blocked by generated pre-existing recovery cases and the complete workflow in `test_e09`.
- **Repair only reads with fallback:** blocked by strict tamper and substitution tests.
- **Repair only scoped context:** blocked because stored frame binding, strict opening, and predecessor validation must consume the same stable identity.
- **Patch a generation or policy table:** blocked because configuration is internally consistent and archived generations are healthy.
- **Hardcode fixture identities or values:** blocked by neutral generated namespace, record, and maintenance cases with verifier-owned expected values.
- **Read the test setup as a diagnosis:** blocked by mechanism-neutral test names, helper APIs, docstrings, labels, and broad case matrices.
- **Treat security vocabulary as difficulty:** blocked by healthy primitive wrappers; the scored work is authority-lineage forensics, validated recovery, strict opening, and idempotent transition design.

### Per-gate Pitfall Inventory
- **RC1 — oracle simplification:** each rewrite must add substantive validation or coordination; no deletion-only, disabled-check, broad fallback, or revert-to-old-state oracle.
- **RC2 — oracle predictability:** use the committed opaque paths, symbols, and `test_eNN` names; ban correctional or cause-bearing names and comments on solver-visible surfaces.
- **RC3 — verifier shallowness:** assert recovered values, exact inventory identities, healthy hashes, complete-state stability, isolation, and strict rejection rather than file existence, JSON parseability, or exit status alone.
- **RC4 — tamper surface:** expected plaintext and generated identity sets stay verifier-owned; rewriting `/app/output/recovery.json`, reset scripts, or environment fixtures cannot alter expected outcomes.
- **RC5 — reference artifacts:** live and segment fixtures contain operational protected material only; no plaintext, corrected record, expected digest, or golden output.
- **RC6 — instruction specificity:** document the four public commands and minimal output schema, but no algorithm, internal identity representation, historical location, threshold, source path beyond public executables/outputs, cause, or repair sequence.
- **RC7 — oracle triviality:** require 130–190 genuine semantic-delta lines across four functions; if the real repair is below 80 lines, return to Step 2a rather than pad.
- **CR1/CR3 — manifest and signature compliance:** use every listed function and exact typed signature, with opaque parameter names and no additional oracle symbol.
- **CR2 — flipping-point compliance:** run every single-location reversion and require exactly the declared subset to flip; A, B, C, and D each control 4/12.
- **CR4/CR5/CR6 — surface opacity:** no scenario literals, shadow-pair functions, or intent comments on the oracle frontier.
- **CR7 — grep resistance:** reject any instruction noun or compound substring in selected paths, symbols, parameters, or test names.
- **CR8 — orchestration opacity:** no visible file may reference more than two committed frontier symbols.
- **CR9 — contract traceability:** every asserted output field, CLI, path, and public status has a home in the instruction or a pre-fix solver-visible interface.
- **GX1/GX3 — genuine edit distance:** correctional comments and cosmetic rewrites are forbidden; all counted oracle lines implement required behavior.
- **GX4/GX5/GX7/GX8 — no padding or orphan contracts:** no no-op frontier writes, test-only domain vocabulary, orphan opaque literals, or test-side domain primitive absent from environment code.
- **GX6 — cause disclosure:** public prose reports symptoms and outcomes without a causal narrative.
- **GX9 — contract saturation:** instruction prose states aggregate properties and the minimal schema, not scenario/key/value answer triples.
- **GX10 — polarity clarity:** state matching acceptance and adversarial rejection in separate unambiguous clauses.
- **Static checks:** use an approved digest-pinned base, pinned build dependencies, `allow_internet = false`, exact output contract, `.dockerignore`, LF scripts, at least 20 substantive environment files, and the CM-007-safe pytest invocation from `/tests` with `PYTHONSAFEPATH=1` and `--confcutdir=/tests`.

### Initial Draft Commitments
- `instruction.md`
- `task.toml`
- `output_contract.toml`
- `construction_manifest.json`
- `environment/Dockerfile`
- `environment/.dockerignore`
- `environment/go.mod`
- `environment/Makefile`
- `environment/cmd/vaultctl/main.go`
- `environment/cmd/inspect/main.go`
- `environment/conductor/arc.go`
- `environment/conductor/commit.go`
- `environment/conductor/plan.go`
- `environment/conductor/dial.go`
- `environment/tenant/spine.go`
- `environment/tenant/table.go`
- `environment/tenant/cache.go`
- `environment/tenant/relay.go`
- `environment/aperture/sill.go`
- `environment/aperture/open.go`
- `environment/aperture/check.go`
- `environment/aperture/panel.go`
- `environment/ledger/reel.go`
- `environment/ledger/index.go`
- `environment/ledger/compact.go`
- `environment/ledger/journal.go`
- `environment/ledger/spool.go`
- `environment/model/item.go`
- `environment/model/codec.go`
- `environment/model/types.go`
- `environment/keyring/ring.go`
- `environment/keyring/catalog.go`
- `environment/keyring/material.go`
- `environment/crypto/box.go`
- `environment/crypto/wrap.go`
- `environment/crypto/primitives.go`
- `environment/crypto/scope.go`
- `environment/config/policy.toml`
- `environment/config/ring.toml`
- `environment/docs/operator-guide.md`
- `environment/docs/storage-format.md`
- `environment/docs/operations.md`
- `environment/fixtures/live/catalog.json`
- `environment/fixtures/live/slice-01.bin`
- `environment/fixtures/live/slice-02.bin`
- `environment/fixtures/live/slice-03.bin`
- `environment/fixtures/segments/chunk-01.bin`
- `environment/fixtures/segments/chunk-02.bin`
- `environment/fixtures/segments/chunk-03.bin`
- `environment/fixtures/logs/operations.ndjson`
- `environment/scripts/reset-fixture.sh`
- `environment/scripts/exercise-store.sh`
- `environment/scripts/observe-store.sh`
- `solution/solve.sh`
- `tests/test.sh`
- `tests/case_factory.py`
- `tests/test_outputs.py`

This list is exhaustive. Every listed file must be substantive and created in the first Step 2b draft. Any addition, deletion, rename, or relocation requires a spec amendment before construction continues.

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```yaml
- path: conductor/arc.go
  symbol: trace_q
  kind: function
  signature: func trace_q(a model.ItemID, b model.AxisID, c keyring.Epoch, d model.Payload) (model.Frame, error)
  purpose: Builds the protected frame metadata for one transition.

- path: tenant/spine.go
  symbol: settle_r
  kind: function
  signature: func settle_r(a model.AxisID, b keyring.Epoch) (crypto.Scope, error)
  purpose: Builds scoped bytes for one key operation.

- path: aperture/sill.go
  symbol: route_s
  kind: function
  signature: func route_s(a model.Frame, b crypto.Scope, c *keyring.Ring) (model.Payload, error)
  purpose: Selects one candidate and performs an authenticated open.

- path: ledger/reel.go
  symbol: replay_t
  kind: function
  signature: func replay_t(a *Journal, b model.ItemID, c model.AxisID, d keyring.Epoch) (*model.Frame, error)
  purpose: Locates and validates one prior protected frame.
```

The signatures enforce distinct boundaries. `trace_q` alone returns a new `model.Frame`; `settle_r` alone returns `crypto.Scope`; `route_s` alone receives the keyring required for an authenticated open; and `replay_t` alone receives `Journal` plus stable item and axis identifiers. The oracle may call existing healthy APIs and rebuild commands, but it may alter no additional code symbol. The expected real semantic delta is 130–190 non-boilerplate lines.

#### flipping_point_contract

```yaml
locations:
  - id: A
    path: conductor/arc.go
    controls_tests: [test_e01, test_e05, test_e09, test_e12]
  - id: B
    path: tenant/spine.go
    controls_tests: [test_e02, test_e06, test_e10, test_e12]
  - id: C
    path: aperture/sill.go
    controls_tests: [test_e03, test_e07, test_e09, test_e11]
  - id: D
    path: ledger/reel.go
    controls_tests: [test_e04, test_e08, test_e09, test_e10]
no_single_location_flips_majority: true
concentration_cap: 0.34
```

The union is exactly twelve tests. A, B, C, and D each control 4/12 = `0.3333333333333333`, below `0.34`. `test_e09` deliberately couples A, C, and D across the full public workflow; `test_e10` couples B and D; `test_e12` couples A and B. Step 2b must run every single-location reversion ablation, and any undeclared flip or missing declared flip is a construction failure.

#### decoy_manifest

```yaml
- path: conductor/dial.go
  kind: helper
  rhymes_with: trace_q
  non_fix_purpose: Produces dry-run timing and item-count telemetry for operator summaries.

- path: tenant/relay.go
  kind: helper
  rhymes_with: settle_r
  non_fix_purpose: Normalizes display labels for diagnostics without participating in protected operations.

- path: aperture/panel.go
  kind: helper
  rhymes_with: route_s
  non_fix_purpose: Routes health observations into human-readable status rows.

- path: ledger/spool.go
  kind: helper
  rhymes_with: replay_t
  non_fix_purpose: Replays compaction counters into metrics without reading protected frame bodies.
```

Every decoy must compile, execute in ordinary diagnostics, and remain untouched by `solution/solve.sh`.

#### code_forbidden_tokens

```yaml
code_forbidden_tokens: [maintenance, window, "maintenance window", "last maintenance window", services, app, secrets, records, "same records", authentication, service, namespaces, "service namespaces", namespace, "namespace values", values, system, "existing system", secret, "affected secret", incident, "pre-incident value", "correct pre-incident value", value, bin, vaultctl, recover, command, output, recovery, recovery.json, JSON, object, "JSON object", recovered, array, "recovered array", items, "array items", form, string, "service/secret identity", "affected service/secret identity", identity, "healthy identity", "healthy records", byte, "byte-for-byte", get, "bundled corpus", corpus, maintain, run, "second run", state, "on-disk state", "complete on-disk state", audit, "recovered values", "tampered records", "substituted records", behavior, "same behavior", reset, "corpus reset", "clean corpus reset", "generated namespaces", "additional generated namespaces", cycles, "maintenance cycles", "later maintenance cycles"]
```

This list is the complete noun and domain-meaningful compound extraction from the reviewer-only exact instruction draft. It applies to code symbols, parameter names, selected paths, and top-level constants on the oracle frontier; it does not restrict clear public instruction vocabulary.
