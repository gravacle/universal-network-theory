# Full-mode spherical gradient-parent forward test

2026-10-04. Prospective source/protocol only until independent root review.
No galaxy fitting, new constitutive function, or physical-length scan.
This is an actual spatial prediction of the declared changed effective
parent, not an observed galaxy, formation calculation, or cosmology.

## Frozen source and equations

Use the unchanged a0=1.0059833281731022e-10 m/s^2 and GM_sun=1.32712440018e20
m^3/s^2. The inherited illustrative masses are 10^7,10^9,10^11 Msun.
ell=100 pc is the disclosed post-Solar-bound development choice. For each
mass rM=sqrt(GM/a0), choose one Plummer ordinary source b=0.1 rM. The source
profile and scale are declared preparations, not fits or measured galaxies.

Let r=R/rM, lambda=ell/rM, q_s=z_s/a0, u_s=q_s/r and c=gc/a0=3*pi/8.
The complete spherical static equations retained in this worker are

    -lambda^2 (u_s''+4u_s'/r)+u_s+r^2 u_s^3/(c^2 s^4)
        =(r^2+0.1^2)^(-3/2)+mean_u,
    mean_u=integral_0^1 2s u_s ds,
    g/a0=r/(r^2+0.1^2)^(3/2)+r mean_u.

No deep-field or gradient expansion replaces these equations. Uniform
Gauss-Legendre s quadrature, Ns=32 or64, approximates the entire interval
(0,1). The local baseline uses this SAME finite spectrum and positive
radius source, solving its full cubic roots and common scalar flux.
The independent closed continuum local flux is a separate visible spectral
control; it is never substituted into the finite-gradient subtraction.

## Origin, mesh and boundary

The finite-gradient regularity condition is u_s'(0)=0. There is no r=0
unknown and no omitted inner ball. Faces are r_j=0.1*expm1(j*h),
h=log(2001)/Nr, j=0..Nr. Nodes are face midpoints and cell weights are
exact integrals (r_hi^5-r_lo^5)/5 of r^4 dr. The zero inner face conductance
implements regularity. The first node is 0.05*expm1(h), not a fitted rmin.
Interior conductance is r_face^4/(r_right-r_left). The outer Dirichlet
conductance uses the half-cell distance to the actual outer face.

The continuum zero-gradient local u may diverge as r^-1/2 at the center;
we impose NO regular local-u boundary condition and never divide by zero.
The local solution is evaluated independently at every positive node and
is used only as a numerical starting vector and matched baseline. The
regular nonlocal finite-volume equations determine the converged state.

At r_out impose the finite-spectrum local z_s(g_local)/r_out. This is an
approximate large-radius boundary, not an exact exterior solution. Test it
by extending 200 to400 rM while retaining ALL original faces and nodes;
append cells with the same logarithmic spacing and one final shortened
cell if necessary. Readouts stay at r={5,10,20,50}. The Plummer mass tail
is included in the exact source at every radius. This is a finite-mass smooth
source, not compact support; its outer ordinary-mass correction is beyond
the displayed asymptotic R^-2 acceleration term.

## Fixed refinement family and solver

For each mass, serially run (Nr,Ns,r_out)=(129,32,200),(257,32,200),
(257,64,200), and the identical-interior extension of the last case to400.
No outcome-selected grid or source is added.

Newton mode matrices are tridiagonal

    H_s=-lambda^2 L5+I+3r^2 u_s^2/(c^2 s^4).

Use sqrt(cell-volume) similarity to obtain symmetric matrices. For residual
F_s, form ONLY the radius-sized Schur complement and right side:

    S=I-sum w_s H_s^-1,
    S delta_mean=-sum w_s H_s^-1 F_s,
    delta_u_s=H_s^-1(delta_mean-F_s).

Build each modal inverse sequentially, release it after accumulation, and
reuse its tridiagonal factors for recovery. There is no dense (Ns*Nr)^2
matrix in the producer. The sole dense full-block control is a declared
3-mode,7-radius synthetic algebra check. Backtracking reduces the scaled
true residual; maximum32 Newton iterations,20 step halvings each.

True residual normalization is LOCAL:
|diffusion|+|u_s|+|cubic|+|source|+|mean_u|+10^-30. No max(1,global field)
floor is used. The public gate is 10^-9, with a prospectively stricter
internal target10^-12 and final proposed Newton correction in A below10^-4.
This latter control resolves the small high-mass gradient signal. Record
the normalized final residual array, term-scale extrema, raw maximum,
iteration history and proposed correction; a residual-only false pass is
not accepted.

## Readouts and numerical gates

Interpolate the MATCHED NODE DIFFERENCE g_ell-g_local itself linearly in
log r; do not subtract a continuum/interpolated total field afterward.
Primary mechanism readout:

    A(r)=-r^2[(g_ell-g_local)/a0]/lambda^2.

Mesh, spectral and boundary comparisons each require max|delta A|<=0.02
at the four frozen radii. This is a numerical gate, not a requirement that
A be close to1. Save actual A, g_ell, matched local g, exact continuum
local discrepancy, and the asymptotic validity parameters 1/r,lambda^2/r.
The independently derived first-gradient finite-r correction is descriptive
only. Its derivation uses analytic Plummer d',d'', KL and KL'; it is not
used to steer the numerical solve, change gates, or score observed rows.

Controls: exact zero source; lambda=0 matched local equations; closed
continuum versus finite-spectrum local discrepancy (reported, not silently
corrected); manufactured radial-operator refinement; positive tridiagonal
pivots; symmetric Schur; synthetic full-block versus Schur solution<=10^-10;
source identities and forward/inverse cubic checks<=10^-11. Manufactured
operator L5[1/(1+r^2)]=-(10+2r^2)/(1+r^2)^3 is checked away from boundaries,
with fine error<=0.02 and refinement ratio<=0.4 on an independent smooth
control grid. All resource/numerical failures are retained.

## Custody, resources, interpretation

--run is required; no work occurs on import. One NumPy thread, total120s
and256MiB, checked during Schur construction and between cases. Every case,
including a solver failure, writes one exclusive compact checkpoint with
state arrays, source/grid parameters and source/protocol hashes. A single
exclusive completion/partial receipt collects their hashes and gates.
No automatic retry, producer rerun, install or other-account work occurs.

All three masses and all four grids remain in the census. Failure of a
small correction to resolve is numerical incompleteness, not physical
exclusion. A qualified result tests this prepared isolated spherical
configuration only. Finite disk geometry, environment, lensing, dynamics,
native formation, the absolute vacuum budget and the full dark program
are not thereby closed.
