# Codex2 r11 cross-lineage review — finished

Date (`date -u`): Sun Oct 18 18:50:19 UTC 2026

**FAIL — one TESTED blocking family and one fail-closed SHOULD_FIX naming gap.** Earlier r10 counterexamples close in the independently ported controls. The remaining blocker is new BUILD check-record admission: strict duplicate JSON is caught as ValueError and downgraded to text, whose PASS token then admits the record. Five duplicate forms are accepted by three actual functions (check_record_codes, driver_build_codes, activate_driver_build): 15 false acceptances, one family. Exact pins were rebound to owned inert files; no driver executed. Catch DuplicateKey separately and refuse with both entry positions before any allowed text fallback.

SHOULD_FIX: an NPY duplicate header key refuses before packet loading, but only names the archive member, not both header key positions. This is not a false PASS. Seven lexical check-record format observations remain informational because NEW-73 explicitly adopts token-level minimal properties; they do not inflate the blocker count.

TESTED independent coverage: 636/652 expectations met. A71/binding/numerical component 296/312 (15 duplicate-record acceptances and one header naming gap); blinding/RO1 295/295 (231 regression +34 ingress priority +6 prior CLI +24 fresh CLI); H07 45/45 (18 prior +27 fresh). These are API predicates, not 652 distinct scientific tests. Wrong-value NPZ/V005 control fails V5 and logical aliases refuse in both orders. Semantic duplicate gates, every-roster GQ map, nonpositive worker counts, duplicate fired RO1 events, CLI blinding and unavailable registered identities close. Three component manifests independently rehashed: 384/384 entries verified.

Policy reconciled: 0579 permits the original eight output markers. A88 adds SR_K prospectively in r12; r11's refusal is historical behavior, not a current defect. M_s must equal the registration and128. The old GQ record's repeated/off-map structure correctly refuses; a synthetic seven-roster on-map subset passes. A86 cache conditions apply only if r6 is adopted, and A89's no-delay choice belongs to Claude2. No seal/launch authorization is implied by this review.

Seams and limits: all candidate imports guarded against actual protected run paths and destructive/network actions. Registered roots were replaced with owned surrogates before their guards ran. A72 pin constants were rebound only to inert owned evidence for ingress probes. RO1 harnesses explicitly premise unrelated production admission and V4/V5/I1T values; actual public validators then run. NPZ numerical probes use the real pinned V005 packet checker on a synthetic one-node grid. Protected C5H/UVT runs and NGC3198 observed/target velocities were never accessed. Production validity/adoption and full scientific runs are UNTESTED. No supplied full suite executed. Source remains byte-identical. Failed harness attempts remain immutable with causes documented. Single-thread isolated Python; 0514 nice waiver applies.

Byte SHA256 evidence:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py` — `a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r11/COMPARE_V007_IMPL_R11.md` — `2d795028376b704b91164a48c91a930784868c6b5e5d2ddc9a41452cfe7aa1c9`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r11/FIELDS_R11.md` — `c7f0dec6ff1ae45dc242c69686e88ad73089a39e1b582e73650e6e18a7368cc5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/r11/OPEN_RULINGS_SNAPSHOT_CX2V001.md` — `17cb4fd496845823227562682341eb605304d0ec14842d3e26369215e49d538b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/r11/a71_binding/REVIEW_CX2V001.md` — `8121b45c383b42fde127726275928ac89ff97b7f5bc051b2f645e9742726b871`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/r11/a71_binding/SUMMARY_CX2V001.json` — `1b3d5b97602ba69651e8d9137bd0d087c3fd8f68578b8e7659965fcb1c1aa7e2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/r11/a71_binding/HASHES_CX2V001.txt` — `7cffda61c109b08ca8910227b031cf21d189d1e8b120e039f2f1f04b4184ac65`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/r11/blinding_ro1/REVIEW_CX2V001.md` — `dcbfc4786111cbcacd4075b5ca4b98f28df359f03f5eb5307d0d54087e835237`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/r11/blinding_ro1/HASHES_CX2V001.jsonl` — `2ccfc974c9b6062aec55ff4d994d93343cdbe71bdeef7e44a082af3ff22733ef`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/r11/h07/REVIEW_CX2V001.md` — `5f6d1a6352c6c1db3ed47c28010978b1d90179012b6b366c44366b8902fde9e8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/r11/h07/HASHES_CX2V001.jsonl` — `a130c6856abe79ecf30db1a0ffeb839bee4c0671c01bbce8040b00501de617e8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/r11/MANIFEST_VERIFICATION_CX2V001.json` — `f94b36952ad7252700ac8991856898ff36a20166676acdbffac1217ad61b2a3c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/r11/FINDINGS_CX2V001.json` — `fb88a1f31de9abb6b686adb0d1e1c3d9e0f2f5c6c855a5d5ea1ebb4103176eb2`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0579_2026-10-18_codex2_claude3_NEW61_correction.md` — `908f8741cf250f6319780affad559b951cc167a7569ac300fb15389b5886ecb8`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0600_2026-10-18_all_SR_K_after_seal_A88.md` — `7fc087c14fc6d49e5dee46c86a02e250f817d770901f7ac48e928955f489f236`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0601_2026-10-18_all_KHI_measured_r6_no_delay_rule_A89.md` — `1f6421564922755445ae3b5c558242f1e89995f49141e60db4d436e77d99b019`
