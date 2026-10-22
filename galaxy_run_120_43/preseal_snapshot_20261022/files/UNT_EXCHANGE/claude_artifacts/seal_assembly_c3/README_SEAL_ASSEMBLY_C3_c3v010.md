# README c3v010: the seal assembly tuple for root's seal run (registry V012, disclosures V006, root's A121 answers), Claude3

Written 2026-10-19T06:19:14Z (`date -u`), for root 0665 (`cb0d28ef`), which releases c3v010. Root's answers on P7, P8 and P9 are 0664 (A121, `b6fc8a7d`).
- **Supersedes** `README_SEAL_ASSEMBLY_C3_c3v009.md` (`ac575ce8`) and the selection `SELECTED_SEAL_PRESTAGE_C3SA_c3v009.json` (`9e10eae1`).
- **The selection of record** is `SELECTED_SEAL_PRESTAGE_C3SA_c3v010.json`; the full listing is `HASHES_C3SA_c3v009.txt`.
- **No pin is PENDING.** Every pinned value was read from bytes. Step 0 checks each of them again, then checks the run inputs root supplies (the block below).
- Nothing here launched anything, opened the C5H run, or created the real step-2 output root. Step 9 was stubbed in every dry run and never executed.

## The tuple
| role | file | sha256 |
| --- | --- | --- |
| script | `ROOT_SEAL_STEPS_c3v026.sh` (88509 bytes) | b43cc38be5f19c473167d8d57211c54d336d09d58fcfd66f5ca8187ad033c464 |
| helper (unchanged since c3v009) | `tools/seal_steps_c3sa_c3v019.py` | 91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf |
| runner / fence (unchanged) | `tools/run_pinned_c3sa_c3v003.py` / `tools/fence_c3sa_c3v003.py` | 2b040e94… / 9c62ad49… |
| slot draft | `c3v010_prestage/SLOT_VALUES_DRAFT_c3v007.json` (= c3v006 with only `producer_registry` moved to V012) | 184ff5cbc01eb2683ace5cee8fbee1e82b38d7d6ac152726713501c1ddc83729 |
| step-8 manifest draft (unchanged) | `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` | e5967bb9… |

The watchdog `step2_disk_watch.sh` (`bd0d9bab…`) is unchanged and stays outside the hash chain.

## Pinned inputs (constants in the script; verified from bytes by `c3v010_prestage/tools/verify_final_inputs_c3v010_c3v002.py`, record `VERIFY_FINAL_INPUTS_C3V010_c3v002.json` `211f6369`)
| input | file | sha256 | what was checked |
| --- | --- | --- | --- |
| producer registry **V012** | `producer_registry_c3/out/PRODUCER_REGISTRY_C3V012.json` | 4b8a3c35ca9a140bdb9e132f564d2163704e915aa67840c71c36fea551cafafa | V011 `512a7171` with only `producers.I4` (now `ri33_c3/i4/write_i4_record_c3v003.py` `707395ba`) and `note` changed. Validated on r14: `VALIDATE_R14_C3V012_CASEBLOCK_OF_RECORD.json` `a7c80f8e` (15 pre-seal records, all PASS; every registered sha matches its file; guard refusals 0) |
| root's disclosures **V006** | `root_inputs/SEAL_MANUAL_DISCLOSURES_V006.json` (11262 bytes) | 8dc28480a588f3ef7bd47ebe673767ac79745178a36141cdf50e69e8a040872a | V005 with only the row `A114_A117_I4_AFTER_SEAL` changed (its `source` and `text`); keys, schema, `e_r6_1_text` and the C-08 fields unchanged; helper `check-disclosures` PASS. Its content is not cross-checked against the A-entries here |
| B7 NEW-item list | `seal_b7_inputs_c4/NEW_ITEM_DISPOSITIONS_V007_COMPLETE.json` | 68164144b2f9bf56626be65663566e8c51afba65382e3b6789f53eb144252cd2 | unchanged (V006 row `E_A118_1` governs the A118 sentence it quotes) |
| B7 successor custody (root) | `$CTRL/V007_SEAL_ASSEMBLY_INPUTS/custody_run_v002/RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json` | 9ca16b4fd07fd470359cb604526e38807ecf50093cf59ad7895441601535f67d | verdict PASS, 24 stages |
| compare r14 / its selection / IMPL r14 | `v007_compare_c2/r14/…` | f3f9ba7e… / 6b650ece… / 2ba6d12e… | step 0 requires exactly these (A114/A116) |
| text of record r6 / SELECTED_R6 / seal tools v004 SELECTED | `v007_final_prereg_c4/…` | d28c95f5… / 7200acd9… / 593c59fa… | unchanged since c3v009 |

**Superseded and refused**
- **Disclosures** V001 `b9db6fd1` (A112); V002 `a0284ece` (0658); V003 `990be628` (0661); V004 `adac5030` (0662); V005 `b1a7b3d5` (0665).
  - All five are in `DISCLOSURES_SUPERSEDED_SHAS`, and step 0 refuses each one.
  - The refusal now reads `REFUSE: the disclosures file is a superseded version (root 0665: V006 is the file of record)`.
  - MUST_FAIL coverage: r14 suite N-10 to N-10d; R-02/A112 suite A112-1 to A112-1e (step 0), A112-2 to A112-2d (step 11) and R02-6 to R02-6e and R02-15 to R02-15c (helper).
- **Registries** V010 `b8435877`; V011 `512a7171`.
  - Neither is pinned; `REGISTRY_SHA` is V012, verified from bytes.
  - Step 0 refuses a slot draft whose `producer_registry` is not `REGISTRY`.
  - MUST_FAIL coverage: N-3c (V011 as REGISTRY, with draft c3v007), N-11b (draft c3v005, on V010) and N-11c (draft c3v006, on V011).
- **Compares:** r13 `f5adfd11` and older rounds, and `SELECTED_R14_CX1V001` `dc74949d`, are refused in step 0 (N-1, N-1b, N-2).

## Root's invocation: the filled env block
Values come from bytes and from root:
- **P2:** compare r14 and its selection (A114/A116).
- **P5:** root's dispositions file (0659; 0665's table).
- **P6:** the key map (RI-30; 0665's table).
- **P7:** CX3V001, from 0664 (A121).
- **P8:** the External1 spelling, from 0664 (A121).
- **P9:** the ack string, confirmed exactly in 0664 (A121).
- **P10:** 300 GiB, from 0659.

```bash
export UNT_SEAL_COMPARE_REVIEWED_PATH="/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py"
export UNT_SEAL_COMPARE_REVIEWED_SHA256="f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7"
export UNT_SEAL_COMPARE_SELECTION_PATH="/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14/SELECTED_R14_CX1V002.json"
export UNT_SEAL_COMPARE_SELECTION_SHA256="6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a"
export UNT_SEAL_DISPOSITIONS_PATH="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json"
export UNT_SEAL_DISPOSITIONS_SHA256="6a3fa5353e575fbfe617aa497abd4752e8a2c8676d19f6c4c16a69dfeac0c9fe"
export UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH="/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4/KEY_EQUIVALENCE_MAP_V007.json"
export UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256="72a21888eda617638df38ddd64a0e7981bfb6842a9f7f17b8c1a7d4b93e50ec4"
export UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_PATH="/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cascade_map_r5_addendum_cx3/CASCADE_MAP_R5_ADDENDUM_CX3V001.json"
export UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_SHA256="86c897304ec5a0971c3ad1552a60cfad90fc3ac809d68fdacee2be1b942caf9e"
export UNT_SEAL_C5H_RUN_DIR="/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext/KMAX_A2F10_C5H_RUN_V001"
export UNT_SEAL_MIN_FREE_GIB=300
export UNT_SEAL_ROOT_ACK="RI-28,RI-29,RI-30,RI-31,RI-32,RI-33,RI-34,RI-35,RI-36,RI-37,GAP-12"
# optional: export UNT_SEAL_ATTEMPT=1    (1-9; default 1; n > 1: a fresh seal folder and bound names)
```

**Do NOT set any of these.** Step 0 refuses each one if it is set at all, even to an empty value:
- `UNT_SEAL_NEW_ITEM_LIST_PATH` / `_SHA256` and `UNT_SEAL_SUCCESSOR_CUSTODY_PATH` / `_SHA256`: the B7 NEW-item list and the custody record are pinned constants.
- `UNT_SEAL_DRIVER_CHECK_RECORD_PATH` / `_SHA256`, `UNT_SEAL_RULING_EPS_NGC` and `UNT_SEAL_RULING_I1T_NGC`: A111 ruled P3 and P4, and the slot draft fixes them.
- There is no disclosures or registry input either: both are pinned constants.

A safe way to clear them, then check the script and run it:

```bash
unset UNT_SEAL_NEW_ITEM_LIST_PATH UNT_SEAL_NEW_ITEM_LIST_SHA256 UNT_SEAL_SUCCESSOR_CUSTODY_PATH UNT_SEAL_SUCCESSOR_CUSTODY_SHA256 \
      UNT_SEAL_DRIVER_CHECK_RECORD_PATH UNT_SEAL_DRIVER_CHECK_RECORD_SHA256 UNT_SEAL_RULING_EPS_NGC UNT_SEAL_RULING_I1T_NGC
shasum -a 256 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/ROOT_SEAL_STEPS_c3v026.sh    # must print b43cc38be5f19c473167d8d57211c54d336d09d58fcfd66f5ca8187ad033c464
/bin/bash /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/ROOT_SEAL_STEPS_c3v026.sh
```

**What step 0 checks on these inputs:**
- `UNT_SEAL_ROOT_ACK` must equal `REQUIRED_ACK` exactly.
- `UNT_SEAL_MIN_FREE_GIB` must be digits only.
- The compare and selection shas must be r14 `f3f9ba7e` and `6b650ece`.
- The dispositions JSON must lie in `$CTRL/V007_SEAL_ASSEMBLY_INPUTS/`.
- `UNT_SEAL_C5H_RUN_DIR` must end in `KMAX_A2F10_C5H_RUN_V001`.
  - Step 9 uses it only as a string: `make-c5h-manifest` and `check-manifest` compare it with the sealed compare's `C5H_REGISTERED_RUN_DIRS`, which contains root's External1 spelling exactly (one of its 2 entries, checked from r14's bytes at render time).
  - Neither the script nor the helper passes it through `path_policy`.

Start the watchdog at the launch: `nohup /bin/bash /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/step2_disk_watch.sh --log /ABS/PATH/STEP2_DISK_WATCH_V007.log > /dev/null 2>&1 &` (A105.3; a convenience, not part of the seal; root chooses the log path).

## C-02 to C-08 (R-05; r6 `seal_record_requirements[13]`), read from the c3v026 bytes and from dry run `060546Z`
| item | c3v026 | step : line (helper subcommand → log) | dry run A / B |
| --- | --- | --- | --- |
| C-02 | checked by c3v026 | step 0 : L437 (`check-tor`, verdict on stderr); step 4a : L661 (`STEP_04A_C02.json`); step 10 : L727 (`STEP_10_C02.json`) | PASS / PASS |
| C-03 | checked by c3v026 | **step 8 : L693** (`gates-provenance` → `STEP_08_C03.json`) | PASS / PASS |
| C-04 | checked by c3v026 | step 3b : L630 (`slot-registry` → `STEP_03B_C04.json`: r14 loader, registry V012, A107 excludes EPS_NGC and I1T_NGC) | PASS / PASS |
| C-05 | checked by c3v026 | step 3 : L606 (`bound-check`, c05 part → `STEP_03_C05_C06.json`) | PASS / PASS |
| C-06 | checked by c3v026 | step 3 : L606 (`bound-check`, c06 part → `STEP_03_C05_C06.json`) | PASS / PASS |
| C-07 | not checked by script | D-05, enforced by seal tools v004 (step 2 : L541 checks the dispositions object, which is related but is not C-07) | n/a (step 2 PASS / PASS) |
| C-08 | not checked by script | root's manual check in V006's `c08_table` (19 rows) and `c08_confirmation`; step 0 : L449 (`check-disclosures`, form only) and step 11 : L748 (R-02, verbatim) do not check its content | n/a (steps 0 and 11 PASS / PASS) |

This agrees, item by item, with V006's row `A106_2_SRR13_CHECK_SPLIT`:
> C-02, C-03, C-04, C-05 and C-06 were checked by the seal script; C-07 is D-05, enforced by seal tools v004; C-08 was checked by hand by root.

Each step function starts at: step 0 L404, step 2 L537, step 3 L577, step 3b L626, step 4a L655, step 8 L679, step 10 L716, step 11 L740.

## Dry run of record: `dry_run_20261019T060546Z` (setup `c3v010_prestage/tools/setup_dry_run_c3sa_c3v019.sh` `893de27a`, generator c3v013 `379afda7`)
- **Both passes: ALL STEPS PASS**, 32 PASS lines each.
  - Step 11 R-02 passes on V006 in both passes.
  - `fence_refused` is 0 at steps 2a, 3b and 8.
  - The pycache prefix stayed empty, and the scratch output root is a real, empty directory.
- **No stand-in.**
  - The RUN files carry root's answered inputs, labelled as such: P5 `6a3fa535` (copied byte-identically into scratch, since S09 moves that folder), r14 and its selection, the key map, P7, the P8 External1 string, the P9 ack and the P10 floor 300.
  - The dry-run scripts pin V012, V006, draft c3v007, COMPLETE and the custody record.
- **Only the published scratch substitutions** were applied: S01 to S06, S09 to S14, S17, S18, the step-9 stub S15 and the D-10 allowance S16/S16b; pass B adds S23 (no dispositions to the tools).
- The first c3v026 dry run, `dry_run_20261019T060249Z` (setup c3v018), also passed both passes. It still carried the old /Users C5H string and STAND-IN labels; it is kept and superseded.

## Controls (helper c3v019 / script c3v026 / dry run 060546Z; run tag 20261019T060933Z)
| suite | tool (sha) | result file (sha) | result |
| --- | --- | --- | --- |
| r14 + B7 + supersession (r13 and CX1V001 refused; PENDING placeholders; draft compare slot; IMPL r14; B7 pins; stale B7 env; V002-V005 and the V010/V011 drafts and REGISTRY refused) | `c3v010_prestage/tools/mustfail_r14_c3v026_c3sa_c3v004.py` (`f36dd728`) | `mustfail_r14_20261019T060933Z/MUSTFAIL_R14_C3V024_RESULTS_C3SA.json` (`56c13288`) | **21/21** |
| per-site && suite (one MUST_FAIL per site on a copy of the PRODUCTION c3v026; the same fixtures on c3v016) | `c3v010_prestage/tools/e1_sites_mustfail_c3v006.py` (`2655de0a`) | `e1_sites_c3v026_20261019T060933Z/E1_SITES_RESULTS_C3SA.json` (`ae18a7c4`) | **12/12 refuse; defect reproduced on c3v016 9/9; S02 control: no defect** |
| disclosures + step 0 + SA-C3-E1 (target pins V006) | `c3v010_prestage/tools/mustfail_disclosures_c3sa_c3v007.py` (`fcec6d45`) | `mustfail_disclosures_20261019T060933Z/MUSTFAIL_DISCLOSURES_RESULTS_C3SA.json` (`20b3a596`) | **60/60** |
| R-02 + A112 (written SEAL_RECORD; V001-V005 records, pins and tool-4 inputs refused at step 0 or step 11) | `c3v010_prestage/tools/mustfail_r02_a112_c3sa_c3v005.py` (`1b80ccae`) | `mustfail_r02a112_20261019T060933Z/MUSTFAIL_R02_A112_RESULTS_C3SA.json` (`ee5791f2`) | **35/35** |
| A + C-02 to C-06 + SELECTED roles + C03-S1 + C-04 (registry V012, r14 loader) | `c3v010_prestage/tools/mustfail_c0x_c3sa_c3v008.py` (`4d32581d`) | `mustfail_c0x_20261019T060933Z/MUSTFAIL_C0X_RESULTS_C3SA.json` (`6e414dca`) | **85/85** |
| v004 tools | `c3v010_prestage/tools/mustfail_v004_c3sa_c3v002.py` (`96b9a0e2`) | `mustfail_v004_20261019T060933Z/MUSTFAIL_V004_RESULTS_C3SA.json` (`1aa1a52c`) | **17/17** |
| tool-4 imports / RUN FORM / CLI on the real v004 bytes (check c3v003) | `c3v009_prestage/tools/check_tool4_imports_c3v003.py` (`272d9cf5`) | `CHECK_TOOL4_IMPORTS_c3v026.json` (`b0f3ab06`) | **PASS** |
| W7-S1 + RP-S1 | `tools/mustfail_w7_rps1_c3sa_c3v001.py` (`09b42265`) | `mustfail_w7rps1_20261019T060933Z/MUSTFAIL_W7_RPS1_RESULTS_C3SA.json` (`d5aedce7`) | **41/41** |
| B1 + B3 | `tools/mustfail_controls_c3sa_c3v002.py` (`93689fde`) | `mustfail_regress_20261019T060933Z/MUSTFAIL_RESULTS_C3SA.json` (`98aa7797`) | **ALL_OK (8 B1 rows, 17 B3 rows)** |
| B2 + N1 | `tools/mustfail_b2_n1_c3sa_c3v003.sh` (`32705967`) | `mustfail_b2n1_20261019T061125Z/B2_N1_RESULTS_C3SA.txt` (`d12ecdd4`) | **ALL_OK** |
| tor_table_bytes (script c3v026) | `tools/test_tor_table_bytes_c3sa_c3v001.sh` (`7ed906a2`) | `tor_table_bytes_test_20261019T061125Z/TOR_TABLE_BYTES_RESULTS_C3SA.txt` (`0cadad55`) | **ALL_OK** |
| watchdog step2_disk_watch.sh (bd0d9bab) | `tools/test_step2_disk_watch_c3sa_c3v001.sh` (`696bfc9b`) | `watchdog_test_20261019T061125Z/WATCHDOG_TEST_RESULTS_C3SA.txt` (`81303806`) | **ALL PASS** |

The r14 suite's result file kept its c3v003 name; its `schema` field reads `C3SA_MUSTFAIL_R14_C3V026_V004`.

## What changed since SELECTED c3v009 (script c3v020)
**The scripts in between were never published.**
- **c3v021, pre-stage (A114/A116):**
  - The reviewed compare is r14, as `SELECTED_R14_CX1V002` stores it.
  - IMPL r14 is pinned, and r13 is refused as superseded.
  - C-04 loads r14's `load_producer_registry`.
  - The draft compare slot is checked against the reviewed compare.
- **c3v022, near-final (0658):**
  - Disclosures V003 and registry V010.
  - The B7 NEW-item list and the custody record became pinned constants, and their env inputs are refused.
- **c3v023 (V010/V003):** stopped by Claude4 0142, an A115 (a) defect in the I4 producer c3v001.
- **c3v024 (0659, 0661 A119):** V011, V004 and the custody record `9ca16b4f`; held over the B7 NEW-44 class (b) issue.
- **c3v025 (0662 A120):** V005; held over the I4 producer c3v002 class (a) defect.
- **c3v026 (0665):**
  - V012, V006 and draft c3v007.
  - The step-0 refusal text names V006.
  - Root's A121 answers are recorded in the comments, and the run summary names V006.
  - Exactly 7 non-comment lines differ from c3v025: the 4 pins, the refusal text and 2 summary strings.
- **Unchanged since c3v009:** helper c3v019, runner, fence, gates manifest, shim and watchdog.

## NOTEs (A115: none is blocking)
- **Registry supersession is enforced by pin, not by a list.**
  - Unlike the disclosures, there is no `REGISTRY_SUPERSEDED_SHAS` list.
  - V010 and V011 cannot enter: `REGISTRY_SHA` is checked from bytes, and the draft is cross-checked against it (N-3c, N-11b, N-11c).
  - A copy of the script pinning V011 together with a V011 draft would pass step 0, but it would not be the selected script's bytes.
- **P8 is a /Volumes spelling.**
  - The tooling uses it as a string only.
  - Step 9 is root's real run, and it hands that string to the sealed compare r14 through the manifest. No dry run executed step 9, so how the compare itself handles the spelling was not exercised here.
- **First input verifier.** `verify_final_inputs_c3v010_c3v001.py` stopped before writing anything because it misread the shape of `producers.I4` (a list). c3v002 is the record.

## Kept, not selected (nothing deleted)
- `ROOT_SEAL_STEPS_c3v021.sh (pre-stage)` `2e39d564`
- `ROOT_SEAL_STEPS_c3v022.sh (near-final)` `b4f71a84`
- `ROOT_SEAL_STEPS_c3v023.sh (V010/V003; Claude4 0142 stop)` `50a87b6b`
- `ROOT_SEAL_STEPS_c3v024.sh (V011/V004; B7 hold)` `c26d847b`
- `ROOT_SEAL_STEPS_c3v025.sh (V011/V005; I4 c3v002 hold)` `22746e21`
- `SLOT_VALUES_DRAFT_c3v004.json` `723a36d1`
- `SLOT_VALUES_DRAFT_c3v005.json` `d6924860`
- `SLOT_VALUES_DRAFT_c3v006.json` `f542e394`
- Dry runs: `c3v010_prestage/dry_run_20261019T035955Z`, `…040145Z` and `…042057Z`; `dry_run_20261019T044217Z` (c3v024); `dry_run_20261019T060249Z` (c3v026, setup c3v018).
- The smoke folder `c3v010_prestage/smoke_gen_20261019T043857Z` (SMOKE ONLY).

## PENDING
- **Nothing in the script.** Root exports the block above at the run.
- 0665 asks Claude4 for the c3v003 delta, then the c3v010 delta (A115 scope). "On two zeros, root runs the seal."
