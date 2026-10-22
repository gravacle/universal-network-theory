# README c3v011: the seal assembly tuple with B0_RO1 and B0_N3 in the gates-only manifest (root A123), Claude3

Written 2026-10-19T06:56:37Z (`date -u`), for root 0667 (A123, `92a1aa78`), which upholds Claude4 0154 (`3b7cc56f`).
- **Supersedes** `README_SEAL_ASSEMBLY_C3_c3v010.md` (`a43c36a7`) and the selection `SELECTED_SEAL_PRESTAGE_C3SA_c3v010.json` (`1f62deb4`).
- **The selection of record** is `SELECTED_SEAL_PRESTAGE_C3SA_c3v011.json`; the full listing is `HASHES_C3SA_c3v010.txt`.
- **The env exports are unchanged** from c3v010. Only the script name and its sha in the run lines change.
- Nothing here launched anything, opened the C5H run, or created the real step-2 output root. Step 9 was stubbed in every dry run and never executed.

## What c3v011 fixes (class (b), and (a); Claude4 0154, root A123)
**The defect.**
- Step 8 ran the sealed compare `--gates-only` on `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` (`e5967bb9`), a registry-V009-era draft with `gates.B0_RO1` and `gates.B0_N3` null.
- E-SEAL1 therefore recorded both as `MISSING` (`GATE_RECORD_MISSING`), although V012 registers their pre-seal records and prereg r6 `seal_record_requirements[0]` puts the RO1 replay's gate output into E-SEAL1.
- c3v010's dry run of record shows it in both passes (`dry_run_20261019T060546Z/pass*/…/GATES_ONLY.json`).
- **I missed it.** I did not compare GATES_ONLY.json against V012's pre-seal set. C-03 (step 8) checks only the slotted gate records, and B0_RO1 and B0_N3 are not slotted, so nothing caught it.

**The fix** (to the letter of A123):
- `MANIFEST_GATES_ONLY_C3SA_c3v002.json` (`46dc5310`) is e5967bb9 with only two values changed:
  - `gates.B0_RO1` = `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ri33_c3/b0_ro1/B0_RO1_RECORD_C3V001.json` (`332452b7`);
  - `gates.B0_N3` = `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ri33_c3/b0_n3/B0_N3_RECORD_C3V001.json` (`dd1dd912`).
  - Both use the absolute form the draft uses for every other gate, and both match V012's `gate_records` from bytes. The diff is those two lines; the note is unchanged.
- `ROOT_SEAL_STEPS_c3v027.sh` changes only the `MANIFEST_GATES` / `MANIFEST_GATES_SHA` pin (L266), plus the header and history comments. No check was added.
- **Things keyed to e5967bb9 were moved with it:**
  - the dry-run generator: c3v014's S10 now matches the target's own manifest line;
  - the dry-run setup: c3v020 derives the gates-only stand-in from the target's manifest pin, and the generator checks it gate for gate (only `identity_runs` is emptied);
  - a documentation-only successor, `SLOT_XREF_C3SA_c3v002.json` (`ef77df63`). The script and helper never read SLOT_XREF.

## E-SEAL1 gates-only, gate by gate, from the bytes of dry run `064733Z`
The two GATES_ONLY.json files: pass A `310d3200`, pass B `e29b169e`.

| gate | V012 gate_records | manifest c3v002 entry | pass A | pass B | record sha (A = B) |
| --- | --- | --- | --- | --- | --- |
| B0 | pre-seal record c2cec35b | `seal_records_c4/build/records/B0_R5_RECORD_C4V001.json` | PASS | PASS | c2cec35b |
| B0_FA | pre-seal record 888488cd | `seal_records_c4/build/records/B0_FA_R5_RECORD_C4V001.json` | PASS | PASS | 888488cd |
| B0_N3 | pre-seal record dd1dd912 | `ri33_c3/b0_n3/B0_N3_RECORD_C3V001.json` | PASS | PASS | dd1dd912 |
| B0_RO1 | pre-seal record 332452b7 | `ri33_c3/b0_ro1/B0_RO1_RECORD_C3V001.json` | PASS | PASS | 332452b7 |
| B0prime_DRY | pre-seal record 7842d2a7 | `seal_records_c4/build/records/B0prime_DRY_R5_RECORD_C4V001.json` | PASS | PASS | 7842d2a7 |
| B0prime_RERUN | pre-seal record e33af53d | `tail_scheme_impl_c2/gates_v007/r2/records/R5_V001/B0prime_RERUN_R5_C2V007.json` | PASS | PASS | e33af53d |
| B1 | pre-seal record 83e7b067 | `tail_scheme_impl_c2/gates_v007/r2/records/R5_V001/B1_R5_C2V007.json` | PASS | PASS | 83e7b067 |
| B1_OFF | pre-seal record 3b9ad402 | `tail_scheme_impl_c2/gates_v007/r2/records/R5_V001/B1_OFF_R5_C2V007.json` | PASS | PASS | 3b9ad402 |
| B2 | pre-seal record 915fbcda | `gate_b2_c3/out/B2_GATE_RECORD_C3V003.json` | PASS | PASS | 915fbcda |
| B3 | pre-seal record 83c853b9 | `seal_records_c4/build/records/B3_RECORD_C4V001.json` | PASS | PASS | 83c853b9 |
| DOUBLING | pre-seal record ea48ac2b | `producer_registry_c3/out/DOUBLING_MERGED_C3V001.json` | PASS | PASS | ea48ac2b |
| EA | PRODUCED_AFTER_THE_SEAL | null | MISSING (`GATE_RECORD_MISSING:EA`) | MISSING | (none) |
| EPS | pre-seal record 598c8fa3 | `tail_scheme_impl_c2/certificates_v002/gates/EPS_CERT_V006.json` | PASS | PASS | 598c8fa3 |
| FLAG_RULINGS | PRODUCED_AFTER_THE_SEAL | null | MISSING (`GATE_RECORD_MISSING:FLAG_RULINGS`) | MISSING | (none) |
| GQ | pre-seal record 5a1b39f8 | `producer_registry_c3/out/GQ_CERT_V006.json` | PASS | PASS | 5a1b39f8 |
| HARMONICS | PRODUCED_AFTER_THE_SEAL | null | MISSING (`GATE_RECORD_MISSING:HARMONICS`) | MISSING | (none) |
| I1T | PRODUCED_AFTER_THE_SEAL | null | MISSING (`GATE_RECORD_MISSING:I1T`) | MISSING | (none) |
| I4 | PRODUCED_AFTER_THE_SEAL | null | MISSING (`GATE_RECORD_MISSING:I4`) | MISSING | (none) |
| LO | pre-seal record 1c384f76 | `tail_scheme_impl_c2/certificates_v004/gates/LO_CERT_V004_MS128.json` | PASS | PASS | 1c384f76 |
| LO_NGC | pre-seal record 33bc2190 | `tail_scheme_impl_c2/certificates_v002/gates/LO_NGC_CERT_V002.json` | PASS | PASS | 33bc2190 |
| MT | PRODUCED_AFTER_THE_SEAL | null | MISSING (`GATE_RECORD_MISSING:MT`) | MISSING | (none) |
| RB_FP | PRODUCED_AFTER_THE_SEAL | null | MISSING (`GATE_RECORD_MISSING:RB_FP`) | MISSING | (none) |
| SRB_ROT | PRODUCED_AFTER_THE_SEAL | null | MISSING (`GATE_RECORD_MISSING:SRB_ROT`) | MISSING | (none) |
| SR_K | PRODUCED_AFTER_THE_SEAL | null | MISSING (`GATE_RECORD_MISSING:SR_K`) | MISSING | (none) |
| T2I | PRODUCED_AFTER_THE_SEAL | null | MISSING (`GATE_RECORD_MISSING:T2I`) | MISSING | (none) |

**Result.**
- **15 PASS:** every pre-seal gate V012 registers, each with its registered record sha.
- **10 MISSING:** exactly the PRODUCED_AFTER_THE_SEAL gates (EA, FLAG_RULINGS, HARMONICS, I1T, I4, MT, RB_FP, SRB_ROT, SR_K, T2I), each with only `GATE_RECORD_MISSING:<gate>`.
- **Against c3v010's dry run, only B0_N3 and B0_RO1 changed**, MISSING to PASS, in both passes.
- The table tool `c3v010_prestage/tools/gates_only_table_c3v001.py` (`72248a64`) writes `c3v011_prestage/GATES_ONLY_TABLE_c3v027_064733Z.json` (`920926b7`) and `.md` (`4e12b1dc`).

## Pre-publication check (A123: a stand-alone check, not a script step)
`c3v010_prestage/tools/check_manifest_gates_vs_registry_c3v001.py` (`f92a4e03`) reads, from bytes:
- every gate V012 registers with record shas must be named in the manifest by a path whose bytes hash to one of those shas;
- every PRODUCED_AFTER_THE_SEAL gate must be null;
- the gate key sets must be equal.

**Results:**
- **On manifest c3v002: PASS**, with 15 pre-seal gates and 10 PRODUCED_AFTER_THE_SEAL gates (`c3v011_prestage/CHECK_MANIFEST_GATES_VS_V012_c3v002.json` `96640253`).
- **Its MUST_FAILs, on synthetic copies: 16/16** (`9be9aa53`). Among them:
  - the superseded draft e5967bb9, refused for both B0_RO1 and B0_N3;
  - B0_RO1 alone null, and B0_N3 alone null;
  - another pre-seal gate null, and I4 named by a path;
  - a wrong record, a missing or extra key, an empty registry slot, a non-path, a wrong sha, a symlink and an unknown form.

## The tuple
| role | file | sha256 |
| --- | --- | --- |
| script | `ROOT_SEAL_STEPS_c3v027.sh` (89551 bytes) | 239a51c34439b9510155762db8ba02709f1a478b3601de371799ec78591df02f |
| **step-8 gates-only manifest (new)** | `MANIFEST_GATES_ONLY_C3SA_c3v002.json` | 46dc53104d518edc9b00e77c0b4995df3e4871999c7264926dad186726ed62ca |
| helper (unchanged) | `tools/seal_steps_c3sa_c3v019.py` | 91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf |
| runner / fence (unchanged) | `tools/run_pinned_c3sa_c3v003.py` / `tools/fence_c3sa_c3v003.py` | 2b040e94… / 9c62ad49… |
| slot draft (unchanged) | `c3v010_prestage/SLOT_VALUES_DRAFT_c3v007.json` | 184ff5cbc01eb2683ace5cee8fbee1e82b38d7d6ac152726713501c1ddc83729 |

The watchdog `step2_disk_watch.sh` (`bd0d9bab…`) is unchanged and stays outside the hash chain.

## Pinned inputs (unchanged from c3v010)
| input | sha256 |
| --- | --- |
| `producer_registry_c3/out/PRODUCER_REGISTRY_C3V012.json` | 4b8a3c35ca9a140bdb9e132f564d2163704e915aa67840c71c36fea551cafafa |
| `seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V006.json` | 8dc28480a588f3ef7bd47ebe673767ac79745178a36141cdf50e69e8a040872a |
| `seal_b7_inputs_c4/NEW_ITEM_DISPOSITIONS_V007_COMPLETE.json` | 68164144b2f9bf56626be65663566e8c51afba65382e3b6789f53eb144252cd2 |
| `$CTRL/V007_SEAL_ASSEMBLY_INPUTS/custody_run_v002/RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json` | 9ca16b4fd07fd470359cb604526e38807ecf50093cf59ad7895441601535f67d |
| `v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py` | f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7 |
| `v007_compare_c2/r14/SELECTED_R14_CX1V002.json` | 6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a |
| `v007_compare_c2/r14/COMPARE_V007_IMPL_R14_CX1V002.md` | 2ba6d12ecc36ab444365348573b7f49a02a12a818dd15d67de35d77300fa17c9 |
| `v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json` | d28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9 |
| `v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json` | 7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0 |
| `v007_final_prereg_c4/seal_tools_v004/SELECTED_SEAL_TOOLS_V004_C4V001.json` | 593c59faf39074b14579f927ae17c5aeda1f7450ee4a9f264f96a1f2c7b195e0 |

V012 is validated on r14 (`a7c80f8e`). V006 passes `check-disclosures`; its content is not cross-checked against the A-entries here.

**Superseded and refused**
- **Disclosures** V001 `b9db6fd1`; V002 `a0284ece`; V003 `990be628`; V004 `adac5030`; V005 `b1a7b3d5`.
  - Step 0 refuses each one, naming V006 as the file of record.
- **Registries** V010 `b8435877`; V011 `512a7171`.
  - Neither is pinned, and step 0 refuses a draft that is not on V012.
- **Gates-only manifest** e5967bb9: no longer pinned. The pre-publication checker refuses it (MG-1, MG-1b).
- **Compares:** r13 and older rounds, and `SELECTED_R14_CX1V001`, are refused in step 0.

## Root's invocation: the env block (unchanged from c3v010; 0664 A121, 0659, 0665)
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

**Do NOT set any of these.** Step 0 refuses each one if it is set at all, even to an empty value: `UNT_SEAL_NEW_ITEM_LIST_PATH` / `_SHA256`, `UNT_SEAL_SUCCESSOR_CUSTODY_PATH` / `_SHA256`, `UNT_SEAL_DRIVER_CHECK_RECORD_PATH` / `_SHA256`, `UNT_SEAL_RULING_EPS_NGC` and `UNT_SEAL_RULING_I1T_NGC`. There is no disclosures, registry or manifest input; all three are pinned constants.

Clear them, check the script and run it (the script name and sha are the only change):

```bash
unset UNT_SEAL_NEW_ITEM_LIST_PATH UNT_SEAL_NEW_ITEM_LIST_SHA256 UNT_SEAL_SUCCESSOR_CUSTODY_PATH UNT_SEAL_SUCCESSOR_CUSTODY_SHA256 \
      UNT_SEAL_DRIVER_CHECK_RECORD_PATH UNT_SEAL_DRIVER_CHECK_RECORD_SHA256 UNT_SEAL_RULING_EPS_NGC UNT_SEAL_RULING_I1T_NGC
shasum -a 256 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/ROOT_SEAL_STEPS_c3v027.sh    # must print 239a51c34439b9510155762db8ba02709f1a478b3601de371799ec78591df02f
/bin/bash /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/ROOT_SEAL_STEPS_c3v027.sh
```

**P8.** `UNT_SEAL_C5H_RUN_DIR` is root's External1 spelling. It is exactly one of the 2 entries in r14's `C5H_REGISTERED_RUN_DIRS`, checked from bytes at render time. Step 0 checks only its suffix, and step 9 compares it as a string.

Start the watchdog at the launch: `nohup /bin/bash /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/step2_disk_watch.sh --log /ABS/PATH/STEP2_DISK_WATCH_V007.log > /dev/null 2>&1 &` (A105.3; a convenience, not part of the seal; root chooses the log path).

## C-02 to C-08 (R-05), read from the c3v027 bytes and from dry run `064733Z`
| item | c3v027 | step : line | dry run A / B |
| --- | --- | --- | --- |
| C-02 | checked | step 0 : L445 (`check-tor`); step 4a : L669; step 10 : L735 | PASS / PASS; PASS / PASS; PASS / PASS |
| C-03 | checked | **step 8 : L701** (`gates-provenance`; slotted gate records only) | PASS / PASS |
| C-04 | checked | step 3b : L638 (`slot-registry`: r14 loader, registry V012) | PASS / PASS |
| C-05 / C-06 | checked | step 3 : L614 (`bound-check`) | PASS / PASS |
| C-07 | not by script | D-05, enforced by seal tools v004 (step 2 : L549 checks the dispositions object) | PASS / PASS |
| C-08 | not by script | root's manual check in V006's `c08_table`; step 0 : L457 and step 11 : L756 check only the file's form and that the record carries it verbatim | PASS / PASS; PASS / PASS |

This agrees with V006's row `A106_2_SRR13_CHECK_SPLIT`.
- The step functions start at: step 0 L412, step 2 L545, step 3 L585, step 3b L634, step 4a L663, step 8 L687, step 10 L724, step 11 L748.
- Step 8's manifest check is at L690.

## Dry run of record: `dry_run_20261019T064733Z` (setup c3v020 `cd406258`, generator c3v014 `b49181e2`)
- **Both passes: ALL STEPS PASS**, 32 PASS lines each.
  - Step 11 R-02 passes on V006 in both passes.
  - `fence_refused` is 0, and the scratch output root is empty.
- **The RUN files carry root's answered inputs** (P5, P7, P8 as a string, P9, P10).
- **The gates-only stand-in** (S10, `6dba5a1c`) is manifest c3v002 with only `identity_runs` emptied, so the dry run evaluates exactly the seal's gate records.
- Only the published scratch substitutions were applied: S01 to S06, S09 to S18, S15, S16/S16b, and S23 in pass B.

## Controls (helper c3v019 / script c3v027 / dry run 064733Z; run tag 20261019T065046Z)
| suite | tool (sha) | result file (sha) | result |
| --- | --- | --- | --- |
| r14 + B7 + supersession | `c3v010_prestage/tools/mustfail_r14_c3v026_c3sa_c3v004.py` (`f36dd728`) | `mustfail_r14_20261019T065046Z/MUSTFAIL_R14_C3V024_RESULTS_C3SA.json` (`7352cde4`) | **21/21** |
| per-site && suite (one MUST_FAIL per site on a copy of the PRODUCTION c3v027; the same fixtures on c3v016) | `c3v010_prestage/tools/e1_sites_mustfail_c3v007.py` (`8cbf0632`) | `e1_sites_c3v027_20261019T065046Z/E1_SITES_RESULTS_C3SA.json` (`4331c432`) | **12/12 refuse; defect reproduced on c3v016 9/9; S02 control: no defect** |
| disclosures + step 0 + SA-C3-E1 | `c3v010_prestage/tools/mustfail_disclosures_c3sa_c3v007.py` (`fcec6d45`) | `mustfail_disclosures_20261019T065046Z/MUSTFAIL_DISCLOSURES_RESULTS_C3SA.json` (`27fddaba`) | **60/60** |
| R-02 + A112 (V001-V005 refused at step 0 or step 11) | `c3v010_prestage/tools/mustfail_r02_a112_c3sa_c3v006.py` (`45b3ac9e`) | `mustfail_r02a112_20261019T065046Z/MUSTFAIL_R02_A112_RESULTS_C3SA.json` (`a59e7a18`) | **35/35** |
| A + C-02 to C-06 + SELECTED roles + C03-S1 + C-04 (registry V012, r14 loader) | `c3v010_prestage/tools/mustfail_c0x_c3sa_c3v008.py` (`4d32581d`) | `mustfail_c0x_20261019T065046Z/MUSTFAIL_C0X_RESULTS_C3SA.json` (`1ce9bcdd`) | **85/85** |
| v004 tools | `c3v010_prestage/tools/mustfail_v004_c3sa_c3v002.py` (`96b9a0e2`) | `mustfail_v004_20261019T065046Z/MUSTFAIL_V004_RESULTS_C3SA.json` (`0043ca09`) | **17/17** |
| tool-4 imports / RUN FORM / CLI on the real v004 bytes (check c3v003) | `c3v009_prestage/tools/check_tool4_imports_c3v003.py` (`272d9cf5`) | `CHECK_TOOL4_IMPORTS_c3v027.json` (`390baf82`) | **PASS** |
| W7-S1 + RP-S1 | `tools/mustfail_w7_rps1_c3sa_c3v001.py` (`09b42265`) | `mustfail_w7rps1_20261019T065046Z/MUSTFAIL_W7_RPS1_RESULTS_C3SA.json` (`39567220`) | **41/41** |
| B1 + B3 | `tools/mustfail_controls_c3sa_c3v002.py` (`93689fde`) | `mustfail_regress_20261019T065046Z/MUSTFAIL_RESULTS_C3SA.json` (`221293a3`) | **ALL_OK (8 B1 rows, 17 B3 rows)** |
| B2 + N1 | `tools/mustfail_b2_n1_c3sa_c3v003.sh` (`32705967`) | `mustfail_b2n1_20261019T065307Z/B2_N1_RESULTS_C3SA.txt` (`a0b765d8`) | **ALL_OK** |
| tor_table_bytes (script c3v027) | `tools/test_tor_table_bytes_c3sa_c3v001.sh` (`7ed906a2`) | `tor_table_bytes_test_20261019T065308Z/TOR_TABLE_BYTES_RESULTS_C3SA.txt` (`577f95e9`) | **ALL_OK** |
| watchdog step2_disk_watch.sh (bd0d9bab) | `tools/test_step2_disk_watch_c3sa_c3v001.sh` (`696bfc9b`) | `watchdog_test_20261019T065308Z/WATCHDOG_TEST_RESULTS_C3SA.txt` (`abc34cb0`) | **ALL PASS** |
| NEW (A123): the manifest-vs-registry checker on synthetic copies | `c3v010_prestage/tools/mustfail_manifest_gates_check_c3v001.py` (`006f3ea9`) | `c3v011_prestage/mustfail_manifest_gates_20261019T064537Z/MUSTFAIL_MANIFEST_GATES_CHECK_RESULTS_C3SA.json` (`9be9aa53`) | **16/16** |

## NOTEs (A115: none is blocking)
- **The manifest's note is stale.** It still reads "registry V009 … null = not built (B0_N3, B0_RO1, I4: fail closed)", because A123 allows only the two gate values to change. Its gates are what step 8 uses, and they are correct.
- **C-03 checks only slotted gate records**, so the script would still not catch a pre-seal gate left null in a future manifest. Per A123 that guard is the pre-publication checker above, not a script step.
- **Carried from c3v010:**
  - registry supersession is by pin, not by a list;
  - P8 is a /Volumes spelling, used as a string only;
  - the r14 suite's result file kept its c3v003 name.

## Kept, not selected (nothing deleted)
- `ROOT_SEAL_STEPS_c3v026.sh` `b43cc38b` (SELECTED c3v010, superseded); c3v021 to c3v025 as listed in README c3v010.
- `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` `e5967bb9`; `SLOT_XREF_C3SA.json` `4bd214a8`.
- c3v010's dry run `dry_run_20261019T060546Z` (it shows the defect) and the earlier ones.

## PENDING
- **Nothing in the script.** Root exports the block above at the run.
- Per 0667, Claude4 does the c3v011 delta (A115 scope). "On two zeros, root runs the seal."
