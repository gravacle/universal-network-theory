# Independent source review: consumed-state join v010

`date -u`: Sun Oct 18 13:22:37 UTC 2026

**TESTED — source/pin review PASS for the four corrected observations below.** No unresolved blocker remains in those inspected mass-premise, manifest-lineage, occurrence-kind and final-snapshot paths. This is a local independent helper review, not a substitute for the coordinator's required distinct-lane scientific/policy approval.

**UNTESTED — complete production replay and real point admission.** No scientific replay or launch was performed for this review. The builder's protocol test result was read and checked against the reviewed bytes, not independently rerun. Those tests explicitly stub the scientific verifier seams. Inventory `complete=True` remains an enumeration/custody statement; GQ, LO, reviewed packet selection, row policy, current-state certificates and launch authorization remain separate gates.

All short filenames below are relative to this report's directory.

| Inspected file | SHA256 from bytes |
|---|---|
| `consumed_states_cx2v007.py` — initial reviewed candidate | `9a0cf59edd71b9060855cac0a4005c41d1e9cdcea18dd2fd6ee6f3ce617fc0ff` |
| `consumed_states_cx2v009.py` — first three corrections | `5d7f3ef8e69d544c6a579334755d214aaeaa4451c350419275df83e06e4d1172` |
| `consumed_states_cx2v010.py` — final reviewed candidate | `e48cca3c35a3d6d3724f74b9407b91f006bd31f2f30f416f9c328ba9e4144ca2` |
| `consumed_states_cx2v005.py` — pinned discovery dependency | `7b7400f331970a5f5fb7f7104f5e1850a765fcd04fc993100b5d1f0f37f4d653` |
| `current_source_evidence_cx2v004.py` — pinned replay/check dependency | `7289f2ba25cbd8becbf1bc9172223faf7626d29d055708fbfb60e4c5d0b42de9` |
| `execution_graph_cx2v002.py` — expected stage graph | `6d59f1d06e7c69e15e8d9766fa1776da2b0603d16febf4406c96157d77019258` |
| `test_consumed_join_cx2v003.py` — builder protocol suite | `c2b8e90714645648172e236b9f6b6596f08e87dc39ab76719271ccf31874c481` |
| `JOIN_PROTOCOL_TESTS_CX2V003.json` — builder result | `8142529ad735af7aacb1a49b18568ad7698d1baa89f5140a9f6b3753fb7c5a22` |

## Four observations and closure

1. **Positive gas zero mode.** Initial v007 removed `POSITIVE_TOTAL_ZERO_MODE_REQUIRED` while checking only `nonnegative_masses=True`. That allowed the structural join to clear a premise needed by the positive-source GQ guard without checking the actual positive denominator. Final v010 requires exactly the single positive gas component and `verify_product`'s computed `positive_gas_zero_mode is True` for every nonsigned state. Stars cannot rescue an all-zero gas source. Signed states remain signed and retain their independent finite-denominator certificate obligation. **Closed by source inspection; builder's zero-gas rejection test passes.**

2. **Accepted route-A and signed-component lineage.** Initial v007 never consumed the negative placeholder's declared parent state digest and did not bind the offset descriptor's selected manifest to this call's accepted manifest. Final `accepted_lineage` requires the accepted manifest inside the own-call directory, exact manifest bytes/path in inherited and offset finishes, equality with the boundary and last-current state, inherited reference/body state equality, and negative-component parent equality. Boundary and inherited replay descriptors must use `accepted_manifest` with that exact ref; the offset rebuild descriptor must use it too. Thus the accepted full source/P/F are actually reconstructed, rather than clearing the manifest reconstruction blocker merely because other states replay. **Closed by source inspection; builder tests reject boundary/parent mismatch and a same-digest alternate manifest.**

3. **Actual TailState kind versus occurrence role.** Initial v007 checked state/source digests but did not compare actual state kind with its occurrence. Final `canonical_stage_kind` requires route_a for current/next/return and inherited reference/body, offset for the signed difference, and the discovered own-source kind otherwise. The actual reconstructed state's kind must match. Each claimed occurrence still joins separately before state deduplication. **Closed by source inspection; builder wrong-kind test passes.**

4. **Final immutable snapshot.** v009 read graph control refs without retaining them for the final hash recheck. Final v010 adds graph controls (requiring own-call paths), coefficient input, row prereg, custody modules, join producer and pinned join dependencies. These are byte-verified, checked for conflicting pins, retained with all reconstruction inputs, and rehashed after all replay arithmetic. **Closed by source inspection; builder control/coefficient-retention test passes.**

## Remaining boundaries inspected

The fixed replay plan binds the exact saved call spec/result and an ordered entry for every real discovered ordinal. Omission, duplication, reordering, Boolean ordinals and placeholder-as-state entries refuse. Signed placeholders are paired by stage and evidence and resolve only after actual signed source components are verified; they are not fabricated TailStates. Current/next route-A selectors require the exact iteration and source-prefix length. Structural discovery blockers and expected-stage-graph failures are retained, rather than cleared along with reconstruction gaps. Source and packet archives must be under the own-call output directory. The mandatory point check binds production P128/M_s128, actual grid/configuration and physical/source custody.

The final builder protocol result reports **33/33 passed** in 0.03942529205232859 seconds, under `SYNTHETIC_PROTOCOL_WITH_EXPLICIT_VERIFIER_STUBS`. These tests establish the join's control-flow contracts, not real scientific source validity. The actual reconstruction/I1-T implementation is a separate tested layer, and a full unmocked production join remains UNTESTED. No existing file was modified during this review.
