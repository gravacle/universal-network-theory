# Independent calibrated physical-field result review

2026-09-29. Accepted within the declared linked local scalar fixed-action
model. No finite-action radius inversion, orbit quadrature or propagation was
repeated in this review. No frozen artifact was changed.

All 50 frozen identities and canonical payload authenticate. The result
preserves all 648 calibration labels, 1,944 physical-field rows, 648 saturation
rows and 36 origins. Producer: 4,254,292 numerical check entries passed,
2,952 angle-rule orbit evaluations with label-preserving caching, 13.322654 s,
45,170,688 bytes peak self RSS on Darwin, not whole-job memory.

- Result: `d70ad800da4b4f0f6948cd547e4b5698b25c8ecdf41ce36c70a499594cd5c2b3`
- Freeze: `b23a6db9359f11a61b355aa5183b546bf02f5784dd13ddfe21595db19edb7724`
- Payload: `3512df4425967f301d9bd7562ecc4acb9eed2e82afdad2b0caa39fb48138e373`

Independent saved algebra passed 24,625 comparisons. It reconstructed each
relaxed cubic minimum and force by closed-form algebra, every physical-field
and bounded-source conversion, the work differences, original-state slopes,
saturation normalization and calibrated endpoint linkage. Largest recombination
discrepancy was 1.09e-14, in the origin energy inherited from the finite-action
kernel. All force-order bounds passed without clipping a failed value.

The linked response is now quantified in physical acceleration units:

| External g (m/s²) | Range of gN/g across all retained branches |
|---|---:|
| 1e-12 | 0.00372686–0.05415293 |
| 1e-10 | 0.02188632–0.07293995 |
| 1e-8 | 0.99988572–0.99991011 |

The low-field values remain close to each state's unchanged excitation-induced
origin slope; the density calibration did not fit that slope away. At higher
field the same bounded source returns the local response close to its bare
value. This is an actual re-evaluation at the newly calibrated source map,
not a rescaled old galaxy curve.

The state-dependent high-field coefficient has the correct acceleration-fourth
units: `C3=gs^4 B_I(S)/(I0 S)` ranges from 9.16615e-37 to 1.167716e-36
`(m/s²)^4`; `C3/gs^4` is 0.928838–0.995999. Its relaxed comparison is independently
recoverable from the calibration derivative `Q'(S)=1/(dS/dQ)`. Every saturated
minimum also equals the negative of that branch's owned calibrated `Q(S)`.

For template 6/reference 0 (branch 108), the three ratios are 0.00385664658,
0.0230377389 and 0.999897785. Its `C3=1.043178586e-36 (m/s²)^4` and
`C3/gs^4=.995065993`. Signed 64-minus-128 differences are preserved: 1,434
negative, 16 positive and 494 zero; maximum absolute normalized difference
7.95e-15. These are numerical convergence measurements, not physical uncertainty.

The independent audit cannot reconstitute the full active aggregate polarization
or each quadrature order separately because those modal means are not stored.
Their complete orbit agreement remains the authenticated producer's evidence;
this review verifies saved identities and the independently computed relaxed
control, not an independent second full finite-action solver.

These fixed physical probes are not observed disk radii, a galaxy fit or a
metric solution. In particular, the force-order inequalities alone do not
prove an invertible or stable spatial response law. Physical inertia/clock,
formation, state transport and the homogeneous-to-radial state relation remain
separate inputs. The result nevertheless supplies the precisely linked local
prediction needed to test those next interfaces without independently choosing
a new force scale or discarding the excitation energy.

Reproducible audit: `calibrated_fixed_action_saved_audit_v001.py` and
`CALIBRATED_FIXED_ACTION_V001_AUDIT_DATA.json`.
