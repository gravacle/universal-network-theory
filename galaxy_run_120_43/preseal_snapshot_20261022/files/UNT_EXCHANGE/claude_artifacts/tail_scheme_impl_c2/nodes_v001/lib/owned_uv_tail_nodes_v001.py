"""Owned UV-tail nodes_v001 library (TAIL_SCHEME_DESIGN_V002 sec 1.3 'nodes_v001 (T2 only)', with the V002_R1 record IA8;
root V005 addendum A50 item 11).  INERT: no file reads and no scientific execution at import.  numpy only.

nodes_v001 replaces the continuum tail t by the explicit packet of the EXTENDED grid's extra nodes:

    t(x) = Re sum_{q in G_ext \\ G_K} a_q exp(i k_q.x),   a_q = lambda dk_q/(2 pi)^3 S_pkt(k_q) / (4 gamma_eff |k_q|^2)

  * G_K is the stage's own composite tensor Gauss cube (seed composite_grid_spec, kmax K); G_ext is the composite tensor cube of
    source_rule.ext_grid.  G_K must be a sub-grid of G_ext: the ext panels inside [-K, K] are EXACTLY the kept panels (same breaks,
    same orders), so the kept axis nodes and weights are bitwise the ext ones (checked from the prep arithmetic, ext_context).
    G_ext \\ G_K = the tensor nodes with at least one coordinate in an ext panel outside [-K, K].
  * dk_q = wx*wy*wz of the ext axis weights (prep v008/v009 L136-147 arithmetic, (wx*wy)*wz order); T_inf = 1/(4 gamma |k|^2)
    (lapse only, component 0); the amplitude expression is the module lane's nodes_v001_packet (owned_uv_tail_lapse_v001
    c28d4209 L888-897) term for term (TESTED bitwise in tests/).
  * S_pkt on the extra nodes is the stage packet's OWN transform of the stage's own roster (sec 1.3 table, K5), evaluated on the
    tensor axes: ring J0 transforms (prep analytic stars / initial rings, feedback v002/v004 rings) and Cartesian forward sums
    (physical_source_fourier of the route-A elements, the offset's forward sum of the body base source).  The arithmetic is the
    cited formulas regrouped on the tensor axes (roundoff only); T2-I (<= 1e-12 against stored packets of a run that carried the
    nodes in its own packet) is the deciding test that the regrouped transforms are the stage arithmetic.
  * Evaluation: per transverse point (x, y) the k_z vectors h_l = sum_ij a_ijl e^{i kx_i x} e^{i ky_j y} (and the x/y derivative
    multipliers) are contracted once (LRU cache), then each height is a k_z sum.  This is the line v002 grouping (exact equal k_z),
    so the field equals the direct packet sum up to roundoff.  Real output: the real part of the full signed sum (the extra-node
    set is reflection symmetric; the imaginary residual is recorded by tests, never added).
  * R0 (K11): b0 = Re sum_l h_l, bd = Re sum_l h_l expm1(i kz_l z) -> bd(z = 0) == 0.0 exactly; t(z) - t(0) is never formed.
  * Jets: fields/gradient/Hessian of component 0 in the (n,10,1), (n,10,1,3), (n,10,1,3,3) slots; order 1 -> Hessian exact zeros.
Units SI (m, 1/m).  The kept region must be the cube K (stage kinds route_a/reference/body and every masked kind with a cube
truncation); any other kept shape is refused (UV_TAIL_NODES_V001_REQUIRES_CUBE_KEPT).
"""
import hashlib
import json
import math
import time
from collections import OrderedDict
import numpy as np

STATE_SCHEMA = 'UNT_UV_TAIL_NODES_STATE_C2V001'
CONTEXT_SCHEMA = 'UNT_UV_TAIL_NODES_EXT_CONTEXT_C2V001'
CONFIG_SCHEMA = 'UNT_UV_TAIL_CONFIG_C2V001'          # the module lane's normalized config schema (owned_uv_tail_lapse_v001)
TEST_ONLY_CERT = 'NONE_TEST_ONLY'
KPC_M = 3.085677581491367e19
MAX_EXT_AXIS_NODES = 128
LINE_LRU = 256
GEMM_GROUP_BLOCK = 64
RING_ROW_BLOCK = 2048


class Refusal(ValueError):
    def __init__(self, code, detail=''):
        self.code = code
        super().__init__(code + ((' ' + detail) if detail else ''))


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _sha(text):
    return hashlib.sha256(text.encode() if isinstance(text, str) else text).hexdigest()


def array_digest(a):
    a = np.ascontiguousarray(a)
    h = hashlib.sha256(); h.update(('%s|%s|' % (a.dtype.str, a.shape)).encode()); h.update(a.tobytes())
    return h.hexdigest()


# ============================================================================= grids (prep v008/v009 L125-147 arithmetic)
def axis_from_spec(spec, kpc_m, max_nodes=MAX_EXT_AXIS_NODES):
    """(axis 1/m, weights 1/m, breaks, orders) of a composite spec, with the prep's own arithmetic and validity rules
    (partition of [-kmax, kmax], int orders >= 2, total_axis_nodes, signed reflection symmetry, no zero node)."""
    if not isinstance(spec, dict):
        raise Refusal('UV_TAIL_NODES_GRID_INVALID', 'composite spec must be an object')
    breaks = np.asarray(spec.get('breaks_inverse_kpc'), dtype=float)
    orders = spec.get('panel_orders')
    if breaks.ndim != 1 or not isinstance(orders, list) or len(breaks) != len(orders) + 1 or not np.isfinite(breaks).all() \
            or np.any(np.diff(breaks) <= 0) or breaks[0] != -breaks[-1]:
        raise Refusal('UV_TAIL_NODES_GRID_INVALID', 'panels must partition exactly [-kmax, kmax]')
    nk = spec.get('total_axis_nodes')
    if any(type(n) is not int or n < 2 for n in orders) or type(nk) is not int or sum(orders) != nk or nk > max_nodes:
        raise Refusal('UV_TAIL_NODES_GRID_INVALID', 'node budget/order mismatch (or more than %d nodes/axis)' % max_nodes)
    if not np.array_equal(breaks, -breaks[::-1]) or orders != orders[::-1]:
        raise Refusal('UV_TAIL_NODES_GRID_INVALID', 'panels/orders must retain signed reflection symmetry')
    axis_parts = []; weight_parts = []
    for lo, hi, n in zip(breaks[:-1], breaks[1:], orders):
        gxk, gwk = np.polynomial.legendre.leggauss(n)
        axis_parts.append(((lo + hi) / 2 + (hi - lo) * gxk / 2) / kpc_m)
        weight_parts.append((hi - lo) * gwk / (2 * kpc_m))
    axis = np.concatenate(axis_parts); w = np.concatenate(weight_parts)
    if np.any(axis == 0) or not np.all(np.isfinite(axis)) or not np.all(w > 0):
        raise Refusal('UV_TAIL_NODES_GRID_INVALID', 'zero mode or nonfinite/nonpositive weight')
    return axis, w, breaks, list(orders)


def tensor_waves(axis):
    """prep L134 order: x outer, y, z inner."""
    n = len(axis)
    return np.stack([np.repeat(axis, n * n), np.tile(np.repeat(axis, n), n), np.tile(axis, n * n)], axis=1)


def tensor_weights(w):
    """prep L135-136: wx*wy*wz evaluated as (wx*wy)*wz, x outer."""
    return ((w[:, None, None] * w[None, :, None]) * w[None, None, :]).reshape(-1)


def ext_context(*, ext_spec, kept_spec, kpc_m, waves=None, dk_weights=None):
    """The nodes_v001 extended-grid context.  Refuses unless G_K is a sub-grid of G_ext with bitwise-identical kept nodes and
    weights; if the stage's own waves / dk weights are supplied they must equal the kept tensor bitwise."""
    if kept_spec is None:
        raise Refusal('UV_TAIL_NODES_GRID_INVALID', 'nodes_v001 requires a declared composite kept grid (seed composite_grid_spec)')
    ax_k, w_k, br_k, or_k = axis_from_spec(kept_spec, kpc_m)
    ax_e, w_e, br_e, or_e = axis_from_spec(ext_spec, kpc_m)
    K = float(br_k[-1]); Ke = float(br_e[-1])
    if not Ke > K:
        raise Refusal('UV_TAIL_NODES_GRID_INVALID', 'ext kmax %g must exceed the kept kmax %g' % (Ke, K))
    inside = [i for i, (lo, hi) in enumerate(zip(br_e[:-1], br_e[1:])) if lo >= -K and hi <= K]
    if not inside or any(not (lo >= -K and hi <= K) and not (hi <= -K or lo >= K) for lo, hi in zip(br_e[:-1], br_e[1:])):
        raise Refusal('UV_TAIL_NODES_GRID_INVALID', 'an ext panel straddles the kept edge +-K')
    sub_breaks = np.concatenate([[br_e[inside[0]]], br_e[[i + 1 for i in inside]]])
    if not np.array_equal(sub_breaks, br_k) or [or_e[i] for i in inside] != or_k:
        raise Refusal('UV_TAIL_NODES_GRID_INVALID', 'ext panels inside [-K, K] are not exactly the kept panels')
    inner = np.zeros(len(ax_e), bool); pos = 0
    for i, n in enumerate(or_e):
        if i in inside:
            inner[pos:pos + n] = True
        pos += n
    if not np.array_equal(ax_e[inner], ax_k) or not np.array_equal(w_e[inner], w_k):
        raise Refusal('UV_TAIL_NODES_GRID_INVALID', 'kept axis nodes/weights are not bitwise the ext ones')
    checks = {}
    if waves is not None:
        wv = np.asarray(waves, float)
        checks['stage_waves_equal_kept_tensor'] = bool(wv.shape == (len(ax_k) ** 3, 3) and np.array_equal(wv, tensor_waves(ax_k)))
        if not checks['stage_waves_equal_kept_tensor']:
            raise Refusal('UV_TAIL_NODES_GRID_INVALID', 'stage waves are not the kept tensor grid (bitwise)')
    if dk_weights is not None:
        checks['stage_dk_equal_kept_tensor'] = bool(np.array_equal(np.asarray(dk_weights, float), tensor_weights(w_k)))
        if not checks['stage_dk_equal_kept_tensor']:
            raise Refusal('UV_TAIL_NODES_GRID_INVALID', 'stage dk weights are not the kept tensor weights (bitwise)')
    N = len(ax_e)
    mask3 = ~(inner[:, None, None] & inner[None, :, None] & inner[None, None, :])
    rec = dict(schema=CONTEXT_SCHEMA, ext_spec=json.loads(_canon(ext_spec)), ext_spec_sha256=_sha(_canon(ext_spec)),
               kept_spec_sha256=_sha(_canon(kept_spec)), K_inverse_kpc=K, K_ext_inverse_kpc=Ke, N_ext_axis=int(N),
               N_kept_axis=int(len(ax_k)), n_ext_nodes=int(mask3.sum()), n_kept_nodes=int(len(ax_k) ** 3),
               axis_digest=array_digest(ax_e), weights_digest=array_digest(w_e), checks=checks)
    return dict(record=rec, axis=ax_e, weights=w_e, inner=inner, mask3=mask3, K_m=K / kpc_m)


def ext_waves_and_dk(axis, weights, inner):
    """Flat ext-node waves (n_ext,3) and dk (n_ext,) in the prep's x-outer order (the masked subset of the full tensor)."""
    N = len(axis)
    mask = (~(inner[:, None, None] & inner[None, :, None] & inner[None, None, :])).reshape(-1)
    full_dk = tensor_weights(weights)
    i, j, l = np.unravel_index(np.flatnonzero(mask), (N, N, N))
    return np.stack([axis[i], axis[j], axis[l]], axis=1), full_dk[mask], mask


# ============================================================================= stage transforms on the tensor axes
def ring_transform_tensor(axis, R_m, z_m, m_kg, c_m_s, j0):
    """S(kx,ky,kz) = -c^2 sum_r m_r J0(k_perp R_r) exp(-i kz z_r) on the full tensor (N,N,N) (the axisymmetric analytic
    formula of axisymmetric_initial_rest_energy_fourier_v001 L42 / uv_tail_source_roster ring_transform, regrouped)."""
    ax = np.asarray(axis, float); N = len(ax)
    R = np.asarray(R_m, float); z = np.asarray(z_m, float); m = np.asarray(m_kg, float)
    if not (R.shape == z.shape == m.shape) or R.ndim != 1 or not (np.all(np.isfinite(R)) and np.all(np.isfinite(z)) and np.all(np.isfinite(m))):
        raise Refusal('UV_TAIL_NODES_SOURCE_SHAPE', 'ring roster')
    kp = np.hypot(ax[:, None], ax[None, :]).reshape(-1)          # (N^2,) x outer
    Z = np.exp(-1j * np.outer(ax, z))                             # (N, Nr)
    out = np.empty((N * N, N), complex)
    for a in range(0, N * N, RING_ROW_BLOCK):
        b = min(a + RING_ROW_BLOCK, N * N)
        J = j0(kp[a:b, None] * R[None, :])                        # (blk, Nr)
        out[a:b] = (J * m[None, :]) @ Z.T
    return (-c_m_s * c_m_s) * out.reshape(N, N, N)


def point_transform_tensor(axis, positions_m, J):
    """S(k) = sum_e J_e exp(-i k.x_e) on the full tensor (N,N,N) (physical_source_fourier / offset Cartesian forward-sum formula,
    roster point_transform), regrouped: elements sharing an exact (x, y) form one column, exp(-i(kx x + ky y)) exp(-i kz z)."""
    ax = np.asarray(axis, float); N = len(ax)
    pos = np.asarray(positions_m, float).reshape(-1, 3); Jv = np.asarray(J)
    if Jv.ndim == 3:
        Jv = Jv[:, 0, 0]
    if np.iscomplexobj(Jv):
        if np.any(np.imag(Jv) != 0):
            raise Refusal('UV_TAIL_SOURCE_NONREAL')
        Jv = np.real(Jv)
    Jv = np.asarray(Jv, float).reshape(-1)
    if len(Jv) != len(pos) or not np.all(np.isfinite(pos)) or not np.all(np.isfinite(Jv)):
        raise Refusal('UV_TAIL_NODES_SOURCE_SHAPE', 'point roster')
    xy, inv = np.unique(pos[:, :2], axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    G = len(xy)
    Q = np.zeros((G, N), complex)                                  # per column: sum_z J exp(-i kz z)
    order = np.argsort(inv, kind='stable')
    bounds = np.searchsorted(inv[order], np.arange(G + 1))
    for g in range(G):
        e = order[bounds[g]:bounds[g + 1]]
        Q[g] = np.exp(-1j * np.outer(ax, pos[e, 2])) @ Jv[e]
    out = np.zeros((N * N, N), complex)
    for a in range(0, G, GEMM_GROUP_BLOCK):
        b = min(a + GEMM_GROUP_BLOCK, G)
        ph = ax[:, None, None] * xy[None, None, a:b, 0] + ax[None, :, None] * xy[None, None, a:b, 1]   # (N,N,blk)
        P = np.exp(-1j * ph).reshape(N * N, b - a)
        out += P @ Q[a:b]
    return out.reshape(N, N, N)


def extract_ext(tensor, mask3):
    return np.ascontiguousarray(np.asarray(tensor)[mask3])


def amplitudes(waves_ext, dk_ext, S_ext, gamma_eff, lambda_scale):
    """The module lane's nodes_v001_packet amplitude, term for term (c28d4209 L891-896)."""
    k = np.asarray(waves_ext, float); dk = np.asarray(dk_ext, float); S = np.asarray(S_ext, complex)
    k2 = np.sum(k * k, axis=1)
    if np.any(k2 <= 0):
        raise Refusal('UV_TAIL_NODES_ZERO_MODE')
    return lambda_scale * dk / (2 * math.pi) ** 3 * S / (4.0 * gamma_eff * k2)


# ============================================================================= state
class NodesTailState:
    """Built nodes_v001 tail of one field state.  Duck-type of owned_uv_tail_lapse_v001.TailState for every consumer slot
    (TailBoundary, controller, route-B binding, parallel worker): empty, record, digest, _digest(), diagnostics, jet,
    jet_for_line, lapse_pair, value, gradient, cyl_jets (order 1), to_arrays, from_arrays.  Picklable (caches dropped)."""

    def __init__(self, *, empty, record, arrays=None, jn_provider=None):
        self.empty = bool(empty); self.record = record; self._a = arrays or {}
        self._lines = OrderedDict(); self._T = None
        self.diagnostics = {'line_builds': 0, 'line_hits': 0, 'points': 0}
        self.digest = self._digest()

    def _digest(self):
        h = hashlib.sha256(); h.update(_canon(self.record).encode())
        for k in sorted(self._a):
            a = np.ascontiguousarray(self._a[k])
            h.update(('|%s|%s|%s|' % (k, a.dtype, a.shape)).encode()); h.update(a.tobytes())
        return h.hexdigest()

    def __getstate__(self):
        d = dict(self.__dict__); d['_lines'] = OrderedDict(); d['_T'] = None
        return d

    def to_arrays(self):
        return {k: np.array(v, copy=True) for k, v in self._a.items()}

    @classmethod
    def from_arrays(cls, arrays, record, jn_provider=None, expected_digest=None):
        st = cls(empty=record.get('empty', False), record=record, arrays={k: np.asarray(v) for k, v in arrays.items()})
        if expected_digest is not None and st.digest != expected_digest:
            raise Refusal('UV_TAIL_STATE_DIGEST_MISMATCH')
        return st

    # -- derived (never part of the digest; deterministic functions of record + arrays)
    def S_total(self):
        """sum over parts in record order of sign * S_part (0 + S_first; a negative part is subtracted)."""
        S = np.zeros(int(self.record['ext_context']['n_ext_nodes']), complex)
        for p in self.record['parts']:
            v = self._a['S_' + p['name']]
            S = S + v if p['sign'] > 0 else S - v
        return S

    def _tensor(self):
        if self._T is None:
            ax = self._a['axis_m']; w = self._a['weights_m']; inner = self._a['inner'].astype(bool)
            k, dk, mask = ext_waves_and_dk(ax, w, inner)
            amp = amplitudes(k, dk, self.S_total(), self.record['gamma_eff'], self.record['lambda_scale'])
            N = len(ax); T = np.zeros(N * N * N, complex); T[mask] = amp
            self._T = T.reshape(N, N, N)
        return self._T

    def _check_point(self, R, z):
        dm = self.record['domain_m']
        if not (math.isfinite(R) and math.isfinite(z)) or R > dm['R_eval_max_m'] or abs(z) > dm['z_eval_max_m']:
            raise ValueError('UV_TAIL_UNRESOLVED_POINT R=%r z=%r' % (R, z))

    def _line(self, x, y):
        key = (float(x), float(y))
        if key in self._lines:
            v = self._lines.pop(key); self._lines[key] = v; self.diagnostics['line_hits'] += 1
            return v
        ax = self._a['axis_m']; T = self._tensor()
        Ex = np.exp(1j * ax * key[0]); Ey = np.exp(1j * ax * key[1])
        B0 = np.tensordot(Ex, T, axes=(0, 0)); B1 = np.tensordot((1j * ax) * Ex, T, axes=(0, 0))
        B2 = np.tensordot((-(ax * ax)) * Ex, T, axes=(0, 0))
        Eyd = (1j * ax) * Ey; Eydd = (-(ax * ax)) * Ey
        v = dict(h=Ey @ B0, hx=Ey @ B1, hy=Eyd @ B0, hxx=Ey @ B2, hxy=Eyd @ B1, hyy=Eydd @ B0)
        self._lines[key] = v; self.diagnostics['line_builds'] += 1
        if len(self._lines) > LINE_LRU:
            self._lines.popitem(last=False)
        return v

    def _point(self, x, y, z, order):
        L = self._line(x, y); kz = self._a['axis_m']
        P = np.exp(1j * kz * float(z)); Pz = (1j * kz) * P
        f = float(np.dot(L['h'], P).real)
        g = np.array([float(np.dot(L['hx'], P).real), float(np.dot(L['hy'], P).real), float(np.dot(L['h'], Pz).real)])
        H = np.zeros((3, 3))
        if order == 2:
            Pzz = (-(kz * kz)) * P
            hxx = float(np.dot(L['hxx'], P).real); hxy = float(np.dot(L['hxy'], P).real); hyy = float(np.dot(L['hyy'], P).real)
            hxz = float(np.dot(L['hx'], Pz).real); hyz = float(np.dot(L['hy'], Pz).real); hzz = float(np.dot(L['h'], Pzz).real)
            H = np.array([[hxx, hxy, hxz], [hxy, hyy, hyz], [hxz, hyz, hzz]])
        self.diagnostics['points'] += 1
        return f, g, H

    # -- public evaluation API (TailState signatures)
    def jet(self, pos, order):
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
            x, y, z = float(pos[i, 0]), float(pos[i, 1]), float(pos[i, 2])
            self._check_point(math.hypot(x, y), z)
            f, g, H = self._point(x, y, z, order)
            fields[i, 0, 0] = f; grad[i, 0, 0, :] = g
            if order == 2:
                hess[i, 0, 0] = H
        return dict(boundary_fields=fields, boundary_gradient=grad, boundary_hessian=hess)

    def jet_for_line(self, line, z_m, order):
        return self.jet(np.array([[float(line['x_m']), float(line['y_m']), float(z_m)]]), order)

    def lapse_pair(self, x_m, y_m, z_m, ns=1):
        if ns != 1:
            raise Refusal('UV_TAIL_SINGLE_SOURCE_FAMILY_REQUIRED', 'ns=%r' % ns)
        if self.empty:
            return np.zeros(ns), np.zeros(ns)
        R = math.hypot(x_m, y_m)
        self._check_point(R, 0.0); self._check_point(R, z_m)
        h = self._line(x_m, y_m)['h']
        em = np.expm1(1j * self._a['axis_m'] * float(z_m))
        b0 = float(np.sum(h.real)); bd = float(h.real @ em.real - h.imag @ em.imag)
        return np.array([b0]), np.array([bd + 0.0])

    def value(self, pos):
        return self.jet(pos, 1)['boundary_fields'][:, 0, 0]

    def gradient(self, pos):
        return self.jet(pos, 1)['boundary_gradient'][:, 0, 0, :]

    def cyl_jets(self, R, phis, zs, order=1, _cache=False):
        """Order 1 only (the route-A monitor): f, fR, fp, fz at (R, phis[i], zs[j]) as (nphi, nz) arrays."""
        if order != 1:
            raise Refusal('UV_TAIL_NODES_CYL_JETS_ORDER_1_ONLY')
        phis = np.atleast_1d(np.asarray(phis, float)); zs = np.atleast_1d(np.asarray(zs, float))
        out = {k: np.zeros((len(phis), len(zs))) for k in ('f', 'fR', 'fp', 'fz')}
        if self.empty:
            return out
        for i, ph in enumerate(phis):
            c, s = math.cos(ph), math.sin(ph); x, y = R * c, R * s
            for j, z in enumerate(zs):
                self._check_point(R, z)
                f, g, _ = self._point(x, y, z, 1)
                out['f'][i, j] = f; out['fR'][i, j] = c * g[0] + s * g[1]; out['fp'][i, j] = -y * g[0] + x * g[1]; out['fz'][i, j] = g[2]
        return out


# ============================================================================= build
def build_state(*, config, kept, ctx, parts, gamma_eff, c_m_s, i1t, stage_kind, source_record=None):
    """The NodesTailState of one stage state.  parts = [(name, sign +1/-1, S_ext (n_ext,) complex, transform record)].
    Checks mirror owned_uv_tail_lapse_v001.build: normalized config + sha, enabled, the nodes_v001 rule with THIS ext grid,
    certificates from bytes (production_admissible), I1-T verdict, positive physics; kept must be the cube of ctx's K."""
    t0 = time.time()
    if not isinstance(config, dict) or config.get('schema') != CONFIG_SCHEMA:
        raise Refusal('UV_TAIL_CONFIG_NOT_NORMALIZED')
    if config['sha256'] != _sha(_canon({k: v for k, v in config.items() if k != 'sha256'})):
        raise Refusal('UV_TAIL_CONFIG_DIGEST_MISMATCH')
    if not config['enabled']:
        raise Refusal('UV_TAIL_DISABLED')
    sr = config['source_rule']
    if not (isinstance(sr, dict) and sr.get('rule') == 'nodes_v001'):
        raise Refusal('UV_TAIL_NODES_V001_RULE_REQUIRED', repr(sr))
    if _sha(_canon(sr['ext_grid'])) != ctx['record']['ext_spec_sha256']:
        raise Refusal('UV_TAIL_NODES_V001_EXT_GRID_MISMATCH')
    if not (isinstance(kept, dict) and kept.get('shape') == 'cube' and abs(kept['K_inverse_kpc'] - ctx['record']['K_inverse_kpc'])
            <= 1e-12 * ctx['record']['K_inverse_kpc']):
        raise Refusal('UV_TAIL_NODES_V001_REQUIRES_CUBE_KEPT', repr(kept))
    if not math.isfinite(gamma_eff) or gamma_eff <= 0 or not math.isfinite(c_m_s) or c_m_s <= 0:
        raise Refusal('UV_TAIL_PHYSICAL_INVALID')
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
        production_admissible = False
    dm = config['domain']
    domain_m = {'R_eval_max_m': dm['R_eval_max_kpc'] * KPC_M, 'z_eval_max_m': dm['z_eval_max_kpc'] * KPC_M,
                'z_src_max_m': dm['z_src_max_kpc'] * KPC_M}
    n_ext = ctx['record']['n_ext_nodes']
    arrays = dict(axis_m=np.array(ctx['axis'], dtype=float), weights_m=np.array(ctx['weights'], dtype=float),
                  inner=ctx['inner'].astype(np.int8))
    prec = []
    for name, sign, S, trec in parts:
        S = np.ascontiguousarray(np.asarray(S, dtype=complex))
        if S.shape != (n_ext,) or not np.all(np.isfinite(S)) or sign not in (1, -1) or not name.isidentifier():
            raise Refusal('UV_TAIL_NODES_SOURCE_SHAPE', 'part %r' % (name,))
        arrays['S_' + name] = S
        prec.append(dict(name=name, sign=int(sign), transform=trec, S_digest=array_digest(S)))
    rec = dict(schema=STATE_SCHEMA, source_rule='nodes_v001', config_sha256=config['sha256'], kept=kept, outer_not_used=config['outer'],
               stage_kind=stage_kind, lambda_scale=config['lambda_scale'], gamma_eff=float(gamma_eff), c_m_s=float(c_m_s),
               domain_m=domain_m, eps_certificate=certs['eps_certificate'], lo_certificate=certs['lo_certificate'], i1t=i1t,
               production_admissible=production_admissible, jet_order=config['jet_order'], ext_context=ctx['record'],
               parts=prec, empty=n_ext == 0, roster_digest=_sha(_canon(prec)), source=source_record,
               domain_rule='D = G_ext \\ G_K (the extended grid extra nodes); outer region O is not used by nodes_v001',
               amplitude='lambda dk/(2pi)^3 S/(4 gamma |k|^2) on component 0 (nodes_v001_packet formula)')
    st = NodesTailState(empty=n_ext == 0, record=rec, arrays=arrays)
    st.diagnostics['build_seconds'] = time.time() - t0
    return st


def brute_force_jet(waves_ext, amp, pos):
    """Test oracle: direct sum over the extra nodes (complex), fields, gradient and Hessian of component 0 at points pos."""
    k = np.asarray(waves_ext, float); a = np.asarray(amp, complex); pos = np.asarray(pos, float)
    out = []
    for p in pos:
        e = a * np.exp(1j * (k @ p))
        f = np.sum(e); g = np.array([np.sum(e * 1j * k[:, i]) for i in range(3)])
        H = np.array([[np.sum(-e * k[:, i] * k[:, j]) for j in range(3)] for i in range(3)])
        out.append((f, g, H))
    return out
