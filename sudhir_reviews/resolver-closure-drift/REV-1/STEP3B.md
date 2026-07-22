# Step 3b Paper Review — resolver-closure-drift

- **REV:** REV-1 (already open; `revise` not re-run)
- **Task path:** `sudhir_tasks/active/resolver-closure-drift`
- **Spec:** `sudhir_ideas/specs/resolver-closure-drift.md` (attempt 2)
- **Date:** 2026-07-19
- **Task files edited:** no
- **Harbor evidence:** preserved (`oracle_1x` mean=1.0 job `2026-07-19__19-10-14`; `nop` mean=0.0 job `2026-07-19__19-11-15`)
- **Fresh mechanical re-check (this review):** `collapse_check.py` → 0 FAIL / 0 WARN / 23 PASS; `run_static_checks.py` → PASS; `dockerfile_check.py` → PASS; `task_integrity.py verify` → checksum verified

---

## 1. Instruction honesty

Public prose matches the attempt-2 Authoring Brief verbatim (two paragraphs). Operational contracts are stated; causes are not.

| Check | Result |
| --- | --- |
| Concise / human prompt | PASS — two dense paragraphs, no synthetic Deliverables sections |
| Absolute in-container paths | PASS — `/app/repo`, `/app/bin/rebuild-forge`, `/app/bin/forge`, `/app/projects/workspace.toml`, `/app/output/workspace.lock` |
| No task-name / canary leak | PASS |
| No solution-revealing bold / emojis | PASS |
| RC6 mechanical | PASS — symptoms-only (0 families) |
| GX9 answer recital | PASS — no extractable (scenario, key, value) triples; parent selections not listed |
| GX10 polarity contradiction | PASS |
| A24 value over-specification | PASS — no unbound candidate-value lists for instruction-named fields |
| A24 metaphor jargon | PASS — multi-word phrases either name absolute paths/CLI (`forge solve`, lock line schema) or ordinary English (“edge-case behaviors”, “release notes”) with env/history anchors; not coined-only constructs like “in-process lane” |
| Honest-instruction (CM-006 / A24) | PASS — rebuild entrypoint, lock schema, closure/build/byte-identity, offline boundary, and history-as-evidence are disclosed without naming the merge seam or fix symbols |

**Note (LOW):** “supported entrypoint” / “merged failure” are meta-English, not unanchored code metaphors. Instruction correctly points solvers at parent checks and release notes without stating selections.

---

## 2. Environment

| Check | Result |
| --- | --- |
| Digest-pinned `FROM`, pinned apt, WORKDIR `/app` | PASS |
| `allow_internet = false` | PASS |
| Verifier deps in Dockerfile (`pytest==8.4.1`, `pytest-json-ctrf==0.3.5`) | PASS |
| `.dockerignore` present (excludes `solution/`, `tests/`, caches) | PASS |
| No AI scaffolding names / hidden HINT/STEP walkthroughs | PASS (`environment_hidden_instructions`) |
| No `solution/`/`tests/` copied into image; bootstrap build material removed after repo reconstruct | PASS |
| `codebase_size = small`; env file count ≈ 71 (excl. Docker files) | PASS |
| History DAG + parent checks/notes + compilable archive payloads | PASS — matches attempt-2 topology |
| Runtime strip of `/opt/bootstrap` | PASS — patch files remain in the task archive for image build only; agent runtime sees `/app/repo` (+ `.git`) and staged archive/projects |

No HIGH environment defects.

---

## 3. Oracle

| Check | Result |
| --- | --- |
| Real implementation (not hardcoded lock answers) | PASS — rewrites `cast_vane` / `turn_sill` / `lace_quay` |
| Offline | PASS |
| GX3 edit distance | PASS — 115 substantive LOC (mechanical) |
| RC7 transitive LOC | PASS — 195 non-boilerplate |
| GX1/GX2/GX4 (comment leak / bulk-tiny / no-op) | PASS |
| Frontier | 3 roots (`src/aero`, `src/cairn`, `src/quill`); RC8 PASS at 33% concentration |
| Harbor oracle 1x | PASS (recorded); Step 4 10x **not** run (out of scope for 3b) |

Oracle is substantive and distributed. No padding / gaming signals.

---

## 4. Verifiers / Part B (per-test feasibility)

`tests/test.sh` matches Edition 2 reward footer and includes CM-007 triad (`cd /tests`, `--confcutdir=/tests`, `PYTHONSAFEPATH=1`).

All twelve tests rebuild via `/app/bin/rebuild-forge`, invoke `forge solve` on isolated generated projects, parse the public lock schema, validate transitive closure against catalog needs, and require `build-report.json` success (real Cargo path). Exact parent tuples `ALPHA` / `BETA` are embedded in verifier code and independently documented in parent history artifacts (RC4-compliant).

| Test | Checks | Approaches | Chain-dep | Exact values | Risk | Rec |
| --- | --- | --- | --- | --- | --- | --- |
| `test_r01` | Alpha parent selection + closure + build | 2+ | no | yes — history-backed | LOW | keep |
| `test_r02` | Beta parent selection + closure + build | 2+ | no | yes — history-backed | LOW | keep |
| `test_r03` | Mixed roots require both parent outcomes | 2+ | self-contained A+B | yes — justified | LOW | keep |
| `test_r04` | Generated preview classification | 2+ | no | derived from extras | LOW | keep |
| `test_r05` | Archive-order byte identity | 2+ | no | property (equality) | LOW | keep |
| `test_r06` | Clean repeated-run byte identity | 2+ | no | property | LOW | keep |
| `test_r07` | Preview vs stable distinction | 2+ | no | inequality of outcomes | LOW | keep |
| `test_r08` | Beta exact context + plain rejection | 2+ | no (paired case) | yes + negative | LOW | keep |
| `test_r09` | Root/traversal permutation identity | 2+ | no | property | LOW | keep |
| `test_r10` | Generated identity in multi-root graph | 2+ | self-contained A+C | derived | LOW | keep |
| `test_r11` | Policy-sensitive transitive API/build | 2+ | self-contained B+C | yes — BETA | LOW | keep |
| `test_r12` | Generated beta admission across names | 2+ | no | derived | LOW | keep |

**CM-006:** Reward requires live rebuild + solve + closure + offline build — not ELF/string proxies.  
**CM-007:** Pytest cwd-shadow hardening present.  
**Part B escalation:** No order-sensitivity, niche-technique, or chain-dependency flags → `verifier_health.py` not required on the routine path.

**Instruction ↔ test alignment:** Lock schema, rebuild, closure/build, archive/repeat determinism, generated neighbors, and dual parent preservation are covered. Prohibitions against hand-written locks / replaced project inputs are enforced by clean rebuild + generated harness inputs (behavioral), not separate negative unit tests — acceptable.

No HIGH-risk tests. No Part B REJECT patterns.

---

## 5. Collapse / RC8 notes

```
Stage: post-oracle (paper + fresh collapse_check)

Smallest plausible successful patch:
Reconcile preview-channel classification, exact-retained withdrawn admission
(including Mixed), and semantic Trellis commitment so both parent contracts
and generated neighbors produce one buildable, byte-stable closure.

Likely editable frontier:
- src/aero/veil.rs (cast_vane)
- src/cairn/sill.rs (turn_sill)
- src/quill/quay.rs (lace_quay)

Requirement-to-file map:
- Preserve alpha/preview selections → A (+ history)
- Preserve beta/exact-retained → B (+ history)
- Merged interaction / transitive API build → A+B (+ C for identity)
- Archive/root/repeat byte identity → C (semantic sort/dedup/reachability)
- Generated names/ranges → general A/B rules, not tables

Oracle line count (non-boilerplate): 195 (GX3 real edit distance 115)

Discoverability:
Instruction points at history evidence without naming the merge seam or
symbols (CR7 PASS). Parent exact values live in docs/tests under the
reconstructed repo and in verifier constants — intentional. Fix symbols are
opaque. Mild localization aid from Legacy* enum names (see MEDIUM-1) does
not remove typed-composition work.

Red flags: none mechanical (0 WARN / 0 FAIL).

Residual hardness: history archaeology + non-substitutable typed handoff
across three authorities + real Cargo closure — not formatter/sort recipe.

Collapse verdict: PASS (RC8 PASS — 3 roots, 33% concentration; no WARN to waive)
```

**RC8:** No WARN justification required. Distribution within tolerance.

---

## 6. Residual hardness (A0–A5)

| Axis | Verdict | Notes |
| --- | --- | --- |
| A0 Discover | PASS | Parent contracts and typed loss are not in `instruction.md` |
| A0 Synthesize | PASS | A lacks policy; B lacks raw/request; C sees only Admitted graph |
| A0 Diagnose | PASS | Symptoms + operational contract; causes absent |
| A0 Navigate coupling | PASS | Revert-one-parent, writer-only, or single-boundary fixes fail cross tests |
| A0 Reason beyond training | PASS | Project-specific historical composition, not textbook resolver recipe |
| A1 Residual hardness | PASS | After honest prompt, work is typed reconciliation + graph identity |
| A2 Smallest patch | PASS | Not “set listed knobs” / one-table edit |
| A3 Editable frontier | PASS | Three non-obvious opaque modules; decoys present |
| A4 Requirement→file | PASS | No 1:1 prompt-bullet → file checklist |
| A5 Grep-collapse | PASS | CR7: 0 instruction-noun hits on oracle symbols/paths |

**CM-008:** Not a named-inspect-probe / always-refine scientific loophole task. Residual operator work is general policy/graph behavior under generated inputs.  
**CM-010:** Attempt-1 semantic defects were reopened; attempt-2 typed boundaries match the shipped oracle (three distinct roots; CR2 max share 42%). No reopen signal from this paper pass.

---

## 7. Findings

### HIGH
None.

### MEDIUM
1. **`VaneKind::LegacyAlpha` / `LegacyBeta` naming (discoverability aid).** Broken classification emits `Legacy*` kinds that admission already treats as context/legacy failures outside narrow parent modes. A strong agent may localize the A/B seam faster than opaque names would allow. **Does not collapse residual hardness** (Mixed composition, withdrawn+exact rules, quay semantic identity, generated neighbors, Cargo API coupling remain). Acceptable as a single MEDIUM note; no task edit required for Step 3b.

### LOW
1. Agent timeout is platform-capped at 1800s while verifier is 1200s (cannot meet a strict 2× build-heavy guideline). Oracle 1x already succeeded; leave as-is unless Step 4 stress shows timeout pressure.
2. `docs/architecture.md` describes the healthy typed pipeline (Vane → Admitted → Trellis). Useful real-repo docs; does not disclose the merge defect.

### WARN / RC justification
None — collapse returned **0 WARN**.

---

## 8. Verdict

**ACCEPT**

Rationale: mechanical stack clean; instruction honest (symptoms-only, no GX9/GX10/A24 cheating); oracle substantive across three typed authorities; twelve tests independently feasible and behavioral (CM-006/007); Harbor oracle 1x / NOP already recorded; only one non-blocking MEDIUM discoverability note. No task-file edits → Harbor 1x evidence remains valid. Proceed to Step 4 (oracle 10x + post-10x NOP); do not package yet.

**Not done (per request):** Harbor 10x, packaging, commit.
