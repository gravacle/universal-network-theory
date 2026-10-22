# seal_tools v003: root-side V007 seal checks (Claude4; D-05 dispatches 0633 and 0640 with C-01; B8 and the README note dispatch 0634; A104-A106)

UTC 2026-10-19T00:09:34Z (`date -u`). Successor of `../seal_tools_v002/r2/` (README `da29c008`, 148/148). **The tool set of record is the six `*_c4v003.py` files at the top level of this folder**, with `tests/test_seal_tools_c4v003.py` and its final run under `tests/`. The scope is A106.2, option (b): D-05 with C-01, B8, this README's parser note, the W7-S1 MUST_FAIL cases, and r13 as a reviewed-compare fixture (A104). Nothing else changed. C-02 to C-06 (and C-03, C-08 if each is quick) go into Claude3's seal script (A106.2). `DELTA_V002R2_TO_V003.md` lists every changed source line against r2, each with its reason. `dev/` and `mutants/` hold work copies only, and nothing there is of record. The SELECTED file is written by the Claude4 main loop after the refuter (FROM_CLAUDE4/0110), not by this build.

Five small scripts that root runs at seal assembly. **Each one only reads and checks.** None writes a file, starts a process or touches the network. The SEAL_RECORD builder and the driver-BUILD-record printer print bytes; root creates the files. Every JSON input is parsed strictly, and a duplicate key refuses (A71). The command line refuses abbreviations and repeated flags. Run them with the pinned isolated Python: `python3 -I -B <script> ...`. A verdict JSON goes to stdout (stderr for tools 4 and 5). Exit 0 means PASS, exit 2 REFUSE. An unexpected exception is also a REFUSE with code `INTERNAL_EXCEPTION:<type>` (D-07), never a traceback.

Tool 3 loads the slot's reviewed compare in-process to call its own `validate_case_block`, `load_driver_build_record` and `activate_driver_build`. Importing it runs only definitions: for r12 and r13, constant assignments, `def`s, `import numpy`, `re.compile` and `math.sqrt`, and no function the tools call reaches the C5H stat or interlock helpers (Claude4's v002 check N-10: AST and call graph, FORMAL). It is compiled from the very bytes whose sha matched the slot. r13 (`f5adfd11`, the compare of record, A104) differs from r12 (`4bd7b262`) only in `check_record_codes` (its IMPL `274f7049`: 1 of 440 top-level AST nodes); both are test fixtures here. Every tool ran inside `tools/fence_c4v002.py` in the tests (see below).

## What v003 changes

| item | change | tool |
|---|---|---|
| D-05 (0633) | The bare `--covered-later` list is **removed**. A non-empty `covered_later` (API) or any `--covered-later` flag (CLI, the `=` form too) refuses `COVERED_LATER_BARE_NAMES_REFUSED` in tools 1, 3 and 4, and covers nothing. Root supplies a byte-pinned dispositions file instead (`--dispositions D.json --dispositions-sha H`), with one row per later or changed entry (below). The builder carries it into the SEAL_RECORD as `later_entry_dispositions` = {pin, content, raw_text}, replacing v002's generic `no_change_notes`, and re-reads the file first (`DISPOSITIONS_CHANGED_AFTER_CHECK`). | 1, 3, 4 |
| D-05 (0640, A104) | "Names the change" is mechanical. A changed entry is disposed `revised` (with a verified `prereg_revision` pin) or `no_change_after_change` (with a `changed_text` excerpt present in the new section bytes and absent from the old, and `why_no_prereg_effect`). Plain `no_change` is for unchanged entries only, so a plain `no_change` on a changed entry refuses (Codex1 PV-D05-1). | 1 |
| C-01 (Claude4 v002 check) | Tool 1 compares **every** entry present in both the frozen copy and the V005 bytes the text of record was written against, not only the A82-A101 table rows. An edit inside a cited A47-A81 entry such as A62 is a change and needs a disposition. Those bytes come from the prereg's `entries_after_A81.addendum_read` pin; root passes the copy with `--addendum-at-text-of-record A.md`, and tools 3 and 4 pass it through. | 1, 3, 4 |
| B8 (0634) | `--check-admission-config` also checks the SEAL_RECORD fields that guard v008 `admission()` checks: `sealed_by` equals the guard's AUTHORITY (L32), and `driver` and `frozen_addendum` are present (L39) and exact {path, sha256} pins verified from bytes (L40, `pin_check` L18). Codex3's six records now refuse, and so does the real guard (TESTED). | 4 |
| W7-S1 (A105, Claude4 0108) | MUST_FAIL tests only: an admission config with 17 rows (BUILD_V007's 15 plus the superseded writers `9fbdb0ca` and `500f8b6a`), and one with BUILD_V006's 15 rows, both refuse the B8 check. The real guard v008 admits both (TESTED), so the B8 check is the control that closes W7-S1. No source change was needed. | 4 (tests) |
| README (0634) | The A102 row no longer says that both JSON probes parse integers as strings. The parser table below says exactly which ones do. | - |
| r13 (A104) | Tests only: r13 is a reviewed-compare fixture for tools 2, 3 and 5, and for one full builder run, alongside r12. | 2, 3, 4, 5 (tests) |
| rename | Module, check and usage names `*_c4v002` -> `*_c4v003`, the in-process compare module name, and header lines naming the predecessor. Input schemas keep their v002 names because their formats did not change. The SEAL_RECORD schema becomes `UNT_V007_SEAL_RECORD_C4V003` because its content changed. Tools 2 and 5 change only by renames. | all |

## The D-05 rule (tool 1)

### The old bytes: `--addendum-at-text-of-record`

The prereg pins the V005 bytes its entry table was read from, in `entries_after_A81.addendum_read`. Prereg r5 has `{open_path, sha256_at_generation: 70a48f51…, bytes: 136359, byte_copy: "addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md …"}`. Root gives that copy to tool 1 (`--addendum-at-text-of-record A.md`, API `text_of_record_addendum=PATH`):

- the copy's bytes must hash to `sha256_at_generation`, and to `bytes` when the prereg states an integer; otherwise `ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH`;
- no copy given, or not a regular file: `ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED` (from the CLI too: a typed code, not a usage error);
- the prereg has no 64-hex `sha256_at_generation`: `ADDENDUM_READ_PIN_ABSENT`;
- every table row must be that copy's section (sha, `section_bytes` and `heading` when stated): `ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD`;
- every cited entry >= A47 must be in it (`CITED_ENTRY_ABSENT_FROM_READ_COPY`), every entry in it must still be in the frozen copy (`READ_COPY_ENTRY_ABSENT_FROM_FROZEN`), and it may not repeat a heading (`READ_COPY_DUPLICATE_ENTRY_HEADING`).

The disposition layer runs only on a verified read copy. Otherwise it is skipped (a `LAYER_SKIPPED` note), and the tool refuses on the read-copy code.

**For prereg r5:** `v007_final_prereg_c4/r5/addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md` (`70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e`). **For prereg r6** (A106, being built): per FROM_CLAUDE4/0110 it is `v007_final_prereg_c4/r6/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md`, which hashes now to the final V005 `c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1` (TESTED by sha). r6 itself was not published at this build, so running these tools on r6 is UNTESTED.

### CH and L

With R = the read copy's sections and F = the frozen copy's sections (r5 section_rule, `sections()`):

- **CH** = every entry in both R and F whose section bytes differ. This covers every cited entry >= A47 and every table row (C-01). CH also contains every table row whose `section_sha256` (or bytes or heading) is not the frozen section's, as r2 checked.
- **L** = every frozen entry after the last cited entry with no table row (as in r2), plus every frozen entry absent from R, minus CH.

L u CH empty: the dispositions file is optional, and the SEAL_RECORD carries `later_entry_dispositions: "NOT_SUPPLIED_NONE_REQUIRED"`. Non-empty: the file is required (`DISPOSITIONS_REQUIRED`, naming the entries). A missing row refuses `UNCOVERED_LATER_ENTRY` (an L entry), `ENTRY_TABLE_SECTION_CHANGED` (a CH table row) or `ENTRY_SECTION_CHANGED` (a CH entry with no table row, the C-01 case).

**As measured (TESTED, from bytes):** prereg r5's read copy `70a48f51` holds A47-A101, and none of those 55 sections differs from the final V005 `c01b3c51` (A47-A106). So for r5, CH is empty and L is A102, A103, A104, A105, A106. For r6, whose table runs to A106 against `c01b3c51`, L u CH is empty if the frozen copy equals `c01b3c51` (A106.3), and no dispositions file is needed (FORMAL; r6 UNTESTED).

### The dispositions file

Root writes it. It is byte-pinned (`--dispositions D.json --dispositions-sha H`; API `dispositions=(path, sha256)`): an absolute path to a regular file whose bytes hash to H, read once, and those bytes are the ones parsed. Otherwise `DISPOSITIONS_PIN_MISMATCH`. The bytes must be UTF-8 text (`DISPOSITIONS_JSON_ENCODING`; a byte-order mark is a syntax error), parsed by r2's strict JSON with native integers and no text fallback: `DISPOSITIONS_JSON_DUPLICATE_KEY`, `_NON_FINITE_CONSTANT`, `_INTEGER_TOO_LONG` (Python's 4,300-digit limit), `_SYNTAX`, `_VALUE_ERROR`, `_DEFECT` (for example nesting deep enough to exhaust the parser).

The object has exactly the keys `schema` (= `UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001`), `frozen_addendum_sha256` (= the frozen copy's sha) and `entries` (a list). The list holds **exactly one row per entry of L u CH**, and each row has **exactly** the keys of its disposition:

| entry class | disposition | exact keys | also required |
|---|---|---|---|
| L | `no_change` | `entry, disposition, reason, section_sha256` | `reason` not empty after strip |
| L or CH | `revised` | `entry, disposition, prereg_revision, reason, section_sha256` | `prereg_revision` is an exact `{path, sha256}` pin of an existing regular file whose bytes hash to it (Checker.pin: absolute path, 64 hex, no PENDING), and it is not the prereg under check, by resolved path or by sha; `reason` not empty after strip |
| CH | `no_change_after_change` | `entry, disposition, changed_text, why_no_prereg_effect, section_sha256` | `changed_text` is a non-empty string whose UTF-8 bytes occur in the new (frozen) section and do not occur in the old (read-copy) section; `why_no_prereg_effect` not empty after strip |

In every row, `entry` is `A<n>` (ASCII digits, no leading zero) and `section_sha256` is the **frozen** section's sha. A generic string never satisfies `changed_text`, because it fails one of the two substring tests: "no change" is not in the new bytes, and a text present in both versions is in the old bytes. The comparison is byte-exact, so an NFD spelling of an NFC excerpt fails.

Row refusals: `DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY` (PV-D05-1), `DISPOSITION_NO_CHANGE_AFTER_CHANGE_ON_UNCHANGED_ENTRY`, `DISPOSITION_ROW_KEYS`, `DISPOSITION_VALUE`, `DISPOSITION_PREREG_REVISION_REQUIRED`, `DISPOSITION_PREREG_REVISION_PIN` (the detail names the pin code), `DISPOSITION_PREREG_REVISION_IS_THE_PREREG`, `DISPOSITION_CHANGED_TEXT_EMPTY`, `DISPOSITION_CHANGED_TEXT_ENCODING` (no UTF-8 form, for example a lone surrogate), `DISPOSITION_CHANGED_TEXT_NOT_IN_NEW_SECTION`, `DISPOSITION_CHANGED_TEXT_IN_OLD_SECTION`, `DISPOSITION_WHY_NO_PREREG_EFFECT_EMPTY`, `DISPOSITION_REASON_EMPTY`, `DISPOSITION_SECTION_SHA_MISMATCH`, `DISPOSITION_ENTRY_FORMAT`, `DISPOSITION_ROW_SHAPE`, `DISPOSITION_DUPLICATE_ENTRY`, `DISPOSITION_ENTRY_NOT_IN_FROZEN`, and for a row of an entry outside L u CH, `DISPOSITION_FOR_TABLED_ENTRY` and/or `DISPOSITION_FOR_CITED_ENTRY`. File refusals: `DISPOSITIONS_SHAPE`, `DISPOSITIONS_KEYS`, `DISPOSITIONS_SCHEMA`, `DISPOSITIONS_FROZEN_SHA_MISMATCH`, `DISPOSITIONS_ENTRIES_SHAPE`. On PASS tool 1 notes `DISPOSITIONS_VERIFIED` and returns `later_entry_dispositions` = {pin, content, raw_text} and `addendum_at_text_of_record` = the read copy's {path, sha256}. A disposed CH entry is noted `ENTRY_TABLE_SECTION_CHANGED_NOTED` or `ENTRY_SECTION_CHANGED_NOTED`. A refusing run returns no verified file.

The tool checks shapes, bytes and shas. It cannot judge whether a reason is adequate, or whether a pinned file really is a revision of the prereg (Codex1 0093 makes the same point), so root and the reviewers own those judgements.

### Worked examples (templates, not root's dispositions)

The section shas below were read from the final V005 bytes `c01b3c51` with the tool's own `sections()` (TESTED). Text in angle brackets is root's to write.

**1. An L row: A102, `no_change`.** This is the prereg-r5 case, where A102 to A106 are later entries. Under prereg r6 they are table rows and need no dispositions row. FROM_CLAUDE4/0109 notes that for r5, A102 and A104 change the prereg's meaning, so an honest disposition there is `revised` (example 3); this example shows only the shape.

```json
{
 "schema": "UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001",
 "frozen_addendum_sha256": "<sha256 of CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md>",
 "entries": [
  {
   "entry": "A102",
   "disposition": "no_change",
   "reason": "<root: why A102 (r12 reviews split; r13 closes A-B1) leaves the prereg text unchanged>",
   "section_sha256": "c4b56728ded3ae292f9e26f31f0cdfa0c41516a7c836f9d5791934034a231a76"
  }
 ]
}
```

**2. A CH row: A62 edited after the text of record was written, `no_change_after_change`.** This is hypothetical: A62 has **not** changed (A62's section is `1e3bbebc12dffcb7e965fec0f99004d3969513152f25e0e84b193420447b8084` in both `70a48f51` and `c01b3c51`). If a line were added inside A62, its row would be:

```json
  {
   "entry": "A62",
   "disposition": "no_change_after_change",
   "changed_text": "<an exact excerpt of the added text: present in the frozen A62 bytes, absent from the read copy's A62 bytes>",
   "why_no_prereg_effect": "<root: why the edit does not change any prereg clause>",
   "section_sha256": "<the frozen A62 section sha (it changes with the edit)>"
  }
```

The tests use exactly this shape for a synthetic edit inside A62 (C-01): with no row the tool refuses `ENTRY_SECTION_CHANGED`; with plain `no_change` it refuses `DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY`; with a correct excerpt it passes; and with the A62 heading line (present in both versions) it refuses `DISPOSITION_CHANGED_TEXT_IN_OLD_SECTION`.

**3. A revised row** (an L or CH entry whose ruling changes the prereg):

```json
  {
   "entry": "A104",
   "disposition": "revised",
   "prereg_revision": {"path": "<absolute path of the prereg revision>", "sha256": "<sha256 of its bytes>"},
   "reason": "<root: which clauses the revision changes, and why>",
   "section_sha256": "742c7ace69df2ea2fb9fb9dab6aba37484c51544f7a956dcf67ef4d1f5622d00"
  }
```

The section shas of any frozen copy, read with the tool's own rule (`T` = this folder):

```sh
python3 -I -B -c "import hashlib, sys; sys.path.insert(0, sys.argv[1]); import check_frozen_addendum_c4v003 as T1; s = T1.sections(open(sys.argv[2], 'rb').read()); [print('A%d' % n, hashlib.sha256(s[n][0][1]).hexdigest()) for n in sorted(s)]" $T <CLAUDE2>/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md
```

### The SEAL_RECORD (tool 4)

Schema `UNT_V007_SEAL_RECORD_C4V003`. It carries:

- `later_entry_dispositions`: {`pin` {path, sha256}, `content` (the parsed file), `raw_text` (its exact text, which hashes to the pin)}, or `"NOT_SUPPLIED_NONE_REQUIRED"`;
- `addendum_at_text_of_record`: the read copy's {path, sha256}, as tool 1 verified it.

v002's `no_change_notes` are gone. Before building, the builder re-reads the dispositions file. It refuses `DISPOSITIONS_CHANGED_AFTER_CHECK` unless the bytes still hash to root's pin and to the sha tool 1 verified, the path is the one tool 1 verified, and the text and its parse equal what tool 1 returned. The v003 admission check refuses a v002 record (`ADMISSION_SEAL_RECORD_SCHEMA`). Guard v008 and launcher v007 do not read the record schema; they read `sealed_by`, `prereg`, `compare`, `driver` and `frozen_addendum` (source reading, FORMAL).

## B8: the admission check against producer guard v008 (`294cb776`)

The guard was read as source, and executed only in the fenced tests with CONFIG and REGISTERED patched to synthetic files.

| guard v008 `admission()` | v003 `--check-admission-config` | code |
|---|---|---|
| L32 `seal.get('sealed_by') != AUTHORITY` | the same equality with the same AUTHORITY | `ADMISSION_SEAL_SEALED_BY_NOT_AUTHORITY` (changed, extra key or absent) |
| L39 `driver` / `frozen_addendum` not in the seal | the same | `ADMISSION_SEAL_DRIVER_REQUIRED`, `ADMISSION_SEAL_FROZEN_ADDENDUM_REQUIRED` |
| L40 `pin_check(seal[key])` (L18: a dict, keys exactly {path, sha256}, sha of the path's bytes) | `Checker.pin`: the same, and stricter (absolute path, 64 hex, no PENDING, a regular file) | `ADMISSION_SEAL_DRIVER_PIN`, `ADMISSION_SEAL_FROZEN_ADDENDUM_PIN` (the detail names the pin code) |
| L27, L29, L30, L33-L37 | as v002 (schema and authority, launcher and guard on the allowlist, config pins, the prereg/compare binding, allowlist bytes and BUILD listing) | as v002 |

So every record the guard refuses on these three fields, the check refuses too: the check is stricter, never looser. Not mirrored, because they are runtime and outside the record: the published `UNT_ROOT_ADMISSION_SHA256` (L23-L25), the config's location beside the guard (L8, L21), and allowlist membership of producers other than the record's launcher and guard (L29).

**W7-S1.** The guard matches allowlist entries by substring in the BUILD text (L37). BUILD_V007 also names, outside its allowlist section, the superseded writers `postseal_records_cx1v006.py` (`9fbdb0ca`) and `srb_rot_record_cx1v008.py` (`500f8b6a`). So the real guard admits a 17-row config holding them, and a config holding BUILD_V006's 15 rows (TESTED here, as Claude4 0108 found). The B8 check refuses both, because the producer_allowlist must equal the SEAL_RECORD's 15-row BUILD_V007 allowlist exactly: `ADMISSION_ALLOWLIST_NOT_THE_SEAL_RECORD_ALLOWLIST`, and for the 17-row config also `ADMISSION_ALLOWLIST_COUNT_NOT_15` and `ADMISSION_ALLOWLIST_NOT_THE_BUILD_ALLOWLIST`. Root runs the B8 check before checklist step B9 (0108). Claude3's seal script builds the config from BUILD_V007's 15 rows (A105.1, 0642).

## Which parsers parse integers as strings (0634; Codex3 A102 note `c09c6c39`)

| parser | integers | used for | on a ValueError that is not a JSON syntax error (a duplicate key, a non-finite constant, a 4,300+ digit integer) |
|---|---|---|---|
| `json_or_text` (seal_common) | strings (`parse_int=str`) | the driver check record probe: tool 3 `DRIVER_CHECK_RECORD_JSON_DEFECT`, tool 5 `CHECK_RECORD_JSON_DEFECT` | refuse; only a JSON syntax error means text |
| `strict_json_bytes` in tool 3's cascade-addendum probe | native | the CASCADE_MAP_R5_ADDENDUM | refuse `CASCADE_MAP_R5_ADDENDUM_JSON`; only a JSON syntax error means text (a Markdown addendum) |
| `strict_json_typed` (v003) | native | root's dispositions file (tools 1 and 4) | refuse with the typed `DISPOSITIONS_JSON_*` code; no text fallback at all |
| `strict_json` / `strict_json_bytes` | native | every other JSON input: prereg, slots, plan, identity records, certificates, B6 bodies, B7 inputs, B2 record and registry, admission config and SEAL_RECORD | refuse with a code naming the input; never text |

So only the driver-check probe parses integers as strings. The cascade probe keeps native integers, and its oversized-integer ValueError refuses with a typed code. Both still refuse the A-B1 record class, and neither admits it (Codex3 found no bypass). The reviewed compare's own loaders (`load_strict_file`, `load_driver_build_record`, `check_record_codes`) belong to the compare, not to these tools: r12's `check_record_codes` admits the A-B1 duplicate-key record and r13's refuses it (TESTED).

## When root runs each tool (the README order, SEAL_CHECKLIST_R5 steps)

`T=…/seal_tools_v003`. The paths below are placeholders. **The order is tool 1, tool 5, tool 3, tool 2, then tool 4 (build), then tool 4 (admission check)**, as in v002's README (0639: v003 uses the README order and states it).

| step | command | it refuses |
|---|---|---|
| B1 (freeze) | `python3 -I -B $T/check_frozen_addendum_c4v003.py --prereg <sealed prereg> --frozen <CLAUDE2>/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md --addendum-at-text-of-record <the prereg's addendum_read copy> [--dispositions <root's dispositions JSON> --dispositions-sha <its sha256>]` | a cited entry missing; a duplicate heading; a copy that is not the FROZEN file or not at path_to_be; the prereg's own sha in the frozen text; an entry-table row missing, repeated, re-hashing differently or not the read copy's; a read copy that is not the prereg's pin; any entry of L u CH without its row, and any defect of the dispositions file (above); a bare `--covered-later` |
| B2a | `python3 -I -B $T/print_driver_build_record_c4v003.py --reviewed <reviewed compare> --reviewed-sha <its sha> --check-record <driver check record of record> \| python3 -I -B -c "import sys; open(sys.argv[1], 'x').write(sys.stdin.read())" <DRIVER_BUILD_R5 record path>` | a check record the compare does not admit for this build, or a defective JSON check record |
| after B4 | `python3 -I -B $T/check_slot_fill_c4v003.py --slots <slots.json> --prereg <sealed prereg> --text-of-record <prereg text of record> --text-of-record-sha <its sha from root's ruling> [--frozen … --addendum-at-text-of-record … [--dispositions … --dispositions-sha …]] [--reviewed … --sealed-compare …]` | everything in the tables that tool 3 owns (with `--frozen`, tool 1's refusals too, as `T1:<code>`); a dispositions pin or read copy without `--frozen` |
| after B5 | `python3 -I -B $T/check_sealed_compare_c4v003.py --reviewed <reviewed source> --sealed <sealed compare> --slots <slots.json> --prereg <sealed prereg>` | a non-pin line; a pin not equal to its slot or assigned twice; a pin slot that is not {path, sha256}; a cited addendum whose bytes are not PIN_ADDENDUM_V005 |
| B7 | `python3 -I -B $T/build_seal_record_c4v003.py --slots … --prereg … --text-of-record … --text-of-record-sha … --frozen … --addendum-at-text-of-record … [--dispositions … --dispositions-sha …] --reviewed … --sealed-compare … --gates-only-output <outdir>/GATES_ONLY.json --validity-only-output <outdir>/VALIDITY_ONLY.json --key-equivalence-map K.json --new-item-list N.json --successor-custody Z.json --b2-record <B2 record of record>` | everything above (it runs tools 1-3), plus the B6/B7/B2 rules and `DISPOSITIONS_CHANGED_AFTER_CHECK`. On PASS it prints the record and its sha goes to stderr. A refusal prints nothing on stdout. |
| B8 | `python3 -I -B $T/build_seal_record_c4v003.py --check-admission-config <ROOT_SEAL_ADMISSION_V001.json> --seal-record <SEAL_RECORD.json>` | a config that does not pin this SEAL_RECORD, its prereg, compare and BUILD_V007, or whose producer_allowlist is not exactly BUILD_V007's 15 sources naming the record's launcher and guard (each verified from bytes and listed literally in the BUILD); a SEAL_RECORD whose sealed_by, driver or frozen_addendum guard v008 would refuse (v003 B8; W7-S1 above) |

Root creates each printed record with exclusive create (`open(…, 'x')`) and compares the written file's sha256 with the one printed on stderr. Flags in brackets are optional as a group. Tool 1 needs `--addendum-at-text-of-record` whenever it runs (directly, or through tools 3 and 4 with `--frozen`). `--dispositions` and `--dispositions-sha` go together, and are required when L u CH is not empty.

**API** (keyword names as in the sources):

| tool | call |
|---|---|
| 1 | `run(prereg, frozen, expect_frozen_sha=None, covered_later=(), allow_open=False, dispositions=None, text_of_record_addendum=None)`; `dispositions=(path, sha256)`; `covered_later` must be empty |
| 3 | `run(slots_path, prereg_path, text_of_record_path, frozen=None, covered_later=(), reviewed=None, sealed_compare=None, text_of_record_sha=None, dispositions=None, text_of_record_addendum=None)`; the passthrough carries `later_entry_dispositions`, `dispositions_required`, `addendum_at_text_of_record` |
| 4 | `safe_build(a)` with `a.dispositions = (path, sha256)` or None, `a.addendum_at_text_of_record = PATH`, and `a.covered_later` absent or empty; `check_admission_config(config_path, seal_record_path)` |

**Text of record.** As in v002: `TEXT_OF_RECORD_SHA` in tool 3 is `PENDING_PREREG_R5_TEXT_OF_RECORD` until a pin-only successor sets it. Until then root states the sha with `--text-of-record-sha`. It must be the file's bytes, and the SEAL_RECORD records `text_of_record_pinned_by: ROOT_ARGUMENT`. Under A106 the text of record is prereg r6, and its pin is checked by Claude3's seal script (C-02, A106.2). Without the argument, tool 3 refuses `TEXT_OF_RECORD_PIN_PENDING` (a gap) and still checks every other layer.

## What v002 fixed (kept in v003)

| item | fix | tool |
|---|---|---|
| D-01 | Every M_s field of FIELDS_R12, per certificate kind: LO `source_gas_M_s` and its echoes (A73 F2); GQ `rosters[].M_s`, with `M_s_doubled` = 2 M_s and NGC_T120L at the NGC M_s; DOUBLING `ddo_gas_M_s` (A73). Then every other M_s-type key (`M_s`, `gas_M_s`, `*_gas_M_s`, `gas_M_s_DDO/NGC`, `…/M_s`). The DDO value is the case block's registered gas.M_s (A68 CHK-1; must be 128, A57). The NGC value is the slot, which must equal the compare's `NGC_GAS_M_S_A57` (96). | 3 |
| D-04 | The sealed prereg must carry `binding_inputs.case_block` {path, sha256}. It is verified from bytes and validated by the reviewed compare's own `validate_case_block`, after the slot's driver BUILD record is activated by the compare's own `activate_driver_build` (the sealed-mode order). Under r5 the `cascade_map_r5_addendum` slot is required (SRR[9], A69) and must name the build's r5 cascade map sha. The `admission_entry` slot (SRR[10], A78 N2) must equal the bound plan's launcher and guard and be BUILD_V007-supported entries. All of this passes through to the SEAL_RECORD. | 3, 4 |
| D-06 | Tool 5 prints the exact driver BUILD record (PIN_DRIVER_BUILD_RECORD): the reviewed compare's `builtin_r5_build()` with `check_record` = the driver check record, admitted by the compare's own `activate_driver_build` before printing. | 5 |
| D-07 | A bare PENDING string, a list or a partial object in a pin slot refuses `PIN_SHAPE` (exit 2 with a verdict JSON), not a TypeError (exit 1). | 2 (and all) |
| D-08 | The layers are reported together. A layer is skipped, with a `LAYER_SKIPPED` note, only when a pin it reads did not verify. | 3 |
| D-09 | The SEAL_RECORD states that it is the authority on sealed status, and lists the PENDING strings that the text of record keeps outside slot values. | 4 |
| D-10 | The frozen copy must sit exactly at `seal_slots.frozen_addendum.path_to_be`: tool 1 checks the file, tool 3 checks the slot. | 1, 3 |
| D-05 | v002: `--covered-later` was an explicit list of `A<n>` items. **Removed in v003** (above). | 1 |
| A99.1 | The launch-packet BUILD is read from the prereg's `seal_slots.launch_packet.named_candidates_verified_from_bytes.build`. It must be `BUILD_V007.md`; anything else refuses `BUILD_NOT_BUILD_V007`. While its sha is the literal `PENDING_BUILD_V007`, tool 3 refuses `BUILD_V007_PENDING` (a gap). Its allowlist must list exactly 15 sources, each path once and each verified from bytes (V6-S3). The bound plan's template must be named in it, and must be the prereg-named `template_plan`. | 3, 4 |
| A99.3 | The prereg's `entries_after_A81` table, in the prereg r5 form. It must hold every frozen entry from A82 through the last cited entry, once each, and each row is re-hashed from the frozen bytes by r5's section_rule. v003: each row must also be the read copy's section, and a changed entry needs a dispositions row (above) or a successor revision. The SEAL_RECORD quotes the table. | 1, 4 |
| R-04 | The B6 inputs must be the sealed compare's own blinded bodies `GATES_ONLY.json` and `VALIDITY_ONLY.json`, under r12's own value rule. The B7 inputs must parse with the schemas below. | 4 |
| R-10 | The SEAL_RECORD key map must equal the validated case block's `key_equivalence_map` (which is `[]` when the block has none). | 4 |
| A100 | When the prereg asks the seal record to repeat the B2 disclosure block, `--b2-record` names the B2 record of record. It must be a PASS B2 gate record listed in the slot registry's `gate_records.B2`. | 4 |
| A102 | A-B1 class. The driver check record and the CASCADE_MAP_R5_ADDENDUM may be text, but if either is JSON it must parse strictly, and the only text fallback is a JSON syntax error. The two probes parse integers differently (corrected in v003; see the parser table): the driver-check probe parses integers as strings, and the cascade-addendum probe keeps native integers and refuses the oversized-integer ValueError with `CASCADE_MAP_R5_ADDENDUM_JSON`. | 3, 5 |
| B8 | Admission mode: `--check-admission-config CFG --seal-record SEAL`. v003 adds guard v008's seal-record conditions (above). | 4 |

## Forms the tools expect

As in v002 (README `da29c008`, "Forms the tools expect"): the sealed prereg is the text of record with each `seal_slots.<k>.value` replaced by the slot value, plus the one BUILD_V007 sha fill. The slot JSON is `UNT_V007_SEAL_SLOTS_C4V002` (unchanged). The sealed compare is the reviewed source with exactly the five pin lines changed (A82). The driver BUILD record is tool 5's bytes: with r12 and CHECK.md `89a6de88` they hash to `25b4ff69…`, and r13 prints the same bytes (TESTED). The B7 JSON forms (key map, NEW items, raw successor custody) keep their v002 schemas. New in v003: the dispositions file (above) and the SEAL_RECORD fields `later_entry_dispositions` and `addendum_at_text_of_record`.

## Fence for lane runs: `tools/fence_c4v002.py`

`tools/fence_c4v002.py` (`c993d34c`) and `tools/run_fenced_c4st2.py` (`fe904509`) are exact byte copies of v002's, made by exclusive create. No path needed adapting: the fence takes its review root from its own location (this folder), and the runner finds the fence beside itself. The fence blocks process creation, kill, network, deletes, writes outside this folder, both runs_ext roots, `UVT_*` components (except `uvt_*.py` sources outside runs_ext), the C5H run name, target words and other NGC3198 data. It allows reading the CLAUDE2 root-decision addenda (v002 exception (b)). The runner checks the fence sha, runs the fence selftest (8/8) and 15 exception probes, then the script, and prints the BLOCKED list after the selftests: **[] in every run of this build.**

Process note (FORMAL, from the fence source): the selftest and the probes call `os.path.realpath` on probe paths that do not exist (under CLAUDE2/runs_ext, and `UVT_probe_should_not_exist` paths), so realpath lstats their components before the fence refuses. No probe touches `runs_ext/KMAX_A2F10_C5H_RUN_V001` or any existing UVT path. Every run of this runner does this once, as in v002 (Claude4 0108 P-N1 made the same note about its own fence).

## Tests

`tests/test_seal_tools_c4v003.py`, run inside the fence from this folder: **352/352** (ENVIRONMENT 1/1, NEW 159/159, NEW_CONTROL 30/30, PORT 90/90, PORT_CHANGED 58/58, REAL_NEW 9/9, REPRO 5/5). Every one of r2's 148 cases is ported once, by r2 index (each PORT_CHANGED case gives its reason).
- Run folder: `tests/run_20261019T000810Z`, with the fenced runner's stdout and stderr copied in as `RUN_LOG_FENCED_C4V003.txt` (its FENCE_C4ST2_SUMMARY line shows selftest 8/8, probes 15/15 and BLOCKED after the selftest []).
- Record: `TEST_RESULTS_C4V003.json` `26bb912f58fbd2f912c3ca162b4a8f0971fbc2cf556d8a80b87c5a99b188f8df`.
- The open V005 was `c01b3c51` (final, A106) throughout, and the ENVIRONMENT case checks that it did not change during the run. BLOCKED after the selftest was [].

What the suite covers, beyond the ported cases:
- **D-05 / 0640 / C-01 (tool 1):** the read copy (missing, a directory, wrong sha, wrong byte count, no pin, a short pin, a repeated heading, a cited entry missing, an entry gone from the frozen copy, table rows that are not its sections); C-01 (an edit inside the cited A62 with no row refuses `ENTRY_SECTION_CHANGED`; r2's own tool 1 passes it, REPRO); PV-D05-1 (plain no_change on A62, on the table row A90, and on Codex1's fixture); every `changed_text` defect (present in the old bytes, absent from the new, generic, empty, not a string, a lone surrogate, NFD against NFC bytes); `why_no_prereg_effect` empty, whitespace or not a string; exact keys per disposition (the removed pre-0640 `change` object included); `no_change_after_change` on an L row; `revised` without a `prereg_revision`, or with a forged, missing, relative, short, extra-key, bare-string or directory pin, or with the prereg itself or a byte copy of it; every file and row defect of v003's first design that still applies; positive controls for each disposition.
- **Codex1's PV-D05-1 fixture** (`b1b6000f`): verbatim (its prereg has no addendum_read, so it refuses `ADDENDUM_READ_PIN_ABSENT`); and with a read copy built from Codex1's own `OLD_A90_SECTION` (`92129acd`), where it refuses `DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY` (the only code once the row has the v003 shape). **Codex3's ED-D05-1 fixtures**: verbatim and with read copies.
- **Bare names** in tools 1, 3 and 4, by API and CLI (the `=` form too).
- **Tools 3 and 4:** the read copy and the dispositions pass through, and each refuses without `--frozen`. The builder refuses a missing or wrong read copy, and a plain no_change on a changed entry with no other refusal. The record carries `later_entry_dispositions` and `addendum_at_text_of_record` exactly. The builder's re-read refuses three injected late changes.
- **B8:** Codex3's six records plus four more of the same class refuse the check, and the real guard v008 refuses each too. **W7-S1:** the 17-row and the BUILD_V006 configs refuse the check, and the real guard admits both (REPRO).
- **r13 (A104):** tool 2 genuine plus two refusals, tool 3 with r13 as the reviewed source (a copy and the file itself), a full builder run with r13 and its IMPL (`274f7049`), tool 5 printing from r13 (bytes equal r12's), and r13's own `check_record_codes` refusing the A-B1 record.
- **REAL:** prereg r5 `3245899f` with its read copy `70a48f51` and a FROZEN-named copy of the final V005. Without a file it refuses exactly `DISPOSITIONS_REQUIRED` and `UNCOVERED_LATER_ENTRY` (L = A102-A106, CH = []). With no_change rows for A102-A106 it passes, with dry-run path notes only. Without the read copy, or with the frozen copy as the read copy, it refuses. A synthetic A62 edit in a FROZEN-named copy refuses with no row, passes with a correct `no_change_after_change`, and refuses with plain no_change.

Test-only fixture detail: the reviewed r12 hashes the open V005 path (`ADDENDUM_V005_CITED`), so tool 2 needs the frozen copy to equal the open file. The one builder test whose frozen copy has an edited A90 uses a SYNTHETIC copy of r12 with that one line pointing at the variant, plus an IMPL stand-in naming that copy's sha. Every fixture and disposition file in the run folder is SYNTHETIC and labelled so.

## Mutation check

`MUTATION_C4V003.json`: 78 of 78 single-change mutants of the final sources are killed (round 2, the set of record: `mutants/final/round2/`). Each mutant disables or weakens one v003 check, and the generator (`tools/make_mutants_final_c4v003.py`) asserts that each old text occurs exactly once and that each mutant compiles. Each mutant folder holds the final sources with that one change and the final test file. A mutant counts as killed when its full fenced suite run (`mutants/final/round2/<id>/run.log`, `…/tests/run_*/TEST_RESULTS_C4V003.json`) has at least one failing case while the ENVIRONMENT case passes, BLOCKED is [] and the folder matches the manifest. The JSON lists, for every mutant, its change and the failing cases.

Round 1 (`mutants/final/M*`, superseded) ran the same 78 mutants against the previous test file. 73 were killed with complete results. In the other 5 (tool 3 or the builder not passing the dispositions or the read copy on), the genuine build refused, and the old harness then stopped at a later case that read the missing record. The harness now records that case as a failure and finishes. That is the only change to the test file, and the whole set was re-run as round 2. The old 24 mutants under `mutants/M01…M24` test the pre-0640 design and are not evidence for v003.

## TESTED / FORMAL / UNTESTED

- **TESTED (fenced suite):** every case above; the CLI exit codes and stdout/stderr split; byte-exact pass-through into the SEAL_RECORD; the real guard v008 `admission()` and launcher v007 `validate()` on synthetic configs and plans (nothing started).
- **FORMAL (source reading):** guard v008 and launcher v007 do not read the SEAL_RECORD schema. Only `## A<n>:` sections are compared, so the 615-byte preamble of V005 (text before its first entry heading) is not; every `## ` heading of `c01b3c51` is an entry (TESTED from bytes). A heading with non-ASCII digits makes r2's `headings()` (str regex) and `sections()` (bytes regex) disagree, and the tool then fails closed with `INTERNAL_EXCEPTION:KeyError` (pre-existing r2 behaviour, unchanged).
- **UNTESTED:** prereg r6 (not published at this build); the real seal, the real admission config and the real SEAL_RECORD; whether any reason, `why_no_prereg_effect` or pinned revision is adequate (mechanical checks only); production compare runs. Nothing was launched, no compare was run, `--validity-only` was never used, no runs_ext/C5H/UVT path was read, listed or stat'ed (beyond the fence probes noted above), and no target or observed-velocity data was opened.

## Files (sha256 from bytes)

| file | role | sha256 |
|---|---|---|
| `seal_common_c4v003.py` | shared helpers | `101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21` |
| `check_frozen_addendum_c4v003.py` | tool 1 | `a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4` |
| `check_sealed_compare_c4v003.py` | tool 2 | `c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1` |
| `check_slot_fill_c4v003.py` | tool 3 | `316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af` |
| `build_seal_record_c4v003.py` | tool 4 (builder, admission check) | `de0ceb15ebfb95e04227730bd2785eb46af8cb5980012de91de98f34ea226b96` |
| `print_driver_build_record_c4v003.py` | tool 5 | `e5bedffe3c91650d5dba7fbd1ed5476e228158679d8959dfea0e2eff436ebdea` |
| `tests/test_seal_tools_c4v003.py` | tests | `67dd8a0085436639ef85650ca966b6b9ae045cc9413f01fc943b7003f142099a` |
| `tests/run_20261019T000810Z/TEST_RESULTS_C4V003.json` | final run record | `26bb912f58fbd2f912c3ca162b4a8f0971fbc2cf556d8a80b87c5a99b188f8df` |
| `DELTA_V002R2_TO_V003.md` | every changed source line, with its reason | `b9c0bea2cfe17d9317fc1ee130e4a8704ab89b0c48d2b772c9ae7b6bbefb3e57` |
| `MUTATION_C4V003.json` | mutation check | `3795b86601a9182dc1e0ffd280bbb61bcb97168d9ddb192f797e760d80e3f6be` |
| `tools/fence_c4v002.py` | fence (v002 copy) | `c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5` |
| `tools/run_fenced_c4st2.py` | fenced runner (v002 copy) | `fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25` |
| `tools/make_mutants_final_c4v003.py` | mutant generator | `24f4841f3373bbbcb04cc813ceb96df7a0d4524cc53643c34d4713f58f935013` |
| `tools/run_one_mutant_c4v003.sh` | one-mutant runner | `71fcc66518fbb3b71c24f914c77316f893a0553d885a8779802637902f4beec5` |
| `tools/analyze_mutants_final_c4v003.py` | mutation analysis | `56d17c06aba7bf65f5a2d5d33d3b73123dfc8de2d768b7b00a6fe0d014623ad7` |
| `tools/make_delta_c4v003.py` | DELTA generator | `bc4fc6c837a1b9e835f80d08aedf8be13ff015f2871935eb46e12d94c1201751` |
| `tools/delta_reasons_c4v003.py` | DELTA reasons | `3a9b2ddff3a1fea2b2cab2440787cf8c4d873c53174fac55dd7e6bc8ad29af65` |
| `tools/publish_c4v003.py` | exclusive-create publisher | `aede64b1a30ede5097743acf368990e8e25dc85c4c975de45c807fcbdb9cb554` |

`HASHES_SEAL_TOOLS_C4V003.txt` lists the sha256 of every published file, the final test run folder included.
