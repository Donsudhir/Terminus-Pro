# VERIFICATION — robust-predicate-scale-parity REV-7

Verification rebuilds through build.sh, runs opaque tests test_r01–test_r12, and also exercises the strict alternate build. Series probes require raw==2 on cancellation cases and exact raw on well-conditioned cases (always-refine alone fails). Status probes require refine mapping for raw code 2. End-to-end checks cover affine cell parity, oriented rows, topology ledger agreement, digest stability, and fail-closed malformed input. pytest runs from /tests with PYTHONSAFEPATH and --confcutdir=/tests.
