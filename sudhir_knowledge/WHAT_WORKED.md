# What Worked

Short success checklist. Load after `COMMON_MISTAKES.md` at chat start.
Promote durable wins here when a revision or acceptance proves a pattern.

| ID | Status | Pattern | When to reuse | Evidence |
| --- | --- | --- | --- | --- |
| WW-001 | active | Exact flipping-point ablations (each fix location fails a declared test subset) | Distributed scientific / multi-root tasks | PATTERN-ABLATION-001; RPSP / SJCC |
| WW-002 | active | Outcome-based tests (cell identity, adjacency, digest) not representation locks | Geometry / report pipelines | PATTERN-REPRESENTATION-001; RPSP rev4 |
| WW-003 | active | Prove a second valid implementation during paper review | Before claiming verifier is not oracle-locked | PATTERN-ALTERNATIVE-001 |
| WW-004 | active | CM-007 one-liner on verifier command: `cd /tests && PYTHONSAFEPATH=1 python -m pytest … --confcutdir=/tests` | Any pytest verifier with agent-writable WORKDIR | CM-007 prevented; RPSP rev6 |
| WW-005 | active | Output/artifact rubric lines (report fields, fail-closed, digests) over process diary | Platform form rubric | RPSP reviewer note 2026-07-19 |
| WW-009 | active | UI rubric paste format: each line `Agent <behavior>, <score>`; score last; ≥3 negatives; ±5/±3/±1–2 severity tiers; positives sum 10–40 | Every Snorkel form rubric field | `TASK_PROPOSAL_RUBRIC.md`; CM-015; ERS REV-2; see cluster-green / SJCC REV-2 exemplars |
| WW-006 | active | Store every form paste in `REV-<n>/` (DIFFICULTY, SOLUTION, VERIFICATION, RUBRIC) before upload | Every submission | ADR-0012 `form-capture` |
| WW-007 | active | Keep an additive evidence schema readable, but stamp new loop state with a contract version that activates new required semantics | Authoring-contract rollouts that must grandfather in-flight evidence | ADR-0013; v3 profile tests; full regression 266 passed |
| WW-008 | active | Agent-facing stack in niche languages (≥2 when needed); never Python-primary | New ideas / construction language choice | ADR-0014; CM-011 |
| WW-010 | active | Normative `environment/docs/*-schema.md` cited from `instruction.md` for every graded JSON key + exact output filename | Any task whose tests parse structured reports or named artifacts | CM-018; maritime/plc/cluster QC PASS; RPM REV-3 plan |
| WW-011 | active | Gate live eligibility before uniqueness/Step 2a/construction; allow later blocks only with source-backed review/revision exemption evidence | Every new idea and every in-flight blocked-category/milestone revision | ADR-0016; Slice 4; RPM `fac356b4` exemption |
| WW-012 | active | Keep platform-recognized structure valid while expressing stricter repository policy as a separate house verdict; require current compatibility checks for exemptions | House-blocked subtypes such as net-new UI with evidence-backed in-flight revisions | ADR-0017; Slice 6; pytest + Playwright Python fixture |
| WW-013 | active | Generate the four Task Idea Proposal fields first, stop for platform Check feedback, then gate uniqueness/Step 2a on captured PASS | Every newly selected task candidate | Snorkel proposal-form screenshots 2026-07-21; `idea proposal`; proposal board column |
| WW-014 | active | Resolve all current writes through one canonical root adapter; keep historical corpora independently indexed and read-only; update generated views with one digest and rollback | Repository root migrations, package/index transactions, generated status | ADR-0019; Slice 7; CM-023 prevented |
| WW-015 | active | Give every official CI check one explicit disposition; enforce deterministic checks locally and name unpublished semantic checks as delegated instead of inventing PASS | CI parity, approval gates, future policy changes | ADR-0020; Slice 8; official coverage matrix |
| WW-017 | active | Document exact digest/hash payload boundaries (closed object vs open prefix) in a cited normative env doc; keep verifier identical to the shipped renderer | Any report digest / checksum contract; especially after instruction-sufficiency near-misses | CM-024; SJCC REV-8 |

## Start-of-chat recall

- [ ] Ablations still match the construction manifest after edits (WW-001).
- [ ] Tests assert scientific outcomes, not one sentinel/representation (WW-002).
- [ ] `test.sh` has CM-007 hardening (WW-004).
- [ ] Rubric and form explanations are filed under the current REV dossier (WW-005/006).
- [ ] UI rubric lines are `Agent …, ±N` with severity tiers and ≥3 negatives (WW-009 / CM-015).
- [ ] New task languages are niche / not Python-primary (WW-008 / ADR-0014).
- [ ] Graded JSON keys and exact output filenames live in instruction or a cited normative schema doc (WW-010 / CM-018).
- [ ] Eligibility uses the current reviewed snapshot; any exemption names the platform review/revision state and durable evidence (WW-011 / CM-020).
- [ ] Platform and house ownership remain distinct; exempt UI revisions use Python pytest + Playwright Python, never JS/Vitest (WW-012 / CM-022).
- [ ] New task work starts with the four-field proposal check and consults the inspiration source ladder before uniqueness or Step 2a (WW-013).
- [ ] Current writes use `root_adapter.py`; historical roots are read-only; current/historical indexes and generated-view digests are independently current (WW-014 / CM-023).
- [ ] Every official CI check has one coverage disposition; approval exposes delegated `typos` and `check_task_sizes` rather than fabricating local PASS (WW-015).
- [ ] DSV fields use acceptance-safe Humanizer precedence and one current atomic hash audit (WW-016 / ADR-0021/0022).

## RPSP REV-7 (CM-008) — anti-TRIVIAL series contract

When named inspect probes exist, require both: cancellation → refine (`raw==2`)
and well-conditioned → exact `raw`. That blocks always-refine shortcuts without
removing CM-002 discoverability. Bury scream-sticky / `if a < 0` host loci behind
plausible wrong helpers.

## RPM REV-4 (CM-008) — anti-TRIVIAL multi-root contract

Before claiming hardness on a multi-root repair: (1) no correct sibling of the
buggy function elsewhere in env (copy-paste oracle); (2) no loaded-but-unused
fields that grep-land on the fix; (3) no background doc stating the repair rule
verbatim; (4) prove each ablation flips exactly its declared test subset. RPM
REV-4 closed sibling `is_live`, dead `markers_complete`, and the architecture.md
skip giveaway, then added vault/stale-marker and sparse-chunk generalization.
