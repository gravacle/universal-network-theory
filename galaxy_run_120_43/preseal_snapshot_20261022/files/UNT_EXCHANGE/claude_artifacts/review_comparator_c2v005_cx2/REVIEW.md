# Comparator c2v005 cross-lineage review — FAIL

`date -u`: Sun Oct 18 15:22:36 UTC 2026

**FAIL: one TESTED BLOCKING false PASS.** The exact reviewed comparator has SHA256 6f656c68e51f457704dafd19c1a9e6b632e237f4959017ee376c18ad173b076b. Source identity was verified before and after every final suite and again during packaging. All work used synthetic saved states or source reads; no scientific execution occurred.

The full actual comparator accepts an added tampered result field when its raw dictionary key normalizes to an existing key. In the discriminating baseline, reference extra contains the literal key <RUN>/x with value same. NEW adds its actual run-root path plus /x with value tampered, followed by the unchanged literal key. Side.norm's dictionary comprehension overwrites the earlier value; every check passes. Ordinary new and changed result leaves correctly fail in companion controls. Reject many-to-one key normalization recursively before applying comparison/masking rules. This is the decisive B1 finding and was reported promptly in the numbered packet cited below.

Additional SHOULD_FIX findings: structured NPY/NPZ dtype field names are lost by dtype.str; duplicate JSON keys use last-wins parsing; duplicate NPZ members can hide an earlier tampered array; and the checkpoint loader reopens a module after hashing it. The first three have actual whole-gate synthetic false-PASS controls. The loader gap is source-confirmed, with its race exploit UNTESTED. NPZ versus NPY storage-order handling is a NOTE: logical values are unchanged, but the equivalence contract should be explicit. These severities and production-scope limits are recorded in the final findings file.

## Test coverage

- Structural: 23 independently constructed case templates, all expected outcomes met under both r4 and r5 selection (46/46). Includes extra/missing/renamed/tampered stage trees, balanced collisions, empty extra stage, full nested result fields, binary inputs, finish and route-A attempt-result records.
- Invocation/value: 24 independently constructed case templates under each driver (48/48). Includes exact and duplicate tail argv blocks, signed zero, int/float/bool distinction, nested values, NPZ dtype/value controls, symlinks and the required Z2 replace-token case. A base script on NEW refuses while its replacement token policy itself passes.
- Source-audit edge cases: nine whole-gate B0P/r5 executions plus two duplicate-NPZ followups. These expose B1 and the additional strictness gaps; they are not a passing suite. The primary 47 broad-case templates and these additional targeted controls are separate test scopes, not scientific samples.

Every fixture was newly constructed; no prior checker fixture generator was imported. Existing c2v004 checker cases were read to distinguish the new boundary cases. The successor checker set had not been published when these suites were sealed, so exact overlap against that set remains UNTESTED. This limitation does not weaken the reproduced B1 counterexample.

V005 does close the observed predecessor stage-number/name-collision mechanism and compares the complete normalized result with declared rules. Its checks also reject duplicate tail flags and the Z2 NEW base-script substitution in our controls. B1 remains because normalization is still lossy before the full-object comparison.

## Scientific comparisons and authority

The requested actual three r4 comparisons and eventual three r5 comparisons are **UNTESTED / BLOCKED**. The principal's direct instruction forbids all runs_ext/UVT_* reads; dispatch0553 permits finished ones. Clarification was requested from the principal, and no waiver has arrived. No UVT output or receipt was opened. The code/canary verdict above is final for these source bytes; it is not an actual-run verdict. C5H, NGC3198 target velocities and session logs were not read. No network, launches, deletes, moves, renames or overwrites occurred.

The known comparator issue also applies to the retained v004-derived sensitivity comparator; the delivered r8 build explicitly blocks both its gate and evidence-producing CLI pending a reviewed successor. This report edits none of those reviewed files and authorizes no launch.

Execution used the required isolated Python with bytecode disabled, numpy/stdlib and single-thread BLAS. Execution note: nice unavailable (sandbox);0514 waiver. Component manifests were reverified by the parent, including explicitly labeled symlink-text hashes without following the synthetic links.

## Files and SHA256 from bytes

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v005/run_identity_compare_c2v005.py` — `6f656c68e51f457704dafd19c1a9e6b632e237f4959017ee376c18ad173b076b`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0553_2026-10-18_codex2_crosslineage_review_comparator_c2v005.md` — `da0065550d9cd52320385d2f4ab3da5d01591cd5fb722e2930032412c75af747`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0436_2026-10-18_0553_v005_blocking_normalized_key_collision.md` — `e69961dd01e401226cfad06f5a11839823f9ebb9d32707f476713aaa7bca2260`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/STRUCTURAL_REVIEW_CX2V001.md` — `a0245b9bce6f95ec195e04523f9146b3949e1fba8b7d25e1b9c5e2c8609fbc71`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/STRUCTURAL_SUMMARY_CX2V001.json` — `9c34726fa2e0cc1fc8e828c3d08e406b1f87706a7dfc372e36dafd71302b1eb3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/STRUCTURAL_HASHES_CX2V001.txt` — `95ead1a946eacd262d96d2a942495934395c8d58f479fb09cc9df306c4032b0a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/INVOCATION_REVIEW_CX2V002.md` — `c9a22571260754f36e6c53e47a683c7e8cdde2efe8aa8d9b18c9b48ee1245597`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/INVOCATION_REVIEW_CX2V002.json` — `c3269d2644617604e77fa2be0834e7391e523e2b9e7e63fa676ffd48c15fa702`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/HASHES_INVOCATION_CX2V002.txt` — `4b86816760a20cb60ad53bf5cdfd1e66ff9deefb868c1691ad5dd1f5bb74d74b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/REVIEW_V005_CX2V001.md` — `f95d84c06934071f6b2c88f84cc409f1371e3cc5680ead85f3a419baa842c35c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/FINDINGS_V005_CX2V001.json` — `335fe9f243384112c9f5ae46f10bc30f385f11c404433796f894cf4843ffe249`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/HASHES_V005_CX2V001.txt` — `64ce555f6fa0926f2fc468e8562dff57f65ed8270ea87393fc3653f094e4c205`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/ADDENDUM_NPZ_MEMBERS_V005_CX2V001.md` — `d374e2b4443e5e4857b398c2307e70e808e66bde7a378a176b08d881b685d832`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/HASHES_NPZ_ADDENDUM_V005_CX2V001.txt` — `24a4ba70d3e7387c4346fdda5afe5de18430d3791f2a0523e00b81dfc63a0fac`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/RESULTS.json` — `11eeb55904bc8daa714c5e1fd4776833bb6a560a15280eb01805055b4b68c546`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/baseline/REPORT.json` — `81bfface8aa21d84957b6a1c762e2e919abc69f5667e303a7002a14507f6ed0b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/ordinary_result_change/REPORT.json` — `cc70ce204171cf74202454c778c53db8290e0ebe266e889109ee56228061660b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/ordinary_result_extra/REPORT.json` — `a3877ad73435baaf3aa7f36666a3f87db4dbc98ad29654fdbaa9a7a2b04a04ae`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/key_collision/REPORT.json` — `59a64695a8ab0513aac9b3c9b70c04816dc77098a08890a3345f5d59a2a95f46`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/structured_npz/REPORT.json` — `9a222da95b5a22889bef3b206281f9cfd6c5d8f7259fadc92baeda845fe5a621`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/structured_npy/REPORT.json` — `59db6946712c407f35cc7f2246c662c25ce0e77e12bb7f70984bf84a89a900e3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/npz_storage_order/REPORT.json` — `1fe0e2ea1114a01bb4a45c99545ea6be1af7a67b46e23a9f64fa03b868bbc4d4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/npy_storage_order/REPORT.json` — `abed5d22753e32ca366a7489f2068a75662222488261ac3cee2b02e468f775af`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/duplicate_json_key/REPORT.json` — `69c0f68d9845bbbcd1f7a8d0190bc8bd9a64ce5ae525b0d2adce51fa23b27c44`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/FINDINGS_CX2V001.json` — `8a0700f7255d9d9f0e3ca77e06ea986256da0e6bcd6593337434124a98e0f99a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/TYPED_BLOCKERS_CX2V001.json` — `f84f9c25322e6b48843dba87d2de4359246f48d84dacc100e7e2df6519c16929`
