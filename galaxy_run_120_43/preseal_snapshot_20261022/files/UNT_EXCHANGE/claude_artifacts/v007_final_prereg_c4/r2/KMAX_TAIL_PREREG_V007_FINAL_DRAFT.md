# KMAX_TAIL_PREREG_V007 — final draft (UNSEALED)

FINAL DRAFT r2 (NOT SEALED). Assembled by Claude4 (dispatch 0526) from R1 c691cab6, integrating V004 A46 RA1-RA13 (frozen 487d4449) and V005 A47-A57 (open; observed sha 78b8e4da963f0370bd7840c5b5f008955a6e6171c5bec99f90984ddeb7943d02 at assembly; PENDING freeze sha). Written before any V007 (tail-corrected) result exists; nothing was launched; C5H, UVT_* and targets were not read. Root seals; the open items are in root_items. Revision r2 integrates A56 and A57 (r1 = c4v001 output, kept).

**Assembly:** Claude4, single author, UTC 2026-10-18T13:06:01Z. Base: R1 `c691cab6dd9752a7bd98025cf7357a5c729b3fef90a78a6277195c5520671e33`. Dispatch 0526 `8bda9cd107f43c518a95209112b1fa9a6659701155d810704d63e48aee575ec4`. V005 addendum observed `78b8e4da963f0370bd7840c5b5f008955a6e6171c5bec99f90984ddeb7943d02` (open).

## Binding inputs (sha256 from bytes at assembly)

- **driver** — galaxy_m0_forward_c2v010 **r5** (A55.2: r4 with only the TAIL_MEMORY_CAP_BYTES module successor and the pin-only re-pin cascade; "the sealed driver is the one the gates ran on", A55.3). sha PENDING_FROM_BYTES at seal (tail_scheme_impl_c2/driver_r5/, not yet on disk at assembly). Base = v010 r4 below (0526 lists r4; see ROOT_ITEMS RI-01).  
  *Sources: A55.2; A55.3; 0530 item 2; 0526*
- **driver_r4_base** — `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py` (`b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b`)
- **driver_r4_build_record** — `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/BUILD_DRIVER_C2V010_R4.json` (`c081d3b209cbf3f5e0aea19e50eecc53ab60a42dc57079b4b518e663e88de9f0`)
- **driver_r4_hashes** — `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/HASHES.txt` (`0fd522946b2775bdf358ca8f8f5ac20272b4765e58b177898f849d5e75c70781`)
- **successors** — Every route-A and route-B successor, worker, facade, controller, binding and the reference successor exactly as pinned by the sealed driver's build record (r5, PENDING; the r4 set is pinned by BUILD_DRIVER_C2V010_R4 above). Reference successor under r4: driver_r4/route_b/…_uvt_c2v003.py (4778fc73).  
  *Sources: A52; A55.2; 0526*
- **reference_successor_r4** — `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/route_b/ddo_homotopy_reference_root_worker_v001_gal_c2v005_uvt_c2v003.py` (`4778fc73d52973da7ab2c07bcbcfc9d0f502277fe34b5a42440962593f648c56`)
- **tail_module:**
  - **lapse** — `owned_uv_tail_lapse_v001.py` (`c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22`)
  - **roster** — `uv_tail_source_roster_c2v001.py` (`4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2`)
  - **jn** — `posix_libm_bessel_jn_provider_c2v001.py` (`d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171`)
  - **successor_note** — A55.2: a module successor changing only TAIL_MEMORY_CAP_BYTES (to 8 GiB), AST-identical otherwise, replaces lapse c28d4209 in r5 (PENDING).
- **ro1_c2v002:**
  - **ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py** — `ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py` (`86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885`)
  - **ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_c2v002.py** — `ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_c2v002.py` (`9f74d4652dbbc237f2d38951440a9a95875251fb2cd286499b404a0cf35a8ad1`)
  - **ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_c2v002.py** — `ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_c2v002.py` (`d676ecb2c05e8017a4ffbde74a01e7a7ec1a4290149baa6cbfe62435bb573d97`)
  - **ngc_composite_full_coupled_binding_v002_uvtail_ro1_c2v002.py** — `ngc_composite_full_coupled_binding_v002_uvtail_ro1_c2v002.py` (`52dc4065da6b0307d1a37bb63bf22921edd08709a763b0ed5a114e8c2b0f2226`)
  - **ngc43_composite_coupled_root_worker_v002_uvtail_ro1_c2v002.py** — `ngc43_composite_coupled_root_worker_v002_uvtail_ro1_c2v002.py` (`6559ff6a364adbd5d23c04378b74e8fb6adfb8681b52f20451bc8582dce3a593`)
  - **ngc43_composite_coupled_root_worker_v002_parallel_uvtail_ro1_c2v002.py** — `ngc43_composite_coupled_root_worker_v002_parallel_uvtail_ro1_c2v002.py` (`4065fe58e9f5c6734c15ab193de95c69392d477eff8d26c0e6254d49483f2292`)
- **nodes_v001:**
  - **lib** — `owned_uv_tail_nodes_v001.py` (`c8a04fb55f6c388c7cc5b735cb0e19222836c49acfce46d846198951593be551`)
  - **ro1_worker_serial** — `ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_nodes_c2v001.py` (`dbb331db412027e3499e1700e1df8dac90b30fcd9216951ced0fbbccd6df1457`)
  - **ro1_worker_parallel** — `ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_nodes_c2v001.py` (`5a4c7d41c5a02d2ed0af74e09b4d3b8e726eab7484069dbb459474d1f8cbc177`)
  - **scope** — nodes RO1 workers and binding 86af6198 on the custody list only for cases whose registered source_rule is nodes_v001 (A53 NEW-13)
- **spec_registry** — The P128 spec set (0530 item 1; A55.1), PENDING: the r4-era registry SPECS_V007_C2V002_R1 (9bfe9674, pinned below) predates P = 128 and is not the sealed registry. The sealed registry is retargeted to r5 (0530 item 2).  
  *Sources: A55.1; 0530; 0526*
- **spec_registry_r4_era** — `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/specs/SPECS_V007_C2V002_R1.json` (`9bfe96741a8aa86a8956f67fab9ebcb62548f228aaaf54dd6c1633754d26e69f`)
- **certificates_v002:**
  - **index** — `CERTIFICATES_V002.json` (`29ee13be86b7a4f18f442b4fb9fa87ee408d6dbee1308190fb66317c2b4ee7e5`)
  - **hashes** — `HASHES.txt` (`5835049b9fdd8877ac0a624b8a554bccd51f07d17faf4a846cfc5e3a5ec90228`)
  - **eps** — `EPS_CERT_V006.json` (`598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192`)
  - **lo** — `LO_CERT_V002.json` (`fd4fa52b76e10ee987461e77c23b1e5dd7f7df800d453a8409a86bd0868e67b4`)
  - **lo_ngc** — `LO_NGC_CERT_V002.json` (`33bc21905045431ca877ea26d5c9edf07fd3d7c9e33409cf9e24752da039c724`)
  - **i1t_ngc** — `I1T_NGC_T120L_V001.json` (`3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6`)
  - **gq_kb128_ms64** — `GQ_CERT_V003_KB128.json` (`24984fd558dadaba1491753871366df6aab334ff5f37dd3f1744cf54abc75727`)
  - **gq_full_ms64_FAIL** — `GQ_CERT_V002.json` (`fac4aca74244dc46c3699ce6502fc365a4bfe2535c4ded3a8de396186ab4d44c`)
  - **gq_kb256_ms128_not_registered** — `GQ_CERT_V003_KB256_MS128.json` (`b3a5390f83f9cdd23667290ed942138a56396afcf27bdec05ca3fab5ae99e5c5`)
  - **note** — EPS (EPS_CERT_V006) does not depend on the gas rule and stays. GQ and LO for the DDO cases move to certificates_v003 (GQ and LO at M_s 128; PENDING, A57.1): GQ over the full DDO reach on all nodes; LO recomputed with the M_s 128 source (the M_s 64 transfer is UNTESTED and not relied on). The v002 GQ/LO records above are evidence only.
- **certificates_v003** — tail_scheme_impl_c2/certificates_v003/ (GQ + LO at M_s 128): PENDING_FROM_BYTES at seal.  
  *Sources: A57.1; 0532*
- **identity_comparator** — c2v004 (gates_v004, PENDING_FROM_BYTES): closes the c2v003 holes (extra files fail; .npy compared; request argv compared; script-custody tokens limited to the declared driver map; strict JSON type and signed zero). The r5 identity comparisons use c2v004.  
  *Sources: A57.3; A52.2*
- **identity_comparator_c2v003_predecessor** — `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v003/run_identity_compare_c2v003.py` (`8f14f466113d07b67c419c7a3b8b6c20a25193d467816d06471b709b4849f04f`)
- **c5h_spec** — `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c5h_hull_c2/CALL_KMAX_C5H_A2F10_HULL_N8_M32_C2V009.json` (`60b4613080055aedd92dbb649cdfa45675f64a4d133c7ba3e4fbb15b59c7704e`)
- **review_v009_orig** — `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/check/REVIEW_V009_PREP_V009_V001_ORIG_3bce7c02.json` (`3bce7c02926526edf2a594418097ff379604ee1c9760dc1145bcd37ed2882d9f`)
- **identity_specs:**
  - **Z2** — `CALL_UVT_Z2_A2F10_EMPTY_DOMAIN_N8_C2V010.json` (`2d5e79d05bf7d7c517a487e2603a09a14bb3e76979474ab25a717e2a5c656229`)
  - **Z2_OFF_RO1** — `CALL_UVT_Z2_OFF_RO1_A2F10_N8_C2V010R4.json` (`894e5b3ab67d58cd9304aab428923cf4bdfa968cd1dd3518ebc10edba572a39c`)
  - **B0prime_RERUN** — `CALL_REPRO_PINNED_ADMIT_PREFIX_C2V005.json` (`4ac5527ad1731353d798c2648adc1033335a12102ec071b3ae6a619334313cb7`)
- **qinf_evaluator** — `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/qinf_dependence_c2/tools/qinf_eval_v001.py` (`f58de0dcc67cc4097b4604dc96b640fbf8aaee0520d0478e214673b931eb3346`)
- **v006_r1_sealed** — `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/v006_r1/prereg/KMAX_MATRIX_PREREG_V006_R1.json` (`807fc5bfcb24ee779137746db3536f41dd97c16bd5f367f79ad5a1b8c3ec067c`)
- **compare** — kmax_tail_compare_c2v007 at the round sealed by root: PENDING r5-final sha, filled at seal (r5 78ac63b7 is FAIL as a seal candidate per A54 continued (CX2-R5-B1); S9 goes into the next round).  
  *Sources: 0526; A54 S9*
- **compare_r5_current** — `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r5/kmax_tail_compare_c2v007_r5.py` (`78ac63b7a52a8746e96f390d0d5b46de4aa7ce5eaa27def6e54ef27330ce9755`)
- **gate_b3_final** — `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b3_c4/GATE_B3_C4_V002.md` (`465cb3c3b105c8bea994259bcf347e86910e8a9ebbc502ba83ff617fa83ceacf`)

## Fixed across all cases

- **anchor** — A2F10, the DDO154 seed of V005; coefficients 2e3a36d8 (V005 anchor block)  
  *Sources: R1*
- **grids** — G2/G3/G4 as V005; G5 (C5H, 108 nodes/axis, kmax 5) for the T2/T2I extension G5\G4; G6 as V006 R1 (120 nodes/axis, prep v009) for C6T.  
  *Sources: R1; A46 RA1; A46 RA3; A46 RA11*
- **tau_km_s** — [0.4, 0.2, 0.175, 0.125, 0.1, 0.05, 0.05, 0.05, 0.075, 0.15, 0.175, 0.325]  
  *Sources: R1*
- **statistic** — V005 criterion.statistic (Dhat)  
  *Sources: R1*
- **validity_gates** — V005 per_case_validity_gates V1-V6. V3 against the registered V007 case block, including the uv_tail config sha and the declared key-equivalence map (any key v010 adds must appear in the map with its absent/default value shown to reproduce v009 behaviour, B0 identity; otherwise V3 fails). The case block asserts each case's registered tail content: source_rule, grid (kept K), outer shape and K_out/K_big, lapse_only, enabled, lambda_scale and the uv_tail config sha; a swapped tail, wrong grid, wrong K_out or wrong K_big is refused (S8). Every pass row-set and the final row-set carry exactly the 12 registered row IDs (no duplicate, no unknown ID), checked before any dictionary is built; a violation is a RECORD_DEFECT and the case reads INCOMPLETE (S9). A pass recorded without rows is a record gap: pass_rows equal passes in number with consecutive indices, otherwise E is unavailable and the case reads INCOMPLETE if no R-PAIR resolves it (B4).  
  *Sources: R1; A48 AMB-13; A54 S8; A54 S9; A54 B4*
- **picard_validity_gate_km_s** — 0.0125  
  *Sources: R1*
- **brackets** — Every V007 tail-corrected case uses C5H's bracket block byte for byte: fs_absolute_overrides [1.5125e8, 3.17625e8] on all 72 columns, le_first [0.4, 0.9], le_next [0.8, 1.1], rfs [0.8, 1.2], rfs override 71: [0.8, 1.01]. Cases: C2T, C3T, C4T, C6T, S4T, C4T-D5, C4T-C5c, C4T-KLO, C4T-KHI, C4T-A (RA4 list with the A56 T3 labels in place of C4T-K16/C4T-K64; RI-05). No W1 widening clause. A miss under the hull makes the case invalid, reading BRACKET_HULL_MISS; next step: its own registration. The identity gates (Z2, Z2_OFF_RO1, B0prime_RERUN) keep their reference specs' brackets, which bitwise identity requires.  
  *Sources: A46 RA4; A48 AMB-16; A55.1; A56 (labels)*
- **route_a** — Route A is computed in every T-run (PICARD R-PAIR members instead admit their base run's route A) with column_workers 8 (parallel), uniformly across T-cases; route_a.max_iterations = 32 for every T-case, matching C5H and C4T-D5; each case's accepted iteration is reported. Every V007 tail-corrected case uses the RO1 workers from its first launch (RO1 changes checkpoint identity); C5H (v009-EXT, no RO1) is the declared exception admitted under A48 AMB-20 / A50. Admission of a route A or prefix with a different uv_tail digest is refused (UVT_ADMISSION_MISMATCH). The I4 condition (V8c-F1 fix; tail-ON serial == parallel bitwise) was met by the final implementation check (A51), so no column_workers exemption is declared.  
  *Sources: R1; A47 I4; A47 I5; A49.4; A51*
- **production_tail:**
  - **P** — Production K_big P = 128 /kpc (cylinder). Production C4T and every tail-corrected case not otherwise specified use cylinder K_big = 128 (C4T-C5c: cube K_out 5, RA2; T3 cases C4T-KLO K_big 64 and C4T-KHI K_big 256; S4T: its registered sphere tail; RI-05).  
    *Sources: A55.1; A54 (generic T3); A46 RA2; A56 (labels)*
  - **source_rule** — continuum_v001 (C4T-D5: nodes_v001 on G5\G4, RA1)  
    *Sources: R1; A46 RA1*
  - **gas** — interp lagrange3_s_gl4 with **M_s = 128 for every DDO tail-corrected case** (registered change, made openly before any T result: at M_s 64 the GQ gate fails at the reach P = 128 needs); NGC keeps M_s 96 (its GQ passes to 32).  
    *Sources: R1; A46 RA7; A57.1; 0532*
  - **quadrature** — order 8; w_perp_max 0.05 /kpc; w_z_max 0.02 /kpc; phases 1.415 / 1.34 rad; corner_zone_rule as R1 (IA1). Node counts (N_perp per K from the module grid; N_z_plus) and the eval/source extents at K_big 128 and 256 are those of the registered P128 uv_tail configs whose shas the case block carries (S8). R1's N_z_plus 12800 and extents were set for K_big 32 (RI-03).  
    *Sources: R1; A54 S8; A55.1*
  - **asymptote** — EH_exact_minus_quarter  
    *Sources: R1*
  - **lapse_only** — true (non-lapse components bounded by LO / LO_NGC)  
    *Sources: R1*
  - **jet_order** — {"route_a": 1, "route_b": 2}  
    *Sources: R1*
  - **stars** — {"segment_rule": "max16_ceil_kdr_plus8", "tail_rule": "t_panels_40a_phase1p5_gl12"}  
    *Sources: R1*
  - **memory_guard** — TAIL_MEMORY_CAP_BYTES is a resource guard, not numerics (design K15); r5 raises it to 8 GiB through a module successor that is AST-identical otherwise.  
    *Sources: A55.2; 0513*
- **kept_region_rule** — route A, reference, body: cube K; offset t[delta]: stage mask (N1); route-B columns/rotations: stage mask  
  *Sources: R1*

## Pairing and decidability

- **noise_allowance** — Norm in which contraction is measured: ||d_k||_tau = max_i |d_k,i|/tau_i. q = min(0.9, the larger of the last two observed ratios ||d_k||_tau/||d_k-1||_tau); with only one ratio, that ratio. Norm-level bound E_i^norm = tau_i * ||d_last||_tau * q/(1-q); with exactly one increment, E_i = tau_i * ||d_last||_tau. Per-row bound for rows whose last two increments have the same sign (d_last,i * d_prev,i > 0): |d_last,i| * q_i/(1-q_i), q_i = min(0.9, |d_last,i|/|d_prev,i|) (S7). Alternating bound for rows whose last two increments change sign: the tail of a geometric series with ratio -q_i, |d_last,i| * q_i/(1+q_i), q_i = |d_last,i|/|d_prev,i| (A56 N1). E_i = max(E_i^norm, same-sign bound, alternating bound). E is UNAVAILABLE for the run (its tests undecidable; to R-PAIR) when: no increment is observed; a tau-norm ratio >= 1 on either of the last two ratios (NEW-7); any row has q_i >= 1, same-sign or alternating (A56 N1); or a pass-row gap / row-ID defect exists (B4, S9). (The 0.9 cap on same-sign q_i: RI-18.) E_i(pair) = E_i(a) + E_i(b). The geometric bound assumes the observed ratio is the map's contraction factor: DECLARED, checked against each run's own increments.  
  *Sources: A51 F2; A54 S7; A56 N1; A53 NEW-7; A48 AMB-05; A54 B4; A54 S9*
- **decidable_iff** — E_i(pair) + E^A_i(pair) <= tau_i/8 on every row  
  *Sources: R1*
- **decidability_scope** — Decidability applies to T1_H, T2 and T3 (pass texts say "decidable"); not to T1, T2c, T1_S or RB_FP.  
  *Sources: A48 AMB-06*
- **if_not_decidable_R_PAIR** — R-PAIR once, branch chosen on the worst undecidable row (largest (E + E^A)/tau): if E is unavailable, branch PICARD; else if E^A_i(pair) > E_i(pair) on that row, branch ROUTE_A, otherwise PICARD. ROUTE_A members recompute route A with route_a.seed_source_rtol_factor 0.1 (absent = 1.0, byte-identical; B0 covers absence); their route-A identity must differ from the base's (NEW-16); the C5H ROUTE_A member carries ro1_workers true. PICARD members admit their base run's route A (route_a.column_workers = 1 is a registered PICARD leaf, byte-equal between members), with picard.passes 12 and speed_change_bound_km_s 0.0025 (byte-equal between members); V6 requires route_a_outcome.result_sha256 equal to the base's; a T-case PICARD member's RO1 record equals its base's canonically and its worker-kind check uses the admitted attempt's worker (R3-4); the C5H PICARD member carries no ro1_workers and reads ro1 armed false, fired false. Each member is validated against its partner and against its base, with only the registered R-PAIR leaves allowed to differ; a member's V2 uses its registered speed bound. C5H members run under v010 tail OFF with the RO1 workers where their branch computes route A, admitted through B0 identity, with worker/binding pins on the declared custody list. A manifest naming R-PAIR members for a test whose R-PAIR was not triggered is refused at load, before any test is read (NEW-17). PICARD members inherit their base run's flag and a cleared base clears them; ROUTE_A members carry their own flags. Still not decidable -> UNDECIDABLE_AT_ITERATION_FLOOR (reported; the test neither passes nor fails).  
  *Sources: R1; A48 AMB-07; A48 AMB-14; A50 B1; A50 N4; A50 item 1; A50 item 10; A50 item 11; A52.3; A53 (R-PAIR, NEW-16, NEW-17); A53 R3-4*
- **thresholds_unchanged** — test thresholds are never widened by E_i; E_i only decides decidability (thresholds separated from the Picard gate, CHECK K7)  
  *Sources: R1; A51*
- **T2_numerics** — C4T-D5 numerics are byte-equal (canonical JSON) to the numerics of the C5H spec 60b46130 after removing composite_grid_spec and uv_tail, and apart from the keys of the declared key-equivalence map in the seal record. The C5H run's normalized numerics must equal the spec's, normalized by its dry run. No column_workers difference is declared (A47 I4; both register route_a.column_workers 8).  
  *Sources: A46 RA1; A47 I4; A48 AMB-13; A50 S1; A47 I2*
- **route_a_noise** — E^A_i(run) = the per-row static rotation-channel effect, in km/s, of the last accepted route-A update: max over the 8 column azimuths of R_i c^2 |d_R packet_K[updated_acc - gas_acc](R_i, phi_j, 0)| / (2 v_i^ref) (the per-row form of M_K at the accepted iteration); E^A_i(pair) = E^A_i(a) + E^A_i(b). C5H's E^A comes from a required EA replay record computed after the seal from C5H's route-A outputs by this formula; the EA record carries the row radii so the row order is verified (or v010 copies probe_R_m into the tail record); the EA record covers C4T, C6T, C4T-D5, C4T-KLO, C4T-KHI and C5H.  
  *Sources: R1; A48 AMB-08; A48 AMB-22; A50 item 13*
- **diagnostics_recorded** — Route-A accepted iteration and Picard pass count of each member and case: recorded, not compared.  
  *Sources: R1; A48 AMB-21; A47 I5*
- **T1_status** — T1 is not subject to the decidability rule: its Dhat pairs follow V005 exactly as sealed; RA6 adds the per-row clause.  
  *Sources: R1; A48 AMB-06; A46 RA6*

## Gates before any T result

- **B0** — planning identity: v010 tail-OFF dry-run requests/inputs/normalized specs byte-identical to v009-EXT after the declared GEO substitution map, and to v009-GEO after the declared EXT map (EXT spec set incl. V005/V006 R1/G5/G6; GEO set incl. 2029f26a, 4ac5527a, A2F10, A2F10_RA8; NGC templates). Counting rule: B0 counts only comparisons whose expected reports are non-empty and whose planning completes; equal early failures are listed separately as no evidence (B0-EMPTY). The six historical positive R3 specs (C2R3, C3R3, C4R3, S4R3, RR3, Y3R3) refuse identically in both drivers (seed/admission custody) and are listed as no evidence, neither a blocker nor a pass; B0 coverage = the completed non-empty comparisons plus separately labelled computed-plan derivatives. The successor B0 tool and a B0 record rerun are required before the seal. Under A55, B0 also shows r5 plan-identical to r4 on every spec (with the B0-EMPTY rule). Each A52.3 C5H R-PAIR member's own spec sha is listed in spec_sets/EXT with its projection to v009-EXT form and its declared differences as evidence.  
  *Sources: R1; A54 (B0-EMPTY); 0530 item 3; A55.2; A53 (r4 validity F1)*
- **B0prime_DRY** — v010 tail OFF and each parent in dry-run on the B0 spec sets: DRYRUN_REPORT.json and DRYRUN_PLAN.txt identical under the declared substitution maps (gal_c2v005 CHECK CMP_DRY method, incl. the ngc_route_b_table needle lines)  
  *Sources: R1*
- **B0prime_RERUN** — prefix-admitted rerun of spec 4ac5527a under v010 tail OFF: result equal to v009-GEO deciding (i) except declared custody fields; declared exceptions: (i) every string value beginning with the run outdir path, compared after substituting that prefix (e.g. stage_records[].stage_dir, passes[].rotation_arrays.path, identity.route_a.checkpoint); (ii) elapsed_seconds at top level and in stage_records[]; (iii) the driver-custody field list. Its route A is admitted from a saved run, so RO1 cannot be armed: it requires ro1 armed false and fired false (exempt from A50 item 12). Rerun on v010 r5.  
  *Sources: R1; A52.1; A55.3*
- **B0_FA** — R-A F-A cases A1/A2/A4 end REFUSED (ROUTE_A_CHECKPOINT_MISSING) under v010; default path identity unchanged  
  *Sources: R1*
- **B0_RO1** — (a) RO1 fires in no identity-gate run; if it fires, that identity gate fails (RO1_FIRED_IN_IDENTITY_RUN). (b) A replay on the C6 iteration-8 checkpoint records ROUTE_A_READOUT_NO_CIRCULAR_BRANCH at query 03 and hands the checkpoint to route B. (c) Every other exception, and a refusal before convergence, still fails the call. RO1 set = {NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH, DEGENERATE_RADIAL_EULER, NON_TIMELIKE_COLUMN}, exact messages (incl. the full L205 string "DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed"), type(exc) is ValueError, only after a converged solve. A case that requires RO1 requires route_a_outcome.ro1.armed true. RO1 firing in a T-run is recorded, not an invalidity; route-A circular-trial rows are diagnostics only; route B decides.  
  *Sources: A46 RA5; A49.1; A49.2; A50 (A49 in the compare); A53 r4 validity F3*
- **B0_N3** — In tail-OFF mode v010 constructs no TailBoundary; the final checker verifies statically that every TailBoundary construction is guarded by an enabled uv_tail block; B0prime_RERUN and Z2_OFF_RO1 bitwise identity are the runtime check.  
  *Sources: A46 RA8; A47 I6; A52.1*
- **B1_Z2** — Z2 = spec 2d5e79d0 (A2F10 C2, v010 tail ON, cylinder K_big = K = 2, every stage domain empty), route A as registered in that spec (route_a.column_workers 8), RO1 workers armed (ro1.armed true, fired false), against DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001 (883b37a0; COMPARE_DECIDING_II e1d3c072): all route-A blobs/records/arrays, every stage npz, rows and speeds equal; only the declared custody list differs. The base -> successor token map is derived from the sealed driver's pin tables only (UVT stage table and STAGE_SUCCESSOR base map), never from the observed diff (the token fix: 16 exact additions for 8 driver-declared successor relations, PASS by Codex3, A57); Z2 is rerun on v010 r5 with independent verification and compared with c2v004. Precondition L as R1.  
  *Sources: R1; A50 item 12; A52.1; A55.3; A54 pre-seal status (Z2 ruling); A57; A57.3*
- **Z2_OFF_RO1** — Mandatory (no longer a fallback): spec 894e5b3a = the 883b37a0 reference spec under v010 tail OFF with the RO1 workers armed; comparator c2v003 gate (c2v004 for the r5 runs, A57.3) with tail-OFF semantics: admits only the declared enabled:false records, fails any other uv_tail record, requires ro1 armed true and fired false. Rerun on v010 r5.  
  *Sources: A47 I6; A52.1; A52.2; A55.3; A57.3*
- **B2** — static rows on saved C2R3/C3R3/C4R3 le3 (rotation_v005 uvt successor + unchanged column mean; continuum_v001, O = cube 12) equal to an independent Cartesian tensor-GL implementation (box(12)\cube(K), 16 azimuths, no symmetry reduction) to <= 1e-4 km/s per row; sanity vs study ADV_TAIL_CHECK KB12 within the m16 alias + star-roster difference (<= 0.05 km/s)  
  *Sources: R1*
- **B3** — independent-lane Cartesian implementation (no import of the tail library; box(8)\cube(4), doubling-converged 1e-10) on saved C4R3: value/gradient/Hessian <= 1e-8/1e-7/1e-6 of max; lapse pair <= 1e-8 max|t|; bd(z=0) == 0.0 exactly; facade midplane ratio == 0.0 and HI v003 L67 passes; reference/body angular reads (TailBoundary tap) <= 1e-7 max|grad t|; column potential(z) <= 1e-7 of max tail potential difference; imaginary part == 0.0; PLUS a cylinder-O case: O = cylinder K_big = 8 over cube 4, same points and tolerances, the independent lane integrating in (k_perp, psi, k_z) with the cube corner zone K < k_perp <= sqrt2 K handled by its psi limits  
  *Sources: R1*
- **EPS** — Numerical sup searches are estimates, not proofs; envelope consumers read the full-envelope fields (A57.4). q(k) sampled via QINF evaluator f58de0dc (cache 7b9816ae cross-check), 13+13 directions x 64/decade per unit shell of [K, K_big]; refined 26+26 x 128/decade; eps_s(refined) <= 1.1 eps_s(base) else refine; 2 refinement failures -> EPS_UNCERTIFIED. Coverage: DDO from 2 to at least sqrt2 * 2P (= 362.04 at P = 128; the module's unit shells end at ceil(sqrt2 * K_big), so the DDO record covers [2, 363]); NGC [2, 46] (ceil(sqrt2 * 32) for the N3 case K_big 32; RI-17). The record carries envelope_bound {rule A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS, coverage_max_inverse_kpc} with coverage >= sqrt2 * 2P (A52.5 as raised by A54). Until such a record is slotted, per-shell values above 15 /kpc are lower bounds and SRB_ROT is not read. An estimate, not a proven sup.  
  *Sources: R1; A52.5; A53 NEW-19; A54 (coverage); A55.4; A50 item 9; A57.4; certificates_v002 (coverage note)*
- **LO** — non-lapse tail (components 1-9 of the asymptotic response) on saved C4R3 le3 state, shells (4,5],(5,6],(6,8],(8,12],(12,16],(16,32],(32,64]; Claude3 method (origin_c3v001, shell_resolved_c4_c3v001); pass <= 0.005 tau per shell and <= 0.05 tau summed; shells extended so that coverage reaches >= sqrt2 * 2P (= 362.04 at P = 128), every extended shell <= 0.005 tau (shell partition: RI-06). The DDO LO certificate is computed with the M_s 128 source (A57.1).  
  *Sources: R1; A54 (coverage); A55.4; A57.1*
- **GQ** — For every gas roster used, the gas transform at M_s and at 2M_s agrees to <= 1e-12 * P0 at the 4096 I1T seeded nodes over [K, K_big]; certified per source geometry over the union of all T-case tail node domains: DDO (C2T-C4T, C4T-KLO, C4T-KHI, incl. the corner zones) and NGC T120L [2, 32]. A replay. With production M_s 128 (A57.1) the DDO certificate is computed at M_s 128 against 256 over the full DDO reach (to sqrt2 * 2P = 362.04, the module node reach at K_big 256) on all nodes, not only sampled ones. A failure or a coverage shortfall reads UV_TAIL_GAS_QUADRATURE_UNCERTIFIED, which is NUMERICS_UNCERTIFIED.  
  *Sources: A46 RA7; A48 AMB-12; A50 item 8; A55.1; A57.1*
- **DOUBLING** — (w/2, o+4): DDO static rows on saved C4R3 le3 change <= tau_i/20; NGC lnN reads on saved T120L change <= theta/20  
  *Sources: R1*
- **I1T** — at every tail build: roster transform vs packet source at 4096 seeded nodes <= 1e-12 relative (UV_TAIL_SOURCE_MISMATCH); the I1T record covers every T-case.  
  *Sources: R1; A48 AMB-11*
- **T2I** — Before T2 is read: nodes_v001 transform replicas applied to the C5H rosters equal the C5H stored packet sources on G5\G4 to <= 1e-12 (route-A updated per iteration; offset new_body_fourier_J; feedback gas_source_feedback). A T2I failure reads IMPLEMENTATION_DEFECT (T2I).  
  *Sources: A46 RA3; A48 AMB-10; R1*
- **SRB_ROT** — static rotation-law channel bound (V001 sec 1.4, renamed; necessary, not sufficient) <= tau_i/10 on C4T. Computed on C4T: when C4T is flagged, a pass carries the flag and a failure is undecidable. Not read until the EPS envelope record (A52.5) is slotted.  
  *Sources: R1; A50 item 7; A52.5*
- **RB_FP** — RB-FP_i = 2 * eps_max * |dv_i/dlambda| * kappa_i <= tau_i/10; dv_i/dlambda := (|v_i(C4T-A) - v_i(C4T)| + E_i(C4T-A, C4T))/0.05 (conservative); the noise contribution 2 kappa_i eps E_i/0.05 is recorded; kappa_i = sum_s|dV_static_is| / |sum_s dV_static_is| (shell split, saved C4T); first-order response DECLARED, UNTESTED. E is the Picard allowance only. If C4T's E is unavailable (NEW-7, A56 N1) or C4T has a B4 gap, RB_FP reads E from C4T's Picard R-PAIR member (the 12-pass rerun admitting C4T's route A); C4T-A gets the same Picard path; both are on the resolvable list; an unresolved one, or RB_FP with undefined kappa, reads INCOMPLETE. Shell labels are read by index and never emitted verbatim in blinded modes (S6).  
  *Sources: R1; A48 AMB-09; A50 item 9; A56 N2; A54 S6*
- **MT_monitor** — route-A per-iteration M_T (static rotation-channel effect of t[S_T(updated_n)] - t[S_T(gas_n)] at 12 row radii x 8 azimuths in tau units, v_ref = A2F10 route_a_rows); M_T(accepted) <= 1/4 else flag TAIL_SOURCE_UNDERCONVERGED (stopping rule unchanged). An MT verdict FAIL for a run is the TAIL_SOURCE_UNDERCONVERGED flag on that run; a defective MT record reads NO_RUN; an MT record, when supplied, covers every T-case.  
  *Sources: R1; A50 S2; A48 AMB-25*
- **result_assembly_identity** — Gated ONLY by B0prime_RERUN, B1 (Z2) and Z2_OFF_RO1, on DDO154; NGC result assembly is UNTESTED (deciding test: the first NGC route-B result under the NGC driver successor compared with a v009 parent).  
  *Sources: R1; A47 I6; A52.1; 0517*
- **LO_NGC** — LO_NGC is the readout-coupled share, the quantity the N-tests read (lnN only, metric v002 L76); the field-level indicator is carried as an auxiliary field; the record carries an honest i1t field. NGC I1-T of stars + H2 against the T120L fixed source must pass before any NGC N-test is read. LO_NGC is reported only in this compare; the NGC N-tests get their own small compare before any N-test is read; N-tests are not read as passed before LO_NGC passes.  
  *Sources: A52.4; A48 AMB-23; R1 (L8)*
- **HARMONIC** — Reported, not deciding: a0/a4/a8 of dlnN/dR at route-A query 03 (R = 1.48 kpc), at the four diagonal azimuths, for C4T, C4T-D5 and C6T, and for C4R3, C5H and C6 direct (C6 from its checkpoint replay).  
  *Sources: A46 RA10*
- **RECEIPTS** — A receipt is required for every run case; a missing receipt reads INCOMPLETE.  
  *Sources: A48 AMB-26*
- **record_verdicts** — A gate record whose verdict contradicts its own data is a RECORD_DEFECT (NO_RUN group), not a decided failure; a defective or malformed gate record reads NO_RUN with next step "fix the record or gate and re-review", never a physics reading.  
  *Sources: A54 S5; A48 AMB-02*

## Tests

- **T1** — Pass iff cases C2T, C3T, C4T are valid AND V005 criterion.shape_pass literally (Dhat_T(3,4) <= 1 AND Dhat_T(3,4) <= 0.5 * Dhat_T(2,3)) AND RA6: for every row i, d23_i * d34_i >= 0 and |d34_i| <= 1/2 |d23_i|, where d23_i = v_i(C3T) - v_i(C2T), d34_i = v_i(C4T) - v_i(C3T); if d23_i = 0 the row passes only if d34_i = 0. TINY (DECLARED; applies to the RA6 clause only): a row is TINY iff |d23_i| <= tau_i/8 and |d34_i| <= tau_i/8; TINY rows are exempt from the per-row clause and stay in Dhat. No floor clause; FLOOR_LIKE pre-named (D14). Known blind spot (G5): a growing row whose increments both stay <= tau/8 is exempt; the backstop is T1_H.  
  *Sources: R1; A46 RA6; A47 I2; A47 (G5)*
- **T1_H** — C6T against C4T: per row |v_i(C6T) - v_i(C4T)|/tau_i <= 1/2 every row, decidable; no TINY exemption. C6T is consistent through RO1.  
  *Sources: R1; A47 (G5 backstop); A47 I7*
- **T1_S** — {"runs": ["S4T", "C4T"], "statistic": "max_i |dv_i|/tau_i", "pass": "<= 2 (V005 tau_shape_agreement)", "S4T": "route-B sphere mask with sphere tail; route A, reference, body cube with cube tail"}  
  *Sources: R1*
- **T2** — C4T-D5 against C5H (spec 60b46130): per row |dv_i|/tau_i <= 1/4, decidable, T2I passed. C4T-D5 = K = 4 cube with the nodes_v001 tail on G5\G4 (lapse-only; the LO certificate on shell (4,5] makes a T2 difference read as tail-implementation error).  
  *Sources: A46 RA1; A52.6; A46 RA11*
- **T2c** — C4T-C5c (continuum_v001, E1, outer cube K_out = 5) against C4T-D5: per row |dv_i|/tau_i <= 1/2 (PASS/FAIL); a failure reads SOURCE_RULE_MATERIAL.  
  *Sources: A46 RA2; A46 RA11*
- **T3** — With production K_big P = 128: T3 = {C4T-KLO (K_big 64 = P/2), C4T-KHI (K_big 256 = 2P)}, each against C4T at P per row <= tau/4, decidable. Producers emit the labels C4T-KLO and C4T-KHI; A55's "C4T-K64/K256" is descriptive only. The compare reads P, P/2 and 2P from the registered case block and refuses any other values; the R1 labels C4T-K16/C4T-K64 are retired.  
  *Sources: A54 (generic T3); A55.1; A56 (labels)*
- **RB_FP_run** — {"runs": ["C4T-A", "C4T"], "C4T-A": "C4T with lambda_scale 1.05 in every stage"}  
  *Sources: R1*
- **SR_K** — {"kind": "static replay", "states": ["C2R3", "C3R3", "C4R3"], "K": [2, 3, 4], "statistic": "Delta_i(K) = rows[packet_K(S_pkt)+t_K] - rows[packet_K(S_T)+t_K] (unit response from each case 01_offset/unit_response.npz); pairwise K-dependence", "use": "reported; enters u_i and the T1-fail reading as max(|Delta_i^SR(4)|, |Delta_i^SR(4)| * A_i), A_i = |dv_i/dlambda| / |dV_i^static,tail| from the AMP run (DECLARED, UNTESTED); the static value is labelled \"static only; fixed-point UNTESTED\", deciding test C4T-SR; flag SOURCE_QUADRATURE_MATERIAL if that max exceeds tau_i on any row"}  
  *Sources: R1*
- **D_m4** — {"runs": ["C4T", "C4R3"], "statistic": "v009 harmonic diagnostic m4", "use": "reported"}  
  *Sources: R1*

## Decision rule

- **ADOPT_TAIL_cube_K4_C4T** — All of B0, B0prime_DRY, B0prime_RERUN, B0_FA, B0_RO1, B0_N3, B1 (Z2), Z2_OFF_RO1, B2, B3 (incl. cylinder-O), EPS, LO, GQ, LO_NGC (for NGC readings), DOUBLING, I1T, T2I, SRB_ROT, RB_FP pass; T1, T1_H, T1_S, T2, T2c, T3 pass; a receipt for every case; no flag unruled; every step resolved (otherwise INCOMPLETE with the pending steps named).  
  *Sources: R1; A46 RA5/RA7/RA8; A47 I6; A48 AMB-17; A48 AMB-26*
- **carried_uncertainty_u_i** — |v_i(C4T)-v_i(C3T)| + |v_i(C6T)-v_i(C4T)| + |v_i(S4T)-v_i(C4T)| + max(|Delta_i^SR(4)|, |Delta_i^SR(4)| A_i) [static only; fixed-point UNTESTED, deciding test C4T-SR] + RB-FP_i (km/s; reported with u_i/tau_i and u_i/sigma_i)  
  *Sources: R1*

## Outcomes, first applicable

- **[1a] NO_RUN** — Any identity or implementation gate fails (B0, B0prime_DRY, B0prime_RERUN, B0_FA, B0_RO1, B0_N3, B1/Z2, Z2_OFF_RO1, B2, B3; a B2/B3 failure is IMPLEMENTATION_DEFECT of the gate), or a gate record is defective, malformed or contradicts its data (RECORD_DEFECT). Next: fix and re-review. Every reading names every missing or invalid case and gate.  
  *Sources: R1; A48 AMB-01; A48 AMB-02; A54 S4; A54 S5*
- **[1b] INCOMPLETE** — Placed directly after NO_RUN. Any registered V007 case (T-runs, C5H, identity-gate runs) invalid or missing, including BRACKET_HULL_MISS, a missing receipt, a pass-row gap or row-ID defect, RB_FP with undefined kappa -> name each case and gate with its next step; no T-test is read. Subtypes: CASES_OR_RECORDS (tests unread) and UNRESOLVED (tests read: ADOPT_TAIL or FLAG_PENDING_RULING with a pending step; a NOT_UV/SRKD split that turns on a flag).  
  *Sources: A47 I1; A50 item 4; A50 item 5; A48 AMB-17; A48 AMB-26; A54 B4; A54 S9; A50 item 9*
- **[1c] NUMERICS_UNCERTIFIED / NON_LAPSE_TAIL_MATERIAL** — Same position. NUMERICS_UNCERTIFIED: EPS uncertified, DOUBLING fails, GQ fails or a GQ/EPS coverage shortfall. NON_LAPSE_TAIL_MATERIAL: LO fails (LO_NGC for NGC readings). Next: named successor. No T-test is read.  
  *Sources: R1; A48 AMB-03; A48 AMB-18; A50 item 8; A46 RA7*
- **[2] decided failure outcomes, in R1 order** — Read in this order: IMPLEMENTATION_DEFECT: T2 decidable and fails; stop, T1/T3 not read as physics (also a T2I failure: IMPLEMENTATION_DEFECT (T2I), A48 AMB-10) | SOURCE_RULE_MATERIAL: T2c fails; root ruling on the gas rule before adoption | KBIG_NOT_CONVERGED: T3 fails; T3prime: production 2P with {P, 4P} (= 256 with {128, 512} at P = 128); EPS/LO coverage >= sqrt2 * 4P (A56 N4; R1's "production K_big 64 under T3prime (32/64/128), EPS and LO to 128" is superseded) | BOUND_INSUFFICIENT: RB_FP or SRB_ROT fails; next: q-corrected shell (second asymptotic order), design successor | FLOOR_LIKE (D14): T1 fails only by a contraction clause (max-based or per-row, RA6) with Dhat_T(2,3) <= 1 and Dhat_T(3,4) <= 1; takes precedence over the two T1-fail readings below; a floor clause needs a new prereg version before any further case | NOT_UV_RESIDUAL: T1 fails AND T2c <= tau_i/4 every row AND SR-K pairwise K-dependence (2,3),(3,4) <= tau_i/4 AND no TAIL_SOURCE_UNDERCONVERGED flag; next: column/Picard map, own prereg | SOURCE_REPRESENTATION_K_DEPENDENT: T1 fails otherwise; next: fixed-point SR runs C2T-SR/C3T-SR/C4T-SR (packets over the smooth source), own design and prereg | HIGHER_K_DISAGREEMENT: T1 passes and T1_H fails; adopt nothing; C6T candidate under a V007 amendment sealed before further results | SHAPE_DISAGREEMENT: T1_S fails; review per-stage C wiring. A decided failure is read when its own condition is fully decided even if another step is unresolved; the pending steps are listed.  
  *Sources: R1; A50 (final order); A48 AMB-10; A48 AMB-17; A46 RA6; A55.1; A56 N4*
- **[3] UNDECIDABLE_ROUTE_A_TAIL** — Only if no decided failure outcome applies and some test with a TAIL_SOURCE_UNDERCONVERGED run failed (flags are evaluated per test: a flagged test that passes, passes with the flag carried; one that fails is undecidable and cannot trigger IMPLEMENTATION_DEFECT, NOT_UV_RESIDUAL, SOURCE_REPRESENTATION_K_DEPENDENT or FLOOR_LIKE). Next: rerun that case with seed source_rtol/10.  
  *Sources: R1; A48 AMB-04; A50 (final order)*
- **[4] UNDECIDABLE_AT_ITERATION_FLOOR** — A paired test still undecidable after R-PAIR: neither pass nor fail; no adoption. Both undecidable readings are listed when both apply.  
  *Sources: R1; A50 (final order)*
- **[5] FLAG_PENDING_RULING** — Every gate and test passes but a flag stays unruled (SOURCE_QUADRATURE_MATERIAL, or TAIL_SOURCE_UNDERCONVERGED on an adoption run); no adoption; needs every step resolved; root rules on the flag (a flag ruling is a root addendum entry naming the flag, run and evidence, registered before any adoption reads the flagged test).  
  *Sources: R1; A48 AMB-04; A48 AMB-17; A48 AMB-19*
- **[6] ADOPT_TAIL** — The decision rule holds and every step is resolved.  
  *Sources: R1; A48 AMB-17*

**Reading rules:**

- Any reading made while a step at an earlier position is pending is marked PROVISIONAL, with the pending steps listed. A decided T3, T1-split or SHAPE reading stands while T2/T2I is pending, marked PROVISIONAL. *(A50 (final order); A50 item 3)*
- "No T-test is read" applies to NO_RUN, INCOMPLETE and NUMERICS_UNCERTIFIED/NON_LAPSE_TAIL_MATERIAL; T values may be reported descriptively, labelled "not read". *(A48 AMB-18)*
- Governing principle: no ruling may make adoption easier than the text; where the text is silent the stricter-on-adoption reading is chosen. *(A48; A53)*
- A V1-V6 failure other than BRACKET_HULL_MISS -> named defect, fix and rerun that case under V007 with thresholds unchanged. *(A48 AMB-16)*

## NGC3198 N-tests

- **state** — saved iteration-0 operator ngc_kgrid_fidelity_c2/phase23/ops/T120L_hovr (OPERATOR.json e6453d520f902e77da77e49b8f8d1cdbed84639f11ed6cc661943553741b2af4); replays only; no NGC prep successor needed
- **theta** — 3.3657664138980042e-09
- **azimuths** — 32
- **tail** — {"source_rule": "continuum_v001", "quadrature": {"K_inverse_kpc": [2], "outer": {"shape": "cylinder", "K_big_inverse_kpc": 16}, "order": 8, "w_perp_max_inverse_kpc": 0.005, "w_z_max_inverse_kpc": 0.007, "R_eval_max_kpc": 136.5, "R_src_max_kpc": 136.4847475059566, "z_eval_max_kpc": 105.0, "z_src_max_kpc": 95.0, "phase_perp_rad": 1.365, "phase_z_rad": 1.4, "N_perp": 25608, "N_z_plus": 18288, "M_s": 96}, "gas": {"M_s": 96}, "jet_order": 1, "roster": "stars + H2 registered (prep v001 L183-250 radial form, no GL4 tail normalization) + razor-thin initial gas (prep v001 L290-295); I1-T vs ops fixed_source_fourier_J / initial_gas_fourier_J", "stars": {"segment_rule": "max16_ceil_kdr_plus8", "tail_rule": "t_panels_40a_phase1p5_gl12"}}
- **K7_note** — deterministic single-operator reads, no iteration; tail quadrature noise certified <= theta/20 (NQ), so theta/4 is 5x the certified noise
- **sites** — {"NE1": "replay_c1 c4a8cd02 L79-93 metric_point (zero boundary L81-82, evaluate_line L86), L105-106 lnN -> TailCtx subclass (ngc_ring_tail_ctx_c2v001.py)", "NE2": "kg_lib_v001 06333714 L163-173 checker pins, L193-201 ctx_with -> ctx_with_tail (same new file)", "NE3": "ringeval_v001 5149ea29 L12 ZK, L23 ctx_with, L24 roster, L31 lnN -> ringeval_uvt_c2v001.py", "NE4": "dsplit_sphere_v001 a4390c6a L34, L46 (mask sphere_info_v001 4f616b14 L22) -> sphere_eval_uvt_c2v001.py", "NE5": "run_p23_v001 3578e83c L19 ALLOWED, L59-70 -> run_ntests_c2v001.py"}
- **tests** — {"NQ": "doubling (w/2, o+4): change of lnN0 and dL <= theta/20", "N0": "K_big = K: lnN at the 7 heights on all rings bitwise equal to phase23/out/rings/T120L_hovr/*.json", "N1": "S = max_phi lnN0 - min_phi lnN0 < theta on the 12 TRUNCATION_SHAPE rings (ordinals 1-8, 10, 13-15), C1 as written; C1prime still passes; all 100 reported", "N2": "sphere-masked T120L + sphere tail vs cube T120L + cube tail, per ring and azimuth, lnN0 and dL(+-10,+-20,+-30) <= theta/4", "N3": "K_big 8 and 32 against 16, at every ring and azimuth: |Delta S| <= theta/4 and |Delta dL| <= theta/4, S = max_phi lnN0 - min_phi lnN0; \"S/theta\" is a reporting unit only (0512; A54 lanes)", "N4": "e4 at +-95 kpc (A14.C5), cube+tail vs sphere+tail: reported"}
- **not_covered** — NGC route-A/route-B fixed points with the tail wait for a valid NGC route-A base (UNTESTED)
- **LO_NGC** — required before N-test readings (R1 L8; A52.4: readout-coupled share; NGC I1-T of stars + H2 against the T120L fixed source passes first)
- **outcomes** — N_NO_RUN (a record is defective or contradicts its data; name it), N_INCOMPLETE (a record missing, NGC I1-T not passed, or LO_NGC absent; name each), N_FAIL_<test>, N_PASS; N_PASS is only an input to NGC route A/B (0512; A54)
- **own_compare** — the N-tests get their own small compare before any N-test is read (A48 AMB-23); NGC tail route support is the driver successor v011 (0517), plan-identical to the sealed DDO driver
- **sources** — ["R1", "0512", "A54 (lanes)", "A52.4", "A48 AMB-23", "0517"]
## Run list

- **DDO_gates** — Z2 (2d5e79d0; rerun on r5 with driver-derived tokens), Z2_OFF_RO1 (894e5b3a; rerun on r5), B0prime_RERUN (4ac5527a; rerun on r5).  
  *Sources: A52.1; A55.3; A47 I6*
- **DDO_tests** — C2T, C3T, C4T, C6T, S4T, C4T-D5, C4T-C5c, C4T-KLO (K_big 64), C4T-KHI (K_big 256), C4T-A (P128 specs with gas M_s 128, re-registered and dry-run again; registry PENDING).  
  *Sources: A46 RA11; A55.1; 0530 item 1; A56 (labels); A57.1*
- **external** — C5H (spec 60b46130; driver 999331af; REVIEW_V009 original 3bce7c02; admitted on the three A50 grounds: REVIEW_V009 PASS for driver 999331af and spec 09ff5a96, a byte diff of 60b46130 against 09ff5a96 limited to the label and fs_absolute_overrides, and the clean dry run). Read before the seal only as validity/admissibility booleans and reason codes, no row value printed or written.  
  *Sources: A46 RA11; A48 AMB-20; A50 (AMB-20 restated); A53 (REVIEW_V009); A47 I3*
- **contingent** — R-PAIR members (<= 4 pairs), with specs registered before any T result (A52.3); the PICARD member specs are successors per A53, with B0 evidence (gates_v004, PENDING): admit the base route A, column_workers 1, V6 result_sha equality, an RO1 record equal to the base's, and for the C5H PICARD member no ro1_workers.  
  *Sources: R1; A52.3; A53; A57.2; compare r5 NEW-20*
- **replays** — B2, B3, EPS, LO, GQ, SR_K, shell_split, DOUBLING, T2I, B0_RO1 replay (RA5 b), EA replay record (AMB-08/22), MT record.  
  *Sources: R1; A46 RA11; A48 AMB-08*
- **NGC** — NQ, N0, N1, N2, N3, N4, LO_NGC, NGC I1-T.  
  *Sources: R1; A52.4*
- **limits** — Resources are root's launch decision; the module memory cap is a resource guard (8 GiB in r5). R1's "<= 4 processes; serial route A; tail memory <= 0.6 GiB/process" is superseded (route A parallel 8, A47 I4; guard A55.2).  
  *Sources: A47 I4; A55.2; 0527*
- **cpu_hours_estimate_UNTESTED** — R1's 77/93 CPU-hours were estimated for K_big 32 and are STALE at P = 128 (route-A tail build 15.1 min per call at K_big 128, Codex2 0418). No new estimate here (RI-09).  
  *Sources: R1; A54 (Codex2 Lane A); A55*

## Seal record requirements

- Before the seal the compare's gate and admissibility functions run on the real input records (the C5H receipt and result if present, the identity-gate records and the RO1 replay); their output goes into the seal record (E-SEAL1). *(A46 RA13)*
- Blinding: on C5H the gate functions run only as validity/admissibility booleans and reason codes, with no row value printed or written; the seal record states that no row value was shown. Record-controlled labels are redacted in blinded modes. *(A47 I3; A54 S6)*
- The compare pins at seal: V007_PREREG_SHA256 (this text once sealed), PIN_ADDENDUM_V005 (frozen V005 sha), PIN_REVIEW_V009 = the preserved original 3bce7c02, PRODUCTION_K_BIG_A55 = 128.0; its custody pins (PIN_RO1_CUSTODY, PIN_RO1_NODES_CUSTODY, the drivers_allowed I4 set) move to r5's re-pinned shas read from r5's BUILD record, verified from bytes. *(0526; A53 (REVIEW_V009); A55; A56 (A55 follow-ups 1, 3); compare r5 NEW-26)*
- Key-equivalence map: every key v010 adds that differs from v009 numerics appears with its absent/default value and B0 evidence. *(A48 AMB-13)*

## Scope UNTESTED

- S1 transfer across parameter space (V005 S1) unchanged
- NGC fixed points with the tail
- outer-panel part of the kept-grid quadrature g_K (V005 S3)
- RB-FP first-order assumption
- all costs and memory
- NGC result assembly under v010 (L3)
- NGC lapse-only omission on (2,16] until LO_NGC (L8)
- sphere-C tail cost and memory at production domains (IA3)
- GQ for C4T-K256 at the registered M_s 64 (TESTED-NEGATIVE; RI-02)
- P128 cost and memory (route-A tail build 15.1 min/call at 128; K_big 256 build ~0.877 GiB)
- driver v010 r5 (not built at assembly)

## Root items

See `ROOT_ITEMS.md`. OPEN: RI-01, RI-03, RI-05, RI-06, RI-09, RI-10, RI-11, RI-12, RI-13, RI-17, RI-18. RESOLVED by A56/A57 and integrated: RI-02, RI-04, RI-07, RI-08, RI-14, RI-15, RI-16.

