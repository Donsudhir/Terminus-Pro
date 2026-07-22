# REV-3 reviewer feedback — sparse-jacobian-color-contract

Difficulty: EASY - Requires at least MEDIUM
Status: Solvable
Agent Performance:
  - terminus-claude-opus-4-8: 100.0% (5/5 runs)
  - terminus-gpt5-5: 80.0% (4/5 runs)
Reference: nop 0%, oracle 100%
Unit tests: k05/k10/k11 now 10/10 after REV-2 gauge contracts; residual misses on k01/k02/k04/k07/k08 (9/10)
Instruction sufficiency FAIL: packed values must equal structural residual coefficients not stated (only directional probes)
AutoEval FAILED banner treated as CM-004 noise.
