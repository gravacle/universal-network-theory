# Claude4 (dispatch 0585) target-free check for the miss-reading prereg r2. Read-only apart from --out (exclusive create).
# It never opens target data, so it cannot compare the text with target values. Instead it proves the text is target-free by construction:
#  T1 no forbidden target term (data-file names, data-source names, data extensions) anywhere in the r2 text files;
#  T2 no number carrying a velocity unit; T3 no target symbol (v_q, sigma_q, observed speed) set equal to a number;
#  T4 every numeric token of the prereg text is listed in the provenance file with a target-free source, and every query radius
#     claimed there equals the Rad_text of that query id in the target-free slots V003 query block (bytes pinned);
#  T5 every source file the prereg's section 11 pins exists, has a target-free path, and hashes to the stated sha256;
#  T6 every clause tag in the prereg has exactly one row in the clause source map, and every map row names a tag in the text.
# An audit hook refuses any open whose path contains a forbidden term, and any write other than --out.
# usage: python3 -I -B check_target_free_c4v001.py --dir R2DIR --provenance NUMBER_PROVENANCE_R2.json --slots SLOTS.json
#        --expect-slots-sha H [--out RESULT.json]
import argparse, hashlib, json, os, re, sys

FORBIDDEN = ('rotmod', 'vobs', 'v_obs', 'massmodels', 'sparc', 'lelli', 'begeman')
FORBIDDEN_EXT = re.compile(r'\.(dat|mrt|csv|fits|fit|tbl|ecsv)\b', re.I)
TEXT_FILES = ('PREREG_MISS_READING_R2.md', 'CLAUSE_SOURCE_MAP_R2.md', 'ROOT_ITEMS_R2.md')
_OUT = []


def _hook(event, args):
    if event == 'open':
        path = args[0]
        if isinstance(path, int):
            return
        p = os.fsdecode(path) if isinstance(path, bytes) else str(path)
        low = p.lower()
        if any(w in low for w in FORBIDDEN):
            raise PermissionError('target-like path refused: %s' % p)
        mode = args[1] if len(args) > 1 and isinstance(args[1], str) else 'r'
        flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
        writing = any(c in mode for c in 'wax+') or (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND))
        if writing and os.path.abspath(p) not in _OUT:
            raise PermissionError('write refused: %s' % p)
    elif event in ('os.remove', 'os.rename', 'os.rmdir', 'shutil.rmtree', 'subprocess.Popen', 'os.system', 'socket.connect'):
        raise PermissionError('refused: %s' % event)


def strict_load(path):
    def hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError('duplicate key %r in %s' % (k, path))
            d[k] = v
        return d
    with open(path, 'rb') as f:
        return json.loads(f.read().decode('utf-8'), object_pairs_hook=hook,
                          parse_constant=lambda c: (_ for _ in ()).throw(ValueError('non-finite %s' % c)))


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


HEX = re.compile(r'\b[0-9a-f]{8,64}\b')
ELIDED = re.compile(r'`[0-9a-f]{6,}…`')
# identifiers that contain digits but are not quantities: entry and item ids, query ids, labels, file names, code names
IDENT = re.compile(r'(?<![\w.])(?:[A-Za-z][A-Za-z0-9_′]*(?:[-.][A-Za-z0-9_′]+)*)')
NUM = re.compile(r'(?<![\w.])\d+(?:\.\d+)?')
SECTION = re.compile(r'§\s*\d+(?:\.\d+)?')
TAG = re.compile(r'\[(C-[A-Za-z0-9.]+)\]')
VEL = re.compile(r'\d(?:[\d.,]*\d)?\s*(?:km\s*/\s*s|km\s*s\s*(?:\^-1|⁻¹|-1)|kms\b)', re.I)
SYM = re.compile(r'(?:\bv_q\b|σ_q|\bsigma_q\b|observed[_ ]speed\w*|\bv_obs\b)\s*(?:=|≈|:)\s*[-+−]?\d', re.I)


def numeric_tokens(text):
    t = ELIDED.sub(' ', text)
    t = HEX.sub(' ', t)
    t = SECTION.sub(' ', t)
    t = re.sub(r'`[^`\n]*`', ' ', t)                 # code spans: field and file names, never quantities
    t = re.sub(r'\[C-[^\]]+\]', ' ', t)
    t = re.sub(r'(?<![\w.])(?:[A-Za-z][\w′]*)(?:[-./][\w′]+)+', ' ', t)   # dotted or hyphenated identifiers (A65.4, RI-23, ML_3p6_0.4)
    t = re.sub(r'\b[A-Za-z]+[\w′]*\d[\w′]*\b', ' ', t)                     # identifiers with digits (Q36, A60, P1g, K32)
    return NUM.findall(t)


def section(text, title_prefix):
    m = re.search(r'^## ' + re.escape(title_prefix) + r'.*$', text, re.M)
    if not m:
        return ''
    rest = text[m.end():]
    n = re.search(r'^## ', rest, re.M)
    return rest[:n.start()] if n else rest


ROOTS = {
    '…/FIRST_CONSTRUCTION_REVIEW_2026-10-13/': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/',
    '…/CLAUDE2/': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/',
    'claude_artifacts/': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/',
}
DISPATCH_DIR = '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/'
FREEZE_DIR = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/'
DECISIONS = {'V003': 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V003_ADDENDUM.md',
             'V004': 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md',
             'V005': 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'}


def expand(p):
    for k, v in ROOTS.items():
        if p.startswith(k):
            return v + p[len(k):]
    return p


def entry_sections(text):
    """{n: section text} for every '## A<n>:' heading: from the heading line up to the next '## ' line, or to the end."""
    lines = text.split('\n')
    starts = [i for i, l in enumerate(lines) if l.startswith('## ')]
    out = {}
    for j, i in enumerate(starts):
        m = re.match(r'^## A(\d{1,3}):', lines[i])
        if not m:
            continue
        end = starts[j + 1] if j + 1 < len(starts) else len(lines)
        body = '\n'.join(lines[i:end])
        if end < len(lines):
            body += '\n'
        n = int(m.group(1))
        out.setdefault(n, []).append(body)
    return out


def v005_entry_pins(text):
    s = section(text, '11.')
    return [(int(n), h) for n, h in re.findall(r'^\| A(\d{1,3}) \|[^\n]*`([0-9a-f]{64})` \|$', s, re.M)]


def sources_from_section11(text):
    """(label, path, sha) for every pinned source in section 11."""
    s = section(text, '11.')
    out = []
    for line in s.splitlines():
        if re.match(r'^\| A\d{1,3} \|', line):
            continue                                  # V005 per-entry pins, checked separately
        cells = [c.strip() for c in line.strip().strip('|').split('|')] if line.startswith('|') else []
        shas = re.findall(r'`([0-9a-f]{64})`', line)
        if not shas:
            if line.startswith('**Target-free query manifest**'):
                m = re.search(r'`([^`]+\.json)`, `([0-9a-f]{64})`', line)
                if m:
                    out.append(('query_manifest', expand(m.group(1)), m.group(2)))
            continue
        h = shas[-1]
        first = cells[0] if cells else ''
        if re.fullmatch(r'0\d{3}', first):
            names = [n for n in os.listdir(DISPATCH_DIR) if n.startswith(first + '_')]
            out.append(('dispatch ' + first, DISPATCH_DIR + names[0] if len(names) == 1 else 'AMBIGUOUS:' + first, h))
        elif first.startswith('V00'):
            out.append(('decisions ' + first[:4], ROOTS['…/CLAUDE2/'] + DECISIONS[first[:4]], h))
        else:
            m = re.search(r'`([^`]+\.(?:py|json|md|npz))`', line)
            if not m:
                out.append(('UNPARSED', line, h))
                continue
            p = m.group(1)
            if not p.startswith(('/', '…', 'claude_artifacts/')):
                p = FREEZE_DIR + p
            out.append((first, expand(p), h))
    return out


def run(a):
    res = {'schema': 'UNT_MISS_READING_R2_TARGET_FREE_CHECK_C4V001', 'checks': {}, 'files': {}}
    texts = {}
    for name in TEXT_FILES:
        p = os.path.join(a.dir, name)
        texts[name] = open(p, 'rb').read().decode('utf-8')
        res['files'][name] = sha(p)
    prereg = texts['PREREG_MISS_READING_R2.md']

    hits = []
    for name, t in texts.items():
        low = t.lower()
        hits += ['%s: term %r' % (name, w) for w in FORBIDDEN if w in low]
        hits += ['%s: extension %r' % (name, m.group(0)) for m in FORBIDDEN_EXT.finditer(t)]
    res['checks']['T1_FORBIDDEN_TERMS'] = {'pass': not hits, 'hits': hits}

    vel = ['%s: %r' % (n, m.group(0)) for n, t in texts.items() for m in VEL.finditer(t)]
    res['checks']['T2_NO_VELOCITY_VALUE'] = {'pass': not vel, 'hits': vel}
    sym = ['%s: %r' % (n, m.group(0)) for n, t in texts.items() for m in SYM.finditer(t)]
    res['checks']['T3_NO_TARGET_SYMBOL_VALUE'] = {'pass': not sym, 'hits': sym}

    prov = strict_load(a.provenance)
    slots_sha = sha(a.slots)
    slots = strict_load(a.slots)
    rad = {r['query_id']: r['Rad_text'] for r in slots['query_block']['rows']}
    units = {r['Rad_unit'] for r in slots['query_block']['rows']}
    toks = sorted(set(numeric_tokens(prereg)), key=lambda x: (float(x), x))
    listed = prov['numbers']
    missing = [t for t in toks if t not in listed]
    unused = [k for k in listed if k not in toks]
    bad_cat = [k for k, v in listed.items() if v.get('category') not in prov['categories']]
    radius_bad = []
    for k, v in listed.items():
        if v.get('category') == 'QUERY_RADIUS':
            ids = v.get('query_ids', [])
            if not ids or any(rad.get(q) != k for q in ids):
                radius_bad.append('%s: claimed %s, slots %s' % (k, ids, [rad.get(q) for q in ids]))
    t4 = not missing and not bad_cat and not radius_bad and slots_sha == a.expect_slots_sha and units == {'kpc'}
    res['checks']['T4_NUMBER_PROVENANCE'] = {'pass': t4, 'numeric_tokens': toks, 'missing_from_provenance': missing,
                                             'listed_but_absent': unused, 'bad_category': bad_cat, 'radius_mismatch': radius_bad,
                                             'slots_sha256': slots_sha, 'slots_sha_expected': a.expect_slots_sha, 'rad_units': sorted(units)}

    srcs = sources_from_section11(prereg)
    bad, notes = [], []
    pins = v005_entry_pins(prereg)
    entry_results = []
    for label, p, h in srcs:
        if p.startswith(('AMBIGUOUS', 'UNPARSED')) or label == 'UNPARSED':
            bad.append('%s: %s' % (label, p))
            continue
        if any(w in p.lower() for w in FORBIDDEN) or FORBIDDEN_EXT.search(p):
            bad.append('%s: target-like path %s' % (label, p))
            continue
        if not os.path.isfile(p):
            bad.append('%s: missing %s' % (label, p))
            continue
        got = sha(p)
        if label == 'decisions V005':
            # the open addendum: a whole-file change is expected; every cited entry's own section must be unchanged
            if got != h:
                notes.append('V005 whole-file sha is now %s (stated %s, read at assembly): open file; entries checked below' % (got, h))
            secs = entry_sections(open(p, 'rb').read().decode('utf-8'))
            if not pins:
                bad.append('no V005 per-entry pins found in section 11')
            for n, eh in pins:
                found = secs.get(n, [])
                if len(found) != 1:
                    bad.append('V005 A%d: %d sections with this heading' % (n, len(found)))
                    continue
                cur = hashlib.sha256(found[0].encode('utf-8')).hexdigest()
                entry_results.append({'entry': 'A%d' % n, 'stated': eh, 'current': cur, 'match': cur == eh})
                if cur != eh:
                    bad.append('V005 A%d section changed: %s, stated %s' % (n, cur, eh))
            continue
        if got != h:
            bad.append('%s: %s sha %s, stated %s' % (label, p, got, h))
    res['checks']['T5_SOURCES_TARGET_FREE_AND_PINNED'] = {'pass': not bad and len(srcs) >= 1, 'n_sources': len(srcs), 'problems': bad,
                                                          'notes': notes, 'v005_entries': entry_results,
                                                          'sources': [{'label': l, 'path': p, 'sha256': h} for l, p, h in srcs]}

    tags = TAG.findall(prereg)
    dup_text = sorted({t for t in tags if tags.count(t) > 1})
    rows = re.findall(r'^\| (C-[A-Za-z0-9.]+) \|', texts['CLAUSE_SOURCE_MAP_R2.md'], re.M)
    dup_map = sorted({r for r in rows if rows.count(r) > 1})
    no_row = sorted(set(tags) - set(rows))
    no_tag = sorted(set(rows) - set(tags))
    res['checks']['T6_CLAUSE_TAGS_MAPPED'] = {'pass': not (dup_text or dup_map or no_row or no_tag), 'n_tags': len(set(tags)),
                                              'duplicate_in_text': dup_text, 'duplicate_in_map': dup_map,
                                              'tag_without_map_row': no_row, 'map_row_without_tag': no_tag}
    res['verdict'] = 'PASS' if all(c['pass'] for c in res['checks'].values()) else 'FAIL'
    return res


def main():
    p = argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument('--dir', required=True)
    p.add_argument('--provenance', required=True)
    p.add_argument('--slots', required=True)
    p.add_argument('--expect-slots-sha', required=True)
    p.add_argument('--out')
    a = p.parse_args()
    if a.out:
        _OUT.append(os.path.abspath(a.out))
    sys.addaudithook(_hook)
    res = run(a)
    text = json.dumps(res, indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    if a.out:
        with open(a.out, 'x') as f:
            f.write(text)
    sys.stdout.write(text)
    return 0 if res['verdict'] == 'PASS' else 2


if __name__ == '__main__':
    raise SystemExit(main())
