"""Synthetic tests for the S1 path c2v001 (MUST_PASS / MUST_FAIL). Target-free; launches nothing.

  python3 -I -B test_s1_path_c2v001.py --run-dir <a new directory>

Every fixture is synthetic and is written inside --run-dir (created here; it must not exist). Read-only inputs are the
pinned registered files the library names (P5, CB, coordinate spec, CORE, ORC, guard011, launcher012, root monitor,
driver r5 (hashed only), gate v003, params C2V003A, compare r11, V005 compare, the DDO154 row-radius binding) and the
campaign run config CFG d9241676. The four 0620 controls are exercised through the real guard011 code on synthetic
admission inputs; the machine gate through the real gate v003 Gate class with a synthetic probe and clock; the reader
through the real compare r11 and V005 compare functions on synthetic result trees. No subprocess is started except
the CLI wrapper tests (python -I -B on the wrappers in this folder; they start no further process).
Results: <run-dir>/TEST_RESULTS.json and <run-dir>/TEST_LOG.txt (exclusive create).
"""
import argparse
import copy
import hashlib
import json
import math
import os
import subprocess
import sys
import time
import traceback
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIB_PATH = HERE / 's1_path_lib_c2v001.py'
CFG_PIN = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sched_s45_c2/v003/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V003.json',
           'sha256': 'd9241676c3b7b32bd3067a55bdfb7821ebc33a68adbdc011ab4e4c58b6e50a4d'}
V6_PATH = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
           'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md')
REG_V002 = HERE / 'S1_REGISTRATION_DRAFT_C2V002.md'
PY = sys.executable

L = None
RUN = None
FX = None
RESULTS = []
LOG = []


def load_lib():
    raw = LIB_PATH.read_bytes()
    m = types.ModuleType('s1_path_lib_c2v001')
    m.__file__ = str(LIB_PATH)
    exec(compile(raw, str(LIB_PATH), 'exec'), m.__dict__)
    return m, hashlib.sha256(raw).hexdigest()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def wjson(path, obj, indent=1):
    data = (json.dumps(obj, indent=indent, sort_keys=True, allow_nan=False) + '\n').encode()
    return L.write_exclusive(str(path), data)


def wbytes(path, data):
    return L.write_exclusive(str(path), data)


def mkdir(p):
    os.mkdir(str(p))
    return Path(p)


def log(s):
    LOG.append(s)


def record(tid, kind, ok, detail):
    RESULTS.append({'id': tid, 'kind': kind, 'result': 'PASS' if ok else 'FAIL', 'detail': detail})
    log('%-5s %-9s %s  %s' % ('ok' if ok else 'FAIL', kind, tid, str(detail)[:300]))


def test(tid, kind):
    def deco(fn):
        fn._tid, fn._kind = tid, kind
        TESTS.append(fn)
        return fn
    return deco


TESTS = []


def expect_refusal(fn, code):
    try:
        fn()
    except L.Refusal as exc:
        return exc.code == code, 'refused %s' % exc.code
    return False, 'no refusal'


# ================================================================================================ fixtures
class Fx:
    pass


def build_fixtures():
    fx = Fx()
    fx.root = mkdir(RUN / 'fx')
    st = L.load_static()
    fx.st = st
    coord = st['coord']
    fx.seed = dict(coord['trial_point']['engine_seed_theta'])
    off = dict(fx.seed)
    off['common_scale_s'] = fx.seed['common_scale_s'] * 1.1
    off['gamma_over_Eref'] = fx.seed['gamma_over_Eref'] * 1.25
    off['ell_F_m'] = fx.seed['ell_F_m'] * 0.9
    fx.off = off
    # synthetic per-point certificates
    cd = mkdir(fx.root / 'certs')
    fx.certs = {}
    for k in ('c4t_eps', 'c4t_lo', 'c3t_eps', 'c3t_lo', 'c4t_seed_eps', 'c4t_seed_lo'):
        fx.certs[k] = wjson(cd / (k + '.json'), {'schema': 'SYNTHETIC_TEST_CERTIFICATE', 'name': k})
    fx.phase1 = wjson(fx.root / 'phase1_record.json',
                      {'schema': 'SYNTHETIC_PHASE1_RECORD', 'theta_keys': [L.theta_key(off), L.theta_key(fx.seed)]})
    fx.cfg = L.pinned_json(CFG_PIN)
    fx.ua = {}
    fx.base = {}
    for tag, th, cert in (('off', off, ('c4t_eps', 'c4t_lo')), ('seed', fx.seed, ('c4t_seed_eps', 'c4t_seed_lo'))):
        fx.ua[tag] = wjson(fx.root / ('ua_%s.json' % tag), ua_doc(th, fx.phase1))
        fx.base[tag] = wjson(fx.root / ('base_%s.spec.json' % tag), base_spec(th, fx.certs[cert[0]], fx.certs[cert[1]]))
    fx.c3t_certs = {'eps_certificate': fx.certs['c3t_eps'], 'lo_certificate': fx.certs['c3t_lo']}
    fx.fill = {}
    for tag in ('off', 'seed'):
        d = mkdir(fx.root / ('fill_' + tag))
        rec = L.fill(fx.ua[tag], fx.base[tag], CFG_PIN, c3t_certs=fx.c3t_certs, out_dir=str(d))
        fx.fill[tag] = {'rec': rec, 'pin': rec['record']}
    # registration + synthetic V006 that names its sha
    fx.reg = wbytes(fx.root / 'S1_REGISTRATION_SYNTHETIC.md', b'# synthetic S1 registration for tests\n')
    fx.v6 = wbytes(fx.root / 'V006_SYNTHETIC.md', ('## A999: S1 registration entered by sha %s\n' % fx.reg['sha256']).encode())
    fx.v6_without = wbytes(fx.root / 'V006_SYNTHETIC_WITHOUT.md', b'## A999: nothing entered\n')
    fx.lcfg = {s: wjson(fx.root / ('launch_cfg_%s.json' % s.lower()),
                        {'schema': L.SCHEMA_LAUNCH_CFG, 'campaign_state': s, 'step2_route_a_state': 'INACTIVE'})
               for s in ('INACTIVE', 'ACTIVE')}
    fx.lcfg_step2 = wjson(fx.root / 'launch_cfg_step2_active.json',
                          {'schema': L.SCHEMA_LAUNCH_CFG, 'campaign_state': 'INACTIVE', 'step2_route_a_state': 'ACTIVE'})
    build_g11(fx)
    build_reader(fx)
    return fx


def ua_doc(theta, phase1):
    return {'schema': L.SCHEMA_UA_POINT, 'theta': theta, 'theta_key': L.theta_key(theta), 'phase1_record': phase1,
            'coordinate_mode': 'DDO154_DISTANCE_FIXED_AT_REGISTERED'}


def base_spec(theta, eps, lo):
    st = FX_ST()
    num = copy.deepcopy(L.pinned_json(CFG_PIN)['numerics']['block'])
    num['uv_tail']['eps_certificate'] = eps
    num['uv_tail']['lo_certificate'] = lo
    ph = {'Eref_J': theta['Eref_base_J'], 'entropy_K_factor': theta['entropy_K_factor'], 'inclination_deg': 66.0}
    ph.update(L.mapped_physical(theta))
    spec = {'schema': 'UNT_GALAXY_M0_FORWARD_CALL_C2V001', 'galaxy': 'DDO154', 'admit': {},
            'coefficients': st['p5']['anchor']['coefficients'], 'physical': ph, 'numerics': num,
            'reference_compare': False, 'label': ''}
    spec['label'] = 'DDO154 cx2v006 theta %s; point %s' % (L.theta_key(theta)[:16], L.digest(L.point_identity(spec))[:16])
    return spec


_ST = {}


def FX_ST():
    if 'st' not in _ST:
        _ST['st'] = L.load_static()
    return _ST['st']


# ---------------------------------------------------------------------------------------------- guard011 fixtures
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
exec(compile(ast.Module(body=_keep, type_ignores=[]), '<s1-test-core-validate_block>', 'exec'), _ns)
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


def build_g11(fx):
    g = mkdir(fx.root / 'g11')
    fx.g = g
    G = L.load_guard()
    fx.G = G
    AUTH = G.AUTHORITY
    v = {}
    v['compare'] = wbytes(g / 'compare_dummy.txt', b'synthetic compare bytes\n')
    v['addendum'] = wbytes(g / 'addendum_dummy.md', b'synthetic frozen addendum\n')
    v['case_block'] = wbytes(g / 'case_block_dummy.json', b'{"synthetic": true}\n')
    v['prereg'] = wjson(g / 'prereg.json', {'binding_inputs': {'case_block': v['case_block']}})
    v['seal'] = wjson(g / 'seal.json', {'sealed_by': AUTH, 'prereg': v['prereg'], 'compare': v['compare'],
                                        'driver': {'sha256': L.R5_SHA}, 'frozen_addendum': v['addendum']})
    fx.verdict_doc = {'schema': 'SYN_VERDICT_SCHEMA', 'test_mode': False, 'decision': {'tests_read': True, 'outcome': 'ADOPT_TAIL'},
                      'script_sha256': v['compare']['sha256'], 'prereg': v['prereg'], 'case_block': v['case_block']}
    v['verdict'] = wjson(g / 'verdict.json', fx.verdict_doc)
    fx.v007 = v
    mods = {}
    mods['context'] = wbytes(g / 'syn_context.py', (CONTEXT_SRC % (L.PINS['CORE'][0], L.PINS['CORE'][1])).encode())
    mods['direct'] = wbytes(g / 'syn_direct_context.py', DIRECT_SRC.encode())
    mods['custody'] = wbytes(g / 'syn_custody_deriver.py', b'def derive_custody(**kw):\n    return {}\n')
    mods['enumerator'] = wbytes(g / 'syn_state_enumerator.py', b'def enumerate_states(**kw):\n    return []\n')
    mods['producer'] = wbytes(g / 'syn_producer.py', b'def produce(**kw):\n    return None\n')
    fx.mods = mods
    reg = wjson(g / 'cert_registry.json', {'points': {}})
    rev = wjson(g / 'cert_policy_review.json', {'schema': 'SYNTHETIC'})
    block = copy.deepcopy(fx.cfg['numerics']['block'])
    fx.c1 = wjson(g / 'config_c1.json', {'numerics': {'verdict_artifact': v['verdict'], 'sealed_prereg': v['prereg'],
                                                       'compare': v['compare'], 'block': block},
                                          'tail_readiness': {'certificate_registry': reg, 'certificate_policy_review': rev,
                                                             'custody_deriver': mods['custody'],
                                                             'state_enumerator': mods['enumerator'],
                                                             'approved_certificate_producers': [mods['producer']]}})
    fx.seal_tuple = (v['compare']['sha256'], v['prereg']['sha256'], v['addendum']['sha256'], 'SYN_VERDICT_SCHEMA',
                     v['verdict']['sha256'])
    fx.policy = {'ok': wbytes(g / 'syn_policy_ok.py', (POLICY_SRC % repr({fx.seal_tuple})).encode()),
                 'empty': wbytes(g / 'syn_policy_empty.py', (POLICY_SRC % 'set()').encode())}
    fx.out_root = str(mkdir(g / 'out'))      # stands in for the External1 step-4 run root (never created there)
    fx.n_adm = 0


def sources_for(fx, policy, drop_driver=False):
    s = {L.PINS[k][0]: L.PINS[k][1] for k in ('LAUNCHER', 'GUARD', 'MONITOR', 'DRIVER', 'CORE')}
    if drop_driver:
        s.pop(L.PINS['DRIVER'][0])
    for m in fx.mods.values():
        s[m['path']] = m['sha256']
    s[policy['path']] = policy['sha256']
    return s


def partial_cfg(fx, policy, v007=None, drop_driver=False):
    return {'schema': 'UNT_STEP4_ADMISSION_CX1V001', 'authority': fx.G.AUTHORITY, 'status': 'ROOT_AUTHORIZED',
            'sources': sources_for(fx, policy, drop_driver), 'v007': v007 or fx.v007, 'adoption_policy': policy,
            'config': fx.c1, 'context_module': fx.mods['context'], 'direct_context': fx.mods['direct'],
            'tail_off_policy': None}


def make_admitted_plan(fx, tag, case, *, policy='ok', v007=None, status='ROOT_AUTHORIZED', core_priority=None,
                       drop_driver=False, prelaunch_tamper=False, force_plan=None, batch=None):
    """spec -> native prelaunch record (real guard011) -> plan (lib.make_plan) -> admission (synthetic root bytes)."""
    fx.n_adm += 1
    d = mkdir(fx.g / ('adm_%03d_%s' % (fx.n_adm, tag)))
    fill = fx.fill['off']
    spec_ref = fill['rec']['cases'][case]['spec']
    pol = fx.policy[policy]
    cfgp = partial_cfg(fx, pol, v007, drop_driver)
    call = {'case': case, 'spec': spec_ref, 'driver': L.const_pin('DRIVER'), 'tail_on': True}
    try:
        pre = fx.G.native_preflight(cfgp, call)
    except Exception as exc:                     # as-built refusal (C3T): a placeholder record so the plan can be written
        pre = {'schema': 'UNT_STEP4_PRELAUNCH_CX1V001', 'case': case, 'spec': spec_ref, 'driver': L.const_pin('DRIVER'),
               'config': fx.c1, 'adoption_verdict': (v007 or fx.v007)['verdict'], 'checks': {'placeholder': str(exc)},
               'adoption_checked': True}
    if prelaunch_tamper:
        pre = copy.deepcopy(pre)
        pre['checks']['normalized_sha256'] = '0' * 64
    pre_ref = wjson(d / 'prelaunch.json', pre)
    r = L.make_plan(fill['pin'], case, pre_ref, attempt=1, output_root=fx.out_root + '/' + d.name, dry=True)
    plan = copy.deepcopy(r['plan'])
    if batch:
        plan['batch'] = batch
    if force_plan:
        force_plan(plan)
    plan_ref = L.write_exclusive(str(d / 'plan.json'), (json.dumps(plan, sort_keys=True, indent=2) + '\n').encode())
    adm = copy.deepcopy(cfgp)
    rule = plan['route_a_admission']
    review = wjson(d / 'source_review.json', {'schema': 'UNT_STEP4_SOURCE_REVIEW_CX1V001', 'status': 'TESTED', 'verdict': 'PASS',
                                              'approved_sources': adm['sources'], 'blocking_findings': [],
                                              'reviewer': 'SYNTHETIC_TEST_REVIEWER'})
    c = plan['calls'][0]
    adm.update(status=status, plan=plan_ref, source_review=review, route_a_admission=rule,
               core_priority=core_priority or dict(L.CORE_PRIORITY), case_order=[case],
               caps={case: {k: c[k] for k in ('wall_cap_s', 'rss_cap_bytes', 'output_cap_bytes')}},
               calls={case: {'spec': c['spec'], 'driver': c['driver'], 'prelaunch': c['prelaunch']}})
    adm_ref = wjson(d / 'admission.json', adm, indent=2)
    return {'plan': plan_ref, 'admission': adm_ref, 'dir': d, 'prelaunch': pre_ref, 'plan_doc': plan}


# ---------------------------------------------------------------------------------------------- gate fakes
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


def tree(pid, fp, outdir, driver='0' * 64, spec=None, nproc=11, age=5000.0):
    return {'monitor_pid': pid, 'age_s': age, 'outdir': outdir, 'members': [pid + 1], 'nproc': nproc,
            'cpu_s': {pid + 1: 10.0}, 'rss_bytes': 1, 'driver_sha256': driver, 'spec': spec, 'footprint_gb': fp}


def make_gate(snapshot):
    G3 = L.load_gate()
    clock = Clock()
    calls = {'n': 0}

    def probe():
        calls['n'] += 1
        return copy.deepcopy(snapshot)
    gate = G3.Gate(probe_fn=probe, clock=clock)
    return gate, clock, calls


def spawn_stub(box):
    def sp(argv, env):
        box.append({'argv': argv, 'env_keys': sorted(k for k in env if k.startswith(('UNT_', 'OPENBLAS', 'OMP', 'MKL', 'VECLIB')))})
        return {'returncode': 0, 'stdout': '{"detached_worker_pid": 1}', 'stderr': ''}
    return sp


def do_launch(fx, adm, *, reg=None, v6=None, lcfg=None, snapshot=None, mode='dry', confirm=None, env=None, record=None,
              admission='default'):
    gate, clock, calls = make_gate(snapshot if snapshot is not None else snap())
    box = []
    out = L.launch(adm['plan'], adm['admission'] if admission == 'default' else admission, reg or fx.reg, v6 or fx.v6,
                   lcfg or fx.lcfg['INACTIVE'], mode=mode, confirm=confirm, guard=fx.G, gate=gate, spawn=spawn_stub(box),
                   sleep=clock.sleep, record_path=record, disk_batch=False, env=env)
    return out, calls['n'], box


# ---------------------------------------------------------------------------------------------- reader fixtures
def build_reader(fx):
    import numpy as np
    r = mkdir(fx.root / 'reader')
    fx.r = r
    fx.runs_dir = mkdir(r / 'runs')
    V5 = L.load_source_module(L.const_pin('COMPARE_V005'), '_t_v005', 'V005')
    fx.packets = {}
    for cbcase, grid in (('C3T', 'G3'), ('C4T', 'G4')):
        gs = L.cb_numerics(fx.st, cbcase)['composite_grid_spec']
        ax = V5.expected_axis(gs)
        k = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3)
        w = np.ones((len(k), 1, 1), dtype=np.float64)
        pd = mkdir(r / ('field_' + grid))
        pp = pd / 'refreshed_prepared.npz'
        with open(pp, 'xb') as f:
            np.savez_compressed(f, wavevectors=k, weighted_responses=w)
        pin = L.pin_of(str(pp))
        wjson(pd / 'finish.json', {'outputs': {'refreshed_prepared.npz': pin}})
        fx.packets[cbcase] = str(pd)
        del k, w
    fx.radii = [float(x) for x in L.load_compare(L.const_pin('COMPARE_R11')).registered_row_radii(fx.st['ids'])]
    fx.att_producer = wbytes(r / 'syn_attestation_producer.txt', b'synthetic attestation producer\n')
    fx.base_v = {i: 10.0 + 3.0 * n for n, i in enumerate(fx.st['ids'])}
    fx.n_run = 0


def make_result(fx, case, fill_tag, vfinal, *, amp=0.004, r=0.1, flagged=False, ea=1e-5, status='COMPLETED', valid=True,
                receipt='FINISHED', packet=None, phys_tweak=None, cb_override=None, driver=None, s9=False, probe=True,
                extra_ns=None, failure_bracket=False, write_result=True):
    fx.n_run += 1
    d = fx.runs_dir / ('%03d_%s' % (fx.n_run, case))
    rec = fx.fill[fill_tag]['rec']
    if case in L.S1_CASES:
        spec_ref = rec['cases'][case]['spec']
    else:
        spec_ref = rec['base_spec']
    spec = L.strict_json(L.verify_pin(spec_ref))
    cbcase = cb_override or L.CASE_CB[case]
    num = copy.deepcopy(L.cb_numerics(fx.st, cbcase))
    for s in L.CERT_SLOTS:
        num['uv_tail'][s] = spec['numerics']['uv_tail'][s]
    ns = {'galaxy': 'DDO154', 'label': spec['label'], 'admit': {}, 'coefficients': spec['coefficients'],
          'physical': copy.deepcopy(spec['physical']), 'numerics': num}
    if phys_tweak:
        ns['physical'][phys_tweak] = math.nextafter(ns['physical'][phys_tweak], math.inf)
    if extra_ns:
        ns.update(extra_ns)
    ids = fx.st['ids']
    if receipt is not None:
        rc = {'schema': 'UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001', 'status': receipt,
              'stop_reason': receipt[len('STOPPED_'):] if receipt.startswith('STOPPED_') else None,
              'driver_status': status, 'exit_code': 0 if receipt == 'FINISHED' else 1}
        wjson(str(d) + '.receipt.json', rc)
    if not write_result:
        return {'result_dir': str(d), 'receipt': str(d) + '.receipt.json'}
    mkdir(d)
    passes = []
    prev = None
    for k in range(1, 7):
        vals = {i: vfinal[i] + amp * (r ** k - r ** 6) for i in ids}
        rows = [{'id': i, 'speed_km_s': vals[i]} for i in ids]
        if s9 and k == 6:
            rows[1] = {'id': ids[0], 'speed_km_s': vals[ids[0]]}
        ch = amp if prev is None else max(abs(vals[i] - prev[i]) for i in ids)
        passes.append({'pass': k, 'rows': rows, 'max_abs_change_km_s': ch, 'field': None, 'rotation': None})
        prev = vals
    passes[-1]['field'] = fx.packets[packet or L.CASE_CB[case]]
    uvt = {'schema': 'UNT_UV_TAIL_ROUTE_A_RECORD_C2V001', 'outcome': 'CONVERGED_FINITE_FIXED_POINT', 'production_admissible': True,
           'admissibility': 'production', 'config_sha256': fx.st['cb']['cases'][L.CASE_CB[case]]['uv_tail_config_sha256'],
           'flags': ['TAIL_SOURCE_UNDERCONVERGED'] if flagged else [],
           'monitor_status': 'FLAGGED' if flagged else 'M_T_WITHIN_THRESHOLD', 'M_T_threshold': 0.25,
           'M_T_accepted': 0.3 if flagged else 0.01, 'accepted_iteration': 7, 'E_A_rows_km_s_accepted': [ea] * 12}
    if probe:
        uvt['probe_R_m'] = fx.radii
    att = wjson(d / 'route_a_attempt_result.json', {'result': {'uv_tail': uvt}})
    res = {'schema': 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001', 'status': status, 'valid': valid, 'reasons': [],
           'driver_sha256': driver or L.R5_SHA, 'call_spec_sha256': spec_ref['sha256'],
           'rows': [{'id': i, 'speed_km_s': passes[-1]['rows'][n]['speed_km_s']} for n, i in enumerate(ids)] if not s9 else
           [{'id': i, 'speed_km_s': prev[i]} for i in ids],
           'passes': passes, 'final_pass': 6, 'normalized_spec': ns,
           'route_a_outcome': {'result_path': att['path'], 'result_sha256': att['sha256'], 'ro1': {'armed': True}},
           'stage_records': []}
    if failure_bracket:
        sd = mkdir(d / 'stage_body')
        mkdir(sd / 'columns')
        wjson(sd / 'columns' / 'finish.json', {'failures': [{'index': 5, 'message': 'BRACKET_MISS: synthetic'}]})
        res['stage_records'] = [{'name': 'body', 'kind': 'columns', 'exit_code': 1, 'stage_dir': str(sd)}]
        res['status'], res['valid'] = 'FAILED_AT_STAGE', False
        res['normalized_spec']['numerics']['brackets'] = fx_ra4()
    rr = wjson(d / 'result.json', res)
    return {'result_dir': str(d), 'receipt': str(d) + '.receipt.json', 'result_sha256': rr['sha256']}


def fx_ra4():
    return L.load_compare(L.const_pin('COMPARE_R11')).ra4_block_expected()


def attest(fx, case, run, gate, status='PASS'):
    fx.n_run += 1
    ev = wbytes(fx.r / ('evidence_%03d_%s_%s.txt' % (fx.n_run, case, gate)), b'synthetic evidence\n')
    return wjson(fx.r / ('attest_%03d_%s_%s.json' % (fx.n_run, case, gate)),
                 {'schema': L.SCHEMA_ATTEST, 'gate': gate, 'run': case, 'result_sha256': run.get('result_sha256'),
                  'status': status, 'producer': fx.att_producer, 'evidence': ev})


def manifest(fx, runs, *, fill_tag='off', drop_attest=None, fail_attest=None, reg=None, v6=None, u_a_status=None,
             anchor=None):
    m = {'schema': L.SCHEMA_MANIFEST, 'registration': reg or fx.reg, 'v6': v6 or fx.v6,
         'fill_record': fx.fill[fill_tag]['pin'], 'compare': L.const_pin('COMPARE_R11'), 'runs': {}}
    if u_a_status:
        m['u_A_status'] = u_a_status
    if anchor:
        m['anchor_reference'] = anchor
    for c, run in runs.items():
        e = {'result_dir': run['result_dir'], 'receipt': run['receipt'], 'prelaunch': None, 'attestations': {}}
        if run.get('result_sha256'):
            for g in L.ATTESTED_GATES:
                if drop_attest == (c, g):
                    continue
                e['attestations'][g] = attest(fx, c, run, g, 'FAIL' if fail_attest == (c, g) else 'PASS')
        m['runs'][c] = e
    fx.n_run += 1
    return wjson(fx.r / ('manifest_%03d.json' % fx.n_run), m)


def vec(fx, scale_by_tau=None):
    """K3 values plus d_i = scale * tau_i (dict row -> multiple)."""
    out = dict(fx.base_v)
    for i, s in (scale_by_tau or {}).items():
        out[i] = out[i] + s * fx.st['tau'][i]
    return out


def triple(fx, d=None, dp=None, fill_tag='off', k3=None, k4=None, k4p=None):
    """Three runs: K3 at base, K4 = base + d (x tau), K4' = base + dp (x tau; default = K4 values)."""
    k3 = k3 or {}
    k4 = k4 or {}
    k4p = k4p or {}
    v3 = dict(fx.base_v)
    v4 = vec(fx, d if d is not None else {i: 0.2 for i in fx.st['ids']})
    v4p = vec(fx, dp) if dp is not None else dict(v4)
    return {L.S1_C3T: make_result(fx, L.S1_C3T, fill_tag, v3, **k3),
            L.S1_C4T: make_result(fx, L.S1_C4T, fill_tag, v4, **k4),
            L.K4P: make_result(fx, L.K4P, fill_tag, v4p, **k4p)}


def read(fx, mref, write=None):
    return L.read_reading(mref, write_dir=write)


# ================================================================================================ template tests
@test('F-P1', 'MUST_PASS')
def t_fill_off():
    rec = FX.fill['off']['rec']
    c3, c4 = rec['cases'][L.S1_C3T], rec['cases'][L.S1_C4T]
    s3 = L.strict_json(L.verify_pin(c3['spec']))
    ok = (c4['changed_paths'] == ['label']
          and sorted(c3['changed_paths']) == sorted(['label', 'numerics.composite_grid_spec.breaks_inverse_kpc',
                                                     'numerics.composite_grid_spec.panel_orders',
                                                     'numerics.composite_grid_spec.scope',
                                                     'numerics.composite_grid_spec.total_axis_nodes',
                                                     'numerics.composite_grid_spec.version',
                                                     'numerics.uv_tail.eps_certificate.path',
                                                     'numerics.uv_tail.eps_certificate.sha256',
                                                     'numerics.uv_tail.lo_certificate.path',
                                                     'numerics.uv_tail.lo_certificate.sha256'])
          and L.canonical(s3['numerics']['composite_grid_spec']) == L.canonical(L.cb_numerics(FX.st, 'C3T')['composite_grid_spec'])
          and c4['point_key'] == rec['base_point_key'] and c3['point_key'] != rec['base_point_key']
          and rec['branch']['branch'] == 'OFF_ANCHOR' and c4['as_built_core_validate_block'] == 'PASS'
          and c3['as_built_core_validate_block'] == 'REFUSED: kept K must be 4'
          and any('S1_UA_C3T: as-built control 3 refuses' in b for b in rec['blockers']))
    return ok, {'c3_changed': c3['changed_paths'], 'branch': rec['branch']['branch'], 'c3_core': c3['as_built_core_validate_block'],
                'max_abs_over_half_width': rec['branch']['max_abs_over_half_width']}


@test('F-P2', 'MUST_PASS')
def t_fill_seed():
    b = FX.fill['seed']['rec']['branch']
    ok = (b['branch'] == 'AT_ANCHOR' and b['seed_bits_equal'] is True and b['anchor_alias_within_rtol'] is True
          and all(v == 0.0 for v in b['u_A_minus_u_seed'].values()))
    return ok, {'branch': b['branch'], 'rel_dev': b['relative_deviation_from_anchor']}


@test('F-P3', 'MUST_PASS')
def t_dry_plan():
    before = sorted(os.listdir(FX.root))
    rec = L.fill(FX.ua['off'], FX.base['off'], CFG_PIN, c3t_certs=None, dry=True)
    after = sorted(os.listdir(FX.root))
    ok = (before == after and rec['dry'] is True and 'record' not in rec
          and any('point certificates' in b for b in rec['blockers'])
          and rec['cases'][L.S1_C4T]['sha256'] == FX.fill['off']['rec']['cases'][L.S1_C4T]['sha256'])
    return ok, {'blockers': rec['blockers']}


@test('F-P4', 'MUST_PASS')
def t_equivalence():
    """theta_key / diff_paths (ORC), point_identity (CORE), Mapper physical (ORC Mapper.build), u map (COORD)."""
    orc = L.verify_pin(L.const_pin('ORC'))
    ns = L.extract_definitions(orc, ('canonical', 'sha256_bytes', 'theta_key', 'diff_paths', 'json_bytes', 'Mapper',
                                     'SCHEMA_THETA_KEY', 'FIXED_TEMPLATE_CHECKS', 'DECLARED_CHANGED_PATHS'),
                               L.PINS['ORC'][0], prelude='import json, hashlib, math, copy\nclass OrchestratorError(Exception):\n    pass\n')
    core = L.extract_definitions(L.verify_pin(L.const_pin('CORE')), ('point_identity', 'DRIVER_SHA'), L.PINS['CORE'][0],
                                 prelude='import copy\n')
    coords = FX.st['coord']['engine_coordinates']
    es = {'names': [c['name'] for c in coords], 'trial_values': {c['name']: c['trial_value'] for c in coords},
          'fixed_names': [c['name'] for c in coords if c['role'] == 'fixed'],
          'lower': {c['name']: c['lower'] for c in coords}, 'upper': {c['name']: c['upper'] for c in coords}}
    base = L.strict_json(L.verify_pin(FX.base['off']))
    ctx = types.SimpleNamespace(es=es, base=base, inclination_deg=66.0, base_sha256=FX.base['off']['sha256'])
    out = {}
    for tag, th in (('off', FX.off), ('seed', FX.seed)):
        b = ns['Mapper'](ctx).build(th)
        out[tag] = all(L.fhex(b['spec']['physical'][k]) == L.fhex(v) for k, v in L.mapped_physical(th).items())
        out[tag + '_key'] = ns['theta_key'](th) == L.theta_key(th)
    s3 = L.strict_json(L.verify_pin(FX.fill['off']['rec']['cases'][L.S1_C3T]['spec']))
    out['diff_paths'] = ns['diff_paths'](base, s3) == L.diff_paths(base, s3)
    out['point_identity'] = core['point_identity'](s3) == L.point_identity(s3)
    cs = {c['name']: c for c in coords}
    tu = FX.st['coord']['trial_point']['engine_trial_u']
    out['u_map'] = [L.u_value(FX.seed[n], cs[n]) for n in L.VARYING] == tu
    return all(out.values()), out


@test('F-P5', 'MUST_PASS')
def t_plan_c4t():
    d = mkdir(RUN / 'plan_c4t')
    pre = wjson(d / 'prelaunch_placeholder.json',
                {'schema': 'UNT_STEP4_PRELAUNCH_CX1V001', 'case': L.S1_C4T, 'spec': FX.fill['off']['rec']['cases'][L.S1_C4T]['spec'],
                 'driver': L.const_pin('DRIVER'), 'adoption_checked': True})
    r = L.make_plan(FX.fill['off']['pin'], L.S1_C4T, pre, attempt=1, out_path=str(d / 'PLAN_S1_UA_C4T.json'))
    p = r['plan']
    c = p['calls'][0]
    dbp = L.pinned_json(L.const_pin('DBP'))['batches']['POST_S1']['caps_per_case']['ROOT_NAMES_AT_REGISTRATION_K4']
    ok = (r['written'] is not None and p['batch'] == 'POST_S1' and p['route_a_admission']['max_active'] == 1
          and c['receipt'] == c['outdir'] + '.receipt.json' and c['outdir'].startswith(L.OUTPUT_ROOT + '/S1_UA_C4T_')
          and {k: c[k] for k in dbp} == dbp and p['guard'] == L.const_pin('GUARD') and p['launcher'] == L.const_pin('LAUNCHER')
          and Path(r['written']['plan']['path']).is_file())
    return ok, {'outdir': c['outdir'], 'caps': dbp}


@test('F-P6', 'MUST_PASS')
def t_plan_c3t_blocked():
    d = mkdir(RUN / 'plan_c3t')
    pre = wjson(d / 'prelaunch_placeholder.json',
                {'schema': 'UNT_STEP4_PRELAUNCH_CX1V001', 'case': L.S1_C3T, 'spec': FX.fill['off']['rec']['cases'][L.S1_C3T]['spec'],
                 'driver': L.const_pin('DRIVER'), 'adoption_checked': True})
    r = L.make_plan(FX.fill['off']['pin'], L.S1_C3T, pre, attempt=1, out_path=str(d / 'PLAN_S1_UA_C3T.json'))
    ok = r['written'] is None and not (d / 'PLAN_S1_UA_C3T.json').exists() and any('kept K must be 4' in b for b in r['sidecar']['blockers'])
    return ok, r['sidecar']['blockers']


def _base_variant(tag, mutate, theta=None):
    th = dict(theta or FX.off)
    b = base_spec(th, FX.certs['c4t_eps'], FX.certs['c4t_lo'])
    mutate(b)
    FX.n_run += 1
    return wjson(FX.root / ('base_variant_%03d_%s.json' % (FX.n_run, tag)), b)


def _ua_variant(tag, theta, key=None, phase1=None):
    FX.n_run += 1
    d = ua_doc(theta, phase1 or FX.phase1)
    if key:
        d['theta_key'] = key
    return wjson(FX.root / ('ua_variant_%03d_%s.json' % (FX.n_run, tag)), d)


def _fill(ua, base, certs='c3t'):
    return lambda: L.fill(ua, base, CFG_PIN, c3t_certs=FX.c3t_certs if certs == 'c3t' else certs, dry=True)


@test('F-F1', 'MUST_FAIL')
def t_wrong_theta_bits():
    b = _base_variant('ulp', lambda s: s['physical'].__setitem__('common_scale_s', math.nextafter(s['physical']['common_scale_s'], 1.0)))
    return expect_refusal(_fill(FX.ua['off'], b), 'THETA_PHYSICAL_MISMATCH')


@test('F-F2', 'MUST_FAIL')
def t_theta_key():
    return expect_refusal(_fill(_ua_variant('key', FX.off, key='f' * 64), FX.base['off']), 'THETA_KEY_MISMATCH')


@test('F-F3', 'MUST_FAIL')
def t_phase1_binding():
    p1 = wjson(FX.root / 'phase1_without_key.json', {'schema': 'SYNTHETIC_PHASE1_RECORD', 'theta_keys': []})
    return expect_refusal(_fill(_ua_variant('p1', FX.off, phase1=p1), FX.base['off']), 'PHASE1_RECORD_DOES_NOT_NAME_THETA_KEY')


@test('F-F4', 'MUST_FAIL')
def t_wrong_k_base():
    k3 = L.cb_numerics(FX.st, 'C3T')['composite_grid_spec']
    b = _base_variant('k3', lambda s: s['numerics'].__setitem__('composite_grid_spec', copy.deepcopy(k3)))
    return expect_refusal(_fill(FX.ua['off'], b), 'BASE_NUMERICS_NOT_CAMPAIGN_BLOCK')


@test('F-F5', 'MUST_FAIL')
def t_wrong_k_plan():
    return expect_refusal(lambda: L.make_plan(FX.fill['off']['pin'], 'S1_UA_C5T', None, dry=True), 'S1_CASE_UNKNOWN')


@test('F-F6', 'MUST_FAIL')
def t_admit():
    b = _base_variant('admit', lambda s: s.pop('admit'))
    return expect_refusal(_fill(FX.ua['off'], b), 'BASE_ADMIT_NOT_EMPTY_OBJECT')


@test('F-F7', 'MUST_FAIL')
def t_recovery_brackets():
    def m(s):
        s['numerics']['brackets']['rule']['le_first_factors'] = [0.3, 0.9]
    return expect_refusal(_fill(FX.ua['off'], _base_variant('rec', m)), 'BASE_NUMERICS_NOT_CAMPAIGN_BLOCK')


@test('F-F8', 'MUST_FAIL')
def t_out_of_box():
    th = dict(FX.off)
    th['common_scale_s'] = FX.seed['common_scale_s'] * 3.0
    return expect_refusal(_fill(_ua_variant('box', th), FX.base['off']), 'THETA_OUT_OF_BOX')


@test('F-F9', 'MUST_FAIL')
def t_fixed_moved():
    th = dict(FX.off)
    th['ML_3p6'] = 0.55
    return expect_refusal(_fill(_ua_variant('fixed', th), FX.base['off']), 'THETA_FIXED_COORDINATE_MOVED')


@test('F-F10', 'MUST_FAIL')
def t_distance():
    th = dict(FX.off)
    th['distance_Mpc'] = 4.05
    return expect_refusal(_fill(_ua_variant('dist', th), FX.base['off']), 'THETA_DISTANCE_NOT_REGISTERED')


@test('F-F11', 'MUST_FAIL')
def t_base_pin():
    bad = {'path': FX.base['off']['path'], 'sha256': '0' * 64}
    return expect_refusal(_fill(FX.ua['off'], bad), 'BASE_SPEC_PIN_BYTES_CHANGED')


@test('F-F12', 'MUST_FAIL')
def t_c3t_certs_required():
    d = mkdir(RUN / 'fill_nocerts')
    return expect_refusal(lambda: L.fill(FX.ua['off'], FX.base['off'], CFG_PIN, c3t_certs=None, out_dir=str(d), dry=False),
                          'C3T_CERTIFICATES_REQUIRED')


@test('F-F13', 'MUST_FAIL')
def t_exclusive():
    d = Path(FX.fill['off']['rec']['record']['path']).parent
    return expect_refusal(lambda: L.fill(FX.ua['off'], FX.base['off'], CFG_PIN, c3t_certs=FX.c3t_certs, out_dir=str(d)),
                          'OUTPUT_EXISTS')


@test('F-F14', 'MUST_FAIL')
def t_label():
    b = _base_variant('label', lambda s: s.__setitem__('label', 'DDO154 cx2v006 theta 0000000000000000; point x'))
    return expect_refusal(_fill(FX.ua['off'], b), 'BASE_LABEL_THETA_MISMATCH')


@test('F-F15', 'MUST_FAIL')
def t_base_cert():
    b = _base_variant('cert', lambda s: s['numerics']['uv_tail'].__setitem__('eps_certificate', {'path': FX.certs['c4t_eps']['path'], 'sha256': '1' * 64}))
    return expect_refusal(_fill(FX.ua['off'], b), 'BASE_EPS_CERTIFICATE_PIN_BYTES_CHANGED')


@test('F-F16', 'MUST_FAIL')
def t_base_coefficients():
    b = _base_variant('coef', lambda s: s.__setitem__('coefficients', {'path': s['coefficients']['path'], 'sha256': '2' * 64}))
    return expect_refusal(_fill(FX.ua['off'], b), 'BASE_COEFFICIENTS_NOT_REGISTERED')


# ================================================================================================ launch tests
def _ok_controls(out):
    return all(out['controls'][c] == 'PASS' for c in L.CONTROLS)


@test('L-P1', 'MUST_PASS')
def t_launch_dry():
    adm = make_admitted_plan(FX, 'ok', L.S1_C4T)
    out, probes, box = do_launch(FX, adm)
    ok = (out['decision'] == 'ADMITTED' and _ok_controls(out) and probes > 0 and box == []
          and out['trace'] == ['s1_checks', 'control_C2_admission_load', 'control_C4', 'control_C1', 'control_C2_C3_validate',
                               'gate_hold_check', 'gate_decide']
          and out['gate']['decide']['admit'] is True and out['gate']['a133_rule']['sum_gb'] <= 103.0)
    return ok, {'decision': out['decision'], 'refusal': out['refusal'], 'gate': out['gate']}


@test('L-P2', 'MUST_PASS')
def t_launch_real_stub():
    adm = make_admitted_plan(FX, 'launch', L.S1_C4T)
    env = {'UNT_STEP4_ADMISSION_PATH': adm['admission']['path'], 'UNT_STEP4_ADMISSION_SHA256': adm['admission']['sha256']}
    rec = str(adm['dir'] / 'PRELAUNCH_DECISION.json')
    out, probes, box = do_launch(FX, adm, mode='launch', confirm=adm['plan']['sha256'], env=env, record=rec)
    written = L.strict_json(L.read_bytes(rec))
    ok = (out['decision'] == 'LAUNCHED' and len(box) == 1 and out['trace'][-2:] == ['record', 'spawn']
          and box[0]['argv'][-2:] == [adm['plan']['path'], '--execute-root-only'] and L.PINS['LAUNCHER'][0] in box[0]['argv']
          and written['decision'] == 'LAUNCHING' and 'UNT_STEP4_ADMISSION_SHA256' in box[0]['env_keys']
          and 'OPENBLAS_NUM_THREADS' in box[0]['env_keys'])
    return ok, {'decision': out['decision'], 'argv_tail': box[0]['argv'][-4:] if box else None}


def _refused(out, code, control=None, probes=None, nprobe=0, box=None):
    ok = out['decision'] == 'REFUSED' and out['refusal']['code'] == code and (box is None or box == [])
    if control:
        ok = ok and out['controls'][control].startswith('REFUSED:')
    if probes is not None:
        ok = ok and probes == nprobe
    return ok, {'refusal': out['refusal'], 'controls': out['controls'], 'probes': probes}


@test('L-F1', 'MUST_FAIL')
def t_c1_adopt():
    d = mkdir(FX.g / 'v007_noadopt')
    vd = copy.deepcopy(FX.verdict_doc)
    vd['decision']['outcome'] = 'HIGHER_K_DISAGREEMENT'
    v = dict(FX.v007, verdict=wjson(d / 'verdict.json', vd))
    adm = make_admitted_plan(FX, 'c1', L.S1_C4T, v007=v)
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'SEALED_ADOPT_TAIL_REQUIRED', L.CONTROLS[0], probes, 0, box)


@test('L-F2', 'MUST_FAIL')
def t_c1_tuple():
    adm = make_admitted_plan(FX, 'c1t', L.S1_C4T, policy='empty')
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'REVIEWED_SEAL_TUPLE_PENDING', L.CONTROLS[0], probes, 0, box)


@test('L-F3', 'MUST_FAIL')
def t_c2_pending():
    adm = make_admitted_plan(FX, 'c2p', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, admission=None)
    return _refused(out, 'PUBLISHED_STEP4_ADMISSION_PENDING', None, probes, 0, box)


@test('L-F4', 'MUST_FAIL')
def t_c2_status():
    adm = make_admitted_plan(FX, 'c2s', L.S1_C4T, status='ROOT_DRAFT')
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'ROOT_PLAN_BINDING_REQUIRED', L.CONTROLS[1], probes, 0, box)


@test('L-F5', 'MUST_FAIL')
def t_c2_priority():
    cp = dict(L.CORE_PRIORITY, campaign_inactive=False)
    adm = make_admitted_plan(FX, 'c2c', L.S1_C4T, core_priority=cp)
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'CORE_PRIORITY_ATTESTATION_REQUIRED', L.CONTROLS[1], probes, 0, box)


@test('L-F6', 'MUST_FAIL')
def t_c3_replay():
    adm = make_admitted_plan(FX, 'c3r', L.S1_C4T, prelaunch_tamper=True)
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'PRELAUNCH_REPLAY_MISMATCH', L.CONTROLS[2], probes, 0, box)


@test('L-F7', 'MUST_FAIL')
def t_c3_c3t_as_built():
    adm = make_admitted_plan(FX, 'c3t', L.S1_C3T)
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'kept K must be 4', L.CONTROLS[2], probes, 0, box)


@test('L-F8', 'MUST_FAIL')
def t_c4_allowlist():
    adm = make_admitted_plan(FX, 'c4', L.S1_C4T, drop_driver=True)
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'SOURCE_NOT_ALLOWLISTED', L.CONTROLS[3], probes, 0, box)


@test('L-F9', 'MUST_FAIL')
def t_s1_driver():
    syn = wbytes(FX.g / 'syn_driver.py', b'# not r5\n')
    adm = make_admitted_plan(FX, 'drv', L.S1_C4T, force_plan=lambda p: p['calls'][0].__setitem__('driver', syn))
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'S1_DRIVER_NOT_R5', None, probes, 0, box)


@test('L-F10', 'MUST_FAIL')
def t_s1_batch():
    adm = make_admitted_plan(FX, 'batch', L.S1_C4T, batch='HEADLINE')
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'S1_BATCH_NOT_POST_S1', None, probes, 0, box)


@test('L-F11', 'MUST_FAIL')
def t_registration_synthetic():
    adm = make_admitted_plan(FX, 'reg', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, v6=FX.v6_without)
    return _refused(out, 'S1_REGISTRATION_NOT_IN_FORCE', None, probes, 0, box)


@test('L-F12', 'MUST_FAIL')
def t_registration_real_bytes():
    """The real V002 registration is not yet entered in the real V006 (read at test time; content not printed)."""
    reg = L.pin_of(str(REG_V002))
    v6 = L.pin_of(V6_PATH)
    adm = make_admitted_plan(FX, 'regreal', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, reg=reg, v6=v6)
    ok, det = _refused(out, 'S1_REGISTRATION_NOT_IN_FORCE', None, probes, 0, box)
    det['v6_sha_at_test'] = v6['sha256']
    det['registration_sha'] = reg['sha256']
    return ok, det


@test('L-F13', 'MUST_FAIL')
def t_overlap():
    adm = make_admitted_plan(FX, 'ovl', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, lcfg=FX.lcfg['ACTIVE'])
    return _refused(out, 'S1_OVERLAP_NEEDS_GUARD_SUCCESSOR', None, probes, 0, box)


@test('L-F14', 'MUST_FAIL')
def t_spec_not_filled():
    c3 = FX.fill['off']['rec']['cases'][L.S1_C3T]['spec']
    adm = make_admitted_plan(FX, 'spec', L.S1_C4T, force_plan=lambda p: p['calls'][0].__setitem__('spec', c3))
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'S1_SPEC_NOT_FILLED_SPEC', None, probes, 0, box)


@test('L-F15', 'MUST_FAIL')
def t_template_replay():
    d = mkdir(RUN / 'fake_fill')
    rec = copy.deepcopy(FX.fill['off']['rec'])
    s = L.strict_json(L.verify_pin(rec['cases'][L.S1_C4T]['spec']))
    s['label'] = s['label'] + ' (edited)'
    rec['cases'][L.S1_C4T]['spec'] = L.write_exclusive(str(d / 'edited_c4t.spec.json'), L.spec_bytes(s))
    rec.pop('record', None)
    fpin = wjson(d / 'FAKE_FILL_RECORD.json', rec)

    def fp(p):
        p['s1']['fill_record'] = fpin
        p['calls'][0]['spec'] = rec['cases'][L.S1_C4T]['spec']
    adm = make_admitted_plan(FX, 'replay', L.S1_C4T, force_plan=fp)
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'S1_TEMPLATE_REPLAY_MISMATCH', None, probes, 0, box)


@test('L-F16', 'MUST_FAIL')
def t_gate_twin():
    tw = wjson(FX.g / 'twin_spec.json', {'numerics': {'route_a': {'column_workers': 8}}})
    G3 = L.load_gate()
    s = snap([tree(500, 30.0, str(FX.g / 'twin_out'), driver=G3.PARAMS['ngc_driver_sha256'], spec=tw['path'])])
    adm = make_admitted_plan(FX, 'twin', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, snapshot=s)
    ok = out['decision'] == 'REFUSED' and out['refusal']['code'] == 'GATE_TWIN_HOLD' and _ok_controls(out) and box == []
    return ok, {'refusal': out['refusal']}


@test('L-F17', 'MUST_FAIL')
def t_gate_probe():
    adm = make_admitted_plan(FX, 'probe', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, snapshot=snap(ok=False))
    ok = out['decision'] == 'REFUSED' and out['refusal']['code'] == 'GATE_PROBE_FAILED' and _ok_controls(out) and box == []
    return ok, {'refusal': out['refusal']}


@test('L-F18', 'MUST_FAIL')
def t_gate_memory():
    s = snap([tree(600, 30.0, str(FX.g / 'campaign_route_a_out'))])
    adm = make_admitted_plan(FX, 'mem', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, snapshot=s)
    ok = (out['decision'] == 'REFUSED' and out['refusal']['code'] == 'GATE_REFUSED' and 'MEMORY_HARD' in out['refusal']['detail']
          and box == [])
    return ok, {'refusal': out['refusal'], 'decide': (out.get('gate') or {}).get('decide')}


@test('L-F19', 'MUST_FAIL')
def t_a133_unknown():
    pd = mkdir(FX.g / 'campaign_after_out')
    wbytes(pd / 'progress.jsonl', b'{"stage": "route_a", "event": "finished"}\n')
    s = snap([tree(700, None, str(pd), nproc=2)])
    adm = make_admitted_plan(FX, 'a133', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, snapshot=s)
    ok = out['decision'] == 'REFUSED' and out['refusal']['code'] == 'A133_FOOTPRINT_UNKNOWN' and box == []
    return ok, {'refusal': out['refusal'], 'a133': (out.get('gate') or {}).get('a133_rule')}


@test('L-F20', 'MUST_FAIL')
def t_confirm():
    adm = make_admitted_plan(FX, 'conf', L.S1_C4T)
    env = {'UNT_STEP4_ADMISSION_PATH': adm['admission']['path'], 'UNT_STEP4_ADMISSION_SHA256': adm['admission']['sha256']}
    out, probes, box = do_launch(FX, adm, mode='launch', confirm='0' * 64, env=env, record=str(adm['dir'] / 'R.json'))
    return _refused(out, 'LAUNCH_CONFIRMATION_REQUIRED', None, probes, 0, box)


@test('L-F21', 'MUST_FAIL')
def t_env():
    adm = make_admitted_plan(FX, 'env', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, mode='launch', confirm=adm['plan']['sha256'], env={}, record=str(adm['dir'] / 'R.json'))
    return _refused(out, 'PUBLISHED_ADMISSION_ENV_MISMATCH', None, probes, 0, box)


@test('L-F23', 'MUST_FAIL')
def t_record_required():
    adm = make_admitted_plan(FX, 'rec', L.S1_C4T)
    env = {'UNT_STEP4_ADMISSION_PATH': adm['admission']['path'], 'UNT_STEP4_ADMISSION_SHA256': adm['admission']['sha256']}
    out, probes, box = do_launch(FX, adm, mode='launch', confirm=adm['plan']['sha256'], env=env, record=None)
    return _refused(out, 'PRELAUNCH_RECORD_PATH_REQUIRED', None, probes, 0, box)


@test('L-F22', 'MUST_FAIL')
def t_step2():
    adm = make_admitted_plan(FX, 'st2', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, lcfg=FX.lcfg_step2)
    return _refused(out, 'STEP2_ROUTE_A_NOT_INACTIVE', None, probes, 0, box)


# ================================================================================================ reader tests
def _code(out, code, sub=None):
    ok = out['code'] == code and (sub is None or (out.get('sub_code') or '').startswith(sub))
    return ok, {'code': out['code'], 'sub_code': out.get('sub_code'), 'next': out.get('next_step')}


@test('R-P1', 'MUST_PASS')
def t_read_pass():
    runs = triple(FX)
    out = read(FX, manifest(FX, runs))
    ids, tau = FX.st['ids'], FX.st['tau']
    want = max(abs(out['rows'][i]['d']) / tau[i] for i in ids)
    ok = (out['code'] == 'PASS' and abs(out['statistic']['Dhat_S1'] - 0.2) < 1e-9 and abs(want - 0.2) < 1e-9
          and all(out['rows'][i]['delta4_bitwise_equal'] for i in ids)
          and out['tests']['TH2_K3_K4']['noise']['decidable'] is True and out['tests']['TH2_K3_K4PRIME']['status'] == 'PASS'
          and 'UNTESTED at every other point' in out['label'])
    return ok, {'code': out['code'], 'Dhat': out['statistic']['Dhat_S1'], 'effect': out['step5_effect']}


@test('R-P2', 'MUST_PASS')
def t_read_seed():
    runs = triple(FX, fill_tag='seed')
    out = read(FX, manifest(FX, runs, fill_tag='seed'))
    ok = out['code'] == 'PASS_AT_ADOPTION_POINT' and 'Phase-2 step-5 reads stay held' in out['step5_effect']
    return ok, {'code': out['code'], 'effect': out['step5_effect']}


@test('R-P3', 'MUST_PASS')
def t_read_write():
    runs = triple(FX)
    m = manifest(FX, runs)
    d = mkdir(FX.r / 'reading_out')
    out = read(FX, m, write=str(d))
    ok1 = Path(out['written']['path']).is_file() and L.sha256_bytes(L.read_bytes(out['written']['path'])) == out['written']['sha256']
    ok2, det = expect_refusal(lambda: read(FX, m, write=str(d)), 'OUTPUT_EXISTS')
    return ok1 and ok2, {'written': out['written'], 'second': det}


@test('R-P4', 'MUST_PASS')
def t_read_anchor_report():
    runs = triple(FX)
    a = wjson(FX.r / 'anchor_reference_syn.json', {'rows': {'C3T': dict(FX.base_v), 'C4T': vec(FX, {i: 0.3 for i in FX.st['ids']})}})
    out = read(FX, manifest(FX, runs, anchor=a))
    ac = out.get('anchor_comparison') or {}
    ok = out['code'] == 'PASS' and ac.get('label') == 'reported, never gating' and 'max_over_tau_S1_vs_V007' in ac
    return ok, {'code': out['code'], 'max_over_tau_S1_vs_V007': ac.get('max_over_tau_S1_vs_V007')}


@test('R-P5', 'MUST_PASS')
def t_read_digests():
    runs = triple(FX)
    out = read(FX, manifest(FX, runs))
    dg = out['reused_function_digests']
    ok = all(isinstance(v, str) and len(v) == 64 for v in list(dg['compare'].values()) + list(dg['v005'].values()))
    return ok, dg


ROW_FAIL = 'DDO154_SPARC12_07'


@test('R-F1', 'MUST_FAIL')
def t_th1():
    d = {i: 0.2 for i in FX.st['ids']}
    d[ROW_FAIL] = 1.5
    return _code(read(FX, manifest(FX, triple(FX, d=d))), 'FAIL_TH1')


@test('R-F2', 'MUST_FAIL')
def t_th2():
    d = {i: 0.2 for i in FX.st['ids']}
    d[ROW_FAIL] = 0.7
    return _code(read(FX, manifest(FX, triple(FX, d=d))), 'FAIL_TH2', 'TH2_K3_K4')


@test('R-F3', 'MUST_FAIL')
def t_th2_k4prime():
    dp = {i: 0.2 for i in FX.st['ids']}
    dp[ROW_FAIL] = 0.7
    out = read(FX, manifest(FX, triple(FX, dp=dp)))
    ok, det = _code(out, 'FAIL_TH2', 'TH2_K3_K4PRIME')
    return ok and out['tests']['TH2_K3_K4']['status'] == 'PASS', det


@test('R-F4', 'MUST_FAIL')
def t_undecidable():
    d = {i: 0.2 for i in FX.st['ids']}
    d[ROW_FAIL] = 0.7
    out = read(FX, manifest(FX, triple(FX, d=d, k3={'amp': 0.05, 'r': 0.9})))
    ok, det = _code(out, 'UNDECIDABLE', 'RPAIR_PENDING')
    det['branch'] = out['tests']['TH2_K3_K4'].get('rpair_branch')
    return ok, det


@test('R-F5', 'MUST_FAIL')
def t_th1_not_subject():
    d = {i: 0.2 for i in FX.st['ids']}
    d[ROW_FAIL] = 1.5
    return _code(read(FX, manifest(FX, triple(FX, d=d, k3={'amp': 0.05, 'r': 0.9}))), 'FAIL_TH1')


@test('R-F6', 'MUST_FAIL')
def t_not_run():
    runs = triple(FX)
    runs[L.S1_C4T] = make_result(FX, L.S1_C4T, 'off', dict(FX.base_v), receipt=None, write_result=False)
    return _code(read(FX, manifest(FX, runs)), 'NOT_RUN', 'NO_RECEIPT:S1_UA_C4T')


@test('R-F7', 'MUST_FAIL')
def t_no_u_a():
    runs = triple(FX)
    return _code(read(FX, manifest(FX, runs, u_a_status='NO_U_A:NO_ADMITTED_POINT_FOUND')), 'NOT_RUN', 'NO_U_A')


@test('R-F8', 'MUST_FAIL')
def t_monitor_stop():
    runs = triple(FX)
    runs[L.S1_C3T] = make_result(FX, L.S1_C3T, 'off', dict(FX.base_v), receipt='STOPPED_WALL_CAP', write_result=False)
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID', 'S1_UA_C3T:MONITOR_STOP')
    return ok and 'cap raised' in out['next_step'], det


@test('R-F9', 'MUST_FAIL')
def t_sv1():
    runs = triple(FX, k4={'status': 'COMPLETED_INVALID', 'valid': False})
    return _code(read(FX, manifest(FX, runs)), 'INVALID', 'S1_UA_C4T:SV1_COMPLETED_INVALID')


@test('R-F10', 'MUST_FAIL')
def t_sv2():
    runs = triple(FX, k4={'amp': 1.0, 'r': 0.5})
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID')
    return ok and 'SV2_FINAL_PASS_CHANGE_ABOVE_TAU_PICARD' in out['validity'][L.S1_C4T]['codes'], det


@test('R-F11', 'MUST_FAIL')
def t_sv3_bits():
    runs = triple(FX, k4p={'phys_tweak': 'common_scale_s'})
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID')
    return ok and 'SV3_PHYSICAL_NOT_U_A_BITS:common_scale_s' in out['validity'][L.K4P]['codes'], det


@test('R-F12', 'MUST_FAIL')
def t_sv3_k():
    runs = triple(FX, k3={'cb_override': 'C4T', 'packet': 'C3T'})
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID')
    cs = out['validity'][L.S1_C3T]['codes']
    return ok and 'SV3_NUMERICS_NOT_CB_C3T' in cs and 'SV3_K_NOT_3' in cs, det


@test('R-F13', 'MUST_FAIL')
def t_sv4():
    runs = triple(FX, k3={'packet': 'C4T'})
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID')
    return ok and 'SV4_PACKET_AXIS' in out['validity'][L.S1_C3T]['codes'], det


@test('R-F14', 'MUST_FAIL')
def t_sv0_driver():
    runs = triple(FX, k4={'driver': '0' * 64})
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID')
    return ok and 'SV0_DRIVER_NOT_R5' in out['validity'][L.S1_C4T]['codes'], det


@test('R-F15', 'MUST_FAIL')
def t_s9():
    runs = triple(FX, k4={'s9': True})
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID')
    return ok and any(c.startswith('SV1_RECORD_DEFECT_S9') for c in out['validity'][L.S1_C4T]['codes']), det


@test('R-F16', 'MUST_FAIL')
def t_sv7():
    runs = triple(FX)
    out = read(FX, manifest(FX, runs, fail_attest=(L.S1_C4T, 'SV7')))
    ok, det = _code(out, 'INVALID')
    return ok and 'A134 Q5' in out['next_step'], det


@test('R-F17', 'MUST_FAIL')
def t_flag_pending():
    runs = triple(FX, k4={'flagged': True})
    return _code(read(FX, manifest(FX, runs)), 'INVALID', 'FLAG_PENDING_RULING')


@test('R-F18', 'MUST_FAIL')
def t_flag_fail():
    d = {i: 0.2 for i in FX.st['ids']}
    d[ROW_FAIL] = 0.7
    runs = triple(FX, d=d, k3={'flagged': True})
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID', 'UNDECIDABLE_FLAGGED')
    return ok and 'source_rtol/10' in out['next_step'], det


@test('R-F19', 'MUST_FAIL')
def t_ea_unavailable():
    runs = triple(FX, k3={'probe': False})
    return _code(read(FX, manifest(FX, runs)), 'INVALID', 'INCOMPLETE_RECORD')


@test('R-F20', 'MUST_FAIL')
def t_attest_missing():
    runs = triple(FX)
    m = manifest(FX, runs, drop_attest=(L.K4P, 'RO1'))
    d = mkdir(FX.r / 'reading_refused')
    ok, det = expect_refusal(lambda: read(FX, m, write=str(d)), 'S1_INPUT_INCOMPLETE')
    return ok and os.listdir(d) == [], det


@test('R-F21', 'MUST_FAIL')
def t_bracket():
    runs = triple(FX, k3={'failure_bracket': True, 'receipt': 'CHILD_FAILED'})
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID')
    return ok and 'own registration' in out['next_step'] and 'BRACKET_HULL_MISS' in ','.join(out['validity'][L.S1_C3T]['codes']), det


@test('R-F22', 'MUST_FAIL')
def t_k4prime_extra():
    runs = triple(FX, k4p={'extra_ns': {'reference_compare': True}})
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID', 'K4_PRIME:SV_K4PRIME_NOT_K4_EXCEPT_LABEL')
    return ok, det


@test('R-F23', 'MUST_FAIL')
def t_target_free():
    runs = triple(FX)
    runs[L.K4P] = dict(runs[L.K4P], result_dir='/Users/bgm/Research/NGC3198_SOMETHING/out')
    return expect_refusal(lambda: read(FX, manifest(FX, runs)), 'PROTECTED_PATH_REFUSED')


@test('R-F24', 'MUST_FAIL')
def t_read_registration():
    runs = triple(FX)
    return expect_refusal(lambda: read(FX, manifest(FX, runs, v6=FX.v6_without)), 'S1_REGISTRATION_NOT_IN_FORCE')


@test('R-F25', 'MUST_FAIL')
def t_seed_fail_th2():
    d = {i: 0.2 for i in FX.st['ids']}
    d[ROW_FAIL] = 0.7
    out = read(FX, manifest(FX, triple(FX, d=d, fill_tag='seed'), fill_tag='seed'))
    ok, det = _code(out, 'FAIL_TH2')
    return ok and 'carries no transfer information' in out['label'], det


@test('R-F26', 'MUST_FAIL')
def t_th1_before_incomplete():
    d = {i: 0.2 for i in FX.st['ids']}
    d[ROW_FAIL] = 1.5
    out = read(FX, manifest(FX, triple(FX, d=d, k3={'probe': False})))
    ok, det = _code(out, 'FAIL_TH1')
    return ok and out['tests']['TH2_K3_K4']['status'] == 'INCOMPLETE', det


@test('R-F27', 'MUST_FAIL')
def t_receipt_unreadable():
    runs = triple(FX)
    FX.n_run += 1
    bad = FX.r / ('bad_receipt_%03d.json' % FX.n_run)
    wbytes(bad, b'{"status": "FINISHED", "status": "FINISHED"}\n')
    runs[L.S1_C4T] = dict(runs[L.S1_C4T], receipt=str(bad))
    return _code(read(FX, manifest(FX, runs)), 'INVALID', 'S1_UA_C4T:RECEIPT_UNREADABLE:DUPLICATE_JSON_KEY')


# ================================================================================================ path guard tests
@test('G-P1', 'MUST_PASS')
def t_guard_ruling_file():
    p = L.guard_path(V6_PATH)
    return str(p) == V6_PATH, str(p)[-60:]


@test('G-F1', 'MUST_FAIL')
def t_guard_ngc_dir():
    return expect_refusal(lambda: L.guard_path('/Users/bgm/Research/x/NGC3198_TARGET/ROOT_DECISIONS_NGC3198_CONSTRUCTION_X.md'),
                          'PROTECTED_PATH_REFUSED')


@test('G-F2', 'MUST_FAIL')
def t_guard_ngc_json():
    return expect_refusal(lambda: L.guard_path('/Users/bgm/Research/x/ROOT_DECISIONS_NGC3198_CONSTRUCTION_X.json'),
                          'PROTECTED_PATH_REFUSED')


@test('G-F3', 'MUST_FAIL')
def t_guard_uvt_c5h():
    a = expect_refusal(lambda: L.guard_path('/Users/bgm/Research/UVT_RUNS/x.json'), 'PROTECTED_PATH_REFUSED')
    b = expect_refusal(lambda: L.guard_path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c5h_hull_c2/x.json'),
                       'PROTECTED_PATH_REFUSED')
    c = expect_refusal(lambda: L.guard_path('/Users/bgm/.codex/sessions/x.json'), 'PROTECTED_PATH_REFUSED')
    return a[0] and b[0] and c[0], [a[1], b[1], c[1]]


# ================================================================================================ CLI wrapper tests
def _cli(script, args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('UNT_STEP4_')}
    r = subprocess.run([PY, '-I', '-B', str(HERE / script)] + args, capture_output=True, text=True, timeout=600, env=env)
    return r.returncode, r.stdout, r.stderr


def _p(ref):
    return '%s@%s' % (ref['path'], ref['sha256'])


@test('W-P1', 'MUST_PASS')
def t_cli_read():
    runs = triple(FX)
    m = manifest(FX, runs)
    rc, so, se = _cli('s1_read_c2v001.py', ['--manifest', _p(m)])
    return rc == 0 and json.loads(so)['code'] == 'PASS', {'rc': rc, 'stderr': se[-300:]}


@test('W-P2', 'MUST_PASS')
def t_cli_dry_plan():
    rc, so, se = _cli('s1_fill_c2v001.py', ['dry-plan', '--u-a', _p(FX.ua['off']), '--base-spec', _p(FX.base['off']),
                                            '--campaign-config', _p(CFG_PIN)])
    return rc == 0 and json.loads(so)['dry'] is True, {'rc': rc, 'stderr': se[-300:]}


@test('W-F1', 'MUST_FAIL')
def t_cli_launch_pending():
    adm = make_admitted_plan(FX, 'cli', L.S1_C4T)
    rc, so, se = _cli('s1_launch_root_c2v001.py', ['--plan', _p(adm['plan']), '--registration', _p(FX.reg), '--v6', _p(FX.v6),
                                                   '--launch-config', _p(FX.lcfg['INACTIVE'])])
    o = json.loads(so)
    return rc == 3 and o['refusal']['code'] == 'PUBLISHED_STEP4_ADMISSION_PENDING' and o['trace'][-1] == 'control_C2_admission_load', \
        {'rc': rc, 'refusal': o.get('refusal')}


@test('W-F2', 'MUST_FAIL')
def t_cli_lib_changed():
    d = mkdir(RUN / 'cli_tamper')
    for f in ('s1_read_c2v001.py',):
        wbytes(d / f, (HERE / f).read_bytes())
    wbytes(d / 's1_path_lib_c2v001.py', LIB_PATH.read_bytes() + b'\n# tampered\n')
    r = subprocess.run([PY, '-I', '-B', str(d / 's1_read_c2v001.py'), '--manifest', '/x@y'], capture_output=True, text=True, timeout=120)
    return r.returncode == 3 and 'LIB_BYTES_CHANGED' in r.stdout, {'rc': r.returncode, 'stdout': r.stdout[-200:]}


# ================================================================================================ main
def main():
    global L, RUN, FX
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    a = ap.parse_args()
    L, lib_sha = load_lib()
    RUN = Path(a.run_dir)
    L.guard_path(str(RUN))
    os.mkdir(str(RUN))
    t0 = time.time()
    started = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    try:
        FX = build_fixtures()
        fx_ok = True
    except Exception:
        fx_ok = False
        log('FIXTURES FAILED\n' + traceback.format_exc())
    if fx_ok:
        for fn in TESTS:
            try:
                ok, det = fn()
            except Exception as exc:
                ok, det = False, 'EXCEPTION %s: %s\n%s' % (type(exc).__name__, exc, traceback.format_exc()[-1500:])
            record(fn._tid, fn._kind, bool(ok), det)
    n = len(RESULTS)
    npass = sum(1 for r in RESULTS if r['result'] == 'PASS')
    files = {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest() for f in sorted(os.listdir(HERE))
             if f.endswith('.py') and (HERE / f).is_file()}
    summary = {'schema': 'UNT_S1_PATH_TEST_RESULTS_C2V001', 'started_utc': started,
               'finished_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'seconds': round(time.time() - t0, 1),
               'python': sys.version.split()[0], 'interpreter': sys.executable, 'lib_sha256': lib_sha, 'files_sha256': files,
               'fixtures_ok': fx_ok, 'n_tests': n, 'n_pass': npass,
               'by_kind': {k: {'n': sum(1 for r in RESULTS if r['kind'] == k),
                               'pass': sum(1 for r in RESULTS if r['kind'] == k and r['result'] == 'PASS')}
                           for k in ('MUST_PASS', 'MUST_FAIL')},
               'results': RESULTS}
    L.write_exclusive(str(RUN / 'TEST_RESULTS.json'), (json.dumps(summary, indent=1, sort_keys=True, default=str) + '\n').encode())
    L.write_exclusive(str(RUN / 'TEST_LOG.txt'), ('\n'.join(LOG) + '\n').encode())
    print(json.dumps({k: summary[k] for k in ('n_tests', 'n_pass', 'by_kind', 'fixtures_ok', 'seconds', 'lib_sha256')}))
    return 0 if (fx_ok and npass == n) else 1


if __name__ == '__main__':
    sys.exit(main())
