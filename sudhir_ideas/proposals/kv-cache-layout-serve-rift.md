# Task Idea Proposal — kv-cache-layout-serve-rift

Generated: 2026-07-22T21:16:44Z
Platform check: PASSED
Evidence: chat-2026-07-23 Snorkel Task Idea Proposal Check feedback pasted by Sudhir

## Paste-ready fields

### Task Idea Summary

An offline inference stack loads exported weights and serves greedy decode for fixed prompts. Training-side export checks pass and short prompts match golden token sequences, but longer prompts diverge while cache-hit counters and latency summaries still look healthy. Short-prompt controls must remain unchanged. Make long-prompt decode match the golden sequences without breaking short controls or inventing a new model architecture.

### Idea Category

Machine Learning / Model Training / Inference

Normalized local category: `machine-learning`

### Associated Skills

transformer inference, KV cache layout, positional encoding at serve time, weight export/load contracts, C++ or Rust runtime debugging, token-sequence verification, numerical layout diagnosis

### Task Tags

inference, kv-cache, positional-encoding, token-decode, model-serving

## Check feedback

Similarity PASS. Idea quality PASS (Decision: Accept; Verifiable: Accept; Well-specified: Uncertain; Solvable: Accept; Difficult: Accept; Interesting: Accept; Outcome-verified: Accept). Category alignment FAIL (selected machine_learning; suggested debugging) — non-blocking. Metadata similarity PASS.

## Inspiration provenance

- Source type: ML serving incident pattern
- Source reference: long-prompt KV/layout serve divergence vs short-prompt control (inspiration only; distinct from train-serve token rift; 2026-07-23)
- Reuse boundary: Inspired by short-prompt-green / long-prompt-wrong serve behavior; no model weights, papers, or benchmark harnesses copied.
