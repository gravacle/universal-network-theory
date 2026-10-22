"""Route-A UV-tail controller (Claude2 tail_scheme_impl_c2/route_a, c2v001). INERT: nothing runs at import.

Design: TAIL_SCHEME_DESIGN_V002 (cdb16d1c) sec 1.1 (route A: C = cube K, always), 1.2 (E1, R0, jet order 1),
1.3 (continuum_v001; route-A row: fixed + gas_n, the solver L215 mixture), 1.7 (M_T, K13), 3.5 (route-A successors);
revision record TAIL_SCHEME_DESIGN_V002_R1 (5e8eea77): L1 (E^A_i = per-row M_K at the accepted iteration),
IA6 (admissibility), IA7 (roster_route_a mirrors L215), IA8 (I1-T in the route-A successor is the deciding test).
Library: tail_scheme_impl_c2/module owned_uv_tail_lapse_v001.py (c28d4209), uv_tail_source_roster_c2v001.py (4366e3d6),
posix_libm_bessel_jn_provider_c2v001.py (d6c55b55) -- pinned below, sha256 checked from bytes at load.

One object (`RouteATailController`) is what the solver successors receive as `uv_tail` (design sec 3.5 names three
arguments uv_tail / uv_tail_builder / uv_tail_sidecar; here they are one object: .boundary is the TailBoundary,
the builder and sidecar are its methods). The solver calls, in this order:
    bind_check(boundary_jet_at_positions)            before any checkpoint record
    open(relaxation, start_iteration, checkpoint_mode, checkpoint_identity_sha256)   after checkpoint.open_run
    begin_iteration(iteration, gas)                  between solver L111 (current=fixed+gas) and L112 (prepare)
    complete_iteration(iteration, positions, columns, gas, updated, current, prepared, converged)
                                                     after L196-199 (residual, bound), BEFORE checkpoint COMPLETED
    result_record(outcome)                           in _finish (every returned outcome)
Tail state of iteration n = build(stars + gas_n) with gas_n = (1-r)^n init + sum_m r(1-r)^(n-1-m) updated_m (the
solver's own relaxation, mirrored by roster_route_a with the same recursion), C = cube K (K = the prep grid edge).
I1-T at every build: the mixture of the discrete transforms (prep analytic J0 rings for init, Cartesian forward sum for
every updated_m) equals the solver's gas array on 4096 seeded waves to <= 1e-12 (else UV_TAIL_SOURCE_MISMATCH).
M_T(n) = max_i max_j R_i c^2 |d_R(t[S_T(updated_n)] - t[S_T(gas_n)])(R_i, phi_j, 0)| / (2 v_i tau_i), computed as
(t[S_T(gas_{n+1})] - t[S_T(gas_n)]) / r: gas_{n+1} = gas_n + r (updated_n - gas_n) and t is linear in the masses, so
this equals the design formula in exact arithmetic (rounding only); the state of gas_{n+1} is the next iteration's.
M_K(n): the same formula on packet_K[updated_n - gas_n], evaluated from the iteration's prepared response as
W(k) (updated-gas)(k) / current(k) (DECLARED: the prepared lapse response is linear per node in the scalar lapse
source, as the inverse cache v001 L84-86 literally multiplies; nodes with current == 0 -> M_K unavailable).
Sidecar (append-only, exclusive create, nothing replaced): SIDECAR_IDENTITY.json, iteration_NNNN.json,
elements_NNNN.npz (updated_n roster), finish_NNN.json. Resume rebuilds the state from the stored rosters and refuses
any digest difference (UV_TAIL_RESUME_MISMATCH); a re-completed iteration must reproduce its stored payload.
"""
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path
import numpy as np

REQUEST_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_REQUEST_C2V001'
SIDECAR_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_SIDECAR_C2V001'
RECORD_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_RECORD_C2V001'
MODULE_DIR = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module')
PINS = {
    'lib': (MODULE_DIR / 'owned_uv_tail_lapse_v001.py', 'c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22'),
    'roster': (MODULE_DIR / 'uv_tail_source_roster_c2v001.py', '4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2'),
    'provider': (MODULE_DIR / 'posix_libm_bessel_jn_provider_c2v001.py', 'd6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171')}
# The library is registered in sys.modules under this name so TailBoundary/TailState pickle by reference; the parallel
# solver successor registers the same pinned file under the same name in every spawned worker before the environment.
LIB_MODULE_NAME = 'unt_owned_uv_tail_lapse_v001_c2'
MT_THRESHOLD = 0.25            # design sec 1.7 (pre-named); flag TAIL_SOURCE_UNDERCONVERGED above it
I1T_SAMPLES = 4096
I1T_SEED = 20261018
I1T_RTOL = 1e-12
PROFILE_NAME = 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json'


class UVTailRouteAError(RuntimeError):
    """Tail custody/build/sidecar failure. Deliberately NOT a ValueError: never a physical HI-column failure."""


def _sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def _file_sha(path):
    with open(path, 'rb') as f:
        return _sha_bytes(f.read())


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _array_digest(a):
    a = np.ascontiguousarray(a)
    h = hashlib.sha256(); h.update(('%s|%s|' % (a.dtype.str, a.shape)).encode()); h.update(a.tobytes())
    return h.hexdigest()


def _plain(obj):
    if isinstance(obj, dict):
        return {str(k): _plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_plain(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return _plain(obj.tolist())
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, Path):
        return str(obj)
    return obj


# ============================================================================= pinned libraries
def load_libraries():
    """(lib, roster, provider) modules from the pinned module-lane files; lib registered as LIB_MODULE_NAME."""
    out = {}
    for key in ('lib', 'roster', 'provider'):
        path, sha = PINS[key]
        if _file_sha(path) != sha:
            raise UVTailRouteAError('UV_TAIL_PIN_MISMATCH ' + str(path))
        name = LIB_MODULE_NAME if key == 'lib' else 'unt_uvt_%s_c2v001_c2' % key
        mod = sys.modules.get(name)
        if mod is not None:
            if os.path.realpath(getattr(mod, '__file__', '')) != os.path.realpath(path):
                raise UVTailRouteAError('UV_TAIL_MODULE_REGISTRY_CONFLICT ' + name)
        else:
            spec = importlib.util.spec_from_file_location(name, str(path))
            mod = importlib.util.module_from_spec(spec)
            sys.modules[name] = mod
            try:
                spec.loader.exec_module(mod)
            except BaseException:
                sys.modules.pop(name, None)
                raise
            if _file_sha(path) != sha:
                raise UVTailRouteAError('UV_TAIL_PIN_CHANGED_AFTER_IMPORT ' + str(path))
        out[key] = mod
    if out['lib'].PROVIDER_SHA256 != PINS['provider'][1]:
        raise UVTailRouteAError('UV_TAIL_PROVIDER_PIN_DISAGREES_WITH_LIBRARY')
    return out


def code_pins():
    return {str(p): s for p, s in PINS.values()} | {str(Path(__file__).resolve()): _file_sha(__file__)}


# ============================================================================= request
def normalize_request(raw, lib):
    """{'schema', 'uv_tail' (library config, strict), 'admissibility' ('production'|'test_only'), 'monitor'}."""
    if not isinstance(raw, dict) or set(raw) != {'schema', 'uv_tail', 'admissibility', 'monitor'}:
        raise UVTailRouteAError('UV_TAIL_REQUEST_INVALID keys %s' % (sorted(raw) if isinstance(raw, dict) else type(raw).__name__))
    if raw['schema'] != REQUEST_SCHEMA:
        raise UVTailRouteAError('UV_TAIL_REQUEST_INVALID schema')
    if raw['admissibility'] not in ('production', 'test_only'):
        raise UVTailRouteAError('UV_TAIL_REQUEST_INVALID admissibility')
    try:
        cfg = lib.normalize_config(raw['uv_tail'])
    except ValueError as exc:
        raise UVTailRouteAError(str(exc)) from None
    m = raw['monitor']
    keys = {'probe_R_m', 'probe_phi_rad', 'v_ref_km_s', 'tau_km_s', 'threshold', 'provenance'}
    if not isinstance(m, dict) or set(m) != keys:
        raise UVTailRouteAError('UV_TAIL_REQUEST_INVALID monitor keys')

    def floats(v, name, positive):
        if not isinstance(v, list) or not v or any(isinstance(x, bool) or not isinstance(x, (int, float)) for x in v):
            raise UVTailRouteAError('UV_TAIL_REQUEST_INVALID monitor.' + name)
        a = [float(x) for x in v]
        if not all(math.isfinite(x) and (x > 0 or not positive) for x in a):
            raise UVTailRouteAError('UV_TAIL_REQUEST_INVALID monitor.' + name)
        return a
    R = floats(m['probe_R_m'], 'probe_R_m', True); ph = floats(m['probe_phi_rad'], 'probe_phi_rad', False)
    if (m['v_ref_km_s'] is None) != (m['tau_km_s'] is None):
        raise UVTailRouteAError('UV_TAIL_REQUEST_INVALID monitor v_ref/tau must both be given or both null')
    v = None if m['v_ref_km_s'] is None else floats(m['v_ref_km_s'], 'v_ref_km_s', True)
    t = None if m['tau_km_s'] is None else floats(m['tau_km_s'], 'tau_km_s', True)
    if v is not None and not (len(v) == len(t) == len(R)):
        raise UVTailRouteAError('UV_TAIL_REQUEST_INVALID monitor row lengths')
    if m['threshold'] != MT_THRESHOLD:
        raise UVTailRouteAError('UV_TAIL_REQUEST_INVALID monitor.threshold must be the pre-named %r' % MT_THRESHOLD)
    if not isinstance(m['provenance'], dict):
        raise UVTailRouteAError('UV_TAIL_REQUEST_INVALID monitor.provenance')
    out = dict(schema=REQUEST_SCHEMA, uv_tail=cfg, admissibility=raw['admissibility'],
               monitor=dict(probe_R_m=R, probe_phi_rad=ph, v_ref_km_s=v, tau_km_s=t, threshold=MT_THRESHOLD,
                            provenance=_plain(m['provenance'])))
    out['sha256'] = _sha_bytes(_canon(out).encode())
    return out


# ============================================================================= controller
class RouteATailController:
    def __init__(self, *, request, libraries, stars, s_edges_kpc2, kpc_m, kmax_inverse_kpc, init_rings, gamma_eff,
                 c_m_s, eval_radii_m, waves, sidecar_directory, provenance):
        self.lib = libraries['lib']; self.rs = libraries['roster']; self.pv = libraries['provider']
        self.request = normalize_request(request, self.lib)
        cfg = self.request['uv_tail']
        if cfg['enabled'] is not True:
            raise UVTailRouteAError('UV_TAIL_DISABLED_CONFIG_GIVEN_TO_CONTROLLER (tail OFF passes uv_tail=None)')
        if cfg['source_rule'] != 'continuum_v001':
            raise UVTailRouteAError('UV_TAIL_ROUTE_A_REQUIRES_CONTINUUM_V001')
        self.config = cfg
        if float(kpc_m) != self.lib.KPC_M:
            raise UVTailRouteAError('UV_TAIL_UNIT_MISMATCH kpc_m %r != library %r' % (kpc_m, self.lib.KPC_M))
        self.kpc_m = float(kpc_m)
        self.kept = self.lib.kept_region('route_a', None, float(kmax_inverse_kpc) / self.kpc_m)
        self.gamma_eff = float(gamma_eff); self.c_m_s = float(c_m_s)
        self.stars = stars; self.s_edges = [float(x) for x in s_edges_kpc2]; self.M_s = cfg['gas']['M_s']
        self.init_rings = {k: np.array(init_rings[k], dtype=float) for k in ('R', 'z', 'm')}
        mon = self.request['monitor']
        self.probe_R = np.array(mon['probe_R_m'], float); self.probe_phi = np.array(mon['probe_phi_rad'], float)
        radii = np.unique(np.concatenate([np.asarray(eval_radii_m, float), self.probe_R]))
        self.eval_radii = radii
        self.waves = np.asarray(waves, dtype=float)
        nk = len(self.waves)
        rng = np.random.default_rng(I1T_SEED)
        self.i1t_index = np.sort(rng.choice(nk, size=min(I1T_SAMPLES, nk), replace=False))
        self.jn = self.pv.create_provider()
        self.boundary = self.lib.TailBoundary(state=None, order=cfg['jet_order']['route_a'])
        self.sidecar = None if sidecar_directory is None else Path(sidecar_directory)
        self.provenance = _plain(provenance)
        self.elements = []; self._T_init = None; self._T_upd = []
        self.relaxation = None; self._next = None; self._pending = None; self._expected = {}
        self.iterations = []; self.last_record = None; self.checkpoint_identity_sha256 = None
        self._opened = False
        init_digest = _array_digest(np.stack([self.init_rings['R'], self.init_rings['z'], self.init_rings['m']]))
        self.static_identity = dict(schema=SIDECAR_SCHEMA, request_sha256=self.request['sha256'],
            config_sha256=cfg['sha256'], kept=self.kept, outer=cfg['outer'], gamma_eff=self.gamma_eff, c_m_s=self.c_m_s,
            stars=self.stars.record(), s_edges_kpc2=self.s_edges, M_s=self.M_s, init_rings_digest=init_digest,
            eval_radii_digest=_array_digest(self.eval_radii), waves_digest=_array_digest(self.waves),
            i1t=dict(samples=int(len(self.i1t_index)), seed=I1T_SEED, rtol=I1T_RTOL), code_pins=code_pins(),
            provenance=self.provenance)

    # ------------------------------------------------------------------ construction from a reviewed prep result
    @classmethod
    def from_prepared(cls, *, galaxy, prep_module, prep_arguments, data, request, sidecar_directory, libraries=None):
        """DDO154 / NGC3198 from the reviewed prep dictionary (prep v007/v008/v009, NGC prep v001):
        stars (+ NGC H2) = the registered profile the prep itself read (prep_module.C / PROFILE_NAME, sha256 checked
        against data['source_pins']); init rings = the razor-thin initial iterate rings (prep L202-211 arithmetic on
        data['gas_columns'] at the first azimuth); eval radii = gas-column radii + monitor probes + the prediction v005
        query stencil radii (R, R +- step, R +- step/2)."""
        libs = libraries or load_libraries()
        rs = libs['roster']
        ppath = Path(prep_module.C) / PROFILE_NAME
        psha = data['source_pins'].get(str(ppath))
        if psha is None or _file_sha(ppath) != psha:
            raise UVTailRouteAError('UV_TAIL_PROFILE_NOT_THE_PREP_PROFILE ' + str(ppath))
        profile = json.loads(Path(ppath).read_text())
        units = dict(kpc_m=prep_arguments['kpc_m'], solar_mass_kg=prep_arguments['solar_mass_kg'])
        extra = []
        prov = dict(galaxy=galaxy, profile={'path': str(ppath), 'sha256': psha},
                    prep={'path': str(Path(prep_module.__file__).resolve()), 'sha256': _file_sha(prep_module.__file__)})
        if galaxy == 'NGC3198':
            red = data['H2_custody']['reduction']
            h2path = Path(red['source']['path'])
            if _file_sha(h2path) != red['source']['sha256']:
                raise UVTailRouteAError('UV_TAIL_H2_SOURCE_PIN')
            from fractions import Fraction
            rows = json.loads(h2path.read_text())['S1_alternative_and_stellar_median_rows']['rows'][:10]   # prep v001 L76
            hr = [float(Fraction(r['radius_kpc_literal']['value'])) for r in rows]
            hs = [float(Fraction(r['components']['H2']['value_literal']['value'])) for r in rows]
            extra = [dict(name='H2', radius_kpc=hr, surface_density_Msun_pc2=hs, outer_scale_kpc=float(red['outer_scale_kpc']))]
            prov['h2_source'] = {'path': str(h2path), 'sha256': red['source']['sha256']}
        elif galaxy != 'DDO154':
            raise UVTailRouteAError('UV_TAIL_GALAXY ' + repr(galaxy))
        stars = rs.stars_registered(profile, galaxy, units=units, extra_components=tuple(extra))
        cols = data['gas_columns']; phi0 = cols[0]['phi']
        R = []; z = []; m = []
        for col in cols:
            if col['phi'] == phi0:   # prep L207-209
                R.append(col['R_m']); z.append(0.); m.append(col['Sigma_kg_m2'] * col['R_m'] * col['radial_weight_m'] * (2 * math.pi))
        kpc = prep_arguments['kpc_m']; step = float(prep_arguments['pressure_step_kpc'] * kpc)
        stencil = []
        for q in data['queries']:
            Rq = float(q['radius_kpc']) * kpc
            stencil.append(Rq)
            for dR in (step, step / 2):
                stencil += [Rq - dR, Rq + dR]
        eval_radii = np.array([c['R_m'] for c in cols] + stencil, float)
        waves = np.asarray(data['fourier_arguments']['k_physical'], float)
        fixed = data.get('fixed_source_fourier_J')
        if galaxy == 'DDO154' and fixed is not None:
            # I1-T of the stars: the profile the tail uses IS the profile of the packet's fixed term (prep v007
            # L172-190 GL4 rings, analytic J0 transform L237-238), on the same seeded waves as the gas I1-T.
            idx = np.sort(np.random.default_rng(I1T_SEED).choice(len(waves), size=min(I1T_SAMPLES, len(waves)), replace=False))
            rings = rs.stars_gl4_rings(profile, galaxy, kpc_m=units['kpc_m'], solar_mass_kg=units['solar_mass_kg'],
                                       gauss_order=prep_arguments['source_gauss_order'])
            T = rs.ring_transform(rings['R'], rings['z'], rings['m'], waves[idx], data['c_m_s'], libs['provider'].create_provider().j0)
            try:
                prov['fixed_stars_i1t'] = rs.check_represented(T, np.asarray(fixed)[idx, 0, 0], 'route_a_fixed_stars:prep_analytic_j0', rtol=I1T_RTOL)
            except ValueError as exc:
                raise UVTailRouteAError(str(exc)) from None
        else:
            prov['fixed_stars_i1t'] = 'NOT_EVALUATED (%s)' % ('NGC3198 fixed term includes the H2 rings; no replica here'
                                                            if galaxy == 'NGC3198' else 'no supplied fixed term')
        return cls(request=request, libraries=libs, stars=stars,
                   s_edges_kpc2=profile['galaxies'][galaxy]['HI_plus_He']['s_edges_kpc2'], kpc_m=kpc,
                   kmax_inverse_kpc=prep_arguments['kmax_inverse_kpc'], init_rings=dict(R=R, z=z, m=m),
                   gamma_eff=data['fourier_arguments']['gamma'], c_m_s=data['c_m_s'], eval_radii_m=eval_radii,
                   waves=data['fourier_arguments']['k_physical'], sidecar_directory=sidecar_directory, provenance=prov)

    # ------------------------------------------------------------------ custody records
    def worker_modules(self):
        path, sha = PINS['lib']
        return [(LIB_MODULE_NAME, str(path), sha)]

    def identity(self):
        """Plain record for the checkpoint caller identity (numerical_controls.uv_tail)."""
        return dict(request_sha256=self.request['sha256'], config_sha256=self.config['sha256'], config=self.config,
                    admissibility=self.request['admissibility'], monitor=self.request['monitor'], kept=self.kept,
                    static_identity_sha256=_sha_bytes(_canon(self.static_identity).encode()), code_pins=code_pins(),
                    sidecar=None if self.sidecar is None else str(self.sidecar))

    def boundary_prescription_suffix(self):
        return (' UV-TAIL c2v001 (config %s): the boundary_* slots carry the UV-tail lapse jet t of the omitted region '
                'D = O \\ cube K (order %d); the physical boundary perturbation stays zero.'
                % (self.config['sha256'], self.config['jet_order']['route_a']))

    def bind_check(self, boundary_jet_at_positions, checkpoint):
        """Before any checkpoint record: the boundary slot is this TailBoundary, and a checkpoint's caller identity
        carries this tail (numerical_controls.uv_tail == identity()), so a tail ON/OFF or config change is identity."""
        if boundary_jet_at_positions is not self.boundary:
            raise UVTailRouteAError('UV_TAIL_BOUNDARY_NOT_BOUND: boundary_jet_at_positions must be controller.boundary')
        if checkpoint is not None:
            nc = (checkpoint.get('caller_identity') or {}).get('numerical_controls')
            if not isinstance(nc, dict) or json.loads(_canon(_plain(nc.get('uv_tail')))) != json.loads(_canon(_plain(self.identity()))):
                raise UVTailRouteAError('UV_TAIL_NOT_IN_CHECKPOINT_IDENTITY: caller_identity.numerical_controls.uv_tail must be identity()')

    # ------------------------------------------------------------------ sidecar
    def _path(self, name):
        return self.sidecar / name

    def _write_new(self, name, obj):
        p = self._path(name)
        with open(p, 'x') as f:
            f.write(_canon(obj)); f.flush(); os.fsync(f.fileno())
        return p

    def _read(self, name):
        try:
            return json.loads(self._path(name).read_text())
        except (OSError, ValueError) as exc:
            raise UVTailRouteAError('UV_TAIL_SIDECAR_UNREADABLE %s %s' % (name, type(exc).__name__)) from None

    def open(self, *, relaxation, start_iteration, checkpoint_mode, checkpoint_identity_sha256):
        if self._opened:
            raise UVTailRouteAError('UV_TAIL_CONTROLLER_ALREADY_OPEN (one solve per controller)')
        self._opened = True
        self.relaxation = float(relaxation); self._next = int(start_iteration)
        self.checkpoint_identity_sha256 = checkpoint_identity_sha256
        ident = dict(self.static_identity, relaxation=self.relaxation, checkpoint_identity_sha256=checkpoint_identity_sha256)
        self.sidecar_identity = ident
        if self.sidecar is None:
            if start_iteration != 0:
                raise UVTailRouteAError('UV_TAIL_RESUME_WITHOUT_SIDECAR')
            return
        if checkpoint_mode == 'resume' and start_iteration == 0 and not self.sidecar.exists():
            checkpoint_mode = 'new'   # interrupted before the sidecar existed: nothing of the tail to resume
        if checkpoint_mode == 'resume':
            stored = self._read('SIDECAR_IDENTITY.json')
            if stored.get('identity') != json.loads(_canon(ident)):
                raise UVTailRouteAError('UV_TAIL_RESUME_MISMATCH sidecar identity differs')
            for n in range(start_iteration):
                rec = self._read('iteration_%04d.json' % n)['payload']
                with np.load(self._path(rec['elements']['file']), allow_pickle=False) as f:
                    pos = f['positions_m'].copy(); J = f['integrated_J'].copy()
                if (_array_digest(pos) != rec['elements']['positions_digest'] or _array_digest(J) != rec['elements']['J_digest']
                        or rec['iteration'] != n):
                    raise UVTailRouteAError('UV_TAIL_RESUME_MISMATCH elements of iteration %d' % n)
                self.elements.append(dict(positions_m=pos, integrated_J=J))
                self.iterations.append(dict(rec['summary'], reloaded=True))
                if n == start_iteration - 1:
                    self._expected[start_iteration] = rec['next_state_digest']
        else:
            try:
                os.mkdir(self.sidecar)
            except FileExistsError:
                raise UVTailRouteAError('UV_TAIL_SIDECAR_EXISTS (never reused as new): ' + str(self.sidecar)) from None
            self._write_new('SIDECAR_IDENTITY.json', dict(identity=ident, identity_sha256=_sha_bytes(_canon(ident).encode())))

    # ------------------------------------------------------------------ I1-T and build
    def _coefficients(self, n):
        coeff = [1.0]; r = self.relaxation
        for _ in range(n):
            coeff = [(1 - r) * c for c in coeff] + [r]
        return coeff

    def _i1t(self, n, gas):
        g = np.asarray(gas)
        if g.ndim != 3 or g.shape[1:] != (10, 1) or len(g) != len(self.waves) or np.any(g[:, 1:, :] != 0):
            raise UVTailRouteAError('UV_TAIL_SOURCE_MISMATCH gas array is not a scalar-lapse [nk,10,1] source')
        k = self.waves[self.i1t_index]
        if self._T_init is None:
            self._T_init = self.rs.ring_transform(self.init_rings['R'], self.init_rings['z'], self.init_rings['m'], k,
                                                  self.c_m_s, self.jn.j0)
        while len(self._T_upd) < n:
            e = self.elements[len(self._T_upd)]
            self._T_upd.append(self.rs.point_transform(e['positions_m'], e['integrated_J'], k))
        coeff = self._coefficients(n)
        T = coeff[0] * self._T_init
        for c, Tm in zip(coeff[1:], self._T_upd[:n]):
            T = T + c * Tm
        try:
            rec = self.rs.check_represented(T, g[self.i1t_index, 0, 0], 'route_a_mixture:prep_analytic_j0+physical_source_fourier',
                                            rtol=I1T_RTOL)
        except ValueError as exc:
            raise UVTailRouteAError(str(exc)) from None
        rec['iteration_source'] = n
        return rec

    def _build(self, n, i1t):
        roster = self.rs.roster_route_a(self.stars, self.init_rings, self.elements[:n], self.relaxation,
                                        s_edges_kpc2=self.s_edges, kpc_m=self.kpc_m, M_s=self.M_s, c_m_s=self.c_m_s)
        try:
            st = self.lib.build(config=self.config, kept=self.kept, roster=roster, gamma_eff=self.gamma_eff,
                                c_m_s=self.c_m_s, eval_radii_m=self.eval_radii, jn_provider=self.jn, i1t=i1t,
                                stage_kind='route_a')
        except ValueError as exc:
            raise UVTailRouteAError(str(exc)) from None
        if self.request['admissibility'] == 'production' and not st.record['production_admissible']:
            raise UVTailRouteAError('UV_TAIL_STATE_NOT_PRODUCTION_ADMISSIBLE')
        return st

    # ------------------------------------------------------------------ solver hooks
    def begin_iteration(self, *, iteration, gas):
        if not self._opened or iteration != self._next:
            raise UVTailRouteAError('UV_TAIL_SEQUENCE_ERROR iteration %r expected %r' % (iteration, self._next))
        t0 = time.monotonic()
        p = self._pending
        if p is not None and p[0] == iteration and p[2] == _array_digest(gas):
            st = p[1]; built = 'prebuilt_at_previous_completion'
        else:
            st = self._build(iteration, self._i1t(iteration, gas)); built = 'built_here'
        exp = self._expected.get(iteration)
        if exp is not None and exp != st.digest:
            raise UVTailRouteAError('UV_TAIL_RESUME_MISMATCH state digest of iteration %d' % iteration)
        if self.sidecar is not None and self._path('iteration_%04d.json' % iteration).exists():
            if self._read('iteration_%04d.json' % iteration)['payload']['state_digest'] != st.digest:
                raise UVTailRouteAError('UV_TAIL_RESUME_MISMATCH stored iteration %d state digest' % iteration)
        self.boundary.set_state(st)
        self._pending = None
        self._current = dict(iteration=iteration, state=st, built=built, seconds=time.monotonic() - t0)
        return st.digest

    def _rows_T(self, st_next, st_now):
        r = self.relaxation; c2 = self.c_m_s ** 2; rows = []
        for Ri in self.probe_R:
            def dR(st):
                if st.empty:
                    return np.zeros(len(self.probe_phi))
                return st.cyl_jets(Ri, self.probe_phi, [0.0], 1)['fR'][:, 0]
            d = (dR(st_next) - dR(st_now)) / r
            rows.append(float(np.max(np.abs(d))) * Ri * c2 / 2.0)     # m^2/s^2: R c^2 |d_R dt| / 2
        return np.array(rows)

    def _rows_K(self, prepared, current, gas, updated):
        cur = np.asarray(current)[:, 0, 0]; d = (np.asarray(updated) - np.asarray(gas))[:, 0, 0]
        W = np.asarray(prepared['weighted_responses'])[:, 0, 0]; k = np.asarray(prepared['wavevectors'], float)
        if k.shape != self.waves.shape or np.any(cur == 0) or not np.all(np.isfinite(cur)):
            return None, 'UNAVAILABLE: current lapse source has zero or nonfinite nodes, or waves differ'
        a = W * (d / cur)
        if not np.all(np.isfinite(a)):
            return None, 'UNAVAILABLE: nonfinite ratio'
        c2 = self.c_m_s ** 2; rows = []
        cph = np.cos(self.probe_phi); sph = np.sin(self.probe_phi)
        for Ri in self.probe_R:
            x = Ri * cph; y = Ri * sph
            vals = []
            for j in range(len(self.probe_phi)):
                phase = np.exp(1j * (k[:, 0] * x[j] + k[:, 1] * y[j]))
                kR = k[:, 0] * cph[j] + k[:, 1] * sph[j]
                vals.append(abs(float(np.sum(a * phase * (1j * kR)).real)))
            rows.append(max(vals) * Ri * c2 / 2.0)
        return np.array(rows), 'OK: ratio form W*(updated-gas)/current (DECLARED linear lapse response)'

    def _normalize(self, raw):
        mon = self.request['monitor']
        if raw is None:
            return None, None, None
        if mon['v_ref_km_s'] is None:
            return raw.tolist(), None, 'UNNORMALIZED_NO_FORWARD_VREF (rows in m^2/s^2 = R c^2 |d_R dn| / 2)'
        v = np.array(mon['v_ref_km_s']) * 1e3; tau = np.array(mon['tau_km_s'])
        kms = raw / v / 1e3
        return kms.tolist(), float(np.max(kms / tau)), 'TAU_UNITS (rows in km/s = R c^2 |d_R dn| / (2 v_ref))'

    def complete_iteration(self, *, iteration, positions, columns, gas, updated, current, prepared, converged):
        cur = getattr(self, '_current', None)
        if cur is None or cur['iteration'] != iteration:
            raise UVTailRouteAError('UV_TAIL_SEQUENCE_ERROR complete %r' % iteration)
        t0 = time.monotonic()
        pos = np.asarray(positions, dtype=float).reshape(-1, 3)
        J = np.array([c[0][0] for c in columns], dtype=float)
        if len(pos) != len(J) or any(any(v != 0.0 for row in c[1:] for v in row) for c in columns):
            raise UVTailRouteAError('UV_TAIL_SOURCE_MISMATCH updated elements are not scalar-lapse columns')
        if len(self.elements) != iteration:
            raise UVTailRouteAError('UV_TAIL_SEQUENCE_ERROR element roster count')
        self.elements.append(dict(positions_m=pos, integrated_J=J))
        r = self.relaxation
        g_next = (1 - r) * gas + r * updated          # the solver L215 expression (bitwise the next iterate)
        st_next = self._build(iteration + 1, self._i1t(iteration + 1, g_next))
        st_now = cur['state']
        rows_T = self._rows_T(st_next, st_now)
        rows_K, k_status = self._rows_K(prepared, current, gas, updated)
        T_rows, M_T, T_units = self._normalize(rows_T)
        K_rows, M_K, K_units = self._normalize(rows_K)
        summary = dict(iteration=iteration, state_digest=st_now.digest, next_state_digest=st_next.digest,
                       M_T=M_T, M_T_rows=T_rows, M_T_units=T_units, M_K=M_K, M_K_rows=K_rows, M_K_units=K_units,
                       M_K_status=k_status, converged=bool(converged),
                       i1t_max_rel=st_now.record['i1t'].get('max_rel'),
                       production_admissible=bool(st_now.record['production_admissible']), empty=bool(st_now.empty))
        name = 'elements_%04d.npz' % iteration
        payload = dict(schema=SIDECAR_SCHEMA, iteration=iteration, state_digest=st_now.digest,
                       next_state_digest=st_next.digest, i1t=_plain(st_now.record['i1t']),
                       next_i1t=_plain(st_next.record['i1t']), relaxation=r,
                       elements=dict(file=name, count=int(len(J)), positions_digest=_array_digest(pos), J_digest=_array_digest(J)),
                       summary=summary)
        payload = json.loads(_canon(payload))
        diag = dict(begin_build=cur['built'], begin_seconds=cur['seconds'], complete_seconds=time.monotonic() - t0,
                    state_record_quadrature=_plain(st_now.record.get('quadrature')),
                    state_diagnostics=_plain(st_now.diagnostics))
        if self.sidecar is not None:
            rec_name = 'iteration_%04d.json' % iteration
            if self._path(rec_name).exists():
                if self._read(rec_name)['payload'] != payload:
                    raise UVTailRouteAError('UV_TAIL_SIDECAR_CONFLICT re-completed iteration %d differs' % iteration)
                summary = dict(summary, reproduced_existing_record=True)
            else:
                if self._path(name).exists():   # written by an interrupted attempt before its record: must be these arrays
                    with np.load(self._path(name), allow_pickle=False) as f:
                        same = _array_digest(f['positions_m']) == _array_digest(pos) and _array_digest(f['integrated_J']) == _array_digest(J)
                    if not same:
                        raise UVTailRouteAError('UV_TAIL_SIDECAR_CONFLICT elements of iteration %d differ' % iteration)
                else:
                    with open(self._path(name), 'xb') as f:
                        np.savez(f, positions_m=pos, integrated_J=J); f.flush(); os.fsync(f.fileno())
                self._write_new(rec_name, dict(payload=payload, diagnostics=diag))
        self.iterations.append(summary)
        self._pending = (iteration + 1, st_next, _array_digest(g_next))
        self._next = iteration + 1
        self._current = None
        return summary

    def result_record(self, *, outcome):
        accepted = None
        if outcome == 'CONVERGED_FINITE_FIXED_POINT' and self.iterations and self.iterations[-1].get('converged'):
            accepted = self.iterations[-1]
        flags = []
        status = 'NO_ACCEPTED_ITERATION'
        if accepted is not None:
            if accepted['M_T'] is None:
                status = 'M_T_NOT_NORMALIZED'
            elif accepted['M_T'] > MT_THRESHOLD:
                flags.append('TAIL_SOURCE_UNDERCONVERGED'); status = 'FLAGGED'
            else:
                status = 'M_T_WITHIN_THRESHOLD'
        st = self.boundary.state
        rec = dict(schema=RECORD_SCHEMA, outcome=outcome, request_sha256=self.request['sha256'],
                   config_sha256=self.config['sha256'], admissibility=self.request['admissibility'], kept=self.kept,
                   outer=self.config['outer'], checkpoint_identity_sha256=self.checkpoint_identity_sha256,
                   boundary_state_digest_at_return=None if st is None else st.digest,
                   production_admissible=None if st is None else bool(st.record['production_admissible']),
                   iterations=self.iterations, accepted_iteration=None if accepted is None else accepted['iteration'],
                   M_T_accepted=None if accepted is None else accepted['M_T'], M_T_threshold=MT_THRESHOLD,
                   monitor_status=status, flags=flags,
                   E_A_rows_km_s_accepted=None if accepted is None or accepted['M_K_units'] is None
                   or not accepted['M_K_units'].startswith('TAU') else accepted['M_K_rows'],
                   sidecar=None)
        if self.sidecar is not None:
            files = {}
            for p in sorted(self.sidecar.iterdir()):
                if p.is_file() and not p.name.startswith('finish_'):
                    files[p.name] = _file_sha(p)
            i = 0
            while self._path('finish_%03d.json' % i).exists():
                i += 1
            fin = self._write_new('finish_%03d.json' % i, dict(record=_plain({k: v for k, v in rec.items() if k != 'sidecar'}),
                                                               files=files))
            rec['sidecar'] = dict(directory=str(self.sidecar), finish={'path': str(fin), 'sha256': _file_sha(fin)}, files=files)
        rec = _plain(rec)
        self.last_record = rec
        return rec
