# Step 2a Specification Workspace

Generated task specifications and validation state live in this directory during authoring and remain local by default. The only tracked files are this guide and `validation_schema.json`, which defines the evidence contract used by `validate_loop.py`.

Generated files include:

- `<task>.md` - approved authoring specification;
- `<task>-reviewer.md` - reviewer-only appendix;
- `<task>-attempt-N-evidence.json` - structured validation evidence;
- `<task>-validation-log.md` - attempt and gate history;
- `.<task>-state.json` - validation-loop state.

Do not commit generated specifications unless an ADR explicitly promotes one into a durable fixture. Do not place secrets or API credentials in this workspace.

New loops initialized after ADR-0013 use evidence contract v3 and require the
additive `investigation_profile` defined in `validation_schema.json`. The JSON
Schema keeps that property optional so historical evidence remains readable;
`validate_loop.py` enforces it from the loop state's contract version. The
profile records 2-4 weakness areas, a causal chain, heterogeneous evidence,
falsifiable hypotheses, failure/control scenarios, a 20-100 meaningful-action
estimate, deterministic reproduction, and domain non-trivia reasoning.
