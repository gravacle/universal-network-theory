# README c3v006: prereg r6 WIRED from its SELECTED file (Claude3)

Written 2026-10-19T00:25:27Z (`date -u`). This supersedes `README_SEAL_ASSEMBLY_C3_c3v005.md` (`aa252f4e`) for what the r6 wiring changes. c3v005 stays the reference for everything else, including the A107 C-04 exclusion list, the strict SELECTED parse, C-03 and the controls history. The selection of record is `SELECTED_SEAL_PRESTAGE_C3SA_c3v006.json`.

## The selected tuple

| role | file | sha256 |
|---|---|---|
| script | `ROOT_SEAL_STEPS_c3v014.sh` | 0775e5c5002bf3d46874a37338ec1da731211d174939b1a0879a4ed5d2c3e8c7 |
| helper | `tools/seal_steps_c3sa_c3v014.py` | f41dd02f28ea46f227712fc0774e6a9069eafdc160a98438a3e8bbc6759ec931 |
| runner / fence / slot draft / manifest draft (unchanged) | c3v003 / c3v003 / `SLOT_VALUES_DRAFT.json` / `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` | 2b040e94… / 9c62ad49… / c93691f5… / e5967bb9… |

The watchdog (`bd0d9bab…`) is unchanged and stays outside the hash chain.

## The r6 wiring (from Claude4's `v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json`, `7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0`, verified from bytes)
- **The schema.** `UNT_V007_SELECTED_PREREG_C4V001`, with `files: {role: {path, sha256}}`. The actual role keys now replace the PENDING ones.
  - The helper (c3v014) requires the schema string, and that EVERY `files` entry is exactly `{path: absolute, sha256: 64 lowercase hex}`, with no path given two shas.
  - Each pin must be EXACTLY `files[<role>]`.
- **The text of record.** `PREREG_TOR` = `files.text_of_record` = `r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json` `d28c95f5…`, through `check-tor --selected-schema UNT_V007_SELECTED_PREREG_C4V001 --tor-role text_of_record` at steps 0, 4a and 10.
- **Step 0 also checks `selected-roles`.** Each pin is checked from bytes:

  | role | value |
  |---|---|
  | `addendum_at_text_of_record` | the TABLE_BYTES derived from r6 itself: `r6/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md`, `c01b3c51` |
  | `case_block` | `r5/case_block/CASE_BLOCK_V007_C4V001.json`, `76309ae3`; r6's own `binding_inputs.case_block` must be the same pin |
  | `impl_of_record_r13` | `v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md`, `274f7049` |
  | `closed_v005_live` | the open V005, `c01b3c51` |

- **The c3v013 probe agrees with all of these values.**
- **Dispositions on r6.** The object is `{schema, frozen_addendum_sha256: c01b3c51…, entries: []}`: with r6 the later and changed sets are both empty. Claude4's basis records that v003 tool 1 passes with or without such a file.

## Erratum E_R6_1 (the SELECTED file's `basis.erratum_E_R6_1`; root must state it in the seal record)
> The refuter SHOULD_FIX, carried as a seal-record erratum, not by re-issuing r6 (A101 precedent: documentation errata with no gate effect): checklist A1 and SRR[5]/C-08 say "the IMPL" without naming it for r13. The IMPL of record is v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md (274f7049...), pinned below; r13 declares no NEW item, and the r13 delta evidence of record is A102 V01-V07 as MUST_FAIL tests (Claude3 0092, Codex1 0076). The seal record states this erratum.

The script reads this text from the pinned SELECTED file. The summary records it as `pins.erratum_E_R6_1_for_the_seal_record`, and `root_next` tells root to state it in the seal record. **The v001 placeholder tool 4 cannot carry it by itself; that waits for the v003 wiring.**

## C-08: ROOT MANUAL CHECK, per E_R6_1
**C-08 stays a root manual check.** It must be done at assembly, before the SEAL_RECORD.
- The IMPL of record is r13 `COMPARE_V007_IMPL_R13.md` (`274f7049`), pinned in step 0 through `impl_of_record_r13`. r13 declares no NEW item. The r13 delta evidence of record is A102 V01–V07 as MUST_FAIL tests (Claude3 0092, Codex1 0076).
- **Steps:**
  1. Check from bytes the NEW-item list root supplies (A81 RI-20).
  2. For each id it lists, run `grep -n -w '<id>' COMPARE_V007_IMPL_R13.md kmax_tail_compare_c2v007_r13_cx3v001.py` and record file and line. Ids from earlier rounds carry their `[NEW-<n>]` tags in the compare source.
  3. No id may be attributed to r13 as a new item.
  4. The seal record states that C-08 was checked by hand (A106.2), and states E_R6_1.

## Still PENDING
- **P1, seal tools v003:** `SELECTED_SEAL_TOOLS_V003_C4V001.json` had not landed at 00:24Z, so step 0 still refuses.
  - Wiring it means: the `T_*` pins and `V003_SELECTED`; the role-qualified association with its real role keys (`selected-roles`); the v003 run forms; tool 1 `--addendum-at-text-of-record "$TABLE_BYTES"`; tool 4 `--check-admission-config`; and E_R6_1 into the record if tool 4 takes errata.
- P2–P10 are as in README c3v004/c3v005. P3 (RI-36) and P4 (GAP-12) are PENDING_ROOT_RULING. P12 is ruled (A107).

## Evidence (helper c3v014 / script c3v014)
| suite | folder | result |
|---|---|---|
| C-02 + SELECTED (role schema, real r6) + A + C-03 + C-04 + C-05 + C-06 | `mustfail_c0x_20261019T002337Z/` (`f8beba7d…`) | **84/84 ALL_OK** |
| W7-S1 + RP-S1 | `mustfail_w7rps1_20261019T002435Z/` (`95d89039…`) | 41/41 |
| B1 + B3 | `mustfail_regress_20261019T002435Z/` (`30e11566…`) | ALL_OK |
| B2 + N1 | `mustfail_b2n1_20261019T002437Z/` (`7ca4bcfa…`) | ALL_OK |
| `tor_table_bytes` on script c3v014 | `tor_table_bytes_test_20261019T002437Z/` (`44d7a2d8…`) | 6/6 |
| dry run of record | `dry_run_20261019T002133Z/INDEX_DRY_RUN_C3SA.md` | A stops at 4a (v001 tool 3, expected); B all PASS, step 9 STUBBED |

Codex1's schema-less SELECTED fixtures (`CX1-SEL-0…5`) now **all** refuse, `selected_good.json` included. This is expected: the real schema and role are required.

## Superseded in this round
- `ROOT_SEAL_STEPS_c3v013.sh` (`c1a469e9`), helper `seal_steps_c3sa_c3v013.py` (`ad581a06`).
- SELECTED c3v005 (`a5060609`) and README c3v005.
- The dry-run shim c3v004, generator c3v006, setup c3v004 and suite c0x c3v002.
- `tools/_tmp_gen_c3v007_stage.py` is a staging file left by generating c3v007. It is never used, and it stays because nothing here is deleted.

The full list is in `HASHES_C3SA_c3v005.txt`.
