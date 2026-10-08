# Independent preflight: finite field at unchanged actions

2026-09-29. Full read of the analytical reduction, source and prospective
protocol; no import, scientific worker, quadrature or fit by this reviewer.

Accepted source `fixed_action_finite_field_v001.py`, SHA-256
`44a35889ab72960ca479169af89c4f1659bd6c0ee35d20089f7f462f8c1e05cd`,
and protocol `FIXED_ACTION_FINITE_FIELD_PROTOCOL_V001.md`, SHA-256
`0d6e1a69dfa6fbbf1a7c0fdb6ee3f56b7e04ae3ca1a3a994f1cd7b178ebbc9b5`.
The full `FIXED_ACTION_FINITE_FIELD_REUSE_V001.md` derivation was also read.

## Checks and prefreeze correction

The equal-endpoint cubic correctly retains the physical product `delta*h`:
`c^3+(delta^2+r^2)c=delta*h`. The positive factor Q, action and period
normalizations, strict monotonicity of action in the half-width, and analytic
upper bracket `sqrt(2I/delta)` check. The stable center/minimum difference
keeps tiny excitation energy separate from the large negative minimum.
The independent excess-potential action control has the correct factor of
pi and uses its separately qualified negative-radicand control; the primary
positive-Q integrand is not clipped.

One issue was identified and corrected before freezing or execution. Computing
the virial from `y*(delta^2*y+y^3-delta*h)` can subtract large equilibrium terms
while its error is measured against tiny excitation. The settled source uses
the exactly equivalent displacement virial

    <x*(stiff*x+3*y_star*x^2+x^3)>,  x=y-y_star,

with x computed from the stable center difference. This equals `<y U'(y)>`
because `<U'>=0`, which remains separately checked. No physics, field, action,
numerical tolerance or output selection changed.

## Census and scientific scope

The full 36-template by seven-field census is retained. Origin comparisons
use the original energy, pressure, turning points and scalar susceptibility;
each template's own nonzero preparation field uses its independently qualified
old phase mean and held energy. The action is not reset between field values.
All 168 old-resolution force differences remain descriptive outputs.

The field response uses the same weights, source scale and contact. The
reported ideal adiabatic work is the endpoint difference of contact plus
intrinsic mode energy, with the old matched constant unchanged. It is not
mislabelled as an executed work trajectory. Signed controls, zero-action
limit, separate minimum/excitation outputs, and exact-zero readouts are
consistent with the protocol. Custody imports only the reviewed data-discovery
helper; old propagation or publication wrappers are not executed.

No remaining load-bearing preflight blocker. The independent analytical
force-ordering result is a separate note, not an added post-hoc numerical
gate. This calculation supplies a scalar fixed-action constitutive continuation,
not an adiabatic formation proof, an isotropic vector response or a solution
of the coupled gravitational constraints.
