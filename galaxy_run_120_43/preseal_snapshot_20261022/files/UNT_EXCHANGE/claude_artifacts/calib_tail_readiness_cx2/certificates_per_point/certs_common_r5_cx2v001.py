"""Shared helpers for the V007 numerics-certificate replays (tail_scheme_impl_c2/certificates_v001).  READ-ONLY on every
input; writes only under certificates_v001/ (callers use exclusive create).  numpy only.

Symbol path (EPS, LO): the reviewed QINF evaluator f58de0dc (qinf_dependence_c2/tools/qinf_eval_v001.py) is a top-level
script that writes into its own out/ (so it is NOT executed here).  Its evaluation route is reproduced verbatim: the A2
pooled grid from the GRID_INVENTORY npz, cross-checked bitwise against the pinned source npz 2e3a36d8, the anchor point
(s0, gamma/Eref, ell_F) read exactly as qinf_eval does, and lwr_common_v001.Binder (the batched transcription that
f58de0dc validates against the pinned modules).  repro_qinf_anchor() re-derives the anchor's Q_lines_13dirs from
QINF_EVAL_V001.json (f58de0dc's own output, 50aab701) and must reproduce them exactly; that ties this path to f58de0dc.
"""
import hashlib
import importlib.util
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CERT = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v001')
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
RUNS = UPC / 'CLAUDE2/runs'
MODULE = ART / 'tail_scheme_impl_c2/driver_r5/module'
QINF = ART / 'qinf_dependence_c2'
LWR = ART / 'long_wavelength_response_c2'
C = 299792458.0
G = 6.67430e-11
THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')

PINS = {
    'qinf_evaluator': (QINF / 'tools/qinf_eval_v001.py', 'f58de0dcc67cc4097b4604dc96b640fbf8aaee0520d0478e214673b931eb3346'),
    'qinf_eval_output': (QINF / 'out/QINF_EVAL_V001.json', '50aab701f10de9a31b315d8d82b9470cd4938cf8ff4bd874a1832c89edfad686'),
    'inverse_cache': (UPC / 'helpers/recovered_packet_audit/owned_scalar_lapse_inverse_cache_v001.py',
                      '7b9816aea218d638c2eece184df22e29ca18b68547f3d04193780c2eff96a529'),
    'inventory_npz': (LWR / 'out/GRID_INVENTORY_V001.npz', '1833cca4b27edafde5e1d27f511b5bc7843f5447eb4d0faebbdeeb98b790d20d'),
    'A2_npz': (UPC / 'CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz',
               '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'),
    'seed_scan_result': (UPC / 'CLAUDE2/runs/A2_SEED_SCAN_G2_RUN_V001/result.json', None),
    'lwr_common': (LWR / 'tools/lwr_common_v001.py', None),
    'uvt_lapse': (MODULE / 'owned_uv_tail_lapse_v002.py', '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'),
    'uvt_roster': (MODULE / 'uv_tail_source_roster_c2v001.py', '4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2'),
    'uvt_jn': (MODULE / 'posix_libm_bessel_jn_provider_c2v001.py', 'd6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171'),
    'profile': (UPC / 'CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json', 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'),
    'row_binding': (UPC / 'CODEX1/DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json',
                    'f42c7c657cd9b8bcef6b88e980918ff2570b1fc0a5480784d8bf3b8bb2a3c600'),
    'prereg_v005': (ART / 'kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json',
                    'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174'),
    'addendum_v004_frozen': (UPC / 'CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md',
                             '487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b'),
    'ngc_T120L_operator': (ART / 'ngc_kgrid_fidelity_c2/phase23/ops/T120L_hovr/OPERATOR.json',
                           'e6453d520f902e77da77e49b8f8d1cdbed84639f11ed6cc661943553741b2af4'),
}
R3 = {'C2R3': ('KMAX_A2F10_C2R3_D7R3_RUN_V001', '1f6b32a4edd0dd28438536165bdb10e13c8125eb5ccafb60ceb17315eba8c169', 2.0),
      'C3R3': ('KMAX_A2F10_C3R3_D7R3_RUN_V001', 'c9c802f44854d4f41f9e119707235899aba75a8bd42e89c19983f9ca9b817674', 3.0),
      'C4R3': ('KMAX_A2F10_C4R3_D7R3_RUN_V001', 'aac01962dc7bf08a7486179bc5674af520f7ea38d73b004154cdd2ff25fa8dee', 4.0)}
ADDENDUM_V005_CITED = str(UPC / 'CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
GATE_SCHEMA = 'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002'


def require_env():
    bad = [k for k in THREAD_ENV if os.environ.get(k) != '1']
    if bad:
        raise SystemExit('single-thread BLAS env required: ' + ','.join(bad))


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def pin(name):
    p, want = PINS[name]
    got = sha(p)
    if want is not None and got != want:
        raise SystemExit('PIN MISMATCH %s %s' % (name, p))
    return {'path': str(p), 'sha256': got}


def load_module(path, name, want=None):
    if want is not None and sha(path) != want:
        raise SystemExit('module pin mismatch ' + str(path))
    spec = importlib.util.spec_from_file_location('certs_' + name, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def write_new(path, obj):
    path = Path(path)
    if HERE not in path.resolve().parents:
        raise SystemExit('refusing to write outside r5 certificate directory: %s' % path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(obj, indent=1, allow_nan=False, sort_keys=False) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(raw)
    return hashlib.sha256(raw).hexdigest()


def producer(script_path):
    return {'path': str(Path(script_path).resolve()), 'sha256': sha(script_path)}


# ------------------------------------------------------------------ tail module (pinned)
def uvt_modules():
    sys.path.insert(0, str(MODULE))
    U = load_module(PINS['uvt_lapse'][0], 'uvt_lapse', PINS['uvt_lapse'][1])
    RS = load_module(PINS['uvt_roster'][0], 'uvt_roster', PINS['uvt_roster'][1])
    PV = load_module(PINS['uvt_jn'][0], 'uvt_jn', PINS['uvt_jn'][1])
    return U, RS, PV


def uvt_config(U, *, K_big, M_s=64, w_perp=0.05, w_z=0.02, order=8, R_eval=14.2, z_eval=35.0, z_src=32.0):
    """The production DDO uv_tail block of the V007 templates (C4T spec) with the outer cylinder K_big varied; certificates
    are the TEST_ONLY sentinel (replay states are production_admissible false by IA6, as required for a replay)."""
    return U.normalize_config({
        'enabled': True, 'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': float(K_big)}, 'source_rule': 'continuum_v001',
        'gas': {'interp': 'lagrange3_s_gl4', 'M_s': int(M_s)},
        'stars': {'segment_rule': 'max16_ceil_kdr_plus8', 'tail_rule': 't_panels_40a_phase1p5_gl12'},
        'quadrature': {'order': order, 'w_perp_max_inverse_kpc': w_perp, 'w_z_max_inverse_kpc': w_z},
        'domain': {'R_eval_max_kpc': R_eval, 'z_eval_max_kpc': z_eval, 'z_src_max_kpc': z_src},
        'asymptote': 'EH_exact_minus_quarter', 'lapse_only': True,
        'jet_order': {'route_a': 1, 'route_b': 2, 'ngc_eval': 1}, 'lambda_scale': 1.0,
        'eps_certificate': U.TEST_ONLY_CERT, 'lo_certificate': U.TEST_ONLY_CERT})


def argmap(req):
    a = json.loads(Path(req).read_text())['argv']
    return {a[i]: a[i + 1] for i in range(len(a) - 1) if a[i].startswith('--')}


class SavedR3:
    """Saved KMAX R3 state (read-only); same reading as module tests/saved_states_v001.py and CHECK indep tools."""

    def __init__(self, cid):
        name, want, K = R3[cid]
        self.cid = cid; self.K = K; self.run = RUNS / name
        self.result_sha = sha(self.run / 'result.json')
        fin = json.loads((self.run / 'finish.json').read_text())
        if self.result_sha != want or fin['result_sha256'] != want:
            raise SystemExit('R3 result pin ' + cid)
        res = json.loads((self.run / 'result.json').read_text())
        last = res['passes'][-1]
        self.rows = np.array([r['speed_km_s'] for r in last['rows']], float)
        self.row_ids = [r['id'] for r in last['rows']]
        self.field = Path(last['field']); self.rot = Path(last['rotation'])
        self.src_rot = Path(argmap(self.field.parent / 'request.json')['--rotation-directory'])
        self.gamma = float(res['identity']['route_a']['custody']['physical']['gamma'])
        self.ni = json.loads((self.run / 'inputs/seed_c2v001.json').read_text())['numerical_inputs']
        self.checkpoint = Path(res['identity']['route_a']['checkpoint'])

    def source_rotation_arrays(self):
        with np.load(self.src_rot / 'rotation_base_arrays.npz', allow_pickle=False) as f:
            return {k: f[k].copy() for k in ('rho0', 'volume_weights_m3', 'radial_nodes_m', 'z')}

    def packet_waves(self):
        with np.load(self.field / 'refreshed_prepared.npz', allow_pickle=False) as f:
            return f['wavevectors'].copy()

    def gas_packet(self):
        with np.load(self.field / 'gas_source_feedback.npz', allow_pickle=False) as f:
            return f['new_gas_fourier_J'][:, 0, 0].copy()

    def star_packet(self):
        stj = json.loads((self.checkpoint / 'iteration_0004/START.json').read_text())['fixed_source_fourier_J']
        if sha(self.checkpoint / stj['blob']) != stj['file_sha256']:
            raise SystemExit('star blob sha')
        return np.load(self.checkpoint / stj['blob'], allow_pickle=False)[:, 0, 0]


def row_radii_and_tau():
    b = json.loads(Path(pin('row_binding')['path']).read_text())
    pre = json.loads(Path(pin('prereg_v005')['path']).read_text())
    ids = [q['id'] for q in b['query_rows']]
    if ids != pre['row_ids']:
        raise SystemExit('row order')
    return ids, np.array([q['radius_m'] for q in b['query_rows']], float), np.array(pre['tau_km_s'], float)


def i1t_on_state(RS, PV, case, prof, s_edges, units, jn, nodes=4096, seed=20261018):
    """I1-T as module test (d) D0 / v010 stages: module ring transform of the represented gas rings + GL4 star rings vs the
    saved packet sources at 4096 seeded packet nodes (<= 1e-12 else UV_TAIL_SOURCE_MISMATCH)."""
    arr = case.source_rotation_arrays()
    waves = case.packet_waves(); rng = np.random.default_rng(seed)
    idx = np.sort(rng.choice(len(waves), nodes, replace=False))
    rho = arr['rho0']; vol = arr['volume_weights_m3']; z = arr['z']
    m = np.sum(vol * rho, axis=1)
    Rg = np.repeat(arr['radial_nodes_m'], z.shape[2]); zg = z[:, 0, :].reshape(-1); mg = m.reshape(-1)
    gasT = RS.packet_transform(dict(R=Rg, z=zg, m=mg), waves[idx], 'feedback_ring_j0_v004', c_m_s=C, j0=jn.j0)
    sr = RS.stars_gl4_rings(prof, 'DDO154', kpc_m=units['kpc_m'], solar_mass_kg=units['solar_mass_kg'],
                            gauss_order=case.ni['source_gauss_order'])
    starT = RS.packet_transform(sr, waves[idx], 'prep_analytic_j0', c_m_s=C, j0=jn.j0)
    gasJ = case.gas_packet()[idx]; starJ = case.star_packet()[idx]
    return RS.check_represented(gasT + starT, gasJ + starJ, 'stars prep_analytic_j0 + gas feedback_ring_j0_v004', rtol=1e-12)


# ------------------------------------------------------------------ symbol (QINF evaluator route, f58de0dc)
def qinf_binder():
    """Exactly qinf_eval_v001.py's A2 grid + anchor point -> lwr_common Binder.  Returns (L, B, info)."""
    pins = {k: pin(k) for k in ('qinf_evaluator', 'qinf_eval_output', 'inventory_npz', 'A2_npz', 'seed_scan_result', 'lwr_common')}
    sys.path.insert(0, str(LWR / 'tools'))
    L = load_module(PINS['lwr_common'][0], 'lwr_common')
    inv = np.load(PINS['inventory_npz'][0])
    g = inv['A2_pooled__grid']; Cb = inv['A2_pooled__Cbar']; mu = inv['A2_pooled__mubar']
    with np.load(PINS['A2_npz'][0]) as z:
        sg, sC, smu = z['source_hessian_grid'].copy(), z['background_C'].copy(), z['background_mu'].copy()
    grid_check = dict(grid_equal_pinned_source=bool(np.array_equal(g, sg)), background_equal_pinned_source=bool(np.array_equal(Cb, sC) and np.array_equal(mu, smu)))
    if not all(grid_check.values()):
        raise SystemExit('A2 grid/background not equal to pinned source')
    scan = json.loads(Path(PINS['seed_scan_result'][0]).read_text())
    EB = scan['base']['Eref_J']
    assert EB == L.ANCHOR_UNSCALED['Eref_J'] and scan['base']['ell_F_m'] == L.ANCHOR_UNSCALED['ell_F_m']
    s0 = L.ANCHOR_UNSCALED['common_scale_s']; ge0 = L.ANCHOR_UNSCALED['gamma'] / EB; ell0 = L.ANCHOR_UNSCALED['ell_F_m']
    Eeff = s0 * EB; geff = s0 * ge0 * EB
    B = L.Binder(g, Cb, mu, Eref=Eeff, ell=ell0, gam=geff)
    info = dict(pins=pins, grid_check=grid_check, point='anchor_F10', s=s0, gamma_over_Eref=ge0, ell_F_m=ell0, Eref_eff_J=Eeff,
                gamma_eff=geff, grid_array_sha256=hashlib.sha256(np.ascontiguousarray(g).tobytes()).hexdigest(),
                Cbar=Cb.tolist(), mubar=mu.tolist())
    return L, B, info, (g, Cb, mu)


def repro_qinf_anchor(L, B):
    """Re-derive QINF_EVAL_V001.json points[anchor_F10].Q_lines_13dirs (f58de0dc's lines loop, verbatim arithmetic)."""
    ref = json.loads(Path(PINS['qinf_eval_output'][0]).read_text())['points'][0]
    assert ref['point'] == 'anchor_F10'
    dirs = {k: np.asarray(v, float) / np.linalg.norm(v) for k, v in L.DIRS.items()}
    QN = lambda T, kv: (T * np.sum(kv * kv, axis=1) * C ** 4 / (4 * np.pi * G))
    out = {}; worst = 0.0
    for kval in [0.3, 1.0, 2.0, 10.0, 100.0, 1000.0]:
        kv = np.stack([d * kval / L.KPC for d in dirs.values()])
        T, cond = B.T_vec(kv, want_cond=True)
        q = QN(T, kv).real
        mine = dict(Q_dir_mean=float(q.mean()), Q_dir_min=float(q.min()), Q_dir_max=float(q.max()), min_cond_inv=float(cond.min()))
        theirs = ref['Q_lines_13dirs'][str(kval)]
        d = {k: abs(mine[k] - theirs[k]) / abs(theirs[k]) for k in mine}
        worst = max(worst, max(d.values()))
        out[str(kval)] = dict(mine=mine, qinf_eval=theirs, rel_diff=d)
    return dict(lines=out, max_rel_diff=worst, bitwise_equal=bool(worst == 0.0), gamma_eff_qinf=ref['gamma_eff'],
                gamma_eff_here=B.gam, gamma_equal=bool(ref['gamma_eff'] == B.gam))


def q_of(B, kv_m):
    """q(k) = 4 gamma_eff |k|^2 T(k) (T = lapse transfer, Binder.T_vec); complex array."""
    kv_m = np.atleast_2d(kv_m)
    T = B.T_vec(kv_m)
    return 4.0 * B.gam * np.sum(kv_m * kv_m, axis=1) * T


def full_response(B, kv_m, chunk=4000):
    """All 10 fields of x = -K^-1 e_n (per unit lapse source density; x[0] = T), same algebra as Binder.T_vec."""
    kv = np.atleast_2d(np.asarray(kv_m, float))
    out = np.empty((kv.shape[0], 10), complex)
    for lo in range(0, kv.shape[0], chunk):
        hi = min(lo + chunk, kv.shape[0])
        F, kr = B.F_of(kv[lo:hi])
        tot = B.native_from_F(F) + B.eh(kr)
        e0 = np.zeros((hi - lo, 10, 1), complex); e0[:, 0, 0] = 1.0
        out[lo:hi] = np.linalg.solve(tot / B.volume, -e0)[:, :, 0]
    return out


# ------------------------------------------------------------------ declared direction sets (EPS)
def _family(base):
    """All signed permutations of `base`, normalized, one representative per +-pair (first nonzero component > 0)."""
    import itertools
    seen = set(); out = []
    for p in itertools.permutations(base):
        for sg in itertools.product((1, -1), repeat=3):
            v = tuple(a * s for a, s in zip(p, sg))
            if all(x == 0 for x in v):
                continue
            first = next(x for x in v if x != 0)
            if first < 0:
                v = tuple(-x for x in v)
            if v not in seen:
                seen.add(v); out.append(v)
    return sorted(out, reverse=True)


def direction_sets(L):
    """level 0 (base, 13 + 13): the 13 lattice-symmetric directions (lwr_common DIRS = cubic-lattice neighbours up to sign)
    + 13 midpoint directions M13 = the 12 axis/body-diagonal midpoints (2,1,1)-family + (1,2,3).
    level 1 (refined, 26 + 26): level 0 + 26 new midpoints: (2,1,0)-family (12) + (3,2,1) + (3,1,1)-family (12) + (1,3,2).
    level 2/3 (further refinements, used only if a shell fails): + 52 / + 104 Fibonacci-hemisphere directions."""
    lat = [np.asarray(v, float) for v in L.DIRS.values()]
    m13 = [np.asarray(v, float) for v in _family((2, 1, 1))] + [np.array([1.0, 2.0, 3.0])]
    n26 = [np.asarray(v, float) for v in _family((2, 1, 0))] + [np.array([3.0, 2.0, 1.0])] + \
          [np.asarray(v, float) for v in _family((3, 1, 1))] + [np.array([1.0, 3.0, 2.0])]
    assert len(lat) == 13 and len(m13) == 13 and len(n26) == 26

    def fib(n, offset):
        i = np.arange(n) + 0.5 + offset
        zc = 1 - i / (n + offset + 0.5)          # hemisphere z in (0, 1)
        r = np.sqrt(np.maximum(0.0, 1 - zc * zc)); th = math.pi * (3 - math.sqrt(5)) * i
        return [np.array([r[j] * math.cos(th[j]), r[j] * math.sin(th[j]), zc[j]]) for j in range(n)]
    lv0 = lat + m13
    lv1 = lv0 + n26
    lv2 = lv1 + fib(52, 0)
    lv3 = lv2 + fib(104, 0.25)
    norm = lambda S: np.stack([v / np.linalg.norm(v) for v in S])
    return {0: norm(lv0), 1: norm(lv1), 2: norm(lv2), 3: norm(lv3)}


PER_DECADE = {0: 64, 1: 128, 2: 256, 3: 512}


def shell_k(lo, hi, per_decade):
    """|k| samples of one shell [lo, hi] (1/kpc): both endpoints + every log-grid point 10^(j/n) strictly inside."""
    j0 = math.floor(math.log10(lo) * per_decade); j1 = math.ceil(math.log10(hi) * per_decade)
    inner = [10 ** (j / per_decade) for j in range(j0, j1 + 1)]
    inner = [x for x in inner if lo < x < hi]
    return np.array([lo] + inner + [hi], float)
