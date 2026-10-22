# Cross-lineage V007 R5 review — FAIL

`date -u`: **Sun Oct 18 12:40:42 UTC 2026**. Codex2, local review helper, dispatch D0524 Lane B. Claude2 remains the only scientific launch owner. This review supersedes no source and grants no launch authority.

**TESTED — FAIL as the current seal candidate.** One blocking record-integrity defect allows a malformed Picard pass history to reach `ADOPT_TAIL`. The requested A53/A54 arithmetic and branch corrections passed the bounded controls below. This is not a scientific finding about any galaxy or a V007 result.

## Blocking finding CX2-R5-B1

**TESTED / BLOCKING.** R5 `pass_rows_gap` (line 853) checks nonempty rows and consecutive pass indices but does not validate raw row IDs. `_pass_rows` (line 868) converts each pass list to a dictionary, silently keeping the last duplicate and retaining/ignoring extra IDs. `read_run` (line 979; extraction at 1019) retains raw IDs only for the final top-level `rows`. The exact-once check in `rows_codes` (line 1354) therefore does not protect pass histories. The noise bound sees the collapsed dictionary.

The independent raw-reader probe creates a complete synthetic C6T result, finish, receipt, start, and route-A attempt under this review directory. It then invokes unmodified R5 `read_run`, the byte-pinned V005 `adapt_result`, the real gate evaluators on synthetic records, and `evaluate_v007`. All scientific inputs are manufactured. With a clean final top-level row list and otherwise passing world:

| Raw pass-history change | Reader codes / gap | C6T valid_all | Decision |
|---|---|---|---|
| Clean control | none / none | true | ADOPT_TAIL |
| Insert conflicting duplicate first-pass row, speed 999, before its retained row | none / none | true | ADOPT_TAIL |
| Append unknown first-pass row, speed 999 | none / none | true | ADOPT_TAIL |
| Insert conflicting duplicate final-pass row before its retained row | none / none | true | ADOPT_TAIL |
| Remove a required first-pass row | none / none | true | INCOMPLETE |
| Make required first-pass speed null | none / none | true | INCOMPLETE |

The duplicate cases are ambiguous records, not valid contraction evidence. A prior speed can disappear solely because of list order. The unknown-row case corroborates missing schema enforcement. No astronomical value is used; 999 is an artificial canary.

**Required successor fix:** check every raw `passes[k].rows` list before dictionary conversion: exactly the registered IDs, each once, finite numeric speeds, with pass-index checks retained. Invalid or ambiguous histories must never supply a decidable E. Treat duplicates as record defects/invalidity or explicitly unresolved status; a silent last-wins policy is unacceptable. Add raw-reader regressions covering duplicates at either end, wrong/unknown IDs, and order permutations. Owner: Claude2 compare-r5 author/loop; root reviews the successor.

## What passed and what it establishes

**TESTED:** 1,122/1,122 first-suite controls, including 1,000 independent randomized noise-oracle comparisons; plus 13/13 additional R-PAIR controls. The raw-reader probe adds six cases above and eight failure/gate serializer canaries, with zero blinding leaks. Peak observed process RSS was under 69 MB. Each replay used one process, the prescribed Python `-I -B`, and single-thread BLAS. Replay note: **nice unavailable (sandbox); 0514 waiver**. D0527 subsequently lifts those caps; this completed review did not need extra concurrency.

- A54 S7: E is the maximum of the norm-level bound and the same-sign per-row bound. A deliberately slow same-sign row strengthens E; a sign-changing row does not get that term. The oracle reproduces the governing formula independently of R5.
- A53 NEW-7: either of the last two norm ratios reaching/exceeding one makes E unavailable before q is capped. Equality, growth, prior-ratio failure, and zero-to-nonzero cases pass.
- A54 B4: missing pass rows/consecutive indices are detected; unresolved gaps do not adopt in the manufactured worlds.
- Invalid receipt/driver/packet, missing case, applicable noncontraction, unresolved flag, and each missing required gate cannot adopt in the exercised worlds. A valid complete manufactured world does adopt, so the barrier checks are not vacuous.
- A53 R-PAIR: Picard members admit the base identity, outcome-result SHA, and tail/RO1 record; the T-case worker kind follows the admitted parallel attempt despite planning column_workers=1. Altered custody and unregistered numerics are rejected. C5H Picard members require unarmed RO1 and no ro1_workers leaf; route-A members require armed RO1 and a distinct route-A identity. Wrong branch is INCOMPLETE. A base flag is carried by Picard members.
- NEW-17: all four decidability pairs refuse untriggered R-PAIR members before test decisions. Generic T3 P/P2/2P content and coverage rules were read in source, not rerun against a production case block.
- Blinding: record-controlled RB_FP shell labels are not emitted; canaries containing decimal, exponent, integer-like and alphabetic labels stay absent. Additional actual gate/failure serializers reject/redact supplied numeric verdict/reason strings. No production `--validity-only` or `--gates-only` CLI run was performed.

**UNTESTED:** a real scientific V007 comparison, real gate production/custody, real V4/V5 packet checks, full deployed CLI behavior, and any sealed campaign. R5 still declares `V007_PREREG_SHA256`, `PIN_ADDENDUM_V005`, and `PRODUCTION_K_BIG_A55` pending. This is an explicit source readiness limit, not a claimed new defect. The observed-contraction extrapolation remains its declared bound assumption; passing formula tests does not prove future contraction.

## Reproduction, custody, and scope

The first harness uses AST-selected pure fixture constructors from FIXTURE_SOURCE; it does not import that test module normally or execute its saved-R3 reads, subprocesses, CLI tests, or main. All row values, tau/sigma, grids, source parameters, certificates, and run identities supplied to the decision are synthetic. The tail library is loaded only for its inert config normalizer. Gate records are read from an in-memory fixture map while the gate functions themselves remain unchanged. Raw `read_run` is separately tested against exclusively-created JSON files, including the actual inherited adapter. An audit hook rejects saved-run paths, prohibited C5H/UVT paths, NGC paths, undeclared Research files, and .codex paths; no denied read occurred.

Artifacts and exact byte hashes are in the manifest. Main evidence: `PROBE_RESULTS_CX2V001.json`, `BOUNDARY_RESULTS_CX2V001.json`, `RPAIR_RESULTS_CX2V001.json`, and `FINDINGS_CX2V001.json`. The raw fixture directory is `synthetic_record_boundaries_v001/`; its every file has a byte hash. Scripts are `probe_compare_r5_cx2v001.py`, `probe_record_boundaries_cx2v002.py`, and `probe_rpair_branches_cx2v001.py`. The first boundary-script attempt, v001, failed at local AST selection before fixture creation; it remains immutable. Its v002 successor fixes only the harness variable collision. No reviewed source was edited.

0519 lensing work was stopped before artifact creation or tests; its directory was empty at the stop inventory. All execution processes in this lane have completed. Parent owns reporting and inbox monitoring.

## Source byte pins

The following hashes were recomputed from bytes. Open RULINGS is a snapshot, not a frozen authority pin. R5 and executed source dependencies were byte-identical at the start/end of each replay and at final review assembly.

| ID | Path | SHA256 |
|---|---|---|
| D0524 | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0524_2026-10-18_WITHDRAWN_0519_0521_0523_and_codex2_reassignment.md` | `d1430abc84025cc4afde31f3fd4fce1845e8d2334e47e95fbeb81936d7dfd4df` |
| D0514 | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0514_2026-10-18_codex_any_nice_waiver.md` | `50d4ab43ba3b2dbdc91330d5d3846010661871b654ac4c5a03b836cbb48ccd55` |
| D0527 | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0527_2026-10-18_all_lanes_process_caps_lifted.md` | `e662fd4d176f71b0d422f24a640f88b6dcccbeca5e4148a9fe3fc7062710a2e4` |
| RULINGS | `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md` | `c48a9433ec13d753972320f5e9e1e55d7881325e061be4e8a1a53b288ccb68e6` |
| R5 | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r5/kmax_tail_compare_c2v007_r5.py` | `78ac63b7a52a8746e96f390d0d5b46de4aa7ce5eaa27def6e54ef27330ce9755` |
| FIELDS | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r5/FIELDS_R5.md` | `736b8d7759484b7bbf90c0a430315ae23678d420020c9e2497c7ba6d3332dcfe` |
| FIXTURE_SOURCE | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r5/tests_kmax_tail_compare_c2v007_r5.py` | `13ce1c08a59fe52ba1977863bb56340740b96051b0501193db4d7c0157b5c716` |
| ADAPTER | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/kmax_compare_c2v005.py` | `49404bc4b0d558c93113ed650802d9009f03be64c364f0d862213783389786f5` |
| NORMALIZER | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module/owned_uv_tail_lapse_v001.py` | `c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22` |
