# Comparator c2v006 — A73 presence/absence review

`date -u`: Sun Oct 18 16:17:23 UTC 2026

**PASS_WITH_FINDINGS for this A73 lane.** SF1, SF2 and SF3 are absent. N3 remains absent from the inherited fill tool, with no v006 replacement. N6 is partial: comparator-verdict checking is present in the record writer, while executable receipt-status checking is absent. A73 expressly allows these should-fix changes in c2v007 if c2v006 lands without them. This is not an overall PASS for the comparator; the parent integrates the independent A71 findings.

**TESTED: 20/47 requirement predicates pass, 27 fail.** The failed predicates demonstrate the specified missing restrictions; they are not unexplained harness failures. Positive and negative controls are included. The candidate source matched the supplied sha before and after execution. No real run or production identity report was read. Scientific comparisons remain UNTESTED in this lane.

| A73 item | Presence | Evidence |
|---|---|---|
| SF1, full RO1 key set | Absent | Both armed and unarmed records accept extra events_suppressed/custom_payload keys. Exact valid records pass and inadmissible_record still refuses. |
| SF2, only driver-derived triples | Absent | r4/r5 policy accepts arbitrary verdict/numeric-string pairs for Z2, Z2_OFF_RO1 and B0P. Z2 reference/label substitutions also pass. Actual normalization erases those string differences. |
| SF3, selected driver static pins | Absent | With r5 selected, an arbitrary own file and an r4-only pin are admitted by matching bytes alone. |
| N3, firmlink/NFD containment | Absent in inherited fill | Both aliases name the registered scratch inode but pass the lexical containment guard. Plain and marker controls still refuse. |
| N6, receipt status and each verdict | Partial | No v006 command successor. Old command tests existence; v006 writer checks each comparator verdict but not receipt status/exit_code. |

SF1 is at check_ro1_armed/check_ro1_unarmed (source lines 1206–1217). Their named-value checks do not constrain the key set. The RESULT rules remove the new-only RO1 object as checked by RO1. Require the exact registered key set before that declaration can excuse the block.

SF2 is at tokens_policy (918–945), token loading (1331–1333) and the normalization chain. Policy verifies successor presence and excludes some inappropriate successor/base values, but does not establish that every complete [ref,new,label] triple belongs to the A59 derivation. The metadata in the token file is ignored by main. A fresh non-derived CONVERGED→NOT_CONVERGED pair and a numeric-string pair each pass policy and become equal under actual Side.norm. These are policy/normalizer unit probes; this lane does not claim a whole-gate false PASS. The separate A71 lane found post-join label non-injectivity; that is a distinct mechanism and is not counted again here. A selected-driver derivation allowlist must constrain all three columns and reject extras.

SF3 is at static_pin_verifier (1268–1276). The predicate only hashes the raw path stored in its reverse map. It never consults DRIVER or a table. The own arbitrary file and cross-driver pin probes confirm this directly. Hash validity is necessary but does not establish declared membership.

N3 belongs to the fill tool's generic containment layer, not the comparison Tree inventory. The bundle provides no fill successor; the inherited c2v002 guarded_resolve uses casefolded lexical containment. Scratch firmlink and NFC/NFD pairs were confirmed with os.path.samefile before probing. No actual C5H path was passed. Existing marker protection remains effective for a marker-bearing scratch path, so this is not evidence of a bypass of the real C5H marker restriction. A filesystem-identity/normalization-aware containment successor remains required.

N6 is a source-only inspection; neither the command script nor identity-record writer was executed. The old script checks -f on receipt files and ends with wait/cat. The v006 writer records status and exit_code but never predicates on them; it does explicitly reject comparator verdicts other than PASS_BITWISE_EQUAL. BUILD's request to wait for FINISHED is prose, not an executable status guard. The dispatch/A73 calls this N6; the original c2v005 CHECK labels the same command-script note N5 (its N6 is a port caveat). This numbering difference does not alter the requested fix.

All probes use fresh scratch fixtures or source-derived configuration tables. Imports were inspected and guarded. All production runs/runs_ext, C5H, NGC targets, session logs, production gates_v006 identity reports and R4 records were prohibited; no prohibited operation was attempted. No network, subprocess, solver, launch, deletion, rename or overwrite occurred. Python used the approved isolated interpreter with single-thread environment settings and the 0514 nice waiver. The open A73 addendum is cited at its observed bytes, not claimed frozen.

Files and SHA256 from bytes:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/run_identity_compare_c2v006.py` — `097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/BUILD.md` — `fedbc6157037e2e1c847e7211b9ed9519193c99185bc4ce2362783384bb647d1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/DIFF_c2v005_c2v006.diff` — `ded144d333a50eaa0f0d45a36850f104227ed348a5db1abcff46c6658bd6621b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/tools/make_tokens_c2v006.py` — `21f9df0f7442f4de121b5425ce60d448e292f9ba69e4c700ffc056ebca6cc4d7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/tools/write_identity_records_c2v006.py` — `ecee65a4d52920adc5f3c0dfe6f1fc7fa343909142cc56da6d3ac8ccaefc13b2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v005/tools/fill_picard_member_c2v002.py` — `0235398dc1b0ec7b3a80c4e552abdbcce81659f5d80f33c371dea875c18f6c2a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v005/R5_IDENTITY_COMPARE_COMMANDS.sh` — `d790f312e762524172d3f5716ffb37819753883b73d66c59b132d1285f2ba3d6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v005/check/CHECK.md` — `6f08a8dd03541cc697b690cc8a2c1f948c9a5a4a7d39565a8ff097a734f77f1e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/a73/probe_a73_cx2v001.py` — `90e1f58bc67d3d903967725f2a3cb2c1dbc02d1e3a5db1ba909d2f726a5056e7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/a73/run_20261018T161641_81032/A73_RESULTS.json` — `dfc74816e75be6a7dd19ee6c6ad6e0fe529d663f40ef278736b0bce4660c2883`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0564_2026-10-18_codex2_crosslineage_review_comparator_c2v006.md` — `332ed9d11fc069b772673b50d07b5db678d11fb68cad13a152ea470c5173103d`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md` — `a28c6828b6b8a43fe8c58186948410f7ff1fa9cb11793b57445a6d9ba344fcac`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/a73/A73_PRESENCE_CX2V001.json` — `cae55d2e77774b32883b169974df7dddf4b4c3f872e13f03f20d2f45cfa456db`
