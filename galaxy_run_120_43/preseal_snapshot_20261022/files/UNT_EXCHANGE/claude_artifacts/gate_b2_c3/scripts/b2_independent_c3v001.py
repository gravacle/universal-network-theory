"""Claude3 gate B2 (dispatch 0597), PATH 2 = INDEPENDENT Cartesian tensor-GL static rows on the saved C2R3/C3R3/C4R3 le3 states.

Imports NO tail library: not owned_uv_tail_lapse_*, not uv_tail_source_roster_*, not the posix_libm Jn provider, not any
route-A/route-B stage or binding, not the module lane's independent_tail_c2v001, not Claude4's b3 tools.  numpy only, own J0
(trapezoidal integral representation), own source transforms, own quadrature, own rotation-law increment.  The only code
loaded is the UNCHANGED observation pipeline that turns rotation into rows (column-mean v004 L223-227 calls it): the pinned
observation module galaxy_hi_observation_forward_v001 (8e30897e) and adapter owned_column_mean_streaming_observation_v002
(6790e28e); libm j0 (ctypes) is used ONLY as a cross-check of the own J0, never in a result.

Definition implemented (TAIL_SCHEME_DESIGN_V001 sec 1.1/1.3 kept by V002 sec 1.1/1.3; R1 B2):
  t(x) = lambda * int_D T_inf(k) S_T(k) e^{ik.x} d^3k/(2pi)^3,  T_inf = 1/(4 gamma_eff |k|^2),  lambda = 1,
  D = box(12) \\ cube(K) = {max(|kx|,|ky|,|kz|) <= 12 /kpc} minus {max(|kx|,|ky|,|kz|) <= K}, K = 2/3/4 for C2R3/C3R3/C4R3.
  S_T = -c^2 [ P_*(kp) V(kz) + sum_i P_i(kp) sigma_i(kz) ]  (continuum_v001):
    stars  P_*(kp) = 2 pi int_0^inf Sigma(R) J0(kp R) R dR, Sigma of the registered profile f5becd45 (constant core, linear
           between nodes, exponential tail; forward_v002 L43-58 definition re-typed here), V = x/sinh x, x = pi h |kz|;
    gas    sigma_i(kz) = sum_l m_il e^{-i kz z_il} / (2 pi w_i), m_il = sum_phi vol*rho0 of the le2 rotation the le2 feedback
           transformed (the source the le3 field carries), w_i = ds*w_GL4/4 the column's int R dR weight;
           P_i(kp) = int_{annulus} pi J0(kp sqrt s) L_i(s) ds, L_i the cubic Lagrange basis in s on the annulus' 4 GL4 nodes
           (integrated here in R with my own Gauss-Legendre nodes, not the production's M_s nodes in s).
  Quadrature: full Cartesian tensor GL in (kx, ky, kz) over [-12,12]^3, panel breaks {0, +-2, +-3, +-4, +-12} /kpc, uniform
  panels of width <= w, order o; the cube C removed by masking every node with |kx|,|ky|,|kz| <= K (breaks at +-K, so no
  node is on the boundary).  NO symmetry reduction: every node of the full box is summed with its own phase; both signs of
  kz are summed and the real part is taken at the end (the imaginary part is reported).  The axisymmetric radial factors
  P(kp) are evaluated once per distinct value of kx^2 + ky^2 (memoization of identical arguments; every node still summed).
  16 azimuths phi_j = 2 pi j / 16 (rotation v005 L281 `phi=2*np.pi*j/NPHI`).  At every le3 column node (R_i, phi_j, z_il):
  value t and radial derivative t_R = d/dR = (cos phi, sin phi).grad, means over the 16 azimuths.
Static row quantity (the production's, rotation v005 L281-292 + rotation law + column mean v004):
  PR = c^2 (g_R + t_R)/(1 + f0 + t) per azimuth (L289), pr = mean_j PR (L292); the rotation law (owned_free_surface_rotation
  v001 e1b354ec) is linear in pr: Omega^2 = (C_R - h k/gamma)/R, C_R = ((gamma-1)Sigma_R + k Sigma + B)/A, B = sum w rho/h pr,
  so Omega^2_ON = Omega^2_saved + sum_l w rho/h dpr / (A R).  dpr uses the saved le3 per-azimuth kept field f0 and g_R
  (rotation arrays full_fields_complex / full_gradient_complex) with the 16-azimuth means of my t and t_R in the O(1e-8)
  denominator (reported: the purely linear dpr = c^2 <t_R>_16 too).  Rows: the pinned adapter exactly as column mean v004
  L208-227 (speed = R Omega, weights = col weights_m * rho0 * HI ratio).
Usage:
  python3 -I -B b2_independent_c3v001.py table  W ORDER NGASR STARMULT TAG [discrete]   -> out/path2/TABLE_<TAG>.npz/.json
  python3 -I -B b2_independent_c3v001.py state  STATE TAG [groups]                      -> out/path2/IND_<STATE>_<TAG>.npz/.json
"""
import ctypes
import ctypes.util
import hashlib
import importlib.util
import json
import math
import os
import resource
import sys
import time
from pathlib import Path

import numpy as np

GATE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3')
OUT = GATE / 'out/path2'
ROOT = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
RUNS = ROOT / 'CLAUDE2/runs'
CODEX1 = ROOT / 'CODEX1'
HR = ROOT / 'helpers/recovered_packet_audit'
PINS = {
    'profile': (CODEX1 / 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json', 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'),
    'binding': (CODEX1 / 'DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json', 'f42c7c657cd9b8bcef6b88e980918ff2570b1fc0a5480784d8bf3b8bb2a3c600'),
    'observation': (HR / 'galaxy_hi_observation_forward_v001.py', '8e30897e875a619b132ba07e93459333cfd9302bbe2fc98d9a2ff0a2ec6d815d'),
    'adapter': (HR / 'owned_column_mean_streaming_observation_v002.py', '6790e28eb6631c0144f2efda26071a5933f47f7bda7d0c15d3b81e3581cc548c'),
    'forward_v002': (HR / 'galaxy_baryonic_source_forward_v002.py', 'e9be043b46790e3493f4e427fb483a98a5665f004dfac287d5758afce0ac96ad'),
}
STATES = {'C2R3': ('KMAX_A2F10_C2R3_D7R3_RUN_V001', '1f6b32a4edd0dd28438536165bdb10e13c8125eb5ccafb60ceb17315eba8c169', 2.0),
          'C3R3': ('KMAX_A2F10_C3R3_D7R3_RUN_V001', 'c9c802f44854d4f41f9e119707235899aba75a8bd42e89c19983f9ca9b817674', 3.0),
          'C4R3': ('KMAX_A2F10_C4R3_D7R3_RUN_V001', 'aac01962dc7bf08a7486179bc5674af520f7ea38d73b004154cdd2ff25fa8dee', 4.0)}
CL = 299792458.0
KOUT = 12.0
BREAKS = (-12.0, -4.0, -3.0, -2.0, 0.0, 2.0, 3.0, 4.0, 12.0)
NPHI = 16
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')
FORBIDDEN = ('owned_uv_tail', 'uv_tail_source_roster', 'posix_libm_bessel', 'independent_tail', 'uvt_route_b', 'b3_independent',
             'b3_points', 'rb_common', 'certs_common')


# ----------------------------------------------------------------------------------------------------------- utilities
def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def pin(name):
    p, s = PINS[name]
    if sha_file(p) != s:
        raise SystemExit('PIN MISMATCH %s %s' % (name, p))
    return {'path': str(p), 'sha256': s}


def load_module(name):
    p, s = PINS[name]
    if sha_file(p) != s:
        raise SystemExit('PIN MISMATCH %s' % p)
    spec = importlib.util.spec_from_file_location('b2c3_' + name, str(p)); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if sha_file(p) != s:
        raise SystemExit('PIN CHANGED %s' % p)
    return m


def write_new(path, raw):
    path = Path(path).resolve()
    if GATE.resolve() not in path.parents:
        raise SystemExit('refusing to write outside gate_b2_c3: %s' % path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'xb') as f:
        f.write(raw)
    return hashlib.sha256(raw).hexdigest()


def write_json(path, obj):
    return write_new(path, (json.dumps(obj, indent=1, allow_nan=False) + '\n').encode())


def write_npz(path, **arrays):
    import io
    buf = io.BytesIO(); np.savez(buf, **arrays)
    return write_new(path, buf.getvalue())


def no_tail_library_loaded():
    bad = sorted(n for n in sys.modules if any(f in n for f in FORBIDDEN))
    files = sorted(str(getattr(m, '__file__', '') or '') for m in list(sys.modules.values()))
    bad += [f for f in files if any(x in f for x in FORBIDDEN)]
    return bad


def gl(n, a, b):
    x, w = np.polynomial.legendre.leggauss(n)
    return (a + b) / 2 + (b - a) * x / 2, (b - a) * w / 2


def axis_nodes(width, order):
    """The k-axis rule on [-12, 12]: GL(order) on uniform panels (<= width) between the breaks {0, 2, 3, 4, 12} of the positive half,
    mirrored (exact negation, so the node set is exactly symmetric; every node of the full axis is used)."""
    x, w = panels(np.array([b for b in BREAKS if b >= 0]), width, order)
    return np.concatenate([-x[::-1], x]), np.concatenate([w[::-1], w])


def panels(edges, width, n):
    xs = []; ws = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = max(1, int(math.ceil((b - a) / width - 1e-12)))
        e = np.linspace(a, b, m + 1)
        for lo, hi in zip(e[:-1], e[1:]):
            x, w = gl(n, lo, hi); xs.append(x); ws.append(w)
    return np.concatenate(xs), np.concatenate(ws)


# ----------------------------------------------------------------------------------------------------------- own J0
_THETA = {}


def _sines(N):
    if N not in _THETA:
        j = np.arange(1, N // 4)
        _THETA[N] = np.sin(2 * math.pi * j / N)
    return _THETA[N]


def J0(x):
    """J0(x) = (1/2pi) int_0^2pi cos(x sin t) dt by the N-point periodic trapezoid (error 2 J_N(x)); N = 4 ceil((xmax+96)/4)
    (J_N(x) < 1e-18 for N >= x + 96 on x <= 400); the four-fold symmetry of sin on the N nodes: 2 + 2cos x + 4 sum_{0<j<N/4}."""
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        return np.zeros(x.shape)
    xm = float(np.max(np.abs(x)))
    if xm > 400:
        raise ValueError('own J0 range')
    N = 4 * int(math.ceil((xm + 96.0) / 4.0))
    s = _sines(N)
    acc = np.zeros(x.shape); tmp = np.empty(x.shape)
    for sj in s:
        np.multiply(x, sj, out=tmp); np.cos(tmp, out=tmp); acc += tmp
    return (2.0 + 2.0 * np.cos(x) + 4.0 * acc) / N


def libm_j0_check(n=200000, seed=7):
    lib = ctypes.CDLL(ctypes.util.find_library('m')); lib.j0.argtypes = [ctypes.c_double]; lib.j0.restype = ctypes.c_double
    rng = np.random.default_rng(seed)
    x = np.concatenate([rng.uniform(0, 300, n), rng.uniform(0, 5, n // 10), np.array([0.0, 1e-8, 2.404825557695773, 100.0, 299.9])])
    ref = np.array([lib.j0(float(v)) for v in x]); mine = J0(x)
    return dict(n=int(x.size), x_max=float(x.max()), max_abs_diff=float(np.max(np.abs(mine - ref))), libm=ctypes.util.find_library('m'))


# ----------------------------------------------------------------------------------------------------------- sources
def sigma_profile(r, radii, sig, rd):
    """registered stellar Sigma(R) [Msun/pc^2]: constant core r<=x0, linear between nodes, y_last exp(-(r-x_last)/rd) beyond."""
    r = np.asarray(r, float); x = np.asarray(radii, float); y = np.asarray(sig, float)
    out = np.interp(r, x, y)
    out = np.where(r <= x[0], y[0], out)
    return np.where(r >= x[-1], y[-1] * np.exp(-(r - x[-1]) / rd), out)


def star_nodes_continuum(st, kpc_m, sigma_unit, mult):
    """Own quadrature of P_* = 2 pi int Sigma J0(kp R) R dR: GL(8 mult) on the core [0, x0], GL(12 mult) on every linear segment,
    the exponential tail on t = (R - x_last)/a in [0, 44] (e^-44 = 8e-20) on uniform panels dt <= 0.5/mult, GL 12."""
    radii = [float(v) for v in st['radius_kpc']]; sig = [float(v) for v in st['surface_density_Msun_pc2']]; a = float(st['outer_scale_kpc'])
    R = []; W = []
    x, w = gl(8 * mult, 0.0, radii[0]); R.append(x); W.append(w)
    for lo, hi in zip(radii[:-1], radii[1:]):
        x, w = gl(12 * mult, lo, hi); R.append(x); W.append(w)
    t, wt = panels(np.array([0.0, 44.0]), 0.5 / mult, 12)
    rr = np.concatenate(R); ww = np.concatenate(W)
    mass = 2 * math.pi * sigma_profile(rr, radii, sig, a) * sigma_unit * (rr * kpc_m) * (ww * kpc_m)
    rt = radii[-1] + a * t
    mass_t = 2 * math.pi * sig[-1] * sigma_unit * np.exp(-t) * (rt * kpc_m) * (a * wt * kpc_m)
    return np.concatenate([rr, rt]) * kpc_m, np.concatenate([mass, mass_t])


def star_rings_discrete(st, kpc_m, sigma_unit, order):
    """The packet's discrete GL rings (prep v007 analytic branch, as described in the design/ADV text): GL(order) per segment of
    [0]+radii, the tail on u in (0,1] (R = x_last - a ln u, dR = a w/(2u)), heights z = 2h atanh(x_GL) with weights w/2."""
    radii = [float(v) for v in st['radius_kpc']]; sig = [float(v) for v in st['surface_density_Msun_pc2']]; a = float(st['outer_scale_kpc'])
    h = float(st['height_kpc']); gx, gw = np.polynomial.legendre.leggauss(order)
    cuts = sorted(set([0.0] + radii)); rr = []; dr = []
    for lo, hi in zip(cuts[:-1], cuts[1:]):
        rr.extend((lo + hi) / 2 + (hi - lo) * gx / 2); dr.extend((hi - lo) * gw / 2)
    u = (gx + 1) / 2; rr.extend(radii[-1] - a * np.log(u)); dr.extend(a * gw / (2 * u))
    rr = np.array(rr); dr = np.array(dr)
    M = sigma_profile(rr, radii, sig, a) * sigma_unit * (rr * kpc_m) * (dr * kpc_m) * 2 * math.pi
    zu = 2 * h * kpc_m * np.arctanh(gx); wu = gw / 2
    return rr * kpc_m, M, zu, wu


def annulus_gl4(s_edges):
    x4, w4 = np.polynomial.legendre.leggauss(4)
    s = []; w = []; ann = []
    for a, (lo, hi) in enumerate(zip(s_edges[:-1], s_edges[1:])):
        s.extend((lo + hi) / 2 + (hi - lo) * x4 / 2); w.extend((hi - lo) * w4 / 4); ann.extend([a] * 4)
    return np.array(s), np.array(w), np.array(ann)          # s [kpc^2], int R dR weight [kpc^2], annulus index


def gas_nodes_continuum(s_edges, kpc_m, nR):
    """Own quadrature of P_i(kp) = int_annulus 2 pi R J0(kp R) L_i(R^2) dR (GL(nR) in R per annulus) -> nodes R [m] and the
    (n_nodes, 72) coefficient matrix [m^2]."""
    s4, _, ann4 = annulus_gl4(s_edges)
    Rn = []; C = np.zeros((nR * (len(s_edges) - 1), len(s4)))
    for a, (lo, hi) in enumerate(zip(s_edges[:-1], s_edges[1:])):
        r, w = gl(nR, math.sqrt(lo), math.sqrt(hi)); s = r * r
        si = s4[4 * a:4 * a + 4]
        for i in range(4):
            L = np.ones_like(s)
            for j in range(4):
                if j != i:
                    L *= (s - si[j]) / (si[i] - si[j])
            C[a * nR:(a + 1) * nR, 4 * a + i] = 2 * math.pi * r * w * L * kpc_m * kpc_m
        Rn.append(r)
    return np.concatenate(Rn) * kpc_m, C


def j0_matrix_apply(kp, R, C, block=4_000_000):
    """sum_q J0(kp_k R_q) C_qc for every kp (sorted ascending) -> (n_k, n_c); kp blocks sized so a block holds <= block args."""
    out = np.zeros((len(kp), C.shape[1]))
    nb = max(1, block // max(1, len(R)))
    for a in range(0, len(kp), nb):
        b = min(a + nb, len(kp))
        out[a:b] = J0(np.outer(kp[a:b], R)) @ C
    return out


# ----------------------------------------------------------------------------------------------------------- saved state
class SavedState:
    def __init__(self, sid):
        run, rsha, K = STATES[sid]; self.sid = sid; self.K = K; self.run = RUNS / run
        if sha_file(self.run / 'result.json') != rsha:
            raise SystemExit('R3 result sha ' + sid)
        self.result_sha = rsha
        fin = json.loads((self.run / 'finish.json').read_text())
        if fin.get('result_sha256') != rsha:
            raise SystemExit('finish.json result sha ' + sid)
        res = json.loads((self.run / 'result.json').read_text())
        self.gamma = float(res['identity']['route_a']['custody']['physical']['gamma'])
        self.c = float(res['identity']['route_a']['custody']['physical'].get('c_m_s', CL))
        st = self.run / 'stages'
        self.rot_dir = st / '19_le3_rotation/rotation'; self.cm_dir = st / '20_le3_column_mean/observation'; self.col_dir = st / '18_le3_columns_00/columns'
        rreq = json.loads((st / '19_le3_rotation/request.json').read_text()); a = rreq['argv']
        self.seed = Path(a[a.index('--seed') + 1]); self.ni = json.loads(self.seed.read_text())['numerical_inputs']
        self.feedback_dir = Path(a[a.index('--feedback-directory') + 1])
        fsha = a[a.index('--feedback-finish-sha256') + 1]
        if sha_file(self.feedback_dir / 'finish.json') != fsha:
            raise SystemExit('le2 feedback finish sha ' + sid)
        fbreq = json.loads((st / '17_le2_feedback/request.json').read_text()); fa = fbreq['argv']
        self.src_rot_dir = Path(fa[fa.index('--rotation-directory') + 1])
        fstart = json.loads((self.feedback_dir / 'start.json').read_text())
        if sha_file(self.src_rot_dir / 'finish.json') != fstart['rotation_finish_sha256']:
            raise SystemExit('source rotation is not the one the le2 feedback transformed ' + sid)
        self.checkpoint = Path(a[a.index('--checkpoint-directory') + 1])
        # saved rows (le3 column mean) and the row ids
        cm = json.loads((self.cm_dir / 'result.json').read_text())
        self.rows_saved = np.array([r['speed_km_s'] for r in cm['prediction']['rows']], float)
        self.row_ids = [r['id'] for r in cm['prediction']['rows']]
        self.cm_result_sha = sha_file(self.cm_dir / 'result.json')
        # the rows the run itself reports for its final pass, for the le3-vs-final note
        self.final_pass_rows = np.array([r['speed_km_s'] for r in res['passes'][-1]['rows']], float)
        self.n_passes = len(res['passes'])

    def le3_rotation(self):
        fin = json.loads((self.rot_dir / 'finish.json').read_text())
        if sha_file(fin['arrays_path']) != fin['arrays_sha256']:
            raise SystemExit('le3 rotation arrays sha ' + self.sid)
        keys = ('radial_nodes_m', 'z', 'rho0', 'enthalpy', 'rotation_Omega_squared', 'rotation_A', 'Omega', 'full_fields_complex',
                'full_gradient_complex', 'Phi_R_full')
        with np.load(fin['arrays_path'], allow_pickle=False) as f:
            arr = {k: f[k].copy() for k in keys}
        return arr, dict(path=fin['arrays_path'], sha256=fin['arrays_sha256'], finish_sha256=sha_file(self.rot_dir / 'finish.json'))

    def columns(self):
        fin = json.loads((self.col_dir / 'finish.json').read_text()); cols = {}
        for it in fin['completed']:
            if sha_file(it['path']) != it['sha256']:
                raise SystemExit('column sha')
            cols[it['index']] = json.loads(Path(it['path']).read_text())
        return [cols[i] for i in range(len(cols))]

    def source_rotation(self):
        fin = json.loads((self.src_rot_dir / 'finish.json').read_text())
        if sha_file(fin['arrays_path']) != fin['arrays_sha256']:
            raise SystemExit('source rotation arrays sha ' + self.sid)
        with np.load(fin['arrays_path'], allow_pickle=False) as f:
            arr = {k: f[k].copy() for k in ('rho0', 'volume_weights_m3', 'radial_nodes_m', 'z')}
        return arr, dict(directory=str(self.src_rot_dir), finish_sha256=sha_file(self.src_rot_dir / 'finish.json'), arrays_sha256=fin['arrays_sha256'])


# ----------------------------------------------------------------------------------------------------------- table mode
def cmd_table(width, order, nR, smult, tag, discrete):
    t0 = time.time(); pins = {k: pin(k) for k in ('profile',)}
    prof = json.loads(Path(PINS['profile'][0]).read_text())['galaxies']['DDO154']
    st = prof['stellar_reference']; s_edges = [float(v) for v in prof['HI_plus_He']['s_edges_kpc2']]
    ni = SavedState('C4R3').ni                                    # units (identical in every R3 seed; checked in state mode)
    kpc_m = float(ni['kpc_m']); sigma_unit = float(ni['solar_mass_kg']) / (kpc_m / 1000.0) ** 2
    ax, aw = axis_nodes(width, order)
    kp2 = (ax[:, None] ** 2 + ax[None, :] ** 2).ravel()
    u, inv = np.unique(kp2, return_inverse=True)
    kp = np.sqrt(u) / kpc_m
    print('table', tag, 'axis', len(ax), 'xy', kp2.size, 'unique kp', len(u), flush=True)
    jchk = libm_j0_check()
    print('own J0 vs libm', jchk, '%.0fs' % (time.time() - t0), flush=True)
    Rs, Ms = star_nodes_continuum(st, kpc_m, sigma_unit, smult)
    Rg, Cg = gas_nodes_continuum(s_edges, kpc_m, nR)
    cols = {}; names = []
    P_sc = j0_matrix_apply(kp, Rs, Ms[:, None]); print('stars continuum done', '%.0fs' % (time.time() - t0), flush=True)
    P_gc = j0_matrix_apply(kp, Rg, Cg); print('gas continuum done', '%.0fs' % (time.time() - t0), flush=True)
    blocks = [P_sc, P_gc]; names += ['stars_cont'] + ['gas_cont_%02d' % i for i in range(Cg.shape[1])]
    extra = {}
    if discrete:
        Rd, Md, zu, wu = star_rings_discrete(st, kpc_m, sigma_unit, int(ni['source_gauss_order']))
        s4, w4, _ = annulus_gl4(s_edges); Rcol = np.sqrt(s4) * kpc_m
        P_sd = j0_matrix_apply(kp, Rd, Md[:, None]); P_gd = j0_matrix_apply(kp, Rcol, np.eye(len(Rcol)))
        blocks += [P_sd, P_gd]; names += ['stars_disc'] + ['gas_disc_%02d' % i for i in range(len(Rcol))]
        extra = dict(star_disc_R_m=Rd, star_disc_M_kg=Md, star_disc_z_m=zu, star_disc_wz=wu)
        print('discrete done', '%.0fs' % (time.time() - t0), flush=True)
    P = np.concatenate(blocks, axis=1)
    star_mass = float(np.sum(Ms))
    rec = dict(schema='CLAUDE3_B2_IND_TABLE_C3V001', producer={'path': str(Path(__file__).resolve()), 'sha256': sha_file(__file__)},
               tag=tag, width_inverse_kpc=width, order=order, gas_nodes_per_annulus=nR, star_mult=smult, discrete=bool(discrete),
               breaks_inverse_kpc=list(BREAKS), K_out_inverse_kpc=KOUT, n_axis=int(len(ax)), n_xy=int(kp2.size), n_unique_kp=int(len(u)),
               n_star_nodes=int(len(Rs)), n_gas_nodes=int(len(Rg)), stellar_mass_kg=star_mass, names=names, j0_check=jchk,
               kpc_m=kpc_m, sigma_unit=sigma_unit, pins=pins, forbidden_modules_loaded=no_tail_library_loaded(),
               seconds=time.time() - t0, peak_rss_bytes=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    h = write_npz(OUT / ('TABLE_%s.npz' % tag), ax=ax, aw=aw, inv=inv.astype(np.int64), u=u, P=P, **extra)
    rec['npz_sha256'] = h
    write_json(OUT / ('TABLE_%s.json' % tag), rec)
    print('table written', tag, h[:12], '%.0fs' % (time.time() - t0), flush=True)


# ----------------------------------------------------------------------------------------------------------- state mode
def rows_from_omega2(om2, rot, cols, binding, obs, adapter):
    R = rot['radial_nodes_m']; rho = rot['rho0']
    weights = [(np.asarray(c['weights_m'], float) * rho[i, 0] * binding['HI_to_HI_plus_He_mass_ratio']).tolist() for i, c in enumerate(cols)]
    speed = R[:, None] * np.sqrt(om2)
    pk = adapter.evaluate(observation_module=obs, radial_nodes_m=R, query_ids=[q['id'] for q in binding['query_rows']],
                          query_radii_m=[q['radius_m'] for q in binding['query_rows']], v_phi_m_s=speed, emissivity_path_weights=weights,
                          physical_inclination_rad=binding['physical_inclination_rad'], released_inclination_rad=binding['released_inclination_rad'],
                          approximation_provenance=binding['observation_rule'], tracer_provenance=binding['tracer_rule'],
                          source_status='CLAUDE3_B2_INDEPENDENT', motion_status='CLAUDE3_B2_INDEPENDENT',
                          nonaxisymmetric_residual_provenance='Claude3 B2 independent static rows')
    return np.array([r['speed_km_s'] for r in pk['rows']], float), [r['id'] for r in pk['rows']]


def cmd_state(sid, tag, groups):
    t0 = time.time()
    bad = [k for k in THREADS if os.environ.get(k) != '1']
    if bad:
        raise SystemExit('single-thread BLAS env required: ' + ','.join(bad))
    S = SavedState(sid)
    tj = json.loads((OUT / ('TABLE_%s.json' % tag)).read_text())
    if sha_file(OUT / ('TABLE_%s.npz' % tag)) != tj['npz_sha256']:
        raise SystemExit('table sha')
    with np.load(OUT / ('TABLE_%s.npz' % tag), allow_pickle=False) as f:
        T = {k: f[k].copy() for k in f.files}
    names = tj['names']; kpc_m = float(S.ni['kpc_m'])
    if kpc_m != tj['kpc_m'] or float(S.ni['solar_mass_kg']) / (kpc_m / 1000.0) ** 2 != tj['sigma_unit']:
        raise SystemExit('units differ from the table')
    prof = json.loads(Path(PINS['profile'][0]).read_text())['galaxies']['DDO154']; st = prof['stellar_reference']
    s_edges = [float(v) for v in prof['HI_plus_He']['s_edges_kpc2']]
    s4, w4, _ = annulus_gl4(s_edges); Rcol = np.sqrt(s4) * kpc_m; rdr = w4 * kpc_m * kpc_m
    # ------------------------------------------------------------------ sources of this state
    src, src_pin = S.source_rotation()
    rho = src['rho0']; z = src['z']
    if not (np.array_equal(rho, np.broadcast_to(rho[:, :1, :], rho.shape)) and np.array_equal(z, np.broadcast_to(z[:, :1, :], z.shape))):
        raise SystemExit('source rotation not m0')
    m_il = np.sum(src['volume_weights_m3'] * rho, axis=1); z_il = z[:, 0, :]
    radial_match = float(np.max(np.abs(src['radial_nodes_m'] / Rcol - 1)))
    if radial_match > 1e-12:
        raise SystemExit('source columns are not the GL4 annulus nodes %.3e' % radial_match)
    c = S.c; gamma = S.gamma; h_m = float(st['height_kpc']) * kpc_m
    ax = T['ax']; aw = T['aw']; kz = ax / kpc_m; wz = aw / kpc_m
    def vert(kind):
        if kind == 'stars_cont':
            x = math.pi * h_m * np.abs(kz)
            v = np.ones_like(x); nz = x > 0; v[nz] = x[nz] / np.sinh(x[nz])
            return -c * c * v[:, None].astype(complex)
        if kind == 'gas_cont':
            E = np.exp(-1j * np.outer(kz, z_il.reshape(-1))).reshape(len(kz), z_il.shape[0], z_il.shape[1])
            E = np.einsum('kil,il->ki', E, m_il)
            return -c * c * E / (2 * math.pi * rdr[None, :])
        if kind == 'stars_disc':
            v = np.exp(-1j * np.outer(kz, T['star_disc_z_m'])) @ T['star_disc_wz']
            return -c * c * v[:, None]
        if kind == 'gas_disc':
            E = np.exp(-1j * np.outer(kz, z_il.reshape(-1))).reshape(len(kz), z_il.shape[0], z_il.shape[1])
            return -c * c * np.einsum('kil,il->ki', E, m_il)
        raise ValueError(kind)
    colsel = {'stars_cont': [names.index('stars_cont')], 'gas_cont': [i for i, n in enumerate(names) if n.startswith('gas_cont_')],
              'stars_disc': [names.index('stars_disc')] if 'stars_disc' in names else None,
              'gas_disc': [i for i, n in enumerate(names) if n.startswith('gas_disc_')] or None}
    groups = [g for g in groups if colsel.get(g)]
    V = {g: vert(g) for g in groups}
    Pg = {g: T['P'][:, colsel[g]] for g in groups}
    # ------------------------------------------------------------------ custody: discrete rings vs the packet sources (I1-style)
    custody = {}
    with np.load(Path(json.loads((S.feedback_dir / 'finish.json').read_text())['outputs']['refreshed_prepared.npz']['path']), allow_pickle=False) as f:
        waves = f['wavevectors'].copy()
    fb = json.loads((S.feedback_dir / 'finish.json').read_text())['outputs']['gas_source_feedback.npz']
    if sha_file(fb['path']) != fb['sha256']:
        raise SystemExit('gas packet sha')
    with np.load(fb['path'], allow_pickle=False) as f:
        gasJ = f['new_gas_fourier_J'][:, 0, 0].copy()
    rng = np.random.default_rng(20261018 + int(S.K)); idx = np.sort(rng.choice(len(waves), 3000, replace=False))
    wv = waves[idx]; kpv = np.hypot(wv[:, 0], wv[:, 1])
    Eg = np.exp(-1j * np.outer(wv[:, 2], z_il.reshape(-1))).reshape(len(wv), z_il.shape[0], z_il.shape[1])
    gas_ring = -c * c * np.einsum('ki,kil,il->k', J0(np.outer(kpv, src['radial_nodes_m'])), Eg, m_il)
    custody['gas_rings_vs_new_gas_fourier_J_max_rel'] = float(np.max(np.abs(gas_ring - gasJ[idx])) / np.max(np.abs(gasJ[idx])))
    stj = None
    for itdir in sorted(S.checkpoint.glob('iteration_*')):
        stj = json.loads((itdir / 'START.json').read_text())['fixed_source_fourier_J']
    if stj is not None and 'star_disc_R_m' in T:
        blob = S.checkpoint / stj['blob']
        if sha_file(blob) != stj['file_sha256']:
            raise SystemExit('star blob sha')
        starJ = np.load(blob, allow_pickle=False)[:, 0, 0]
        cw = None
        # the checkpoint's wave order: the route-A prepared wavevectors (iteration START prepared_wavevectors)
        sref = json.loads((itdir / 'START.json').read_text()).get('prepared_wavevectors')
        if sref is not None and (S.checkpoint / sref['blob']).exists() and sha_file(S.checkpoint / sref['blob']) == sref['file_sha256']:
            cw = np.load(S.checkpoint / sref['blob'], allow_pickle=False)
        if cw is not None and np.array_equal(cw, waves):
            sv = np.exp(-1j * np.outer(wv[:, 2], T['star_disc_z_m'])) @ T['star_disc_wz']
            star_ring = -c * c * (J0(np.outer(kpv, T['star_disc_R_m'])) @ T['star_disc_M_kg']) * sv
            custody['star_rings_vs_fixed_source_fourier_J_max_rel'] = float(np.max(np.abs(star_ring - starJ[idx])) / np.max(np.abs(starJ[idx])))
        else:
            custody['star_rings_vs_fixed_source_fourier_J_max_rel'] = 'NOT_EVALUATED: checkpoint wave order not matched'
    custody['source_columns_vs_GL4_annulus_nodes_max_rel'] = radial_match
    print(sid, 'custody', custody, '%.0fs' % (time.time() - t0), flush=True)
    # ------------------------------------------------------------------ evaluation geometry (saved le3 rotation)
    rot, rot_pin = S.le3_rotation(); cols = S.columns()
    Rev = rot['radial_nodes_m']; zev = rot['z'][:, 0, :]
    binding = json.loads(Path(PINS['binding'][0]).read_text()); pin('binding')
    Rrow = np.array([q['radius_m'] for q in binding['query_rows']], float)
    Rall = np.concatenate([Rev, Rrow])                              # 72 column radii + 12 row radii (z = 0 proxy)
    nR = len(Rall)
    phis = 2 * math.pi * np.arange(NPHI) / NPHI
    cph = np.cos(phis); sph = np.sin(phis)
    # ------------------------------------------------------------------ full-box contraction
    K = S.K; inner = np.abs(ax) <= K * (1 + 1e-12)
    pref = 1.0 / (4.0 * gamma * (2 * math.pi) ** 3)
    inv = T['inv'].reshape(len(ax), len(ax))
    GR = {g: np.zeros((nR, len(kz)), complex) for g in groups}
    GV = np.zeros((nR, len(kz)), complex)
    kz2 = kz * kz
    nrow = max(1, 9216 // len(ax))
    n_kept_nodes = 0
    for a0 in range(0, len(ax), nrow):
        a1 = min(a0 + nrow, len(ax))
        kx = np.repeat(ax[a0:a1], len(ax)) / kpc_m; ky = np.tile(ax, a1 - a0) / kpc_m
        wxy = (np.repeat(aw[a0:a1], len(ax)) * np.tile(aw, a1 - a0)) / kpc_m ** 2
        ixy = (np.repeat(inner[a0:a1], len(ax)) & np.tile(inner, a1 - a0))
        rows_u = inv[a0:a1].reshape(-1)
        kp2 = kx * kx + ky * ky
        keep = ~(ixy[:, None] & inner[None, :])
        n_kept_nodes += int(keep.sum())
        common = (pref * wxy[:, None] * wz[None, :] / (kp2[:, None] + kz2[None, :])) * keep
        P16 = np.zeros((nR, len(kx)), complex); V16 = np.zeros((nR, len(kx)), complex)
        for j in range(NPHI):
            proj = kx * cph[j] + ky * sph[j]
            E = np.exp(1j * np.outer(Rall, proj))
            P16 += (1j * proj)[None, :] * E; V16 += E
        P16 /= NPHI; V16 /= NPHI
        Ftot = None
        for g in groups:
            Pr = Pg[g][rows_u]
            Fg = (Pr @ V[g].real.T + 1j * (Pr @ V[g].imag.T)) * common
            GR[g] += P16 @ Fg
            if g in ('stars_cont', 'gas_cont'):
                Ftot = Fg if Ftot is None else Ftot + Fg
        if Ftot is not None:
            GV += V16 @ Ftot
        if a0 % (nrow * 16) == 0:
            print(sid, tag, 'kx rows %d/%d' % (a1, len(ax)), '%.0fs' % (time.time() - t0), flush=True)
    # ------------------------------------------------------------------ to the column nodes
    def at_nodes(G):
        tc = np.empty(zev.shape, complex)
        for i in range(len(Rev)):
            tc[i] = G[i] @ np.exp(1j * np.outer(kz, zev[i]))
        t0z = G[len(Rev):] @ np.ones(len(kz))                 # the 12 row radii at z = 0
        return tc, t0z
    out = {}; arrays = {}
    for g in groups:
        tc, t0z = at_nodes(GR[g]); out[g] = dict(imag_over_real_max=float(np.max(np.abs(tc.imag)) / np.max(np.abs(tc.real))))
        arrays['tR_' + g] = tc.real; arrays['tR_imag_' + g] = tc.imag; arrays['tR_rows_z0_' + g] = t0z.real
    tv, tv0 = at_nodes(GV)
    arrays['t_total'] = tv.real; arrays['t_total_imag'] = tv.imag
    # ------------------------------------------------------------------ static rows
    obs = load_module('observation'); adapter = load_module('adapter')
    A = np.sum(np.array([cc['weights_m'] for cc in cols]) * rot['rho0'][:, 0, :] / rot['enthalpy'][:, 0, :], axis=1)
    A_rel = float(np.max(np.abs(A / rot['rotation_A'] - 1)))
    w_rho_h = np.array([cc['weights_m'] for cc in cols]) * rot['rho0'][:, 0, :] / rot['enthalpy'][:, 0, :]
    rows0, ids = rows_from_omega2(rot['rotation_Omega_squared'], rot, cols, binding, obs, adapter)
    control_bitwise = bool(rows0.tobytes() == S.rows_saved.tobytes()) and ids == S.row_ids
    om_bitwise = bool(np.array_equal(np.sqrt(rot['rotation_Omega_squared']), rot['Omega'][:, 0, :]))
    f0 = rot['full_fields_complex'][..., 0].real                    # (72,16,32)
    grad = rot['full_gradient_complex'][..., 0, :].real            # (72,16,32,3)
    gR = grad[..., 0] * cph[None, :, None] + grad[..., 1] * sph[None, :, None]
    PR_saved = c * c * gR / (1 + f0)
    PR_saved_check = float(np.max(np.abs(PR_saved - rot['Phi_R_full'])) / np.max(np.abs(rot['Phi_R_full'])))
    def omega2_with(dpr):
        return rot['rotation_Omega_squared'] + (np.sum(w_rho_h * dpr, axis=1) / A / Rev)[:, None]
    variants = {}
    if 'stars_cont' in groups and 'gas_cont' in groups:
        tR = arrays['tR_stars_cont'] + arrays['tR_gas_cont']; tt = arrays['t_total']
        dpr_exact = np.mean(c * c * (gR + tR[:, None, :]) / (1 + f0 + tt[:, None, :]) - c * c * gR / (1 + f0), axis=1)
        dpr_lin = c * c * tR
        variants['B2_continuum_v001'] = dpr_exact; variants['B2_continuum_v001_linear'] = dpr_lin
        arrays['dpr_B2'] = dpr_exact
    for gname in groups:
        variants['only_' + gname] = c * c * arrays['tR_' + gname]
    if 'stars_disc' in groups and 'gas_disc' in groups:
        variants['discrete_total'] = c * c * (arrays['tR_stars_disc'] + arrays['tR_gas_disc'])
        if 'stars_cont' in groups and 'gas_cont' in groups:     # source-rule decomposition (linear in the tail force)
            variants['mixed_gas_disc_stars_cont'] = c * c * (arrays['tR_gas_disc'] + arrays['tR_stars_cont'])
            variants['mixed_gas_cont_stars_disc'] = c * c * (arrays['tR_gas_cont'] + arrays['tR_stars_disc'])
    rows = {}
    for vn, dpr in variants.items():
        om2 = omega2_with(dpr)
        if np.any(om2 <= 0):
            raise SystemExit('Omega^2 <= 0 in ' + vn)
        r, ids2 = rows_from_omega2(om2, rot, cols, binding, obs, adapter)
        if ids2 != S.row_ids:
            raise SystemExit('row ids')
        rows[vn] = dict(rows_km_s=r.tolist(), delta_rows_km_s=(r - S.rows_saved).tolist())
    # z = 0 proxy at the 12 row radii (DOUBLING / certificates_v001 sec 4 static proxy definition)
    proxy = {}
    if 'stars_cont' in groups and 'gas_cont' in groups:
        tr0 = arrays['tR_rows_z0_stars_cont'] + arrays['tR_rows_z0_gas_cont']
        proxy = dict(definition='dv_i = R_i c^2 <d_R t>_16(R_i, z=0) / (2 v_i), v_i = saved le3 row speed',
                     dv_km_s=(Rrow * c * c * tr0 / (2 * S.rows_saved * 1e3) / 1e3).tolist(), dRt_mean_per_m=tr0.tolist())
    rec = dict(schema='CLAUDE3_B2_IND_STATE_C3V001', producer={'path': str(Path(__file__).resolve()), 'sha256': sha_file(__file__)},
               state=sid, state_result_sha256=S.result_sha, K_inverse_kpc=K, K_out_inverse_kpc=KOUT, azimuths=NPHI, table=tag,
               table_record=dict(path=str(OUT / ('TABLE_%s.json' % tag)), sha256=sha_file(OUT / ('TABLE_%s.json' % tag)),
                                 npz_sha256=tj['npz_sha256'], width=tj['width_inverse_kpc'], order=tj['order'], n_axis=tj['n_axis'],
                                 gas_nodes_per_annulus=tj['gas_nodes_per_annulus'], star_mult=tj['star_mult']),
               groups=groups, gamma_eff=gamma, c_m_s=c, n_box_nodes=int(len(ax) ** 3), n_kept_nodes_in_D=n_kept_nodes,
               inputs=dict(le3_rotation=rot_pin, source_rotation=src_pin, columns_finish_sha256=sha_file(S.col_dir / 'finish.json'),
                           saved_column_mean_result_sha256=S.cm_result_sha, seed=dict(path=str(S.seed), sha256=sha_file(S.seed))),
               pins={k: pin(k) for k in ('profile', 'binding', 'observation', 'adapter')},
               custody=custody, controls=dict(zero_correction_rows_equal_saved_le3_rows_bitwise=control_bitwise,
                                              sqrt_Omega2_equals_saved_Omega_bitwise=om_bitwise, A_vs_saved_rotation_A_max_rel=A_rel,
                                              Phi_R_from_saved_fields_vs_saved_Phi_R_full_max_rel=PR_saved_check),
               imag=out, row_ids=S.row_ids, rows_saved_le3_km_s=S.rows_saved.tolist(), final_pass_index=S.n_passes,
               final_pass_rows_km_s=S.final_pass_rows.tolist(), rows=rows, z0_proxy=proxy,
               forbidden_modules_loaded=no_tail_library_loaded(), seconds=time.time() - t0,
               peak_rss_bytes=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    hn = write_npz(OUT / ('IND_%s_%s.npz' % (sid, tag)), **arrays)
    rec['npz_sha256'] = hn
    hj = write_json(OUT / ('IND_%s_%s.json' % (sid, tag)), rec)
    print(sid, tag, 'rows B2', np.round(np.array(rows.get('B2_continuum_v001', {}).get('delta_rows_km_s', [])), 6).tolist(), 'json', hj[:12],
          '%.0fs' % (time.time() - t0), flush=True)


def main():
    bad = [k for k in THREADS if os.environ.get(k) != '1']
    if bad:
        raise SystemExit('single-thread BLAS env required: ' + ','.join(bad))
    if sys.argv[1] == 'table':
        w, o, nR, sm, tag = float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
        cmd_table(w, o, nR, sm, tag, len(sys.argv) > 7 and sys.argv[7] == 'discrete')
    elif sys.argv[1] == 'state':
        groups = sys.argv[4].split(',') if len(sys.argv) > 4 else ['stars_cont', 'gas_cont', 'stars_disc', 'gas_disc']
        cmd_state(sys.argv[2], sys.argv[3], groups)
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
