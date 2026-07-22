# RUBRIC — resolver-closure-drift REV-2

- +2 Lockfile emitted only by rebuilt `/app/bin/forge solve` with exact `<name> <version> <source-id>` lines
- +2 Lock lines sorted ascending by (name, version, source-id) with no duplicate tuples and one final newline
- +2 Solved set satisfies all direct and transitive requirements for bundled and generated projects
- +2 Both established parent edge-case selections remain correct after the merge repair
- +1 Equivalent package archive orderings produce byte-identical lockfiles
- +1 Clean repeated solves produce byte-identical lockfiles
- +1 `/app/output/build-report.json` has success true and members equal to lock tuple count
- +1 Bundled downstream build completes using the solved lock offline
- -2 Hand-writing `/app/output/workspace.lock` or bypassing rebuild-forge
- -2 Tampering with tests/verifier or reward files
