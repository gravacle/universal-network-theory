# Independent hostile prefix-history engine V001

## Scope and independence

This is a clean-room executable control for the finite owner-once relational
history. It imports no development module, matrix, state array, transition
map, or generated history. Physical constants and acceptance thresholds are
transcribed from the sealed relational protocol and the certified
prefix-lineage theorem before control output.

The implementation deliberately differs in representation:

- carrier and lineage subsets use reversed combination order;
- edges use reversed site order and the block order rail 2, connectors,
  rail 1;
- transport uses a Gershgorin-scaled Chebyshev action and independent
  Gauss--Legendre current quadrature;
- lineage indices are full integer masks. No digest is an array key and no
  state is grouped by a digest, orbit, symmetry class, or representative.

## Exact reachable blocks

Immediately before fresh event `n`, the state is stored in

```text
H_n = direct_sum_q C[Subsets({0,...,n-1},q)]
                   tensor C[Subsets({0,...,2L-1},q)].
```

Admission allocates the complete next prefix block. The blank branch maps to
the same full lineage mask; the write branch adds event bit `n` to both the
lineage and carrier masks. Transport changes only the carrier mask and is
applied independently to every canonical lineage row.

At the terminal event the full `H_L` array is forbidden. The bit-zero and
bit-one children are generated one lineage-row window at a time from the
retained `H_(L-1)` state, transported independently, and accumulated only at
the level of lineage-diagonal registered observables. A terminal amplitude
query is invertible: the final lineage bit selects its child, clearing that
lineage bit selects one preterminal row, and the carrier write rule supplies
the unique child input before transport.

## Numerical controls

The two independently evaluated resolutions are frozen as:

```text
rough: Chebyshev degrees 16,24,32,48,64,80; GL18; tolerance 3e-9
sharp: Chebyshev degrees 24,32,48,64,80,96; GL28; tolerance 8e-11
route time pi/2; admission angle pi/4; scale bound 3q
```

The 32 subsequent Bessel coefficients are a convergence indicator, not a
claim of an infinite-tail proof. Rough/sharp history agreement, strict
admission and number ledgers, node continuity, norms, owner-once support,
nonnegative writes, and dynamically nonzero blocking are all required.

## Locks and claim boundary

Only L4, L6, and L8 controls are authorized by this packet. L10 requires a
future hash-pinned `CONTROL_GATE.json`. L12 requires that control gate, a
future hash-pinned `SEALED_L10_GATE.json`, and the separate reduced-method
resource gate. Missing, malformed, or failed gates stop before state
allocation.

This packet can validate only an independent finite numerical representation.
It cannot authorize an L10 or L12 history, spectrum, `z=1`, criticality,
continuum behavior, emergence, or gravity.
