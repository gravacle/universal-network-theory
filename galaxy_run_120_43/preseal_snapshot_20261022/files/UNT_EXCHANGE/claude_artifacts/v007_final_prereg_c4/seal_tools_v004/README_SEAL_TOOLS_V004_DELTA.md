# seal_tools v004: tool 4 takes root's manual disclosures and binds them into the SEAL_RECORD (Claude4; A110, dispatches 0646 and 0647)

UTC 2026-10-19T01:58:55Z (`date -u`). **This is a delta README.** Read it together with `../seal_tools_v003/README_SEAL_TOOLS_V003.md` (`8601211723b352a9498fa4cb8d3dc4b64d30b7451c400c89230e5d13cd909ea0`), which still describes tools 1, 2, 3 and 5, seal_common, D-05, B8 and the run order. Only what changed is described here.

**Authority.**
- Dispatch 0646 (`f6306587c6fe5b104745e677b3d28033b35f8e1238c6718e419f186ab5b17068`).
- Root entry A110 in `CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` (`43d4562b4fce53cf7bc0ea101af2792b8669689cbbddf882882e1ac4a14cbb0c` when read for this build). A110 rules route 2: tool 4 v004 gets a byte-pinned, strict-schema input that it embeds verbatim, and nothing else changes.
- Codex1 0114, finding C3V007-DISCLOSURE-01 (`39b336645e628f2a432fc8df4dc6369d1e338b212550b23df56aeb8d87088f64`).
- Claude4 0121, the design (`7d79931018541229ace05bfd08297d661cef67e1d55d10b8b8f62646225f45ee`).
- Dispatch 0647, root's file and its schema (`f9e9680b526d050512f65ddec3a4080ea650a18eceae74fc917787ef583ff5c6`), with Claude4's ack 0122.

**What this folder holds.**
- The tool set of record is the six `*.py` files at the top level:
  - **five byte-identical copies of v003** (same names, same shas): `seal_common_c4v003.py` and tools 1, 2, 3 and 5;
  - **tool 4, `build_seal_record_c4v004.py`**: v003's tool 4 (`de0ceb15`) plus the one new input.
- Tests: `tests/test_seal_tools_c4v004.py` and its final run, `tests/run_20261019T015236Z/`.
- `DELTA_V003_TO_V004.md` lists every changed line, with its reason, for tool 4 and for the tests.
- `tools/` holds the fence and runner (byte copies of v003's) and the build helpers.
- `dev/` holds work copies only; nothing there is of record.
- **There is no SELECTED file yet.** Per Claude4 0121, `SELECTED_SEAL_TOOLS_V004_C4V001.json` follows the refuter's verdict.

## What v004 changes

| item | change | where |
|---|---|---|
| A110 | **One new input:** `--manual-disclosures <path> --manual-disclosures-sha256 <hex>`, or `manual_disclosures=(path, sha256)` in the API. It is root's `SEAL_MANUAL_DISCLOSURES_V001` file. **It is required**: without it, tool 4 refuses `MANUAL_DISCLOSURES_REQUIRED`. | tool 4 |
| A110 | The file is checked before tools 1-3 run. It is pinned, read once, and those bytes are parsed by v003's strict JSON and checked against the exact schema below. | tool 4 |
| A110 | **Just before the record is built**, the file is re-read. The build refuses `MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK` unless the bytes still hash to the pin. | tool 4 |
| A110 | The SEAL_RECORD carries the file verbatim as `manual_disclosures` = {`pin` {path, sha256}, `content` (the parsed file), `raw_text` (its exact text)}. It sits next to `disclosures`, the derived prereg disclosures, which are unchanged. | tool 4 |
| A110 | The record schema becomes `UNT_V007_SEAL_RECORD_C4V004`, because its content changed (as v003 renamed it for D-05). So the v004 admission check refuses a v003 record (`ADMISSION_SEAL_RECORD_SCHEMA`), which has no manual disclosures (TESTED). | tool 4 |
| rename | Tool 4's own names follow its file: `build_seal_record_c4v004`, `check_admission_config_c4v004`. It still imports `seal_common_c4v003`, `check_slot_fill_c4v003` and `check_sealed_compare_c4v003`, whose v003 bytes sit beside it. | tool 4 |

Nothing else changes. Tools 1, 2, 3 and 5, seal_common, the B6/B7/B2/D-05/B8 rules and the admission check are v003's, apart from the record schema name.

## The input: `SEAL_MANUAL_DISCLOSURES_V001`

### The pin

The pin is (path, sha256): an **absolute** path to a **regular file** (a symlink that resolves to one is accepted, as in v003) whose bytes hash to the given sha.
- The bytes are read **once**, and those bytes are the ones hashed and then parsed.
- In the CLI, giving one flag without the other is a half pin and refuses `MANUAL_DISCLOSURES_PIN_MISMATCH`.
- **Giving neither flag** refuses `MANUAL_DISCLOSURES_REQUIRED`.
- **A pinned path with no file** refuses `MANUAL_DISCLOSURES_PIN_MISMATCH` ("not a regular file"), as v003 treats a missing dispositions path.

### The parse

v003's `strict_json_typed` with the prefix `MANUAL_DISCLOSURES`:
- the bytes must be UTF-8 text (a byte-order mark is a syntax error);
- native integers;
- no text fallback.

### The form (exact)

| key | rule | refusal |
|---|---|---|
| (the file) | a JSON object with **exactly** the keys `schema`, `e_r6_1_text`, `c08_table`, `c08_confirmation`, `root_disclosures` | `MANUAL_DISCLOSURES_SHAPE`, `MANUAL_DISCLOSURES_KEYS` |
| `schema` | `SEAL_MANUAL_DISCLOSURES_V001` | `MANUAL_DISCLOSURES_SCHEMA` |
| `e_r6_1_text` | non-empty after strip, and **equal to `E_R6_1`** (below) | `MANUAL_DISCLOSURES_E_R6_1_TEXT_EMPTY`, `MANUAL_DISCLOSURES_E_R6_1_TEXT_MISMATCH` (the detail gives both lengths and the first differing character) |
| `c08_table` | a non-empty list of rows | `MANUAL_DISCLOSURES_C08_TABLE_SHAPE` |
| a `c08_table` row | keys `new_item_id`, `file`, `line`, plus `declared_in_r13` if given, and no others: `new_item_id` is `NEW-` and 1 to 3 ASCII digits; `file` is a non-empty string; `line` is an integer > 0 (not a bool); `declared_in_r13` is `true` or `false` | `MANUAL_DISCLOSURES_C08_ROW` |
| `c08_table` ids | each `new_item_id` once (A71) | `MANUAL_DISCLOSURES_C08_DUPLICATE_ID` |
| `c08_confirmation` | non-empty after strip | `MANUAL_DISCLOSURES_C08_CONFIRMATION_EMPTY` |
| `root_disclosures` | a non-empty list (A110.3 names the disclosures root carries) | `MANUAL_DISCLOSURES_ROOT_DISCLOSURES_SHAPE` |
| a `root_disclosures` row | **exactly** `id`, `source`, `text`, each non-empty after strip | `MANUAL_DISCLOSURES_ROOT_DISCLOSURE_ROW` |
| `root_disclosures` ids | each `id` once (A71) | `MANUAL_DISCLOSURES_ROOT_DISCLOSURE_DUPLICATE_ID` |
| every string | has a UTF-8 form (no lone surrogate), checked once the form holds | `MANUAL_DISCLOSURES_TEXT_ENCODING` (typed, not `INTERNAL_EXCEPTION`) |

Root's file `seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json` (`b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6`) passes, and it is carried verbatim (TESTED, API and CLI). It has 19 C-08 rows (NEW-4 to NEW-73, each `declared_in_r13: false`) and five root disclosures: A100_B2_SANITY, A101_B2_DOC_ERRATUM, A105_E_OPS5, A107_P12 and A111_P3_P4.

**Choices beyond the brief's minimum.** Each is stricter, and none refuses root's file (TESTED):
- the NEW-id form;
- a non-empty `file`;
- unique C-08 ids;
- a non-empty `root_disclosures`;
- the typed UTF-8 check.

`declared_in_r13` is **optional**, because 0646 names three row keys. Claude3's c3v017 pre-check requires it; root's file carries it in every row.

**What the tool does not judge.** It checks the form and E_R6_1 only. Whether the C-08 table matches the r13 source lines, and whether root's texts match A100, A101 and A105, are root's manual C-08 check and Claude3's and Codex1's cross-checks (0646, 0647).

### `E_R6_1`

`E_R6_1` is a constant in tool 4. It was generated by `tools/make_tool4_c4v004.py` from the bytes of `v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json` (`7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0`), key `basis.erratum_E_R6_1`:
- 469 ASCII characters;
- the sha256 of its UTF-8 bytes is `c28202b0909371f43180ca832e4652f3d835a977852cde5c261842315deb33f4`.

The generator checked the literal by AST after writing it, and the suite re-reads the SELECTED file (strict parse, sha-verified) and asserts that the constant equals `basis.erratum_E_R6_1` byte for byte (TESTED). The comparison is on the parsed strings, which is UTF-8 byte equality of the text; a JSON escape that spells the same text is equal.

## The SEAL_RECORD (tool 4)

Schema `UNT_V007_SEAL_RECORD_C4V004`. Every v003 field is unchanged. One field is new:

```json
"manual_disclosures": {
 "content": {"c08_confirmation": "...", "c08_table": [...], "e_r6_1_text": "...", "root_disclosures": [...], "schema": "SEAL_MANUAL_DISCLOSURES_V001"},
 "pin": {"path": "<the path root gave>", "sha256": "<the sha root gave, the sha256 of the file's bytes>"},
 "raw_text": "<the file's exact text; its UTF-8 bytes are the file's bytes>"
}
```

The record is canonical JSON, as in v003 (sorted keys, indent 1, trailing newline), so `content` is re-serialized with sorted keys, while `raw_text` is the file byte for byte. The verdict on stderr lists `pins_verified.manual_disclosures` and notes `MANUAL_DISCLOSURES_VERIFIED`.

**Order inside a build:**
1. The manual disclosures check (the pin, the read, the parse, the form).
2. Tools 1-3, then v003's B6, B7 and B2 checks and its derived disclosures.
3. The dispositions re-read.
4. The manual disclosures re-read.
5. The record.

Every refusal of steps 1-2 is reported together, D-08 style (TESTED with a PENDING slot). A refusal prints no record.

**Readers of the record schema.** Guard v008 `admission()` and launcher v007 read `sealed_by`, `prereg`, `compare`, `driver` and `frozen_addendum`, not the schema. Claude3's c3v017 `check-tool4` reads the verdict, the sha and `sealed_by` (source reading, FORMAL). The real guard v008 and launcher v007 accept the v004 record (TESTED, ported integration cases).

## When root runs tool 4 (the README_SEAL_TOOLS_V003 order is unchanged)

Set `T=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004`. Tools 1, 2, 3 and 5 can run from either folder, since the bytes are identical. The other placeholders are as in the v003 README.

**B7, build the record.** These are v003's flags plus the two new ones, with root's file of record:

```sh
python3 -I -B $T/build_seal_record_c4v004.py --slots <slots.json> --prereg <sealed prereg> --text-of-record <prereg r6 text of record> --text-of-record-sha <its sha> --frozen <CLAUDE2>/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md --addendum-at-text-of-record <r6>/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md [--dispositions <D.json> --dispositions-sha <its sha256>] --reviewed <reviewed compare> --sealed-compare <sealed compare> --gates-only-output <outdir>/GATES_ONLY.json --validity-only-output <outdir>/VALIDITY_ONLY.json --key-equivalence-map <K.json> --new-item-list <N.json> --successor-custody <Z.json> --b2-record <B2 record of record> --manual-disclosures /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json --manual-disclosures-sha256 b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6 | python3 -I -B -c "import sys; open(sys.argv[1], 'x').write(sys.stdin.read())" <SEAL_RECORD path>
```

On PASS the record goes to stdout and the verdict, with `seal_record_sha256`, to stderr. A refusal prints nothing on stdout and exits 2. Root compares the written file's sha256 with the one on stderr, as before.

**B8, the admission check:**

```sh
python3 -I -B $T/build_seal_record_c4v004.py --check-admission-config <ROOT_SEAL_ADMISSION_V001.json> --seal-record <SEAL_RECORD.json>
```

This is v003's check, on the v004 record schema.

**API.** `safe_build(a)` with `a.manual_disclosures = (path, sha256)`. The other attributes are as in v003. The record-only helpers are `manual_disclosures_codes(chk, pin)`, `manual_disclosures_form_codes(chk, obj)` and `manual_disclosures_record(chk, checked)`.

**Wiring note for the seal script (Claude3's c3v008):**
- Only `--main` changes, to `build_seal_record_c4v004.py` and its sha.
- Tool 4 v004 imports the v003 module names. Their bytes are unchanged, so the `--module` pins (`check_frozen_addendum_c4v003`, `check_sealed_compare_c4v003`, `check_slot_fill_c4v003`, `seal_common_c4v003`) keep their v003 shas. The files exist in this folder, and also in v003's.
- The step-10 flags are exactly `--manual-disclosures "$DISCLOSURES" --manual-disclosures-sha256 "$DISCLOSURES_SHA"`. This matches README_SEAL_ASSEMBLY_C3_c3v008, by source reading.
- A check that the record carries the file verbatim needs `manual_disclosures.raw_text`, encoded as UTF-8, to equal the pinned file's bytes, and `manual_disclosures.pin` to equal the pin.

## Fence

`tools/fence_c4v002.py` (`c993d34c`) and `tools/run_fenced_c4st2.py` (`fe904509`) are byte copies of v003's, made by exclusive create. The fence takes its review root from its own location (this folder). Every run here showed a selftest of 8/8, exception probes of 15/15, and an empty BLOCKED list after the selftest.

Process note (FORMAL, from the runner and fence source; unchanged from v003): each runner start reads the first 64 bytes of the open V005 and frozen V004 root-decision addenda and of one `uvt_*.py` source outside runs_ext (fence exception probes). Its selftest also lstats nonexistent probe paths under CLAUDE2/runs_ext and `UVT_probe_should_not_exist` before refusing them. No probe touches `runs_ext/KMAX_A2F10_C5H_RUN_V001` or any existing UVT path.

## Tests

`tests/test_seal_tools_c4v004.py` (`ee237685e24d6efd799f441a4e7340009e1bc65064f86b62d5be6071dfa417e8`) was run from `tests/` inside the fence. Result: **467/467**.

| tag | count | meaning |
|---|---|---|
| PORT | 309/309 | v003's call and expectation |
| PORT_CHANGED | 43/43 | v003 cases that call the builder, whose base arguments now carry MD0 |
| NEW | 101/101 | MUST_FAIL cases |
| NEW_CONTROL | 8/8 | positive controls |
| REAL_NEW | 6/6 | root's real file and r6's SELECTED file |

- Run folder: `tests/run_20261019T015236Z/`.
  - Record: `TEST_RESULTS_C4V004.json` (`f6b664c09e21e7201d4c0e7fdfeb0cd1af9a085ddc981d98f5ebc5963e271d7c`).
  - The fenced runner's output: `RUN_LOG_FENCED_C4V004.txt` (`597d47d254a17be34c84bdffe3998eda2c02600e8e8662045835084f799a9c9f`).
- **The port.** The v003 suite (352/352, `TEST_RESULTS_C4V003.json` `26bb912f`) runs unchanged, in order, against this folder.
  - The port map checks every v003 case once, in order, with v003's tool, tag, r2 index, expectation and text: **352/352, no problems**.
  - Four texts that named the v003 record or admission check now say v004 (`V4_RENAMES`).
  - The 43 PORT_CHANGED cases are exactly the cases that call the builder: v003 indexes 241-266, 268-280, 282, 283, 320 and 344. They are detected by counting builder calls. Each case gives its reason, and the genuine build also expects schema C4V004.
  - v003's own r2 port map still holds (148/148).
  - The base fixture MD0 (`manual_disclosures_001/SEAL_MANUAL_DISCLOSURES_SYNTH_C4V004.json`, `bf1ac145c45a4baa54460fe179916d4f493b54fa7f0e0618d9e0e9a8511d066c`) is SYNTHETIC, in root's form. Its `e_r6_1_text` is read from SELECTED_R6_C4V001's bytes.
- **New cases (115):**
  - **The unchanged files:** the five copies are v003's bytes and are the modules the suite imports; no v003 tool 4 is in this folder.
  - **E_R6_1:** the constant equals the SELECTED text.
  - **Root's real file b9db6fd1,** API and CLI:
    - it is accepted, and the record carries it verbatim (`raw_text` equals the file's bytes, and the content equals its strict parse);
    - the API and CLI records are byte-equal;
    - that record passes the v004 admission check and the real guard v008 `admission()`.
  - **A record in v003's form** refuses the v004 admission check.
  - **Rows without `declared_in_r13`,** and with `true`, pass.
  - **One build opens the file exactly twice:** the checked read and the re-read.
  - **MUST_FAIL, each refusing with exactly its own code and no record:**
    - **No pin:** API `None`, the v003 argument form, no CLI flags.
    - **The pin:** a missing file, a wrong sha, a capital sha, another file's sha, a short sha, a relative path, a directory, a bare path, a dict pin, half pins (API and CLI), a three-element pin.
    - **The parse:** duplicate keys (top level, in a C-08 row, in a root disclosure), NaN, -Infinity, a 5,000-digit integer, a duplicate key behind one, truncation, trailing data, UTF-16, a BOM, deep nesting.
    - **The shape and keys:** a list or a string as the file, an extra key, missing keys, `{}`.
    - **The schema:** V002, lower case, null.
    - **E_R6_1:** empty, whitespace or null; another text; nine one-character or look-alike differences (including U+201C, a non-breaking space and U+2026); and a SYNTHETIC copy of root's file ending "erratum!".
    - **The C-08 table:** empty, an object, null.
    - **C-08 rows (22 cases):** missing or extra keys; `line` 0, negative, `"7"`, `true`, `7.0` or null; bad ids (not a string, `NEW71`, a newline, fullwidth digits, four digits); an empty, whitespace or non-string `file`; `declared_in_r13` as `"false"`, 0 or null.
    - **Duplicates:** a C-08 id twice; a root-disclosure id twice.
    - **`c08_confirmation`:** empty, whitespace, a list.
    - **`root_disclosures`:** an object or an empty list; 8 bad rows.
    - **Encoding:** lone surrogates in three fields.
    - **A change after the check,** at two points: bytes appended while tools 1-3 run, and in the last step before the re-read. A control with both patches removed passes and prints the genuine record.
    - **Layered reporting:** a bad pin together with a T3 refusal.
    - **The CLI:** a repeated flag (`CLI_REPEATED_FLAG`) and an abbreviated flag (`CLI_ARGUMENTS`). The `=` forms pass.

## TESTED / FORMAL / UNTESTED

**TESTED (fenced suite, 467/467):**
- every case above;
- the v003 suite ported unchanged against v004;
- byte-exact carriage of MD0 and of root's real file into the SEAL_RECORD;
- the re-read refusal;
- the CLI exit codes and the stdout/stderr split;
- the v004 record under the v004 admission check and under the real guard v008 `admission()` and launcher v007 `validate()` (CONFIG and REGISTERED patched to synthetic files; nothing started).

**TESTED from bytes:** the five copies, the fence and the runner hash to v003's pins. Tool 4 v004 and the tests are reproduced byte for byte by `tools/make_tool4_c4v004.py` and `tools/make_tests_c4v004_r2.py`.

**FORMAL (source reading):**
- guard v008, launcher v007 and Claude3's c3v017 helper do not read the SEAL_RECORD schema;
- c3v008's README passes exactly the two new flags;
- the runner's probe reads (above).

**UNTESTED:**
- the real seal, the real SEAL_RECORD and the real admission config;
- Claude3's c3v008 wiring of tool 4 v004;
- whether root's C-08 table matches the r13 source lines, and whether its disclosure texts are adequate (root's and the reviewers' checks);
- the independent refuter and Codex1's delta (both pending);
- a mutation run for v004 (not done in this build).

**Never done:** nothing was launched; no compare was run; `--validity-only` was never used; no runs_ext, C5H or UVT path was read, listed or stat'ed (beyond the fence probes above; one listing of the CLAUDE2 control folder, made to find the V006 addendum, showed the runs_ext symlink entry itself, and nothing under it was touched); no target or observed-velocity data was opened (the CLAUDE2 V006 root-decision addendum, a decision record as fence exception (b) classes it, was read as authority); no recursive content search was used. v003, root's disclosures file and every author file were only read. Writes were exclusive creates in this folder.

## Files (sha256 from bytes)

| file | role | sha256 |
|---|---|---|
| `build_seal_record_c4v004.py` | tool 4 v004 (builder, admission check) | `9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41` |
| `seal_common_c4v003.py` | shared helpers (v003 bytes) | `101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21` |
| `check_frozen_addendum_c4v003.py` | tool 1 (v003 bytes) | `a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4` |
| `check_sealed_compare_c4v003.py` | tool 2 (v003 bytes) | `c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1` |
| `check_slot_fill_c4v003.py` | tool 3 (v003 bytes) | `316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af` |
| `print_driver_build_record_c4v003.py` | tool 5 (v003 bytes) | `e5bedffe3c91650d5dba7fbd1ed5476e228158679d8959dfea0e2eff436ebdea` |
| `tests/test_seal_tools_c4v004.py` | tests | `ee237685e24d6efd799f441a4e7340009e1bc65064f86b62d5be6071dfa417e8` |
| `tests/run_20261019T015236Z/TEST_RESULTS_C4V004.json` | final run record | `f6b664c09e21e7201d4c0e7fdfeb0cd1af9a085ddc981d98f5ebc5963e271d7c` |
| `DELTA_V003_TO_V004.md` | every changed line, with its reason | `6e52ebd5c3040bcafc00efc6d2ddbbd0c680dfb1c7c26d7aaa5001adea952867` |
| `tools/fence_c4v002.py` | fence (v003 copy) | `c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5` |
| `tools/run_fenced_c4st2.py` | fenced runner (v003 copy) | `fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25` |
| `tools/make_tool4_c4v004.py` | generator of tool 4 v004 (from v003's bytes and r6's SELECTED) | `a33da974763b3627c5f321b235c1de78e9eeb24fb429c88e8d9c3f81e44f8062` |
| `tools/make_tests_c4v004_r2.py` | generator of the tests (from v003's bytes) | `82a8794bd026d22ce5b202297d89e2f6fde21a2325c214b8fdcf5f07088dec6d` |
| `tools/make_delta_c4v004_r3.py` | DELTA generator | `32711ba18652c3281e90e09be4501f4dd2cf9e695f7d2b30677531901d509e46` |
| `tools/make_readme_c4v004.py` | fills the shas of this README from bytes | `153359b3899c42a4c5ba2c5c971e981eec6d9618616b8cc2b70b5b031ff06b06` |
| `tools/make_tests_c4v004.py`, `tools/make_delta_c4v004.py` | superseded helpers. Each refused before writing anything: one on an anchor that occurred twice, one on unused reasons. | `2d1fe08519313aeda12b09ce34e2afb20ee8e26f819a0b0110a8d83406756525`, `49e8bea5e7c1d33ba382fe553186ffca789b4f7699bd5009dfdc63ff8eb0821d` |
| `tools/make_delta_c4v004_r2.py` | superseded DELTA generator (wrote one dev dry run) | `7e0bb9b2596009cde6341d28ebf088c5aacdb510763636a3c55c6a974ac2cb63` |

`HASHES_SEAL_TOOLS_C4V004.txt`, written last, lists the sha256 of every file in this folder, the final run folder and `dev/` included (dev marked "not of record").
