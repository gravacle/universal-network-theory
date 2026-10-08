# Frontier V022 — fixed coefficients, shared records, and actual formed-state response

2026-09-27. Additive BS-parent advance; the H6 matched-dephasing work in
V021 remains a separate parent. The research objective continues.

## Verified fixed-coefficient formation

The new balanced channel uses fixed U=1, Delta=6, lambda_R=2,
epsilon_r=1, d_star=7/4, g=0.1 and Omega=0.05, with native h=Omega/N.
Its endpoint graph cost +1 and storage cost +1 are paid by feedback -2.
An independent exact two-block derivation gives formation failure O(N^-2)
at time O(N). The N=1 instance is a full native single-edge sector;
N>1 four-state calculations are isolated-channel diagnostics, not claims
that all other graph links can be frozen in a native slab.

The frozen numerical check verified 1,070 identities across seven isolated
channels and the full 32-state N=2 competition model. Maximum difference
between independent calculations was 4.543e-12. Measured peak self RSS was
33,144,832 bytes; all eight cases have separate durable, hashed receipts.
No larger calculation, package installation, or infrastructure change occurred.

For N=1 the joint formation probability is 0.99975874455, measured copying-off
work is 9.031852497e-6, and the analytical all-time joint hold failure bound
is 0.01323332. For isolated N=64 the corresponding values are
0.99999978056, 8.440057424e-9, and 4.129071143e-6. The actual imperfect
endpoint is held; it is not silently replaced by the ideal target state.

Evidence: `fixed_coefficient_formation/PROTOCOL.md`, `FROZEN.json`,
`compute.py`, `RESULTS.json`, and individual case receipts. Source SHA-256:
`180bd1ba57f076f102df8380d111d4f361ed30c9f5a573165cb404e3875040fa`.
Freeze SHA-256:
`09895bcff7600d1fe3f1b8c0924a86e15dbf8017335a3184458d7fc84500a9ed`.
The pre-run independent review found no formula/indexing blocker. Its
qualification that float acceptance used 1e-9 even for exact assembly
identities is retained; those assembly residuals in fact equal zero.

## Connected growth has an explicit, testable competition

With lambda_R=2U and epsilon_r=a+2U, the full diagonal ledger is exactly

    H_diag-E_empty = a(Q-M)+2U R,

where R is the nonnegative shared-degree expression in
`NATIVE_OVERLAPPING_RECORD_PAID_FORMATION_V001.md`. Shared-record paths
and occupied cycles with Q=M,R=0 have the same diagonal energy as the
empty configuration at fixed coefficients. This is an overlapping-network
result, not a sum of independent record cells.

Both an occupied path tip and an unused blank donor can pay for the next
record/link. A frozen-background star makes them exactly equivalent.
The full N=2 calculation retains all four possible link flips and resolves
the actual competition:

| Predeclared time | Connected append | Separate seed | Background-row departure |
| --- | ---: | ---: | ---: |
| T/2 | 0.384294 | 0.391135 | 0.017024 |
| T | 0.282253 | 0.314560 | 0.051559 |
| 2T | 0.551894 | 0.290093 | 0.081856 |

Here T=323.0882195 is the prospectively selected isolated N=2 beat time,
not an optimized full-network time. Thus the background's own dynamics
breaks the conditional-star symmetry and can reverse the preference.
The useful question is how to control and scale this real selection
mechanism, not whether an isolated energy resonance guarantees a path.

An independent exact generic-polynomial implementation additionally passed
78 exact checks, with no floating-point tolerance. For tau=t/hbar it confirms

    P_append-P_seed = -(2/3) U^2 g^2 h^4 tau^8 + O(tau^10).

The earlier powers cancel. This checks the hand-derived moment differences
40Ugh^3 at order five and 320U^2gh^3 at order six. It predicts the earliest
contrast only, consistent with the later reversal above.
Evidence: `fixed_coefficient_formation/exact_competition_audit.py` and
`EXACT_COMPETITION_AUDIT.json`. Audit source SHA-256:
`779d4cdd0f328c6eab89d1878ca46c1b86a182da696303a06dcdf40757d8ca46`.

## From formation to independently meaningful response

`NATIVE_FORMED_NETWORK_RESPONSE_BRIDGE_V001.md` and
`NATIVE_FORMED_RESPONSE_NOISE_AND_PROBE_V001.md` derive the response of the
actual earlier exact one-link formation endpoint, not an assumed ground
state. Its formation age, unforced leakage L and frequency omega_0 jointly
fix detuning response, record insertion-work coefficients, fresh-carrier
transfer curvature and noise. Independent analytical review found no
blocker in the primary bridge.

The phase-mixed preparation predicts without a fitted response amplitude

    hbar omega_0 chi_bar(0) = (L/2) sqrt(1-L).

For the actual freshly formed endpoint, immediate occupation-kick response
is zero while fresh-carrier curvature is maximal. A persistent detuning
starts at order t^4, and differentiating a family of re-prepared phase
mixtures gives twice the fixed-state static susceptibility. These are
different specified experiments, not contradictory response formulas.

For a formed many-link state the same full response matrix chi_ef supplies
both local record-cost and fresh-carrier-curvature responses through its
incidence projection. Its uniform projection supplies the response of total
incidence. The next small test will instantiate these identities in an
actually formed shared-record state, retaining its copying-off work and
all native link flips. Total incidence is not silently renamed physical
volume: operational geometry remains part of the constructive bridge.

The new conditional-star collective asymptotic argument is undergoing
independent review; it is not yet promoted here. This frontier reports a
completed formation/competition check and analytical response predictions,
not a completed dark-matter/dark-energy observational result.
