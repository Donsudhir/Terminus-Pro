# Protected store operator guide

The store exposes one command-line program at `/app/bin/vaultctl`. `get` reads
one catalog identity, `maintain` advances eligible protected frames to the
active key epoch, `recover` processes unreadable live entries, and `audit`
checks live and retained structures. Operational commands return nonzero when
a protected frame cannot be accepted.

The catalog under `/app/var/live` is authoritative for public item placement.
Bundle names and slots are storage details; callers address entries by service
and secret labels. A maintenance run is restartable. It writes a bundle through
a sibling temporary file and renames it only after encoding succeeds.

`/app/bin/inspect` prints a neutral summary of key epochs, live counts, segment
counts, and compaction-density buckets. The summary is diagnostic only and does
not read protected frame bodies.
