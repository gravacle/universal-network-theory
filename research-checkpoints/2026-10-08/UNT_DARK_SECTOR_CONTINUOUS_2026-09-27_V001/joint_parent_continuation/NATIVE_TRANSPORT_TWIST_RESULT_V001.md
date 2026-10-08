# Native transport work depends on retained correlations

2026-09-29. Completed saved-state calculation and independent audit. No new
formation, eigensolve, larger lattice, physical calibration or observational
fit. This is an additive result, not a replacement of the gravity parent.

## Result

The actual formed native state has a nonzero carrier-phase energy response
that disappears if the joint incidence/carrier expectation is factorized.
At the five retained ages, the contact D=t<nT> is:

| Held age | D | Transfer current j=t<nJ> |
| ---: | ---: | ---: |
| 0 | 0.04600676445 | 0.11183038467 |
| 0.25 | 0.07726155785 | 0.13750286187 |
| 0.5 | 0.10151556691 | 0.12801801787 |
| 1 | 0.08470676783 | 0.02606213495 |
| 2 | -0.05676535704 | 0.06998582861 |

The separate-average substitute t<n><T> is numerically zero at every actual
age (all 15 preparation/age values below 5.5e-17 in magnitude). The held
Hamiltonian conserves <T>, but not the correlated <nT>. Thus separate link
occupancy and carrier coherence do not determine this response. The native
complete held energy is conserved at 4.12798401232428.

The response is not unique to the record-feedback preparation. Both retained
controls also have nonzero correlated contacts. Feedback-off and copying-off
have equal contact/current histories to roundoff while their total energies
and records differ; they are not a Hamiltonian/energy-matched proof of a
record-only cause. Formal total-record dephasing leaves this particular
transport channel unchanged. The distinct writer/record-clock channel must
not be conflated with it.

## What was measured

For a dimensionless carrier-link phase phi at a fixed actual state,

    H(phi)=H+t*n[T*(1-cos(phi))-J*sin(phi)],
    E(phi)-E(0)=D*(1-cos(phi))-j*sin(phi).

The same phase applied to the state at fixed H has the opposite linear-work
sign. Both source and state experiments were retained with their complete
energy ledger. The current-square term and other nonhopping terms were not
discarded. All 15 actual states, six synthetic controls and six prescribed
angles per state were evaluated; no sign or history contrast was selected
as a success criterion.

The negative native contact at age 2 is curvature about a current-carrying
state, not by itself an equilibrium instability. Nor is a positive contact
a relaxed stiffness: this single-edge Hamiltonian phase is a pure gauge,
and transforming source and state together leaves every energy unchanged.
The state/current response must accompany the instantaneous contact.

## Connection to the gravity question

The independently reviewed finite-gap gravitational interface identifies
relative motion between the hard phase and the preferred clock as a specific
transport question. A separately declared candidate spatial term has a
dimensionless coefficient alpha. In the stated positive-kinetic local
constant-kernel regime, its potential determinant is alpha-1. Alpha=1 removes
that local negative direction, leaving ordinary phase pressure and a neutral
clock direction; it does not establish global or nonlinear stability.

That coefficient is NOT the contact D above. Relating them requires the same
state's temporal/current response, canonical phase normalization and physical
geometry/volume mapping. The native carrier phase is not automatically the
record phase or the candidate hard collective phase. The exact held local
record-occupation phase has zero twist energy. These concrete distinctions
specify the next source-response matching; no extra term has been inserted
to force a preferred outcome.

## Qualification and evidence

All 3,110 numerical controls and 959 independent saved-data arithmetic
comparisons pass. The latter independently contracts the three original
age-zero vectors and recombines all 126 angle readouts; it does not claim a
second independent propagation of later ages. Runtime was 0.0286731 seconds,
peak self RSS 33,931,264 bytes. The sole numerical worker has exited.

The nine-member freeze and inherited evidence authenticate. The published
388,727-byte raw JSON exactly matches the compressed stdout transport.

- Result: NATIVE_TRANSPORT_TWIST_V001_RESULTS.json,
  SHA-256 9f29e3d5083d5a03b2e02dca62c2dd90041fa1303a573c55e5a73ed5545775d3.
- Freeze: NATIVE_TRANSPORT_TWIST_V001_FROZEN.json,
  SHA-256 1f511788e25dbdf203355f1f0b3de0861d09c4a7e07fe80eab544d15f55a5330.
- Independent result review: NATIVE_TRANSPORT_TWIST_V001_RESULTS_REVIEW.md,
  SHA-256 4991e72c2b30f5b864ef38d522ae93ddabb3f2952f7551e23aa61b7b917a955a.
- Reproducible audit: native_transport_twist_saved_audit_v001.py and
  NATIVE_TRANSPORT_TWIST_SAVED_AUDIT_V001.json.
- Candidate derivation: NATIVE_RELATIVE_PHASE_TRANSPORT_TEST_V001.md,
  SHA-256 6e9cc504ae81841c55d73c84f91239ce407e84455f11efc10a32ed8724d4b45a.
- Independent candidate review: RELATIVE_PHASE_TRANSPORT_INDEPENDENT_REVIEW_V001.md,
  SHA-256 bb3f091af3e57e9aa6f68b83fdc78807c8bef1d809ba26a3cc78179d96d08994.

Next: derive the complete gauge-covariant, nonstationary source-response
identity and its physical matching, not another formation rerun. The wider
joint dark-sector program is not declared complete by this finite-cell result.
