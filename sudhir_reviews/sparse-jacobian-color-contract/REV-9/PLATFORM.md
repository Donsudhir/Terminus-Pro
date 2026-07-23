# Platform snapshot (sanitized)

Captured: 2026-07-23T13:16:08Z

## Scalars
- difficulty: TRIVIAL
- solvable: True
- status_line: ✅ Solvable (all tests passed by at least one agent run)
- static_outcome: PASS
- submission_id: d9082cd8-c0ad-4174-a34f-4731f0b63907
- zip_filename: sparse-jacobian-color-contract.zip
- uploaded_at: 2026-07-22T19:35:52.263Z
- source_file: submission_d9082cd8.json

## Agent performance
- terminus-claude-opus-4-8: 100.0%
- terminus-gpt5-5: 100.0%

## text_summary

```
Difficulty: ❌ TRIVIAL - Requires at least MEDIUM

Status: ✅ Solvable (all tests passed by at least one agent run)

Agent Performance:
  • terminus-claude-opus-4-8: 100.0% (5/5 runs)
  • terminus-gpt5-5: 100.0% (5/5 runs)

Reference Agents:
  • nop: 0.0% (0/1 runs)
  • oracle: 100.0% (3/3 runs)

Failure Breakdown:
  • nop: 1 other

Unit Tests Results:
  • test_k01: 10 passed / 10 runs
  • test_k02: 10 passed / 10 runs
  • test_k03: 10 passed / 10 runs
  • test_k04: 10 passed / 10 runs
  • test_k05: 10 passed / 10 runs
  • test_k06: 10 passed / 10 runs
  • test_k07: 10 passed / 10 runs
  • test_k08: 10 passed / 10 runs
  • test_k09: 10 passed / 10 runs
  • test_k10: 10 passed / 10 runs
  • test_k11: 10 passed / 10 runs
  • test_k12: 10 passed / 10 runs
  • test_k13: 10 passed / 10 runs
  • test_k14: 10 passed / 10 runs

Analysis on Agent Failures:
  • Task Instruction Sufficiency: ➖ NOT_APPLICABLE, debug output not available
```

## test_rubrics (from platform export)

```
Agent rebuilds and runs /app/bin/senslab so /app/output/sensitivity_report.json is emitted by the compiled pipeline with schema_version runs and digest, +3
Agent repairs conflict-valid probe grouping so ledger.groups matches the nonzero conflict structure, +5
Agent clears resume seed carry so cold and resumed evaluations agree on packed values and indices, +3
Agent restores per-batch Euclidean residual magnitude for span_info.ref and derives step from that same batch with the disclosed residual-scaled formula including runtime.conf step knobs, +5
Agent preserves unpack orientation and matches packed values to operator first-order response after native residual tinting, +5
Agent drives directional products from the disclosed bundled companion directions and keeps scale-equivalent tags agreeing, +3
Agent keeps runs lexicographically ordered by family then tag with byte-identical clean rebuilds, +2
Agent leaves malformed input exiting nonzero without a partial report, +2
Agent hand-writes the sensitivity report or bypasses the compiled senslab pipeline, -5
Agent invents probe direction vectors or quantizes the finite-difference step instead of using the disclosed residual-scaled contract, -3
Agent edits verifier tests, shadows pytest, or forces reward without repairing the pipeline, -5
Agent patches only one authority and leaves permute, resume, scale, or tint disagreement, -3
```

