# Provisional A106 C02/freeze helper delta — Codex1

`date -u`: Sun Oct 18 23:22:02 UTC 2026

**TESTED: 29/34 expected-behavior checks passed. Five accepted counterexamples establish two related selection-validation findings.** Freeze and the tested slot-only derivation controls passed. This is an unselected helper012 draft audit, not a runnable-seal verdict; r6/v003 integration remains pending.

1. **C02-SEL-ASSOCIATION — correction required before C02 closure.** `_selected_names` lines 1176–1181 only requires the path and SHA to occur as substrings somewhere in the SELECTED bytes. Full `c_check_tor` accepted both an object with unrelated `requested_path` and `unrelated_sha` fields, and a `selected_source` whose path was the requested path plus `.other`. Neither stores the requested exact path/hash pair. Require an exact complete association under the actual published SELECTED schema. Ordinary matched pairs and contradictory same-path structured pins behaved as expected.

2. **C02-SEL-STRICT — correction required before C02 closure.** Lines 1159–1163 catch every strict-JSON error and continue with `obj=None`, disabling the contradictory-pair walk. Full `c_check_tor` accepted three pinned files containing a conflicting stored SHA plus the correct SHA in an unrelated memo: duplicate keys, trailing invalid JSON text, and NaN. Reject strict parse failures; substring fallback must not convert invalid JSON into selection authority. This also affects `c_selected_names`, which uses the same function.

Every counterexample was a new immutable file under this review's fixture directory, passed with its true byte hash and a valid independently pinned inert unsealed TOR. Thus these are actual helper runtime counterexamples, not only source suspicions. They do not establish a bypass of a currently runnable production package: its final r6/v003 pins are pending.

**TESTED passing scope:** supplied hash and length before freeze writes; exclusive destination preservation; copy rehash and post-copy open-source recheck (the last two use injected read observations without changing any file); exact selected TOR and exact slot-value-only sealed bytes; refusal of partial arguments, self-as-sealed, filled TOR, altered scientific/slot/slot-metadata fields, and different sealed serialization; actual pinned-byte checks. The existing pin/read/write/dumps dependency ASTs are unchanged from helper011. Freeze verifies caller-supplied final SHA/length; root-script pin wiring is owned by the parent review and was not tested here.

**UNTESTED/outside scope:** final published r6/v003 schema/wiring, original root script, real seal/comparator/scientific execution, watchdog, production output and protected/observed-target reads. The checked source buffer was compiled under a non-main identity. No author file changed; fixtures/reports were exclusively created. Actual priority was nice10 with isolated Python and single-thread environment settings.

## Byte SHA256 pins

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_a106_cx1v001/snapshot/seal_steps_c3sa_c3v012.py`
  SHA256 `b13483966fcb8755608d73e05c0e70dc94e39a2b07635f54efc0c86849748bac`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/selected_publication_v003/seal_steps_c3sa_c3v011.py`
  SHA256 `7caad125be19160c6e431dcf6be8f038cb9bba172c95f1f8059ebcdd938a0aff`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_a106_cx1v001/snapshot/0643_2026-10-18_claude4_claude3_codex1_A106_final_V005.md`
  SHA256 `2926f7ab57cac05168d079807224f05317d2b71e0f0a86e7a78b92e98005172e`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_a106_cx1v001/c02_freeze_cx1v001/review_c02_freeze_cx1v001.py`
  SHA256 `dc158c663571b2ee4f9855aed42818cfefeca358414ba625a4b9b8a8ef4d5a60`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_a106_cx1v001/c02_freeze_cx1v001/RESULTS_C02_FREEZE_CX1V001.json`
  SHA256 `da0dc7bcea69bff02049115f6449ded1613b03ad92ddd3aae6612bf457d2628b`

The results JSON contains every fixture path, its independently calculated byte SHA256, all 34 observations and injected-control labels.
