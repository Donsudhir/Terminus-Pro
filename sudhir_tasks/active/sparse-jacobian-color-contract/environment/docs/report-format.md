# Report format

The driver emits compact JSON at the configured output path.
Normative layout for `/app/output/sensitivity_report.json` (and any
`SENSLAB_OUTPUT` override) is defined here.

Top-level fields:

- `schema_version` — integer, currently `1`.
- `runs` — array sorted lexicographically by `label.family` then `label.tag`.
  Reordering input families must not change this array or the digest.
- `digest` — sixteen lowercase hex characters from the FNV-1a contract below.

Each run object contains:

- `label` — `{ "family": string, "tag": string }`
- `ids` — unknown identities in source order `1..cols` (cardinality and labels
  unchanged by tag scale/shift; permutations remapped in the packed matrix, not
  by rewriting `ids`)
- `values` — packed nonzero sensitivity entries (operator first-order response at
  each retained `(row, col)` for the active affine state; may differ from bare
  declared term numbers when the operator applies equation participation)
- `indices` — flattened `[row, col, row, col, ...]` pairs aligned with `values`
- `dims` — `{ "rows": m, "cols": n, "nnz": k }`
- `products` — directional companion results for the bundled probe directions:
  width 4 → `[1.0, 0.5, 0.25, 2.0]`; width 5 → `[1.0, 0.5, 0.25, 2.0, 1.5]`;
  other widths → entry `i` (0-based) is `1.0 + 0.1 * i`
- `ledger` — `{ "total": k, "groups": g, "active": a }` support counters where
  `active == len(values)`, `total == dims.nnz`, and `groups` is the number of
  independent probe groups required by the nonzero conflict structure (not
  merely one group per unknown)
- `span_info` — scale summary for the active run only:
  - `ref` — Euclidean residual magnitude of the active batch state
  - `step` — `max(max(ref * 1e-6, step_floor) * step_gain, step_floor)` from
    `/app/conf/runtime.conf` (defaults `step_floor=1e-8`, `step_gain=0.5`);
    must not inherit magnitude from a prior batch and must not invent
    power-of-two quantization. Changing `step_floor` / `step_gain` in
    `runtime.conf` must change the emitted `step` accordingly.

## Digest (exact FNV-1a contract)

The reproducibility digest uses **FNV-1a 64-bit** over a precisely bounded
payload:

1. Serialize the report as compact JSON with only `schema_version` and `runs`
   (no `digest` key yet). That serialization is a **complete JSON object**, so
   the hashed payload **includes the final closing `}`** of that object. It is
   not an open prefix that stops before the brace.
2. Hash those payload bytes with FNV-1a-64:
   - offset basis `0xCBF29CE484222325`
   - prime `0x100000001B3`
   - for each byte: `hash ^= byte`, then `hash = (hash * prime) mod 2^64`
3. Format the 64-bit result as **sixteen lowercase hexadecimal digits**
   (`%016x`).
4. Append `,"digest":"<hex>"}` and a trailing newline so `digest` is the final
   top-level key on disk.

Repeated clean rebuilds must be byte-identical for the same input.
Malformed input must exit nonzero without writing a partial report.
