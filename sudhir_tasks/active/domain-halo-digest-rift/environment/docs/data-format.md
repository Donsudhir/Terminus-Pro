# Data format

Bundled family files under `/app/data/` use a line-oriented text form:

```
family <name>
nodes <n>
values <n floats>
order <n ints>
refine <m>
tag <label>
end
```

`nodes` is the initial width. `values` are the starting solution samples.
`order` is the active sample ordering used when folding digests. `refine` is
the post mid-run width after the rank-map transition. Blank lines and `#`
comments are ignored. Fixture binaries under `/app/fixtures/` are opaque
support artifacts and are not a graded answer surface.
