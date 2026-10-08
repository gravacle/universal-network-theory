# Conserved stellar support and the time dependent network response

2026-10-03. The current calibrated K(X) comparison can be given a conserved
ordinary stellar source without adding dark support. Its slow gravitational
response can also be separated from its rapid material oscillations. These
are two prerequisites for a longer source calculation, not a formed galaxy,
a native derivation or evidence of observational superiority.

The action, functions, two tested widths and cosmic budgets are unchanged.
This note does not promote the wider width to an adopted physical solution.
It preserves the completed thermal and source results in the existing
NETWORK_THERMAL_ASSUMPTIONS_AND_OBSERVABLES_V001.md.

## A supported source that conserves ordinary matter and work

A declared spherical collisionless preparation consists of stellar shells
with random orbital planes. Let b denote enclosed ordinary rest mass,
R(t,b) their physical areal radius and ell(b) their specific angular
momentum. Before shell crossing, the weak-field equations are

    Rdot=V,
    Vdot=(addot/a)R-g_pec(t,R)+ell²/R³, ell_dot=0,
    rho_b=1/(4pi R² R_b), p_t=rho_b ell²/(2R²).

Here g_pec is supplied by the complete evolving metric response. If the
solver instead supplies TOTAL inward areal acceleration, do not add the
background term twice. Initial instantaneous balance chooses

    ell²=R³[g_pec-(addot/a)R] >= 0.

After that choice ell is conserved. A later force change moves shells;
it cannot be canceled by changing ell to keep their density fixed. This is
ordinary orbital support, not a free supporting apparatus. Profile, mass,
size, angular-momentum preparation, radial velocity transition, compensation
and assembly epoch are counted source assumptions. They are not predicted
native formation, and may not be retuned after scoring the force.

For the general metric ds²=-N²dt²+A²(dr+beta dt)²+R²dOmega², radial
canonical momentum p_b and conserved ell give

    e=sqrt(1+p_b²/A²+ell²/R²), H_b=N e-beta p_b,
    rdot=N p_b/(A²e)-beta,
    pdot=-N_r e+(N/e)(p_b² A_r/A³+ell² R_r/R³)+beta_r p_b.

If n_b is slice rest mass per normal proper volume, the normal-frame source
is rho=n_b e, radial momentum n_b p_b/A, radial stress n_b p_b²/(A²e)
and tangential stress n_b ell²/(2R²e). Rest mass obeys

    partial_t(AR² n_b)+partial_r(AR² n_b rdot)=0.

The particle energy satisfies dH_b/dt=partial_t H_b; in the Newtonian
limit d[V²/2+ell²/(2R²)+Phi_tot]/dt=partial_t Phi_tot. Field and orbital
energy must both be included. The static necessary relation is

    p_t=rho R(dlnN/dR)/2,
    ell_circ²=R³(dlnN/dR)/[1-R(dlnN/dR)].

Here rho is ENERGY density. Timelike circular orbits require
0<=R(dlnN/dR)<1. Stability against a radial test displacement in a fixed
static field requires d ell_circ²/dR>0, not proof of coupled-field stability.
The standard conserved-source construction is described, for example, in
[Szybka and Rutkowski](https://link.springer.com/article/10.1140/epjc/s10052-020-7948-0).
We use it for visible matter, not the dark-halo interpretation sometimes
assigned to this mathematical construction.

The earlier expanding CMC dust data cannot be reused unchanged. A core
with physical Rdot=0 has normal radial velocity -HR/F on that slice,
F=R_r/A, so both its momentum density and orbital kinetic energy change
the constraints. Only the core is supported; it must be joined to expanding
outer ordinary matter with ell tending to zero and a nonnegative compensated
density. No compensation profile or updated constraints have yet been
solved in this note. At R_b=0, a multistream description is required.

## An exactly resolved local source response

At a frozen epoch in the LINEAR, weak-metric, subhorizon limit put
Q=X, m=KX, d=KXX, mu=m/Q, eta=C/KB. With scalar gradient w and vector
velocity sigma, p=w+Q sigma. The local field equations give

    wdot=grad(deltaX)+Q gradPhi,
    pdot=grad(deltaX)+Q E,
    Zdot=QD, E=(Z-Cp)/KB, D=eta(Z-2p),
    Zddot+eta Q² Z=-2eta Q grad(deltaX).

Define S=delta_m+divZ/Q and Y=divZ/Q. Then

    Sdot=mu divw, 2lapPhi=rho_source+QS,
    deltaX=(S-Y)/d.

The important cancellation is in the effective gravitational source QS;
delta_m by itself does not give the metric response. At Fourier wavenumber
k, with rho_source in the inherited 8pi Gcos normalization,

    Sddot=(Jg-W)S+W Y+f,
    Yddot=B S-(M²+B)Y,
    Jg=mQ/2, W=m k²/(Qd), B=2eta k²/d,
    M²=eta Q², f=m rho_source/2.

The determinant is exactly -Jg M². There is one positive growth exponent
lambda² and one negative oscillatory eigenvalue -nu²:

    lambda² nu²=Jg M²,
    nu²-lambda²=M²+B+W-Jg.

The positive root is a gravitational Jeans direction, not a negative-norm
material ghost. Eliminating a positive rapid oscillator does not make
the full gravitational binding energy positive. For a constant source
with zero initial material perturbations, the exact response is

    S/f=a[cosh(lambda t)-1]/lambda²+b[1-cos(nu t)]/nu²,
    a=(M²+B+lambda²)/(nu²+lambda²), b=1-a.

As k grows, b tends mu/(2eta+mu), about3.80e-7 at Q100. The omitted rapid
contribution has the analytic absolute envelope 2|f b|/nu². This small
metric-source residue does not mean all charge derivatives or fields have
the same relative error; their reconstruction must keep the rapid residue
when checking branch boundaries and nonlinear constitutive terms.

The source-kernel calculation is complete for the two existing widths and
k=1/(5 kpc),1/(50 kpc). All frozen numerical gates pass, with maximum
error1.77e-12. It checks characteristic identities, initial data, both full
ODEs and an independent RK4 integration over two rapid periods. It does
not integrate a new cosmology or simulate a finite supported source.

At t_dyn=L/sqrt(kappa)=.00388175 H0^-1, motivated by the previously
declared L=5 kpc and kappa=1e-7, the potential enhancement is about
2.83654e-6 for all four rows. Ht is.00388: this is a local frozen-epoch
benchmark, not a controlled Hubble-age extrapolation. The leading response
is mQ t²/4, linear in source mass. It is not the nonlinear square-root mass
law required by BTFR. Any such law must arise in the nonlinear response
and formed state, not from relabeling this susceptibility.

Receipt: INVARIANT_CLOCK_LOCAL_SOURCE_KERNEL_V001_RESULT.json, with source,
dependency and input hashes. Source and response are independently checked
by endpoint_equations_check; conserved shell support by
handoff_plan_review_v005. These are internal equation checks, not external
observational validation.

## Expansion and slow history must survive the reduction

In Newtonian slicing define T=divZ/Q, qdot=Qdot/Q and
Sc=delta_m-3mPhi+T. Linear conservation and the metric constraint instead give

    Sc_dot+3H Sc=div(mu w)-qdot T,
    2lapPhi-6H(Phidot+H Phi)=delta_rho_b+Q(delta_m+T).

Neither equation imposes zero flux or erases preparation dependence. The
linear vector equation retaining background drift is

    Zddot+(3H-qdot)Zdot
      +[eta Q²+eta H Q+2H²+2Hdot-2Hqdot]Z
      =-2eta Q grad(deltaX)-2eta Q Qdot sigma.

For nonlinear spatial J, let F(p)=[2+KB j(p²)]p and A=F_p=2+KB jt>0
in the radial direction. Before convective terms are restored, exactly

    p=F_inverse[Z-(Zdot+2HZ)/(eta Q)].

Its first derivative correction is essential. With p0=F_inverse(Z),
p=p0-A^-1(Zdot+2HZ)/(eta Q)+..., and

    grad(deltaX)+Q(1+j)p0
      =H p0-2H A^-1 Z-Qdot sigma
       -(partial_t+H)[A^-1(Zdot+2HZ)/(eta Q)]+... .

The cancellation of the leading Zdot terms permits slow evolution; setting
p_dot or the scalar current to zero at the outset would destroy it. The
nonlinear elliptic reconstruction still has to satisfy its branch and
derivative-expansion conditions. Cosmological matching comes from retained
incoming/initial data, not an adjustable phase per galaxy.

## Immediate physical test before a long source run

Even while S is small, sigma and w/Q can grow to an ordinary orbital
velocity with opposite signs. Their spatial advection can become important
on t_dyn, far earlier than H^-1. A geodesic-like vector congruence might
focus while the stars remain orbitally supported. A coordinate caustic in
the old freely falling dust chart is not by itself an invariant vector
singularity. The next task is to determine this nonlinear advection/
focusing regime and whether the full shared source response remains regular.
Do not extend the frozen linear kernel for a Hubble time or discard
advection merely because the metric-source perturbation is small.

## Nonlinear source conservation and the rejected cold shortcut

Within the same weak-NR equations, define FULL S=m+T,T=divZ/Q, not only
its perturbation. Radially Zdot+2HZ+v divZ=QD. With time derivatives at
fixed comoving position, partial_t(divZ)=divZdot-HdivZ; hence exactly
within this reduction

    Sdot+3HS+div[v(S-m+Qmu)-mu p]=-qdot T.

Only after checking Q approximately equals X may the flux be shortened to
vS-mu p. S contains a divergence and is not positive physical mass by
definition. This is an effective geometric source, not a halo of record
counts. Its formation and work must nevertheless be accounted for.
The useful exact force split in these variables is

    E-Z/2=D/2+(C/2)j p.

The nonlinear part is outward only for p>0. Dropping D because it is a
derivative would remove a potentially important central acceleration.

There is also an important mixed-variable correction to the slow solver.
With L=partial_t|R+(HR+v)partial_R, a=H+v_R,b=2H+2v/R, the j=0 relation
is

    X_R+(Q+b-a)Z/2
      =-(L+a)[(L+b)Z/(2eta Q)]-Qdot v-p p_R/Q.

For constant homologous physical expansion h, the leading coupled
elliptic equations imply

    [-lap+Q d(Q+h)/2]Z=-Q grad S.

At Q+h=0 this remains a finite-k Poisson problem. Do NOT divide by Q+h
and call the resulting artificial pole a full-model singularity. Negative
Q+h changes a lower-order term, not principal ellipticity; monitor the
actual boundary-conditioned operator and derivative correction. Use X,Z
jointly or Z as the elliptic variable. This qualification corrects a
provisional pointwise-inversion concern raised during the analytical review.

A prospective cold-displacement limit neglecting the mu p transport and
using m approximately mbar gives shell label R0, radius R and velocity v:

    Z=Q mbar(R0³-R³)/(3R²), D=-mbar v,
    [2+KB j(p²)]p=Z+mbar v/eta,
    Rddot=-g_b(R)-mbar v/2+(C/2)j p.

This constructive approximation retains compression of the geometric
source and a nonlinear interaction without supplying a fitted halo. But
it is NOT an accepted substitute for the full model. Its initial inferred
X shift is -mbar Phi_b/(2eta), not exactly the old uniform-X preparation.
Small missing enclosed charge also need not mean small force error when
the background Gauss terms nearly cancel.

Most decisively, this cold approximation has an analytical smooth-center
caustic. For a harmonic source core and R=b_c(t)R0+o(R0), j p is O(R0²),
so its central slope satisfies

    b_c_ddot+(mbar/2)b_c_dot+omega_g² b_c=0,
    b_c(0)=1, b_c_dot(0)=0.

For gamma=mbar/4, omega_d=sqrt(omega_g²-gamma²), its first zero is

    t_c=[pi/2+atan(gamma/omega_d)]/omega_d.

At the declared weak galaxy scale this is approximately1.57 t_dyn.
Finite-radius shell bounces cannot erase this central limit. No shell
simulation was launched after identifying it: a finite inner grid could
mistake an unresolved central failure for a regular source solution.
This rejects the cold shortcut as a globally regular continuation, not
the full K(X) action. Its omitted current and clock response are precisely
the terms that might change the result and must now be retained.

Related Maxwell-vector focusing is a known structural issue; see
[Contaldi, Wiseman and Withers](https://arxiv.org/abs/0802.1215).
Their TeVeS result is not an exclusion of this different K(X) action.

The next exact derivation is polar-areal canonical evolution with the same
matter action and conserved orbital source. Unlike a freely falling
geodesic coordinate grid, this slicing need not fail at a coordinate
congruence crossing. The test must track the invariant vector expansion,
acceleration and Raychaudhuri balance, scalar domain and Legendre inverse,
not identify a grid failure with a physical caustic. Polar constraints,
lapse, and the source kinetic energy must be derived before execution;
no new physical parameter or data fitting is licensed by changing gauge.

## Exact polar areal equations for the next source evolution

The polar reduction is now independently derived. Vary the original
canonical action BEFORE imposing pi_a=0, otherwise the lapse condition is
lost. Put V=AR², sigma=u/A,c=sqrt(1+sigma²),w=phi_R/A,Z=pi_u/(2R²),
q=sqrt(X²+w²),Q=cq+sigma w,p=sigma q+cw. Q here is the local vector
contraction, not the constant Q0 used in the preceding short-time limit.
At each point solve the unchanged scalar momentum relation

    M=pi_phi/(2V)=m q/X+sigma D,
    m=KX, e=(Z-Cp)/KB, D=C[e-(1+j)p],
    Jcurrent=cD-(m/X)w.

With Ecal=KB e²+C p²+CJ-2K and ordinary canonical Hamiltonian H_b,
the bulk Hamiltonian is

    H[N]=integral N[-2A+2/A-4R A_R/A²
                      +V Ecal+pi_phi q+c pi_u_R+H_b] dR.

The integration by parts of -pi_u(Nc)_R has an associated boundary term;
it cannot be ignored in source work or boundary conditions. The exact
canonical matter equations in this gauge are

    u_dot=N A e-(Nc)_R,             phi_dot=N q,
    pi_u_dot=2N R² QD/c-N sigma pi_u_R/(A c),
    pi_phi_dot=-2 partial_R(N R² Jcurrent).

There is no extra k*u term: u=A sigma already carries that metric factor.
The field energy and radial pressure in the inherited 8pi Gcos units are

    rho_c=Ecal/2+M q+c pi_u_R/(2V),
    P_c=-Ecal/2-sigma QD/c-w Jcurrent+sigma² pi_u_R/(2cV).

In particular the energy is not simply Xm-K in an inhomogeneous state.
The radial metric and lapse equations are

    A_R=A(1-A²)/(2R)+A³R(rho_c+rho_b)/2,
    N_R/N=(A²-1)/(2R)+A²R(P_c+P_r,b)/2.

For ordinary particle restweight nu_b, normal energy e_b and canonical
radial momentum p_b, H_b=nu_b e_b and the shift generator is -nu_b p_b.
Thus the eliminated momentum and independent radial-flux check are

    pi_b=R[u pi_u_R-pi_phi phi_R+nu_b p_b],
    A_dot/A=N[-u pi_u_R+pi_phi phi_R-nu_b p_b]/(4AR).

The sign gives decreasing enclosed metric mass for outward ordinary flux.
For a distribution, sum its momentum and stresses; do not replace it with
a fixed rest-density insertion. A second independent Einstein check is

    pi_b_dot=-4R[(N/A)_R+R(N_R/A)_R]
             +2N V(Lvec+2K)+4N V P_t,b,
    Lvec=KB e²+2C e p-Cp²-CJ.

Regularity requires A=1+O(R²),u,w,Z=O(R),pi_u=O(R³),pi_phi=O(R²).
Retain the scalar inverse derivative

    (q/X)[d-(m/X)w²/q²-C sigma² X²/q²(2/KB+jt)].

This changes no physical action or parameter. Both reviewers confirmed
the complete pi_u_R terms: V001 already contains sigma² pi_u_R/c; there
was no missing historical term. That concern was a reading error, not a
reason to alter or rerun the frozen source results.

For a local polar representation of FLRW, A=1+H²R²/2+O(R⁴),
N=1-(H²+Hdot)R²/2+O(R⁴),sigma approximately HR and w approximately
-Q HR. X also has the corresponding time-slicing variation at O(R²).
This is not an asymptotically flat outer condition. Domain/current and
incoming-mode controls must still connect the nonlinear core to its
specified cosmological preparation. A long domain-wide explicit run has
NOT been launched: first implement the existing equations with conserved
ordinary source and quantify cost/boundary error on a bounded interval.

## Full central current can change the focusing verdict

With central proper time, sigma=s R, w=w1 R, Z=z R and
X=Xc+chi R²/2 at leading order, independently derived equations are

    p1=Xc s+w1, e1=(z-Cp1)/KB, D1=eta(z-2p1), mu=m/Xc,
    d Xc_dot=-3(D1-mu w1), z_dot=Xc D1-3s z,
    s_dot=e1-g1-s², w1_dot=chi+w1²/Xc+Xc g1,
    g1=(rho_b+3P_b+Xc m+2K+3z)/6.

Here P_b is isotropic ordinary pressure at a regular centre. Hence

    s_dot+s²=D1/2-(rho_b+3P_b+Xc m+2K)/6,
    d/dtau(s+m/6)=-s²+m w1/(2Xc)-(rho_b+3P_b+Xc m+2K)/6.

The invariant expansion is Theta_U=3s and acceleration divergence is3e1.
Unlike the rejected cold approximation, D1 is dynamical. Defocusing is
possible only through actual current/charge/phase dynamics, not inserted
pressure. The independent clock curvature chi requires higher radial
current coefficients; there is no exact finite-centre-jet closure for a
generic compact source. J proportional to |p|³ also permits subleading
nonanalytic radial terms. The homogeneous FLRW specialization is a control,
not a replacement for the compact-source problem.

## Bounded polar source implementation

The new implementation retains two ordinary populations: a circularly
supported core and expanding ordinary background with a nonnegative
compensating density. The declared core profile is Plummer times
[1-(R/20L)²]^4 inside20L, L=5kpc; Gaussian compensation width300L.
These are preparation assumptions, not derived formation or fitted dark
profiles. kappa1e-7 normalizes the coordinate density integral, not the
total gravitating energy after orbital/metric corrections. Both species'
momenta, angular momentum and restweights evolve by their Hamiltonian.

Technical pilots are preserved separately. V001/PILOT01 fails central mass
quadrature (Hamiltonian error .0304); V002/PILOT02 factors out the regular
R² measure, reducing that error to2.23e-5. V002's tiny negative empty-source
tail is not accepted as positivity. V003/PILOT03 instead uses conservative
slope-limited ordinary restweight transport. Its initial orbit balance is
3.13e-16 relative and supported restweight is conserved to reported precision.
Its raw angular spatial derivative suffers severe Newtonian cancellation;
this is not a field-theory failure or a passed trajectory.

V004 retains that raw result and tests the equivalent equation

    pi_b_dot/R³=2NA[anis/R-P_R-g(rho+P)],
    anis=2[Ze+sigma QD/c+w Jcurrent-sigma² divZ/(Ac)+Pt_b-Pr_b].

This follows from the radial constraints and is independently reviewed.
It is an angular stress/time-evolution check CONDITIONAL on those
constraints, not independent evidence for the canceled spatial derivatives.
P_R uses a spatially constant K reference and cancellation-free K(s)-Kref.
Mass-based metric time tangents use two increments. Existing numerical
gates stay1e-3 (inverse2e-12); failed pilots are not promoted.

The first V004 interval is prospectively0.25 t_dyn on160 sinh-grid cells,
with one local numerical worker and bounded checkpointing. Initial polar
FLRW data retain the R² cosmic-time shift; outer extrapolation and higher
orders still require domain/initialization controls. The field trajectory
does not become scientific evidence merely by completing this pilot.

The quarter-orbit spatial comparison is now finished and FAILS: CENTRAL01
and CENTRAL02 agree in gravity/Theta at1.29e-4/1.37e-4, but Z-change and
canonical clock-charge-change discrepancies are .931 and1.758. Both
individual runs passed the implemented equation/conservation checks.
Those checks alone did not ensure convergence of the small field response.
The failed comparison is INVARIANT_CLOCK_POLAR_COMPARE_GRID01_RESULT.json.

A saved-state audit, INVARIANT_CLOCK_POLAR_CHAIN_RULE_V001_RESULT.json,
identifies a nonlinear q_R chain-rule defect. It decreases by15.29 for
twice the resolution (consistent with fourth-order discretization), but
is significant relative to the small physical p dynamics. This diagnoses
a numerical contribution, not the full cause by assertion.

An exact mixed-variable formulation evolves p rather than phi_R. Put
Q=sqrt(X²+p²), q=cQ-sigma p,w=cp-sigma Q. With kbar=A_dot/A,

    F=NcX X_R/(Aq)+Nw p_R/(Aq)-NQp sigma_R/(Aq c²)
      +NQe/c-Qp kbar/(q c),
    p_dot-(sigma X/q)X_dot=F,
    M_X=d q/X+m(c/Q-q/X²), M_p=mw/(XQ)-sigma C(2/KB+jt),
    M_sigma=D-mw/(cX), M_Z=sigma eta,
    X_dot=[cp_dot/A-M kbar-M_p F-M_sigma sigma_dot-M_Z Z_dot]
          /[M_X+M_p sigma X/q].

Here cp denotes pi_phi/(2R²) only when written as cp_dot; the product
c p elsewhere is written without ambiguity in the implementation. The
fixed-p algebraic inverse uses M_X, while the denominator in the coupled
time update is exactly the original fixed-w Schur. These distinctions and
the analytical lapse-gradient cancellation are independently reviewed.
The canonical integrability residual is separately reconstructed; changing
variables does not waive any equation or refinement gate.

V005/MIXED01 has now completed the same quarter-orbit interval on160 cells.
Its implemented checks, including reconstructed canonical integrability,
pass. Minimum clock s is .178760 rather than V004 coarse .152679, while
the gravity/compression prediction is essentially unchanged. MIXED02 is
the sole running320-cell control; this is not yet a qualified solution.

The invariant diagnostic is also explicit. For F_tR=NA e,
a^t=sigma e/N,a^R=c e/A. Let j_r be outward normal momentum density and
P_t,c=(Lvec+2K)/2. Then

    R_UU=c²rho-2c sigma j_r+sigma²P_r+(-rho+P_r+2P_t)/2,
    shear²=(2/3)[Theta-3sigma/(AR)]²,
    U(Theta)=(c/N)Theta_t+(sigma/A)Theta_R,
    div(a)=(sigma/N)e_t+(c/A)e_R+e²+2ce/(AR).

Track the full Raychaudhuri balance. For a followed vector bundle,
Rdot=N sigma/(Ac), dproper_tau=Ndt/c and
Jacobian=AR²c*(partial R/partial R0)/(A_i R0²c_i).
A converged decrease followed by increase of this physical bundle volume
would show resolved reversal in the tested interval. A finite value at
the innermost cell is not proof against a central caustic. A failed grid
test is not a physical singularity. The exact U-frame charge density and
relative flux are (m/X)Q and D-(m/X)p, respectively; charge transfer must
be distinguished from geometric compression. All11 lanes remain OPEN.

The mixed-p series has now completed N160,320,640,960 at the SAME0.25 t_dyn
endpoint and nearly the same physical timestep. All individual trajectory
gates pass. MIXEDGRID01 maximum.00669486 and MIXEDGRID02 maximum.00178751
decrease, but MIXEDGRID03 maximum.0015283612 is dominated by a nonmonotonic
charge-change error. Its ordinary-profile errors are below.000337 and
gravity/Theta below5e-7. This still FAILS the frozen.001 full-state gate.
The next control is SAME N960 with dtfactor1.5 instead of3, not another
spatial sweep. No singularity or regular-source verdict is earned yet.

## Unadopted compression-stiffness contingency

Independent analytical review examined adding -c_theta*(nabla.U)^2 inside
the existing action bracket. It is one NEW universal coefficient, not a
native derivation, not adopted, and not yet needed by a proven caustic.
Aligned flat FLRW would satisfy

    3*(1+3*c_theta/2)*H^2 = rho_b/Mplanck^2 + X*K_X - K,

with a^3*K_X constant unchanged. A strictly stationary aligned U has
Theta=0, so this term and its first variation vanish there. That fact does
not extend to a tilted/cosmologically matched galaxy. Conditional on the
old static GN dictionary, rG becomes rG_old/(1+3*c_theta/2); positive
stiffness therefore changes early expansion AND the late calibration.
It cannot be a free galaxy repair with old cosmic budgets left implicit.

On a fixed weak metric it adds K_B*v_tt containing
c_theta*grad(div(v)). With scalar mixing, the fixed-metric high-frequency
diagnostic polynomial is

    K_B*d*s^4-[K_B*(C+mu)+C^2+d*c_theta]*s^2
       +c_theta*(C+mu)=0, mu=m/X.

These are NOT the constrained theory's established physical speeds.
The lapse, shift and unit-vector constraints change; existing polar
momenta cannot merely receive an extra force. A complete constrained
quadratic action and local/preferred-frame/radiation tests would be
required before adoption. No coefficient chosen or fit performed.
Relevant background and motivation (different theories, not inherited
observational success): https://arxiv.org/pdf/0801.1547 and
https://arxiv.org/pdf/0802.1215 .

## Clock-charge discrepancy and a targeted wave-mesh control

The SAME-grid half-step run MIXED05B completed from MIXED05's checkpoint;
MIXEDTIME01 FAILS at.00135545 charge-change error. Gravity3e-14 and
Theta7.2e-11 agreement do not establish full-state convergence. This could
include time damping, amplified roundoff or spatial-wave interaction; do
not assert a unique cause from this test alone.

INVARIANT_CLOCK_POLAR_CHARGE_AUDIT_V001_RESULT.json reuses saved states.
The split and combined current-divergence forms differ below5e-14 relative;
inner integral-budget defects are below5e-7. The latter use the actual
point quadrature Q(R)=2*(massint@cp), not ordinary FV restweight volumes.
No evidence here warrants a new scalar conservation law/discretization.
Inverting the existing interval mass matrix is also not an automatic
remedy: its uniform-grid cubic-average symbol has a checkerboard zero.

For a fourth-order centred derivative, k_eff*h=(8sin(kh)-sin(2kh))/6.
Its maximum is1.37222. With h~dx*R, an outgoing kL~1 packet has a local
numerical turning radius~133L atN960, and estimated round-trip.205 t_dyn.
This WKB argument offers a TESTABLE numerical-reflection hypothesis, not
proof. Halving dt may change unresolved-wave damping; alternatively there
may be a different temporal/roundoff issue.

V006 prospectively tests a resolved buffer: retain original core nodes,
cap spacing at.125L through600L, then increase spacing gradually to the
same.012 outer extent. At the old measured speed, ray travel is325.47L
in.25 t_dyn. No physical absorption, new boundary, source or coupling is
introduced. The same cubic interval quadrature is stored locally with
cumulative sums. Mesh-audit gates pass: dense/prefix error<4e-16; exact
10L core nodes; initial-state difference<6e-9 and force<5e-10. There are
5660 cells but no dense5660-squared matrices. All acceptance gates remain
unchanged; buffer/time/core-grid controls remain required. BUFFER01 is a
bounded diagnostic trajectory, not yet evidence of regularity or BTFR.

## Constrained principal audit of the unadopted compression term

The fixed-metric polynomial above is NOT the physical constrained answer.
Independent ADM derivation and a separate algebra check retain lapse and
shift before reduction. This is a strict local principal limit about an
aligned on-shell epoch, not finite-k cosmological evolution or a nonlinear
source solution. Let N=1+n, N_i=partial_i beta, gamma_ij=exp(2zeta)delta_ij,
U_i=partial_i alpha; E=alpha_dot+n, b=beta-alpha, and varphi the leading
gauge-invariant phase perturbation delta_phi+Q*alpha. Up to a boundary term,
the principal action bracket is

    Lpr=d*varphi_dot^2-(C+mu)*k^2*varphi^2
      +KB*k^2*E^2+2*C*k^2*E*varphi
      -6*zeta_dot^2-4*k^2*zeta_dot*b+2*k^2*zeta^2+4*k^2*E*zeta
      -c_theta*(3*zeta_dot+k^2*b)^2.

The constraints give KB*E+C*varphi+2*zeta=0 and
2*zeta_dot+c_theta*(3*zeta_dot+k^2*b)=0. Eliminating them yields

    Lred=d*varphi_dot^2+B*zeta_dot^2
       -k^2[(2*eta+mu)*varphi^2+4*eta*varphi*zeta+2*eta*zeta^2],
    B=6+4/c_theta, eta=C/KB, mu=m/X.

Therefore squared principal speeds x obey

    d*B*x^2-[B*(2*eta+mu)+2*eta*d]*x+2*eta*mu=0.

For0<KB<2 and c_theta,d,mu>0 the kinetic matrix is positive, and the
gradient determinant is2*eta*mu>0. This local scalar sector has two
positive-norm, positive-speed principal modes; it is not a full stability
certificate. The c_theta->0+ fast root recovers (2*eta+mu)/d. Removing the
scalar gives2*eta/B=c_theta*(2-KB)/[KB*(2+3*c_theta)], the pure-aether limit
check, not transferred observational phenomenology.

The Rayleigh trial(varphi,zeta)=(1,-1) gives the exact useful bound

    0<x_slow <= mu/(d+B) < mu/(d+6).

At the nominal supplied epoch this is about6.4e-8, below kappa=1e-7 for
every positive c_theta with those local coefficients held fixed. In the
small-mu limit x_slow~mu/[d+6+4/c_theta], not c_theta/2. The earlier
fixed-metric small-coefficient sound-crossing estimate is consequently
SUPERSEDED for the constrained theory. Increasing this coefficient cannot
make the slowest principal mode cross this particular core within t_dyn.
That fact does NOT prove continued focusing or exclude fast-mode support.
For homogeneous central contraction grad(Theta)=0 at leading order;
actual radial structure, mode residues and source history matter.

The next analytical requirement, if considering adoption, is the finite-k
source response and its coupling to ordinary matter, together with cosmic
recalibration and preferred-frame/radiation losses of the actual mixed
theory. No coefficient is chosen, no caustic cure claimed, no physical
model changed, and no extra record mass introduced by this contingency.

The exact auxiliary representation clarifies what an implementation would
actually require. Replace -c_theta*Theta^2 by2*chi*Theta+chi^2/c_theta;
variation gives chi=-c_theta*Theta. With V=AR^2, its polar bracket after
integration by parts is

    Lchi=-2*V*c*chi_t-2*N*R^2*sigma*chi_R+N*V*chi^2/c_theta.

The removed boundary density is partial_t(2Vc*chi)+partial_R(2NR^2sigma*chi).
The primary constraint is Pi_chi+2Vc=0. The extended Hamiltonian adds
N[2R^2sigma*chi_R-V*chi^2/c_theta]+lambda_chi*(Pi_chi+2Vc), where the
multiplier is chi_t. This is not an extra unconstrained fluid.
Define chi_n=chi_t/N and chi_s=chi_R/A. The additional polar sources are

    rho_chi=sigma*chi_s-chi^2/(2*c_theta), j_chi=c*chi_s,
    Pr_chi=-chi_n/c+sigma*chi_s+chi^2/(2*c_theta),
    Pt_chi=-c*chi_n-sigma*chi_s+chi^2/(2*c_theta).

Then pi_u_dot gains -2NR^2[chi_s+(sigma/c)*chi_n]; pi_a_dot gains2NV*Pr_chi
and pi_b_dot gains4NV*Pt_chi. The momentum generator before shift fixing
includes Pi_chi*chi_R, so its polar reduction is

    pi_b=R[u*pi_u_R-pi_phi*phi_R+sum(nu_b*p_b)-Pi_chi*chi_R].

It adds -NRc*chi_R/2 to A_dot/A. Radial metric constraints require the new
rho_chi and Pr_chi, including the constrained chi_t. Direct scalar canonical
terms are unchanged, but the geometry and vector equations are not.
Preserving the primary constraint gives chi=-c_theta*Theta; the secondary
consistency and full metric constraints determine multipliers. Eliminating
this pair changes the reduced symplectic/Dirac structure. The old brackets
must not simply be retained with an extra vector force.

Aligned FLRW gives rho_chi=-9*c_theta*H^2/2 and
P_chi=3*c_theta*H_dot+9*c_theta*H^2/2. Their continuity equation closes
and the Friedmann normalization above is recovered. Negative effective
RHS density here means a gravitational kinetic modification moved across
Einstein's equation, not an adopted negative-energy material component.
These independently checked equations remain an UNADOPTED contingency.

## Buffered trajectory outcome and next diagnostic

BUFFER01/01B/01C completed the same.25 t_dyn in bounded continuations.
Every implemented individual check passes, but BUFFERMATCH01 versus the
original960 mesh FAILS: charge-change .313334, Z-change .004145; gravity
4.51e-10 and Theta2.46e-8. The buffer did NOT deliver a numerical cure.
Its central acceleration divergence rises to15.645 but remains tiny next
to Ricci_UU211561; no physical claim can be based on this unqualified row.
The planned600/800L buffer-size comparison is now running as BUFFER02.
It will distinguish buffer dependence before another physical extension.

The full same-state prefix/dense RHS audit also passes: clock/vector
components coincide at printed precision, force differences are roundoff.
A separate discrete principal wave-operator audit on160/320 grids has
fastest real growth about.64/1.02 per t_dyn, concentrated toward the outer
boundary; this simplified operator does not explain rapid core growth by
itself or establish full-system stability. Polynomial controls pass. Keep
these diagnostics separate from either physical instability or convergence.

BUFFER02/02B/02C/02D is now DONE at the same .25 t_dyn. All individual
checks pass. BUFFERDOMAIN01, comparing the 600L and 800L buffers, FAILS:
charge-change .751771, Z-change .0073313; gravity 7.77e-12 and Theta
4.30e-8. This does not qualify the charge/current state or establish a
physical failure. No further buffer enlargement or blind refinement is
justified by these results. The buffered representation has not supplied
the controlled nonlinear formation answer. BUFFER02D result SHA256 is
44c6daefb57f8242597d1017d931b076869bda8eae5a443826d36bf32a4cb7d2;
checkpoint d0821ac50e1188b0c6d5a73a660fa8bcb795001c3cb4aff74eed266a16ebf189.

## What the principal modes and exact charge balance do establish

Independent review corrects a possible overinterpretation of the zero
principal speed. In the direct constrained c_theta=0 ADM system, use
zero shift and define chi=k*varphi, z=k*zeta, pi=d*varphi_dot, v=k*alpha,
and A0=2*eta+mu. The frozen principal equations are

    chi_dot=k*pi/d, pi_dot=-k*(A0*chi+2*eta*z), z_dot=0,
    v_dot=-eta*(chi+z).

The k-principal matrix has the fast pair and two independent zero
eigenvectors, not a k-Jordan block. Its conserved positive energy is

    E=pi^2/(2*d)+A0*(chi+2*eta*z/A0)^2/2+(eta*mu/A0)*z^2.

Adding a fixed-weight v^2 gives a finite-time estimate with constants
independent of k. This is only a frozen-principal statement: it does not
control grad(v) without extra regularity, degenerates as mu tends to zero,
and is not a full nonlinear hyperbolicity proof. The earlier square-form
fast-oscillator reduction must not be presented as the full constrained
zero-frequency sector. A zero speed alone does not diagnose the numerical
failure as a physical high-k instability.

For the exact polar system, define C_phi(R)=2*integral_0^R(cp*r^2 dr).
Then C_phi_t=-2*N*R^2*Jcur. On a vector-following sphere this becomes

    dC_phi/dtau_U=-2*R^2*[D-(m/X)*p].

Network-flow compression is therefore not scalar-charge conservation in
the moving volume: relative flux remains. With f=c/A and
rho_reg=Ecal/2+M*q, integration by parts gives the exact clock contribution
to the Hamiltonian mass,

    M_C(R)=f(R)*R^2*Z(R)/2+integral(r^2*rho_reg dr)/2
           -integral(f_R*r^2*Z dr)/2.

The boundary Z contribution and imported charge cannot be bounded merely
by the local ratio of background clock density to ordinary core density.
A conditional short-time reduction gives a small force only if compression,
relative flux and reduction errors are also controlled. In particular,
with J_R=(R/R0)^3 and
B_flux=3*integral(R^2*abs(mu*p) dt)/(mbar*R0^3), its central estimate scales
as mbar*Q*t_dyn^2*[(1+B_flux)/J_R+1]/6, plus reduction errors. The small
prefactor alone is NOT a full-equation no-go. The missing estimate is a
regularity/flux bootstrap, including the initial fast transient and outer
state. These identities guide a formation compatibility test rather than
another unqualified long trajectory.

## The cosmically charged MOND branch has a testable compatibility condition

The new analytical target is branch existence with supplied cosmological
data, distinguished from its selection by the previously tested preparation.
No new parameter, initial MOND profile or equation is adopted here.

Combining the exact vector equation with the current, and writing
mu=m/X, gives

    Jcur+mu*c*p = sigma*[mu*Q+c*divZ/(A*Q)] + c^2*Zdot/(N*Q).

Here c is the boost factor: mu*c*p is NOT mu times the canonical charge cp.
For a quasi-stationary positive MOND-type segment with p>0, divZ>0, mu>0
and nonnegative matched Jcur, this requires outward sigma. An inward
vector flow cannot sustain that segment with Zdot approximately zero.
This is conditional: the actual retarded current need not remain positive,
and a time-dependent branch has the displayed Zdot term. No physical
exclusion is inferred from the failed numerical charge comparison.

In the weak stationary limit e approximately equals g=(ln N)_R. Then
Z approximately equals KB*g+C*p. If g_K denotes the ENCLOSED excess
clock-energy contribution, not a local density ratio, the leading force
and current relations are

    C*(g-p) = 2*(g_b+g_K) + controlled stress/drift corrections,
    [C*j(p^2)+mu]*p+Jcur-mu*Q*sigma = 2*(g_b+g_K) + corrections,
    g_K(R) = integral_0^R [rho_K-rho_K,bg]*r^2 dr/(2*R^2),
    rho_K=X*m-K.

This recovers the familiar MOND relation only when the extra displayed
terms are small. It does not justify discarding them in a vacuum exterior.
The conditional high-acceleration normalization is
GN/Gcos=2*(1+lambda_s)/(C*lambda_s); it is not automatically the measured
normalization of every time-dependent charged branch.

For an IDEAL point-source MOND target p=a_M/R, Z approximately2p,
a_M=sqrt(2*kappa*L*a0/[C*lambda_s/(1+lambda_s)])=1.44983e-7.
This corresponds to114.15 km/s; it is not a simulated rotation curve.
The stationary-excess background example Jcur=m*H*R requires

    sigma_req=(m*R/2)*[1+H*Q*R^2/a_M]/[1+m*Q*R^2/(2*a_M)].

The cosmic-current numerator changes by order unity at31.019L (155.1kpc),
well before the denominator scale505.532L. A zero-current approximation
cannot be carried through the20--300L matching region. These scales use
frozen local coefficients and an ideal uncompensated monopole; the actual
prepared source is compensated, and this is not its solved outer profile.

There is a second shared constraint. For a stationary phase
phi=omega*t+psi(R), q=omega/N and X^2=q^2-w^2 give EXACTLY

    X_R=-(q^2*g+w*w_R)/X,
    (rho_K)_R=-d*(q^2*g+w*w_R).

Thus constant m is generally inconsistent with an attractive potential.
At matching radius Rm, linearization about specified Xbar,dbar gives

    delta_rho_K = delta_rho_m-Xbar^2*dbar*ln(N/Nm)
                  -dbar*(w^2-wm^2)/2.

For the ideal MOND segment this is delta_rho_m+Dstar*a_M*ln(Rm/R)
-dbar*a_M^2*(R^-2-Rm^-2)/2, with Dstar=Xbar^2*dbar=1.16821e7.
The inner density rises unless the gradient correction compensates it.
The annular clock mass from Rs to R is

    delta_MK=delta_rho_m*(R^3-Rs^3)/6
       +Dstar*a_M*[F(R)-F(Rs)]/2
       -dbar*a_M^2*[R-Rs-(R^3-Rs^3)/(3*Rm^2)]/4,
    F(R)=R^3*ln(Rm/R)/3+R^3/9.

Include the independently determined inner mass as well. If and only if
delta_rho_m=0, inner/gradient corrections are neglected and Rs<<Rm, the
estimate MK(Rm)=Dstar*a_M*Rm^3/18 equals the declared ordinary monopole at
89.014L (0.445Mpc). This is a conditional warning scale, NOT a predicted
turnover: the phase datum changes it, and frozen-d linearization may already
be inaccurate. The radial clock cap is a further independent requirement.

The executable scale/identity check is
invariant_clock_mond_compatibility_v001.py (SHA256
62e03d8d0d265100bf792e673b0c05212c114f44d28665aa403d77f7ee58b3db).
Its named JSON receipt passes all17 prespecified numerical controls,
including an independent quadrature of the annular formula. These check
algebra/calibration only, not branch formation or observations.

The minimal consequential branch test must retain N_R=g*N, the enclosed
clock-energy equation, the actual constitutive law, vector/current relation
above and the matched physical phase rate q_m and state X_m. The outer
current comes from

    N*R^2*Jcur-Nbg*R^2*Jbg = -partial_t(C_ex)/2.

Neither q_m, delta_rho_m nor the inner clock mass may become a fitted
galaxy chemical potential or halo. A coordinate change rescales N and
omega together, leaving q invariant. Imposing a stationary phase while
independently prescribing Jbg is not automatically a closed solution:
the evolving charge profile must satisfy this last equation too. The
actual missing datum is the retarded shared state/history, not an extra
chosen galaxy profile. A regular compatible branch would be progress;
its formation from the original preparation would still need to be shown.

Related quasistatic AeST work also finds boundary-dependent regimes, but
uses a different action; neither its branch solutions nor its successes
are inherited here: https://arxiv.org/abs/2304.05134.

## Exact expanding background audit before another galaxy run

The polar source code explicitly approximated the homogeneous cosmic
slice through R^2. Audit that approximation rather than assume the failed
charge comparison is physical. This is a source-free coordinate/control
calculation, not a changed action, another fit or a galaxy simulation.
Use the original no-radiation calibration to isolate the old approximation.

From flat FLRW in areal radius, B=1-H(t)^2 R^2 and
ds^2=-B dt^2-2HR dt dR+dR^2+R^2 dOmega^2. The zero-shift polar coordinate
T has t_R=-HR/B and t_T=Jtime. Integrability requires
Jtime_R=-Hdot R(1+H^2R^2)Jtime/B^2, with Jtime(T,0)=1. Thus

    x_R=-H^2 R/B, x=ln a, A=B^-1/2, N=sqrt(B)*Jtime,
    u=HR/B, phi_R=-QHR/B, p=e=Z=0,
    cp=m/B, nb=rho_b/B, pb=u.

These fields contain no supported population. Cosmic rho=3H^2 and
P=-2Hdot-3H^2 give normal rho=3H^2-2Hdot H^2R^2/B,
Pr=-2Hdot/B-3H^2 and mass=H^2R^3/2. The required lapse gradient is
g=-H^2R/B-Hdot R/B^2. All functions are evaluated at the varying cosmic
time on the same polar slice, not at its center time everywhere.

Prospective bounded audit: integrate the two radial ODEs using RK4 with
maximum radial steps extent/1024 and extent/2048. Require state agreement
1e-11 relative with nonzero physical scales, analytic metric/current/evolution
identities1e-10 and inverse residual2e-12. Compare exact and old source-free
initializations and their discrete initial RHS on320/640 original meshes
and the existing600L/800L buffered meshes. Report those measured defects;
do not invent an observational or trajectory pass from this initial test.
The old full-state1e-3 trajectory gate is not relaxed. Assess error in the
core and its quarter-orbit characteristic reach separately from the much
larger outer domain, including the global lapse normalization difference.
Do not extend a galaxy trajectory merely because this coordinate audit
passes. A causal explanation of old failures remains a separate question.

The source-free audit is DONE in2.912 seconds, all40 frozen controls pass.
The independent analytical reviewer confirms the embedding and code
transcription. Coverage is precise: constraints and vector/scalar/charge
evolution are gated; ordinary momentum and the independent metric-time/
angular equation are not separately gated by this receipt. Also require
1-(HR)^2*c_L^2>0 for the scalar inverse, independently of B>0; the present
small domain safely satisfies both conditions.

For both buffered meshes, the old charge initialization differs from exact
FLRW by2.30e-16 relative in the inner10L and3.15e-14 inside the frozen
quarter-orbit fast reach335.47L. The difference is only3.15e-6 of the
prespecified charge floor in that latter region. The outer-domain difference
is2.20e-8 relative and the time normalization differs by about6.3e-10.
The exact-background discrete charge RHS error is below8.6e-13 relative
inside that reach; the spurious core p RHS is about2.3e-13 in code units.
The outermost ordinary transport cell has a much larger residual (up to
.207 relative), while the same residual within reach is below1.3e-12.
Boundary treatment therefore remains unqualified, but this is not evidence
that it contaminated the core or explains the buffered trajectory failures.
The reach estimate is linear and frozen, not a full nonlinear causality proof.

There is no demonstrated basis for another long run merely replacing the
R^2 initialization. Preserve this negative diagnosis. Source script
invariant_clock_flrw_polar_audit_v001.py SHA256:
b904f5ce1b7ed382f1ce4e2a100347f0e744a347e15644502a1f7c890c97a479.
Receipt INVARIANT_CLOCK_FLRW_POLAR_AUDIT_V001_RESULT.json SHA256:
b17f509c29b06bc35fccdfedd8e494e3fe41bea0bee5eda3b0bf717674fc92ec.
The first invocation stopped before numerical work because a local variable
shadowed the time module; the naming repair is recorded in the receipt.

The latest CMB-calibrated Hunit also cannot erase the galaxy obligations.
At fixed physical ordinary mass, size and a0, let
lambda=68.065020107/73.6. Physical X,m scale as lambda; d,mu and the MOND
target amplitude a_M remain fixed; Dstar=X^2*d scales as lambda squared.
Hence the illustrative current scale grows approximately8.1% (about168kpc,
including the small actual-H radiation correction), and the conditional
mass-warning scale grows5.35% (about.469Mpc). Neither is a prediction of a
formed galaxy. The fractional clock cap and ideal flat-segment logarithmic
span remain unchanged. Prior stellar/galaxy evidence is not superseded by
the successful acoustic calibration.

Next discriminate the physical transient from numerical charge error using
the independently solved LINEAR source kernel for the same compensated
source shape, rather than another nonlinear quarter-orbit run. First fix
the mapping of its initial phase/charge and observables to the polar
preparation. A zero-material initial Fourier mode must not be assumed
equivalent to a curved polar initial slice without that check. Any early
comparison must report Hubble, stress and nonlinear-advection truncation
errors separately from numerical quadrature error.

The finite-source Hankel reconstruction is DONE, with all14 numerical
controls passing. It uses the same analytic compact/compensated shape and
ordinary monopole, normalized by its continuum integral, not literally
the old mesh quadrature normalization. Source reconstruction and cutoff/
quadrature differences are below5e-12 in the chosen norms. The first
saved time is.01562377939 t_dyn, Ht=6.0646e-5. The predicted physical
material-charge contrast peaks at4.64742e-9. Reconstructing the exact
canonical inverse from the three saved snapshots gives peaks4.64221e-9,
4.64417e-9 and4.63606e-9. Corresponding whole-profile differences are
.0011215,.0006991,.0024434. Z differs by about.0001241 and p by
.00026--.00028. This is an early spatial response check, not full nonlinear
trajectory qualification or a new observational success.

The initial mapping is essential: delta_m=p=Z=0 does NOT mean zero
phase-rate perturbation. delta(phi_dot)=Q*Phi is required by
deltaX=delta(phi_dot)-Q*Phi. Also cp=A*m at zero boost, so coordinate-volume
charge initially includes the metric even when physical m is unperturbed.
The frozen kernel keeps the fast oscillator in delta_m; its tiny residue
in the effective metric source S cannot justify dropping it from charge.

Independent review checks the Hankel prefactors, source transform and
initial leading frozen mapping. It identifies a diagnostic correction:
the exact canonical boost/current contact is m*(q/X-1)+sigma*D, not
m*(c-1)+sigma*D as the V001 auxiliary contact field reports. The inverse
and physical m comparisons use q/X correctly and are unaffected. Preserve
that receipt with this qualification; correct the auxiliary quantity in
a bounded postprocessing check, without redoing the Hankel integration.

The actual constitutive tangent changes by only1.88e-7; its local
linearization remainder is below9.4e-8 of the measured material contrast.
But the background-subtracted kinetic clock contact is about46.7 times
that contrast and cancels against other phase/lapse terms. It is NOT an
uncancelled error. Likewise the loose absolute tilt sensitivity.00114
is not a physical discrepancy: pure FLRW has exact tilt cancellation.
No explicit full H/gauge correction is included in the frozen kernel.
Before using it to adjudicate the old.001 trajectory gate, account for
those cancellations, phase drift |nu_dot|t^2, center-clock interpolation
and nonlinear advection (the measured |Theta_center*t| is.000596).
The agreement supports the early-response interpretation, but does not
explain or excuse the later600L/800L charge disagreement.

Source invariant_clock_finite_source_linear_v001.py SHA256:
e46843ddcc05de64a82855b36ad2fadead66aa57483c3b83a82ae62a3836c612.

Receipt INVARIANT_CLOCK_FINITE_SOURCE_LINEAR_V001_RESULT.json SHA256:
55e3fb4d95215b083bdb1ebb5be632eb8db23b8bc76661769bc99fb14188c8ce.

## Central source discrepancy remains unresolved

The saved-state locality test is complete in
INVARIANT_CLOCK_POLAR_LOCALITY_V001_RESULT.json. Copying an identical inner
state between the600L and800L domains gives identical A and X and clock/
vector core proper-time rates agreeing near machine precision. The strict
all-component relative1e-10 gate FAILS in ordinary orbital momentum:
absolute cancellation residuals near7e-18 divide by a1e-12 floor. That
failed gate remains failed; it is not evidence of a material outer-domain
coupling. The exact boost contact correction above and a refined center
clock change the early comparison negligibly. The continuum source peak
differs from the old mesh normalization by6.6398e-5, explicitly retained.

The late disagreement is also present in reconstructed invariant material
m, not merely coordinate charge cp. Its maximum grows from8.11e-12 at
.015624 t_dyn to1.79664e-5 at.25 t_dyn, concentrated at the first radial
cell R=.00514628L. Similarity of gravitational forces does not qualify it:
that cell has little enclosed volume. The approximate late growth rate
near80/t_dyn is an empirical envelope, not an identified eigenmode.

Two bounded spectral checks do NOT support the proposed central CFL
explanation. The parity-correct spherical principal operator on64/96/128
central cells has stable RK4 amplification at the actual time steps
(all9 numerical controls pass). A four-field Jacobian including the full
implemented geometric solve on32/64/96 central cells passes18 matrix/
eigen-residual controls. At the late saved state, localized continuous
eigenvalues near5.97 +/-181533i per t_dyn are strongly damped by actual
RK4, not amplified. Maximum RK4 growth over all tested modes is only
about.5--.6/t_dyn. Matrix refinement is not proof of eigenvalue accuracy;
ordinary perturbations were frozen, and non-normal/time-dependent effects
are not excluded. Neither test bounds the full evolving discretization.

Decision: the early independent response is useful, but the quarter-orbit
galaxy solution remains UNQUALIFIED. Do not launch another blind buffer,
time-step or initialization rerun. Continue the independent mandatory
recombination-perturbation lane while retaining this specific source gap.

Audit provenance, source SHA256 then receipt SHA256:

- invariant_clock_polar_locality_v001.py:
  33a08141262a6dfe0e55d44eea24d602e42be4f2741192bde712ba78e7a678b2;
  2694a8255a694ec54df34529c585026221d613e4a9fcb145d7f6c19555947e53.
- invariant_clock_polar_cfl_audit_v001.py:
  c5c2b119d048ee056a13a10e1bb18d203c9d20b28fec01c7d3a5dee95b310301;
  203e6613b200fc0341df71dbee51b928fa7bf7e63d465dc20a7a64bda4bd4cc4.
- invariant_clock_polar_central_jacobian_v001.py:
  ac87e95aa3f79eddbd176759e9dcddb68885c723cad9c6d1011cff9fc0af25b0;
  dd47cc11de9d8cf34622eb7361fa2bee3b1a8d19c0bc0e82d6f703023a58c56d.

## Stellar phase winding and a nonspherical escape

The stationary spherical cap obstruction has a precise time-dependent
extension. For a fixed spherical metric, regular central phase, proper
outer time T and actual outer phase rate q_m(T), let
Delta=ln(N_m/N_c). Then
d(phi_m-phi_c)/dT > q_m(T)-exp(-Delta)*X_cap.
If that right side remains above delta_q>0, the radial phase difference
grows at least delta_q*T. Over finite proper matching length ell,
sup|w(T)-w(0)| > delta_q*T/ell. Thus no globally bounded or periodic
radial gradient satisfies these assumptions forever. This is NOT an
energy, inflow or metric-drift theorem, and the gradient need not reside
inside the star. Evolving geometry requires integrating the actual
time-dependent lapse ratio instead of using a fixed Delta.

The measured638+-6 m/s redshift proxy is development-exposed and includes
3D convective modeling: https://arxiv.org/abs/2009.10558. Under the adopted
minimal photon coupling and attractive-center assumptions it supplies
Delta>=2.12814e-6, versus present spherical headroom4.23986e-7. Current
unboosted outer phase gives delta_q/Q0=1.70415e-6. Even using any unboosted
outer X>=Q0 gives a positive lower deficit1.62814e-6. Illustrative lengths
and ages in the receipt are not physical matching radii or stellar histories.
The25 analytic identity/unit checks pass; they are not observational gates.

A stationary NONspherical phase instead needs
|grad phi|_center^2 > q_m^2 exp(2Delta)-X_cap^2. Its minimum phase-normal
speed scale is.00184616*c for the stated current outer rate. This is a
phase kinematic scale, not an ordinary-matter velocity or observed wind.
The preferred direction and its stress must be solved, not declared harmless.

Source invariant_clock_stellar_winding_v001.py SHA256:
73b9b98662063a3a1558e2d77501fc057961abd448490ecf2401d1b439e8a97d.
Receipt INVARIANT_CLOCK_STELLAR_WINDING_V001_RESULT.json SHA256:
4325cea7d13074fee0b2b353756f12b8af85e9554875f6b6a6b6aea5a2a53a7b.

## Local through flow exists on a prescribed background

Independent analytical review confirms a constructive restricted escape.
In a prescribed static planar lapse N(z), A=1, take phi=omega*t+psi(z),
negative nonzero vector tilt sigma, c=sqrt(1+sigma^2), q=omega/N and
w=(p-sigma*q)/c. Then X^2=q^2-w^2, e=(Z-Cp)/KB,
D=C[e-(1+j)p], NJ=N[cD-(m/X)w] is constant. Stationarity gives
(Nc)'=N e and Z'=QD/sigma. Evolving B=Nc removes explicit N'/N from
these equations and gives uniform finite-length bounds even at the
center of the imposed well. For B approximately constant and Z small,
p is negative, e positive and delta X approximately sigma*p/c positive.
The current inverse includes compressibility; it is not simply2*C/KB.

The fixed diagnostic uses a Gaussian log-lapse well of depth2.12814e-6
and illustrative695700km width, NOT a solar metric or positive planar
ordinary-density solution. Two prescribed incident tilts -.001 and-.0001
are additional preparation choices, not observed or natively selected
velocities. No action parameter or data fit is added. RK4 512/1024 steps,
exact algebraic current and independent derivative checks pass all24
predeclared numerical gates in.447 seconds.

For tilt-.001, central sigma=-.0022926593, p=-4.91615e-8 Hunit,
e=4.86699e-6 Hunit and X-Xbar=1.12710e-10 Hunit. For tilt-.0001,
X-Xbar=1.54396e-10 Hunit. Both are far below the cap, with current inverse
above197.99 and branch fraction between.1520273 and.1520304. The exact
tiny B and Z evolution is retained rather than set to zero. Along the
negative flow, downstream Z is5.34456e-18 and1.59660e-17 Hunit; it cannot
be reset to the incoming value. A matched downstream state remains required.

There is also real energy flux: j_energy=qJ, verified independently and
numerically. The imposed-curvature stress/flux screens are~1e-29/~1e-32
at the illustrative stellar scale. Their smallness supports a local weak
backreaction approximation; it is NOT the Einstein constraint solution,
a global finite-time error bound, or cancellation of the nonzero flux.
The bare coupling could approach Gcos on this branch; the earlier static
GN calibration must not be silently imported. Three-dimensional focusing,
downstream matching, preferred-frame effects and formation remain unresolved.
This result defeats only an overbroad spherical-cap no-go claim. It does
not establish a full star, galaxy, BTFR or native state.

Source invariant_clock_planar_throughflow_v001.py SHA256:
4eb1ddb2aefb53e6665eab9299e6f9e0c6570ce4fa20458842924d1804fc2a47.
Receipt INVARIANT_CLOCK_PLANAR_THROUGHFLOW_V001_RESULT.json SHA256:
8b223198995404e4b404c6719c656a76b3c05a453f50be07b76afb7109dfc895.

## Three-dimensional stationary equations and focusing caveat

Independent analytical review extends the prescribed-static-metric system.
Let v be spatial U, c=sqrt(1+v²), w=grad(psi), q=omega/N,
Q=cq+v·w, X²=q²-w², Y=Q²-X²; all spatial operators use that metric.
Define e=grad(Nc)/N, B=curl(v), r=qv+cw,
Z=KB*e+C*r, Hmag=KB*B-C*(v cross w). In general r is NOT w+Qv.
The stationary action density (apart from the volume factor) is
N{KB(e²-B²)+2C[e·r+B·(v cross w)]-C[Y+J(Y)]+2K(X)}.
The phase current and vector equation are

    Jcur=C[c e-v cross B-(1+j)(w+Qv)]-(m/X)w
    div(N Jcur)=0
    -curl(N Hmag)/N
      +C[q e+w cross B-(1+j)Qw]
      +(v/c)[-div Z+C e·w+C(1+j)Qq]=0.

The parallel planar reduction recovers sigma*Z'=Q*D. These are proposed
analytical equations checked by independent reduction, not a solved 3D
Einstein/matter system.

Weak ballistic deflection gives Delta v_perp=-2GM/(b*v_inf) and first
axis focus z_f=b²*v_inf²/(2GM). Weak deflection therefore allows MANY
crossing times before focus, not a universal one-crossing obstruction.
Native interactions could regulate this only if the transverse Jacobi
correction integral is order unity:
norm[integral_0^tf (tf-s)*grad_perp(a_U,perp) ds] >= order1.
A small acceleration amplitude or large characteristic speed alone does
not decide this; steep layers may matter.

Generic small-length Maxwell power counting is NOT a uniform no-go.
The linear stationary channel delta v=grad chi, v0·grad chi=0,
delta w=-Xbar*delta v has delta B=delta c=delta e=delta r=delta X=0
to first order. Charge conservation still requires mbar*laplacian chi=0
or an appropriate relative current. Vector focusing need not imply
charge compression: relative phase current can transport the charge.
No incoming vortex or charge profile may be selected to engineer the cure.

The metric normalization also requires an integrated budget, schematically
surface integral Z + volume integral delta rhoK + retained stress/drift
=(GN/Gcos-1)*enclosed ordinary source. Tiny local stress in the planar
experiment does not supply this2% enhancement or establish the inherited
static GN dictionary. A cylindrical/axisymmetric matching problem is being
derived before another numerical source run; no numerical worker is live.

## Restricted cylindrical caustic layer, derived but not solved

The smallest curl-retaining local layer uses prescribed weak N(R), flat
spatial metric at this approximation order, phi=omega*t+k*z+psi(R),
v=u(R)e_R+V(R)e_z and c=sqrt(1+u²+V²). Let w=psi', q=omega/N,
Q=cq+uw+Vk, X²=q²-k²-w², Y=Q²-X², mu=m/X and g=N'/N.
Omega and k are inherited phase data, not adjustable local potentials.
With e=c'+cg, define Z=KB*e+C(qu+cw) and
Hmag=-KB*V'-C(Vw-uk). The reduced radial action INCLUDING measure is

    N R {KB(e²-V'²)+2C[e(qu+cw)-V'(Vw-uk)]
         -C[Y+J(Y)]+2K(X)}.

Regular phase conservation gives J_R=0 (no line source), where

    J_R=C[uu'+c²g-(1+j)(w+Qu)]-mu*w,
    J_z=C[uV'-(1+j)(k+QV)]-mu*k.

Thus axial relative current is retained. With
T=-(RZ)'/R+Cew-C(1+j)Qq, vector equations are

    0=C[qe+kV'-(1+j)Qw]+(u/c)T,
    0=-(NR Hmag)'/(NR)+C[-wV'-(1+j)Qk]+(V/c)T.

The axis requires u=u1*R+..., V=V0+V2*R²+..., w=w1*R+...,
g=g1*R+.... There X_a=sqrt(q_a²-k²), Q_a=c0*q_a+V0*k,
c0=sqrt(1+V0²), and

    w1=C[u1²+c0²g1-(1+j_a)Q_a*u1]/[C(1+j_a)+mu_a],
    e1=(u1²+2V0*V2)/c0+c0*g1,
    Z1=KB*e1+C(q_a*u1+c0*w1),
    H1=-2KB*V2-C(V0*w1-u1*k),
    T_a=-2Z1-C(1+j_a)Q_a*q_a,
    0=C[q_a*e1+2k*V2-(1+j_a)Q_a*w1]+(u1/c0)T_a,
    0=-2H1-C(1+j_a)Q_a*k+(V0/c0)T_a.

Do not divide by u at the axis or choose u1 freely without these relations.
The outer boundary must match inherited u,V,w,Z,Hmag, not just velocities;
unmatched slopes introduce new incoming field data.

Two necessary screens can avoid an unjustified BVP:

    X_a²=X_L²+w_L²+q_a²-q_L² < Xcap²,
    u_L²/2 + integral c²g dR
      =integral[(1+j)Qu+(1+j+mu/C)w]dR.

For inward u<=0, Q>0, attractive g>=0 and bounded constitutive response,
R_L >= u_L²/[2(1+j_star+mu_star/C)*w_star].
A very thin layer may need near-pole susceptibility or axial-current
divergence. Failure of this axially invariant local cylinder does NOT
exclude a genuinely2D/3D solution. Curl B_phi=-V' is retained; this is not
a false identification of vector focusing with charge compression.

The same reduced action gives normal energy density

    M=mu*q+C[u e-(1+j)(Qc-q)],
    rho={KB(e²+V'²)+C[Y+J]-2K}/2
         +q*M+C*V'(Vw-uk)+c*(RZ)'/R.

Its divergence integrates as boundary R*c*Z minus integral R*Z*c';
do not discard either. A local cylinder supplies energy per axial length,
not a stellar GN or a galaxy solution. Full metric matching needs the
integrated lapse source rho+sum(P_i), flux and possible stationary shift.
This analytical reduction was independently checked; no BVP, numerical
qualification, global caustic cure or new observational claim is implied.

## The demonstrated regular through-flow does not supply a galaxy boost

The independent active-source derivation adds transverse pressure

    PT={KB e²+2C e p-C(p²+J)+2K}/2.

Stationarity makes PR=-Ecal/2-w*Jcur and
rho=Ecal/2+M*q+c*Z'. Thus active=rho+PR+2PT=c*Z'+A,
A=M*q-w*Jcur+2PT. For incoming constant active source Abar, the exact
restricted-field integral is

    Iact(z)=[NcZ]_incoming^z
       +integral_incoming^z N(A-Abar-eZ) dz.

It was computed both directly from the full stress and by these boundary/
volume terms; neither the downstream memory nor the derivative source was
discarded. The leading weak-metric lapse diagnostic is
max|Iact|/(2max|N'_imposed|). A pointwise ratio at the zero-gradient center
would be meaningless. This is not a completed metric solution: spatial
stress, momentum constraints and the possible shift from energy flux
remain required.

At the NEW two-parameter joint calibration, depth=(200km/s/c)²,
prescribed incident tilt-.001 and Gaussian widths5/20kpc, all22 numerical
controls pass in.519s. The two widths test a length scaling and lower
acceleration, not a search for a preferred boundary profile.

| Width | Peak imposed acceleration/a0 | Active-force diagnostic | Downstream Z/Hunit |
| --- | --- | --- | --- |
|5kpc|1.853215|6.90761e-7|4.68662e-7|
|20kpc|.463304|1.10517e-5|1.88155e-6|

The absolute diagnostic is far below an order-one gravitational boost,
even in the lower-acceleration example. The background-subtracted active
density is negative at the well center (~-.20529 Hunit²); its sign alone
does not determine a global force without metric/boundary matching.
Current inverse stays above197.998 and branch fractions stay within
.152027.. .152100, far from the cap. Increasing width by4 changes the
force diagnostic by about16, as the short-length estimate predicts.

This supports a precise limitation: the REGULAR branch continuously
selected by those upstream data escapes the stellar spherical cap but
does not also furnish the galaxy boost. Its convective acceleration
largely cancels g in e=cg+sigma*sigma'/c. It is not the aligned response
with e approximately g that was used in the old conditional MOND formula.
This does not exclude other dynamical/3D branches, near-stagnation/cap
states or different native laws. Those alternatives must be selected by
source evolution, not by inserting fitted incoming Z, phase or charge.
Do not relabel this prescribed-plane diagnostic as a galaxy fit or a
derivation of locally measured GN.

Source invariant_clock_galaxy_throughflow_v001.py SHA256:
ab0ff8cf46daaa8b1df42f8c4d9fa8425f43880d11c229be2b6525db1687698d.
RESULT SHA256:
96f02b9e83cc8aba6c278796a63d3cab5c39ce493ebe768e6c54b5f31f5c2ed0.

## Selecting the modified branch: exact flow and genuine curl

The independently checked exact polar identity already given above implies,
for a weak quasi-stationary MOND segment with Z approximately2p, p~1/R,
and matched |Jcur| much smaller than mu*p,

    sigma_required=(Jcur+mu*c*p)/(mu*Q+c*divZ/(A*Q))
                  approximately m*R/2 >0.

This last estimate requires the divergence term to dominate its denominator.
Inward flow can build Z through time-dependent compression, but does not
thereby become this stationary segment. The associated leading readout is

    Zdot/Z approximately Q*Jcur/(2*p)+m/2
                       -sigma*[1/R+mu*Q^2/(2*p)].

It is a spherical zero-curl control, not a general3D prohibition. Source
evolution must select the current/flow and amplitude; neither an incoming
phase profile nor accumulated gravitating clock energy is a free substitute.

The exact3D canonical equations do not preserve zero coordinate curl
automatically, but coordinate curl B=curl(v) is NOT physical vector twist.
The Frobenius combination is c*B+v cross e (with v dot B also zero for an
orthogonal congruence). An apparent fourth-order coordinate-curl term
cancels in this combination. Independent analytical review instead finds
the following necessary condition on a zero-twist branch in its orthogonal
coordinates ds²=-L²dτ²+gamma_ij dx^i dx^j:

    S_i=KB*a_i+C*p_i, a_i=D_i ln L, p_i=D_i phi,
    partial_tau S_i=L[(2K_i^j-Theta delta_i^j)S_j
                      +C Q(a_i-(1+j)p_i)],
    exterior_curl(right_hand_side)=0.

S is a spatial gradient on that branch. With homogeneous initial fields
and weak static source potential Phi, its first generic curl-compatibility
obstruction has leading form

    C*Qbar*(1+eta)*mbar*tau^5/(12*d)
       *curl[(Hess Phi) grad(Delta Phi)], eta=C/KB.

This is an obstruction in the vector-equation RHS, NOT a vorticity amplitude
or a galaxy force prediction. For Phi=A cos(k.x)+B cos(l.x), the spatial
factor is AB(k.l)(|l|²-|k|²)(k cross l)cos(k.x)cos(l.x). It vanishes in
plane/spherical symmetry, constant-density quadratics, harmonic vacuum,
equal-length pairs and orthogonal pairs. Nonparallel unequal k,l with
nonzero dot product give a constructive density-gradient/tidal-misalignment
source. A small smooth-cutoff perturbation within a positive-density core
can realize this locally without negative total ordinary density.

The Taylor expansion requires eta*Q*tau<<1, omega_fast(kmax)*tau<<1,
tau*sqrt(norm(Hess Phi))<<1 and small constitutive displacement. Generated
wave numbers and cutoff scales count. It cannot be extrapolated to an
orbital time. Thus 3D redistribution is not barred by an exact zero-twist
invariant, but its gravitational size remains unknown. A2D consistency
experiment is deferred in favor of the direct response question below.

## Proposed compression completion: full finite-k source response protocol

The previously unadopted -cTheta*(div U)^2 completion now targets the
demonstrated convective cancellation. It is one new universal coefficient,
not a native graph derivation or a record halo. No physical adoption or
parameter fit occurs in the following diagnostic. The principal action's
ordinary-source vertex was independently derived: for conserved isotropic
stress, the reduced driving vector is

    (eta*rho, 2*rho/KB-2*P/cTheta).

Its formal static response has E=n, while the cTheta->0 and zero-frequency
limits do not commute. This alone does not prove source-selected support:
the omitted Q-dependent terms can compete in the slow galactic response.
They are retained in the full linear FLRW extension independently checked
against the exact auxiliary stresses. Let F=1+3cTheta/2, and reserve chi
here for the COMPRESSION auxiliary perturbation, not the relative phase:

    3F H²=sum rho_i+Q*m-K, F Hdot=-(sum W_i+Q*m)/2,
    chibar=-3cTheta*H,
    delta_rho_chi=3H*chi,
    delta_P_chi=-chidot-3H*chi-3cTheta*Hdot*Phi,
    q_chi=-chi, Pi_chi=0,
    chi=cTheta/F*[3*qbase/2+kappa²*alpha],
    Zdot=-H*Z+Q*D-chi+3cTheta*Hdot*alpha.

Other material and ordinary conservation equations in the radiation note
remain, with Psi_dot+H*Phi=(qbase-chi)/2. The00 constraint cancels chi:

    2kappa²Psi=kappa²Z-Q*delta_m-sum delta_rho_i-3H*qbase.

Full energy/momentum identities and the high-frequency constrained limit
agree; the projected force, not q_chi, contains alpha*chibar_dot.

Prospective script: invariant_clock_compression_response_v001.py. ONE
serial small worker after source review; no duplicate original science.
Use cTheta=.01 and zero ablation, fixed5/20kpc modes and prior200km/s depth
to set formation time. Apply an infinitesimal conserved isotropic Fourier
test stress with zero initial fields. For R=a³(rho_s+3H*q_s)=Rfinal*f,

    q_s=-Rfinal*H*f_x/[a³(kappa²-3Hdot)],
    rho_s=R/a³-3H*q_s, P_s=q_s_dot+3H*q_s.

Quintic f rises over one declared formation interval, then stays constant;
the forcing density and wavelength subsequently expand. A signed test
stress is NOT a positive matter assembly model or a held galaxy. Evolve
six retained fields through four intervals with all Q/charge/metric terms.
Radiation is consistently omitted from this local late-time diagnostic,
not silently removed from the separate calibrated thermal calculations.
Do not inherit the old cosmic fit: H changes by1/sqrt(F) at fixed budgets,
and the conditional effective Gcos/GN dictionary becomes.98/F.

Frozen numerical gates in the source:128/256/512 subdivisions per interval,
CF4 exponential evolution, full-history state/observable refinement1e-4,
matrix-exponential controls1e-10, Einstein/source identities1e-9. Actual
source depth is1e-12 times the nominal finite potential; explicitly report
where extrapolating to the latter violates clock/interaction linearity.
No scientific acceptance threshold or galaxy-fit success is assumed.

### Result: elasticity removes the infinitesimal cancellation

The bounded calculation is complete. V001 took4.381s:18/19 controls passed,
with only the5kpc zero-elasticity delta_m refinement failing4.16461e-4
against the frozen1e-4 gate. V002 refined that one row to1024 steps but
still failed3.61367e-4. Neither failure was hidden or its gate loosened.
V003 instead evolves the EXACT relative phase r=varphi+Q*alpha directly:

    rdot=delta_m/d+Q*E-3H*m*alpha/d.

This avoids subtracting nearly equal phase/flow histories. The transformed
time-dependent RHS identity agrees3.58e-16. Original-variable full-state
refinement is1.26256e-5 and all20 controls pass. Only the failed row was
recomputed; three qualified rows were reused. The source/dependency hashes
and all failed receipts remain. Independent saved-result review agrees.
Saved states use the listed scales; time labels are log(a) ramp intervals,
not exact elapsed proper time divided by the nominal formation time.

At four ramp intervals, the response is:

| Scale | cTheta | Phi/probe depth | E/Phi |
| --- | --- | --- | --- |
|5kpc|0|-.993289|2.84187e-5|
|5kpc|.01|-15940.2375|.99999133|
|20kpc|0|-.973511|.000185166|
|20kpc|.01|-21922.0082|.99996376|

Thus this one proposed operator CAN prevent cancellation in the retained
infinitesimal retarded equations; it is not just a different formal static
limit. The large numbers are a highly susceptible linear response, NOT
predicted galaxy boosts. At this endpoint, the5kpc metric decomposition
in probe-depth units is Z/2=-15939.48605, clock-density=-Q*delta_m/(2k²)
=+.245307, ordinary response=-.003426, source=-.993331 and the remaining
momentum term~2.3e-10. At20kpc the corresponding values are-21921.06466,
+.089691,-.059603,-.973589 and~5.4e-9. The large infinitesimal effect is
therefore predominantly the derivative/geometric source, not accumulated
positive clock mass. This restricted statement does not establish nonlinear
formation, stable support, BTFR, a rotation curve or local Newton calibration.

An important ordering prevents a false negative conclusion. The relevant
weak-response nonlinear threshold is C*j/mu~1, NOT |p|/bs~1. For the
nominal physical-depth extrapolation, the5kpc snapshot at.03125 ramp
intervals already has C*j/mu=2.24 while |deltaX|/cap=.0397. At20kpc the
.03125/.0625 snapshots give C*j/mu=.572/18.0 and cap fractions.00990/.1545.
The nonlinear MOND term becomes important BEFORE the subsequently huge
linear cap extrapolation. Therefore the latter cannot exclude this
completion. It demands nonlinear saturation with the same J and K, not
a changed threshold or a larger clock cap chosen to hide the effect.

At the actual1e-12-amplitude probe, maximum cap fractions are3.44e-8 and
3.66e-9; |p|/bs maxima3.46e-10 and1.16e-10. Even then C*j/mu is roughly
.00089/.00030: the solved equations are the formal zero-amplitude derivative,
not a nonlinear result at1e-4 accuracy. Full nonlinear corrections were not
computed or acceptance-gated. At galaxy-depth extrapolation ordinary
contrasts also leave their linear regime. The signed test stress is not
a physical matter formation history. These qualifications remain material.

With cTheta=.01 the conditional Gcos/GN is.96551724 and H/H_old=.99258333
at fixed budgets. The successful OLD joint thermal calibration is not
automatically a calibration of this proposed completion. Coefficient.01
was a prospective diagnostic, not optimized or natively selected.

V001 source SHA256:b5595f45db8f57031b521ab4dab2afe443dae0469c0dce563478e4826b46498c.
V003 repair source SHA256:c6df0531ea63a26a67730d43d4a1b740ed709d7ba6b09b68c9b501392c0fd6bc.
Accepted V003 RESULT SHA256:
57039f275d2a7d21d98d90da4e9910bc66bbd546929a4140e6cec242eae71c35.
Failed V001/V002 RESULT SHA256:
6c87ff722533db05d66a75cc3eb06c6cc07cb41c2a5ff0c5a3691b64ede1509a,
f08a3f422a0a7376c92f055a799d17390f613fcab29a512b41f6b0bdaf4e602d.

Next actual scientific requirement: source-selected NONLINEAR saturation
with J, exact K(X), charge flux and ordinary support/work all retained.
The new exact polar balance gains compression terms:

    Jcur+mu*c*p = sigma[mu*Q+c*divZ/(A*Q)]
      +c²*Zdot/(N*Q)+c²*chi_R/(A*Q)+c*sigma*chi_t/(N*Q).

Scalar-current conservation is unchanged. This is the new possible support
mechanism; simply prescribing a desired phase/flow/current is not a test.
No numerical worker remains live. Independent analytic reviewers are
deriving the smallest justified nonlinear source/matching calculation.

### Exact nonlinear compression closure for the next source calculation

Both analytical reviewers independently confirmed a useful simplification:
the apparent radial derivative of chi_t cancels. The completion does not
require a dense numerical time-constraint Jacobian. The following equations
are for the full polar-areal zero-shift state, not the linear test stress.
Let f=phi_R, cp=pi_phi/(2R²), sigma=u/A, c=sqrt(1+sigma²). The old-sector
normal density, radial pressure and outward flux include ordinary matter:

    j0=[u*divZ-cp*f+sum(n_i*p_i)]/A²,
    rho_chi=sigma*chi_R/A-chi²/(2cTheta),
    j_chi=c*chi_R/A,
    active_chi=chi²/cTheta-(2c+1/c)*chi_t/N.

The spatial terms cancel in active_chi; its time term cannot be discarded
in a cosmically matched source. Compression does NOT remove the stationary
spherical cap: w(0)=0 still implies X_center=omega/N_center. The inherited
depth bound~4.24e-7 therefore still rules out the previously specified
200km/s-depth stationary sphere under those boundary assumptions. It does
not exclude time-dependent/nonspherical solutions; they must retain phase
winding and current rather than reset them.

Define

    T0=-R*A*j0/(2c)+sigma*e/c+sigma_R/(A*c²)+2sigma/(A*R).

Kinematics and momentum give exactly

    Theta=T0-R*chi_R/2,
    chi-cTheta*R*chi_R/2=-cTheta*T0.

Together with the Hamiltonian equation, the two radial constraints are

    A_R-(A²R sigma/2)*chi_R
      =A(1-A²)/(2R)+A³R[rho0-chi²/(2cTheta)]/2,
    sigma*A_R/(A²c²)+R*chi_R/2=chi/cTheta+Tstar,
    Tstar=-R*A*j0/(2c)+sigma*e/c+u_R/(A²c²)+2sigma/(AR).

Their determinant is R*(1+sigma²/c²)/2>0 away from the center. Regularity
requires A=1+rho_total(0)R²/6+... and chi(0)=-3cTheta*sigma_R(0), but
does NOT replace the outer chi datum: the homogeneous R^(2/cTheta) mode
is regular and numerically explosive outward (R^200 here). For fixed T0,
the stable inward representation is

    chi(R)=exp[-a*ln(Rm/R)]*chi_m
           -2 integral_0^ln(Rm/R) exp(-a*t)*T0(R*exp(t)) dt,
    a=2/cTheta.

Outer chi_m comes from the matched exterior, not a fit. Center-regular A
and exterior-matched chi define the radial state solve. Ordinary rest,
kinetic and angular-momentum support remain dynamical and conserved.

Let tau=chi_t, Ltau=A²R/(2c), and use the RAW radial pressure coefficient

    L0=(A²-1)/(2R)+A²R[Pr0+sigma*chi_R/A+chi²/(2cTheta)]/2,
    N_R=L0*N-Ltau*tau.

Then A_t/A=N*kA with kA=-R(A*j0+c*chi_R)/2. The remaining exact field
equations are linear in N,tau at a fixed state:

    u_t=N(Ae-c_R-cL0)+(RA²/2)*tau,
    Z_t=N[QD/c-sigma*divZ/(Ac)-chi_R/A]-(sigma/c)*tau,
    f_t=N(q_R+qL0)-qLtau*tau,
    cp_t=-N[J_R+(2/R+L0)J]+J Ltau*tau.

Differentiating T0 analytically, including spatial derivative slots, gives

    T0_t=N*T_N+tau*T_tau+(R/2)*tau_R.

The last term cancels identically in the time derivative of the chi
constraint. Therefore

    tau/N=-cTheta*T_N/(1+cTheta*T_tau),
    N_R/N=L0+Ltau*cTheta*T_N/(1+cTheta*T_tau).

The multiplier denominator must be monitored independently of the clock
inverse. At a regular center it tends to1+3cTheta/2, agreeing with FLRW.
This is a branch condition, not permission to clip a small denominator.
The exterior chi value and predicted derivative cannot both be clamped
independently if they disagree with the incoming solution.

An equivalent explicit coefficient implementation differentiates primitive
T0(A,sigma,w,M,Z,Pb,e,divZ,sigma_R), where M=cp/A and
Pb=A²j_b=sum(n_i*p_i). Conserved ordinary matter supplies

    Pb_t=-N*A[PrB_R+2(PrB-PtB)/R]-N_R*A(rhoB+PrB).

The inverse can be differentiated analytically; no finite-difference
time-Jacobian or altered reduced Poisson bracket is needed. Work is now
implementing these two small scientific components, then testing the
on-shell compressed-FLRW oracle before any nonlinear source integration.
This check is essential to the named changed-action source calculation,
not another default microscopic consistency project.

Keep the earlier physical Plummer source normalization Gbare*M/L fixed
when changing F: the effective cosmological coupling is Gbare/F, but the
action's bare coupling and physical ordinary source are not rescaled byF.
The earlier5kpc Plummer kappa=1e-7 and supported orbital preparation differ
from the infinitesimal test's200km/s timing convention; do not conflate them.
The old full quarter-orbit trajectory remains numerically unqualified and
is NOT being reused as physical initial evolution evidence.

Related vector-caustic motivation exists in the primary paper
[Contaldi, Wiseman and Withers](https://doi.org/10.1103/PhysRevD.78.044034).
Its different-theory results are not evidence for this completion; the
equations, numerical controls and limited claims above are project-specific.

### Compression component qualification, 2026-10-04

The inward radial kernel and exact local lapse/compression multiplier are
implemented in `invariant_clock_compression_radial_v001.py` and
`invariant_clock_compression_multiplier_v001.py`. Independent source review
checked the ordinary canonical momentum update, constitutive inverse,
time-derivative cancellation and center limit. Here `divZ=Z_R+2Z/R`;
it does not contain an additional physical `1/A` factor.

`invariant_clock_compression_components_v001.py` preserved six failures:
three came from the TEST oracle incorrectly using `-c*chi_t/N` in radial
pressure, and three from binary cancellation in the pointwise outward
coupled radial formula near the origin. The evolution multiplier itself
already contained the correct pressure. At fixed covariant radial vector,

    rho_chi=sigma*chi_R/A-chi²/(2cTheta),
    Pr_chi=sigma*chi_R/A+chi²/(2cTheta)-chi_t/(N*c),
    Pt_chi=-sigma*chi_R/A+chi²/(2cTheta)-c*chi_t/N.

These also reproduce the radial boost of the homogeneous perfect-fluid
stress. V001 receipt SHA
`01888050c639f6d0a9e6999661342277bb7cb5270761b34aa1875d646a0ec3f0`.

V002 reran only those six checks, correcting the pressure oracle and using
50-digit Decimal arithmetic with consistently regenerated on-shell inputs
for the cancellation-sensitive coupled algebra. The separate arithmetic
helper is `invariant_clock_compression_radial_v002.py`; no Decimal evolution
is proposed. It reused the 39 passing V001 controls and added three
high-precision A_R checks, totaling48 passing controls in0.298s. Receipt SHA
`09d9d3dbd3eae4a2138663aefb1f5e213ee6acb91488bb07e81eec68e44d8ff8`.
The binary outward helper's original1e-9 chi_R gate remains FAILED;
higher-precision algebra does not retroactively qualify that implementation.
The planned physical solve uses inward chi integration and integrated mass,
not outward shooting of the R^200 mode. Kernel power/log controls and the
binary local multiplier independently passed their original gates.

This qualifies components, not a galaxy or full discrete constraint flow.
Next: a supported positive ordinary Plummer source with conserved rest,
radial/angular motion, matched cosmic chi/lapse and no fitted incoming
phase. Test the complete discrete constraint tangent before interpretation.
Retain the old source's bare mass normalization and distinguish numerical
preparation from native galaxy formation. All scientific lanes remain open.

### First nonlinear ordinary-source results — NOT yet qualified

`invariant_clock_compression_source_v001.py` now implements the full
mixed-p action equations, positive conserved ordinary populations, radial
mass/chi constraints and supplied evolving exterior; source SHA
`a8b790f2bcf0c80d91e8a9b20b233389272ef57a9e7037364cc7c9d8399334f6`.
The bounded driver is `invariant_clock_compression_source_test_v001.py`.
Its exact compressed-FLRW comparator and outer history do not impose an
extra scalar phi_t or chi_t: those must follow the solved equations.

Initial128/256/512-node preparations passed the inherited1e-3 independent
Hamiltonian, mass-flow and chi-flow checks. At128 nodes a first short run
left the positive mixed-charge sheet on attempted step30, dt8.64740e-9;
half-step attempted59 and256-node half-step attempted118 reached similar
times around2.5e-7 Hunit^-1. This is NOT yet a physical branch exclusion.
The V001 exception checkpoint labels the attempted step while containing
the preceding accepted state; subtract one for these three specific failures.
V002 runner repairs that bookkeeping and reports final failed controls.

Preboundary runs at the same t=1e-7 Hunit^-1 reveal an origin artifact:
max|p| at128/256/512 nodes is2.18993e-7/1.14874e-7/5.65120e-8, roughly
halving. Mass-flow defects are.013275/.002440/.00020668; only the finest
passes1e-3. Therefore the coarse endpoint exit code0 is not evidence of
trajectory qualification; all receipts already say trajectory_qualified=false.
The log-radius kernel interpolates an even regular T0 on first midpoint
ratios1:3:5:7 that persist under refinement. For T0=T00+T2 R²+... this
creates O(h²) interpolation error, and recovering chi_R divides byR,
yielding O(h) odd-field error. Root and source reviewer independently
identified this specific mechanism. The pending repair is parity-respecting
R² interpolation with unchanged inward boundary and action, not damping,
clipping or a new physical assumption. Do not extend the old failed mesh
sweep blindly or declare the candidate rejected from these trajectories.

Independent weak-field early-time analysis nonetheless predicts a REAL
outward charge response for this specified initial source. With H neglected
only for this local Taylor estimate, p=Z=0, cosmic m approximately uniform,
F=1+3cTheta/2 and central proper time tau,

    g≈g_bare/F, chi_tau≈cTheta*rho_b/(2F),
    p_tau=p_tautau=0 initially,
    Z≈-cTheta*grad(rho_b)*tau²/(4F),
    delta_m≈m*DeltaPhi*tau²/2
            +C*cTheta*Delta(rho_b)*tau³/(12*KB*F).

The second term depletes clock charge at a density maximum. For the
declared truncated Plummer, Delta rho_b(0)=-15.06rho_b(0)/L², giving

    tau_evac≈[12*KB*F*m*L²/(15.06*C*cTheta*rho_b(0))]^(1/3).

Its order agrees with2.5e-7, but finite sound travel, constitutive response
and the numerical origin artifact forbid treating this as an exact event
prediction. A short Cauchy preparation does not establish native formation,
stationary MOND support or long-time stability. Equal coordinate source
and compensation integrals also do not exactly cancel canonical rest or
all kinetic/field energy; actual integrals and exterior defects are saved.

### Why negative charge is not an automatic technical continuation

Independent constraint elimination on an aligned background gives the
principal scalar action, with d=KXX>0, mu=m/X, eta=(2-KB)/KB and
B=6+4/cTheta,

    Lpr=d*varphi_dot²+B*zeta_dot²
       -k²[(2eta+mu)varphi²+4eta*varphi*zeta+2eta*zeta²].

The kinetic matrix is diag(d,B)>0 and det(gradient matrix)=2eta*mu.
For0<KB<2 and cTheta>0, negative m gives one negative squared principal
speed; near zero cs_slow²=mu/(d+B)+O(mu²). The direction(varphi,zeta)=(1,-1)
has positive kinetic coefficient d+B but gradient coefficient mu exactly.
Atm=0 the kinetic inverse can stay regular while one principal speed is
zero: neither a ghost nor a physical singularity follows merely from this.
Finite-k growth and effective-theory cutoff require separate treatment.
But entering m<0 is not an innocuous charge convention or an approved
repair. A lawful vacuum/free boundary must obey charge-current matching;
the vector contribution D need not vanish at m=0, so clipping is invalid.
This is a distinct statement from the older K(Q) tilt-fold failure.

### Parity repair and corrected nonlinear results

`invariant_clock_compression_radial_v003.py` implements cubic interpolation
in R² and cancellation-safe positive-series exponential moments. Source SHA
`9a0ff2237df9742375110ad5b404b92c825a1ab0ce989bb411d236bde74c094b`.
Exact even-polynomial and first-cell parity checks passed. The independent
smooth Plummer oracle initially failed its1e-6 gate at512 nodes(error1.78e-5);
the unchanged-gate1024/2048 refinement reached1.3456e-6/8.9316e-8.
Even-kernel V002 passes21 controls; receipt SHA
`ed42725662dc0efec5f42a5af8bda819375c9d1d926e0cbb8e5c36652e551be2`.
That component result does not qualify lower-resolution physical meshes.

`invariant_clock_compression_source_test_v002.py` selects only this changed
numerical kernel and fixes accepted-step bookkeeping. At t=1e-7, corrected
128/256/512-node max|p|=2.06531e-8/2.06791e-8/2.07088e-8; the old O(h)
origin artifact is removed. Independent final mass-flow errors are
3.60696e-4/2.29916e-5/3.51944e-6 and chi-flow errors
9.49395e-6/1.14086e-6/1.15821e-7. Listed control gates pass. Saved tags:
`preboundary128_even_v002`, `preboundary256_even_v002`,
`preboundary512_even_v002`, plus `preboundary256_time_v002` (half dt) and
`preboundary278_domain_v002` (roughly doubled extent, identical inner grid).
Full CHANGE-profile comparisons using inherited floors are pending; do not
replace those with matching maxima or a clean process exit.

Corrected boundary runs are also saved, not clipped:

| Tag | Last accepted time/Hunit^-1 | Accepted/attempted steps | Minimum s |
| --- | --- | --- | --- |
| boundary256_even_v002 | 2.525178789292004e-7 | 117/118 | .0038192788 |
| boundary512_even_v002 | 2.534919827811162e-7 | 235/236 | .0016566633 |

Each next attempted step fails the positive mixed-charge branch. Their
receipt hashes are respectively
`0216a087188dcf8295a427ccf1a3df6e32c07e33456db21befc706633b2671bf` and
`81698b393b1b955f090e045e0e1fb3710f7a7586910edb07d7fcf7c7674dd790`.
At the latter last state the upper clock-cap margin is still.99728 of its
initial margin. This is lower-charge evacuation, not the former upper-cap
failure. Cj/mu can exceed1 as mu shrinks; that does not by itself certify
nonlinear saturation. Constraint checks and event convergence remain scoped
as recorded, not a stationary galaxy/no-go verdict.

Reporting correction for the initial preparation receipts: their field
`background_j_outer` contains OLD-SECTOR j0, while `actual_j_outer` is total
j including compression. A correct exterior comparison adds c*chi_R/A to
the reference j0 too. The apparent~1.5% difference between those two raw
fields is NOT an established exterior mismatch. The pending comparison
producer reports the corrected total-versus-total diagnostic separately.

Next action is saved-state comparison plus a full-compression
Ricci/Raychaudhuri check, then decide what has genuinely been learned about
this source-selected branch. Do not rerun calibration, the infinitesimal
response or the old log-kernel trajectories. All11 lanes remain open.

### Completed saved-state comparison and physical scope (2026-10-04)

The above pending comparisons are now DONE, not a new trajectory run.
Producer `invariant_clock_compression_source_compare_v001.py`, SHA
`b63796dbd3471e58878fd3f461d4da6a7630af908ea3e30ddddf9230594bb962`,
reconstructs canonical phi_R and calls the old polar_compare_v003 complete
state/CHANGE comparison unchanged. The same1e-3 gate and floors apply.

| Comparison | Maximum error | Result |
| --- | --- | --- |
| 256 to512 nodes | 2.1864629616691735e-4 | PASS |
| 256-node half timestep | 4.84960019e-6 | PASS |
| doubled domain, identical inner grid | 4.33179300e-14 | PASS |

All are at t=1e-7 Hunit^-1. Full-material compression-aware Raychaudhuri
errors are about3.8e-6 at both tangent increments, also PASS. The receipts
preserve initial and final profiles, total momentum-reference correction,
ordinary rest/flux and energy reports, and pointwise branch margins.
This is a controlled SHORT-TIME response; the later branch event and a
long-time galaxy are not certified by these early comparisons. No scalar
charge clipping or continuation onto the negative-gradient branch occurred.

Receipts in this directory, with SHA256:

- `INVARIANT_CLOCK_COMPRESSION_COMPARE_grid256_512_v001_RESULT.json`:
  `8c12ff88ca86ccd0dbb92c1f38933c598c2754fbabee2ec9da41df8959c591f0`
- `INVARIANT_CLOCK_COMPRESSION_COMPARE_time256_v001_RESULT.json`:
  `3f93c5ab570b9963d9c446dd4c48af1da1eda1a5088ce74d4c5f5cc2f8e0f908`
- `INVARIANT_CLOCK_COMPRESSION_COMPARE_domain256_278_v001_RESULT.json`:
  `50da8234d682d292a38687a93dc9bc7dc0a6e4da07407efc0457e1d663a00063`

Fine-grid central m changes from.0075299996981 to.0070481901551,
delta_m=-.0004818095430; the separately derived short-time Taylor value
is-.0004859566846. That agreement is diagnostic, not a fitted acceptance
criterion. The source-only Taylor evacuation time2.49306e-7 predicts the
scale of the preserved later branch failures without certifying their
endpoint. These are declared Cauchy data, not a proof of native assembly.
The next constructive question is whether ordinary source assembly selects
a different lawful branch, or the effective constitutive model needs an
explicit revision. The same model must explain both domains; no hidden
incoming phase/halo fit or inherited old thermal calibration is allowed.

### Constructive branch question: dressed, tilted source versus sudden preparation

Independent analytical review confirms that the tested cosmic p=Z=0
preparation is constrained but undressed, not every possible assembly.
For a local exactly stationary spherical screen, write phi=omega*t+psi(R),
q=omega/N, w=psi'/A, sigma=U_R/A, c=sqrt(1+sigma²), X²=q²-w²,
Q=cq+sigma*w, p=sigma*q+c*w, mu=m/X and g=N'/N. Then

    e=(c*g+c')/A; Z=KB*e+C*p; D=C*(e-(1+j)*p);
    chi=-cTheta*(sigma'+g*sigma+2*sigma/R)/A;
    J=c*D-mu*w; (N*R²*J)'=0;
    c*chi'=A*Q*D-sigma*(Z'+2*Z/R).

A regular center without a scalar sink selects J=0. Aligned sigma=chi=0
then forces D=w=p=e=g=0 for m>0: preloading an aligned static MOND field
is not a lawful repair. Tilt/divergence can change this conclusion; a local
weak-field screen gives cTheta*(sigma''+2sigma'/R-2sigma/R²)-mu*Q²*sigma
approximately -mu*Q*p, with omitted time and sigma*divZ terms explicit.

Exact charged FLRW has p=D=0 but w=-X*sigma and J=m*sigma, not zero.
An exact static zero-current solution cannot be glued to that boundary.
The exact assembly identity is

    N*R²*J = -integral_0^R r²*partial_t(A*M) dr,
    M=mu*q+sigma*D.

It is A*M whose volume integral is conserved. Quasistatic matching must
retain its time terms, even when local fields evolve slowly. Ordinary
shells must retain their rest weights and angular momenta; circular balance
requires ell_b²=R³*g/(1-R*g), so radii and density adjust rather than
resetting velocities for an unchanged density profile.

At a regular tilted center sigma=sigma1*R, w=w1*R, g=g1*R, q0=X0,
Pr,b0=0 for the circular source, the reviewed central equations reduce to

    w1=q0*(rho_b0+q0*m0+2*K0+6*F*sigma1²)/(3*m0),
    g1=(1+mu0/C)*w1+q0*sigma1-sigma1²,
    X²=q0²-(q0²*g1+w1²)*R²+o(R²), F=1+1.5*cTheta.

The small arithmetic diagnostic `invariant_clock_stationary_center_v001.py`
evaluates the cosmic central charge and prospectively listed local q*m/rho
fractions, minimizing the quadratic X² curvature over sigma1 via a unique
cubic root. All28 numerical identity/derivative checks PASS. Receipt
`INVARIANT_CLOCK_STATIONARY_CENTER_V001_RESULT.json`, SHA
`93451bf26c61dfbfce4a481379bf0bfbd71618ae3ce57351d92c3915f8fd5ad4`.

| Local q*m/rho_b | Taylor floor scale / L | Central m / cosmic m |
| --- | --- | --- |
| cosmic (1.50e-6) | 1.5552e-5 | 1 |
| .01 | .25897 | 6681 |
| .03 | .72248 | 20044 |
| .1 | 1.73032 | 66813 |

These are LOCAL Taylor scales, NOT actual branch radii, selected profiles,
stability tests, or galaxy fits. The original central ordinary density is
only a reference; a conserved-shell equilibrium will change it. A larger
central charge is not automatically locally mass-dominating, but its
formation, global energy and reservoir costs remain unanswered. The uniform
reservoir estimate in the receipt is not an exact conserved-charge budget.
Next scientific target is the tilted matched quasistatic branch, not a
new arbitrary central-charge fit or rerun of the undressed trajectory.

## 2026-10-04: source-free assembly, early-phase audit and revised priority

The next-action sentence above is superseded: the smaller direct formation
question is whether evolving ordinary matter selects clock dressing at all.
An exact static zero-current BVP cannot supply its cosmological preparation.
The reviewed tilted equations remain a LOCAL necessary test, not a global
rescue. Tilt does not evade the regular-center clock lapse cap, and the
nonanalytic jp~p|p| interaction warrants o(R²), not an unproved O(R⁴), in
the center expansion above. This correction leaves its leading curvature
diagnostic unchanged.

`invariant_clock_compression_assembly_v001.py` reuses the full six finite-k
compression equations with prescribed test stress identically zero. The
ordinary continuity/Euler equations now evolve the source together with
the fields. Same joint-calibration constitutive point, cTheta=.01 and
20kpc comoving width (k=1/width); a=.01 to1, dust background. No new fit,
held source, incoming halo or chosen central charge. Two explicit unit
tangent seeds are ordinary-only at rest, and equal clock-charge/ordinary
contrasts with common velocity and Phi_dot=0. The latter is algebraically
reviewed, but NOT selected primordial adiabatic growing initial data.
Radiation, primordial preparation and the changed thermal normalization
remain missing from this DEVELOPMENT diagnostic.

V001 receipt SHA
`b2043bf559fb5aed6b22386183a389062e7b2698bc9e9575083ead6825121f10`.
Its1024/2048/4096 Gauss refinement passed the original full-history
component1e-4 test (maximum5.3153e-5). This qualification is insufficient:
`invariant_clock_assembly_audit_v001.py` applies the SAME relative gate
to every saved-history prefix/adjacent-epoch segment. It FAILS (prefix
state1.85, observables1.60; segment9.33/8.08). Huge endpoint growth had
masked misresolved early fast oscillations. Audit receipt SHA
`d8d1995600ab987f2aa8e1aa6363fe3608f67a6b1ea53160aee3565861f48596`.
Do not present the V001 full trajectory or illustrated finite-seed crossing
epochs as numerically qualified. Both receipts and the failed claim scope
remain preserved; this is a numerical issue, not a physical-model revision.

The saved-only audit also verifies two algebraic identities to about2e-16:

    S=delta_m/m-delta_b,
    Sdot=kphys²*[D-(m/Q)*(varphi-Q*theta_b)]/m,
    Phi=Z/2-[Q*delta_m+rho_b*delta_b
              +3H*(m*varphi+rho_b*theta_b)]/(2*kphys²).

It retains baryon-rest-slice contrasts delta_m/m+3Htheta_b and
delta_b+3Htheta_b. Negative S is not necessarily negative absolute clock
overdensity. In the provisional growing part both clock and ordinary
contrasts become positive, while most enhanced potential is Z/2, NOT
additional clock density. This is a candidate interaction modification,
not evidence for a gravitating record halo. Unit-seed endpoint densities
of order1e23 are linear TRANSFERS, not physical galaxies.

Validity must include C*j/mu as well as clock-branch headroom, matter/clock
contrasts, vector tilt and |p|/bs. The J interaction can invalidate the
linear extrapolation before any density becomes order unity. Illustrative
amplitudes1e-5/1e-9/1e-12 are neither fitted nor observational primordial
amplitudes. The revised numerical method retains all fast modes rather
than filtering them, and does not certify a nonlinear galaxy.

CF4/Pade13 V0024096/8192/16384 refinement improves but still FAILS full
prefix/segment gates (state.0372/.0468; observable.0175/.0468). Its receipt
SHA `e3b6a9eed1f3b6230958abe4aff625a2545f54913a1d5981514bafb93eaba9e4`
is preserved. V003 bounded refinement is the current numerical task;
no physical conclusion relies on a failed phase check.

Independent source-only analysis identifies a candidate finite-Q growing
channel, distinct from fast phase error. With B=6+4/cTheta and mu=m/Q,
a late/subhorizon approximate dispersion relation is

    (d+B)*lambda^4+(mu*kphys²-d*Q²)*lambda²-rho_b*kphys² ~ 0.

This is not yet a full trajectory stability certificate. It suggests a
useful distinction: an interaction-driven growing mode may provide source
assembly but requires the SAME J nonlinearity to saturate before invalid
linear extrapolation. Neither its existence nor its huge formal gain is
automatically an observational success or an exclusion.

The separate `SHARED_CONSTITUTIVE_ALTERNATIVE_SCREEN_V001.md` preserves
the restricted pure-vector sign obstacle and a two-invariant constructive
alternative. No new function is adopted and no native derivation claimed.
All11 lanes, both CMB scopes and independent final synthesis remain OPEN.

### Full-phase repair completed; bounded nonlinear question

V00332768/65536/131072 still failed, worst.01428; its SHA is
`c76974fdebc68f017b2947b5e2434cd0fff27b1eeabe4eeed25a44f7168c106c`.
V004 adds262144/524288 steps in one151.32s checkpointed six-state worker,
without changing physical parameters/seeds or filtering modes. It PASSES
all unchanged1e-4 prefix/segment gates: state1.48083e-6/1.76815e-6,
observables8.15039e-7/1.63324e-6. Einstein identity3.75e-16. Receipt SHA
`7ed429224a93aaef44c97dc2bdaedce5c2f3fc7b685ceb863ae99c91fc9f304b`.
No numerical worker remains live after this result.

Saved interpretation audit V002 SHA
`e92edaa10f1263f924a038408eb320f42f4d78d28bc16594e983b7dad02acb9d`
passes relative-current and complete source-sum identities (~2e-16).
At a=.1, Z/2 supplies96.8%/96.2% of Phi in the two preparations; at
a=.316 it supplies99.889%. These are qualified infinitesimal transfers,
not a gravitating-record halo or finite-amplitude galaxy.

For the illustrative1e-12 equal-contrast seed, at a=.5233 Cj/mu=.1303,
ordinary contrast.0010187 and norm/Bernoulli diagnostic
d*|grad(varphi)|²/(2Q|delta_m|)=.0002945. At a=.56234 the linear prediction
is Cj/mu=1.7796, ordinary contrast.0099584 and norm ratio.0031001. This
ordering motivates a bounded first-nonlinearity test, not a chosen
primordial spectrum. At1e-5 the norm/advection corrections are already
percent-level near onset; |p|/bs alone would have missed them.

Independently reviewed periodic semilinear insertion: with physical
gradient nabla, p=nabla(varphi+Qalpha), define N_J=-C*j(p²)*p and its
zero-mean periodic primitive n_J=nabla^-1 N_J. Add only

    delta(dm_dot)=-nabla N_J, delta(Z_dot)=Q*n_J

to the six retained linear equations. These insertions cancel in Phi_dot
and conserve the retained-order periodic charge a³*(dm-3mPhi). Reflection-
symmetric cosine preparation has zero mean current. All J-generated
harmonics must be retained/refined; a single harmonic is not closed.
This is NOT a full nonlinear action truncation: ordinary advection, exact
charge/norm/current and nonlinear stress generate additional harmonics and
mean terms. Their equation residuals must be bounded relative to the small
surviving soft terms, not to the separately cancelling large terms.

Prospective diagnostic: begin from the qualified equal-contrast1e-12
history at a=.4869675 (saved epoch54) and evolve a short periodic interval
without changing phases, velocities, parameters or ordinary forcing.
Numerical state/observable/refinement gates stay1e-4; use a SEPARATE1%
asymptotic validity ceiling for ordinary contrast, relative norm correction,
branch shift and omitted stress, with all values reported. Crossing that
ceiling is an approximation boundary, NOT physical failure or permission
to relax it. This diagnostic does not fit or select a physical primordial
amplitude. Determine whether full J moderates the growing mode before that
boundary; otherwise upgrade the action-consistent weak-field equations.

### Semilinear run completed, failed spatial gate; exact upgrade required

`invariant_clock_semilinear_assembly_v001.py` ran33-node512/1024/2048 and
65-node2048 histories in22.15s. Receipt SHA
`0cabe0b6636312b7bf7b4c665912bc033552c8f08cde5384d0c842efc7f928ca`.
Time refinement passes1.77e-5/1.85e-5; spatial full-state/observable
refinement FAILS.1000/.1021 against unchanged1e-4. Retained nonlinear
constraint identity passes3.1e-16. Do not promote the trajectory or simply
score its seemingly stable fundamental while unresolved harmonics remain.

The specified diagnostic amplitude was1e-12 at epoch54, not a fitted
primordial spectrum. The formal end at a=.6043 has density fundamental
.0440, peak.0829, and Cj/mu up to2.392. Its apparent moderation is NOT a
qualified saturation result. Even the partial asymptotic estimates exceed
1% by saved a=.564876 (ordinary contrast.01119/advection.01114).
There is no demonstrated arrest before the approximation boundary.

Source-only code review confirms FFT/gradient/inverse signs, cosine
normalization and Gauss stage ordering. It also narrows the diagnostics:
`within_declared_asymptotic_ceiling` is only a screen of LISTED proxies,
not a proven1% bound on the full action. The current proxy omitted
+m*deltaX*w/Q² and delta D=-C*(2/KB+j_t)*v*deltaX at fixed physical Z,
among other nonlinear kinematic terms. Stress proxies omit parts of the
compression/momentum/anisotropic response. 3N quadrature is overintegration,
not exact dealiasing of a nonpolynomial |p| law. Retained mean charge is
zero by symmetry, not an independent exact-Noether conservation check.
Preserve all these limitations; no expensive late refinement of an already
invalid physical truncation is the default next action.

Next is the source-reviewed exact1D synchronous-comoving canonical action:
it retains ordinary matter advection through its conserved rest weight,
full local K(X) inversion, J and compression, before shell crossing. This
is a targeted physical upgrade, not a new fitted source or protocol layer.
Use the qualified first-order Newtonian-to-synchronous seed only as a
small-amplitude guess and solve its exact Hamiltonian/momentum constraints.
Do not recycle the older K(Q) plane model as if it were K(X).

### Exact periodic conserved-source equations reviewed

Use synchronous-comoving dust coordinates before shell crossing, metric
ds²=-dt²+A²dx²+B²(dy²+dz²), a=lnA, b=lnB (these local a,b are not the
cosmic scale factor), V=AB², covariant vector component u=U_x. Define

    sigma=u/A, c=sqrt(1+sigma²), w=phi_x/A, q=phi_dot,
    X=sqrt(q²-w²), p=sigma*q+c*w, e=(u_dot+c_x)/A,
    Theta=a_dot/c+2*c*b_dot+sigma*u_dot/(A*c)
          +(sigma_x+2*sigma*b_x)/A,
    L=V[-4*a_dot*b_dot-2*b_dot²+KB*e²+2*C*e*p
         -C*p²-C*J(p²)+2*K(X)-cTheta*Theta²]+2*(B²/A)*b_x².

This is the exact symmetry-reduced parent action, not the semilinear
insertion. With chi=-cTheta*Theta, Z=KB*e+C*p and D=C*(e-(1+j)*p),

    pi_a=-4*V*b_dot+2*V*chi/c,
    pi_b=-4*V*(a_dot+b_dot)+4*V*c*chi,
    pi_u=2*V*(Z+sigma*chi/c)/A,
    pi_phi=2*V*(m*q/X+sigma*D).

Let P=pi_u/(2*B²), Gx=sigma_x/(A*c²)+2*sigma*b_x/A. Invert using

    b_dot=-pi_a/(4V)+chi/(2c),
    a_dot=(pi_a-pi_b)/(4V)+(c-1/(2c))*chi,
    e=(P-sigma*chi/c-C*p)/KB,
    F1=m*q/X+sigma*D-pi_phi/(2V)=0,
    F2=chi/cTheta-[(1+2sigma²)*pi_a+pi_b]/(4Vc)
       +(2-1/(2c²))*chi+sigma*e/c+Gx=0.

The symmetric Jacobian in q,chi is

    J11=d*q²/X²-m*w²/X³-sigma²*C*(2/KB+j_t),
    J12=J21=-(C/KB)*sigma²/c,
    J22=1/cTheta+2-1/(2c²)-sigma²/(KB*c²).

At rest this is diag(d,F/cTheta). Continue its regular branch and monitor
the determinant; no global positivity or branch clipping is assumed.
Since F2 is linear in chi for fixed q, eliminate chi and perform a stable
one-dimensional K(X) auxiliary-s inversion with the Schur derivative.

Canonical evolution comes from the local Lagrangian variation at fixed
velocities: pi_dot=L_coordinate-partial_x L_coordinate_gradient. The
useful differential is

    dL=Lcore*dV+V*(2Z*de+2D*dp+2m*dX+2chi*dTheta)
       +2*(B²/A)*[(2db-da)*b_x²+2*b_x*db_x].

Preserve the lapse/shift equations even after gauge fixing. For
Hcan=sum(pi*q_dot)-L and fixed ordinary rest weight pi_T,

    Hcan+partial_x[4*(B²/A)*b_x+c*pi_u]+pi_T=0,
    pi_a*a_x+pi_b*b_x-partial_x pi_a-u*partial_x pi_u
       +pi_phi*phi_x=0,
    rho_b=pi_T/(2V).

Independent review confirms the lapse-gradient coefficient is c*pi_u,
including compression. Ordinary matter advection is now retained through
V, without resetting rest weights or prescribing density. The homogeneous
oracle is chi=-3*cTheta*H, pi_a=-4*V*F*H, pi_b=2*pi_a,
pi_phi=2*V*m, 3*F*H²=rho_b+Q*m-K.

The reviewed first-order Newtonian-to-synchronous map uses T=theta_b and
L_dot=T/abar², with the initial spatial shift L=0:

    delta a=delta b=-Phi-H*theta_b,
    u=partial_x(alpha+theta_b), phase=varphi-Q*theta_b,
    delta_b_sync=delta_b+3*H*theta_b,
    delta b_dot=-Phi_dot-Hdot*theta_b-H*Phi,
    delta a_dot=delta b_dot+kphys²*theta_b,
    u_dot=partial_x E_potential, q-Q=(delta_m+3Hm*theta_b)/d.

This provides small-amplitude initial GUESSES, not exact constrained data.
Fix mapped spatial fields, field canonical data and ordinary rest weights,
including explicit total ordinary mass and total scalar charge. Solve H
locally for pi_b on the expansion-connected branch and the remaining
periodic momentum equation for pi_a, with an explicit homogeneous shear
condition and periodic compatibility check. Recompute all velocities from
the exact Legendre map, not by reimposing the linear values afterward.
This remains a1D periodic development experiment, not a formed galaxy.

Independent initial-data review fixes the one remaining homogeneous freedom
by zero proper-volume mean shear, <V(a_dot-b_dot)>=0. Equivalently use
<(2*pi_a-pi_b)/4+V*sigma²*chi/c>=0, not merely mean(pi_b-2*pi_a)=0.
Do NOT additionally fix mean expansion or both mapped metric velocities.
For the local Hamiltonian solution pi_b=P(pi_a), P'=−a_dot/b_dot. The
reduced momentum Newton operator is
[a_x−(a_dot/b_dot)*b_x]*delta_pi_a−partial_x(delta_pi_a).
Its constant kernel at FLRW is fixed nonsingularly by the shear condition.
Initial spatial volume is explicitly normalized by a common constant
−log(mean(exp(3*f*cos(x))))/3 in both metric logs, before normalizing
integrated ordinary rest weight and scalar charge. These are counted
nonlinear preparation choices, not fitted physical parameters.

Saved-only semilinear audit (no repeated evolution),
INVARIANT_CLOCK_SEMILINEAR_SAVED_AUDIT_V001_RESULT.json,
SHA256 5400ea59b5c1955c89254e972a0192f22895cd44b23c61daa92578064097a6b5:
even the early prefix before the listed advection screen fails spatial
refinement (0.01644/0.01729 versus1e-4). Doubling nonlinear quadrature from
3N to6N changes current divergence by6.79e-5 initially and9.37e-4 finally
on65nodes. Missing current terms checked here are small; they do not
establish a full-action error bound. The failed semilinear receipt remains
unqualified and is not evidence for physical saturation.

### Exact periodic action implemented; independent component checks pass

The source-only exact module is `invariant_clock_periodic_exact_v001.py`,
SHA256 24bf29a2b41de34eb105c1191b2f844be86391675160476fffa478752fe8772b.
It includes background-subtracted canonical evolution, regular-sheet local
Legendre inversion, both constraints, and stress coefficients. It is the
K(X)/J/compression action above, not the earlier K(Q) plane implementation.

Components V003 passes30 listed checks on17/33 grids: independently supplied
resolved primitive velocities recover to9.01e-11 relative; homogeneous
RHS4.94e-16; exact initial Hamiltonian background2.86e-15 and perturbation
1.19e-12; momentum6.14e-7; scalar/ordinary conserved totals pass1e-12.
The exact Hamiltonian-flow identity passes at two tangent increments to
2.51e-13; the analytic nine-term momentum-flow identity passes1.27e-15.
Receipt SHA256 c366ac8a6ca2aa8d71ff3d7411e3592d1cd35b52bb96b4fba57957b4c697db39.
Initial V001/V002 failures are preserved (ecef9a67c548ad30281d813b2bc22b0539995044bfdc0a598de101d686b68b7c,
7b22c43a2ab52370547922307e9cd7ce12366010c60f7a9a97b51c0e15e79104):
background-scaled stopping was premature, and direct background subtraction
did not resolve the tiny transverse velocity. No acceptance gate was relaxed.
The resolved forward-oracle state is explicitly a numerical control, not a
change of the scientific seed. Exact constrained seed source is initial V002.

An independent variation of the original integrated Hamiltonian, without
using the implementation's delta-core expressions, passes18 checks at two
increments on17/33 grids (worst9.65e-9 versus1e-4). The linear modal operator
satisfies the canonical symplectic identity to2.89e-17. Receipt
INVARIANT_CLOCK_PERIODIC_VARIATION_V001_RESULT.json SHA256
6e3d30ebc44f2e31921cbdc6178df0d8c1daa60940a87212a38d291eb24d4ff6.
Independent review corrected the modal preconditioner's pi_a gradient sign
BEFORE execution; finite exact-RHS tangent controls then pass3.03e-10.

The first bounded exact evolution attempt stops before its first accepted
step: stage iteration changes6.23e-11 fail the fixed1e-11 gate. This is NOT
a physical branch failure or saturation result. Its receipt is preserved,
SHA256 f8c24fa49892dbcf5ed1b04e2956269063871b6e4ea08e1e99305260af556586.
Next numerical repair retains delta-s as the local Newton unknown, avoiding
loss of tiny perturbations through s−sbar, and tightens inverse precision.
No field filtering, hidden fit, tolerance relaxation or trajectory claim.

### Unreduced numerical limitation and equivalent constraint-reduced chart

Delta-s coreV002 is independently rechecked: componentsV00430 and
Hamiltonian-variationV00218 controls PASS. Core SHA256
dd8583d6cded1520e6ff8a3b9b7c93a0e14e22ce1e6cc88af991214783da1957;
receipts f4bc4d6c9b5ace57b9d6848fd0b27a299e429eb3a5c4c1f8d3f5b2c99295e831
and13afe44b5a5939f82678aea5b9af53f0ac8a9002484e9283870aaf04d876c11b.
Exact evolutionV002..V006 still fail the1e-11 stage gate. Direct stage
defect correction, smaller steps and direct spectral scalar-current
derivative do not remove the highest-mode precision floor. The zero-mode
derivative repair is mathematically sound but does not explain the remaining
nonzero-mode residual. Independent Lawson-RK4 V007 stops within16steps at a
local-inverse residual1.066e-16 versus its tightened1e-16 gate; its rapidly
changed trial state is unqualified. All attempts are preserved, no full
history or nonlinear physical result claimed.

The frozen unreduced canonical tangent is extremely nonnormal (matrix
1-norm about1e11 at this representation). Its apparent instantaneous large
real roots are NOT the qualified physical growth spectrum: the constrained
subspace and physical-coordinate map vary with time. No instability claim
can be based on that frozen unconstrained eigenspectrum alone.

Two independent analytical reviews support the following exact reduction.
Evolve fa,fb,u,phase,pi_u,pi_phi and ONE homogeneous mean(delta_pi_a).
Keep every mode of fixed ordinary restweight pi_T. Reconstruct pi_a,pi_b
from H=0,D=0 at each RHS with the evolved meanpi_a, not zero mean shear.
Evolve the latter by mean of the original canonical pi_a RHS. For defects
r_a=dot(pi_a_reconstructed)−F_a and r_b analogously, the differentiated
constraints imply

    a_dot*r_a+b_dot*r_b=0,
    partial_x(r_a)=[a_x−(a_dot/b_dot)*b_x]*r_a.

On a regular branch with b_dot nonzero, a nonzero real continuous solution
of the homogeneous first-order equation has one sign. Its mean is zero by
the evolved meanpi_a equation, so r_a=r_b=0. No physical degree of freedom
or mean-shear dynamics is removed. This is an equivalent constrained chart,
not a post-step projection, fitted halo or changing action.

The linear constraints (nonzero comoving Fourier k) are

    delta_pi_a=pi_a_bar*(fa+2fb)+pi_phi_bar*phase,
    H*(delta_pi_a+delta_pi_b)+Q*delta_pi_phi
      −V*core_bar*(fa+2fb)−2a*chi_bar*ik*u−4a*k²*fb
      +ik*pi_u+delta_pi_T=0.

Retain the last, ordinary-source term in the reduced operator or its affine
remainder. At mode0, pi_a is the independent evolved homogeneous momentum.
The discrete spectral implementation also needs an eliminated-momentum
tangent check: continuum Leibniz identities alone do not certify spectral
products. Monitor reconstruction rank, b_dot, constitutive regularity,
positive volume and dust single-valuedness. A failure of this chart does
not by itself exclude the physical action. Same outer numerical gates and
all11 scientific lanes remain open; no new thermal calibration is inherited.

### Paired reduced chart and local nonlinear restoring response (2026-10-04)

Reduced componentsV001 andV002 preserve failures of reflection arithmetic.
V003 uses explicit paired cosine/sine derivatives for BOTH parity sectors;
no allowed harmonic or RHS is projected away. Initial-only pairing changes
the already symmetric preparation by at most4.75e-15. All28 controls on
17/33 grids pass, including original eliminated-momentum tangents below
3.8e-8 and independent FFT derivatives below2.1e-14. Receipt SHA256
ec7d78567d50cf486698ea1e57aa17869ce84cd09c29f53971f36ebf3bf6e8ab.

Full reduced evolutionsV001..V005 remain unqualified. Explicit stages
lose their local inverse; implicit stages fail the unchanged1e-11 residual
criterion. V004's accidental weight-variable shadowing is a preserved
technical failure, repaired inV005. Tightened constraints and multisecant
acceleration do not remove the remaining high-mode charge/mean-momentum
floor. No failed trial is a physical branch exclusion or saturation result.

Independently, two source-only derivations retain lapse and shift to obtain
the coupled local LONGITUDINAL principal action at a smooth on-shell point.
Use an orthonormal aether-rest frame and a wave parallel to the local p.
The temporal phase component is q_U=sqrt(X²+p²)=c*q_coordinate+sigma*w,
not the synchronous coordinate q. Set mu=m/X, d=KXX, eta=C/KB,
B=6+4/cTheta and jt=d(jp)/dp. Then

    A=d+(d-mu)*p²/X²,
    bK=(d-mu)*q_U*p/X²,
    mu_eff=mu+C*jt-(d-mu)*p²/X².

The K(X) Hessian is independently the Lorentz boost of diag(d,-mu).
With E=alpha_dot+n and bshift=beta-alpha, lapse/shift principal constraints
are KB*E+C*varphi+2*zeta=0 and
2*zeta_dot+cTheta*(3*zeta_dot+k²*bshift)=0. Their elimination gives

    Lpr=A*varphi_t²-2*bK*varphi_t*varphi_x+B*zeta_t²
      -(2eta+mu_eff)*varphi_x²-4eta*varphi_x*zeta_x-2eta*zeta_x².

The characteristic polynomial for v=omega/k_physical is

    (A*v²+2*bK*v-2eta-mu_eff)*(B*v²-2eta)-4eta²=0.

For A,B,eta,mu_eff>0 the principal energy is positive, with spatial
determinant2eta*mu_eff, and the four longitudinal characteristic speeds
are real. The inherited J has1<=jt/j<=2. Accordingly Cj/mu=1 adds between
mu and2mu to the longitudinal spatial stiffness before the explicit
K(X) tilt subtraction; it is NOT itself an instability threshold.
mu_eff=0 is only the boundary of this sufficient positive-energy test.
When it fails, the mixed derivative means the full quartic must still be
examined; a negative spatial coefficient alone is not a proof of complex
characteristics. Normal-slice speeds transform as
(sigma+c*v)/(c+sigma*v), requiring regular denominators and admissible time.

The14-check audit
INVARIANT_CLOCK_NONLINEAR_PRINCIPAL_V001_RESULT.json, SHA256
5d7537e91da623bad38a993d36a2baacb018b8f32772a18d6c9e4b4f73cb67f8,
finds positive rest-frame energy at every qualified initial17/33 point;
the largest K-tilt fraction of mu+Cjt is4.42e-10. At prescribed Cj/mu=1
and four frozen epochs, the tilt fraction is below1.04e-6 and stiffness
is approximately3mu. Those probes are NOT later evolved physical states.

These are strict local principal statements. Background stress/anisotropy,
curvature, gradients, finite-Q terms and ordinary Jeans coupling remain
in the actual evolution and may dominate a very slow principal mode.
Dust adds an advected/zero-speed principal sector. Neither all-direction
hyperbolicity, nonlinear arrest, a galaxy nor observational superiority
follows. This is a constructive physical reason to test J saturation,
not a replacement for the still-missing exact nonlinear calculation.
