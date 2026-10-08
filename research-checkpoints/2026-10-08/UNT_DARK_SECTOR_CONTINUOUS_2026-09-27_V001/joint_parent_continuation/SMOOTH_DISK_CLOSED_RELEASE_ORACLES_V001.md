# Smooth-disk closed release: constrained initial state and exact oracles V001

2026-09-29. Analytical derivation and prospective first-unit protocol. No
scientific execution, changed old source, halo fit, or finite-age outcome.
This uses the same declared macroscopic alpha-one action on its geodesic,
zero-soft branch, not a native derivation of that effective action.

## 1. Why the razor-thin source is not a smooth global release

Near a positive razor-thin sheet the Newtonian potential is
phi=phi_0+g_sheet |z| to leading normal order. A mirror-symmetric geodesic
normal congruence initially at rest reaches z=0 from height |z0| after
sqrt(2|z0|/g_sheet). The infimum of these times is zero. Smooth initial
Hubble expansion changes higher terms, not this limiting conclusion.

Thus this PARTICULAR two-sided, initially resting geodesic clock cannot
be assumed smooth on a nonzero global time interval for the ideal sheet.
Hard-fluid pressure does not accelerate the independent geodesic preferred
clock. Off-sheet local oracles remain valid. This is not a theorem excluding
all clock data or a thin sheet as a stationary source diagnostic.

A global release therefore needs finite vertical source data or an openly
declared smooth synthetic family. It must not hide a smoothing width in the
mesh or infer a physical disk thickness from a favorable response.

## 2. A positive smooth source with the correct thin limit

Keep the existing synthetic M and a. Introduce b>0 and define, in physical
Euclidean coordinates used to prescribe the conformal seed,

    zeta=sqrt(z^2+b^2), A=a+zeta, d=sqrt(R^2+A^2),
    phi_N=-GM/d,
    D_b=(M b^2/(4pi))
             *[a R^2+(a+3zeta)(a+zeta)^2]/[zeta^3 d^5].   (1)

Direct differentiation gives Delta phi_N=4piG D_b. Every factor in D_b
is positive. The asymptotic flux gives total mass M; as b decreases to
zero, phi_N tends to the original Kuzmin potential away from the sheet
and D_b tends distributionally to its surface density. This is a source
family, not a numerical refinement parameter or a new dark profile.

Useful exact derivatives, in the orthonormal cylindrical basis, are

    phi_R=GM R/d^3, phi_z=GM A z/(zeta d^3),
    Hess(phi_N)=GM{d^(-3) diag[1,1,1+a b^2/zeta^3]
                                      -3 d^(-5) w w^T},
    w=(R,0,A z/zeta).                                     (2)

For 0<b<=a this gives the sharp global operator-norm bound

    ||Hess(phi_N)|| <= L_N=GM/[b(a+b)^2],                   (3)

attained by the vertical curvature at the origin. The positive-eigenvalue
bound is GM(1+a/b)/(a+b)^3; the negative-eigenvalue magnitude is at most
2GM/(a+b)^3. This derives (3), not an empirical tidal scale.

## 3. An exactly constrained initial state, with no inserted lapse

The cheapest first closed seed is initially NONROTATING and at rest relative
to the cosmic normal. It is not a supported disk equilibrium: ordinary
matter is released and evolves. Adding rotation later requires its momentum
constraint, rather than using a prescribed force or holding the source fixed.

Use c=1 in this section. On the initial slice choose

    gamma_ij=psi^4 delta_ij, K_ij=-H gamma_ij,
    preferred T=t, N=1, shift=0 for the subsequent synchronous gauge,
    hard I=I_bar (physical scalar), theta_i=0,
    soft y_j=v_j=0.

The ordinary seed's specified quantity D_b in (1) is its conserved rest mass
per coordinate volume. Its actual proper rest density is D_b/psi^6. Hence
the seed rest mass is exactly integral D_b d^3x=M; its physical profile is
not asserted to equal the Euclidean formula after metric reconstruction.
Cosmic ordinary matter and the hard state are homogeneous in proper density
initially. Their actual background pressure and matched DeltaU fix H,Hdot.

All initial momentum vanishes, so the momentum constraint is EXACTLY zero.
The Hamiltonian constraint, after using the same flat-FLRW background
equation and retaining the matched vacuum there, is exactly

    -Delta psi=2piG D_b/psi,        psi->1 at infinity.      (4)

This is not the old aligned-static material equation. No independently
chosen potential is inserted into the clock. Let

    u=-phi_N/2, U=sup u=GM/[2(a+b)].

The positive Green operator rewrites (4) as
psi=1+G_Newton[2piG D_b/psi]. For U<1 its map on the interval
1<=psi<=1+u is a contraction in sup norm, of Lipschitz constant at most U.
It therefore supplies a unique global positive solution and the explicit
bounds

    1+u/(1+U) <= psi <=1+u,
    ||psi-(1+u)||_infinity <=U^2.                          (5)

The physical SI compactness is U=GM/[2c_light^2(a+b)]. Restoring units in
(4) replaces G D_b by G D_b/c_light^2. Formula (5) is an exact constraint
certificate, not merely the first weak-field iterate. The simple iterate
psi_1=1+u has an explicitly known residual proportional to
D_b[1-1/(1+u)]; it must not be called an exact solution.
With extrinsic curvature defined using a unit normal and length-valued
proper time, the SI initial value is K_ij=-(H/c_light)gamma_ij. The
homogeneous ordinary density/pressure and hard density/pressure have not
been dropped: their background constraint fixes H together with DeltaU.

This smooth, initially comoving seed is chosen instead of global circular
motion for the first unit. At large radius it follows the cosmological
normal; it does not prescribe a superluminal peculiar velocity -H R to
hold an infinite tail at fixed physical radius. Initial peculiar velocities
and the free gravitational transverse-traceless data are exactly zero in
this first declared state. It is a new prospective initial preparation,
not inferred from the previous pulse or static-clamp outputs.

## 4. Where the hard response first appears

Let tau be proper time from the slice and I_bar(t) the SAME homogeneous
solution. Define q=I/I_bar(t)-1. More generally for constrained CMC data
with initial hard I uniform and theta_i=0, put

    A_focus=sigma_ij sigma^ij+4piG delta(rho+S),             (6)

where rho and S are total normal energy and spatial stress trace, excluding
the constant vacuum when taking their difference from the same background.
Equivalently the vacuum cancels only between the two Raychaudhuri equations;
it remains in H,Hdot and the initial metric.

Normal Raychaudhuri and current conservation give the exact initial jets

    q(0)=q_dot(0)=0, q_ddot(0)=A_focus,
    q=.5 A_focus tau^2+O(tau^3).                          (7)

Initially the hard-fluid acceleration relative to the geodesic normal is
zero: its pressure gradient vanishes. The trace K=-3H also makes I_dot
uniform. Consequently phase and pressure-driven current enter later:

    theta_i=(e_II I_bar/6) partial_i A_focus tau^3+O(tau^4),
    v_H^i=-(c_I^2/6) D^i A_focus tau^3+O(tau^4),
    P=P0+(P0 c_I^2/24) Delta_gamma A_focus tau^4+O(tau^5),
    P=sqrt(gamma) I Gamma, P0=sqrt(gamma_0) I_bar.          (8)

All coefficients are evaluated on the initial slice. The spatial metric
variation in the last line is already included by using the canonical
coordinate density P. Time variation of gamma,e_II,I_bar changes higher
orders, not these coefficients. In SI, the velocity coefficient uses
c_s^2=c_light^2 c_I^2 and A_focus has units time^(-2).
Equivalently, for energy-density/stress inputs in SI,
A_focus=sigma_time^2+4piG delta(rho_energy+S_energy)/c_light^2;
sigma_time is the expansion shear measured per second.

For the nonrotating construction (4), sigma=0 and the proper seed is
pressureless. Thus, exactly,

    A_focus=4piG D_b/psi^6,
    4piG D_b/(1+u)^6 <= A_focus <=4piG D_b.                (9)

Equation (9), with SI mass density, bounds the actual initial density
growth without solving an orbit or a galaxy evolution. At this order
delta rho_H/rho_H,bar=(1+w_bar)q and delta p_H=c_I^2 delta rho_H.
The network energy is retained; it is not assigned an extra density profile.

An exact current-coefficient identity follows from (4):

    Delta_gamma A_focus=4piG psi^(-10)
      *[Delta D_b-10 grad(ln psi).grad D_b
         +30 D_b |grad ln psi|^2+12piG D_b^2/psi^2].        (10)

The final G in the square bracket becomes G/c_light^2 in SI. An approximate
psi or finite-difference evaluation of (10) must carry its own derivative
error; the sup-norm bracket (5) alone is not a derivative certificate.

These are local Taylor COEFFICIENTS. They do not bound a finite-tau solution
without a remainder/evolution check. In particular, the vanishing initial
relative current does not imply vanishing density response: geodesic volume
focusing already changes the proper density at order tau^2.

## 5. Tidal and caustic controls, with their distinct domains

The exact initial normal tidal matrix for (4) is

    E_ij=R^(3)_ij+[2H^2-4piG(rho-p_bar)-Lambda]gamma_ij,
    E_ij-E_background gamma_ij
                                  =R^(3)_ij-4piG rho_seed gamma_ij. (11)

Its trace difference is A_focus. The exact conformal Ricci tensor provides
an independent derivative oracle. At leading weak field (11) reduces to
Hess(phi_N), whose trace and anisotropic parts are separately known in (2).
This establishes the Newtonian tidal interpretation without choosing a
Newtonian lapse as physical clock data.

For comparison, off a truly source-free region of a static Newtonian
potential, an initially resting cold congruence with zero initial shear has

    delta I/I=(tau^4/12) Tr[Hess(phi_N)^2]+O(tau^5).       (12)

It follows from sigma_ij=-tau phi_,ij+... and Raychaudhuri. A point-mass
potential gives (GM)^2 tau^4/(2r^6). This is a separate local vacuum,
negligible-expansion oracle, not the tau^2 formula in a nonzero smooth
seed density and not a claimed late-time halo. Source evolution and cosmic
terms must be retained when its premises fail.

A sufficient caustic-free bound is available without assuming equilibration.
For the Jacobi matrix along the actual clock congruence, suppose the tidal
operator norm is bounded by L on the whole proposed interval and initial
expansion/shear norm is at most B0. Then

    ||Jacobi(tau)-1|| <= cosh(sqrt(L) tau)-1
                           +(B0/sqrt(L))sinh(sqrt(L) tau). (13)

If the right side is less than one, its smallest singular value is positive.
For B0=0 it suffices tau<arcosh(2)/sqrt(L). In the CMC state B0=|H|.
This is a bound on the actual interval tidal field, not permission to use
its initial value throughout a changing closed system. A future release
must bound/check L along its computed interval.

In the SEPARATE frozen Newtonian-source oracle, L=L_N in (3) is global.
The central vertical geodesic Jacobi mode is exactly cos(sqrt(L_N)tau)
for initially resting normals and reaches zero at pi/(2sqrt(L_N)). Its
scale tends to zero as b->0. Neither frozen-source time is a predicted
caustic time of the closed evolving baryons. They give independent method
controls and explain the nonuniform thin-sheet limit.

## 6. Prospective smallest implementation unit

Preserve the already declared a=3.2 kpc, GM=gstar a^2 and the current
spectrum-1/reference-0 finite calibrations R={128,8192}. Declare both
b/a={1/8,1/16} now, retaining all four combinations; no thickness is chosen
from a rotation or release outcome. Thicknesses are two synthetic source
alternatives, NOT numerical convergence copies or measurements.

The first producer can be an arithmetic/constraint-oracle unit rather than
a galaxy-age integrator. Its complete fixed witness census is
R_coordinate/a={0,1/2,1,2}, z/a={0,1/4,1/2,1} for all four combinations.
Read the actual saved I_bar,e_bar,p_bar,e_II,gstar,Kb and DeltaU with their
ancestry. Output all source densities, potential/gradient/Hessian/trace,
U, psi brackets, A_focus bounds, the same-state density/pressure conversion,
and the frozen-source tidal scale. Zero-component comparisons use a fixed
nonzero source scale, not division by a vanishing value.

Independent elementary controls are the source Laplacian, positive density,
total-mass asymptotic flux, central vertical curvature, and a fourth-order
finite-difference check at h/a=2^(-10),2^(-11), including even Cartesian
extensions through the axis. Prospective relative/contribution-scaled
arithmetic tolerance is 2e-11 and finite-difference tolerance 1e-6. All
finite-difference discrepancies are retained. No orbit or BBN calculation
is needed for these inherited states and analytical geometry readouts.

This first readout certifies bounds on a uniquely defined exact initial
constraint solution; it does not claim to have numerically reconstructed
psi or evolved a finite interval. Before reporting an ACTUAL finite-time
release, implement (4)'s positive Green iteration or an equivalent
asymptotically matched constraint solve, qualify its derivatives, then evolve
the synchronous ADM, hard-current/phase and ordinary dust equations together.
Use (7)-(11) as independent initial-jet tests and (13) as the clock-regularity
screen. The ordinary seed is never clamped after its initial preparation.

The exact Green iteration has contraction factor U; no empirical damping
parameter or galaxy radius is required. A finite computational interface
must approximate this asymptotic solution/current with quantified error,
not replace it by an adjustable wall. Scalar-clock or dust caustics end the
qualified smooth unit; adding kinetic dispersion or shock physics would
require a separately owned state/extension. The first unit is therefore
small, closed and falsifiable without pretending to have produced a mature
galaxy or selected its cosmological history.

## Sources and peer algebra

- `PHYSICAL_GALAXY_EXTERIOR_AND_INITIAL_VALUE_V001.md`, SHA256
  `7cbe96fb731d5675e2420237178e64981adc3f89f9020bce73b510aea3851dd8`.
- `MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md`, SHA256
  `64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3`.
- `COMMON_ACTION_GALAXY_BOUNDARY_AND_INITIAL_STATE_V001.md`, SHA256
  `2eb30bb54416d31a69109b1d48795789a208b2418bfb237cfd81a291ec006c26`.

The CMC Raychaudhuri, phase-gradient and current coefficients (7)-(8) were
independently checked by the results-audit agent before this note was saved.
No science producer or software import was used for these derivations.
