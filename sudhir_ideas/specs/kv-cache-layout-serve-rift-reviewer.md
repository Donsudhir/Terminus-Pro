### Decision
GO — Attempt 3. Distributed three-location short/long greedy-serve topology across C++ and Rust (`native/`, `host/`); symptoms-only instruction; 0 FAIL / 0 WARN after schema fix on attempts 1–2.

### Metadata
- Task name: kv-cache-layout-serve-rift
- Title: KV Cache Layout Serve Rift
- Category: machine-learning
- Languages: [c++, rust]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [inference, kv-cache, positional-encoding, token-decode, model-serving]
- Milestones: 0

### Investigation profile
The primary weakness area is long-horizon debugging, reinforced by multi-component reasoning, partial failures, and misleading documentation. The task is one offline serve incident: short prompts and cache-hit/latency summaries can look healthy while longer greedy sequences diverge from goldens.

1. Run short and long families. Short-green / long-wrong concentrates after generation extends past short lengths.
2. Correlate logs, metrics, and ember_report fields. Disagreement tracks long-sequence fields rather than export-check banners.
3. Trace exported-weight binding in native code. Packing stride disagrees with the runtime contract.
4. Probe host working-set write/read indices across length thresholds. Slot stride is wrong while cache-hit counters stay plausible.
5. Inspect serve-time sequence-index offset intermediates. Offsets diverge past a length threshold.
6. Repair all three authorities, rebuild, and verify short/long matrices end-to-end.

Evidence surfaces are code (`native/`, `host/`), runtime-state (`/app/bin/kiln` short/long runs), logs (`fixtures/logs/run_trace.ndjson`), metrics (cache-hit/latency counters in `ember_report.json`), and filesystem (prompt/export artifacts). Competing hypotheses include tokenizer truncation, cache-hit/latency-as-failure, and numeric noise; each has a deterministic falsifier. The conditional matrix includes failing long families / generated variants plus healthy short controls and non-decisive cache-hit bait. The estimate is 46 meaningful actions. All sources and fixtures are fixed and offline.

### Discovery budget
- Discovery: Exported weight tensors are bound with a packing stride that short prompts can tolerate while longer prompts diverge.
  Planned location: environment/native/reed.cpp::plait_m
  Why instruction must not reveal it: Naming export packing stride would collapse the C++ diagnosis into a disclosed tensor-layout recipe.
- Discovery: Incremental generation working-set slots use a wrong index stride while cache-hit counters can still look plausible.
  Planned location: environment/host/silt.rs::latch_y
  Why instruction must not reveal it: Naming KV-cache slot stride would directly expose the Rust repair.
- Discovery: Serve-time sequence-index offsets diverge past a length threshold.
  Planned location: environment/host/weld.rs::pivot_z
  Why instruction must not reveal it: Naming positional/RoPE phase policy would reduce the third repair to a disclosed encoding flip.

### Anti-trivialization verdict
| Check | Verdict | Reviewer basis |
| --- | --- | --- |
| Disclosure-collapse | PASS | Honest short/long outcomes and schema citation do not reveal the three inconsistent authorities. |
| Hidden-instance | PASS | Bundled, generated, and short-control scenarios require a general repair. |
| Single-artifact repair | PASS | Three roots and regenerated short/long matrices prevent artifact replacement. |
| Generalization | PASS | Generated length variants extend beyond the bundled incident. |
| Prompt-honesty | PASS | Invocation, schema path, short/long outcomes, and hardcoding bans are documented. |
| Cheating-vs-difficulty | PASS | Anti-hardcoding protects tests; cross-language serve diagnosis creates difficulty. |
| Mechanical-fix filter | PASS | No dependency, timeout, reward, or metadata repair is the task. |
| Localized-fix | PASS | Three distinct roots each control 4/12 tests. |
| Oracle-locality | PASS | Planned semantic delta is substantive across three functions, not one short rewrite. |
| Small declarative-cluster | PASS | Report schema documents keys only; it does not contain the behavioral solution. |
| Grep-collapse | PASS | Complete noun provenance has no selected path, symbol, parameter, or test hit. |
| Pre-factored-helper | PASS | Opaque names, plausible baseline bodies, and decoys avoid stub completion. |
| Recipe-discount | PASS | Tokenizer, prefix-cache, or short-prompt retune recipes leave binding/slot/offset defects. |
| Security-aura discount | PASS | ML serve correctness remains after removing any security framing. |
| Orthogonal-checklist | PASS | Long goldens, short controls, and non-decisive bait are one coupled invariant. |
| Harness-discount | PASS | Deterministic Docker and fixtures provide reproducibility only. |
| One-pass solvability | PASS | Obvious entrypoints do not expose all three authorities or their coupling. |
| Hard-only gate | PASS | Professional mixed-language serve-layout diagnosis and three-boundary coordination remain. |
| Discovery budget test | PASS | Three non-trivial discoveries have concrete homes and disclosure reasons. |
| Instruction specificity test | PASS | Symptoms-only; schema is public contract; causes remain hidden. |
| Topology distribution test | PASS | Three ≥3-location topologies are viable and no one location suffices. |

### Topology enumeration (3 candidate fix topologies)
1. **topology_a_selected** — `native/reed.cpp::plait_m`, `host/silt.rs::latch_y`, `host/weld.rs::pivot_z`. No single location suffices because binding, slot, and offset failures are independently observable on short/long matrices.
2. **topology_b_lifecycle_chain** — `native/reed.cpp::plait_m`, `host/silt.rs::latch_y`, `host/weld.rs::pivot_z`, `host/relay.rs::swing_u`. Correct bind fails without slot write/read agreement; correct buffers fail under wrong offsets.
3. **topology_c_authority_map** — `native/reed.cpp::plait_m`, `host/silt.rs::latch_y`, `host/weld.rs::pivot_z`. Packing, slot keys, and sequence offsets must agree end-to-end after short-to-long generation.

### Rubric axes
- **Verifiable — PASS:** long goldens, short controls, regenerated reports are machine-checkable.
- **Well-specified — PASS:** symptoms, invocation, schema citation, and prohibited hardcoding are clear.
- **Solvable — PASS:** bounded existing pipeline; expert hours, not research years.
- **Difficult — PASS:** hard after honest disclosure; causes not named.
- **Interesting — PASS:** real offline serve engineering value in ML inference.
- **Outcome-verified — PASS:** any correct implementation accepted.

### Hardness axes
- **Discover — PASS:** three hidden facts must be recovered from code/runtime.
- **Synthesize — PASS:** two languages and three authorities.
- **Diagnose — PASS:** symptoms-only instruction.
- **Navigate coupling — PASS:** subset fixes leave other short/long properties red.
- **Reason beyond training — PASS:** not a tokenizer/prefix-cache textbook recipe.

### Instruction completeness / specificity
Instruction completeness PASS. Specificity level: symptoms-only.

### Collapse audit
PASS. Residual hardness is identifying which of three authorities explains short-green / long-wrong decode with healthy cache-hit bait, then coordinating all three repairs.

### CM-010 independent review (schema-PASS is insufficient)
- Absorb A into B/C from signatures alone? No — binding, slot, and offset failures remain separable on the test matrix.
- Skip any causal stage? No — later stages depend on earlier short/long characterization and boundary correlation.
- Every scored assertion has a solver-visible contract home in the public short/long + schema citation? Yes.
- Re-extracted nouns from the public contract match `code_forbidden_tokens`? Yes (62 tokens).

### Public contract noun list (authoring provenance)
["app", "architecture", "bin", "breaking", "bundled", "cache-hit", "checks", "compiled", "controls", "correct", "counters", "decode", "diverge", "docs", "ember-report-schema", "ember_report", "emit", "export", "exported", "fixed", "follow", "golden", "greedy", "hand", "healthy", "inventing", "invoke", "json", "keys", "kiln", "lab", "latency", "layout", "loads", "long-prompt", "longer", "match", "md", "model", "new", "normative", "offline", "output", "pass", "pipeline", "prompts", "rebuild", "regenerate", "remain", "replace", "report", "runs", "schema", "sequences", "short", "short-prompt", "summaries", "token", "training-side", "unchanged", "weights", "write"]
