# Order-2L finite prism-orbit compression

## 1. Finite relabeling and source-preserving group

Label the supplied component vertices `(a,i)` with two cycle labels
`a in {0,1}` and `i mod L`. Relabel only for combinatorial calculation by
`x=i-a`. The two cycle edge sets and shifted connectors then form the abstract
prism graph `C_L square K_2`.

For `epsilon in {+1,-1}` and `k mod L`, define in the relabeled graph

\[
 x'=\epsilon x+k,\qquad a'=a\mathbin{\mathrm{xor}}(k\bmod 2),
 \qquad i'=x'+a'.                                      \tag{PR-01}
\]

These `2L` distinct vertex permutations preserve the declared undirected
support. They also preserve the parity of the original site label `i`, hence
the uniform source pattern with even tails blank and odd heads in
`(B+x)/sqrt(2)`. Equation (PR-01) defines a finite automorphism subgroup. The
packet does not claim that it is the maximal automorphism group.

“Prism” has no physical content here. It names an isomorphism of a finite
support graph and supplies neither spatial coordinates nor a grid.

## 2. Exact orbit quotient and edge reconstruction

The group partitions occupation words into complete orbits. For normalized
word-orbit states, the owner-once quotient entry remains exactly

\[
 (H_{orb})_{ba}=-n_{ab}\sqrt{|O_a|/|O_b|}.             \tag{PR-02}
\]

Complete enumeration produces:

| L | full dimension | orbit dimension | group order | quotient nonzeros |
|---:|---:|---:|---:|---:|
| 4 | 256 | 55 | 8 | 184 |
| 6 | 4,096 | 430 | 12 | 3,044 |
| 8 | 65,536 | 4,435 | 16 | 49,076 |
| 10 | 1,048,576 | 53,764 | 20 | 786,300 |

Every quotient has zero displayed Hermiticity mismatch. Applying the group to
oriented owner edges gives two consistent signed edge orbits—internal and
connector—at each size. Their signs reconstruct every stored oriented current
without inserting a continuity equation.

## 3. Lower-size full-record cross-check

At conditional `kappa=pi/2`, order-10 Taylor evolution and 2,048-panel Simpson
integration in the new orbit bases give:

| L | max occupation difference | max signed-current difference | ledger L1 |
|---:|---:|---:|---:|
| 4 | `6.994e-15` | `1.268e-13` | `3.043e-12` |
| 6 | `3.719e-15` | `7.355e-16` | `4.743e-12` |
| 8 | `1.110e-15` | `1.527e-16` | `6.328e-12` |
| 10 | `4.441e-16` | `1.568e-15` | `7.742e-12` |

All values agree with the sealed records inside the declared numerical
envelope. Norm, energy, number-sector law, and direct continuity checks also
pass. The cross-check is numerical evidence for using the exact finite basis;
it does not make evolution or quadrature exact.

## 4. L12 feasibility screen

A separate pre-target structural screen applies the same enumerated group at
L12. It observes `16,777,216 -> 704,370` word orbits, histogram
`{1:4, 2:6, 3:12, 4:30, 6:142, 8:15, 12:10316, 24:693845}`, and 12,582,508
quotient entries. Quotient arrays occupy `191.9938 MiB`; one reduced
Hamiltonian action took `0.013946 s`, and construction reached
`1,703,739,392` bytes (`1.58673 GiB`) maximum RSS on the declared 48 GiB host.
These are unpromoted feasibility observations, not an L12 evolution result or
complexity law.

## 5. Claim classes

**Proved:** the order-`2L` finite permutation set at L4/L6/L8/L10; support and
source-parity preservation; complete word and signed-edge orbit partitions;
quotient normalization; and owner-once equivalence in the invariant subspace.

**Adopted:** inherited F3-MDC `alpha=r0`.

**Conditional:** connected support, `kappa`, separate hopping/clock
calibration, content sector, source routing, and complete read.

**Empirical/numerical:** evolved states, lower-size comparisons, residuals,
conservation tolerances, and L12 feasibility resource observations.

**Open:** a refined L12 evolution; autonomous support selection; any generic
phase or collective interpretation; maximality of the group; and every
macroscopic response question.

This packet adds no interaction, physical grid, continuum assumption, Ward
axiom, critical law, graviton, or gravity. Residuals remain unassigned
record-ledger terms, not defects.
