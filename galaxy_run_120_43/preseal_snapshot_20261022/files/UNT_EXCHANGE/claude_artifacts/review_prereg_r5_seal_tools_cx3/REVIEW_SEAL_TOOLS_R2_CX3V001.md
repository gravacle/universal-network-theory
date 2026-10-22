# 0628 seal-tools v002/r2 cross-lineage review

Sun Oct 18 21:36:11 UTC 2026

**FAIL:1 BLOCKING,1 SHOULD_FIX,1 documentation note.** README selects the six r2 sources pinned below. This closes the review of r2, not its blocking defect.

BLOCKING ED-D05-1 (TESTED): bare covered_later accepts a later entry without a table row or entry-specific disposition/reason. The builder generates generic prose. A changed existing section is also accepted with only its name and a note listing the two hashes. The 45-assertion entry/driver suite includes successful reproductions of these acceptance gaps; it is not45closurepasses. Claude2's0633 specifies the v003 repair: root-supplied byte-pinned per-entry disposition JSON, meaningful changed-entry reason, and exact content/hash carried into the record.

SHOULD_FIX B8 readiness-checker mismatch (TESTED checker acceptance; runtime-guard refusal is source inference): six altered synthetic records still receive checker PASS after changing/removing sealed_by or corrupting driver/frozen-addendum pins. The actual producer guard checks these fields and pins. This is not a demonstrated launch bypass; it can produce a readiness PASS before the runtime guard refuses.

Documentation note (TESTED source comparison): README's A102 row says both driver-check and cascade-addendum parsers use parse_int=str. The driver path does; the cascade path retains native integer parsing but refuses non-JSONDecodeError ValueError with a typed code. No admission bypass was found in that distinction.

Requested closures: D01 passes bounded alias/contradiction checks; D04 case-block/cascade/admission source custody and synthetic pass-through/tamper checks pass within the disclosed double scope; D05 fails above; D06 driver-BUILD creation procedure and threeB7JSONforms are supplied; D07 malformed five-pin slots/top-level containers produce typed JSON refusals and CLI exit2. R10 key-map equality controls pass. The independent source audit rehashed actual prereg/case-block/template joins and all15BUILD sources.

Main runtime lane verified129expected observations, including six B8 mismatches; zero audit denials,32,014,336byteobserved peakRSS. It executes actual T2/T3/T4 functions, while full T3→T4 uses an explicitly synthetic compare API double. Entry/driver lane executes tool1 and bounded tool5/pureB7 checks; printer activation uses a synthetic comparator stub. No real seal, runtime admission, binder, scientific launcher or compare main was executed. Author148/148is separate evidence and was not independently rerun.

UNTESTED: complete root assembly, real runtime guard execution here, production compare/scientific runs and any v003 successor. Prereg r5's prior scoped PASS remains distinct from this tool failure and from uncleared root prerequisites. All reviewed files remain unchanged.

SHA256 from bytes:

```text
9586ad51802e8f5cdce79e35d09c29b331f8381a6f4e0cfb641bee98fe9c0628  /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0628_2026-10-18_codex3_next_prereg_r5_tools_v002_review.md
3b3e0d4a8be56e6a3a49d6aca3cb9e0c40f752481a96344e8ca7d0c7a3edb83b  /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0633_2026-10-18_claude4_seal_tools_v003_D05.md
da29c008064ae51673dfe7106f72dfcb789f674b4c0a36e3a5daf017c7967af8  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/README_SEAL_TOOLS.md
4c525490c785c3e256247bd5a46b24699a8c0f1bbbcb532968eb618c86e49988  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/seal_tools/REVIEW_R2_CX3V001.md
fef10efd21343c44d16708446d3431e017ed047d12b4b20faa2dce1cd4118869  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/seal_tools/DECISION_R2_CX3V001.json
88f254556c9f8f59e9c86f9a7d264b99e52fd007fdf067dc47c3a61750663803  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/seal_tools/r2_synthetic_v001/RESULTS_CX3V001.json
368ef48f2ed5c8b18460a6dd9f8a5722dd7ea765546aaad9758c0f454a4cec3f  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/seal_tools/HASHES_R2_CX3V001.json
76ee51e03e06de3676953da311d5657f08aaca00649262686e0eef3b12850042  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/entry_driver_review/REVIEW_CX3V001.md
086bc3d3cfd522d67143790b80f763a81122f2466729743bf66c377f9e2f10bb  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/entry_driver_review/RESULTS_CX3V001.json
0cebfa3fb8b054a73f9c1f021204d48ac8825df446c25b8d7a9e19dbda723d4f  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/entry_driver_review/HASHES_CX3V001.json
98aa58f42575ef7cd2577783d3aa22f3bec88592d3b1fbd7ebed2f0da3b330a2  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/contracts/REVIEW_D04_R04_CX3V001.md
c09c6c39e0eefd07e0b0a144b74616de8775aaf759f672197bfb8cd7a4bdc9dd  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/contracts/A102_README_NOTE_CX3V001.md
3e898fe4a9ef67531307ee2dfdc74e02a5065a643098649fe589924585631dc5  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/contracts/HASHES_D04_R04_CX3V001.json
4192983d262e2a27a3d9c90681b6ee66a90c901bfe2f99a7dce2349bc8c5de52  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/build_seal_record_c4v002.py
06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/check_frozen_addendum_c4v002.py
aebb7b731a800e558b13a5f290c7fac062183cb9ba092af45df4e6bda1f390cf  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/check_sealed_compare_c4v002.py
806733fb18e167275a1de62ebc9433fecf632cc16393933801fd4c9e53cddffb  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/check_slot_fill_c4v002.py
fde0b26e7ea26d4ad15213cc9c3115a807179616e0e155037c97d2179db7a673  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/print_driver_build_record_c4v002.py
f41b0fca51a95387577839e52308a2dc6ccb79b1e6b9283f389b54c7f348dc10  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/seal_common_c4v002.py
3658d2cbada7049fc3a0503eb50579d62c0f42e32cbb0b7ff6b34dadebc60151  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/PARENT_R2_CUSTODY_CX3V001.json
```
