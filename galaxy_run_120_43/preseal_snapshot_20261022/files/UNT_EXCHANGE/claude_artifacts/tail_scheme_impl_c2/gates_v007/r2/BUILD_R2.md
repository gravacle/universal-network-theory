# c2v007r2 — immutable identity-comparator successor

date -u: Sun Oct 18 19:12:47 UTC 2026

Status: TESTED build; frozen for Codex2 delta review. Root retains production comparison/adoption/launch ownership. No real UVT, C5H or NGC target read. No science launch.

The comparator now rejects missing or malformed checkpoint identity/caller digests on either side before accepting equality. Full checkpoint bodies remain compared. Identity schema/digest failures report RA_IDENTITY and RECORD_DEFECT; valid controls pass.

| Finding | Closure | Evidence |
|---|---|---|
| B1/A91 | TESTED_CLOSED | 44 integrated MUST_FAIL omissions/type defects; independent114 full-main positive/negative cases, including all four original omission reproductions. |
| S2 | TESTED_CLOSED | 11 exact final-aggregation AST fault/control probes integrated as driver unit; all four original faults MUST_FAIL; full879 rows/9 driver units PASS. |
| A79.4_NPZ | TESTED_CLOSED_NO_COMPARATOR_CHANGE | 7 direct parser cases including both alias orders, nested alias, duplicate identical/different members. |
| PARTIAL_CHECKS | TESTED_RECONCILED | 58 available partial rows reconciled to frozen parent expectations; historic baseline NORM_INJECTIVE fails remain intentional. No additional open TESTED defect in those partial outputs. |

**Validation.** Full final selftest: 879/879 rows, 9/9 driver units, all child exits0, zero breaches. This includes44 new MUST_FAIL digest cases and11 accounting fault/control probes in one integrated unit. Independent full-main suite114/114; NPZ logical-name7/7; static bundle13/13. nice10, Python-I-B, single-thread BLAS.

**Preserved failed predecessor.** FULL_V001 had18 positive structural-fixture failures on RA_IDENTITY: those old fixtures omitted both producer digest fields. Successor fixtures compute the two digests before initial publication; expected PASS/FAIL outcomes are unchanged. Their pinned support dependency and port manifest were updated. The final full suite reruns every case. No comparator relaxation.

**Tools.** Successor record writer binds r2 comparator; exclusive script generator writes the R2 command file. The command file was inspected and byte pins verified, never run. Source inspection does not certify real receipts or writer output. Earlier candidate tools and harnesses are retained but excluded from SUPPORTED_FILES_R2.

**UNTESTED.** Production r4/r5 comparisons, production seal records, scientific identity, r6 adoption and launch execution. Root executes actual comparisons only after review. No attempt to read protected run trees. Synthetic FIFO/symlink fixtures remain preserved; no special files are opened or hashed.

**Full selftest command (fresh output directory required).**
```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 10 /Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/selftest/selftest_c2v007_r2v003.py --comparator /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/run_identity_compare_c2v007.py --ported /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/selftest/ported --fill /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/tools/fill_picard_member_c2v003.py --out <NEW_OUTPUT_DIRECTORY>
```

## Byte-pinned evidence
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/selftest/out/FULL_FINAL_V002/SELFTEST_C2V007.json — 33a60780924af2574171dbc4d447ce4f68f825ad59d42004126a412055122dbc
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/selftest/whole_20261018T185722_71779/RESULTS_WHOLE_IDENTITY.json — 709b4776365799eb79d439a4205df5bab27f1f6885d37919604fdec7dbd030af
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/prep/NPZ_LOGICAL_R2_V001/NPZ_LOGICAL_PREP_RESULTS_V001.json — 4eb38711070b6c0587555f177565cc342608f417bd83696f6178a57c100ce1da
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/STATIC_BUNDLE_CHECKS_V001.json — 1603c1ed780ce673c547b57c18e534dee03940c0b6ae454a2814a55375923ff3
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/CLOSURE_TABLE_R2.json — 98b1f72e86aac2d4a8ab9a998c5d905ff3b35a85b863a5fac90f961fa3ce2c2f
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/SUPPORTED_FILES_R2.json — 2e546a0a8da59a7462619ac25954cfbc65e21e49d76e9433f4059ed05b5a2e9a
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/DIFF_FINAL_R2.diff — d6d9eff233dd02ba0a2fab468bdc0f81771b7848506dbe3573606bde22319616
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/DIFF_STRUCTURAL_FIXTURES_R2_V001.diff — 44c2946d276ea7e9a7d5867f8e5982b18ebe67ed9f0cbf583d4a2ad538356320
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/selftest/out/FULL_V001/SELFTEST_C2V007.json — f6d766ce51df43329e70188fabd3aa399f4abb439eb21f821ac3a9424bb7ae6d
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/REVIEW_CX2V001.md — 02717971aefc71e632772ff607fcb828ce25c5ee21d31aa6f9d334cce17765f8
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/FINDINGS_CX2V001.json — 29410f817efe2f637abcbfe21401649d7f57e56b2b55830c492454ff4c716567
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/prep/PARTIAL_CHECK_LEDGER_CX1V001.json — 3139701dfe7cf6db835f293a00e81b2eceac6e68c839b92ebcd710c779534b5c
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/run_identity_compare_c2v007.py — 052da0fe378b7927f35be28f9eda6f03313aef32bae7d5c9a301d276de21b12e
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/selftest/selftest_c2v007_r2v003.py — ae3844f4bae96f14eca4470a10670dff7be76282bcbcc16c71bd79e39192ce65
