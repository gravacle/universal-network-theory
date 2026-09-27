# Lineage Carrier Reduction V001

## Purpose

This directory tests a sharply limited proposition about the existing
owner-once, one-pass finite history model:

> Before a loaded cell is revisited, tracing out the lineage register gives
> the same carrier state as a carrier-only channel with
> `K0 = P_occupied + cos(phi) P_blank` and
> `K1 = -i sin(phi) a_event^dagger P_blank`, followed by the same prism-ladder
> transport.

The target is the historical joint implementation in
`DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py`.
The comparison channel is implemented independently in
`verify_carrier_reduction.py`.  Historical and provenance-bearing files are
read but never modified.

Every output is fail-closed against the frozen theorem and protocol in
`DEVELOPMENT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001`.  Their repository
paths and pinned SHA-256 digests are embedded in the JSON dependency record.

## What is compared

For every event the verifier compares the joint target with a Kraus-ensemble
purification of the carrier-only channel both immediately after admission and
after transport.  It reports:

- phase-sensitive purification L2 and Linf residuals;
- an exact reduced-carrier Hilbert--Schmidt residual, evaluated through small
  environment Gram matrices without constructing a large carrier density
  matrix;
- a purification-derived upper bound on carrier trace distance;
- sector-weight, occupation, instantaneous-current, integrated-current,
  null-integrated-current, and delta-integrated-current residuals; and
- explicit reduced-carrier trace distance at L4.

The Kraus outcome row is only a computational purification label.  No future
operation reads it.

## Run

```bash
python3 verify_carrier_reduction.py
python3 -m unittest -v test_carrier_reduction.py
```

The default target is L4 and L6 with 16 Taylor substeps per transport dwell.
L8 is supported but intentionally opt-in because the historical joint state
has 735,471 amplitudes and the repeated transport is substantially more
expensive:

```bash
python3 verify_carrier_reduction.py --lengths 8 --output CARRIER_REDUCTION_L8_RESULT_V001.json
```

The primary `CARRIER_REDUCTION_VERIFIED_FINITE` disposition requires both L4
and L6.  An L8-only pass is labeled
`SUPPLEMENTAL_L8_CARRIER_REDUCTION_VERIFIED_FINITE`; it cannot satisfy or
replace the mandatory primary protocol.  Empty and partial mandatory length
sets fail closed.

`CARRIER_REDUCTION_RESULT_V001.json` is deterministic: it contains no clock,
host, memory, or wall-time fields.

The report separates model-equivalence disagreements from common numerical
control error.  The former measures differences between the joint target and
the matched channel.  The latter contains norm drift from the shared finite
Taylor evolution and the fresh-event precondition.  Both must independently
pass their declared tolerances.

Nonfinite metrics, nonfinite arrays, materially negative squared residuals,
or frozen-document hash mismatches terminate verification rather than being
serialized as a pass.

## Interpretation boundary

A passing finite result shows that the current owner-once implementation has
a matched carrier-only channel at the tested sizes.  It does not show that
lineage correlations are absent, prove an all-L theorem, exclude a later
lineage-reading interaction, derive gravity, or establish an experimental
difference from an ordinary ladder model.  Those are separate questions.
