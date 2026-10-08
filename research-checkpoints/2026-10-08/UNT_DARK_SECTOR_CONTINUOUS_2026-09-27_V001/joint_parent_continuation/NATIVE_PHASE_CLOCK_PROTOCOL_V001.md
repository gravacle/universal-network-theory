# Native writer-phase clock test: prospective fixed census

2026-09-28. Authorised small saved-state postprocessing. This protocol and
source are frozen before execution; new artifacts have the prefix
native_phase_clock_v001_. No old source or evidence may be edited.

## Inputs and retained scope

Authenticate RECORD_ADDITION_RESULTS.json and RECORD_ADDITION_FROZEN.json
using the literal hashes already used by native_writer_pulse_compute.py;
authenticate their canonical payload/source links. Authenticate
native_writer_pulse_results.json (SHA-256
ca023664cd9798999198ff3999b918a95613798d30ce1d434a318669697c49ea)
and its freeze (SHA-256
9dde274111747690e7cfab23cd6f184ba6a5db6388a00b59f4d658e393564092),
including their payload/source links and complete passing check lists.

Retain native, feedback_off, copying_off in that order, all 16 basis states,
all 12 analytic energy-sector projectors and all 16 adjacent-count lines.
Use each saved formed vector exactly as stored; no preparation is rerun.
Keep the original physical coefficients and hbar=1. The prospective candidate
is A=A_L+A_R and T_phase=continuous phase change/epsilon_r. Neither sign,
phase source, observable nor time window may be selected from the new output.

## Fixed comparisons and decision

The output-age census is exactly 0,.25,.5,1,2. At those ages compare analytic
line sums against full original-matrix eigensolver and independent inherited
scaled-Taylor evaluation, and against saved pulse K,Y. Check the exact
commutator a_dot=i(epsilon_r*a-lambda_R*z), the amplitude derivative,
projector resolution/orthogonality/eigenvalues, every allowed coefficient,
and no unsupported matrix block. Inherited crosscheck tolerance is 1e-11.

For the continuous SAME interval [0,2], retain both endpoint grids with 512
and 1024 intervals. Apply exactly the coefficient-based Lipschitz bounds and
eta=1e-10 allowance in NATIVE_PHASE_CLOCK_CANDIDATE_V001.md. Positive/negative
orientation is stated only when the whole-window amplitude and numerator
bounds certify it. Otherwise report unresolved, not an adjusted phase.
Copying-off is the analytically zero-amplitude control, not a numerical phase.
Feedback-off must independently reproduce constant amplitude and rate +1.
Record a safely unwrapped phase only after the no-hidden-winding check.

The bounds are exact arithmetic inequalities with a declared numerical
allowance; they are not directed-rounding interval arithmetic. Numerical
method agreement is reported separately from the scientific sign decision.
A negative or unresolved native scientific result is not a computational
failure and must be published with all controls.

## Execution and publication

One process, one numerical thread, 16x16 matrices and at most 1025x16 line
phases. No long calculation, checkpoint, environment installation or physical
source change. Atomically publish a new freeze and new result without
overwriting old files. Record all checks, coefficients, both bounds, inherited
age rows, payload hash, source identities, timing and peak self RSS. Parent
and independent audit review the saved result before a scientific report.
