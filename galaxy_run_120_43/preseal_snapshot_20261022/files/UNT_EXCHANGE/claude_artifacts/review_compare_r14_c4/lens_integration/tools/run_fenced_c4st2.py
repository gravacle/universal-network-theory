# Claude4 seal tools v002: run SCRIPT as __main__ inside the fence tools/fence_c4v002.py (sha pinned below), installed first.
# Before the script runs: (1) the fence's own 8-class selftest must pass 8/8; (2) the v002 exception probes must all behave:
# the three allowed reads (a real uvt_*.py source outside runs_ext, the open V005 and the frozen V004 root decision files) read,
# and every refused probe raises the fence's PermissionError. Refused probes are evaluated by calling the fence policy on the
# path (no file is opened for them). The fence's BLOCKED list after the selftests is printed to stderr at the end, as JSON.
# usage: python3 -I -B run_fenced_c4st2.py SCRIPT [ARGS...]
import hashlib, importlib.util, json, os, runpy, sys
from pathlib import Path

FENCE = Path(__file__).resolve().parent / 'fence_c4v002.py'
FENCE_SHA = 'c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5'
if hashlib.sha256(FENCE.read_bytes()).hexdigest() != FENCE_SHA:
    sys.stderr.write('REFUSED: the fence is not fence_c4v002 c993d34c\n')
    raise SystemExit(3)
spec = importlib.util.spec_from_file_location('fence_c4v002', str(FENCE))
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)
st = F.selftest()
if not all(ok for _, ok in st):
    sys.stderr.write('REFUSED: fence selftest failed %r\n' % (st,))
    raise SystemExit(3)

C2 = F.CTRL_C2
ALLOWED = [
    ('a_uvt_source_outside_runs_ext', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/'
                                      'tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001_r5.py'),
    ('b_open_V005_addendum', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'),
    ('b_frozen_V004_addendum', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md'),
]
REFUSED_READ = [
    ('uvt_py_under_runs_ext', F.RUNS_EXT[1] + '/uvt_probe_should_not_exist.py'),
    ('uvt_py_in_a_UVT_dir', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/UVT_probe_should_not_exist/uvt_probe.py'),
    ('uvt_pyc_not_a_source', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/__pycache__/uvt_probe_should_not_exist.cpython-312.pyc'),
    ('UVT_uppercase_basename', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/UVT_probe_should_not_exist.py'),
    ('uvt_json_not_py', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/uvt_probe_should_not_exist.json'),
    ('ngc3198_data_in_CLAUDE2', C2 + '/NGC3198_probe_should_not_exist.json'),
    ('addendum_name_other_folder', '/Users/bgm/Research/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'),
    ('addendum_name_not_md', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.json'),
    ('addendum_glob_with_target_word', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_rotmod_ADDENDUM.md'),
    ('addendum_other_series', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V010_ADDENDUM.md'),
]
REFUSED_WRITE = [
    ('write_open_V005_addendum', C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'),
    ('write_uvt_source', ALLOWED[0][1]),
]
probes = []
for name, p in ALLOWED:
    try:
        with open(p, 'rb') as f:
            n = len(f.read(64))
        probes.append({'probe': name, 'expect': 'READ', 'ok': n > 0})
    except PermissionError as e:
        probes.append({'probe': name, 'expect': 'READ', 'ok': False, 'error': str(e)[:160]})
for name, p in REFUSED_READ:
    try:
        F._hook('open', (p, 'rb', os.O_RDONLY))
        probes.append({'probe': name, 'expect': 'REFUSED', 'ok': False})
    except PermissionError as e:
        probes.append({'probe': name, 'expect': 'REFUSED', 'ok': str(e).startswith('FENCE_C4')})
for name, p in REFUSED_WRITE:
    try:
        F._hook('open', (p, 'a', os.O_WRONLY | os.O_APPEND | os.O_CREAT))
        probes.append({'probe': name, 'expect': 'REFUSED', 'ok': False})
    except PermissionError as e:
        probes.append({'probe': name, 'expect': 'REFUSED', 'ok': str(e).startswith('FENCE_C4')})
if not all(x['ok'] for x in probes):
    sys.stderr.write('REFUSED: fence v002 exception probes failed %s\n' % json.dumps(probes))
    raise SystemExit(3)
n_self = len(F.BLOCKED)
script = sys.argv[1]
sys.argv = [script] + sys.argv[2:]
rc = 0
try:
    runpy.run_path(script, run_name='__main__')
except SystemExit as e:
    rc = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
sys.stderr.write('\nFENCE_C4ST2_SUMMARY ' + json.dumps({'fence_sha256': FENCE_SHA, 'review_root': F.REVIEW,
                 'selftest_pass': sum(1 for _, ok in st if ok), 'selftest_of': len(st),
                 'v002_exception_probes_pass': sum(1 for x in probes if x['ok']), 'v002_exception_probes_of': len(probes),
                 'blocked_during_selftests': len(F.BLOCKED[:n_self]),
                 'blocked_after_selftest': F.BLOCKED[n_self:]}) + '\n')
raise SystemExit(rc)
