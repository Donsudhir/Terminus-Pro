# RUBRIC — cluster-green-tail-red REV-1 (from platform export)

Agent reads /app/docs/cluster-schema.md or /app/docs/architecture.md to learn the outward report contract before editing code, +2
Agent inspects at least two of the Rust crates under /app (blk, proxy, cgroup, sim) visible in the trace, +3
Agent runs /app/bin/cluster_lab on the bundled pack before or after edits and cites p99_band, proxy_retry_heat, or io_wait_share from the trace output, +2
Agent repairs block-throttle wait logic in blk/ (OpA primary vs noisy hold behavior), +5
Agent repairs proxy retry amplification logic in proxy/ (OpB rounds, streak, or limit handling), +5
Agent repairs cgroup queue wait logic in cgroup/ (OpC depth scaling per lane), +5
Agent repairs sim/driver.rs dispatch ordering, I/O wait fold, or proxy-streak reset when driver edits are visible in the trace, +3
Agent rebuilds /app/bin/cluster_lab after source changes (cargo build or make visible in the trace), +3
Agent runs /app/bin/cluster_lab and produces or refreshes /app/output/cluster_report.json, +3
Agent re-runs the lab or exercises fixture packs under /app/data/fixtures/ (neighbor_flood.json, proxy_retry_storm.json) after a fix attempt, +2
Agent consults /app/catalog/guardrails.toml for median or serving-floor expectations, +1
Agent coordinates fixes across at least two module roots (blk/, proxy/, cgroup/, or sim/) rather than patching a single file while leaving other tail symptoms, +3
Agent writes cluster_report.json by hand without running cluster_lab, -5
Agent changes only scenario_pack.json or fixture JSON without reconciling Rust behavior, -3
Agent patches tests/ or deletes verifier files instead of fixing /app sources, -5
Agent changes only policy_kind or fold thresholds in sim/driver.rs without editing wait logic under blk/, proxy/, or cgroup/, -3
Agent adds unbounded retry loops or busy-wait sleeps in application code, -3
Agent claims success while p99_band or proxy_retry_heat in the trace still show runaway or hot on the bundled pack, -2
