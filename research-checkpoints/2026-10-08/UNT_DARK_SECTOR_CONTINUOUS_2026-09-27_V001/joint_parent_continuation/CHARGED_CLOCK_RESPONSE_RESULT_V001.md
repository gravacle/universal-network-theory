# Evolving network gravity on the charged cosmic background

2026-10-03. The first coupled ordinary-matter, metric, clock and vector
initial-value calculation is complete. The declared small perturbations
produce a large departure from the equally normalized dust reference at
the fixed present inverse wavenumber 136 kpc. The frozen-current reduction
fails its prospective approximation screen. This is a prediction of a
provisional effective model, not evidence of observational superiority or
a nonlinear galaxy solution.

## Completed response and interpretation

The protocol CHARGED_CLOCK_RESPONSE_V001.md fixed the background, all
constants, one Fourier scale, two explicit preparations and numerical
gates before execution. No source mass was injected during evolution,
and no halo, radial clock or vector profile was fitted. The six independent
constrained scalar response columns were propagated alongside the two
specified preparations. The clock's homogeneous abundance remains an
independent calibrated initial charge; its origin is NOT explained away.

All numerical controls passed in 0.641 seconds, peak 34.54 MB, one worker.
The 1024/2048-step normalized checkpoint trajectory difference was
2.571e-8 against the frozen 1e-4 gate; the normalized Einstein-constraint
residual was 4.381e-11 against 1e-6. Matrix/current/trace identities passed,
and the independent EdS growing-mode error was 5.646e-13. Source-only
review independently confirmed the equations, initialization, density-unit
factors and collocation implementation.

| Initial preparation | Final ordinary density contrast | Matched dust reference | Potential ratio to reference | Dropped current time-term ratio |
| --- | ---: | ---: | ---: | ---: |
| Baryon isocurvature at rest | -0.0000243918 | 0.0000290582 | -12.6009 | 0.6295 |
| Adiabatic development case | -0.00153178 | 0.000778982 | -13.6013 | 0.6288 |

Both preparations started with ordinary density contrast +1e-5. Negative
final ratios denote a changed Fourier phase, not a negative power spectrum.
The adiabatic potential changes sign between a=0.237 and 0.316; the baryon
density changes sign between a=0.562 and 0.750 at the saved checkpoints.
Do not call this automatically a fatal instability: propagation, ordinary
growth and additional scalar-mode transients must be distinguished.
It DOES show that the homogeneous near-dust energy bound does not ensure
near-dust perturbation evolution.

The time-term ratio is the prescribed late-interval L2 diagnostic, not a
relative observational error. Both values exceed its 0.1 accuracy screen.
The linear MOND constitutive term is absent about zero spatial gradient;
these results cannot be promoted to a solved flat galaxy rotation curve.

## Scope and review qualifications

The code's `within_conservative_linear_window` means the listed FIRST
ORDER checks at 65 stored checkpoints passed. It is not a proof of the
complete finite-amplitude bounded-Q solution or continuous-time maxima.
The largest first-order rate perturbation divided by the nearest rate
margin is 7.095e-6 and 0.0003024 for the two preparations. Freezing the
phase instead would give 0.008556 and 0.20536. The exact clock response
therefore matters even when all metric potentials are very small.

Review identified the need also to check quadratic kinematic contributions
against the narrow clock margin. For a single real cosine mode, covariant
U_i=partial_i alpha and r=gamma/Q, reconstructing the first-order metric,
phase and vector gives the fractional second-order term

    Q2/Q = (Phi^2/2-Phi*r) cos^2(kx)
           + kphys^2(alpha^2/2+alpha*theta) sin^2(kx).

Its maximum absolute value is the larger absolute coefficient. This
checks unit-vector kinematics, not the missing second-order dynamical
fields. Comparator refinement and dependency hashes are also to be
recorded; the original successful JSON and protocol remain unchanged.

## Fixed diagnostic continuation before execution

To identify the behavior rather than fit it away, keep all model constants
unchanged. Use the saved response, reconstruct the charge-density contrast
delta n/n=F+kappa2 Z/(3W), and separate it from the gradient contribution
to the effective gravitating density. Evaluate the quadratic kinematic
rate bound above at the same saved checkpoints. Independently compare the
dust comparator at 1024 steps with its already saved 2048-step result,
using the same trajectory normalization and 1e-4 numerical gate.

Eliminate the Einstein constraint algebraically and inspect the six-mode
frozen-coefficient matrix at a=0.1, 0.3 and 1, at the original K times
1, 2, 4, 8, 16 and 32. This is a principal-mode diagnostic, not a fitted
new history or observational score. A real growing eigenvalue that scales
with K would demand a gradient-instability investigation; an oscillatory
pair whose frequency scales with K instead identifies a propagating mode.
Finite-K frozen eigenvalues depend on variables/background evolution and
are NOT a substitute for the evolving solution or a ghost-energy test.
No new favorable physical parameters or initial modes may be selected.

Continue into a fixed-band transfer or nonlinear matching test according
to this diagnostic. All eleven program lanes remain open, including the
two distinct CMB questions and native formation. The conventional reference
is equally normalized development physics, not a fresh data likelihood.
