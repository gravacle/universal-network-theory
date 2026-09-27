# Protocol: blind hostile lineage-sensitive scaling audit

## 1. Fixed scope and blindness

The audit sizes are `L in {4, 6, 8}` and the revisit events are independently
evaluated from the same terminal owner-once checkpoint.  Revisit responses are
not chained.  The target scaling directory and target scaling outputs are
forbidden inputs until the hostile result is sealed.

This source freeze authorizes synthetic tests only.  A future L4 execution
requires a distinct authorization record.  L6 and L8 require later gates.

## 2. Authenticated engine and checkpoint

The dynamical authority is the hostile V002 prefix engine:

- `independent_prefix_history.py` provides the reversed-mask prefix basis,
  owner-once admission, carrier graph, and frozen rough/sharp parameters;
- `independent_prefix_history_v002.py` supplies recurrence-replay transport;
- `FROZEN_MANIFEST_V002.json`, `V002_LOW_MEMORY_SUPPLEMENT.md`, and
  `CONTROL_HISTORY_L{4,6,8}_V002.json` bind the authenticated method and
  controls.

The historical engine streams the final event and discards the final
amplitude.  The audit therefore regenerates the sharp prefix-`L-1` state and
uses a newly frozen adapter to materialize the final event in q blocks.  For
each old q block it independently evolves:

1. the same-q child, with the frozen cosine on event-blank carrier words; and
2. the q+1 child, with `-i sin(pi/4)` and exact event-bit insertion.

The hostile carrier transport and sharp tolerance are unchanged.  Every q
block must have the canonical reversed-mask shape

```text
(binomial(L,q), binomial(2L,q))
```

and the total checkpoint norm must pass before response algebra begins.

## 3. Independent signed-low-rank algebra

For terminal q-block amplitude `A_q`, compute the thin SVD

```text
A_q = U_q diag(s_q) V_q^H.
```

The actual arm is the pure joint density `|A_q><A_q|`.  The matched-product
arm is

```text
(rho_lineage,q tensor rho_carrier,q) / p_q,
p_q = ||A_q||_F^2.
```

No global joint density is formed.  The revisit rotation couples only the
event-local `(lineage bit, carrier bit)` pairs `00 <-> 11`.  The actual arm is
propagated as compact amplitude factors.  In a fixed-q lineage sector the
one-event reduced lineage density is diagonal; the code checks that fact and
then applies its two diagonal weights analytically to the matched carrier
density.

After tracing lineage, each carrier-q difference is represented as

```text
Delta_q = X_q,+ X_q,+^H - X_q,- X_q,-^H.
```

Positive and negative factors are compressed separately.  Any discarded SVD
weight is recorded as an explicit error bound.  The nonzero signed spectrum is
computed from the QR-reduced signed Gram matrix, not a dense carrier matrix.

Registered observables are:

- carrier trace distance;
- carrier configuration total variation;
- carrier-number-sector total variation;
- site occupation-difference vector and RMS; and
- total signed trace and per-q signed trace controls.

The same authenticated carrier transport acts on both signs.  Trace distance
must be invariant under that common blockwise unitary within the numerical
error budget.  Occupation diagnostics may change.

## 4. Synthetic gate

Before any scientific execution, the independent algebra must agree with an
explicit full-density construction on synthetic complex checkpoints.  The
gate includes:

- full reduced carrier matrices before transport;
- all registered observables;
- independently generated random blockwise carrier unitaries;
- a rank-one checkpoint for which actual and matched-product arms coincide;
- refusal of a nonunitary transport; and
- finite-value and trace controls.

The custody tests separately require strict JSON, exact hash and byte count,
ordered complete q shards, canonical shapes/dtype, exact-prefix relocation,
root containment, no symlinks, no traversal, corruption refusal, stable
checkpoint identities, and atomic non-overwrite creation.

## 5. Checkpoint identity and restart rule

The canonical checkpoint identity hashes a sorted JSON object containing:

- schema and stage;
- L, prefix, and sharp accuracy label;
- hostile V002 engine hash;
- hostile history hash;
- this packet's source-freeze hash; and
- every ordered q shard's q, SHA-256, byte count, shape, and dtype.

Resume is permitted only when a complete receipt recomputes to the same
identity and says `unblinded_to_target: false`.  Missing, duplicate, reordered,
corrupt, partially published, differently relocated, or differently frozen
inputs cause refusal.  Existing scientific outputs are never overwritten.

## 6. Relocation rule

Frozen provenance paths are preserved verbatim.  At runtime, a path may be
relative to the current repository or lie under one exact registered legacy
root.  Only the suffix is mapped to the current root.  The resolver rejects
unknown absolute roots, traversal, symlinks, repository escapes, non-files,
the blinded target directory, size mismatches, and hash mismatches.

## 7. Future execution and reconciliation order

The required order is:

1. source/input freeze;
2. synthetic gate;
3. separately authorized hostile L4 regeneration;
4. dense-L4 reproduction;
5. real restart and corruption-refusal exercise;
6. resource and energy-assumption report;
7. separate L6 authorization and target/hostile reconciliation;
8. revised L8 estimate and, only if all gates pass, separate L8 authorization;
9. hostile result seal; and
10. separate unblinded reconciliation.

Failure or incomplete reconstruction leaves the classification unresolved.
No tuning from target values is permitted.

## 8. Claim boundary

The maximum possible claim is a finite, separately audited L4/L6/L8 response
ledger under the frozen owner-once model.  The protocol cannot establish an
all-L theorem, a scaling exponent from fewer than independently resolved
sizes, continuum behavior, emergent geometry, curvature, gravity, RGRL, WTC,
alpha, or cosmology.

