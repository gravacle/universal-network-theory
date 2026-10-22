# c2v007 identity, paths and selftest review — FAIL

date -u: Sun Oct 18 18:50:22 UTC 2026

TESTED on source and owned synthetic fixtures only. Candidate COMPARATOR SHA256 `06ff52d636c640ebe9a92a4b2cf54620a01514992019e2b2f2dca1529f7dc188` is unchanged from the parent start snapshot. Execution: `nice unavailable (sandbox); 0514 waiver`; prescribed isolated Python, NumPy/stdlib and single-thread settings. No scientific launch, production run/receipt/identity-report access, target velocity access, network, deletion or overwrite. Guards were installed before candidate import, covering open/stat/lstat/readlink/listdir/scandir. Every containment call used owned registered-root defaults.

## B1 — proposed BLOCKING integrity/schema closure

Both r4 and r5 accept an IDENTITY record pair with `identity_sha256` absent from both sides, or `caller.sha256` absent from both sides, after recomputing valid payload wrappers. Each returns `PASS_BITWISE_EQUAL`, no failing checks. The two complete-field positive controls pass. Re-digested changes to format, code (including solver/checkpoint/modules), controls, environment, fixed_source, inputs_sha256, shapes and unknown fields all fail RA_IDENTITY. Forged identity/caller digests, on one or both sides, also fail RA_IDENTITY. Thus the old unequal-body gap is closed; this finding concerns missing integrity fields.

Attribution is precise: RULINGS_SNAPSHOT L1148, A76 B-ID, names identity_sha256 in the complete comparison and calls B-ID BLOCKING. It does **not** separately state a mandatory-presence sentence. The presence obligation comes from CHECKPOINT's producer schema: caller.sha256 is always emitted at L312 and identity_sha256 at L489–490; resume indexes the latter at L498–500. COMPARATOR L2409–2410 makes both optional. BUILD L63 explicitly says “present.” Require the exact producer record/caller fields and then verify their digests, or obtain an explicit root ruling permitting a different schema. Do not interpret this as evidence that unequal science was hidden.

WHOLE_RESULT contains all four negative reports and both positive reports with full byte pins. The four omission fixtures alone explain its 70/74 expectation count.

## S2 — SHOULD_FIX selftest aggregation

The supplied `judge()` now requires every named owner for MUST_FAIL, and rejects a wrong-owner-only failure or unrelated COMPARATOR_EXCEPTION. Those controls pass. However, exact judging/aggregation AST fault probes accept (1) PASS with a nonempty failing list, (2) an omitted expected case in a nonempty suite, (3) a duplicate case replacing another expected case, and (4) a child suite exit1. Relevant SELFTEST sites: L110–111, L282–306; main also lacks nonzero return propagation at its final invocation. Check expected case identity/cardinality, report/check/failing agreement and child success explicitly.

This is a harness resilience finding. The current SAVED_SYNTHETIC_SELFTEST has 835 unique judged rows, all child exit0, and all stored MUST_FAIL rows satisfy the named owner sets. We did not rerun its suites or follow any production path. Its summary omits refusal exception text, so that text cannot be rejudged from the summary alone. The preserved V001 unit harness initially counted that packaging limitation as a failure; V002 corrects only this assertion and preserves both artifacts.

## Checks closed within this slice

- Whole-main r4/r5 comparisons reject nonexistent stage paths/keys on RESULT; Unicode stage indices on STAGE_SET; empty inputs/output/attempt directories and a FIFO on INVENTORY. The FIFO was never opened.
- Direct Tree controls identify inert character/block/socket modes as special without reading. Side.s normalizes only actual side-local directories; an opposite-side directory or regular file does not authorize it. ASCII stage controls pass.
- Changed stdout/stderr bytes fail BYTES_EQUAL at top-level stage logs and nested/input paths. c2v007 intentionally has no log exemption; this is stricter than A76's allowed stage-top exclusion.
- Strict comparator CLI refuses repeats, equals syntax and abbreviations. Armed/unarmed RO1 positives pass; every missing registered key and tested extra key refuses.
- Comparator and fill containment refuse owned exact, NFD, firmlink, symlink, symlink-dotdot and marker aliases. Missing registered identity refuses. Safe owned paths pass. No actual protected root was probed.
- Actual N6 checker rejects bad receipt status, driver status, exit/retry type/value, stop reason and driver/schema pins, and bad report verdict/failing/driver/gate/comparator/exit. A later good item cannot hide an earlier failure. COMMAND_SCRIPT checks all three new-run receipts, waits all three comparator processes, checks each verdict, then invokes WRITER. SCRIPT_GENERATOR and WRITER were source-inspected, not executed. This does not certify real receipts or seal records.

## Scope and evidence

100/104 unit/fault assertions plus 70/74 whole-main assertions = **170/178**; the eight unmet expectations are exactly the four schema omissions and four selftest weaknesses above. Source pins were rehashed after testing. Zero protected-access attempts, zero FIFO open attempts, zero scientific launches. Existing artifact files were never changed. Owned FIFO and symlink fixtures are preserved and listed by metadata, never byte-hashed.

The old independent OWN_OLD_FACTORY is reused for fixture construction. Full identity keys/digests and current mutations were added independently here. The sibling parse/token lens corroborated the corrected digest construction; no builder test suite was imported. Complete production identity and scientific acceptance remain UNTESTED. The actual R5 command script was never executed.

## Cited bytes

- **COMPARATOR**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/run_identity_compare_c2v007.py` — SHA256 `06ff52d636c640ebe9a92a4b2cf54620a01514992019e2b2f2dca1529f7dc188`.
- **BUILD**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/BUILD.md` — SHA256 `d5e318da17550cfff62dce7c0c64fdd4b9b3f715672cd432fac90479568792a5`.
- **DIFF**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/DIFF_c2v006_c2v007.diff` — SHA256 `3f19a27cf180e7254a1f9e785261a62f776fa8f34e254c1cbde0d694a2e53501`.
- **FILL**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/tools/fill_picard_member_c2v003.py` — SHA256 `54992e3353ff472f70ee4830bfcb816d9768dc15172a5c72b124bf310a273e20`.
- **N6_CHECKER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/tools/r5_gate_check_c2v007.py` — SHA256 `5dcd51422409f3354b480e67bd59c28f1b3412b756ea3228d834d133a673d745`.
- **WRITER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/tools/write_identity_records_c2v007.py` — SHA256 `f3ae76b0816b1b9d3fe401c4034bac9c92715e1f2e6c1ff678b89c9c9bd7d871`.
- **SCRIPT_GENERATOR**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/tools/write_r5_script_c2v007.py` — SHA256 `90d9532cdb5afa4fd1e8aea7c87f80ab61a5132b35380c271546dcb216348840`.
- **COMMAND_SCRIPT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/R5_IDENTITY_COMPARE_COMMANDS_C2V007.sh` — SHA256 `92d28db561683256417c2cca4b10cf3e87bf3620850c595b96b1399d2e3b5267`.
- **SELFTEST**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/selftest/selftest_c2v007.py` — SHA256 `4d8a503828b2be6a5a0161b3fdc5bd3b772d9129d2e46e19ec3fd22e984c4357`.
- **EXPECT_BUILDER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/selftest/make_expect_c2v007.py` — SHA256 `1c917096174e2d757f0b807b72963664a7dab006bdf6b15402cfb8a441c771a5`.
- **CANARIES_SOURCE**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/selftest/canaries_c2v007.py` — SHA256 `ff853f81f07fe11313840704278da76507134b8dcbc109397c154d1edb46819b`.
- **SAVED_SYNTHETIC_SELFTEST**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/selftest/out/SELFTEST_C2V007_V002/SELFTEST_C2V007.json` — SHA256 `ca057755003c006cb618fac4a2e9071b5723a316c362a0b02f0f9568c30a0101`.
- **CHECKPOINT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py` — SHA256 `069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114`.
- **OWN_OLD_FACTORY**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/invocation_canaries_cx2v003.py` — SHA256 `711580269ba37be0fc6c4e7206c27ca5427d56b7a558e1247cff8e44172ce72e`.
- **INPUT_PINS**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/INPUT_PINS_START_CX2V001.json` — SHA256 `110346000d72e3e932371d5993bf1663abdf21ba61a322c864860e05e4f04c99`.
- **RULINGS_SNAPSHOT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/OPEN_RULINGS_SNAPSHOT_CX2V001.md` — SHA256 `17cb4fd496845823227562682341eb605304d0ec14842d3e26369215e49d538b`.
- **A76_PREP**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/prep/A76_REQUIREMENTS_TEST_CROSSWALK_CX2V001.md` — SHA256 `421064c4c8c4d39e91dfc7abbd5918f48b1b9dfccab92e8c35483d2059fb59a7`.
- **PRIOR_PREP**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/prep/REQUIREMENTS_TEST_CROSSWALK_CX2V001.md` — SHA256 `648337b976e22a93f5d76fd3a6aaf65ab7cece954a13fafa72d4e32caba27e20`.
- **UNITS_SCRIPT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/identity_paths_selftest/probe_units_cx2v002.py` — SHA256 `4dd6c298ebc2e08e72cd8edca973f3dd82559a093d2100c9d3c3b9e4fca90645`.
- **UNITS_RESULT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/identity_paths_selftest/units_20261018T184712_45718/RESULTS.json` — SHA256 `3cb563f26e9d0f5ed08f13373a24e37783b05e3f8fe6ba8d8ec6f0237dafd930`.
- **WHOLE_SCRIPT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/identity_paths_selftest/probe_whole_identity_cx2v001.py` — SHA256 `85ef3d38207558be373b3e4f6d9299bf5c07a47294fa897ea4792690ebd93f0b`.
- **WHOLE_RESULT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/identity_paths_selftest/whole_20261018T184812_47351/RESULTS_WHOLE_IDENTITY.json` — SHA256 `b281c199f058cb3f40926c4ffc2d4af51c9151cebdfae4a67bc8ecc7e974844f`.
- **PRESERVED_V001_SCRIPT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/identity_paths_selftest/probe_units_cx2v001.py` — SHA256 `cf9abba1e568d0cf153d170e8d6d29a03120e2d8cbdb5156efdfad797ede7601`.
- **PRESERVED_V001_RESULT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/identity_paths_selftest/units_20261018T184702_45353/RESULTS.json` — SHA256 `6b19c672ab2fd1bd2d7b8fe5f72afb5bce3a9ad42cbb7bed76bdcace91e41c09`.
- **PACKAGER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_cx2/identity_paths_selftest/seal_review_cx2v001.py` — SHA256 `6e151a587c20594d6ca2d2eb5014384e25910518ea4475ba457e71b970fc4bd4`.
