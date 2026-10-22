# Seal pre-stage preliminary review — two tested blockers

date -u: Sun Oct 18 21:52:27 UTC 2026

**PRELIMINARY FAIL: 2 blocking findings on current helper007/script005 bytes.** The builder is still publishing successors; this is an actionable partial return, not a final selected-tuple review.

- **SA-CX1-B1 — TESTED_INERT_METADATA.** Lexical guard calls realpath before checking resolved symlink target; a safe-looking alias into forbidden-name directory performs target lstat before eventual refusal. Extracted exact helper function; inert alias and dummy protected-name directory wholly under own review output; intercepted lstat observed 4 target calls, zero content reads. Fix: No-follow componentwise traversal, veto lexical and each discovered link target before target metadata; preserve valid canonical artifact paths.
- **SA-CX1-B2 — TESTED_INERT_LOADER.** Byte-pin check then spec.loader.exec_module may execute cached .pyc whose payload differs from pinned source, even under -I -B. Exact extracted helper with synthetic fence and manually exclusive-written matching-header synthetic .pyc: source pin passes, runtime marker is UNPINNED_BYTECODE rather than PINNED_SOURCE. Fix: Read pinned fence bytes once; verify digest; compile/exec exactly that same buffer; avoid source/bytecode loader fallback.

Both controls used inert fixtures entirely inside the reviewer output folder. No actual C5H/UVT/NGC target file or metadata was accessed, and the real root script was never executed.

All 12 concrete slot pins match bytes; 8 slots remain explicitly pending root/ruling. The tool2/tool3 reversal against0626 is a separate order discrepancy pending resolution, not included in the two tested blockers. Production execution is **UNTESTED**.

Byte pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/ROOT_SEAL_STEPS_c3v005.sh` — `f43bab616de4ffd87c56ec8240d07e3a956a60133b382441aad3a0dfebb8b7a6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/tools/seal_steps_c3sa_c3v007.py` — `2f08fb88c17dbe340fe5f03da10ed510aff384cdb404d8e3d9544664d2d79172`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/tools/fence_c3sa_c3v003.py` — `9c62ad4902c895f0aeeba3a78976b5944146ee0de153989dbc79470528dd2863`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/SLOT_VALUES_DRAFT.json` — `c93691f5d1931beef8abb656ced3446c99d0adf286d4b5de0c709ecb570284ba`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/SLOT_PINS_CX1V001.json` — `bbb265f6962d0f03b11ae86de0009456a7e7b6cfad93ca5b5f6672a6173fe9a3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/METADATA_INERT_CX1V001.json` — `1840d32b25c7b97a3663e1963cb5d59b7b26bedb28f0bf8026f6c0bdab5b7fea`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/LOADER_INERT_CX1V001.json` — `ce32b9d582154e9b5fd8f546cb3fec70b3716e8624747de0891d480d88cf15ba`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/PRELIMINARY_FINDINGS_CX1V001.json` — `94c95c0fd3be3646ba5559ca7024622b56a4a411aee96ed1212fc1dc56a1d666`
