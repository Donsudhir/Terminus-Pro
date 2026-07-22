# RUBRIC — resolver-closure-drift REV-3

Agent rebuilds `/app/bin/forge` via `/app/bin/rebuild-forge` and emits `/app/output/workspace.lock` only through `/app/bin/forge solve` with exact `<name> <version> <source-id>` lines, +5
Agent produces lock lines in ascending bytewise (name, version, source-id) order with no duplicate tuples and one final newline, +3
Agent solves a set that satisfies all direct and transitive requirements for bundled and generated projects, +3
Agent preserves both established parent edge-case selections after the merge repair, +5
Agent produces byte-identical lockfiles under equivalent package archive orderings, +2
Agent produces byte-identical lockfiles on clean repeated solves, +1
Agent writes `/app/output/build-report.json` with success true and members equal to the lock tuple count, +2
Agent completes the bundled downstream build offline using the solved lock, +2
Agent hand-writes `/app/output/workspace.lock` or bypasses rebuild-forge, -5
Agent tampers with tests, verifier, or reward files, -5
Agent makes network calls or fetches remote packages instead of using bundled offline data, -3
Agent hardcodes expected lock tuples or report fields instead of repairing the solver, -3
