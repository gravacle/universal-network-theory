# Codex2 cross-lineage review: identity comparator c2v006

date -u: Sun Oct 18 16:21:52 UTC 2026

**FAIL — three BLOCKING findings, two additional SHOULD_FIX findings, and the five A73 successor items still absent or partial.** Findings are TESTED software behaviors unless explicitly labelled source-only. Reviewed comparator SHA256 `097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48` is unchanged. No scientific identity or production incidence claim is made.

The original0553 failures are closed on our independent regression set: **138/138** controls pass across r4 and r5, with actual owning-check assertions and clean baselines. That does not close the independently discovered A71 holes below.

1. **CX2-V6-B1: duplicate NPY header keys.** ast.literal_eval constructs the header dict before key validation. Duplicate descr, shape and equal fortran_order entries disappear into the final value. Both standalone NPY and NPY-inside-NPZ records return full PASS; STRICT_PARSE and NO_LAST_WINS remain true. This is malformed-header acceptance; the tests do not claim unequal decoded arrays in these cases. Reject duplicates in the header AST before evaluation.
2. **CX2-V6-B2: post-join token collision.** One declared pair labelled `<X>|<Y>` and another pair given both `<X>` and `<Y>` receive the same final joined token. Different synthetic result strings then compare equal with every check passing. The same change without the tokens fails RESULT only. Constrain complete triples to the driver derivation, use the closed label grammar and verify final normalization injectivity. This is a concrete whole-gate alias beyond the broader A73 SF2 policy omission.
3. **CX2-V6-B3: attempt-ledger newline alias.** The regex `$` accepts a final newline, so ordinary and newline-suffixed start filenames share a captured directory/token/kind. Grouping overwrites the earlier entry after both entries are popped from inventory. A tampered value900 is hidden by value1 and the full comparison passes, including ATTEMPT_LEDGER, INVENTORY, NO_LAST_WINS and COVERAGE. The same ordinary change without the alias fails ATTEMPT_LEDGER only. Use fullmatch/absolute-end semantics and reject grouped-key duplicates before removing inventory entries.

The A71 audit independently enumerates139 conversion/assignment candidate sites and checks all199 dict literals for duplicate constant keys. It includes overbroad fixed state/report assignments to avoid relying on the build's own inventory. All sites have source locations and assessments. This finite audit is not a formal proof of completeness. New whole-gate probes comprise13 executions: seven undesired PASS outcomes across the three blocker classes and repeated-token case, three positive controls PASS, and three ordinary-change controls fail solely their owners. Eighteen unit observations support parser/normalizer/Store mechanisms.

**CX2-V6-S1:** repeated identical declared triples silently deduplicate in sets and read PASS/NO_LAST_WINS PASS. A71 explicitly rejects duplicates even when equal; the equal duplicate alone does not demonstrate changed values.

**CX2-V6-S2:** current saved selftest results are consistent, but some wrapper assertions are weak. Independent source/report audit checked266/266 saved synthetic cases against byte hashes, candidate pin, driver, verdict, actual false checks and semantic owner. All current must-fail cases hit their owner. However19 structural negatives per driver only require any FAIL, and17 invocation negatives per driver have empty required_failure lists (72 total weak expectations). A future unrelated failure could satisfy them. Add owner assertions. The original marker-bearing A baseline is explicitly expected to fail NORM_INJECTIVE-only; clean independent variants also pass/fail the intended owners. The supplied harness was not imported or run by our lanes; saved-report audit is distinguished from our138 fresh executions.

| A73 item | Presence on the reviewed bytes |
|---|---|
| SF1 full RO1 key set |Absent, TESTED: extra fields accepted; known inadmissible_record still refuses.|
| SF2 driver-derived ref/new/token triples |Absent, TESTED: arbitrary string pairs pass policy and normalize unequal inputs equally. Distinct from B2's joined-label collision.|
| SF3 selected-driver static pins |Absent, TESTED: arbitrary owned file and r4-only pin accepted while r5 is selected.|
| N3 firmlink and NFD aliases |Absent in inherited fill, TESTED on scratch same-inode aliases; no v006 fill successor. Existing marker protections still work; no actual C5H guard bypass is claimed.|
| N6 receipt status and each verdict |Partial, SOURCE REVIEW: no v006 command successor; old script checks existence. The v006 record writer checks each comparator verdict but does not predicate on receipt FINISHED/exit_code. Neither script nor writer was executed.|

A73 explicitly allows these should-fixes in c2v007 if missing from c2v006; they are reported separately from the three blockers. The A73 probes yield20/47 satisfied requirement predicates;27 failed predicates expose the listed omissions, not harness crashes. A74 observed during review incorporates the first two blockers and duplicate-token rule into the successor design. The ledger finding was sent separately while final review compiled. This lane has not built or launched any successor.

Source/hash consistency: modules and driver tables are compiled/parsed from their verified byte buffers. Bounded Store probes confirm array caching and digest consistency, stable and changed end hashes, and remembered intermediate changes. JSONL/raw/scan paths can reread and compare digests against the first digest; BUILD's blanket every-file-once wording needs that qualification. Changed-and-restored bytes between observations remain outside an end-hash guarantee; compared bytes retain their recorded hash. No new Store consistency bypass was found by this slice.

UNTESTED: any actual r4/r5 identity pair or its production report, scientific correctness, incidence of these malformed inputs in production, full seal integration and unprobed concurrency races. No UVT/C5H run or receipt, NGC observed/target velocities, session logs, network or git writes were accessed. The source BUILD's reported real-run claims were not independently verified. Only source, static tables and synthetic fixtures/reports were read. No scientific launches; no deletion/move/rename/overwrite. All reviewed source files remain untouched. Python used the approved isolated interpreter, numpy/stdlib, single-thread environment and0514 nice waiver.

Evidence counts are separated by purpose; overlapping templates and unit observations are not combined into a scientific pass rate. Earlier selftest-audit v001 records missing owner declarations; v002 adds independent owner mappings. All versions remain immutable. The final manifest uses JSONL-escaped paths because ledger fixtures intentionally contain newlines; symlink objects use explicitly labelled hashes of link-text bytes without following them. The open ruling snapshot is an observation, not a freeze or seal.

## Cited files and byte hashes

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/run_identity_compare_c2v006.py`
  sha256 `097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0564_2026-10-18_codex2_crosslineage_review_comparator_c2v006.md`
  sha256 `332ed9d11fc069b772673b50d07b5db678d11fb68cad13a152ea470c5173103d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/BUILD.md`
  sha256 `fedbc6157037e2e1c847e7211b9ed9519193c99185bc4ce2362783384bb647d1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/DIFF_c2v005_c2v006.diff`
  sha256 `ded144d333a50eaa0f0d45a36850f104227ed348a5db1abcff46c6658bd6621b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/OPEN_RULINGS_SNAPSHOT_CX2V001.md`
  sha256 `4ebdd96729366a6215d5ddaec2c10b12e9b8b6aceeeeabfbc0c3adf343c36c8a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/FINDINGS_CX2V001.json`
  sha256 `420d1816bdd8e1a9c05488341f2bd3cc849bcd23f9e19d13b556da7df9bdf653`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/TYPED_BLOCKERS_CX2V001.json`
  sha256 `246a6c52ac73681c2d17f7265ce5cfcc9ee15dceebe2f17a9e29df623d1609de`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/REVIEW_SOURCE_CX2V001.md`
  sha256 `5e5d749c412e2f209cb726396761b3d93e50c9c189416e31dfe412d2916a7666`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/REVIEW.md`
  sha256 `3650fb0b35829a3d5c600093d8f5d55c9e32f1ad4017321603abd3ef17bef106`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/a73/REVIEW_CX2V001.md`
  sha256 `850311f6ffacb4b8ba64e5db1104733d540222c0bd736cc7d013f4a80e81f67a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/selftest_audit/REVIEW_CX2V001.md`
  sha256 `f719ad8c247140dca863cfad26449819db9576719704d6c5320cc36c70c7b56a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/CONVERSION_INVENTORY_CX2V001.json`
  sha256 `678980881cc452d2d67a618edbdb033495dd6e7f07950acb106a08e6c8ec7239`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probes_v001/RESULTS_CX2V001.json`
  sha256 `39b218bb9296be1a6181688151f302a98bd499eff842947c79aa073c9e2f232a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/ledger_v001/RESULTS_LEDGER_CX2V001.json`
  sha256 `203f85346f9a86c5ea39df03392a3d38eaa1ea009c5f510d6f3245cf12f11c18`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/SUMMARY_CX2V001.json`
  sha256 `aee6fd408b8fe463712fc87ec5598d7a855710e8392c44c76e6e53c9bf737bb4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/PORT_PROVENANCE_CX2V001.json`
  sha256 `950916f8788075a55b94d225376b55ab7340bf7822b29c66802a6c98521ccda4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/a73/A73_PRESENCE_CX2V001.json`
  sha256 `cae55d2e77774b32883b169974df7dddf4b4c3f872e13f03f20d2f45cfa456db`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/selftest_audit/SELFTEST_INTEGRITY_CX2V002.json`
  sha256 `04d085647da953d5fe440e9675e10d91f42567621e573419d30a1571ce91ddbf`
