# Common-action galaxy boundary and initial-state decision V001

2026-09-29. Analytical continuation of the declared finite-gap alpha-one
scalar candidate. No numerical science, new observational fit, new
preparation, remote operation or frozen-file edit.

## Decision

A cosmic action density fixes the hard abundance and one phase frequency,
but does not by itself select the accelerated, aligned static galaxy branch.
There is an exact alternative branch with a geodesic preferred clock and
ordinary GR coupled to the SAME barotropic network energy. The next honest
test can therefore be a constrained initial-state transfer test, with no
halo radius or new abundance. A static solve remains a useful existence
test if its outer state is declared; it is not automatically a prediction
of formation.

Network concentration is allowed and may be the desired result. The issue
is selecting and predicting it from one common state, not requiring the
network excitation to remain smooth.

## 1. What a static boundary can and cannot own

Use the already specified scalar hard action, soft static minima and full
stress in MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md. The occupied phase obeys

    N omega(I,h)=mu,                                      (1)

and the cosmological boundary supplies the same action and frequency at a
stated epoch. A rescaling of time changes N and mu together; it does not
provide freedom to change mu/N or the local density. At a finite boundary,
I_b, N_b and an angularly varying h_b cannot all be assigned independently.
For example, if mu and N_b are owned, I_b must solve (1) at the actual h_b.
It must not simply be set equal to the homogeneous I_bar as well.

The linearized static cosmic exterior illustrates a genuine selection
problem. On the convex occupied branch, with K0>0,

    K0 Laplacian Phi+J Phi=S_b,
    J=beta[omega_bar^2/e_II+3 I_bar omega_bar]>0.            (2)

For the formal constant-coefficient problem, put q_J^2=J/K0. The spherical
homogeneous solution sin(q_J r)/(q_J r) is regular at the center and tends
to zero at infinity. Consequently regularity and Phi->0 alone do not
select its amplitude. This is a mathematical ambiguity of those weak
boundary conditions, not proof that every properly matched BVP is
nonunique. That homogeneous solution is not a localized finite-norm
perturbation. A physical norm/flux condition, time-dependent matching or
a finite domain with specified outer data may eliminate it.

Equivalently the Fourier static inverse has a pole at |k|=q_J. A generic
localized baryonic source has nonzero power there, so demanding a localized
static response is itself substantive; it is not equivalent to choosing
one convenient outer Dirichlet wall. The flat static approximation also
cannot be extended literally beyond its local cosmological domain.

Thus increasing a numerical box is an important diagnostic, but its radius
must not become a hidden fitted halo radius. Record sensitivity to the
outer state, resonances and failed matching. Do not select the box giving
a better rotation curve. The full cosmological initial-value problem is
the physical means to select a response when static selection is ambiguous.

## 2. An exact local initial-state branch of the proposed action

This result uses the NEW full square-root hard phase action, not merely
the older quadratic alpha counterterm. Set

    a_mu=0,       y_soft=0,       v_soft=0.                 (3)

The scalar orbit energy is even in h, so e_h(I,0)=0 for every retained I.
All first variations of the acceleration/polarization sector then vanish.
The residual action is exactly

    S=integral sqrt(-g) [M2 R/2
          +C beta(I sqrt(-partial theta squared)-e_R(I,0))
          -C DeltaU] + S_ordinary.                       (4)

It is GR plus the same irrotational barotropic network fluid and the same
matched constant. No energy or mass-like background has disappeared.
The hard-fluid velocity need not coincide with the preferred clock: finite
fluid pressure can accelerate the former while the latter is geodesic.

Locally choose T as proper time along a hypersurface-orthogonal geodesic
normal congruence of a solution of (4). Then a_mu=0 supplies the preferred
clock until that congruence develops a caustic. Equations (3)-(4) are an
invariant local branch, not an assertion that arbitrary cosmological data
select it, or that its clock remains regular throughout collapse.

Its linear limit is the already derived alpha-one Q_k=0 branch:

    Q_k=a^2 Pcal=0,
    delta p=c_I^2 delta rho,
    c_I^2=I e_II/omega,

with ordinary barotropic-fluid metric equations. A geodesic-clock
realization has the scalar clock rate pi_dot=Phi and no acceleration
source. It is not the aligned static choice T=t in a nonconstant lapse.

This provides a decisive preparation distinction. Homogeneous zero-soft,
zero-polarization data plus ordinary gravity do NOT by themselves prove
formation of an accelerated static modified-force branch. That branch
needs a different admissible clock/state selection or a demonstrated
nonlinear transition. It must not be produced by resetting the clock,
relaxing modes or assigning an extra chemical potential during the solve.
Conversely, (4) can predict an ordinary gravitating concentration of network
energy. Such clustering is a possible result, not a failure by definition.

## 3. A concrete smallest executable initial-state test

The appropriate first transfer test does not require a mature-galaxy halo
boundary. Retain the same e_R(I,0), energy normalization and DeltaU; evolve
the alpha-one Q=0 metric/fluid equations from one declared cosmic slice.
The homogeneous solution is I(a)=I_1/a^3, with its actual e and pressure;
do not use exact dust+Lambda at epochs where its pressure is material.

A minimal complete scalar linear test uses normalized Fourier initial-data
basis columns for the ordinary baryon and hard-fluid density/velocity.
Metric lapse/curvature are obtained from the Einstein constraints, not
set independently to zero in a density-bearing column. Set the soft
coordinates and polarization charge to zero and reconstruct the geodesic
clock. The normalization denotes a transfer matrix, not a physical unit
density perturbation. Actual small amplitudes multiply it afterward.
It selects no radial hard profile and fits no per-galaxy abundance.

The full equations already exist in ALPHA_ONE_FLRW_ENTROPY_INTERFACE_V001.md
and the ordinary matter conservation equations. All prescribed k values
must use the adopted physical ruler and lie inside the local/averaging
window. An observed baryonic source profile may later supply a spatial
forcing or seed shape, but its present profile does not determine its
formation time, initial velocity or primordial amplitude. Those missing
history data must not be inferred from a favorable final rotation curve.

A cheap independent analytic oracle is available before such evolution.
For a frozen local background, negligible pressure relative to energy,
subhorizon wavelengths and times short enough to neglect expansion, use
mass-equivalent densities rho_b and rho_H and set

    Gamma_b=4 pi G rho_b,   Gamma_H=4 pi G rho_H,
    u_k=c_s^2 k^2,         c_s^2=c^2 c_I^2.

The closed ordinary-baryon plus network-fluid perturbations obey

    d2/dt2 [delta_b] = [Gamma_b, Gamma_H       ] [delta_b],
            [delta_H]   [Gamma_b, Gamma_H-u_k ] [delta_H]. (5)

Both species are evolved; there is no uncounted externally held baryonic
density or assembly work. The two squared rates are exactly

    lambda_+-=(Gamma_b+Gamma_H-u_k
       +-sqrt[(Gamma_b+Gamma_H-u_k)^2+4Gamma_b u_k])/2.     (6)

For nonzero pressure and Gamma_b>0, one is positive and one negative:
ordinary self-gravitational growth coexists with a restoring mode. At
k=0 they reduce to Gamma_b+Gamma_H and zero; at large k the growing
rate tends to Gamma_b while the hard perturbation is pressure-suppressed.
These are tests of the common fluid's transfer, not an anomalous-instability
pass/fail gate. The constant-background oracle must not be extrapolated
over a Hubble time; the actual FLRW test retains H, w and c_I^2 evolution.
There is no G/mu replacement in this geodesic Q=0 branch. Its pressure/Jeans
scale is not the q_J of the different aligned, polarized static branch in
(2); using that static K0 in (5) would mix the two state prescriptions.

For a separately labeled external-source diagnostic, fixing delta rho_b(t)
instead gives

    sigma_ddot+(c_s^2 k^2-Gamma_H)sigma
                                          =Gamma_H delta rho_b(t),
    sigma=delta rho_H.                                    (7)

Zero perturbations initially and a constant switched source have response
Gamma_H delta rho_b times (1-cos(omega t))/omega^2 for omega^2>0,
t^2/2 at zero, or (cosh(gamma t)-1)/gamma^2 for omega^2=-gamma^2.
Its general version is the corresponding causal convolution. This shows
why an undamped response does not automatically settle to a selected
static profile. Equation (7) requires an explicit external source/work
interpretation; (5) avoids that extra port and is the preferred closed
qualification. Neither constitutes a simulated galaxy in this note.

## 4. Does early coldness rule out useful galactic response?

No. It restricts intrinsic pressure support and can instead favor strong
concentration. For small changes on the intrinsic h=0 static branch,

    delta ln I=Psi/c_I^2,
    delta e/e=(1+w)Psi/c_I^2,
    Psi=ln(N_b/N)>0.                                      (8)

The expansion in (8) fails when the predicted contrast is not small; one
must solve the nonlinear phase condition, not extrapolate negative or
infinite densities. Early-cold same-action histories make present c_I^2
small, so a significant galactic potential can lie well outside this
linear smooth-response regime. That is a warning against discarding the
hard contribution, not a proof that a nonlinear concentration is unphysical.

The rigorous finite-amplitude condition is in the preceding smoothness
note. If a smoothness tolerance s and early pressure tolerance w_c at
inverse scale factor A are actually specified, let w(r_c)=w_c and
x=f(r_c)/A^3. Intrinsic smoothness requires

    Psi_eff <= (1/4)ln{[1+4(1+s)(x+x^2)]/[1+4(x+x^2)]},
    Psi_eff=Psi-Delta_src,
    Delta_src=ln[omega(I,h)/omega(I,0)]
               -ln[omega(I_b,h_b)/omega(I_b,0)].            (9)

Delta_src is computed from the SAME field/state branch, not adjusted. In
the hard small-action/source regime its leading contribution is
3(h^2-h_b^2)/(2R^4). Polarization anisotropy and div F still enter the full
gravitating source. Thus an early-cold bound on the zero-source fluid is
not an all-branch exclusion of the polarized BVP.

In the intrinsic fluid limit a useful timescale comparison is

    t_sound/t_dyn ~ sqrt(Psi/c_I^2),
    t_sound~L/(c sqrt(c_I^2)),  t_dyn~L/(c sqrt(Psi)).       (10)

It is a scale estimate, not a derived relaxation time or observational
threshold. If pressure communication is slow, a static solution cannot be
assumed accessible before infall. Streaming, caustics, shocks or retained
native amplitude-gradient/memory stress may become material. None is
silently inserted into (1); they are questions for the same-parent dynamic
test or a separately derived extension.

## 5. Owned inputs and the few genuinely new choices

- Already owned: exact scalar orbit/action/source functions, finite-gap
  energy/pressure/curvature, matched-baseline rule, the current static and
  alpha-one linear equations, and baryonic source products with fixed
  geometry/provenance. These are enough to implement the transfer oracle
  and, for a specified finite candidate, the constrained linear evolution.
- Already stored but not interchangeable: six actual pulse states use
  R={32,64,128}, Hp={1,4}, with full soft plus hard excitation. Their
  actions are usable without re-preparing them, but they are NOT the
  zero-soft scalar cosmological state postulated in the current BVP.
  Removing their soft energy or replacing their phases by an equilibrium
  ensemble is a new state prescription, not numerical postprocessing.
- The 72 completed shared-calibration branches are R->infinity limits.
  They are not already calibrated finite-R equilibria. A finite-R test
  must solve the same cosmic energy/vacuum matching at that R and preserve
  its pressure; this is shared calibration, not an extra local halo fit.
- New but explicit effective-model choices can be legitimate: the scalar
  square-root hard completion, its global finite gap/action calibration,
  a geodesic Q=0 initial branch or an alternative owned clock-charge
  branch, and an initial cosmic slice with density/velocity transfer basis.
  A mature-galaxy prediction additionally needs an ordinary source history
  or a verified stationary matching prescription. None is supplied by
  merely declaring the final hard density smooth or cold.

The minimal advance is therefore to test the common initial-state transfer
and its coupling to ordinary matter, while treating the aligned static
galaxy as an explicitly different branch until its selection is shown.
This neither adds arbitrary abundance nor postpones effective-model testing
until native microscopic parameters are derived.

## Source identities

- MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md:
  `64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3`.
- ALPHA_ONE_FLRW_ENTROPY_INTERFACE_V001.md:
  `48b6ba835fb84d30182bfb2233d17e49ad2b4cd2cb7e5f10def2ff934d94911e`.
- GALACTIC_SMOOTHNESS_AND_COLD_HISTORY_CONSTRAINT_V001.md:
  `5628b4615baf23ff173d898d7e436d25b47843b184d224e1ed52655c8512a902`.
- GLOBAL_GAP_LIMIT_CALIBRATION_V001_RESULTS.json (identity stated by its
  completed result report; no numerical payload re-audit here):
  `11e7c8e7d9119ef02177904e462e1959e5d554eed245000f8609530b5b64b628`.

All earlier evidence remains unchanged. No numerical producer ran.
