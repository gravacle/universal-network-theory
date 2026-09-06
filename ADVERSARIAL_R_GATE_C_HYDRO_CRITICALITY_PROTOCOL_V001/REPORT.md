# Blind hostile structural review of the hydrodynamic criticality protocol

## Disposition

`PASS_BLIND_STRUCTURAL_PROTOCOL_SCREEN_WITH_FAIL_CLOSED_SCHEMA_NOTES`,
`26/26`.

This is a pass for the frozen protocol's exact finite bookkeeping, topology,
symmetry controls, and automatic stop/authorization logic. It is not a review
of any target spectrum and does not certify a critical density. The verifier
did not inspect a target numerical result. Physical graph/configuration work
was limited to L4, L6, and L8. L10/L12 occur only in rational bookkeeping and
synthetic state-machine fixtures; no larger graph, Hamiltonian, spectrum, or
response was constructed.

The independently pinned protocol SHA-256 is

```text
3da9e74b0dcc2d8b65ce98cfb42735864cf3d045e41655082baa7a7a295cb334
```

## Owner-once prism and fixed Hamiltonian

The reconstructed L4/L6/L8 prisms have respectively `8/12/16` sites and
`12/18/24` unique owner edges. Every site has degree three, every support is
connected, and every rail or shifted-connector edge crosses the axial-parity
bipartition. Every allowed configuration hop preserves carrier number.

The one-particle matrix is constructed only from this owner set. Its exact
Fourier eigenvectors reproduce

```text
epsilon(m,+/-) = -2 cos(2 pi m/L) +/- 1
```

with maximum explicit residuals `6.75e-16`, `3.32e-15`, and `5.69e-15` at
L4/L6/L8. Hashing the same integer matrix over every admissible write count
gives one signature at each size: there is no `H(N)` spectrum in the frozen
parent.

L6 has four one-particle zeros, at `(m,band)=(1,+),(2,-),(4,-),(5,+)`, while
L4 and L8 have none. These L6 zeros follow directly from commensurate momenta
with `cos(k)=+/-1/2`; they are not a density root.

## Exact chiral false-zero theorem

Color a `q`-carrier configuration by the parity of the number of occupied
sites in one axial sublattice. Every allowed hop reverses this color, so each
fixed-`q` Hamiltonian is exactly off-diagonal between the two configuration
sublattices. Their signed dimension difference is the coefficient of `x^q`
in

```text
(1-x)^L (1+x)^L = (1-x^2)^L.
```

Therefore

```text
N_plus-N_minus = (-1)^(q/2) binomial(L,q/2),  q even,
                 0,                           q odd.
```

The zero-energy nullity is consequently at least `binomial(L,q/2)` in every
even sector. Exhaustive L4/L6/L8 configuration enumeration verifies this
identity, chiral sign reversal on every hop, particle-hole hop equivalence,
and connectivity of every sector through half filling. Representative forced
zero lower bounds are:

| L | q=2 | q=4 | q=6 | q=8 |
|---:|---:|---:|---:|---:|
| 4 | 4 | 6 | — | — |
| 6 | 6 | 15 | 20 | — |
| 8 | 8 | 28 | 56 | 70 |

Thus raw zero energy, zero multiplicity, or generic level spacing would create
an immediate false criticality signal. The response-active projector weight
and pole-identity controls are mandatory.

The same connectivity makes the nonpositive fixed-sector hopping matrix
irreducible, supporting the protocol's unique Perron--Frobenius ground-state
premise for the scanned sectors. Particle-hole complementation maps every
hop in sector `q` to the corresponding hop in sector `2L-q` exactly.

## Density bookkeeping and cells

Exact rational summation of every authenticated `N`-write binomial record
through L8 gives

```text
sum_q p(q|N) = 1,
E[q]          = N/2,
Var(q)        = N/4,
E[rho]        = N/(4L),
Var(rho)      = N/(16 L^2).
```

The density cells, including the `q=0` bookkeeping cell, tile `[0,1/2]`
without gaps. Pure arithmetic verifies that the common authenticated
mean-density grid for L4/L6/L8/L10/L12 is exactly

```text
{0, 1/8, 1/4, 3/8, 1/2}.
```

It also verifies `rho_(4,N4)=rho_(8,2*N4)` for all authenticated L4 write
counts. This is only density arithmetic; it does not assert that differently
shaped source preparations select the same response.

## Automatic authorization screen

Exact rational fixtures exercise every gate disposition:

- no L4--L8 seed: `NO_CANDIDATE_L4_L8`, no larger calculation or response;
- unresolved seed: `UNRESOLVED`, no larger calculation or response;
- consistent seed only: `SEED_L4_L8`, authorizes only sparse L10/L12 spectral
  confirmation;
- confirmed connected interval with the gapless fit winning:
  `CANDIDATE_INTERVAL`, automatically authorizes spatial characterization and
  the three bounded response tracks;
- positive-gap fit winning: `NO_CANDIDATE`, all response tracks blocked;
- competing-cell ambiguity: `UNRESOLVED`, all response tracks blocked.

For the synthetic quarter-density fixture, the L4/L6/L8 seed-cell
intersection is `[7/32,9/32]`, and the L8/L10/L12 confirmed intersection is
`[11/48,13/48]`. These numbers test interval logic only and are not observed
candidate densities.

## Fail-closed schema notes

The frozen wording is executable with the following hostile interpretations:

1. If `sum_a w_a` is numerically indistinguishable from zero, `chi_tau` is
   undefined and the row is `UNRESOLVED`; it is not assigned zero or infinity.
2. A strict local density extremum requires both neighboring sector rows.
   Endpoint `q=1` or `q=L` is not a seed unless a new one-sided rule is frozen
   before inspection.
3. Degenerate-projector grouping should be repeated at tighter and looser
   energy grouping tolerances, not merely weight thresholds. If the first
   active pole changes identity, the row is `UNRESOLVED`.
4. The protocol's “three response tracks” are B--D. Spatial response A is the
   separately listed criticality characterization. All four are blocked until
   `CANDIDATE_INTERVAL`.
5. The five-size comparison needs one tracked cell/mode per size. Competing
   admissible cells cannot be selected retrospectively by best fit and are
   `UNRESOLVED`.

These notes close schema edge cases; they do not modify a physics definition
or authorize additional machinery.

## Claim boundary

The topology, density arithmetic, band formula, chiral imbalance identity,
particle-hole map, and authorization logic are exact finite results.
No target response-active spectrum has been inspected here. No `rho_c`, gap
closure, divergent susceptibility, algebraic response, predictive closure,
universal coupling, nonlocal potential, phase, continuum, graviton,
emergence, or gravity is established.
