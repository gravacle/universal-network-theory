# A205 campaign-set review, Codex3 v002 — pending one input

Date (`date -u`): Tue Oct 20 14:57:26 UTC 2026

**Status: REVIEW INCOMPLETE. Zero A115 blocking findings in the checks completed below.** Part2 check5's production HEADLINE11 spec-construction comparison remains pending the exact named inputs requested in0662. This is not the final campaign PASS packet.

Codex3 wrote none of the reviewed production set. Concentration disclosure: Codex3 holds generator/output-diff review, campaign-set review, certificate-policy signing and per-wave EPS signing. Signer gate and request-form findings below are **same-path**. Codex3's22 EPS signatures already feed the genesis registry; this review does not independently re-certify their science.

## Tests

TESTED — H3 c2v002:94/94 twice. Campaign certification c2v004:90/90 twice (58 MUST_PASS,31 MUST_FAIL,1 INFO per run). IDs, expectations and pass outcomes match between repeats. Additional isolated adversarial boundaries53/53; independent generator checks36/36. Handoff idempotence has a separate isolated probe.

All four passing suite runs used new distinct Codex3 runs-roots, pinned Python -I -B and BLAS1. The exact pinned suite bytes ran through an audit wrapper. The audit records478 instrumented processes,135 distinct loaded program/input paths with byte hashes, zero access denials, and maximum observed Darwin peak RSS109297664bytes. No scientific driver subprocess was allowed: only the pinned suites, pinned monitor and exact synthetic mock bytes. No target or forbidden run file was read.

Harness limits and substitutions are explicit. The original suites declare synthetic producer/custody/driver substitutions. The outer wrapper preserved128 redundant hard-linked temporary names instead of deleting them; no existing input was edited. macOS refused setrlimit; a per-process RSS watchdog guarded8GiB instead. The H3 retry test needed approved read-only process-table access. Earlier own wrapper failures (resource-limit setting, local gethostname, audit destination) and the sandbox-only93/94 H3 run are retained; they are not production defects. The generator's audit caught one optional Python cache-read attempt, then loaded the pinned source; no cache file was opened or written.

## Findings and confirmations

1. **TESTED / FORMAL — generator, no blocking.** `make_campaign_cascade_c2v004.py:161` keeps policy transformations, tuple validation and core generation identical to the Claude4 v002 parent. AST/source checks confirm the unchanged rules through campaign generator versions001–004. No-tuple SUBv006r10 produces published policy93d9c0ac, coredc895f8a, ledger-wrapper source7c9b4248 and only the entry WRAPPER path delta. Inert tuple build differs from its no-tuple build by2/1/1/1lines and its policy equals the A129 inert policy. Malformed C/P/A/schema/V controls refuse. This does not approve a real verdict tuple.

2. **TESTED — acceptance and reingest, no blocking under A196's operating rule.** `h3_accept_call_c2v004.py:211` checks first-pass schema, adopted handoff, call directory, pass directory, pin and INCOMPLETE reading. At246 it refuses a third pass and rechecks pass count under the lock. `h3_campaign_entry_c2v004.py:101` binds accepted content to the call/receipt/bundle; wrapper:108/119/623 checks latest pass. Suite EB14,EB26–EB33 and the added boundary cases cover refusal of frozen first readings, missing/wrong/stale pins, third passes and stale reingest records.

3. **TESTED known residual R1 / FORMAL scope — non-blocking under A115.** Suite EB34 INFO confirms that a direct handoff call outside the acceptance step can bypass the first-pass condition. README c2v004 §5 and A196 already rule that root operates campaign handoffs only through h3_accept_call_c2v004. Requiring the first-pass record on A002 at both reingest entry points is deferred. The check is conditional on that explicit operating rule; it does not claim the bypass is mechanically closed.

4. **TESTED boundary / FORMAL wording note — no wrong admission demonstrated.** Wrapper `write_acceptance` at320–340 is idempotent for an existing identical handoff and refuses a different handoff. An isolated exact-method probe confirmed same-pin repeat leaves bytes unchanged and different-pin repeat refuses (certificate checks were synthetic stand-ins). Therefore an unconditional statement that every VALID path refuses mere handoff-file existence would overstate these bytes. Invalid reingest explicitly refuses the existing accepted certificate at472; latest-pass and same-call requirements still hold. No new cache class or re-roll was demonstrated by this idempotence case.

5. **TESTED — F6, no blocking.** Acceptance step:102 maps ACCEPTED/PASS_FLAGGED to cached VALID; INCOMPLETE allows at most the one post-export rerun; other readings halt unless eligible under the two ruled invalid readings. Wrapper:455 and651 bind certified MODEL_INVALID to the same finished call, result, registered point and latest acceptance pass. Provenance:681 carries judgment_call=true; these entries do not count toward D5 TESTED-NEGATIVE. Suite EB15–EB25 covers both invalid readings, invalid/accepted/incomplete cross-cases, reuse and byte tampering.

6. **TESTED / FORMAL — ledger, no blocking.** Wrapper:364–453 and693–759 check exact policy path, canonical hash-chain sequence, key/identity uniqueness, registered proof bindings and re-derived planned spec before appending under lock. Config/cache identity binds genesis+policy, not changing ledger contents. Full suite EA/EB verifies new-point refusal, certified append, unchanged cache ID, later planning and reuse. F03 verifies removed points refuse on use after truncation. The isolated probes test torn/noncanonical/hash/sequence/key defects; certificate science is stubbed only in those isolated probes. Source/genesis lookup and wrapper physics values remain unchanged.

7. **TESTED / FORMAL — HEADLINE evidence reading; production-construction item pending.** `h11_evidence_assembler_c2v001.py:180` verifies FINISHED/COMPLETED receipt/result bindings and an ACCEPTED adopted-handoff record of that call, with no stop. At223–264 all nine exact probe-spec hashes must be covered once before run_mode_admitted=true. H01–H04 verify that capability-row meaning and refusal of changed spec bytes, wrong receipts, foreign acceptance records and incomplete/stop readings. `reuse_test:150` consumes the entry's status normalization hashes; it does not invent a second normalization algorithm. However test helper h11_specs:532 makes both sides with the same mapper. The production HEADLINE builder/spec inputs have not been authorized or compared here; request0662 is outstanding. Actual post-C1 spec equality is UNTESTED.

8. **TESTED / FORMAL, same-path — CP-1 list mode and EPS signer admission, no blocking.** `cp1_points_runner_c2v001.py:104` delegates table mode to pinned c3v004; list mode validates pins/keys/rows and preserves its anchor gate and worker environment. List assembler requires complete wave bundles and consistent EPS source pins. Runner:143/202 passes explicit approved signer lanes to the existing gate. `s4rc1_common_c3v004.py:477` refuses excluded producer/operator lanes, unapproved/missing signers, missing distinctness and templates. Own six signer probes confirm Codex3 requires explicit approval and Claude2/Codex2 remain excluded. c3v004 runner:594–602 writes the list-mode request form from the exact numeric/point/custody/adapter bindings; adapt_point:889–945 rechecks these and the root-approved review hash. No review is produced by the runner. This confirms admission wiring, not independent approval of Codex3's signatures.

9. **TESTED — storage, no blocking.** `storage_check_h3_c2v003.py:62` counts every regular file in the call directory, including post-acceptance exports; allocated/apparent maximum and inode deduplication are used. Suite S01–S04 and own export fixture confirm this; threshold regression gives17.08GiB for the documented synthetic inputs. Real volume capacity and real b remain UNTESTED and are root's later measurements.

## Remaining scope

Pending: named production HEADLINE spec-construction comparison (0662), and later actual final C1/config/ledger/verdict inputs. Real list-mode producers/custody, scientific outcomes, real HEADLINE layout and live campaign execution were not run. No scientific launch approval is given by this review. Verdict/C1/wave posts preempt the remaining campaign work in that order; minute inbox polling continues.

## SHA256 from bytes

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_campaign_set_cx3/SUITE_SUMMARY_CX3V002.json` — `a1963efe1bcc3f51f665600c385c6f5894041dae263bb53f39fa40bb66d1aa7e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_campaign_set_cx3/ADVERSARIAL_RESULTS_CX3V002.json` — `90ec8ce5a9f355f91ab511a4ad202c696fe64b697b867a20f843e3c8ce53cf15`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_campaign_set_cx3/GENERATOR_REVIEW_CX3V001.json` — `4762cd60a55fe1fa4c0ee458bfc590c79d85de018f3146034dad781c2179f8c6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_campaign_set_cx3/HANDOFF_IDEMPOTENCE_CX3V001.json` — `e90181cb0c2e349b5679e40b1e642f8ed4326d200f8dc2b8a0e81f8f6edc61b5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_campaign_set_cx3/run_audited_suite_cx3v003.py` — `84a99c7028346ae6f4f23f84043e73dbadb92998757f700f373feb9049c95b65`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_campaign_set_cx3/adversarial_checks_cx3v002.py` — `b14af345fb8ea53f0e7e7105cca4916b44600377470b3aafbb1370a1cb959923`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_campaign_set_cx3/check_campaign_generator_cx3v001.py` — `37690af7588e0aae35c60339fdd5a051295e0645c8f9a8e5c1e260842b7dc322`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_campaign_set_cx3/check_handoff_idempotence_cx3v001.py` — `ade0d5b48f513e0e72c8bda43ee808720e5d57cfe84576da203efa24df6d7572`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/h3_campaign_entry_c2v004.py` — `cbdf0d49b8bfa09bccf8ba1ebfb518f8c00b663c2564db7c3a02c8b7a86e116d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/h3_accept_call_c2v004.py` — `eb895263c8458696b265b30dc5dee771dcb89649e5b490c893bb613281c7bf19`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py` — `7c9b42483773a9e95fa8b3af9aaef972025fda2cfe071ada8d0092393fbda229`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/make_campaign_cascade_c2v004.py` — `5014b04f0de3cf2fc0289dcabe519e0056f9395302cfd1b9b4082b4d045b228a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/regenerate_h3_c2v004.py` — `ad5cee08650b78d3e012a874dcde6afdad39a9cfd17146a35422802ac8db346e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/cp1_points_runner_c2v001.py` — `3c6a5ba3195711d4f00e812620582db4a8dc5b2c7a0a8387f9fe730ff6153d89`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/cp1_points_common_c2v001.py` — `302abdad6b076190f7bc8e79cc71cf4de91402a1a216eb94c254acf2be22c27e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/cp1_points_assembler_c2v001.py` — `951e7203a676afe3cdf566d54970cf5a7d574fbb4cc4c485cd628aca2c0da3af`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/h11_evidence_assembler_c2v001.py` — `2a8df9dfb85933b0cbe27af791d6966537537aea9e37d90fe82b6106195b33ee`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/storage_check_h3_c2v003.py` — `8eee1f68ac7395c11be0046ccc11f1a24efbec1e4d62bc064111de099c8a01aa`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/apply_h3_fields_c2v003.py` — `02addc1d687c9d6d6e7ca26a0fe220540261133afee5074a0e89b5c32e11cc20`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/build_adoption_derivation_c2v001.py` — `01a4cbae729a0c44df2ea1f4cc500ae95669cb9ff6a7541bc94621c23c2294bd`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/README_CAMPAIGN_CERT_C2V004.md` — `638d6543d09cf8305235197ea42ed9c3530f13bc531743b012466c8ba68dc9c1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/CAMPAIGN_CERT_DESIGN_MAP_C2V001.md` — `29071333cfa40a88f7c86cd737a34ff7b2350d80265e19e566fe84aa891724e7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/HASHES_CAMPAIGN_CERT_C2V004.txt` — `394880b6d6672395ccf69dc28e6c7e483dbed2ee8aa780ded10d1d30fffdbfa1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v004/cp1_runner_c3v004.py` — `3f5e5c188d4a6967afdb3bfab805d1cc8650e9c26793895096be55ca8f4f1a48`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v004/s4rc1_common_c3v004.py` — `53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0768_2026-10-20_codex3_A205_queue_verdict_diffs_campaign_review_policy_reviews_wave_signer.md` — `2aa4d476714dbb0cef053c7c525b80cba290b0ed7698dc5c853537ce57586eef`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0771_2026-10-20_codex3_campaign_suite_scratch_mutation_confirmed.md` — `633d88eccb1e9a6f9a72893e1c631ff939bfba37ba26fc57032eee601f247bda`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0662_2026-10-20_A205_HEADLINE_spec_construction_input_request.md` — `3cc96bc253943fa37b31ae57fc4c4db6c9ae499dc5142cce3461a656f2a491c4`

Additional source pins (exclusive successor, `date -u`: Tue Oct 20 14:57:54 UTC 2026):

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_campaign_set_cx3/CAMPAIGN_REVIEW_PENDING_INPUT_CX3V001.md` — `190eec66013b8ecc7d31fd7107a6610934ab83cd080d6ff0cc0d636cadbe8c7b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/tests/test_h3_campaign_path_c2v002.py` — `6705c949b504aac4cfd994710c0beea8abd2775ef347ede2dff986035f2caa1d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/tests/test_campaign_cert_c2v004.py` — `52d0420206718a73e92ec89779deebe49ea90bf367cd8db798cf68e427be748e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py` — `dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/b1_policy_successor_c4/tools/make_b1_cascade_c4v002.py` — `a7a5fe58d509b99f14cb000305633c6f192ac71f5093f4ec5fa1a2fa6f1a1f35`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` — `79a42b07301d34aea67afd10aa5c74a999ade6e1660aadb825ddbc3f58cd5713`
