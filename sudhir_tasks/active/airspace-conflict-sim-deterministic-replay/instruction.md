Build a deterministic replay audit from fragmented telemetry under /app/environment/data. You are not changing application source code here. The core work is parsing, filtering, reconciling, and aggregating datasets into final outputs.

Create exactly two files:
- /app/output/conflict_windows.json
- /app/output/replay_manifest.tsv

Use these rules.
1. Load manifest.csv, overrides.csv, capacity.csv, corrections.ndjson, and all tracks_*.ndjson files.
2. Apply corrections by event_id: mode=drop removes that event; mode=replace updates only the listed fields.
3. Deduplicate events by (scenario, event_id): keep highest revision; on equal revision keep the record from lexicographically later source filename.
4. Keep only records with state=in.
5. Build per-window flight sets keyed by (scenario, sector, tick). If the same flight appears multiple times in the same window, count it once.
6. A conflict window exists only when unique flights in that window is strictly greater than capacity.
7. Effective priority = base_priority + priority_delta (0 if missing).
8. Rank flights inside each conflict window by: effective priority descending, eta tick ascending, flight_id ascending.
9. Decision is CLEAR for ranks within capacity, HOLD otherwise.

replay_manifest.tsv columns must be:
scenario\ttick\tsector\twindow_id\tflight_id\teffective_priority\teta_tick\trank\tdecision

conflict_windows.json must contain schema_version, scenarios, totals, and deterministic_hash. deterministic_hash is the sha256 hex digest of the exact replay_manifest.tsv bytes.

For scenario context only, read /app/environment/docs/scenario_brief.md.
