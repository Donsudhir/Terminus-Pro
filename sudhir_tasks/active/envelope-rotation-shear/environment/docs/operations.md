# Operations notes

The deterministic fixture reset copies the checked-in protected bundles into
`/app/var`, clears transient sibling files, and removes the previous recovery
report. It does not synthesize key material or decode payloads.

Maintenance visits catalog entries in item order. An entry already written for
the active epoch remains in place. Older accepted entries are replaced
atomically, and an interrupted write leaves only a `.next` file that reset can
discard. Operators compare complete tree hashes between repeated runs when
checking stability.

Audit opens every catalog entry through its public identity and separately
checks segment structure, sequence uniqueness, and authority headers. A failed
live open or malformed segment stops the command. The observation utility is
safe to run during triage because it reports counts and key fingerprints only.
