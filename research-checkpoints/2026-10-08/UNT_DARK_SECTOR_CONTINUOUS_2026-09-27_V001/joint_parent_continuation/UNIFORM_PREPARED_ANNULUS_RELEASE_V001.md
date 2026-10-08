# Uniform prepared annulus: exact initial release by two quadratures

2026-09-29. New analytical simplification of
`PREPARED_SPHERICAL_TEST_REDUCTION_V001.md`; no propagation, fit, new force
term, or change to saved states. Root and this derivation independently
obtained the same scalar-flux equation. This is an internal test of the
existing conditional metric/mode parent, not a native-to-metric identification.

## 1. The actual frozen state, without a new population

Read `COMMON_HISTORY_MECHANISM_V001_RESULTS.json`. Fix gap=.001, duration=8,
hold=0 and the lowest **already prescribed** amplitude g=.0025, equivalently
g/a0_internal=.002945243112740431. No galaxy residual selects this input.
Its three inherited resolution entries are:

| JSON location | Mode nodes | Preparation dt | Role |
|---|---:|---:|---|
| payload.cases[0].observations[0] | 64 | .01 | Quadrature coarse |
| payload.cases[1].observations[0] | 128 | .01 | Same-dt quadrature control |
| payload.cases[2].observations[0] | 128 | .005 | Preparation-time refinement |

There is **no** 64-node dt=.005 entry in this frozen file. Do not invent it
or conflate the [0]-[2] difference with a purely spectral error. Each case
owns its complete `delta`, `weights`, `Kb` and the observation's actual
`y`, `v`, energy, kinetic energy and work arrays/scalars. Use all modes.
The same stored source parameters are kappa=u4=m=1, gs=21.65919852693508,
Kb=.4999995 and an explicitly UNCALIBRATED internal time unit.

For orientation, arithmetic on the saved arrays gives

    B=sum_j w_j delta_j y_j ≈ .00172035974227 > 0,
    V_B=sum_j w_j delta_j v_j ≈ 8.60555703e-5 > 0.

The 128/.005 entry has saved preparation work 8.845073643961865e-7 and
complete local mechanical energy 8.845073643972368e-7. These are clamped
preparation quantities, not the total ADM energy of a new spatial universe.
Individual v_j have both signs; V_B must come from their signed sum, not
from an RMS, a rephased state or zeroed velocities.

Result outer SHA-256:
`e57f1f93254a610abc9b08ef5df355d74035efa762079ffd43e89205bc0f715a`.
Its canonical payload SHA-256 is
`91793086852fe6fe12908bae49f6eb983c7aa15d7211cd7abf496a7827d4691e`,
and its frozen-input SHA-256 is
`13d05e24680166cb903e02fb961717a2bef1a89771a1d76c80156ab50cbe76ef`.
Authenticate the existing freeze and its actual relative/absolute source
paths; this note does not replace that source provenance.

## 2. A precise initial-data class

Choose an annulus r_in<=r<=r_out with r_in>0. At its initial instant let

    R=r,   L=f^(-1/2)>0,   beta=0,
    x_j(r)=y_j,saved,   v_j(r)=v_j,saved,
    p_L=p_R=0,   chi'=0.

The last condition means any ordinary baryons are instantaneously at rest
relative to the normal; it is not a permanent support prescription. Since
x'_j=0, the initial radial momentum constraint is satisfied. Both metric
velocities and both extrinsic curvatures initially vanish. The physical
mode momenta vary as C L r^2 w_j m_j v_j, even though x and v are uniform.
Confusing uniform physical velocities with uniform canonical momenta would
give a different state and spoil the argument.

Specify one positive initial lapse N(r) and solve the exact initial f ODE
in the preceding note, retaining the original DeltaU and actual E0. This
is not the substitution f=1. Own the inner metric/mass datum and the two
lapse boundary values. They describe a conditional annular embedding;
they do not establish a closed regular-center formation history.

For an explicit small weak-field family, one may prospectively take
r_out=2 r_in, N=exp[g_c(r-r_out)], g_c=.0025, a vacuum annulus rho_b=0,
and an inner baryonic mass with GM_b=g_c*r_in^2. The inner metric datum
from that body plus the unchanged baseline is

    f(r_in)=1-2g_c*r_in-Lambda*r_in^2/3,
    Lambda=2DeltaU/Kb.

Take r_in sufficiently small that g_s*r_in, |Lambda|*r_out^2 and the
actual prepared-energy compactness are small, and verify f>0 and the
nonzero initial-ODE coefficient rather than assuming them. This names the
dimensionless diagnostic family without claiming an inherited physical
length calibration. DeltaU may remain symbolic until its actual owned
value is supplied; it must not silently be set to zero. A zero-baseline
case, if useful, is a separately labeled control, not the principal parent.
No new local force coefficient or per-radius action is inferred or fitted.

## 3. Factorization of the exact lapse linearization

Use the normalized constraint with sign

    F=(M^2/2)(R3+4 K_r K_t+2 K_t^2)-rho_b-rho_mode.

At fixed canonical fields define eta=delta N/N, so
delta a=sqrt(f)*eta'. Put

    D=N r^2 B h''(a) sqrt(f),
    a=sqrt(f)*(ln N)'.

Direct variation of the full acceleration-dependent density gives

    F_N[delta N]
       = -C sqrt(f)/(N r^2) * [D eta']'.                  (1)

In particular the a B h' term and the lapse derivative of the polarization
divergence must both be retained to obtain this weighted divergence. There
is no additional zeroth-order term in eta. A uniform eta is the residual
common time-normalization direction, fixed by the boundary clock choice.

For B>0 and a>0, the bounded source has h''(a)<0, hence D<0 throughout a
regular annulus. With eta=0 at both ends, the homogeneous equation has no
nonzero solution: multiply (D eta')'=0 by eta, integrate, and obtain
integral D(eta')^2 dr=0. Thus this release operator is invertible when D is
continuous and bounded away from zero. Its magnitude can still be very
small, yielding a large required rate; invertibility does not imply slow
response, physical stability, or well-posed nonlinear evolution forever.

## 4. The actual state source also integrates exactly

At this instant theta=0 and geometry_dot=0. Holding lapse fixed while
taking the canonical Hamiltonian flow gives

    B_dot=N V_B,        E0_dot=h(a) B_dot,
    rho_b_dot=0.

The last equation holds for the declared momentarily resting dust/vacuum
source and no explicit boundary or production term. The derivative of the
extrinsic-curvature quadratic terms vanishes because both curvatures are
zero. Consequently constraint preservation integrates once to

    N r^2 [B h''(a) sqrt(f) eta' + B_dot h'(a)] = K,
    eta=N_dot/N.                                         (2)

Define A=N^2 r^2 V_B h'(a). At fixed boundary lapse values, eta=0 at both
ends, so just two radial quadratures determine the constant and the solution:

    K = [integral_(r_in)^(r_out) A/D dr]
                           /[integral_(r_in)^(r_out) 1/D dr],
    eta'=(K-A)/D,
    eta(r)=integral_(r_in)^r (K-A)/D ds.                  (3)

No large functional Jacobian, guessed clock source, new damping or pump is
needed for this particular initial-release calculation. Nonzero prescribed
boundary lapse rates enter the endpoint difference in the integral of
eta' and have to be retained with their source/work interpretation.

The initial physical acceleration and source rates are

    a_dot=sqrt(f)*eta',
    D_proper h = h'(a)*sqrt(f)*eta'/N.                    (4)

The scalar flux K is the constraint integration constant, not automatically
a photon, matter or energy luminosity. Those currents require their own
stress/continuity equations. The two fixed boundary clocks supply no explicit
N_dot boundary drive in this diagnostic; extending the annulus through time
still requires its metric/matter boundary evolution and complete work ledger.

## 5. Sharp weak-field oracle and what it decides

In the small-compactness limit f,N approach one and a approaches a fixed g_c
while B,V_B remain the actual initial-state values. Equation (3) reduces to

    eta' = [V_B h'(g_c)/(B h''(g_c))]
                          *[r_in*r_out/r^2-1].           (5)

This follows from integral r^-2 dr=(r_out-r_in)/(r_in*r_out), and provides
an independent analytic oracle for the exact finite-curvature quadratures.
It is a limit of the constraint-compatible initial data, not a claim that
f=1 exactly solves the gravitating prepared-energy constraint.

For r_out=2r_in the bracket is +1 at the inner end, zero at sqrt(2)r_in,
and -1/2 at the outer end. For this actual V_B>0,B>0 and h''<0, the source
rate therefore has opposite signs at the two ends. Shrinking both radii
with their ratio fixed does not remove this leading rate. The small h''
at the inherited weak source can make it large; its actual magnitude and
comparison with all retained mode frequencies are prospective outputs.

An initially stationary source would instead require A(r) to be constant.
Uniform V_B with the stated lapse/geometry does not satisfy that condition.
Choosing a new spatial V_B proportional to 1/[N^2 r^2 h'] or resetting the
saved velocities to force stationarity is a new preparation, not this test.
For a regular-center continuation, a finite initial field makes the constant
zero, requiring V_B=0 wherever h'>0. An annulus may retain a nonzero boundary
flux, but cannot pass it off as a closed whole-galaxy preparation. A separately
owned phase-paired ensemble could cancel V_B while retaining excitation;
it would be a new prepared state/formation rule, not the original saved state.
V_B=0 is only an initial first-derivative condition, not sufficient for
long-time equilibrium or preservation of higher constraint derivatives.
In the exactly linear-coupling limit h''=0, equation (2) becomes a genuine
compatibility requirement (N r^2 B_dot h')'=0 rather than an equation one
may invert. This identifies precisely why a Gauss-only instantaneous release
can fail while the bounded parent has a unique but potentially fast clock rate.

The same rate predicts the actual instantaneous action drift, without any
new mode population:

    D_proper I_j= b_j(<x_j>-x_j) D_proper h/omega_j,       (6)

because theta=0 initially. The held orbit average and frequency here are
evaluated at the actual current x,v,h; if the embedding changes h from its
old clamp value, recompute that instantaneous orbit label rather than silently
holding an inapplicable old I fixed. The exact local interaction-energy
change is -B[h(a)-h_c]; metric/controller/boundary preparation costs remain
separate. The earlier clamped work includes its contact once; do not add
that contact a second time to the covariant parent.

## 6. Lowest-cost next calculation

For the three frozen resolution inputs above: solve the first-order initial
metric ODE on two small radial grids, evaluate (3), and compare with (5).
Report original constraints, the unintegrated differentiated constraint,
both endpoint rates, f/N positivity, coefficient signs/minima, K, a_dot and
the same-state energy/action diagnostics. Keep the common state and all signs.
This uses O(radial cells * mode nodes) storage and one scalar radial solve;
it requires neither a new PDE evolution nor a new phase-mean integral study.

This internal test asks whether the actual prepared state can be used
quasistatically after gravity/clock coupling. It can provide a fast positive
compatibility result and still a negative quasistatic result. Either outcome
is more informative than rescaling the saved galaxy velocities by the deep
held-mean coefficient. Shared physical parameters may later be calibrated
and tested in both domains, as Stage2 explicitly permits; this calculation
does not require deriving every constant before making progress, nor does
it grant independently fitted radial state functions the status of a UNT
prediction.
