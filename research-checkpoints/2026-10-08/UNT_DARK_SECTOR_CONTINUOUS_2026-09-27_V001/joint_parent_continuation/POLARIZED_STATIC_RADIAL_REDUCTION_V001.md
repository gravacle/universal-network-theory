# A two-equation static problem with phase equilibrium and polarization retained

2026-09-29. New analytical reduction of the already adopted averaged radial
scalar parent. No new population, fitted radius/gap, numerical producer,
formation history, or change to sealed evidence. A full-read independent
review of the preceding support/history note is saved separately.

## Result

The nonlinear stationary problem does not require an independently fitted
halo density or a new radial PDE. On a specified boundary-connected phase
branch it reduces to **two radial first-order equations and local algebraic
inversions**. The same source fixes its intrinsic pressure, polarization,
metric and lensing. The inverse response is not generally the fixed-action
response: phase equilibrium changes the action when the source changes.

This gives a tractable conditional annulus problem immediately. A regular
center of the averaged scalar stress is also describable, but a smooth
microscopic vector center and transport from the isotropic cosmological
ensemble are separate requirements, not silently supplied by radial alignment.

## 1. Definitions, with no discarded absolute energy

Use c=1, areal radius r, N>0, s=sqrt(f)>0,

    ds^2=-N^2 dt^2+dr^2/s^2+r^2 dOmega^2,
    a=s N'/N,    C=1/(4 pi G Kb),
    h(a)=a/sqrt(1+a^2/gs^2).

The radial scalar source a and h are signed. In particular a vacuum-dominated
static patch need not have attractive a>0. For each occupied scalar orbit,
retain the old per-mode energy e_j(I,h) and impose the sufficient phase branch

    omega_j=e_j,I,       N omega_j=mu_j,
    theta_j=mu_j t+constant_j.                            (1)

The mu_j are derived from one supplied boundary state, not independently
fitted at each radius. Keep a boundary-connected root with e_j,II nonzero;
positive e_j,II is the stable hardening branch of interest. Nonexistence,
folds and negative-curvature branches must remain explicit outcomes.

Define, with the unchanged weights and matched DeltaU,

    E=sum w_j e_j,    Pi=sum w_j(I_j omega_j-e_j),
    B=sum w_j b_j<y_j>,  b_j=kappa delta_j,
    F(N,a)=h'(a)B,       D(N,a)=Kb*a-F(N,a).             (2)

An explicitly unoccupied I=0 copy may instead remain on its relaxed minimum
and contribute e_min(h), Pi=-e_min and its polarization. It has no occupied
phase angle to which (1) can be applied. Do not generate a new population by
silently clipping a failed occupied root or assigning it a chemical phase.

The full mode stress is exactly the already derived one:

    rho=C[E+DeltaU+aF+s(F'+2F/r)],
    pr=C[Pi-DeltaU-aF],        pt=C[Pi-DeltaU].           (3)

Add ordinary matter rho_b,p_b if present. Below it is either absent, or an
isotropic static supported component with p_b'=-(rho_b+p_b)N'/N. A supplied
baryon density without its supporting stress/current is not automatically
such a component. An anisotropic ordinary source requires its own stress
and conservation equation rather than replacing p_b by a guessed pressure.

## 2. Exact first-order reduction

The radial Einstein equation gives an algebraic positive metric branch:

    s^2+2r*a*s=1+8 pi G r^2 p_b
                   +2r^2[Pi-DeltaU-aF]/Kb,

    s=-r*a+sqrt(1+r^2*a^2+8 pi G r^2 p_b
                   +2r^2[Pi-DeltaU-aF]/Kb).             (4)

The discriminant and s>0 are domain conditions, not guaranteed by the
positive local oscillator potential. The alternative quadratic root is not
silently selected at a failed boundary continuation.

For a static metric, the lapse equation is
Laplace_spatial(N)/N=4 pi G(rho_total+pr_total+2pt_total).
Its left side is s(a'+2a/r)+a^2. In (3) the explicit aF terms cancel from
rho+pr+2pt, leaving E+3Pi-2DeltaU+s(F'+2F/r). Therefore

    N'=N*a/s,
    (r^2 D)'=r^2/s *
       [4 pi G Kb(rho_b+3p_b)+E+3Pi-2DeltaU-Kb*a^2].     (5)

One may evolve (N,mathcalD), mathcalD=r^2D. At each radius solve
D(N,a)=mathcalD/r^2, then (1) for the retained actions, and use (4) for s.
There is no independently supplied mass-density profile for the modes.
The mass function is reconstructed as m=r(1-s^2)/(2G).

Equations (4)-(5), static stress conservation and the chosen ordinary-matter
conservation give the same Einstein mass equation m'=4 pi r^2 rho_total.
That equation, and not just the constitutive residual, is an independent
implementation check. The local circular speed and finite-boundary lensing
then follow from the SAME N,s in STATIONARY_LENSING_CLOSURE_V001.md.

The leading weak-field form is div[D(N,grad ln N)] equal to the same active
source, retaining E+3Pi-2DeltaU and any ordinary stress. Neither the signed
polarization contribution nor the absolute excitation energy is renamed or
discarded. Dropping a^2 and setting s=1 requires weak-field control; the
exact reduction (5) need not make those approximations.

## 3. Which response must be invertible?

At fixed N the phase condition holds omega fixed, rather than I fixed.
For B_j=b_j<y_j>=-e_j,h, differentiation gives

    I_j,a=h'(a) B_j,I/e_j,II,
    I_j,N=-omega_j/(N e_j,II),

    F_a|N = h'' B+h'^2 sum w_j
                [B_j,h|I+(B_j,I)^2/e_j,II],
    N F_N|a = -h' sum w_j omega_j B_j,I/e_j,II.         (6)

An unoccupied relaxed branch contributes its direct minimum-energy
derivatives instead. The extra squared term is nonnegative on a positive
e_II branch. Thus even a well-behaved fixed-action force curve does not by
itself establish an invertible phase-equilibrium curve. This is a measurable
local derivative of the same orbit energy, not an extra adjustable term.

The radial constitutive Jacobian is

    Kcal=partial_a D|N=Kb-F_a|N.                        (7)

Where Kcal is nonzero, implicit inversion and the two ODEs are locally
well-defined; Kcal>0 is the relevant static monotone branch. Kcal=0 is a
constitutive fold/degeneracy to report. Do not jump to a different algebraic
root to improve a galaxy curve. Existence of this static branch is not its
dynamical clock stability, which remains a separate retained constraint.

At a=0, parity makes B=B_j,I=0 and h'=1,h''=0. Hence

    Kcal_c=Kb-sum w_j B_j,h(I_c,0).                    (8)

The previously proved scalar fixed-action susceptibility is below the
relaxed value for every positive excitation. Thus an excited positive-weight
scalar component produces a positive contribution to (8); relaxed copies
have their usual exact contact cancellation. This statement uses the
occupied zero-source scalar orbit, not an assumed vector susceptibility.

## 4. Center regularity and its microscopic qualification

For finite N_c, ordinary central stress and invertible occupied roots, let

    S_c=4 pi G Kb(rho_bc+3p_bc)+E_c+3Pi_c-2DeltaU.

If Kcal_c is nonzero, the regular averaged-stress expansion is

    a=a1*r+O(r^3),        a1=S_c/(3 Kcal_c),
    mathcalD=S_c*r^3/3+O(r^5),
    N=N_c[1+a1*r^2/2+O(r^4)],
    s=1+[-a1+4 pi G p_bc+(Pi_c-DeltaU)/Kb]r^2+O(r^4).  (9)

Substituting these coefficients in the reconstructed mass equation agrees
with rho_c including the finite polarization density 3C F_a,c*a1.
This is a useful exact normalization check for a future radial integration.
If Kcal_c=0, (9) cannot be used: the next source powers and regularity must
be analyzed without dividing by a fictitious susceptibility floor.

A genuinely excited strictly radial microscopic vector y_j=q_j e_r is not
continuous at the origin unless q_j tends to zero. A regular averaged scalar
stress alone does not make that individual vector smooth. A smooth isotropic
orientation ensemble can have nonzero central energy, but its finite-source
transverse/angular response must be transported; it is not automatically
the scalar function e(I,h). The qualified isotropic-vector infinitesimal
response can supply a local central linear response under its selected
periodic-orbit conditions, not an entire nonlinear scalar profile.

Consequently (5) is directly a conditional radial ANNULUS problem, with owned
inner data, and also a regular-center MEAN-FIELD scalar diagnostic if that
averaging closure is expressly adopted. A smooth full vector-center problem
needs that additional existing state-transport question resolved. This is
not an assertion that all regular network-supported centers are impossible.

## 5. Boundary data and independent input count

Fix the shared spectrum/weights and potential, gstar, S=gs/gstar, and the
actual boundary-action vector from a named common history at a stated epoch.
The matched DeltaU is a function of those same choices, not another input.
An inferred hard gap, beta, template normalization, preparation/phase rule
or matching prescription is a counted global model/state choice. The
physical time scale tau_star controls averaging and dynamical admissibility;
it cancels from the static frequency ratios when the dimensionless actions
and common scale are consistently retained.

For the simplest baryon-free, regular averaged-stress boundary test, specify
one finite outer radius r_b and the nonzero vector I_b. Normalize N_b=1
(coordinate gauge, not an extra physical parameter). If its source a_b is
not separately imposed, it is one unknown scalar and

    mu_j=omega_j(I_b,j,h(a_b))                           (10)

for occupied copies. A two-parameter shooting description uses the unknown
N_c and a_b, imposes regular mathcalD(0)=0, and requires N(r_b)=1 and the
integrated a(r_b)=a_b. Thus the many mu_j are outputs of the ONE supplied
boundary-state vector and a_b, not independent per-mode halo fits. A
solution, its multiplicity or nonexistence remains an actual result.

This count does not provide r_b from cosmology. It is a finite static
interface specification; matching a moving FLRW exterior without a shell
also needs its metric/extrinsic-curvature and stress conditions. A static
reservoir/cavity is a permissible declared internal test but not proof of
that cosmological matching. If an exterior mass or a_b is supplied
independently, it adds a matching condition; do not silently satisfy it by
introducing an uncounted central or outer action amplitude.

With ordinary static matter add its actual supported source prescription.
For a barotropic perfect fluid, the EOS and one boundary enthalpy determine
p_b(N),rho_b(N); this is not a new arbitrary function of radius. An annulus
instead has owned N and mass/source-flux data at its inner boundary; a
hidden interior mass must not be inferred from the desired outer speed.

## 6. Smallest executable test, without choosing a new halo

First use a complete already retained state family and its existing
zero-source orbit quantities. For every occupied mode calculate the
center Jacobian (8), E,Pi and

    J_static=sum w_j[omega_j^2/e_j,II+3I_j omega_j].      (11)

At zero source the equilibrium variation is
delta I_j=-omega_j*delta ln N/e_j,II, so
delta(E+3Pi)=-J_static*delta ln N. In a locally frozen, consistently
background-subtracted weak-field patch this gives the scalar static
operator Kcal*Laplacian(delta ln N)+J_static*delta ln N, plus the owned
ordinary source. Its squared static response wave number J_static/Kcal
is a useful local diagnostic, NOT a dynamical instability proof or a halo
radius. Background gradients/curvature, source variation and the actual
boundary cannot be discarded in a global interpretation. Zero-action copies
held on their minimum have no action-repopulation contribution to (11).

These derivatives and the exact center coefficients can be checked without
a new source trajectory, empirical radius, galaxy fit or action distribution.
They expose directly how including polarization changes the isolated
pressure-length estimate. Next, on a prospectively specified annulus or
owned mean-field matching surface, integrate only (5), retaining the same
finite-field orbit function and checking (1), (4), the mass equation and
the full stress conservation. Existing fixed-action orbit kernels supply
energy, frequency and polarization; e_II and mixed derivatives must be
qualified before using the algebraic inversion. No independent radial
population function is needed.

Finite-gap phase hardening permits a density to respond to a lower lapse;
the harmonic obstruction concerns STATIC occupied support on this phase
branch. It does not forbid dynamic infall. Conversely a dust-like averaged
background does not guarantee a static halo: this two-equation problem,
the vector/phase transport and the independent compensated-clock evolution
give concrete ways to test that assertion within the retained parent.

## Source identities

* `FINITE_GAP_STATIC_SUPPORT_AND_EARLY_HISTORY_V001.md`:
  `a72f1e6c0a4fbd2ebabd38a9ac1d3fe91e2aebcd92144c5d8e51487547a32439`.
* `SHARED_MODE_INFERENCE_AND_STATIC_CLOSURE_V001.md`:
  `48dbfeeefc012af2f4d663e1ec37732f9e007efcbbe8fd66bfaced64a4a9a07b`.
* `STATIONARY_LENSING_CLOSURE_V001.md`:
  `3bc694411ba8a71708cc8222589f7486863a8588856897d77f93c11aeadf055c`.
