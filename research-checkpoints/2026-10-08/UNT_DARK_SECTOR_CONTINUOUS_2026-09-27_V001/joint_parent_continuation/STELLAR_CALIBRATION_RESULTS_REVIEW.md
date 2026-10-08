# Independent completed stellar-calibration review

All four prescribed calculations and the matched diagnostic pass their numerical
checks. The physical finding is mixed and useful: the fixed photometric
convention change removes much of the intermediate-radius discrepancy, while
increasing the central and outer excess. It is not an all-radius repair and
does not select the true stellar mass-to-light ratio.

This is a read-only, post-execution audit. No field was solved again, no source
or tolerance changed, and no frozen artifact was edited. The independent
standard-library arithmetic is preserved in `stellar_calibration_saved_audit.py`
and its printed output in `STELLAR_CALIBRATION_RESULTS_REVIEW_DATA.json`.

## 1. Source and custody

The calibration freeze has 63 authenticated members. Its SHA-256 is
`622f381e523b43ea4910fda55ff1130ef17e8ad143cffa29b0a72165498ac656`.
All four exact N/domain/equation identities, canonical payload hashes,
same-grid original-case identities and the final result's case-file hashes
match. The new result SHA-256 is
`21db2263f7a49a11312d4e2c8abfb5412946784fbcebfa8e5db2b1447668f14a`.
The recombined ring-oracle SHA-256 is
`a63c0a5625b601d72a60174027ded7827e04835bbec9f1dc53f29452c02f9cd0`.
The complete case hash map is retained in the review-data JSON. These establish
artifact consistency, not independent physical truth.

Exactly the prescribed full stellar density was multiplied by
1.2567828155112788. Both gas profiles, distance, inclination, thin-disk geometry,
law, a0 and shape parameter remain unchanged. The new stellar mass is
19,798,896,050.1033 solar masses; gas masses remain
15,134,141,724.8567 (HI+He) and 574,779,508.7155 (H2+He). Total mass is
35,507,817,283.6754 solar masses, 1.12857386877308 times the original HI1/H21
total. This is a published-convention substitution identified independently of
the velocity residuals, but performed after those residuals were exposed. It
is not a blind test, measured true M/L, best-fit normalization, or native
derivation of the adopted gravity interface.

## 2. Numerical verification

All 27 case checks, 85 recombined-oracle checks and 172 matched-diagnostic
checks pass. All 43 observations occur in every case; none was removed because
of a negative force. The three nonlinear jobs and same-source Newtonian control
are all present; no successful subset was selected.

Independent arithmetic reconstructed the midplane extrapolation from the saved
potential matrices, nonuniform three-point radial derivatives, observed-radius
interpolation, velocities, signed changes and every descriptive summary. The
maximum discrepancy in reconstructed radial force was
3.63798e-12 a0 units. Scalar and diagnostic mixed-unit comparisons were checked
on their own `max(1,abs(value))` scales; their largest scaled discrepancies were
4.46221e-12 and 5.01532e-12. These are arithmetic audit residuals, not physical
error estimates. The independently implemented scalar constitutive formula,
inverse, profile interpolation and exponential tails reproduce the matched
sheet/force decomposition.

At the prescribed R>=2 kpc radii, the maximum nonlinear mesh change is
0.4450911%; extending the domain changes the force by at most 0.00909605%.
The maximum same-source Newtonian/ring discrepancy is 0.03365282%. All remain
inside the unchanged qualification criteria. The largest saved final flux
imbalance is 7.8852e-7, largest nonlinear residual 9.6765e-10, and all clipped
face counts are zero. These checks support numerical resolution; they are not
rigorous observational uncertainty bands.

The independent-of-finite-volume ring reference was recombined component by
component at all five radii, three heights and both quadrature orders. Only
stellar contributions were scaled. Potentials, signed radial forces,
component/omitted masses, both height extrapolations and force/potential tail
bounds were retained and checked. This reuses an independently implemented
qualified oracle; it is not newly independent quadrature evidence.

## 3. The improvement and the worsening

Finest N512/L255 RMS residuals, km/s:

| Selection | Original network | Recalibrated network | Original baryon-only Newtonian | Recalibrated baryon-only Newtonian |
|---|---:|---:|---:|---:|
| All 43 radii | 13.17366 | 13.78953 | 59.10226 | 53.40666 |
| R>=2 kpc, 37 radii | 11.14382 | 9.57703 | 63.42959 | 57.01660 |
| R>=8 kpc, 21 radii | 10.34278 | 12.16396 | 75.86190 | 70.13068 |

The signed mean network residual beyond 2 kpc changes from -3.87229 to
+4.23706 km/s. Beyond 8 kpc it changes from +1.96088 to +9.17026 km/s.
The higher stellar normalization raises the computed speed at every retained
radius in this particular numerical experiment, by 3.89766–10.87859 km/s.
That observed outcome is not a general pointwise monotonicity theorem for
nonlinear disk forces.

For localization only, the reviewer also divided the already exposed finest
curve into four disjoint regions. These are post-hoc descriptive summaries,
not new acceptance gates or an optimized radial selection:

| Region | Rows | Original network RMS | Recalibrated network RMS |
|---|---:|---:|---:|
| R<2 kpc | 6 | 21.86171 | 28.23379 |
| 2<=R<8 kpc | 16 | 12.11508 | 4.23101 |
| 8<=R<20 kpc | 8 | 9.07820 | 2.39398 |
| 20<=R<50 kpc | 13 | 11.04928 | 15.34563 |

Thus the fixed source-convention mismatch accounts for much of the former
intermediate-radius shortfall. It does not explain away the remaining shape:
the central excess worsens and the outer excess grows. At 44.08 kpc the
prediction increases from 168.69241 to 172.79223 km/s, versus the retained
149 km/s observation; the same-source Newtonian control gives 66.95767 km/s.
The model supplies substantial rotational support without a halo, but this
specific source/law/geometry combination is not an adequate all-radius match.

## 4. Matched diagnostic and interpretation

The 43-row diagnostic uses the new-source nonlinear and Newtonian fields at
the same mesh and domain. The upper-sheet equation has the already reviewed
unique nonnegative vertical solution. Its reconstruction is a boundary-law
inference, not a separate measurement or independent vertical PDE validation.
The radial flux difference is a component of a divergence-free difference
in the exact same-source continuum equations; it is not a curl measurement.

At 44.08 kpc the signed velocity-squared ledger, in (km/s)^2, is:

| Term | Value |
|---|---:|
| Total-mass deep spherical reference minus observation | +1578.79253 |
| Newtonian disk versus monopole | +3271.43867 |
| Constitutive-law shape versus deep limit | +1858.44290 |
| Vertical projection | -117.34980 |
| Remaining field difference | +1064.83121 |
| Actual residual | +7656.15551 |

The terms telescope exactly. The remaining-field term includes nonlocal field,
finite-boundary and numerical effects; this partition is not a unique causal
decomposition. All profiles here have continuous tails, so there is no hard
edge flag at any observation. The endpoint does not justify treating the whole
curve as a point mass or treating each baryonic component through a separate
nonlinear algebraic law.

The strongest supported conclusion is that a fixed, no-halo conditional network
candidate supplies most of the missing rotation support under two independently
specified stellar conventions, and one identifiable convention difference
substantially changes the residual pattern. The next scientific issue is the
remaining source/geometry and constitutive shape, not simply a larger lattice
or a numerical convergence failure. This experiment compares against
baryon-only Newtonian gravity, not a fitted dark-matter halo; it neither
demonstrates that dark matter cannot exist nor establishes native UNT source,
metric, lensing, state-selection or cosmological closure. The model-dependent
reference calibration used to set the fixed law remains disclosed.

No blocking numerical or custody defect was found. All original models and
the calibration result should remain visible together; neither improved
R>=2 RMS nor worsened outer RMS should be reported alone.
