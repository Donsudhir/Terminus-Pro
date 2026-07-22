# Release contract

Entrypoint: `/app/tools/build_payload.sh`.

## Outputs

- `/app/output/payload` — fully static x86_64 ELF (no PT_INTERP)
- `/app/output/probe_report.json` — behavior ledger

## Ledger

```json
{
  "schema_version": "1",
  "payload_digest": "<hex>",
  "rows": [
    {"name": "marker", "ok": true, "detail": "..."},
    {"name": "thread", "ok": true, "detail": "..."},
    {"name": "errno", "ok": true, "detail": "..."}
  ],
  "settlement": true
}
```

`payload_digest` is the lowercase hex digest of the payload file bytes
(sha256). Row `detail` values are short labels.

## Runtime probes

Under `qemu-x86_64`, payload stdout must include:

- `MARKER=CXR-7F`
- `THREAD=7`
- `ERRNO=2`
- `LANE_TAG=BRAVO`

`readelf -l` must not list an `INTERP` segment.
