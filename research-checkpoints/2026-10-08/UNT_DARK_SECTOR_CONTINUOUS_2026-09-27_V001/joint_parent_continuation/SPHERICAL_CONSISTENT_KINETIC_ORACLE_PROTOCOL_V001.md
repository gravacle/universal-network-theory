# Prospective consistent shell kinetic kernel oracle

This packet tests only the unchanged inert `spherical_consistent_kinetic_v001.py` kernel. It does not integrate a trajectory, modify its solver or force laws, or replace its quadrature by the new exact expressions. Root is the sole numerical runner after independent source review. Every numerical result is still prospective at authorship.

## Owned evidence and independent analytic reference

The kernel is pinned at SHA-256 `c1b0c4268071687ebca7949e20a5d05df9750ed41e5cb601e03228b6bd488e0e`. The repair proposal, original two-current result audit and frontier V067 remain immutable. The exact-inertia derivation is pinned at `3a60f43ea5e666e23bac8e478df74f38aeaac77f0cc4a86c15cae593a622a431`.

The oracle author independently checked the symbolic derivation, not a numerical output. Substitution `ds = 3r^2 dr/(R^3-L^3)` yields the three elementary shell integrals. Their numerator polynomials factor by `(1-q)^3`, with `q=L/R`, giving the three rational entries in the exact-inertia note. Quotient differentiation reproduces all three radius derivative polynomials; expanding its factored velocity contraction gives `F_LL' vL^2 + 2 F_LR' vL vR + F_RR' vR^2`. This is independent symbolic review, not numerical reproduction or a new runtime kernel.

The prospective oracle uses Python `Fraction` arithmetic on the exact binary64 input values to assemble the closed-form matrix. It differentiates the rational entry polynomials by the quotient rule, rather than copying the kernel's Jacobian/quadrature derivatives. An independently evaluated harmonic potential and gradient use direct differentiation of `(3/5)(R^5-L^5)/(R^3-L^3)` with exact rational differences. Exact arithmetic prevents thin-shell cancellation in these references. The origin contribution is separately `3m/5`, independent of the free radius.

## Fixed census and numerical criteria

Four dimensionless positive meshes are frozen. Masses are fixed shell masses, not regenerated when radii are perturbed.

| Case | Faces including constrained origin | Fixed masses | Free-face peculiar velocity | Free-face canonical momentum |
| --- | --- | --- | --- | --- |
| Single origin shell | 0, 1.25 | 0.7 | 0.37 | 0.23 |
| Uniform | 0, 0.5, 1, 1.5, 2 | 0.7, 1.1, 0.9, 1.3 | 0.17, -0.11, 0.23, -0.07 | 0.29, -0.13, 0.19, -0.17 |
| Graded | 0, 0.125, 0.5, 1.25, 2 | same four masses | same four velocities | same four momenta |
| Thin annuli | 0, 1, 1+1/1024, 1+2/1024, 1+4/1024 | same four masses | same four velocities | same four momenta |

Every case is evaluated at all three existing orders 16, 32 and 64. The scale factor is 1.3, the affine-velocity coefficient is 0.19, and radius scaling factors are 0.5 and 2. All order results and all adjacent-order differences are saved. No preferred order or successful subset is selected after execution.

Arithmetic tolerance remains `2e-11`; derivative tolerance remains `2e-6`. Dimensionless comparisons use `max(1, |left|, |right|)` after the declared normalization. With total mass `Mtot` and outer radius `Lmax`, compare matrix entries as `M/Mtot`, kinetic energy as `K/Mtot`, geometric force as `g/(Mtot/Lmax)`, harmonic gradient as `grad V/(Mtot Lmax)`, harmonic potential as `V/(Mtot Lmax^2)`, acceleration as `acceleration/Lmax`, and work rates per `Mtot`. Velocities use the fixed unit velocity. Volumes are compared relative to their independent positive cell volumes; input immutability has zero tolerance. No tiny-mass suppression, clipping, jitter, out-of-domain extrapolation or fallback is permitted. Every order's matrix and force are compared with the exact integral reference at the arithmetic criterion; a quadrature miss remains a failure, even if another order succeeds. Adjacent-order comparisons use the same arithmetic criterion and do not replace the exact reference.

Checks comprise:

1. Exact origin inertia and zero origin-shell geometric force; positive finite factored volumes; independent matrix and non-affine geometric-force references; separate versus combined kernel APIs and unchanged inputs.
2. Symmetry and independent matrix-vector multiplication. Exact rational LDL of each small assembled binary64 matrix must have positive pivots. Its exact inverse infinity norm and condition number are retained. The kernel's fixed-momentum solve has an exact rational residual, giving the bound `||error||inf <= ||M^-1||inf ||residual||inf`. Its relative residual and relative forward bound must each be at most `2e-11`. These are certificates for the literal assembled matrix, not for the uncomputed continuum integral.
3. Radius-scale invariance of inertia, inverse-length scaling of geometric force, `x dot geometric_force = 0`, affine geometric-force null, and the independent harmonic identity `gradient = kappa M x`. Harmonic acceleration recovered by the kernel solve must equal `-kappa x`, including the first face. `kappa=1.7` is fixed.
4. Canonical velocity, kinetic energy and geometric force against exact references. At fixed momentum and scale factor, each free radius is perturbed by `epsilon` times its smaller adjacent width (the only width for the outer face), with `epsilon = 1e-4, 5e-5, 2.5e-5`. Every centered derivative and both adjacent Richardson estimates are retained and tested against `partial_x Hkin = -geometric_force` at `2e-6`; no step is selected by its outcome.
5. A nonzero-velocity instantaneous work chain with declared test potentials, not a physical trajectory. Set `U` to the harmonic potential with coefficient 0.7, `W` with coefficient -0.4, expansion rate 0.07, and traction 0.03 on the outer face only. Use `pdot = geometric_force - grad U - grad W/A + traction`. Compare the kinetic-plus-potential chain with `traction dot xdot - 2 H K - H W/A`, first using the independent exact kinetic gradient at arithmetic tolerance, then every saved centered and Richardson gradient at derivative tolerance. Individual cancelling terms are saved; zero velocity cannot make the test vacuous.

The finite-difference steps are restricted analytically by positive shell widths, not by successful output. They do not evolve states, measure convergence of a trajectory, or establish interval positivity. Conditioning certificates do not waive quadrature, derivative or work failures.

## Custody and bounded execution

The new source and protocol, all pinned evidence, the fixed census, criteria and limits are recorded in an exclusive intent before importing the kernel or evaluating numerical cases. Root invokes the source once from the sole project root with all OpenBLAS, OMP, MKL, Accelerate and NumExpr thread controls set to one. Only the already available NumPy and standard library are used. There is no installation, subprocess, compiler, remote job or full solver import.

The wall limit is 60 seconds, CPU soft/hard limits 60/65 seconds, self RSS limit 512 MiB, input cap 2 MiB, and output cap 8 MiB. An internal alarm and root's external wall guard bound execution. Checks retain all signed values and failures. Per-case exceptions retain the fixed case/order context and accumulated partial records; resource or custody failure stops further cases. Nonfinite floats are represented losslessly by their binary64 hexadecimal bytes and labeled display, never replaced by a passing zero. Source/input hashes are rechecked at the end.

The fixed intent and one result are published exclusively and atomically with fsync. Existing output or intent refuses a rerun. A hard kill may leave only the intent and is not a pass. The output reports numerical controls separately from physical scope; every kernel/trajectory/continuum/metric/observational/Stage-3 qualification remains false. The old two-current evidence, its regular-origin defect, all 11 open scientific lanes and all source/formation debts remain unchanged.
