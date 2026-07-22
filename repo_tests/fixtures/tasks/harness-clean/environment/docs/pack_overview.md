# Pack overview

Vendor trees live under `/app/vendor/{alpha,bravo,charlie}` with `include/`
and `lib/` populated at image seed time.

Helpers under `/app/mod_a`, `/app/mod_b`, and `/app/mod_c` feed the staged
workdir used by `/app/tools/build_payload.sh`. Companion dry-run helpers
write operator telemetry under `/tmp` only.

See `/app/vendor/MANIFEST.txt` for a short layout note on each vendor root.
