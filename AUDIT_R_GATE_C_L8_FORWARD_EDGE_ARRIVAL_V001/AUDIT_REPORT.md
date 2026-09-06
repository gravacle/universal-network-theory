# Independent hostile audit report

## Disposition

**PASS, 52/52.** No material discrepancy was found in custody, topology,
directed-edge orientation, write authentication, numerical values, trend
status, or claim boundaries. No L greater than 8 was run.

Target and immutable antecedent SHA-256 values are pinned in
`INDEPENDENT_RESULT.json`. The audit solver is independent of the target: it
uses a norm-preserving fourth-order Suzuki--Yoshida edge-factorization, while
the target uses an order-ten Taylor polynomial. Both coarse and fine runs are
performed separately.

Audit runtime was `9.371861917 s`; maximum RSS was `29,982,720 bytes` on the
recorded 48 GB environment. A separate target replay passed `14/14` in
`16.517954084 s` with `31,703,040 bytes` maximum RSS.

## Custody and exact controls

The independently reconstructed support has 16 sites, 24 distinct owner-once
edges, eight connectors, degree three at every site, and graph distance four
from probe node zero to target node four. The selected oriented edge is
exactly owner edge index three, `3 -> 4` on Rail 1. Rail wraparound edge
`7 -> 0` remains present.

The complete zero-through-four-particle reachable sector has dimension 2,517
inside the 65,536-word space. Each of the eight `B0/P0` through `B3/P3`
terms-off write ledgers is exact:

```text
Delta Q = k/2,  edge flux = 0,  total W_R = k/2,
Delta Q + edge flux - total W_R = 0.
```

Fine norm and retained-number errors are `1.837e-12` and `4.425e-12`.
Fine energy drift over `2*pi` is `5.917e-12`. The product formula's coarse
energy drift is `1.306e-10`, still well inside the audit control.

## Independent forward-edge observations

| N | independent `tau_fwd` | peak `delta J_3->4` | `delta q4(tau_fwd)` | tau target error |
|---:|---:|---:|---:|---:|
| 0 | `1.1689248233321285` | `0.0031013425481132262` | `0.0010580240013809696` | `1.138e-10` |
| 1 | `1.349957618520621` | `0.0054861224548746245` | `0.0015577475582251776` | `8.459e-11` |
| 2 | `2.616413582161456` | `0.08678470625746924` | `0.06950833751780286` | `2.475e-11` |
| 3 | `2.4653208228722225` | `0.044181800613942876` | `0.060647167516033634` | `8.028e-11` |

Maximum target errors are `1.138e-10` for time, `2.964e-12` for peak directed
current, and `4.257e-12` for interpolated node-four contrast. Maximum audit
coarse/fine differences are `4.089e-6`, `8.130e-9`, and `4.251e-7`
respectively.

The result is not strictly monotone. In particular,

```text
tau_fwd(2) - tau_fwd(3) = 0.1510927592892335 > 0.
```

That separation is more than four orders of magnitude larger than the maximum
coarse/fine timing difference, so the `N=3 < N=2` inversion survives the
independent solver and refinement control.

## Hostile claim gates

The observable is an instantaneous ensemble contrast on the final oriented
edge into node four. Option A selects that final-edge inflow, but the original
prism and its counter-clockwise wraparound route are unchanged. The selected
edge does not reveal which earlier route contributed to its current.

Background subtraction contrasts two coherent ensemble histories. It is not
an individual carrier tag and supplies no individual lineage transit.

The measured peak time is a finite operational graph diagnostic. With no
physical metric, clock, or geodesic map, it cannot be promoted to metric
strain, gravitational time dilation, Shapiro delay, or gravity. Other edges,
clusters, phases, peak rules, an open-boundary control, physical metric/clock,
Gate R-C, and Gate A-P remain open.

## Claim classes

**Proved:** unchanged owner-once L8 prism, directed edge custody, and exact
authenticated terms-off write ledgers.

**Adopted:** Option A, common phase, background subtraction, bounded search
window, and first-positive-peak rule.

**Conditional:** all-blank parent, finite numerical evolution, and ensemble
difference.

**Empirical:** finite `N=0..3` forward-edge peak times and amplitudes, including
the independently reproduced `N=3 < N=2` inversion.

**Open:** alternative controls and supports, individual route or lineage,
physical metric or clock, Gate R-C, and Gate A-P.

## Discrepancies

None material. The audit's split formula has larger coarse energy drift than
the target Taylor method, but its fine conservation, solver agreement, and
coarse/fine controls are all comfortably within the hostile thresholds.
