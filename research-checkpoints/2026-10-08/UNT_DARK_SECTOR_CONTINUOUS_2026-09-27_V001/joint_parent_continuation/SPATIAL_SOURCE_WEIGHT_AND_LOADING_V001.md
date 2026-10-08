# Spatial source selection and nonlinear matter loading

2026-10-03 UTC. Analytical candidate screens, not a newly adopted native
action, a galaxy fit or a completed physical source dictionary. These tests
address two missing steps between the finite network calculations and the
galaxy target: which spatial modes the complete source actually excites,
and how response depends on a physically specified ordinary-matter loading.

The strongest new static result is exact: a local scalar-gradient realization
of an adjustment field gives only a local matter self-interaction on top of
the original graph Green function. It does not enhance the exterior field
of a compact source. The finite-time result separately bounds the nonlinear
response available from a smooth complete-state loading family at a usable
internal clock. Neither result excludes other UNT completions.

## Existing target and distinct new test

SOFT_SPECTRUM_ROTATION_SELECTOR.md already derives the conditional separable
mode target: stiffness lambda=kappa*delta^2, source overlap proportional to
delta, positive quartic stabilization and a source-weighted density
nu(delta) proportional to delta can yield an energy proportional to |g|^3.
The resulting spherical interface can give g proportional to sqrt(M)/r.
Neither the required source weights nor independent mode quartics follow
from counting small eigenvalues. NATIVE_SHARED_WORK_INTEGRABILITY_V001.md
already gives the source/contact cancellation and static analytic boundary.
Those are prior results, not rediscovered here.

An interface between network environments suggests testing surface-like
soft modes as one possible origin of that count. This is a proposed route,
not evidence that an actual galaxy edge is a sharp two-dimensional surface.
The following calculation tests a minimal local-gradient realization before
investing in a spectrum or a fit. Its geometry, energy and source assignment
are explicit additional premises, not consequences of the BS Hamiltonian.

## Exact graph source weights

Let D be an oriented incidence matrix of a fixed connected graph, W positive
edge weights, B=W^(1/2)D, and L=B^T B. Work on a fixed Dirichlet or mean-zero
node subspace where L is positive definite. The source-independent real
edge vector e and scalar amplitude a define the candidate static energy

    E[y;a]=kappa/2 * ||a*e-B*y||^2 + U4(y),
    U4(y)=u/4 * sum_v y_v^4,      kappa,u>0.             (1)

Unit node weights are chosen only for this mathematical test; they are not
physical volume calibration. A constant shift of y is fixed consistently
in this section. If the constant mode is free, it must instead be minimized
with the quartic and cannot be silently omitted.

For L*v_j=lambda_j*v_j with orthonormal v_j, set
u_j=B*v_j/sqrt(lambda_j). These edge vectors are orthonormal. The quadratic
stiffnesses, linear source coefficients and source contact in (1) are

    k_j=kappa*lambda_j,
    b_j=kappa*sqrt(lambda_j)*(u_j^T e),
    C=kappa*||e||^2.

Consequently

    C-sum_j b_j^2/k_j
        =kappa*||P_ker(B^T) e||^2.                    (2)

This is an exact orthogonal projection identity, not a chosen cancellation.
The linear response is fully screened only when the source lies in the
gradient image of B. The weights |u_j^T e|^2, not an unweighted eigenvalue
histogram, decide the source-coupled spectrum. Degenerate eigenspaces must
be treated through their total projector weights, not selected eigenvectors.

The local quartic becomes

    U4=u/4 * sum_(i,j,k,l) T_ijkl*y_i*y_j*y_k*y_l,
    T_ijkl=sum_v v_i(v)*v_j(v)*v_k(v)*v_l(v).           (3)

It is generally not a sum of independent modal quartics. A change of basis
that diagonalizes L does not establish the separability of the previous
soft-mode comparison action.

If e=B*f with f in the specified node subspace, the finite-graph minimum
has the controlled small-a expansion

    y=a*f-(u/kappa)*a^3*L^(-1)*Pi(f^3)+O(a^5),
    E_min(a)=u*a^4/4 * sum_v f_v^4
       -u^2*a^6/(2*kappa)*<Pi(f^3),L^(-1)Pi(f^3)>+O(a^8). (4)

Pi is the orthogonal projector onto that node subspace and powers of f are
pointwise. This follows from the implicit-function theorem applied to
kappa*L*(y-a*f)+u*Pi(y^3)=0. It is not uniform as the smallest eigenvalue
vanishes; an increasing-size intermediate-field regime remains a separate
question. Equation (4) is not the desired cubic energy at fixed graph.

## Surface source selection does not follow from dimension

The continuum analogue of (1), considered only as an explicit comparison,
is E=integral_Sigma [kappa*|g_T-grad_Sigma y|^2/2+u*y^4/4] dA on a
closed surface, or a periodic planar patch. Integration by parts gives

    E=E_contact + kappa/2*integral |grad_Sigma y|^2
        -integral b_g*y + u/4*integral y^4,
    b_g=-kappa*div_Sigma(g_T).                         (5)

A constant tangent field on a periodic flat patch is divergence free.
It excites no scalar gradient modes at all in (5). This is a statement
about that periodic source, not a single-valued linear potential on a torus.
On a closed surface embedded with position X, a uniform ambient vector g
instead has g_T=grad_Sigma(g dot X). With outward mean curvature H defined
by Delta_Sigma X=-2H*n,

    b_g=2*kappa*H*(g dot n).

For a sphere of radius R and g=a*z_hat, the source is entirely l=1,
lambda=2/R^2. It is not a continuum of independently driven low modes,
even though a two-dimensional Laplacian has the familiar constant
high-mode stiffness counting density. Here "soft" would additionally
require an increasing-radius/scale limit; that count is not automatically
a low-eigenvalue limit of one fixed compact surface. Under lambda
proportional to delta^2 the corresponding unweighted delta count is linear,
but neither that Jacobian nor the count creates the missing source weights.

With the mean mode fixed and f=R*cos(theta), elementary sphere integrals give

    E_contact=4*pi*kappa*R^2*a^2/3,
    E_min(a)=pi*u*R^6*a^4/5+O(a^6)                    (6)

at fixed R. The local cubic force y^3 generates further harmonics:
cos(theta)^3 has both l=1 and l=3, so independent modal quartics cannot be
assumed even in this symmetric example.

An exactly centered spherical galaxy field g(r)*n is different again: its
tangential projection onto a concentric sphere is zero. This particular
surface-gradient coupling is therefore blind to that radial field. Normal
displacements, curvature couplings, vector modes, boundaries, disorder and
time-dependent memory are possible different mechanisms, not covered or
supplied by (5). A smooth galaxy edge is not proved to realize any of them.

## Self consistent field variation gives an exact exterior result

A source-clamped response is not yet gravity. Test the natural scalar
spatial completion of (1) by varying the field itself. On a fixed finite
Dirichlet graph consider

    E[phi,y;J]=kappa/2*||B*(phi-y)||^2
                  +u/4*sum_v y_v^4 + sum_v J_v*phi_v. (7)

Both phi and y have fixed zero boundary data. J is a separately owned
ordinary-matter source vector; no record mass is added. Calling phi a
physical gravitational potential still requires that additional dictionary.
The change of variables q=phi-y is bijective and separates (7) exactly:

    E=kappa/2*||B*q||^2 + J dot q
                      +sum_v [u*y_v^4/4+J_v*y_v].

The unique static minimizer therefore satisfies

    kappa*L*q=-J,           u*y_v^3=-J_v,
    phi=-kappa^(-1)*L^(-1)*J - real_cuberoot(J/u),     (8)
    E_min=-J^T*L^(-1)*J/(2*kappa)
                 -3*u^(-1/3)/4*sum_v |J_v|^(4/3).   (9)

These are exact at every source strength, not a perturbation series or a
claim of native dynamical relaxation. Outside the source support y=0.
For disjoint source supports the nonlinear term in (9) is additive: it
adds local self-energy, not a new intersource interaction. The exterior
field remains precisely the original graph Green function.

Only in a separately assumed three-dimensional Euclidean continuum, with
kappa=1/(4*pi*G), does this become Delta q=4*pi*G*rho_b and the ordinary
Newtonian exterior. A two-dimensional planar Green function can instead
give a logarithmic potential, but its amplitude remains proportional to
source mass. With fixed calibration it gives v^4 proportional to M^2,
not the required M. Geometry can change radial falloff without fixing the
mass dependence. Neither continuum is inferred from the native node count.

Smooth sources and physical boundary conditions must be owned before force
readouts at a source edge: a discontinuous J can produce a discontinuous
local y in this idealized model. The open exterior result is unaffected.
For a more general local potential U(y), the same separation survives if
U+J*y has a well-defined minimizer for each admitted J and the zero-source
minimizer is uniquely y=0. Boundedness of U alone would not suffice.

Thus (7) fails as an explanation of enhanced exterior gravity without any
spectrum computation or halo fit. It does not reject the earlier independent
vector-mode action, every collective interface theory, or the BS parent.
Its value is to eliminate one seemingly natural local spatial realization
of that action's source-weighted soft-mode target.

## Finite time loading with the complete state retained

This second discriminator does not assume equilibrium or the static energy
(1). On one fixed finite BS Hilbert space, let an independently specified
smooth loading/source family be

    H_eta=H_0+eta*V,    rho_eta(0)=rho_0+eta*sigma,
    0<=eta<=eta_0,      x=tau/hbar,    0<=x<=T.        (10)

Every rho_eta must be a physical density matrix. All source, clock, record,
work and retained apparatus terms belong in H_eta and rho_eta; this is not
a prescription to trace away memory or replace a preparation by equilibrium.
Set s=||sigma||_1, v=||V|| and S=s+2*T*v. Duhamel and unitary invariance give

    ||rho_eta(x)-rho_0(x)||_1 <= eta*S,
    ||partial_eta rho_eta(x)||_1 <= S.                (11)

The first bound follows by separating the initial-state difference from
the two unitary differences, each bounded by eta*x*v. The derivative uses
||rho_eta||_1=1 and the integrated generator derivative. Partial tracing
cannot increase the distance. If V=0, every fixed-x expectation is exactly
affine in eta, even with complete retained record correlations.

Let B be the fixed complex clock readout, b=||B||, and

    z_eta(x)=Tr[rho_eta(x)*B],
    C_eta(x)=arg z_eta(x)-arg z_eta(0),
    nu_eta=partial_x C_eta.

Here the phase is continuously unwrapped and ELAPSED FROM EACH FAMILY
MEMBER'S OWN PREPARATION PHASE. Both boundary terms must be differentiated.
This is not the common pre-kick phase origin used in the preceding
instantaneous-kick result. A fixed common phase reference can be treated
with its own boundary derivative and obeys the same conservative bounds.
Switching these conventions midway through a source comparison is invalid.

On a branch with |z_eta|>=beta>0 and nu_eta>=n>0, the inverse endpoint
x_eta(Theta) is real analytic, as are bounded fixed-operator readouts at
that endpoint. The finite matrix exponential is analytic and the nonzero
clock rate permits the real analytic implicit-function theorem. With
O fixed and L_O>=sup_eta ||[H_eta,O]||,

    |partial_eta x_eta| <= 2*b*S/(beta*n),
    |partial_eta <O>|_Theta
          <= S*[||O||+2*b*L_O/(beta*n)].              (12)

The factor two retains both phase boundary terms. This statement does not
identify O with a gravitational acceleration. Source-dependent O or its
calibration requires its additional derivatives.

### A source window certified from the baseline

Suppose the baseline has |z_0|>=beta_0 and nu_0>=n_0>0 throughout [0,T].
The baseline inverse endpoint must lie a generator-TIME distance at least
m>0 from both ends, not merely a phase distance. Let

    L_B=||[H_0,B]||,
    C_nu=2/beta_0 * [L_B*S*(1+b/beta_0)+2*v*b],
    eta_star=min[eta_0, beta_0/(2*b*S), n_0/(2*C_nu),
                             beta_0*n_0*m/(8*b*S)].  (13)

Zero denominators with a zero perturbation bound impose no restriction;
if S=0 the family is constant. For 0<=eta<=eta_star, the amplitude is at
least beta_0/2 and the clock rate at least n_0/2. In detail,

    |delta z|<=eta*b*S,
    |delta dot z|<=eta*(L_B*S+2*v*b),
    |nu_eta-nu_0|<=eta*C_nu.

The two phase differences sum to at most 4*eta*b*S/beta_0; the final
term of (13) preserves endpoint bracketing and the same inverse branch.
These are conservative pre-outcome analytic guards, not fitted tolerances.

### Acceleration requires its own chain rule

Let X be a fixed Hermitian position readout. A physical ruler interpretation
and phase-to-seconds calibration would still have to be independently
established. Define full-parent derivatives

    p_j=Tr[rho_eta*(i*ad_Heta)^j X],
    z_j=Tr[rho_eta*(i*ad_Heta)^j B],
    nu=Im(z_1/z_0),
    xi=partial_x nu=Im[z_2/z_0-(z_1/z_0)^2].

The actual second derivative against clock phase, not an operator renamed
acceleration, is

    A=p_2/nu^2-p_1*xi/nu^3.                           (14)

Choose uniform OPERATOR-NORM upper bounds P_j,Z_j on the differentiated X
and B operators and D_j,E_j on the parameter derivatives of their
expectations. For example, with h=sup_(0<=eta<=eta_star)||H_eta||,

    P_j=(2*h)^j*||X||,       Z_j=(2*h)^j*b,
    D_0=S*||X||,            E_0=S*b,
    D_j=S*P_j+2*j*v*(2*h)^(j-1)*||X||,               (j>=1)
    E_j=S*Z_j+2*j*v*(2*h)^(j-1)*b.                  (j>=1)

When h=0 these formulas can instead be read directly from the vanishing
commutators; no negative-power convention is needed. Tighter actual
commutator norm bounds are allowed. Small measured expectation values must
not replace the operator bounds inside the D_j or E_j estimates.

For certified amplitude beta and rate n, set

    N_eta=E_1/beta+Z_1*E_0/beta^2,
    Xi=Z_2/beta+Z_1^2/beta^2,
    Xi_eta=E_2/beta+Z_2*E_0/beta^2+2*Z_1*N_eta/beta,
    Omega_c=Z_3/beta+3*Z_2*Z_1/beta^2+2*Z_1^3/beta^3.

These bound |partial_eta nu|, |xi|, |partial_eta xi| and |partial_x xi|.
Straight differentiation of (14) then gives

    A_x_bound=P_3/n^2+3*P_2*Xi/n^3+P_1*Omega_c/n^3
                                      +3*P_1*Xi^2/n^4,
    A_eta_bound=D_2/n^2+2*P_2*N_eta/n^3+D_1*Xi/n^3
                         +P_1*Xi_eta/n^3+3*P_1*Xi*N_eta/n^4,
    K_acc=A_eta_bound+A_x_bound*2*b*S/(beta*n),
    |A_eta(Theta)-A_0(Theta)|<=K_acc*eta.              (15)

Here A_eta in the last line denotes the acceleration in member eta, not
its parameter derivative. The two similarly named upper bounds are
explicitly labeled. A common fixed conversion to physical length and time
rescales K_acc accordingly. If that conversion changes with loading, its
derivatives must be included; it cannot be chosen to impose the desired law.

### The conditional mass scaling discriminator

Only if an independently owned physical loading family identifies
M=eta*M_star and (14) with the relevant acceleration contrast can the
following galaxy comparison be made. A target A_target=A_*sqrt(eta),
A_*>0, cannot hold arbitrarily near eta=0 under the uniform finite bounds.
Even agreement to relative error epsilon<1 requires

    eta >= [(1-epsilon)*A_*/K_acc]^2                  (16)

within the certified interval. If K_acc=0, no positive target is possible
there. No numerical rejection interval is claimed without actual physical
calibrations and evaluated bounds. A large conservative K_acc can make (16)
weak; the theorem does not disprove a finite observed scaling window.

Crucially, a probabilistic mixture of an empty and a massive preparation is
not a deterministic galaxy of the mixture's mean mass. Native particle
number sectors are discrete. A specified continuum/coarse-grained loading
family is needed before making that identification. A preparation containing
coherent amplitudes proportional to sqrt(eta) already imports nonanalytic
dependence into rho_eta; it is not generated by memory in (10).

For a genuine limiting square-root law, some uniform bound must give way:
an increasing-system collective response, increasing formation or response
time, a nonanalytic state-selection limit, changing source/readout norms or
a collapsing clock guard. A failed clock or singular unit convention is not
itself physical evidence for modified gravity. Expansion about a nonzero
environmental field, and noncommuting size/time/source limits, remain open.

## The earlier Dirac parent under a complete energy source

The earlier GRAPH_SPECTRAL_PARENT.md supplies a different, successful
CONDITIONAL cubic-energy construction. Its square graph has
h(k)=d(k) dot alpha, d=t*(sin kx,sin ky), four internal orbitals and three
mass matrices Gamma_i anticommuting with h. The imposed mass source is
lambda*g_i*Gamma_i. Its two branches have energies
plus/minus sqrt(delta^2+lambda^2*g^2), delta=|d|. One normalized lower
projector P_-/2 is occupied per graph momentum, and one normalized upper
on-site block per vertex balances its high-field response. The positive
critical contact Kb=lambda^2*(<1/delta>-1/D) was supplied, not derived.
The earlier finite-q calculation in SPATIAL_RESPONSE_DERIVATION.md also
uses that MASS source. None of those calculations is repeated here.

The new test supplies the symmetric complete-energy lapse extension

    H[L]=[L*H0+H0*L]/2,       L=I+ell,                (17)

where L is a real diagonal node multiplier and identity on internal
orbitals. This is an explicit comparison completion, not a derivation of
the BS parent or its geometry. It assigns half of each hopping energy to
each endpoint and the full on-site energy to its node. The source is
affine, so its second derivative is zero in this chart. Its domain requires
positive L. For a separately calibrated finite embedding X_i,

    Z_i={X_i,H0}/(2*c^2),
    (Z_i)_nm=(E_n+E_m)*(X_i)_nm/(2*c^2).              (18)

Thus exactly balanced opposite branches with energies +/-delta have zero
dipole matrix element. Unequal-gap transitions can survive. Since X_i
commutes with each internal Gamma_j, {Z_i,Gamma_j}=0 for the zero-baseline
graph Hamiltonian. The insertion cannot equal a nonzero combination of the
three comparison mass matrices. Uniform lapse merely rescales H0 and has
no interband matrix element. Nonuniform lapse must still be evaluated.

A retained one-particle storage term epsilon*I changes (18) by
epsilon*X_i/c^2. It cannot be discarded as an irrelevant energy zero when
the source couples to the complete energy. Consequently the equal-gap null
and the three anticommutators are baseline-specific. A source-dependent
c-number vacuum allocation is different: it changes work/contact without
creating these one-particle transitions. Neither type of absolute energy
is determined by the old galaxy response fit.

### Exact finite momentum response and its infrared limit

Use the old Fourier normalization ell(v)=N^(-1/2)*sum_q ell(q)*exp(i*q.v),
with q mapping the antiperiodic momentum grid onto itself. Set
delta'=|d(k+q)|, n=d/delta, n'=d'/delta', S=delta+delta',
Delta=delta'-delta. Projectors obey

    Tr[P_-(k)*P_+(k+q)]/2=(1-n dot n')/2.

For H0=epsilon*I+h, the lower-to-upper matrix insertion per unit ell_q is
(epsilon+Delta/2)*P_+(k+q)*P_-(k). Summing the two transition directions
on the equally populated lower branch gives the exact static susceptibility

    chi_ell(q)=< [epsilon^2+Delta^2/4]
                         *(1-n dot n')/S >.          (19)

In particular chi_ell(0)=0. There is no missing degeneracy factor: the
trace-one rank-two population is the earlier per-branch convention.
Filling both lower orbitals doubles the complete energy and susceptibility.
The actual work curvature of this affine lower-band source is -chi_ell,
not +chi_ell. This is a specified adiabatic population calculation, not
the two-time response of the native blank preparation. In the stated
N^(-1/2) Fourier convention the TOTAL quadratic energy is
-sum_q chi_ell(q)*|ell(q)|^2/2; divide by N for energy per vertex.

There are useful exact bounds before taking a continuum limit. Let
r=|d'-d| and w=(1-n dot n')/2. Then

    w=(r^2-Delta^2)/(4*delta*delta'),
    |Delta|<=r<=S,
    K_0:=Delta^2*w/(2*S)
       <=r^2/(2*S)<=r/2,
    K_0<=r^4/(32*delta*delta'*S).

For the sine lattice r<=2*t*|sin(q/2)| and S>=t*|sin(q)|, where sine
is componentwise and bars on vectors denote Euclidean norm. The latter
follows from sin(q)=diag(cos k)*sin(k+q)-diag(cos(k+q))*sin k and the
triangle inequality. It becomes uninformative at cone-connecting momenta;
it is not S>=t*|q| over the entire Brillouin zone. In one linear cone,
S>=t*|q| does follow. Thus finite-q source transitions have their own
pair threshold, not the old independent mass-block gaps 2*delta.

For a momentum segment with gap at least delta_*>0, the zero-baseline
interband operator is bounded by t^2*|q|^2/(4*delta_*) per unit lapse.
That estimate cannot be extended through the cones. The full continuum
cone integral resolves the omitted region without a numerical grid.
Take d=t*k and q=|q|>0. With r=|k|, r'=|k+q|, choose elliptic coordinates

    r+r'=q*cosh(u),     r'-r=q*cos(v),
    d^2k=r*r'*du*dv,
    1-n dot n'=q^2*sin(v)^2/(2*r*r'),
    0<=u<infinity,      0<=v<2*pi.

The measure times integrand in (19), including (2*pi)^(-2), becomes

    q/(8*pi^2*t) * sech(u)*sin(v)^2
                      *[epsilon^2+t^2*q^2*cos(v)^2/4] du dv.

Using integrals pi/2, pi and pi/4 for sech(u), sin(v)^2 and
sin(v)^2*cos(v)^2, respectively, gives exactly

    chi_one_cone(q)=epsilon^2*|q|/(16*t)
                                      +t*|q|^3/256.  (20)

These convergent integrals are for the unbounded linear cone, not the
entire lattice band. At epsilon=0 the four lattice cones therefore give

    chi_lattice(q)=t*|q|^3/64+o(|q|^3).              (21)

Away from fixed neighborhoods of the cones, the zero-baseline contribution
is O(|q|^4); it supplies no O(q^2) term for THIS source and state. Cone
linearization errors are subleading in (21). If epsilon is nonzero, the
leading full-lattice statement is instead
chi_lattice=epsilon^2*|q|/(4*t)+o(|q|). The lattice corrections to that
storage contribution cannot be dropped to advertise (20)'s cubic term as
the next lattice coefficient. The finite-size continuum window requires
1/L << |q| << 1 and its specified order of limits. The earlier mass-source
|q| kernel and this energy-source |q|^3 kernel are different responses.

The free-cone normalization is also consistent with Huh and Strack,
arXiv:1410.1902v3, equations (3),(6),(8),(9): their free two-component
Dirac limit has C_T=1/256 and C_J=1/16. At zero frequency the 00,00
tensor factor in their equation (6) is one. This is an external theoretical
cross-check, not a discovery of those standard coefficients or an empirical
UNT test. Their interacting gauge theory is not adopted here.
[Primary paper](https://arxiv.org/pdf/1410.1902).

### The old compensation and field law do not transfer

For the old on-site comparison sector, H_upper=D*Gamma_0 independently at
each node. Every scalar L commutes with its internal projectors. The lapse
insertion is interband-dark even for nonuniform L, regardless of whether
the upper or lower branch is populated. Its retained absolute energy still
contributes to source work; its positive mass-source susceptibility does
NOT carry over to (19). A supplied quadratic contact also cannot create a
missing transition. The old equal-count cancellation and its static/dynamic
stability proof remain results of the original mass-source comparison.
The alternative four-dimensional Laplacian construction has the same
selection problem: H0=t*L_graph tensor Gamma_0 and its scalar-lapse source
both preserve Gamma_0. The equally occupied entire lower branch has no
interband susceptibility and its fixed-population trace energy is affine.
This does not cover a partly filled branch, finite population changes, or
a different internal/source completion.

Equations (19)-(21) show that the energy-lapse response is nonzero but does
not reproduce the old local cubic constitutive energy. It is quadratic in
lapse amplitude and nonlocal in the internal spatial coordinates. A cubic
power of wave number is not a cubic power of field amplitude. Only after
a physical ruler and clock dictionary is independently adopted may one
write an acceleration. The lattice q above is DIMENSIONLESS. If a_lat is
an independently calibrated length per internal coordinate unit, Q=q/a_lat
and g_Q=c^2*i*Q*ell_q. The zero-baseline four-cone curvature per longitudinal
g and per vertex is then

    -chi_ell(q)/(c^4*|Q|^2)
          =-t*a_lat^2*|q|/(64*c^4)+o(|q|).           (22)

Per physical volume it additionally needs the independently owned vertex
density N/V. The internal two-dimensional graph supplies neither a_lat
nor a three-dimensional volume per vertex. Equation (22) remains a
nonlocal quadratic response, not a derived a0 or v^4=G*M_b*a0.

### Changing the response size is a distinct state hypothesis

One possible attempted escape is to let the response wavelength depend on
acceleration. At epsilon=0, the SECOND-ORDER energy per vertex for the real
profile ell=A*cos(q dot v) is

    Delta w^(2)=-t*A^2*|q|^3/256,
    g_amp=c^2*|q|*|A|/a_lat.

Following an IMPOSED path of fixed |A| and |q|=a_lat*g_amp/(c^2*|A|) gives

    Delta w^(2)=-t*a_lat^3*g_amp^3/(256*c^6*|A|).      (23)

The coefficient depends on the imposed profile amplitude. Different weak
cosine profiles with the same distribution of acceleration amplitudes have
different energies if their wavelengths differ. This is not a local energy
function of |g| alone. Taking g_amp to zero along (23) leaves |A| fixed,
so omitted finite-amplitude corrections do not vanish just because g is small.
The sign is also that of the lower-band curvature, not the old positive
critical cubic-energy term.

A dynamically selected scale could evade this argument, but it requires
stationarity of the complete state/source/boundary energy. A derivative
along a freely prescribed q(g) includes (partial_q w)*dq/dg; it is not
automatically the gravitational constitutive force. The envelope theorem
does not remove this term before a physical stationary branch is supplied.
For response length R=a_lat/|q|, g_amp*R/c^2=|A|. A horizon-like choice
R~c^2/g_amp reaches |A|~1, beyond this weak-lapse expansion. Fixed g and
unbounded R likewise leave its domain. Neither is a calculated native horizon.

As a limited constructive check, ADD a separately postulated positive
source-field energy C*sum|grad_graph ell|^2/2 in the continuum window.
The quadratic kernel becomes K=C*q^2-chi_ell. For epsilon=0 and C>0 it
is positive sufficiently far into the infrared. For epsilon!=0 the
-epsilon^2*|q|/(4*t) term dominates at sufficiently small q; a finite
domain may not contain that interval. These are static signs for this
comparison, not physical growth rates or a native gravitational instability.

The linear-cone expression at fixed g_amp is

    w_total^(2)=a_lat^2*g_amp^2/(4*c^4)
                 *[C-t*|q|/64-epsilon^2/(4*t*|q|)].   (24)

For epsilon=0 it has no finite-q minimum. For epsilon!=0 its possible
interior stationary point is a maximum, and must in any event lie within
the cone and weak-lapse domain. Thus even this added stiffness does not
select the desired q(g) at quadratic order. Lattice corrections, additional
interactions and finite-amplitude dynamics are not inferred from (24).
Any proposed stabilizing mechanism must retain the same absolute energy,
clock, source and work; the old mass-source Kb cannot be silently reused.

This comparison neither makes the internal graph a physical two-dimensional
space nor rules out deformation, interactions, state selection or additional
metric channels in a different completion. It identifies the missing physical
source binding of a previously successful conditional parent without altering
its frozen mass-source results or replacing it with a fitted response.

## What follows for native work

The BS bare weak-lapse source is affine in the assigned node energies; its
quadratic source contact is zero in that chart. Equation (1)'s positive
contact is therefore not inherited automatically. Any source-field or
coarse-graining contribution must be derived or counted as a physical
postulate before matching it. The same applies to a local gradient stiffness,
its node/volume measure and the physical meaning of a surface.

URM's frozen q4 additive-source theorem independently establishes the
relevant discipline: an absent linear source direction is not restored by
blocking or a contact Hessian. It is not a proof of the scalar-gradient
construction above. The q4 count-front and programmed support results do
not, by themselves, establish an autonomous physical galaxy interface.

The next useful native measurement is the joint spatial source operator,
its mode overlaps and interaction tensor on one justified formed state,
with contacts and work retained. A spectral histogram, a fitted spatial
kernel or a larger repetition of identical local cells is insufficient.
The finite-time loading bound distinguishes actual nonlinear source/state
selection from apparent nonlinearity introduced by clock or preparation
conventions. Neither result supplies a formation law or an absolute volume
stress. The expansion and both CMB lanes keep their separate obligations.

## Evidence and review

Root derived (1)-(9); endpoint_equations_check independently checked the
source signs, sphere coefficients, fixed-subspace qualification, sixth-order
term, exact field separation and dimension-dependent exterior interpretation.
Handoff_plan_review_v005 derived (10)-(13) and the finite-source consequence;
root extended this to the actual relational acceleration (14)-(15).
V005_resume_review independently checked the baseline constants and full
acceleration chain rule, and corrected the readout and clock-origin scope.
The complete-energy Dirac source identities and the on-site upper-block
null were independently checked by handoff_plan_review_v005. Root derived
the finite-momentum projector response and elliptic-coordinate integrals;
v005_resume_review independently verified the two cone coefficients and
the exact lattice bounds. Handoff_plan_review_v005 separately checked the
cosine normalization, imposed-size-path limitation, weak-lapse domain and
the optional field-stiffness signs; the amplitude expansion is explicit.
This is internal mathematical review, not external peer review or an
observational test. No numerical producer, parameter scan or new physical
adoption occurred. All eleven dark-program lanes remain open.

Resident sources read for scope and nonduplication:

- SOFT_SPECTRUM_ROTATION_SELECTOR.md.
- NATIVE_SHARED_WORK_INTEGRABILITY_V001.md.
- DARK_SECTOR_SHARED_MODEL_CANDIDATE_V001.md.
- LOCAL_DENSITY_EXTERIOR_DISCRIMINATOR_V001.md.
- NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md.
- program-worktree/LANE_GRA_FR_F3_Q4_BLOCK_STRAIN_SOURCE_RANK_OBSTRUCTION_V001/THEOREM.md.

The first five are in this directory. These candidate-screen equations are
not attributed to those earlier sources. No general literature novelty is
claimed for the projection, variational or implicit-function identities.
The fixed-clock antecedents are NATIVE_ENDPOINT_CLOCK_SIGNAL_AND_REDSHIFT_V001.md
and NATIVE_FORMED_STATE_SOURCE_MATCHING_V001.md; neither old numerical
producer was rerun and no old whole-window clock certificate was transferred
to an untested family.

The distinct Dirac comparison sources are ../network_parent_bridge/
GRAPH_SPECTRAL_PARENT.md and ../joint_parent_dynamics/SPATIAL_RESPONSE_DERIVATION.md.
The source allocation premise is compared with NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md;
it does not identify the square-graph Hamiltonian with the native BS action.
