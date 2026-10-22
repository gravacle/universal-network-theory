# Post-C1 pin trace — root0859 / deputy0330

`date -u`: Thu Oct 22 03:43:51 UTC 2026

**FORMAL: no C1 source-pin successor is required on the A296 bound path.** All24 selected source hashes match. Exactly two active source files contain the old C1 path/hash: lookup’s unused global constant (zero AST loads), and binding helper’s required frozen lineage. Preserve both. The legacy cx3v001 pair cited by0707 does enforce oldC1; it is not the selected new-C1 path.

**TESTED:23/23 author AST controls.** The exact binding validator accepts a synthetic non-v001 C1 tail and refuses v001/unbound/malformed policy/tail substitutions. Exact lookup prefixes (including real legacy prefix), preflight35–41 and registry72/81 argument statements demonstrate propagation/refusal. Old unbound legacy remains supported. These are projections with RAM docs and inert module/source-read stubs, not full caller or replay tests. No synthetic ROOT_BOUND file was written.

- [BOUND_MODE_AST_TESTS_CX2V001.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/post_c1_prestage_cx2v001/trace/BOUND_MODE_AST_TESTS_CX2V001.json) — SHA256 `b15b49769eef5e2c36689dde487659ad2a46dc91e3128f752d2985148150e2a3`
- [test_bound_c1_ast_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/post_c1_prestage_cx2v001/trace/test_bound_c1_ast_cx2v001.py) — SHA256 `c21f332c9c953e6f56b7f1a39c1968241e2e921a5ac6d88de154d14f90db945b`

The new C1, its C1-policy re-sign and root-written binding are data inputs. Binding fields to fill are status, c1 and certificate_policy_review; frozen_c1 stays401593. Policy must equal newC1.tail_readiness.certificate_policy_review. Root’s writer additionally rejects synthetic/draft/non-successor documents; the binding validator alone is not author authentication.

The final lookup accepts exact request keys schema,records,verification,c1,genesis_registry,approved_producers,a296_binding. Records and verification must carry the same new binding; verification.c1 must equal binding.c1. Their existing assembler generator stays unchanged. No previous PASS can be rebranded merely by replacing C1 text.

FinalF1 main calls validate, replay, publish. publish requires _replayed_binding and emits MANIFEST.generator=its own unchanged pin and verification_replayed=True. Real replay invokes custody. Metadata-only tooling must prepare the authenticated inputs/root replay command, or consume genuinely replayed outputs; it must not synthesize a replayed manifest. CLI flags are --request, --request-sha256 and --out-dir.

Admission metadata selects direct_context=finalF2 and direct_certificate_lookup={request,manifest}. sources is a full path→SHA allowlist; source_review.approved_sources must exactly match it with a real distinct PASS. The24 changed sources are not the exhaustive transitive closure. Existing Step4 binder calls full validation/native checks before output, so it must not be run merely to prepare metadata. No concrete production command/admission predecessor was supplied in0859/0330; require explicit pinned inputs.

Acceptance has no C1 path/hash field. Root fills deps.guard with3939 and policy.approved_certificate_producers with the configured ordered7; enumerator remains unchanged. The handoff5ff464cc remains selected. The template contains null dependencies/reviews and must remain nonadmissible until root fills them. Equality to config does not independently impose seven.

**Policy role constraint:** binding uses the C1 policy re-sign. FinalF2 also requires config.tail certificate_policy_review to equal that C1 pin. W1 campaign policy is a separate re-sign binding newC1. Do not conflate these pins or claim the same config satisfies both roles without the actual reviewed context. This is a source constraint, not a production compatibility test.

**UNTESTED:** full caller execution (separate independent lane), actual rootC1/policies/binding, real custody/replay/native preflight, acceptance/campaign, binder/launcher and source-review/admission publication. No production source changed, no project modules or custody were imported, and no run dependency was accessed.

Full machine-readable trace: [C1_PIN_TRACE_CX2V001.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/post_c1_prestage_cx2v001/trace/C1_PIN_TRACE_CX2V001.json) — SHA256 `81899629c69c0d240d7eae902031e3defea6dc8c6f8203f0d515c17be1969b89`.

## Evidence pins

- [0859_2026-10-22_codex2_prestage_post_C1_pin_successors.md](/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0859_2026-10-22_codex2_prestage_post_C1_pin_successors.md) — SHA256 `e9e51aa7e6b3d7dce35a63b4ba2509da2216fbd135a73e6e73e77917226890da`
- [0328_2026-10-21_0857-delivered-A296-chain-checklist-C3V002-root-waits-marked-pin-verifier-78of78.md](/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0328_2026-10-21_0857-delivered-A296-chain-checklist-C3V002-root-waits-marked-pin-verifier-78of78.md) — SHA256 `18cd819eef9c4300331d9ef44734605691039ecdd9ad3e2adfba388b92765177`
- [0707_2026-10-21_0856_future_C1_lookup_pin_dependency.md](/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0707_2026-10-21_0856_future_C1_lookup_pin_dependency.md) — SHA256 `40e7cff358a66cdb034f73a23ffe9072ef16ea88a9391dccc95b7cb1cd159167`
- [0330_2026-10-22_ack-0858-0861-deputy-no-C1-pin-successor-needed-on-A296-bound-path-two-re-signs-C1-tail-first-importer-rule-logged.md](/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0330_2026-10-22_ack-0858-0861-deputy-no-C1-pin-successor-needed-on-A296-bound-path-two-re-signs-C1-tail-first-importer-rule-logged.md) — SHA256 `077663a0194a8ab67cfa68f50fce8ab0be4837f58a19fc7f9da425133475d0a9`
- [INTEGRATION_CURRENT_PINS_CX2V003.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/INTEGRATION_CURRENT_PINS_CX2V003.json) — SHA256 `0e17b273f07871606e09756309e6e7e6ba15be206a95ab8c70bd2ac97853f6f8`
- [A296_CHAIN_CHECKLIST_C3V002.md](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/root_thu_checklist_c3/A296_CHAIN_CHECKLIST_C3V002.md) — SHA256 `81e24b585dcb6d32faff65e32c01ab4b8ae6522ca83b2d2fd3d11b14c2b9e2b9`
- [make_root_binding_c3v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/root_thu_checklist_c3/make_root_binding_c3v001.py) — SHA256 `e2cc8afe9c86a74e296522086482b680490ebce7b886fb23d2ecd4f87e5925ce`
- [LOOKUP_FINAL_PINS_CX2V003.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/LOOKUP_FINAL_PINS_CX2V003.json) — SHA256 `1b4c7c2c9798efc0c37b7607c9da21fd68c48fdc05f5bc63edeee13c1cfe66d8`
- [A296_BINDING_TEMPLATE_CX2V002.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/A296_BINDING_TEMPLATE_CX2V002.json) — SHA256 `b882a15f934140f228b32caecc208586984511e7295928384c45042ced9767ca`
- [ACCEPT_DEPS_RECORD_C2V001_TEMPLATE.json](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/ACCEPT_DEPS_RECORD_C2V001_TEMPLATE.json) — SHA256 `48ec0e010cd4228f6b3a7eab78940e956465af32d3d3e796efb41f4a7ca3bfa5`
- [direct_cert_lookup_cx3v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx3/direct_cert_lookup_cx3v001.py) — SHA256 `1cb5039ef380f7472191f40d1293f45b98cbc4e301efb06d9ea9ccc5b59de7e5`
- [direct_preflight_cert_cx3v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx3/direct_preflight_cert_cx3v001.py) — SHA256 `586391ecd15453608956347ecafd4f61f6dea77a33ec71a61435a7a714e39a8f`
- [acceptance_handoff_c2v004.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py) — SHA256 `5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8`
- [direct_cert_lookup_a296_cx2v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/direct_cert_lookup_a296_cx2v003.py) — SHA256 `bfcaa714555dcea236121071644f1de3ba34bd57e95dd631f36145d42094c2f1`
- [direct_preflight_cert_a296_cx2v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/direct_preflight_cert_a296_cx2v003.py) — SHA256 `3ae08ba9a4d442b5f21f64e421f5205d87c3b9ecb2531f03193c228385c999e0`
- [a296_binding_cx2v002.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/a296_binding_cx2v002.py) — SHA256 `141c1cd291ece1899ebaa0308882e6b44a91bd8896738e233a94a28cc31bfe43`
- [registry_verify_a296_cx2v003.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/registry_verify_a296_cx2v003.py) — SHA256 `60ed81b58ea205a3dc61f43b58bfee47dee688fd2ab448ea1762f94e8b48a5e0`
- [registry_assembler_a296_cx2v002.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/registry_assembler_a296_cx2v002.py) — SHA256 `0f9283b86f47a1382c9c00173d70d8a4fd34fa20664400ca55ed3bbf3c9cf548`
- [cp1_points_assembler_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/cp1_points_assembler_a296_cx2v001.py) — SHA256 `aa0fdc84539ac09bedbfe25932350410f3a3e17ad52caa348e818b85891478fb`
- [h3_accept_call_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/h3_accept_call_a296_cx2v001.py) — SHA256 `edcd3ffa647c143eeb2a942e46d2420d2126d9f61f33252be8c9126db1bba007`
- [step4_guard_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/admission/step4_guard_a296_cx2v001.py) — SHA256 `52cceaf71be65e6321041f7cbcff6c8eef0bc5ef0ac9503fe878fc459453ea93`
- [step4_bind_a296_cx2v001.py](/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/admission/step4_bind_a296_cx2v001.py) — SHA256 `3194c6f363fff3a5f2c62f69d290122dd49b656af22c81e0c3c915f714ffe96b`
