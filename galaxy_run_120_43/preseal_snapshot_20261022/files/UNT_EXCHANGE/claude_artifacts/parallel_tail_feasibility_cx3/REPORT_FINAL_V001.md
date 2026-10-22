# 0595 parallel-tail feasibility

`date -u`: Sun Oct 18 21:09:06 UTC 2026.

Process matrix overall verdict: **TESTED_PASS** across the complete saved C4R3 K32/K128/K256 N2/6/12 matrix. Individual case verdicts remain in the data artifact. Configured VECLIB1-versus6: **TESTED_PASS** on the listed finite experiments. All table arrays, records, state digests and order1/order2 jets at218 probes were compared directly. This is nonproduction component evidence, not launch admission.

| Saved C4R3 K | Worker cap | Wall s | Wall speedup | Total CPU s | CPU speedup |
|---:|---:|---:|---:|---:|---:|
|32|1 serial|19.811|1.000|19.575|1.000|
|32|2|13.145|1.507|19.806|0.988|
|32|6|9.241|2.144|22.522|0.869|
|32|12|7.835|2.528|23.659|0.827|
|128|1 serial|233.695|1.000|230.237|1.000|
|128|2|140.638|1.662|222.214|1.036|
|128|6|88.094|2.653|242.518|0.949|
|128|12|75.279|3.104|260.836|0.883|
|256|1 serial|943.113|1.000|934.827|1.000|
|256|2|584.048|1.615|912.060|1.025|
|256|6|381.125|2.475|1006.792|0.929|
|256|12|326.595|2.888|1086.751|0.860|

VECLIB configuration comparisons (native build timing; startup/IPC excluded):

| Case | K | 1-config wall s | 6-config wall s | Byte verdict |
|---|---:|---:|---:|---|
|c4r3|256|943.113|885.469|TESTED_PASS|
|synthetic|32|0.474|0.473|TESTED_PASS|
|c4r3|32|16.541|16.523|TESTED_PASS|
|c4r3|128|221.352|214.772|TESTED_PASS|

Maximum observed RSS: parent 4.350 GiB; worker/thread child 2.364 GiB. These are measured lifetime peaks; no hard allocation-limit claim.

The prototype splits existing independent256-frequency star batches. It retains full-grid nodes, original matrix shapes, component/doubling order, each +=, the global doubling certificate and native cache key. Native gas/source contractions and ring/corner/shell assembly remain unchanged. Full process timing includes preparation and worker creation/teardown. Radius and shell splitting remain source-analysis proposals; changing shapes or reduction grouping needs separate byte proof.

KHI projections below are **UNTESTED**. The prior A89 approximately7.84–13.86h values are a component-based full-call model using measured components, not a measured complete KHI run. When process byte validation passes, only the inherited rotation-equivalent cold-build term is scaled by measured K256 wall ratio. Other costs and counts remain fixed; cache savings are not added. Future load and different source/stage states can invalidate the estimate.

| Scenario | Worker cap | Prior modeled full h | Projected full h | Saving h |
|---|---:|---:|---:|---:|
|C4T-KHI_expected_I7_P3|2|7.84–7.84|7.15–7.16|0.69|
|C4T-KHI_expected_I7_P3|6|7.84–7.84|6.76–6.77|1.07|
|C4T-KHI_expected_I7_P3|12|7.84–7.84|6.66–6.67|1.18|
|C4T-KHI_upper_I32_P6|2|13.85–13.86|12.65–12.66|1.20|
|C4T-KHI_upper_I32_P6|6|13.85–13.86|11.97–11.98|1.88|
|C4T-KHI_upper_I32_P6|12|13.85–13.86|11.79–11.80|2.06|

Projection status: UNTESTED_PROJECTION.

Retain the sealed r5 lineage. For a later reviewed successor, an optional default1 cold-star process count can be integrated into the native cache-miss path, preserving256-batch arithmetic/order/certificates and BLAS1. The fastest setting in this single K256 experiment was cap12; this is not a general scheduling guarantee. Cache-hit and parallel savings overlap. Estimated development/review cost: one narrow implementation pass and one independent review/byte-replay pass plus measured replay runtime; not a promised elapsed time. No production adoption in this study.

Limitations:

- Single samples per setting under uncontrolled ambient load; own numerical matrices execute sequentially.
- Pool N and VECLIB6 are configured caps; task PIDs do not measure simultaneous workers and actual thread utilization was not instrumented.
- RSS is an observed lifetime peak after allocation, not an OS hard memory limit; scratch limits are estimates.
- Every state uses TEST_ONLY certificates and production_admissible false. No scientific launch, protected run or target read.
- Saved C4R3 prior I1T PASS is carried from the pinned prior evidence, not independently rerun here.
- One registered stellar component and rotation-stage grid were numerically exercised; other source/stage classes and spherical residual are UNTESTED.
- v003 persistent-cache behavior is source-only; current store rename/cleanup conflicts with immutable-write policy.
- Process timings include pool startup/teardown and full cold star preparation plus native build; thread child timings exclude fresh interpreter startup/imports/jets/IPC.
- Thread verdict is read from result/summary status; process exit0 alone is not a numerical pass.
- All table arrays and returned jet keys were directly byte-compared, plus record/digest; finite218-probe coverage does not prove all possible query points.

File pins (SHA256 read from bytes):

- `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` — `8506f337a83611246ffcff62d6e96c6d2269e5db48508ca3ac2553d56c962aee`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0595_2026-10-18_codex3_parallel_tail_build_feasibility.md` — `72c05307e6011d8e410c560429c83b1dcb0f752df23f9e5364d92692070f99dd`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0601_2026-10-18_all_KHI_measured_r6_no_delay_rule_A89.md` — `1f6421564922755445ae3b5c558242f1e89995f49141e60db4d436e77d99b019`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0613_2026-10-18_all_lanes_taskpolicy_preferred_not_required.md` — `82c214dfe8729603ccea43f803cc091f5b484f4b2fa09147ea57955a1a0f1377`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0617_2026-10-18_all_lanes_multi_agent_concurrent_workstreams.md` — `622f5cc99633a2433ce4fb7feebabb6580a468c6660f48377c7c8e48f6bd102d`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/SOURCE_ANALYSIS_V003.md` — `bf394b2e7ac0fdf082ec2814a456e701599cab2ec7d0fb1269e70b2bd67dfaf9`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/SYNTHETIC_INPUT_CX3V001.json` — `acbdf04bdc7d750668834d1d8bbdf49ad63c9605df7ea77d6a744dffaa80ee53`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/assemble_final_cx3v009.py` — `c50427e3bf149a1b823bb5cca7de373e7b862e9310aaf8ea2c46995ab44e1b29`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v003.py` — `231ac02239264543c2482bcee306e97f7f11bb37ddf26699bdf6084300c62659`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v004.py` — `56e08972a4edd329975e7adca96ae8924aa548354cb7db9d3b63af3f03a2e645`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v007.py` — `fa1ee0531243773a7dc4bfaa35d9ac5cdf1f127ce7929a82a45afaf1a2e46629`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_assembly_cx3/REVIEW_ASSEMBLER_CX3V002.md` — `a685cf0ea6216bd81c1684b2ac230fa7bf918d7683b48cc63fad511e2a62f920`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_assembly_cx3/SUCCESSOR_v007_49_RESULTS_CX3V001.json` — `db72ef00fc0174f6b9958de316a181dac8c0fef3611bddc2ace79a7650d1c107`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_combined_cx3/REVIEW_CX3V001.md` — `27cb2fa432b22eb2149aae715fd7b2e333d498cfb8d165e468d8d040631c510f`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_cx3/REVIEW_CX3V001.md` — `0ac6837d9599fd40f3e320321681788f85da27609e84f30c53697ef311b968d4`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_parent/COMBINED_HARNESS_REVIEW_CX3V001.md` — `dee4b009086ccbfcebd1aa0b7f786fd9f9ecedbcd3bd981784f8ee1407d1cb86`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_projection_cx3/PROJECTION_CX3V002.json` — `162d84e9e8d9292d3f89cae7f0bca3b4dabfe7771072c08f720580723e2fc844`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_projection_cx3/REVIEW_PROJECTION_CX3V002.md` — `23283fe909e4b9f7f91a9ab3a6a90c657944525dffa084fd183485fe262cccf1`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/parallel_stars_prototype_cx3v001.py` — `3b92bb26dae611af928dbc7f935cb808a364a8bbc634f9ce2a99c29f1f9c3a09`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/parallel_stars_prototype_cx3v002.py` — `f1daa12e71418cd565188b1760345b7c0b8c78c5705589e0918e5edf6d20e8c7`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K032_THREADS_V001/SUMMARY_V001.json` — `12844500fd6a86711da22c5dbf9c49bb7885c7af2ce8b5834f8463cd1db9c3d1`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K032_THREADS_V001/THREADS1_REPEAT0_V001.json` — `7dad37ff31802a48b4dc468570af1f4d5a2430cb71898d8845a4052b0a314ec6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K032_THREADS_V001/THREADS6_REPEAT1_V001.json` — `472c36105771d9291f90aca55e226dd77cc12b0e3338420300b24441adf7bfb4`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K032_V001/INPUTS_V001.json` — `9d50d47126552ebefb8d0fc22622811eb574ada99f0847191ef28e92d0ac2ace`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K032_V001/N02_V001.json` — `a400f0b4082ca243c795dc5c0b189d311fb5bd61245c287d0b222432331de4d6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K032_V001/N06_V001.json` — `297f049d38da09522a83786f72d0f5b10d1d483c496db62484824ac53560b870`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K032_V001/N12_V001.json` — `2c5b4f33e5ce6cc02f47abc7a63846698f624745a8fcb337735726ebce44c5d6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K032_V001/SERIAL_V001.json` — `1e034e003ca6f347d5af01359d692ea2e1d060344df07ce9144878421b435365`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K032_V001/SUMMARY_V001.json` — `a8731e7e6274400a857008f25ef817b42777ea1f9e0c2ccec0878ae1bbcd7ee7`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K128_THREADS_V001/SUMMARY_V001.json` — `992370030d210f2e499b10bfd2aef7a703aa59ad328f891a8df53e464a6e7ec6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K128_THREADS_V001/THREADS1_REPEAT0_V001.json` — `bb4e63f6a4cb2c357f7e23911909f75260d85aca88474a1ab1e090131098a7a4`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K128_THREADS_V001/THREADS6_REPEAT1_V001.json` — `e883bcb541d212fc4ccd7adc651d74771d12dc1fa8add61dce38811fa56bf105`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K128_V001/INPUTS_V001.json` — `44417462886362e7a0d2fd73aa8a107da9d58cfa43ac750c1108c9f87bddddbf`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K128_V001/N02_V001.json` — `dde7112aacc568a048e9eeb14083b748bfc8a84142a97a42c45a968b54c0fc05`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K128_V001/N06_V001.json` — `f1d3ce32d66f05f150bb32264561c825d85c35431c66a9b9ce5cc1418dd7c2a6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K128_V001/N12_V001.json` — `bbfdc8478a73b225a15f322798505fa4fae6bb2c82eba60af9f70aabdc205cc6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K128_V001/SERIAL_V001.json` — `79f4d5699a75d985df6ce303a4c24eaa4af5d3a57f83e2fd16f29debb066260b`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K128_V001/SUMMARY_V001.json` — `3ecfcbd2ec0a50268806ad76d27f442dce5166786b4fce3aa5e6418b0c4e6b60`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/INPUTS_V001.json` — `daf95df6d8d3f20582a786da1e0359e695dfa703a9e9cac96e2ce1c5cee57988`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/N02_V001.json` — `9316b0c2db6cca09466c2a5f810e80603b20f91f17d1588765a59f14342d2522`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/N06_V001.json` — `97678d2809285b950f4ee4eabbc53e4cd4517ceb32c84fe138f204beb7373c85`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/N12_V001.json` — `6975bcfc2628893cee38bcefd8ce552216492c6d9143c6edfa8af48bc7e78bc0`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/SERIAL_V001.json` — `9c3d387e7765131ef8de209b464302d290e7bfebc15c0bc043c4d2c8cffc1660`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/SUMMARY_V001.json` — `a2ef19a03987ee4ba19dc59916fbf83860b32acc1710f30c7cfee3d3880766db`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/THREADS6_REPEAT0_V001.json` — `c29481f94301d4dae3a7fe69ec2c2f26d2657f5727d6fc3e3f8d5e8fc7a40696`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_COMBINED_V001/INPUTS_V001.json` — `7361063958a23d704de3263575ce70a634da52265710e31d35e3f6372f15a98e`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_COMBINED_V001/N02_V001.json` — `cdbdd845149b998b8772dccaa7ae5f266d3509dc0b8d6b553c31eec3cc40b856`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_COMBINED_V001/SERIAL_V001.json` — `ab8d4747349c2da4d675a5f0ce8d6eec5f24b69d4f001d34595a26cc0558efa6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_COMBINED_V001/SUMMARY_V001.json` — `dbebb4b7552c7f54befd5403f0e0b53dc783d0381776e5d84d4b332f4ea6eee2`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_COMBINED_V001/THREADS6_REPEAT0_V001.json` — `aa2ca5279b1769da4331310b5144962eaad8057f746467c3160d2247f200b1ce`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_V002/INPUTS_V001.json` — `e529bc2d54774c8aae1cb7b206c32fc50e69161c5a0c7b8356ba2e5fe7c9d031`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_V002/N02_V001.json` — `02361c975dd42ba8ade0c65ee4453b3da6566f98493d555e7b021ac2d4a080c9`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_V002/N06_V001.json` — `57279db42dcd879669ef48d30f1176c1644f376a1ccf551200ce21c12fddc11e`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_V002/N12_V001.json` — `0b616949f2dd16485977dc80f1157d96acc52bc3731ce7d4b929e9ff41d8372a`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_V002/SERIAL_V001.json` — `17404bd47ce0ca0497bd137884c7d9f9584a37f74932b4f3ad9bc18eccdc6a11`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_V002/SUMMARY_V001.json` — `6060af747e413a9765197fea5b3a0a7877661b2256eaffb041566df4a2774f4b`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K128_V001/INPUTS_V001.json` — `ea3832bcc5c72c48d77824f4076f8660209f41f5fd5e6630d0b3d925cd6aecae`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K128_V001/N02_V001.json` — `62bc6efcc45008677f64b1786ddfd183b9e8830735cdd52df76bec74fffd0d36`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K128_V001/N06_V001.json` — `3240ec1e3a7c714fa7003320a6751575c4c276f848dd709df2d628054b90d051`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K128_V001/N12_V001.json` — `98e4bf96c220222108bf763115b7ae63a0d6588ea0fddcca72eb4cf49cc9102c`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K128_V001/SERIAL_V001.json` — `b59913c0f564746cbe6bac6571031bdb02a51119e350a42997f0b3ca8a6f51f6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K128_V001/SUMMARY_V001.json` — `1f39ac0784507fa2ec66edd15797d27c7f4bc444f741ee781d2755bf9324e1fc`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/threading_tail_cx3v003.py` — `78d54f9bfd6b60b2b9f8405ecdb0e0d3372263a4a2de0ebf06d6eb65ee7134cc`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py` — `2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/posix_libm_bessel_jn_provider_c2v001.py` — `d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/uv_tail_source_roster_c2v001.py` — `4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r6/module/owned_uv_tail_lapse_v003.py` — `e733eb1ebfe2137a6f58d0e35caa345525756e3896ca729c1ba15a39204c7155`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_timing_v003/TIMING_V003.json` — `3e3fb60081acf19c6247bda056ebcb92a4cfb4439dbe912b8b6213da4f9ec925`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_timing_v003/out/TIMING_route_b_rot_KB0256_MS128_st_V003.json` — `616e4c3944bf3782152bd0acae384fac6f5910f08e82a0b25ebba4ded44b77ed`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_timing_v003/tools/assemble_timing_v003.py` — `a154e3b22c25bc9fb4c6c95255c081d75981f683dc4e44355b781b27f6a9875d`.
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/inputs/seed_c2v001.json` — `fc70a262b12773c6f60c93101bce9f499000b96a2c58c04e94e3691e9019df59`.
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/result.json` — `aac01962dc7bf08a7486179bc5674af520f7ea38d73b004154cdd2ff25fa8dee`.
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/stages/15_le2_rotation/rotation/rotation_base_arrays.npz` — `4e53085c8dc1d44b8a83a46eff4ae595ee3a64068ce544ba928d8b2abf9693cf`.
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json` — `f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b`.
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/galaxy_baryonic_source_forward_v002.py` — `e9be043b46790e3493f4e427fb483a98a5665f004dfac287d5758afce0ac96ad`.
