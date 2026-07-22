# REV-3 reviewer feedback — envelope-rotation-shear

Platform difficulty feedback:

Difficulty: ❌ MEDIUM - Requires at least HARD for python

Status: ✅ Solvable (all tests passed by at least one agent run)

Agent Performance:
  • terminus-claude-opus-4-8: 80.0% (4/5 runs)
  • terminus-gpt5-5: 60.0% (3/5 runs)

Reference Agents:
  • nop: 0.0% (0/1 runs)
  • oracle: 100.0% (3/3 runs)

Failure Breakdown:
  • nop: 1 other
  • terminus-claude-opus-4-8: 1 other
  • terminus-gpt5-5: 2 other

Unit Tests Results:
  • test_e01: 10 passed / 10 runs
  • test_e02: 8 passed / 10 runs
  • test_e03: 10 passed / 10 runs
  • test_e04: 10 passed / 10 runs
  • test_e05: 10 passed / 10 runs
  • test_e06: 8 passed / 10 runs
  • test_e07: 10 passed / 10 runs
  • test_e08: 9 passed / 10 runs
  • test_e09: 10 passed / 10 runs
  • test_e10: 8 passed / 10 runs
  • test_e11: 10 passed / 10 runs
  • test_e12: 8 passed / 10 runs

Analysis on Agent Failures:
  • Task Instruction Sufficiency: ❌ FAIL

Job Summary: Vault System Repair (3 Trials)

0/3 trials passed. All failures traced to the same root bug: agents over-aggressively removed the derived-scope fallback branch in aperture/open.go openSet. That branch was dual-purpose: it enabled cross-namespace substitution and legitimate reads for freshly provisioned namespaces where crypto.SealAt and tenant.ScopeFor produce different scopes for non-cached entries. The correct fix preserves fallback only when frame.Axis == AxisFor(frame.Item), while blocking it otherwise.

No cheating was detected. The task specification was judged partially insufficient because it described authentication failures and cross-namespace leaks but did not make the healthy generated-namespace read invariant clear enough. The best run reached 11/12, while the others reached 8/12. The recommendation was to clarify that namespace-consistent derived-scope behavior must remain available while substituted identities are rejected.

User directive: do not classify or design this as a Python task. Python is verifier-only; the agent-facing implementation is Go.
