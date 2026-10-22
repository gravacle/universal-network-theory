# Independent v006r9 numerics-binding review

`date -u`: Sun Oct 18 15:23:50 UTC 2026

**PASS — 41/41 independent controls.** This verdict covers the 0557 delta on the exact source pins below. All evidence records were explicitly synthetic; the actual pinned r5 normalizer, actual receipt verifier and actual Context/fresh_gates implementation were exercised. Production calls and scientific acceptance remain UNTESTED. No scientific launches, actual UVT run/receipt reads, forbidden targets or network access occurred. The audit hook reported no blocked launch/mutation attempts. Execution note: `nice unavailable (sandbox); 0514 waiver`.

The new comparison deep-copies each raw numerics block and removes exactly `uv_tail.eps_certificate` and `uv_tail.lo_certificate`. It compares canonical bytes against the current config block for **both** named deciding roles. All other fields, key presence and JSON number types remain bound. Code inspection found no extra exclusion. The original objects are preserved.

The actual-normalizer positive pair passes. For each role independently, fewer Picard passes, fewer route-A iterations, lower tail quadrature order, omitted column_workers, added valid default seed_source_rtol_factor, changed Picard speed bound, and integer/float representation changes refuse with the specific numerics/config mismatch. Every mutated case rebuilds the spec, normalized result, receipt and finish; the reanchor result/receipt/spec pins are also rebound. These are discriminating numerics checks rather than stale-pin failures.

Six certificate-only controls (EPS, LO and both slots, in each role) pass. Their sentinel substitutions verify only the intended identity exclusion; they are not scientific certificate proofs. A second consistent synthetic config and pair pass, while both cross-config pairings refuse. An unbound direct call fails closed.

Actual Context construction and inherited fresh_gates pass for independent A/B contexts and A→B→A refresh order. Changing the current context's configured block makes stale deciding evidence refuse; restoring the block restores the pass. Both anchor and numerics ContextVars preserve outer sentinels and reset after injected constructor or refresh failures. Subsequent refresh still works. No source monkeypatch was used for the positive or normal negative cases; only deliberate post-deciding exceptions were injected to test cleanup.

The wrapper delta changes only the core reference, sibling sensitivity-policy reference and version error text. The pinned r8 sensitivity policy remains unchanged: root review-byte allowlist empty, A68 false, direct compute_pair refused before any run read. Root-invalid tail-ON resolution still refuses. Candidate wrapper/core/config hashes were rechecked unchanged after execution. No residual finding remains within the reviewed delta.

Local fixture configs declare their own local work directory and no external volume UUID, as a test setup. The production External1 identity guard and production configuration remain unchanged. This independent review does not replace the parent's final static/dry report or authorize scientific launches.

Files and SHA256 from bytes:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/calibration_core_cx2v006r9.py` — `a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py` — `24abe3bc4f6ee0e3c5d7c89502062cf99464573b35bc5b53c33c14ef2ae888af`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json` — `721c7230f3f3efde6f8406f13a52995ae321248829ab1ee64a2f522ad5582b8e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/independent_review/test_deciding_numerics_cx2v001.py` — `c315d99eea9b1de8bdb19f033197f402f1b7dbb1d89313aad88e7af6c38b02f5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/independent_review/controls_v001/RESULTS.json` — `b3d4438d6ad8d735083164c8d6185c2a557cb99aa3731e182efc6eb018b7603e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/calibration_core_cx2v006r8_v003.py` — `603ab460fb039494659f5b0e03998b28ff2a7f124d9ae7fd7491340523929e08`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py` — `8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0557_2026-10-18_codex2_v006r9_numerics_binding.md` — `160399540c1d5eabe156d3a3f5d9737376eb8106d6dd4018af09b5575efcc98a`
