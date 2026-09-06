# Refined L6 connected-cycle autonomous accumulation

## 1. Finite parent and owner census

Replace each four-site cycle in the audited connected L4 witness by a six-site
cycle and retain the same owner rule: two cycles plus six opposite-parity
connectors form one connected degree-three component. Eighteen components
cover all 216 L6 sites. The two F3 layers contain 108 sites each and 11,664
possible links; the conditional support selects 12 internal plus 6 connector
edges per component, 324 unique owner-counted edges globally.

The source input remains uniform: every even tail is blank and every odd head
is `(B+x)/sqrt(2)`. There is no component-dependent preparation, node stagger,
or finite gate order. Source-off evolution is one simultaneous BS09
Hamiltonian exponential at conditional `kappa=t tau/hbar=pi/2`.

## 2. Matrix-free controlled integration

One component has 12 qutrit occupation sites in the fixed-content blank/`x`
sector, hence 4,096 basis states. The computation applies
`H=-sum_e T_e` without allocating its dense matrix. Each short unitary step is
evaluated through order ten in its Taylor series. The final state and all 18
oriented-current integrals are computed independently with 1024 and 2048 time
steps; composite Simpson integration is used for the currents.

The 2048-step row is the reported record. `RESULT.json` retains the maximum
coarse/fine differences in the state, occupations, and currents, as well as
both coarse and fine continuity residuals. These controls classify numerical
integration error directly. They do not turn it into an exact result or a
physical defect.

## 3. Finite CTP and ledger boundary

The owner-once Hamiltonian contains each of the 324 selected physical edges
once. The finite CTP bookkeeping uses one deformation source per unique edge
and obeys `Z[0,0]=Tr(rho)=1`. It remains a normalized finite unitary
functional, not a 1PI action or Ward identity.

With the stored orientation and incidence matrix `B`, the refined raw ledger
is

\[
 \Delta q+B J=r_{num}.                               \tag{L6-01}
\]

Every component residual, its global tiled bound, and its 1024-to-2048-step
change are reported rather than set to zero.

The refined occupations alternate `0.2600645249/0.2399354751`. All twelve
internal currents and all six connector currents are active. Their respective
magnitudes are `0.0882107462` and `0.0836430325`. Raw absolute throughput is
`1.5603871492` per component and `28.0869686859` globally; the connector/seam
part is `0.5018581948` per component and `9.0334475069` globally. Expected
retained total is 54, and the observed numerical value differs by
`2.64e-12`. The L6/L4 total-throughput ratio is `3.5293818600`; per retained
record it is `1.0457427733`. These are finite comparator records, not a fitted
scaling rule.

The current refinement difference is `1.974e-12`. Fine raw residuals are
`4.740e-12` L1 and `4.073e-13` Linf per component, with global tiled L1 bound
`8.532e-11`; the coarse L1 value was `7.569e-11`. State and occupation
refinement differences are `3.061e-15` and `1.483e-14`. Norm and number-law
errors are `4.020e-14` and `1.810e-14`, while the recorded energy change is
zero at displayed precision.

## 4. Claim classes

**Proved:** the finite L6 support, connectivity, degree, site/link/lineage
census, owner-once action, finite CTP normalization, and exact retained-number
commutation of BS09.

**Adopted:** inherited F3-MDC `alpha=r0`.

**Conditional:** connected support, `kappa`, separate hopping and clock
calibration, content sector, source routing, and complete read.

**Empirical/numerical:** the refined state, occupations, all internal and
connector currents, correlations, L6/L4 comparisons, residuals, and numerical
control bounds.

**Open:** autonomous connected-support selection; a connected L8 or larger
trajectory; generic phase behavior; and every macroscopic response question.

Residuals are raw unassigned record-ledger terms, not physical defects. Tuple
labels are finite enumeration, not a physical grid. No continuum behavior,
Ward axiom, critical law, graviton, or gravity is inserted or inferred.
