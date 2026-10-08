# Higher precision galaxy tangent check

2026-10-03. Numerical repair of V001, not a changed physical model. Preserve
the V001 script, protocol and unresolved N256 result unchanged. Its first
directional check passed at1e-4 (5.6874e-6 error), then failed at5e-5
(1.1950e-5 versus1e-5). Parameter derivatives and other checks passed.
No tangent was solved. Inverse step-size error growth suggests subtraction
roundoff; it does not establish a correct derivative by itself.

V002 changes only the arithmetic for the two centered FIELD-direction
residual evaluations: form phi +/- step*direction in NumPy longdouble,
before adding the small increment. Retain the same saved input bytes,
double-precision analytic Jacobian, source, field equation, derivative
steps, solver, boundaries, all tolerances and scientific interpretation.
No parameter or error threshold is adjusted. Parameter-direction checks
remain double precision. No software installation is needed.

Every requirement of GALAXY_SATURATION_TANGENT_V001.md still applies.
Publish V002 results separately. If higher arithmetic precision does not
resolve the check, report it unresolved and examine the operator; do not
infer a physical failure or widen tolerance.
