# Independent K256 process-matrix projection review

Date -u: Sun Oct 18 20:45:33 UTC 2026

TESTED_PASS: 128/128 metadata, byte-custody and arithmetic checks. This is the completed K256 process-matrix review, not a full-study completion decision. The configured-thread experiment and pending whole-study assembly are outside this review. No numerical model, table/jet replay or scientific stage was rerun. Saved array/record/digest comparisons were checked for internal consistency, equal recorded hashes and PASS status; this review does not claim a new independent raw-array bitwise comparison.

All four supplied result hashes match their bytes and the matrix's path/hash/size records. The matrix joins the exact serial record and N2/N6/N12 measured values. Each saved process record reports 18 named arrays with identical serial/parallel SHA256 values plus record/digest equality. The input record carries C4R3, K256, 72 evaluation radii, 218 jet probes and BLAS caps1. TEST_ONLY certificates and production_admissible false remain explicit. Reported process memory peaks are below8 GiB per process; this is observed lifetime RSS, not a hard allocation guarantee.

| Configured process cap | Cold whole-build wall seconds | Parallel/serial ratio | Wall speedup | Total CPU ratio |
|---:|---:|---:|---:|---:|
|1 serial|943.113142|1.000000|1.000000|1.000000|
|2|584.048023|0.619276731|1.614787|0.975646|
|6|381.125288|0.404114068|2.474549|1.076983|
|12|326.595120|0.346294740|2.887714|1.162516|

The projection uses the exact pinned A89 timing decomposition:

`T(N) = T_base + (2*950.4 + I*417.7) + 2*897.3 + (2+2*P)*811.5*(wall_N/wall_serial)` seconds.

Only the cold rotation-build term receives the measured ratio. The count is8 for I7/P3 and14 for I32/P6. All baseline, route-A and column terms stay unchanged. The equivalent difference formula was checked independently against the full component sum. The selected final-assembler source uses the same arithmetic; its full pending assembly was not run here. No persistent-cache/r6 saving is added.

| Scenario | Cap | Prior modeled full hours | Conditional full hours | Conditional saving hours |
|---|---:|---:|---:|---:|
|C4T-KHI_expected_I7_P3|2|7.837404–7.844598|7.150833–7.158027|0.686571|
|C4T-KHI_expected_I7_P3|6|7.837404–7.844598|6.762823–6.770017|1.074581|
|C4T-KHI_expected_I7_P3|12|7.837404–7.844598|6.658555–6.665750|1.178848|
|C4T-KHI_upper_I32_P6|2|13.854682–13.861876|12.653182–12.660377|1.201499|
|C4T-KHI_upper_I32_P6|6|13.854682–13.861876|11.974165–11.981359|1.880517|
|C4T-KHI_upper_I32_P6|12|13.854682–13.861876|11.791697–11.798891|2.062985|

All full-call runtimes and savings above are **UNTESTED projections**. The prior model is also not a measured complete KHI call. Same-K256 measurement removes cross-K extrapolation only; evolving source/stage/state and future load transfer remain UNTESTED. Cap12 is fastest in these single observed samples, not a general scheduling guarantee. A rho=1 planning fallback retains the prior model but is not an upper bound: contention could be worse.

The cold timer includes the process preparation/startup/teardown and native build. Validation comparison times are separate:134.046152s,74.308860s,70.050595s for caps2/6/12. These are not repeatedly subtracted or added to production component costs. Adoption still needs its separate net-benefit accounting for build, review and identity reruns; this arithmetic grants no adoption or launch authority. Historical r6-directory observations remain time-scoped and are not promoted into BUILD/admission claims.

Reviewer peak RSS: 22790144 bytes. No protected run, observed/target data, network, scientific launch, binder or launcher access occurred. All successors are exclusively written; prior review artifacts remain unchanged.

Byte pins read from files:

- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/K256_PROCESS_MATRIX_V001.json — SHA256 `0c8f9633996c3c5e8f37c3580167a4269f50b1cd73d391bb9d6da72b4f92234d`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/SERIAL_V001.json — SHA256 `9c3d387e7765131ef8de209b464302d290e7bfebc15c0bc043c4d2c8cffc1660`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/N02_V001.json — SHA256 `9316b0c2db6cca09466c2a5f810e80603b20f91f17d1588765a59f14342d2522`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/N06_V001.json — SHA256 `97678d2809285b950f4ee4eabbc53e4cd4517ceb32c84fe138f204beb7373c85`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/N12_V001.json — SHA256 `6975bcfc2628893cee38bcefd8ce552216492c6d9143c6edfa8af48bc7e78bc0`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/INPUTS_V001.json — SHA256 `daf95df6d8d3f20582a786da1e0359e695dfa703a9e9cac96e2ce1c5cee57988`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_timing_v003/TIMING_V003.json — SHA256 `3e3fb60081acf19c6247bda056ebcb92a4cfb4439dbe912b8b6213da4f9ec925`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_projection_cx3/PROJECTION_CX3V001.json — SHA256 `b4e319048c0998401be1fc8dc4cba62fe0df36d7b764be793d10c0dd135558ff`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/assemble_final_cx3v008.py — SHA256 `41af7c1f5a054c1cd1b9d6a847ba691518866be9d40f4ef792d48141cc05ee0c`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_projection_cx3/calculate_projection_cx3v002.py — SHA256 `e192fc4bf5119b761f8c3bfe7077d2cc76d6ed3ad7727a64e1617ebc01a0a7dc`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_projection_cx3/PROJECTION_CX3V002.json — SHA256 `162d84e9e8d9292d3f89cae7f0bca3b4dabfe7771072c08f720580723e2fc844`
