# A coupled spherical initial-value problem for matter, clock and modes

2026-09-28. New analytical reduction of the SAME conditional action in
EXPLICIT_MODE_COSMOLOGY_PATHWAY.md. No field evolution, fit, new gradient
term, dissipation, native inertia choice, or frozen-file edit.

## Result

There is a compact exact 1+1-dimensional variational/Hamiltonian system
retaining spherical gravity, the preferred clock, radial response modes and
conserved ordinary matter. It does not replace the modes by a clamped
mu_age or prescribe the gravitational acceleration they are meant to explain.

A decisive benchmark follows immediately: **unexcited modes and a geodesic
clock form an invariant GR-plus-matched-Lambda branch**, even during genuine
matter-density evolution. A spherical dust solution supplies an exact test
of this branch, including continuity and both gravitational constraints.
Consequently a common baryon-growth history does not by itself select the
enhanced stationary response. The native preparation of the clock and modes
is a physical discriminator, not an optional per-radius fit.

This is an existence branch, not a uniqueness theorem or an exclusion of
prepared, excited or stationary polarized branches. The general equations
below retain those possibilities and identify the initial/boundary data
needed to calculate them.

## 1. Exact spherical reduction before gauge fixing the constraints

Use c=1 and M²=1/(8 pi G). The finite positive mode band has weights w_j,
delta_j>0, m_j>0, kappa>0, u4>0 and the existing coefficients

    K_b=kappa*sum_j w_j,    C=2M²/K_b,
    h(a)=a/sqrt(1+a²/g_s²),
    V=sum_j w_j[kappa*delta_j²*x_j²/2+u4*x_j^4/4],
    B=sum_j w_j*kappa*delta_j*x_j.

DeltaU is the already declared absolute matching in the earlier action,
not a newly adjusted cosmological parameter. Set T=t, but retain lapse,
shift and both spatial metric functions in

    ds²=-N²dt²+L²(dr+beta*dt)²+R²dOmega²,
    n^mu=(1,-beta,0,0)/N,
    e_r^mu=(0,1/L,0,0),
    y_j^mu=x_j*e_r^mu.                                      (1)

Here n is the unit normal, not a lapse perturbation. N,L>0 and R>0 away
from the regular center. The radial variable r need not be areal radius.
Spherical symmetry gives P*nabla_n e_r=0: its possible normal component
is removed by P. Thus the exact physical mode speed and signed acceleration
are particularly simple:

    v_j=(x_dot_j-beta*x'_j)/N,
    a=N'/(N*L).

Primes denote r derivatives. Define the two eigenvalues of extrinsic
curvature and the spatial scalar curvature by

    K_r=[L_dot-(beta*L)']/(N*L),
    K_t=[R_dot-beta*R']/(N*R),
    theta=K_r+2K_t,
    R3=2/R²*[1-(R'/L)²-(2R/L)*(R'/L)'].

The complete reduced gravitational/mode action, apart from the standard
metric boundary term, is

    S=4pi integral dt dr N*L*R² {
       (M²/2)[R3-4K_r*K_t-2K_t²]
       +C[sum_j w_j*m_j*v_j²/2-V+B*h(a)-DeltaU] }+S_b.       (2)

This follows by direct angular reduction of the covariant parent; there
is no extra radial gradient penalty for x. The preferred-foliation ADM
framework and a_i=D_i ln N are the explicitly imported interface of
[Blanchet and Marsat, sections II–III](https://arxiv.org/pdf/1107.5264).
All finite-mode couplings in (2) are the previously specified comparison
parent, not a claim that the native BS continuum has already been matched.

Setting beta=0 is a permissible radial-threading choice AFTER variation.
Setting N=1 everywhere is not a generic gauge choice: it forces a=0 and
selects a physical clock branch. Similarly, R=r must not be imposed before
retaining its metric equation or equivalent gauge-preservation condition.

## 2. Matter with an actual current: the smallest closed example

For a first dynamical source use the ALREADY present ordinary matter sector
as one pressureless, irrotational baryonic stream before shell crossing.
This is a restricted source model, not a model of a supported stellar disk
or an added dark abundance. Its covariant action can be written

    S_b=-1/2 integral sqrt(-g)*rho0
                         [g^{mu nu} partial_mu chi partial_nu chi+1],

where U_mu=-partial_mu chi and rho0>=0 is the rest-density multiplier.
In the spherical variables the normalization and positive-energy branch are

    Gamma=sqrt(1+chi'²/L²),
    (chi_dot-beta*chi')/N=Gamma,
    p_chi=L*R²*rho0*Gamma >=0.

Dropping the common angular factor 4pi, its Hamiltonian density is

    H_b=N*p_chi*Gamma+beta*p_chi*chi'.                       (3)

The exact dust equations are

    chi_dot=beta*chi'+N*Gamma,
    p_chi_dot=[beta*p_chi+N*p_chi*chi'/(L²*Gamma)]',
    rho_b,normal=p_chi*Gamma/(L*R²).

In particular

    p_chi_dot+(p_chi*v_b,coord)'=0,
    v_b,coord=-beta-N*chi'/(L²*Gamma).                       (4)

Thus 4pi integral p_chi dr is conserved except for its specified boundary
flux. Matter density and current are evolved together, rather than imposed
independently. Pressure, velocity dispersion or a controller requires its
own ordinary-matter action/stress and must replace this dust approximation
where appropriate.

## 3. An explicit Hamiltonian suitable for a constraint-preserving solver

Use canonical momenta with the overall 4pi omitted:

    p_L=-2M²*R²*K_t,
    p_R=-2M²*L*R*(K_r+K_t),
    p_j=C*L*R²*w_j*m_j*v_j.

Then H_total=4pi integral dr H, with

    H=N[ -p_L*p_R/(2M²*R)+L*p_L²/(4M²*R²)
          -(M²/2)*L*R²*R3
          +sum_j p_j²/(2C*L*R²*w_j*m_j)
          +C*L*R²*(V+DeltaU-B*h(a))
          +p_chi*Gamma ]
       +beta*H_r,

    H_r=p_R*R'-L*p_L'+sum_j p_j*x'_j+p_chi*chi'.           (5)

IMPORTANT: the bracket multiplying N is NOT lapse independent, because
a=N'/(NL). One must use the functional lapse variation, not set that
bracket to zero as if it were the GR Hamiltonian constraint.

The position and mode-momentum equations are

    R_dot=beta*R'-N*p_L/(2M²*R),
    L_dot=(beta*L)'+N[-p_R/(2M²*R)+L*p_L/(2M²*R²)],
    x_dot_j=beta*x'_j+N*p_j/(C*L*R²*w_j*m_j),
    p_dot_j=(beta*p_j)'
       -N*C*L*R²*w_j[kappa*delta_j²*x_j+u4*x_j³
                                      -kappa*delta_j*h(a)],
    p_dot_L=-delta H_total/(4pi delta L),
    p_dot_R=-delta H_total/(4pi delta R).                   (6)

The last two are completely specified functional derivatives of (5), not
unknown stresses. For an implementation using only first spatial derivatives,
the curvature part can equivalently be integrated by parts:

    -(M²/2)*N*L*R²*R3
       = -M²[N*L+N*R'²/L+2N'*R*R'/L]
                                  +[2M²*N*R*R'/L]'.        (7)

Retain its boundary term or the equivalent chosen metric boundary action.
Taking functional derivatives of either form with consistent endpoint data
gives the same bulk evolution. This avoids inventing a pressure closure.

The two constraints are H_r=0 and delta H_total/delta N=0. With
T_osc=sum_j w_j*m_j*v_j²/2, the latter is transparently

    (M²/2)[R3+4K_r*K_t+2K_t²]
                                      =rho_b,normal+rho_mode,

    rho_mode=C[T_osc+V+DeltaU-B*h(a)+a*B*h'(a)
                       +(R²*B*h'(a))'/(L*R²)].             (8)

Both the divergence and the a*B*h' contribution are compulsory. At a
stationary mode minimum they reproduce the full earlier J(Y) stress; using
only the oscillator energy or a substituted static mu would miss them.

The mode equation can also be checked without canonical variables:

    m_j[(partial_t-beta*partial_r)v_j/N+theta*v_j]
           +kappa*delta_j²*x_j+u4*x_j³=kappa*delta_j*h(a).    (9)

Retaining all metric equations, modes and covariantly conserved ordinary
matter also retains the clock equation through the diffeomorphism identity
in unitary gauge, where grad T is timelike and nonzero. A numerical scheme
must preserve the constraints and their consistency conditions; merely
evolving (9) with a prescribed N would discard that clock equation.

## 4. What is and is not an elliptic solve

At fixed canonical data, the functional lapse constraint includes a radial
second derivative with principal coefficient, after dividing by L*R²,

    C*B*h''(a)/(N*L²),
    h''(a)=-3a/g_s²*(1+a²/g_s²)^(-5/2).                    (10)

Where B*h'' is nonzero it is a second-order radial lapse equation. Its
corresponding principal quadratic form is positive when B*a>0. It is NOT
uniformly coercive: it degenerates at a=0 or B=0, and excited polarization
can change its sign or pass through zero. An implementation must not hide
this with an arbitrary pinning coefficient or new spatial gradient.

This does not mean the unexcited finite-band problem is undefined. Its
linear constraint consistency is precisely the regular system already
derived in FINITE_MODE_CONSTRAINED_RESPONSE.md. In the local weak-field
spherical limit, with regular center and no incoming polarization flux,

    B_dot=0,
    a=[sum_j w_j*kappa*delta_j*Omega_j²*x_j]/Gamma_resp,
    Gamma_resp=sum_j w_j*(kappa*delta_j)²/m_j >0,
    Omega_j²=kappa*delta_j²/m_j.                            (11)

Equation (11) is obtained by preserving B twice using the mode equations,
not by dividing the degenerate coefficient (10). The independent tangent
oscillators retain the positive interlacing spectrum already proved.
More generally the full nonlinear system is a differential-algebraic
constraint problem. General existence, nonlinear well-posedness and uniform
continuum hyperbolicity have not been proved by this reduction.

The metric null coordinate speeds are -beta+/-N/L; dust is timelike with
the velocity (4). Modes have convective time derivatives along the normal
and no independently supplied radial wave-speed term. Radial constraint
solves and this local oscillator structure are calculable, but are not a
license to assert a new signal cone from a density-of-states plot. One must
test the coupled principal/constraint system on the actual chosen branch.

## 5. Exact invariant branch: growing matter need not polarize the clock

Take ANY GR solution with cosmological constant

    Lambda=C*DeltaU/M²=2DeltaU/K_b

and its ordinary conserved matter. Locally choose a hypersurface-orthogonal
geodesic unit normal, equivalently a proper-time function satisfying
g^{mu nu} T_,mu T_,nu=-1 before its congruence develops a caustic. Set

    a_mu=0,   y_j^mu=0,   v_j^mu=0.                        (12)

The mode equations have zero force, so this is a solution. Every variation
of the nonconstant extra action vanishes there: the potential and kinetic
terms are quadratic or higher in y, and the source term is bilinear in
h(a) and y with h(0)=0. The remaining stress is exactly -C*DeltaU*g_mu_nu.
The clock equation is also satisfied. This proves an invariant branch of
the SAME parent, not a change to its static force law.

An enhanced stationary clock typically has a_mu!=0 and nonzero prepared
polarization. Branch (12) shows that such a state cannot be inferred from
the baryonic density alone. It does NOT show that every initial state,
boundary condition or native formation history selects the geodesic branch.
Nor is it a global caustic-free theorem. It supplies a precise null
preparation against which a proposed record/clock formation mechanism can
be tested.

### Fully dynamical spherical benchmark, including the matched constant

For ordinary comoving dust, choose N=1, beta=0, chi=t and

    L=R'/sqrt(1+2E(r)),
    R_dot²=2G*M_b(r)/R+2E(r)+Lambda*R²/3,
    rho0=M_b'(r)/(4pi*R²*R'),
    x_j=p_j=0.                                              (13)

This is the standard Lambda–Lemaître–Tolman dust reduction; its metric and
first integral are given, for example, in
[Enqvist, section 2, equations (2.9)–(2.13)](https://arxiv.org/pdf/0709.2044).
Here M_b is the gravitational mass function, not an extra dark component.
The actual proper rest mass is 4pi integral p_chi dr and is also conserved;
for E!=0 it need not numerically equal M_b at a given outer shell.

The especially small E=0 benchmark has the explicit expanding solution

    R³=(6G*M_b/Lambda)
             *sinh²[sqrt(3Lambda)*(t-t_B(r))/2].             (14)

It can use a smooth positive mass profile and initial R(t0,r), which fix
t_B through (14), not through a desired enhancement. Keep M_b'>=0 and
R'>0 on the comparison interval. Density changes physically while the
normal acceleration and every response mode remain exactly zero.

Useful exact checks for a future integrator are BOTH constraints, the
mode null solution, dust continuity and the invariant mass relation

    m_MS,sub=R/(2G)*[1+((R_dot-beta*R')/N)²
                       -(R'/L)²-Lambda*R²/3] = M_b(r),
    partial_t m_MS,sub=0 on (13),
    partial_t(4pi integral p_chi dr)=boundary rest-mass flux. (15)

Here m_MS,sub is the Lambda-subtracted Misner–Sharp mass. The full geometric
Misner–Sharp mass is m_MS,sub+Lambda*R³/(6G); it is not constant along an
expanding shell when Lambda is nonzero.

This benchmark needs no physical mode inertia or native age because the
modes remain zero for every positive finite set. It can qualify the coupled
constraint/matter implementation now; it cannot validate an enhancement.
Dust shell crossing or a failed timelike foliation ends this approximation,
not an excuse to continue with an unreported reset.

## 6. The first sourced linear discriminator

The same conclusion is visible before a nonlinear simulation. In a local
weak-field radial description, the leading metric constraint is

    Phi'=G*M_b(<r,t)/r²+B(r)/K_b,                            (16)

after regular-center integration and specified boundary data. Its linear
mode/clock charge has B_dot=0. Mode evolution determines the normal
acceleration a from (11), while the normal's physical radial velocity obeys

    v_clock_dot=a-Phi'                                      (17)

at this local linear order. Ordinary density/current must still satisfy
their conservation equations. With initially x_j=v_j=0, equations
(11), (16), (17) give B=a=0: the clock falls freely while the ordinary
Newtonian potential changes. There is no automatically produced linear
enhancement to assign an outer response time.

For nonzero prepared polarization, (16) instead retains an independently
specified signed initial charge and the finite internal collective modes.
On an expanding homogeneous background the corresponding comoving charge
is conserved and its linear density decays as a^-3, as separately checked
in the cosmology lane. A spatial charge profile or excited state must come
from actual preparation; it must not be chosen to reproduce a galaxy curve.
These local linear formulas are validation limits of (2)–(9), not a
substitute for their nonlinear galaxy or cosmological evolution.

## 7. Can a fixed source profile be grown with an explicit current?

Yes as a controlled source experiment, but continuity and work constrain
the proposal. In a weak-field near-zone example, if
rho_b(r,t)=f(t)*rho_*(r), regular-center continuity requires

    j_r(r,t)=-f_dot(t)*M_*(<r)/(4pi*r²),
    v_b=j_r/rho_b.                                          (18)

One cannot start a positive fixed spatial density from f=0 with this finite
velocity prescription, or keep a compact outer boundary empty while
nonzero flux crosses it. A supply region/boundary, a finite initial
population, or explicitly modeled production/transfer is required.
For an isolated closed system, redistribute existing matter through (3)–(4)
instead of increasing its total mass by hand.

Continuity alone is also insufficient. The prescribed current must satisfy
its momentum equation. In the same nonrelativistic radial dust notation,
the controller force density needed to impose it is

    f_ext=partial_t(rho_b*v_b)
             +r^-2 partial_r(r²*rho_b*v_b²)+rho_b*Phi'.       (19)

Its power is 4pi integral r²*f_ext*v_b dr, in addition to boundary energy
flux. Pressure/anisotropic support requires the corresponding stress terms.
In the full relativistic system the controller must have a conserved total
stress together with the source; its force and energy cannot disappear
from the Einstein/clock consistency conditions. Prescribing rho(t,r) while
ignoring that controller generally fails those conditions.

Thus one common source-growth history can be tested, but it means either
an evolved matter initial state or an explicitly supported current, not
an independently prescribed acceleration at every radius. The clamped
six-trajectory test remains useful for the mode integrator and source-work
identities; it does not select the solution of (2).

## 8. Practical next calculation and required data

The smallest implementation can use a finite positive mode set and beta=0
normal threading, evolve the canonical equations, and solve/preserve the
lapse and radial constraints with regular-center and explicit finite-domain
metric/clock boundary data. At the center require smooth radial fields:
R=O(r), R'/L->1, x_j=O(r), a=O(r), and no hidden point charge. Stop the
claimed domain if shell crossing, lapse degeneracy without a resolved
consistency branch, or loss of a timelike smooth clock occurs.

First reproduce (13)–(15), including nontrivial density evolution. Then
reproduce the sourced linear charge/tilt relations and the earlier finite-
mode determinant. These are exact, small, independently calculable
benchmarks; no NGC3198 fit or physical native inertia is needed to test them.

Only then compare two fully specified preparations of the SAME baryonic
system—for example, the geodesic null preparation and an independently
derived record-bearing clock/mode state—with identical outer conditions.
The output is Phi or the metric's circular/light response, the physical
normal acceleration, current, mode state and full constraint/work residuals.
An outer enhancement or delay would be an output of that solution, not
mu_age inserted into (16).

The remaining physical inputs are precise: the native source/contact and
volume matching, positive or active response spectrum and inertia, actual
initial clock/mode state, ordinary matter phase-space/support, and boundary
history. NATIVE_SOURCE_BRIDGE_DECISION.md and the existing writer-pulse
evidence constrain the actual-state matching; they do not authorize replacing
it with a passive minimum. No arbitrary halo profile, new damping constant
or radius-dependent age has been added to fill these inputs.
