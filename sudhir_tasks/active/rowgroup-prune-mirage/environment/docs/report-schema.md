# Loam audit report contract

This document is the normative grading reference for `/app/bin/loam audit`
JSON output and for fresh ingest artifacts. Architecture and rollout notes are
background only; when they disagree with this file, this file wins.

## Audit JSON

UTF-8 JSON object written to the report path passed to `audit`.

| Key | Type | Meaning |
| --- | --- | --- |
| `status` | string | Always the literal `complete` when the run finishes successfully. |
| `cases` | array | One object per `.case` file, in bytewise filename order. |
| `digest` | string | Non-empty hex digest of the serialized `cases` body. |

### Each element of `cases`

| Key | Type | Meaning |
| --- | --- | --- |
| `case_id` | string | Identifier from the case line. |
| `row_count` | integer | Number of qualifying live rows included in the answer. |
| `sum_amount` | integer | Sum of amounts for those qualifying live rows. |
| `pages_total` | integer | Number of slabs present in the store for the case. |
| `pages_read` | integer | Number of slabs actually opened for the case. |
| `path` | string | Execution lane used: `row` or `batch`. |
| `skipping` | boolean | Whether selective admission was requested for the case. |

`row_count`, `sum_amount`, `pages_total`, and `pages_read` are the per-case
answer and work counters. Equivalent modes on the same store and probe must
agree on `row_count` and `sum_amount`. Selective healthy controls must keep
`pages_read` strictly below `pages_total` while still returning the correct
answer. Repeated identical audits must emit byte-identical report files.

## Fresh ingest artifact

`/app/bin/loam ingest <CSV> <store-directory>` writes exactly:

`<store-directory>/data.store`

No other store filename is accepted for grading.

## Faithful live-value markers

Each slab in a store carries numeric markers `low`, `high`, and `has_absent`.

- `low` and `high` span only live amounts in that slab.
- `has_absent` is true when the slab contains any non-live entry.
- A slab whose entries are all non-live records `low` 0, `high` 0, and
  `has_absent` true.
- Fresh ingest must keep those markers faithful to the live-value domain of the
  CSV it wrote. Archived mixed-generation stores keep their on-disk markers;
  readers must interpret them without rewriting the artifact.
