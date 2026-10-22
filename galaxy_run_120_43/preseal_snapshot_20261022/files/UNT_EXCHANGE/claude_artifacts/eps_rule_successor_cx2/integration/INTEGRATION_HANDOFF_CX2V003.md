# A296 full integration handoff — CX2V003, D017/F4

`date -u`: Wed Oct 21 23:26:00 UTC 2026

**BUILD REVIEW-READY; F4 Claude3 delta review and root adoption remain pending.** All 23 selected v002 sources are byte-identical. The new per-call acceptance consumer is appended as source 24. The exact ordered seven C1 proof producers are unchanged; the consumer is not a new proof producer.

Claude3 0320 closed F1/F2/F3 and its review of the 23 files stands. Claude3 0325 corrects the overall chain verdict to **FAIL, one blocker (F4)**: the old acceptance consumer refuses the honest A296 entry name before loading its wrapper. This D017 successor is ready for that delta review. Local author and independent PASS do not themselves change Claude3’s disposition or authorize production use.

- [0320_2026-10-21_A296-integration-delta-review-PASS-0-blocking-F1-F3-closed-D006-scoped-custody-pin-overall-integration-ready-for-root-adoption.md](/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0320_2026-10-21_A296-integration-delta-review-PASS-0-blocking-F1-F3-closed-D006-scoped-custody-pin-overall-integration-ready-for-root-adoption.md) — SHA256 `a6359bc45ebf1f4391a82fe0bd3cf10754a0fc8dbc3c7a2a6ab8305083506421`
- [RESULT_C3V002.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_a296_integration_c3/RESULT_C3V002.json) — SHA256 `ef6f71a6505662c69a7cb5ab4f103e0ee5b0242d68a0b450927f587a64b8146e`
- [0325_2026-10-21_R3-reviews-PASS-both-gates-NEW-blocking-F4-accept-call-refuses-A296-entry-D017-Codex2-one-line-successor-0320-erratum.md](/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0325_2026-10-21_R3-reviews-PASS-both-gates-NEW-blocking-F4-accept-call-refuses-A296-entry-D017-Codex2-one-line-successor-0320-erratum.md) — SHA256 `2485fd1cddb9270f37325d606200166aa05ffcb8881fb2f1123daef88d0193ca`

## Selected acceptance path

Select the new W1 per-call acceptance executable: [h3_accept_call_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/h3_accept_call_a296_cx2v001.py) — SHA256 `edcd3ffa647c143eeb2a942e46d2420d2126d9f61f33252be8c9126db1bba007`. Its only allowed changes are ENTRY_LINE, the refusal text naming that line, and module docstring/usage naming. CLI/options, residual-R1 rerun, locking, acceptance pass counting and reingest logic remain unchanged. Do not bypass this step by calling the handoff directly.

Keep the unchanged handoff: [acceptance_handoff_c2v004.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py) — SHA256 `5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8`. Root’s dependency record must bind the selected A296 wrapper guard: [certificate_guard_b1_a296_cx2v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/certificate_guard_b1_a296_cx2v003.py) — SHA256 `3939bc47c48f46f9e313969d77cc7895d7dd6936648b2060df31a5aff3cc4c25`. Its policy.approved_certificate_producers must be the exact ordered seven below, matching root’s approved C1/config. The old unfilled template still names the old guard and must not be treated as a ready dependency record: [ACCEPT_DEPS_RECORD_C2V001_TEMPLATE.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/ACCEPT_DEPS_RECORD_C2V001_TEMPLATE.json) — SHA256 `48ec0e010cd4228f6b3a7eab78940e956465af32d3d3e796efb41f4a7ca3bfa5`.

The consumer preserves equality checks; it does not independently impose a count of seven. Six deps against a seven-producer config refuses, while matching six/config and six/deps passes that isolated legacy predicate. Root C1, policy and native gates supply the exact-seven premise. No broader producer policy was introduced.

**TESTED:** author 36/36; independent 45/45. Bounded checks cover A296 and r12 entry acceptance, old/unnamed entry refusal, wrong guard, six-versus-seven and ordering mismatch, the restored-old-line mutant, and the exact permitted AST delta. Real selected function/predicate AST runs with synthetic loader/module/config boundaries. Actual campaign entry, wrapper/context, handoff, full accept(), production call and reingest remain UNTESTED.

- [BUILD_CX2V001.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/accept_f4_cx2v001/BUILD_CX2V001.json) — SHA256 `26be277209c29a41a179738e884d19ca998b0a6637c6962a29e587701d71b9fc`
- [TEST_RESULTS_CX2V001.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/accept_f4_cx2v001/TEST_RESULTS_CX2V001.json) — SHA256 `0a29240b9f6a95a1e8e8a5a08c9741fa178eeec580aa027e07edab6fe55a9bc6`
- [REVIEW_CX2V001.md](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/accept_f4_cx2v001/REVIEW_CX2V001.md) — SHA256 `82718c560342f9f9ea6dfda4e6f9fa6526004532c93a7078ba71dc922c862e74`
- [RESULTS_CX2V001.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/independent_accept_f4_cx2v001/RESULTS_CX2V001.json) — SHA256 `d6f951b83b9b7e1b65c2f1fd1a88f66853a1e70953078f41e0ec57c79160fbe7`
- [REVIEW_CX2V001.md](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/independent_accept_f4_cx2v001/REVIEW_CX2V001.md) — SHA256 `07b22625060d6b70626270c9c82759cf74c5a5c898619864742bc0ce7d1c3884`

## Unchanged C1 producer list and wider closure

Preserve the original six entries in order and append only the EPS bridge as seventh. Within the proposed C1 tail, only approved_certificate_producers and certificate_policy_review change. Custody, enumerator, frozen genesis and other tail fields remain unchanged. Rule, audit, core, guards, callers and this acceptance consumer are transitive implementation sources, not additional proof producers.

1. [point_response_admission_adapter_cx2v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/point_response_admission_adapter_cx2v003.py) — SHA256 `4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372`
2. [gq_producer_cx2v005.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v005.py) — SHA256 `2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd`
3. [lo_slot_proof_c3v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/lo_slot_proof_c3v003.py) — SHA256 `cd10cd59df44d7b79f3c3aa7ba88998d94c7292c4c2656e09bbbe16ded01bca3`
4. [lo_state_proof_adapter_c3v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/lo_state_proof_adapter_c3v003.py) — SHA256 `211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c`
5. [srb_rot_adapter_c3v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/srb_rot_adapter_c3v003.py) — SHA256 `08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a`
6. [current_source_evidence_b1_c2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/current_source_evidence_b1_c2v001.py) — SHA256 `7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce`
7. [point_response_admission_a296_bridge_cx2v002.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/point_response_admission_a296_bridge_cx2v002.py) — SHA256 `1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4`

The bridge/core, guards, saved stage, native wrapper, W1 generation chain, Step4 and scoped lookup/preflight/registry sources retain their v002 byte pins. Ordinary producer behavior and source digests remain unchanged. A296 authentication preserves original discrete failure, accepted-shell disclosure and exact reconstruction; approved signer review precedes proof emission.

The scoped custody helper retains strict request/output/public Snapshot boundaries. Its one exact production dependency is parsed from authenticated source literals only; target existence, bytes and hash were not checked by these build lanes. Prior one-read claims remain per Snapshot for BASE bootstrap and owned payload, not all imports process-wide. The old RAM-only lookup tests remain historical; the scoped synthetic-I/O tests and Claude30320 provide their separate reviewed scope.

Use final v003 lookup/preflight/registry and helper coherently. Under the new C1 use bound mode for every point and regenerate lookup manifests with final F1. The separate registry verifier requires the complete 31-point set; the inherited registry-bridge CLI remains legacy-only.

**Step4 needs the complete selected transitive source closure**, including rule/audit, scoped helper and selected acceptance consumer where used. The 24 active changes are not an exhaustive runtime allowlist. The existing exact standalone wrapper fence does not admit campaign-template or empty-seal owner hashes. Any actual generated wrapper used inside the fence needs a reviewed exact owner binding with unchanged buffer SHA256 `79e8936d96103b1540987a980b289b6d25e5e25941b02db647f7a833818da0e1`; no wildcard or invented post-verdict hash is supplied.

## R3 state and root-owned work

The three R3 signer records now exist. Claude30325 reports both stage/core gate checks passed; this handoff checks their bytes only. Root still approves their exact hashes, signer lane Codex3, the producer set and adaptation calls. The output root must not contain the signer-review directory. No actual EPS proof is claimed.

- [REVIEW_ROW302_CX3V001.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/a296_r3_signer_reviews_cx3/REVIEW_ROW302_CX3V001.json) — SHA256 `ca3fb3a2a118a9766fa9aae00ccd4b668e8835f4fcf61d0d96c6a13109f6936c`
- [REVIEW_ROW501_CX3V001.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/a296_r3_signer_reviews_cx3/REVIEW_ROW501_CX3V001.json) — SHA256 `5f9fd691252271c154602f062b2e4380af4828334215dcce86a87e1b721d7818`
- [REVIEW_ROW504_CX3V001.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/a296_r3_signer_reviews_cx3/REVIEW_ROW504_CX3V001.json) — SHA256 `48a599e2074a81e9e7c07e7bdc7482f6c4dd3aa06e4c4c977afd136469aee2ac`
- [R3_GATE_CHECK_C3V001.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/root_thu_checklist_c3/evidence/R3_GATE_CHECK_C3V001.json) — SHA256 `073b9c36035214bdb6fc01c6ce955db27702e58c5a4666d5ea799c795cfdeb76`

Remaining: Claude3 F4 delta review; actual root C1/policy and ROOT_BOUND binding; acceptance executable/dependency-record selection; exact command/direct_context/source reviews; point-review approvals and proof adaptation; real frozen31 custody verification and native preflight; B6/B6R regeneration review; actual post-verdict wrapper/config/admission and fence pins; W1 cache-ID bindings before any first-wave plan or work initialization. Rows302/501/504 still require actual EPS proof, rho, slot, bundle and final-spec chains, row302 first. Six-call L2 remains the baseline until the seventh-point chain is complete. Empty-seal r12 files remain review-only.

## Current pins

Full manifest: [INTEGRATION_CURRENT_PINS_CX2V003.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/INTEGRATION_CURRENT_PINS_CX2V003.json) — SHA256 `0e17b273f07871606e09756309e6e7e6ba15be206a95ab8c70bd2ac97853f6f8`.

Predecessor handoff (preserved historical state): [INTEGRATION_HANDOFF_CX2V002.md](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/INTEGRATION_HANDOFF_CX2V002.md) — SHA256 `866ea15674a1ed59475a5e68151449a5bc336481fc01ea09657241a89e0cfd44`.

- [point_response_admission_a296_bridge_cx2v002.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/point_response_admission_a296_bridge_cx2v002.py) — SHA256 `1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4`
- [point_response_admission_a296_cx2v002.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/point_response_admission_a296_cx2v002.py) — SHA256 `1a44bc59a5fc6a72c381d3c0c0875b6aa154c21fc108730d67c9ec529a39d9d7`
- [guard/certificate_guard_a296_cx2v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/certificate_guard_a296_cx2v003.py) — SHA256 `fe192884d983236806538272b52769e78fd13a54106e2eed9585b1c6279c02c9`
- [guard/certificate_guard_b1_a296_cx2v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/certificate_guard_b1_a296_cx2v003.py) — SHA256 `3939bc47c48f46f9e313969d77cc7895d7dd6936648b2060df31a5aff3cc4c25`
- [guard/eps_a296_guard_branch_cx2v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/eps_a296_guard_branch_cx2v003.py) — SHA256 `80a22d3eb97ac526ad3b930dee273a57ce3628cdbb8d38d319a0c721951899ff`
- [guard/calibration_orchestrator_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/calibration_orchestrator_a296_cx2v001.py) — SHA256 `c9fc5d16087526121d958c87a636350883a10d9b8e0b00abc273300ef872ec65`
- [lookup/eps_lineage_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/eps_lineage_cx2v001.py) — SHA256 `da5329e1f9530dc296b9592361cc86b7b480096f9514a9f4aba8cbfdd29c7abb`
- [lookup/a296_binding_cx2v002.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/a296_binding_cx2v002.py) — SHA256 `141c1cd291ece1899ebaa0308882e6b44a91bd8896738e233a94a28cc31bfe43`
- [lookup/registry_assembler_a296_cx2v002.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/registry_assembler_a296_cx2v002.py) — SHA256 `0f9283b86f47a1382c9c00173d70d8a4fd34fa20664400ca55ed3bbf3c9cf548`
- [lookup/cp1_points_common_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/cp1_points_common_a296_cx2v001.py) — SHA256 `24e848e43638482cb9595c5afb6c2bc2771c39c6cedb752f361baf6a73989ca1`
- [lookup/cp1_points_assembler_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/cp1_points_assembler_a296_cx2v001.py) — SHA256 `aa0fdc84539ac09bedbfe25932350410f3a3e17ad52caa348e818b85891478fb`
- [lookup/direct_cert_lookup_a296_cx2v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/direct_cert_lookup_a296_cx2v003.py) — SHA256 `bfcaa714555dcea236121071644f1de3ba34bd57e95dd631f36145d42094c2f1`
- [lookup/direct_preflight_cert_a296_cx2v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/direct_preflight_cert_a296_cx2v003.py) — SHA256 `3ae08ba9a4d442b5f21f64e421f5205d87c3b9ecb2531f03193c228385c999e0`
- [stage/cp1_saved_eps_stage_cx2v002.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/stage/cp1_saved_eps_stage_cx2v002.py) — SHA256 `0c9d0243c57bab053bb0a73e00183b0366b0c83b6eac33d9d5344b136238ccc5`
- [admission/step4_guard_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/admission/step4_guard_a296_cx2v001.py) — SHA256 `52cceaf71be65e6321041f7cbcff6c8eef0bc5ef0ac9503fe878fc459453ea93`
- [admission/step4_launcher_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/admission/step4_launcher_a296_cx2v001.py) — SHA256 `58a5a765ebd79e747bf6770388e0a38b9142ae5c6e81fbb93385c00295d461a2`
- [admission/step4_bind_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/admission/step4_bind_a296_cx2v001.py) — SHA256 `3194c6f363fff3a5f2c62f69d290122dd49b656af22c81e0c3c915f714ffe96b`
- [campaign/calibration_orchestrator_q5b1_ledger_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/calibration_orchestrator_q5b1_ledger_a296_cx2v001.py) — SHA256 `cb1f5e73753b69d1e8b6067c746b8fcda89d94d6bc4f34fb0a78f927e07cca04`
- [campaign/h3_campaign_entry_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/h3_campaign_entry_a296_cx2v001.py) — SHA256 `05738509efb85f1a64d0031bf0e1c6b0d96f3427ab1a5670704affcd47f4ff28`
- [campaign/make_campaign_cascade_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/make_campaign_cascade_a296_cx2v001.py) — SHA256 `114c90c301c07610eb1d6cd8ad27e5ced27691d42614556ff1a48a5dd58092e8`
- [campaign/regenerate_h3_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/regenerate_h3_a296_cx2v001.py) — SHA256 `2a69e63782ee29591eaa6b0d1abf311b072d6f304d6372cd56be0872254099a1`
- [lookup/registry_verify_a296_cx2v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/registry_verify_a296_cx2v003.py) — SHA256 `60ed81b58ea205a3dc61f43b58bfee47dee688fd2ab448ea1762f94e8b48a5e0`
- [lookup/custody_snapshot_cx2v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/custody_snapshot_cx2v003.py) — SHA256 `0af1b41b8dc04940dd244b453ed95e27d5a0e7dc2832fa5bf0e71d85fdd74b06`
- [campaign/h3_accept_call_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/h3_accept_call_a296_cx2v001.py) — SHA256 `edcd3ffa647c143eeb2a942e46d2420d2126d9f61f33252be8c9126db1bba007`

All cited hashes are from direct allowed file bytes. No pin references inside external documents were expanded, no production run data was opened, no scientific or native computation was repeated, and no existing file was changed. Actual production/adoption is UNTESTED.
