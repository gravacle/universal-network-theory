# Candidate r2 source review: D-04, R-04 and A102

`date -u`: Sun Oct 18 21:33:46 UTC 2026

**Source-scope verdict: PASS WITH NOTE; 0 demonstrated blocking findings in this assigned subset.** This is a candidate source snapshot, not final-package, seal or launch approval. The separate D-05 coverage finding is owned by the entry/driver review lane and is not counted here.

TESTED byte custody: the actual r5 prereg pin joins to case block76309ae3, BUILD_V00794bc05a5 and selected template1b406591. All15 supported BUILD source hashes match bytes, with unique paths. The template's launcher861bba68 and guard294cb776 are exact allowlist entries. The target-free case block has11 cases, including10 tail cases with registered gas M_s128 and a common driver list, and route_a_mode parallel8. The full pins and inventory are in D04_R04_SOURCE_AUDIT_CX3V001.json. No referenced run directory was opened.

FORMAL source support for D-04: tool3 reads the case block only from binding_inputs.case_block, verifies the exact pin and bytes, activates the byte-pinned driver BUILD through the reviewed comparator, and validates the strict case block against that active build. Under r5 it requires the cascade addendum pin and passes it through. BUILD_V007, its15 source entries, the bound plan's driver/frozen pins, exact launcher/guard selection, template pin,10 call spec pins, and binder command are checked. A separate post-SEAL_RECORD API verifies the admission config, exact allowlist, and launcher/guard without demanding an admission config prematurely.

FORMAL source support for R-04: B6 bodies must be strict JSON with the expected blinded schema, test_mode false and the sealed comparator's full script hash. Route mode and C5H validity-case keys are checked, with number screening. B7 key-map, NEW-item and raw-custody inputs have explicit schemas and typed fields; the selected IMPL is byte-pinned and must name the reviewed comparator hash, and custody requires Z2, the selected driver, positive integer stage totals, complete successor counts and PASS. These checks are metadata/schema bindings; they do not independently recreate the scientific evidence quoted by those inputs.

FORMAL A102 support: json_or_text uses duplicate-key/non-finite hooks and parse_int=str; only JSONDecodeError permits text fallback. Driver-check and driver-BUILD printing paths translate other ValueError into typed refusal. The cascade addendum retains the ordinary numeric parser but catches every non-syntax ValueError as refusal; an oversized otherwise valid integer can be rejected, but cannot trigger the old JSON-to-text admission bypass.

**Note B8-GUARD-PARITY (source observation; runtime UNTESTED here).** The admission-config checker does not validate SEAL_RECORD.sealed_by or its driver/frozen_addendum pins. The actual guard_v008 does. A malformed or repinned seal could therefore produce checker PASS followed by guard refusal; this is a readiness-check mismatch, not a demonstrated launch bypass. The runtime lane was asked to test this narrow case. The stated D-04 fix specifically requires the config to name launcher/guard exactly, which is implemented.

Sixteen source obligations are mapped to exact functions and line locations in D04_R04_CHECKLIST_CX3V001.json. No candidate module was imported or executed in this source lane. UNTESTED here: synthetic refusals (separate lane), author148-case results, final README/procedure/manifest completion, real sealed inputs, admission, binding and launches. No source file was changed.

Byte SHA256 citations:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/contracts/D04_R04_SOURCE_AUDIT_CX3V001.json` — `8bf7400bff508613d8b89fd5d12ca75959c1d40676e43e3dcb4a8dd216799506`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/contracts/D04_R04_CHECKLIST_CX3V001.json` — `120b5ace951d4510c546eb1a2ce05b14ebe48aa8f0caf0e08362b704d7091402`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_rehearsal_c4/run/GAPS_C4V001.md` — `566b206635d7ba160ab602842c64e7f1ffd38878c6bf0d7ed3721faffcc3543c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_rehearsal_c4/refute/REFUTE.md` — `7be3fb347310040a1fc806b8886c85cb17e631cb9933aed6261cd958499c3eda`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/producer_guard_cx1v008.py` — `294cb7760679b883a62fb3117dc75e91231b2f173bcec65983e6762371ea0731`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/build_seal_record_c4v002.py` — `4192983d262e2a27a3d9c90681b6ee66a90c901bfe2f99a7dce2349bc8c5de52`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/check_frozen_addendum_c4v002.py` — `06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/check_sealed_compare_c4v002.py` — `aebb7b731a800e558b13a5f290c7fac062183cb9ba092af45df4e6bda1f390cf`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/check_slot_fill_c4v002.py` — `806733fb18e167275a1de62ebc9433fecf632cc16393933801fd4c9e53cddffb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/print_driver_build_record_c4v002.py` — `fde0b26e7ea26d4ad15213cc9c3115a807179616e0e155037c97d2179db7a673`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/seal_common_c4v002.py` — `f41b0fca51a95387577839e52308a2dc6ccb79b1e6b9283f389b54c7f348dc10`
