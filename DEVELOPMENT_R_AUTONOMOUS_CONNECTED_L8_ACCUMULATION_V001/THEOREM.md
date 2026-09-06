# Refined L8 connected-cycle autonomous accumulation

## 1. Finite parent and owner census

Replace each six-site cycle in the audited connected L6 witness by an
eight-site cycle and retain the same owner rule: two cycles plus eight
opposite-parity connectors form one connected degree-three component.
Thirty-two components cover all 512 L8 sites. The two F3 layers contain 256
sites each and 65,536 possible links; the conditional support selects 16
internal plus 8 connector edges per component, 768 unique owner-counted edges
globally.

The source input remains uniform: every even tail is blank and every odd head
is `(B+x)/sqrt(2)`. There is no component-dependent preparation, node stagger,
or finite gate order. Source-off evolution is one simultaneous BS09
Hamiltonian exponential at conditional `kappa=t tau/hbar=pi/2`.

## 2. Matrix-free controlled integration

One component has 16 qutrit occupation sites in the fixed-content blank/`x`
sector, hence 65,536 basis states. The computation applies
`H=-sum_e T_e` without allocating its dense matrix. Each short unitary step is
evaluated through order ten in its Taylor series. The final state and all 24
oriented-current integrals are computed independently with 1,024 and 2,048
time steps; composite Simpson integration is used for the currents.

The 2,048-step row is the reported record. `RESULT.json` retains the maximum
coarse/fine differences in the state, occupations, and currents, as well as
both coarse and fine continuity residuals. These controls classify numerical
integration error directly. They do not turn it into an exact result or a
physical defect.

## 3. Finite CTP and ledger boundary

The owner-once Hamiltonian contains each of the 768 selected physical edges
once. The finite CTP bookkeeping uses one deformation source per unique edge
and obeys `Z[0,0]=Tr(rho)=1`. It remains a normalized finite unitary
functional, not a 1PI action or Ward identity.

With the stored orientation and incidence matrix `B`, the refined raw ledger
is

\[
 \Delta q+B J=r_{num}.                               \tag{L8-01}
\]

Every component residual, its global tiled bound, and its 1,024-to-2,048-step
change are reported rather than set to zero.

The refined occupations alternate `0.2606978854/0.2393021146`. All 16
internal currents and all 8 connector currents are active. Their respective
magnitudes are `0.0882983706` and `0.0841011442`. Raw absolute throughput is
`2.0855830833` per component and `66.7386586644` globally; the connector/seam
part is `0.6728091539` per component and `21.5298929261` globally. Expected
retained total is 128, and the observed numerical value differs by
`4.15e-12`.

The L8/L4 total-throughput ratio is `8.3863165827`; per retained record it is
`1.0482895728`. The L8/L6 total-throughput ratio is `2.3761431648`; per
retained record it is `1.0024353977`. These are finite comparator records, not
a fitted scaling rule.

The current refinement difference is `1.976e-12`. Fine raw residuals are
`6.321e-12` L1 and `4.034e-13` Linf per component, with global tiled L1 bound
`2.023e-10`; the coarse L1 value was `1.010e-10`. State and occupation
refinement differences are `2.172e-15` and `8.826e-15`. Norm and number-law
errors are `3.730e-14` and `1.832e-14`, while the recorded energy change is
zero at displayed precision.

One passing run on the declared 48 GiB environment took `55.522473084 s` and
used `73,613,312` bytes (`70.203125 MiB`) maximum RSS. These are host
observations, not complexity claims.

## 4. Claim classes

**Proved:** the finite L8 support, connectivity, degree, site/link/lineage
census, owner-once action, finite CTP normalization, and exact retained-number
commutation of BS09.

**Adopted:** inherited F3-MDC `alpha=r0`.

**Conditional:** connected support, `kappa`, separate hopping and clock
calibration, content sector, source routing, and complete read.

**Empirical/numerical:** the refined state, occupations, all internal and
connector currents, correlations, L8/L4 and L8/L6 comparisons, residuals,
resource observation, and numerical control bounds.

**Open:** autonomous connected-support selection; a connected L10 or larger
trajectory; generic phase behavior; and every macroscopic response question.

Residuals are raw unassigned record-ledger terms, not physical defects. Tuple
labels are finite enumeration, not a physical grid. No continuum behavior,
Ward axiom, critical law, graviton, or gravity is inserted or inferred.
