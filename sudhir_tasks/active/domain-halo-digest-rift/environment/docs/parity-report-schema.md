# Parity report schema

The driver emits compact JSON at the configured output path.
Normative layout for `/app/output/parity_report.json` (and any
`PARTLAB_OUTPUT` override) is defined here.

Top-level fields:

- `schema_version` — integer, currently `1`.
- `runs` — array sorted lexicographically by `family` then `tag` then `mode`.
  Reordering input families must not change this array or the digest.
- `summary` — aggregate flags derived from the emitted runs:
  - `twin_agree` — boolean; true only when every mapped run’s
    `field_digest` equals the matching steady twin on the same
    `(family, tag)`.
  - `control_stable` — boolean; true only when every no-map-change control
    run’s `reuse_mark` is zero under a clean paired evaluation of the
    same inputs.
  - `digest_match` — boolean; true only when every run’s `field_digest`
    equals an independent fold of that run’s solution samples under its
    emitted `fold_order` (see digest contract below for the fold algorithm).
- `digest` — sixteen lowercase hex characters from the FNV-1a contract below.

Each run object contains:

- `family` — string family identity from the bundled case file
- `tag` — string variant tag within the family
- `mode` — one of `"mapped"`, `"twin"`, or `"control"`
- `field_digest` — sixteen lowercase hex characters; FNV-1a-64 fold of the
  solution `samples` under `fold_order` (same algorithm as the independent
  verifier fold)
- `samples` — array of floating-point solution-field values at active nodes
  after the trajectory finishes (length equals the active node count); this
  is the vector folded into `field_digest`
- `residual_samples` — array of floating-point pointwise residual samples at
  active nodes after the trajectory finishes (length equals the active node
  count)
- `residual_norm` — Euclidean residual magnitude of those samples
- `iterations` — integer step count actually advanced for that trajectory
- `reuse_mark` — unsigned integer host stage binding recorded for the run
- `layout_token` — sixteen lowercase hex characters identifying the active
  fringe/layout stamp after any mid-run rank-map transition
- `fold_order` — array of zero-based integer indices giving the active sample
  ordering used for `field_digest`

## Field digest fold (exact contract)

Given solution `samples` `s[0..n)` and `fold_order` of length `n`:

1. Start with FNV-1a-64 offset basis `0xCBF29CE484222325`.
2. For each index `p` in `fold_order` in listed order, take `s[p]` as an
   IEEE-754 little-endian `f64` byte sequence and mix each of the eight
   bytes: `hash ^= byte`, then `hash = (hash * 0x100000001B3) mod 2^64`.
3. Format the 64-bit result as sixteen lowercase hexadecimal digits.

## Report digest (exact FNV-1a contract)

The reproducibility digest uses **FNV-1a 64-bit** over a precisely bounded
payload:

1. Serialize the report as compact JSON with only `schema_version`, `runs`,
   and `summary` (no `digest` key yet). That serialization is a **complete
   JSON object**, so the hashed payload **includes the final closing `}`**.
2. Hash those payload bytes with FNV-1a-64 (same offset/prime as above).
3. Format as sixteen lowercase hex digits.
4. Append `,"digest":"<hex>"}` and a trailing newline so `digest` is the
   final top-level key on disk.

Repeated clean rebuilds must be byte-identical for the same input.
Malformed input must exit nonzero without writing a partial report.
