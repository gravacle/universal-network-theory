# L10 target V002 memory-only repair

## Frozen change

V001 completed with fully agreeing numerical results but exceeded the target's
`4 GiB` RSS limit by `144,998,400 B`. V002 changes one implementation control:

```text
target maximum retained Krylov basis bytes per genesis-row batch
V001: 1,400,000,000
V002: 1,000,000,000
```

Smaller batches partition the same genesis rows and retain the same complete
`D_10=30,045,015` basis. The graph, parent, admission and transport operators,
coarse/fine Krylov dimensions, tolerances, current quadrature, ledgers, sector
rule, `7,200 s` limit, and `4 GiB` limit are unchanged. The independent V001
Chebyshev result is retained as the blind record because it already passed all
frozen numerical and resource guards.

Before V002 L10 output, the wrapper, V001 base implementation, blind result,
and V002 adjudicator are hash-frozen. An L8 validation must reproduce the V001
streamed target within `1e-10` and pass the original history gates. V002 L10
must agree with the frozen blind L10 history within the original `1e-8`
observable and sector thresholds and independently pass every strict ledger,
wall, and RSS guard.

If V002 again exceeds `4 GiB`, exceeds `7,200 s`, fails numerical convergence,
or disagrees with the blind record, the L10 obstruction remains sealed and no
further batch tuning is authorized in this packet.

This is an implementation repair, not a new physical model or a relaxation of
the gate. It cannot promote L12, scaling, criticality, continuum behavior,
emergence, or gravity by itself.
