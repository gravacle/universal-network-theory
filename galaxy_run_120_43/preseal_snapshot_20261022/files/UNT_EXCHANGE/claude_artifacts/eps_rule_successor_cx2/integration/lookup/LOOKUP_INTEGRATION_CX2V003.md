# A296 lookup and custody-scope integration — CX2V003

`date -u`: Wed Oct 21 18:50:06 UTC 2026

**BUILT_TESTED_NOT_ADOPTED.** TESTED: helper/F1 78/78; F2 25/25; F3 77/77; F2/F3 static delta 8/8. These are bounded source and synthetic-boundary checks, not scientific trials. Production custody, full registry CLI and native direct preflight remain UNTESTED.

Use the final v003 direct lookup, direct preflight and explicit-bound registry verifier together with custody Snapshot v003. Only loading/calling the frozen custody deriver receives the exact internal path-and-hash exception. Public request, manifest, output and proof/slot reads retain the strict policy. The physical synthetic `runs` seam now reproduces the predecessor refusal and tests successful exact-pin reads, unpinned/wrong-hash refusals, nested-scope restoration and single physical reads under Python 3.12.14. No actual driver/custody/guard was imported or executed; no production run data was accessed.

The source scan verified all 22 previous source pins. After replacing the three repaired callers and adding the helper, the resulting 23-source set has no stale repaired-v001 path/hash dependency. The other 19 sources remain unchanged. No EPS-lineage, binding, guard, W1 or launcher/binder code cascade is required. The existing unbound binding template is unchanged; the exact C1 producer policy remains original six plus the EPS bridge.

Root must repin the selected command entry, direct_context, source allowlist and its exact source review, and publish new direct-lookup manifests whose generator is final F1. Use the separate final registry verifier with explicit binding path/hash for all 31 genesis points; the inherited registry-bridge CLI remains legacy-only. Old-generator direct manifests are deliberately rejected by the final preflight. Root C1/policy authorization and Claude3's independent delta disposition are separate prerequisites.

Earlier lookup/registry tests and cross-chain reports remain immutable predecessor evidence. Their checks do not establish the corrected physical I/O boundary. The manifest labels those historical fields explicitly and preserves unchanged dependency/frozen-input references.

## Current source pins

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/eps_lineage_cx2v001.py` — SHA256 `da5329e1f9530dc296b9592361cc86b7b480096f9514a9f4aba8cbfdd29c7abb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/a296_binding_cx2v002.py` — SHA256 `141c1cd291ece1899ebaa0308882e6b44a91bd8896738e233a94a28cc31bfe43`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/registry_assembler_a296_cx2v002.py` — SHA256 `0f9283b86f47a1382c9c00173d70d8a4fd34fa20664400ca55ed3bbf3c9cf548`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/cp1_points_common_a296_cx2v001.py` — SHA256 `24e848e43638482cb9595c5afb6c2bc2771c39c6cedb752f361baf6a73989ca1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/cp1_points_assembler_a296_cx2v001.py` — SHA256 `aa0fdc84539ac09bedbfe25932350410f3a3e17ad52caa348e818b85891478fb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/direct_cert_lookup_a296_cx2v003.py` — SHA256 `bfcaa714555dcea236121071644f1de3ba34bd57e95dd631f36145d42094c2f1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/direct_preflight_cert_a296_cx2v003.py` — SHA256 `3ae08ba9a4d442b5f21f64e421f5205d87c3b9ecb2531f03193c228385c999e0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/custody_snapshot_cx2v003.py` — SHA256 `0af1b41b8dc04940dd244b453ed95e27d5a0e7dc2832fa5bf0e71d85fdd74b06`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/registry_verify_a296_cx2v003.py` — SHA256 `60ed81b58ea205a3dc61f43b58bfee47dee688fd2ab448ea1762f94e8b48a5e0`

## Manifest and seam evidence

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/LOOKUP_FINAL_PINS_CX2V003.json` — SHA256 `1b4c7c2c9798efc0c37b7607c9da21fd68c48fdc05f5bc63edeee13c1cfe66d8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/A296_BINDING_TEMPLATE_CX2V002.json` — SHA256 `b882a15f934140f228b32caecc208586984511e7295928384c45042ced9767ca`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/LOOKUP_FINAL_PINS_CX2V002.json` — SHA256 `c2ed13a68aa2078b0e1c5209928fa81de69928821ae01cc38e318d161e1ceda9`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/LOOKUP_INTEGRATION_CX2V002.md` — SHA256 `cc39854eef96e9a254c32a4d769e41249141b6477dc2a6ea70da033489bb9192`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/custody_replay_fix/SNAPSHOT_F1_TESTS_CX2V002.json` — SHA256 `7e090f5e4fba030f5706135fe34aa49170b584f07191a9a150cd3a1f94238a55`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/custody_replay_fix/f2f3/PREFLIGHT_RESULTS_CX2V002.json` — SHA256 `4761bcd45dc063011c8c32a532010ea281e327484dc8b22f5074e2cb4d778b8d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/custody_replay_fix/f2f3/REGISTRY_RESULTS_CX2V003.json` — SHA256 `c84b14bfe983502b9778bc52b4c3987c9fb018f57f0999c3ba470dd27b25bdf5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/custody_replay_fix/f2f3/F2F3_RESULTS_CX2V001.json` — SHA256 `178e5d2ace64167f7233d0923b9a534295588eed5bcc95aa440b650462c297fa`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/custody_replay_fix/SNAPSHOT_F1_REVIEW_CX2V001.md` — SHA256 `668995cbb30dbb08ac6e061bb7245ab00bd1d41325d976d1c6054e9ff643ddea`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/custody_replay_fix/SNAPSHOT_F1_REVIEW_CX2V001.json` — SHA256 `709f654526234064e442d9a2faa4380f5d1ee43b8cc65ba0b46f2be678593d09`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/custody_replay_fix/f2f3/F2F3_REVIEW_CX2V002.md` — SHA256 `585a28864a2870a11b8a056545a95f9a98b7efe22e1d7c4209aecfe7ff78f905`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/custody_replay_fix/f2f3/CALLER_PINS_CX2V002.json` — SHA256 `a3a81b9a2aae3317183dfe0f3b1af271d8aaa5a39071c5415696898536d63c7f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/custody_replay_fix/AUTHORITY_D006_D013_CX2V001.json` — SHA256 `01bf12fb17fbaa4206dc8a32d0ed1a3753e5704ea60fe3bcf923392827644a3b`
