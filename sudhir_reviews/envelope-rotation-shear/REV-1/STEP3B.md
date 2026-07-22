# envelope-rotation-shear — Step 3b Paper Review

- Date: 2026-07-19
- Revision: REV-1 (already open; `revise` not re-invoked)
- Task path: `sudhir_tasks/active/envelope-rotation-shear`
- Approved spec: `sudhir_ideas/specs/envelope-rotation-shear.md`
- Collapse: `0 FAIL, 1 WARN (RC8), 22 PASS` (fresh `collapse_check.py` this review)
- Static / Dockerfile / integrity: PASS (fresh this review; checksum verified)
- Harbor (recorded, not re-run): oracle 1x mean=1.0 (`jobs/2026-07-19__19-17-23`); NOP mean=0.0 (`jobs/2026-07-19__19-18-53`)
- Task files edited this review: **no**
- Harbor re-run required: **no**
- Diagnostics: quality check not run; verifier-health not escalated (no order/flake/chain flags on paper)

## Verdict

**ACCEPT WITH NOTES**

Canonical decision under `review-and-submit.mdc`: collapse overall WARN with documented residual hardness and no HIGH findings. Proceed to Step 4 (oracle 10x + post-10x NOP). Not REJECT.

---

## 1. Instruction honesty

Verdict: PASS.

- Two plain paragraphs (~171 words). Human incident report; no roleplay, headings, emoji, bold solution markers, or synthetic Deliverables sections.
- Absolute in-container paths for `/app/bin/vaultctl`, `/app/output/recovery.json`.
- No task name, canary, algorithm, patch site, internal representation, threshold, or repair order.
- RC6 symptoms-only (0 families). GX6 0 connectives. GX9 no extractable answer triples. GX10 clean.
- A24 reviewer checks:
  - **Value over-spec:** schema fields (`recovered` / `service` / `secret`) and aggregate inventory rules only; no unbound scenario numeric dumps.
  - **Metaphor jargon:** multi-word phrases (`service namespaces`, `protected records`, `healthy identities`) each touch env vocabulary (`ItemID.Service`/`Secret`, operator docs, `vaultctl` usage). No coined-only metaphors.
- Named public CLIs are the contract surface (required by `output_contract.toml`), not implementation scaffolding.

CM-006/CM-008 note: instruction does not emit structural sensitivities that let an agent rewrite the host and skip lineage work; residual work is authority-lineage repair across four typed consumers.

---

## 2. Environment

Verdict: PASS.

- Digest-pinned single-container image; `WORKDIR /app`; apt + verifier pip pinned; `asciinema`/`tmux` present; `allow_internet = false`.
- `.dockerignore` present; no compose / UI / multi-container.
- ~47 substantive env files (excluding Dockerfile/dockerignore) → `codebase_size = "small"` correct; not minimal.
- No AI-scaffolding names, LICENSE, solution/tests COPY, privileged mounts, or precomputed `environment/output|bin` artifacts in the shipped tree.
- Docs (`operator-guide.md`, `storage-format.md`, `operations.md`) describe public workflow and storage layout without STEP/HINT walkthroughs (static `environment_hidden_instructions` clean).
- Decoys (`dial.go`, `relay.go`, `panel.go`, `spool.go`) compile and stay off the oracle frontier.
- Bug shape is plausible production drift: `RouteAxis` / `cachedAxis` / permissive `openSet` / secret-only `Candidates` — not scream-sticky one-glance `if a < 0` loci (CM-008).

---

## 3. Oracle

Verdict: PASS.

- Rewrites exactly the four manifest symbols: `trace_q`, `settle_r`, `route_s`, `replay_t` in four distinct roots; then `gofmt` + `make build`.
- Offline, deterministic, no network, no fixture/gold overwrite, no test edits.
- RC1 PASS (net +132 expanded). RC7 substantive (205 non-boilerplate LOC). GX3 edit distance 168. GX1/GX2/GX4 clean (no comment leakage, bulk-tiny-diff, or no-op rewrite).
- CR1 symbol-table match; CR7 grep-resistant vs instruction nouns; CR8 no central orchestration.
- Real work: stable axis binding on seal, scope encoding without routed cache collapse, strict single-scope open (reject cross-namespace substitutions), predecessor selection validating full item+axis identity.

---

## 4. Verifiers / per-test feasibility

Verdict: PASS. CM-007 triad present in `tests/test.sh` (`cd /tests`, `PYTHONSAFEPATH=1`, `--confcutdir=/tests`). Timeout coherent (verifier 900 ≥ build 600; agent 1800).

| Test | Checks | Approaches | Chain-dep | Exact values | Risk |
|------|--------|------------|-----------|--------------|------|
| `test_e01` | maintain + public reads + healthy file digest | 2+ | no (own reset) | digest justified by byte-stable contract | LOW |
| `test_e02` | generated namespace isolation via get | 2+ | no | derived verifier values | LOW |
| `test_e03` | matching reads + substitute rejection on get | 2+ | no | none | LOW |
| `test_e04` | recover then get on retained damaged case | 2+ | no | derived value | LOW |
| `test_e05` | maintain twice → full tree digest equality | 2+ | no | digest justified | LOW |
| `test_e06` | wider generated matrix isolation | 2+ | no | set equality | LOW |
| `test_e07` | audit rejects tamper and substitute | 2+ | no | exit nonzero only | LOW |
| `test_e08` | recovery.json exact affected inventory + healthy digest | 2+ | no | schema/inventory from instruction | LOW |
| `test_e09` | recover→maintain×2→substitute/audit full workflow | 2+ | no (own reset; multi-requirement in one test) | digest + rejection | LOW |
| `test_e10` | multi generated recover inventory + values | 2+ | no | set of identities | LOW |
| `test_e11` | clean audit OK; substitute fails get+audit | 2+ | no | none | LOW |
| `test_e12` | generated identities through maintain×2 | 2+ | no | digest + values | LOW |

Paper cheat checks (CM-006):

- Formula-only `get` bypass fails substitute/refusal tests (`test_e03`, `test_e11`) because expected failure is keyed to ciphertext acceptance, not CLI-arg plaintext.
- Always-fail `audit` fails `test_e11`'s clean `returncode == 0`.
- Skipping recover fails inventory/`recovery.json` assertions (`test_e08`, `test_e10`).
- Re-encrypt-everything / copy-all-history blocked by healthy byte digests and exact affected-only inventory.

No HIGH chain-dependency: each test calls `cases.reset()` (and usually `retain`/`add_case`) before acting. No wall-clock/memory asserts. No source parsing. Alternate correct lineage implementations that preserve public CLI/schema/digests would pass.

CR2 flipping-point contract PASS (4/12 each under 0.34 cap) — mechanical backstop that single-location patches cannot clear the suite.

---

## 5. RC8 WARN — justification (no task edit)

**Signal:** RC8 WARN — `avg_target_loc = 16.5` (≤20 small-file band); `dominant_root_share = 0.25`, `subsystem_share = 0.25` (not concentrated; concentration thresholds are ≥0.9).

**Why this is acceptable without expanding the frontier:**

1. WARN triggers solely on **small baseline file shape**, not one-subsystem clustering. Targets are evenly split across `aperture`, `conductor`, `ledger`, `tenant` (25% each).
2. CR2 PASS confirms genuine distribution: four locations, four roots, max single-location share 33% under the 34% cap; declared flipping subsets match the suite design.
3. RC7 (205 LOC) and GX3 (168 edit distance) show the oracle's substantive repair is large; thin pre-fix bodies are intentional typed boundaries from the approved Step 2a manifest, not a one-function exploit.
4. Inflating env file size or adding cosmetic oracle lines to silence RC8 would be A16/GX gaming; reviewer policy prefers documenting this WARN.

**Residual hardness after seeing all files and the instruction:** the agent must discover that one stable authority identity must be preserved through seal binding, scope materialization, authenticated open, and journal predecessor selection; local fixes at any single boundary leave the public recover/maintain/get/audit contract failing on the complementary flipping subset. Grep does not map instruction nouns onto `trace_q` / `settle_r` / `route_s` / `replay_t`. Fixture-only cache hits (`cachedAxis` identity rows) vs generated namespaces force general, not scenario-table, repairs.

Collapse verdict for shipping: **WARN justified** → ACCEPT WITH NOTES.

---

## 6. Residual hardness (A0–A2 summary)

| Axis | Assessment |
|------|------------|
| Discover | Must inspect code/logs/fixtures; instruction alone insufficient (RC6 symptoms-only). |
| Synthesize | Four interacting packages + CLI workflow. |
| Diagnose | Symptoms (auth failures, cross-namespace reads), not causes. |
| Navigate coupling | Single-boundary patches flip complementary tests (CR2). |
| Beyond training | Authority-lineage forensics across envelope rotation, not textbook HMAC fill-in. |

Smallest successful patch is still four coordinated function bodies with real validation — not a knob table.

Difficulty estimate: **hard** (aligned with `task.toml`).

---

## 7. Findings

### HIGH

None.

### MEDIUM

None blocking. Single noted observation (does not reject alone):

- **M1 (note):** Pre-fix frontier files are naturally short (12–25 LOC). RC8 WARN is expected for this topology; justified above. Do not pad.

### LOW

- Test docstrings are mechanism-neutral (good); a few are slightly vaguer than the Step 2a plan wording — no contract impact.
- `case_factory.py` embeds a Go sealer for generated cases; stays under `tests/` (not solver-visible as env), GX8 clean.

### CM ledger cross-check

| ID | Result |
|----|--------|
| CM-006 | PASS — behavioral get/audit/recover/digest coverage; reward=1 needs lineage work |
| CM-007 | PASS — hardened pytest invocation present and statically enforced |
| CM-008 | PASS on paper — opaque symbols, no always-refine loophole, loci not scream-sticky; platform re-measure still belongs to post-upload eval |
| CM-010 | PASS relative to shipped artifacts — CR2/CR1/CR9/GX stack green; public contract homes for asserted fields |

---

## 8. Decision criteria mapping

| Criterion | Status |
|-----------|--------|
| Oracle 1x / NOP (Step 2b evidence) | 1.0 / 0.0 recorded |
| Collapse FAIL | none |
| RC6 / RC7 | symptoms-only / substantive |
| Discoverability shortcut | none found requiring fix |
| Static checks | PASS |
| HIGH findings | none |
| Concept redesign needed | no |

**ACCEPT WITH NOTES** — proceed to Step 4. Do not package until oracle 10x + post-10x NOP + PREUPLOAD + `approve_task.py`.

---

## 9. Actions taken / not taken

- Used existing `REV-1` (reason was evidence capture); did **not** run `sudhir_task.py revise`.
- Did **not** edit task files under `sudhir_tasks/active/envelope-rotation-shear`.
- Did **not** invalidate Harbor evidence.
- Did **not** run Harbor 10x, package, or commit.
- Fresh local evidence this review: `collapse_check.py` WARN (RC8 only); `run_static_checks.py` PASS; `dockerfile_check.py` PASS; `task_integrity.py verify` PASS.
