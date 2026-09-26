# Owner-once joint lineage--carrier persistence freeze V001

Freeze time (UTC): `2026-09-25T11:55:29Z`

Status:
`FROZEN_POST_HOSTILE_COMPUTATION__PRE_UNBLINDING__TARGET_OUTPUT_PENDING`

## 1. Relationship to the original held-out protocol

This is a new, secondary analysis rule. It does not amend, replace, rescue, or
change the classification in the previously frozen exact L10/L12 held-out
protocol. The original held-out result must be reconciled and classified by
its unchanged rules before this secondary criterion is evaluated.

At this freeze time:

- the hostile branch had published one atomic L10/L12 result file;
- the target branch had not published an atomic result file;
- this authoring workflow had not opened, parsed, displayed, or used any
  hostile or target L10/L12 witness value; and
- no intermediate L10 or L12 scientific value had been published by either
  atomic all-or-nothing orchestrator.

Only the existence of the hostile atomic path and the absence of the target
atomic path were checked while making this record. Accordingly, this record is
a **post-computation, pre-unblinding secondary-analysis freeze**, not part of
the original preregistration. The non-observation declaration applies to this
authoring workflow; it does not claim knowledge of every person's actions.

## 2. Frozen persistence floor

The independently reconciled seed values available before this freeze are

```text
D_6 = 0.0018321913827511092
D_8 = 0.001963064475535806
D_8 / D_6 = 1.0714298156932632097...
```

Thus the published L6-to-L8 step is an increase, not a decay. No decaying
L6-to-L8 trend exists to extrapolate. The frozen floor is therefore the last
seed-size value itself:

```text
f = 0.001963064475535806
```

This choice permits no held-out decline below the L8 site-averaged witness.
It is deliberately stronger than merely requiring a nonzero resolved value.

For each `L in {10,12}`, define the conservative resolved lower value

```text
D_lower(L) = min(D_target(L), D_hostile(L)) - tau_L.
```

The secondary persistence criterion passes if and only if all original
held-out numerical, custody, and reconciliation controls pass and

```text
D_lower(10) >= 0.001963064475535806
D_lower(12) >= 0.001963064475535806
```

The signed positive value is required; an absolute-value substitution is not
allowed. No alternate floor, fitted exponent, monotonicity rescue, selected
sector, or post-output tolerance may replace this rule.

A pass licenses only this statement:

> The resolved site-averaged lineage--carrier witness did not fall below its
> L8 seed value at L10 or L12; no finite-size collapse occurred through L12
> under this frozen persistence criterion.

A failure of either inequality is a failure of this secondary persistence
criterion even if the original held-out resolved-witness classification
passes. Neither outcome establishes an all-L or thermodynamic limit.

## 3. Frozen immediate lineage-response corollary

For a dynamical comparison, remove cross-charge-sector coherence in both arms:

```text
rho_bar = sum_q Pi_q rho Pi_q
sigma   = sum_(q:p_q>0) (rho^S_q tensor rho^C_q) / p_q.
```

Both states have the same charge-sector weights and the same separate
within-sector lineage and carrier marginals. `sigma` removes their
within-sector joint association. Comparing coherent `rho` directly with
block-diagonal `sigma` is forbidden because it would confound association
removal with charge-sector dephasing.

Let `U_e` be one complete bidirectional relational admission pulse at site
`e`, with the already declared angle `phi = pi/4`. Let `Q_C` be total carrier
charge. Freeze the carrier-only response battery

```text
Y_L = (1/L) sum_e [
        Tr(Q_C^2 U_e rho_bar U_e^dagger)
      - Tr(Q_C^2 U_e sigma   U_e^dagger)
      ].
```

The exact admission algebra gives

```text
Y_L = D_L
```

at `phi = pi/4`. Therefore the frozen response margin is

```text
delta = 0.001963064475535806.
```

Subject to the same conservative resolution rule, the immediate response
criterion is `Y_L >= delta` at both L10 and L12. This proves that the declared
lineage-reading admission pulse can transduce the stored joint association
into a carrier charge-variance response not fixed by the carrier marginal
alone.

This response identity is an analytic corollary of `D_L`, not statistically
or dynamically independent evidence. It does not establish that a fixed
autonomous revisit-and-transport continuation produces a later occupation,
current, or transport difference. Such a continuation requires a separate
pre-output protocol with its exact schedule, comparator, carrier observable,
and effect-size rule frozen before any response output is computed.

## 4. Claim boundary

Neither criterion proves persistence beyond L12, an infinite-size limit,
geometry, the Record--Geometry Realization Law, Einstein--Hilbert response,
Newton's constant, or gravity. A persistence pass plus the immediate response
identity supplies a finite microscopic record-conditioned-response premise
for a later geometry-response theorem.
