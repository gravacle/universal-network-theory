# Independent comparator c2v005 source audit

`date -u`: Sun Oct 18 15:19:31 UTC 2026

**FAIL — one BLOCKING full-result bypass.** Tested exact source SHA `6f656c68e51f457704dafd19c1a9e6b632e237f4959017ee376c18ad173b076b` (69,421 bytes), rehashed unchanged after the probes. Execution note: `nice unavailable (sandbox); 0514 waiver`. Nine independent whole-gate synthetic B0P/r5 cases ran through actual `main --driver r5`; no comparator checks were stubbed. No scientific launch or actual run/receipt read occurred. Actual scientific comparisons remain UNTESTED and forbidden to this helper.

B1 (BLOCKING, TESTED): `Side.norm` normalizes dictionary keys with a comprehension and silently overwrites collisions. A reference result has `extra={'<RUN>/x':'same'}`. The new result adds the distinct raw key `str(new_run)+'/x'` with value `'tampered'`, before the unchanged literal `'<RUN>/x'`. Both normalize to `'<RUN>/x'`; the changed field disappears. The complete comparator returns PASS_BITWISE_EQUAL with every check passing. This requires no declared tokens. The positive baseline passes; ordinary added and changed result fields fail RESULT, demonstrating a discriminating full-result fixture. Reject every many-to-one key normalization before comparison, including nested dicts and pin dictionaries.

S1 (SHOULD_FIX, TESTED): both array readers compare `dtype.str`, which becomes a void-type summary for structured arrays. Renaming a structured field `radius` to `speed`, preserving bytes/shape/primitive types, passes the whole gate in both NPZ and NPY. Use full dtype descriptors or refuse unsupported structured arrays. Whether production outputs contain such dtypes is UNTESTED; no production arrays were opened.

S2 (SHOULD_FIX, TESTED): JSON uses ordinary last-wins parsing. New result bytes with `valid:false` followed by `valid:true` pass every check. Reject duplicate members consistently in JSON and JSONL readers before claiming strict full-result identity.

N1 (NOTE, TESTED): changing C storage order to Fortran order passes for NPZ but fails STAGES for NPY. Logical values are unchanged; make the equivalence explicit or compare NPZ order too. N2 (SHOULD_FIX, source-confirmed; race UNTESTED): `load_cm` hashes its path and then reopens it through importlib. Execute the exact verified byte snapshot.

The v005 delta does address the two visible predecessor mechanisms: Tree rejects duplicate stage names/numbers, preserves invalid raw paths, checks order and records symlinks; RESULT now compares the full normalized object with declared exceptions. Tail argv blocks are exact and duplicate-aware; SCRIPT_CUSTODY checks actual planned new-side scripts. These improvements do not close B1 above, because full-object comparison occurs after lossy dictionary normalization.

Own canary outcomes: baseline PASS; ordinary result-value change FAIL; ordinary result added leaf FAIL; normalized-key collision unexpected PASS; structured NPZ unexpected PASS; structured NPY unexpected PASS; NPZ storage order PASS (contract note); NPY storage order FAIL; duplicate JSON member unexpected PASS. This audit complements, and does not replace, the separate broader structural/invocation suites.

Files and SHA256 from bytes:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v005/run_identity_compare_c2v005.py` — `6f656c68e51f457704dafd19c1a9e6b632e237f4959017ee376c18ad173b076b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/test_whole_gate_edge_cases_cx2v001.py` — `4b2635f65472bdca319f3d4aafbac4b0e908e033fa3dca5d69d43d8cf33267fa`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/RESULTS.json` — `11eeb55904bc8daa714c5e1fd4776833bb6a560a15280eb01805055b4b68c546`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/FINDINGS_V005_CX2V001.json` — `335fe9f243384112c9f5ae46f10bc30f385f11c404433796f894cf4843ffe249`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/baseline/REPORT.json` — `81bfface8aa21d84957b6a1c762e2e919abc69f5667e303a7002a14507f6ed0b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/ordinary_result_change/REPORT.json` — `cc70ce204171cf74202454c778c53db8290e0ebe266e889109ee56228061660b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/ordinary_result_extra/REPORT.json` — `a3877ad73435baaf3aa7f36666a3f87db4dbc98ad29654fdbaa9a7a2b04a04ae`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/key_collision/REPORT.json` — `59a64695a8ab0513aac9b3c9b70c04816dc77098a08890a3345f5d59a2a95f46`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/structured_npz/REPORT.json` — `9a222da95b5a22889bef3b206281f9cfd6c5d8f7259fadc92baeda845fe5a621`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/structured_npy/REPORT.json` — `59db6946712c407f35cc7f2246c662c25ce0e77e12bb7f70984bf84a89a900e3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/npz_storage_order/REPORT.json` — `1fe0e2ea1114a01bb4a45c99545ea6be1af7a67b46e23a9f64fa03b868bbc4d4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/npy_storage_order/REPORT.json` — `abed5d22753e32ca366a7489f2068a75662222488261ac3cee2b02e468f775af`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/duplicate_json_key/REPORT.json` — `69c0f68d9845bbbcd1f7a8d0190bc8bd9a64ce5ae525b0d2adce51fa23b27c44`
