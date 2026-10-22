# Claude4 seal tools v002, tool 1 (successor of check_frozen_addendum_c4v001.py c4ebbb5b): the frozen V005 addendum contains every
# A-entry the prereg cites, and every later entry is accounted for. Read-only.
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
# usage: python3 -I -B check_frozen_addendum_c4v002.py --prereg P.json --frozen F.md [--expect-frozen-sha H]
#        [--covered-later A100,A101] [--allow-open-copy-for-dry-run]
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import seal_common_c4v002 as C

SRC_RX = re.compile(r'^A(\d{1,3})(?![\d])')
RANGE_RX = re.compile(r'\bA(\d{1,3})-A(\d{1,3})\b')
FROZEN_SUFFIX = '_V005_ADDENDUM_FROZEN.md'
FIRST_TABLE_ENTRY = 82            # A81 RI-26 / A99.3: the table runs from A82 to the freeze
ENTRY_TABLE_KEYS = ('entries_after_A81',)      # prereg r5 (dry run 1528164 read 2026-10-18T20:59Z); the first key present is read
TABLE_DECISIONS = ('REVISED_HERE', 'NO_CHANGE')


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


def _run(prereg, frozen, expect_frozen_sha=None, covered_later=(), allow_open=False):
    chk = C.Checker('check_frozen_addendum_c4v002')
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
    table = set()
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
        table.add(n)
        if n < FIRST_TABLE_ENTRY:
            chk.fail('ENTRY_TABLE_ENTRY_BEFORE_A82', 'A%d (the table runs from A82 to the freeze, A99.3)' % n)
        if n not in hset:
            chk.fail('ENTRY_TABLE_ENTRY_NOT_IN_FROZEN', 'A%d' % n)
            continue
        heading, sec = secs[n][0]
        got = C.sha_bytes(sec)
        if got != r['section_sha256'] or (r['section_bytes'] is not None and r['section_bytes'] != len(sec)) or \
                (r['heading'] is not None and r['heading'] != heading):
            changed[n] = {'entry': 'A%d' % n, 'row_section_sha256': r['section_sha256'], 'frozen_section_sha256': got}
    if tkey is not None:
        need = sorted(n for n in hset if FIRST_TABLE_ENTRY <= n <= last and n not in table)
        if need:
            chk.fail('ENTRY_TABLE_MISSING_ENTRY', 'frozen entries from A82 through the last cited entry A%d need a table row (A99.3): %s'
                     % (last, ', '.join('A%d' % n for n in need)))
    # D-05: --covered-later is an explicit list
    cov = set()
    for a in covered_later:
        m = re.fullmatch(r'A(\d{1,3})', a.strip())
        if not m:
            chk.fail('COVERED_LATER_FORMAT', '%r: an explicit list of A<n> items, no ranges (D-05)' % a)
            continue
        n = int(m.group(1))
        if n in cov:
            chk.fail('COVERED_LATER_DUPLICATE', 'A%d is listed twice' % n)
        cov.add(n)
    for n in sorted(cov):
        if n not in hset:
            chk.fail('COVERED_LATER_NOT_IN_FROZEN', 'A%d' % n)
        if n in changed:
            continue                     # a table row whose section changed: root's explicit seal-record note (A81 RI-26)
        if n <= last:
            chk.fail('COVERED_LATER_IS_CITED', 'A%d is cited by the prereg; a no-change note is for later entries (or a changed table row) only' % n)
        if n in table:
            chk.fail('COVERED_LATER_IN_ENTRY_TABLE', 'A%d has a table row in the prereg; one decision per entry (A99.3)' % n)
    for n in sorted(changed):
        if n in cov:
            chk.note('ENTRY_TABLE_SECTION_CHANGED_NOTED', 'A%d: its section changed after the text of record was written; root lists it in --covered-later' % n)
        else:
            chk.fail('ENTRY_TABLE_SECTION_CHANGED', 'A%d: the frozen section hashes to %s, the table row says %s; a successor revision, or root\'s explicit '
                     'seal-record note (--covered-later A%d), is needed (A81 RI-26)' % (n, changed[n]['frozen_section_sha256'][:8], changed[n]['row_section_sha256'][:8], n))
    later = sorted(n for n in hset if n > last)
    uncovered = [n for n in later if n not in cov and n not in table]
    if uncovered:
        chk.fail('UNCOVERED_LATER_ENTRY', 'entries after A%d need a table row or a no-change note (A81 RI-26; A99.3): %s'
                 % (last, ', '.join('A%d' % n for n in uncovered)))
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
    res['covered_later'] = ['A%d' % n for n in sorted(cov)]
    return res


def run(prereg, frozen, expect_frozen_sha=None, covered_later=(), allow_open=False):
    return C.guarded_run('check_frozen_addendum_c4v002', _run, prereg, frozen, expect_frozen_sha, covered_later, allow_open)


def main(argv=None):
    p = C.parser('frozen V005 addendum vs the prereg\'s cited entries, its entry table (A99.3) and path_to_be (D-10)')
    p.add_argument('--prereg', required=True)
    p.add_argument('--frozen', required=True)
    p.add_argument('--expect-frozen-sha')
    p.add_argument('--covered-later', default='')
    p.add_argument('--allow-open-copy-for-dry-run', action='store_true')
    a = C.parse_args(p, argv)
    cov = [x for x in a.covered_later.split(',') if x.strip()]
    return C.emit(run(a.prereg, a.frozen, a.expect_frozen_sha, cov, a.allow_open_copy_for_dry_run))


if __name__ == '__main__':
    raise SystemExit(main())
