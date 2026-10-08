# Prospective same-state scalar susceptibility census

2026-09-29. Stdlib arithmetic only. Use ALL 36 unchanged returned-action cases
and their 3,840 mode entries; no new trajectories, quadratures, populations,
galaxy fit, spectral changes or physical-time calibration.

The exact equations are in `FIXED_ACTION_SUSCEPTIBILITY_CONSTRAINT_V001.md`.
For the inherited kappa=u4=m=Lambda=A=1 units, k_j=delta_j² and

    q_j=3(e_j+p_j)/(delta_j^4+4e_j),
    mu_linear=sum weights*q / sum weights,
    chi_j=(1-q_j)/k_j.

The implementation evaluates chi directly, not by subtracting nearly equal
numbers: chi=[k+(e-3p)/k]/(k²+4e). Also reconstruct the second moment using the
INDEPENDENTLY STORED quartic time moment v4, <y²>=(e-3v4)/k, and use the stored
turning amplitude b in chi_alt=(k+<y²>)/(k+b²)². This is a virial reconstruction
from a stored fourth moment, not a previously saved independent second moment
or a fresh numerical differentiation. Retain that distinction.

Authenticate the exact returned-state result (SHA-256
`b8a0efd517e9492aa2546f83eb7cc81bb3a5553e22ff847f5c6f736b545b9678`), its
payload/freeze, all transitive frozen files, and the held-state and phase-mean
wrappers. Read weights/gaps from the exactly corresponding old source case.
The new freeze includes the new script/protocol and settled analytical note.
Do not import or execute inherited scientific scripts.

## Controls and retained outputs

Before the census, evaluate the polynomial variational identity of the note
at k in {.25,1}, u in {.5,1}, b in {0,.1,1,3}, y/b in {0,.3,1}; this is
algebraic substitution, not orbit integration. Check the zero-energy limit.

For every old case retain its gap, duration, source amplitude, time step and
spectral order; all modal q and chi, their ranges, and weighted E, P, P/E and
mu_linear. Check aggregate E/P against the old return, the contact weight,
turning energy, exact q+ k chi=1, q's turning-point bounds, and

    mu_linear >= max(0,3(E-15P)/I0),
    P >= E²/[sqrt(S4+3E)+sqrt(S4)]²,
    I0=sum weights,  S4=sum weights*delta^4.

Use 2e-12 for arithmetic identities and q-range/turning bounds in dimensionless
units; energy identities scale by their positive energy, bounded q and k*chi
identities by one. For checks using the independently stored pressure/quartic
moments retain the OLD 2e-8 energy-normalized tolerance. In particular pressure
may have the old tiny negative rounding residual; never clip it. The chi_alt
check uses |k*(chi-chi_alt)|<=2e-8. No physical success threshold is assigned
to a resulting floor, energy or equation of state.

Retain all 24 matched old-resolution differences in E, P and mu descriptively:
64/.01 versus 128/.01, and 128/.01 versus 128/.005, for each of the 12
gap/duration/amplitude combinations. These differences describe the already
computed preparations; do not require identity between different resolutions
or select one by its favorable response.

`prepared_susceptibility_v001.py freeze` emits a JSON snapshot to stdout for
root publication as `PREPARED_SUSCEPTIBILITY_V001_FROZEN.json`. A no-argument
run verifies that parsed snapshot and emits a result wrapper, all cases,
failures and payload hash. No file is written by the script. Root alone
reviews, freezes, executes and publishes; the author has not run the census.

This is the zero-source, fixed-action, phase-averaged SCALAR response. The
isotropic vector ensemble has additional transverse response and is not
silently assigned this answer. It is not a fresh evolved gravitational law,
an observational coldness test, a native BS matching, or proof that the
stationary clock/metric constraints are satisfied.
