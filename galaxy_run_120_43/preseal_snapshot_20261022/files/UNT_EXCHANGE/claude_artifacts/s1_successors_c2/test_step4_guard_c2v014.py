"""Synthetic MUST_PASS / MUST_FAIL tests for step4_guard_c2v014.py and step4_launcher_c2v015.py (s1_successors_c2).

  python3 -I -B test_step4_guard_c2v014.py --run-dir <a new directory>

Port of test_step4_guard_c2v013.py (30324d80) for V006 A172 (the step-4 packet A166 set). Target-free; launches
nothing; starts no process. guard014 and guard013 (sha-pinned) are executed from their bytes, guard011 (sha-pinned)
only for G14-F23; every admission is synthetic (synthetic seal, verdict, prereg, adoption policy, context and
direct-context modules, a synthetic S1 replay module). No machine gate is loaded. launcher015 / launcher014 are
executed as modules (their import loads their guard; main() is never called). The launcher worker loop is driven by a
synthetic harness: G.validate and G.disk_admission are stubbed (the real disk check stats /Volumes/External1), the lock
is a scratch file, subprocess and time are shims (taskpolicy, caffeinate and the monitor are recorded, never run), and
an audit hook records and BLOCKS every real process creation, so nothing is executed; a real /usr/bin/memory_pressure
request is the blocked event that makes memory "unreadable" in L15-P3.
Rules: guard013 runs on the C2V004 POST_S1 route_a_admission (memory fields present); guard014 on the same rule with
the three memory fields dropped (= DIRECT_BATCH_PARAMS_S45_C2V004B). Caps: C2V004B POST_S1 (RSS = RAM, A166).
Results: <run-dir>/TEST_RESULTS.json and <run-dir>/TEST_LOG.txt (exclusive create).
"""
import argparse
import ast
import contextlib
import copy
import difflib
import hashlib
import io
import json
import os
import signal
import subprocess
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
G13_PATH = SUCC + '/step4_guard_c2v013.py'
G13_SHA = '593bebb6958f947488c0566f91d2355d8653f72401fb764c417a3f9998d8b4e1'
L14_PATH = SUCC + '/step4_launcher_c2v014.py'
L14_SHA = '5d6af4a7024c6563be2ab99f519e32363bcdbc3397c1f852e86ab81109e4d12f'
G14_PATH = str(HERE / 'step4_guard_c2v014.py')
L15_PATH = str(HERE / 'step4_launcher_c2v015.py')
MONITOR = (ART + '/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py', 'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107')
DRIVER = (ART + '/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py', 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6')
CORE = (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py', 'dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6')
CFG = (ART + '/sched_s45_c2/v003/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V003.json', 'd9241676c3b7b32bd3067a55bdfb7821ebc33a68adbdc011ab4e4c58b6e50a4d')
DBP4 = (ART + '/sched_s45_c2/v004/DIRECT_BATCH_PARAMS_S45_C2V004.json', '7c3ceae51a702722fce543c60c726c67a80226d2b5d77cbb398da6e09b5a8455')
DBP4B = (ART + '/sched_s45_c2/v004b/DIRECT_BATCH_PARAMS_S45_C2V004B.json', 'e239d21e8f29e4711ec20c28c335bc25340fb8780253ceb1e57f037624e99205')
P5 = (ART + '/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json', 'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174')
GATE_V003 = ART + '/sched_s45_c2/v003/machine_gate_s45_c2v003.py'      # path only: must never be opened here
RAM_BYTES = 137438953472          # V006 A166: per-call RSS cap = physical RAM
MEM_FIELDS = ('minimum_free_percent', 'source', 'first_case_memory_exemption')
BLAS_KEYS = ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')

RUN = None
RESULTS, LOG, TESTS = [], [], []
G11 = G13 = G14 = None
FX = None


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


# ================================================================================================ audit hook
class Blocked(RuntimeError):
    pass


PROC_EVENTS = ('subprocess.Popen', 'os.posix_spawn', 'os.exec', 'os.system', 'os.fork', 'os.forkpty', 'os.spawn')
AUDIT = {'on': False, 'events': [], 'installed': False}


def _hook(event, args):
    if not AUDIT['on']:
        return
    if event == 'open':
        AUDIT['events'].append(('open', os.fsdecode(args[0]) if isinstance(args[0], (str, bytes, os.PathLike)) else repr(args[0])))
    elif event in PROC_EVENTS:
        AUDIT['events'].append((event, repr(args[0])[:200] if args else '', repr(args[1])[:300] if len(args) > 1 else ''))
        raise Blocked('process creation blocked by the test audit hook: %s %r' % (event, args[1] if len(args) > 1 else args))


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


def proc_events(ev):
    return [e for e in ev if e[0] != 'open']


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
exec(compile(ast.Module(body=_keep, type_ignores=[]), '<g14-test-core-validate_block>', 'exec'), _ns)
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
    v['seal'] = wj(g / 'seal.json', {'sealed_by': G14.AUTHORITY, 'prereg': v['prereg'], 'compare': v['compare'],
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
    d4 = json.loads(rb_pinned(*DBP4))['batches']
    d4b = json.loads(rb_pinned(*DBP4B))['batches']
    fx.caps = dict(d4b['POST_S1']['caps_per_case']['ROOT_NAMES_AT_REGISTRATION_K4'])
    assert fx.caps['rss_cap_bytes'] == RAM_BYTES
    fx.rule13 = dict(d4['POST_S1']['route_a_admission'], max_active=1)            # memory fields present (guard013 form)
    fx.rule14 = dict(d4b['POST_S1']['route_a_admission'], max_active=1)           # C2V004B form (guard014)
    assert fx.rule14 == {k: v for k, v in fx.rule13.items() if k not in MEM_FIELDS}
    fx.d4b = d4b
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
             prelaunch_tamper=False, extra_sources=(), rule=None, rule_fn=None):
    """spec -> native prelaunch record (the guard under test) -> plan -> admission (synthetic root bytes).
    rule: the route_a_admission for plan and admission (default: guard013 and older the memory form, guard014 the
    C2V004B form); rule_fn edits a copy of it, applied to both."""
    FX.n += 1
    d = FX.root / ('adm_%03d' % FX.n)
    os.mkdir(d)
    spec = spec or FX.spec_c4t
    fill = fill or FX.fill
    replay = replay or FX.replay
    rule = copy.deepcopy(rule if rule is not None else (FX.rule14 if G is G14 else FX.rule13))
    if rule_fn:
        rule_fn(rule)
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
            'monitor': pinj(MONITOR), 'route_a_admission': copy.deepcopy(rule),
            'launcher_log': str(FX.out_root / d.name / 'batch.launcher.log'), 'calls': calls,
            's1': {'fill_record': fill}}
    if mutate_plan:
        mutate_plan(plan)
    plan_ref = wx(d / 'plan.json', (json.dumps(plan, sort_keys=True, indent=2) + '\n').encode())
    review = wj(d / 'source_review.json', {'schema': 'UNT_STEP4_SOURCE_REVIEW_CX1V001', 'status': 'TESTED', 'verdict': 'PASS',
                                           'approved_sources': srcs, 'blocking_findings': [],
                                           'reviewer': 'SYNTHETIC_TEST_REVIEWER'})
    adm = dict(partial, status=status, plan=plan_ref, source_review=review, route_a_admission=copy.deepcopy(rule),
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
    return {id(G11): (G11_PATH, L12_PATH), id(G13): (G13_PATH, L14_PATH), id(G14): (G14_PATH, L15_PATH)}[id(G)]


def adm_for(G, **kw):
    gp, lp = for_guard(G)
    return admitted(G, gp, lp, **kw)


def run_validate(G, a, *, check_outputs=True):
    try:
        G.validate(a['plan'], a['plan_doc']['launcher']['path'], check_outputs=check_outputs,
                   execute_native=True, config_ref=a['admission'], disk_batch=False)
        return 'PASS'
    except Exception as exc:
        return code_of(exc)


def tmpdir(tag):
    FX.n += 1
    d = FX.root / ('%s_%03d' % (tag, FX.n))
    os.mkdir(d)
    return d


# ================================================================================================ guard014 tests
# The declared guard013 -> guard014 edits. Applied to guard013's pinned bytes they must give guard014's bytes exactly.
DOC13 = '''c2v013 = guard012 (f4656fec) with one change (V006 A166, the principal's direction to stop micromanaging the
Mac's resources): the S1 overlap's live memory admission is removed. A POST_S1 batch of one S1_UA_C3T / S1_UA_C4T
call, tail ON on r5, its spec verified by the S1 fill-record replay (guard012's core_priority_admission, unchanged),
may be admitted with the campaign active with no memory condition: no machine gate v003 hold_check / decide, no
r5 route-A allowance, no A133 rule. Every other batch is unchanged: campaign_inactive true is still required,
with guard011's code and refusal.
'''
G13_RULE_LINES = ("    require(rule.get('minimum_free_percent')==25 and rule.get('poll_seconds')==60 and rule.get('source')=='/usr/bin/memory_pressure' and rule.get('ramp')=='previous_first_completed_route_a_iteration','RAMP_RULE_REQUIRED')\n"
                  "    require(rule.get('first_case_memory_exemption') is False,'FIRST_MEMORY_BYPASS_REFUSED')\n")
G14_RULE_LINES = ("    require(rule.get('poll_seconds')==60 and rule.get('ramp')=='previous_first_completed_route_a_iteration','RAMP_RULE_REQUIRED')\n"
                  "    require(not MEMORY_ADMISSION_FIELDS&set(rule),'MEMORY_ADMISSION_FIELD_REFUSED')\n")
G13_ANCHOR = "# c2v013 (V006 A166): GATE_PIN, the A133 constants, s1_overlap_started, load_gate and s1_overlap_live are removed.\n"
G14_CONST = ("# c2v014 (V006 A172): the route-A rule's memory fields. guard013 L372-373 required them; guard014 refuses them.\n"
             "MEMORY_ADMISSION_FIELDS=frozenset({'minimum_free_percent','source','first_case_memory_exemption'})\n")


def forward_guard014(t13, t14):
    def once(s, old, new):
        assert s.count(old) == 1, old[:60]
        return s.replace(old, new, 1)
    s = t13
    a = s.index(DOC13)
    a14 = t14.index('\nc2v014 = guard013 (593bebb6)') + 1
    s = s[:a] + t14[a14:t14.index('"""', a14)] + s[a + len(DOC13):]      # docstring paragraph: replaced (checked below)
    s = once(s, G13_ANCHOR, G13_ANCHOR + G14_CONST)
    s = once(s, G13_RULE_LINES, G14_RULE_LINES)
    return s


@test('G14-P0', 'MUST_PASS')
def t_diff_scope():
    """guard014 == the declared edits applied to guard013 (593bebb6): the doc paragraph, the memory-field constant and
    the two rule lines; every other line is byte-identical. Top-level definitions other than validate are AST-identical."""
    t13 = rb_pinned(G13_PATH, G13_SHA).decode()
    t14 = rb(G14_PATH).decode()
    fwd = forward_guard014(t13, t14)
    doc = t14.split('"""')[1]
    doc_ok = ('MEMORY_ADMISSION_FIELD_REFUSED' in doc and 'core_priority_admission' in doc and 'V006 A172' in doc)
    a13 = {n.name: ast.dump(n) for n in ast.parse(t13).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    a14 = {n.name: ast.dump(n) for n in ast.parse(t14).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    changed = sorted(k for k in set(a13) | set(a14) if a13.get(k) != a14.get(k))
    return fwd == t14 and doc_ok and changed == ['validate'], {'forward_sha': sha(fwd.encode()), 'guard014': sha(t14.encode()),
                                                               'defs_changed': changed}


@test('G14-P1', 'MUST_PASS')
def t_overlap_admits_no_memory_fields():
    """A route_a_admission with no memory fields (C2V004B form) is admitted: the S1 overlap (campaign active), RSS = RAM."""
    a = adm_for(G14)
    got = run_validate(G14, a)
    rule = a['plan_doc']['route_a_admission']
    rss = a['plan_doc']['calls'][0]['rss_cap_bytes']
    return got == 'PASS' and not set(rule) & set(MEM_FIELDS) and rss == RAM_BYTES, {'got': got, 'rule': rule, 'rss': rss}


@test('G14-P2', 'MUST_PASS')
def t_inactive_unchanged():
    a = adm_for(G14, core=CORE_INACTIVE, s1_overlap=None)
    got = run_validate(G14, a)
    return got == 'PASS', {'got': got}


def _nonmemory_variants():
    return {
        'overlap_post_s1': dict(),
        'inactive_post_s1': dict(core=CORE_INACTIVE, s1_overlap=None),
        'inactive_headline': dict(core=CORE_INACTIVE, s1_overlap=None, batch='HEADLINE', case='C4T_HEAD', spec=FX.spec_head),
        'inactive_headline_two_calls_max3': dict(core=CORE_INACTIVE, s1_overlap=None, batch='HEADLINE', case='C4T_HEAD',
                                                 spec=FX.spec_head, n_calls=2, rule_fn=lambda r: r.__setitem__('max_active', 3)),
        'inactive_with_ignored_overlap_block': dict(core=CORE_INACTIVE),
        'overlap_flag_headline_batch': dict(core=CORE_OVERLAP, batch='HEADLINE', case='C4T_HEAD', spec=FX.spec_head),
        'step2_active': dict(core=dict(CORE_INACTIVE, step2_route_a_inactive=False)),
        'extra_core_key': dict(core=dict(CORE_INACTIVE, extra=True)),
        'qos_false': dict(core=dict(CORE_OVERLAP, normal_qos_required=False)),
        'status_draft': dict(core=CORE_INACTIVE, status='ROOT_DRAFT'),
        'prelaunch_tamper': dict(core=CORE_INACTIVE, prelaunch_tamper=True),
        'caps_mismatch': dict(core=CORE_INACTIVE, mutate_adm=lambda adm: adm['caps']['S1_UA_C4T'].__setitem__('wall_cap_s', 1)),
        'rss_cap_mismatch': dict(mutate_adm=lambda adm: adm['caps']['S1_UA_C4T'].__setitem__('rss_cap_bytes', 1)),
        'two_calls_inactive': dict(core=CORE_INACTIVE, s1_overlap=None, n_calls=2),
        'max_active_0': dict(rule_fn=lambda r: r.__setitem__('max_active', 0)),
        'max_active_7': dict(rule_fn=lambda r: r.__setitem__('max_active', 7)),
        'max_active_str': dict(rule_fn=lambda r: r.__setitem__('max_active', '1')),
        'max_active_missing': dict(rule_fn=lambda r: r.pop('max_active')),
        'poll_30': dict(rule_fn=lambda r: r.__setitem__('poll_seconds', 30)),
        'poll_missing': dict(rule_fn=lambda r: r.pop('poll_seconds')),
        'ramp_other': dict(rule_fn=lambda r: r.__setitem__('ramp', 'none')),
        'ramp_missing': dict(rule_fn=lambda r: r.pop('ramp')),
        'root_rule_differs': dict(mutate_adm=lambda adm: adm['route_a_admission'].__setitem__('max_active', 2)),
        'extra_nonmemory_key_both': dict(rule_fn=lambda r: r.__setitem__('note', 'x')),
        'extra_nonmemory_key_plan_only': dict(mutate_plan=lambda p: p['route_a_admission'].__setitem__('note', 'x')),
        'rule_missing_both': dict(mutate_plan=lambda p: p.pop('route_a_admission'),
                                  mutate_adm=lambda adm: adm.pop('route_a_admission')),
    }


@test('G14-P3', 'MUST_PASS')
def t_differential_guard013():
    """Non-memory behaviour is guard013's: on every non-memory variant (custody, batch, caps, status, and the non-memory
    rule fields max_active / poll_seconds / ramp / root equality / extra keys) guard013 on the memory form and guard014
    on the C2V004B form give the same outcome."""
    out, ok = {}, True
    for name, kw in _nonmemory_variants().items():
        r13 = run_validate(G13, adm_for(G13, **kw))
        r14 = run_validate(G14, adm_for(G14, **kw))
        out[name] = [r13, r14]
        ok = ok and r13 == r14
    refusals = sum(1 for v in out.values() if v[0] != 'PASS')
    return ok and refusals >= 15, dict(out, n_refusing_variants=refusals)


@test('G14-P4', 'MUST_PASS')
def t_revalidation_after_start():
    """The worker's re-validation (check_outputs=False) while the S1 call runs still admits."""
    a = adm_for(G14)
    c = a['plan_doc']['calls'][0]
    with open(c['monitor_log'], 'xb') as f:
        f.write(b'started\n')
    got = run_validate(G14, a, check_outputs=False)
    return got == 'PASS', {'got': got}


@test('G14-P5', 'MUST_PASS')
def t_memory_conditions_removed():
    """Each memory refusal guard013 gives (L372 RAMP_RULE_REQUIRED on the free / source terms, L373
    FIRST_MEMORY_BYPASS_REFUSED) is gone: guard013 refuses with the listed code and guard014 admits the rule with no
    memory field, for the same custody form."""
    def drop(*ks):
        return lambda r: [r.pop(k) for k in ks]
    variants = {
        'fields_absent': (dict(rule=FX.rule14), 'RAMP_RULE_REQUIRED'),
        'free_24': (dict(rule_fn=lambda r: r.__setitem__('minimum_free_percent', 24)), 'RAMP_RULE_REQUIRED'),
        'free_absent': (dict(rule_fn=drop('minimum_free_percent')), 'RAMP_RULE_REQUIRED'),
        'source_other': (dict(rule_fn=lambda r: r.__setitem__('source', '/usr/bin/vm_stat')), 'RAMP_RULE_REQUIRED'),
        'source_absent': (dict(rule_fn=drop('source')), 'RAMP_RULE_REQUIRED'),
        'exemption_true': (dict(rule_fn=lambda r: r.__setitem__('first_case_memory_exemption', True)), 'FIRST_MEMORY_BYPASS_REFUSED'),
        'exemption_absent': (dict(rule_fn=drop('first_case_memory_exemption')), 'FIRST_MEMORY_BYPASS_REFUSED'),
    }
    out, ok = {}, True
    for name, (kw13, want13) in variants.items():
        r13 = run_validate(G13, adm_for(G13, **kw13))
        r14 = run_validate(G14, adm_for(G14))
        out[name] = [r13, r14]
        ok = ok and r13 == want13 and r14 == 'PASS'
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


@test('G14-P6', 'MUST_PASS')
def t_custody_agrees_guard013():
    """guard013 and guard014 give the same outcome on every S1 overlap custody variant (core_priority_admission is
    guard013's, unchanged): the change is the route-A rule's memory fields only."""
    out, ok = {}, True
    for name, (kw, want) in _custody_variants().items():
        r13 = run_validate(G13, adm_for(G13, **kw))
        r14 = run_validate(G14, adm_for(G14, **kw))
        out[name] = [r13, r14]
        ok = ok and r13 == r14 == want
    return ok, out


@test('G14-P7', 'MUST_PASS')
def t_no_gate_read_no_process():
    """guard014's validation (overlap and inactive) opens no gate source and starts no process (the audit hook blocks
    and records any); the hook is live (it records the plan and admission opens)."""
    a1, a2 = adm_for(G14), adm_for(G14, core=CORE_INACTIVE, s1_overlap=None)
    (r1, r2), ev = audited(lambda: (run_validate(G14, a1), run_validate(G14, a2)))
    gate = [e for e in ev if e[0] == 'open' and e[1] == GATE_V003]
    procs = proc_events(ev)
    live = any(e[0] == 'open' and e[1] == a1['plan']['path'] for e in ev)
    ok = r1 == r2 == 'PASS' and not gate and not procs and live
    return ok, {'overlap': r1, 'inactive': r2, 'gate_opens': len(gate), 'process_events': procs, 'hook_live': live,
                'n_open_events': sum(1 for e in ev if e[0] == 'open')}


@test('G14-P8', 'MUST_PASS')
def t_headline_no_memory_fields():
    """A non-S1 batch (HEADLINE, campaign attested inactive, 2 calls, max_active 3) with the no-memory rule is admitted."""
    a = adm_for(G14, core=CORE_INACTIVE, s1_overlap=None, batch='HEADLINE', case='C4T_HEAD', spec=FX.spec_head, n_calls=2,
                rule_fn=lambda r: r.__setitem__('max_active', 3))
    got = run_validate(G14, a)
    return got == 'PASS', {'got': got, 'rule': a['plan_doc']['route_a_admission']}


@test('G14-P9', 'MUST_PASS')
def t_dbp_c2v004b_rules():
    """Every batch rule of DIRECT_BATCH_PARAMS_S45_C2V004B is exactly guard014's bound fields and is admitted by guard014
    (on a synthetic inactive HEADLINE plan carrying it); guard013 refuses each (RAMP_RULE_REQUIRED), so C2V004B is a
    guard014-only parameter set. DIII max_active 4 (its call count), every rss_cap_bytes = RAM."""
    out, ok = {}, True
    for b, bd in sorted(FX.d4b.items()):
        rule = bd['route_a_admission']
        r14 = run_validate(G14, adm_for(G14, core=CORE_INACTIVE, s1_overlap=None, batch='HEADLINE', case='C4T_HEAD',
                                        spec=FX.spec_head, rule=rule))
        r13 = run_validate(G13, adm_for(G13, core=CORE_INACTIVE, s1_overlap=None, batch='HEADLINE', case='C4T_HEAD',
                                        spec=FX.spec_head, rule=rule))
        rss = sorted({c['rss_cap_bytes'] for c in bd['caps_per_case'].values()})
        out[b] = {'keys': sorted(rule), 'max_active': rule['max_active'], 'guard014': r14, 'guard013': r13, 'rss': rss}
        ok = ok and sorted(rule) == ['max_active', 'poll_seconds', 'ramp'] and r14 == 'PASS' and r13 == 'RAMP_RULE_REQUIRED' \
            and rss == [RAM_BYTES]
    ok = ok and FX.d4b['DIII']['route_a_admission']['max_active'] == 4 == FX.d4b['DIII']['n_calls']
    return ok, out


def _ff(code, **kw):
    a = adm_for(G14, **kw)
    got = run_validate(G14, a)
    return got == code, {'got': got, 'want': code}


@test('G14-F1', 'MUST_FAIL')
def t_overlap_headline():
    return _ff('CORE_PRIORITY_ATTESTATION_REQUIRED', batch='HEADLINE', case='C4T_HEAD', spec=FX.spec_head)


@test('G14-F2', 'MUST_FAIL')
def t_overlap_non_s1_case():
    return _ff('S1_OVERLAP_S1_CASE_REQUIRED', case='C4T')


@test('G14-F3', 'MUST_FAIL')
def t_overlap_two_calls():
    return _ff('S1_OVERLAP_ONE_CALL_REQUIRED', n_calls=2)


@test('G14-F4', 'MUST_FAIL')
def t_overlap_replay_mismatch():
    return _ff('S1_OVERLAP_REPLAY_MISMATCH', fill=FX.fill_tamper)


@test('G14-F5', 'MUST_FAIL')
def t_overlap_replay_not_allowlisted():
    kw, want = _custody_variants()['replay_not_allowlisted']
    return _ff(want, **kw)


@test('G14-F6', 'MUST_FAIL')
def t_overlap_replay_api():
    return _ff('S1_OVERLAP_REPLAY_API', replay=FX.replay_bad_api)


@test('G14-F7', 'MUST_FAIL')
def t_overlap_fill_binding():
    return _ff('S1_OVERLAP_FILL_RECORD_BINDING', mutate_plan=lambda p: p['s1'].__setitem__('fill_record', FX.fill_other))


@test('G14-F15', 'MUST_FAIL')
def t_overlap_step2_active():
    return _ff('CORE_PRIORITY_ATTESTATION_REQUIRED', core=dict(CORE_OVERLAP, step2_route_a_inactive=False))


@test('G14-F16', 'MUST_FAIL')
def t_overlap_block_missing():
    return _ff('S1_OVERLAP_ADMISSION_REQUIRED', s1_overlap=None)


@test('G14-F17', 'MUST_FAIL')
def t_overlap_block_schema():
    return _ff('S1_OVERLAP_ADMISSION_SCHEMA', s1_overlap={'schema': 'X', 'replay_module': FX.replay, 'fill_record': FX.fill})


@test('G14-F19', 'MUST_FAIL')
def t_overlap_spec_not_filled():
    return _ff('S1_OVERLAP_SPEC_NOT_FILLED_SPEC', case='S1_UA_C3T')


@test('G14-F20', 'MUST_FAIL')
def t_overlap_replay_refused():
    return _ff('S1_OVERLAP_REPLAY_REFUSED', fill=FX.fill_refuse)


@test('G14-F21', 'MUST_FAIL')
def t_overlap_tail_off():
    return _ff('S1_OVERLAP_TAIL_ON_R5_REQUIRED', mutate_plan=lambda p: p['calls'][0].__setitem__('tail_on', False))


@test('G14-F22', 'MUST_FAIL')
def t_guard_identity():
    """A plan naming guard013 is refused by guard014 (LAUNCHER_GUARD_IDENTITY)."""
    a = adm_for(G14, extra_sources=({'path': G13_PATH, 'sha256': G13_SHA},),
                mutate_plan=lambda p: p.__setitem__('guard', {'path': G13_PATH, 'sha256': G13_SHA}))
    got = run_validate(G14, a)
    return got == 'LAUNCHER_GUARD_IDENTITY', {'got': got}


@test('G14-F23', 'MUST_FAIL')
def t_guard011_refuses_overlap():
    """The same overlap admission under guard011 is refused at L333 (unchanged since guard012)."""
    got = run_validate(G11, adm_for(G11))
    return got == 'CORE_PRIORITY_ATTESTATION_REQUIRED', {'got': got}


@test('G14-F24', 'MUST_FAIL')
def t_guard013_refuses_guard014_plan():
    """A plan naming guard014 with launcher014 is refused by guard013, the guard launcher014 loads: the memory-free rule
    needs the guard014 / launcher015 pair."""
    a = admitted(G13, G13_PATH, L14_PATH, extra_sources=({'path': G14_PATH, 'sha256': sha(rb(G14_PATH))},),
                 mutate_plan=lambda p: p.__setitem__('guard', {'path': G14_PATH, 'sha256': sha(rb(G14_PATH))}))
    got = run_validate(G13, a)
    return got == 'LAUNCHER_GUARD_IDENTITY', {'got': got}


@test('G14-F25', 'MUST_FAIL')
def t_plan_with_free_25_refused():
    """Design (V006 A172 'as guard014 requires'): a plan whose route_a_admission still carries the C2V004 memory fields
    (free 25, source memory_pressure, exemption false; plan and root copy equal) is REFUSED by guard014 with
    MEMORY_ADMISSION_FIELD_REFUSED, and so is each memory field alone; guard013 admits the full C2V004 form (control: the
    fixture is otherwise admissible)."""
    full = run_validate(G14, adm_for(G14, rule=FX.rule13))
    ctl = run_validate(G13, adm_for(G13, rule=FX.rule13))
    single = {}
    for k in MEM_FIELDS:
        single[k] = run_validate(G14, adm_for(G14, rule=dict(FX.rule14, **{k: FX.rule13[k]})))
    ok = full == 'MEMORY_ADMISSION_FIELD_REFUSED' and ctl == 'PASS' and all(v == 'MEMORY_ADMISSION_FIELD_REFUSED' for v in single.values())
    return ok, {'guard014_full_c2v004_rule': full, 'guard013_control': ctl, 'single_field': single}


# ================================================================================================ launcher015 tests
L14_HEADER = ["# c2v014 = launcher013 (620a44da) with the two guard constants changed only: the guard is guard013 (V006 A166). The",
              "# machine lock (launcher012's file, absolute path) and the memory_pressure ramp (all batches) are launcher013's, unchanged."]
L15_HEADER = ["# c2v015 = launcher014 (5d6af4a7) with its memory terms removed (V006 A172): no memory_free / memory_pressure read, no",
              "# free term in decision or in the admission log, no nice >= 10 requirement; the guard is guard014. The machine lock,",
              "# max_active, the first-iteration ramp, single-thread BLAS, normal QoS, caffeinate and drain-on-failure are launcher014's."]
L14_REMOVED_BODY = [
    "import argparse, fcntl, hashlib, json, os, re, signal, subprocess, sys, time, types",
    "GUARD_PATH=HERE/'step4_guard_c2v013.py'",
    "GUARD_SHA256='%s'" % G13_SHA,
    "def memory_free():",
    "    try:",
    "        s=subprocess.check_output(['/usr/bin/memory_pressure'],text=True,stderr=subprocess.STDOUT,timeout=10)",
    "        m=re.findall(r'^System-wide memory free percentage:\\s*(\\d+)%\\s*$',s,re.M)",
    "        return int(m[0]) if len(m)==1 and 0<=int(m[0])<=100 else None",
    "    except Exception:return None",
    "def decision(*,active_route_a,free,previous_iteration,first,max_active):",
    "    return type(active_route_a) is int and 0<=active_route_a<max_active and type(free) is int and 25<=free<=100 and (first or previous_iteration is True)",
    "    G.require(os.getpriority(os.PRIO_PROCESS,0)>=10,'NICE_10_REQUIRED')",
    "                    free=memory_free()",
    "                    go=decision(active_route_a=count,free=free,previous_iteration=prev_ok,first=previous is None,max_active=plan['route_a_admission']['max_active'])",
    "                    print(json.dumps({'event':'step4_admission_decision','case':pending[0]['case'],'free_percent':free,'active_route_a':count,'previous_first_iteration':prev_ok,'admitted':go}),flush=True)",
]
L15_ADDED_BODY = [
    "import argparse, fcntl, hashlib, json, os, signal, subprocess, sys, time, types",
    "GUARD_PATH=HERE/'step4_guard_c2v014.py'",
    "GUARD_SHA256='@G14@'",
    "def decision(*,active_route_a,previous_iteration,first,max_active):",
    "    return type(active_route_a) is int and 0<=active_route_a<max_active and (first or previous_iteration is True)",
    "                    go=decision(active_route_a=count,previous_iteration=prev_ok,first=previous is None,max_active=plan['route_a_admission']['max_active'])",
    "                    print(json.dumps({'event':'step4_admission_decision','case':pending[0]['case'],'active_route_a':count,'previous_first_iteration':prev_ok,'admitted':go}),flush=True)",
]


@test('L15-P1', 'MUST_PASS')
def t_launcher_diff_scope():
    """launcher014 -> launcher015 removes exactly memory_free, its call, the free term (decision and log), the nice >= 10
    line and the now-unused re import, re-pins the guard to guard014 and replaces the header comment; nothing else.
    runtime_settings keeps single-thread BLAS; normal_qos, acquire_lock, monitor_argv, systemic, main are AST-identical."""
    t15 = rb(L15_PATH).decode()
    t14 = rb_pinned(L14_PATH, L14_SHA).decode()
    diff = [ln for ln in difflib.unified_diff(t14.splitlines(keepends=True), t15.splitlines(keepends=True), n=0)
            if ln[:1] in '+-' and not ln.startswith(('+++', '---'))]
    removed = sorted(ln[1:].rstrip('\n') for ln in diff if ln.startswith('-'))
    added = sorted(ln[1:].rstrip('\n') for ln in diff if ln.startswith('+'))
    want_removed = sorted(L14_HEADER + L14_REMOVED_BODY)
    want_added = sorted(L15_HEADER + [x.replace('@G14@', sha(rb(G14_PATH))) for x in L15_ADDED_BODY])
    d14 = {n.name: ast.dump(n) for n in ast.parse(t14).body if isinstance(n, ast.FunctionDef)}
    d15 = {n.name: ast.dump(n) for n in ast.parse(t15).body if isinstance(n, ast.FunctionDef)}
    same = sorted(k for k in d15 if d14.get(k) == d15[k])
    changed = sorted(k for k in set(d14) | set(d15) if d14.get(k) != d15.get(k))
    names15 = {n.id for n in ast.walk(ast.parse(t15)) if isinstance(n, ast.Name)} | \
              {n.attr for n in ast.walk(ast.parse(t15)) if isinstance(n, ast.Attribute)}
    ok = (removed == want_removed and added == want_added and changed == ['decision', 'memory_free', 'runtime_settings', 'worker']
          and {'normal_qos', 'acquire_lock', 'monitor_argv', 'systemic', 'main', 'read_progress', 'first_iteration',
               'route_a_finished'} <= set(same)
          and 'memory_pressure' not in t15.split('\n', 4)[4] and 'getpriority' not in names15 and 'memory_free' not in names15
          and 'nice' not in t15.split('\n', 4)[4] and "'SINGLE_THREAD_BLAS_REQUIRED'" in t15)
    return ok, {'removed_n': len(removed), 'added_n': len(added), 'defs_changed': changed,
                'removed_ok': removed == want_removed, 'added_ok': added == want_added}


@test('L15-P2', 'MUST_PASS')
def t_launcher_loads_guard014():
    """launcher015 loads guard014 by its sha; the lock and interpreter are launcher014's; decision equals launcher014's
    at every admitted free reading (25..100) on the full grid, so only the free term is gone."""
    m15 = load_bytes_module(L15_PATH, sha(rb(L15_PATH)), '_t_launcher015')
    m14 = load_bytes_module(L14_PATH, L14_SHA, '_t_launcher014')
    grid = [dict(active_route_a=a, previous_iteration=p, first=fi, max_active=mx)
            for a in (0, 1, 2, 3, '1', None) for p in (None, False, True) for fi in (False, True) for mx in (1, 2, 3)]
    same = all(m15.decision(**g) == m14.decision(free=f, **g) for g in grid for f in range(25, 101))
    blocked14 = all(m14.decision(free=f, **g) is False for g in grid for f in (None, 0, 24, 101, '80'))
    ok = (m15.G.__file__ == G14_PATH and sha(m15.GUARD_BYTES) == sha(rb(G14_PATH))
          and hasattr(m15.G, 'MEMORY_ADMISSION_FIELDS') and hasattr(m15.G, 'core_priority_admission')
          and not hasattr(m15, 'memory_free') and str(m15.LOCK) == str(m14.LOCK) and m15.PYTHON == m14.PYTHON
          and m15.BLAS == m14.BLAS and same and blocked14)
    return ok, {'guard': m15.G.__file__, 'lock': str(m15.LOCK), 'decision_equal_at_free_25_100': same, 'grid': len(grid),
                'launcher014_false_when_free_unknown_or_low': blocked14}


@test('L15-F1', 'MUST_FAIL')
def t_launcher_tampered_guard():
    d = tmpdir('l15_tamper')
    wx(d / 'step4_launcher_c2v015.py', rb(L15_PATH))
    wx(d / 'step4_guard_c2v014.py', rb(G14_PATH) + b'\n# tampered\n')
    try:
        raw = rb(str(d / 'step4_launcher_c2v015.py'))
        m = types.ModuleType('_t_l15_tampered')
        m.__file__ = str(d / 'step4_launcher_c2v015.py')
        exec(compile(raw, m.__file__, 'exec'), m.__dict__)
        return False, 'loaded'
    except PermissionError as exc:
        return str(exc) == 'GUARD_BOOTSTRAP_HASH_MISMATCH', str(exc)


def os_proxy(prio, calls):
    px = types.ModuleType('_t_os_proxy')
    px.__dict__.update(os.__dict__)

    def getpriority(*a):
        calls.append(a)
        return prio
    px.getpriority = getpriority
    return px


@test('L15-P6', 'MUST_PASS')
def t_runtime_settings():
    """runtime_settings drops only the nice requirement: with a synthetic priority 0 (an os proxy; the real priority is
    neither read nor changed) launcher015 passes with single-thread BLAS, never reads the priority, and refuses without
    BLAS (SINGLE_THREAD_BLAS_REQUIRED); launcher014 refuses NICE_10_REQUIRED at priority 0 and passes at 10."""
    m15 = load_bytes_module(L15_PATH, sha(rb(L15_PATH)), '_t_l15_rs')
    m14 = load_bytes_module(L14_PATH, L14_SHA, '_t_l14_rs')
    saved = {k: os.environ.get(k) for k in BLAS_KEYS}
    out, c15, c14 = {}, [], []

    def rs(m):
        try:
            m.runtime_settings()
            return 'PASS'
        except Exception as exc:
            return code_of(exc)
    try:
        for k in BLAS_KEYS:
            os.environ[k] = '1'
        m15.os, m14.os = os_proxy(0, c15), os_proxy(0, c14)
        out['l15_prio0_blas'] = rs(m15)
        out['l14_prio0_blas'] = rs(m14)
        m14.os = os_proxy(10, c14)
        out['l14_prio10_blas'] = rs(m14)
        os.environ.pop('OMP_NUM_THREADS')
        out['l15_prio0_no_blas'] = rs(m15)
        out['l14_prio10_no_blas'] = rs(m14)
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    ok = (out == {'l15_prio0_blas': 'PASS', 'l14_prio0_blas': 'NICE_10_REQUIRED', 'l14_prio10_blas': 'PASS',
                  'l15_prio0_no_blas': 'SINGLE_THREAD_BLAS_REQUIRED', 'l14_prio10_no_blas': 'SINGLE_THREAD_BLAS_REQUIRED'}
          and c15 == [] and len(c14) == 3)
    return ok, dict(out, launcher015_priority_reads=len(c15), launcher014_priority_reads=len(c14))


# ---------------------------------------------------------------------------------------------- the worker harness
class HarnessStop(Exception):
    pass


class FakeProc:
    def __init__(self, fn):
        self.fn = fn

    def poll(self):
        return self.fn()


class World:
    """One synthetic batch: plan, calls, the monitor processes' state, and a step script run at each launcher sleep."""
    def __init__(self, tag, n_calls, max_active, script, mem_text=None, stop_after=None, disk_refuse=None,
                 revoke_at=None):
        self.dir = tmpdir('w_' + tag)
        os.mkdir(self.dir / 'out')
        self.calls = []
        for k in range(n_calls):
            od = str(self.dir / 'out' / ('call_%d' % k))
            self.calls.append({'case': 'CASE_%d' % k, 'outdir': od, 'receipt': od + '.receipt.json',
                               'monitor_log': od + '.monitor.log', 'driver': {'path': DRIVER[0], 'sha256': DRIVER[1]},
                               'spec': {'path': str(self.dir / ('spec_%d.json' % k)), 'sha256': '0' * 64},
                               'wall_cap_s': 100800, 'rss_cap_bytes': RAM_BYTES, 'output_cap_bytes': 85899345920})
        self.by_outdir = {c['outdir']: c['case'] for c in self.calls}
        self.case = {c['case']: c for c in self.calls}
        self.plan = {'launcher_log': str(self.dir / 'out' / 'batch.launcher.log'), 'calls': self.calls,
                     'monitor': {'path': MONITOR[0], 'sha256': MONITOR[1]},
                     'route_a_admission': {'max_active': max_active, 'poll_seconds': 60,
                                           'ramp': 'previous_first_completed_route_a_iteration'}}
        wx(self.plan['launcher_log'], b'')
        self.script, self.mem_text, self.stop_after = script, mem_text, stop_after
        self.disk_refuse, self.revoke_at = disk_refuse, revoke_at
        self.rc, self.started, self.requests, self.sleeps = {}, [], [], []
        self.n_validate, self.step, self.forced = 0, 0, False
        self.refusal = None

    # ---- stubs
    def fake_validate(self, plan_ref, producer, **kw):
        self.n_validate += 1
        if self.revoke_at is not None and self.n_validate >= self.revoke_at:
            raise self.refusal('SYNTHETIC_ADMISSION_REVOKED')
        return self.plan, {}

    def fake_disk(self, plan, call=None):
        if call is not None and self.disk_refuse is not None and call['case'] == self.disk_refuse:
            raise self.refusal('DISK_START_BOUND')
        return {'free_bytes': 1, 'required_bytes': 0, 'volume': 'SYNTHETIC'}

    def on_sleep(self, s):
        self.sleeps.append(s)
        self.step += 1
        if self.stop_after is not None and self.step == self.stop_after:
            raise HarnessStop('synthetic stop after %d polls' % self.step)
        fn = self.script.get(self.step)
        if fn:
            fn(self)
        if self.step > 40 and not self.forced:          # safety net: end every started monitor
            self.forced = True
            for c in self.started:
                if self.rc.get(c) is None:
                    self.rc[c] = 0

    # ---- monitor-side effects (each file written once, by exclusive create)
    def it1(self, case):
        od = Path(self.case[case]['outdir']) / 'stages/01_route_a/attempt_000'
        os.makedirs(od)
        wx(od / 'progress.jsonl', b'{"stage": "iteration_completed", "iteration": 0}\n')

    def ra_done(self, case):
        wx(Path(self.case[case]['outdir']) / 'progress.jsonl', b'{"stage": "route_a", "event": "finished"}\n')

    def finish(self, case, status='FINISHED', rc=0):
        wj(self.case[case]['receipt'], {'status': status, 'exit_code': rc})
        self.rc[case] = rc


def make_shim(world):
    sh = types.ModuleType('_t_subprocess_shim')
    for k in ('DEVNULL', 'PIPE', 'STDOUT', 'CalledProcessError', 'TimeoutExpired', 'CompletedProcess'):
        setattr(sh, k, getattr(subprocess, k))

    def Popen(argv, **kw):
        world.requests.append(list(argv))
        if list(argv[:3]) == ['/usr/bin/caffeinate', '-i', '-w']:
            return FakeProc(lambda: None)
        if list(argv[:2]) == ['/usr/bin/caffeinate', '-i'] and '--outdir' in argv:
            od = argv[argv.index('--outdir') + 1]
            case = world.by_outdir[od]
            os.mkdir(od)                                  # the monitor creates its outdir
            world.started.append(case)
            return FakeProc(lambda c=case: world.rc.get(c))
        return subprocess.Popen(argv, **kw)              # anything else: real, so the audit hook blocks and records it

    def run(argv, **kw):
        world.requests.append(list(argv))
        if list(argv[:2]) == ['/usr/sbin/taskpolicy', '-B']:
            return subprocess.CompletedProcess(argv, 0, b'', b'')
        return subprocess.run(argv, **kw)

    def check_output(argv, **kw):
        world.requests.append(list(argv))
        if list(argv) == ['/usr/bin/memory_pressure'] and world.mem_text is not None:
            return world.mem_text                       # readable: synthetic text, nothing executed
        return subprocess.check_output(argv, **kw)       # real request: the audit hook blocks it (unreadable)
    sh.Popen, sh.run, sh.check_output = Popen, run, check_output
    return sh


def run_worker(which, world, *, nice_proxy=False):
    path, want = (L15_PATH, sha(rb(L15_PATH))) if which == 'L15' else (L14_PATH, L14_SHA)
    m = load_bytes_module(path, want, '_t_worker_' + which)
    world.refusal = m.G.Refusal
    m.LOCK = world.dir / 'STEP4_MACHINE_LOCK_SYNTHETIC'
    m.subprocess = make_shim(world)
    m.time = types.SimpleNamespace(sleep=world.on_sleep)
    m.G.validate = world.fake_validate
    m.G.disk_admission = world.fake_disk
    if nice_proxy:                                     # launcher014 only: its nice >= 10 check reads a synthetic 10
        m.os = os_proxy(10, [])
    saved = {k: os.environ.get(k) for k in BLAS_KEYS}
    buf = io.StringIO()
    for k in BLAS_KEYS:
        os.environ[k] = '1'
    try:
        def go():
            with contextlib.redirect_stdout(buf):
                return m.worker({'path': str(world.dir / 'plan.synthetic.json'), 'sha256': '0' * 64})
        rc, ev = audited(go)
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    lines = [json.loads(x) for x in buf.getvalue().splitlines() if x.startswith('{')]
    return {'rc': rc, 'decisions': [x for x in lines if x.get('event') == 'step4_admission_decision'],
            'finished': [x for x in lines if x.get('event') == 'step4_finished'], 'started': list(world.started),
            'requests': world.requests, 'audit_process_events': proc_events(ev), 'n_validate': world.n_validate,
            'sleeps': len(world.sleeps), 'forced': world.forced, 'wdir': str(world.dir)}


def normalized(r):
    """The run with free_percent and memory_pressure requests dropped and the world folder replaced by <W>."""
    return {'rc': r['rc'], 'started': r['started'], 'finished': r['finished'], 'n_validate': r['n_validate'],
            'sleeps': r['sleeps'], 'forced': r['forced'],
            'decisions': [{k: v for k, v in d.items() if k != 'free_percent'} for d in r['decisions']],
            'requests': [[str(a).replace(r['wdir'], '<W>') for a in x] for x in r['requests']
                         if x != ['/usr/bin/memory_pressure']]}


def S(*fns):
    def f(w):
        for fn in fns:
            fn(w)
    return f


def scenarios():
    """name -> (World kwargs, script). Each script step runs at that launcher sleep (one per 60-s poll)."""
    return {
        'ramp_two_calls': (dict(n_calls=2, max_active=2), {
            2: lambda w: w.it1('CASE_0'),
            3: S(lambda w: w.ra_done('CASE_0'), lambda w: w.it1('CASE_1'), lambda w: w.ra_done('CASE_1'),
                 lambda w: w.finish('CASE_0'), lambda w: w.finish('CASE_1'))}),
        'max_active_cap': (dict(n_calls=3, max_active=1), {
            1: lambda w: w.it1('CASE_0'),
            2: lambda w: w.ra_done('CASE_0'),
            3: S(lambda w: w.it1('CASE_1'), lambda w: w.ra_done('CASE_1'), lambda w: w.finish('CASE_0')),
            4: S(lambda w: w.it1('CASE_2'), lambda w: w.ra_done('CASE_2'), lambda w: w.finish('CASE_1'),
                 lambda w: w.finish('CASE_2'))}),
        'predecessor_ended_before_first_iteration': (dict(n_calls=2, max_active=2), {
            1: lambda w: w.finish('CASE_0')}),
        'systemic_receipt': (dict(n_calls=2, max_active=2), {
            1: S(lambda w: w.it1('CASE_0'), lambda w: w.finish('CASE_0', status='STOPPED_RSS_CAP', rc=1))}),
        'disk_start_bound': (dict(n_calls=2, max_active=2, disk_refuse='CASE_1'), {
            1: lambda w: w.it1('CASE_0'),
            3: S(lambda w: w.ra_done('CASE_0'), lambda w: w.finish('CASE_0'))}),
        'admission_revoked': (dict(n_calls=2, max_active=2, revoke_at=5), {
            1: lambda w: w.it1('CASE_0'),
            3: S(lambda w: w.ra_done('CASE_0'), lambda w: w.finish('CASE_0'))}),
        'signal_drain': (dict(n_calls=2, max_active=2), {
            1: lambda w: signal.getsignal(signal.SIGTERM)(signal.SIGTERM, None),
            3: S(lambda w: w.it1('CASE_0'), lambda w: w.ra_done('CASE_0'), lambda w: w.finish('CASE_0'))}),
        'scientific_failure_retained': (dict(n_calls=2, max_active=2), {
            1: lambda w: w.it1('CASE_0'),
            2: S(lambda w: w.ra_done('CASE_0'), lambda w: w.finish('CASE_0', status='FAILED', rc=1)),
            3: S(lambda w: w.it1('CASE_1'), lambda w: w.ra_done('CASE_1'), lambda w: w.finish('CASE_1'))}),
    }


def run_scenario(which, name, **extra):
    kw, script = scenarios()[name]
    w = World('%s_%s' % (which, name), script=script, **dict(kw, **extra))
    return run_worker(which, w, nice_proxy=(which == 'L14'))


@test('L15-P3', 'MUST_PASS')
def t_memory_pressure_unreadable():
    """launcher015 starts the first call with memory_pressure unreadable (the shim passes any /usr/bin/memory_pressure
    request to the real subprocess, where the audit hook blocks it): no memory request is made and the audit hook records
    no process creation at all. Control: launcher014 under the same condition requests memory_pressure at every poll
    (each blocked by the hook, so it is never executed), reads None and starts nothing."""
    script = {1: S(lambda w: w.it1('CASE_0'), lambda w: w.ra_done('CASE_0'), lambda w: w.finish('CASE_0'))}
    r15 = run_worker('L15', World('l15_memx', 1, 1, script, mem_text=None))
    r14 = run_worker('L14', World('l14_memx', 1, 1, script, mem_text=None, stop_after=3), nice_proxy=True)
    mp15 = [x for x in r15['requests'] if x and x[0] == '/usr/bin/memory_pressure']
    mp14 = [x for x in r14['requests'] if x and x[0] == '/usr/bin/memory_pressure']
    hooked14 = [e for e in r14['audit_process_events'] if 'memory_pressure' in e[1] + e[2]]
    ok = (r15['rc'] == 0 and r15['started'] == ['CASE_0'] and r15['decisions'][0]['admitted'] is True and not mp15
          and r15['audit_process_events'] == [] and 'free_percent' not in r15['decisions'][0]
          and r14['started'] == [] and len(mp14) >= 2 and len(hooked14) == len(mp14)
          and all(d['admitted'] is False and d['free_percent'] is None for d in r14['decisions']))
    return ok, {'l15': {'rc': r15['rc'], 'started': r15['started'], 'memory_requests': len(mp15),
                        'audit_process_events': r15['audit_process_events'], 'first_decision': r15['decisions'][0]},
                'l14_control': {'rc': r14['rc'], 'started': r14['started'], 'memory_requests': len(mp14),
                                'blocked_by_hook': len(hooked14), 'decisions': r14['decisions']}}


@test('L15-P4', 'MUST_PASS')
def t_ramp_waits():
    """The first-iteration ramp stays: the second call is not admitted until the first call's first route-A iteration
    is logged (decision admitted False with previous_first_iteration False), then starts at the next poll."""
    r = run_scenario('L15', 'ramp_two_calls')
    d = [(x['case'], x['previous_first_iteration'], x['admitted']) for x in r['decisions']]
    ok = (r['rc'] == 0 and r['started'] == ['CASE_0', 'CASE_1'] and ('CASE_1', False, False) in d
          and d.index(('CASE_1', False, False)) < d.index(('CASE_1', True, True)) and r['audit_process_events'] == [])
    return ok, {'decisions': d, 'started': r['started'], 'rc': r['rc']}


@test('L15-P5', 'MUST_PASS')
def t_nonmemory_identical():
    """Non-memory behaviour is launcher014's: on every scenario (ramp, max_active cap, predecessor ended, systemic
    receipt, disk start bound, admission revoked, signal drain, retained scientific failure) launcher014 (memory readable
    at 80 %, nice check satisfied) and launcher015 give the same exit code, starts, admission decisions (free_percent
    aside), finish record, process requests (memory_pressure aside), validations and polls. Neither creates a real process."""
    out, ok = {}, True
    for name in scenarios():
        r14 = run_scenario('L14', name, mem_text='System-wide memory free percentage: 80%\n')
        r15 = run_scenario('L15', name)
        n14, n15 = normalized(r14), normalized(r15)
        same = n14 == n15 and not r14['audit_process_events'] and not r15['audit_process_events'] and not r15['forced']
        out[name] = {'same': same, 'rc': r15['rc'], 'started': r15['started'],
                     'failures': [(f['reason'], f['case']) for f in (r15['finished'][0]['failures'] if r15['finished'] else [])]}
        ok = ok and same
    return ok, out


@test('L15-F2', 'MUST_FAIL')
def t_predecessor_ended_fail_fast():
    """launcher015 still fails fast when the predecessor ends before its first route-A iteration: the worker drains with
    PREDECESSOR_ENDED_BEFORE_FIRST_ITERATION, the second call never starts, exit 1."""
    r = run_scenario('L15', 'predecessor_ended_before_first_iteration')
    f = r['finished'][0]['failures'] if r['finished'] else []
    ok = (r['rc'] == 1 and r['started'] == ['CASE_0']
          and any('PREDECESSOR_ENDED_BEFORE_FIRST_ITERATION' in (x.get('detail') or '') for x in f))
    return ok, {'rc': r['rc'], 'started': r['started'], 'failures': f}


@test('L15-F3', 'MUST_FAIL')
def t_max_active_binds():
    """max_active stays: with max_active 1 the second call waits while the first is in route A even after its first
    iteration (admitted False, active_route_a 1), and starts once route A has finished."""
    r = run_scenario('L15', 'max_active_cap')
    d = [(x['case'], x['active_route_a'], x['previous_first_iteration'], x['admitted']) for x in r['decisions']]
    ok = r['rc'] == 0 and ('CASE_1', 1, True, False) in d and r['started'] == ['CASE_0', 'CASE_1', 'CASE_2']
    return ok, {'decisions': d, 'started': r['started']}


# ================================================================================================ main
def main():
    global RUN, FX, G11, G13, G14
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    a = ap.parse_args()
    RUN = Path(os.path.abspath(a.run_dir))
    os.mkdir(str(RUN))
    t0 = time.time()
    started = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    G11 = load_bytes_module(G11_PATH, G11_SHA, '_t_guard011')
    G13 = load_bytes_module(G13_PATH, G13_SHA, '_t_guard013')
    G14 = load_bytes_module(G14_PATH, sha(rb(G14_PATH)), '_t_guard014')
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
    summary = {'schema': 'UNT_STEP4_GUARD014_TEST_RESULTS_C2V001', 'started_utc': started,
               'finished_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'seconds': round(time.time() - t0, 1),
               'python': sys.version.split()[0], 'interpreter': sys.executable,
               'files_sha256': {p: sha(rb(p)) for p in (G14_PATH, L15_PATH, str(Path(__file__).resolve()), DBP4B[0])},
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
