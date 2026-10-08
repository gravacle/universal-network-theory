# Closed release to lensing, and the first collision boundary

2026-09-29. Analytical continuation and prospective implementation design.
No producer, new fit, halo profile, numerical evolution or sealed-file edit.
The subject is the explicitly adopted macroscopic alpha-one scalar action,
not a claim to have derived that action from BS or to have selected a cosmic
origin. Only a finite initial slice is required.

## Decision

The smallest useful next spatial unit is a **short, closed release of the
already constrained smooth ordinary seed**, with the same cosmic hard state,
an evolved exterior/current and a same-metric null readout. It is not another
static wall calculation. It can measure actual focusing, matter transport and
the onset of a lensing excess, or identify a caustic before the proposed
observable. A merger simulation is premature until this unit transports its
state without a reset.

There are two new discriminators available before a long calculation:

* The initial hard projected-density increment has a fixed cosmic-enthalpy
  coefficient, equation (8), rather than a halo normalization. Its conversion
  into lensing must be checked in the same metric.
* In the dust limit initially comoving ordinary and hard material retain
  their density ratio along the common flow, equation (9). Coldness does
  not supply the missing multiple velocities at a collision.

Neither discriminator rules out concentration from a different, explicitly
owned prior state. They constrain this actual uniform-hard-action release.

## 1. Exact equations and inherited initial data

On the geodesic preferred-clock branch a_mu=0, the zero soft coordinates and
velocities are invariant, and e_R,h(I,0)=0. The residual action is Einstein
gravity plus the SAME hard scalar current, ordinary material and matched
vacuum. In c=1 units define

    Q=sqrt(-partial theta squared)=omega(I),
    U_mu=-partial_mu theta/omega,
    rho_H=C beta e(I), p_H=C beta[I omega-e],
    W_H=rho_H+p_H=C beta I omega,
    c_I^2=I e_II/omega,    0<c_I^2<1/3 for I>0.           (1)

The exact closed matter equations are

    nabla_mu(I U^mu)=0,
    U^nu nabla_nu U_mu=-(delta_mu^nu+U_mu U^nu)
                                            partial_nu ln omega,
    G_mu,nu=8piG[T_H+T_ordinary-C DeltaU g]_mu,nu.        (2)

The hard phase remains irrotational. Ordinary baryons have their own
conserved mass/current and stress; the first seed uses pressureless rest
matter, not a density held fixed by an uncounted support force. Homogeneous
ordinary species and the hard pressure determine H,Hdot with DeltaU.
Vacuum is subtracted only in comparisons to that same background.
Ordinary radiation starts in the declared background state but generally
develops perturbations in the released metric. Exact evolution requires
its owned transport/stress equations; holding that radiation homogeneous
is an additional weak approximation whose stress/metric error must be bounded.

Use precisely the two old smooth thicknesses b/a=1/8,1/16, a=3.2 kpc and
GM=gstar*a^2. The positive density D_b, total coordinate rest mass M,
conformal initial metric and CMC extrinsic curvature are those in
SMOOTH_DISK_CLOSED_RELEASE_ORACLES_V001:

    gamma_ij=psi^4 delta_ij, K_ij=-H gamma_ij,
    -Delta psi=2piG D_b/psi, psi->1,
    I=I_bar, theta_i=0, ordinary peculiar velocity=0.     (3)

Here the excess ordinary proper mass density is D_b/psi^6. The already
proved positive Green contraction gives a unique initial constraint solution
for U=GM/[2c^2(a+b)]<1, with controlled first-iterate and derivative errors.
The initial constraints are not a prescription for the later lapse.

Evolve the metric in a hyperbolic coordinate gauge, for example generalized
harmonic gauge, and evolve the physical preferred clock independently by

    g^mu,nu T_mu T_nu=-1,
    T_dot=shift^i T_i+N sqrt(1+gamma^ij T_i T_j).          (4)

This maintains a_mu=0 while the clock is smooth. It avoids mistaking the
weak hyperbolicity of a naive synchronous ADM implementation for a physical
instability. The hard phase and preferred clock are different fields.
Their velocities need not coincide once pressure gradients develop.

The prior exact canonical kernel remains available: P=sqrt(gamma) I Gamma,
Gamma=sqrt(1+gamma^ij theta_i theta_j/omega^2),
theta_dot=shift.grad theta+N omega Gamma and
P_dot=partial_i[shift^i P+N sqrt(gamma) I gamma^ij theta_j/omega].
Its algebraic density inversion is monotone because
d(I Gamma)/dI=Gamma(1-v^2 c_I^2)>0. No new inertia, K(Q), viscosity or
quasistatic mu table is introduced.

## 2. Finite-time regularity and the precise cold limit

For a finite positive state interval I_min<=I<=I_max, the rest-frame
principal matter system is

    delta I_dot+I div delta v=0,
    delta v_dot+(e_II/omega) grad delta I=0.

Its positive quadratic energy is
(C beta/2)[e_II(delta I)^2+I omega|delta v|^2]; its sound cone is c_I.
Together with a hyperbolic Einstein gauge this supplies the expected local
classical Cauchy structure. Smooth positive initial density avoids a hard
vacuum/free-boundary problem. This is not a proof of a common existence time
for every very cold state or of stability over a galaxy age. The standard
Einstein--Euler local-existence literature concerns specified equations of
state and data classes; it is not being applied as an unexamined theorem for
our entire asymptotically FLRW census. A primary example of that framework is
[Brauer and Karp](https://arxiv.org/abs/0810.5045).

Report separately: loss of timelike hard phase, unbounded material gradients,
ordinary-dust crossing, and preferred-clock caustics. A regular coordinate
gauge cannot repair a caustic of the PHYSICAL clock T. Conversely a coordinate
singularity alone does not prove material failure.

The exact pressure acceleration in (2) is -c_I^2 projected grad ln I.
The saved Xi=c_s^2/(gstar*a) is its initial source-scale comparison, not a
uniform-in-time estimate. Compression changes c_I and density gradients.
It is legitimate to use a dust solution as a controlled numerical reference
only while the integrated pressure force AND the coupled metric correction
are bounded. Small initial Xi alone does not justify discarding pressure
near a caustic.

The all-inferred map already retains 1340 state labels. Its finite joint-band
Xi values are 4.83462e-10 to1.11951e-7, with sound/dynamical ratios2988.72 to
45479.82. These saved facts motivate the cold control; they do not select a
final age or prove collisionless dark matter. The exact adopted current is
testable in physical time without an additional microscopic oscillator gate.
Derivation of that current by averaging native oscillators is a separate
claim with an unresolved physical clock conversion.

## 3. A finite-time compression bound that can be checked during evolution

For the exact dust control the hard fluid and preferred geodesic clock share
their initially normal velocity. Let J be the physical geodesic separation
matrix and Z=(a_i/a(t))J, so Z_i=1,Z_dot_i=0 for the CMC seed. In a parallel
transported frame, with delta E the actual normal tidal matrix minus its
FLRW value,

    Z_ddot+2H Z_dot=-delta E Z.                           (5)

If H>=0 and ||delta E||<=L throughout the proposed interval, the positive
Volterra kernel gives

    ||Z-1||<=B(t):=cosh(sqrt(L)(t-ti))-1.

When B<1, det Z>0 and the exact dust action ratio obeys

    I/I_bar=1/det Z <=[1-B(t)]^-3.                       (6)

This is an actual interval statement conditional on the ACTUAL interval
tidal bound. It must not substitute the already known initial L_N for an
uncomputed evolving supremum. It supplies a useful sufficient regularity and
finite-compression check, not the true first-caustic time. Finite-pressure
material has its own flow Jacobian and pressure acceleration; (6) must not
be silently applied to it. Its exact current and Gamma provide the direct
compression readout instead.

Equation (6) bounds the possible local hard overdensity by
rho_H,bar([1-B]^-3-1) on the dust branch. A volume-integrated bound must use
the actual proper volume/worldtube and include its flux. This distinguishes
ordinary smooth focusing from importing an arbitrarily massive halo into a
small chamber. It makes no claim about an infinite background-subtracted
particle number in a chosen coordinate chart.

## 4. The first projected-density increment has no free halo coefficient

The exact initial coefficient from the constrained seed is

    delta rho_H,mass=(1/2)W_H,mass A_focus (t-ti)^2+O(dt^3),
    A_focus=4piG D_b/psi^6,
    W_H,mass=rho_H,mass+p_H/c^2.                         (7)

In the leading local weak-field projection psi=1+O(U), integrate through
the smooth seed. The hard surface-density coefficient is

    delta Sigma_H=2piG W_H,mass dt^2 Sigma_b+...,
    delta Sigma_H/Sigma_b
         =(3/4)Omega_H(1+w_H)(H dt)^2+....               (8)

Here Omega_H=8piG rho_H,mass/(3H_actual^2) and H=H_actual at the same
epoch. Saved Hcal-normalized density coefficients must be converted before
using this form; the first expression in (8) is normalization-independent.
The dots include the bounded initial metric correction and higher TIME
orders. Equation (8) is a coefficient identity, not a finite-time prediction
without a remainder or evolution check. It assumes the same local-epoch
background and a projection of the actual density perturbation. The
ordinary profile also moves; its later potential is not held at the initial
value. Pressure-driven hard velocity first appears at order dt^3 and
canonical-density transport at order dt^4, as previously proved.

This is a density jet on the declared normal/CMC slicing, not automatically
a Weyl curvature, deflection or shear increment. Pressure, evolving extrinsic
curvature, slicing transformations and photon flight-time terms may affect
that conversion. A cold weak slow-lens reduction can TEST the corresponding
Born projection only after controlling those terms, with a/c much smaller
than the elapsed/modulation time, small metric potentials and velocities,
and actual finite source/observer geometry. The potentially useful window
a/c << dt << t_dyn=sqrt(a/gstar) is not a fitted formation age or a proof of
an instantaneous lensing enhancement.

For general readout, integrate null geodesics and the screen Jacobi matrix
in the SAME evolved metric, with initial observer tetrad and source plane.
The optical tidal tensor is defined with trace R_mu,nu k^mu k^nu and enters
D_AB''=-Ropt_AC D_CB. Compare its angular/distance map to the SAME FLRW
observer/source configuration. This retains both scalar potentials, vector
terms, anisotropic material motion and cosmological boundaries; no separate
lensing halo or unverified Phi=Psi is needed. A weak implementation may
instead use integral grad_perp(Phi+Psi)dl along the background ray only after
quantifying the omitted metric/retardation terms.

The null readout assumes the adopted metric light-propagation prescription;
it is not a new native identification of a carrier with a physical photon.
The useful eventual observed target is jointly the finite-source shear/
deflection and the ordinary dynamical mass/current distribution. This first
synthetic release predicts their relation, not a fit to an observed cluster
or a mature galaxy. Equation (8) alone does not permit an order-one prompt
projected-density enhancement merely by assigning the material a cold sound speed.

## 5. A strong collision/memory oracle

In the exact dust limit, suppose ordinary and hard dust share the initial
velocity and there are no non-gravitational ordinary forces. Their common
geodesic flow persists until a crossing. Separate current conservation gives

    U.grad(rho_H/rho_b)=0                               (9)

where rho_b>0; equivalently each material parcel preserves its two initial
mass labels. For the present preparation that ratio is spatially nonuniform
because the hard initial density is homogeneous and the ordinary seed is
not. It is not reset to a universal cosmic ratio inside a forming object.
Equation (9) is an exact matched-flow control, not a theorem that all spatial
hard and baryonic density peaks coincide for every initial state.

For finite R the force -c_I^2 projected grad ln I changes this relation in
a calculable way. At a stream crossing, one local pair (I,grad theta) cannot
represent two distinct momenta. The limit c_I->0 removes pressure; it does
not turn the scalar into a collisionless phase-space distribution. Continuing
through a crossing as freely interpenetrating dark streams requires an owned
multistream/kinetic or dispersive completion. Shock selection/dissipation
also cannot be added silently to this conservative scalar action.

A merger test must therefore start from complete released states (metric,
ordinary distribution, I,theta,T and currents), not two fitted hard-density
profiles. Ordinary stars may be modeled kinetically only with their declared
distribution; gas collision/thermal physics is another owned ordinary sector.
Translation/boost/gluing of two snapshots requires solving the momentum and
Hamiltonian constraints and fixing their relative phase/current. If the
single-phase domain ends before the lensing epoch, that is the precise
missing continuation, not a successful collisionless-merger prediction.

## 6. Smallest prospective implementation and exterior

1. **One initial-constraint unit.** Numerically reconstruct (3) with the
   existing positive Green contraction, including the analytic seed tail.
   Check both constraints, derivative bounds and the actual proper seed
   mass. The original four release examples remain method controls; they
   are not relabeled newly viable joint states. A physical finite-state
   comparison uses its authenticated inferred state and its full background.
2. **Axisymmetric release.** Evolve the exact canonical hard kernel, ordinary
   mass/momentum and the metric, with the independent clock (4). Proposed
   initial outputs are dt/t_dyn={0,1/64,1/32,1/16}, frozen before any result.
   A prospective regularity failure is retained, not evaded by selecting an
   earlier favorable end state. Use32^2 then64^2 interior cells with explicit
   midplane/axis parity and refinement of the smaller fixed thickness.
3. **Exterior, not a clamp.** Match to the retarded linear FLRW perturbation
   system of the SAME finite-R current, with the actual initial1/r metric
   tail and initial hard/ordinary data. An evolved radial-multipole outer
   buffer is one low-memory realization. Match induced geometry, constraints
   and normal current; do not prescribe independent I=I_bar and zero flux.
   Interface radii8a and16a are numerical overlap tests, not halo radii.
   Retain higher multipoles and extend the buffer until the resulting ray/
   current error is qualified. Failure of linear overlap is reported rather
   than repaired by a wall. Non-incoming radiation data concern characteristic
   fields and do not erase the initial Coulomb/constraint tail.
4. **Independent controls.** Homogeneous FLRW; all existing initial density,
   pressure-current and tidal jets; equations (5)-(9); current flux through
   each fixed worldtube; metric-constraint propagation; and zero-source
   material inversion. A spherical dust+Lambda LTB subcase can provide an
   exact open-exterior evolution/null-ray oracle, but is only a method
   control and never a replacement for the axisymmetric source.
5. **Same-state rays.** Report the full signed lensing increment and its
   component accounting at every fixed time, with observer/source endpoints
   and interface/refinement errors. Retain actual evolving baryons when
   attributing a hard contribution. Do not compare to an externally held
   baryonic potential and call the difference a physical halo.

The exact equations define the reference. A cheaper constrained weak-field
solver is eligible only if it bounds/records the omitted Einstein residual,
stress-induced slip, vector contribution and time/retardation terms at the
readout's precision; it is not licensed by naming it quasistatic. Small U
and H*a/c help, but do not bound matter gradients or later velocities.

Storage is O(number of cells), not a material mode per cell: this invariant
branch has no soft arrays and uses scalar EoS evaluations. Tens of metric,
matter and clock arrays on64^2 cells occupy a few MB before working buffers.
Matrix-free spatial operators or blocked ring kernels avoid a dense64^4
Green/Jacobian allocation. Rays and an outer multipole buffer can be streamed.
An explicit relativistic update also pays the light-CFL cost: for interior
spacing dx and endpoint t_dyn/16, the step count is at least of order
c*t_dyn/(16*dx), not merely one matter-crossing step per cell. Constraint
iterations, outer buffers and accuracy can increase it. A low-memory design
therefore does not by itself establish a cheap runtime.
Runtime is not inferred from an unexecuted design: size one32^2 unit, retain
all controls, then decide the qualified queue. No arbitrary job deadline,
empirical time, physical wall or new fit is introduced.

This step yields an actual finite-time, open-exterior observable or a precise
regularity/closure failure. It does not assume that an initially uniform
cosmic population is already a galaxy halo, that static necessity results
exclude its dynamic branch, or that low-pressure scalar matter automatically
survives an observed merger.

## Resident custody

- MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md:
  `64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3`.
- PHYSICAL_GALAXY_EXTERIOR_AND_INITIAL_VALUE_V001.md:
  `7cbe96fb731d5675e2420237178e64981adc3f89f9020bce73b510aea3851dd8`.
- SMOOTH_DISK_CLOSED_RELEASE_ORACLES_V001.md:
  `5f5f2985167b47751aeceb78b823fb327aa58074b58e18a6d8856cd32bc7f7aa`.
- INFERRED_RELEASE_STATE_MAP_V001_RESULTS.json:
  `46179beab779ff242d1c72a6f694ae2f27c93394264f1bbbc820e47b507f2962`.
- SHARED_STATIC_RADIATION_NECESSITY_V001.md and the stationary-lensing,
  smooth-current-bound and all-state result reviews were read in full.

The exterior and scalar-stream distinction was independently challenged by
the native-scope lane; the audit lane independently checked the density-jet
coefficient, the interval Volterra/singular-value bound, current inversion
and dust-label conservation. It required the explicit separation from
observable lensing and the actual-H density normalization.
No external observational data or source implementation was imported.
