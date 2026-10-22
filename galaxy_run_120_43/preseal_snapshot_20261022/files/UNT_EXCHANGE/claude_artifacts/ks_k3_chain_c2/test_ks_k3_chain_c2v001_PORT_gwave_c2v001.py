"""PORT (ks_k3_chain_c2 G-wave c2v001): the wave-1 KS suite run against KS3', KS4', KS5'' and KS6' (KS1, KS2, KS5 and the
KS6 lo_core/lo_config are unchanged). Adaptations are marked PORT (G-wave) and listed in README_KS_K3_GWAVE_C2V001.md.

KS1-KS6 synthetic tests (ks_k3_chain_c2 c2v001; root A160): MUST_PASS, MUST_FAIL, DIFFERENTIAL and FINDING cases.

  taskpolicy -b PY -I -B test_ks_k3_chain_c2v001.py --ks-dir DIR --run-dir DIR/synthetic/<new>

SYNTHETIC inputs only; nothing is launched; no run tree, UVT_*, C5H or NGC3198 path is opened (audit-hook fence below).
Real files READ: the successor and predecessor modules (import), the CB case block 76309ae3, the 31 CP-1 dry-plan specs
(bytes and point keys only), the A134 ruling files the c3v003 adapter's root gate re-reads, the driver_r5 uv-tail
module 2026f2b6 (the GQ kernel FINDING: kept_region/_grid on the TAIL_REANCHOR uv_tail block). Custody derive_details,
point_context, produce_eps/produce_rho and lo_core produce_current_lo are never run on real inputs: their seams
(libraries, point geometry, coefficient file, symbol evaluation, searches) are synthetic doubles, set on the successor
and on its predecessor object alike, so differential cases compare like with like. Every write is exclusive create
under --run-dir. Results: <run-dir>/TEST_RESULTS_KS_C2V001.json.
"""
import os
for _k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS',
           'BLIS_NUM_THREADS'):
    os.environ[_k] = '1'
import argparse
import copy
import hashlib
import importlib.util
import json
import math
import struct
import sys
import time
import traceback
import types
from pathlib import Path

import numpy as np

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
CERT = ART + '/calib_tail_readiness_cx2/certificates_per_point'
CB_PATH = ART + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json'
CB_SHA = '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'
SPEC_DIR = ART + '/step4_launch_readiness_c4/dryplans/specs_v001/specs'
C3T_LABEL = 'S1 transfer test C3T at u_A theta 0123456789abcdef; base 89abcdef'
C4T_LABEL = 'S1 transfer test C4T at u_A theta 0123456789abcdef; base 89abcdef'
KPC = 3.0856775814913673e19
SYN = 'ks_k3_chain_c2 c2v001 synthetic test fixture; not a measurement, not a review, not a ruling'
PRED = {
    'custody': (CERT + '/custody_cx2v002.py', '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377'),
    'response': (CERT + '/point_response_producer_cx2v002.py', 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'),
    'guard_b1': (ART + '/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py', '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'),
    'common': (ART + '/s4rc1_c3/build_c3v004/s4rc1_common_c3v004.py', '53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083'),
    'runner': (ART + '/s4rc1_c3/build_c3v004/cp1_runner_c3v004.py', '3f5e5c188d4a6967afdb3bfab805d1cc8650e9c26793895096be55ca8f4f1a48'),
    'assembler': (ART + '/s4rc1_c3/build_c3v004/registry_assembler_c3v004.py', 'cb5c61ee3d515588394c694b115aca733426db670385eddf92ed389894d065b0'),
    'lo_core': (CERT + '/lo_core_r5_cx2v001.py', '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e'),
    'lo_config': (CERT + '/lo_config_r5_cx2v001.py', '6654d93c0241afd230d90bfcf327f16c22dd24c4da1d3eea72602212c2b6ae5a'),
    'adapter': (ART + '/s4rc1_c3/proof_side_c3v003/lo_state_proof_adapter_c3v003.py', '211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c'),
    'handoff': (ART + '/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py', '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'),
    'wrapper_s1k3': (ART + '/s1_successors_c2/calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v001.py', 'e7f52461c33d45d7e506daf25a8c115161cf5cfe661e31afd5a2b1848443856e'),
    'uvt_lapse': (ART + '/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py', '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'),
}
NAMES = {   # PORT (G-wave): KS5P, KS3C, KS3R, KS4, KS6AD and KS6HO are their G-wave successors (in --gw-dir)
    'KS1': 'custody_cx2v002_ks1_c2v001.py', 'KS2': 'point_response_producer_cx2v002_ks2_c2v001.py',
    'KS5': 'certificate_guard_b1_ks5_c2v001.py', 'KS5P': 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003.py',
    'KS3C': 's4rc1_common_c3v004_ks3_c2v002.py', 'KS3R': 'cp1_runner_c3v004_ks3_c2v002.py',
    'KS4': 'registry_assembler_c3v004_ks4_c2v002.py', 'KS6CORE': 'lo_core_r5_cx2v001_ks6_c2v001.py',
    'KS6CFG': 'lo_config_r5_cx2v001_ks6_c2v001.py', 'KS6AD': 'lo_state_proof_adapter_c3v003_ks6_c2v002.py',
    'KS6HO': 'acceptance_handoff_c2v004_ks6_c2v002.py'}
GW_KEYS = ('KS5P', 'KS3C', 'KS3R', 'KS4', 'KS6AD', 'KS6HO')   # PORT (G-wave)
RESULTS = []
FENCE = {'refused': []}


def _fence(event, args):
    if event not in ('open', 'os.mkdir', 'os.listdir', 'os.scandir'):
        return
    if not args or not isinstance(args[0], (str, bytes, os.PathLike)):
        return
    p = os.fsdecode(args[0])
    parts = [s.casefold() for s in Path(p).parts]
    if ('runs' in parts or 'runs_ext' in parts or 'unt_internal_runs' in parts or 'kmax_a2f10_c5h_run_v001' in parts
            or 'cp1_run_c3v004' in parts or '.codex' in parts or 'c5h_hull_c2' in parts
            or any(s.startswith('uvt_') or 'ngc3198' in s for s in parts) or p.startswith('/Volumes/External1')):
        FENCE['refused'].append(p)
        raise PermissionError('KS_TEST_FENCE_FORBIDDEN_PATH ' + p)


sys.addaudithook(_fence)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, 'rb') as f:
        return sha_bytes(f.read())


def pin_file(p):
    return {'path': str(p), 'sha256': sha_file(p)}


def canonical(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(o):
    return sha_bytes(canonical(o))


def load(path, name, sha=None):
    with open(path, 'rb') as f:
        raw = f.read()
    if sha is not None and sha_bytes(raw) != sha:
        raise SystemExit('PIN MISMATCH ' + path)
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    exec(compile(raw, str(path), 'exec'), m.__dict__)
    return m


def record(tid, kind, ok, detail):
    RESULTS.append({'id': tid, 'kind': kind, 'passed': bool(ok), 'detail': detail})


def outcome(fn):
    try:
        return 'PASS', fn()
    except Exception as exc:
        return '%s: %s' % (type(exc).__name__, exc), None


def case(tid, kind):
    def deco(fn):
        try:
            ok, det = fn()
        except Exception as exc:
            ok, det = False, 'EXCEPTION %s: %s | %s' % (type(exc).__name__, exc, traceback.format_exc(limit=6)[-1500:])
        record(tid, kind, ok, det)
        return fn
    return deco


class Fixtures:
    def __init__(self, root):
        self.root = root
        self.n = 0

    def path(self, rel):
        p = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        return p

    def raw(self, rel, data):
        p = self.path(rel)
        with open(p, 'xb') as f:
            f.write(data)
        return {'path': p, 'sha256': sha_bytes(data)}

    def json(self, rel, obj):
        if isinstance(obj, dict) and 'synthetic_fixture' not in obj:
            obj = dict(obj, synthetic_fixture=SYN)
        return self.raw(rel, json.dumps(obj, sort_keys=True, indent=1, allow_nan=False).encode() + b'\n')

    def uniq(self, stem):
        self.n += 1
        return '%s_%03d' % (stem, self.n)


def cb_grid(case_):
    with open(CB_PATH, 'rb') as f:
        raw = f.read()
    assert sha_bytes(raw) == CB_SHA
    return copy.deepcopy(json.loads(raw)['cases'][case_]['normalized_spec_equal']['/numerics']['composite_grid_spec'])


def grid_k(k):
    """s1k3 c2v001 test L120-133: a synthetic grid with last break k (CB C4T's seed panels plus outer unit panels)."""
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


def spec_with(base, label=None, grid=None, mut=None):
    s = copy.deepcopy(base)
    if label is not None:
        s['label'] = label
    if grid is not None:
        s['numerics']['composite_grid_spec'] = copy.deepcopy(grid)
    if mut:
        mut(s)
    return s




PROOF = 'UNT_CALIBRATION_POINT_PROOF_CX2V001'
BUNDLE = 'UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001'
ENV_RULE = 'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS'
ACC_RULE = 'ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED'
CUSTODY_KEYS = ('grid_sha256', 'background_sha256', 'geometry_sha256', 'modules_sha256', 'row_contract_sha256')
SLOT_RULE = 'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE'
HANDOFF_RULE = 'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'


def partition(K):
    edges = [K] + [e for e in (4, 5, 6, 8, 12, 16, 32, 64) if e > K] + [128, 182]
    return [[float(a), float(b)] for a, b in zip(edges[:-1], edges[1:])]


def fib_sphere(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    th = math.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], axis=1)


def strip(obj, keys):
    """Copy of a dict without run-metadata keys (top level)."""
    return {k: v for k, v in obj.items() if k not in keys} if isinstance(obj, dict) else obj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ks-dir', required=True)
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--gw-dir')                                    # PORT (G-wave): the G-wave successors' folder
    a = ap.parse_args()
    KS = os.path.realpath(a.ks_dir)
    GWD = os.path.realpath(a.gw_dir or a.ks_dir)
    run = os.path.abspath(a.run_dir)
    if not run.startswith((KS + '/synthetic/', KS + '/dev/')):
        raise SystemExit('REFUSED: --run-dir must be a new folder under <ks-dir>/synthetic/')
    os.makedirs(os.path.dirname(run), exist_ok=True)
    os.mkdir(run)
    FX = Fixtures(run)
    t0 = time.time()
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1):
        raise SystemExit('REFUSED: python3 -I -B required')
    M = {k: load(os.path.join(GWD if k in GW_KEYS else KS, n), 'kst_' + k.lower()) for k, n in NAMES.items()}   # PORT (G-wave)
    KS1, KS2, KS5, S5 = M['KS1'], M['KS2'], M['KS5'], M['KS5P']
    R3, A4, L6, F6, AD6, H6 = M['KS3R'], M['KS4'], M['KS6CORE'], M['KS6CFG'], M['KS6AD'], M['KS6HO']
    C = R3.C                                        # the runner's own KS3 common instance
    P1, P2, PL6, PF6 = KS1.P, KS2.P, L6.P, F6.P      # the predecessor objects the successors hold
    PRED_R = load(PRED['runner'][0], 'kst_pred_runner', PRED['runner'][1])
    PRED_A = load(PRED['assembler'][0], 'kst_pred_assembler', PRED['assembler'][1])
    PRED_C = PRED_R.C
    B1G = load(PRED['guard_b1'][0], 'kst_pred_guard_b1', PRED['guard_b1'][1])
    PAD = load(PRED['adapter'][0], 'kst_pred_adapter', PRED['adapter'][1])
    rows = C.point_rows()
    specs = {}
    for r in rows:
        with open(r['spec_path'], 'rb') as f:
            specs[r['row']] = json.loads(f.read())
    BASE = specs[1]
    C3T = spec_with(BASE, C3T_LABEL, cb_grid('C3T'))
    C3T_ID = C.point_identity(C3T)
    K4_ID = C.point_identity(BASE)
    with open(FX.path('placeholder/SYNTHETIC_PRODUCER_PLACEHOLDER.txt'), 'xb') as f:
        f.write(b'synthetic proof producer placeholder (ks_k3_chain_c2 tests); not a producer\n')
    TP = pin_file(FX.path('placeholder/SYNTHETIC_PRODUCER_PLACEHOLDER.txt'))
    CUST = {k: digest('synthetic ' + k) for k in CUSTODY_KEYS}
    KSPIN = {k: {'path': os.path.join(GWD if k in GW_KEYS else KS, n), 'sha256': sha_file(os.path.join(GWD if k in GW_KEYS else KS, n))}
             for k, n in NAMES.items()}   # PORT (G-wave)

    # ============================================================================================ chain pins
    @case('X-P1_chain_pins_consistent_from_bytes', 'MUST_PASS')
    def _():
        got = {
            'KS2.CUSTODY_SHA=KS1': KS2.CUSTODY_SHA == KSPIN['KS1']['sha256'] and str(KS2.CUSTODY_PATH) == KSPIN['KS1']['path'],
            'KS3C.custody_ks1': list(C.PINS['custody_ks1']) == [KSPIN['KS1']['path'], KSPIN['KS1']['sha256']],
            'KS3C.response_producer_ks2': list(C.PINS['response_producer_ks2']) == [KSPIN['KS2']['path'], KSPIN['KS2']['sha256']],
            'KS3C.guard_ks5': list(C.PINS['guard_ks5']) == [KSPIN['KS5']['path'], KSPIN['KS5']['sha256']],
            'KS3C.wrapper_s1k3_ks5pp': list(C.PINS['wrapper_s1k3_ks5pp']) == [KSPIN['KS5P']['path'], KSPIN['KS5P']['sha256']],   # PORT (G-wave): KS5''
            'KS3R.COMMON_SHA': R3.COMMON_SHA == KSPIN['KS3C']['sha256'], 'KS4.COMMON_SHA': A4.COMMON_SHA == KSPIN['KS3C']['sha256'],
            'KS5P.GUARD_KS5': list(S5.GUARD_KS5) == [KSPIN['KS5']['path'], KSPIN['KS5']['sha256']],
            'KS6CORE.RESPONSE=KS2': str(L6.RESPONSE_PATH) == KSPIN['KS2']['path'] and sha_file(L6.RESPONSE_PATH) == KSPIN['KS2']['sha256'],
            'KS6CFG.BASE=KS6CORE': str(F6.BASE) == KSPIN['KS6CORE']['path'] and F6.BASE_SHA == KSPIN['KS6CORE']['sha256'],
            'KS6AD.pins': (list(AD6.CUSTODY_KS1) == [KSPIN['KS1']['path'], KSPIN['KS1']['sha256']]
                           and list(AD6.LO_CONFIG_KS6) == [KSPIN['KS6CFG']['path'], KSPIN['KS6CFG']['sha256']]
                           and list(AD6.LO_CORE_KS6) == [KSPIN['KS6CORE']['path'], KSPIN['KS6CORE']['sha256']]
                           and AD6.RESPONSE_KS2_SHA == KSPIN['KS2']['sha256']),
            'KS6HO.LO_ADAPTER_KS6': (H6.LO_ADAPTER_KS6 == dict(KSPIN['KS6AD'], entry='adapt_call_lo')),
            'predecessors_unchanged': all(sha_file(p) == h for p, h in PRED.values()),
            'predecessor_objects': (P1.__file__ == PRED['custody'][0] and P2.__file__ == PRED['response'][0]
                                    and str(PL6.__file__) == PRED['lo_core'][0] and str(PF6.__file__) == PRED['lo_config'][0]),
        }
        return all(got.values()), got

    # ============================================================================================ identity gates
    def g_edit(fn):
        g = cb_grid('C3T')
        fn(g)
        return g
    battery = {
        'S1_C3T': (spec_with(BASE, C3T_LABEL, cb_grid('C3T')), True, True),
        'campaign_label_CB_C3T_grid': (spec_with(BASE, None, cb_grid('C3T')), False, True),
        'S1_C3T_label_base_K4_grid': (spec_with(BASE, C3T_LABEL), False, False),
        'S1_C3T_label_CB_C4T_grid': (spec_with(BASE, C3T_LABEL, cb_grid('C4T')), False, False),
        'S1_C4T_label_CB_C3T_grid': (spec_with(BASE, C4T_LABEL, cb_grid('C3T')), False, True),
        'S1_C3T_label_K2_grid': (spec_with(BASE, C3T_LABEL, grid_k(2)), False, False),
        'S1_C3T_label_K5_grid': (spec_with(BASE, C3T_LABEL, grid_k(5)), False, False),
        'S1_C3T_label_CB_C6T_grid': (spec_with(BASE, C3T_LABEL, cb_grid('C6T')), False, False),
        'S1_C3T_label_C3T_grid_leaf_edited': (spec_with(BASE, C3T_LABEL, g_edit(lambda g: g.__setitem__('total_axis_nodes', 85))), False, False),
        'S1_C3T_label_C3T_last_break_3.0': (spec_with(BASE, C3T_LABEL, g_edit(lambda g: g['breaks_inverse_kpc'].__setitem__(-1, 3.0))), False, False),
        'S1_C3T_label_C3T_last_break_ulp': (spec_with(BASE, C3T_LABEL, g_edit(lambda g: g['breaks_inverse_kpc'].__setitem__(-1, 3.0000000000000004))), False, False),
        'S1_C3T_label_trailing_space': (spec_with(BASE, C3T_LABEL + ' ', cb_grid('C3T')), False, True),
        'S1_C3T_label_upper_hex': (spec_with(BASE, C3T_LABEL.replace('0123456789abcdef', '0123456789ABCDEF'), cb_grid('C3T')), False, True),
        'no_label_CB_C3T_grid': (spec_with(BASE, None, cb_grid('C3T'), lambda s: s.pop('label')), False, True),
    }

    def spec_gates(s):
        return {'KS1': KS1.s1_c3t_spec(s), 'KS2.CU': KS2.CU.s1_c3t_spec(s), 'KS3C': C.s1_c3t_spec(s), 'KS4.C': A4.C.s1_c3t_spec(s),
                'KS6CORE.CU': L6.CU.s1_c3t_spec(s), 'KS6CFG.CU': F6.CU.s1_c3t_spec(s), 'KS6AD': AD6._s1_c3t_spec(s),
                'KS6HO': H6._s1_c3t_spec(s),
                'KS5P': S5.s1_c3t_identified(s) and outcome(lambda: S5.validate_s1_c3t_block(copy.deepcopy(s['numerics'])))[0] == 'PASS'}

    def ident_gates(s):
        ident = C.point_identity(s)
        return {'KS5.kept_k==3': KS5.kept_k(ident) == 3.0, 'KS6AD._rho_contract==3': AD6._rho_contract(ident)[4] == 3}

    @case('G-P1_S1_UA_C3T_admitted_by_every_gate', 'MUST_PASS')
    def _():
        s, _, _ = battery['S1_C3T']
        sg, ig = spec_gates(s), ident_gates(s)
        return all(sg.values()) and all(ig.values()), {'spec': sg, 'identity': ig}

    @case('G-F1_every_other_spec_refused_by_every_spec_gate', 'MUST_FAIL')
    def _():
        out, ok = {}, True
        for name, (s, want_spec, want_ident) in battery.items():
            if name == 'S1_C3T':
                continue
            sg, ig = spec_gates(s), ident_gates(s)
            out[name] = {'spec_any_true': any(sg.values()), 'identity': ig}
            ok = ok and not any(sg.values()) and all(v == want_ident for v in ig.values())
        return ok, out

    # ============================================================================================ KS1 custody
    npz = FX.path('ks1/coefficients_synthetic.npz')
    with open(npz, 'xb') as f:
        np.savez(f, source_hessian_grid=np.arange(12.).reshape(3, 4), background_C=np.eye(3), background_mu=np.ones(3))
    coeff_path = BASE['coefficients']['path']
    rows_c = [{'id': 'R%02d' % i, 'radius_m': (0.5 + 0.7 * i) * KPC} for i in range(12)]
    prereg = {'row_ids': [r['id'] for r in rows_c], 'tau_km_s': [3.0 + 0.25 * i for i in range(12)]}

    def stub_custody(mod):
        real_sha, real_allowed = mod.sha, mod.allowed_path

        class D:
            GEOMETRY_PINS = {}
            uvt_static_pins = staticmethod(lambda flag: {})

        class CCs:
            pin = staticmethod(lambda name: {'path': '/synthetic/prereg_v005', 'sha256': '0' * 64})
        mod.libraries = lambda: (D, CCs)
        mod.point_geometry = lambda spec, d=None: ({'galaxies': {'DDO154': {'synthetic_distance_Mpc': spec['physical']['distance_Mpc']}}},
                                                   {'monotone': 'synthetic'}, {'query_rows': copy.deepcopy(rows_c)},
                                                   {'derivation': 'synthetic'})
        mod.read_pin = lambda ref, document=True: copy.deepcopy(prereg)
        mod.sha = lambda p: mod.A2_SHA if str(p) == coeff_path else real_sha(p)
        mod.allowed_path = lambda p: Path(npz) if str(p) == coeff_path else real_allowed(p)
    stub_custody(KS1)
    stub_custody(P1)

    @case('K1-P1_S1_UA_C3T_custody_derived_K3_cube', 'MUST_PASS')
    def _():
        d = KS1.derive_details(spec=C3T)
        ok = (d['identity']['numerics']['composite_grid_spec'] == cb_grid('C3T') and KSPIN['KS1']['path'] in d['modules']
              and PRED['custody'][0] not in d['modules'] and d['schema'] == 'DDO154_POINT_CUSTODY_CX2V001'
              and d['custody_sha256'] == digest(d['custody']) and d['point_sha256'] == digest(C3T_ID))
        return ok, {'point_sha256': d['point_sha256'][:16], 'modules_has_ks1': KSPIN['KS1']['path'] in d['modules']}

    @case('K1-P2_C3T_custody_differs_from_K4_only_in_grid_and_modules', 'MUST_PASS')
    def _():
        d3 = KS1.derive_details(spec=C3T)['custody']
        d4 = KS1.derive_details(spec=BASE)['custody']
        same = [k for k in CUSTODY_KEYS if d3[k] == d4[k]]
        return sorted(set(CUSTODY_KEYS) - set(same)) == ['grid_sha256', 'modules_sha256'], {'equal': same}

    @case('K1-D1_non_S1_specs_byte_identical_to_6810b7c3', 'DIFFERENTIAL')
    def _():
        out, ok = {}, True
        cases_ = {('row%02d' % r): s for r, s in specs.items()}
        cases_.update({k: v[0] for k, v in battery.items() if k != 'S1_C3T'})
        for name, s in cases_.items():
            a_, b_ = outcome(lambda: KS1.derive_details(spec=copy.deepcopy(s))), outcome(lambda: P1.derive_details(spec=copy.deepcopy(s)))
            c_, d_ = (outcome(lambda: KS1.derive_custody(spec=copy.deepcopy(s), driver_sha256=KS1.DRIVER_SHA)),
                      outcome(lambda: P1.derive_custody(spec=copy.deepcopy(s), driver_sha256=P1.DRIVER_SHA)))
            same = (a_[0] == b_[0] and (a_[1] is None or canonical(a_[1]) == canonical(b_[1]))
                    and c_[0] == d_[0] and (c_[1] is None or canonical(c_[1]) == canonical(d_[1])))
            out[name] = a_[0][:60] if not same else ('equal: ' + a_[0][:50])
            ok = ok and same
        return ok, out

    @case('K1-F1_K3_refused_outside_S1_UA_C3T', 'MUST_FAIL')
    def _():
        r = {n: outcome(lambda n=n: KS1.derive_details(spec=battery[n][0]))[0] for n in
             ('campaign_label_CB_C3T_grid', 'S1_C4T_label_CB_C3T_grid', 'S1_C3T_label_K2_grid', 'S1_C3T_label_C3T_grid_leaf_edited',
              'S1_C3T_label_trailing_space')}
        r['S1_C3T_truncation_sphere'] = outcome(lambda: KS1.derive_details(
            spec=spec_with(C3T, mut=lambda s: s['numerics'].__setitem__('truncation', {'shape': 'sphere'}))))[0]
        ok = all('K4 cube required' in v for k, v in r.items() if k != 'S1_C3T_truncation_sphere') and \
            'K3 cube required (S1_UA_C3T)' in r['S1_C3T_truncation_sphere']
        return ok, r

    # ============================================================================================ KS2 response producer
    @case('K2-P1_EPS_plan_179_unit_shells_from_3', 'MUST_PASS')
    def _():
        sel, complete, end = KS2.shell_plan(C3T)
        return (sel == [[float(n), float(n + 1)] for n in range(3, 182)] and len(sel) == 179 and complete is True
                and end == 182), {'n': len(sel), 'first': sel[0], 'last': sel[-1]}

    @case('K2-P2_rho_plan_10_shell_partition_from_3', 'MUST_PASS')
    def _():
        sel, complete, end = KS2.shell_plan(C3T, unit=False)
        want = [[3.0, 4.0], [4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0], [32.0, 64.0],
                [64.0, 128.0], [128.0, 182.0]]
        return sel == want and complete is True, sel

    ranges_variants = [None, [[4, 5]], [[5, 6], [6, 7]], [[3, 4]], [[4, 4.5]], [[181, 182]], [[182, 183]], [[4, 5], [4, 5]],
                       [[5, 6], [4, 5]], [[2, 3]], [[3, 5]], [[128, 182]]]

    @case('K2-D1_shell_plan_non_S1_identical_to_a1dcdea8', 'DIFFERENTIAL')
    def _():
        out, ok = {}, True
        cases_ = {('row%02d' % r): s for r, s in specs.items()}
        cases_.update({k: v[0] for k, v in battery.items() if k != 'S1_C3T'})
        n = 0
        for name, s in cases_.items():
            for rv in ranges_variants:
                for unit in (True, False):
                    x, y = outcome(lambda: KS2.shell_plan(s, rv, unit=unit)), outcome(lambda: P2.shell_plan(s, rv, unit=unit))
                    n += 1
                    if x != y:
                        ok = False
                        out['%s/%r/%s' % (name, rv, unit)] = [x[0], y[0]]
        return ok, {'compared': n, 'differences': out}

    @case('K2-F1_C3T_shells_outside_K3_domain_refused', 'MUST_FAIL')
    def _():
        r = {repr(rv): outcome(lambda rv=rv: KS2.shell_plan(C3T, rv))[0] for rv in ([[2, 3]], [[2.5, 3.5]], [[3, 3.5]], [[182, 183]])}
        ok = ('shell outside point domain' in r['[[2, 3]]'] and 'shell outside point domain' in r['[[2.5, 3.5]]']
              and 'EPS requires unit shells' in r['[[3, 3.5]]'] and 'shell outside point domain' in r['[[182, 183]]'])
        return ok, r

    def synth_ctx(spec):
        ident = KS2.CU.identity(spec)
        return {'details': {'identity': ident, 'point_sha256': digest(ident), 'custody': dict(CUST), 'custody_sha256': digest(CUST)},
                'L': types.SimpleNamespace(KPC=KPC), 'B': types.SimpleNamespace(gam=1.0, volume=1.0), 'isq': np.eye(3),
                'D': [fib_sphere(26), fib_sphere(52), fib_sphere(104)], 'cache': {}, 'E': None,
                'source_pins': {'synthetic': {'path': '/synthetic', 'sha256': '0' * 64}}, 'checks': {'synthetic': True}}

    def with_numeric_doubles(fn):
        saved = (KS2.CC, KS2.search_envelope, KS2.discrete_shell, KS2.actual_eps_search)
        KS2.CC = types.SimpleNamespace(shell_k=saved[0].shell_k, PER_DECADE=saved[0].PER_DECADE,
                                       full_response=lambda B, kv, chunk=2048: np.full((len(kv), 10), 0.01 + 0j))
        KS2.search_envelope = lambda ctx, lo, hi, cfg, objective='EPS', audit=False, previous=None: {
            'estimate': 1e-4 / (lo + 1.0), 'objective': objective, 'audit': audit, 'synthetic': True}
        KS2.discrete_shell = lambda ctx, lo, hi: {'eps_base': 1e-5, 'eps_refined': 1e-5, 'refinements': 0, 'certified': True,
                                                  'levels': {}}
        KS2.actual_eps_search = lambda ctx, lo, hi, cfg, discrete: {'estimate': 2e-5}
        try:
            return fn()
        finally:
            KS2.CC, KS2.search_envelope, KS2.discrete_shell, KS2.actual_eps_search = saved

    REC = {}

    @case('K2-P3_produce_rho_C3T_10_shells_coverage_3_182_samples_outside_K3_cube', 'MUST_PASS')
    def _():
        ctx = synth_ctx(C3T)
        rec = with_numeric_doubles(lambda: KS2.produce_rho(C3T, settings='registered', context=ctx))
        REC['rho3'] = rec
        first = rec['shells'][0]
        ks = [np.max(np.abs(lv['k_argmax_inverse_kpc'])) for sh in rec['shells'] for lv in sh['sampled_levels']]
        ok = ([s['range_inverse_kpc'] for s in rec['shells']] == partition(3) and rec['required_coverage_inverse_kpc'] == [3.0, 182.0]
              and rec['coverage_complete'] is True and rec['full_registered_search_executed'] is True
              and rec['producer'] == {'path': KSPIN['KS2']['path'], 'sha256': KSPIN['KS2']['sha256']}
              and all(lv['n_samples'] > 0 for sh in rec['shells'] for lv in sh['sampled_levels']) and min(ks) > 3.0
              and rec['custody'] == CUST and rec['identity'] == C3T_ID)
        chk = R3.check_rho(rec, rec['point_sha256'], CUST, s1=True)
        return ok and all(chk.values()), {'shell_3_4_samples': [lv['n_samples'] for lv in first['sampled_levels']], 'check_rho_s1': chk}

    @case('K2-F2_a1dcdea8_L347_filter_leaves_the_3_4_shell_empty', 'FINDING')
    def _():
        CCr = KS2.CC
        out = {}
        for lv in (1, 2):
            ks = CCr.shell_k(3.0, 4.0, CCr.PER_DECADE[lv])
            kv = (ks[:, None, None] * fib_sphere(52)[None, :, :] / KPC).reshape(-1, 3)
            m = np.max(np.abs(kv), axis=1) * KPC
            out['level%d' % lv] = {'samples': int(len(kv)), 'kept_K4_filter': int(np.sum(m > 4 * (1 + 1e-12))),
                                   'kept_K3_filter': int(np.sum(m > 3 * (1 + 1e-12)))}
        return all(v['kept_K4_filter'] == 0 and v['kept_K3_filter'] > 0 for v in out.values()), out

    @case('K2-P4_produce_eps_C3T_179_shells_14_audits_KS2_producer', 'MUST_PASS')
    def _():
        ctx = synth_ctx(C3T)
        rec = with_numeric_doubles(lambda: KS2.produce_eps(C3T, settings='registered', context=ctx))
        REC['eps3'] = rec
        chk = R3.check_eps(rec, rec['point_sha256'], CUST, s1=True)
        chk4 = R3.check_eps(rec, rec['point_sha256'], CUST, s1=False)
        ok = (len(rec['shells']) == 179 and rec['required_coverage_inverse_kpc'] == [3.0, 182.0]
              and len(rec['envelope_audit']) == 14 and rec['verdict'] == 'NUMERICAL_RULE_PASSED_REVIEW_REQUIRED'
              and all(chk.values()) and not chk4['shells_4_to_182_unit'] and not chk4['producer_pin_canonical_R4'])
        return ok, {'check_eps_s1': chk, 'check_eps_k4_on_k3_record': chk4}

    @case('K2-D2_non_S1_entry_points_are_a1dcdea8_objects', 'DIFFERENTIAL')
    def _():
        saved = {n: getattr(P2, n) for n in ('point_context', 'shell_plan', 'produce_eps', 'produce_rho')}
        hits = []
        for n in saved:
            setattr(P2, n, (lambda n: lambda *a, **k: ('A1DCDEA8_' + n))(n))
        try:
            res = {}
            for name, s in [('row%02d' % r, specs[r]) for r in (1, 2, 29)] + [(k, v[0]) for k, v in battery.items()]:
                res[name] = [KS2.point_context(s) if name != 'S1_C3T' else 'skip', KS2.shell_plan(s),
                             outcome(lambda: KS2.produce_eps(s, context={'details': {}}))[1] if name != 'S1_C3T' else 'skip',
                             outcome(lambda: KS2.produce_rho(s, context={'details': {}}))[1] if name != 'S1_C3T' else 'skip']
        finally:
            for n, f in saved.items():
                setattr(P2, n, f)
        ok = all(all(isinstance(x, str) and x.startswith('A1DCDEA8_') for x in v) for k, v in res.items() if k != 'S1_C3T') \
            and not str(res['S1_C3T'][1]).startswith('A1DCDEA8_')
        return ok, {k: [str(x)[:20] for x in v] for k, v in res.items()}

    # ============================================================================================ KS5 guard
    def guard_world(identity, K, *, eps_from=None, lo_from=None, Kbig=128.0, tag='g'):
        tag = FX.uniq(tag)
        psha, csha = digest(identity), digest(CUST)
        e0 = int(eps_from if eps_from is not None else K)
        eps = {'schema': PROOF, 'gate': 'EPS', 'status': 'TESTED', 'verdict': 'PASS', 'point_sha256': psha, 'custody_sha256': csha,
               'producer': TP, 'envelope_rule': ENV_RULE,
               'shells': [{'range_inverse_kpc': [float(n), float(n + 1)], 'refinement_failures': 0, 'eps': 1e-4, 'eps_envelope': 1e-4}
                          for n in range(e0, 182)]}
        gq = {'schema': PROOF, 'gate': 'GQ', 'status': 'TESTED', 'verdict': 'PASS', 'point_sha256': psha, 'custody_sha256': csha,
              'producer': TP, 'method': 'GEOMETRY_UNIFORM_COLUMN_BOUND', 'all_columns_included': True,
              'all_production_kperp_nodes': True, 'nonnegative_masses_required': True, 'M_s': 128, 'M_s_doubled': 256,
              'K_big_inverse_kpc': Kbig, 'max_column_difference_over_analytic_Pi0': 3e-14, 'max_zero_mode_relative_error': 3.5e-14}
        eps_pin, gq_pin = FX.json(tag + '/eps.json', eps), FX.json(tag + '/gq.json', gq)
        st = {'state_sha256': 'c' * 64, 'source_sha256': 'd' * 64, 'stage_kind': 'route_a', 'nonnegative_masses': True}
        part = partition(int(lo_from if lo_from is not None else K))
        lo = {'schema': PROOF, 'gate': 'LO', 'status': 'TESTED', 'verdict': 'PASS', 'point_sha256': psha, 'custody_sha256': csha,
              'producer': TP, 'state': st, 'shells': [{'range_inverse_kpc': p, 'max_over_tau': 0.001} for p in part],
              'summed_max_over_tau': 0.001 * len(part), 'row_contract_sha256': CUST['row_contract_sha256'], 'i1t_verdict': 'PASS',
              'GQ_uniform_proof_sha256': gq_pin['sha256']}
        lo_pin = FX.json(tag + '/lo.json', lo)
        b = {'schema': BUNDLE, 'identity': identity, 'custody': CUST, 'domain': {'K_inverse_kpc': K, 'K_big_inverse_kpc': Kbig},
             'prelaunch': {'EPS': eps_pin, 'GQ': gq_pin}, 'acceptance_rule': ACC_RULE, 'states': [{'state': st, 'LO': lo_pin}]}
        return FX.json(tag + '/bundle.json', b), [st]

    def guard_run(G, bpin, identity, states, phase):
        return G.verify_bundle(bpin, identity, expected_custody=CUST, approved_producer_sha256=[TP['sha256']], phase=phase,
                               required_states=states if phase == 'acceptance' else [])

    @case('K5-P1_C3T_identity_domain_K3_bundle_passes_both_phases', 'MUST_PASS')
    def _():
        bp, st = guard_world(C3T_ID, 3.0)
        r = [guard_run(KS5, bp, C3T_ID, st, ph) for ph in ('prelaunch', 'acceptance')]
        rb1 = guard_run(B1G, bp, C3T_ID, st, 'prelaunch')
        return all(x['ok'] for x in r) and rb1['ok'] is False, {'ks5': [x['blockers'] for x in r], 'b1_on_same_bundle': rb1['blockers']}

    @case('K5-F1_K4_bundle_cannot_certify_the_K3_point', 'MUST_FAIL')
    def _():
        bp, st = guard_world(C3T_ID, 4.0)
        r = guard_run(KS5, bp, C3T_ID, st, 'prelaunch')
        return r['ok'] is False and 'is not the kept K 3.0' in r['blockers'][0], r['blockers']

    @case('K5-F2_K3_domain_refused_for_every_non_C3T_identity', 'MUST_FAIL')
    def _():
        out, ok = {}, True
        for name in ('S1_C3T_label_base_K4_grid', 'S1_C3T_label_C3T_grid_leaf_edited', 'S1_C3T_label_C3T_last_break_3.0',
                     'S1_C3T_label_K2_grid', 'S1_C3T_label_K5_grid'):
            ident = C.point_identity(battery[name][0])
            bp, st = guard_world(ident, 3.0)
            a_, b_ = guard_run(KS5, bp, ident, st, 'prelaunch'), guard_run(B1G, bp, ident, st, 'prelaunch')
            out[name] = a_['blockers']
            ok = ok and a_['ok'] is False and a_['blockers'] == ['unsupported calibration domain'] and canonical(a_) == canonical(b_)
        return ok, out

    @case('K5-F3_C3T_K3_domain_with_shells_from_4_refused', 'MUST_FAIL')
    def _():
        bp, st = guard_world(C3T_ID, 3.0, eps_from=4)
        r1 = guard_run(KS5, bp, C3T_ID, st, 'prelaunch')
        bp2, st2 = guard_world(C3T_ID, 3.0, lo_from=4)
        r2 = guard_run(KS5, bp2, C3T_ID, st2, 'acceptance')
        return (r1['ok'] is False and 'EPS shell gap' in r1['blockers'][0] and r2['ok'] is False
                and 'LO shell gap' in r2['blockers'][0]), [r1['blockers'], r2['blockers']]

    @case('K5-D1_K4_identities_byte_identical_to_b1', 'DIFFERENTIAL')
    def _():
        out, ok, n = {}, True, 0
        for ident_name, ident in (('K4_base', K4_ID), ('K3_edited', C.point_identity(battery['S1_C3T_label_C3T_grid_leaf_edited'][0])),
                                  ('K2', C.point_identity(battery['S1_C3T_label_K2_grid'][0]))):
            for K in (4.0, 4, 3.0, 5.0, '4', None, True):
                for Kbig in (128.0, 64.0, 256.0):
                    for frm in (4, 3):
                        try:
                            bp, st = guard_world(ident, K, eps_from=frm, lo_from=frm, Kbig=Kbig, tag='gd')
                        except (TypeError, ValueError):
                            continue
                        for ph in ('prelaunch', 'acceptance'):
                            a_, b_ = guard_run(KS5, bp, ident, st, ph), guard_run(B1G, bp, ident, st, ph)
                            n += 1
                            if canonical(a_) != canonical(b_):
                                ok = False
                                out['%s/%r/%r/%d/%s' % (ident_name, K, Kbig, frm, ph)] = [a_['blockers'], b_['blockers']]
        return ok and n > 100, {'compared': n, 'differences': out}

    # ============================================================================================ KS5' wrapper
    Q = S5.W
    se_pin = pin_file(ART + '/s4_acceptance_c2/offset_b1/consumed_states_b1_c2v001.py')
    reg_dummy = FX.json('ks5p/registry_dummy.json', {'points': {}})

    def review(guard_sha, deriver):
        return FX.json(FX.uniq('ks5p/review') + '.json', {
            'schema': Q.POLICY_SCHEMA, 'status': 'TESTED', 'ok': True, 'driver_sha256': Q.DRIVER_SHA, 'custody_deriver': deriver,
            'state_enumerator': se_pin, 'approved_certificate_producers': [TP], 'guard_sha256': guard_sha,
            'driver_slot_rule': SLOT_RULE, 'post_state_handoff': HANDOFF_RULE})

    def c1(guard_sha, deriver, registry=reg_dummy):
        return {'tail_readiness': {'certificate_registry': registry, 'custody_deriver': deriver, 'state_enumerator': se_pin,
                                   'certificate_policy_review': review(guard_sha, deriver), 'approved_certificate_producers': [TP]}}

    def mkctx(mod, cfg, ks5=None, base=None):
        class Ctx(mod.Context):
            def __init__(self):
                self.cfg = copy.deepcopy(cfg)
                self.numerics = copy.deepcopy((base or BASE)['numerics'])
        c_ = Ctx()
        if ks5 is not None:
            c_._s1_guard_ks5 = ks5
        return c_
    KS1PIN = KSPIN['KS1']
    CFG_KS5 = c1(KSPIN['KS5']['sha256'], KS1PIN)
    CFG_B1 = c1(PRED['guard_b1'][1], KS1PIN)

    @case('P-P1_policy_binds_ks5_detection', 'MUST_PASS')
    def _():
        broken = copy.deepcopy(CFG_KS5)
        broken['tail_readiness']['certificate_policy_review'] = dict(broken['tail_readiness']['certificate_policy_review'], sha256='0' * 64)
        r = {'ks5': S5._policy_binds_ks5(CFG_KS5), 'b1': S5._policy_binds_ks5(CFG_B1), 'empty': S5._policy_binds_ks5({}),
             'broken_pin': S5._policy_binds_ks5(broken), 'none': S5._policy_binds_ks5(None)}
        return r == {'ks5': True, 'b1': False, 'empty': False, 'broken_pin': False, 'none': False}, r

    @case('P-P2_policy_gate_scope_KS5_bound_C1_ok_b1_scope_pending', 'MUST_PASS')
    def _():
        g_ks5 = mkctx(S5, CFG_KS5, ks5=True).certificate_policy_gate()
        g_ks5_in_b1 = mkctx(S5, CFG_KS5, ks5=False).certificate_policy_gate()
        g_b1 = mkctx(S5, CFG_B1, ks5=False).certificate_policy_gate()
        g_q = mkctx(Q, CFG_B1).certificate_policy_gate()
        g_q_ks5 = mkctx(Q, CFG_KS5).certificate_policy_gate()
        ok = (g_ks5['ok'] is True and g_ks5_in_b1['ok'] is False and 'binding mismatch: guard_sha256' in g_ks5_in_b1['reasons']
              and g_b1['ok'] is True and canonical(g_b1) == canonical(g_q) and canonical(g_ks5_in_b1) == canonical(g_q_ks5))
        return ok, {'ks5_bound': g_ks5['ok'], 'ks5_bound_in_b1_scope': g_ks5_in_b1['reasons'], 'q5b1_on_ks5_c1': g_q_ks5['reasons']}

    @case('P-P3_guard_dispatch_KS5_only_inside_S1_UA_C3T_scope', 'MUST_PASS')
    def _():
        seen = []

        class StubBase(Q.Context):
            def certificate_check(self, spec, phase, *, result=None, call_dir=None, _handoff=None):
                seen.append((spec.get('label'), Q.G.__file__, Q.G.verify_bundle.__code__.co_filename, self.certificate_policy_gate()['ok']))
                return {'ok': False, 'blockers': ['stub']}

        class T(S5.Context, StubBase):
            def __init__(self):
                self.cfg = copy.deepcopy(CFG_KS5)
                self._s1_guard_ks5 = True
        t = T()
        t.certificate_check(C3T, 'prelaunch')
        t.certificate_check(BASE, 'prelaunch')
        t.certificate_check(battery['campaign_label_CB_C3T_grid'][0], 'prelaunch')
        outside = (Q.G.__file__, S5._GUARD.get())
        ks5p, b1p = KSPIN['KS5']['path'], PRED['guard_b1'][0]
        ok = (seen[0][1] == ks5p and seen[0][2] == ks5p and seen[0][3] is True
              and seen[1][1] == b1p and seen[1][2] == b1p and seen[1][3] is False
              and seen[2][1] == b1p and outside == (b1p, None))
        return ok, {'seen': [(str(x[0])[:24], os.path.basename(x[1]), x[3]) for x in seen], 'outside': os.path.basename(outside[0])}

    # ---------------------------------------------------------------- shared record builders (KS5', KS3, KS4, KS6)
    PLACE = {}
    for nm in ('EPS_ADAPTER', 'GQ_PRODUCER', 'SLOT_PRODUCER'):
        with open(FX.path('placeholder/%s.txt' % nm), 'xb') as f:
            f.write(('synthetic %s placeholder (ks_k3_chain_c2 tests); not a producer\n' % nm).encode())
        PLACE[nm] = pin_file(FX.path('placeholder/%s.txt' % nm))
    APPROVED = [PLACE['EPS_ADAPTER'], PLACE['GQ_PRODUCER'], PLACE['SLOT_PRODUCER']]
    KS2PIN = {'path': KSPIN['KS2']['path'], 'sha256': KSPIN['KS2']['sha256']}
    A1PIN = {'path': PRED['response'][0], 'sha256': PRED['response'][1]}
    ANCHOR_PINS = {'custody': C.canonical_pin('custody'), 'producer': C.canonical_pin('response_producer'),
                   'envelope': {'path': CERT + '/certs2_common_r5_cx2v001.py', 'sha256': 'f8f422f034153b4551e5fd5f89740cb594cb9d877e54b467c617206d2fcd6d8c'},
                   'lwr_common': {'path': '/synthetic/lwr_common_v001.py', 'sha256': '1' * 64},
                   'reference_symbols': {'path': '/synthetic/symbols.py', 'sha256': '2' * 64}}

    def pins_k3(**over):
        p = dict(ANCHOR_PINS, custody=C.canonical_pin('custody_ks1'), producer=C.canonical_pin('response_producer_ks2'))
        p.update(over)
        return p

    def eps_record(spec, K, producer, deps):
        ident = C.point_identity(spec)
        sh = [{'range_inverse_kpc': [float(n), float(n + 1)], 'lo_inverse_kpc': float(n), 'hi_inverse_kpc': float(n + 1),
               'eps': 1e-4 / (n - 1), 'eps_envelope': 1e-4 / (n - 1), 'eps_base': 5e-5 / (n - 1), 'eps_refined': 5e-5 / (n - 1),
               'refinements': 0, 'certified': True, 'actual': {'estimate': 9e-5 / (n - 1)}} for n in range(int(K), 182)]
        return {'schema': 'UNT_POINT_EPS_NUMERICAL_CX2V001', 'gate': 'EPS', 'status': 'TESTED', 'identity': ident,
                'point_sha256': digest(ident), 'custody': dict(CUST), 'producer': producer, 'dependencies': deps,
                'settings': 'registered', 'full_registered_search_executed': True, 'coverage_complete': True,
                'registered_discrete_verdict': 'CERTIFIED', 'verdict': 'NUMERICAL_RULE_PASSED_REVIEW_REQUIRED', 'shells': sh,
                'envelope_audit': [{'range_inverse_kpc': [float(n), float(n + 1)]} for n in (4, 5, 6, 8, 12, 16, 19, 32, 45, 63, 64, 100, 128, 181)],
                'eps_max': 1e-4, 'eps_max_shell': [float(K), float(K) + 1], 'required_coverage_inverse_kpc': [float(K), 182.0],
                'seconds': 1.0, 'peak_rss_bytes': 1}

    def rho_record(spec, K, producer, deps):
        ident = C.point_identity(spec)
        return {'schema': 'UNT_POINT_RHO_NUMERICAL_CX2V001', 'gate': 'RHO_G', 'status': 'TESTED', 'utc': '2026-10-19T00:00:00Z',
                'identity': ident, 'point_sha256': digest(ident), 'custody': dict(CUST), 'producer': producer, 'dependencies': deps,
                'settings': 'registered', 'verdict': 'NUMERICAL_ESTIMATE_REVIEW_REQUIRED', 'coverage_complete': True,
                'required_coverage_inverse_kpc': [float(K), 182.0], 'full_registered_search_executed': True,
                'shells': [{'range_inverse_kpc': p, 'rho_used': 0.02 - 0.001 * i, 'rho_envelope': {'estimate': 0.02 - 0.001 * i},
                            'sampled_levels': [{'level': 1, 'estimate': 0.01, 'n_samples': 10}]} for i, p in enumerate(partition(int(K)))],
                'seconds': 1.0, 'peak_rss_bytes': 1}

    def gq_record(spec, producer=None):
        ident = C.point_identity(spec)
        return {'schema': PROOF, 'gate': 'GQ', 'status': 'TESTED', 'verdict': 'PASS', 'point_sha256': digest(ident),
                'custody_sha256': digest(CUST), 'producer': producer or C.canonical_pin('gq_producer_g3' if C.s1_c3t_spec(spec) else 'gq_producer'),   # PORT (G-wave): row 32's GQ producer is G3
                'method': 'GEOMETRY_UNIFORM_COLUMN_BOUND', 'all_columns_included': True, 'all_production_kperp_nodes': True,
                'nonnegative_masses_required': True, 'M_s': 128, 'M_s_doubled': 256, 'K_big_inverse_kpc': 128.0,
                'max_column_difference_over_analytic_Pi0': 3e-14, 'max_zero_mode_relative_error': 3.5e-14,
                'nodes_tested': 20736, 'production_nodes': 20736, 'seconds': 1.0}

    def eps_proof_doc(spec, K, slot, producer, eps_from=None):
        ident = C.point_identity(spec)
        return {'schema': PROOF, 'gate': 'EPS', 'status': 'TESTED', 'verdict': 'PASS', 'point_sha256': digest(ident),
                'custody_sha256': digest(CUST), 'producer': producer, 'driver_certificate': slot, 'numeric_evidence': slot,
                'envelope_rule': ENV_RULE,
                'shells': [{'range_inverse_kpc': [float(n), float(n + 1)], 'eps': 1e-4, 'eps_envelope': 1e-4, 'refinement_failures': 0}
                           for n in range(int(eps_from if eps_from is not None else K), 182)]}

    def slot_proof_doc(spec, rho_pin, rho_doc, producer):
        ident = C.point_identity(spec)
        return {'schema': PROOF, 'gate': 'LO_RHO_SLOT', 'status': 'TESTED', 'verdict': 'PASS', 'point_sha256': digest(ident),
                'custody_sha256': digest(CUST), 'producer': producer, 'driver_certificate': rho_pin, 'rho_record': rho_pin,
                'rho_bitwise_projection': AD6.rho_projection(rho_doc)}

    # ============================================================================================ KS5' end to end
    with open(FX.path('ks5p/synthetic_custody_deriver.py'), 'xb') as f:
        f.write(("CUSTODY = %r\ndef derive_custody(*, spec, driver_sha256):\n    return dict(CUSTODY)\n" % CUST).encode())
    DERIVER = pin_file(FX.path('ks5p/synthetic_custody_deriver.py'))

    def cert_world(spec0, K, tag, *, eps_from=None, domain_K=None, guard_sha=None, rho_K=None):
        tag = FX.uniq(tag)
        es = FX.json(tag + '/EPS_NUMERIC.json', eps_record(spec0, K, KS2PIN, pins_k3()))
        rdoc = rho_record(spec0, rho_K or K, KS2PIN, pins_k3())
        rs = FX.json(tag + '/RHO_NUMERIC.json', rdoc)
        spec = copy.deepcopy(spec0)
        spec['numerics']['uv_tail']['eps_certificate'], spec['numerics']['uv_tail']['lo_certificate'] = es, rs
        ident = C.point_identity(spec)
        ep = FX.json(tag + '/EPS_PROOF.json', eps_proof_doc(spec, K, es, TP, eps_from))
        gp = FX.json(tag + '/GQ_PROOF.json', gq_record(spec, TP))
        lp = FX.json(tag + '/SLOT_PROOF.json', slot_proof_doc(spec, rs, rdoc, TP))
        b = FX.json(tag + '/BUNDLE.json', {'schema': BUNDLE, 'identity': ident, 'custody': CUST,
                                          'domain': {'K_inverse_kpc': float(domain_K if domain_K is not None else K), 'K_big_inverse_kpc': 128.0},
                                          'prelaunch': {'EPS': ep, 'GQ': gp, 'LO_RHO_SLOT': lp},
                                          'driver_certificate_bindings': {'eps_certificate': es, 'lo_certificate': rs},
                                          'acceptance_rule': ACC_RULE, 'point_sha256': digest(ident), 'custody_sha256': digest(CUST)})
        reg = FX.json(tag + '/REGISTRY.json', {'points': {digest(ident): {'identity': ident, 'bundle': b, 'eps_certificate': es,
                                                                         'lo_certificate': rs}}})
        return spec, c1(guard_sha or KSPIN['KS5']['sha256'], DERIVER, reg)
    S1K3_V1 = load(PRED['wrapper_s1k3'][0], 'kst_pred_wrapper_s1k3_c2v001', PRED['wrapper_s1k3'][1])

    @case('P-P4_S1_UA_C3T_certificate_check_passes_with_KS5_and_K3_bundle', 'MUST_PASS')
    def _():
        spec, cfg = cert_world(C3T, 3, 'ks5p_ok')
        g = mkctx(S5, cfg, ks5=True).certificate_check(spec, 'prelaunch')
        g_pred = outcome(lambda: mkctx(S1K3_V1, cfg).certificate_check(spec, 'prelaunch'))
        g_q = outcome(lambda: mkctx(Q, cfg).certificate_check(spec, 'prelaunch'))
        return (g.get('ok') is True and g_pred[1] is not None and g_pred[1]['ok'] is False and g_q[0] != 'PASS'), {
            'ks5p': g.get('blockers'), 's1k3_c2v001': (g_pred[1] or {}).get('blockers'), 'q5b1': g_q[0][:120]}

    @case('P-F2_S1_UA_C3T_K4_bundle_or_b1_C1_refused', 'MUST_FAIL')
    def _():
        spec, cfg = cert_world(C3T, 3, 'ks5p_k4b', domain_K=4.0, eps_from=4)
        g1 = mkctx(S5, cfg, ks5=True).certificate_check(spec, 'prelaunch')
        spec2, cfg2 = cert_world(C3T, 3, 'ks5p_b1c1', guard_sha=PRED['guard_b1'][1])
        g2 = mkctx(S5, cfg2, ks5=False).certificate_check(spec2, 'prelaunch')
        spec3, cfg3 = cert_world(C3T, 3, 'ks5p_k4rho', rho_K=4)
        g3 = mkctx(S5, cfg3, ks5=True).certificate_check(spec3, 'prelaunch')
        ok = (g1['ok'] is False and 'is not the kept K 3.0' in str(g1['blockers'])
              and g2['ok'] is False and 'binding mismatch: guard_sha256' in str(g2['blockers'])
              and g3['ok'] is False and 'S1_UA_C3T_RHO_SLOT_NOT_THE_K3_CONTRACT' in str(g3['blockers']))   # PORT (G-wave, A175)
        return ok, {'k4_bundle': g1['blockers'], 'b1_bound_c1': g2['blockers'], 'k4_rho_slot': g3.get('blockers'),
                    'note_k4_rho_slot': 'PORT (G-wave, A175): KS5\'\' now checks the slot rho at prelaunch (wave 1 read ok)'}

    @case('P-D1_non_S1_certificate_check_identical_to_s1k3_c2v001_and_q5b1', 'DIFFERENTIAL')
    def _():
        out, ok = {}, True
        for nm, (spec0, K) in {'K4_base': (BASE, 4), 'S1_C4T_label_K4': (spec_with(BASE, C4T_LABEL), 4)}.items():
            for gname, gsha, ks5 in (('b1_c1', PRED['guard_b1'][1], False), ('ks5_c1', KSPIN['KS5']['sha256'], True)):
                spec, cfg = cert_world(spec0, K, 'ks5p_d_' + nm, guard_sha=gsha)
                r = [mkctx(S5, cfg, ks5=ks5).certificate_check(spec, 'prelaunch'), mkctx(S1K3_V1, cfg).certificate_check(spec, 'prelaunch'),
                     mkctx(Q, cfg).certificate_check(spec, 'prelaunch')]
                same = canonical(r[0]) == canonical(r[1]) == canonical(r[2])
                out['%s/%s' % (nm, gname)] = {'same': same, 'ok': r[0].get('ok'), 'blockers': str(r[0].get('blockers'))[:120]}
                ok = ok and same and r[0]['ok'] is (gname == 'b1_c1')
        return ok, out

    # ============================================================================================ KS3 row 32
    with open(FX.path('s1_specs/S1_UA_C3T_0123456789abcdef.cp1.spec.json'), 'xb') as f:
        raw32 = json.dumps(C3T, sort_keys=True, indent=1).encode() + b'\n'
        f.write(raw32)
    spec32_path = FX.path('s1_specs/S1_UA_C3T_0123456789abcdef.cp1.spec.json')
    prefix = os.path.relpath(os.path.dirname(spec32_path), ART) + '/'
    key32 = C.point_key(C3T)
    rowdoc = {'schema': C.S1_ROW_SCHEMA, 'row': 32, 'key': key32, 'label': 'S1_UA_C3T', 'names': ['S1_UA_C3T'],
              'spec_path': prefix + os.path.basename(spec32_path), 'spec_sha256': sha_bytes(raw32), 'distance_Mpc': 4.04, 'q_inf': 8.062}

    def write_row(doc, name):
        p = FX.path('s1_rows/' + FX.uniq(name) + '.json')
        with open(p, 'xb') as f:
            f.write(json.dumps(doc, sort_keys=True).encode())
        return p
    good_row = write_row(rowdoc, 'ROW32_ok')
    COMMONS = (C, A4.C, M['KS3C'])

    def set_row(p):
        for mod in COMMONS:
            mod.S1_ROW_FILE, mod.S1_SPEC_PREFIX = p, prefix
    set_row(good_row)

    @case('R-P1_row32_from_root_row_file', 'MUST_PASS')
    def _():
        r = C.s1_rows()
        ok = (len(r) == 1 and r[0]['row'] == 32 and r[0]['key'] == key32 and r[0]['s1_c3t'] is True and r[0]['kept_K'] == 3
              and C.select_points('1,32')[1]['key'] == key32 and [x['row'] for x in C.select_points('1,32')] == [1, 32]
              and C.select_points('S1_UA_C3T')[0]['key'] == key32 and C.select_points(key32[:12])[0]['key'] == key32
              and len(C.select_points(None)) == 31 and C.rows_for_key(key32)[0]['row'] == 32 and C.domain_of_row(r[0])['K_inverse_kpc'] == 3.0)
        return ok, {'row': {k: r[0][k] for k in ('row', 'label', 'kept_K')}}

    @case('R-D1_table_selections_identical_to_c3v004_and_never_read_the_row_file', 'DIFFERENTIAL')
    def _():
        corrupt = write_row({'not': 'a row'}, 'ROW32_corrupt')
        set_row(corrupt)
        try:
            toks = [None, ''] + [str(i) for i in range(1, 32)] + [r['names'][0] for r in rows] + [r['key'][:8] for r in rows] + \
                   [r['key'] for r in rows] + ['1,2,3', '31,1', 'TAIL_REANCHOR,HEADLINE_CORNER_000', '1,1']
            diffs = {}
            for t in toks:
                a_ = outcome(lambda: [x['key'] for x in C.select_points(t)])
                b_ = outcome(lambda: [x['key'] for x in PRED_C.select_points(t)])
                if a_ != b_:
                    diffs[repr(t)] = [a_[0], b_[0]]
            rk = outcome(lambda: [C.rows_for_key(r['key'])[0]['row'] for r in rows])
            unresolved = outcome(lambda: C.select_points('32'))[0]
        finally:
            set_row(good_row)
        return (not diffs and rk[0] == 'PASS' and 'S1_ROW_FILE_INVALID' in unresolved), {
            'tokens': len(toks), 'diffs': diffs, 'row32_with_corrupt_file': unresolved[:80]}

    @case('R-F1_invalid_row_files_refused', 'MUST_FAIL')
    def _():
        out = {}
        base_spec_raw = json.dumps(BASE, sort_keys=True).encode()
        p_k4 = FX.path('s1_specs/' + FX.uniq('K4_SPEC') + '.json')
        with open(p_k4, 'xb') as f:
            f.write(base_spec_raw)
        variants = {
            'spec_not_S1_UA_C3T': dict(rowdoc, spec_path=prefix + os.path.basename(p_k4), spec_sha256=sha_bytes(base_spec_raw), key=C.point_key(BASE)),
            'spec_sha_wrong': dict(rowdoc, spec_sha256='0' * 64), 'key_wrong': dict(rowdoc, key='0' * 64),
            'key_of_row_1': dict(rowdoc, key=rows[0]['key']), 'spec_outside_prefix': dict(rowdoc, spec_path='s4rc1_c3/x/' + os.path.basename(spec32_path)),
            'distance_mismatch': dict(rowdoc, distance_Mpc=4.1), 'row_33': dict(rowdoc, row=33), 'q_inf_zero': dict(rowdoc, q_inf=0.0),
            'extra_key': dict(rowdoc, extra=1), 'label_other': dict(rowdoc, label='S1_UA_C4T'),
        }
        for n, d in variants.items():
            set_row(write_row(d, 'ROW32_' + n))
            out[n] = outcome(lambda: C.s1_rows())[0][:90]
        set_row(good_row)
        return all('S1_ROW_FILE_INVALID' in v for v in out.values()), out

    @case('R-P2_plan_rows_1_and_32_verified', 'MUST_PASS')
    def _():
        p = R3.plan(C.select_points('1,32'))
        st = [x['status'] for x in p['points']]
        return st == ['SPEC_AND_KEY_VERIFIED'] * 2 and p['points'][1]['kept_K'] == 3, {'statuses': st, 'row32': {
            k: p['points'][1].get(k) for k in ('row', 'kept_K', 'eps_shells', 'rho')}}

    @case('R-D2_plan_of_rows_1_31_identical_to_c3v004', 'DIFFERENTIAL')
    def _():
        a_, b_ = R3.plan(C.select_points(None)), PRED_R.plan(PRED_C.select_points(None))
        drop = ('utc', 'runner', 'common')
        return canonical(strip(a_, drop)) == canonical(strip(b_, drop)), {'n': len(a_['points'])}

    @case('R-D3_check_eps_check_rho_rows_1_31_identical_to_c3v004', 'DIFFERENTIAL')
    def _():
        recs = {'eps_k4': eps_record(BASE, 4, A1PIN, ANCHOR_PINS), 'eps_k3': eps_record(C3T, 3, KS2PIN, pins_k3()),
                'rho_k4': rho_record(BASE, 4, A1PIN, ANCHOR_PINS), 'rho_k3': rho_record(C3T, 3, KS2PIN, pins_k3())}
        same = {}
        for n, r in recs.items():
            fn_a, fn_b = (R3.check_eps, PRED_R.check_eps) if n.startswith('eps') else (R3.check_rho, PRED_R.check_rho)
            same[n] = fn_a(r, r['point_sha256'], CUST) == fn_b(r, r['point_sha256'], CUST)
        return all(same.values()), same

    @case('R-P3_check_eps_check_rho_row32_K3_records', 'MUST_PASS')
    def _():
        e3, r3 = eps_record(C3T, 3, KS2PIN, pins_k3()), rho_record(C3T, 3, KS2PIN, pins_k3())
        ce, cr = R3.check_eps(e3, e3['point_sha256'], CUST, s1=True), R3.check_rho(r3, r3['point_sha256'], CUST, s1=True)
        return all(ce.values()) and all(cr.values()), {'eps': ce, 'rho': cr}

    @case('R-F2_row32_checks_refuse_K4_records_and_K4_producer', 'MUST_FAIL')
    def _():
        e4, r4 = eps_record(C3T, 4, KS2PIN, pins_k3()), rho_record(C3T, 4, KS2PIN, pins_k3())
        e3a = eps_record(C3T, 3, A1PIN, pins_k3())
        ce, cr, cp = (R3.check_eps(e4, e4['point_sha256'], CUST, s1=True), R3.check_rho(r4, r4['point_sha256'], CUST, s1=True),
                      R3.check_eps(e3a, e3a['point_sha256'], CUST, s1=True))
        ok = (ce['shells_3_to_182_unit'] is False and cr['coverage_3_to_182'] is False and cr['partition_10_shells_K_big_128'] is False
              and cp['producer_pin_canonical_R4'] is False)
        return ok, {'eps_k4': ce, 'rho_k4': cr, 'eps_a1dcdea8': cp}

    # ---- run_point
    review = FX.json('rho_review/SYNTHETIC_PROOF_SIDE_REVIEW.json', {'schema': 'SYNTHETIC_REVIEW'})
    GATE_OPEN = {'allow_rho': True, 'review_pin': review, 'review_sha256': review['sha256']}

    def loader_for(K, src, producer, eps_K=None, rho_K=None):
        def point_context(spec):
            ident = C.point_identity(spec)
            return {'details': {'identity': ident, 'point_sha256': digest(ident), 'custody': dict(CUST), 'custody_sha256': digest(CUST)},
                    'source_pins': copy.deepcopy(src), 'checks': {'synthetic': True}}
        pr = types.SimpleNamespace(point_context=point_context,
                                   produce_eps=lambda spec, **kw: eps_record(spec, eps_K or K, producer, copy.deepcopy(src)),
                                   produce_rho=lambda spec, **kw: rho_record(spec, rho_K or K, producer, copy.deepcopy(src)))
        gq = types.SimpleNamespace(produce=lambda spec, **kw: gq_record(spec))
        return lambda: (gq, pr)

    def out_root_with_anchor(tag):
        o = FX.path(FX.uniq(tag) + '/x')
        o = os.path.realpath(os.path.dirname(o))
        os.makedirs(o, exist_ok=True)
        k16 = C.ANCHOR_KEY[:16]
        d = os.path.join(o, 'P01_%s_TAIL_REANCHOR_a1' % k16)
        os.mkdir(d)
        with open(os.path.join(d, 'STAGE_CONTEXT_%s.json' % k16), 'xb') as f:
            f.write(json.dumps({'source_pins': ANCHOR_PINS, 'synthetic_fixture': SYN}).encode())
        return o

    def run32(loader, gate=GATE_OPEN, tag='run32', mod=R3, row=None):
        o = out_root_with_anchor(tag)
        row = row or C.select_points('32')[0]
        rc, summ = mod.run_point(row, o, operator_lane='KS-test', attempt=1, run_id='t', loader=loader, hold_poll_seconds=0.0,
                                 hold_sleep=lambda s: None, rho_gate_args=gate)
        pdir = os.path.join(o, mod.point_dir_name(row, 1))
        recs = {}
        for n in sorted(os.listdir(pdir)):
            if n.endswith('.json'):
                with open(os.path.join(pdir, n), 'rb') as f:
                    recs[n] = json.loads(f.read())
        return rc, summ, recs

    def stage(recs, prefix_):
        hits = [v for k, v in recs.items() if k.startswith(prefix_)]
        return hits[0] if len(hits) == 1 else {}

    @case('R-P4_run_point_row32_end_to_end_K3_records', 'MUST_PASS')
    def _():
        rc, summ, recs = run32(loader_for(3, pins_k3(), KS2PIN))
        cx, ep, rh = stage(recs, 'STAGE_CONTEXT_'), stage(recs, 'STAGE_EPS_'), stage(recs, 'STAGE_RHO_a_')
        ok = (rc == 0 and 'POINT_DONE_%s.json' % key32[:16] in recs and all(cx.get('checks', {}).values())
              and cx['checks'].get('s1_source_pins_are_ks1_and_ks2') is True and cx['checks'].get('source_pins_match_anchor') is True
              and ep.get('ok') is True and ep['checks'].get('shells_3_to_182_unit') is True and rh.get('ok') is True
              and rh['checks'].get('partition_10_shells_K_big_128') is True and rh['checks'].get('coverage_3_to_182') is True
              and stage(recs, 'POINT_START_')['producers']['eps'] == KS2PIN and stage(recs, 'POINT_START_').get('s1_c3t_row', {}).get('kept_K') == 3)
        return ok, {'rc': rc, 'stages': summ.get('stages'), 'context_checks': cx.get('checks')}

    @case('R-F3_run_point_row32_K4_source_pins_or_drift_stop_at_CONTEXT', 'MUST_FAIL')
    def _():
        rc1, s1_, r1 = run32(loader_for(3, ANCHOR_PINS, KS2PIN), tag='run32_k4pins')
        rc2, s2_, r2 = run32(loader_for(3, pins_k3(envelope={'path': '/synthetic/drift', 'sha256': '9' * 64}), KS2PIN), tag='run32_drift')
        st1, st2 = stage(r1, 'POINT_STOP_'), stage(r2, 'POINT_STOP_')
        ok = (rc1 == 3 and st1.get('stage') == 'CONTEXT' and st1['detail'].get('s1_source_pins_are_ks1_and_ks2') is False
              and rc2 == 3 and st2.get('stage') == 'CONTEXT' and st2['detail'].get('source_pins_match_anchor') is False)
        return ok, {'k4_pins': st1.get('detail'), 'drift': st2.get('detail')}

    @case('R-F4_run_point_row32_K4_EPS_or_rho_record_stops', 'MUST_FAIL')
    def _():
        rc1, _, r1 = run32(loader_for(3, pins_k3(), KS2PIN, eps_K=4), tag='run32_eps4')
        rc2, _, r2 = run32(loader_for(3, pins_k3(), KS2PIN, rho_K=4), tag='run32_rho4')
        rc3, _, r3_ = run32(loader_for(3, pins_k3(), A1PIN), tag='run32_a1')
        s1_, s2_, s3_ = stage(r1, 'POINT_STOP_'), stage(r2, 'POINT_STOP_'), stage(r3_, 'POINT_STOP_')
        ok = (rc1 == 3 and s1_.get('stage') == 'EPS' and rc2 == 3 and s2_.get('stage') == 'RHO' and rc3 == 3 and s3_.get('stage') == 'EPS')
        return ok, {'eps4': s1_.get('detail'), 'rho4': s2_.get('detail'), 'a1dcdea8_producer': s3_.get('detail')}

    VOLATILE = ('utc', 'seconds', 'cpu_seconds', 'peak_rss_bytes_process_high_water', 'pid', 'held_seconds', 'runner', 'common',
                'python', 'runtime', 'stages_seconds', 'producer_seconds', 'producer_peak_rss_bytes')

    def deep_strip(o):
        if isinstance(o, dict):
            return {k: deep_strip(v) for k, v in o.items() if k not in VOLATILE}
        if isinstance(o, list):
            return [deep_strip(v) for v in o]
        return o

    @case('R-D4_run_point_row2_identical_records_to_c3v004', 'DIFFERENTIAL')
    def _():
        row2 = C.select_points('2')[0]
        ld = loader_for(4, ANCHOR_PINS, C.canonical_pin('response_producer'))
        rc_a, sa, ra = run32(ld, gate={}, tag='run2_ks3', row=row2)
        rc_b, sb, rb = run32(ld, gate={}, tag='run2_c3v004', mod=PRED_R, row=PRED_C.select_points('2')[0])
        oa, ob = os.path.dirname(sa['point_dir']), os.path.dirname(sb['point_dir'])
        diffs = {}
        if sorted(ra) != sorted(rb):
            diffs['files'] = [sorted(ra), sorted(rb)]
        for n in ra:
            if n in rb:
                x = deep_strip(json.loads(json.dumps(ra[n]).replace(oa, '<OUT>')))
                y = deep_strip(json.loads(json.dumps(rb[n]).replace(ob, '<OUT>')))
                if canonical(x) != canonical(y):
                    diffs[n] = sorted(k for k in set(x) | set(y) if x.get(k) != y.get(k))
        same_bytes = all(canonical(ra[n]) == canonical(rb[n]) for n in ra if n.startswith(('GQ_PROOF', 'EPS_NUMERIC')))
        return rc_a == rc_b == 0 and not diffs and same_bytes, {'files': sorted(ra), 'diffs': diffs, 'gq_eps_records_identical': same_bytes}

    # ============================================================================================ KS4 assembler
    def asm_world(row, spec, K, tag, *, eps_producer, deps, eps_from=None):
        tag = FX.uniq(tag)
        es = FX.json(tag + '/EPS_NUMERIC.json', eps_record(spec, K, eps_producer, deps))
        rdoc = rho_record(spec, K, eps_producer, deps)
        rs = FX.json(tag + '/RHO_NUMERIC.json', rdoc)
        ep = FX.json(tag + '/EPS_PROOF.json', eps_proof_doc(spec, K, es, PLACE['EPS_ADAPTER'], eps_from))
        gp = FX.json(tag + '/GQ_PROOF.json', gq_record(spec, PLACE['GQ_PRODUCER']))
        lp = FX.json(tag + '/SLOT_PROOF.json', slot_proof_doc(spec, rs, rdoc, PLACE['SLOT_PRODUCER']))
        return ep, gp, lp

    def reg_dir(tag):
        d = os.path.realpath(os.path.dirname(FX.path(FX.uniq(tag) + '/x')))
        os.makedirs(d, exist_ok=True)
        return d
    row1, row32 = C.select_points('1')[0], C.select_points('32')[0]
    AW = {}

    @case('A-P1_bundle_row32_domain_K3_row1_domain_K4', 'MUST_PASS')
    def _():
        d = reg_dir('asm_ok')
        e, g, l = asm_world(row32, C3T, 3, 'asm32', eps_producer=KS2PIN, deps=pins_k3())
        b32 = A4.assemble_bundle(row32, eps_proof=e, gq_proof=g, lo_proof=l, approved=APPROVED, out_root=d)
        e1, g1, l1 = asm_world(row1, BASE, 4, 'asm1', eps_producer=A1PIN, deps=ANCHOR_PINS)
        b1 = A4.assemble_bundle(row1, eps_proof=e1, gq_proof=g1, lo_proof=l1, approved=APPROVED, out_root=d)
        AW.update(d=d, b32=b32, b1=b1, p1=(e1, g1, l1))
        with open(b32['path'], 'rb') as f:
            d32 = json.loads(f.read())
        with open(b1['path'], 'rb') as f:
            d1 = json.loads(f.read())
        return d32['domain'] == {'K_inverse_kpc': 3.0, 'K_big_inverse_kpc': 128.0} and d1['domain'] == C.DOMAIN, {
            'row32': d32['domain'], 'row1': d1['domain']}

    @case('A-D1_row1_bundle_identical_to_c3v004', 'DIFFERENTIAL')
    def _():
        d = reg_dir('asm_pred')
        e1, g1, l1 = AW['p1']
        bp = PRED_A.assemble_bundle(PRED_C.select_points('1')[0], eps_proof=e1, gq_proof=g1, lo_proof=l1, approved=APPROVED, out_root=d)
        with open(bp['path'], 'rb') as f:
            x = json.loads(f.read())
        with open(AW['b1']['path'], 'rb') as f:
            y = json.loads(f.read())
        return canonical(strip(x, ('generator', 'utc'))) == canonical(strip(y, ('generator', 'utc'))), {'pred': os.path.basename(bp['path'])}

    @case('A-P2_registry_rows_1_and_32_single_value_rule_after_mapping', 'MUST_PASS')
    def _():
        rp, mp = A4.assemble_registry([AW['b1']['path'], AW['b32']['path']], approved=APPROVED, out_root=AW['d'])
        with open(rp['path'], 'rb') as f:
            reg = json.loads(f.read())
        with open(mp['path'], 'rb') as f:
            man = json.loads(f.read())
        AW['reg'] = rp
        ok = (reg['count'] == 2 and reg['s1_c3t_points'] == [key32] and reg['complete_31_point_table'] is False
              and man['s1_c3t_c1_tail_readiness_fields']['custody_deriver'] == C.canonical_pin('custody_ks1')
              and man['s1_c3t_guard'] == C.canonical_pin('guard_ks5') and man['c1_tail_readiness_fields']['custody_deriver'] == C.canonical_pin('custody'))
        return ok, {'count': reg['count'], 'missing': len(reg['missing_points'])}

    @case('A-D2_K4_only_registry_identical_to_c3v004', 'DIFFERENTIAL')
    def _():
        d1, d2 = reg_dir('asm_reg_ks4'), reg_dir('asm_reg_pred')
        rp, mp = A4.assemble_registry([AW['b1']['path']], approved=APPROVED, out_root=d1)
        rq, mq = PRED_A.assemble_registry([AW['b1']['path']], approved=APPROVED, out_root=d2)
        docs = []
        for p in (rp, mp, rq, mq):
            with open(p['path'], 'rb') as f:
                docs.append(json.loads(f.read()))
        drop = ('generator', 'common', 'utc', 'registry')
        same_reg = canonical(strip(docs[0], drop)) == canonical(strip(docs[2], drop))
        m0, m1 = strip(docs[1], drop), strip(docs[3], drop)
        for m in (m0, m1):
            m['c1_tail_readiness_fields'] = strip(m['c1_tail_readiness_fields'], ('certificate_registry',))
        return same_reg and canonical(m0) == canonical(m1), {'registry_equal': same_reg}

    @case('A-F1_row32_EPS_record_pins_refused', 'MUST_FAIL')
    def _():
        out = {}
        for n, prod, deps in (('producer_a1dcdea8', A1PIN, pins_k3()), ('deps_K4_pins', KS2PIN, ANCHOR_PINS),
                              ('deps_drift', KS2PIN, pins_k3(lwr_common={'path': '/synthetic/other', 'sha256': '7' * 64}))):
            d = reg_dir('asm_f_' + n)
            e, g, l = asm_world(row32, C3T, 3, 'asmf' + n, eps_producer=prod, deps=deps)
            b = A4.assemble_bundle(row32, eps_proof=e, gq_proof=g, lo_proof=l, approved=APPROVED, out_root=d)
            out[n] = outcome(lambda: A4.assemble_registry([AW['b1']['path'], b['path']], approved=APPROVED, out_root=d))[0][:100]
        ok = ('S1_EPS_RECORD_PRODUCER_IS_NOT_KS2' in out['producer_a1dcdea8'] and 'S1_SOURCE_PINS_ARE_NOT_KS1_AND_KS2' in out['deps_K4_pins']
              and 'EPS_SOURCE_PINS_DIFFER_ACROSS_POINTS' in out['deps_drift'])
        return ok, out

    @case('A-F2_row32_bundle_from_a_non_S1_spec_refused', 'MUST_FAIL')
    def _():
        fake = dict(row32, spec_path=rows[0]['spec_path'], spec_sha256=rows[0]['spec_sha256'], key=rows[0]['key'])
        e1, g1, l1 = AW['p1']
        r = outcome(lambda: A4.assemble_bundle(fake, eps_proof=e1, gq_proof=g1, lo_proof=l1, approved=APPROVED, out_root=reg_dir('asm_f2')))
        return 'S1_ROW_SPEC_IS_NOT_S1_UA_C3T' in r[0], r[0][:120]

    def c1_doc(registry, deriver, guard_sha, tag):
        enum_ = C.canonical_pin('state_enumerator_g6' if guard_sha == KSPIN['KS5']['sha256'] else 'state_enumerator')   # PORT (G-wave): an S1 C1 names G6c
        rv = FX.json(FX.uniq(tag) + '/REVIEW.json', {
            'schema': 'DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001', 'status': 'TESTED', 'ok': True, 'driver_sha256': C.DRIVER_SHA,
            'custody_deriver': deriver, 'state_enumerator': enum_,
            'approved_certificate_producers': APPROVED, 'guard_sha256': guard_sha, 'driver_slot_rule': SLOT_RULE,
            'post_state_handoff': HANDOFF_RULE})
        return FX.json(FX.uniq(tag) + '/C1.json', {'tail_readiness': {
            'certificate_registry': registry, 'custody_deriver': deriver, 'state_enumerator': enum_,
            'certificate_policy_review': rv, 'approved_certificate_producers': APPROVED}})

    def verify(rows_, c1ref):
        return A4.verify_registry(AW['reg'], rows_, c1_ref=c1ref, custody_loader=lambda pin: (lambda spec: dict(CUST)), guard=B1G,
                                  guard_s1=KS5, canonical_producers=APPROVED)

    @case('A-P3_verify_row32_with_the_S1_C1_KS1_KS5', 'MUST_PASS')
    def _():
        c1s = c1_doc(AW['reg'], C.canonical_pin('custody_ks1'), KSPIN['KS5']['sha256'], 'c1s')
        rep = verify([row32], c1s)
        return rep['ok'] is True and rep['points'][0]['ok'] is True, {'s1_gate': rep.get('c1_policy_gate_s1_c3t', {}).get('blockers'),
                                                                     'point': rep['points'][0]['wrapper_replica']['blockers']}

    @case('A-F3_one_C1_never_certifies_both_kinds', 'MUST_FAIL')
    def _():
        c1s = c1_doc(AW['reg'], C.canonical_pin('custody_ks1'), KSPIN['KS5']['sha256'], 'c1s2')
        c1k = c1_doc(AW['reg'], C.canonical_pin('custody'), PRED['guard_b1'][1], 'c1k')
        a_, b_ = verify([row1, row32], c1s), verify([row1, row32], c1k)
        ok = (a_['ok'] is False and [p['ok'] for p in a_['points']] == [False, True]
              and b_['ok'] is False and [p['ok'] for p in b_['points']] == [True, False])
        return ok, {'s1_c1': [p['ok'] for p in a_['points']], 'k4_c1': [p['ok'] for p in b_['points']],
                    'row32_under_k4_c1': b_['points'][1]['wrapper_replica']['blockers'][:1]}

    @case('A-F4_K4_bundle_cannot_certify_row32', 'MUST_FAIL')
    def _():
        d = reg_dir('asm_k4b')
        e, g, l = asm_world(row32, C3T, 3, 'asmk4b', eps_producer=KS2PIN, deps=pins_k3(), eps_from=4)
        b = A4.assemble_bundle(row32, eps_proof=e, gq_proof=g, lo_proof=l, approved=APPROVED, out_root=d)
        with open(b['path'], 'rb') as f:
            doc = json.loads(f.read())
        rp, _ = A4.assemble_registry([b['path']], approved=APPROVED, out_root=d)
        c1s = c1_doc(rp, C.canonical_pin('custody_ks1'), KSPIN['KS5']['sha256'], 'c1k4b')
        rep = A4.verify_registry(rp, [row32], c1_ref=c1s, custody_loader=lambda pin: (lambda spec: dict(CUST)), guard=B1G,
                                 guard_s1=KS5, canonical_producers=APPROVED)
        bl = (rep['points'][0].get('guard_b1') or {}).get('blockers')
        return rep['ok'] is False and 'EPS shell gap' in str(bl), {'domain': doc['domain'], 'blockers': bl}

    @case('A-D4_verify_edge_cases_identical_to_c3v004', 'DIFFERENTIAL')
    def _():
        c1k = c1_doc(AW['reg'], C.canonical_pin('custody'), PRED['guard_b1'][1], 'c1ke')
        c1s = c1_doc(AW['reg'], C.canonical_pin('custody_ks1'), KSPIN['KS5']['sha256'], 'c1se')
        drop = ('utc', 'generator')
        out = {}
        for n, rows_, c1ref in (('no_rows_k4_c1', [], c1k), ('no_rows_s1_c1', [], c1s), ('row1_s1_c1', [row1], c1s)):
            a_ = verify(rows_, c1ref)
            b_ = PRED_A.verify_registry(AW['reg'], [PRED_C.select_points('1')[0]] if rows_ else [], c1_ref=c1ref,
                                        custody_loader=lambda pin: (lambda spec: dict(CUST)), guard=B1G, canonical_producers=APPROVED)
            out[n] = {'same': canonical(strip(a_, drop)) == canonical(strip(b_, drop)), 'ok': [a_['ok'], b_['ok']]}
        return all(v['same'] for v in out.values()), out

    @case('A-D3_verify_row1_identical_to_c3v004', 'DIFFERENTIAL')
    def _():
        c1k = c1_doc(AW['reg'], C.canonical_pin('custody'), PRED['guard_b1'][1], 'c1kd')
        a_ = verify([row1], c1k)
        b_ = PRED_A.verify_registry(AW['reg'], [PRED_C.select_points('1')[0]], c1_ref=c1k,
                                    custody_loader=lambda pin: (lambda spec: dict(CUST)), guard=B1G, canonical_producers=APPROVED)
        drop = ('utc', 'generator')
        return a_['ok'] is True and canonical(strip(a_, drop)) == canonical(strip(b_, drop)), {'ok': [a_['ok'], b_['ok']]}

    # ============================================================================================ KS6 lo_core
    U = types.SimpleNamespace(KPC_M=KPC, _c0_D=lambda kept, outer, kp, kz: np.ones((len(kp), len(kz))))
    rng = np.random.default_rng(20261019)

    def tail(K, kept_K=None, edges_from=None):
        kp = np.linspace(0.5, 120.0, 40) / KPC
        kz = np.linspace(0.2, 100.0, 30) / KPC
        wkp, wz = np.full(40, 0.1 / KPC), np.full(30, 0.1 / KPC)
        Pm, Fm = rng.uniform(0.5, 1.5, (40, 5)), rng.uniform(0.5, 1.5, (30, 5))
        edges = np.arange(float(edges_from if edges_from is not None else K), 183.0)
        rec = {'empty': False, 'kept': {'shape': 'cube', 'K_inverse_kpc': float(kept_K if kept_K is not None else K)},
               'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0}, 'lambda_scale': 1.0, 'gamma_eff': 2.0, 'c_m_s': 299792458.0}
        rec['pref'] = rec['lambda_scale'] / (4 * rec['gamma_eff'] * (2 * math.pi) ** 3)
        out = np.zeros(len(edges) - 1)
        for st_ in range(0, 40, 64):
            sl = slice(st_, min(st_ + 64, 40))
            src = Pm[sl] @ Fm.T
            km = np.sqrt(kp[sl, None] ** 2 + kz[None, :] ** 2)
            fac = (rec['pref'] * wkp[sl] * kp[sl])[:, None] * wz[None, :] / km ** 2
            w = 2 * np.abs(src) * fac * 1.0 * km
            idx = np.clip(np.searchsorted(edges, km * KPC, side='right') - 1, 0, len(out) - 1)
            out += np.bincount(idx.ravel(), weights=w.ravel(), minlength=len(out))
        si = np.ones((len(edges) - 1, 3))
        si[:, 1] = out
        arr = {'kp': kp, 'kz': kz, 'wkp': wkp, 'wz': wz, 'P': Pm, 'F': Fm, 'shell_edges_inverse_kpc': edges, 'shell_integrals': si}
        return arr, rec

    def b1_out(fn):
        r = outcome(fn)
        return r[0], (None if r[1] is None else (r[1][0].tolist(), r[1][1]))

    @case('L-P1_K3_saved_state_accepted_with_kept_k_3', 'MUST_PASS')
    def _():
        arr, rec = tail(3)
        a_ = b1_out(lambda: L6.recompute_b1(arr, rec, U, kept_k=3.0))
        e = outcome(lambda: L6.validate_tail_arrays(arr, rec, 3.0))
        return a_[0] == 'PASS' and e[0] == 'PASS' and float(e[1][0]) == 3.0, {'recompute': a_[0], 'first_edge': float(e[1][0])}

    @case('L-F1_K3_state_refused_without_the_S1_kept_k_and_mixed_states_refused', 'MUST_FAIL')
    def _():
        arr3, rec3 = tail(3)
        arr_mix, rec_mix = tail(3, kept_K=3, edges_from=4)
        arr_mix2, rec_mix2 = tail(4, kept_K=4, edges_from=3)
        r = {'k3_default_k4': outcome(lambda: L6.validate_tail_arrays(arr3, rec3))[0],
             'kept3_edges4': outcome(lambda: L6.validate_tail_arrays(arr_mix, rec_mix, 3.0))[0],
             'kept4_edges3_as_k3': outcome(lambda: L6.validate_tail_arrays(arr_mix2, rec_mix2, 3.0))[0],
             'kept4_edges4_as_k3': outcome(lambda: L6.validate_tail_arrays(*tail(4), 3.0))[0]}
        ok = ('K4 cube required' in r['k3_default_k4'] and 'shell data shape/coverage' in r['kept3_edges4']
              and 'K3 cube required (S1_UA_C3T)' in r['kept4_edges3_as_k3'] and 'K3 cube required (S1_UA_C3T)' in r['kept4_edges4_as_k3'])
        return ok, r

    @case('L-D1_lo_core_record_functions_identical_to_12d36305_by_default', 'DIFFERENTIAL')
    def _():
        out, ok = {}, True
        variants = {'k4': tail(4), 'k3': tail(3), 'kept3_edges4': tail(3, kept_K=3, edges_from=4), 'kept4_edges3': tail(4, kept_K=4, edges_from=3)}
        for n, (arr, rec) in variants.items():
            a_, b_ = b1_out(lambda: L6.recompute_b1(arr, rec, U)), b1_out(lambda: PL6.recompute_b1(arr, rec, U))
            c_, d_ = outcome(lambda: L6.validate_tail_arrays(arr, rec)), outcome(lambda: PL6.validate_tail_arrays(arr, rec))
            same = a_ == b_ and c_[0] == d_[0]
            out[n] = [a_[0][:40], same]
            ok = ok and same
        sh = {'aggregate_shares': L6.aggregate_shares.__code__.co_code == PL6.aggregate_shares.__code__.co_code,
              'row_values': L6.row_values.__code__.co_code == PL6.row_values.__code__.co_code,
              'source_bound_J': L6.source_bound_J.__code__.co_code == PL6.source_bound_J.__code__.co_code}
        return ok and all(sh.values()), {'recompute/validate': out, 'same_bytecode': sh}

    @case('L-D2_lo_core_and_lo_config_non_S1_entry_points_are_the_predecessor_objects', 'DIFFERENTIAL')
    def _():
        names_core = ('produce_current_lo', 'produce_conditional_lo', 'saved_b1_diagnostic')
        saved = {n: getattr(PL6, n) for n in names_core}
        saved_cfg = {n: getattr(PF6, n) for n in ('validate_current_config', 'produce_current_lo')}
        for n in saved:
            setattr(PL6, n, (lambda n: lambda *a, **k: '12D36305_' + n)(n))
        for n in saved_cfg:
            setattr(PF6, n, (lambda n: lambda *a, **k: '6654D93C_' + n)(n))
        try:
            res = {}
            for nm, s in [('row01', BASE), ('row29', specs[29])] + [(k, v[0]) for k, v in battery.items() if k != 'S1_C3T']:
                res[nm] = [L6.produce_current_lo(s, None), L6.produce_conditional_lo(s, None), L6.saved_b1_diagnostic(s, None),
                           F6.validate_current_config(s, {}, {}, U), F6.produce_current_lo(s, None)]
            c3 = [outcome(lambda: L6.produce_conditional_lo(C3T, None))[0], outcome(lambda: L6.saved_b1_diagnostic(C3T, None))[0]]
        finally:
            for n, f in saved.items():
                setattr(PL6, n, f)
            for n, f in saved_cfg.items():
                setattr(PF6, n, f)
        ok = all(all(isinstance(x, str) and x[:9] in ('12D36305_', '6654D93C_') for x in v) for v in res.values()) and \
            all('not extended to S1_UA_C3T' in x for x in c3)
        return ok, {'n_specs': len(res), 'C3T_retired_paths': c3}

    @case('L-P2_lo_config_C3T_wants_the_K3_kept_region', 'MUST_PASS')
    def _():
        calls = []
        U2 = types.SimpleNamespace(
            KPC_M=KPC, TEST_ONLY_CERT='TEST_ONLY',
            kept_region=lambda stage, trunc, K: calls.append(K * KPC) or {'shape': 'cube', 'K_inverse_kpc': round(K * KPC, 9)},
            normalize_config=lambda raw: {'sha256': 'cfg', 'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0},
                                          'domain': {'R_eval_max_kpc': 14.2, 'z_eval_max_kpc': 35.0, 'z_src_max_kpc': 32.0},
                                          'jet_order': 2, 'quadrature': {'order': 8}},
            _grid=lambda kept, outer, quad, R: {'kp': np.arange(1.0, 5.0), 'kz': np.arange(1.0, 4.0), 'wkp': np.ones(4), 'wz': np.ones(3)})
        arrays = {'kp': np.arange(1.0, 5.0) / KPC, 'kz': np.arange(1.0, 4.0) / KPC, 'wkp': np.ones(4) / KPC, 'wz': np.ones(3) / KPC}

        def rec_for(K):
            return {'eps_certificate': 'PENDING_UV_TAIL_CERTIFICATE', 'lo_certificate': 'PENDING_UV_TAIL_CERTIFICATE', 'config_sha256': 'cfg',
                    'stage_kind': 'route_a', 'kept': {'shape': 'cube', 'K_inverse_kpc': float(K)},
                    'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0},
                    'domain_m': {'R_eval_max_m': 14.2 * KPC, 'z_eval_max_m': 35.0 * KPC, 'z_src_max_m': 32.0 * KPC},
                    'jet_order': 2, 'i1t': {'verdict': 'PASS'}, 'quadrature': {'order': 8, 'N_perp': 4, 'N_z_plus': 3}}
        a_ = outcome(lambda: F6.validate_current_config(C3T, rec_for(3), arrays, U2))
        k_seen = list(calls)
        b_ = outcome(lambda: F6.validate_current_config(C3T, rec_for(4), arrays, U2))
        c_ = outcome(lambda: PF6.validate_current_config(BASE, rec_for(4), arrays, U2))
        ok = (a_[0] == 'PASS' and a_[1]['exact_production_nodes_verified'] is True and abs(k_seen[0] - 3.0) < 1e-12
              and 'actual state kept/outer mismatch' in b_[0] and c_[0] == 'PASS')
        return ok, {'c3t_k3_record': a_[0], 'kept_K_asked': k_seen[:1], 'c3t_k4_record': b_[0][:60], 'k4_on_6654d93c': c_[0]}

    # ============================================================================================ KS6 adapter
    def rd_pin(ref):
        with open(ref['path'], 'rb') as f:
            raw = f.read()
        if sha_bytes(raw) != ref['sha256']:
            raise ValueError('byte pin mismatch')
        return raw

    IDS = ['R%02d' % i for i in range(12)]

    def adapter_world(spec0, K, tag, *, rho_K=None, rho_producer=None, core_shas=None, ident_spec=None):
        tag = FX.uniq(tag)
        call = os.path.realpath(os.path.dirname(FX.path(tag + '/call/x')))
        outd = os.path.join(call, 'out')
        os.makedirs(outd)
        passes = [{'rows': [{'id': i, 'speed_km_s': 10.0 + j + 0.5 * p} for j, i in enumerate(IDS)]} for p in range(2)]
        result = {'status': 'COMPLETED', 'valid': True, 'passes': passes, 'rows': passes[-1]['rows'], 'synthetic_fixture': SYN}
        rraw = json.dumps(result, sort_keys=True).encode()
        with open(os.path.join(outd, 'result.json'), 'xb') as f:
            f.write(rraw)
        result_pin = {'path': os.path.join(outd, 'result.json'), 'sha256': sha_bytes(rraw)}
        vmax = [max(abs(p_['rows'][j]['speed_km_s']) for p_ in passes) for j in range(12)]
        rdoc = rho_record(ident_spec or spec0, rho_K or K, rho_producer or KS2PIN, pins_k3())
        rs = FX.json(tag + '/RHO_SLOT.json', rdoc)
        es = FX.json(tag + '/EPS_SLOT.json', {'schema': 'SYNTHETIC_EPS_SLOT'})
        spec = copy.deepcopy(spec0)
        spec['numerics']['uv_tail']['eps_certificate'], spec['numerics']['uv_tail']['lo_certificate'] = es, rs
        ident = C.point_identity(spec)
        details = {'identity': ident, 'point_sha256': digest(ident), 'custody': dict(CUST), 'custody_sha256': digest(CUST),
                   'row_contract': {'rows': [{'id': i, 'radius_m': (1 + j) * KPC} for j, i in enumerate(IDS)], 'tau_km_s': [5.0] * 12}}
        sp = FX.json(tag + '/SLOT_PROOF.json', slot_proof_doc(spec, rs, rdoc, PLACE['SLOT_PRODUCER']))
        gp = FX.json(tag + '/GQ_PROOF.json', gq_record(spec, PLACE['GQ_PRODUCER']))
        bp = FX.json(tag + '/BUNDLE.json', {'schema': BUNDLE, 'identity': ident, 'custody': CUST,
                                           'driver_certificate_bindings': {'eps_certificate': es, 'lo_certificate': rs},
                                           'prelaunch': {'LO_RHO_SLOT': sp, 'GQ': gp}})
        s1 = {'state_sha256': 'a' * 64, 'source_sha256': 'b' * 64, 'stage_kind': 'route_a', 'nonnegative_masses': True}
        s2 = {'state_sha256': 'c' * 64, 'source_sha256': 'd' * 64, 'stage_kind': 'route_a', 'nonnegative_masses': True}
        inv = {'schema': AD6.INVENTORY_SCHEMA, 'complete': True,
               'producer': ({'path': AD6.ENUMERATOR_G6[0], 'sha256': AD6.ENUMERATOR_G6[1]} if C.s1_c3t_spec(spec0) else   # PORT (G-wave): S1 -> G6c
                            {'path': ART + '/s4_acceptance_c2/offset_b1/consumed_states_b1_c2v001.py', 'sha256': AD6.ENUMERATOR_SHA}),
               'point_sha256': details['point_sha256'], 'custody_sha256': details['custody_sha256'], 'states': [s1, s2],
               'occurrences': [{'ordinal': 0, 'role': 'boundary_at_return', 'stage': 'route_a', 'state_sha256_claimed': s1['state_sha256']},
                               {'ordinal': 1, 'role': 'next_built_and_monitor_consumed', 'stage': 'route_a'}],
               'joined_occurrences': [{'ordinal': 0, 'state': s1}, {'ordinal': 1, 'state': s2}]}
        inputs = {}
        for n, st in enumerate((s1, s2)):
            for kind in ('source', 'state'):
                with open(os.path.join(outd, '%s_%d.bin' % (kind, n)), 'xb') as f:
                    f.write(b'synthetic %s file %d\n' % (kind.encode(), n))
            src = FX.json(tag + '/SRC_%d.json' % n, {'schema': AD6.SOURCE_SCHEMA, 'source_files': [pin_file(os.path.join(outd, 'source_%d.bin' % n))]})
            row = FX.json(tag + '/ROWS_%d.json' % n, {'schema': AD6.ROWS_SCHEMA, 'state_sha256': st['state_sha256'], 'call_result': result_pin,
                                                    'speed_reference_policy': AD6.SPEED_POLICY, 'row_ids': IDS, 'v_reference_km_s': vmax,
                                                    'state_files': [pin_file(os.path.join(outd, 'state_%d.bin' % n))]})
            inputs[st['state_sha256']] = FX.json(tag + '/STATE_INPUT_%d.json' % n, {
                'schema': AD6.STATE_INPUT_SCHEMA, 'state': st, 'identity': ident, 'custody': CUST, 'call_result': result_pin,
                'execution': dict(AD6.EXECUTION_KEYS, run_root=outd), 'source_reconstruction': src, 'row_reference': row,
                'tail_state': {'record': {'path': '/synthetic', 'sha256': '0' * 64}, 'arrays': {'path': '/synthetic', 'sha256': '0' * 64}}})
        cshas = core_shas or (KSPIN['KS6CORE']['sha256'], KSPIN['KS2']['sha256'])

        def core(spec_, ref, expected_state=None, **kw):
            return {'schema': AD6.CORE_SCHEMA, 'gate': 'LO', 'kind': AD6.CORE_KIND, 'state': expected_state, 'identity': ident,
                    'custody': CUST, 'point_sha256': details['point_sha256'], 'producer': {'path': '/synthetic/core', 'sha256': cshas[0]},
                    'response_producer': {'path': '/synthetic/response', 'sha256': cshas[1]}, 'v_reference_km_s': vmax,
                    'rho': copy.deepcopy(rdoc), 'blockers': [], 'verdict': AD6.CORE_PASS_VERDICT, 'numerical_thresholds_pass': True,
                    'all_nonzero_B1_consumed': True, 'shells': [{'range_inverse_kpc': s_['range_inverse_kpc'], 'max_over_tau': 0.001}
                                                                for s_ in rdoc['shells']], 'summed_max_over_tau': 0.001 * len(rdoc['shells'])}
        lo_out = os.path.realpath(os.path.dirname(FX.path(tag + '/lo_out/x')))
        env = types.SimpleNamespace(derive_details=lambda s_: details, read_pin=lambda r: json.loads(rd_pin(r)), read_raw=rd_pin,
                                    read_bytes=lambda p: open(p, 'rb').read(), resolve=lambda p: os.path.realpath(p),
                                    point_context=lambda s_: {'synthetic': True}, produce_current_lo=core,
                                    validate_config=lambda s_, obj: {'certificate_slots_bound': True},
                                    write=lambda obj, root, name: AD6.common().write_new(os.path.join(root, name), obj, root),
                                    self_pin=AD6._self_pin, utc=AD6._utc)
        return dict(spec=spec, call=call, result=result, inv=inv, bundle=bp, inputs=inputs, env=env, lo_out=lo_out)

    def adapt(mod, w, env=None):
        return mod._adapt_call(w['spec'], call_dir=w['call'], result=w['result'], inventory=w['inv'], bundle_ref=w['bundle'],
                               state_inputs=w['inputs'], root_ruling_refs=list(AD6.ROOT_RULINGS),
                               approved_producer_sha256=[KSPIN['KS6AD']['sha256'], PAD._self_pin()['sha256'], PLACE['SLOT_PRODUCER']['sha256']],
                               trusted_source_producers=['e' * 64], trusted_row_policy_review_sha256=['f' * 64], out_root=w['lo_out'],
                               env=env or w['env'])

    @case('AD-P1_C3T_call_every_state_PASS_with_KS6_adapter_proofs', 'MUST_PASS')
    def _():
        w = adapter_world(C3T, 3, 'ad_ok')
        rec = adapt(AD6, w)
        proofs = [json.loads(rd_pin(s['record'])) for s in rec['states'] if s['verdict'] == 'PASS']
        ok = (rec['call_lo_reading'] == 'PASS' and len(proofs) == 2
              and all(p['producer'] == {'path': KSPIN['KS6AD']['path'], 'sha256': KSPIN['KS6AD']['sha256']} for p in proofs)
              and all(p['shells'][0]['range_inverse_kpc'] == [3.0, 4.0] for p in proofs))
        return ok, {'reading': rec['call_lo_reading'], 'blockers': rec['blockers'], 'states': [s['verdict'] for s in rec['states']]}

    @case('AD-F1_C3T_call_with_K4_slot_rho_or_a1dcdea8_rho_or_K4_core_refused', 'MUST_FAIL')
    def _():
        r1 = adapt(AD6, adapter_world(C3T, 3, 'ad_k4rho', rho_K=4, rho_producer=A1PIN))
        r2 = adapt(AD6, adapter_world(C3T, 3, 'ad_a1rho', rho_producer=A1PIN))
        r3 = adapt(AD6, adapter_world(C3T, 3, 'ad_k4core', core_shas=(PRED['lo_core'][1], PRED['response'][1])))
        ok = (r1['call_lo_reading'] == 'INCOMPLETE' and 'RHO_COVERAGE_NOT_3_TO_182' in str(r1['blockers'])
              and r2['call_lo_reading'] == 'INCOMPLETE' and 'RHO_PRODUCER_NOT_RESPONSE_KS2' in str(r2['blockers'])
              and r3['call_lo_reading'] == 'INCOMPLETE' and all('CORE_PRODUCER_NOT_KS6_LO_CORE_AND_KS2' in str(s['blockers']) for s in r3['states']))
        return ok, {'k4_rho': str(r1['blockers'])[:100], 'a1_rho': str(r2['blockers'])[:100], 'k4_core': str(r3['states'][0]['blockers'])[:100]}

    @case('AD-F2_K4_point_with_a_K3_slot_rho_refused', 'MUST_FAIL')
    def _():
        r = adapt(AD6, adapter_world(BASE, 4, 'ad_k4pt_k3rho', rho_K=3, rho_producer=KS2PIN))
        return r['call_lo_reading'] == 'INCOMPLETE' and 'RHO_COVERAGE_NOT_4_TO_182' in str(r['blockers']), str(r['blockers'])[:160]

    @case('AD-D1_K4_call_identical_to_211a3220', 'DIFFERENTIAL')
    def _():
        out = {}
        ok = True
        for n, kw in (('k4_a1_core', {'core_shas': (PRED['lo_core'][1], PRED['response'][1])}),
                      ('k4_ks_core', {'core_shas': (KSPIN['KS6CORE']['sha256'], KSPIN['KS2']['sha256'])}),
                      ('k4_point_k3_rho', {'core_shas': (PRED['lo_core'][1], PRED['response'][1]), 'rho_K': 3}),
                      ('k4_point_ks2_rho', {'core_shas': (PRED['lo_core'][1], PRED['response'][1]), 'rho_producer': KS2PIN})):
            kw = dict(kw)
            rp = kw.pop('rho_producer', A1PIN)
            wa = adapter_world(BASE, 4, 'ad_d_a_' + n, rho_producer=rp, **kw)
            wb = adapter_world(BASE, 4, 'ad_d_b_' + n, rho_producer=rp, **kw)
            fixed = lambda: {'path': '/synthetic/fixed_adapter_pin', 'sha256': PAD._self_pin()['sha256']}
            wa['env'].self_pin = wb['env'].self_pin = fixed
            ra, rb = adapt(AD6, wa), adapt(PAD, wb)
            ka = [(s['verdict'], s['reading'], [str(b)[:60] for b in s['blockers']]) for s in ra['states']]
            kb = [(s['verdict'], s['reading'], [str(b)[:60] for b in s['blockers']]) for s in rb['states']]
            same = ka == kb and ra['call_lo_reading'] == rb['call_lo_reading'] and [str(b)[:60] for b in ra['blockers']] == [str(b)[:60] for b in rb['blockers']]
            out[n] = {'same': same, 'reading': ra['call_lo_reading']}
            ok = ok and same
        ok = ok and out['k4_a1_core']['reading'] == 'PASS' and all(out[k]['reading'] == 'INCOMPLETE' for k in
                                                                   ('k4_ks_core', 'k4_point_k3_rho', 'k4_point_ks2_rho'))
        return ok, out

    @case('AD-D2_adapt_call_lo_and_check_rho_record_non_S1_are_211a3220s', 'DIFFERENTIAL')
    def _():
        pred = AD6._predecessor()
        saved = pred.adapt_call_lo
        pred.adapt_call_lo = lambda *a, **k: '211A3220_adapt_call_lo'
        try:
            res = {nm: AD6.adapt_call_lo(s, call_dir='/x', result={}, inventory={}, bundle_ref={}, state_inputs={}, out_root='/x')
                   for nm, s in [('row01', BASE)] + [(k, v[0]) for k, v in battery.items() if k != 'S1_C3T']}
            c3 = AD6.adapt_call_lo(C3T, call_dir='/x', result={}, inventory={}, bundle_ref={}, state_inputs={}, out_root='/x')
        finally:
            pred.adapt_call_lo = saved
        recs = {'k4_a1': rho_record(BASE, 4, A1PIN, ANCHOR_PINS), 'k4_ks2': rho_record(BASE, 4, KS2PIN, pins_k3()),
                'k3_on_k4_identity': rho_record(BASE, 3, KS2PIN, pins_k3())}
        rr = {n: [outcome(lambda: AD6.check_rho_record(r, read_raw=rd_pin))[0], outcome(lambda: PAD.check_rho_record(r, read_raw=rd_pin))[0]]
              for n, r in recs.items()}
        ok = (all(v == '211A3220_adapt_call_lo' for v in res.values()) and isinstance(c3, dict) and c3.get('call_lo_reading') == 'INCOMPLETE'
              and all(a_ == b_ for a_, b_ in rr.values()))
        return ok, {'delegated': len(res), 'c3t_entry': str(c3.get('blockers'))[:100], 'check_rho_record': rr}

    # ============================================================================================ KS6 handoff
    @case('H-P1_handoff_non_S1_is_5ff464cc_and_C3T_takes_the_KS6_adapter', 'MUST_PASS')
    def _():
        pred = H6._predecessor()
        saved = pred.accept_call
        pred.accept_call = lambda **k: ('5FF464CC_accept_call', None)
        try:
            res = {nm: H6.accept_call(call_dir='/x', spec=s, deps={}, policy={}, records_dir='/x')[0]
                   for nm, s in [('row01', BASE)] + [(k, v[0]) for k, v in battery.items() if k != 'S1_C3T']}
        finally:
            pred.accept_call = saved
        w = adapter_world(C3T, 3, 'ho_c3t')
        fn = H6.load_pinned(H6.LO_ADAPTER_KS6, 'kst_ho_ks6_adapter').adapt_call_lo
        receipt = FX.json('ho/RECEIPT_NOT_FINISHED.json', {'status': 'RUNNING'})
        rec, ref = H6.accept_call(call_dir=w['call'], spec=w['spec'], deps={'pins': {'lo_adapter': dict(H6.LO_ADAPTER_KS6)}, 'lo_adapter': fn},
                                  policy={'receipt': receipt}, records_dir=os.path.join(run, FX.uniq('ho_records')))
        ok = (all(v == '5FF464CC_accept_call' for v in res.values()) and rec['blockers'] == ['FINISHED_RECEIPT_REQUIRED']
              and rec['handoff'] == {'path': KSPIN['KS6HO']['path'], 'sha256': KSPIN['KS6HO']['sha256']})
        return ok, {'delegated': len(res), 'c3t_blockers': rec['blockers'], 'record': os.path.basename(ref['path'])}

    @case('H-F1_C3T_with_the_211a3220_adapter_and_bogus_adapter_pins_refused', 'MUST_FAIL')
    def _():
        w = adapter_world(C3T, 3, 'ho_c3t_old')
        fn = H6.load_pinned(H6.LO_ADAPTER, 'kst_ho_211a3220').adapt_call_lo
        rec, _ = H6.accept_call(call_dir=w['call'], spec=w['spec'], deps={'pins': {'lo_adapter': dict(H6.LO_ADAPTER)}, 'lo_adapter': fn},
                                policy={}, records_dir=os.path.join(run, FX.uniq('ho_records_old')))
        bogus = outcome(lambda: H6.load_deps({'lo_adapter': dict(H6.LO_ADAPTER_KS6, sha256='0' * 64)}))[0]
        prob = H6.lo_adapter_problem({'pins': {'lo_adapter': dict(H6.LO_ADAPTER_KS6)}, 'lo_adapter': fn}, H6.LO_ADAPTER_KS6)
        ok = ('LO_ADAPTER_PIN_NOT_A138 (required %s' % KSPIN['KS6AD']['path']) in str(rec['blockers']) and \
            'LO_ADAPTER_PIN_NOT_A138' in bogus and prob == 'LO_ADAPTER_CALLABLE_NOT_THE_PINNED_ENTRY'
        return ok, {'c3t_old_adapter': rec['blockers'], 'bogus_pin': bogus[:80], 'wrong_callable': prob}

    # ============================================================================================ GQ kernel finding
    @case('GQ-K1_GQ_production_kperp_nodes_depend_on_the_kept_K', 'FINDING')
    def _():
        mod_dir = os.path.dirname(PRED['uvt_lapse'][0])
        sys.path.insert(0, mod_dir)
        try:
            Ulib = load(PRED['uvt_lapse'][0], 'uvt_lapse', PRED['uvt_lapse'][1])
        finally:
            sys.path.remove(mod_dir)
        uv = BASE['numerics']['uv_tail']
        nodes = {}
        for K in (4, 3):
            kept = Ulib.kept_region('route_a', None, K / Ulib.KPC_M)
            nodes[K] = np.asarray(Ulib._grid(kept, uv['outer'], uv['quadrature'], uv['domain']['R_eval_max_kpc'])['kp'])
        s4, s3 = set(np.round(nodes[4], 12)), set(np.round(nodes[3], 12))
        det = {'N_kp_K4': int(len(nodes[4])), 'N_kp_K3': int(len(nodes[3])), 'K3_nodes_absent_at_K4': len(s3 - s4),
               'K4_nodes_absent_at_K3': len(s4 - s3), 'shared': len(s3 & s4),
               'source': 'gq_geometry_r5_cx2v001 c6ffb338 L39-40: kept_region(route_a, None, 4/KPC_M) then _grid(...)[kp]'}
        return len(s3 - s4) > 0, det

    # ============================================================================================ summary
    n = len(RESULTS)
    np_ = sum(r['passed'] for r in RESULTS)
    kinds = {}
    for r in RESULTS:
        k = kinds.setdefault(r['kind'], {'n': 0, 'passed': 0})
        k['n'] += 1
        k['passed'] += r['passed']
    summary = {'schema': 'KS_K3_CHAIN_TEST_RESULTS_C2V001', 'ks_dir': KS, 'run_dir': run, 'n': n, 'passed': np_, 'by_kind': kinds,
               'failed': [r['id'] for r in RESULTS if not r['passed']], 'fence_refused_opens': FENCE['refused'],
               'modules': KSPIN, 'predecessors': {k: {'path': p, 'sha256': h} for k, (p, h) in PRED.items()},
               'suite': pin_file(os.path.realpath(__file__)), 'python': sys.version.split()[0],
               'flags': {'isolated': sys.flags.isolated, 'dont_write_bytecode': sys.flags.dont_write_bytecode},
               'background_qos': os.getpriority(4, 0) == 1, 'seconds': round(time.time() - t0, 1), 'results': RESULTS,
               'synthetic_fixture': SYN}
    with open(os.path.join(run, 'TEST_RESULTS_KS_PORT_GWAVE_C2V001.json'), 'xb') as f:   # PORT (G-wave)
        f.write(json.dumps(summary, sort_keys=True, indent=1, default=str).encode() + b'\n')
    print(json.dumps({'n': n, 'passed': np_, 'by_kind': kinds, 'failed': summary['failed'], 'seconds': summary['seconds']}))
    return 0 if np_ == n else 1


if __name__ == '__main__':
    sys.exit(main())
