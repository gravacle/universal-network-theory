# CROSSCHECK_V003_C4V001: root's seal disclosures V003 (dispatch 0658), A115 scope

From a **Claude4 lane helper**, for Claude4. Written 2026-10-19T04:43:26Z (`date -u`). Folder: `claude_artifacts/review_disclosures_v003_c4/`. Every sha below was computed from bytes in this session. Nothing was launched. No NGC3198 target or observed-velocity data, `runs_ext`, `UVT_*` run output or C5H path was opened. Every scripted check ran under the review fence `tools/fence_c4v002.py` (c993d34c…), through `tools/run_fenced_c4st2.py` (fe904509…), both byte-identical copies of the seal_tools_v004 tools. In every run the fence selftest passed 8/8, the exception probes passed 15/15, and `blocked_after_selftest` was `[]`. Python: the codex runtime python3 with `-I -B` and OMP/OPENBLAS/MKL/VECLIB thread variables set to 1.

**Object.** `seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V003.json`, sha256 `990be628e810bc38afd6657ac151cfb908c761ce266c232de71baf8bd6d300eb`, 9,733 bytes, mtime 04:14:57Z. **Predecessor:** V002 `a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3`, 6,286 bytes.

## Verdict

V003 passes every check that 0658 asks for: the form, the delta from V002, E_R6_1, every pin, the C-08 table and tool 4 v004.

It is nevertheless **superseded and must not be sealed.** Its A114_A117 row names I4 producer **c3v001** (`4d6263f6…`) and registry **V010** (`b8435877…`). That is the class-(a) defect in Claude4 0142: c3v001 refuses the honest I4 runs, which sit under a symlinked ancestor. This helper saw the supersession on disk on its own at about 04:24Z (PARTIAL 04:29Z), before 0142.

Root has already fixed it:
- 0660 rules registry V011 (`512a7171…`);
- 0661/A119 publishes disclosures **V004** (`adac5030…`), which changes only that row.

The V004 delta at the end of this report reads **0 blocking**.

**Counts against V003:** (a) 1, already resolved by V004; (b) 0; NOTE 6 (N2–N7). **Against V004 (addendum):** 0 blocking; NOTE 1 (N8). V004 also carries N2–N7 unchanged, because only its A114 row differs.

## The checks (TESTED = executed on bytes; FORMAL = read and compared)

The records are `out/CHECK_V003_C4V001.json` (29 checks, all TESTED checks ok) and `out/TOOL4_V003_C4V001.json` (6 checks, all ok).

### (1) V003 is V002 plus exactly the declared changes (TESTED)

- **Parse and keys.** A strict parse that refuses duplicate keys succeeds on both files. The keys are exactly `{schema, e_r6_1_text, c08_table, c08_confirmation, root_disclosures}`, and `schema` is `SEAL_MANUAL_DISCLOSURES_V001`. Both files are ASCII and are exactly `json.dumps(obj, indent=1, sort_keys=True)`, with no trailing newline.
- **`e_r6_1_text`.** It is byte-identical in V003, V002 and SELECTED_R6_C4V001 `basis.erratum_E_R6_1` (SELECTED_R6 `7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0`). It is 469 characters; the UTF-8 sha is `c28202b0909371f43180ca832e4652f3d835a977852cde5c261842315deb33f4`, which matches tool 4's header. It also equals tool 4's `E_R6_1` constant.
- **`root_disclosures`.** V002's six rows are unchanged and in the same order. They are followed by exactly E_R6_2, A113_ROOT_ITEMS_R6, A114_A117_I4_AFTER_SEAL and A118_CUSTODY_FORM. All 10 ids are unique and every row is `{id, source, text}`.
- **`c08_table`.** It has 19 rows with the same ids, lines and `declared_in_r13: false` as V002. Only `file` changes, from the r13 path to `v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py`.
- **Text diff.** Every changed line falls into one of three classes: the `c08_confirmation` line, the 19 `file` lines, or the 20 inserted lines of the four new rows. No other line changes.
- **Reverting restores V002 exactly.** Put the r13 paths back, restore V002's `c08_confirmation` and drop the four new rows; the canonical dump then hashes to V002's `a0284ece…`.

### (2) Every cited pin, verified from bytes (TESTED)

All 6 full shas in V003 match their bytes:

| Item | sha256 |
|---|---|
| r14 | `f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7` |
| SELECTED_R14_CX1V002 | `6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a` |
| IMPL_R14_CX1V002 | `2ba6d12ecc36ab444365348573b7f49a02a12a818dd15d67de35d77300fa17c9` |
| I4 producer c3v001 | `4d6263f6b94d7ba50750eb7e19d96c16a17aa3fb9959faa1213d9504a7101845` |
| V010 | `b843587733ea2a532b522c69657dc5aab11cb33771acd3f20a4c4f3656c2331b` |
| N1 spec | `8ae6e2db8a1c721fa347d960c5aabe50bef20878ef8cefa047fabfed576c7ee7` |

All 10 eight-hex prefixes match the file each one names:

| Prefix | File | Full sha256 |
|---|---|---|
| 274f7049 | IMPL r13 | `274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3` |
| 915fbcda | B2_GATE_RECORD_C3V003 | `915fbcda4f4a2cb5f61b257ff83494738144e177401c11c94e254c322df2411c` |
| 1d5eef1b | EPS_CERT_NGC91_V001 | `1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d` |
| 3ae7981a | I1T_NGC_T120L_V001 | `3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6` |
| 89a6de88 | driver_r5/check/CHECK.md | `89a6de88739e1c4b76c39dc11d7417d7e243b7235511d8ea0951e1493865b632` |
| 6758bd24 | R5_REVIEW_FINAL_V001 | `6758bd24784ec514d73054a30a8fdd673c3d0c571521a62514ba4260f3ad7ba9` |
| f5adfd11 | r13 | `f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157` |
| 84933cad | C2T FILLED | `84933cad8fa19bd9d8e95893e19ce744f8d19d3b44c937eb9ddf599c5c333bf2` |
| b5cc62af | driver r5 | `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6` |
| ac793faf | Z2 report | `ac793faff46adb26c71effe880dfb3e92642a36dec8c33e57d83f350d8f49795` |

The two NGC certificates and the Z2 report were hashed only; their content was not printed.

Further checks:
- **Relative paths.** V003's relative paths resolve under `claude_artifacts/`.
- **Files cited by name.** `NEW_ITEM_DISPOSITIONS_V007_COMPLETE` is `68164144…`. The CASCADE_MAP_R5_ADDENDUM is `86c89730…`.
- **Messages cited.** Claude3 0124 and 0127, Claude4 0131, 0134 and 0135, Codex1 0126, Codex3 0646 and root 0657 all exist.
- **A105 (C5H) is UNTESTED by rule.** The row cites the C5H run by name only, and it was never opened or stat-ed.

### (3) The C-08 table against r14 (TESTED)

- **The r13 → r14 delta.** r13 and r14 both have 5,866 lines. They differ only at L341, where `, 'I4'` is appended to `GATE_RECORD_AFTER_SEAL_ALLOWED`. Removing it restores r13's `f5adfd11…` exactly. No line shifts.
- **Every row.** Line N of r14 carries that row's NEW-n id, and N is the **first** r14 line that carries it. The same holds on r13.
  - The forms match V002's r13 rows: NEW-13, NEW-60 and NEW-73 are parenthesised, and the rest are bare.
  - NEW-21 at L108 is the start of the range `NEW-21..29`.
- **The id set.** The explicit NEW-n tokens of r14 are exactly the 19 table ids, and r13's are the same 19.
- **IMPL r14.** IMPL_R14_CX1V002 names the full r14 sha, says "r14 declares no NEW item", and contains no NEW-n token.
- **SELECTED_R14_CX1V002.** Its `selected_source` and `implementation` pins equal r14 and the IMPL.
- **The NEW-item list.** The COMPLETE file holds the same 19 ids, its compare_impl is IMPL r14, and NEW-30 and NEW-44 are ADOPTED.
- **The `c08_confirmation` statements** are therefore true of r14's bytes and of IMPL r14, apart from NOTE N3 (the timestamp) and NOTE N4 (the "[NEW-n]" wording).
- **"Row key `declared_in_r13` kept for the tool contract"** is consistent with tool 4, for which that key is an optional bool (FORMAL).
- **"As declared in the originating rounds' IMPLs".** The COMPLETE file grounds all 17 non-A118 dispositions in their originating IMPLs: 11 stated there, 4 adopted under RI-10 as declared stricter, and 2 that carry out root rulings.

### (4) The new rows against r6 and A113–A118

My FORMAL comparisons used V006 `8ac68396110fd789471d65e4bff663f07d6132a08fcf52df4d54784a197000ff`. At the record run V006 was `7165cffb3d9b3b895eaf9a912c5616490db9ad544d365d52df2f73bcbf8ca8db`: A119 had been appended at 04:38:15Z, and A113–A118 are still at lines 99–188.

**E_R6_2: accurate.**
- r6 (`d28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9`) `seal_slots.compare.rule` contains "The final compare round is r13 cx3v001 (f5adfd11" (TESTED).
- `producer_registry.rule` says "…and the B0_N3, B0_RO1 and I4 records once built (their empty slots fail closed)", so the quote "the ... I4 records once built" is a faithful ellipsis (TESTED).
- The slot rule's general clause, "V007 seals on the final compare round whose delta reviews of record each report 0 blocking", is present (TESTED).
- Claude3 0124 and Claude4 0134 each report 0 BLOCKING as reviews of record (TESTED).
- "r13 + 'I4'" holds (TESTED, item 3).
- V010 has `producers.I4` = [c3v001 pin] and `gate_records.I4` = PRODUCED_AFTER_THE_SEAL (TESTED).
- The row matches A116.2 and A117 (FORMAL). For other r6 clauses that still carry the old wording, see N2.

**A113_ROOT_ITEMS_R6: matches A113 and A118.**
- Each RI clause and the NEW-30 and NEW-44 wording match A113's table and A118's bullets (FORMAL).
- The open r6 root items are exactly RI-30, 31, 32, 33, 35, 36 and 37. The row covers all of them except RI-36, which A113 rules "in A111" and which row A111_P3_P4 carries (TESTED).
- **RI-31:** the record `b0_ms128_c4/out/B0_R5_VS_R4_MS128_C4V001.json` (`3a798efa…`) reads `summary.verdict_B0` = PASS_PLAN_IDENTICAL with n_pass 10. Codex1 0126 PASS names that sha (TESTED).
- **RI-32:** Codex3 0646 lists the addendum's sha `86c89730…` (TESTED).
- **RI-33:** V010 `gate_records.B0_N3` = [`dd1dd912…`] and `B0_RO1` = [`332452b7…`]. Both records exist at those shas, and both read gate B0_N3 or B0_RO1 with verdict PASS (TESTED).
- **RI-37:** V010 `producers.SR_K` is only `aggregate_records_cx1v008.py` (`9794123d…`) (TESTED).

**A114_A117_I4_AFTER_SEAL: matches A114, A116 and A117** (FORMAL), except for the stale producer and registry (F1).
- **N1 spec against C2T FILLED.** The strict-parse leaf diff is exactly `/numerics/route_a/column_workers` 8 → 1. The files differ in one byte, at offset 5170 (0-based). Both are 6,771 bytes, and route B's `numerics.column_workers` is unchanged (TESTED).
- **Tail ON.** C2T has `/numerics/uv_tail/enabled` true (TESTED).
- **Earlier verifications.** Claude3 0127 and Claude4 0135 both state the one-leaf result (TESTED).

**A118_CUSTODY_FORM: matches A118 and 0657.**
- The row deliberately names no converter version. A118's `1b097cba` is v001, which refuses the real report (0656), and A119 now names v002, `f7d78bce`.
- The row is tested against the custody record of record (V6 below), with one wording NOTE, N6.

### (5) Tool 4 v004 under the fence (TESTED)

The tools were loaded from bytes and checked against SELECTED_SEAL_TOOLS_V004_C4V001 (`593c59faf39074b14579f927ae17c5aeda1f7450ee4a9f264f96a1f2c7b195e0`):
- tool 4 `9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41`;
- seal_common `101a3aeb…`;
- tools 1, 2 and 3: `a56f8d79…`, `c2c5dfc5…` and `316973a1…`.

Results:
- **`manual_disclosures_codes`** with the pin `(…/SEAL_MANUAL_DISCLOSURES_V003.json, 990be628…)` returns no failures. Its note is "19 C-08 rows and 10 root disclosures; e_r6_1_text equals prereg r6's E_R6_1".
- **`manual_disclosures_record`** returns `{pin, content, raw_text}`, with no failures:
  - `raw_text` encoded as UTF-8 **equals V003's bytes**: sha `990be628…`;
  - `content` equals the parse;
  - the pin equals the path and sha.
- **R-02 round trip.** The same three facts survive serialising the record as tool 4 prints it and parsing it back.
- **Controls.** These only show that the check is not vacuous; under A115 none of them is a finding.

| Control | Result |
|---|---|
| wrong sha | PIN_MISMATCH |
| relative path | PIN_MISMATCH |
| V002 | accepted: 19 rows and 6 rows |
| a one-character E_R6_1 change | E_R6_1_TEXT_MISMATCH |
| an extra top-level key | MANUAL_DISCLOSURES_KEYS |
| bytes changed after the check | CHANGED_AFTER_CHECK |

## Findings, by A115 class

- **F1 — class (a), already resolved by V004.** V003's A114_A117 row names I4 producer `ri33_c3/i4/write_i4_record_c3v001.py` (`4d6263f6…`) as registered in V010 (`b8435877…`).
  - c3v001 refuses an honest run under a symlinked ancestor. This is Claude3's helper's own finding, from `ri33_c3/i4/PARTIAL.md` (`d93f3b9f8974dc92102b49a4e82244d6ee0f257e3b6605362ed82d780b808d76`, 04:15:44Z and 04:18:57Z). Claude4 0142 classes it BLOCKING (a), because no I4 record could be written and parallel8 route A would never be licensed.
  - The successor `write_i4_record_c3v002.py` (`2a315da24b06d1825fd5015e8b3f17a9a77e2b0fc670a3d75043c8507d7bdaa4`) appeared at 04:17:20Z, after V003 (04:14:57Z).
  - **Remedy, already done:** 0660 rules V011, and 0661/A119 publishes V004. Do not seal V003. V003's statements are true of V010's bytes; the defect is the producer it discloses.
  - **Scope of the class.** This helper did not itself test c3v001's refusal; Claude4's V011/c3v002 delta covers it. Root's 0660 run-plan note puts the C2T N8 T-run and the N1 companion under `/Users/bgm/Research/UNT_INTERNAL_RUNS/…`, which it calls a real directory. So whether c3v001 would actually have been reached depends on that path's ancestors. A119 accepts the (a) class regardless, since c3v002 handles both cases. F1 is classed (a) here to match 0142 and A119.
- **N2 — NOTE.** E_R6_2 names only `seal_slots.compare.rule` and `producer_registry.rule`. r6 also still carries the old wording here (TESTED):
  - `status`: "The final compare round is r13 cx3v001 (f5adfd11…";
  - `gates_before_any_T_result.after_seal_marker_policy`: "accepted only for the nine gates … refused … for every other gate (r13)", whereas under r14 I4 is a tenth;
  - `outcome_branch_tests_required`: "the final round: r13 cx3v001 f5adfd11";
  - `seal_record_requirements[13]`: C-04 "through r13's own load_producer_registry against registry V009";
  - RI-32 and RI-33 with status OPEN.

  E_R6_2's substance ("the compare of record is r14 … I4 is an after-seal gate whose producer is registered in V010") covers them, and the sealed r14 code computes every gate verdict. So no reading changes. A successor could list these clauses in one sentence.
- **N3 — NOTE.** `c08_confirmation` says the check was done "at 2026-10-19 ~04:20Z", but V003's mtime is 04:14:57Z. The check cannot postdate the file. The V003_DRAFT has the same pattern: "~03:45Z" against an mtime of 03:19:53Z. V004 carries the same text. The stamp is forward-dated, with no effect on any reading.
- **N4 — NOTE.** `c08_confirmation` calls the ids "[NEW-n] tag[s]". In r14 only NEW-52 has a literal bracketed form ([NEW-52], L1106). The 19 table lines carry the ids bare or parenthesised, exactly as V002's r13 rows did. This is wording only, and the table is correct.
- **N5 — NOTE.** r14 L108 reads "RI-10 NEW-21..29 dispositions". NEW-20 and NEW-22 to NEW-29 are not table rows, and they are not in the COMPLETE list.
  - Their dispositions are in compare r6's IMPL (`COMPARE_V007_IMPL_R6.md`, `5741a76c4f0c838b771f76f1b2e8c7997d4a59e42a0fbeada1c12d88e021266e`, L63–77, headed "(for the seal record)"). There, NEW-28 is "Open: no compare rule is ruled".
  - A58 RI-10 says that list is quoted in the seal record. A113 P6 and A118 fixed the 19-id index, and none of these items changes a reading.
  - Root may add a pointer sentence in a successor.
- **N6 — NOTE.** A118_CUSTODY_FORM says "the per-kind counts and per-stage list are in its method/note". What the record actually carries is TESTED in V6 below:
  - the class counts: stages_total 24 = stages_successor 24 = n_successor 18 + n_base_by_design 6;
  - the list of base-by-design stages and kinds;
  - a 24-row per-stage list.

  It carries no count per kind; 0657 says "the three counts". This is wording only.
- **N7 — NOTE.** The byte-fixed E_R6_1 names the r13 IMPL `274f7049` as "the IMPL of record". E_R6_2 does not say that IMPL r14 succeeds it, as Claude4 0134 suggested. The c08_confirmation and the A114_A117 row do name IMPL r14.
- **N8 — NOTE (V004 addendum).** V004's A114 row says "= V010 b8435877 with only the I4 producer pin changed". V011 also differs from V010 in its free-text `note` (TESTED: the differing keys are `note` and `producers.I4`). This is wording only.

An aside, outside V003's text: Claude3 0127 gives the N1/C2T byte offset as 5171. The 0-based offset is 5170, which Claude4 0135 and Claude3's own helper log both give. V003 cites no offset.

## Addendum (outside 0658's object): the V003 → V004 delta, 0 BLOCKING

0661 superseded V003 during this check, so the same fence and tool bytes were applied to the V004 delta. The record is `out/V004_DELTA_C4V001.json`, 6 of 6 ok, TESTED.

- **V1, the pin.** V004 `adac5030770ec78114145fe80ae1b21e454d43b788037a632c01af076b25abfe` is 9,906 bytes. It has the five keys and the same schema, its `e_r6_1_text` is byte-identical to SELECTED_R6's, and it is in canonical form.
- **V2, the delta.** Every field except one row equals V003's. The only changed row is A114_A117_I4_AFTER_SEAL:
  - its source gains ", A119";
  - its text changes c3v001 → c3v002 (`2a315da2…`, with the supersession reason), and V010 → V011 (`512a7171…`, "= V010 b8435877 with only the I4 producer pin changed");
  - putting back V003's row restores V003's `990be628…` exactly.
- **V3, the pins.** Every full sha in V004 matches its bytes. `4d6263f6` and `b8435877` no longer appear as pins.
- **V4, the registry.** V011 is `512a7171b952ca97668e8646b106608679ed963faaceba9604dbc3750a7e45f8`. It differs from V010 only in `producers.I4`, which is [c3v002 `2a315da2…`], and in `note`. `gate_records.I4` is PRODUCED_AFTER_THE_SEAL.
- **V5, tool 4.** Tool 4 v004 accepts V004 with no failures ("19 C-08 rows and 10 root disclosures"), and `raw_text` encodes to V004's bytes.
- **V6, the custody record.** This is the A118 row, identical in V003 and V004, tested against the custody record of record `CLAUDE2/V007_SEAL_ASSEMBLY_INPUTS/custody_run_v002/RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json` (`9ca16b4fd07fd470359cb604526e38807ecf50093cf59ad7895441601535f67d`):
  - tool 4's own `custody_codes`, on driver b5cc62af, reports no failures, with all evidence pins verified;
  - stages_successor = stages_total = 24, which equals the 24 per-stage rows;
  - the classes are 18 successor and 6 base_by_design; the base kinds are column_mean_v004, feedback_v002 and feedback_v004;
  - the evidence includes Z2 report `ac793faf`, B1 record `83e7b067` and converter v002 `f7d78bce`;
  - the method states that each stage ran "the script the driver slot designates for their kind".
  
  So the row's statements hold of the real record, apart from N6.

## Not tested, and the rules kept

**Not tested:**
- the C5H row (A105) and any C5H path;
- c3v002's path rule itself, which is Claude4's V011/c3v002 delta;
- the I4 run pair, which does not exist yet;
- the seal script c3v010;
- the production seal.

**Rules kept:**
- No recursive content search was run. `find` was used by name once, with the forbidden names pruned, and `grep` was run only on named files.
- No file outside this folder was written.

The dry runs under `out/dry/` are kept. dry1 of the V003 check and dry1 of the V004 delta each failed only on a defect in the check script itself: a trailing newline assumed in the canonical form, the B0 verdict key under `summary`, and the A119 source suffix. Each script was patched, and its dry2 equals its record run. The V003 record differs from dry2 only in the V006 sha, because A119 was appended in between.

## Files

| Role | Path | sha256 |
|---|---|---|
| check record, V003 | `out/CHECK_V003_C4V001.json` | `843b65b3cefd43509ac563816eea57790367e24967c5e098b5bdce452d46e0df` |
| tool 4 record, V003 | `out/TOOL4_V003_C4V001.json` | `a5d0a9517e2129803c90f6c1eeaabffbadda8255dbf2d9177bc1fd7bd6274df1` |
| V004 delta record | `out/V004_DELTA_C4V001.json` | `f3087034793181ffdefab22d12f124a66dabe271160365059535d3544cc315be` |
| V003 check script | `tools/check_v003_c4v001.py` | `240b69e70c0d03846d3791644c16de55674a9ec3581c15569083898e820292ca` |
| tool 4 check script | `tools/check_tool4_v003_c4v001.py` | `2936e5edca46f71fd539de40866c53829d3a0ea63736b66485003976bd91b4ca` |
| V004 delta script | `tools/check_v004_delta_c4v001.py` | `2e51aece65493c6d50300a5e11a94d2e0fa4748cfe8589a1c57c85915ee1a530` |

All files, this report included, are listed in `HASHES_CROSSCHECK_V003_C4V001.txt`, which is written last.
