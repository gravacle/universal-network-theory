# cx3r007 dry-plan identity and registry

Date -u: Sun Oct 18 17:48:33 UTC 2026

**PASS (TESTED): 78/78 case outcomes and emitted-artifact identities match r006.** These are 61 completed nonempty dry plans and 17 matching refusals. Refusals are not plan passes.

The unchanged canonical ordered 78-spec set is `155b1095984c393426c90b43ec744e74a7d05f0f3628b26d017926d448caa875`. All 78 spec byte pins were checked before the run and again in comparison. The r006 baseline is reused from the prior successful suite: all 2,060 prior output-manifest byte hashes were verified, and the selected 1,012 baseline logs/artifacts are pinned individually and reverified before comparison and sealing. No baseline rerun or duplicate baseline outputs were needed. Earlier r007 candidate runs are preserved and excluded from the selected-source result.

Compared 934 emitted artifacts: 377 raw-equal, 557 equal after identity-only substitutions, zero residuals. Closed artifact substitutions are the successor self path/full hash and per-case output root. A derived full hash is admitted only after the same-relative-path artifact is already byte-equal under proved substitutions; each proof and use is retained. No JSON fields are ignored, no arbitrary identity digests or short hash prefixes are normalized.

Separately, exit values, exception text, stdout/stderr, read/write sets, simulate-only Ctx modes and RO1 call traces agree. Traceback metadata additionally maps the current harness path to the prior harness path. Independent AST proof verifies all 295 parent nodes and prefix bytes, the inactive forwarding factory, 48 original-function registrations and the unchanged inactive selector return. Across 17 refusal cases, exactly 51 frames at the proven inactive forwarding return are removed and 17 inactive selector-return source lines map by AST identity. Every raw frame and mapping is retained. No active strict frame is removed or mapped. These metadata rules never apply to emitted files. Normalized read sets remain exact; no eager dependency-read allowance is used.

The new registry pins r007 from bytes and preserves exactly the eight previous NGC source-readiness fixture specs, in their original order. Registry adoption remains controlled by Claude2 acceptance.

Audit: zero blocked events, zero overwrites and zero scientific stages. The prescribed isolated Python runtime used numpy/stdlib and single-thread BLAS, with six bounded dry-plan processes. Successor peak RSS: 363282432 bytes; peak across retained baseline and successor: 363282432 bytes, below 8 GB. macOS rejects RLIMIT_AS; the inherited wrapper records that host limitation and checks observed RSS during calls and on completion. This is measured memory evidence, not a guaranteed hard address-space cap.

**UNTESTED here:** scientific launches/predictions, malformed-record strictness/RO1 correctness (the parallel review lane), and cases beyond these 78 specs.

Byte pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r006.py` — SHA256 `c2930e18eb2ba6f691dcaffffd56658143490ab366552cf90b27506a2357be49`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r007_cx3v004.py` — SHA256 `e4f5864aee796febf133aa03e2bf3236a9fc566971c5d2f0f5d3e2d6b226ea69`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/plans/INACTIVE_DELEGATION_PROOF_CX3V004.json` — SHA256 `35d667d81f59fcca87e517abebc600fb13ddbe0413a0b69b2d006233685c162b`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/plans/COMPARATOR_CANARIES_CX3V001.json` — SHA256 `24240e08fed0f140d795efc2a7bcf699461474a4327a9926ce4733dd3b2555a2`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/plans/BASELINE_CUSTODY_CX3V001.json` — SHA256 `f125190b93eb8dfa42429116a868d62710965206d2344b8bba7831c5d0e549dc`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/plans/SPEC_SET_78_CX3V001.json` — SHA256 `6b91a8f2c2b226402b34d5c1cc863027cde4d27ddece9a1d22fa96f3e32f87bd`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/plans/DRY_PLAN_IDENTITY_CX3V004.json` — SHA256 `fdb783639b361d0fa69b5be0b977ebe86a9cc86fc3db64d5530147d2bc5e9b3b`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/plans/SPEC_REGISTRY_CX3R007_V001.json` — SHA256 `cd30429c27ced0837dc383c00f78899a758fefeeaae2f6134e6aae7fcad18ea2`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/plans/INPUT_HASHES_CX3V001.json` — SHA256 `565fb841850168a5d4aea745fa8f0837e5e425b695b491c70a5ee77a1840d72e`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/plans/DECISION_CX3V001.json` — SHA256 `d706eecda7808352f3683d6c4e1e7fc835ddb7ec2b12813f45514c16d7913f5d`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/plans/RUN_S_CX3V004.json` — SHA256 `ece8bb3aee35aaa871cd606568553efb614d4eee5416d46f16d8573dee91e374`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/plans/dry_one_cx3v001.py` — SHA256 `f05a3eb41d9e81c693ed402c49a85b556d3e458e943f47f346c7b206a995dcb8`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/plans/compare_cx3v004.py` — SHA256 `99a134d23b01e410d55e720d078ae0c1d31f5c89f959e17b4f673a1dbc7309f6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/plans/seal_cx3v004.py` — SHA256 `3bf7b204cdd99e71790cb3cbb57d230df37178f1e2361504743c51da6b194f2b`.
