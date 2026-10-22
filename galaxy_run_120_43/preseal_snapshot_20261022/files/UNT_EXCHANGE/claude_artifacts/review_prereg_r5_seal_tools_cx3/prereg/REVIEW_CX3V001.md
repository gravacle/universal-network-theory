# Independent prereg r5 review — Codex3

`date -u`: Sun Oct 18 21:17:42 UTC 2026

**PASS. New artifact-review BLOCKING: 0; SHOULD_FIX: 0.** This verdict covers the pinned, unsealed preregistration and its A82–A101 table. It does not adopt a seal, clear existing root items, approve a scientific launch, or review seal tools v002.

**TESTED:** 319/319 independent metadata, custody, Markdown/JSON and in-memory tamper checks passed; audit denials 0; observed RSS 24,985,600 bytes. Reviewed producers, case-block builders, comparison engines and seal tools were not executed. No numerical replay, protected run access, actual root config or seal was used.

Evidence:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/prereg/RESULTS_CX3V002.json` — SHA256 `dfcc70915e7dfe9157439d6e3f72da493ffe8a4053648b10f40ee6c392ceef89`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/prereg/check_prereg_cx3v002.py` — SHA256 `4e7845d1240ee3165de66037db3f0b8693141cb2cafee359a407a89e09dad87b`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0628_2026-10-18_codex3_next_prereg_r5_tools_v002_review.md` — SHA256 `9586ad51802e8f5cdce79e35d09c29b331f8381a6f4e0cfb641bee98fe9c0628`

The bound BUILD and case block match their full SHA256 values from actual bytes. The case block has ten tail cases with the r5 driver and gas M_s=128 plus one inert C5H declaration; no referenced run was opened. The registered plan/candidate source pins also match.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/BUILD_V007.md` — SHA256 `94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json` — SHA256 `76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71`

The Markdown explicitly states that the JSON contains the full clause text. All rendered seal-slot rules/values, all 13 rendered seal-record requirements, entry-table rows, and BUILD/case-block pins agree. This is agreement of the declared partial rendering, not an assertion that both documents contain identical full scientific prose.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json` — SHA256 `3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.md` — SHA256 `2ed287717a831b422d93ad62339a85aa5b1ffbc570d39bd3ddc6066e8989c208`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/ENTRY_TABLE_R5.md` — SHA256 `b4bf8392db0ed5919b9583cf2f8b71b4d1ec26fd3c735cfd622e9cb81ac3063e`

All 20 pinned ruling sections A82 through A101 were read and compared with their table dispositions and named clauses. Exact section bytes, lengths and SHA256 values were independently reconstructed from heading boundaries, not accepted from the author table. The table has 16 revised entries and four justified no-change entries (A84, A85, A95, A98). No decimal-numbered section is omitted: A98.1 is an item within A98. Three recorded addendum snapshots also match their byte pins. All named revised clauses resolve and differ from the r4 base.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md` — SHA256 `70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json` — SHA256 `e3b6b5b2ba265f54d15381f358913dd3ea931761aaa649c98a7583f58f1b7cf8`

| Entry | Disposition | Independent reading | Section SHA256 |
|---|---|---|---|
| A82 | REVISED_HERE | Reviewed compare source / sealed compare ordering and acyclic pin filling are retained. | `8a45e4a9378e5c51e5d410f007af5040840cbfa7404f52220bb4db37130ddedc` |
| A83 | REVISED_HERE | Cross-lineage compare and identity reviews replace the stopped own checks. | `b2c7417ffbde8f7c44b630e2e103d18984d36bed78ec9b96be86b06e499f2e08` |
| A84 | NO_CHANGE | NO_CHANGE is honest: scheduling/conditional r6 work, later made moot by A96. | `598055296c7d18d52f82d1ee248c3fd5de2b2022c8b4bb25fea496b49b122360` |
| A85 | NO_CHANGE | NO_CHANGE is honest: operational QoS/SSD/guarded parallel work stays in BUILD/runbook. | `8be593cf6eff91d21503345fdcd58a495b6eeed8a06122530b42aa320efb1cef` |
| A86 | REVISED_HERE | GQ V006 and DOUBLING informational K handling are carried into clauses. | `b3f451697f29bbc6ef094f76c94753d8a649d9d4a952aba55ee1dc4b83b7e0a8` |
| A87 | REVISED_HERE | Merged DOUBLING, B3 fields, LO_NGC V002 and missing producer records remain explicit. | `3d479167fe3049dbbf72629120d13b393df2dc4f595a7c9dc3544cf56d8116bb` |
| A88 | REVISED_HERE | SR_K after-seal timing and pinned producer custody are stated; other gate prerequisites remain. | `216fce8735405f208179561ca94e25019b6aec4ed7389f140979bfcc6aed47d7` |
| A89 | REVISED_HERE | The revised KHI estimate is retained under an explicit UNTESTED estimate field. | `2e7844cc5145afee32def134780bbab526ac93edf8a5c23cdf41559b0a6bf3a7` |
| A90 | REVISED_HERE | NGC K32 certificate work is distinguished from the V007 LO_NGC record; r12 scope is retained. | `b1fce9a94cea5217ad474b5c72a802772bb53ec0ffcabcb44f42b147cec41232` |
| A91 | REVISED_HERE | r12 review scope and required identity/caller digests are stated; conditional r6 cache work is moot. | `7eb0f0a7093a7eee9a0cb89db14c6049358f9c11ada6f8590914ea1e0faab75c` |
| A92 | REVISED_HERE | c2v007r2 / R5 identity record requirements are carried into seal slots. | `6d671c27db121106c5a6773b5aaf7bcdbccd04737dbe75466d1a887a49d3ae00` |
| A93 | REVISED_HERE | r007 NGC registry is acknowledged as separate step-5 scope, without launch authority. | `9474602df90fac58d31835eb5a950f909299ecc0e1f95e6d8f403ac5e60e5c7f` |
| A94 | REVISED_HERE | B2 full static le3 / P16 requirements and unresolved interpretation are recorded. | `7ea61f90cd8feb9327b7db92bb8894fd0043383fd1ffe3ad7bbf5d1efc662b8f` |
| A95 | NO_CHANGE | NO_CHANGE is honest: taskpolicy is a preferred operational measure; production single-thread policy remains. | `435403e307b70701cf7e006c4e49477033c684041239e7862a5190ddf1bda8a5` |
| A96 | REVISED_HERE | Production remains r5, without r6/cache; reviewed r12 source is named with pending adoption controls. | `fed0c12f8eab596f2eefd2e896fb218da527114a837339590b1ccebc35d4957c` |
| A97 | REVISED_HERE | B2 decomposition and missing-record INCOMPLETE handling preserve the unchanged 0.05 threshold. | `a1734bcd393e4c16503f9cc541335694bcd1d873730550314e4a4b5bb01931a0` |
| A98 | NO_CHANGE | NO_CHANGE is honest: NGC diagnostic traceback and step-6 work are outside this V007 prereg text. | `181248d91db1437786cc8654c4dc82bb3983ea36a069f702f6dfd2acadfd8aa9` |
| A99 | REVISED_HERE | BUILD_V007, independent case-block binding, complete entry table and freeze-time rehash obligation are present. | `195fe36e8abf997656ec52e92c949db188411673c3820baf1f28d85e09dbe57c` |
| A100 | REVISED_HERE | B2 like-for-like interpretation, exact disclosed values, unchanged tolerance and physical-correctness limitation are retained. | `ff872d375e55bb31489bdd2cd82ca533f93e9041c03c6af76a399c203f841b5a` |
| A101 | REVISED_HERE | B2 C3V003 and documentation errata, case-block review and registry updates are acknowledged. | `1a8babc42526e6af7f24075746e8e6010b5c161b9ee0e7a42564dc11c20cf961` |

The table is complete for its pinned generation snapshot through A101. It honestly requires a successor or explicit seal-record note for later entries and rehashing against the frozen bytes. This review does not claim that no later ruling exists.

The author’s original delta audit remains **FAIL**: 1,039 differing leaves included three header/bookkeeping leaves not named by its original delta row. The immutable erratum identifies `revision`, `supersedes_draft.path`, and `supersedes_draft.sha256`; the r5/r4 bookkeeping and predecessor pin were checked here. This is a disclosed documentation correction, not a silently converted author PASS or a changed prereg hash.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/out/AUDIT_R5_VS_R4_C4V001.json` — SHA256 `4374e85aea8a59ab418e2e6cb32e8d09bc23bdcf50d5fbc209ddeca18bd709ac`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/DELTA_R4_R5.md` — SHA256 `741cb7985125f1cb705a289001a329aee74c6c8314b80b1877a7c72d88e6fd4a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/DELTA_R4_R5_ERRATUM_E1.md` — SHA256 `b68a1f539cd0c6e9a4fe5bc4d841d0ceae7c2070a37bb05d2f4f09d46fdc10e8`

The pinned draft explicitly leaves RI-28 through RI-37 open. In particular, RI-28 records the compare A-B1 finding and pending root disposition. The other adoption, identity, registry, record-availability and freeze obligations are preserved. Their existing status is separate from this review’s zero new artifact blockers; none is cleared by this review.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/ROOT_ITEMS_R5.md` — SHA256 `2387dc23c790a894b6f969d133d48eb0a095f46ed97448fce67070ed59cdd3d4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/SEAL_CHECKLIST_R5.md` — SHA256 `7ff81720e6cf108a6f71d478dcc23493fb1ee943ed2c90e88873715a2921bd13`

The nine MUST_FAIL integrity canaries reject a missing/duplicate entry, wrong section hash, unknown decision, missing no-change reason, missing revised-clause list, changed snapshot, changed BUILD bytes and changed case-block bytes. These exercise this independent metadata checker only; seal-tool tamper behavior remains outside this lane.

Checker correction: v001 passed 318/319 and failed a spelling-only expectation (`section_sha256` versus the actual prose “section sha256”). Immutable v002 corrects that expected prose spelling and changes its output filename; reviewed prereg bytes are unchanged. The first checker and its result are preserved:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/prereg/check_prereg_cx3v001.py` — SHA256 `10a2296c3e9727b8939bcf9d6a4c031679cf6404fa8ee44e7b7e43920001d630`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/prereg/RESULTS_CX3V001.json` — SHA256 `d54ce8ab681d1c3ab9bddd8952dbf9338bb01a90d868bb4e4a9636291be3e5b4`

**UNTESTED here:** live seal assembly, seal-tools v002, scientific gate truth, root adoption and any production execution.
