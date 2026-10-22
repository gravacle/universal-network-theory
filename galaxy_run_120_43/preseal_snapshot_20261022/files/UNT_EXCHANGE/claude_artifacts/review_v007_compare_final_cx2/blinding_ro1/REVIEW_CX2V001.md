# Independent r10 blinding and RO1 review

date -u: Sun Oct 18 17:13:53 UTC 2026

**FAIL — 3 BLOCKING, 1 SHOULD_FIX, 1 NOTE within this slice.** Candidate SHA256 e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93. Source and published document hashes remain equal to the parent start pins.

TESTED: source plus owned synthetic fixtures. Main controls 221/231; ingress/priority follow-up 34/34; CLI code-only expectations 0/6 (six leaks). Combined 255/271. Counts do not replace the finding/coverage distinctions below. `nice unavailable (sandbox); 0514 waiver`.

BR-B1: two identical fired RO1 events pass actual C4T and nodes C4T-D5 public case validity, while single-event controls also pass. A75 explicitly includes B10 among the required guards. The loop at L2020–2036 validates each event separately and never rejects repetition. Packet/I1-T positives are isolated test premises; no full scientific adoption was established.

BR-B2: actual Z2 and Z2-OFF identity validation accepts column_workers 0 and -1 with a valid parallel worker and DDO binding, returning valid=true and no codes. Positive count 1/8 controls pass. The exact owned records show identical worker/binding/driver/call-spec pins and only the normalized count changing; every result/receipt has its correct new byte pin. L2570–2573 checks integer type then treats every value other than 1 as parallel. Require a positive admitted-attempt integer first. Picard isolated-member corroboration is reported separately because its mutated base would fail ordinary base registration.

BR-S1 (BLOCKING by A79 / dispatch 0578): unknown flag, invalid route-mode choice and abbreviation each echo a CLI-controlled numeric canary in both blinded modes. argparse prints first and raises SystemExit(2), which main’s Refused/Exception handlers do not sanitize. This is a CLI-string leak. The original 13 record-derived early-refusal routes now pass all 26 route/mode owning-code and no-leak tests. Repeated ordinary flags and repeated validity-case labels refuse correctly.

BR-S2: strict parsing detects duplicate JSON and names safe object/member indices. The public side/attempt wrappers discard these locations and emit only *_UNREADABLE:DuplicateKey. They fail closed, but do not satisfy A75.3’s requirement to identify both entries. Preserve the safe position code without echoing record text.

BR-N1: worker_sha256 list/object values raise TypeError inside check_ro1_record. Public validators catch the exception and return invalid; no acceptance bypass was observed. Type these fields before hash-map lookup for a typed diagnostic.

Coverage includes DDO/nodes serial/parallel positives, cross-family and cross-binding negatives, both identity paths, own-route R-PAIR and admitted-base Picard checks, optional unarmed records, raw result/attempt/start/finish/receipt duplicate parsing, failed-call rejection, hash-only scope and nine decision-priority controls. A77’s family table and A53 admitted-base rule are preserved in positive controls.

The context is an owned surrogate built from a pinned static prereg and prior independent case-block metadata. Tail hash-normalization is skipped via check_uv_link=False; packet and I1-T validity are explicit positive premises. Priority tests substitute only declared upstream status producers and retain actual evaluate_v007. Full production/sealed CLI adoption, raw producer-start reconstruction, a C5H Picard-specific member and the restricted numerics-only reader remain UNTESTED. No supplied suite ran.

Guarding covered reads and stat/list metadata before import; actual protected C5H/UVT roots were never accessed. Main reader tests replace the registered forbidden-root set with an owned surrogate. No launches, target reads, network, destructive operations or existing-file changes occurred. No active process remains.

A79 / dispatch 0578 was read before sealing: the CLI leak is BLOCKING. Its all-gates seal-marker prohibition and production-128 conjunction supersede the older prep expectations; those bindings are reviewed by the parent’s separate lane. Prior prep files remain unchanged.

Every cited file below has a byte hash; HASHES_CX2V001.txt also covers all owned fixture files and recorded static inputs.

| Reference | SHA256 | Path |
|---|---|---|
| candidate | e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r10/kmax_tail_compare_c2v007_r10.py |
| main_result | 35dbc074dd1cf9d5527707f87894f5821d9b1ac6e9f47e57156d9cf7e512b64a | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/fixtures_20261018T170950_92776/RESULTS.json |
| followup_result | 14950c2ff8e7b8a94f2c03ab74220716fe5ebaf5253250ba8d9cb72c06ba86ad | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/fixtures_20261018T171127_95755/FOLLOWUP_RESULTS.json |
| early_cli_result | a9c40bdc7a6d5fb37d43c8e4d2382c548313856e400b12da6d3a9178f4906c12 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/EARLY_CLI_RESULT_CX2V001.json |
| main_harness | d4f17810442daad3481ee0d73bfc3cecf4438f5728d24826b0f388de4102d32e | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/probe_blinding_ro1_cx2v002.py |
| followup_harness | eb1f1a51ac99e366d4a7823dab94b96e68c7531f41817bc33a844a8f694ac663 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/probe_ingress_priority_cx2v001.py |
| early_cli_harness | 67bf9b19370036b862b1938d26cec32b2d4273dd97d69bdf43c188e0fb3608d1 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/early_cli_cx2v001.py |
| impl | fd6f877910e89c5a9b182e92d3cb95faa8285581d6f000e05e7b0c48c0a1ad06 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r10/COMPARE_V007_IMPL_R10.md |
| fields | 03655a02f08fdd59c6ea36f18a2a782bd80c7940d15df515db364fadd0bc8029 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r10/FIELDS_R10.md |
| candidate_manifest | eea462d18e7a7189ba40e5dc378499c54cec4b4d17e2dfb30bf6ce7a88c8af87 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r10/HASHES.txt |
| input_pins_start | cd140f3c02c5a58bdbf79bf508708842f47309ee1015b5b20444a366172bac6a | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/INPUT_PINS_START_CX2V001.json |
| open_rulings_snapshot | 2da736b5f4f8f6c007035996218f98838c2766b4a4daf11ca62ab3d3ec254827 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/OPEN_RULINGS_SNAPSHOT_CX2V001.md |
| a77_preparation | b7c77d5f5232eff27cd36f8bcb1ffc30a3eccc55e04573bf62c12086aa85abd5 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/prep/A77_RO1_PREPARATION_CX2V001.json |
| original_preparation | 727bb76e6876aa07a0ce8154546fee1ad92439921de9783b6a8c07999059db14 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/prep/REQUIREMENTS_TEST_CROSSWALK_CX2V001.json |
| dispatch_0578 | a2f5da46fb70441cbeaa47b96e3d32a64b9ef9a642f3b3286166de7f01bf29c8 | /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0578_2026-10-18_codex2_claude3_r10_interim_rulings_A79.md |
| root_A79_observation | 4c68b462a419c2e4524fc6cb65e5c08040980bd070dd607db300c0783a7430f5 | /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md |
| dispatch_0573 | 3fc3b734d56025d836a8e366d8fb4eace322f6382cabde2cd9f96da9d13b452e | /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0573_2026-10-18_codex2_claude3_A77_2_per_case_family.md |
| sealer | 2c53755afe8252e62595a2e8b1c52ebb95e88294d8dbae8ec0a3521447dc58a6 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/seal_review_cx2v003.py |
| identity_count_evidence | aedca59bf5ee9e47782c39f117ef176586f38a3e785092d16a3b9683b65907dd | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/IDENTITY_COUNT_EVIDENCE_CX2V001.json |
| findings | 2245210673be7154f8bfe446838717615634be45f4685350ebba6c7cc0e0a0d5 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/FINDINGS_CX2V001.json |
| coverage | eb55f6ae2679bcc897a83e78b14f3425040d988b29c0815c3ba8c4aaff297059 | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/COVERAGE_CX2V001.json |
