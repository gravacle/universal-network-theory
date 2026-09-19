# Low-memory terminal supplement V002

The V001 controls validate prefix allocation but materialize the terminal
control block and retain the sealed Lanczos basis. They do not exercise the
L12 terminal path. V002 changes only the executable representation:

1. the final event is emitted as complete last-lineage-bit-zero and
   last-lineage-bit-one row windows;
2. blank and occupied carrier columns remain in one child-zero vector, so
   their physical interference is retained;
3. all currents are signed-summed over rows and children before connector L1
   aggregation and node-ledger norms;
4. an adaptive time-subdivided Lanczos path caps each physical work set at
   `1,000,000,000 B`, including its basis and four live vectors; and
5. L10 terminal q=9 and q=10 force this path even though their natural rows
   fit, making the benchmark exercise the L12 algorithm.

The large-row path retains the same Hamiltonian, admission angle, total route
time, coarse/fine tolerances, and Gauss--Legendre order. It subdivides time
until two retained Krylov endpoints and their residual indicator satisfy the
per-segment tolerance. At most sixteen subdivisions are allowed; failure is
`UNRESOLVED`.

For L12 the exact terminal supports are refined to

```text
child zero: C(35,11) = 417,225,900
child one:  C(34,11) = 286,097,760
```

Neither child may be materialized in full. This supplement remains hard-
locked at L12 until its V002 controls and the separately frozen target/hostile
L10 benchmark pass.
