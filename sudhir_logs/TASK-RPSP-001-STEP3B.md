# TASK-RPSP-001 Step 3b Log

## 2026-07-18 - Paper review

- Phase: Step 3b structural, collapse, and feasibility review
- Starting registry state: an automated package/approval run had advanced the task before Step 3b and Step 4 oracle stress
- Lifecycle correction:
  - opened registry revision 3;
  - removed the premature final zip;
  - reran current cheap gates;
  - returned the task to review phase.
- Independent adversarial review found:
  - exact `mapped == 0` verifier lock on the refinement sentinel;
  - lex-least-even canonical row lock despite a broader public parity contract;
  - implementation-specific `nm` symbol policing;
  - no direct coverage that all nine bundled batches remain present;
  - cause-adjacent reusable-state wording in architecture documentation.
- Unsupported external finding rejected: review policy files belong at repository root and are inputs to review; they must not be copied into the task directory.
- Revision 4 corrections:
  - accepted any distinct refinement sentinel when refinement is preserved;
  - compared geometric cell identity independently of row representation;
  - rebuilt adjacency and topology expectations from emitted positive rows;
  - removed the binary symbol-table assertion;
  - exercised all three bundled families and all nine named variants;
  - removed reusable-state cause wording from the architecture document.
- One test-drafting slip was found immediately: bundled variant names were assumed uniform. Replaced them with each family's actual names before final gates.
- Multi-approach proof: an always-refine C path, alternate Rust sentinel, and lex-greatest-even Fortran canonicalization passed all twelve revised tests.
- Dynamic concentration proof: A, B, C, and D still fail exactly their declared four tests under one-location ablation.
- Current preflight: static PASS, Dockerfile PASS, collapse 23/23 PASS, packaging preview PASS, checksum current.
- Current Harbor evidence:
  - oracle `jobs/2026-07-18__23-21-05/result.json`: mean 1.0, zero errors;
  - NOP `jobs/2026-07-18__23-22-00/result.json`: mean 0.0, zero errors.
- Docker infrastructure note: compose teardown permission denial repeated after completed Harbor trials; internal process cleanup left no stale task containers.
- Final repository certification: Ruff PASS, pytest 240 passed and 26 skipped, task checksum current, 157-archive index current, no final zip, no stale task container, whitespace PASS.
- Final review evidence: `sudhir_reviews/robust-predicate-scale-parity/STEP3B.md`.
- Next action: Step 4 oracle 10x, final NOP, packaging, validation, and approval.
