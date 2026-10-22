"""PORT (ks_k3_chain_c2 G-wave c2v001): the s1k3 wrapper suite (wave-1 port) against KS5'' (wrapper c2v003).

Synthetic MUST_PASS / MUST_FAIL tests for the S1-only kept-K-3 wrapper successor
calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v001.py (s1_successors_c2; A150 R-S1-3 (2)).

  python3 -I -B test_wrapper_s1k3_c2v001.py --run-dir <a new directory>

Target-free; launches nothing. The successor is executed from its bytes (it loads q5b1 7a6af535, core dc895f8a, the
v005 orchestrator, sensitivity policy 8fb06600 and certificate guard b1 unchanged); a fresh, independent load of q5b1 is
the predecessor reference. Contexts are the direct-adapter form (cfg, numerics, D, norm_base) with a stub driver whose
normalize_spec adds r5's truncation default only; the real r5 normalization of a K=3 spec is FORMAL (CB C3T /numerics
is r5's dry-run normalized output) and is exercised by root's dry native preflight. guard012's fence is the real one.
Results: <run-dir>/TEST_RESULTS.json and <run-dir>/TEST_LOG.txt (exclusive create).
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
import sys
import time
import traceback
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
SUCC_PATH = str(HERE / 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003.py')   # PORT (G-wave): KS5''
G12_PATH = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_guard_c2v012.py'
Q5B1 = (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py',
        '7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d')
CORE = (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py',
        'dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6')
ORC = (ART + '/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py',
       'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d')
SENS = (ART + '/calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py',
        '8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f')
GB1 = (ART + '/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py',
       '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677')
CB = (ART + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json',
      '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71')
CFG = (ART + '/sched_s45_c2/v003/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V003.json',
       'd9241676c3b7b32bd3067a55bdfb7821ebc33a68adbdc011ab4e4c58b6e50a4d')
P5 = (ART + '/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json',
      'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174')
C3T_LABEL = 'S1 transfer test C3T at u_A theta 0123456789abcdef; base 89abcdef'
C4T_LABEL = 'S1 transfer test C4T at u_A theta 0123456789abcdef; base 89abcdef'
CAMPAIGN_LABEL = 'DDO154 cx2v006 theta 0123456789abcdef; point fedcba9876543210'

RUN = None
RESULTS, LOG, TESTS = [], [], []
S = P = G12 = None
FX = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rb(p):
    with open(p, 'rb') as f:
        return f.read()


def wx(path, data):
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)
    return {'path': str(path), 'sha256': sha(data)}


def wj(path, obj):
    return wx(path, (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode())


def test(tid, kind):
    def deco(fn):
        fn._tid, fn._kind = tid, kind
        TESTS.append(fn)
        return fn
    return deco


def record(tid, kind, ok, detail):
    RESULTS.append({'id': tid, 'kind': kind, 'result': 'PASS' if ok else 'FAIL', 'detail': detail})
    LOG.append('%-5s %-9s %s  %s' % ('ok' if ok else 'FAIL', kind, tid, str(detail)[:300]))


def load_module(path, expect, name, source=None):
    raw = rb(path) if source is None else source
    if expect is not None:
        assert sha(raw) == expect, path
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    exec(compile(raw, path, 'exec'), m.__dict__)
    return m


def outcome(fn):
    try:
        r = fn()
        return 'PASS', r
    except Exception as exc:
        return '%s: %s' % (type(exc).__name__, exc), None


# ================================================================================================ fixtures
def cb_grid(case):
    return copy.deepcopy(json.loads(rb(CB[0]))['cases'][case]['normalized_spec_equal']['/numerics']['composite_grid_spec'])


def grid_k(k):
    """A synthetic composite grid with last break k (CB C4T's seed panels plus outer unit panels), for K=2 and K=5."""
    g = cb_grid('C4T')
    inner = [b for b in g['breaks_inverse_kpc'] if abs(b) <= 2]
    outer = [float(x) for x in range(3, k + 1)]
    br = sorted(set([-x for x in outer] + inner + outer))
    if k == 2:
        br = inner
    g['breaks_inverse_kpc'] = [int(x) if float(x).is_integer() else x for x in br]
    g['panel_orders'] = [6] * (len(g['breaks_inverse_kpc']) - 1)
    g['total_axis_nodes'] = 6 * len(g['panel_orders'])
    g['version'] = 'SYNTHETIC_K%d' % k
    return g


def make_spec(label, grid=None, mutate=None):
    p5 = json.loads(rb(P5[0]))
    num = copy.deepcopy(json.loads(rb(CFG[0]))['numerics']['block'])
    num['uv_tail']['eps_certificate'] = FX['eps']
    num['uv_tail']['lo_certificate'] = FX['lo']
    if grid is not None:
        num['composite_grid_spec'] = grid
    ph = copy.deepcopy(p5['anchor']['physical'])
    ph['inclination_deg'] = 66.0
    s = {'schema': 'UNT_GALAXY_M0_FORWARD_CALL_C2V001', 'galaxy': 'DDO154', 'admit': {},
         'coefficients': p5['anchor']['coefficients'], 'physical': ph, 'numerics': num,
         'reference_compare': False, 'label': label}
    if mutate:
        mutate(s)
    return s


class StubDriver:
    """r5's normalize_spec adds the truncation default kmax_inverse_kpc: None (core L169-174); nothing else here."""
    def __init__(self, extra_grid_leaf=False):
        self.extra = extra_grid_leaf

    def normalize_spec(self, spec):
        n = copy.deepcopy(spec)
        n['numerics']['truncation'] = {'shape': 'cube', 'kmax_inverse_kpc': None}
        if self.extra:
            n['numerics']['composite_grid_spec']['normalized_extra'] = 1
        return n


def make_ctx(mod, cfg=None, driver=None):
    base = make_spec(CAMPAIGN_LABEL)
    D = driver or StubDriver()
    numerics = copy.deepcopy(base['numerics'])

    class Ctx(mod.Context):
        def __init__(self):
            self.cfg = copy.deepcopy(cfg if cfg is not None else {'tail_readiness': {'certificate_registry': None}})
            self.numerics = numerics
            self.D = D
            self.norm_base = D.normalize_spec(copy.deepcopy(base))
    return Ctx()


# ================================================================================================ tests
@test('WS-P1', 'MUST_PASS')
def t_validate_c3t():
    s = make_spec(C3T_LABEL, cb_grid('C3T'))
    a = outcome(lambda: S.validate_spec_block(s))[0]
    b = outcome(lambda: P.validate_block(s['numerics']))[0]
    return a == 'PASS' and b == 'OrchestratorError: kept K must be 4', {'successor': a, 'predecessor': b}


@test('WS-P2', 'MUST_PASS')
def t_prelaunch_c3t():
    s = make_spec(C3T_LABEL, cb_grid('C3T'))
    a, n = outcome(lambda: make_ctx(S).prelaunch_check(s))
    b = outcome(lambda: make_ctx(P).prelaunch_check(s))[0]
    ok = (a == 'PASS' and json.dumps(n['numerics']['composite_grid_spec'], sort_keys=True)
          == json.dumps(cb_grid('C3T'), sort_keys=True) and b == 'OrchestratorError: kept K must be 4')
    return ok, {'successor': a, 'predecessor': b}


@test('WS-P3', 'MUST_PASS')
def t_differential_non_s1():
    """Every non-S1_UA_C3T spec: the successor's outcome equals a fresh, unpatched q5b1's, for the block check and for
    prelaunch_check (pass, or the same exception type and message)."""
    def cw4(s):
        s['numerics']['route_a']['column_workers'] = 4

    def tail_off(s):
        s['numerics']['uv_tail']['enabled'] = False
    specs = {
        'campaign_k4': make_spec(CAMPAIGN_LABEL),
        's1_c4t_k4': make_spec(C4T_LABEL),
        'campaign_k3_cb': make_spec(CAMPAIGN_LABEL, cb_grid('C3T')),
        's1_c4t_label_k3_cb': make_spec(C4T_LABEL, cb_grid('C3T')),
        'campaign_k2': make_spec(CAMPAIGN_LABEL, grid_k(2)),
        'campaign_k5': make_spec(CAMPAIGN_LABEL, grid_k(5)),
        'campaign_k6_cb': make_spec(CAMPAIGN_LABEL, cb_grid('C6T')),
        'c3t_label_suffix_k3': make_spec(C3T_LABEL + '; recovery x', cb_grid('C3T')),
        'c3t_label_upper_hex_k3': make_spec(C3T_LABEL.replace('0123456789abcdef', '0123456789ABCDEF'), cb_grid('C3T')),
        'campaign_cw4': make_spec(CAMPAIGN_LABEL, mutate=cw4),
        'campaign_tail_off': make_spec(CAMPAIGN_LABEL, mutate=tail_off),
        's1_c4t_undeclared': make_spec(C4T_LABEL, mutate=lambda s: s['numerics']['picard'].__setitem__('passes', s['numerics']['picard']['passes'] + 1)),
    }
    out, ok = {}, True
    for name, s in specs.items():
        r1 = [outcome(lambda: S.validate_spec_block(copy.deepcopy(s)))[0],
              outcome(lambda: make_ctx(S).prelaunch_check(copy.deepcopy(s)))[0]]
        r0 = [outcome(lambda: P.validate_block(copy.deepcopy(s)['numerics']))[0],
              outcome(lambda: make_ctx(P).prelaunch_check(copy.deepcopy(s)))[0]]
        out[name] = {'successor': r1, 'predecessor': r0}
        ok = ok and r1 == r0
    ok = ok and out['campaign_k4']['successor'] == ['PASS', 'PASS'] and out['s1_c4t_k4']['successor'] == ['PASS', 'PASS']
    return ok, out


@test('WS-P4', 'MUST_PASS')
def t_sensitivity_c3t():
    s = make_spec(C3T_LABEL, cb_grid('C3T'))
    g = make_ctx(S).sensitivity_gate(s)
    return g.get('ok') is True and g.get('status') == 'HEADLINE_NOT_GATED', g


@test('WS-P5', 'MUST_PASS')
def t_exports():
    s = make_spec(C3T_LABEL, cb_grid('C3T'))
    outside = outcome(lambda: S.W.validate_block(s['numerics']))[0]
    ok = (S.validate_block is S.M.validate_block and S.PREDECESSOR_VALIDATE_BLOCK is S.M.validate_block
          and S.W.validate_block is not S.M.validate_block and outside == 'OrchestratorError: kept K must be 4'
          and S._S1_BLOCK.get() is None and S.Context.__mro__[1] is S.W.Context)
    return ok, {'outside_override': outside}


@test('WS-P6', 'MUST_PASS')
def t_fence_load():
    """The successor loads inside guard012's real fence with exactly its sources: q5b1's generated buffer is still
    compiled under q5b1's path, so guard011/012's compile contract covers it (no PREFLIGHT_COMPILE_HASH_MISMATCH)."""
    srcs = {p: h for p, h in (Q5B1, CORE, ORC, SENS, GB1)}
    srcs[SUCC_PATH] = sha(rb(SUCC_PATH))
    srcs['/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/certificate_guard_b1_ks5_c2v001.py'] = sha(rb('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/certificate_guard_b1_ks5_c2v001.py'))   # PORT: KS5'' loads KS5 (wave-1 folder)
    cfg = {'sources': srcs}
    try:
        with G12.fence(srcs):
            m = G12.load({'path': SUCC_PATH, 'sha256': srcs[SUCC_PATH]}, cfg, '_t_ws_fence_successor')
            r = outcome(lambda: m.validate_spec_block(make_spec(C3T_LABEL, cb_grid('C3T'))))[0]
        return r == 'PASS' and m.MODULE_NAME.endswith('s1k3_c2v003'), {'validate_in_fence': r}
    except Exception as exc:
        return False, '%s: %s' % (type(exc).__name__, exc)


class _StubOk(object):
    pass


def stub_ctx(result):
    """Unit seam for the S1-only post-check: a class whose next-in-MRO certificate_check returns `result`."""
    class StubBase(S.W.Context):
        def certificate_check(self, spec, phase, *, result=None, call_dir=None, _handoff=None):
            return copy.deepcopy(FX['stub_result'])

    class T(S.Context, StubBase):
        def __init__(self):
            self.cfg = {'tail_readiness': {'certificate_registry': FX['registry']}}
    FX['stub_result'] = result
    return T()


@test('WS-P7', 'MUST_PASS')
def t_cert_domain_k3_ok():
    s = make_spec(C3T_LABEL, cb_grid('C3T'))
    FX['registry'] = registry_for(s, 3.0)
    g = stub_ctx({'ok': True, 'blockers': []}).certificate_check(s, 'prelaunch')
    return g.get('ok') is True, g


def registry_for(spec, k):
    FX['n'] = FX.get('n', 0) + 1
    d = RUN / ('reg_%03d' % FX['n'])
    os.mkdir(d)
    bundle = wj(d / 'bundle.json', {'schema': 'UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001',
                                     'domain': {'K_inverse_kpc': k, 'K_big_inverse_kpc': 128.0}})
    ident = S.point_identity(spec)
    return wj(d / 'registry.json', {'points': {S.M.digest(ident): {'identity': ident, 'bundle': bundle,
                                                                     'eps_certificate': FX['eps'], 'lo_certificate': FX['lo']}}})


def _refuses(fn, needle):
    r = outcome(fn)[0]
    return (r != 'PASS' and needle in r), r


@test('WS-F1', 'MUST_FAIL')
def t_c3t_label_k2():
    return _refuses(lambda: S.validate_spec_block(make_spec(C3T_LABEL, grid_k(2))), 'must equal CB C3T bitwise')


@test('WS-F2', 'MUST_FAIL')
def t_c3t_label_k4():
    return _refuses(lambda: S.validate_spec_block(make_spec(C3T_LABEL)), 'must equal CB C3T bitwise')


@test('WS-F3', 'MUST_FAIL')
def t_c3t_label_k5_k6():
    a = _refuses(lambda: S.validate_spec_block(make_spec(C3T_LABEL, grid_k(5))), 'must equal CB C3T bitwise')
    b = _refuses(lambda: S.validate_spec_block(make_spec(C3T_LABEL, cb_grid('C6T'))), 'must equal CB C3T bitwise')
    return a[0] and b[0], [a[1], b[1]]


@test('WS-F4', 'MUST_FAIL')
def t_c3t_grid_leaf():
    g = cb_grid('C3T')
    g['total_axis_nodes'] = 85
    a = _refuses(lambda: S.validate_spec_block(make_spec(C3T_LABEL, g)), 'must equal CB C3T bitwise')
    g2 = cb_grid('C3T')
    g2['breaks_inverse_kpc'][-1] = 3.0000000000000004
    b = _refuses(lambda: S.validate_spec_block(make_spec(C3T_LABEL, g2)), 'must equal CB C3T bitwise')
    return a[0] and b[0], [a[1], b[1]]


@test('WS-F5', 'MUST_FAIL')
def t_c4t_label_k3():
    return _refuses(lambda: S.validate_spec_block(make_spec(C4T_LABEL, cb_grid('C3T'))), 'kept K must be 4')


@test('WS-F6', 'MUST_FAIL')
def t_campaign_label_k3():
    return _refuses(lambda: S.validate_spec_block(make_spec(CAMPAIGN_LABEL, cb_grid('C3T'))), 'kept K must be 4')


@test('WS-F7', 'MUST_FAIL')
def t_label_suffix():
    return _refuses(lambda: S.validate_spec_block(make_spec(C3T_LABEL + ' ', cb_grid('C3T'))), 'kept K must be 4')


@test('WS-F8', 'MUST_FAIL')
def t_c3t_workers():
    def cw4(s):
        s['numerics']['route_a']['column_workers'] = 4
    return _refuses(lambda: S.validate_spec_block(make_spec(C3T_LABEL, cb_grid('C3T'), cw4)), 'route A workers 8 required')


@test('WS-F9', 'MUST_FAIL')
def t_c3t_gas():
    def gas(s):
        s['numerics']['uv_tail']['gas'] = {'M_s': 64, 'interp': 'lagrange3_s_gl4'}
    return _refuses(lambda: S.validate_spec_block(make_spec(C3T_LABEL, cb_grid('C3T'), gas)), 'A57 production gas M_s 128')


@test('WS-F10', 'MUST_FAIL')
def t_c3t_undeclared():
    s = make_spec(C3T_LABEL, cb_grid('C3T'), lambda s: s['numerics']['picard'].__setitem__('passes', s['numerics']['picard']['passes'] + 1))
    return _refuses(lambda: make_ctx(S).prelaunch_check(s), 'undeclared paths')


@test('WS-F11', 'MUST_FAIL')
def t_c3t_recovery():
    return _refuses(lambda: make_ctx(S).prelaunch_check(make_spec(C3T_LABEL, cb_grid('C3T')), recovery=True), 'no bracket recovery')


@test('WS-F12', 'MUST_FAIL')
def t_c3t_normalized_grid_differs():
    s = make_spec(C3T_LABEL, cb_grid('C3T'))
    return _refuses(lambda: make_ctx(S, driver=StubDriver(extra_grid_leaf=True)).prelaunch_check(s),
                    "undeclared paths ['numerics.composite_grid_spec")


@test('WS-F13', 'MUST_FAIL')
def t_cert_domain_k4():
    s = make_spec(C3T_LABEL, cb_grid('C3T'))
    FX['registry'] = registry_for(s, 4.0)
    g = stub_ctx({'ok': True, 'blockers': []}).certificate_check(s, 'prelaunch')
    return g.get('ok') is False and 'S1_UA_C3T_CERTIFICATE_DOMAIN_K_IS_NOT_THE_KEPT_K' in str(g.get('blockers')), g


@test('WS-F14', 'MUST_FAIL')
def t_cert_real_parent_policy_pending():
    """Through q5b1's real certificate_check: the S1 block check passes, then the certificate policy is pending."""
    s = make_spec(C3T_LABEL, cb_grid('C3T'))
    ctx = make_ctx(S, cfg={'tail_readiness': {}})
    g = ctx.certificate_check(s, 'prelaunch')
    return g.get('ok') is False and 'CERTIFICATE_POLICY_PENDING' in str(g.get('blockers')), g


@test('WS-F15', 'MUST_FAIL')
def t_cert_wrong_grid_raises():
    s = make_spec(C3T_LABEL, grid_k(2))
    return _refuses(lambda: make_ctx(S, cfg={'tail_readiness': {}}).certificate_check(s, 'prelaunch'), 'must equal CB C3T bitwise')


@test('WS-F16', 'MUST_FAIL')
def t_predecessor_pin():
    d = RUN / 'tamper'
    os.mkdir(d)
    tq = wx(d / 'q5b1_tampered.py', rb(Q5B1[0]) + b'\n# tampered\n')
    src = rb(SUCC_PATH).replace(b"PREDECESSOR = (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py',",
                                ("PREDECESSOR = (%r," % tq['path']).encode(), 1)
    r = outcome(lambda: load_module(str(d / 'succ_tampered_pred.py'), None, '_t_ws_tamper', source=src))[0]
    return 'source byte pin mismatch' in r, r


@test('WS-F17', 'MUST_FAIL')
def t_fence_without_q5b1():
    srcs = {p: h for p, h in (CORE, ORC, SENS, GB1)}
    srcs[SUCC_PATH] = sha(rb(SUCC_PATH))
    try:
        with G12.fence(srcs):
            G12.load({'path': SUCC_PATH, 'sha256': srcs[SUCC_PATH]}, {'sources': srcs}, '_t_ws_fence_noq5b1')
        return False, 'loaded'
    except Exception as exc:
        return str(exc.args[0]) == 'UNPINNED_PREFLIGHT_SOURCE', '%s: %s' % (type(exc).__name__, exc)


@test('WS-F18', 'MUST_FAIL')
def t_cert_s1_contextvar_scoped():
    """The predecessor's validate_block seam is active only for the S1 spec's own numerics object inside the override."""
    s = make_spec(C3T_LABEL, cb_grid('C3T'))
    other = copy.deepcopy(s['numerics'])
    tok = S._S1_BLOCK.set(s['numerics'])
    try:
        a = outcome(lambda: S.W.validate_block(s['numerics']))[0]
        b = outcome(lambda: S.W.validate_block(other))[0]
    finally:
        S._S1_BLOCK.reset(tok)
    return a == 'PASS' and b == 'OrchestratorError: kept K must be 4', {'same_object': a, 'equal_copy': b}


# ================================================================================================ main
def main():
    global RUN, S, P, G12
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    a = ap.parse_args()
    RUN = Path(os.path.abspath(a.run_dir))
    os.mkdir(str(RUN))
    t0 = time.time()
    started = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    fx_ok = True
    try:
        S = load_module(SUCC_PATH, None, '_t_ws_successor')
        P = load_module(Q5B1[0], Q5B1[1], '_t_ws_q5b1_reference')
        g = types.ModuleType('_t_ws_guard012')
        g.__file__ = G12_PATH
        exec(compile(rb(G12_PATH), G12_PATH, 'exec'), g.__dict__)
        G12 = g
        FX['eps'] = wj(RUN / 'cert_eps_syn.json', {'schema': 'SYNTHETIC_EPS'})
        FX['lo'] = wj(RUN / 'cert_lo_syn.json', {'schema': 'SYNTHETIC_LO', 'coverage_complete': True, 'required_coverage_inverse_kpc': [3.0, 182.0], 'shells': [{'range_inverse_kpc': p} for p in [[3.0, 4.0], [4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0], [32.0, 64.0], [64.0, 128.0], [128.0, 182.0]]], 'producer': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/point_response_producer_cx2v002_ks2_c2v001.py', 'sha256': '99c29df639482032114f84420a309d29017cfca7fe01a8412be2757fbff75dd7'}})   # PORT (G-wave, A175): KS5'' reads the S1 slot rho's K=3 contract
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
    summary = {'schema': 'UNT_WRAPPER_S1K3_TEST_RESULTS_C2V001', 'started_utc': started,
               'finished_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'seconds': round(time.time() - t0, 1),
               'python': sys.version.split()[0], 'interpreter': sys.executable,
               'files_sha256': {p: sha(rb(p)) for p in (SUCC_PATH, G12_PATH, str(Path(__file__).resolve()))},
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
