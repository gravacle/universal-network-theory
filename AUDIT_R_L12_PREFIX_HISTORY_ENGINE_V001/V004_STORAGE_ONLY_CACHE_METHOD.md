# Hostile V004 storage-only carrier cache method

**Status:** `FROZEN_PRE_CACHE_PRE_HISTORY`

## Purpose and boundary

V004 is a conditional storage-only successor to the frozen hostile V003
q-sharded prefix-history engine.  It is not permission to interrupt, replace,
or reinterpret a current V003 or target V004 execution.  It may be activated
only after an explicit future gate records that those executions reached
their frozen six-hour resource guards.

The carrier basis order, complete carrier masks, complete canonical lineage
masks, hostile edge order, Hamiltonian coefficient `-1`, exchange orientation,
current formula, ALLOW/REQUIRE behavior, owner-once admission, terminal child
streaming, rough/sharp Chebyshev degrees, quadrature, tolerances, ledgers, and
observables are unchanged.  A cache entry is an authenticated serialization
of indices that V003 reconstructs repeatedly; it is not a reduced state,
matrix approximation, sampled lineage, or new physical operator.

## Immutable cache payload

For each `(L,q)`, the independent hostile builder serializes raw little-host
NumPy scalar arrays in the exact frozen reversed-combination order:

```text
q_Q_words.u32       C(2L,q) complete occupation masks
q_Q_offsets.u64     3L+1 offsets in the frozen hostile edge order
q_Q_sources.i32     concatenated occupied-u/blank-v source ranks
q_Q_targets.i32     matching XOR-toggled target ranks
```

The `-1` exchange amplitude remains implicit, exactly as in V003.  The
consumer reconstructs the same ordered list of `(source,target)` views and
uses the unchanged V003 multiply and current operations.

The builder also serializes, for every applicable event and charge, the exact
old/new carrier-column admission maps and the exact stay/write canonical
lineage-row maps.  Every file is size checked and SHA-256 pinned in a cache
manifest.  Target and hostile implementations must build independent caches;
they must not share payloads.

## Exact L12 storage arithmetic

The raw basis and exchange-index payload over `q=0,...,12` is `744,524,728 B`.
The thirteen small edge-offset arrays add `3,848 B` of format metadata. All
admission column maps total `81,676,960 B`; all nonterminal lineage row maps
total `16,376 B`.  The exact closed-form basis/exchange/admission/lineage
payload is therefore `826,218,064 B`, plus those offsets and the small JSON
manifest.
Together with the frozen `H_10+H_11` maximum of `8,773,664,640 B`, the maximum
logical scratch is `9,599,882,704 B`, leaving `11,874,953,776 B` below the
20-GiB limit before small manifest/filesystem overhead.  The preflight
requires at least 1 MiB overhead headroom in addition to those exact bytes.

Only one charge cache is memory-mapped at a time.  The largest q-cache plus
its largest terminal admission map is `224,797,664 B`.  The unchanged
`1,400,000,000 B` numerical allocation, `512 MiB` amplitude window, 16-GiB
RSS guard, and six-hour method guard remain authoritative.  Logical byte
arithmetic is not promoted as an empirical RSS result.

## Cache construction invariants

Before sealing a payload the builder checks exhaustively for every stored
array:

1. basis count `C(2L,q)`, word width, Hamming weight, uniqueness, and exact
   reversed-combination order;
2. every source satisfies occupied `u`, blank `v` for its named edge;
3. every target is the exact source word XOR the two edge bits and has the
   exact reverse-colex rank;
4. source/target counts are `C(2L-2,q-1)` per oriented edge;
5. every admission map adds only the named event and is injective;
6. every lineage map preserves the complete old mask and optionally adds only
   the fresh event bit; and
7. the sum of file bytes equals the closed-form cache census.

The consumer validates the cache manifest, graph, dependency hashes, every
payload path, byte size, and SHA-256 before opening a history workspace.

## Hard locks and future controls

`CACHE_PAYLOAD_BUILD_GATE_V004.json` is absent at freeze.  Without its exact
future classification and hashes, the builder exits before creating a cache
directory.  It must also bind terminal resource-obstruction records from both
currently running implementations; unchanged current runs are never
interrupted.

All physical history modes are separately locked.  L4/L6/L8 require a future
physical-control execution gate.  L10 additionally requires a passing complete
L4--L8 same-path comparison.  L12 additionally requires a passing L10
same-path/hostile comparison and the unchanged 20-GiB free-scratch check.
Each gate pins this V004 consumer, its freeze, and the exact cache manifest.

No cache payload or physical history is produced at this freeze.  The only
permitted output is the nonphysical index/allocation preflight after this
method, builder, consumer, and preflight implementation have been frozen.

## Claims

V004 may establish only that a future cached execution is the same finite
record computation as V003.  Any six-hour miss remains a resource obstruction.
Future histories and parity results are conditional or empirical until hostile
adjudication.  Scaling, spectral intervals, `z=1`, continuum behavior,
spacetime algebra, anomaly cancellation, universal coupling, emergence, and
gravity remain open.  No grid, graviton, Ward axiom, reservoir, or continuum
assumption is introduced.
