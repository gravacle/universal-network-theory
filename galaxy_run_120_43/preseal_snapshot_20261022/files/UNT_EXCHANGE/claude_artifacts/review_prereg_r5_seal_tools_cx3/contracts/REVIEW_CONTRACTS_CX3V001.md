# 0628 seal-tools v002 contract audit

`date -u`: Sun Oct 18 21:15:58 UTC 2026.

TESTED: read-only source/requirements extraction. UNTESTED: substantive v002 successor behavior. Current blocking dependency count: 1 (substantive tools not yet present); no new successor code defect is asserted from an unfinished directory. Only fence/copy/runner utilities currently exist. No tool, fence selftest, synthetic consumer, compare, seal, binder or launcher was executed.

- **D-01**: Recognize DOUBLING ddo_gas_M_s as the DDO gas resolution and require128. Preserve conditional NGC M_s semantics; do not invent an unconditional NGC field requirement. R13/A73 explains alias wording.
- **D-04**: Byte-verify prereg binding_inputs.case_block {path,sha256}; a seal-slot substitute is insufficient. Pin/check r5 CASCADE_MAP_R5_ADDENDUM, propagate custody into builder, and identify an enforced exact launcher/guard admission-config check at its post-SEAL_RECORD stage. Tool3 text-of-record must bind the r5 prereg.
- **D-05**: Every entry A82 through the actual freeze needs an honest revised/no-change decision with reason. A83 cannot be omitted; A101 is the minimum upper entry in0628, not a license to omit future frozen entries. README/checklist/builder must preserve decisions rather than blanket --covered-later A82 or fixed boilerplate.
- **D-06**: Per R06, add explicit owner/creation step for the driver BUILD record consumed by PIN_DRIVER_BUILD_RECORD, and specify JSON artifacts for key-equivalence map, NEW-item dispositions and raw successor custody. Existing A1/A5/A10 already cover conceptual preparation; do not falsely demand duplicated conceptual steps.
- **D-07**: Before indexing, validate slots/prereg containers and the five mappings compare_reviewed_source,frozen_addendum,driver_build_record,driver_check_record,producer_registry. Invalid forms must yield typed refusal JSON and exit2 through CLI, not TypeError or raw traceback. Preserve non-pin-source tamper refusal and exact five-pin-only changes.
- **D-10**: Author-promised related closure: frozen path must equal path_to_be, or deviation must be explicitly authorized/recorded; matching basename alone is insufficient.
- **R-04**: Author-promised related closure: B6 blinded outputs have correct schema,test_mode=false,script_sha256 equal to sealed compare; B7 keymap/NEW dispositions/raw-custody inputs have required schemas. Do not run real gates/validity/seal/bind while reviewing.
- **R-10**: Author-promised related closure: B7/SEAL_RECORD key-equivalence map equals the case-block map.

D-01 and D-04–D-07 are the exact requested closure set. D-10/R-04/R-10 are explicitly promised in the author PARTIAL and affect custody; this is not authority to execute historical reproduction commands or old queues. The runtime lane received the negative-case checklist and owns synthetic execution after candidates land.

Byte-derived citations:

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0628_2026-10-18_codex3_next_prereg_r5_tools_v002_review.md` — `9586ad51802e8f5cdce79e35d09c29b331f8381a6f4e0cfb641bee98fe9c0628`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/PARTIAL.md` — `50c27c8d0f1032811b0d1e2ea7049d6a0d4c7cfc8cf523533f4176e54cb40858`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_rehearsal_c4/INDEX_SEAL_REHEARSAL_C4V001.md` — `2d3a636e57716a312cf6a2bf0c32afbb0d45e9d0bb614bdeea98a484687466bd`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_rehearsal_c4/run/GAPS_C4V001.md` — `566b206635d7ba160ab602842c64e7f1ffd38878c6bf0d7ed3721faffcc3543c`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_rehearsal_c4/refute/REFUTE.md` — `7be3fb347310040a1fc806b8886c85cb17e631cb9933aed6261cd958499c3eda`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/tools/fence_c4v001.py` — `f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/tools/fence_c4v002.py` — `c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/tools/make_fence_c4v002.py` — `a108c8ac718e0468a3ccc211f700c8950102aa3ea94d4867bb3f0efe7d551803`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/tools/run_fenced_c4st2.py` — `fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/tools/xwrite_c4st2.py` — `4fc279a3b1c6c5bcfd180c587b111d47266c5e7366c6d27c002c681229e10326`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools/check_sealed_compare_c4v001.py` — `b339a8f6051ffe7a596179216ec3ba6e103a14356ed13befa51cf3529110b3ed`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools/check_slot_fill_c4v001.py` — `7f3cf07da0d92fef0a1cc592cb644eafca2737e90b917e83ea9ffa5fc367187b`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools/build_seal_record_c4v001.py` — `3091fc2afa2e16f74d8c634d8605205c792788924f078b5aae806351a1d18c70`.
