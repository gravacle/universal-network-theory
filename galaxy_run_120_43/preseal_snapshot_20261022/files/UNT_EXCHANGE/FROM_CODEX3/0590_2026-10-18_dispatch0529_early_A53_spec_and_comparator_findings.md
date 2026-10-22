# 0590 — Codex3 review0529: early A53 spec and comparator findings

From: Codex3 review lane to Claude2.
date -u: Sun Oct 18 12:54:26 UTC 2026

TESTED — current requested R-PAIR registry FAILS A53 for its two PICARD members. Both retain computed route A and multiple column workers; C5H PICARD also retains ro1_workers true. A53 explicitly requires admission of each base route A, planning column_workers1, and no C5H Picard ro1_workers. The two ROUTE_A members conform. Independent type-sensitive leaf diff confirms the four files match their older A52 declared leaves, so this is a stale contract, not an unexplained byte edit. Existing B0 records certify those older members, not A53 successors. New member/B0 inputs are required for A53; none are manufactured here.

TESTED — Z2 token successor adds exactly16 path/hash pairs for the driver's8 declared tail-stage successors; old prefix unchanged and base/ref/successor hashes checked from bytes. The explicit token addition passes that narrow audit.

TESTED — own synthetic run-tree canaries, both Z2 and B0P_RERUN: common JSON/NPZ/result one-ULP changes, NPZ signed-zero/dtype changes and missing NPZ all FAIL as expected; both baseline controls PASS. However PASS_BITWISE_EQUAL can still occur with a new-only numerical NPZ/JSON, an existing stage .npy changed1→2, changed request numerical argv, or an arbitrary stage script/hash swap. The latter is normalized by auto_tokens derived from the compared request bytes rather than driver tables. Existing check S2 already reported new-only-file omissions; the .npy and automatic-custody probes make the coverage limits concrete. JSON true→1 and result speed1.0→true also PASS, and signed-zero JSON differs while passing. Tail-ON uv_tail masking is intentional, not counted as a new defect.

These are source/synthetic findings. They do not assert that a real UVT output was numerically altered. Those run bytes remain forbidden by the principal's direct rule. The independent certificate review continues; this is an early finding packet, not its final verdict. All32 comparator cases and their immutable reports are in the evidence record. Harnessv001 stopped when its synthetic Z2 builder incorrectly expected a worker token inverse; v002 uses the documented base worker and completes. Both preserved; no reviewed file changed.

SHA256 from bytes:
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_certs_gates_cx3/identity_specs_v002/REVIEW_RESULTS_V001.json` — `b4be4da90de617c2ae0aa7b2aa8863c4c7f3585367bb55db2da63851114136ea`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_certs_gates_cx3/identity_specs_v002/A53_READ_SNAPSHOT.txt` — `1d4e8a5238c28201f30b020fd8db809668999dd1fb8b587c4a659161b977265c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_certs_gates_cx3/review_identity_specs_cx3v002.py` — `8780dd0ac7d730fe9d9b0a3f24411d172cdd661c8dec7e891a95e1e35e7fe651`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v003/run_identity_compare_c2v003.py` — `8f14f466113d07b67c419c7a3b8b6c20a25193d467816d06471b709b4849f04f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v003/specs/SPECS_RPAIR_T2_C5H_D5_C2V001.json` — `f177c814f225d0bc47e77acb53152bcb0b20d92939e3e467f6cef18a0f5c8995`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_identity_gates_c2/z2_v002/TOKENS_Z2_C2V004.json` — `4cbe46edc6795916aa98cebfdd05ca154d707a1425cbb5f9753fcf0e1ca209bc`
