### Decision
GO — Attempt 1 replacement. One stable authority-lineage invariant now connects maintenance binding, scoped context, strict opening, and predecessor validation; twelve neutral tests distribute at 4/12 per typed boundary.

### Revision 3 amendment — 2026-07-19
The agent-facing implementation language is Go only. Python is verifier infrastructure and is not task-language metadata. The public contract now pairs direct reads of valid live records in newly introduced service namespaces with strict rejection of intact cross-namespace substitutions, both without recovery. The verifier accepts any implementation with those outcomes; guarded compatibility and canonicalized single-scope designs remain valid, so no fifth oracle location or internal fallback requirement is introduced.

### Revision 4 amendment — 2026-07-21
Clarify the paired polarity further: generated records sealed under the public service name as their namespace binding remain directly readable; maintenance keeps that binding and skips rewriting active matching-service records; additive fallbacks that open substituted foreign records, and reductive changes that break matching-service generated reads, both violate the contract. Still no required internal algorithm or fifth oracle location.

### Metadata
- Task name: envelope-rotation-shear
- Title: Envelope Rotation Recovery
- Category: security
- Languages: ["go"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["envelope-encryption", "key-rotation", "forensics", "data-recovery", "go"]
- Milestones: 0

### Investigation profile
The primary weakness area is security reasoning, reinforced by hidden terminal/filesystem state, long-horizon debugging, and multi-component reasoning. The task is one authority-lineage incident: maintenance binding, scoped context, strict opening, and predecessor validation are typed consumers of the same stable identity.

1. Reset and compare failing records, healthy neighbors, and generated identities. The failures correlate at one maintenance-era authority boundary, which justifies cross-surface correlation.
2. Correlate operation logs, protected headers, and snapshots. Stored and runtime authority fingerprints disagree, narrowing the hypotheses to key availability or identity representation.
3. Exercise archived generations and compare immutable protected-body digests. Successful controls falsify key loss and random corruption, making identity tracing the next justified step.
4. Trace the stable identity through write, context, and open boundaries. Divergent representations become observable, providing a safe key for historical search.
5. Follow stable item identities through ordinary indexes and validate candidates with the complete authority identity. Each affected record has one authenticated predecessor; ambiguous candidates reject.
6. Repair the four typed consumers and rebuild. Recovered, healthy, and future records now share one lineage model.
7. Reset, recover, maintain twice, read, audit, hash state, and run neutral generated cases. This proves exact recovery inventory, healthy preservation, isolation, idempotence, and strict rejection.

Evidence surfaces are code (`conductor/`, `tenant/`, `aperture/`, `ledger/`, `model/`, `keyring/`), logs (`fixtures/logs/operations.ndjson`), filesystem state (live and protected segment fixtures), runtime state (neutral `/app/bin/inspect` observations), and configuration (`policy.toml`, `ring.toml`). Competing hypotheses include destroyed older key material, random protected-payload corruption, and an unrelated cache leak; each has a deterministic generation, digest, or fresh-process falsifier. The conditional matrix includes affected maintenance records and generated identities plus neighboring healthy records and adversarial substitutions. The estimate is 52 meaningful actions. All source, keys, records, logs, segments, and schedules are fixed and offline; resets avoid clocks, entropy, and filesystem-order dependence.

### Discovery budget
- Discovery: One maintenance placement convention binds a projection of the stable authority identity that disagrees with later opens.
  Planned location: `environment/conductor/arc.go`, `environment/model/codec.go`, operation logs, and neutral header observations.
  Why instruction must not reveal it: naming metadata or identity disagreement would disclose the first repair boundary.
- Discovery: A second typed consumer does not preserve the complete authority identity, allowing distinct public namespace inputs to share one runtime context.
  Planned location: `environment/tenant/spine.go` and neutral runtime context observations.
  Why instruction must not reveal it: naming representation loss or its triggering input shape would reduce isolation diagnosis to an encoding edit.
- Discovery: Archived key generations remain usable.
  Planned location: `environment/keyring/catalog.go`, `environment/config/ring.toml`, and generation observations.
  Why instruction must not reveal it: key destruction is a plausible hypothesis that must be falsified before recovery authority can be chosen.
- Discovery: Ordinary protected segment history contains one valid predecessor for every affected live record.
  Planned location: `environment/ledger/{index.go,compact.go,reel.go}` and protected segment fixtures.
  Why instruction must not reveal it: the location and purpose of the predecessor substrate are the forensic discovery, not part of the public contract.
- Discovery: Strict opening and predecessor validation must each resolve one complete authority identity; alternate projections admit intact substitutions.
  Planned location: `environment/aperture/sill.go` and neutral rejection observations.
  Why instruction must not reveal it: candidate ambiguity would expose both the read repair and the flaw in a compatibility fallback.

### Anti-trivialization verdict
| Check | Verdict | Reviewer basis |
| --- | --- | --- |
| Disclosure-collapse | PASS | Honest public outcomes and schema do not reveal the internal invariant. |
| Hidden-instance | PASS | Bundled, generated, healthy, and repeated scenarios require a general repair. |
| Single-artifact repair | PASS | Four typed boundaries and generated recovery cases prevent artifact replacement. |
| Generalization | PASS | Neutral generated identities and cycles extend beyond bundled fixtures. |
| Prompt-honesty | PASS | Every CLI, output field, and public property is documented. |
| Cheating-vs-difficulty | PASS | Anti-hardcoding protects tests; investigation and coordination create difficulty. |
| Mechanical-fix filter | PASS | No dependency, timeout, reward, or metadata repair is the task. |
| Localized-fix | PASS | Four distinct roots each control 4/12 tests. |
| Oracle-locality | PASS | Expected real semantic delta is 130–190 lines across four functions. |
| Small declarative-cluster | PASS | No policy table or report schema contains the behavioral solution. |
| Grep-collapse | PASS | Complete noun provenance has no selected path, symbol, parameter, or test hit. |
| Pre-factored-helper | PASS | Opaque names, plausible baseline bodies, typed responsibilities, and decoys avoid stub completion. |
| Recipe-discount | PASS | Healthy primitive wrappers leave project-specific authority reasoning. |
| Security-aura discount | PASS | Recovery authority, evidence falsification, and migration remain after removing crypto terminology. |
| Orthogonal-checklist | PASS | All four repairs enforce one stable authority-lineage invariant. |
| Harness-discount | PASS | Deterministic Docker and fixtures provide reproducibility only. |
| One-pass solvability | PASS | Obvious CLI and crypto code do not expose the identity disagreement or valid history. |
| Hard-only gate | PASS | Professional security-storage diagnosis and four-boundary coordination remain. |
| Discovery budget test | PASS | Five non-trivial discoveries have concrete homes and disclosure reasons. |
| Instruction specificity test | PASS | Minimal output schema is public contract; causes and implementation remain hidden. |
| Topology distribution test | PASS | Three four-location topologies are viable and no one location suffices. |

### Topology enumeration (3 candidate fix topologies)
1. **Selected typed boundaries:** `conductor/arc.go::trace_q`, `tenant/spine.go::settle_r`, `aperture/sill.go::route_s`, and `ledger/reel.go::replay_t`. The writer cannot inspect history, the context builder cannot authenticate, the opener cannot mutate stored history, and the journal validator cannot define future writes.
2. **Transactional migration:** `conductor/plan.go::draft_batch`, `model/codec.go::pack_frame`, `ledger/index.go::seek_prior`, and `aperture/open.go::open_one`. Planning, encoding, historical authority, and opening must agree; any isolated change leaves unsafe or unrecovered state.
3. **Provenance commit:** `keyring/catalog.go::select_epoch`, `tenant/table.go::axis_key`, `ledger/compact.go::keep_prior`, and `conductor/commit.go::apply_set`. Generation, stable identity, retention, and atomic commit jointly establish provenance; no one can substitute for the others.

### Rubric axes
- **Verifiable — PASS:** deterministic public reads, recovery inventory, state hashes, generated identities, and rejection cases are machine-checkable.
- **Well-specified — PASS:** all public commands, output fields, and outcome properties are explicit without implementation prescription.
- **Solvable — PASS:** all evidence and protected history are local, deterministic, and sufficient for an expert-hours investigation.
- **Difficult — PASS:** four manifestations of one authority-lineage disagreement must be diagnosed and repaired without weakening strict opening.
- **Interesting — PASS:** safe post-maintenance recovery of envelope-encrypted records is realistic paid incident work.
- **Outcome-verified — PASS:** final values, identity sets, bytes, isolation, and rejection are graded rather than process or representation.

### Hardness axes
- **Discover — PASS:** the stable authority representation, its divergent consumers, and valid history are absent from public prose.
- **Synthesize — PASS:** write, context, open, and journal boundaries share one invariant.
- **Diagnose — PASS:** the public report gives symptoms and outcomes, not causes.
- **Navigate coupling — PASS:** every partial repair leaves data unavailable, identity ambiguous, or substitutions accepted.
- **Reason beyond training — PASS:** standard primitives do not answer the bespoke lineage and recovery questions.

### Instruction completeness test
No. The instruction is sufficient to judge public correctness, including the recovery schema, but it does not identify the authority representation, divergent consumers, valid predecessor source, or safe coordination order.

## Reviewer Appendix

### Exact public instruction draft (reviewer-only)
After the last maintenance window, several services under `/app` can no longer read their secrets: the same records consistently fail authentication, and some service namespaces return namespace values they do not own. Repair the existing system and recover every affected secret to its correct pre-incident value with `/app/bin/vaultctl recover`. The command must write `/app/output/recovery.json` as a JSON object with one `recovered` array. Its array items have the form `{"service": "<string>", "secret": "<string>"}`. The array must list each affected service/secret identity once and no healthy identity. Healthy records must remain byte-for-byte unchanged. Read values with `/app/bin/vaultctl get <service> <secret>`; do not replace the bundled corpus or bypass authentication.

After recovery, `/app/bin/vaultctl maintain` must complete safely. A second run must leave the complete on-disk state byte-for-byte unchanged. `/app/bin/vaultctl get <service> <secret>` must read valid live records for newly introduced service namespaces without invoking recovery. It must still strictly fail when an intact protected record has been substituted across service namespaces, and that failure must not invoke recovery. `/app/bin/vaultctl audit` must succeed with every namespace isolated, recovered values readable, and tampered records and substituted records rejected. The same behavior must hold after a clean corpus reset and across additional generated namespaces and later maintenance cycles.

This draft is the noun-provenance source. Step 2b should preserve its complete public meaning and concise two-paragraph shape. If wording changes introduce, remove, or inflect a noun or domain-meaningful compound, amend the spec and all three token lists before construction continues.

### Implementation plan
Build a small existing Go service around typed `ItemID`, `AxisID`, `Epoch`, `Frame`, `Payload`, and `Scope` values. The baseline performs real maintenance, reads, compaction, and audit work; its four selected functions use plausible but mutually inconsistent representations of one authority identity. Logs and neutral inspection observations let a solver correlate symptoms and falsify key loss without directly naming a faulty function.

The oracle changes only the four committed functions. It canonicalizes and validates identity material at frame creation, derives scoped context from the same complete value, opens exactly one matching frame under the configured ring, and selects one authenticated predecessor from ordinary journal data. Existing CLI orchestration iterates affected records, commits validated frames, and emits the documented recovery inventory, so the oracle is a four-boundary repair rather than new command plumbing.

### Proposed file inventory
- `instruction.md` — concise symptoms-only public contract.
- `task.toml` — standard v2 hard security metadata, anonymous author, offline environment.
- `output_contract.toml` — `/app/output/recovery.json` schema and internal inspect declaration.
- `construction_manifest.json` — machine-readable copy of the four typed boundaries and ablations.
- `environment/Dockerfile` — digest-pinned Go build plus offline verifier dependencies.
- `environment/.dockerignore` — excludes VCS, caches, build outputs, tests, and solution.
- `environment/go.mod` — local standard-library Go module.
- `environment/Makefile` — deterministic build and reset targets.
- `environment/cmd/vaultctl/main.go` — existing public recover/get/maintain/audit dispatch.
- `environment/cmd/inspect/main.go` — neutral deterministic observation interface.
- `environment/conductor/arc.go` — selected protected-frame creation boundary.
- `environment/conductor/commit.go` — healthy atomic live-state commit logic.
- `environment/conductor/plan.go` — healthy maintenance work planning.
- `environment/conductor/dial.go` — executable telemetry decoy.
- `environment/tenant/spine.go` — selected scoped-context boundary.
- `environment/tenant/table.go` — healthy namespace table and parsing.
- `environment/tenant/cache.go` — healthy process-local lookup cache.
- `environment/tenant/relay.go` — executable label-normalization decoy.
- `environment/aperture/sill.go` — selected strict authenticated-open boundary.
- `environment/aperture/open.go` — healthy public read orchestration.
- `environment/aperture/check.go` — healthy audit aggregation.
- `environment/aperture/panel.go` — executable health-row decoy.
- `environment/ledger/reel.go` — selected journal predecessor-validation boundary.
- `environment/ledger/index.go` — ordinary stable item index.
- `environment/ledger/compact.go` — ordinary compaction and segment retention.
- `environment/ledger/journal.go` — journal loading and iteration types.
- `environment/ledger/spool.go` — executable compaction-metric decoy.
- `environment/model/item.go` — protected item and frame structures.
- `environment/model/codec.go` — neutral binary frame codec.
- `environment/model/types.go` — distinct opaque typed identifiers and payload aliases.
- `environment/keyring/ring.go` — configured ring and strict epoch lookup.
- `environment/keyring/catalog.go` — generation catalog and neutral probes.
- `environment/keyring/material.go` — deterministic protected key material.
- `environment/crypto/box.go` — healthy standard-library payload wrapper.
- `environment/crypto/wrap.go` — healthy key wrapping.
- `environment/crypto/primitives.go` — fixed primitive helpers.
- `environment/crypto/scope.go` — typed `Scope` representation and healthy low-level encoding support.
- `environment/config/policy.toml` — maintenance and retention policy.
- `environment/config/ring.toml` — deterministic generation configuration.
- `environment/docs/operator-guide.md` — realistic public operation context without repair steps.
- `environment/docs/storage-format.md` — neutral protected-frame format.
- `environment/docs/operations.md` — historical operator notes that remain experimentally testable.
- `environment/fixtures/live/catalog.json` — protected live index.
- `environment/fixtures/live/slice-01.bin` — protected live records.
- `environment/fixtures/live/slice-02.bin` — protected live records.
- `environment/fixtures/live/slice-03.bin` — protected live records.
- `environment/fixtures/segments/chunk-01.bin` — ordinary protected segment data.
- `environment/fixtures/segments/chunk-02.bin` — ordinary protected segment data.
- `environment/fixtures/segments/chunk-03.bin` — ordinary protected segment data.
- `environment/fixtures/logs/operations.ndjson` — realistic incident operations.
- `environment/scripts/reset-fixture.sh` — deterministic state reset.
- `environment/scripts/exercise-store.sh` — ordinary maintenance/read workflow.
- `environment/scripts/observe-store.sh` — neutral diagnostic workflow.
- `solution/solve.sh` — four-function substantive patch, rebuild, and public recovery.
- `tests/test.sh` — CM-007-safe offline pytest runner and reward footer.
- `tests/case_factory.py` — neutral verifier-owned case generation and expected values.
- `tests/test_outputs.py` — twelve opaque outcome tests.

The inventory has 48 non-Docker files under `environment/`, comfortably within `small`; no file exists only to satisfy the count.

### Oracle notes
`solve.sh` should apply targeted rewrites or a patch to the four committed functions, rebuild, reset, and invoke `/app/bin/vaultctl recover`. The expected substantive changes are:

- `trace_q` — approximately 30–45 real lines: validate typed inputs, serialize the complete axis and item identity with epoch information, bind frame metadata, and preserve deterministic ordering.
- `settle_r` — approximately 20–35 real lines: encode complete typed axis material into one unambiguous scoped context with validation and no lossy projection.
- `route_s` — approximately 35–50 real lines: resolve configured epoch material, require one matching scope and frame authority, perform the authenticated open, and reject alternate candidates.
- `replay_t` — approximately 45–60 real lines: traverse the journal deterministically, match stable item and axis identity, validate epoch and authenticated frame candidates, reject ambiguity, and return one predecessor.

The total target is 130–190 real semantic-delta lines. Existing healthy orchestration writes the recovered frames and schema; the oracle must not add a parallel recovery command, hardcode fixture values, copy protected segment files wholesale, modify tests, or touch decoys.

### Collapse audit
Stage: implementation-plan

Smallest plausible successful patch:
A coordinated four-function change that establishes one complete typed authority identity at write, context, open, and journal boundaries, followed by ordinary public recovery. Omitting any boundary leaves future writes unreadable, namespace contexts ambiguous, substitutions accepted, or historical recovery untrustworthy.

Likely editable frontier:
- `environment/conductor/arc.go::trace_q`
- `environment/tenant/spine.go::settle_r`
- `environment/aperture/sill.go::route_s`
- `environment/ledger/reel.go::replay_t`

Requirement-to-file map:
- Safe future maintenance and byte stability → A plus B, with C validating results.
- Namespace isolation → B plus C, with A required for newly maintained frames.
- Exact recovery and inventory → D plus C, with A required by the post-recovery maintenance workflow.
- Strict tamper and substitution rejection → C, constrained by A/B identity and D predecessor validation.

Oracle estimated complexity: 130–190 substantive changed lines.

Red flags:
- None at Step 2a. Construction must confirm plausible baseline bodies, neutral diagnostics, no central orchestrator referencing more than two frontier symbols, and exact ablation subsets.

Residual hardness:
The file tree reveals system responsibilities but not which authority representation is legitimate, why generations remain usable, where one valid predecessor can be proven, or why a compatibility fallback is unsafe. The solver still needs cross-surface evidence and a four-boundary migration model.

Collapse verdict: PASS

### Naming-pass record
**Instruction nouns extracted:**
maintenance, window, maintenance window, last maintenance window, services, app, secrets, records, same records, authentication, service, namespaces, service namespaces, namespace, namespace values, values, system, existing system, secret, affected secret, incident, pre-incident value, correct pre-incident value, value, bin, vaultctl, recover, command, output, recovery, recovery.json, JSON, object, JSON object, recovered, array, recovered array, items, array items, form, string, service/secret identity, affected service/secret identity, identity, healthy identity, healthy records, byte, byte-for-byte, get, bundled corpus, corpus, maintain, run, second run, state, on-disk state, complete on-disk state, audit, recovered values, tampered records, substituted records, behavior, same behavior, reset, corpus reset, clean corpus reset, generated namespaces, additional generated namespaces, cycles, maintenance cycles, later maintenance cycles

**Renames during drafting:**
- `runner/arc.go` → `conductor/arc.go`: removed the `run` substring.
- `namespace/context.go` → `tenant/spine.go`: removed the public namespace noun and direct symptom mapping.
- `recover_entry` → `replay_t`: removed the public recovery command and restoration locus.
- `test_prefix_collision` → `test_e06`: removed mechanism disclosure.

**Test names audited:**
- `test_e01`
- `test_e02`
- `test_e03`
- `test_e04`
- `test_e05`
- `test_e06`
- `test_e07`
- `test_e08`
- `test_e09`
- `test_e10`
- `test_e11`
- `test_e12`

**Concentration math:**
- Total tests: 12
- A (`conductor/arc.go`): 4/12 = `0.3333333333333333`
- B (`tenant/spine.go`): 4/12 = `0.3333333333333333`
- C (`aperture/sill.go`): 4/12 = `0.3333333333333333`
- D (`ledger/reel.go`): 4/12 = `0.3333333333333333`
- Cap: `0.34`; maximum: `0.3333333333333333`; status: PASS

### Per-test feasibility pre-check
- Test: `test_e01`
  Checks: Healthy maintenance control preserves reads and protected bytes.
  Valid approaches: 2+
  Chain-dependent: no; setup creates healthy state.
  Feasibility risk: LOW
- Test: `test_e02`
  Checks: Generated service identities remain isolated.
  Valid approaches: 2+
  Chain-dependent: no; setup creates all records.
  Feasibility risk: LOW
- Test: `test_e03`
  Checks: Valid current and historical authority cases open only when matching.
  Valid approaches: 2+
  Chain-dependent: no; no recovery prerequisite.
  Feasibility risk: LOW
- Test: `test_e04`
  Checks: Public recovery restores an independently generated damaged record.
  Valid approaches: 2+
  Chain-dependent: no; neutral setup creates the incident.
  Feasibility risk: LOW
- Test: `test_e05`
  Checks: Healthy maintenance is byte-stable on repetition.
  Valid approaches: 2+
  Chain-dependent: no.
  Feasibility risk: LOW
- Test: `test_e06`
  Checks: A broad generated label matrix remains isolated.
  Valid approaches: 2+
  Chain-dependent: no.
  Feasibility risk: LOW
- Test: `test_e07`
  Checks: Tampered and intact substituted records reject.
  Valid approaches: 2+
  Chain-dependent: no; cases are independently created.
  Feasibility risk: LOW
- Test: `test_e08`
  Checks: Recovery inventory is exact and healthy hashes are unchanged.
  Valid approaches: 2+
  Chain-dependent: no; setup owns affected and healthy sets.
  Feasibility risk: LOW
- Test: `test_e09`
  Checks: Full reset, recover, maintain twice, get, and audit workflow.
  Valid approaches: 2+
  Chain-dependent: no between tests; coupling is intentionally inside this test.
  Feasibility risk: LOW
- Test: `test_e10`
  Checks: Multiple generated public identities recover their own original values.
  Valid approaches: 2+
  Chain-dependent: no.
  Feasibility risk: LOW
- Test: `test_e11`
  Checks: Strict current and historical authority matching without recovery.
  Valid approaches: 2+
  Chain-dependent: no.
  Feasibility risk: LOW
- Test: `test_e12`
  Checks: Newly created generated identities remain isolated and byte-stable through two maintenance runs.
  Valid approaches: 2+
  Chain-dependent: no.
  Feasibility risk: LOW
