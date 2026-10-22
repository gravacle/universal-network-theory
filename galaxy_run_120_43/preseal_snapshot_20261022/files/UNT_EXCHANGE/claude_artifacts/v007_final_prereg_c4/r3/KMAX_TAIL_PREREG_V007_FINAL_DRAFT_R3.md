# KMAX_TAIL_PREREG_V007: final draft r3 (UNSEALED)

FINAL DRAFT r3 (NOT SEALED). Assembled by Claude4 (dispatch 0580) from r2 58a0b87d, integrating V005 A58-A79 and A80 (open; observed sha 4b937ec11192e3b54cfc114832be2b035c82a91753769c76316afb6bb08dcf5b at assembly) and dispatches 0561, 0576, 0577, 0582. Written before any V007 (tail-corrected) result exists; nothing was launched; C5H, UVT_* and targets were not read. Root fills the named seal slots and seals; the open items are in ROOT_ITEMS_R3.

**Assembly:** Claude4, single author, UTC 2026-10-18T17:47:27Z. Base: r2 `58a0b87d995ce06e13706c127e3783dc352a292f0ec1614cf9b9b877b6140bfa`. Dispatch 0580 `2556b0f2e28447acbfb36c288bd79221e5a7ded74f9b0b9c0c7f21d8aed7288b`. V005 addendum observed `4b937ec11192e3b54cfc114832be2b035c82a91753769c76316afb6bb08dcf5b` (open).

## Seal slots (root fills at seal assembly; never guessed)

- **frozen_addendum**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Root exclusively creates the immutable copy at seal assembly, after the last pre-seal entry; it must contain every entry this text cites; its path and sha go to the binder and into the SEAL_RECORD.  
  *Sources: 0576; 0574; RUNBOOK_V005 step 3; A78*
- **driver**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Path and full sha from bytes at seal; the SEAL_RECORD names it; the launcher refuses a plan whose driver differs (C4-S1, guard v008 / launcher v007); every identity run carries driver_sha256 equal to it (A67 N1). For T-runs see ROOT_ITEMS_R3 RI-24 (recommendation).  
  *Sources: A58 RI-01; A72; A67 N1; A78; 0574*
  - named candidate r5 (verified from bytes, not the slot value): `galaxy_m0_forward_c2v010.py` (`b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6`)
  - r6: NOT_A_CANDIDATE_AT_ASSEMBLY: no r6 BUILD published (driver_r6/ has no BUILD.md); A72 conditions (a)-(c) not yet reported
- **compare**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. The final compare round: r11 (wf_9baf53cd, built from r10), or the fix round r12 if r11's rechecks force one (A80, 0582). It closes A79.1-6, A75 in full, A77.2 per family, A73 F2, every r10 recheck item (including binding gas_M_s_NGC to the registered value or refusing) and every Claude3 and Codex2 r10 finding, plus A71, A68 CHK-1, A69 and the RI-10 dispositions. Checks: three independent refute-by-default recheck lenses (A71; paths and blinding; regression). The distinct reviews of record (Claude3, Codex2) are of the final round.  
  *Sources: A79; A80; 0582; A75; A71; A58 RI-10*
  - named candidate r10_frozen_not_for_seal (verified from bytes, not the slot value): `kmax_tail_compare_c2v007_r10.py` (`e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93`)
- **identity_comparator**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. c2v007 (equal bytes first; strict parse; A59-derived tokens only; injective labels) or its fix round if its own check or Codex2's review requires one; c2v004-c2v006 are superseded and not used at the seal.  
  *Sources: A68; A70; A74; A76*
  - named candidate c2v007_source_observed_still_changing_at_assembly (verified from bytes, not the slot value): `run_identity_compare_c2v007.py` (`06ff52d636c640ebe9a92a4b2cf54620a01514992019e2b2f2dca1529f7dc188`)
- **identity_gate_records**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Z2 (replace-mode tokens, A59), Z2_OFF_RO1 and B0prime_RERUN records produced by the identity-comparator slot on runs of the driver slot (r5 runs launched 14:56Z; r6 reruns if A72 adopts r6); each carries driver_sha256 = the driver slot; records carrying another driver sha are not seal records.  
  *Sources: A59; A67 N1; A72.3; A74; A76*
- **launch_packet**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. BUILD_V005 (46bc5b5d) with the bound plan and command that the build-only binder writes from the selected template, the chosen driver and the frozen addendum (exclusive create); the pending r5 template V010 refuses validation by design.  
  *Sources: A78; 0576; 0577; 0574; Claude4 0079*
  - named candidate build (verified from bytes, not the slot value): `BUILD_V005.md` (`46bc5b5d23bb39e74478e1b8ce49f31ebe07fc5afe59276eb4792375352e6e30`)
  - named candidate runbook (verified from bytes, not the slot value): `RUNBOOK_V005.md` (`c1f574a05d0f0e216223c8ccb69dbdc20d54bcbed52d5b546811a5bd76381956`)
  - named candidate admission_format (verified from bytes, not the slot value): `ROOT_SEAL_ADMISSION_FORMAT_V004.md` (`6908ee88e903443487280bfde6d4e91d6d4a53b621aee543eba8948cfcda1fb1`)
  - named candidate r5_template_plan_PENDING_ADDENDUM (verified from bytes, not the slot value): `LAUNCH_PLAN_V010.json` (`26f1ebf90d95d2674d4bcba7ac3416049cdba171c5754c32440b4c66480c8021`)
  - named candidate r5_template_command (verified from bytes, not the slot value): `LAUNCH_COMMAND_V010.txt` (`7d649ac5e0fe6a17625e7c773e1ed500101367ea8b99d578c2da8f716e1809c4`)
  - named candidate binder (verified from bytes, not the slot value): `bind_sealed_launch_plan_cx1v001.py` (`f3e4e2beeb8f1cb151892fd903b889c471cea58fea1b67c72552137d037575ca`)
  - named candidate guard (verified from bytes, not the slot value): `producer_guard_cx1v008.py` (`294cb7760679b883a62fb3117dc75e91231b2f173bcec65983e6762371ea0731`)
  - named candidate launcher (verified from bytes, not the slot value): `route_a_token_launcher_cx1v007.py` (`861bba68dd7d207beb30ed828c1557955f31979cf2e15369acccc52ea595953d`)
  - named candidate spec_registry (verified from bytes, not the slot value): `SPEC_REGISTRY_R5_MS128_CX1V004.json` (`c7023846299bae03c5793c4187ca334d35ca3108401208761edbca37574dee90`)
  - named candidate delta_review (verified from bytes, not the slot value): `REVIEW_LAUNCH_PACKET_0574_DELTA_C4V002.md` (`2b4832672a0daac814df2658b361afe5330388b784360e6625910eee66349c2f`)
- **certificates**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Root confirms each record of record at seal assembly; every record states source_gas_M_s where it depends on M_s, equal to the case block's gas.M_s, which must be 128 for DDO.  
  *Sources: A70; A67 SF2; A68; A73; A64.2; A58 RI-03; A79 NEW-67*
  - named candidate EPS (verified from bytes, not the slot value): `EPS_CERT_V006.json` (`598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192`)
  - named candidate LO (verified from bytes, not the slot value): `LO_CERT_V004_MS128.json` (`1c384f763e663d85414f25ef8c02b4291efd88b63353a77961f2e88aca2e204a`)
  - named candidate GQ (verified from bytes, not the slot value): `GQ_CERT_V005_MS128.json` (`fbceefe68fecda35745575fba6c85e550e016e8aeefea59233147e520c803e21`)
  - named candidate GQ_FAIL_control (verified from bytes, not the slot value): `GQ_CERT_V004_MS128.json` (`7ebb1d480556bb171861dce8610600e370ec22a4e5687ea2cf272d5647f30e22`)
  - named candidate EPS_NGC_91 (verified from bytes, not the slot value): `EPS_CERT_NGC91_V001.json` (`1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d`)
  - LO_NGC_91: NOT_ON_DISK_AT_ASSEMBLY (Codex1 0049: the sole blocker of the NGC N-test compare)
  - GQ_NGC_91: NOT_REGISTERED_AT_ASSEMBLY (A64.2: with Codex1)
  - named candidate I1T_NGC (verified from bytes, not the slot value): `I1T_NGC_T120L_V001.json` (`3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6`)
  - DOUBLING_merged: NOT_ASSEMBLED (A73: format pending; assembled in the seal-assembly step)
  - named candidate DOUBLING_DDO_half_evidence K128 (verified from bytes, not the slot value): `DOUBLING_K128_V001.json` (`ec169d43cdd116ee663bcbf08719c0d70706f4f2501155701a27dc6a79fb6439`)
  - named candidate DOUBLING_DDO_half_evidence K256 (verified from bytes, not the slot value): `DOUBLING_K256_V001.json` (`1ba4773d9ccc927bc0499f9e57bc6ad3c72d0ff1be1afaa035c910246eb57ab6`)
- **producer_registry**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Root-registered producer paths and shas and the gate-record shas of record (A67 N2); the compare hashes the producer bytes, not only the claimed sha (A69.1); SR_K and every replay gate record bound to it (A62.2). Pinned in the compare as PIN_PRODUCER_REGISTRY (A67).  
  *Sources: A62.2; A67 N2; A67 (seal-time pins); A69.1*

## Binding inputs (sha256 from bytes at assembly)

- **successors**: Every route-A and route-B successor, worker, facade, controller, binding and the reference successor exactly as pinned by the build record of the driver in the driver slot (r5: tail_scheme_impl_c2/driver_r5/ BUILD and CASCADE_MAP_R5 plus the immutable CASCADE_MAP_R5_ADDENDUM required by A69 before the seal; r6, if adopted under A72: its own BUILD and cascade map, a pin-only cascade from tail-module v003). The tail module is the one that driver pins (r5: the TAIL_MEMORY_CAP_BYTES successor of A55.2; r6: v003 with the content-addressed cache, cache-disabled path byte-identical to v002, A72.1).  
  *Sources: A52; A55.2; 0526; A69; A72.1; A72.3; A58 RI-01*
- **c5h_spec**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c5h_hull_c2/CALL_KMAX_C5H_A2F10_HULL_N8_M32_C2V009.json` (`60b4613080055aedd92dbb649cdfa45675f64a4d133c7ba3e4fbb15b59c7704e`)
- **review_v009_orig**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/check/REVIEW_V009_PREP_V009_V001_ORIG_3bce7c02.json` (`3bce7c02926526edf2a594418097ff379604ee1c9760dc1145bcd37ed2882d9f`)
- **identity_specs:**
  - **Z2**: `CALL_UVT_Z2_A2F10_EMPTY_DOMAIN_N8_C2V010.json` (`2d5e79d05bf7d7c517a487e2603a09a14bb3e76979474ab25a717e2a5c656229`)
  - **Z2_OFF_RO1**: `CALL_UVT_Z2_OFF_RO1_A2F10_N8_C2V010R4.json` (`894e5b3ab67d58cd9304aab428923cf4bdfa968cd1dd3518ebc10edba572a39c`)
  - **B0prime_RERUN**: `CALL_REPRO_PINNED_ADMIT_PREFIX_C2V005.json` (`4ac5527ad1731353d798c2648adc1033335a12102ec071b3ae6a619334313cb7`)
- **qinf_evaluator**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/qinf_dependence_c2/tools/qinf_eval_v001.py` (`f58de0dcc67cc4097b4604dc96b640fbf8aaee0520d0478e214673b931eb3346`)
- **v006_r1_sealed**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/v006_r1/prereg/KMAX_MATRIX_PREREG_V006_R1.json` (`807fc5bfcb24ee779137746db3536f41dd97c16bd5f367f79ad5a1b8c3ec067c`)
- **gate_b3_final**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/GATE_B3_C4_V002.md` (`465cb3c3b105c8bea994259bcf347e86910e8a9ebbc502ba83ff617fa83ceacf`)
- **ro1_role_table**: RO1 custody is per case family (A77.2), verified from the driver slot's own tables: DDO cases fbe9ae79 (serial) / 869ce387 (parallel) with binding 86af6198; C4T-D5 and its R-PAIR member (the registered nodes_v001 source) 0ae245d8 (serial) / a5277172 (parallel) with binding 86af6198. The NGC RO1 workers (b6c4586d / ee0510df, binding 52dc4065; A73, A74) are not V007 custody. These are the r5 values; under r6 the table is re-read from r6's cascade map (pin-only) before the seal.  
  *Sources: A62.3; A73 (correction); A74 (binding precision); A77 N7; A77.2*
- **ro1_role_table_r5_pins:**
  - **ddo_worker_serial**: `ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_c2v002_r5.py` (`fbe9ae79ac113aab76109ece785d8030729ce62890dc76ff58144a75af6c17b3`)
  - **ddo_worker_parallel**: `ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_c2v002_r5.py` (`869ce3870a13fdc94a014cdb0b34eab867c05e59ab7d8abfb15f7db382fd52da`)
  - **nodes_worker_serial**: `ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_nodes_c2v001_r5.py` (`0ae245d86ef4f28c9a348094cedca14e5b2f4e704a9c90905a167084ac88af15`)
  - **nodes_worker_parallel**: `ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_nodes_c2v001_r5.py` (`a527717283f8234df6a562eae6a4f28d5c9d34abfbc08cd7cf3f18d7d5f903f2`)
  - **binding**: `ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py` (`86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885`)
- **spec_set**: The ten filled P128/M_s 128 V007 specs of SPEC_REGISTRY_R5_MS128_CX1V004 (c7023846; launch-packet slot), each with the A70 certificate slots; their case block is accepted by the compare's own validate_case_block (Claude3 0065). Specs, caps and order are byte-identical from the reviewed packet to BUILD_V005 apart from the declared changes (Claude4 0076/0079).  
  *Sources: A70; A72 (packet final); A78; Claude4 0079*

## Fixed across all cases

- **anchor**: A2F10, the DDO154 seed of V005; coefficients 2e3a36d8 (V005 anchor block)  
  *Sources: R1*
- **grids**: G2/G3/G4 as V005; G5 (C5H, 108 nodes/axis, kmax 5) for the T2/T2I extension G5\G4; G6 as V006 R1 (120 nodes/axis, prep v009) for C6T.  
  *Sources: R1; A46 RA1; A46 RA3; A46 RA11*
- **tau_km_s**: [0.4, 0.2, 0.175, 0.125, 0.1, 0.05, 0.05, 0.05, 0.075, 0.15, 0.175, 0.325]  
  *Sources: R1*
- **statistic**: V005 criterion.statistic (Dhat)  
  *Sources: R1*
- **validity_gates**: V005 per_case_validity_gates V1-V6. V3 against the registered V007 case block, including the uv_tail config sha and the declared key-equivalence map (any key v010 adds must appear in the map with its absent/default value shown to reproduce v009 behaviour, B0 identity; otherwise V3 fails). The case block asserts each case's registered tail content: source_rule, grid (kept K), outer shape and K_out/K_big, lapse_only, enabled, lambda_scale and the uv_tail config sha; a swapped tail, wrong grid, wrong K_out or wrong K_big is refused (S8). Every pass row-set and the final row-set carry exactly the 12 registered row IDs (no duplicate, no unknown ID), checked before any dictionary is built; a violation is a RECORD_DEFECT and the case reads INCOMPLETE (S9). A pass recorded without rows is a record gap: pass_rows equal passes in number with consecutive indices, otherwise E is unavailable and the case reads INCOMPLETE if no R-PAIR resolves it (B4).  
  *Sources: R1; A48 AMB-13; A54 S8; A54 S9; A54 B4*
- **picard_validity_gate_km_s**: 0.0125  
  *Sources: R1*
- **brackets**: Every V007 tail-corrected case uses C5H's bracket block byte for byte: fs_absolute_overrides [1.5125e8, 3.17625e8] on all 72 columns, le_first [0.4, 0.9], le_next [0.8, 1.1], rfs [0.8, 1.2], rfs override 71: [0.8, 1.01]. Cases: C2T, C3T, C4T, C6T, S4T, C4T-D5, C4T-C5c, C4T-KLO, C4T-KHI, C4T-A (RA4 list with the A56 T3 labels in place of C4T-K16/C4T-K64; RI-05). No W1 widening clause. A miss under the hull makes the case invalid, reading BRACKET_HULL_MISS; next step: its own registration. The identity gates (Z2, Z2_OFF_RO1, B0prime_RERUN) keep their reference specs' brackets, which bitwise identity requires.  
  *Sources: A46 RA4; A48 AMB-16; A55.1; A56 (labels); A58 RI-05*
- **route_a**: Route A is computed in every T-run (PICARD R-PAIR members instead admit their base run's route A) with column_workers 8 (parallel), uniformly across T-cases; route_a.max_iterations = 32 for every T-case, matching C5H and C4T-D5; each case's accepted iteration is reported. Every V007 tail-corrected case uses the RO1 workers from its first launch (RO1 changes checkpoint identity); C5H (v009-EXT, no RO1) is the declared exception admitted under A48 AMB-20 / A50. Admission of a route A or prefix with a different uv_tail digest is refused (UVT_ADMISSION_MISMATCH). The I4 condition (V8c-F1 fix; tail-ON serial == parallel bitwise) was met by the final implementation check (A51), so no column_workers exemption is declared. RO1 records are checked against the case family's role table (binding_inputs.ro1_role_table): serial/parallel against the admitted attempt's column_workers (for T-case PICARD members the base's admitted attempt, per A53), parsed strictly (A71); a cross-family worker or binding is a RECORD_DEFECT.  
  *Sources: R1; A47 I4; A47 I5; A49.4; A51; A77 N7; A77.2*
- **production_tail:**
  - **P**: Production K_big P = 128 /kpc. Outer domains by case (A58 RI-05): C2T, C3T, C4T, C6T, C4T-A and S4T use cylinder K_big 128; S4T keeps its R1 sphere/cube kept-region rule ("sphere tail" = sphere truncation of the kept region with the cylinder tail; A62 note). The exceptions are by design: C4T-KLO (K_big 64) and C4T-KHI (K_big 256) (T3); C4T-C5c (continuum_v001, outer cube K_out 5, RA2); C4T-D5 (nodes_v001 on G5\G4, no continuum outer, RA1). RA4's case list reads C4T-KLO/KHI.  
    *Sources: A55.1; A54 (generic T3); A46 RA2; A56 (labels); A58 RI-05; A62 (S4T note)*
  - **source_rule**: continuum_v001 (C4T-D5: nodes_v001 on G5\G4, RA1)  
    *Sources: R1; A46 RA1*
  - **gas**: interp lagrange3_s_gl4 with **M_s = 128 for every DDO tail-corrected case** (registered change, made openly before any T result: at M_s 64 the GQ gate fails at the reach P = 128 needs); NGC keeps M_s 96 (its GQ passes to 32). NGC: production K_big 32 (A64.2) with M_s 96 unless GQ_NGC at M_s 96 fails on its required coverage (>= sqrt2 * 64 = 90.5, i.e. to 91 /kpc), in which case root rules on M_s 128 (A64.2; ROOT_ITEMS_R3). The certificate M_s must equal the case block's registered gas.M_s, and for DDO that value must be 128 (A68 CHK-1, A75.8, A79 NEW-67). The compare binds the NGC gas M_s to the registered value (96) or refuses (A80, r10 validity recheck note).  
    *Sources: R1; A46 RA7; A57.1; 0532; A60; A64.2; A68 CHK-1; A75.8; A79 NEW-67; A80*
  - **quadrature**: Defined by the registered rules: order 8; w_perp_max 0.05 /kpc; w_z_max 0.02 /kpc; phases 1.415 / 1.34 rad; corner_zone_rule as R1 (IA1). The module derives N_perp and N_z from K_big. R1's numeric N values (N_z_plus 12800) are the K_big 32 instance and informational. The R/z eval and source extents depend on geometry and are unchanged. Each case block carries the sha of its registered P128 uv_tail config (S8).  
    *Sources: R1; A54 S8; A55.1; A58 RI-03*
  - **asymptote**: EH_exact_minus_quarter  
    *Sources: R1*
  - **lapse_only**: true (non-lapse components bounded by LO / LO_NGC)  
    *Sources: R1*
  - **jet_order**: {"route_a": 1, "route_b": 2}  
    *Sources: R1*
  - **stars**: {"segment_rule": "max16_ceil_kdr_plus8", "tail_rule": "t_panels_40a_phase1p5_gl12"}  
    *Sources: R1*
  - **memory_guard**: TAIL_MEMORY_CAP_BYTES is a resource guard, not numerics (design K15); r5 raises it to 8 GiB through a module successor that is AST-identical otherwise (A55.2). Under r6 the module is v003 (A72.1).  
    *Sources: A55.2; 0513; A72.1*
  - **tail_table_cache**: A72: adopted only if (a) the independent check passes, including stale-cache attacks, (b) bitwise equality is TESTED at K_big 32, 128 and 256, and (c) the measured timings (kbig_timing_v003/) show a net saving after the cost of the cascade, its review and an identity rerun. If adopted, the sealed driver is r6; the identity runs are rerun on r6 with caching enabled where the tail is ON; every V007 T-case runs with the cache, so all are compared on equal footing; the r5 identity runs are superseded and kept. If any condition fails, V007 seals on r5 and no case uses the cache. The cache is bitwise exact (hit, miss and cold builds identical). At launch the plan's driver must equal the SEAL_RECORD's driver (C4-S1; A78), so the ten T-cases of one bound plan share the sealed driver.  
    *Sources: A72; A72.3; A78*
- **kept_region_rule**: route A, reference, body: cube K; offset t[delta]: stage mask (N1); route-B columns/rotations: stage mask  
  *Sources: R1*

## Pairing and decidability

- **noise_allowance**: Norm in which contraction is measured: ||d_k||_tau = max_i |d_k,i|/tau_i. q = the larger of the last two observed ratios ||d_k||_tau/||d_k-1||_tau (with only one ratio, that ratio); there is no cap (A58 RI-18). For q < 1 the norm-level bound is E_i^norm = tau_i * ||d_last||_tau * q/(1-q), exactly; with exactly one increment, E_i = tau_i * ||d_last||_tau. Per-row bound for rows whose last two increments have the same sign (d_last,i * d_prev,i > 0): |d_last,i| * q_i/(1-q_i), q_i = |d_last,i|/|d_prev,i|, exactly (S7 without the 0.9 cap). Alternating bound for rows whose last two increments change sign: the tail of a geometric series with ratio -q_i, |d_last,i| * q_i/(1+q_i), q_i = |d_last,i|/|d_prev,i| (A56 N1). E_i = max(E_i^norm, same-sign bound, alternating bound). E is UNAVAILABLE for the run (its tests undecidable; to R-PAIR) when: no increment is observed; a tau-norm ratio >= 1 on either of the last two ratios (NEW-7); any row has q_i >= 1, same-sign or alternating (A56 N1); or a pass-row gap / row-ID defect exists (B4, S9). A slowly contracting run (q near 1) therefore gets a large E and goes to R-PAIR. E_i(pair) = E_i(a) + E_i(b). The geometric bound assumes the observed ratio is the map's contraction factor: DECLARED, checked against each run's own increments.  
  *Sources: A51 F2; A54 S7; A56 N1; A53 NEW-7; A48 AMB-05; A54 B4; A54 S9; A58 RI-18*
- **decidable_iff**: E_i(pair) + E^A_i(pair) <= tau_i/8 on every row  
  *Sources: R1*
- **decidability_scope**: Decidability applies to T1_H, T2 and T3 (pass texts say "decidable"); not to T1, T2c, T1_S or RB_FP.  
  *Sources: A48 AMB-06*
- **if_not_decidable_R_PAIR**: R-PAIR once, branch chosen on the worst undecidable row (largest (E + E^A)/tau): if E is unavailable, branch PICARD; else if E^A_i(pair) > E_i(pair) on that row, branch ROUTE_A, otherwise PICARD. ROUTE_A members recompute route A with route_a.seed_source_rtol_factor 0.1 (absent = 1.0, byte-identical; B0 covers absence); their route-A identity must differ from the base's (NEW-16); the C5H ROUTE_A member carries ro1_workers true. PICARD members admit their base run's route A (route_a.column_workers = 1 is a registered PICARD leaf, byte-equal between members), with picard.passes 12 and speed_change_bound_km_s 0.0025 (byte-equal between members); V6 requires route_a_outcome.result_sha256 equal to the base's; a T-case PICARD member's RO1 record equals its base's canonically and its worker-kind check uses the admitted attempt's worker (R3-4); the C5H PICARD member carries no ro1_workers and reads ro1 armed false, fired false. Each member is validated against its partner and against its base, with only the registered R-PAIR leaves allowed to differ; a member's V2 uses its registered speed bound. C5H members run under v010 tail OFF with the RO1 workers where their branch computes route A, admitted through B0 identity, with worker/binding pins on the declared custody list. A manifest naming R-PAIR members for a test whose R-PAIR was not triggered is refused at load, before any test is read (NEW-17). PICARD members inherit their base run's flag and a cleared base clears them; ROUTE_A members carry their own flags. Still not decidable -> UNDECIDABLE_AT_ITERATION_FLOOR (reported; the test neither passes nor fails). On an exact tie in (E + E^A)/tau the branch row is the lowest row index (deterministic; A69 AMB-07). Member RO1 records follow the case family's role table (A77.2; for T-case PICARD members serial/parallel is checked against the base's admitted attempt).  
  *Sources: R1; A48 AMB-07; A48 AMB-14; A50 B1; A50 N4; A50 item 1; A50 item 10; A50 item 11; A52.3; A53 (R-PAIR, NEW-16, NEW-17); A53 R3-4; A69 (AMB-07); A77.2*
- **thresholds_unchanged**: test thresholds are never widened by E_i; E_i only decides decidability (thresholds separated from the Picard gate, CHECK K7)  
  *Sources: R1; A51*
- **T2_numerics**: C4T-D5 numerics are byte-equal (canonical JSON) to the numerics of the C5H spec 60b46130 after removing composite_grid_spec and uv_tail, and apart from the keys of the declared key-equivalence map in the seal record. The C5H run's normalized numerics must equal the spec's, normalized by its dry run. No column_workers difference is declared (A47 I4; both register route_a.column_workers 8).  
  *Sources: A46 RA1; A47 I4; A48 AMB-13; A50 S1; A47 I2*
- **route_a_noise**: E^A_i(run) = the per-row static rotation-channel effect, in km/s, of the last accepted route-A update: max over the 8 column azimuths of R_i c^2 |d_R packet_K[updated_acc - gas_acc](R_i, phi_j, 0)| / (2 v_i^ref) (the per-row form of M_K at the accepted iteration); E^A_i(pair) = E^A_i(a) + E^A_i(b). C5H's E^A comes from a required EA replay record computed after the seal from C5H's route-A outputs by this formula; the EA record carries the row radii so the row order is verified (or v010 copies probe_R_m into the tail record); the EA record covers C4T, C6T, C4T-D5, C4T-KLO, C4T-KHI and C5H.  
  *Sources: R1; A48 AMB-08; A48 AMB-22; A50 item 13*
- **diagnostics_recorded**: Route-A accepted iteration and Picard pass count of each member and case: recorded, not compared.  
  *Sources: R1; A48 AMB-21; A47 I5*
- **T1_status**: T1 is not subject to the decidability rule: its Dhat pairs follow V005 exactly as sealed; RA6 adds the per-row clause.  
  *Sources: R1; A48 AMB-06; A46 RA6*

## Gates before any T result

- **B0**: planning identity: v010 tail-OFF dry-run requests/inputs/normalized specs byte-identical to v009-EXT after the declared GEO substitution map, and to v009-GEO after the declared EXT map (EXT spec set incl. V005/V006 R1/G5/G6; GEO set incl. 2029f26a, 4ac5527a, A2F10, A2F10_RA8; NGC templates). Counting rule: B0 counts only comparisons whose expected reports are non-empty and whose planning completes; equal early failures are listed separately as no evidence (B0-EMPTY). The six historical positive R3 specs (C2R3, C3R3, C4R3, S4R3, RR3, Y3R3) refuse identically in both drivers (seed/admission custody) and are listed as no evidence, neither a blocker nor a pass; B0 coverage = the completed non-empty comparisons plus separately labelled computed-plan derivatives. The successor B0 tool and a B0 record rerun are required before the seal. Under A55, B0 also shows r5 plan-identical to r4 on every spec (with the B0-EMPTY rule). Each A52.3 C5H R-PAIR member's own spec sha is listed in spec_sets/EXT with its projection to v009-EXT form and its declared differences as evidence.  
  *Sources: R1; A54 (B0-EMPTY); 0530 item 3; A55.2; A53 (r4 validity F1)*
- **B0prime_DRY**: v010 tail OFF and each parent in dry-run on the B0 spec sets: DRYRUN_REPORT.json and DRYRUN_PLAN.txt identical under the declared substitution maps (gal_c2v005 CHECK CMP_DRY method, incl. the ngc_route_b_table needle lines)  
  *Sources: R1*
- **B0prime_RERUN**: prefix-admitted rerun of spec 4ac5527a under v010 tail OFF: result equal to v009-GEO deciding (i) except declared custody fields; declared exceptions: (i) every string value beginning with the run outdir path, compared after substituting that prefix (e.g. stage_records[].stage_dir, passes[].rotation_arrays.path, identity.route_a.checkpoint); (ii) elapsed_seconds at top level and in stage_records[]; (iii) the driver-custody field list. Its route A is admitted from a saved run, so RO1 cannot be armed: it requires ro1 armed false and fired false (exempt from A50 item 12). Rerun on v010 r5. Compared by the identity-comparator slot; carries driver_sha256 = the driver slot (A67 N1); rerun on r6 if A72 adopts r6.  
  *Sources: R1; A52.1; A55.3; A67 N1; A72.3; A74*
- **B0_FA**: R-A F-A cases A1/A2/A4 end REFUSED (ROUTE_A_CHECKPOINT_MISSING) under v010; default path identity unchanged  
  *Sources: R1*
- **B0_RO1**: (a) RO1 fires in no identity-gate run; if it fires, that identity gate fails (RO1_FIRED_IN_IDENTITY_RUN). (b) A replay on the C6 iteration-8 checkpoint records ROUTE_A_READOUT_NO_CIRCULAR_BRANCH at query 03 and hands the checkpoint to route B. (c) Every other exception, and a refusal before convergence, still fails the call. RO1 set = {NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH, DEGENERATE_RADIAL_EULER, NON_TIMELIKE_COLUMN}, exact messages (incl. the full L205 string "DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed"), type(exc) is ValueError, only after a converged solve. A case that requires RO1 requires route_a_outcome.ro1.armed true. RO1 firing in a T-run is recorded, not an invalidity; route-A circular-trial rows are diagnostics only; route B decides. A repeated B0_RO1 case kind is a RECORD_DEFECT (guards keyed on the semantic kind, not the whole object; A79.1).  
  *Sources: A46 RA5; A49.1; A49.2; A50 (A49 in the compare); A53 r4 validity F3; A79.1*
- **B0_N3**: In tail-OFF mode v010 constructs no TailBoundary; the final checker verifies statically that every TailBoundary construction is guarded by an enabled uv_tail block; B0prime_RERUN and Z2_OFF_RO1 bitwise identity are the runtime check. A repeated constructions entry is a RECORD_DEFECT (A79.1).  
  *Sources: A46 RA8; A47 I6; A52.1; A79.1*
- **B1_Z2**: Z2 = spec 2d5e79d0 (A2F10 C2, v010 tail ON, cylinder K_big = K = 2, every stage domain empty), route A at N8 as registered in that spec (route_a.column_workers 8; R1's "serial" is superseded, A58 RI-11), RO1 workers armed (ro1.armed true, fired false), against DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001 (883b37a0; COMPARE_DECIDING_II e1d3c072 shows it bitwise equal to serial): all route-A blobs/records/arrays, every stage npz, rows and speeds equal; only the declared custody list differs. The token map is derived by rule from the sealed driver's pin tables only (A58 RI-12), never from the observed diff, and for the 8 successor kinds it REPLACES the base->token mapping on the new side (A59: the new side must carry the successor, so a base script on the new side fails the gate). Tokens follow the identity comparator's closed grammar: only A59-derived [ref, new, token] triples, each exactly once, injective labels (A73 SF2, A74). Compared with the identity-comparator slot (c2v007 lineage); the raw successor-custody check is recorded in the seal record (A59). The run carries driver_sha256 = the driver slot (A67 N1). Precondition L as R1.  
  *Sources: R1; A50 item 12; A52.1; A55.3; A54 pre-seal status (Z2 ruling); A57; A57.3; A58 RI-11; A58 RI-12; A59; A67 N1; A73 SF2; A74; A76*
- **Z2_OFF_RO1**: Mandatory: spec 894e5b3a = the 883b37a0 reference spec under v010 tail OFF with the RO1 workers armed; compared by the identity-comparator slot with tail-OFF semantics: admits only the declared enabled:false records, fails any other uv_tail record, requires ro1 armed true and fired false. Rerun on the driver slot (r5 runs launched 14:56Z; r6 if adopted); carries driver_sha256 = the driver slot.  
  *Sources: A47 I6; A52.1; A52.2; A55.3; A57.3; A67; A67 N1; A72.3; A74; A76*
- **B2**: static rows on saved C2R3/C3R3/C4R3 le3 (rotation_v005 uvt successor + unchanged column mean; continuum_v001, O = cube 12) equal to an independent Cartesian tensor-GL implementation (box(12)\cube(K), 16 azimuths, no symmetry reduction) to <= 1e-4 km/s per row; sanity vs study ADV_TAIL_CHECK KB12 within the m16 alias + star-roster difference (<= 0.05 km/s)  
  *Sources: R1*
- **B3**: independent-lane Cartesian implementation (no import of the tail library; box(8)\cube(4), doubling-converged 1e-10) on saved C4R3: value/gradient/Hessian <= 1e-8/1e-7/1e-6 of max; lapse pair <= 1e-8 max|t|; bd(z=0) == 0.0 exactly; facade midplane ratio == 0.0 and HI v003 L67 passes; reference/body angular reads (TailBoundary tap) <= 1e-7 max|grad t|; column potential(z) <= 1e-7 of max tail potential difference; imaginary part == 0.0; PLUS a cylinder-O case: O = cylinder K_big = 8 over cube 4, same points and tolerances, the independent lane integrating in (k_perp, psi, k_z) with the cube corner zone K < k_perp <= sqrt2 K handled by its psi limits  
  *Sources: R1*
- **EPS**: Numerical sup searches are estimates, not proofs; envelope consumers read the full-envelope fields (A57.4). q(k) sampled via QINF evaluator f58de0dc (cache 7b9816ae cross-check), 13+13 directions x 64/decade per unit shell of [K, K_big]; refined 26+26 x 128/decade; eps_s(refined) <= 1.1 eps_s(base) else refine; 2 refinement failures -> EPS_UNCERTIFIED. Coverage: DDO from 2 to at least sqrt2 * 2P (= 362.04 at P = 128; the DDO record covers [2, 363]); NGC at production K_big 32 with N3' to 64: >= sqrt2 * 64 = 90.5, i.e. [2, 91] (A64.2; supersedes RI-17's [2, 46], which was the K_big 32 N3-case edge of A58). The record carries envelope_bound {rule A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS, coverage_max_inverse_kpc} with coverage >= sqrt2 * 2P (A52.5 as raised by A54). The top-level and nested "dominates" flags must agree; a disagreement is a RECORD_DEFECT (A67 N4). EPS does not depend on M_s (A68); the record of record is the EPS slot (A70: EPS_CERT_V006 598c8fa3 for DDO; EPS_CERT_NGC91 for NGC). Until such a record is slotted, per-shell values above 15 /kpc are lower bounds and SRB_ROT is not read. An estimate, not a proven sup.  
  *Sources: R1; A52.5; A53 NEW-19; A54 (coverage); A55.4; A50 item 9; A57.4; certificates_v002 (coverage note); A58 RI-17; A64.2; A67 N4; A68; A70*
- **LO**: LO (V001 sec 1.6) on the DDO shells, at the M_s 128 source (A57.1), with the partition ruled by A58 RI-06: (4,5], (5,6], (6,8], (8,12], (12,16], (16,32], (32,64], (64,128], (128,256], (256,363]. Each shell <= 0.005 tau, summed <= 0.05 tau; coverage starts at lo >= K = 4 and reaches >= sqrt2 * 2P (A69.2, A54, A55.4). A duplicate shell is a RECORD_DEFECT naming both entries (A71, A75 A01), keyed on the shell range. The record states source_gas_M_s, which must equal its own gas_M_s and tail_config gas.M_s (A73 F2) and the case block's registered gas.M_s, which is 128 (A68 CHK-1, A75.8, A79 NEW-67); a superseded M_s 64 record refuses. Record of record: the LO slot (A70: LO_CERT_V004_MS128 1c384f76).  
  *Sources: R1; A54 (coverage); A55.4; A57.1; A58 RI-06; A68 CHK-1; A69.2; A70; A71; A73 F2; A75 A01; A75.8; A79 NEW-67*
- **GQ**: For every gas roster used, the gas transform at M_s and at 2M_s agrees to <= 1e-12 * P0, certified per source geometry over the union of all T-case tail node domains (DDO C2T-C4T, C4T-KLO, C4T-KHI, incl. the corner zones). At production M_s 128 the DDO certificate is computed at M_s 128 against 256 over the full DDO reach on all nodes (A57.1); the all-nodes check uses the root-registered per-geometry production node counts from the gq_full part records, and a record whose all_nodes count equals the 4096 sample refuses (A67 SF1). Roster names map to geometries by the fixed map DDO_C2T -> C2T_KB<P>, DDO_C3T -> C3T_KB<P>, DDO_C4T -> C4T_KB<2P>; a mismatch, a duplicate roster name, or a roster name repeated with a different valid geometry is a RECORD_DEFECT (A75.6 P-SF1, A75 A05, A79.1). The certificate M_s is bound as in LO (A68 CHK-1). Record of record: GQ_CERT_V005_MS128 (fbceefe6), with V004 (7ebb1d48) as the FAIL control (A67 SF2, A70). NGC: GQ_NGC is a required input over [2, 91] at the NGC M_s (A62 via 0544, A64.2). A failure or a coverage shortfall reads UV_TAIL_GAS_QUADRATURE_UNCERTIFIED, which is NUMERICS_UNCERTIFIED.  
  *Sources: A46 RA7; A48 AMB-12; A50 item 8; A55.1; A57.1; A64.2; A67 SF1; A67 SF2; A68 CHK-1; A70; A75 A05; A75.6; A79.1; 0544*
- **DOUBLING**: (w/2, o+4) is required at K_big 128 and 256 with gas M_s 128: DDO static rows on saved C4R3 le3 change <= tau_i/20 (A58 RI-03); NGC lnN reads on the saved operator change <= theta/20 at the NGC production K_big. One merged record (FIELDS_R7/R8 shape) carries ddo_K_big_inverse_kpc {128, 256}, ddo_gas_M_s 128 and the NGC half (ngc_operator_sha256 e6453d52, ngc_max_change_over_theta from NQ at K_big 32); it is assembled at seal assembly and must exist before the seal (A73, A58 RI-03; the DDO half PASSed at 128 and 256, max 4.7e-13 tau, independently recomputed). Its sha is registered before the seal (A79 NEW-61) and it keeps RI-03's production-128 rule (A79 NEW-67).  
  *Sources: R1; A58 RI-03; A73; A79 NEW-61; A79 NEW-67*
- **I1T**: at every tail build: roster transform vs packet source at 4096 seeded nodes <= 1e-12 relative (UV_TAIL_SOURCE_MISMATCH); the I1T record covers every T-case.  
  *Sources: R1; A48 AMB-11*
- **T2I**: Before T2 is read: nodes_v001 transform replicas applied to the C5H rosters equal the C5H stored packet sources on G5\G4 to <= 1e-12 (route-A updated per iteration; offset new_body_fourier_J; feedback gas_source_feedback). A T2I failure reads IMPLEMENTATION_DEFECT (T2I).  
  *Sources: A46 RA3; A48 AMB-10; R1*
- **SRB_ROT**: static rotation-law channel bound (V001 sec 1.4, renamed; necessary, not sufficient) <= tau_i/10 on C4T. Computed on C4T: when C4T is flagged, a pass carries the flag and a failure is undecidable. Not read until the EPS envelope record (A52.5) is slotted.  
  *Sources: R1; A50 item 7; A52.5*
- **RB_FP**: RB-FP_i = 2 * eps_max * |dv_i/dlambda| * kappa_i <= tau_i/10; dv_i/dlambda := (|v_i(C4T-A) - v_i(C4T)| + E_i(C4T-A, C4T))/0.05 (conservative); the noise contribution 2 kappa_i eps E_i/0.05 is recorded; kappa_i = sum_s|dV_static_is| / |sum_s dV_static_is| (shell split, saved C4T); first-order response DECLARED, UNTESTED. E is the Picard allowance only. If C4T's E is unavailable (NEW-7, A56 N1) or C4T has a B4 gap, RB_FP reads E from C4T's Picard R-PAIR member (the 12-pass rerun admitting C4T's route A); C4T-A gets the same Picard path; both are on the resolvable list; an unresolved one, or RB_FP with undefined kappa, reads INCOMPLETE. Shell labels are read by index and never emitted verbatim in blinded modes (S6). The shell split covers the domain exactly [K, sqrt2 * P]; excess, shortfall or a partial-domain record refuses and never PASSes (A62.1, A67 N3, A69.2).  
  *Sources: R1; A48 AMB-09; A50 item 9; A56 N2; A54 S6; A62.1; A67 N3; A69.2*
- **MT_monitor**: route-A per-iteration M_T (static rotation-channel effect of t[S_T(updated_n)] - t[S_T(gas_n)] at 12 row radii x 8 azimuths in tau units, v_ref = A2F10 route_a_rows); M_T(accepted) <= 1/4 else flag TAIL_SOURCE_UNDERCONVERGED (stopping rule unchanged). An MT verdict FAIL for a run is the TAIL_SOURCE_UNDERCONVERGED flag on that run; a defective MT record reads NO_RUN; an MT record, when supplied, covers every T-case.  
  *Sources: R1; A50 S2; A48 AMB-25*
- **result_assembly_identity**: Gated ONLY by B0prime_RERUN, B1 (Z2) and Z2_OFF_RO1, on DDO154; NGC result assembly is UNTESTED (deciding test: the first NGC route-B result under the NGC driver successor compared with a v009 parent).  
  *Sources: R1; A47 I6; A52.1; 0517*
- **LO_NGC**: LO_NGC is the readout-coupled share, the quantity the N-tests read (lnN only, metric v002 L76); the field-level indicator is carried as an auxiliary field; the record carries an honest i1t field. NGC I1-T of stars + H2 against the T120L fixed source must pass before any NGC N-test is read. LO_NGC is reported only in this compare; the NGC N-tests get their own small compare before any N-test is read; N-tests are not read as passed before LO_NGC passes. At NGC production K_big 32 its shell coverage reaches >= 91 /kpc (A64.2); shells keyed on range, a duplicate is a RECORD_DEFECT (A75 A01); an NGC roster with a different range refuses (A79.1). Lane state at assembly: LO_NGC to 91 is absent and is the sole blocker of the NGC N-test compare (Codex1 0049).  
  *Sources: A52.4; A48 AMB-23; R1 (L8); A64.2; A75 A01; A79.1; Codex1 0049 (state only)*
- **HARMONIC**: Reported, not deciding: a0/a4/a8 of dlnN/dR at route-A query 03 (R = 1.48 kpc), at the four diagonal azimuths, for C4T, C4T-D5 and C6T, and for C4R3, C5H and C6 direct (C6 from its checkpoint replay). A repeated HARMONICS row is a RECORD_DEFECT (A79.1).  
  *Sources: A46 RA10; A79.1*
- **RECEIPTS**: A receipt is required for every run case; a missing receipt reads INCOMPLETE.  
  *Sources: A48 AMB-26*
- **record_verdicts**: A gate record whose verdict contradicts its own data is a RECORD_DEFECT (NO_RUN group), not a decided failure; a defective or malformed gate record reads NO_RUN with next step "fix the record or gate and re-review", never a physics reading. An unregistered record reads NO_RUN (A67 order N1). Seal-time record states: GQ_CERT_V003 (no all_nodes), LO_CERT_V003_MS128 (no source_gas_M_s), the c2v004 identity records and unregistered gate records read RECORD_DEFECT until re-emitted (A73).  
  *Sources: A54 S5; A48 AMB-02; A67 (order N1); A73*
- **no_last_wins**: Any list-to-mapping conversion, and any JSON object, rejects duplicate keys before the mapping is built: shells, rows, cases, gates, members, tokens, registry entries, NPY/NPZ headers and the JSON parse itself (object_pairs_hook). A duplicate is a RECORD_DEFECT naming both entries by index or JSON path, never by a record label (blinding), even when the values are equal. Guards key on the semantic identity (case kind, roster name, shell range), not the whole object. NPZ archives: collisions are rejected both in raw member names and in the logical names NumPy uses; an extensionless NPY member is refused. No tool may be last-wins anywhere; the final compare round lists every dict-from-list site with its guard and a MUST_FAIL test. Every refusal site names both entries, including the fifteen sites listed in A79.6 (T01/T02; C02-C04 and S01; the registry duplicate-key forms; the S9/D2 row codes, C10, A06/A07/B09).  
  *Sources: A71; A74; A75.1; A75.2; A75.3; A79.1; A79.4; A79.6*
- **after_seal_marker_policy**: PRODUCED_AFTER_THE_SEAL is accepted only for the eight gates computed from V007 run outputs: SRB_ROT, RB_FP, T2I, EA, MT, I1T, FLAG_RULINGS and HARMONICS; at compare time those records are verified by producer pin against the producer registry (A62.2, A69). It is refused for SR_K, EPS, GQ, LO, LO_NGC, DOUBLING and the identity gates, whose records of record exist (and SR_K's gate-record sha is registered) before the seal.  
  *Sources: A79 NEW-61 (as corrected 17:16Z); A75.7 (corrected by A79); A67 N2; A62.2; A69*
- **c5h_interlock**: c5h_path_hit and read_run catch /.vol/<dev>/<ino> aliases of the C5H run directory and its files, and hard links, by (st_dev, st_ino) against every file of the C5H run (H-07); rejecting any multiply-linked file on the protected device is the accepted conservative substitute for a per-file inode inventory (NEW-64); a failed os.stat of the registered C5H root is a refusal, never a silent drop (A79.3). The name test and the identity walk run on the resolved path as well as the lexical one; every prefix of realpath(s) is stat-walked against the registered (st_dev, st_ino); strings are NFC-normalized before every comparison, so firmlink (/System/Volumes/Data), NFD and symlink-then-/../ spellings are caught (A79.5). A refusal can delay the verdict but never changes a reading.  
  *Sources: A72 (H-07); A75.4; A79.3; A79.5; A79 NEW-64*
- **blinded_output**: Blinded modes print codes only: the 13 early-refusal sites (A75.5) and the CLI parser, whose error() raises a typed refusal and prints a code only, with allow_abbrev=False and repeated flags refused (A79.2, A76 SF-ARGV).  
  *Sources: A75.5; A79.2; A76 (SF-ARGV)*
- **certificate_ms_binding**: Every certificate whose content depends on M_s states source_gas_M_s; it must equal the record's own gas_M_s, its tail_config gas.M_s and the case block's registered gas.M_s, and for DDO that value must be 128 (both bindings hold together). A superseded M_s 64 certificate refuses in an M_s 128 context; a matched-64 control refusing is correct.  
  *Sources: A68 CHK-1; A68 (records); A73 F2; A75.8; A79 NEW-67*

## Tests

- **T1**: Pass iff cases C2T, C3T, C4T are valid AND V005 criterion.shape_pass literally (Dhat_T(3,4) <= 1 AND Dhat_T(3,4) <= 0.5 * Dhat_T(2,3)) AND RA6: for every row i, d23_i * d34_i >= 0 and |d34_i| <= 1/2 |d23_i|, where d23_i = v_i(C3T) - v_i(C2T), d34_i = v_i(C4T) - v_i(C3T); if d23_i = 0 the row passes only if d34_i = 0. TINY (DECLARED; applies to the RA6 clause only): a row is TINY iff |d23_i| <= tau_i/8 and |d34_i| <= tau_i/8; TINY rows are exempt from the per-row clause and stay in Dhat. No floor clause; FLOOR_LIKE pre-named (D14). Known blind spot (G5): a growing row whose increments both stay <= tau/8 is exempt; the backstop is T1_H.  
  *Sources: R1; A46 RA6; A47 I2; A47 (G5)*
- **T1_H**: C6T against C4T: per row |v_i(C6T) - v_i(C4T)|/tau_i <= 1/2 every row, decidable; no TINY exemption. C6T is consistent through RO1.  
  *Sources: R1; A47 (G5 backstop); A47 I7*
- **T1_S**: {"runs": ["S4T", "C4T"], "statistic": "max_i |dv_i|/tau_i", "pass": "<= 2 (V005 tau_shape_agreement)", "S4T": "route-B sphere mask with sphere tail; route A, reference, body cube with cube tail"} ("sphere tail" for S4T = sphere truncation of the kept region with the cylinder K_big 128 outer tail; A62 note, A58 RI-05.)  
  *Sources: R1; A62 (S4T note); A58 RI-05*
- **T2**: C4T-D5 against C5H (spec 60b46130): per row |dv_i|/tau_i <= 1/4, decidable, T2I passed. C4T-D5 = K = 4 cube with the nodes_v001 tail on G5\G4 (lapse-only; the LO certificate on shell (4,5] makes a T2 difference read as tail-implementation error).  
  *Sources: A46 RA1; A52.6; A46 RA11*
- **T2c**: C4T-C5c (continuum_v001, E1, outer cube K_out = 5) against C4T-D5: per row |dv_i|/tau_i <= 1/2 (PASS/FAIL); a failure reads SOURCE_RULE_MATERIAL.  
  *Sources: A46 RA2; A46 RA11*
- **T3**: With production K_big P = 128: T3 = {C4T-KLO (K_big 64 = P/2), C4T-KHI (K_big 256 = 2P)}, each against C4T at P per row <= tau/4, decidable. Producers emit the labels C4T-KLO and C4T-KHI; A55's "C4T-K64/K256" is descriptive only. The compare reads P, P/2 and 2P from the registered case block and refuses any other values; the R1 labels C4T-K16/C4T-K64 are retired.  
  *Sources: A54 (generic T3); A55.1; A56 (labels)*
- **RB_FP_run**: {"runs": ["C4T-A", "C4T"], "C4T-A": "C4T with lambda_scale 1.05 in every stage"}  
  *Sources: R1*
- **SR_K**: {"kind": "static replay", "states": ["C2R3", "C3R3", "C4R3"], "K": [2, 3, 4], "statistic": "Delta_i(K) = rows[packet_K(S_pkt)+t_K] - rows[packet_K(S_T)+t_K] (unit response from each case 01_offset/unit_response.npz); pairwise K-dependence", "use": "reported; enters u_i and the T1-fail reading as max(|Delta_i^SR(4)|, |Delta_i^SR(4)| * A_i), A_i = |dv_i/dlambda| / |dV_i^static,tail| from the AMP run (DECLARED, UNTESTED); the static value is labelled \"static only; fixed-point UNTESTED\", deciding test C4T-SR; flag SOURCE_QUADRATURE_MATERIAL if that max exceeds tau_i on any row"} SR_K and its gate record are bound to root-registered producer shas (A62.2); its gate-record sha of record is registered in the producer registry before the seal (A67 N2), so PRODUCED_AFTER_THE_SEAL is refused for SR_K (A79 NEW-61); a synthetic or fixture record refuses; a bitwise-identical Delta across K is an SR_K RECORD_DEFECT (A67 N2).  
  *Sources: R1; A62.2; A67 N2; A79 NEW-61*
- **D_m4**: {"runs": ["C4T", "C4R3"], "statistic": "v009 harmonic diagnostic m4", "use": "reported"}  
  *Sources: R1*

## Decision rule

- **ADOPT_TAIL_cube_K4_C4T**: All of B0, B0prime_DRY, B0prime_RERUN, B0_FA, B0_RO1, B0_N3, B1 (Z2), Z2_OFF_RO1, B2, B3 (incl. cylinder-O), EPS, LO, GQ, LO_NGC (for NGC readings), DOUBLING, I1T, T2I, SRB_ROT, RB_FP pass; T1, T1_H, T1_S, T2, T2c, T3 pass; a receipt for every case; no flag unruled; every step resolved (otherwise INCOMPLETE with the pending steps named). No RECORD_DEFECT anywhere (A71); every seal slot filled and verified from bytes (0580).  
  *Sources: R1; A46 RA5/RA7/RA8; A47 I6; A48 AMB-17; A48 AMB-26; A71; 0580*
- **carried_uncertainty_u_i**: |v_i(C4T)-v_i(C3T)| + |v_i(C6T)-v_i(C4T)| + |v_i(S4T)-v_i(C4T)| + max(|Delta_i^SR(4)|, |Delta_i^SR(4)| A_i) [static only; fixed-point UNTESTED, deciding test C4T-SR] + RB-FP_i (km/s; reported with u_i/tau_i and u_i/sigma_i)  
  *Sources: R1*

## Outcomes, first applicable

- **[1a] NO_RUN**: Any identity or implementation gate fails (B0, B0prime_DRY, B0prime_RERUN, B0_FA, B0_RO1, B0_N3, B1/Z2, Z2_OFF_RO1, B2, B3; a B2/B3 failure is IMPLEMENTATION_DEFECT of the gate), or a gate record is defective, malformed or contradicts its data (RECORD_DEFECT). Next: fix and re-review. Every reading names every missing or invalid case and gate. An unregistered record reads NO_RUN (A67 order N1); a duplicate anywhere is a RECORD_DEFECT (A71).  
  *Sources: R1; A48 AMB-01; A48 AMB-02; A54 S4; A54 S5; A67 (order N1); A71*
- **[1b] INCOMPLETE**: Placed directly after NO_RUN. Any registered V007 case (T-runs, C5H, identity-gate runs) invalid or missing, including BRACKET_HULL_MISS, a missing receipt, a pass-row gap or row-ID defect, RB_FP with undefined kappa -> name each case and gate with its next step; no T-test is read. Subtypes: CASES_OR_RECORDS (tests unread) and UNRESOLVED (tests read: ADOPT_TAIL or FLAG_PENDING_RULING with a pending step; a NOT_UV/SRKD split that turns on a flag).  
  *Sources: A47 I1; A50 item 4; A50 item 5; A48 AMB-17; A48 AMB-26; A54 B4; A54 S9; A50 item 9*
- **[1c] NUMERICS_UNCERTIFIED / NON_LAPSE_TAIL_MATERIAL**: Same position. NUMERICS_UNCERTIFIED: EPS uncertified, DOUBLING fails, GQ fails or a GQ/EPS coverage shortfall. NON_LAPSE_TAIL_MATERIAL: LO fails (LO_NGC for NGC readings). Next: named successor. No T-test is read.  
  *Sources: R1; A48 AMB-03; A48 AMB-18; A50 item 8; A46 RA7*
- **[2] decided failure outcomes, in R1 order**: Read in this order: IMPLEMENTATION_DEFECT: T2 decidable and fails; stop, T1/T3 not read as physics (also a T2I failure: IMPLEMENTATION_DEFECT (T2I), A48 AMB-10) | SOURCE_RULE_MATERIAL: T2c fails; root ruling on the gas rule before adoption | KBIG_NOT_CONVERGED: T3 fails; T3prime: production 2P with {P, 4P} (= 256 with {128, 512} at P = 128); EPS/LO coverage >= sqrt2 * 4P (A56 N4; R1's "production K_big 64 under T3prime (32/64/128), EPS and LO to 128" is superseded) | BOUND_INSUFFICIENT: RB_FP or SRB_ROT fails; next: q-corrected shell (second asymptotic order), design successor | FLOOR_LIKE (D14): T1 fails only by a contraction clause (max-based or per-row, RA6) with Dhat_T(2,3) <= 1 and Dhat_T(3,4) <= 1; takes precedence over the two T1-fail readings below; a floor clause needs a new prereg version before any further case | NOT_UV_RESIDUAL: T1 fails AND T2c <= tau_i/4 every row AND SR-K pairwise K-dependence (2,3),(3,4) <= tau_i/4 AND no TAIL_SOURCE_UNDERCONVERGED flag; next: column/Picard map, own prereg | SOURCE_REPRESENTATION_K_DEPENDENT: T1 fails otherwise; next: fixed-point SR runs C2T-SR/C3T-SR/C4T-SR (packets over the smooth source), own design and prereg | HIGHER_K_DISAGREEMENT: T1 passes and T1_H fails; adopt nothing; C6T candidate under a V007 amendment sealed before further results | SHAPE_DISAGREEMENT: T1_S fails; review per-stage C wiring. A decided failure is read when its own condition is fully decided even if another step is unresolved; the pending steps are listed.  
  *Sources: R1; A50 (final order); A48 AMB-10; A48 AMB-17; A46 RA6; A55.1; A56 N4*
- **[3] UNDECIDABLE_ROUTE_A_TAIL**: Only if no decided failure outcome applies and some test with a TAIL_SOURCE_UNDERCONVERGED run failed (flags are evaluated per test: a flagged test that passes, passes with the flag carried; one that fails is undecidable and cannot trigger IMPLEMENTATION_DEFECT, NOT_UV_RESIDUAL, SOURCE_REPRESENTATION_K_DEPENDENT or FLOOR_LIKE). Next: rerun that case with seed source_rtol/10.  
  *Sources: R1; A48 AMB-04; A50 (final order)*
- **[4] UNDECIDABLE_AT_ITERATION_FLOOR**: A paired test still undecidable after R-PAIR: neither pass nor fail; no adoption. Both undecidable readings are listed when both apply. A C4T-KHI B4 gap whose Picard members reach the floor reads UNDECIDABLE_AT_ITERATION_FLOOR, PROVISIONAL; it is undecidable and adopts nothing (A67 NEW-31).  
  *Sources: R1; A50 (final order); A67 NEW-31*
- **[5] FLAG_PENDING_RULING**: Every gate and test passes but a flag stays unruled (SOURCE_QUADRATURE_MATERIAL, or TAIL_SOURCE_UNDERCONVERGED on an adoption run); no adoption; needs every step resolved; root rules on the flag (a flag ruling is a root addendum entry naming the flag, run and evidence, registered before any adoption reads the flagged test).  
  *Sources: R1; A48 AMB-04; A48 AMB-17; A48 AMB-19*
- **[6] ADOPT_TAIL**: The decision rule holds and every step is resolved.  
  *Sources: R1; A48 AMB-17*

**Reading rules:**

- Any reading made while a step at an earlier position is pending is marked PROVISIONAL, with the pending steps listed. A decided T3, T1-split or SHAPE reading stands while T2/T2I is pending, marked PROVISIONAL. *(A50 (final order); A50 item 3)*
- "No T-test is read" applies to NO_RUN, INCOMPLETE and NUMERICS_UNCERTIFIED/NON_LAPSE_TAIL_MATERIAL; T values may be reported descriptively, labelled "not read". *(A48 AMB-18)*
- Governing principle: no ruling may make adoption easier than the text; where the text is silent the stricter-on-adoption reading is chosen. *(A48; A53)*
- A V1-V6 failure other than BRACKET_HULL_MISS -> named defect, fix and rerun that case under V007 with thresholds unchanged. *(A48 AMB-16)*

## NGC3198 N-tests

- **state**: saved iteration-0 operator ngc_kgrid_fidelity_c2/phase23/ops/T120L_hovr (OPERATOR.json e6453d520f902e77da77e49b8f8d1cdbed84639f11ed6cc661943553741b2af4); replays only; no NGC prep successor needed
- **theta**: 3.3657664138980042e-09
- **azimuths**: 32
- **tail**: {"source_rule": "continuum_v001", "quadrature": {"K_inverse_kpc": [2], "outer": {"shape": "cylinder", "K_big_inverse_kpc": 16}, "order": 8, "w_perp_max_inverse_kpc": 0.005, "w_z_max_inverse_kpc": 0.007, "R_eval_max_kpc": 136.5, "R_src_max_kpc": 136.4847475059566, "z_eval_max_kpc": 105.0, "z_src_max_kpc": 95.0, "phase_perp_rad": 1.365, "phase_z_rad": 1.4, "N_perp": 25608, "N_z_plus": 18288, "M_s": 96}, "gas": {"M_s": 96}, "jet_order": 1, "roster": "stars + H2 registered (prep v001 L183-250 radial form, no GL4 tail normalization) + razor-thin initial gas (prep v001 L290-295); I1-T vs ops fixed_source_fourier_J / initial_gas_fourier_J", "stars": {"segment_rule": "max16_ceil_kdr_plus8", "tail_rule": "t_panels_40a_phase1p5_gl12"}}
- **K7_note**: deterministic single-operator reads, no iteration; tail quadrature noise certified <= theta/20 (NQ), so theta/4 is 5x the certified noise
- **sites**: {"NE1": "replay_c1 c4a8cd02 L79-93 metric_point (zero boundary L81-82, evaluate_line L86), L105-106 lnN -> TailCtx subclass (ngc_ring_tail_ctx_c2v001.py)", "NE2": "kg_lib_v001 06333714 L163-173 checker pins, L193-201 ctx_with -> ctx_with_tail (same new file)", "NE3": "ringeval_v001 5149ea29 L12 ZK, L23 ctx_with, L24 roster, L31 lnN -> ringeval_uvt_c2v001.py", "NE4": "dsplit_sphere_v001 a4390c6a L34, L46 (mask sphere_info_v001 4f616b14 L22) -> sphere_eval_uvt_c2v001.py", "NE5": "run_p23_v001 3578e83c L19 ALLOWED, L59-70 -> run_ntests_c2v001.py"}
- **tests**: {"NQ": "doubling (w/2, o+4): change of lnN0 and dL <= theta/20", "N0": "K_big = K: lnN at the 7 heights on all rings bitwise equal to phase23/out/rings/T120L_hovr/*.json", "N1": "S = max_phi lnN0 - min_phi lnN0 < theta on the 12 TRUNCATION_SHAPE rings (ordinals 1-8, 10, 13-15), C1 as written; C1prime still passes; all 100 reported", "N2": "sphere-masked T120L + sphere tail vs cube T120L + cube tail, per ring and azimuth, lnN0 and dL(+-10,+-20,+-30) <= theta/4", "N3": "N3' = K_big 16 and 64 against production 32, at every ring and azimuth: |Delta S| <= theta/4 and |Delta dL| <= theta/4 (A64.2; the R1 form 8/32 against 16 is superseded)", "N4": "e4 at +-95 kpc (A14.C5), cube+tail vs sphere+tail: reported"}
- **not_covered**: NGC route-A/route-B fixed points with the tail wait for a valid NGC route-A base (UNTESTED)
- **LO_NGC**: required before N-test readings (R1 L8; A52.4: readout-coupled share; NGC I1-T of stars + H2 against the T120L fixed source passes first)
- **outcomes**: N_NO_RUN (a record is defective or contradicts its data; name it), N_INCOMPLETE (a record missing, NGC I1-T not passed, or LO_NGC absent; name each), N_FAIL_<test>, N_PASS; N_PASS is only an input to NGC route A/B (0512; A54)
- **own_compare**: the N-tests get their own small compare before any N-test is read (A48 AMB-23); NGC tail route support is the driver successor v011 (0517), plan-identical to the sealed DDO driver
- **sources**: ["R1", "0512", "A54 (lanes)", "A52.4", "A48 AMB-23", "0517", "A62", "A64.1", "A64.2", "A64.3", "A66"]
- **production_K_big_A64**: NGC production K_big = 32, in force after the formal N3 at 16 failed (8-vs-16 dL 0.749 theta; A64.2). N3' = {16, 64} against 32; N1, N2, N4 and NQ are evaluated at 32; N1 is read only on the production-K_big records (A64.3). The R1 tail block above is the K_big 16 instance; its node counts are re-derived by the module rules at 32. EPS, LO_NGC and GQ_NGC coverage >= sqrt2 * 64 = 90.5 (to 91 /kpc).
- **C1_scope_A64**: C1' applies only on NOT_GRID rings (A17); C1 is kept on TRUNCATION_SHAPE and QUADRATURE_LIMITED rings (A64.1).
- **N1_consequence_A66**: Ruled after the N1 diagnostic was seen and labelled so (A66): the N-test reading is decided by the compare as registered; N_FAIL_N1 is never relabelled a pass. N_FAIL_N1 confined to TRUNCATION_SHAPE rings does not block NGC route A/B; every NGC row within the radial support of a failing TRUNCATION_SHAPE ring is flagged TRUNCATION_SHAPE_RESIDUAL in the freeze manifest (disclosure, not INVALID, with the measured S/theta). A failure of N0, NQ, N2 or N3', or an N1 failure on a ring that is not TRUNCATION_SHAPE, blocks NGC route A/B.
- **NQ_note_A62**: NQ's exact zero is genuine: the lnN resolution is one N step, about 3.3e-8 theta (A62, Claude4 0065).
## Run list

- **DDO_gates**: Z2 (2d5e79d0), Z2_OFF_RO1 (894e5b3a), B0prime_RERUN (4ac5527a): the r5 identity reruns launched at 14:56Z (monitor ba031c23; wall 43,200 s, RSS 16 GiB, output 32 GiB; no retries; detached), compared by the identity-comparator slot; if A72 adopts r6 they are rerun on r6 with caching enabled where the tail is ON and the r5 runs are superseded and kept.  
  *Sources: A52.1; A55.3; A47 I6; A67; A72.3; A74*
- **DDO_tests**: C2T, C3T, C4T, C6T, S4T, C4T-D5, C4T-C5c, C4T-KLO (K_big 64), C4T-KHI (K_big 256), C4T-A: the ten filled P128/M_s 128 specs (binding_inputs.spec_set), launched by root from the bound plan (launch-packet slot), all on the driver slot and, under r6, all with the cache.  
  *Sources: A46 RA11; A55.1; 0530 item 1; A56 (labels); A57.1; A70; A72.3; A78; 0576*
- **external**: C5H (spec 60b46130; driver 999331af; REVIEW_V009 original 3bce7c02; admitted on the three A50 grounds: REVIEW_V009 PASS for driver 999331af and spec 09ff5a96, a byte diff of 60b46130 against 09ff5a96 limited to the label and fs_absolute_overrides, and the clean dry run). Read before the seal only as validity/admissibility booleans and reason codes, no row value printed or written.  
  *Sources: A46 RA11; A48 AMB-20; A50 (AMB-20 restated); A53 (REVIEW_V009); A47 I3*
- **contingent**: R-PAIR members (<= 4 pairs), with specs registered before any T result (A52.3); the PICARD member specs are successors per A53, with B0 evidence (gates_v004, PENDING): admit the base route A, column_workers 1, V6 result_sha equality, an RO1 record equal to the base's, and for the C5H PICARD member no ro1_workers. gates_v004: the R-PAIR member specs PASS (18/18 leaves; the C5H ROUTE_A B0 holds; 10/10 negative controls); PICARD members are fillable only after their bases run (A68).  
  *Sources: R1; A52.3; A53; A57.2; compare r5 NEW-20; A68*
- **replays**: B2, B3, EPS, LO, GQ, SR_K, shell_split, DOUBLING, T2I, B0_RO1 replay (RA5 b), EA replay record (AMB-08/22), MT record. DOUBLING merged record (A73); EA, MT, I1T, T2I, SRB_ROT, RB_FP, FLAG_RULINGS and HARMONICS records are produced after the seal from run outputs and verified by producer pin (A79 NEW-61).  
  *Sources: R1; A46 RA11; A48 AMB-08; A73; A79 NEW-61*
- **NGC**: NQ, N0, N1, N2, N3' (16, 64 vs 32), N4 at NGC production K_big 32; LO_NGC, EPS and GQ_NGC to 91; NGC I1-T.  
  *Sources: R1; A52.4; A64.2*
- **limits**: Resources are root's launch decision. Route-A admission is ramp-gated: KHI starts immediately; each later case starts only after the previous case logs its first completed route-A iteration and free memory is >= 25% with fewer than 6 cases in route A; route B overlaps freely; every decision is logged (A72, 0559). RSS caps >= 1.5x the modelled peak; monitors and the launcher run detached (A61). One case failing does not cancel the others; new starts halt only on systemic failures (RSS cap or memory kill, disk guard, a refusal that would repeat for every case) or a predecessor that ends without a completed iteration (A62, 0559). The root admission config names the BUILD_V005 launcher and guard sources exactly (A78 N2). The module memory cap is a resource guard (8 GiB in r5).  
  *Sources: A47 I4; A55.2; 0527; A61; A62; A72 (ITEM3-R1); 0559; A78 N2*
- **cpu_hours_estimate_UNTESTED**: Restated from the measured-timing cost model in Codex1's launch packet (plan V010, UNTESTED): solo route-A+B hours per case from 5.0 (C4T-KLO, C4T-C5c) to 27.8 (C4T-KHI), 104.4 solo hours in total; wall caps about 2x solo (KHI 56 h). Co-load may lengthen execution; elapsed time is unbounded under the memory gate. UNTESTED.  
  *Sources: R1; A54 (Codex2 Lane A); A55; A58 RI-09; A61*

## Seal record requirements

- Before the seal the compare's gate and admissibility functions run on the real input records (the C5H receipt and result if present, the identity-gate records and the RO1 replay); their output goes into the seal record (E-SEAL1). *(A46 RA13)*
- Blinding: on C5H the gate functions run only as validity/admissibility booleans and reason codes, with no row value printed or written; the seal record states that no row value was shown. Record-controlled labels are redacted in blinded modes. *(A47 I3; A54 S6)*
- The compare pins at seal: V007_PREREG_SHA256 (this text once sealed), PIN_ADDENDUM_V005 (frozen V005 sha), PIN_REVIEW_V009 = the preserved original 3bce7c02, PRODUCTION_K_BIG_A55 = 128.0; its custody pins (PIN_RO1_CUSTODY, PIN_RO1_NODES_CUSTODY, the drivers_allowed I4 set) move to r5's re-pinned shas read from r5's BUILD record, verified from bytes. *(0526; A53 (REVIEW_V009); A55; A56 (A55 follow-ups 1, 3); compare r5 NEW-26)*
- Key-equivalence map: every key v010 adds that differs from v009 numerics appears with its absent/default value and B0 evidence. *(A48 AMB-13)*
- Publication order (0561, FORMAT_V004, RUNBOOK_V005): root first freezes the V005 addendum (exclusive create) and binds the plan with the build-only binder; then exclusively creates the SEAL_RECORD, which names the prereg sha (this text, the first pin), the compare, the driver and the frozen-addendum pins; then the ROOT_SEAL_ADMISSION config pinning the SEAL_RECORD's full sha; then a separate SEAL_ADMISSION_RECEIPT naming both, posted in a numbered root packet. No file is edited after it is created; the config sha is therefore not inside the SEAL_RECORD (see ROOT_ITEMS_R3 RI-19 on A72 H-01's wording). *(0561; 0576; A72 (H-01); A78; 0580)*
- The seal record quotes the final compare IMPL's list of every compare-lane NEW item with its disposition: adopted as text if stricter on adoption and gap-filling, rejected if looser (A58 RI-10). *(A58 RI-10)*
- The raw successor-custody check of the Z2 run is recorded (A59). *(A59)*
- Disclosure E5-08: C5R3 ran the C5H driver and spec except for the label and fs overrides, so the C5R3 route-A fixtures the producers were tested on are very likely equal to C5H's route-A values, E^A included; they are not row values, and A47 I3 holds. *(A62 (E5-08))*
- Seal-time pins in the compare: PIN_ADDENDUM_V005 (the frozen copy), PIN_V010_R5_CHECK (or the r6 equivalent under A72), PIN_PRODUCER_REGISTRY; the custody pins follow the A77.2 role table read from the driver slot. *(A67 (seal-time pins); A72; A77.2)*
- CASCADE_MAP_R5_ADDENDUM (the immutable inventory addendum naming the unreachable pin-only successor) exists before the seal if the driver slot is r5. *(A69)*
- The root admission config names the BUILD_V005 launcher and guard sources exactly (the build check is a substring match). *(A78 N2)*

## Scope UNTESTED

- S1 transfer across parameter space (V005 S1) unchanged
- NGC fixed points with the tail
- outer-panel part of the kept-grid quadrature g_K (V005 S3)
- RB-FP first-order assumption
- all costs and memory
- NGC result assembly under v010 (L3)
- NGC lapse-only omission on (2,16] until LO_NGC (L8)
- sphere-C tail cost and memory at production domains (IA3)
- P128 cost and memory (route-A tail build 15.1 min/call at 128; K_big 256 build ~0.877 GiB)
- GQ for C4T-KHI at M_s 64 (TESTED-NEGATIVE in certificates_v002; superseded by production M_s 128, A57/A68)
- cost figures restated from the launch packet cost model (A58 RI-09): UNTESTED
- float-floor note (A67): deciding test the late-pass increments of the first real 12-pass member
- the A72 cache saving, until kbig_timing_v003 reports (condition (c))

## Not V007 text

- A60 (NGC gap rows, cut binding, fe5a2f06, miss-reading prereg), A61 calibration F1-F4, A63 and A65 (stage-0 grid; STAGE0_GRID_OUTER), A66 freeze-manifest flag, the NGC launch-path wrappers and registries (A74 cx3r005, A77 cx3r006, A80 cx3r007; launch registry cx3r006 3c42ca07, retired 47023c27 and c5abc2d5) and the calibration orchestrator items are registered in the NGC freeze, the miss-reading prereg or the calibration lane, not in this text; only their V007-facing parts (A64 coverage, A66 N-test consequence, A80's compare items) are integrated here. *(A60; A61; A63; A65; A66; A74; A77; A80; 0580)*

## Root items

See `ROOT_ITEMS_R3.md`. OPEN: RI-19, RI-20, RI-21, RI-22, RI-23, RI-24, RI-25, RI-26.

