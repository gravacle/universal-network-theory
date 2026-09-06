# Exact finite-orbit compression of connected records

## 1. Finite group

For even cycle length `L`, label the two cycles by `(a,i)` with `a in {0,1}`
and `i mod L`. The declared support contains both cycle-edge sets and the
connectors `(0,i)--(1,i+1)`. Define

\[
 T(a,i)=(a,i+2),\qquad S(a,i)=(1-a,-i).
\]

`T` has order `L/2`, `S` has order two, and `STS=T^{-1}`. Their `L` distinct
permutations preserve the undirected support. They also preserve site parity,
so they leave the uniform F3-MDC source state—blank on every even tail and
`(B+x)/sqrt(2)` on every odd head—invariant. This is an exact automorphism
group of the supplied finite support, not a spacetime or continuum symmetry.

## 2. Orbit Hamiltonian

Let `O_a` be an orbit of occupation words and

\[
 |O_a\rangle=|O_a|^{-1/2}\sum_{w\in O_a}|w\rangle .
\]

Because the owner-once BS09 hopping sum commutes with every group
permutation, the invariant source evolves inside the orbit span. If a
representative of `O_a` has `n_ab` active owned-edge swaps into `O_b`, the
reduced matrix element is exactly

\[
 (H_{orb})_{ba}=-n_{ab}\sqrt{|O_a|/|O_b|}.             \tag{OR-01}
\]

The validator enumerates every orbit and transition rather than assuming a
translation law. Its reduced matrices are Hermitian to exact displayed
floating evaluation (`0.0` mismatch) at all three validation sizes.

The orbit dimensions are:

| L | full dimension | orbit dimension | finite group order | reduced nonzero entries |
|---:|---:|---:|---:|---:|
| 4 | 256 | 76 | 4 | 340 |
| 6 | 4,096 | 720 | 6 | 5,948 |
| 8 | 65,536 | 8,356 | 8 | 97,684 |

## 3. Current reconstruction and full-state tests

Even translations reduce the current calculation to cycle-0 even/odd edge
representatives and one even connector. Reflection gives

\[
 J_{1,i}=-J_{0,-i-1},\qquad K_i=-K_{-i-1},             \tag{OR-02}
\]

with the edge orientations used in the sealed full-state packets. The
validator computes each representative expectation from the complete word
orbit map and reconstructs every oriented edge current.

Using the same conditional `kappa=pi/2`, order-10 Taylor evolution, and 2,048
Simpson panels, the reduced calculation compares with every full-state
occupation and current as follows:

| L | max occupation difference | max signed-current difference | ledger L1 |
|---:|---:|---:|---:|
| 4 | `6.828e-15` | `1.266e-13` | `3.054e-12` |
| 6 | `2.831e-15` | `4.163e-16` | `4.739e-12` |
| 8 | `2.665e-15` | `4.163e-16` | `6.330e-12` |

Norm, energy, and complete number-sector law controls also pass. These are
numerical cross-checks of an algebraically exact finite basis reduction. They
do not make the time evolution or current quadrature exact.

## 4. Claim classes

**Proved:** the declared finite group action; preservation of support and
source parity; complete orbit partitions; formula (OR-01); symmetry current
reconstruction (OR-02); and owner-once equivalence within the invariant
subspace.

**Adopted:** inherited F3-MDC `alpha=r0`.

**Conditional:** the connected support, `kappa`, separate hopping/clock
calibration, content sector, source routing, and complete read.

**Empirical/numerical:** all evolved states, cross-size numerical differences,
ledger residuals, correlations, and conservation tolerances.

**Open:** use of the validated reduction for L10; autonomous support selection;
generic phase behavior; and every macroscopic response question.

This packet adds no physical interaction, boundary, grid, or continuum
assumption. Residuals remain unassigned record-ledger terms, not defects. It
does not insert or infer a Ward axiom, critical law, graviton, or gravity.
