# L4/L6/L8 pre-target validation

## Scope

This is a validation-only replay of the sealed `rho=1/4` rows.  No `L=10` or
`L=12` target row was run.  The replay uses the separately frozen centerline
protocol and adaptive response-cyclic Krylov implementation in
`compute_phase_screen.py`.

During validation, NumPy's square root of the `int16` translation-orbit period
array was found to produce single-precision normalization factors on this
runtime.  That caused apparent response-subspace projection errors of
`1.290e-7` at L6 and `6.106e-8` at L8 even though all observables already
matched.  Casting the periods to `float64` before the square root removes the
representation error.  The resulting projection residuals are at machine
precision.

## Comparison with sealed direct rows

The four signed differences below are, in order, ground energy, active gap,
response time susceptibility, and lowest-pole residue fraction.

| L | q | status | signed differences from sealed direct row | response projection error |
|---:|---:|---|---|---:|
| 4 | 2 | `RESOLVED` | `-3.553e-15, +3.553e-15, -4.441e-16, -3.331e-16` | `0.000e+00` |
| 6 | 3 | `RESOLVED` | `+5.329e-15, -4.441e-15, +1.221e-15, +0.000e+00` | `4.441e-16` |
| 8 | 4 | `RESOLVED` | `+3.553e-15, -3.553e-15, +1.554e-15, -9.992e-16` | `2.220e-16` |

All rows pass with `PYTHONWARNINGS=error`.  The source comparison is
`DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001/RAW/SECTOR_L*_Q*.json`.
After the authorized target wave, a reporting-only repair added the already
computed lowest five Ritz values to every serialized checkpoint.  The three
controls were replayed and retained the values and projection closure above.

## Current hashes

```text
protocol  9a7bc040c990cdb14c01026ab0e3ce55cc94d767e738911c44bce1753c7584c2
solver    e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7
L4 q2     91ed6d187af06ccb237f5c9f1f53cd75a8da3ae7226252523b33041b9eef71a0
L6 q3     7a905fb31fe6cac898b09c99d801020135b8f57c5c8238f46624db4a06f3a271
L8 q4     e8cc50be7cf253e213bbebda7ee1309990b5c3ad92aefd5a406140169437ea22
```

These hashes are pre-target controls, not a promotion.  The independent blind
implementation must freeze separately before either new target row is opened.
