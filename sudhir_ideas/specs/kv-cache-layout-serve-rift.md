### Decision
GO — Attempt 3. Distributed three-location short/long greedy-serve topology across C++ and Rust (`native/reed.cpp`, `host/silt.rs`, `host/weld.rs`); symptoms-only instruction; 0 FAIL / 0 WARN evidence after schema fix on attempts 1–2 (`recomputed_concentration` removed).

### Metadata
- version: 2
- Task name: kv-cache-layout-serve-rift
- Title: KV Cache Layout Serve Rift
- Category: machine-learning
- Languages: [c++, rust]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [inference, kv-cache, positional-encoding, token-decode, model-serving]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites beyond the construction manifest, or an exhaustive hidden bug narrative here.

### Public contract

The offline kiln lab under `/app` loads exported weights and runs greedy decode for fixed prompts. Training-side export checks pass. Short prompts match golden token sequences. Longer prompts diverge while cache-hit counters and latency summaries still look healthy. Short-prompt controls must remain unchanged.

Correct the pipeline so long-prompt greedy sequences match the golden sequences without breaking short-prompt controls or inventing a new model architecture. Rebuild and invoke `/app/bin/kiln`. Emit `/app/output/ember_report.json` whose keys and layout follow the normative schema documented in `/app/docs/ember-report-schema.md`. Do not replace the bundled prompts or write the report by hand; the checks regenerate it through the compiled pipeline.

### Failure topology

Symptom clusters are short-prompt-green / long-prompt-wrong greedy decode disagreement, healthy-looking cache-hit and latency summaries that must not count as success, and nearby short-prompt controls that must remain unchanged. Hardness comes from three interacting authorities — native exported-weight binding, host incremental working-set slot indexing, and host serve-time sequence-index offsets — none of which alone explains every failure mode. The instruction stays symptoms-only; causes and algorithms are not named.

### Investigation architecture

Use four reinforcing weakness areas: long-horizon debugging, multi-component reasoning, partial failures, and misleading documentation. The intended six-stage progression is: characterize short-green / long-wrong decode beside healthy cache-hit/latency bait; correlate logs/metrics with the short-to-long generation boundary; recover the export-binding fact; recover the working-set slot-indexing fact; recover the sequence-index offset fact; then coordinate all three repairs and verify end-to-end short/long outcomes. Evidence spans code, runtime observations, logs, metrics, and filesystem export/prompt state. The deterministic offline investigation is estimated at 46 meaningful terminal actions; that estimate is authoring evidence, never a scored process requirement.

### Environment shape

Major subsystems under `environment/`:

- `native/` — C++ export binding and related helpers (selected + decoy)
- `host/` — Rust orchestration, working-set slots, sequence-index offsets, report assembly, FFI
- `probe/` — deterministic short/long decode helpers used by the pipeline and verifier-facing runs
- `data/` / `fixtures/` — prompt families, export samples, and cause-free run traces
- `docs/` — architecture notes plus normative `ember-report-schema.md` (WW-010)
- `conf/` — runtime defaults that are not a one-knob fix surface
- build scripts and a digest-pinned offline Dockerfile with `.dockerignore`

### Required artifacts

Step 2b must create instruction.md, task.toml, output_contract.toml if required by harness, environment/ with ≥20 substantive files, tests/ (test.sh + opaque scored tests), solution/solve.sh, and construction-manifest-faithful selected locations plus decoys. No milestones. No UI. `allow_internet = false`. Normative report keys live in `/app/docs/ember-report-schema.md` and must be cited from instruction.md (WW-010).

### Test plan

At least twelve opaque scored tests (`test_e01`–`test_e12`):

1. `test_e01` — long-prompt greedy sequence matches golden on bundled failing family (binding-sensitive)
2. `test_e02` — long-prompt family variant golden match (binding-sensitive)
3. `test_e03` — incremental working-set slot consistency on long prompts (slot-sensitive)
4. `test_e04` — emitted sequence fields in ember_report agree with independent fold (offset-sensitive)
5. `test_e05` — sequential long runs do not inherit prior slot identity (slot-sensitive)
6. `test_e06` — combined long golden under binding+slot interaction (binding+slot)
7. `test_e07` — cache-hit/latency plausibility does not mask sequence disagreement after repair (slot-sensitive)
8. `test_e08` — sequence-index offsets use correct indices on long trajectories (offset-sensitive)
9. `test_e09` — report summary fields agree with emitted sequences (offset-sensitive)
10. `test_e10` — reordered execution of the same family is deterministic for long goldens (binding+slot)
11. `test_e11` — short-prompt healthy control remains golden across clean rebuilds (slot/control)
12. `test_e12` — clean rebuild byte identity of ember_report on long+short matrix (offset+control)

Multiple valid algorithmic approaches are allowed if outcomes hold. Tests are metamorphic/property-based against regenerated short/long matrices, not golden-file clones of the oracle.

### Drafting guardrails

Do not leak KV stride, RoPE/phase, weight-layout packing, cache invalidation, or fix-path names through instruction text, comments, helper names on the fix path, test names, or fixture labels. Keep decoys doing real non-fix work. Forbidden instruction nouns are banned from fix-path code symbols only. Cite `/app/docs/ember-report-schema.md` from instruction.md for every graded JSON key.

### Triviality Ledger

- **Tokenizer / truncation retune:** blocked because export binding and sequence-offset authorities remain broken even when inputs are unchanged, and short controls already pass without that retune.
- **Enable prefix caching / flush cache:** blocked because slot indexing and sequence offsets remain broken even when cache-hit counters look healthy, and tests reject cache-hit/latency as success.
- **Rewrite golden sequences / report fields:** blocked by regenerated short/long matrices and independent fold checks with no solver-visible expected digests.
- **Fix only short prompts:** blocked by long-prompt golden tests that stay red when short controls look green.
- **Prompt-noun grep:** blocked by opaque selected paths/symbols and the audited forbidden-token list.
- **One location flipping the score:** blocked by twelve tests with three locations at 4/12 under the 0.5 concentration cap.
- **Invent a new model architecture:** blocked because the public contract forbids architecture invention and tests grade the existing pipeline outcomes only.
- **Fixture or manifest repair:** blocked because the baseline builds and runs while hidden tests regenerate short/long matrices.

### Per-gate Pitfall Inventory

- **RC1 instruction honesty:** keep symptoms-only; re-audit after any wording change for algorithm/threshold/cause leaks (especially KV/RoPE/layout phrasing).
- **RC2 oracle locality:** require substantive edits at A–C; reject single-file rewrite or compiler-flag-only “fixes.”
- **RC3 nop/baseline:** untouched baseline must compile, run, and fail a majority of scored tests for long-prompt reasons while short controls already look healthy.
- **RC4 anti-cheat:** regenerate reports and short/long matrices; never ship expected sequence digests on solver-visible surfaces.
- **RC5 determinism:** no clocks, RNG, network, or host-dependent paths; clean rebuild byte identity required; pin reduction and slot traversal order.
- **RC6 category fit:** primary work is machine-learning offline serve correctness, not generic debugging theater.
- **RC7 environment scale:** ship ≥20 meaningful environment files; no padding empty stubs.
- **GX1 Docker offline:** digest-pinned base, all deps at build time, `allow_internet = false`.
- **GX3 collapse/flipping-point:** verify each location controls only its declared ≤0.5 subset after oracle green.
- **GX9 naming/grep:** enforce construction-manifest symbols and forbidden-token ban on the fix path.
- **GX10 packaging:** exclude solution, tests, reviewer material, and caches from the image and zip.
- **Static checks:** anonymous author fields, version 2.0 task.toml, `.dockerignore` present; CM-007 verifier triad; CM-001 python/asciinema hygiene.
- **WW-010 schema citation:** instruction.md must cite `/app/docs/ember-report-schema.md` for graded keys.
- **ADR-0014 / CM-011:** agent-facing languages stay C++ and Rust; pytest is verifier-only and must not appear in agent language metadata.

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
- `environment/docs/ember-report-schema.md`
- `environment/docs/data-format.md`
- `environment/data/families.case`
- `environment/fixtures/logs/run_trace.ndjson`
- `environment/fixtures/prompts/short_a.bin`
- `environment/fixtures/prompts/long_a.bin`
- `environment/fixtures/export/bundle.bin`
- `environment/native/reed.cpp`
- `environment/native/bract.cpp`
- `environment/native/ember.cpp`
- `environment/native/include/reed.h`
- `environment/native/include/common.h`
- `environment/host/main.rs`
- `environment/host/silt.rs`
- `environment/host/weld.rs`
- `environment/host/loam.rs`
- `environment/host/seam.rs`
- `environment/host/relay.rs`
- `environment/host/ffi.rs`
- `environment/host/report.rs`
- `environment/host/error.rs`
- `environment/host/config.rs`
- `environment/probe/sample.cpp`
- `environment/probe/include/sample.h`
- `environment/tools/build_all.sh`
- `environment/tools/run_kiln.sh`
- `tests/test.sh`
- `tests/test_outputs.py`
- `solution/solve.sh`
- `construction_manifest.json`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: native/reed.cpp
  symbol: plait_m
  kind: function
  signature: int32_t plait_m(const uint8_t* a, size_t b, uint64_t* c);
  purpose: Binds exported tensor bytes into runtime working buffers under the active packing context.

- path: host/silt.rs
  symbol: latch_y
  kind: function
  signature: pub(crate) fn latch_y(a: u64, b: &mut Slate) -> i8
  purpose: Writes and reads incremental generation working-set slots under the active index context.

- path: host/weld.rs
  symbol: pivot_z
  kind: function
  signature: pub(crate) fn pivot_z(a: u64, b: &mut Phase) -> i8
  purpose: Applies sequence-index offsets during generation under the active phase context.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: native/reed.cpp
    controls_tests: [test_e01, test_e02, test_e06, test_e10]
  - id: B
    path: host/silt.rs
    controls_tests: [test_e03, test_e05, test_e07, test_e11]
  - id: C
    path: host/weld.rs
    controls_tests: [test_e04, test_e08, test_e09, test_e12]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: native/bract.cpp
  kind: helper
  rhymes_with: plait_m
  non_fix_purpose: Counts export banner fields for diagnostic lines without binding tensors.

- path: host/loam.rs
  kind: helper
  rhymes_with: latch_y
  non_fix_purpose: Maps display codes for status lines without changing working-set slots.

- path: host/seam.rs
  kind: helper
  rhymes_with: pivot_z
  non_fix_purpose: Formats phase labels for logs without applying sequence-index offsets.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: ["app", "architecture", "bin", "breaking", "bundled", "cache-hit", "checks", "compiled", "controls", "correct", "counters", "decode", "diverge", "docs", "ember-report-schema", "ember_report", "emit", "export", "exported", "fixed", "follow", "golden", "greedy", "hand", "healthy", "inventing", "invoke", "json", "keys", "kiln", "lab", "latency", "layout", "loads", "long-prompt", "longer", "match", "md", "model", "new", "normative", "offline", "output", "pass", "pipeline", "prompts", "rebuild", "regenerate", "remain", "replace", "report", "runs", "schema", "sequences", "short", "short-prompt", "summaries", "token", "training-side", "unchanged", "weights", "write"]
```
