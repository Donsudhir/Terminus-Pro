# Pinned Humanizer policy for TERMINUS DSV prose

## Source

- Repository: https://github.com/blader/humanizer
- Version: 2.9.1
- Commit: `523374dee72d67c7b2b5f858ea0094ffda49c3ac`
- Commit date: 2026-07-22
- License: MIT, copyright 2025 Siqi Chen
- Local use: reviewed, pinned policy summary. No network fetch occurs while
  writing or validating a task.

This reference is derived from the upstream Humanizer skill. The upstream MIT
notice is stored in [LICENSE](./LICENSE).

## Governing principles

1. Platform acceptance requirements, task truth, and TERMINUS project rules
   outrank every Humanizer preference.
2. Preserve every supported fact and obligation, but do not preserve an awkward
   draft shape when wording can change safely.
3. Never invent a fact, name, number, date, quote, citation, cause, test, or
   personal experience.
4. Use technical, neutral, plain language for DSV fields. Do not inject opinion
   or a persona.
5. A rewrite must not weaken, strengthen, broaden, narrow, or remove an
   observable contract or acceptance-relevant claim.
6. Use clusters and context during the model audit. The deterministic scanner
   is intentionally stricter on mechanically detectable forms.
7. Run draft, audit, and final internally. Embedded mode returns only final
   prose.

## Acceptance-safe transformation boundary

Humanizer may alter only wording and rhythm. The following
elements are immutable unless the underlying accepted task evidence changes:

- required field openers and field-length rules;
- technical meaning, named domain terms, and obligation strength;
- the set of failure modes and healthy controls described;
- solution facts and the distinction between required and optional behavior;
- verifier properties, tested cases, rejection behavior, and determinism claims;
- difficulty reasons, coupling claims, counts, and recorded outcomes;
- all current platform feedback and TERMINUS submission requirements.

After the style pass, compare every clause with the pre-humanized claim ledger.
If a safe rewrite is not possible, keep the acceptance-correct meaning. A less
stylish sentence is always preferable to a cleaner sentence that changes what
the task, solution, or tests actually establish.

## All 33 pattern families

Audit every field and the combined set for these patterns:

1. Inflated significance, legacy, symbolism, or broad-trend claims.
2. Padding based on notability, media coverage, or unnamed prominence.
3. Superficial analysis attached with `-ing` phrases.
4. Promotional or advertisement-like language.
5. Vague attribution to experts, observers, reports, or critics.
6. Formulaic challenges, future prospects, and upbeat outlook sections.
7. High-frequency AI vocabulary used instead of plain technical words.
8. Avoiding `is`, `are`, or `has` with ceremonial substitutes.
9. Negative parallelism such as `not only` or `not just`, and tailing negation.
10. Repeated rule-of-three lists or three-part cadence.
11. Synonym cycling that renames one actor or concept repeatedly.
12. False `from X to Y` ranges without a real ordered scale.
13. Passive voice or subjectless fragments that hide the actor.
14. Em dashes, en dashes, and dash-like double hyphens.
15. Mechanical boldface emphasis.
16. Vertical lists with inline mini-headings.
17. Title-case headings.
18. Emojis or decorative symbols.
19. Curly quotation marks.
20. Chatbot correspondence such as offers, closers, or `let me know`.
21. Knowledge-cutoff disclaimers and speculative gap filling.
22. Sycophantic or servile praise.
23. Filler phrases that can be stated directly.
24. Stacked hedging such as `could potentially possibly`.
25. Generic positive conclusions without a concrete final fact.
26. Uniform overuse of hyphenated compounds.
27. Persuasive-authority tropes such as `the real question`.
28. Signposting announcements such as `let's dive in`.
29. A heading followed by a fragment that merely repeats it.
30. Diff-anchored prose that narrates what changed instead of the final system.
31. Manufactured punchlines and runs of short dramatic fragments.
32. Aphorism formulas such as `the language of` or `becomes a trap`.
33. Fake-candid rhetorical openers such as `Honestly?` or `Here's the thing`.

## TERMINUS overrides

The local DSV contract is stricter than general-purpose upstream file mode:

- Voice samples cannot relax the dash, punctuation, Markdown, or sentence rules.
- File mode is disabled. Use embedded drafting followed by the local validator
  and atomic `form-capture` command.
- First-person observations are disallowed because a model cannot prove the
  builder personally had that experience.
- The exact opener `The tests checks` is preserved as a platform field contract.
- No other grammar error is deliberately added.
- Rubrics and task instructions are outside scope.

## Final internal audit

Before validation, answer these questions internally:

- Does every factual clause have a source in the finished task, solution, tests,
  evidence, or reviewer record?
- Did the rewrite add a cause, algorithm, count, success claim, or test case?
- Did it remove or weaken any supported obligation?
- Did it strengthen a claim beyond the available task or test evidence?
- Did any `must`, `rejects`, `preserves`, `requires`, count, or technical term
   change meaning during the style pass?
- Does Difficulty explain coupled reasoning rather than repeat the instruction?
- Does Solution explain the central repair without hidden answer leakage?
- Does Verification describe actual properties and failure modes in the tests?
- Are the three sections distinct rather than paraphrases of each other?
- Are all 33 pattern families absent or clearly legitimate technical usage?

Any uncertain answer blocks the text. Return to the sources and rewrite without
changing the accepted contract.
