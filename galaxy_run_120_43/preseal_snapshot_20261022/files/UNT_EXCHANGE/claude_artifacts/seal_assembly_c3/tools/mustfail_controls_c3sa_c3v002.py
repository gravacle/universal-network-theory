# c3v002: the later entries are read from the frozen bytes (every heading after the prereg's last cited entry), not hardcoded
# (c3v001 hardcoded A102, A103 and went stale when A104 landed at 22:13Z).
# Claude3 (FROM_CODEX/0639 + 0640): MUST_FAIL controls for SA-CX1-B1 (no target metadata before a symlink refusal) and SA-CX1-B3 /
# PV-D05-1 (v003 dispositions contract). In-process; everything it creates is synthetic and lies under OUTDIR (exclusive creates).
# Every stat / lstat / readlink / access / open / listdir / scandir is counted, and BLOCKED (PermissionError before the syscall) when
# its path lies under a case's link target, is a protected look-alike, or is /.vol: so even the old helper's reproduction never reads
# a target's metadata, and no real protected path can be touched. The old helper is never given the /.vol alias.
# usage: python3 -I -B -X pycache_prefix=<empty> mustfail_controls_c3sa.py OUTDIR OLD_HELPER=SHA NEW_HELPER=SHA R5=SHA TABLE_BYTES=SHA OPEN_V005=SHA
import hashlib, json, os, sys, types, time
OUT = sys.argv[1]
def pinarg(s):
    p, h = s.rsplit('=', 1); return p, h
OLD, NEW, R5, TB, OPEN = (pinarg(x) for x in sys.argv[2:7])
def rd(p, h):
    b = open(p, 'rb').read(); assert hashlib.sha256(b).hexdigest() == h, p; return b
def load(p, h, name):                      # SA-CX1-B2 pattern: one read, verify, compile that buffer, exec
    m = types.ModuleType(name); m.__file__ = p; sys.modules[name] = m
    exec(compile(rd(p, h), p, 'exec', dont_inherit=True), m.__dict__); return m
Hold, Hnew = load(OLD[0], OLD[1], 'helper_old_c3v007'), load(NEW[0], NEW[1], 'helper_new_c3v009')
os.mkdir(OUT)
B1 = OUT + '/b1'; os.mkdir(B1)
for d in ('LOOK', 'LOOK/KMAX_A2F10_C5H_RUN_V001', 'LOOK/runs_ext', 'LOOK/runs_ext/UVT_FAKE_RUN', 'plain_dir'):
    os.mkdir(B1 + '/' + d)
for f in ('LOOK/KMAX_A2F10_C5H_RUN_V001/dummy.txt', 'LOOK/runs_ext/UVT_FAKE_RUN/dummy.txt', 'plain_dir/dummy.txt'):
    with open(B1 + '/' + f, 'x') as fh:
        fh.write('SYNTHETIC LOOK-ALIKE (Claude3 0639 MUST_FAIL control); not a run file\n')
LOOKC5H = B1 + '/LOOK/KMAX_A2F10_C5H_RUN_V001'
os.symlink(LOOKC5H, B1 + '/alias_abs'); os.symlink('LOOK/KMAX_A2F10_C5H_RUN_V001', B1 + '/alias_rel')
os.symlink('hop2', B1 + '/hop1'); os.symlink('LOOK/KMAX_A2F10_C5H_RUN_V001', B1 + '/hop2')
os.symlink('LOOK/runs_ext/UVT_FAKE_RUN', B1 + '/alias_uvt'); os.symlink('/.vol/1/2', B1 + '/alias_vol')
os.symlink('plain_dir', B1 + '/plain_alias')
DUMMY_SHA = hashlib.sha256(open(B1 + '/plain_dir/dummy.txt', 'rb').read()).hexdigest()
# ---------------------------------------------------------------- counting + blocking wrappers
REC = {'calls': [], 'blocked': []}
TARGETS = []
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
        REC['calls'].append((kind, s)); return fn(p, *a, **k)
    return w
os.lstat, os.stat, os.readlink, os.access = _wrap('lstat', _ol), _wrap('stat', _os), _wrap('readlink', _orl), _wrap('access', _oa)
def hook(ev, args):
    if ev in ('open', 'os.listdir', 'os.scandir') and args and not isinstance(args[0], int) and args[0] is not None:
        s = os.fsdecode(args[0])
        if is_target(s):
            REC['blocked'].append((ev, s)); raise PermissionError('MUSTFAIL_BLOCKED %s %s' % (ev, s))
sys.addaudithook(hook)
def case(helper, fn, targets):
    TARGETS[:] = targets; REC['calls'], REC['blocked'] = [], []
    try:
        fn(helper); verdict, code = 'PASS', ''
    except Exception as e:
        verdict, code = ('REFUSE' if type(e).__name__ == 'Refuse' else 'ERROR:' + type(e).__name__), str(e)[:160]
    n = len(REC['blocked'])
    TARGETS[:] = []
    return {'verdict': verdict, 'code': code, 'target_metadata_attempts': n, 'attempts': REC['blocked'][:6]}
C5T = [LOOKC5H, B1 + '/hop2']
cases = [
 ('B1-1 pin through an absolute alias whose text names the protected look-alike', lambda H: H.pin(B1 + '/alias_abs/dummy.txt', DUMMY_SHA), C5T, True, 'REFUSE'),
 ('B1-2 path through a relative alias to the protected look-alike', lambda H: H.path_policy(B1 + '/alias_rel/dummy.txt', True), C5T, True, 'REFUSE'),
 ('B1-3 two-hop alias (innocent first text) to the protected look-alike', lambda H: H.path_policy(B1 + '/hop1/dummy.txt', True), C5T, True, 'REFUSE'),
 ('B1-4 alias to a runs_ext/UVT_* look-alike', lambda H: H.path_policy(B1 + '/alias_uvt/dummy.txt', True), [B1 + '/LOOK/runs_ext'], True, 'REFUSE'),
 ('B1-5 alias to an innocent directory (still not followed)', lambda H: H.path_policy(B1 + '/plain_alias/dummy.txt', True), [B1 + '/plain_dir'], True, 'REFUSE'),
 ('B1-6 output whose parent is an alias to the protected look-alike', lambda H: H.path_policy(B1 + '/alias_abs/new_out.json', False), C5T, True, 'REFUSE'),
 ('B1-7 dangling alias whose text is /.vol (new helper only)', lambda H: H.path_policy(B1 + '/alias_vol', True), ['/.vol'], False, 'REFUSE'),
 ('B1-8 control: the canonical path (no link)', lambda H: H.pin(B1 + '/plain_dir/dummy.txt', DUMMY_SHA), [], True, 'PASS'),
]
b1 = []
for name, fn, tg, run_old, want in cases:
    row = {'case': name, 'expected_new': want + (' with 0 target-metadata attempts' if want == 'REFUSE' else '')}
    row['new_c3v009'] = case(Hnew, fn, tg)
    row['old_c3v007'] = case(Hold, fn, tg) if run_old else 'NOT RUN (would reach the real /.vol)'
    row['MUST_FAIL_ok'] = (row['new_c3v009']['verdict'] == want and row['new_c3v009']['target_metadata_attempts'] == 0)
    b1.append(row)
os.lstat, os.stat, os.readlink, os.access = _ol, _os, _orl, _oa
# ---------------------------------------------------------------- B3 / PV-D05-1 fixtures (v003 object contract)
B3 = OUT + '/b3'; os.mkdir(B3)
fb = rd(*OPEN); tb = rd(*TB)
def x(path, b):
    with open(path, 'xb') as f: f.write(b)
    return hashlib.sha256(b).hexdigest()
real_fz = B3 + '/FROZEN_REAL_BYTES_COPY.md'; real_sha = x(real_fz, fb)
sec = lambda b, e: Hnew._section(b, e)
a90_new_line = b'SYNTHETIC FIXTURE LINE (Claude3 0640 MUST_FAIL control; NOT ROOT TEXT): A90 changed after the table.\n'
s90 = sec(fb, 'A90'); assert s90 is not None
syn = fb.replace(s90, s90.rstrip(b'\n') + b'\n' + a90_new_line + b'\n', 1); assert syn != fb
syn_fz = B3 + '/SYNTHETIC_FROZEN_A90_CHANGED_NOT_ROOT_TEXT.md'; syn_sha = x(syn_fz, syn)
SCH = Hnew.DISPOSITIONS_SCHEMA
import re as _re
LAST_CITED = max(Hnew._cited(json.loads(rd(*R5))))
def later_names(b):
    return ['A%d' % n for n in sorted({int(m.group(1)) for m in _re.finditer(rb'^## A(\d{1,3}):', b, _re.M)}) if n > LAST_CITED]
def later_rows(b):
    return [{'entry': e, 'disposition': 'no_change', 'reason': 'FIXTURE reason for %s' % e, 'section_sha256': hashlib.sha256(sec(b, e)).hexdigest()}
            for e in later_names(b)]
s90n = hashlib.sha256(sec(syn, 'A90')).hexdigest()
old90 = sec(tb, 'A90').decode('utf-8')
excerpt_old = old90.splitlines()[2][:60]
def obj(rows, fsha, **kw):
    d = {'schema': SCH, 'frozen_addendum_sha256': fsha, 'entries': rows}; d.update(kw); return d
F = []
F.append(('B3-P1 v003 object, every later entry no_change (real bytes)', obj(later_rows(fb), real_sha), real_fz, real_sha, 'PASS'))
F.append(('B3-N1 legacy bare list', later_rows(fb), real_fz, real_sha, 'DISPOSITIONS_LEGACY_BARE_LIST_REFUSED'))
F.append(('B3-N2 legacy key dispositions', {'dispositions': later_rows(fb)}, real_fz, real_sha, 'DISPOSITIONS_LEGACY_KEY_REFUSED'))
F.append(('B3-N3 legacy key rows', {'rows': later_rows(fb)}, real_fz, real_sha, 'DISPOSITIONS_LEGACY_KEY_REFUSED'))
F.append(('B3-N4 wrong schema string', dict(obj(later_rows(fb), real_sha), schema='UNT_V007_SOMETHING_ELSE'), real_fz, real_sha, 'DISPOSITIONS_SCHEMA'))
F.append(('B3-N5 extra top-level key', obj(later_rows(fb), real_sha, note='x'), real_fz, real_sha, 'DISPOSITIONS_KEYS'))
F.append(('B3-N6 row for an unchanged cited entry (A85)', obj(later_rows(fb) + [{'entry': 'A85', 'disposition': 'no_change', 'reason': 'x', 'section_sha256': hashlib.sha256(sec(fb, 'A85')).hexdigest()}], real_sha), real_fz, real_sha, 'DISPOSITION_FOR_UNCHANGED_CITED_OR_TABLED_ENTRY'))
F.append(('B3-N7 empty reason on a later entry', obj([dict(later_rows(fb)[0], reason='  '), later_rows(fb)[1]], real_sha), real_fz, real_sha, 'DISPOSITION_EMPTY_REASON'))
r90 = lambda **kw: dict({'entry': 'A90', 'section_sha256': s90n}, **kw)
F.append(('B3-N8 plain no_change on the changed cited entry A90 (PV-D05-1)', obj(later_rows(syn) + [r90(disposition='no_change', reason='x')], syn_sha), syn_fz, syn_sha, 'DISPOSITION_NO_CHANGE_ON_CHANGED_ENTRY'))
F.append(('B3-N9 generic changed_text ("## A")', obj(later_rows(syn) + [r90(disposition='no_change_after_change', changed_text='## A', why_no_prereg_effect='x')], syn_sha), syn_fz, syn_sha, 'DISPOSITION_CHANGED_TEXT_IN_OLD_BYTES'))
F.append(('B3-N10 changed_text present in the old bytes', obj(later_rows(syn) + [r90(disposition='no_change_after_change', changed_text=excerpt_old, why_no_prereg_effect='x')], syn_sha), syn_fz, syn_sha, 'DISPOSITION_CHANGED_TEXT_IN_OLD_BYTES'))
F.append(('B3-N11 changed_text absent from the new bytes', obj(later_rows(syn) + [r90(disposition='no_change_after_change', changed_text='TEXT THAT IS NOWHERE', why_no_prereg_effect='x')], syn_sha), syn_fz, syn_sha, 'DISPOSITION_CHANGED_TEXT_NOT_IN_NEW_BYTES'))
F.append(('B3-N12 empty why_no_prereg_effect', obj(later_rows(syn) + [r90(disposition='no_change_after_change', changed_text=a90_new_line.decode().strip(), why_no_prereg_effect=' ')], syn_sha), syn_fz, syn_sha, 'DISPOSITION_WHY_NO_PREREG_EFFECT_EMPTY'))
F.append(('B3-N13 revised without a prereg-revision pointer', obj(later_rows(syn) + [r90(disposition='revised', reason='x')], syn_sha), syn_fz, syn_sha, 'DISPOSITION_REVISED_NEEDS_PREREG_REVISION_POINTER'))
F.append(('B3-N14 changed A90 left without a row', obj(later_rows(syn), syn_sha), syn_fz, syn_sha, 'DISPOSITION_ENTRIES'))
F.append(('B3-P2 no_change_after_change naming the change exactly', obj(later_rows(syn) + [r90(disposition='no_change_after_change', changed_text=a90_new_line.decode().strip(), why_no_prereg_effect='FIXTURE: the synthetic line changes no prereg clause')], syn_sha), syn_fz, syn_sha, 'PASS'))
F.append(('B3-P3 revised with a prereg-revision pointer', obj(later_rows(syn) + [r90(disposition='revised', reason='x', prereg_revision='FIXTURE: prereg r6 clause X')], syn_sha), syn_fz, syn_sha, 'PASS'))
b3 = []
class A: pass
for i, (name, d, fz, fsha, want) in enumerate(F):
    p = B3 + '/D%02d.json' % (i + 1)
    dsha = x(p, (json.dumps(d, indent=1) + '\n').encode())
    a = A(); a.dispositions, a.dispositions_sha, a.prereg, a.prereg_sha = p, dsha, R5[0], R5[1]
    a.frozen, a.frozen_sha, a.table_bytes, a.table_bytes_sha = fz, fsha, TB[0], TB[1]
    try:
        res = Hnew._dispositions(a); verdict, code = 'PASS', res.get('entries')
    except Exception as e:
        verdict, code = 'REFUSE', str(e)[:170]
    ok = (verdict == 'PASS') if want == 'PASS' else (verdict == 'REFUSE' and str(code).startswith(want))
    b3.append({'case': name, 'fixture': {'path': p, 'sha256': dsha}, 'expected': want, 'verdict': verdict, 'code': code, 'MUST_FAIL_ok': ok})
out = {'schema': 'C3SA_MUSTFAIL_CONTROLS_V001', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'old_helper': OLD, 'new_helper': NEW,
       'B1_no_target_metadata_before_symlink_refusal': b1, 'B3_v003_dispositions_contract_PV_D05_1': b3,
       'v003_tool1_on_these_fixtures': 'UNTESTED: seal tools v003 not landed (its dev work copy predates PV-D05-1)',
       'all_ok': all(r['MUST_FAIL_ok'] for r in b1) and all(r['MUST_FAIL_ok'] for r in b3)}
with open(OUT + '/MUSTFAIL_RESULTS_C3SA.json', 'x') as f:
    f.write(json.dumps(out, indent=1) + '\n')
for r in b1:
    o = r['old_c3v007']; o = o if isinstance(o, str) else '%s/%d' % (o['verdict'], o['target_metadata_attempts'])
    print('%-74s new %s/%d  old %s  ok=%s' % (r['case'][:74], r['new_c3v009']['verdict'], r['new_c3v009']['target_metadata_attempts'], o, r['MUST_FAIL_ok']))
for r in b3:
    print('%-62s %-6s ok=%s  %s' % (r['case'][:62], r['verdict'], r['MUST_FAIL_ok'], str(r['code'])[:70]))
print('ALL_OK', out['all_ok'])
