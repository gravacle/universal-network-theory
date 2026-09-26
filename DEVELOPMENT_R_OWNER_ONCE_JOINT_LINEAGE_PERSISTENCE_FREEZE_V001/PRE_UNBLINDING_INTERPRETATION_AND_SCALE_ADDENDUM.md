# Pre-unblinding interpretation and scale addendum V001

Addendum time (UTC): `2026-09-25T12:12:25Z`

Status:
`FROZEN_POST_HOSTILE_COMPUTATION__PRE_UNBLINDING__TARGET_OUTPUT_PENDING`

This addendum supplements, but does not alter, the criterion in
`BLINDED_SECONDARY_ANALYSIS_FREEZE.md`.  At this addendum time the hostile
branch had published an atomic result, the target branch had not published an
atomic result, and this authoring workflow had not opened either branch's
held-out L10/L12 witness values.

## 1. Interpretation of a miss below the frozen floor

The no-decline criterion remains the exact pair of inequalities

```text
D_lower(10) >= 0.001963064475535806
D_lower(12) >= 0.001963064475535806.
```

There is no rounding allowance, near-pass band, or post-output tolerance.  If
either resolved lower value is positive but below the frozen floor, report:

> The resolved positive witness persists at the held-out sizes but fails the
> frozen no-decline criterion.  That failure is not, by itself, evidence of
> finite-size collapse or disappearance.

The original held-out protocol retains authority over its own classification.
An unresolved value, failed numerical or custody control, or failure of the
original held-out reproduction rule may not be redescribed as a narrow miss.

## 2. Dimensionless positive-association scale

For sharp sector `q`, put `theta_(L,q)=q/L`.  The largest possible positive
site-averaged covariance in that sector is

```text
b_(L,q) = theta_(L,q) * (1 - theta_(L,q)).
```

To see this, write `a_e = Pr(F_e=1 | q)`.  For Bernoulli variables,
`Cov(F_e,n_e) <= a_e(1-a_e)`.  Because `sum_e a_e=q`, concavity gives

```text
(1/L) * sum_e Cov(F_e,n_e) <= (q/L) * (1-q/L).
```

The bound is attainable by a uniform distribution over `q`-element lineage
sets with the carrier occupying the matching first-rail sites.  Therefore,
for the observed sector weights `p_(L,q)`, define the exact sector-weighted
positive capacity

```text
B_L = sum_q p_(L,q) * (q/L) * (1-q/L)
eta_L = D_L / B_L.
```

`eta_L` is the fraction of the largest positive witness compatible with the
same sharp-sector weights.  It is a reporting scale only.  It does not replace
`D_L`, `tau_L`, `T_L`, the frozen floor, or any protocol classification, and it
does not by itself measure macroscopic physical importance.

Using the already reconciled seed-sector weights gives:

| L | `D_L` | `B_L` | `eta_L` |
|---:|---:|---:|---:|
| 4 | 0.025544765930507966 | 0.1950938980342479 | 0.13093575036377453 |
| 6 | 0.0018321913827511092 | 0.21317212330561375 | 0.008594892025935268 |
| 8 | 0.001963064475535806 | 0.22094482705933932 | 0.008884862803366672 |

Thus the raw L6-to-L8 increase is about `7.14298%`, while the increase after
normalizing by the sector-weighted positive capacity is about `3.37376%`.
The local increase is evidence against a simple monotone-decay account over
that one interval.  It does not, by itself, reject every finite-size or
write-together-residue explanation, particularly because L4-to-L6 decreased
substantially.  L10 and L12 remain the held-out test.

## 3. Null-model boundary

The existing sector-matched sham is already a static same-marginal null: it
preserves the separate within-sector lineage and carrier marginals and removes
their joint association.  A transport-scrambled or autonomous revisit null
would answer a different, dynamical question.  It is not part of this
secondary criterion and would require a separate pre-output protocol before
its result is computed.
