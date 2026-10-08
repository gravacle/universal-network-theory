# Independent interpretation of the helium cache curvature attribution

The isolated helium RHS-history correction changes the imported quarter-minus-half curvature difference at the fixed atomic-step witness from `-1158.1874505709497` to `+207.48161348849953`. The sign reverses and the absolute difference is smaller at this one location. At the fixed resolution witness, both flavors retain exactly the same thirteen local input rows and imported readouts. This supports a specific numerical-source attribution; it does not resolve or waive either original thermal-audit failure.

This reviewer authored neither the attribution producer nor its protocol. The review read both in full, inspected the unchanged PCHIP primitive definitions, checked the derivative formula analytically, independently rehashed the result and all 18 recorded input artifacts, and read the saved aggregates and local-window equality fields. No source was imported, compiled or executed, no atomic/CLASS job or auditor was rerun, and no full-table numerical audit was reproduced. This is an independent interpretation and custody review, not an independently implemented reproduction of the diagnostic.

## Signed findings at the fixed witnesses

The retained census is two atomic-step flavors at two preselected locations: four before/after local records, each with thirteen input knots and nine interior two-sided curvature witnesses. The quarter history shared by the original smoke64 and smoke128 acquisitions is evaluated once, not miscounted as two new CLASS runs. All four saved baseline-minus-prior analytic readouts are exactly zero, and both pair change-decomposition residuals are zero.

| Fixed location | Quarter imported D2_K before | Quarter after | Half before | Half after | Quarter minus half before | Quarter minus half after |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Resolution, z = 1625.773896926712 | -124.08275651732828 | -124.08275651732828 | -124.12749355127744 | -124.12749355127744 | +0.04473703394916129 | +0.04473703394916129 |
| Atomic step, z = 2851.8156745887045 | +2858.6290687852193 | +1616.1930338766128 | +4016.816519356169 | +1408.7114203881133 | -1158.1874505709497 | +207.48161348849953 |

The table's quarter-minus-half comparison at the **resolution location** is not the original resolution failure, which compared smoke64 and smoke128 using the same quarter history. That original imported difference was zero. Its saved CLASS reconstruction difference remains the historical `+441.2940451362297`; the isolated cache correction provides no changed local input at that witness from which to claim its removal.

At the atomic-step location, the saved quarter and half imported changes are respectively `-1242.4360349086064` and `-2608.1050989680557`. Their second-derivative contributions change by `-1242.7080158793776` and `-2608.702817129625`; first-derivative changes are `+0.27178742142563905` and `+0.5973049634489804`, and value changes are `+0.00019354934534021595` and `+0.0004131981204409385`. Thus the recorded change is dominated by curvature of the imported numerical history, not by an altered opacity normalization. The background and opacity coefficient are the original owned values, and the authenticated grids and H ordinates are unchanged.

The readout remains the derivative of the original interior PCHIP interpolant. With `x=ln(1+z)`, `s=1+z`, `K=C*s^2*xe`, `Hc=H/s`, and `alpha=dlnH/dlns`, the unchanged formula is

    D2_K = Ksecond/Hc^3
         = C*s^3/H * [(2+2*alpha)*xe + (3+alpha)*xe_x + xe_xx].

Its nonuniform interior slope stencil is supported by the thirteen retained rows; the nine knot comparisons stay inside the admissible segments. No new smooth interpolator, physical clock, approximation-switch location, tolerance or favorable probe was introduced. The signed knot jumps remain properties of a prescribed piecewise polynomial, not evidence of physical nonsmoothness or a completed smoothness repair.

## What remains untested

There are no corrected CLASS derivative outputs in this packet. In particular, the historical atomic-step CLASS-minus-imported difference `-82.32603233824966` must not be added to the new imported difference to predict a corrected CLASS residual. Changing the input curve can also change downstream reconstruction error. Neither this historical reconstruction term nor the old global-amplitude allowance can be used to convert the new single-witness import difference into a pass.

The result therefore provides evidence that the isolated cache correction materially affects the imported atomic-step curvature at the prescribed witness. It does not demonstrate global improvement, validate all knot jumps, settle the separate helium-cutoff issue, or qualify PCHIP/CLASS derivative reconstruction. A fully owned corrected thermal acquisition and the unchanged complete audit are still required. The original result with eight passing individual acquisitions and only four of six passing required comparisons remains immutable.

All stored qualification flags are false: `qualification`, `thermal_qualified`, `thermal_failure_waived`, `propagation_allowed` and `Stage3_complete`. The diagnostic also keeps `corrected_CLASS_derivatives_computed`, `changed_interpolator` and `new_locations_selected` false. All 11 mandatory scientific lanes remain OPEN. This numerical engineering result does not establish the physical dark-sector model, formation, observational success or the superfluity of DM and DE.

## Custody and resource scope

The result reports `SAVED_HELIUM_CACHE_ATTRIBUTION_COMPLETE`, with no error. Every one of its 18 input file hashes independently matched the extant file. The payload identity below is the stored canonical receipt; this reviewer did not separately recanonicalize the payload. Source inspection confirms that the producer itself authenticates the wrapped inputs' canonical payloads and raw stream lineage, and checks the recorded inputs again at successful completion.

| Artifact relative to this directory | SHA-256 |
| --- | --- |
| `CLASS_THERMAL_HELIUM_CACHE_ATTRIBUTION_V001_RESULTS.json` | `77788ba66e35ce27aaf0570e638230c880af5c06845cb46231144f4d44f342fe` |
| Stored canonical payload receipt | `39f00acffde6da7cd2b752d12783878eada96fc4e0fd79f614a34de3a7453a2b` |
| `class_thermal_helium_cache_attribution_v001.py` | `0ecba7c549326149548f0bf8403ceaf6758decaf8e727c8a60910b6b9f2f5bc3` |
| `CLASS_THERMAL_HELIUM_CACHE_ATTRIBUTION_PROTOCOL_V001.md` | `917b1cb822055837f0738ead6e7a120df18cf7975f6d38cb3e934725c84cbb37` |
| `CLASS_THERMAL_HELIUM_CACHE_ATTRIBUTION_V001_INTENT.json` | `8cbf6e205b2a7dd38c52689fbb68ff054ecaa4a3346587da494b004a621bd842` |
| `class_thermal_pchip_curvature_v001.py` | `28ea84dc164036bdc7f696a74f018c7e0ac116a5f2a813859e554195e2cf9d2d` |
| `CLASS_THERMAL_PCHIP_CURVATURE_V001_RESULTS.json` | `48f1ea52c7fa81d49ecc3e6417b78ba81b0d084683999cab0418d512a21fbe1b` |
| `../hyrec_inputs_v001/HYREC_HELIUM_RHS_CACHE_V001_FROZEN.json` | `92aa3d4bca90e9b6bf1a4ad10c8b60efb25eb9eccead739c73bb6cd30316d6c8` |
| `../hyrec_inputs_v001/HYREC_HELIUM_RHS_CACHE_COMPARE_V001.json` | `ce4b8fd7d2e2f2cc9bc393e45da3234cfec332b73cbcc730d5f61cff1f1df5b6` |

The remaining exact input identities, including the old and corrected quarter/half receipts, are retained in the result's `inputs` map. The saved elapsed time is `0.40439420798793435` seconds and maximum self RSS `131383296` bytes. Both are snapshots taken after analysis and before final result serialization/publication, not independently measured end-to-end resource totals. No previously frozen source, result, gate or history was changed by this review.
