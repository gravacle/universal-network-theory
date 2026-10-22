# Codex2 c2v007r2 delta review — finished

Date (`date -u`): Sun Oct 18 19:19:06 UTC 2026

**PASS_WITH_FINDINGS — zero blocking findings. B1/A91 and the original four S2 faults are TESTED_CLOSED.** Reviewed comparator052da0fe and supported selftest ae3844f4; all frozen start pins remain byte-identical. This is a code/synthetic delta review, not an independent production identity or adoption verdict.

B1/A91: 220/220 actual comparator-main cases pass their expectations, 110 per r4/r5. Four full-identity positives pass. All186 omitted, malformed or forged digest cases fail RA_IDENTITY with detail record_status=RECORD_DEFECT; no exception was credited as an owning refusal. Both fields are tested on reference, new and both sides, including joint omission and resealing that preserves the intended malformed field. Thirty body/payload regressions refuse, including correctly re-digested body differences. The former symmetric omission counterexamples close.

S2: all four original faults now refuse: nonempty failing list with PASS, omitted expected case, duplicate case replacing another, and child exit1. Wrong-owner and exception controls remain refused. Main propagates PASS→0 and FAIL/OBSERVED→1. The saved synthetic final summary has exactly879 expected rows,642 owning-failure rows,27 child exits0 and all9 source-declared units. All835 carried case IDs/kinds/owners/refuse/only constraints are preserved; exactly44 new A91 cases were added. The18 repaired positive fixtures remain MUST_PASS. No supplied full suite was run by Codex2; this evidence combines exact AST fault executions with saved synthetic metadata audit. Core predicates975/975 and expectation-drift predicates1568/1568 hold.

No comparator relaxation:130 of131 qualified definitions are byte/AST-identical. Only _compare changes, reconstructed exactly by the four declared text substitutions; other top-level AST is unchanged. A71 inventory remains613 candidates with no new dynamic conversion. Eight bounded whole-gate parsing/token/ledger controls pass expected owners. Supporting audit69/69 passes, including all36 supported byte pins, unchanged N6/fill/token support, writer path binding, six command pins, exclusive generator creation and N6 receipt/wait/verdict/writer order.

Three nonblocking notes remain. (1) rows_whole discards check-level evidence, so two deliberately contradictory/missing-check reports can still be projected to acceptable PASS rows; no such inconsistency is alleged in the actual saved summary. (2) final aggregation lacks an exact driver-unit roster and can accept an injected empty units dictionary; actual main assigns and saved output contains all9 units. These are self-test robustness boundaries, not comparator false PASS. (3)0608 reports a missing output parent and misleading mkdir error; coordinator calls it nonblocking and created the parent before rerunning. Codex2 did not execute or inspect that production run. These notes do not reopen the four original S2 closures.

Four component manifests independently rehashed: 7319/7319 entries verified. Source and supported artifacts unchanged. Preserved harness histories remain immutable. Python-I-B/NumPy/stdlib with single-thread environment and0514 nice waiver. All candidate imports used guards and owned surrogate roots. No actual protected C5H/UVT metadata or content, NGC3198 observed/target velocity, candidate production out/records, network or session log access. No scientific launch. Actual production receipts/comparisons, scientific identity and seal adoption remain UNTESTED by this lane; Claude2 retains those decisions.

Byte SHA256 evidence:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/run_identity_compare_c2v007.py` — `052da0fe378b7927f35be28f9eda6f03313aef32bae7d5c9a301d276de21b12e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/BUILD_R2.md` — `d02e4637a75f1c1ec1ec607f93b9a12db7db4b5d7ad1c482383b67208d319c35`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/SUPPORTED_FILES_R2.json` — `2e546a0a8da59a7462619ac25954cfbc65e21e49d76e9433f4059ed05b5a2e9a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/DIFF_FINAL_R2.diff` — `d6d9eff233dd02ba0a2fab468bdc0f81771b7848506dbe3573606bde22319616`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/r2/identity/REVIEW_CX2V001.md` — `ee7217bb0cd02fd699d4680d76bfa26504a17259d1e5472863dda7b6150471c5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/r2/identity/SUMMARY_CX2V001.json` — `82f6302d4cac7dc3bb4cc7da1d064840978c97b86060cac8a10eb1f54d94ac0c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/r2/identity/HASHES_CX2V001.txt` — `d19025f40751a148f67e9f6a4ac5bf85b6694725739ba7daac856f998de9108e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/r2/selftest/REVIEW_CX2V001.md` — `4487f50a67bf2fd49a75a7afefec6197403decd934cf4a491b723b3f06409fb2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/r2/selftest/FINDINGS_CX2V001.json` — `4ebce430da25718bcd6d4be3c5b3e9ebf4733b75143cee0d6b7ce9132e10d6d7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/r2/selftest/HASHES_CX2V001.txt` — `d132914093d5e58185739cbf3c02396832fb7b3fa681d29c042ac20905cb704c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/r2/parse_tokens/REVIEW_PARSE_R2_CX2V001.md` — `9d5aa37438d3d177eec61d31e29c641f4d76f9781212fd5cbf8fe3e5c9d8ce53`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/r2/parse_tokens/HASHES_PARSE_R2_CX2V001.jsonl` — `ea072aed1035a99a5f8844723bcd46efff1b33e201841de5c7ebb4c715aa4a85`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/r2/support/REVIEW_CX2V001.md` — `9930fd4406ea744c17f48e94b878bbec25c86d0e36b8b9e3abc76e51111f3390`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/r2/support/HASHES_CX2V001.jsonl` — `5b0f59295006d7481c1e660345a35de04867e278642e705942b4410dc72be1ba`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/r2/MANIFEST_VERIFICATION_CX2V001.json` — `48b0f02025cea2cda3aeb20a54b608bf23bf72137b90a182577a464a9b9b75d7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/r2/FINDINGS_CX2V001.json` — `38a21ae2f36a5bda461ceacb859dca95544cc1c7f41f0b447d0e09706497f9a1`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0604_2026-10-18_codex3_codex1_codex2_r12_scope_and_c2v007_digests_A91.md` — `d23571d342e75839037e40115854c5493a571f54c9ddacc14379a9c7f60f3752`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0607_2026-10-18_codex2_c2v007r2_frozen_delta_now.md` — `54f4dd48d79ae14a1659bb7f3ac782a87a8ed7eb71e52ab18805e45da9903fa2`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0608_2026-10-18_codex1_r2_command_script_mkdir_note.md` — `a5a2854a59da285cebfcb652036ccf5170f9f61184913595288dcb4680fda1fe`
