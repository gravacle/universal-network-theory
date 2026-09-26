# Final reconciliation result

## Disposition

All frozen numerical, custody, independence, and control conditions pass.  The
exact protocol classification is:

```text
RESOLVED_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_L4_L8
```

The independently recomputed primary statistic is

```text
T_4:8 = 1832191.382751109 > 1
```

No tolerance was changed.  Each `tau_L` remains at the preregistered
`1e-9` floor after the reconciliation uses the larger applicable target and
hostile residuals.

## Numerical reconciliation

| L | target `D_L` | hostile `D_L` | absolute `D_L` difference | max target/hostile difference over all required fields | `d_L` | `r_L` | `tau_L` | `T_L` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.025544765930507966 | 0.025544765930507973 | 6.938893903907228e-18 | 5.551115123125783e-17 | 3.1086244689504383e-15 | 1.865174681370263e-14 | 1e-9 | 25544765.930507965 |
| 6 | 0.0018321913827511092 | 0.0018321913827511083 | 8.673617379884035e-19 | 8.326672684688674e-17 | 3.4416913763379853e-15 | 5.062616992290714e-14 | 1e-9 | 1832191.382751109 |
| 8 | 0.001963064475535806 | 0.0019630644755358074 | 1.3010426069826053e-18 | 8.326672684688674e-17 | 2.4424906541753444e-15 | 5.417888360170764e-14 | 1e-9 | 1963064.475535806 |

The “all required fields” comparison includes `w_L`, `w_L^sham`, `D_L`, every
`q`-resolved contribution to `D_L`, and every sharp-sector probability.  Its
maximum is below the frozen target/independent tolerance of `1e-8` by more
than eight orders of magnitude.  The `d_L` calculation also includes target
64-versus-128 values and independent row-versus-column accumulators, exactly
as specified by Equation (15).  The reconciled `r_L` is the larger applicable
target/hostile norm, content, normalization, marginal, and charge residual.

## Custody and controls

The following checks all pass:

- protocol SHA-256:
  `70984a927c30585704622dfd03ee91bf516cd9a5d14474a228d231144e5e513e`;
- target result SHA-256:
  `c1763b57b3d6a1a61b66f621b563bfc9cf34123d311e04dff2b1ac02061c1ac8`;
- hostile result SHA-256:
  `8b9c9cbdf53e857e29756c95d3702a1401cc509f294d162260e12b9b5c49a29c`;
- every target-seal artifact hash and byte count;
- every hostile source/result manifest entry and the separately pinned source
  freeze, execution record, source, tests, and compatibility-repair record;
- byte-identical target and hostile deterministic-rerun declarations;
- exact mandatory sizes L4/L6/L8 and exact terminal checkpoint schedules;
- both implementations' coarse/fine, norm/content, probability/marginal,
  sharp-charge, and row/column conditions;
- the sector-matched sham negative control and exact within-`q` shuffle null;
  and
- L4 direct-basis sums and exhaustive 24-permutation target control, together
  with the hostile exhaustive direct and permutation results from its pinned
  independent implementation.

The hostile README and source-freeze record describe the pre-output freeze,
while the later execution record and result manifests document authorized
execution.  Their chronology is consistent: the compatibility repair was
refrozen before physical output, changed no equation or parameter, and the
failed attempt wrote no result.

## Exact scientific scope

This result establishes only that, for the finite existing owner-once engine
at L4, L6, and L8, the terminal state after the final first-pass transport and
before revisit has a resolved value of the preregistered centered
lineage--carrier conditional-covariance witness.  The sector-matched sham
preserves both separate within-`q` marginals while removing their association,
and the lineage shuffle preserves the carrier state while erasing label
placement.  Both controls return their frozen null values.  Together with the
protocol's non-identifiability construction, this establishes joint
lineage--carrier information not reconstructible from the unconditional
carrier marginal.

It does **not** establish:

- that any future dynamics reads the lineage register or that it causes
  back-reaction;
- persistence through a revisit;
- entanglement;
- a held-out L10 or L12 result;
- an all-L, thermodynamic, or continuum limit; or
- the ARGER Gate, Record--Geometry Realization Law, alpha, GL6T, spacetime,
  metric response, Einstein--Hilbert dynamics, or gravity.

The reconciliation did not compute or open a new L10/L12 witness.  It verifies
seed prerequisites 1--3 of the held-out rule only.  The pre-existing exact
streamed-history resource gate remains a separate prerequisite and was not
evaluated here.
