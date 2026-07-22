# DIFFICULTY — resolver-closure-drift REV-1

This task is hard because a correct lock is only produced after a typed multi-stage dependency pipeline merges two independently valid parent histories. The solver has to recover the intended admission and trellis rules from repository history, Cargo payloads, and failing vs healthy controls, then keep direct/transitive closure, edge-case parent selections, and byte-identical rebuilds true together. Patching one stage or writing the lockfile by hand does not satisfy the checks.
