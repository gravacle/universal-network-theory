# dev helper (work copy): turn the v002 README bytes (da29c008) into README_SEAL_TOOLS_V003.md by exact replacements, so that every unchanged
# line stays byte for byte and DELTA_V002R2_TO_V003.md can list each changed line. The Tests and Files sections are filled from the final run.
# usage: python3 -I -B edit_readme_c4v003.py V002_README OUT_README FINAL_JSON   (FINAL_JSON: values from the final run; OUT is created exclusively)
import hashlib, json, sys
from pathlib import Path

V002, OUT, FINAL = Path(sys.argv[1]), Path(sys.argv[2]), json.loads(Path(sys.argv[3]).read_text())
raw = V002.read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'da29c008064ae51673dfe7106f72dfcb789f674b4c0a36e3a5daf017c7967af8'
s = raw.decode('utf-8')
A102_SEC = 'c4b56728ded3ae292f9e26f31f0cdfa0c41516a7c836f9d5791934034a231a76'
F = FINAL


def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('# seal_tools v002: root-side V007 seal checks (Claude4, A99 item 4, dispatch 0621)\n',
    '# seal_tools v003: root-side V007 seal checks (Claude4; D-05 dispatch 0633; B8 and the README note dispatch 0634)\n')
rep('UTC 2026-10-18T21:32:30Z (`date -u`). Successor of `../seal_tools/` v001 (README `1e04bd2a`, 40/40). **The tool set of record is `r2/`.** The top-level '
    '`*_c4v002.py` files are r1, kept unchanged; r2 supersedes them with the A102 (A-B1) hardening and the text-of-record argument. Tools 1 and 2 are '
    'byte-identical in r1 and r2.\n',
    'UTC %s (`date -u`). Successor of `../seal_tools_v002/r2/` (README `da29c008`, 148/148). **The tool set of record is the six `*_c4v003.py` files at the '
    'top level of this folder.** v003 changes only D-05 (root\'s byte-pinned later-entry dispositions file replaces the bare covered-later list; Codex3 '
    '0637/0639 ED-D05-1, BLOCKING), B8 (the admission check refuses every SEAL_RECORD that producer guard v008 refuses on sealed_by, driver and '
    'frozen_addendum; Codex3 0639, SHOULD_FIX), this README\'s parser note (Codex3 A102 note `c09c6c39`) and the v002 -> v003 renames. '
    '`DELTA_V002R2_TO_V003.md` lists every changed line of the six sources and of this README, each with its reason. `dev/` and `mutants/` hold work '
    'copies only; nothing there is of record.\n' % F['utc'])
rep('## What v002 fixes\n', '## What v003 changes\n\n'
    '| item | change | tool |\n|---|---|---|\n'
    '| D-05 | The bare `--covered-later` list is **removed**. A non-empty `covered_later` (API) or any `--covered-later` flag (CLI, the `=` form too) refuses '
    '`COVERED_LATER_BARE_NAMES_REFUSED` in tools 1, 3 and 4 and covers nothing. Root instead supplies its later-entry dispositions file, pinned by '
    '`--dispositions D.json --dispositions-sha H` (API `dispositions=(path, sha256)`). Tool 1 verifies it (below); tool 3 passes the pin to tool 1 and '
    'tool 1\'s verified result through; the builder re-reads the file (`DISPOSITIONS_CHANGED_AFTER_CHECK` unless its bytes still hash to root\'s pin and to '
    'what tool 1 verified) and carries it into the SEAL_RECORD as `later_entry_dispositions` = {pin, content, raw_text}, replacing v002\'s generic '
    '`no_change_notes`. The SEAL_RECORD schema becomes `UNT_V007_SEAL_RECORD_C4V003`. | 1, 3, 4 |\n'
    '| B8 | `--check-admission-config` also checks the SEAL_RECORD fields guard v008 `admission()` checks: `sealed_by` equal to the guard\'s AUTHORITY '
    '(L32), `driver` and `frozen_addendum` present (L39) and exact {path, sha256} pins verified from bytes (L40, `pin_check` L18). Codex3\'s six records '
    '(changed or removed sealed_by; malformed or stale driver or frozen_addendum, each re-pinned by its config) now refuse with typed codes, and the real '
    'guard refuses each of them too (tested). | 4 |\n'
    '| README | The A102 row below no longer says that both JSON probes parse integers as strings; the parser table below says exactly which parsers do. | - |\n'
    '| rename | Module, check and usage names `*_c4v002` -> `*_c4v003`; the in-process compare module name; header lines naming the predecessor. Input '
    'schemas keep their v002 names (their formats did not change). Tools 2 and 5 change only by renames. | all |\n\n'
    '## What v002 fixed (kept in v003)\n')
rep('| D-05 | `--covered-later` is an explicit comma-separated list of `A<n>` items, with no ranges and no repeats (example below). | 1 |\n',
    '| D-05 | v002: `--covered-later` was an explicit list of `A<n>` items, with no ranges and no repeats. **Removed in v003** (the table above). | 1 |\n')
rep('A changed row needs root\'s explicit note (list it in `--covered-later`) or a successor revision. The SEAL_RECORD quotes the table. | 1, 4 |\n',
    'A changed row needs a row in root\'s dispositions file carrying the change (v003) or a successor revision. The SEAL_RECORD quotes the table. | 1, 4 |\n')
rep('| A102 | A-B1 class. The driver check record and the CASCADE_MAP_R5_ADDENDUM may be text, but if either is JSON it must parse strictly. Integers are parsed '
    'as strings, and the only text fallback is a JSON syntax error. So a duplicate key behind a 4,300+ digit integer refuses, even while r12\'s own '
    '`check_record_codes` still admits it; r13 fixes the compare. The addendum part was patched by the Claude4 main loop in r1. | 3, 5 |\n',
    '| A102 | A-B1 class. The driver check record and the CASCADE_MAP_R5_ADDENDUM may be text, but if either is JSON it must parse strictly, and the only '
    'text fallback is a JSON syntax error. The two probes parse integers differently (corrected in v003, Codex3 A102 note): the driver-check probe '
    '(`json_or_text`, tools 3 and 5) parses integers as strings, so a duplicate key behind a 4,300+ digit integer reaches the duplicate hook and refuses '
    '(`DRIVER_CHECK_RECORD_JSON_DEFECT`, `CHECK_RECORD_JSON_DEFECT`), even while r12\'s own `check_record_codes` still admits it; r13 fixes the compare. The '
    'cascade-addendum probe (tool 3) keeps native integers (`strict_json_bytes`): the oversized integer raises a ValueError that is not a JSON syntax '
    'error, and that refuses `CASCADE_MAP_R5_ADDENDUM_JSON` with no text fallback. The addendum part was patched by the Claude4 main loop in r1. | 3, 5 |\n')
rep('| B8 | Admission mode: `--check-admission-config CFG --seal-record SEAL`. | 4 |\n',
    '| B8 | Admission mode: `--check-admission-config CFG --seal-record SEAL`. v003 adds guard v008\'s seal-record conditions (the table above). | 4 |\n')
rep('`T=…/seal_tools_v002/r2`. The paths below are placeholders.\n', '`T=…/seal_tools_v003`. The paths below are placeholders.\n')
rep('| B1 (freeze) | `python3 -I -B $T/check_frozen_addendum_c4v002.py --prereg <sealed prereg> --frozen <CLAUDE2>/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md '
    '--covered-later A102,A103` | a cited entry missing; a duplicate heading; a copy that is not the FROZEN file or not at path_to_be; the prereg\'s own sha in '
    'the frozen text; an entry-table row missing, repeated or re-hashing differently; any entry after the last cited one (r5: A101) with neither a table '
    'row nor a listed note |\n',
    '| B1 (freeze) | `python3 -I -B $T/check_frozen_addendum_c4v003.py --prereg <sealed prereg> --frozen <CLAUDE2>/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md '
    '--dispositions <root\'s dispositions JSON> --dispositions-sha <its sha256>` | a cited entry missing; a duplicate heading; a copy that is not the FROZEN '
    'file or not at path_to_be; the prereg\'s own sha in the frozen text; an entry-table row missing, repeated or re-hashing differently; any entry after the '
    'last cited one (r5: A101) with neither a table row nor a dispositions row; a changed table row without a dispositions row carrying its change; any '
    'defect of the dispositions file (below); a bare `--covered-later` |\n')
rep('| B2a | `python3 -I -B $T/print_driver_build_record_c4v002.py ', '| B2a | `python3 -I -B $T/print_driver_build_record_c4v003.py ')
rep('| after B4 | `python3 -I -B $T/check_slot_fill_c4v002.py ', '| after B4 | `python3 -I -B $T/check_slot_fill_c4v003.py ')
rep('| after B5 | `python3 -I -B $T/check_sealed_compare_c4v002.py ', '| after B5 | `python3 -I -B $T/check_sealed_compare_c4v003.py ')
rep('| B7 | `python3 -I -B $T/build_seal_record_c4v002.py --slots … --prereg … --text-of-record … --text-of-record-sha … --frozen … --covered-later A102,A103 '
    '--reviewed … ', '| B7 | `python3 -I -B $T/build_seal_record_c4v003.py --slots … --prereg … --text-of-record … --text-of-record-sha … --frozen … '
    '--dispositions <root\'s dispositions JSON> --dispositions-sha <its sha256> --reviewed … ')
rep('| everything above (it runs tools 1–3), plus the B6/B7/B2 rules. On PASS it prints the record; its sha goes to stderr. |\n',
    '| everything above (it runs tools 1–3), plus the B6/B7/B2 rules and `DISPOSITIONS_CHANGED_AFTER_CHECK`. On PASS it prints the record; its sha goes '
    'to stderr. A refusal prints nothing on stdout. |\n')
rep('| B8 | `python3 -I -B $T/build_seal_record_c4v002.py --check-admission-config <ROOT_SEAL_ADMISSION_V001.json> --seal-record <SEAL_RECORD.json>` | a config '
    'that does not pin this SEAL_RECORD, its prereg, compare and BUILD_V007, or whose producer_allowlist is not exactly BUILD_V007\'s 15 sources naming the '
    'record\'s launcher and guard (each verified from bytes and listed literally in the BUILD) |\n',
    '| B8 | `python3 -I -B $T/build_seal_record_c4v003.py --check-admission-config <ROOT_SEAL_ADMISSION_V001.json> --seal-record <SEAL_RECORD.json>` | a config '
    'that does not pin this SEAL_RECORD, its prereg, compare and BUILD_V007, or whose producer_allowlist is not exactly BUILD_V007\'s 15 sources naming the '
    'record\'s launcher and guard (each verified from bytes and listed literally in the BUILD); a SEAL_RECORD whose sealed_by, driver or frozen_addendum '
    'guard v008 would refuse (v003, B8) |\n')
DISP = (
    '**Root\'s later-entry dispositions file (D-05, v003).** It replaces v002\'s `--covered-later` list. Tool 1 works out two sets from the bytes:\n\n'
    '- **L**: every frozen entry after the prereg\'s last cited entry that has no table row (r5 cites A47–A101, so L is A102 onward);\n'
    '- **CH**: every `entries_after_A81` row whose section no longer re-hashes from the frozen bytes (r5 section_rule, tool 1 `sections()`).\n\n'
    'The file has exactly one row for each entry of L ∪ CH, and no other row. When L ∪ CH is empty the file is optional (the SEAL_RECORD then carries '
    '`later_entry_dispositions: "NOT_SUPPLIED_NONE_REQUIRED"`); otherwise a missing file refuses `DISPOSITIONS_REQUIRED`, naming the entries. In the V005 '
    'bytes read for this build (`643ef6ef` at 21:45Z, then `acb7f44a` at 22:18Z) L is A102, A103 and A104, and CH is empty (all 20 r5 rows re-hash); '
    'root\'s file at the freeze must follow the frozen bytes, whatever later entries they hold.\n\n'
    '- **The pin:** an absolute path to a regular file (a symlink only if it resolves to one) whose bytes hash to the sha root states; read once, and those '
    'bytes are the ones parsed. Anything else refuses `DISPOSITIONS_PIN_MISMATCH`.\n'
    '- **The parse:** UTF-8 text (else `DISPOSITIONS_JSON_ENCODING`; a byte-order mark is a syntax error), parsed by r2\'s strict JSON with native '
    'integers and no text fallback. A duplicate key refuses `DISPOSITIONS_JSON_DUPLICATE_KEY`; NaN or ±Infinity `DISPOSITIONS_JSON_NON_FINITE_CONSTANT`; an '
    'integer over Python\'s 4,300-digit limit `DISPOSITIONS_JSON_INTEGER_TOO_LONG`; a syntax error `DISPOSITIONS_JSON_SYNTAX`; any other ValueError '
    '`DISPOSITIONS_JSON_VALUE_ERROR`; any other exception (for example nesting deep enough to exhaust the parser) `DISPOSITIONS_JSON_DEFECT`.\n'
    '- **The object:** keys exactly `schema` (= `UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001`), `frozen_addendum_sha256` (= the frozen copy\'s sha) and '
    '`entries` (a list).\n'
    '- **A row:** keys exactly `entry` (`A<n>`, ASCII digits, no leading zero), `disposition` (`revised` or `no_change`), `reason` (a string that is not '
    'empty after strip) and `section_sha256` (that entry\'s section in the frozen bytes), plus `change` exactly on a CH row: `{from_section_sha256` (the '
    'table row\'s section_sha256), `to_section_sha256` (the frozen section\'s sha), `what_changed` (not empty after strip)`}`, whatever the disposition. An '
    'L row carries no `change`.\n\n'
    '```json\n'
    '{\n'
    ' "schema": "UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001",\n'
    ' "frozen_addendum_sha256": "<sha256 of CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md>",\n'
    ' "entries": [\n'
    '  {\n'
    '   "entry": "A102",\n'
    '   "disposition": "<revised | no_change: root\'s decision>",\n'
    '   "reason": "<root\'s entry-specific reason: what A102 rules (r12 reviews split; r13 closes A-B1) and why the prereg text does or does not change>",\n'
    '   "section_sha256": "%s"\n'
    '  }\n'
    ' ]\n'
    '}\n'
    '```\n\n'
    'This is a template, not root\'s disposition: the angle-bracket values are root\'s to write, and the file needs a row like it for A103, A104 and every '
    'later entry of the frozen bytes. `%s` is A102\'s section sha in both V005 reads above; root re-reads it from the frozen copy. A changed table row (say '
    'A90) would add `"change": {"from_section_sha256": "<A90\'s r5 table row sha>", "to_section_sha256": "<A90\'s frozen section sha>", "what_changed": '
    '"<what changed in A90>"}` to its row. The tool checks shapes, shas and that each string is not empty; it cannot judge whether a reason is adequate '
    '(a placeholder string passes), so root and the reviewer own that. The section shas, read with the tool\'s own rule:\n\n'
    '```sh\n'
    'python3 -I -B -c "import hashlib, sys; sys.path.insert(0, sys.argv[1]); import check_frozen_addendum_c4v003 as T1; '
    's = T1.sections(open(sys.argv[2], \'rb\').read()); [print(\'A%%d\' %% n, hashlib.sha256(s[n][0][1]).hexdigest()) for n in sorted(s) if n > 101]" '
    '$T <CLAUDE2>/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md\n'
    '```\n\n'
    'Row refusals: a missing L row `UNCOVERED_LATER_ENTRY`; a missing CH row `ENTRY_TABLE_SECTION_CHANGED`; an entry not in the frozen bytes '
    '`DISPOSITION_ENTRY_NOT_IN_FROZEN`; a repeated entry `DISPOSITION_DUPLICATE_ENTRY`; a row for an unchanged tabled entry `DISPOSITION_FOR_TABLED_ENTRY`; '
    'a row for an entry at or before the last cited one that is not a changed table row `DISPOSITION_FOR_CITED_ENTRY` (both can apply); a bad entry name '
    '`DISPOSITION_ENTRY_FORMAT`; a row that is not an object `DISPOSITION_ROW_SHAPE`; wrong row keys `DISPOSITION_ROW_KEYS`; a bad disposition '
    '`DISPOSITION_VALUE`; an empty, whitespace or non-string reason `DISPOSITION_REASON_EMPTY`; a wrong section sha `DISPOSITION_SECTION_SHA_MISMATCH`; on a '
    'CH row, no change `DISPOSITION_CHANGE_REQUIRED`, a malformed change `DISPOSITION_CHANGE_SHAPE`, a wrong from or to sha '
    '`DISPOSITION_CHANGE_FROM_MISMATCH` / `DISPOSITION_CHANGE_TO_MISMATCH`, an empty what_changed `DISPOSITION_CHANGE_WHAT_EMPTY`; an L row with a change '
    '`DISPOSITION_CHANGE_NOT_ALLOWED`. File refusals: `DISPOSITIONS_SHAPE` (not an object), `DISPOSITIONS_KEYS`, `DISPOSITIONS_SCHEMA`, '
    '`DISPOSITIONS_FROZEN_SHA_MISMATCH`, `DISPOSITIONS_ENTRIES_SHAPE`. Tool 3 refuses `DISPOSITIONS_WITHOUT_FROZEN` for a pin given without `--frozen`. '
    'On PASS tool 1 notes `DISPOSITIONS_VERIFIED` and returns `later_entry_dispositions` = {pin, content, raw_text}; a disposed CH row is noted '
    '`ENTRY_TABLE_SECTION_CHANGED_NOTED`.\n\n'
    '| tool | CLI | API |\n|---|---|---|\n'
    '| 1 | `--dispositions D.json --dispositions-sha H` (both or neither) | `run(prereg, frozen, expect_frozen_sha=None, covered_later=(), allow_open=False, dispositions=None)`, `dispositions=(path, sha256)` |\n'
    '| 3 | the same two flags, with `--frozen` | `run(..., text_of_record_sha=None, dispositions=None)`; passthrough `later_entry_dispositions`, `dispositions_required` |\n'
    '| 4 | the same two flags | `a.dispositions = (path, sha256)` or None; `a.covered_later` must be absent or empty |\n\n'
    '**B8: the admission check against producer guard v008** (`294cb776`, read as source; executed only in the fenced tests with CONFIG patched):\n\n'
    '| guard v008 `admission()` | v003 `--check-admission-config` | code |\n|---|---|---|\n'
    '| L32 `seal.get(\'sealed_by\') != AUTHORITY` | the same equality with the same AUTHORITY | `ADMISSION_SEAL_SEALED_BY_NOT_AUTHORITY` (changed, extra key or absent) |\n'
    '| L39 `driver` / `frozen_addendum` not in the seal | the same | `ADMISSION_SEAL_DRIVER_REQUIRED`, `ADMISSION_SEAL_FROZEN_ADDENDUM_REQUIRED` |\n'
    '| L40 `pin_check(seal[key])` (L18: a dict, keys exactly {path, sha256}, sha of the path\'s bytes) | `Checker.pin`: the same, and stricter (absolute '
    'path, 64 hex, no PENDING, a regular file) | `ADMISSION_SEAL_DRIVER_PIN`, `ADMISSION_SEAL_FROZEN_ADDENDUM_PIN` (detail: the pin code) |\n'
    '| L27, L29, L30, L33–L37 | as v002 (schema and authority, launcher and guard on the allowlist, config pins, prereg/compare binding, allowlist bytes and BUILD listing) | as v002 |\n\n'
    'So every record the guard refuses on these three fields, the check refuses too; the check is stricter, never looser. Not mirrored (runtime, outside '
    'the record): the published `UNT_ROOT_ADMISSION_SHA256` (L23–L25), the config\'s location beside the guard (L8, L21), and allowlist membership of '
    'producers other than the record\'s launcher and guard (L29). Launcher v007 `validate()` also requires the plan\'s driver and frozen_addendum to equal '
    'the seal\'s (L68–L71); the builder writes them from the bound plan, and the check does not read the plan.\n\n'
    '**Which parsers parse integers as strings** (`parse_int=str`; Codex3 A102 note):\n\n'
    '| parser | integers | used for | on a non-syntax ValueError (a duplicate key, a non-finite constant, a 4,300+ digit integer) |\n|---|---|---|---|\n'
    '| `json_or_text` (seal_common) | strings | the driver check record probe (tool 3 `DRIVER_CHECK_RECORD_JSON_DEFECT`; tool 5 `CHECK_RECORD_JSON_DEFECT`) | '
    'refuse; only a JSON syntax error means text |\n'
    '| `strict_json_bytes` in tool 3\'s cascade-addendum probe | native | the CASCADE_MAP_R5_ADDENDUM | refuse `CASCADE_MAP_R5_ADDENDUM_JSON`; only a JSON '
    'syntax error means text (a Markdown addendum) |\n'
    '| `strict_json_typed` (v003) | native | root\'s dispositions file (tools 1 and 4) | refuse with the typed `DISPOSITIONS_JSON_*` code; no text fallback at all |\n'
    '| `strict_json` / `strict_json_bytes` | native | every other JSON input: prereg, slots, plan, identity records, certificates, B6 bodies, B7 inputs, '
    'B2 record and registry, admission config and SEAL_RECORD | refuse (a code naming the input), never text |\n\n'
    'The reviewed compare\'s own loaders (`load_strict_file`, `load_driver_build_record`, `check_record_codes`) are the compare\'s, not these tools\'.\n'
) % (A102_SEC, A102_SEC[:8])
rep('**`--covered-later` (D-05).** Give every entry after the prereg\'s last cited entry up to the freeze, one by one, plus any table row whose section no '
    'longer re-hashes. r5 cites A47–A101. If the freeze comes after A103 and nothing in A82–A101 changed, the list is `--covered-later A102,A103`. If A99\'s '
    'section had also changed, it is `--covered-later A99,A102,A103`. A bare `A82` is now refused (`COVERED_LATER_IS_CITED`, `UNCOVERED_LATER_ENTRY`). Each '
    'listed entry becomes a seal-record note. A changed row\'s note carries both section shas.\n', DISP)
rep('- **Slot JSON**, schema `UNT_V007_SEAL_SLOTS_C4V002`. All keys are required. These are the v001 keys plus two:\n',
    '- **Slot JSON**, schema `UNT_V007_SEAL_SLOTS_C4V002` (unchanged in v003). All keys are required. These are the v001 keys plus two:\n')
rep('- **Driver BUILD record:** tool 5\'s bytes. In my run, with r12 and CHECK.md `89a6de88`, they hash to '
    '`25b4ff697748ae23c0d1322228c8bdd689b4b378a70035ab89f5de03b2ba79fb`. Root prints and creates its own.\n',
    '- **Driver BUILD record:** tool 5\'s bytes. In my run, with r12 and CHECK.md `89a6de88`, they hash to '
    '`25b4ff697748ae23c0d1322228c8bdd689b4b378a70035ab89f5de03b2ba79fb`. Root prints and creates its own.\n'
    '- **Later-entry dispositions** (v003): above. **SEAL_RECORD** (v003): schema `UNT_V007_SEAL_RECORD_C4V003`; `later_entry_dispositions` = {`pin` '
    '{path, sha256}, `content` (the parsed file), `raw_text` (its exact text)} or `"NOT_SUPPLIED_NONE_REQUIRED"`; v002\'s `no_change_notes` are gone. The '
    'v003 admission check refuses a v002 record (`ADMISSION_SEAL_RECORD_SCHEMA`).\n')
rep('## Fence for lane runs: `tools/fence_c4v002.py`\n',
    '## Fence for lane runs: `tools/fence_c4v002.py`\n\n'
    'v003: `tools/fence_c4v002.py` (`c993d34c`) and `tools/run_fenced_c4st2.py` (`fe904509`) are exact byte copies of v002\'s, made by exclusive create. No '
    'path needed adapting: the fence takes its review root from its own location (this folder) and the runner finds the fence beside itself. The v002 '
    'description follows.\n')
# Tests and Files sections: replaced as a whole from the final run
i = s.index('## Tests\n')
s = s[:i] + F['tests_and_files']
with open(OUT, 'x') as f:
    f.write(s)
print(OUT, hashlib.sha256(s.encode('utf-8')).hexdigest())
