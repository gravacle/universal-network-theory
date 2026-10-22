# Claude4 (dispatch 0584) seal tool 1: the frozen V005 addendum contains every A-entry the prereg cites. Read-only.
# Cited entries are taken from the prereg's structured `sources` lists and its cites_by_name range, never from prose (so labels such as
# "A75 A01" count as A75 only). Entries >= A47 must be `## A<n>:` headings in the frozen V005 bytes (each exactly once); entries <= A46
# must be headings in one of the frozen decision files the prereg pins (decision_pins_frozen, each verified from bytes). Also refused:
# a frozen file that is not the separate ..._FROZEN.md copy (0576), a sha that differs from the slot, the sealed prereg's own sha inside
# the frozen bytes (RI-27 / A82), and any entry after the last cited one that root's no-change list does not cover (A81 RI-26; A82).
# usage: python3 -I -B check_frozen_addendum_c4v001.py --prereg P.json --frozen F.md [--expect-frozen-sha H] [--covered-later A82,A83]
#        [--allow-open-copy-for-dry-run]
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import seal_common_c4v001 as C

SRC_RX = re.compile(r'^A(\d{1,3})(?![\d])')
RANGE_RX = re.compile(r'\bA(\d{1,3})-A(\d{1,3})\b')


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


def run(prereg, frozen, expect_frozen_sha=None, covered_later=(), allow_open=False):
    chk = C.Checker('check_frozen_addendum_c4v001')
    try:
        doc = C.strict_json(prereg)
    except Exception as e:
        chk.fail('PREREG_JSON', type(e).__name__ + ': ' + str(e))
        return chk.result()
    fz = Path(frozen)
    if not fz.is_file():
        chk.fail('FROZEN_MISSING', str(fz))
        return chk.result()
    if not fz.name.endswith('_V005_ADDENDUM_FROZEN.md') and not allow_open:
        chk.fail('NOT_THE_FROZEN_COPY', 'expected the separate ..._V005_ADDENDUM_FROZEN.md copy (0576): %s' % fz.name)
    fsha = C.sha(fz)
    chk.pins['frozen'] = {'path': str(fz.resolve()), 'sha256': fsha}
    if expect_frozen_sha is not None and fsha != expect_frozen_sha:
        chk.fail('FROZEN_SHA_MISMATCH', 'file %s, expected %s' % (fsha, expect_frozen_sha))
    slot = (doc.get('seal_slots') or {}).get('frozen_addendum', {}).get('value')
    if isinstance(slot, dict):
        if slot != {'path': str(fz.resolve()), 'sha256': fsha}:
            chk.fail('PREREG_SLOT_DIFFERS', 'prereg frozen_addendum slot %r vs file %s %s' % (slot, fz, fsha))
    else:
        chk.note('PREREG_SLOT_NOT_FILLED', 'the prereg\'s frozen_addendum slot holds no pin (draft or dry run)')
    text = fz.read_bytes().decode('utf-8')
    hs = headings(text)
    dup = sorted({n for n in hs if hs.count(n) > 1})
    if dup:
        chk.fail('DUPLICATE_ENTRY_HEADING', ', '.join('A%d' % n for n in dup))
    cited = cited_entries(doc)
    chk.notes.append({'code': 'CITED_ENTRIES', 'detail': 'A%d-A%d (%d entries cited)' % (min(cited), max(cited), len(cited)) if cited else 'none'})
    missing_v005 = sorted(n for n in cited if n >= 47 and n not in hs)
    if missing_v005:
        chk.fail('CITED_ENTRY_ABSENT_FROM_FROZEN', ', '.join('A%d' % n for n in missing_v005))
    old = sorted(n for n in cited if n < 47)
    if old:
        older = ''
        for k, ref in (doc.get('decision_pins_frozen') or {}).items():
            if chk.pin('decision_pins_frozen.' + k, ref):
                older += Path(ref['path']).read_bytes().decode('utf-8') + '\n'
        oh = set(headings(older))
        miss_old = [n for n in old if n not in oh]
        if miss_old:
            chk.fail('CITED_EARLY_ENTRY_ABSENT', ', '.join('A%d' % n for n in miss_old))
    last = max(cited) if cited else 0
    cov = set()
    for a in covered_later:
        m = re.fullmatch(r'A(\d{1,3})', a.strip())
        if not m:
            chk.fail('COVERED_LATER_FORMAT', a)
            continue
        cov.add(int(m.group(1)))
    for n in sorted(cov):
        if n not in hs:
            chk.fail('COVERED_LATER_NOT_IN_FROZEN', 'A%d' % n)
        if n <= last:
            chk.fail('COVERED_LATER_IS_CITED', 'A%d is cited by the prereg; a no-change note is for later entries only' % n)
    later = sorted(n for n in set(hs) if n > last)
    uncovered = [n for n in later if n not in cov]
    if uncovered:
        chk.fail('UNCOVERED_LATER_ENTRY', 'entries after A%d need a revision or a no-change note (A81 RI-26): %s' % (last, ', '.join('A%d' % n for n in uncovered)))
    psha = C.sha(prereg)
    chk.pins['prereg'] = {'path': str(Path(prereg).resolve()), 'sha256': psha}
    if psha in text:
        chk.fail('FROZEN_CITES_SEALED_PREREG_SHA', 'the frozen addendum contains the prereg\'s own sha (pin cycle, RI-27 / A82)')
    elif psha[:8] in text:
        chk.note('PREREG_SHA_PREFIX_SEEN', 'the first 8 hex of the prereg sha occur in the frozen text; check it is a coincidence, not a citation')
    return chk.result()


def main(argv=None):
    p = C.parser('frozen V005 addendum vs the prereg\'s cited entries')
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
