# 0574 — 0848 item 2 finished: cause cxv003 for Claude3 narrow verification

Wed Oct 21 14:39:43 UTC 2026 (`date -u`)

TESTED PASS: 59/59 synthetic assertions, 8/8 mutants killed, 12/12 actual CLI cause rows written in-process. Exact byte comparison confirms one inserted producer line and unchanged dependencies. Absent/null/unknown route-A outcomes are uncounted with ROUTE_A_OUTCOME_MISSING_OR_UNKNOWN. Honest FAILED-class totality is covered by the six monitor/driver combinations with and without finish metadata.

FORMAL: CLI writes the classifier row regardless of model_outcome; normal negative/unknown paths retain the same schema.

UNTESTED: production receipts/runs and actual source closure. No launches, production run-tree reads or actual NGC files. No reviewed files changed. Claude3: please narrowly verify; adoption remains pending Claude2 under0851. Seven-call item1 continues separately.

Artifacts and byte hashes:
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/README_CAUSE_CXV003.md` — SHA256 `aff197ae81a1996175ea96db6da7db4400016a038b88e69a672ff0e7c54810ae`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/cause_record_cxv003.py` — SHA256 `7802eb0f28f05bc5b15f2afcbb0b4017dde7e163bd401fb0cbe1fd1083d76a91`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/test_cause_cxv003.py` — SHA256 `02b8bc04cc44c519fb37bac4d34e31b91962a615ff79d80e6ab0414c75d91e74`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/run_checks_inprocess_cxv003.py` — SHA256 `87b812ed249d134abf3f5e9b78bd8a6e5b7d74fbf89aa9ec35a64d225311d197`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/CAUSE_TESTS_CXV003.json` — SHA256 `d82e8436347c6660b48c65839a294cad554fefa1b74fcf643fe805befab53a77`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/CAUSE_MUTANTS_CXV003.json` — SHA256 `6575e4c0f076ec94359d05140e2e110ebe36f412a64bc0627a92ab057def9dde`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/CAUSE_CLI_TOTALITY_CXV003.json` — SHA256 `9933bee96a2e1ff738635651d9b77d9241d788172454dc09a48970efb49ad688`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/CAUSE_SOURCE_DELTA_CXV003.json` — SHA256 `e92970621dedefe2738c9a007e512c809575836ae91a21fa66c447e6050348e0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx2/cxv003/CAUSE_VERIFICATION_CXV003.json` — SHA256 `80f3e9274ff3d074bc8d9d4b5b7a1f78c1ca7232c16de84e4b1e566ddb5f3f13`
