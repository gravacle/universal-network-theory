# Independent r13 source and carried-record review

`date -u`: Sun Oct 18 21:21:38 UTC 2026

**TESTED PASS; 0 blocking findings in this scope.** Selected source SHA256 `f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157`.

The only changed top-level AST node is `check_record_codes` (439/440 nodes unchanged). Replacing its exact source span with the predecessor span restores every r12 byte. It parses check-record integers as strings, preserves duplicate-key refusal, permits text fallback only for `json.JSONDecodeError`, and returns typed `DRIVER_BUILD_CHECK_RECORD_UNREADABLE` for other `ValueError`. The common numeric JSON loader, scientific calculations, custody policy, and all other source bytes remain unchanged. Inspection of strict parser try sites found no other equivalent JSON-to-text admission fallback.

The guarded real-record rerun passes **70/70**, preserving the exact prior expectation roster and outcomes. The carried mutation rerun passes **96/96**; its result JSON is byte-identical to the r12 result. Harness successors change only source/import/path bindings and the mutation output basename; expected outcomes are unchanged. The fixture library is imported without running its author-suite main.

Both processes returned0 and spawned no child commands. Real-record peak RSS was1,142,980,608bytes and mutation peak RSS93,011,968bytes. These are observed measurements, both below8GiB. BLAS controls were asserted1 by the preserved guard. The real-record guard reports zero denied operations. The mutation guard denied exactly seven legacy `/.vol` metadata attempts before filesystem access, matching the inherited mutation design. Every protected registered-directory identity was replaced with an inert test directory before module execution. Historical `real_registered_dir` result names therefore describe stand-ins.

UNTESTED in this lane: the new focused A102 V01–V07 and T01–T19 checks, the full author suite, external Claude3/Codex2 approval, production admission, real seal/launch, and scientific outcomes. Those first two validation lanes are separate parent-owned evidence. No scientific launch, producer run, protected run/target read, or real seal operation occurred here.

Byte SHA256 custody:

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0629_2026-10-18_codex3_r13_A_B1_fix.md` — `ca8606b0d89c449c912bb36b745ba4f3a3a6c250221d865acb9c909907b88b21`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py` — `f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py` — `4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/SOURCE_DELTA_CX3V001.json` — `6637b4a9fb178e7b251b96d98ee72c96bafdc52d8fc06a00c800adccd9619be1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/BUILD_HARNESSES_CX3V001.json` — `7d24e2aa98aa5b7062f22a935ca85506102887325a9f370c66671e6abf040919`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/RESULTS_CX3V001.json` — `38b7f13cba6ecb6ac82dcc5c8241530b1d4d28dccb2b176e67cd77b3e7004e0c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/out/real_cx3v001.json` — `f2f2ad003c2b875f6d3be3c695d0406d3ee9b32d9c614ded5262033265765c72`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/out/mutation_cx3v001/MUTATION_R13.json` — `7bb7e5390e2fa2cdaf8cbac5e97d3ed9521750882ed638aa1bd8a831b6a24eb1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/out/real_cx3v003.json` — `3ceba6abb2e09a8e16feeeecf16435468b84d0c577a51f8c6769fa7f27db7e35`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/out/mutation_cx3v003/MUTATION_R12.json` — `7bb7e5390e2fa2cdaf8cbac5e97d3ed9521750882ed638aa1bd8a831b6a24eb1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/tests_kmax_tail_compare_c2v007_r12_cx3v003.py` — `51db35cdc6738bd13a6886263a2814270079d85685e88fe586dc7024d76fc156`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/tools/fixture_library_cx3v001.py` — `3690e7aeccb9f95cdc945953d6d9a150106b1e731832f02df615d757abfa32be`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/tools/real_record_check_c2v007_r12_cx3v002.py` — `f5f2c075e401b2a33d5d3f7b866cbc109d75a9de4b30a1076927d0386cc1d497`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/tools/real_record_check_r13_cx3v001.py` — `65b4711fa5519a8068bb71ad87066f4530d23ec7ebef8abddda6b63930ab3325`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/tools/mutation_check_c2v007_r12_cx3v003.py` — `170ad9b67fe9811e2922a8c70f37f4f4786b1916df637114f3e7a2f9c689677d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/tools/mutation_check_r13_cx3v001.py` — `af2c23525929192f7e3302667e6f6c6f515d298c8415f0a055a04561d55a30ca`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/tools/guard_r12_cx3v003.py` — `40afbe0810fd55ee05b3368adcd6651dd24834b5b7a54b254cb232a4c3271f80`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/tools/guard_r13_cx3v001.py` — `73d16ba57d694d7d365ff9f3d790a057db193ea96e390315983c88b4b6465f70`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/tools/run_checks_cx3v001.py` — `8da9a22751a9e70e728b071fa8f975218711afdaa583c68f04282eef43eb1142`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/out/real_cx3v001_guard/GUARD_90830_1792358454162920000.json` — `221c7e27ac93a55c7aa6dfa8cb3ab16299142e2ae998aa309e5cfa1819895dd1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/out/mutation_cx3v001_guard/GUARD_90831_1792358448759867000.json` — `6fc70f84a0ece20ecb8cb0a6a321716b6a6d48137211613ccce1563a41987ac1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/out/real_cx3v001.stdout.txt` — `d9f9dc485cd9c35cb3af9b8b83ce9cc9b1c96e2e67818932ac04c53781a51ea7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/out/real_cx3v001.stderr.txt` — `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/out/mutation_cx3v001.stdout.txt` — `0ac7e2b7fa331b85b7c4ee40c150f3af6cafed67d9650f4a9448e9e1f46ad6e0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/out/mutation_cx3v001.stderr.txt` — `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
