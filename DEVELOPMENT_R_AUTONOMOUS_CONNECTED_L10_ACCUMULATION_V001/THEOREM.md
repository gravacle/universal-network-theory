# Refined L10 connected-cycle accumulation in the finite orbit basis

## 1. Finite parent and owner census

Extend the hostile-audited connected L4/L6/L8 family to two ten-site cycles
plus ten opposite-parity connectors per component. Fifty identical connected
degree-three components cover all 1,000 L10 sites. The two F3 layers contain
500 sites each and 250,000 possible links; the conditional support selects 20
internal plus 10 connector edges per component, 1,500 unique owner-counted
edges globally.

The source input remains uniform: every even tail is blank and every odd head
is `(B+x)/sqrt(2)`. There is no component-dependent preparation, node stagger,
or finite gate order. Source-off evolution is one simultaneous BS09
Hamiltonian exponential at conditional `kappa=t tau/hbar=pi/2`.

## 2. Exact finite compression, numerical evolution

One twenty-site component has 1,048,576 occupation words. The separately
hostile-audited finite group has order ten and partitions them into 105,376
normalized word orbits with size histogram
`{1:4, 2:6, 5:1020, 10:104346}`. The reduced owner-once Hamiltonian has
1,570,516 nonzero entries and zero displayed Hermiticity mismatch. This is the
same exact orbit construction already cross-checked against every full-state
L4/L6/L8 current and occupation.

The finite basis compression is exact. The state within it is evolved by an
order-10 short-step Taylor method. The final state and three symmetry-
representative current integrals are computed at 1,024 and 2,048 steps using
composite Simpson integration; the audited signed-edge identities reconstruct
all 30 currents. The 2,048-step row is reported. Neither the evolution nor the
quadrature is exact.

## 3. Owner-once current ledger

The global Hamiltonian is

\[
 H=-t\sum_{e\in E_{1500}}T_e,
\]

with each selected physical edge included once. The finite CTP bookkeeping
uses one deformation source per unique edge and obeys
`Z[0,0]=Tr(rho)=1`. It is a normalized finite unitary functional, not a 1PI
action or Ward identity.

With stored orientation and incidence matrix `B`, the refined raw ledger is

\[
 \Delta q+B J=r_{num}.                               \tag{L10-01}
\]

The refined occupations alternate `0.2606498343/0.2393501657`. All 20
internal currents and all 10 connector currents are active. Their respective
magnitudes are `0.0882859968` and `0.0840778407`. Raw absolute throughput is
`2.6064983430` per component and `130.3249171478` globally; the connector/seam
part is `0.8407784065` per component and `42.0389203272` globally. Expected
retained total is 250, and the observed numerical value differs by
`2.70e-12`.

The finite total/per-retained throughput comparisons are
`16.3765055469/1.0480963550` against L4,
`4.6400492202/1.0022506316` against L6, and
`1.9527650054/0.9998156828` against L8. These are raw finite records, not a
fitted scaling rule or continuum trend.

The current refinement difference is `1.978e-12`. Fine raw residuals are
`7.766e-12` L1 and `3.910e-13` Linf per component, with global tiled L1 bound
`3.883e-10`; the coarse L1 value is `1.262e-10`. The coarse/fine residual ratio
is `16.253`, a numerical convergence diagnostic rather than an exactness
proof. State and occupation refinement differences are `5.038e-15` and
`4.718e-15`. Norm and number-law errors are `2.132e-14` and `1.016e-14`, while
the recorded energy change is zero at displayed precision.

One passing run on the declared 48 GiB environment took `48.279534083 s` and
used `349,585,408` bytes (`333.390625 MiB`) maximum RSS. These are host
observations, not complexity claims.

## 4. Claim classes

**Proved:** the finite L10 support, connectivity, degree, site/link/lineage
census, owner-once action, finite CTP normalization, complete finite-orbit
partition and quotient Hermiticity, and exact retained-number commutation of
BS09.

**Adopted:** inherited F3-MDC `alpha=r0`.

**Conditional:** connected support, `kappa`, separate hopping and clock
calibration, content sector, source routing, and complete read.

**Empirical/numerical:** the evolved state, occupations, all internal and
connector currents, correlations, finite-size comparisons, residuals,
resource observation, and numerical control bounds.

**Open:** autonomous connected-support selection; a connected L12 or larger
record; generic phase behavior; and every macroscopic response question.

Residuals are raw unassigned record-ledger terms, not physical defects. Tuple
labels are finite enumeration, not a physical grid. No continuum behavior,
Ward axiom, critical law, graviton, or gravity is inserted or inferred.
