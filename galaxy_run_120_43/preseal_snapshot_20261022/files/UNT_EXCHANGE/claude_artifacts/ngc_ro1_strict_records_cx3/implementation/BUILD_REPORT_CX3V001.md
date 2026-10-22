# cx3r006 NGC strict RO1 records implementation

Sun Oct 18 16:47:52 UTC 2026

**TESTED: 637/637 focused checks pass.** Candidate source is sealed for the parent lane's independent review, 78-spec dry-plan identity and new SPEC_REGISTRY. Those external integration results are not claimed by this implementation report.

Dispatch0570 GC-S1 required duplicate rejection before NGC RO1 admission; GC-N4/N6 required typed refusals for list/dict worker_pin and row-less rejected reads. The actual prior-review JSON results under both guard_correctness and no_regression_parity were read and pinned below; no Markdown review existed there when inspected.

The successor preserves every r005 byte and adds 9,737 bytes before the main guard. Outside `_NGC_V011_ACTIVE`, the three public functions delegate directly to their retained r005 references. The global json parser is unchanged. No worker, binding, preparation, solver, numerical arithmetic, stage map or physical source changes.

Inside either NGC headline or Stage0 context, a strict loader uses `object_pairs_hook` to retain every object member, then walks the entire tree before constructing dictionaries. Any duplicate, including equal values, escaped-key aliases, nested unused metadata and objects inside arrays, raises typed `Refusal`. Both decoded-key occurrences are named by paths qualified with zero-based object member indexes. Example: `first_path=$["worker_pin"]@member[0] second_path=$["worker_pin"]@member[1]`. Each ancestor object segment also retains its member index; array indices and JSON-escaped keys make nested and punctuation-containing paths unambiguous. No duplicated value is printed.

`route_a_outcome_record` rereads the raw result before classification, closing the existing execute-chain path that initially uses permissive json.loads. `ro1_outcome` consumes strict raw result and start records instead of relying on an already lossy caller dictionary. List/dict worker_pin raises `NGC_RO1_WORKER_PIN_TYPE` before membership. The NGC RO1 block still requires current V011 serial/parallel workers paired with current binding 9b5ce82a; the r5 parent's 52dc4065 binding remains disarmed. All prior convergence, refusal-message and event-shape conditions are retained.

The NGC-only reader body is copied from the parent with strict result loading, a prediction-object guard, and a row-list guard. A legitimate fired RO1 with rows=null retains its existing early return (`valid=false`, no rows), while missing/non-list rows after an unfired RO1 raise `NGC_ROUTE_A_ROWS_REQUIRED`. Outside NGC, legacy TypeError and permissive duplicate behavior remain unchanged.

Focused evidence comprises 366 inactive parity assertions over guard, classifier and reader, comparing complete return values or exception class/message; 168 duplicate rejection checks with both exact paths; 48 typed list/dict worker checks; eight reproduced r005 duplicate-admission holes; valid headline/Stage0 serial/parallel cases; row-less refusals; normal 43-row parity; r5 binding refusals; normal/exception context restoration; unchanged global parser; and exact parent-byte preservation. All records, velocities and manifest rows in this harness are synthetic. Peak RSS was 68,517,888 bytes; audit denials were zero.

UNTESTED here: scientific runtime and full independent integration. The 78-spec dry-plan comparison and SPEC_REGISTRY are separately owned by the plans helper, and independent semantic review by another helper. The parent lane decides overall readiness and publishes numbered packets. No launch authority is conveyed.

No scientific launch, real NGC target/observed velocity read, protected-run read, network operation, deletion or existing-file overwrite occurred. Isolated Python, standard library/NumPy and single-thread BLAS were used. Every cited hash is from bytes; fixture/read dependency pins are retained in the results and manifest.

| File | SHA256 |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0570_2026-10-18_codex3_cx3r006_strict_ro1_records.md` | `4a480bd45ecee2e11851bfd41cd5a2486937c8ea23f4fecc2741ae33f03b330b` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r006.py` | `c2930e18eb2ba6f691dcaffffd56658143490ab366552cf90b27506a2357be49` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/successor/galaxy_m0_forward_c2v011_cx3v005_cx3r005.py` | `f85746f0bdfd3c108771225eff7c8a55a81e5d6634ee0e5403cf68aa9fa3dd6b` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/implementation/BUILD_SOURCE_CX3V001.json` | `7ea91c236a1eaee5d019ca43da22e3a4c7add4d8226898d53203f49c776d2d13` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/implementation/FOCUSED_TEST_RESULTS_CX3V001.json` | `73e12f212e8d089c40f0a4c68454d60a5033fea4f666c727fd87ff25f75b0b87` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/implementation/test_strict_records_cx3v001.py` | `b11601570d5907bf4cebb649073351a5638dec920d33f095d13497564341337e` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/implementation/build_strict_records_cx3v001.py` | `2039de27e8047277fa956ef0189edc1d8199b9bdb91c1c9a7257c99b8c33ffd0` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/implementation/ADDED_NGC_SOURCE_CX3V001.txt` | `086a72b79a091f6b29420e6437ad929516e3389fea00de71ce5179b965f3099a` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_v011_cx3r005_c2/guard_correctness/runs/run_20261018T163546Z/RESULTS.json` | `64bccd06e7d30b52042e5e8c9db11182660a183c48d9ad667f2ad116ffd2cc5d` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_v011_cx3r005_c2/no_regression_parity/results/P2_RO1_PARITY_V001.json` | `fcb8940a0612471977ac5cb048b2902ab16853ddccbd822abdcd5cb9088957e6` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_v011_cx3r005_c2/no_regression_parity/results/P6_SECOND_CONSUMER_V001.json` | `b0b04e4384dc7fbcd322420c90e1e16a1fc1a53d62d57e11358b7e1da7fc1560` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_v011_cx3r005_c2/no_regression_parity/results/P7_TRACEBACK_CHECK_V001.json` | `71ceece449cdba588b63691cc8adc9a30fc1656bc0360f72b3960df2c729804f` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/implementation/seal_strict_records_cx3v001.py` | `0b07d05d0e971d3d95edfff28767db37ca6e62281d75fb9f03de7ec601f6173d` |
