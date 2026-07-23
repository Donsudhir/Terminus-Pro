### Decision
GO — Attempt 2. Distributed three-location fixed-timestep replay topology across C++ and Rust (`lane/`, `draw/`, `mark/`); symptoms-only instruction; duration-gated long/short matrix; 0 FAIL / 0 WARN evidence.

### Metadata
- version: 2
- Task name: input-ring-physics-desync
- Title: Input Ring Physics Desync
- Category: games
- Languages: [c++, rust]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [deterministic-replay, game-simulation, input-buffer, fixed-timestep, state-digest]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites beyond the construction manifest, or an exhaustive hidden bug narrative here.

### Public contract

The headless game lab under `/app` records inputs and claims deterministic replay. Fresh live sessions look fine, but replays of the same seed diverge in entity-state digests after a few hundred ticks while tick-count overlays remain green. A short healthy-control replay stays bit-stable. Correct the pipeline so failing long replays match the recorded outcome digests, and so the short healthy control stays bit-identical. Do not accept approximate physics. Rebuild and invoke `/app/bin/simlab`. Emit `/app/output/replay_report.json` whose keys and layout follow the normative schema documented in `/app/docs/replay-report-schema.md`. Do not replace the bundled inputs or write the report by hand; the checks regenerate it through the compiled pipeline.

### Failure topology

Symptom clusters are digest-wrong / tick-count-green long replays, short healthy-control bit stability, and rejection of approximate integration shortcuts. Hardness comes from three interacting authorities — lane slot retirement versus tick consume boundary, fixed-step draw/apply count under long traces, and seal-side sample phase relative to post-apply snapshots — none of which alone explains every failure mode. The instruction stays symptoms-only; causes and algorithms are not named.

### Investigation architecture

Use four reinforcing weakness areas: long-horizon debugging, multi-component reasoning, partial failures, and ambiguous bug reports. The intended six-stage progression is: characterize long digest disagreement beside the short healthy control; correlate traces/metrics with duration bands; recover the lane-vs-tick boundary fact; recover the per-step draw mismatch; recover the seal sample-phase fact; then coordinate all three repairs and verify end-to-end long/short outcomes. Evidence spans code, runtime observations, logs, metrics, and filesystem recordings. The deterministic offline investigation is estimated at 52 meaningful terminal actions; that estimate is authoring evidence, never a scored process requirement.

### Environment shape

Major subsystems under `environment/`:

- `lane/` — C++ buffered-sample lane authority and related helpers (selected + decoy)
- `draw/` — Rust fixed-step draw/apply orchestration, report assembly, FFI
- `mark/` — C++ seal-side sample/fold and diagnostic tallies
- `core/` — shared headers, runtime glue, and headless driver
- `data/` / `fixtures/` — bundled traces, shelves, and cause-free run traces
- `docs/` — architecture notes plus normative `replay-report-schema.md` (WW-010)
- `conf/` — runtime defaults that are not a one-knob fix surface
- build scripts and a digest-pinned offline Dockerfile with `.dockerignore`

### Required artifacts

Step 2b must create instruction.md, task.toml, output_contract.toml if required by harness, environment/ with ≥20 substantive files, tests/ (test.sh + opaque scored tests), solution/solve.sh, and construction-manifest-faithful selected locations plus decoys. No milestones. No UI. `allow_internet = false`. Normative report keys live in `/app/docs/replay-report-schema.md` and must be cited from instruction.md (WW-010).

### Test plan

At least twelve opaque scored tests (`test_m01`–`test_m12`):

1. `test_m01` — long same-seed replay entity-state digest matches recorded outcome (lane-sensitive)
2. `test_m02` — long-trace family regenerates digest parity under the same public contract (lane-sensitive)
3. `test_m03` — short healthy-control replay remains bit-identical across clean rebuilds (draw/control)
4. `test_m04` — emitted digest fields in replay_report agree with independent post-apply fold (mark-sensitive)
5. `test_m05` — approximate-integration shortcut still fails long digest parity (draw/anti-approx)
6. `test_m06` — combined long parity under lane+draw interaction (lane+draw)
7. `test_m07` — tick-count overlay coherence does not mask digest disagreement after repair (draw-sensitive)
8. `test_m08` — seal fold uses post-apply phase on long traces (mark-sensitive)
9. `test_m09` — report summary fields agree with emitted digests (mark-sensitive)
10. `test_m10` — reordered execution of the same long family remains deterministic (lane-sensitive)
11. `test_m11` — short control stays bit-identical when long families are exercised first (draw/control)
12. `test_m12` — clean rebuild byte identity of replay_report after mark path on long+short matrix (mark+control)

Multiple valid algorithmic approaches are allowed if outcomes hold. Tests are metamorphic/property-based against regenerated long/short matrices, not golden-file clones of the oracle.

### Drafting guardrails

Do not leak ring desync, consume skew, sample phase, input-buffer, or fix-path names through instruction text, comments, helper names on the fix path, test names, or fixture labels. Keep decoys doing real non-fix work. Forbidden instruction nouns are banned from fix-path code symbols only. Cite `/app/docs/replay-report-schema.md` from instruction.md for every graded JSON key.

### Triviality Ledger

- **Global timestep tweak / fixed-dt only:** blocked because lane boundary and seal sample phase remain broken even when draw is forced to a textbook dt, and short controls already pass without that tweak.
- **Rewrite recorded digests / golden reports:** blocked by regenerated long/short matrices and independent fold checks with no solver-visible expected digests.
- **Fix only tick-count overlays:** blocked by entity-state digest tests that stay red when overlays look green.
- **Approximate physics shortcut:** blocked by explicit anti-approximate tests and long digest contracts.
- **Prompt-noun grep:** blocked by opaque selected paths/symbols and the audited forbidden-token list.
- **One location flipping the score:** blocked by twelve tests with three locations at 4/12 under the 0.5 concentration cap.
- **Decorative language diversity:** blocked because C++ owns lane authority and seal fold, Rust owns draw/apply.
- **Fixture or manifest repair:** blocked because the baseline builds and runs while hidden tests regenerate long/short pairs.

### Per-gate Pitfall Inventory

- **RC1 instruction honesty:** keep symptoms-only; re-audit after any wording change for algorithm/threshold/cause leaks (especially ring/consume/sample phrasing).
- **RC2 oracle locality:** require substantive edits at A–C; reject single-file rewrite or compiler-flag-only “fixes.”
- **RC3 nop/baseline:** untouched baseline must compile, run, and fail a majority of scored tests for simulation reasons while short controls already look healthy.
- **RC4 anti-cheat:** regenerate reports and long/short matrices; never ship expected digests on solver-visible surfaces.
- **RC5 determinism:** no clocks, RNG, network, or host-dependent paths; clean rebuild byte identity required; pin reduction order.
- **RC6 category fit:** primary work is games/simulation deterministic replay, not generic debugging theater.
- **RC7 environment scale:** ship ≥20 meaningful environment files; no padding empty stubs.
- **GX1 Docker offline:** digest-pinned base, all deps at build time, `allow_internet = false`.
- **GX3 collapse/flipping-point:** verify each location controls only its declared ≤0.5 subset after oracle green.
- **GX9 naming/grep:** enforce construction-manifest symbols and forbidden-token ban on the fix path (watch `bin` substring in names).
- **GX10 packaging:** exclude solution, tests, reviewer material, and caches from the image and zip.
- **Static checks:** anonymous author fields, version 2.0 task.toml, `.dockerignore` present; CM-007 verifier triad; CM-016 early reward write.
- **WW-010 schema citation:** instruction.md must cite `/app/docs/replay-report-schema.md` for graded keys.
- **ADR-0014 / CM-011:** agent-facing languages are C++ and Rust only; pytest is verifier-only and must not appear in languages metadata.

### Initial Draft Commitments

- `instruction.md`
- `task.toml`
- `output_contract.toml`
- `environment/Dockerfile`
- `environment/.dockerignore`
- `environment/Makefile`
- `environment/verifier-requirements.txt`
- `environment/conf/runtime.conf`
- `environment/docs/architecture.md`
- `environment/docs/replay-report-schema.md`
- `environment/docs/data-format.md`
- `environment/data/families.trace`
- `environment/fixtures/logs/run_trace.ndjson`
- `environment/fixtures/traces/alpha.bin`
- `environment/lane/knit.cpp`
- `environment/lane/ledge.cpp`
- `environment/lane/ember.cpp`
- `environment/lane/include/knit.h`
- `environment/lane/include/common.h`
- `environment/draw/main.rs`
- `environment/draw/step.rs`
- `environment/draw/locker.rs`
- `environment/draw/relay.rs`
- `environment/draw/ffi.rs`
- `environment/draw/report.rs`
- `environment/draw/error.rs`
- `environment/draw/config.rs`
- `environment/mark/fold.cpp`
- `environment/mark/tally.cpp`
- `environment/core/driver.cpp`
- `environment/core/include/driver.h`
- `environment/tools/build_all.sh`
- `environment/tools/run_simlab.sh`
- `tests/test.sh`
- `tests/test_outputs.py`
- `solution/solve.sh`
- `construction_manifest.json`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: lane/knit.cpp
  symbol: knit_u
  kind: function
  signature: int32_t knit_u(const int32_t* a, int32_t b, uint64_t* c);
  purpose: Aligns lane slot retirement with the integrator consume boundary.

- path: draw/step.rs
  symbol: pull_v
  kind: function
  signature: pub(crate) fn pull_v(a: u64, b: &mut DrawBuf) -> i8
  purpose: Selects how many buffered intents the fixed step applies.

- path: mark/fold.cpp
  symbol: fold_w
  kind: function
  signature: int32_t fold_w(const uint64_t* a, int32_t b, uint64_t* c);
  purpose: Folds body samples into a stable digest at the post-apply phase.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: lane/knit.cpp
    controls_tests: [test_m01, test_m02, test_m06, test_m10]
  - id: B
    path: draw/step.rs
    controls_tests: [test_m03, test_m05, test_m07, test_m11]
  - id: C
    path: mark/fold.cpp
    controls_tests: [test_m04, test_m08, test_m09, test_m12]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: lane/ledge.cpp
  kind: helper
  rhymes_with: knit_u
  non_fix_purpose: Computes ordinary lane occupancy banners for diagnostics.

- path: draw/locker.rs
  kind: helper
  rhymes_with: pull_v
  non_fix_purpose: Maps display codes for status lines without changing draw counts.

- path: mark/tally.cpp
  kind: helper
  rhymes_with: fold_w
  non_fix_purpose: Folds scalar diagnostic marks into aggregate counters.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [headless, game, lab, app, inputs, deterministic, replay, live, sessions, seed, entity-state, digests, ticks, tick-count, overlays, healthy-control, bit-stable, pipeline, long, replays, recorded, outcome, short, control, approximate, physics, bin, simlab, output, replay_report, json, keys, layout, schema, docs, replay-report-schema, bundled, report, checks, compiled, healthy, bit-identical, normative]
```
