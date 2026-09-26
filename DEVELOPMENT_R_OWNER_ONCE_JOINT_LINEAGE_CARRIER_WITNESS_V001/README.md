# Owner-once joint lineage--carrier witness V001

This packet preregisters one terminal joint observable for the existing
owner-once relational accumulation engine.  It asks whether the retained
spent-lineage label and the carrier configuration contain a resolved finite
correlation that is absent from the unconditional carrier marginal.

The observable is built only from basis data already present in that engine:

- `F_e`, the diagonal indicator that event cell `e` is spent in the canonical
  lineage mask; and
- `n_e`, the diagonal occupation of the co-located retained carrier target.

No Hamiltonian, projector, Gate condition, Record--Geometry Realization Law,
continuum premise, or gravity premise is imported from another construction.
The observable is a terminal readout; it does not change the frozen evolution.

The fixed witness compares the observed joint expectation with a
sector-matched sham register that preserves both separate within-`q` density
marginals while removing their correlation.  A second exact within-`q`
permutation control randomizes lineage labels while leaving the carrier state
and sharp-`q` weights unchanged.

Mandatory seed sizes are `L=4,6,8`.  The sole primary checkpoint is the state
immediately after the final transport of the first owner-once pass and before
any revisit.  Event-resolved values are diagnostic only.  The newly defined
`D_10` and `D_12` readouts are held out and cannot be computed until the seed
result, implementations, and hashes are sealed.  Existing L10/L12 history
artifacts remain historical inputs, not newly generated experimental data.

The protocol was frozen before target output was opened.  The mandatory
L4/L6/L8 target calculation has now been executed and sealed; the hostile
source and output remained unread by the target implementation path.

- [`PROTOCOL.md`](PROTOCOL.md) freezes the observable, controls, schedule,
  tolerances, falsifier, and held-out rule.

## Target implementation and sealed output

`target_joint_witness.py` is the target implementation prepared after the
protocol freeze.  It imports the historical dense seed engine only for the
joint dynamics.  It independently implements:

- the registered centered overlap witness;
- separately ordered row- and column-streaming accumulators;
- exact within-charge permutation-twirl identities;
- the sector-matched sham and its direct product-state negative control;
- all charge-resolved contributions and marginals;
- L4 direct-basis and exhaustive 24-permutation controls;
- the frozen 64/128-substep comparison and residual gates; and
- deterministic, fail-closed target-only adjudication.

The executable requires the explicit `--authorize-frozen-seed` guard.  After
the independent hostile source was frozen and authorization was recorded, the
target run produced `TARGET_WITNESS_RESULT_V001.json`.  A second target-only
run was byte-identical.  `TARGET_WITNESS_SEAL_V001.json` records the result,
source, protocol, test, and README hashes plus the rerun and resource evidence.
The target classification does not decide the final `T_4:8` disposition; it
remains explicitly awaiting the independent comparison.

Synthetic-only tests are safe before that freeze:

```bash
python3 -m unittest -v test_target_joint_witness.py
```
