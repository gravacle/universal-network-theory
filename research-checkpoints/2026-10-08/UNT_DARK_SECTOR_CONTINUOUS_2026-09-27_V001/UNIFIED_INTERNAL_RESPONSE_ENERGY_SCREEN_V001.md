# One internal network response: a joint energy and stability screen

2026-09-27. Construct ID: `UNIFIED_INTERNAL_RESPONSE_ENERGY_SCREEN_V001`.
Conditional analytical extension of primary A/M; no newly adopted UNT
mechanics, physical density map, extra dark species, numerical run or fitted
cosmological function. The question is whether ONE microscopic response
can supply both the matter-like energy and the accelerating stress.

## 1. Explicit interface and what is not yet earned

Read completely after resident flag checks:

- `I0_ALLOCATION_COVARIANT_PERTURBATION_SCREEN_V001.md`, SHA256
  `7883730dea0d6908d740a86afe5d5d14e89d2d7c996b99d9d1611ae54928e6a6`.
- `CONSERVED_RECORD_STRESS_SCREEN_V001.md`, SHA256
  `7e4fbb948014c00e0144b980273317749ea574cacd1640fd2ab1a47c957ccc2a`.

Adopt for this screen one common metric of signature (-+++), c=1, a
transported conserved current n u^mu with n>0, and one retained internal
coordinate chi. Let epsilon(n,chi) be the complete local rest-energy
density, twice continuously differentiable on the tested branch. Chi is
an independent metric scalar during source variation; identifying it with
a metric-dependent network observable would require the corresponding
extra variation. The local closure neglects retained gradient, kinetic,
entropy and nonlocal stresses only in its declared regime.

Neither the current nor n is automatically native record occupation per
graph label, and chi is not automatically a q4 covariance, degree or clock.
A same-parent operational map is required. There are no independently
postulated DM/DE fluids in the algebra below: the A/M names refer to a
decomposition of ONE total stress, if the physical interface is earned.

## 2. Relaxing one stable internal coordinate softens the density response

Suppose a local stationary branch exists with

    epsilon_chi(n,chi_*(n)) = 0,
    D := epsilon_chichi(n,chi_*(n)) > 0,
    mu := epsilon_n(n,chi_*(n)) > 0.                         (1)

D>0 means stability against changing chi at fixed n, not stability against
joint density/internal perturbations or proof that evolution prepares this
branch. Implicit differentiation and the envelope rule give

    dchi_*/dn = -epsilon_nchi/D,
    epsilon_eff(n) := epsilon(n,chi_*(n)),
    epsilon_eff' = mu,
    epsilon_eff'' = epsilon_nn - epsilon_nchi^2/D.            (2)

All partial derivatives in these equations are evaluated before eliminating
chi, at fixed value of the other coordinate. The negative term is the exact
relaxation correction, not a separately inserted attractive interaction.

The conditional current action supplies

    rho = epsilon_eff,       p = n mu - epsilon_eff,
    rho_A = rho+p = n mu,    rho_M = -p = epsilon_eff-n mu,
    c_s^2 = dp/drho = n(epsilon_nn-epsilon_nchi^2/D)/mu.       (3)

This sound response concerns inhomogeneous perturbations which actually
remain on the local adiabatic branch. It is not a general sound speed for
the uneliminated system. The static joint quadratic form can be written

    delta^2 epsilon =
      D[delta chi+(epsilon_nchi/D)delta n]^2
      +(epsilon_nn-epsilon_nchi^2/D)(delta n)^2.              (4)

Here delta^2 epsilon denotes the Hessian quadratic form; the energy expansion
contains one half of it. Thus absence of negative relaxed compressibility
requires the exact same-parent condition

    epsilon_nn >= epsilon_nchi^2/epsilon_chichi.              (5)

Equality gives zero linear sound response at that point. Equality on an
open connected density interval makes epsilon_eff affine there, recovering
the previous cold-density screen; equality at one point does not control
other densities or nonlinear perturbations. A claimed common-cone bound
would additionally require n(epsilon_nn-epsilon_nchi^2/D)/mu <= 1.

The constructive route is explicit: a microscopic density stiffness can
balance the softening due to the same internal response. Native degree or
interaction curvature could contribute only after its relation to physical
density and total energy is derived. Coupling-parameter curvature is not
automatically epsilon_nn, and an independently fitted positive term would
not establish the requested unified mechanism.

## 3. The simplest shared mass/background ansatz has a sharp cost

As a restricted candidate, not an adopted UNT law, take

    epsilon(n,chi) = n m(chi) + V(chi),       m(chi)>0.        (6)

Both functions must ultimately come from one complete network energy; merely
giving two arbitrary fitted functions the same argument is not a derivation.
On a branch obeying (1),

    n m' + V' = 0,       D = n m''+V'' > 0,
    mu = m,             p = -V,
    rho_A = n m,        rho_M = V,
    c_s^2 = -n[m'(chi)]^2/[m(chi)(n m''+V'')] <= 0.          (7)

Primes on m,V are derivatives with respect to chi, not n. Any nonzero m'
therefore makes the strictly local, fully relaxed density response negative.
Increasing n lowers the relaxed insertion energy, dmu/dn = -m'^2/D. In the
conditional fluid momentum equation,

    a^mu = -c_s^2 D^mu ln n
         = [m'^2/(m D)] D^mu n,                             (8)

where D^mu is the rest-frame spatial derivative. This favors motion toward
higher density in this local approximation. It is not a derived Newtonian
force, long-range potential, universal record-pair attraction or rotation
curve. The same mass-response coupling which supplies this attraction also
fixes the negative compressibility; the two cannot be adjusted independently.

Ignoring chi gradients/kinetic energy on this branch, its homogeneous
background term has vacuum-form stress -V g_munu. It need not be constant:
V is evaluated at chi_*(n), and energy transfers internally as n changes.
For example dV/dn = n m'^2/D, fixed by the same response, not a new exchange
function. A claim of positive maintenance density also requires V>=0.

Only under the additionally adopted homogeneous, isotropic FLRW
Einstein/perfect-fluid interface is the accelerating-sign test

    rho+3p = 3n mu-2epsilon_eff < 0,
    or, for (6),                 n m - 2V < 0.              (9)

For this component alone that is the acceleration condition; with other
sources their complete rho+3p must be included. The gravity premise is the
standard one described by [Trodden and Carroll, section 2.2](https://ned.ipac.caltech.edu/level5/Sept03/Trodden/Trodden2_2.html),
not a new microscopic UNT derivation. No second cosmological constant may
be added while also counting the same background energy in V.

The local ansatz therefore exposes a joint requirement, not a joint success:
positive accelerating stress can coexist with an attractive response, but
the latter has negative adiabatic density curvature unless m'=0 or the
ansatz is extended by owned density stiffness/dynamics. At m'=0 the local
relaxation-induced attraction vanishes at that point; it does not follow
that all higher responses or other interactions vanish.

## 4. Why the sign is a diagnostic, not a universal rejection

Where the reduced hydrodynamic approximation is valid, c_s^2<0 gives a
growing local density mode instead of a stable acoustic mode. It does not
by itself determine the allowed wavelength band, growth time, cosmological
damping, nonlinear endpoint, or observational acceptability. A retained chi
with kinetic and gradient terms has its own propagation and relaxation
times; finite-wavelength or nonadiabatic perturbations need not follow
chi_*(n). Positive D alone supplies no relaxation time without that dynamical
normalization. Eliminating chi and then extending the negative sound speed
to arbitrary frequencies/wavelengths would be inconsistent.

This distinction is established in the coupled-fluid literature, not newly
discovered here. [Bean, Flanagan and Trodden (2008), sections III–IV](https://arxiv.org/html/0709.1128v2)
derive the local adiabatic instability and separately examine its regime,
scale dependence and Jeans interpretation; weak coupling, nonadiabaticity
and kinetic effects matter. Those sections were inspected for this scope
check. Their dark-sector models are an analogy, not adopted UNT contents.

Consequently a proposed network response can remain constructive if its
owned finite-range/finite-rate dynamics yields acceptable clustering rather
than uncontrolled growth. It must derive that dynamics and test its actual
domain and rate; renaming every growing mode “dark matter” is not enough.
Conversely it is unjustified to reject every attractive retained response
merely because its strictly static local limit has negative curvature.

## 5. One shared-energy reciprocity test, and the missing microscopic inputs

Let X_chi := -epsilon_chi be the internal generalized force density, and
write mu(n,chi) = epsilon_n before restricting it to the stationary branch.
A single differentiable energy requires the off-branch reciprocity

    partial_chi mu = epsilon_nchi = -partial_n X_chi.         (10)

Thus the change of complete insertion energy under an internal displacement
must equal minus the change of the restoring force under a density change.
Near (1), the measured stiffness D and this SAME mixed derivative must
reproduce both dchi_*/dn and the relaxed density curvature in (2).
Equivalently, if an explicitly declared source enters as -J chi,

    partial_J chi_* = 1/D,
    partial_J mu_* = epsilon_nchi/D = -partial_n chi_*        (11)

at fixed J for the last density derivative, and at fixed n for the source
derivatives. These are falsifiable reciprocal response identities, not a
license to identify unrelated graph measurements with the needed controls.
A mismatch rejects this two-variable local-energy closure; it may indicate
missing retained variables, irreversible history, or an incorrect source map.

The smallest constructive next test is to obtain, from ONE fixed native
energy and state/control prescription, epsilon, mu, epsilon_nn,
epsilon_nchi and D on the same physical-density branch. Independently check
(10), then the relaxation correction (2), and use that very branch in both
(7)/(9) and its perturbation dynamics. This requires the physical current,
volume/deformation and clock map, the meaning and preparation of chi, and
its kinetic/gradient response if the static approximation is insufficient.
It does not require positing separate dark species to do the test.

Absolute energy remains load-bearing: epsilon -> epsilon+C leaves all
displayed derivative/reciprocity tests unchanged but shifts rho by C,
p by -C and rho+3p by -2C. The complete matched volume/reference term must
therefore be owned once; these density/internal-coordinate response data
alone do not predict the accelerating background normalization. Actual
metric/volume stress responses could detect that constant. Conservation
fixes n's evolution given its initial
value, not its abundance. Neither that initial population, a matter/vacuum
ratio, nor a common observational fit has been derived here.
