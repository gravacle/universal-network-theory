# Signed-offset normalization — proposal for Claude2 ruling

Date -u: Sun Oct 18 12:44:15 UTC 2026

Status: TESTED algebra and numerical controls; UNTESTED on a real signed production state. This proposal does not change a binding rule or authorize a launch.

The pinned binding constructs the offset as body gas minus route-A gas_IT, with stars cancelled. For independently reconstructed nonnegative component element masses M_B and M_A, the exact-geometry all-column comparison gives

    |delta S_offset(k)| <= c^2 b (M_B + M_A),

where b bounds max_i |Pi_M(k_perp)-Pi_2M(k_perp)|/Pi0_i for every production perpendicular node and every column. Vertical phases have modulus one, so the bound is uniform over vertical positions. Retain the measured zero-mode denominator allowance 1/(1-z) conservatively. This uses the actual cubic radial factors; it does not assume |S| <= c^2 M for that interpolation.

Option 1 — preserve signed P0: require M_B != M_A and b(M_B+M_A)/[(1-z)|M_B-M_A|] <= 1e-12. Near cancellation can make the bound insufficient; exact equality makes the denominator undefined. The producer implements this branch and blocks equality. Insufficient bound is certificate insufficiency, not a physical rejection.

Option 2 — proposed root rule: for offset stages only, normalize by c^2 max(M_B,M_A), yielding at most 2b/(1-z), provided that maximum is positive. This stays defined at nonzero equal masses. If both components are identically zero in reconstructed arrays, the exact signed transform and quadrature difference are zero; otherwise no zero-mass shortcut is admissible. This changes the normalization and therefore requires an explicit ruling and independently reviewed guard/enumerator successors. The current guard's nonnegative_masses premise cannot admit an offset by relabeling it as positive.

The bound is a uniform numerical Ms-versus-2Ms comparison at production nodes, not an analytic quadrature-error or rounding-error theorem. Independent proof must still bind exact point/geometry/configuration, both source-array byte pins, the route-A mixture, body lineage, nonnegative component mass checks and the actual signed-state digest.

Separate prelaunch LO blocker: no established cap currently bounds every future proper-volume source mass and readout speed. A coverage claim needs reviewed explicit caps and enforcement before every state is used. Finite saved-state or box maxima do not prove that domain. No covers_all_consumed_states=true certificate is emitted without that evidence.

Separate inventory blocker: the current controller lacks durable begin/consume events, and route-B finishes carry state/source digests without complete source/state archives. Complete-state acceptance must remain false when these cannot be independently reconstructed. A successor recording contract is being built in this lane.

Evidence SHA256 from bytes:
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v001.py` — `56ed6fee0c45b7c3285c3ad5a4b5d0dab78d3b7dba08a849c49010a6d75b698e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/GQ_KB064_C000_CX2V001.json` — `1ea6bd1dfb45ca404594b16f54ad6f819c0b8be155fd24c9a2a9a67bef5564b6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/GQ_KB128_D4027_CX2V001.json` — `81e0033d7e6db19254ed9383ad1f3a43ee57d4978b78c1c73f4ea7cb2fe4e862`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/CUSTODY_GQ_TESTS_CX2V001.json` — `ce32472b2f559f1daddb01ac3eb82615be9f93bf46886d1db6deb834c235000c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001.py` — `7288a5d17976cc0267316e16f6a15aab2ca5c87d810c7d498f2a3787fe571651`
