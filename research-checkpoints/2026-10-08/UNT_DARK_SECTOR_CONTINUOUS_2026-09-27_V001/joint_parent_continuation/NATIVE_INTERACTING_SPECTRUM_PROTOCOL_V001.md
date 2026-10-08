# Prospective native interacting-incidence spectrum census

2026-09-29. No outcomes seen. The standalone worker is inert until run by the
root's single numerical lane. No propagation, fit, new formation or changed
frozen source is authorized by this protocol.

## Fixed scientific census

Use exactly eight cases: uniform record occupancies q=0,1, each at
h={.5,.025,.0125,.00625}, with all other coefficients inherited and U_d=1.
The two h=.5 cases are the original N=2 microscopic parent. The other six
explicitly changed flip strengths are controlled asymptotic identity checks,
not retuned production parameters. All carriers/writers/reservoirs are blank,
copying off. Keep the occupied-record absolute onsite cost. No U=0 case.

Build the16-state Hamiltonian from degrees/onsite/feedback and the independent
six-state orbit matrix in NATIVE_INTERACTING_COLLECTIVE_MODE_V001.md. The
ten-state orthogonal complement is constructed by twice-reorthogonalized
Gram-Schmidt on the canonical basis, without removing physical states. Check
both Hamiltonian and source intertwining and retain the complement spectra.

Source convention is H-fM, M=sum n. Output all full/bright/dark eigenvalues,
all degenerate-projector source strengths Tr(P_a M P_b M), all corresponding
real projectors, absolute matrices/isometries, and source-moment sum rules.
Real symmetric matrices are serialized by their upper triangles, with a
declared reconstruction convention. No eigenvector-dependent identity is
assigned within a degenerate full-space level.

The main readout is the first-three ORDERED BRIGHT transition-spacing
curvature and the complete bright source-strength ladder. Its sign is an
outcome, not a pass gate or a continuous classical E_II. A bright degeneracy
would stop the simple-level ratio readout rather than choose an eigenvector;
full-space degeneracies are retained normally. Report weak-flip coefficients
and residuals for all cases; only the controlled cases satisfying h<R use
the prederived Cauchy remainder as an upper-bound check. No fitted coefficient.

## Energy and source readouts

Keep the initially blank-link state's exact absolute energy/variance, and the
record-sector difference 4I-M. A passive ground susceptibility is reported
explicitly as a spectral diagnostic, NOT as the actual formed preparation.
Cross-check it through a bordered linear solve for the exact eigenvector
derivative, independent of the spectral sum. For every degenerate cluster
retain its trace second source-energy derivative and its equal-mixture
impulse-work curvature. The latter is <[M,[H,M]]>/hbar^2; a negative excited
moment is not treated as a failure. The Hamiltonian's bare source contact is
zero. There is no new physical source amplitude, evolution or work-free state
preparation.

## Prospective numerical controls

NumPy only, one thread, matrices at most16-by16. All operator, isometry,
normalization and direct identity tolerances are absolute1e-11. Spectral
residuals, grouped projector equations, source moments and independent
susceptibilities use absolute1e-10. Degenerate eigenvalues are grouped if
the entire group lies within1e-10 of its first eigenvalue. Projectors, group
spread and ranks remain in output. Bright-to-dark crossblocks are checked
directly, not inferred from a sampled response.

For control branches use R=g_min/16, g_min=min(kappa,2U), and the rigorous
curvature remainder16R(h/R)^4/[1-(h/R)^2] plus1e-10 floating allowance.
Individual energy remainders use one quarter of this bound. This is analytic
truncation control with separately stated floating tolerance, not interval
arithmetic. Source-entry asymptotic errors and ratios are retained as outcomes;
no desired monotonic convergence or native sign is imposed. The source-ratio
denominator floor is fixed at1e-24, below which the ratio is null, not zero.

All checks and failures are retained. Numerical failure returns exit2;
physics signs do not alter status. Estimated memory is dominated by NumPy's
runtime, not the tiny matrices. The compact JSON payload targets1MiB.

## Publication and custody

`native_interacting_spectrum_v001.py freeze` prints the complete prospective
source snapshot and performs no spectrum calculation. Root publishes it as
NATIVE_INTERACTING_SPECTRUM_V001_FROZEN.json using apply_patch. `run` requires
byte-authenticated matching sources and prints one JSON wrapper with freeze
hash, payload hash, full census, check maxima/counts and failures. The worker
does not create, edit or overwrite any file, and disables bytecode writes.
Root inspects and publishes the result. Source hashes include the independent
analytical review, original BS source and inherited coefficient declaration.
