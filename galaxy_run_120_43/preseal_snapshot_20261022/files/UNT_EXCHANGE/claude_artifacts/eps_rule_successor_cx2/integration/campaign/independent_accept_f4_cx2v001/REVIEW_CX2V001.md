# Independent D017 / F4 acceptance-consumer delta review

`date -u`: **Wed Oct 21 23:23:58 UTC 2026**.

**PASS for this bounded source delta; zero blocking findings. TESTED: 45/45 independent static and synthetic AST controls passed.** Selected candidate: `h3_accept_call_a296_cx2v001.py`, SHA256 `edcd3ffa647c143eeb2a942e46d2420d2126d9f61f33252be8c9126db1bba007`. This is a build-review result, not production acceptance or root adoption.

The exact D017 scope is the ENTRY_LINE successor, its named refusal text, and module docstring/usage names. Compared with c2v004 `eb895263...`, precisely lines 1, 5, 6, 20, 73, 94 and 144 change. After normalizing only those permitted AST values, the entire module AST equals the predecessor. Every function except `load_chain` is independently AST-identical; that function differs only in the refusal prefix. No other logic or pin changes are hidden in the successor.

**TESTED entry-name boundary.** The exact candidate `load_chain` function AST ran with an explicitly synthetic module loader. That loader verified the cached bytes' SHA and obtained ENTRY_NAME from the actual pinned A296 template, r12 placeholder and old c2v004 entry sources, without importing any entry or wrapper. Both A296 sources passed the line check and reached the stubbed wrapper load followed by `check_patch`, in that order. Old, unnamed, null, near-name, wrong-case and boolean names refused before either wrapper operation. Wrong entry source SHA also refused before wrapper loading. An in-memory mutant restoring the old ENTRY_LINE was killed by the valid A296 case. These checks establish the entry-line/control-flow correction; they do not validate a real wrapper/context cascade.

**TESTED dependency predicates.** The exact statements at accept-call lines 268–277 were projected into an isolated in-memory function. The wrapper guard SHA came from actual source-byte hashing of the old `9e3fc109...` and new `3939bc47...` B1 guards. The synthetic configuration used the exact ordered six producer references from the frozen C1 metadata followed by the actual A296 bridge reference, as required for the proposed seven. All seven cited producer source hashes were independently read back from source bytes when this report was sealed; no producer was imported or executed.

Under that seven-producer configuration, new guard plus the exact ordered seven passes; old/foreign guard, six producers, reordered seven, duplicate producer, extra eighth, wrong bridge path/SHA and wrong enumerator refuse with `DEPS_DIFFER_FROM_CONFIG`. The guard/enumerator/producer comparisons themselves are unchanged.

**Contract boundary, not a new finding:** this predicate checks equality to the native configuration; it does not independently assert a count of seven. A control with the same six-producer list on both sides still satisfies the unchanged comparison. Root's correctly bound C1/policy/native gates must establish the seven-producer premise. No ROOT_FILLED dependency record or production C1/policy was manufactured by these tests. The successor preserves the old dependency schema and requires the root-filled record to carry the new wrapper guard and configured ordered producer list.

**FORMAL preservation.** The full `accept` function is unchanged, including cached-key refusal, maximum two acceptance passes, explicit first-pass record, INCOMPLETE-only rerun, frozen non-INCOMPLETE readings, rechecking pass list under lock, handoff result checks, reingest routing and exclusive step-record write. `first_pass_problems`, `passes_of`, `f6_action`, `finished`, `locate`, CLI handling and the handoff pin/constants are unchanged. This source comparison preserves those protections; no live rerun, latest-pass, locking or acceptance behavior was executed. The correction does not bypass the acceptance consumer by calling the handoff directly.

**UNTESTED / root-owned:** actual generated post-verdict entry/wrapper bytes, native context/gates, filled dependency record, root adoption and source-review pins, real call receipts/state, handoff, reingest and runtime acceptance. The root must select this consumer in the A296 chain and obtain the applicable reviewer disposition. This report does not expand the earlier 23-file review into a whole-chain execution claim.

Only source/metadata reads and exact AST snippets with synthetic objects were used. No accept(), context, handoff, adapt, producer, generator, launcher or supplied suite was run. No production run-tree or volume metadata, NGC data/targets, postseal records, session logs, network or subprocess was accessed. Python was the prescribed isolated 3.12.14 with single-thread environment settings; runtime note: `nice unavailable (sandbox); 0514 waiver`.

All cited source bytes matched the final rehash. Outputs are new immutable files.

## Byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0325_2026-10-21_R3-reviews-PASS-both-gates-NEW-blocking-F4-accept-call-refuses-A296-entry-D017-Codex2-one-line-successor-0320-erratum.md` — SHA256 `2485fd1cddb9270f37325d606200166aa05ffcb8881fb2f1123daef88d0193ca`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c1_h1_c2/C1_H1_C2V001.json` — SHA256 `4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v005.py` — SHA256 `2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/point_response_admission_adapter_cx2v003.py` — SHA256 `4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/h3_accept_call_a296_cx2v001.py` — SHA256 `edcd3ffa647c143eeb2a942e46d2420d2126d9f61f33252be8c9126db1bba007`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/h3_campaign_entry_a296_cx2v001.py` — SHA256 `05738509efb85f1a64d0031bf0e1c6b0d96f3427ab1a5670704affcd47f4ff28`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/independent_accept_f4_cx2v001/RESULTS_CX2V001.json` — SHA256 `d6f951b83b9b7e1b65c2f1fd1a88f66853a1e70953078f41e0ec57c79160fbe7`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/independent_accept_f4_cx2v001/probe_accept_f4_cx2v001.py` — SHA256 `31e9465a19cfe935c52f4e8121cd763cc1d2586ceeff3a92d326f103e81e1619`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/campaign/placeholder_chain_a296_cx2v001/v006r12_c4/h3_campaign_entry_cx2v006r12_c4.py` — SHA256 `af4e4f36ab74c8be01d3384bcaf83bdfdc3d867207b41bad447087eea4e21743`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/guard/certificate_guard_b1_a296_cx2v003.py` — SHA256 `3939bc47c48f46f9e313969d77cc7895d7dd6936648b2060df31a5aff3cc4c25`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/point_response_admission_a296_bridge_cx2v002.py` — SHA256 `1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/h3_accept_call_c2v004.py` — SHA256 `eb895263c8458696b265b30dc5dee771dcb89649e5b490c893bb613281c7bf19`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/h3_campaign_entry_c2v004.py` — SHA256 `cbdf0d49b8bfa09bccf8ba1ebfb518f8c00b663c2564db7c3a02c8b7a86e116d`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py` — SHA256 `9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/current_source_evidence_b1_c2v001.py` — SHA256 `7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/lo_slot_proof_c3v003.py` — SHA256 `cd10cd59df44d7b79f3c3aa7ba88998d94c7292c4c2656e09bbbe16ded01bca3`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/lo_state_proof_adapter_c3v003.py` — SHA256 `211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/srb_rot_adapter_c3v003.py` — SHA256 `08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a`.
