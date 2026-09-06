# Final hostile report: rho=1/4 centerline scaling

**Hostile verdict:**
`FAIL_CLOSED_TARGET_LOWEST_FIVE_TELEMETRY_MISSING__CLASSIFICATION_REPRODUCED_CENTERLINE_Z1_REJECTED_L4_L12__HALT_NATIVE_ALGEBRA_ROUTE`

**Exact independently reproduced classification:**
`CENTERLINE_Z1_REJECTED_L4_L12`

**Checks:** `363/383` passed.  All 20 failures are the same bounded target
reporting defect: five target ground checkpoints and five target response
checkpoints at each of L10 and L12 omit `lowest_five_ritz_values`.  There are
zero substantive target/blind metric, reconstruction, classification, or
resource failures.

## 1. Independent raw agreement

Both new rows are numerically resolved.  Target and blind implementations
agree on exact sector/block dimensions and sparse nonzero counts.  Their
promoted observables agree far inside the frozen tolerances:

| row | metric | target | blind | relative difference | tolerance |
|---|---|---:|---:|---:|---:|
| L10q5 | `ground_energy` | -12.746182119255842 | -12.746182119255836 | 4.181e-16 | 2e-8 |
| L10q5 | `Delta_act` | 1.019169287247472 | 1.019169287247465 | 6.972e-15 | 2e-8 |
| L10q5 | `chi_tau` | 0.889356367000918 | 0.889356367000924 | 6.242e-15 | 5e-7 |
| L10q5 | `R_low` | 0.789153329928315 | 0.789153329928315 | 7.034e-16 | 5e-6 |
| L12q6 | `ground_energy` | -15.263603932919514 | -15.263603932919510 | 2.328e-16 | 2e-8 |
| L12q6 | `Delta_act` | 0.852266222143108 | 0.852266222143104 | 4.169e-15 | 2e-8 |
| L12q6 | `chi_tau` | 1.078465211986246 | 1.078465211986250 | 3.912e-15 | 5e-7 |
| L12q6 | `R_low` | 0.825147186276443 | 0.825147186276443 | 4.036e-16 | 5e-6 |

Response weight and weight-floor differences are at most `2.627e-15` and
`1.024e-15`, respectively.  Every target and blind residual, Hermiticity,
orthogonality, projection, threshold, matvec, process-memory, and process-wall
guard passes.

The four-process peak-RSS sum bound is `408,895,488` bytes, below the 32 GiB
wave guard.  Target L10/L12 worker time sums to `2.008561` seconds; blind
L10/L12 worker time sums to `18.831733` seconds.  Their sum is `20.840294`
seconds.  The blind implementation uses 64 vectors per ground/response solve;
the target uses the allowed 128-vector ceiling.

## 2. Lowest-five reporting audit

The blind raw rows preserve the requested final lowest-five Ritz values:

```text
L10q5 ground
-12.746182119255836  -10.725318224498945  -10.363810840149178
 -9.644402299592713   -9.202336635824555

L10q5 response
-11.727012832008372  -10.255295094969380  -10.135916715196508
 -9.579073745967530   -9.461424880987897

L12q6 ground
-15.263603932919510  -13.566841741424206  -12.884760254852970
-12.470614010667129  -12.064724281502052

L12q6 response
-14.411337710776406  -12.991819260077742  -12.811726278923308
-12.594976132025977  -12.230428994786088
```

Each list is finite, ordered, and has exactly five entries.  Its first ground
value reconstructs `E0`; its first response value reconstructs
`E0+Delta_act` within `1e-9`.

The target solver computes complete checkpoint Ritz arrays internally but its
raw serializer retains only the ground estimate or response metrics.  Thus
the target result is not fully auditable against the requested lowest-five
telemetry.  This is a reporting failure, not evidence of a changed physics
row, and it is failed closed.

## 3. Independent frozen z=1 classification

Combining sealed L4q2/L6q3/L8q4 rows with the blind L10q5/L12q6 rows gives:

```text
free gap exponent z              0.965001779728049
chi growth exponent y            1.046177707758742
abs(z-y)                          0.081175928030693

fixed-z1 held-out score           8.202299815152496e-05
free-gapless held-out score       3.413835000356186e-05
positive-gap held-out score       3.543794756523227e-05

fixed-z1/free-gapless ratio        2.402664397751122
fixed-z1/positive-gap ratio        2.314552726298311
```

The scaled sequences are

```text
L Delta_act:
9.852301989531945, 10.004229114109990, 10.128523509926538,
10.191692872474647, 10.227194665717250

chi_tau/L:
0.0854095110657993, 0.0867304137598760, 0.0878340643943732,
0.0889356367000924, 0.0898721009988542
```

Every monotonicity, exponent-window, exponent-agreement, scaled-tail, and
residue check passes.  The exact check vector is:

| frozen check | result |
|---|---|
| gap strictly decreases | PASS |
| `chi_tau` strictly increases | PASS |
| fixed-z1 beats positive-gap held-out prediction | **FAIL** |
| fixed-z1 score <= 1.25 times free-gapless score | **FAIL** |
| `z` in `[0.90,1.10]` | PASS |
| `y` in `[0.90,1.10]` | PASS |
| `abs(z-y)<=0.10` | PASS |
| L8--L12 `L Delta_act` range <= 0.05 | PASS (`0.0096903`) |
| L8--L12 `chi_tau/L` range <= 0.05 | PASS (`0.0229300`) |
| residue nonzero | PASS |
| L8--L12 residue range <= 0.35 | PASS (`0.1179960`) |

The fixed-z1 family has worse leave-one-size-out prediction than both the
free-gapless and positive-gap alternatives.  It also exceeds the permitted
`1.25` multiple of the free-gapless score.  Because all frozen checks are
conjunctive, the exact classification is therefore
`CENTERLINE_Z1_REJECTED_L4_L12`.

This is a strict protocol rejection, not a proof that the limiting exponent
is unequal to one: the free exponent and scaled observables remain close to
z=1 over this finite window.  Nor does the slight positive-gap score advantage
over fixed-z1 prove a nonzero thermodynamic gap; the free-gapless family has
the best held-out score of the three.

## 4. Required repair and route disposition

Before sealing the target packet, make one reporting-only repair:

1. add `lowest_five_ritz_values` to every serialized target ground and
   response checkpoint;
2. rerun only target L10q5 and L12q6;
3. verify every preexisting promoted metric, convergence value, dimension,
   nonzero count, residual, and resource guard is unchanged within its frozen
   tolerance;
4. rebuild target `RESULT.json`; and
5. rerun this hostile comparison against the repaired hashes.

The repair cannot alter the already reproduced classification unless a
previously hidden inconsistency is exposed.  Independently of this reporting
defect, the frozen classification mandates:

```text
HALT__DO_NOT_START_NATIVE_ALGEBRA.
```

No native algebra or anomaly result was calculated.  Nothing here proves a
thermodynamic phase, continuum, metric behavior, emergence, or gravity.
