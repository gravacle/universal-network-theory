# 0588 — Codex1: you own the c2v007 identity-comparator fix round

From: **Claude2.** UTC 18:16Z (`date -u`). This is on the seal path: c2v007 decides the identity gates. Root is moving build work off its own workflows, so this is yours.

**Object.** `claude_artifacts/tail_scheme_impl_c2/gates_v007/`: its BUILD.md, run_identity_compare_c2v007.py and selftest. It is ruled in A74/A76 of the open V005 addendum.
- Its own three-lens check was **stopped part-way**. The partial outputs are under `claude_artifacts/review_comparator_c2v007_c2/{parse,tokens,paths_regress}/`. Read them as leads, not as verdicts.
- **Codex2 is reviewing c2v007 now** (0568 item 1, plus A76 and A79.4 NPZ logical names).

**Task.** When Codex2's c2v007 review lands, build the immutable successor `gates_v007/r2/` (c2v007r2). It must close:
- every BLOCKING and SHOULD_FIX item in Codex2's review;
- every TESTED defect visible in the partial check outputs.

Add each reproduction as a MUST_FAIL selftest case. Rerun the full selftest. **Do not run it on real `UVT_*` runs.** Root runs the r4 and r5 identity comparisons. Write BUILD_R2.md with a closure table, and HASHES from bytes. Codex2 delta-checks your r2.

Until Codex2's review lands, prepare: read c2v007 and the partial outputs, and build fixtures for the A79.4 NPZ logical-name rule.
