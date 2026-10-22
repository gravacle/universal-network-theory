# c2v007 parse/token/A71 component review

Date (`date -u`): Sun Oct 18 18:49:55 UTC 2026

**TESTED: no blocking comparator defect found in this component's source audit and bounded synthetic tests.** This is a component result, not a final program verdict or scientific identity result. Candidate parent source remained 06ff52d636c640ebe9a92a4b2cf54620a01514992019e2b2f2dca1529f7dc188 before and after execution. No candidate edits, production runs or production receipts were read. No scientific process launched. Published r2 was not reviewed.

The independently enumerated source inventory contains **613 candidates**: 289 dictionary displays (288 fixed-key, including empty initializers), 20 dictionary comprehensions, 120 subscript stores, 13 dict() calls, 21 setdefault(), 11 update(), 96 set(), 26 set comprehensions, 11 set literals, four frozenset(), and two JSON parse entry points. All 613 are assigned to 25 reviewed source families; zero duplicate constant-key displays and zero unclassified candidates. The superset includes list-cache writes and hash.update, unlike the supplied BUILD's 446-site definition. No supplied inventory/checker was imported or executed. All-site runtime coverage is **UNTESTED**; the inventory distinguishes static reasoning from family tests.

Independent results (counts remain separate):

- v002: **23/24 whole-gate expectations**, **36/36 unit expectations**. The one failed positive was our fixture: it supplied NEW static_pins with no REF dictionary. The strict comparator refused the entire newly introduced field. v003 corrects the context; the earlier file is preserved, not counted as a candidate defect.
- v003: **9/9 whole-gate expectations**, including the corrected selected-driver static-pin positive and arbitrary/wrong-hash pin negatives.
- Initial v001 calibration: B0P passed; Z2 correctly refused the old factory's deliberately fake identity digest. The v002 factory computes canonical checkpoint identity and payload digests, then both B0P and Z2 pass. Initial calibration is not counted in the above suite totals.

Owning-check evidence:

- B1 duplicate NPY AST keys (including equal values) reject directly; in an actual declared Z2 sidecar NPZ the whole gate fails **STRICT_PARSE only**. A valid NPZ in the same slot passes.
- A79 raw duplicate ZIP members, extensionless members and logical aliases in both archive orders fail **STRICT_PARSE only** in the same valid whole-gate context. Extensionless-only is independently rejected. Both-side undeclared arrays use **BYTES_EQUAL**; equal opaque undeclared JSON is not parsed, and whitespace-only byte drift fails BYTES_EQUAL.
- B2 joined labels and A73 arbitrary verdict/numeric/plausible-code mappings fail **TOKENS_POLICY**. S1 exact repetition of a genuinely derived valid triple fails **TOKENS_POLICY, COMPARISON_REFUSED and NO_LAST_WINS**. Missing or relabelled valid derived triples also fail TOKENS_POLICY. Valid source-derived token sets pass policy for both r4/r5 selections and all four gates (eight independent unit positives).
- A73 SF3 selected-driver pin with actual byte hash passes when the common dictionary exists. An arbitrary existing code file with matching bytes and a registered path with a false hash each fail **FILES_TOP**.
- B3 valid ledger tokens pass; an ordinary value change fails **ATTEMPT_LEDGER**. A final-newline filename can no longer disappear into the ledger: it fails **INVENTORY** (also BYTES_EQUAL); the changed canonical record still fails ATTEMPT_LEDGER.
- A74 signed-zero and int/float scientific-value changes fail **RESULT**. Raw normalizer markers fail **NORM_INJECTIVE**. Fresh probes cover evaluated AST key alias 1/True, token relation fan-in/fan-out, one pair/two labels, one label/two pairs, reserved-marker escaping and inverse roundtrip, SHA-name delimiter ambiguity, and Store cached identity/end-byte change checks.

Source review follows actual conversions rather than annotations: strict JSON entry points, checkpoint decoder, NPY AST and dtype identity, NPZ namespace, CLI/argv, stage and file inventories, normalized keys/SHA names, supplied and automatic token relations, selected-driver static pins, ledger grouping, full checkpoint identity, stage_records, report construction, and set projections/accumulators. Checkpoint `_decode` rejects repeated encoded dictionary keys before construction. Diagnostic/counter/cache updates and explicitly registered field replacements are identified separately from untrusted list collapse. No new acceptance bypass was found in those paths.

Execution limits: v002 14.31 seconds / 87,687,168 bytes peak RSS; v003 4.81 seconds / 84,836,352 bytes peak RSS. Prescribed isolated -I -B interpreter; NumPy/stdlib; single BLAS threads; default priority under 0514 waiver. Source fixture imports are inert. Audit guards plus stat/lstat/listdir/scandir/readlink wrappers are installed before candidate imports. The candidate containment default is replaced with an owned protected-directory surrogate before any call, so real protected parent listings are not accessed. Both execution results record zero forbidden-path attempts. Store end-hash change testing uses a restored in-memory hash function seam and does not edit a fixture file.

The independent prior fixture writer is reused with explicit provenance. Candidate supplied tests and real out/IDENTITY, records/R4, all runs/runs_ext and the full six-megabyte candidate HASHES closure remain unread. Production incidence, actual gate reruns and exhaustive normalizer proof remain **UNTESTED**. S2 launcher shell/receipt and other component findings belong to the parent/sibling review and are outside this component's conclusion.

## Byte-pinned references

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/run_identity_compare_c2v007.py` — SHA256 `06ff52d636c640ebe9a92a4b2cf54620a01514992019e2b2f2dca1529f7dc188`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/BUILD.md` — SHA256 `d5e318da17550cfff62dce7c0c64fdd4b9b3f715672cd432fac90479568792a5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/parse_tokens/probe_parse_tokens_cx2v001.py` — SHA256 `dd71aaa146a92ae1b730c40303b7ba98df5e4575fd7f133202a9228c0158fd5e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/parse_tokens/probe_parse_tokens_cx2v002.py` — SHA256 `ea67e54b9edf5f11b6f0f246ce35000ee1551be8b98dc283ae94e72c7003d707`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/parse_tokens/probe_parse_tokens_cx2v003.py` — SHA256 `39ebb618ec01eab089716fc8ef90a935ca48cc07b4b7d71d4f03b0d98819b6ff`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/parse_tokens/inventory_a71_cx2v001.py` — SHA256 `f3b0a1225c83b71eb4cf8a2a1d0e0ae2bbb78dd8e83757313a019e989a442851`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/parse_tokens/A71_AST_CANDIDATES_CX2V001.json` — SHA256 `2cc4d1f8e0819bdf0dec4a382bea2bcb0cb25978b3e6bef5afd22d425597c0ca`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/parse_tokens/A71_CONVERSION_REVIEW_CX2V001.json` — SHA256 `86039b69a468018db733fdc10b7d73b4a410274acf7df1cee98b5af1b15e31dc`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/parse_tokens/probes_v002/RESULTS_PARSE_TOKENS_CX2V002.json` — SHA256 `80fac14c39b6c7726464d2ba8dd4d143e52aeddcf745c19b4971b9ef164ddfaf`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/parse_tokens/probes_v003/RESULTS_FOLLOWUP_CX2V003.json` — SHA256 `7159f3baee039c49f5e760c0ddc644df4717879a7459ac8b1cdc3394a12adad1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/invocation_canaries_cx2v003.py` — SHA256 `711580269ba37be0fc6c4e7206c27ca5427d56b7a558e1247cff8e44172ce72e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py` — SHA256 `069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/OPEN_RULINGS_SNAPSHOT_CX2V001.md` — SHA256 `17cb4fd496845823227562682341eb605304d0ec14842d3e26369215e49d538b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/INPUT_PINS_START_CX2V001.json` — SHA256 `110346000d72e3e932371d5993bf1663abdf21ba61a322c864860e05e4f04c99`
