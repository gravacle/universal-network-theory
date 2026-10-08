# Prepared annulus initial-release census: prospective protocol V001

2026-09-29. The worker is inert until the parent reviews it, captures its
`freeze` JSON, publishes that freeze with `apply_patch`, and runs the sole
numerical process. It writes no files. Its `run` JSON is likewise published
by the parent without overwriting earlier evidence. No long-time field or
mode propagation, fit, rephasing or physical inertia calibration is performed.

## Parent, baseline and complete input census

Use `EXPLICIT_MODE_COSMOLOGY_PATHWAY.md`, the full spherical reduction and
`UNIFORM_PREPARED_ANNULUS_RELEASE_V001.md`. Authenticate the original common-
history result, its canonical payload, freeze and transitive source hashes.
Keep cases 0,1,2 and observation 0: gap=.001, duration=8, hold=0, g=.0025,
orders/dt=(64,.01),(128,.01),(128,.005). Retain every saved delta, weight,
position and SIGNED velocity; do not replace any state by its minimum.

Preserve the inherited high-source endpoint matching RULE in the actual
finite parent. With the unchanged gs from the authenticated source, solve
`y_s³+delta²*y_s=delta*gs` and set

    DeltaU=sum w[delta²*y_s²/2+3*y_s⁴/4],
    Kb=sum w, C=2/Kb, Lambda=2DeltaU/Kb, M²=1.

This is exactly `Kb*gs²/2-W_el(gs)` for the same retained weights, not a
new fitted offset. The three quadrature/regulator-dependent values remain
separate. Record continuum full-band and [.001,1] endpoints as contrasts
using independent 96/192-point quadrature after delta=z³; do NOT insert
the full-band value into a finite-band action while calling J(infinity)=0.
Verify the cubic roots by 96 bisections and the positive versus complete-
energy endpoint identity. No baseline is zeroed and no prepared energy is
subtracted from the gravitating parent.

For each saved state retain both r_in=1/4096 and1/8192, r_out=2r_in,
N=exp[g_c(r-r_out)], g_c=.0025, rho_b=0 and inner GM_b=g_c*r_in².
These are conditional diagnostic embeddings, not galaxy measurements.
Initial R=r, p_L=p_R=0, beta=0, chi'=0, with uniform PHYSICAL x,v.
The inner metric is `f_in=1-2g_c*r_in-Lambda*r_in²/3`.

## Stable metric and release calculation

At x=r/r_in in[1,2], evolve u=(1-f)/r_in rather than subtracting two nearly
equal metric values. Set a=g_c sqrt(f), E=E0+DeltaU-Bh+aBh', and solve

    u_x=[-u/x+C*r_in*x*E+2C*sqrt(f)*B*h']
              /[1+C*r_in*x*B*h''*g_c/2],
    u(1)=2g_c+Lambda*r_in/3, f=1-r_in*u.

Use RK4 on both64 and128 cells and, independently for each, half-step
refinement. A Schwarzschild-plus-Lambda initial constraint with B=E0=0
has the exact control `u=2g_c/x+Lambda*r_in*x²/3`; it is only a metric-
constraint control, not an assertion of an accelerated-clock null release.

For the full prepared state use scaled fluxes

    d=N*x²*B*h''sqrt(f), a_flux=N²*x²*V_B*h',
    ktilde=integral(a_flux/d)dx / integral(1/d)dx,
    eta_r=(ktilde-a_flux)/d, eta=r_in integral eta_r dx.

Composite Simpson quadrature uses two half-cell panels per metric cell,
with cubic-Hermite metric quarter-point and midpoint values. This prospective
choice reduces the known weak-oracle quadrature error sixteen-fold compared
with one panel per cell; it does not change either metric grid or tolerance.
An independent four-point Gauss rule per cell uses the SAME metric
interpolation: it checks quadrature, not independent metric integration.
Half-step RK4 and its own quadratures provide the metric-resolution test.
No density/clock pinning or new gradient is introduced if a denominator
vanishes. Preserve a domain failure rather than modifying the initial state.

Report eta at BOTH endpoints, exact source rates
`a_dot=sqrt(f)*eta_r` and `D h=h'*sqrt(f)*eta_r/N`, the original constraint,
and the unintegrated differentiated constraint. Seven-point centered finite
differences use interior nodes3..n-3 for the metric equation, and6..n-6
for the reconstructed release flux derivative. Endpoint values are not
deleted: all boundary rates, eta values, positivity and fluxes remain in
the output; only these finite-difference stencils exclude boundary nodes.

## Fixed numerical gates and non-gates

Before outcomes, use input/root/algebra tolerance2e-11; absolute u half-step
agreement2e-9; quadrature and clock-rate comparisons2e-7; primary endpoint
eta absolute2e-11 and independent-Gauss endpoint eta absolute2e-7.
Clock-rate differences use the fixed input scale

    S=max(1,abs[V_B*h'(g_c)/(B*h''(g_c))]),

never a pointwise rate that crosses zero. Save absolute differences too.
The metric FD residual is divided by the input scale
`S_u=abs(u_in)+2C abs(B)+C*r_in*(abs(E0)+DeltaU)` and must be<=2e-6.
The release-flux FD residual is divided by `max(2abs(V_B),1e-30)` and
must be<=2e-5. These check discretization, not physical quasistatic success.
Require f,N positive, the metric denominator nonzero, and B*h'' fixed
negative sign for the stated invertible release branch. Preserve violations.

Weak-field-oracle differences, the signs and sizes of the source rates,
and their relation to mode frequencies are SCIENTIFIC OUTPUTS, not pass
conditions. The instantaneous local-curvature frequencies
sqrt(delta²+3y²) are labeled as such, not claimed to equal nonlinear held
orbit frequencies. No numerical action drift is computed; the analytic
identity remains available, but this census does not qualify action evolution.

Compare 64/.01 against 128/.01 as the preparation quadrature control, and
128/.01 against 128/.005 as the preparation step-size control. Do not call
64/.01 versus 128/.005 a purely spectral comparison. Small eta alone is
not quasistaticity: retain its physical radial derivative and source rate,
which can stay large as the annulus shrinks.

Retain E0, kinetic/quadratic/quartic components, old clamp work/energy,
local interaction change -B[h(a)-h_c], full mode density including source
and divergence terms, both geometric mass functions and all radial rates.
`GM_geom=r(1-f)/2` and its Lambda-subtracted value are finite-slice
geometric quantities, not ADM energy or a new dark-matter rest population.
The scalar constraint flux is not labeled an energy luminosity.
