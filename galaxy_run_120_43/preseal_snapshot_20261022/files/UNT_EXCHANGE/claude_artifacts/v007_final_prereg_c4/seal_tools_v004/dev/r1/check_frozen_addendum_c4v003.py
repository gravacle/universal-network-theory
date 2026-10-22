# Claude4 seal tools v003, tool 1 (successor of r2 check_frozen_addendum_c4v002.py 06a98bc6; v002 succeeded check_frozen_addendum_c4v001.py
# c4ebbb5b): the frozen V005 addendum contains every A-entry the prereg cites, and every later or changed entry is accounted for. Read-only.
# Kept from v001: cited entries come from the prereg's structured `sources` lists and its cites_by_name ranges, never from prose;
# entries >= A47 must be `## A<n>:` headings of the frozen V005 bytes (each exactly once); entries <= A46 must be headings of a frozen
# decision file the prereg pins (decision_pins_frozen, verified from bytes); refused: a file that is not the separate
# ..._FROZEN.md copy (0576), a sha that differs from the slot, the sealed prereg's own sha inside the frozen bytes (RI-27 / A82),
# and an entry after the last cited one that root's no-change list does not cover (A81 RI-26; A82).
# New in v002:
#  - D-10: the frozen file must be exactly seal_slots.frozen_addendum.path_to_be (the CLAUDE2 control path), resolved;
#  - A99.3: the prereg's entry-by-entry table entries_after_A81 (prereg r5 form: {rule, section_rule, rows: [{entry, decision
#    REVISED_HERE with revised_clauses | NO_CHANGE with reason, section_sha256, ...}], ...}) must hold every frozen entry from A82
#    through the last cited entry, once each; each row is re-hashed from the frozen bytes (r5 section_rule: from the first byte of
#    the "## A<n>:" heading line up to, not including, the next line beginning "## ", or the end of the file); a row whose section
#    differs needs root's explicit seal-record note (list the entry in --covered-later) or a successor revision; every entry after
#    the last cited one is covered by a table row or by --covered-later, never by both;
#  - D-05: --covered-later is an explicit comma-separated list of A<n> items (no ranges, no repeats).
# New in v003 (D-05: dispatches 0633 and 0640; Codex3 0637/0639 ED-D05-1; Codex1 0081/0083 PV-D05-1; Claude4 v002 check C-01):
#  - the bare covered-later list is removed: a non-empty covered_later (API) or any --covered-later flag (CLI) refuses
#    COVERED_LATER_BARE_NAMES_REFUSED, and covers nothing;
#  - the old bytes (0640): the prereg pins the V005 bytes its entry table was read from (entries_after_A81.addendum_read:
#    sha256_at_generation, and its byte count when stated); root gives that copy (--addendum-at-text-of-record A.md; API
#    text_of_record_addendum=PATH). It must hash to the pin (else ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH; no copy given or not a regular
#    file: ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED; no pin in the prereg: ADDENDUM_READ_PIN_ABSENT). Every table row must be that copy's
#    section (else ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD), every cited entry >= A47 must be in it, every entry in it must still be in
#    the frozen bytes, and it may not repeat a heading;
#  - CH = every entry in both copies whose section bytes (r5 section_rule) differ, so every cited entry >= A47 and every table row is
#    compared (C-01: an edit inside a cited A62 is caught), plus every table row whose section_sha256 is not the frozen section's;
#    L = every frozen entry after the last cited entry with no table row, and every frozen entry absent from the read copy, minus CH;
#  - root's dispositions file, pinned (path, sha256) by root (--dispositions D.json --dispositions-sha H): an absolute path to a
#    regular file whose bytes hash to H (else DISPOSITIONS_PIN_MISMATCH), read once; those bytes are UTF-8 text parsed by r2's strict
#    JSON (typed codes, C.strict_json_typed); schema UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001, keys exactly {schema,
#    frozen_addendum_sha256 (= the frozen copy's sha), entries}; entries hold exactly one row per entry of L u CH, each with exactly
#    the keys of its disposition (DISPOSITION_ROW_KEYS):
#      L  rows: no_change {entry, disposition, reason, section_sha256} or revised {entry, disposition, prereg_revision, reason,
#               section_sha256};
#      CH rows: revised (as above) or no_change_after_change {entry, disposition, changed_text, why_no_prereg_effect, section_sha256};
#               changed_text is a non-empty excerpt whose UTF-8 bytes occur in the new (frozen) section and not in the old (read-copy)
#               one, so a generic string never passes; a plain no_change on a CH row refuses (PV-D05-1);
#    prereg_revision is an exact {path, sha256} pin of an existing regular file whose bytes hash to it, and it is not the prereg
#    under check (by resolved path or by sha); section_sha256 is the frozen section's sha; reason and why_no_prereg_effect are
#    non-empty after strip. L u CH empty: the file is optional; non-empty: it is required (DISPOSITIONS_REQUIRED). The disposition
#    layer runs only on a verified read copy (otherwise LAYER_SKIPPED, and the tool refuses on the read-copy code);
#  - the verified file (pin, parsed content, exact text) is returned as later_entry_dispositions, and the read copy's pin as
#    addendum_at_text_of_record, for tools 3 and 4.
# usage: python3 -I -B check_frozen_addendum_c4v003.py --prereg P.json --frozen F.md --addendum-at-text-of-record A.md
#        [--expect-frozen-sha H] [--dispositions D.json --dispositions-sha H] [--allow-open-copy-for-dry-run]
import os, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import seal_common_c4v003 as C

SRC_RX = re.compile(r'^A(\d{1,3})(?![\d])')
RANGE_RX = re.compile(r'\bA(\d{1,3})-A(\d{1,3})\b')
FROZEN_SUFFIX = '_V005_ADDENDUM_FROZEN.md'
FIRST_TABLE_ENTRY = 82            # A81 RI-26 / A99.3: the table runs from A82 to the freeze
ENTRY_TABLE_KEYS = ('entries_after_A81',)      # prereg r5 (dry run 1528164 read 2026-10-18T20:59Z); the first key present is read
TABLE_DECISIONS = ('REVISED_HERE', 'NO_CHANGE')
ADDENDUM_READ_KEY = 'addendum_read'            # v003 D-05 (0640): prereg r5 {open_path, sha256_at_generation, bytes, byte_copy}
DISPOSITIONS_KEYS = {'schema', 'frozen_addendum_sha256', 'entries'}             # v003 D-05: the file's exact key set
DISPOSITION_ROW_KEYS = {                                                        # v003 D-05 (0640): the exact keys of each disposition
    'no_change': {'entry', 'disposition', 'reason', 'section_sha256'},
    'revised': {'entry', 'disposition', 'prereg_revision', 'reason', 'section_sha256'},
    'no_change_after_change': {'entry', 'disposition', 'changed_text', 'why_no_prereg_effect', 'section_sha256'}}
DISPOSITION_ENTRY_RX = re.compile(r'A([1-9][0-9]{0,2})')                       # v003 D-05: A<n>, ASCII digits, no leading zero


def cited_entries(doc):
    out = set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'sources' and isinstance(v, list):
                    for s in v:
                        if isinstance(s, str):
                            m = SRC_RX.match(s)
                            if m:
                                out.add(int(m.group(1)))
                            for a, b in RANGE_RX.findall(s):
                                out.update(range(int(a), int(b) + 1))
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(doc)
    for s in doc.get('cites_by_name', []):
        for a, b in RANGE_RX.findall(s):
            out.update(range(int(a), int(b) + 1))
    return out


def headings(text):
    return [int(n) for n in re.findall(r'^## A(\d{1,3}):', text, re.M)]


def sections(raw):
    """{n: [(heading line, section bytes)]} for every '## A<n>:' heading of the frozen bytes, by the prereg r5 section_rule"""
    starts = [m.start() for m in re.finditer(rb'(?m)^## ', raw)]
    out = {}
    for i, st in enumerate(starts):
        m = re.match(rb'## A(\d{1,3}):', raw[st:st + 12])
        if not m:
            continue
        en = starts[i + 1] if i + 1 < len(starts) else len(raw)
        le = raw.find(b'\n', st)
        out.setdefault(int(m.group(1)), []).append((raw[st:(le if 0 <= le < en else en)].decode('utf-8'), raw[st:en]))
    return out


def entry_table(doc):
    """(key, rows) of the A99.3 table in its prereg r5 form; rows = [{n, decision, section_sha256, section_bytes, heading}];
    (None, None) when no table key is present; raises ValueError naming the first malformed row."""
    for key in ENTRY_TABLE_KEYS:
        if key not in doc:
            continue
        t = doc[key]
        if not (isinstance(t, dict) and isinstance(t.get('rows'), list)):
            raise ValueError('%s must be an object with a rows list (prereg r5 form)' % key)
        out = []
        for i, r in enumerate(t['rows']):
            w = '%s.rows[%d]' % (key, i)
            if not isinstance(r, dict):
                raise ValueError('%s is not an object' % w)
            m = re.fullmatch(r'A(\d{1,3})', r.get('entry') if isinstance(r.get('entry'), str) else '')
            if not m:
                raise ValueError('%s: entry must be A<n>' % w)
            dec = r.get('decision')
            if dec not in TABLE_DECISIONS:
                raise ValueError('%s: decision must be one of %s' % (w, ', '.join(TABLE_DECISIONS)))
            if dec == 'REVISED_HERE' and not (isinstance(r.get('revised_clauses'), list) and r['revised_clauses']
                                              and all(isinstance(c, str) and c.strip() for c in r['revised_clauses'])):
                raise ValueError('%s: REVISED_HERE names its revised_clauses' % w)
            if dec == 'NO_CHANGE' and not (isinstance(r.get('reason'), str) and r['reason'].strip()):
                raise ValueError('%s: NO_CHANGE states its reason' % w)
            if not (isinstance(r.get('section_sha256'), str) and C.HEX64.fullmatch(r['section_sha256'])):
                raise ValueError('%s: section_sha256 must be 64 hex (read from bytes)' % w)
            out.append({'n': int(m.group(1)), 'decision': dec, 'section_sha256': r['section_sha256'],
                        'section_bytes': r.get('section_bytes'), 'heading': r.get('heading')})
        return key, out
    return None, None


def nonblank(x):
    return isinstance(x, str) and bool(x.strip())


def read_copy_bytes(chk, doc, path):
    """v003 D-05 (0640): the V005 bytes the prereg's entry table was read from. The prereg pins them in
    entries_after_A81.addendum_read (sha256_at_generation; bytes, when it states an integer); root gives the copy. Returns the bytes,
    read once, when they verify; otherwise None, after the failure."""
    t = doc.get(ENTRY_TABLE_KEYS[0])
    ar = t.get(ADDENDUM_READ_KEY) if isinstance(t, dict) else None
    want = ar.get('sha256_at_generation') if isinstance(ar, dict) else None
    if not (isinstance(want, str) and C.HEX64.fullmatch(want)):
        chk.fail('ADDENDUM_READ_PIN_ABSENT', 'the prereg pins the V005 bytes its entry table was read from in %s.%s.sha256_at_generation '
                 '(64 hex); found %r' % (ENTRY_TABLE_KEYS[0], ADDENDUM_READ_KEY, want))
        want = None
    if isinstance(path, os.PathLike):
        path = os.fspath(path)
    if not (isinstance(path, str) and path):
        chk.fail('ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED', 'root gives the V005 copy the text of record was written against '
                 '(--addendum-at-text-of-record A.md; API text_of_record_addendum=PATH)')
        return None
    p = Path(path)
    if not p.is_file():
        chk.fail('ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED', 'not a regular file: %s' % path)
        return None
    raw = p.read_bytes()
    got = C.sha_bytes(raw)
    if want is None:
        return None
    if got != want:
        chk.fail('ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH', '%s has %s; the prereg pins %s (addendum_read.sha256_at_generation)' % (path, got, want))
        return None
    n = ar.get('bytes')
    if type(n) is int and n != len(raw):
        chk.fail('ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH', '%s has %d bytes; the prereg states %d (addendum_read.bytes)' % (path, len(raw), n))
        return None
    chk.pins['addendum_at_text_of_record'] = {'path': str(p.resolve()), 'sha256': got}
    return raw


def dispositions_file(chk, dispositions):
    """v003 D-05: root's pin (path, sha256) of the dispositions file: an absolute path to a regular file whose bytes hash to sha256; the
    bytes are read once and are the ones parsed. Else DISPOSITIONS_PIN_MISMATCH. Returns (path, sha256, raw) or None."""
    if not (isinstance(dispositions, (tuple, list)) and len(dispositions) == 2 and all(isinstance(x, str) for x in dispositions)):
        chk.fail('DISPOSITIONS_PIN_MISMATCH', 'the dispositions pin is (path, sha256), both given: %r' % (dispositions,))
        return None
    p, h = dispositions
    if not Path(p).is_absolute():
        chk.fail('DISPOSITIONS_PIN_MISMATCH', 'not an absolute path: %r' % p)
        return None
    if not Path(p).is_file():
        chk.fail('DISPOSITIONS_PIN_MISMATCH', 'not a regular file: %s' % p)
        return None
    raw = Path(p).read_bytes()
    got = C.sha_bytes(raw)
    if got != h:
        chk.fail('DISPOSITIONS_PIN_MISMATCH', '%s has %s; root pinned %r' % (p, got, h))
        return None
    return p, h, raw


def changed_text_codes(chk, w, ct, new, old):
    """0640: changed_text is an exact excerpt of the change: a non-empty string whose UTF-8 bytes occur in the new (frozen) section
    and do not occur in the old (read-copy) section. Generic strings fail one of the two substring tests."""
    if not (isinstance(ct, str) and ct):
        chk.fail('DISPOSITION_CHANGED_TEXT_EMPTY', '%s: changed_text is a non-empty string, an exact excerpt of the new section' % w)
        return
    try:
        b = ct.encode('utf-8')
    except UnicodeEncodeError as e:
        chk.fail('DISPOSITION_CHANGED_TEXT_ENCODING', '%s: changed_text has no UTF-8 form (%s)' % (w, str(e)[:120]))
        return
    if b not in new:
        chk.fail('DISPOSITION_CHANGED_TEXT_NOT_IN_NEW_SECTION', '%s: changed_text %r is not a substring of the frozen section bytes' % (w, ct[:80]))
    if b in old:
        chk.fail('DISPOSITION_CHANGED_TEXT_IN_OLD_SECTION', '%s: changed_text %r is also a substring of the section the text of record was '
                 'written against, so it does not name the change' % (w, ct[:80]))


def prereg_revision_codes(chk, w, ref, prereg_real, prereg_sha):
    """0640: a revised row points to the prereg revision: an exact {path, sha256} pin of an existing regular file whose bytes hash to
    it (the Checker.pin rule), and not the prereg under check (by resolved path or by sha)."""
    sub = C.Checker('prereg_revision')
    if not sub.pin('%s.prereg_revision' % w, ref):
        for f in sub.failures:
            chk.fail('DISPOSITION_PREREG_REVISION_PIN', '%s: %s %s' % (w, f['code'], f['detail']))
        return
    if str(Path(ref['path']).resolve()) == prereg_real or ref['sha256'] == prereg_sha:
        chk.fail('DISPOSITION_PREREG_REVISION_IS_THE_PREREG', '%s: prereg_revision is the prereg under check (%s), not a revision of it' % (w, prereg_sha[:8]))
        return
    chk.pins['%s.prereg_revision' % w] = dict(ref)


def disposition_codes(chk, obj, fsha, secs, rsecs, hset, table, ch, l_set, last, prereg):
    """v003 D-05: the parsed dispositions object against the frozen bytes (secs) and the read copy (rsecs). ch = CH, l_set = L. Every
    defect is a failure. Returns the set of entries that have a row (a defective row included), so a missing row is told apart from a
    defective one."""
    seen = set()
    if not isinstance(obj, dict):
        chk.fail('DISPOSITIONS_SHAPE', 'the dispositions file is not a JSON object')
        return seen
    if set(obj) != DISPOSITIONS_KEYS:
        chk.fail('DISPOSITIONS_KEYS', 'keys exactly %s: missing %s, extra %s' % (sorted(DISPOSITIONS_KEYS), sorted(DISPOSITIONS_KEYS - set(obj)),
                                                                              sorted(set(obj) - DISPOSITIONS_KEYS)))
    if 'schema' in obj and obj['schema'] != C.DISPOSITIONS_SCHEMA:
        chk.fail('DISPOSITIONS_SCHEMA', '%r; the schema is %s' % (obj['schema'], C.DISPOSITIONS_SCHEMA))
    if 'frozen_addendum_sha256' in obj and obj['frozen_addendum_sha256'] != fsha:
        chk.fail('DISPOSITIONS_FROZEN_SHA_MISMATCH', 'the file names %r; the frozen copy is %s' % (obj['frozen_addendum_sha256'], fsha))
    rows = obj.get('entries')
    if not isinstance(rows, list):
        chk.fail('DISPOSITIONS_ENTRIES_SHAPE', 'entries must be a list of rows')
        return seen
    prereg_real, prereg_sha = str(Path(prereg).resolve()), C.sha(prereg)
    for i, r in enumerate(rows):
        w = 'entries[%d]' % i
        if not isinstance(r, dict):
            chk.fail('DISPOSITION_ROW_SHAPE', '%s is not an object' % w)
            continue
        e = r.get('entry')
        m = DISPOSITION_ENTRY_RX.fullmatch(e) if isinstance(e, str) else None
        if not m:
            chk.fail('DISPOSITION_ENTRY_FORMAT', '%s: entry must be A<n> (no leading zero): %r' % (w, e))
            continue
        n = int(m.group(1))
        w = '%s A%d' % (w, n)
        if n in seen:
            chk.fail('DISPOSITION_DUPLICATE_ENTRY', '%s: the entry has a row already (A71)' % w)
            continue
        seen.add(n)
        if n not in hset:
            chk.fail('DISPOSITION_ENTRY_NOT_IN_FROZEN', '%s is not an entry of the frozen bytes' % w)
            continue
        if n not in ch and n not in l_set:
            if n in table:
                chk.fail('DISPOSITION_FOR_TABLED_ENTRY', '%s has an unchanged table row in the prereg; one decision per entry (A99.3)' % w)
            if n <= last:
                chk.fail('DISPOSITION_FOR_CITED_ENTRY', '%s is at or before the last cited entry A%d and its section did not change' % (w, last))
            continue
        d = r.get('disposition')
        if not (isinstance(d, str) and d in DISPOSITION_ROW_KEYS):
            chk.fail('DISPOSITION_VALUE', '%s: disposition %r, one of %s' % (w, d, ', '.join(sorted(DISPOSITION_ROW_KEYS))))
        else:
            if d == 'no_change' and n in ch:
                chk.fail('DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY', '%s: its section changed after the text of record was written; the '
                         'disposition is revised or no_change_after_change, never plain no_change (0640, PV-D05-1)' % w)
            if d == 'no_change_after_change' and n in l_set:
                chk.fail('DISPOSITION_NO_CHANGE_AFTER_CHANGE_ON_UNCHANGED_ENTRY', '%s did not change against the text of record\'s bytes; '
                         'no_change_after_change is for a changed entry only' % w)
            want = DISPOSITION_ROW_KEYS[d]
            if set(r) != want:
                chk.fail('DISPOSITION_ROW_KEYS', '%s: a %s row has exactly %s: missing %s, extra %s' % (w, d, sorted(want), sorted(want - set(r)),
                                                                                                     sorted(set(r) - want)))
            if d == 'revised' and 'prereg_revision' not in r:
                chk.fail('DISPOSITION_PREREG_REVISION_REQUIRED', '%s: a revised row points to the prereg revision {path, sha256}' % w)
        if 'section_sha256' in r and r['section_sha256'] != C.sha_bytes(secs[n][0][1]):
            chk.fail('DISPOSITION_SECTION_SHA_MISMATCH', '%s: section_sha256 %r; the frozen section hashes to %s' % (w, r['section_sha256'],
                                                                                                            C.sha_bytes(secs[n][0][1])))
        if 'reason' in r and not nonblank(r['reason']):
            chk.fail('DISPOSITION_REASON_EMPTY', '%s: the reason is a non-empty string (after strip)' % w)
        if 'why_no_prereg_effect' in r and not nonblank(r['why_no_prereg_effect']):
            chk.fail('DISPOSITION_WHY_NO_PREREG_EFFECT_EMPTY', '%s: why_no_prereg_effect is a non-empty string (after strip)' % w)
        if 'changed_text' in r:
            changed_text_codes(chk, w, r['changed_text'], secs[n][0][1], rsecs[n][0][1] if n in rsecs else b'')
        if 'prereg_revision' in r:
            prereg_revision_codes(chk, w, r['prereg_revision'], prereg_real, prereg_sha)
    return seen


def _run(prereg, frozen, expect_frozen_sha=None, covered_later=(), allow_open=False, dispositions=None, text_of_record_addendum=None):
    chk = C.Checker('check_frozen_addendum_c4v003')
    try:
        doc = C.strict_json(prereg)
    except Exception as e:
        chk.fail('PREREG_JSON', type(e).__name__ + ': ' + str(e))
        return chk.result()
    if not isinstance(doc, dict):
        chk.fail('PREREG_SHAPE', 'the prereg is not a JSON object')
        return chk.result()
    fz = Path(frozen)
    if not fz.is_file():
        chk.fail('FROZEN_MISSING', str(fz))
        return chk.result()
    if not fz.name.endswith(FROZEN_SUFFIX):
        if allow_open:
            chk.note('DRY_RUN_NOT_THE_FROZEN_COPY', 'dry run only, never for the seal: %s' % fz.name)
        else:
            chk.fail('NOT_THE_FROZEN_COPY', 'expected the separate ..._V005_ADDENDUM_FROZEN.md copy (0576): %s' % fz.name)
    fres = str(fz.resolve())
    fsha = C.sha(fz)
    chk.pins['frozen'] = {'path': fres, 'sha256': fsha}
    if expect_frozen_sha is not None and fsha != expect_frozen_sha:
        chk.fail('FROZEN_SHA_MISMATCH', 'file %s, expected %s' % (fsha, expect_frozen_sha))
    fa = (doc.get('seal_slots') or {}).get('frozen_addendum')
    fa = fa if isinstance(fa, dict) else {}
    # D-10: the frozen copy sits exactly where the prereg says root creates it
    ptb = fa.get('path_to_be')
    if not (isinstance(ptb, str) and Path(ptb).is_absolute()):
        chk.fail('FROZEN_PATH_TO_BE_ABSENT', 'seal_slots.frozen_addendum.path_to_be must name the absolute path of the frozen copy (D-10)')
    elif fres != ptb:
        if allow_open:
            chk.note('DRY_RUN_FROZEN_PATH_NOT_PATH_TO_BE', 'dry run only, never for the seal: %s, path_to_be %s' % (fres, ptb))
        else:
            chk.fail('FROZEN_PATH_NOT_PATH_TO_BE', 'the frozen copy is %s; the prereg puts it at %s (D-10)' % (fres, ptb))
    slot = fa.get('value')
    if isinstance(slot, dict):
        if slot != {'path': fres, 'sha256': fsha}:
            chk.fail('PREREG_SLOT_DIFFERS', 'prereg frozen_addendum slot %r vs file %s %s' % (slot, fres, fsha))
    else:
        chk.note('PREREG_SLOT_NOT_FILLED', 'the prereg\'s frozen_addendum slot holds no pin (draft or dry run)')
    text = fz.read_bytes().decode('utf-8')
    hs = headings(text)
    hset = set(hs)
    dup = sorted({n for n in hs if hs.count(n) > 1})
    if dup:
        chk.fail('DUPLICATE_ENTRY_HEADING', ', '.join('A%d' % n for n in dup))
    cited = cited_entries(doc)
    chk.notes.append({'code': 'CITED_ENTRIES', 'detail': 'A%d-A%d (%d entries cited)' % (min(cited), max(cited), len(cited)) if cited else 'none'})
    missing_v005 = sorted(n for n in cited if n >= 47 and n not in hset)
    if missing_v005:
        chk.fail('CITED_ENTRY_ABSENT_FROM_FROZEN', ', '.join('A%d' % n for n in missing_v005))
    old = sorted(n for n in cited if n < 47)
    if old:
        older = ''
        dpf = doc.get('decision_pins_frozen') or {}
        for k, ref in (dpf.items() if isinstance(dpf, dict) else []):
            if chk.pin('decision_pins_frozen.' + k, ref):
                older += Path(ref['path']).read_bytes().decode('utf-8') + '\n'
        oh = set(headings(older))
        miss_old = [n for n in old if n not in oh]
        if miss_old:
            chk.fail('CITED_EARLY_ENTRY_ABSENT', ', '.join('A%d' % n for n in miss_old))
    last = max(cited) if cited else 0
    # A99.3: the entry-by-entry table, each row re-hashed from the frozen bytes
    malformed = False
    try:
        tkey, rows = entry_table(doc)
    except ValueError as e:
        chk.fail('ENTRY_TABLE_MALFORMED', str(e))
        tkey, rows, malformed = None, [], True
    table = {}
    changed = {}
    secs = sections(fz.read_bytes())
    if tkey is None:
        if not malformed:
            chk.fail('ENTRY_TABLE_ABSENT', 'the prereg carries no entry-by-entry table (A99.3; key %s)' % ', '.join(ENTRY_TABLE_KEYS))
        rows = []
    else:
        chk.note('ENTRY_TABLE', '%s: %d rows' % (tkey, len(rows)))
    for r in rows:
        n = r['n']
        if n in table:
            chk.fail('ENTRY_TABLE_DUPLICATE_ENTRY', 'A%d is listed twice (A71)' % n)
            continue
        table[n] = r
        if n < FIRST_TABLE_ENTRY:
            chk.fail('ENTRY_TABLE_ENTRY_BEFORE_A82', 'A%d (the table runs from A82 to the freeze, A99.3)' % n)
        if n not in hset:
            chk.fail('ENTRY_TABLE_ENTRY_NOT_IN_FROZEN', 'A%d' % n)
            continue
        heading, sec = secs[n][0]
        got = C.sha_bytes(sec)
        if got != r['section_sha256'] or (r['section_bytes'] is not None and r['section_bytes'] != len(sec)) or \
                (r['heading'] is not None and r['heading'] != heading):
            changed[n] = {'entry': 'A%d' % n, 'table_row_section_sha256': r['section_sha256'], 'text_of_record_section_sha256': None,
                          'frozen_section_sha256': got}
    if tkey is not None:
        need_t = sorted(n for n in hset if FIRST_TABLE_ENTRY <= n <= last and n not in table)
        if need_t:
            chk.fail('ENTRY_TABLE_MISSING_ENTRY', 'frozen entries from A82 through the last cited entry A%d need a table row (A99.3): %s'
                     % (last, ', '.join('A%d' % n for n in need_t)))
    # v003 D-05: the bare covered-later list is removed
    if covered_later:
        chk.fail('COVERED_LATER_BARE_NAMES_REFUSED', C.COVERED_LATER_REMOVED)
    # v003 D-05 (0640): the bytes the text of record was written against
    rsecs = None
    old_raw = read_copy_bytes(chk, doc, text_of_record_addendum)
    if old_raw is not None:
        rsecs = sections(old_raw)
        rdup = sorted(n for n, v in rsecs.items() if len(v) > 1)
        if rdup:
            chk.fail('READ_COPY_DUPLICATE_ENTRY_HEADING', ', '.join('A%d' % n for n in rdup))
        miss_r = sorted(n for n in cited if n >= 47 and n not in rsecs)
        if miss_r:
            chk.fail('CITED_ENTRY_ABSENT_FROM_READ_COPY', ', '.join('A%d' % n for n in miss_r))
        gone = sorted(n for n in rsecs if n not in hset)
        if gone:
            chk.fail('READ_COPY_ENTRY_ABSENT_FROM_FROZEN', 'entries of the text of record\'s V005 bytes that the frozen copy lacks: %s'
                     % ', '.join('A%d' % n for n in gone))
        for n in sorted(table):
            r = table[n]
            if n not in rsecs:
                chk.fail('ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD', 'A%d: the read copy has no such entry' % n)
                continue
            rh, rs = rsecs[n][0]
            if r['section_sha256'] != C.sha_bytes(rs) or (r['section_bytes'] is not None and r['section_bytes'] != len(rs)) or \
                    (r['heading'] is not None and r['heading'] != rh):
                chk.fail('ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD', 'A%d: the table row is not the section of the bytes the text of record was '
                         'written against (row %s, read copy %s)' % (n, r['section_sha256'][:8], C.sha_bytes(rs)[:8]))
        for n in sorted(set(rsecs) & hset):
            o, nw = rsecs[n][0][1], secs[n][0][1]
            if o != nw:
                c = changed.setdefault(n, {'entry': 'A%d' % n, 'table_row_section_sha256': None, 'frozen_section_sha256': C.sha_bytes(nw)})
                c['text_of_record_section_sha256'] = C.sha_bytes(o)
    later = sorted(n for n in hset if n > last)
    seen, verified, need = set(), None, None
    if rsecs is None:
        chk.note('LAYER_SKIPPED', 'D-05 dispositions: needs the verified read copy of the V005 bytes the text of record was written against')
    else:
        ch = set(changed)
        l_set = ({n for n in later if n not in table} | {n for n in hset if n not in rsecs}) - ch
        need = sorted(l_set | ch)
        if dispositions is None:
            if need:
                chk.fail('DISPOSITIONS_REQUIRED', 'root\'s dispositions file (--dispositions D.json --dispositions-sha H) must give a row for each of %s '
                         '(D-05; A81 RI-26)' % ', '.join('A%d' % n for n in need))
        else:
            got = dispositions_file(chk, dispositions)
            if got is not None:
                dpath, dsha, draw = got
                obj, dtext, bad = C.strict_json_typed(draw, 'DISPOSITIONS')
                if bad is not None:
                    chk.fail(*bad)
                else:
                    before = len(chk.failures)
                    seen = disposition_codes(chk, obj, fsha, secs, rsecs, hset, table, ch, l_set, last, prereg)
                    if len(chk.failures) == before and all(n in seen for n in need):
                        verified = {'pin': {'path': dpath, 'sha256': dsha}, 'content': obj, 'raw_text': dtext}
                        chk.pins['dispositions'] = {'path': dpath, 'sha256': dsha}
                        chk.note('DISPOSITIONS_VERIFIED', '%s %s: %s' % (dpath, dsha[:8], ', '.join('A%d %s' % (n, next(
                            r['disposition'] for r in obj['entries'] if r['entry'] == 'A%d' % n)) for n in need) or 'no rows (none needed)'))
        for n in sorted(ch):
            if n in seen:
                chk.note('ENTRY_TABLE_SECTION_CHANGED_NOTED' if n in table else 'ENTRY_SECTION_CHANGED_NOTED',
                         'A%d: its section changed after the text of record was written; root\'s dispositions row disposes of it' % n)
            elif n in table:
                chk.fail('ENTRY_TABLE_SECTION_CHANGED', 'A%d: the frozen section hashes to %s, the table row says %s; a revised or '
                         'no_change_after_change row in root\'s dispositions file is needed (D-05, 0640; A81 RI-26)'
                         % (n, changed[n]['frozen_section_sha256'][:8], changed[n]['table_row_section_sha256'][:8]))
            else:
                chk.fail('ENTRY_SECTION_CHANGED', 'A%d%s: its section changed after the text of record was written (read copy %s, frozen %s); a revised '
                         'or no_change_after_change row in root\'s dispositions file is needed (D-05, 0640; C-01)'
                         % (n, ' (cited)' if n in cited else '', changed[n]['text_of_record_section_sha256'][:8], changed[n]['frozen_section_sha256'][:8]))
        uncovered = [n for n in sorted(l_set) if n not in seen]
        if uncovered:
            chk.fail('UNCOVERED_LATER_ENTRY', 'entries after A%d with no table row, or absent from the text of record\'s V005 bytes, need a row in '
                     'root\'s dispositions file (D-05; A81 RI-26; A99.3): %s' % (last, ', '.join('A%d' % n for n in uncovered)))
    psha = C.sha(prereg)
    chk.pins['prereg'] = {'path': str(Path(prereg).resolve()), 'sha256': psha}
    if psha in text:
        chk.fail('FROZEN_CITES_SEALED_PREREG_SHA', 'the frozen addendum contains the prereg\'s own sha (pin cycle, RI-27 / A82)')
    elif psha[:8] in text:
        chk.note('PREREG_SHA_PREFIX_SEEN', 'the first 8 hex of the prereg sha occur in the frozen text; check it is a coincidence, not a citation')
    res = chk.result()
    res['entry_table'] = {'key': tkey, 'rows': [['A%d' % r['n'], r['decision']] for r in rows]} if tkey is not None else None
    res['changed_sections'] = [changed[n] for n in sorted(changed)]
    res['later_entries'] = ['A%d' % n for n in later]
    res['dispositions_required'] = None if need is None else ['A%d' % n for n in need]
    res['later_entry_dispositions'] = verified
    res['addendum_at_text_of_record'] = chk.pins.get('addendum_at_text_of_record')
    return res


def run(prereg, frozen, expect_frozen_sha=None, covered_later=(), allow_open=False, dispositions=None, text_of_record_addendum=None):
    return C.guarded_run('check_frozen_addendum_c4v003', _run, prereg, frozen, expect_frozen_sha, covered_later, allow_open, dispositions,
                         text_of_record_addendum)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if C.covered_later_flag(argv):                       # v003 D-05: the removed flag is a typed refusal, not a usage error
        return C.emit(C.covered_later_refusal('check_frozen_addendum_c4v003'))
    p = C.parser('frozen V005 addendum vs the prereg\'s cited entries, its entry table (A99.3), path_to_be (D-10), the V005 bytes the text of '
                 'record was written against and root\'s dispositions (D-05)')
    p.add_argument('--prereg', required=True)
    p.add_argument('--frozen', required=True)
    p.add_argument('--addendum-at-text-of-record')
    p.add_argument('--expect-frozen-sha')
    p.add_argument('--dispositions')
    p.add_argument('--dispositions-sha')
    p.add_argument('--allow-open-copy-for-dry-run', action='store_true')
    a = C.parse_args(p, argv)
    disp = None if a.dispositions is None and a.dispositions_sha is None else (a.dispositions, a.dispositions_sha)
    return C.emit(run(a.prereg, a.frozen, a.expect_frozen_sha, (), a.allow_open_copy_for_dry_run, disp, a.addendum_at_text_of_record))


if __name__ == '__main__':
    raise SystemExit(main())
