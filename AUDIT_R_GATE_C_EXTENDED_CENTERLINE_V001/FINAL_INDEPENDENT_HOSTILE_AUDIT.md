# Final independent hostile audit: Gate R-C centerline reporting repair

**Verdict:**
`PASS_REPORTING_REPAIR__CENTERLINE_Z1_REJECTED_L4_L12__HALT_NATIVE_ALGEBRA_ROUTE`

**Exact frozen check census:** `542/542` passed, `0` failed.

The pre-repair hostile result remains correctly failed closed at `363/383`:
all 20 failures were omitted target `lowest_five_ritz_values` fields.  The
bounded reporting repair closes that defect.  It does not promote a physics
result or alter the frozen finite-window classification.

## 1. Custody and repair scope

The frozen protocol, sealed L4/L6/L8 input, blind raws, original comparison
method, original comparator, and pre-repair failed report reproduce their
pinned SHA-256 digests.  Current repaired target custody is:

```text
9a7bc040c990cdb14c01026ab0e3ce55cc94d767e738911c44bce1753c7584c2  PROTOCOL.md
e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7  compute_phase_screen.py
c8ce97913795f46b493b1aab328d93cc61eeeefd167407c283e4137847e2dcb9  RAW/SECTOR_L10_Q5.json
0e04d2286b3c1669078dc5cd8ff68180c7a989b8741c9f3da772605ca49dde49  RAW/SECTOR_L12_Q6.json
dcaefd6259fe653676cd6da181f4ee341c2d6e14409b6cc5146a9cdc9c5d056a  RESULT.json
a95ae802279a11630fb81a496e1d56240da44c48d26010acaa992e89f283ad63  RESULT.md
85704337ca735d3fca3ef1578c84343dca18111b8bddc42b11e743437a696b98  REPORTING_REPAIR.md
```

Independent comparison custody is:

```text
ebd522411a0e7f67e37d5023fbdea01bc63bdd796ca23020b0d749b414146a05  sealed L4/L6/L8 RESULT.json
3989879720404d6bd5cb1238788f4f31eb8e5b19d09c61ce604b26fa3ae5345b  blind L10 q5 raw
dff0bc6f9c5f4eeacfd7f56485dd0c27812d226dc866f4225d9803ec37a5d8a5  blind L12 q6 raw
29f4b6ca97765c219018ab8116a926a99dc77bb1b13b29d44b53686701e976ed  POST_OUTPUT_METHOD.md
ab66f64b61b1503a5c5c4a275ff31944f63f12833b1f4523a09551f734cfa853  compare_and_classify.py
4be4138270dc0ff1adedf4c0b2ed91322831ae630001707c7d492a398acc85bb  POST_OUTPUT_FREEZE.json
17599e68fab5cc541facbf073d66e8ec66ed74ee93c4a9c6ac120669ae8caa58  PRE_REPORTING_REPAIR_FINAL_REPORT.md
```

The pre-repair input hashes remain pinned as target aggregate
`0dea9b4625fa53ed7dd6e24b47d9c767eb828e3f9878c70b41422424cbc97ece`,
L10 raw
`23b5250ffd9a15668afab4e61eb72baddae85b55feafacbb8cf2a05635ef8c32`,
and L12 raw
`e2e0e9c3c18bf4352e58653dd6d0637412a60fa683997de52e12b964470581f5`.
The pre-repair failed hostile result remains pinned as
`daf75f081eb28b05517d854b7b3b05c5305fbd13cf817e49a61227b92a20dc5b`.

The repaired serializer has exactly the two authorized insertion sites: one
for ground checkpoints and one for response checkpoints.  Replayed
`ground_energy`, `Delta_act`, `chi_tau`, and `R_low` reproduce the pre-repair
promoted values to the audit's `1e-14` relative invariant guard.  All other
raw target/blind comparisons, residuals, dimensions, nonzero counts,
convergence checks, and resource guards pass.  The maximum relative
difference among target/blind `ground_energy`, `Delta_act`, `chi_tau`, and
`R_low` is `6.971783242007844e-15`.

## 2. Lowest-five telemetry and reconstruction

All 20 target checkpoint lists were audited: five ground and five response
checkpoints at each of L10 and L12, comprising 100 serialized Ritz values.
Every list has exactly five finite values in nondecreasing order.  The 16
blind checkpoint lists, comprising 80 values, pass the same count, finiteness,
ordering, and first-value reconstruction checks.

The final lists are:

```text
L10 target ground
-12.746182119255842  -10.725318224498952  -10.363810840149172
 -9.644402299592715   -9.202877096468752

L10 target response
-11.727012832008370  -10.255295094969387  -10.135916715196510
 -9.579073745974084   -9.461424881190696

L10 blind ground
-12.746182119255836  -10.725318224498945  -10.363810840149178
 -9.644402299592713   -9.202336635824555

L10 blind response
-11.727012832008372  -10.255295094969380  -10.135916715196508
 -9.579073745967531   -9.461424880987897

L12 target ground
-15.263603932919514  -13.566841741424197  -12.884760255091882
-12.470614010668532  -12.064798917719289

L12 target response
-14.411337710776406  -12.991819260077742  -12.811726278923302
-12.594976132059523  -12.230429026980064

L12 blind ground
-15.263603932919510  -13.566841741424206  -12.884760254852971
-12.470614010667129  -12.064724281502052

L12 blind response
-14.411337710776406  -12.991819260077742  -12.811726278923308
-12.594976132025977  -12.230428994786088
```

At every target and blind checkpoint, the first ground Ritz value reconstructs
that checkpoint's reported ground estimate, and the first response Ritz value
reconstructs `ground_energy + Delta_act`, within the frozen `1e-9` absolute
guard.  For all four final target/blind ground-response pairs the serialized
reconstruction error is exactly `0.0`.

The higher Ritz values are telemetry from separately converged
response-cyclic Krylov spaces; only ordering, finiteness, completeness, and
the promoted first-pole reconstruction are required.  They are not asserted
to be a common complete low spectrum.

## 3. Frozen classification and route disposition

The independent reconstruction and repaired target both return exactly:

```text
CENTERLINE_Z1_REJECTED_L4_L12
```

The same two preregistered conjunctive checks fail:

```text
fixed_z1_beats_positive_gap   FAIL
fixed_z1_near_free_gapless    FAIL
```

All other frozen classification decisions pass.  In particular, the fitted
finite-window exponents and scaled tails remain close to `z=1`; the rejection
arises from the two held-out model-comparison requirements.  This is an
empirical rejection of the declared L4--L12 centerline prerequisite, not a
proof that the thermodynamic exponent differs from one and not proof of a
positive thermodynamic gap.

The mandated route status is therefore unchanged:

```text
HALT__DO_NOT_START_NATIVE_ALGEBRA
```

No native Poincare/Virasoro algebra or anomaly calculation is authorized by
this packet.  No thermodynamic phase, continuum, metric, universal coupling,
emergence, Gate B, or gravity result is claimed.  No grid, graviton, or Ward
axiom is introduced.

