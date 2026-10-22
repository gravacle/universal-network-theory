# Independent source crosscheck of saved-component B2 decomposition

`date -u`: Sun Oct 18 20:06:24 UTC 2026

**PASS_WITH_SCOPE_LIMITS for the stated decomposition semantics.** No concrete algebraic or readout defect found. This is an independent source/record inspection, not a duplicate numerical replay or an A97 acceptance decision. The saved37/37 result is attributed to the reduction harness; no supplied module was executed in this crosscheck. `nice unavailable (sandbox); 0514 waiver`.

**Common readout.** `rows_for_force` adds the vertically weighted force to saved Ω², takes sqrt before the emissivity-weighted column mean, interpolates those column means with the saved support weights, and applies sin(i_phys)/sin(i_release) once. That matches the observation/adapter source formulas. `weights/h` is valid for the force weighting because `weights` is w_zρ times the constant HI/He ratio, which cancels in the normalized force integral. The harness uses NumPy sums versus the adapter's fsum, so formula-equivalent does not mean byte-identical; reported row checks tolerate and show only ~2e−14 km/s differences.

**Named source contrast.** `same_le3_named_star_residual_gas_matched_linear` is R(stars_cont,gas_cont,linear)−R(stars_disc,gas_cont,linear), with the same saved le3 state and readout. This changes only the named stellar representation at the common linear readout, using saved force arrays. Its maximum absolute values are:

| state | gas-matched/common-linear star residual km/s | stars-first residual km/s | max absolute switch-order interaction km/s |
|---|---:|---:|---:|
| C2R3 | 0.030115450568374058 | 0.030160704319449394 | 9.062101777601583e-05 |
| C3R3 | 0.0356225797997638 | 0.035685316127874955 | 0.00013035183680187856 |
| C4R3 | 0.03835728930356197 | 0.03843453334366842 | 0.0001696154863068955 |

Both actual comparison sides are P16, so `named_alias_actual_P16_to_P16=0` is the correct **difference in this comparison**. It does not say the physical P16−m0 alias is zero. The older ADV alias is separate, and C3's older alias remains a le4 diagnostic. Source-switch order interaction arises from the Ω²→sqrt/readout nonlinearity, even though the force channels are additive; it is not evidence of nonlinear source-transform physics. Both orders are preserved, and scalar maxima are not summed.

**Pathwise corrected reference limitation.** The `corrected_reference` expression algebraically reduces to mixed(stars_disc,gas_cont,linear) + [all-continuum mean-tail nonlinear − all-continuum linear] + [production − rebuilt independent]. Thus production minus this reference equals the common-linear named-star contrast by construction. The telescope/closure assertions correctly verify vector bookkeeping; they do not independently validate an alternate nonlinear field. The record explicitly says it is **not an independently integrated mixed-source nonlinear potential**, because the saved components lack the discrete-star potential t needed in the nonlinear denominator. That caveat must travel with any A97 use; the pure common-linear contrast is the independently reconstructed quantity.

**Other distinctions.** The nonlinear force reconstruction reproduces the original independent B2 mean-tail-before-denominator formula, not retained phi-dependent mixed-tail fields. The C3 reference mismatch is not hidden: same_ADV_baseline=false and the old-reference step contains a state difference. A fresh same-le3 ADV result is separately delegated. Reusing pinned component arrays means no quadrature reintegration or independent validation of their source construction took place in this reduction.

**Production/shared-input reading.** No real production or shared-input error is demonstrated by the available checks. Saved baseline reconstruction, force/readout agreement and production-versus-rebuilt rows support consistency for these exact inputs; because those inputs and component arrays are shared, this is not proof that every shared source or implementation premise is correct. The output appropriately leaves scientific acceptance and the unchanged0.05 allowance to the fixed A97 rule.

**TESTED here:** input byte hashes and source/formula inspection only. **UNTESTED here:** duplicate array replay, fresh quadrature, missing mixed-source potential, original-run custody and final A97 disposition. No actual run tree/receipt metadata/target was opened by this crosscheck; no active process remains.

## Exact bytes reviewed

- reduction_result: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/run_20261018T200537Z_93548/RESULTS_CX2V001.json` — SHA256 `0d672be05df87becc9ed5486946d20f23203921796b22b2e7e19b963e5a0cbe3`.
- reduction_source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/decompose_saved_components_cx2v002.py` — SHA256 `451a4ac93a44c9802637d32af9e54ad59aac05aa034d7658338cf8e7fe3d6efd`.
- independent_source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/scripts/b2_independent_c3v001.py` — SHA256 `6c013801d8b86255c9ca042deb9de2a95adaa37a11fad06ea23abe104c6089d5`.
- adapter_source: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/owned_column_mean_streaming_observation_v002.py` — SHA256 `6790e28eb6631c0144f2efda26071a5933f47f7bda7d0c15d3b81e3581cc548c`.
- observation_source: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/galaxy_hi_observation_forward_v001.py` — SHA256 `8e30897e875a619b132ba07e93459333cfd9302bbe2fc98d9a2ff0a2ec6d815d`.
