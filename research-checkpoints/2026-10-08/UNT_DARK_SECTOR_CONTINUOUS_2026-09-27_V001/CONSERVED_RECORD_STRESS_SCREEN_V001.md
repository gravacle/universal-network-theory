# Conserved-record stress: an exact conditional screen and its constructive escape

2026-09-27. Analytical diagnostic, not a new adopted UNT microscopic law.
No numerical experiment, cosmological fit, changed historical source, remote
execution, or A0 freeze. The previous goal turn established necessary
allocation identities; this note tests a specific proposed continuum
interpretation that would otherwise remain ambiguous.

## Result

A conserved record density with a local, single-fluid energy law cannot have
negative pressure if its energy vanishes at zero density and is convex all
the way from zero to the tested density. A conventional stable barotropic
branch with positive chemical potential has that convexity condition.

This is **not a no-go for network dark energy**, or even for every zero-vacuum
record fluid. Stability only near the current density is insufficient for the
theorem. An exact counterexample below has locally acceptable sound speed
and an accelerating-sign stress, but an unstable density interval separates
it from the zero-density state. This identifies a phase/formation question
that can be tested, rather than assuming that all obstacles refute UNT.

## 1. Imported interface — visible and limited

The repository's working-gravity closure supplies an adopted common metric,
complete source variation and calibrated positive total gravitational
stiffness. It does not derive record transport or the following fluid action:

See the resident [working-theory closure](../program-worktree/GRAVITY_RECORD_FIRST_WORKING_THEORY_CLOSURE_V001.md),
especially WTC-H1, H3, H5 and WTC06. Its physical bridge is adopted, not an
experimental or microscopic derivation.

**Additional conditional premises for this screen:** a smooth same-metric
continuum, one timelike conserved record current, local isentropic energy
density epsilon(n), no independent entropy/elastic/memory variables, no
nonlocal stresses or exchange sources, and a regular hydrodynamic regime.
These are hypotheses to earn from a network parent, not consequences of
recordhood. In particular fixed register labels in the finite hold do not
already supply a physical transport current.

For an explicit variational realization use the irrotational, isentropic
specialization of the relativistic current-action framework in
[Brown (1993), section 2](https://arxiv.org/pdf/gr-qc/9304026). The import is
the constrained-fluid variational method, not its validity for UNT. In
signature (-,+,+,+), define a vector density J^mu and

    n = sqrt(-g_mu_nu J^mu J^nu)/sqrt(-g),
    J^mu = sqrt(-g) n u^mu,       u_mu u^mu = -1,
    S = integral d^4x [-sqrt(-g) epsilon(n) + J^mu partial_mu phi].

Fix the boundary variation. Varying phi gives partial_mu J^mu=0; varying
J gives partial_mu phi=-epsilon'(n)u_mu. Vorticity requires additional
flow labels; the single-potential construction is not a general fluid.

At fixed J the independently checked metric variation is

    delta n = (n/2)(g_mu_nu+u_mu u_nu) delta g^(mu_nu).

Thus the stress obtained from this action, rather than assigned by naming a
record energy “vacuum,” is

    T_mu_nu = n epsilon' u_mu u_nu + (n epsilon' - epsilon) g_mu_nu,
    rho = epsilon(n),              p = n epsilon'(n)-epsilon(n).

This is a conditional physical realization of the earlier energy-elasticity
identity. It is not a derivation of the function epsilon or of the current.
The constant part of epsilon must be owned once: in this retained action or
in the matched geometric volume coefficient, not in both.

## 2. Exact convex-branch test

For n>0 suppose epsilon is continuous at zero, differentiable on [0,n],
and convex there. The supporting-tangent inequality at n gives

    epsilon(0) >= epsilon(n)-n epsilon'(n),
    p(n) >= -epsilon(0).

Therefore epsilon(0)=0 implies p(n)>=0. Equivalently, for a smooth function
with an integrable second derivative,

    p(n) = -epsilon(0) + integral_0^n x epsilon''(x) dx.

This displays exactly where a negative pressure can arise: a positive
background contribution, negative curvature of the energy somewhere in the
interval, or failure of this local one-variable energy description.

For the conditional barotropic perturbation closure, linearizing current
conservation and momentum balance in a locally inertial uniform patch gives

    partial_t delta n + n0 div(delta v) = 0,
    n0 epsilon'(n0) partial_t delta v + grad(delta p) = 0,
    partial_t^2 delta n - c_s^2 laplacian(delta n) = 0,
    c_s^2 = n0 epsilon''(n0)/epsilon'(n0).

Here epsilon'>0 gives positive enthalpy density n epsilon'. Absence of the
short-wavelength hydrodynamic gradient instability requires c_s^2>=0 in the
regime where this fluid approximation applies. Subluminality adds c_s^2<=1
in the adopted common-cone units. Neither condition proves full network,
gravitational or nonlinear stability. Gravity can still produce Jeans growth.

If epsilon'>0 and this stability condition hold **throughout (0,n]**, the
convexity theorem applies. Stability only near n does not imply it. If the
fluid description ends at n_min>0, its low-density continuation cannot be
invented to close this test.

For positive rho in the adopted Einstein leading response with no separately
counted cosmological term, this p>=0 component cannot provide the negative
rho+3p required for homogeneous acceleration. This final acceleration
interpretation is conditional on that gravity/cosmology interface; the
pressure inequality itself is not an Einstein-equation result.

## 3. Exact counterexample to an overstrong rejection

Consider the dimensionless algebraic family

    epsilon(n)=epsilon_* f(x),    x=n/n_*,
    f(x)=x-(3/2)x^2+x^3,         epsilon_*,n_*>0.

This is a counterexample chosen to test the theorem's scope, not a UNT
proposal, fitted dark energy or a network-derived equation of state.

Here f(0)=0 and f'(x)=3(x-1/2)^2+1/4>0, but f''(x)=6x-3 changes sign.
At x=11/20, direct rational substitution gives

    rho/epsilon_*       = 2101/8000,
    p/epsilon_*         = -121/1000,
    (rho+3p)/epsilon_*  = -803/8000,
    c_s^2               = 66/103.

Thus positive energy, positive enthalpy, negative accelerating-sign stress
and 0<c_s^2<1 coexist locally. The branch has epsilon''<0 below x=1/2,
so it is not a convex/stable continuation to zero density. No contradiction
of section 2 exists. A globally equilibrated system may phase-separate;
this local calculation proves neither metastable lifetime nor a viable
cosmic trajectory. In an expanding conserved-current history n decreases,
and a proposed evolution approaching the unstable region must address it.

The reviewer identified a sharper equilibrium check. Exactly,

    f(x) - (7/16)x = x(x-3/4)^2 >= 0.

A vacuum/dense-phase mixture using x=0 and x=3/4 therefore has energy
(7/16)x and the same mean conserved density for 0<=x<=3/4, ignoring interface
energy in the bulk limit where phase separation is permitted. At x=11/20
it is lower than the homogeneous energy by 11 epsilon_*/500. This proves
that the displayed homogeneous state is not the global bulk equilibrium in
that setting. Interface costs, topology or kinetic barriers might delay or
forbid the transition, but only a specified mechanism and lifetime analysis
could establish that for a network parent.

This example prevents rejection of a phase-based network explanation merely
because its dilute vacuum energy is zero. The new scientific obligations
would be a same-parent phase-selection/formation law, transition/gradient
dynamics, lifetime and perturbation analysis—not a post-hoc choice of this
polynomial's coefficients.

## 4. Constructive disposition for UNT

Three routes remain distinct and testable:

1. **Convex retained defects plus network background.** Derive epsilon(0)
   from the same network, retain positive dilute insertion energy for the
   matter-like part, and test interaction/stress corrections. The existing
   induced-action packet supplies a conditional volume-term mechanism, not
   its matched numerical value. Fitting a new constant is not the sought
   explanation.
2. **A selected nontrivial phase.** Derive a locally stable negative-pressure
   branch and how the network reaches and stays on it without uncontrolled
   instability. Zero energy at the dilute endpoint does not settle this.
3. **More than a density-only fluid.** Retained arrangement, elastic shear,
   multiple fields, sources or nonlocal memory can invalidate this reduction.
   Then derive their actual stress and perturbation law. They cannot be
   discarded to claim a simple-fluid pass and restored only after a failure.

The fastest discriminant is to determine whether the selected parent really
has a conserved transported record current and a single-valued local
epsilon(n). If so, its complete insertion-energy derivative and curvature
are the direct next quantities; if not, do not impose this fluid on it.
Changing the Hamiltonian coupling strength is not automatically changing
record density, so coupling-parameter concavity cannot substitute for this
compressibility test.

No route is declared completed, selected by observational fitting, or a
substitute for the primary active/maintenance program. The result narrows
which mathematical realizations can consistently support its claimed stress.
