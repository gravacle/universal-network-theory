# Independent result review: a common pulse prepares the high-gap state

2026-09-29. Accepted. The full nonlinear synthetic scalar test does prepare
substantial retained energy with low orbit-averaged pressure and a small
averaged weak-source defect. It does so with one explicit source pulse and
its full paid work, not by assigning the mode population afterward.

## Custody and numerical evidence

Result SHA-256:
`3ff381351716259c36d3ef1cca01431e40a73c3deeabcf0bb24df27696617140`.
Freeze SHA-256:
`1f78119c2b20516e7fa6de9586acd8e58817d489c029f8564982ab4aeb639435`.
Payload SHA-256:
`8e4c812d8a8b84e99a65b492f4899cd263cb6fdd490d9d3f0e7bcf21e788fca1`.

All 20 frozen inputs authenticate. All six cases, 24 integrations and 61,440
integration steps remain represented; all 276 original numerical controls
pass. The largest error/tolerance ratio is 0.22520, without changing a gate.
The producer recorded 3.285752 seconds and 38,273,024 bytes peak self RSS,
not whole-job memory.

`high_gap_pulse_saved_audit_v001.py` and its saved
`HIGH_GAP_PULSE_V001_AUDIT_DATA.json` reproduce 7,713 checks using the saved
states and elementary arithmetic only. They check all 774 fine modal energies,
turning amplitudes, moments, action/period identities and exact susceptibilities;
all control energy/work ledgers; the component totals, coherent polarization,
contact and endpoint; and the old/new relaxed force mixture. Endpoint minima
were reconstructed by independent monotone root bisection. No dynamics or
orbit quadrature was repeated. Largest modal energy/moment discrepancy is
6.61e-16 on its energy scale; the force-mixture absolute discrepancy is
1.78e-15. No defect was found.

## All six outcomes

Numbers below are in the declared dimensionless model units. `mu` is the
zero-source, fixed-action scalar orbit-averaged coefficient, not an evolved
galaxy law.

| Hard gap R | Pulse Hp | Retained E | P/E | mu | Final Bdot |
|---:|---:|---:|---:|---:|---:|
| 32 | 1 | 0.39478784 | 2.82328e-5 | 2.23690e-6 | 2.01063 |
| 32 | 4 | 6.31742827 | 4.50682e-4 | 3.56493e-5 | 8.04207 |
| 64 | 1 | 0.39478441 | 1.76481e-6 | 1.39801e-7 | 4.02124 |
| 64 | 4 | 6.31660539 | 2.82328e-5 | 2.23626e-6 | 16.08502 |
| 128 | 1 | 0.39478419 | 1.10301e-7 | 8.73699e-9 | 8.04248 |
| 128 | 4 | 6.31655049 | 1.76481e-6 | 1.39790e-7 | 32.16992 |

Soft retained energy never exceeds 1.15921e-9. The contact returns to zero;
the retained energy agrees with the integrated source work within the frozen
numerical controls. The matched constant does not pay for that excitation.
The harmonic predictions remain approximate comparisons: the largest observed
hard-energy ratio is 1.000139546, not exactly one.

The new contact is 0.5049995. The finite-window relaxed scale increases from
0.8488255143 to 0.8573137780, and the matched vacuum density ratio is
1.080943713–1.080963942: an approximately **8.095% increase** that must be
included in any later joint inference. The plotted or tabulated relaxed
forces are not the excited-state force.

## What is established, and the next dynamical issue

This is a constructive solution of the preparation subproblem for the named
conditional spectrum: increasing the hard gap stores comparable source-paid
energy with rapidly decreasing averaged pressure and response defect. It
does not yet provide a stationary or phase-mixed gravitating state.

The coherent-motion issue is quantitative. If the final source stays clamped
at zero, each hard mode follows its saved periodic orbit. Its exact contribution
to force-oscillation amplitude is `wH*R*b/Kb`. For Hp=4 this is respectively
0.497414, 0.497662 and 0.497678 at R=32,64,128. The corresponding total soft
amplitude upper bounds are only 5.44e-5, 7.18e-6 and 9.10e-7. Thus the small
instantaneous endpoint force is a phase property; the large-gap oscillation
has not disappeared. Higher gap raises its frequency. These amplitudes are
algebraic consequences of the retained turning points, not a new hold-time
propagation or a prediction for a released metric.

The useful next physical calculation is how the same coherent state couples
to the retained source/clock/metric dynamics, or a specified physical mixing
mechanism. No autonomous source, native high-gap spectrum, cosmological time
calibration, isotropic vector transport, cosmic abundance fit or joint
observational success is claimed by this result.
