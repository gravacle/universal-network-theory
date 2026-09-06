# Connected-cycle autonomous BS09 accumulation and owner-once action

## 1. Complete finite support and source

Use two four-site cycles `A` and `B`. Each has the four internal edges
`i--(i+1 mod 4)`. Add four connectors `A_i--B_(i+1 mod 4)`. Every edge joins
opposite head/tail parity, every site has degree three, and the eight-site
component is connected. Tile eight disjoint copies to cover the 64-site L4
record family. The owner-once census is 8 internal plus 4 connector edges per
component, hence 96 distinct active edges globally.

The input is exactly the audited uniform F3-MDC preparation: even tails blank,
odd heads `(B+x)/sqrt(2)`, 32 source lineages, and sources off during the
accumulation hold. No cycle receives a different source rule.

The complete selected carrier action is

\[
 H_{conn}=\epsilon_\psi Q-t\sum_{e\in E_{conn}}T_e, \tag{C01}
\]

with every physical edge in the displayed support summed once. Evolution is
the simultaneous exponential of (C01) at conditional `kappa=t tau/hbar=pi/2`.
There is no finite gate order or node-dependent stagger.

## 2. Owner-once CTP bookkeeping and ledger

For independently source-deformed forward/backward evolutions define the
finite closed-time-path bookkeeping functional

\[
 Z[\eta_+,\eta_-]
 =\operatorname{Tr}\!\left(U_+[\eta_+]\rho_0
 U_-^\dagger[\eta_-]\right),\qquad Z[0,0]=1.       \tag{C02}
\]

Each source differentiates one of the 96 edge terms in (C01), so no internal
or connector current is duplicated. Equation (C02) is a finite unitary record
functional. It is not a 1PI action, continuum contour, Ward identity, or
gravity action.

Orient the stored edge list once and let `B_(ve)=+1` at its tail and `-1` at
its head. Direct spectral integration of all twelve component current
operators verifies

\[
 q_v(\kappa)-q_v(0)+\sum_e B_{ve}J_e(\kappa)=0       \tag{C03}
\]

at every one of the eight sites. The global ledger is eight copies of (C03).
The terminal instrument remains the complete failure-inclusive product qutrit
read.

## 3. Finite result and claim classes

The zero-`kappa` control has no active current above the declared numerical
threshold. At `pi/2`, all eight internal and all four connector supports per
component carry physically nonzero integrated current. Expected retained
total remains 16 across the 64 sites. `RESULT.json` records the raw connector
and total throughput, correlations, connected-versus-disjoint comparison,
residuals, and norm/energy/number controls.

At `pi/2`, occupations alternate `0.2486888091/0.2513111909`. Every internal
and connector current has magnitude `0.0828962697`, with orientation
alternating under the stored owner order. Absolute throughput is
`0.9947552362` per component and `7.9580418896` globally; the connector/seam
part is `0.3315850787` per component and `2.6526806299` globally. Total
throughput is `1.5711763705` times the disjoint-cycle L4 baseline under the
same source and `kappa`. The largest connected edge correlation magnitude is
`0.0357710943`.

Across the zero and active rows, raw residual maxima are `2.110e-15` L1 and
`6.662e-16` Linf per component. Norm, energy, and number-law errors remain at
or below `6.662e-16`, `9.671e-16`, and `6.662e-16`. These last-bit values are
retained directly and are not assigned physical meaning.

**Proved:** finite connected support/census, owner-once Hamiltonian and CTP
bookkeeping, uniform source-preparation compatibility, and the discrete
continuity identity.

**Adopted:** inherited F3-MDC `alpha=r0`.

**Conditional:** the connected support program, `kappa`, separate hopping and
clock calibration, content sector, source routing, and complete read.

**Empirical/numerical:** the finite L4 occupations, all directly integrated
internal/connector currents, throughputs, correlations, residuals, and
controls.

**Open:** autonomous connected-support selection, connected scaling beyond
this L4 witness, generic phase behavior, and all macroscopic response.

Residuals are unassigned record-ledger terms, not defects. The enumeration
labels do not define a physical grid. No graph reward, continuum behavior,
Ward axiom, graviton, critical law, or gravity is introduced or inferred.
