# Linear-source parent: galaxy reference and finite-gradient asymptotic

2026-10-04. Prospective source-only protocol. The old bounded-source Solar
failures and galaxy scores are retained. This is a changed h(g)=g parent,
with J_delta=kappa*delta^2*ell^2. The illustrative ell=100 pc is explicitly
chosen during development after inspecting the Solar-bound work; it is not
a blinded prediction or a claimed Solar pass. The old a0=1.0059833281731022e-10
m/s^2 is adopted unchanged, not recalibrated to this new parent.

## Exact zero-gradient constitutive reference

Put x=g/a0, h=(8/3pi)x, t+t^3=h, theta=atan(1/t), and

    B(theta)=3theta/2-sin(2theta)/2-sin(4theta)/8,
    f_infinity(x)=h^2 B(theta) / [2*(8/3pi)].

In a spherical zero-gradient configuration gN/a0=f_infinity(g/a0).
Equivalently mu=gN/g=integral_0^1 2s t_s^2/(1+t_s^2) ds with
t_s+t_s^3=g/(gc*s^2), gc=3*pi*a0/8. This is the unbounded-source limit,
not an arbitrary MOND interpolation. It has

    mu(x)=x-[64/(9pi^2)]x^2+O(x^3),
    f_infinity(x)/x -> 1 at high x,

and retains the previously identified slow high-acceleration relaxed
deficit. Finite-gradient physics, not this reference limit, was proposed
to change the small-system response.

The scalar radial relation applied to a disk catalogue is an explicitly
adopted local algebraic proxy. It is not the solution of the nonlinear disk
field equations, and ell does not occur in this calculation. A good score
therefore cannot validate ell=100 pc; a bad score is not automatically a
failure of the nonlocal disk solution. This inexpensive check asks whether
the changed local shape transfers at the inherited a0 without a new fit.

## A separate same-parent finite-gradient prediction

For an isolated spherical source the exact equations are

    -ell^2 Delta_1 z_s+z_s+z_s^3/(gc^2*s^4)=g,
    g=gN+integral_0^1 2s z_s ds,
    Delta_1 z=z''+2z'/R-2z/R^2.

Let z_s^0 be the local solution for g0, and A_s=1+3t_s^2. The first
finite-gradient correction, before any observational substitution, is

    delta_g=ell^2 [integral 2s (Delta_1 z_s^0)/A_s ds]
                    /[1-integral 2s/A_s ds].

The vector term -2z/R^2 cannot be omitted. In the isolated deep exterior
g0~sqrt(GMa0)/R, the weighted hard-mode contribution tends to
-2g0/R^2, while the denominator tends to 2g0/a0. Hence, with
beta=32/(9pi^2),

    g=sqrt(GMa0)/R + [beta*GM-a0*ell^2]/R^2 + o(R^-2),
    v_c^2=sqrt(GMa0)+[beta*GM-a0*ell^2]/R+o(R^-1).

The approach to the flat asymptote changes sign at

    Mcrit=a0*ell^2/(beta*G).

The worker reports Mcrit/Msun using the inherited GM_sun, without inventing
galaxy total masses. It does not score this asymptotic against disk rows.
Control parameters are rM/R<<1 and ell^2/(rM*R)<<1, rM=sqrt(GM/a0),
plus a radius exterior to the actual ordinary source, negligible external
field compared with g0, and a settled static response. Finite source
multipoles, extended gas, disk geometry, preparation history and external
fields remain separate obligations. This is an asymptotic prediction, not
a finite-radius error certificate; cancellation near Mcrit makes neglected
terms especially important. No claim is made that fixed-N/count volume or
native network formation has derived this effective geometry.

## Frozen data and scoring

Read GALAXY_RADIAL_TRANSFER_V001_RESULT.json and authenticate every case
against its saved case_sha256. Reuse all 100 evaluation-galaxy receipts,
their exact row order and stored inner/outer masks. The same six n<6
exclusions remain; all 94 eligible galaxies are retained. All prior SPARC
data exposure remains disclosed. No old producer is imported or rerun.

For each positive saved gbar_si, invert the NEW f_infinity with 72 and 88
bisections; convert g to km/s with the saved R_kpc. The fixed M/L, signed
gas source, distances, inclinations and quoted velocity errors are reused
unchanged from the saved rows. No inner or outer velocity enters the new
prediction. There are zero new per-galaxy or global fits in this screen.

Primary readout: galaxy-balanced OUTER velocity MSE; secondary: OUTER
log10-acceleration MSE. Save all new full-radius predictions and signed
residuals, per-galaxy paired differences against the saved baryon, bounded
network, RAR, NFW_513 and ISO_513 predictions, and all original exclusions.
Reference scores are recomputed only from saved predictions, not refitted.
No sample filtering, loss-based model selection, new bootstrap, or
observational pass threshold is introduced. Neither this screen nor the
earlier radial comparison establishes superiority over full LCDM.

## Arithmetic controls and limits

The small-theta B series is fixed analytically through n=12. Independently
verify B(theta)=integral_0^theta 2sin^2(u)[3-2sin^2(u)]du using 32/64-node
positive quadrature over x=10^-12..10^12. Relative flux agreement <=1e-11;
inverse residual and 72/88 prediction agreement <=1e-11. Check positivity,
monotonicity, the deep asymptote at x=10^-8 to 1e-6, source/SI readout
identities and saved-reference metric reconstruction to 1e-10 scaled.
The synthetic inverse takes only gbar; changing observed velocities cannot
change it. All input/source/protocol hashes and numerical failures are
retained in one exclusive result, with --run required. One NumPy thread,
120 seconds and 256 MiB; no worker is run while authoring this protocol.

The finite-gradient coefficient and Mcrit are saved separately from scores.
No score is labelled a finite-100-pc prediction. Removing the bounded source
also removes the old finite-endpoint vacuum relation; shared cosmology and
all mandatory dark-program lanes remain open.
