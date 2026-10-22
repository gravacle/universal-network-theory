# COMPARE_V007_IMPL_R10: the V007 tail-scheme compare, R10 (Claude2 root lane)

`claude_artifacts/v007_compare_c2/r10/`, 2026-10-18 (about 16:05Z to 17:10Z). It succeeds `r8/kmax_tail_compare_c2v007_r8.py` (bd51db15). The stopped r9 is superseded and unused (A72); it was not read. At the start, 114 of the 115 r8 `HASHES.txt` entries verified from bytes; the one that did not is the open V005 addendum, which had moved (expected). No earlier round was written to. All writes went to `r10/`. R10 is not sealed, and every sha is in `HASHES.txt`, computed from bytes.

## Status

**Binding text.**
- The V004 addendum, 487d4449 (A46): frozen, and verified at every start.
- The open V005 addendum. **A67, A68 CHK-1, A69, A71 and A72 govern this round.**
  - Its sha moved during the round: b4f72035 at the start, ef754025 at about 16:49Z, and the end value is in `HASHES.txt`.
  - The text added mid-round is A73 to A77. A73 F2, A75 (Claude3 0067, the must-guard list for "the final compare round") and A77.2 (the RO1 role table) were read and implemented in this round. They are marked "read mid-round" below.
  - A78 (the launch packet V004 review, read at the end) rules no compare item. The C4-S1 binding of the plan's driver to the seal's driver concerns the packet; the compare's side of that binding is the A72 BUILD pin.
- **Seal-time pins stay None:** `PIN_ADDENDUM_V005`, `PIN_V010_R5_CHECK`, `PIN_PRODUCER_REGISTRY`, the new **`PIN_DRIVER_BUILD_RECORD`** (A72), and `V007_PREREG_SHA256`. Sealed mode refuses while any of them is None (TESTED).

**TESTED** (every run was under the OS sandbox `tools/sandbox_r10.sb` plus the audit-hook guard `tools/guard_r10.py`; 0 refused events, and no subprocess named the registered run):

| Run | Result |
|---|---|
| Suite (`out/tests_R10/`) | **646/646**, compare e801adc4, tests cc9f1bb8, 53 s. 20 subprocesses, all CLI calls of the compare. The regenerated FIELDS equals `FIELDS_R10.md` byte for byte, and so does the in-suite R10 check copy. The stdout equals the trial t9 run's byte for byte. |
| Real-record check (`out/REAL_RECORD_CHECK_R10.json`) | **63/63** expectations: the 55 carried from r8, plus 8 new. Tool `tools/real_record_check_c2v007_r10.py`. |
| Mutation check (`out/MUTATION_R10_RECORD/MUTATION_R10.json`) | **54/54**: 24 carried r7/r8 checks, plus 15 R10 fixes, each reverted to its r8 behaviour and then restored (30). |
| Tail-library probe (`out/UVLIB_PROBE_R10.stdout.txt`) | 10/10. Library v001 equals v002 `normalize_config` on every real P128 MS128 template. |

**Suite composition (by name, against the r8 TEST_SUMMARY):**
- **549** r8 tests are carried. None changed its pass, outcome, expected outcome or subtype.
  - 14 of them gain additive codes in `reasons` (A68 CHK-1, A69.2, A75 GQ reach, and the AMB-07 basis text). In each case the reading is unchanged.
- **1** was renamed, because its premise changed (NEW-52 / A75.7): `R8_A67_N2_PRODUCED_AFTER_THE_SEAL_TOKEN_BINDS_BY_PRODUCER_ONLY_ADOPT` became `R10_A67_N2_PRODUCED_AFTER_THE_SEAL_TOKEN_BINDS_THE_POST_SEAL_GATES_BY_PRODUCER_ONLY_ADOPT`.
- **96** are new, in `r10_tests`.

**Fixture changes the suite needs (premises R10 changes; no expectation was edited):**
- The TEST registry is schema **C2V003**.
  - Producers, the identity comparator and the token sets are `{path, sha256}` pins of real files: `tools/fixture_producers/*.fixture`. The bytes of each file are exactly the r8 fixture string, so every r8 fixture sha is now the sha of a file.
  - The `PRODUCED_AFTER_THE_SEAL` token stays only on the post-seal gates.
  - `run_eval`, `eval_record`, `EG` and `cli()` register the records they evaluate, by sha, as `run_eval` already did in r8.
- Every DDO GQ roster carries `kept` and `outer`.
- One r6 test called `_pass_rows` on a duplicate world to show the r5 last-wins reading. It now rebuilds that reading locally, because R10's `_pass_rows` refuses the duplicate itself.

**Hygiene.**
- Nothing under the registered C5H run, `runs_ext/UVT_*` or the KMAX_A2F10_C5H_RUN_V001 outputs was opened or listed. The sandbox denies reads there and on `/.vol`. The only access is `os.stat` of the registered directory itself, for its (st_dev, st_ino).
- No NGC velocity was read. Nothing was launched, deleted, moved or renamed.
- The in-progress `driver_r6/` tree was read only: bytes hashed, and the cascade map parsed. That probe is reported, not an expectation.

## Items implemented

| Item | Implementation | Tests (suite unless noted) |
|---|---|---|
| **A67, all items** | Carried unchanged: SF1, SF2, N1, N2, N3, N4, NEW-31, the float floor (UNTESTED; no floor in the code), order N1, and the seal-time pins. Under an r6 build, N1 reads the active build's driver (A72). | The carried `R8_A67_*` tests, plus one `R10_A67_<item>_CARRIED_TESTS_PASS` per item (10); mutation `A67_*` (12). |
| **A68 CHK-1** | `registered_gas_M_s(ctx)` reads the case block's C4T uv_tail `gas.M_s`. `gas_M_s_context_codes` makes LO, GQ and DOUBLING a RECORD_DEFECT when that value is unreadable or is not the A57 value 128, so a direct gate call in an M_s 64 context refuses.<br>**LO:** `source_gas_M_s` must equal the registered value.<br>**GQ:** every DDO roster's M_s, and a top-level `gas_M_s_DDO` or `source_gas_M_s` when present, must equal it.<br>**DOUBLING:** `ddo_gas_M_s` must equal it.<br>**A68 Records / A73 F2:** LO's `gas_M_s`, `tail_config_gas/M_s` and `build/roster_gas/M_s` must each equal `source_gas_M_s` when present. | `R10_A68_CHK1_*` (7), `R10_A68_RECORDS_*` (2); Codex2 `lo_direct_gate_context_ms64` and `lo_ms64` fixtures; real-record `R10_A68_CHK1_*` (2); mutation `R10_A68_CHK1_*`. |
| **A69 note 1** | Registry schema **C2V003**.<br>- producers, identity_comparators and identity_tokens are lists of `{path, sha256}`.<br>- `producer_registry_from_obj` hashes every pinned file from bytes at load. A missing file, a wrong sha, a relative path or an r8-form sha string REFUSES the registry.<br>- `file_pin_codes` requires the record's producer path (by realpath) **and** sha to be a registered pin of its gate, and re-hashes the file at every gate read (`PRODUCER_PATH_NOT_ROOT_REGISTERED_A69_1`, `PRODUCER_BYTES_NOT_THE_REGISTERED_SHA_A69_1`). Stricter, DECLARED: the identity comparator and token files are bound the same way. | `R10_A69_1_*` (4); Codex2 `b2_missing_producer_path`; real-record `R10_A69_1_*`; mutation `R10_A69_1_*`. |
| **A69 note 2** | `RB_FP_SHELL_BELOW_K_A69_2` is named on its own, alongside the A67 N3 EXCEED code. Stricter, DECLARED: an LO shell below K = 4 is `LO_SHELL_BELOW_K_A69_2`. | `R10_A69_2_*` (2). |
| **A69 note 3** | `rpair_branch_row(und, ratio, ids)`: the largest ratio, and on an exact tie the **lowest row index** in row_ids order, whatever the input order. | `R10_A69_3_*` (2, including an exact all-row tie through `pair_noise`); mutation `R10_A69_3_*`. |
| **A71** | Every list-to-mapping site goes through `unique_map` / `unique_keys_codes`, and every JSON parse goes through `_hook_factory` (object_pairs_hook). A duplicate is refused **before** the mapping is built, and the refusal names both entries by index: `DUPLICATE_ENTRY_A71:<where>:<list>[i]:<list>[j]`, or `DUPLICATE_JSON_KEY_A71:object[n]:members[i]:members[j]`. No record label is emitted (A54 S6).<br>Where the duplicate lands:<br>- gate records: RECORD_DEFECT (`DuplicateEntry` is caught in `evaluate_gate`);<br>- runs: a read code, and the run is invalid;<br>- case block, registry, build record or pinned input: a refusal. | The audit table below: one test per site. |
| **Codex2 0442 B1** | `_shells` reads and type-checks every raw entry. A range given twice is a RECORD_DEFECT naming both entries, so LO, LO_NGC and the LO extended shells are all covered. | `R10_A71_CX2_B1_*` (4); all 15 Codex2 binding fixtures read as their text requires (`R10_CX2_R8_BINDING_FIXTURES_*`), plus the 12 RB_FP fixtures; mutation. |
| **Codex2 0442 S1** | `Refused` carries a fixed `refusal_code`. In `--validity-only` and `--gates-only`, `refusal_text` prints the code only, and `main` prints `REFUSED: INTERNAL_EXCEPTION:<type>` with no traceback for any other exception. Every one of the 13 Claude3 S1 sites (A75.5) raises with a code. Full mode keeps the r8 detail. | `R10_CX2_S1_*` (2: 3 inputs × 2 blinded modes + an internal exception, against the canary `v_73.246813579`; plus the formatter); mutation `R10_CX2_S1_*`. |
| **Claude3 0065 H-07** | `c5h_path_hit` now also refuses:<br>- a `/.vol` path, and any path whose realpath is one (string test, no stat);<br>- any path an ancestor of which **is** a registered run directory by (st_dev, st_ino). The walk is top-down, so a firmlink or second spelling is caught before anything inside is stat'ed;<br>- a regular file with `st_nlink > 1` on the registered run's device (a possible hard link).<br>The run directory is never listed (DECLARED, NEW-64). `read_run`, `c5h_interlock` and the audit-hook guard all use it. The guard and sandbox deny `/.vol` too. | `R10_H07_*` (9 cases on a stand-in directory, including an alias that only identity catches, plus the interlock); real-record `R10_H07_*` (the real directory's one identity, and its /.vol spellings refused without a stat); mutation `R10_H07_*`. |
| **A72** | The custody pins are a **seal-time PIN set**: `PIN_DRIVER_BUILD_RECORD` (None until the seal) names a BUILD record (schema `UNT_V007_SEALED_DRIVER_BUILD_C2V001`) with build r5 or r6. Anything else is refused (`driver_build_codes`).<br>**r5** must equal the A62.3 pins exactly.<br>**r6** must be the pin-only image of r5:<br>- predecessor r5 with the r5 shas;<br>- binding 86af6198 unchanged;<br>- a new `galaxy_m0_forward_c2v010.py`;<br>- every file under `driver_r6/`, or the unchanged r5 file;<br>- the cascade map maps each changed r5 sha to its r6 image and remaps nothing else;<br>- every sha from bytes;<br>- no two pins share a sha.<br>The active build supplies every T-case `drivers_allowed`, the I4 driver, the N1 identity driver (code `..._R6_A67_N1_A72` under r6) and the RO1 / nodes custody lists.<br>Test mode: `--test-driver-build-record`, or the built-in r5 set (the r8 behaviour). Sealed mode refuses without the pin or without the build's `check_record`. | `R10_A72_*` (5: r5 default; an r5 record through the CLI; 5 malformed records refused; a synthetic r6 accepted and made the custody set; 7 non-image r6 records refused; sealed refusals); real-record `R10_A72_*` (and, reported only: the in-progress `driver_r6` bytes form an r6 build that passes the r6 rule); mutation `R10_A72_*`. |
| **NEW-52** (r8 recheck validity N1, order N2; Claude3 P-N2; A75.7, read mid-round) | The token is accepted only on `GATE_RECORD_AFTER_SEAL_ALLOWED` = SRB_ROT, RB_FP, T2I, EA, MT, I1T, FLAG_RULINGS, HARMONICS (the gates whose inputs are V007 run outputs). It is refused at load for every other gate, SR_K included (A67 N2). A hand-built registry carrying it elsewhere fails closed at the gate (`GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52`). | `R10_NEW52_*` (3); real-record `R10_NEW52_*`; mutation `R10_NEW52_*`. |
| **r8 recheck validity SF1, order N1; Claude3 P-SF1** | `gq_geometry_binding_codes`:<br>- each DDO roster's `geometry` must be the label **derived** from its own `kept` / `outer` blocks: `C<K>T_KB<K_big>`, `S<K>T_SPHERE_KB<K_big>` or `C<K>T-C<K_out>c`;<br>- `kept` must be its roster case's kept node set;<br>- its k range may not reach above the outer edge.<br>Each geometry is named by one roster (A71). Every violation is a RECORD_DEFECT. | `R10_SF1_*` (6: probes S3, S4, S5, P-SF1 and swapped labels on V005 copies; derived = label for all 10 real V005 rosters); real-record `R10_SF1_*`; mutation `R10_SF1_*`. |
| **A75.1 A05** (read mid-round) | A named GQ reach is met by **one** roster that spans from its case's kept K (NGC: 2) to the reach. Same-name rosters are never merged. | `R10_A75_A05_*`. |
| **A75.6** (read mid-round) | The fixed map binds DDO_C2T → C2T_KB<K_big of C2T>, DDO_C3T → C3T_KB<K_big of C3T>, DDO_C4T → C4T_KB<2P>. The named reach is met only by a roster carrying that geometry. When it is absent, the reading is `GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT` (FAIL: V004 keeps its A67 SF2 FAIL reading). A mislabel is a RECORD_DEFECT (the derivation above). | `R10_A75_6_*`; real V005 PASS and V004 FAIL (`R10_REAL_GQ_*`). |
| **A75.2** (read mid-round) | - S01: an interlock marker that is unreadable or has a duplicate key refuses.<br>- B03 to B06: a repeated B0_RO1 case, B0_N3 runtime check, B0prime_DRY file, or DOUBLING K_big value is a RECORD_DEFECT.<br>- A06 / A07: `classify_failure` names a repeated route_a stage record and differing readout-refusal texts.<br>- B12: a repeated CLI option, a repeated `--case` and an abbreviated option are refused (`allow_abbrev=False`).<br>- The pinned C4R3's adapter side files are parsed strictly (T05). | `R10_A75_2_*` (7), `R10_A71_B12_*`, `R10_A71_SITE_T05_S02_*`. |
| **A77.2** (read mid-round) | The existing custody checks already enforce the role table per case family:<br>- DDO cases: fbe9ae79 / 869ce387;<br>- C4T-D5 and its member: nodes 0ae245d8 / a5277172;<br>- binding 86af6198 for both;<br>- serial or parallel from the admitted attempt's column_workers (a Picard member: its base's).<br>Any other worker or binding makes the case or identity run invalid. R10 adds TESTED probes with the r5 NGC worker shas b6c4586d / ee0510df and the NGC binding 52dc4065, all taken from the r5 driver bytes. | `R10_A77_2_*` (3: 7 cross-role probes plus D5 and DDO controls; a full reading; an identity run). |
| **A74.1 class (packet)** | `npy_header_duplicate_key_code`: the AST of each `.npy` header in the field packet is checked, and a repeated header key reads V4/V5 False. | `R10_A71_NPY_HEADER_*`. |
| **Claude3 r7 A-N1** | `pass_rows_gap` leaves a present non-list row-set to S9 only; it is no longer also a B4 gap. | `R10_C3_R7_A_N1_*`; mutation `R10_C3_A_N1_*`. |

## A71 audit: every dict-from-list and JSON-parse site

The site ids are Claude3 helper I's 63-site inventory of r8 (`review_v007_compare_c3/r10_pre/I_a71_audit/SITES_R8_I.json`), plus R10's own (R-). Lines are r10 lines.

| Site | r10 function (line) | Before (r8) | Guard (r10) | Test |
|---|---|---|---|---|
| J / C01 | `_hook_factory` / `loads_strict` (527) | refused, named nothing | refuses before the object is built; names `object[n]:members[i]:members[j]` | `R10_A71_SITE_JSON_OBJECT_PAIRS_HOOK_NAMES_BOTH_MEMBERS` |
| C01 | `evaluate_gate` read (3436) | `GATE_RECORD_UNREADABLE` only | plus `DUPLICATE_JSON_KEY_A71:...:<gate>` | `R10_A71_SITE_GATE_RECORD_DUPLICATE_JSON_KEY_*`; carried D8 |
| D01 | `load_pinned_json` (662) | `json.loads`, last-wins | strict; refuses `PINNED_FILE_DUPLICATE_JSON_KEY_A71` | `R10_A71_SITE_PINNED_JSON_PARSED_STRICTLY` |
| C05 / C06 | `load_producer_registry`, `load_strict_file`, `load_manifest` | refused | refused with a fixed code (S1) | carried D8 / A62.2 registry; `R10_CX2_S1_*` |
| R-1 | `load_driver_build_record` | (new) | strict; refuses | `R10_A71_SITE_DRIVER_BUILD_RECORD_*` |
| C02 / C03 / C04 | `read_run`, `_side_json`, `read_route_a_attempt` | strict | unchanged (strict) | carried D8 / N3 |
| T01 / T02 | `adapter_side_file_codes` (1639), from `read_run` | pinned V005 parsed field / rotation `finish.json` last-wins | strict pre-parse; a duplicate is a read code and the run is invalid | `R10_A71_SITE_V005_ADAPTER_FIELD_*`, `..._ROTATION_*` |
| T03 | V005 re-read of result.json | guarded by `adapted_sha_equal` | unchanged (a TOCTOU, not a duplicate) | carried |
| T04 / C08 | V005 rows dict | guarded by `rows_codes` (D2) | unchanged | carried D2 |
| T05 | pinned C4R3 in `_main` | not pre-parsed | `adapter_side_file_codes` first | `R10_A71_SITE_T05_S02_*` |
| R-2 | V005 `packet_checks` → `numpy.load` (zip index, NPY header) | last-wins | `npz_duplicate_member_code` + `npy_header_duplicate_key_code`: V4/V5 False | `R10_A71_SITE_FIELD_PACKET_NPZ_*`, `R10_A71_NPY_HEADER_*` |
| S02 | `read_numerics_only` | swallowed → None | unchanged; None is fail-closed (C4T-D5 V3 invalid) | `R10_A71_SITE_T05_S02_*` |
| S01 | `c5h_interlock` markers (1869) | a duplicate marker read as absent | refuses | `R10_A75_2_S01_*` |
| A01 | `_shells` (2590) | last-wins (LO, LO_NGC, LO extended) | `unique_map` after reading every entry | `R10_A71_CX2_B1_*` (4), Codex2 fixtures, mutation |
| A02 | `g_FLAG_RULINGS` (3357) / `flag_rulings` (3969) | last-wins (flag, run) | DEFECT naming both rulings; `flag_rulings` via `unique_map` | `R10_A71_SITE_FLAG_RULINGS_*` (both orders), mutation |
| A03 / B07 / C10 | `_spec_sets` (2605) | EXT evidence last-wins; set-dedup | a sha twice in one set is a DEFECT | `R10_A71_SITE_B0_SPEC_SET_*`, `..._B0_EXT_*`, mutation |
| A04 | `validate_case_block` key_equivalence_map (1336) | both entries acted (union) | a pointer twice is refused | `R10_A71_SITE_KEY_EQUIVALENCE_MAP_*` |
| A05 | `g_GQ` reach (3018) | same-name max-merge | one roster per reach, from kept K, with the A75.6 geometry | `R10_A75_A05_*`, `R10_A75_6_*` |
| R-3 | `g_GQ` rosters | none | (name, geometry, k range) twice, or one geometry twice: DEFECT | `R10_A71_SITE_GQ_ROSTER_TWICE_*`, `..._ONE_GEOMETRY_*`, mutation |
| A06 / A07 | `classify_failure` (1560) | first / last-wins silently | `ROUTE_A_STAGE_RECORD_REPEATED_A71`, `ROUTE_A_READOUT_REFUSALS_DIFFER_A71` | `R10_A75_2_A06_A07_*` |
| A08 | `classify_failure` reasons[0] | positional first token (report only) | unchanged: a list read positionally, not a mapping (DECLARED) | carried |
| B01 | `g_EPS` shells (2814) | every entry checked | a range twice is a DEFECT | `R10_A71_SITE_EPS_SHELL_RANGE_TWICE_*`, mutation |
| B02 | `g_I1T` builds (3165) | FAIL-sticky per case | (case, stage) twice is a DEFECT | `R10_A71_SITE_I1T_*`, mutation |
| B03 / B04 / B05 / B06 | `g_B0_RO1`, `g_B0_N3`, `g_B0prime_DRY`, `g_DOUBLING` | set membership | an entry twice is a DEFECT | `R10_A75_2_<gate>_LIST_ENTRY_TWICE_*` (4) |
| B08 | `producer_registry_from_obj` (978) | frozenset dedup | an entry twice refuses the registry | `R10_A71_SITE_REGISTRY_LIST_ENTRY_TWICE_REFUSED` |
| B09 | `check_uvt_record` flags (1906) | repeated flag accepted | `UVT_FLAG_REPEATED_A71`, the case invalid | `R10_A71_SITE_UVT_FLAG_REPEATED_*` |
| B10 / B11 | RO1 events; HARMONICS rows | lists, every entry checked; not mapped | unchanged (not a list-to-mapping site; DECLARED, root may extend) | carried |
| B12 | `_main --validity-only` labels | set-dedup | a repeated `--case` is refused; a repeated option or an abbreviation too | `R10_A71_B12_*` |
| B13 / D15 | `_case_validity` pointer loop | overlapping pointers, each checked | unchanged (no mapping from a list) | carried |
| C07 | `pass_rows_ids_code` → `_pass_rows` (1522) | S9 first, then a last-wins dict | S9 unchanged; `_pass_rows` uses `unique_map` (defence) | `R10_A71_SITE_PASS_ROWS_*` |
| C09 | `g_RB_FP` labels / ranges (3211) | refused, one entry named | both entries named; a range twice is DUPLICATE | `R10_A71_SITE_RB_FP_*` (2) |
| C11 / C14 / C12 / C13 | case-block cases, manifest keys, the alias detector, MT | JSON objects / detector | unchanged (strict JSON; the alias detector names every entry) | carried |
| D02 | `registered_row_radii` (708) | id→radius dict | `unique_map`; refuses | `R10_A71_SITE_ROW_RADII_*` |
| D03 | `registered_row_maps` (1092) in `build_context` | `dict(zip(...))` | 12 ids, equal lengths, `unique_map` | `R10_A71_SITE_V005_ROW_IDS_TAU_SIGMA_MAPS` |
| D04 / D05 | `_spec_leaves` (726) / `c5h_admission_bases` | `update()` last-wins | a pointer collision refuses | `R10_A71_SITE_SPEC_LEAVES_*` |
| D06 / R-4 | `r5_custody_codes`; `driver_build_codes` (824) | pinned map | pins sharing one sha refuse the build (A71); strict map parse | `R10_A72_R6_RECORDS_*` (TWO_PINS_ONE_SHA) |
| D07 / D08 / D10 / D14 / D16 / D17 | grids, canonical round-trips, constants, filters, key-path sets | pinned or code keys | unchanged (cannot carry a record duplicate) | carried |
| D09 | `dict(zip(ids, ...))` (E^A, SR_K Δ, rb_fp) | positional | ids unique (D03), lists `num12` | carried |
| D11 | `runs_sha_map` (5018), `cross_gate_checks` (5029) | keys disjoint by construction | `unique_map`: a collision raises | `R10_A71_SITE_RUNS_SHA_MAP_AND_CROSS_GATE_*` |
| D12 | `evaluate_gate.xr` crossref / mt_flags | dict writes | a field written twice is `DUPLICATE_ENTRY_A71:<gate>:crossref` | `R10_A71_SITE_EVALUATE_GATE_CROSSREF_*` |
| D13 | `_rpair_ea_view` (3908) | re-keyed dict | `unique_map`; a collision gives an empty view (fail closed) | `R10_A71_SITE_RPAIR_EA_VIEW_*` |
| E01 / E02 | `blind_strings` (4497), `blinded_gate` (4534) | blinded-key collisions last-wins | both kept under `<BLINDED_KEY_COLLISION_j>` | `R10_A71_SITE_BLINDED_KEYS_*`, `..._BLINDED_CROSSREF_*` |
| E03 | `finite_or_null` (4577) | `str(k)` collision last-wins | `unique_map`: raises | `R10_A71_SITE_REPORT_KEYS_*` |
| E04 | report `rulings` keys | from `flag_rulings` | unique by A02 | `R10_A71_SITE_FLAG_RULINGS_*` |
| R-5 | `unique_map` itself (504) | — | names both entries | `R10_A71_UNIQUE_MAP_NAMES_BOTH_ENTRIES` |

**Out of scope, DECLARED:** the pinned tail library's internals (`normalize_config`; pinned and inert) and the pinned V005 compare's internals beyond T01–T05 (not reached).

## Real records (TESTED; TEST registries built from bytes, never a root registration)

| Record | Reading |
|---|---|
| LO_CERT_V004_MS128 (**1c384f76**), the A70 slot | **PASS**, no codes. It is also PASS in a C2V003 registry of real pins, with its record sha registered. |
| LO_CERT_V003_MS128 (9fdb897a) | RECORD_DEFECT, `FIELD_MISSING:LO:source_gas_M_s` |
| LO_CERT_V002 (fd4fa52b; M_s 64 era) | RECORD_DEFECT |
| V004 rewritten as M_s 64 (all four M_s fields) | RECORD_DEFECT, the A57 and CHK-1 codes |
| V004 in an M_s 64 case-block context (direct gate call) | RECORD_DEFECT, `LO_REGISTERED_GAS_M_S_NOT_THE_A57_PRODUCTION_M_S_A68_CHK1` |
| GQ_CERT_V005_MS128 (**fbceefe6**) | **PASS**, no codes. All 10 geometries equal the label derived from each roster's node set. |
| GQ_CERT_V004_MS128 (7ebb1d48), the FAIL control | **FAIL**, `GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT:DDO_C4T` |
| GQ_CERT_V002 (M_s 64 rosters) | RECORD_DEFECT |
| V005 rewritten as M_s 64, and V005 in an M_s 64 context | RECORD_DEFECT |
| V005 S3 / S5 relabelled copies | RECORD_DEFECT, `GQ_DDO_C2T_GEOMETRY_NOT_THE_ROSTER_NODE_SET_R10` |
| EPS_CERT_V006 (598c8fa3) by record sha | PASS |
| A byte-different copy of LO V004 | RECORD_DEFECT, `GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:LO` |
| The token on EPS / GQ / LO / SR_K in a real-pin registry | REFUSED. On SRB_ROT it is accepted. |
| 968 real JSON files (certificates_v00*/gates, the launch packet, gq_full parts) | All parse strictly; no repeated key. LO V004, EPS V006 and GQ V005 lists have no repeated entry. |
| Every real certificate's producer path | Exists, and hashes to its named sha (A69 note 1). |
| The registered C5H directory | 1 identity (os.stat of the directory only). Its `/.vol` spellings, and both named spellings, are refused with no stat inside. |
| The built-in r5 build | Valid on bytes. An r5 BUILD record loads. |
| *Reported only:* the in-progress `driver_r6/` (driver 24c9f54c, CASCADE_MAP_R6 cd903ade, as read) | An r6 BUILD object formed from its declared path and sha maps passes the r6 rule (no codes). This is not an adoption check (A72.2). |

All 55 r8 expectations are carried and met. The carried r7/r8 checks were written for the r8 registry form, so the tool reads them through a TEST-tool emulation: a sha becomes the `{path, sha256}` pin of the file the real record names, and a token on a pre-seal gate becomes "register the record read" for that gate. This is DECLARED in the tool's docstring.

## Dispositions

| Finding | Disposition |
|---|---|
| Codex2 0442 **CX2-R8-B1** (BLOCKING) | Fixed (A71 `_shells`). Its fixtures read as their text requires: the four false-PASS cases now refuse, and the LO_NGC duplicates too. |
| Codex2 0442 **CX2-R8-S1** | Fixed: fixed refusal codes in both blinded modes; no stderr echo, no traceback. |
| Codex2 0442 deferred A68 CHK-1 / A69.1 probes | Fixed: `lo_direct_gate_context_ms64` and `b2_missing_producer_path` are now RECORD_DEFECT. |
| Codex2 0442 RB_FP 12 controls | Carried: 12/12. |
| r8 recheck validity **SF1** | Fixed: geometry derived and bound (option (b)); probes S3, S4 and S5 refuse. |
| r8 recheck validity **N1** / order **N2** (token on pre-seal gates) | Fixed (NEW-52 / A75.7 allow-list). |
| r8 recheck validity **N2** (c2v005 named in the seal steps) | Seal step corrected: the identity comparator of record is **c2v007** (A74–A76 supersede c2v005 and c2v006). Registry data; no compare change. |
| r8 recheck validity **N3** (the N3 edge is a producer contract) | Recorded under NEW-58: the producer emits `math.sqrt(2) * P` unrounded. |
| r8 recheck order **N1** (geometry not bound) | Fixed (as validity SF1). |
| r8 recheck order **N3** (independence) | Noted. The R10 tests are written from the A68–A77 texts and the Codex2 / Claude3 fixtures; the fixture library is shared with r8. |
| r8 recheck order **N4** (A71 not audited) | Done: the audit table above. |
| Claude3 r7 **A-N1** | Fixed. |
| Claude3 r7 **A-N2** (registry unknown key on stderr) | Blinded modes print the code only (S1). Full mode keeps the detail (DECLARED). |
| Claude3 r10_pre: P-SF1, P-N2, B1 reproduction, CHK-1 baseline, helper I items 1–7 | All fixed (above). |
| A75 items 1–8 (read mid-round) | Closed and TESTED. Interpretations are DECLARED under NEW-61, NEW-62, NEW-64 and NEW-66. |
| A77.2 (read mid-round) | TESTED. No code change was needed: the custody lists already were the role table. |

## NEW items for root

Numbered from NEW-61. NEW-52 to NEW-60 are r8's.

- **NEW-61: A75.7 and A67 N2 disagree on SR_K.** A75.7's parenthesis lists SR_K among the token-accepting gates, but A67 N2 says SR_K never takes the token. R10 keeps the stricter reading: SR_K is always registered by sha.
- **NEW-62: B0 is off the token list (A75.7, stricter).**
  - A post-seal B0 re-record that carries C5H R-PAIR member EXT evidence must therefore be registered by sha.
  - A registry pinned at the seal cannot hold that sha. Root decides one of two things: either B0 takes the token (NEW-52 "possibly"), or the registry gets a post-seal amendment step.
- **NEW-63: the A72 BUILD record.** Schema `UNT_V007_SEALED_DRIVER_BUILD_C2V001`, with the r5 and r6 rules above (DECLARED).
  - Root writes the record at the seal and pins it as `PIN_DRIVER_BUILD_RECORD`.
  - In sealed mode the record's `check_record` is required: the independent check of that build.
  - Reported: today's in-progress r6 bytes already satisfy the r6 rule.
- **NEW-64: the H-07 hard-link rule.** A75.4 asks for hard links "against every file of the C5H run", which means listing the run directory. The brief forbids that.
  - R10 instead refuses every multiply-linked regular file on the registered run's device, in test-mode full mode only. This is a superset, and it fails closed.
  - Root to accept, or to authorize an inode inventory written by root.
- **NEW-65: registry C2V003.** It holds `{path, sha256}` pins, and every file is hashed at load and again at every read.
  - A C2V002 (sha-only) registry is refused.
  - So is a pin with a relative path, and so are two pins sharing one sha.
- **NEW-66: GQ geometry (DECLARED).**
  - The derivation formats are as above.
  - Only the k range's upper edge is bound to the node set, so that the lower-edge fixture form [2, K_big] stays valid. The A05 reach takes the lower edge into account.
  - A75.6 is read as follows: the fixed-map geometry must carry the named reach. When it is absent, the reading is `GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT`, a FAIL, so that GQ V004 keeps its A67 SF2 FAIL. A mislabel is a RECORD_DEFECT.
- **NEW-67: CHK-1 scope (DECLARED, stricter).**
  - DOUBLING is bound to the registered M_s too, and so are GQ's top-level DDO M_s fields.
  - The LO echo fields include `build/roster_gas/M_s`, beyond A73 F2.
  - The registered M_s must itself be 128.
- **NEW-68: A71 reaches the CLI and the outputs.**
  - Repeated options, abbreviations and a repeated `--case` are refused.
  - Blinded-key collisions in outputs keep both entries.
  - A `str(k)` collision in the report raises.
- **NEW-69: A77.2 under A72.** If r6 is adopted, the role table becomes the r6 images of the same families, read from the BUILD record. The binding stays 86af6198.
- **NEW-70: the identity comparator of record is c2v007** (A74, A76). It goes into the C2V003 registry as an `identity_comparators` pin, and its token sets as `identity_tokens` pins.

## UNTESTED

- Every real V007 record, and every R-PAIR on real runs. None exist.
- A root C2V003 registry; a root BUILD record; the r5 or r6 check record.
- The real r5 identity runs (UVT_*; forbidden to open).
- An RB_FP producer record that carries `shell_ranges_inverse_kpc` (NEW-43 / NEW-58).
- A c2v007 identity-gate record.
- Adoption of the r6 driver (A72.2).
- H-07 on a real hard link or real `/.vol` access into the registered run. The run is never touched; the rule is TESTED on a stand-in directory.
- The float floor. Its deciding test is the late-pass increments of the first real 12-pass member.

## Seal-time steps

The r8 steps, plus:
1. Root rulings on NEW-61 to NEW-70, and on the open NEW-30 to NEW-60.
2. The root producer registry in schema C2V003:
   - producer, comparator (c2v007) and token **file pins**;
   - `gate_records`: by sha everywhere except the A75.7 post-seal gates;
   - `gq_all_nodes_counts`.

   It is pinned as `PIN_PRODUCER_REGISTRY`.
3. The A72 decision (r5 or r6). Root writes the BUILD record, with its `check_record`, and pins it as `PIN_DRIVER_BUILD_RECORD`. For r5, `PIN_V010_R5_CHECK` is pinned as well.
4. Two independent rechecks of r10, Claude3's distinct review (0560), and at most one fix round, r11 (A72).
5. Freeze and pin the V005 addendum.

## Errors register (this round)

1. **A placeholder sha in a docstring.** The r10 real-record tool's docstring first cited its r8 parent as "2dfd6b76", a placeholder. That violates the hashes-from-bytes rule. It was corrected to **4b23a2e4**, computed from bytes, before any run of record. Trials rrc1–rrc3 carried the placeholder text; they are not of record.
2. **A global text replacement made `PRF` recursive** in the suite. It was corrected before the first trial.
3. **Trial t1:** an r6 test called `_pass_rows` on a duplicate world and crashed. The test was adapted (above). The crash was R10 behaving as intended.
4. **Trial t3:** the r10 tests used a relative OUT path in registry pins, and the registry correctly refused them. Fixed by using absolute paths.
5. **Trial t4: four failures; two test-side corrections and one compare change.**
   - **Test side** (corrected): the repeated-flag world carried an MT record that contradicted its run (the MT gate is now dropped there), and the CHK-1 real-record test expected a CHK-1 code from GQ_CERT_V002, which fails earlier on `all_nodes` (an M_s 64 copy of V005 now carries that expectation).
   - **Compare change:** the other two failures (the SF1 probes and the kept-node-set test) showed that a GQ duplicate raised alone hid the record's binding codes. GQ duplicates are now appended to the record's other defects, so both are named.
6. **Mutation trials:**
   - ORDER_B1 reverted now reads REFUSED_AT_LOAD, not ADOPT_TAIL. This comes from the A-N1 interaction and is documented in the tool.
   - The SF1 mutation world was isolated after A75.6 made the first world FAIL with the derivation reverted.
7. **The binding text moved mid-round** (A73–A77). A75 and A77.2 were implemented after the first green trial. Their tests were added and the full runs of record were repeated. Trial outputs are kept: `out/trial/`, about 446 MB, no deletion.
8. No file was written outside `r10/`: no scratchpad, no earlier round. Build edits ran as in-process heredoc scripts, so no build fragment file exists.

## Files

| File | What it is |
|---|---|
| `kmax_tail_compare_c2v007_r10.py` | The compare. |
| `tests_kmax_tail_compare_c2v007_r10.py` | The suite. |
| `FIELDS_R10.md` | The field contract, from `--write-field-contract`. It equals the suite's regeneration. |
| `tools/real_record_check_c2v007_r10.py`, `tools/mutation_check_c2v007_r10.py`, `tools/uvlib_probe_c2v007_r10.py` | The checks. |
| `tools/guard_r10.py`, `tools/sandbox_r10.sb`, `tools/run_guarded_r10.sh` | Guard, sandbox profile and runner. |
| `tools/fixture_producers/*.fixture` | Inert fixture producer, comparator and token files. Each file's bytes are the r8 fixture string. |
| `out/tests_R10/`, `out/tests_R10.{stdout,stderr}.txt`, `out/tests_R10_guard.json` | Suite run of record. |
| `out/REAL_RECORD_CHECK_R10.json` (+ `.records/`, stdout, stderr, guard) | Real-record run of record. |
| `out/MUTATION_R10_RECORD/` (+ stdout, stderr, guard) | Mutation run of record. |
| `out/UVLIB_PROBE_R10.*` | Tail-library probe. |
| `out/trial/` | Trials (not of record). |
| `HASHES.txt` | Every sha, from bytes. |
