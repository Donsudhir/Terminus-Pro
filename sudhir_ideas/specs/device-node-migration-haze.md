### Decision
GO — Attempt 2. Distributed three-location cutover topology across C and Rust (`crate/loom.c`, `crate/veil.rs`, `crate/tether.rs`); symptoms-only instruction; 0 FAIL / 0 WARN evidence after schema fix on attempt 1.

### Metadata
- version: 2
- Task name: device-node-migration-haze
- Title: Device Node Migration Haze
- Category: system-administration
- Languages: [c, rust]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [device-nodes, rootfs-migration, permissions, linux, service-restore]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites beyond the construction manifest, or an exhaustive hidden bug narrative here.

### Public contract

The cutover lab under `/app` copies a service root between staging trees. The tool reports success from file counts and exit codes. After cutover, device-backed services fail to open required nodes, lose expected major/minor identity, or bind the wrong path, while ordinary file bytes look intact. A non-device healthy control tree still migrates cleanly. Deliberately invalid device fixtures must remain rejected.

Correct the pipeline so post-cutover opens, identities, and paths match the pre-cutover contract on failing fixtures, the file-only control stays green, and reject fixtures stay rejected. Rebuild and invoke `/app/bin/haze`. Emit `/app/output/cutover_report.json` whose keys and layout follow the normative schema in `/app/docs/cutover-report-schema.md`. Do not replace the bundled fixtures or write the report by hand; the checks regenerate it through the compiled pipeline.

### Failure topology

Symptom clusters are count-green / open-red disagreement after staging cutover, major/minor identity or path binding failures on device-backed fixtures, a nearby file-only healthy control that migrates cleanly, and deliberately reject fixtures that must stay rejected. Hardness comes from three interacting authorities — packed special-file materialization in C, special-entry mode/owner fidelity in Rust, and staging-relative open-path rebinding in Rust — none of which alone explains every failure mode. The instruction stays symptoms-only; causes and algorithms are not named.

### Investigation architecture

Use four reinforcing weakness areas: infrastructure debugging, multi-component reasoning, partial failures, and hidden terminal/filesystem state. The intended six-stage progression is: characterize count-green / open-red cutover beside the healthy file-only control and rejected invalid fixtures; correlate logs/metrics with the staging-swap boundary; recover the packed materialization fact; recover the special-entry fidelity fact; recover the relative-anchor rebinding fact; then coordinate all three repairs and verify end-to-end failing/control/reject outcomes. Evidence spans code, runtime observations, logs, metrics, and filesystem staging/fixture state. The deterministic offline investigation is estimated at 44 meaningful terminal actions; that estimate is authoring evidence, never a scored process requirement.

### Environment shape

Major subsystems under `environment/`:

- `loom/` — C packed-ledger materialization (`knit_p`) plus decoy helper
- `veil/` — Rust special-entry fidelity (`hinge_q`) plus decoy helper
- `tether/` — Rust staging-relative rebinding (`moor_r`) plus decoy helper
- `crate/` — orchestration only (main/relay/report/config/ffi/pass_* wrappers); no selected fix sites
- `probe/` — deterministic open/identity probe helpers used by the pipeline and verifier-facing runs
- `ledger/` — packed special-entry records and roster samples (not a one-table fix surface)
- `fixtures/` — failing trees, file-only control trees, reject fixtures, and cause-free run traces
- `docs/` — architecture notes plus normative `cutover-report-schema.md` (WW-010)
- `conf/` — runtime defaults that are not a one-knob fix surface
- build scripts and a digest-pinned offline Dockerfile with `.dockerignore`

### Required artifacts

Step 2b must create instruction.md, task.toml, output_contract.toml if required by harness, environment/ with ≥20 substantive files, tests/ (test.sh + opaque scored tests), solution/solve.sh, and construction-manifest-faithful selected locations plus decoys. No milestones. No UI. `allow_internet = false`. Normative report keys live in `/app/docs/cutover-report-schema.md` and must be cited from instruction.md (WW-010).

### Test plan

At least twelve opaque scored tests (`test_h01`–`test_h12`):

1. `test_h01` — post-cutover major/minor identity matches pre-cutover contract on bundled failing fixture (materialization-sensitive)
2. `test_h02` — post-cutover node kind / openability matches pre-cutover contract on failing fixture (materialization-sensitive)
3. `test_h03` — mode/owner fidelity on special entries matches pre-cutover contract (fidelity-sensitive)
4. `test_h04` — post-cutover open paths resolve to required nodes on failing fixture (rebinding-sensitive)
5. `test_h05` — sequential cutover families do not inherit prior roster fidelity mistakes (fidelity-sensitive)
6. `test_h06` — combined open+identity under cutover with materialization+fidelity interaction (materialization+fidelity)
7. `test_h07` — count/exit plausibility does not mask identity disagreement after repair (fidelity-sensitive)
8. `test_h08` — rebinding uses post-swap relative anchors on failing fixtures (rebinding-sensitive)
9. `test_h09` — report summary fields agree with emitted open/identity probe results (rebinding-sensitive)
10. `test_h10` — reordered execution of the same family is deterministic for identity probes (materialization+fidelity)
11. `test_h11` — file-only healthy control remains successful and byte-identical across clean rebuilds (fidelity/control)
12. `test_h12` — deliberately invalid reject fixtures remain rejected; cutover_report stay consistent after rebinding path (rebinding+reject)

Multiple valid algorithmic approaches are allowed if outcomes hold. Tests are metamorphic/property-based against regenerated probes and controls, not golden-file clones of the oracle.

### Drafting guardrails

Do not leak mknod, mode stripping, alias anchors, packed-ledger decode, or fix-path names through instruction text, comments, helper names on the fix path, test names, or fixture labels. Keep decoys doing real non-fix work. Forbidden instruction nouns are banned from fix-path code symbols only. Cite `/app/docs/cutover-report-schema.md` from instruction.md for every graded JSON key.

### Triviality Ledger

- **Naive archive-preserving copy (`cp -a` / `rsync -a`):** blocked because packed ledger materialization and staging-relative rebinding remain broken even when ordinary files preserve metadata, and the file-only control already passes without that shortcut.
- **Rewrite staging trees / golden report fields:** blocked by regenerated probe/control/reject matrices and independent open/identity checks with no solver-visible expected digests.
- **Fix only file counts / exit codes:** blocked by open/identity/path tests that stay red when counts look successful.
- **Prompt-noun grep:** blocked by opaque selected paths/symbols and the audited forbidden-token list.
- **One location flipping the score:** blocked by twelve tests with three locations at 4/12 under the 0.5 concentration cap.
- **Loosen reject-fixture rejects to pass opens:** blocked by reject-contract tests that must stay red on deliberately reject fixtures.
- **Fixture or manifest repair:** blocked because the baseline builds and runs while hidden tests regenerate failing/control/reject matrices.

### Per-gate Pitfall Inventory

- **RC1 instruction honesty:** keep symptoms-only; re-audit after any wording change for algorithm/threshold/cause leaks (especially mknod/mode/alias phrasing).
- **RC2 oracle locality:** require substantive edits at A–C; reject single-file rewrite or compiler-flag-only “fixes.”
- **RC3 nop/baseline:** untouched baseline must compile, run, and fail a majority of scored tests for cutover reasons while file-only controls already look healthy.
- **RC4 anti-cheat:** regenerate reports and probes; never ship expected identity tables on solver-visible surfaces.
- **RC5 determinism:** no clocks, RNG, network, udev, or host-dependent paths; clean rebuild byte identity required; pin packed-ledger decode order.
- **RC6 category fit:** primary work is system-administration cutover fidelity, not generic debugging theater.
- **RC7 environment scale:** ship ≥20 meaningful environment files; no padding empty stubs.
- **GX1 Docker offline:** digest-pinned base, all deps at build time, `allow_internet = false`.
- **GX3 collapse/flipping-point:** verify each location controls only its declared ≤0.5 subset after oracle green.
- **GX9 naming/grep:** enforce construction-manifest symbols and forbidden-token ban on the fix path.
- **GX10 packaging:** exclude solution, tests, reviewer material, and caches from the image and zip.
- **Static checks:** anonymous author fields, version 2.0 task.toml, `.dockerignore` present; CM-007 verifier triad; CM-001 python/asciinema hygiene.
- **WW-010 schema citation:** instruction.md must cite `/app/docs/cutover-report-schema.md` for graded keys.
- **ADR-0014 / CM-011:** agent-facing languages stay C and Rust; pytest is verifier-only and must not appear in agent language metadata.

### Initial Draft Commitments

- `instruction.md`
- `task.toml`
- `output_contract.toml`
- `environment/Dockerfile`
- `environment/.dockerignore`
- `environment/Makefile`
- `environment/Cargo.toml`
- `environment/verifier-requirements.txt`
- `environment/conf/runtime.conf`
- `environment/docs/architecture.md`
- `environment/docs/cutover-report-schema.md`
- `environment/docs/data-format.md`
- `environment/ledger/packed.bin`
- `environment/ledger/roster.sample`
- `environment/fixtures/logs/run_trace.ndjson`
- `environment/fixtures/trees/failing_alpha/`
- `environment/fixtures/trees/control_plain/`
- `environment/fixtures/trees/reject_delta/`
- `environment/loom/loom.c`
- `environment/loom/ledge.c`
- `environment/loom/include/loom.h`
- `environment/loom/include/common.h`
- `environment/crate/include/common.h`
- `environment/crate/main.rs`
- `environment/crate/relay.rs`
- `environment/crate/report.rs`
- `environment/crate/error.rs`
- `environment/crate/config.rs`
- `environment/crate/ffi.rs`
- `environment/crate/pass_loom.rs`
- `environment/crate/pass_veil.rs`
- `environment/crate/pass_tether.rs`
- `environment/veil/veil.rs`
- `environment/veil/cloak.rs`
- `environment/tether/tether.rs`
- `environment/tether/berth.rs`
- `environment/probe/open_probe.c`
- `environment/probe/include/open_probe.h`
- `environment/tools/build_all.sh`
- `environment/tools/run_haze.sh`
- `tests/test.sh`
- `tests/test_outputs.py`
- `solution/solve.sh`
- `construction_manifest.json`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: loom/loom.c
  symbol: knit_p
  kind: function
  signature: int32_t knit_p(const uint8_t* a, size_t b, uint64_t* c);
  purpose: Decodes packed ledger records and rematerializes special entries into the destination staging tree.

- path: veil/veil.rs
  symbol: hinge_q
  kind: function
  signature: pub(crate) fn hinge_q(a: u64, b: &mut Roster) -> i8
  purpose: Applies mode and owner fidelity for entries during cutover using the active roster context.

- path: tether/tether.rs
  symbol: moor_r
  kind: function
  signature: pub(crate) fn moor_r(a: u64, b: &mut Anchor) -> i8
  purpose: Rebinds open targets after staging swap under the active relative-anchor context.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: loom/loom.c
    controls_tests: [test_h01, test_h02, test_h06, test_h10]
  - id: B
    path: veil/veil.rs
    controls_tests: [test_h03, test_h05, test_h07, test_h11]
  - id: C
    path: tether/tether.rs
    controls_tests: [test_h04, test_h08, test_h09, test_h12]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: loom/ledge.c
  kind: helper
  rhymes_with: knit_p
  non_fix_purpose: Counts ordinary entries for diagnostic banners without rematerializing specials.

- path: veil/cloak.rs
  kind: helper
  rhymes_with: hinge_q
  non_fix_purpose: Maps display codes for status lines without changing roster fidelity.

- path: tether/berth.rs
  kind: helper
  rhymes_with: moor_r
  non_fix_purpose: Formats alias labels for logs without rebinding open targets.
```

#### code_forbidden_tokens

```
app, bin, bind, broken, bundled, bytes, checks, code, codes, compiled, contract,
control, counts, cutover, cutover-report-schema, cutover_report, device,
device-backed, docs, emit, exit, expected, failing, file, file-only, fixture,
fixtures, green, hand, haze, healthy, identities, identity, intact, invoke,
json, keys, lab, layout, major, major/minor, migrates, minor, node, nodes,
non-device, normative, opens, ordinary, output, path, paths, pipeline,
pre-cutover, rebuild, regenerate, rejected, remain, replace, report, required,
root, schema, service, services, staging, success, tool, tree, trees, write
```
