# Frontier V015: cold allocation, collective response and the scalar route

2026-09-27. New analytical results and completed independent checks. No
numerical physics, production retry, remote dispatch, parameter adoption,
package/infrastructure change or publication. The preceding user-facing
status response was not itself a new scientific milestone; this continuation
has completed the explicit derivations below. The full dark-sector goal
remains active and incomplete, not blocked or replaced by these narrower tests.

## 1. Primary A/M result: allocation also determines a force

Construct `AM_LOCAL_DENSITY_COLD_SCREEN_V001` is a conditional test of the
primary active/maintenance proposal, not a newly adopted microscopic rule.
Assume the already available common-metric interface and a closed pair with
complete assigned stresses

    T_A = rho_A u u,       T_M = -rho_M g,       rho_A > 0.

Conservation independently fixes BOTH the energy and momentum exchange:

    dot rho_A + theta rho_A = Q = -dot rho_M,
    rho_A a_mu = D_mu rho_M.

Here D is the spatial derivative in the active component's rest frame,
theta is its expansion, and a_mu is its proper acceleration. Geodesic motion
does not mean absence of gravitational clustering. These relations expose a
test missing from a homogeneous allocation or density-ratio calculation:
spatial changes in a vacuum-form maintenance energy exert a force.

For the additional local, isentropic, conserved-record-current hypothesis
with total energy density epsilon(n), the same variational stress requires

    rho_A = n epsilon',       rho_M = epsilon - n epsilon',
    c_s^2 = n epsilon'' / epsilon',
    a_mu = -c_s^2 D_mu ln n,  Q = -theta c_s^2 rho_A.

These are conditional consequences of a physical current/action, not a map
from fixed native register labels to a continuum current. No such map has
been silently supplied. The established covariant framework is checked
against [Wands, De-Santiago and Wang (2012)](https://arxiv.org/html/1203.6776);
our result applies it to the A/M acceptance question rather than claiming a
new general fluid principle.

### A decisive fixed-share screen

Let f = rho_A/epsilon be the ENERGY fraction, with 0 < f < 1. Then

    dot f = -theta f [(1-f) + c_s^2].

A constant nontrivial share throughout an expanding density interval
therefore forces c_s^2 = -(1-f) < 0. Equivalently epsilon = C n^f.
It fails the short-wavelength barotropic gradient-stability condition in
the domain where this assumed hydrodynamic description holds. No observed
abundance was used. This is not a rejection of a fixed OPERATION fraction
unless an independently derived transduction map makes it this energy
fraction, nor of nonadiabatic/history-dependent alternatives.

Exactly cold, geodesic inhomogeneous response throughout an open density
interval instead forces

    epsilon(n) = m n + Lambda,       m > 0,
    rho_A = m n,                    rho_M = Lambda,       Q = 0.

This is a constructive compatible form, not a derivation of m, Lambda or
their abundance. A single background point or homogeneous trajectory does
not prove this interval result. Approximate coldness is allowed and is now
quantified: if 0 <= c_s^2 <= sigma on n_- <= n <= n_+, then

    0 <= rho_M(n_-) - rho_M(n_+)
       <= sigma/(1+sigma) [rho_A(n_+) - rho_A(n_-)].

The bound concerns an absolute change, not a fractional-vacuum guarantee.
No empirical sigma is inserted. Full proof and acceptance scope are in
[the primary perturbation screen](I0_ALLOCATION_COVARIANT_PERTURBATION_SCREEN_V001.md).

## 2. A history-dependent escape is possible, but has a precise condition

Do not turn the density-only result into a universal no-go. A geodesic
interacting pair may have a time-dependent vacuum if D_mu rho_M = 0.
However the transfer one-form must be exact:

    d rho_M = Q u,       d(Q u) = 0.

Its projections require Q omega_mu_nu = 0 and D_mu Q + Q a_mu = 0.
On a regular geodesic patch with Q nonzero this gives zero vorticity and
D_mu Q = 0. A freely selected local Q(rho_A) generally does not satisfy
this in an inhomogeneous medium. A background Q(t) is not enough.

The independently checked comparison
`AM_GEODESIC_CLOCK_COMPARISON_V001` supplies an explicit constrained
proper-time action. Its complete stress is dust plus -V(tau)g, and its field
equation supplies Q = -V'(tau). This is a known effective construction,
not an adopted UNT law; see the [primary constrained-field treatment](https://arxiv.org/html/1403.3961v2#S2).
Its potential, physical clock and initial dust abundance remain unowned
inputs. An arbitrary V(tau) cannot be counted as a network prediction.

A further exact test closes a tempting shortcut. If one also requires a
conserved record current and rho_A = m(tau)n with the same per-record energy
on every proper-time slice, then n m'(tau) = -V'(tau). Admitted spatial
variations in n force m' = V' = 0 on that slice. Nontrivial exchange needs
actual formation, flow-line-dependent internal energy/history, or additional
stress dynamics; changing only a count equation leaves an energy residual.

The [independent review](GEODESIC_ACTIVE_MAINTENANCE_PERTURBATION_REVIEW_V001.md)
derives these statements, the explicit counterexample and the gauge/caustic
limits. Rest-frame sound speed must not be confused with a background
dot p / dot rho in a nonadiabatic completion.

## 3. Native energy and response: positive results, with their scaling limit

Three supporting native results completed since V014 remain separate from
the continuum A/M construct:

- [Nonempty-degree energy](NATIVE_NONEMPTY_DEGREE_RECORD_COST_V001.md):
  exact parameter intervals allow record occupation to raise the preferred
  degree while keeping complete leading record excess positive. At the
  inherited other coefficients, the prospective d_* interval (9/4,5/2)
  changes preferred degree 1 to 2 and has mu = 5 - 2d_* > 0. No point was
  selected, no existing coefficient changed, and no geometric phase or
  preparation claimed. Other intervals have zero or negative bulk excess.
- [Prepared-link transport](NATIVE_PREPARED_GRAPH_PERSISTENCE_AND_TRANSFER_V001.md):
  under native h_N = Omega/N, local prepared incidence can persist while a
  carrier crosses a prepared matched link with order-one probability. The
  full-model readout differs from the fixed-graph comparison by an explicit
  O(1/N) fixed-time bound, with all native flips retained. A disconnected
  matching is not a macroscopic geometry or a preparation theorem.
- [Source-response scaling](NATIVE_SOURCE_RESPONSE_SCALING_V001.md):
  removing only one record's feedback from the SAME initial state changes
  an admissible bounded hold readout by at most O(N^-1/2) for bounded expected
  source degree, or O(1/N) for a prepared source star. For r prepared sources
  the bound is O(r/N). Extensive r escapes this bound's forced suppression,
  but does not prove a collective response. Differently prepared histories,
  growing observation times and readouts outside the commutator premises
  are not excluded. Exact inter-occupation dephasing also leaves the stated
  hold readouts unchanged; within-sector graph/carrier correlations remain.

Thus persistent transport and single-source feedback are different questions.
Neither the finite effect nor its larger numerical replay supplies a gravity
law by itself. N is native layer width, not remote L6 or physical volume.

## 4. Gravitational-action route: a scale is not automatically cold matter

The existing adopted gravity endpoint already supplies metric variation,
vacuum-form stress and a conditional common-metric shell calculation. What
is missing is its physical spectral/matching input and same-parent A/M map,
not the mere existence of a continuum interface.

We tested an explicitly additional completion: a retained physical scalar
controls the crossover kappa; fixed shell shape, massless signed spectrum,
no pre/matching terms or extra Jordan kinetic/potential terms. On a regular
positive-stiffness patch, F = 2 C_R and V = -C_0 obey

    V = beta F^2,
    beta = (4 pi)^2/(4 hbar) (A_0/A_1^2) (1+x^2)/(1-x^2).

Here x = mu/kappa, and A_0 and A_1 are the complete convention-matched
signed shell sums. Set hbar = c = 1 for the following frame relations.
The canonical Einstein-frame potential is constant, U = M^4 beta. The
scalar is massless, not a cold oscillating mode. The homogeneous source-free
kinetic component has w = 1; matter exchange changes its dilution, and
frame-dependent fluid labels cannot be equated. Varying a physical scalar
is distinct from keeping an external cutoff fixed. Extra derivative terms
from the actual parent cannot be omitted without justification.

The [scalar screen](SCALE_ONLY_RETAINED_SCALAR_DARK_SCREEN_V001.md) and
[independent review](SCALE_ONLY_INDUCED_ACTION_REVIEW_V001.md) also require
the on-shell curvature ratio |A_0/A_1|(1+x^2)/x^2 to be small before using
this derivative expansion. Changing the absolute cutoff cannot repair that
ratio or change beta. No observed vacuum magnitude has been predicted.

The constructive extension test is B = V/F^2, y = ln(F/M^2), with
B > 0, B_y = 0 and B_yy > 0. Under the stated kinetic convention,
m_scalar^2/H_vac^2 = 2 B_yy/B at the vacuum. This is a necessary screen for
a single-field vacuum-plus-cold-oscillation proposal, not a new requirement
that the whole UNT program use one scalar for both effects.

A [new exact threshold test](SINGLE_MASS_THRESHOLD_SCALAR_SCREEN_V001.md)
closes one minimal proposed repair: one physically fixed mass makes B
strictly monotonic, not minimized. The result also holds for a sharp shell
with fixed masses and exactly aligned nonnegative spectral weights in F
and V. Different signed/relative weights, owned matching terms and actual
state-dependent spectra remain outside that theorem; none is supplied by
simply selecting a desired potential.

## 5. What is now required, and what has not passed

The next primary calculation must use an actual network-defined current,
internal state and complete work/stress law. If it claims a local density
closure, its epsilon and exchange must meet the force/coldness tests above.
If history is essential, it must supply that history variable's equations
and exchange integrability; adding a free time function is not progress
toward the requested predictive explanation.

The native affine *count* energy 2N m_0 + D mu is not yet the affine physical
energy-density law m n + Lambda: node count is not a volume variation,
the conditional ground state is not a formation rule, and fixed register
occupations are not yet a transported physical current. This is the precise
bridge to pursue, not grounds to claim the compatible form already derived.

The full joint-plan requirements remain: primary allocation/formation,
physical source map, same-rule normalized abundances, valid perturbations,
and the declared expansion, early-universe, clustering/lensing/merger and
other applicable observational tests. No A0/A2/B0 or observational pass is
claimed. The single-scalar candidate's failure does not reject the distinct
record-matter plus network-background route. The last verified other-Mac
state remains the reported numerical stop; no live remote handle was
available here and no resumed calculation is inferred from pasted authority.

## Review and evidence boundary

Root read the new proofs and reviews in full, checked the pressure/exchange
signs, fixed-share derivative, coldness bound, exact-form integrability,
constrained-clock action, Weyl/trace factors and single-/aligned-mass
monotonicity independently. Three same-family agents supplied independent
algebra and scope challenges; shared assumptions remain, and agreement is
not empirical confirmation. Primary literature was used for the explicitly
labelled continuum mathematical interfaces, not as evidence that UNT earns
them. No packages or numerical tests were needed for these proofs.

The revised joint plan V002 was read in full. The original user-path V001
and several old notes were compressed,dataless; they were not hydrated.
Resident recovered index-only construction/accounting documents were read
as historical conditional designs, not replayed numerical evidence. No
historical source or failed attempt was rewritten.
