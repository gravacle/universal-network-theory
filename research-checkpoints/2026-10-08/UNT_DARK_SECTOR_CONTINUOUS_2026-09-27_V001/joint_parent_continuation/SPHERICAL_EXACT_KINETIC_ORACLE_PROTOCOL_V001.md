# Prospective closed form shell inertia kernel check

This separately versioned kernel evaluates the same fixed-mass shell kinetic action through its exact rational-polynomial integrals. It changes the integration method, not the mass map, canonical equations, physical force law, masks or tolerances. Its binary64 evaluation still needs numerical testing. No trajectory is implemented or qualified.

The predecessor quadrature packet remains immutable and **not qualified**: its saved result has SHA-256 `bb9810e5d392e2ce7ee3ae3d2bdf48abbe7576bd349c2d2928e77fb332228327`, with 1,905 entries and 35 failed check groups. The completed packet and all 12 case-orders and eight adjacent-order comparisons remain evidence; they are not overwritten or reclassified by a later method. No new result exists at authorship of this prospective protocol.

## New kernel and unchanged equations

`spherical_exact_kinetic_v001.py` has no quadrature function, order parameter or selection branch. It uses the independently symbolically checked formulas in `SPHERICAL_EXACT_INERTIA_DERIVATION_V001.md`, SHA-256 `3a60f43ea5e666e23bac8e478df74f38aeaac77f0cc4a86c15cae593a622a431`. The positive-polynomial matrix entries and factored velocity contraction avoid subtraction of nearly equal shell powers. The constrained-origin contribution remains `3m/5` and has zero free-radius geometric force.

The equations remain `p=A M v=A^2 M xdot`, `K=v^T M v/2`, and kinetic `pdot_j=+v^T(partial_j M)v/2`. Fixed positive masses, input validation, factored positive volumes, unpivoted SPD LDL solve, canonical velocity and energy conventions are unchanged. The harmonic-potential API remains independent of inertia assembly. There is no force multiplier, pivot repair, added pressure, radius clipping, fallback or hidden shell mask.

## Reused independent controls

The new wrapper pins and imports only definitions from the existing oracle source at SHA-256 `a7cd9bfe6026ce2e664a804394009b32e5023d5b9cda43a84844ebd039bd4a66`. Neither its `main` nor its `run` is invoked, and the old quadrature kernel is not imported by this wrapper. Only its fixed `run_case` helper is reused, with its exact Fraction references, independently differentiated rational matrix entries, direct quotient harmonic oracle, exact literal-matrix LDL/conditioning/residual certificates, finite differences, work chain, and unchanged-input controls.

One internal compatibility adapter supplies the single immutable label `closed_form_rational_polynomial_binary64_v001` in the inherited helper's former order argument. It rejects every other value and forwards no order to the new kernel. This label is not a precision setting or exposed runtime knob.

Exactly four cases run once each: the same single-origin shell, uniform mesh, graded mesh and thin-annulus mesh, with the same faces, masses, non-affine velocities, momenta, scale factor, affine rate, radius scales, harmonic test potentials, expansion rate and boundary traction frozen in the predecessor protocol. The wrapper verifies its explicit fixed census and configuration against the pinned helper before numerical work. It does not choose a subset from predecessor outcomes.

Arithmetic tolerance stays `2e-11`, derivative tolerance stays `2e-6`, and the centered fixed-momentum step ladder stays `1e-4, 5e-5, 2.5e-5` times the same adjacent shell widths. All centered and both Richardson estimates remain mandatory. Every existing case control and its normalization are unchanged, including the independent exact and finite-difference nonzero-velocity work chains. Signed comparisons, finite-difference samples, rational conditioning certificates, partial failures and nonfinite evidence are retained.

The only inapplicable controls are repetition under three quadrature orders and comparisons between those orders: the new runtime has one closed form and no quadrature. These controls are not recorded as passes or executed three times under fictitious labels. Their removal is a prospective method change, **not a waiver of the original quadrature failures**. The four cases still test the full closed-form matrix and geometric force against exact rational integrals, rather than checking only the harmonic combination.

## Single bounded execution and scope

Root is the sole runner after complete independent source review. The new source, protocol, kernel, pinned helper and protocol, exact derivation, predecessor kernel, failed result and intent are bound in an exclusive new intent before NumPy, helper or kernel import. Existing intent or result refuses a rerun. Source hashes and bytes are rechecked at completion, including after a retained case failure when possible. No prior files are modified, and bytecode writing is disabled for the new run.

Use the sole project root and all five existing thread controls equal to one. Wall time remains 60 seconds, CPU soft/hard limits 60/65 seconds, self RSS 512 MiB, individual input cap 2 MiB and output cap 8 MiB. The internal alarm is supplemented by root's external wall guard. The wrapper uses only already available NumPy and standard library modules; no build, package installation, subprocess, scientific ancestor execution or remote work occurs.

One exclusive, atomically published, fsynced result retains every attempted case, failed control and caught exception. A resource stop or hard kill is never a pass; a hard kill can leave only the intent. Numerical counts are not independent physical tests. All kernel/trajectory/continuum/full-metric/observation/native-source/Stage-3 promotion fields remain false; all 11 mandatory scientific lanes remain OPEN. A passing four-case oracle would permit considering the separate full-solver integration and its new characteristic, crossing, energy, time, domain and spatial controls, not skipping them.
