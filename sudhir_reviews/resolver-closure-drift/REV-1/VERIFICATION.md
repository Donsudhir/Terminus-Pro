# VERIFICATION — resolver-closure-drift REV-1

Checks rebuild the forge binary from clean state, run solve on bundled and generated workspaces, and assert lock schema/order/uniqueness, transitive closure, parent edge-case selections, byte-identical repeats under reordered inputs, and successful downstream builds. NOP remains 0.0; oracle remains 1.0 across ten Harbor trials.
