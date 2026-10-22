# Independent c2v006 counterexample closure

**PASS in this subtask — TESTED, 138/138 controls.** This is not a complete candidate approval; the parent integrates the separate A71, A73 and builder-selftest reviews.

`date -u`: `Sun Oct 18 16:18:13 UTC 2026`

Candidate bytes before and after: `097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48` (91,076 bytes). No candidate or prior review file was edited.

| Suite | r4 | r5 |
|---|---:|---:|
| Original source-audit counterexamples, exact and clean variants | 20/20 | 20/20 |
| Original structural templates + stage-order/renumber controls | 25/25 | 25/25 |
| Original invocation/value templates | 24/24 | 24/24 |

The new scripts start from our original 0553 harnesses, not the builder's ports. Every fixture is freshly published under this directory with exclusive creation. The port diffs and original/successor byte pins are in PORT_PROVENANCE_CX2V001.json.

## Owner-check evidence

- **Normalized key collision:** the original NEW extra dictionary contains `<new root>/x: tampered` and `<RUN>/x: same`. It FAILs **NORM_INJECTIVE**, with a **KEY_COLLISION** detail naming both exact raw keys. This assertion prevents a false closure due only to reserved-marker rejection.
- **Duplicate JSON and NPZ:** they FAIL **STRICT_PARSE** with **DUPLICATE_JSON_KEY** and **DUPLICATE_NPZ_MEMBER**, respectively. The NPZ fixture retains the original conflicting first member and good last member.
- **Structured dtype and storage order:** renamed structured fields in both NPY and NPZ, and C/F changes in both containers, FAIL **STAGES**. Scalar signed-zero/type changes and ordinary payload changes also fail their assigned checks.
- **Stage membership/order:** earlier/later/both-side and middle-of-three aliases, empty extra stages, missing/renamed stages and a swapped reference/route-A order FAIL **STAGE_SET**. Merely renumbering the same ordered stages passes.
- **Ordinary data:** unknown nested result value/presence changes FAIL **RESULT**; input changes FAIL **FILES_INPUTS** or **INVENTORY** as appropriate; finish changes FAIL **FILES_TOP**; attempt-result changes FAIL **FILES_ROUTE_A**.
- **Invocation:** repeated/malformed/foreign-stage tail flags and ordinary argv changes FAIL **REQUEST**. A Z2 NEW base script fails **SCRIPT_CUSTODY** even while its declared replace-mode token set passes TOKENS_POLICY. Wrong hashes, symlinks, dtype changes and extra stage aliases fail their assigned checks.

Full reports are retained for all cases. Every MUST_FAIL checks the responsible check by name; normalization and duplicate cases additionally check the stated diagnostic. Source-audit cases also reject COMPARATOR_EXCEPTION as a substitute for successful detection. All positive baselines and benign controls pass.

## Explicit expectation changes

1. The exact old source-audit baseline contains literal `<RUN>/x`. c2v006 now reserves normalizer output text, so this exact original baseline is expected to FAIL **only NORM_INJECTIVE**. Its original negative variants are retained, but each must fail its own owning check. A second complete set uses a plain-key positive baseline. In that set, ordinary/JSON/NPZ/dtype/storage mutations do **not** fail NORM_INJECTIVE; their intended checks detect the defect.
2. Original invocation P17 accepted equal logical NPZ values stored C versus F. c2v006's explicit ARRAY_POLICY includes `fortran_order`, so the successor is named F17 and must FAIL **STAGES**. This agrees with the new policy rather than claiming the old expectation was unchanged.

## Limits and execution hygiene

**UNTESTED:** real scientific output identity and production acceptance. No `gates_v006/out/IDENTITY*`, `records/R4`, production `runs`/`runs_ext` tree, C5H, any UVT run, NGC target/observed velocity or session log was opened. The comparator's actual `main` ran in process only on owned synthetic files. Driver modules and checkpoint code were loaded for static constants/serialization; no scientific entry point, subprocess or network operation ran.

An installed audit hook denied prohibited paths and process/network/destructive actions, and allowed writes only by exclusive creation under this directory. No audit-blocked attempt was recorded. All runs used the prescribed isolated Python, numpy/stdlib, and single-thread environment. `nice unavailable (sandbox); 0514 waiver`.

A possible duplicate-dictionary-key issue in the NPY header's `ast.literal_eval` was independently noticed during source inspection and relayed to the parent/A71 lane; its independent canary and disposition belong to that lane. The PASS here concerns the 138 specified controls only.

## Files and byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/run_identity_compare_c2v006.py` — `097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/BUILD.md` — `fedbc6157037e2e1c847e7211b9ed9519193c99185bc4ce2362783384bb647d1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/DIFF_c2v005_c2v006.diff` — `ded144d333a50eaa0f0d45a36850f104227ed348a5db1abcff46c6658bd6621b`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0564_2026-10-18_codex2_crosslineage_review_comparator_c2v006.md` — `332ed9d11fc069b772673b50d07b5db678d11fb68cad13a152ea470c5173103d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/test_whole_gate_edge_cases_cx2v001.py` — `4b2635f65472bdca319f3d4aafbac4b0e908e033fa3dca5d69d43d8cf33267fa`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/whole_gate_r4_v001/RESULTS.json` — `43100d17ed420ba2276f28805d983d69e804af30c2d911ad4c2a0537b9a0a6de`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/whole_gate_r5_v001/RESULTS.json` — `dbec0cde7de9e3fc9351c9fd56364dae6e441bfd0926765e97c5f9192a129528`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/run_20261018T161555_80192/STRUCTURAL_RESULTS.json` — `74b77b6c02bb38d6c14635fd92a3af5d636288e41fda542b433f341bc200bfee`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/run_20261018T161705_82693/STRUCTURAL_RESULTS.json` — `c144999df3846e834fb61a4c15d070a8fe32d69186b594a84b7b74754b0f96db`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/invocation_r4_v001/RESULT.json` — `6427eec100217c62c6a0de8850a46b0b3bd1e40e49b4ec6c754c99a4d73faafc`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/invocation_r5_v001/RESULT.json` — `e1f225fcd7d305ef11996424996a1bf8dabf20edabb14fc24ed9367c36ecc4b7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/PORT_PROVENANCE_CX2V001.json` — `950916f8788075a55b94d225376b55ab7340bf7822b29c66802a6c98521ccda4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/guard_cx2v001.py` — `b6c741172795a8ee2e769063a80faefc9795ee27b338ae0ab9990a620a7848a1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/test_duplicate_npz_members_cx2v001.py` — `3f94c347ec5714873c0e61326aba5df50f5f88dd1d07b7cc2bce567596c4c8db`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/test_whole_gate_counterexamples_cx2v002.py` — `73aeca5ffd9fe0e5ea06c3110243fe9eb22472c45c2f0d75eacc7acbf60ab6c0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/common_structural_cx2v003.py` — `db5d7dabecb5306d834eaf07ccf6881f4152a9c147fa107ad53ede5b2aff576e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/common_structural_cx2v004.py` — `bb5b98a4ce66e146715b4a6d0ff28e10558189ff644bb1ee657a65b7f026709f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/run_structural_canaries_cx2v002.py` — `7d924e33374183dd1935cf31c93cb154ca444cce9965feced2956b943046ad7e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/run_structural_canaries_cx2v003.py` — `e69359cd19e6cc6a2e4b2e7166715cb2d7684753c666c037af0d60ff9c13c960`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/invocation_canaries_cx2v003.py` — `711580269ba37be0fc6c4e7206c27ca5427d56b7a558e1247cff8e44172ce72e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/invocation_canaries_cx2v004.py` — `bfac48c4a31f992926b8ff0bdf19b15a91e7a17e19549e3028a4918f7cbf13c3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/PORT_DIFF_00.diff` — `90111041d63a6cbb395f87c6a128f9a68b24974c3f7742e457160554e247403b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/PORT_DIFF_01.diff` — `895d8ad30eabe6237cf2b36c9b3e355fcbdd9eb80749886f541436a8d8f48c37`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/PORT_DIFF_02.diff` — `d34e6bd3a9e1463dc88d30e1ff77554236f2a07e622004930159b7179b1c5091`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/PORT_DIFF_03.diff` — `e7a6b294a30e3050add1012a3629865b2b8a897aa1d8378f8a1ed517b05039d3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/counterexamples/SUMMARY_CX2V001.json` — `aee6fd408b8fe463712fc87ec5598d7a855710e8392c44c76e6e53c9bf737bb4`
