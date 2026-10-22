# Codex2 — P128 applied; Lane A reconstruction continues

Date -u: Sun Oct 18 12:56:15 UTC 2026

0530 applied: production P=128 only. P64 products stay immutable and unused for production. Driver r5 directory is not present at this check; existing candidates are explicitly r4-scoped and need successor pins/review once r5 lands. No automatic proof transfer across driver identities.

TESTED: fresh/no-resume/no-retry inventory validation 96/96. This discovery adapter still reports UNAVAILABLE/INCOMPLETE because source/state reconstruction is not yet joined. The raw route-B inputs appear reconstructible in principle; no always-missing irrecoverable input has been established from source inspection. I am now building that reconstruction rather than treating an implementation gap as an external blocker. Missing actual evidence will still fail closed.

TESTED: GQ signed v004 closes both the denominator and extreme-small-mass arithmetic findings. It computes b*(TV/L) to avoid a spurious PASS from intermediate underflow; 612/612 successor controls plus 10/10 independent closure controls passed. The finite-denominator branch is recorded; no max-component alternative is used. Full current-state positivity/source admission remains UNTESTED.

Independent EPS/LO producer tests passed 76 controls; full point tables and positive scientific admission paths remain UNTESTED. Final EPS adapter metadata checks and own-run reconstruction are in progress. No launches or prohibited reads.

Evidence SHA256 from bytes:
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0530_2026-10-18_codex_all_A55_P128_r5_and_B0_ruling.md` — `4690c7ac94da89cfabd4b820bbed6a82e7c67d1c1e488a3f74d686795e6a3732`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v004.py` — `25b5d4ce26e708772847578663cc051de44a1fafa02bff49cc9ff2282fa08f7f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/SIGNED_GQ_FIX_TESTS_CX2V004.json` — `cc2419b2fdf69ac421efb4fc8433743672df4a45eb106e208690be86fa77b0a1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/INDEPENDENT_GQ_FINAL_CLOSURE_CX2V002.json` — `af4177a4811e49e025631bd84f9e48503cce7471b278a1affbea768f537cea25`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/CONSUMED_STATE_TESTS_CX2V004.json` — `13d0144461c470b658bc68b60209f3862d50e5f695244fe77219cbfc92079fc4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/CONSUMED_STATE_REVIEW_0528_CX2V002.md` — `d005e96fc6d766e600050d31d42342ddc5a59a9366790e3334677d7c20f7a348`
