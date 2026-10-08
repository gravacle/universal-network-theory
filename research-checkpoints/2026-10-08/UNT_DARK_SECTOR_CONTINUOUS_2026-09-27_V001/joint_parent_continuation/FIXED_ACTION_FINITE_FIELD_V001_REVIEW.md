# Independent result review: unchanged actions across finite fields

2026-09-29. Accepted. All 252 template/field rows, 36 origin comparisons,
36 own-held-field anchors and 168 numerical-resolution comparisons are retained.
All 641,600 original scalar arithmetic controls pass. No propagation, action
inversion or angle quadrature was repeated by this reviewer.

## Custody and independent checks

Result SHA-256:
`5d7ceb3a4b98f73cb1a41f295100aec65cce99e85677e369b0bd17840779408f`.
Freeze SHA-256:
`0d1552f783c95b172b76d79622ef5b14101a8a08a667f7377ea9b56a05518155`.
Payload SHA-256:
`9d6b5665c30066c667a2f14c1127af8d1ecd42cf0c42703af5adb99e2016ff16`.

All 36 frozen inputs authenticate. The reviewed prefreeze centered-virial
correction is present; no frozen source or tolerance changed after execution.
The producer recorded 2.407171 seconds, 43,171,840 bytes peak self RSS, and
398,311 canonical payload bytes. Self RSS is not whole-job memory.

`fixed_action_finite_field_saved_audit_v001.py` and its saved audit JSON
reproduce 10,676 checks. Every row's three prospective witnesses—756 total—
match original gaps and target actions. Their center cubic, independently
reconstructed minimum, stable excitation and equal turning energies check.
Origin and own-held witnesses also agree with old saved energies, means and
periods. All aggregate origin/anchor comparisons, energy bookkeeping and
resolution differences reproduce. The largest reconstructed witness excitation
discrepancy is 3.98e-11 relative, within the original 2e-8 scale; reconstructing
small widths from rounded saved endpoints is less precise than the producer's
internal radius. Aggregate minimum energy agrees to 1.95e-16 relative.

The audit independently reconstructs equilibrium minima and verifies the
analytically derived ordering at all 216 positive-field aggregate rows. This
is a consistency check of the separate proof, not a new numerical gate.
**Full new modal means are not saved:** this audit does not independently
reconstruct every aggregate mean force at non-anchor fields. Its evidence
there consists of authenticated full-census producer controls, the three
fixed witnesses per row, exact algebraic bounds and the saved comparisons.

## Main readout

For retained template 6, with no action or scale changes:

| External G | D/G |
|---:|---:|
| 1e-5 | 0.00385470843 |
| 0.0025 | 0.00469200558 |
| 0.01 | 0.01225779442 |
| 0.04 | 0.04567556219 |
| 1 | 0.54040729084 |
| 100 | 0.99984745864 |

The first readout approaches its independently established origin slope
0.00385470013. At the original preparation field it recovers the old held
phase mean. Thus the code follows the same actual actions from their origin
response through the nonlinear and bounded-source regimes rather than
assigning a separate population at each field. The largest old-resolution
force difference divided by G is 2.07e-13 over the retained census.

The exact force-ordering proof, not these seven sampled fields alone, shows
the fixed-action scalar force lies between its same-spectrum relaxed and bare
responses. This does not prove a monotone derivative, a universally stable
gravity law or a fit to galaxy data. The reported source-work difference is
ideal fixed-volume adiabatic endpoint bookkeeping, not an executed history.
The old matched constant remains unchanged. Physical state selection, vector
transport and the coupled clock/metric constraints remain separate from this
now-qualified constitutive calculation.
