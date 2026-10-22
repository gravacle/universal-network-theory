"""Owned UV-tail lapse library (TAIL_SCHEME_DESIGN_V002 sec 1, 3.1; with the R1 revision record's amendments).

INERT library: no file reads at import, no scientific execution at import. numpy + the libm Jn provider.

    t(x) = lambda * int_D T_inf(k) S_T(k) e^{ik.x} d^3k/(2pi)^3,  T_inf = 1/(4 gamma_eff |k|^2),  D = O \\ C
The tail is the operator's own asymptotic lapse symbol over the omitted region, applied to the registered smooth
source S_T (uv_tail_source_roster_c2v001). Lapse only: component 0 of the 10 field components.

Evaluator E1 (exact cylindrical reduction, pointwise at the true azimuth):
    t(R,phi,z) = 2 Re sum_{kz>=0} w_z e^{i kz z} sum_kp w_kp kp S/k^2 pref [c0^D J0(kp R) + sum_j h_j^D J_4j(kp R) cos 4j phi]
    c^D = c^O - c^C (azimuthal Fourier coefficients of the cross-sections); square half-width L at radius kp:
    kp<=L: c0=2pi; L<kp<=sqrt2 L: c0=2pi-8a, c_4j=-8 sin(4ja)/(4j), a=arccos(L/kp); kp>sqrt2 L: 0.  Disc: 2pi inside.
    h_j = 2 c_4j^D (family sign +1 for an outer cube, -1 for a kept cube).
  * k_z >= 0 stored; Hermitian symmetry of the real source gives the real output (sec 1.2a).
  * R0 (K11): bd = 2 Re sum G expm1(i kz z), so bd(z=0) == 0.0; t(z)-t(0) by subtraction is never formed.
  * Quadrature: tensor GL of order o on uniform panels (<= w_perp, w_z) between the breaks; an interval that starts at a
    cube corner L is integrated in a = arccos(L/kp) on panels that keep both the k-width <= w_perp and the phase of the
    highest corner harmonic <= 1.5 rad (IA1/IA1b: removes the sqrt endpoint singularity of a at kp = L+).  Sphere C: tensor part as the cylinder(K,K) plus the piece cyl(K,K)\\sphere(K) on a smooth
    (gamma,u) map (IA3).  Phase rule (sec 1.2c) fail-closed at build; points outside the declared domain raise
    ValueError('UV_TAIL_UNRESOLVED_POINT').
  * Jets: R derivatives by J_m' = (J_{m-1}-J_{m+1})/2, J_m'' = (J_{m-2}-2J_m+J_{m+2})/4; phi on cos 4j phi; z by i kz;
    Cartesian by the V001 sec 1.2 formulas.  Order 1 -> Hessian slot exact zeros.
Units: SI inside (m, 1/m); configuration in kpc and 1/kpc with KPC_M.
"""
import hashlib
import json
import math
import time
from collections import OrderedDict
import numpy as np

CONFIG_SCHEMA = 'UNT_UV_TAIL_CONFIG_C2V001'
STATE_SCHEMA = 'UNT_UV_TAIL_STATE_C2V001'
KPC_M = 3.085677581491367e19
TWO_PI = 2.0 * math.pi
PHASE_LIMIT_RAD = 1.5
TAIL_MEMORY_CAP_BYTES = int(0.6 * 2 ** 30)
CORNER_LRU = 16
RADIUS_SNAP_EPS = 8.0 * np.finfo(float).eps
STAGE_KINDS_CUBE = ('route_a', 'reference', 'body', 'ngc_ring_eval')
STAGE_KINDS_MASK = ('offset', 'fs_columns', 'rfs_columns', 'le_columns', 'fs_rotation', 'le_rotation', 'ngc_sphere_eval')
TEST_ONLY_CERT = 'NONE_TEST_ONLY'
PROVIDER_FILE = 'posix_libm_bessel_jn_provider_c2v001.py'
PROVIDER_SHA256 = 'd6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171'   # sha256 of the sibling provider's bytes (pinned; checked before any fallback load)


class Refusal(ValueError):
    def __init__(self, code, detail=''):
        self.code = code
        super().__init__(code + ((' ' + detail) if detail else ''))


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _sha(text):
    return hashlib.sha256(text.encode() if isinstance(text, str) else text).hexdigest()


def _pos_float(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(float(x)) or float(x) <= 0:
        raise Refusal('UV_TAIL_CONFIG_INVALID', name + ' must be a positive finite number')
    return float(x)


def _strict(d, keys, name):
    if not isinstance(d, dict) or set(d) != set(keys):
        raise Refusal('UV_TAIL_CONFIG_INVALID', '%s keys must be exactly %s, got %s' % (name, sorted(keys), sorted(d) if isinstance(d, dict) else type(d).__name__))


# ============================================================================= configuration
def normalize_config(raw):
    """Strict keys (sec 3.1, with R1 IA2 stars.tail_rule); returns the canonical dict (+schema, +sha256)."""
    _strict(raw, ('enabled', 'outer', 'source_rule', 'gas', 'stars', 'quadrature', 'domain', 'asymptote', 'lapse_only',
                  'jet_order', 'lambda_scale', 'eps_certificate', 'lo_certificate'), 'uv_tail')
    if type(raw['enabled']) is not bool:
        raise Refusal('UV_TAIL_CONFIG_INVALID', 'enabled must be bool')
    o = raw['outer']
    if not isinstance(o, dict) or o.get('shape') not in ('cylinder', 'cube'):
        raise Refusal('UV_TAIL_CONFIG_INVALID', 'outer.shape must be cylinder or cube')
    if o['shape'] == 'cylinder':
        _strict(o, ('shape', 'K_big_inverse_kpc'), 'outer')
        outer = {'shape': 'cylinder', 'K_big_inverse_kpc': _pos_float(o['K_big_inverse_kpc'], 'outer.K_big_inverse_kpc')}
    else:
        _strict(o, ('shape', 'K_out_inverse_kpc'), 'outer')
        outer = {'shape': 'cube', 'K_out_inverse_kpc': _pos_float(o['K_out_inverse_kpc'], 'outer.K_out_inverse_kpc')}
    sr = raw['source_rule']
    if sr == 'continuum_v001':
        source_rule = 'continuum_v001'
    elif isinstance(sr, dict) and sr.get('rule') == 'nodes_v001':
        _strict(sr, ('rule', 'ext_grid'), 'source_rule')
        source_rule = {'rule': 'nodes_v001', 'ext_grid': sr['ext_grid']}
    else:
        raise Refusal('UV_TAIL_CONFIG_INVALID', "source_rule must be 'continuum_v001' or {rule:'nodes_v001',ext_grid}")
    g = raw['gas']; _strict(g, ('interp', 'M_s'), 'gas')
    if g['interp'] != 'lagrange3_s_gl4' or type(g['M_s']) is not int or g['M_s'] < 4:
        raise Refusal('UV_TAIL_CONFIG_INVALID', 'gas')
    s = raw['stars']; _strict(s, ('segment_rule', 'tail_rule'), 'stars')
    if s['segment_rule'] != 'max16_ceil_kdr_plus8' or s['tail_rule'] != 't_panels_40a_phase1p5_gl12':
        raise Refusal('UV_TAIL_CONFIG_INVALID', 'stars')
    q = raw['quadrature']; _strict(q, ('order', 'w_perp_max_inverse_kpc', 'w_z_max_inverse_kpc'), 'quadrature')
    if type(q['order']) is not int or not 2 <= q['order'] <= 64:
        raise Refusal('UV_TAIL_CONFIG_INVALID', 'quadrature.order')
    quad = {'order': q['order'], 'w_perp_max_inverse_kpc': _pos_float(q['w_perp_max_inverse_kpc'], 'w_perp'),
            'w_z_max_inverse_kpc': _pos_float(q['w_z_max_inverse_kpc'], 'w_z')}
    dm = raw['domain']; _strict(dm, ('R_eval_max_kpc', 'z_eval_max_kpc', 'z_src_max_kpc'), 'domain')
    domain = {k: _pos_float(dm[k], 'domain.' + k) for k in dm}
    if raw['asymptote'] != 'EH_exact_minus_quarter' or raw['lapse_only'] is not True:
        raise Refusal('UV_TAIL_CONFIG_INVALID', 'asymptote/lapse_only')
    jo = raw['jet_order']; _strict(jo, ('route_a', 'route_b', 'ngc_eval'), 'jet_order')
    if any(type(jo[k]) is not int or jo[k] not in (1, 2) for k in jo):
        raise Refusal('UV_TAIL_CONFIG_INVALID', 'jet_order')
    lam = _pos_float(raw['lambda_scale'], 'lambda_scale')
    certs = {}
    for name in ('eps_certificate', 'lo_certificate'):
        c = raw[name]
        if c == TEST_ONLY_CERT:
            certs[name] = TEST_ONLY_CERT
        else:
            _strict(c, ('path', 'sha256'), name)
            if not isinstance(c['path'], str) or not isinstance(c['sha256'], str) or len(c['sha256']) != 64 \
                    or any(ch not in '0123456789abcdef' for ch in c['sha256']):
                raise Refusal('UV_TAIL_CONFIG_INVALID', name)
            certs[name] = {'path': c['path'], 'sha256': c['sha256']}
    out = {'schema': CONFIG_SCHEMA, 'enabled': raw['enabled'], 'outer': outer, 'source_rule': source_rule,
           'gas': {'interp': 'lagrange3_s_gl4', 'M_s': g['M_s']}, 'stars': dict(s), 'quadrature': quad, 'domain': domain,
           'asymptote': 'EH_exact_minus_quarter', 'lapse_only': True, 'jet_order': dict(jo), 'lambda_scale': lam, **certs}
    out['sha256'] = _sha(_canon(out))
    return out


def _snap(x):
    r = round(x, 9)
    return r if abs(x - r) <= 1e-12 * max(abs(r), 1.0) else x


def kept_region(stage_kind, truncation, K_inverse_m):
    """Per-stage kept region C (sec 1.1 table): route A/reference/body (and the NGC cube operator) -> cube K always;
    offset and route-B columns/rotations -> the stage mask. truncation = None | {'shape':'cube'} |
    {'shape':'sphere'|'cylinder','kmax_inverse_kpc':x} (driver normalization). K_inverse_m = the cube grid edge."""
    K = _snap(float(K_inverse_m) * KPC_M)
    if not math.isfinite(K) or K <= 0:
        raise Refusal('UV_TAIL_KEPT_INVALID', 'K')
    if stage_kind in STAGE_KINDS_CUBE:
        return {'shape': 'cube', 'K_inverse_kpc': K}
    if stage_kind not in STAGE_KINDS_MASK:
        raise Refusal('UV_TAIL_KEPT_INVALID', 'unknown stage kind ' + repr(stage_kind))
    tr = truncation or {'shape': 'cube'}
    shape = tr.get('shape')
    if shape == 'cube' and tr.get('kmax_inverse_kpc') is None:
        return {'shape': 'cube', 'K_inverse_kpc': K}
    if shape in ('sphere', 'cylinder'):
        Km = _pos_float(tr.get('kmax_inverse_kpc'), 'truncation.kmax_inverse_kpc')
        if Km > K * (1 + 1e-12):
            raise Refusal('UV_TAIL_MASK_EXCEEDS_GRID', '%g > %g' % (Km, K))
        if shape == 'sphere':
            return {'shape': 'sphere', 'K_inverse_kpc': Km}
        return {'shape': 'cylinder', 'K_perp_inverse_kpc': Km, 'K_z_inverse_kpc': K}
    raise Refusal('UV_TAIL_KEPT_INVALID', 'truncation ' + repr(tr))


def _kept_dims(kept):
    s = kept['shape']
    if s == 'cylinder':
        return kept['K_perp_inverse_kpc'], kept['K_z_inverse_kpc']
    return kept['K_inverse_kpc'], kept['K_inverse_kpc']


def _outer_contains(outer, kept):
    """C subset of O?"""
    Kp, Kz = _kept_dims(kept); s = kept['shape']
    if outer['shape'] == 'cylinder':
        Kb = outer['K_big_inverse_kpc']
        if s == 'cube':
            return math.sqrt(2) * Kp <= Kb and Kz <= Kb
        return Kp <= Kb and Kz <= Kb
    Ko = outer['K_out_inverse_kpc']
    return Kp <= Ko and Kz <= Ko


def domain_is_empty(kept, outer):
    """D = O \\ C empty, i.e. O subset of C (e.g. cylinder K_big = K over cube K)."""
    Kp, Kz = _kept_dims(kept); s = kept['shape']
    if outer['shape'] == 'cylinder':
        L = outer['K_big_inverse_kpc']
        if s == 'cube':
            return L <= Kp and L <= Kz
        if s == 'cylinder':
            return L <= Kp and L <= Kz
        return math.sqrt(2) * L <= Kp
    L = outer['K_out_inverse_kpc']
    if s == 'cube':
        return L <= Kp
    if s == 'cylinder':
        return math.sqrt(2) * L <= Kp and L <= Kz
    return math.sqrt(3) * L <= Kp


# ============================================================================= quadrature grid
def _gl(order):
    x, w = np.polynomial.legendre.leggauss(order)
    return x, w


def _uniform(a, b, wmax, order):
    n = max(1, int(math.ceil((b - a) / wmax - 1e-12)))
    x, w = _gl(order); e = np.linspace(a, b, n + 1)
    nodes = np.concatenate([(lo + hi) / 2 + (hi - lo) * x / 2 for lo, hi in zip(e[:-1], e[1:])])
    weights = np.concatenate([(hi - lo) * w / 2 for lo, hi in zip(e[:-1], e[1:])])
    return nodes, weights, float(np.max(np.diff(e))), n


def _alpha(L, b, wmax, order, R_eval_max_kpc):
    """Interval (L, b] integrated in a = arccos(L/k), k = L/cos a, dk = L sin a / cos^2 a da (IA1: removes the sqrt
    endpoint singularity of a at k = L+). Panels in a are marched from a = 0 with
        a_next = min(a + 1.5 / (sqrt2 L R_eval_max + 40),  arccos(L / (L/cos a + w_perp)),  arccos(L/b)),
    i.e. every panel keeps its k-width <= w_perp AND the phase of the highest corner harmonic sin(4j a), 4j <= sqrt2 L R
    + 40, <= 1.5 rad (IA1b: k-uniform panels alone under-resolve sin(4ja) in the first panels; TESTED, module test b/h)."""
    A = math.acos(min(1.0, L / b))
    dah = PHASE_LIMIT_RAD / (math.sqrt(2) * L * R_eval_max_kpc + 40.0)
    e = [0.0]; a = 0.0
    while a < A * (1 - 1e-15):
        k = L / math.cos(a)
        a_k = math.acos(min(1.0, L / (k + wmax)))
        a = min(a + dah, a_k, A)
        e.append(a)
    e = np.array(e)
    x, w = _gl(order)
    al = np.concatenate([(lo + hi) / 2 + (hi - lo) * x / 2 for lo, hi in zip(e[:-1], e[1:])])
    wa = np.concatenate([(hi - lo) * w / 2 for lo, hi in zip(e[:-1], e[1:])])
    k = L / np.cos(al)
    wk = wa * L * np.sin(al) / np.cos(al) ** 2
    return k, wk, float(np.max(np.diff(L / np.cos(e)))), int(len(e) - 1)


def _grid(kept, outer, quad, R_eval_max_kpc):
    """k_perp and k_z >= 0 nodes (1/kpc), weights, corner families, widths."""
    o = quad['order']; wp = quad['w_perp_max_inverse_kpc']; wz = quad['w_z_max_inverse_kpc']
    s = kept['shape']; Kp, Kz = _kept_dims(kept)
    B = {0.0}; starts = []
    if s == 'cube':
        B |= {Kp, math.sqrt(2) * Kp}; starts.append(Kp)
    else:
        B.add(Kp)
    if outer['shape'] == 'cylinder':
        top = outer['K_big_inverse_kpc']; topz = top; B.add(top)
    else:
        Ko = outer['K_out_inverse_kpc']; B |= {Ko, math.sqrt(2) * Ko}; starts.append(Ko)
        top = math.sqrt(2) * Ko; topz = Ko
    B = sorted(b for b in B if b <= top * (1 + 1e-15))
    kp = []; wk = []; widths = []; intervals = []
    for a, b in zip(B[:-1], B[1:]):
        if any(abs(a - L) <= 1e-12 * L for L in starts):
            n_, w_, wd, npan = _alpha(a, b, wp, o, R_eval_max_kpc); rule = 'alpha_phase'
        else:
            n_, w_, wd, npan = _uniform(a, b, wp, o); rule = 'uniform'
        kp.append(n_); wk.append(w_); widths.append(wd); intervals.append(dict(lo=a, hi=b, rule=rule, panels=npan))
    Bz = sorted({0.0, Kz, topz})
    kz = []; wzz = []; zwidths = []; zint = []
    for a, b in zip(Bz[:-1], Bz[1:]):
        n_, w_, wd, npan = _uniform(a, b, wz, o)
        kz.append(n_); wzz.append(w_); zwidths.append(wd); zint.append(dict(lo=a, hi=b, panels=npan))
    fam = []
    if s == 'cube':
        fam.append(dict(L=Kp, Lz=Kz, sign=-1))
    if outer['shape'] == 'cube':
        fam.append(dict(L=outer['K_out_inverse_kpc'], Lz=outer['K_out_inverse_kpc'], sign=+1))
    return dict(kp=np.concatenate(kp), wkp=np.concatenate(wk), kz=np.concatenate(kz), wz=np.concatenate(wzz),
                w_perp_actual=max(widths), w_z_actual=max(zwidths), kp_intervals=intervals, kz_intervals=zint,
                families=fam, top=top, topz=topz)


def _c0_square(L, Lz, kp, kz):
    a = np.arccos(np.minimum(1.0, L / np.maximum(kp, 1e-300)))
    v = np.where(kp <= L, TWO_PI, np.where(kp <= math.sqrt(2) * L, TWO_PI - 8.0 * a, 0.0))
    return v[:, None] * (kz <= Lz)[None, :]


def _c0_disc(Kp, Kz, kp, kz):
    return TWO_PI * ((kp <= Kp)[:, None] & (kz <= Kz)[None, :])


def _c0_D(kept, outer, kp, kz):
    """c0^D = c0^O - c0^C on the tensor nodes (1/kpc units). Sphere C enters the tensor part as cylinder(K,K)."""
    if outer['shape'] == 'cylinder':
        L = outer['K_big_inverse_kpc']; cO = _c0_disc(L, L, kp, kz)
    else:
        L = outer['K_out_inverse_kpc']; cO = _c0_square(L, L, kp, kz)
    s = kept['shape']; Kp, Kz = _kept_dims(kept)
    cC = _c0_square(Kp, Kz, kp, kz) if s == 'cube' else _c0_disc(Kp, Kz, kp, kz)
    return cO - cC


def _family_h(sign, L, kp_kpc, jm):
    """h_j = 2 c_4j^D of one square family (sign +1 outer cube, -1 kept cube), j = 1..jm, on L < kp <= sqrt2 L:
    c_4j(square) = -8 sin(4j a)/(4j), a = arccos(L/kp)  ->  h_j = -sign * 4 sin(4j a) / j."""
    al = np.arccos(np.minimum(1.0, L / np.asarray(kp_kpc, float)))
    js = np.arange(1, jm + 1)
    return -sign * 4.0 * np.sin(4.0 * js[:, None] * al[None, :]) / js[:, None]


def azimuthal_W(kp_kpc, kz_kpc, R_kpc, phi, kept, outer, jn):
    """W_D(kp, kz; R, phi) = int_{psi in D} exp(i kp R cos(psi - phi)) dpsi by the library's own coefficient code
    (c0^D J0 + sum_j h_j J_4j cos 4j phi; tensor-part semantics, i.e. a sphere C as cylinder(K,K)). Test hook."""
    kp = np.atleast_1d(np.asarray(kp_kpc, float)); kz = np.atleast_1d(np.asarray(kz_kpc, float))
    W = _c0_D(kept, outer, kp, kz) * jn.j0(kp * R_kpc)[:, None]
    fams = []
    if kept['shape'] == 'cube':
        fams.append((kept['K_inverse_kpc'], kept['K_inverse_kpc'], -1))
    if outer['shape'] == 'cube':
        fams.append((outer['K_out_inverse_kpc'], outer['K_out_inverse_kpc'], +1))
    for L, Lz, sign in fams:
        jm = int(math.ceil((math.sqrt(2) * L * R_kpc + 40.0) / 4.0))
        inzone = (kp > L) & (kp <= math.sqrt(2) * L)
        h = _family_h(sign, L, np.where(inzone, kp, L), jm) * inzone[None, :]
        Jm = np.array([jn.jn(4 * j, kp * R_kpc) for j in range(1, jm + 1)])
        cw = np.cos(4.0 * np.arange(1, jm + 1) * phi)
        W = W + (np.sum(h * Jm * cw[:, None], axis=0))[:, None] * (kz <= Lz)[None, :]
    return W


def _sphere_piece(K, wp, wz, order):
    """cyl(K,K) \\ sphere(K): kp = K cos g (g in [0,pi/2], dkp = K sin g dg), kz = K sin g + K(1-sin g) u (IA3)."""
    n_g = max(1, int(math.ceil((math.pi / 2) * K / wp - 1e-12)))
    x, w = _gl(order); e = np.linspace(0.0, math.pi / 2, n_g + 1)
    g = np.concatenate([(lo + hi) / 2 + (hi - lo) * x / 2 for lo, hi in zip(e[:-1], e[1:])])
    wg = np.concatenate([(hi - lo) * w / 2 for lo, hi in zip(e[:-1], e[1:])])
    kp = K * np.cos(g); wkp = wg * K * np.sin(g)
    kz_l = []; w_l = []; gi = []
    for i, gg in enumerate(g):
        lo = K * math.sin(gg); ln = K - lo
        n_u = max(1, int(math.ceil(ln / wz - 1e-12)))
        eu = np.linspace(lo, K, n_u + 1)
        kz_l.append(np.concatenate([(a + b) / 2 + (b - a) * x / 2 for a, b in zip(eu[:-1], eu[1:])]))
        w_l.append(np.concatenate([(b - a) * w / 2 for a, b in zip(eu[:-1], eu[1:])]))
        gi.append(np.full(order * n_u, i))
    return kp, wkp, np.concatenate(kz_l), np.concatenate(w_l), np.concatenate(gi)


# ============================================================================= state
class TailState:
    """Built tail of one field state. Picklable (the provider and caches are rebuilt on demand)."""

    def __init__(self, *, empty, record, arrays=None, jn_provider=None):
        self.empty = bool(empty); self.record = record; self._a = arrays or {}
        self._jn = jn_provider; self._corner_cache = OrderedDict(); self._ring_extra = OrderedDict()
        self._sphere_cache = OrderedDict(); self._line_cache = OrderedDict()
        self.diagnostics = {'on_demand_radius_builds': 0, 'corner_table_builds': 0}
        self.digest = self._digest()

    # -- custody
    def _digest(self):
        h = hashlib.sha256(); h.update(_canon(self.record).encode())
        for k in sorted(self._a):
            a = np.ascontiguousarray(self._a[k])
            h.update(('|%s|%s|%s|' % (k, a.dtype, a.shape)).encode()); h.update(a.tobytes())
        return h.hexdigest()

    def __getstate__(self):
        d = dict(self.__dict__); d['_jn'] = None
        d['_corner_cache'] = OrderedDict(); d['_ring_extra'] = OrderedDict(); d['_sphere_cache'] = OrderedDict(); d['_line_cache'] = OrderedDict()
        return d

    def _provider(self):
        if self._jn is None:
            from importlib import util as _u
            import os as _o
            here = _o.path.dirname(_o.path.abspath(__file__))
            path = _o.path.join(here, PROVIDER_FILE)
            with open(path, 'rb') as fh:
                if hashlib.sha256(fh.read()).hexdigest() != PROVIDER_SHA256:
                    raise Refusal('UV_TAIL_PIN_MISMATCH', path)
            spec = _u.spec_from_file_location('uvt_jn_provider_c2v001', path)
            m = _u.module_from_spec(spec); spec.loader.exec_module(m)
            self._jn = m.create_provider()
        return self._jn

    def to_arrays(self):
        return {k: np.array(v, copy=True) for k, v in self._a.items()}

    @classmethod
    def from_arrays(cls, arrays, record, jn_provider=None, expected_digest=None):
        st = cls(empty=record.get('empty', False), record=record, arrays={k: np.asarray(v) for k, v in arrays.items()},
                 jn_provider=jn_provider)
        if expected_digest is not None and st.digest != expected_digest:
            raise Refusal('UV_TAIL_STATE_DIGEST_MISMATCH')
        return st

    # -- geometry helpers
    def _check_point(self, R, z):
        dm = self.record['domain_m']
        if not (math.isfinite(R) and math.isfinite(z)) or R > dm['R_eval_max_m'] or abs(z) > dm['z_eval_max_m']:
            raise ValueError('UV_TAIL_UNRESOLVED_POINT R=%r z=%r' % (R, z))

    def _ring(self, R):
        """(radius used, ring table (3,Nz)) with radius snapping to the declared radii."""
        radii = self._a['ring_radii_m']
        if len(radii):
            i = int(np.searchsorted(radii, R))
            for j in (i - 1, i):
                if 0 <= j < len(radii) and abs(radii[j] - R) <= RADIUS_SNAP_EPS * radii[j]:
                    return float(radii[j]), self._a['ring_tables'][j]
        key = float(R)
        if key in self._ring_extra:
            v = self._ring_extra.pop(key); self._ring_extra[key] = v; return key, v
        tab = _ring_tables(self, np.array([key]))[0]
        self.diagnostics['on_demand_radius_builds'] += 1
        self._ring_extra[key] = tab
        if len(self._ring_extra) > CORNER_LRU:
            self._ring_extra.popitem(last=False)
        return key, tab

    def _corner(self, f, R):
        key = (f, R)
        if key in self._corner_cache:
            v = self._corner_cache.pop(key); self._corner_cache[key] = v; return v
        fam = self.record['families'][f]
        kpc = self._a['corner_kp_%d' % f]           # 1/m
        Mc = self._a['corner_M_%d' % f]             # (Nc, nzl) complex
        L = fam['L_inverse_kpc']
        jm = int(math.ceil((math.sqrt(2) * L * (R / KPC_M) + 40.0) / 4.0))
        jn = self._provider().jn
        x = kpc * R
        J = {}
        for j in range(1, jm + 1):
            for m in (4 * j - 2, 4 * j - 1, 4 * j, 4 * j + 1, 4 * j + 2):
                if m not in J:
                    J[m] = jn(m, x)
        js = np.arange(1, jm + 1)
        h = _family_h(fam['sign'], L, kpc * KPC_M, jm)                                      # (jm, Nc)
        D0 = h * np.array([J[4 * j] for j in js])
        D1 = h * kpc[None, :] * np.array([(J[4 * j - 1] - J[4 * j + 1]) / 2 for j in js])
        D2 = h * (kpc * kpc)[None, :] * np.array([(J[4 * j - 2] - 2 * J[4 * j] + J[4 * j + 2]) / 4 for j in js])
        G = np.empty((3, jm, Mc.shape[1]), complex)
        for d, D in enumerate((D0, D1, D2)):
            G[d] = (D @ Mc.real) + 1j * (D @ Mc.imag)
        self._corner_cache[key] = G; self.diagnostics['corner_table_builds'] += 1
        if len(self._corner_cache) > CORNER_LRU * max(1, len(self.record['families'])):
            self._corner_cache.popitem(last=False)
        return G

    def _sphere_B(self, R):
        if R in self._sphere_cache:
            v = self._sphere_cache.pop(R); self._sphere_cache[R] = v; return v
        P = self._provider(); kp = self._a['sph_kp']; x = kp * R
        B = np.stack([P.j0(x), -kp * P.j1(x), kp * kp * (P.jn(2, x) - P.j0(x)) / 2])[:, self._a['sph_gi']]   # per entry
        self._sphere_cache[R] = B
        if len(self._sphere_cache) > CORNER_LRU:
            self._sphere_cache.popitem(last=False)
        return B

    # -- core evaluator: cylindrical jets at one radius, many azimuths and heights
    def _H(self, R, phis, need_phi, need_R2):
        """Combined k_z vectors at radius R for each azimuth: dict of (nphi, Nz) complex arrays."""
        Ru, G = self._ring(R)
        n = len(phis)
        H = {'0': np.repeat(G[0][None, :], n, 0), '1': np.repeat(G[1][None, :], n, 0)}
        if need_R2:
            H['2'] = np.repeat(G[2][None, :], n, 0)
        if need_phi:
            H['p0'] = np.zeros_like(H['0']); H['p1'] = np.zeros_like(H['0'])
            if need_R2:
                H['pp0'] = np.zeros_like(H['0'])
        for f in range(len(self.record['families'])):
            if Ru == 0.0:
                break
            Gf = self._corner(f, Ru); jm = Gf.shape[1]; nzl = Gf.shape[2]
            m = 4.0 * np.arange(1, jm + 1)
            C = np.cos(np.outer(phis, m)); S = np.sin(np.outer(phis, m))
            H['0'][:, :nzl] += C @ Gf[0]; H['1'][:, :nzl] += C @ Gf[1]
            if need_R2:
                H['2'][:, :nzl] += C @ Gf[2]
            if need_phi:
                H['p0'][:, :nzl] += (-m[None, :] * S) @ Gf[0]; H['p1'][:, :nzl] += (-m[None, :] * S) @ Gf[1]
                if need_R2:
                    H['pp0'][:, :nzl] += (-(m * m)[None, :] * C) @ Gf[0]
        return Ru, H

    def cyl_jets(self, R, phis, zs, order=2, _cache=False):
        """Cylindrical derivatives at (R, phis[i], zs[j]): dict of (nphi, nz) float64 arrays
        keys f, fR, fp, fz (+ fRR, fRp, fpp, fRz, fpz, fzz for order 2)."""
        phis = np.atleast_1d(np.asarray(phis, float)); zs = np.atleast_1d(np.asarray(zs, float))
        for z in zs:
            self._check_point(R, z)
        need2 = order >= 2
        if _cache and len(phis) == 1:
            key = ('H', float(R), float(phis[0]), need2)
            if key in self._line_cache:
                Ru, H = self._line_cache[key]
            else:
                Ru, H = self._H(R, phis, True, need2); self._line_cache[key] = (Ru, H)
                if len(self._line_cache) > 64:
                    self._line_cache.popitem(last=False)
        else:
            Ru, H = self._H(R, phis, True, need2)
        kz = self._a['kz']
        E = np.exp(1j * np.outer(kz, zs))
        Ez = (1j * kz)[:, None] * E
        def re(Hm, Em):
            return 2.0 * (Hm.real @ Em.real - Hm.imag @ Em.imag)
        out = {'f': re(H['0'], E), 'fR': re(H['1'], E), 'fp': re(H['p0'], E), 'fz': re(H['0'], Ez)}
        if need2:
            Ezz = (-(kz * kz))[:, None] * E
            out.update(fRR=re(H['2'], E), fRp=re(H['p1'], E), fpp=re(H['pp0'], E), fRz=re(H['1'], Ez),
                       fpz=re(H['p0'], Ez), fzz=re(H['0'], Ezz))
        if 'sph_A' in self._a:
            B = self._sphere_B(Ru); A = self._a['sph_A']; kzs = self._a['sph_kz']
            Es = np.exp(1j * np.outer(kzs, zs)); Esz = (1j * kzs)[:, None] * Es
            s0 = B[0] * A; s1 = B[1] * A
            def rs(v, Em):
                return 2.0 * (v.real @ Em.real - v.imag @ Em.imag)[None, :]
            out['f'] = out['f'] + rs(s0, Es); out['fR'] = out['fR'] + rs(s1, Es); out['fz'] = out['fz'] + rs(s0, Esz)
            if need2:
                s2 = B[2] * A; Eszz = (-(kzs * kzs))[:, None] * Es
                out['fRR'] = out['fRR'] + rs(s2, Es); out['fRz'] = out['fRz'] + rs(s1, Esz); out['fzz'] = out['fzz'] + rs(s0, Eszz)
        return out

    # -- public evaluation API
    def jet(self, pos, order):
        """boundary_fields (n,10,1), boundary_gradient (n,10,1,3), boundary_hessian (n,10,1,3,3); float64;
        component 0 only; order 1 -> Hessian exact zeros; empty -> the reviewed np.zeros (prep v007 L214-218)."""
        pos = np.asarray(pos, dtype=float)
        n = len(pos)
        fields = np.zeros((n, 10, 1)); grad = np.zeros((n, 10, 1, 3)); hess = np.zeros((n, 10, 1, 3, 3))
        if self.empty:
            return dict(boundary_fields=fields, boundary_gradient=grad, boundary_hessian=hess)
        if order not in (1, 2):
            raise Refusal('UV_TAIL_JET_ORDER')
        if pos.ndim != 2 or pos.shape[1] != 3 or not np.all(np.isfinite(pos)):
            raise ValueError('UV_TAIL_UNRESOLVED_POINT nonfinite or misshaped positions')
        for i in range(n):
            f, g, H = self._cart(pos[i, 0], pos[i, 1], pos[i, 2], order)
            fields[i, 0, 0] = f; grad[i, 0, 0, :] = g
            if order == 2:
                hess[i, 0, 0] = H
        return dict(boundary_fields=fields, boundary_gradient=grad, boundary_hessian=hess)

    def _snap_radius(self, R):
        radii = self._a['ring_radii_m']
        if len(radii):
            i = int(np.searchsorted(radii, R))
            for j in (i - 1, i):
                if 0 <= j < len(radii) and abs(radii[j] - R) <= RADIUS_SNAP_EPS * radii[j]:
                    return float(radii[j])
        return float(R)

    def _cart(self, x, y, z, order):
        R = self._snap_radius(math.hypot(x, y)); phi = math.atan2(y, x)
        j = self.cyl_jets(R, [phi], [z], order, _cache=True)
        J = {k: float(v[0, 0]) for k, v in j.items()}
        return cyl_to_cart(R, phi, J, order)

    def jet_for_line(self, line, z_m, order):
        return self.jet(np.array([[float(line['x_m']), float(line['y_m']), float(z_m)]]), order)

    def lapse_pair(self, x_m, y_m, z_m, ns=1):
        """(b0, bd), each shape (ns,) float64: b0 = t(x,y,0), bd = 2 Re sum H0 expm1(i kz z) (R0; bd(0) == 0.0)."""
        if ns != 1:
            raise Refusal('UV_TAIL_SINGLE_SOURCE_FAMILY_REQUIRED', 'ns=%r' % ns)
        if self.empty:
            return np.zeros(ns), np.zeros(ns)
        R = math.hypot(x_m, y_m); phi = math.atan2(y_m, x_m)
        self._check_point(R, 0.0); self._check_point(R, z_m)
        key = (float(x_m), float(y_m))
        if key in self._line_cache:
            H0, s0, kzs = self._line_cache[key]
        else:
            Ru, H = self._H(R, np.array([phi]), False, False)
            H0 = H['0'][0]; s0 = None; kzs = None
            if 'sph_A' in self._a:
                s0 = self._sphere_B(Ru)[0] * self._a['sph_A']; kzs = self._a['sph_kz']
            self._line_cache[key] = (H0, s0, kzs)
            if len(self._line_cache) > 64:
                self._line_cache.popitem(last=False)
        kz = self._a['kz']
        em = np.expm1(1j * kz * float(z_m))
        b0 = 2.0 * float(np.sum(H0.real)); bd = 2.0 * float(H0.real @ em.real - H0.imag @ em.imag)
        if s0 is not None:
            ems = np.expm1(1j * kzs * float(z_m))
            b0 = b0 + 2.0 * float(np.sum(s0.real)); bd = bd + 2.0 * float(s0.real @ ems.real - s0.imag @ ems.imag)
        return np.array([b0]), np.array([bd + 0.0])

    def value(self, pos):
        return self.jet(pos, 1)['boundary_fields'][:, 0, 0]

    def gradient(self, pos):
        return self.jet(pos, 1)['boundary_gradient'][:, 0, 0, :]


def cyl_to_cart(R, phi, J, order=2):
    """V001 sec 1.2 Cartesian conversion; at R == 0 the m=0 limits (f_R -> 0, f_xx = f_yy = f_RR)."""
    c, s = math.cos(phi), math.sin(phi)
    f = J['f']
    if R == 0.0:
        g = np.array([0.0, 0.0, J['fz']])
        H = np.zeros((3, 3))
        if order == 2:
            H = np.array([[J['fRR'], 0.0, 0.0], [0.0, J['fRR'], 0.0], [0.0, 0.0, J['fzz']]])
        return f, g, H
    fR, fp, fz = J['fR'], J['fp'], J['fz']
    g = np.array([c * fR - s / R * fp, s * fR + c / R * fp, fz])
    if order < 2:
        return f, g, np.zeros((3, 3))
    fRR, fRp, fpp, fRz, fpz, fzz = J['fRR'], J['fRp'], J['fpp'], J['fRz'], J['fpz'], J['fzz']
    hxx = c * c * fRR + s * s / R * fR + s * s / R ** 2 * fpp - 2 * c * s / R * fRp + 2 * c * s / R ** 2 * fp
    hyy = s * s * fRR + c * c / R * fR + c * c / R ** 2 * fpp + 2 * c * s / R * fRp - 2 * c * s / R ** 2 * fp
    hxy = c * s * fRR - c * s / R * fR - c * s / R ** 2 * fpp + (c * c - s * s) / R * fRp - (c * c - s * s) / R ** 2 * fp
    hxz = c * fRz - s / R * fpz; hyz = s * fRz + c / R * fpz
    return f, g, np.array([[hxx, hxy, hxz], [hxy, hyy, hyz], [hxz, hyz, fzz]])


# ============================================================================= build
def _block_rows(nz):
    return int(max(16, min(512, (2 ** 27) // max(1, 64 * nz))))


def _ring_tables(state, radii_m):
    """Ring tables G_R^{(d)}(k_z), d = 0,1,2 for the given radii (recomputes S blocks from P, F)."""
    a = state._a; rec = state.record
    kp = a['kp']; wkp = a['wkp']; kz = a['kz']; wz = a['wz']; P = a['P']; F = a['F']; c0 = None
    pref = rec['pref']
    kept = rec['kept']; outer = rec['outer']
    jn = state._provider()
    radii_m = np.asarray(radii_m, float)
    out = np.zeros((len(radii_m), 3, len(kz)), complex)
    blk = _block_rows(len(kz))
    Fr = np.ascontiguousarray(F.real); Fi = np.ascontiguousarray(F.imag)
    for s0 in range(0, len(kp), blk):
        sl = slice(s0, min(s0 + blk, len(kp)))
        k = kp[sl]
        c0 = _c0_D(kept, outer, k * KPC_M, kz * KPC_M)
        if not np.any(c0):
            continue
        Sr = P[sl] @ Fr.T; Si = P[sl] @ Fi.T
        fac = (pref * wkp[sl] * k)[:, None] * wz[None, :] / (k[:, None] ** 2 + kz[None, :] ** 2) * c0
        Ar = Sr * fac; Ai = Si * fac
        x = np.outer(radii_m, k)
        J0 = jn.j0(x); J1 = jn.j1(x); J2 = jn.jn(2, x)
        for d, Bd in enumerate((J0, -k[None, :] * J1, (k * k)[None, :] * (J2 - J0) / 2)):
            out[:, d, :] += (Bd @ Ar) + 1j * (Bd @ Ai)
    return out


def build(*, config, kept, roster, gamma_eff, c_m_s, eval_radii_m, jn_provider, i1t, stage_kind=None):
    """Build the TailState of one field state (sec 3.1). Empty domain -> TailState(empty=True), no arithmetic."""
    t_start = time.time()
    if not isinstance(config, dict) or config.get('schema') != CONFIG_SCHEMA:
        raise Refusal('UV_TAIL_CONFIG_NOT_NORMALIZED')
    if config['sha256'] != _sha(_canon({k: v for k, v in config.items() if k != 'sha256'})):
        raise Refusal('UV_TAIL_CONFIG_DIGEST_MISMATCH')
    if not config['enabled']:
        raise Refusal('UV_TAIL_DISABLED')
    if config['source_rule'] != 'continuum_v001':
        raise Refusal('UV_TAIL_NODES_V001_IS_A_PACKET', 'evaluate nodes_v001 with nodes_v001_packet + line v002')
    if not math.isfinite(gamma_eff) or gamma_eff <= 0 or not math.isfinite(c_m_s) or c_m_s <= 0:
        raise Refusal('UV_TAIL_PHYSICAL_INVALID')
    outer = config['outer']
    if not _outer_contains(outer, kept) and not domain_is_empty(kept, outer):
        raise Refusal('UV_TAIL_OUTER_DOES_NOT_CONTAIN_KEPT')
    dm = config['domain']
    domain_m = {'R_eval_max_m': dm['R_eval_max_kpc'] * KPC_M, 'z_eval_max_m': dm['z_eval_max_kpc'] * KPC_M,
                'z_src_max_m': dm['z_src_max_kpc'] * KPC_M}
    certs = {k: config[k] for k in ('eps_certificate', 'lo_certificate')}
    production_admissible = all(v != TEST_ONLY_CERT for v in certs.values())
    for name, c in certs.items():
        if c != TEST_ONLY_CERT:
            try:
                with open(c['path'], 'rb') as fh:
                    got = hashlib.sha256(fh.read()).hexdigest()
            except OSError:
                raise Refusal('UV_TAIL_CERTIFICATE_MISSING', name)
            if got != c['sha256']:
                raise Refusal('UV_TAIL_CERTIFICATE_MISMATCH', name)
    if not isinstance(i1t, dict) or i1t.get('verdict') not in ('PASS', 'NOT_APPLICABLE_SYNTHETIC'):
        raise Refusal('UV_TAIL_I1T_MISSING')
    if i1t.get('verdict') == 'NOT_APPLICABLE_SYNTHETIC':
        if getattr(roster, 'kind', None) != 'synthetic':
            raise Refusal('UV_TAIL_I1T_MISSING', 'synthetic exemption for a registered roster')
        production_admissible = False
    radii = np.unique(np.asarray(eval_radii_m, dtype=float))
    if not np.all(np.isfinite(radii)) or np.any(radii < 0) or (len(radii) and radii[-1] > domain_m['R_eval_max_m']):
        raise ValueError('UV_TAIL_UNRESOLVED_POINT eval radius outside the declared domain')
    pref = config['lambda_scale'] / (4.0 * gamma_eff * (2.0 * math.pi) ** 3)
    base = dict(schema=STATE_SCHEMA, config_sha256=config['sha256'], kept=kept, outer=outer, stage_kind=stage_kind,
                lambda_scale=config['lambda_scale'], gamma_eff=gamma_eff, c_m_s=c_m_s, domain_m=domain_m,
                eps_certificate=certs['eps_certificate'], lo_certificate=certs['lo_certificate'], i1t=i1t,
                production_admissible=production_admissible, jet_order=config['jet_order'], pref=pref)
    if domain_is_empty(kept, outer):
        rec = dict(base, empty=True, roster_digest=None, families=[])
        st = TailState(empty=True, record=rec, arrays={}, jn_provider=None)
        st.diagnostics['build_seconds'] = time.time() - t_start
        return st
    g = _grid(kept, outer, config['quadrature'], dm['R_eval_max_kpc'])
    ext = roster.extent()
    R_src = ext['R_src_max_m']
    if ext['gas_z_abs_max_m'] > domain_m['z_src_max_m']:
        raise Refusal('UV_TAIL_SOURCE_OUTSIDE_DECLARED_EXTENT', 'gas |z| %.6g kpc > %.6g' % (ext['gas_z_abs_max_m'] / KPC_M, dm['z_src_max_kpc']))
    z_src = max(domain_m['z_src_max_m'], ext['stars_24h_m'])
    ph_perp = g['w_perp_actual'] * (dm['R_eval_max_kpc'] + R_src / KPC_M)
    ph_z = g['w_z_actual'] * (dm['z_eval_max_kpc'] + z_src / KPC_M)
    if ph_perp > PHASE_LIMIT_RAD * (1 + 1e-12) or ph_z > PHASE_LIMIT_RAD * (1 + 1e-12):
        raise Refusal('UV_TAIL_PHASE_RULE', 'perp %.4f z %.4f rad' % (ph_perp, ph_z))
    kp = g['kp'] / KPC_M; wkp = g['wkp'] / KPC_M; kz = g['kz'] / KPC_M; wz = g['wz'] / KPC_M
    sph = None
    if kept['shape'] == 'sphere':
        Ks = kept['K_inverse_kpc']
        skp, swkp, skz, swz, sgi = _sphere_piece(Ks, config['quadrature']['w_perp_max_inverse_kpc'],
                                                 config['quadrature']['w_z_max_inverse_kpc'], config['quadrature']['order'])
        sph = dict(kp=skp / KPC_M, wkp=swkp / KPC_M, kz=skz / KPC_M, wz=swz / KPC_M, gi=sgi)
    # memory estimate (K15 cap)
    nz = len(kz); nR = len(radii)
    fam_rec = []
    for f in g['families']:
        sel = (g['kp'] > f['L']) & (g['kp'] <= math.sqrt(2) * f['L'])
        nzl = int(np.sum(g['kz'] <= f['Lz']))
        jm = int(math.ceil((math.sqrt(2) * f['L'] * dm['R_eval_max_kpc'] + 40.0) / 4.0))
        fam_rec.append(dict(L_inverse_kpc=f['L'], Lz_inverse_kpc=f['Lz'], sign=f['sign'], n_kp=int(sel.sum()), n_kz=nzl, j_max_at_R_eval_max=jm))
    r_est = 1 + (roster.gas.present.sum() if getattr(roster, 'gas', None) is not None else 0)
    mem = (nR * 3 * nz * 16 + len(kp) * r_est * 8 + nz * r_est * 16 + _block_rows(nz) * nz * 8 * 6
           + sum(fr['n_kp'] * fr['n_kz'] * 16 + CORNER_LRU * 3 * fr['j_max_at_R_eval_max'] * fr['n_kz'] * 16 for fr in fam_rec)
           + (0 if sph is None else len(sph['kz']) * 40 + CORNER_LRU * 3 * len(sph['kp']) * 8))
    if mem > TAIL_MEMORY_CAP_BYTES:
        raise Refusal('UV_TAIL_MEMORY_CAP', 'estimate %.3f GiB' % (mem / 2 ** 30))
    j0 = jn_provider.j0
    P = roster.radial_factors(kp, j0); F = roster.vertical_factors(kz, c_m_s)
    P = np.ascontiguousarray(P, dtype=float); F = np.ascontiguousarray(F, dtype=complex)
    arrays = dict(kp=kp, wkp=wkp, kz=kz, wz=wz, P=P, F=F, ring_radii_m=radii)
    # corner source blocks M_c (A restricted to the corner zone and kz <= Lz), shell integrals
    Kmin = min(_kept_dims(kept))
    shell_edges = Kmin + np.arange(0, int(math.ceil(math.sqrt(g['top'] ** 2 + g['topz'] ** 2) - Kmin)) + 2, dtype=float)
    shells = np.zeros((len(shell_edges) - 1, 3))
    Fr = np.ascontiguousarray(F.real); Fi = np.ascontiguousarray(F.imag)
    blk = _block_rows(nz)
    Mc = [[] for _ in g['families']]
    kz_kpc = kz * KPC_M
    ring = np.zeros((len(radii), 3, nz), complex)
    for s0 in range(0, len(kp), blk):
        sl = slice(s0, min(s0 + blk, len(kp)))
        k = kp[sl]; kk = k * KPC_M
        c0 = _c0_D(kept, outer, kk, kz_kpc)
        corner_rows = [((kk > f['L']) & (kk <= math.sqrt(2) * f['L'])) for f in g['families']]
        if not np.any(c0) and not any(np.any(cr) for cr in corner_rows):
            continue
        Sr = P[sl] @ Fr.T; Si = P[sl] @ Fi.T
        fac = (pref * wkp[sl] * k)[:, None] * wz[None, :] / (k[:, None] ** 2 + kz[None, :] ** 2)
        for fi, (f, cr) in enumerate(zip(g['families'], corner_rows)):
            if np.any(cr):
                nzl = fam_rec[fi]['n_kz']
                Mc[fi].append((Sr[cr, :nzl] + 1j * Si[cr, :nzl]) * fac[cr, :nzl])
        if len(radii) and np.any(c0):
            Ar = Sr * fac * c0; Ai = Si * fac * c0
            x = np.outer(radii, k)
            J0 = jn_provider.j0(x); J1 = jn_provider.j1(x); J2 = jn_provider.jn(2, x)
            for d, Bd in enumerate((J0, -k[None, :] * J1, (k * k)[None, :] * (J2 - J0) / 2)):
                ring[:, d, :] += (Bd @ Ar) + 1j * (Bd @ Ai)
        absA = np.hypot(Sr, Si) * fac * c0 * 2.0     # x2: the k_z < 0 half
        kmag = np.sqrt(kk[:, None] ** 2 + kz_kpc[None, :] ** 2)
        idx = np.clip(np.searchsorted(shell_edges, kmag, side='right') - 1, 0, len(shells) - 1)
        km = kmag / KPC_M
        for a_ in range(3):
            shells[:, a_] += np.bincount(idx.ravel(), weights=(absA * km ** a_).ravel(), minlength=len(shells))
    for fi in range(len(g['families'])):
        f = g['families'][fi]; sel = (g['kp'] > f['L']) & (g['kp'] <= math.sqrt(2) * f['L'])
        arrays['corner_kp_%d' % fi] = kp[sel]
        arrays['corner_M_%d' % fi] = np.concatenate(Mc[fi], axis=0) if Mc[fi] else np.zeros((0, fam_rec[fi]['n_kz']), complex)
    if sph is not None:
        Pg = np.ascontiguousarray(roster.radial_factors(sph['kp'], j0), dtype=float)
        A = np.zeros(len(sph['kz']), complex)
        for s0 in range(0, len(sph['kz']), 4096):
            sl = slice(s0, min(s0 + 4096, len(sph['kz'])))
            Fs = roster.vertical_factors(sph['kz'][sl], c_m_s)
            gi = sph['gi'][sl]
            S = np.einsum('nr,nr->n', Pg[gi], Fs)
            kpn = sph['kp'][gi]
            A[sl] = pref * TWO_PI * sph['wkp'][gi] * kpn * sph['wz'][sl] * S / (kpn ** 2 + sph['kz'][sl] ** 2)
            kmag = np.sqrt(kpn ** 2 + sph['kz'][sl] ** 2) * KPC_M
            idx = np.clip(np.searchsorted(shell_edges, kmag, side='right') - 1, 0, len(shells) - 1)
            for a_ in range(3):
                shells[:, a_] += np.bincount(idx, weights=2.0 * np.abs(A[sl]) * (kmag / KPC_M) ** a_, minlength=len(shells))
        arrays.update(sph_kp=sph['kp'], sph_kz=sph['kz'], sph_A=A, sph_gi=sph['gi'].astype(np.int64))
    arrays['shell_edges_inverse_kpc'] = shell_edges
    arrays['shell_integrals'] = shells
    rec = dict(base, empty=False, roster_digest=roster.digest(), roster_record=roster.record(), families=fam_rec,
               quadrature=dict(order=config['quadrature']['order'], N_perp=int(len(kp)), N_z_plus=int(nz),
                               w_perp_actual_inverse_kpc=g['w_perp_actual'], w_z_actual_inverse_kpc=g['w_z_actual'],
                               kp_intervals=g['kp_intervals'], kz_intervals=g['kz_intervals'],
                               phase_perp_rad=ph_perp, phase_z_rad=ph_z, R_src_max_kpc=R_src / KPC_M, z_src_kpc=z_src / KPC_M,
                               sphere_entries=0 if sph is None else int(len(sph['kz']))),
               memory_estimate_bytes=int(mem), rank=int(P.shape[1]), n_eval_radii=int(len(radii)),
               stars_certificates=list(getattr(getattr(roster, 'stars', None), 'certificates', []) or []),
               provider_custody={k: v for k, v in jn_provider.custody().items() if k != 'counts'})
    arrays['ring_tables'] = ring
    st = TailState(empty=False, record=rec, arrays=arrays, jn_provider=jn_provider)
    st.diagnostics['build_seconds'] = time.time() - t_start
    return st


# ============================================================================= boundary callable
class TailBoundary:
    """Picklable replacement of the zero boundary closures: __call__(pos) == state.jet(pos, order)."""

    def __init__(self, state=None, order=2, tap=0):
        if order not in (1, 2):
            raise Refusal('UV_TAIL_JET_ORDER')
        self.state = state; self.order = order; self.tap = int(tap); self.tapped = []

    def set_state(self, state):
        self.state = state

    def _st(self):
        if self.state is None:
            raise Refusal('UV_TAIL_STATE_NOT_SET')
        return self.state

    def __call__(self, pos):
        jet = self._st().jet(pos, self.order)
        if len(self.tapped) < self.tap:
            self.tapped.append((np.array(pos, dtype=float, copy=True), {k: v.copy() for k, v in jet.items()}))
        return jet

    def jet_for_line(self, line, z_m):
        return self._st().jet_for_line(line, z_m, self.order)

    def lapse_pair(self, x_m, y_m, z_m, ns=1):
        return self._st().lapse_pair(x_m, y_m, z_m, ns)


# ============================================================================= bounds and monitors
def _eps_per_shell(state, eps_certificate):
    edges = state._a['shell_edges_inverse_kpc']
    shells = eps_certificate['shells']
    eps = np.full(len(edges) - 1, np.nan)
    for i, (lo, hi) in enumerate(zip(edges[:-1], edges[1:])):
        vals = [float(s['eps']) for s in shells if float(s['lo_inverse_kpc']) < hi and float(s['hi_inverse_kpc']) > lo]
        cov = [(float(s['lo_inverse_kpc']), float(s['hi_inverse_kpc'])) for s in shells]
        if state._a['shell_integrals'][i].any():
            covered = any(a <= lo + 1e-12 for a, b in cov) and any(b >= min(hi, edges[-1]) - 1e-12 for a, b in cov)
            if not vals or not covered:
                raise Refusal('UV_TAIL_EPS_COVERAGE', 'shell [%g,%g)' % (lo, hi))
            eps[i] = max(vals)
        else:
            eps[i] = max(vals) if vals else 0.0
    return eps


def field_bound(state, eps_certificate):
    """|d^a r(x)| <= sum_s eps_s B_s^(a) (V001 sec 1.4), B_s^(a) = pref int_{D cap shell s} kp |k|^(a-2) |S_T| c0^D (x2
    for k_z < 0). Shells: unit shells from min(K) (node-assigned; a bound estimate). eps_certificate = {'shells':
    [{'lo_inverse_kpc','hi_inverse_kpc','eps'}]}. Returns per-shell B (SI: 1, 1/m, 1/m^2) and the sums."""
    if state.empty:
        return dict(empty=True, total=[0.0, 0.0, 0.0])
    eps = _eps_per_shell(state, eps_certificate)
    B = state._a['shell_integrals']
    tot = (eps[:, None] * B).sum(axis=0)
    return dict(empty=False, shell_edges_inverse_kpc=state._a['shell_edges_inverse_kpc'].tolist(), eps=eps.tolist(),
                B=B.tolist(), total=tot.tolist(), scope='node-assigned unit shells; eps an estimate (EPS), not a proven sup')


def srb_rot(state, eps_certificate, rows):
    """SRB-ROT (sec 1.5; V001 sec 1.4 static rotation channel; necessary, not sufficient):
    |dv_c(R)| <= R c^2 sum_s eps_s B_s^(1) / (2 N_min v_c(R)); row bound = max over the row's columns.
    rows = {'column_R_m', 'v_c_m_s' (per column), 'row_columns' (list of index lists), 'N_min', 'tau_km_s'}."""
    fb = field_bound(state, eps_certificate)
    B1 = fb['total'][1]
    R = np.asarray(rows['column_R_m'], float); v = np.asarray(rows['v_c_m_s'], float)
    col = R * state.record['c_m_s'] ** 2 * B1 / (2 * float(rows['N_min']) * v) / 1e3   # km/s
    tau = np.asarray(rows['tau_km_s'], float)
    rb = np.array([float(np.max(col[np.asarray(ix)])) for ix in rows['row_columns']])
    return dict(bound_km_s=rb.tolist(), ratio_to_tau=(rb / tau).tolist(), pass_tau_over_10=bool(np.all(rb <= tau / 10)),
                scope='static rotation-law channel only (SRB-ROT): necessary, not sufficient')


def monitor_MT(state_new, state_old, probes, v_ref, tau):
    """M_T = max_{i,j} R_i c^2 |d_R (t_new - t_old)(R_i, phi_j, 0)| / (2 v_i tau_i)  (sec 1.7; v_ref, tau in km/s)."""
    R = np.asarray(probes['R_m'], float); ph = np.asarray(probes['phi'], float)
    v = np.asarray(v_ref, float) * 1e3; ta = np.asarray(tau, float) * 1e3
    def dR(st, Ri):
        if st.empty:
            return np.zeros(len(ph))
        return st.cyl_jets(Ri, ph, [0.0], 1)['fR'][:, 0]
    c = (state_new.record if not state_new.empty else state_old.record)['c_m_s']
    vals = np.array([float(np.max(np.abs(dR(state_new, Ri) - dR(state_old, Ri)))) * Ri * c * c / (2 * vi * ti)
                     for Ri, vi, ti in zip(R, v, ta)])
    return float(np.max(vals)) if len(vals) else 0.0


def nodes_v001_packet(waves_ext, dk_ext, S_pkt_ext, gamma_eff, lambda_scale=1.0):
    """nodes_v001 (T2 only): explicit packet over G_ext \\ G_K, amplitude dk/(2pi)^3 T_inf S_pkt on component 0,
    evaluated by the unchanged line v002 (V001 sec 1.3). Returns a prepared-like dict."""
    k = np.asarray(waves_ext, float); dk = np.asarray(dk_ext, float); S = np.asarray(S_pkt_ext, complex)
    k2 = np.sum(k * k, axis=1)
    if np.any(k2 <= 0):
        raise Refusal('UV_TAIL_NODES_ZERO_MODE')
    wr = np.zeros((len(k), 10, 1), complex)
    wr[:, 0, 0] = lambda_scale * dk / (2 * math.pi) ** 3 * S / (4.0 * gamma_eff * k2)
    return {'wavevectors': k, 'weighted_responses': wr}
