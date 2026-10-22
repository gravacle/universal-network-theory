"""CHECKER replay (independent of tools/replay_lib_v001.py). Diagnostics only, no run.

Own record decoder; module/blob shas recomputed from bytes against the run IDENTITY/START;
metric callback transcribed from solver c2v001:129-158 (vertical_fourier_module branch,
zero boundary jets = prep v001:269-273); HI module called exactly as solver :162-165.
Reads no velocities/targets/result.json values.
"""
import hashlib, importlib.util, json, math, sys
from pathlib import Path
import numpy as np

RUN = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
           'FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/NGC3198_ROUTE_A_A2F10_RUN_V001')
CK = RUN/'checkpoint'; IT0 = CK/'iteration_0000'
KPC = 3.085677581491367e19


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def dec(e):
    t = e[0]
    if t == 'n': return None
    if t == 'b': return e[1]
    if t == 'i': return int(e[1])
    if t == 'f': return float.fromhex(e[1])
    if t == 'c': return complex(float.fromhex(e[1]), float.fromhex(e[2]))
    if t == 's': return e[1]
    if t == 'l': return [dec(x) for x in e[1]]
    if t == 't': return tuple(dec(x) for x in e[1])
    if t == 'd':
        out = {}
        for k, v in e[1]:
            assert k not in out
            out[k] = dec(v)
        return out
    if t in ('a', 'g'):
        a = np.frombuffer(bytes.fromhex(e[3]), dtype=np.dtype(e[1])).reshape(tuple(e[2])).copy()
        return a if t == 'a' else a[()]
    raise ValueError('bad tag '+t)


def load(path, expect, name):
    got = sha(path)
    if got != expect: raise SystemExit('PIN MISMATCH %s %s %s' % (path, got, expect))
    spec = importlib.util.spec_from_file_location('chk_'+name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


class Ctx:
    def __init__(self):
        ident = json.loads((CK/'IDENTITY.json').read_text())
        idn = ident['identity']; self.idn = idn; self.identity_sha = ident['identity_sha256']
        mods = idn['code']['modules']
        self.hi = load(mods['hi_module']['path'], mods['hi_module']['sha256'], 'hi')
        self.metric = load(mods['metric_module']['path'], mods['metric_module']['sha256'], 'metric')
        self.quad = load(mods['quadrature_module']['path'], mods['quadrature_module']['sha256'], 'quad')
        self.line = load(mods['vertical_fourier_module']['path'], mods['vertical_fourier_module']['sha256'], 'line')
        ck = idn['code']['checkpoint']; self.ckm = load(ck['path'], ck['sha256'], 'ckpt')
        caller = dec(idn['caller']['record'])
        phys = caller['physical_parameters']; self.caller = caller
        self.Cbar = phys['Cbar']; self.mubar = phys['mubar']
        ctrl = {k: dec(v) for k, v in idn['controls'].items()}
        self.ratol = ctrl['reality_atol']; self.rrtol = ctrl['reality_rtol']; self.c = ctrl['c_m_s']
        st = json.loads((IT0/'START.json').read_text()); self.start = st
        arr = {}
        for key in ('prepared_wavevectors', 'prepared_weighted_responses'):
            ref = st[key]; p = CK/ref['blob']
            if sha(p) != ref['file_sha256']: raise SystemExit('blob sha mismatch '+key)
            arr[key] = np.load(p, allow_pickle=False)
        self.prepared = {'wavevectors': arr['prepared_wavevectors'], 'weighted_responses': arr['prepared_weighted_responses']}
        self._k = None; self._line = None

    def metric_point(self, R, phi, z):
        pos = np.array([[R*math.cos(phi), R*math.sin(phi), z]])
        b = dict(boundary_fields=np.zeros((1, 10, 1)), boundary_gradient=np.zeros((1, 10, 1, 3)),
                 boundary_hessian=np.zeros((1, 10, 1, 3, 3)))
        if (R, phi) != self._k:
            self._line = self.line.prepare_line(prepared=self.prepared, x_m=float(pos[0, 0]), y_m=float(pos[0, 1]))
            self._k = (R, phi)
        pk = self.line.evaluate_line(line=self._line, z_m=z, **b)
        d = pk['fields'][0, :, 0]; g = pk['gradient'][0, :, 0, :]
        for a in (d, g):
            sc = float(np.linalg.norm(a.real)); im = float(np.linalg.norm(a.imag))
            if not all(math.isfinite(v) for v in (im, sc)) or im > self.ratol+self.rrtol*sc:
                raise ValueError('NONREAL_PHYSICAL_METRIC; no unconditional real projection')
        return self.metric.evaluate_point(delta_fields=d.real, delta_gradient_physical=g.real,
                                          Cbar=self.Cbar, mubar=self.mubar, R=R, phi=phi, z=z)

    def solve(self, col, counter=None, **over):
        R = col['R_m']; phi = col['phi']; opts = dict(col['hi_options']); opts.update(over)
        def at_z(z):
            if counter is not None: counter.append(z)
            m = self.metric_point(R, phi, z)
            return {'N': m['N'], 'metric_cyl': m['g_cylindrical'].tolist(), 'mode_weights': [[1.0]+[0.0]*9]}
        return self.hi.solve_hi_column(metric_at_z=at_z, quadrature_module=self.quad, radius_m=R,
                                       radial_weight_m=col['radial_weight_m'], azimuth_weight_rad=col['azimuth_weight_rad'],
                                       surface_ref_kg_m2=col['Sigma_kg_m2'], c_m_s=self.c, **opts)

    def lnN(self, R, phi, z):
        return math.log(self.metric_point(R, phi, z)['N'])


def failure_record():
    fs = sorted(IT0.glob('FAILURE.*.json')); assert len(fs) == 1
    raw = json.loads(fs[0].read_text())
    return raw, dec(raw['failure'])


def threshold(sig=11000., g=5/3, c=299792458.0):
    h0 = g*sig*sig/(g-1); return math.log1p(h0/(c*c))
