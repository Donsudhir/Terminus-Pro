# TASK-KCLS-001 — kv-cache-layout-serve-rift — Super-Uniqueness Dossier

- Idea: `kv-cache-layout-serve-rift` (IDEA-0035)
- Category: machine-learning
- Archetype: long-horizon investigation — offline greedy serve where short-prompt golden tokens and cache-hit/latency summaries stay healthy while long-prompt decode diverges due to KV-cache / positional layout contracts
- Research date: 2026-07-23
- Verdict: **no semantic collision found** across all six required scopes

## Novelty fingerprint (four parts)

1. **Domain/system:** an offline transformer inference / serve stack that loads exported weights and runs greedy decode for fixed prompts, with KV cache, positional encoding at serve time, and short/long prompt controls.
2. **Failure mechanism:** training-side export checks pass and short prompts match golden token sequences, but longer prompts diverge while cache-hit counters and latency summaries still look healthy.
3. **Distributed fix topology:** weight load / layout binding, KV-cache write/read indexing, and serve-time positional encoding must coordinate. Inventing a new architecture or only retuning short prompts is rejected.
4. **Verifier/invariant surface:** long-prompt greedy sequences match goldens; short-prompt controls remain unchanged; cache-hit/latency bait is not success.

## Collision audit — all six scopes

### 1. Idea registry

Scanned `sudhir_progress/registry.json` / `IDEA_INDEX.md` on 2026-07-23.

ML neighbours:

- `tokenizer-serving-rift` / train-serve token rift (IDEA-0016) — documentation-falsification about tokenizer/normalization/truncation vs training artifacts; not KV-cache layout or length-gated decode divergence.
- `feature-skew-horizon` (IDEA-0024) — temporal leakage in feature stores; different ontology.
- Same-batch scientific/mesh ideas are unrelated.

Differentiation vs train-serve / tokenizer-serving: KCLS grades **numerical layout / KV + positional contracts at serve** under **short-green / long-wrong** metamorphic length, not “model card lies about preprocessing.” **No collision.**

### 2. Active tasks

`sudhir_tasks/active/`: no ML inference / KV-cache / tokenizer-serving task. **No collision.**

### 3. Archived tasks / submission archives

`sudhir_tasks/archived/` empty. Content-scanned submission zips (2026-07-23):

- Strict `kv.?cache|positional.?encod|RoPE|attention.?cache`: **0 hits**.
- Name/content neighbour `transformer-inference-latency.zip` mentions `kv_cache_hits` as an **SLO/performance** metric (int8 FFN / arena reuse / RSS), not golden long-prompt token-sequence correctness under layout drift. ANN scheduler zips use unrelated `cache_hit` ranking fields.

**No semantic collision** with KCLS’s short/long golden decode contract.

### 4. Upstream corpus

Local `tasks/` and prior TB research notes contain no Terminal-Bench public task whose core is KV-cache / positional layout causing long-prompt greedy divergence with short-prompt controls. **No collision.**

### 5. Current external research

Searches performed 2026-07-23:

- `Terminal-Bench KV cache layout inference long prompt decode divergence serve`
- vLLM / serving literature on prefix caching and KV layout (inspiration only)

External systems discuss real KV reuse and layout hazards. No public Terminal-Bench task instance, patch, or test suite matching this short/long golden-token contract was adopted. Inspiration boundary: symptom shape only. **No benchmark collision.**

### 6. Structural-neighbour check

Nearest engineering analogue is a serve runtime where short contexts hide a wrong KV stride or positional binding that only appears past a length threshold, while cache-hit counters remain plausible. “Enable prefix caching” or “fix the tokenizer” recipes do not match this distributed layout + length-metamorphic verifier.

## Closest analogue and structural difference

- **Closest analogue:** captured `tokenizer-serving-rift` (IDEA-0016, train-serve token rift); archive neighbour `transformer-inference-latency` is SLO/perf only.
- **Structural difference:** this idea’s core is **KV-cache / positional layout correctness** judged by **long-prompt golden greedy sequences** with **short-prompt controls** and **healthy cache-hit bait** — not tokenizer/normalization documentation falsification, and not latency/SLO repair.

## Result

Uniqueness PASS for `kv-cache-layout-serve-rift`. Do not start Step 2a in this session.
