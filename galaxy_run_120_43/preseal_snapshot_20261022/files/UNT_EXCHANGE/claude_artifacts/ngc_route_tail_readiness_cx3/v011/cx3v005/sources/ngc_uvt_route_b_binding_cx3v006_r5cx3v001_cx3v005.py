"""Shared UV-tail binding of the route-B stage successors *_gal_c2v005_uvt_c2v001.py (Claude2 tail_scheme_impl_c2/route_b).

TAIL_SCHEME_DESIGN_V002 sec 1.1, 1.3, 2.2, 3.6 with the V002_R1 revision record (IA4 single source family, IA6 certificate
admissibility). INERT at import (no file reads, no arithmetic). Loaded by every successor through a pinned-bytes loader.

The tail enters ONLY through the reviewed additive boundary slots (line v002 evaluate_line boundary_*, lapse_difference
boundary_lapse_at_zero / boundary_lapse_difference, the reference/body boundary_jet_at_positions callback) and, in the offset,
one guarded addition to the lapse component of the real-space offset fields before the total (N1: diagnostic only).

  enabled == False  -> every accessor returns the reviewed zero literals (np.zeros of the reviewed shapes, float64); no record
                       is added to any output; no tail arithmetic, no manifest, no roster.
  enabled == True   -> the stage's TailState (owned_uv_tail_lapse_v001.build or, for reference/body, the route-A accepted-iteration
                       state from the route-A tail manifest); an EMPTY domain (O inside C) gives exactly the reviewed zeros again.

Per-stage kept region C (sec 1.1): reference/body cube K (always); offset and fs/rfs/LE columns and rotations the stage
truncation (argv --uv-tail-truncation, checked against the stage's own packet: every row outside C exactly zero and no
all-zero row inside C, else UV_TAIL_KEPT_REGION_EVIDENCE).
Per-stage tail source (continuum_v001; sec 1.3):
  reference, body            route-A mixture at the accepted iteration (manifest state; I1-T done by route A)
  offset                     Delta = body gas - route-A gas_IT (stars cancel exactly; sec 1.3 'old-field/new-source')
  fs_columns, fs_rotation    stars (registered profile) + body gas (offset updated_base_arrays: -c^2 rho0 vol at physical_positions_m)
  rfs/le columns, le_rotation stars + the rings of the rotation the feedback transformed (--uv-tail-source-rotation-directory)
I1-T (sec 1.3, custody): the represented discrete roster transform vs the stage's own packet source at 4096 seeded nodes,
max relative difference <= 1e-12, else UV_TAIL_SOURCE_MISMATCH.
nodes_v001 (T2) is not bound here: refused (UV_TAIL_NODES_V001_NOT_BOUND_ROUTE_B_C2V001).
NGC-only successor (0517): registered stars + H2 continuum; prep finite H2 packet replica for I1-T; anisotropic cube quadrature. DDO stages retain the original binding.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import numpy as np

SCHEMA = 'UNT_UV_TAIL_ROUTE_B_BINDING_C2V001'
RECORD_SCHEMA = 'UNT_UV_TAIL_ROUTE_B_STAGE_RECORD_C2V001'
MANIFEST_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_MANIFEST_C2V001'
MODULE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module')
PINS = {
    'radial_kernel': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/annular_source_kernel_0403/annular_bernstein_source_kernel_v001.py'), '2544d22f46dbf225139f92f6a566f814e5857f265c43d88565c6a4d3894a759e'),
    'grid_cut': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_grid_cut_cx3v001_cx3v005.py'), '5d037291c8d683d7921f38365640bf41502216a67a5ed6ca84986aa671faf353'),
    'lib': (MODULE / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py', '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'),
    'roster': (MODULE / 'uv_tail_source_roster_c2v001.py', '4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2'),
    'jn': (MODULE / 'posix_libm_bessel_jn_provider_c2v001.py', 'd6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171'),
}
KINDS = ('reference', 'body', 'offset', 'fs_columns', 'fs_rotation', 'rfs_columns', 'le_columns', 'le_rotation')
MANIFEST_KINDS = ('reference', 'body', 'offset')
MASK_KINDS = ('offset', 'fs_columns', 'fs_rotation', 'rfs_columns', 'le_columns', 'le_rotation')
ROTATION_SOURCE_KINDS = ('rfs_columns', 'le_columns', 'le_rotation')
TAP_KINDS = ('reference', 'body', 'fs_columns')
GALAXIES = ('NGC3198',)
I1T_SEED = 20261018
I1T_NODES = 4096
I1T_RTOL = 1e-12


class Refusal(ValueError):
    def __init__(self, code, detail=''):
        self.code = code
        super().__init__(code + ((' ' + detail) if detail else ''))


def _sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _load(name):
    path, pin = PINS[name]
    if _sha_file(path) != pin:
        raise Refusal('UV_TAIL_PIN_MISMATCH', str(path))
    spec = importlib.util.spec_from_file_location('uvt_rb_' + name + '_c2v001', str(path))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    if _sha_file(path) != pin:
        raise Refusal('UV_TAIL_PIN_CHANGED_AFTER_IMPORT', str(path))
    return mod


def _hex64(v):
    return type(v) is str and len(v) == 64 and all(c in '0123456789abcdef' for c in v)


def add_argv(p, kind):
    """The successor argv (sec 3.6; eps/lo certificates are config fields verified from bytes at build, R1 IA6)."""
    if kind not in KINDS:
        raise Refusal('UV_TAIL_STAGE_KIND', repr(kind))
    p.add_argument('--uv-tail-config', required=True)
    p.add_argument('--uv-tail-config-sha256', required=True)
    p.add_argument('--uv-tail-admit-test-only', action='store_true',
                   help='admit a state that is not production admissible (NONE_TEST_ONLY certificates or a synthetic roster) and '
                        'producers without a tail record (static replay); recorded; never passed by the driver')
    if kind in MASK_KINDS:
        p.add_argument('--uv-tail-truncation', default=None, help="stage truncation JSON (driver normalization); absent = cube")
    if kind in MANIFEST_KINDS:
        p.add_argument('--route-a-tail-manifest', default=None)
        p.add_argument('--route-a-tail-manifest-sha256', default=None)
    if kind in ROTATION_SOURCE_KINDS:
        p.add_argument('--uv-tail-source-rotation-directory', default=None)
    if kind in TAP_KINDS:
        p.add_argument('--uv-tail-tap', type=int, default=0, help='B3 only: record the first N (pos, jet) pairs to uv_tail_tap.npz')


def _reviewed_zero_jets(n):
    # the reviewed zero literals (prep v007 L214-218; stage boundary closures and evaluate_line keywords)
    return dict(boundary_fields=np.zeros((n, 10, 1)), boundary_gradient=np.zeros((n, 10, 1, 3)),
                boundary_hessian=np.zeros((n, 10, 1, 3, 3)))


class _DifferenceRoster:
    """S_T(a) - S_T(b) in the factor form S = P @ F.T (offset Delta; stars excluded on both sides, they cancel exactly)."""

    def __init__(self, a, b, synthetic):
        self.a = a; self.b = b; self.kind = 'synthetic' if synthetic else 'registered'; self.stars = None
        self.gas = a.gas

    def radial_factors(self, k, j0):
        cols = [self.a.radial_factors(k, j0)]
        if self.b is not None:
            cols.append(self.b.radial_factors(k, j0))
        return np.concatenate(cols, axis=1)

    def vertical_factors(self, kz, c):
        cols = [self.a.vertical_factors(kz, c)]
        if self.b is not None:
            cols.append(-self.b.vertical_factors(kz, c))
        return np.concatenate(cols, axis=1)

    def extent(self):
        ea = self.a.extent()
        if self.b is None:
            return ea
        eb = self.b.extent()
        return {k: max(ea[k], eb[k]) for k in ea}

    def record(self):
        return dict(kind=self.kind, rule='offset_delta_body_minus_route_a_gas', a=self.a.record(),
                    b=None if self.b is None else self.b.record())

    def digest(self):
        h = hashlib.sha256(b'offset_delta|'); h.update(self.a.digest().encode())
        h.update(b'|none' if self.b is None else self.b.digest().encode())
        return h.hexdigest()


class Binding:
    def __init__(self, a, kind, cfg, raw_sha):
        self.kind = kind; self.cfg = cfg; self.enabled = bool(cfg['enabled']); self.args = a
        self.config_file_sha256 = raw_sha
        self.test_only = bool(getattr(a, 'uv_tail_admit_test_only', False))
        self.state = None; self.tb = None; self.rec = None; self.lineage = []; self.calls = {'jets': 0, 'lapse_pair': 0}
        self.lib = self.rs = self.pv = self.jn = None
        self._offset_pending = None
        self.h2_custody = None
        self.ngc_outer_gas_cut_custody = None
        self.ngc_radial_count_custody = None

    # ---------------------------------------------------------------- slot accessors (reviewed zeros when disabled)
    def jets(self, pos):
        pos = np.asarray(pos, dtype=float)
        if self.tb is None:
            if self.enabled:
                raise Refusal('UV_TAIL_STATE_NOT_BOUND', self.kind)
            return _reviewed_zero_jets(len(pos))
        self.calls['jets'] += 1
        return self.tb(pos)

    def line_jets(self, line, z):
        if self.tb is None and not self.enabled:
            return _reviewed_zero_jets(1)
        return self.jets(np.array([[float(line['x_m']), float(line['y_m']), float(z)]]))

    def line_lapse_pair(self, line, z):
        if self.tb is None:
            if self.enabled:
                raise Refusal('UV_TAIL_STATE_NOT_BOUND', self.kind)
            return dict(boundary_lapse_at_zero=np.zeros(1), boundary_lapse_difference=np.zeros(1))
        self.calls['lapse_pair'] += 1
        b0, bd = self.tb.lapse_pair(float(line['x_m']), float(line['y_m']), float(z), 1)
        return dict(boundary_lapse_at_zero=b0, boundary_lapse_difference=bd)

    def offset_fields(self, fields, pos):
        """Offset L258 split: fields[:,0] += t[Delta](pos) only for a non-empty state; otherwise the SAME object (no
        addition at all: -0.0 + 0.0 would change bytes, design S3)."""
        if not self.enabled or self.state is None or self.state.empty:
            if self.enabled and self.state is None:
                raise Refusal('UV_TAIL_STATE_NOT_BOUND', self.kind)
            return fields
        t = self.state.value(np.asarray(pos, float).reshape(-1, 3))
        out = np.array(fields, copy=True)
        out[:, 0] = out[:, 0] + t
        self.calls['jets'] += len(t)
        return out

    def boundary_text(self):
        return ('UV-tail lapse boundary (uvt_c2v001; %s state %s); otherwise the actual zero imposed perturbations'
                % ('EMPTY' if self.state.empty else 'non-empty', self.state.digest))

    def record(self, final=False):
        if not self.enabled:
            return {}
        if self.rec is None:
            if final:
                raise Refusal('UV_TAIL_STATE_NOT_BOUND', self.kind)
            return {'uv_tail': dict(schema=RECORD_SCHEMA, stage_kind=self.kind, enabled=True, config_sha256=self.cfg['sha256'],
                                    config_file_sha256=self.config_file_sha256, binding_sha256=_sha_file(__file__),
                                    state='PENDING: built after the new-body forward transform (offset); see finish.json')}
        r = dict(self.rec)
        r['lineage'] = list(self.lineage)
        if final:
            st = self.state
            r['diagnostics'] = dict(calls=dict(self.calls), **({} if st is None else {k: v for k, v in st.diagnostics.items()}))
            tap = int(getattr(self.args, 'uv_tail_tap', 0) or 0)
            if tap > 0 and self.tb is not None:
                out = Path(self.args.outdir) / 'uv_tail_tap.npz'
                pos = np.array([p for p, _ in self.tb.tapped]).reshape(-1, 3) if self.tb.tapped else np.zeros((0, 3))
                arr = {'positions_m': pos}
                for key in ('boundary_fields', 'boundary_gradient', 'boundary_hessian'):
                    arr[key] = np.concatenate([j[key] for _, j in self.tb.tapped]) if self.tb.tapped else np.zeros((0,))
                np.savez(out, **arr)
                r['tap'] = dict(path=str(out), sha256=_sha_file(out), count=len(self.tb.tapped))
            r['srb_rot'] = ('NOT_EVALUATED: test-only certificates' if self.cfg['eps_certificate'] == self.lib.TEST_ONLY_CERT
                            else 'NOT_EVALUATED_IN_STAGE: SRB-ROT is a gate on the C4T rows (sec 1.5), computed by gates/ from this state digest')
        return {'uv_tail': r}

    # ---------------------------------------------------------------- shared checks
    def _modules(self):
        if self.lib is None:
            self.lib = _load('lib')
        if self.rs is None:
            self.rs = _load('roster'); self.pv = _load('jn'); self.jn = self.pv.create_provider()

    def _galaxy(self, galaxy):
        if galaxy not in GALAXIES:
            raise Refusal('UV_TAIL_ROUTE_B_GALAXY_NOT_BOUND_C2V001', repr(galaxy))

    def _grid_K(self, ni, waves):
        anisotropic = ni.get('composite_grid_spec_anisotropic')
        if anisotropic is not None:
            if ni.get('composite_grid_spec') is not None:
                raise Refusal('UV_TAIL_GRID_AMBIGUOUS', 'both isotropic and anisotropic grids supplied')
            try:
                axes = anisotropic['axes']
                bounds = [(float(axes[k]['breaks_inverse_kpc'][0]), float(axes[k]['breaks_inverse_kpc'][-1])) for k in ('x', 'y', 'z')]
            except (KeyError, TypeError, ValueError, IndexError):
                raise Refusal('UV_TAIL_KEPT_INVALID', 'anisotropic axis endpoints missing') from None
            if any(lo != -hi or hi <= 0 or not math.isfinite(hi) for lo, hi in bounds) or len(set(bounds)) != 1:
                raise Refusal('UV_TAIL_KEPT_INVALID', 'anisotropic quadrature must cover one symmetric cube')
            br = list(bounds[0])
        else:
            br = [float(x) for x in ni['composite_grid_spec']['breaks_inverse_kpc']]
        if br[0] != -br[-1] or br[-1] <= 0:
            raise Refusal('UV_TAIL_KEPT_INVALID', 'composite grid not a symmetric cube')
        K_m = br[-1] / float(ni['kpc_m'])
        w = np.asarray(waves, float)
        if w.ndim != 2 or w.shape[1] != 3 or float(np.max(np.abs(w))) > K_m:
            raise Refusal('UV_TAIL_KEPT_INVALID', 'stage waves outside the declared cube')
        if float(ni['kpc_m']) != float(self.lib.KPC_M):
            raise Refusal('UV_TAIL_UNITS', 'seed kpc_m differs from the library KPC_M')
        return K_m


    def _truncation(self):
        raw = getattr(self.args, 'uv_tail_truncation', None)
        if raw is None:
            return None
        tr = json.loads(raw)
        if not isinstance(tr, dict) or tr.get('shape') not in ('cube', 'sphere', 'cylinder'):
            raise Refusal('UV_TAIL_KEPT_INVALID', 'truncation ' + raw)
        return tr

    def _kept(self, waves, K_m, responses):
        tr = self._truncation() if self.kind in MASK_KINDS else None
        kept = self.lib.kept_region(self.kind, tr, K_m)
        # evidence on the stage's own packet: outside rows exactly zero, no all-zero row inside
        w = np.asarray(waves, float) * float(self.lib.KPC_M)
        if kept['shape'] == 'cube':
            inside = np.all(np.abs(w) <= kept['K_inverse_kpc'] * (1 + 1e-12), axis=1)
        elif kept['shape'] == 'sphere':
            inside = np.sqrt(np.sum(w * w, axis=1)) <= kept['K_inverse_kpc']
        else:
            inside = np.hypot(w[:, 0], w[:, 1]) <= kept['K_perp_inverse_kpc']
        flat = np.asarray(responses).reshape(len(w), -1)
        nonzero = np.any(flat != 0, axis=1)
        bad_out = int(np.count_nonzero(nonzero & ~inside)); zero_in = int(np.count_nonzero(~nonzero & inside))
        if bad_out or zero_in:
            raise Refusal('UV_TAIL_KEPT_REGION_EVIDENCE', '%s: %d nonzero rows outside, %d zero rows inside' % (kept, bad_out, zero_in))
        return kept, dict(truncation=tr, kept_nodes=int(inside.sum()), total_nodes=int(len(w)), outside_rows_nonzero=0, inside_rows_zero=0)

    def _admissible(self, state):
        if not state.record.get('production_admissible', False):
            if not self.test_only:
                raise Refusal('UV_TAIL_STATE_NOT_PRODUCTION_ADMISSIBLE', 'test-only certificate or synthetic roster (R1 IA6)')
            return False
        return True

    def _lineage(self, producers):
        """Each producer finish record that this stage reads (pinned bytes): tail OFF needs no enabled producer record; tail ON
        needs the same config sha, or (record absent) an EMPTY own state or the explicit test-only static-replay admission."""
        for name, fin in producers:
            rec = fin.get('uv_tail') if isinstance(fin, dict) else None
            if not self.enabled:
                if rec is not None and rec.get('enabled'):
                    raise Refusal('UV_TAIL_LINEAGE_MISMATCH', '%s carries a tail record but this stage is tail OFF' % name)
                continue
            if rec is None:
                if self.state is not None and self.state.empty:
                    self.lineage.append(dict(producer=name, status='PRODUCER_TAIL_ABSENT_ADMITTED_EMPTY_DOMAIN'))
                elif self.test_only:
                    self.lineage.append(dict(producer=name, status='PRODUCER_TAIL_ABSENT_ADMITTED_TEST_ONLY_STATIC_REPLAY'))
                else:
                    raise Refusal('UV_TAIL_LINEAGE_MISMATCH', '%s has no tail record (tail ON, non-empty domain)' % name)
            elif rec.get('config_sha256') != self.cfg['sha256']:
                raise Refusal('UV_TAIL_LINEAGE_MISMATCH', '%s config %s != %s' % (name, rec.get('config_sha256'), self.cfg['sha256']))
            else:
                self.lineage.append(dict(producer=name, status='SAME_CONFIG', state_digest=rec.get('state_digest')))

    def _i1t_parts(self, parts):
        verdicts = [p['verdict'] for p in parts]
        v = 'PASS' if all(x == 'PASS' for x in verdicts) else 'NOT_APPLICABLE_SYNTHETIC'
        return dict(verdict=v, parts=parts, rtol=I1T_RTOL, nodes=I1T_NODES, seed=I1T_SEED)

    def _sample(self, n):
        rng = np.random.default_rng(I1T_SEED)
        return np.sort(rng.choice(n, min(I1T_NODES, n), replace=False))

    def _stars(self, profile, galaxy, ni):
        self._galaxy(galaxy)
        path, pin = profile
        if _sha_file(path) != pin:
            raise Refusal('UV_TAIL_PIN_MISMATCH', str(path))
        prof = json.loads(Path(path).read_text())
        units = dict(kpc_m=float(ni['kpc_m']), solar_mass_kg=float(ni['solar_mass_kg']))
        extra, custody = ngc_h2_component()
        # R1 continuum source: same registered radial function, no GL4 tail-mass renormalization.
        stars = self.rs.stars_registered(prof, galaxy, units=units, extra_components=(extra,))
        rings = self.rs.stars_gl4_rings(prof, galaxy, kpc_m=units['kpc_m'], solar_mass_kg=units['solar_mass_kg'],
                                        gauss_order=ni['source_gauss_order'])
        # I1-T compares the represented *finite packet* to its independent replica.
        # Its H2 tail uses the prep's positive mass-normalized mapped GL rule.
        hrings, hstats = h2_packet_rings(extra, prof['galaxies'][galaxy]['stellar_reference']['height_kpc'],
                                        units, ni['source_gauss_order'], ni['h2_tail_mass_rtol'],
                                        stars._rs)
        rings = {key: np.concatenate((rings[key], hrings[key])) for key in ('R', 'z', 'm')}
        self.h2_custody = dict(custody, packet_replica=hstats,
                               continuum_rule='registered radial function; no finite-GL tail normalization',
                               packet_rule='NGC prep v001 L212-246; mass-normalized mapped-GL H2 tail; I1-T only')
        return prof, stars, rings


    def _base_record(self, kept, kept_evidence, i1t, extra=None):
        st = self.state
        q = st.record.get('quadrature')
        return dict(schema=RECORD_SCHEMA, stage_kind=self.kind, enabled=True, binding_sha256=_sha_file(__file__),
                    ngc_h2_custody=self.h2_custody,
                    ngc_outer_gas_cut_custody=self.ngc_outer_gas_cut_custody,
                    ngc_radial_count_custody=self.ngc_radial_count_custody,
                    library_pins={k: [str(p), s] for k, (p, s) in PINS.items()}, config_file_sha256=self.config_file_sha256,
                    config_sha256=self.cfg['sha256'], config=self.cfg, kept=kept, kept_evidence=kept_evidence,
                    outer=self.cfg['outer'], jet_order=self.cfg['jet_order']['route_b'], state_digest=st.digest, empty=st.empty,
                    roster_digest=st.record.get('roster_digest'), i1t=i1t,
                    production_admissible=bool(st.record.get('production_admissible', False)),
                    test_only_admitted=self.test_only and not bool(st.record.get('production_admissible', False)),
                    quadrature=None if q is None else {k: q[k] for k in ('order', 'N_perp', 'N_z_plus', 'phase_perp_rad', 'phase_z_rad',
                                                                       'w_perp_actual_inverse_kpc', 'w_z_actual_inverse_kpc')},
                    **(extra or {}))

    def _set_state(self, state):
        self.state = state
        self.tb = self.lib.TailBoundary(state, order=self.cfg['jet_order']['route_b'],
                                        tap=int(getattr(self.args, 'uv_tail_tap', 0) or 0))

    def _build(self, kept, roster, i1t, phys, radii):
        st = self.lib.build(config=self.cfg, kept=kept, roster=roster, gamma_eff=float(phys['gamma']), c_m_s=float(phys['c_m_s']),
                            eval_radii_m=np.asarray(radii, float), jn_provider=self.jn, i1t=i1t, stage_kind=self.kind)
        self._admissible(st)
        self._set_state(st)
        return st

    # ---------------------------------------------------------------- route-A manifest (reference, body, offset)
    def _manifest(self, identity, iteration, start, kept):
        path = getattr(self.args, 'route_a_tail_manifest', None); pin = getattr(self.args, 'route_a_tail_manifest_sha256', None)
        if path is None or not _hex64(pin):
            raise Refusal('UV_TAIL_ROUTE_A_MANIFEST_REQUIRED', self.kind)
        raw = Path(path).read_bytes()
        if hashlib.sha256(raw).hexdigest() != pin:
            raise Refusal('UV_TAIL_PIN_MISMATCH', str(path))
        man = json.loads(raw)
        if man.get('schema') != MANIFEST_SCHEMA:
            raise Refusal('UV_TAIL_ROUTE_A_MANIFEST_INVALID', 'schema')
        want = dict(identity_sha256=identity, accepted_iteration=iteration, iteration_start_payload_sha256=start['payload_sha256'])
        if man.get('route_a') != want:
            raise Refusal('UV_TAIL_ROUTE_A_MANIFEST_MISMATCH', 'route-A identity/iteration/start %s != %s' % (man.get('route_a'), want))
        if man.get('config_sha256') != self.cfg['sha256']:
            raise Refusal('UV_TAIL_ROUTE_A_MANIFEST_MISMATCH', 'config sha')
        s = man['state']
        if _sha_file(s['arrays']['path']) != s['arrays']['sha256']:
            raise Refusal('UV_TAIL_PIN_MISMATCH', s['arrays']['path'])
        with np.load(s['arrays']['path'], allow_pickle=False) as f:
            arrays = {k: f[k].copy() for k in f.files}
        st = self.lib.TailState.from_arrays(arrays, s['record'], jn_provider=self.jn, expected_digest=s['digest'])
        if st.record.get('config_sha256') != self.cfg['sha256'] or st.record.get('kept') != kept or st.record.get('stage_kind') != 'route_a':
            raise Refusal('UV_TAIL_ROUTE_A_MANIFEST_MISMATCH', 'state config/kept/stage_kind (%s, %s)' % (st.record.get('kept'), kept))
        if st.record.get('i1t') != man.get('i1t') or (man.get('i1t') or {}).get('verdict') not in ('PASS', 'NOT_APPLICABLE_SYNTHETIC'):
            raise Refusal('UV_TAIL_I1T_MISSING', 'route-A manifest')
        self._admissible(st)
        return man, st, dict(path=str(Path(path).resolve()), sha256=pin)

    def _manifest_gas_roster(self, man, ni):
        r = man.get('roster') or {}
        if r.get('kind') == 'registered_gas_columns':
            if _sha_file(r['arrays']['path']) != r['arrays']['sha256']:
                raise Refusal('UV_TAIL_PIN_MISMATCH', r['arrays']['path'])
            rec = r['record']
            with np.load(r['arrays']['path'], allow_pickle=False) as f:
                a = {k: f[k].copy() for k in f.files}
            n = len(a['gas_column_R_m'])
            gas = self.rs.GasColumns(s_edges_kpc2=rec['s_edges_kpc2'], kpc_m=float(ni['kpc_m']), M_s=rec['M_s'],
                                     column_R_m=a['gas_column_R_m'], column_rdr_m2=a['gas_column_rdr_m2'],
                                     present=a['gas_present'].astype(bool), elements_z=[a['gas_z_%03d' % i] for i in range(n)],
                                     elements_m=[a['gas_m_%03d' % i] for i in range(n)])
            if rec['M_s'] != self.cfg['gas']['M_s']:
                raise Refusal('UV_TAIL_ROUTE_A_MANIFEST_MISMATCH', 'gas M_s')
            return self.rs.Roster(stars=None, gas=gas, provenance=dict(rule='route_a_manifest_gas_IT')), False
        if r.get('kind') == 'synthetic_no_gas':
            if not self.test_only:
                raise Refusal('UV_TAIL_STATE_NOT_PRODUCTION_ADMISSIBLE', 'synthetic route-A roster')
            return None, True
        raise Refusal('UV_TAIL_ROUTE_A_MANIFEST_INVALID', 'roster kind %r' % r.get('kind'))

    # ---------------------------------------------------------------- per-kind binding
    def bind(self, *, ni, phys, galaxy, profile, identity, iteration, start, prepared=None, cm=None, cp=None,
             reference_start=None, reference_finish=None, body_finish=None, offset_finish=None, base=None,
             feedback_start=None, feedback_finish=None, column_manifest=None, radii=None, caller=None):
        self.ngc_outer_gas_cut_custody = ngc_cut_custody(ni, caller or {})
        self.ngc_radial_count_custody = ngc_effective_radial_layout(25*ni['source_gauss_order'],ni,caller or {},profile)
        if self.ngc_outer_gas_cut_custody is not None:self.ngc_outer_gas_cut_custody['profile_pin']={'path':str(profile[0]),'sha256':profile[1]}
        k = self.kind
        column_finishes = []
        if column_manifest is not None:
            for run in column_manifest['runs']:
                fp = Path(run['directory']) / 'finish.json'
                if _sha_file(fp) != run['finish_sha256']:
                    raise Refusal('UV_TAIL_PIN_MISMATCH', str(fp))
                column_finishes.append(('column_run ' + Path(run['directory']).parent.name, json.loads(fp.read_text())))
        if not self.enabled:
            # tail OFF: only the lineage refusal (no enabled producer record); nothing is computed or recorded
            prod = {'body': [('reference_start', reference_start), ('reference_finish', reference_finish)],
                    'offset': [('body_finish', body_finish)]}.get(k, [('offset_finish', offset_finish)] if k != 'reference' else [])
            self._lineage(prod + column_finishes)
            return self
        self._modules()
        cfg = self.cfg
        if cfg['source_rule'] != 'continuum_v001':
            raise Refusal('UV_TAIL_NODES_V001_NOT_BOUND_ROUTE_B_C2V001', 'T2 nodes_v001 route-B packet path not built')
        self._galaxy(galaxy)
        if float(phys['c_m_s']) <= 0 or float(phys['gamma']) <= 0:
            raise Refusal('UV_TAIL_PHYSICAL_INVALID')
        if k in ('reference', 'body'):
            K_m = self._grid_K(ni, prepared['wavevectors'])
            kept, ev = self._kept(prepared['wavevectors'], K_m, prepared['weighted_responses'])
            man, st, mref = self._manifest(identity, iteration, start, kept)
            self._set_state(st)
            extra = dict(route_a_manifest=mref, route_a_state_digest=st.digest)
            if k == 'body':
                rs_ = (reference_start or {}).get('uv_tail')
                if rs_ is not None and rs_.get('state_digest') != st.digest:
                    raise Refusal('UV_TAIL_REFERENCE_BODY_MISMATCH', 'reference state %s != body state %s (logN0 -> K0, CHECK F1)'
                                  % (rs_.get('state_digest'), st.digest))
                self._lineage([('reference_start', reference_start), ('reference_finish', reference_finish)])
            self.rec = self._base_record(kept, ev, man['i1t'], extra)
            return self
        if k == 'offset':
            # the offset's own state is built later (bind_offset), when the new body transform exists
            self._offset_pending = dict(ni=ni, phys=phys, galaxy=galaxy, profile=profile, identity=identity, iteration=iteration,
                                        start=start, body_finish=body_finish)
            return self
        # own-roster stages: fs (stars + body gas) or rfs/le (stars + the feedback's rotation rings)
        waves = prepared['wavevectors']
        K_m = self._grid_K(ni, waves)
        kept, ev = self._kept(waves, K_m, prepared['weighted_responses'])
        prof, stars, star_rings = self._stars(profile, galaxy, ni)
        s_edges = prof['galaxies'][galaxy]['HI_plus_He']['s_edges_kpc2']
        c = float(phys['c_m_s']); kpc = float(ni['kpc_m'])
        idx = self._sample(len(waves)); wv = np.asarray(waves)[idx]
        fixed = np.asarray(cm._get(str(cp), start['fixed_source_fourier_J']))[:, 0, 0][idx]
        starT = self.rs.packet_transform(star_rings, wv, 'prep_analytic_j0', c_m_s=c, j0=self.jn.j0)
        producers = [('offset_finish', offset_finish)]
        extra = {}
        if k in ('fs_columns', 'fs_rotation'):
            pos = np.asarray(base['physical_positions_m'], float).reshape(-1, 3)
            J = (-c * c * np.asarray(base['rho0']) * np.asarray(base['volume_weights_m3'])).reshape(-1)
            roster_gas = self.rs.roster_body({'physical_positions_m': pos, 'base_integrated_source_J': J}, stars,
                                             s_edges_kpc2=s_edges, kpc_m=kpc, M_s=cfg['gas']['M_s'], c_m_s=c)
            ref = offset_finish['outputs']['source_offset.npz']
            if _sha_file(ref['path']) != ref['sha256']:
                raise Refusal('UV_TAIL_PIN_MISMATCH', ref['path'])
            with np.load(ref['path'], allow_pickle=False) as f:
                newbody = f['new_body_fourier_J'][:, 0, 0][idx].copy()
            gasT = self.rs.packet_transform({'positions_m': pos, 'integrated_J': J}, wv, 'offset_cartesian_v003')
            i1t = self.rs.check_represented(starT + gasT, fixed + newbody, 'stars prep_analytic_j0 + body offset_cartesian_v003', rtol=I1T_RTOL)
            roster = roster_gas
            extra['source'] = dict(rule='stars_registered + body_gas (offset updated_base_arrays)', new_body=ref)
        else:
            d = getattr(self.args, 'uv_tail_source_rotation_directory', None)
            if d is None:
                raise Refusal('UV_TAIL_SOURCE_ROTATION_REQUIRED', k)
            d = Path(d)
            if _sha_file(d / 'finish.json') != feedback_start['rotation_finish_sha256']:
                raise Refusal('UV_TAIL_SOURCE_ROTATION_MISMATCH', 'finish sha != feedback start rotation_finish_sha256')
            rfin = json.loads((d / 'finish.json').read_text())
            if _sha_file(rfin['arrays_path']) != rfin['arrays_sha256']:
                raise Refusal('UV_TAIL_PIN_MISMATCH', rfin['arrays_path'])
            with np.load(rfin['arrays_path'], allow_pickle=False) as f:
                arr = {kk: f[kk].copy() for kk in ('rho0', 'volume_weights_m3', 'radial_nodes_m', 'z')}
            roster = self.rs.roster_rotation(arr, stars, s_edges_kpc2=s_edges, kpc_m=kpc, M_s=cfg['gas']['M_s'])
            m = np.sum(arr['volume_weights_m3'] * arr['rho0'], axis=1)
            Rg = np.repeat(arr['radial_nodes_m'], arr['z'].shape[2]); zg = arr['z'][:, 0, :].reshape(-1); mg = m.reshape(-1)
            gasT = self.rs.packet_transform(dict(R=Rg, z=zg, m=mg), wv, 'feedback_ring_j0_v004', c_m_s=c, j0=self.jn.j0)
            fb = feedback_finish['outputs']['gas_source_feedback.npz']
            if _sha_file(fb['path']) != fb['sha256']:
                raise Refusal('UV_TAIL_PIN_MISMATCH', fb['path'])
            with np.load(fb['path'], allow_pickle=False) as f:
                newgas = f['new_gas_fourier_J'][:, 0, 0][idx].copy()
            i1t = self.rs.check_represented(starT + gasT, fixed + newgas, 'stars prep_analytic_j0 + gas feedback_ring_j0', rtol=I1T_RTOL)
            producers.append(('source_rotation_finish', rfin))
            extra['source'] = dict(rule='stars_registered + feedback rings', source_rotation=dict(directory=str(d.resolve()),
                                   finish_sha256=feedback_start['rotation_finish_sha256']), feedback_worker_sha256=feedback_start['worker_sha256'],
                                   feedback_gas_packet=fb)
        i1t = dict(i1t, verdict=i1t['verdict'], nodes=int(len(idx)), seed=I1T_SEED)
        self._build(kept, roster, i1t, phys, radii)
        self._lineage(producers + column_finishes)
        self.rec = self._base_record(kept, ev, i1t, extra)
        return self

    def bind_offset(self, *, body, new, waves, unit_weighted_responses):
        """Offset t[Delta]: Delta = body gas - route-A gas_IT; C = the stage mask (evidence on the masked unit response)."""
        if not self.enabled:
            return self
        P = self._offset_pending
        if P is None:
            raise Refusal('UV_TAIL_STATE_NOT_BOUND', 'offset')
        ni, phys = P['ni'], P['phys']
        K_m = self._grid_K(ni, waves)
        kept, ev = self._kept(waves, K_m, unit_weighted_responses)
        K_cube = self.lib.kept_region('route_a', None, K_m)
        man, ra_state, mref = self._manifest(P['identity'], P['iteration'], P['start'], K_cube)
        prof, stars, _ = self._stars(P['profile'], P['galaxy'], ni)
        s_edges = prof['galaxies'][P['galaxy']]['HI_plus_He']['s_edges_kpc2']
        c = float(phys['c_m_s']); kpc = float(ni['kpc_m'])
        pos = np.asarray(body['physical_positions_m'], float).reshape(-1, 3)
        J = np.asarray(body['base_integrated_source_J'])[..., 0, 0].reshape(-1)
        body_r = self.rs.roster_body({'physical_positions_m': pos, 'base_integrated_source_J': J}, None,
                                     s_edges_kpc2=s_edges, kpc_m=kpc, M_s=self.cfg['gas']['M_s'], c_m_s=c)
        idx = self._sample(len(waves)); wv = np.asarray(waves)[idx]
        gasT = self.rs.packet_transform({'positions_m': pos, 'integrated_J': J}, wv, 'offset_cartesian_v003')
        part_body = self.rs.check_represented(gasT, np.asarray(new)[:, 0, 0][idx], 'body offset_cartesian_v003', rtol=I1T_RTOL)
        ra_roster, synthetic = self._manifest_gas_roster(man, ni)
        part_ra = dict(man['i1t'], kind='route_a manifest (gas_IT)')
        i1t = self._i1t_parts([part_body, part_ra])
        roster = _DifferenceRoster(body_r, ra_roster, synthetic or i1t['verdict'] != 'PASS')
        self._build(kept, roster, i1t, phys, np.unique(np.asarray(body['radial_nodes_m'], float)))
        bf = P['body_finish']
        brec = bf.get('uv_tail') if isinstance(bf, dict) else None
        if brec is not None and brec.get('state_digest') != ra_state.digest:
            raise Refusal('UV_TAIL_LINEAGE_MISMATCH', 'body state %s != route-A manifest state %s' % (brec.get('state_digest'), ra_state.digest))
        self._lineage([('body_finish', bf)])
        self.rec = self._base_record(kept, ev, i1t, dict(route_a_manifest=mref, route_a_state_digest=ra_state.digest,
                                                         source=dict(rule='offset Delta = body gas - route-A gas_IT (stars cancel)')))
        return self



# NGC fixed source custody: these are target-free baryonic source records already
# owned by the NGC prep. The stage takes its stellar/HI profile from per-call custody.
H2_REDUCTION = (Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NGC3198_H2_SOURCE_TAIL_REDUCTION_RUN_V001/stdout.txt'),
                '157ede0487beed6658a413ae4db34cae2e819efc58efd292ccc56794ae5917d2')


def ngc_h2_component():
    from fractions import Fraction
    path, sha = H2_REDUCTION
    if _sha_file(path) != sha:
        raise Refusal('UV_TAIL_H2_REDUCTION_PIN', str(path))
    reduction = json.loads(path.read_bytes())
    source = reduction['source']
    if _sha_file(source['path']) != source['sha256']:
        raise Refusal('UV_TAIL_H2_SOURCE_PIN', source['path'])
    rows = json.loads(Path(source['path']).read_bytes())['S1_alternative_and_stellar_median_rows']['rows'][:10]
    if len(rows) != 10 or any(r['conventions']['gas_helium']['value'] != 'ALREADY_INCLUDED' for r in rows):
        raise Refusal('UV_TAIL_H2_HELIUM_OR_ROSTER')
    component = dict(name='H2', radius_kpc=[float(Fraction(r['radius_kpc_literal']['value'])) for r in rows],
                     surface_density_Msun_pc2=[float(Fraction(r['components']['H2']['value_literal']['value'])) for r in rows],
                     outer_scale_kpc=float(reduction['outer_scale_kpc']))
    return component, dict(reduction=dict(path=str(path), sha256=sha), source=source)


def h2_packet_rings(component, height_kpc, units, gauss_order, tail_mass_rtol, radial_surface):
    """Independent replica of the prep's finite H2 packet, never the continuum tail rule."""
    if type(gauss_order) is not int or gauss_order < 1 or not math.isfinite(tail_mass_rtol) or tail_mass_rtol <= 0:
        raise Refusal('UV_TAIL_H2_PACKET_NUMERICS')
    hr = component['radius_kpc']; hs = component['surface_density_Msun_pc2']
    hrd = float(component['outer_scale_kpc']); height = float(height_kpc)
    kpc = units['kpc_m']; sigma_unit = units['solar_mass_kg'] / (kpc / 1000)**2
    gx, gw = np.polynomial.legendre.leggauss(gauss_order)
    gauss = [(float(x), float(w)) for x, w in zip(gx, gw)]
    radial = []
    for lo, hi in zip([0.] + hr, hr):
        for x, w in gauss:
            r = (lo + hi) / 2 + (hi - lo) * x / 2; dr = (hi - lo) * w / 2
            sigma = radial_surface(r, hr, hs, outer_scale=hrd)
            radial.append((r, 2 * math.pi * sigma * sigma_unit * (r * kpc) * (dr * kpc)))
    last = hr[-1]
    exact = 2 * math.pi * hs[-1] * sigma_unit * kpc * kpc * hrd * (last + hrd)
    tail = []
    for x, w in gauss:
        u = (x + 1) / 2; r = last - hrd * math.log(u)
        mass = 2 * math.pi * hs[-1] * sigma_unit * kpc * kpc * hrd * r * w / 2
        tail.append((r, mass))
    raw = math.fsum(m for _, m in tail); factor = exact / raw
    if not all(math.isfinite(v) and v > 0 for v in (hrd, exact, raw, factor)):
        raise Refusal('UV_TAIL_H2_PACKET_TAIL_MASS')
    normalized = [(r, m * factor) for r, m in tail]
    actual = math.fsum(m for _, m in normalized)
    error = abs(actual - exact) / exact
    if error > tail_mass_rtol:
        raise Refusal('UV_TAIL_H2_PACKET_TAIL_TOLERANCE')
    radial.extend(normalized)
    R, z, m = [], [], []
    for r, mass in radial:
        for u, w in gauss:
            R.append(r * kpc); z.append(2 * height * kpc * math.atanh(u)); m.append(mass * w / 2)
    return dict(R=np.asarray(R), z=np.asarray(z), m=np.asarray(m)), dict(
        tail_mass_exact_kg=exact, tail_mass_quadrature_kg=actual, tail_mass_relative_error=error,
        mapped_GL_raw_mass_kg=raw, mapped_GL_mass_normalization=factor)


def apply_ngc_outer_cut(roster, ni, caller, digest):
    """Reference's reconstructed roster uses the shared, checkpoint-bound cut."""
    pin = ni.get('ngc_outer_gas_cut')
    bound = (caller.get('numerical_controls') or {}).get('ngc_outer_gas_cut')
    if pin != bound:
        raise Refusal('NGC_OUTER_CUT_CUSTODY_MISMATCH', 'seed and checkpoint numerical_controls differ')
    if pin is None:
        return roster
    helper = _load('grid_cut')
    kept, record = helper.apply_cut(roster, pin, float(ni['kpc_m']), controls=ni)
    if digest(kept) != record['kept_roster_digest']:
        raise Refusal('NGC_OUTER_CUT_CHECKPOINT_DIGEST_MISMATCH')
    return kept


def ngc_cut_record(ni, caller):
    pin = ni.get('ngc_outer_gas_cut')
    if pin != (caller.get('numerical_controls') or {}).get('ngc_outer_gas_cut'):
        raise Refusal('NGC_OUTER_CUT_CUSTODY_MISMATCH')
    if pin is None:
        return None
    if not isinstance(pin, dict) or set(pin) != {'path', 'sha256'} or _sha_file(pin['path']) != pin['sha256']:
        raise Refusal('NGC_OUTER_CUT_PIN_MISMATCH')
    rec = json.loads(Path(pin['path']).read_bytes())
    if rec.get('confinement_status') != 'CERTIFIED_UNCONFINED' or type(rec.get('classification_evidence')) is not dict or not rec['classification_evidence']:
        raise Refusal('NGC_OUTER_CUT_CERTIFICATE_INVALID')
    cut = rec.get('first_unconfined_R_kpc')
    if rec.get('schema') != 'NGC_CANDIDATE_ROSTER_CUT_CX3V001' or type(cut) not in (float, int) or not math.isfinite(cut) or cut <= 0:
        raise Refusal('NGC_OUTER_CUT_RECORD_INVALID')
    if rec.get('controls_sha256') != _load('grid_cut').controls_digest(ni):
        raise Refusal('NGC_OUTER_CUT_CONTROLS_MISMATCH')
    return rec


def ngc_radial_domain_upper(original_upper_m, ni, caller):
    rec = ngc_cut_record(ni, caller)
    return original_upper_m if rec is None else min(original_upper_m, rec['first_unconfined_R_kpc'] * ni['kpc_m'])


def ngc_filter_radial_nodes(R, weights, ni, caller):
    rec = ngc_cut_record(ni, caller)
    if rec is None:
        return R, weights
    if len(R) != len(weights):
        raise Refusal('NGC_OUTER_CUT_RADIAL_WEIGHT_SHAPE')
    cut_m = rec['first_unconfined_R_kpc'] * ni['kpc_m']
    selected = [(r, w) for r, w in zip(R, weights) if r < cut_m]
    if not selected:
        raise Refusal('NGC_OUTER_CUT_NO_ROUTE_B_RADIAL_NODES')
    return [r for r, w in selected], [w for r, w in selected]

def open_binding(a, kind, galaxy_config_path=None, galaxy_config_sha256=None):
    """Read and normalize the uv_tail config (bytes pinned by --uv-tail-config-sha256). Disabled -> a Binding whose accessors
    return the reviewed zeros; the absence of every tail-only argument is then required."""
    if kind not in KINDS:
        raise Refusal('UV_TAIL_STAGE_KIND', repr(kind))
    pin = a.uv_tail_config_sha256
    if not _hex64(pin):
        raise Refusal('UV_TAIL_CONFIG_INVALID', '--uv-tail-config-sha256 must be 64 lowercase hex')
    raw = Path(a.uv_tail_config).read_bytes()
    if hashlib.sha256(raw).hexdigest() != pin:
        raise Refusal('UV_TAIL_PIN_MISMATCH', str(a.uv_tail_config))
    lib = _load('lib')
    cfg = lib.normalize_config(json.loads(raw))
    b = Binding(a, kind, cfg, pin)
    if not b.enabled:
        extra = [n for n in ('route_a_tail_manifest', 'route_a_tail_manifest_sha256', 'uv_tail_source_rotation_directory', 'uv_tail_truncation')
                 if getattr(a, n, None) is not None]
        if extra or getattr(a, 'uv_tail_tap', 0) or b.test_only:
            raise Refusal('UV_TAIL_ARGV_WITH_TAIL_OFF', ','.join(extra) or 'tap/test-only flag')
    else:
        b.lib = lib
        b._modules()
    return b

def ngc_cut_custody(ni, caller):
    rec = ngc_cut_record(ni, caller)
    if rec is None:
        return None
    seed = caller.get('seed') or {}
    seed_sha = seed.get('sha256')
    if type(seed_sha) is not str or len(seed_sha) != 64 or any(c not in '0123456789abcdef' for c in seed_sha):
        raise Refusal('NGC_OUTER_CUT_SEED_CUSTODY')
    kpc_m = ni.get('kpc_m')
    if type(kpc_m) not in (float, int) or not math.isfinite(kpc_m) or kpc_m <= 0:
        raise Refusal('NGC_OUTER_CUT_UNITS')
    return dict(pin=ni['ngc_outer_gas_cut'], record=rec, seed_sha256=seed_sha, seed_pin=dict(seed),
                kpc_m=kpc_m, first_unconfined_R_m=rec['first_unconfined_R_kpc'] * kpc_m)


def ngc_surviving_radial_count(original_radial_nodes_m, ni, caller):
    """Count original source-prefix GL nodes below the cut. No targets or reweighting."""
    nodes, _ = ngc_filter_radial_nodes(original_radial_nodes_m, [1.] * len(original_radial_nodes_m), ni, caller)
    return len(nodes)


def ngc_effective_radial_layout(registered_n_columns, ni, caller, profile):
    """Keep full schema admission; derive a smaller count from the pinned cut only."""
    order=ni['source_gauss_order']
    if (order,registered_n_columns) not in ((4,100),(10,250)):
        raise Refusal('NGC_REGISTERED_FULL_COUNT_MISMATCH')
    rec=ngc_cut_record(ni,caller)
    if rec is None:
        return dict(registered_n_columns=registered_n_columns,effective_n_columns=registered_n_columns,cut=None,expected_radii_m=None)
    path,sha=profile
    if _sha_file(path)!=sha:raise Refusal('NGC_RADIAL_PROFILE_PIN')
    gas=json.loads(Path(path).read_bytes())['galaxies']['NGC3198']['HI_plus_He']
    edges=gas['s_edges_kpc2'];means=gas['annular_means_Msun_pc2'];controls=gas['boundary_controls_Msun_pc2']
    gx,gw=np.polynomial.legendre.leggauss(order);kpc=ni['kpc_m'];R=[]
    kernel=_load('radial_kernel')
    for lo,hi in zip(edges[:-1],edges[1:]):
        for x,w in zip(gx,gw):
            r=float(np.sqrt((lo+hi)/2+(hi-lo)*x/2)*kpc)
            ans=kernel.annular_bernstein_sigma(s_edges=edges,annular_means=means,boundary_controls=controls,s_query=[float((r/kpc)**2)])
            if not ans['ok']:raise Refusal('NGC_RADIAL_PROFILE_KERNEL')
            if float(ans['sigma'][0])!=0:R.append(r)
    # The registered N2 source domain is the original 25-annulus positive prefix.
    # Full count remains 100/250; changing it in galaxy config remains refused.
    full=R[:registered_n_columns]
    if len(full)!=registered_n_columns:raise Refusal('NGC_FULL_RADIAL_PREFIX_MISSING')
    kept,_=ngc_filter_radial_nodes(full,[1.]*len(full),ni,caller)
    return dict(registered_n_columns=registered_n_columns,effective_n_columns=len(kept),cut=ni['ngc_outer_gas_cut'],expected_radii_m=kept)


def ngc_effective_n_columns(registered_n_columns, ni, caller, profile, radii=None):
    layout=ngc_effective_radial_layout(registered_n_columns,ni,caller,profile)
    if radii is not None:
        arr=np.asarray(radii,float)
        if arr.shape!=(layout['effective_n_columns'],) or not np.isfinite(arr).all():raise Refusal('NGC_EFFECTIVE_RADIAL_SHAPE')
        if layout['expected_radii_m'] is not None and not np.array_equal(arr,np.asarray(layout['expected_radii_m'])):raise Refusal('NGC_EFFECTIVE_RADIAL_ROSTER')
    return layout['effective_n_columns']


def ngc_offset_grid(ni):
    if ni.get('composite_grid_spec_anisotropic') is not None:
        if ni.get('composite_grid_spec') is not None:raise Refusal('NGC_AMBIGUOUS_GRID')
        return _load('grid_cut').tensor_grid(ni['composite_grid_spec_anisotropic'],ni['kpc_m'],ni['kmax_inverse_kpc'])
    spec=ni['composite_grid_spec'];axis=[];aw=[]
    for lo,hi,n in zip(spec['breaks_inverse_kpc'][:-1],spec['breaks_inverse_kpc'][1:],spec['panel_orders']):
        x,w=np.polynomial.legendre.leggauss(n);axis.extend(((lo+hi)/2+(hi-lo)*x/2)/ni['kpc_m']);aw.extend((hi-lo)*w/(2*ni['kpc_m']))
    return np.array([(x,y,z) for x in axis for y in axis for z in axis]),np.array([x*y*z for x in aw for y in aw for z in aw])

