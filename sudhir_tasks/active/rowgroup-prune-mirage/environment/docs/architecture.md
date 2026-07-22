# Loam architecture

Loam is a small offline columnar lab used by release engineering before storage
changes reach the billing warehouse. `rust/` owns import and compaction. It emits
self-describing slabs with value lanes, presence lanes, origin lanes, text codes,
and compact markers. `cpp/` owns reads. The harbor stage decides which slabs are
needed, then either the row reader or lattice reader computes a tally. The row
reader walks record structs; the lattice reader consumes per-slab column lanes.

The command front end reads every `.case` file in bytewise filename order and
every record in source order. Structured counters come from the selected reader,
not from estimates. Artifact files are append-free after creation; a reader must
not repair them in place.

`/app/tools/reset-lab` restores the bundled drill data before a clean replay.

Older slabs are supported because disaster-recovery snapshots outlive the writer
that created them. Newer writers can add header generations, but readers remain
responsible for interpreting each slab according to its own header and local
markers.
