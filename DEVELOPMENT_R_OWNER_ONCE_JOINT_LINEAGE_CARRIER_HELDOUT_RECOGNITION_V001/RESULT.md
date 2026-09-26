# Recognized result

Disposition:

```text
COMPUTATIONAL EVIDENCE:
  VALID_INDEPENDENTLY_REPRODUCED_FINITE_L10_L12_ASSOCIATION

STRICT ORIGINAL PROTOCOL:
  NOT_CLAIMED_AS_FORMALLY_PASSED__RELEASE_SKEW_DEVIATION

SECONDARY SIGNED PERSISTENCE:
  FAIL__SIGN_REVERSAL_AND_MAGNITUDE_DECLINE_AT_L10_AND_L12
```

## Independently recomputed values

| L | target `D_L` | hostile `D_L` | absolute disagreement | `d_L` | `r_L` | `tau_L` | `T_L` | sector-capacity bound `B_L` | normalized `eta_L=D_L/B_L` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | `-0.0003118488593728413` | `-0.00031184885937283205` | `9.269928574751063e-18` | `3.552713678800501e-15` | `3.9968028886505635e-15` | `1e-9` | `311848.8593728413` | `0.22714282661304128` | `-0.0013729196912042685` |
| 12 | `-0.00003236588485223031` | `-0.000032365884852249583` | `1.927169361592984e-17` | `2.4424906541753444e-15` | `1.0658141036401503e-14` | `1e-9` | `32365.88485223031` | `0.23119534505251413` | `-0.0001399936700493631` |

Here `B_L = sum_q p_q (q/L)(1-q/L)` is the sharp-sector-weighted
largest absolute covariance available to this registered witness.  Thus the
finite association is extremely well resolved numerically, while occupying
about `0.137%` of its capacity at L10 and `0.0140%` at L12 (with negative
sign).  Numerical resolution and physical effect size are distinct claims.

The conservative two-size statistic is
`T_10:12 = 32365.88485223031 > 1`. All target-internal,
hostile-internal, row/column, and target/hostile comparison controls pass.
This is why the computational result is recognized despite the separately
disclosed procedural deviation.

## Signed no-decline prediction

The pre-unblinding secondary rule required the signed conservative lower value
to remain at or above positive `D8 = 0.001963064475535806` at both held-out
sizes. Instead:

| L | signed lower value | fraction of `|D8|` | positive-floor pass |
|---:|---:|---:|:---:|
| 10 | `-0.00031184985937284134` | `0.15885818487328296` | no |
| 12 | `-0.000032366884852249586` | `0.01648742833237622` | no |

The association therefore remains numerically resolved but changes sign and
declines in magnitude by about `84.11%` at L10 and `98.35%` at L12 relative
to L8. This falsifies the frozen positive no-decline criterion. It does not
make the exact finite computations invalid, and it does not by itself prove a
particular asymptotic law.

## Timing adjudication

The observed launch-proxy gap was `10,748 s`, exceeding the frozen `60 s`
maximum by `10,688 s`. That rule protected blinding; it did not enter the
Hamiltonian, event schedule, checkpoint, witness, or arithmetic. Neither final
value existed at either launch, the target was already running before the
hostile launch, both branches retained source/value isolation, and their
atomic answers agree independently. The deviation blocks an unqualified claim
that every operational clause of the original protocol was followed, but it
does not invalidate the deterministic numerical evidence.
