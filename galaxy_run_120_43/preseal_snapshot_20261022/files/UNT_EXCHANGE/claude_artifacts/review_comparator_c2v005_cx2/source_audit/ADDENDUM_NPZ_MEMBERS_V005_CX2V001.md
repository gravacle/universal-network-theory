# c2v005 source-audit addendum: duplicate NPZ members

`date -u`: Sun Oct 18 15:21:23 UTC 2026

**S3 SHOULD_FIX — TESTED whole-gate unexpected PASS.** The existing overall FAIL and primary normalized-key-collision blocker are unchanged. Comparator source remained SHA `6f656c68e51f457704dafd19c1a9e6b632e237f4959017ee376c18ad173b076b` before and after this probe.

The synthetic reference archive contains one `state.npy` array `[1.,2.]`. The new archive contains two ZIP entries named `state.npy`: first `[900.,-123.]`, then `[1.,2.]`. Its raw member inventory is therefore different, with a hidden tampered member. The actual c2v005 `main --driver r5 --gate B0P_RERUN` returns PASS_BITWISE_EQUAL with every check passing. The separate ordinary positive baseline passes too. NumPy resolves duplicate names to the last member, and `npz_members` converts its name list to a dictionary, losing the extra member.

Reject duplicate raw ZIP member names and duplicate logical array names before loading or hashing NPZ content. This is a malformed-container/array-inventory check; existence in registered production archives is UNTESTED. No production archives were read. NPZ C/F storage order remains a separate equivalence-contract NOTE, not this finding.

Execution used isolated prescribed Python, stdlib plus NumPy, one thread and no launches. `nice unavailable (sandbox); 0514 waiver`. No actual run or receipt reads.

Files and SHA256 from bytes:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v005/run_identity_compare_c2v005.py` — `6f656c68e51f457704dafd19c1a9e6b632e237f4959017ee376c18ad173b076b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/test_duplicate_npz_members_cx2v001.py` — `3f94c347ec5714873c0e61326aba5df50f5f88dd1d07b7cc2bce567596c4c8db`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_duplicate_npz_v001/RESULTS.json` — `1ac023bb4a3e80c0741a99abf7216cdbc6347992f1baf0e28f2c689f302bf2eb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_duplicate_npz_v001/duplicate_npz_member/REPORT.json` — `d46f77b401790bc2937108de50bc0d5bc55a58f9966d923bb1c5d1f41d05786f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_duplicate_npz_v001/duplicate_npz_member/ref/stages/00_body/state.npz` — `5ece9b8d38e231f91f401abc95cb4d5f506758c407d08dba3ee744ea2177c11f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_duplicate_npz_v001/duplicate_npz_member/new/stages/00_body/state.npz` — `57a83fe0597f01a77948eccfd2dce6c8dbed31133bc31fad8dd9c20ef1d19aa1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/REVIEW_V005_CX2V001.md` — `f95d84c06934071f6b2c88f84cc409f1371e3cc5680ead85f3a419baa842c35c`
