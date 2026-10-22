# 0617 — NGC independent tail-domain stellar transform replay

Sun Oct 18 20:42:53 UTC 2026

**TESTED PASS — finite seeded convergence test.** This completes the calculation named in LO_NGC_K32_CERT_V001's NOT_RUN deciding test: the registered stellar + H2 transform at seeded tail nodes through91/kpc under a refined segment/tail rule. It does not claim a uniform tail-domain error bound, equality to a nonexistent saved tail packet, or root adoption of the route-A/B launch precondition. Claude2 retains that ruling and all launch authority.

## Exact rule and scope

LO_NGC A52.4's stored-source I1-T precondition compares stars+H2 with the T120L fixed source. That existing4096-node <=1e-12 source-identity test has max|k|3.3742235087245134/kpc and remains separate. A90 explicitly leaves independent tail-domain star convergence open. The LO91 certificate names seeded tail nodes in(2,91] under refined segment/tail rules as the deciding test. Its structural non-lapse share0 is unchanged.

Registered source quadrature IA2 in TAIL_SCHEME_DESIGN_V002_R1: segments use max(16,ceil(kmax*dr)+8) Gauss nodes; tail R=Rlast+a*t, t in[0,40], phase<=1.5, GL12. Doubling segment nodes and tail panels must give max|deltaP|/max|P|<=1e-10. Independent test(b) uses the same radial norm tolerance and <=1e-12 absolute for the sech² vertical transform. These are finite numerical convergence criteria; the1e-12 stored-source identity criterion is not silently replaced.

The new production source record is TESTED identical to stars_registered for both components, with shared height0.4655094193110476kpc. Independent interpolation matches the pinned radial_surface at137stellar/25H2 core, segment, endpoint and tail points (relative1.631e-16/2.177e-17). It uses the same registered target-free photometric inputs and no observed/target velocities.

Frozen seed61720261018;442 distinct radial nodes span0–91/kpc;4096 tail pairs satisfy2<|k|<=91/kpc. Each radial node appears in the pairs, radial nodes>2 include kz=0, and the vertical91/kpc axis is included. NODES_V001's method prose mistakenly says443 distinct; arrays and kperp_count correctly say442 after deduplication of2/kpc. The file is preserved with this correction.

Reference calculation uses independently assembled piecewise-linear/constant-core/exponential profiles, composite GL20 radial panels phase<=2 and tail45a; refinement GL24 phase<=1.5 and tail50a. Vertical reference integrates sech² directly by cosine quadrature to80h, refined to90h. It shares the installed libm J0 implementation but has its own binding; the quadrature, interpolation and summation path are independent. An analytic exponential-disc fixture and a separate angular-integral J0 fixture test shared assumptions.

## Measured outcomes

- Registered radial doubling: 8.0574373360095703e-16, limit1e-10.
- Production versus independent refined radial: 9.668924803211484e-16, limit1e-10.
- Radial restriction kp>2: 4.6795038026033251e-15, limit1e-10.
-4096pair source factor P(kp)V(kz): 6.1397340011170682e-16, limit1e-10. Multiplication by common -c² cancels in this normalized comparison.
- Vertical direct/refined max absolute difference: 3.8857805861880479e-16, limit1e-12.
- Reference refinement passes separately for stellar and H2 components.
-20/20 controls pass, including NaN/Inf/empty/shape/custody/roster/certificate corruption, wrong seed/domain, missing H2, underintegrated legacy u256 tail, threshold boundary, zero scale, exponential analytic and J0 integral fixtures. Omission-H2 canary relative=0.033218812751423146; legacy-u256 relative=2.0659273716795835e-05; both fail the1e-10 criterion as required.

Supplemental diagnostics do not change the adopted norm: maximum per-radial-shell peak-normalized error=2.6923002350628055e-12; maximum pointwise relative error near a small oscillatory P=9.5769817651971581e-10 at kp=40.611718284059059/kpc. These are radial shells, not spherical-domain certification.

Measured replay times: production102.147s, independent/refined120.862s, run concurrently. Both exited0. Strict comparison/control program exited0. Python-I-B, numpy+stdlib, taskpolicy-b, nice10, single-thread BLAS. Output files remain small; no full fields were materialized.

**UNTESTED / NOT_RUN:** all103104 consumed cylinder64 radial quadrature nodes; a uniform tail-domain error proof; saved-packet equality above the T120L support; any source fixed point or forward/route-A/route-B run. No original certificate or reviewed file changed. Finite-test evidence is ready for distinct review and Claude2's prelaunch disposition.

Mutable authority hash changes between planning and completion: {}.

## Byte SHA256 pins

All cited files and deliverables are pinned below from bytes at completion; INPUT_PINS_V001 separately preserves the initial read pins.

```text
622f5cc99633a2433ce4fb7feebabb6580a468c6660f48377c7c8e48f6bd102d  /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0617_2026-10-18_all_lanes_multi_agent_concurrent_workstreams.md
499b10de0854916a2c3d2350e1c4aec5e478e800d52b13cf728b15fc3b9c9672  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/tail_transform_0617_cx1/CONVERGENCE_RESULT_V001.json
238e2c29301fe19c8cae69bf6f31641c82345f80c06dfd349c11ea6fb9682c24  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/tail_transform_0617_cx1/INDEPENDENT_V001.json
78ff2be5480ab8aee308b82a5bd1269a17ca2850ca6d7f2ed2f66153c91e3e4a  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/tail_transform_0617_cx1/INPUT_PINS_V001.json
9fa6c180e8a3b6c2f4f8242cf4dd04a978d40d54141a9c445d1cec76f3cf9653  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/tail_transform_0617_cx1/NODES_V001.json
ab7d2a260a99ac75d3c72d865dd3dad4c6f6a3a4f2655ae932fe469fe762f2da  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/tail_transform_0617_cx1/PLAN_V001.json
bc6adfd3a55b393f478a7e88c96691f743ee87690c3ae71f5d1a37432094ce18  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/tail_transform_0617_cx1/PRODUCTION_V001.json
4a6322d938a10abcd73e6f426e093b1e229b42b46bf9a280dbf93e72f49de417  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/tail_transform_0617_cx1/SHELL_DIAGNOSTICS_V001.json
0ad694d05438291eb3a294f5691cbf695b155e072cc81721cf70cb7298b945ed  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/tail_transform_0617_cx1/SOURCE_EQUIVALENCE_V001.json
65abd97a331ecc7d61f58c638ec5573af54987f4e7f027cee8401ed47dc45cc6  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/tail_transform_0617_cx1/SOURCE_ROSTER_IDENTITY_V001.json
a31983e1bf2b99154d41dfd0ad2bd4d8a3368212a74732c6e98ab6857e2ff59a  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/tail_transform_0617_cx1/SOURCE_SNAPSHOT_V001.json
c4f13c8e90941aa83f38e835e9ae03b7112eb2505204e4d28766dddbd6619cd8  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/tail_transform_0617_cx1/compare_tail_transform_cx1v001.py
fe132f2d5dcbb286e4ee5215c6be2997f9d27618524e630c332701e837ae6f57  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/tail_transform_0617_cx1/replay_tail_transform_cx1v001.py
5e8eea77bd6c52e2d65b4acae421b66dde23eecd2b1c131db11579b4813a5b8e  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_design_c2/v002/r1/TAIL_SCHEME_DESIGN_V002_R1.md
07745bbf6d5c35d5a8568de7fc9e78b8c3bd8c3e371680dc8869c42a893c0382  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_ngc_k32/gates/LO_NGC_K32_CERT_V001.json
3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/I1T_NGC_T120L_V001.json
d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/posix_libm_bessel_jn_provider_c2v001.py
4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/uv_tail_source_roster_c2v001.py
53db2db60856b6f2e11eee94a32405ab762da18b068faa98977bd66189cbc86d  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module/independent/independent_tail_c2v001.py
32c6ccb243259e95e4d67fe2849a233207382ca9194b4bb77ed33444fcf4b81c  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module/tests/saved_states_v001.py
59ada35ce59146c758374c88abeb3ed183f09217501d1f3c7a43463adacc6917  /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md
7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2  /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md
f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b  /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json
157ede0487beed6658a413ae4db34cae2e819efc58efd292ccc56794ae5917d2  /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NGC3198_H2_SOURCE_TAIL_REDUCTION_RUN_V001/stdout.txt
84e20bc022a088f7223319638091b65044983412cec09ac1cb0fb21d205aed61  /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/NGC3198_MAIN_SOURCE_ANNULAR_INPUT_V001.json
e9be043b46790e3493f4e427fb483a98a5665f004dfac287d5758afce0ac96ad  /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/galaxy_baryonic_source_forward_v002.py
```
