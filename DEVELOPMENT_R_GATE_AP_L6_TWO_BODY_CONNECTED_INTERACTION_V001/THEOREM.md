# Finite L6 four-history connected-response statement

## Parent, writes, and histories

Let the physical support be the already audited owner-once L6 prism with 12
sites and 18 hopping edges. On the all-blank state, the two distinct local
write factors commute and each applies

\[
 |B\rangle\longmapsto
 \frac{|B\rangle-i|x\rangle}{\sqrt2},
 \qquad W_1=W_2=\frac12.
\]

Thus the terms-off write ledgers are exactly

\[
 \Delta Q+\sum_eJ_e-W_a=\frac12+0-\frac12=0
\]

for either single write and

\[
 \Delta Q+\sum_eJ_e-W_1-W_2
 =1+0-\frac12-\frac12=0
\]

for the double write. `O00`, `O10`, `O01`, and `O11` denote the no-write,
first-only, second-only, and double-write histories. Once written, both
sources and writers are off and all four histories evolve under the same
complete owner-once prism Hamiltonian.

The alternating accumulation baseline cannot serve this odd-separation
protocol: its authenticated blank targets lie on only one bipartite
sublattice. The all-blank vacuum is therefore a declared conditional parent,
not a relabeling of that accumulated baseline.

## Exact connected definition and ledger

For every retained observable,

\[
 \Delta_{12}O(d)=O_{11}(d)-O_{10}-O_{01}+O_{00}.
\]

Initial occupation is additive, so `Delta12 q_before=0` exactly. Subtracting
the four owner-once continuity identities gives

\[
 \Delta_{12}q_{\rm after}-\Delta_{12}q_{\rm before}
 +B\Delta_{12}J=r_{\rm num}^{(12)}.
\]

The source terms cancel. Incidence columns telescope exactly, and the stored
binary64 connected-ledger L1 remainders are below `1.7e-15`.

## Hamiltonian energy

The network Hamiltonian is

\[
 H=-\sum_{(u,v)\in E}
 (|xB\rangle\langle Bx|+|Bx\rangle\langle xB|)_{uv}.
\]

The vacuum and either single-write state have zero expectation. For two
equal-phase writes, a directly occupied support edge contributes exactly
`-1/2`; a nonedge contributes zero. Hence, for the canonical pairs
`(A0,A1)`, `(A0,A2)`, and `(A0,A3)`,

\[
 \Delta_{12}E(1)=-\frac12,
 \qquad
 \Delta_{12}E(2)=\Delta_{12}E(3)=0.
\]

Time independence follows from evolution under the same Hamiltonian. The
stored final values reproduce these identities within `1.3e-15`.

## Complete finite evolution

All four histories occupy only number sectors zero, one, and two. Since `H`
conserves number, their dimensions `1+12+66=79` exactly exhaust the reachable
part of the full `2^12=4096` word space. The target diagonalizes the complete
79-dimensional restriction, analytically integrates every current matrix
element, embeds the result in all 4096 words, and checks the raw physical-hop
action. The full-word embedding error is `1.11e-16`, with no amplitude or
Hamiltonian action outside the retained sectors.

The finite result is

| d | `Delta12 E` | `sum abs Delta12 J` | `max abs Delta12 J_e` | connected ledger L1 |
|---:|---:|---:|---:|---:|
| 1 | `-0.5` | `0.26695732547505335` | `0.04154319898895599` | `1.2611439670351388e-15` |
| 2 | `0` (`4.65e-16` final roundoff) | `0.8946409434809176` | `0.09319924937698945` | `1.3183898417423734e-15` |
| 3 | `0` (`-4.30e-16` final roundoff) | `0.2936201703231855` | `0.04319870224705729` | `1.627170620466245e-15` |

Strict current superposition is therefore false on this finite coherent
protocol. The energy screen does not show mutual attractive binding over all
three separations: it shows one direct-contact negative term and zero
noncontact energy. A connected coherent current is not, without an additional
energy or force construction, a long-range exchange potential.

## Claim classes

**Proved:** owner-once L6 prism census; exact blank-target write ledgers;
four-history inclusion-exclusion identity; completeness of the reachable
zero/one/two number sectors; exact contact-energy formula.

**Adopted:** F3-MDC `alpha=r0`, `kappa=pi/2`, and canonical A-ring pair
representatives.

**Conditional:** the all-blank vacuum parent, pair orientation, common source
phase, and write/transport schedule.

**Empirical:** the binary64 finite L6 current vectors and numerical ledger
remainders.

**Open:** independent hostile audit; other pair orbits and phases; larger
supports; a physical distance map; an energy-defined noncontact potential;
binding; and Gate A-P.

No long-range exchange potential, scaling law, grid, continuum behavior,
Ward identity, phase, graviton, or gravity is claimed.
