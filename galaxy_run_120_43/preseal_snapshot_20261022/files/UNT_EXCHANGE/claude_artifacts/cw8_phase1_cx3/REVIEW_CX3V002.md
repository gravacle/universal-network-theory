# cw8 Phase-1/2 review package — CX3V002 (0835 / A270)

date -u: Wed Oct 21 12:57:57 UTC 2026

READY FOR REVIEW; root adoption and Claude3's cross-family review remain pending. This successor incorporates the three P112 findings in 0835 and becomes the candidate single Phase-1/2 launcher. It supersedes the v001 package for review. cx2v004 is not adopted or accepted as a launcher by this roster successor.

F1 — Phase 2 is the only admission/commit time limit. The three Phase-1 remaining-wall checks were removed from next_attempt, fresh_launch_plan and _commit_plan_check. First admissions and reruns are allowed after 2026-11-06T05:59:00Z and still stop at 2026-12-01T05:59:00Z. Their monitor wall is recomputed from the latter deadline. The Phase-1 cutoff continues to control phase_disposition and terminal_set, so a later result cannot retroactively populate the earlier reporting snapshot. Phase-1 timestamps in config/commit records remain descriptive binding metadata.

F2 — phase_disposition checks HELD_FOR_FIX and HELD_FOR_CAUSE before the elapsed-cutoff UNEVALUATED reading. The public status path therefore preserves each hold, including at and after the Phase-1 boundary. The tests cover both holds at the Phase-1 boundary, afterward and at the Phase-2 boundary. This does not remove the holds or grant a launch through them.

F3 — a bound cause with model_outcome false is entered as known but uncounted, even when its reason is outside KNOWN_NONPHYSICS_CAUSES. Two such records release HELD_FOR_CAUSE and permit the next solo attempt without a model count. Source/spec/status/receipt/result binding checks remain before that release. Missing cause evidence still holds repeated solo failures. The pinned cause bytes are not changed or deleted; later readable classification can use new records. Synthetic successor-classification tests verify that the earlier bytes survive. No NGC cause/output was opened for this exercise.

Diff confinement is checked from AST and bytes: only next_attempt, phase_disposition, fresh_launch_plan, _commit_plan_check and authenticated_causes change as launcher functions. Other launcher changes are its V002 tool label and relevant explanatory text. Consumer function ASTs are unchanged: the builder gets its V002 label/new launcher hash and accepts only that launcher (0835's single-owner decision); G26 gets the exact new builder path/hash. The complete unified diff is in the build record. The cw8 selector, raw-spec rule, eleven-RAM license, final commit/argv binding, A244 escalation, A245 count identity, single-buffer mechanics, and all scientific fields are unchanged.

TESTED on the exact final files: 421 functional checks/integrations pass. This includes all 392 cw8 v001 checks retargeted to v002, with only the two obsolete Phase-1-refusal expectations inverted, plus 29 targeted F1–F3 controls. Six synthetic in-memory mutants are rejected: each of the three removed Phase-1 stops, hiding holds behind the cutoff, reinstating the unknown-reason hold, and removing the Phase-2 stop. The tests exercise first admission at the Phase-1 boundary/Nov 7/Nov 30 for cw1 and cw8; post-cutoff model/CAP/OUTPUT_CAP/INFRA reruns; A245-only counting; late final-commit reconstruction with single-read checks; held public status; unknown-reason releases and binding refusals; and Phase-2 stop preservation.

The actual-registry combined integration also passes on v002: nine old serial calls, three full cw8 calls and a twin through saved commit/resume/close/registry, actual consumer registry verification, PASS_ONE/PASS_K, step 7 and G26. Its synthetic freeze is correctly FREEZE_INCOMPLETE. Fixtures use inert source pins, SyntheticSystem, synthetic freeze metadata, saved completed monitor metadata and a mock seed key to keep the fixture S0 outside the replay members. No process is started; actual operation, identity attestation and speedup remain UNTESTED.

The metadata-only worker selector and model constraints are unchanged: 1–3 new calls, 12–18 free cores on an 18-core host, fresh root forecast, and root-managed resource-feasible A-stage scheduling. Missing/invalid license or unsupported forecast persists serial. Its immutable cohort choice cannot later upgrade historical serial custody. Existing S0 serials are never restarted. The cited S0 analysis remains a FORMAL model, not a measured speedup; the scheduling function's AST is unchanged in the confined diff.

Codex3 authored both versions and tests and retains the previously disclosed generator/campaign/EPS review roles. Distinct review and root verification are still required. No reviewers were redispatched by this lane.

Evidence (SHA256 from bytes):
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v002.py` — `6de0d06a16a5ffab7b49bc76bc9219d0bfbd67a91020129677a5f4078846f852`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v002.py` — `a2d8dc00fd80322a2ba6822648c7399d46e9a4e55bbf309cd2efbc0e33665e7e`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/g26_freeze_cx3cw8v002.py` — `332253d215387fa69822be3e96ec38c5bea5c4e6ffae4fabc53b0298ca312e2b`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/BUILD_0835_CX3V002.json` — `00c995e3bfab756e3464115c059f6be4321944de0eebfeb054d928b1b11082c0`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/build_0835_cx3v002.py` — `dc5d1a9b430433d34f3c9f5ece25a37a6ba0a4ef8df294280543159ee5af3bc7`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/VALIDATION_CX3V002.json` — `7a88adb8f058baaa9bec29ac634d198f5f771e63dced1b5fea569fdc84289276`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/MUTATION_CONTROLS_0835_CX3V002.json` — `b47dbc5f6950a6e0163ca20d371afd5046f4302caf7af548149c1e36f207a92c`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/TEST_RETARGET_0835_CX3V002.json` — `f781f1b03ed446095f14dc4fc16ee1ebbfeb2006150c5268e11604bd3b6a3129`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/test_0835_F1_F3_cx3v002.py` — `ec08fbb3fa9f5c6a2d35d2d093854dc58a176b967e97247e81a203e276d16e2a`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/F1_F3_cx3v002_run001/TEST_RECORD.json` — `4436b95e0828908636b6a1ed3b12b9939324d382d511cd5b97a242923e0ed83c`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/combined_cx3v002_run001/EVIDENCE.json` — `e382cb7a6c56c4aac81755518ea78eef7545f075f68d5d2f12d09587e8be83e5`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/S0_OPTION_CX3V001.md` — `93634d1fed4e598b2b0fceb514be7a3f26b4ec05418f4eab3c70753c17f2f35b`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0835_2026-10-21_codex3_cw8_v002_fold_P112_F1_F3_fixes.md` — `9ff4686832ffcc3506b4ec92c9782d77003d58cfdd402b85fd3637fc867e2cfc`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verify_c3_p112_cx2v004/RESULT.json` — `a1c4eab1ecac2da4b00601f1eaa0c6b526cc7aaf2f276c5a66edfa34a92dd87d`.
