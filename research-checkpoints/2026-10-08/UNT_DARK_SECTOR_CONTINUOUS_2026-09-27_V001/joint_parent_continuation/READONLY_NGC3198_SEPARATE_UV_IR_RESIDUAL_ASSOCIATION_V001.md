# Separate FUV/24µm association with NGC3198 saved residuals

The two bands do not show an exact monotone mirror of the saved EXP24 FINE_Q3 residuals. This is a descriptive test of historical Q1 and legacy readouts, not a calculated-metric geodesic prediction or a test of an arbitrary thermodynamic stress kernel.

The audit used 28 SPARC radii within the measured 0.3–15.1 kpc support. All 43 rotation rows are retained; band quantities at the other 15 radii remain `None`. It reused the closed activity adapter’s linear interpolation operands and the closed photon adapter’s nominal conversions, without fitting a sign, gain, phase boundary, or source law. Four descriptive bins were declared before the calculation at existing Leroy knots.

| Band | Spearman with signed Q1 residual | Pearson with log10 intensity | Adjacent changes: same / opposite |
|---|---:|---:|---:|
| FUV | -0.158183 | -0.364165 | 10 / 17 of 27 |
| IR24 | 0.467433 | 0.679167 | 12 / 15 of 27 |

Residual means **model minus observed**, in km/s. A required speed correction has the opposite sign. Left and right Q1 values coincide at these overlapping radii; the separately retained legacy ranks are −0.173 for FUV and +0.470 for 24µm. The 24µm profile is itself strongly radial (Spearman with radius −0.933), so its association is not evidence of causation. No p-value or confidence level is asserted.

| Fixed bin, kpc | Rows | Mean Q1 residual, km/s | Quoted-error demand: positive / negative / not common |
|---|---:|---:|---:|
| 0.3–2.3 | 7 | +14.8421 | 0 / 4 / 3 |
| 2.3–6.4 | 12 | -5.1264 | 4 / 0 / 8 |
| 6.4–10.4 | 6 | -1.9779 | 3 / 2 / 1 |
| 10.4–15.1 | 3 | -6.9570 | 3 / 0 / 0 |

The original within-coverage demand census remains **10 positive, 6 negative, 12 not-common-sign**. “Not common” preserves the original one-error-band classification; it is not a new zero-source test. At 0.64, 0.96, 1.28 and 1.61 kpc the residuals are +25.07, +28.89, +19.01 and +8.45 km/s, respectively, all requiring a negative correction under that screen. At 6.43 and 6.74 kpc the residuals are +2.625 and +4.070 km/s, also requiring negative corrections. The broader 6.4–10.4 kpc bin is mixed (2 negative, 3 positive, 1 not common); the two named radii themselves have the same demand sign.

Leroy Table 7 supplies separate FUV and 24µm **SFR contributions**, in 10⁻⁴ M⊙ yr⁻¹ kpc⁻², plus an RMS for their combined SFR estimate. There is no separate quoted band RMS. The nominal face-on specific intensities are recovered as contribution/0.081 and contribution/0.0032 in MJy sr⁻¹. Published SFR coefficient ranges are not brightness-error intervals: the tabulated derived component would covary with the coefficient. No total-SFR RMS is assigned to either band.

The FUV term traces unobscured stellar emission, with Galactic extinction correction; 24µm supplies dust-embedded/reprocessed emission information. Their calibration accounts for obscured versus unobscured activity, rather than identifying two separately normalized native stresses. They average present stellar activity over different populations/timescales and do not give an emission history. [Leroy et al. 2008, Appendix D](https://arxiv.org/html/0810.2556v1).

Both catalogues use 13.8 Mpc. Leroy uses inclination 72°; the frozen SPARC sample records 73° ± 3°. Neither convention was changed. No band integration, bolometric correction, 3D thickness, opacity, Maxwell/native correlation, photon-to-record conversion, clock, formation state, or coupling coefficient was selected. In the existing Z(O)F² candidate the direct vertex needs F² (or the relevant joint composite), which intensity alone does not supply; a null outgoing beam can have nonzero radiation stress and F²=0.

A causal or spatially nonlocal kernel could produce a signed radial response, so these associations do not rule it out. The concrete next constitutive requirement is a derived, independently normalized operator/current/stress response to the two radiation observables, with energy accounting and retarded state specified. These data alone do not provide that response. The mandatory rotating-material/full-metric geodesic branch remains separate from these historical residual diagnostics.

Audit PID 27927 naturally closed 0; 18 selected input hashes and the three closed owners/results were authenticated and rechecked. Nominal band conversions and saved interpolation consistency passed (maximum relative regrouping difference 2.81e-16); this is an arithmetic check, not a physical acceptance gate. All physical qualification flags remain false. No producer/helper/operator/field/Gram/inverse/eigen/solve/evolution replay occurred.

[Raw 23 bands, all 43 context rows, signed changes and seals](/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/READONLY_NGC3198_SEPARATE_UV_IR_RESIDUAL_ASSOCIATION_V001.json)

JSON SHA256: `1e48c7cf413c9e3c5ff068a1438b95f265bcf50c50625664c6939723fd5b12f0`
Predeclared plan SHA256: `a2eea78cc01367827383eb906b250ede870c107ee8132d5c0dd260f6b38fa7bb`
Saved scalar audit source SHA256: `1add1345e47962bccefdb3b6e4019e4d98e2af8487814be193a694177f4c6d6d`
