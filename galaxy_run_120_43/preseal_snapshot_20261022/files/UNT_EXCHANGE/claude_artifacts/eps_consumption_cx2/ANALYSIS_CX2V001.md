# Independent EPS-consumption analysis — Codex2 CX2V001

date -u: Wed Oct 21 17:32:03 UTC 2026

**ROOT_ESCALATION — 0854(a) finished; 0854(b) is now authorized by 0855/A296 and underway.** FORMAL: neither requested driver's production-continuum tail/lapse construction uses numeric EPS values as an amplitude or correction. Those paths authenticate and carry the certificate pin. The numerical acceptance-bound consumer uses **per-shell EPS, not the single global eps_max**. Changing only a certification decision, with every numeric EPS entry and physical input fixed, leaves those numerical calculations unchanged; it changes admission and custody. The existing finite-sampling records do **not** establish a rigorous numerical worst-case error for an under-converged shell.

This analysis was derived from the pinned implementations, original registration sources and saved certification records. No coordination with Claude3 occurred. Earlier inbox reads included interim reports; the same-question escalation posted during this analysis was not read beyond its filename/recipient. Those reports are not evidence for the conclusions below. TESTED means static byte/text checks or saved-record arithmetic; FORMAL means code-flow/math reasoning. All production execution and true continuous-error enclosures are UNTESTED here.

**1. What each driver actually consumes.** DDO b5cc62af and NGC cx3r008 577f8c94 normalize EPS as a {path, sha256} reference, reject missing/mismatched bytes and carry that identity in requests/configuration/state records. The common library's build path (LIB 645–796, particularly 664–687) hashes the certificate; it does not parse EPS shell values into its quadrature, source amplitudes, jets or lapse. Its numerical arrays are built from source, geometry, quadrature and physical inputs. Native route-B binding records mark SRB-ROT NOT_EVALUATED_IN_STAGE. The source audit follows the selected DDO stages and the NGC final override/strict execution chain, rather than assuming that the first NGC function definition is active. It finds no numeric EPS use added by those overrides.

The separate proof-side SRB adapter (ADAPTER 265–291, 419–451) authenticates the point's accepted EPS proof and certificate slot, preserves every shell's recorded eps (not eps_envelope), and calls LIB.field_bound and LIB.srb_rot on that call's own state and rows. It neither substitutes the record's global eps_max nor ignores small shells. This distinguishes a library API and proof-side acceptance calculation from a driver stage directly evaluating that acceptance gate. Detailed transitive pin/call evidence is in DRIVER_REVIEW. The DDO T2-only nodes_v001 numerical branch is outside this production-continuum analysis; the NGC nodes branch is refused.

LIB._eps_per_shell (830–844) uses the maximum EPS **only among certificate intervals overlapping a particular state shell**. LIB.field_bound (847–857) then forms, for derivative order a=0,1,2:

    F_a = sum_i e_i B_i^(a).

The nonnegative B weights come from the actual source/state shell integrals. LIB.srb_rot (860–871) uses F_1:

    bound_j = beta_j F_1,
    beta_j = max over columns k in row j of R_k c^2 / (2 N_min v_k * 1000).

With valid fixed positive rows this factorization is exact for the implemented expression. The gate compares bound_j <= tau_j/10. ADAPTER uses the registered row-contract tau=0.25 sigma, so its modelled budget is 0.025 sigma. This is the static rotation channel's necessary condition, not a demonstrated bound on every error channel.

**2. Worst-case effect: the distinctions needed for a sound ruling.**

- **A decision-only amendment:** if the stored numeric EPS values, physical source/state and row inputs do not change, the numerical tail/lapse and the numerical bound above change by exactly zero as a code-flow consequence. Certificate/config/state digests can change, and newly accepted points can now run. This is not a claim that complete output files or the campaign's admitted trajectory remain identical.
- **A changed shell estimate:** for one aligned unit shell s, Delta F_a = Delta e_s B_s^(a), and Delta bound_j = beta_j Delta e_s B_s^(1). If a certificate interval overlaps several state cells, apply the changed overlap maxima and sum their weighted differences. For e_s>0 and F_a>0, multiplying e_s by m gives F_a_new/F_a = 1+(m-1) alpha_s^(a), where alpha_s^(a)=e_s B_s^(a)/F_a lies in [0,1]. The ratio e_s/eps_max alone places no useful upper bound on alpha: a smaller-EPS shell can carry a large source weight.
- **The true unresolved response:** the producer expressly labels finite/search maxima as estimates or lower bounds on a continuous supremum, not a rigorous enclosure. Neither a 1.1 pass, a 1.12 failure, the difference between two sampled maxima, nor an arbitrary safety multiplier proves the missing upper bound. The existing records therefore provide no supported numerical upper limit on the true missed-shell error. This does not assert that the physical response is unbounded; it identifies what has not been established.
- **What is missing for a quantitative accuracy guarantee:** an independently justified upper bound on the shell response, plus the relevant state weights and row factors (and any needed propagation argument for channels beyond static rotation). The latter are not contained in certification-only records. A dimensionless EPS refinement delta cannot directly be compared with a km/s observational allowance. No actual NGC values or states were read to fill that gap.

Thus a uniform added-pass rule may be specified as a new registered **numerical admission policy**. These results do not justify calling such a rule a rigorous worst-case physical-error proof. Root retains the decision and must state the assumptions for any stronger accuracy claim.

**3. Row 302 from its saved record (TESTED arithmetic).** The only failing shell is [46,47] inverse-kpc. Its last two discrete estimates are 1.086706276298699e-6 and 1.2200030085063318e-6, ratio 1.122661233412251. Their observed increment is 1.3329673220763283e-7; that increment is not an error upper bound. The stored shell eps is already 1.90905655250706e-6, dominated by the envelope search and 1.564796594 times the last discrete estimate. The governing maximum is 2.524697669156195e-4 at the certified [4,5] shell. The failing shell's stored eps/max ratio is 0.007561525389077993. These are saved estimates, not a guarantee that its weighted contribution is below that fraction. BOUND_SENSITIVITY records the source pins, arithmetic and conditional formulas.

**4. Where 1.1 was registered, and why.** The earliest explicit form located in this examined chain is DESIGN V002 §1.5 (235–240): 26 directions and 64 radial samples per decade, refinement to 52/128 and then 104/256, acceptance when the refined maximum is <=1.1 times its preceding maximum; two failed comparisons yield EPS_UNCERTIFIED. The design itself was unadopted, so it is origin evidence rather than sufficient authority. DRAFT_PREREG /gates_before_any_T_result/EPS contains the rule; frozen root V005 A50 item 9 confirms the two-failure refusal; SEALED_PREREG retains the 1.1 rule and the estimate-not-proven-sup warning. POINT_PRODUCER 139–160 implements those comparisons, and 305–329 separately chooses each stored eps as the maximum of discrete, actual, envelope and dense-audit estimates.

The stated rationale is refinement stability of a sampled estimate. No derivation of the exact 10% cutoff from observational uncertainty or a rigorous enclosure was found in this source chain. Root A52.5 and A57.4 preserve the distinction between per-shell envelope searches and proofs. The source history even records sampled EPS underestimation despite passing the 1.1 test; those historical statements were inspected as source evidence, not re-run here. RULE_ORIGIN supplies exact passages and byte pins. This is a scoped provenance finding, not an assertion that no other historical discussion exists.

**5. Near-threshold context (TESTED, saved-record snapshot).** Snapshot date-u: Wed Oct 21 17:23:50 UTC 2026; all 97 input hashes were stable at readback. A shell is one point-specific shell instance. Ratio means eps_refined/eps_base for the last comparison used for the decision. The two bins below are descriptive, not proposed thresholds.

| Cohort | Available points | Shell instances | Ratio (1.05,1.10] | Ratio (1.09,1.10] | Ratio >1.10 |
|---|---:|---:|---:|---:|---:|
| Genesis, numerical rule passed | 31/31 | 5,518 | 111 | 12 | 0 |
| Current list, all available | 17/27 | 3,026 | 62 | 5 | 3 |
| Current list, numerical rule passed | 14 | 2,492 | 47 | 1 | 0 |
| All numerical-rule-passed points | 45 | 8,010 | 158 | 13 | 0 |

The three failing points are rows 302,501,504, each with exactly one failing shell. Their final ratios are respectively 1.122661233412251, 1.1022550974260659 and 1.121347037390027. Each stored failing-shell eps is envelope-dominated, while the governing [4,5] shell passed. Missing current EPS/stage records are 408–411 and 506–511; no success or failure is inferred for them. "Numerical rule passed" here does not mean approved production admission. CENSUS and INPUT_BYTES preserve the individual records, cohort definitions and every input byte pin.

**6. A296 adoption condition and build status.** Root's final 0855/A296 arrived while this independent report was being assembled. The successor build is now authorized and underway; it is not yet reviewed or adopted. The analysis confirms the scoped per-shell, post-run SRB consumption and the absence of numerical EPS in the continuum tail/lapse kernel.

An independent saved-record audit count (EXISTING_AUDITS) finds 672 dense audits over 48 available records. All dense/production ratios are <=1.05; the maximum is 1.0000002660434393 (which rounds to 1.0000, but is not literally <=1). This is empirical stability on the selected audited shells, not a continuous-supremum theorem. None of the three failing shells already has the required dense audit.

For rows 302,501,504, the recorded values satisfy A296 R1(a,b): 10*measured_eps/eps_max is respectively 0.0756152539, 0.0277010178 and 0.0300249366, all <=0.1; the last refinement changes are respectively 1.3329673221e-7, 2.0977796611e-8 and 6.6901401086e-8, all <=1e-6. Each point has exactly one failed discrete shell, and its other shells pass. R1(c) remains UNTESTED on these three shells until their own dense audits run and pass. Multiplying the accepted shell EPS by ten keeps it below the unchanged global maximum and increases that shell's weighted contribution tenfold; the eventual call's SRB gate then uses its own exact stored weights.

This supports the **numerical-policy interpretation** of A296, conditional on the missing R1(c) checks and reviewed integration. It does not independently establish that ten times an estimate is a rigorous true worst case or that the small eps/eps_max fraction alone proves a physical margin. That distinction is escalated explicitly for root's adoption decision. No actual NGC values were used to assess margins.

The requested pure rule/re-evaluator, boundary tests and audit path are being built under immutable new names. Existing admission validators reject the new verdict and need explicit reviewed integration; SRB's per-shell reader itself can stay unchanged. The naive producer context would initialize prohibited NGC run inputs, so it is not executed. A narrowly pinned frozen-coefficient/static-definition route is being checked instead. No new point is claimed accepted or admitted by this report.

No solver, forward/route-A/route-B run, monitor, scientific fixture or reviewed project function/module was executed. Only static source analysis and arithmetic on explicitly authorized certification records ran. No actual NGC data, observed/target velocities, forbidden external run, postseal record, session log or network was accessed. Python was isolated -I -B with six single-thread variables and nice -n 10 requested; nice unavailable (sandbox), 0514 waiver. Minute inbox polling continued throughout.

**Evidence — SHA256 from bytes at posting.**

- **DDO**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py`
  SHA256 `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6`
- **NGC**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py`
  SHA256 `577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377`
- **LIB**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py`
  SHA256 `2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54`
- **ADAPTER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/srb_rot_adapter_c3v003.py`
  SHA256 `08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a`
- **POINT_PRODUCER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/point_response_producer_cx2v002.py`
  SHA256 `a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231`
- **DESIGN**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_design_c2/v002/TAIL_SCHEME_DESIGN_V002.md`
  SHA256 `cdb16d1c42da39cf8eabe253b7192f4f391d19adfdd026e57a6971837a6aa944`
- **DRAFT_PREREG**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_design_c2/v002/KMAX_TAIL_PREREG_V007_DRAFT.json`
  SHA256 `357c0738344a3266b21506b7ab5e4278524a837fc8ccd831cd4222f7cfa8a0a7`
- **SEALED_PREREG**: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/V007_SEAL_ASSEMBLY/KMAX_TAIL_PREREG_V007_SEALED.json`
  SHA256 `b2989012c92161a7da3dd10d0148e1607422416d369fc4ebe164217758b5c695`
- **ROOT_V005_FROZEN**: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md`
  SHA256 `c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1`
- **DRIVER_REVIEW**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/driver_consumption/DRIVER_EPS_CONSUMPTION_CX2V001.md`
  SHA256 `143cd3b891b6511ed6271d6a4f1085a39f9cdd1ddef6d2182fb4b72de83fd34c`
- **DRIVER_SOURCE_PINS**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/driver_consumption/SOURCE_PINS_CX2V001.json`
  SHA256 `b62da5857719195a205c39c9a5ae830c79e78f4e52dafd751dd9b6780d958b0d`
- **RULE_ORIGIN**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/rule_origin/RULE_ORIGIN_CXV001.md`
  SHA256 `35e8d38ae170af5b883c7b06c29c34a4a14d59a670a857cda76b1327e18e7164`
- **CENSUS_REPORT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/census/CENSUS_REPORT_CX2V001.md`
  SHA256 `8609b57d65bc5a4dabd2d2f05311fd48c38e06c8d2a332f1134efe5420eb3b77`
- **CENSUS**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/census/CENSUS_CX2V001.json`
  SHA256 `d9659d9000b74390f49d9a10b2168ca3021e98ba6fbef4380dfe3fa5505d5756`
- **INPUT_BYTES**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/census/INPUT_BYTES_CX2V001.json`
  SHA256 `2a3b96f15321dd1973cd451f06ad9db0e9bce896727c7abf5f3c52fbd0e4ba2e`
- **READBACK**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/census/READBACK_CX2V001.json`
  SHA256 `b6800717e777a66f9f13542bebb2f49591812ffcae47cf771f1a93fb1cc910d8`
- **BOUND_SENSITIVITY**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/BOUND_SENSITIVITY_CX2V001.json`
  SHA256 `75ec37705b1a2e4415bcfc8f3910d995eec787ecc3448f389b6bf17bf147b199`
- **EXISTING_AUDITS**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/EXISTING_DENSE_AUDITS_CX2V001.json`
  SHA256 `6e5d21c923cc6a9c9fc52489ce5eb07dadb9e176c977013bf8917f7431a36306`
- **A296_AUTHORITY**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/A296_AUTHORITY_CX2V001.json`
  SHA256 `d1656a16e386b5bb1d0c6dd566706cd3d06ed47ec83ae1d6bf69b9d10238ea92`
- **DISPATCH_0854**: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0854_2026-10-21_codex2_independent_eps_consumption_analysis_then_rule_successor_standby.md`
  SHA256 `9669f5d4fa93931ad0d546d2ac9834f962ad946b57f45a3695023a92b234ae5c`
- **DISPATCH_0855**: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0855_2026-10-21_codex2_claude3_A296_final_text_build_now_and_F5_gap_proposal.md`
  SHA256 `1541dad07b9d14d994fc7f595c8276f2f0555f38b67f1c8fd1142d883fa36b5a`
