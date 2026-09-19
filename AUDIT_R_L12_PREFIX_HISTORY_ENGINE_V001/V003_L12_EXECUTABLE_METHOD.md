# Hostile V003 q-sharded L12 executable method

## Scope

V003 supplies an executable storage schedule for the already certified exact
prefix-lineage history. It does not alter the graph, owner-once predicates,
admission or transport operators, canonical full lineage masks, current
orientation, ledgers, observables, sector rule, rough/sharp Chebyshev controls,
or terminal two-child reconstruction.

The implementation imports only the frozen hostile V001 physical primitives
and V002 recurrence-replay action from this audit directory. It imports no
development module, target matrix, target array, or target output. Their
hashes are dependencies of the V003 freeze.

## Q-sharded state

At prefix `n`, every sharp-number component is a separate complex128 memmap:

```text
state_n/q_Q.c128 has shape C(n,Q) by C(2L,Q).
```

The row address remains the complete canonical lineage mask in reversed
combination order. A digest never indexes an amplitude. Admission constructs
`state_(n+1)` one output `q` shard at a time. The unchanged branch is copied
from input `q`; the write branch is copied from input `q-1` using exact
reverse-colex ranks after adding the fresh event bit to both masks. The input
prefix is released only after every output shard, actual route, null route,
and ledger statistic is complete.

Transport constructs one carrier `q` block at a time. Its lineage-row batches
use the V002 recurrence-replay action, at most 12 quadrature nodes per group,
and a conservative 20-vector allocation certificate. Any numerical-workspace
estimate above `1,400,000,000 B`, amplitude I/O window above `512 MiB`, live
logical scratch estimate above `20 GiB`, process RSS above `16 GiB`, or method
runtime above six hours fails closed. No lineage or carrier state may be
deleted to satisfy a guard.

## Terminal stream

No `H_12` shard is created. The final event reads retained `H_11` shards and
performs three one-`q` passes:

1. bit-zero actual child: multiply blank-event columns by `cos(pi/4)`;
2. bit-one actual child: populate only event-occupied columns from the unique
   preterminal carrier mask with coefficient `-i sin(pi/4)`;
3. null child: route the unchanged preterminal rows.

Each batch is discarded after its transported occupation, sector weight,
norm, and oriented current are accumulated. The sharp `H_11` shards remain
available as the inverse terminal-amplitude record. The exact admission
support counts are `417,225,900` for child zero and `C(34,11)=286,097,760`
for child one; neither count licenses a full terminal allocation.

## Exact resource arithmetic

The largest nonterminal transition is

```text
H_10 + H_11 = 548,354,040 complex128 entries
              = 8,773,664,640 bytes.
```

The rough workspace is removed after its complete row record is retained and
before the sharp resolution starts. Therefore the two resolutions never
co-reside on disk. The retained sharp terminal state is `6,675,614,400 B`.
These are exact logical file sizes; filesystem and runtime telemetry remain
empirical and authoritative.

## Hard gate and claims

L12 execution requires a future local gate whose classification is exactly
`PASS_PREFIX_HISTORY_L10_GATE_V002` and which pins this V003 implementation
hash, followed by the `20 GiB` free-scratch check. The gate is absent at this
freeze. Authorization is checked before a workspace is created or any basis
or carrier block is constructed.

V003 validation is limited to syntax and exact allocation/index invariants.
No L12 history is run here. This method cannot promote an L12 history,
spectrum, `z=1`, criticality, continuum behavior, emergence, or gravity.
