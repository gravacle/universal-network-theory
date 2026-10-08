# A minimal shared-state galaxy BVP with hard energy retained

2026-09-29. Analytical, unrun, explicitly conditional macroscopic completion.
This defines an axisymmetric existence/consistency screen before a disk fit.
It neither modifies a frozen calculation nor claims a native derivation of
the new scalar constitutive action. It is not a spherical surrogate.

## 1. Declare the candidate completely

Use c=1, signature (-+++), M2=(8 pi G)^-1, the preferred normal
u_mu=-partial_mu T/sqrt(-partial T squared), its spatial projector P,
and acceleration a_mu=nabla_u u_mu. Write g=sqrt(a_mu a^mu),
h(g)=g/sqrt(1+g^2/gs^2), and h_mu=h(g)a_mu/g, continuously at g=0.
For positive soft weights w_j retain the existing constrained spatial vectors
y_j, their projected normal velocities v_j=P nabla_u y_j, and positive
quadratic-plus-quartic potentials V_j.

The separately named candidate is

    S=integral sqrt(-g4) { M2 R4/2
       +C[sum_soft w_j(m_j v_j^2/2-V_j(y_j)+b_j h_mu y_j^mu)
           +beta(I sqrt(-partial theta squared)-e_R(I,h(g)))
           -DeltaU] } + S_ordinary,
    b_j=kappa delta_j, Kb=kappa(sum_soft w_j+beta),
    C=2M2/Kb.                                             (1)

The hard function e_R is the same scalar tilted-quartic orbit energy with
e_I=omega and e_h=-b_R<y>, b_R=kappa R. Here its even dependence on signed h
is **adopted as a rotationally invariant scalar constitutive function**.
It is not asserted to describe every orientation/angular-action state of
the original vector oscillator, or to be the old coherent pulse state.
The full square-root phase term is a specified nonlinear alpha-one
completion, not merely the earlier quadratic counterterm.

Keep the absolute matched constant

    DeltaU=-sum_soft w_j e_j,min(gs)-beta e_R,min(gs).

Do not subtract e_R(0,h) again inside a galaxy. At I=0 that source-dependent
minimum remains part of the hard response. The bare Kb g^2/2 is already
supplied by the matched gravitational sector; adding it to (1) again would
double-count the contact. An independently adjustable vacuum offset or local
hard abundance would define another model.

The same aligned FLRW candidate has h=0 and, on its declared unexcited soft
background,

    I_bar_dot=-3H I_bar,
    rho_mode_bar=C[beta e_R(I_bar,0)+DeltaU],
    p_mode_bar=C[beta(I_bar omega_bar-e_R(I_bar,0))-DeltaU]. (2)

Together with ordinary species these determine H and Hdot. Shared calibration
fixes the spectrum, physical scales, I_bar at a stated epoch and DeltaU.
A finite-R test must use its finite-R calibration and pressure, not paste
the formal R=infinity numerical calibration onto a different spectrum.
The microscopic origin of these coefficients is not required to test (1)
as an explicitly labeled effective model.

## 2. Specify the stationary branch, not a free halo profile

First define the exact static core on a finite domain:

    ds^2=-N(x)^2 dt^2+gamma_ij(x) dx^i dx^j,
    T=t, theta=mu t, N>0, a_i=D_i ln N.

The soft velocities vanish on this branch and their full static equations are

    kappa delta_j^2 y_j+u4 |y_j|^2 y_j=b_j h_vector.        (3)

Their unique minima align with h. This is an explicitly stationary soft
state, not a claim of damping or automatic relaxation of an excited history.
The vectors remain in (1); static elimination uses their equations rather
than dropping their source energy. Nonzero soft actions would require a
different retained-state closure.

For occupied hard I the phase equation is

    N omega_R(I,h)=mu.                                   (4)

One common cosmic/boundary state sets mu; I(x) is then a solved quantity.
On a declared convex branch e_II>0, the constrained I>=0 Legendre condition
is I>=0, e_I-mu/N>=0, I(e_I-mu/N)=0. The empty boundary applies only when
it is the admissible continuation of that convex constitutive problem.
At finite h, e_II can vanish or change sign. Record branch loss or
multiplicity; do not clip an occupied root to zero or select a different
root to improve the observed curve. Local softening of this fluid reduction
does not imply that the original confining oscillator is itself unstable.

In the strictly harmonic occupied limit, omega_R is constant and (4)
forces N constant. That limit cannot supply a nontrivial static zero-flow
hard density. Finite pressure or an explicitly nonstatic/streaming state
is essential, rather than an optional ignored source term.

## 3. Exact static stress and field equations in any spatial geometry

After (3)-(4), define

    E=sum_soft w_j e_j,min(h)+beta e_R(I,h),
    Pi=-sum_soft w_j e_j,min(h)+beta(I omega_R-e_R),
    B=sum_soft w_j b_j |y_j|+beta[-e_R,h],
    F^i=h'(g) B a^i/g,     D^i=Kb a^i-F^i.             (5)

The formulas use the continuous vector limit at g=0, not an arbitrary
direction at a critical point. In the static reduced action,

    S_static=integral dt d3x N sqrt(gamma)
                  [M2 R3/2+C(Pi(mu/N,h)-DeltaU)] + S_b, (6)

the spatial metric, lapse and ordinary matter must still be varied, with
their boundary terms retained. Envelope derivatives include the implicit
I and soft minima correctly: Pi_Q=beta I and Pi_g=F for Q=mu/N.

Lapse and spatial-metric variation give

    rho_mode=C[E+DeltaU+a_i F^i+D_i F^i],
    S_mode,ij=C[(Pi-DeltaU)gamma_ij-a_(i F_j)],
    S_mode=C[3Pi-3DeltaU-a_i F^i].                      (7)

On (3) F is parallel to a. Thus the tensor is symmetric without assuming
spherical symmetry. It has both the intrinsic hard pressure and the
polarization anisotropy. In particular neither rho=C E nor a baryon-only
force equation is the same source.

Writing rho_tot=rho_b+rho_mode and S_tot,ij=S_b,ij+S_mode,ij, the exact static
Einstein system is

    R3=2 rho_tot/M2,
    D^2 N/N=(rho_tot+S_tot)/(2M2),
    R3_ij-N^-1 D_i D_j N
              =[S_tot,ij+gamma_ij(rho_tot-S_tot)/2]/M2. (8)

Only an independent constraint/evolution subset is solved, with the remainder
checked. Combining the lapse equation with (7) gives a useful exact scalar
constitutive equation in the *same* spatial geometry:

    D_i D^i=4 pi G Kb(rho_b+S_b)
                    +E+3Pi-2DeltaU-Kb g^2.             (9)

On the left D_i is the covariant derivative and D^i is the response defined
in (5). Equation (9) is not a substitute for the spatial metric equations.
Static stress conservation supplies an independent check,

    D_j S_tot^j_i+(rho_tot delta_i^j+S_tot^j_i)D_j ln N=0. (10)

The static phase current has no spatial flux and satisfies its continuity
equation. The preferred-clock variation is not dropped: at aligned static
data its acceleration variation is a time derivative of a spatial gradient,
and integration by parts gives a time derivative of the stationary
polarization-divergence coefficient. It vanishes on this branch. This says
nothing about time-dependent clock stability.

## 4. Axisymmetry and the weak-field implementation

For a reflection-symmetric nonrotating static core one may use cylindrical
coordinates (varpi,z,phi) and spatial gauge

    gamma_ij dx^i dx^j=A(varpi,z)^2(dvarpi^2+dz^2)
                              +Bmetric(varpi,z)^2 varpi^2 dphi^2.

Retain both metric functions; imposing A=Bmetric or Phi=Psi at the outset
would discard part of the anisotropic-stress equation. Axis regularity
requires Bmetric=A on the axis and the appropriate even normal derivatives;
midplane-reflection conditions hold at z=0. The observed disk density remains
axisymmetric, not a spherical enclosed-mass replacement.

The leading weak-field lapse equation uses Phi=ln N, physical spatial
coordinates at a stated epoch, g_vector=grad Phi, and the flat principal part

    (1/varpi)partial_varpi(varpi D_varpi)+partial_z D_z
                =4 pi G Kb(delta rho_b+delta S_b)
                               +delta(E+3Pi).          (11)

Here subtraction and errors have the specific meaning in section 5. The full
nonlinear dependence of I on N and of F on g is retained: small Phi does not
justify expanding I when the compressibility is large. Equation (11) cannot
reuse the old mu(g) table or fixed-action response without re-solving (4).

The spatial metric must also be reconstructed from (8). For example the
linear-metric scalar constraint has leading source

    Laplacian Psi=4 pi G delta rho_b
                            +[delta E+div F]/Kb,        (12)

with the a.F contribution, nonlinear metric terms and cosmological derivative
terms included at their required order rather than claimed absent. The exact
stress (7) defines them. In a general weak-field spatial gauge a traceless
spatial metric perturbation can also be required; its equation contains
the full S_ij, not just its trace. The exact system (8) is the reference for
assessing the accuracy of a scalar-potential truncation. Keeping a selected
g^2 or a.F term while ignoring equally large metric corrections is not a
qualified higher-order approximation.

In the nonrotating weak-field limit circular test-body motion reads
v_c^2=varpi partial_varpi Phi on the midplane, and lensing uses the same
metric and its actual observer/source boundaries. In SI units Phi is
dimensionless, v_phys^2=c^2 varpi partial_varpi Phi and acceleration is
c^2 grad Phi. The phase/source scales must use that conversion consistently.

## 5. Cosmological subtraction, boundaries and support

An occupied expanding FLRW exterior is not a globally static asymptotically
flat spacetime. An exact continuation needs the time-dependent equations of
(1), metric/clock matching and phase-current flux through the matching
worldtube. No material wall or surface stress is introduced without its
energy/work. In particular, a cosmic normal with zero acceleration must not
be replaced silently by a static accelerated normal in a different chart.

A controlled first existence screen may instead be a local quasistatic
interior at a specified cosmic epoch. Derive (11)-(12) by subtracting the
homogeneous FLRW Einstein equations of (1), then expanding the *perturbation*
equations on scales L with HL much less than one. Since background F=0,

    delta E=E-E_bar,  delta Pi=Pi-Pi_bar,
    delta rho_mode=C[delta E+a.F+div F].                (13)

The constant DeltaU cancels from the subtracted source, not from the action.
It remains in H, Hdot, the cosmic state and the outer metric. One must not
solve the un-subtracted static system with DeltaU deleted, or impose an
isolated-flat infinite boundary on its positive-vacuum background. The
neglected expansion/time-derivative and nonlinear metric terms must be
smaller than the intended field accuracy; HL alone does not prove that an
extremely cold hard population can equilibrate in less than H^-1.

Choose the outer worldtube/domain and its metric/environment from one declared
matching prescription, not a fitted halo radius. Cosmic proper-time
normalization fixes the reference omega_bar(I_bar,0) at that epoch. A static
interior has a single constant mu; the boundary value of I must satisfy
omega(I_b,h_b)=mu/N_b. Uniform I_b, arbitrary fixed N_b and an angularly
varying h_b cannot all be imposed independently. A finite boundary with
negligible peculiar source can approximate the cosmic state only to a
checked tolerance. Constant rescaling of time rescales N and mu together,
not the physical ratio mu/N. Exterior potentials and clock matching that
affect this ratio are physical data, not gauge freedom to tune the density.

The ordinary source must also be supported. An exact static model requires
S_b,ij and zero momentum consistent with (10), not pressureless matter held
at rest in a nonconstant N. An actual rotating disk is stationary rather
than static: at leading weak-field order its measured density can supply
rho_b while rotational/dispersion stress and frame dragging are retained
or bounded at their proper order. If those corrections are material, solve
the stationary shift/momentum equations as well. A clamped external density
with uncounted support is only a source diagnostic, not a completed galaxy.

## 6. Finite, testable existence criteria

The prospective screen supplies one shared spectrum/state/scale choice,
DeltaU, ordinary source with support prescription, outer matching and metric
gauge. Unknowns are N, the spatial metric, soft y_j and hard I. No arbitrary
radial/vertical hard-density profile or per-mode chemical potential is fitted.

Follow the boundary-connected occupied branch. At fixed N, define scalar
F=h' B. Its derivative includes

    F_g=h''B+h'^2[sum_soft w_j b_j^2/(kappa delta_j^2+3u4 y_j^2)
                      +beta(B_R,h|I+B_R,I^2/e_R,II)],
    N F_N=-h' beta omega_R B_R,I/e_R,II.                (14)

The principal eigenvalues of the lapse constitutive map are

    lambda_trans=Kb-F/g,     lambda_long=Kb-F_g.        (15)

Both must be positive on the proposed elliptic branch; use their continuous
limits at g=0. A monotone fixed-I force is insufficient because the square
term in (14) is compulsory at phase equilibrium. Nonexistent phase roots,
e_II=0, constitutive folds, loss of ellipticity, large metric corrections or
unmatchable boundary flux are substantive outcomes, not solver tolerances
to relax. A different named state/completion could be tested afterward
without rewriting this one.

Positive principal coefficients do not prove uniqueness or remove ordinary
self-gravitational response. Around the occupied cosmic state N=1,g=0,

    delta(E+3Pi)=-J_static Phi,
    J_static=beta[omega_bar^2/e_R,II+3 I_bar omega_bar]>0,
    K0 Laplacian Phi+J_static Phi=ordinary source,        (16)

where K0 is the common zero-source limit of (15). For example a Dirichlet
domain has a homogeneous kernel when J_static/K0 equals an eigenvalue of
minus its Laplacian. This Helmholtz/Jeans feature precludes a generic
maximum-principle uniqueness claim, even though the principal part is
elliptic. It requires boundary-connected solution/existence checks rather
than fitting the domain to avoid an inconvenient response. The soft ground
modes have no occupied phase and do not add spurious omega^2/e_II terms to
J_static. Nonlinear action positivity and free-boundary conditions remain
part of the actual problem beyond this linear screen.

A successful first solve would report the separate hard energy/pressure,
soft and hard polarization, total metric constraints and conservation, and
boundary/approximation errors. Only then are rotation and lensing from that
same solution eligible for calibration/comparison. Existence does not prove
formation or stability, but this BVP removes the immediate ambiguity that
prevented the old galaxy and new cosmological calculations from constituting
one macroscopic test. No native microscopic derivation is added as a gate.
