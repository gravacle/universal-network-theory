"""Claude3 helper probes, cross-family review of Codex2 0848 unit 3 (seven-call direct Jacobian admission).

In-memory validation calls only. The REAL guard014 code runs (validate, core_priority_admission, spec_structure,
disk_admission, disk_output_volume, disk_free_bytes, safe_path, lexical_path, raw/sha/pin/verify/doc, source_map,
admitted_source, check_review), loaded exactly as launcher015/binder011 load it (exec of the pinned bytes).
Mocked: native_preflight (returns the L270 shape after the real spec_structure), the monitor/driver byte seam
(their bytes are not opened), and every filesystem call under /Volumes (an in-memory fake filesystem; the real
/Volumes is never stat'ed, listed or opened). No subprocess, network, launcher worker()/main() or scientific code.
Synthetic fixture documents are written only under argv[1] (scratch, exclusive create); results to argv[2].
Usage: python3 -I -B probe_seven_call_c3h001.py <scratch_fixture_dir_new> <result_json_new>
"""
import ast, copy, errno, fcntl, hashlib, json, os, stat, sys, types, datetime
from pathlib import Path

FIX = Path(sys.argv[1]); RESULT = Path(sys.argv[2])
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
GUARD = A + '/s1_successors_c2/step4_guard_c2v014.py'
LAUNCHER = A + '/s1_successors_c2/step4_launcher_c2v015.py'
BINDER = A + '/s1_successors_c2/step4_bind_c2v011.py'
OBJ = A + '/jacobian_seven_call_admission_cx2'
PLAN_T = OBJ + '/PLAN_TEMPLATE_CX2V001.json'
ADM_T = OBJ + '/ADMISSION_TEMPLATE_CX2V001.json'
DBP_D = A + '/h11_wall_ceiling_c3/C2V004D_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004D.json'
EXPECT = {
    GUARD: '6efdca016416a919b25a1e23d46a415b75fe2b5e60145ba098f864730975165d',
    LAUNCHER: 'cd987edd097323999847208d7b5fdfd93dadecb8a10beb6feaf91a0c53b68e0b',
    BINDER: 'd3d9702eb8096d11b98461f1c62c67931b9ecf74957cee95fbc3a60f60deaea0',
    PLAN_T: 'f7e9d389869f0360c6dddf7e8307072e8d421afd20a0ecd1228d0cbc07a43fac',
    ADM_T: '450861b8e2766bd5bac24c875864680a721cbe93990099b4394ffdc8b08ffdcb',
    DBP_D: '5d3f4bb84c35adee296048264ed306102ae51267f7da7ba2595cce561698f7a2',
}
FIX.mkdir(parents=False, exist_ok=False)
FIXS = str(FIX.resolve())
RESULTS = str(RESULT.parent.resolve())

# ---------------- safety layer ----------------
def _s(p):
    if isinstance(p, int): return None
    try: return os.fsdecode(p)
    except TypeError: return None
def is_vol(p):
    s = _s(p)
    if s is None or not s.startswith('/'): return False
    s = os.path.normpath(s)
    return s == '/Volumes' or s.startswith('/Volumes/')
def audit(event, args):
    if event in ('subprocess.Popen', 'os.system', 'os.fork', 'os.forkpty', 'os.posix_spawn', 'os.exec',
                 'socket.connect', 'socket.bind', 'os.kill', 'os.killpg'):
        raise RuntimeError('PROBE_PROCESS_OR_NETWORK_FORBIDDEN:' + event)
    if event in ('os.listdir', 'os.scandir') and args and is_vol(args[0]):
        raise RuntimeError('PROBE_VOLUMES_LIST_FORBIDDEN')
    if event == 'open':
        p, mode, flags = args
        if is_vol(p): raise RuntimeError('PROBE_VOLUMES_OPEN_FORBIDDEN:' + str(p))
        writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (
            isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        s = _s(p)
        if writing and s is not None:
            r = os.path.normpath(os.path.abspath(s))
            if not (r.startswith(FIXS + '/') or r == str(RESULT.resolve()) or r.startswith('/private/tmp/claude-501/')):
                raise RuntimeError('PROBE_WRITE_OUTSIDE_SCRATCH_FORBIDDEN:' + r)
    if event in ('os.mkdir', 'os.remove', 'os.rmdir', 'os.rename', 'os.link', 'os.symlink', 'os.truncate', 'os.chmod'):
        s = _s(args[0]) if args else None
        if s is None or is_vol(s) or not os.path.normpath(os.path.abspath(s)).startswith('/private/tmp/claude-501/'):
            raise RuntimeError('PROBE_FS_MUTATION_FORBIDDEN:' + event + ':' + str(s))
sys.addaudithook(audit)

FAKE = {}; INO = [100]; FREE = [0]
class FakeStat:
    def __init__(self, e):
        self.st_mode = {'dir': stat.S_IFDIR | 0o755, 'file': stat.S_IFREG | 0o644, 'link': stat.S_IFLNK | 0o777}[e['kind']]
        self.st_dev = e['dev']; self.st_ino = e['ino']; self.st_size = 0; self.st_nlink = 1
        self.st_uid = 501; self.st_gid = 20; self.st_mtime = 0; self.st_atime = 0; self.st_ctime = 0
def fs_add(path, kind, dev=2, target=None):
    INO[0] += 1; FAKE[os.path.normpath(path)] = {'kind': kind, 'dev': dev, 'ino': INO[0], 'target': target}
def fake_lookup(path, follow=True, depth=0):
    path = os.path.normpath(path); parts = path.split('/')[1:]; cur = ''
    for i, part in enumerate(parts):
        cur = cur + '/' + part; e = FAKE.get(cur); last = i == len(parts) - 1
        if e is None: raise FileNotFoundError(errno.ENOENT, 'FAKE_ENOENT', path)
        if e['kind'] == 'link' and (follow or not last):
            if depth > 40: raise OSError(errno.ELOOP, 'FAKE_ELOOP', path)
            t = e['target'] if e['target'].startswith('/') else os.path.normpath(os.path.dirname(cur) + '/' + e['target'])
            if not is_vol(t): raise RuntimeError('PROBE_FAKE_LINK_MUST_STAY_IN_VOLUMES')
            rest = '/'.join(parts[i + 1:])
            return fake_lookup(t + ('/' + rest if rest else ''), follow, depth + 1)
        if not last and e['kind'] != 'dir': raise NotADirectoryError(errno.ENOTDIR, 'FAKE_ENOTDIR', path)
    return e
REAL = {n: getattr(os, n) for n in ('stat', 'lstat', 'statvfs', 'readlink')}
def p_stat(p, *a, follow_symlinks=True, **k):
    if is_vol(p): return FakeStat(fake_lookup(_s(p), follow=follow_symlinks))
    return REAL['stat'](p, *a, follow_symlinks=follow_symlinks, **k)
def p_lstat(p, *a, **k):
    if is_vol(p): return FakeStat(fake_lookup(_s(p), follow=False))
    return REAL['lstat'](p, *a, **k)
def p_readlink(p, *a, **k):
    if is_vol(p):
        e = fake_lookup(_s(p), follow=False)
        if e['kind'] != 'link': raise OSError(errno.EINVAL, 'FAKE_EINVAL', _s(p))
        return e['target']
    return REAL['readlink'](p, *a, **k)
def p_statvfs(p):
    if is_vol(p):
        fake_lookup(_s(p))
        return types.SimpleNamespace(f_bavail=FREE[0], f_frsize=1)
    return REAL['statvfs'](p)
os.stat = p_stat; os.lstat = p_lstat; os.readlink = p_readlink; os.statvfs = p_statvfs

# ---------------- pinned inputs ----------------
RAW = {}
for p, h in EXPECT.items():
    b = open(p, 'rb').read(); RAW[p] = b
    assert hashlib.sha256(b).hexdigest() == h, ('PIN', p)
def canon(o): return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def sha(b): return hashlib.sha256(b).hexdigest()
PT = json.loads(RAW[PLAN_T]); AT = json.loads(RAW[ADM_T]); DBP = json.loads(RAW[DBP_D])

def load_guard():
    G = types.ModuleType('_probe_guard'); G.__file__ = GUARD
    exec(compile(RAW[GUARD], GUARD, 'exec'), G.__dict__)
    return G
SEAM = {}
def install_seams(G):
    real_verify = G.verify
    def seam_verify(ref):
        if isinstance(ref, dict) and set(ref) == {'path', 'sha256'} and ref['path'] in SEAM:
            G.require(SEAM[ref['path']] == ref['sha256'], 'PIN_BYTES_CHANGED')
            return b'DECLARED_SEAM_BYTES_NOT_READ'
        return real_verify(ref)
    G.verify = seam_verify
    def mock_native(cfg, call):
        spec = G.doc(call['spec']); G.spec_structure(call, spec)
        return native_shape(cfg, call, spec, G)
    G.native_preflight = mock_native
    return G
def native_shape(cfg, call, spec, G):
    return {'schema': 'UNT_STEP4_PRELAUNCH_CX1V001', 'case': call['case'], 'spec': call['spec'], 'driver': call['driver'],
            'config': cfg['config'], 'adoption_verdict': cfg['v007']['verdict'],
            'checks': {'SYNTHETIC_NATIVE_SEAM_ONLY': True, 'normalized_sha256': G.digest(spec)}, 'adoption_checked': True}

G = install_seams(load_guard())
MON = FIXS + '/SEAM_monitor_NOT_READ.py'; DRV = FIXS + '/SEAM_driver_r5_NOT_READ.py'
SEAM[MON] = G.MONITOR_SHA; SEAM[DRV] = G.R5_SHA
N = [0]
def put(name, obj):
    N[0] += 1; p = FIX / ('%03d_%s' % (N[0], name)); b = canon(obj) if not isinstance(obj, bytes) else obj
    with p.open('xb') as f: f.write(b)
    return {'path': str(p), 'sha256': sha(b)}

def fill(plan_t=PT, adm_t=AT, rename=None, regen_prelaunch=True, extra_calls=0):
    """Fill only Codex2's null/pending slots; every other template byte is kept."""
    plan = copy.deepcopy(plan_t); cfg = copy.deepcopy(adm_t)
    plan['binding_status'] = 'ROOT_BOUND'; plan['monitor'] = {'path': MON, 'sha256': plan_t['monitor']['sha256']}
    cfg['status'] = 'ROOT_AUTHORIZED'; cfg['sources'] = dict(cfg['sources']); cfg['sources'][MON] = G.MONITOR_SHA; cfg['sources'][DRV] = G.R5_SHA
    cfg['config'] = put('config_SYNTHETIC.json', {'SYNTHETIC_PROBE': 'config'})
    cfg['v007'] = dict(cfg['v007']); cfg['v007']['verdict'] = put('verdict_SYNTHETIC.json', {'SYNTHETIC_PROBE': 'verdict'})
    for i in range(extra_calls):
        c = copy.deepcopy(plan['calls'][-1]); c['case'] = 'EXTRA_PROBE_%d' % i
        d = os.path.dirname(c['outdir']) + '_EXTRA%d' % i
        c['outdir'] = d + '/out'; c['receipt'] = d + '/RECEIPT.json'; c['monitor_log'] = d + '/monitor.log'
        plan['calls'].append(c); cfg['case_order'].append(c['case']); cfg['caps'][c['case']] = dict(cfg['caps'][plan['calls'][0]['case']])
    cfg['calls'] = {}
    for c in plan['calls']:
        orig = c['case']
        c['driver'] = {'path': DRV, 'sha256': c['driver']['sha256']}
        spec = {'schema': 'SYNTHETIC_PROBE_SPEC_NOT_A_REAL_SPEC', 'galaxy': 'DDO154', 'admit': {}, 'physical': {'distance_Mpc': 4.04},
                'numerics': {'uv_tail': {'enabled': True}}, 'probe_case': orig}
        c['spec'] = put(orig + '.spec.json', spec); c['spec_status'] = 'ROOT_FINAL'; c['pending'] = []
        c['prelaunch'] = put(orig + '.prelaunch.json', native_shape(cfg, c, spec, G))
        if rename and orig in rename:
            new = rename[orig]; c['case'] = new
            if regen_prelaunch: c['prelaunch'] = put(new + '.prelaunch.json', native_shape(cfg, c, spec, G))
            cfg['case_order'] = [new if x == orig else x for x in cfg['case_order']]
            cfg['caps'][new] = cfg['caps'].pop(orig)
        cfg['calls'][c['case']] = {'spec': c['spec'], 'driver': c['driver'], 'prelaunch': c['prelaunch']}
    cfg['source_review'] = put('source_review_SYNTHETIC.json', {'schema': 'UNT_STEP4_SOURCE_REVIEW_CX1V001', 'status': 'TESTED', 'verdict': 'PASS',
        'approved_sources': cfg['sources'], 'blocking_findings': [], 'reviewer': 'Claude3-probe-SYNTHETIC'})
    return plan, cfg

ROOT = '/Volumes/External1/Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001'
def fs_base(plan, D_exists=True, ext_dev=2, root_exists=True):
    FAKE.clear()
    fs_add('/Volumes', 'dir', dev=1); fs_add('/Volumes/External1', 'dir', dev=ext_dev)
    fs_add('/Volumes/External1/Research', 'dir'); fs_add('/Volumes/External1/Research/UNT_STEP4_RUNS', 'dir')
    if root_exists: fs_add(ROOT, 'dir')
    if D_exists:
        for c in plan['calls']: fs_add(os.path.dirname(c['outdir']), 'dir')

def validate_guard(plan, cfg, **kw):
    b = canon(plan); ref = put('plan_SYNTHETIC.json', b); c = copy.deepcopy(cfg); c['plan'] = ref
    return G.validate(ref, LAUNCHER, _candidate_config=c, _plan_bytes=b, **kw)

results = []
def check(name, fn, expect='ACCEPT', label='TESTED', cite=''):
    try:
        v = fn(); obs = 'FALSE' if v is False else 'ACCEPT'
    except Exception as e:
        obs = (e.args[0] if type(e).__name__ == 'Refusal' and e.args else type(e).__name__ + ':' + str(e))
    results.append({'name': name, 'expected': expect, 'observed': obs, 'pass': obs == expect, 'label': label, 'cite': cite})

GiB = 1024 ** 3
# ---- A. template-filled admission through the real guard ----
plan, cfg = fill()
assert cfg.get('plan') is None and AT.get('plan') is None
fs_base(plan); FREE[0] = 580 * GiB
check('A1_template_filled_full_validate_7calls_HEADLINE_max6_real_paths_fakeFS_580GiB', lambda: validate_guard(plan, cfg), cite='guard014 L354-406')
FREE[0] = 580 * GiB - 1
check('A1b_same_free_580GiB_minus_1', lambda: validate_guard(plan, cfg), 'DISK_BATCH_BOUND', cite='guard014 L313-315')
FREE[0] = 580 * GiB

# binder-form validate (binder011 L33-38) using the binder's own guard instance
B = {'__file__': BINDER, '__name__': '_probe_binder'}
exec(compile(RAW[BINDER], BINDER, 'exec'), B)
install_seams(B['G'])
def binder_form():
    pb = canon(plan); inp = put('final_plan_SYNTHETIC.json', pb)
    c = json.loads(canon(cfg)); B['G'].require(c.get('plan') is None, 'BINDER_REQUIRES_UNBOUND_ADMISSION_CANDIDATE')
    probe = copy.deepcopy(c); probe['plan'] = inp
    return B['G'].validate(inp, plan['launcher']['path'], _candidate_config=probe, _plan_bytes=pb)
check('A2_binder011_validate_form_accepts_template_filled', binder_form, cite='binder011 L33-38')
argv = ['env', 'OPENBLAS_NUM_THREADS=1', 'OMP_NUM_THREADS=1', 'MKL_NUM_THREADS=1', 'VECLIB_MAXIMUM_THREADS=1', B['PYTHON'], '-I', '-B',
        plan['launcher']['path'], A + '/step4_launch_packet_cx1/jacobian_seven_call_root_binding_A1/PLAN_ROOT_BOUND.json', '--execute-root-only']
check('A2b_binder_check_command_on_binder_argv', lambda: B['check_command'](argv), cite='binder011 L26-30,L47')

# worker-form validate (launcher015 L58/L79/L96/L121) after six calls have started and written outputs
def worker_validate():
    fs_base(plan); fs_add(plan['launcher_log'], 'file')
    for c in plan['calls'][:6]:
        fs_add(c['monitor_log'], 'file'); fs_add(c['outdir'], 'dir')
    b = canon(plan); ref = put('plan_SYNTHETIC.json', b); c = copy.deepcopy(cfg); c['plan'] = ref
    return G.validate(ref, LAUNCHER, _candidate_config=c, _plan_bytes=b, check_outputs=False, disk_batch=False)
check('A3_worker_poll_validate_with_six_started_outputs_present', worker_validate, cite='launcher015 L96,L121; guard014 L403-405')
FREE[0] = 100 * GiB
check('A4_seventh_start_disk_exactly_100GiB', lambda: G.disk_admission(plan, plan['calls'][6]), cite='launcher015 L116,L122; guard014 L307-316')
FREE[0] = 100 * GiB - 1
check('A4b_seventh_start_disk_100GiB_minus_1', lambda: G.disk_admission(plan, plan['calls'][6]), 'DISK_START_BOUND', cite='guard014 L315')
FREE[0] = 580 * GiB
check('A5_batch_bound_value_is_622770257920', lambda: G.disk_admission(plan)['required_bytes'] == 622770257920 or False, cite='guard014 L313')
check('A5b_start_bound_value_is_107374182400', lambda: G.disk_admission(plan, plan['calls'][0])['required_bytes'] == 107374182400 or False, cite='guard014 L313')

# ---- B. refutation probes ----
fs_base(plan); FREE[0] = 580 * GiB
def mut(pm=None, cm=None, **fk):
    p, c = fill(**fk)
    if pm: pm(p)
    if cm: cm(c)
    fs_base(p)
    return p, c
def run_mut(pm=None, cm=None, **fk):
    p, c = mut(pm, cm, **fk); return validate_guard(p, c)
def set_max(v):
    return lambda d: d['route_a_admission'].__setitem__('max_active', v)
check('B1_max_active_7_in_plan_and_cfg', lambda: run_mut(set_max(7), set_max(7)), 'ROUTE_A_CAP_REQUIRED', cite='guard014 L373')
check('B2_plan6_cfg3_DBP_value', lambda: run_mut(None, set_max(3)), 'ROOT_RAMP_APPROVAL_REQUIRED', cite='guard014 L374')
check('B3_max_active_3_both_DBP_value_also_admits', lambda: run_mut(set_max(3), set_max(3)), cite='guard014 L373-374')
check('B4_case_name_outside_any_family_consistent', lambda: run_mut(rename={'JACOBIAN_R28': 'NOT_A_FAMILY_ZZZ_R28'}), cite='guard014 L378-394 (no case whitelist on tail-ON)')
check('B4b_S1_case_name_under_inactive_core_priority', lambda: run_mut(rename={'JACOBIAN_R29': 'S1_UA_C3T'}), cite='guard014 L333 (inactive dict returns before S1 rules)')
check('B5_case_renamed_after_prelaunch_produced', lambda: run_mut(rename={'JACOBIAN_R28': 'NOT_A_FAMILY_ZZZ_R28'}, regen_prelaunch=False), 'PRELAUNCH_REPLAY_MISMATCH', cite='guard014 L270,L396')
check('B6_cfg_case_order_is_DBP_HEADLINE11_order', lambda: run_mut(None, lambda c: c.__setitem__('case_order', list(DBP['batches']['HEADLINE']['case_order']))), 'ROOT_ORDER_BINDING', cite='guard014 L381')
check('B7_batch_label_DIII_tail_on_also_admits', lambda: run_mut(lambda p: p.__setitem__('batch', 'DIII')), cite='guard014 L378 (label only)')
check('B7b_batch_label_JACOBIAN_refused', lambda: run_mut(lambda p: p.__setitem__('batch', 'JACOBIAN')), 'BATCH_REQUIRED', cite='guard014 L378')
check('B8_campaign_live_S1_overlap_dict_batch_POST_S1_7calls', lambda: run_mut(lambda p: p.__setitem__('batch', 'POST_S1'), lambda c: c.__setitem__('core_priority', dict(G.CORE_PRIORITY_INACTIVE, campaign_inactive=False))), 'S1_OVERLAP_ADMISSION_REQUIRED', cite='guard014 L334-336')
check('B8b_campaign_live_batch_HEADLINE', lambda: run_mut(None, lambda c: c.__setitem__('core_priority', dict(G.CORE_PRIORITY_INACTIVE, campaign_inactive=False))), 'CORE_PRIORITY_ATTESTATION_REQUIRED', cite='guard014 L334')
def with_free(n, fn):
    old = FREE[0]; FREE[0] = n
    try: return fn()
    finally: FREE[0] = old
check('B9_eight_calls_consistent_at_580GiB_batch_bound_scales', lambda: run_mut(extra_calls=1), 'DISK_BATCH_BOUND', cite='guard014 L313 (8*80+20=660 GiB)')
check('B9a_eight_calls_consistent_660GiB_no_total_count_ceiling', lambda: with_free(660 * GiB, lambda: run_mut(extra_calls=1)), cite='guard014 L379-381,L313')
check('B9b_twelve_calls_consistent_980GiB_no_total_count_ceiling', lambda: with_free(980 * GiB, lambda: run_mut(extra_calls=5)), cite='guard014 L379-381,L313')
# filesystem variants (real disk_output_volume / safe_path / lexists against the fake /Volumes)
def fs_variant(setup, check_outputs=True):
    p, c = fill(); setup(p); FREE[0] = 580 * GiB
    b = canon(p); ref = put('plan_SYNTHETIC.json', b); c2 = copy.deepcopy(c); c2['plan'] = ref
    return G.validate(ref, LAUNCHER, _candidate_config=c2, _plan_bytes=b, check_outputs=check_outputs)
check('B10_D_absent_guard_still_admits', lambda: fs_variant(lambda p: fs_base(p, D_exists=False)), cite='guard014 L295-305,L403-404 (D not required by guard; launcher015 L127 needs it)')
check('B11_D_out_preexisting', lambda: fs_variant(lambda p: (fs_base(p), fs_add(p['calls'][3]['outdir'], 'dir'))), 'EXISTING_OUTPUT', cite='guard014 L404')
check('B11b_D_RECEIPT_launch_sidecar_preexisting', lambda: fs_variant(lambda p: (fs_base(p), fs_add(p['calls'][6]['receipt'] + '.launch.json', 'file'))), 'EXISTING_OUTPUT', cite='guard014 L398,L404')
check('B11c_launcher_log_preexisting', lambda: fs_variant(lambda p: (fs_base(p), fs_add(p['launcher_log'], 'file'))), 'EXISTING_OUTPUT', cite='guard014 L399,L404')
def symlink_D(p):
    fs_base(p); d = os.path.dirname(p['calls'][2]['outdir']); del FAKE[d]
    fs_add(ROOT + '/ELSEWHERE', 'dir'); fs_add(d, 'link', target=ROOT + '/ELSEWHERE')
check('B12_D_is_symlink_within_volume', lambda: fs_variant(symlink_D), 'OUTPUT_SYMLINK_REFUSED', cite='guard014 L300-304')
check('B13_output_root_missing', lambda: fs_variant(lambda p: fs_base(p, D_exists=False, root_exists=False)), 'OUTPUT_ROOT_MISSING', cite='guard014 L289')
check('B14_External1_not_a_mount', lambda: fs_variant(lambda p: fs_base(p, ext_dev=1)), 'DECLARED_OUTPUT_VOLUME_UNMOUNTED', cite='guard014 L292')
def other_dev(p):
    fs_base(p); d = os.path.dirname(p['calls'][5]['outdir']); FAKE[d]['dev'] = 3
check('B15_D_on_other_device', lambda: fs_variant(other_dev), 'WRONG_OUTPUT_VOLUME', cite='guard014 L303')
def launcher_log_in_D(p):
    p['launcher_log'] = os.path.dirname(p['calls'][0]['outdir']) + '/DDO154_JACOBIAN_BATCH_A1.launcher.log'; fs_base(p)
check('B16_launcher_log_inside_a_D_not_refused_by_guard', lambda: fs_variant(launcher_log_in_D), cite='guard014 L295-305,L400-402 (0841 placement is template-enforced only)')
def outside_root(p):
    p['calls'][1]['monitor_log'] = '/Volumes/External1/Research/OTHER_ROOT/monitor.log'; fs_base(p); fs_add('/Volumes/External1/Research/OTHER_ROOT', 'dir')
check('B17_output_outside_OUTPUT_ROOT', lambda: fs_variant(outside_root), 'OUTPUT_OUTSIDE_DECLARED_ROOT', cite='guard014 L299')
check('B18_template_unfilled_as_published', lambda: (fs_base(PT), validate_guard(PT, AT)), 'ROOT_PLAN_BINDING_REQUIRED', cite='guard014 L361 (status PENDING_ROOT_AUTHORIZATION)')

# ---- C. launcher015 pieces (AST-extracted functions only; worker()/main() are NOT executed) ----
tree = ast.parse(RAW[LAUNCHER])
def defs(names, ns):
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), LAUNCHER, 'exec'), ns)
LOCKFILE = FIX / 'PROBE_ONLY_LOCK_NOT_THE_MACHINE_LOCK'
L = {'G': types.SimpleNamespace(require=G.require, Refusal=G.Refusal, safe_path=G.safe_path, decode=G.decode),
     'LOCK': LOCKFILE, 'os': os, 'fcntl': fcntl, 'Path': Path}
defs(['acquire_lock', 'decision', 'first_iteration', 'route_a_finished', 'read_progress'], L)
fd1 = L['acquire_lock']()
check('C1_real_flock_second_description_refused', L['acquire_lock'], 'ANOTHER_STEP4_BATCH_ACTIVE', cite='launcher015 L48-55')
fd2 = os.dup(fd1); os.close(fd1)
check('C1b_dup_shares_description_lock_survives_original_close', L['acquire_lock'], 'ANOTHER_STEP4_BATCH_ACTIVE', cite='launcher015 L128 pass_fds analog (FORMAL for cross-process)')
os.close(fd2)
def reacquire():
    fd = L['acquire_lock'](); os.close(fd); return True
check('C1c_lock_free_after_last_descriptor_closed', reacquire, cite='launcher015 L48-55,L147-148')
check('C1d_lock_inode_never_truncated', lambda: LOCKFILE.stat().st_size == 0 or False, cite='launcher015 L49-52')

# scheduling replay: a literal transcription of launcher015 L98-L133 bookkeeping, using the REAL decision,
# route_a_finished and first_iteration predicates on the template's own outdir paths (progress kept in memory).
PROG = {}
L['read_progress'] = lambda path: list(PROG.get(str(path), []))
def replay(first_iter_after, route_a_after, total_after, max_active=6):
    """Polls are integers. Call k: first iteration completes first_iter_after[k] polls after start; route A finishes
    route_a_after[k] polls after start; the monitor exits total_after[k] polls after start."""
    PROG.clear(); calls = plan['calls']; pending = list(calls); active = []; previous = None; starts = {}; t = 0; log = []
    maxA = 0; maxLive = 0
    while (pending or active) and t < 10000:
        t += 1
        for item in list(active):
            c = item['call']; k = calls.index(c); age = t - item['t0']
            if age >= first_iter_after[k]: PROG[c['outdir'] + '/stages/01_route_a/attempt_000/progress.jsonl'] = [{'stage': 'iteration_completed', 'iteration': 0}]
            if age >= route_a_after[k]: PROG[c['outdir'] + '/progress.jsonl'] = [{'stage': 'route_a', 'event': 'finished'}]
        for item in list(active):
            c = item['call']; k = calls.index(c)
            item['route_a_finished'] = L['route_a_finished'](Path(c['outdir']) / 'progress.jsonl')
            if t - item['t0'] < total_after[k]: continue
            item['terminal'] = True; active.remove(item)
        if pending:
            prev_ok = previous is None or L['first_iteration'](Path(previous['call']['outdir']) / 'stages/01_route_a/attempt_000/progress.jsonl')
            count = sum(not item['route_a_finished'] for item in active)
            go = L['decision'](active_route_a=count, previous_iteration=prev_ok, first=previous is None, max_active=max_active)
            if previous is not None and previous.get('terminal') and not prev_ok: return {'refused': 'PREDECESSOR_ENDED_BEFORE_FIRST_ITERATION', 't': t}
            if go:
                c = pending.pop(0); item = {'call': c, 't0': t, 'route_a_finished': False, 'terminal': False}
                active.append(item); previous = item; starts[c['case']] = t
                log.append({'t': t, 'start': c['case'], 'active_route_a_before': count})
        maxA = max(maxA, sum(not i['route_a_finished'] for i in active)); maxLive = max(maxLive, len(active))
    return {'starts': starts, 'max_route_a_active': maxA, 'max_live_monitors': maxLive, 'log': log}
# S1: fast first iterations (2 polls), long route A (100 polls for call 1, 400 for the others), route B 300 more
S1 = replay([2] * 7, [100] + [400] * 6, [400] + [700] * 6)
check('C2_S1_seventh_waits_for_first_routeA_exit', lambda: bool(S1.get('starts', {}).get('JACOBIAN_R302') == S1.get('starts', {}).get('JACOBIAN_R28', -999) + 100 and S1.get('max_route_a_active') == 6),
      cite='launcher015 L113-L133 (transcribed), L32-33 real decision')
check('C2b_S1_route_B_monitors_do_not_count', lambda: bool(S1.get('max_live_monitors') == 7), cite='launcher015 L115')
# S2: call 1 leaves route A at 3 polls, but call 6's first iteration takes 50 polls -> call 7 waits for call 6
S2 = replay([2, 2, 2, 2, 2, 50, 2], [3] + [400] * 6, [5] + [700] * 6)
check('C2c_S2_seventh_waits_for_predecessor_first_iteration', lambda: bool(S2.get('starts', {}).get('JACOBIAN_R302') == S2.get('starts', {}).get('JACOBIAN_R301', -999) + 50), cite='launcher015 L114,L117')
S3 = replay([2] * 7, [400] * 7, [700] * 7, max_active=7)
check('C2d_S3_hypothetical_max7_would_start_all_seven_without_waiting', lambda: bool(S3.get('max_route_a_active') == 7), cite='contrast: guard014 L373 forbids 7')
# S4: call 6 (R301) ends before its first iteration -> launcher015 L119 refusal -> drain: call 7 never starts
S4 = replay([2, 2, 2, 2, 2, 50, 2], [400] * 7, [700, 700, 700, 700, 700, 4, 700])
check('C2e_S4_predecessor_ends_before_first_iteration_seventh_never_starts', lambda: bool(S4.get('refused') == 'PREDECESSOR_ENDED_BEFORE_FIRST_ITERATION'), cite='launcher015 L119,L134-135 (drain clears pending)')

for p, h in EXPECT.items():
    assert hashlib.sha256(open(p, 'rb').read()).hexdigest() == h, ('PIN_CHANGED', p)
out = {'schema': 'C3_SEVEN_CALL_PROBES_C3H001', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'python': sys.version, 'pins_before_after': EXPECT, 'fixture_dir_scratch': FIXS,
       'mocked': ['native_preflight (L270 shape after real spec_structure)', 'monitor/driver byte seam', 'all /Volumes fs calls (in-memory fake)'],
       'real': ['guard014 validate and everything it calls except native_preflight', 'binder011 module (own guard instance) validate form + check_command',
                'launcher015 acquire_lock on a scratch lock file (real flock)', 'launcher015 decision/first_iteration/route_a_finished'],
       'not_executed': ['launcher015 worker()/main()', 'binder011 bind() writes', 'any subprocess or scientific code'],
       'replays': {'S1': S1, 'S2': S2, 'S3': {k: S3[k] for k in ('starts', 'max_route_a_active', 'max_live_monitors')}, 'S4': S4},
       'passed': sum(r['pass'] for r in results), 'total': len(results), 'results': results}
with RESULT.open('xb') as f: f.write(json.dumps(out, indent=1, sort_keys=True).encode() + b'\n')
print(json.dumps({'passed': out['passed'], 'total': out['total'], 'failed': [r for r in results if not r['pass']]}, indent=1))
