# r13 independent source delta review

date -u: Sun Oct 18 21:46:41 UTC 2026

**TESTED PASS; 0 blocking findings.** 17/17 source/AST/byte/exception-seam checks pass.

Both expected source pins match. Of 440 top-level AST nodes, 439 are unchanged; only check_record_codes differs. Exact substitution of the r12 function into r13 restores all original r12 bytes, covering unchanged text outside the function as well as AST identity.

At r13 L875, parse_int=str is local to this record classification parser and retains the duplicate-key object_pairs_hook. L876 catches DuplicateKey first with its unchanged typed refusal and member naming. Only JSONDecodeError at L878 falls back to text. Other ValueError at L880 returns DRIVER_BUILD_CHECK_RECORD_UNREADABLE. Injected ValueError and UnicodeDecodeError returned that code; injected syntax error kept the registered text fallback. This source audit does not run the full comparator or re-evaluate scientific gates. V01–V07 and T01–T19 are reviewed separately.

Production admission remains **UNTESTED**. No actual check-record fixture, protected run, target data, network or scientific process was used.

Byte pins:

- r12: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py` — `4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28`
- r13: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py` — `f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157`
- selected: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/SELECTED_R13_CX3V001.json` — `10acd09887bffa5130e2ebbff7d54ab2d70ea7aff0fb2cd696e0cda0fcf6bb5e`
- declared_delta: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/SOURCE_DELTA_CX3V001.json` — `8275e8d50efdf334ab10f913b62e1e30982f76374f2017eb3d3cdafa3e539645`
- dispatch0635: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0635_2026-10-18_reassign_codex2_queue.md` — `c6fd229feeef4c399198118d5c1465a1af9a5bff029f44865e1813b5eeec9758`
- dispatch0636: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0636_2026-10-18_codex3_conserve_codex1_takes_prestage.md` — `6b29ccf2ef10e7643975c79b232a98bd080968044acfedde7a18606aa0265621`
- audit: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r13_delta_cx1/source/audit_source_delta_cx1v001.py` — `549e351607c689ec213ba3b5793a3f7a94cf837597b5f79c86652f1e25a2409a`
- report JSON: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r13_delta_cx1/source/SOURCE_REVIEW_CX1V001.json` — `f03c5bb04846b53156bca97bf3c119703e62873eb8aab17a72ea33c6742d28ee`
