# Transport per native clock phase: source discrimination and intrinsic evolution

2026-10-03. One working derivation using the existing BS matrices. The A/B
laws remain proposed physical completions, not newly adopted laws. No source
function, acceleration history, astronomical scale or extra interaction is fit.

## 1. An exact finite-N source discriminator

Use the same prepared bounded-degree graph G, one carrier at u, blank records
and occupied fixed-content writers as the continuing-writer clock construction
in NATIVE_ACTIVE_RECORD_LOCALITY_AND_CLOCK_V001.md. Leave g_wr=g nonzero;
carrier-record and fragment copying are off. All actual incidence flips,
degree energy, feedback, carrier storage and current-square terms remain.
No static-incidence approximation is required for the following initial result.

The sender clock is its fixed dressed observable B_d with

    Delta_d=sqrt[(epsilon_r-lambda_R d_G(u))^2+4g^2],
    beta(0)=g/Delta_d,   nu_B(0)=Delta_d/hbar.

Use g>0 with the inherited orientation. Consider one initially occupied edge
u-v and a constant clamped q, f=exp(-q). The existing complete source laws are

    E_A(q)=f H_N,
    E_B(q)=H_N-T_N-E_b I+f T_N+E_b exp(3q) I,
    T_N=-t_hop sum n_e T_e+lambda_J sum n_e J_e^2,
    E_b=2N U_d d_*^2.

Here q is the logarithmic RULER source of the A/B note, whose proposed
V/V_N=exp(3q) is an additional embedding premise. It is not the differently
normalized log-V coordinate of the continuous-controller proposal.

For a carrier initially at u, the probability of finding it at v starts as

    P_v(s;q)=f^2 t_hop^2 s^2/hbar^2+O(s^4).

Only the initially occupied carrier hopping block contributes at this order.
Onsite terms do not move the carrier; a link flip followed by a hop enters
at a higher order. The initial clock rate is f Delta_d/hbar for A and
Delta_d/hbar for B. Define elapsed clock phase theta with theta(0)=0. Then

    K(q)=lim_(theta->0) P_v(theta;q)/theta^2,
    K_A(q)=t_hop^2/Delta_d^2,
    K_B(q)=exp(-2q)t_hop^2/Delta_d^2,
    partial_q log K_A=0,   partial_q log K_B=-2.

These are exact coefficients at FINITE N. For this real preparation, both
clamped Hamiltonians are real symmetric and B_d is real. Hence P_v(-s)=P_v(s),
beta(-s)=beta(s)* and the locally unwrapped theta(s) is odd with nonzero
initial derivative. This justifies O(theta^4), rather than discarding cubic
terms by assumption. Arbitrary complex preparations need not have this parity.

For A the entire relational curve is exactly q-independent wherever its clock
is invertible: the full state and clock are both evaluated at the same age fs.
For B only the initial coefficient is exact without a finite-window estimate.
On a prepared regular graph the carrier reference has
T_G=lambda_J d I-t_hop A_G, so its curve is

    P_v^A(theta)=|<v|exp(-i T_G theta/Delta_d)|u>|^2,
    P_v^B(theta)=|<v|exp(-i f T_G theta/Delta_d)|u>|^2.

The existing active-clock/locality estimates control the actual finite-window
comparison, with degree, q and observation window bounded independently of N.
The exact initial coefficient does not require extrapolating those estimates.
No group velocity, arrival threshold, continuum dispersion or photon has been
introduced. The readout distinguishes the proposals; simulating either
inserted proposal would not decide which source law nature realizes.

## 2. Complete source work and the scope of the test

For a classically prescribed q path, the work rates are

    Wdot_A=-qdot<E_A>,
    Wdot_B=qdot[-exp(-q)<T_N>+3E_b exp(3q)].

All expectations are in the actual state. The regular-graph lambda_J d I
term may drop out of position probabilities but not source energy or work.
Neither may the volume-dependent identity baseline be discarded. Clamping
and preparing identical states at different q require their own apparatus
and work; those preparations are not free cosmological initial conditions.

The previous 96D autonomous apparatus already separated A/B through recoil
and formation. Its operator q can be entangled with the network. Substituting
its mean q into an externally prescribed integral exp(-q(t)) is not exact.
This new coefficient uses a stated classical clamp instead, with no claim
that the apparatus supplies an expanding metric or a native creation law.

## 3. An intrinsic diagnostic without an inserted q

At any native age a, prepare a carrier localized at u while retaining a stated
environment density matrix rho_env(a). During the short probe let the actual
parent evolve with no additional carrier-moving port. The initial coefficient
for v across one possible edge is

    P_v(s)=t_hop^2<n_uv>_a s^2/hbar^2+O(s^3),
    K_intrinsic(a)=t_hop^2<n_uv>_a/(hbar^2 nu_u(a)^2).

Here nu_u is the ACTUAL post-preparation clock rate. Both its amplitude and
rate must be nonzero. The relation uses n_e^2=n_e; it is not a mean-link
Hamiltonian approximation. An arbitrary evolving background can have a cubic
term. K is a dimensionless probe coefficient, not a distance or volume.

There is an explicit information-preserving version of this intervention in
the already saved 16D held experiment. Its complete generator is

    H_hold=H_env tensor I_C-t_hop n tensor X_C,

where H_env includes every identity, storage, incidence and current-square
contribution; J_C^2=I_C. Introduce a fresh two-level position-pointer P with
degenerate self-energy, initially |L>. An ideal controlled SWAP of C and P
produces carrier |L> and moves its previous correlations into P. It does not
erase them or claim a free reset. The environment marginal is exactly unchanged.
Since [H_hold,A_L]=epsilon_r A_L-lambda_R n A_L, the initial clock amplitude
and rate are unchanged too. The complete bulk switching work is

    W_swap=t_hop<n X_C>_old=-E_hopping,old.

The new hopping expectation vanishes; all other bulk terms are unchanged.
Pointer energy is zero by declared degeneracy, not a claim that preparing,
controlling or reusing that pointer has no cost. The physical implementation
of a finite-duration swap, its endpoint access, calibration and preparation
resources remain to be supplied. It is an ideal readout prescription, not
a native local graph-formation mechanism or an operation performed on matter.

The saved record-swap symmetry makes each local clock rate equal to the
saved global A_L+A_R rate. Thus K and W for every saved age can be obtained
from the already authenticated link occupation, clock rate and hopping energy,
without propagating the old histories or losing the moved correlations.
The old whole-window clock certificate concerns the ORIGINAL held trajectory;
it does not qualify a finite interval after the new swap. Only a local
nonzero-clock derivative is used here.

This work identity is special to the two-endpoint, one-carrier cell. On a
larger graph J_e^2 is an endpoint-occupation projector, and changing the
carrier position generally changes additional current-square energy.

## 4. Saved-state result: relational variation, not expansion

The single saved-scalar calculation is complete. All 408 assigned arithmetic
and custody-linked checks pass under the inherited 1e-10 numerical allowance.
It includes every inherited preparation and age, with no new propagation,
eigensolve, fitted source, age selection or tolerance change.

| Held age | Native K | Feedback-off K | Native ideal bulk SWAP work |
| ---: | ---: | ---: | ---: |
| 0 | 0.2041207661 | 0.1092530527 | 0.0460067644 |
| 0.25 | 0.2215331895 | 0.1014803386 | 0.0772615578 |
| 0.5 | 0.1793012570 | 0.0723388590 | 0.1015155669 |
| 1 | 0.0622416318 | 0.0181642442 | 0.0847067678 |
| 2 | 0.0638668712 | 0.0766361042 | -0.0567653570 |

The native record count stays 1.31433676545 while K varies nonmonotonically.
The feedback-off control also varies, even though its phase rate is exactly
one. Thus neither fixed counts nor a fixed clock rate enforce fixed probe
transport, but transport aging is not uniquely caused by record feedback.
Copying-off has five undefined K values because its phase amplitude vanishes;
its carrier transport is not zero. All fifteen signed work values are retained
in the JSON. The negative native work at age2 means energy leaves the bulk
in the ideal intervention, not that a reset apparatus operates for free.

The result makes a narrower positive statement than a scale-factor claim:
the specified native evolution changes an operational, dimensionless
transport-per-clock observable at fixed counts. It does not give a monotone
expanding universe, a distance-redshift curve or a common metric. Neither
the nonmonotonicity nor the two-node size rejects every macroscopic network
expansion model.

- Saved-arithmetic source `native_intrinsic_transport_clock_saved_v001.py`:
  `af81a93a76938cae5386bd737f983caf1d5c8e1a4c9c4d41673d3377d6c94838`.
- Result `native_intrinsic_transport_clock_saved_v001_results.json`:
  `0eeccca739e01ca89384cd35c30a9823fe6870d009337169e9801cc962609811`.
- Original record/state result:
  `2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a`.
- Original clock result:
  `5992e6daf072b3873670d22c280f4f1592e95a0f250eb703d919d6d548f21206`.

The successful saved-arithmetic run used 0.0127432 seconds and 24,707,072
bytes peak self RSS. Initial page delivery lacked an interactive input session
after its producer had exited successfully; only its first of four pages was
received. The same short arithmetic was rerun unchanged through the existing
pager with a live PTY, all four pages were recovered, and both producer and
pager exited0. This was a capture repair, not a rerun of a scientific history
or a change in the result criteria.

## Decision significance and review

A changing K at fixed node and record counts is a concrete relational change
that a count-only geometry would miss. The feedback-off control must be kept:
incidence dynamics and clock behavior can vary without record feedback.
Neither change establishes a physical scale factor, common-probe metric,
cosmic acceleration, or spectral redshift. Repeating this local probe in a
formed extended state with shared clocks and source accounting is the next
physical issue, not assigning V proportional to K to obtain a desired history.

Root and agents endpoint_equations_check and handoff_plan_review_v005
independently derived the finite-N source coefficient. Endpoint review also
checked the complex-background cubic remainder and work/source distinctions.
Endpoint review separately verified the ideal SWAP, its cell restriction,
correlation custody and work identity before root ran the saved arithmetic.
Agent v005_resume_review authored that source without executing it; root read
the full source and executed the sole sequential arithmetic worker.
The active dressed gap is prior work, not a new source constant. All proposed
readout interventions are separate from the saved unperturbed preparation.
