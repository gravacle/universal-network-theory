"""Tests v007 for roster_builder_parent_check_c3v003 (Claude3, backlog #7, D038) on REAL step7 and custody ledger commits.
v002: run() records an exception that escapes the base main (the custody main catches only Stop/Refused, so a
post-commit OSError escapes it: a traceback in a real CLI run) instead of aborting the suite (v001 draft).
v003: the no-read check counts READS right after the call, before the test's own ledger() read (v002 draft).
v004: targets wrapper c3v002 and adds Codex1 0295 B7-1 controls (L1-L5, H4-H6, custody L1c/L2c, mutants M6-M8).
v005: every mutant asserts that its replacement applies exactly once (v004's M1 still matched c3v001 text).
v006: targets c3v003 (Codex1 B7-2): L6/L6c valid trailing-slash dangling link, L7 loop, the K1 14-case kernel
matrix against preflight itself, L5 now PARENT_MISSING, mutants M9/M10, M1/M6/M8 retargeted.
v007: drops two stale explicit c3v002-text asserts (mutate() asserts every replacement) (v006 draft).

The synthetic world, FULL builds, pass drivers and custody copies come from Codex3's cw8 inherited suite
test_inherited_cx3v003.py (7d3afc1f), run under its own read and immutability fences. The base roster builder is the
pinned f710334b module that suite loads (its seams: synthetic registry verifier, guarded reads). A custody breach is
made by chmod 000 on one registered result and on a private custody-copy folder: nothing is deleted or overwritten,
and the permissions are restored at the end. Three real-CLI subprocess checks run first, before the fixture's
no-child-process fence is installed.
usage: $PY -I -B test_roster_parent_check_c3v007.py WORK   (WORK must not exist)"""
import contextlib, hashlib, io, json, os, re, subprocess, sys, types
from pathlib import Path
HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/roster_parent_check_c3')
WRAP = HERE / 'roster_builder_parent_check_c3v003.py'
WRAP_RAW = WRAP.read_bytes()
BASE_PATH = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v003.py'
BASE_SHA = 'f710334b6f5ec2663fbebd826c7b326ebf7ff9eb600e751584de4f518a4e0b11'
FIX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/test_inherited_cx3v003.py')
FIX_RAW = FIX.read_bytes()
assert hashlib.sha256(FIX_RAW).hexdigest() == '7d3afc1f9cccd8dbc54036bbe9ebb151ede0cb850337e2c98bc4644e9933aeda'
RESULTS = []
def check(name, ok, detail=''):
    RESULTS.append({'id': name, 'pass': bool(ok), 'detail': str(detail)[:400]})
# ---- 0. real CLI (subprocess), before the fixture's fences: delegation and one pre-commit refusal
PY = sys.executable
def cli(path, args):
    r = subprocess.run([PY, '-I', '-B', path] + args, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr
check('C1_cli_no_args_identical_to_base', cli(str(WRAP), []) == cli(BASE_PATH, []))
check('C2_cli_unknown_command_identical_to_base', cli(str(WRAP), ['bogus']) == cli(BASE_PATH, ['bogus']))
WORK0 = Path(sys.argv[1] + '_cli'); WORK0.mkdir(); (WORK0 / 'exists').mkdir()
rc, out, err = cli(str(WRAP), ['step7', '--input', str(WORK0 / 'never_read.json'), '--input-sha256', '0' * 64, '--out-dir', str(WORK0 / 'exists')])
check('C3_cli_wrapper_refuses_existing_out_dir_before_input_read', rc == 2 and json.loads(err)['refused'] == 'OUT_DIR_EXISTS' and out == '', (rc, out, err))
# ---- fixture world (installs read/immutability/no-child fences)
src = FIX_RAW.decode().split("\nif len(sys.argv) > 2:\n")[0]
__file__ = str(FIX)
exec(compile(src, str(FIX) + ':definitions', 'exec'), globals())
RB = env.rb
check('F0_fixture_base_is_pinned_f710334b', RB.__file__ == BASE_PATH and hashlib.sha256(Path(BASE_PATH).read_bytes()).hexdigest() == BASE_SHA)
def mutate(old, new):
    assert WRAP_RAW.count(old) == 1, old
    return WRAP_RAW.replace(old, new)
def wrapper(raw=WRAP_RAW, name='w', seam=True):
    m = types.ModuleType(name); m.__file__ = str(WRAP)
    exec(compile(raw, str(WRAP), 'exec'), m.__dict__)
    if seam:
        m.load_base = lambda: RB
    return m
W = wrapper()
def run(fn, argv, cwd=None):
    so, se, old = io.StringIO(), io.StringIO(), os.getcwd()
    try:
        if cwd:
            os.chdir(cwd)
        with contextlib.redirect_stdout(so), contextlib.redirect_stderr(se):
            try:
                rc = fn(argv)
            except Exception as exc:   # escapes the base main: a traceback in a real CLI run
                rc = 'UNCAUGHT:' + type(exc).__name__
    finally:
        os.chdir(old)
    return rc, so.getvalue(), se.getvalue()
def ledger(build_out):
    raw = Path(build_out, 'BUILD_RECORD.json').read_bytes()
    d = Path(json.loads(raw)['step7_ledger_root']) / (RB.LEDGER_DIR_PREFIX + hashlib.sha256(raw).hexdigest())
    return d, sorted(p.name for p in d.iterdir() if re.fullmatch(r'STEP7_\d{4}\.json', p.name))
RO = []
def condition(d, kind):
    if kind == 'exists':
        p = d / 'out_exists'; p.mkdir(); return str(p)
    if kind == 'parent_missing':
        return str(d / 'no_such_parent' / 'out')
    if kind == 'parent_file':
        f = d / 'parent_is_file'; t.wbytes(str(f), b'inert\n'); return str(f / 'out')
    if kind == 'parent_readonly':
        r = d / 'readonly_parent'; r.mkdir(); os.chmod(r, 0o500); RO.append(r); return str(r / 'out')
    raise KeyError(kind)
WRAP_CODE = {'exists': 'OUT_DIR_EXISTS', 'parent_missing': 'OUT_DIR_PARENT_MISSING', 'parent_file': 'OUT_DIR_PARENT_MISSING',
             'parent_readonly': 'OUT_DIR_PARENT_NOT_WRITABLE'}
N = [0]
def step7_setup(tag):
    N[0] += 1; tag = 'c3p7_s7_%02d_%s' % (N[0], tag)
    out = world.build_p1(tag)
    bp = t.pin(os.path.join(out, 'BUILD_RECORD.json')); pp = t.pin(os.path.join(out, 'REPLAY_PLAN.json'))
    one, _, _ = t.drive(env, world.b1, out, 'PASS_ONE'); last, _, _ = t.drive(env, world.b1, out, 'PASS_K')
    d = Path(env.dir(tag + '_in'))
    p1 = jwrite(d / 'one.json', one); pk = jwrite(d / 'last.json', last)
    inp = jwrite(d / 'input.json', {'schema': 'STEP7_INPUT_C2V003', 'build_record': bp, 'replay_plan': pp, 'pass_one': p1, 'pass_k': pk})
    return out, d, ['step7', '--input', inp['path'], '--input-sha256', inp['sha256'], '--out-dir']
# ---- 1. step7: the hazard on the unchanged base (each condition commits, then fails)
for kind in ('exists', 'parent_missing', 'parent_file', 'parent_readonly'):
    out, d, argv = step7_setup('base_' + kind)
    od = condition(d, kind)
    rc, so, se = run(RB.main, argv + [od])
    _, entries = ledger(out)
    check('H1_step7_base_%s_commits_then_fails' % kind, rc != 0 and entries == ['STEP7_0001.json'] and not os.path.exists(os.path.join(od, 'STEP7_RESULT.json')), (rc, se.strip(), entries))
out, d, argv = step7_setup('base_valid')
rc, base_valid_stdout, se = run(RB.main, argv + [str(d / 'out')])
check('V1_step7_base_valid', rc == 0 and json.loads(base_valid_stdout) == {'status': 'NO_NEW_DISCREPANCY', 'ledger_seq': 1}, (rc, base_valid_stdout, se))
# ---- 2. step7 through the wrapper: four refusals before any read or commit, then the valid run is seq 1
out, d, argv = step7_setup('wrap')
for kind in ('exists', 'parent_missing', 'parent_file', 'parent_readonly'):
    od = condition(d, kind); before = len(READS)
    rc, so, se = run(W.main, argv + [od]); reads = len(READS) - before
    _, entries = ledger(out)
    check('W1_step7_wrapper_%s_refused_pre_commit' % kind, rc == 2 and so == '' and json.loads(se) == {'refused': WRAP_CODE[kind], 'detail': od} and entries == [] and reads == 0, (rc, se.strip(), entries, reads))
M2 = wrapper(mutate(b"    if not os.path.isdir(parent):\n        return 'OUT_DIR_PARENT_MISSING'\n", b''), 'm2')
assert M2 is not None and WRAP_RAW.count(b"    if not os.path.isdir(parent):\n        return 'OUT_DIR_PARENT_MISSING'\n") == 1
rc, so, se = run(M2.main, argv + [str(d / 'm2_no_parent' / 'out')])
m2_killed = not (rc == 2 and json.loads(se).get('refused') == 'OUT_DIR_PARENT_MISSING')
rc, so, se = run(W.main, argv + [str(d / 'out')])
ld, entries = ledger(out)
check('W2_step7_wrapper_valid_is_first_commit', rc == 0 and so == base_valid_stdout and entries == ['STEP7_0001.json'], (rc, so, se, entries))
check('W3_step7_out_equals_ledger_entry_bytes', (d / 'out' / 'STEP7_RESULT.json').read_bytes() == (ld / 'STEP7_0001.json').read_bytes())
out, d, argv = step7_setup('wrap_relative')
M6 = wrapper(mutate(b"    return _parent_problem(os.path.dirname(name) or '.')\n", b"    return _parent_problem(os.path.dirname(name))\n"), 'm6')
rc, so, se = run(M6.main, argv + ['rel_out'], cwd=str(d))
m6_killed = rc != 0 and not (d / 'rel_out').exists()
rc, so, se = run(W.main, argv + ['rel_out'], cwd=str(d))
check('W4_step7_wrapper_relative_out_dir_valid', rc == 0 and (d / 'rel_out' / 'STEP7_RESULT.json').is_file() and ledger(out)[1] == ['STEP7_0001.json'], (rc, so, se))
out, d, argv = step7_setup('wrap_symlink_parent')
(d / 'real_parent').mkdir(); os.symlink(d / 'real_parent', d / 'link_parent')
rc, so, se = run(W.main, argv + [str(d / 'link_parent' / 'out')])
check('W5_step7_wrapper_symlinked_parent_valid', rc == 0 and (d / 'real_parent' / 'out' / 'STEP7_RESULT.json').is_file(), (rc, so, se))
out, d, argv = step7_setup('m1')
M1 = wrapper(mutate(b"    if os.path.lexists(name):\n        if name != out_dir", b"    if False:\n        if name != out_dir"), 'm1')
rc, so, se = run(M1.main, argv + [condition(d, 'exists')])
m1_killed = ledger(out)[1] == ['STEP7_0001.json']
out, d, argv = step7_setup('m3')
M3 = wrapper(mutate(b"    if not os.access(parent, os.W_OK | os.X_OK):\n        return 'OUT_DIR_PARENT_NOT_WRITABLE'\n", b''), 'm3')
rc, so, se = run(M3.main, argv + [condition(d, 'parent_readonly')])
m3_killed = ledger(out)[1] == ['STEP7_0001.json']
# ---- 2b. raw-prefix semantics (Codex1 0295 B7-1): '..' after a symlink, a missing intermediate, trailing slashes
def dotdot_world(d):
    (d / 'actual' / 'deep').mkdir(parents=True); (d / 'lexical').mkdir()
    os.symlink(d / 'actual' / 'deep', d / 'lexical' / 'link')
    (d / 'actual' / 'only_actual').mkdir(); (d / 'lexical' / 'only_lexical').mkdir()
    (d / 'x').mkdir(); os.symlink(d / 'x' / 'no_dir' / 'target', d / 'dang')
    os.symlink(d / 'x' / 'made_target', d / 'dang_ok'); os.symlink('loop', d / 'loop')
    return str(d / 'lexical' / 'link') + '/../'
L_REFUSALS = (('L2_dotdot_after_symlink_lexical_only_parent', 'only_lexical/out', 'OUT_DIR_PARENT_MISSING'),
              ('L3_missing_intermediate_then_dotdot', None, 'OUT_DIR_PARENT_MISSING'),
              ('L5_dangling_symlink_trailing_slash_target_parent_missing', None, 'OUT_DIR_PARENT_MISSING'),
              ('L7_symlink_loop_with_trailing_slash', None, 'OUT_DIR_EXISTS'))
def l_path(d, pre, tag, rel):
    if tag.startswith('L2'):
        return pre + rel
    if tag.startswith('L3'):
        return str(d / 'nope') + '/../out'
    if tag.startswith('L7'):
        return str(d / 'loop') + '/'
    return str(d / 'dang') + '/'
out, d, argv = step7_setup('l1_dotdot_actual_parent')
pre = dotdot_world(d)
rc, so, se = run(W.main, argv + [pre + 'only_actual/out'])
check('L1_step7_dotdot_after_symlink_actual_parent_valid', rc == 0 and (d / 'actual' / 'only_actual' / 'out' / 'STEP7_RESULT.json').is_file() and ledger(out)[1] == ['STEP7_0001.json'], (rc, so, se))
for tag, rel, code in L_REFUSALS:
    out, d, argv = step7_setup('h_' + tag[:2])
    pre = dotdot_world(d)
    rc, so, se = run(RB.main, argv + [l_path(d, pre, tag, rel)])
    check('H_%s_base_commits_then_fails' % tag, rc != 0 and ledger(out)[1] == ['STEP7_0001.json'], (rc, se.strip()))
out, d, argv = step7_setup('l_wrap')
pre = dotdot_world(d)
for tag, rel, code in L_REFUSALS:
    od = l_path(d, pre, tag, rel); before = len(READS)
    rc, so, se = run(W.main, argv + [od]); reads = len(READS) - before
    check(tag + '_wrapper_refused_pre_commit', rc == 2 and so == '' and json.loads(se) == {'refused': code, 'detail': od} and ledger(out)[1] == [] and reads == 0, (rc, se.strip(), reads))
rc, so, se = run(W.main, argv + [str(d / 'tsl_out') + '/'])
check('L4_trailing_slash_valid_is_first_commit', rc == 0 and (d / 'tsl_out' / 'STEP7_RESULT.json').is_file() and ledger(out)[1] == ['STEP7_0001.json'], (rc, so, se))
out, d, argv = step7_setup('m8')
pre = dotdot_world(d)
M8 = wrapper(mutate(b"    return _parent_problem(os.path.dirname(name) or '.')\n", b"    return _parent_problem(os.path.dirname(os.path.abspath(name)))\n"), 'm8')
rc, so, se = run(M8.main, argv + [pre + 'only_lexical/out'])
m8_killed = ledger(out)[1] == ['STEP7_0001.json']
out, d, argv = step7_setup('m7')
pre = dotdot_world(d)
assert WRAP_RAW.count(b"    if os.path.lexists(name):\n") == 1
M7 = wrapper(mutate(b"    if os.path.lexists(name):\n", b"    if os.path.lexists(out_dir):\n"), 'm7')
rc, so, se = run(M7.main, argv + [str(d / 'dang') + '/'])
m7_killed = ledger(out)[1] == ['STEP7_0001.json']
out, d, argv = step7_setup('l6_dangling_ok')
pre = dotdot_world(d)
rc, so, se = run(W.main, argv + [str(d / 'dang_ok') + '/'])
check('L6_step7_dangling_link_trailing_slash_target_parent_exists_valid', rc == 0 and (d / 'x' / 'made_target' / 'STEP7_RESULT.json').is_file() and ledger(out)[1] == ['STEP7_0001.json'], (rc, so, se))
out, d, argv = step7_setup('m10')
pre = dotdot_world(d)
M10 = wrapper(mutate(b"        if name != out_dir and os.path.islink(name):\n", b"        if False:\n"), 'm10')
rc, so, se = run(M10.main, argv + [str(d / 'dang_ok') + '/'])
m10_killed = rc == 2 and ledger(out)[1] == []
out, d, argv = step7_setup('m9')
pre = dotdot_world(d)
M9 = wrapper(mutate(b"            if os.path.lexists(target):\n                return 'OUT_DIR_EXISTS'                 # the chain does not resolve (ELOOP)\n", b''), 'm9')
rc, so, se = run(M9.main, argv + [str(d / 'loop') + '/'])
m9_killed = ledger(out)[1] == ['STEP7_0001.json']
# K1: the wrapper's own preflight against the kernel's mkdir on 14 symlink/trailing-slash shapes
KM = Path(env.dir('c3p7_kernel_matrix'))
KCASES = {
 'dang_rel_parent_exists': lambda d: os.symlink('new_target', d + '/L'),
 'dang_rel_parent_missing': lambda d: os.symlink('x/no_dir/t', d + '/L'),
 'chain_dangling_end': lambda d: (os.symlink('L2', d + '/L'), os.symlink('newt', d + '/L2')),
 'loop_self': lambda d: os.symlink('L', d + '/L'),
 'loop_pair': lambda d: (os.symlink('L2', d + '/L'), os.symlink('L', d + '/L2')),
 'link_to_existing_dir': lambda d: (os.mkdir(d + '/real'), os.symlink('real', d + '/L')),
 'link_to_existing_file': lambda d: (t.wbytes(d + '/f', b''), os.symlink('f', d + '/L')),
 'dang_abs_readonly_root': lambda d: os.symlink('/nonexistent_c3p7_target', d + '/L'),
 'dang_dotdot_after_symlinked_dir': lambda d: (os.makedirs(d + '/a/deep'), os.mkdir(d + '/b'), os.symlink(d + '/a/deep', d + '/b/lk'), os.symlink('lk/../made', d + '/b/L')),
 'dang_target_with_trailing_slash': lambda d: os.symlink('new_target2/', d + '/L'),
 'dang_target_parent_is_dangling_link': lambda d: (os.symlink('nowhere', d + '/pl'), os.symlink('pl/t', d + '/L')),
 'dang_target_in_readonly_dir': lambda d: (os.mkdir(d + '/ro'), os.symlink('ro/t', d + '/L'), os.chmod(d + '/ro', 0o500), RO.append(Path(d + '/ro'))),
 'plain_missing_name_slash': lambda d: None,
 'regular_file_name_slash': lambda d: t.wbytes(d + '/L', b''),
}
matrix = {}
for k, setup in KCASES.items():
    kd = str(KM / k); os.mkdir(kd); setup(kd)
    od = kd + ('/b/L/' if k == 'dang_dotdot_after_symlinked_dir' else '/L/')
    em = W.preflight(od)
    try:
        os.mkdir(od); kern = 'OK'
    except OSError as e:
        kern = type(e).__name__ + '(%d)' % e.errno
    matrix[k] = (em, kern, (em is None) == (kern == 'OK'))
check('K1_preflight_equals_kernel_mkdir_on_14_shapes', len(matrix) == 14 and all(v[2] for v in matrix.values()), matrix)
# ---- 3. delegation of everything else is untouched; base pin
for name, argv in (('no_args', []), ('unknown', ['bogus']), ('step7_missing_out_dir', ['step7', '--input', 'x', '--input-sha256', 'y']),
                   ('custody_extra_key', ['custody', '--input', 'x', '--input-sha256', 'y', '--out-dir', 'z', '--extra', 'w'])):
    check('D1_delegated_identical_%s' % name, run(W.main, argv) == run(RB.main, argv))
WR = wrapper(seam=False, name='wr')
real = WR.load_base()
check('P1_real_loader_keeps_base_identity', real.own_pin() == {'path': BASE_PATH, 'sha256': BASE_SHA} and real.__file__ == BASE_PATH)
tampered = Path(env.dir('c3p7_pin')) / 'tampered_base.py'; t.wbytes(str(tampered), Path(BASE_PATH).read_bytes().replace(b'immutable review candidate', b'immutable review candidatX', 1))
WT = wrapper(seam=False, name='wt'); WT.BASE = {'path': str(tampered), 'sha256': BASE_SHA}
rc, so, se = run(WT.main, ['step7'])
check('P2_tampered_base_refused', rc == 2 and json.loads(se)['refused'] == 'BASE_PIN' and 'BASE_PIN_MISMATCH' in se, se)
link = Path(env.dir('c3p7_pin_link')) / 'base_link.py'; os.symlink(BASE_PATH, link)
WS = wrapper(seam=False, name='ws'); WS.BASE = {'path': str(link), 'sha256': BASE_SHA}
rc, so, se = run(WS.main, ['step7'])
check('P3_symlinked_base_refused', rc == 2 and json.loads(se)['refused'] == 'BASE_PIN', se)
# ---- 4. custody: builds first (results readable), then the breach
myroot = Path(os.path.realpath(env.dir('c3p7_custody_root'))); sub = myroot / 'copies'; sub.mkdir()
def custody_build(tag):
    N[0] += 1; tag = 'c3p7_cu_%02d_%s' % (N[0], tag)
    d = env.dir('cases', tag)
    ipin = world.b1.input(d, 'PHASE_1', 'FULL', world.p1_extra())
    doc = t.jload(ipin['path'])
    for item in doc['custody']['copies']:
        raw = Path(item['source']['path']).read_bytes(); h = hashlib.sha256(raw).hexdigest()
        dest = sub / (h + '.bin')
        if not dest.exists():
            t.wbytes(str(dest), raw)
        item['copy'] = {'path': str(dest), 'sha256': h}
    doc['custody']['root'] = str(myroot)
    out = env.fresh(tag); world.b1.build(jwrite(Path(d) / 'input_c3root.json', doc), out)
    bp = t.pin(os.path.join(out, 'BUILD_RECORD.json')); pp = t.pin(os.path.join(out, 'REPLAY_PLAN.json'))
    cd = Path(env.dir(tag + '_in'))
    inp = jwrite(cd / 'input.json', {'schema': 'CUSTODY_INPUT_C2V007', 'build_record': bp, 'replay_plan': pp})
    return out, cd, ['custody', '--input', inp['path'], '--input-sha256', inp['sha256'], '--out-dir']
cbase = {k: custody_build('base_' + k) for k in ('parent_missing', 'parent_file', 'parent_readonly')}
cvalid = custody_build('base_valid'); cwrap = custody_build('wrap'); cm4 = custody_build('m4'); cl1 = custody_build('l1'); cl6 = custody_build('l6')
plan = json.loads(Path(cwrap[0], 'REPLAY_PLAN.json').read_text())
target = sorted({e['result']['path'] for es in plan['replay_index'].values() for e in es if e.get('result')})[0]
os.chmod(target, 0); os.chmod(sub, 0)
try:
    for kind, (out, d, argv) in cbase.items():
        od = condition(d, kind)
        rc, so, se = run(RB.main, argv + [od])
        check('H2_custody_base_%s_commits_then_fails' % kind, rc != 0 and ledger(out)[1] == ['STEP7_0001.json'] and not os.path.exists(os.path.join(od, 'CUSTODY_RESULT.json')), (rc, se.strip(), ledger(out)[1]))
    out, d, argv = cvalid
    rc, so, se = run(RB.main, argv + [condition(d, 'exists')])
    check('H3_custody_base_existing_out_dir_already_pre_checked', rc == 2 and json.loads(se)['refused'] == 'OUT_DIR_EXISTS' and ledger(out)[1] == [], (rc, se))
    rc, custody_valid_stdout, se = run(RB.main, argv + [str(d / 'out')])
    check('V2_custody_base_valid', rc == 0 and json.loads(custody_valid_stdout) == {'status': 'NEW_UNEVALUATED', 'ledger_seq': 1}, (rc, custody_valid_stdout, se))
    out, d, argv = cwrap
    for kind in ('exists', 'parent_missing', 'parent_file', 'parent_readonly'):
        od = condition(d, kind); before = len(READS)
        rc, so, se = run(W.main, argv + [od]); reads = len(READS) - before
        check('W6_custody_wrapper_%s_refused_pre_commit' % kind, rc == 2 and so == '' and json.loads(se) == {'refused': WRAP_CODE[kind], 'detail': od} and ledger(out)[1] == [] and reads == 0, (rc, se.strip(), reads))
    pre = dotdot_world(d); od = pre + 'only_lexical/out'; before = len(READS)
    rc, so, se = run(W.main, argv + [od]); reads = len(READS) - before
    check('L2c_custody_dotdot_lexical_only_parent_refused_pre_commit', rc == 2 and json.loads(se) == {'refused': 'OUT_DIR_PARENT_MISSING', 'detail': od} and ledger(out)[1] == [] and reads == 0, (rc, se.strip(), reads))
    rc, so, se = run(W.main, argv + [str(d / 'out')])
    ld, entries = ledger(out)
    check('W7_custody_wrapper_valid_is_first_commit', rc == 0 and so == custody_valid_stdout and entries == ['STEP7_0001.json'] and sorted(os.listdir(d / 'out')) == ['CUSTODY_RESULT.json', 'REPLAY_PLAN.json'], (rc, so, se, entries))
    check('W8_custody_out_equals_ledger_bytes', (d / 'out' / 'CUSTODY_RESULT.json').read_bytes() == (ld / 'STEP7_0001.json').read_bytes())
    out, d, argv = cl1
    pre = dotdot_world(d)
    rc, so, se = run(W.main, argv + [pre + 'only_actual/out'])
    check('L1c_custody_dotdot_actual_parent_valid', rc == 0 and json.loads(so) == {'status': 'NEW_UNEVALUATED', 'ledger_seq': 1} and sorted(os.listdir(d / 'actual' / 'only_actual' / 'out')) == ['CUSTODY_RESULT.json', 'REPLAY_PLAN.json'], (rc, so, se))
    out, d, argv = cl6
    pre = dotdot_world(d)
    rc, so, se = run(W.main, argv + [str(d / 'dang_ok') + '/'])
    check('L6c_custody_dangling_link_trailing_slash_valid', rc == 0 and json.loads(so) == {'status': 'NEW_UNEVALUATED', 'ledger_seq': 1} and sorted(os.listdir(d / 'x' / 'made_target')) == ['CUSTODY_RESULT.json', 'REPLAY_PLAN.json'], (rc, so, se))
    out, d, argv = cm4
    M4 = wrapper(mutate(b"LEDGER_COMMANDS = ('step7', 'custody')", b"LEDGER_COMMANDS = ('step7',)"), 'm4')
    rc, so, se = run(M4.main, argv + [condition(d, 'parent_missing')])
    m4_killed = ledger(out)[1] == ['STEP7_0001.json']
finally:
    os.chmod(sub, 0o755); os.chmod(target, 0o644)
    for r in RO:
        os.chmod(r, 0o755)
mutants = {'M1_no_exists_check_commits': m1_killed, 'M2_no_isdir_check_code_changes': m2_killed, 'M3_no_access_check_commits': m3_killed,
           'M4_custody_not_covered_commits': m4_killed, 'M6_no_dot_default_refuses_relative_valid': m6_killed,
           'M7_exists_check_on_raw_trailing_slash_commits': m7_killed, 'M8_lexical_parent_restored_commits': m8_killed,
           'M9_no_unresolved_chain_check_commits_on_loop': m9_killed, 'M10_no_trailing_link_branch_refuses_valid': m10_killed}
check('all_mutants_killed', all(mutants.values()), mutants)
rec = {'schema': 'TEST_ROSTER_PARENT_CHECK_C3V007', 'wrapper': {'path': str(WRAP), 'sha256': hashlib.sha256(WRAP_RAW).hexdigest()},
       'base_sha256': BASE_SHA, 'fixture_sha256': hashlib.sha256(FIX_RAW).hexdigest(), 'python': sys.version.split()[0],
       'n': len(RESULTS), 'passed': sum(r['pass'] for r in RESULTS), 'results': RESULTS, 'mutants': mutants}
jwrite(WORK / 'TEST_RECORD.json', rec)
print(json.dumps({'n': rec['n'], 'passed': rec['passed'], 'failed': [r for r in RESULTS if not r['pass']], 'mutants': mutants}))
