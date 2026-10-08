# Two shared scales from the unchanged original-spectrum state

2026-09-29. Analytical calibration reduction, not a galaxy fit or a new
cosmological success. The original positive soft spectrum and all36 saved
returned-action templates are retained. The separate high-gap candidate is
NOT used. Read the shared-inference, cosmological-closure, exact-susceptibility
and centered finite-field action notes; no worker or numerical root solve
was run for this derivation.

## 1. Calibrate the same energy and vacuum, not separate amplitudes

At the declared reference scale factor a=1, keep each template's actual
dimensionless actions unchanged. Let its weighted zero-source energy be E>0,
pressure P, and I0=sum w=(1-epsilon^2)/2 for the original A=1 measure.
For its same finite weighted spectrum define

    Q(S)=-sum w emin,delta(S)
        =sum w[delta^2 ys^2/2+3ys^4/4],
    delta^2 ys+ys^3=delta S,  S=gs/g*.                    (1)

The source's absolute high-field matching RULE remains the existing one.
No extra offset or independently fitted excitation normalization is supplied.
The common dimensional stress factor is

    rho_exc=4M^2(g*_SI/c^2)^2 E/(1-epsilon^2),
    rho_vac=4M^2(g*_SI/c^2)^2 Q(S)/(1-epsilon^2).        (2)

Declare the inherited late-flat reference H0,Omega_Lambda and a standard-BBN
omega_b=Omega_b h100^2, with radiation omitted only in this late-time
diagnostic. Set Omega_b=omega_b/(H0/100)^2 and
Omega_exc=1-Omega_Lambda-Omega_b. Then TWO algebraic conditions eliminate
the TWO shared scales:

    g*_SI=c H0 sqrt[3(1-epsilon^2)Omega_exc/(4E)],
    Q(S)=E Omega_Lambda/Omega_exc.                        (3)

H0 in the first line is in inverse seconds. For a positive finite quadrature,
the numerically exact equivalent uses g*_SI=cH0 sqrt[3I0 Omega_exc/(2E)],
with the same I0 used throughout. The original Gaussian weights integrate
I0 exactly in mathematical arithmetic; do not replace a genuinely different
measure by the continuum prefactor without saying so.

This assigns real positive network excitation energy. It does not generate
that energy from an empty homogeneous state, determine its production work,
or erase the associated stress. It is legitimate shared-parameter inference
conditional on that state, not an independently inferred new dust abundance.

## 2. Positive domain and unique vacuum-scale solution

For S>0, the minimum root is unique and positive, and

    Q'(S)=sum w delta ys >0,
    Q(0)=0,
    Q(S)~(3/4)S^(4/3) sum w delta^(4/3) as S->infinity.

Thus any positive finite target on the second line of (3) has one positive
solution. A monotone doubling bracket and bisection suffice; no optimizer or
galaxy residual is needed. The derivative also gives the sensitivity
`dS/dQ=1/Q'(S)` and distinguishes a numerical condition estimate from a fit.

Require H0>0, E>0, Omega_exc>0 and Omega_Lambda>0. E=0 cannot supply a
positive target excitation with finite g*. E>0 with Omega_exc=0 would force
the degenerate g*=0 boundary; negative targets are outside this positive
parent. If E=Omega_exc=0, the scale elimination loses a constraint rather
than defining a zero divided by zero. A zero vacuum target gives S=0, the
boundary of the bounded-source family, not an ordinary positive-gs solution.
These cases must be reported explicitly, never repaired by a hidden offset.

## 3. The small-S relation and its actual cutoff qualifications

Let W_el(S) be the SAME finite-spectrum minimized complete mechanical energy.
Exactly,

    Q(S)=I0 S^2/2-W_el(S),
    d(S)=2W_el(S)/(I0 S^2) in [0,1).

Combining this identity with (3) gives

    gs_SI=cH0 sqrt[3Omega_Lambda/(1-d(S))]
          >=cH0 sqrt(3Omega_Lambda).                     (4)

Thus if d is small, gs approaches a fixed cosmological acceleration scale
even while g* becomes large and S becomes small. The factor3 is not6 or3/2.
This is a consequence of the adopted absolute matching, not a new empirical
coincidence or an independent measurement of acceleration.

The UNIFORM finite-gap series requires S<<epsilon^2:

    Q=I0 S^2/2-(S^4/4)sum w delta^-4
                          +(S^6/2)sum w delta^-8+... .

Small S alone does not justify that series when very soft modes are present.
There are stronger useful collective bounds. For the CONTINUOUS finite band,
positivity and its embedding in the already derived (0,infinity) integral give

    0<=W_el(S)<=pi S^3/16,
    0<=d(S)<=pi S/[4(1-epsilon^2)].                       (5)

This collective bound does not require S<<epsilon^2. For the actual FINITE
positive quadrature, use an exact separate trial bound:

    W_el(S)<=sum w min[S^2/2,S^4/(4delta^4)].             (6)

The two trials are y=0 and y=S/delta. A discrete sum must not be declared
to satisfy the continuum constant (5) without a quadrature-error assessment.
Equation (6), the positive-root expression (1), and the identity defining d
give an inexpensive cutoff-aware check without replacing the retained parent.
When a proved d_bound<1 is available, (4) is bracketed above by
`cH0 sqrt[3Omega_Lambda/(1-d_bound)]`.

## 4. What this immediately predicts beyond present density matching

The ratio w=P/E is UNCHANGED by this calibration. For the same reference
fractions, the late-flat acceleration parameter becomes

    q0=Omega_b/2+Omega_exc(1+3w)/2-Omega_Lambda.

Compared with the inherited dust-plus-vacuum reference its shift is
`Delta q0=3Omega_exc w/2`. Matching present densities therefore does not
automatically match even the first expansion derivative. Earlier evolution
uses the same actual actions and mode equations: under controlled fast-mode
averaging I_j(a)=I_j(1)/a^3, with pressure growing away from the quadratic
regime. Without that time separation use the unaveraged homogeneous parent.
No early-universe, growth or acoustic success follows from (3).

Nor does (3) preserve the old galaxy curve. Its actual scalar source law is

    g_N=g*_SI D_I(G;S), G=g/g*_SI,
    D_I=G-h'_S(G) sum w delta<y>_(I,h_S(G))/I0,
    h_S(G)=G/sqrt[1+(G/S)^2].                             (7)

The fixed-action kernel e(I,h) can be reused, but changing S changes the
map from physical field to h. The ongoing seven-field census at the old S
cannot simply be rescaled into a new calibrated prediction. Its analytic
kernel, source authentication and numerical controls remain useful.

A relaxed continuum illustration shows the structural issue. In the window
epsilon^2<<G<<1 and G<<S,

    D_0(G)≈G^2/a0_dim+2G^3/S^2,
    a0_dim=16I0/(3pi).

For the quadratic term to dominate also requires
`G<<S^2/(2a0_dim)`. A small S can narrow or remove that parametrically
controlled interval above the cutoff. Fixed-action excitation adds its
owned linear contact defect and further finite-field changes; it is not a
separately adjustable cancellation. One must compute (7), not identify
`8g*_SI/(3pi)` with an already observed acceleration scale.

For additional clarity, consider the ordered limiting family E->0 at fixed
positive cutoff, fixed reference fractions and vanishing actual actions.
Then g*->infinity, S->0 and gs approaches (4)'s lower limit. At a FIXED
positive physical field the uniformly harmonic relaxed response tends to

    g_N -> g {1-[1+(g/gs)^2]^-2}.                       (8)

Its small-g behavior is cubic, not the original soft-continuum quadratic
law. The order of cutoff, action and field limits matters. Equation (8) is a
structural illustration, not a substitution for any of the36 finite templates
or a claim that their scalar equilibrium is realized by cosmological formation.

## 5. Parameter count, complete census, and the actual next test

Keep ALL36 returned-action rows: two cutoffs, two pulse durations, three
original amplitudes and the three old numerical-resolution entries. The
resolution entries test convergence; they are not independent physical
populations from which to choose a best fit. Keep ALL18 inherited reference/
BBN alternatives, giving648 conditional calibration rows with no selection.

With each template fixed at a=1, no new abundance zeta is inferred. Equations
(3) remove g* and S as independent choices. The physical inertia/time scale
tau*, the mode phase/orientation and clock initial data, and their formation
history are not fixed. If zeta, a different reference epoch, a modified action
template or spectral cutoff is later inferred, it is an additional counted
state/model choice, and (3) becomes a family rather than one fixed prediction.

The inherited H0/Omega_Lambda reference was already inferred under a
cosmological model. The two baryon alternatives import standard-BBN expansion,
nuclear and primordial-to-present assumptions. They are retained exactly as
documented in `COSMOLOGY_CLOSURE_TEST_V001.md`; this is not a new independent
validation using Pantheon+ or BBN. It is a transparent test target.

After the small calibration arithmetic, evaluate the recalibrated fixed-I
finite-field response and the boundary-determined scalar equilibrium
`N omega_j=mu_j`, with mu_j fixed by the SAME outer state. Keep the full
metric/clock stress and momentum constraints. The scalar calculation does
not automatically transport an isotropic vector cosmological ensemble into
radial scalar actions, and the coherent-annulus compatibility result still
applies to its own distinct initial-data class. This is an original-spectrum
route worth testing, not a license to fit I(r), vacuum, and galaxy response
independently.
