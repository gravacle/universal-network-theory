# Provisional seal-tools v003 delta review

`date -u`: Sun Oct 18 22:05:25 UTC 2026

**FAIL at the tested provisional snapshot: 1 BLOCKING finding. Final publication approval remains UNTESTED.**

34/35 targeted controls passed. All six original B8 malformed-seal counterexamples now refuse; bare-name and empty-reason D05 inputs refuse. Valid inert controls pass.

**PV-D05-1 — TESTED.** A cited A90 section changed from `synthetic rule 90` to `changed scientific rule`. With correct old/new section hashes, the snapshot accepts `disposition: no_change`, reason `no change, because this synthetic rule has no operative delta`, and `change.what_changed: no change`. Result: PASS with no failure codes. This does not name the change as 0633 requires. Snapshot checks enforce only nonempty reason/what_changed strings. Root clarification or author closure is needed.

Each of six dev sources was read once and preserved; only checked snapshot bytes were executed. The tested builder helper preserves exact disposition text/content/hash and refuses changed bytes. The final record attachment was inspected via AST; complete T3/builder assembly remains UNTESTED. No README was available. T2/T5 normalized ASTs are unchanged; observed executable deltas are confined to D05/B8 plumbing and version/schema changes.

No real seal, scientific comparison, protected run, launch or target read occurred. Actual process nice was 10; isolated Python, bytecode disabled, BLAS variables one. Zero audit denials.

Pins from bytes:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_controls_v002/RESULTS_CX1V001.json` — SHA256 `421e1dd7e3fb960be8338f8e11a3b1ec4532a7fded4025eaf1e8fdf2393508aa`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/PROVISIONAL_SOURCE_DELTA_CX1V001.json` — SHA256 `0a16c612971f03211bd06f8a1c4c63e1502cf14d67f11725eab139078eda5151`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_snapshot_v001/SNAPSHOT_CX1V001.json` — SHA256 `cdc6f9c6b2036c6e9cb9670fd6b0c0cb8f1c08aa80b569c107bddf21ded4d51a`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/review_provisional_v003_cx1v002.py` — SHA256 `58dfadcffb2a884712ec7f9ac8858ef8ae88681f850e388173f3e2ac33c40a30`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0633_2026-10-18_claude4_seal_tools_v003_D05.md` — SHA256 `3b3e0d4a8be56e6a3a49d6aca3cb9e0c40f752481a96344e8ca7d0c7a3edb83b`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0634_2026-10-18_claude4_v003_add_B8.md` — SHA256 `eda276080429e2bceba2925bf8485f8b8a73069b56aba5931e6f8cca99f489da`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_controls_v002/D05/changed_nominal_reason_nominal_change/SYNTH_DISPOSITIONS.json` — SHA256 `b1b6000f6e886d130396777c483eca583e182e6b1b84304c6f47cdf5499004ba`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/PROVISIONAL_REVIEW_CX1V001.json` — SHA256 `b6356c03aaaf3c33e10ff451c39fe3564be6eb3f74012f66b97b0d99c935198a`.
