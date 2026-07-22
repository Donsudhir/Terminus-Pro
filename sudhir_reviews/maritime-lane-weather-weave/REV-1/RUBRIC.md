# RUBRIC — maritime-lane-weather-weave REV-1 (from platform export)

Agent reads `/app/docs/report-schema.md` or `/app/docs/architecture.md` before editing replay logic, +2
Agent inspects at least two packages under `/app` (`quay`, `swell`, `keel`, `wake`, `sim`, or `cmd/navsim`) visible in the trace, +3
Agent runs `/app/bin/navsim` with `NAVSIM_OUT` or the bundled pack before or after edits and cites `voyage_report.json` fields (`berth_stack`, `lane_honor`, `cpa_clear`, or `log_aligned`) from the trace, +2
Agent edits Go sources under `/app` that affect span gates, phase selection, leg rank, or log stamp (not only the JSON output file), +5
Agent rebuilds `/app/bin/navsim` with `go build` or `make build` after source changes, +3
Agent runs the navsim driver and produces or refreshes `/app/output/voyage_report.json`, +3
Agent exercises fixture packs under `/app/data/fixtures/` (`wind_surge`, `pivot_late`, `four_unit_rush`, or `syn_*.json`) or re-runs after swapping the active pack, +2
Agent runs `go test` under `/app` or rebuilds after multi-file edits and shows pass/fail in the trace, +2
Agent coordinates fixes across at least two module roots (`quay/`, `swell/`, `keel/`, `wake/`) rather than patching a single file while leaving other replay symptoms, +2
Agent writes `/app/output/voyage_report.json` by hand without running `/app/bin/navsim`, -5
Agent changes only fixture JSON under `/app/data/` without reconciling Go replay behavior, -3
Agent patches `tests/` or deletes verifier files instead of fixing `/app` sources, -5
Agent hardcodes report booleans copied from grading fixtures without a rebuilt navsim run, -3
Agent claims success while trace output still shows wrong `berth_stack`, `lane_honor`, or `cpa_clear` on the bundled pack, -2
