# Independent V002 lensing result review

Accepted within the declared metric, source and exterior assumptions. The
interpolation repair resolves the V001 numerical failure without changing
any physical field, source, ray, law, boundary model or acceptance target.
All 20 original/calibrated cases and 300 rays remain. The new HALOGAS gas
contrasts are not part of this lensing census.

## Qualification and repair outcome

All 7,891 recorded checks pass: **246 new synthetic controls, 2,245 newly
computed real-field checks and 5,400 explicitly inherited unchanged spherical
checks**. The inherited checks are not new independent integrations.

The maximum error among the 25 source-own Newtonian projected-mass controls
is now **0.0286623%**, at b=2.7 kpc in the original HI1/H21 source. V001's
same control was high by 5.5183%; V002 is low by 0.02866%. All five former
failures are resolved, and the original 1% criterion is unchanged. The
identified low-order monopole-subtraction defect was therefore genuinely
numerical; its diagnosis was not a justification for relaxing the test.

Across the candidate cases, maximum N256/N512 angle change is **0.00808965%**
(b=2.7 kpc, 72-degree major axis), and maximum L255/L1023 change is
**0.15170861%** (b=43.7 kpc, face-on). These are retained numerical/exterior
sensitivities, not observational uncertainty estimates. Runtime was 234.3017
seconds, with reported self-RSS 139,280,384 bytes.

V001's full failure record remains unchanged. The largest V002/V001 angle
change is 9.58981%, at the formerly sensitive face-on b=2.7-kpc ray in the
original HI1/H21 larger-domain case. This is explicitly a post-failure
method repair, not a newly blind prediction.

## What the same potentials now predict

Across all retained geometries and sources, candidate physical bending
components along the principal impact axis span 0.122344–0.371445 arcsec;
the Newtonian controls span 0.026438–0.139530 arcsec. The 75 same-source,
same-impact **fine-grid** candidate/Newtonian magnitude ratios range from
2.16853 to 12.43478. All 300 rays were audited; coarse/domain cases are
retained for numerical comparisons rather than mixed into those fine-grid
ratios.

For the fixed calibrated old-gas source, the face-on fine-grid predictions
illustrate the radial relation:

| Impact (kpc) | Candidate bending (arcsec) | Same-source Newtonian (arcsec) | Ratio |
|---:|---:|---:|---:|
| 2.7 | 0.140553 | 0.058667 | 2.39576 |
| 8.7 | 0.258081 | 0.075012 | 3.44054 |
| 20.7 | 0.312761 | 0.051819 | 6.03562 |
| 35.7 | 0.337302 | 0.036647 | 9.20404 |
| 43.7 | 0.345139 | 0.031743 | 10.87278 |

No lensing halo, lensing mass normalization or source redshift was fitted.
These are physical bending angles, not observed reduced angles. The common
metric interface supplies the relation between the solved matter potential
and photon response; that relation does not follow from the nonrelativistic
force law alone. Existing rotation discrepancies are not erased by obtaining
a well-resolved photon prediction.

## Audit scope and custody

`saved_lensing_v002_audit.py` verifies all 81 frozen members, canonical seals,
the preserved V001 failure hash, full case/ray census, exact reuse identities
and all inherited check records. It recomputes saved component/unit closure,
four/eight-node and reflection discrepancies, unchanged projected-mass
targets, V001/V002 differences, numerical comparisons and all fine-grid
ratios. It imports no physical worker and runs no ray integration or PDE.
Independent saved-data arithmetic agrees to 2.19e−16 scaled units.
The complete snapshot is `SAVED_POTENTIAL_LENSING_V002_REVIEW_DATA.json`.

This is numerical qualification of a conditional forward model, **not an
observed lensing validation**. Stationary aligned-clock weak-field dynamics,
the adopted covariant interface and isolated spherical exterior remain
assumptions. Actual source/metric/clock matching, environmental/cosmological
light paths and observed lens-source distances require their own evidence.
The complete source alternatives and every numerical diagnostic are retained.

Result SHA-256:
`e3b9fe6bd2a0d4d049c2a8111b77c833f49480fd10a01f3298a77b11001577e9`.
Freeze SHA-256:
`fa08a693ec43be934d3a846a16351bcbec5602c2b83b54a52ac9191fa4e184aa`.
No frozen source, result or scientific tolerance was edited in this review.
