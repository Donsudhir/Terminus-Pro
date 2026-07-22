# VERIFICATION — resolver-closure-drift REV-2

Checks rebuild the forge binary from clean state, run solve on bundled and generated workspaces, and assert lock schema/order/uniqueness, transitive closure, parent edge-case selections, byte-identical repeats under reordered inputs, successful downstream builds, and build-report success/members. NOP remains 0.0; oracle remains 1.0 across Harbor trials.
