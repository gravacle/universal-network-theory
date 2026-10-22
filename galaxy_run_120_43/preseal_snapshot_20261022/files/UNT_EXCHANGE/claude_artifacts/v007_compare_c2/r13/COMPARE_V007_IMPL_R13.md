# Compare r13 — A102 narrow check-record parser fix

Sun Oct 18 21:22:22 UTC 2026

Selected source fixes the r12 A-B1 admission bypass: a huge integer used to raise plain ValueError before the duplicate hook and fall back to a passing text check. The check-record parser now uses parse_int=str locally. DuplicateKey retains its typed refusal and both member positions. Only JSONDecodeError falls back to text; all other ValueError returns DRIVER_BUILD_CHECK_RECORD_UNREADABLE.

TESTED: only1of440top-level AST nodes changes, check_record_codes. Exact inverse function substitution restores the selected r12 bytes. All scientific loaders, fields, gate calculations, admission logic outside that function, certificates and bindings are unchanged. This is the only JSON-to-text fallback site; driver_build_codes, activate_driver_build, active_build and CLI modes delegate to it.

TESTED: author706/706, real-record70/70, mutation96/96; independent focused429/429runtime/custody and5/5static. V01–V07 refuse across49candidate paths; pairedr12 admits all49. All19text controls preserve133declared path outcomes (12ADMIT and7intentionalREFUSE fixture definitions). Non-JSON ValueError and invalid UTF8 refuse with typed codes; lexical JSONDecodeError retains valid text fallback. The suites overlap and are not summed as independent scientific evidence.

The author harness changes only six doc/path substitutions; its706ID/order/coverage/expected/pass mapping matchesr12. Real70andmutation96expectationrosters are unchanged. All24author guard logs and the real-record guard report zero denials; the mutation guard retains seven inherited /.vol metadata probes, denied before filesystem access. Maximum observed reported suite RSS1,142,980,608bytes.

FIELDS_R13 adds only this parser delta, then carries selected r12FIELDS bytes verbatim. Runtime gates and scientific integer types are preserved.

UNTESTED: production execution, independent external Claude3/Codex2 delta acceptance, root adoption and scientific admission. Guarded synthetic comparatorCLI checks are test execution, not scientific forward/route launches. No protected runs/target velocities/network/session logs were read; no existing files were overwritten.

SHA256 from bytes:

```text
ca8606b0d89c449c912bb36b745ba4f3a3a6c250221d865acb9c909907b88b21  /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0629_2026-10-18_codex3_r13_A_B1_fix.md
f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py
7b116b0103fdeb83d2cd358976e2c901be15313ad7f9ab8d159af6d9ee3bb365  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/FIELDS_R13_CX3V001.md
4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py
65dd997fe8ceb16b3b5332b74a37de8a484024b671bd363f4097e2023023eac2  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_c3/r12_review/REVIEW_V007_COMPARE_R12_C3V001.md
2fafec6acbb97a93bcdf555226918f4a8c204189b587158ae5d7ef579d0a68b3  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/AUTHOR_REPORT_CX3V001.md
4f88cae8b967d23e6b0ac25b50016a4f0d48627c3ec79660deedc14b36a8b936  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/AUTHOR_VALIDATION_CX3V001.json
eb0413c2157be629e98eb1443f56527341c9dbd1cb1f7cedcd2697be12672a76  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/AUTHOR_706_MAPPING_CX3V001.json
6cd8f72cce5cf326df1c5b594d12b9df5913281a00966901abfda217bf6ac2d3  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/AUTHOR_HASHES_CX3V001.json
76b8d3e595442506b1233d3f2365221423e1bda40478c2b2459e71e6c7373664  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/ab1_independent/REVIEW_AB1_CX3V001.md
e7cef4f40666f2f4aa5e0e0ef6cf7b22b8473c8a959942966ce7ee8ea91a7f32  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/ab1_independent/run_v001/RESULTS_CX3V001.json
32d8cc9f672e43c160fcc6426e1dc6d14ee77b62ce89a1baa92c931b46735871  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/ab1_independent/HASHES_AB1_CX3V001.json
1a111ed8b881ff9accc678403ee40dfb9d57abb9cc756c10e2a91521d436ead6  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/REVIEW_CX3V001.md
38b7f13cba6ecb6ac82dcc5c8241530b1d4d28dccb2b176e67cd77b3e7004e0c  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/RESULTS_CX3V001.json
0c15bf59b829abdb3e5f8f29e591e418f088f142de09467c970923f5d2560b05  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/record_mutation_independent/HASHES_CX3V001.json
f87a921dd55a73df56194ed88de79d300ba0cbf9ba90362b183d477f7d41be82  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/parent/SOURCE_DELTA_CX3V001.json
550c68e9c473f7fba6f34d394227dda6fed15d6847fedfa1c1aaaeb705e44ee5  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/parent/CUSTODY_FINAL_CX3V001.json
143afa3d7077e606383da50c2a16c4cb85946c7182a0c66eb879ba0f97b32dec  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/VALIDATION_FINAL_CX3V001.json
```
