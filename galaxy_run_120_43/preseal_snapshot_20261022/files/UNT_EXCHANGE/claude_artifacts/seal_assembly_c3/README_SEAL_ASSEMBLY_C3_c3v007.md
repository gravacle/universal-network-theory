# README c3v007: the FINAL seal pre-stage tuple (prereg r6 and seal tools v003 wired) (Claude3)

Written 2026-10-19T01:16:06Z (`date -u`). This supersedes `README_SEAL_ASSEMBLY_C3_c3v006.md` (`bc7e6a06`) for what the v003 wiring changes. c3v006 and c3v005 stay the reference for the r6 wiring, A107, C-02 to C-06 and the control history. The selection of record is `SELECTED_SEAL_PRESTAGE_C3SA_c3v007.json`. **Step 0 no longer refuses for P1 or P11; only root inputs P2-P10 remain.**

## The FINAL tuple

| role | file | sha256 |
|---|---|---|
| script | `ROOT_SEAL_STEPS_c3v016.sh` | dcdb746c76546169bc0b4702c832265b59115c552480f248bdd5c3f354f0a6e8 |
| helper | `tools/seal_steps_c3sa_c3v016.py` | 21f0eb09e927722237459d65cf60eae79d92acf4c6a25bb4340f1519e66d28c0 |
| runner / fence (unchanged) | `tools/run_pinned_c3sa_c3v003.py` / `tools/fence_c3sa_c3v003.py` | 2b040e94… / 9c62ad49… |
| slot draft (NEW: v003 schema C4V002) | `SLOT_VALUES_DRAFT_c3v002.json` | 02d97c376ddf231ec9e9643e21b88e57669719e9bb3687c2e8b6f30eec711e7f |
| step-8 manifest draft (unchanged) | `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` | e5967bb9… |

The watchdog `step2_disk_watch.sh` (`bd0d9bab…`) is unchanged and stays outside the hash chain.

## The v003 wiring (Claude4's `seal_tools_v003/SELECTED_SEAL_TOOLS_V003_C4V001.json`, `cf7e5b2f1b3daf55c485ada1c869bc7249040a8db8202eb1b1a90bebe1431305`, verified from bytes)
- **The schema** is `UNT_V007_SELECTED_SEAL_TOOLS_C4V001`, checked role-qualified in step 0 with `selected-roles`. The generic exact-pair search is **removed** from the helper.

  | role | file | sha |
  |---|---|---|
  | `seal_common` | `seal_common_c4v003.py` | 101a3aeb |
  | `tool_1_check_frozen_addendum` | | a56f8d79 |
  | `tool_2_check_sealed_compare` | | c2c5dfc5 |
  | `tool_3_check_slot_fill` | | 316973a1 |
  | `tool_4_build_seal_record` | | de0ceb15 |
  | `tool_5_print_driver_build_record` | | e5bedffe |
  | `readme` | `README_SEAL_TOOLS_V003.md` | 86012117 |
  | `selected_r6` | | 7200acd9; must equal the r6 SELECTED the script wires |

- **The order and CLI follow `README_SEAL_TOOLS_V003` L157 and each tool's argparse.**
  - **Tool 1 (step 2):** `--expect-frozen-sha c01b3c51…`, required by the SELECTED basis R-01, plus `--addendum-at-text-of-record "$TABLE_BYTES"`.
  - **Tool 5 (step 2a):** its stdout is written exclusively as the driver BUILD record (`25b4ff69…`; the earlier helper record `d9226430` carried a note field). The new helper `check-driver-build-record` re-checks those exact bytes, fenced: byte-equal to `builtin_r5_build()` plus the check record, and the compare's own codes.
  - **Tool 3 (4a):** `--text-of-record-sha` and `--addendum-at-text-of-record`.
  - **Tool 2 (5a):** unchanged.
  - **Tool 4 build (10):** `--text-of-record-sha`, `--addendum-at-text-of-record`, and `--b2-record` (B2_GATE_RECORD_C3V003 `915fbcda`, V009's `gate_records.B2`; r6 asks for the B2 disclosure, A100).
    - It also takes the compare's own `GATES_ONLY.json` and `VALIDITY_ONLY.json` (the B6 names), not the stdout captures.
  - **Tool 4 `--check-admission-config` (12, B8):** on the written config and SEAL_RECORD.
  - **Dispositions** (`--dispositions` and `--dispositions-sha`) go to tools 1, 3 and 4. On r6 that is the pinned `entries: []` object; pass B also proves that "no file" works.
- **The slot draft follows v003's schema `UNT_V007_SEAL_SLOTS_C4V002`.** It adds two slots:
  - `cascade_map_r5_addendum`, filled from root input P7 at invocation;
  - `admission_entry`: the BUILD_V007 launcher `861bba68` and guard `294cb776`, checked in step 0 against LAUNCHER and GUARD.
  - The helper's SLOT_KEYS follow. `COV_ARGS` now expands safely under bash 3.2.

## Erratum E_R6_1: root's manual seal-record statement
**v003 tool 4 has no errata input.** Neither its argparse nor its README offers one, so the SEAL_RECORD cannot carry E_R6_1. Root must state it, exactly as `SELECTED_R6_C4V001`'s `basis.erratum_E_R6_1` gives it (quoted in README c3v006), in the numbered root packet that publishes the SEAL_RECORD, config and receipt. The script's summary carries the exact text (`pins.erratum_E_R6_1_for_the_seal_record`), and `root_next` says so.

## The v003 SELECTED basis R-01 to R-07 (not changed by this tuple; recorded as Claude4 states them)
- **R-01:** tool 1 compares only the entry sections, so frozen-copy bytes outside them (near-miss headings, preamble) are not compared.
  - **Handled:** every direct tool 1 run gets `--expect-frozen-sha c01b3c51`, and the frozen_addendum slot sha is the same value, which tools 3 and 4 enforce.
  - **Tested:** MUST_FAIL F1 (a preamble line refuses `FROZEN_SHA_MISMATCH`); F1r reproduces that the same copy passes without the flag.
- **R-02** (a one-character `changed_text` passes), **R-03** (`prereg_revision` may pin the text of record or another byte form of the prereg) and **R-04** (a reason of only invisible characters passes): **none is reachable for r6.** The r6 seal needs no dispositions rows (L ∪ CH is empty). They are deferred to a seal tools v004 after the V007 seal.
- **R-05:** simulated TOCTOU races fail closed downstream (the sealed compare's V007_PREREG_SHA256; tool 2's frozen-to-open tie).
- **R-06: a lone-surrogate reason refuses UNTYPED (`INTERNAL_EXCEPTION`) in tool 4.** It is still a refusal, but without a specific code. Not reachable for r6, which has no dispositions rows.
- **R-07:** the v003 README L36/L238 and build note B-N1 call v003-on-r6 UNTESTED. That is stale: the refuter TESTED it (I1–I17, J1–J2), and so does this dry run.

## Dry run of record: `dry_run_20261019T010953Z/INDEX_DRY_RUN_C3SA.md`
- **Both passes run every step with the REAL v003 tools,** and step 9 is STUBBED.
- The only tool-side allowance is D-10: a dry run's FROZEN copy is in scratch, never at the real `path_to_be`. The tools' own flag and the shim, which changes one code into a note, are both published as substitutions S16 and S16b.
- MUST_FAIL F2 shows that, without the allowance, v003 tool 1 refuses a FROZEN copy that is not at `path_to_be`.

## Controls (helper c3v016 / script c3v016)
| suite | folder | result |
|---|---|---|
| **v003** (F0–F3 frozen copy incl. non-entry bytes; S1–S4 v003 roles; D1–D4 tool-5 record form; A1–A3 tool 4 admission) | `mustfail_v003_20261019T011231Z/` (`399ab512…`) | **16/16** |
| A + C-02 to C-06 + SELECTED (r6 and v003 roles) + C03-S1 + C-04 A107/verdict | `mustfail_c0x_20261019T011422Z/` (`a04d4bc4…`) | **85/85** |
| W7-S1 + RP-S1 | `mustfail_w7rps1_20261019T011311Z/` (`c6ea2f3c…`) | 41/41 |
| B1 + B3 | `mustfail_regress_20261019T011311Z/` (`ed54c393…`) | ALL_OK |
| B2 + N1 | `mustfail_b2n1_20261019T011335Z/` (`877371b8…`) | ALL_OK |
| `tor_table_bytes` (script c3v016) | `tor_table_bytes_test_20261019T011336Z/` (`98f938f4…`) | 6/6 |
| watchdog | `watchdog_test_20261019T011336Z/` (`a4194011…`) | ALL PASS |

## Left behind by this round (kept; nothing is deleted)
- **Superseded intermediate dry runs:**
  - `dry_run_20261019T010239Z` (script c3v015): stopped at 4a on the C4V001 slot schema; pass B hit a bash 3.2 empty array.
  - `dry_run_20261019T010520Z` (c3v016): stopped at 4a on tool 3's D-10 check and the old cascade fixture.
  - `dry_run_20261019T010745Z`: stopped at 10 on the old B7 fixtures.
- **Aborted, never run:** `dry_run_20261019T010213Z` (setup c3v006: a sed pattern with brackets).
- **Crashed partial control folders:** `mustfail_c0x_20261019T011311Z` and `mustfail_c0x_probe_20261019T011353Z` (suite c3v003 used the removed v003 stand-in; no results file).

## PENDING (root inputs only; step 0 refuses until they are given)
- **P2–P10**, exactly as listed in the script header:
  - P2: the compare, r13 `f5adfd11` plus its SELECTED;
  - P3: RI-36, PENDING_ROOT_RULING;
  - P4: GAP-12, EPS_NGC and I1T_NGC, PENDING_ROOT_RULING;
  - P5: the dispositions object, `entries: []` for r6;
  - P6: the B7 inputs, in the C4V002 forms;
  - P7: CASCADE_MAP_R5_ADDENDUM, which must name CASCADE_MAP_R5_C2V001 `a7281e10`;
  - P8: the C5H spelling;
  - P9: the ack string;
  - P10: the floor.
- **C-08** stays a ROOT MANUAL CHECK at assembly (README c3v006). **E_R6_1** is root's manual statement (above).
