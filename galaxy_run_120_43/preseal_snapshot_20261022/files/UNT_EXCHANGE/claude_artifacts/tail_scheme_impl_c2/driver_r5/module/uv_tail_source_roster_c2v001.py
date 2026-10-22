"""UV-tail source roster and the registered smooth tail source S_T (TAIL_SCHEME_DESIGN_V002 sec 1.3, 3.2; V001 sec 1.3).

INERT library: no file reads or scientific execution at import. numpy + the libm Jn provider only.

S_T(k_perp, k_z) = -c^2 [ P_*(k_perp) V(k_z) + sum_i P_i(k_perp) sigma_i(k_z) ]  (rank r = gas columns + 1)
  stars (+ NGC H2, same sech^2 height h): P_*(k) = 2 pi int Sigma(R) J0(kR) R dR of the registered profile
      (galaxy_baryonic_source_forward_v002 radial_surface: linear nodes, constant core, exponential tail);
      GL per linear segment/core with n = max(16, ceil(k_max dr) + 8) nodes; exponential tail R = R_last + a t,
      t in [0,40], uniform t panels (phase k_max a dt <= 1.5), GL12 (rule 't_panels_40a_phase1p5_gl12', R1 IA2);
      doubling-certified (n -> 2n, tail panels -> 2x) to max|dP|/max|P| <= 1e-10 or refused.
      V(k_z) = x / sinh x, x = pi h |k_z| (exact transform of sech^2(z/2h)/(4h)).
  gas (declared rule 'lagrange3_s_gl4'): E_i(k_z) = sum_l m_il exp(-i k_z z_il) over all elements of column i (all
      azimuths: the m=0 projection); sigma_i = E_i / (2 pi w_i), w_i = column int R dR; per annulus the cubic Lagrange
      interpolant in s = R^2 through its four GL4 columns (absent column -> sigma = 0); integrated with M_s GL nodes:
      P_i(k) = sum_q pi w_q J0(k sqrt(s_q)) L_i(s_q).  Nothing outside the represented annuli.
Units SI (m, 1/m, kg, J). Roster.factors(k_perp, k_z, c) -> (P (Nk,r) float64, F (Nz,r) complex128), S = P @ F.T.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import numpy as np

SCHEMA = 'UNT_UV_TAIL_SOURCE_ROSTER_C2V001'
FORWARD_V002 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/galaxy_baryonic_source_forward_v002.py')
FORWARD_V002_SHA = 'e9be043b46790e3493f4e427fb483a98a5665f004dfac287d5758afce0ac96ad'
STARS_DOUBLING_RTOL = 1e-10


def _sha_bytes(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_pinned(path, sha256, name):
    path = Path(path)
    if _sha_bytes(path) != sha256:
        raise ValueError('UV_TAIL_PIN_MISMATCH ' + str(path))
    spec = importlib.util.spec_from_file_location('uvt_' + name, str(path))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    if _sha_bytes(path) != sha256:
        raise ValueError('UV_TAIL_PIN_CHANGED_AFTER_IMPORT ' + str(path))
    return mod


def _digest_arrays(parts):
    h = hashlib.sha256()
    for key in sorted(parts):
        v = parts[key]
        if isinstance(v, np.ndarray):
            a = np.ascontiguousarray(v)
            h.update(key.encode() + b'|' + str(a.dtype).encode() + b'|' + str(a.shape).encode() + b'|')
            h.update(a.tobytes())
        else:
            h.update(key.encode() + b'|' + json.dumps(v, sort_keys=True, default=str).encode())
    return h.hexdigest()


def vertical_sech2(k_z, height_m):
    """x/sinh x, x = pi h |k_z|, evaluated as 2x e^-x / (1 - e^-2x) (exact form, no overflow); V(0) = 1."""
    x = math.pi * height_m * np.abs(np.asarray(k_z, dtype=float))
    out = np.ones_like(x)
    nz = x > 0
    xn = x[nz]
    out[nz] = 2.0 * xn * np.exp(-xn) / (-np.expm1(-2.0 * xn))
    return out


# ----------------------------------------------------------------------------- stars (registered profile)
class StarsProfile:
    """Registered stellar (+ H2) surface profile(s) sharing one sech^2 height."""

    def __init__(self, *, components, height_kpc, kpc_m, solar_mass_kg, segment_rule, tail_rule, radial_surface):
        if segment_rule != 'max16_ceil_kdr_plus8':
            raise ValueError('UV_TAIL_CONFIG_INVALID stars.segment_rule')
        if tail_rule != 't_panels_40a_phase1p5_gl12':
            raise ValueError('UV_TAIL_CONFIG_INVALID stars.tail_rule')
        self.components = [dict(name=str(c['name']), radii_kpc=[float(x) for x in c['radius_kpc']],
                                sigma_Msun_pc2=[float(x) for x in c['surface_density_Msun_pc2']],
                                outer_scale_kpc=float(c['outer_scale_kpc'])) for c in components]
        self.height_kpc = float(height_kpc); self.kpc_m = float(kpc_m); self.solar_mass_kg = float(solar_mass_kg)
        self.segment_rule = segment_rule; self.tail_rule = tail_rule
        self._rs = radial_surface
        self.sigma_unit = self.solar_mass_kg / (self.kpc_m / 1000.0) ** 2
        self.certificates = []

    @property
    def height_m(self):
        return self.height_kpc * self.kpc_m

    def R_src_max_m(self):
        return max((c['radii_kpc'][-1] + 12.0 * c['outer_scale_kpc']) for c in self.components) * self.kpc_m

    def z_src_m(self):
        return 24.0 * self.height_m

    def _nodes(self, comp, kmax_kpc, mult):
        radii = comp['radii_kpc']; rd = comp['outer_scale_kpc']
        cuts = sorted(set([0.0] + radii))
        rr = []; ww = []
        for lo, hi in zip(cuts, cuts[1:]):
            n = mult * max(16, int(math.ceil(kmax_kpc * (hi - lo))) + 8)
            x, w = np.polynomial.legendre.leggauss(n)
            rr.append((lo + hi) / 2 + (hi - lo) * x / 2); ww.append((hi - lo) * w / 2)
        r = np.concatenate(rr); w = np.concatenate(ww)
        sig = np.array([self._rs(float(v), radii, comp['sigma_Msun_pc2'], outer_scale=rd) for v in r]) * self.sigma_unit
        # 2 pi Sigma R dR (kg) on the segments
        mass_seg = 2 * math.pi * sig * (r * self.kpc_m) * (w * self.kpc_m)
        # exponential tail R = R_last + a t, t in [0, 40] (omitted weight e^-40): Sigma R dR = Sigma_last e^-t R a dt,
        # uniform t panels with phase k_max a dt <= 1.5 rad, GL order 12 per panel (IA2: the V002 u-map with 256
        # nodes fails this module's 1e-10 doubling certificate; see the R1 revision record)
        n_pan = mult * max(4, int(math.ceil(40.0 * kmax_kpc * rd / 1.5)))
        x, w = np.polynomial.legendre.leggauss(12)
        edges = np.linspace(0.0, 40.0, n_pan + 1)
        tt = np.concatenate([(lo + hi) / 2 + (hi - lo) * x / 2 for lo, hi in zip(edges[:-1], edges[1:])])
        wt = np.concatenate([(hi - lo) * w / 2 for lo, hi in zip(edges[:-1], edges[1:])])
        rt = radii[-1] + rd * tt
        mass_tail = 2 * math.pi * (comp['sigma_Msun_pc2'][-1] * self.sigma_unit) * np.exp(-tt) * (rt * self.kpc_m) * (rd * self.kpc_m) * wt
        return np.concatenate([r, rt]) * self.kpc_m, np.concatenate([mass_seg, mass_tail])

    def radial_transform(self, k_perp_m, j0):
        """P_*(k_perp) [kg] with the doubling certificate (sec 1.3; STARS_DOUBLING_RTOL); cached per exact k array."""
        k = np.asarray(k_perp_m, dtype=float)
        ck = hashlib.sha256(np.ascontiguousarray(k).tobytes()).hexdigest()
        cache = self.__dict__.setdefault('_cache', {})
        if ck in cache:
            return cache[ck].copy()
        kmax_kpc = float(np.max(k)) * self.kpc_m if k.size else 0.0
        out = np.zeros(k.shape); out2 = np.zeros(k.shape)
        for comp in self.components:
            for mult, acc in ((1, out), (2, out2)):
                R, M = self._nodes(comp, kmax_kpc, mult)
                for a in range(0, len(k), 256):
                    b = min(a + 256, len(k))
                    acc[a:b] += j0(k[a:b, None] * R[None, :]) @ M
        scale = float(np.max(np.abs(out))) if out.size else 0.0
        rel = float(np.max(np.abs(out - out2)) / scale) if scale > 0 else 0.0
        cert = dict(kind='stars_radial_doubling', k_max_inverse_kpc=kmax_kpc, n_k=int(k.size), max_rel_change=rel,
                    rtol=STARS_DOUBLING_RTOL, verdict='PASS' if rel <= STARS_DOUBLING_RTOL else 'FAIL')
        self.certificates.append(cert)
        if rel > STARS_DOUBLING_RTOL:
            raise ValueError('UV_TAIL_STARS_TRANSFORM_UNCERTIFIED max_rel_change=%.3e' % rel)
        cache[ck] = out.copy()
        return out

    def record(self):
        return dict(components=self.components, height_kpc=self.height_kpc, kpc_m=self.kpc_m,
                    solar_mass_kg=self.solar_mass_kg, segment_rule=self.segment_rule, tail_rule=self.tail_rule)


def stars_registered(profile_record, galaxy, components=('stellar_reference',), *, units, extra_components=(),
                     segment_rule='max16_ceil_kdr_plus8', tail_rule='t_panels_40a_phase1p5_gl12', radial_surface=None):
    """f5becd45 profile -> StarsProfile. extra_components: e.g. NGC H2 {name, radius_kpc, surface_density_Msun_pc2,
    outer_scale_kpc} (prep v001 L212-241 radial form, without the GL4 tail-mass normalization)."""
    g = profile_record['galaxies'][galaxy]
    comps = []
    for name in components:
        s = g[name]
        comps.append(dict(name=name, radius_kpc=s['radius_kpc'], surface_density_Msun_pc2=s['surface_density_Msun_pc2'],
                          outer_scale_kpc=s['outer_scale_kpc']))
    height = float(g['stellar_reference']['height_kpc'])
    comps.extend(extra_components)
    if radial_surface is None:
        radial_surface = load_pinned(FORWARD_V002, FORWARD_V002_SHA, 'forward_v002').radial_surface
    return StarsProfile(components=comps, height_kpc=height, kpc_m=units['kpc_m'], solar_mass_kg=units['solar_mass_kg'],
                        segment_rule=segment_rule, tail_rule=tail_rule, radial_surface=radial_surface)


# ----------------------------------------------------------------------------- gas columns (declared rule)
class GasColumns:
    def __init__(self, *, s_edges_kpc2, kpc_m, M_s, column_R_m, column_rdr_m2, present, elements_z, elements_m):
        self.s_edges_kpc2 = np.asarray(s_edges_kpc2, dtype=float); self.kpc_m = float(kpc_m); self.M_s = int(M_s)
        self.column_R_m = np.asarray(column_R_m, dtype=float)        # (n_annuli*4,)
        self.column_rdr_m2 = np.asarray(column_rdr_m2, dtype=float)  # (n_annuli*4,)
        self.present = np.asarray(present, dtype=bool)
        self.elements_z = [np.asarray(z, dtype=float) for z in elements_z]   # per column (all azimuths)
        self.elements_m = [np.asarray(m, dtype=float) for m in elements_m]
        if self.M_s < 4:
            raise ValueError('UV_TAIL_CONFIG_INVALID gas.M_s')

    def support_R_m(self):
        return math.sqrt(float(self.s_edges_kpc2[-1])) * self.kpc_m

    def z_abs_max_m(self):
        zs = [float(np.max(np.abs(z))) for z, p in zip(self.elements_z, self.present) if p and len(z)]
        return max(zs) if zs else 0.0

    def radial_factors(self, k_perp_m, j0):
        """P_i(k) for the PRESENT columns, (Nk, n_present) [m^2]."""
        x4, w4 = np.polynomial.legendre.leggauss(4)
        xm, wm = np.polynomial.legendre.leggauss(self.M_s)
        k = np.asarray(k_perp_m, dtype=float)
        cols = []
        for a, (lo, hi) in enumerate(zip(self.s_edges_kpc2[:-1], self.s_edges_kpc2[1:])):
            si = (lo + hi) / 2 + (hi - lo) * x4 / 2                       # kpc^2
            sq = (lo + hi) / 2 + (hi - lo) * xm / 2; wq = (hi - lo) * wm / 2
            L = np.ones((self.M_s, 4))
            for i in range(4):
                for j in range(4):
                    if j != i:
                        L[:, i] *= (sq - si[j]) / (si[i] - si[j])
            Jq = j0(k[:, None] * (np.sqrt(sq) * self.kpc_m)[None, :])        # (Nk, M_s)
            Pa = Jq @ (math.pi * (wq * self.kpc_m * self.kpc_m)[:, None] * L)  # (Nk, 4)
            for i in range(4):
                if self.present[4 * a + i]:
                    cols.append(Pa[:, i])
        return np.stack(cols, axis=1) if cols else np.zeros((len(k), 0))

    def vertical_factors(self, k_z_m):
        """sigma_i(k_z) for the PRESENT columns, (Nz, n_present) complex [kg/m^2]."""
        kz = np.asarray(k_z_m, dtype=float)
        out = []
        for i in range(len(self.present)):
            if not self.present[i]:
                continue
            z = self.elements_z[i]; m = self.elements_m[i]
            E = np.exp(-1j * np.outer(kz, z)) @ m
            out.append(E / (2 * math.pi * self.column_rdr_m2[i]))
        return np.stack(out, axis=1) if out else np.zeros((len(kz), 0), complex)

    def record(self):
        return dict(s_edges_kpc2=self.s_edges_kpc2.tolist(), M_s=self.M_s, n_columns=int(len(self.present)),
                    n_present=int(self.present.sum()), interp='lagrange3_s_gl4')

    def arrays(self):
        d = dict(gas_column_R_m=self.column_R_m, gas_column_rdr_m2=self.column_rdr_m2, gas_present=self.present.astype(np.int8))
        for i, (z, m) in enumerate(zip(self.elements_z, self.elements_m)):
            d['gas_z_%03d' % i] = z; d['gas_m_%03d' % i] = m
        return d


def annulus_columns(s_edges_kpc2, kpc_m):
    """The GL4-in-s column radii and R dR weights (prep v007 L156-164 arithmetic) for every annulus node."""
    x4, w4 = np.polynomial.legendre.leggauss(4)
    R = []; rdr = []
    for lo, hi in zip(s_edges_kpc2[:-1], s_edges_kpc2[1:]):
        for x, w in zip(x4, w4):
            s = (lo + hi) / 2 + (hi - lo) * float(x) / 2
            Rm = math.sqrt(s) * kpc_m
            dR = (hi - lo) * float(w) * kpc_m * kpc_m / (4 * Rm)
            R.append(Rm); rdr.append(Rm * dR)
    return np.array(R), np.array(rdr)


def gas_columns(positions_m, integrated_J, *, radial_nodes_m, rdr_weights_m2, s_edges_kpc2, M_s, kpc_m, c_m_s,
                radius_rtol=1e-12):
    """Elements (positions (n,3), J (n,) or (n,10,1) component 0) -> GasColumns. Masses m = -J/c^2 (nothing re-derived).
    radial_nodes_m / rdr_weights_m2: the stage's present columns; must coincide with the GL4 annulus nodes."""
    pos = np.asarray(positions_m, dtype=float); J = np.asarray(integrated_J)
    if J.ndim == 3:
        J = J[:, 0, 0]
    J = np.asarray(J)
    if np.iscomplexobj(J):
        if np.any(J.imag != 0):
            raise ValueError('UV_TAIL_SOURCE_NONREAL')
        J = J.real
    J = J.astype(float)
    if pos.ndim != 2 or pos.shape[1] != 3 or len(pos) != len(J) or not np.all(np.isfinite(pos)) or not np.all(np.isfinite(J)):
        raise ValueError('UV_TAIL_SOURCE_SHAPE')
    allR, allrdr = annulus_columns(list(map(float, s_edges_kpc2)), kpc_m)
    nodes = np.asarray(radial_nodes_m, dtype=float); rdr = np.asarray(rdr_weights_m2, dtype=float)
    present = np.zeros(len(allR), bool); col_of_node = np.full(len(nodes), -1)
    for n, Rn in enumerate(nodes):
        j = int(np.argmin(np.abs(allR - Rn)))
        if abs(allR[j] - Rn) > radius_rtol * Rn or abs(allrdr[j] - rdr[n]) > 1e-12 * abs(allrdr[j]):
            raise ValueError('UV_TAIL_COLUMN_NOT_ON_GL4_ANNULUS_NODE R=%r' % Rn)
        present[j] = True; col_of_node[n] = j
    Rel = np.hypot(pos[:, 0], pos[:, 1])
    zs = [[] for _ in allR]; ms = [[] for _ in allR]
    for e in range(len(pos)):
        n = int(np.argmin(np.abs(nodes - Rel[e])))
        if abs(nodes[n] - Rel[e]) > radius_rtol * nodes[n]:
            raise ValueError('UV_TAIL_ELEMENT_OFF_COLUMN R=%r' % Rel[e])
        j = col_of_node[n]
        zs[j].append(pos[e, 2]); ms[j].append(-J[e] / (c_m_s * c_m_s))
    return GasColumns(s_edges_kpc2=s_edges_kpc2, kpc_m=kpc_m, M_s=M_s, column_R_m=allR, column_rdr_m2=allrdr,
                      present=present, elements_z=zs, elements_m=ms)


def gas_columns_from_rings(*, ring_R_m, ring_z_m, ring_m_kg, s_edges_kpc2, M_s, kpc_m, radius_rtol=1e-12):
    """Axisymmetric ring roster (R, z, m) -> GasColumns (the ring masses are already the m=0 projection)."""
    allR, allrdr = annulus_columns(list(map(float, s_edges_kpc2)), kpc_m)
    present = np.zeros(len(allR), bool); zs = [[] for _ in allR]; ms = [[] for _ in allR]
    for R, z, m in zip(np.asarray(ring_R_m, float), np.asarray(ring_z_m, float), np.asarray(ring_m_kg, float)):
        j = int(np.argmin(np.abs(allR - R)))
        if abs(allR[j] - R) > radius_rtol * R:
            raise ValueError('UV_TAIL_RING_OFF_GL4_ANNULUS_NODE R=%r' % R)
        present[j] = True; zs[j].append(z); ms[j].append(m)
    return GasColumns(s_edges_kpc2=s_edges_kpc2, kpc_m=kpc_m, M_s=M_s, column_R_m=allR, column_rdr_m2=allrdr,
                      present=present, elements_z=zs, elements_m=ms)


# ----------------------------------------------------------------------------- roster
class Roster:
    kind = 'registered'

    def __init__(self, *, stars, gas, provenance):
        self.stars = stars; self.gas = gas; self.provenance = dict(provenance)

    def radial_factors(self, k_perp_m, j0):
        cols = []
        if self.stars is not None:
            cols.append(self.stars.radial_transform(k_perp_m, j0)[:, None])
        if self.gas is not None:
            cols.append(self.gas.radial_factors(k_perp_m, j0))
        return np.concatenate(cols, axis=1)

    def vertical_factors(self, k_z_m, c_m_s):
        cols = []
        if self.stars is not None:
            cols.append((-c_m_s * c_m_s * vertical_sech2(k_z_m, self.stars.height_m))[:, None].astype(complex))
        if self.gas is not None:
            cols.append(-c_m_s * c_m_s * self.gas.vertical_factors(k_z_m))
        return np.concatenate(cols, axis=1)

    def factors(self, k_perp_m, k_z_m, c_m_s, j0):
        return self.radial_factors(k_perp_m, j0), self.vertical_factors(k_z_m, c_m_s)

    def extent(self):
        R = []; zt = 0.0; zg = 0.0
        if self.stars is not None:
            R.append(self.stars.R_src_max_m()); zt = self.stars.z_src_m()
        if self.gas is not None:
            R.append(self.gas.support_R_m()); zg = self.gas.z_abs_max_m()
        return dict(R_src_max_m=max(R), stars_24h_m=zt, gas_z_abs_max_m=zg)

    def record(self):
        return dict(kind=self.kind, stars=None if self.stars is None else self.stars.record(),
                    gas=None if self.gas is None else self.gas.record(), provenance=self.provenance)

    def digest(self):
        parts = {'record': self.record()}
        if self.gas is not None:
            parts.update(self.gas.arrays())
        return _digest_arrays(parts)


def roster_rotation(rotation_arrays, stars, *, s_edges_kpc2, kpc_m, M_s, rule='feedback_v004'):
    """Rings of a rotation stage's arrays (the ring set feedback v002/v004 transforms; study gas_rings arithmetic:
    m(R_i, z_il) = sum_phi volume_weights * rho0, requires an m=0 rho0)."""
    if rule not in ('feedback_v002', 'feedback_v004'):
        raise ValueError('UV_TAIL_ROSTER_RULE')
    rho = np.asarray(rotation_arrays['rho0']); vol = np.asarray(rotation_arrays['volume_weights_m3'])
    R = np.asarray(rotation_arrays['radial_nodes_m']); z = np.asarray(rotation_arrays['z'])
    if not np.array_equal(rho, np.broadcast_to(rho[:, :1, :], rho.shape)):
        raise ValueError('UV_TAIL_ROTATION_GAS_NOT_M0')
    if not np.array_equal(z, np.broadcast_to(z[:, :1, :], z.shape)):
        raise ValueError('UV_TAIL_ROTATION_Z_NOT_M0')
    m = np.sum(vol * rho, axis=1)
    gas = gas_columns_from_rings(ring_R_m=np.repeat(R, z.shape[2]), ring_z_m=z[:, 0, :].reshape(-1),
                                 ring_m_kg=m.reshape(-1), s_edges_kpc2=s_edges_kpc2, M_s=M_s, kpc_m=kpc_m)
    return Roster(stars=stars, gas=gas, provenance=dict(rule=rule, n_rings=int(m.size)))


def roster_route_a(stars, init_rings, element_rosters, relaxation, *, s_edges_kpc2, kpc_m, M_s, c_m_s):
    """Route-A iteration-n roster: gas_n = (1-r)^n init + sum_m r(1-r)^(n-1-m) updated_m (mirrors solver L215,
    gas=(1-r)gas+r updated), with the coefficients built by that same recursion. init_rings = dict(R,z,m) (prep
    v007 L202-211, razor-thin, z=0); element_rosters = [dict(positions_m, integrated_J), ...] for m = 0..n-1."""
    coeff = [1.0]; r = float(relaxation)
    for _ in element_rosters:
        coeff = [(1 - r) * c for c in coeff] + [r]
    zs = []; ms = []; Rs = []
    for (R, z, m) in zip(init_rings['R'], init_rings['z'], init_rings['m']):
        Rs.append(R); zs.append(z); ms.append(coeff[0] * m)
    for cm, el in zip(coeff[1:], element_rosters):
        pos = np.asarray(el['positions_m'], float); J = np.asarray(el['integrated_J'])
        if J.ndim == 3: J = J[:, 0, 0]
        J = np.real(J).astype(float)
        Rs.extend(np.hypot(pos[:, 0], pos[:, 1]).tolist()); zs.extend(pos[:, 2].tolist())
        ms.extend((cm * (-J / (c_m_s * c_m_s))).tolist())
    # azimuthal positions collapse onto their column radius (m=0 projection, declared rule)
    allR, _ = annulus_columns(list(map(float, s_edges_kpc2)), kpc_m)
    Rsn = []
    for R in Rs:
        j = int(np.argmin(np.abs(allR - R)))
        if abs(allR[j] - R) > 1e-12 * R:
            raise ValueError('UV_TAIL_ELEMENT_OFF_COLUMN R=%r' % R)
        Rsn.append(allR[j])
    gas = gas_columns_from_rings(ring_R_m=Rsn, ring_z_m=zs, ring_m_kg=ms, s_edges_kpc2=s_edges_kpc2, M_s=M_s, kpc_m=kpc_m)
    return Roster(stars=stars, gas=gas, provenance=dict(rule='route_a_mixture', relaxation=r, coefficients=coeff))


def roster_body(body_arrays, stars, *, s_edges_kpc2, kpc_m, M_s, c_m_s):
    """Body base_integrated_source_J at physical_positions_m -> roster (all azimuths, m=0 projection)."""
    pos = np.asarray(body_arrays['physical_positions_m'], float).reshape(-1, 3)
    J = np.asarray(body_arrays['base_integrated_source_J'])
    J = J.reshape(len(pos), -1)[:, 0] if J.size != len(pos) else J.reshape(-1)
    R = np.hypot(pos[:, 0], pos[:, 1])
    allR, allrdr = annulus_columns(list(map(float, s_edges_kpc2)), kpc_m)
    nodes = np.unique(np.array([allR[int(np.argmin(np.abs(allR - r)))] for r in R]))
    rdr = np.array([allrdr[int(np.argmin(np.abs(allR - r)))] for r in nodes])
    gas = gas_columns(pos, J, radial_nodes_m=nodes, rdr_weights_m2=rdr, s_edges_kpc2=s_edges_kpc2, M_s=M_s,
                      kpc_m=kpc_m, c_m_s=c_m_s)
    return Roster(stars=stars, gas=gas, provenance=dict(rule='body_base_integrated_source_J', n_elements=int(len(pos))))


def source_continuum(roster, k_perp_m, k_z_m, c_m_s, j0):
    """S_T on the tensor grid (Nk, Nz) complex -- small grids only (tests)."""
    P, F = roster.factors(k_perp_m, k_z_m, c_m_s, j0)
    return P @ F.T


# ----------------------------------------------------------------------------- discrete packet transforms (I1-T)
def ring_transform(R_m, z_m, m_kg, waves, c_m_s, j0):
    """S(k) = -c^2 sum m J0(k_perp R) exp(-i k_z z) (axisymmetric_initial_rest_energy_fourier_v001 L42 formula)."""
    k = np.asarray(waves, float); R = np.asarray(R_m, float); z = np.asarray(z_m, float); m = np.asarray(m_kg, float)
    kp = np.hypot(k[:, 0], k[:, 1]); out = np.zeros(len(k), complex)
    for a in range(0, len(k), 256):
        b = min(a + 256, len(k))
        out[a:b] = -c_m_s * c_m_s * np.einsum('kr,kr,r->k', j0(kp[a:b, None] * R[None, :]),
                                              np.exp(-1j * k[a:b, 2, None] * z[None, :]), m, optimize=False)
    return out


def point_transform(positions_m, J, waves):
    """S(k) = sum_l J_l exp(-i k.x_l) (physical_source_fourier / offset Cartesian forward-sum formula)."""
    k = np.asarray(waves, float); x = np.asarray(positions_m, float); J = np.asarray(J)
    if J.ndim == 3: J = J[:, 0, 0]
    out = np.zeros(len(k), complex)
    for a in range(0, len(k), 128):
        b = min(a + 128, len(k))
        out[a:b] = np.exp(-1j * (k[a:b] @ x.T)) @ J
    return out


def packet_transform(elements, waves, kind, *, c_m_s=None, j0=None):
    """Formula replicas of the stage transforms (sec 1.3). T2-I (<= 1e-12 vs stored C6 sources) is the deciding test
    that they are the stage arithmetic; until it runs they are formula-level (UNTESTED as byte replicas)."""
    if kind in ('prep_analytic_j0', 'feedback_ring_j0_v002', 'feedback_ring_j0_v004'):
        return ring_transform(elements['R'], elements['z'], elements['m'], waves, c_m_s, j0)
    if kind in ('physical_source_fourier', 'offset_cartesian_v003'):
        return point_transform(elements['positions_m'], elements['integrated_J'], waves)
    raise ValueError('UV_TAIL_TRANSFORM_KIND ' + str(kind))


def check_represented(transform_sample, packet_sample, kind, rtol=1e-12):
    """I1-T: represented discrete roster transform vs the stage's packet source at sampled nodes."""
    a = np.asarray(transform_sample, complex); b = np.asarray(packet_sample, complex)
    if a.shape != b.shape or not a.size:
        raise ValueError('UV_TAIL_SOURCE_MISMATCH shape')
    scale = float(np.max(np.abs(b)))
    rel = float(np.max(np.abs(a - b)) / scale) if scale > 0 else float(np.max(np.abs(a - b)))
    rec = dict(kind=kind, n=int(a.size), max_rel=rel, rtol=rtol, verdict='PASS' if rel <= rtol else 'FAIL')
    if rel > rtol:
        raise ValueError('UV_TAIL_SOURCE_MISMATCH max_rel=%.3e kind=%s' % (rel, kind))
    return rec


def stars_gl4_rings(profile_record, galaxy, *, kpc_m, solar_mass_kg, gauss_order, radial_surface=None):
    """Replica of prep v007 L172-190 (analytic branch star rings): (R, z, m) for the I1-T stars check."""
    if radial_surface is None:
        radial_surface = load_pinned(FORWARD_V002, FORWARD_V002_SHA, 'forward_v002').radial_surface
    st = profile_record['galaxies'][galaxy]['stellar_reference']
    pc_m = kpc_m / 1000; sigma_unit = solar_mass_kg / (pc_m * pc_m)
    gx, gw = np.polynomial.legendre.leggauss(gauss_order)
    gauss = [(float(x), float(w)) for x, w in zip(gx, gw)]
    radii = [float(x) for x in st['radius_kpc']]; sigmas = [float(x) for x in st['surface_density_Msun_pc2']]
    rd = float(st['outer_scale_kpc']); height = float(st['height_kpc'])
    nodes = []; cuts = sorted(set([0.] + radii))
    for lo, hi in zip(cuts, cuts[1:]):
        for x, w in gauss: nodes.append(((lo + hi) / 2 + (hi - lo) * x / 2, (hi - lo) * w / 2))
    for x, w in gauss:
        u = (x + 1) / 2; nodes.append((radii[-1] - rd * math.log(u), rd * w / (2 * u)))
    R = []; z = []; m = []
    for r, dr in nodes:
        Sigma = radial_surface(r, radii, sigmas, outer_scale=rd) * sigma_unit
        for u, w in gauss:
            R.append(r * kpc_m); z.append(2 * height * kpc_m * math.atanh(u)); m.append(Sigma * (r * kpc_m) * (dr * kpc_m) * (2 * math.pi) * w / 2)
    return dict(R=np.array(R), z=np.array(z), m=np.array(m))
