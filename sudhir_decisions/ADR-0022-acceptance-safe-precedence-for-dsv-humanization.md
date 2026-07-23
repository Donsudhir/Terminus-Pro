# ADR-0022: Acceptance-safe precedence for DSV humanization

- Status: Accepted
- Date: 2026-07-22
- Task ID: Repository-wide
- Supersedes: ADR-0021 only where Humanizer strictness could compete with acceptance meaning
- Related: ADR-0012, ADR-0021

## Context

ADR-0021 correctly restricts Humanizer to Difficulty, Solution, and
Verification and makes their audit non-bypassable. Its wording could still be
read as requiring style cleanup at any cost. A generic Humanizer preference
must never remove a tested behavior, soften an obligation, strengthen an
unsupported claim, change a technical term, or conflict with current platform
and TERMINUS submission requirements.

The user requires all three fields to sound human while preserving task
acceptance and every project guideline.

## Decision

1. Humanizer is a final style-only pass. It may alter wording and rhythm but
   not sentence order or acceptance meaning.
2. Apply this precedence:
   1. current platform field requirements and reviewer feedback;
   2. finished task truth from instruction, solution, tests, and evidence;
   3. TERMINUS lifecycle, acceptance, and submission rules;
   4. Humanizer style preferences.
3. The following are immutable during humanization: requirement and obligation
   strength, failure modes, healthy controls, solution facts, verifier
   properties, tested cases, difficulty reasons, technical terms, counts,
   determinism claims, and recorded outcomes.
4. If a style rewrite risks any item above, keep the acceptance-correct meaning
   and use another plain sentence. A less polished accurate sentence is better
   than a human-sounding semantic drift.
5. Continue the DSV-only scope and atomic capture from ADR-0021. Humanizer still
   cannot inspect or rewrite instructions, rubrics, code, tests, schemas,
   configuration, evidence, task source, or archives.
6. Version the mechanical policy as
   `terminus-dsv-humanizer-acceptance-safe-2026-07-22`. Every audit records its
   three-field scope, `wording-and-rhythm-only` boundary, and the exact
   acceptance precedence.
7. The deterministic checker validates format and detectable style patterns but
   cannot prove semantic equivalence or platform acceptance. The source claim
   comparison remains a mandatory model-side review.

## Consequences

- DSV prose is humanized only inside a fixed acceptance envelope.
- Humanizer cannot become a reason to alter task meaning or violate project
  guidance.
- Existing ADR-0021 scope, atomic capture, hash audit, and package enforcement
  remain active.
- A stale audit from the prior policy ID must be regenerated before packaging.
