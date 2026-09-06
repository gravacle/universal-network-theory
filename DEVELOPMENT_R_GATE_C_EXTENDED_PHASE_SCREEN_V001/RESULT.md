# Gate R-C rho=1/4 centerline result

## Frozen verdict

```text
CENTERLINE_Z1_REJECTED_L4_L12
```

Both new target rows resolved and an independently frozen implementation
reproduced them to machine precision.  The finite-size exponents are close to
one, and the scaled tail is stable, but the preregistered strict `z=1`
classification fails both held-out model-comparison gates.  Therefore the
Unified Algebraic-Scaling Protocol halts at Step 1.  No native-algebra or
anomaly calculation is authorized.

This is rejection of the declared finite-window `z=1` prerequisite, not a
proof that the thermodynamic exponent differs from one.

## New target rows

| L | q | block dimensions `(ground,response)` | `Delta_act` | `chi_tau` | `R_low` | target RSS | target wall |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 5 | `(1552,1550)` | `1.019169287247472` | `0.889356367000918` | `0.789153329928315` | `44,875,776 B` | `0.245 s` |
| 12 | 6 | `(11240,11196)` | `0.852266222143108` | `1.078465211986246` | `0.825147186276443` | `174,489,600 B` | `1.782 s` |

Both rows are `RESOLVED`.  Ground and active-pole residuals are below
`2.0e-14`, response projection errors are below `3.2e-15`, and all
Hermiticity, orthogonality, threshold, matvec, wall, and memory guards pass.

The blind implementation returns:

| L | `Delta_act` | `chi_tau` | `R_low` | blind RSS | blind wall |
|---:|---:|---:|---:|---:|---:|
| 10 | `1.019169287247465` | `0.889356367000924` | `0.789153329928315` | `44,924,928 B` | `0.777 s` |
| 12 | `0.852266222143104` | `1.078465211986250` | `0.825147186276443` | `129,859,584 B` | `18.054 s` |

Across the two new rows, the maximum target/blind relative disagreement in
ground energy, gap, `chi_tau`, or `R_low` is `6.972e-15`.

## Five-size scaling record

| L | q | `Delta_act` | `L Delta_act` | `chi_tau` | `chi_tau/L` | `R_low` |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 2 | `2.463075497383` | `9.852301989532` | `0.341638044263` | `0.085409511066` | `0.428094707816` |
| 6 | 3 | `1.667371519018` | `10.004229114110` | `0.520382482559` | `0.086730413760` | `0.632801772065` |
| 8 | 4 | `1.266065438741` | `10.128523509927` | `0.702672515155` | `0.087834064394` | `0.732829820694` |
| 10 | 5 | `1.019169287247` | `10.191692872475` | `0.889356367001` | `0.088935636700` | `0.789153329928` |
| 12 | 6 | `0.852266222143` | `10.227194665717` | `1.078465211986` | `0.089872100999` | `0.825147186276` |

The free gap power fit gives

```text
Delta_act = 9.395464209341 L^(-0.965001779728)
chi_tau exponent y = 1.046177707759
```

The tail (`L=8,10,12`) relative ranges are `0.0096903` for
`L Delta_act`, `0.0229300` for `chi_tau/L`, and `0.1179960` for the residue.
Thus monotonicity, exponent windows, exponent agreement, both scaled-tail
stability checks, and both residue checks pass.

The two failing preregistered checks are:

```text
fixed-z1 held-out relative SSE     8.202299815160e-5
free-gapless held-out relative SSE 3.413835000353e-5
positive-gap held-out relative SSE 3.543794756520e-5

fixed-z1 <= 1.25 free-gapless      FAIL
fixed-z1 < positive-gap             FAIL
```

The fixed-`z=1` prediction error is about `2.40` times the free-gapless score
and `2.31` times the positive-gap score.  Because all frozen checks were
conjunctive, the classification is rejected even though the fitted exponents
and scaled tail separately look `z=1`-like.

## Claim classification

**Proved inputs:** owner-once topology, exact charge conservation, translation
symmetry, response-momentum selection, and the sealed L4/L6/L8 controls.

**Adopted:** the sharp-sector `rho=1/4` diagnostic, response channel, Krylov
tolerances, fit families, held-out score, and conjunctive pass rule.

**Empirical/numerically certified after final hostile audit:** the L10/L12
rows, finite-window exponents, scaled observables, model scores, and rejected
classification.

**Open/not computed:** an exact or thermodynamic dynamic exponent, a critical
phase or density, authenticated accumulation selection, native Poincare or
Virasoro generators, anomaly, continuum behavior, universal coupling,
emergence, and gravity.

No grid, graviton, Ward axiom, continuum assumption, Gate B, emergence, or
gravity claim is introduced.
