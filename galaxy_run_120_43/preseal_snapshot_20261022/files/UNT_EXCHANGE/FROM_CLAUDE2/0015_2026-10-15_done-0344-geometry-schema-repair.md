# 0015 — DONE 0344: geometry schema diagnosis + fail-closed extractor V002

From CLAUDE2 to Codex1. No real-source execution by Claude; no geometry adopted; no velocity field inspected. The original V001 script (418e9793…) and the quarantined output (c2d709ff…) are unchanged.

Directory: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/geometry_schema_repair_0344/`

| File | sha256 |
|---|---|
| extract_sparc_geometry_metadata_v002.py | 9ac0275b583b5014062006ddc05638766ed25ea060f39efd26b501edcfb0c297 |
| V001_to_V002.diff | 0c9104193108f980deab0c3c7edb3b7ee5468fb831cf974bb6541467c99366a0 |
| SPARC_GEOMETRY_ALLOWED_FIELD_SPEC_V002.json | 837251c5290e733bbbc4e84a4308036b564f5605c78b6acaffef60ea06495fa1 |
| SCHEMA_DIAGNOSIS_0344_V001.json | d87b953acb7ac675f229d4beab9f25723bd670a9186fc2482f12e5d43e665821 |
| TESTS_0344_V001.json | d0b02899f1d4535805744a665206f6c53fcb5fa3adeeb476994473a3369c98c5 |
| test_extract_v002_synthetic.py | 0b27b605590a47209c0d3d6f1eabf5d1ccc4cdee4e5d7ef6e5fed22db112dfc5 |

**Diagnosis.** Bytes 1–39 of lines 104 and 152 only, reported as class masks and token spans with no values. The CDS ReadMe documents those bytes as Name/Type/Dist/e_Dist/f_Dist/i/e_i.
- **The actual rows follow neither documented layout.**
- **In-file MRT header:** tokens straddle field boundaries for D, e_D, f_D, Inc and e_Inc in both rows, which is why V001 emitted malformed literals.
- **CDS table1 (ReadMe 457f61cd…):** matches bytes 1–27 only (Type, Dist, e_Dist contained, right-justified and format-valid). From byte 28 every token sits one byte right: f_Dist at 30 (documented 29); i at 32–35 (documented 31–34); e_i starts at 38 and runs past 39.
- **Observed token ends** are 14, 21, 27, 30, 35 and ≥40. They are consistent with each MRT header field widened by one leading blank. That is recorded as a hypothesis only: it is undocumented locally, and e_Inc's end byte is beyond the inspected window.
- **Names** are right-justified in bytes 1–11.
- **Earlier program code** (sparc_effective_transfer_v001.py, parse lines only) read this table by whitespace splitting, so the byte layout was never exercised before V001.
- **Why my 0337 fixture passed:** it reproduced the declared schema, not this source.

**V002 extractor.**
- It accepts a layout only if it is documented (the in-file header verified line by line; the CDS ReadMe pinned with all seven table1 description lines verified) or declared by root via `--declared-layout PATH SHA256` (provenance fields required; no byte beyond 41).
- Strict checks: right-justified digits only, exact decimals, no sign/exponent/nan, documented blank bytes blank, row reaches the last byte, target found exactly once, D>0, errors ≥0, f_D∈1..5, 0≤Inc≤90, Type 0..11, and CDS documented column ranges.
- Statuses: PASS_DOCUMENTED_LAYOUT, PASS_DECLARED_LAYOUT, or FAILED_*. Never plain OK. A FAILED output carries masks and booleans only, no values.
- **Predicted result of root's real run:** FAILED_SCHEMA_VALIDATION, with per-field failures listed in the diagnosis (from a replica whose bytes 1–39 class masks equal the real rows').
- **Conditional repair:** the diagnosis includes a DRAFT declaration (clearly not a declaration) for root to author and pin if it chooses. The alternative is to obtain a documented layout that reproduces the observed boundaries.

**Tests:** 25/25 synthetic, listed in TESTS_0344_V001.json.
- CDS-layout PASS and MRT-layout PASS.
- The real-spacing replica FAILS under V002, while V001 on the same replica returns OK with 5 malformed fields, reproducing the defect.
- The replica plus a pinned declaration gives PASS_DECLARED.
- 19 synthetic failures, each fail-closed: non-numeric, sign, zero D, bad method code, Inc 95, blank field, missing, duplicate, truncated row, nan, exponent, wrong decimals, below documented range, wrong declaration sha, declaration beyond byte 41, declaration conflict, output exists, source pin, tampered ReadMe.
- A fake Vflat sentinel beyond byte 41 never appears in any output.

**Exposure wording corrected.** V001 (and my 0337 note) said excluded bytes never enter a variable. That was inaccurate: the whole file was read, hashed, decoded and split, and only the 34-byte truncations were interpreted and emitted. V002's wording: the whole file is read, hashed and split into byte lines; bytes 1–11 of each post-header row are compared with the target names; for target rows only bytes 1–41 are kept and interpreted; nothing beyond byte 41 is decoded, parsed, compared, measured or emitted.

**Incidental:** a grep for parsers displayed one code line asserting the DDO154 MassModels distance value (a distance, not a velocity). No velocity values were seen or used.

Task states: 0336–0340, 0342–0344 DONE; 0341 IN PROGRESS (write-up next; will use NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json as radius metadata only). Polling active.
