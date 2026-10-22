"""Synthetic tests for the S1 path c2v002a (MUST_PASS / MUST_FAIL). Target-free; launches nothing.

  python3 -I -B test_s1_path_c2v002a.py --run-dir <a new directory>

Ports all 135 c2v002 tests with ids and expected codes unchanged (the c2v002 suite ported the 87 c2v001 tests and added
MUST_FAIL tests for B1-B3, notes 1, 2, 4-13 and the verifier's E2-E7 probes); R-P1 also requires fill_record_replayed,
and L-F15's refusal (same code and stage) now comes from the replay, with the case as detail. It adds the BLK-1
tests: an edited fill record
(branch, theta_key, physical_u_A, every other consumed field, a log-only u_A point, a swapped spec) refused at read
time, by guard_replay, by guard012's own validate and by the launch path; the read CLI refusing it; the BLK-1 defect
reproduced on the predecessor's bytes (so the MUST_FAIL inputs are not vacuous); format compatibility with c2v002.
The predecessor library s1_path_lib_c2v002.py (e3ca4d80) is loaded read-only, by path and sha, for B-P1, A-P2, F-P8.

Every fixture is synthetic and is written inside --run-dir (created here; it must not exist). Read-only inputs are the
pinned registered files the library names (P5, CB, coordinate spec, CORE, ORC, q5b1 and its loaded modules, guard012,
launcher013, the wrapper successor, root monitor, driver r5 (hashed only), gate v003, params C2V003A, compare r11 and
r14, V005 compare, the DDO154 row-radius binding, the real registration C2V002), the campaign run config CFG d9241676
and the real V006 (hashed and line-scanned for root's entry line only; nothing printed).

Test seam (disclosed): the library constant V6_PATH is set to a synthetic V006 inside this process for the synthetic
readings and launches (it carries root-form entry lines for the real registration sha and the synthetic SV7 producer);
the CLI wrappers load the library by sha and never patch it, and L-P4 / W-P1 run against the real V006.
The four 0620 controls run through guard012's real code on synthetic admission inputs, with the real wrapper successor
(or q5b1, for the as-built refusal) as the context module; the machine gate is the real gate v003 Gate class with a
synthetic probe and clock; the reader uses the real compare r14 / r11 and V005 functions on synthetic result trees.
No subprocess is started except the CLI wrapper tests (python -I -B on the wrappers in this folder).
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
LIB_PATH = HERE / 's1_path_lib_c2v002a.py'
PRED_LIB = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/s1_path_lib_c2v002.py',
            'sha256': 'e3ca4d80fee093456117a6fe3401861c8166f5015c9ad99e7b04feae7410bc1c'}
CFG_PIN = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sched_s45_c2/v003/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V003.json',
           'sha256': 'd9241676c3b7b32bd3067a55bdfb7821ebc33a68adbdc011ab4e4c58b6e50a4d'}
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
WRAPPER_DEPS = ((ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py',
                 '7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d'),
                (ART + '/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py',
                 'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'),
                (ART + '/calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py',
                 '8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f'),
                (ART + '/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py',
                 '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'))
Q5B1 = WRAPPER_DEPS[0]
RO1_PARALLEL = '869ce3870a13fdc94a014cdb0b34eab867c05e59ab7d8abfb15f7db382fd52da'
RO1_SERIAL = 'fbe9ae79ac113aab76109ece785d8030729ce62890dc76ff58144a75af6c17b3'
RO1_BINDING = '86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885'
PY = sys.executable

L = None
RUN = None
FX = None
REAL_V6_PATH = None
RESULTS = []
LOG = []


def load_lib():
    raw = LIB_PATH.read_bytes()
    m = types.ModuleType('s1_path_lib_c2v002a')
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
        return exc.code == code, 'refused %s %s' % (exc.code, str(exc.detail)[:150] if exc.detail else '')
    return False, 'no refusal'


def fresh(tag):
    FX.n_run += 1
    return mkdir(FX.root / ('%s_%03d' % (tag, FX.n_run)))


class use_v6:
    """Set the library's V6_PATH constant to a V006 pin's path for the block (test seam; restored after)."""
    def __init__(self, pin):
        self.pin = pin

    def __enter__(self):
        self.old = L.V6_PATH
        L.V6_PATH = self.pin['path']
        return self.pin

    def __exit__(self, *a):
        L.V6_PATH = self.old


def syn_v6(extra_lines=(), with_registration=True, with_producer=True, tag='v6'):
    lines = ['# synthetic V006 for the S1 path c2v002a tests', '', '## A150: synthetic entry', '']
    if with_registration:
        lines.append('**Registration in force:** `claude_artifacts/s1_path_c2/S1_REGISTRATION_DRAFT_C2V002.md`, sha256 `%s`.'
                     % L.REGISTRATION_SHA)
    if with_producer:
        lines.append('**S1 attestation producer (SV7):** synthetic producer, sha256 `%s`' % FX.att_producer['sha256'])
    lines += list(extra_lines)
    d = fresh(tag)
    return wbytes(d / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_SYNTHETIC_V006_ADDENDUM.md', ('\n'.join(lines) + '\n').encode())


# ================================================================================================ fixtures
class Fx:
    pass


def build_fixtures():
    global FX
    fx = Fx()
    FX = fx
    fx.root = mkdir(RUN / 'fx')
    fx.n_run = 0
    st = L.load_static()
    fx.st = st
    coord = st['coord']
    fx.cs = {c['name']: c for c in coord['engine_coordinates']}
    fx.seed = dict(coord['trial_point']['engine_seed_theta'])
    off = dict(fx.seed)
    off['common_scale_s'] = fx.seed['common_scale_s'] * 1.1
    off['gamma_over_Eref'] = fx.seed['gamma_over_Eref'] * 1.25
    off['ell_F_m'] = fx.seed['ell_F_m'] * 0.9
    fx.off = off
    cd = mkdir(fx.root / 'certs')
    fx.certs = {}
    for k in ('c4t_eps', 'c4t_lo', 'c3t_eps', 'c3t_lo', 'c4t_seed_eps', 'c4t_seed_lo'):
        fx.certs[k] = wjson(cd / (k + '.json'), {'schema': 'SYNTHETIC_TEST_CERTIFICATE', 'name': k})
    fx.snap = {'off': phase1_snapshot('off', off, fx.seed), 'seed': phase1_snapshot('seed', fx.seed, off)}
    fx.cfg = L.pinned_json(CFG_PIN)
    fx.ua, fx.base, fx.registry, fx.fill = {}, {}, {}, {}
    for tag, th, cert in (('off', off, ('c4t_eps', 'c4t_lo')), ('seed', fx.seed, ('c4t_seed_eps', 'c4t_seed_lo'))):
        fx.ua[tag] = wjson(fx.root / ('ua_%s.json' % tag), ua_doc(th, fx.snap[tag]))
        fx.base[tag] = wjson(fx.root / ('base_%s.spec.json' % tag), base_spec(th, fx.certs[cert[0]], fx.certs[cert[1]]))
        fx.registry[tag] = c3t_registry(tag, fx.base[tag], th)
        d = mkdir(fx.root / ('fill_' + tag))
        rec = L.fill(fx.ua[tag], fx.base[tag], CFG_PIN, c3t_registry=fx.registry[tag], out_dir=str(d))
        fx.fill[tag] = {'rec': rec, 'pin': rec['record']}
    fx.att_producer = wbytes(fx.root / 'syn_attestation_producer.txt', b'synthetic attestation producer\n')
    fx.reg = L.const_pin('REGISTRATION')
    fx.v6 = syn_v6(tag='v6_default')
    L.V6_PATH = fx.v6['path']                                     # the test seam (see the module docstring)
    fx.lcfg = {
        'INACTIVE': wjson(fx.root / 'launch_cfg_inactive.json', {'schema': L.SCHEMA_LAUNCH_CFG, 'campaign_state': 'INACTIVE',
                                                                  'step2_route_a_state': 'INACTIVE'}),
        'ACTIVE': wjson(fx.root / 'launch_cfg_active.json', {'schema': L.SCHEMA_LAUNCH_CFG, 'campaign_state': 'ACTIVE',
                                                              'step2_route_a_state': 'INACTIVE',
                                                              'campaign_window': 'SINGLE_CALL_WAVE_START'}),
        'ACTIVE_NO_WINDOW': wjson(fx.root / 'launch_cfg_active_nowin.json', {'schema': L.SCHEMA_LAUNCH_CFG,
                                                                            'campaign_state': 'ACTIVE',
                                                                            'step2_route_a_state': 'INACTIVE'})}
    fx.lcfg_step2 = wjson(fx.root / 'launch_cfg_step2_active.json',
                          {'schema': L.SCHEMA_LAUNCH_CFG, 'campaign_state': 'INACTIVE', 'step2_route_a_state': 'ACTIVE'})
    build_g12(fx)
    build_reader(fx)
    return fx


def phase1_snapshot(tag, theta, other, mutate_snap=None, mutate_rec=None):
    """A synthetic Phase-1 snapshot in the phase1_c2v003 cmd_snapshot form, beside its calibration record. The record's
    engine log names both points; only the primary anchor (log index 3) is u_A."""
    d = mkdir(RUN / 'fx' / ('phase1_%s_%d' % (tag, len(os.listdir(str(RUN / 'fx'))))))
    cs = {c['name']: c for c in L.load_static()['coord']['engine_coordinates']}
    u = [L.u_value(theta[n], cs[n]) for n in L.VARYING]
    pa = {'log_index': 3, 'source': 'seed' if tag == 'seed' else 'admitted', 'purpose': 'synthetic', 'u': u,
          'theta_natural': theta}
    rec = {'module_file_sha256': 'synthetic', 'run': {'status': 'BUDGET_EXHAUSTED',
           'exploration': {'status': 'BUDGET_EXHAUSTED', 'stage_reached': 'march', 'primary_anchor': pa},
           'evaluation_log': [{'log_index': 0, 'theta_natural': other}, {'log_index': 3, 'theta_natural': theta}]}}
    if mutate_rec:
        mutate_rec(rec)
    r = wjson(d / 'PHASE1_CALIBRATION_RECORD_BUDGET_EXHAUSTED_synthetic.json', rec)
    snap = {'schema': 'PHASE1_SNAPSHOT_C2V001', 'module': 'phase1_c2v003', 'phase1_status': 'BUDGET_EXHAUSTED', 'b_p1': 4,
            'u_A': {'log_index': 3, 'source': pa['source'], 'purpose': pa['purpose'], 'u': u, 'u_hex': [float(x).hex() for x in u],
                    'theta_natural': theta},
            'record': {'file': os.path.basename(r['path']), 'registry_file': 'PHASE1_CALIBRATION_REGISTRY.jsonl',
                       'record_file_sha256': r['sha256']}}
    if mutate_snap:
        mutate_snap(snap)
    return wjson(d / 'SNAPSHOT_C2V001.json', snap)


def ua_doc(theta, snapshot):
    return {'schema': L.SCHEMA_UA_POINT, 'theta': theta, 'theta_key': L.theta_key(theta), 'phase1_snapshot': snapshot,
            'coordinate_mode': 'DDO154_DISTANCE_FIXED_AT_REGISTERED'}


def base_spec(theta, eps, lo):
    st = L.load_static()
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


def c3t_registry(tag, base_ref, theta, mutate=None):
    """The certificate registry that holds point_identity(S1_UA_C3T) (as CP-1's assembler would write it)."""
    base = L.strict_json(L.verify_pin(base_ref))
    pending, _, _ = L.build_case(base, base_ref['sha256'], L.theta_key(theta), L.S1_C3T, L.load_static(), None)
    ident = L.point_identity(pending)
    entry = {'identity': ident, 'eps_certificate': FX_CERT('c3t_eps'), 'lo_certificate': FX_CERT('c3t_lo'),
             'bundle': FX_CERT('c3t_eps')}
    pts = {L.digest(ident): entry}
    if mutate:
        mutate(pts, ident)
    d = mkdir(RUN / 'fx' / ('registry_%s_%d' % (tag, len(os.listdir(str(RUN / 'fx'))))))
    return wjson(d / 'CERTIFICATE_REGISTRY_SYNTHETIC.json', {'schema': 'SYNTHETIC_REGISTRY', 'points': pts})


_CERTS = {}


def FX_CERT(k):
    if not _CERTS:
        for n in ('c3t_eps', 'c3t_lo'):
            _CERTS[n] = L.pin_of(str(RUN / 'fx' / 'certs' / (n + '.json')))
    return dict(_CERTS[k])


# ---------------------------------------------------------------------------------------------- guard012 fixtures
DIRECT_SRC = '''import json
DIRECT_CONTEXT_API = 'UNT_STEP4_DIRECT_PREFLIGHT_CX1V001'
class _Ctx:
    def __init__(self, C, config):
        self.C, self.config = C, config
    def _block(self, spec):
        f = getattr(self.C, 'validate_spec_block', None)
        return f(spec) if f is not None else self.C.validate_block(spec['numerics'])
    def certificate_policy_gate(self):
        return {'ok': True, 'reasons': []}
    def certificate_check(self, spec, phase):
        self._block(spec)
        u = spec['numerics']['uv_tail']
        b = ['CERTIFICATE_SLOT_NOT_A_PIN:' + k for k in ('eps_certificate', 'lo_certificate') if not isinstance(u.get(k), dict)]
        return {'ok': not b, 'blockers': b}
    def sensitivity_gate(self, spec):
        return {'ok': True, 'reasons': []}
    def prelaunch_check(self, spec):
        self._block(spec)
        return json.loads(json.dumps(spec))
def build(C, config, guard=None, admission=None):
    return _Ctx(C, config)
'''
POLICY_SRC = '''APPROVED_V007_SEALS = %s
def check_numerics(ncfg, block, n, O=None, validate_block=None, driver_sha=None, synthetic=False):
    validate_block(block)
    return None, {'ok': True, 'reasons': []}
'''


def build_g12(fx):
    g = mkdir(fx.root / 'g12')
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
    mods = {'direct': wbytes(g / 'syn_direct_context.py', DIRECT_SRC.encode()),
            'custody': wbytes(g / 'syn_custody_deriver.py', b'def derive_custody(**kw):\n    return {}\n'),
            'enumerator': wbytes(g / 'syn_state_enumerator.py', b'def enumerate_states(**kw):\n    return []\n'),
            'producer': wbytes(g / 'syn_producer.py', b'def produce(**kw):\n    return None\n')}
    fx.mods = mods
    fx.context = {'successor': L.const_pin('WRAPPER_S1K3'), 'q5b1': {'path': Q5B1[0], 'sha256': Q5B1[1]}}
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


def sources_for(fx, policy, context, drop_driver=False, extra=()):
    s = {L.PINS[k][0]: L.PINS[k][1] for k in ('LAUNCHER', 'GUARD', 'MONITOR', 'DRIVER', 'CORE', 'WRAPPER_S1K3')}
    for p, h in WRAPPER_DEPS:
        s[p] = h
    if drop_driver:
        s.pop(L.PINS['DRIVER'][0])
    for m in fx.mods.values():
        s[m['path']] = m['sha256']
    s[policy['path']] = policy['sha256']
    s[context['path']] = context['sha256']
    for e in extra:
        s[e['path']] = e['sha256']
    return s


def partial_cfg(fx, policy, context, v007=None, drop_driver=False, extra=()):
    return {'schema': 'UNT_STEP4_ADMISSION_CX1V001', 'authority': fx.G.AUTHORITY, 'status': 'ROOT_AUTHORIZED',
            'sources': sources_for(fx, policy, context, drop_driver, extra), 'v007': v007 or fx.v007,
            'adoption_policy': policy, 'config': fx.c1, 'context_module': context, 'direct_context': fx.mods['direct'],
            'tail_off_policy': None}


def make_admitted_plan(fx, tag, case, *, policy='ok', v007=None, status='ROOT_AUTHORIZED', core_priority=None,
                       drop_driver=False, prelaunch_tamper=False, force_plan=None, batch=None, overlap=False,
                       context='successor', fill_tag='off', fill_override=None):
    """spec -> native prelaunch record (real guard012) -> plan (lib.make_plan) -> admission (synthetic root bytes).
    fill_override (c2v002a, BLK-1 tests): a fill-record pin used in place of fill_tag's (plan s1 block and s1_overlap)."""
    fx.n_adm += 1
    d = mkdir(fx.g / ('adm_%03d_%s' % (fx.n_adm, tag)))
    fill = fx.fill[fill_tag] if fill_override is None else {'rec': L.pinned_json(fill_override), 'pin': fill_override}
    spec_ref = fill['rec']['cases'][case]['spec']
    pol = fx.policy[policy]
    ctx = fx.context[context]
    extra = (L.self_pin(),) if overlap else ()
    cfgp = partial_cfg(fx, pol, ctx, v007, drop_driver, extra)
    call = {'case': case, 'spec': spec_ref, 'driver': L.const_pin('DRIVER'), 'tail_on': True}
    try:
        pre = fx.G.native_preflight(cfgp, call)
    except Exception as exc:                     # an as-built refusal: a placeholder record so the plan can be written
        pre = {'schema': 'UNT_STEP4_PRELAUNCH_CX1V001', 'case': case, 'spec': spec_ref, 'driver': L.const_pin('DRIVER'),
               'config': fx.c1, 'adoption_verdict': (v007 or fx.v007)['verdict'], 'checks': {'placeholder': str(exc)},
               'adoption_checked': True}
    if prelaunch_tamper:
        pre = copy.deepcopy(pre)
        pre['checks']['normalized_sha256'] = '0' * 64
    pre_ref = wjson(d / 'prelaunch.json', pre)
    r = L.make_plan(fill['pin'], case, pre_ref, attempt=1, output_root=fx.out_root + '/' + d.name, dry=True, overlap=overlap)
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
    fields = r['sidecar']['admission_fields_for_root']
    adm.update(status=status, plan=plan_ref, source_review=review, route_a_admission=rule,
               core_priority=core_priority or dict(fields['core_priority']), case_order=[case],
               caps={case: {k: c[k] for k in ('wall_cap_s', 'rss_cap_bytes', 'output_cap_bytes')}},
               calls={case: {'spec': c['spec'], 'driver': c['driver'], 'prelaunch': c['prelaunch']}})
    if overlap:
        adm['s1_overlap'] = fields['s1_overlap']
    adm_ref = wjson(d / 'admission.json', adm, indent=2)
    return {'plan': plan_ref, 'admission': adm_ref, 'dir': d, 'prelaunch': pre_ref, 'plan_doc': plan, 'sidecar': r['sidecar']}


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
              admission='default', free=80, inject=True):
    gate, clock, calls = make_gate(snapshot if snapshot is not None else snap())
    box = []
    kw = dict(guard=fx.G, gate=gate, memory_free=lambda: free) if inject else {}
    out = L.launch(adm['plan'], adm['admission'] if admission == 'default' else admission, reg or fx.reg, v6 or fx.v6,
                   lcfg or fx.lcfg['INACTIVE'], mode=mode, confirm=confirm, spawn=spawn_stub(box),
                   sleep=clock.sleep, record_path=record, disk_batch=False, env=env, **kw)
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
    fx.radii = [float(x) for x in L.load_compare(L.const_pin('COMPARE_R14')).registered_row_radii(fx.st['ids'])]
    fx.base_v = {i: 10.0 + 3.0 * n for n, i in enumerate(fx.st['ids'])}


def ro1_block(armed=True, worker=RO1_PARALLEL):
    return {'rule': 'RO1', 'fired': False, 'events': [], 'armed': armed,
            'worker_sha256': worker if armed else None, 'binding_sha256': RO1_BINDING if armed else None}


def make_result(fx, case, fill_tag, vfinal, *, amp=0.004, r=0.1, flagged=False, ea=1e-5, status='COMPLETED', valid=True,
                receipt='FINISHED', packet=None, phys_tweak=None, cb_override=None, driver=None, s9=False, probe=True,
                extra_ns=None, failure_bracket=False, write_result=True, radii=None, ro1='default', side_paths=None):
    fx.n_run += 1
    d = fx.runs_dir / ('%03d_%s' % (fx.n_run, case))
    rec = fx.fill[fill_tag]['rec']
    spec_ref = rec['cases'][case]['spec'] if case in L.S1_CASES else rec['base_spec']
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
           'M_T_accepted': 0.3 if flagged else 0.01, 'accepted_iteration': 7,
           'E_A_rows_km_s_accepted': [ea] * 12 if not isinstance(ea, list) else ea}
    if probe:
        uvt['probe_R_m'] = list(radii) if radii is not None else fx.radii
    att = wjson(d / 'route_a_attempt_result.json', {'result': {'uv_tail': uvt}})
    rao = {'result_path': att['path'], 'result_sha256': att['sha256']}
    if ro1 == 'default':
        rao['ro1'] = ro1_block()
    elif ro1 is not None:
        rao['ro1'] = ro1
    res = {'schema': 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001', 'status': status, 'valid': valid, 'reasons': [],
           'driver_sha256': driver or L.R5_SHA, 'call_spec_sha256': spec_ref['sha256'],
           'rows': [{'id': i, 'speed_km_s': passes[-1]['rows'][n]['speed_km_s']} for n, i in enumerate(ids)] if not s9 else
           [{'id': i, 'speed_km_s': prev[i]} for i in ids],
           'passes': passes, 'final_pass': 6, 'normalized_spec': ns, 'route_a_outcome': rao, 'stage_records': []}
    if failure_bracket:
        sd = mkdir(d / 'stage_body')
        mkdir(sd / 'columns')
        wjson(sd / 'columns' / 'finish.json', {'failures': [{'index': 5, 'message': 'BRACKET_MISS: synthetic'}]})
        res['stage_records'] = [{'name': 'body', 'kind': 'columns', 'exit_code': 1, 'stage_dir': str(sd)}]
        res['status'], res['valid'] = 'FAILED_AT_STAGE', False
        res['normalized_spec']['numerics']['brackets'] = fx_ra4()
    if side_paths:
        side_paths(res)
    rr = wjson(d / 'result.json', res)
    return {'result_dir': str(d), 'receipt': str(d) + '.receipt.json', 'result_sha256': rr['sha256']}


def fx_ra4():
    return L.load_compare(L.const_pin('COMPARE_R14')).ra4_block_expected()


def attest(fx, case, run, gate, status='PASS', producer=None):
    fx.n_run += 1
    ev = wbytes(fx.r / ('evidence_%03d_%s_%s.txt' % (fx.n_run, case, gate)), b'synthetic evidence\n')
    return wjson(fx.r / ('attest_%03d_%s_%s.json' % (fx.n_run, case, gate)),
                 {'schema': L.SCHEMA_ATTEST, 'gate': gate, 'run': case, 'result_sha256': run.get('result_sha256'),
                  'status': status, 'producer': producer or fx.att_producer, 'evidence': ev})


def manifest(fx, runs, *, fill_tag='off', drop_attest=None, fail_attest=None, reg=None, v6=None, u_a_status=None,
             anchor=None, compare=None, extra=None, producer=None):
    m = {'schema': L.SCHEMA_MANIFEST, 'registration': reg or fx.reg, 'v6': v6 or fx.v6,
         'fill_record': fx.fill[fill_tag]['pin'], 'compare': compare or L.const_pin('COMPARE_R14'), 'runs': {}}
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
                e['attestations'][g] = attest(fx, c, run, g, 'FAIL' if fail_attest == (c, g) else 'PASS', producer)
        m['runs'][c] = e
    if extra:
        m.update(extra)
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
    k3, k4, k4p = k3 or {}, k4 or {}, k4p or {}
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
    reg = L.pinned_json(FX.registry['off'])
    ent = list(reg['points'].values())[0]
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
          and c3['successor_validate_spec_block'] == 'PASS' and c4['successor_validate_spec_block'] == 'PASS'
          and rec['blockers'] == [] and s3['numerics']['uv_tail']['eps_certificate'] == ent['eps_certificate']
          and rec['c3t_registry'] == FX.registry['off'] and rec['phase1_snapshot'] == FX.snap['off'])
    return ok, {'c3_changed': c3['changed_paths'], 'branch': rec['branch']['branch'], 'c3_core': c3['as_built_core_validate_block'],
                'c3_successor': c3['successor_validate_spec_block'], 'blockers': rec['blockers']}


@test('F-P2', 'MUST_PASS')
def t_fill_seed():
    b = FX.fill['seed']['rec']['branch']
    ok = (b['branch'] == 'AT_ANCHOR' and b['seed_bits_equal'] is True and b['anchor_alias_within_rtol'] is True
          and all(v == 0.0 for v in b['u_A_minus_u_seed'].values()))
    return ok, {'branch': b['branch'], 'rel_dev': b['relative_deviation_from_anchor']}


@test('F-P3', 'MUST_PASS')
def t_dry_plan():
    before = sorted(os.listdir(FX.root))
    rec = L.fill(FX.ua['off'], FX.base['off'], CFG_PIN, c3t_registry=None, dry=True)
    after = sorted(os.listdir(FX.root))
    ok = (before == after and rec['dry'] is True and 'record' not in rec
          and any('no certificate-registry entry' in b for b in rec['blockers'])
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
    tu = FX.st['coord']['trial_point']['engine_trial_u']
    out['u_map'] = [L.u_value(FX.seed[n], FX.cs[n]) for n in L.VARYING] == tu
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
          and Path(r['written']['plan']['path']).is_file()
          and r['sidecar']['admission_fields_for_root']['core_priority'] == L.CORE_PRIORITY
          and 's1_overlap' not in r['sidecar']['admission_fields_for_root'])
    return ok, {'outdir': c['outdir'], 'caps': dbp}


@test('F-P6', 'MUST_PASS')
def t_plan_c3t_now_written():
    """c2v001 F-P6 (the C3T plan was blocked by the as-built core) is now a MUST_PASS: the successor admits C3T."""
    d = mkdir(RUN / 'plan_c3t')
    pre = wjson(d / 'prelaunch_placeholder.json',
                {'schema': 'UNT_STEP4_PRELAUNCH_CX1V001', 'case': L.S1_C3T, 'spec': FX.fill['off']['rec']['cases'][L.S1_C3T]['spec'],
                 'driver': L.const_pin('DRIVER'), 'adoption_checked': True})
    r = L.make_plan(FX.fill['off']['pin'], L.S1_C3T, pre, attempt=1, out_path=str(d / 'PLAN_S1_UA_C3T.json'), overlap=True)
    f = r['sidecar']['admission_fields_for_root']
    ok = (r['written'] is not None and (d / 'PLAN_S1_UA_C3T.json').is_file() and r['sidecar']['blockers'] == []
          and r['sidecar']['as_built_core_validate_block'] == 'REFUSED: kept K must be 4'
          and r['sidecar']['successor_validate_spec_block'] == 'PASS' and f['core_priority'] == L.CORE_PRIORITY_S1_OVERLAP
          and f['s1_overlap']['replay_module'] == L.self_pin() and f['context_module'] == L.const_pin('WRAPPER_S1K3')
          and any('K=4-only' in n for n in r['sidecar']['notes']))
    return ok, {'blockers': r['sidecar']['blockers'], 'notes': r['sidecar']['notes']}


@test('F-P7', 'MUST_PASS')
def t_c3t_cp1_spec():
    """The CP-1 input form of S1_UA_C3T: point key equal to the filled C3T spec's; slots PENDING; written once."""
    d = mkdir(RUN / 'cp1_spec')
    r = L.write_c3t_cp1_spec(FX.ua['off'], FX.base['off'], CFG_PIN, out_dir=str(d))
    s = L.strict_json(L.verify_pin(r['spec']))
    filled = L.strict_json(L.verify_pin(FX.fill['off']['rec']['cases'][L.S1_C3T]['spec']))
    diff = L.diff_paths(filled, s)
    ok = (r['point_key'] == FX.fill['off']['rec']['cases'][L.S1_C3T]['point_key'] and r['successor_validate_spec_block'] == 'PASS'
          and s['numerics']['uv_tail']['eps_certificate'] == 'PENDING_UV_TAIL_CERTIFICATE'
          and all(p.startswith('numerics.uv_tail.') for p in diff) and diff)
    again = expect_refusal(lambda: L.write_c3t_cp1_spec(FX.ua['off'], FX.base['off'], CFG_PIN, out_dir=str(d)), 'OUTPUT_EXISTS')
    return ok and again[0], {'point_key': r['point_key'][:16], 'diff': diff}


def _base_variant(tag, mutate, theta=None):
    th = dict(theta or FX.off)
    b = base_spec(th, FX.certs['c4t_eps'], FX.certs['c4t_lo'])
    mutate(b)
    FX.n_run += 1
    return wjson(FX.root / ('base_variant_%03d_%s.json' % (FX.n_run, tag)), b)


def _ua_variant(tag, theta, key=None, snapshot=None):
    FX.n_run += 1
    d = ua_doc(theta, snapshot or FX.snap['off'])
    if key:
        d['theta_key'] = key
    return wjson(FX.root / ('ua_variant_%03d_%s.json' % (FX.n_run, tag)), d)


def _fill(ua, base, registry='default'):
    return lambda: L.fill(ua, base, CFG_PIN, c3t_registry=FX.registry['off'] if registry == 'default' else registry, dry=True)


@test('F-F1', 'MUST_FAIL')
def t_wrong_theta_bits():
    b = _base_variant('ulp', lambda s: s['physical'].__setitem__('common_scale_s', math.nextafter(s['physical']['common_scale_s'], 1.0)))
    return expect_refusal(_fill(FX.ua['off'], b), 'THETA_PHYSICAL_MISMATCH')


@test('F-F2', 'MUST_FAIL')
def t_theta_key():
    return expect_refusal(_fill(_ua_variant('key', FX.off, key='f' * 64), FX.base['off']), 'THETA_KEY_MISMATCH')


@test('F-F3', 'MUST_FAIL')
def t_phase1_binding():
    """c2v001 F-F3 ported (B2, the verifier's E3): the seed snapshot's engine log names the off point, but its primary
    anchor is the seed, so the off point does not bind."""
    return expect_refusal(_fill(_ua_variant('p1', FX.off, snapshot=FX.snap['seed']), FX.base['off']), 'PHASE1_PRIMARY_ANCHOR_NOT_U_A')


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
def t_c3t_registry_required():
    d = mkdir(RUN / 'fill_noregistry')
    return expect_refusal(lambda: L.fill(FX.ua['off'], FX.base['off'], CFG_PIN, c3t_registry=None, out_dir=str(d), dry=False),
                          'C3T_REGISTRY_REQUIRED')


@test('F-F13', 'MUST_FAIL')
def t_exclusive():
    d = Path(FX.fill['off']['rec']['record']['path']).parent
    return expect_refusal(lambda: L.fill(FX.ua['off'], FX.base['off'], CFG_PIN, c3t_registry=FX.registry['off'], out_dir=str(d)),
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


# ---- new template MUST_FAILs (B2 and note 10)
@test('F-F17', 'MUST_FAIL')
def t_phase1_status():
    s = phase1_snapshot('off', FX.off, FX.seed, mutate_snap=lambda d: d.__setitem__('phase1_status', 'NO_IDENTIFIED_DIRECTION'))
    return expect_refusal(_fill(_ua_variant('st', FX.off, snapshot=s), FX.base['off']), 'PHASE1_STATUS_NOT_BUDGET_EXHAUSTED')


@test('F-F18', 'MUST_FAIL')
def t_phase1_record_anchor_differs():
    s = phase1_snapshot('off', FX.off, FX.seed, mutate_rec=lambda r: r['run']['exploration']['primary_anchor'].__setitem__(
        'theta_natural', FX.seed))
    return expect_refusal(_fill(_ua_variant('rpa', FX.off, snapshot=s), FX.base['off']), 'PHASE1_PRIMARY_ANCHOR_NOT_U_A')


@test('F-F19', 'MUST_FAIL')
def t_phase1_snapshot_ulp():
    def m(d):
        d['u_A']['theta_natural'] = dict(d['u_A']['theta_natural'])
        d['u_A']['theta_natural']['ell_F_m'] = math.nextafter(d['u_A']['theta_natural']['ell_F_m'], 1.0)
    s = phase1_snapshot('off', FX.off, FX.seed, mutate_snap=m)
    return expect_refusal(_fill(_ua_variant('ulp1', FX.off, snapshot=s), FX.base['off']), 'PHASE1_PRIMARY_ANCHOR_NOT_U_A')


@test('F-F20', 'MUST_FAIL')
def t_phase1_record_status():
    s = phase1_snapshot('off', FX.off, FX.seed, mutate_rec=lambda r: r['run'].__setitem__('status', 'COMPLETE'))
    return expect_refusal(_fill(_ua_variant('rst', FX.off, snapshot=s), FX.base['off']), 'PHASE1_STATUS_NOT_BUDGET_EXHAUSTED')


@test('F-F21', 'MUST_FAIL')
def t_phase1_u_bits():
    s = phase1_snapshot('off', FX.off, FX.seed, mutate_rec=lambda r: r['run']['exploration']['primary_anchor'].__setitem__(
        'u', [x + 1e-9 for x in r['run']['exploration']['primary_anchor']['u']]))
    return expect_refusal(_fill(_ua_variant('ub', FX.off, snapshot=s), FX.base['off']), 'PHASE1_PRIMARY_ANCHOR_NOT_U_A')


@test('F-F22', 'MUST_FAIL')
def t_phase1_record_name_path():
    s = phase1_snapshot('off', FX.off, FX.seed, mutate_snap=lambda d: d['record'].__setitem__('file', '../x.json'))
    return expect_refusal(_fill(_ua_variant('rn', FX.off, snapshot=s), FX.base['off']), 'PHASE1_RECORD_FILE_NAME')


@test('F-F23', 'MUST_FAIL')
def t_registry_point_missing():
    reg = c3t_registry('off', FX.base['off'], FX.off, mutate=lambda pts, ident: pts.clear())
    return expect_refusal(_fill(FX.ua['off'], FX.base['off'], reg), 'C3T_REGISTRY_POINT_MISSING')


@test('F-F24', 'MUST_FAIL')
def t_registry_identity_mismatch():
    def m(pts, ident):
        e = list(pts.values())[0]
        e['identity'] = copy.deepcopy(ident)
        e['identity']['numerics']['picard']['passes'] = e['identity']['numerics']['picard']['passes'] + 1
    reg = c3t_registry('off', FX.base['off'], FX.off, mutate=m)
    return expect_refusal(_fill(FX.ua['off'], FX.base['off'], reg), 'C3T_REGISTRY_IDENTITY_MISMATCH')


@test('F-F25', 'MUST_FAIL')
def t_registry_cert_pin():
    def m(pts, ident):
        e = list(pts.values())[0]
        e['eps_certificate'] = {'path': e['eps_certificate']['path'], 'sha256': '3' * 64}
    reg = c3t_registry('off', FX.base['off'], FX.off, mutate=m)
    return expect_refusal(_fill(FX.ua['off'], FX.base['off'], reg), 'C3T_EPS_CERTIFICATE_PIN_BYTES_CHANGED')


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
          and out['gate']['decide']['admit'] is True and out['gate']['a133_rule']['sum_gb'] <= 103.0
          and out['gate']['memory_pressure_free_percent'] == 80 and out['gate']['r5_route_a_trees'] == [])
    return ok, {'decision': out['decision'], 'refusal': out['refusal'], 'gate': out['gate']}


@test('L-P2', 'MUST_PASS')
def t_launch_record_then_spawn():
    """c2v001 L-P2 ported: launch mode refuses injected guards and gates (note 7), so the launch steps are tested on a dry
    admission: the exclusive record, then the spawn (stub), then the exclusive outcome record (note 5)."""
    adm = make_admitted_plan(FX, 'launch', L.S1_C4T)
    rec = str(adm['dir'] / 'PRELAUNCH_DECISION.json')
    out, probes, box = do_launch(FX, adm, record=rec)
    env = {'UNT_STEP4_ADMISSION_PATH': adm['admission']['path'], 'UNT_STEP4_ADMISSION_SHA256': adm['admission']['sha256']}
    L.launch_after_record(out, out['launch_argv'], dict(env, **L.BLAS), spawn_stub(box), rec)
    written = L.strict_json(L.read_bytes(rec))
    oc = L.strict_json(L.read_bytes(rec + '.outcome.json'))
    ok = (out['decision'] == 'LAUNCHED' and len(box) == 1 and out['trace'][-2:] == ['record', 'spawn']
          and box[0]['argv'][-2:] == [adm['plan']['path'], '--execute-root-only'] and L.PINS['LAUNCHER'][0] in box[0]['argv']
          and written['decision'] == 'ADMITTED' and oc['decision'] == 'LAUNCHED' and oc['schema'] == L.SCHEMA_LAUNCH_OUTCOME
          and 'UNT_STEP4_ADMISSION_SHA256' in box[0]['env_keys'] and 'OPENBLAS_NUM_THREADS' in box[0]['env_keys'])
    return ok, {'decision': out['decision'], 'argv_tail': box[0]['argv'][-4:] if box else None}


@test('L-P3', 'MUST_PASS')
def t_launch_overlap():
    """guard012 overlap: campaign ACTIVE (root's window attestation), the overlap admission with this library as the
    replay module, one r5 campaign tree in route A (the gate's allowance); guard012's live gate and the lib's gate admit."""
    adm = make_admitted_plan(FX, 'ovl', L.S1_C4T, overlap=True)
    s = snap([tree(600, 9.0, str(FX.g / 'campaign_route_a_tree'), driver=L.R5_SHA)])
    out, probes, box = do_launch(FX, adm, lcfg=FX.lcfg['ACTIVE'], snapshot=s)
    ok = (out['decision'] == 'ADMITTED' and _ok_controls(out) and 'guard012_overlap_gate' in out['trace']
          and len(out['gate']['r5_route_a_trees']) == 1 and out['campaign_window'] == 'SINGLE_CALL_WAVE_START' and box == [])
    return ok, {'decision': out['decision'], 'refusal': out['refusal'], 'trace': out['trace']}


@test('L-P4', 'MUST_PASS')
def t_registration_real():
    """c2v001 L-F12 ported: the real registration C2V002 is now entered on root's V006 entry line (A150); read against the
    real V006 at its constant path (content not printed)."""
    real = L.pin_of(REAL_V6_PATH)
    with use_v6(real):
        ok = L.registration_in_force(FX.reg, real) is True
    return ok, {'v6_sha_at_test': real['sha256'], 'registration_sha': FX.reg['sha256']}


@test('L-P5', 'MUST_PASS')
def t_launch_c3t_successor():
    """S1_UA_C3T passes control 3 with the wrapper successor as the context module (c2v001 L-F7's blocker removed)."""
    adm = make_admitted_plan(FX, 'c3t_ok', L.S1_C3T)
    out, probes, box = do_launch(FX, adm)
    return out['decision'] == 'ADMITTED' and _ok_controls(out), {'decision': out['decision'], 'refusal': out['refusal']}


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
    """c2v001 L-F5 ported: an admission whose core_priority is not the launch config's state is refused before guard012."""
    cp = dict(L.CORE_PRIORITY, campaign_inactive=False)
    adm = make_admitted_plan(FX, 'c2c', L.S1_C4T, core_priority=cp)
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'S1_ADMISSION_CORE_PRIORITY_NOT_THE_LAUNCH_CONFIG_STATE', L.CONTROLS[1], probes, 0, box)


@test('L-F6', 'MUST_FAIL')
def t_c3_replay():
    adm = make_admitted_plan(FX, 'c3r', L.S1_C4T, prelaunch_tamper=True)
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'PRELAUNCH_REPLAY_MISMATCH', L.CONTROLS[2], probes, 0, box)


@test('L-F7', 'MUST_FAIL')
def t_c3_c3t_as_built():
    """The as-built context (q5b1 over core dc895f8a) still refuses S1_UA_C3T at native preflight."""
    adm = make_admitted_plan(FX, 'c3t', L.S1_C3T, context='q5b1')
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
    """c2v001 L-F11 ported (note 1): a V006 that does not carry root's entry line for the registration."""
    v6 = syn_v6(with_registration=False, tag='v6_noreg')
    adm = make_admitted_plan(FX, 'reg', L.S1_C4T)
    with use_v6(v6):
        out, probes, box = do_launch(FX, adm, v6=v6)
    return _refused(out, 'S1_REGISTRATION_NOT_IN_FORCE', None, probes, 0, box)


@test('L-F12', 'MUST_FAIL')
def t_registration_rejection_note():
    """Note 1 / the verifier's E7: the sha mentioned in a rejection note (no entry line) is not in force."""
    v6 = syn_v6(with_registration=False, extra_lines=('Draft %s REJECTED by root' % L.REGISTRATION_SHA,
                                                      '- note: sha256 `%s` superseded' % L.REGISTRATION_SHA), tag='v6_rej')
    with use_v6(v6):
        ok, det = expect_refusal(lambda: L.registration_in_force(FX.reg, v6), 'S1_REGISTRATION_NOT_IN_FORCE')
    return ok, det


@test('L-F13', 'MUST_FAIL')
def t_overlap_window():
    """c2v001 L-F13 ported: ACTIVE needs root's campaign-window attestation (registration section 11 rule 4, C14)."""
    adm = make_admitted_plan(FX, 'ovl_nowin', L.S1_C4T, overlap=True)
    out, probes, box = do_launch(FX, adm, lcfg=FX.lcfg['ACTIVE_NO_WINDOW'])
    return _refused(out, 'S1_OVERLAP_CAMPAIGN_WINDOW_REQUIRED', None, probes, 0, box)


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
    out, probes, box = do_launch(FX, adm, mode='launch', confirm='0' * 64, env=env, record=str(adm['dir'] / 'R.json'), inject=False)
    return _refused(out, 'LAUNCH_CONFIRMATION_REQUIRED', None, probes, 0, box)


@test('L-F21', 'MUST_FAIL')
def t_env():
    adm = make_admitted_plan(FX, 'env', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, mode='launch', confirm=adm['plan']['sha256'], env={}, record=str(adm['dir'] / 'R.json'),
                                 inject=False)
    return _refused(out, 'PUBLISHED_ADMISSION_ENV_MISMATCH', None, probes, 0, box)


@test('L-F23', 'MUST_FAIL')
def t_record_required():
    adm = make_admitted_plan(FX, 'rec', L.S1_C4T)
    env = {'UNT_STEP4_ADMISSION_PATH': adm['admission']['path'], 'UNT_STEP4_ADMISSION_SHA256': adm['admission']['sha256']}
    out, probes, box = do_launch(FX, adm, mode='launch', confirm=adm['plan']['sha256'], env=env, record=None, inject=False)
    return _refused(out, 'PRELAUNCH_RECORD_PATH_REQUIRED', None, probes, 0, box)


@test('L-F22', 'MUST_FAIL')
def t_step2():
    adm = make_admitted_plan(FX, 'st2', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, lcfg=FX.lcfg_step2)
    return _refused(out, 'STEP2_ROUTE_A_NOT_INACTIVE', None, probes, 0, box)


# ---- new launch MUST_FAILs (notes 1, 2, 4, 5, 6, 7; the verifier's E5, E6, E7)
@test('L-F24', 'MUST_FAIL')
def t_launch_mode_injection():
    """Note 7: launch mode refuses injected guard / gate / memory_free (nothing probed, nothing spawned)."""
    adm = make_admitted_plan(FX, 'inj', L.S1_C4T)
    env = {'UNT_STEP4_ADMISSION_PATH': adm['admission']['path'], 'UNT_STEP4_ADMISSION_SHA256': adm['admission']['sha256']}
    out, probes, box = do_launch(FX, adm, mode='launch', confirm=adm['plan']['sha256'], env=env, record=str(adm['dir'] / 'R.json'))
    ok, det = _refused(out, 'LAUNCH_MODE_INJECTION_REFUSED', None, probes, 0, box)
    return ok and Path(adm['dir'] / 'R.json').is_file(), det


@test('L-F25', 'MUST_FAIL')
def t_spawn_exception():
    """Note 5 / E6: a spawn exception is recorded (SPAWN_FAILED) in <record>.outcome.json; nothing propagates."""
    adm = make_admitted_plan(FX, 'e6', L.S1_C4T)
    rec = str(adm['dir'] / 'PRELAUNCH_DECISION_E6.json')
    out, probes, box = do_launch(FX, adm, record=rec)

    def boom(argv, env):
        raise subprocess.TimeoutExpired(argv, 600)
    L.launch_after_record(out, out['launch_argv'], {}, boom, rec)
    oc = L.strict_json(L.read_bytes(rec + '.outcome.json'))
    ok = out['decision'] == 'SPAWN_FAILED' and oc['decision'] == 'SPAWN_FAILED' and 'TimeoutExpired' in oc['launcher_result']['exception']
    return ok, {'decision': out['decision'], 'outcome': oc['launcher_result']}


@test('L-F26', 'MUST_FAIL')
def t_inactive_but_r5_tree():
    """Note 2 / E5: the launch config says INACTIVE but the snapshot shows an r5 tree in route A."""
    s = snap([tree(800, 15.0, str(FX.g / 'campaign_tree_out'), driver=L.R5_SHA, nproc=2)])
    adm = make_admitted_plan(FX, 'e5', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, snapshot=s)
    return _refused(out, 'S1_CAMPAIGN_ROUTE_A_TREE_WHILE_ATTESTED_INACTIVE', None, None, 0, box)


@test('L-F27', 'MUST_FAIL')
def t_inactive_unknown_driver_tree():
    s = snap([tree(800, 3.0, str(FX.g / 'unknown_driver_tree'), driver=None, nproc=2)])
    adm = make_admitted_plan(FX, 'e5b', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, snapshot=s)
    return _refused(out, 'S1_CAMPAIGN_ROUTE_A_TREE_WHILE_ATTESTED_INACTIVE', None, None, 0, box)


@test('L-F28', 'MUST_FAIL')
def t_memory_pressure():
    """Note 4: memory_pressure free below 25 % right after Gate.decide refuses (unknown too)."""
    adm = make_admitted_plan(FX, 'mp', L.S1_C4T)
    out, probes, box = do_launch(FX, adm, free=24)
    a = _refused(out, 'MEMORY_PRESSURE_FREE_BELOW_25', None, None, 0, box)
    adm2 = make_admitted_plan(FX, 'mp2', L.S1_C4T)
    out2, _, box2 = do_launch(FX, adm2, free=None)
    b = _refused(out2, 'MEMORY_PRESSURE_FREE_BELOW_25', None, None, 0, box2)
    return a[0] and b[0], [a[1]['refusal'], b[1]['refusal']]


@test('L-F29', 'MUST_FAIL')
def t_internal_error():
    """Note 6: an unexpected error (a fill record without 'cases') is an INTERNAL_ERROR refusal naming the stage."""
    d = mkdir(RUN / 'broken_fill')
    rec = {k: v for k, v in FX.fill['off']['rec'].items() if k not in ('cases', 'record')}
    fpin = wjson(d / 'FILL_RECORD_NO_CASES.json', rec)
    adm = make_admitted_plan(FX, 'int', L.S1_C4T, force_plan=lambda p: p['s1'].__setitem__('fill_record', fpin))
    out, probes, box = do_launch(FX, adm, record=str(adm['dir'] / 'R.json'))
    ok, det = _refused(out, 'INTERNAL_ERROR', None, probes, 0, box)
    return ok and out['refusal']['stage'] == 'S1_CHECKS' and Path(adm['dir'] / 'R.json').is_file(), det


@test('L-F30', 'MUST_FAIL')
def t_overlap_two_r5():
    """guard012's allowance: with the campaign active, two r5 trees in route A refuse at guard012's live gate."""
    adm = make_admitted_plan(FX, 'ovl2', L.S1_C4T, overlap=True)
    s = snap([tree(600, 3.0, str(FX.g / 'r5_a'), driver=L.R5_SHA, nproc=2),
              tree(700, 3.0, str(FX.g / 'r5_b'), driver=L.R5_SHA, nproc=2)])
    out, probes, box = do_launch(FX, adm, lcfg=FX.lcfg['ACTIVE'], snapshot=s)
    ok, det = _refused(out, 'S1_OVERLAP_R5_ROUTE_A_BEYOND_GATE_ALLOWANCE', None, None, 0, box)
    return ok and out['refusal']['stage'] == 'GUARD012_OVERLAP_GATE', det


@test('L-F31', 'MUST_FAIL')
def t_overlap_admission_without_active_config():
    adm = make_admitted_plan(FX, 'ovl_cfg', L.S1_C4T, overlap=True)
    out, probes, box = do_launch(FX, adm, lcfg=FX.lcfg['INACTIVE'])
    return _refused(out, 'S1_ADMISSION_CORE_PRIORITY_NOT_THE_LAUNCH_CONFIG_STATE', L.CONTROLS[1], probes, 0, box)


@test('L-F32', 'MUST_FAIL')
def t_registration_not_implemented():
    syn = wbytes(fresh('reg_syn') / 'S1_REGISTRATION_SYNTHETIC.md', b'# synthetic registration\n')
    return expect_refusal(lambda: L.registration_in_force(syn, FX.v6), 'S1_REGISTRATION_NOT_IMPLEMENTED_HERE')


@test('L-F33', 'MUST_FAIL')
def t_v6_path_not_root():
    """Note 1 / E7: a V006 pin at any other path is refused (the path is a library constant, not an input)."""
    other = wbytes(fresh('v6_other') / 'not_v6_rejection_note.md',
                   ('**Registration in force:** sha256 `%s`\n' % L.REGISTRATION_SHA).encode())
    return expect_refusal(lambda: L.registration_in_force(FX.reg, other), 'V6_PATH_NOT_THE_ROOT_FILE')


@test('L-F34', 'MUST_FAIL')
def t_plan_guard011():
    """A plan on guard011/launcher012 (c2v001's packet) is refused: c2v002 runs only guard012/launcher013."""
    def fp(p):
        p['guard'] = L.const_pin('GUARD011')
        p['launcher'] = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_launcher_c2v012.py',
                         'sha256': '59c00707ea8f3dc42fb2349bd806d42758119354954f878299d56bd21933f2a9'}
    adm = make_admitted_plan(FX, 'g11', L.S1_C4T, force_plan=fp)
    out, probes, box = do_launch(FX, adm)
    return _refused(out, 'S1_PACKET_NOT_GUARD012_LAUNCHER013', None, probes, 0, box)


@test('L-F35', 'MUST_FAIL')
def t_overlap_replay_not_this_lib():
    """An overlap admission whose replay module is not this library is refused by the launch path before guard012."""
    other = wbytes(fresh('other_replay') / 'other_replay.py', b"S1_REPLAY_API = 'UNT_S1_FILL_REPLAY_C2V002'\n")
    adm = make_admitted_plan(FX, 'ovl_other', L.S1_C4T, overlap=True)
    doc = L.pinned_json(adm['admission'])
    doc['s1_overlap'] = dict(doc['s1_overlap'], replay_module=other)
    adm = dict(adm, admission=wjson(adm['dir'] / 'admission_other_replay.json', doc, indent=2))
    out, probes, box = do_launch(FX, adm, lcfg=FX.lcfg['ACTIVE'])
    return _refused(out, 'S1_OVERLAP_ADMISSION_NOT_THIS_PATH', L.CONTROLS[1], probes, 0, box)


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
          and 'UNTESTED at every other point' in out['label'] and out['compare'] == L.const_pin('COMPARE_R14')
          and all((out['validity'][c]['ro1'] or {}).get('worker_kind') == 'parallel' for c in L.RUNS)
          and out.get('fill_record_replayed') is True)                  # c2v002a: the fill record was replayed (BLK-1)
    return ok, {'code': out['code'], 'Dhat': out['statistic']['Dhat_S1'], 'effect': out['step5_effect']}


@test('R-P2', 'MUST_PASS')
def t_read_seed():
    runs = triple(FX, fill_tag='seed')
    out = read(FX, manifest(FX, runs, fill_tag='seed'))
    ok = out['code'] == 'PASS_AT_ADOPTION_POINT' and 'Phase-2 step-5 reads stay held' in out['step5_effect'] and 'S1-B' in out['next_step']
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
    ok = (all(isinstance(v, str) and len(v) == 64 for v in list(dg['compare'].values()) + list(dg['v005'].values()))
          and dg['compare'] == L.REVIEWED_COMPARES[L.PINS['COMPARE_R14'][1]]['functions'] and dg['compare_reviewed'] is True)
    return ok, {'n': len(dg['compare']), 'closure': dg['compare_closure_informational']}


@test('R-P6', 'MUST_PASS')
def t_read_r11_reviewed():
    """B1: r11 (a5d10cb1) is the other reviewed compare; the same triple reads PASS through it."""
    runs = triple(FX)
    out = read(FX, manifest(FX, runs, compare=L.const_pin('COMPARE_R11')))
    return out['code'] == 'PASS' and out['compare'] == L.const_pin('COMPARE_R11'), {'code': out['code']}


@test('R-P7', 'MUST_PASS')
def t_flag_cleared():
    """Note 13: a root flag ruling (entered in V006) clears the flagged K4 run; the reading is PASS."""
    runs = triple(FX, k4={'flagged': True})
    d = fresh('flag_ruling')
    fr = wjson(d / 'S1_FLAG_RULING.json', {'schema': L.SCHEMA_FLAG_RULING, 'run': L.S1_C4T,
                                           'result_sha256': runs[L.S1_C4T]['result_sha256'],
                                           'flags': ['TAIL_SOURCE_UNDERCONVERGED'], 'ruling': L.FLAG_CLEARED,
                                           'registration_sha256': L.REGISTRATION_SHA})
    v6 = syn_v6(extra_lines=('**S1 flag ruling:** K4 flag cleared, sha256 `%s`' % fr['sha256'],), tag='v6_flag')
    with use_v6(v6):
        out = read(FX, manifest(FX, runs, v6=v6, extra={'flag_rulings': {L.S1_C4T: fr}}))
    return out['code'] == 'PASS' and out['flag_rulings'][L.S1_C4T]['cleared'] is True, {'code': out['code'], 'sub': out.get('sub_code')}


@test('R-P8', 'MUST_PASS')
def t_decidability_boundary():
    """The verifier's E1b: E^A 0.0031 per run (pair 0.0062) is decidable on rows 06-08 (tau/8 = 0.00625); 0.0032 is not."""
    out = {}
    for ea in (0.0031, 0.0032):
        runs = triple(FX, k3={'ea': ea}, k4={'ea': ea}, k4p={'ea': ea})
        r = read(FX, manifest(FX, runs))
        out[ea] = [r['tests']['TH2_K3_K4']['noise'].get('decidable'), r['code']]
    return out[0.0031] == [True, 'PASS'] and out[0.0032][0] is False and out[0.0032][1] == 'UNDECIDABLE', out


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
    m = manifest(FX, runs, drop_attest=(L.K4P, 'SV7'))
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
    v6 = syn_v6(with_registration=False, tag='v6_read_noreg')
    with use_v6(v6):
        return expect_refusal(lambda: read(FX, manifest(FX, runs, v6=v6)), 'S1_REGISTRATION_NOT_IN_FORCE')


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


# ---- new reader MUST_FAILs (B1, B3, notes 8, 9, 11, 12, 13; the verifier's E2 and E4)
@test('R-F28', 'MUST_FAIL')
def t_compare_modified():
    """B1 / E4: r14 with `thresholded` patched to return True is not a reviewed compare: refused, nothing written."""
    raw = L.read_bytes(L.PINS['COMPARE_R14'][0])
    needle = b"def thresholded(stat, th, per_row=True):\n"
    mod = raw.replace(needle, needle + b"    return True\n", 1)
    cmp_ref = L.write_exclusive(str(fresh('cmp_mod') / 'compare_r14_modified_thresholded.py'), mod)
    d = {i: 0.2 for i in FX.st['ids']}
    d[ROW_FAIL] = 0.7
    m = manifest(FX, triple(FX, d=d), compare=cmp_ref)
    w = fresh('cmp_mod_out')
    ok, det = expect_refusal(lambda: read(FX, m, write=str(w)), 'COMPARE_NOT_REVIEWED')
    return ok and os.listdir(w) == [] and mod.count(needle) == 1, det


@test('R-F29', 'MUST_FAIL')
def t_compare_copy_elsewhere():
    """B1: the reviewed bytes at another path are not the reviewed compare (the path is part of the review)."""
    raw = L.read_bytes(L.PINS['COMPARE_R11'][0])
    cmp_ref = L.write_exclusive(str(fresh('cmp_copy') / 'kmax_tail_compare_c2v007_r11.py'), raw)
    m = manifest(FX, triple(FX), compare=cmp_ref)
    return expect_refusal(lambda: read(FX, m), 'COMPARE_NOT_REVIEWED')


@test('R-F30', 'MUST_FAIL')
def t_compare_digests():
    """B1: a reviewed sha whose recorded digests differ refuses (exercised by tampering the in-memory reviewed table)."""
    old = L.REVIEWED_COMPARES
    try:
        t = copy.deepcopy(old)
        t[L.PINS['COMPARE_R14'][1]]['functions']['thresholded'] = '0' * 64
        L.REVIEWED_COMPARES = t
        return expect_refusal(lambda: L.load_compare(L.const_pin('COMPARE_R14')), 'COMPARE_FUNCTION_DIGESTS_NOT_REVIEWED')
    finally:
        L.REVIEWED_COMPARES = old


@test('R-F31', 'MUST_FAIL')
def t_ea_record_refused():
    """B3 / E2: an EA replay record in the manifest is refused (the fallback is deleted); without it the runs whose
    uv_tail record lacks probe_R_m read INVALID INCOMPLETE_RECORD."""
    runs = triple(FX, k3={'probe': False, 'ea': 0.5}, k4={'probe': False, 'ea': 0.5}, k4p={'probe': False, 'ea': 0.5})
    ea_doc = {'schema': 'ANY_SCHEMA_NOT_CHECKED',
              'per_case': {c: {'result_sha256': runs[c]['result_sha256'], 'E_A_rows_km_s': [0.0] * 12} for c in L.RUNS}}
    ea_ref = wjson(fresh('ea') / 'syn_ea_record_no_radii.json', ea_doc)
    a = expect_refusal(lambda: read(FX, manifest(FX, runs, extra={'ea_record': ea_ref})), 'MANIFEST_EA_RECORD_NOT_ACCEPTED')
    b = _code(read(FX, manifest(FX, runs)), 'INVALID', 'INCOMPLETE_RECORD')
    return a[0] and b[0], [a[1], b[1]]


@test('R-F32', 'MUST_FAIL')
def t_permuted_radii():
    """B3: a uv_tail record whose probe_R_m is the registered radii permuted is not E^A of record."""
    rad = list(FX.radii)
    rad[0], rad[1] = rad[1], rad[0]
    runs = triple(FX, k4={'radii': rad})
    out = read(FX, manifest(FX, runs))
    return out['code'] in ('INVALID',) and out['code'] != 'PASS', {'code': out['code'], 'sub': (out.get('sub_code') or '')[:200]}


@test('R-F33', 'MUST_FAIL')
def t_ro1_unarmed():
    """Note 8: RO1 is computed with R14 check_ro1_record; an unarmed RO1 record (C3T requires RO1) is INVALID."""
    runs = triple(FX, k3={'ro1': ro1_block(armed=False)})
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID')
    return ok and 'RO1_NOT_ARMED' in out['validity'][L.S1_C3T]['codes'], det


@test('R-F34', 'MUST_FAIL')
def t_ro1_serial_worker():
    runs = triple(FX, k4={'ro1': ro1_block(worker=RO1_SERIAL)})
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID')
    return ok and 'RO1_WORKER_IS_NOT_THE_PARALLEL_CUSTODY_WORKER_FOR_THE_COLUMN_WORKERS' in out['validity'][L.S1_C4T]['codes'], det


@test('R-F35', 'MUST_FAIL')
def t_ro1_missing():
    runs = triple(FX, k4p={'ro1': None})
    out = read(FX, manifest(FX, runs))
    ok, det = _code(out, 'INVALID')
    return ok and any('ro1' in c for c in out['validity'][L.K4P]['codes']), det


@test('R-F36', 'MUST_FAIL')
def t_attestation_producer_not_allowlisted():
    """Note 9: an SV7 attestation whose producer is not on a root V006 entry line refuses the reading."""
    runs = triple(FX)
    other = wbytes(fresh('other_producer') / 'other_producer.txt', b'some other producer\n')
    return expect_refusal(lambda: read(FX, manifest(FX, runs, producer=other)), 'ATTESTATION_PRODUCER_NOT_ALLOWLISTED')


@test('R-F37', 'MUST_FAIL')
def t_side_path_protected():
    """Note 11: a protected path inside the result record (route-A result path) refuses before read_run opens it."""
    runs = triple(FX, k4={'side_paths': lambda res: res['route_a_outcome'].__setitem__(
        'result_path', '/Users/bgm/Research/UVT_SOMETHING/route_a_attempt_result.json')})
    w = fresh('side_out')
    ok, det = expect_refusal(lambda: read(FX, manifest(FX, runs), write=str(w)), 'PROTECTED_PATH_REFUSED')
    return ok and os.listdir(w) == [], det


@test('R-F38', 'MUST_FAIL')
def t_side_path_field_ngc():
    runs = triple(FX, k3={'side_paths': lambda res: res['passes'][0].__setitem__('rotation', '/Users/bgm/Research/x/NGC3198_ROT/r')})
    return expect_refusal(lambda: read(FX, manifest(FX, runs)), 'PROTECTED_PATH_REFUSED')


@test('R-F39', 'MUST_FAIL')
def t_symlink_mid_path():
    """Note 12: a symlinked directory in the middle of a run path whose target is protected is refused (the target is
    checked lexically; nothing at the target is opened or created)."""
    runs = triple(FX)
    d = fresh('symlink')
    os.symlink('/Users/bgm/Research/NGC3198_NOT_A_REAL_DIR_FOR_TESTS', str(d / 'link'))
    runs[L.K4P] = dict(runs[L.K4P], result_dir=str(d / 'link' / 'run'))
    a = expect_refusal(lambda: read(FX, manifest(FX, runs)), 'PROTECTED_PATH_REFUSED')
    b = expect_refusal(lambda: L.guard_path(str(d / 'link' / 'x.json')), 'PROTECTED_PATH_REFUSED')
    return a[0] and b[0], [a[1], b[1]]


@test('R-F40', 'MUST_FAIL')
def t_flag_ruling_not_entered():
    """Note 13: a flag ruling whose sha is not on a V006 entry line refuses the reading."""
    runs = triple(FX, k4={'flagged': True})
    fr = wjson(fresh('fr_noentry') / 'S1_FLAG_RULING.json', {'schema': L.SCHEMA_FLAG_RULING, 'run': L.S1_C4T,
                                                             'result_sha256': runs[L.S1_C4T]['result_sha256'],
                                                             'flags': ['TAIL_SOURCE_UNDERCONVERGED'], 'ruling': L.FLAG_CLEARED,
                                                             'registration_sha256': L.REGISTRATION_SHA})
    return expect_refusal(lambda: read(FX, manifest(FX, runs, extra={'flag_rulings': {L.S1_C4T: fr}})), 'FLAG_RULING_NOT_ENTERED_IN_V6')


@test('R-F41', 'MUST_FAIL')
def t_flag_upheld():
    """Note 13: an entered ruling that upholds the flag leaves the reading INVALID FLAG_PENDING_RULING."""
    runs = triple(FX, k4={'flagged': True})
    fr = wjson(fresh('fr_upheld') / 'S1_FLAG_RULING.json', {'schema': L.SCHEMA_FLAG_RULING, 'run': L.S1_C4T,
                                                            'result_sha256': runs[L.S1_C4T]['result_sha256'],
                                                            'flags': ['TAIL_SOURCE_UNDERCONVERGED'], 'ruling': 'FLAG_UPHELD',
                                                            'registration_sha256': L.REGISTRATION_SHA})
    v6 = syn_v6(extra_lines=('**S1 flag ruling:** upheld, sha256 `%s`' % fr['sha256'],), tag='v6_flag_up')
    with use_v6(v6):
        out = read(FX, manifest(FX, runs, v6=v6, extra={'flag_rulings': {L.S1_C4T: fr}}))
    return _code(out, 'INVALID', 'FLAG_PENDING_RULING')


@test('R-F42', 'MUST_FAIL')
def t_flag_ruling_wrong_run():
    runs = triple(FX, k4={'flagged': True})
    fr = wjson(fresh('fr_wrong') / 'S1_FLAG_RULING.json', {'schema': L.SCHEMA_FLAG_RULING, 'run': L.S1_C4T,
                                                           'result_sha256': runs[L.S1_C3T]['result_sha256'],
                                                           'flags': ['TAIL_SOURCE_UNDERCONVERGED'], 'ruling': L.FLAG_CLEARED,
                                                           'registration_sha256': L.REGISTRATION_SHA})
    v6 = syn_v6(extra_lines=('**S1 flag ruling:** sha256 `%s`' % fr['sha256'],), tag='v6_flag_wrong')
    with use_v6(v6):
        return expect_refusal(lambda: read(FX, manifest(FX, runs, v6=v6, extra={'flag_rulings': {L.S1_C4T: fr}})),
                              'FLAG_RULING_BINDING')


# ================================================================================================ replay API (guard012) tests
@test('A-P1', 'MUST_PASS')
def t_guard_replay():
    rep = L.guard_replay(FX.fill['off']['pin'])
    ok = (rep['api'] == L.S1_REPLAY_API and all(L.sha256_bytes(rep['cases'][c]['bytes']) == FX.fill['off']['rec']['cases'][c]['spec']['sha256']
                                                for c in L.S1_CASES))
    return ok, {c: rep['cases'][c]['spec']['sha256'][:16] for c in L.S1_CASES}


@test('A-F1', 'MUST_FAIL')
def t_guard_replay_tampered_spec():
    d = mkdir(RUN / 'replay_tamper')
    rec = copy.deepcopy(FX.fill['off']['rec'])
    s = L.strict_json(L.verify_pin(rec['cases'][L.S1_C3T]['spec']))
    s['numerics']['uv_tail']['eps_certificate'] = FX.certs['c4t_eps']
    rec['cases'][L.S1_C3T]['spec'] = L.write_exclusive(str(d / 'c3t_other_cert.spec.json'), L.spec_bytes(s))
    rec.pop('record', None)
    fpin = wjson(d / 'FILL_RECORD_TAMPERED.json', rec)
    return expect_refusal(lambda: L.guard_replay(fpin), 'S1_TEMPLATE_REPLAY_MISMATCH')


# ================================================================================================ path guard tests
@test('G-P1', 'MUST_PASS')
def t_guard_ruling_file():
    p = L.guard_path(REAL_V6_PATH)
    return str(p) == REAL_V6_PATH, str(p)[-60:]


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


@test('G-F4', 'MUST_FAIL')
def t_guard_dotdot():
    return expect_refusal(lambda: L.guard_path('/Users/bgm/Research/UNT_EXCHANGE/../x.json'), 'PROTECTED_PATH_REFUSED')


# ================================================================================================ CLI wrapper tests
def _cli(script, args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('UNT_STEP4_')}
    r = subprocess.run([PY, '-I', '-B', str(HERE / script)] + args, capture_output=True, text=True, timeout=600, env=env)
    return r.returncode, r.stdout, r.stderr


def _p(ref):
    return '%s@%s' % (ref['path'], ref['sha256'])


@test('W-P1', 'MUST_PASS')
def t_cli_read():
    """c2v001 W-P1 ported: the CLI loads the library unpatched, so it reads against the real registration and the real
    V006 (constant path); a NO_U_A manifest reads NOT_RUN through the full CLI path (exit 0)."""
    real = L.pin_of(REAL_V6_PATH)
    m = wjson(fresh('cli_manifest') / 'manifest_no_u_a.json',
              {'schema': L.SCHEMA_MANIFEST, 'registration': FX.reg, 'v6': real, 'u_A_status': 'NO_U_A:SYNTHETIC_CLI_TEST',
               'runs': {}})
    rc, so, se = _cli('s1_read_c2v002a.py', ['--manifest', _p(m)])
    o = json.loads(so) if so.strip().startswith('{') else {}
    return rc == 0 and o.get('code') == 'NOT_RUN', {'rc': rc, 'code': o.get('code'), 'stderr': se[-300:]}


@test('W-P2', 'MUST_PASS')
def t_cli_dry_plan():
    rc, so, se = _cli('s1_fill_c2v002a.py', ['dry-plan', '--u-a', _p(FX.ua['off']), '--base-spec', _p(FX.base['off']),
                                            '--campaign-config', _p(CFG_PIN), '--c3t-registry', _p(FX.registry['off'])])
    o = json.loads(so) if so.strip().startswith('{') else {}
    return rc == 0 and o.get('dry') is True and o.get('blockers') == [], {'rc': rc, 'stderr': se[-300:]}


@test('W-F1', 'MUST_FAIL')
def t_cli_launch_pending():
    adm = make_admitted_plan(FX, 'cli', L.S1_C4T)
    real = L.pin_of(REAL_V6_PATH)
    rc, so, se = _cli('s1_launch_root_c2v002a.py', ['--plan', _p(adm['plan']), '--registration', _p(FX.reg), '--v6', _p(real),
                                                   '--launch-config', _p(FX.lcfg['INACTIVE'])])
    o = json.loads(so)
    return rc == 3 and o['refusal']['code'] == 'PUBLISHED_STEP4_ADMISSION_PENDING' and o['trace'][-1] == 'control_C2_admission_load', \
        {'rc': rc, 'refusal': o.get('refusal')}


@test('W-F2', 'MUST_FAIL')
def t_cli_lib_changed():
    d = mkdir(RUN / 'cli_tamper')
    for f in ('s1_read_c2v002a.py',):
        wbytes(d / f, (HERE / f).read_bytes())
    wbytes(d / 's1_path_lib_c2v002a.py', LIB_PATH.read_bytes() + b'\n# tampered\n')
    r = subprocess.run([PY, '-I', '-B', str(d / 's1_read_c2v002a.py'), '--manifest', '/x@y'], capture_output=True, text=True, timeout=120)
    return r.returncode == 3 and 'LIB_BYTES_CHANGED' in r.stdout, {'rc': r.returncode, 'stdout': r.stdout[-200:]}


@test('W-F3', 'MUST_FAIL')
def t_cli_internal_error():
    """Note 6: an unexpected error in the CLI prints INTERNAL_ERROR with the stage and exits 3 (no bare traceback)."""
    d = fresh('cli_int')
    rec = {k: v for k, v in FX.fill['off']['rec'].items() if k not in ('cases', 'record')}
    fpin = wjson(d / 'FILL_RECORD_NO_CASES.json', rec)
    rc, so, se = _cli('s1_fill_c2v002a.py', ['plan', '--fill-record', _p(fpin), '--case', 'S1_UA_C4T', '--dry'])
    o = json.loads(so) if so.strip().startswith('{') else {}
    return rc == 3 and o.get('refused') == 'INTERNAL_ERROR' and o.get('stage') == 'plan', {'rc': rc, 'out': so[-300:]}


@test('W-F4', 'MUST_FAIL')
def t_cli_read_producer_not_allowlisted():
    """Note 9 through the real CLI: the real V006 has no SV7 producer entry, so a reading with attestations refuses."""
    real = L.pin_of(REAL_V6_PATH)
    runs = triple(FX)
    m = manifest(FX, runs, v6=real)
    rc, so, se = _cli('s1_read_c2v002a.py', ['--manifest', _p(m)])
    o = json.loads(so) if so.strip().startswith('{') else {}
    return rc == 3 and o.get('refused') == 'ATTESTATION_PRODUCER_NOT_ALLOWLISTED', {'rc': rc, 'out': so[-300:]}


# ================================================================================================ BLK-1 tests (c2v002a)
def forged_fill(tag, mutate, fill_tag='seed'):
    """fill_tag's written fill record (its bytes, parsed) with one edit, written by exclusive create in a fresh folder."""
    doc = json.loads(L.read_bytes(FX.fill[fill_tag]['pin']['path']))
    mutate(doc)
    return wjson(fresh('forged_' + tag) / ('S1_FILL_RECORD_%s.json' % tag), doc)


def manifest_with_fill(fx, runs, fill_pin, fill_tag='seed', **kw):
    """manifest(...) for fill_tag, then the same manifest with only fill_record replaced by fill_pin."""
    doc = L.pinned_json(manifest(fx, runs, fill_tag=fill_tag, **kw))
    doc['fill_record'] = fill_pin
    fx.n_run += 1
    return wjson(fx.r / ('manifest_forged_fill_%03d.json' % fx.n_run), doc)


def set_branch_off(d):
    d['branch']['branch'] = 'OFF_ANCHOR'


def logonly_ua(tag):
    """A u_A point file for the seed theta pinned to the OFF snapshot: the seed is in that record's engine log (index 0)
    but is not its primary anchor, so B2 does not bind it."""
    return _ua_variant(tag, FX.seed, snapshot=FX.snap['off'])


def phys_ulp_forge(d):
    v = math.nextafter(d['physical_u_A']['common_scale_s']['value'], math.inf)
    d['physical_u_A']['common_scale_s'] = {'value': v, 'hex': L.fhex(v)}


def ulp_triple():
    """The off triple computed one ulp above u_A in common_scale_s (all three runs; spec shas genuine)."""
    tw = {'phys_tweak': 'common_scale_s'}
    return triple(FX, k3=dict(tw), k4=dict(tw), k4p=dict(tw))


def load_pred():
    """The predecessor library c2v002 (e3ca4d80) from its verified bytes, with the same V6_PATH test seam."""
    raw = L.verify_pin(PRED_LIB, 'PRED_LIB')
    m = types.ModuleType('s1_path_lib_c2v002_predecessor')
    m.__file__ = PRED_LIB['path']
    exec(compile(raw, PRED_LIB['path'], 'exec'), m.__dict__)
    m.V6_PATH = FX.v6['path']
    return m


@test('R-F43', 'MUST_FAIL')
def t_blk1_branch_edited_read():
    """BLK-1 (a), the verifier's probe_adv2: a genuine AT_ANCHOR (seed) triple reads PASS_AT_ADOPTION_POINT; the same runs
    with a fill record whose only edit is branch.branch = OFF_ANCHOR are refused at read time, since the branch is
    re-derived from the u_A theta bits; nothing is written. (c2v002 reads them PASS: B-P1.)"""
    runs = triple(FX, fill_tag='seed')
    g = read(FX, manifest(FX, runs, fill_tag='seed'))
    forged = forged_fill('branch_off_read', set_branch_off)
    w = fresh('blk1_branch_out')
    ok, det = expect_refusal(lambda: read(FX, manifest_with_fill(FX, runs, forged), write=str(w)), 'FILL_RECORD_BRANCH_NOT_REPLAYED')
    return ok and g['code'] == 'PASS_AT_ADOPTION_POINT' and os.listdir(w) == [], {'genuine': g['code'], 'forged': det}


@test('R-F44', 'MUST_FAIL')
def t_blk1_logonly_ua_read():
    """BLK-1 (b): a fill record whose u_A_point names a log-only point (the seed theta in the OFF snapshot) is refused at
    read time with B2's code, exactly as guard_replay refuses it; nothing is written. (c2v002 read it
    PASS_AT_ADOPTION_POINT: B-P1.)"""
    runs = triple(FX, fill_tag='seed')
    ua = logonly_ua('blk1_logonly_read')
    forged = forged_fill('ua_logonly_read', lambda d: d.__setitem__('u_A_point', ua))
    w = fresh('blk1_ua_out')
    a = expect_refusal(lambda: read(FX, manifest_with_fill(FX, runs, forged), write=str(w)), 'PHASE1_PRIMARY_ANCHOR_NOT_U_A')
    b = expect_refusal(lambda: L.guard_replay(forged), 'PHASE1_PRIMARY_ANCHOR_NOT_U_A')
    return a[0] and b[0] and os.listdir(w) == [], [a[1], b[1]]


@test('R-F45', 'MUST_FAIL')
def t_blk1_physical_edited_read():
    """BLK-1: physical_u_A is re-derived. Three runs one ulp above u_A (common_scale_s) read INVALID (SV3) against the
    genuine record; a record whose physical_u_A was edited to those bits is refused at read time. (c2v002 reads the
    edited one PASS: B-P1.)"""
    runs = ulp_triple()
    g = read(FX, manifest(FX, runs, fill_tag='off'))
    forged = forged_fill('phys_ulp_read', phys_ulp_forge, fill_tag='off')
    ok, det = expect_refusal(lambda: read(FX, manifest_with_fill(FX, runs, forged, fill_tag='off')),
                             'FILL_RECORD_PHYSICAL_U_A_NOT_REPLAYED')
    sv3 = all('SV3_PHYSICAL_NOT_U_A_BITS:common_scale_s' in g['validity'][c]['codes'] for c in L.RUNS)
    return ok and g['code'] == 'INVALID' and sv3, {'genuine': g['code'], 'forged': det}


@test('R-F46', 'MUST_FAIL')
def t_blk1_theta_key_edited_read():
    """BLK-1: theta_key is recomputed from the u_A theta bits at read time (it names the reading file)."""
    runs = triple(FX)
    forged = forged_fill('theta_key_read', lambda d: d.__setitem__('theta_key', 'f' * 64), fill_tag='off')
    return expect_refusal(lambda: read(FX, manifest_with_fill(FX, runs, forged, fill_tag='off')), 'FILL_RECORD_THETA_KEY')


@test('R-F47', 'MUST_FAIL')
def t_blk1_every_consumed_field():
    """BLK-1: each other consumed fill-record field, edited alone, is refused at read time with its named code
    (bitwise: one ulp in a branch float is enough)."""
    def ulp_branch(d):
        d['branch']['max_abs_over_half_width'] = math.nextafter(d['branch']['max_abs_over_half_width'], math.inf)

    def case_set(case, f, v):
        return lambda d: d['cases'][case].__setitem__(f, v)

    def extra_case(d):
        d['cases']['S1_UA_C5T'] = copy.deepcopy(d['cases'][L.S1_C4T])
    subs = [
        ('branch_ulp', ulp_branch, 'FILL_RECORD_BRANCH_NOT_REPLAYED'),
        ('branch_seed_bits', lambda d: d['branch'].__setitem__('seed_bits_equal', True), 'FILL_RECORD_BRANCH_NOT_REPLAYED'),
        ('branch_missing', lambda d: d.pop('branch'), 'FILL_RECORD_BRANCH_NOT_REPLAYED'),
        ('theta_hex', lambda d: d['theta']['ell_F_m'].__setitem__('hex', '0x1.0p+0'), 'FILL_RECORD_THETA_NOT_REPLAYED'),
        ('base_point_key', lambda d: d.__setitem__('base_point_key', '0' * 64), 'FILL_RECORD_BASE_POINT_KEY_NOT_REPLAYED'),
        ('static_pins', lambda d: d['static_pins']['P5'].__setitem__('sha256', '0' * 64), 'FILL_RECORD_STATIC_PINS_NOT_REPLAYED'),
        ('c4t_label', case_set(L.S1_C4T, 'label', 'edited label'), 'FILL_RECORD_CASE_FIELD_NOT_REPLAYED'),
        ('c3t_point_key', case_set(L.S1_C3T, 'point_key', '0' * 64), 'FILL_RECORD_CASE_FIELD_NOT_REPLAYED'),
        ('c3t_k', case_set(L.S1_C3T, 'k', 4), 'FILL_RECORD_CASE_FIELD_NOT_REPLAYED'),
        ('c4t_cb_case', case_set(L.S1_C4T, 'cb_case', 'C3T'), 'FILL_RECORD_CASE_FIELD_NOT_REPLAYED'),
        ('c3t_changed_paths', case_set(L.S1_C3T, 'changed_paths', ['label']), 'FILL_RECORD_CASE_FIELD_NOT_REPLAYED'),
        ('c4t_sha256', case_set(L.S1_C4T, 'sha256', '0' * 64), 'FILL_RECORD_CASE_FIELD_NOT_REPLAYED'),
        ('extra_case', extra_case, 'FILL_RECORD_CASES_NOT_REPLAYED'),
    ]
    runs = triple(FX)
    res = {}
    for tag, mut, code in subs:
        forged = forged_fill('field_' + tag, mut, fill_tag='off')
        res[tag] = expect_refusal(lambda: read(FX, manifest_with_fill(FX, runs, forged, fill_tag='off')), code)
    return all(v[0] for v in res.values()), {k: v[1][:90] for k, v in res.items()}


@test('R-F48', 'MUST_FAIL')
def t_blk1_spec_pin_swapped_read():
    """BLK-1: the reader takes the S1 spec pins from the fill record (SV0 / SV3); a record whose C3T spec pin names an
    edited spec (another eps certificate) is refused at read time (the spec bytes are replayed)."""
    s = L.strict_json(L.verify_pin(FX.fill['off']['rec']['cases'][L.S1_C3T]['spec']))
    s['numerics']['uv_tail']['eps_certificate'] = FX.certs['c4t_eps']
    alt = L.write_exclusive(str(fresh('blk1_spec_alt') / 'c3t_other_cert.spec.json'), L.spec_bytes(s))
    forged = forged_fill('spec_swap_read', lambda d: d['cases'][L.S1_C3T].__setitem__('spec', alt), fill_tag='off')
    runs = triple(FX)
    return expect_refusal(lambda: read(FX, manifest_with_fill(FX, runs, forged, fill_tag='off')), 'S1_TEMPLATE_REPLAY_MISMATCH')


@test('A-F2', 'MUST_FAIL')
def t_blk1_guard_replay_branch():
    """BLK-1 (3): guard_replay (guard012's S1_REPLAY_API) refuses the edited-branch record (c2v002 accepted it)."""
    forged = forged_fill('branch_replay', set_branch_off)
    return expect_refusal(lambda: L.guard_replay(forged), 'FILL_RECORD_BRANCH_NOT_REPLAYED')


@test('A-F3', 'MUST_FAIL')
def t_blk1_guard012_validate():
    """BLK-1 (3) through guard012's own code: validate (the launcher's pre-start check; no native preflight here) of an
    overlap admission whose replay module is this library and whose fill record has an edited branch refuses
    S1_OVERLAP_REPLAY_REFUSED with this library's code as detail."""
    forged = forged_fill('branch_g12', set_branch_off)
    adm = make_admitted_plan(FX, 'blk1_g12', L.S1_C4T, overlap=True, fill_tag='seed', fill_override=forged)
    try:
        FX.G.validate(adm['plan'], L.PINS['LAUNCHER'][0], check_outputs=True, execute_native=False,
                      config_ref=adm['admission'], disk_batch=False)
        return False, 'guard012 validate accepted the edited-branch record'
    except FX.G.Refusal as exc:
        a = list(exc.args)
        return a[:2] == ['S1_OVERLAP_REPLAY_REFUSED', 'FILL_RECORD_BRANCH_NOT_REPLAYED'], a


@test('L-F36', 'MUST_FAIL')
def t_blk1_launch_branch():
    """BLK-1 (3) on the launch path: an INACTIVE C4T plan and an overlap C3T plan whose fill record has an edited branch
    are refused at S1_CHECKS (before guard012, the gate and any process; nothing probed or spawned)."""
    forged = forged_fill('branch_launch', set_branch_off)
    adm = make_admitted_plan(FX, 'blk1_l', L.S1_C4T, fill_tag='seed', fill_override=forged)
    out, probes, box = do_launch(FX, adm)
    a = _refused(out, 'FILL_RECORD_BRANCH_NOT_REPLAYED', None, probes, 0, box)
    adm2 = make_admitted_plan(FX, 'blk1_lo', L.S1_C3T, overlap=True, fill_tag='seed', fill_override=forged)
    out2, probes2, box2 = do_launch(FX, adm2, lcfg=FX.lcfg['ACTIVE'])
    b = _refused(out2, 'FILL_RECORD_BRANCH_NOT_REPLAYED', None, probes2, 0, box2)
    ok = a[0] and b[0] and out['refusal']['stage'] == 'S1_CHECKS' and out2['refusal']['stage'] == 'S1_CHECKS'
    return ok, [a[1]['refusal'], b[1]['refusal']]


@test('W-F5', 'MUST_FAIL')
def t_blk1_cli_read_branch():
    """BLK-1 through the real read CLI (library loaded by sha, unpatched; real V006): the edited-branch manifest exits 3
    with the replay code (before any attestation is read)."""
    real = L.pin_of(REAL_V6_PATH)
    runs = triple(FX, fill_tag='seed')
    forged = forged_fill('branch_cli', set_branch_off)
    m = manifest_with_fill(FX, runs, forged, v6=real)
    rc, so, se = _cli('s1_read_c2v002a.py', ['--manifest', _p(m)])
    o = json.loads(so) if so.strip().startswith('{') else {}
    return rc == 3 and o.get('refused') == 'FILL_RECORD_BRANCH_NOT_REPLAYED', {'rc': rc, 'out': so[-300:], 'stderr': se[-200:]}


@test('B-P1', 'MUST_PASS')
def t_blk1_reproduced_on_predecessor():
    """BLK-1 reproduced on the predecessor's bytes (c2v002 e3ca4d80 by path and sha; same test seam), so the R-F43, R-F44
    and R-F45 inputs reach the defect: c2v002 reads the edited-branch manifest PASS (genuine PASS_AT_ADOPTION_POINT),
    the log-only-u_A manifest PASS_AT_ADOPTION_POINT while its own guard_replay refuses that record, and the
    physical_u_A-edited manifest over the one-ulp-off runs PASS (genuine INVALID). c2v002a refuses all three."""
    P = load_pred()
    runs = triple(FX, fill_tag='seed')
    out = {'genuine_seed': P.read_reading(manifest(FX, runs, fill_tag='seed'))['code']}
    out['branch_edited'] = P.read_reading(manifest_with_fill(FX, runs, forged_fill('pred_branch', set_branch_off)))['code']
    ua = logonly_ua('pred_logonly')
    f2 = forged_fill('pred_ua', lambda d: d.__setitem__('u_A_point', ua))
    out['ua_logonly'] = P.read_reading(manifest_with_fill(FX, runs, f2))['code']
    try:
        P.guard_replay(f2)
        out['ua_logonly_guard_replay'] = 'ACCEPTED'
    except P.Refusal as exc:
        out['ua_logonly_guard_replay'] = exc.code
    r3 = ulp_triple()
    out['ulp_genuine'] = P.read_reading(manifest(FX, r3, fill_tag='off'))['code']
    f3 = forged_fill('pred_phys', phys_ulp_forge, fill_tag='off')
    out['ulp_physical_edited'] = P.read_reading(manifest_with_fill(FX, r3, f3, fill_tag='off'))['code']
    want = {'genuine_seed': 'PASS_AT_ADOPTION_POINT', 'branch_edited': 'PASS', 'ua_logonly': 'PASS_AT_ADOPTION_POINT',
            'ua_logonly_guard_replay': 'PHASE1_PRIMARY_ANCHOR_NOT_U_A', 'ulp_genuine': 'INVALID', 'ulp_physical_edited': 'PASS'}
    return out == want, out


@test('A-P2', 'MUST_PASS')
def t_pred_fill_record_replays():
    """Format unchanged: a fill record written by the predecessor c2v002 replays under c2v002a (guard_replay), and differs
    from c2v002a's own record for the same inputs only at module, module_sha256 and the spec-file paths."""
    P = load_pred()
    d = fresh('pred_fill')
    prec = P.fill(FX.ua['off'], FX.base['off'], CFG_PIN, c3t_registry=FX.registry['off'], out_dir=str(d))
    rep = L.guard_replay(prec['record'])

    def strip(r):
        r = copy.deepcopy(r)
        for k in ('module', 'module_sha256', 'record'):
            r.pop(k, None)
        for c in L.S1_CASES:
            r['cases'][c]['spec'] = r['cases'][c]['spec']['sha256']
        return r
    same = L.canonical(strip(prec)) == L.canonical(strip(FX.fill['off']['rec']))
    ok = (same and prec['module'] == 's1_path_lib_c2v002' and FX.fill['off']['rec']['module'] == 's1_path_lib_c2v002a'
          and all(L.sha256_bytes(rep['cases'][c]['bytes']) == FX.fill['off']['rec']['cases'][c]['sha256'] for c in L.S1_CASES))
    return ok, {'same_except_module_and_paths': same, 'pred_module_sha256': (prec.get('module_sha256') or '')[:16]}


@test('F-P8', 'MUST_PASS')
def t_cp1_spec_same_as_predecessor():
    """The procedure's step 2 output (c3t-cp1-spec) is byte-identical under c2v002 and c2v002a (dry; spec sha, point key)."""
    P = load_pred()
    a = P.write_c3t_cp1_spec(FX.ua['off'], FX.base['off'], CFG_PIN, dry=True)
    b = L.write_c3t_cp1_spec(FX.ua['off'], FX.base['off'], CFG_PIN, dry=True)
    keys = ('sha256', 'point_key', 'theta_key', 'successor_validate_spec_block', 'k')
    return all(a[k] == b[k] for k in keys), {k: (str(b[k])[:16], a[k] == b[k]) for k in keys}


# ================================================================================================ main
def main():
    global L, RUN, FX, REAL_V6_PATH
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    a = ap.parse_args()
    L, lib_sha = load_lib()
    REAL_V6_PATH = L.V6_PATH
    RUN = Path(os.path.abspath(a.run_dir))
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
    summary = {'schema': 'UNT_S1_PATH_TEST_RESULTS_C2V002A', 'started_utc': started,
               'finished_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'seconds': round(time.time() - t0, 1),
               'python': sys.version.split()[0], 'interpreter': sys.executable, 'lib_sha256': lib_sha, 'files_sha256': files,
               'real_v6_sha256_at_test': L.sha256_bytes(L.read_bytes(REAL_V6_PATH)),
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
