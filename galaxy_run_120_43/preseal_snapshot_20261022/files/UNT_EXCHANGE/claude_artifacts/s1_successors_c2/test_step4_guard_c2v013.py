"""Synthetic MUST_PASS / MUST_FAIL tests for step4_guard_c2v013.py and step4_launcher_c2v014.py (s1_successors_c2).

  python3 -I -B test_step4_guard_c2v013.py --run-dir <a new directory>

Port of test_step4_guard_c2v012.py (a652e1d3) for V006 A166. Target-free; launches nothing. guard013, guard012 and
guard011 are executed from their bytes (guard012/guard011 sha-pinned); every admission is synthetic (synthetic seal,
verdict, prereg, adoption policy, context and direct-context modules, a synthetic S1 replay module). Machine gate
v003 is loaded (pinned) only to drive guard012 in the comparison tests (synthetic probe and clock); guard013 has no
gate. launcher014 / launcher013 are executed as modules (their import loads their guard; main() is never called).
Per A166 the synthetic POST_S1 caps carry rss_cap_bytes = physical RAM (137438953472 B).
Results: <run-dir>/TEST_RESULTS.json and <run-dir>/TEST_LOG.txt (exclusive create).
"""
import argparse
import ast
import copy
import difflib
import hashlib
import json
import os
import sys
import time
import traceback
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
SUCC = ART + '/s1_successors_c2'
G11_PATH = ART + '/step4_launch_packet_cx1/impl/step4_guard_c2v011.py'
G11_SHA = 'eb97e303b968dc941e2059ada813be95340662253c327a7b9a9634bb8a2c8033'
L12_PATH = ART + '/step4_launch_packet_cx1/impl/step4_launcher_c2v012.py'
L12_SHA = '59c00707ea8f3dc42fb2349bd806d42758119354954f878299d56bd21933f2a9'
G12_PATH = SUCC + '/step4_guard_c2v012.py'
G12_SHA = 'f4656fecc863acf1df1d440f7eb44295dd1a43a8aa4955c18f8e50f57862eeb0'
L13_PATH = SUCC + '/step4_launcher_c2v013.py'
L13_SHA = '620a44da8c68af5175195653da5eaa4d3e4025b2c8029ea841def2332ebb1c58'
G13_PATH = str(HERE / 'step4_guard_c2v013.py')
L14_PATH = str(HERE / 'step4_launcher_c2v014.py')
MONITOR = (ART + '/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py', 'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107')
DRIVER = (ART + '/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py', 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6')
CORE = (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py', 'dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6')
GATE = (ART + '/sched_s45_c2/v003/machine_gate_s45_c2v003.py', '736a3438b0a3af41eb8d7b2c764f25ff0f9e18942320a4542a9893b6b419f811')
CFG = (ART + '/sched_s45_c2/v003/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V003.json', 'd9241676c3b7b32bd3067a55bdfb7821ebc33a68adbdc011ab4e4c58b6e50a4d')
DBP = (ART + '/sched_s45_c2/v003/DIRECT_BATCH_PARAMS_S45_C2V003A.json', '4adc296bcb0ddcd154ec0dcea820908ac525d1d39ce00d633eecc4d0c95f87e7')
P5 = (ART + '/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json', 'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174')
RAM_BYTES = 137438953472          # V006 A166: per-call RSS cap = physical RAM

RUN = None
RESULTS, LOG, TESTS = [], [], []
G11 = G12 = G13 = GM = None
FX = None
AUDIT = {'on': False, 'events': [], 'installed': False}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rb(p):
    with open(p, 'rb') as f:
        return f.read()


def rb_pinned(path, expect):
    raw = rb(path)
    assert sha(raw) == expect, (path, sha(raw))
    return raw


def load_bytes_module(path, expect, name):
    raw = rb(path)
    assert sha(raw) == expect, (path, sha(raw))
    m = types.ModuleType(name)
    m.__file__ = path
    exec(compile(raw, path, 'exec'), m.__dict__)
    return m


def wx(path, data):
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)
    return {'path': str(path), 'sha256': sha(data)}


def wj(path, obj, indent=1):
    return wx(path, (json.dumps(obj, indent=indent, sort_keys=True, allow_nan=False) + '\n').encode())


def test(tid, kind):
    def deco(fn):
        fn._tid, fn._kind = tid, kind
        TESTS.append(fn)
        return fn
    return deco


def record(tid, kind, ok, detail):
    RESULTS.append({'id': tid, 'kind': kind, 'result': 'PASS' if ok else 'FAIL', 'detail': detail})
    LOG.append('%-5s %-9s %s  %s' % ('ok' if ok else 'FAIL', kind, tid, str(detail)[:300]))


def code_of(exc):
    return str(exc.args[0]) if getattr(exc, 'args', None) else type(exc).__name__


# ================================================================================================ synthetic modules
CONTEXT_SRC = '''import ast, hashlib
CORE_PATH = %r
CORE_SHA = %r
with open(CORE_PATH, 'rb') as _f:
    _raw = _f.read()
if hashlib.sha256(_raw).hexdigest() != CORE_SHA:
    raise ValueError('core pin')
_keep = [n for n in ast.parse(_raw).body if (isinstance(n, ast.FunctionDef) and n.name == 'validate_block')
         or (isinstance(n, ast.Assign) and any(getattr(t, 'id', None) == 'HULL' for t in n.targets))]
class Error(Exception):
    pass
_ns = {'Error': Error}
exec(compile(ast.Module(body=_keep, type_ignores=[]), '<g13-test-core-validate_block>', 'exec'), _ns)
validate_block = _ns['validate_block']
O = object()
'''
DIRECT_SRC = '''import json
DIRECT_CONTEXT_API = 'UNT_STEP4_DIRECT_PREFLIGHT_CX1V001'
class _Ctx:
    def __init__(self, C, config):
        self.C, self.config = C, config
    def certificate_policy_gate(self):
        return {'ok': True, 'reasons': []}
    def certificate_check(self, spec, phase):
        self.C.validate_block(spec['numerics'])
        u = spec['numerics']['uv_tail']
        b = ['CERTIFICATE_SLOT_NOT_A_PIN:' + k for k in ('eps_certificate', 'lo_certificate') if not isinstance(u.get(k), dict)]
        return {'ok': not b, 'blockers': b}
    def sensitivity_gate(self, spec):
        return {'ok': True, 'reasons': []}
    def prelaunch_check(self, spec):
        self.C.validate_block(spec['numerics'])
        return json.loads(json.dumps(spec))
def build(C, config, guard=None, admission=None):
    return _Ctx(C, config)
'''
POLICY_SRC = '''APPROVED_V007_SEALS = %s
def check_numerics(ncfg, block, n, O=None, validate_block=None, driver_sha=None, synthetic=False):
    validate_block(block)
    return None, {'ok': True, 'reasons': []}
'''
REPLAY_SRC = '''import hashlib, json
S1_REPLAY_API = %r
def guard_replay(ref):
    with open(ref['path'], 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != ref['sha256']:
        raise ValueError('fill record pin')
    d = json.loads(raw)
    if d.get('refuse'):
        raise ValueError('synthetic replay refusal')
    out = {}
    for c, e in d['cases'].items():
        with open(e['spec']['path'], 'rb') as f:
            b = f.read()
        out[c] = {'spec': e['spec'], 'bytes': b + (b' ' if d.get('tamper') else b'')}
    return {'cases': out}
'''


# ================================================================================================ fixtures
class Fx:
    pass


def pinj(t):
    return {'path': t[0], 'sha256': t[1]}


def base_spec(label, certs):
    p5 = json.loads(rb_pinned(*P5))
    num = copy.deepcopy(json.loads(rb_pinned(*CFG))['numerics']['block'])
    num['uv_tail']['eps_certificate'], num['uv_tail']['lo_certificate'] = certs
    ph = copy.deepcopy(p5['anchor']['physical'])
    ph['inclination_deg'] = 66.0
    return {'schema': 'UNT_GALAXY_M0_FORWARD_CALL_C2V001', 'galaxy': 'DDO154', 'admit': {},
            'coefficients': p5['anchor']['coefficients'], 'physical': ph, 'numerics': num,
            'reference_compare': False, 'label': label}


def build_fixtures():
    fx = Fx()
    fx.root = RUN / 'fx'
    os.mkdir(fx.root)
    g = fx.root
    certs = (wj(g / 'cert_eps.json', {'schema': 'SYNTHETIC'}), wj(g / 'cert_lo.json', {'schema': 'SYNTHETIC_LO'}))
    fx.spec_c4t = wj(g / 'S1_UA_C4T_syn.spec.json', base_spec('S1 transfer test C4T at u_A theta %s; base %s'
                                                              % ('a' * 16, 'b' * 8), certs))
    fx.spec_c3t_like = wj(g / 'S1_UA_C3T_syn_k4grid.spec.json',
                          base_spec('S1 transfer test C3T at u_A theta %s; base %s' % ('a' * 16, 'b' * 8), certs))
    fx.spec_head = wj(g / 'HEADLINE_syn.spec.json', base_spec('DDO154 headline synthetic', certs))
    fx.fill = wj(g / 'S1_FILL_RECORD_syn.json', {'schema': 'SYNTHETIC_FILL', 'cases': {'S1_UA_C4T': {'spec': fx.spec_c4t},
                                                                                       'S1_UA_C3T': {'spec': fx.spec_c3t_like}}})
    fx.fill_tamper = wj(g / 'S1_FILL_RECORD_syn_tamper.json', {'schema': 'SYNTHETIC_FILL', 'tamper': True,
                                                               'cases': {'S1_UA_C4T': {'spec': fx.spec_c4t}}})
    fx.fill_refuse = wj(g / 'S1_FILL_RECORD_syn_refuse.json', {'schema': 'SYNTHETIC_FILL', 'refuse': True, 'cases': {}})
    fx.fill_other = wj(g / 'S1_FILL_RECORD_syn_other.json', {'schema': 'SYNTHETIC_FILL',
                                                             'cases': {'S1_UA_C4T': {'spec': fx.spec_head}}})
    fx.replay = wx(g / 'syn_replay.py', (REPLAY_SRC % 'UNT_S1_FILL_REPLAY_C2V002').encode())
    fx.replay_bad_api = wx(g / 'syn_replay_bad_api.py', (REPLAY_SRC % 'SOMETHING_ELSE').encode())
    v = {}
    v['compare'] = wx(g / 'compare_dummy.txt', b'synthetic compare bytes\n')
    v['addendum'] = wx(g / 'addendum_dummy.md', b'synthetic frozen addendum\n')
    v['case_block'] = wx(g / 'case_block_dummy.json', b'{"synthetic": true}\n')
    v['prereg'] = wj(g / 'prereg.json', {'binding_inputs': {'case_block': v['case_block']}})
    v['seal'] = wj(g / 'seal.json', {'sealed_by': G13.AUTHORITY, 'prereg': v['prereg'], 'compare': v['compare'],
                                     'driver': {'sha256': DRIVER[1]}, 'frozen_addendum': v['addendum']})
    vd = {'schema': 'SYN_VERDICT_SCHEMA', 'test_mode': False, 'decision': {'tests_read': True, 'outcome': 'ADOPT_TAIL'},
          'script_sha256': v['compare']['sha256'], 'prereg': v['prereg'], 'case_block': v['case_block']}
    v['verdict'] = wj(g / 'verdict.json', vd)
    fx.v007 = v
    fx.mods = {'context': wx(g / 'syn_context.py', (CONTEXT_SRC % (CORE[0], CORE[1])).encode()),
               'direct': wx(g / 'syn_direct_context.py', DIRECT_SRC.encode()),
               'custody': wx(g / 'syn_custody_deriver.py', b'def derive_custody(**kw):\n    return {}\n'),
               'enumerator': wx(g / 'syn_state_enumerator.py', b'def enumerate_states(**kw):\n    return []\n'),
               'producer': wx(g / 'syn_producer.py', b'def produce(**kw):\n    return None\n')}
    reg = wj(g / 'cert_registry.json', {'points': {}})
    rev = wj(g / 'cert_policy_review.json', {'schema': 'SYNTHETIC'})
    block = copy.deepcopy(json.loads(rb_pinned(*CFG))['numerics']['block'])
    fx.c1 = wj(g / 'config_c1.json', {'numerics': {'verdict_artifact': v['verdict'], 'sealed_prereg': v['prereg'],
                                                     'compare': v['compare'], 'block': block},
                                        'tail_readiness': {'certificate_registry': reg, 'certificate_policy_review': rev,
                                                           'custody_deriver': fx.mods['custody'],
                                                           'state_enumerator': fx.mods['enumerator'],
                                                           'approved_certificate_producers': [fx.mods['producer']]}})
    tup = (v['compare']['sha256'], v['prereg']['sha256'], v['addendum']['sha256'], 'SYN_VERDICT_SCHEMA', v['verdict']['sha256'])
    fx.policy = wx(g / 'syn_policy_ok.py', (POLICY_SRC % repr({tup})).encode())
    fx.out_root = fx.root / 'out'
    os.mkdir(fx.out_root)
    fx.n = 0
    dbp = json.loads(rb_pinned(*DBP))['batches']
    # A166: the RSS-at-RAM form is the first-run form; wall and output caps are DBP POST_S1's, unchanged.
    fx.caps = dict(dbp['POST_S1']['caps_per_case']['ROOT_NAMES_AT_REGISTRATION_K4'], rss_cap_bytes=RAM_BYTES)
    fx.rule = dict(dbp['POST_S1']['route_a_admission'], max_active=1)
    return fx


def sources(guard_path, launcher_path, extra=()):
    s = {p: sha(rb(p)) for p in (guard_path, launcher_path, MONITOR[0], DRIVER[0], CORE[0])}
    for m in FX.mods.values():
        s[m['path']] = m['sha256']
    s[FX.policy['path']] = FX.policy['sha256']
    for e in extra:
        s[e['path']] = e['sha256']
    return s


CORE_INACTIVE = {'normal_qos_required': True, 'step2_route_a_inactive': True, 'campaign_inactive': True,
                 'background_noncritical_lanes': True, 'sleep_assertion_required': True}
CORE_OVERLAP = dict(CORE_INACTIVE, campaign_inactive=False)


def admitted(G, gpath, lpath, *, case='S1_UA_C4T', spec=None, batch='POST_S1', core=None, s1_overlap='default',
             fill=None, replay=None, status='ROOT_AUTHORIZED', n_calls=1, mutate_plan=None, mutate_adm=None,
             prelaunch_tamper=False, extra_sources=()):
    """spec -> native prelaunch record (the guard under test) -> plan -> admission (synthetic root bytes)."""
    FX.n += 1
    d = FX.root / ('adm_%03d' % FX.n)
    os.mkdir(d)
    spec = spec or FX.spec_c4t
    fill = fill or FX.fill
    replay = replay or FX.replay
    calls = []
    srcs = sources(gpath, lpath, (replay,) + tuple(extra_sources))
    partial = {'schema': 'UNT_STEP4_ADMISSION_CX1V001', 'authority': G.AUTHORITY, 'status': 'ROOT_AUTHORIZED',
               'sources': srcs, 'v007': FX.v007, 'adoption_policy': FX.policy, 'config': FX.c1,
               'context_module': FX.mods['context'], 'direct_context': FX.mods['direct'], 'tail_off_policy': None}
    for k in range(n_calls):
        name = 'call_%d' % k
        outdir = str(FX.out_root / d.name / name)
        c = {'case': case if k == 0 else case + '_%d' % k, 'spec': spec, 'driver': pinj(DRIVER), 'spec_status': 'ROOT_FINAL',
             'pending': [], 'distance_Mpc': 4.04, 'tail_on': True, 'family': 'S4_POST_S1', 'outdir': outdir,
             'receipt': outdir + '.receipt.json', 'monitor_log': outdir + '.monitor.log'}
        c.update({kk: FX.caps[kk] for kk in ('wall_cap_s', 'rss_cap_bytes', 'output_cap_bytes')})
        pre = G.native_preflight(partial, c)
        if prelaunch_tamper:
            pre = copy.deepcopy(pre)
            pre['checks']['normalized_sha256'] = '0' * 64
        c['prelaunch'] = wj(d / ('prelaunch_%d.json' % k), pre)
        calls.append(c)
    os.mkdir(str(FX.out_root / d.name))
    plan = {'schema': 'UNT_STEP4_LAUNCH_PLAN_CX1V001', 'binding_status': 'ROOT_BOUND', 'batch': batch,
            'launcher': {'path': lpath, 'sha256': sha(rb(lpath))}, 'guard': {'path': gpath, 'sha256': sha(rb(gpath))},
            'monitor': pinj(MONITOR), 'route_a_admission': FX.rule,
            'launcher_log': str(FX.out_root / d.name / 'batch.launcher.log'), 'calls': calls,
            's1': {'fill_record': fill}}
    if mutate_plan:
        mutate_plan(plan)
    plan_ref = wx(d / 'plan.json', (json.dumps(plan, sort_keys=True, indent=2) + '\n').encode())
    review = wj(d / 'source_review.json', {'schema': 'UNT_STEP4_SOURCE_REVIEW_CX1V001', 'status': 'TESTED', 'verdict': 'PASS',
                                           'approved_sources': srcs, 'blocking_findings': [],
                                           'reviewer': 'SYNTHETIC_TEST_REVIEWER'})
    adm = dict(partial, status=status, plan=plan_ref, source_review=review, route_a_admission=FX.rule,
               core_priority=core or CORE_OVERLAP, case_order=[c['case'] for c in calls],
               caps={c['case']: {kk: c[kk] for kk in ('wall_cap_s', 'rss_cap_bytes', 'output_cap_bytes')} for c in calls},
               calls={c['case']: {'spec': c['spec'], 'driver': c['driver'], 'prelaunch': c['prelaunch']} for c in calls})
    if s1_overlap == 'default':
        adm['s1_overlap'] = {'schema': 'UNT_S1_OVERLAP_ADMISSION_C2V001', 'replay_module': replay, 'fill_record': fill}
    elif s1_overlap is not None:
        adm['s1_overlap'] = s1_overlap
    if mutate_adm:
        mutate_adm(adm)
    adm_ref = wj(d / 'admission.json', adm, indent=2)
    return {'plan': plan_ref, 'admission': adm_ref, 'dir': d, 'plan_doc': plan, 'adm_doc': adm}


def for_guard(G):
    return {id(G11): (G11_PATH, L12_PATH), id(G12): (G12_PATH, L13_PATH), id(G13): (G13_PATH, L14_PATH)}[id(G)]


def adm_for(G, **kw):
    gp, lp = for_guard(G)
    return admitted(G, gp, lp, **kw)


# ---------------------------------------------------------------------------------------------- gate fakes (guard012 only)
class Clock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t

    def sleep(self, s):
        self.t += float(s)


def snap(runs=(), ok=True, swap=1.0, pool_free=100.0):
    return {'ok': ok, 'reasons': [] if ok else ['ps: synthetic probe failure'], 'runs': list(runs), 'swap_gb': swap,
            'vm': None, 'pool_free_gb': pool_free, 'procs_cpu': {}, 'footprint_source': 'top'}


def tree(pid, fp, outdir, driver=DRIVER[1], spec=None, nproc=11, age=5000.0):
    return {'monitor_pid': pid, 'age_s': age, 'outdir': outdir, 'members': [pid + 1], 'nproc': nproc,
            'cpu_s': {pid + 1: 10.0}, 'rss_bytes': 1, 'driver_sha256': driver, 'spec': spec, 'footprint_gb': fp}


def make_gate(snapshot, params=None):
    clock = Clock()
    calls = {'n': 0}

    def probe():
        calls['n'] += 1
        return copy.deepcopy(snapshot)
    return GM.Gate(params=params, probe_fn=probe, clock=clock), clock, calls


def admitting_snapshot():
    return snap([tree(600, 9.0, str(FX.root / 'campaign_route_a'))])


def run_validate(G, a, *, snapshot=None, gate_params=None, check_outputs=True, gate_obj=None):
    """guard013 and guard011 take no gate; guard012 gets the synthetic gate (admitting unless a snapshot is given)."""
    kw, calls = {}, {'n': None}
    if G is G12:
        gate, clock, calls = make_gate(snapshot if snapshot is not None else admitting_snapshot(), gate_params)
        kw = {'_overlap_gate': gate_obj if gate_obj is not None else gate, '_overlap_sleep': clock.sleep}
    try:
        G.validate(a['plan'], a['plan_doc']['launcher']['path'], check_outputs=check_outputs,
                   execute_native=True, config_ref=a['admission'], disk_batch=False, **kw)
        return 'PASS', calls['n']
    except Exception as exc:
        return code_of(exc), calls['n']


def tmpdir(tag):
    FX.n += 1
    d = FX.root / ('%s_%03d' % (tag, FX.n))
    os.mkdir(d)
    return d


def twin_snapshot():
    ngc = GM.PARAMS['ngc_driver_sha256']
    tw = wj(tmpdir('twin') / 'spec.json', {'numerics': {'route_a': {'column_workers': 8}}})
    return snap([tree(500, 30.0, str(FX.root / 'twin_out'), driver=ngc, spec=tw['path'])])


class BoomGate:
    def __init__(self):
        self.P = dict(GM.PARAMS)

    def hold_check(self):
        raise RuntimeError('synthetic gate failure')


# ================================================================================================ guard013 tests
# The declared guard012 -> guard013 edits. Applied to guard012's pinned bytes they must give guard013's bytes exactly.
DOC12 = '''c2v012 = guard011 (eb97e303) with one change (A150 R-S1-3 (1)): the L333 core-priority clause. A POST_S1 batch
of one S1_UA_C3T / S1_UA_C4T call, its spec verified by the S1 fill-record replay, may be admitted with the
campaign active iff machine gate v003 hold_check and decide admit the S1 head from a live snapshot, A133's root
memory rule holds on that snapshot, and the snapshot shows no other r5 tree in route A beyond the gate's
allowance. The live gate is evaluated at every validation before the call starts. Every other batch is
unchanged: campaign_inactive true is still required, with guard011's code and refusal.
'''
REMOVED_NAMES = {'GATE_PIN', 'A133_LIMIT_GB', 'A133_S1_TERM_GB', 'A133_CAMPAIGN_RESERVE_GB', 's1_overlap_started',
                 'load_gate', 's1_overlap_live', '_overlap_gate', '_overlap_sleep', 'hold_check', 'decide', 'runs_view',
                 'class_from_spec_bytes', 'warmup_s', 'route_a_cap', 'footprint_gb', 'time'}


def forward_guard013(t12):
    def once(s, old, new):
        assert s.count(old) == 1, old[:60]
        return s.replace(old, new, 1)
    s = t12
    a = s.index(DOC12)
    b = s.index('"""', a)
    assert b == a + len(DOC12)
    doc13 = rb(G13_PATH).decode()
    a13 = doc13.index('\nc2v013 = guard012 (f4656fec)') + 1
    s = s[:a] + doc13[a13:doc13.index('"""', a13)] + s[b:]          # docstring paragraph: replaced (text compared below)
    s = once(s, ', sys, time, types, threading\n', ', sys, types, threading\n')
    a = s.index("GATE_PIN={'path':")
    b = s.index('def core_priority_admission(plan,cfg):')
    s = s[:a] + ('# c2v013 (V006 A166): GATE_PIN, the A133 constants, s1_overlap_started, load_gate and s1_overlap_live'
                 ' are removed.\n\n') + s[b:]
    a = s.index('def s1_overlap_started(call):\n')
    b = s.index('def validate(plan_ref,producer')
    s = s[:a] + s[b:]
    s = once(s, ',disk_batch=True,_overlap_gate=None,_overlap_sleep=None):', ',disk_batch=True):')
    s = once(s, '    overlap=core_priority_admission(plan,cfg)\n', '    core_priority_admission(plan,cfg)\n')
    s = once(s, '    if overlap is not None and not s1_overlap_started(overlap):'
                's1_overlap_live(overlap,gate=_overlap_gate,sleep=_overlap_sleep)\n', '')
    return s


def identifiers(text):
    out = set()
    for n in ast.walk(ast.parse(text)):
        if isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            out.add(n.name)
        elif isinstance(n, ast.Attribute):
            out.add(n.attr)
        elif isinstance(n, ast.arg):
            out.add(n.arg)
        elif isinstance(n, ast.alias):
            out.add(n.name)
        elif isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value.isidentifier():
            out.add(n.value)
    return out


@test('G13-P0', 'MUST_PASS')
def t_diff_scope():
    """guard013 == the declared edits applied to guard012 (f4656fec); none of the removed names survives."""
    t12 = rb_pinned(G12_PATH, G12_SHA).decode()
    t13 = rb(G13_PATH).decode()
    fwd = forward_guard013(t12)
    left = sorted(REMOVED_NAMES & identifiers(t13))
    gone = sorted(REMOVED_NAMES - identifiers(t12))       # every listed name existed in guard012 (no vacuous check)
    doc_ok = ('no memory condition' in t13.split('"""')[1] and 'campaign_inactive true is still required' in t13.split('"""')[1])
    return fwd == t13 and not left and not gone and doc_ok, {'forward_sha': sha(fwd.encode()), 'guard013': sha(t13.encode()),
                                                             'removed_names_left': left, 'names_absent_in_g12': gone}


@test('G13-P1', 'MUST_PASS')
def t_overlap_admits():
    """The S1 overlap (campaign active) is admitted with no gate, no snapshot and RSS cap = RAM."""
    a = adm_for(G13)
    got, _ = run_validate(G13, a)
    rss = a['plan_doc']['calls'][0]['rss_cap_bytes']
    return got == 'PASS' and rss == RAM_BYTES and a['adm_doc']['caps']['S1_UA_C4T']['rss_cap_bytes'] == RAM_BYTES, \
        {'got': got, 'rss_cap_bytes': rss}


@test('G13-P2', 'MUST_PASS')
def t_inactive_unchanged():
    a = adm_for(G13, core=CORE_INACTIVE, s1_overlap=None)
    got, _ = run_validate(G13, a)
    return got == 'PASS', {'got': got}


@test('G13-P3', 'MUST_PASS')
def t_differential_guard011():
    """Every admission that is not the overlap form gets the same outcome from guard011 and guard013."""
    variants = {
        'inactive_post_s1': dict(core=CORE_INACTIVE, s1_overlap=None),
        'inactive_headline': dict(core=CORE_INACTIVE, s1_overlap=None, batch='HEADLINE', case='C4T_HEAD', spec=FX.spec_head),
        'inactive_with_ignored_overlap_block': dict(core=CORE_INACTIVE),
        'overlap_flag_headline_batch': dict(core=CORE_OVERLAP, batch='HEADLINE', case='C4T_HEAD', spec=FX.spec_head),
        'step2_active': dict(core=dict(CORE_INACTIVE, step2_route_a_inactive=False)),
        'extra_core_key': dict(core=dict(CORE_INACTIVE, extra=True)),
        'qos_false': dict(core=dict(CORE_OVERLAP, normal_qos_required=False)),
        'status_draft': dict(core=CORE_INACTIVE, status='ROOT_DRAFT'),
        'prelaunch_tamper': dict(core=CORE_INACTIVE, prelaunch_tamper=True),
        'caps_mismatch': dict(core=CORE_INACTIVE, mutate_adm=lambda adm: adm['caps']['S1_UA_C4T'].__setitem__('wall_cap_s', 1)),
        'two_calls_inactive': dict(core=CORE_INACTIVE, s1_overlap=None, n_calls=2),
        'ramp_rule_changed': dict(core=CORE_INACTIVE, s1_overlap=None,
                                  mutate_plan=lambda p: p.__setitem__('route_a_admission', dict(p['route_a_admission'], minimum_free_percent=0)),
                                  mutate_adm=lambda adm: adm.__setitem__('route_a_admission', dict(adm['route_a_admission'], minimum_free_percent=0))),
    }
    out, ok = {}, True
    for name, kw in variants.items():
        r11, _ = run_validate(G11, adm_for(G11, **kw))
        r13, _ = run_validate(G13, adm_for(G13, **kw))
        out[name] = [r11, r13]
        ok = ok and r11 == r13
    return ok, out


@test('G13-P4', 'MUST_PASS')
def t_revalidation_after_start():
    """The worker's re-validation (check_outputs=False) while the S1 call runs still admits."""
    a = adm_for(G13)
    c = a['plan_doc']['calls'][0]
    with open(c['monitor_log'], 'xb') as f:
        f.write(b'started\n')
    got, _ = run_validate(G13, a, check_outputs=False)
    return got == 'PASS', {'got': got}


@test('G13-P5', 'MUST_PASS')
def t_memory_conditions_removed():
    """Each memory refusal guard012 gives the S1 overlap (gate v003, route-A allowance, A133) is gone in guard013:
    guard012 refuses with the listed code and guard013 admits the same custody form."""
    params_a133 = {'knee_static_gb': 200.0, 'hard_static_gb': 250.0}
    variants = {
        'gate_refused': (dict(snapshot=snap([tree(600, 30.0, str(FX.root / 'campaign_big'))])), 'S1_OVERLAP_GATE_REFUSED'),
        'twin_hold': (dict(snapshot=twin_snapshot()), 'S1_OVERLAP_GATE_TWIN_HOLD'),
        'probe_failed': (dict(snapshot=snap(ok=False)), 'S1_OVERLAP_GATE_PROBE_FAILED'),
        'two_r5_route_a': (dict(snapshot=snap([tree(600, 3.0, str(FX.root / 'r5_a'), nproc=2),
                                               tree(700, 3.0, str(FX.root / 'r5_b'), nproc=2)])),
                           'S1_OVERLAP_R5_ROUTE_A_BEYOND_GATE_ALLOWANCE'),
        'unknown_driver_route_a': (dict(snapshot=snap([tree(600, 3.0, str(FX.root / 'r5_a2'), nproc=2),
                                                       tree(700, 3.0, str(FX.root / 'unk_b'), driver=None, nproc=2)])),
                                   'S1_OVERLAP_R5_ROUTE_A_BEYOND_GATE_ALLOWANCE'),
        'a133_footprint_unknown': (dict(snapshot=snap([tree(600, None, str(FX.root / 'r5_unknown_fp'), nproc=2)])),
                                   'S1_OVERLAP_A133_FOOTPRINT_UNKNOWN'),
        'a133_rule': (dict(snapshot=snap([tree(600, 50.0, str(FX.root / 'r5_50gb'), nproc=2)], pool_free=500.0),
                           gate_params=params_a133), 'S1_OVERLAP_A133_MEMORY_RULE'),
        'gate_error': (dict(gate_obj=BoomGate()), 'S1_OVERLAP_GATE_ERROR'),
    }
    out, ok = {}, True
    for name, (gkw, want12) in variants.items():
        r12, _ = run_validate(G12, adm_for(G12), **gkw)
        r13, _ = run_validate(G13, adm_for(G13))
        out[name] = [r12, r13]
        ok = ok and r12 == want12 and r13 == 'PASS'
    return ok, out


def _custody_variants():
    def not_allowlisted(adm):
        adm['sources'] = {k: v for k, v in adm['sources'].items() if k != FX.replay['path']}
        sr = json.loads(rb(adm['source_review']['path']))
        sr['approved_sources'] = adm['sources']
        adm['source_review'] = wj(Path(adm['source_review']['path']).parent / 'source_review_2.json', sr)
    return {
        'admits': (dict(), 'PASS'),
        'headline_batch': (dict(batch='HEADLINE', case='C4T_HEAD', spec=FX.spec_head), 'CORE_PRIORITY_ATTESTATION_REQUIRED'),
        'non_s1_case': (dict(case='C4T'), 'S1_OVERLAP_S1_CASE_REQUIRED'),
        'two_calls': (dict(n_calls=2), 'S1_OVERLAP_ONE_CALL_REQUIRED'),
        'replay_mismatch': (dict(fill=FX.fill_tamper), 'S1_OVERLAP_REPLAY_MISMATCH'),
        'replay_not_allowlisted': (dict(mutate_adm=not_allowlisted), 'SOURCE_NOT_ALLOWLISTED'),
        'replay_api': (dict(replay=FX.replay_bad_api), 'S1_OVERLAP_REPLAY_API'),
        'fill_binding': (dict(mutate_plan=lambda p: p['s1'].__setitem__('fill_record', FX.fill_other)), 'S1_OVERLAP_FILL_RECORD_BINDING'),
        'step2_active': (dict(core=dict(CORE_OVERLAP, step2_route_a_inactive=False)), 'CORE_PRIORITY_ATTESTATION_REQUIRED'),
        'block_missing': (dict(s1_overlap=None), 'S1_OVERLAP_ADMISSION_REQUIRED'),
        'block_schema': (dict(s1_overlap={'schema': 'X', 'replay_module': FX.replay, 'fill_record': FX.fill}), 'S1_OVERLAP_ADMISSION_SCHEMA'),
        'spec_not_filled': (dict(case='S1_UA_C3T'), 'S1_OVERLAP_SPEC_NOT_FILLED_SPEC'),
        'replay_refused': (dict(fill=FX.fill_refuse), 'S1_OVERLAP_REPLAY_REFUSED'),
        'tail_off': (dict(mutate_plan=lambda p: p['calls'][0].__setitem__('tail_on', False)), 'S1_OVERLAP_TAIL_ON_R5_REQUIRED'),
    }


@test('G13-P6', 'MUST_PASS')
def t_custody_agrees_guard012():
    """With guard012's gate admitting, guard012 and guard013 give the same outcome on every S1 overlap custody variant:
    the change is the memory admission only."""
    out, ok = {}, True
    for name, (kw, want) in _custody_variants().items():
        r12, _ = run_validate(G12, adm_for(G12, **kw))
        r13, _ = run_validate(G13, adm_for(G13, **kw))
        out[name] = [r12, r13]
        ok = ok and r12 == r13 == want
    return ok, out


def _hook(event, args):
    if AUDIT['on'] and event in ('open', 'subprocess.Popen', 'os.posix_spawn', 'os.fork', 'os.forkpty', 'os.exec', 'os.system'):
        AUDIT['events'].append((event, str(args[0]) if args else ''))


def audited(fn):
    if not AUDIT['installed']:
        sys.addaudithook(_hook)
        AUDIT['installed'] = True
    AUDIT['events'] = []
    AUDIT['on'] = True
    try:
        r = fn()
    finally:
        AUDIT['on'] = False
    return r, list(AUDIT['events'])


@test('G13-P7', 'MUST_PASS')
def t_no_gate_read_no_process():
    """guard013's overlap validation opens no gate source and starts no process; guard012's (control) opens the gate."""
    a13 = adm_for(G13)
    a12 = adm_for(G12)
    (r13, _), ev13 = audited(lambda: run_validate(G13, a13))
    (r12, _), ev12 = audited(lambda: run_validate(G12, a12))
    g13_gate = [e for e in ev13 if e[0] == 'open' and e[1] == GATE[0]]
    g13_proc = [e for e in ev13 if e[0] != 'open']
    g12_gate = [e for e in ev12 if e[0] == 'open' and e[1] == GATE[0]]
    ok = r13 == 'PASS' and r12 == 'PASS' and not g13_gate and not g13_proc and len(g12_gate) >= 1
    return ok, {'g13': r13, 'g12': r12, 'g13_gate_opens': len(g13_gate), 'g13_process_events': g13_proc,
                'g12_gate_opens_control': len(g12_gate)}


def _ff(code, **kw):
    a = adm_for(G13, **kw)
    got, _ = run_validate(G13, a)
    return got == code, {'got': got, 'want': code}


@test('G13-F1', 'MUST_FAIL')
def t_overlap_headline():
    return _ff('CORE_PRIORITY_ATTESTATION_REQUIRED', batch='HEADLINE', case='C4T_HEAD', spec=FX.spec_head)


@test('G13-F2', 'MUST_FAIL')
def t_overlap_non_s1_case():
    return _ff('S1_OVERLAP_S1_CASE_REQUIRED', case='C4T')


@test('G13-F3', 'MUST_FAIL')
def t_overlap_two_calls():
    return _ff('S1_OVERLAP_ONE_CALL_REQUIRED', n_calls=2)


@test('G13-F4', 'MUST_FAIL')
def t_overlap_replay_mismatch():
    return _ff('S1_OVERLAP_REPLAY_MISMATCH', fill=FX.fill_tamper)


@test('G13-F5', 'MUST_FAIL')
def t_overlap_replay_not_allowlisted():
    kw, want = _custody_variants()['replay_not_allowlisted']
    return _ff(want, **kw)


@test('G13-F6', 'MUST_FAIL')
def t_overlap_replay_api():
    return _ff('S1_OVERLAP_REPLAY_API', replay=FX.replay_bad_api)


@test('G13-F7', 'MUST_FAIL')
def t_overlap_fill_binding():
    return _ff('S1_OVERLAP_FILL_RECORD_BINDING', mutate_plan=lambda p: p['s1'].__setitem__('fill_record', FX.fill_other))


@test('G13-F15', 'MUST_FAIL')
def t_overlap_step2_active():
    return _ff('CORE_PRIORITY_ATTESTATION_REQUIRED', core=dict(CORE_OVERLAP, step2_route_a_inactive=False))


@test('G13-F16', 'MUST_FAIL')
def t_overlap_block_missing():
    return _ff('S1_OVERLAP_ADMISSION_REQUIRED', s1_overlap=None)


@test('G13-F17', 'MUST_FAIL')
def t_overlap_block_schema():
    return _ff('S1_OVERLAP_ADMISSION_SCHEMA', s1_overlap={'schema': 'X', 'replay_module': FX.replay, 'fill_record': FX.fill})


@test('G13-F19', 'MUST_FAIL')
def t_overlap_spec_not_filled():
    return _ff('S1_OVERLAP_SPEC_NOT_FILLED_SPEC', case='S1_UA_C3T')


@test('G13-F20', 'MUST_FAIL')
def t_overlap_replay_refused():
    return _ff('S1_OVERLAP_REPLAY_REFUSED', fill=FX.fill_refuse)


@test('G13-F21', 'MUST_FAIL')
def t_overlap_tail_off():
    return _ff('S1_OVERLAP_TAIL_ON_R5_REQUIRED', mutate_plan=lambda p: p['calls'][0].__setitem__('tail_on', False))


@test('G13-F22', 'MUST_FAIL')
def t_guard_identity():
    """A plan naming guard012 is refused by guard013 (LAUNCHER_GUARD_IDENTITY)."""
    a = adm_for(G13, extra_sources=({'path': G12_PATH, 'sha256': G12_SHA},),
                mutate_plan=lambda p: p.__setitem__('guard', {'path': G12_PATH, 'sha256': G12_SHA}))
    got, _ = run_validate(G13, a)
    return got == 'LAUNCHER_GUARD_IDENTITY', {'got': got}


@test('G13-F23', 'MUST_FAIL')
def t_guard011_refuses_overlap():
    """The same overlap admission under guard011 is refused at L333."""
    got, _ = run_validate(G11, adm_for(G11))
    return got == 'CORE_PRIORITY_ATTESTATION_REQUIRED', {'got': got}


@test('G13-F24', 'MUST_FAIL')
def t_guard012_refuses_guard013_plan():
    """A plan naming guard013 with launcher013 is refused by guard012, the guard launcher013 loads: the memory-free
    overlap needs the guard013 / launcher014 pair."""
    a = admitted(G12, G12_PATH, L13_PATH, extra_sources=({'path': G13_PATH, 'sha256': sha(rb(G13_PATH))},),
                 mutate_plan=lambda p: p.__setitem__('guard', {'path': G13_PATH, 'sha256': sha(rb(G13_PATH))}))
    got, _ = run_validate(G12, a)
    return got == 'LAUNCHER_GUARD_IDENTITY', {'got': got}


# ================================================================================================ launcher014 tests
LCOM13 = ["# c2v013 = launcher012 (59c00707) with two constants changed only: the guard is guard012 (A150 R-S1-3 (1)), and the",
          "# machine lock stays launcher012's own file (absolute path), so every step-4 batch still shares one lock."]


@test('L14-P1', 'MUST_PASS')
def t_launcher_diff_scope():
    t14 = rb(L14_PATH).decode().splitlines(keepends=True)
    t13 = rb_pinned(L13_PATH, L13_SHA).decode().splitlines(keepends=True)
    diff = [ln for ln in difflib.unified_diff(t13, t14, n=0) if ln[:1] in '+-' and not ln.startswith(('+++', '---'))]
    removed = sorted(ln[1:].rstrip('\n') for ln in diff if ln.startswith('-'))
    added = sorted(ln[1:].rstrip('\n') for ln in diff if ln.startswith('+'))
    want_removed = sorted(LCOM13 + ["GUARD_PATH=HERE/'step4_guard_c2v012.py'", "GUARD_SHA256='%s'" % G12_SHA])
    ok = (removed == want_removed and len(added) == 4
          and "GUARD_PATH=HERE/'step4_guard_c2v013.py'" in added
          and "GUARD_SHA256='%s'" % sha(rb(G13_PATH)) in added
          and sum(1 for x in added if x.startswith('# ')) == 2
          and sum(1 for x in added if x.startswith('# c2v014 = launcher013 (620a44da)')) == 1)
    return ok, {'removed': removed, 'added': added}


@test('L14-P2', 'MUST_PASS')
def t_launcher_loads_guard013():
    m14 = load_bytes_module(L14_PATH, sha(rb(L14_PATH)), '_t_launcher014')
    m13 = load_bytes_module(L13_PATH, L13_SHA, '_t_launcher013')
    l12_lock = Path(L12_PATH).resolve().parent.parent / 'STEP4_MACHINE_LOCK_V001'
    grid = [dict(active_route_a=a, free=f, previous_iteration=p, first=fi, max_active=mx)
            for a in (0, 1, 2) for f in (None, 0, 24, 25, 100) for p in (None, False, True) for fi in (False, True) for mx in (1, 2)]
    same_ramp = all(m14.decision(**g) == m13.decision(**g) for g in grid)
    ok = (m14.G.__file__ == G13_PATH and sha(m14.GUARD_BYTES) == sha(rb(G13_PATH))
          and hasattr(m14.G, 'core_priority_admission') and not hasattr(m14.G, 's1_overlap_live')
          and not hasattr(m14.G, 'GATE_PIN') and str(m14.LOCK) == str(l12_lock) == str(m13.LOCK)
          and m14.PYTHON == m13.PYTHON and same_ramp)
    return ok, {'guard': m14.G.__file__, 'lock': str(m14.LOCK), 'ramp_equal_launcher013': same_ramp, 'grid': len(grid)}


@test('L14-F1', 'MUST_FAIL')
def t_launcher_tampered_guard():
    d = tmpdir('l14_tamper')
    wx(d / 'step4_launcher_c2v014.py', rb(L14_PATH))
    wx(d / 'step4_guard_c2v013.py', rb(G13_PATH) + b'\n# tampered\n')
    try:
        raw = rb(str(d / 'step4_launcher_c2v014.py'))
        m = types.ModuleType('_t_l14_tampered')
        m.__file__ = str(d / 'step4_launcher_c2v014.py')
        exec(compile(raw, m.__file__, 'exec'), m.__dict__)
        return False, 'loaded'
    except PermissionError as exc:
        return str(exc) == 'GUARD_BOOTSTRAP_HASH_MISMATCH', str(exc)


# ================================================================================================ main
def main():
    global RUN, FX, G11, G12, G13, GM
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    a = ap.parse_args()
    RUN = Path(os.path.abspath(a.run_dir))
    os.mkdir(str(RUN))
    t0 = time.time()
    started = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    G11 = load_bytes_module(G11_PATH, G11_SHA, '_t_guard011')
    G12 = load_bytes_module(G12_PATH, G12_SHA, '_t_guard012')
    G13 = load_bytes_module(G13_PATH, sha(rb(G13_PATH)), '_t_guard013')
    GM = load_bytes_module(GATE[0], GATE[1], '_t_gate_v003')
    try:
        FX = build_fixtures()
        fx_ok = True
    except Exception:
        fx_ok = False
        LOG.append('FIXTURES FAILED\n' + traceback.format_exc())
    if fx_ok:
        for fn in TESTS:
            try:
                ok, det = fn()
            except Exception as exc:
                ok, det = False, 'EXCEPTION %s: %s\n%s' % (type(exc).__name__, exc, traceback.format_exc()[-1500:])
            record(fn._tid, fn._kind, bool(ok), det)
    n = len(RESULTS)
    npass = sum(1 for r in RESULTS if r['result'] == 'PASS')
    summary = {'schema': 'UNT_STEP4_GUARD013_TEST_RESULTS_C2V001', 'started_utc': started,
               'finished_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'seconds': round(time.time() - t0, 1),
               'python': sys.version.split()[0], 'interpreter': sys.executable,
               'files_sha256': {p: sha(rb(p)) for p in (G13_PATH, L14_PATH, str(Path(__file__).resolve()))},
               'fixtures_ok': fx_ok, 'n_tests': n, 'n_pass': npass,
               'by_kind': {k: {'n': sum(1 for r in RESULTS if r['kind'] == k),
                               'pass': sum(1 for r in RESULTS if r['kind'] == k and r['result'] == 'PASS')}
                           for k in ('MUST_PASS', 'MUST_FAIL')},
               'results': RESULTS}
    wx(RUN / 'TEST_RESULTS.json', (json.dumps(summary, indent=1, sort_keys=True, default=str) + '\n').encode())
    wx(RUN / 'TEST_LOG.txt', ('\n'.join(LOG) + '\n').encode())
    print(json.dumps({k: summary[k] for k in ('n_tests', 'n_pass', 'by_kind', 'fixtures_ok', 'seconds')}))
    return 0 if (fx_ok and npass == n) else 1


if __name__ == '__main__':
    sys.exit(main())
