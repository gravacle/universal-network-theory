# Codex3 GQ review: certificates_v003, dispatch 0552

`date -u`: Sun Oct 18 15:05:04 UTC 2026

**PASS_WITH_FINDINGS. TESTED:** 86/86 numerical, domain and record checks pass; all ten DDO part source chains and their pinned module/provider/profile bytes verify. The one finding is a non-gating relative-maximum aggregation label. No DDO GQ acceptance blocker was found.

Record reviewed: GQ_CERT_V005_MS128, SHA-256 `fbceefe68fecda35745575fba6c85e550e016e8aeefea59233147e520c803e21`.

## Independent numerical reconstruction

The harness independently reconstructs C2R3 gas columns from the saved rotation arrays, checks axisymmetry and positive masses, and matches radial nodes to the profile's GL4-in-s columns. Its radial cardinal functions use normalized-coordinate polynomial coefficients, independently of the producer's product formula in s. It contracts vertical ring masses directly and constructs the production axes from the declared panel rules. No certificate, producer, reviewer or tail-module numerical code is imported. Shared mathematical inputs are the saved state, profile, declared quadrature/domain rules and system libm J0; J0 is separately checked against its cosine integral.

The case is **C2T K_big 256**, kept cube K=2. The reconstructed axes are bit-identical to the stored k_perp row profile and have 41,176 × 102,400 nodes. Subtracting the kept core gives **4,216,166,400** production tensor nodes, equal to the record. K_big is a component-cylinder radius: k_perp ≤256 and |k_z|≤256, so |k| reaches sqrt(2)×256 = **362.03867196751236 /kpc**. It is not a sphere of radius256 or a cylinder with component limit362.

All masses are nonnegative. Writing the transform in normalized column factors Q_i gives

`|S128(kp,kz)-S256(kp,kz)| / M <= sum_i (m_i/M) |Q_i128(kp)-Q_i256(kp)|`.

This bound was independently evaluated at **every one of the 41,176 production k_perp nodes**, so it covers all positive and negative k_z, including every production node in the upper shell (256,sqrt(2)×256]. Its maximum is **1.653208411490979e-14**, versus the gate threshold1e-12 (about60.5-fold margin). The producer's corresponding bound is1.6650687147813326e-14. The independently computed roster-free maximum `max_i |ΔQ_i|` is3.143492410817572e-14 at these nodes. These are numerical estimates with a wide acceptance margin, not interval-arithmetic proofs.

An explicit upper-shell contraction also used48 k_perp rows (12 largest stored row maxima,12 highest-k rows,24 independently seeded rows), and every production k_z in the shell on those rows:

| Quantity | Independently recomputed |
|---|---:|
| Shell nodes explicitly contracted | 1,548,647 |
| Maximum sampled |k|, /kpc | 362.0376892706585 |
| max |S128−S256| / P0 | 1.5003347545585697e-16 |
| M_s64→128 failure canary | 1.318428301607498e-9 |

P0 equals the independently summed gas mass to the recorded precision. Both subtracting the two transforms and contracting the radial-factor difference first were checked. Negative-k_z conjugacy holds exactly in the selected check. The M_s64 canary fails by over1300 times the threshold, so this check does not merely reproduce an insensitive sample.

At the producer's global-maximum coordinate (k_perp0.0009927535875615956,k_z196.81796666477413), the independent difference-first value is1.7575171329293744e-15 and subtraction gives1.7416623698807143e-15, compared with the record's1.801987469716857e-15. The source magnitude agrees within2e-16 in P0 units. These differences sit at floating-point roundoff. The producer's exact tensor maximum was not independently enumerated; the stronger all-k_z bound establishes the requested shell's acceptance.

## Record, reach and source custody

Every DDO roster entry is field-equal to its pinned part's sample and all-node fields, and every row-profile hash, shape and maximum matches. DDO_C2T, DDO_C3T and DDO_C4T each include K_big256. All DDO sample entries use M_s128, doubled256 and4096 nodes. The record's DDO all-node maximum1.801987469716857e-15 and total18,215,051,040 nodes reaggregate exactly from the ten parts. That total is a record reconciliation, not a new18-billion-node replay.

All ten DDO part references trace back through the saved C2R3/C3R3/C4R3 result, finish and final-field request to the declared source rotation arrays; all cited byte pins verify. C6T's C4R3 stand-in remains explicitly labelled in the record. This lane independently reconstructs the C2R3 transform; it does not infer independent numerical reproduction of the other source states.

## Finding CX3-GQ-1 — NOTE, TESTED

The unqualified top-level `max_rel_change` is **4.6673200698272256e-7**, which equals the DDO sample maximum. The record also includes the NGC_T120L reach46 entry with **5.460625163380553e-7**. Therefore the top-level field understates the maximum over all included roster entries. Aggregate all entries or rename it `max_rel_change_DDO_sample` and state its scope.

This does **not** change the P0-normalized GQ gate: relative change is reported rather than gated, and the absolute maxima and the large-|S| relative maximum aggregate correctly. Embedded NGC entries cover32/46 at M_s96; this DDO review does not qualify current NGC K32/reach91.

## TESTED / UNTESTED limits and hygiene

**TESTED:** the full C2T upper-shell acceptance bound, the explicit selected-row upper-shell replay, the M_s64 failure canary, source reconstruction, domain/count/profile identity and described record custody/reaggregation.

**UNTESTED here:** an independently enumerated maximum over all4.2b C2T or18.2b aggregate nodes; exact continuum quadrature error (128→256 is a consistency test); numerical replay of every other source/geometry; current NGC certificate qualification; any real score or new scientific run.

The selected run took77.22337698936462 seconds with peak RSS162,496,512 bytes. Python used the prescribed isolated runtime, no bytecode writes and single-thread BLAS. There were zero audit denials. Scientific-data reads were explicitly registered. No UVT run, C5H run, NGC target or observed velocity, network, deletion, rename or overwrite was used.

Selected harness: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/gq/review_gq_cx3v002.py`, SHA-256 `6395b28a0e7da89db35df230cc3c3ae3879ae5db237e0605806ecacabb041549`. The earlier source version is preserved but was not run; v002 only removed a dead no-op before execution. A supplemental aggregation assertion exposed CX3-GQ-1; its factual results are recorded below, with the finding preserved.

## Evidence byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/gq/GQ_REVIEW_CX3V001.json`: `32b32d05d4cc19b0c38797d0fe580bfd394a1bd39c2c4323c53091d5ad14b080`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/gq/CUSTODY_AND_AGGREGATION_CX3V001.json`: `6bf8b01d6099cc2b30893483ee8f702b4b1b1bec72011997c01ebd2137e7fe4b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/gq/review_gq_cx3v002.py`: `6395b28a0e7da89db35df230cc3c3ae3879ae5db237e0605806ecacabb041549`

## Input byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0552_2026-10-18_codex3_crosslineage_review_r5_and_certs_v003.md`: `8bf2c832f1490f67beceb03c0bccbe7f5773f2d76dd8a1352a9afe411672ca99`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/gates/GQ_CERT_V005_MS128.json`: `fbceefe68fecda35745575fba6c85e550e016e8aeefea59233147e520c803e21`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_C2T_KB128_V001.json`: `ff9ad11b50a9a924d3336106cfdf1e443e0e5fe0ef216bf2f238be32af1a4a5b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_C2T_KB256_V001.json`: `1c3570385c1539ce035ff8e2d309e9ff93e6b64924ddf520a465e0d1a709535c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_C3T_KB128_V001.json`: `509e93e76156e22ed3c0c7b67d9d6595c2ae705223dd35f16768f4fac7377093`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_C3T_KB256_V001.json`: `d22c5702b3ce8770d10582dd8eeba79c1bb294f597bdc7996c587656e4e15b40`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_C4T-C5c_V001.json`: `f204cf94d27dca1dd1de8d2cb21dce147a78c13dc689e6cca381f97456a95c60`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_C4T_KB128_V001.json`: `b0106ac7a597aa9271bf5e15f8f3e1961a329d564a24cc253d3aa0da2195e352`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_C4T_KB256_V001.json`: `c79fc8416d6012f744d02b7807ed14d68e1841411274271d8e67ca55d3092aec`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_C4T_KB64_V001.json`: `6ec4e65b489c66cc84f6c185aca1e37d4f40151bbc6c524845a11b18a00ae27c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_C6T_KB128_V001.json`: `1e5be969d23a17983896e7d5b90970fcc529a5b462ed41c6c28913193eb298fb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_ROWMAX_C2T_KB128_V001.npy`: `5ef4e73cf16b80e08bc2b5251dda06bee0a0ba44906342a2041e25a0a7512d9e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_ROWMAX_C2T_KB256_V001.npy`: `ada97598e5dd9c59a2724d1bc27392512c8e559ba350494ef1cbed438f2521e3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_ROWMAX_C3T_KB128_V001.npy`: `d0c7028ebc0bbf5f31315f5fd11880b3b8eb2f1ebe88e9e303101544aacec844`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_ROWMAX_C3T_KB256_V001.npy`: `11e65e86bd29a58c68bbddc9920efba8ee6a728a531356c66df416b86c75d9f4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_ROWMAX_C4T-C5c_V001.npy`: `26de1cfa89b912a9aa08367d19899e502fa6a7bf91329887535618cea205a66a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_ROWMAX_C4T_KB128_V001.npy`: `d2e8e95701c07d3478cbaaac4664bb3f1e85adac7f052830f1f88fb5964c242c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_ROWMAX_C4T_KB256_V001.npy`: `ea3a5c3a5fcd66305f44e5cb7f04659c4afafb0e0d4ac0b6b3c3b4428fe5d699`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_ROWMAX_C4T_KB64_V001.npy`: `17cdc60710b1d9b0013d9170ecdf646b064a9c5a4ace8bcfb0008e4a4be5af67`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_ROWMAX_C6T_KB128_V001.npy`: `ac9b55ca8db6483b65de7d76bfc48dc597928753a193b09435defc047affa969`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_ROWMAX_S4T_SPHERE_KB128_V001.npy`: `5effe7b01a1ad824a24b6705505b77f215afa8b6edafdc64212d88fe52cdc093`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/out/GQ_FULL_S4T_SPHERE_KB128_V001.json`: `dbe454d89ae7e73920512bb0531a8f53a39def135a556497c10d38f1280c8521`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/tools/assemble_validate_c2v004.py`: `6b01835c76f388fccba68712a84538551711e07494295aeb87f1966261f93598`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/tools/certs3_common_c2v003.py`: `2e6b1bc5b4cc164ef2361aff420e69c38e309f1d221659bff06300c008c67635`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/tools/gq_full_c2v003.py`: `17ce5e4102945ccb61148097ac486615618f82bfdc2d98b744492bd03dcbcecb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module/owned_uv_tail_lapse_v001.py`: `c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module/posix_libm_bessel_jn_provider_c2v001.py`: `d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module/uv_tail_source_roster_c2v001.py`: `4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C2R3_D7R3_RUN_V001/finish.json`: `a7b6f260045ae63f984dc9ae2c1f83ce3aee2f014d4c0e80e403a0e1f671ecfb`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C2R3_D7R3_RUN_V001/inputs/seed_c2v001.json`: `059b4a1603f116581e080abc284fc4a766eec440bcdd061917be0764a6d70e8c`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C2R3_D7R3_RUN_V001/result.json`: `1f6b32a4edd0dd28438536165bdb10e13c8125eb5ccafb60ceb17315eba8c169`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C2R3_D7R3_RUN_V001/stages/15_le2_rotation/rotation/rotation_base_arrays.npz`: `642493bf92e114f81bdc43b8e87626169b5fe636998dba175fd2e961d97942d1`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C2R3_D7R3_RUN_V001/stages/17_le2_feedback/request.json`: `34cb2f3841346826037c9934fff507e14e572f8f9c730f6a9ae0a57b4993b1dc`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C3R3_D7R3_RUN_V001/finish.json`: `56bff835cb150c16e0de44b8e484f7e3d6e4e98df9ae1986217b80951afa1af3`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C3R3_D7R3_RUN_V001/result.json`: `c9c802f44854d4f41f9e119707235899aba75a8bd42e89c19983f9ca9b817674`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C3R3_D7R3_RUN_V001/stages/19_le3_rotation/rotation/rotation_base_arrays.npz`: `f5709f8423fcf7de1373cab4043efad261ad2d5aece22e5342d5254e4b449d04`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C3R3_D7R3_RUN_V001/stages/21_le3_feedback/request.json`: `5ef26e3fd18da0309d51ab1a35cec45edf7835bce63f2e0503adae1690f6cb54`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/finish.json`: `499563b73e67738fafe151a95b17fc4698172151b0f905f71d912725a679d57b`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/result.json`: `aac01962dc7bf08a7486179bc5674af520f7ea38d73b004154cdd2ff25fa8dee`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/stages/15_le2_rotation/rotation/rotation_base_arrays.npz`: `4e53085c8dc1d44b8a83a46eff4ae595ee3a64068ce544ba928d8b2abf9693cf`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/stages/17_le2_feedback/request.json`: `1c31f0e0cd7206fbd352e24d7607bba27dfcd53ec32cb5464bccc0d9e92585f8`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json`: `f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b`
