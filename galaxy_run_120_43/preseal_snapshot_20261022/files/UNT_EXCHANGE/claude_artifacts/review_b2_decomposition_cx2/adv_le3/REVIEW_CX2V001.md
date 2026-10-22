# C3 le3 ADV-compatible static reference — TESTED PASS (bounded scope)

`date -u`: Sun Oct 18 20:08:38 UTC 2026. Computation began Sun Oct 18 20:07:47 UTC 2026.

The missing C3 same-le3 reference was computed. All 12 fresh ADV O6 P16 rows match the saved independent discrete-gas/discrete-star result within **3.907985046680551e-12 km/s**. No C3 input is missing for this bounded reference. This is a static reference result, not a B2 gate verdict or seal decision.

| Measured control | Result |
|---|---:|
| Saved le3 zero-correction rows reconstructed | 7.1054273576010019e-15 km/s maximum absolute error |
| Reconstructed rotation A | 2.2204460492503131e-16 maximum relative error |
| Fresh O6 P16 versus independent O12 discrete total | 3.907985046680551e-12 km/s |
| Discrete-star radial-profile transcription against selected inert source function | exactly zero at all 204 roster radii |
| Separate P16 versus m0 diagnostic | 0.0870977916345268 km/s |
| Start/end byte pins | 13/13 unchanged |
| Forbidden-path attempts during successful computation | 0 |

The P16-to-m0 value is a **separate contrast**, with gas and star rosters fixed. The reference being matched here is P16. This diagnostic must not be silently added to the matched-P16 named-star residual or presented as the B2 sanity residual. Signed values for every row are preserved in the result.

Method: AST-selected original `axis_nodes`, `cart_tail`, and `rows_with`; K=3, outer box=12 inverse kpc, width0.25, Gauss order6, 16 azimuths, the original positive-xy quadrant factor4 and full kz. The evaluation contains 47,775,744 quarter-xy/full-z nodes. Discrete gas rings come from the exact saved le2 source; the evaluation uses exact saved le3 arrays. Discrete stellar GL rings were independently transcribed from the ADV equations and pinned DDO154 source profile. J0/J1 use stdlib ctypes/libm as the original ADV implementation. The only third-party dependency is numpy.

The inert observation and column-mean functions were selected by AST, with the exact original byte pins. Column path weights were recovered from the pinned target-free CM_ON emission weights by undoing rho and the scalar HI ratio. The zero-correction and A controls above validate this readout reconstruction. No observation targets were read. No Case, main, validation routine, producer, driver, stage, route or solver was executed.

Measured quadrature time: 5.429379 seconds. Peak resident memory: 653770752 bytes. Output derivatives are only two 72×32 arrays plus three 12-row vectors.

Evidence (SHA256 from bytes):
- RESULTS_CX2V001.json: `513c117295a43a6ec6ef778e35476eb3520b6032c0c0217c14ee624f59e16bf4`.
- C3_LE3_ADV_O6_CX2V001.npz: `fa5c31a88f99833d1e846e843a3b9f44487554e0382efa56b351936baca5d23b`.
- recompute_c3_adv_le3_cx2v003.py: `fa75c3ffa1920556049af358328ebf99bc21802a17a6a0154d96964520e75a6a`.
- INPUT_PINS_CX2V001.json (full paths, all source/input hashes and end pins): `86b00f56e488019165cb1ec6b31fc066e3e875cf2025c5e9f220d192146eb46f`.
- Original ADV source: `67a6eeb66b1f94fe356272a31294be012fa448f6c8c03b75cdab66fb540e896a`.
- Saved independent discrete-total comparator: `fdbacd7de467c10924d5201b0b168f974a8206d59ee2100473b9340623cfcbce`.

Limitations: this is one O6,width0.25 evaluation; the O12 comparison is measured but not a new general convergence proof. Fourier/unit-response custody was not revalidated. The separate lane owns gas-continuum/star/force-law attribution; no continuum-gas quadrature was repeated here. C2/C4 fresh quadrature was not repeated. No final B2 acceptance decision is made.

The v001 and v002 harnesses remain immutable. They stopped before quadrature on disallowed lazy standard-runtime imports. The successful v003 preloads only those numpy/encoding components before installing guards; source AST execution and saved-state reads remain guarded. No result from an unsuccessful attempt is used.
