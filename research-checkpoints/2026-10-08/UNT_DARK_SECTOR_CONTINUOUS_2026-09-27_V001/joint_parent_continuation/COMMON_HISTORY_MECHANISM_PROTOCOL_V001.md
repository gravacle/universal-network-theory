# Common-history mechanical test

2026-09-28. Prospective conditional-model calculation. This is not a galaxy
history, a native UNT clock calibration, or a substitution into a gravity PDE.

Test the equations and work/error identities in
`RESPONSE_HISTORY_RADIAL_TEST_V001.md` without using any galaxy residual to
choose a time, a source amplitude, an initial state, or a response phase.
Keep the existing mechanical normalization kappa=u4=A=Lambda=1 and the
bounded source scale from the already sealed `SHAPE_REFERENCE_RESULTS.json`.
Set m=1 to define an explicitly **uncalibrated dimensionless time unit**.

Use final external source amplitudes 0.0025, 0.01, and 0.04 in the existing
mechanical units, with a0_internal=8/(3*pi). These place the force-carrying
gap scales near 0.05, 0.1, 0.2, below the fixed upper cutoff 1. This choice
was made in pre-execution review to test the soft regime, not from a velocity
residual. Use the same C-infinity bump-integral
ramp in the analytical note, durations T=8 and T=16, and post-ramp holds
0, 8, 16 for both durations and every amplitude. Start every mode from rest
at zero source. Retain all 18 observations, regardless of sign. The native
active preparation is not identified with this control state.

Use a positive band [0.001,1] with measure delta*d(delta), and a separately
reported [0.002,1] sensitivity calculation. In each case its own contact is
Kb=(1-delta_min^2)/2. No excluded-mode contact is retained. The two gaps
define different finite-band controls, not a convergence certificate for an
arbitrary excited continuum tail.

Integrate the full nonlinear driven oscillators by fixed-step RK4, carrying
the external work integral as another state variable. Compare (quadrature
order,time step)=(64,0.01),(128,0.01),(128,0.005) for both cutoffs and durations.
The finite-band relaxed state is the unique positive cubic root. Keep the
actual mode coordinates, velocities and integrated work at every stated
observation. Report kinetic energy, complete energy, relaxed energy, excitation,
signed force departure, normalized force, and the exact energy/force bounds.
Evaluate the smooth ramp by Gauss-Legendre integration; compare its 64 and
128 point values. The force/work identities must hold to 2e-7 of Kb*G^2;
cross-resolution sample forces/energies must agree to 2e-6 in the corresponding
G or Kb*G^2 units. Report actual errors as well as pass/fail. Check the relaxed
finite-band force against the already frozen full-band analytic law, with
the gap explicitly retained as a physical difference.

This is a small rerunnable calculation: no new checkpoint framework, runtime
deadline, background service, package installation, galaxy fit, or source
selection. Publish results without overwriting. A failed criterion stays
visible and requires diagnosis rather than changing its threshold.
