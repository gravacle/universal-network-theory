# A prepared spherical release test from the retained parent

2026-09-29. Analytical reduction, no numerical worker, new fit or change to
the frozen force law. This uses the full conditional action in
`COUPLED_SPHERICAL_RESPONSE_PATHWAY_V001.md` and the exact per-mode action
identities in `FIXED_ACTION_MODE_INTERFACE_V001.md`. Both were read in full.
The native BS-to-metric dictionary is not assumed to have been derived.

## Result

A small self-consistency test is available **before** attempting a long
prepared-galaxy evolution. Insert an actual finite-band prepared state into
the full spherical constraints, then calculate the lapse/clock rate required
to preserve them on release. This computes whether that state admits a slow
source, rather than assigning it an effective static mu by hand.

The useful new ingredients are:

1. an explicit first-order initial-slice constraint for the radial metric;
2. the required lapse-rate equation, retaining the clock consistency condition;
3. an exact instantaneous action-change identity connecting that rate to the
   SAME prepared modes' subsequent population and energy evolution.

These are a small conditional gravity test, not another arbitrary creation
port or a velocity rescaling. A failed constraint, singular release operator,
or rapidly changing source is a meaningful outcome for the proposed state.
It would rule out the attempted quasistatic use, not all preparations or UNT.

## 1. Why Gauss plus local oscillators is not yet the closed system

The full parent has mode coordinates x_j, physical normal velocities v_j,
positive finite weights w_j, and

    b_j=kappa*delta_j,
    B=sum_j w_j*b_j*x_j,
    h(a)=a/sqrt(1+a^2/g_s^2),
    E0=sum_j w_j[m_j*v_j^2/2+kappa*delta_j^2*x_j^2/2+u4*x_j^4/4].

The spherical normal acceleration is a=N'/(N L), not in general the
coordinate metric force of a static observer. With normal threading
beta=0, the exact mode equation is

    D x_j=v_j,
    m_j[D v_j+theta*v_j]+kappa*delta_j^2*x_j+u4*x_j^3=b_j*h(a),
    D=(1/N)partial_t,       theta=K_r+2K_t.                 (1)

Its normal density is

    rho_mode=C[E0+DeltaU-Bh+a B h'
                         +(R^2 B h')'/(L R^2)].            (2)

Here h' and h'' mean acceleration derivatives; primes on radial fields mean
radial derivatives. Both uses are written explicitly when ambiguity matters.
The same state also contributes sum p_j*x'_j to the radial momentum constraint.
Thus an update which solves only a static spherical force equation and (1),
while holding the clock or geometry motion fixed, has discarded equations.
In particular, a local held mean does not satisfy the full momentum equation
merely because the local oscillator periods were accurately calculated.

The already known linear limit is a stringent null check: regular-center
clock charge obeys B_dot=0, and the physical clock velocity changes according
to v_clock_dot=a-Phi'. Zero prepared modes select the geodesic GR branch,
not an automatically amplified static force. The nonlinear calculation must
retain that limit, not replace it with the galaxy law.

## 2. Exact initial-slice construction with actual mode data

On ONE initial slice choose areal radius R=r and K_t=0, equivalently p_L=0.
This is an initial-data choice, not a permanent gauge truncation. Keep the
radial metric dynamical afterward. Define

    f=L^-2>0,       nu=(ln N)',       a=sqrt(f)*nu.

For specified physical x_j(r),v_j(r), a positive lapse N(r), and normal
baryon density rho_b(r), the mode momenta are

    p_j=C*(r^2/sqrt(f))*w_j*m_j*v_j.

The full initial momentum constraint can then be satisfied by

    p_R=-sum_j p_j*x'_j-p_chi*chi',                        (3)

since R'=1 and p_L'=0. For baryons initially at rest relative to the normal,
chi'=0 and p_chi=(r^2/sqrt(f))*rho_b. This is a momentary dust initial state,
not an unsupported static dust galaxy. It must subsequently follow its
continuity and momentum equations. A supported body instead needs its own
ordinary pressure/stress; it cannot be held fixed without that owner.

The spatial scalar curvature is exactly

    R3=2(1-f-r f')/r^2.

The extrinsic combination 4 K_r K_t+2 K_t^2 vanishes on this slice even
though K_r and p_R need not vanish. Substituting (2) into the full lapse
constraint and collecting the occurrences of f' gives the explicit ODE

    [M^2/r + (C/2)*B*h''(a)*nu] f'
       = M^2*(1-f)/r^2-rho_b
         -C{E0+DeltaU-B*h(a)+a*B*h'(a)
              +sqrt(f)*h'(a)*(B'+2B/r)
              +f*B*h''(a)*nu'}.                           (4)

No weak-field expansion, phase average, fitted density, or replacement of
mode energy by its relaxed minimum was used in (3)-(4). To check (4), expand

    sqrt(f)/r^2 * [r^2 B h'(a)]'
       =sqrt(f)*h'(a)*(B'+2B/r)
          +f*B*h''(a)*nu' + (B*h''(a)*nu/2)*f'.          (5)

This identity gives an independent implementation check against the original
constraint before any release step. The coefficient of f' can vanish;
dividing by it without reporting that event is not justified. Positivity of
f, regularity, the actual constraint residual and this coefficient are outputs.

For a regular center take B=O(r), nu=O(r), f=1+O(r^2), and regular physical
radial x_j,v_j=O(r). Alternatively use a finite annulus with an explicitly
owned inner mass/metric boundary and outer clock boundary. Annular initial
data are not a complete isolated galaxy until their boundary source and
continuation are supplied. Changing old coefficient DeltaU or subtracting
the prepared energy to obtain a favorable f is not allowed.

Choosing N at this initialization specifies a physical preferred-clock
preparation; it is not the claim that arbitrary future lapse histories are
gauge choices. Equations (3)-(4) impose the displayed constraints on that
preparation. Their preservation still has to pass the next test.

## 3. Release determines the clock rate

Let z denote ALL canonical fields of the existing spherical Hamiltonian:
L,R,x_j,chi and their momenta. Write its functional lapse constraint as

    F[z,N]=delta H/delta N=0,

with its specified metric and clock boundary conditions. After the preparation
controller is released, Hamilton's equations give z_dot=X_H[z,N]. Constraint
preservation requires

    F_N[N_dot] = -F_z[X_H].                               (6)

Equivalently the right side is -F_q H_p+F_p H_q. The notation denotes full
functional linearization including radial derivatives and endpoint terms,
not the derivative of a pointwise algebraic Gauss relation. The common time
normalization must be fixed, for example by the declared outer lapse, rather
than misidentifying its residual reparametrization as a physical zero mode.
Equation (6) assumes no explicit time-dependent source or boundary data;
if the chosen boundary/controller still moves, add -partial_t F|explicit
and its actual work instead of calling that protocol a free release.

The principal radial part of F_N has the previously derived coefficient
C B h''(a)/(N L^2), after the same density normalization used in the parent
note. It becomes degenerate at B=0 or a=0 and can change its character with
the state. A finite discretization must retain its full lower-order terms,
not insert a new pinning term to make it solvable. If the operator has a
null space, the right side must satisfy its compatibility conditions before
one can claim release. The already derived linear clock-charge system is
the appropriate independent benchmark at its degenerate null branch.

Where (6) is solvable, the actual initial source rate is

    partial_t a = [(N_dot/N)']/L-a*(L_dot/L),
    D h = h'(a)*(partial_t a)/N.                          (7)

It need not be slow merely because the baryonic density was changed slowly
in a different clamped experiment. Equations (3)-(7), with the full canonical
equations, provide a precise release diagnostic using the actual y and v,
without requiring a new long-time phase average or a galaxy observation.

The radial momentum constraint and its first time derivative must also be
reported. Their continuum consistency follows from the retained action;
a finite radial discretization does not automatically preserve it. A static
mean state additionally has the established condition

    sum_j w_j I_j partial_r(N omega_j)=0.                 (8)

Failure of (8) is not repaired by phase randomization: it is a secular
momentum source. Keeping actual unaveraged modes permits the geometry and
clock to respond instead of imposing (8) artificially.

## 4. Exact action drift at release, not an action reset

For each positive-gap mode define its instantaneous held-orbit action using
its ACTUAL instantaneous energy and source:

    e_j=m_j*v_j^2/2+kappa*delta_j^2*x_j^2/2+u4*x_j^4/4-b_j*h*x_j,
    I_j=I_j(e_j,h),       omega_j=partial e_j/partial I_j.

This defines a local diagnostic even before an adiabatic approximation. Away
from I=0, the exact orbit identities and mode energy equation give

    D e_j=-theta*m_j*v_j^2-b_j*x_j*D h,

    D I_j= -theta*m_j*v_j^2/omega_j
           + b_j*(<x_j>_(e_j,h)-x_j)*D h/omega_j.         (9)

The brackets in (9) describe the held orbit at the current state, not a
substitution of its mean into the real evolution. Hence

    D I_j+theta I_j
       =theta*(I_j-m_j*v_j^2/omega_j)
          +b_j*(<x_j>-x_j)*D h/omega_j.                  (10)

Only if source and volume changes are small over a period may averaging use
<m_j v_j^2>=I_j omega_j and yield D I_j=-theta I_j. Equations (9)-(10)
provide the quantitative bridge from the constraint-determined clock rate
to the existing prepared action/stress ledger. They do not assume that
action conservation already holds during release.

A useful finite-band diagnostic reports both terms of (10), their absolute
weighted sums, and their size compared with omega_j I_j for nonzero actions.
Near-zero-action modes require absolute excitation-energy controls instead
of division by a tiny I. The moving-minimum branch must use the unaveraged
equations rather than an undefined oscillator phase. No mode is dropped
because its rate makes the quasistatic hypothesis inconvenient.

The coefficient 1.615863038 of the previously proved deep held mean has no
place as a multiplier in (3)-(10). It may emerge in its specific gap/time/
preparation limit, but it neither determines this lapse rate nor removes
the additional excitation stress and momentum. In particular, it cannot be
applied to a saved disk velocity curve as a substitute for solving the field.

## 5. Precise small implementation target

The next task should be a **constraint-compatible prepared-release derivative
census**, followed by a short coupled continuation only if its initial
constraints and consistency equations admit it. It need not start with a
large spherical evolution or another family of orbit-mean integrations.

Use one authenticated, already qualified finite-band state and retain every
mode in it. An economical reproducible choice is the existing 64-node,
gap=.001, duration=8 preparation, taking the lowest previously frozen source
amplitude by its existing index rather than selecting an amplitude from a
rotation residual. Its 128-node counterpart supplies the inherited spectral
resolution contrast. This is an internal conditional example: time remains
uncalibrated, and no native-to-physical inertia or metric conversion is inferred.

There are two honest ways to supply its new spatial data:

- For a finite annular release, use the SAME saved x_j,v_j at every initial
  proper position and own the two boundary geometries/clock values. This is
  an explicitly adopted uniform radial-state preparation on that annulus,
  not a regular-center whole-galaxy state. Its original local clamp history
  and work are known. Any mismatch between the old clamp h_c and initial
  metric source h(a) contributes the explicit local interaction-work change
  -B[h(a)-h_c], plus separately owned metric/controller/boundary work.
- For a regular-center body, first specify one smooth radial source and one
  common temporal preparation with a conserved ordinary-matter/controller
  stress. Integrate that history. Do not multiply the saved nonlinear orbits
  by a spatial envelope and call the result the same computed history.

The first option is the smaller interface test. It explicitly adds an
initial spatial/boundary embedding, not new constitutive parameters. Freeze
its annulus, lapse, inner metric datum and baryonic initial state before
computing the response; none may be inferred from the exposed galaxy residuals.
No choice is fixed by this analytical note, and no outcomes were generated
to select them. The controller/boundary ledger is necessary if the exercise
is later promoted from an initial-data diagnostic to a closed physical history.

At 16 and 32 radial cells, 64/128 finite modes need only a few thousand real
state entries; there is no Hilbert-space exponential. Evaluate (3)-(5), then
the full variational Hamiltonian derivatives and the linearized equation (6)
with the declared endpoint conditions. Independent differentiation of the
original constraint checks (4), and finite directional differences check
F_N and F_z before a short release step. Retain all constraint residuals,
singular values/compatibility residuals, f and lapse positivity, mode energy,
momentum, a_dot, action-rate diagnostics and boundary work. Exact null/linear
benchmarks remain mandatory comparisons, not scientific pass conditions.

If the release rates are controlled, the same canonical equations advance
the state without resetting actions. If not, the calculation has identified
why an independently held mean cannot yet be used as an autonomous gravity
law. That is a direct constraint on the proposed prepared mechanism and the
missing physical preparation—not a reason to substitute a fitted halo or
to adjust the frozen source spectrum.
