# Codex2 c2v007 comparator review — finished

Date (`date -u`): Sun Oct 18 18:51:00 UTC 2026

**FAIL — one TESTED BLOCKING_PROPOSED integrity/schema family and one SHOULD_FIX self-test family.** The parent comparator source is frozen at06ff52d6; r2 is not included in this verdict.

B1: both r4/r5 accept checkpoint records with identity_sha256 omitted symmetrically, and with caller.sha256 omitted symmetrically: four PASS_BITWISE_EQUAL results. Both digests are unconditional producer fields and the resume path indexes identity_sha256. Require those fields and validate them before accepting the checkpoint. Attribution is deliberately precise: A76 B-ID names identity_sha256 among all compared fields but has no separate mandatory-presence sentence; the mandatory-schema conclusion derives from the pinned checkpoint producer/resume code. This is a proposed blocking closure for Claude2, not a claim that the older unequal-body bypass remains. Correct full identities pass and all tested re-digested body mutations and forged present digests fail RA_IDENTITY.

S2: exact self-test judge/aggregation code accepts four injected inconsistencies: MUST_PASS with nonempty failing list; an omitted expected case; duplicate observed case replacing an expected case; child exit1. Require exact expected membership/cardinality, coherent verdict/check state, and acceptable child status. The prior wrong-owner MUST_FAIL issue is closed. The current saved synthetic report has unique rows, all child exits0, and all saved MUST_FAIL rows satisfy their named owners. No claim that this saved run actually exploited a weakness; this is fault-resilience evidence.

TESTED coverage is kept separate to avoid disguising a corrected harness fixture: identity/path/self-test component170/178 expectations (four digest omissions and four harness weaknesses); parsing/token36/36 units,23/24 first whole-gate expectations and9/9 follow-ups. The first parse positive failed because our fixture omitted the REF static_pins dictionary; a successor corrects it and passes. All earlier candidate defects close in bounded current controls: duplicate NPY headers and NPZ raw/logical namespaces; joined labels/repeated derived triples; ledger newline names; undeclared byte equality and normalization injectivity; exact driver-derived token sets and selected-driver pin tables; CLI repetitions/abbreviations; side-local existing stage maps and ASCII; FIFO/nonregular/empty-directory inventory; nested logs; owned containment aliases; exact RO1 keys; N6 receipt/exit/verdict ordering. Correct r4/r5 full-identity positives and B0P/Z2 positives pass.

Independent A71 source inventory613 candidates, all assigned to25 reviewed families; no duplicate constant-key display or unclassified candidate. Its definition is a broader syntactic superset of the builder inventory, so counts are not contradictory. Per-site runtime coverage and exhaustive normalization proof remain UNTESTED.

Two component manifests independently rehashed: 2750/2750 regular-file entries verified. Newline fixture paths use JSONL in the parse manifest. FIFOs and symlinks are inventory metadata only. All source pins unchanged. Failed harness versions remain immutable and explained.

Limits: source/static review and bounded owned synthetic computations only. No supplied scientific suite, launch script, actual identity/record writer run, production receipt, protected C5H/UVT tree, or NGC3198 observed/target velocity was opened or executed. Supplied synthetic self-test summary was audited without rerunning its suite. Production scientific identity/adoption remains UNTESTED. Guard wrappers precede candidate imports; registered roots are owned surrogates. NumPy/stdlib isolated interpreter, single-thread BLAS and0514 nice waiver.

Byte SHA256 evidence:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/run_identity_compare_c2v007.py` — `06ff52d636c640ebe9a92a4b2cf54620a01514992019e2b2f2dca1529f7dc188`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/BUILD.md` — `d5e318da17550cfff62dce7c0c64fdd4b9b3f715672cd432fac90479568792a5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/DIFF_c2v006_c2v007.diff` — `3f19a27cf180e7254a1f9e785261a62f776fa8f34e254c1cbde0d694a2e53501`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py` — `069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/OPEN_RULINGS_SNAPSHOT_CX2V001.md` — `17cb4fd496845823227562682341eb605304d0ec14842d3e26369215e49d538b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/INPUT_PINS_START_CX2V001.json` — `110346000d72e3e932371d5993bf1663abdf21ba61a322c864860e05e4f04c99`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/parse_tokens/REVIEW_PARSE_TOKENS_CX2V001.md` — `4a4c15b5d1af34fc3fd9d21368edbbe4537a45407976f2ee06da1e7590a8309c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/parse_tokens/A71_CONVERSION_REVIEW_CX2V001.json` — `86039b69a468018db733fdc10b7d73b4a410274acf7df1cee98b5af1b15e31dc`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/parse_tokens/HASHES_PARSE_TOKENS_CX2V001.jsonl` — `7ecd2644f60a84eacf1bd810591d355c244894fdf04c4b6bd61bbfa64befb042`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/identity_paths_selftest/REVIEW_CX2V001.md` — `ea20a157cfbca3017f73abb52be016a95f340a6d6549fcc52f4658fad4cd42da`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/identity_paths_selftest/SUMMARY_CX2V001.json` — `269eb73271ce2dbc94d1ae3da481cd5dd634190d69bd52f666381b6e0436d613`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/identity_paths_selftest/HASHES_CX2V001.txt` — `17269dda6c37b5997cf5c3c57d52bc0450a1bd7f88434d4b038216b1c09c8eb6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/MANIFEST_VERIFICATION_CX2V001.json` — `f66b4cdcfa027cee30e8047a3798a57f8ebf094e0b87de926581e6a3ce2ca82a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/FINDINGS_CX2V001.json` — `29410f817efe2f637abcbfe21401649d7f57e56b2b55830c492454ff4c716567`
