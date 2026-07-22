Courier build under /app should ship a fully static musl binary at
/app/output/payload and a behavior ledger at /app/output/probe_report.json.
Stock assembly still links, but qemu-user disagrees with the release contract
at /app/docs/release_contract.md: we still see a program interpreter, the
identity / thread-local / errno rows are off, and settlement stays false.

Get /app/tools/build_payload.sh producing a payload that clears those probes
and a deterministic probe_report.json matching that release contract
(schema_version, payload_digest, rows, settlement; each row has name, ok,
and detail). Tests rebuild through the entrypoint, so hand-written bytes
will not pass.
