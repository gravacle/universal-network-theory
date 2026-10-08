# Formation state selection and matter source correspondence

2026-10-03 UTC. Source-only continuation of frontier V112. Two results
sharpen the missing physical join. First, the dense-eligibility BS parent
does not select finite average raw degree in a fixed-finite-temperature
Gibbs state, even with quantum incidence, copying and carrier dynamics.
Second, an exact fixed-clock response specifies what must match when
ordinary matter changes the network; a response to an externally imposed
lapse alone does not establish that correspondence.

Neither result substitutes equilibrium for the actual evolving preparation.
No numerical history, parameter fit, new physical coupling or gravity
prediction is introduced. All eleven dark-program lanes remain open.

## Provenance and the precise extension

The inherited numerical tuple is explicitly described as illustrative,
not fitted or measured, in the original
`UNT_RECORD_TO_GEOMETRY_MINIMAL_JOIN_2026-09-27_V001/PROTOCOL.md`.
The positive-cost ground-state bound is therefore not a no-go for every
parameter choice in the BS family. Existing finite-degree alternatives
and connected excited-state persistence are preserved, not rediscovered.

There is ALSO earlier entropy-obstruction work. Resident
`program-worktree/MODEL.md`, passages around lines365-381 and420-436,
records a local-family theorem requiring O(N) projected spectral width,
and a clean-classical-slice finite-valence obstruction respectively.
The latter explicitly does not cover nonzero carrier/current/port dynamics.
The register identifies these as GE-X59 and GE-X61. Their original EA/EC
packet directories were not found at the referenced paths in this checkout;
these are verified resident summaries, not newly authenticated original
proofs or reproduced check counts.

The independent proof below needs only an extensive LOWER energy bound and
an extensive upper bound on selected trial expectations. It does not assume
O(N) spectral width of the full soft parent, which has high-degree states
with much larger energies. It extends the obstruction to the full quantum
model and to finite AVERAGE degree, within the stated canonical ensembles.

## Quantum Gibbs sparsity theorem

Use one slab with N nodes in each of two layers and all N^2 eligible link
qubits. Let M be occupied-link number. All microscopic coefficients are
fixed as N grows, the number and dimension of local registers are fixed,
and h_N=Omega/N. Work either in the full declared register space or a
preserved carrier-number/content sector. No hard degree projection is made.

Assume H_N >= -C_minus*N for a fixed constant. This follows in BS13 and
also from the separately proved degree-stabilized lower bound when U_d>0,
after retaining bounded copying and port contributions. This is a lower
bound, not a claim that every thermodynamic state's energy is extensive.

For every fixed integer k, there are many orthogonal trial states with
bounded graph degree k and <H_N> <= C_k*N+O_k(1). Records can be blank,
writers fixed, and any allowed definite carrier pattern retained. In a
definite k-regular graph the complete diagonal expectation is

    Delta*k*N + 2*N*U_d*(k-d_star)^2
      +epsilon_psi*Q+2*N*epsilon_w
      +lambda_J*sum_edges n_e*(p_u-p_v)^2.

The displayed one-content sector has p in {0,1}. Flip, hopping and copying
expectations vanish in this basis trial; the terms remain in H. Feedback
vanishes because the trial records are blank, not because it was removed.
The current contribution is bounded by lambda_J*k*N. Group-averaged trials
below may have hopping expectation; its magnitude is at most |t|*k*N.
With nonnegative storage coefficients, a common sufficient constant for
both types of trial, including padded graphs, is

    C_k=(|Delta|+lambda_J+|t|)*k
          +2*U_d*max(d_star^2,(k-d_star)^2)
          +2*epsilon_psi+2*epsilon_w.

Bounded O(N) additional port terms add their norm constant. More general
fixed local registers change the constants and an exp(O(N)) dimension
factor, not the counting exponent.

### Elementary graph count

First take N=k*m. Partition each layer into k fixed blocks of m vertices.
In each of the k^2 disjoint block pairs choose one perfect matching. Each
vertex then has degree k, and different choices give different simple
graphs. Therefore the number R_N,k of eligible trial graphs obeys

    R_N,k >= (m!)^(k^2),
    log R_N,k >= k*N*log N-O_k(N).

For arbitrary N use k*floor(N/k) active vertices per layer and leave fewer
than k vertices per side isolated. Their extra degree costs are O_k(1),
and the same asymptotic count holds. This construction supplies a lower
bound only; it is not a generated geometry or a preparation protocol.

For fixed D>=0, the number S_N,D of graph configurations with M<=D*N is

    S_N,D <= sum_(m=0)^floor(D*N) binom(N^2,m),
    log S_N,D <= D*N*log N+O_D(N).

D=0 has exactly one blank graph. For D>0 the bound follows from
binom(n,m)<=(e*n/m)^m and eventual monotonicity of these binomial terms.
The average degree on 2N vertices is M/N, so this is an average-degree
statement, not merely a maximum-degree statement.

### Full quantum ensemble

Let beta be fixed, finite and nonnegative in inverse microscopic energy
units. It is a hypothetical equilibrium parameter, not an identified CMB
temperature. Scalar spectral Jensen applied to each orthonormal trial gives

    <i|exp(-beta*H_N)|i> >= exp(-beta*<i|H_N|i>),
    Z_N >= R_N,k*exp[-beta*C_k*N-O_k(beta)].

Let P_D project onto M<=D*N with all admitted local registers included.
Their dimension is at most exp(c_reg*N). The spectral lower bound implies

    Tr[P_D exp(-beta*H_N)]
       <= S_N,D*exp[(c_reg+beta*C_minus)*N].

This trace bound does NOT require [P_D,H_N]=0. Consequently

    Prob_beta(M<=D*N)
       <= exp[-(k-D)*N*log N+O_(k,D,beta)(N)].

Choose any fixed integer k>D. The probability tends to zero for every
fixed D. The proof retains quantum flips, copying and carrier/current
terms through the actual H, not a diagonal classical replacement.

### Permutation invariant ensemble

This is not an artifact of counting only labeled copies of the same graph.
Suppose H retains the within-layer permutation symmetry and restrict its
Gibbs trace to the invariant Hilbert subspace. BS does not declare this
restriction a gauge quotient; it is a separately stated ensemble.

There are at least R_N,k/(N!)^2 graph orbits. For each orbit, group-average
a compatible basis trial and normalize. The average is nonzero because
these register permutations carry no signs. Distinct graph orbits have
disjoint support, hence orthogonal averaged trials. Each has fixed M and
blank records, so flip/copy expectations still vanish; the hopping bound
already included in C_k covers its possible surviving expectation.

The invariant partition function therefore has lower bound

    Z_N,sym >= [R_N,k/(N!)^2]*exp[-beta*C_k*N-O_k(beta)].

The crude full-space bound on rank(P_D) is still valid after restriction.
It follows that

    Prob_beta,sym(M<=D*N)
       <= exp[-(k-D-2)*N*log N+O_(k,D,beta)(N)] -> 0

by choosing fixed k>D+2. No assumption of thermal access to other symmetry
representations is needed for this version. Any claimed restriction to a
different invariant sector needs its own state-count argument.

For a geometry family with at most exp(c_geom*N) graph shapes modulo
within-layer permutations, the sharper local-family exponent k-2 follows
in either ensemble. In the invariant space its target rank is at most
exp(c_geom*N) times the local-register dimension: an invariant vector on
one graph orbit is determined by one register vector invariant under the
graph stabilizer. Fixed-template bounded-range lattice families are
examples, not a classification of every possible emergent geometry.

### What this rules out and what it leaves open

At fixed finite beta, changing fixed degree-preference or copying constants
does not rescue a sparse raw-incidence Gibbs phase of this unrestricted
parent. An extensive lower stability bound is not sufficient to establish
sparse finite-temperature thermodynamics. A bounded extensive perturbation
V_N, ||V_N||<=c*N, only changes the constants; this includes declared
bounded static ports with exp(O(N)) total port dimension. Symmetry or charge
restriction additionally requires those ports to preserve the chosen sector;
the invariant-space proof also needs an admissible invariant port trial.

This is an asymptotic theorem, with no asserted practical finite-N crossover.
It says neither that the actual blank preparation becomes Gibbs nor that
the finite universe is equilibrated. It excludes neither a protected
nonequilibrium formation process, a temperature/coupling scale varying with
N, hard active capacity or reduced eligibility, nor an operational geometry
encoded in correlations rather than sparse raw links. Those are different
physical mechanisms to derive or explicitly propose, not free repairs.
In particular it does not invalidate the existing conditional RGRL/working-
theory closure, which supplies its own geometry and response premises.

## Complete response at a fixed internal clock

Return to the ACTUAL state rho_0 and the complete source family
H[L]=sum_v L_v*h_v of the V112 mechanism note. Set x=tau/hbar, so dots
below are derivatives with respect to generator age x. At L=1, for x>y,

    chi_vw(x,y)=i Tr rho_0 [h_v(x),h_w(y)],
    sum_v chi_vw=partial_y <h_w(y)>,
    sum_w chi_vw=-partial_x <h_v(x)>,
    sum_vw chi_vw=0.

Nonstationarity remains on the right sides. Let beta_B(x)=<B(x)> be a
complex clock amplitude and theta(x)=arg beta_B(x)-arg beta_B(0).
Require nonzero amplitudes and nu(x)=Im[dot beta_B/beta_B]!=0 on the
selected local inverse-clock branch. This is an expectation-phase clock,
not a certified single-shot apparatus or physical-seconds calibration.

For O Hermitian and A either O or B, write the first-order response to
L_w=1+ell_w, including preparation and readout dependence, as

    delta a(x)=b_A(x)+sum_w integral R_Aw(x,y)*ell_w(y)dy,
    b_A(x)=Tr[delta rho_0*A(x)],
    R_Aw=-i Theta(x-y)<[A(x),h_w(y)]>+D_Aw(x,y).

D contains explicit source-dependent readout contacts; source-dependent
preparation belongs in delta rho_0. On a fixed elapsed-phase comparison,

    delta o|theta = delta o(x)-(dot o/nu)*Im[
                       delta beta_B(x)/beta_B(x)
                         -delta beta_B(0)/beta_B(0)].

Thus the full kernel is

    K^theta_Ow=R_Ow-(dot o/nu)*Im[
                     R_Bw(x,y)/beta_B(x)-R_Bw(0,y)/beta_B(0)],

with the identical linear combination of b_O,b_B as its separate boundary
term b^theta_O. For an externally fixed absolute phase origin, omit the
initial-phase subtraction only if that is the declared experiment.

For fixed readouts/preparation and interior times, the dynamical part is

    Q_B(x)=[B(x)/beta_B(x)-B(x)^dagger/beta_B(x)^*]/(2i),
    K^theta_Ow=-i Theta(x-y)<[O(x)-(dot o/nu)*Q_B(x),h_w(y)]>.

The Hermitian phase quadrature requires BOTH B and B^dagger. A uniform lapse
gives delta o=dot o*integral ell and delta theta=nu*integral ell, so the
fixed-clock dynamical kernel sums to zero over w. Arbitrary preparation or
explicit readout contacts need not cancel. For example LH retains its
explicit L dependence as a coordinate-energy readout. Energy and work are
not erased by the internal-clock cancellation.

## A decisive endogenous matter comparison

Specify an actual native matter-loading or redistribution operation, with
its complete state tangent delta rho_m, correlations and work. After that
operation the evolution uses the common native H. This is a preparation
change, not an externally imposed lapse. Its fixed-clock signal is
b_O^(m,theta) from the preceding formula.

A lapse-only effective description requires ONE common profile ell_m to obey

    b_O^(m,theta)(x)=sum_w integral K^theta_Ow(x,y)*ell_m,w(y)dy

for a prospectively specified complete PROBE algebra throughout the declared
interval, with separate energy/work consistency. A linear combination of
probe histories that vanishes for every lapse profile but responds to the
matter operation is a decisive rejection of this lapse-only description.
Fitting a separate profile to each readout would not pass the test.

Do not impose equivalence of the entire source-containing state: lapse
evolution preserves carrier-sector weights, while matter addition can change
them. A supply belongs in the complete preparation ledger. Conversely,
matching restricted probes does not derive an endogenous field equation,
uniquely determine lapse (uniform clock rescaling is invisible here), or
establish BTFR. A spatial-metric/shift channel may also be required; failure
of lapse-only matching would not exclude that larger declared completion.

## Immediate scientific consequence

Do not rerun the regular-degree or frozen-degree transport examples hoping
that finite-temperature equilibration will supply locality. The prior
frozen degree-two static-potential mixture is already solved. A useful
analytic qualification is that the actual blank-record occupation response
near detuning zero starts LINEARLY in detuning, whereas a separately
prepared lower-state response starts quadratically; a static equilibrium
replacement can therefore remove the leading causal signal.

Explicitly, for h=delta*r+a*X, blank rho=(I+Z)/2, a>0 and
Delta_r=sqrt(delta^2+4*a^2), the PLUS-source retarded convention gives

    chi_XX,blank(x,y)=(2*delta/Delta_r^3)*{
       4*a^2*[sin(Delta_r*x)-sin(Delta_r*y)]
       +delta^2*sin[Delta_r*(x-y)]},
    chi_XX,lower(x,y)=2*delta^2*sin[Delta_r*(x-y)]/Delta_r^2.

The latter uses a separately prepared lower eigenstate. At fixed finite
times the blank expression is (delta/a)*[sin(2ax)-sin(2ay)]+O(delta^3).
For the conjugate carrier-copy operator gX multiply both kernels by g^2.
At exactly fixed delta=0 and initially independent blank records, the
all-history influence factor reduces to

    F[p_plus,p_minus]=product_v cos[g*integral(p_plus-p_minus)_v dx].

It has no average-path dependence: occupation-to-X causal response is zero
to all orders, but the static binary-potential fluctuations are not zero.
This extends the already known frozen-degree mixture, not a new simulation.
Dynamic incidence escapes this restricted null because
dot X_v=(epsilon_r-lambda_R*d_v_operator)*Y_v; an initially resonant degree
does not set that operator to zero throughout subsequent evolution.
The previously derived degree/occupation mixed responses remain nonzero.

The next actual-state calculation must retain dynamic incidence and memory.
First use the EXISTING formation/locality results in URM to identify a
declared accessible configuration sector or formation rule, explicitly
separating supplied capacity/locality from derived properties. Then match
matter-induced probe response on that sector to the complete energy source
above, retaining its spatial response and formation work. The present
thermal theorem makes a generic Gibbs reset an invalid shortcut; it does
not require abandoning the user's nonequilibrium network interpretation.

## Review and evidence ceiling

Source-only independent review by v005_resume_review checked the counting,
Jensen/trace inequalities, padded-size extension and symmetry-sector proof.
endpoint_equations_check independently derived the energy Ward identities,
complex phase quadrature and initial-boundary fixed-clock terms. Root
checked the results against the complete BS action, the energy-dipole and
nonstationary Ward notes, and the resident older obstruction summaries.
handoff_plan_review_v005 independently derived the explicit detuning
kernels and all-history resonant influence factor.
No new numerical producer ran and no historical count was requalified.
This is internal mathematical review, not external peer review or new
astronomical evidence. No Stage 1, 2 or 3 completion is asserted.
