# cw8 Phase-1/2 v003 — 0842 review packet

date -u: Wed Oct 21 13:37:52 UTC 2026

READY FOR CLAUDE3 NARROW DELTA REVIEW; NOT ROOT-ADOPTED.

TESTED: 502/502 controls, including all 421 inherited checks, 39 additional selector/custody/CLI/locking controls, three kit-relaunch controls and 39 snapshot controls. The saved synthetic kit relaunch with fresh fill path and identical bytes passes history, close and closed-receipt verification. Changed SHA is refused. Malformed forecasts/comparators produce durable serial records, including non-dict forms and numeric overflow.

TESTED: 15/15 targeted mutants killed. Nine reproduce the custody/CLI survivor patterns named in the combined review: root license equality, write-time watcher guard, legacy-role widening, history check, restore license authentication, prediction derivation, choice producer, default serial choice and full-cw8 root spec pin. This is a new targeted set, not a claim that the reviewer's entire 24-mutant set was rerun. The shape-guard mutant is caught by the specific fallback reason; its fallback still remains serial. The other 14 mutations violate acceptance, refusal, binding or single-choice behavior.

TESTED: two concurrent metadata threads on the same real synthetic work root produce exactly one cohort record, even when both Contexts cached calls beforehand and their forecasts disagree. Removing the lock creates CW8_CHOICE_DUPLICATE in both contenders. No processes were launched by this contention test.

TESTED: snapshots refuse missing/null cause rows for eligible solo FAILED attempts and reject wrong monitor bindings. Valid bound model_outcome=false/unknown-reason rows pass; non-solo and post-cutoff failures retain their prior behavior. The synthetic G26/combined suites use the root-preserved calibration fixture; no old scratch fixture is read.

FORMAL: implementation delta is three changed launcher functions plus one lock decorator, one changed builder function and necessary version/consumer pins. Scientific sources, raw-spec worker-only rule, selector cost model, status maps and Phase-2 cutoff remain unchanged. The durable empty lock inode is never overwritten or removed. N2/N3 rulings are documented in the contract.

UNTESTED: production comparator/forecast inputs, measured speedup or memory use, real kit relaunch/snapshot, distinct review and root adoption. Only synthetic saved metadata, source/AST checks and fenced metadata tests were executed. No scientific driver, monitor, sampler, comparator, target velocity read, protected run read or network operation occurred.

All development artifacts are retained. Two adverse-fixture location mistakes and a kit-test API/fence mistake were corrected through new test successors; the initial v003 implementation bytes are unchanged. The validation record lists those failures.

Review inputs and evidence (SHA256 from bytes):
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v003.py` — `4d5b47e75f90241460dd0b86155ddae2267117c31f6043fc57777ea94564919d`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v003.py` — `f710334b6f5ec2663fbebd826c7b326ebf7ff9eb600e751584de4f518a4e0b11`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/g26_freeze_cx3cw8v003.py` — `171710bb5428d7baa9e05fda049c1095239ea5461eae351abbbacea1d608fa89`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0842_2026-10-21_codex3_cw8_v003_F2_sha_only_plus_hardening_before_0838c.md` — `704951f325ca1adb8de119d6a624c1ab7f6b7c881fb6c70bdc01d664b6d9498f`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/BUILD_0842_CX3V003.json` — `c549a9c46a9029ab2966092ef3d2540460c7c43aa6cce45eaee0a86e0bb2c2eb`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/VALIDATION_CX3V003.json` — `541d11886c9c460ec50c59ece02487f77cff4454f4aea74915849022a7dc4774`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/MUTATION_CONTROLS_0842_CX3V003.json` — `26e90ca0075b1ce9f6494d57268226e126b8301bd8299b663ed82581185ef0b3`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/ROOT_METADATA_CONTRACT_CX3V003.md` — `16c6f3e478d19c952d51cb300cde21df45be98e9ed014fb430673e12203e8c9c`.
