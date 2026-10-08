# An owned galaxy exterior and a closed initial-value continuation: V001

2026-09-29. Analytical design only. No scientific producer, new fit, chosen
halo radius, altered finite-gap calibration, or frozen-file edit. This
continues the declared macroscopic alpha-one action, not a claim that its
clock or constitutive parameters have been derived from native BS dynamics.

## 1. Decision: an exterior is state and current data, not a zero wall

The completed clamped patch is a legitimate externally supported scalar
diagnostic. Increasing its box or removing its hard reaction does not by
itself supply a physical cosmological exterior. The same action has two
different branches that must remain distinct:

- Aligned static clock: T=t, soft minima, theta=mu t, and
  N omega_R(I,h)=mu. This is the polarized equilibrium existence problem.
- Geodesic preferred clock: a_mu=0 and zero soft coordinates/velocities.
  The exact residual theory is GR plus the SAME hard barotropic energy
  e_R(I,0), its full phase current, ordinary matter, and matched DeltaU.
  The hard-fluid velocity need not be geodesic or coincide with the clock.

Neither branch may be silently selected by resetting T or the hard phase
inside a spatial solve. The first can fail a qualified static necessity
test without excluding the second. Network energy is allowed to concentrate;
its concentration must be solved rather than supplied as a halo profile.

## 2. Necessary data for a genuinely matched static interior

At a specified cosmological epoch, the existing calibration supplies I_bar,
omega_bar, e_bar, p_bar, H and DeltaU. A time normalization fixes N and mu
together. Only their ratio is physical. On a finite matching worldtube,
assigning N_b and the actual h_b determines occupied I_b through
omega(I_b,h_b)=mu/N_b; one cannot also set I_b=I_bar independently.

Without an added surface layer, matching must retain the induced geometry,
the gravitational constraints/boundary momenta, the hard current through
the worldtube, and the clock/soft state. In the qualified weak scalar
equation the normal response flux D=Kb grad Phi-F is continuous when there
is no ordinary sheet. A jump in polarization flux is a source, not a free
boundary convention. The full action supplies the corresponding metric
and clock boundary terms. Since the soft modes have convective dynamics,
their incoming state follows clock characteristics; arbitrary extra spatial
Neumann data are not a substitute for that state.

Two tempting shortcuts fail:

1. A homogeneous cosmic I_bar, arbitrary Dirichlet potential, and zero
   current are not three independent pieces of exterior data.
2. A compact hard droplet with I=0 outside is not the same cosmic branch:
   at N->1,h->0 its chemical potential is mu=omega_bar>R, so the empty
   complementarity inequality mu<=omega_R(0,0)=R fails.

Near the cosmic state the aligned-static exterior is
K0 Delta Phi+J Phi=0, not the Laplace equation. Its regular oscillatory
homogeneous solution j0(sqrt(J/K0)r) decays pointwise but is not a localized
finite-norm perturbation. Pointwise Phi->0 therefore does not select a
unique exterior; imposing a chosen outgoing static complex wave would be
an additional prescription, not cosmological matching. A retarded dynamic
solution can select a response, but need not approach a time-independent
limit. Moreover, the weak-density overlap criterion includes
|Phi|/c_I,b^2<<1 and the actual source-induced frequency shift, not merely
|Phi|<<1. An extremely cold boundary may have no useful static overlap on
the intended local patch.

Thus the cheapest next STATIC step is the analytical/saved-arithmetic
necessity certificate in SHARED_STATIC_RADIATION_NECESSITY_V001.md. A
successful certificate application is not a replacement for matching; an
inadmissible attractive branch should not trigger repeated wall tuning.

## 3. The exact geodesic-branch hard-fluid evolution is already closed

Use c=1 and the same action density C beta[I Q-e_R(I,0)],
Q=sqrt(-partial theta squared). Let

    ds^2=-N^2 dt^2+gamma_ij(dx^i+shift^i dt)(dx^j+shift^j dt),
    omega=e_I, p=I omega-e,
    k_theta^2=gamma^ij theta_i theta_j,
    Gamma=sqrt(1+k_theta^2/omega^2),
    Pi_theta/(C beta)=P=sqrt(gamma) I Gamma.                 (1)

Choose the future branch theta_dot-shift^i theta_i>0. Variation gives

    theta_dot=shift^i theta_i+N omega Gamma,
    P_dot=partial_i[shift^i P
                         +N sqrt(gamma) I gamma^ij theta_j/omega]. (2)

These are exact on the stated geodesic/zero-soft branch. They retain the
normal current and its actual energy, not a fitted fluid mass. For fixed
P, spatial metric and phase gradient the algebraic inversion is unique:

    d(I Gamma)/dI=Gamma(1-v^2 c_I^2)>0,
    v^2=1-Gamma^(-2), c_I^2=I e_II/omega.                    (3)

The h=0 positive quadratic-plus-quartic orbit has 0<c_I^2<1/3 for I>0;
the empty and harmonic limits follow continuously. No arbitrary kinetic
function or transport coefficient is introduced by (1)-(3).

The full stress to use in the Einstein equations is

    rho_normal=C beta[(e+p)Gamma^2-p]+C DeltaU,
    S_ij=C beta[(e+p)Gamma^2 v_i v_j+p gamma_ij]
                                                -C DeltaU gamma_ij,
    v^i=-gamma^ij theta_j/(omega Gamma),                     (4)

with ordinary matter added and its momentum retained. The vacuum cancels
only from properly subtracted perturbation equations; it remains in H,
Hdot and the geometry. This is not the aligned-static E+3Pi lapse equation
with h set to zero. In particular its scalar metric constraint, phase
current and time derivatives must be solved consistently. Frame dragging
and stress-induced slip may be bounded at their actual weak-field order,
not suppressed by declaring Phi=Psi without a check.

Equations (1)-(4) are a reusable exact matter kernel for a relativistic or
controlled weak-field axisymmetric evolution. The fluid sound cone follows
c_I; the preferred-clock congruence must also remain caustic-free. Fluid
shocks, multistreaming or clock caustics are breakdowns to report, not a
license to insert unowned velocity dispersion, viscosity or phase resets.
The scalar constitutive/rapid-averaging assumption is still the adopted
macroscopic state; it does not establish the microscopic averaging window.

## 4. Smallest concrete closed synthetic disk initial state

Reuse the same synthetic baryonic source scale a and mass M as the clamped
test, including its calibration-dependent GM=gstar a^2. The exact initial
Kuzmin density and its baryon-only peculiar potential are

    Sigma(R)=M a/[2pi(R^2+a^2)^(3/2)],
    Phi_b(R,z)=-GM/[c_light^2 sqrt(R^2+(|z|+a)^2)].          (5)

This is not an observed NGC3198 input or a halo fit. A prospective initial
slice may set the hard fluid to its same homogeneous cosmic action I_bar
and zero peculiar phase gradient, and set the preferred clock to a
hypersurface-orthogonal geodesic normal with zero soft state. The ordinary
disk is represented by collisionless circular rings with initial physical
radial velocity zero and

    v_phi^2(R)=GM R^2/(R^2+a^2)^(3/2).                      (6)

In comoving coordinates the required peculiar radial velocity also includes
the coordinate conversion -H R. Rotational momentum and the cosmological
background are part of the initial constraint data. Formula (5) is the
leading weak-field scalar potential when the hard peculiar density is zero;
it does not fix the independent metric time derivatives or shift, which
come from the Hamiltonian/momentum constraints and gauge. Full constraint
residuals and the corrections to (5)-(6) must be recorded.

After the initial slice, both the baryonic rings and the hard phase evolve
under their shared metric. Ring angular momentum is conserved by axisymmetry;
radial motion is not clamped. Hence there is no external assembly port or
unrecorded work keeping the disk fixed. The initial preparation energy is
explicitly part of the new initial state. It is not claimed to follow from
the previous pulse histories or a demonstrated cosmological formation path.

This initial condition tests whether that one shared cosmic population
concentrates around an existing baryonic seed, and how its force, density,
current and pressure change together. It does not test a mature equilibrium
at time zero. The reference epoch and a complete output-time census must
be fixed before any run; no final age may be chosen from a favorable
rotation curve. The natural gravitational unit sqrt(a^3/(GM)) is already
fixed by (5), not an adjustable per-radius response time.

## 5. A cosmological exterior must carry its induced current

Use a nonlinear interior plus a linear cosmological exterior of the SAME
finite-R fluid and ordinary species. Initialize that exterior with the same
unperturbed hard state and the actual ordinary seed tails. Interface values
are supplied by its retarded initial-value solution, or by an explicitly
evolved outer linear buffer, not independent zero-potential/zero-flow walls.
The full Kuzmin tail should be retained analytically or with a documented
convergent ring quadrature; truncating it is a numerical error, not a new
physical edge or halo radius.

An inexpensive leading weak-field check exposes the necessary velocity
tail. In a region where hard density changes and pressure gradients are
negligible to the intended order, write theta=theta_bar+delta theta.
The phase equation gives delta theta_dot=omega_bar Phi. With zero initial
peculiar gradient, the physical peculiar hard velocity in c=1 units is

    v_H(t,x)=-[a(t) omega_bar(t)]^(-1)
                   integral_ti^t omega_bar(t') grad_x Phi(t',x) dt'. (7)

This is an approximation to the same current equation, not a new forcing
law. It has friction H(1-3c_I,b^2), because
omega_bar_dot/omega_bar=-3H c_I,b^2. A locally harmonic exterior potential
can therefore drive a nonzero divergence-free velocity tail while leaving
the leading Newtonian density perturbation zero. Setting both density
perturbation and velocity to zero there is generally incompatible. Include
the ordinary tail and cosmological/metric terms where (7)'s simplifying
hypotheses fail; the existing full scalar Einstein/fluid interface supplies
that linear exterior.

For a fixed-coordinate computational volume, the exact current ledger is

    d/dt integral_volume P d^3x
      =integral_boundary [shift^i P
             +N sqrt(gamma) I gamma^ij theta_j/omega] dSigma_i. (8)

Here P and the displayed flux are coordinate densities, and dSigma_i is
directed coordinate area. A boundary moving with coordinate velocity
v_boundary^i adds P*v_boundary^i inside the right-hand flux by Reynolds'
identity. Moving an interface only between separate convergence runs does
not add a within-run velocity. The apparent acquisition of halo action
must equal the corresponding flux plus the
initial enclosed action, not a newly assigned abundance. Keep the ordinary
mass/angular-momentum ledger and the full matter-plus-metric energy/work
accounting as well. No global conserved FLRW energy is invented by (8).

The numerical interface is moved for overlap/convergence, not optimized to
fit the response. Its linear-exterior eligibility requires small actual
density/velocity perturbations and the same metric/averaging regime. A
failure to find an overlap is an outcome, not authority to change the
cosmic state. Likewise taking a static zero-frequency inverse of an unstable
or nonrelaxing exterior is not equivalent to evolving its retarded kernel.

## 6. Implementation order and scope of the decision

A first implementation can reuse the existing axisymmetric geometry and
ordinary Newtonian controls, but it evolves two hard fields (P,theta) plus
the baryonic ring coordinates and the metric constraints; it does not
reuse a static mu table. On this branch no soft-mode arrays need propagation
because their exact zero state is invariant. Exact h=0 orbit/action
functions already exist, so the new material work is the monotone scalar
inversion (3), not a new finite-field frequency solve at every cell.

The cheapest qualified first unit is a small axisymmetric initial slice
and short-time release, followed by a fixed refinement/current-conservation
test. Its independent limits are the initial Kuzmin field, the homogeneous
FLRW state, the previously derived closed two-fluid linear transfer matrix,
and the exterior current (7). A whole galaxy-age evolution is not required
to discover an inconsistent constraint or boundary prescription. A later
long evolution must keep actual H(t), pressure, state transport and clock
validity rather than repeat the short-time approximations indefinitely.

This is a concrete evolution of the already declared energy-bearing network
population. Its output may be weak concentration, collapse, oscillation or
loss of the scalar/clock description; none is selected in advance. It is
more physically informative than treating an attribution counterfactual as
a second model or repeatedly tuning a static wall. No calculation has been
authorized or executed by this note, and no empirical success is asserted.

## Sources read in full

- `MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md`, SHA256
  `64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3`.
- `COMMON_ACTION_GALAXY_BOUNDARY_AND_INITIAL_STATE_V001.md`, SHA256
  `2eb30bb54416d31a69109b1d48795789a208b2418bfb237cfd81a291ec006c26`.
- `CLAMPED_PHASE_EXISTENCE_AND_CONTINUATION_V001.md`, SHA256
  `ccd005abb0c74c736d06cda8cd961f01982d46801a205bb0c4b28cea164282af`.
- `SHARED_STATIC_RADIATION_NECESSITY_V001.md`: additive conditional
  necessity proof prepared alongside this continuation, no old-file edits.
