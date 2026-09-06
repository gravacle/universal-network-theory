# Final hostile report after lowest-five reporting repair

**Hostile verdict:**
`PASS_REPORTING_REPAIR__CENTERLINE_Z1_REJECTED_L4_L12__HALT_NATIVE_ALGEBRA_ROUTE`

**Checks:** `542/542` passed.

**Exact independently reproduced classification:**
`CENTERLINE_Z1_REJECTED_L4_L12`

The bounded target repair passes.  It closes the reporting defect found by the
first hostile audit; it does not change the physical calculation or promote a
new claim.

## Reporting-repair audit

All five ground and all five response checkpoints at each of L10q5 and L12q6
now serialize `lowest_five_ritz_values`: 20 checkpoint lists in total.  Every
list has exactly five finite values in nondecreasing order.  At every ground
checkpoint the first value reconstructs the checkpoint energy, and at every
response checkpoint it reconstructs `E0 + Delta_act` within `1e-9`.

The final target lists are:

```text
L10q5 ground
-12.746182119255842  -10.725318224498952  -10.363810840149172
 -9.644402299592715   -9.202877096468752

L10q5 response
-11.727012832008370  -10.255295094969387  -10.135916715196510
 -9.579073745974084   -9.461424881190696

L12q6 ground
-15.263603932919514  -13.566841741424197  -12.884760255091882
-12.470614010668532  -12.064798917719289

L12q6 response
-14.411337710776406  -12.991819260077742  -12.811726278923302
-12.594976132059523  -12.230429026980064
```

## Reporting-only classification

The pre-repair promoted values are exactly unchanged in the repaired rows:

| row | `E0` | `Delta_act` | `chi_tau` | `R_low` |
|---|---:|---:|---:|---:|
| L10q5 | -12.746182119255842 | 1.0191692872474718 | 0.8893563670009184 | 0.7891533299283154 |
| L12q6 | -15.263603932919514 | 0.8522662221431077 | 1.0784652119862461 | 0.8251471862764429 |

The independently rebuilt target and blind implementations agree on all exact
dimensions and sparse counts.  All residual, Hermiticity, orthogonality,
projection, convergence, threshold, matvec, wall, and memory checks pass.  The
maximum repaired-target/blind relative difference among `E0`, `Delta_act`,
`chi_tau`, and `R_low` is `6.972e-15`, far inside the frozen tolerances.

The five-size fits are also unchanged:

```text
gap exponent z                 0.965001779728044
chi exponent y                 1.046177707758737
fixed-z1 held-out score        8.202299815159502e-05
free-gapless held-out score    3.413835000353292e-05
positive-gap held-out score    3.543794756520251e-05
```

The same two preregistered checks fail:

```text
fixed_z1_beats_positive_gap    FAIL
fixed_z1_near_free_gapless     FAIL
```

Therefore the repair leaves the exact classification
`CENTERLINE_Z1_REJECTED_L4_L12` unchanged.

## Human-result and route audit

The target `RESULT.md` reports the repaired numerical values, distinguishes a
finite-window rejection from a proof that the thermodynamic exponent differs
from one, and explicitly leaves the critical phase, native spacetime
generators, anomaly, continuum behavior, universal coupling, emergence, and
gravity open.  It records that the Unified Algebraic-Scaling Protocol halts at
Step 1 and that no native-algebra or anomaly calculation is authorized.

The mandatory route disposition remains:

```text
HALT__DO_NOT_START_NATIVE_ALGEBRA
```

## Resource and custody record

The post-repair four-process peak-RSS sum bound is `394,149,888` bytes.  Target
L10/L12 worker time sums to `2.027479916` seconds; blind worker time sums to
`18.831732750` seconds.  Every frozen resource guard passes.

The first hostile method, comparator, freeze, and detailed failure report are
preserved byte-identically.  The first failed-result body remains independently
hash-pinned by `POST_OUTPUT_FREEZE.json` as
`daf75f081eb28b05517d854b7b3b05c5305fbd13cf817e49a61227b92a20dc5b`.
The separate post-repair verifier passed against these current target hashes:

```text
solver                    e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7
target RESULT.json        dcaefd6259fe653676cd6da181f4ee341c2d6e14409b6cc5146a9cdc9c5d056a
target L10q5 raw          c8ce97913795f46b493b1aab328d93cc61eeeefd167407c283e4137847e2dcb9
target L12q6 raw          0e04d2286b3c1669078dc5cd8ff68180c7a989b8741c9f3da772605ca49dde49
```

This result certifies only the repaired finite L4--L12 centerline record and
its frozen rejection.  It does not establish a thermodynamic exponent,
positive limiting gap, spacetime algebra, anomaly, continuum limit, metric,
emergence, or gravity.
