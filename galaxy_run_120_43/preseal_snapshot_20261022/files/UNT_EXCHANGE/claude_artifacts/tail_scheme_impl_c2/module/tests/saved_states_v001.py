"""Read-only access to the saved KMAX R3 states (the R3 verdict COMPARE_R3_V001 is registered) and the NGC iteration-0
source inputs. No NGC3198 observed or target velocity is opened (the NGC inputs read here are the f5becd45 surface
profile, the annular Bernstein kernel, the H2 source rows' H2 and radius literals, and the ring radii of the
T120L lnN ring-read files)."""
import json, math
from fractions import Fraction
from pathlib import Path
import numpy as np
import common_tests_v001 as T

BINDING = T.C1 / 'DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json'
BINDING_SHA = 'f42c7c657cd9b8bcef6b88e980918ff2570b1fc0a5480784d8bf3b8bb2a3c600'
SUF = {'C2': ('C2R3', 2.0), 'C3': ('C3R3', 3.0), 'C4': ('C4R3', 4.0)}
RESULT_SHA = {'C2': '1f6b32a4', 'C3': 'c9c802f4', 'C4': 'aac01962'}   # prefixes cited by the design (checked below)


def argmap(req):
    a = json.loads(Path(req).read_text())['argv']
    return {a[i]: a[i + 1] for i in range(len(a) - 1) if a[i].startswith('--')}


class SavedCase:
    def __init__(self, cid):
        suf, self.K = SUF[cid]; self.cid = cid
        self.run = T.RUNS / ('KMAX_A2F10_%s_D7R3_RUN_V001' % suf)
        self.result_sha = T.sha(self.run / 'result.json')
        fin = json.loads((self.run / 'finish.json').read_text())
        if fin['result_sha256'] != self.result_sha or not self.result_sha.startswith(RESULT_SHA[cid]):
            raise SystemExit('result sha mismatch ' + cid)
        res = json.loads((self.run / 'result.json').read_text())
        last = res['passes'][-1]
        self.rows = np.array([r['speed_km_s'] for r in last['rows']], float)
        self.rot = Path(last['rotation']); self.field = Path(last['field'])
        fm = argmap(self.field.parent / 'request.json'); self.src_rot = Path(fm['--rotation-directory'])
        rm = argmap(self.rot.parent / 'request.json')
        if Path(rm['--feedback-directory']) != self.field:
            raise SystemExit('rotation/field mismatch')
        self.manifest = Path(rm['--column-manifest'])
        self.gamma = float(res['identity']['route_a']['custody']['physical']['gamma'])
        self.seed_ni = json.loads((self.run / 'inputs/seed_c2v001.json').read_text())['numerical_inputs']

    def source_rotation_arrays(self):
        with np.load(self.src_rot / 'rotation_base_arrays.npz', allow_pickle=False) as f:
            return {k: f[k].copy() for k in ('rho0', 'volume_weights_m3', 'radial_nodes_m', 'z', 'radial_RdR_weights_m2')}

    def final_rotation_arrays(self):
        with np.load(self.rot / 'rotation_base_arrays.npz', allow_pickle=False) as f:
            return {k: f[k].copy() for k in ('radial_nodes_m', 'z', 'rho0', 'enthalpy', 'rotation_Omega_squared', 'rotation_A')}

    def columns(self):
        man = json.loads(self.manifest.read_text()); cols = {}
        for run in man['runs']:
            for it in json.loads((Path(run['directory']) / 'finish.json').read_text())['completed']:
                cols[it['index']] = json.loads(Path(it['path']).read_text())
        return [cols[i] for i in range(72)]

    def gas_packet(self):
        with np.load(self.field / 'gas_source_feedback.npz', allow_pickle=False) as f:
            return f['new_gas_fourier_J'][:, 0, 0].copy()

    def unit_waves(self):
        with np.load(self.field / 'refreshed_prepared.npz', allow_pickle=False) as f:
            return f['wavevectors'].copy()

    def prepared(self):
        with np.load(self.field / 'refreshed_prepared.npz', allow_pickle=False) as f:
            return {'wavevectors': f['wavevectors'].copy(), 'weighted_responses': f['weighted_responses'].copy()}


def ddo_row_radii():
    b = T.load_json_pinned(BINDING, BINDING_SHA)
    return np.array([q['radius_m'] for q in b['query_rows']], float), b


def ddo_gas_elements(arr):
    """Per GL4 column: (z list, mass list) from source-rotation arrays (sum over azimuth of vol * rho0; m=0 checked)."""
    rho = arr['rho0']; vol = arr['volume_weights_m3']; z = arr['z']
    if not np.array_equal(rho, np.broadcast_to(rho[:, :1, :], rho.shape)) or not np.array_equal(z, np.broadcast_to(z[:, :1, :], z.shape)):
        raise SystemExit('gas not m0')
    m = np.sum(vol * rho, axis=1)
    return [z[i, 0, :].copy() for i in range(z.shape[0])], [m[i].copy() for i in range(z.shape[0])]


# ----------------------------------------------------------------------------- NGC iteration-0 source inputs
NGC_KERNEL = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/annular_source_kernel_0403/annular_bernstein_source_kernel_v001.py')
NGC_KERNEL_SHA = '2544d22f46dbf225139f92f6a566f814e5857f265c43d88565c6a4d3894a759e'
H2_TAIL = T.C1 / 'NGC3198_H2_SOURCE_TAIL_REDUCTION_RUN_V001/stdout.txt'
H2_TAIL_SHA = '157ede0487beed6658a413ae4db34cae2e819efc58efd292ccc56794ae5917d2'
RINGS_DIR = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_kgrid_fidelity_c2/phase23/out/rings/T120L_hovr')


def ngc_inputs():
    prof = T.profile()['galaxies']['NGC3198']
    tail = T.load_json_pinned(H2_TAIL, H2_TAIL_SHA)
    h2src = T.load_json_pinned(tail['source']['path'], tail['source']['sha256'])
    rows = h2src['S1_alternative_and_stellar_median_rows']['rows'][:10]
    hr = [float(Fraction(r['radius_kpc_literal']['value'])) for r in rows]
    hs = [float(Fraction(r['components']['H2']['value_literal']['value'])) for r in rows]
    kern = T.load_module(NGC_KERNEL, 'bernstein', NGC_KERNEL_SHA)
    gas = prof['HI_plus_He']
    edges = [float(x) for x in gas['s_edges_kpc2']]
    x4, w4 = np.polynomial.legendre.leggauss(4)
    kpc = T.KPC; msun = 1.98847e30; sig_unit = msun / (kpc / 1000) ** 2
    ring_R = []; ring_m = []; ring_rdr = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        for x, w in zip(x4, w4):
            s = (lo + hi) / 2 + (hi - lo) * float(x) / 2
            R = math.sqrt(s) * kpc; dR = (hi - lo) * float(w) * kpc * kpc / (4 * R)
            p = kern.annular_bernstein_sigma(s_edges=edges, annular_means=[float(v) for v in gas['annular_means_Msun_pc2']],
                                             boundary_controls=[float(v) for v in gas['boundary_controls_Msun_pc2']], s_query=[float((R / kpc) ** 2)])
            if not p['ok']:
                raise SystemExit('kernel query failed')
            Sig = float(p['sigma'][0]) * sig_unit
            if Sig == 0:
                continue
            ring_R.append(R); ring_m.append(Sig * R * dR * 2 * math.pi); ring_rdr.append(R * dR)
    h2 = dict(name='H2', radius_kpc=hr, surface_density_Msun_pc2=hs, outer_scale_kpc=float(tail['outer_scale_kpc']))
    # ring radii of the saved T120L ring reads (lnN read files; R_kpc only)
    ringR = []
    for p in sorted(RINGS_DIR.glob('rings_*.json')):
        ringR += [r['R_kpc'] for r in json.loads(p.read_text())['rows']]
    return dict(profile_all=T.profile(), edges=edges, ring_R=np.array(ring_R), ring_m=np.array(ring_m), ring_rdr=np.array(ring_rdr),
                h2=h2, kpc_m=kpc, msun=msun, rings_R_kpc=np.array(ringR), stars=prof['stellar_reference'])
