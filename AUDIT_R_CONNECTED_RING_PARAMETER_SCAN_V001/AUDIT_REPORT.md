# Independent hostile audit

## Disposition

`PASS_CONTROLLED_NUMERICAL_PARAMETER_SCAN`.

An independently assembled 256-state ring reproduces all 12 combinations of
`delta=(0,1/2,1,2)` and the three declared pulse times. The hopping matrix is
Hermitian, preserves total occupation exactly, and direct commutators give
the target continuity convention `dot(q_i)=-J_i+J_(i-1)`.

Pointwise occupations, integrated currents, connected correlations,
retained-total changes, residuals, and norm/energy/number-law controls agree
with `RESULT.json` within floating precision. The envelope stays below the
declared L1/Linf tolerances `3e-11/4e-12`; all stronger controls are also
inside their target bounds.

At zero staggered bias, local occupations stay one half and oriented
throughput vanishes to numerical precision, while connected correlations are
nonzero. This is a symmetry control separating positional/current response
from correlation formation. It does not say the evolution is trivial.

The inherited preparation retains adopted `alpha=r0`, not a bare-F3
derivation, and the complete failure-inclusive qutrit/controller/work/reference
product PVM remains in force.

The residuals are raw record-ledger residuals, unassigned pending owner
classification. They are not called physical defects or exact zeros. The scan
does not fit a scaling law or claim generic retention, criticality, continuum
behavior, Ward structure, mature macro dynamics, or gravity.

No material defect was found at controlled numerical prepared-scan scope.
