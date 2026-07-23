## Platform difficulty — REV-4 upload remeasure

Difficulty: ❌ EASY - Requires at least MEDIUM

Status: ✅ Solvable (all tests passed by at least one agent run)

Agent Performance:
  • terminus-claude-opus-4-8: 80.0% (4/5 runs)
  • terminus-gpt5-5: 100.0% (5/5 runs)

Reference Agents:
  • nop: 0.0% (0/1 runs)
  • oracle: 100.0% (3/3 runs)

Failure Breakdown:
  • nop: 1 other
  • terminus-claude-opus-4-8: 1 other

Unit Tests Results:
  • test_r01–r04,r07,r08,r12: 10/10
  • test_r05,r06,r09,r10,r11: 9/10

Task Instruction Sufficiency: ❌ FAIL
- Agent patched sill.rs Mixed admission but missed lock ascending bytewise order.
- Sort reads as format contract, not a second defect; smoke tests with alder/birch/cedar/elm mask unsorted writer because catalog/serial order is already lex-sorted.
- Do NOT fix by naming “lock writer has a sort bug” (that worsens EASY). Harden so sill-only + accidental lex order cannot pass.
