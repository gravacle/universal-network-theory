# Fixed-width finite engine validation

## 1. Exact representation

For each sealed `L=4,6,8,10` connected component, the validator reconstructs
the complete order-`2L` source-preserving finite group. Two `L`-bit chunk
tables implement each group permutation exactly. Burnside's count sizes the
representative and byte-sized orbit-size arrays; compiled enumeration assigns
every binary word to exactly one orbit and verifies the counted sizes sum to
the full word space.

For each representative word and each active owner-once edge, the engine
stores one unaggregated destination and the normalized coefficient

\[
 -\sqrt{|O_a|/|O_b|}.                                  \tag{FW-01}
\]

Repeated destinations remain repeated, so their sum is the prior aggregated
coefficient. This changes storage, not the finite owner-once action.

## 2. Signed current reduction

The source-preserving group gives two signed edge orbits, internal and
connector. For an invariant state, the expectation on a representative edge
equals the appropriately normalized signed sum over that complete finite edge
orbit. The engine evaluates those two signed operator sums directly from the
same owner-once transitions and reconstructs every oriented edge value with
the audited signs. This is a finite operator identity. It does not insert a
continuity equation or Ward axiom; the record-ledger residual remains a
separate numerical check.

## 3. Lower-size numerical parity

At conditional `kappa=pi/2`, order-10 Taylor evolution and 2,048-panel Simpson
integration reproduce every sealed L4/L6/L8/L10 occupation, oriented current,
and maximum connected-edge correlation within `4e-11`. Direct record-ledger,
norm, energy, and particle-number checks also pass. The orbit partitions and
transition ceilings are exact; evolution and quadrature remain numerical.

An initial pre-result trial failed closed because NumPy evaluated
`sqrt(uint8)` in float16 when preparing orbit amplitudes. Explicit float64
promotion repaired the implementation. No failed-trial value is promoted.

## 4. Claim classes

**Proved:** the finite orbit construction, unaggregated owner-once transition
equivalence, and signed finite edge-orbit operator reduction.

**Adopted:** inherited F3-MDC `alpha=r0` and the sealed connected component
family.

**Conditional:** source, support, `kappa`, content, routing, clock, read, and
fixed-width implementation choices.

**Empirical/numerical:** evolved states, currents, correlations, and residual
tolerances at L4/L6/L8/L10.

**Open:** independent hostile audit and any L14 construction or evolution.

No autonomous support, physical grid, continuum behavior, Ward identity,
phase, graviton, gravity, convergence, limit, fit, scaling, or complexity law
is claimed.
