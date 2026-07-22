# Long-Horizon Investigation Profile Rollout

## Goal

Make the long-horizon investigation doctrine durable for newly initialized
ideas without retroactively breaking current work or adding speculative runtime
gates.

## Change surface

- Governance: ADR-0013, long-horizon philosophy, decision index, lifecycle,
  knowledge graph, status, and changelog.
- Step 1: idea-bank and refinement prompts plus strategic idea guidance.
- Step 2a: additive `investigation_profile` schema, new-loop contract marker,
  profile validation, and authoring/reviewer guidance.
- Construction: a short preservation rule for declared investigation shape.
- Tests: schema/validator compatibility and web-bundle regression coverage.

No task source, task verifier, packaging rule, category enum, platform
subcategory, runtime gate, or trajectory score changes in this rollout.

## Compatibility strategy

`specs/validation_schema.json` accepts evidence with or without the additive
profile so stored evidence remains readable. `validate_loop.py init` stamps new
loop state with evidence contract version 3. `record` requires the profile only
for version-3 state. Existing state files without that marker use the previous
contract.

## Profile contract

- 2-4 weakness areas;
- 4-8 causally dependent stages;
- 3-8 heterogeneous evidence surfaces with distinct surface types;
- 2-4 plausible hypotheses with deterministic falsifiers;
- 2-6 conditional scenarios containing at least one failing case and one
  healthy control;
- estimated 20-100 meaningful actions;
- deterministic reproduction strategy;
- domain and explanation of why the work is not trivia.

## Verification

1. JSON Schema accepts a valid profile and rejects malformed profile shapes.
2. Custom validation rejects duplicate evidence-surface types and missing
   failure/control roles.
3. A newly initialized loop refuses evidence without the profile.
4. A legacy loop state can still record historical evidence without it.
5. Existing Step 2a and lint tests remain green.
6. Web-bundle tests pin the 2-4-area, 4-stage-chain, and 20-100-action doctrine.
7. Repository lint and focused regression suites pass.

## Rollback

Remove the version-3 marker and profile validation from `validate_loop.py`,
remove the optional schema property, and revert prompt/governance additions.
Historical v2 evidence remains unaffected either way.

## Deferred by design

- action counting from Harbor trajectories;
- process-based reward or rubric scoring;
- static log-volume quotas;
- new platform categories or subcategories;
- generic multi-repository, race, SQL, or performance runtime gates;
- healthcare-specific category metadata.

Promote a deferred mechanism only after pilot evidence demonstrates a recurring
failure that a narrow mechanical check can prevent.

## Verification done

- [x] ADR and canonical philosophy added.
- [x] New loops stamped with evidence contract v3; legacy state grandfathered.
- [x] Additive investigation-profile schema and semantic checks implemented.
- [x] Step 1, Step 2a, Step 2b, taxonomy, workflow, and lifecycle guidance synced.
- [x] Blocked category labels remain blocked; no platform enum changes.
- [x] Directly affected validator, finalize, naming, lint, web, and driver tests: 57 passed.
- [x] Full locked-environment certification: Ruff PASS; 266 passed / 26 skipped.
- [x] No active task source, verifier, package, or archive changed.