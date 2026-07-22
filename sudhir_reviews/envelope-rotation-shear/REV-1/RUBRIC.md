# RUBRIC — envelope-rotation-shear REV-1

- +2 Recovery via `/app/bin/vaultctl recover` restores every affected secret readable by `get`
- +2 `/app/output/recovery.json` lists each affected service/secret once and excludes healthy identities
- +2 Healthy records remain byte-identical through recovery and maintenance
- +2 Second `maintain` leaves complete on-disk state unchanged
- +1 Namespace isolation holds for bundled and generated service identities
- +1 Audit rejects tampered protected records
- +1 Audit rejects intact records substituted across service namespaces
- +1 Behavior holds after clean corpus reset and later maintenance cycles
- -2 Replacing the bundled corpus, bypassing authentication, or planting plaintext answers
- -2 Tampering with tests/verifier or reward files
