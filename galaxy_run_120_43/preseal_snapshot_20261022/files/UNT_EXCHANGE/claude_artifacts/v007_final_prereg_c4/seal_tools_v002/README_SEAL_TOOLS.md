# seal_tools v002: root-side V007 seal checks (Claude4, A99 item 4, dispatch 0621)

UTC 2026-10-18T21:32:30Z (`date -u`). Successor of `../seal_tools/` v001 (README `1e04bd2a`, 40/40). **The tool set of record is `r2/`.** The top-level `*_c4v002.py` files are r1, kept unchanged; r2 supersedes them with the A102 (A-B1) hardening and the text-of-record argument. Tools 1 and 2 are byte-identical in r1 and r2.

Five small scripts that root runs at seal assembly. **Each one only reads and checks.** None writes a file, starts a process or touches the network. The SEAL_RECORD builder and the driver-BUILD-record printer print bytes; root creates the files. Every JSON input is parsed strictly, and a duplicate key refuses (A71). The command line refuses abbreviations and repeated flags. Run them with the pinned isolated Python: `python3 -I -B <script> ...`. A verdict JSON goes to stdout (stderr for tools 4 and 5). Exit 0 means PASS, exit 2 REFUSE. An unexpected exception is also a REFUSE with code `INTERNAL_EXCEPTION:<type>` (D-07), never a traceback.

Tool 3 loads the slot's reviewed compare in-process to call its own `validate_case_block`, `load_driver_build_record` and `activate_driver_build`. Importing it runs only definitions (r12: constant assignments, `def`s and `import numpy`; read by AST). It is compiled from the very bytes whose sha matched the slot. My tests ran every tool inside `tools/fence_c4v002.py` (see below).

## What v002 fixes

| item | fix | tool |
|---|---|---|
| D-01 | Every M_s field of FIELDS_R12, per certificate kind: LO `source_gas_M_s` and its echoes (A73 F2); GQ `rosters[].M_s`, with `M_s_doubled` = 2 M_s and NGC_T120L at the NGC M_s; DOUBLING `ddo_gas_M_s` (A73). Then every other M_s-type key (`M_s`, `gas_M_s`, `*_gas_M_s`, `gas_M_s_DDO/NGC`, `…/M_s`). The DDO value is the case block's registered gas.M_s (A68 CHK-1; must be 128, A57). The NGC value is the slot, which must equal the compare's `NGC_GAS_M_S_A57` (96). The real DOUBLING `ea48ac2b` passes and any contradiction refuses. The NGC half needs no M_s while the slot is 96. Under RI-23's 128, DOUBLING and LO_NGC must state it. | 3 |
| D-04 | The sealed prereg must carry `binding_inputs.case_block` {path, sha256}. It is verified from bytes and validated by the reviewed compare's own `validate_case_block`, after the slot's driver BUILD record is activated by the compare's own `activate_driver_build` (the sealed-mode order, r12 L5689–5729). The route-A modes of the prereg and the case block must agree. Under r5 the `cascade_map_r5_addendum` slot is required (SRR[9], A69) and must name the build's r5 cascade map sha. The `admission_entry` slot (SRR[10], A78 N2) must equal the bound plan's launcher and guard and be BUILD_V007-supported entries. All of this passes through to the SEAL_RECORD. | 3, 4 |
| D-06 | Tool 5 prints the exact driver BUILD record (PIN_DRIVER_BUILD_RECORD): the reviewed compare's `builtin_r5_build()` with `check_record` = the driver check record, admitted by the compare's own `activate_driver_build` before printing. The three B7 JSON forms are defined below. The checklist step itself is SEAL_CHECKLIST_R5 B2a (prereg r5). | 5 |
| D-07 | A bare PENDING string, a list or a partial object in a pin slot refuses `PIN_SHAPE` (exit 2 with a verdict JSON), not a TypeError (exit 1). | 2 (and all) |
| D-08 | The layers are reported together. A layer is skipped, with a `LAYER_SKIPPED` note, only when a pin it reads did not verify. | 3 |
| D-09 | The SEAL_RECORD states that it is the authority on sealed status, and lists the PENDING strings that the text of record keeps outside slot values. | 4 |
| D-10 | The frozen copy must sit exactly at `seal_slots.frozen_addendum.path_to_be`: tool 1 checks the file, tool 3 checks the slot. | 1, 3 |
| D-05 | `--covered-later` is an explicit comma-separated list of `A<n>` items, with no ranges and no repeats (example below). | 1 |
| A99.1 | The launch-packet BUILD is read from the prereg's `seal_slots.launch_packet.named_candidates_verified_from_bytes.build`. It must be `BUILD_V007.md`; V005, V006 or anything else refuses `BUILD_NOT_BUILD_V007`. While its sha is the literal `PENDING_BUILD_V007`, tool 3 refuses `BUILD_V007_PENDING` (a gap). If the text of record holds that literal, the sealed prereg may fill that one leaf with the real sha, verified from bytes; nothing else may change. Its allowlist must list exactly 15 sources, each path once and each verified from bytes (V6-S3). The bound plan's template must be named in it, and must be the prereg-named `template_plan` (r5: V011). | 3, 4 |
| A99.3 | The prereg's `entries_after_A81` table, in the prereg r5 form: rows {entry, decision REVISED_HERE with revised_clauses, or NO_CHANGE with reason, section_sha256, section_bytes, heading}. It must hold every frozen entry from A82 through the last cited entry, once each. Each row is re-hashed from the frozen bytes by r5's section_rule. A changed row needs root's explicit note (list it in `--covered-later`) or a successor revision. The SEAL_RECORD quotes the table. | 1, 4 |
| R-04 | The B6 inputs must be the sealed compare's own blinded bodies `GATES_ONLY.json` and `VALIDITY_ONLY.json`. Each has schema `<SCHEMA_REPORT>_GATES_ONLY` / `_VALIDITY_ONLY` (read by AST from the sealed compare), `blinded` true, `test_mode` false, `script_sha256` = the sealed compare, and `route_a_mode` = the case block's. The validity body covers exactly C5H. Neither may carry a value: no JSON number, and no number token in any string or key, under r12's own rule and allowed constants (L4818–4824) plus v001's row-value rule. The B7 inputs must parse with the schemas below. | 4 |
| R-10 | The SEAL_RECORD key map must equal the validated case block's `key_equivalence_map` (which is `[]` when the block has none). | 4 |
| A100 | When the prereg asks the seal record to repeat the B2 disclosure block (r5 SRR[12]), `--b2-record` names the B2 record of record. It must be a PASS B2 gate record listed in the slot registry's `gate_records.B2`. Its `disclosure` object, and that requirement's text with A101's erratum, are quoted. | 4 |
| A102 | A-B1 class. The driver check record and the CASCADE_MAP_R5_ADDENDUM may be text, but if either is JSON it must parse strictly. Integers are parsed as strings, and the only text fallback is a JSON syntax error. So a duplicate key behind a 4,300+ digit integer refuses, even while r12's own `check_record_codes` still admits it; r13 fixes the compare. The addendum part was patched by the Claude4 main loop in r1. | 3, 5 |
| B8 | Admission mode: `--check-admission-config CFG --seal-record SEAL`. | 4 |

## When root runs each tool (SEAL_CHECKLIST_R5 order)

`T=…/seal_tools_v002/r2`. The paths below are placeholders.

| step | command | it refuses |
|---|---|---|
| B1 (freeze) | `python3 -I -B $T/check_frozen_addendum_c4v002.py --prereg <sealed prereg> --frozen <CLAUDE2>/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md --covered-later A102,A103` | a cited entry missing; a duplicate heading; a copy that is not the FROZEN file or not at path_to_be; the prereg's own sha in the frozen text; an entry-table row missing, repeated or re-hashing differently; any entry after the last cited one (r5: A101) with neither a table row nor a listed note |
| B2a | `python3 -I -B $T/print_driver_build_record_c4v002.py --reviewed <reviewed compare> --reviewed-sha <its sha> --check-record <driver check record of record> \| python3 -I -B -c "import sys; open(sys.argv[1], 'x').write(sys.stdin.read())" <DRIVER_BUILD_R5 record path>` | a check record the compare does not admit for this build, or a defective JSON check record |
| after B4 | `python3 -I -B $T/check_slot_fill_c4v002.py --slots <slots.json> --prereg <sealed prereg> --text-of-record <prereg r5> --text-of-record-sha <r5 sha from root's ruling>` | everything in the table above that tool 3 owns |
| after B5 | `python3 -I -B $T/check_sealed_compare_c4v002.py --reviewed <reviewed source> --sealed <sealed compare> --slots <slots.json> --prereg <sealed prereg>` | a non-pin line; a pin not equal to its slot or assigned twice; a pin slot that is not {path, sha256}; a cited addendum whose bytes are not PIN_ADDENDUM_V005 |
| B7 | `python3 -I -B $T/build_seal_record_c4v002.py --slots … --prereg … --text-of-record … --text-of-record-sha … --frozen … --covered-later A102,A103 --reviewed … --sealed-compare … --gates-only-output <outdir>/GATES_ONLY.json --validity-only-output <outdir>/VALIDITY_ONLY.json --key-equivalence-map K.json --new-item-list N.json --successor-custody Z.json --b2-record <B2 record of record>` | everything above (it runs tools 1–3), plus the B6/B7/B2 rules. On PASS it prints the record; its sha goes to stderr. |
| B8 | `python3 -I -B $T/build_seal_record_c4v002.py --check-admission-config <ROOT_SEAL_ADMISSION_V001.json> --seal-record <SEAL_RECORD.json>` | a config that does not pin this SEAL_RECORD, its prereg, compare and BUILD_V007, or whose producer_allowlist is not exactly BUILD_V007's 15 sources naming the record's launcher and guard (each verified from bytes and listed literally in the BUILD) |

Root creates each printed record with exclusive create (`open(…, 'x')`) and compares the written file's sha256 with the one printed on stderr.

**`--covered-later` (D-05).** Give every entry after the prereg's last cited entry up to the freeze, one by one, plus any table row whose section no longer re-hashes. r5 cites A47–A101. If the freeze comes after A103 and nothing in A82–A101 changed, the list is `--covered-later A102,A103`. If A99's section had also changed, it is `--covered-later A99,A102,A103`. A bare `A82` is now refused (`COVERED_LATER_IS_CITED`, `UNCOVERED_LATER_ENTRY`). Each listed entry becomes a seal-record note. A changed row's note carries both section shas.

**Text of record.** `TEXT_OF_RECORD_SHA` in tool 3 is `PENDING_PREREG_R5_TEXT_OF_RECORD`, because prereg r5 (`3245899f`, FROM_CLAUDE4/0103) is not yet ruled the text of record. Until a pin-only successor sets it, root states the sha with `--text-of-record-sha`. It must be the file's bytes, and the SEAL_RECORD records `text_of_record_pinned_by: ROOT_ARGUMENT`. Without the argument, tool 3 refuses `TEXT_OF_RECORD_PIN_PENDING` (a gap) and still checks every other layer. A wrong text is refused by content too: r4, for example, lacks the case block, BUILD_V007 and the entry table.

## Forms the tools expect

- **Sealed prereg:** the text of record (prereg r5) with each `seal_slots.<k>.value` replaced by the slot value. The one exception is the BUILD_V007 sha fill above. `binding_inputs.case_block` is text and is already pinned there.
- **Slot JSON**, schema `UNT_V007_SEAL_SLOTS_C4V002`. All keys are required. These are the v001 keys plus two:
  - `cascade_map_r5_addendum`: {path, sha256} under r5 (the immutable inventory addendum, named `CASCADE_MAP_R5_ADDENDUM*`, naming the r5 cascade map sha), or `NOT_APPLICABLE_R6` under r6;
  - `admission_entry`: {launcher: {path, sha256}, guard: {path, sha256}}, exactly the bound plan's launcher and guard.
  - Unchanged: `driver_branch` r5; `ngc_gas_M_s` 96 (A81 RI-23 not triggered; Codex1 0032); `cache_directory_r6_only` `NOT_APPLICABLE_R5`; `frozen_addendum` at path_to_be; and the other pins as in v001.
- **Sealed compare:** as in v001. It is the reviewed source with exactly the five pin lines changed (A82).
- **Driver BUILD record:** tool 5's bytes. In my run, with r12 and CHECK.md `89a6de88`, they hash to `25b4ff697748ae23c0d1322228c8bdd689b4b378a70035ab89f5de03b2ba79fb`. Root prints and creates its own.
- **B7 JSON forms** (DECLARED by these tools; the producers are root's):
  - key map: `{"schema": "UNT_V007_SEAL_KEY_EQUIVALENCE_MAP_C4V002", "key_equivalence_map": [ {pointer, absent_equivalent_value, b0_identity_evidence}, … ], "note"?}`. It equals the case block's map, so for CASE_BLOCK_V007_C4V001 it is `[]`.
  - NEW items: `{"schema": "UNT_V007_SEAL_NEW_ITEM_DISPOSITIONS_C4V002", "compare_impl": {path, sha256}, "items": [ {"id": "NEW-<n>", "disposition": "ADOPTED"|"REJECTED", "reason": str, "must_fail_tests": [str, …]} ], "note"?}`. The IMPL must name the reviewed source sha in full. An ADOPTED item names its MUST_FAIL tests. No id repeats.
  - raw successor custody: `{"schema": "UNT_V007_SEAL_RAW_SUCCESSOR_CUSTODY_C4V002", "identity_run": "Z2", "driver_sha256": <driver slot>, "stages_total": n, "stages_successor": n, "verdict": "PASS", "method": str, "evidence"?: [ {path, sha256} ], "note"?}`. The evidence pins are verified from bytes, and the check itself is root's (A59).

## Fence for lane runs: `tools/fence_c4v002.py`

It is the exact copy of `fence_c4v001.py` (`f813c430`) with only two read-only exceptions. The diff is `out/FENCE_C4V001_TO_C4V002.diff` (`2dad9dcfce5636ea108ea03a2a2970e1198a4b9303f96efb4b69206fb4e4a097`): 3 lines replaced, 25 added (comments, 3 constants, 2 predicates).

- **(a)** A `uvt_*.py` source module (basename with lowercase `uvt_` and `.py`, no `uvt_*` directory component) outside both runs_ext roots. A `.pyc`, an uppercase `UVT_*.py`, a file inside a `UVT_*` directory, and anything under runs_ext stay refused.
- **(b)** The root decision files `CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md`, in exactly that folder, by literal and resolved path. Scratch copies inside the fence's folder were already readable.

Every other block is unchanged: process creation, kill, network, deletes, writes outside the folder, runs_ext, the C5H name, target words and other NGC3198 data.

`tools/run_fenced_c4st2.py` checks the fence sha, runs the v001 selftest (8/8) and 15 v002 exception probes (3 reads allowed, 12 refusals), then runs the script. It prints the BLOCKED list after the selftests: **[] in every run here.**

## Tests

`r2/tests/test_seal_tools_c4v002.py`, run inside the fence: **148/148** (NEW 96/96, PORT 39/39, PORT_CHANGED 1/1, REAL 12/12).
- Run folder: `r2/tests/run_20261018T212903Z`.
- Record: `TEST_RESULTS_C4V002.json` `6de5ab43119b2371e6941ba3ab56ae7ea70f8cdd57a2c59e1678be2948e6b639`.

What the suite covers:
- **PORT:** the 40 v001 cases, ported. One has a changed expectation: r6 with an empty cache directory now refuses `DRIVER_BUILD_NOT_THE_BRANCH`, because the slot's driver BUILD record is r5 (A96). The cache rule itself still passes.
- **NEW:** one or more MUST_FAIL cases for each fix.
- **REAL:** positives on the real records. These are DOUBLING `ea48ac2b`, CHECK.md `89a6de88`, the A92 identity records, the real certificates, r12 itself, the B2 record of record `915fbcda`, and the real BUILD_V007 `94bc05a5` with a plan bound by the real binder from template V011. The real guard v008 `admission()` accepts the config built from the v002 record. The landed prereg r5 `3245899f` also reads compatibly: tool 1 re-hashes its 20 rows, and tool 3 refuses only for the frozen path, because the frozen copy of record does not exist yet.

The r1 suite at the top level ran 139/139 (`tests/run_20261018T212152Z`).

## Files (sha256 from bytes)

| file | role | sha256 |
|---|---|---|
| `r2/seal_common_c4v002.py` | r2 (of record) | `f41b0fca51a95387577839e52308a2dc6ccb79b1e6b9283f389b54c7f348dc10` |
| `r2/check_frozen_addendum_c4v002.py` | r2 (of record) | `06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891` |
| `r2/check_sealed_compare_c4v002.py` | r2 (of record) | `aebb7b731a800e558b13a5f290c7fac062183cb9ba092af45df4e6bda1f390cf` |
| `r2/check_slot_fill_c4v002.py` | r2 (of record) | `806733fb18e167275a1de62ebc9433fecf632cc16393933801fd4c9e53cddffb` |
| `r2/build_seal_record_c4v002.py` | r2 (of record) | `4192983d262e2a27a3d9c90681b6ee66a90c901bfe2f99a7dce2349bc8c5de52` |
| `r2/print_driver_build_record_c4v002.py` | r2 (of record) | `fde0b26e7ea26d4ad15213cc9c3115a807179616e0e155037c97d2179db7a673` |
| `r2/tests/test_seal_tools_c4v002.py` | r2 (of record) | `8c677fdb204ad62cd86a79e441115d0ba45559d83a6745b7cef33158d51b704d` |
| `r2/tests/run_20261018T212903Z/TEST_RESULTS_C4V002.json` | r2 (of record) | `6de5ab43119b2371e6941ba3ab56ae7ea70f8cdd57a2c59e1678be2948e6b639` |
| `seal_common_c4v002.py` | r1 (superseded by r2) | `db6423785f3ca48d9d3473d13758f62fa735a342fc39c91082f265b1bc834b8d` |
| `check_frozen_addendum_c4v002.py` | r1 (superseded by r2) | `06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891` |
| `check_sealed_compare_c4v002.py` | r1 (superseded by r2) | `aebb7b731a800e558b13a5f290c7fac062183cb9ba092af45df4e6bda1f390cf` |
| `check_slot_fill_c4v002.py` | r1 (superseded by r2) | `cf8492700d533be971a9378ce8219549ab66480f421b53165693331e553ba72e` |
| `build_seal_record_c4v002.py` | r1 (superseded by r2) | `60de881fd17f0d47fc5694ad1a65532588884db6618c167a3cd61a3329c61b89` |
| `print_driver_build_record_c4v002.py` | r1 (superseded by r2) | `224ea8290e1997fbc3a78e5edd9952ba1834ee5dbcb94c98b9990de3ca75d7eb` |
| `tests/test_seal_tools_c4v002.py` | r1 (superseded by r2) | `5e0806b1246a7e70d0094f633ea7ed57ce07ee84ab57b4df1f7ed06723212d54` |
| `tools/fence_c4v001.py` | fence / tools | `f813c43099cfdadd3a779e395d223887d0df7cd8c8a8eb67b3a73de86eb699f0` |
| `tools/fence_c4v002.py` | fence / tools | `c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5` |
| `tools/make_fence_c4v002.py` | fence / tools | `a108c8ac718e0468a3ccc211f700c8950102aa3ea94d4867bb3f0efe7d551803` |
| `tools/run_fenced_c4st2.py` | fence / tools | `fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25` |
| `tools/xwrite_c4st2.py` | fence / tools | `4fc279a3b1c6c5bcfd180c587b111d47266c5e7366c6d27c002c681229e10326` |
| `out/FENCE_C4V001_TO_C4V002.diff` | evidence | `2dad9dcfce5636ea108ea03a2a2970e1198a4b9303f96efb4b69206fb4e4a097` |
