# Codex2 cross-lineage review: V007 compare r8

date -u: Sun Oct 18 15:36:34 UTC 2026

**FAIL — one BLOCKING parser defect and one SHOULD_FIX blinding defect. TESTED software findings; scientific and sealed adoption remain UNTESTED.** The reviewed compare bytes are unchanged, SHA256 `bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3`. No source was edited and no launch occurred.

**CX2-R8-B1, BLOCKING: a duplicate shell hides a failing LO bound.** The reader converts shells into a dictionary keyed by their range; a later value replaces an earlier one before threshold validation. A required [4,5] shell with bound0.1 followed by the same shell with bound0.0001 reads PASS. The unique bad entry and reversed ordering both read RECORD_DEFECT. The same issue is TESTED for an extended LO shell and for synthetic LO_NGC. This contradicts the every-shell0.005 bound and A54 S5 verdict/data consistency.

The admission slice independently constructed raw result, attempt, finish and receipt fixtures and ran the actual readers, case/identity validators, selected gate readers and evaluate_v007. The malformed registered LO gate reaches **ADOPT_TAIL** under its explicit synthetic V4/V5 and other-gate PASS premises. This tests the code consequence; it does not establish real scientific validity, a complete certified production gate suite or a sealed CLI adoption. Exact registration of the synthetic record bytes was supplied deliberately to isolate semantic validation. Recommend rejecting duplicate ranges before dictionary construction and checking every raw entry, with both orderings as negative controls. The mutable A71 ruling observed during this review already directs an immutable successor and a wider dictionary-construction audit; this review does not implement or launch that successor.

**CX2-R8-S1, SHOULD_FIX: blinded early refusals echo numeric input keys.** Six actual CLI calls (three malformed input types times two blinded modes) print an invented numeric key verbatim on stderr. Both --validity-only and --gates-only are affected before their successful-output redaction. They exit2 without a report; this is no adoption bypass and no real velocity was disclosed. Fixed refusal codes or a mode-aware redaction boundary should cover all early diagnostics.

| Independent slice | TESTED outcome |
|---|---|
| Noise and R-PAIR |85/85 controls plus5/5 exact-tie checks pass. Uncapped norm/same-sign rules, alternating bound, NEW-7, per-row noncontraction, branch selection, inheritance and R3-4 covered.|
| Admission/registry |101/102 controls meet expectations; the duplicate-LO must-refuse case is the sole failure. Fifteen raw S9 mutations, B4, all three identity driver pins, GQ production counts, SR_K record/producer registry and EPS repeated-field consistency pass.|
| CLI blinding |37/43; six failures form S1. Successful blinded output and sha-only gate reads pass the tested sentinels.|
| Isolated decision priority |43/43, with explicitly substituted upstream predicates. Invalid, missing, pending, undecidable and unruled-flag states prevent adoption as specified; earlier pending states mark later decisions PROVISIONAL.|
| Additional binding probes |29 observations:12/12 RB_FP domain guards; four duplicate-shell false-PASS reproductions; three declared deferred-rule mismatches; remaining controls behave as expected. These overlap conceptually with admission findings and are not a distinct-bug count.|

The A51→A54 S7→A56 N1→A58 RI-18 rule chain is implemented without q caps. The old unsealed r2 cap text is superseded by A58. The tested S9 raw-row bug from r5 is closed. A53/R3-4 admission and A62/A67 bindings pass the stated controls; these are bounded tests, not exhaustive proofs.

A68 CHK-1 and A69.1 remain **explicit successor requirements**, separately from the new B1 finding: bind certificate gas.M_s to the registered context, and bind registered producer paths to hashes of their bytes. The owned direct gate API can accept an inconsistent M_s context, but the normal case-block validator rejects that context; no CLI bypass is claimed. A nonexistent producer path can pass with a registered claimed producer SHA and exact record SHA; r8 discloses the missing producer-byte check. A69 exact-tie behavior passed on the registered ordered-row basis. RB_FP low/high excess, shortfall including one-ULP top differences, gaps, overlaps, missing ranges, extra dV keys, false coverage and duplicate labels all refused in12 controls.

Independence: no supplied test module or fixture generator was imported/executed. Admission shared only the fresh static registration setup built by our blinding slice; its raw run records, mutations and gate records were its own. Numerical history oracles use exact rational arithmetic. The initial admission and blinding fixture mistakes are preserved and excluded from final counts. No reviewed file was edited.

UNTESTED: production scientific validity, real R-PAIR outputs and late-pass floating-point floor, actual producer races, full certified/sealed adoption and the future successor. Seal-time pins are still pending. The geometric contraction premise remains DECLARED. C5H call/preflight prep was inspected where needed, but no actual C5H or any UVT run/receipt, NGC observed/target velocities, session logs, network or git writes were accessed. Isolated Python/stdlib/numpy, single-thread environment, nice unavailable under0514 waiver; exclusive small artifact writes only.

All four component manifests were verified from bytes by the parent. Their verification counts and final inputs appear in REVIEW_INDEX_CX2V001.json. V005 is open and changed during the review; the exact final observed bytes are retained as a snapshot, not represented as frozen.

## Cited files and byte hashes

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0558_2026-10-18_codex2_crosslineage_review_compare_r8.md`
  sha256 `dbec760754966a7d4cbdb6ee00815eeb6750e0e8746bc20137adf5cdcfd1fe36`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py`
  sha256 `bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/tests_kmax_tail_compare_c2v007_r8.py`
  sha256 `1735a5e26d82b81d9e7424286d47eddea8c35f1ef1999191321720e393f90769`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/FIELDS_R8.md`
  sha256 `40253fe52f04caf081080e1b28826c70625fa033fcf5343e418b29b8ff8e644b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/COMPARE_V007_IMPL_R8.md`
  sha256 `947248bbb239cd684c8521e0659238d35b8c7f795eb2e50d92bf03b7c0b1ccaa`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r2/KMAX_TAIL_PREREG_V007_FINAL_DRAFT.json`
  sha256 `58a0b87d995ce06e13706c127e3783dc352a292f0ec1614cf9b9b877b6140bfa`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r2/CLAUSE_SOURCE_MAP.md`
  sha256 `c6a0287c7d763286b5764fa073c1c7f0f7a3d0ceafeca4cc7ac1a157b0ebb6a1`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md`
  sha256 `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/V005_OPEN_RULINGS_SNAPSHOT_CX2V002.md`
  sha256 `3380b0fa273d10a9696efde1e10121a83a20adc59ee9033492e9a864e7ea11d4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/INPUT_PINS_CX2V002.json`
  sha256 `b637f4b8ad935955f125aca04afec989869784ca0af9f13b651c7b9f33bc4634`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/FINDINGS_CX2V001.json`
  sha256 `9ae69635550277d5f4ee4837b13eb455a587eba220cdd6022efe041ee178d6c5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/TYPED_BLOCKERS_CX2V001.json`
  sha256 `387d8fe761d2e3f5ee4ff1b975b5f8310df891acfa98e004e0f3736ac5d7558c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/NUMERICAL_REVIEW_CX2V001.md`
  sha256 `e4168d7816dc68d90d30bb2509258062c65f7ee762e6c40cd05f03d583256470`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/admission/REVIEW.md`
  sha256 `36c11589b7adc9be4e02be90dce4a39804be8c5653d3b042a3ccb4183a4f4d32`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/blinding/REVIEW_CX2V001.md`
  sha256 `cd158f11d2d555524ef953bc50fcafc5c7a51a3aebafc635299218bbd95ea1e2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/binding/BINDING_REVIEW_CX2V001.md`
  sha256 `ce2eabdf171f163c9c0a6063f9b5850b70852d95a071d3a93ccbf344783491e8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/admission/run_20261018T153415_33235/RESULTS.json`
  sha256 `8cd1be66cc5e3ae0062c8810233f31216ae87d18c77a7849357f19594187410a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/admission/run_20261018T153415_33235/LO_DUPLICATE_ADOPTION_POLICY_REPORT.json`
  sha256 `0ecb3cf3c6bf698b5f8b73008c1606cd2cc72b2e13d2e11d5c2bc55a28ebed6c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/binding/BINDING_CANARIES_CX2V001.json`
  sha256 `388c3a0e26d09d0dab84728dee7d3f8f85edecce6c1915d0e9bc85c1999aaba3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/binding/LO_NGC_DUPLICATE_RESULTS_CX2V001.json`
  sha256 `8c588c448bff2cbec9acdea33a5b8a73b229c3d7ed23b36da25d0bbeaf1ff52b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/binding/RB_FP_RANGES_RESULTS_CX2V001.json`
  sha256 `c9fdf59b563b77e74bd0b13cd51ec58f66c84375b4b45f10f63e6460110de9a1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/blinding/run_20261018T153234_27448/BLINDING_RESULTS.json`
  sha256 `f45e43af41b7e0c284b1560004db1f6d4a06893162a6a38230726c02833f52df`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/blinding/run_20261018T153337_32888/PRIORITY_RESULTS.json`
  sha256 `4ba6a857e9ad043aa4c022d4776391c2186cc76b261031c8028e2220620c1904`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/A69_TIE_FOLLOWUP_CX2V001.json`
  sha256 `6e549576a6a142bf886e64646312d8019a86b493990734f507e251f130a1456b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/HASHES_NUMERICAL_CX2V002.txt`
  sha256 `f140a31719cefd8238ce86a5df403b690a67d17ed21b7eed4ff27772065f8529`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/admission/HASHES.txt`
  sha256 `adfc6dacdddfa483a951cdc37d7fd88153f49b15c480a10b7713a210844a1d73`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/blinding/HASHES_CX2V001.txt`
  sha256 `0ffefb1c0bdbda1b2396e9c621c41fd207af101ba63d41e06bcc9cc4ef4e4229`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/binding/HASHES_BINDING_CX2V001.txt`
  sha256 `1f3a6ffe60e1975edb4b86c2977f54db5499a1d5e05d69c32d495773a042f121`
