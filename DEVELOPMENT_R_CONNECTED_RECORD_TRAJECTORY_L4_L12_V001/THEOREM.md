# Audited connected-record trajectory through L12

## 1. Append-only custody

The packet pins the sealed L4--L10 trajectory hash and the hostile-audited L12
result hash. It preserves the prior four rows and three adjacent comparators,
then compiles the L12 row by the identical arithmetic definitions. No earlier
record is recomputed, rounded, or replaced.

## 2. Five finite records

| L | sites | lineages | retained | owner-once edges | total throughput | throughput / retained |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 64 | 32 | 16 | 96 | `7.9580418896` | `0.4973776181` |
| 6 | 216 | 108 | 54 | 324 | `28.0869686859` | `0.5201290497` |
| 8 | 512 | 256 | 128 | 768 | `66.7386586644` | `0.5213957708` |
| 10 | 1,000 | 500 | 250 | 1,500 | `130.3249171478` | `0.5212996686` |
| 12 | 1,728 | 864 | 432 | 2,592 | `225.1993457748` | `0.5212947819` |

Connector throughput per retained record is
`0.1657925394, 0.1672860649, 0.1682022885, 0.1681556813, 0.1681544187`.
Maximum absolute connected edge correlations are
`0.0357710943, 0.0345321434, 0.0353698326, 0.0360091085, 0.0360485022`.

The L10-to-L12 site and analytic prepared-retention ratio is `1.728`. Its raw
total-throughput ratio is `1.7279838016`, and its per-retained ratio is
`0.9999906259`. The raw connector ratio is `1.7279870255`, and its
per-retained ratio is `0.9999924916`. These are one adjacent finite comparison,
not a convergence or limiting-value result.

The L12 per-component numerical residual is `1.430e-10` L1 and `5.960e-12`
Linf, with tiled global L1 bound `1.030e-8`. It remains distinct from the
lower packets' different quadrature histories and is not renamed a defect.

## 3. Claim classes

**Proved:** input-hash custody; append-only preservation of the sealed L4--L10
rows; the L12 finite census; and arithmetic definitions of the appended
comparators.

**Adopted:** inherited F3-MDC `alpha=r0`.

**Conditional:** support, `kappa`, hopping/clock calibration, content, routing,
and complete read in every row.

**Empirical/numerical:** all occupations, currents, throughputs, correlations,
residuals, and finite comparator values.

**Open:** the behavior of any later finite record; autonomous support
selection; onset or collective interpretation; and every macroscopic response
question.

The close L10/L12 normalized values do not establish monotonicity,
convergence, a limit, exponent, fit, or scaling law. No physical grid,
continuum, Ward identity, critical or generic phase, graviton, or gravity is
inserted or inferred.
