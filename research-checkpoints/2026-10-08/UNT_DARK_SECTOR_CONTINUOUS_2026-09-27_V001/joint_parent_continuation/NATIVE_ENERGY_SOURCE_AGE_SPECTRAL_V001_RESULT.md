# Energy-source age spectrum: signed static response, not a passive closure

2026-09-30. Source-informed interpretation of the saved root-produced result.
This review reads existing source and result bytes; it does not rerun the
producer, import it, reconstruct an independent eigensolve, or propagate states.
The reviewer authored the producer. The separate independent source preflight
is `NATIVE_ENERGY_SOURCE_AGE_SPECTRAL_PREFLIGHT_INDEPENDENT_V001.md`; neither
review is an independent numerical reproduction.

## Result and its scope

All four original preparations have a negative dipole static susceptibility
in the **uncertified numerical stationary comparator**. Source-age averaging
therefore does not supply evidence for the proposed all-positive passive
dipole spectral closure for these preparations. This is not a no-go for UNT,
a physical antigravity result, or a determination of astronomical gravity.

The saved run completed 325 arithmetic checks with no reported failures,
exactly two 96-by-96 eigensolves, four initial preparations and checks of all
20 previously saved states. The checks concern the frozen apparatus and
numerical consistency, not 325 independent confirmations of its physics.
All 4560 unordered eigen-index pairs per model and every preparation's full
coherences are retained, including weak and negative contributions.

No unresolved energy cluster was found at the frozen numerical resolution.
The minimum positive numerical gaps are 0.0014757205893340952 for A and
0.0008776448719531871 for B, compared with neighborhood half-widths
2.7938631393633555e-9 and 2.7537037275809467e-9. These neighborhoods are NOT
rigorous eigenvalue inclusion intervals. This justifies the producer's
descriptive `UNCERTIFIED_NUMERICAL_NONDEGENERATE_DIAGNOSTIC` branch, not an
exact-degeneracy proof or a certified inverse-gap bound.

The source coordinates are the inherited dimensionless `(alpha,eta)`,
`alpha=gamma0*a_ext`, with `G=(Z/gamma0,-B_eta)` and microscopic `hbar=1`.
Values below are rounded from the saved full-precision fields. The moment
is evaluated in the numerical stationary comparator, NOT at a selected
instantaneous age.

| Preparation | Dipole chi0 | Dipole chi2 | Dipole first moment | Volume chi0 |
| --- | ---: | ---: | ---: | ---: |
| A minus | -1.88241705 | -2827.63035 | +0.07032016 | +0.17961120 |
| A plus | -2.03263568 | +5300.53906 | -0.03229560 | +0.29510372 |
| B minus | -1.20476628 | -1.31833620 | +0.11876623 | +0.96830282 |
| B plus | -2.25622175 | +8.58882562 | -0.38224105 | -4.93454363 |

## What the signs establish conditionally

For an exact stationary spectrum under the reviewed conventions,

    chi0 = 2 sum_(Delta>0) M_Delta/Delta,
    chi2 = 2 sum_(Delta>0) M_Delta/Delta^3,
    first_moment = 2 sum_(Delta>0) Delta*M_Delta.

An exact negative dipole chi0 would require some negative dipole spectral
weight even after correctly grouping equal gaps. It is incompatible with
an everywhere nonnegative dipole spectral measure. The four saved negative
values are numerical evidence of that obstruction in these fixed
preparations, not a directed-rounding certificate of the exact signs.
No transition-resolution group has been promoted to an exact equal-gap
group or a physical resolved line.

Positive first moments in the two minus preparations do not cure their
negative chi0: the sums use different gap weights. Conversely, positive
chi2 in the two plus preparations is not passivity, positive physical
inertia, or evidence of a viable constitutive law. A selected coefficient
cannot replace the signed source spectrum, contact terms and retained
memory. Strictly subgap absorption is identically absent for any stationary
finite spectrum, including an inverted one; that absence would not provide
a useful passivity test.

The Hamiltonian uses a PLUS source. Its conjugate-energy response has
work curvature `<C>-chi`, not `chi`. Here `C_alphaalpha=0` within the owned
affine lapse family, so the positive dipole entries of `<C>-chi0` are simply
the negatives of the four chi0 values above. This sign bookkeeping does
not derive gravitational attraction, a source field equation, a positive
mechanical mass, or a physical lapse/clock calibration. The adopted weak-lapse
dictionary and source assignments remain premises of
`NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md`.

## Conditional reflection explanation of small mixed responses

There is an exact algebraic reflection of the declared two-endpoint
apparatus: exchange the left and right record factors and exchange the
carrier endpoints, leaving Q, C and incidence unchanged. Call this unitary
`R`. The owned A/B Hamiltonians commute with R. Their sums, including the
formation term, make `B_eta` and `C_etaeta` even. The differences
`DeltaP`, `DeltaR` and `DeltaX` make `Z/gamma0` odd. The B mixed contact
`C_alphaeta` is odd; A's mixed contact is identically zero.

For any R-invariant density matrix, the dipole/volume commutator response
and mixed-contact expectation consequently vanish exactly. If the exact
Hamiltonian spectrum is nondegenerate, each energy eigenstate has definite
reflection parity, so exact energy dephasing of any initial state has this
invariance. Equivalently, an odd and an even source cannot both connect
the same two definite-parity states.

The numerical diagonal comparator therefore has a symmetry-based reason
for its tiny mixed entries under its nondegenerate-spectrum assumption.
Saved static mixed entries are of order 1e-14; the larger, still small
chi2 mixed entries are consistent with inverse-cube gap weighting
amplifying numerical remnants of a parity null. This is an explanation
from the source algebra, NOT an additional numerical symmetry audit or
an error certificate.

The initial left-carrier state itself is NOT reflection invariant. Neither
its actual finite-age state nor a finite-duration age average is thereby
proved to have zero mixed response. Exact cross-parity energy degeneracies
could preserve odd coherences inside a full energy block. The present
ordinary eigensolve does not certify their absence, so the application of
the symmetry to the exact infinite-age comparator remains conditional.

## Readout is not preparation

No physical T, lag cutoff L, damping kappa, or frequency window was chosen
or evaluated. The retained age-envelope and remainder inputs allow later
explicit readout/error analysis; they are not measured relaxation times.
The original conserved populations and transient coherences are preserved.
Constructing a numerical energy-diagonal comparator does not physically
dephase the system, form a passive state, cool a reservoir, or justify
interchanging the infinite-age and zero-frequency limits.

This diagnostic closes none of the eleven scientific lanes. All 16 saved
qualification flags remain false, including passivity, physical readout
window, source-age error certification, rigorous gap/eigenvalue bounds,
stationary preparation, native metric, continuous soft spectrum, physical
source validation, mechanical mapping, galaxy polarization, vacuum
normalization, observational success and Stage 3 completion. It does not
make DM or DE superfluous. A formation/continuum completion and the common
source/clock/volume mapping still require independent justification and
the same-state cross-domain tests.

## Custody and resources

The following SHA256 identities were checked against existing bytes during
this read-only review. The canonical payload identity is the saved receipt;
this review does not independently recanonicalize the numerical payload.

| Artifact | SHA256 |
| --- | --- |
| `NATIVE_ENERGY_SOURCE_AGE_SPECTRAL_V001_RESULTS.json` | `201baf3b3558814818e1dfa76c2965bea3ab473f5295d5ab9ea8d326f59d4960` |
| Saved canonical payload | `4201dce3b3fdc4ac0161ee78dfd35140b75693f926de5a682a78498532e83893` |
| `NATIVE_ENERGY_SOURCE_AGE_SPECTRAL_V001_FROZEN.json` | `42cc9cfc3876bf34a0c270280103d5202e304a3d2bc7d5f5eca81f6b77724ebc` |
| `native_energy_source_age_spectral_v001.py` | `ad4f55dd8db0945c8dd221ce2c14aadde0594cabc45a5b9ab5c452904ade4982` |
| `NATIVE_ENERGY_SOURCE_AGE_SPECTRAL_V001_PROTOCOL.md` | `d36ebbfd7f3608a961cf49e134f5bb32796067401f4ce198fb3e1c37bf592b98` |
| `NATIVE_ENERGY_SOURCE_AGE_SPECTRAL_V001_INTENT.json` | `7037902ee48ab1c253581a072d438388fc6f2b73c269362d64f26a5e761d1713` |

The result file has 18,763,277 bytes. Its saved **analysis-phase** counters
are 0.14169737504562363 elapsed seconds, 0.131335 CPU seconds, and maximum
self RSS 111,820,800 bytes, with NumPy 2.3.5. The timing/RSS snapshot precedes
result serialization and atomic publication; it is not a complete end-to-end
runtime or post-serialization peak-memory measurement.

The exact age-average and spectral identities, with their stated hypotheses,
are in `NATIVE_ENERGY_SOURCE_AGE_AVERAGE_V001.md` and its separate analytic
review. This note preserves the frozen result and does not alter its source,
protocol, tolerances, inputs, numerical signs or qualification flags.
