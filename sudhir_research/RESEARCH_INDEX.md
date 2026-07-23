# Research Index

## Research policy

- Official documentation, papers, and reproducible local behavior are primary evidence.
- GitHub issues, discussions, Reddit, X, Discord, videos, and blog posts are community signals until corroborated.
- Every stored claim records retrieval date, source, confidence, and implication.
- Do not store credentials, private messages, or browser cookies.

## Terminal-Bench and Harbor baseline

| Date | Source | Claim | Confidence | Implication |
| --- | --- | --- | --- | --- |
| 2026-07-18 | https://www.tbench.ai/ | Terminal-Bench 3.0 and Terminal-Bench Science are in development; difficult scientific tasks are a current project direction | High | Robust scientific computing is timely and category-aligned |
| 2026-07-18 | https://arxiv.org/abs/2601.11868 | The benchmark targets hard, realistic terminal tasks with unique environments, human solutions, and comprehensive tests | High | Task realism and independent verification matter more than mathematical prestige |
| 2026-07-18 | https://github.com/harbor-framework/terminal-bench | Tasks contain an instruction, verifier, and oracle and run through a sandboxed execution harness | High | Preserve standard artifact roles while extending local workflow |
| 2026-07-18 | https://harborframework.com/docs | Harbor exists because managing container tasks at scale is difficult and emphasizes modular tasks, agents, environments, and reproducible jobs | High | Repository governance and path adapters should integrate with Harbor rather than replace it |

## Mathematical sources for TASK-RPSP-001

| Date | Source | Claim | Confidence | Implication |
| --- | --- | --- | --- | --- |
| 2026-07-18 | https://www.cs.cmu.edu/~quake/robust.html | Near-zero determinant predicates can return wrong signs in ordinary floating point; adaptive exact methods do only enough work to certify the sign | High | Exact sign and topology invariants provide strong deterministic verification |
| 2026-07-18 | https://doi.org/10.1017/S096249291000005X | Rigorous numerical verification can use floating-point arithmetic when rounding and error bounds are controlled | High | Cross-language floating-point semantics can create legitimate, proof-like hardness |
| 2026-07-18 | https://bebop.cs.berkeley.edu/reproblas/ | Floating-point reductions depend on ordering, partition, SIMD choice, alignment, and reduction tree unless reproducibility is designed explicitly | High | Metamorphic execution configurations are useful anti-shallow verification patterns |

## Mathematical sources for TASK-SJCC-001

| Date | Source | Claim | Confidence | Implication |
| --- | --- | --- | --- | --- |
| 2026-07-19 | https://doi.org/10.1093/imamat/13.1.117 | Sparse Jacobians can be estimated with few residual evaluations by grouping structurally orthogonal columns (CPR) | High | Compression/unpack correctness is a scientific invariant |
| 2026-07-19 | https://doi.org/10.1137/0720013 | Structurally orthogonal partitions are a graph coloring problem; symmetry assumptions are unsafe on unsymmetric patterns | High | Unsafe symmetry in the partitioner is a legitimate seeded defect |
| 2026-07-19 | https://doi.org/10.1137/s0036144504444711 | Distance-1/2 coloring unifies Jacobian estimation; wrong partitions yield plausible but wrong sparse matrices | High | Metamorphic `J` / `J·v` parity is a strong verifier surface |
| 2026-07-19 | https://doi.org/10.1145/1271.1610 | Production software separates partition determination from finite-difference estimation; stale plans reuse wrong seeds | High | Plan lifecycle and seed hygiene are cross-module defects |

Full uniqueness dossier: `sudhir_research/TASK-SJCC-001-RESEARCH.md`.

## Security sources for TASK-ERS-001

| Date | Source | Claim | Confidence | Implication |
| --- | --- | --- | --- | --- |
| 2026-07-19 | https://www.rfc-editor.org/rfc/rfc5116 | AEAD associated data is authenticated and must match at decrypt time | High | Stale generation metadata can deterministically invalidate otherwise intact wrapped records; accepting alternate metadata would weaken binding |
| 2026-07-19 | https://www.rfc-editor.org/rfc/rfc5869 | HKDF `info` provides application context separation | High | Truncating distinct scope names into one derivation context is a real cross-scope isolation failure |
| 2026-07-19 | https://cloud.google.com/kms/docs/envelope-encryption | Envelope encryption separates data keys from the key-encryption key and supports re-wrapping | High | Rotation can repair wrapped-key lineage without re-encrypting every payload |
| 2026-07-19 | https://github.com/harbor-framework/terminal-bench-3/pull/1127 | `crash-safe-vault` is the nearest public task and implements a specified single-module crash protocol | High | ERS remains distinct: forensic recovery after a completed multi-module mutation, strict forgery rejection, and idempotent re-rotation |

Full uniqueness dossier: `sudhir_research/TASK-ERS-001-RESEARCH.md`.

## Dependency-resolution sources for TASK-RCD-001

| Date | Source | Claim | Confidence | Implication |
| --- | --- | --- | --- | --- |
| 2026-07-19 | https://peps.python.org/pep-0440/ | Pre-release ordering and eligibility are separate policy concerns | High | Candidate ranking can conflict with fallback eligibility after independently correct changes merge |
| 2026-07-19 | https://peps.python.org/pep-0592/ | Yanked releases remain available for some pinned cases but should be avoided for ordinary new resolution | High | Yank fallback has a real semantic seam with pre-release selection |
| 2026-07-19 | https://peps.python.org/pep-0665/ | Lockfiles exist to make dependency choices reproducible | Medium-high (PEP withdrawn; analysis still applicable) | Canonical serialization is a behavioral supply-chain invariant, not formatting trivia |
| 2026-07-19 | https://github.com/alibaba/terminal-bench-pro/blob/main/implement-depgraph-dependency-resolver/instruction.md | The nearest public task is a spec-complete blank-canvas resolver implementation | High | RCD remains distinct: existing-system history archaeology and preservation of two merged feature contracts |

Full uniqueness dossier: `sudhir_research/TASK-RCD-001-RESEARCH.md`.

## Columnar storage sources for TASK-RPM-001

| Date | Source | Claim | Confidence | Implication |
| --- | --- | --- | --- | --- |
| 2026-07-19 | https://parquet.apache.org/docs/file-format/nulls/ | Parquet encodes nullity separately in definition levels and omits null values from the data plane | High | Validity and value bytes are distinct authorities; sentinel-shaped legitimate values cannot be treated as null after an explicit-validity migration |
| 2026-07-19 | https://parquet.apache.org/docs/file-format/pageindex/ | Per-page min/max metadata permits readers to skip pages for selective scans | High | Persisted bounds become correctness-bearing when the planner uses them to avoid reads |
| 2026-07-19 | https://orc.apache.org/specification/ORCv1/ | ORC combines PRESENT streams, row-group statistics including `hasNull`, dictionary encodings, and predicate pushdown | High | A producer, planner, and scan kernel must agree on validity, ordering, and page-local encoding semantics |

Full uniqueness dossier: `sudhir_research/TASK-RPM-001-RESEARCH.md`.

## Community research queue

Recent social and community research is not yet captured. It requires a separate consented setup if browser-authenticated sources are used. The first pass will prioritize public GitHub issues and discussions, official Discord guidance when accessible, task-contribution feedback, common rejection reasons, reproducibility pain points, and what task authors report as the largest time sinks.
- `TASK-MCOS-001-RESEARCH.md` — mesh-checkpoint-operator-skew uniqueness (2026-07-23)
- `TASK-DNMH-001-RESEARCH.md` — device-node-migration-haze uniqueness (2026-07-23)
- `TASK-IRPD-001-RESEARCH.md` — input-ring-physics-desync uniqueness (2026-07-23)
- `TASK-KCLS-001-RESEARCH.md` — kv-cache-layout-serve-rift uniqueness (2026-07-23)
- `TASK-ACPR-001-RESEARCH.md` — amg-coarsen-parity-rift uniqueness (2026-07-23)
- `TASK-DHDR-001-RESEARCH.md` — domain-halo-digest-rift uniqueness (2026-07-23)
