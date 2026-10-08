# Consistent-inertia oracle result: quadrature limitation retained

2026-09-30. The fixed 12-case/order evaluations and eight adjacent-order
comparisons completed without exception, resource failure or changed input.
The packet evaluated 1,905 scalar entries and retains 35 failed check groups.
It therefore **does not pass the full frozen numerical packet**. No trajectory
was integrated and no physical or continuum qualification was granted.

| Mesh | Order 16 | Order 32 | Order 64 |
| --- | --- | --- | --- |
| Single origin shell | all controls pass | all controls pass | all controls pass |
| Uniform | 6 failed groups | all controls pass | all controls pass |
| Graded | 10 failed groups | 10 failed groups | all controls pass |
| Thin annuli | all controls pass | all controls pass | all controls pass |

The other nine failed groups are the three comparisons in each of uniform
16/32, graded16/32 and graded32/64. These are overlapping controls of the
same numerical errors, not 35 independent physical failures.

The exact rational matrix and derivative reference distinguishes quadrature
error from internal consistency. On the graded mesh the normalized matrix
error is 1.1713351376785308e-5 at order16 and 4.925274466049956e-9 at order32.
The canonical geometric-force error is 2.609044955186019e-4 and
2.6662049468684137e-7 respectively, against the unchanged 2e-11 arithmetic
criterion. All order64 controls pass on these four meshes; this does not
establish a uniform error bound for all admissible radius ratios.

Every literal assembled matrix has exact positive rational LDL pivots. The
largest recorded infinity-norm condition number is approximately
4.2058665509423045. Exact solve-residual/forward-error controls, every fixed-p
centered and Richardson derivative control, the affine nulls, input integrity
and the exact single-origin identities pass. The independent-exact work
comparison fails where the quadrature force differs from the exact integral;
finite-difference work consistency for each numerical action remains intact.
Thus passing a discrete energy derivative does not certify accuracy of the
underlying shell integral.

## Custody and independent review

- Source: `a7cd9bfe6026ce2e664a804394009b32e5023d5b9cda43a84844ebd039bd4a66`.
- Protocol: `c5b1dec4402aa5387a1aa3be8f76fc3e642c66ae0792b0a3ac5e28dc5098ae36`.
- Intent: `c8231192d96b0983d49effb030dd20b822ab9b0883eae5f3e36b3900b3918ca0`.
- Result SPHERICAL_CONSISTENT_KINETIC_ORACLE_V001_RESULTS.json:
  `bb9810e5d392e2ce7ee3ae3d2bdf48abbe7576bd349c2d2928e77fb332228327`.
- Canonical payload:
  `43e3230323c2e49edaff8ce3a2b8466230f5b66e0a687e1bccb763dcaed5a6be`.

Root read the entire kernel, oracle and protocol before its single bounded
run; short_path_adversarial independently preflighted those sources and the
closed-form derivation. Root subsequently recomputed the canonical payload
hash and authenticated every recorded input. The independent reviewer read
the saved aggregate failures without rerunning calculations and confirmed the
quadrature-versus-canonical-consistency distinction. This is agent source and
saved-result review, not an external scientific peer review.

The reported analysis-phase snapshot is 0.357291458 seconds and 37,158,912
bytes self RSS, excluding final serialization/publication. The external wall
cap was60 seconds with the fixed internal CPU/RSS bounds and five thread
controls set to one. No worker remains. Do not rerun or reclassify this packet.

## Next numerical method, not a threshold repair

The independently derived exact rational-polynomial inertia and geometric
force in SPHERICAL_EXACT_INERTIA_DERIVATION_V001.md represent the same shell
action without quadrature. Author a separate runtime kernel and test it on
the same four cases, exact references, FD steps and arithmetic/derivative
criteria. Its single closed-form method has no quadrature-order knob: do not
repeat it three times under misleading order labels or call the old failures
passed. Root and an independent source reader must review before execution.

Even a successful kernel packet leaves the full consistent two-current
implementation, time/width/domain controls, physical/semidiscrete propagation
and crossing limits, source/formation, lensing and merger observations open.
All eleven program lanes remain OPEN; Stage 3 is not complete.
