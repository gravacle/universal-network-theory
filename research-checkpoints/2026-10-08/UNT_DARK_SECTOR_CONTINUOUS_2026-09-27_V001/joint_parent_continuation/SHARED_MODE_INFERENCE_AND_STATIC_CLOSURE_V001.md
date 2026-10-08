# Shared inference is possible; the same state must pass a joint pressure test

2026-09-29. Additive analytical result for the explicitly adopted covariant
mechanical-mode parent. No fit, new trajectory, galaxy-field rescaling, source
change, or claim of a native BS-to-metric derivation.

## Result

It is legitimate to test this effective candidate using a small set of SHARED
parameters before deriving every physical constant from native UNT. Two new
reductions make that proposal substantive:

1. The overall spectral normalization cancels against the already matched
   gravitational contact. It cannot independently tune a cosmological abundance.
2. An outer state fixes a sufficient stationary closure
   `N omega_j(I_j,h)=constant_j`. Actions inside a spherical system can then be
   solved, rather than fitted independently at each radius.

There is also a decisive pre-fit constraint. In this fixed positive quartic
parent, a large homogeneous phase-averaged excitation density has an unavoidable
pressure floor. Neither an arbitrary action distribution nor the inertia can
make that density arbitrarily cold. A joint inference must satisfy this bound,
not merely add a free abundance to an otherwise unchanged galaxy law.

This note reads the full `EXPLICIT_MODE_COSMOLOGY_PATHWAY.md`,
`COSMOLOGY_CLOSURE_TEST_V001.md`, `FIXED_ACTION_MODE_INTERFACE_V001.md`, and
`COUPLED_SPHERICAL_RESPONSE_PATHWAY_V001.md`. Those adopted action and matching
premises remain in force; the new state ansatz below is explicitly additional.

## 1. Count the independent parameters before calibrating them

Use c=1, M²=(8 pi G)^-1, constant positive inertia m, and

    nu(delta)=A delta,  epsilon Lambda <= delta <= Lambda,
    Kb=A kappa Lambda²(1-epsilon²)/2,   C=2M²/Kb,
    h(a)=a/sqrt(1+a²/gs²).

The same per-mode energy is

    e=m v²/2+kappa delta² y²/2+u4(y²)²/4-kappa delta h.y.

Define the dimensionless variables and three scales

    s=delta/Lambda,                  y*=Lambda sqrt(kappa/u4),
    g*=Lambda² sqrt(kappa/u4),       tau*=sqrt(m/kappa)/Lambda,
    S=gs/g*,                        Y=y/y*,  tbar=t/tau*,
    E*=kappa² Lambda^4/u4=kappa g*², I*=E* tau*.

Then, on the locally nonexpanding clamped branch,

    Y''+s²Y+|Y|²Y=s H(G),
    G=a/g*,   H(G)=G/sqrt(1+(G/S)²).                       (1)

Expansion, clock and metric terms follow from the original action; they are
not discarded in a coupled calculation. The exact collective stress scale is

    C A Lambda² E* = 4M²g*²/(1-epsilon²) =: Kstress.       (2)

Thus A cancels completely when its simultaneous change in Kb and C is retained.
At fixed spectral shape, the independent dynamical scales are g*, tau*, S,
plus epsilon if the cutoff is to be inferred rather than fixed. A separately
adjustable A in the cosmological density would contradict this contact matching.

For the zero-cutoff RELAXED deep continuum, a0=8g*/(3pi). At a fixed positive
cutoff that formula labels the inherited continuum scale, not a strict
zero-field quadratic asymptote. The finite-band response itself must be used.
In SI acceleration units the geometric g* appearing in (2) is g*_SI/c²;
proper-time scale tau*_SI equals tau*/c. One must not put acceleration in m/s²
directly into a c=1 stress formula.

Let ebar_s(j,H) be the dimensionless orbit energy, j=I/I*, and let
Q(S)=-integral_epsilon^1 s ebar_min,s(S) ds. The OLD high-field matching gives

    rho_vac=Kstress Q(S),   Lambda_eff=rho_vac/M².          (3)

No extra vacuum offset is added. If one is later inferred, it is an additional
parameter and the corresponding force-to-vacuum prediction has been surrendered.
Changing inertia changes tau* but not the relaxed curve or (3).

## 2. A concrete shared state family, not a per-radius population

One minimal, explicitly conditional initial-state proposal is:

- Fix epsilon=.001 and the existing 128-node spectral quadrature.
- Fix the returned-action SHAPE to row 6 of
  `PREPARED_ACTION_RETURN_V001_RESULTS.json`: gap .001, mode order 128,
  dt .005, ramp duration 8, original external amplitude .0025. Its
  `mode_data.action` is the dimensionless vector j*_j. The corresponding
  gaps/weights are case 2 of `COMMON_HISTORY_MECHANISM_V001_RESULTS.json`.
- At one declared cosmological reference slice ai, put
  `j_j(ai)=zeta j*_j`, with ONE nonnegative global parameter zeta.
- Adopt uniform orbital phases at zero source and an isotropic distribution
  of fixed polarization directions. Replace each original spectral weight
  by normalized phase/orientation copies with the SAME total weight. This is
  an explicit ensemble/coarse-graining premise, not a discovered native
  degeneracy. Evolve every copy with the same unaveraged action; do not
  repeatedly randomize phases, change weights, or reset to a minimum.
- Fix the initial clock rule and ordinary baryon/radiation/metric initial
  data independently of later rotation residuals. The clock is then evolved
  with its constraints, not forced to be stationary.

This defines a four-global-parameter candidate `(g*,S,tau*,zeta)` after the
cutoff, reference epoch, template and ensemble rule are fixed. The epoch is a
state-reference convention, not a predicted formation time. An inferred epoch,
template parameter, cutoff or clock-state parameter must be counted as such.
An ensemble of vectors is not replaced by the scalar radial equation under a
changing source direction; the latter is a restricted exact subspace only.

The template's recorded return energy is 8.778693373929561e-7 and pressure
5.354691617904655e-10 in its original internal units. Its complete result-file
SHA-256 is `b8a0efd517e9492aa2546f83eb7cc81bb3a5553e22ff847f5c6f736b545b9678`,
payload SHA-256 `05ff139b16a2949d4b903261c037c6d48125cfcf6656ccc915ce854c27f42788`.
This identifies the template, not a new numerical run or a cosmic production
claim. Choosing zeta different from one or replacing the original coherent
phases defines a NEW state family; it does not rewrite the saved state.

Merely pairing a velocity with its negative cancels an initial Bdot but is
weaker than uniform orbital phase and does not establish subsequent equilibrium.
Uniform phases at h=0 have zero mean B and Bdot while retaining positive energy.
They do not automatically stay locally phase-isotropic under a changing field.

In the controlled fast-mode FLRW limit the SAME actions give

    j_j(a)=zeta j*_j (ai/a)^3,
    rho_exc=Kstress sum_j wbar_j ebar_j(j_j,0),
    p_exc=Kstress sum_j wbar_j[j_j omega_bar_j-ebar_j],
    3M²(H_FRW²+K/a²)=rho_b+rho_r+rho_vac+rho_exc.           (4)

Here the dimensionless weights approximate s ds. For modes not fast compared
with expansion, solve the original homogeneous vector equations instead of
using (4). The background does not give tau* merely by being fitted in the
adiabatic regime; tau* primarily controls response and averaging validity.
In a quadratic regime only the product zeta ai³ appears in the conserved
action normalization. These are identifiability facts, not extra free controls.

Crucially, zeta represents real positive excitation energy. If it is calibrated
to supply cosmological matter-like stress, that stress cannot simultaneously be
described as absent, nor can the initial energy be produced from the parent's
exact homogeneous zero state. Initial-state inference is legitimate without
claiming a formation derivation; a claimed formation history must debit its
source by the actual work. This is a network-energy explanation to test, not
an elimination of energy by renaming it.

## 3. Exact distribution-independent pressure floor

At zero source, for any rapidly averaged bounded scalar or vector orbit in the
positive quadratic-plus-quartic potential, the virial identity gives

    E=2V2+3P,    P=V4,
    V2=sum wbar s²<|Y|²>/2,
    V4=sum wbar <|Y|^4>/4.

Jensen and weighted Cauchy-Schwarz imply, without specifying the actions,

    V2 <= sqrt(S4 P),
    S4=sum wbar s^4  [=(1-epsilon^6)/6 in the continuum].

Therefore the SAME normalized spectrum obeys

    P >= E²/[sqrt(S4+3E)+sqrt(S4)]²,
    w=P/E >= E/[sqrt(S4+3E)+sqrt(S4)]².                   (5)

For E=0 use the continuous zero-energy limit. The lower bound is conservative;
no claim that an actual time-dependent orbit saturates both inequalities is
needed. Equivalently, a proposed w<=wmax<1/3 requires

    E <= 4S4 wmax/(1-3wmax)².                              (6)

Neither m nor redistribution of the action amplitudes evades (5). At high
normalized density its bound tends to 1/3. Increasing a sole abundance zeta
therefore changes pressure and response along with density; it does not supply
an independently cold dust component.

For reference-density diagnostics in SI units,

    E_required = (3/4)(1-epsilon²) Omega_exc
                       (c H0/g*_SI)².                    (7)

Equations (5)-(7) are a direct pre-fit joint test once a background reference
and a galaxy acceleration calibration are declared. They are not an observation
fit. The older conditional background reference is already documented in
`COSMOLOGY_CLOSURE_TEST_V001.md`; it must not be recycled as independent evidence.
Using g*=3pi*a0/8 from the OLD relaxed curve is specifically a diagnostic of
that inherited calibration. An excited-state galaxy response is different:
joint inference could change g* and must recompute the full state-dependent
prediction. Failure of the inherited reference is not a proof that every
four-parameter candidate is excluded.

More generally the dimensional moment governing the bound is

    C (kappa²/u4) integral nu(delta) delta^4 ddelta.

Changing the high-gap spectral shape can change this moment, but also changes
the same force response and matching energy. That is a named new shared model
parameter/assumption requiring recomputation, not a hidden abundance correction.
A coherent nonadiabatic state need not obey the rapid-virial bound, but must
then predict its actual time-dependent stress; it cannot simply be called dust.

## 4. A boundary-determined stationary galaxy closure

The averaged scalar action already derived in
`FIXED_ACTION_MODE_INTERFACE_V001.md` has per-mode energy e_j(I,h), frequency
omega_j=e_{j,I}, and phase theta_j. Choose an actual outer state (Ib,j,hb,Nb)
from the shared history/boundary prescription and set

    mu_j=Nb omega_j(Ib,j,hb),
    N(r) omega_j(I_j(r),h(a(r)))=mu_j,
    theta_j(t,r)=mu_j t+constant_j.                       (8)

This subsection is the RADIAL SCALAR subspace, hence an immediately definable
internal test with a declared radial boundary state. The isotropic vector
ensemble of section 2 is not automatically in that subspace after a radial
source develops: transverse/angular motion can survive. A prediction from
that SAME cosmological ensemble must either retain the vector copies or derive
their additional action/orientation transport. One cannot silently align them
and reuse scalar I_j. The scalar calculation needs no new arbitrary growth
port, but does not itself establish this transport or formation selection.

The constants mu_j are mode-specific outputs of the ONE boundary state, not
independent halo parameters. Simultaneous normalization of coordinate time,
N and mu changes no local frequency mu/N. On a chosen branch with e_{II}>0,
(8) determines I_j algebraically and

    I'_j= -[omega_j N'/N + omega_{j,h} h_r]/e_{j,II}.      (9)

It solves the static phase transport equation and gives zero initial and
secular mode momentum: theta'_j=0 and
sum w_j I_j (N omega_j)'=0. Uniform phases are a declared ensemble, not a
postprocessing replacement of the saved coherent trajectories.

At h=0 the positive harmonic-plus-quartic oscillator hardens: omega(I) increases
from omega0 to infinity. For mu/N>omega0 the positive-action solution is unique,
and lowering N at fixed mu raises I. This is a constructive conditional
clustering response, not an imposed radial density. At or below the ground
frequency, handle I=0 and its unilateral boundary separately. At nonzero h,
the already derived softening can make e_{II} vanish or change sign. Follow the
boundary-connected branch and retain nonexistence/multiplicity/instability as
outcomes; do not choose roots to improve a curve.

Where that branch is invertible, define the already owned Legendre function

    Pi_j(Q,h)=I_j Q-e_j(I_j,h),   Q=mu_j/N.

An explicit reduced STATIC variational problem is then

    S_static=4pi integral dt dr N L R² {
        M² R3/2+C[sum_j w_j Pi_j(mu_j/N,h(a))-DeltaU]}+S_b,
    a=N'/(N L),                                          (10)

with the usual metric boundary term retained. Vary N,L,R before imposing an
areal gauge; Q's lapse dependence and h's lapse-gradient dependence remain.
For example its normal mode density is still

    rho_mode=C[sum w e+DeltaU+a Bbar h'(a)
                         +(R² Bbar h'(a))'/(L R²)],
    Bbar=sum w kappa delta <y>_(I,h),                     (11)

not just sum w e and not a separately fitted static mu. The original metric,
clock and matter equations must all hold. Ordinary static baryons require
their supported stress/current, or a declared exterior annulus with an owned
interior-mass boundary. Pressureless collapsing dust is not a stationary disk.

The same static variation also supplies the other components, not a guessed
fluid closure. Put E=sum w e, Pi=sum w(I omega-e), F=Bbar h'(a), and
div F=(R²F)'/(L R²). Then

    rho_mode=C[E+DeltaU+aF+div F],
    p_r,mode=C[Pi-DeltaU-aF],
    p_t,mode=C[Pi-DeltaU].                                (12)

In particular N omega=mu implies

    Pi'=-(E+Pi)N'/N+Bbar h_r.

Using h_r=h'(a)a' and a=N'/(NL), direct substitution gives the exact static
radial conservation identity of this averaged closure,

    p_r'+(rho+p_r)N'/N+2(p_r-p_t)R'/R=0.                  (13)

The term aF makes the pressure anisotropic and is required for the cancellation;
keeping only Pi would fail it. This supplies a useful constraint-consistent
static source for Einstein's radial equations. It does not establish an
equilibrium boundary-value solution, its stability, or its formation from the
isotropic vector initial ensemble of section 2.

Equations (8)-(11) specify a small coupled equilibrium candidate. They do not
establish that cosmological formation reaches it, remove clock caustics, justify
uniform averaging at vanishing gaps, or establish stability. A finite outer
matching surface and its cosmological/source data must be owned; an arbitrarily
chosen outer halo amplitude is not supplied by calling it a boundary condition.

## 5. What may be calibrated, and what remains a real prediction

Shared g*, S, tau* and state normalization may be inferred transparently, with
the template/cutoff/ensemble assumptions counted. Ordinary distance, stellar
calibration and baryonic-history uncertainties retain their independent data
and priors. No radius-dependent force, independently fitted galaxy actions,
unrecorded vacuum shift or separate cosmic abundance is allowed within this
candidate. All earlier frozen-law results remain results of their old model.

The immediate inexpensive sequence is: apply the exact pressure bound; test
the existing prepared-annulus release for the actual coherent state; then test
the NEW boundary-determined equilibrium (8)-(11) on its explicitly different
phase ensemble. It is not necessary to invent another arbitrary source port
before performing these conditional effective-model tests. It is necessary to
keep the difference between an inferred initial state and its native formation.

If the candidate survives, independently useful predictions include held-out
galaxies under the same parameters/state rule, the pressure and redshift
evolution in (4), the relation rho_exc/rho_vac from the same energy function,
and coupled lensing/growth once their full equations are solved. A low
homogeneous bulk-compression coefficient is not by itself a derived spatial
clustering sound speed. No such observation, equilibrium or perturbation
success is claimed by this analytical note.
