# Isolated-bound numerical control repair

2026-10-05 UTC. V001 result and source remain untouched. Its closed-form
kernel control at x=.01 failed: relative discrepancy 3.2866312011e-10 versus
the frozen 2e-10 tolerance. All other 22 controls passed. The result rows
do not depend on this numerical kernel value; they use the analytic bound.
Nevertheless the failure must not be relabeled as a passing original run.

Diagnosis: the expression `1+2*((1+x)*exp(-x)-1)/x²` cancels twice at small
x. The independent quadrature used positive `-expm1(-xu)` and agreed across
64/128 nodes. Reevaluate only the five closed-form controls at 80-digit
Decimal precision from the standard library, retaining the ORIGINAL 2e-10
tolerance and all prior controls/results. Compare them with the saved
quadrature values; do not recompute the virial science or alter the model.
Archive the original failed control, reference its result hash, and report
combined qualification only if all retained and repaired controls pass.
