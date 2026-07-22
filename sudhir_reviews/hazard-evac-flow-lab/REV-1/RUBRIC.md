# RUBRIC — hazard-evac-flow-lab REV-1 (from platform export)

Agent reads `/app/docs/plan-schema.md` or `/app/docs/architecture.md` before editing routing or replay logic, +2
Agent inspects at least two of `graph/`, `flow/`, `wave/`, `prior/`, and `sim/` packages visible in the trace, +3
Agent runs `/app/bin/evac_planner` with `EVAC_PLANNER_OUT` or default output path and cites `evac_plan.json` fields in the trace, +2
Agent edits Go sources under `/app` (not only JSON output), +5
Agent rebuilds `/app/bin/evac_planner` with `go build` after source changes, +3
Agent exercises `/app/data/evac_pack.json` or a swapped fixture pack and compares plan fields, +2
Agent coordinates fixes across at least two package roots rather than one file only, +2
Agent runs `go test` under `/app` after substantive edits and shows pass/fail in the trace, +2
Agent writes `/app/output/evac_plan.json` by hand without running `/app/bin/evac_planner`, -5
Agent patches `tests/` or deletes verifier files instead of fixing `/app` sources, -5
Agent changes only `/app/data/` fixtures without reconciling Go replay logic, -3
Agent hardcodes plan field literals copied from grading packs without a rebuilt planner run, -3
Agent claims success while trace still shows severe jam_band or false hazard_ok on the bundled pack, -2
