# Cutover report schema

The driver emits compact JSON at the configured output path.
Normative layout for `/app/output/cutover_report.json` (and any
`HAZE_OUTPUT` override) is defined here.

Top-level fields:

- `schema_version` — integer, currently `1`.
- `runs` — array sorted lexicographically by `family` then `tag` then `mode`.
- `summary` — aggregate flags derived from the emitted runs:
  - `failing_ok` — boolean; true only when every failing cutover run reports
    successful opens, identity agreement, path resolution, and mode fidelity.
  - `control_stable` — boolean; true only when every file-only control run
    completes with exit_code 0, open_ok true, and rejected false.
  - `reject_stable` — boolean; true only when every reject-family run sets
    `rejected` true.
- `digest` — sixteen lowercase hex characters from the FNV-1a contract below.

Each run object contains:

- `family` — string family identity (for example `failing_alpha`)
- `tag` — string variant tag within the family
- `mode` — one of `"cutover"`, `"control"`, or `"reject"`
- `entry_count` — integer count of durable entries after the cutover attempt
- `exit_code` — integer process-level status recorded for that family
- `open_ok` — boolean; true when every probe open for the family succeeds
- `identity_ok` — boolean; true when every special-entry identity matches the
  pre-cutover contract
- `path_ok` — boolean; true when every alias resolves to an openable target
  under the post-swap staging root
- `mode_ok` — boolean; true when special-entry mode bits match the roster seed
- `rejected` — boolean; true when the family is rejected as deliberately invalid
- `probes` — array of probe objects, each with:
  - `name` — alias name
  - `open_ok` — boolean
  - `identity_ok` — boolean
  - `path_ok` — boolean
  - `mode_ok` — boolean
  - `id_hex` — sixteen lowercase hex characters for the packed identity token
    (or `"0"` when not applicable)

## Report digest (exact FNV-1a contract)

1. Serialize the report as compact JSON with only `schema_version`, `runs`,
   and `summary` (no `digest` key yet). That serialization is a **complete
   JSON object**, so the hashed payload **includes the final closing `}`**.
2. Hash those payload bytes with FNV-1a-64 (offset `0xCBF29CE484222325`,
   prime `0x100000001B3`).
3. Format as sixteen lowercase hex digits.
4. Append `,"digest":"<hex>"}` and a trailing newline so `digest` is the
   final top-level key on disk.

Repeated clean rebuilds must be byte-identical for the same input.
Malformed input must exit nonzero without writing a partial report.
