# envelope-rotation-shear Edit Ledger

## 2026-07-19T13:49:33Z — Revision 1

- evidence capture

## 2026-07-19T16:49:51Z — Revision 2

- Snorkel Needs Revision: rubric format/severity, reward initial write, golang apt pin, instruction grading contracts

## 2026-07-19T18:12:46Z — Revision 3

- Platform difficulty MEDIUM because task metadata included Python despite a Go-only agent-facing core; agent analysis also found an instruction-sufficiency gap around preserving namespace-consistent generated reads while rejecting substitutions.

## 2026-07-21T00:59:54Z — Revision 4

- Instruction-sufficiency FAIL on axis/namespace binding for generated live reads vs substitution rejection; clarify observable contract without naming internals. Also capture tb_check FAILED vs difficulty SUCCEEDED.

## 2026-07-21T — Revision 4

- Instruction-sufficiency: public-service namespace-binding polarity for generated reads vs substitutions; maintain skip rewrite of active matching-service records
