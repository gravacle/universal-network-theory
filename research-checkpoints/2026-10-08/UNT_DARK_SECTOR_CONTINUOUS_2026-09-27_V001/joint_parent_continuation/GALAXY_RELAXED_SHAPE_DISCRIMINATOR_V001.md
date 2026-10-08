# A relaxed-force shape discriminator, without a cosmological completion

2026-10-04. Source-only algebra from the existing relaxed law. No new fit, numerical experiment, response function, timescale or cosmological branch is introduced. This is an operational consequence of the already saved low-field curvature, not a new microscopic derivation.

## Low-field shape versus empirical RAR

Use x=g/a0, d=g_bar/a0, and A_I=8/(3 pi). The exact closed flux in `disk_solver.py` and the inherited relaxed-parent derivation give

    d=f(x)=x^2+b x^3+O(x^4),
    b=2/r^2-64/(9 pi^2),
    x_network=sqrt(d)-(b/2)d+O(d^(3/2)).

The empirical RAR comparison used in the saved calculations is

    x_RAR=d/[1-exp(-sqrt(d))]
         =sqrt(d)+d/2+d^(3/2)/12+O(d^(5/2)).

At the SAME a0,

    v_network/v_RAR-1=-(1+b)sqrt(d)/4+O(d).

Because b>-64/(9 pi^2)>-1 for every finite positive r, the leading network correction is smaller than the RAR correction. No choice of r identifies these two exact low-field expansions. This distinguishes functions; it does not reject the measured RAR data, whose source/geometry uncertainties are separate.

The actual saved comparisons calibrated a0 separately. Their leading deep-field velocity ratio includes `(a0_network/a0_RAR)^(1/4)`, and more explicitly

    v_network/v_RAR = (a0_network/a0_RAR)^(1/4)
       *[1-(b/4)sqrt(g_bar/a0_network)
           -(1/4)sqrt(g_bar/a0_RAR)+O(g_bar/a0)].

Their saved typical separation must not be called a matched-a0 shape test. The radial audit finds median absolute outer velocity separation 0.73663%, maximum 3.68666%, and no primary-score advantage over RAR. Fixed source conventions and the adopted radial closure leave this small separation insufficiently isolated from nuisance/geometry effects.

## One observable that removes the leading normalization intercept

For an isolated compact spherical baryonic source of independently known total mass M, define r_star=sqrt(G M/a0). In the relaxed monopole regime, with R much larger than both the source and r_star,

    v_network^2(R)=sqrt(G M a0)-(b/2)G M/R
                   +O[sqrt(G M a0)(r_star/R)^2],
    v_RAR^2(R)=sqrt(G M a0)+G M/(2R)
                   +O[sqrt(G M a0)(r_star/R)^2].

For two comparable large radii, scaled outward together, the directly measurable shape statistic

    C12=[v_c^2(R1)-v_c^2(R2)]/[G M(1/R1-1/R2)]

tends to

    C12_network=32/(9 pi^2)-1/r^2,
    C12_RAR=1/2.

The leading a0-dependent constant cancels. Separate recalibration of a0 therefore cannot absorb this first nonconstant term. The network coefficient is bounded above by 32/(9 pi^2), independent of its inherited saturation calibration.

This is the proposed single shape discriminator, not another overall RMS ranking. Practical use requires an independently constrained baryonic mass, adequately compact source, verified geometry, circular-motion interpretation, and an isolated-field window before external fields or surrounding structure dominate. A full nonlinear disk field is not automatically equivalent to applying the algebraic relation to its radial baryonic component. Finite-radius terms and source multipoles must be controlled rather than fitted away. Existing exposed SPARC data would remain development evidence if used to estimate this statistic.

## High-field saturation is also analytically different

In internal units, h(g_I)=g_I/sqrt[1+(g_I/g_s)^2], g_I=A_I x and g_s=A_I r. With P_s=P(g_s)>0, the exact flux can be written

    f(x)=x-2 P[h(A_I x)] h'(A_I x)/A_I.

At fixed finite r and x>>r,

    f(x)=x-C_r/x^3+O(x^-5),
    C_r=2 r^3 P_s/A_I>0,
    mu=1-C_r/x^4+O(x^-6),
    g-g_bar=a0 C_r/d^3+O(a0 d^-5).

RAR instead gives `g-g_bar ~ a0 d exp(-sqrt(d))`. Thus the parent has an algebraic saturation tail rather than an exponential one; eventually its residual exceeds RAR's, although both vanish. This asymptotic requires acceleration far beyond r a0 and is not a claim about an arbitrary high-brightness galaxy, external-field configuration or dynamical source. No high-field observational score is computed here.

## A history signature is not yet calibrated in physical seconds

`RESPONSE_HISTORY_RADIAL_TEST_V001.md` already provides a conditional mechanical memory model. For constant mode inertia,

    m(delta) y_ddot+kappa delta^2 y+u4 y^3=kappa delta h[g(t)],
    omega_h^2=sqrt(kappa u4)h/m,
    G_T=m/[sqrt(kappa u4) T^2]

in the stated low-field continuum control regime. That gives a common-history amplitude/rate scaling once the inertia, physical source history, state and time conversion are independently fixed. It does not provide them from a0 and r.

In particular, multiplying all inertias by lambda^2 leaves every relaxed force prediction unchanged while multiplying response times by lambda. The static calibration therefore cannot determine a unique lag in seconds; forming the dimensional combination c/a0 is not an identification of a native pole or clock. Even the source-dependent exponent changes for a different inertia spectrum. The existing conservative parent can ring, overshoot and reverse a clamped response, so older does not automatically mean more relaxed and no monotonic lag function is licensed.

Required missing input is the native source/clock/inertia and actual-state mapping, followed by the complete constrained gravitational response. None of the failed cosmological completions supplies that mapping. The present shape test concerns the static effective law only and leaves the full program's formation, gravity, cosmology and clock questions open.

Sources read: `disk_solver.py`; `SHARED_GEOMETRY_PREDICTION_V001.md` (static curvature only, not adoption of its failed action); `SPARC_EFFECTIVE_TRANSFER_V001_RESULT.md`; `GALAXY_RADIAL_TRANSFER_V001_AUDIT.md`; and `RESPONSE_HISTORY_RADIAL_TEST_V001.md`. No files underlying those results were changed.
