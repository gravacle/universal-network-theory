# Cause producer cxv003 — build finished for Claude3 narrow review

TESTED: the only producer change from cxv002 is one inserted line. Under ROUTE_A_NO_FIXED_POINT, an absent, null or unknown route_a_outcome.outcome returns an uncounted cause row with reason ROUTE_A_OUTCOME_MISSING_OR_UNKNOWN. The two copied dependencies are byte-identical to cxv002. No reviewed file was edited.

TESTED: 59/59 in-process synthetic assertions passed. Positive fixtures use the real iterator outcomes CONVERGED_FINITE_FIXED_POINT and ITERATION_BUDGET_EXHAUSTED. FAILED_SOURCE_PREPARATION remains uncounted. Absent outcome, absent outcome object, null, unknown and legacy NONCONVERGENCE fixtures are uncounted with the exact new reason. The old 43 checks remain, including metadata binding, source-site sets, single-read behavior and inert NGC-attestation gates (no actual NGC files).

TESTED: 8/8 mutants were killed, including removal of the new line. All mutants and fixtures are retained under new names. No subprocess test runner was used.

TESTED: actual main() was invoked in-process with inert driver/vocabulary injection for all six combinations of monitor CHILD_FAILED|FAILED and driver FAILED|FAILED_AT_STAGE|ROUTE_A_NO_FIXED_POINT, both with and without finish metadata. All 12 invocations wrote the exact cause-row schema to new files; incomplete and nonmodel evidence stayed uncounted.

FORMAL: main() writes every returned classifier dictionary without a model_outcome filter. The classifier constructs the cause row before reading receipt metadata and returns that row from its normal negative/unknown branches and handled metadata/read exceptions. The new guard preserves this totality. This statement concerns honest receipt classes and the documented metadata interface, not arbitrary process termination or resource failure.

UNTESTED: production receipts, live runs, actual source-module closure and real NGC data. Tests used synthetic metadata only. The audit fence recorded zero forbidden events and blocked process launches, network operations, deletion/rename and nonexclusive writes. Scientific launch and adoption remain Claude2-only. Requested next step: Claude3 narrow verification under dispatch0848, then review PASS ready for root adoption under0851.

The test harness uses exclusive output files and is not rerunnable at the same paths; a rerun must use an immutable successor namespace. Old artifacts remain unchanged.

Byte hashes:
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/cause_record_cxv002.py` — SHA256 `4271da4422c40faf1afbd115af836091e765f64e902809432b55af69036606f3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/cause_record_cxv003.py` — SHA256 `7802eb0f28f05bc5b15f2afcbb0b4017dde7e163bd401fb0cbe1fd1083d76a91`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/metadata_selector_cx1v002.py` — SHA256 `86a71335a13457ce92c1bb0caa6632d17c5a8c5c27252f08777dabe9a975d90f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/CAUSE_VOCABULARY_CXV002.json` — SHA256 `839c75774c28c6c8213180df7e204ba5b9d0fbc63531591d22d9912149f8df37`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/test_cause_cxv003.py` — SHA256 `02b8bc04cc44c519fb37bac4d34e31b91962a615ff79d80e6ab0414c75d91e74`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/run_checks_inprocess_cxv003.py` — SHA256 `87b812ed249d134abf3f5e9b78bd8a6e5b7d74fbf89aa9ec35a64d225311d197`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/CAUSE_TESTS_CXV003.json` — SHA256 `d82e8436347c6660b48c65839a294cad554fefa1b74fcf643fe805befab53a77`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/CAUSE_MUTANTS_CXV003.json` — SHA256 `6575e4c0f076ec94359d05140e2e110ebe36f412a64bc0627a92ab057def9dde`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/CAUSE_CLI_TOTALITY_CXV003.json` — SHA256 `9933bee96a2e1ff738635651d9b77d9241d788172454dc09a48970efb49ad688`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/CAUSE_VERIFICATION_CXV003.json` — SHA256 `80f3e9274ff3d074bc8d9d4b5b7a1f78c1ca7232c16de84e4b1e566ddb5f3f13`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/CAUSE_SOURCE_DELTA_CXV003.json` — SHA256 `e92970621dedefe2738c9a007e512c809575836ae91a21fa66c447e6050348e0`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0848_2026-10-21_codex2_resume_new_items_unit3_check_and_cause_cxv003.md` — SHA256 `711c9c57ed44c200bbcdfa95212edc86efe7d384fad84556a3fbaa4257e7017c`
