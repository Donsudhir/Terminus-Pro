---
name: terminus-dsv-humanizer
description: "Use whenever writing, revising, reviewing, validating, or capturing Terminal-Bench Difficulty Explanation, Solution Explanation, or Verification Explanation fields. Applies blader/humanizer only as an acceptance-safe style pass: platform requirements, task truth, and TERMINUS rules always win. Never use for task instructions, rubrics, code, tests, schemas, or configuration."
user-invocable: false
disable-model-invocation: false
---

# TERMINUS acceptance-safe DSV Humanizer

Apply this workflow only to the three final Snorkel explanation fields:
Difficulty, Solution, and Verification. The policy is derived from
`blader/humanizer` v2.9.1 at commit
`523374dee72d67c7b2b5f858ea0094ffda49c3ac` under the MIT license.
Read [the pinned policy](./references/HUMANIZER-POLICY.md) before drafting.

## Hard scope

- Use the full strict pass for all three fields every time one changes.
- Never humanize `instruction.md`, rubrics, task source, tests, solution code,
  TOML, JSON, schemas, identifiers, commands, paths, or evidence records.
- Treat the three fields as one atomic set. Do not revise or capture only one.
- Work in embedded mode. Run draft, audit, and final internally, then expose
  only the final three fields.

## Acceptance lock

Apply this precedence without exception:

1. Current platform field requirements and reviewer feedback.
2. Truth from the finished instruction, solution, tests, and recorded evidence.
3. TERMINUS lifecycle, acceptance, and submission rules.
4. Humanizer style preferences.

Humanizer may change wording and sentence rhythm only. It must not add, remove,
weaken, strengthen, generalize, or reinterpret any requirement, failure mode,
solution fact, verifier property, difficulty reason, technical term, count, or
evidence claim. Keep obligation words such as `must`, `rejects`, `preserves`,
and `requires` when they carry acceptance meaning.

If removing an AI-writing pattern would change technical meaning, acceptance
scope, or project compliance, keep the accurate meaning and find a different
plain-language sentence. Never trade acceptance safety for a more human tone.

## Source lock

Before writing, read the finished public instruction, oracle solution, tests,
current Harbor evidence, and current reviewer findings. Build an internal claim
ledger with one source location for every technical statement. A statement
without a source is removed, not softened, generalized, or guessed.

Do not add facts, names, numbers, dates, causes, algorithms, test coverage,
success claims, citations, personal experiences, or implementation details that
are absent from those sources. Do not expose hidden answer-shaped details.

## Required field contract

- Difficulty begins exactly `This task is hard because`.
- Solution has no forced opener.
- Verification begins exactly `The tests checks`.
- Each field is one paragraph containing exactly four or five sentences.
- Use 45 to 140 words per field and 6 to 45 words per sentence.
- Use simple technical English with varied sentence lengths.
- Use no Markdown, list, heading, code formatting, URL, or citation.
- Use no em dash, en dash, double-hyphen dash, semicolon, curly quote, or emoji.
- Use no repeated five-word phrase across fields.
- Preserve the platform-required `The tests checks` wording even though its
  grammar is unusual. Do not manufacture any other grammar mistakes.

The last rule supersedes the older instruction to inject two or three grammar
mistakes. Human prose comes from concrete facts, uneven rhythm, and direct
language, not planted errors.

## Strict Humanizer loop

1. Draft from the claim ledger, not from memory.
2. Run the acceptance-lock comparison against the draft before styling it.
3. Audit all 33 upstream pattern families in the pinned policy.
4. Ask internally whether any claim lacks a source, any obligation disappeared,
   or any acceptance-relevant word changed strength.
5. Rewrite style only until every finding is gone without changing meaning.
6. Run the deterministic gate:
   `python3 dsv_humanizer.py --difficulty-file D --solution-file S --verification-file V`
7. Treat every mechanical finding as blocking, but resolve it only through a
   meaning-preserving rewrite. Revise all three fields and rerun until it exits
   zero.
8. Capture the passing set with `sudhir_task.py form-capture`. That command
   validates again, writes a content-addressed audit, and rejects partial sets.

Never claim that the deterministic scan proves human authorship. It proves only
that the current files satisfy the local style contract and match the recorded
audit. Platform acceptance, factual fidelity, and project compliance remain the
controlling requirements.
