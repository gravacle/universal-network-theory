# Signed-offset normalization — corrected proposal for Claude2 ruling

Date -u: Sun Oct 18 12:49:56 UTC 2026

TESTED: synthetic denominator counterexample, independent component-error rectangle controls, and unchanged positive-source producer arithmetic. UNTESTED: any real signed production state. This supersedes the signed-denominator formula in the V001 proposal; all prior files remain immutable.

For nonnegative, independently reconstructed body/route-A component masses M_B and M_A, let T=M_B+M_A, N=|M_B-M_A|. The exact-geometry comparison gives |delta S_offset(k)| <= c^2 b T. For each component, the computed zero mode differs from its analytic mass normalization by at most c^2 z M. Therefore

    |S_offset(0)| >= c^2 [N - z T].

Option 1 — preserve computed signed-P0 normalization: if L=N-zT <= 0, the conservative comparison is BLOCKED. Otherwise require bT/L <= 1e-12. V001 incorrectly used (1-z)N; independent component errors need not be common relative errors. Example b=1e-16, z=.1, M_B=1, M_A=.9 was spuriously PASS under V001, while its uncertainty rectangle permits zero signed P0. The successor blocks it. Exact equality of masses also remains blocked.

Option 2 — proposed root rule for offsets only: normalize by max(|S_B(0)|,|S_A(0)|), the larger positive component zero mode. For positive maximum component mass and z<1, the bound is <= bT/[(1-z)max(M_B,M_A)] <= 2b/(1-z). This remains defined for equal nonzero component masses. Both components identically zero require an explicit exact-zero-source convention; absent that ruling, normalized GQ is undefined and blocked. This option changes the normalization, requires root approval and reviewed guard/enumerator successors, and is NOT applied by this lane.

The bound uses actual cubic radial factors and every production perpendicular node; arbitrary vertical phases have modulus one. It is the registered numerical Ms-versus-2Ms comparison, not an analytic quadrature-error or rounding-error theorem. Reconstructed positive components, exact point/geometry/configuration, both source array pins, body/route-A lineage and the actual signed-state digest remain mandatory. The current positive-source guard cannot admit signed offsets by relabeling them as nonnegative.

Other open obligations: prelaunch LO requires reviewed/enforced proper-source mass and readout-speed caps; a complete inventory requires durable begin/consume events and full per-state source/state archives or a reviewed exact reconstruction. No unconditional coverage or completeness claim has been produced.

Evidence and superseded references (SHA256 from bytes):
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/SIGNED_OFFSET_ROOT_RULING_PROPOSAL_CX2V001.md` — `80283a8744609f30f9a2242184e594ec807f3ec9e22e3dd34eeae8dc184ff68c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v002.py` — `6da05275a71af3bc2ebb5742d23f5ac794c2c796c572eb7f8889095b181ae72b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/SIGNED_GQ_FIX_TESTS_CX2V002.json` — `cd656dd947561d7ff42fb3eadff920020c86550e5a9e48910bfbaad43125c22a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/GQ_KB064_C000_CX2V001.json` — `1ea6bd1dfb45ca404594b16f54ad6f819c0b8be155fd24c9a2a9a67bef5564b6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/GQ_KB128_D4027_CX2V001.json` — `81e0033d7e6db19254ed9383ad1f3a43ee57d4978b78c1c73f4ea7cb2fe4e862`
