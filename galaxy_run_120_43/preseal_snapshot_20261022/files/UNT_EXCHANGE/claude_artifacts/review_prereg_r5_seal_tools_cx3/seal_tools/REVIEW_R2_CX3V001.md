# Seal tools v002 selected r2: independent bounded review

date -u: Sun Oct 18 21:35:36 UTC 2026

**FAIL: one BLOCKING D-05 closure finding, plus one nonblocking SHOULD_FIX admission-readiness mismatch.** The selected handoff is the README's r2 tool set. All six source pins were checked before and after execution and still match the README; no availability blocker remains. This is a build/review verdict, not root adoption or seal/launch authorization.

**TESTED:** 129/129 expected observations in this lane. That total comprises 123 ordinary positive/refusal/integration assertions and six successful reproductions of an admission-checker mismatch. It must not be read as 129 successful closure tests. Zero audit denials; observed process RSS 32,014,336 bytes, below 8 GB. A hard address-space cap is not claimed.

D-07 has a valid five-pin positive plus five malformed forms for each required mapping (PENDING, null, list, wrong object, wrong types), and malformed top-level slot/prereg containers. Every negative was checked both through the actual API and actual in-process CLI, with REFUSE JSON and exit 2. No subprocess CLI launch occurred. D-01 has 13 direct field tests: DDO alias128, contradictions and bools, optional NGC96, explicit NGC mismatch, LO echoes and GQ doubling/context.

D-04 was exercised through actual T3 on a complete synthetic metadata chain: byte-pinned case block, synthetic active driver record, cascade addendum, 15 inert source entries, bound-plan metadata, exact launcher/guard, ten inert spec pins and exact command string. Positive pass-through equals the input pins. Stale/missing/malformed case-block and cascade pins, launcher/guard mismatches, named BUILD/template mismatches, route disagreement, frozen path mismatch, text-of-record changes and missing/wrong root SHA refuse. Oversized-integer duplicate, nonfinite and invalid-UTF8 check records refuse, as do defective cascade JSON variants. These checks use an **explicit synthetic compare API double** to isolate T3 wiring and activation-before-validation order; production compare/driver scientific validation is UNTESTED.

The actual T4 builder then ran T1/T2/T3 and B6/B7 validators over the same inert fixtures, returned a synthetic record in memory and propagated case-block/cascade/build/allowlist/admission pins exactly. It was never installed as a real seal. B6 positives and wrong schema, blinding, test_mode, script hash, route mode, value-bearing payload and empty gate set were checked directly. The synthetic B7 inputs assert no scientific evidence.

**BLOCKING ED-D05-1 (delegated TESTED evidence, byte-verified here).** The entry/driver lane demonstrates a 20-row A82–A101 positive, refusal of uncovered A102, but acceptance of A102 via a bare name and a fixed generic note. A changed A90 likewise passes with only its name and old/new section hashes. Neither supplies the required reasoned revision/no-change decision. The selected README explicitly instructs that same mechanism; it does not repair it. Its 45 expected-observation assertions and D-06/R-10 scope are reported separately, not attributed to this lane's 129. A successor needs a pinned per-entry decision/reason with exact entry coverage, or an explicit coordinator disposition; this review does not infer one.

**SHOULD_FIX B8-GUARD-PARITY (nonblocking).** With otherwise valid and repinned synthetic inputs, actual r2 admission checking returns PASS for each of: wrong sealed_by; absent sealed_by; malformed driver pin; stale driver hash; malformed frozen-addendum pin; stale frozen-addendum hash. The selected runtime guard source explicitly requires the authority and validates both pins. The guard itself was **not invoked**: its refusal is source inference, whereas checker acceptance is executed evidence. This is a readiness-checker inconsistency, not a scientific launch or admission bypass. Matching those guard requirements would avoid a misleading checker PASS.

The source-review lane also notes a documentation precision issue: README A102 says integer-as-string parsing applies to the cascade addendum, but that branch retains native integer parsing and refuses non-syntax ValueError. This is fail-closed, not the old duplicate-key fallback bypass. It adds no blocking count.

UNTESTED: real seal/prereg/config installation, real admission, binder/launcher execution, scientific stages/targets, the author's full 148-case suite, and eventual root disposition. No protected run or target file was read. All fixture and evidence writes were exclusive. Two orchestration tool calls had JavaScript syntax errors before shell execution (harness construction and report sealing); their corrected calls created the intended new artifacts. They do not alter source/test outcomes.

Byte SHA256 citations (all re-read for this report):

- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/seal_tools/review_r2_synthetic_cx3v001.py — 126407d445fbede0a38240df3b2e1ee7ae366cc84f352a6ee273651b8e3dcd74
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/seal_tools/r2_synthetic_v001/RESULTS_CX3V001.json — 88f254556c9f8f59e9c86f9a7d264b99e52fd007fdf067dc47c3a61750663803
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/README_SEAL_TOOLS.md — da29c008064ae51673dfe7106f72dfcb789f674b4c0a36e3a5daf017c7967af8
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/entry_driver_review/REVIEW_CX3V001.md — 76ee51e03e06de3676953da311d5657f08aaca00649262686e0eef3b12850042
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/entry_driver_review/RESULTS_CX3V001.json — 086bc3d3cfd522d67143790b80f763a81122f2466729743bf66c377f9e2f10bb
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/contracts/REVIEW_D04_R04_CX3V001.md — 98aa58f42575ef7cd2577783d3aa22f3bec88592d3b1fbd7ebed2f0da3b330a2
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/contracts/CONTRACTS_CX3V001.json — b7c818d6f0b474faad55aad93edaa86b0896be7b05fa0efaca77d7a6e5950538
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_rehearsal_c4/run/GAPS_C4V001.md — 566b206635d7ba160ab602842c64e7f1ffd38878c6bf0d7ed3721faffcc3543c
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_rehearsal_c4/refute/REFUTE.md — 7be3fb347310040a1fc806b8886c85cb17e631cb9933aed6261cd958499c3eda
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/producer_guard_cx1v008.py — 294cb7760679b883a62fb3117dc75e91231b2f173bcec65983e6762371ea0731
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/seal_common_c4v002.py — f41b0fca51a95387577839e52308a2dc6ccb79b1e6b9283f389b54c7f348dc10
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/check_frozen_addendum_c4v002.py — 06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/check_sealed_compare_c4v002.py — aebb7b731a800e558b13a5f290c7fac062183cb9ba092af45df4e6bda1f390cf
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/check_slot_fill_c4v002.py — 806733fb18e167275a1de62ebc9433fecf632cc16393933801fd4c9e53cddffb
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/build_seal_record_c4v002.py — 4192983d262e2a27a3d9c90681b6ee66a90c901bfe2f99a7dce2349bc8c5de52
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/print_driver_build_record_c4v002.py — fde0b26e7ea26d4ad15213cc9c3115a807179616e0e155037c97d2179db7a673
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/seal_tools/CUSTODY_R2_CX3V001.json — 1e5a7c808ed5ebd464b25df8e215be697de5a65fb07d60b8045579ee799ed86d
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/seal_tools/DECISION_R2_CX3V001.json — fef10efd21343c44d16708446d3431e017ed047d12b4b20faa2dce1cd4118869

