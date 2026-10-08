# Calibrated physical-field prediction: prospective V001

2026-09-29. Same-state constitutive arithmetic, not a galaxy solution, fit,
new preparation or numerical propagation. Root alone freezes/runs/publishes.
This protocol and worker are inert until that sequential run.

Use the authenticated COMPLETE648-row original-spectrum calibration and all36
returned-action templates. Preserve each of its18 reference alternatives per
template, including identical calibrations carrying distinct historical labels.
The immutable reviewed `fixed_action_finite_field_v001.py` supplies only its
centered `orbit`, cubic and quadrature functions; never call its `run` or reuse
its inherited fixed gs as the new gs. Its complete source/results are authenticated.

For EVERY branch use physical fields g={1e-12,1e-10,1e-8}m/s^2. Compute G=g/g*,
new h=G/sqrt[1+(G/S)^2] and hprime, then solve the unchanged saved actions at
this h. Use64/128-point angle quadrature and the frozen64 radius bisections.
Also solve h=S once for each branch's exact asymptotic coefficient; this is
an orbit limit evaluation, not an infinite external field or new state.
Bit-identical h within a given template can reuse a cached evaluated orbit,
but ALL1944 physical rows and648 saturation rows remain. Origins are shared36
template rows, not unnecessarily repeated orbit calculations.

Qualified controls retain the old2e-8 orbit tolerance and2e-12 arithmetic
tolerance: fixed action, analytic bracket, turning energies, independent
energy-integral action, factorization, virial, energy, action-times-frequency
and mean equation of motion. Compare both angle orders on mean polarization,
excitation, period and D/G. At zero source independently recover every saved
mode's energy, pressure and exact scalar susceptibility, and compare aggregate
origin slope against the already qualified fixed-field result. At each new h
compare the positive cubic relaxed minimum and the exact interval

    0<mean y_I<y_min<h/delta,
    gN_relaxed <= gN_I <= g,
    g[1-(1+(g/gs)^2)^-2] <= gN_I.

Numerical inequalities allow only the same2e-8 scale-normalized arithmetic
error; they are not permissions to clip or change a response. Store signed
gN and signed angle-order difference. The paired positive-mean theorem does
not assert a monotone derivative or allow a stationary PDE substitution.
For tiny lower bounds use the stable expression
g*z*(2+z)/(1+z)^2, z=(g/gs)^2, not subtraction of two nearly equal numbers.

At h=S compute C3=g*^4*S^3*B_I(S)/I0 and its ratio to gs^4, equivalently
B_I(S)/(I0*S). Check0<=ratio<=1 and compare against relaxed polarization.
This asymptotic coefficient is exact within the selected retained state; no
large-g extrapolation or astronomical high-field test is being performed.
The origin slope is independent of g*,S; reconstruct it from the exact same
zero-source modes, not a finite-difference fit at one of the three fields.

Store compact column-labeled arrays for1944 physical rows and648 saturation
rows, all648 branch IDs/scales and36 template IDs/origin controls. Include
full aggregate check counts/maxima and every failure. Full arrays remain in
authenticated ancestors; no modal state is discarded or selected. Target
compact output below1MiB; report an overage without truncating evidence.
Reference metadata stays in the pinned calibration file, with IDs retained.

Every branch is a fixed dimensionless preparation with its own calibrated
dimensional stress scale. Physical inertia/time, isotropic-vector to radial-
scalar state transport and formation are not established. Adiabatic source
work is an energy-difference readout, not a performed trajectory. The full
metric/clock and stationary momentum conditions remain necessary for a galaxy
prediction. No old disk or fixed-gs response is rescaled; no new parameter is
adjusted after seeing these physical-field values.

`freeze` and `run` emit JSON only and never write files. Source authentication
and prospective snapshot equality are required before any orbit calculation.
Small working arrays and cached aggregate readouts are used; no lattice,
matrix propagation, external dataset, SciPy or concurrent worker is needed.
