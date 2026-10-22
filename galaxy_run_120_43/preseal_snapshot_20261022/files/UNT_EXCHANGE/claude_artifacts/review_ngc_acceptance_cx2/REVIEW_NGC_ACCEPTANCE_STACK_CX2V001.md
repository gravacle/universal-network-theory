# P-106 NGC acceptance stack review — Codex2 CX2V001

Tue Oct 20 14:43:39 UTC 2026

**PASS — 0 blocking findings under A115.** TESTED synthetic behavior and FORMAL source correspondence support the commissioned S0 path. This is not a real-call acceptance or a launch authorization. Claude2 retains adoption and all launches.

The reviewed objects are adapter c2v003a, handoff c2v005 and recipes c2v002, with the unchanged reader c2v003, S5 c2v003 and enumerator c2v001. All cited file hashes below were taken from bytes.

## Results

TESTED: both requested suite runs returned 40/40 MUST_PASS and 59/59 MUST_FAIL; P16/P18/P29/F38 stayed blocked. Independent checks returned 98/98, including an 81-case Q5 truth table, handoff mapping for every case, exact and nextafter threshold boundaries, missing-row failure precedence, zero/empty behavior and max-absolute readouts. Ten mutants were exercised: eight killed and two expected order-equivalent survivors. The independently added checks used synthetic fixtures only and skipped all four blocked tests before entry.

TESTED: all 36 file pins match dispatch 0767; both published diffs reconstruct successor bytes exactly; canonical A153/A155 section pins match the adapter. See the verification artifact for exact paths and hashes.

## Findings and notes

### F1 — FORMAL / TESTED

Location: ngc_lo_state_adapter_c2v003a.py:821,897,959,1062.

Q5 precedence, ratio thresholds, theta bits and spec gamma route agree with A153/A155/A167. Synthetic tests and independent checks support the inspected logic.

### F2 — FORMAL / TESTED — same-lineage

Location: ngc_acceptance_handoff_c2v005.py:277; consumed_states_cx2v005.py:223; lo_producer_cx2v004.py:56.

Execution-facts rule mirrors Codex2 fresh_scope/LO keys. It establishes completed, fresh, single successful computed route A with start zero, no retry/reload/resume. This is same-lineage evidence.

### F3 — FORMAL / TESTED — same-lineage

Location: ngc_lo_state_adapter_c2v003a.py:111,502; ngc_acceptance_handoff_c2v005.py:86; ngc_rho_producer_c3v003.py:313.

S2 pins/schema agree with A179. Refusal of Codex2 DDO rho schema/EPS producer and the symbol-route reference to that producer are same-lineage. NGC rho source was inspected, not executed.

### F4 — FORMAL / TESTED

Location: ngc_roster_recipes_c2v002.py:574,614; route_a_uv_tail_controller_c2v001_r5.py:483; coupled_gas_checkpoint_c2v003.py:576.

R1 reconstructs next gas with the same expression and recorded updated array, includes element n, and checks next I1-T exactly before S5 digest admission. N and broken-chain synthetic paths pass.

### F5 — FORMAL / TESTED

Location: ngc_roster_recipes_c2v002.py:630,653,793,844,877,914; ngc_s5_rebuild_export_c2v003.py:306.

R2 inputs match the six stage scripts and driver reuse patch: checkpoint caller physical constants, patched reuse profile, recorded body arrays, selected columns or own rotation radii. All six synthetic kinds admit; S5 requires exact roster/state digest.

### N1 — TESTED / FORMAL

Location: owned_uv_tail_lapse_v002.py:681,728; ngc_roster_recipes_c2v002.py:816,831.

Both order-only mutants survive as expected. np.unique sorts/deduplicates evaluation radii before state construction, so these are order-equivalent for valid finite inputs. Removing a radius fails S5 digest admission.

### N2 — FORMAL (suite execution TESTED)

Location: test_ngc_acceptance_c2v003a.py:1289.

The requested suite P29 parses the actual hash-only row contract before its query-manifest open is blocked. This is a test-scope guard gap, disclosed in packet 0529. Its contents were neither displayed nor used for this review. Independent checks skip P16/P18/P29/F38 before entry. No reviewed file was changed.

### N3 — FORMAL / UNTESTED prospective readiness

Location: ngc_lo_state_adapter_c2v003a.py:455; ngc_rho_producer_c3v003.py:275.

Current point custody admits exactly the four registered S0 keys. This review covers that commissioned path; it does not establish acceptance of future member/F keys. Root must resolve point registration before broader P112 use; deciding test is authorized acceptance with each newly registered point.

## Source correspondence

FORMAL: the scalar gate is g=(v*1000)^2 R rho B1/(2 c^2 theta), using the fixed theta bits and per-shell/cumulative bounds 0.005/0.05. Coverage/empty/unavailable handling and monotone observed failure precede PASS. Q5 makes accepted, inherited and route-B own-source states decisive; iterate-only failure is transient only when decisive classes pass. State input, configuration, source, I1-T, physical constants and ten-key rho identity are rebound to the call/state before admission. Readouts use each call own finite absolute maximum across passes, retaining missing-row uncertainty.

FORMAL: handoff execution checks precede inventory/adapter work; the adopted record is reread from its pin and checked against inventory/classes. SRB_ROT is report-only and catches its own failures. The reader enumerates current and next for every completed iteration 0..a, including final monitor-next N; nonaccepted sources require S5 admissions. S5 compares source and TailState digests, reloads exported arrays and checks the digest again.

FORMAL: recipes use controller/checkpoint order and recorded updated gas, not a fabricated next checkpoint. The six route-B paths follow the inspected driver and binding inputs. README builder choices 1–5 and root items R1–R5 were checked against A181: broken-chain reconstruction, exact reuse patch execution at authorized S5 time, pinned external controls, exact patch shape, and unchanged adapter choice are consistent. Production profile/H2/prep/roster contents were not examined. The source comparison does not replace the real-call deciding tests.

## Remaining deciding tests

- **UNTESTED — P16, P18, P29, F38:** Authorized root execution; P18 public handoff entry with A179 pins specifically remains root-owned.
- **UNTESTED — Real-call N and all consumed-state S5 admissions:** First real call S5 on the run host, including COMPLETED(a).updated_gas_fourier_J and N digest.
- **UNTESTED — Actual reuse-module load/patch, checkpoint caller decode and route-B profile/stars match:** Root first real-call S5. Code correspondence and stand-ins do not prove real data compatibility.
- **UNTESTED — Admitted body path:** Root scope ruling and an authorized test if this path enters the plan; current fresh-call path and recipe fail-closed behavior reviewed.
- **UNTESTED — Scientific acceptance/value readiness:** Root-approved row policy/S10 and successful public post-run acceptance of each real call. No real call or numerical scientific verdict was examined.

## Conduct and lineage

The execution-facts mapping, DDO-schema/EPS-producer refusal and rho symbol-route comparison are explicitly same-lineage. Driver/stage correspondence is cross-lineage source review. The exact permitted Python ran isolated with bytecode disabled and single-thread BLAS. nice -n 10 was attempted but setpriority was denied by the sandbox; successful low-priority scheduling is not claimed. No real run tree, target/velocity/sigma/slots/query file, network or session log was accessed. The provided P29 test did parse the separately hash-only row contract before its forbidden manifest read was stopped; this exception is recorded above, rather than claiming perfect scope enforcement.

## Byte hashes

RESULT: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_acceptance_cx2/RESULT_CX2V001.json — 3b40a3445d67cd88fb2e66f6f964205d44f3524616a97e15ecd35c565215df5b

Verification: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_acceptance_cx2/PIN_AND_DIFF_VERIFICATION_CX2V001.json — eebde2c3ebdbea109955f01629ac1efe6b335fad78859b019673871f60cdcb40

Dispatch: /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0767_2026-10-20_codex2_A205_queue_P106_classifierB_launcher_v004_G26.md — 47531f2671f30ba3966b0ddc896686b354f3d67d2e3304ad95c1e12978205025

### Evidence artifacts

- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_acceptance_cx2/record_run_1_cx2v001/SUITE_RESULTS_C2V005.json — 002496f2e865050a39b68ca4095f0144f613f756405950d26fe29ce3f5a0840e
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_acceptance_cx2/record_run_2_cx2v001/SUITE_RESULTS_C2V005.json — 37b14d98bbcd1f332dc549781d9d1de664a09bc22803c662b9bf887022b1ca9d
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_acceptance_cx2/INDEPENDENT_CHECKS_RESULT_CX2V001.json — 912da17f01b0712e6c377185e8d8dc3aed4a775f6f28d89a45f2eda4488c407b
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_acceptance_cx2/independent_checks_cx2v001.py — 529cf82666f7e7d19356fda281fa50d83b68e430b0e6be2050c99711733019d5
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_acceptance_cx2/AUTHORIZED_RULINGS_SNAPSHOT_CX2V001.json — 5cd7bdd5a2fd897eba5d943702bd25bbb21e94364ee0ff685d599f4e00223d32

### Source files

- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_lo_state_adapter_c2v003a.py — 9c4b6dfc591cfd5c372416beb936d5d903540e5fc41e4a327b428d7ba5001eb2
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_acceptance_handoff_c2v005.py — 7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_acceptance_handoff_c2v004.py — 2721cfd1d27f6b05b831ba53b02a99125bd49033d235530b911453696bb8f29d
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_roster_recipes_c2v002.py — c700f469314d73e90cd2498cdbea5b7f69fbbd9b61676468ea5e37356939978e
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_roster_recipes_c2v001.py — 6c9e8508cb590e764bda8643caf48c931359bc7318674b1a150ccd43d9ccebce
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_route_a_iterates_c2v003.py — 9335ee4212719944b6dd45369161de16891ec0ed5dbdd97fed36d68d0b993bdc
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_s5_rebuild_export_c2v003.py — 3611e9933b57363ffab8dbdbaae67960751e59d3d34b219f1777e8e2f2a54100
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_consumed_states_c2v001.py — 607b7f667dfa1612da3fd874ab2656dc5ca487285a28afb2e4b1bfe979bd3125
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_row_contract_c2v003.py — f2f54d79cbdbda89113121e1c2068d42f0c8d8460b5ccff963d015ac0f9e73a2
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/test_ngc_acceptance_c2v003a.py — e452cec252aeb54c64723c5fc324409bb6e308b0b27f01f3bd43cebeab3a11c0
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/test_ngc_acceptance_c2v004.py — fcf7e43f2cfbf1c4f059e30b48cb07ebbff591bd7e765d4975dc21ac0c4e52f4
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/test_ngc_acceptance_c2v005.py — ae045203a3c6bb2b9663ebfb807f0c1208d8177067cca4f83857a7c088802605
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/README_NGC_ACCEPTANCE_C2V005.md — 6a8b1bc7b69d6d9ebd4d1c848a7da13a4f0c26288313255a643865387b747611
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/DIFF_HANDOFF_C2V004_TO_C2V005.diff — e9f1111456b91854510bb929779586ddbbbdc5fe98036a5925717df6d00faf60
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/DIFF_RECIPES_C2V001_TO_C2V002.diff — 868de8542a8474674692d63b2bae45ffc4a93b03a5cccd08989ccdceb6bf756d
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/NGC_ROW_CONTRACT_C2V001.json — 80cbf2f5be2e9f22a0b751376dcde3e7e779bd89f531a8ffe9d654616490fe32
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py — 577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/ngc_route_a_tail_manifest_cx3v011_r5cx3v001_cx3v005.py — b9247b1aef0d9c3c05757bd27d68a9964a22d078ce8189311f11e0e2ad6b4c7c
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_uvt_route_b_binding_cx3v006_r5cx3v001_cx3v005.py — aee7af1286f2d3d9d52117d6b4d4ae82e31d8776af4a4b0a6da7cee96be12fb3
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_a/route_a_uv_tail_controller_c2v001_r5.py — c5bdd0553968e3f00b61db89f7944cebe51166006f58b727a7aed2a9b6a434fc
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_uvtail_c2v001.py — 8ef3079b0a23c32c688605e96eb5b79beb79768578cc7aef22ea087c7ae12469
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_uvtail_c2v001.py — 7667025bd9382a58688153fde98bf90f2b67d27baa39a939982631c305c229db
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py — 069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py — 2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/posix_libm_bessel_jn_provider_c2v001.py — d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/ngc_rho_c3v003/ngc_rho_producer_c3v003.py — d3d0f3ddda8be2e3d4b0e0732e5237a602cb3b1fb99d7921e8c10a886420a3c4
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/ngc_rho_c3v003/ngc_lo_slot_proof_c3v003.py — ada31d121871598aa0cd7db5137691502421c873cc75bdf331706501d3f3310a
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/consumed_states_cx2v005.py — 7b7400f331970a5f5fb7f7104f5e1850a765fcd04fc993100b5d1f0f37f4d653
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/lo_producer_cx2v004.py — 5db60d0f6db6d481e2f748b19bef08ce425f19a0e463d58727c184d633e03d51
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_body_source_offset_root_v003_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py — 1ede2384637bfacaa52944b2aebb70fb82bfe1ede7ec08da3c9691e929df68e3
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_fixed_K_free_surface_root_v001_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py — 4d4c34674d45a3832f28591ac53b88c6f343ce194b1c75d2fced608f55dcd60a
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_free_surface_rotation_root_v001_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py — 9922a919ebadfc1ba17508f42ee553918d50ad29e36fdfa2bc3677bcbc1767c4
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_fixed_K_free_surface_root_v003_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py — 5657503c4d5c9c7db203c1de09f3ceb6cbd9a5a70aa4e680a56227f20e03b58b
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_fixed_K_free_surface_root_v005_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py — dd0c759be8b85b107828b1db8d7e453134176ac32a68544f6f6d6a8f1f92eee0
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_free_surface_rotation_root_v005_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py — e22e79e80a63825458ca659dd32c81bef473e170ba81486ef9db86929007249f
- /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/ddo_homotopy_reference_root_worker_v001.py — acda989d375925bf9a8163d8d8a3a22c3f183b6b253c8137312bccc0cefbbe36

