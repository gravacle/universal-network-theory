# Refined L12 connected-cycle accumulation

## 1. Finite parent and owner census

Extend the hostile-audited connected L4/L6/L8/L10 family to two twelve-site
cycles plus twelve opposite-parity connectors per component. Seventy-two
identical connected degree-three components cover all 1,728 L12 sites. The two
F3 layers contain 864 sites each and 746,496 possible links; the supplied
support selects 24 internal plus 12 connector edges per component, 2,592
unique owner-counted edges globally.

The source remains uniform: every even tail is blank and every odd head is
`(B+x)/sqrt(2)`. There is no component-dependent preparation, node stagger,
or finite gate order. Source-off evolution is one simultaneous BS09
Hamiltonian exponential at conditional `kappa=t tau/hbar=pi/2`.

## 2. Exact finite compression, bounded numerical evolution

One component has 16,777,216 occupation words. The separately hostile-audited
order-24 finite subgroup partitions them into 704,370 word orbits with
histogram
`{1:4, 2:6, 3:12, 4:30, 6:142, 8:15, 12:10316, 24:693845}`. The normalized
owner-once quotient has 12,582,508 nonzero entries, occupies 201,320,128 bytes
in its stored arrays, and has zero displayed Hermiticity mismatch. Two signed
edge orbits reconstruct every one of the 36 stored oriented currents without
imposing continuity.

The finite basis compression is exact. The state within it is evolved using
order-10 Taylor steps. To bound this larger finite run, final states and
representative current integrals are calculated with 512 and 1,024 time steps
using composite Simpson integration. The 1,024-step record is reported.
Neither evolution nor quadrature is exact.

## 3. Owner-once current ledger

The global Hamiltonian contains each of the 2,592 selected physical edges
once. The finite CTP bookkeeping assigns one deformation source to every
unique edge and obeys `Z[0,0]=Tr(rho)=1`. It is a normalized finite unitary
functional, not a 1PI action or Ward identity.

The refined occupations alternate `0.2606473909/0.2393526091`. All 24
internal currents and all 12 connector currents are active. Their respective
magnitudes are `0.0882850908` and `0.0840772094`. Raw absolute throughput is
`3.1277686913` per component and `225.1993457748` globally; the connector/seam
part is `1.0089265124` per component and `72.6427088935` globally. Expected
retained total is 432, with observed numerical difference `-2.16e-12`.

Finite total/per-retained throughput comparisons are
`28.2983363117/1.0480865301` against L4,
`8.0179298910/1.0022412364` against L6,
`3.3743462977/0.9998063104` against L8, and
`1.7279838016/0.9999906259` against L10. These are raw finite records, not
monotonicity, a limit, fitted scaling, or a continuum trend.

The 512/1,024 current refinement difference is `3.165e-11`. Fine raw
record-ledger residuals are `1.430e-10` L1 and `5.960e-12` Linf per component,
with global tiled L1 bound `1.030e-8`; coarse L1 is `2.418e-9`. Their ratio is
`16.906`, a numerical Simpson-consistency diagnostic, not an exactness proof.
State and occupation refinement differences are `9.576e-16` and `1.443e-15`.
Norm and number-law errors are `7.216e-15` and `1.277e-15`, while energy
change is zero at displayed precision.

One passing run on the declared 48 GiB environment took `321.367049417 s` and
used `2,399,076,352` bytes (`2.23431396484375 GiB`) maximum RSS. These are host
observations, not complexity claims.

## 4. Claim classes

**Proved:** finite L12 connectivity, degree, site/link/lineage census,
owner-once action, finite CTP normalization, complete orbit and signed-edge
partitions, quotient Hermiticity, and exact retained-number commutation of
BS09.

**Adopted:** inherited F3-MDC `alpha=r0`.

**Conditional:** connected support, `kappa`, separate hopping/clock
calibration, content sector, source routing, and complete read.

**Empirical/numerical:** evolved state, occupations, all currents,
correlations, finite-size comparisons, residuals, resource observation, and
refinement/conservation controls.

**Open:** an L14 or later finite record; autonomous support selection; any
onset, collective, or generic-phase interpretation; and every macroscopic
response question.

Residuals remain raw unassigned record-ledger terms, not physical defects.
“Prism” is a finite graph relabeling, not a physical grid. No continuum
behavior, Ward axiom, critical law, graviton, or gravity is inserted or
inferred.
