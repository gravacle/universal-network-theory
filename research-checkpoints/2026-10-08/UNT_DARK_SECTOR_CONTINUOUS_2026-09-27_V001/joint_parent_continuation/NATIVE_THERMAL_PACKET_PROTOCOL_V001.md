# Prospective native64 energy/current/probe packet

2026-09-29. Inert source/protocol, before outputs. Root owns the sole execution.
No fitted thermal state, added noise, finite source pulse, parameter adjustment,
new graph shape, or physical photon/clock map is adopted. A prospective uniform
record-loading contrast is explicitly added before any execution below.

## Owned input and complete census

Use the exact N=2, 64-dimensional held incidence/one-carrier sector already
qualified by `NATIVE_CARRIER_RULER_V001_RESULTS.json`: index `4*mask+vertex`,
vertices L0,L1,R0,R1, edges (L0,R0),(L0,R1),(L1,R0),(L1,R1). Preserve both
initial basis states, cycle mask15 and anchored tree mask11 with carrier L0.
Both initial graphs are connected; neither is frozen during evolution. Writers
and reservoirs are blank; copying/ports are off. Carrier content is fixed but
content-symmetric. Preserve hbar=Omega=Ud=dstar=epsilon_psi=1,
Delta=4, t=.5, lambdaJ=.25, hN=Omega/2. No absolute offset is removed.

Retain **both** uniform fixed record sectors q=0 (all blank) and q=1 (each of
the four nodes has a fixed-content occupied record). The latter pair are new
explicitly prepared comparison states, not saved formed states or a claimed
record-loading trajectory. The existing native coefficients epsilon_r=1 and
lambda_R=.5 are pinned from the old record-addition source and BS action;
no coefficient is added. Each sector remains dimension64 and invariant under
the held action. Its Hamiltonian relative to the old q=0 block is exactly

    H_q-H_0 = 4 epsilon_r q I - 2 lambda_R q sum_e n_e.

The absolute initial energies are 21.5/15.5 for blank cycle/tree and 21.5/16.5
for occupied cycle/tree. Preparation-energy differences 0/+1 are reported
by this identity, not called autonomous loading work. All four initial energy
variances are 1.5. The node partition adds epsilon_r q I to each node and
-lambda_R q n_e per incident edge. This retains BS10 storage and BS11 feedback
and is checked against a separately assembled full row Hamiltonian, not a
silent replacement of the old block. Old saved-time readout checks apply only
to q=0; q=1 receives the same independent method and exact identity checks.

Hold times are exactly the old eleven: 0,1/32,1/16,1/8,1/4,1/2,1,pi/2,2,pi,4.
The primary readout census is 4×11=44. Return all local energies and energy
currents, including negative and zero values, carrier currents separately, and
equal-time connected covariance. The ten operators are four node energies
followed by six oriented energy currents u→v with u<v. Retain their full
110×110 complex two-time correlation for each state (time-major ordering),
and all 66 causally ordered 10×10 response blocks per state (264 total). At equal times
the response is the one-sided retarded limit; no theta(0)=1/2 convention is
silently imposed. The opposite time ordering is recoverable by Hermiticity.

The incidence-probe census inherits the earlier photon-probe choices, now on
this distinct owned64 system: ages {0,.5,2}, positive frequencies {.75,1.5,3},
durations {.25,1,2}, both frequency signs, all four edge n_e. There are 216
state/age/window/frequency/sign rows, each containing a complete complex 4×4
Gram, connected Gram, separate energy-dephased Gram and their difference.
The reuse of probe frequencies/windows is a prospective diagnostic choice,
not a frequency selection based on this system's spectrum or a physical CMB
identification. Microscopic times and energies retain hbar=1 units.

## Exact partition, current and work conventions

Freeze Eq(1) of `NATIVE_THERMAL_CONNECTIVITY_DISCRIMINATOR_V001.md`, plus the
explicit uniform-record terms above:

    h_v = Ud(d_v-dstar)^2 + epsilon_psi P_v
          + sum_(e incident v)[Delta*n_e/2-hN*X_e/2-t*n_e*T_e/2]
          + lambdaJ sum_(e incident v) n_e P_v
          + epsilon_r q I - lambda_R q sum_(e incident v) n_e.

The one-carrier identity J_e²=P_u+P_v gives exactly sum h_v=H. Current-square
energy is never replaced by a squared mean. A separately assembled full row
matrix checks the partition, all degree constants and correlated hopping.
Define J_uv=i[h_u,h_v]/hbar. Then J_uv=-J_vu and dot h_v=sum_u J_uv.
The left-layer patch is h_A=h_L0+h_L1, with crossing currents, not a fitted
localization. These energy currents can have support beyond the initially
occupied edges; carrier-number current is a different observable.

For any two Hermitian operators from the ten-element list, write

    C_ab(t,s)=<O_a(t) O_b(s)>,
    chi_ab(t,s)=i<[O_a(t),O_b(s)]>/hbar=-2 Im C_ab(t,s)/hbar,

for t≥s. The initial coherent state is retained. Source convention is
H_source=-f(s)O_b; convolution of chi with f is its linear response. In
particular, the exact nonstationary Ward identity is

    sum_v chi_(v,A)(t,s) = <dot h_A(s)>.

It is not generally zero: an impulse -eta*h_A would supply the corresponding
linear total-energy change eta*<dot h_A>. This worker applies no such source,
so no source work or thermalization trajectory is claimed. If a finite source
is later applied, its work is -integral f_dot<h_A> ds including switches.
After removal, held H is conserved. The four prepared states have energy
variance 1.5, not zero: each conserved total-energy connected covariance is
1.5 at every pair of times. No microcanonical fluctuation constraint is imposed.

Full commutator continuity is checked as a matrix identity and in the actual
states. The checked first-time derivative/current-divergence identity applies
to the stored **regular commutator kernel**, evaluated for t>=s with its
one-sided value at equality. For the full retarded distribution
theta(t-s)*chi(t,s), its first-time derivative additionally contains the
equal-time contact delta(t-s)*chi(s,s). This distributional contact is not a
missing numerical term in the stored regular kernel. Nonstationary age
dependence is not replaced by a function of t-s.

## Probe and stationary diagnostics

For each edge and both signs use the continuous sinc formula in the energy
basis for

    F_e^± = integral_0^T exp(±i omega s) n_e(s) ds,
    K_ef = <(F_e^±)† F_f^±>,
    Kconn_ef = K_ef - conjugate(<F_e^±>)*<F_f^±>.

Both K and Kconn are Hermitian positive-semidefinite Gram matrices. All complex
off-diagonal entries and coherent means are saved; deterministic coherent
drive is not called connected noise. The inherited plus sign is the leading
empty-probe emission coefficient, minus is absorption. Independent weak
oscillator probes would have leading cross occupation proportional to
g_e* g_f K_ef/hbar², with the conjugation convention fixed by the coupling;
the numerical packet does not couple or evolve such probes. Switching and
counter-rotating contributions remain, so these are finite-window coefficients,
not irreversible rates or an observed photon spectrum.

For a separately labeled stationary comparator, dephase only between distinct
whole energy eigenspaces. Retain coherence within each degenerate space. Do
not substitute this density matrix for the actual state. Every pair of energy
groups is output for each preparation and all four n_e channels, including
numerically absent lines. Nonnegative absorption/emission weights are computed
as squared norms, not cancellation-prone traces. Elastic weight, zeroth moment
and signed first double-commutator moment are checked. The reporting floor
1e-12 labels numerical absence and guards log ratios only; it does not drop
any pair or weight. Where both weights exceed it, report
beta_eff=log(W_abs/W_emit)/gap, including inverted negative values. No common
beta is fitted and no agreement/thermality threshold is a numerical pass gate.
No individual eigenvector populations are substituted for degenerate projectors.

## Numerical qualification fixed before results

Primary method: one Hermitian 64×64 eigensystem of each explicitly declared
native record-sector H. Independent method: shifted/scaled full-matrix Taylor exponential
with Gershgorin spectral enclosure, scaled norm≤.5 and exponential Taylor tail
below 1e-19 before squaring. Guard 256 terms is an algorithmic failure guard,
not a physical time limit. The reported product-tail bound excludes roundoff.
The center phase is restored; it does not subtract energy from the ledger.

Compare all eleven held states, all ten Heisenberg operator-on-state vectors,
and saved native carrier populations/currents/return amplitudes. For all probe
windows/signs, independently integrate with 32-point Gauss–Legendre using the
Taylor propagator. A separate 64-point spectral-propagator quadrature is also
compared to the exact sinc integral; this is an additional quadrature check,
not a second independent spectral decomposition. There are 36 integral-method
rows per record sector (72 total). All primitive matrices have size64; covariance matrices have size110.
No 3072-dimensional construction or new size sequence is involved.

Fixed absolute tolerances: operator/partition identities 2e-11, state and
ordinary correlation checks 2e-9, total-energy/variance and summed response
identities 2e-8, finite-window operator agreement 1e-9. Group energies within
1e-10, retaining whole groups. PSD qualification is
max(0,-lambda_min)/max(1,trace K)≤1e-10; Schwarz violation is divided by that
same fixed trace scale squared. Absolute negative eigenvalue, spectrum and
normalization are saved. Hermiticity uses the absolute state tolerance.
These floating-point qualifications are not interval-arithmetic certification.
All physical signs, ratios, zeros and incomplete thermal patterns are outputs,
never acceptance gates. Every executed failure is retained in FAILED_CHECKS.

## Custody, output and interpretation

The stdout-only worker has `freeze` and `run` modes. Freeze authenticates the
original result/freeze/review, all original frozen native sources, this thermal
note, inherited probe protocol, and its own source/protocol. Run requires exact
snapshot equality and the original COMPLETE result with all checks passed.
It checks the canonical original payload digest and frozen source hashes before
any evolution. Root captures/publishes stdout; the worker creates or edits no
file. The new result contains a canonical payload SHA, freeze SHA, all arrays,
check counts/maxima/failures, runtime and process-self RSS. Expected work is two
64D decompositions and roughly two hundred tiny independent propagators, with
small memory and a few-MiB output; root sizes the single job rather than imposing
a research deadline. No outcomes have been viewed to choose tolerances/census.

This tests whether the same native states own energy transport, temporal
memory and correlated local source response. It does not infer a bath,
temperature equilibration, dissipation, white noise, a continuum limit, a
cosmological geometry, photons or seconds. Initial connectedness is not a
thermalization proof. A Gibbs/KMS or transport/noise closure would be a separate
physical inference requiring a demonstrated time/size window and energy ledger.
