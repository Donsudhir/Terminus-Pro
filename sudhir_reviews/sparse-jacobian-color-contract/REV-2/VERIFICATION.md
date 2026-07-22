# VERIFICATION — sparse-jacobian-color-contract REV-2

Verification rebuilds through build_all.sh and runs opaque tests test_k01–test_k13. Checks cover permutation and resume parity, directional probes, per-batch scale summary isolation with absolute ref/step expectations, lexicographic run ordering for byte-identical reordered inputs, ledger.active equal to retained packed values, ids preserved as 1..cols, digest stability, and malformed input exiting nonzero without writing a partial report. pytest runs from /tests with PYTHONSAFEPATH and --confcutdir=/tests.
