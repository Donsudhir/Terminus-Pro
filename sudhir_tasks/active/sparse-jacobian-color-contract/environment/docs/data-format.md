# Data format

Input files use line-oriented records:

```
family <name>
dim <n>
eq <m>
term <equation> <column> <coefficient>   # equation and column indices are 1-based
base <n floating values>
tag <name> <scale> <n shifts>
perm <name> <n indices>    # optional 1-based reordering of unknown ids
end
```

Each `term` line adds one unknown contribution to the current equation. Equations are
numbered implicitly in file order starting at 1. Coefficients define a linear residual
family; sensitivities are constant and verified through independent directional companions.

Tags apply an affine map `x' = scale * x + shift` before evaluation. Permutation records
reorder unknown indices for metamorphic checks while preserving ids in the report.

The bundled corpus under `data/families.resid` defines three families with three tags each.
