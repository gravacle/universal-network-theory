# Prospective native photon-source diagnostic

2026-09-29. New conditional photon-probe coupling, unchanged native parent.
This tests necessary microscopic ingredients for the CMB pathway, not measured
photons, a continuum thermal bath or an observational CMB fit.

Use the original authenticated 16-state held Hamiltonians and saved native,
feedback-off and copying-off preparations in RECORD_ADDITION_RESULTS.json.
No new native state, ground-state replacement or retuned parameter is allowed.
The separate external weak probe adopts H_photon=omega*a†a and
H_int=eta*B*(a+a†), with hbar=1 in owned microscopic units. Test B=n and
B=R=QL+QR. The physical photon dictionary and this coupling are additional
conditional premises, not derived native electrodynamics.

For each saved state, retain ages {0,0.5,2}; probe durations {0.25,1,2};
frequencies {0.75,1.5,3}; and both operators. Total census: 162 rows.
Compute the exact leading-order finite-time occupation coefficients

    F_±(omega,t)=integral_0^t exp(±i omega s) B_I(s) ds,
    E=||F_+ psi||^2, A=||F_- psi||^2.

For an initially empty photon mode, P(0→1)=eta² E+O(eta⁴); for an initially
single-occupied mode, P(1→0)=eta² A+O(eta⁴). This is a perturbative probe
diagnostic, not a large-time irreversible rate. Finite-duration switching and
counter-rotating contributions are retained, not called free thermal radiation.

Compute F exactly in the native energy basis, using its continuous zero-
denominator limit. Independently integrate it with 32-node Gauss–Legendre
quadrature using scaled-Taylor native propagators, not the energy eigenvectors.
Check both operators and both signs, all states, ages, frequencies and times.
Use absolute 1e-9 numerical consistency tolerance; preserve every outcome.

Also compute the energy-dephased stationary comparator, preserving whole
degenerate eigenspaces. This is an explicitly separate diagnostic, not a
substitution for the actual coherent native state. Report the full/dephased
finite-time difference. For n, derive each spectral line's nonnegative
absorption/emission weight both from the exact R,s projectors and independently
from grouped numerical eigenspaces. For each occupied positive-frequency pair,
report beta_eff=log(W_abs/W_emit)/omega where finite; do not fit a common
temperature or score cosmological acceptance from it.

Expected positive operator gaps at lambda_R=1/2 are sqrt(k)/4 with
k={73,89,113,145,185}. At lambda_R=0 they are sqrt(113)/4 and sqrt(185)/4.
Population support may be smaller: copying-off has R=0. Verify all support
without silently dropping an allowed unoccupied line. Check line sums against
Tr(rho_dephased B²), the first frequency moment against
Tr(rho_dephased [B,[H,B]]), and invariance of stationary weights with age.
For R, [H,R]=0 implies zero nonzero-frequency support and exactly
E=A=|integral exp(i omega s) ds|² <R²>, a bounded switching response.

Root runs the only numerical worker. Maximum matrices are 16 by 16; no new
packages, long-lived processes, infrastructure or custom small-job checkpoint
machinery. The worker emits raw JSON to stdout, with source/input hashes,
complete census, failures, runtime and self RSS. No frozen old file is edited.
An independent review checks the numerical evidence and physical interpretation.
