# Data format

Bundled case files use a line-oriented text format (default
`/app/data/families.case`).

```
family <name>
nodes <n>
values <v0> <v1> ... <v{n-1}>
order <p0> <p1> ... <p{n-1}>
refine <m>
tag <tag-name>
end
```

- `nodes` — active node count for the cold start geometry
- `values` — initial solution samples at those nodes
- `order` — zero-based permutation used when folding digests after remesh
- `refine` — node count after the mid-run remesh (linear interpolation onto
  the refined grid; `order` is reapplied by truncating or wrapping to the
  new length)
- `tag` — variant label emitted on matching runs

Binary fixture blobs under `/app/fixtures/cases/` are opaque shelf samples for
local diagnostics and are not graded inputs.
