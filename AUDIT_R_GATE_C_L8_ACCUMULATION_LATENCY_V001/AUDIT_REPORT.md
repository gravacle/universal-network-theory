# Independent hostile audit report

## Disposition

**PASS, 59/59.** No material numerical, topology, conservation, fit, or
claim-boundary discrepancy was found. Target and immutable antecedent hashes
are pinned in `INDEPENDENT_RESULT.json`. No L greater than 8 was run.

The independent audit uses a norm-preserving fourth-order Suzuki--Yoshida
product formula over three exact eight-edge matchings. The target instead uses
a tenth-order direct Taylor polynomial. Both operate on the complete
zero-through-four-particle sector of dimension 2,517 inside the 65,536-word
space. Separate 1,024/2,048-step audit evolutions provide genuine coarse/fine
control.

Audit runtime was `9.714857250 s`; maximum RSS was `31,391,744 bytes` on the
recorded 48 GB environment. A separate target replay passed `17/17` in
`17.075226875 s` with `32,538,624 bytes` maximum RSS.

## Topology, writes, and histories

The independently reconstructed support has 16 sites, 24 owner-once edges,
eight connectors, degree three at every site, and graph distance four from
probe node zero to target node four. Even rail edges, odd rail edges, and
connectors form three disjoint perfect matchings whose union is the full edge
set.

All eight histories `B0/P0` through `B3/P3` begin from the declared all-blank
parent. Every terms-off write ledger is exact:

```text
Delta Q = k/2,  edge flux = 0,  total W_R = k/2,
Delta Q + edge flux - total W_R = 0.
```

The eight complete transport-ledger L1 residuals are at most `1.311e-10`.
The four background-subtracted probe-ledger L1 residuals are at most
`1.329e-10`. Maximum capacity energy drift is `9.608e-12`; capacity and search
norm errors are `4.375e-13` and `1.837e-12` respectively.

## Complete finite results

All 32 connector-vector components agree with the target within `8.215e-12`;
all 96 components of the complete background-subtracted current vectors agree
within `8.315e-12`. The full capacity-current coarse/fine difference is
`2.276e-10`.

| N | independent connector L1 | independent signed sum | independent tau | tau target error | peak |
|---:|---:|---:|---:|---:|---:|
| 0 | `0.4999999999893556` | `0.4999999999893556` | `1.2226898687332437` | `1.212e-10` | `0.001092389289208868` |
| 1 | `0.42815973373462957` | `0.42815973373462957` | `1.3455677496386216` | `1.809e-10` | `0.0015579313219193597` |
| 2 | `0.36531361322715183` | `0.35636815242930525` | `2.9716009673233863` | `1.444e-11` | `0.10363914916445095` |
| 3 | `0.3308471281018145` | `0.32844405033570967` | `2.8614646859261184` | `5.885e-11` | `0.08531515936216011` |

The first-positive-peak rule was independently applied over `0<t<=2*pi`
with the fixed `1e-8` floor and parabolic vertex refinement. Maximum audit
coarse/fine tau separation is `1.631e-5`; maximum target tau difference is
`1.809e-10`.

Connector L1 decreases strictly across `N=0..3`. Operational latency does not:
it increases through `N=2` and then decreases at `N=3`.

The independently fitted line is

```text
J(N) = 0.4916258291887531 - 0.057030473617010115 N
R^2 = 0.9778724186808181
formal zero = 8.620405863894474
```

This agrees with the target within the distinct solver's numerical control.

## Hostile claim gates

The L8 rail has at most six distinct background sites after reserving the
probe and target. The fitted zero at about `8.6204` is outside that finite
capacity. It is therefore a formal extrapolation only: `Ncrit` is undefined
and pinch-off is unmeasured.

The measured `tau` is the first positive local maximum of a background-
subtracted occupation signal on a finite graph. There is no physical metric,
clock, geodesic map, or individual carrier tag. It cannot be promoted to
metric strain, time dilation, Shapiro delay, or gravity. Background
subtraction is an operational ensemble contrast, not individual-lineage
transit.

**Proved:** finite owner-once prism census, exact authenticated write ledgers,
and the declared subtraction identities.

**Adopted:** `alpha=r0`, the bounded time windows, canonical cluster, and
first-positive-peak rule.

**Conditional:** the all-blank parent, common phase, background subtraction,
and finite numerical representation.

**Empirical:** the four capacity and transit rows, decreasing capacity over
`N=0..3`, nonmonotone latency, and the inadmissible fitted zero.

**Open:** other clusters, phases, rules, windows, larger `N` and `L`,
individual lineage, a physical metric or clock, `Ncrit`, pinch-off, Gate R-C,
and Gate A-P.

## Discrepancies

None material. The independent product formula has a larger energy drift than
the target Taylor solver (`9.608e-12` versus about `4.9e-15`), but its unitary
coarse/fine controls, conservation remainders, and complete-vector agreement
are all well inside the audit thresholds.
