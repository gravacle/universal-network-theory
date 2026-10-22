# Claude4 (dispatches 0585, 0606 and 0619/A98.2; 0687/A133 for r3a) generator v005 for the miss-reading prereg r3a: v004 with the R3A file names (tools-builder revision).
# It reads the draft folder and the hand-written V005 entry table (V005_ENTRY_TABLE_R3A.json, schema
# UNT_MISS_READING_V005_ENTRY_TABLE_C4V001), verifies the table against the V005 bytes (the whole-file sha it was read at, every
# '## ' heading exactly once in file order with its exact text, each CITED_PINNED section sha and its allow-listed end-marker),
# takes the cited V005 set from the texts' own citations and fails on any cited entry that is not CITED_PINNED, renders the
# entry table into the prereg's sources section, and fills the dispatch pins. It never computes a "no change" list.
# Every file is written into --out (a new folder) with exclusive create. INDEX_R3A.md is written before the checks so that the
# check scans it. The target-free check and the mutation test then run as separate processes, each with its own audit hook,
# and HASHES_R3A.txt is written last. An audit hook in this process refuses target-like opens, writes outside --out, and any
# process other than those two. It opens no target data, launches nothing else and overwrites nothing.
# Placeholders in the draft prereg: @@V005_ENTRY_TABLE@@ (required, once), @@V005_SHA@@ (required, once), @@V005_READ_UTC@@,
# @@V005_ENTRY_ROWS@@ (optional legacy rows under the r2 header '| entry | used for | ends before | section sha256 |') and
# @@SHA_nnnn@@ (the sha256 of dispatch FROM_CODEX/nnnn_*). @@V005_UNCITED@@ is refused.
# Fix stage (refute RF-B1/TF-B1): the hand-written V006_ENTRY_TABLE_R3A.json (schema UNT_MISS_READING_V006_ENTRY_TABLE_C4V001) is
# verified against the V006 bytes the same way (every '## ' heading once, in file order, verbatim; v006_sha256_read and
# v006_trimmed_sha256 from the bytes; CITED_PINNED section shas taken with trailing newlines removed) and rendered at
# @@V006_ENTRY_TABLE@@ (required, once), with @@V006_SHA@@ (required, once) and @@V006_READ_UTC@@. A V006 addendum must exist.
# usage: python3 -I -B make_miss_reading_c4v005.py --draft DRAFT_DIR --out NEW_DIR --label LABEL --mutation-work NEW_SCRATCH_DIR
#        [--entry-table V005_ENTRY_TABLE_R3A.json] [--v005 V005_BYTE_COPY.md] [--entry-table6 V006_ENTRY_TABLE_R3A.json]
#        [--v006 V006_BYTE_COPY.md]
import argparse, hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_target_free_c4v004 as T

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
SLOTS_SHA = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
NODES = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json'
NODES_SHA = 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'
FILES = (T.PREREG, T.CSM, T.ROOT, T.PROV)
TOOLS = T.TOOL_FILES
DEFAULT_TAIL_REASON = ('the root log after the end-marker; this text cites its content only through the dispatch pins of the '
                       'sources section, and the tail is pinned so that an edit there is seen')
ETAB_REQUIRED = ('entry', 'heading', 'disposition', 'reason')


class BuildError(Exception):
    pass


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def read(p):
    with open(p, 'rb') as f:
        return f.read()


norm_marker = T.norm_marker


def validate_entry_table(et, v_bytes):
    """Check the hand-written table against the V005 bytes; return the rows to render, in file order."""
    if not isinstance(et, dict) or et.get('schema') != T.ETAB_SCHEMA:
        raise BuildError('entry table: schema must be %s' % T.ETAB_SCHEMA)
    extra = set(et) - {'schema', 'v005_sha256_read', 'read_utc', 'entries', 'note'}
    if extra:
        raise BuildError('entry table: unknown top-level fields %s' % sorted(extra))
    got = sha_bytes(v_bytes)
    if et.get('v005_sha256_read') != got:
        raise BuildError('entry table was read at V005 %s, but the V005 bytes now hash %s: re-read the new or changed entries, '
                         'update the table and its v005_sha256_read' % (et.get('v005_sha256_read'), got))
    if not isinstance(et.get('read_utc'), str) or not re.fullmatch(r'20\d\d-\d\d-\d\dT\d\d:\d\d(?::\d\d)?Z', et['read_utc']):
        raise BuildError('entry table: read_utc must be an ISO UTC time from date -u')
    v_text = v_bytes.decode('utf-8')
    heads = T.v005_headings(v_text)
    ents = et.get('entries')
    if not isinstance(ents, list) or not all(isinstance(e, dict) for e in ents):
        raise BuildError('entry table: entries must be a list of objects')
    problems = []
    if len(ents) != len(heads):
        problems.append('the table has %d entries; V005 has %d "## " headings' % (len(ents), len(heads)))
    seen = {}
    for e in ents:
        if isinstance(e, dict) and isinstance(e.get('entry'), str):
            seen[e['entry']] = seen.get(e['entry'], 0) + 1
    problems += ['entry %r occurs %d times' % (k, v) for k, v in seen.items() if v != 1]
    table_ids = [e.get('entry') for e in ents if isinstance(e, dict)]
    problems += ['V005 heading not in the table: %r' % l for _, l, i in heads if i not in table_ids]
    file_ids = [i for _, _, i in heads]
    problems += ['table entry %r matches no V005 heading' % i for i in table_ids if i not in file_ids]
    if not problems and table_ids != file_ids:
        problems.append('the table is not in V005 file order')
    if problems:
        raise BuildError('entry table does not cover V005 exactly once in file order: ' + '; '.join(problems))
    out = []
    for e, (idx, line, ent) in zip(ents, heads):
        miss = [k for k in ETAB_REQUIRED if k not in e]
        if miss or set(e) - T.ETAB_FIELDS:
            raise BuildError('entry %r: missing %s or unknown fields %s' % (ent, miss, sorted(set(e) - T.ETAB_FIELDS)))
        if not all(isinstance(e[k], str) for k in ETAB_REQUIRED):
            raise BuildError('entry %r: entry, heading, disposition and reason must be strings' % ent)
        h = e['heading'][3:] if e['heading'].startswith('## ') else e['heading']
        if h != line[3:]:
            raise BuildError('entry %r: heading is not the V005 heading line verbatim' % ent)
        if e['disposition'] not in T.DISPOSITIONS:
            raise BuildError('entry %r: disposition must be one of %s' % (ent, T.DISPOSITIONS))
        for k in ('reason', 'tail_reason'):
            v = e.get(k)
            if v is not None and (not isinstance(v, str) or not v.strip() or '\n' in v or '@@' in v or v != v.strip()):
                raise BuildError('entry %r: %s must be one non-empty line without leading or trailing blanks' % (ent, k))
        marker = norm_marker(e.get('end_marker'))
        if marker is None:
            raise BuildError('entry %r: end_marker must be a string ("next heading", empty, or the marker text)' % ent)
        row = {'entry': ent, 'heading': h, 'disposition': e['disposition'], 'reason': e['reason'], 'marker': marker}
        if e['disposition'] == 'CITED_PINNED':
            if marker and T.END_MARKER_ALLOW.get(ent) != marker:
                raise BuildError('entry %r: end_marker %r is not allow-listed (%s)' % (ent, marker, T.END_MARKER_ALLOW))
            main, tail, prob = T.entry_parts(v_text, idx, marker)
            if prob:
                raise BuildError('entry %r: %s' % (ent, prob))
            cur = sha_bytes(main.encode('utf-8'))
            if e.get('section_sha256') != cur:
                raise BuildError('entry %r: section_sha256 %s differs from the V005 bytes %s' % (ent, e.get('section_sha256'), cur))
            row['sha'] = cur
            if marker:
                tsha = sha_bytes(tail.encode('utf-8'))
                if e.get('tail_sha256') not in (None, tsha):
                    raise BuildError('entry %r: tail_sha256 differs from the V005 bytes %s' % (ent, tsha))
                row['tail_sha'] = tsha
                row['tail_reason'] = e.get('tail_reason') or DEFAULT_TAIL_REASON
            elif e.get('tail_sha256') or e.get('tail_reason'):
                raise BuildError('entry %r: tail fields without an end_marker' % ent)
        else:
            if marker or any(e.get(k) for k in ('section_sha256', 'tail_sha256', 'tail_reason')):
                raise BuildError('NO_CHANGE entry %r carries pin fields (section_sha256/end_marker/tail are CITED_PINNED only)' % ent)
            main, _, _ = T.entry_parts(v_text, idx, '')
            row['sha'] = sha_bytes(main.encode('utf-8'))        # the bytes read, recorded so that a later edit is seen (T7)
        out.append(row)
    return out


def validate_entry_table6(et, v_bytes):
    """Check the hand-written V006 table against the V006 bytes; return the rows to render, in file order (fix stage)."""
    if not isinstance(et, dict) or et.get('schema') != T.ETAB6_SCHEMA:
        raise BuildError('V006 entry table: schema must be %s' % T.ETAB6_SCHEMA)
    extra = set(et) - T.ETAB6_TOP
    if extra:
        raise BuildError('V006 entry table: unknown top-level fields %s' % sorted(extra))
    got = sha_bytes(v_bytes)
    if et.get('v006_sha256_read') != got:
        raise BuildError('V006 entry table was read at V006 %s, but the V006 bytes now hash %s: re-read the new or changed '
                         'entries, update the table and its v006_sha256_read' % (et.get('v006_sha256_read'), got))
    if et.get('v006_trimmed_sha256') != T.trimmed_sha(v_bytes):
        raise BuildError('V006 entry table: v006_trimmed_sha256 must be the sha256 of the read bytes with trailing newlines removed')
    if not isinstance(et.get('read_utc'), str) or not re.fullmatch(r'20\d\d-\d\d-\d\dT\d\d:\d\d(?::\d\d)?Z', et['read_utc']):
        raise BuildError('V006 entry table: read_utc must be an ISO UTC time from date -u')
    secs = T.v006_sections(v_bytes.decode('utf-8'))
    ents = et.get('entries')
    if not isinstance(ents, list) or not all(isinstance(e, dict) for e in ents):
        raise BuildError('V006 entry table: entries must be a list of objects')
    file_ids = [s[1] for s in secs]
    table_ids = [e.get('entry') for e in ents]
    problems = []
    if len(ents) != len(secs):
        problems.append('the table has %d entries; V006 has %d "## " headings' % (len(ents), len(secs)))
    problems += ['entry %r occurs %d times' % (k, table_ids.count(k)) for k in sorted(set(map(str, table_ids))) if table_ids.count(k) != 1]
    problems += ['V006 heading not in the table: %r' % s[0] for s in secs if s[1] not in table_ids]
    problems += ['table entry %r matches no V006 heading' % i for i in table_ids if i not in file_ids]
    if not problems and table_ids != file_ids:
        problems.append('the table is not in V006 file order')
    if problems:
        raise BuildError('V006 entry table does not cover V006 exactly once in file order: ' + '; '.join(problems))
    out = []
    for e, (line, ent, section, _) in zip(ents, secs):
        miss = [k for k in ETAB_REQUIRED if k not in e]
        if miss or set(e) - T.ETAB6_FIELDS:
            raise BuildError('V006 entry %r: missing %s or unknown fields %s' % (ent, miss, sorted(set(e) - T.ETAB6_FIELDS)))
        if not all(isinstance(e[k], str) for k in ETAB_REQUIRED):
            raise BuildError('V006 entry %r: entry, heading, disposition and reason must be strings' % ent)
        h = e['heading'][3:] if e['heading'].startswith('## ') else e['heading']
        if h != line[3:]:
            raise BuildError('V006 entry %r: heading is not the V006 heading line verbatim' % ent)
        if e['disposition'] not in T.DISPOSITIONS:
            raise BuildError('V006 entry %r: disposition must be one of %s' % (ent, T.DISPOSITIONS))
        v = e['reason']
        if not v.strip() or '\n' in v or '@@' in v or v != v.strip():
            raise BuildError('V006 entry %r: reason must be one non-empty line without leading or trailing blanks' % ent)
        if norm_marker(e.get('end_marker')) not in ('',):
            raise BuildError('V006 entry %r: a V006 pin runs to the next heading; no end_marker is allowed' % ent)
        cur = T.trimmed_sha(section)
        if e['disposition'] == 'CITED_PINNED':
            if e.get('section_sha256') != cur:
                raise BuildError('V006 entry %r: section_sha256 %s differs from the V006 bytes %s (trailing newlines removed)'
                                 % (ent, e.get('section_sha256'), cur))
        elif e.get('section_sha256'):
            raise BuildError('NO_CHANGE V006 entry %r carries a section_sha256 (CITED_PINNED only)' % ent)
        out.append({'entry': ent, 'heading': h, 'disposition': e['disposition'], 'reason': v, 'marker': '', 'sha': cur})
    return out


def render_entry_table6(rows6):
    lines = [T.ETAB6_HEADER, T.ETAB_SEP]
    for r in rows6:
        lines.append('| %s | %s | %s | %s | %s | `%s` |' % (r['entry'], T.esc_cell(r['heading']), r['disposition'],
                                                             T.esc_cell(r['reason']), T.NEXT_HEADING, r['sha']))
    return '\n'.join(lines)


def render_entry_table(rows):
    lines = [T.ETAB_HEADER, T.ETAB_SEP]
    for r in rows:
        mk = ('`%s`' % r['marker']) if r['marker'] else T.NEXT_HEADING
        lines.append('| %s | %s | %s | %s | %s | `%s` |' % (r['entry'], T.esc_cell(r['heading']), r['disposition'],
                                                             T.esc_cell(r['reason']), mk, r['sha']))
        if r.get('tail_sha'):
            lines.append('| %s%s | from `%s` to the next heading or end of file | TAIL_PINNED | %s | %s | `%s` |' % (
                r['entry'], T.TAIL_SUFFIX, r['marker'], T.esc_cell(r['tail_reason']), T.NEXT_HEADING, r['tail_sha']))
    return '\n'.join(lines)


def render_legacy_rows(rows):
    lines = []
    for r in rows:
        if r['disposition'] != 'CITED_PINNED':
            continue
        mk = ('`%s`' % r['marker']) if r['marker'] else T.NEXT_HEADING
        lines.append('| %s | %s | %s | `%s` |' % (r['entry'], T.esc_cell(r['reason']), mk, r['sha']))
        if r.get('tail_sha'):
            lines.append('| %s%s | %s | from `%s` to the next heading or end of file | `%s` |' % (
                r['entry'], T.TAIL_SUFFIX, T.esc_cell(r['tail_reason']), r['marker'], r['tail_sha']))
    return '\n'.join(lines)


def check_cited(texts, rows, v_text, rows6=(), v6_text=None):
    """The cited V005 and V006 sets are taken from the three texts' own citations; every cited entry must be CITED_PINNED."""
    v_ids = {i for _, _, i in T.v005_headings(v_text)}
    cited = T.cited_v005({n: texts[n] for n in T.TEXT_FILES}, v_ids, {})
    pinned = {r['entry'] for r in rows if r['disposition'] == 'CITED_PINNED'}
    unpinned = sorted(set(cited) - pinned)
    if unpinned:
        raise BuildError('cited V005 entries that the table does not pin (make them CITED_PINNED with a section sha, or drop the '
                         'citation): ' + '; '.join('%s (%s)' % (e, cited[e][0]) for e in unpinned))
    if v6_text is not None:
        v6_ids = {s[1] for s in T.v006_sections(v6_text)}
        cited6 = T.cited_v005({n: texts[n] for n in T.TEXT_FILES}, v6_ids, {})
        pinned6 = {r['entry'] for r in rows6 if r['disposition'] == 'CITED_PINNED'}
        unpinned6 = sorted(set(cited6) - pinned6)
        if unpinned6:
            raise BuildError('cited V006 entries that the V006 table does not pin: ' + '; '.join(
                '%s (%s)' % (e, cited6[e][0]) for e in unpinned6))
    return cited


def hook_self_probe(hook, out, chk):
    """Direct calls of this process's hook (no side effects): a foreign process, a write and a mkdir outside --out must be
    refused, and the check's own command allowed."""
    outside = os.path.join(os.path.dirname(out), os.path.basename(out) + '_GENERATOR_PROBE_NEVER_CREATED')
    probes = [('subprocess /bin/sh', ('subprocess.Popen', ('/bin/sh', ['/bin/sh', '-c', 'true'], None, None)), 'REFUSED'),
              ('subprocess python without the tool', ('subprocess.Popen', (PY, [PY, '-I', '-B', '-c', 'pass'], None, None)), 'REFUSED'),
              ('write outside --out', ('open', (outside + '.txt', 'w', os.O_WRONLY | os.O_CREAT)), 'REFUSED'),
              ('mkdir outside --out', ('os.mkdir', (outside, 0o777, -1)), 'REFUSED'),
              ('os.remove', ('os.remove', (outside, -1)), 'REFUSED'),
              ('the check command', ('subprocess.Popen', (PY, [PY, '-I', '-B', chk, '--dir', out], None, None)), 'ALLOWED')]
    res = []
    for name, (ev, args), want in probes:
        try:
            hook(ev, args)
            got = 'ALLOWED'
        except PermissionError:
            got = 'REFUSED'
        res.append((name, want, got))
    return res


def dispatch_sha(num):
    names = [x for x in os.listdir(T.DISPATCH_DIR) if x.startswith(num + '_')]
    if len(names) != 1:
        raise BuildError('dispatch %s: %d files in FROM_CODEX' % (num, len(names)))
    return sha_bytes(read(os.path.join(T.DISPATCH_DIR, names[0])))


def fill(prereg, rows, v_sha, read_utc, rows6, v6_sha, read6_utc):
    if '@@V005_UNCITED@@' in prereg:
        raise BuildError('@@V005_UNCITED@@ is refused: the computed no-change list is replaced by the entry table (A99.3)')
    for ph in ('@@V005_ENTRY_TABLE@@', '@@V005_SHA@@', '@@V006_ENTRY_TABLE@@', '@@V006_SHA@@'):
        if prereg.count(ph) != 1:
            raise BuildError('%s must occur exactly once in the draft prereg (found %d)' % (ph, prereg.count(ph)))
    for ph in ('@@V005_ENTRY_ROWS@@', '@@V005_READ_UTC@@', '@@V006_READ_UTC@@'):
        if prereg.count(ph) > 1:
            raise BuildError('%s occurs more than once' % ph)
    if '@@V005_ENTRY_ROWS@@' in prereg and T.LEGACY_HEADER not in prereg:
        raise BuildError('@@V005_ENTRY_ROWS@@ needs the legacy header %r above it' % T.LEGACY_HEADER)
    t = prereg.replace('@@V005_ENTRY_TABLE@@', render_entry_table(rows))
    t = t.replace('@@V005_ENTRY_ROWS@@', render_legacy_rows(rows))
    t = t.replace('@@V005_SHA@@', v_sha).replace('@@V005_READ_UTC@@', read_utc)
    t = t.replace('@@V006_ENTRY_TABLE@@', render_entry_table6(rows6))
    t = t.replace('@@V006_SHA@@', v6_sha).replace('@@V006_READ_UTC@@', read6_utc)
    for num in sorted(set(re.findall(r'@@SHA_(0\d{3})@@', t))):
        t = t.replace('@@SHA_%s@@' % num, dispatch_sha(num))
    left = sorted(set(re.findall(r'@@[A-Z0-9_]*@@', t)))
    if left or '@@' in t:
        raise BuildError('unfilled placeholders remain: %s (supported: @@V005_ENTRY_TABLE@@, @@V005_SHA@@, @@V005_READ_UTC@@, '
                         '@@V005_ENTRY_ROWS@@, @@V006_ENTRY_TABLE@@, @@V006_SHA@@, @@V006_READ_UTC@@, @@SHA_nnnn@@)' % (left or ['@@']))
    return t


def main():
    p = argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument('--draft', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--label', required=True)
    p.add_argument('--mutation-work', required=True)
    p.add_argument('--entry-table', default=None, help='default: DRAFT/V005_ENTRY_TABLE_R3A.json')
    p.add_argument('--v005', default=None, help='a byte copy of V005 to build against (default: the live addendum)')
    p.add_argument('--entry-table6', default=None, help='default: DRAFT/V006_ENTRY_TABLE_R3A.json')
    p.add_argument('--v006', default=None, help='a byte copy of V006 to build against (default: the live addendum)')
    a = p.parse_args()
    out = os.path.abspath(a.out)
    work = os.path.abspath(a.mutation_work)
    draft = os.path.abspath(a.draft)
    etab_path = os.path.abspath(a.entry_table or os.path.join(draft, T.ETAB))
    etab6_path = os.path.abspath(a.entry_table6 or os.path.join(draft, T.ETAB6))
    if os.path.exists(out) or os.path.exists(work):
        raise BuildError('--out and --mutation-work must not exist')
    chk = os.path.join(out, 'tools', 'check_target_free_c4v004.py')
    tst = os.path.join(out, 'tools', 'test_check_target_free_c4v004.py')

    def exec_ok(args):
        argv = list(args[1]) if args[1] is not None else []
        return len(argv) >= 4 and argv[:3] == [PY, '-I', '-B'] and argv[3] in (chk, tst) and (args[0] in (None, PY))
    gen_hook = T.make_hook(write_dirs=[out], mkdir_dirs=[out], exec_ok=exec_ok)
    sys.addaudithook(gen_hook)
    probes = hook_self_probe(gen_hook, out, chk)
    if any(w != g for _, w, g in probes):
        raise BuildError('generator hook self-probe failed: %s' % probes)

    v_path = os.path.abspath(a.v005) if a.v005 else T.V005_PATH
    if T.path_denied(v_path):
        raise BuildError('refused V005 path %s' % v_path)
    v_bytes = read(v_path)
    v_sha = sha_bytes(v_bytes)
    if not os.path.isfile(etab_path):
        raise BuildError('the hand-written entry table %s does not exist' % etab_path)
    try:
        et = T.strict_load(etab_path)
    except ValueError as e:
        raise BuildError('entry table %s: %s' % (etab_path, e))
    rows = validate_entry_table(et, v_bytes)
    v_text = v_bytes.decode('utf-8')
    v6_path = os.path.abspath(a.v006) if a.v006 else T.V006_PATH
    if T.path_denied(v6_path):
        raise BuildError('refused V006 path %s' % v6_path)
    if not os.path.isfile(v6_path):
        raise BuildError('no V006 addendum at %s: this text expects one (A106.3 puts every later root ruling there)' % v6_path)
    v6_bytes = read(v6_path)
    v6_sha = sha_bytes(v6_bytes)
    if not os.path.isfile(etab6_path):
        raise BuildError('the hand-written V006 entry table %s does not exist' % etab6_path)
    try:
        et6 = T.strict_load(etab6_path)
    except ValueError as e:
        raise BuildError('V006 entry table %s: %s' % (etab6_path, e))
    rows6 = validate_entry_table6(et6, v6_bytes)
    v6_text = v6_bytes.decode('utf-8')

    texts = {}
    for name in FILES:
        texts[name] = read(os.path.join(draft, name)).decode('utf-8')
    check_cited(texts, rows, v_text, rows6, v6_text)
    texts[T.PREREG] = fill(texts[T.PREREG], rows, v_sha, et['read_utc'], rows6, v6_sha, et6['read_utc'])

    os.makedirs(out)
    os.makedirs(os.path.join(out, 'tools'))
    for name in FILES:
        with open(os.path.join(out, name), 'x', encoding='utf-8') as f:
            f.write(texts[name])
    with open(os.path.join(out, T.ETAB), 'xb') as f:
        f.write(read(etab_path))
    with open(os.path.join(out, T.ETAB6), 'xb') as f:
        f.write(read(etab6_path))
    for name in TOOLS:
        with open(os.path.join(out, 'tools', name), 'xb') as f:
            f.write(read(os.path.join(HERE, name)))

    def h(name):
        return sha_bytes(read(os.path.join(out, name)))
    draft_rows = ['| `%s` | `%s` |' % (os.path.join(draft, n), sha_bytes(read(os.path.join(draft, n)))) for n in FILES]
    draft_rows.append('| `%s` | `%s` |' % (etab_path, sha_bytes(read(etab_path))))
    draft_rows.append('| `%s` | `%s` |' % (etab6_path, sha_bytes(read(etab6_path))))
    n_cited = sum(1 for r in rows if r['disposition'] == 'CITED_PINNED')
    n6_cited = sum(1 for r in rows6 if r['disposition'] == 'CITED_PINNED')
    idx = [
        '# INDEX_R3A (%s): the miss-reading prereg r3a. Claude4, dispatches 0585, 0606 and 0619 (A98), and 0687 (A133)' % a.label, '',
        'Built by `tools/make_miss_reading_c4v005.py` from the draft folder below, with exclusive create into a new folder. '
        'The V005 entry table in the prereg\'s sources section is rendered from the hand-written `%s`, after the generator '
        'checked it against the V005 bytes (every heading once, in file order, verbatim; each pinned section sha). The cited '
        'V005 set is taken from the texts, and every cited entry is pinned.' % T.ETAB, '',
        '| file | role | sha256 |', '|---|---|---|',
        '| %s | the prereg text r3a (unsealed) | `%s` |' % (T.PREREG, h(T.PREREG)),
        '| %s | where each clause comes from; dispatch coverage; closure tables | `%s` |' % (T.CSM, h(T.CSM)),
        '| %s | root items, each with a recommendation | `%s` |' % (T.ROOT, h(T.ROOT)),
        '| %s | the target-free source of every numeric token in the three texts | `%s` |' % (T.PROV, h(T.PROV)),
        '| %s | the hand-written V005 entry table, read at `%s` | `%s` |' % (T.ETAB, et['read_utc'], h(T.ETAB)),
        '| %s | the hand-written V006 entry table, read at `%s` | `%s` |' % (T.ETAB6, et6['read_utc'], h(T.ETAB6)),
        '| tools/check_target_free_c4v004.py | the target-free check | `%s` |' % h('tools/check_target_free_c4v004.py'),
        '| tools/test_check_target_free_c4v004.py | the mutation test | `%s` |' % h('tools/test_check_target_free_c4v004.py'),
        '| tools/make_miss_reading_c4v005.py | this generator | `%s` |' % h('tools/make_miss_reading_c4v005.py'), '',
        '**Draft inputs, for replay:**', '', '| draft file | sha256 |', '|---|---|'] + draft_rows + ['',
        '**V005 at assembly:** `%s`, from %s. The entry table covers its %d headings; %d are CITED_PINNED.' % (
            v_sha, 'the live addendum' if not a.v005 else 'the byte copy `%s`' % v_path, len(rows), n_cited), '',
        '**V006 at assembly:** `%s`, from %s. The V006 entry table covers its %d headings; %d are CITED_PINNED. The seal entry, '
        'when root writes it, is the first V006 heading naming the rendered prereg\'s sha; it and later entries lie outside the '
        'table.' % (v6_sha, 'the live addendum' if not a.v006 else 'the byte copy `%s`' % v6_path, len(rows6), n6_cited), '',
        '**Generator hook self-probe** (direct calls, no side effects): %s.' % '; '.join(
            '%s %s' % (n, g) for n, _, g in probes), '',
        '**Results.** The check writes `TARGET_FREE_CHECK_R3A.json` and the mutation test `TARGET_FREE_MUTATION_TEST_R3A.json`. '
        '`HASHES_R3A.txt` gives the sha256 of every file. The generator exits 0 only when the target-free and currency verdicts '
        'both PASS and every mutation case and hook probe is caught. This INDEX is written before the checks, so that the '
        'check scans it.', '',
        '**What the check establishes, and what it does not.** It is a mechanical check against fixed deny-lists and a '
        'listed-value inventory; it is not exhaustive and it is not a proof.',
        '- **Checked from bytes:**',
        '  - T1 to T3: no deny-listed term (also split by separators), data-file extension, unpinned NGC3198-named file, URL, '
        'HTML entity or comment, disallowed letter, velocity unit or target-symbol value (symbol then value, value then symbol, '
        'or a symbol column of a table) in the three texts, this INDEX, the provenance JSON or the two entry-table JSONs, and no '
        'unexpected file in the bundle;',
        '  - T4: every number token of the three texts and of the JSON notes that survives the stated stripping rules is listed '
        '(digits grouped by underscores or thousands commas, leading-dot numbers and numbers before a prime or inside emphasis '
        'included), every listed value occurs, every category is in the closed list and passes its verification (radii and '
        'node values against bytes; quoted values located in pinned sources; labels shape-checked; post numbers against the '
        'exchange folders); the census lists every occurrence with its context;',
        '  - T5: every sources row parses and every pinned source hashes as stated; the cited V005 entries are pinned by section '
        'sha, with allow-listed end-markers and a tail pin; a cited V006 entry must be pinned in the V006 table;',
        '  - T6: every clause is mapped;',
        '  - T7 (currency, not target-freeness): the V005 entry table covers the V005 bytes exactly, and nothing in V005 changed '
        'since it was read; the V006 entry table does the same for every V006 heading before this text\'s seal entry.',
        '- **Not established by the script:** that no rule depends on a target value (a semantic property, which the lens '
        'reviews check), and that the shape-checked categories are right (review checks them against the cited sources).',
        '- **No target was ever opened.** The check cannot compare against target values, and never needs to.',
        '- **Stated limits of the check and its hook:**'] + ['  - %s;' % x for x in T.LIMITS] + ['']
    with open(os.path.join(out, T.INDEX), 'x', encoding='utf-8') as f:
        f.write('\n'.join(idx))

    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')
    chk_out = os.path.join(out, 'TARGET_FREE_CHECK_R3A.json')
    cmd = [PY, '-I', '-B', chk, '--dir', out, '--provenance', os.path.join(out, T.PROV), '--slots', SLOTS,
           '--expect-slots-sha', SLOTS_SHA, '--nodes', NODES, '--expect-nodes-sha', NODES_SHA, '--out', chk_out]
    if a.v005:
        cmd += ['--v005', v_path]
    if a.v006:
        cmd += ['--v006', v6_path]
    rc_chk = subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    res = json.loads(read(chk_out).decode('utf-8'))
    cmd = [PY, '-I', '-B', tst, '--built', out, '--work', work]
    if a.v005:
        cmd += ['--v005', v_path]
    if a.v006:
        cmd += ['--v006', v6_path]
    mt = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    mtd = json.loads(mt.stdout)
    with open(os.path.join(out, 'TARGET_FREE_MUTATION_TEST_R3A.json'), 'x', encoding='utf-8') as f:
        f.write(json.dumps(mtd, indent=1, sort_keys=True, ensure_ascii=False) + '\n')
    names = sorted(FILES) + [T.ETAB, T.ETAB6, T.INDEX, 'TARGET_FREE_CHECK_R3A.json', 'TARGET_FREE_MUTATION_TEST_R3A.json'] + ['tools/' + n for n in TOOLS]
    with open(os.path.join(out, 'HASHES_R3A.txt'), 'x', encoding='utf-8') as f:
        for n in names:
            f.write('%s  %s\n' % (h(n), n))
    t4 = res['checks']['T4_NUMBER_PROVENANCE']
    summary = {'out': out, 'target_free': res['verdict_target_free'], 'currency': res['verdict_currency'], 'check_exit': rc_chk.returncode,
               'check_stderr': rc_chk.stderr[-600:], 'mutation_all_ok': mtd.get('all_ok'), 'n_cases': mtd.get('n_cases'),
               'failed_cases': [c['case'] for c in mtd.get('cases', []) if not c.get('ok')],
               'hook_probes_ok': mtd.get('hook_probes_all_ok'), 'mutation_stderr': mt.stderr[-600:],
               'failed_checks': {k: {kk: vv for kk, vv in v.items() if kk not in ('pass', 'numeric_tokens', 'closed_category_list',
                                                                                  'token_origins_other_than_plain_number', 'sources',
                                                                                  'v005_entries', 'files_scanned')}
                                 for k, v in res['checks'].items() if not v['pass']},
               'missing_from_provenance': t4['missing_from_provenance'], 'v005_sha': v_sha, 'v006_sha': v6_sha,
               'hashes': {n: h(n) for n in names}}
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    ok = res['verdict_target_free'] == 'PASS' and res['verdict_currency'] == 'PASS' and mtd.get('all_ok')
    return 0 if ok else 2


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except BuildError as e:
        sys.stderr.write('BUILD REFUSED: %s\n' % e)
        raise SystemExit(4)
