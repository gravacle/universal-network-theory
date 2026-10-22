# Claude4 (dispatch 0585) target-free check v002 for the miss-reading prereg r2 (round 2). Read-only apart from --out (exclusive create).
# It never opens target data, so it cannot compare the text with target values. It shows the text is target-free by construction,
# checked mechanically (not proved):
#  T1 no forbidden target term, data-source name or data-file extension in any r2 text file (after NFKC + Cf stripping);
#  T2 no number carrying a velocity unit (many spellings); T3 no target symbol set equal to a number;
#  T4 every numeric token in every r2 text file is listed in the provenance file (value level), each listed category is known, each
#     QUERY_RADIUS and NODE_RADIUS value is verified against target-free bytes; an occurrence census with context is written for review;
#  T5 every pinned source exists, has a target-free path, and hashes as stated; open-V005 entries are pinned per section (end-markers allowed);
#  T6 every clause tag in the prereg has exactly one map row and vice versa;
#  T7 (currency, not target-freeness) every '## A<n>:' heading in the current V005 is either cited or in the read-with-no-change list.
# Limits (stated): categories are self-declared and verified by review; T5 judges a source target-free by its path, not its content.
# An audit hook refuses any open whose path contains a forbidden term, any write other than --out, and process/network/delete events.
# usage: python3 -I -B check_target_free_c4v002.py --dir R2DIR --provenance NUMBER_PROVENANCE_R2.json --slots SLOTS.json
#        --expect-slots-sha H --nodes NODES.json --expect-nodes-sha H [--out RESULT.json] [--no-hook]
import argparse, hashlib, json, os, re, sys, unicodedata

FORBIDDEN = ('rotmod', 'vobs', 'v_obs', 'vrot_obs', 'massmodels', 'sparc', 'lelli', 'begeman', 'vgas', 'vdisk', 'vbul',
             'e_vobs', 'errv', 'rotcur', 'rotation_curve_data')
FORBIDDEN_EXT = re.compile(r'\.(dat|mrt|csv|tsv|fits|fit|fts|tbl|ecsv|vot|votable|ipac|rdb)\b', re.I)
TEXT_FILES = ('PREREG_MISS_READING_R2.md', 'CLAUSE_SOURCE_MAP_R2.md', 'ROOT_ITEMS_R2.md')
_OUT = []
_PROTECT = ('kmax_a2f10_c5h_run_v001', '/uvt_', 'runs_ext/uvt')


def _hook(event, args):
    if event == 'open':
        path = args[0]
        if isinstance(path, int):
            return
        p = os.fsdecode(path) if isinstance(path, bytes) else str(path)
        low = p.lower()
        if any(w in low for w in FORBIDDEN) or any(w in low for w in _PROTECT):
            raise PermissionError('protected or target-like path refused: %s' % p)
        mode = args[1] if len(args) > 1 and isinstance(args[1], str) else 'r'
        flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
        writing = any(c in mode for c in 'wax+') or (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND))
        if writing and os.path.abspath(p) not in _OUT:
            raise PermissionError('write refused: %s' % p)
    elif event in ('os.remove', 'os.rename', 'os.rmdir', 'shutil.rmtree', 'subprocess.Popen', 'os.system', 'os.posix_spawn',
                   'socket.connect', 'socket.getaddrinfo'):
        raise PermissionError('refused: %s' % event)


def norm(t):
    t = unicodedata.normalize('NFKC', t)
    return ''.join(ch for ch in t if unicodedata.category(ch) != 'Cf')


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


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha(path):
    with open(path, 'rb') as f:
        return sha_bytes(f.read())


VEL = re.compile(r'\d(?:[\d.,]*\d)?\s*(?:km\s*/\s*s(?:ec)?\b|km\s*[·⋅.]?\s*s\s*(?:\^\s*-\s*1|-1|−1)|kms\s*-?1\b|kms\b|km\s+per\s+s(?:ec(?:ond)?)?\b|'
                 r'kilomet(?:re|er)s?\s+per\s+second)', re.I)
SYM = re.compile(r'(?:\bv_q\b|σ_q|\bsigma_q\b|\bv_obs\b|\bvobs\b|\bv_rot\b|\bvrot\b|\bv_flat\b|observed[_ ](?:speed|velocity)\w*)\s*(?:=|≈|:|~)\s*[-+−]?\d', re.I)
TAG = re.compile(r'\[(C-[A-Za-z0-9.]+)\]')
HEX64 = re.compile(r'\b[0-9a-f]{64}\b')
HEXL = re.compile(r'\b(?=[0-9a-f]*[a-f])[0-9a-f]{6,}\b')
ELIDED = re.compile(r'[0-9a-f]{6,}…')
ISO = re.compile(r'\b\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2})?Z?)?\b|\b\d{2}:\d{2}(?::\d{2})?Z\b|\b\d{4}Z\b')
SECTION = re.compile(r'§\s*\d+(?:\.\d+)*')
IDENT_CHAIN = re.compile(r'(?<![\w.])[A-Za-z][\w′]*(?:[-./][\w′]+)+')
IDENT_DIGIT = re.compile(r'\b[A-Za-z]+[\w′]*\d[\w′]*\b')
NUM = re.compile(r'(?<![\w.])\d+(?:\.\d+)?')


def strip_for_numbers(text):
    t = norm(text)
    t = HEX64.sub(' ', t)
    t = ELIDED.sub(' ', t)
    t = HEXL.sub(' ', t)
    t = ISO.sub(' ', t)
    t = SECTION.sub(' ', t)
    t = t.replace('`', ' ')
    t = re.sub(r'\[C-[^\]]+\]', ' ', t)
    t = IDENT_CHAIN.sub(' ', t)
    t = IDENT_DIGIT.sub(' ', t)
    return t


def numeric_tokens(text):
    return NUM.findall(strip_for_numbers(text))


def census(name, text):
    t = strip_for_numbers(text)
    out = {}
    for m in NUM.finditer(t):
        tok = m.group(0)
        ctx = t[max(0, m.start() - 40):m.end() + 40].replace('\n', ' ')
        out.setdefault(tok, []).append('%s: …%s…' % (name, ' '.join(ctx.split())))
    return out


def section(text, title_prefix):
    m = re.search(r'^## ' + re.escape(title_prefix) + r'.*$', text, re.M)
    if not m:
        return ''
    rest = text[m.end():]
    n = re.search(r'^## ', rest, re.M)
    return rest[:n.start()] if n else rest


def entry_sections(text, end_markers=None):
    """{n: [section text]} for every '## A<n>:' heading: from the heading line up to the next '## ' line (or EOF),
    or, when end_markers[n] is given, up to the first later line that starts with that marker."""
    end_markers = end_markers or {}
    lines = text.split('\n')
    starts = [i for i, l in enumerate(lines) if l.startswith('## ')]
    out = {}
    for j, i in enumerate(starts):
        m = re.match(r'^## A(\d{1,3}):', lines[i])
        if not m:
            continue
        n = int(m.group(1))
        end = starts[j + 1] if j + 1 < len(starts) else len(lines)
        marker = end_markers.get(n)
        if marker:
            for k in range(i + 1, end):
                if lines[k].startswith(marker):
                    end = k
                    break
            else:
                out.setdefault(n, []).append(None)
                continue
        body = '\n'.join(lines[i:end])
        if end < len(lines):
            body += '\n'
        out.setdefault(n, []).append(body)
    return out


def all_headings(text):
    return [int(x) for x in re.findall(r'^## A(\d{1,3})\b', text, re.M)]


def v005_entry_pins(text):
    s = section(text, '11.')
    rows = []
    for line in s.splitlines():
        m = re.match(r'^\| A(\d{1,3}) \|(.*)\| `([0-9a-f]{64})` \|$', line)
        if m:
            cells = [c.strip() for c in m.group(2).split('|')]
            marker = cells[-1] if len(cells) >= 2 else ''
            marker = '' if marker in ('', '—', 'next heading') else marker.strip('`')
            rows.append((int(m.group(1)), marker, m.group(3)))
    return rows


def no_change_list(text):
    s = section(text, '11.')
    m = re.search(r'\*\*Read with no change to this text:\*\*\s*(.*?)\.\s', s)
    if not m:
        return None
    out = set()
    for part in m.group(1).split(','):
        part = part.strip()
        r = re.fullmatch(r'A(\d{1,3})(?:[–-]A(\d{1,3}))?', part)
        if r:
            a = int(r.group(1))
            b = int(r.group(2)) if r.group(2) else a
            out.update(range(a, b + 1))
    return out


ROOTS = {
    '…/FIRST_CONSTRUCTION_REVIEW_2026-10-13/': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/',
    '…/CLAUDE2/': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/',
    'claude_artifacts/': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/',
}
DISPATCH_DIR = '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
DECISIONS = {'V003': 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V003_ADDENDUM.md',
             'V004': 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md',
             'V005': 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'}


def expand(p):
    for k, v in ROOTS.items():
        if p.startswith(k):
            return v + p[len(k):]
    return p


def sources_from_section11(text):
    s = section(text, '11.')
    out = []
    for line in s.splitlines():
        if re.match(r'^\| A\d{1,3} \|', line):
            continue
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
                p = ART + p
            out.append((first, expand(p), h))
    return out


def run(a):
    res = {'schema': 'UNT_MISS_READING_R2_TARGET_FREE_CHECK_C4V002', 'checks': {}, 'files': {}, 'limits': [
        'T4 checks token values, not each occurrence; the census lists every occurrence with context for review',
        'provenance categories are self-declared; reviewers verify them against the cited sources',
        'T5 judges a pinned source target-free by its path; content target-freeness rests on the source registration',
        'the check never opens target data, so it cannot compare the text with target values']}
    raw, texts = {}, {}
    for name in TEXT_FILES:
        p = os.path.join(a.dir, name)
        raw[name] = open(p, 'rb').read().decode('utf-8')
        texts[name] = norm(raw[name])
        res['files'][name] = sha(p)
    prereg = raw['PREREG_MISS_READING_R2.md']

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
    slots_sha, nodes_sha = sha(a.slots), sha(a.nodes)
    slots = strict_load(a.slots)
    nodes = strict_load(a.nodes)
    rad = {r['query_id']: r['Rad_text'] for r in slots['query_block']['rows']}
    units = {r['Rad_unit'] for r in slots['query_block']['rows']}
    node_kpc = nodes['orders']['4']['radii_kpc']
    allcensus = {}
    for name, t in raw.items():
        for tok, ctxs in census(name, t).items():
            allcensus.setdefault(tok, []).extend(ctxs)
    toks = sorted(allcensus, key=lambda x: (float(x), x))
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
        if v.get('category') == 'NODE_RADIUS':
            idx = v.get('node_index')
            dp = len(k.split('.')[1]) if '.' in k else 0
            if not isinstance(idx, int) or not (0 <= idx < len(node_kpc)) or ('%.*f' % (dp, node_kpc[idx])) != k:
                radius_bad.append('%s: node %r does not round to it' % (k, idx))
    t4 = (not missing and not bad_cat and not radius_bad and slots_sha == a.expect_slots_sha and nodes_sha == a.expect_nodes_sha
          and units == {'kpc'})
    res['checks']['T4_NUMBER_PROVENANCE'] = {'pass': t4, 'numeric_tokens': toks, 'missing_from_provenance': missing,
                                             'listed_but_absent': unused, 'bad_category': bad_cat, 'radius_mismatch': radius_bad,
                                             'slots_sha256': slots_sha, 'nodes_sha256': nodes_sha, 'rad_units': sorted(units)}
    res['census'] = {k: allcensus[k] for k in toks}

    srcs = sources_from_section11(prereg)
    bad, notes, entry_results = [], [], []
    pins = v005_entry_pins(prereg)
    v005_text = None
    for label, p, h in srcs:
        if p.startswith(('AMBIGUOUS', 'UNPARSED')) or label == 'UNPARSED':
            bad.append('%s: %s' % (label, p))
            continue
        if any(w in p.lower() for w in FORBIDDEN) or FORBIDDEN_EXT.search(p) or any(w in p.lower() for w in _PROTECT):
            bad.append('%s: target-like or protected path %s' % (label, p))
            continue
        if not os.path.isfile(p):
            bad.append('%s: missing %s' % (label, p))
            continue
        b = open(p, 'rb').read()
        got = sha_bytes(b)
        if label == 'decisions V005':
            v005_text = b.decode('utf-8')
            if got != h:
                notes.append('V005 whole-file sha is now %s (stated %s at assembly): open file; entries checked below' % (got, h))
            markers = {n: mk for n, mk, _ in pins if mk}
            secs = entry_sections(v005_text, markers)
            if not pins:
                bad.append('no V005 per-entry pins found in section 11')
            for n, mk, eh in pins:
                found = secs.get(n, [])
                if len(found) != 1 or found[0] is None:
                    bad.append('V005 A%d: %d sections, or end-marker %r not found' % (n, len(found), mk))
                    continue
                cur = sha_bytes(found[0].encode('utf-8'))
                entry_results.append({'entry': 'A%d' % n, 'ends_before': mk, 'stated': eh, 'current': cur, 'match': cur == eh})
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
    rows = re.findall(r'^\| (C-[A-Za-z0-9.]+) \|', raw['CLAUSE_SOURCE_MAP_R2.md'], re.M)
    dup_map = sorted({r for r in rows if rows.count(r) > 1})
    no_row = sorted(set(tags) - set(rows))
    no_tag = sorted(set(rows) - set(tags))
    res['checks']['T6_CLAUSE_TAGS_MAPPED'] = {'pass': not (dup_text or dup_map or no_row or no_tag), 'n_tags': len(set(tags)),
                                              'duplicate_in_text': dup_text, 'duplicate_in_map': dup_map,
                                              'tag_without_map_row': no_row, 'map_row_without_tag': no_tag}

    cited = {n for n, _, _ in pins}
    nochange = no_change_list(prereg)
    if v005_text is None or nochange is None:
        res['checks']['T7_V005_CURRENCY'] = {'pass': False, 'problem': 'V005 or the no-change list was not found'}
    else:
        heads = sorted(set(n for n in all_headings(v005_text) if n >= 47))
        later = [n for n in heads if n not in cited and n not in nochange]
        res['checks']['T7_V005_CURRENCY'] = {'pass': not later, 'later_entries_needing_a_revision_or_no_change_note': ['A%d' % n for n in later],
                                             'note': 'currency only: a FAIL here means root added an entry after assembly (M-6 item 4)'}
    tf = [k for k in res['checks'] if k != 'T7_V005_CURRENCY']
    res['verdict_target_free'] = 'PASS' if all(res['checks'][k]['pass'] for k in tf) else 'FAIL'
    res['verdict_currency'] = 'PASS' if res['checks']['T7_V005_CURRENCY']['pass'] else 'FAIL'
    res['verdict'] = res['verdict_target_free']
    return res


def main():
    p = argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument('--dir', required=True)
    p.add_argument('--provenance', required=True)
    p.add_argument('--slots', required=True)
    p.add_argument('--expect-slots-sha', required=True)
    p.add_argument('--nodes', required=True)
    p.add_argument('--expect-nodes-sha', required=True)
    p.add_argument('--out')
    p.add_argument('--no-hook', action='store_true')
    a = p.parse_args()
    if a.out:
        _OUT.append(os.path.abspath(a.out))
    if not a.no_hook:
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
