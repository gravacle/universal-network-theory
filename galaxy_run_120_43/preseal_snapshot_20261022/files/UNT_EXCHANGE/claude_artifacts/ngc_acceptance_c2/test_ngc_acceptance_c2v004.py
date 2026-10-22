"""Synthetic suite for NGC acceptance c2v004 (V006 A177): the NGC roster recipes ngc_roster_recipes_c2v001 (route A, route B)
through the S5 rebuild-export tool c2v003, the handoff c2v004 (the recipe module as the approved-recipe source), the two
verifier-note-3 MUST_FAIL tests, and every c2v003a test ported (the c2v003a suite file is loaded by exact sha and run
against the c2v004 handoff; its fixture and intent are unchanged).

SYNTHETIC ONLY. The recipe fixture (RFx) builds each call the way the driver does, with the named code itself:
  - the route-A sidecar is written by the REAL route-A controller c5bdd055 (from_prepared, open, begin_iteration,
    complete_iteration, result_record), driven by a synthetic prep, a synthetic roster module and the pinned library v002
    (2026f2b6) and provider (d6c55b55): every recorded route-A state digest is the real build's;
  - the ROUTE_A_TAIL_MANIFEST is written by the REAL manifest writer b9247b1a functions (rebuild_state, write_outputs);
  - every route-B stage state is built by the REAL route-B binding aee7af12 (Binding.bind / bind_offset / record) with the
    synthetic roster module and a synthetic H2 component (the registered H2 source is NGC3198-named: never opened);
  - the checkpoint is written in the form the driver reads (IDENTITY / iteration_NNNN START, COMPLETED; driver L7024-7038)
    through a synthetic checkpoint module exposing the two entries the writer uses (_read, _get).
Test-only stand-ins (written into the run dir, loaded by exact sha): the roster module, prep, checkpoint module, the
recipe toolkit and an S5 recipe wrapper that calls the real recipe module's recipe_for_state with that toolkit.

HARD-RULE GUARD. An audit hook refuses (PermissionError) every open of an NGC3198-named path (the V006 addendum included:
it is read only by awk, outside this suite) and of every non-named code path (the roster module 4366e3d6, the checkpoint
module 069b3935, the solvers, the prep 8681da84, the route-B stage scripts). A test that triggers a refused open is
recorded BLOCKED_BY_HARD_RULE (neither pass nor fail; its refused paths listed). The recipe tests require zero refused opens.

Usage: python3 -I -B test_ngc_acceptance_c2v004.py --run-dir <new dir> [--module-dir <dir>]
Writes SUITE_RESULTS_C2V004.json (exclusive create). Exit 0 iff every run MUST_PASS passes and every run MUST_FAIL fails
closed (BLOCKED tests are listed, not counted).
"""
import argparse
import copy
import hashlib
import importlib.util
import io
import json
import math
import os
import sys
import time
import traceback
import types

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
KPC_M = 3.085677581491367e19
C_M_S = 299792458.0
PREV_SUITE = ('test_ngc_acceptance_c2v003a.py', 'e452cec252aeb54c64723c5fc324409bb6e308b0b27f01f3bd43cebeab3a11c0')
HANDOFF_NAME = 'ngc_acceptance_handoff_c2v004.py'
RECIPES_NAME = 'ngc_roster_recipes_c2v001.py'
DRIVER = (ART + '/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py',
          '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377')
MW_PATH = ART + '/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/ngc_route_a_tail_manifest_cx3v011_r5cx3v001_cx3v005.py'
BB_PATH = ART + '/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_uvt_route_b_binding_cx3v006_r5cx3v001_cx3v005.py'
CTL_PATH = ART + '/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_a/route_a_uv_tail_controller_c2v001_r5.py'
CURRENT = 'current_begin_inferred_from_completion'
NEXT = 'next_built_and_monitor_consumed'
CONV = 'CONVERGED_FINITE_FIXED_POINT'

# ---------------------------------------------------------------------------------------------------------------- guard
DENY_PREFIXES = (ART + '/tail_scheme_impl_c2/module/', ART + '/resumable_coupled_gas_0422/', ART + '/ngc_route_tail_readiness_cx3/',
                 ART + '/tail_scheme_impl_c2/driver_r5/cascade/', ART + '/tail_scheme_impl_c2/route_a/',
                 ART + '/tail_scheme_impl_c2/route_b/', ART + '/ngc_route_a_freeboundary_c2/')
DENY_ALLOW = {MW_PATH, BB_PATH, CTL_PATH}
GUARD = {'blocked': [], 'log': None}


def _forbidden(path):
    r = os.path.realpath(path)
    if 'ngc3198' in r.casefold():
        return True
    return any(r.startswith(p) for p in DENY_PREFIXES) and r not in DENY_ALLOW


def _audit(event, args):
    if event != 'open' or not args or isinstance(args[0], int):
        return
    try:
        p = os.fsdecode(args[0])
    except (TypeError, ValueError):
        return
    p = p if os.path.isabs(p) else os.path.abspath(p)
    if GUARD['log'] is not None:
        GUARD['log'].append(p)
    if _forbidden(p):
        GUARD['blocked'].append(p)
        raise PermissionError('HARD_RULE_BLOCKED_OPEN %s' % p)


# ---------------------------------------------------------------------------------------------------------------- helpers
def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha_file(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def load(path, name, sha=None):
    with open(path, 'rb') as f:
        raw = f.read()
    if sha is not None:
        assert sha_bytes(raw) == sha, 'PIN %s' % path
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


def put_bytes(path, raw):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)
    return {'path': path, 'sha256': sha_bytes(raw)}


def put_json(path, obj):
    return put_bytes(path, (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode())


def npz_raw(arrays):
    import numpy as np
    buf = io.BytesIO()
    np.savez(buf, **arrays)
    return buf.getvalue()


def put_npz(path, arrays):
    return put_bytes(path, npz_raw(arrays))


def read_json(pin):
    with open(pin['path'] if isinstance(pin, dict) else pin, 'rb') as f:
        return json.loads(f.read())


def plain(o):
    import numpy as np
    if isinstance(o, dict):
        return {str(k): plain(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [plain(v) for v in o]
    if isinstance(o, np.ndarray):
        return plain(o.tolist())
    if isinstance(o, np.generic):
        return o.item()
    return o


# ---------------------------------------------------------------------------------------------------------------- stand-ins
SYN_ROSTER_SRC = r'''"""SYNTHETIC roster module (TEST ONLY; NGC acceptance c2v004 suite). Stands in for uv_tail_source_roster_c2v001
(4366e3d6), which is not a named path under the A177 commission. Call signatures are the ones the route-A controller and
the route-B binding use (controller L250, L378-388, L396-397; binding L334-341, L407-422, L485-499, L514-517, L551-555);
the arithmetic is synthetic, deterministic and content-addressed (digest = sha256 of the canonical record)."""
import hashlib
import json
import math
import numpy as np

KPC_M = 3.085677581491367e19
R1 = 0.01 * KPC_M
H1 = 0.002 * KPC_M


def _canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _sha(o):
    return hashlib.sha256(_canon(o).encode()).hexdigest()


def _adig(a):
    a = np.ascontiguousarray(a)
    h = hashlib.sha256()
    h.update(('%s|%s|' % (a.dtype.str, a.shape)).encode())
    h.update(a.tobytes())
    return h.hexdigest()


class SynStars:
    def __init__(self, profile, galaxy, units, extra):
        g = profile['galaxies'][galaxy]
        self.mass = float(g['stellar_reference']['mass_kg'])
        self._rec = {'kind': 'synthetic_stars', 'galaxy': galaxy, 'profile_sha256': _sha(g),
                     'units': {k: float(v).hex() for k, v in sorted(units.items())}, 'extra_sha256': [_sha(e) for e in extra]}
        self.certificates = []

    def record(self):
        return dict(self._rec)

    @staticmethod
    def _rs(r, hr, hs, outer_scale=None):
        if r <= hr[-1]:
            return float(np.interp(r, [0.0] + list(hr), [hs[0]] + list(hs)))
        return float(hs[-1] * math.exp(-(r - hr[-1]) / outer_scale))


def stars_registered(profile, galaxy, units=None, extra_components=()):
    return SynStars(profile, galaxy, dict(units or {}), list(extra_components))


def stars_gl4_rings(profile, galaxy, kpc_m, solar_mass_kg, gauss_order):
    mk = float(profile['galaxies'][galaxy]['stellar_reference']['mass_kg'])
    return {'R': np.array([0.01, 0.03, 0.05]) * kpc_m, 'z': np.zeros(3), 'm': np.array([1.0, 2.0, 1.5]) * mk / 4.5}


class GasColumns:
    def __init__(self, *, s_edges_kpc2, kpc_m, M_s, column_R_m, column_rdr_m2, present, elements_z, elements_m):
        self.s_edges = [float(x) for x in s_edges_kpc2]
        self.kpc_m = float(kpc_m)
        self.M_s = int(M_s)
        self.column_R_m = np.asarray(column_R_m, float)
        self.column_rdr_m2 = np.asarray(column_rdr_m2, float)
        self.present = np.asarray(present, dtype=bool)
        self.elements_z = [np.asarray(z, float) for z in elements_z]
        self.elements_m = [np.asarray(m, float) for m in elements_m]

    def arrays(self):
        out = {'gas_column_R_m': self.column_R_m, 'gas_column_rdr_m2': self.column_rdr_m2, 'gas_present': self.present}
        for i, (z, m) in enumerate(zip(self.elements_z, self.elements_m)):
            out['gas_z_%03d' % i] = z
            out['gas_m_%03d' % i] = m
        return out

    def record(self):
        a = self.arrays()
        return {'kind': 'synthetic_gas_columns', 's_edges_kpc2': list(self.s_edges), 'M_s': self.M_s,
                'kpc_m_hex': self.kpc_m.hex(), 'n_columns': int(len(self.column_R_m)),
                'arrays_sha256': _sha({k: _adig(a[k]) for k in sorted(a)})}

    def total(self):
        return float(sum(float(np.sum(m)) for m in self.elements_m))


def _columns(R, z, m, s_edges, kpc_m, M_s):
    R = np.asarray(R, float).reshape(-1)
    z = np.asarray(z, float).reshape(-1)
    m = np.asarray(m, float).reshape(-1)
    return GasColumns(s_edges_kpc2=s_edges, kpc_m=kpc_m, M_s=M_s, column_R_m=R, column_rdr_m2=R * R * 0.01,
                      present=np.ones(len(R), bool), elements_z=[np.array([v]) for v in z], elements_m=[np.array([v]) for v in m])


class Roster:
    kind = 'registered'

    def __init__(self, stars=None, gas=None, provenance=None):
        self.stars = stars
        self.gas = gas
        self.provenance = dict(provenance or {})

    def extent(self):
        return {'R_src_max_m': 0.05 * KPC_M, 'gas_z_abs_max_m': 0.01 * KPC_M, 'stars_24h_m': 0.02 * KPC_M}

    def _amps(self):
        out = []
        if self.gas is not None:
            out.append(1.0e-3 * (1.0 + 0.5 * math.tanh(self.gas.total() / 1.0e33)))
        if self.stars is not None:
            out.append(0.5e-3)
        return out or [1.0e-3]

    def radial_factors(self, k, j0):
        k = np.asarray(k, float)
        return np.stack([a * j0(k * R1 * (i + 1)) for i, a in enumerate(self._amps())], axis=1)

    def vertical_factors(self, kz, c):
        kz = np.asarray(kz, float)
        return np.stack([1.0 / (1.0 + (kz * H1 * (i + 1)) ** 2) + 0j for i in range(len(self._amps()))], axis=1)

    def record(self):
        return {'kind': 'synthetic_roster', 'stars': None if self.stars is None else self.stars.record(),
                'gas': None if self.gas is None else self.gas.record(), 'provenance': self.provenance}

    def digest(self):
        return _sha(self.record())


def roster_route_a(stars, init_rings, elements, relaxation, *, s_edges_kpc2, kpc_m, M_s, c_m_s):
    r = float(relaxation)
    coeff = [1.0]
    for _ in range(len(elements)):
        coeff = [(1 - r) * c for c in coeff] + [r]
    R = list(np.asarray(init_rings['R'], float))
    z = list(np.asarray(init_rings['z'], float))
    m = list(coeff[0] * np.asarray(init_rings['m'], float))
    for c, e in zip(coeff[1:], elements):
        p = np.asarray(e['positions_m'], float).reshape(-1, 3)
        R += list(np.hypot(p[:, 0], p[:, 1]))
        z += list(p[:, 2])
        m += list(c * np.asarray(e['integrated_J'], float) / (c_m_s * c_m_s))
    return Roster(stars, _columns(R, z, m, s_edges_kpc2, kpc_m, M_s),
                  {'rule': 'synthetic_route_a', 'iterations': len(elements), 'relaxation_hex': r.hex()})


def roster_body(body, stars, *, s_edges_kpc2, kpc_m, M_s, c_m_s):
    p = np.asarray(body['physical_positions_m'], float).reshape(-1, 3)
    J = np.asarray(body['base_integrated_source_J'], float).reshape(-1)
    return Roster(stars, _columns(np.hypot(p[:, 0], p[:, 1]), p[:, 2], -J / (c_m_s * c_m_s), s_edges_kpc2, kpc_m, M_s),
                  {'rule': 'synthetic_body'})


def roster_rotation(arr, stars, *, s_edges_kpc2, kpc_m, M_s):
    m = np.sum(arr['volume_weights_m3'] * arr['rho0'], axis=1)
    R = np.repeat(arr['radial_nodes_m'], arr['z'].shape[2])
    return Roster(stars, _columns(R, arr['z'][:, 0, :].reshape(-1), m.reshape(-1), s_edges_kpc2, kpc_m, M_s),
                  {'rule': 'synthetic_rotation'})


def ring_transform(R, z, m, k, c, j0):
    k = np.asarray(k, float).reshape(-1, 3)
    kp = np.hypot(k[:, 0], k[:, 1])
    A = j0(np.outer(kp, np.asarray(R, float))) * np.cos(np.outer(k[:, 2], np.asarray(z, float)))
    return A @ np.asarray(m, float)


def point_transform(pos, J, k):
    k = np.asarray(k, float).reshape(-1, 3)
    return np.cos(k @ np.asarray(pos, float).reshape(-1, 3).T) @ np.asarray(J, float).reshape(-1)


def packet_transform(obj, wv, rule, c_m_s=None, j0=None):
    if rule in ('prep_analytic_j0', 'feedback_ring_j0_v004'):
        return ring_transform(obj['R'], obj['z'], obj['m'], wv, c_m_s, j0)
    if rule == 'offset_cartesian_v003':
        return point_transform(obj['positions_m'], obj['integrated_J'], wv)
    raise ValueError('SYNTHETIC_PACKET_RULE ' + str(rule))


def check_represented(T, target, label, rtol=1e-12):
    T = np.asarray(T)
    t = np.asarray(target)
    scale = float(np.max(np.abs(t))) if t.size else 0.0
    diff = float(np.max(np.abs(T - t))) if t.size else 0.0
    rel = diff / scale if scale > 0 else (0.0 if diff == 0 else math.inf)
    if not rel <= rtol:
        raise ValueError('UV_TAIL_SOURCE_MISMATCH %s max_rel %r > %r' % (label, rel, rtol))
    return {'verdict': 'PASS', 'label': label, 'max_rel': rel, 'rtol': float(rtol), 'n': int(t.size)}
'''

SYN_CHECKPOINT_SRC = r'''"""SYNTHETIC checkpoint module (TEST ONLY; NGC acceptance c2v004 suite) standing in for coupled_gas_checkpoint_c2v003
(069b3935, not a named path): only the two entries the manifest writer, the binding and the recipe use, _read(path, kind)
and _get(directory, ref) (MW L214-221; BB L484)."""
import hashlib
import io
import json
import os
import numpy as np


def _read(path, kind):
    with open(path, 'rb') as f:
        rec = json.loads(f.read())
    if not isinstance(rec, dict) or rec.get('kind') != kind:
        raise ValueError('SYNTHETIC_CHECKPOINT_KIND %s %r' % (path, kind))
    return rec


def _get(directory, ref):
    with open(os.path.join(directory, ref['file']), 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != ref['array_sha256']:
        raise ValueError('SYNTHETIC_CHECKPOINT_ARRAY_SHA ' + ref['file'])
    return np.load(io.BytesIO(raw), allow_pickle=False)
'''

SYN_PREP_TEMPLATE = r'''"""SYNTHETIC reviewed-prep stand-in (TEST ONLY; NGC acceptance c2v004 suite) for the NGC prep 8681da84 (the manifest
writer's LOCAL['prep'], not a named path). prepare_inputs(**numerical_inputs) returns the keys
RouteATailController.from_prepared reads (controller L219-284). COEFFICIENT / COEFFICIENT_SHA are the globals the driver's
prep patch sets (driver L1020-1028); the patched sha scales the gas columns, so a dropped patch changes the static identity."""
import hashlib
import math
import os

C = %(C)r
H2_SOURCE = %(H2)r
COEFFICIENT = None
COEFFICIENT_SHA = None
PROFILE_NAME = 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json'
COLUMN_R_KPC = [0.01, 0.02, 0.035, 0.05, 0.065, 0.08]


def _sha(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def prepare_inputs(**ni):
    kpc = ni['kpc_m']
    scale = 1.0 if COEFFICIENT_SHA is None else 1.0 + int(str(COEFFICIENT_SHA)[:6], 16) / 2.0 ** 30
    cols = []
    for phi in (0.0, 0.5 * math.pi):
        for i, r in enumerate(COLUMN_R_KPC):
            cols.append({'phi': phi, 'R_m': r * kpc, 'Sigma_kg_m2': 1.0e-3 * (1.0 + 0.1 * i) * scale,
                         'radial_weight_m': 0.01 * kpc})
    a = [-0.875, -0.375, 0.375, 0.875]
    K = ni['kmax_inverse_kpc'] / kpc
    k = [[x * K, y * K, z * K] for x in a for y in a for z in a]
    ppath = os.path.join(C, PROFILE_NAME)
    return {'source_pins': {ppath: _sha(ppath)},
            'H2_custody': {'reduction': {'source': {'path': H2_SOURCE, 'sha256': _sha(H2_SOURCE)}, 'outer_scale_kpc': 0.02}},
            'gas_columns': cols, 'queries': [{'radius_kpc': 0.05}],
            'fourier_arguments': {'k_physical': k, 'gamma': ni['gamma']}, 'c_m_s': 299792458.0}
'''

SYN_TOOLKIT_TEMPLATE = r'''"""SYNTHETIC recipe toolkit (TEST ONLY; NGC acceptance c2v004 suite) for ngc_roster_recipes_c2v001.recipe_for_state: the
production toolkit with exactly these substitutions: the synthetic call driver sha; the synthetic prep in place of the
writer's LOCAL['prep']; the synthetic checkpoint module sha; the synthetic roster module handed to the controller and the
binding; a synthetic binding H2 component (the registered source is NGC3198-named and never opened)."""
import hashlib
import importlib.util

DRIVER_SHA256 = %(driver)r
PREP = %(prep)r
CHECKPOINT_SHA256 = %(cm)r
ROSTER = %(roster)r
LIBRARY = %(lib)r
PROVIDER = %(provider)r
H2 = %(h2)r


def _load(path, sha, name):
    with open(path, 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != sha:
        raise ValueError('SYNTHETIC_TOOLKIT_PIN ' + path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


class SyntheticToolkit:
    kind = 'SYNTHETIC_TEST'

    def __init__(self, R):
        self.writer = R.MANIFEST_WRITER
        self.binding = R.ROUTE_B_BINDING
        self.driver_sha256 = DRIVER_SHA256
        self.checkpoint_module_sha256 = CHECKPOINT_SHA256

    def prep_pin(self, mw):
        return PREP

    def controller_libraries(self, ctl_mod):
        return {'lib': _load(LIBRARY[0], LIBRARY[1], 'syn_tk_lib'), 'roster': _load(ROSTER[0], ROSTER[1], 'syn_tk_roster'),
                'provider': _load(PROVIDER[0], PROVIDER[1], 'syn_tk_provider')}

    def binding_roster(self, bmod):
        return _load(ROSTER[0], ROSTER[1], 'syn_tk_roster_b')

    def h2_component(self, bmod):
        return dict(H2)
'''

WRAPPER_TEMPLATE = r'''"""TEST-ONLY S5 recipe wrapper (NGC acceptance c2v004 suite): roster_for_state = the real recipe module
ngc_roster_recipes_c2v001 (exact bytes) recipe_for_state with this run's synthetic toolkit (exact bytes)."""
import hashlib
import importlib.util

RECIPES = %(recipes)r
TOOLKIT = %(toolkit)r


def _load(path, sha, name):
    with open(path, 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != sha:
        raise ValueError('WRAPPER_PIN ' + path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


def roster_for_state(**kw):
    R = _load(RECIPES[0], RECIPES[1], 'suite_c2v004_recipes')
    T = _load(TOOLKIT[0], TOOLKIT[1], 'suite_c2v004_toolkit')
    return R.recipe_for_state(toolkit=T.SyntheticToolkit(R), **kw)
'''

H2_ROWS = [{'radius_kpc_literal': {'value': '%d/1000' % (5 * (i + 1))},
            'components': {'H2': {'value_literal': {'value': '%d/10' % (30 - 2 * i)}}},
            'conventions': {'gas_helium': {'value': 'ALREADY_INCLUDED'}}} for i in range(10)]
SYN_H2_COMPONENT = {'name': 'H2', 'radius_kpc': [0.005 * (i + 1) for i in range(10)],
                    'surface_density_Msun_pc2': [(30 - 2 * i) / 10.0 for i in range(10)], 'outer_scale_kpc': 0.02}


# ---------------------------------------------------------------------------------------------------------------- RFx
class RFx:
    """Recipe fixture: synthetic NGC calls whose recorded states come from the named code (controller, writer, binding)."""

    def __init__(self, root, suite):
        import numpy as np
        self.np, self.root, self.s = np, root, suite
        self.U, self.PV, self.R, self.S, self.E = suite.U, suite.PV, suite.R, suite.S, suite.E
        reg = os.path.join(root, 'registry')
        self.reg = reg
        self.driver_sha = suite.fx.registry['driver']['sha256']
        self.rs_pin = put_bytes(os.path.join(reg, 'syn_roster_module.py'), SYN_ROSTER_SRC.encode())
        self.cm_pin = put_bytes(os.path.join(reg, 'syn_checkpoint_module.py'), SYN_CHECKPOINT_SRC.encode())
        cdir = os.path.join(reg, 'syn_C')
        prof = {'schema': 'SYNTHETIC_GALAXY_RADIAL_SOURCE_REFERENCE', 'galaxies': {'NGC3198': {
            'HI_plus_He': {'s_edges_kpc2': [0.0, 0.0004, 0.0016, 0.0036, 0.0064, 0.01],
                           'annular_means_Msun_pc2': [5.0, 4.0, 3.0, 2.0, 1.0], 'boundary_controls_Msun_pc2': [5.0, 0.5]},
            'stellar_reference': {'height_kpc': 0.002, 'mass_kg': 1.0e33}}}}
        self.profile = put_json(os.path.join(cdir, 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json'), prof)
        self.h2 = put_json(os.path.join(reg, 'syn_h2_source.json'), {'S1_alternative_and_stellar_median_rows': {'rows': H2_ROWS}})
        self.coeff = put_bytes(os.path.join(reg, 'syn_coefficients.bin'), b'synthetic coefficient grid (test only)\n')
        self.prep_pin = put_bytes(os.path.join(reg, 'syn_prep.py'),
                                  (SYN_PREP_TEMPLATE % {'C': cdir, 'H2': self.h2['path']}).encode())
        self.cert = suite.fx.certs[0]
        self.launch = suite.fx.launch
        self.toolkit_pin = put_bytes(os.path.join(reg, 'syn_toolkit.py'), (SYN_TOOLKIT_TEMPLATE % {
            'driver': self.driver_sha, 'prep': (self.prep_pin['path'], self.prep_pin['sha256']),
            'cm': self.cm_pin['sha256'], 'roster': (self.rs_pin['path'], self.rs_pin['sha256']),
            'lib': tuple(suite.A.LIBRARY), 'provider': tuple(suite.S.PROVIDER), 'h2': SYN_H2_COMPONENT}).encode())
        self.recipes = {'path': suite.paths['RECIPES'], 'sha256': suite.shas['RECIPES']}
        self.wrapper = put_bytes(os.path.join(reg, 'syn_recipe_wrapper.py'), (WRAPPER_TEMPLATE % {
            'recipes': (self.recipes['path'], self.recipes['sha256']),
            'toolkit': (self.toolkit_pin['path'], self.toolkit_pin['sha256'])}).encode())
        self.SR = load(self.rs_pin['path'], 'rfx_syn_roster')
        self.SCM = load(self.cm_pin['path'], 'rfx_syn_checkpoint')
        self.MW = load(MW_PATH, 'rfx_manifest_writer', 'b9247b1aef0d9c3c05757bd27d68a9964a22d078ce8189311f11e0e2ad6b4c7c')
        cpath, csha = self.MW.PINS['controller']
        self.CTL = load(str(cpath), 'rfx_route_a_controller', csha)
        self.BB = load(BB_PATH, 'rfx_route_b_binding', 'aee7af1286f2d3d9d52117d6b4d4ae82e31d8776af4a4b0a6da7cee96be12fb3')
        self.BB.ngc_h2_component = lambda: (dict(SYN_H2_COMPONENT), {'synthetic': True})     # fixture only: never the registered H2
        self.libs = {'lib': self.U, 'roster': self.SR, 'provider': self.PV}
        self.gamma = 9.0
        self.r = 0.5
        self.a = 2
        self.cfg_raw = {'enabled': True, 'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 32.0}, 'source_rule': 'continuum_v001',
                        'gas': {'interp': 'lagrange3_s_gl4', 'M_s': 4},
                        'stars': {'segment_rule': 'max16_ceil_kdr_plus8', 'tail_rule': 't_panels_40a_phase1p5_gl12'},
                        'quadrature': {'order': 2, 'w_perp_max_inverse_kpc': 4.0, 'w_z_max_inverse_kpc': 4.0},
                        'domain': {'R_eval_max_kpc': 0.1, 'z_eval_max_kpc': 0.1, 'z_src_max_kpc': 0.1},
                        'asymptote': 'EH_exact_minus_quarter', 'lapse_only': True,
                        'jet_order': {'route_a': 1, 'route_b': 1, 'ngc_eval': 1}, 'lambda_scale': 1.0,
                        'eps_certificate': dict(self.cert), 'lo_certificate': dict(self.launch)}
        self.n = 0

    # ------------------------------------------------------------------------------------------------ pieces
    def ni(self):
        return {'kpc_m': KPC_M, 'solar_mass_kg': 1.98847e30, 'pressure_step_kpc': 0.01, 'kmax_inverse_kpc': 2.0,
                'gamma': self.gamma, 'composite_grid_spec': {'breaks_inverse_kpc': [-2.0, 0.0, 2.0], 'panel_orders': [4, 4]},
                'source_gauss_order': 4, 'h2_tail_mass_rtol': 1.0e-10}

    def prep_module(self, patched):
        mod = load(self.prep_pin['path'], 'rfx_syn_prep_%d' % self.n, self.prep_pin['sha256'])
        if patched:
            mod.COEFFICIENT = __import__('pathlib').Path(self.coeff['path'])
            mod.COEFFICIENT_SHA = self.coeff['sha256']
        return mod

    def patches(self):
        return [{'path': self.prep_pin['path'], 'sha256': self.prep_pin['sha256'],
                 'set': {'COEFFICIENT': {'__path__': self.coeff['path']}, 'COEFFICIENT_SHA': self.coeff['sha256']}}]

    def elements(self, n):
        np = self.np
        pos = np.array([[(0.01 + 0.012 * i + 0.003 * n) * KPC_M, (0.004 * i - 0.002 * n) * KPC_M, 0.001 * (i - 1) * KPC_M]
                        for i in range(3)])
        J = np.array([1.0e33 * (1.0 + 0.2 * i + 0.1 * n) for i in range(3)])
        return pos, J

    def as_field(self, v):
        np = self.np
        out = np.zeros((len(v), 10, 1), dtype=complex)
        out[:, 0, 0] = v
        return out

    def ckpt_array(self, cp, rel, arr):
        np = self.np
        buf = io.BytesIO()
        np.save(buf, np.asarray(arr), allow_pickle=False)
        pin = put_bytes(os.path.join(cp, rel), buf.getvalue())
        return {'file': rel, 'array_sha256': pin['sha256']}

    # ------------------------------------------------------------------------------------------------ one call
    def make_call(self, name, **o):
        np, U, PV, SR, CTL, MW, BB = self.np, self.U, self.PV, self.SR, self.CTL, self.MW, self.BB
        self.n += 1
        base = os.path.join(self.root, 'calls', name)
        call_dir = os.path.join(base, 'call')
        out = os.path.join(call_dir, 'out')
        stages = os.path.join(out, 'stages')
        os.makedirs(os.path.join(out, 'inputs'))
        ni = self.ni()
        cfg = U.normalize_config(self.cfg_raw)
        cfg_pin = put_json(os.path.join(out, 'inputs', 'uv_tail_config.json'), self.cfg_raw)
        request = {'schema': 'UNT_UV_TAIL_ROUTE_A_REQUEST_C2V001', 'uv_tail': self.cfg_raw, 'admissibility': 'production',
                   'monitor': {'probe_R_m': [0.02 * KPC_M, 0.05 * KPC_M, 0.09 * KPC_M], 'probe_phi_rad': [0.0, 0.5 * math.pi],
                               'v_ref_km_s': None, 'tau_km_s': None, 'threshold': 0.25, 'provenance': {'synthetic': True}}}
        req_pin = put_json(os.path.join(out, 'inputs', 'uv_tail_route_a_request.json'), request)
        seed = {'status': 'SYNTHETIC_SEED', 'numerical_inputs': ni,
                'pins': {self.profile['path']: self.profile['sha256'], self.h2['path']: self.h2['sha256'],
                         self.coeff['path']: self.coeff['sha256']}}
        seed_pin = put_json(os.path.join(out, 'inputs', 'ngc_seed_v011.json'), seed)
        prep = self.prep_module(patched=True)
        data = prep.prepare_inputs(**ni)
        waves = np.asarray(data['fourier_arguments']['k_physical'], float)
        nk = len(waves)
        jn = PV.create_provider()
        # ---------------------------------------------------------------- route A: the real controller writes the sidecar
        ra = os.path.join(stages, '01_route_a')
        att, cp, sdir = os.path.join(ra, 'attempt_000'), os.path.join(ra, 'checkpoint'), os.path.join(ra, 'uv_tail_sidecar')
        os.makedirs(cp)
        cpid = sha_bytes(('synthetic checkpoint identity ' + name).encode())
        ctl = CTL.RouteATailController.from_prepared(galaxy='NGC3198', prep_module=prep, prep_arguments=ni, data=data,
                                                     request=request, sidecar_directory=sdir, libraries=self.libs)
        if o.get('drop_element'):
            dropped = os.path.join(ra, 'dropped_elsewhere')
            os.makedirs(dropped)
            orig = ctl._path
            ctl._path = lambda nm: (__import__('pathlib').Path(dropped) / nm) if nm == 'elements_0000.npz' else orig(nm)
        ctl.open(relaxation=self.r, start_iteration=0, checkpoint_mode='new', checkpoint_identity_sha256=cpid)
        init = ctl.init_rings
        gas = self.as_field(SR.ring_transform(init['R'], init['z'], init['m'], waves, C_M_S, jn.j0))
        prepared = {'weighted_responses': np.full((nk, 10, 1), 1.0e-3 + 0j), 'wavevectors': waves}
        gases, els, upds = [], [], []
        for n in range(self.a + 1):
            if n == 1 and o.get('chain_break'):
                j = int(np.argmax(np.abs(gas[:, 0, 0])))
                gas = gas.copy()
                gas[j, 0, 0] = gas[j, 0, 0] * (1.0 + 1.0e-13)
            gases.append(gas)
            ctl.begin_iteration(iteration=n, gas=gas)
            pos, J = self.elements(n)
            upd = self.as_field(SR.point_transform(pos, J, waves))
            cols = [[[float(x)]] + [[0.0]] * 9 for x in J]
            ctl.complete_iteration(iteration=n, positions=pos, columns=cols, gas=gas, updated=upd, current=gas + 1.0e30,
                                   prepared=prepared, converged=(n == self.a))
            els.append({'positions_m': pos, 'integrated_J': J})
            upds.append(upd)
            gas = (1 - self.r) * gas + self.r * upd
        rec = plain(ctl.result_record(outcome=CONV))
        payloads = [json.loads(open(os.path.join(sdir, 'iteration_%04d.json' % n)).read())['payload'] for n in range(self.a + 1)]
        # ---------------------------------------------------------------- checkpoint (driver L7024-7038 form)
        star_b = BB.Binding(types.SimpleNamespace(uv_tail_tap=0), 'fs_columns', cfg, cfg_pin['sha256'])
        star_b.lib, star_b.rs, star_b.pv, star_b.jn = U, SR, PV, jn
        _, _, star_rings = star_b._stars((self.profile['path'], self.profile['sha256']), 'NGC3198', ni)
        fixed = self.as_field(SR.packet_transform(star_rings, waves, 'prep_analytic_j0', c_m_s=C_M_S, j0=jn.j0))
        ident_body = {'synthetic': True, 'caller': name}
        put_json(os.path.join(cp, 'IDENTITY.json'), {'kind': 'identity', 'identity': ident_body, 'identity_sha256': cpid})
        starts = []
        for n in range(self.a + 1):
            g = gases[n]
            gref = self.ckpt_array(cp, 'iteration_%04d/gas_fourier_J.npy' % n, g)
            ge = o.get('gas_edit') if n == 1 else None
            if ge is not None:
                gx = g.copy()
                if ge == 'tiny':                                   # inside the I1-T tolerance: a different recorded max_rel
                    jx = int(np.argmax(np.abs(gx[:, 0, 0])))
                    gx[jx, 0, 0] = gx[jx, 0, 0] * (1.0 + 1.0e-14)
                else:
                    gx[3, 0, 0] = gx[3, 0, 0] * (1.0 + 1.0e-6)
                eref = self.ckpt_array(cp, 'iteration_%04d/gas_fourier_J_edited.npy' % n, gx)
                gref = dict(eref, array_sha256=gref['array_sha256']) if ge == 'bytes' else eref
            fref = self.ckpt_array(cp, 'iteration_%04d/fixed_source_fourier_J.npy' % n, fixed)
            body = {'iteration': n, 'identity_sha256': cpid, 'gas_fourier_J': gref, 'fixed_source_fourier_J': fref}
            psha = sha_bytes(canon(body).encode())
            psha_true = psha
            if ge == 'repinned':
                psha_true = sha_bytes(canon(dict(body, gas_fourier_J=self.ckpt_array(
                    cp, 'iteration_%04d/gas_fourier_J_original_ref.npy' % n, g))).encode())
            put_json(os.path.join(cp, 'iteration_%04d' % n, 'START.json'), dict(body, kind='iteration_start', payload_sha256=psha))
            put_json(os.path.join(cp, 'iteration_%04d' % n, 'COMPLETED.json'), {
                'kind': 'iteration_completed', 'iteration': n, 'identity_sha256': cpid,
                'iteration_start_sha256': psha_true if ge == 'repinned' else psha, 'converged': n == self.a})
            starts.append(dict(body, payload_sha256=psha))
        # ---------------------------------------------------------------- attempt (MW attempt_tail_record form)
        ares = put_json(os.path.join(att, 'result.json'), {'result': {'uv_tail': rec, 'source_fixed_point': {
            'checkpoint': {'identity_sha256': cpid, 'attempt': 'synthetic'}}}})
        put_json(os.path.join(att, 'finish.json'), {'status': 'RETURNED_ACTUAL_RESULT', 'result_sha256': ares['sha256']})
        records = []

        def stage_record(sname, kind, sdir_, script, argv, patches=None):
            req = {'name': sname, 'kind': kind, 'script': script['path'], 'script_sha256': script['sha256'],
                   'argv': [str(x) for x in argv], 'stage_globals': {}, 'module_patches': patches or [], 'mask': None}
            rp = put_json(os.path.join(sdir_, 'request.json'), req)
            r = dict(req, request_path=rp['path'], request_sha256=rp['sha256'], stage_dir=sdir_, exit_code=0,
                     elapsed_seconds=0.0, executed=True)
            records.append(r)
            return r
        worker = put_bytes(os.path.join(base, 'syn_route_a_worker.py'), b'# synthetic route-A worker (test only)\n')
        stage_record('route_a', 'route_a', ra, worker,
                     ['--seed', seed_pin['path'], '--seed-sha256', seed_pin['sha256'], '--outdir', att, '--checkpoint-directory', cp,
                      '--start-iteration', '0', '--uv-tail-config', req_pin['path'], '--uv-tail-config-sha256', req_pin['sha256'],
                      '--uv-tail-sidecar-directory', sdir], self.patches())
        # ---------------------------------------------------------------- manifest stage: the real writer's functions
        ms = os.path.join(stages, '02_route_a_tail_manifest')
        mdir = os.path.join(ms, 'manifest')
        os.makedirs(ms)
        mprep = self.prep_module(patched=not o.get('drop_patch_in_run'))
        mctl = CTL.RouteATailController.from_prepared(galaxy='NGC3198', prep_module=mprep, prep_arguments=ni,
                                                      data=mprep.prepare_inputs(**ni), request=request, sidecar_directory=None,
                                                      libraries=self.libs)
        sid = json.loads(open(os.path.join(sdir, 'SIDECAR_IDENTITY.json')).read())['identity']
        st = MW.rebuild_state(mctl, sidecar_identity=sid, elements=els[:self.a], n=self.a, gas=gases[self.a])
        assert st.digest == payloads[self.a]['state_digest'] == rec['boundary_state_digest_at_return'], 'MW rebuild'
        mrec = MW.write_outputs(mdir, controller=mctl, state=st, n=self.a, identity_sha256=cpid,
                                start_payload_sha256=starts[self.a]['payload_sha256'], provenance={'synthetic': True})
        mfin = put_json(os.path.join(mdir, 'finish.json'), dict(status='ROUTE_A_TAIL_MANIFEST_WRITTEN', elapsed_seconds=0.0,
                                                               worker_sha256=sha_file(MW_PATH), **mrec))
        writer = {'path': MW_PATH, 'sha256': sha_file(MW_PATH)}
        if o.get('writer_sha'):                                    # e.g. the STAGE0 writer 443d9fdc: not recipe-bound
            writer = put_bytes(os.path.join(base, 'syn_other_writer.py'), b'# another manifest writer (test only)\n')
        stage_record('route_a_tail_manifest', 'route_a_tail_manifest', ms, writer,
                     ['--seed', seed_pin['path'], '--seed-sha256', seed_pin['sha256'], '--attempt-directory', att,
                      '--checkpoint-directory', cp, '--checkpoint-module', self.cm_pin['path'],
                      '--checkpoint-module-sha256', self.cm_pin['sha256'], '--uv-tail-request', req_pin['path'],
                      '--uv-tail-request-sha256', req_pin['sha256'], '--outdir', mdir],
                     [] if o.get('drop_patch') else self.patches())
        man_pin = {'path': mrec['manifest'], 'sha256': mrec['manifest_sha256']}
        accepted = mrec['state_digest']
        # ---------------------------------------------------------------- route B: the real binding builds every state
        phys = {'gamma': self.gamma, 'c_m_s': C_M_S}
        profile = (self.profile['path'], self.profile['sha256'])
        common = ['--seed', seed_pin['path'], '--checkpoint-directory', cp]
        tail_argv = ['--uv-tail-config', cfg_pin['path'], '--uv-tail-config-sha256', cfg_pin['sha256']]
        man_argv = ['--route-a-tail-manifest', man_pin['path'], '--route-a-tail-manifest-sha256', man_pin['sha256']]
        stage_script = put_bytes(os.path.join(base, 'syn_route_b_stage.py'), b'# synthetic route-B stage successor (test only)\n')
        finishes = {}
        counter = [2]

        def binding(kind, outdir, **extra):
            ns = types.SimpleNamespace(**dict(dict(uv_tail_tap=0, outdir=outdir, uv_tail_truncation=None, route_a_tail_manifest=None,
                                                   route_a_tail_manifest_sha256=None, uv_tail_source_rotation_directory=None,
                                                   uv_tail_admit_test_only=False), **extra))
            b = BB.Binding(ns, kind, cfg, cfg_pin['sha256'])
            b.lib, b.rs, b.pv, b.jn = U, SR, PV, PV.create_provider()
            return b

        def finish(sname, ckind, outdir, b, extra=None, argv=(), mutate=None):
            sd = os.path.dirname(outdir)
            os.makedirs(outdir, exist_ok=True)
            body = dict(extra or {}, uv_tail=json.loads(json.dumps(plain(b.record(final=True)['uv_tail']))))
            if mutate:
                mutate(body)
            fp = put_json(os.path.join(outdir, 'finish.json'), body)
            finishes[sname] = (ckind, fp, body)
            stage_record(sname, ckind, sd, stage_script, list(argv) + ['--outdir', outdir])
            return fp, body

        def sd(nm):
            counter[0] += 1
            return os.path.join(stages, '%02d_%s' % (counter[0] + 1, nm))
        ident = cpid
        start_a = starts[self.a]
        # reference, body: the accepted manifest state (BB L457-470)
        ref_out = os.path.join(sd('reference'), 'reference')
        b = binding('reference', ref_out, route_a_tail_manifest=man_pin['path'], route_a_tail_manifest_sha256=man_pin['sha256'])
        b.bind(ni=ni, phys=phys, galaxy='NGC3198', profile=profile, identity=ident, iteration=self.a, start=start_a,
               prepared=prepared, caller={})
        rfp, rbody = finish('reference', 'reference', ref_out, b, argv=common + tail_argv + man_argv)
        body_out = os.path.join(sd('body'), 'body')
        b = binding('body', body_out, route_a_tail_manifest=man_pin['path'], route_a_tail_manifest_sha256=man_pin['sha256'])
        b.bind(ni=ni, phys=phys, galaxy='NGC3198', profile=profile, identity=ident, iteration=self.a, start=start_a,
               prepared=prepared, reference_start=rbody, reference_finish=rbody, caller={})
        body_pos = np.array([[(0.012 + 0.013 * i) * KPC_M, (0.003 * i) * KPC_M, 0.0005 * (i - 2) * KPC_M] for i in range(5)])
        body_J = np.zeros((5, 10, 1))
        body_J[:, 0, 0] = [1.0e33 * (1.0 + 0.15 * i) for i in range(5)]
        radial = np.array([0.02, 0.04, 0.06, 0.08]) * KPC_M
        body_arr = put_npz(os.path.join(body_out, 'body_arrays.npz'),
                           {'physical_positions_m': body_pos, 'base_integrated_source_J': body_J, 'radial_nodes_m': radial})
        bfp, bbody = finish('body', 'body', body_out, b, extra={'outputs': {'body_arrays.npz': body_arr}},
                            argv=common + tail_argv + man_argv)
        # offset (BB bind_offset)
        off_out = os.path.join(sd('offset'), 'offset')
        b = binding('offset', off_out, route_a_tail_manifest=man_pin['path'], route_a_tail_manifest_sha256=man_pin['sha256'])
        b.bind(ni=ni, phys=phys, galaxy='NGC3198', profile=profile, identity=ident, iteration=self.a, start=start_a,
               body_finish=bbody, caller={})
        new_body = self.as_field(SR.point_transform(body_pos, body_J[:, 0, 0], waves))
        b.bind_offset(body={'physical_positions_m': body_pos, 'base_integrated_source_J': body_J, 'radial_nodes_m': radial},
                      new=new_body, waves=waves, unit_weighted_responses=prepared['weighted_responses'])
        base_pos = np.array([[(0.015 + 0.012 * i) * KPC_M, (-0.002 * i) * KPC_M, 0.0004 * (i - 2) * KPC_M] for i in range(5)])
        rho0 = np.array([1.0e-21 * (1.0 + 0.1 * i) for i in range(5)])
        vol = np.full(5, 1.0e37)
        base_J = (-C_M_S * C_M_S * rho0 * vol).reshape(-1)
        base_arrays = {'physical_positions_m': base_pos, 'rho0': rho0, 'volume_weights_m3': vol, 'radial_nodes_m': radial}
        os.makedirs(off_out, exist_ok=True)
        upb = put_npz(os.path.join(off_out, 'updated_base_arrays.npz'), base_arrays)
        if o.get('base_edit'):
            upb = put_npz(os.path.join(off_out, 'updated_base_arrays_edited.npz'), dict(base_arrays, rho0=rho0 * (1.0 + 1.0e-9)))
        srcoff = put_npz(os.path.join(off_out, 'source_offset.npz'),
                         {'new_body_fourier_J': self.as_field(SR.point_transform(base_pos, base_J, waves))})
        off_body = {'outputs': {'source_offset.npz': srcoff, 'updated_base_arrays.npz': upb},
                    'uv_tail': json.loads(json.dumps(plain(b.record(final=True)['uv_tail'])))}
        ofp = put_json(os.path.join(off_out, 'finish.json'), off_body)
        finishes['offset'] = ('offset', ofp, off_body)
        stage_record('offset', 'offset', os.path.dirname(off_out), stage_script,
                     common + ['--body-directory', body_out, '--body-finish-sha256', bfp['sha256'], '--wave-batch', '64',
                               '--position-batch', '64'] + tail_argv + man_argv + ['--outdir', off_out])
        base_argv = common + ['--offset-directory', off_out]
        start_fs = start_a
        fs_radii = np.unique(radial)
        # fs_columns_00, fs_rotation (BB L476-501)
        kinds_fs = (('fs_columns_00', 'columns_v001', 'fs_columns', 'columns'), ('fs_rotation', 'rotation_v001', 'fs_rotation', 'rotation'))
        rot_arrays = None
        for sname, ckind, bkind, leaf in kinds_fs:
            if o.get('swap_kind') and sname == 'fs_columns_00':
                ckind = 'rotation_v001'
            od = os.path.join(sd(sname), leaf)
            b = binding(bkind, od)
            ph = dict(phys, gamma=math.nextafter(self.gamma, math.inf)) if (o.get('route_b_gamma_ulp') and sname == 'fs_columns_00') else phys
            b.bind(ni=ni, phys=ph, galaxy='NGC3198', profile=profile, identity=ident, iteration=self.a, start=start_fs,
                   prepared=prepared, cm=self.SCM, cp=cp, offset_finish=off_body, base=base_arrays, radii=fs_radii, caller={})
            extra = {}
            if leaf == 'rotation':
                os.makedirs(od, exist_ok=True)
                rho = np.full((4, 2, 3), 1.0e-21)
                rho[:, 1, :] *= 1.5
                zz = np.tile(np.array([-0.002, 0.0, 0.002]) * KPC_M, (4, 2, 1))
                rot = put_npz(os.path.join(od, 'rotation_base_arrays.npz'), {
                    'rho0': rho, 'volume_weights_m3': np.full((4, 2, 3), 1.0e37), 'radial_nodes_m': radial, 'z': zz})
                rot_arrays = {'rho0': rho, 'volume_weights_m3': np.full((4, 2, 3), 1.0e37), 'radial_nodes_m': radial, 'z': zz}
                extra = {'arrays_path': rot['path'], 'arrays_sha256': rot['sha256'], 'positive_rotation_square': True,
                         'minimum_rotation_square': 1.0, 'nonpositive_indices': []}
                mut = (lambda bd: bd['uv_tail'].update(binding_sha256='0' * 64)) if o.get('binding_sha') else None
                body = dict(extra, uv_tail=json.loads(json.dumps(plain(b.record(final=True)['uv_tail']))))
                if mut:
                    mut(body)
                fp = put_json(os.path.join(od, 'finish.json'), body)
                finishes[sname] = (ckind, fp, body)
                stage_record(sname, ckind, os.path.dirname(od), stage_script, base_argv + tail_argv + ['--outdir', od])
                fs_rot, fs_rot_fin = od, fp
            else:
                finish(sname, ckind, od, b, argv=base_argv + ['--controls', 'x', '--controls-sha256', '0' * 64] + tail_argv)
        # fs_feedback (not a tail stage): the gas packet the rfs/le stages check (BB L518-523)
        fb_out = os.path.join(sd('fs_feedback'), 'feedback')
        m_ring = np.sum(rot_arrays['volume_weights_m3'] * rot_arrays['rho0'], axis=1)
        Rg = np.repeat(rot_arrays['radial_nodes_m'], rot_arrays['z'].shape[2])
        zg = rot_arrays['z'][:, 0, :].reshape(-1)
        gfb = put_npz(os.path.join(fb_out, 'gas_source_feedback.npz'), {'new_gas_fourier_J': self.as_field(
            SR.packet_transform(dict(R=Rg, z=zg, m=m_ring.reshape(-1)), waves, 'feedback_ring_j0_v004', c_m_s=C_M_S, j0=jn.j0))})
        fb_fin = {'outputs': {'gas_source_feedback.npz': gfb}, 'status': 'synthetic'}
        fbp = put_json(os.path.join(fb_out, 'finish.json'), fb_fin)
        stage_record('fs_feedback', 'feedback_v002', os.path.dirname(fb_out), stage_script, base_argv + ['--outdir', fb_out])
        fb_start = {'rotation_finish_sha256': fs_rot_fin['sha256'], 'worker_sha256': '1' * 64}
        # rfs_columns_00, le1_columns_00, le1_rotation (BB L502-527)
        for sname, ckind, bkind, leaf in (('rfs_columns_00', 'columns_v003', 'rfs_columns', 'columns'),
                                          ('le1_columns_00', 'columns_v005', 'le_columns', 'columns'),
                                          ('le1_rotation', 'rotation_v005', 'le_rotation', 'rotation')):
            od = os.path.join(sd(sname), leaf)
            b = binding(bkind, od, uv_tail_source_rotation_directory=fs_rot)
            b.bind(ni=ni, phys=phys, galaxy='NGC3198', profile=profile, identity=ident, iteration=self.a, start=start_fs,
                   prepared=prepared, cm=self.SCM, cp=cp, offset_finish=off_body, feedback_start=fb_start, feedback_finish=fb_fin,
                   radii=fs_radii, caller={})
            finish(sname, ckind, od, b, argv=base_argv + ['--feedback-directory', fb_out, '--feedback-finish-sha256', fbp['sha256']]
                   + tail_argv + ['--uv-tail-source-rotation-directory', fs_rot])
        # ---------------------------------------------------------------- result, finish (driver L9081-9101 form)
        srecs = [{'stage': 'route_a_tail_manifest', 'kind': 'route_a_tail_manifest', 'finish_sha256': mfin['sha256'],
                  'state_digest': accepted, 'empty': False, 'production_admissible': True, 'test_only_admitted': None,
                  'i1t_verdict': None, 'srb_rot': None}]
        for sname, (ckind, fp, body) in finishes.items():
            u = body['uv_tail']
            srecs.append({'stage': sname, 'kind': ckind, 'finish_sha256': fp['sha256'], 'state_digest': u.get('state_digest'),
                          'empty': u.get('empty'), 'production_admissible': u.get('production_admissible'),
                          'test_only_admitted': u.get('test_only_admitted'), 'i1t_verdict': (u.get('i1t') or {}).get('verdict'),
                          'srb_rot': u.get('srb_rot')})
        rar = {k: rec.get(k) for k in ('outcome', 'accepted_iteration', 'M_T_accepted', 'M_T_threshold', 'monitor_status', 'flags',
                                       'production_admissible', 'boundary_state_digest_at_return', 'config_sha256',
                                       'request_sha256', 'admissibility', 'E_A_rows_km_s_accepted', 'sidecar')}
        rar.update(probe_R_m=request['monitor']['probe_R_m'], probe_phi_rad=request['monitor']['probe_phi_rad'], probe_source='synthetic')
        result = {'driver_sha256': self.driver_sha, 'galaxy': 'NGC3198', 'status': 'COMPLETED', 'valid': True,
                  'call_spec_sha256': '2' * 64, 'normalized_spec': {'galaxy': 'NGC3198', 'synthetic': True},
                  'identity': {'seed': {'path': seed_pin['path'], 'sha256': seed_pin['sha256'], 'source': 'synthetic'},
                               'route_a': {'mode': 'computed', 'attempt': att, 'checkpoint': cp,
                                           'custody': {'identity_sha256': cpid, 'iteration': self.a,
                                                       'start_payload_sha256': start_a['payload_sha256']}}},
                  'stage_records': records,
                  'uv_tail': {'config': {'path': cfg_pin['path'], 'sha256': cfg_pin['sha256'], 'normalized_sha256': cfg['sha256']},
                              'request': {'path': req_pin['path'], 'sha256': req_pin['sha256']},
                              'manifest': dict(man_pin, state_digest=accepted, empty=False, production_admissible=True),
                              'route_a_record': rar, 'stage_records': srecs}}
        rp = put_json(os.path.join(out, 'result.json'), result)
        put_json(os.path.join(out, 'finish.json'), {'status': 'COMPLETED', 'valid': True, 'result_path': rp['path'],
                                                    'result_sha256': rp['sha256'], 'retries': 0, 'reasons': []})
        return {'name': name, 'base': base, 'call_dir': call_dir, 'out': os.path.realpath(out), 'result': rp, 'payloads': payloads,
                'accepted': accepted, 'finishes': {k: v[2] for k, v in finishes.items()}, 'a': self.a}

    # ------------------------------------------------------------------------------------------------ S5 / targets
    def route_a_targets(self, c):
        enum = self.R.enumerate_sidecar(c['call_dir'], driver_sha256=self.driver_sha)
        return self.R.s5_targets(enum), enum

    def route_b_targets(self, c):
        inv = self.E.enumerate_call(c['call_dir'], route_a_iterates_ref=None, driver_sha256=self.driver_sha)
        out = []
        for oc in inv.get('occurrences') or []:
            if oc.get('role') == 'own_source_state':
                out.append({'state': dict(oc['state']), 'origin': {'kind': 'ROUTE_B_STAGE', 'stage': oc['stage']}})
        return out, inv

    def admit(self, c, target, tag, recipe=None, approved=None):
        d = os.path.join(c['base'], 's5_' + tag)
        os.makedirs(d)
        rec = recipe or self.wrapper
        pin = self.S.rebuild_admit(call_dir=c['call_dir'], target=target, recipe_ref=rec,
                                   approved_recipe_sha256=[rec['sha256']] if approved is None else approved, out_dir=d,
                                   driver_sha256=self.driver_sha)
        return read_json(pin), pin

    def direct(self, c, target, toolkit=None):
        """The recipe called directly (no S5): returns the RecipeRefusal code, or None."""
        R = load(self.recipes['path'], 'rfx_direct_recipes', self.recipes['sha256'])
        T = load(self.toolkit_pin['path'], 'rfx_direct_toolkit', self.toolkit_pin['sha256'])
        result = read_json(c['result'])
        try:
            R.recipe_for_state(call_dir=c['call_dir'], out_dir=c['out'], result=result, target=target, lib=self.S.libraries()[0],
                               provider=self.S.libraries()[1], toolkit=toolkit or T.SyntheticToolkit(R))
            return None, None
        except R.RecipeRefusal as exc:
            return exc.code, str(exc)[:240]


# ---------------------------------------------------------------------------------------------------------------- suite
def make_suite_class(T):
    class Suite4(T.Suite):
        def __init__(self, run_dir, module_dir):
            T.Suite.__init__(self, run_dir, module_dir)
            self.paths['RECIPES'] = os.path.join(module_dir, RECIPES_NAME)
            self.shas['RECIPES'] = sha_file(self.paths['RECIPES'])
            self.rfx = RFx(os.path.join(run_dir, 'recipes'), self)
            self.blocked = []

        # ported runner: the c2v003a tests with the c2v004 handoff; the approvals carry the (synthetic) recipe
        def handoff(self, call, *, approvals=None, **kw):
            approvals = approvals or {'reader': dict(self.H.ITERATE_READER), 's5': dict(self.H.S5_TOOL),
                                      'recipes': dict(self.fx.recipe)}
            return T.Suite.handoff(self, call, approvals=approvals, **kw)

        def run(self, rid, kind, fn):
            n0 = len(GUARD['blocked'])
            T.Suite.run(self, rid, kind, fn)
            new = GUARD['blocked'][n0:]
            if new:
                r = self.results[-1]
                r['blocked_by_hard_rule'] = sorted(set(new))
                r['ok_as_run'] = r['ok']
                r['ok'] = None
                self.blocked.append(rid.split()[0])

        # ======================================================================== c2v004 MUST_PASS
        def p36(self):
            """A177: the handoff c2v004 pins the recipe module (sha from bytes) as the approved-recipe source: the prepare
            default, the REGISTERED approvals and the record pins; everything else is c2v003a's pins."""
            H = self.H
            import inspect
            sig = inspect.signature(H.prepare_acceptance_inputs)
            c = self.fx.make_call('p36')
            rec, _ = self.handoff(c)
            src = inspect.getsource(H._accept)
            ok = (H.ROSTER_RECIPES == {'path': self.paths['RECIPES'], 'sha256': self.shas['RECIPES']}
                  and sig.parameters['recipe_ref'].default is None and sig.parameters['approved_recipe_sha256'].default is None
                  and "'recipes': ROSTER_RECIPES" in src and rec['pins']['roster_recipes'] == self.fx.recipe
                  and rec['reading'] == 'ACCEPTED' and H.LO_ADAPTER['sha256'] == '9c4b6dfc591cfd5c372416beb936d5d903540e5fc41e4a327b428d7ba5001eb2'
                  and H.ITERATE_READER['sha256'] == self.shas['R'] and H.S5_TOOL['sha256'] == self.shas['S']
                  and H.RECORD_SCHEMA == 'UNT_NGC_LO_ACCEPTANCE_RECORD_C2V004')
            return ok, {'ROSTER_RECIPES': H.ROSTER_RECIPES['sha256'], 'reading': rec['reading']}

        def r01(self):
            """Route A: every non-accepted iterate except the monitor-next state is rebuilt by the real recipe (manifest-writer
            path at iteration m) and S5 ADMITS it on exact TailState digest equality; the recipe provenance cites its inputs."""
            c = self.rfx.make_call('r01')
            tg, enum = self.rfx.route_a_targets(c)
            res = {}
            for t in tg:
                o = t['origin']
                a, _ = self.rfx.admit(c, t, 'r01_%d_%s' % (o['iteration'], o['role'][:4]))
                res[(o['iteration'], o['role'])] = a
            p = c['payloads']
            nx = (c['a'], NEXT)
            adm = {k: v for k, v in res.items() if k != nx}
            ok = (enum['accepted_iteration'] == 2 and enum['chain_next_equals_next_current'] == [True, True]
                  and set(res) == {(0, CURRENT), (0, NEXT), nx}
                  and all(a['admitted'] is True and a['digest_equal'] is True and a['codes'] == [] for a in adm.values())
                  and res[(0, CURRENT)]['rebuilt']['state_digest'] == p[0]['state_digest']
                  and res[(0, NEXT)]['rebuilt']['state_digest'] == p[1]['state_digest']
                  and all(a['recipe_provenance']['recipe'] == 'RECIPE_ROUTE_A' and a['recipe_provenance']['toolkit'] == 'SYNTHETIC_TEST'
                          and a['recipe_provenance']['inputs']['gas']['basis'] == 'FORMAL' for a in adm.values())
                  and res[nx]['admitted'] is False and 'ROUTE_A_MONITOR_NEXT_GAS_UNRECORDED' in ' '.join(res[nx]['detail']))
            return ok, {str(k): (v['admitted'], v['codes']) for k, v in res.items()}

        def r02(self):
            """Route B: offset, fs columns/rotation, rfs columns, le columns/rotation are each rebuilt by its
            RECIPE_ROUTE_B_<kind>; S5 checks the recipe roster digest against the recorded uv_tail.roster_digest and ADMITS
            each on exact TailState digest equality."""
            c = self.rfx.make_call('r02')
            tg, inv = self.rfx.route_b_targets(c)
            res = {}
            for t in tg:
                a, _ = self.rfx.admit(c, t, 'r02_' + t['origin']['stage'])
                res[t['origin']['stage']] = (t['state']['stage_kind'], a)
            want = {'offset': 'offset', 'fs_columns_00': 'fs_columns', 'fs_rotation': 'fs_rotation', 'rfs_columns_00': 'rfs_columns',
                    'le1_columns_00': 'le_columns', 'le1_rotation': 'le_rotation'}
            ok = ({k: v[0] for k, v in res.items()} == want
                  and all(a['admitted'] is True and a['roster']['equal'] is True and a['digest_equal'] is True for _, a in res.values())
                  and all(a['recipe_provenance']['recipe'] == 'RECIPE_ROUTE_B_' + k for k, a in res.values())
                  and res['offset'][1]['recipe_provenance']['inputs']['eval_radii_m']['basis'] == 'FORMAL'
                  and res['fs_columns_00'][1]['recipe_provenance']['inputs']['eval_radii_m']['basis'] == 'DECLARED')
            return ok, {k: (v[0], v[1]['admitted'], v[1]['codes']) for k, v in res.items()}

        def r03(self):
            """Route A with a broken chain (iteration 1 began from a gas array not bitwise the monitor's g_next): the begun
            state of iteration 1 is rebuilt from START(1) and ADMITTED."""
            c = self.rfx.make_call('r03', chain_break=True)
            tg, enum = self.rfx.route_a_targets(c)
            t1 = [t for t in tg if t['origin'] == {'kind': 'ROUTE_A_ITERATE', 'iteration': 1, 'role': CURRENT}]
            a, _ = self.rfx.admit(c, t1[0], 'r03') if len(t1) == 1 else ({'admitted': None}, None)
            ok = enum['chain_next_equals_next_current'] == [False, True] and len(t1) == 1 and a['admitted'] is True
            return ok, {'chain': enum['chain_next_equals_next_current'], 'admitted': a.get('admitted'), 'codes': a.get('codes')}

        def r04(self):
            """Custody: during S5 + recipe, every file opened is the call's own output, the S5 out dir, a pinned module, a
            seed pin or a config certificate; no open is refused by the hard-rule guard."""
            c = self.rfx.make_call('r04')
            tga, _ = self.rfx.route_a_targets(c)
            tgb, _ = self.rfx.route_b_targets(c)
            n0 = len(GUARD['blocked'])
            GUARD['log'] = []
            try:
                a1, _ = self.rfx.admit(c, [t for t in tga if t['origin']['role'] == CURRENT][0], 'r04_a')
                a2, _ = self.rfx.admit(c, [t for t in tgb if t['origin']['stage'] == 'le1_rotation'][0], 'r04_b')
                a3, _ = self.rfx.admit(c, [t for t in tgb if t['origin']['stage'] == 'offset'][0], 'r04_c')
            finally:
                log, GUARD['log'] = GUARD['log'], None
            fx = self.rfx
            allowed_files = {os.path.realpath(p) for p in (
                self.A.LIBRARY[0], self.S.PROVIDER[0], self.paths['S'], self.paths['RECIPES'], fx.wrapper['path'], fx.toolkit_pin['path'],
                fx.rs_pin['path'], fx.cm_pin['path'], fx.prep_pin['path'], MW_PATH, BB_PATH, CTL_PATH, fx.profile['path'],
                fx.h2['path'], fx.coeff['path'], fx.cert['path'], fx.launch['path'])}
            roots = (c['out'], os.path.realpath(c['base']))
            other = sorted({p for p in log if os.path.realpath(p) not in allowed_files
                            and not any(os.path.realpath(p).startswith(r + os.sep) for r in roots)
                            and not os.path.realpath(p).startswith(sys.prefix) and '/site-packages/' not in p
                            and not os.path.realpath(p).startswith(os.path.realpath(sys.base_prefix))})
            ok = (a1['admitted'] and a2['admitted'] and a3['admitted'] and not other and len(GUARD['blocked']) == n0 and log)
            return ok, {'opens': len(log), 'outside_allowed': other[:10], 'admitted': [a1['admitted'], a2['admitted'], a3['admitted']]}

        def r05(self):
            """The production toolkit: its pins are the driver's (writer b9247b1a -> prep 8681da84 and controller c5bdd055 read
            from the writer bytes; checkpoint module 069b3935, binding aee7af12 and driver 577f8c94 as in the driver bytes);
            on a synthetic call it refuses at the call-driver check before any module is loaded (nothing refused by the guard)."""
            Rm = load(self.paths['RECIPES'], 'r05_recipes', self.shas['RECIPES'])
            mw = Rm.load_exact(Rm.MANIFEST_WRITER[0], Rm.MANIFEST_WRITER[1], 'r05_mw')
            tk = Rm.ProductionToolkit()
            with open(DRIVER[0], 'rb') as f:
                draw = f.read()
            dtext = draw.decode()
            c = self.rfx.make_call('r05')
            tg, _ = self.rfx.route_a_targets(c)
            n0 = len(GUARD['blocked'])
            code, detail = self.rfx.direct(c, tg[0], toolkit=tk)
            d2 = os.path.join(c['base'], 's5_r05')
            os.makedirs(d2)
            prod = {'path': self.paths['RECIPES'], 'sha256': self.shas['RECIPES']}
            adm = read_json(self.S.rebuild_admit(call_dir=c['call_dir'], target=tg[0], recipe_ref=prod,
                                                 approved_recipe_sha256=[prod['sha256']], out_dir=d2, driver_sha256=self.rfx.driver_sha))
            aux = "'checkpoint_module': (EX / 'resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py', '%s')" % Rm.CHECKPOINT_MODULE_SHA256
            ok = (sha_bytes(draw) == DRIVER[1] == Rm.DRIVER_SHA256 == tk.driver_sha256
                  and tk.prep_pin(mw)[1] == '8681da84bbd2b6858f5334d724b4e22e10c191e68f305b6e29df841571bf712b'
                  and mw.PINS['controller'][1] == Rm.CONTROLLER_SHA256 and aux in dtext
                  and ("'manifest_writer': ('%s', '%s')" % tuple(Rm.MANIFEST_WRITER)) in dtext
                  and ("'route_b_binding': ('%s', '%s')" % tuple(Rm.ROUTE_B_BINDING)) in dtext
                  and code == 'RECIPE_CALL_NOT_BOUND' and adm['admitted'] is False and adm['codes'] == ['S5_RECIPE_FAILED']
                  and 'RECIPE_CALL_NOT_BOUND' in ' '.join(adm['detail']) and len(GUARD['blocked']) == n0)
            return ok, {'direct': code, 's5': adm['codes'], 'prep_pin': tk.prep_pin(mw)[1][:12]}

        # ======================================================================== c2v004 MUST_FAIL
        def f43(self):
            """Verifier note 3 (a): out/start.json must bind the call's driver and call spec (execution fact fresh_call);
            a start.json naming another driver sha, or another call spec sha, refuses before the inventory."""
            out = {}
            for v in ('driver', 'spec'):
                c = self.fx.make_call('f43_' + v, exec='no_start')
                res = read_json(c['result'])
                put_json(os.path.join(c['out'], 'start.json'), {
                    'schema': 'synthetic start', 'driver_sha256': ('3' * 64) if v == 'driver' else res['driver_sha256'],
                    'call_spec_sha256': ('4' * 64) if v == 'spec' else res['call_spec_sha256']})
                rec, _ = self.handoff(c, policy=self.policy(c, prep=False), tag='handoff_start_' + v)
                ex = rec['execution'] or {}
                out[v] = (rec['reading'] == 'INCOMPLETE' and ex.get('fresh_call') is False
                          and any('EXECUTION_FACTS_REFUSE' in b and 'fresh_call=False' in b for b in rec['blockers'])
                          and 'inventory' not in rec and ex['basis'].get('start_present') is True, ex.get('fresh_call'))
            return all(x[0] for x in out.values()), out

        def f44(self):
            """Verifier note 3 (b): the W-1 point-pin check on the S5-exported TailState (record.eps_certificate = the point
            certificate) is reached past the stage-finish check: a finish whose config names the point certificate while the
            state ran with another certificate reads UNAVAILABLE TAIL_STATE_DID_NOT_RUN_WITH_THE_POINT_CERTIFICATE."""
            H = self.H
            c = self.fx.make_call('f44', cert_eps_scale=2.0)                        # states and finish ran with certificate B
            pr = self.prep(c)
            point_cert = self.fx.certs[c['point']]                                    # A: the point's own certificate
            result = read_json(c['result'])
            inv = self.E.enumerate_call(c['call_dir'], route_a_iterates_ref=pr['route_a_iterates'],
                                        approved_iterate_producer_sha256=[self.shas['R']], driver_sha256=self.fx.registry['driver']['sha256'])
            fp = result['passes'][-1]
            old = os.path.join(fp['rotation'], 'finish.json')
            fin = read_json(old)
            cfgA = self.fx.cfg(point_cert)
            forged = copy.deepcopy(fin)
            forged['uv_tail']['config'] = cfgA                                        # finish config names A ...
            assert forged['uv_tail']['config_sha256'] == c['cfg']['sha256'] != cfgA['sha256']   # ... its config sha stays B's
            new_rot = os.path.join(c['out'], 'stages', '21_le3_rotation', 'rotation')
            fpin = put_json(os.path.join(new_rot, 'finish.json'), forged)
            res2 = copy.deepcopy(result)
            res2['passes'][-1]['rotation'] = new_rot
            for e in res2['uv_tail']['stage_records']:
                if e['stage'] == 'le3_rotation':
                    e['finish_sha256'] = fpin['sha256']
            store = H.Store(os.path.join(c['base'], 'f44_records'))
            si = {d: dict(p) for d, p in pr['rebuild_exports'].items()}
            out = {}
            st = H.srb_rot_report(store=store, out=c['out'], result=res2, inv=inv, spec=read_json(c['spec_ref']), cert_ref=point_cert,
                                  state_inputs=si, lib=self.U, rowmod=self.rowmod)
            out['past_stage_finish_check'] = (st['status'] == 'UNAVAILABLE' and 'TAIL_STATE_DID_NOT_RUN_WITH_THE_POINT_CERTIFICATE'
                                              in str(st['code']) and st['report'] is None and st['gates'] is False, st['code'])
            st2 = H.srb_rot_report(store=store, out=c['out'], result=result, inv=inv, spec=read_json(c['spec_ref']), cert_ref=point_cert,
                                   state_inputs=si, lib=self.U, rowmod=self.rowmod)
            out['control_stage_finish_check'] = ('STAGE_EPS_PIN_NOT_THE_POINT_CERTIFICATE' in str(st2['code']), st2['code'])
            return all(x[0] for x in out.values()), out

        def f45(self):
            """A177 at accept: an S5 export whose admission names a recipe other than the approved source is dropped
            (REBUILD_EXPORT_REFUSED ... S5_ADMISSION_RECIPE_IS_NOT_THE_APPROVED_RECIPE_SOURCE) and the call reads INCOMPLETE;
            under the REGISTERED registry the approvals must be the module constants."""
            H = self.H
            c = self.fx.make_call('f45')
            pr = self.prep(c)
            other = dict(self.fx.raising_recipe)
            rec, _ = self.handoff(c, policy=self.policy(c, prep=pr), tag='handoff_other_recipe',
                                  approvals={'reader': dict(H.ITERATE_READER), 's5': dict(H.S5_TOOL), 'recipes': other})
            out = {'other_recipe': (rec['reading'] == 'INCOMPLETE' and sum('S5_ADMISSION_RECIPE_IS_NOT_THE_APPROVED_RECIPE_SOURCE' in b
                                                                           for b in rec['blockers']) == 3, rec['blockers'][:1])}
            rec2, _ = self.handoff(c, policy=self.policy(c, prep=False), registry=self.A.real_registry(), s2=dict(H.S2_PINS),
                                   contract=dict(H.ROW_CONTRACT), tag='handoff_registered_recipes',
                                   approvals={'reader': dict(H.ITERATE_READER), 's5': dict(H.S5_TOOL), 'recipes': other})
            out['registered_non_constant_recipes'] = (rec2['reading'] == 'INCOMPLETE' and any(
                'READER_S5_OR_RECIPES_NOT_THE_PINNED_MODULES' in b for b in rec2['blockers']), rec2['blockers'][:1])
            return all(x[0] for x in out.values()), out

        def r11(self):
            """Wrong iteration: a target whose origin iteration is not the iteration whose state it names is refused."""
            c = self.rfx.make_call('r11')
            p = c['payloads']
            t = {'state': {'state_sha256': p[1]['state_digest'], 'source_sha256': None, 'stage_kind': 'route_a'},
                 'origin': {'kind': 'ROUTE_A_ITERATE', 'iteration': 0, 'role': CURRENT}}
            code, why = self.rfx.direct(c, t)
            a, _ = self.rfx.admit(c, t, 'r11')
            t2 = dict(t, origin={'kind': 'ROUTE_A_ITERATE', 'iteration': 5, 'role': CURRENT})
            code2, _ = self.rfx.direct(c, t2)
            ok = (code == 'ROUTE_A_TARGET_NOT_THE_ITERATE_STATE' and a['admitted'] is False and a['codes'] == ['S5_RECIPE_FAILED']
                  and code2 == 'ROUTE_A_TARGET_ITERATION_OUT_OF_RANGE')
            return ok, {'direct': code, 's5': a['codes'], 'out_of_range': code2}

        def r12(self):
            """Missing sidecar element: elements_0000.npz absent from the sidecar (the controller wrote it elsewhere); the
            state of iteration 1 needs it and is refused (the reader also refuses the sidecar)."""
            c = self.rfx.make_call('r12', drop_element=True)
            p = c['payloads']
            t = {'state': {'state_sha256': p[1]['state_digest'], 'source_sha256': None, 'stage_kind': 'route_a'},
                 'origin': {'kind': 'ROUTE_A_ITERATE', 'iteration': 1, 'role': CURRENT}}
            code, why = self.rfx.direct(c, t)
            a, _ = self.rfx.admit(c, t, 'r12')
            reader, _ = self.refused(lambda: self.R.enumerate_sidecar(c['call_dir'], driver_sha256=self.rfx.driver_sha), self.R.Refusal)
            ok = code == 'ROUTE_A_SIDECAR_ELEMENT_MISSING' and a['admitted'] is False and reader
            return ok, {'direct': code, 's5': a['codes'], 'reader_refuses': reader}

        def r13(self):
            """Swapped kind: a route-B target naming another kind's state or stage kind, a stage whose ctx kind is swapped,
            and a route-B recipe called on another kind's stage are refused; inherited kinds are never rebuilt."""
            Rm = load(self.paths['RECIPES'], 'r13_recipes', self.shas['RECIPES'])
            c = self.rfx.make_call('r13')
            tg, _ = self.rfx.route_b_targets(c)
            by = {t['origin']['stage']: t for t in tg}
            out = {}
            t = {'state': dict(by['fs_rotation']['state']), 'origin': {'kind': 'ROUTE_B_STAGE', 'stage': 'fs_columns_00'}}
            out['target_kind_swapped'] = self.rfx.direct(c, t)[0] == 'ROUTE_B_STAGE_KIND_MISMATCH'
            t = {'state': dict(by['fs_rotation']['state'], stage_kind='fs_columns'), 'origin': {'kind': 'ROUTE_B_STAGE', 'stage': 'fs_columns_00'}}
            out['target_state_swapped'] = self.rfx.direct(c, t)[0] == 'ROUTE_B_TARGET_NOT_THE_STAGE_STATE'
            T_ = load(self.rfx.toolkit_pin['path'], 'r13_toolkit', self.rfx.toolkit_pin['sha256'])
            try:
                Rm.RECIPE_ROUTE_B_le_columns(call_dir=c['call_dir'], out_dir=c['out'], result=read_json(c['result']),
                                             target=by['le1_rotation'], lib=self.S.libraries()[0], provider=self.S.libraries()[1],
                                             toolkit=T_.SyntheticToolkit(Rm))
                out['recipe_of_other_kind'] = False
            except Rm.RecipeRefusal as exc:
                out['recipe_of_other_kind'] = exc.code == 'ROUTE_B_STAGE_KIND_MISMATCH'
            t = {'state': {'state_sha256': c['accepted'], 'source_sha256': None, 'stage_kind': 'reference'},
                 'origin': {'kind': 'ROUTE_B_STAGE', 'stage': 'reference'}}
            out['inherited_never_rebuilt'] = self.rfx.direct(c, t)[0] == 'ROUTE_B_KIND_NOT_REBUILT'
            c2 = self.rfx.make_call('r13_swapped_ctx', swap_kind=True)
            fin = c2['finishes']['fs_columns_00']['uv_tail']
            t = {'state': {'state_sha256': fin['state_digest'], 'source_sha256': fin['roster_digest'], 'stage_kind': 'fs_columns'},
                 'origin': {'kind': 'ROUTE_B_STAGE', 'stage': 'fs_columns_00'}}
            a, _ = self.rfx.admit(c2, t, 'r13_swapped')
            out['ctx_kind_swapped'] = (self.rfx.direct(c2, t)[0] == 'ROUTE_B_STAGE_KIND_MISMATCH' and a['admitted'] is False)
            return all(out.values()), out

        def r14(self):
            """Edited checkpoint gas (iteration 1): file bytes off its START ref, a re-pinned START whose COMPLETED does not
            bind it, a fully consistent forgery (the I1-T against the sidecar roster refuses it) and a consistent forgery
            inside the I1-T tolerance (its I1-T record is not the recorded one) are each refused."""
            out = {}
            want = {'bytes': 'ROUTE_A_CHECKPOINT_GAS_UNREADABLE', 'repinned': 'ROUTE_A_CHECKPOINT_RECORDS_DISAGREE',
                    'forged': 'ROUTE_A_I1T_REFUSED', 'tiny': 'ROUTE_A_I1T_NOT_THE_RECORDED_I1T'}
            for v, code in want.items():
                c = self.rfx.make_call('r14_' + v, gas_edit=v)
                tg, _ = self.rfx.route_a_targets(c)
                t = [x for x in tg if x['origin'] == {'kind': 'ROUTE_A_ITERATE', 'iteration': 0, 'role': NEXT}][0]
                got, why = self.rfx.direct(c, t)
                a, _ = self.rfx.admit(c, t, 'r14_' + v)
                out[v] = (got == code and a['admitted'] is False, got)
            return all(x[0] for x in out.values()), out

        def r15(self):
            """Missing updated_a: the monitor-next state of the accepted iteration (gas_{a+1} unrecorded) and a broken-chain
            monitor-next state are refused with ROUTE_A_MONITOR_NEXT_GAS_UNRECORDED; through the handoff c2v004
            prepare_acceptance_inputs the call then has no iterate list (ROUTE_A_ITERATE_SOURCE_UNESTABLISHED)."""
            out = {}
            c = self.rfx.make_call('r15')
            tg, _ = self.rfx.route_a_targets(c)
            t = [x for x in tg if x['origin'] == {'kind': 'ROUTE_A_ITERATE', 'iteration': c['a'], 'role': NEXT}][0]
            out['accepted_next_direct'] = self.rfx.direct(c, t)[0] == 'ROUTE_A_MONITOR_NEXT_GAS_UNRECORDED'
            c2 = self.rfx.make_call('r15_chain', chain_break=True)
            tg2, _ = self.rfx.route_a_targets(c2)
            t2 = [x for x in tg2 if x['origin'] == {'kind': 'ROUTE_A_ITERATE', 'iteration': 0, 'role': NEXT}][0]
            out['broken_chain_next_direct'] = self.rfx.direct(c2, t2)[0] == 'ROUTE_A_MONITOR_NEXT_GAS_UNRECORDED'
            H = self.H
            try:
                H.prepare_acceptance_inputs(call_dir=c['call_dir'], out_dir=os.path.join(c['base'], 'prep_chain'),
                                            recipe_ref=self.rfx.wrapper, approved_recipe_sha256=[self.rfx.wrapper['sha256']],
                                            driver_sha256=self.rfx.driver_sha, modules=(self.E, self.A, self.R, self.S))
                out['chain'] = False
            except self.R.Refusal as exc:
                adms = [read_json(os.path.join(c['base'], 'prep_chain', f)) for f in sorted(os.listdir(os.path.join(c['base'], 'prep_chain')))
                        if f.startswith('S5_ADMISSION_')]
                out['chain'] = (exc.code == 'ROUTE_A_ITERATE_SOURCE_UNESTABLISHED' and len(adms) == 3
                                and sorted(a['admitted'] for a in adms) == [False, True, True]
                                and any('ROUTE_A_MONITOR_NEXT_GAS_UNRECORDED' in ' '.join(a['detail']) for a in adms))
            return all(out.values()), out

        def r16(self):
            """Prep patch dropped: the manifest stage request records no module patch while the call ran the patched prep;
            the rebuilt controller identity differs from SIDECAR_IDENTITY and the recipe refuses."""
            c = self.rfx.make_call('r16', drop_patch=True)
            tg, _ = self.rfx.route_a_targets(c)
            code, why = self.rfx.direct(c, tg[0])
            return code == 'ROUTE_A_CONTROLLER_IDENTITY_DIFFERS', {'code': code, 'why': why}

        def r17(self):
            """A DECLARED route-B input that is not the stage's: the offset outputs pin an edited updated_base_arrays; the
            fs roster differs from the recorded roster digest and S5 refuses before any build."""
            c = self.rfx.make_call('r17', base_edit=True)
            tg, _ = self.rfx.route_b_targets(c)
            t = [x for x in tg if x['origin']['stage'] == 'fs_columns_00'][0]
            a, _ = self.rfx.admit(c, t, 'r17')
            return (a['admitted'] is False and a['codes'] == ['S5_ROSTER_NOT_THE_RECORDED_ROSTER'] and a['roster']['equal'] is False), a['codes']

        def r18(self):
            """A DECLARED build argument that is not the stage's: the fs_columns stage ran at gamma one ulp off the accepted
            state's gamma_eff; the roster is the recorded one but the rebuilt TailState digest differs (not admitted)."""
            c = self.rfx.make_call('r18', route_b_gamma_ulp=True)
            tg, _ = self.rfx.route_b_targets(c)
            t = [x for x in tg if x['origin']['stage'] == 'fs_columns_00'][0]
            a, _ = self.rfx.admit(c, t, 'r18')
            return (a['admitted'] is False and a['codes'] == ['S5_REBUILD_DIGEST_MISMATCH'] and a['roster']['equal'] is True), a['codes']

        def r20(self):
            """A manifest stage not run by the recipe-bound writer b9247b1a (another writer sha, e.g. the STAGE0 writer
            443d9fdc) is refused before any module is loaded."""
            c = self.rfx.make_call('r20', writer_sha=True)
            tg, _ = self.rfx.route_a_targets(c)
            code, why = self.rfx.direct(c, tg[0])
            return code == 'ROUTE_A_MANIFEST_WRITER_NOT_RECIPE_BOUND', code

        def r19(self):
            """A route-B stage record not written by the pinned binding (binding_sha256) is refused."""
            c = self.rfx.make_call('r19', binding_sha=True)
            fin = c['finishes']['fs_rotation']['uv_tail']
            t = {'state': {'state_sha256': fin['state_digest'], 'source_sha256': fin['roster_digest'], 'stage_kind': 'fs_rotation'},
                 'origin': {'kind': 'ROUTE_B_STAGE', 'stage': 'fs_rotation'}}
            code, _ = self.rfx.direct(c, t)
            return code == 'ROUTE_B_BINDING_NOT_THE_PINNED_BINDING', code

        def all(self):
            P, F = T.Suite.all(self)
            P2 = [('P36', 'A177 handoff c2v004 pins the recipe module as the approved-recipe source', self.p36),
                  ('R01', 'A177 route A: real recipe + S5 ADMIT every non-accepted iterate except monitor-next', self.r01),
                  ('R02', 'A177 route B: each RECIPE_ROUTE_B_<kind> reproduces the recorded roster; S5 ADMITTED', self.r02),
                  ('R03', 'A177 route A broken chain: iteration 1 begun state rebuilt from START(1), ADMITTED', self.r03),
                  ('R04', 'A177 custody: the recipe opens only own outputs, pinned modules, seed pins, certificates', self.r04),
                  ('R05', 'A177 production toolkit pins from bytes; refuses a synthetic call before loading modules', self.r05)]
            F2 = [('F43', 'note 3a: start.json driver_sha256 / call_spec_sha256 not this call refuses (fresh_call False)', self.f43),
                  ('F44', 'note 3b: W-1 point-pin check on the exported TailState reached past the stage-finish check', self.f44),
                  ('F45', 'A177 accept: an export admitted under another recipe dropped; REGISTERED recipes constant', self.f45),
                  ('R11', 'A177 wrong iteration (and out of range)', self.r11),
                  ('R12', 'A177 missing sidecar element', self.r12),
                  ('R13', 'A177 swapped kind (target, ctx record, recipe of another kind); inherited kinds', self.r13),
                  ('R14', 'A177 edited checkpoint gas (bytes, re-pinned, consistent forgery, in-tolerance forgery)', self.r14),
                  ('R15', 'A177 missing updated_a: monitor-next refused; prepare chain ROUTE_A_ITERATE_SOURCE_UNESTABLISHED', self.r15),
                  ('R16', 'A177 prep patch dropped: controller identity differs', self.r16),
                  ('R17', 'A177 DECLARED route-B input not the stage one: roster digest refusal before build', self.r17),
                  ('R18', 'A177 DECLARED gamma not the stage one: TailState digest mismatch', self.r18),
                  ('R19', 'A177 stage record not written by the pinned binding', self.r19),
                  ('R20', 'A177 manifest stage not run by the recipe-bound writer', self.r20)]
            for rid, name, fn in P2:
                self.run(rid + ' ' + name, 'MUST_PASS', fn)
            for rid, name, fn in F2:
                self.run(rid + ' ' + name, 'MUST_FAIL', fn)
            return P + P2, F + F2
    return Suite4


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--module-dir', default=os.path.dirname(os.path.realpath(__file__)))
    ap.add_argument('--only', default=None, help='dev: comma-separated test ids')
    a = ap.parse_args(argv)
    for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS',
              'BLIS_NUM_THREADS'):
        os.environ[k] = '1'
    sys.addaudithook(_audit)
    run_dir = os.path.realpath(a.run_dir)
    os.mkdir(run_dir)
    module_dir = os.path.realpath(a.module_dir)
    t0 = time.monotonic()
    T = load(os.path.join(module_dir, PREV_SUITE[0]), 'suite_c2v003a_port', PREV_SUITE[1])
    T.NAMES = dict(T.NAMES, H=HANDOFF_NAME)
    s = make_suite_class(T)(run_dir, module_dir)
    if a.only:
        want = set(a.only.split(','))
        orig = s.run
        s.run = lambda rid, kind, fn: orig(rid, kind, fn) if rid.split()[0] in want else None
    s.all()
    run = [r for r in s.results if r['ok'] is not None]
    mp = [r for r in run if r['kind'] == 'MUST_PASS']
    mf = [r for r in run if r['kind'] == 'MUST_FAIL']
    blocked = [r for r in s.results if r['ok'] is None]
    out = {'schema': 'NGC_ACCEPTANCE_C2V004_SUITE_RESULTS', 'synthetic_only': True, 'module_shas': s.shas,
           'ported_suite': {'path': os.path.join(module_dir, PREV_SUITE[0]), 'sha256': PREV_SUITE[1]},
           'library_sha256': s.A.LIBRARY[1], 'handoff_pins': {'iterate_reader': s.H.ITERATE_READER, 's5_tool': s.H.S5_TOOL,
                                                            'row_contract': s.H.ROW_CONTRACT, 's2': s.H.S2_PINS,
                                                            'roster_recipes': s.H.ROSTER_RECIPES, 'lo_adapter': s.H.LO_ADAPTER},
           'recipe_fixture': {'roster_module': s.rfx.rs_pin, 'checkpoint_module': s.rfx.cm_pin, 'prep': s.rfx.prep_pin,
                              'toolkit': s.rfx.toolkit_pin, 'wrapper': s.rfx.wrapper},
           'art_patched_for_dev_run': s.art_patched, 'python': sys.version.split()[0],
           'flags': {'isolated': sys.flags.isolated, 'dont_write_bytecode': sys.flags.dont_write_bytecode}, 'only': a.only,
           'must_pass': '%d/%d' % (sum(bool(r['ok']) for r in mp), len(mp)),
           'must_fail': '%d/%d' % (sum(bool(r['ok']) for r in mf), len(mf)),
           'blocked_by_hard_rule': [r['id'].split()[0] for r in blocked],
           'guard': {'deny': 'NGC3198-named paths; non-named code under %s except %s' % (list(DENY_PREFIXES), sorted(DENY_ALLOW)),
                     'refused_opens': sorted(set(GUARD['blocked']))},
           'results': s.results, 'seconds': round(time.monotonic() - t0, 3)}
    pin = put_json(os.path.join(run_dir, 'SUITE_RESULTS_C2V004.json'), out)
    print(json.dumps({'must_pass': out['must_pass'], 'must_fail': out['must_fail'], 'blocked': out['blocked_by_hard_rule'],
                      'results': pin, 'failed': [r['id'] for r in run if not r['ok']]}))
    return 0 if all(r['ok'] for r in run) else 1


if __name__ == '__main__':
    sys.exit(main())
