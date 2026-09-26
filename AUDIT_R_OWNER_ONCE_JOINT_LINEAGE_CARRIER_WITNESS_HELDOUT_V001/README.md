# Hostile held-out L10/L12 joint-witness reader

This directory freezes the independently authored hostile reader for the
owner-once joint lineage--carrier witness at `L=10` and `L=12`.  It uses only
the hash-bound hostile V003/V004R4 engine, retained hostile sharp
`H_(L-1)` shards, and a new hostile rough regeneration.  It does not import or
open the target implementation, target arrays, or target result.

The final event is reconstructed exactly as two orthogonal child windows.
Each window is transported by the frozen hostile propagator, consumed by
separately ordered row-first and column-chunk-first witness reductions, and
discarded.  No full `H_L` array is allocated.  Both sizes must finish and pass
the fixed controls before one deterministic JSON result can be published.

The reader carries forward the hash-authenticated V003 endpoint-capacity
repair.  Rough checkpoints extend through degree 112 and sharp checkpoints
through degree 128, while the quadrature orders, convergence tolerances,
graph, Hamiltonian, admission angle, route time, and observables remain
unchanged.  This is numerical approximation capacity, not a change to the
physical calculation.

## Frozen physics and controls

- checkpoint: after final owner-once transport and before revisit;
- witness: the unchanged parent-protocol joint lineage--carrier covariance;
- resolutions: regenerated rough and retained sharp;
- controls: normalization, total content, charge identity, row/column
  agreement, sham self-covariance, analytic shuffle identity, solver
  convergence, and rough/sharp agreement;
- tolerances: `1e-8` rough/sharp, `1e-10` norm/content/marginals/charge and
  row/column, `1e-12` sham/shuffle;
- output: strict sorted finite JSON, published atomically only after both
  sizes complete.

## Synthetic freeze test

```text
PYTHONPYCACHEPREFIX=/tmp/heldout-pycache \
python3 -W error::ResourceWarning -m unittest -v test_source_freeze.py
```

The tests use only constructed `L=2`/`L=3`/`L=4` states.  They include a
dense-versus-streamed terminal reconstruction and a dense-versus-streamed
witness/sham comparison.  They do not execute or open the physical held-out
L10/L12 witness values.

## Execution lock

Physical execution remains locked behind the exact hostile authorization
literal and the sealed fresh-telemetry/resource gate.  No execution was
performed while this source was written, tested, or frozen.
