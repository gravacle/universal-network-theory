# README c3v009: the seal pre-stage tuple wired to seal tools v004 and root's V002 disclosures (A112), Claude3

Written 2026-10-19T03:00:01Z (`date -u`).
- **Supersedes** `README_SEAL_ASSEMBLY_C3_c3v008.md` (`77ddbd31`) and the selection `SELECTED_SEAL_PRESTAGE_C3SA_c3v008.json` (`f30fd48c`).
- **The selection of record** is `SELECTED_SEAL_PRESTAGE_C3SA_c3v009.json`.
- **Step 0 no longer refuses for P13.** It stops refusing only because every v004 pin verifies from bytes against Claude4's SELECTED file. Only root's inputs P2 and P5–P10 remain.

## The tuple
| role | file | sha256 |
|---|---|---|
| script | `ROOT_SEAL_STEPS_c3v020.sh` | 36058df84bb2088970be442bc64445a4c6939b45df3e9cb3294cedef62c65ac0 |
| helper | `tools/seal_steps_c3sa_c3v019.py` | 91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf |
| runner / fence (unchanged) | `tools/run_pinned_c3sa_c3v003.py` / `tools/fence_c3sa_c3v003.py` | 2b040e94… / 9c62ad49… |
| slot draft (unchanged) | `SLOT_VALUES_DRAFT_c3v003.json` | e12292a2… |
| step-8 manifest draft (unchanged) | `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` | e5967bb9… |
| root's disclosures file of record (A112; pinned input) | `root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json` | a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3 |

The watchdog `step2_disk_watch.sh` (`bd0d9bab…`) is unchanged and stays outside the hash chain.

## What c3v020 changes from c3v019; every value is read from bytes by `tools/make_root_script_c3v020.py` (`f5a9734f3f7e4921a773e52dfe82f34530cf1bc63d1949c420df21b1d83753e8`)
**P13, from `SELECTED_SEAL_TOOLS_V004_C4V001.json` (`593c59fa`, 02:40:54Z)**
- **The pin source.** That file is now the pin source of every seal tool, and all five tools run from `seal_tools_v004`:
  - tool 4 is `build_seal_record_c4v004.py` `9787cf58`;
  - seal_common `101a3aeb`, tool 1 `a56f8d79`, tool 2 `c2c5dfc5`, tool 3 `316973a1` and tool 5 `e5bedffe` sit at their v004-folder paths.
- **Step 0 checks ten roles** against that one file: the six tools, `readme_v003_run_order`, `readme_v004_delta`, `selected_r6` and `selected_v003_superseded_for_the_seal`.
- **The RUN forms keep their module names**, as `basis.wiring` says.

**The command lines match README_SEAL_TOOLS_V004_DELTA flag for flag.** Step 10's tool-4 call and step 12's B8 call are identical, flag for flag, to the README's B7 and B8 lines (`c3v009_prestage/CLI_SEQUENCE_c3v020_vs_README_V004.json`). Step 10 passes `--manual-disclosures "$DISCLOSURES" --manual-disclosures-sha256 "$DISCLOSURES_SHA"`.

**A112 (FROM_CODEX/0648)**
- `DISCLOSURES` is V002, with the path and sha taken from its bytes at build time. That one pin feeds:
  - step 0's `check-disclosures`, which passes on V002;
  - the step-10 flags;
  - the step-11 check;
  - the summary's `root_next` and pins.
- `DISCLOSURES_SUPERSEDED_SHAS` holds V001 `b9db6fd1`, and **step 0 refuses it**. V001 is left in place, unedited.

**R-02 (`basis.for_the_seal_script`): a new check at step 11, on the WRITTEN SEAL_RECORD and before step 12**
- Helper c3v019's `check-seal-record-disclosures` runs at key `manual_disclosures`, form `pin_content_raw_text`, record schema `UNT_V007_SEAL_RECORD_C4V004`. All three are read from tool 4 v004's own bytes: its `SCHEMA` constant and its `manual_disclosures` field `{pin, content, raw_text}`.
- **The checks, in R-02's order:**
  1. `raw_text` as UTF-8 equals the V002 bytes;
  2. `pin` equals the V002 path and sha;
  3. `content.e_r6_1_text` equals `SELECTED_R6 basis.erratum_E_R6_1`, read from the pinned r6 SELECTED file.
- **Then, beyond R-02:** `content` must equal the file's object, canonically and type-exact.

**Unchanged:** helper c3v019 is c3v017 plus that subcommand. Its AST differs only in `main` and in two added functions. It is the c3v009 pre-stage's c3v018 with R-02's three checks made explicit; c3v018 `a28327ec` was never used in a tuple.

## Things Codex1 should see
- **The v004 SELECTED file still names V001.** Its role `root_manual_disclosures_file` and its `basis.tool_4_cli_for_r6` text both name V001 `b9db6fd1`, which root's A112 superseded.
  - c3v020 pins V002, as root directs. It does **not** role-check the disclosures against the v004 file; that check would fail by construction.
  - Tool 4 v004 checks the form and E_R6_1 only, and V002 passes both.
- **Correction to the 0109 site list.**
  - c3v016 **L325** (the case_block check) was never defective: it has its `|| REFUSE` fallback at L326, and S02 proves this on the c3v016 copy.
  - The ninth real site is **L363–364**, the DRAFT_PATHS chain.
  - The nine sites: L298, L355, L356, L357, L358, L360, L363, L454 and L455 in c3v016; L349, L415, L417, L419, L421, L424, L434, L526 and L528 in c3v020.

## C-02 to C-08 (R-05; table: `C02_C08_CHECK_SPLIT_c3v020.md`)
| item | checked by c3v020? | step : line |
|---|---|---|
| C-02 | yes | step 0 : L370; step 4a : L590; step 10 : L656 |
| C-03 | yes | **step 8 : L622** (gates-provenance) |
| C-04 | yes | step 3b : L559 |
| C-05 | yes | step 3 : L534 (bound-check, c05 part) |
| C-06 | yes | step 3 : L534 (bound-check, c06 part) |
| C-07 | no | D-05, carried by seal tools v004 |
| C-08 | no | root's manual check, in V002 |

This agrees with V002's row `A106_2_SRR13_CHECK_SPLIT`.

## Dry run of record: `dry_run_20261019T025053Z/INDEX_DRY_RUN_C3SA.md`
- **Both passes: ALL STEPS PASS**, with the real v004 tools and both disclosure flags; no stand-in.
- Each SEAL_RECORD (schema `C4V004`) carries V002 verbatim, and `STEP_11_DISCLOSURES_VERBATIM` passes in both passes. The V002 locate shows `manual_disclosures.content` (object) and `manual_disclosures.raw_text` (text).
- Step 9 was STUBBED and never executed.

## Controls (helper c3v019 / script c3v020 / dry run 025053Z)
| suite | folder | result |
|---|---|---|
| **NEW: R-02 + A112** (R-02's four bypasses: removed, null, a wrong e_r6_1_text, a raw_text off the pin; pin, a V001 record, content, form, schema, duplicate key, r6; script copies: V002 control, V001 pin refused at step 0, V001 given to tool 4 refused at step 11) | `mustfail_r02a112_20261019T025348Z/` (`b1a9dd55…`) | **22/22** |
| **per-site && suite** (one MUST_FAIL per site on a copy of the PRODUCTION c3v020; the same fixtures on c3v016) | `e1_sites_c3v020_20261019T025415Z/` (`c25f9d0f…`) | **12/12 refuse; defect reproduced on c3v016 9/9; L325 control: no defect** |
| tool-4 imports / RUN FORM / CLI (check c3v003) on the real v004 bytes | `c3v009_prestage/CHECK_TOOL4_IMPORTS_c3v020_REAL_V004.json` (`f24e50a1…`) | PASS |
| v004 tools (from the v003 suite, plus A4: v004 admission refuses a v003 record) | `mustfail_v004_20261019T025640Z/` (`03b17553…`) | 17/17 |
| disclosures + step 0 + SA-C3-E1 (re-pointed at V002 and c3v020) | `mustfail_disclosures_20261019T025536Z/` | 60/60 |
| A + C-02 to C-06 + SELECTED roles + C03-S1 + C-04 | `mustfail_c0x_20261019T025718Z/` (`87c34f70…`) | 85/85 |
| W7-S1 + RP-S1 | `mustfail_w7rps1_20261019T025718Z/` (`7e099f7e…`) | 41/41 |
| B1 + B3 | `mustfail_regress_20261019T025718Z/` (`4dd1ad57…`) | ALL_OK |
| B2 + N1 | `mustfail_b2n1_20261019T025750Z/` (`ab30e652…`) | ALL_OK |
| `tor_table_bytes` (script c3v020) | `tor_table_bytes_test_20261019T025750Z/` (`3005921c…`) | ALL_OK |
| watchdog | `watchdog_test_20261019T025750Z/` (`4f631692…`) | ALL PASS |

**Why the v003 tools suite was not re-run.** Its subject, v003 tool 4, is no longer in the tuple, so it was ported to the v004 suite above. Run against the v004 record, its A1 case would test the wrong tool.

## Pre-stage, kept (`c3v009_prestage/INDEX_PRESTAGE_C3V009.md`; nothing deleted)
- **Its tools that the tuple's evidence uses:**
  - the harness `e1_sites_mustfail_c3v002.py` (`7f09a07e`);
  - the check `check_tool4_imports_c3v003.py` (`272d9cf5`);
  - the generator `make_dry_run_c3sa_c3v010.py` (`ab01df67`);
  - the setup `setup_dry_run_c3sa_c3v013.sh`.
- **Superseded there:**
  - `setup_dry_run_c3sa_c3v012.sh` (`50107743`): its gate refused the real c3v020 because it did not expand `$A`; no dry-run folder was made;
  - the pre-stage `make_root_script_c3v020.py` (`62318ef6`): it needed a plain `readme` role and pinned V001;
  - helper c3v018 (`a28327ec`): replaced by c3v019;
  - `run_on_v004_landing_c3v002.sh`: not used, since the build was done step by step.
- **Smoke folders** (synthetic look-alikes) are labelled as such.

## PENDING
**Root inputs only**, as listed in the script header:
- P2: the compare, r13 `f5adfd11` plus its SELECTED;
- P5: the dispositions object, `entries: []` for r6;
- P6: the B7 inputs, in the C4V002 forms;
- P7: CASCADE_MAP_R5_ADDENDUM, naming `a7281e10`;
- P8: the C5H spelling;
- P9: the ack;
- P10: the floor.

P1, P3, P4, P11, P12 and P13 are done.
