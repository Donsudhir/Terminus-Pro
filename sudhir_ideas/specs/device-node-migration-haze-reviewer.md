### Decision
GO — Attempt 2. Distributed three-location cutover topology across C and Rust (`loom/loom.c`, `veil/veil.rs`, `tether/tether.rs`); symptoms-only instruction; 0 FAIL / 0 WARN evidence after schema fix on attempt 1.

### Metadata
- Task name: device-node-migration-haze
- Title: Device Node Migration Haze
- Category: system-administration
- Languages: [c, rust]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [device-nodes, rootfs-migration, permissions, linux, service-restore]
- Milestones: 0

### Investigation profile
The primary weakness area is infrastructure debugging, reinforced by multi-component reasoning, partial failures, and hidden terminal/filesystem state. The task is one cutover incident: file counts and exit codes can look successful while device-backed opens/identity/path probes fail, a nearby file-only control stays healthy, and deliberately reject fixtures must stay rejected.

1. Run failing cutover beside file-only control and reject fixtures. Count-green / open-red concentrates after staging swap, justifying boundary-focused investigation.
2. Correlate logs, metrics, and cutover_report fields. Disagreement tracks special-file identity and open-path fields rather than ordinary bytes or the file-only control.
3. Trace packed ledger records and C rematerialization. Type/identity decode disagrees with the pre-cutover contract.
4. Probe mode/owner fidelity for ordinary versus special entries. Ordinary-file roster rules are applied to specials.
5. Inspect post-cutover open-path rebinding intermediates. Rebinding uses a wrong relative anchor.
6. Repair all three authorities, rebuild, and verify failing/control/reject matrices end-to-end.

Evidence surfaces are code (`crate/`, `probe/`), runtime-state (`/app/bin/haze` failing/control/reject runs), logs (`fixtures/logs/run_trace.ndjson`), metrics (count/probe counters in `cutover_report.json`), and filesystem (bundled trees and staging artifacts). Competing hypotheses include ordinary-file truncation, random udev reallocation, and harness fixture mismatch; each has a deterministic control-byte, offline-no-udev, or case-identity falsifier. The conditional matrix includes failing cutover / generated variants plus healthy file-only control and rejected reject fixtures. The estimate is 44 meaningful actions. All sources and fixtures are fixed and offline; resets avoid clocks, entropy, udev, and filesystem-order dependence.

### Discovery budget
- Discovery: Special-file entries are rematerialized from a packed ledger encoding whose type/identity decode disagrees with the pre-cutover contract, so count-green copies still yield wrong major/minor or node kind.
  Planned location: environment/loom/loom.c::knit_p
  Why instruction must not reveal it: Naming packed ledger decode or special-file rematerialization would collapse the C diagnosis into a disclosed mknod recipe.
- Discovery: The mode/owner fidelity pass applies ordinary-file roster rules to special entries, so permissions and ownership diverge from the pre-cutover contract even when node kind looks plausible.
  Planned location: environment/veil/veil.rs::hinge_q
  Why instruction must not reveal it: Naming mode stripping or roster fidelity for specials would directly expose the Rust repair and convert the task into a recipe.
- Discovery: Post-cutover service open-path rebinding uses a wrong staging-relative anchor or alias, so opens miss required nodes even when identity metadata is restored.
  Planned location: environment/tether/tether.rs::moor_r
  Why instruction must not reveal it: Naming relative-anchor rebinding or alias tables would reduce the third repair to a disclosed path rewrite.

### Anti-trivialization verdict
| Check | Verdict | Reviewer basis |
| --- | --- | --- |
| Disclosure-collapse | PASS | Honest failing/control/reject outcomes and schema citation do not reveal the three inconsistent authorities. |
| Hidden-instance | PASS | Bundled, generated, control, and broken scenarios require a general repair. |
| Single-artifact repair | PASS | Three roots and regenerated probe matrices prevent artifact replacement. |
| Generalization | PASS | Generated cutover variants extend beyond the bundled incident. |
| Prompt-honesty | PASS | Invocation, schema path, failing/control/reject outcomes, and hardcoding bans are documented. |
| Cheating-vs-difficulty | PASS | Anti-hardcoding protects tests; cross-language cutover diagnosis creates difficulty. |
| Mechanical-fix filter | PASS | No dependency, timeout, reward, or metadata repair is the task. |
| Localized-fix | PASS | Three distinct modules each control 4/12 tests. |
| Oracle-locality | PASS | Planned semantic delta is substantive across three functions, not one short rewrite. |
| Small declarative-cluster | PASS | Report schema documents keys only; it does not contain the behavioral solution. |
| Grep-collapse | PASS | Complete noun provenance has no selected path, symbol, parameter, or test hit. |
| Pre-factored-helper | PASS | Opaque names, plausible baseline bodies, and decoys avoid stub completion. |
| Recipe-discount | PASS | Archive-preserving copy or mknod recipes leave fidelity and rebinding defects. |
| Security-aura discount | PASS | System cutover fidelity remains after removing any exploit framing. |
| Orthogonal-checklist | PASS | Open/identity/path, control green, and broken reject are one coupled invariant. |
| Harness-discount | PASS | Deterministic Docker and fixtures provide reproducibility only. |
| One-pass solvability | PASS | Obvious entrypoints do not expose all three authorities or their coupling. |
| Hard-only gate | PASS | Professional device-node cutover diagnosis and three-boundary coordination remain. |
| Discovery budget test | PASS | Three non-trivial discoveries have concrete homes and disclosure reasons. |
| Instruction specificity test | PASS | Symptoms-only; schema is public contract; causes remain hidden. |
| Topology distribution test | PASS | Three ≥3-location topologies are viable and no one location suffices. |

### Topology enumeration (3 candidate fix topologies)
1. **topology_a_selected** — `loom/loom.c::knit_p`, `veil/veil.rs::hinge_q`, `tether/tether.rs::moor_r`. No single location suffices because materialization, fidelity, and rebinding failures are independently observable on failing/control/reject matrices.
2. **topology_b_lifecycle_chain** — `loom/loom.c::knit_p`, `veil/veil.rs::hinge_q`, `tether/tether.rs::moor_r`, `crate/pass_loom.rs::swing_u`. Correct ledger decode fails without rematerialization and fidelity; correct upstream state fails under wrong relative anchors.
3. **topology_c_authority_map** — `loom/loom.c::knit_p`, `veil/veil.rs::hinge_q`, `tether/tether.rs::moor_r`. Identity packing, roster fidelity keys, and alias anchors must agree end-to-end after staging swap.

### Rubric axes
- **Verifiable — PASS:** open/identity/path probes, control byte identity, broken rejects, and regenerated reports are machine-checkable.
- **Well-specified — PASS:** symptoms, invocation, schema citation, and prohibited hardcoding are clear.
- **Solvable — PASS:** bounded existing toolkit; expert hours, not research years.
- **Difficult — PASS:** hard after honest disclosure; causes not named.
- **Interesting — PASS:** real service-root cutover engineering value in systems operations.
- **Outcome-verified — PASS:** any correct implementation accepted.

### Hardness axes
- **Discover — PASS:** three hidden facts must be recovered from code/runtime.
- **Synthesize — PASS:** C and Rust authorities across three modules.
- **Diagnose — PASS:** symptoms-only instruction.
- **Navigate coupling — PASS:** subset fixes leave other failing/control/reject properties red.
- **Reason beyond training — PASS:** not reducible to textbook archive-copy or mknod recipes.

### Collapse audit (Part A)
- **Verdict:** PASS
- **Residual hardness:** After the full tree is visible, the solver must still reconcile packed materialization, special-entry fidelity, and staging-relative rebinding as one cutover invariant.
- **Smallest plausible patch:** substantive edits at all three selected locations; any strict subset fails.
- **Editable frontier:** `loom/loom.c`, `veil/veil.rs`, `tether/tether.rs` with real decoys nearby.
- **Red flags:** none recorded.

### Independent CM-010 review notes
- Flipping points are not mutually absorbable: materialization identity failures remain when only fidelity/rebinding are fixed; fidelity mode/owner failures remain when only materialization/rebinding are fixed; path misses remain when only materialization/fidelity are fixed.
- Causal stages are skip-resistant: control/reject matrix characterization unlocks boundary focus; ledger decode unlocks fidelity scrutiny; fidelity unlocks rebinding scrutiny.
- Noun provenance was re-extracted from the exact public-contract prose and audited against selected paths, symbols, parameters, and test names (0 substring hits).
- Every planned assertion family has a solver-visible contract home in instruction symptoms or the cited schema (opens/identities/paths, control green, broken rejected, report keys).

### Construction risks for Step 2b
- Do not let decoy helpers become the obvious “device” or “bind” modules.
- Keep packed ledger opaque; do not ship human-readable major/minor answer tables in solver-visible fixtures.
- Preserve reject polarity for reject fixtures; never teach the oracle to accept them.
- Enforce CM-007 on `tests/test.sh` and CM-001 Dockerfile python/asciinema hygiene from the first draft.
- Agent-facing languages must remain C and Rust only (ADR-0014).
