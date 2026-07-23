# ADR-0021: Strict Humanizer gate for DSV fields

- Status: Accepted
- Date: 2026-07-22
- Task ID: Repository-wide
- Related: ADR-0012, ADR-0020

## Context

Difficulty, Solution, and Verification are human-facing submission fields, but
the prior lifecycle relied only on prose instructions. It also asked agents to
plant two or three grammar mistakes, which can create artificial writing and
has no deterministic enforcement. The upstream `blader/humanizer` skill offers
a useful no-fabrication rule and a 33-pattern audit, but its general file mode
can silently rewrite facts or contracts if applied without a TERMINUS boundary.

The user requires Humanizer to apply very strictly to these three fields and to
no other task surface.

## Decision

1. Pin the reviewed Humanizer policy to version 2.9.1, commit
   `523374dee72d67c7b2b5f858ea0094ffda49c3ac`, under its MIT license. Runtime
   task work does not fetch the upstream repository.
2. Add the project-local `terminus-dsv-humanizer` skill to both supported agent
   skill roots. It applies only to Difficulty, Solution, and Verification.
3. Never apply Humanizer to task instructions, rubrics, code, tests, schemas,
   configuration, identifiers, commands, paths, or evidence.
4. Generate DSV prose from a source claim ledger built from the finished public
   instruction, oracle solution, tests, Harbor evidence, and reviewer findings.
   Unsupported facts are removed, never invented or guessed.
5. Treat DSV as one atomic set. `form-capture` rejects partial DSV inputs,
   validates all three before changing the dossier or registry, and creates a
   content-addressed `DSV-HUMANIZER-AUDIT.json` record after PASS.
6. `dsv_humanizer.py` enforces the deterministic portion of the policy:
   required openers, 4–5 sentences, one paragraph, word and sentence bounds,
   punctuation bans, distinct wording, and mechanically detectable Humanizer
   patterns. Every finding blocks capture.
7. New revision dossiers carry `DSV_HUMANIZER_REQUIRED: yes`. Packaging checks
   that the audit hashes match the current DSV files. `package --force` cannot
   bypass this gate.
8. Preserve the platform-required opener `The tests checks`, but stop planting
   any other grammar mistakes. Concrete facts and varied rhythm provide a human
   voice without deliberate errors.
9. The mechanical validator does not claim to prove human authorship or
   semantic fidelity. The model-side 33-pattern and no-fabrication audit remains
   mandatory.

## Consequences

- All future or newly recaptured DSV fields receive the same strict policy.
- Legacy dossiers remain readable and package-compatible until their DSV fields
  are recaptured or a new revision is opened.
- Any DSV edit invalidates its hash audit and blocks packaging until the three
  fields are revalidated and recaptured together.
- Rubric grammar remains a separate planned deterministic gate.
