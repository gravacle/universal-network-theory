# PARTIAL — lens R2-B (regressions and new defects), helper of lane Claude4

Started: 2026-10-18T19:56:52Z

## Object hash verification (from bytes, shasum -a 256)
All 10 files listed in round2/HASHES_R2.txt match:
- PREREG_MISS_READING_R2.md 97d5ce33ffa90e64ac208d36863c776460ad596fded2f376f1090a232e5ce407 MATCH
- CLAUSE_SOURCE_MAP_R2.md 38cd6852bdc32c240a6935671c82d618da399dd20e7d6adaa5aa2a26cd24f201 MATCH
- ROOT_ITEMS_R2.md 4907cf019c7bec62da646dc862f6c36c2b3aa03b11b761f36475c1056e968500 MATCH
- NUMBER_PROVENANCE_R2.json ff6ca9b84384171285abbbc6d072a21346048884e9deff4fa79b0629f52c98bf MATCH
- TARGET_FREE_CHECK_R2.json 624f278e02419ca28ea4a3a12fb869822cd4fddd8eaa721492d38996217c91f9 MATCH
- TARGET_FREE_MUTATION_TEST_R2.json 4445a9bf014e0cabe6d49cd0f45e4df1c388ac7c2c443df0d6f1d3a62214ec02 MATCH
- tools/check_target_free_c4v002.py 4ae4f7053f18aa13416ad4e3d118d9250a959e72035c6e5f0c5f92305d8511aa MATCH
- tools/test_check_target_free_c4v002.py dc812342fa7c363e71949e3ecb2a206d68786ff5973280cf98909d03dd114f92 MATCH
- tools/make_miss_reading_c4v003.py 2132078f9779b01d5ad05c01b0280c218d160f6380f75ed5b99af893a1a2f9ab MATCH
- INDEX_R2.md 0d24b8fe778fb704398a7039f579977d92e51dfd152994d6e68048cffa03b926 MATCH
HASHES_R2.txt itself: 2e3cf0c60088f23a9530a3ab5b8d8ec1a2d8c5184a7eeff11f726fafa964c6fd

## Status
- [ ] read prereg R2
- [ ] read v003g code (format)
- [ ] own classifier + synthetic edge cases
- [ ] source checks (TSR overlap, gate wording, receipt, timing, A65, Codex1 0032)
- [ ] steerability

## Progress note (TSR source check), stamped below
- V005 read: 991cc242e30eeea5118058e0f60862f7f50f1cb2cf434a85d92f4055413848c8 (same as at assembly; headings to A96).
- V004 487d4449... and V003 5bef6552... match section 11.
- Dispatch shas in section 11 all match bytes (0512..0606). 0592 = b1a5310f... (not cited).
- K32 compare 6f095f64 MATCH, N1 record 8867c376 MATCH, GL4 nodes ec1dcca5 MATCH.
- N1 ring_radii_kpc == GL4 radii_kpc bitwise 100/100 and == radii_m/kpc_m bitwise 100/100.
- r14 = 9.901810628740723, r15 = 10.540847190215317, r16 = 10.911721936765339, r17 = 11.655974441199351 (0-based ordinals; compare S_over_theta[15] = 1.01481832531416).
- Interval (r14, r16) contains only Q25 (10.04). Q24 9.04 < r14; Q26 11.04 > r16. Flag set = {Q25} CONFIRMED.
- Slots V003 observation rule: "HI-weighted mean of R*Omega, then piecewise-linear interpolation of mean onto the supplied 43 manifest radii without extrapolation" (slots projection_pins.entries.observation_rule). Prereg says "of the azimuthal mean": misquote (NOTE).
- Adapter owned_column_mean_streaming_observation_v002.py (6790e28e) does bisect_left piecewise-linear interpolation of column means, emits query_support.radial_support_m = bracketing nodes. Rotation evaluate owned_free_surface_rotation_v001.py (e1b354ec) is column-local in Phi_R (D only enters the shear C_RR). So the derived rule holds, but the column-locality premise is uncited.
2026-10-18T20:03:42Z

## Progress note 2026-10-18T20:25:49Z
- V005 changed during the review: 991cc242 (19:59:28Z) -> cf9bbf19eae3d2fb0262c31c3a0af43ecc2f100b9295c4075a591716b6ebb9dc (20:08:40Z). New A97 (B2 sanity) and A98 (r2 FAIL per Codex2 0490; r3 ordered, dispatch 0619). All 14 cited section pins still match (V005_PINS_R2B.json).
- Own classifier tools/classify_r2b.py; generator tools/synth_r2b.py (uses v003g helpers; 0 replica mismatches); runner tools/run_cases_r2b.py (V1, 42 cases, superseded) and tools/run_cases_r2b_v2.py (V2, 48 cases). Fence: no audit events.
- TSR recompute: {Q25} by rule (i) in kpc, in metre form, and by the adapter's bisect dependence; 100/100 bitwise.
- Draft findings: R2B-01 BLOCKING undefined-sign MISS rows (dup of A98/Codex2 0490, extended: S(Z) from hits only, C16b P11 with no signed miss; P1g; DT-S0G); R2B-02 SF NOT_READ unconditioned after targets; R2B-03 SF LATE status not mechanical, every RUNBOOK-step-4 gate is LATE; R2B-04 SF STAGE0 receipt rule differs PREREG vs ROOT_ITEMS, circular, successor unpinned; R2B-05 SF P5 "as P1"; R2B-06 SF status tuples (R-MF P6/P7, R-ML, R-TSR P13/LATE, P9 R-DRIFT, DT-T1a); R2B-07 SF TSR flags two sources of truth, no fail-closed stop; NOTES 08-13.

## Final 2026-10-18T20:29:29Z
- V005 last read 20:26:07Z: 7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2 (A99, A100 added; both V007-only). 14/14 cited pins match (V005_PINS_R2B_2.json).
- REVIEW.md written: FAIL, 1 BLOCKING, 6 SHOULD_FIX, 6 NOTE. HASHES.txt written last.
