# Format notes from the v2 rollout

These notes were copied from the rollout ticket and may lag the current reader.
They are useful background only. The operational grading contract for audit JSON,
per-case counters, ingest output naming, and live-value markers is
`/app/docs/report-schema.md`.

A file begins with `H|generation`. Each `P` record describes one slab, followed
by the declared number of `R` records. The row record carries presence, origin,
amount, and region. Marker fields let readers avoid opening slabs for predicates
that cannot match.

The v2 rollout assumed the amount lane remained sufficient to recognize missing
historical values because old producers reserved one amount. The later writer
kept origin and presence lanes to support mixed compaction and legitimate values
that overlap old conventions. If these assumptions conflict, the artifact and a
full reader are stronger evidence than this note.
