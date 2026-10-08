# Frontier V051 — finite-gap shared calibration and variable galaxy state

2026-09-29. Actual local science continued after V050. The user's renewed
unattended-work request is implemented by an ACTIVE same-chat heartbeat,
`unt-dark-sector-autonomous-continuation`, every two minutes. This is a
continuation cadence, not a calculation deadline. See
`AUTONOMOUS_CONTINUATION_STATUS_2026-09-29.md`. The other Mac remains finished;
no successor was queued there.

## Completed finite-gap screen

The local worker has completed all 360 prospective combinations: four owned
soft quadratures, 18 inherited cosmological reference alternatives and hard
gaps R={32,128,512,2048,8192}. Each is a newly declared scalar macroscopic
hard state with the SAME calibrated excitation energy, its own exact action,
and its own finite-R vacuum matching. It is not a relabeled finite-R pulse.
The exposed acceleration coefficient remains a calibration, not unused data.

All 80,076 producer controls and 10,080 independent saved-arithmetic comparisons
pass. Retained run time: 2.568623208 seconds; peak self RSS: 35,323,904 bytes.
This was small local arithmetic, not a memory-intensive galaxy simulation.

| Global hard gap | Cosmic-state static length, pc | Pressure/energy at A=1101 |
|---:|---:|---:|
| 32 | 959,652–1,057,046 | 0.333306–0.333310 |
| 128 | 3,766–4,153 | 0.332248–0.332381 |
| 512 | 14.713–16.222 | 0.293342–0.297840 |
| 2048 | 0.057472–0.063369 | 0.026208–0.031067 |
| 8192 | 0.000224498–0.000247534 | 0.000116535–0.000141661 |

These ranges retain all 72 reference/spectrum combinations per gap, not
independent experimental successes. They quantify a genuine common-state
tradeoff: the gap that makes the stipulated early history colder also changes
the present static response. Neither column is an observational acceptance
criterion. The length is an inverse Helmholtz wave number near the cosmic
state, NOT a halo radius or a prohibition on nonlinear galactic concentration.

At R=8192 the density linearization requires |Phi| much less than roughly
2e-13. It is not legitimate to extrapolate that tiny-background response
unchanged through a galaxy. Finite-field polarization and the solved local
action must replace it. The tiny finite-R shift S-S_infinity is only 14–20
floating-point steps at that gap; its displayed relative precision is not
certified and it is not the source of the pressure/contact/length result.

Read in `joint_parent_continuation/`:

- `FINITE_GAP_SHARED_SCREEN_PROTOCOL_V001.md` and
  `finite_gap_shared_screen_v002.py`.
- `FINITE_GAP_SHARED_SCREEN_V002_TRANSPORT.json`: lossless compressed complete
  result; decoded raw SHA-256
  `822dd216b33ff4ce08cdcd8b5f1ad5e3e27c583b7833107cef58b158cb3f9cc0`.
- `FINITE_GAP_SHARED_SCREEN_V002_REVIEW.md`: independent review, SHA-256
  `1e924814e6a804681afdf60c389c837d7be645556f05ef7e29737929db75ec18`.
- `FINITE_GAP_SHARED_SCREEN_V002_SAVED_AUDIT.json`: 10,080 comparisons, SHA-256
  `21f77467d89369f8ad64b8ebf1c3aec31bb11dfc6628b0cce2c4945c24f32915`.

The V001 launch refused a publisher-altered float literal before science.
The first V002 numerical launch lost output custody through a host orchestration
exception; after confirming no worker remained, the unchanged short calculation
was repeated to capture its output. Both incidents are explicitly preserved in
the launch-failure and output-recovery notes. No tolerances, scientific choices
or source formulas were altered to obtain success.

## Completed analytic consequences

`FINITE_GAP_CALIBRATION_STATIC_LENGTH_V001.md`, SHA-256
`e8c4622d1f86a97f63b24499e21c134100edcad5e30e74208503f4af3cd62d36`,
derives the exact same-state K0/J ratio and physical units, a conditional
cold-history upper bound and a useful static branch test. For a genuinely
specified zero-Dirichlet domain with positive source, an everywhere-attractive
weak-linear solution requires kJ^2 below the domain's lowest Laplace eigenvalue.
Do not invent or fit a box radius to satisfy it, or extend it to nonlinear
states that violate the linear-density approximation.

`COMMON_ACTION_GALAXY_BOUNDARY_AND_INITIAL_STATE_V001.md`, SHA-256
`2eb30bb54416d31a69109b1d48795789a208b2418bfb237cfd81a291ec006c26`,
identifies an exact local geodesic-clock branch of the full alpha=1 candidate:
GR coupled to the same barotropic network energy and matched vacuum, until
the normal-clock congruence develops a caustic. Cosmic abundance alone does
not select the different accelerated static branch. A closed baryon/network
initial-value transfer test is available, with an exact local two-fluid oracle;
its dynamic Jeans scale is not the aligned static K0/J scale. No arbitrary
halo radius, extra abundance or microscopic-GR-derivation prerequisite is added.
Root read both notes fully; peers independently checked their stated domains.

## User's galaxy-outskirts question and the active next calculation

The user explicitly asks whether changing network/gravitational density at
galactic outskirts is accounted for. The earlier force tables varied local
acceleration while holding their prepared actions fixed. The new BVP instead
uses F(N,g) with N*omega(I,h(g))=mu: the local action, intrinsic energy,
polarization and spatial gradients must be solved together. A homogeneous
cosmic reference is an outer-state datum, not an imposed uniform interior.
An arbitrarily prescribed I(r) is not automatically a conserved static solution.

The next inert worker/protocol is being prepared as
`finite_field_phase_response_v001.py` by the result-audit agent, with analytical
derivative review by the law and native-scope agents. Do not launch duplicate
work or assume it has run. The prospective local-material census uses the
R={128,8192} subset explicitly, all 72 reference/spectrum combinations, three
already exposed physical acceleration probes and illustrative lapse depths
Phi={0,-1e-8,-1e-7}. This is a constitutive comparison, not a galaxy fit or a
claim that these depths were measured.

It will solve the common-phase state rather than fixed I, compare those two
prescriptions at identical fields, and retain both local response eigenvalues,
including the phase-redistribution term B_I^2/e_II. The stable normalized
frequency-excess formula avoids subtracting order-one frequencies to resolve
the cold state's roughly 1e-13 shift. Legitimate empty states and branch loss
must be reported, not clipped to produce a favorable force. Finite-field
stiffness can differ greatly from the tiny cosmic K0; the completed screen
does not establish a no-go for galactic support.

Continue through this next small calculation and review without asking for
milestone approval. Longer numerical work still needs restartable state; small
jobs may be rerun after interruption. No numerical worker is active at the
publication of this frontier; analytical/code agents are preparing the next
one. All 56 original handoff members freshly match. No account reset, remote
dispatch, installation, L8 work, new arbitrary deadline or completed-dark-
program claim has been made.
