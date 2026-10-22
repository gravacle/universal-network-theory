# Claude4 helper (seal tools v002 check): run a script under tools/fence_c4v002.py (this folder's own v002 fence).
# 1. the fence file must hash to FENCE_SHA; 2. import it (the audit hook is installed and cannot be removed);
# 3. selftest() must give 8/8; 4. the v002 exception probes call the hook directly (no file is opened by a probe), plus one
# real read of the open V005 addendum; 5. runpy the target with its argv; 6. print FENCE_C4CHK_SUMMARY with the BLOCKED list
# of the run itself (entries after the selftests and probes) to stderr.
# usage: python3 -I -B run_fenced_c4chk.py SCRIPT [args...]
import hashlib, os, sys, json, runpy, atexit
HERE = os.path.dirname(os.path.realpath(__file__))
FENCE = os.path.join(HERE, 'fence_c4v002.py')
FENCE_SHA = '3d9d69257145dfe20a0c33b93d3632bdbb8ac75b9ac960311464d993c89c0e69'
got = hashlib.sha256(open(FENCE, 'rb').read()).hexdigest()
if got != FENCE_SHA:
    print('FENCE_SHA_MISMATCH', got, file=sys.stderr); sys.exit(3)
sys.path.insert(0, HERE)
import fence_c4v002 as F
st = F.selftest()
if not all(ok for _, ok in st) or len(st) != 8:
    print('FENCE_SELFTEST_FAILED', st, file=sys.stderr); sys.exit(3)
CTRL = F.CTRL_C2
ADD = CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
RX = F.RUNS_EXT[1]
PROBES = [  # (name, event args, expect_allowed)
    ('read_open_V005_addendum', (ADD, 'rb', 0), True),
    ('read_V004_addendum', (CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md', 'rb', 0), True),
    ('read_future_frozen_name', (CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', 'rb', 0), True),
    ('read_uvt_source_module', ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/x_probe/uvt_probe_module.py', 'rb', 0), True),
    ('write_open_V005_addendum', (ADD, 'a', os.O_WRONLY | os.O_APPEND), False),
    ('create_addendum_named_file', (CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V009_ADDENDUM.md', 'x', os.O_WRONLY | os.O_CREAT | os.O_EXCL), False),
    ('read_V001_decisions_not_addendum', (CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001.md', 'rb', 0), False),
    ('read_addendum_name_in_other_folder', ('/Users/bgm/Research/UNT_EXCHANGE/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md', 'rb', 0), False),
    ('read_addendum_name_in_CLAUDE2_subdir', (CTRL + '/sub/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md', 'rb', 0), False),
    ('read_addendum_with_target_word', (CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_rotmod.md', 'rb', 0), False),
    ('read_ngc3198_data_in_CLAUDE2', (CTRL + '/NGC3198_TABLE.json', 'rb', 0), False),
    ('read_uvt_pyc', ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/x_probe/__pycache__/uvt_probe_module.cpython-312.pyc', 'rb', 0), False),
    ('read_uppercase_UVT_py', ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/x_probe/UVT_probe_module.py', 'rb', 0), False),
    ('read_uvt_py_in_UVT_dir', ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/UVT_X_RUN/uvt_probe_module.py', 'rb', 0), False),
    ('read_uvt_py_in_uvt_dir', ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/uvt_dir/uvt_probe_module.py', 'rb', 0), False),
    ('read_uvt_py_under_runs_ext', (RX + '/x/uvt_probe_module.py', 'rb', 0), False),
    ('read_uvt_py_under_runs_ext_external', (F.RUNS_EXT[0] + '/x/uvt_probe_module.py', 'rb', 0), False),
    ('read_uvt_py_c5h_name', ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/KMAX_A2F10_C5H_RUN_V001/uvt_probe_module.py', 'rb', 0), False),
    ('read_uvt_json', ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/x_probe/uvt_probe.json', 'rb', 0), False),
    ('write_uvt_source_module', ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/x_probe/uvt_probe_module.py', 'w', os.O_WRONLY | os.O_CREAT), False),
    ('read_runs_ext_addendum_name', (RX + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md', 'rb', 0), False),
]
res = []
for name, args, want in PROBES:
    try:
        F._hook('open', args)
        allowed = True
    except PermissionError as e:
        allowed = False
    res.append((name, allowed == want))
real_read = False
try:
    with open(ADD, 'rb') as f:
        real_read = len(f.read(64)) > 0
except Exception as e:
    real_read = False
n0 = len(F.BLOCKED)
probes_ok = all(ok for _, ok in res) and real_read


def _summary():
    print('FENCE_C4CHK_SUMMARY ' + json.dumps({'fence_sha256': got, 'review_root': F.REVIEW, 'selftest': '%d/%d' % (sum(ok for _, ok in st), len(st)),
                                              'probes': '%d/%d' % (sum(ok for _, ok in res), len(res)), 'probe_failures': [n for n, ok in res if not ok],
                                              'real_addendum_read': real_read, 'blocked_during_run': F.BLOCKED[n0:]}), file=sys.stderr)


if not probes_ok:
    _summary(); sys.exit(3)
atexit.register(_summary)
if len(sys.argv) < 2:
    print('usage: run_fenced_c4chk.py SCRIPT [args...]', file=sys.stderr); sys.exit(3)
script = os.path.realpath(sys.argv[1])
sys.argv = [script] + sys.argv[2:]
sys.path.insert(0, os.path.dirname(script))
runpy.run_path(script, run_name='__main__')
