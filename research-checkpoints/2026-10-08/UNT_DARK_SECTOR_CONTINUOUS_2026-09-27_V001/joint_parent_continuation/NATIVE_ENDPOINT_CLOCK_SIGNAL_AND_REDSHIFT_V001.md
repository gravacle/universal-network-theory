# Same-state clocks, signals and an operational expansion test

2026-10-03. Working derivation and prospective finite diagnostic. This uses the
existing apparatus, not a new physical adoption or an observational result.

## The shortest unresolved join

The old record-phase clock and the blank-record carrier ruler were different
experiments. Neither their product nor an arbitrary rescaling of graph time
establishes a physical clock/ruler pair. Here both endpoint record clocks and
the carrier signal are evaluated in the SAME saved writer-formed 16D state.
The original formation is not rerun. Carrier-controlled copying and fragment
formation remain absent, as in the inherited experiment; the later all-copy
algebra cannot silently be substituted for this preparation.

Let a_j(t)=<A_j>, C_j=arg(a_j) with continuous phase, and
nu_j=Im(conj(a_j)*a_dot_j)/|a_j|^2. The held Hamiltonian gives

    nu_j = [epsilon_r - lambda_R Re(<n A_j>/<A_j>)] / hbar.

The record-only swap commutes with the writer-only formation and held
Hamiltonians, preserves the actual preparation, and exchanges A_L with A_R.
Thus a_L=a_R=a_total/2 throughout the inherited window, not just at sampled
ages. The established global-clock certificate transfers to either endpoint:
native local amplitude is at least 0.4581650 and its rate lies between
0.6699443 and 0.9724974 on held ages [0,2]. The copying-off blank control has
no phase clock. Equal endpoint clocks at equal age do not imply equal rates
at different emission and reception ages.

## An explicit informational source, including its work

Use the local carrier phase kick U_alpha=exp(-i alpha P_L), where P_L and P_R
are the carrier-left/right projectors. Integrated source action is hbar*alpha.
This is a declared probe, not a photon injection, gravitational source or
physical-distance measurement. For O(tau)=U_hold(tau)^dagger O U_hold(tau),

    R_O(tau) = i <[P_L,O(tau)]>.
    delta<O> = sin(alpha) R_O + (1-cos(alpha)) D_O,
    D_O = -<[P_L,[P_L,O(tau)]]>.

These are exact projector-kick identities. The receiver-clock variation is
R_C=Im(R_A_R/a_R). Comparing carrier readouts at the SAME receiver phase,
instead of the same external integration parameter, gives

    delta t / alpha = -R_C / nu_R,
    R_rel = R_P_R - (p_dot_R/nu_R) R_C.

This local implicit-function derivative requires a nonzero, oriented clock.
It is not a finite arrival-time estimator. If the emitter state commutes with
P_L, the first-order response vanishes; coherence must not be inserted to
rescue a null. Both the baseline carrier drift and the clock backreaction stay.

With conventional Pauli Y for the carrier, the complete held-energy change is

    Delta E = t_hop [(1-cos(alpha))<n X_C> + sin(alpha)<n Y_C>].
    E'_alpha(0) = hbar*p_dot_R.
    E''_alpha(0) = hbar*R'_P_R(0) = t_hop*<n X_C>.

No source-work term or absolute Hamiltonian term is removed. Work can have
either sign for a nonequilibrium preparation. An informational response alone
does not establish that the receiver can decode a physical signal reliably.

## What would count as network redshift

For an identified emission/reception event map t_r=F(t_e), the measured pulse
spacing in local clock ticks is

    Z_tick = dC_B(t_r)/dC_A(t_e) = nu_B(t_r)*F'(t_e)/nu_A(t_e).

Only after specifying phase-preserving signal transport, identical calibrated
emitter/receiver clock transitions and a suitable packet limit may this be
identified with a spectral 1+z. It is not enough to count new records, change
the graph radius, or relabel a coordinate. The present finite test does not
derive those transport/measurement assumptions or the event map F.

For the illustrative, additional assumptions of homogeneous nondispersive
transport, fixed coordinate endpoint separation chi, and positive speed c_g,

    integral(t_e,t_r) c_g(t) dt = chi,
    F' = c_g(t_e)/c_g(t_r),
    Z_tick = [nu_B(t_r)/c_g(t_r)] / [nu_A(t_e)/c_g(t_e)].

Z_tick equals spectral 1+z only under the preceding signal/calibration
assumptions. This explicitly allows a network interpretation different from metric
expansion. Constant clock rate with c_g=c/a recovers the usual scale-factor
ratio as ONE case, not a premise imposed on UNT. The replacement must predict
both quantities and the signal law rather than fit their ratio to redshift.
Direction-dependent transport, moving endpoints or dispersion can invalidate
this integral transport law and require the more general event map. Clock
drift remains explicit in nu_A and nu_B; nonstationarity is allowed when the
stated homogeneous transport law remains valid.

A sharper restriction is independent of this transport approximation: if the
entire closed generator is H(t)=f(t)H_0, f>0, and preparation, source events,
controllers and readouts are compared at u=integral f dt, evolution is exactly
exp(-i H_0 u/hbar). A common rate change is then only a reparametrization of
the SAME relational experiment. It adds no expansion observable. This does
not say every nonstationary experiment has Z_tick=1; intrinsic aging can
already affect its baseline. An externally unscaled controller breaks the
premise and its dynamics/work must be retained. An additive identity term is
unobservable as a common closed-system phase, but source/branch-dependent
identity terms cannot be discarded from controller or volume work.

The general need to compare dimensionless clock/ruler observables is familiar
from [Catena, Pietroni and Scarabello, Einstein and Jordan frames reconciled](https://arxiv.org/abs/astro-ph/0604492).
The identities here are applied to the local UNT candidates, not claimed as
a new theorem of cosmology. No conclusion about photons follows from them.

## Frozen small test, before its first execution

Worker: native_endpoint_signal_clock_v001.py, SHA-256
`2da6bde5f8ca4c65e811caa79c39b1508a7530000dcb54ba0fc6a3e34a14e68e`.
Root read the entire source and the imported operator/propagator definitions.
Only definitions are imported; old formation/audit producers are not called.
The worker authenticates the original saved states, clock certificates and
their source files before and after evaluation.

Three inherited controls; emission ages 0,.25,.5,1; delays
1/32,1/16,1/8,.25,.5,1; signed kicks 2^-8,2^-9,2^-10. All 72 rows have
reception age at most 2. Base matrix tolerance 1e-11 is inherited, not fitted.
Centered checks use the exact sin(alpha) denominator with its explicitly
amplified roundoff allowance; phase-log truncation has an analytic remainder.
The finite-kick trace-norm bound 2|sin(alpha/2)| transfers conservative clock
nonzero/orientation bounds to both signs. A failed bound is inconclusive,
not permission to change the kick or window after seeing the result.

One local root worker, one numerical thread, 120-second CPU/wall watchdog,
2-GiB peak-self-RSS acceptance ceiling (not a hard allocation limit), stdout
captured into one saved JSON. No physical parameter scan or new wrapper.
Failure and null results are retained. Numerical agreement qualifies this
finite relational readout only; it does not close the galaxy/expansion join,
source/volume law, formation selection, CMB, or any Stage 3 observational lane.

## Executed result and independent scope check

The root worker completed once: all 3,211 assigned numerical checks passed
across all 72 rows; 0.0671 seconds, 37,502,976 bytes peak self RSS. Result
`native_endpoint_signal_clock_v001_results.json`, SHA-256
`e3db002a21750274aa10bda2f0f916890d700245b5d4c225e16ef9850acdfca9`.
The maximum check-residual/tolerance ratio is 0.03323. These are implementation
checks, not independent observations or a bound on every floating-point error.

Native R_rel ranges from -0.00838097215 (emission1, delay1) to
0.06046901029 (emission.25, delay1); exactly one sampled row is negative.
The maximum absolute receiver-clock correction is 0.00050663020. This sign
change is a derivative of carrier probability with respect to the signed
source kick, NOT a negative signal speed or metric. The negative row ends
at the certificate boundary t=2, so no finite equal-phase event inside that
window is asserted. The defined finite-kick clock bounds stay positive:
at the largest kick, native amplitude>=0.45425875 and phase numerator>=0.16015746.
Feedback-off has zero clock backreaction within roundoff; copying-off keeps
all 24 relational responses undefined despite having carrier responses.

The frozen JSON field `trace_distance_bound` is a conservative bound on
the trace NORM of the state difference, twice the usual trace distance.
The formulas use the trace norm consistently; the historical field name is
not a tighter conventional-distance assertion.

Agent endpoint_equations_check independently read the source, equations and
saved result and accepted these claims. It ran no second propagation and is
not an external physical replication. Its two wording corrections concerning
clock drift and the conditional spectral interpretation are incorporated above.

## Apply the discriminator to existing source alternatives

This is a consequence of the already declared A/B candidates, not a new
dilation law or a numerical rerun. For fixed held state and q=ln(s), define
v=<dot P_R>, a=<A>, b=<nA>. Where nu>0 and v!=0, common scaling A gives

    (partial_q ln nu)_rho = (partial_q ln|v|)_rho = -z,
    (partial_q ln|nu/v|)_rho = 0.

Candidate B retains H_B=H_0-T-E_b I+exp(-q)T+E_b exp(3q)I.
Since [T,A]=0 and dot P_R=exp(-q)V_0, V_0=i[T,P_R]/hbar,

    (partial_q ln nu)_rho = 0,
    (partial_q ln|nu/v|)_rho = 1.

For an actual differentiable state path rho(q), the B sensitivity instead is

    d ln|nu/v|/dq = 1 - lambda_R/(hbar*nu) Re[(b'a-ba')/a^2]
                     - Tr(rho' V_0)/Tr(rho V_0).

The state terms cannot be suppressed by assuming the desired answer. Active
copying changes the clock commutator; a quantum entangled volume requires
<exp(-Q)V_0>, not exp(-<Q>)<V_0>. Probability current v is not group speed.
A frozen homogeneous graph with q-independent band basis can have
E(k,q)=E_rest+exp(-q)T(k)+E_b exp(3q), hence c_g=exp(-q)c_g0;
dynamical incidence does not generally preserve that band factorization.

The existing 96D A controller apparatus is also NOT a common scaling of its
entire closed Hamiltonian: its unscaled controller/volume terms break that
premise. The conditional null does not reject that different apparatus.
These distinctions were independently checked source-only by agent
handoff_plan_review_v005. No further matrix sweep is needed for these identities.
An independently specified formation/source evolution and a usable signal-event
map, not an arbitrarily chosen accelerating q(t), remain the next physical inputs.
