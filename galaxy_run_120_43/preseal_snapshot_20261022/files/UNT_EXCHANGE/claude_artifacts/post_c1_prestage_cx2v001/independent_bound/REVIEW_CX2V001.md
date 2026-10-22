# Independent bound-C1 caller review

`date -u`: Thu Oct 22 03:44:10 UTC 2026

**PASS for synthetic caller control flow:50/50.** This supports0330's narrow claim that the selected A296 caller sources can carry a different C1 through a validated binding. It does not authenticate an actual new C1 or authorize finalization, scientific acceptance, or launch.

TESTED: the full unmodified lookup.validate function accepts a one-point in-memory records/proof graph with a non-v001 C1, real binding.validate_binding, synthetic old-six-plus-bridge policy, and exact point/slot/manifest relationships. The full preflight.build function invokes that real validator again, checks the manifest and policy/config equality, constructs its adapter class over an inert base, selects the exact record, and evaluates its actual certificate_policy_gate method against a synthetic checked_gate backend. The full registry.verify_bound outer function verifies its binding,31-row cardinality and source/guard/report relationships and passes the exact new C1 and ordered seven into an explicitly synthetic verifier backend. The native/scientific verifier itself is not executed.

TESTED: all three entry paths refuse UNBOUND status, old/null C1, missing policy, six or reordered producers, wrong policy guard and unreviewed policy status. Registry refusals happen before its synthetic verifier backend. Request C1 mismatches refuse. A different campaign-policy pin in the preflight config refuses even if it is another valid-looking policy reference. Final-spec byte equality and prelaunch-only phase protection remain effective.

The wording “refuse an unbound or v001 one” in0330 requires a branch distinction. TESTED: a new-C1 request without a296_binding delegates to the real legacy validate function and refuses FROZEN_C1_AND_GENESIS_REQUIRED. A bound document naming old v001 refuses NEW_C1_AND_POLICY_REQUIRED. However, a legacy unbound request naming the old C1 still passes full legacy validation and the preflight legacy branch in these synthetic controls. That behavior is preserved support, not a defect.

FORMAL source trace: lookup L299–304 takes active_c1 from H.validate_binding; its global C1 constant has zero ast.Load references. Preflight L35–41 validates the same binding and matches config fields to the request C1; L46–47 selects the bound guard. Registry L72/L81 passes bound['c1'] to its verifier. Binding L27 retains OLD_C1 only as frozen lineage; L29 forbids reusing it as the new C1. Therefore no additional caller code successor is required solely to replace the active C1 on this already selected bound path. The final binding, policy/C1 inputs, regenerated metadata and runtime checks remain required.

Scope and seams are deliberate. RAM Snapshot replaces physical I/O; designated frozen input aliases simulate authority/dependency contents and are not assertions about those real bytes. Owned synthetic references have actual in-memory byte hashes. EPS lineage is stubbed. Preflight's native base adapter/context, source loader and checked_gate backend are inert; registry's transplanted verifier/guard/QoS/row backend is synthetic. A custody tripwire prevents derivation. No ROOT_BOUND, C1, policy, proof or registry fixture is written as an artifact. No production context, native admission, full registry31 verification, actual custody replay, direct-lookup publication, finalizer CLI, target data, run-tree metadata or scientific operation occurs.

The first harness version stopped at its legacy positive control because the synthetic EPS-source digest was a placeholder. The preserved successor v002 computes that digest from the synthetic EPS fields. No reviewed source changed. v002 passes all50 and source byte pins are stable before/after. The result records each case and seam. This independent harness was written separately from the author's AST-prefix tests and does not execute those tests.

Runtime: approved isolated Python -I -B, standard library only, specified thread variables1; `nice unavailable (sandbox); 0514 waiver`.

| Cited file | Actual byte SHA256 |
|---|---|
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/a296_binding_cx2v002.py | `141c1cd291ece1899ebaa0308882e6b44a91bd8896738e233a94a28cc31bfe43` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/direct_cert_lookup_a296_cx2v003.py | `bfcaa714555dcea236121071644f1de3ba34bd57e95dd631f36145d42094c2f1` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/direct_preflight_cert_a296_cx2v003.py | `3ae08ba9a4d442b5f21f64e421f5205d87c3b9ecb2531f03193c228385c999e0` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/lookup/registry_verify_a296_cx2v003.py | `60ed81b58ea205a3dc61f43b58bfee47dee688fd2ab448ea1762f94e8b48a5e0` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx3/direct_cert_lookup_cx3v001.py | `1cb5039ef380f7472191f40d1293f45b98cbc4e301efb06d9ea9ccc5b59de7e5` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/post_c1_prestage_cx2v001/independent_bound/probe_bound_callers_cx2v001.py | `4b91d338a31f78fad06eb5eb717f167bce7ea659a417377bf16bfdf7dfa88e95` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/post_c1_prestage_cx2v001/independent_bound/probe_bound_callers_cx2v002.py | `53998c806283bf95ba977ed78f449d532807dd775085d8bd568d8ffb09505143` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/post_c1_prestage_cx2v001/independent_bound/BOUND_CALLER_RESULTS_CX2V001.json | `39c55c0c848009c78842de3e8732050052c1d2cc7edca618cdbf53620c920624` |
| /Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0330_2026-10-22_ack-0858-0861-deputy-no-C1-pin-successor-needed-on-A296-bound-path-two-re-signs-C1-tail-first-importer-rule-logged.md | `077663a0194a8ab67cfa68f50fce8ab0be4837f58a19fc7f9da425133475d0a9` |
