# README_SCHEMA_C4V003: classifier A output schema supplement, c4v003 (schema only)

Lane Claude4 helper, 2026-10-19T19:54:54Z. For Codex1's independent classifier B. Successor of `schema_c4v002/` (README `f399d3878a17569ace9455db7372d0c915acf90194ac7bf206c35c7170b30534`, schema `1b0f9866bb67115a731835cf0570c5efece126a5b319afc65e527f57d8177758`, constants `78035ae128017cf490e6df5abf68447d12d8dcc05c9048e527e040c7c7852f38`). It describes the output of `claude_artifacts/classifier_a_c4/build_c4v003/classifier_a_c4v003.py`, sha256 `394a8b6116b4cbb795de303a7a51778b671b39599cd7df5e032cadc97f7946e5`, read off `diff -u` against `classifier_a_c4v002.py` (`a11ae7b9c062899d806d25af9d9649eef9f4f21105218484ba224c26d7983e81`; `work/diff_c4v002_c4v003.diff`, 18 hunks, every hunk read) and the c4v003 code wherever a hunk touches output, with its README (`512b5c59df5b9f167daa3473752b3f25491078c334c5c537aec8a3b208cebc0e`), and checked with jq against the 47 c4v003 outputs in `build_c4v003/work/outs_d02/`. Ln = line n of classifier_a_c4v003.py.

## DELTA against c4v002

Everything not listed here is unchanged from c4v002 and reads as `schema_c4v002/README_SCHEMA_C4V002.md` describes it: the other 173 `$defs` are byte-identical under `jq -S` to those of `OUTPUT_SCHEMA_C4V002.json`, the root `oneOf` and `$schema` are unchanged, and the other 85 constant groups are identical (Check 4).

**Schema `$defs`: 17 changed, 5 added, 1 removed.**

| $def | change | written by |
|---|---|---|
| `classifier_const` | const `classifier_a_c4v002` -> `classifier_a_c4v003` | NAME L36; printed L1960, L2105, L2130, L2559, L2563 |
| `stage0_status_read` | `result_first_available_utc` removed; `source` (`stage0_source`) and `post_score_exploratory` (boolean) added, both required; `phase2_step4_start_utc` a time -> a time or null; `receipt_times_utc` items a time -> a time or null; `allOf` adds `stage0_read_rules`; description | the dict L1390-L1393, from `_stage0_facts` L1527-L1528; null start L1469-L1470; null `written_utc` L1483, L1487; source L1377, L1388 |
| `stage0_source` (added) | enum `STAGE0_STATUS_RECORD_C4V003`, `FREEZE_MANIFEST_STAGE0_STATUS_BLOCK` | L82-L83; L1375, L1377, L1388 |
| `stage0_read_rules` (added) | seven cross-field rules of a read status: (1) EVALUATED_BEFORE_FREEZE and EVALUATED_REFUSED come only from the block, with a step-4 start and at least one receipt time, none null; (2) source record implies NO_SEALED_SUCCESSOR; (3) `post_score_exploratory` iff RECEIPTS_AFTER_STEP4, which needs a start and a receipt time; (4) a null receipt time implies STAGE0_RECEIPT_NOT_FINISHED; (5) a null start with a member implies STAGE0_RECEIPT_NOT_FINISHED; (6) the block with no member implies STAGE0_RECEIPT_NOT_FINISHED; (7) the record with no member gives reasons exactly `[NO_SEALED_SUCCESSOR]` | finished rows L1490-L1495; rule (a) L1503-L1504; rule (b) L1507-L1510; on time L1513; reasons L1516; reading L1521-L1522; post_score_exploratory L1525-L1528 |
| `stage0_block_defect_word` (added) | enum of the 27 words below, in the order the checks run | `_stage0_block_facts` L1408-L1447, `_stage0_facts` L1467-L1526; printed L1374-L1376 |
| `stage0_status_block_defect` (added) | `{status: NOT_AVAILABLE, reasons: [STAGE0_STATUS_BLOCK_DEFECT], source: FREEZE_MANIFEST_STAGE0_STATUS_BLOCK, defect: <word>}` | L1373-L1376 |
| `stage0_status_phase2` | `oneOf` adds `stage0_status_block_defect`; description added | L1370-L1388 |
| `stage0_status_phase_null` (added) | `stage0_status_phase2` without the block source: a null phase reads root's record | `successor_mode` L550; L2475-L2476 |
| `header` | phase-null branch: `stage0_status` -> `stage0_status_phase_null`; `stage0_status` description | L2475-L2476, L550 |
| `stage0_p2` | new case: the block defect with `twin: TWIN_INPUT_DEFECT`, `comparison: null`; the six read cases take the keys, types and rules of `stage0_status_read`; EVALUATED_REFUSED described as a receipt or evaluation refusal, block only; description (eight cases) | L2298-L2299, L2287; L1390-L1393; L1521-L1522 |
| `stage0_reasons_not_evaluated` | description only (reasons from the record or the block); enum unchanged | L1516 |
| `alt_stage0_defect` | `reasons` const `[STAGE0_STATUS_RECORD_DEFECT]` -> enum adding `[STAGE0_STATUS_BLOCK_DEFECT]`; description (source and defect are not copied) | L2360-L2361 over L1375, L1387 |
| `part2_drift` | TWIN_INPUT_DEFECT `reasons` enum adds `[STAGE0_STATUS_BLOCK_DEFECT]`; description | L2298-L2299, L1283 |
| `na_drift_part1` | items enum adds `STAGE0_STATUS_BLOCK_DEFECT` | L1234-L1235 with L2299 |
| `agreement_record` | property `at0b_values_sha256` (`hex64`) added; rule: present iff `at0b_members_sha256` is, so only on an AT-0b record under the `7d891ff7` pin; description | L1666-L1667; L1743-L1749 |
| `agree_defect_word` | enum adds `AT0B_VALUES_SHA256` after `AT0B_MEMBERS_SHA256`; description | L1746-L1747 |
| `failing_v003a`, `reported_v003a` | description only: these v003a encodings now print under the `7d891ff7` pin (phase1_c2v003b); c4v002's v003a pin reads PHASE1_TOOL_PIN_DEFECT | PHASE1_TOOLS L60-L62; L1731-L1733 |
| `row_main_kind_rules` | `near` on HIT, INVALID_AS_MISS and LATE_GATE_MISS rows is `false` only (was `false` or `{NOT_AVAILABLE: [FIELD_DEFECT_ENVELOPE]}`, c4v002's OC-35); description | basis row T3: L2158-L2161, L2211 |
| `na_near_row_envelope` (removed) | no longer referenced | as above |
| `na_near` | description only: FIELD_DEFECT_ENVELOPE only on a tier-MISS row | L2162-L2163, L2168-L2175 |
| `a15` | `E1.a.Q03_Q15` items: tier HIT or INVALID_AS_MISS implies `near: false`; description | L2385 over L2158-L2161 |
| `stop` | description only: the companion file is OUTPUT_CONSTANTS_C4V003.json | (none) |

Root annotations `$id`, `$comment`, `title`, `description`: the c4v003 names and the classifier sha (NAME L36).

The 27 block defect words, in check order: STAGE0_SUCCESSOR_PIN_NOT_BOUND, MANIFEST_SCHEMA_NOT_SUCCESSOR, BLOCK_KEYS, BLOCK_MODULE, BLOCK_SUCCESSOR_SHA, BLOCK_STATUS_RECORD, BLOCK_DIAGNOSTICS, then `_stage0_facts`: PHASE, STEP4_START_UTC, SEALED_SUCCESSOR, MEMBERS, MEMBER_ROW, MEMBER_WRITTEN_UTC, MEMBER_FINISHED, MEMBER_BEFORE_STEP4 (per member), RULE_FLAGS, LISTS, RULE_A, RULE_B, RECEIPTS_BEFORE_STEP4, REASONS, EVALUATION_REFUSALS, READING, POST_SCORE_EXPLORATORY, then BLOCK_MEMBER, BLOCK_MEMBERS_NOT_THE_PRIMARY_MEMBERS, STAGE0_STATUS_RECORD_NOT_THE_BLOCK_PROJECTION.

**Constants: 9 groups changed, 2 added, none removed.**

| group (field) | change | written by |
|---|---|---|
| `schema`, `describes`, `rule` | the c4v003 names; the classifier sha | L36 |
| classifier (every form) | `classifier_a_c4v003` | L36 |
| stops[].code and status_code: class ALL stop codes | `from` adds Run.check_manifest_schema | L563, call L1976 |
| stops[].detail templates: FIELD_DEFECT_OUTSIDE_ROWS | adds `freeze manifest schema %r is not %s, the schema of the freeze module the seal names for %s (M-5 addition 2; A154)`; `from`; `note` (fill-ins FREEZE_MANIFEST_C2V003G L64, FREEZE_MANIFEST_C2V003G_STAGE0_C2V002 L65, the phase or `PHASE_2 with the STAGE0 successor pinned` L566) | L563-L566 |
| stops[].detail templates: FIELD_DEFECT_ALTERNATIVE | adds `STAGE0_GRID_OUTER: the frozen stage0_status block of the STAGE0 successor is not bound or malformed (%s)`; `note` | L2066-L2068 |
| STAGE0 reasons | adds `STAGE0_STATUS_BLOCK_DEFECT`; `from` (S0_RNF, S0_NSS, S0_RA4) | L1375; L85, L1516 |
| STAGE0 source (added) | `STAGE0_STATUS_RECORD_C4V003`, `FREEZE_MANIFEST_STAGE0_STATUS_BLOCK` | L82-L83; L1375, L1377, L1388 |
| STAGE0 block defect words (added) | the 27 words | L1408-L1447, L1467-L1526 |
| agreement.agree_record_defect | adds `AT0B_VALUES_SHA256` | L1747 |
| agreement.failing_member_rows[].category | `note`: OUTSIDE_BOX_SLICE only under the `7d891ff7` pin | L60-L62, L1733 |
| agreement.target_free_always_reported (checked words) | `field` names the `7d891ff7` pin | L1733, L1818-L1823 |
| NOT_AVAILABLE codes: readings[R-DRIFT].part1 | adds `STAGE0_STATUS_BLOCK_DEFECT` | L1234-L1235, L2299 |

**Removed from the output:** the key `result_first_available_utc`. The only constant value that left is `classifier_a_c4v002`.

## New corners and fixed forms

- **A null phase reads the record.** Successor mode needs PHASE_2 (L550): with refused phase inputs (blanked output, header printed) `header.stage0_status` is the record defect or read from the record (`stage0_status_phase_null`).
- **The record is never evaluated.** Rule (b) is false on the record by construction (L1510): NOT_EVALUATED_BEFORE_FREEZE with NO_SEALED_SUCCESSOR; with no member exactly `[NO_SEALED_SUCCESSOR]` (the default no-successor record, OC-41). The block with no member reads STAGE0_RECEIPT_NOT_FINISHED (`bool(members)`, L1504).
- **Null times.** The step-4 start may be null when no member is finished (L1469-L1470, L1490-L1493). A receipt time is the member's `written_utc` (L1392), null iff that is null; the code does not tie it to the receipt pin of an unfinished block member (L1428-L1434).
- **The STAGE0 entry of `alternatives`** copies status, reasons, twin and label only (L2361): a block defect shows `[STAGE0_STATUS_BLOCK_DEFECT]` there without source or defect; times and `post_score_exploratory` never appear there.
- **Stops of a block defect.** Every block defect adds FIELD_DEFECT_ALTERNATIVE for STAGE0_GRID_OUTER (class ALT: NOT_READ, not blanked; S08, S09, S13, S15-S17, S22). MANIFEST_SCHEMA_NOT_SUCCESSOR also meets the manifest-schema FIELD_DEFECT_OUTSIDE_ROWS (class ALL), so the output is blanked while `header.stage0_status` carries the block defect (S10, S11). Record-path words (RECORD_KEYS L1383 and the fact words) are never printed: the record defect keeps c4v002's fixed detail (L2070-L2071).
- **NEAR (basis row T3).** An envelope stop no longer blanks NEAR, or N(Z), `e3_line.N`, `a15.E1.a.N`, through a HIT, INVALID_AS_MISS or LATE_GATE_MISS row; a tier-MISS row it names still prints `{NOT_AVAILABLE: [FIELD_DEFECT_ENVELOPE]}` and blanks its zone's N (T3C).
- **Item 11 pins.** The output still does not print which pin was bound; the failing-entry key set and the at0b pair show it (P's README item 4, now with `at0b_values_sha256`).

**Not determined by the code alone** (additions to P's list): `phase2_step4_start_utc` and `receipt_times_utc` are ECHO of the source's strings (a time `parse_utc` accepts, with the `utc` def's caveat, or null); the manifest-schema detail formats the manifest's `schema` with Python's `%r` (a quoted string, `None`, or another repr).

**A's open choices printed as fixed forms** (c4v003 README OC table): OC-36 (a wrong manifest schema is FIELD_DEFECT_OUTSIDE_ROWS; in successor mode the block also reads TWIN_INPUT_DEFECT), OC-37 (another successor pin: STAGE0_SUCCESSOR_PIN_NOT_BOUND), OC-38 (root's record optional in successor mode, else STAGE0_STATUS_RECORD_NOT_THE_BLOCK_PROJECTION), OC-39 (the block's own reading is printed), OC-40 (block phase null or PHASE_2), OC-41, OC-42 (block members: the frozen PRIMARY members), OC-46 (a scored Phase 1 without phase1_header reads PHASE_MISMATCH; B must share it), OC-47, OC-48 (NOT_SUPPLIED for a missing agree record), OC-49 (RECEIPTS_AFTER_STEP4 as the block encodes it). c4v002's OC-35 is resolved by T3.

## C9 against the bytes

What C9 and "The output" state holds in the bytes: `at0b_values_sha256` (L1666-L1667, v003b AT-0b only, L1743-L1749); the read dict gains `source` and `post_score_exploratory` and loses `result_first_available_utc` (L1390-L1393); the block defect form (L1375-L1376); the record defect as in c4v002 (L1387); R-DRIFT's code list (L2299); `near: false` on non-MISS rows (L2158-L2161); `classifier_a_c4v003` (L36). Discrepancies (omissions, and one wording point):
1. C9 omits the new FIELD_DEFECT_OUTSIDE_ROWS detail for a wrong manifest schema (L563-L566); change 5 names the check, not the printed text.
2. C9 omits the new FIELD_DEFECT_ALTERNATIVE detail of a block defect (L2066-L2068); "The output" only says that the detail names the word.
3. Neither says that `phase2_step4_start_utc` can now be null (L1469-L1470, L1391); c4v002 required a time.
4. "The output" says a receipt time is null "where no receipt"; the bytes print `written_utc` (L1392), null iff it is null, which the code does not tie to the receipt pin of an unfinished block member (L1428-L1434).
5. C9 omits the new `agree_record_defect` word AT0B_VALUES_SHA256 (L1747; change 2 has it).
6. C9 omits `[STAGE0_STATUS_BLOCK_DEFECT]` in the STAGE0 entry of `alternatives` (L2361).
7. C9 names `near` only; with it `zones[].N`, `e3_line.N` and `a15.E1.a.N` print a count where c4v002 blanked them for an envelope defect on a non-MISS row (L2168-L2175; change 6 has it).
8. C9 does not restate the output effect of C6: under c4v002's v003a pin, item 11 and the band column now read PHASE1_TOOL_PIN_DEFECT (words unchanged; L60-L62, L1577-L1578, L1731-L1732).
9. "The output" places the new STAGE0 form "in Phase 2"; the header also prints the record form under a null phase (L550, L2475-L2476).

## Checks (jq only; details in PARTIAL.md)

1. **Outputs.** The 47 outputs (B01-B19, S01-S25, T3A-T3C) against the root `oneOf` and their expected form (prescore 1, blanked 3, Phase 1 4, Phase 2 39): 47 of 47 with 0 errors. Checker: `work/schema_check.jq`, a byte copy of P's (no keyword missing, no extension). Control: the same outputs fail P's c4v002 schema at the changed places.
2. **Mutations.** 64 in-memory mutations (jq edits, nothing written), at least one per schema DELTA item (`work/mutations_d01.txt`): 64 of 64 rejected, each at the mutated path; 5 accept controls accepted; each of the 27 defect words accepted in a block defect. Constants-only items (detail templates, `from`, `note`, `field` texts) have no schema content to reject (stop details are free strings, as in c4v002); Check 3 covers them.
3. **Literals.** Every const/enum string of the schema (388) and every constants value (437), Python's adjacent literals joined: found as whole literals in classifier_a_c4v003.py except the composed ones P listed (BAND_REGION_EXTENT_* L1897 over L1849-L1859; MISSING:<key> L1762 over L1758; query ids L43). The 69 new or changed strings: 69 found. The words raised in L1397-L1528 equal the 27-word enum as sets.
4. **Unchanged claim.** `$defs` c4v002 -> c4v003: 173 same, 17 changed, 5 added, 1 removed; the 173 streamed with `jq -S -c` from both files are cmp-equal; root `oneOf` and `$schema` equal. The classifier name occurs in both files only in `$comment`, `title`, `description` and `classifier_const`. Constants: 85 groups equal, 9 changed, 2 added.

## Files

| file | sha256 | content |
|---|---|---|
| `OUTPUT_SCHEMA_C4V003.json` | `36d8a1dc079e58a0667517504cc9acf3d445766a4fffda52e38a5af25063f541` | JSON Schema (draft 2020-12), 195 `$defs`, seven disjoint forms as in c4v002, with the DELTA above; byte copy of `work/OUTPUT_SCHEMA_C4V003_d01.json` |
| `OUTPUT_CONSTANTS_C4V003.json` | `1df18c6e6459206eff8d0210df00894942e2778473fbb9687137017c362af696` | every literal string the output can carry, 96 groups; byte copy of `work/OUTPUT_CONSTANTS_C4V003_d01.json` |
| `README_SCHEMA_C4V003.md`, `HASHES_SCHEMA_C4V003.txt`, `PARTIAL.md` | in HASHES | this page; shasum of the three deliverables; the append-only log. `work/` holds the diff, the two generators, the checker copy, the mutation table and the drafts (review aids, not deliverables). |

**Rule.** As for c4v002: schema only, no implementation and no expected case output; read off the code; outputs opened for structure and checking only.
