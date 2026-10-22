# Claude3 (FROM_CODEX/0642, A105): MUST_FAIL controls for W7-S1 (the admission allowlist is exactly BUILD_V007's 15-row table) and
# RP-S1 (the step-2 output root is created exclusively, new and empty). In-process; every case goes through the helper's own CLI
# entry, main(argv), exactly as ROOT_SEAL_STEPS calls it. Everything created is synthetic and lies under OUTDIR (mkdir / open 'x'),
# except case R-14, which runs CHECK mode (writes nothing) on the real literal path. As in the B1 controls, every stat / lstat /
# readlink / access / open / listdir / scandir / mkdir at or under a case's link target is counted and BLOCKED before its syscall.
# usage: python3 -I -B -X pycache_prefix=<empty> mustfail_w7_rps1_c3sa_c3v001.py OUTDIR HELPER=SHA OLD_HELPER=SHA BUILD7=SHA BUILD6=SHA
import contextlib, hashlib, io, json, os, sys, types
OUT = sys.argv[1]
def pinarg(s):
    p, h = s.rsplit('=', 1); return p, h
(HP, HS), (OP, OSHA), (B7, B7S), (B6, B6S) = (pinarg(x) for x in sys.argv[2:6])
def rd(p, h):
    b = open(p, 'rb').read(); assert hashlib.sha256(b).hexdigest() == h, p; return b
def load(p, h, name):                      # SA-CX1-B2 pattern: one read, verify, compile that buffer, exec
    m = types.ModuleType(name); m.__file__ = p; sys.modules[name] = m
    exec(compile(rd(p, h), p, 'exec', dont_inherit=True), m.__dict__); return m
H = load(HP, HS, 'helper_c3v011'); HOLD = load(OP, OSHA, 'helper_c3v010')
os.mkdir(OUT)
# ------------------------------------------------------------------------------------------- counting + blocking wrappers
REC = {'blocked': []}; TARGETS = []
def is_target(s):
    sc = s.casefold()
    return (sc.startswith('/.vol') or 'kmax_a2f10_c5h_run_v001' in sc or '/runs_ext' in sc or '/uvt_' in sc
            or any(s == t or s.startswith(t + '/') for t in TARGETS))
_ol, _os, _orl, _oa = os.lstat, os.stat, os.readlink, os.access
def _wrap(kind, fn):
    def w(p, *a, **k):
        s = os.fsdecode(p) if not isinstance(p, int) else ''
        if s and is_target(s):
            REC['blocked'].append((kind, s)); raise PermissionError('MUSTFAIL_BLOCKED %s %s' % (kind, s))
        return fn(p, *a, **k)
    return w
os.lstat, os.stat, os.readlink, os.access = _wrap('lstat', _ol), _wrap('stat', _os), _wrap('readlink', _orl), _wrap('access', _oa)
def hook(ev, args):
    if ev in ('open', 'os.listdir', 'os.scandir', 'os.mkdir') and args and not isinstance(args[0], int) and args[0] is not None:
        s = os.fsdecode(args[0])
        if is_target(s):
            REC['blocked'].append((ev, s)); raise PermissionError('MUSTFAIL_BLOCKED %s %s' % (ev, s))
sys.addaudithook(hook)
def cli(mod, argv, targets=()):
    TARGETS[:] = list(targets); REC['blocked'] = []
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        rc = mod.main(argv)
    TARGETS[:] = []
    lines = [ln for ln in err.getvalue().splitlines() if ln.strip()]
    v = json.loads(lines[-1]) if lines else {'verdict': 'NO_OUTPUT'}
    return rc, v, len(REC['blocked'])
RESULTS = []
def case(cid, desc, argv, want, targets=(), post=None, mod=None):
    rc, v, n = cli(mod or H, argv, targets)
    row = {'case': cid, 'what': desc, 'want': want, 'verdict': v.get('verdict'), 'exit': rc, 'code': (v.get('code') or '')[:220],
           'target_metadata_attempts': n}
    if post is not None:
        row['post'] = post()
    row['MUST_FAIL_ok'] = (row['verdict'] == want and n == 0 and all((row.get('post') or {}).values()))
    if want == 'PASS':
        row['detail'] = {k: v[k] for k in ('output_root', 'w7_s1_allowlist') if k in v}
    RESULTS.append(row); return v
# ============================================================================================= W7-S1
W = OUT + '/w7'; os.mkdir(W)
b7 = rd(B7, B7S).decode('utf-8'); rows = H._build_table(b7)
b6 = rd(B6, B6S).decode('utf-8'); rows6 = H._build_table(b6)
V006_WRITERS = [r for r in rows6 if r not in rows]
FACTS = {'build_v007_rows': len(rows), 'build_v006_rows': len(rows6), 'first_13_equal': rows6[:13] == rows[:13],
         'v006_rows_not_in_v007': [(p.rsplit('/', 1)[1], h[:8]) for p, h in V006_WRITERS],
         'v007_rows_14_15': [(p.rsplit('/', 1)[1], h[:8]) for p, h in rows[13:]]}
BINDER = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/bind_sealed_launch_plan_cx1v001.py',
          'f3e4e2beeb8f1cb151892fd903b889c471cea58fea1b67c72552137d037575ca')
assert ('%s  %s' % (BINDER[1], BINDER[0])) in b7 and all(('%s  %s' % (h, p)) in b7 for p, h in V006_WRITERS)  # BUILD cites them (L45, L46, L54)
def cfg_with(allow, build=(B7, B7S)):
    return {'schema': H.CONFIG_SCHEMA, 'authority': dict(H.AUTHORITY),
            'seal': {'path': W + '/SYNTHETIC_SEAL_RECORD_NOT_A_SEAL.json', 'sha256': '0' * 64},
            'prereg': {'path': W + '/SYNTHETIC', 'sha256': '0' * 64}, 'compare': {'path': W + '/SYNTHETIC', 'sha256': '0' * 64},
            'build': {'path': build[0], 'sha256': build[1]}, 'producer_allowlist': allow}
N = [0]
def write_cfg(obj=None, text=None):
    N[0] += 1; p = '%s/CONFIG_SYNTHETIC_%02d.json' % (W, N[0])
    t = text if text is not None else json.dumps(obj, indent=1) + '\n'
    with open(p, 'x') as f:
        f.write(t)
    return p, hashlib.sha256(t.encode()).hexdigest()
def w7(cid, desc, obj=None, text=None, want='REFUSE', build=(B7, B7S)):
    p, h = write_cfg(obj, text)
    case(cid, desc, ['check-config-allowlist', '--config', p, '--config-sha', h, '--build', build[0], '--build-sha', build[1]], want)
exact = {p: h for p, h in rows}
w7('W7-0', 'control: exactly the 15 BUILD_V007 rows in table order', cfg_with(exact), want='PASS')
w7('W7-1', '17 rows: the 15 plus the V006 writers 9fbdb0ca / 500f8b6a', cfg_with(dict(exact, **{p: h for p, h in V006_WRITERS})))
w7('W7-2', "V006's old 15 rows (rows 1-13 plus the V006 writers; BUILD_V006 fb9e6a4a table)", cfg_with({p: h for p, h in rows6}))
tr = dict(exact); p0, h0 = rows[0]; del tr[p0]; tr = dict([(p0[:-4], h0)] + list(tr.items()))
w7('W7-3', 'substring-matched row: row 1 path truncated (its "<sha>  <path>" is a substring of BUILD text)', cfg_with(tr))
bn = dict(list(exact.items())[:14] + [BINDER])
w7('W7-4', 'substring-matched row: the binder f3e4e2be (cited in BUILD L54, outside the table) in place of row 15', cfg_with(bn))
ro = list(exact.items()); ro[0], ro[1] = ro[1], ro[0]
w7('W7-5', 'reordered: rows 1 and 2 swapped', cfg_with(dict(ro)))
t = json.dumps(cfg_with(exact), indent=1) + '\n'; first = '  "%s": "%s",\n' % rows[0]; assert t.count(first) == 1
w7('W7-6', 'duplicated row: row 1 repeated as a duplicate JSON key (16 entries in the text)', text=t.replace(first, first + first))
dsh = dict(list(exact.items())[:14] + [(W + '/other_name.py', rows[13][1])])
w7('W7-7', 'duplicated sha: row 15 replaced by row 14 sha under another path', cfg_with(dsh))
w7('W7-8', '14 rows (row 15 missing)', cfg_with(dict(list(exact.items())[:14])))
w7('W7-9', 'list form [[sha, path], ...] instead of an object', cfg_with([[h, p] for p, h in rows]))
up = dict(exact); up[rows[2][0]] = rows[2][1].upper()
w7('W7-10', 'row 3 sha in upper case (not byte-equal)', cfg_with(up))
sp = dict([(p + ' ', h) if i == 4 else (p, h) for i, (p, h) in enumerate(rows)])
w7('W7-11', 'row 5 path with a trailing space (not byte-equal)', cfg_with(sp))
w7('W7-12', 'config pins BUILD_V006 while checked against BUILD_V007', cfg_with(exact, build=(B6, B6S)))
def synth_build(cid, desc, newtext):
    p = '%s/BUILD_SYNTHETIC_%s.md' % (W, cid)
    with open(p, 'x') as f:
        f.write(newtext)
    h = hashlib.sha256(newtext.encode()).hexdigest()
    w7(cid, desc, cfg_with(exact, build=(p, h)), build=(p, h))
last = '%s  %s\n```' % (rows[14][1], rows[14][0]); assert b7.count(last) == 1
synth_build('W7-13a', 'BUILD copy whose table has a 16th row (a V006 writer)', b7.replace(last, '%s  %s\n%s  %s\n```' % (rows[14][1], rows[14][0], V006_WRITERS[0][1], V006_WRITERS[0][0])))
synth_build('W7-13b', 'BUILD copy with prose inside the section, outside the fence', b7.replace('## Supported runtime entry allowlist\n\n', '## Supported runtime entry allowlist\n\nSYNTHETIC prose line\n'))
synth_build('W7-13c', 'BUILD copy with the allowlist heading twice', b7 + '\n## Supported runtime entry allowlist\n')
r1 = '%s  %s' % (rows[0][1], rows[0][0]); assert b7.count(r1) == 1
synth_build('W7-13d', 'BUILD copy with one table line using a single space', b7.replace(r1, '%s %s' % (rows[0][1], rows[0][0])))
# ============================================================================================= RP-S1
R = OUT + '/rps1'; os.mkdir(R)
def tree(cid):
    d = '%s/%s' % (R, cid); os.mkdir(d); return d
def orr(path, mode='create', floor='0', extra=()):
    return ['output-root', '--path', path, '--mode', mode, '--min-free-gib', floor] + list(extra)
def lex(p):
    try:
        os.lstat(p); return True
    except FileNotFoundError:
        return False
d = tree('R-0a'); root = d + '/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007'
v0 = case('R-0a', 'create; parent absent (as on disk today): parent and root created, verified', orr(root), 'PASS',
          post=lambda: {'root_is_real_empty_dir': os.path.isdir(root) and not os.path.islink(root) and os.listdir(root) == []})
d = tree('R-0b'); os.mkdir(d + '/UNT_INTERNAL_RUNS'); root_b = d + '/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007'
case('R-0b', 'create; parent exists', orr(root_b), 'PASS', post=lambda: {'root_created': os.path.isdir(root_b)})
d = tree('R-0c'); root_c = d + '/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007'
case('R-0c', 'check mode (step 0) writes nothing', orr(root_c, 'check'), 'PASS', post=lambda: {'parent_still_absent': not lex(d + '/UNT_INTERNAL_RUNS')})
o = v0.get('output_root', {})
case('R-0d', 'verify mode on R-0a with its recorded st_dev/st_ino', ['output-root', '--path', root, '--mode', 'verify', '--expect-dev', str(o.get('st_dev')), '--expect-ino', str(o.get('st_ino'))], 'PASS')
d = tree('R-1'); os.mkdir(d + '/P'); os.mkdir(d + '/P/ROOT'); ino1 = os.lstat(d + '/P/ROOT').st_ino
case('R-1a', 'root exists as a directory (check mode)', orr(d + '/P/ROOT', 'check'), 'REFUSE')
case('R-1b', 'root exists as a directory (create mode)', orr(d + '/P/ROOT'), 'REFUSE',
     post=lambda: {'same_dir_untouched': os.lstat(d + '/P/ROOT').st_ino == ino1 and os.listdir(d + '/P/ROOT') == []})
d = tree('R-2'); os.mkdir(d + '/P'); open(d + '/P/ROOT', 'x').write('SYNTHETIC regular file (MUST_FAIL control)\n')
case('R-2', 'root exists as a regular file', orr(d + '/P/ROOT'), 'REFUSE')
d = tree('R-3'); os.mkdir(d + '/P'); os.symlink(d + '/ELSEWHERE_ABSENT', d + '/P/ROOT')
case('R-3', 'root exists as a DANGLING symlink', orr(d + '/P/ROOT'), 'REFUSE', targets=[d + '/ELSEWHERE_ABSENT'])
d = tree('R-4'); os.mkdir(d + '/P'); os.mkdir(d + '/ELSEWHERE'); os.symlink(d + '/ELSEWHERE', d + '/P/ROOT')
case('R-4', 'root exists as a symlink to a real directory', orr(d + '/P/ROOT'), 'REFUSE', targets=[d + '/ELSEWHERE'],
     post=lambda: {'target_dir_untouched_empty': os.listdir(d + '/ELSEWHERE') == []})
d4b = tree('R-4b'); os.mkdir(d4b + '/P'); os.symlink(d4b + '/LOOK/KMAX_A2F10_C5H_RUN_V001', d4b + '/P/ROOT')
case('R-4b', 'root is a symlink whose text names a protected look-alike (dangling)', orr(d4b + '/P/ROOT'), 'REFUSE', targets=[d4b + '/LOOK'])
d5 = tree('R-5'); os.mkdir(d5 + '/REALPARENT'); os.symlink(d5 + '/REALPARENT', d5 + '/P')
case('R-5', 'the parent is a symlink to a real directory', orr(d5 + '/P/ROOT'), 'REFUSE', targets=[d5 + '/REALPARENT'],
     post=lambda: {'nothing_created_through_the_link': os.listdir(d5 + '/REALPARENT') == []})
d = tree('R-6'); open(d + '/P', 'x').write('SYNTHETIC regular file as the parent\n')
case('R-6', 'the parent is a regular file', orr(d + '/P/ROOT'), 'REFUSE')
d = tree('R-7')
case('R-7', 'the grandparent is missing', orr(d + '/MISSING/P/ROOT'), 'REFUSE', post=lambda: {'nothing_created': not lex(d + '/MISSING')})
d = tree('R-8')
case('R-8', 'firmlink spelling /System/Volumes/Data/Users/...', orr('/System/Volumes/Data' + d + '/P/ROOT'), 'REFUSE', post=lambda: {'nothing_created': os.listdir(d) == []})
d9 = tree('R-9a')
case('R-9a', "'..' as the last component under an ABSENT parent", orr(d9 + '/P/..'), 'REFUSE', post=lambda: {'parent_not_created': not lex(d9 + '/P')})
d9o = tree('R-9a-old')
rc, vo, no = cli(HOLD, orr(d9o + '/P/..'))
RESULTS.append({'case': 'R-9a-old (reproduction, helper c3v010 823c8aca)', 'what': "the same '..' path on c3v010", 'verdict': vo.get('verdict'),
                'code': (vo.get('code') or '')[:200], 'parent_created_before_the_refusal': lex(d9o + '/P'), 'note': 'contrast only; the gap c3v011 closes'})
d = tree('R-9b'); os.mkdir(d + '/P')
case('R-9b', "a '.' component", orr(d + '/P/./ROOT'), 'REFUSE', post=lambda: {'nothing_created': os.listdir(d + '/P') == []})
d10 = tree('R-10')
case('R-10', 'free space below a (synthetic) floor of 100000 GiB', orr(d10 + '/P/ROOT', 'create', '100000'), 'REFUSE', post=lambda: {'nothing_created': not lex(d10 + '/P')})
d11 = tree('R-11'); r11 = d11 + '/P/ROOT'; v11 = cli(H, orr(r11))[1]['output_root']
open(r11 + '/planted.txt', 'x').write('SYNTHETIC entry planted after creation\n')
case('R-11', 'verify after an entry appeared in the root', ['output-root', '--path', r11, '--mode', 'verify', '--expect-dev', str(v11['st_dev']), '--expect-ino', str(v11['st_ino'])], 'REFUSE')
d12 = tree('R-12'); r12 = d12 + '/P/ROOT'; v12 = cli(H, orr(r12))[1]['output_root']
case('R-12', 'verify with another inode than the recorded one', ['output-root', '--path', r12, '--mode', 'verify', '--expect-dev', str(v12['st_dev']), '--expect-ino', str(v12['st_ino'] + 1)], 'REFUSE')
d = tree('R-13')
case('R-13', 'a protected name in the path (runs_ext/)', orr(d + '/runs_ext/P/ROOT'), 'REFUSE', post=lambda: {'nothing_created': os.listdir(d) == []})
REAL = '/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007'
case('R-14', 'the REAL literal path in CHECK mode (step 0 today; writes nothing)', orr(REAL, 'check'), 'PASS',
     post=lambda: {'real_parent_still_absent': not lex('/Users/bgm/Research/UNT_INTERNAL_RUNS')})
d = tree('R-15')
case('R-15', 'an unknown mode', orr(d + '/P/ROOT', 'make'), 'REFUSE', post=lambda: {'nothing_created': os.listdir(d) == []})
case('R-16', 'a non-integer floor', orr(d + '/P/ROOT', 'create', '-1'), 'REFUSE', post=lambda: {'nothing_created': os.listdir(d) == []})
ok = all(r.get('MUST_FAIL_ok', True) for r in RESULTS)
res = {'schema': 'C3SA_MUSTFAIL_W7_RPS1_V001', 'helper': {'path': HP, 'sha256': HS}, 'contrast_helper': {'path': OP, 'sha256': OSHA},
       'build_v007': {'path': B7, 'sha256': B7S}, 'build_v006': {'path': B6, 'sha256': B6S}, 'facts_from_bytes': FACTS,
       'n_cases': len(RESULTS), 'ALL_OK': ok, 'results': RESULTS}
t = json.dumps(res, indent=1) + '\n'
with open(OUT + '/MUSTFAIL_W7_RPS1_RESULTS_C3SA.json', 'x') as f:
    f.write(t)
print(json.dumps({'ALL_OK': ok, 'n': len(RESULTS), 'sha256': hashlib.sha256(t.encode()).hexdigest()}))
for r in RESULTS:
    print('%-8s %-7s exit=%s attempts=%s ok=%s  %s' % (r['case'][:8], r.get('verdict'), r.get('exit'), r.get('target_metadata_attempts'), r.get('MUST_FAIL_ok'), r.get('code', '')[:110]))
