Terminal Airspace Replay Audit

You are preparing an audit package from fragmented telemetry. Each scenario models one busy terminal sector. The operations team only trusts reports that are reproducible from raw shards, so the same records must always produce the same ranked decisions and the same digest.

Scenarios:
- alpha: one sector X1 with capacity 2
- beta: one sector M1 with capacity 1
- gamma: one sector C1 with capacity 2

Data has realistic quirks: duplicate event revisions, correction records that replace or drop events, repeated sightings for the same flight in the same tick, and priority overrides separated from manifest data. The report should resolve these in a deterministic way and produce the final replay artifact.
