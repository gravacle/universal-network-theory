# REVIEW_RECORD_0353_V001: distinct adversarial review of the V003 SPARC ordinal-geometry extractor

**Task:** Codex1 0353
**Reviewed artifact:** `extract_sparc_geometry_metadata_v003.py`, SHA256 `4dc8e3874a2908260194870ebb6900965f969993c98417dbaabe684b7d392dd0`
**Manifest:** `FILE_MANIFEST_0353_V001.json`, SHA256 `f9194cdfeb6fc1b4ff04616c090c33e2fef8168377bee09a7b71e19edee9f8f1`. The reviewer verified all 8 entries.

**Roles:**

| Role | Agent |
|---|---|
| Author (implementation helper) | Claude helper a29414925248942ad |
| Distinct reviewer | Claude helper a9f7371c107f28a8c |
| Coordinator | CLAUDE2 main session |

The reviewer did not write any of the reviewed code.

**Verdict:** `PASS_WITH_NOTES`. The review found no MEDIUM-or-higher findings and no SHOULD-FIX items. The extractor needs no V004.

## Checks Codex required (0353)

- **Literal-field mapping:** PASS. The field contract agrees with the extractor's constants, key lists and synthetic success output.
- **All guards, including C9:** PASS. C9 is a load-bearing rejector:
  - 9 of 9 one-byte slot shifts that keep 7 tokens are rejected.
  - R2, R2c and R3 each fail with exactly `E_SPAN_ENDS`, both in the no-anchor row and in the anchored row with the attacker's best anchor.
- **Exact byte boundary:** PASS.
  - The source-buffer slice log shows the header [0, 5159] plus 11 data-line slices of at most 41 bytes, and 109 `find` calls, all on LF.
  - Edge cases are correct:
    - A 41-byte row passes; a 40-byte row fails.
    - A CR at byte 41 is rejected; CRLF at byte 42 is benign.
    - A 1 MiB 0xFF tail is benign.
- **No values on failure:** PASS.
  - When one row fails, the output carries booleans and codes only; see `review_0353/E9_mixed_stdout_rerun.txt`.
  - A post-parse exception gives exit 3 with the exception type only.
  - An infinite anchor fails closed and is not echoed.
- **Preserved output custody (0348 protocol):** PASS.
  - The publication functions are AST-identical to 0348 v005 apart from docstrings.
  - Success leaves the output and `.candidate` hard-linked: nlink 2, mode 0444.
  - A rerun gives `E_OUTPUT_EXISTS` and leaves the bytes unchanged.
  - Dangling and racing symlinks are refused, and their targets are not created.
  - Wrong names give `E_OUTPUT_NAME`.
  - A missing parent directory gives exit 4 and creates nothing.

## Re-execution and attacks

- **Author harness, re-run from a scratch copy:** 131/131 cases pass. The cases array is identical to `SYNTHETIC_TEST_RECEIPT_0353_V001.json`; only the paths differ.
- **Supplied diffs:** V002→V003 and 0349 checker→V003 are identical to the reviewer's recomputed diffs, excluding header lines.
- **Fuzz equivalence:** V003 `check_prefix` and the 0349 checker produce identical fail-code lists on 120,000 fuzzed prefixes; 3,392 of the prefixes pass.
- **Reviewer attack suite:** 39 cases. 38 passed. The 39th was a substring bug in the reviewer's own checker; it was re-run by hand and is clean.

## Residual assumptions (carried as declared, not discharged)

- **A1b, T↔f_D cell transposition in the NGC3198 row:** reproduced end to end (attack E1). With an anchor-consistent swap, the extractor accepts and emits a misread f_D token, and labels A1b `DECLARED_NOT_DISCHARGED`. This matches the 0353 instruction that A1/A1b are catalogue-integrity assumptions, carried rather than closed.
- **DDO154:**
  - A swap with a two-digit T is rejected (`E_SHAPE_f_D`).
  - A swap with a one-digit T is accepted, with A1b DECLARED computed from token width.
- **A2 and A3:** retained as assumptions.

## INFO notes for root (non-blocking)

1. **Anchor regex** `[0-9]+(?:\.[0-9]+)?` (line 189) is stricter than 0349's `float()`. If the real manifest anchor text contains whitespace, a sign or an exponent, root's run fails closed with `E_ANCHOR_TEXT`. This is a readiness risk, not a safety risk. It was not checked against the real manifest text.
2. **A1b label** `EXCLUDED_BY_BYTES_TOKEN2_TWO_DIGITS` also depends on the Note (2) f_D domain. A successful output therefore reveals that DDO154's T token has two digits. K1 permits this.
3. **Failure output:** on failure, the passing target's C8 and C10 booleans are printed. They are booleans only and within the spec.
4. **`check_prefix`** relies on `main`'s 41-byte slice (line 161) rather than slicing itself. A direct caller passing a longer line fails closed with misleading codes. `main` never does this.
5. **Header structure check** covers only lines 10–17 and 30–38. The remaining header bytes are protected only by the source SHA pin.
6. **`exposure_label` values** are inherited from V002/0344. They are not in root's 0353 acceptance list, so root should confirm them against its own register.
7. **Truncation at byte 41:** a row truncated exactly at byte 41 passes. This is inherent to the bytes 1–41 scope and is already listed in `not_established`.

## Expected real-file outcome

This is the reviewer's inference, not a run. It combines the 0349 real booleans with the fuzz equivalence.

- Validation passes unless note 1 triggers.
- Spans:

  | Field | NGC3198 | DDO154 |
  |---|---|---|
  | D | [17,21] | [18,21] |
  | e_D | [24,27] | [24,27] |
  | f_D | [30,30] | [30,30] |
  | Inc | [32,35] | [32,35] |
  | e_Inc | [38,40] | [38,40] |

- Assumption states:

  | Row | A1 | A1b |
  |---|---|---|
  | NGC3198 | CLOSED | DECLARED |
  | DDO154 | DECLARED | EXCLUDED |

## Reviewer constraints observed

- No real extraction and no value-emitting run on the real MRT.
- The real MRT was hashed, and read only through its 98th LF.
- No real data-row bytes were read beyond the header.
- Not opened:
  - velocities;
  - rotmod/MassModels files;
  - V001 quarantine files.
- No network.
- Nothing was written under Universal Network Theory.
- No deletions. The aborted `runs/attack01` scratch directory was kept.
- All Python ran with `-I -B`.

## Review evidence (copied read-only into `review_0353/`)

| File | SHA256 |
|---|---|
| attack_v003_r2.py | `e75af65c512416910a70148d3b04f232da976fd0dd836d04d582ced4947fde16` |
| attack02_results.json | `580ad30760db41fe4f09a7d14327f59f3298da92a63fa7903429095747c9652e` |
| receipt_run01.json (author-harness re-run) | `2658aee899863269089e8f062dc71e79e39fb12a84c5e3cff35c90e9bd46c2e3` |
| E9_mixed_stdout_rerun.txt | `5fd3e9d6a88f0bd3eb5ed209d7d660810f50cf62b56309b2cb83ca5cf5b6328f` |

## Status

- **REVIEWED** (distinct Claude review). This is code review only.
- Root review and the single real extraction remain root-only.
- This is not physical geometry adoption.
