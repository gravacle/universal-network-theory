# AST identity report: STAGE0 successor c2v002 against v003g

Generated 2026-10-19T17:19:32Z by `make_reports_stage0_successor_c2v002.py` (python 3.9.6, `-I -B`).

- v003g: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py`, sha256 `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405`
- successor: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage0_successor_c2/prediction_freeze_c2v003g_stage0_c2v002.py`, sha256 `d260ee308a7f215176cab1fff51e94cb52c7fc6cdd64aa4da48c66f8091820f0`
- diff: `DIFF_v003g_to_stage0_successor_c2v002.diff` (566 lines added, 10 removed)
- fix diff against the unadopted c2v001 (sha256 `e015e617c7437afc1863ef8e30e82f040555bdf32ed0f6518f27ac7ccfb330fe`): `DIFF_stage0_successor_c2v001_to_c2v002.diff` (160 lines added, 49 removed)

Method: `ast.parse` both files; every top-level statement is compared by `ast.dump` (no line or column attributes), so comments, blank lines and line positions do not count. The sha256 columns are sha256 of the `ast.dump` strings, not of file bytes. TESTED: computed from the bytes named above.

## Summary

| Item | Count |
|---|---|
| v003g top-level functions | 109 |
| identical (non-STAGE0) | 102 |
| changed, STAGE0-only (listed below) | 7 |
| missing from the successor | 0 |
| changed but not in the STAGE0 list | 0 |
| new successor functions (all `_stage0_*`) | 25 |
| v003g top-level constants | 111 (identical 108, changed 3) |
| new successor constants (all `STAGE0_*`) | 25 |
| v003g top-level order kept (as a subsequence) | True |

Result: every v003g function other than the 7 below is AST-identical; no v003g function or constant is missing; no other function changed.

## Changed functions (STAGE0 only)

| Function | What changed |
|---|---|
| `_load_row_roster` | require_evaluated no longer refuses the STAGE0 roster, so a STAGE0 replay evaluation can be computed; whether it is frozen is decided only by the receipt rule in the writer |
| `_root_rosters_for_alternatives` | the slots comparison and the per-roster record comparison go through _stage0_status_neutral / _stage0_neutral_record: STAGE0 status is the only tolerated difference |
| `_bind_alternatives` | the slots comparison goes through _stage0_status_neutral (STAGE0 status only) |
| `_validate_manifest_structure` | runs _stage0_manifest_check after the v003g checks (writer, verifier, scorer) |
| `write_freeze_manifest` | new keyword stage0_status_record=None; caller STAGE0 status neutralised; STAGE0 evaluation set aside before D9; _stage0_freeze_decision admits it only by the receipt rule; manifest body gains stage0_status; custody_ok STAGE0 files (sha256 verified and STAGE0 schema valid) added to input_files by realpath unless input_files or code_files already list them; docstring paragraph |
| `_alternative_score_scope` | the STAGE0 record comparison goes through _stage0_neutral_record (status only) |
| `score_after_freeze` | output gains stage0_status (None on refusal paths; the frozen block when scored) |

## Changed constants

| Constant | v003g | successor |
|---|---|---|
| `SCHEMA` | `'FREEZE_MANIFEST_C2V003G'` | `'FREEZE_MANIFEST_C2V003G_STAGE0_C2V002'` |
| `MODULE_NAME` | `'prediction_freeze_c2v003g_cx3v001'` | `'prediction_freeze_c2v003g_stage0_c2v002'` |
| `MANIFEST_KEYS` | `frozenset of 29 names` | `adds ['stage0_status']; removes []` |

Unchanged pins (AST-identical): `ROOT_SLOTS_PATH`, `ROOT_SLOTS_SHA256` (slots V003 `d3859b42...`), `REGISTRATION_SCHEMA`, `PROGRAM_QUERY_MANIFEST_SHA256`, `REGISTERED_GL_NODES_PATH`, `REGISTERED_GL_NODES_SHA256`, `ROW_ROSTER_SCHEMA`, `INVALID_GATE_SCHEMA` and every other v003g constant.

## New functions

| Function | ast sha256 | First docstring line |
|---|---|---|
| `_stage0_neutral_record` | `d6416ed5fd8fa9295d53b7909609e8d4219afa6fd77745ec831997fd08269b91` | A STAGE0_GRID_OUTER record that reads EVALUATED_BEFORE_FREEZE, with its status put back to the slots V003 |
| `_stage0_status_neutral` | `f4be96f28c4756542aab4a5d31290f4f11a3780735aa5d49d6fab6db10c7e63f` | The alternatives declaration with _stage0_neutral_record applied to every declared record. |
| `_stage0_effective_alternatives` | `3b5e633a3ffdb3fcf813c13db7c8c37261f72cbf38310a6284b24f6e7a4e1677` | The slots alternatives with STAGE0's status EVALUATED_BEFORE_FREEZE (used only once the receipt rule held). |
| `_stage0_split_evaluations` | `27b94419805a37c81d881a7610c6cf185822527de95e5000c66c657c0a6a9d4b` | (the evaluations without STAGE0, the STAGE0 evaluation or None). |
| `_stage0_registered` | `d39796fc8ac5d4b502bfb92209dd7ee43f952f3e74478dd3581fae3f0141c5d8` | The slots V003 STAGE0_GRID_OUTER record (None if the pinned slots declare none). |
| `_stage0_self_sha256` | `6fc595c486d5cc6e22df4b2c695cb11a98f3c6798afcbb1ea574f4c5411a3b4a` | sha256 of this module's own file bytes: the sha rule (b) needs the seal entry to pin. |
| `_stage0_utc` | `e533f21e04c0ddca85cb6dc1e336271ec1ae302ddf0bbbfc0d7e9c8b06abe1a2` | A root-recorded UTC time written exactly in one of STAGE0_UTC_FORMATS; None otherwise. |
| `_stage0_pin` | `593fcec8be8900c0d5d8cf22fe508e1085de9be4a5c101b20339cda4ee8a177a` | A well-formed {'path', 'sha256'} pin whose path is absolute, normalised LEXICALLY to |
| `_stage0_real` | `d7a5591d3f50701df1fe0294e9e234e54f83da2d4a934b746180e30534257f65` | os.path.realpath(path) -- the path _pin_files records -- or None if it cannot be computed. Used only to pin |
| `_stage0_source` | `d5cb279bf20333d0aa6e7caa8fc97ce78c14b9dce92f82857263f102b60b5887` | The file a STAGE0 pin is read from. At freeze time (pinned None): the path root named. At verify and score |
| `_stage0_read` | `4c2dc8789e52013e675dff5082fc17f299cad5edc285f823b421374f69757678` | (doc, None) for a custody-verified (sha256 from the bytes), target-screened JSON object; (None, code) |
| `_stage0_same_theta` | `798cb35bf976e6b725b8bee8c8a8c8efebd805506d3bfc69191841a8f9d224d4` | Exact theta identity (same keys, equal finite values): the receipt is for this member's call. |
| `_stage0_members_of` | `241543878efca88ef82763eec31b81f9214f2b73fc8dfd020dc07e4f4f295a6b` | The registered STAGE0 members: one per PRIMARY member, in member order ([] if the list is malformed). |
| `_stage0_frozen_code` | `37d0f99c844b308f4ca74e2448eac79f8a5ca4cef9a61e60c88fc48c25507c01` | c2v002 (D07): the single frozen code of a STAGE0 file that is not read again, when it is one of allowed; the |
| `_stage0_frozen_row` | `4dc1a7574041cad7e8e0a3beccd6449c6813ba69eed791fc6cc2a03e540e2354` | c2v002 (D07): the frozen member row i when it is member m's (same member_id and log_index); None otherwise. |
| `_stage0_apply_record` | `30ae2066084b302ad1aeadddb55809458998d3a344f50f0560e6faadb9994705` | Fill the verdict v from the status record and its receipts (helper of _stage0_receipt_verdict). frozen and |
| `_stage0_receipt_verdict` | `1127ffcd001faf7fe6d436eba023619d1158022214814d00f2c29ae09e718be5` | M-14 rule (a), rule (b) and the step-4 timing, from root-written bytes only (no output value is read). |
| `_stage0_eligible` | `450b6bcb2e69c9a22166a8e6444cea165bcdd91dcb5fbe7caacb924fb501cb91` | Phase 2, rule (a), rule (b) and the step-4 timing all hold (refusals are judged after this). |
| `_stage0_block` | `3819b26d9ede30ad6469d416bae247504f65086ef63f7872bf1ae476d3dbb23e` | The frozen stage0_status block: the receipt verdict plus the M-14 reading and its codes. |
| `_stage0_custody_pins` | `243f90a79b65012ea96e86ba7fcf5dd6d39381e9ab8d2b01af58b34c7ae84f49` | The custody_ok STAGE0 files (sha256 verified and STAGE0 schema valid: status record, member receipts), as |
| `_stage0_pinned_map` | `0a7aa46970db7716510ab80f574fa7d542672b6c560b450853fd792178ab06bb` | {sha256: path} of the manifest's code_files and input_files pins (the first path per sha256). |
| `_stage0_input_files` | `c504fd559dcf5c2b7808385a8be6bed5d7f6de0ccd0a05f826547f1d67f8359c` | input_files plus the custody_ok STAGE0 files, by realpath (the path _pin_files records). c2v002 (D05): a |
| `_stage0_evaluation_refusals` | `d1d77eb09698d05b2699538830ccf248229d2bc45dbf0689cc7136c6750c413c` | Every check v003g applies to a frozen non-primary alternative (writer: ok, query ids, root roster pin, D2 |
| `_stage0_freeze_decision` | `e430d018e8ebcc5f1004c824acbd7c440774923a9afe55cffaa1dcdbcb2ad8cc` | Writer side of M-14. Returns (stage0_status block, admitted). Appends no refusal reason: when STAGE0 is not |
| `_stage0_manifest_check` | `c55d79ecb43928302145f9238c57ba79de314a716dbd17500c6ce2201a4be12c` | Verifier side of M-14 (writer, verifier and scorer all run it): every custody_ok STAGE0 file must be pinned |

## New constants

`STAGE0_ALTERNATIVE`, `STAGE0_STATUS_RECORD_SCHEMA`, `STAGE0_RECEIPT_SCHEMA`, `STAGE0_STATUS_RECORD_KEYS`, `STAGE0_SEALED_SUCCESSOR_KEYS`, `STAGE0_RECEIPT_ENTRY_KEYS`, `STAGE0_RECEIPT_KEYS`, `STAGE0_PHASE_1`, `STAGE0_PHASE_2`, `STAGE0_FINISHED`, `STAGE0_EVALUATED_REFUSED`, `STAGE0_NOT_IN_PHASE_1`, `STAGE0_RECEIPT_NOT_FINISHED`, `STAGE0_NO_SEALED_SUCCESSOR`, `STAGE0_RECEIPTS_AFTER_STEP4`, `STAGE0_UTC_FORMATS`, `STAGE0_MEMBER_KEYS`, `STAGE0_BLOCK_KEYS`, `STAGE0_RECORD_NOT_SUPPLIED`, `STAGE0_RECORD_PIN_MALFORMED`, `STAGE0_NO_RECORD_CODES`, `STAGE0_UNREAD_RECORD_CODES`, `STAGE0_UNREAD_RECEIPT_CODES`, `STAGE0_FROZEN_DEFECT_INCONSISTENT`, `STAGE0_RULE`

## Other top-level statements

| # | Kind | Status |
|---|---|---|
| 0 | Expr | CHANGED (module docstring: successor header prepended) |
| 1 | Import | IDENTICAL |
| 2 | Import | IDENTICAL |
| 3 | Import | IDENTICAL |
| 4 | Import | IDENTICAL |
| 5 | Import | IDENTICAL |
| 6 | Import | IDENTICAL |
| 7 | Import | IDENTICAL |
| 8 | Import | IDENTICAL |
| 9 | Import | IDENTICAL |

## Changes against the unadopted c2v001 (by AST)

| Kind | Name | Against c2v001 |
|---|---|---|
| function | `_stage0_apply_record` | CHANGED |
| function | `_stage0_custody_pins` | CHANGED |
| function | `_stage0_frozen_code` | NEW |
| function | `_stage0_frozen_row` | NEW |
| function | `_stage0_input_files` | CHANGED |
| function | `_stage0_manifest_check` | CHANGED |
| function | `_stage0_pin` | CHANGED |
| function | `_stage0_pinned_map` | NEW |
| function | `_stage0_read` | CHANGED |
| function | `_stage0_real` | NEW |
| function | `_stage0_receipt_verdict` | CHANGED |
| function | `_stage0_source` | NEW |
| function | `write_freeze_manifest` | CHANGED |
| constant | `MODULE_NAME` | CHANGED |
| constant | `SCHEMA` | CHANGED |
| constant | `STAGE0_FROZEN_DEFECT_INCONSISTENT` | NEW |
| constant | `STAGE0_NO_RECORD_CODES` | NEW |
| constant | `STAGE0_RECORD_NOT_SUPPLIED` | NEW |
| constant | `STAGE0_RECORD_PIN_MALFORMED` | NEW |
| constant | `STAGE0_RULE` | CHANGED |
| constant | `STAGE0_UNREAD_RECEIPT_CODES` | NEW |
| constant | `STAGE0_UNREAD_RECORD_CODES` | NEW |

Every top-level function and constant not listed here is AST-identical to c2v001.

## Every v003g function

| Function | Status | v003g ast sha256 | successor ast sha256 |
|---|---|---|---|
| `_is_int` | IDENTICAL | `ce519eafdba718c3ac4032b823b3e43628ab5175189fb115a1cf8bd53b13fcb0` | `ce519eafdba718c3ac4032b823b3e43628ab5175189fb115a1cf8bd53b13fcb0` |
| `_is_real` | IDENTICAL | `1af5a36ecef37860745a4c6789b749803ac0f916efe8cffa06d38a041dcd8f12` | `1af5a36ecef37860745a4c6789b749803ac0f916efe8cffa06d38a041dcd8f12` |
| `_is_hex64` | IDENTICAL | `e6d1eea57b095419a5164081e1d88b171c81727725f36188eab5695f628e9427` | `e6d1eea57b095419a5164081e1d88b171c81727725f36188eab5695f628e9427` |
| `_sha256_hex` | IDENTICAL | `3a9f1b72a6a716b585ab4677624dfe22116e04156056b82412ae20eb5a76c1b1` | `3a9f1b72a6a716b585ab4677624dfe22116e04156056b82412ae20eb5a76c1b1` |
| `_safe_str` | IDENTICAL | `de622ec17471ded0f598ec22773fda20fc085a2ffe251430fd45bd91f16c815b` | `de622ec17471ded0f598ec22773fda20fc085a2ffe251430fd45bd91f16c815b` |
| `_safe_repr` | IDENTICAL | `85d8bb4e6545f7d05e472bb030788fc1a5298b4c371465f61c1988325277e6fd` | `85d8bb4e6545f7d05e472bb030788fc1a5298b4c371465f61c1988325277e6fd` |
| `_fail_closed` | IDENTICAL | `1a4bf74666d2a957fcfa95f8de31676c783c9614cb08f6dc2b4a10d9d6f64ff2` | `1a4bf74666d2a957fcfa95f8de31676c783c9614cb08f6dc2b4a10d9d6f64ff2` |
| `_canonical_bytes` | IDENTICAL | `3207813ca8daa80e56d9eb7fe7207b66d5f10ce1215acd560da610a012877326` | `3207813ca8daa80e56d9eb7fe7207b66d5f10ce1215acd560da610a012877326` |
| `_read_regular` | IDENTICAL | `c7a2f5309742a76f1a49a1473167b17d0d5bbd47fd9f90b4647a6ffb7362a5e2` | `c7a2f5309742a76f1a49a1473167b17d0d5bbd47fd9f90b4647a6ffb7362a5e2` |
| `_reject_constant` | IDENTICAL | `a27f4a60147ef6d1f1638db5b102616e51f1ace40ef49dfe01954d309c2ce027` | `a27f4a60147ef6d1f1638db5b102616e51f1ace40ef49dfe01954d309c2ce027` |
| `_parse_json_bytes` | IDENTICAL | `0959c4a7ca00bdc23652a6358c64b7970e5ba493a30bcc34061462a30cb18c3d` | `0959c4a7ca00bdc23652a6358c64b7970e5ba493a30bcc34061462a30cb18c3d` |
| `_plain` | IDENTICAL | `ad401af667b63a5fe908bf877882ffeed6023347eab5fc0716c78cd9887ebc01` | `ad401af667b63a5fe908bf877882ffeed6023347eab5fc0716c78cd9887ebc01` |
| `_scan_forbidden` | IDENTICAL | `ae2ee141c872f5c32aee5e6cb3abcc7519a7cf61115bd689ab0fe7ad7da4345c` | `ae2ee141c872f5c32aee5e6cb3abcc7519a7cf61115bd689ab0fe7ad7da4345c` |
| `_safe_scan` | IDENTICAL | `3ef1e8e0602643c10cec6a42313c7bb55a8dee05406f177de87ad985eb167e4e` | `3ef1e8e0602643c10cec6a42313c7bb55a8dee05406f177de87ad985eb167e4e` |
| `_dot` | IDENTICAL | `3f2d818b1115ed94a6a87d222b21a5600be83f9f1e78cda4e3e7dce0c5794467` | `3f2d818b1115ed94a6a87d222b21a5600be83f9f1e78cda4e3e7dce0c5794467` |
| `_median` | IDENTICAL | `4f56141786761f618922dcb43097374b04e56ac9f9a3473a09eb77c3bf382a12` | `4f56141786761f618922dcb43097374b04e56ac9f9a3473a09eb77c3bf382a12` |
| `_evenly_spaced_indices` | IDENTICAL | `abddbd765a4f0a148397b0acb7af1e24fafc8252ad59d854c28c323bc744d824` | `abddbd765a4f0a148397b0acb7af1e24fafc8252ad59d854c28c323bc744d824` |
| `_check_query_ids` | IDENTICAL | `b61612f1392d10dc42340456c7bce622fcde0610b1b6caac2b82071ec83ecea3` | `b61612f1392d10dc42340456c7bce622fcde0610b1b6caac2b82071ec83ecea3` |
| `_cap_reasons` | IDENTICAL | `ee273d43a06db6881b15e6a0ae65186a561cc7a53b8afab4b352bdaf143f8383` | `ee273d43a06db6881b15e6a0ae65186a561cc7a53b8afab4b352bdaf143f8383` |
| `_close` | IDENTICAL | `965a17af5e18d7039a2706736ff5f4ab64085cbbb7c3a01d79986aad4990eca8` | `965a17af5e18d7039a2706736ff5f4ab64085cbbb7c3a01d79986aad4990eca8` |
| `_now_utc` | IDENTICAL | `dea6c39674ce2d4f1c11ae5160215f3dca4f55b97907a19ddea8768f5ef0b910` | `dea6c39674ce2d4f1c11ae5160215f3dca4f55b97907a19ddea8768f5ef0b910` |
| `load_query_manifest` | IDENTICAL | `c085d5ca53b7bd0e921f2573729f34f201f5b06c1bac53ff0ec4bbfe4c2f563b` | `c085d5ca53b7bd0e921f2573729f34f201f5b06c1bac53ff0ec4bbfe4c2f563b` |
| `_build_spec` | IDENTICAL | `5653a62c475f2b5b952e9c98ac108288f80778e38258c6f2c5ca65e1bd037b79` | `5653a62c475f2b5b952e9c98ac108288f80778e38258c6f2c5ca65e1bd037b79` |
| `_spec_from` | IDENTICAL | `4aaa598782fa04603d6b5e1248e586a980981befc843c6e5f4b55407ab77e757` | `4aaa598782fa04603d6b5e1248e586a980981befc843c6e5f4b55407ab77e757` |
| `make_freeze_coordinate_spec` | IDENTICAL | `dd9212436314b965196ca43e48d850f8445c086cbcb8dbab0b0147bdfd72bcc2` | `dd9212436314b965196ca43e48d850f8445c086cbcb8dbab0b0147bdfd72bcc2` |
| `apply_coordinate_mode` | IDENTICAL | `47c55f26895d88da74bcf88a05d7ede3620768647efd8b11c8c3a201af54b82a` | `47c55f26895d88da74bcf88a05d7ede3620768647efd8b11c8c3a201af54b82a` |
| `_mode_labels` | IDENTICAL | `1b1bbedba3607ebe728330b244484df51d577f8a40955e3d7d67afdce3785d87` | `1b1bbedba3607ebe728330b244484df51d577f8a40955e3d7d67afdce3785d87` |
| `_check_run_coordinate_binding` | IDENTICAL | `42263517dd0c60a6c3b614f4713e40e517be01763322ee8596df64188991a7fd` | `42263517dd0c60a6c3b614f4713e40e517be01763322ee8596df64188991a7fd` |
| `_engine_coordinate` | IDENTICAL | `d1561badd0bd1da9f2d38d018155cfbfe8393ddf8c223c21efba676ee074a531` | `d1561badd0bd1da9f2d38d018155cfbfe8393ddf8c223c21efba676ee074a531` |
| `_x_bounds` | IDENTICAL | `b73b42d27edf36a67b14ebcfd45cdd632c1e703826794fa53a14a90d8c363d0f` | `b73b42d27edf36a67b14ebcfd45cdd632c1e703826794fa53a14a90d8c363d0f` |
| `_theta_engine_from_u` | IDENTICAL | `f62f020231ee8fcef7a37983cd3bb3130f26ad9dbe4e5e680158ccb0ef1e164b` | `f62f020231ee8fcef7a37983cd3bb3130f26ad9dbe4e5e680158ccb0ef1e164b` |
| `_u_of_trial` | IDENTICAL | `d3eaa6f7c00825467fd7d6f8699eb84049a0f532e5dd1a26526750cc9ea421a0` | `d3eaa6f7c00825467fd7d6f8699eb84049a0f532e5dd1a26526750cc9ea421a0` |
| `_theta_ngc_from_engine` | IDENTICAL | `60d13ce0e56f545c15f1bec0df7294440c6dcd22ab3ffea7a7f6b481a28708d1` | `60d13ce0e56f545c15f1bec0df7294440c6dcd22ab3ffea7a7f6b481a28708d1` |
| `_bind_u` | IDENTICAL | `5fd892bfc93c4dcbd2d1756f1dedef85bb531cb3e51d6547af44adacde8c0d2c` | `5fd892bfc93c4dcbd2d1756f1dedef85bb531cb3e51d6547af44adacde8c0d2c` |
| `_bind_theta` | IDENTICAL | `f160fd7b9f7be6e857ab5aa6506874d2f2ce8b40793bf521f36bf7268bf70ed9` | `f160fd7b9f7be6e857ab5aa6506874d2f2ce8b40793bf521f36bf7268bf70ed9` |
| `_resolve_exploration` | IDENTICAL | `2a1e06e3dd1ee7e5e822baf35a5f7f12bc6e28a869c0da392d50774fa7fa4cc9` | `2a1e06e3dd1ee7e5e822baf35a5f7f12bc6e28a869c0da392d50774fa7fa4cc9` |
| `_bind_index_list` | IDENTICAL | `a2a698ab6137a7f5bebaeef6d4dba89f70d53f11b54071ad645efea471f74897` | `a2a698ab6137a7f5bebaeef6d4dba89f70d53f11b54071ad645efea471f74897` |
| `_centroid` | IDENTICAL | `a2ef846bdf4fb298d747b87eb51ff07332d6526a7bc4ed99af41609c26b85fe2` | `a2ef846bdf4fb298d747b87eb51ff07332d6526a7bc4ed99af41609c26b85fe2` |
| `_selection_plan` | IDENTICAL | `43f1e5d821ae33802bd48406515099e7c5fb78fa42f8cf55f9e2b845e77d1e30` | `43f1e5d821ae33802bd48406515099e7c5fb78fa42f8cf55f9e2b845e77d1e30` |
| `_reclassify_admitted` | IDENTICAL | `686b3033cc2b0919dd5b8cb4eed69b0b3d6fb47d420afe516a3ed63ec172dc45` | `686b3033cc2b0919dd5b8cb4eed69b0b3d6fb47d420afe516a3ed63ec172dc45` |
| `_region_from_bytes` | IDENTICAL | `e13841c8975c14dcec29cc66060b37a9e8a491e6ea2a698dc5434ed9dcbd1e64` | `e13841c8975c14dcec29cc66060b37a9e8a491e6ea2a698dc5434ed9dcbd1e64` |
| `_region_of` | IDENTICAL | `57f9105178f7ae6604afc5823b54d3760c799e81c597b030c9ab8286f9989ad3` | `57f9105178f7ae6604afc5823b54d3760c799e81c597b030c9ab8286f9989ad3` |
| `_fingerprint` | IDENTICAL | `33153aa40bdf5ec3fb415a98d18d6414af416d0afe7b23b2ee1bc7ec6ee63c4f` | `33153aa40bdf5ec3fb415a98d18d6414af416d0afe7b23b2ee1bc7ec6ee63c4f` |
| `select_representative_points` | IDENTICAL | `15966d2f1ef817fe5f53fd4ba56c5cfca336fa2d6bab18032bdd41cf110e6c64` | `15966d2f1ef817fe5f53fd4ba56c5cfca336fa2d6bab18032bdd41cf110e6c64` |
| `_root_target_screen` | IDENTICAL | `ec78c9b2811ac7922a360bc082745790f67167a67b16c17dcb8b0f31012b5242` | `ec78c9b2811ac7922a360bc082745790f67167a67b16c17dcb8b0f31012b5242` |
| `_root_pinned_document` | IDENTICAL | `e92c84739c7fc821036abe8b3bd5a27ac8dcb89dc29176c927b5b8b8641a4fb5` | `e92c84739c7fc821036abe8b3bd5a27ac8dcb89dc29176c927b5b8b8641a4fb5` |
| `_exact_string_list` | IDENTICAL | `eeffd2eb9ef8afd55f52160a0b238b47e010a00a0bec56a02b151ccbc6583c0e` | `eeffd2eb9ef8afd55f52160a0b238b47e010a00a0bec56a02b151ccbc6583c0e` |
| `_root_slots` | IDENTICAL | `4f3c83889d117ae302ccd59a976b185ee3463187323a92d9fe7a0e9658b0eaeb` | `4f3c83889d117ae302ccd59a976b185ee3463187323a92d9fe7a0e9658b0eaeb` |
| `_registered_gl_nodes` | IDENTICAL | `7ca371be6169038547a3f970e927543849ed99a3dc2688e2608f602c65220ea7` | `7ca371be6169038547a3f970e927543849ed99a3dc2688e2608f602c65220ea7` |
| `_load_row_roster` | CHANGED_STAGE0 | `3dd87e8a647b981eff9c61d0eeb3a04fa7badb2fba9b88dfcf199af09c20a6a2` | `3cefa11fa2e168342b2d239847fc6e9eb262f25334798b76941df1653a68bc5b` |
| `_row_contract` | IDENTICAL | `81e5462f0a90dd637599b492b5543130bc8faf1a1143ed434b2fc359fd07f58f` | `81e5462f0a90dd637599b492b5543130bc8faf1a1143ed434b2fc359fd07f58f` |
| `_authorized_row_registration` | IDENTICAL | `48cc39c2e91e12750efb139b237bb68370b03f954e0c9fa75e095f3b6da4ef18` | `48cc39c2e91e12750efb139b237bb68370b03f954e0c9fa75e095f3b6da4ef18` |
| `_root_result_rows` | IDENTICAL | `c9925da287e2e69b07c2577a1139bcd31570ac7614aa8c86c467a2eb93a755aa` | `c9925da287e2e69b07c2577a1139bcd31570ac7614aa8c86c467a2eb93a755aa` |
| `_root_frozen_rows` | IDENTICAL | `b73fdf9935b701c4ea556550b08c9a5443e1ae561907a629006f7cf75bd7431a` | `b73fdf9935b701c4ea556550b08c9a5443e1ae561907a629006f7cf75bd7431a` |
| `_root_rosters_for_alternatives` | CHANGED_STAGE0 | `66fe04f4038f9e8165299163f8151baef725fdb3276438d32fa56bdf11940d69` | `084a8e18b5780afc6ce8af3a23e1167a1d823878b1bd86a7972970302e6429ec` |
| `_root_manifest_check` | IDENTICAL | `cd32a75a68c0ec6191e1aaf33fe2177a0d0020e0de981fc6f170756b0266ef82` | `cd32a75a68c0ec6191e1aaf33fe2177a0d0020e0de981fc6f170756b0266ef82` |
| `_invalid_registration_ok` | IDENTICAL | `2f2c98fd1ce8f8b306a8ae048ee29a637da4094fbc7a1c95b679cb310470e39a` | `2f2c98fd1ce8f8b306a8ae048ee29a637da4094fbc7a1c95b679cb310470e39a` |
| `_registered_rows_ok` | IDENTICAL | `953031327b6c6cd6d19b1306fe8a7972c5ad80655167ae07ce478625582fc7b1` | `953031327b6c6cd6d19b1306fe8a7972c5ad80655167ae07ce478625582fc7b1` |
| `_member_contract_valid` | IDENTICAL | `0411ce069564d12b509430169fe65cd7af129bffeb6517e72283f82175e74da3` | `0411ce069564d12b509430169fe65cd7af129bffeb6517e72283f82175e74da3` |
| `_v010_preflight` | IDENTICAL | `9d4b6688c267b108f1ccfb505bfd833f3bfdd942e3ca4fcdf0a10cce41f362f1` | `9d4b6688c267b108f1ccfb505bfd833f3bfdd942e3ca4fcdf0a10cce41f362f1` |
| `_call_forward` | IDENTICAL | `b1e96d78f118e8694d91eb0697502b4392d622f22cd1ee2d3160566591f37d9e` | `b1e96d78f118e8694d91eb0697502b4392d622f22cd1ee2d3160566591f37d9e` |
| `_pointwise_envelope` | IDENTICAL | `2aed5fb691609774b12480dc6aa793101002d74dce292b4e80b3ede99698150d` | `2aed5fb691609774b12480dc6aa793101002d74dce292b4e80b3ede99698150d` |
| `evaluate_envelopes` | IDENTICAL | `6340fa75dfe13cc81b991e91cd191adc540c1fc81df83b595bf68cc33c2cc646` | `6340fa75dfe13cc81b991e91cd191adc540c1fc81df83b595bf68cc33c2cc646` |
| `_reference_ranking` | IDENTICAL | `98647f64d3c87504cc7e1e6d74d4e585a916f458c9cd88e154e03469ca17f8ec` | `98647f64d3c87504cc7e1e6d74d4e585a916f458c9cd88e154e03469ca17f8ec` |
| `select_reference_member` | IDENTICAL | `a0f343237c3aa05e072ba65c9e7c6fde12b9eb73a427639bde693e5ad108042e` | `a0f343237c3aa05e072ba65c9e7c6fde12b9eb73a427639bde693e5ad108042e` |
| `_edge_t` | IDENTICAL | `c6306183e71f6bc807284d7d3dbcff661e6e0211ae04d5c4aa699e67c669a0c4` | `c6306183e71f6bc807284d7d3dbcff661e6e0211ae04d5c4aa699e67c669a0c4` |
| `_bind_null_rule` | IDENTICAL | `400be84d2be4ea66eb37724e37925ab073b90e6e98b04558cdf5916ad27074de` | `400be84d2be4ea66eb37724e37925ab073b90e6e98b04558cdf5916ad27074de` |
| `_sensitivity_plan` | IDENTICAL | `f481231a7de8f16f1d7bc9ee735558b40fcdb694a5430534d5f574ebbb9f3e19` | `f481231a7de8f16f1d7bc9ee735558b40fcdb694a5430534d5f574ebbb9f3e19` |
| `_sensitivity_summary` | IDENTICAL | `3380b17a88c0d4bf6997e894a4cef99ad68b14b05251474535e82a0036cb7342` | `3380b17a88c0d4bf6997e894a4cef99ad68b14b05251474535e82a0036cb7342` |
| `evaluate_sensitivity` | IDENTICAL | `6f62dd4eb3c650b415c10fa8607b8d1e4faebf6f65598e499b4d827a0b7cb8b9` | `6f62dd4eb3c650b415c10fa8607b8d1e4faebf6f65598e499b4d827a0b7cb8b9` |
| `_bind_alternatives` | CHANGED_STAGE0 | `728cd90d6414ad957d1c8057c796cb4eccc57740e6622f23fd9c48c5a0c5fcac` | `0b89082898595f2df6fc7fdcd49dddaba47d980d31728e3188288f0b7008aa66` |
| `_incomplete_reasons` | IDENTICAL | `614898166ca53b0946ff98e968183614a8079ee3f668c44bacf726abdbf53aac` | `614898166ca53b0946ff98e968183614a8079ee3f668c44bacf726abdbf53aac` |
| `_conditional_on_trial` | IDENTICAL | `e00767702834e6befc22aa4ef0164d7ce5931bb236f9267a1628b3e9eeaa52c7` | `e00767702834e6befc22aa4ef0164d7ce5931bb236f9267a1628b3e9eeaa52c7` |
| `_is_list_of` | IDENTICAL | `744dc146e5cb1e2a6b6494b4b1e546c13d1b0d4e0990bf2b40c630598afa09ae` | `744dc146e5cb1e2a6b6494b4b1e546c13d1b0d4e0990bf2b40c630598afa09ae` |
| `_opt_real` | IDENTICAL | `7b3ecfab067d15996fcde8edd6be095ab98d5b48318ba3dbc733076ff2b2c2d1` | `7b3ecfab067d15996fcde8edd6be095ab98d5b48318ba3dbc733076ff2b2c2d1` |
| `_validate_members` | IDENTICAL | `8adf938273303b44687772a4bac3e113b54e5fd749412b7dca90fdcf9c43e6e9` | `8adf938273303b44687772a4bac3e113b54e5fd749412b7dca90fdcf9c43e6e9` |
| `_validate_member_eval` | IDENTICAL | `82bdaa24eaba6d3006f259c4dd20710115e174881fd65c0d21c4219e53cb6410` | `82bdaa24eaba6d3006f259c4dd20710115e174881fd65c0d21c4219e53cb6410` |
| `_validate_envelope` | IDENTICAL | `53516f9d4822af00f4693082933f87045fa9e04545da916b6c4a995b35c1329f` | `53516f9d4822af00f4693082933f87045fa9e04545da916b6c4a995b35c1329f` |
| `_validate_admitted_region` | IDENTICAL | `ea3df90943366d04cfd842365ab9cddfc9ff27bccffd154d532bc53b7bef83c1` | `ea3df90943366d04cfd842365ab9cddfc9ff27bccffd154d532bc53b7bef83c1` |
| `_identification_rule_reasons` | IDENTICAL | `a9e8df10784f78c66bcc971ee08c942ea9caa495d82e26d34be278eaa82f6cd0` | `a9e8df10784f78c66bcc971ee08c942ea9caa495d82e26d34be278eaa82f6cd0` |
| `_record_identifiability_reasons` | IDENTICAL | `f80bc8eebedd4a5ba8a80a7c538c65cbae22e6edcb84192c45d715c9b18c252a` | `f80bc8eebedd4a5ba8a80a7c538c65cbae22e6edcb84192c45d715c9b18c252a` |
| `_validate_reference` | IDENTICAL | `476610beefa8d1c2912e71f07bffc83f3cd58b87ebeee51c9abc9dcf0dad52d6` | `476610beefa8d1c2912e71f07bffc83f3cd58b87ebeee51c9abc9dcf0dad52d6` |
| `_validate_sensitivity` | IDENTICAL | `1d5d53b299bb5a96808d2944ff0b097d6b5fac564ad2a316064d649d5f83c496` | `1d5d53b299bb5a96808d2944ff0b097d6b5fac564ad2a316064d649d5f83c496` |
| `_check_slot_geometry` | IDENTICAL | `0490cbe5cf241f3151823409cf0d91eb196d84123c600962ba5ef7d355d4bd7b` | `0490cbe5cf241f3151823409cf0d91eb196d84123c600962ba5ef7d355d4bd7b` |
| `_headline_conditions` | IDENTICAL | `fcbc73a722f28dc54729461e41f5c307cf0c1f65e7eb0d7091de848245c90df4` | `fcbc73a722f28dc54729461e41f5c307cf0c1f65e7eb0d7091de848245c90df4` |
| `_validate_manifest_structure` | CHANGED_STAGE0 | `2e57985b6f5684cf4576b8e878ac7c9c18479c061dba483090aa3070c89c31d0` | `90fe71d92d7446495c871e8a00d02d78981c52beb78565ef44588d1e54210ec4` |
| `_validate_manifest_impl` | IDENTICAL | `8cc6352e125681b244f8567a21d0b236a90b61500da34d58ed6c2f320374c0fa` | `8cc6352e125681b244f8567a21d0b236a90b61500da34d58ed6c2f320374c0fa` |
| `_query_ids_sha256` | IDENTICAL | `6df1d14e89384e75ac99e18f079ceabc52e933679348c65d0cb85093b46c27c6` | `6df1d14e89384e75ac99e18f079ceabc52e933679348c65d0cb85093b46c27c6` |
| `_validate_input_bindings` | IDENTICAL | `72823b28057d2872a784994de01bd2788891a6c0a2a6866d7396abf55da915ea` | `72823b28057d2872a784994de01bd2788891a6c0a2a6866d7396abf55da915ea` |
| `_check_calibration_record` | IDENTICAL | `1885f947739e203ed49f467cf39b9b22207f6528cd43013a22a8926dc68413fb` | `1885f947739e203ed49f467cf39b9b22207f6528cd43013a22a8926dc68413fb` |
| `_record_status_reasons` | IDENTICAL | `89b17be393306467ab64c6330bc03ef5b995195f299dbc1f705d09e9b0eae694` | `89b17be393306467ab64c6330bc03ef5b995195f299dbc1f705d09e9b0eae694` |
| `_member_key` | IDENTICAL | `83495088a99de97b642ca75532edbbef50956c57916c9b5596e8304d7994f676` | `83495088a99de97b642ca75532edbbef50956c57916c9b5596e8304d7994f676` |
| `_check_record_binds_selection` | IDENTICAL | `b9e9152b5ee845e9f9e34ad2f842f569eb1ba37d8c8d1279d30bf106e431b99e` | `b9e9152b5ee845e9f9e34ad2f842f569eb1ba37d8c8d1279d30bf106e431b99e` |
| `_member_order` | IDENTICAL | `55925a06fb08eca140db4d162f855063cceee81e2b9bdfccd5ab913289d89e10` | `55925a06fb08eca140db4d162f855063cceee81e2b9bdfccd5ab913289d89e10` |
| `_pin_files` | IDENTICAL | `b531c0b744dbc0e38f1e1cb7757dc26ec9c64c4382547e13218f7743352819ec` | `b531c0b744dbc0e38f1e1cb7757dc26ec9c64c4382547e13218f7743352819ec` |
| `_member_eval_record` | IDENTICAL | `ec04373e5c080417e02fc4cef09e10459b63c3be5dc4e038f40c2b7bd23f8786` | `ec04373e5c080417e02fc4cef09e10459b63c3be5dc4e038f40c2b7bd23f8786` |
| `write_freeze_manifest` | CHANGED_STAGE0 | `e3b3a3a0e9ef8610696971e5b0a4df6787bcfcf463f3d8460cb4561df31e7b59` | `be7f70465b3a1f2a955b4b7201b1a89ffa6d97b129ccf29ed5352e1ec33a5895` |
| `_verify_bytes` | IDENTICAL | `590d8eb1cb9e66ad05018bf6c1bbe124996e5cc365e6e96a78e448edf7a67a51` | `590d8eb1cb9e66ad05018bf6c1bbe124996e5cc365e6e96a78e448edf7a67a51` |
| `_verify_impl` | IDENTICAL | `eb78991843b27d26b61592cc2db7e84f53113243d118891d55e0eed22a565071` | `eb78991843b27d26b61592cc2db7e84f53113243d118891d55e0eed22a565071` |
| `verify_freeze_manifest` | IDENTICAL | `b8f6a1eb4fc8137134bf95ae8b0b2753b16104d9b1c33ab51ccd350dfcd3cb57` | `b8f6a1eb4fc8137134bf95ae8b0b2753b16104d9b1c33ab51ccd350dfcd3cb57` |
| `_verify_registration_impl` | IDENTICAL | `4190a74af7e95b375681b6839f3de173eb88c3e7515a16d34fc14a548533872c` | `4190a74af7e95b375681b6839f3de173eb88c3e7515a16d34fc14a548533872c` |
| `verify_registration` | IDENTICAL | `0041f6f834970aa82cb35132c02bd5626d2761a413ea23cbf80c2bbb0da869c5` | `0041f6f834970aa82cb35132c02bd5626d2761a413ea23cbf80c2bbb0da869c5` |
| `_ladder_row` | IDENTICAL | `60606889fca27611eeed15e965dcd7da9e0671a98523a0b61a1f193728752d37` | `60606889fca27611eeed15e965dcd7da9e0671a98523a0b61a1f193728752d37` |
| `_score_members` | IDENTICAL | `24249121df4d63e665236e1a5d631d731628e3816a98128a120d3f9ac6001d28` | `24249121df4d63e665236e1a5d631d731628e3816a98128a120d3f9ac6001d28` |
| `_alternative_score_scope` | CHANGED_STAGE0 | `9f59972c483a0e5976fc3c0766d6f5ac32834419e1a3d9c05a0611ce3a44e4fa` | `1d4c7f4a7a044ff206fbb09ac1bcfe2f45b2e8b59b664374c436532b7b6d4295` |
| `_score_members_on_rows` | IDENTICAL | `7c3e639ff3a5685c73bb5eb16e21dfc2957bda5a71a787a9f8592f1deb7839f1` | `7c3e639ff3a5685c73bb5eb16e21dfc2957bda5a71a787a9f8592f1deb7839f1` |
| `_distribution` | IDENTICAL | `9352ed1b7b1b28198451ec46caac2565c5d73926f49b3774768e9df96a1fd36a` | `9352ed1b7b1b28198451ec46caac2565c5d73926f49b3774768e9df96a1fd36a` |
| `_band_rows` | IDENTICAL | `97c475b82621f1c1b1b90ab370c00b9f2d9492b4e83b0edf484a09ae26a78e4e` | `97c475b82621f1c1b1b90ab370c00b9f2d9492b4e83b0edf484a09ae26a78e4e` |
| `score_after_freeze` | CHANGED_STAGE0 | `8364aab9a824676bfa2d531e056c92e055e140c23eae1f6a40e6cd7c156875b5` | `f737f4aba995c4908b2384be2c01da8b8d2494bb2896b8293ca8e1efb3293702` |
