"""G-wave synthetic tests (ks_k3_chain_c2 G-wave c2v001; root A175, A176): MUST_PASS, MUST_FAIL, DIFFERENTIAL,
EQUIVALENCE and DECIDING cases for G1, G2, G3, G4, G6 and KS3', KS4', KS5'', KS6'.

  taskpolicy -b PY -I -B test_gwave_c2v001.py --gw-dir DIR --run-dir DIR/synthetic/<new>

SYNTHETIC inputs only; nothing is launched; no run tree, UVT_*, C5H or NGC3198 path is opened, and no CP-1 out-root
(cp1_run_c3v004*) either (audit-hook fence below). Real files READ: the G-wave successors (--gw-dir), the wave-1
successors and every predecessor (import, by path and sha), the CB case block 76309ae3, the 31 CP-1 dry-plan specs
(bytes, point keys, identity fields), the library 2026f2b6 with its roster 4366e3d6 and jn provider d6c55b55 (the GQ and
TailState computations run for real, on synthetic geometry), r14 f3f9ba7e (the SRB adapter's own apply_flag extraction),
the A134 ruling files the proof-side root gates re-read, and the 0528/b1 ruling files the GQ policies read.
Custody is never derived from real inputs: every custody module instance a case touches gets the same synthetic seams
(libraries, point_geometry, the coefficient file and the prereg pin), so derive_details' own logic runs on synthetic
geometry (wave-1's seam, plus a GQ profile and the real uvt modules). EPS/rho numerics are schema-valid synthetic doubles
inside the real KS2 produce_eps/produce_rho. Every write is exclusive create under --run-dir.
Results: <run-dir>/TEST_RESULTS_GWAVE_C2V001.json.
"""
import os
for _k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS',
           'BLIS_NUM_THREADS'):
    os.environ[_k] = '1'
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import math
import sys
import time
import traceback
import types
from pathlib import Path

import numpy as np

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
KS = ART + '/ks_k3_chain_c2'
CERT = ART + '/calib_tail_readiness_cx2/certificates_per_point'
B1 = ART + '/s4_acceptance_c2/offset_b1'
PS = ART + '/s4rc1_c3/proof_side_c3v003'
MODDIR = ART + '/tail_scheme_impl_c2/driver_r5/module'
CB_PATH = ART + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json'
CB_SHA = '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'
C3T_LABEL = 'S1 transfer test C3T at u_A theta 0123456789abcdef; base 89abcdef'
C4T_LABEL = 'S1 transfer test C4T at u_A theta 0123456789abcdef; base 89abcdef'
KPC = 3.0856775814913673e19
SYN = 'ks_k3_chain_c2 G-wave c2v001 synthetic test fixture; not a measurement, not a review, not a ruling'
GW_NAMES = {
    'G3A': 'gq_geometry_r5_cx2v001_g3_c2v001.py', 'G3B': 'gq_producer_cx2v005_g3_c2v001.py',
    'G3C': 'gq_producer_b1_c2v001_g3_c2v001.py', 'G4': 'point_response_admission_adapter_cx2v003_g4_c2v001.py',
    'G1': 'lo_slot_proof_c3v003_g1_c2v001.py', 'G6A': 'execution_graph_cx2v002_g6_c2v001.py',
    'G6B': 'current_source_evidence_b1_c2v001_g6_c2v001.py', 'G6C': 'consumed_states_b1_c2v001_g6_c2v001.py',
    'G2': 'srb_rot_adapter_c3v003_g2_c2v001.py', 'KS5PP': 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003.py',
    'KS3C2': 's4rc1_common_c3v004_ks3_c2v002.py', 'KS3R2': 'cp1_runner_c3v004_ks3_c2v002.py',
    'KS42': 'registry_assembler_c3v004_ks4_c2v002.py', 'KS6AD2': 'lo_state_proof_adapter_c3v003_ks6_c2v002.py',
    'KS6HO2': 'acceptance_handoff_c2v004_ks6_c2v002.py'}
KS_NAMES = {
    'KS1': ('custody_cx2v002_ks1_c2v001.py', 'ad020470aee354201ab6c68926784d75d3ebe2e16628323d49280bd2eb18aea6'),
    'KS2': ('point_response_producer_cx2v002_ks2_c2v001.py', '99c29df639482032114f84420a309d29017cfca7fe01a8412be2757fbff75dd7'),
    'KS3C': ('s4rc1_common_c3v004_ks3_c2v001.py', '736d2e7e26c6e6f6325796ea83774682a82f2a045a5f6e3f0ae13358725b1656'),
    'KS3R': ('cp1_runner_c3v004_ks3_c2v001.py', '54595c2d68e63e82378e5ca29f7aa48a19fe6c919f8c8775d2ff4d47fbc41730'),
    'KS4': ('registry_assembler_c3v004_ks4_c2v001.py', '080ed1718908948cb1cfac96a7505a19b2e1741e8742055858cc9037ebbf8cad'),
    'KS5': ('certificate_guard_b1_ks5_c2v001.py', 'e394ae94c6f48ff9e0919e9b186103d2f7c5b00077967579029e8404a62215d6'),
    'KS5P': ('calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v002.py', '66560a6a8335d36eff8b4ec58ef780445dc8c6fa21088712e334311bd6fce1eb'),
    'KS6CORE': ('lo_core_r5_cx2v001_ks6_c2v001.py', '2cf7c59790638cc1595a615b226143a5a3eb74e713001d85db4d469edf0b2b2f'),
    'KS6CFG': ('lo_config_r5_cx2v001_ks6_c2v001.py', '510ff07b9557c3829063fe25fe127dc0477a0bfdace5627d84f61aba8b256a2b'),
    'KS6AD': ('lo_state_proof_adapter_c3v003_ks6_c2v001.py', '8fa371a719b41c174175942308ca64bebe40fb1e0d42b99ae27def939cbe6c33'),
    'KS6HO': ('acceptance_handoff_c2v004_ks6_c2v001.py', '6642d2090d7f0801c1eeb68fcb2c6304616030370cdc15047719f653718d4132')}
PRED = {
    'G3A': (CERT + '/gq_geometry_r5_cx2v001.py', 'c6ffb338fd7e87bca0028afcf8c1b6c0ae52b8d89823bdcaded69ce798305d85'),
    'G3B': (CERT + '/gq_producer_cx2v005.py', '2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd'),
    'G3C': (B1 + '/gq_producer_b1_c2v001.py', '3e668a2b04288ce4ff4f95b582412ceb4aecf2c908516b97e84f4b1d6d42c3c5'),
    'G4': (CERT + '/point_response_admission_adapter_cx2v003.py', '4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372'),
    'G1': (PS + '/lo_slot_proof_c3v003.py', 'cd10cd59df44d7b79f3c3aa7ba88998d94c7292c4c2656e09bbbe16ded01bca3'),
    'G6A': (CERT + '/execution_graph_cx2v002.py', '6d59f1d06e7c69e15e8d9766fa1776da2b0603d16febf4406c96157d77019258'),
    'G6B': (B1 + '/current_source_evidence_b1_c2v001.py', '7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce'),
    'G6C': (B1 + '/consumed_states_b1_c2v001.py', '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0'),
    'G2': (PS + '/srb_rot_adapter_c3v003.py', '08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a'),
    'custody': (CERT + '/custody_cx2v002.py', '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377'),
    'response': (CERT + '/point_response_producer_cx2v002.py', 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'),
    'guard_b1': (B1 + '/certificate_guard_b1_c2v001.py', '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'),
    'lo_config': (CERT + '/lo_config_r5_cx2v001.py', '6654d93c0241afd230d90bfcf327f16c22dd24c4da1d3eea72602212c2b6ae5a'),
    'lo_producer_v004': (CERT + '/lo_producer_cx2v004.py', '5db60d0f6db6d481e2f748b19bef08ce425f19a0e463d58727c184d633e03d51'),
    'base_381b': (CERT + '/point_response_admission_base_r5_cx2v001.py', '381b3eaa6ba8a56c2ca4c89f88c6e5e333d7152b52c5386892b19d0a8f50d4e6'),
    'q5b1': (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py', '7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d'),
    'adapter_211a': (PS + '/lo_state_proof_adapter_c3v003.py', '211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c'),
    'handoff_5ff4': (ART + '/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py', '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'),
    'reconstruction': (CERT + '/reconstruction_cx2v003.py', 'b8471197027bd2f0511966713656893860dfb22cba18e8d799ed2cc89b7c3a50'),
    'consumed_D': (CERT + '/consumed_states_cx2v005.py', '7b7400f331970a5f5fb7f7104f5e1850a765fcd04fc993100b5d1f0f37f4d653'),
}
LIBS = {'U': (MODDIR + '/owned_uv_tail_lapse_v002.py', '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'),
        'RS': (MODDIR + '/uv_tail_source_roster_c2v001.py', '4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2'),
        'PV': (MODDIR + '/posix_libm_bessel_jn_provider_c2v001.py', 'd6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171')}
PROOF = 'UNT_CALIBRATION_POINT_PROOF_CX2V001'
BUNDLE = 'UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001'
ENV_RULE = 'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS'
ACC_RULE = 'ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED'
SLOT_RULE = 'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE'
HANDOFF_RULE = 'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'
CUSTODY_KEYS = ('grid_sha256', 'background_sha256', 'geometry_sha256', 'modules_sha256', 'row_contract_sha256')
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
            or any(s.startswith('cp1_run_c3v004') for s in parts) or '.codex' in parts or 'c5h_hull_c2' in parts
            or any(s.startswith('uvt_') or 'ngc3198' in s for s in parts) or p.startswith('/Volumes/External1')):
        FENCE['refused'].append(p)
        raise PermissionError('GWAVE_TEST_FENCE_FORBIDDEN_PATH ' + p)


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


def load(path, name, sha=None, text=None):
    with open(path, 'rb') as f:
        raw = f.read()
    if sha is not None and sha_bytes(raw) != sha:
        raise SystemExit('PIN MISMATCH ' + path)
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    exec(compile(raw if text is None else text, str(path), 'exec'), m.__dict__)
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
        t = time.time()
        try:
            ok, det = fn()
        except Exception as exc:
            ok, det = False, 'EXCEPTION %s: %s | %s' % (type(exc).__name__, exc, traceback.format_exc(limit=8)[-2500:])
        record(tid, kind, ok, det)
        print('%-6s %-11s %6.1fs %s' % ('ok' if ok else 'FAIL', kind, time.time() - t, tid), flush=True)
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

    def dir(self, rel):
        d = os.path.realpath(os.path.dirname(self.path(rel + '/x')))
        os.makedirs(d, exist_ok=True)
        return d


def cb_grid(case_):
    with open(CB_PATH, 'rb') as f:
        raw = f.read()
    assert sha_bytes(raw) == CB_SHA
    return copy.deepcopy(json.loads(raw)['cases'][case_]['normalized_spec_equal']['/numerics']['composite_grid_spec'])


def grid_k(k):
    """s1k3 c2v001 test L120-133 (wave-1 grid_k): a synthetic grid with last break k."""
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


def partition(K):
    edges = [K] + [e for e in (4, 5, 6, 8, 12, 16, 32, 64) if e > K] + [128, 182]
    return [[float(a), float(b)] for a, b in zip(edges[:-1], edges[1:])]


def fib_sphere(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    th = math.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], axis=1)


def strip(obj, keys):
    return {k: v for k, v in obj.items() if k not in keys} if isinstance(obj, dict) else obj


def fn_node(path, name):
    with open(path) as f:
        tree = ast.parse(f.read())
    hits = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    assert len(hits) == 1, (path, name)
    return hits[0]


def independent_kp_nodes(K, K_big, order, w_perp, R_eval_max):
    """Re-implemented here from the library's documented grid definition (owned_uv_tail_lapse_v002 module docstring
    'Quadrature' and _alpha docstring L150-155), not by calling it. A cube kept region of edge K inside the cylinder
    K_big: breaks B = {0, K, sqrt2 K, K_big}; tensor Gauss-Legendre of `order` on uniform panels of width <= w_perp on
    every interval, except the interval starting at the cube corner K, which is integrated in a = arccos(K/k) on panels
    marched from a = 0 by a_next = min(a + 1.5/(sqrt2 K R_eval_max + 40), arccos(K/(K/cos a + w_perp)), arccos(K/b))."""
    x, _ = np.polynomial.legendre.leggauss(order)
    B = sorted(b for b in {0.0, float(K), math.sqrt(2) * K, float(K_big)} if b <= K_big * (1 + 1e-15))
    out = []
    for a, b in zip(B[:-1], B[1:]):
        if abs(a - K) <= 1e-12 * K:
            A = math.acos(min(1.0, K / b))
            dah = 1.5 / (math.sqrt(2) * K * R_eval_max + 40.0)
            e, al = [0.0], 0.0
            while al < A * (1 - 1e-15):
                k = K / math.cos(al)
                al = min(al + dah, math.acos(min(1.0, K / (k + w_perp))), A)
                e.append(al)
            e = np.array(e)
            alpha = np.concatenate([(lo + hi) / 2 + (hi - lo) * x / 2 for lo, hi in zip(e[:-1], e[1:])])
            out.append(K / np.cos(alpha))
        else:
            n = max(1, int(math.ceil((b - a) / w_perp - 1e-12)))
            e = np.linspace(a, b, n + 1)
            out.append(np.concatenate([(lo + hi) / 2 + (hi - lo) * x / 2 for lo, hi in zip(e[:-1], e[1:])]))
    return np.concatenate(out)


class SyntheticRoster:
    """Two smooth synthetic source terms (not a galaxy). kind 'synthetic' (I1-T NOT_APPLICABLE_SYNTHETIC)."""
    kind = 'synthetic'
    gas = None
    stars = None

    def __init__(self, amp):
        self.R = np.array([0.05, 0.15]) * KPC
        self.h = np.array([0.02, 0.04]) * KPC
        self.amp = np.array([1.0, 0.5]) * amp

    def extent(self):
        return {'R_src_max_m': float(self.R.max()), 'gas_z_abs_max_m': float(self.h.max()), 'stars_24h_m': 0.0}

    def radial_factors(self, kp, j0):
        return np.stack([a * j0(np.asarray(kp) * r) for a, r in zip(self.amp, self.R)], axis=1)

    def vertical_factors(self, kz, c_m_s):
        return np.stack([np.exp(-(np.asarray(kz) * h) ** 2) + 0j for h in self.h], axis=1)

    def record(self):
        return {'kind': 'synthetic', 'R_m': self.R.tolist(), 'h_m': self.h.tolist(), 'amp': self.amp.tolist()}

    def digest(self):
        return sha_bytes(json.dumps(self.record(), sort_keys=True).encode())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gw-dir', required=True)
    ap.add_argument('--run-dir', required=True)
    a = ap.parse_args()
    GW = os.path.realpath(a.gw_dir)
    run = os.path.abspath(a.run_dir)
    if not (run.startswith(KS + '/synthetic/') or run.startswith(KS + '/dev/')):
        raise SystemExit('REFUSED: --run-dir must be a new folder under ks_k3_chain_c2/synthetic/ (or dev/)')
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1):
        raise SystemExit('REFUSED: python3 -I -B required')
    os.makedirs(os.path.dirname(run), exist_ok=True)
    os.mkdir(run)
    FX = Fixtures(run)
    t0 = time.time()
    # ------------------------------------------------------------------------------------------ modules
    GPIN = {k: pin_file(os.path.join(GW, n)) for k, n in GW_NAMES.items()}
    KPIN = {k: {'path': os.path.join(KS, n), 'sha256': h} for k, (n, h) in KS_NAMES.items()}
    assert all(sha_file(p['path']) == p['sha256'] for p in KPIN.values()), 'wave-1 successor bytes changed'
    assert all(sha_file(p) == h for p, h in PRED.values()), 'predecessor bytes changed'
    U = load(LIBS['U'][0], 'gwt_uvt_lapse', LIBS['U'][1])
    RS = load(LIBS['RS'][0], 'gwt_uvt_roster', LIBS['RS'][1])
    PV = load(LIBS['PV'][0], 'gwt_uvt_jn', LIBS['PV'][1])
    M = {k: load(GPIN[k]['path'], 'gwt_' + k.lower(), GPIN[k]['sha256']) for k in GW_NAMES}
    G3A, G3B, G3C, G4, G1, G6A, G6B, G6C, G2 = (M[k] for k in ('G3A', 'G3B', 'G3C', 'G4', 'G1', 'G6A', 'G6B', 'G6C', 'G2'))
    S5, R3, A4, AD6, H6 = M['KS5PP'], M['KS3R2'], M['KS42'], M['KS6AD2'], M['KS6HO2']
    C = R3.C                                            # the runner's own KS3' common
    W = {k: load(KPIN[k]['path'], 'gwt_w1_' + k.lower(), KPIN[k]['sha256']) for k in KS_NAMES}
    KS1, KS2, KS5 = W['KS1'], W['KS2'], W['KS5']
    P = {k: load(PRED[k][0], 'gwt_pred_' + k.lower(), PRED[k][1]) for k in ('G3A', 'G3B', 'G3C', 'G4', 'G1', 'G6A', 'G6B',
                                                                               'G6C', 'G2', 'guard_b1')}
    rows = C.point_rows()
    specs = {}
    for r in rows:
        with open(r['spec_path'], 'rb') as f:
            specs[r['row']] = json.loads(f.read())
    BASE = specs[1]
    C3T = spec_with(BASE, C3T_LABEL, cb_grid('C3T'))
    K4_ID = C.point_identity(BASE)

    # ------------------------------------------------------------------------------------------ custody seams
    npz = FX.path('custody/coefficients_synthetic.npz')
    with open(npz, 'xb') as f:
        np.savez(f, source_hessian_grid=np.arange(12.).reshape(3, 4), background_C=np.eye(3), background_mu=np.ones(3))
    coeff_path = BASE['coefficients']['path']
    rows_c = [{'id': 'R%02d' % i, 'radius_m': (0.5 + 0.7 * i) * KPC} for i in range(12)]
    prereg = {'row_ids': [r['id'] for r in rows_c], 'tau_km_s': [3.0 + 0.25 * i for i in range(12)]}
    PREREG = {'path': '/synthetic/prereg_v005', 'sha256': '0' * 64}
    EDGES = (np.linspace(0.0, 8.0, 7) ** 2).tolist()      # 6 synthetic annuli (s in kpc^2): 24 GL4 columns

    def stub_custody(mod):
        """Wave-1 seam (test_ks_k3_chain_c2v001 stub_custody) plus a GQ profile and the real uvt modules: derive_details'
        own logic runs on synthetic geometry; the coefficient file and the prereg pin are synthetic."""
        if getattr(mod, '_gwt_stubbed', False):
            return mod
        real_sha, real_allowed, real_read = mod.sha, mod.allowed_path, mod.read_pin

        class D:
            GEOMETRY_PINS = {}
            uvt_static_pins = staticmethod(lambda flag: {})

        class CCs:
            pin = staticmethod(lambda name: dict(PREREG))
            uvt_modules = staticmethod(lambda: (U, RS, PV))
        mod.libraries = lambda: (D, CCs)
        mod.point_geometry = lambda spec, d=None: (
            {'galaxies': {'DDO154': {'HI_plus_He': {'s_edges_kpc2': list(EDGES)}, 'synthetic_distance_Mpc': spec['physical']['distance_Mpc']}}},
            {'monotone': 'synthetic'}, {'query_rows': copy.deepcopy(rows_c)}, {'derivation': 'synthetic'})
        mod.read_pin = lambda ref, document=True: copy.deepcopy(prereg) if ref == PREREG else real_read(ref, document)
        mod.sha = lambda p: mod.A2_SHA if str(p) == coeff_path else real_sha(p)
        mod.allowed_path = lambda p: Path(npz) if str(p) == coeff_path else real_allowed(p)
        mod._gwt_stubbed = True
        if isinstance(getattr(mod, 'P', None), types.ModuleType) and hasattr(mod.P, 'derive_details'):
            stub_custody(mod.P)                          # KS1's predecessor object (6810b7c3) takes the same seams
        return mod
    for cu in (KS1, KS2.CU, G3A.C, G3A.P.C, G3B.C, G3B.PRED.C, G3C.C, G3C.PRED.C, G4.CU, G4.P.CU, G6A.C, G6A.PRED.C,
               G6B.C, G6B.PRED.C, G6C.C, P['G3A'].C, P['G3B'].C, P['G3C'].C, P['G4'].CU, P['G6A'].C, P['G6B'].C,
               P['G6C'].C):
        stub_custody(cu)
    DET = G3A.C.derive_details(spec=C3T)                 # the S1_UA_C3T details every seam returns (KS1's own logic)
    CUST = DET['custody']
    C3T_ID = DET['identity']

    def details_of(spec):
        return G3A.C.derive_details(spec=spec)

    # ------------------------------------------------------------------------------------------ identity battery
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
    NON_S1 = [(k, v[0]) for k, v in battery.items() if k != 'S1_C3T']

    # ============================================================================================ X: pins
    @case('X-P1_gwave_pins_consistent_from_bytes', 'MUST_PASS')
    def _():
        p = lambda m, attr: [str(x) for x in getattr(m, attr)]
        got = {
            'G3A.custody=KS1': str(G3A.CP) == KPIN['KS1']['path'] and G3A.CS == KPIN['KS1']['sha256'],
            'G3A.PREDECESSOR=c6ffb338': p(G3A, 'PREDECESSOR') == list(PRED['G3A']),
            'G3B.kernel=G3A': str(G3B.P) == GPIN['G3A']['path'] and G3B.S == GPIN['G3A']['sha256'],
            'G3B.PREDECESSOR=2832ceb9': p(G3B, 'PREDECESSOR') == list(PRED['G3B']),
            'G3C.kernel=G3A': str(G3C.P) == GPIN['G3A']['path'] and G3C.S == GPIN['G3A']['sha256'],
            'G3C.PREDECESSOR=3e668a2b': p(G3C, 'PREDECESSOR') == list(PRED['G3C']),
            'G4.response=KS2': str(G4.RESPONSE_PATH) == KPIN['KS2']['path'] and G4.RESPONSE_SHA == KPIN['KS2']['sha256'],
            'G4.PREDECESSOR=4de70486': str(G4.PREDECESSOR) == PRED['G4'][0] and G4.PREDECESSOR_SHA == PRED['G4'][1],
            'G4.CU=KS1': G4.CU.__file__ == KPIN['KS1']['path'],
            'G1.pins': (list(G1.CUSTODY_KS1) == [KPIN['KS1']['path'], KPIN['KS1']['sha256']] and G1.RESPONSE_KS2_SHA == KPIN['KS2']['sha256']
                        and list(G1.PREDECESSOR) == list(PRED['G1'])),
            'G6A.custody=KS1': str(G6A.P) == KPIN['KS1']['path'] and G6A.SHA == KPIN['KS1']['sha256'] and p(G6A, 'PREDECESSOR') == list(PRED['G6A']),
            'G6B.PINS': (list(G6B.PINS['L']) == [KPIN['KS6CFG']['path'], KPIN['KS6CFG']['sha256']]
                         and list(G6B.PINS['G']) == [GPIN['G3C']['path'], GPIN['G3C']['sha256']]
                         and list(G6B.PINS['R']) == list(PRED['reconstruction']) and p(G6B, 'PREDECESSOR') == list(PRED['G6B'])),
            'G6B.C=KS1': G6B.C.__file__ == KPIN['KS1']['path'],
            'G6C.PINS': (list(G6C.PINS['A']) == [GPIN['G6B']['path'], GPIN['G6B']['sha256']]
                         and list(G6C.PINS['X']) == [GPIN['G6A']['path'], GPIN['G6A']['sha256']]
                         and list(G6C.PINS['D']) == list(PRED['consumed_D']) and p(G6C, 'PREDECESSOR') == list(PRED['G6C'])),
            'G6C.C=KS1(via A)': G6C.C.__file__ == KPIN['KS1']['path'] and G6C.C is G6C.A.C,
            'G2.pins': (list(G2.CUSTODY_KS1) == [KPIN['KS1']['path'], KPIN['KS1']['sha256']]
                        and list(G2.ENUMERATOR_G6) == [GPIN['G6C']['path'], GPIN['G6C']['sha256']]
                        and G2.ENUMERATOR_SHA == PRED['G6C'][1] and list(G2.PREDECESSOR) == list(PRED['G2'])),
            'KS6AD2.ENUMERATOR_G6': list(AD6.ENUMERATOR_G6) == [GPIN['G6C']['path'], GPIN['G6C']['sha256']] and AD6.ENUMERATOR_SHA == PRED['G6C'][1],
            'KS6HO2.pins': (H6.LO_ADAPTER_KS6 == dict(GPIN['KS6AD2'], entry='adapt_call_lo')
                            and H6.B1_EVIDENCE_G6 == GPIN['G6B'] and H6.B1_EVIDENCE['sha256'] == PRED['G6B'][1]),
            'KS3C2.PINS': all(list(C.PINS[k]) == [GPIN[g]['path'], GPIN[g]['sha256']] for k, g in
                              (('gq_producer_g3', 'G3B'), ('gq_geometry_g3', 'G3A'), ('eps_adapter_g4', 'G4'),
                               ('lo_slot_proof_g1', 'G1'), ('state_enumerator_g6', 'G6C'), ('wrapper_s1k3_ks5pp', 'KS5PP'))),
            'KS3C2.wave1_pins_kept': all(list(C.PINS[k]) == [KPIN[w]['path'], KPIN[w]['sha256']] for k, w in
                                         (('custody_ks1', 'KS1'), ('response_producer_ks2', 'KS2'), ('guard_ks5', 'KS5'),
                                          ('wrapper_s1k3_ks5p', 'KS5P'))),
            'KS3C2.rows_1_31_pins_unchanged': all(C.PINS[k] == W['KS3C'].PINS[k] for k in W['KS3C'].PINS),
            'KS3C2.canonical_S1': C.CANONICAL_APPROVED_PRODUCERS_S1 == ('eps_adapter_g4', 'gq_producer_g3', 'lo_slot_proof_g1')
                                  and C.CANONICAL_APPROVED_PRODUCERS == W['KS3C'].CANONICAL_APPROVED_PRODUCERS,
            'KS3R2.COMMON': R3.COMMON_SHA == GPIN['KS3C2']['sha256'] and R3.COMMON_PATH == GPIN['KS3C2']['path'],
            'KS42.COMMON': A4.COMMON_SHA == GPIN['KS3C2']['sha256'] and A4.COMMON_PATH == GPIN['KS3C2']['path'],
            'KS5PP.pins': list(S5.GUARD_KS5) == [KPIN['KS5']['path'], KPIN['KS5']['sha256']] and S5.RESPONSE_KS2 == {'path': KPIN['KS2']['path'], 'sha256': KPIN['KS2']['sha256']},
            'predecessors_unchanged': all(sha_file(p_) == h for p_, h in PRED.values()),
            'wave1_successors_unchanged': all(sha_file(v['path']) == v['sha256'] for v in KPIN.values()),
        }
        return all(got.values()), got

    @case('X-P2_predecessor_objects_are_the_pinned_predecessors', 'MUST_PASS')
    def _():
        got = {'G3A.P': G3A.P.__file__ == PRED['G3A'][0], 'G3B.PRED': G3B.PRED.__file__ == PRED['G3B'][0],
               'G3C.PRED': G3C.PRED.__file__ == PRED['G3C'][0], 'G4.P': G4.P.__file__ == PRED['G4'][0],
               'G1.pred': G1._predecessor().__file__ == PRED['G1'][0], 'G6A.PRED': G6A.PRED.__file__ == PRED['G6A'][0],
               'G6B.PRED': G6B.PRED.__file__ == PRED['G6B'][0], 'G6C.PRED': G6C.PRED.__file__ == PRED['G6C'][0],
               'G2.pred': G2._predecessor().__file__ == PRED['G2'][0],
               'pred_custodies_6810b7c3': all(m.__file__ == PRED['custody'][0] for m in (G3A.P.C, G3B.PRED.C, G3C.PRED.C, G4.P.CU, G6A.PRED.C, G6B.PRED.C, G6C.PRED.C)),
               'G6B.L_is_KS6_lo_config': G6B.L.__file__ == KPIN['KS6CFG']['path'] and G6B.L.PR.__file__ == KPIN['KS2']['path'],
               'G6B.G_is_G3C': G6B.G.__file__ == GPIN['G3C']['path'],
               'G6C.A_X': G6C.A.__file__ == GPIN['G6B']['path'] and G6C.X.__file__ == GPIN['G6A']['path']}
        return all(got.values()), got

    # ============================================================================================ G: identity gates
    def spec_gates(s):
        return {'G3A.C(KS1)': G3A.C.s1_c3t_spec(s), 'G4.CU(KS1)': G4.CU.s1_c3t_spec(s), 'G1': G1._s1_c3t_spec(s),
                'G2': G2._s1_c3t_spec(s), 'G6A.C': G6A.C.s1_c3t_spec(s), 'G6B.C': G6B.C.s1_c3t_spec(s),
                'G6C.C': G6C.C.s1_c3t_spec(s), 'KS3C2': C.s1_c3t_spec(s),
                'KS5PP': S5.s1_c3t_identified(s) and outcome(lambda: S5.validate_s1_c3t_block(copy.deepcopy(s['numerics'])))[0] == 'PASS',
                'KS6AD2': AD6._s1_c3t_spec(s), 'KS6HO2': H6._s1_c3t_spec(s)}

    def ident_gates(s):
        ident = C.point_identity(s)
        return {'G1._rho_contract==3': G1._rho_contract(ident)[3] == 3, 'G2._s1_identity': G2._s1_identity({'identity': ident}),
                'KS6AD2._s1_c3t_numerics': AD6._s1_c3t_numerics(ident['numerics']), 'KS5.kept_k==3': KS5.kept_k(ident) == 3.0}

    @case('G-P1_S1_UA_C3T_admitted_by_every_G_wave_gate', 'MUST_PASS')
    def _():
        s = battery['S1_C3T'][0]
        sg, ig = spec_gates(s), ident_gates(s)
        return all(sg.values()) and all(ig.values()), {'spec': sg, 'identity': ig}

    @case('G-F1_every_other_spec_refused_by_every_G_wave_gate', 'MUST_FAIL')
    def _():
        out, ok = {}, True
        for name, s in NON_S1:
            sg, ig = spec_gates(s), ident_gates(s)
            want_ident = battery[name][2]
            out[name] = {'spec_any_true': any(sg.values()), 'identity': ig}
            ok = ok and not any(sg.values()) and all(v == want_ident for v in ig.values())
        return ok, out
    for cu in (G6C.X.C, G6C.X.PRED.C, G6C.A.PRED.C, G6C.PRED.C, G6C.PRED.X.C, G6C.A.L.CU):
        stub_custody(cu)

    # ============================================================================================ G3: GQ
    GQ = {}
    SPY = []
    real_grid, real_kept = U._grid, U.kept_region

    def spy_on():
        def spy_kept(stage, trunc, K):
            r = real_kept(stage, trunc, K)
            SPY.append(('kept', stage, trunc, K, copy.deepcopy(r)))
            return r

        def spy_grid(kept, outer, quad, R):
            g = real_grid(kept, outer, quad, R)
            SPY.append(('grid', copy.deepcopy(kept), np.array(g['kp'], copy=True)))
            return g
        del SPY[:]
        U.kept_region, U._grid = spy_kept, spy_grid

    def spy_off():
        U.kept_region, U._grid = real_kept, real_grid
        out = list(SPY)
        del SPY[:]
        return out

    def custody_as_ks1(mod):
        """A 6810b7c3 instance whose derive_details returns KS1's (the K=3 details), every other seam as stub_custody."""
        stub_custody(mod)
        mod.derive_details = lambda *, spec, driver_sha256=None: details_of(spec)
        return mod
    with open(PRED['G3A'][0]) as f:
        src_c6 = f.read()
    SUB_OLD = "kept=U.kept_region('route_a',None,4/U.KPC_M)"
    SUB_NEW = "kept=U.kept_region('route_a',None,3/U.KPC_M)"
    assert src_c6.count(SUB_OLD) == 1 and src_c6.count('4/U.KPC_M') == 1
    SUBST = load(PRED['G3A'][0], 'gwt_c6ffb338_K3_substituted_in_memory', text=src_c6.replace(SUB_OLD, SUB_NEW, 1))
    custody_as_ks1(SUBST.C)
    CTRL = load(PRED['G3A'][0], 'gwt_c6ffb338_K4_control', PRED['G3A'][1])
    custody_as_ks1(CTRL.C)
    quad = BASE['numerics']['uv_tail']['quadrature']
    R_EVAL = BASE['numerics']['uv_tail']['domain']['R_eval_max_kpc']
    PINVOL = ('producer', 'custody_deriver', 'seconds')

    def gq_runs():
        if 'runs' not in GQ:
            spy_on()
            try:
                rs = G3A.produce(copy.deepcopy(C3T))
                sp_s = spy_off()
                spy_on()
                rp = SUBST.produce(copy.deepcopy(C3T))
                sp_p = spy_off()
                spy_on()
                rc = CTRL.produce(copy.deepcopy(C3T))
                sp_c = spy_off()
            finally:
                U.kept_region, U._grid = real_kept, real_grid
            GQ['runs'] = (rs, rp, rc, sp_s, sp_p, sp_c)
        return GQ['runs']

    @case('GQ-E1_code_object_diff_is_exactly_the_gate_and_the_kept_K', 'EQUIVALENCE')
    def _():
        succ, pred = fn_node(GPIN['G3A']['path'], 'produce'), fn_node(PRED['G3A'][0], 'produce')
        gate = succ.body[0]
        gate_ok = (isinstance(gate, ast.If) and ast.unparse(gate.test) == 'not C.s1_c3t_spec(spec)' and not gate.orelse
                   and len(gate.body) == 1 and isinstance(gate.body[0], ast.Return)
                   and ast.unparse(gate.body[0].value) == 'P.produce(spec, node_limit=node_limit, progress=progress)')
        succ.body = succ.body[1:]
        subs = []

        class Sub(ast.NodeTransformer):
            def visit_Call(self, node):
                self.generic_visit(node)
                if isinstance(node.func, ast.Name) and node.func.id == 'kept_k' and [ast.unparse(x) for x in node.args] == ['spec']:
                    subs.append(ast.unparse(node))
                    return ast.copy_location(ast.Constant(4), node)
                return node
        succ = Sub().visit(succ)
        same_ast = ast.dump(succ, include_attributes=False) == ast.dump(pred, include_attributes=False)
        cs, cp = G3A.produce.__code__, G3A.P.produce.__code__
        key = lambda c: (type(c).__name__, repr(c))
        names_added, names_removed = sorted(set(cs.co_names) - set(cp.co_names)), sorted(set(cp.co_names) - set(cs.co_names))
        consts_added = sorted(repr(c) for c in cs.co_consts if key(c) not in {key(d) for d in cp.co_consts})
        consts_removed = sorted(repr(c) for c in cp.co_consts if key(c) not in {key(d) for d in cs.co_consts})
        kk = fn_node(GPIN['G3A']['path'], 'kept_k')
        others = {}
        for k_, path_s, path_p, gate_txt in (('G3B', GPIN['G3B']['path'], PRED['G3B'][0], 'PRED.produce(spec, node_limit=node_limit, progress=progress)'),
                                             ('G3C', GPIN['G3C']['path'], PRED['G3C'][0], 'PRED.produce(spec, node_limit=node_limit, progress=progress)')):
            s_, p_ = fn_node(path_s, 'produce'), fn_node(path_p, 'produce')
            g_ = s_.body[0]
            ok_gate = isinstance(g_, ast.If) and ast.unparse(g_.test) == 'not C.s1_c3t_spec(spec)' and ast.unparse(g_.body[0].value) == gate_txt
            s_.body = s_.body[1:]
            others[k_] = ok_gate and ast.dump(s_, include_attributes=False) == ast.dump(p_, include_attributes=False)
            for fname in ('policy', 'signed_bound'):
                others['%s.%s_AST_identical' % (k_, fname)] = (ast.dump(fn_node(path_s, fname), include_attributes=False)
                                                                == ast.dump(fn_node(path_p, fname), include_attributes=False))
        det = {'gate_is_first_statement': gate_ok, 'kept_k_substitutions': subs, 'AST_equal_after_removing_gate_and_K_to_4': same_ast,
               'co_names_added': names_added, 'co_names_removed': names_removed, 'co_consts_added': consts_added,
               'co_consts_removed': consts_removed, 'kept_k_source': ast.unparse(kk), 'G3B_G3C_produce_and_spec_free_functions': others}
        ok = (gate_ok and subs == ['kept_k(spec)'] and same_ast and names_removed == [] and consts_removed == ['4']
              and set(names_added) == {'P', 'kept_k', 'produce', 's1_c3t_spec'} and set(consts_added) <= {"('node_limit', 'progress')", 'None'}
              and all(others.values()))
        return ok, det

    @case('GQ-E2_K3_certificate_equals_c6ffb338_with_only_the_kept_K_substituted', 'EQUIVALENCE')
    def _():
        rs, rp, rc, sp_s, sp_p, sp_c = gq_runs()
        a_, b_ = strip(rs, PINVOL), strip(rp, PINVOL)
        diff = sorted(k for k in set(a_) | set(b_) if a_.get(k) != b_.get(k))
        kp_s = [x[2] for x in sp_s if x[0] == 'grid']
        kp_p = [x[2] for x in sp_p if x[0] == 'grid']
        kp_c = [x[2] for x in sp_c if x[0] == 'grid']
        same_nodes = len(kp_s) == len(kp_p) == 1 and np.array_equal(kp_s[0], kp_p[0])
        ok = (not diff and canonical(a_) == canonical(b_) and same_nodes and rs['verdict'] == 'PASS'
              and rs['production_nodes'] == rs['nodes_tested'] == 20720 and rc['production_nodes'] == 20736
              and rs['producer'] == GPIN['G3A'] and rs['custody_deriver'] == KPIN['KS1'] and rp['producer'] == pin_file(PRED['G3A'][0]))
        return ok, {'fields_differing_besides_producer_custody_deriver_seconds': diff, 'same_kperp_nodes': same_nodes,
                    'K3': {k: rs.get(k) for k in ('verdict', 'production_nodes', 'conservative_bound', 'worst', 'columns')},
                    'K4_control_same_spec': {k: rc.get(k) for k in ('verdict', 'production_nodes', 'conservative_bound', 'worst')},
                    'K3_vs_K4_nodes_shared': int(len(set(np.round(kp_s[0], 12)) & set(np.round(kp_c[0], 12)))) if kp_s and kp_c else None,
                    'note': 'the substituted predecessor is c6ffb338 text with exactly one in-memory replacement (L39 4 -> 3), never '
                            'written; its producer pin names the unsubstituted file, so producer/custody_deriver/seconds are excluded'}

    @case('GQ-E3_independent_K3_kept_region_and_kperp_node_set', 'EQUIVALENCE')
    def _():
        rs, rp, rc, sp_s, sp_p, sp_c = gq_runs()
        kept_s = [x for x in sp_s if x[0] == 'kept']
        kp_s = [x for x in sp_s if x[0] == 'grid']
        kp_c = [x for x in sp_c if x[0] == 'grid']
        ind3 = independent_kp_nodes(3.0, 128.0, quad['order'], quad['w_perp_max_inverse_kpc'], R_EVAL)
        ind4 = independent_kp_nodes(4.0, 128.0, quad['order'], quad['w_perp_max_inverse_kpc'], R_EVAL)
        rel3 = float(np.max(np.abs(ind3 - kp_s[0][2]) / np.abs(kp_s[0][2]))) if len(ind3) == len(kp_s[0][2]) else None
        rel4 = float(np.max(np.abs(ind4 - kp_c[0][2]) / np.abs(kp_c[0][2]))) if len(ind4) == len(kp_c[0][2]) else None
        det = {'kept_region_used': kept_s[0][4] if kept_s else None, 'kept_region_stage_trunc': kept_s[0][1:3] if kept_s else None,
               'kept_K_arg_times_KPC': kept_s[0][3] * U.KPC_M if kept_s else None,
               'N_independent_K3': int(len(ind3)), 'N_used_K3': int(len(kp_s[0][2])), 'bitwise_equal_K3': bool(np.array_equal(ind3, kp_s[0][2])),
               'max_rel_K3': rel3, 'N_independent_K4': int(len(ind4)), 'N_used_K4_control': int(len(kp_c[0][2])),
               'bitwise_equal_K4': bool(np.array_equal(ind4, kp_c[0][2])), 'max_rel_K4': rel4,
               'record_production_nodes': rs['production_nodes'],
               'K3_nodes_absent_at_K4': int(len(set(np.round(ind3, 12)) - set(np.round(ind4, 12)))),
               'breaks_K3': [0.0, 3.0, math.sqrt(2) * 3.0, 128.0]}
        ok = (det['kept_region_used'] == {'shape': 'cube', 'K_inverse_kpc': 3.0} and det['kept_region_stage_trunc'] == ('route_a', None)
              and len(ind3) == 20720 == rs['production_nodes'] and det['bitwise_equal_K3'] and len(ind4) == 20736 and det['bitwise_equal_K4'])
        return ok, det

    @case('GQ-P1_S1_GQ_TESTED_PASS_through_the_G3_producer_and_row32_check_gq', 'MUST_PASS')
    def _():
        rb = G3B.produce(copy.deepcopy(C3T))
        GQ['g3b'] = rb
        chk = R3.check_gq(rb, DET['point_sha256'], DET['custody_sha256'], s1=True)
        chk4 = R3.check_gq(rb, DET['point_sha256'], DET['custody_sha256'], s1=False)
        ok = (rb['status'] == 'TESTED' and rb['verdict'] == 'PASS' and rb['production_nodes'] == rb['nodes_tested'] == 20720
              and rb['producer'] == GPIN['G3B'] and rb['numeric_producer'] == GPIN['G3A'] and rb['custody_deriver'] == KPIN['KS1']
              and rb['point_sha256'] == DET['point_sha256'] and rb['custody_sha256'] == DET['custody_sha256']
              and all(chk.values()) and chk4['producer_pin_canonical_R4'] is False)
        return ok, {'record': {k: rb.get(k) for k in ('verdict', 'production_nodes', 'conservative_bound')}, 'check_gq_s1': chk,
                    'check_gq_rows_1_31_rule_on_it': chk4}

    @case('GQ-F1_K3_GQ_refused_outside_S1_UA_C3T', 'MUST_FAIL')
    def _():
        out = {}
        for name, s in NON_S1:
            if name in ('S1_C3T_label_base_K4_grid', 'S1_C3T_label_CB_C4T_grid'):
                continue                                  # valid K=4 specs: the GQ runs (GQ-D2)
            out[name] = [outcome(lambda s=s: mod.produce(copy.deepcopy(s)))[0][:60] for mod in (G3A, G3B, G3C)]
        ok = all(all('K4 cube required' in x for x in v) for v in out.values())
        return ok, out

    @case('GQ-F2_K4_GQ_record_at_the_K3_point_refused_by_the_row32_check', 'MUST_FAIL')
    def _():
        rs, rp, rc, *_ = gq_runs()
        k4 = dict(rc)                                     # c6ffb338 (K=4 nodes) on the K=3 point, its own producer pin
        wave1 = dict(rs, producer={'path': PRED['G3B'][0], 'sha256': PRED['G3B'][1]})   # the wave-1 canonical GQ pin
        c1 = R3.check_gq(k4, DET['point_sha256'], DET['custody_sha256'], s1=True)
        c2 = R3.check_gq(wave1, DET['point_sha256'], DET['custody_sha256'], s1=True)
        ok = (c1['producer_pin_canonical_R4'] is False and c2['producer_pin_canonical_R4'] is False
              and rc['production_nodes'] != rs['production_nodes'])
        return ok, {'k4_nodes_record': c1, 'wave1_producer_pin': c2}

    @case('GQ-D1_non_S1_GQ_entries_are_the_predecessor_objects', 'DIFFERENTIAL')
    def _():
        saved = [(G3A.P, G3A.P.produce), (G3B.PRED, G3B.PRED.produce), (G3C.PRED, G3C.PRED.produce)]
        for mod, _f in saved:
            mod.produce = (lambda tag: lambda *a, **k: 'PRED_' + tag)(os.path.basename(mod.__file__))
        try:
            res = {}
            for name, s in [('row%02d' % r, specs[r]) for r in (1, 2, 29)] + NON_S1:
                res[name] = [G3A.produce(s), G3B.produce(s), G3C.produce(s)]
        finally:
            for mod, f_ in saved:
                mod.produce = f_
        ok = all(v == ['PRED_gq_geometry_r5_cx2v001.py', 'PRED_gq_producer_cx2v005.py', 'PRED_gq_producer_b1_c2v001.py'] for v in res.values())
        return ok, {'n_specs': len(res)}

    @case('GQ-D2_K4_GQ_record_identical_to_2832ceb9', 'DIFFERENTIAL')
    def _():
        a_ = G3B.produce(copy.deepcopy(BASE))
        b_ = P['G3B'].produce(copy.deepcopy(BASE))
        same = canonical(strip(a_, ('seconds',))) == canonical(strip(b_, ('seconds',)))
        return same and a_['production_nodes'] == 20736 and a_['producer'] == pin_file(PRED['G3B'][0]), {
            'production_nodes': a_['production_nodes'], 'producer': a_['producer']['path'][-30:], 'equal_but_seconds': same}

    @case('GQ-D3_spec_free_policy_and_signed_bound_equal_predecessors_up_to_self_pins', 'DIFFERENTIAL')
    def _():
        args = [(1e-14, 1e-3, 1.0, 1.0), (1e-14, 1e-3, 2.0, 1.0), (5e-13, 0.0, 1.0, 1.0), (7e-13, 0.0, 1.0, 1.0),
                (1e-14, 1e-3, 0.0, 0.0), (1e-16, 0.001, 2.0, 1.0), (1e-14, 0.1, 1e-310, 0.999e-310)]
        out, ok = {}, True
        for k_, new, old in (('G3B', G3B, P['G3B']), ('G3C', G3C, P['G3C'])):
            same_pol = canonical(new.policy()) == canonical(old.policy())
            sb = []
            for a_ in args:
                for norm in ('SIGNED_P0', 'MAX_COMPONENT'):
                    x, y = outcome(lambda: new.signed_bound(*a_, normalizer=norm)), outcome(lambda: old.signed_bound(*a_, normalizer=norm))
                    xs = None if x[1] is None else strip(x[1], ('producer', 'numeric_producer'))
                    ys = None if y[1] is None else strip(y[1], ('producer', 'numeric_producer'))
                    sb.append(x[0] == y[0] and canonical(xs) == canonical(ys) and (x[1] is None or x[1]['producer'] == GPIN[k_]))
            out[k_] = {'policy_equal': same_pol, 'signed_bound_cases_equal': sum(sb), 'n': len(sb)}
            ok = ok and same_pol and all(sb)
        return ok, out

    # ============================================================================================ shared record builders
    A1PIN = {'path': PRED['response'][0], 'sha256': PRED['response'][1]}
    KS2PIN = {'path': KPIN['KS2']['path'], 'sha256': KPIN['KS2']['sha256']}
    ANCHOR_PINS = {'custody': C.canonical_pin('custody'), 'producer': C.canonical_pin('response_producer'),
                   'envelope': {'path': CERT + '/certs2_common_r5_cx2v001.py', 'sha256': 'f8f422f034153b4551e5fd5f89740cb594cb9d877e54b467c617206d2fcd6d8c'},
                   'lwr_common': {'path': '/synthetic/lwr_common_v001.py', 'sha256': '1' * 64},
                   'reference_symbols': {'path': '/synthetic/symbols.py', 'sha256': '2' * 64}}

    def pins_k3(**over):
        p = dict(ANCHOR_PINS, custody=C.canonical_pin('custody_ks1'), producer=C.canonical_pin('response_producer_ks2'))
        p.update(over)
        return p

    def rho_doc(ident, custody, K, producer, deps, *, part=None, cov=None, utc='2026-10-19T00:00:00Z', seconds=1.0):
        part = part if part is not None else partition(int(K))
        return {'schema': 'UNT_POINT_RHO_NUMERICAL_CX2V001', 'gate': 'RHO_G', 'status': 'TESTED', 'utc': utc,
                'identity': ident, 'point_sha256': digest(ident), 'custody': dict(custody), 'producer': producer, 'dependencies': deps,
                'settings': 'registered', 'verdict': 'NUMERICAL_ESTIMATE_REVIEW_REQUIRED', 'coverage_complete': True,
                'required_coverage_inverse_kpc': cov if cov is not None else [float(K), 182.0], 'full_registered_search_executed': True,
                'shells': [{'range_inverse_kpc': p_, 'rho_used': 0.02 - 0.001 * i, 'rho_envelope': {'estimate': 0.02 - 0.001 * i},
                            'sampled_levels': [{'level': 1, 'estimate': 0.01, 'n_samples': 10}]} for i, p_ in enumerate(part)],
                'seconds': seconds, 'peak_rss_bytes': 1}
    ADV_D = {   # A175 (ADV-D1/D2): row-32 rho slots that must never bind the K=3 point
        'K4_partition_from_4_5_coverage_4_182': dict(K=4, part=partition(4), cov=[4.0, 182.0], producer=KS2PIN),
        'K4_partition_from_4_5_coverage_3_182': dict(K=3, part=partition(4), cov=[3.0, 182.0], producer=KS2PIN),
        'merged_3_5': dict(K=3, part=[[3.0, 5.0]] + partition(4)[1:], cov=[3.0, 182.0], producer=KS2PIN),
        'producer_a1dcdea8': dict(K=3, part=partition(3), cov=[3.0, 182.0], producer=A1PIN)}

    # ---- schema-valid EPS / rho numeric doubles inside the REAL KS2 (and its a1dcdea8 object) produce_eps / produce_rho
    CC_REAL = KS2.CC

    def d_discrete(ctx, lo, hi):
        levels = {}
        for lv, nd in ((0, 26), (1, 52)):
            nk = len(CC_REAL.shell_k(lo, hi, CC_REAL.PER_DECADE[lv]))
            levels[str(lv)] = dict(eps=1e-5, n_samples=nd * nk, n_k=nk, n_dirs=nd, k_at_max_inverse_kpc=float(lo + 0.5 * (hi - lo)),
                                   dir_at_max=[0.0, 0.0, 1.0], max_abs_imag_q=0.0)
        return dict(eps_base=1e-5, eps_refined=1e-5, refinements=0, certified=True, levels=levels)

    def d_search(ctx, lo, hi, cfg, *, objective='EPS', audit=False, previous=None):
        nt, nd = cfg['audit_torus' if audit else 'torus'], cfg['audit_dirs' if audit else 'directions']
        fr = [0.0, 0.25, 0.5, 0.75, 1.0] if audit else [0.0, 0.5, 1.0]
        est = (2e-5 if objective == 'EPS' else 0.015) / (lo + 1.0) * (1.25 if audit else 1.0)
        return dict(estimate=est, grid_max=0.9 * est, n_grid=len(fr) * nd * nt ** 3, torus_m=nt, direction_count=nd,
                    radial_fractions=fr, starts=cfg['audit_starts' if audit else 'starts'] + (0 if previous is None else 1),
                    iterations=7, seed=20261018 + int(lo * 17 + hi * 29) + (100000 if audit else 0) + (200000 if objective != 'EPS' else 0),
                    t_at=[0.1, 0.2, 0.3], dir_at=[0.0, 0.0, 1.0], k_at_inverse_kpc=float(lo + 0.5 * (hi - lo)),
                    estimator_scope='synthetic double (G-wave test)')

    def d_actual(ctx, lo, hi, cfg, discrete):
        return dict(estimate=3e-6, dense_max=3e-6, local_max=2e-6, dense_nodes=10000 * len(CC_REAL.shell_k(lo, hi, 256)),
                    iterations=5, dir_at=[0.0, 1.0, 0.0], k_at_inverse_kpc=float(lo + 0.25 * (hi - lo)))
    CC_DOUBLE = types.SimpleNamespace(shell_k=CC_REAL.shell_k, PER_DECADE=CC_REAL.PER_DECADE,
                                      full_response=lambda B, kv, chunk=2048: np.full((len(kv), 10), 0.01 + 0j))
    for mod in (KS2, KS2.P):
        mod.discrete_shell, mod.search_envelope, mod.actual_eps_search, mod.CC = d_discrete, d_search, d_actual, CC_DOUBLE

    def synth_ctx(spec, source_pins):
        d = details_of(spec) if C.s1_c3t_spec(spec) else G3A.P.C.derive_details(spec=spec)
        return {'details': d, 'L': types.SimpleNamespace(KPC=KPC), 'B': types.SimpleNamespace(gam=1.0, volume=1.0),
                'isq': np.eye(3), 'D': [fib_sphere(26), fib_sphere(52), fib_sphere(104)], 'cache': {}, 'E': None,
                'source_pins': copy.deepcopy(source_pins), 'checks': {'synthetic': True}}

    # ---- the row file (procedure step 3) and the anchor context, as wave 1
    spec32_rel = 's1_specs/S1_UA_C3T_0123456789abcdef.cp1.spec.json'
    raw32 = json.dumps(C3T, sort_keys=True, indent=1).encode() + b'\n'
    FX.raw(spec32_rel, raw32)
    spec32_path = FX.path(spec32_rel)
    prefix = os.path.relpath(os.path.dirname(spec32_path), ART) + '/'
    key32 = C.point_key(C3T)
    assert key32 == DET['point_sha256']
    rowdoc = {'schema': C.S1_ROW_SCHEMA, 'row': 32, 'key': key32, 'label': 'S1_UA_C3T', 'names': ['S1_UA_C3T'],
              'spec_path': prefix + os.path.basename(spec32_path), 'spec_sha256': sha_bytes(raw32), 'distance_Mpc': 4.04, 'q_inf': 8.062}
    row_file = FX.raw('s1_rows/ROW32.json', json.dumps(rowdoc, sort_keys=True).encode())['path']
    for mod in (C, A4.C, M['KS3C2']):
        mod.S1_ROW_FILE, mod.S1_SPEC_PREFIX = row_file, prefix
    row32, row1 = C.select_points('32')[0], C.select_points('1')[0]
    rv_review = FX.json('rho_review/SYNTHETIC_PROOF_SIDE_REVIEW.json', {'schema': 'SYNTHETIC_REVIEW'})
    GATE_OPEN = {'allow_rho': True, 'review_pin': rv_review, 'review_sha256': rv_review['sha256']}

    def out_root_with_anchor(tag):
        o = FX.dir(FX.uniq(tag))
        k16 = C.ANCHOR_KEY[:16]
        d = os.path.join(o, 'P01_%s_TAIL_REANCHOR_a1' % k16)
        os.mkdir(d)
        with open(os.path.join(d, 'STAGE_CONTEXT_%s.json' % k16), 'xb') as f:
            f.write(json.dumps({'source_pins': ANCHOR_PINS, 'synthetic_fixture': SYN}).encode())
        return o

    def stage_files(pdir):
        recs = {}
        for n in sorted(os.listdir(pdir)):
            if n.endswith('.json'):
                with open(os.path.join(pdir, n), 'rb') as f:
                    recs[n] = json.loads(f.read())
        return recs

    def one(recs, prefix_):
        hits = [v for k, v in recs.items() if k.startswith(prefix_)]
        return hits[0] if len(hits) == 1 else {}

    def loader_with(gq_mod, source_pins):
        pr = types.SimpleNamespace(point_context=lambda spec: synth_ctx(spec, source_pins),
                                   produce_eps=KS2.produce_eps, produce_rho=KS2.produce_rho)
        return lambda: (gq_mod, pr)
    E = {}

    # ============================================================================================ E: end to end (S1_UA_C3T)
    @case('E-P1_plan_rows_1_and_32_with_the_G_wave_producers', 'MUST_PASS')
    def _():
        p = R3.plan(C.select_points('1,32'))
        st = [x['status'] for x in p['points']]
        r32 = p['points'][1]
        ok = (st == ['SPEC_AND_KEY_VERIFIED'] * 2 and r32['kept_K'] == 3 and r32['producers']['gq'] == GPIN['G3B']
              and r32['producers']['eps_adapter'] == GPIN['G4'] and r32['producers']['eps_rho'] == KS2PIN and 'gwave' in r32
              and 'producers' not in p['points'][0])
        return ok, {'statuses': st, 'row32_producers': r32.get('producers')}

    @case('E-P2_run_point_row32_real_G3_GQ_KS2_EPS_and_rho_all_K3', 'MUST_PASS')
    def _():
        o = out_root_with_anchor('e2e_run32')
        rc, summ = R3.run_point(row32, o, operator_lane='GW-test', attempt=1, run_id='gwave', loader=loader_with(G3B, pins_k3()),
                                hold_poll_seconds=0.0, hold_sleep=lambda s: None, rho_gate_args=GATE_OPEN)
        pdir = os.path.join(o, R3.point_dir_name(row32, 1))
        recs = stage_files(pdir)
        k16 = key32[:16]
        gq, eps, rho = recs.get('GQ_PROOF_%s.json' % k16, {}), recs.get('EPS_NUMERIC_%s.json' % k16, {}), recs.get('RHO_NUMERIC_%s_a.json' % k16, {})
        sg, se, sr = one(recs, 'STAGE_GQ_'), one(recs, 'STAGE_EPS_'), one(recs, 'STAGE_RHO_a_')
        req = one(recs, 'EPS_REVIEW_REQUEST_')
        E.update(out_root=o, pdir=pdir, k16=k16, gq_pin={'path': os.path.join(pdir, 'GQ_PROOF_%s.json' % k16)},
                 eps_pin=se.get('record'), rho_pin=sr.get('record'))
        E['gq_pin'] = pin_file(E['gq_pin']['path']) if gq else None
        ok = (rc == 0 and 'POINT_DONE_%s.json' % k16 in recs and sg.get('ok') is True and se.get('ok') is True and sr.get('ok') is True
              and gq.get('producer') == GPIN['G3B'] and gq.get('production_nodes') == 20720 and gq.get('verdict') == 'PASS'
              and sg['checks'].get('producer_pin_canonical_R4') is True and len(eps.get('shells') or []) == 179
              and eps['shells'][0]['range_inverse_kpc'] == [3.0, 4.0] and eps.get('producer') == KS2PIN and len(eps.get('envelope_audit') or []) == 14
              and [s['range_inverse_kpc'] for s in rho.get('shells') or []] == partition(3) and rho.get('producer') == KS2PIN
              and one(recs, 'POINT_START_')['producers'] == {'gq': GPIN['G3B'], 'eps': KS2PIN}
              and req['bindings']['adapter_sha256'] == GPIN['G4']['sha256'])
        return ok, {'rc': rc, 'stages': summ.get('stages'), 'stopped': summ.get('stopped'), 'reason': summ.get('reason'),
                    'gq_checks': sg.get('checks'), 'eps_checks': se.get('checks'), 'rho_checks': sr.get('checks')}

    def eps_review(numeric_ref, adapter_sha, tag, **over):
        doc = {'schema': 'UNT_POINT_EPS_REVIEW_CX2V001', 'verdict': 'APPROVED', 'numeric_ref': numeric_ref, 'point_sha256': key32,
               'custody_sha256': DET['custody_sha256'], 'adapter_sha256': adapter_sha,
               'accepts_registered_numerical_estimate_not_rigorous_sup': True, 'reviewer_lane': 'Claude3',
               'distinct_from_producer_lane': True}
        doc.update(over)
        return FX.json('reviews/' + FX.uniq(tag) + '.json', doc)

    @case('E-F1_adapt_eps_row32_review_binding_the_K4_adapter_4de70486_refused', 'MUST_FAIL')
    def _():
        rv = eps_review(E['eps_pin'], PRED['G4'][1], 'eps_review_4de7')
        r = outcome(lambda: R3.adapt_point(row32, E['out_root'], review_path=rv['path'], approved_review_sha256=rv['sha256'],
                                           approved_signer_lanes=['Claude3'], attempt=1, adapter_loader=lambda: G4))
        return 'EPS_REVIEW_FIELD_MISMATCH: adapter_sha256' in r[0], r[0][:200]

    @case('E-P3_adapt_eps_row32_through_the_G4_adapter_179_shells_from_3', 'MUST_PASS')
    def _():
        rv = eps_review(E['eps_pin'], GPIN['G4']['sha256'], 'eps_review_g4')
        rc, res = R3.adapt_point(row32, E['out_root'], review_path=rv['path'], approved_review_sha256=rv['sha256'],
                                 approved_signer_lanes=['Claude3'], attempt=1, adapter_loader=lambda: G4)
        E['eps_proof_pin'] = res.get('eps_proof')
        with open(res['eps_proof']['path'], 'rb') if res.get('eps_proof') else open(os.devnull, 'rb') as f:
            proof = json.loads(f.read() or b'{}')
        ok = (rc == 0 and all(res.get('checks', {}).values()) and proof.get('producer') == GPIN['G4']
              and len(proof.get('shells') or []) == 179 and proof['shells'][0]['range_inverse_kpc'] == [3.0, 4.0]
              and proof.get('driver_certificate') == E['eps_pin'])
        return ok, {'rc': rc, 'checks': res.get('checks'), 'blockers': res.get('blockers')}

    SLOT_ENV = G1._real_env()
    SLOT_ENV.derive_details = lambda spec: details_of(spec)
    ANCHOR_RHO = [FX.json('anchor_rho/run_%d.json' % i, rho_doc(K4_ID, CUST, 4, A1PIN, ANCHOR_PINS, utc='run-%d' % i, seconds=30.0 + i))
                  for i in (1, 2)]

    def filled(spec0, eps_pin, lo_pin):
        s = copy.deepcopy(spec0)
        s['numerics']['uv_tail']['eps_certificate'], s['numerics']['uv_tail']['lo_certificate'] = eps_pin, lo_pin
        return s

    def slot_prove(mod, spec, rho_pin, *, registered=None, pair=None, env=None, approved=None):
        pair = pair if pair is not None else ANCHOR_RHO
        return mod._prove(spec, rho_pin, registered_rho_records=registered if registered is not None else [rho_pin] + pair,
                          anchor_rho_pair=pair, root_ruling_refs=[dict(r) for r in mod.ROOT_RULINGS],
                          approved_producer_sha256=approved if approved is not None else [GPIN['G1']['sha256'], PRED['G1'][1]],
                          env=env or SLOT_ENV)

    @case('E-P4_LO_slot_proof_G1_K3_rho_slot_with_the_K4_anchor_pair', 'MUST_PASS')
    def _():
        spec_f = filled(C3T, E['eps_pin'], E['rho_pin'])
        E['spec_filled'] = spec_f
        res = slot_prove(G1, spec_f, E['rho_pin'])
        ok = res['verdict'] == 'READY_FOR_MANIFEST' and res['proof']['producer'] == GPIN['G1']
        if ok:
            E['slot_pin'] = G1.write_proof(res, FX.dir('slot_proofs'))
        return ok and E.get('slot_pin') is not None, {'verdict': res['verdict'], 'blockers': res['blockers'],
                                                       'anchor_pair': (res.get('proof') or {}).get('anchor_rho_reproducibility')}

    APPROVED_S1 = [GPIN['G4'], GPIN['G3B'], GPIN['G1']]

    @case('E-P5_bundle_and_registry_row32_domain_K3_S1_C1_draft_names_G6c_and_KS5pp', 'MUST_PASS')
    def _():
        d = FX.dir('e2e_registry')
        b = A4.assemble_bundle(row32, eps_proof=E['eps_proof_pin'], gq_proof=E['gq_pin'], lo_proof=E['slot_pin'],
                               approved=APPROVED_S1, out_root=d)
        rp, mp = A4.assemble_registry([b['path']], approved=APPROVED_S1, out_root=d)
        E.update(bundle=b, registry=rp, reg_dir=d)
        with open(b['path'], 'rb') as f:
            bd = json.loads(f.read())
        with open(mp['path'], 'rb') as f:
            man = json.loads(f.read())
        s1f = man.get('s1_c3t_c1_tail_readiness_fields') or {}
        ok = (bd['domain'] == {'K_inverse_kpc': 3.0, 'K_big_inverse_kpc': 128.0} and s1f.get('custody_deriver') == C.canonical_pin('custody_ks1')
              and s1f.get('state_enumerator') == GPIN['G6C'] and man.get('s1_c3t_wrapper') == GPIN['KS5PP']
              and man.get('s1_c3t_canonical_approved_producers') == APPROVED_S1 and man.get('s1_c3t_guard') == KPIN['KS5'])
        return ok, {'domain': bd['domain'], 's1_fields': s1f, 'wrapper': man.get('s1_c3t_wrapper')}

    def c1_doc(registry, *, deriver, enumerator, approved, guard_sha, tag):
        rv = FX.json(FX.uniq(tag) + '/REVIEW.json', {
            'schema': 'DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001', 'status': 'TESTED', 'ok': True, 'driver_sha256': C.DRIVER_SHA,
            'custody_deriver': deriver, 'state_enumerator': enumerator, 'approved_certificate_producers': approved,
            'guard_sha256': guard_sha, 'driver_slot_rule': SLOT_RULE, 'post_state_handoff': HANDOFF_RULE})
        return FX.json(FX.uniq(tag) + '/C1.json', {'tail_readiness': {
            'certificate_registry': registry, 'custody_deriver': deriver, 'state_enumerator': enumerator,
            'certificate_policy_review': rv, 'approved_certificate_producers': approved}})

    def verify(mod, reg, rows_, c1ref, canonical_producers=None):
        return mod.verify_registry(reg, rows_, c1_ref=c1ref, custody_loader=lambda pin_: (lambda spec: details_of(spec)['custody']),
                                   guard=P['guard_b1'], guard_s1=KS5, canonical_producers=canonical_producers)

    @case('E-P6_verify_row32_against_the_canonical_S1_C1_G4_G3_G1_G6c_KS1_KS5', 'MUST_PASS')
    def _():
        c1 = c1_doc(E['registry'], deriver=C.canonical_pin('custody_ks1'), enumerator=GPIN['G6C'], approved=APPROVED_S1,
                    guard_sha=KPIN['KS5']['sha256'], tag='c1_s1_canonical')
        rep = verify(A4, E['registry'], [row32], c1)
        pt = rep['points'][0]
        return rep['ok'] is True and pt['ok'] is True, {'s1_gate': rep.get('c1_policy_gate_s1_c3t', {}).get('blockers'),
                                                       'wrapper_replica': pt['wrapper_replica'].get('blockers'),
                                                       'guard': (pt.get('guard_b1') or {}).get('blockers')}

    @case('E-F2_S1_C1_approving_the_wave1_K4_producers_or_naming_4ca7f364_refused', 'MUST_FAIL')
    def _():
        k4prod = [C.canonical_pin(n) for n in C.CANONICAL_APPROVED_PRODUCERS]
        c1a = c1_doc(E['registry'], deriver=C.canonical_pin('custody_ks1'), enumerator=GPIN['G6C'], approved=k4prod,
                     guard_sha=KPIN['KS5']['sha256'], tag='c1_s1_k4prod')
        c1b = c1_doc(E['registry'], deriver=C.canonical_pin('custody_ks1'), enumerator=C.canonical_pin('state_enumerator'),
                     approved=APPROVED_S1, guard_sha=KPIN['KS5']['sha256'], tag='c1_s1_4ca7')
        c1c = c1_doc(E['registry'], deriver=C.canonical_pin('custody'), enumerator=GPIN['G6C'], approved=APPROVED_S1,
                     guard_sha=KPIN['KS5']['sha256'], tag='c1_s1_6810')
        ra, rb, rc_ = verify(A4, E['registry'], [row32], c1a), verify(A4, E['registry'], [row32], c1b), verify(A4, E['registry'], [row32], c1c)
        ba, bb, bc = (str(r.get('c1_policy_gate_s1_c3t', {}).get('blockers')) for r in (ra, rb, rc_))
        ok = (ra['ok'] is False and 'C1_APPROVED_PRODUCER_NOT_CANONICAL' in ba and rb['ok'] is False
              and 'C1_STATE_ENUMERATOR_NOT_THE_G6_ENUMERATOR' in bb and rc_['ok'] is False and 'C1_CUSTODY_DERIVER_NOT_CANONICAL' in bc)
        return ok, {'k4_producers': ba[:160], 'enumerator_4ca7f364': bb[:160], 'custody_6810b7c3': bc[:160]}

    # ---- KS5'' end to end: the wrapper's own prelaunch certificate_check on the same artefacts
    Q = S5.W
    deriver_src = ("CUSTODY = %r\ndef derive_custody(*, spec, driver_sha256):\n    return dict(CUSTODY)\n" % CUST).encode()
    DERIVER = FX.raw('ks5pp/synthetic_custody_deriver.py', deriver_src)

    def wrapper_cfg(registry, guard_sha, approved, enumerator, tag):
        rv = FX.json(FX.uniq(tag) + '/REVIEW.json', {
            'schema': Q.POLICY_SCHEMA, 'status': 'TESTED', 'ok': True, 'driver_sha256': Q.DRIVER_SHA, 'custody_deriver': DERIVER,
            'state_enumerator': enumerator, 'approved_certificate_producers': approved, 'guard_sha256': guard_sha,
            'driver_slot_rule': SLOT_RULE, 'post_state_handoff': HANDOFF_RULE})
        return {'tail_readiness': {'certificate_registry': registry, 'custody_deriver': DERIVER, 'state_enumerator': enumerator,
                                   'certificate_policy_review': rv, 'approved_certificate_producers': approved}}

    def mkctx(mod, cfg, ks5=None):
        class Ctx(mod.Context):
            def __init__(self):
                self.cfg = copy.deepcopy(cfg)
                self.numerics = copy.deepcopy(BASE['numerics'])
        c_ = Ctx()
        if ks5 is not None:
            c_._s1_guard_ks5 = ks5
        return c_

    @case('E-P7_wrapper_KS5pp_prelaunch_certificate_check_on_the_e2e_artefacts', 'MUST_PASS')
    def _():
        cfg = wrapper_cfg(E['registry'], KPIN['KS5']['sha256'], APPROVED_S1, GPIN['G6C'], 'ks5pp_e2e')
        g = mkctx(S5, cfg, ks5=True).certificate_check(E['spec_filled'], 'prelaunch')
        return g.get('ok') is True, {'blockers': g.get('blockers')}

    # ---- ADV-D (A175) at KS4' verify and KS5'' prelaunch: wave-1-style certificate worlds with placeholder producers
    PLACE = {}
    for nm in ('EPS_ADAPTER', 'GQ_PRODUCER', 'SLOT_PRODUCER'):
        PLACE[nm] = FX.raw('placeholder/%s.txt' % nm, ('synthetic %s placeholder (G-wave tests); not a producer\n' % nm).encode())
    APPROVED_PH = [PLACE['EPS_ADAPTER'], PLACE['GQ_PRODUCER'], PLACE['SLOT_PRODUCER']]
    for mod in (W['KS3R'].C, W['KS4'].C, W['KS3C']):
        mod.S1_ROW_FILE, mod.S1_SPEC_PREFIX = row_file, prefix

    def eps_doc(ident, K, producer, deps):
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

    def adv_world(tag, rho_kw):
        t = FX.uniq(tag)
        es = FX.json(t + '/EPS_NUMERIC.json', eps_doc(C3T_ID, 3, KS2PIN, pins_k3()))
        rdoc = rho_doc(C3T_ID, CUST, rho_kw['K'], rho_kw['producer'], pins_k3(), part=rho_kw['part'], cov=rho_kw['cov'])
        rs = FX.json(t + '/RHO_NUMERIC.json', rdoc)
        ep = FX.json(t + '/EPS_PROOF.json', {'schema': PROOF, 'gate': 'EPS', 'status': 'TESTED', 'verdict': 'PASS', 'point_sha256': key32,
                                            'custody_sha256': DET['custody_sha256'], 'producer': PLACE['EPS_ADAPTER'], 'driver_certificate': es,
                                            'numeric_evidence': es, 'envelope_rule': ENV_RULE,
                                            'shells': [{'range_inverse_kpc': [float(n), float(n + 1)], 'eps': 1e-4, 'eps_envelope': 1e-4,
                                                        'refinement_failures': 0} for n in range(3, 182)]})
        gp = FX.json(t + '/GQ_PROOF.json', dict(GQ['g3b'] if 'g3b' in GQ else gq_runs()[0], producer=PLACE['GQ_PRODUCER']))
        lp = FX.json(t + '/SLOT_PROOF.json', {'schema': PROOF, 'gate': 'LO_RHO_SLOT', 'status': 'TESTED', 'verdict': 'PASS',
                                             'point_sha256': key32, 'custody_sha256': DET['custody_sha256'], 'producer': PLACE['SLOT_PRODUCER'],
                                             'driver_certificate': rs, 'rho_record': rs, 'rho_bitwise_projection': G1.rho_projection(rdoc)})
        d = FX.dir(t + '/reg')
        b = A4.assemble_bundle(row32, eps_proof=ep, gq_proof=gp, lo_proof=lp, approved=APPROVED_PH, out_root=d)
        rp, _m = A4.assemble_registry([b['path']], approved=APPROVED_PH, out_root=d)
        return {'spec': filled(C3T, es, rs), 'registry': rp}

    @case('KF-ADV-D_row32_rho_slot_not_the_K3_contract_refused_at_KS4pp_verify_and_KS5pp_prelaunch', 'MUST_FAIL')
    def _():
        out, ok = {}, True
        honest = dict(K=3, part=partition(3), cov=[3.0, 182.0], producer=KS2PIN)
        for name, kw in list(ADV_D.items()) + [('honest_K3_control', honest)]:
            w = adv_world('adv_' + name, kw)
            c1 = c1_doc(w['registry'], deriver=C.canonical_pin('custody_ks1'), enumerator=GPIN['G6C'], approved=APPROVED_PH,
                        guard_sha=KPIN['KS5']['sha256'], tag='c1_adv')
            v = verify(A4, w['registry'], [row32], c1, canonical_producers=APPROVED_PH)
            cfg = wrapper_cfg(w['registry'], KPIN['KS5']['sha256'], APPROVED_PH, GPIN['G6C'], 'ks5pp_adv')
            g2 = mkctx(S5, cfg, ks5=True).certificate_check(w['spec'], 'prelaunch')
            g1 = mkctx(W['KS5P'], cfg, ks5=True).certificate_check(w['spec'], 'prelaunch')
            blk = str((v['points'][0].get('guard_b1') or {}).get('blockers'))
            out[name] = {'KS4p_verify_ok': v['ok'], 'KS4p_blockers': blk[:200], 'KS5pp_ok': g2.get('ok'),
                         'KS5pp_blockers': str(g2.get('blockers'))[:200], 'wave1_KS5p_ok': g1.get('ok')}
            if name == 'honest_K3_control':
                ok = ok and v['ok'] is True and g2.get('ok') is True and g1.get('ok') is True
            else:
                ok = (ok and v['ok'] is False and 'S1_UA_C3T_RHO_SLOT_NOT_THE_K3_CONTRACT' in blk and g2.get('ok') is False
                      and 'S1_UA_C3T_RHO_SLOT_NOT_THE_K3_CONTRACT' in str(g2.get('blockers')) and g1.get('ok') is True)
        return ok, out

    # ============================================================================================ G4: EPS adapter
    def eps_record_of(pin):
        with open(pin['path'], 'rb') as f:
            return json.loads(f.read())

    @case('G4-P1_S1_adapt_eps_on_the_KS2_record_ready_179_shells_G4_producer', 'MUST_PASS')
    def _():
        rv = eps_review(E['eps_pin'], GPIN['G4']['sha256'], 'g4p1')
        r = G4.adapt_eps(copy.deepcopy(C3T), E['eps_pin'], review_ref=rv, approved_producer_sha256=(KS2PIN['sha256'], GPIN['G4']['sha256']),
                         approved_review_sha256=(rv['sha256'],))
        pf = r.get('proof') or {}
        ok = (r['verdict'] == 'READY_FOR_MANIFEST' and pf.get('producer') == GPIN['G4'] and len(pf.get('shells') or []) == 179
              and pf['shells'][0]['range_inverse_kpc'] == [3.0, 4.0] and pf['shells'][-1]['range_inverse_kpc'] == [181.0, 182.0])
        return ok, {'verdict': r['verdict'], 'blockers': r['blockers']}

    @case('G4-F1_K4_records_reviews_or_approvals_at_the_K3_point_refused', 'MUST_FAIL')
    def _():
        rec = eps_record_of(E['eps_pin'])
        v_a1 = FX.json('g4f/eps_producer_a1dcdea8.json', dict(rec, producer=A1PIN))
        k4s = dict(rec, shells=rec['shells'][1:], required_coverage_inverse_kpc=[4.0, 182.0],
                   eps_max=max(s['eps'] for s in rec['shells'][1:]), eps_max_shell=max(rec['shells'][1:], key=lambda s: s['eps'])['range_inverse_kpc'])
        v_k4 = FX.json('g4f/eps_shells_from_4.json', k4s)
        appr = (KS2PIN['sha256'], GPIN['G4']['sha256'], A1PIN['sha256'])

        def run(mod, spec, ref, adapter_sha=None, approved=appr):
            rv = eps_review(ref, adapter_sha or GPIN['G4']['sha256'], 'g4f', custody_sha256=details_of(C3T)['custody_sha256'])
            return mod.adapt_eps(copy.deepcopy(spec), ref, review_ref=rv, approved_producer_sha256=approved,
                                 approved_review_sha256=(rv['sha256'],))
        r = {'producer_a1dcdea8': run(G4, C3T, v_a1)['blockers'], 'shells_from_4': run(G4, C3T, v_k4)['blockers'],
             'review_binds_4de70486': run(G4, C3T, E['eps_pin'], adapter_sha=PRED['G4'][1])['blockers'],
             'G4_not_approved': run(G4, C3T, E['eps_pin'], approved=(KS2PIN['sha256'],))['blockers'],
             'S1_record_for_K4_spec': run(G4, BASE, E['eps_pin'])['blockers'],
             '4de70486_on_the_K3_point': run(P['G4'], C3T, E['eps_pin'], adapter_sha=PRED['G4'][1])['blockers']}
        want = {'producer_a1dcdea8': 'UNSUPPORTED_NUMERICAL_PRODUCER', 'shells_from_4': 'EPS_ACTUAL_SHELL_COVERAGE_GAP',
                'review_binds_4de70486': 'EPS_REVIEW_ADAPTER_MISMATCH', 'G4_not_approved': 'NOT_INDEPENDENTLY_APPROVED',
                'S1_record_for_K4_spec': 'EPS_NUMERICAL_POINT_CUSTODY_MISMATCH', '4de70486_on_the_K3_point': 'K4 cube required'}
        ok = all(want[k] in str(v) for k, v in r.items())
        return ok, {k: str(v)[:120] for k, v in r.items()}

    @case('G4-D1_non_S1_adapt_eps_is_4de70486_and_K4_result_identical', 'DIFFERENTIAL')
    def _():
        saved = G4.P.adapt_eps
        G4.P.adapt_eps = lambda *a, **k: 'PRED_4de70486'
        try:
            sent = {n: G4.adapt_eps(s, {'path': '/x', 'sha256': '0' * 64}) for n, s in [('row01', BASE), ('row29', specs[29])] + NON_S1}
        finally:
            G4.P.adapt_eps = saved
        ctx4 = synth_ctx(BASE, ANCHOR_PINS)
        k4 = KS2.produce_eps(copy.deepcopy(BASE), context=ctx4)        # KS2 -> a1dcdea8 (with the same numeric doubles)
        k4pin = FX.json('g4d/EPS_NUMERIC_K4.json', k4)
        rv = FX.json('g4d/REVIEW.json', {'schema': 'UNT_POINT_EPS_REVIEW_CX2V001', 'verdict': 'APPROVED', 'numeric_ref': k4pin,
                                         'point_sha256': ctx4['details']['point_sha256'], 'custody_sha256': ctx4['details']['custody_sha256'],
                                         'adapter_sha256': PRED['G4'][1], 'accepts_registered_numerical_estimate_not_rigorous_sup': True})
        kw = dict(review_ref=rv, approved_producer_sha256=(A1PIN['sha256'], PRED['G4'][1]), approved_review_sha256=(rv['sha256'],))
        a_, b_ = G4.adapt_eps(copy.deepcopy(BASE), k4pin, **kw), P['G4'].adapt_eps(copy.deepcopy(BASE), k4pin, **kw)
        norm = lambda r: json.loads(json.dumps(r).replace('"utc": "%s"' % r.get('utc'), '"utc": "X"')) if False else \
            dict(strip(r, ('utc',)), proof=strip(r.get('proof'), ('utc',)) if r.get('proof') else None)
        same = canonical(norm(a_)) == canonical(norm(b_))
        ok = (all(v == 'PRED_4de70486' for v in sent.values()) and same and a_['verdict'] == 'READY_FOR_MANIFEST'
              and a_['proof']['producer'] == pin_file(PRED['G4'][0]) and len(k4['shells']) == 178)
        return ok, {'delegated': len(sent), 'K4_result_equal_but_utc': same, 'verdict': a_['verdict'], 'blockers': a_['blockers']}

    # ============================================================================================ G1: LO slot proof
    @case('G1-F1_ADV_D_row32_rho_slots_refused_by_the_slot_proof', 'MUST_FAIL')
    def _():
        want = {'K4_partition_from_4_5_coverage_4_182': 'RHO_COVERAGE_NOT_3_TO_182',
                'K4_partition_from_4_5_coverage_3_182': 'RHO_PARTITION_NOT_REGISTERED',
                'merged_3_5': 'RHO_PARTITION_NOT_REGISTERED', 'producer_a1dcdea8': 'RHO_PRODUCER_NOT_RESPONSE_KS2'}
        out, ok = {}, True
        for name, kw in ADV_D.items():
            rp = FX.json('g1f/' + FX.uniq(name) + '.json', rho_doc(C3T_ID, CUST, kw['K'], kw['producer'], pins_k3(), part=kw['part'], cov=kw['cov']))
            res = slot_prove(G1, filled(C3T, E['eps_pin'], rp), rp)
            out[name] = res['blockers']
            ok = ok and res['verdict'] == 'BLOCKED' and res['proof'] is None and want[name] in str(res['blockers'])
        return ok, out

    @case('G1-F2_anchor_pair_stays_K4_and_a_K3_rho_never_binds_a_K4_point', 'MUST_FAIL')
    def _():
        k3anc = [FX.json('g1f2/anchor_k3_%d.json' % i, rho_doc(K4_ID, CUST, 3, KS2PIN, pins_k3(), utc='k3-%d' % i)) for i in (1, 2)]
        r1 = slot_prove(G1, E['spec_filled'], E['rho_pin'], pair=k3anc)
        rho3 = eps_record_of(E['rho_pin'])
        rec_k4id = dict(rho3, identity=K4_ID, point_sha256=digest(K4_ID))
        r2 = outcome(lambda: G1.check_rho_record(rec_k4id, read_raw=SLOT_ENV.read_raw, identity=K4_ID, custody=rho3['custody'],
                                                 point_sha256=digest(K4_ID)))[0]
        ok = r1['verdict'] == 'BLOCKED' and 'RHO_COVERAGE_NOT_4_TO_182' in str(r1['blockers']) and 'RHO_COVERAGE_NOT_4_TO_182' in r2
        return ok, {'K3_anchor_pair': r1['blockers'], 'K3_rho_for_K4_identity': r2[:100]}

    @case('G1-F3_cd10cd59_itself_cannot_bind_the_K3_point', 'MUST_FAIL')
    def _():
        env_a = P['G1']._real_env()
        env_a.derive_details = lambda spec: G3A.P.C.derive_details(spec=spec)        # 6810b7c3 (synthetic seams)
        env_b = P['G1']._real_env()
        env_b.derive_details = lambda spec: details_of(spec)                         # even with KS1's details
        ra = slot_prove(P['G1'], E['spec_filled'], E['rho_pin'], env=env_a)
        rb = slot_prove(P['G1'], E['spec_filled'], E['rho_pin'], env=env_b)
        ok = ('K4 cube required' in str(ra['blockers']) and 'RHO_COVERAGE_NOT_4_TO_182' in str(rb['blockers'])
              and ra['verdict'] == rb['verdict'] == 'BLOCKED')
        return ok, {'cd10cd59_custody': ra['blockers'], 'cd10cd59_with_KS1_details': rb['blockers']}

    @case('G1-D1_non_S1_slot_proof_is_cd10cd59_and_K4_rho_checks_identical', 'DIFFERENTIAL')
    def _():
        pred = G1._predecessor()
        saved = pred.prove_lo_slot
        pred.prove_lo_slot = lambda *a, **k: 'PRED_cd10cd59'
        try:
            sent = {n: G1.prove_lo_slot(s, {'path': '/x', 'sha256': '0' * 64}) for n, s in [('row01', BASE)] + NON_S1}
        finally:
            pred.prove_lo_slot = saved
        recs = {'anchor_a1dcdea8_K4': eps_record_of(ANCHOR_RHO[0]), 'K3_KS2': eps_record_of(E['rho_pin'])}
        for name, kw in ADV_D.items():
            recs[name] = rho_doc(C3T_ID, CUST, kw['K'], kw['producer'], pins_k3(), part=kw['part'], cov=kw['cov'])
        rr = {}
        for n, r in recs.items():
            for idn, ident in (('none', None), ('K4', K4_ID)):
                kw = {} if ident is None else {'identity': ident, 'custody': r.get('custody'), 'point_sha256': digest(ident)}
                a_ = outcome(lambda: G1.check_rho_record(copy.deepcopy(r), read_raw=SLOT_ENV.read_raw, **kw))
                b_ = outcome(lambda: P['G1'].check_rho_record(copy.deepcopy(r), read_raw=SLOT_ENV.read_raw, **kw))
                rr['%s/%s' % (n, idn)] = (a_[0][:70], a_ == b_)
        ok = all(v == 'PRED_cd10cd59' for v in sent.values()) and all(v[1] for v in rr.values())
        return ok, {'delegated': len(sent), 'check_rho_record': rr}

    # ============================================================================================ G2: SRB-ROT adapter
    JN = PV.create_provider()

    def tail_config(eps_slot, lo_slot):
        return U.normalize_config({
            'enabled': True, 'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0}, 'source_rule': 'continuum_v001',
            'gas': {'interp': 'lagrange3_s_gl4', 'M_s': 8},
            'stars': {'segment_rule': 'max16_ceil_kdr_plus8', 'tail_rule': 't_panels_40a_phase1p5_gl12'},
            'quadrature': {'order': 4, 'w_perp_max_inverse_kpc': 2.0, 'w_z_max_inverse_kpc': 2.0},
            'domain': {'R_eval_max_kpc': 0.2, 'z_eval_max_kpc': 0.2, 'z_src_max_kpc': 0.2},
            'asymptote': 'EH_exact_minus_quarter', 'lapse_only': True, 'jet_order': {'route_a': 1, 'route_b': 1, 'ngc_eval': 1},
            'lambda_scale': 1.0, 'eps_certificate': eps_slot, 'lo_certificate': lo_slot})

    def build_state(K, eps_slot, lo_slot, amp):
        kept = U.kept_region('le_rotation', {'shape': 'cube'}, K / U.KPC_M)
        return U.build(config=tail_config(eps_slot, lo_slot), kept=kept, roster=SyntheticRoster(amp), gamma_eff=2.0e-17,
                       c_m_s=299792458.0, eval_radii_m=[0.1 * U.KPC_M], jn_provider=JN, i1t={'verdict': 'NOT_APPLICABLE_SYNTHETIC'},
                       stage_kind='le_rotation')

    def cert(lo, hi, eps=1.0e-6):
        return {'shells': [{'lo_inverse_kpc': float(n), 'hi_inverse_kpc': float(n + 1), 'eps': eps} for n in range(lo, hi)]}

    @case('G2-T_DECIDING_library_field_bound_srb_rot_at_shells_from_3', 'DECIDING')
    def _():
        st3 = build_state(3, U.TEST_ONLY_CERT, U.TEST_ONLY_CERT, 1.0e30)
        st4 = build_state(4, U.TEST_ONLY_CERT, U.TEST_ONLY_CERT, 1.0e30)
        e3, si3 = st3._a['shell_edges_inverse_kpc'], st3._a['shell_integrals']
        rows_ = {'column_R_m': [0.05 * U.KPC_M, 0.1 * U.KPC_M], 'v_c_m_s': [3.0e4, 4.0e4], 'row_columns': [[0], [0, 1]], 'N_min': 1.0,
                 'tau_km_s': [1.0, 1.0]}
        r = {'K3_first_edge': float(e3[0]), 'K3_first_shell_B1_nonzero': bool(si3[0, 1] != 0), 'K4_first_edge': float(st4._a['shell_edges_inverse_kpc'][0]),
             'K3_field_bound_3_182': outcome(lambda: U.field_bound(st3, cert(3, 182)))[0],
             'K3_srb_rot_3_182': outcome(lambda: U.srb_rot(st3, cert(3, 182), rows_))[0],
             'K3_field_bound_4_182': outcome(lambda: U.field_bound(st3, cert(4, 182)))[0],
             'K3_srb_rot_4_182': outcome(lambda: U.srb_rot(st3, cert(4, 182), rows_))[0],
             'K4_field_bound_4_182': outcome(lambda: U.field_bound(st4, cert(4, 182)))[0]}
        ok = (r['K3_first_edge'] == 3.0 and r['K3_first_shell_B1_nonzero'] and r['K4_first_edge'] == 4.0
              and r['K3_field_bound_3_182'] == 'PASS' and r['K3_srb_rot_3_182'] == 'PASS' and r['K4_field_bound_4_182'] == 'PASS'
              and 'UV_TAIL_EPS_COVERAGE' in r['K3_field_bound_4_182'] and 'UV_TAIL_EPS_COVERAGE' in r['K3_srb_rot_4_182'])
        r['result'] = ('TESTED: field_bound/srb_rot WORK at shells from 3 with an EPS certificate on [3,182]; with [4,182] they '
                       'refuse UV_TAIL_EPS_COVERAGE at [3,4). The library needs no change; the adapter does (EPS coverage from the '
                       'kept K, KS1, the G6c enumerator).') if ok else 'UNEXPECTED'
        return ok, r

    # ---- the S1_UA_C3T final-rotation call for SRB-ROT, on the e2e EPS record, G4 proof and bundle
    SRB = {}

    def srb_world():
        if SRB:
            return SRB
        st = build_state(3, E['eps_pin'], E['rho_pin'], 1.0e-40)
        call = FX.dir('srb_call/call')
        os.makedirs(os.path.join(call, 'out'))
        result = {'status': 'COMPLETED', 'valid': True, 'final_pass': 1, 'passes': [{'pass': 1}],
                  'uv_tail': {'route_a_record': {'flags': [], 'monitor_status': 'M_T_WITHIN_THRESHOLD'}}, 'synthetic_fixture': SYN}
        rraw = json.dumps(result, sort_keys=True).encode()
        with open(os.path.join(call, 'out', 'result.json'), 'xb') as f:
            f.write(rraw)
        result_pin = {'path': os.path.join(call, 'out', 'result.json'), 'sha256': sha_bytes(rraw)}
        rec_pin = FX.raw('srb_call/state_record.json', json.dumps(st.record, sort_keys=True).encode())
        buf = FX.path('srb_call/state_arrays.npz')
        with open(buf, 'xb') as f:
            np.savez(f, **st.to_arrays())
        arr_pin = pin_file(buf)
        state = {'state_sha256': st.digest, 'source_sha256': st.record['roster_digest'], 'stage_kind': 'le_rotation', 'nonnegative_masses': True}
        inv = {'schema': 'DDO154_CONSUMED_STATE_JOIN_CX2V010', 'complete': True, 'producer': GPIN['G6C'], 'point_sha256': DET['point_sha256'],
               'custody_sha256': DET['custody_sha256'], 'states': [state],
               'occurrences': [{'ordinal': 0, 'role': 'own_source_state', 'stage': 'le1_rotation', 'stage_kind': 'le_rotation',
                                'state_sha256_claimed': st.digest}],
               'joined_occurrences': [{'ordinal': 0, 'state': state}]}
        sin = FX.json('srb_call/STATE_INPUT.json', {'schema': 'UNT_POINT_LO_STATE_INPUT_CX2V001', 'state': state, 'identity': DET['identity'],
                                                   'custody': CUST, 'call_result': result_pin,
                                                   'tail_state': {'record': rec_pin, 'arrays': arr_pin}})
        rprod = FX.raw('srb_call/synthetic_rows_producer.py', b'# synthetic SRB rows producer stand-in (G-wave tests)\n')
        rc = DET['row_contract']
        rows_in = FX.json('srb_call/ROWS_INPUT.json', {
            'schema': 'S4RC1_SRB_ROT_ROWS_INPUT_C3V001', 'state': state, 'call_result': result_pin, 'producer': rprod,
            'row_ids': [r_['id'] for r_ in rc['rows']], 'row_contract_sha256': CUST['row_contract_sha256'], 'tau_km_s': list(rc['tau_km_s']),
            'column_R_m': [0.05 * KPC, 0.1 * KPC], 'v_c_m_s': [3.0e4, 4.0e4], 'row_columns': [[0, 1]] * len(rc['rows']), 'N_min': 1.0})
        env = G2._real_env()
        env.derive_details = lambda spec: details_of(spec)
        SRB.update(st=st, call=call, result=result, inv=inv, sin=sin, rows_in=rows_in, rprod=rprod, env=env)
        return SRB

    def srb_run(mod, inv=None, env=None, approved=None, spec=None):
        w = srb_world()
        return mod._adapt(spec or E['spec_filled'], call_dir=w['call'], result=w['result'], inventory=inv or w['inv'], bundle_ref=E['bundle'],
                          state_input_ref=w['sin'], rows_input_ref=w['rows_in'], root_ruling_refs=[dict(r) for r in mod.ROOT_RULINGS],
                          approved_producer_sha256=approved or [GPIN['G2']['sha256'], GPIN['G4']['sha256']],
                          trusted_source_producers=[w['rprod']['sha256']], env=env or w['env'])

    @case('G2-P1_S1_SRB_ROT_end_to_end_PASS_on_a_K3_TailState_with_the_KS2_EPS_record', 'MUST_PASS')
    def _():
        r = srb_run(G2)
        pf = r.get('proof') or {}
        ok = (r['verdict'] == 'PASS' and r['reading'] == 'PASS' and pf.get('producer') == GPIN['G2'] and pf.get('eps_record') == E['eps_pin']
              and r.get('field_bound_eps_per_shell', [None])[0] is not None and SRB['st']._a['shell_edges_inverse_kpc'][0] == 3.0)
        return ok, {'verdict': r['verdict'], 'blockers': r['blockers'], 'bound_km_s': r.get('bound_km_s')}

    @case('G2-F1_K4_inventory_EPS_or_adapter_at_the_K3_point_refused', 'MUST_FAIL')
    def _():
        w = srb_world()
        inv4 = dict(w['inv'], producer={'path': PRED['G6C'][0], 'sha256': PRED['G6C'][1]})
        rec = eps_record_of(E['eps_pin'])
        e4 = dict(rec, shells=rec['shells'][1:], required_coverage_inverse_kpc=[4.0, 182.0])
        d4 = details_of(BASE) if False else G3A.P.C.derive_details(spec=BASE)
        rec4 = dict(rec, identity=d4['identity'], custody=d4['custody'], point_sha256=d4['point_sha256'])
        env_p = P['G2']._real_env()
        env_p.derive_details = lambda spec: details_of(spec)
        r = {'inventory_4ca7f364': str(srb_run(G2, inv=inv4)['blockers']),
             'eps_from_4_for_K3': outcome(lambda: G2.format_eps(e4, DET))[0],
             'eps_from_3_for_K4_identity': outcome(lambda: G2.format_eps(rec4, d4))[0],
             'G6c_inventory_for_K4_identity': outcome(lambda: G2.check_inventory(dict(w['inv'], point_sha256=d4['point_sha256'],
                                                                                       custody_sha256=d4['custody_sha256']), d4))[0],
             '08e9ac0a_on_the_K3_point': str(srb_run(P['G2'], env=env_p, approved=[PRED['G2'][1], GPIN['G4']['sha256']])['blockers'])}
        want = {'inventory_4ca7f364': 'INVENTORY_PRODUCER_NOT_THE_G6_ENUMERATOR', 'eps_from_4_for_K3': 'EPS_COVERAGE_NOT_3_TO_182',
                'eps_from_3_for_K4_identity': 'EPS_COVERAGE_NOT_4_TO_182', 'G6c_inventory_for_K4_identity': 'INVENTORY_PRODUCER_NOT_B1_4CA7F364',
                '08e9ac0a_on_the_K3_point': 'INVENTORY_PRODUCER_NOT_B1_4CA7F364'}
        ok = all(want[k] in v for k, v in r.items())
        return ok, {k: v[:120] for k, v in r.items()}

    @case('G2-D1_non_S1_SRB_is_08e9ac0a_and_K4_format_checks_identical', 'DIFFERENTIAL')
    def _():
        pred = G2._predecessor()
        saved = pred.adapt_call_srb_rot
        pred.adapt_call_srb_rot = lambda *a, **k: 'PRED_08e9ac0a'
        try:
            sent = {n: G2.adapt_call_srb_rot(s, call_dir='/x', result={}, inventory={}, bundle_ref={}, state_input_ref={}, rows_input_ref={})
                    for n, s in [('row01', BASE)] + NON_S1}
        finally:
            pred.adapt_call_srb_rot = saved
        d4 = G3A.P.C.derive_details(spec=BASE)
        rec = eps_record_of(E['eps_pin'])
        recs = {'k3_record': rec, 'k4_record': dict(rec, shells=rec['shells'][1:], required_coverage_inverse_kpc=[4.0, 182.0])}
        res = {}
        for n, r in recs.items():
            r4 = dict(r, identity=d4['identity'], custody=d4['custody'], point_sha256=d4['point_sha256'])
            a_, b_ = outcome(lambda: G2.format_eps(r4, d4)), outcome(lambda: P['G2'].format_eps(r4, d4))
            res['format_eps/' + n] = (a_[0][:60], a_ == b_)
        for prod in (GPIN['G6C'], {'path': PRED['G6C'][0], 'sha256': PRED['G6C'][1]}):
            inv = dict(srb_world()['inv'], producer=prod, point_sha256=d4['point_sha256'], custody_sha256=d4['custody_sha256'])
            a_, b_ = outcome(lambda: G2.check_inventory(inv, d4)), outcome(lambda: P['G2'].check_inventory(inv, d4))
            res['check_inventory/' + prod['sha256'][:8]] = (a_[0][:60], a_ == b_)
        ok = all(v == 'PRED_08e9ac0a' for v in sent.values()) and all(v[1] for v in res.values())
        return ok, {'delegated': len(sent), 'K4_identity_checks': res}

    # ============================================================================================ G6: acceptance inventory
    def graph_result(spec, n_pass=2):
        d = details_of(spec) if C.s1_c3t_spec(spec) else G3A.P.C.derive_details(spec=spec)
        ids = [r_['id'] for r_ in d['row_contract']['rows']]
        stages = []
        exp = [('route_a', 'route_a'), ('route_a_tail_manifest', 'route_a_tail_manifest'), ('reference', 'reference'), ('body', 'body'),
               ('offset', 'offset'), ('fs_columns_00', 'columns_v001'), ('fs_columns_01', 'columns_v001'), ('fs_rotation', 'rotation_v001'),
               ('fs_feedback', 'feedback_v002'), ('rfs_columns_00', 'columns_v003'), ('rfs_columns_01', 'columns_v003')]
        for i in range(1, n_pass + 1):
            exp += [('le%d_columns_00' % i, 'columns_v005'), ('le%d_rotation' % i, 'rotation_v005'), ('le%d_column_mean' % i, 'column_mean_v004')]
            if i < n_pass:
                exp.append(('le%d_feedback' % i, 'feedback_v004'))
        for name, kind in exp:
            rec = {'name': name, 'kind': kind, 'executed': True, 'exit_code': 0, 'argv': []}
            if kind.startswith('columns_'):
                idx = list(range(72)) if name.startswith('le') else (list(range(36)) if name.endswith('_00') else list(range(36, 72)))
                cp = FX.json('graph/controls/' + FX.uniq(name) + '.json', {'radial_indices': idx})
                rec['argv'] = ['--controls', cp['path'], '--controls-sha256', cp['sha256']]
            stages.append(rec)
        p1 = [{'id': i, 'speed_km_s': 10.0 + j} for j, i in enumerate(ids)]
        p2 = [{'id': i, 'speed_km_s': 10.005 + j} for j, i in enumerate(ids)]
        delta = max(abs(a_['speed_km_s'] - b_['speed_km_s']) for a_, b_ in zip(p1, p2))
        return {'status': 'COMPLETED', 'valid': True, 'final_pass': 2, 'passes': [{'pass': 1, 'rows': p1}, {'pass': 2, 'rows': p2, 'max_abs_change_km_s': delta}],
                'rows': p2, 'stage_records': stages}

    @case('G6-P1_execution_graph_S1_validates_with_KS1_6d59f1d0_refuses_K3', 'MUST_PASS')
    def _():
        res = graph_result(C3T)
        a_ = G6A.validate_graph(spec=copy.deepcopy(C3T), result=res)
        b_ = G6A.PRED.validate_graph(spec=copy.deepcopy(C3T), result=res)
        ok = a_['ok'] is True and a_['point_sha256'] == DET['point_sha256'] and b_['ok'] is False and 'K4 cube required' in str(b_['blockers'])
        return ok, {'G6a': {k: a_.get(k) for k in ('ok', 'blockers', 'passes')}, '6d59f1d0': b_.get('blockers')}

    def verify_point_world(spec, K):
        d = details_of(spec) if C.s1_c3t_spec(spec) else G3A.P.C.derive_details(spec=spec)
        raw = copy.deepcopy(spec['numerics']['uv_tail'])
        cfg = U.normalize_config(raw)
        kept = U.kept_region('le_rotation', spec['numerics']['truncation'], K / U.KPC_M)
        g = U._grid(kept, cfg['outer'], cfg['quadrature'], cfg['domain']['R_eval_max_kpc'])
        dm = cfg['domain']
        rec = {'eps_certificate': raw['eps_certificate'], 'lo_certificate': raw['lo_certificate'], 'config_sha256': cfg['sha256'],
               'stage_kind': 'le_rotation', 'kept': kept, 'outer': cfg['outer'],
               'domain_m': {'R_eval_max_m': dm['R_eval_max_kpc'] * U.KPC_M, 'z_eval_max_m': dm['z_eval_max_kpc'] * U.KPC_M,
                            'z_src_max_m': dm['z_src_max_kpc'] * U.KPC_M},
               'jet_order': cfg['jet_order'], 'i1t': {'verdict': 'PASS'},
               'quadrature': {'order': cfg['quadrature']['order'], 'N_perp': int(len(g['kp'])), 'N_z_plus': int(len(g['kz']))},
               'gamma_eff': spec['physical']['common_scale_s'] * spec['physical']['gamma']}
        arrays = {k: g[k] / U.KPC_M for k in ('kp', 'kz', 'wkp', 'wz')}
        r = types.SimpleNamespace(profile={'galaxies': {'DDO154': d['geometry']['profile']}}, c_m_s=G6B.L.PR.CC.C, kpc_m=U.KPC_M,
                                  solar_mass_kg=1.98847e30, lib=U)
        p = types.SimpleNamespace(state=types.SimpleNamespace(record=rec, to_arrays=lambda: arrays))
        return r, p, d

    @case('G6-P2_evidence_S1_verify_point_wants_the_K3_production_grid_7044e131_refuses', 'MUST_PASS')
    def _():
        sf = E['spec_filled']
        r3, p3, d3 = verify_point_world(sf, 3)
        a_ = outcome(lambda: G6B.verify_point(sf, r3, p3, d3))
        b_ = outcome(lambda: G6B.PRED.verify_point(sf, r3, p3, d3))
        r4, p4, _d = verify_point_world(sf, 4)
        c_ = outcome(lambda: G6B.verify_point(sf, r4, p4, d3))
        ok = (a_[0] == 'PASS' and a_[1]['exact_production_nodes_verified'] is True and a_[1]['certificate_slots_bound'] is True
              and p3.state.record['quadrature']['N_perp'] == 20720 and 'kept/outer mismatch' in b_[0] and 'kept/outer mismatch' in c_[0])
        return ok, {'G6b_K3_state': a_[0], 'N_perp': p3.state.record['quadrature']['N_perp'], '7044e131_K3_state': b_[0][:90],
                    'G6b_K4_state_at_K3_point': c_[0][:90]}

    @case('G6-P3_enumerator_S1_routes_to_G6c_code_and_names_G6c_every_other_spec_4ca7f364', 'MUST_PASS')
    def _():
        saved = (G6C.D.consumed_states, G6C.PRED.D.consumed_states)

        def boom(**kw):
            raise ValueError('SENTINEL_DISCOVERY_STOP (test seam)')
        G6C.D.consumed_states = G6C.PRED.D.consumed_states = boom
        try:
            a_ = G6C.consumed_states(spec=copy.deepcopy(C3T), result={}, call_dir='/nonexistent')
            b_ = G6C.consumed_states(spec=copy.deepcopy(BASE), result={}, call_dir='/nonexistent')
        finally:
            G6C.D.consumed_states, G6C.PRED.D.consumed_states = saved
        ok = (a_['producer'] == GPIN['G6C'] and b_['producer'] == pin_file(PRED['G6C'][0]) and a_['complete'] is False
              and 'SENTINEL' in str(a_['blockers']) and 'SENTINEL' in str(b_['blockers']) and a_['schema'] == b_['schema'])
        return ok, {'S1_producer': a_['producer']['path'][-45:], 'K4_producer': b_['producer']['path'][-45:]}

    @case('G6-D1_non_S1_inventory_entries_are_the_predecessor_objects_and_K4_graph_identical', 'DIFFERENTIAL')
    def _():
        targets = [(G6A.PRED, 'expected_stages'), (G6A.PRED, 'validate_graph'), (G6B.PRED, 'assemble_current'),
                   (G6B.PRED, 'export_lo_source'), (G6B.PRED, 'verify_point'), (G6B.PRED, 'verify_occurrence'), (G6C.PRED, 'consumed_states')]
        saved = [(m, n, getattr(m, n)) for m, n in targets]
        for m, n in targets:
            setattr(m, n, (lambda tag: lambda *a, **k: tag)('PRED_' + n))
        try:
            res = {}
            for name, s in [('row01', BASE), ('row29', specs[29])] + NON_S1:
                res[name] = [G6A.expected_stages(s, 2), G6A.validate_graph(spec=s, result={}), G6B.assemble_current(s, None, None, None),
                             G6B.export_lo_source(s, None, None, None, None), G6B.verify_point(s, None, None, None),
                             G6B.verify_occurrence(s, None, None, None), G6C.consumed_states(spec=s, result={}, call_dir='/x')]
        finally:
            for m, n, f_ in saved:
                setattr(m, n, f_)
        names = ['PRED_' + n for _m, n in targets]
        res4 = graph_result(BASE)
        a_, b_ = G6A.validate_graph(spec=copy.deepcopy(BASE), result=res4), P['G6A'].validate_graph(spec=copy.deepcopy(BASE), result=res4)
        same_graph = canonical(a_) == canonical(b_) and a_['ok'] is True
        ast_same = {fn: ast.dump(fn_node(GPIN['G6B']['path'], fn)) == ast.dump(fn_node(PRED['G6B'][0], fn))
                    for fn in ('compute_i1t', 'verify_gas', 'verify_product', '_approved')}
        ok = all(v == names for v in res.values()) and same_graph and all(ast_same.values())
        return ok, {'delegated_specs': len(res), 'K4_graph_identical_to_6d59f1d0': same_graph, 'spec_free_functions_AST_identical': ast_same}

    # ============================================================================================ KS6': inventory pin by identity
    @case('K6-P1_KS6pp_adapter_inventory_producer_by_identity', 'MUST_PASS')
    def _():
        d4 = G3A.P.C.derive_details(spec=BASE)
        base_inv = srb_world()['inv']
        inv3 = dict(base_inv, schema=AD6.INVENTORY_SCHEMA)
        inv4 = dict(inv3, producer={'path': PRED['G6C'][0], 'sha256': PRED['G6C'][1]}, point_sha256=d4['point_sha256'],
                    custody_sha256=d4['custody_sha256'])
        a_ = outcome(lambda: AD6.check_inventory(inv3, DET))[0]
        b_ = outcome(lambda: AD6.check_inventory(inv4, d4))[0]
        return a_ == 'PASS' and b_ == 'PASS', {'S1_G6c': a_, 'K4_4ca7f364': b_}

    @case('K6-F1_KS6pp_adapter_crossed_inventory_producers_refused', 'MUST_FAIL')
    def _():
        d4 = G3A.P.C.derive_details(spec=BASE)
        inv3 = dict(srb_world()['inv'], producer={'path': PRED['G6C'][0], 'sha256': PRED['G6C'][1]})
        inv4 = dict(srb_world()['inv'], point_sha256=d4['point_sha256'], custody_sha256=d4['custody_sha256'])
        a_ = outcome(lambda: AD6.check_inventory(inv3, DET))[0]
        b_ = outcome(lambda: AD6.check_inventory(inv4, d4))[0]
        w1 = outcome(lambda: W['KS6AD'].check_inventory(dict(srb_world()['inv']), DET))[0]
        ok = 'INVENTORY_PRODUCER_NOT_THE_G6_ENUMERATOR' in a_ and 'INVENTORY_PRODUCER_NOT_B1_4CA7F364' in b_ and 'INVENTORY_PRODUCER_NOT_B1_4CA7F364' in w1
        return ok, {'S1_with_4ca7f364': a_, 'K4_with_G6c': b_, 'wave1_KS6_with_G6c_S1_inventory': w1}

    @case('K6-D1_KS6pp_non_S1_entries_are_211a3220_and_5ff464cc_and_K4_inventory_checks_identical', 'DIFFERENTIAL')
    def _():
        pa, ph = AD6._predecessor(), H6._predecessor()
        sa, sh = pa.adapt_call_lo, ph.accept_call
        pa.adapt_call_lo = lambda *a, **k: 'PRED_211a3220'
        ph.accept_call = lambda **k: ('PRED_5ff464cc', None)
        try:
            res = {n: [AD6.adapt_call_lo(s, call_dir='/x', result={}, inventory={}, bundle_ref={}, state_inputs={}, out_root='/x'),
                       H6.accept_call(call_dir='/x', spec=s, deps={}, policy={}, records_dir='/x')[0]] for n, s in [('row01', BASE)] + NON_S1}
        finally:
            pa.adapt_call_lo, ph.accept_call = sa, sh
        d4 = G3A.P.C.derive_details(spec=BASE)
        cmp_ = {}
        for tag, prod in (('4ca7f364', {'path': PRED['G6C'][0], 'sha256': PRED['G6C'][1]}), ('G6c', GPIN['G6C']), ('v010', {'path': '/x', 'sha256': 'e' * 64})):
            inv = dict(srb_world()['inv'], producer=prod, point_sha256=d4['point_sha256'], custody_sha256=d4['custody_sha256'])
            a_, b_ = outcome(lambda: AD6.check_inventory(inv, d4)), outcome(lambda: W['KS6AD'].check_inventory(inv, d4))
            cmp_[tag] = (a_[0][:60], a_ == b_)
        ok = all(v == ['PRED_211a3220', 'PRED_5ff464cc'] for v in res.values()) and all(v[1] for v in cmp_.values())
        return ok, {'delegated': len(res), 'K4_identity_inventory_checks_equal_KS6': cmp_}

    @case('K6-P2_KS6pp_handoff_S1_path_wants_the_KS6pp_adapter_and_G6b_evidence', 'MUST_PASS')
    def _():
        fn = H6.load_pinned(H6.LO_ADAPTER_KS6, 'gwt_h6_lo_adapter_ks6pp').adapt_call_lo
        good = H6.lo_adapter_problem({'pins': {'lo_adapter': dict(H6.LO_ADAPTER_KS6)}, 'lo_adapter': fn}, H6.LO_ADAPTER_KS6)
        old = H6.lo_adapter_problem({'pins': {'lo_adapter': dict(W['KS6HO'].LO_ADAPTER_KS6)}, 'lo_adapter': fn}, H6.LO_ADAPTER_KS6)
        ok = (good is None and 'LO_ADAPTER_PIN_NOT_A138' in str(old) and H6.B1_EVIDENCE_G6 == GPIN['G6B']
              and H6.LO_ADAPTER_KS6['sha256'] == GPIN['KS6AD2']['sha256'])
        return ok, {'KS6pp_adapter': good, 'wave1_KS6_adapter_pin': old}

    # ============================================================================================ KS3'/KS4' differentials (rows 1-31)
    @case('R-D1_check_gq_rows_1_31_identical_to_KS3_and_c3v004_rule', 'DIFFERENTIAL')
    def _():
        rs = gq_runs()[0]
        recs = {'g3_k3': rs, 'g3b_k3': GQ.get('g3b', rs), 'k4_2832': dict(rs, producer=C.canonical_pin('gq_producer')),
                'partial': dict(rs, nodes_tested=10)}
        same = {n: R3.check_gq(r, r['point_sha256'], r['custody_sha256']) == W['KS3R'].check_gq(r, r['point_sha256'], r['custody_sha256'])
                for n, r in recs.items()}
        return all(same.values()), same

    # ============================================================================================ summary
    n = len(RESULTS)
    np_ = sum(r['passed'] for r in RESULTS)
    kinds = {}
    for r in RESULTS:
        k = kinds.setdefault(r['kind'], {'n': 0, 'passed': 0})
        k['n'] += 1
        k['passed'] += r['passed']
    summary = {'schema': 'KS_GWAVE_TEST_RESULTS_C2V001', 'gw_dir': GW, 'run_dir': run, 'n': n, 'passed': np_, 'by_kind': kinds,
               'failed': [r['id'] for r in RESULTS if not r['passed']], 'fence_refused_opens': FENCE['refused'],
               'gwave_modules': GPIN, 'wave1_modules': KPIN, 'predecessors': {k: {'path': p_, 'sha256': h} for k, (p_, h) in PRED.items()},
               'libraries': {k: {'path': p_, 'sha256': h} for k, (p_, h) in LIBS.items()},
               'suite': pin_file(os.path.realpath(__file__)), 'python': sys.version.split()[0], 'numpy': np.__version__,
               'flags': {'isolated': sys.flags.isolated, 'dont_write_bytecode': sys.flags.dont_write_bytecode},
               'background_qos': os.getpriority(4, 0) == 1, 'seconds': round(time.time() - t0, 1), 'results': RESULTS,
               'synthetic_fixture': SYN}
    with open(os.path.join(run, 'TEST_RESULTS_GWAVE_C2V001.json'), 'xb') as f:
        f.write(json.dumps(summary, sort_keys=True, indent=1, default=str).encode() + b'\n')
    print(json.dumps({'n': n, 'passed': np_, 'by_kind': kinds, 'failed': summary['failed'], 'seconds': summary['seconds'],
                      'fence_refused': len(FENCE['refused'])}))
    return 0 if np_ == n else 1


if __name__ == '__main__':
    sys.exit(main())
