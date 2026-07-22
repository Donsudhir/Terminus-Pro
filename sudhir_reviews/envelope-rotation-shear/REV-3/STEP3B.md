# envelope-rotation-shear — REV-3 Step 3b Paper Review

- Date: 2026-07-19
- Revision: REV-3
- Task path: `sudhir_tasks/active/envelope-rotation-shear`
- Trigger: platform MEDIUM result was evaluated as Python; failure analysis also found that direct healthy reads for generated namespaces were not stated clearly enough
- Task edits: `task.toml` language metadata and `instruction.md` only
- Spec amendment: authoring brief and reviewer appendix record the Go-only classification and paired positive/adversarial read contract
- Static / Dockerfile / integrity: PASS
- Collapse: 0 FAIL, 2 WARN, 21 PASS
- Harbor oracle 1x: mean 1.0, `jobs/2026-07-19__23-51-22`
- Harbor NOP: mean 0.0, `jobs/2026-07-19__23-52-55`
- Diagnostics: quality check not run; verifier-health not escalated because platform agents did not score 0/10 and paper review found no order, chain, or flake concern

## Verdict

**ACCEPT WITH NOTES** for Step 4.

The revision corrects a metadata defect and a real instruction-sufficiency gap without changing the environment, oracle, verifier, or expected behavior. The platform's implementation-level fallback description is treated as one possible repair, not as a required algorithm. No task file should change after this review without reopening evidence.

## 1. Feedback resolution

### Go-only agent-facing language

`task.toml` now declares `languages = ["go"]`. Every agent-facing source file and every oracle fix location is Go. Python remains only in verifier infrastructure under `tests/`, which is allowed by ADR-0014 and does not make this a Python task. The next platform upload must select Go rather than Python in any language field.

### Paired healthy and adversarial read contract

The instruction now states both observable outcomes:

1. valid live records in newly introduced service namespaces read directly without recovery;
2. intact records substituted across service namespaces fail without recovery and do not trigger recovery.

The clarification is symptoms-only. It does not name scopes, routing, caches, fallback branches, `AxisFor`, `SealAt`, a source path, or a repair order.

### Platform fallback analysis

The feedback says fallback should remain when `frame.Axis == AxisFor(frame.Item)`. That condition already exists in the baseline, and the verifier's substitution helper copies an internally coherent source frame, so the condition alone cannot reject the substituted bundle. The current oracle instead canonicalizes context production and requires one matching scope at authenticated open. This strict design passes all tests and proves that retaining one particular fallback branch is not the only valid implementation.

The verifier correctly grades outcomes rather than source representation. A solver may canonicalize the producer/consumer scope or preserve a compatibility path guarded by sufficient caller identity, provided valid generated reads work and substitutions fail. No fifth oracle location or construction-manifest change is justified.

## 2. Instruction honesty

Verdict: PASS.

- Two natural incident-report paragraphs with absolute public paths.
- No task name, internal cause, algorithm, patch location, threshold, or implementation prescription.
- RC6 remains `symptoms-only` with zero specificity families.
- GX9 has no extracted answer triples and GX10 finds no polarity contradiction.
- The new positive sentence closes CM-002 rather than manufacturing difficulty through a hidden healthy-control requirement.
- Schema vocabulary remains limited to the documented public recovery artifact.

The clarification may make the intended tradeoff easier to notice. That reduction is required because both sides are scored. Residual difficulty remains in diagnosing and coordinating the implementation, not guessing an unstated contract.

## 3. Environment and oracle

Verdict: PASS.

- The single-container offline Go system remains unchanged.
- Digest pinning, dependency placement, `.dockerignore`, agent session tools, and Python interpreter hygiene all pass.
- The oracle still rewrites exactly four manifest symbols in four roots and makes no test, fixture, or gold edits.
- RC1 reports net +132 lines, RC7 reports 205 transitive non-boilerplate lines, and GX3 reports 168 lines of real edit distance.
- CR1, CR2, CR7, CR8, and CR9 pass. The frontier remains opaque to public instruction nouns.

## 4. Test alignment and feasibility

| Test | Public property | Independent setup | Risk |
| --- | --- | --- | --- |
| `test_e01` | maintenance, matching reads, healthy-byte preservation | yes | LOW |
| `test_e02` | direct reads for generated namespaces without recovery | yes | LOW |
| `test_e03` | matching reads plus substituted-record rejection | yes | LOW |
| `test_e04` | public recovery and restored read | yes | LOW |
| `test_e05` | exact second-maintenance stability | yes | LOW |
| `test_e06` | wider generated-namespace direct-read and isolation matrix | yes | LOW |
| `test_e07` | audit rejects tamper and substitution | yes | LOW |
| `test_e08` | exact recovery inventory and healthy preservation | yes | LOW |
| `test_e09` | complete recovery/maintenance workflow and later rejection | yes | LOW |
| `test_e10` | generated prior-history recovery and reads | yes | LOW |
| `test_e11` | clean audit succeeds, then get and audit reject substitution | yes | LOW |
| `test_e12` | generated older records remain readable through two maintenance runs | yes | LOW |

`test_e02` and `test_e06` are the direct positive controls that agents missed after deleting all compatibility behavior. `test_e03`, `test_e07`, `test_e09`, and `test_e11` cover the adversarial side. `test_e10` and `test_e12` extend the generated-identity invariant through recovery and maintenance. Every test resets or creates its own state, uses deterministic values, and permits multiple valid implementation strategies.

CM-007 hardening is present. The verifier writes initial zero reward, runs from `/tests` with `PYTHONSAFEPATH=1` and `--confcutdir=/tests`, and does not make Python part of the agent-facing implementation.

## 5. Collapse WARN justifications

### RC8 frontier concentration

The diagnostic reports a 25% dominant-root share across four targets in four roots. This is evenly distributed, not concentrated. The WARN is caused by short baseline typed-boundary files, while CR2 confirms four locations and a maximum single-location share below the cap. RC7 and GX3 confirm substantive oracle work. Padding files to silence the warning would be gate gaming.

### GX6 causal connective density

The instruction contains three ordinary connectives in 245 words, just inside the WARN band. They describe observed timing and required command behavior, not an internal causal chain. RC6 finds no algorithm, schema over-specification, API enumeration cluster, numeric threshold, binding phrase, or scope closure. The prose names no authority representation or patch site, so the WARN is accepted without weakening the now-complete public contract.

## 6. Difficulty assessment

The platform measured this revision family as MEDIUM with model pass rates of 80% and 60%. That result is recorded honestly and is not relabeled as HARD locally. The rejection text applied the Python threshold because metadata incorrectly included Python; REV-3 fixes that classification to Go.

The repo-local hard authoring checks still pass: the oracle is substantive, four roots are involved, the instruction is symptoms-only, and the verifier forces both healthy and adversarial outcomes. The next platform run remains authoritative for acceptance and difficulty under the corrected Go label.

## 7. Findings

### HIGH

None.

### MEDIUM

None blocking.

### LOW / notes

- Platform language must be selected as Go at upload; the archive cannot correct a manually selected UI field.
- The platform's fallback explanation overstates one implementation path. Public behavior, not that source-level prescription, is authoritative.
- The platform pass rate may remain MEDIUM. REV-3 resolves the stated Python-threshold mismatch rather than disguising the measured result.

## 8. Decision mapping

| Criterion | Result |
| --- | --- |
| Static / Dockerfile / integrity | PASS |
| Oracle 1x | 1.0 |
| NOP | 0.0 |
| Collapse | WARN, both justified |
| RC6 / RC7 | symptoms-only / substantive |
| Test-instruction alignment | PASS after positive generated-read clarification |
| Go-only agent-facing metadata | PASS |
| HIGH findings | none |
| Step 4 needed | oracle 10x, fresh NOP, PREUPLOAD, package, approval |

**Decision: ACCEPT WITH NOTES. Proceed to Step 4 without further task edits.**
