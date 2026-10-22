# A296 EPS guard integration candidate

`date -u`: Wed Oct 21 17:46:57 UTC 2026

**PASS for the bounded implementation checks; root adoption and native execution remain pending.** The base and B1 successors add one explicit A296 EPS branch, retain `refinement_failures=2` and `certified=False`, and leave ordinary nf0/1 behavior and all downstream GQ/LO/state predicates unchanged. No reviewed file was edited. Provisional v001/v002 files remain historical; selected guards and branch are v003.

TESTED: **133/133** in 2.581 seconds on the selected source bytes. This includes 31 saved genesis bundles against both base and B1 old/new guards (62 exact return-value comparisons), rows 300/301 ordinary proof projections with identical old/new returns, actual saved row302 numeric reconstruction behind in-memory review/proof/GQ fixtures, malformed history/trace/review/source-byte refusals, required post-state inventory refusal, and exact wrapper loader/AST/generated-literal comparisons. The row300/301 and row302 synthetic wrappers exist only in process memory; no fake approved review or admission proof was written. Expected identity/custody in the differential tests came from saved certification metadata, not a new independent custody derivation.

FORMAL: the new branch reads the exact successor numeric record, reconstructs it byte-for-byte from pinned original EPS and registered dense audit, and matches every proof row and acceptance-trace field. It verifies the review's numeric, point, custody, adapter, acceptance, and numerical-convention bindings. The ordinary old six approved proof producers plus the exact new bridge remain the C1 proof-producer set. The bridge's pinned original producer, rule and dense-audit sources are implementation dependencies, not additional approved proof producers.

The guard preserves its existing trust model: it validates integrity and recorded claims for caller-approved producers. It does **not** prove producer authorship, scientific truth, or root approval of a review. Exact review-list approval remains mandatory in the adapter/import workflow. The tests' in-memory review is deliberately not evidence of such authorization.

The native wrapper successor changes exactly three loader statements: absolute core/sensitivity paths only because the file moved, and the new certificate `G` path/pin. All other bytes and the generated 5199-byte `resolve` literal are unchanged. The literal SHA256 is `79e8936d96103b1540987a980b289b6d25e5e25941b02db647f7a833818da0e1`. Its new owner wrapper must be registered by the Step4 fence. The shared core also compiles an exact pinned AST projection of pure rule functions; native fence compatibility is pending parent verification, not claimed by these tests.

The existing direct-preflight `build(..., guard=...)` argument is the Step4 guard, not certificate `G`: direct_preflight L41 takes `G=C.G`, and L181 invokes it. Therefore selecting only a new standalone guard is insufficient; the native wrapper, policy review guard hash, registry verifier, C1/lookup/config and source allowlist must all name the new closure. The exact caller locations and ownership are recorded in BUILD_CX2V001.json. Inspected LO-slot/LO-state/SRB producers do not separately load B1 or call verify_bundle. SRB accepts the unchanged approved TESTED/PASS slot-proof contract and consumes substituted per-shell `eps`; no SRB formula change was made.

UNTESTED: actual A296 review approval, complete new registry/final-spec chain, native wrapper/context import or preflight, post-state scientific acceptance, production source reconstruction, or forward execution. No scientific producer was run and no run-tree, NGC data, target velocity, postseal record, session log, or network was accessed. Tests were isolated stdlib computations with single-thread environment; `nice unavailable (sandbox); 0514 waiver`.

## Selected files (SHA256 from bytes)

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/certificate_guard_a296_cx2v003.py` — `fe192884d983236806538272b52769e78fd13a54106e2eed9585b1c6279c02c9`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/certificate_guard_b1_a296_cx2v003.py` — `3939bc47c48f46f9e313969d77cc7895d7dd6936648b2060df31a5aff3cc4c25`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/eps_a296_guard_branch_cx2v003.py` — `80a22d3eb97ac526ad3b930dee273a57ce3628cdbb8d38d319a0c721951899ff`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/calibration_orchestrator_a296_cx2v001.py` — `c9fc5d16087526121d958c87a636350883a10d9b8e0b00abc273300ef872ec65`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/test_a296_guards_cx2v002.py` — `da6b223d1fe2597553b8de2d50dc70bb130cd5b9efac4cdb8765800a20a39ea8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/GUARD_TESTS_CX2V002.json` — `1936c3fac0a6cfb385b2c82df4efbd335738669b51e6f4db896b8ba686472df6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/WRAPPER_CHANGE_MANIFEST_CX2V001.json` — `3468ef45e0c4805ce29af032e612c6d224d51b5c9e4f72f55791162455fe860b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/BUILD_CX2V001.json` — `c5e7a9701945aa85ee4247ae06fa63cfa46f60f2f9ad4c1796ca6562d3eb9e6a`

## Source pins

- base_guard: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/certificate_guard_cx2v003.py` — `5f1e49e689a859c003b137c45c07f887423443ef2c726182616b41bf290c9c2f`
- b1_guard: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py` — `9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677`
- wrapper: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py` — `7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d`
- core: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py` — `dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6`
- sensitivity: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py` — `8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f`
- adapter_core: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/point_response_admission_a296_cx2v002.py` — `1a44bc59a5fc6a72c381d3c0c0875b6aa154c21fc108730d67c9ec529a39d9d7`
- adapter_bridge: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/point_response_admission_a296_bridge_cx2v002.py` — `1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4`
- rule: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/rule/eps_negligible_rule_cx2v003.py` — `669f0640b4a9e2a005e91245c27223499dc96a35189c6b4852a11a1e99190e3b`
- dense_audit_source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/audit_path/dense_eps_audit_cx2v002.py` — `618ba8fa9db2e7d7747c007d00f0ec64fd30083a164b01ad8ff60195e1b0d341`
- authority: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/A296_AUTHORITY_CX2V001.json` — `d1656a16e386b5bb1d0c6dd566706cd3d06ed47ec83ae1d6bf69b9d10238ea92`
- authority_A297_A298: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/A297_A298_AUTHORITY_CX2V001.json` — `a672644bb0305356e46d93fa0fc76bbeab511a3b0952b11b0a1cdf49e7791694`
- dispatch_0856: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0856_2026-10-21_codex2_A296_integration_adapter_validator_successors_before_mount.md` — `44952183a2b41c4726a5f99ad88e0e4bc3daf66d0c17f32694a4728ba7667870`
- registry_assembler: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v005_c2/registry_assembler_c3v005.py` — `7df1c4813865b9e1245f5a91d827591a6d87963b6413ab53c50d2a542d211310`
- common: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v005_c2/s4rc1_common_c3v005.py` — `2308a47ce3c758b6befa0aa954fa7e2b6ad7f4cb41ed73d4b8cd1d257021e7c5`
- direct_preflight: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx3/direct_preflight_cert_cx3v001.py` — `586391ecd15453608956347ecafd4f61f6dea77a33ec71a61435a7a714e39a8f`
- base_direct_preflight: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_direct_preflight_cx1v001.py` — `eee61ac61ff93a11c97b9fdd3d6340661f17a92394653e524ac1cd8648d20fd1`
- step4_guard: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_guard_c2v014.py` — `6efdca016416a919b25a1e23d46a415b75fe2b5e60145ba098f864730975165d`
- lo_slot: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/lo_slot_proof_c3v003.py` — `cd10cd59df44d7b79f3c3aa7ba88998d94c7292c4c2656e09bbbe16ded01bca3`
- lo_state: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/lo_state_proof_adapter_c3v003.py` — `211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c`
- srb: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/srb_rot_adapter_c3v003.py` — `08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a`

All actually read genesis bundle/proof/source pins and row300/301/302 certification inputs are enumerated in the selected test result input_pins and in HASHES_CX2V001.txt. They were rehashed at test completion.
