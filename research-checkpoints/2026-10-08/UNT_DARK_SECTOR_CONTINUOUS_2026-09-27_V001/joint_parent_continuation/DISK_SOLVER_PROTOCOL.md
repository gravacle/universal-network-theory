# Prospective axisymmetric field-solver benchmark V001

2026-09-28. Numerical implementation test of the already adopted stationary
modified-Poisson interface, not galaxy data or a new physical law. Retain the
mechanical constitutive law and central r from the frozen prior shape result.
The known Kuzmin solution is an exact oracle, not initial data for the solve.

Units are disk length a=1 and acceleration a0=1. Choose eta=GM/(a²a0) of
.01,1,100, and square half-domains 0<R<8, 0<z<8. Use cell-centred cylindrical
finite volumes with N=32,64,128 on each axis; keep all nine cases. Outer and
top potential boundaries come from the exact disk solution with Phi(s=1)=0.
At the lower face impose its baryonic flux, integrated exactly over each
radial annulus. At R=0 impose regular zero radial flux. No field equation or
numerical tolerance is adjusted after seeing the benchmark outputs.

Normal derivatives use neighbour differences, transverse derivatives use
second-order cell-centred gradients averaged to the face; outer tangential
derivatives are fixed by the exact Dirichlet boundary. Evaluate the full
gradient norm before applying mu, never a radial-component shortcut. Frozen
mu floors at 1e-12 are numerical initialization protection only; require zero
clipped faces at the accepted result. The coefficients for a Picard step
are symmetric positive finite-volume conductances. Solve the linear step by
diagonally preconditioned conjugate gradients, relative residual1e-12,
maximum8N+100 iterations; damp each Picard update by .6. Maximum300 outer
iterations and nonlinear normalized residual1e-9 are convergence criteria,
not a wall-clock termination policy. Preserve a convergence failure intact.
The Picard loop stops only when the declared global flux-balance condition
also passes; a small boundary-normalized residual alone is insufficient.

The initial potential is a scaled Newtonian disk potential, using only the
field-strength scale at s=2, not the exact nonlinear potential. Exact
boundaries are integrated with48-point Gauss quadrature and compared with96;
relative difference tolerance1e-9 (scale=max(1,max absolute boundary)). All
inverse-response evaluations use70-step bisection, and analytical closed-form
mechanical forces are used (the preceding independent quadrature comparisons
are frozen). No physical acceleration is inferred from computer runtime.

At convergence save the grid potential and exact radial prediction. Extract
the disk potential by linear extrapolation from z=h/2,3h/2 and take its
second-order radial derivative. Score the maximum relative radial-force error
on the prospectively selected .5<=R<=4 interval. Require finest-mesh error<.02
and successive refinement reduces that error at each eta. Also require the
global boundary/source flux balance within2e-6 relative, no negative radial
field on the scored interval, and all nonlinear convergence conditions.
The exact finite-domain sheet mass is eta[1−1/sqrt(1+8²)] in the reduced
flux convention (2pi omitted); check it against summed annular flux to1e-13.

Each completed case is saved separately with source/protocol freeze and
payload hashes; a rerun skips only a fully verified completed case. Long
Case publication uses a fully serialized, flushed temporary file and an
atomic no-overwrite link; incomplete temporary files are not accepted cases.
Resume also verifies case identity and the successive-refinement comparison.
future jobs will checkpoint within iterations; these small benchmark cases
can restart from their beginning if interrupted. One numerical worker and
one BLAS thread. Store failures, iteration histories and actual memory/time.
This benchmark does not establish the validity of the adopted galaxy equation,
its cosmological clock dynamics, or agreement with observed galaxies.
