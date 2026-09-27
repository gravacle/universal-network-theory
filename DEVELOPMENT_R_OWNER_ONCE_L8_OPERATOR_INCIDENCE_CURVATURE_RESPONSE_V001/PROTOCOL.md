# Prospective L8 operator-incidence curvature/response protocol V001

Date frozen: 2026-09-26

Status: `FROZEN_IMPLEMENTATION_CANDIDATE__NO_L8_RESPONSE_OPENED`

## 1. Question and scope

At the completed owner-once `L=8` checkpoint, is the eventwise difference
between actual and same-`q`-product admission-edge Ollivier--Ricci curvature
associated with the independently computed eventwise autonomous carrier
response?

This is a finite construction test.  Pass, fail, and unresolved outcomes are
retained under the same rules.  No outcome is spacetime Ricci curvature,
geometry, a scaling law, RGRL/WTC response, or gravity.

## 2. Support recovered from primitive generators

Let `F_e` be the spent-lineage occupation for event `e` and let `C_u` be the
carrier occupation at prism vertex `u`.  The support has `3L` vertices,

```text
F_0,...,F_(L-1), C_0,...,C_(2L-1),
```

and only these edges:

1. `F_e--C_e` for each reversible admission generator `K_rel(e)`;
2. `C_u--C_v` for each hopping term of the fixed degree-three periodic prism
   transport generator `H_T`.

This is the minimal two-factor support of the displayed primitive generators:
each off-diagonal monomial changes exactly the named pair, so deleting its
edge loses generator support; adding another edge has no primitive monomial.
The graph is therefore recovered before any response value is read.  Its
metric cost is unit shortest-path distance on this fixed, unpruned support.

## 3. Conductance from generator squares

For each support edge `a`, use `g_a=<K_a^2>` at the frozen checkpoint.  In the
occupation basis this is exactly

```text
g(C_u,C_v) = P(n_u XOR n_v),
g(F_e,C_e) = P(F_e = n_e).
```

Here `F_e=0` is loaded/unspent and `F_e=1` is spent.  The admission equality
contains the two reversible support states `(loaded,blank)` and
`(spent,occupied)`.

Construct the control independently within every sharp carrier-number sector:

```text
rho_P = sum_q rho^F_q tensor rho^C_q / p_q.
```

Only diagonal expectations of `K_a^2` are required.  Hence the same-`q`
product conductance is computed exactly from the sectorwise lineage and
carrier diagonal marginals.  Transport conductances must agree between actual
and product arms because the complete carrier marginal is preserved; this is
a mandatory control, not a fitted condition.

## 4. Weighted lazy Ollivier--Ricci convention

Freeze idleness `alpha=1/2`.  For vertex `x`, put the remaining mass on fixed
support neighbors in proportion to conductance:

```text
m_x(x)=1/2,
m_x(y)= (1/2) g_xy / sum_(z~x) g_xz.
```

Zero individual conductance is permitted, but zero total weighted degree is a
control failure.  For every fixed support edge `{x,y}`,

```text
kappa_xy = 1 - W_1(m_x,m_y),
```

because its fixed metric length is one.  `W_1` uses unit shortest-path cost.
The target implementation uses a complete-metric transportation min-cost
flow; an independently coded graph-transshipment min-cost-flow control must
agree within `1e-11` on every edge in both arms.

## 5. Predictor and response fixed before L8 output

The eight-entry primary predictor is

```text
X_e = kappa_A(F_e,C_e) - kappa_P(F_e,C_e),  e=0,...,7.
```

No carrier node, selected subset, absolute-value transform, sign flip,
normalization, or alternate curvature convention may replace it after the
response is opened.

The response input must be a sealed JSON object with schema
`L8_ALL_EVENT_AUTONOMOUS_LINEAGE_RESPONSE_V001`, labels exactly `0,...,7`,
and response definition
`POST_TRANSPORT_CARRIER_CONFIGURATION_TV_ACTUAL_VS_SAME_Q_PRODUCT`.  Its fixed
vector is `carrier_configuration_tv_by_event`.  The canonical JSON payload
excluding `seal` must match the embedded SHA-256.  Any other size, observable,
label order, missing provenance, nonfinite entry, or out-of-range TV value
fails before analysis.

## 6. Statistic, controlled null, and disposition

Use Spearman midrank correlation.  Enumerate all `8!=40320` response-label
permutations while holding the graph and predictor fixed.  With comparison
guard `1e-12`, define

```text
p_abs = #{pi: |rho(X,Y_pi)| >= |rho(X,Y)|}/40320.
```

Also report directional tails.  This exhaustive label permutation is the
controlled null.  Report product-arm admission curvature correlation as a
secondary control, never as a rescue statistic.

If all controls pass, classify:

- `RESOLVED_L8_OPERATOR_INCIDENCE_CURVATURE_RESPONSE_ASSOCIATION` iff
  `|rho|>=0.5` and `p_abs<=0.05`;
- `NO_RESOLVED_L8_OPERATOR_INCIDENCE_CURVATURE_RESPONSE_ASSOCIATION` otherwise.

Custody, source, normalization, support, weighted-degree, transport-control,
solver-agreement, zero-variance, nonfinite, or runtime failures return
`L8_OPERATOR_INCIDENCE_CURVATURE_RESPONSE_UNRESOLVED` and publish no partial
result.

## 7. Runtime and restart boundary

Source review, synthetic tests, and the L4 development check are short jobs
and need no checkpoint machinery.  Production L8 conductance extraction is a
single read-only pass over authenticated terminal shards plus the already
specified final transport.  Its conservative budget is 30 minutes and 2 GiB
RSS.  The smallest valid restart unit is that extraction; it emits only one
atomic compact JSON, so interruption loses at most that pass.  The final
curvature/response join is expected below one minute and is rerun from the
two sealed compact adapters after interruption.

No worker farm, daemon, incremental numerical result, or bespoke resume layer
is introduced.  A computation exceeding the long-run threshold must be
re-estimated and checkpointed before any later expansion beyond this packet.

## 8. Claim ceiling

A pass establishes an association at L8 for this exact operator-incidence
support, conductance checkpoint, same-`q` control, curvature convention, and
response.  It does not establish causation, size persistence, a continuum,
spacetime curvature, metric dynamics, RGRL/WTC response, or gravity.  A null
rejects only this fixed construction.
