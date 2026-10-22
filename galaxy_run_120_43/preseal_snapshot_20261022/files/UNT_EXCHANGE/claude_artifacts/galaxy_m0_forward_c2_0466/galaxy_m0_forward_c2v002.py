"""INERT parameterized clean m=0 ("route B") forward driver, Claude2 lane, dispatch 0466 (c2v002).

c2v002 = c2v001 + an NGC3198 configuration (NGC3198 section at the end of this file and
INTERFACE_C2_0466_V002.md).  DDO154 behaviour is unchanged: every DDO code path is the c2v001
code; the only DDO-visible addition is the OPTIONAL numerics.k_domain check (absent = c2v001).
NGC3198 calls are normalized, pinned, seeded and planned, but `run` ends BLOCKED with zero
stages executed: the reviewed NGC43 route-A binding cannot open any existing checkpoint module
(it lacks the c2v003 caller contract), and no reviewed NGC route-B stage exists.

One call = one parameter point, read from a single JSON call spec.  Runs the full chain that
produced the saved DDO154 axisymmetric reference, reusing every reviewed stage script by
executing its exact pinned bytes (SHA256 verified from bytes) in a child process:

  route_a     ddo_composite_stable_cached_root_worker_v002 (+solver/checkpoint 0422)  -> G4 fixed point
  reference   ddo_homotopy_reference_root_worker_v001 (reference module V003)        -> 72-radius reference
  body        ddo_saved_root_body_array_root_v002                                    -> 72x16x8 body arrays
  offset      ddo_body_source_offset_root_v003                                       -> unit response, offset
  fs_*        ddo_fixed_K_free_surface_root_v001 / rotation_root_v001 / feedback_root_v002 (original K)
  rfs_columns ddo_fixed_K_free_surface_root_v003 (original K, refreshed field; bracket source only)
  le{p}_*     ddo_fixed_K_free_surface_root_v005 / rotation_root_v005 / feedback_root_v004 (scaled K)
  le{P}_column_mean  ddo12_lower_entropy_column_mean_root_v004                         -> 12 rows

No equation, tolerance or guard of any stage is changed.  The ONLY substitutions are module
globals that hard-code the identity of one historical run (seed SHA, checkpoint identity,
offset finish SHA, reference-run pins, column-mean input pins, coefficient-grid pin).  They
are replaced by per-call values computed from bytes of this call's own (or explicitly
admitted, re-verified) upstream outputs.  Optional truncation shapes 'sphere'/'cylinder'
are a declared NUMERICAL CHOICE implemented only as a 0/1 weight mask on the existing
composite grid (see truncation_mask and INTERFACE_C2_0466_V001.md).

Importing this module does nothing.  CLI:
  run      --spec SPEC.json --outdir NEW_DIR      (outdir must be absent; never retries)
  dry-run  --spec SPEC.json --report-dir NEW_DIR  (pins, JSON/NPZ headers, planned stage calls;
                                                   no stage is executed)
  _stage   REQUEST.json                           (internal: one stage in this process)
"""
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path

SCHEMA = 'UNT_GALAXY_M0_FORWARD_CALL_C2V001'
RESULT_SCHEMA = 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
ROOT = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
HC = ROOT / 'helpers/coefficient_method'
HR = ROOT / 'helpers/recovered_packet_audit'
C1 = ROOT / 'CODEX1'
HP = ROOT / 'helpers/response_packet_audit'
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
KPC_M = 3.085677581491367e19  # identical to seed numerical_inputs.kpc_m (checked at run time)
THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')

# Reviewed stage scripts (exact versions used by the saved chain).
SCRIPTS = {
    'route_a': (HR / 'ddo_composite_stable_cached_root_worker_v002.py', 'c4cb682669993afbad3c623a010244cc8a31b9fcbacfe44e6bc692bf2d5895a4'),
    'reference': (HR / 'ddo_homotopy_reference_root_worker_v001.py', 'acda989d375925bf9a8163d8d8a3a22c3f183b6b253c8137312bccc0cefbbe36'),
    'body': (HC / 'ddo_saved_root_body_array_root_v002.py', '271e5612caf00cbde3a154d6deb4c7c4d5c7ec342b9ede893e0bf820d044a8f6'),
    'offset': (HC / 'ddo_body_source_offset_root_v003.py', 'c5faed578e8e9b6e60b2c0309049232ed11c634347cf80570f939764df6620b1'),
    'columns_v001': (HC / 'ddo_fixed_K_free_surface_root_v001.py', '399720adc6eb1836a15e147ccd395a5a9346e9fc2a49db8f2c41bb1c2f5dc347'),
    'rotation_v001': (HC / 'ddo_free_surface_rotation_root_v001.py', '3df32880972a4cd94cac6072a106ef94cacaa8a1a1de52f7f3872692e7efbfc2'),
    'feedback_v002': (HC / 'ddo_free_surface_native_feedback_root_v002.py', '44376116d64825ce5319e402a47c138e5e69303a6482d3ebc54abee8291ae1fd'),
    'columns_v003': (HC / 'ddo_fixed_K_free_surface_root_v003.py', 'c9e2c2ecb6dd7d388cb9cb8658f5330d0d7cab48abde8de1c82b91f326dde1f9'),
    'columns_v005': (HC / 'ddo_fixed_K_free_surface_root_v005.py', '8a9b2ec1eaba3661b8e5d11cca66b7761efcb0bd0dab4a53987b222b242cda96'),
    'rotation_v005': (HC / 'ddo_free_surface_rotation_root_v005.py', '1b42990556ee34d30a7a12eb5b5605aa1e43aa8322e03d73bbab86e5c38497b7'),
    'feedback_v004': (HC / 'ddo_free_surface_native_feedback_root_v004.py', '6da11133734e65fe31b6408d4f64d0e50df9f453c8872308b960678d80ec02ed'),
    'column_mean_v004': (HC / 'ddo12_lower_entropy_column_mean_root_v004.py', '12504c4b86c31e20d0e019868c406f22c35a568e3ad25ee39a9db8ddabfda3c2'),
}
AUX = {
    'solver': (EX / 'resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py', '44d9c23c47d6beb52b7539802fcf0f284c1a2c7eea7662536f04b184523e3644'),
    'checkpoint_module': (EX / 'resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py', '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114'),
    'reference_module': (HC / 'owned_axisymmetric_homotopy_reference_v003.py', '81a04b1241c1004f8766f68d22f9c586824ae3b3cbe32ca36243a2d3da387128'),
    'prep': (HC / 'ddo_actual_initial_source_preparation_v007.py', 'ac905597b1aa06da3a0178bfa629f6256b78cc87e8b1b05fcea22b3f6df25a42'),
    'cache': (HR / 'owned_scalar_lapse_inverse_cache_v001.py', '7b9816aea218d638c2eece184df22e29ca18b68547f3d04193780c2eff96a529'),
}
# Reviewed fixed stage arguments (not parameters).
FIXED_ARGS = {'wave_batch': '256', 'position_batch': '512', 'bessel_cache_entries': '500000',
              'mass_relative_tolerance': '1.1e-8'}

_ORIG = 'DDO154_'
GALAXIES = {
    'DDO154': {
        'supported': True,
        'base_seed': (C1 / 'DDO154_STABLE_CACHED_COUPLED_TRIAL_SEED_V002.json', '694eaaaab38547a369ac85c3c3d0b5550d8878753ccafe7bc0e5cdcb79be6680'),
        'profile': (C1 / 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json', 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'),
        'monotone_source': (C1 / 'DDO154_MONOTONE_SOURCE_RECONSTRUCTION_RUN_V001/source.json', '1dbf2b687b8ef2747091557f3a92ebd4995409f326ec21df816f6c7397c11be2'),
        'column_mean_binding': (C1 / 'DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json', 'f42c7c657cd9b8bcef6b88e980918ff2570b1fc0a5480784d8bf3b8bb2a3c600'),
        'solver_template': (C1 / 'DDO154_REMAINING_FREE_SURFACE_CONTROLS_V001.json', '5d69360f24fc1c943bdec1b24b2a1dd6e22670375118f344c4e66231df002d16'),
        'default_coefficients': (C1 / 'PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz', 'fe5a2f065dec8f120c573eeeb6edc0a24a945d2a0fd70e3f29a66cb986e53e4f'),
        'registered_geometry': {'distance_Mpc': 4.04, 'inclination_deg': 66.0, 'released_inclination_deg': 64.0,
                                'HI_original_distance_Mpc': 4.3},
        'n_columns': 72, 'n_queries': 12,
        'default_entropy_K_factor': 64 / 121,
        # Controls used by the saved chain, in the saved run order (reproduction, mode pinned_controls).
        'saved_controls': {
            'fs': [(C1 / 'DDO154_OUTER_FREE_SURFACE_CONTROLS_V001.json', 'f9f07c0ef0709c226b3346ecf38aedb3e3342ae7a4ed71d7f4018f40ff994dae'),
                   (C1 / 'DDO154_REMAINING_FREE_SURFACE_CONTROLS_V001.json', '5d69360f24fc1c943bdec1b24b2a1dd6e22670375118f344c4e66231df002d16'),
                   (C1 / 'DDO154_FREE_SURFACE_BRACKET_CORRECTION_CONTROLS_V001.json', '7719e7d8e35501fb1277973ddc53b3d75655646aaa60fc0705d32e891bc00f31')],
            'rfs': [(C1 / 'DDO154_REFRESHED_FREE_SURFACE_CONTROLS_V001.json', 'db835b143f735d9ebae74d28c99bfbd7e2f392b1554f78ed2e60a73989bb03ef'),
                    (C1 / 'DDO154_REFRESHED_OUTER_BRACKET_CORRECTION_CONTROLS_V001.json', '87eef1fd7454879e13ef05eb96ea9d727f8b3daa2a736efc1bae15132189c5ad')],
            'le': [[(C1 / 'DDO154_LOWER_ENTROPY_FREE_SURFACE_CONTROLS_V001.json', 'c2f8b434c0de06cf8bfeef0f202e8a8140c33a4b140dbf1a75ebffc4e83b4938')],
                   [(C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_CONTROLS_V001.json', '24f404e64b4c514c9bd331ba711426faa53d5d77e3dfa3bf222a4d88262ff4b0')],
                   [(C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_CONTROLS_V002.json', '7a4ac8e216ea71f3aee2db774a09fcc13089535f7206ffbf0d4ba41d2a73e54c')]]},
        # Saved run outputs of the chain (reproduction map; read-only).
        'saved_runs': {
            'route_a': {'attempt': C1 / 'DDO154_STABLE_CACHED_COUPLED_RUN_V002/attempt_000', 'checkpoint': C1 / 'DDO154_STABLE_CACHED_COUPLED_RUN_V002/checkpoint'},
            'reference': C1 / 'DDO154_NONCIRCULAR_REFERENCE_RUN_V001/reference',
            'body': C1 / 'DDO154_NORMALIZED_BODY_ARRAY_RUN_V001/body',
            'offset': C1 / 'DDO154_BODY_SOURCE_OFFSET_RUN_V001/offset',
            'fs_columns': [C1 / 'DDO154_OUTER_FREE_SURFACE_RUN_V001/columns', C1 / 'DDO154_REMAINING_FREE_SURFACE_RUN_V001/columns', C1 / 'DDO154_FREE_SURFACE_BRACKET_CORRECTION_RUN_V001/columns'],
            'fs_rotation': C1 / 'DDO154_FREE_SURFACE_ROTATION_RUN_V001/rotation',
            'fs_feedback': C1 / 'DDO154_FREE_SURFACE_NATIVE_FEEDBACK_RUN_V001/feedback',
            'rfs_columns': [C1 / 'DDO154_REFRESHED_FREE_SURFACE_RUN_V001/columns', C1 / 'DDO154_REFRESHED_OUTER_BRACKET_CORRECTION_RUN_V001/columns'],
            'le1_columns': [C1 / 'DDO154_LOWER_ENTROPY_FREE_SURFACE_RUN_V001/columns'],
            'le1_rotation': C1 / 'DDO154_LOWER_ENTROPY_ROTATION_RUN_V001/rotation',
            'le1_feedback': C1 / 'DDO154_LOWER_ENTROPY_NATIVE_FEEDBACK_RUN_V001/feedback',
            'le2_columns': [C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_COLUMNS_RUN_V001/columns'],
            'le2_rotation': C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_ROTATION_RUN_V001/rotation',
            'le2_feedback': C1 / 'DDO154_LOWER_ENTROPY_NATIVE_FEEDBACK_RUN_V002/feedback',
            'le3_columns': [C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_COLUMNS_RUN_V002/columns'],
            'le3_rotation': C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_ROTATION_RUN_V002/rotation',
            'le3_column_mean': C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_COLUMN_MEAN_RUN_V002/observation',
        },
        # The two manual bracket corrections of the saved chain, written as declared rule overrides.
        'repro_rule_overrides': {
            'fs_absolute_overrides': {str(i): [302500000.0, 317625000.0] for i in (5, 6, 7, 8, 9, 45, 46, 47, 48, 49, 50)},
            'rfs_factor_overrides': {'71': [0.8, 1.01]}},
        'saved_reference_speeds_km_s': [11.582165247926024, 21.882993578802893, 29.132298352542904, 34.53811554072339,
                                        38.18655701048106, 41.43604462412697, 44.62663756340822, 47.756836739826575,
                                        49.19289920475613, 49.39790797958474, 50.909676339988216, 48.65527268393767],
    },
    'NGC3198': {
        # c2v002: normalized by normalize_ngc_spec (NGC3198 section); route B stays unsupported.
        'supported': False,
        'config': 'NGC3198_C2V002',
        'registered_geometry': {'distance_Mpc': 13.8, 'inclination_deg': 72.0, 'released_inclination_deg': 73.0},
        'n_queries': 43,
        'default_coefficients': (C1 / 'PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz', 'fe5a2f065dec8f120c573eeeb6edc0a24a945d2a0fd70e3f29a66cb986e53e4f'),
        'blockers': [
            'Every reused route-B stage hard-codes the DDO154 geometry: 72 radial columns (body/offset reshape (72,16,8); '
            'columns/rotation require exactly 72; column mean requires 72 and a 32-node m0 geometry). NGC3198 has 51 HI bins x GL4.',
            'ddo_homotopy_reference_root_worker_v001 and ddo_body_source_offset_root_v003 read galaxies["DDO154"] of the profile.',
            'ddo_saved_root_body_array_root_v002 pins DDO154_NONCIRCULAR_REFERENCE_RUN_V001 and the DDO monotone source.',
            'ddo_free_surface_rotation_root_v001/v005 pin the DDO154 monotone source.json.',
            'ddo12_lower_entropy_column_mean_root_v004 pins a DDO154 12-row binding; no NGC 43-row column-mean binding exists.',
            'No NGC route-A seed exists; the only NGC worker (ngc43_composite_coupled_root_worker_v001) is the azimuth-resolved route.',
        ],
    },
}
LE_RULE_DEFAULTS = {'fs_absolute_overrides': {}, 'rfs_factors': [0.8, 1.2], 'rfs_factor_overrides': {},
                    'le_first_factors': [0.4, 0.9], 'le_next_factors': [0.8, 1.1], 'le_factor_overrides': {}}


# ----------------------------------------------------------------------------- small helpers
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _is_hex64(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s)


class Refusal(ValueError):
    pass


class StageFailed(RuntimeError):
    pass


class Blocked(RuntimeError):
    pass


def verify_pin(path, sha, label):
    p = Path(path)
    if not p.is_file():
        raise Refusal('%s missing: %s' % (label, p))
    actual = sha256_file(p)
    if actual != sha:
        raise Refusal('%s pin mismatch: %s expected %s actual %s' % (label, p, sha, actual))
    return actual


def exec_verified(path, sha, name):
    """Execute a pinned module from the exact bytes that were hashed (no reread)."""
    import types
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refusal('Pin mismatch on load: %s' % path)
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


def _jsonable(v):
    if isinstance(v, Path):
        return str(v)
    if isinstance(v, dict):
        return {str(k): _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    if hasattr(v, 'tolist'):
        return _jsonable(v.tolist())
    if isinstance(v, float) and not math.isfinite(v):
        return repr(v)
    return v


def _write_x(path, obj):
    with open(path, 'x') as f:
        json.dump(_jsonable(obj), f, indent=1, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    return sha256_file(path)


def single_thread_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    for k in THREAD_ENV:
        env[k] = '1'
    return env


# ----------------------------------------------------------------------------- truncation mask
def truncation_mask(k_physical, shape, kmax_inverse_m):
    """0/1 weight mask on the EXISTING composite grid nodes (numerical choice, not physics).
    cube: all ones (identity; the driver then installs no hook at all).
    sphere: keep |k| <= kmax.  cylinder: keep k_perp = sqrt(kx^2+ky^2) <= kmax (disk axis = chart z),
    all k_z of the cube kept.  Both masks are invariant under k -> -k, so real fields stay real.
    Zeroing a node's weight is exactly zeroing its weighted response row, because the reviewed
    prepare() forms weighted_response = dk_weight/(2pi)^3 * x_tilde node by node."""
    import numpy as np
    k = np.asarray(k_physical, dtype=float)
    if k.ndim != 2 or k.shape[1] != 3 or not np.isfinite(k).all():
        raise ValueError('k nodes (n,3) finite required')
    if shape == 'cube':
        return np.ones(len(k))
    if not (isinstance(kmax_inverse_m, float) and math.isfinite(kmax_inverse_m) and kmax_inverse_m > 0):
        raise ValueError('positive finite kmax required for a non-cube mask')
    if shape == 'sphere':
        r = np.sqrt(k[:, 0] * k[:, 0] + k[:, 1] * k[:, 1] + k[:, 2] * k[:, 2])
    elif shape == 'cylinder':
        r = np.sqrt(k[:, 0] * k[:, 0] + k[:, 1] * k[:, 1])
    else:
        raise ValueError('shape must be cube, sphere or cylinder')
    return (r <= kmax_inverse_m).astype(float)


def apply_mask(weighted_responses, mask):
    import numpy as np
    a = np.asarray(weighted_responses)
    if a.ndim < 1 or a.shape[0] != len(mask):
        raise ValueError('mask/packet length mismatch')
    return a * np.asarray(mask, dtype=float).reshape((len(mask),) + (1,) * (a.ndim - 1))


# ----------------------------------------------------------------------------- _stage shim
def _decode_value(v):
    if isinstance(v, dict) and len(v) == 1:
        (key, val), = v.items()
        if key == '__path__':
            return Path(val)
        if key == '__pathdict__':
            return {Path(p): s for p, s in val}
        if key == '__ordered__':
            return {p: s for p, s in val}
    return v


def _install_hooks(request):
    """Wrap importlib.util.spec_from_file_location so that the listed dependency modules get
    their identity globals replaced (after their own code ran) and, for a non-cube truncation,
    the mask wrappers.  Every patched file is re-verified from bytes."""
    import importlib.util
    patches = {str(Path(p['path']).resolve()): p for p in request.get('module_patches', [])}
    mask = request.get('mask')
    targets = dict(patches)
    if mask:
        for key in ('checkpoint_module', 'cache_module'):
            targets.setdefault(str(Path(mask[key][0]).resolve()), {'path': mask[key][0], 'sha256': mask[key][1], 'set': {}})
    original = importlib.util.spec_from_file_location

    class PatchedLoader:
        def __init__(self, inner, key):
            self.inner = inner
            self.key = key

        def create_module(self, spec):
            return self.inner.create_module(spec)

        def exec_module(self, module):
            patch = targets[self.key]
            if sha256_file(self.key) != patch['sha256']:
                raise ValueError('Patched dependency pin mismatch: ' + self.key)
            self.inner.exec_module(module)
            for name, value in patch.get('set', {}).items():
                if not hasattr(module, name):
                    raise ValueError('Override target absent: %s.%s' % (self.key, name))
                setattr(module, name, _decode_value(value))
            if mask and self.key == str(Path(mask['checkpoint_module'][0]).resolve()):
                _wrap_checkpoint_get(module, mask)
            if mask and self.key == str(Path(mask['cache_module'][0]).resolve()):
                _wrap_cache(module, mask)

    def hooked(name, location=None, *args, **kwargs):
        spec = original(name, location, *args, **kwargs)
        if spec is not None and location is not None:
            key = str(Path(location).resolve())
            if key in targets:
                spec.loader = PatchedLoader(spec.loader, key)
        return spec

    importlib.util.spec_from_file_location = hooked


def _wrap_checkpoint_get(module, mask):
    orig = module._get
    state = {}

    def _get(directory, ref):
        a = orig(directory, ref)
        if isinstance(ref, dict) and ref.get('file_sha256') == mask['g4_file_sha256']:
            if directory not in state:
                waves = orig(directory, mask['waves_ref'])
                state[directory] = truncation_mask(waves, mask['shape'], mask['kmax_inverse_m'])
            a = apply_mask(a, state[directory])
        return a
    module._get = _get


def _wrap_cache(module, mask):
    orig_make = module.make_fourier_module

    def make_fourier_module(**kw):
        inner = orig_make(**kw)
        orig_prepare = inner.prepare

        def prepare(**arguments):
            out = orig_prepare(**arguments)
            m = truncation_mask(arguments['k_physical'], mask['shape'], mask['kmax_inverse_m'])
            out = dict(out)
            out['weighted_responses'] = apply_mask(out['weighted_responses'], m)
            out['truncation_mask'] = {'shape': mask['shape'], 'kmax_inverse_m': mask['kmax_inverse_m'],
                                      'kept_nodes': int(m.sum()), 'total_nodes': int(len(m))}
            return out
        inner.prepare = prepare
        return inner
    module.make_fourier_module = make_fourier_module


def stage_main(request_path):
    request = json.loads(Path(request_path).read_text())
    script, sha = request['script'], request['script_sha256']
    _install_hooks(request)
    module = exec_verified(script, sha, 'c2v001_stage_' + Path(script).stem)
    for name, value in request.get('stage_globals', {}).items():
        if name not in module.__dict__:
            raise ValueError('Stage override target absent: ' + name)
        module.__dict__[name] = _decode_value(value)
    sys.argv = [script] + list(request['argv'])
    module.main()
    return 0


# ----------------------------------------------------------------------------- call spec
def _num(x, label, positive=True):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(float(x)):
        raise Refusal(label + ' must be a finite number')
    x = float(x)
    if positive and x <= 0:
        raise Refusal(label + ' must be > 0')
    return x


def _strict(d, allowed, label):
    if not isinstance(d, dict):
        raise Refusal(label + ' must be an object')
    extra = set(d) - set(allowed)
    if extra:
        raise Refusal('%s: unknown keys %s' % (label, sorted(extra)))


def normalize_spec(spec):
    if isinstance(spec, dict) and spec.get('schema') == NGC_SCHEMA:
        return normalize_ngc_spec(spec)  # c2v002 NGC3198 configuration (route A only; see NGC section)
    _strict(spec, ('schema', 'galaxy', 'label', 'physical', 'coefficients', 'numerics', 'admit', 'reference_compare'), 'spec')
    if spec.get('schema') != SCHEMA:
        raise Refusal('schema must be ' + SCHEMA)
    gname = spec.get('galaxy')
    if gname not in GALAXIES:
        raise Refusal('unknown galaxy %r' % gname)
    g = GALAXIES[gname]
    if not g['supported']:
        raise Refusal('galaxy %s UNSUPPORTED by the reused route-B stages: %s' % (gname, ' | '.join(g['blockers'])))
    phys = spec.get('physical', {})
    _strict(phys, ('Eref_J', 'ell_F_m', 'gamma', 'common_scale_s', 'entropy_K_factor', 'distance_Mpc', 'inclination_deg'), 'physical')
    out = {'schema': SCHEMA, 'galaxy': gname, 'label': spec.get('label', '')}
    p = {'Eref_J': _num(phys.get('Eref_J'), 'Eref_J'), 'ell_F_m': _num(phys.get('ell_F_m'), 'ell_F_m'),
         'gamma': _num(phys.get('gamma'), 'gamma'),  # static EH block requires net gamma > 0
         'common_scale_s': _num(phys.get('common_scale_s', 1.0), 'common_scale_s'),
         'entropy_K_factor': _num(phys.get('entropy_K_factor', g['default_entropy_K_factor']), 'entropy_K_factor'),
         'distance_Mpc': _num(phys.get('distance_Mpc', g['registered_geometry']['distance_Mpc']), 'distance_Mpc'),
         'inclination_deg': _num(phys.get('inclination_deg', g['registered_geometry']['inclination_deg']), 'inclination_deg')}
    geo = g['registered_geometry']
    if p['distance_Mpc'] != geo['distance_Mpc'] or p['inclination_deg'] != geo['inclination_deg']:
        raise Refusal('UNSUPPORTED geometry: only the registered distance %.2f Mpc and inclination %.0f deg are supported. '
                      'The D/4.3 radial scaling and cos66/cos64 stellar re-facing are baked into the pinned source JSON '
                      '(no code applies them) and the 12 query radii/sin66/sin64 map are fixed in the pinned binding.'
                      % (geo['distance_Mpc'], geo['inclination_deg']))
    out['physical'] = p
    coeff = spec.get('coefficients', None)
    if coeff is None:
        coeff = {'path': str(g['default_coefficients'][0]), 'sha256': g['default_coefficients'][1]}
    _strict(coeff, ('path', 'sha256'), 'coefficients')
    if not _is_hex64(coeff.get('sha256')) or not isinstance(coeff.get('path'), str):
        raise Refusal('coefficients {path, sha256(64 lowercase hex)} required')
    out['coefficients'] = {'path': str(Path(coeff['path'])), 'sha256': coeff['sha256']}
    num = spec.get('numerics', {})
    _strict(num, ('composite_grid_spec', 'truncation', 'picard', 'brackets', 'column_workers', 'k_domain'), 'numerics')
    grid = num.get('composite_grid_spec', None)
    if grid is not None:
        _strict(grid, ('version', 'breaks_inverse_kpc', 'panel_orders', 'total_axis_nodes', 'scope'), 'composite_grid_spec')
        br, po = grid.get('breaks_inverse_kpc'), grid.get('panel_orders')
        if not (isinstance(br, list) and isinstance(po, list) and len(br) == len(po) + 1 and len(po) >= 1):
            raise Refusal('composite_grid_spec breaks/panel_orders malformed')
        if any(type(n) is not int or n < 2 for n in po) or grid.get('total_axis_nodes') != sum(po):
            raise Refusal('panel orders must be ints >=2 summing to total_axis_nodes')
        if br[0] != -br[-1] or br[-1] <= 0:
            raise Refusal('breaks must partition [-kmax,kmax]')
    out_num = {'composite_grid_spec': grid}
    if num.get('k_domain') is not None:  # c2v002 OPTIONAL check; absent => exactly the c2v001 behaviour
        kd = normalize_k_domain(num['k_domain'])
        k_domain_report(grid if grid is not None else _base_seed_grid(g), kd['length_kpc'], refuse=True)
        out_num['k_domain'] = kd
    tr = num.get('truncation', {'shape': 'cube'})
    _strict(tr, ('shape', 'kmax_inverse_kpc'), 'truncation')
    shape = tr.get('shape', 'cube')
    if shape not in ('cube', 'sphere', 'cylinder'):
        raise Refusal('truncation.shape must be cube, sphere or cylinder')
    kmask = tr.get('kmax_inverse_kpc', None)
    if shape == 'cube' and kmask is not None:
        raise Refusal('cube truncation takes no kmax_inverse_kpc (the grid edge is the cube)')
    if kmask is not None:
        kmask = _num(kmask, 'truncation.kmax_inverse_kpc')
    out_num['truncation'] = {'shape': shape, 'kmax_inverse_kpc': kmask}
    pc = num.get('picard', {})
    _strict(pc, ('passes', 'speed_change_bound_km_s', 'observe_every_pass'), 'picard')
    passes = pc.get('passes', 3)
    if type(passes) is not int or not 1 <= passes <= 12:
        raise Refusal('picard.passes must be an int in 1..12')
    bound = pc.get('speed_change_bound_km_s', None)
    if bound is not None:
        bound = _num(bound, 'speed_change_bound_km_s')
    obs = pc.get('observe_every_pass', True)
    if type(obs) is not bool:
        raise Refusal('observe_every_pass must be bool')
    out_num['picard'] = {'passes': passes, 'speed_change_bound_km_s': bound, 'observe_every_pass': obs}
    bk = num.get('brackets', {'mode': 'rule'})
    _strict(bk, ('mode', 'rule', 'pinned_controls'), 'brackets')
    mode = bk.get('mode', 'rule')
    if mode == 'rule':
        rule = dict(LE_RULE_DEFAULTS)
        r_in = bk.get('rule', {})
        _strict(r_in, tuple(LE_RULE_DEFAULTS), 'brackets.rule')
        rule.update(r_in)
        for key in ('rfs_factors', 'le_first_factors', 'le_next_factors'):
            f = rule[key]
            if not (isinstance(f, list) and len(f) == 2 and 0 < _num(f[0], key) < _num(f[1], key)):
                raise Refusal(key + ' must be [lo, hi] with 0<lo<hi')
        for key, absolute in (('fs_absolute_overrides', True), ('rfs_factor_overrides', False)):
            for idx, pair in rule[key].items():
                if not (idx.isdigit() and 0 <= int(idx) < g['n_columns'] and isinstance(pair, list) and len(pair) == 2
                        and 0 < _num(pair[0], key) < _num(pair[1], key)):
                    raise Refusal('%s entries must be "index": [lo, hi]' % key)
        for ps, table in rule['le_factor_overrides'].items():
            if not (ps.isdigit() and 1 <= int(ps) <= passes) or not isinstance(table, dict):
                raise Refusal('le_factor_overrides keys must be pass numbers 1..passes')
            for idx, pair in table.items():
                if not (idx.isdigit() and 0 <= int(idx) < g['n_columns'] and isinstance(pair, list) and len(pair) == 2
                        and 0 < _num(pair[0], 'le override') < _num(pair[1], 'le override')):
                    raise Refusal('le_factor_overrides entries must be "index": [lo, hi]')
        out_num['brackets'] = {'mode': 'rule', 'rule': rule}
    elif mode == 'pinned_controls':
        pcs = bk.get('pinned_controls')
        _strict(pcs, ('fs', 'rfs', 'le'), 'pinned_controls')

        def runs(lst, label):
            if not isinstance(lst, list) or not lst:
                raise Refusal(label + ' must be a non-empty list of {path, sha256}')
            res = []
            for item in lst:
                _strict(item, ('path', 'sha256'), label)
                if not _is_hex64(item.get('sha256')):
                    raise Refusal(label + ' sha256 must be 64 lowercase hex')
                res.append({'path': str(item['path']), 'sha256': item['sha256']})
            return res
        le = pcs.get('le')
        if not isinstance(le, list) or len(le) != passes:
            raise Refusal('pinned_controls.le must list one run list per Picard pass')
        out_num['brackets'] = {'mode': 'pinned_controls', 'pinned_controls': {
            'fs': runs(pcs.get('fs'), 'pinned fs'), 'rfs': runs(pcs.get('rfs'), 'pinned rfs'),
            'le': [runs(x, 'pinned le') for x in le]}}
        if any(len(x) != 1 for x in out_num['brackets']['pinned_controls']['le']):
            raise Refusal('each LE pass must be a single column run (column-mean V004 requires one 72-column run)')
    else:
        raise Refusal('brackets.mode must be rule or pinned_controls')
    workers = num.get('column_workers', 1)
    if type(workers) is not int or not 1 <= workers <= 12:
        raise Refusal('column_workers must be int 1..12')
    if workers > 1 and mode != 'rule':
        raise Refusal('column_workers>1 requires brackets.mode rule (pinned controls cannot be split without new bytes)')
    out_num['column_workers'] = workers
    out['numerics'] = out_num
    adm = spec.get('admit', {}) or {}
    _strict(adm, ('route_a', 'reference', 'body'), 'admit')
    norm_adm = {}
    if adm.get('route_a') is not None:
        a = adm['route_a']
        _strict(a, ('attempt_directory', 'checkpoint_directory', 'identity_sha256', 'result_sha256'), 'admit.route_a')
        if not (_is_hex64(a.get('identity_sha256')) and _is_hex64(a.get('result_sha256'))):
            raise Refusal('admit.route_a needs identity_sha256 and result_sha256')
        norm_adm['route_a'] = {k: str(a[k]) for k in ('attempt_directory', 'checkpoint_directory', 'identity_sha256', 'result_sha256')}
    if adm.get('reference') is not None:
        if 'route_a' not in norm_adm:
            raise Refusal('admit.reference requires admit.route_a')
        a = adm['reference']
        _strict(a, ('directory', 'start_sha256', 'finish_sha256'), 'admit.reference')
        norm_adm['reference'] = {k: str(a[k]) for k in ('directory', 'start_sha256', 'finish_sha256')}
    if adm.get('body') is not None:
        if 'reference' not in norm_adm:
            raise Refusal('admit.body requires admit.reference')
        a = adm['body']
        _strict(a, ('directory', 'finish_sha256'), 'admit.body')
        norm_adm['body'] = {k: str(a[k]) for k in ('directory', 'finish_sha256')}
    out['admit'] = norm_adm
    rc = spec.get('reference_compare', False)
    if type(rc) is not bool:
        raise Refusal('reference_compare must be bool')
    out['reference_compare'] = rc
    return out


def per_call_seed(nspec):
    """Return (seed_object, changed_fields, base_seed_reusable).  Only numerical_inputs Eref_J,
    gamma (both times s), ell_F_m and the composite grid (with kmax/fourier_points) change;
    the 'physical' annotation mirrors follow.  Every other field is copied unchanged."""
    g = GALAXIES[nspec['galaxy']]
    path, sha = g['base_seed']
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refusal('base seed pin mismatch')
    base = json.loads(raw)
    seed = json.loads(raw)
    ni = seed['numerical_inputs']
    p = nspec['physical']
    s = p['common_scale_s']
    new = {'Eref_J': s * p['Eref_J'], 'gamma': s * p['gamma'], 'ell_F_m': p['ell_F_m']}
    grid = nspec['numerics']['composite_grid_spec']
    if grid is not None:
        new['composite_grid_spec'] = grid
        new['kmax_inverse_kpc'] = float(grid['breaks_inverse_kpc'][-1])
        new['fourier_points_per_axis'] = int(grid['total_axis_nodes'])
    changed = []
    for k, v in new.items():
        if canonical(ni.get(k)) != canonical(v):
            changed.append({'field': 'numerical_inputs.' + k, 'old': ni.get(k), 'new': v})
        ni[k] = v
    for k in ('Eref_J', 'ell_F_m', 'gamma'):
        seed['physical'][k] = ni[k]
    reusable = canonical(seed) == canonical(base)
    return seed, changed, reusable


# ----------------------------------------------------------------------------- execution context
class Ctx:
    """mode 'run': executes stages.  mode 'simulate': executes nothing; a stage's outputs are
    the SAVED chain's outputs (reproduction map) when they exist, else symbolic placeholders."""

    def __init__(self, mode, nspec, outdir, saved_runs=None):
        self.mode = mode
        self.spec = nspec
        self.out = Path(outdir)
        self.saved = saved_runs or {}
        self.counter = 0
        self.records = []
        self.passes = []
        self.compare = []
        self.t0 = time.monotonic()
        self.log = None
        self.driver = str(Path(__file__).resolve())

    # -- paths / hashes ------------------------------------------------------------------
    def stage_dir(self, name):
        self.counter += 1
        d = self.out / 'stages' / ('%02d_%s' % (self.counter, name))
        if self.mode == 'run':
            d.mkdir(parents=True, exist_ok=False)
        return d

    def finish_sha(self, d, name='finish.json'):
        p = Path(d) / name
        if p.is_file():
            return sha256_file(p)
        return 'PENDING_SHA256(%s)' % p

    def event(self, **kw):
        kw['elapsed_seconds'] = time.monotonic() - self.t0
        if self.log is not None:
            self.log.write(json.dumps(_jsonable(kw), allow_nan=False) + '\n')
            self.log.flush()

    def write_input(self, name, obj):
        d = self.out / 'inputs'
        if self.mode == 'run':
            d.mkdir(parents=True, exist_ok=True)
        p = d / name
        if self.mode == 'run':
            return p, _write_x(p, obj)
        raw = (json.dumps(_jsonable(obj), indent=1, allow_nan=False) + '\n').encode()
        d.mkdir(parents=True, exist_ok=True)
        if p.exists():
            raise Refusal('dry-run input exists: %s' % p)
        p.write_bytes(raw)
        return p, sha256_bytes(raw)

    # -- stage execution -------------------------------------------------------------------
    def request(self, name, key, argv, stage_globals=None, module_patches=None, mask=None):
        script, sha = SCRIPTS[key]
        return {'name': name, 'kind': key, 'script': str(script), 'script_sha256': sha, 'argv': [str(a) for a in argv],
                'stage_globals': stage_globals or {}, 'module_patches': module_patches or [], 'mask': mask}

    def run_stages(self, requests, stage_dirs):
        """Run one or more independent stage requests concurrently (single-thread each)."""
        import subprocess
        recs = []
        if self.mode != 'run':
            for req, d in zip(requests, stage_dirs):
                rec = dict(req, stage_dir=str(d), executed=False)
                self.records.append(rec)
                recs.append(rec)
            return recs
        procs = []
        for req, d in zip(requests, stage_dirs):
            rp = d / 'request.json'
            rsha = _write_x(rp, req)
            fo = open(d / 'stdout.txt', 'x')
            fe = open(d / 'stderr.txt', 'x')
            t = time.monotonic()
            pr = subprocess.Popen([PY, '-I', '-B', self.driver, '_stage', str(rp)], stdout=fo, stderr=fe,
                                  env=single_thread_env(), cwd=str(d))
            self.event(stage=req['name'], event='started', pid=pr.pid, request_sha256=rsha)
            procs.append((req, d, rp, rsha, pr, fo, fe, t))
        failed = []
        for req, d, rp, rsha, pr, fo, fe, t in procs:
            code = pr.wait()
            fo.close()
            fe.close()
            rec = dict(req, request_path=str(rp), request_sha256=rsha, stage_dir=str(d), exit_code=code,
                       elapsed_seconds=time.monotonic() - t, executed=True)
            self.records.append(rec)
            recs.append(rec)
            self.event(stage=req['name'], event='finished', exit_code=code, elapsed=rec['elapsed_seconds'])
            if code != 0:
                failed.append(req['name'])
        if failed:
            raise StageFailed('stage(s) exited nonzero: %s' % failed)
        return recs

    def saved_or(self, key, default):
        v = self.saved.get(key)
        return Path(v) if isinstance(v, (str, Path)) else default


# ----------------------------------------------------------------------------- chain helpers
def _read_checkpoint_identity(cm, cp):
    ident = cm._read(str(Path(cp) / 'IDENTITY.json'), 'identity')
    if ident['identity_sha256'] != cm._sha(cm._canonical(ident['identity'])):
        raise Blocked('checkpoint identity self-hash mismatch')
    return ident


def route_a_custody(cp, seed_sha, coeff_path, call_physical):
    """Verify a route-A checkpoint (computed in this call or admitted) from bytes and return
    the per-call identity the route-B stages need.  The route-B stages hard-code
    iteration_0004: any other converged iteration is a BLOCKER (no reviewed successor)."""
    import numpy as np
    cm = exec_verified(AUX['checkpoint_module'][0], AUX['checkpoint_module'][1], 'c2v001_ckpt')
    ident = _read_checkpoint_identity(cm, cp)
    caller = cm.decode(ident['identity']['caller']['record'])
    if caller['seed']['sha256'] != seed_sha:
        raise Blocked('checkpoint caller seed %s is not this call seed %s' % (caller['seed']['sha256'], seed_sha))
    phys = caller['physical_parameters']
    for k in ('Eref_J', 'ell_F_m', 'gamma'):
        if phys.get(k) != call_physical[k]:
            raise Blocked('checkpoint %s differs from call' % k)
    with np.load(coeff_path, allow_pickle=False) as f:
        grid = f['source_hessian_grid'].copy()
    if cm.digest(grid) != ident['identity']['inputs_sha256']['fourier_arguments']['source_hessian_grid']:
        raise Blocked('checkpoint coefficient grid differs from call coefficient grid')
    folder = Path(cp) / 'iteration_0004'
    if not (folder / 'COMPLETED.json').is_file():
        its = sorted(x.name for x in Path(cp).glob('iteration_*'))
        raise Blocked('ROUTE_A_ITERATION_NOT_4: route-B stages hard-code iteration_0004; present %s' % its)
    start = cm._read(str(folder / 'START.json'), 'iteration_start')
    done = cm._read(str(folder / 'COMPLETED.json'), 'iteration_completed')
    if start['iteration'] != 4 or done['converged'] is not True or done['iteration_start_sha256'] != start['payload_sha256']:
        raise Blocked('ROUTE_A_NOT_CONVERGED_AT_ITERATION_4 (route-B stages accept only that record)')
    return {'identity_sha256': ident['identity_sha256'], 'start_payload_sha256': start['payload_sha256'],
            'g4_ref': start['prepared_weighted_responses'], 'waves_ref': start['prepared_wavevectors'],
            'caller_seed': caller['seed'], 'physical': {k: phys.get(k) for k in ('Eref_J', 'ell_F_m', 'gamma')}}


def column_H(run_dirs):
    """Solved central enthalpies of completed columns (file pins from the run finish.json)."""
    H = {}
    for d in run_dirs:
        fin = Path(d) / 'finish.json'
        if not fin.is_file():
            return None
        f = json.loads(fin.read_text())
        for item in f['completed']:
            if sha256_file(item['path']) != item['sha256']:
                raise StageFailed('column file pin mismatch ' + item['path'])
            col = json.loads(Path(item['path']).read_text())
            if col['radial_index'] in H:
                raise StageFailed('duplicate column %d' % col['radial_index'])
            H[col['radial_index']] = col['Hc_m2_s2']
    return H


def rule_brackets(H, factors, overrides, indices):
    lo, hi = factors
    out = {}
    for i in indices:
        f = overrides.get(str(i), [lo, hi])
        out[str(i)] = [f[0] * H[i], f[1] * H[i]]
    return out


def merged_brackets(paths):
    """index -> bracket actually supplied by a list of controls files (later runs win)."""
    out = {}
    for p in paths:
        c = json.loads(Path(p).read_text())
        b = c.get('column_enthalpy_brackets', {})
        for i in c['radial_indices']:
            out[str(i)] = list(b.get(str(i), c['solver']['enthalpy_bracket']))
    return out


def rule_vs_saved(g, key, table):
    """DIAGNOSTIC: rule-generated bracket table versus the saved chain's controls for that pass."""
    sc = g.get('saved_controls', {})
    if key == 'fs':
        paths = [p for p, _ in sc.get('fs', [])]
    elif key == 'rfs':
        paths = [p for p, _ in sc.get('rfs', [])]
    else:
        k = int(key[2:]) - 1
        paths = [p for p, _ in sc['le'][k]] if 'le' in sc and k < len(sc['le']) else []
    if not paths:
        return {'checked': False}
    saved = merged_brackets(paths)
    diff = [i for i in saved if saved[i] != list(table.get(i, []))]
    return {'checked': True, 'n': len(saved), 'bitwise_equal_to_saved_controls': not diff, 'differing_indices': diff[:20]}


def bracket_check(pinned_paths, H, factors, overrides):
    """Diagnostic: do the pinned controls equal rule(H) bitwise?"""
    if H is None:
        return {'checked': False, 'reason': 'previous columns not available'}
    pinned = {}
    for p in pinned_paths:
        c = json.loads(Path(p).read_text())
        b = c.get('column_enthalpy_brackets', {})
        for i in c['radial_indices']:
            pinned[str(i)] = b.get(str(i), c['solver']['enthalpy_bracket'])
    rule = rule_brackets(H, factors, overrides, sorted(int(i) for i in pinned))
    diff = [i for i in pinned if pinned[i] != rule[i]]
    return {'checked': True, 'n': len(pinned), 'bitwise_equal': not diff, 'differing_indices': diff[:20]}


def _chunks(seq, n):
    n = max(1, min(n, len(seq)))
    size, rem = divmod(len(seq), n)
    out, i = [], 0
    for c in range(n):
        j = i + size + (1 if c < rem else 0)
        out.append(seq[i:j])
        i = j
    return out


def array_digests(npz_path, keys=None):
    import numpy as np
    out = {}
    with np.load(npz_path, allow_pickle=False) as f:
        for k in (keys or f.files):
            a = np.ascontiguousarray(f[k])
            h = hashlib.sha256((a.dtype.str + str(a.shape)).encode())
            h.update(a.tobytes())
            out[k] = h.hexdigest()
    return out


def compare_npz(new, old, keys=None):
    import numpy as np
    res = {}
    with np.load(new, allow_pickle=False) as a, np.load(old, allow_pickle=False) as b:
        for k in (keys or b.files):
            if k not in a.files:
                res[k] = 'MISSING'
                continue
            x, y = a[k], b[k]
            if x.shape != y.shape or x.dtype != y.dtype:
                res[k] = 'SHAPE_OR_DTYPE_DIFFERS'
            elif np.array_equal(x, y):
                res[k] = 'BITWISE_EQUAL'
            else:
                res[k] = 'DIFFERS max_abs=%r' % float(np.max(np.abs(x - y)))
    return res


def harmonic_diagnostic(rotation_npz):
    """Driver-side DIAGNOSTIC (not a stage output): azimuthal Fourier amplitude ratios of the
    stored full radial force Phi_R_full over the 16 azimuths, |F_m|/|F_0|, m=1..8."""
    import numpy as np
    with np.load(rotation_npz, allow_pickle=False) as f:
        pr = f['Phi_R_full'].copy()
        R = f['radial_nodes_m'].copy()
    F = np.abs(np.fft.rfft(pr, axis=1))
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = F[:, 1:, :] / F[:, :1, :]
    ratio = np.where(np.isfinite(ratio), ratio, np.nan)
    per_m = {('m%d' % (m + 1)): float(np.nanmax(ratio[:, m, :])) for m in range(ratio.shape[1])}
    per_radius = [{('m%d' % (m + 1)): float(np.nanmax(ratio[i, m, :])) for m in range(ratio.shape[1])} for i in range(len(R))]
    return {'quantity': '|FFT_m(Phi_R_full)|/|FFT_0(Phi_R_full)| over 16 azimuths, max over z', 'global_max': per_m,
            'per_radius_max': per_radius, 'radial_nodes_m': R.tolist(), 'status': 'DIAGNOSTIC_ONLY'}


# ----------------------------------------------------------------------------- the chain
def execute_chain(ctx):
    sp = ctx.spec
    g = GALAXIES[sp['galaxy']]
    sv = ctx.saved
    P = sp['numerics']['picard']['passes']
    bound = sp['numerics']['picard']['speed_change_bound_km_s']
    workers = sp['numerics']['column_workers']
    brackets = sp['numerics']['brackets']
    ef = sp['physical']['entropy_K_factor']
    efs = repr(ef)
    coeff_path, coeff_sha = sp['coefficients']['path'], sp['coefficients']['sha256']
    verify_pin(coeff_path, coeff_sha, 'coefficient grid')
    seed_obj, changed, reusable = per_call_seed(sp)
    if reusable:
        seed_path, seed_sha = g['base_seed']
    else:
        seed_path, seed_sha = ctx.write_input('seed_c2v001.json', seed_obj)
    seed_path = Path(seed_path)
    ni = seed_obj['numerical_inputs']
    if ni['kpc_m'] != KPC_M:
        raise Refusal('seed kpc_m differs from driver constant')
    call_phys = {k: ni[k] for k in ('Eref_J', 'ell_F_m', 'gamma')}
    tr = sp['numerics']['truncation']
    kgrid = float(ni['composite_grid_spec']['breaks_inverse_kpc'][-1])
    if tr['kmax_inverse_kpc'] is not None and tr['kmax_inverse_kpc'] > kgrid:
        raise Refusal('mask kmax exceeds the composite grid edge %.6g/kpc' % kgrid)
    kmask_m = (tr['kmax_inverse_kpc'] if tr['kmax_inverse_kpc'] is not None else kgrid) / KPC_M
    info = {'seed': {'path': str(seed_path), 'sha256': seed_sha, 'base_seed_reused': reusable, 'changed_fields': changed}}
    coeff_default = (coeff_path == str(g['default_coefficients'][0]) and coeff_sha == g['default_coefficients'][1])
    reuse_path, reuse_sha = SCRIPTS['reference']

    # ---------------- route A
    adm = sp['admit']
    if 'route_a' in adm:
        a = adm['route_a']
        att, cp = Path(a['attempt_directory']), Path(a['checkpoint_directory'])
        fin = json.loads((att / 'finish.json').read_text())
        if fin['status'] != 'RETURNED_ACTUAL_RESULT' or sha256_file(att / 'result.json') != a['result_sha256'] or fin['result_sha256'] != a['result_sha256']:
            raise Refusal('admitted route-A attempt does not verify')
        info['route_a'] = {'mode': 'admitted', 'attempt': str(att), 'checkpoint': str(cp)}
    else:
        d = ctx.stage_dir('route_a')
        sa = (sv.get('route_a') or {}) if ctx.mode != 'run' else {}
        att = Path(sa['attempt']) if 'attempt' in sa else d / 'attempt_000'
        cp = Path(sa['checkpoint']) if 'checkpoint' in sa else d / 'checkpoint'
        patches = []
        if not coeff_default:
            patches.append({'path': str(AUX['prep'][0]), 'sha256': AUX['prep'][1],
                            'set': {'COEFFICIENT': {'__path__': coeff_path}, 'COEFFICIENT_SHA': coeff_sha}})
        req = ctx.request('route_a', 'route_a', [
            '--seed', seed_path, '--seed-sha256', seed_sha, '--solver', AUX['solver'][0], '--solver-sha256', AUX['solver'][1],
            '--checkpoint-module', AUX['checkpoint_module'][0], '--checkpoint-module-sha256', AUX['checkpoint_module'][1],
            '--outdir', att, '--checkpoint-directory', cp, '--start-iteration', '0'], module_patches=patches)
        ctx.run_stages([req], [d])
        info['route_a'] = {'mode': 'computed', 'attempt': str(att), 'checkpoint': str(cp)}
    if (Path(cp) / 'IDENTITY.json').is_file():
        cust = route_a_custody(cp, seed_sha, coeff_path, call_phys)
        if 'route_a' in adm and cust['identity_sha256'] != adm['route_a']['identity_sha256']:
            raise Refusal('admitted checkpoint identity differs from declared')
    else:
        cust = {'identity_sha256': 'PENDING(route_a identity)', 'start_payload_sha256': 'PENDING',
                'g4_ref': {'file_sha256': 'PENDING'}, 'waves_ref': None}
    info['route_a']['custody'] = cust
    att_res = Path(att) / 'result.json'
    if att_res.is_file():
        ra = json.loads(att_res.read_text())
        info['route_a']['route_a_rows'] = ra['result']['result']['rows']
    ident = cust['identity_sha256']
    reuse_patch = {'path': str(reuse_path), 'sha256': reuse_sha, 'set': {'SEED_SHA': seed_sha, 'IDENTITY': ident}}
    mask = None
    if tr['shape'] != 'cube':
        mask = {'shape': tr['shape'], 'kmax_inverse_m': kmask_m, 'g4_file_sha256': cust['g4_ref']['file_sha256'],
                'waves_ref': cust['waves_ref'], 'checkpoint_module': [str(AUX['checkpoint_module'][0]), AUX['checkpoint_module'][1]],
                'cache_module': [str(AUX['cache'][0]), AUX['cache'][1]]}
    common = ['--seed', seed_path, '--checkpoint-directory', cp]

    # ---------------- reference (homotopy worker main)
    if 'reference' in adm:
        ref = Path(adm['reference']['directory'])
        verify_pin(ref / 'start.json', adm['reference']['start_sha256'], 'admitted reference start')
        verify_pin(ref / 'finish.json', adm['reference']['finish_sha256'], 'admitted reference finish')
    else:
        d = ctx.stage_dir('reference')
        ref = d / 'reference' if ctx.mode == 'run' else ctx.saved_or('reference', d / 'reference')
        req = ctx.request('reference', 'reference', common + ['--reference-module', AUX['reference_module'][0],
                          '--reference-sha256', AUX['reference_module'][1], '--outdir', ref],
                          stage_globals={'SEED_SHA': seed_sha, 'IDENTITY': ident})
        ctx.run_stages([req], [d])

    # ---------------- body
    if 'body' in adm:
        body = Path(adm['body']['directory'])
        verify_pin(body / 'finish.json', adm['body']['finish_sha256'], 'admitted body finish')
    else:
        d = ctx.stage_dir('body')
        body = d / 'body' if ctx.mode == 'run' else ctx.saved_or('body', d / 'body')
        src_path, src_sha = g['monotone_source']
        data_pins = [[str(ref / 'start.json'), ctx.finish_sha(ref, 'start.json')], [str(ref / 'finish.json'), ctx.finish_sha(ref)],
                     [str(src_path), src_sha]]
        req = ctx.request('body', 'body', common + ['--outdir', body],
                          stage_globals={'REFERENCE': {'__path__': str(ref)}, 'DATA_PINS': {'__pathdict__': data_pins}},
                          module_patches=[reuse_patch])
        ctx.run_stages([req], [d])
    body_fin = ctx.finish_sha(body)

    # ---------------- offset
    d = ctx.stage_dir('offset')
    off = d / 'offset' if ctx.mode == 'run' else ctx.saved_or('offset', d / 'offset')
    req = ctx.request('offset', 'offset', common + ['--body-directory', body, '--body-finish-sha256', body_fin,
                      '--wave-batch', FIXED_ARGS['wave_batch'], '--position-batch', FIXED_ARGS['position_batch'], '--outdir', off],
                      stage_globals={'COEFF': {'__path__': coeff_path}, 'COEFF_SHA': coeff_sha},
                      module_patches=[reuse_patch], mask=mask)
    ctx.run_stages([req], [d])
    off_fin = ctx.finish_sha(off)
    gl = {'OFFSET_SHA': off_fin}
    base = common + ['--offset-directory', off]

    verify_pin(g['solver_template'][0], g['solver_template'][1], 'solver template')
    template = json.loads(Path(g['solver_template'][0]).read_text())['solver']
    n = g['n_columns']

    def column_pass(tag, key, extra_args, plan_runs):
        """plan_runs: list of (controls_path, controls_sha) or ('GENERATE', controls_obj).  Returns run dirs."""
        dirs, reqs, sdirs = [], [], []
        saved_dirs = sv.get(tag + '_columns') if ctx.mode != 'run' else None
        for j, item in enumerate(plan_runs):
            if item[0] == 'GENERATE':
                cpath, csha = ctx.write_input('%s_controls_%02d.json' % (tag, j), item[1])
            else:
                cpath, csha = item
            dd = ctx.stage_dir('%s_columns_%02d' % (tag, j))
            outc = dd / 'columns'
            if saved_dirs is not None and len(saved_dirs) == len(plan_runs):
                outc = Path(saved_dirs[j])
            reqs.append(ctx.request('%s_columns_%02d' % (tag, j), key, base + ['--controls', cpath, '--controls-sha256', csha]
                                    + extra_args + ['--outdir', outc], stage_globals=gl, module_patches=[reuse_patch], mask=mask))
            sdirs.append(dd)
            dirs.append(outc)
        # run in waves of `workers` processes (rule mode only; otherwise len==sequential)
        for k in range(0, len(reqs), max(1, workers)):
            ctx.run_stages(reqs[k:k + workers], sdirs[k:k + workers])
        if ctx.mode != 'run' and saved_dirs is not None and len(saved_dirs) != len(plan_runs):
            dirs = [Path(x) for x in saved_dirs]
        return dirs

    def manifest(tag, run_dirs):
        obj = {'runs': [{'directory': str(x), 'finish_sha256': ctx.finish_sha(x)} for x in run_dirs],
               'scope': 'c2v001 generated manifest for %s; complete %d columns required by the stage itself' % (tag, n)}
        return ctx.write_input('%s_manifest.json' % tag, obj)

    def generated_runs(tag, bracket_table, v001=False, split=True):
        """Group indices into column runs.  v001 supports only one global bracket per run."""
        runs = []
        if v001:
            groups = {}
            for i in range(n):
                groups.setdefault(tuple(bracket_table[str(i)]), []).append(i)
            for br, ids in sorted(groups.items(), key=lambda kv: kv[1][0]):
                for ch in (_chunks(ids, workers) if split else [ids]):
                    sol = dict(template)
                    sol['enthalpy_bracket'] = list(br)
                    runs.append(('GENERATE', {'radial_indices': ch, 'solver': sol, 'selection': '%s c2v001 rule' % tag}))
        else:
            for ch in (_chunks(list(range(n)), workers) if split else [list(range(n))]):
                runs.append(('GENERATE', {'radial_indices': ch, 'solver': dict(template),
                                          'column_enthalpy_brackets': {str(i): bracket_table[str(i)] for i in ch},
                                          'selection': '%s c2v001 rule' % tag}))
        return runs

    rule = brackets.get('rule')
    pinned = brackets.get('pinned_controls')
    checks = {}

    # ---------------- FS pass, original K (v001 / v001 / v002)
    if pinned:
        fs_plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned fs controls')) for x in pinned['fs']]
        merged = {}
        for x in pinned['fs']:
            c = json.loads(Path(x['path']).read_text())
            for i in c['radial_indices']:
                merged[str(i)] = c['solver']['enthalpy_bracket']
            if any(c['solver'][k] != template[k] for k in template if k != 'enthalpy_bracket'):
                checks.setdefault('fs_solver_block_differs', []).append(x['path'])
        ro = g.get('repro_rule_overrides', {}).get('fs_absolute_overrides', {})
        expect = {str(i): list(ro.get(str(i), template['enthalpy_bracket'])) for i in range(n)}
        checks['fs'] = {'checked': True, 'n': len(merged), 'bitwise_equal': merged == expect,
                        'rule': 'nominal template bracket + repro_rule_overrides.fs_absolute_overrides (last successful run wins)'}
    else:
        table = {str(i): list(rule['fs_absolute_overrides'].get(str(i), template['enthalpy_bracket'])) for i in range(n)}
        fs_plan = generated_runs('fs', table, v001=True)
        checks['fs'] = rule_vs_saved(g, 'fs', table)
    fs_dirs = column_pass('fs', 'columns_v001', [], fs_plan)
    mpath, msha = manifest('fs', fs_dirs)
    d = ctx.stage_dir('fs_rotation')
    fs_rot = d / 'rotation' if ctx.mode == 'run' else ctx.saved_or('fs_rotation', d / 'rotation')
    ctx.run_stages([ctx.request('fs_rotation', 'rotation_v001', base + ['--column-manifest', mpath, '--column-manifest-sha256', msha,
                    '--mass-relative-tolerance', FIXED_ARGS['mass_relative_tolerance'], '--outdir', fs_rot],
                    stage_globals=gl, module_patches=[reuse_patch], mask=mask)], [d])
    d = ctx.stage_dir('fs_feedback')
    fs_fb = d / 'feedback' if ctx.mode == 'run' else ctx.saved_or('fs_feedback', d / 'feedback')
    ctx.run_stages([ctx.request('fs_feedback', 'feedback_v002', base + ['--rotation-directory', fs_rot,
                    '--rotation-finish-sha256', ctx.finish_sha(fs_rot), '--wave-batch', FIXED_ARGS['wave_batch'],
                    '--position-batch', FIXED_ARGS['position_batch'], '--bessel-cache-entries', FIXED_ARGS['bessel_cache_entries'],
                    '--outdir', fs_fb], stage_globals=gl, module_patches=[reuse_patch], mask=mask)], [d])
    fs_fb_sha = ctx.finish_sha(fs_fb)

    # ---------------- RFS columns, original K, refreshed field (v003): source of LE1 brackets
    H_fs = column_H(fs_dirs)
    rfs_args = ['--feedback-directory', fs_fb, '--feedback-finish-sha256', fs_fb_sha]
    if pinned:
        rfs_plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned rfs controls')) for x in pinned['rfs']]
        checks['rfs'] = bracket_check([x['path'] for x in pinned['rfs']], H_fs, LE_RULE_DEFAULTS['rfs_factors'],
                                      g.get('repro_rule_overrides', {}).get('rfs_factor_overrides', {}))
    else:
        if H_fs is None:
            rfs_plan = 'PENDING'
        else:
            table = rule_brackets(H_fs, rule['rfs_factors'], rule['rfs_factor_overrides'], range(n))
            checks['rfs'] = rule_vs_saved(g, 'rfs', table)
            rfs_plan = generated_runs('rfs', table)
    if rfs_plan == 'PENDING':
        rfs_dirs = ['PENDING(rfs columns)']
        ctx.records.append({'name': 'rfs_columns', 'executed': False, 'note': 'controls depend on fs column enthalpies (rule mode)'})
    else:
        rfs_dirs = column_pass('rfs', 'columns_v003', rfs_args, rfs_plan)

    # ---------------- LE Picard passes (v005 / v005 / v004 + column mean v004)
    field_dir, field_sha = fs_fb, fs_fb_sha
    field_worker = SCRIPTS['feedback_v002'][1]
    prev_dirs = rfs_dirs
    prev_speeds = None
    final = None
    for p in range(1, P + 1):
        tag = 'le%d' % p
        last = (p == P)
        serial = last or bound is not None
        H_prev = column_H(prev_dirs) if all(isinstance(x, Path) for x in prev_dirs) else None
        factors = rule['le_first_factors'] if (rule and p == 1) else (rule['le_next_factors'] if rule else None)
        if pinned:
            plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned le controls')) for x in pinned['le'][p - 1]]
            checks[tag] = bracket_check([x['path'] for x in pinned['le'][p - 1]], H_prev,
                                        LE_RULE_DEFAULTS['le_first_factors'] if p == 1 else LE_RULE_DEFAULTS['le_next_factors'], {})
        elif H_prev is None:
            plan = 'PENDING'
        else:
            ov = rule['le_factor_overrides'].get(str(p), {})
            table = rule_brackets(H_prev, factors, ov, range(n))
            checks[tag] = rule_vs_saved(g, tag, table)
            plan = generated_runs(tag, table, split=not serial)
        if plan == 'PENDING':
            ctx.records.append({'name': tag + '_columns', 'executed': False, 'note': 'controls depend on previous column enthalpies'})
            break
        cols = column_pass(tag, 'columns_v005', ['--feedback-directory', field_dir, '--feedback-finish-sha256', field_sha,
                           '--feedback-worker-sha256', field_worker, '--entropy-scale', efs], plan)
        mpath, msha = manifest(tag, cols)
        d = ctx.stage_dir(tag + '_rotation')
        rot = d / 'rotation' if ctx.mode == 'run' else ctx.saved_or(tag + '_rotation', d / 'rotation')
        ctx.run_stages([ctx.request(tag + '_rotation', 'rotation_v005', base + ['--column-manifest', mpath, '--column-manifest-sha256', msha,
                        '--feedback-directory', field_dir, '--feedback-finish-sha256', field_sha,
                        '--column-worker-sha256', SCRIPTS['columns_v005'][1], '--feedback-worker-sha256', field_worker,
                        '--mass-relative-tolerance', FIXED_ARGS['mass_relative_tolerance'], '--outdir', rot, '--entropy-scale', efs],
                        stage_globals=gl, module_patches=[reuse_patch], mask=mask)], [d])
        pass_rec = {'pass': p, 'columns': [str(x) for x in cols], 'rotation': str(rot), 'field': str(field_dir)}
        rf = Path(rot) / 'finish.json'
        if rf.is_file():
            rfj = json.loads(rf.read_text())
            pass_rec.update(rotation_positive=rfj['positive_rotation_square'], minimum_rotation_square=rfj['minimum_rotation_square'],
                            nonpositive_indices=rfj['nonpositive_indices'], rotation_arrays={'path': rfj['arrays_path'], 'sha256': rfj['arrays_sha256']})
            if ctx.mode == 'run':
                pass_rec['rotation_array_content_digests'] = array_digests(rfj['arrays_path'])
        failures = []
        for x in cols:
            fx = Path(x) / 'finish.json'
            if fx.is_file():
                failures += json.loads(fx.read_text())['failures']
        pass_rec['column_failures'] = failures
        observe = len(cols) == 1 and (last or bound is not None or sp['numerics']['picard']['observe_every_pass'])
        speeds = None
        if observe:
            d = ctx.stage_dir(tag + '_column_mean')
            obsd = d / 'observation' if ctx.mode == 'run' else ctx.saved_or(tag + '_column_mean', d / 'observation')
            b_path, b_sha = g['column_mean_binding']
            pins = [[str(b_path), b_sha], [str(Path(rot) / 'start.json'), ctx.finish_sha(rot, 'start.json')],
                    [str(Path(rot) / 'finish.json'), ctx.finish_sha(rot)],
                    [str(Path(cols[0]) / 'start.json'), ctx.finish_sha(cols[0], 'start.json')],
                    [str(Path(cols[0]) / 'finish.json'), ctx.finish_sha(cols[0])]]
            ctx.run_stages([ctx.request(tag + '_column_mean', 'column_mean_v004', ['--outdir', obsd],
                            stage_globals={'PINS': {'__ordered__': pins}})], [d])
            rp = Path(obsd) / 'result.json'
            if rp.is_file():
                res = json.loads(rp.read_text())
                pass_rec['column_mean'] = {'path': str(rp), 'sha256': sha256_file(rp), 'status': res['status']}
                if res['status'] == 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION':
                    speeds = [r['speed_km_s'] for r in res['prediction']['rows']]
                    pass_rec['rows'] = res['prediction']['rows']
                    pass_rec['nonaxisymmetric_residual_maxima'] = res['nonaxisymmetric_residual_maxima']
                    pass_rec['residual_units'] = res.get('residual_units')
                else:
                    pass_rec['column_mean_failure'] = res.get('failure')
        else:
            pass_rec['column_mean'] = 'NOT_OBSERVED (multi-run parallel pass or observe_every_pass false)'
        if speeds is not None and prev_speeds is not None:
            pass_rec['max_abs_change_km_s'] = max(abs(a - b) for a, b in zip(speeds, prev_speeds))
        ctx.passes.append(pass_rec)
        ctx.event(event='pass_done', **{k: v for k, v in pass_rec.items() if k in ('pass', 'max_abs_change_km_s', 'rotation_positive')})
        stop = last or (bound is not None and pass_rec.get('max_abs_change_km_s') is not None and pass_rec['max_abs_change_km_s'] <= bound)
        if stop:
            final = pass_rec
            break
        prev_speeds = speeds
        d = ctx.stage_dir(tag + '_feedback')
        fb = d / 'feedback' if ctx.mode == 'run' else ctx.saved_or(tag + '_feedback', d / 'feedback')
        ctx.run_stages([ctx.request(tag + '_feedback', 'feedback_v004', base + ['--rotation-directory', rot,
                        '--rotation-finish-sha256', ctx.finish_sha(rot), '--wave-batch', FIXED_ARGS['wave_batch'],
                        '--position-batch', FIXED_ARGS['position_batch'], '--bessel-cache-entries', FIXED_ARGS['bessel_cache_entries'],
                        '--outdir', fb, '--current-feedback-directory', field_dir, '--current-feedback-finish-sha256', field_sha,
                        '--rotation-worker-sha256', SCRIPTS['rotation_v005'][1], '--current-feedback-worker-sha256', field_worker],
                        stage_globals=gl, module_patches=[reuse_patch], mask=mask)], [d])
        field_dir, field_sha, field_worker = fb, ctx.finish_sha(fb), SCRIPTS['feedback_v004'][1]
        prev_dirs = cols
    info['bracket_rule_checks'] = checks
    return info, final


def reference_comparison(records, saved):
    """DIAGNOSTIC ONLY (never alters the flow): compare this call's stage outputs with the saved
    chain's outputs by array content.  NPZ file bytes are not deterministic (zip timestamps), so
    arrays are compared, not file hashes."""
    rows = []
    for rec in records:
        if not rec.get('executed') or rec.get('exit_code') != 0:
            continue
        name = rec['name']
        am = _argv_map(rec['argv'])
        new = Path(am.get('--outdir', ''))
        try:
            if name == 'route_a' and 'route_a' in saved:
                a = json.loads((Path(am['--checkpoint-directory']) / 'iteration_0004/START.json').read_text())
                b = json.loads((Path(saved['route_a']['checkpoint']) / 'iteration_0004/START.json').read_text())
                res = {k: ('BITWISE_EQUAL' if a[k]['array_sha256'] == b[k]['array_sha256'] else 'DIFFERS')
                       for k in ('prepared_wavevectors', 'prepared_weighted_responses', 'gas_fourier_J', 'fixed_source_fourier_J')}
            elif name == 'body' and 'body' in saved:
                res = compare_npz(new / 'body_arrays.npz', Path(saved['body']) / 'body_arrays.npz')
            elif name == 'offset' and 'offset' in saved:
                res = {f: compare_npz(new / f, Path(saved['offset']) / f) for f in
                       ('unit_response.npz', 'source_offset.npz', 'offset_prepared.npz', 'updated_base_arrays.npz')}
            elif name.endswith('_rotation') and name in saved:
                res = compare_npz(new / 'rotation_base_arrays.npz', Path(saved[name]) / 'rotation_base_arrays.npz')
            elif name.endswith('_feedback') and name in saved:
                res = {f: compare_npz(new / f, Path(saved[name]) / f) for f in ('gas_source_feedback.npz', 'refreshed_prepared.npz')}
            elif '_columns_' in name:
                tag = name.split('_columns_')[0]
                old_paths = {}
                for od in saved.get(tag + '_columns') or []:
                    for y in json.loads((Path(od) / 'finish.json').read_text())['completed']:
                        old_paths[y['index']] = y['path']
                if not old_paths:
                    continue
                fa = json.loads((new / 'finish.json').read_text())
                keys = ('Hc_m2_s2', 'z_m', 'weights_m', 'rho_kg_m3', 'enthalpy_m2_s2', 'roots_m', 'K_SI')
                res = {'failures_new': [x['index'] for x in fa['failures']]}
                for x in fa['completed']:
                    if x['index'] not in old_paths:
                        res[str(x['index'])] = 'NO_SAVED_COUNTERPART'
                        continue
                    ca, cb = json.loads(Path(x['path']).read_text()), json.loads(Path(old_paths[x['index']]).read_text())
                    res[str(x['index'])] = 'BITWISE_EQUAL' if all(ca[k] == cb[k] for k in keys) else 'DIFFERS'
            elif name.endswith('_column_mean') and name in saved:
                a = json.loads((new / 'result.json').read_text())['prediction']['rows']
                b = json.loads((Path(saved[name]) / 'result.json').read_text())['prediction']['rows']
                res = {'bitwise_equal': a == b, 'max_relative_difference': max(abs(x['speed_km_s'] - y['speed_km_s']) / abs(y['speed_km_s'])
                                                                              for x, y in zip(a, b))}
            else:
                continue
        except Exception as exc:
            res = 'COMPARISON_ERROR %s: %s' % (type(exc).__name__, exc)
        rows.append({'stage': name, 'result': res})
    return rows


# ----------------------------------------------------------------------------- run command
def all_static_pins(nspec):
    pins = {}
    for path, sha in list(SCRIPTS.values()) + list(AUX.values()):
        pins[str(path)] = verify_pin(path, sha, 'code')
    g = GALAXIES[nspec['galaxy']]
    for key in ('base_seed', 'profile', 'monotone_source', 'column_mean_binding', 'solver_template'):
        path, sha = g[key]
        pins[str(path)] = verify_pin(path, sha, key)
    pins[nspec['coefficients']['path']] = verify_pin(nspec['coefficients']['path'], nspec['coefficients']['sha256'], 'coefficients')
    return pins


def transitive_pins_and_scipy(roots=None):
    """Load each stage script from verified bytes (inert) and verify every (path, sha) it pins;
    scan every pinned .py for a top-level scipy import.  c2v002: `roots` (default = the DDO
    SCRIPTS+AUX, i.e. exactly c2v001) lets the NGC configuration scan its own files."""
    import re
    seen, problems, scipy_hits = {}, [], []
    if roots is None:
        roots = list(SCRIPTS.values()) + list(AUX.values())
    queue = [(str(p), s) for p, s in roots]
    pat = re.compile(r'^\s*(import\s+scipy|from\s+scipy)', re.M)

    def collect(obj, acc):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and _is_hex64(v) and isinstance(k, (str, Path)):
                    acc.append((str(k), v))
                else:
                    collect(v, acc)
        elif isinstance(obj, (list, tuple)):
            if len(obj) == 2 and isinstance(obj[1], str) and _is_hex64(obj[1]) and isinstance(obj[0], (str, Path)):
                acc.append((str(obj[0]), obj[1]))
            else:
                for v in obj:
                    collect(v, acc)
    while queue:
        path, sha = queue.pop()
        if path in seen:
            if seen[path] != sha:
                problems.append('conflicting pins for %s' % path)
            continue
        seen[path] = sha
        p = Path(path)
        if not p.is_file():
            problems.append('missing %s' % path)
            continue
        if sha256_file(p) != sha:
            problems.append('pin mismatch %s' % path)
            continue
        if p.suffix == '.py':
            text = p.read_text()
            if pat.search(text):
                scipy_hits.append(path)
            try:
                m = exec_verified(p, sha, 'c2v001_scan_' + p.stem)
            except Exception as exc:  # inert modules only define names
                problems.append('could not load %s: %s' % (path, exc))
                continue
            acc = []
            for name in dir(m):
                if name.isupper():
                    collect(getattr(m, name), acc)
            for path2, sha2 in acc:
                if Path(path2).suffix in ('.py', '.json', '.npz'):
                    queue.append((path2, sha2))
    return {'verified_files': len(seen), 'files': seen, 'problems': problems, 'scipy_imports': scipy_hits}


def cmd_run(spec_path, outdir):
    out = Path(outdir)
    if out.exists():
        print('REFUSED: outdir exists', file=sys.stderr)
        return 2
    out.mkdir(parents=True)
    t0 = time.monotonic()
    raw = Path(spec_path).read_bytes()
    spec_sha = sha256_bytes(raw)
    (out / 'inputs').mkdir()
    with open(out / 'inputs' / 'call_spec.json', 'xb') as f:
        f.write(raw)
    result = {'schema': RESULT_SCHEMA, 'call_spec_sha256': spec_sha, 'driver_sha256': sha256_file(__file__),
              'accepted_for_calibration': False, 'scored': False, 'valid': False, 'reasons': []}
    status = 'FAILED'
    ctx = None
    try:
        nspec = normalize_spec(json.loads(raw))
        if nspec.get('config') == 'NGC3198_C2V002':
            ngc_run_blocked(out, nspec, spec_sha, result)  # writes start/inputs, executes 0 stages, raises Blocked
        pins = all_static_pins(nspec)
        g = GALAXIES[nspec['galaxy']]
        _write_x(out / 'start.json', {'schema': RESULT_SCHEMA, 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                 'pid': os.getpid(), 'driver': str(Path(__file__).resolve()), 'driver_sha256': result['driver_sha256'],
                 'call_spec_sha256': spec_sha, 'normalized_spec': nspec, 'static_pins': pins,
                 'scope': 'Route-B m0 forward call; no observed velocity read, no score, no calibration admission.'})
        ctx = Ctx('run', nspec, out)
        ctx.log = open(out / 'progress.jsonl', 'x')
        info, final = execute_chain(ctx)
        result.update(galaxy=nspec['galaxy'], normalized_spec=nspec, identity=info, passes=ctx.passes)
        if final is None:
            result['reasons'].append('no final pass')
        else:
            result['final_pass'] = final['pass']
            if 'rows' in final and len(final['rows']) == g['n_queries'] and all(math.isfinite(r['speed_km_s']) for r in final['rows']):
                result['rows'] = final['rows']
                result['speeds_km_s'] = {r['id']: r['speed_km_s'] for r in final['rows']}
                result['valid'] = (not final['column_failures']) and final.get('rotation_positive') is True
                if not result['valid']:
                    result['reasons'].append('final pass column failures or nonpositive rotation')
            else:
                result['reasons'].append('final column mean did not return %d rows: %s' % (g['n_queries'], final.get('column_mean')))
            diag = {'nonaxisymmetric_residual_maxima': final.get('nonaxisymmetric_residual_maxima'),
                    'residual_units': final.get('residual_units'),
                    'stored_residual_arrays': {'rotation_arrays': final.get('rotation_arrays'),
                                               'keys': ['angular_radial_residual', 'angular_vertical_residual', 'angular_azimuthal_residual',
                                                        'Phi_R_full', 'Phi_z_full', 'base_residual_r0']},
                    'per_pass_maxima': [{'pass': x['pass'], 'maxima': x.get('nonaxisymmetric_residual_maxima')} for x in ctx.passes]}
            if final.get('rotation_arrays'):
                try:
                    diag['azimuthal_harmonics'] = harmonic_diagnostic(final['rotation_arrays']['path'])
                except Exception as exc:
                    diag['azimuthal_harmonics'] = 'unavailable: %s' % exc
            result['residual_diagnostics'] = diag
        status = 'COMPLETED' if result['valid'] else 'COMPLETED_INVALID'
    except Refusal as exc:
        status = 'REFUSED'
        result['reasons'].append(str(exc))
    except Blocked as exc:
        status = 'BLOCKED'
        result['reasons'].append(str(exc))
    except StageFailed as exc:
        status = 'FAILED_AT_STAGE'
        result['reasons'].append(str(exc))
    except Exception as exc:
        import traceback
        status = 'FAILED'
        result['reasons'].append('%s: %s' % (type(exc).__name__, exc))
        result['traceback'] = traceback.format_exc()
    if ctx is not None:
        result['stage_records'] = ctx.records
        if ctx.spec.get('reference_compare'):
            result['reference_comparison'] = reference_comparison(ctx.records, GALAXIES[ctx.spec['galaxy']].get('saved_runs', {}))
        if result.get('passes') is None:
            result['passes'] = ctx.passes
        if ctx.log is not None:
            ctx.log.close()
    result['status'] = status
    result['elapsed_seconds'] = time.monotonic() - t0
    rsha = _write_x(out / 'result.json', result)
    _write_x(out / 'finish.json', {'status': status, 'valid': result['valid'], 'result_path': str(out / 'result.json'),
             'result_sha256': rsha, 'elapsed_seconds': result['elapsed_seconds'], 'reasons': result['reasons'],
             'retries': 0, 'partial_outputs_preserved': True})
    return 0 if status in ('COMPLETED', 'COMPLETED_INVALID') else 3


# ----------------------------------------------------------------------------- dry-run command
def _argv_map(argv):
    out, i = {}, 0
    while i < len(argv):
        k = argv[i]
        if i + 1 < len(argv) and not str(argv[i + 1]).startswith('--'):
            out[k] = str(argv[i + 1])
            i += 2
        else:
            out[k] = None
            i += 1
    return out


UPSTREAM_FLAGS = ('--checkpoint-directory', '--body-directory', '--body-finish-sha256', '--offset-directory',
                  '--rotation-directory', '--rotation-finish-sha256', '--feedback-directory', '--feedback-finish-sha256',
                  '--current-feedback-directory', '--current-feedback-finish-sha256', '--column-manifest', '--column-manifest-sha256')


def _compare_argv(kind, planned, original):
    """Per-flag comparison of the planned argv (upstream outputs resolved to the SAVED chain's
    outputs) with the saved launch argv: identical literal / identical file bytes / identical
    manifest content / output location / different.  'role' says whether the value is an
    upstream output (in a real call it is this call's own output with the same role)."""
    pm, om = _argv_map(planned[1:]), _argv_map(original[4:])
    rows = []
    outputs = ('--outdir', '--checkpoint-directory') if kind == 'route_a' else ('--outdir',)
    for k in sorted(set(pm) | set(om)):
        a, b = pm.get(k, '<absent>'), om.get(k, '<absent>')
        role = 'output' if k in outputs else ('upstream-output' if k in UPSTREAM_FLAGS else 'static')
        if k in outputs:
            verdict = 'OUTPUT_LOCATION (fresh per call in a real run)'
        elif a == b:
            verdict = 'IDENTICAL_VALUE'
            if a and Path(a).is_file():
                verdict = 'IDENTICAL_VALUE_FILE_SHA256=' + sha256_file(a)
        elif k == '--column-manifest' and Path(a).is_file() and Path(b).is_file() and \
                json.loads(Path(a).read_text())['runs'] == json.loads(Path(b).read_text())['runs']:
            verdict = 'IDENTICAL_MANIFEST_RUNS (generated file; bytes differ)'
        elif k == '--column-manifest-sha256' and Path(pm['--column-manifest']).is_file() and \
                sha256_file(pm['--column-manifest']) == a and sha256_file(om['--column-manifest']) == b:
            verdict = 'IDENTICAL_ROLE (sha256 of the respective manifest file)'
        elif a and b and Path(a).is_file() and Path(b).is_file() and sha256_file(a) == sha256_file(b):
            verdict = 'IDENTICAL_FILE_BYTES'
        else:
            verdict = 'DIFFERENT'
        rows.append({'flag': k, 'role': role, 'planned': a, 'original': b, 'verdict': verdict})
    return rows


def _orig_launch(stage_outdir):
    lp = Path(stage_outdir).parent / 'launch.json'
    if lp.is_file():
        return json.loads(lp.read_text())['command']
    return None


def _npz_headers(path):
    import zipfile
    import numpy as np
    heads = {}
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            with z.open(name) as f:
                ver = np.lib.format.read_magic(f)
                shape, fortran, dtype = (np.lib.format.read_array_header_1_0(f) if ver == (1, 0)
                                         else np.lib.format.read_array_header_2_0(f))
                heads[name[:-4] if name.endswith('.npy') else name] = {'shape': list(shape), 'dtype': dtype.str}
    return heads


def cmd_dry_run(spec_path, report_dir):
    rd = Path(report_dir)
    if rd.exists():
        print('REFUSED: report dir exists', file=sys.stderr)
        return 2
    rd.mkdir(parents=True)
    raw = Path(spec_path).read_bytes()
    nspec = normalize_spec(json.loads(raw))
    if nspec.get('config') == 'NGC3198_C2V002':
        return ngc_dry_run(spec_path, raw, nspec, rd)
    g = GALAXIES[nspec['galaxy']]
    report = {'schema': 'UNT_GALAXY_M0_FORWARD_DRYRUN_C2V001', 'call_spec': str(spec_path), 'call_spec_sha256': sha256_bytes(raw),
              'driver_sha256': sha256_file(__file__), 'normalized_spec': nspec, 'executed_stages': 0}
    report['static_pins'] = all_static_pins(nspec)
    report['transitive_pins'] = transitive_pins_and_scipy()
    report['coefficient_npz_headers'] = _npz_headers(nspec['coefficients']['path'])
    seed_obj, changed, reusable = per_call_seed(nspec)
    report['seed'] = {'base_seed_reused_bitwise': reusable, 'changed_fields': changed}
    repro_like = reusable and nspec['numerics']['truncation']['shape'] == 'cube' and \
        nspec['physical']['entropy_K_factor'] == g['default_entropy_K_factor'] and \
        nspec['coefficients']['sha256'] == g['default_coefficients'][1] and nspec['numerics']['picard']['passes'] == 3
    saved = dict(g['saved_runs']) if repro_like else {}
    ctx = Ctx('simulate', nspec, rd / 'simulated_call', saved_runs=saved)
    info, final = execute_chain(ctx)
    report['identity'] = info
    stages = []
    for rec in ctx.records:
        row = {k: rec.get(k) for k in ('name', 'kind', 'script', 'script_sha256', 'argv', 'stage_globals', 'module_patches', 'mask', 'note')}
        if rec.get('argv') and repro_like:
            outdir = _argv_map(rec['argv']).get('--outdir')
            orig = _orig_launch(outdir) if outdir else None
            if orig is not None:
                row['original_launch'] = str(Path(outdir).parent / 'launch.json')
                row['original_launch_script_identical'] = (orig[3] == rec['script'] and sha256_file(orig[3]) == rec['script_sha256'])
                row['argv_comparison'] = _compare_argv(rec['kind'], [rec['script']] + rec['argv'], orig)
                row['all_inputs_identical'] = row['original_launch_script_identical'] and all(
                    x['verdict'].startswith('IDENTICAL') or x['verdict'].startswith('OUTPUT_LOCATION') for x in row['argv_comparison'])
            else:
                row['original_launch'] = None
                row['note'] = (row.get('note') or '') + ' no saved launch for this stage (extra observation or new stage)'
        if rec.get('argv'):
            # override values versus the values hard-coded in the stage / dependency files
            ov = []
            if rec.get('stage_globals') or rec.get('module_patches'):
                m = exec_verified(rec['script'], rec['script_sha256'], 'c2v001_dry_' + rec['kind'])
                for name, val in (rec.get('stage_globals') or {}).items():
                    ov.append(_override_row(rec['kind'], name, m.__dict__.get(name, _ABSENT), _decode_value(val)))
                for patch in rec.get('module_patches') or []:
                    dm = exec_verified(patch['path'], patch['sha256'], 'c2v001_dry_dep')
                    for name, val in patch['set'].items():
                        ov.append(_override_row(Path(patch['path']).name, name, getattr(dm, name, _ABSENT), _decode_value(val)))
            row['override_comparison'] = ov
        stages.append(row)
    report['stages'] = stages
    report['passes_simulated'] = ctx.passes
    if final is not None and final.get('rows'):
        report['final_rows_from_saved_chain'] = final['rows']
    sp = [ctx_row for ctx_row in stages if ctx_row.get('argv_comparison') is not None]
    report['summary'] = {
        'repro_like': repro_like,
        'stages_planned': len(stages),
        'stages_compared_with_original_launch': len(sp),
        'stages_all_inputs_identical': sum(1 for x in sp if x.get('all_inputs_identical')),
        'overrides_total': sum(len(x.get('override_comparison') or []) for x in stages),
        'overrides_noop_identical': sum(1 for x in stages for o in (x.get('override_comparison') or []) if o['verdict'] == 'NO_OP_IDENTICAL_VALUE'),
        'bracket_rule_checks': info.get('bracket_rule_checks'),
        'scipy_imports': report['transitive_pins']['scipy_imports'],
        'pin_problems': report['transitive_pins']['problems'],
    }
    ra = info.get('route_a', {})
    rp = Path(ra.get('attempt', '')) / 'result.json'
    if rp.is_file():
        src = json.loads(rp.read_text())['result'].get('source_pins', {})
        bad = [p for p, s in src.items() if not Path(p).is_file() or sha256_file(p) != s]
        report['route_a_recorded_source_pins'] = {'n': len(src), 'all_current_files_match': not bad, 'mismatch': bad,
            'note': 'prep V007 loads these helper modules by path and RECORDS (does not verify) their SHA256; checked here from bytes'}
    lines = ['DRY-RUN PLAN %s  (spec %s)' % (nspec.get('label', ''), report['call_spec_sha256']), '']
    for i, s in enumerate(stages, 1):
        verdict = s.get('all_inputs_identical')
        lines.append('%02d %-22s %-18s %s  inputs_identical_to_saved_launch=%s' % (i, s['name'], s['kind'] or '', (s['script_sha256'] or '')[:12], verdict))
        for x in s.get('argv_comparison') or []:
            lines.append('      %-34s %-15s %s' % (x['flag'], x['role'], x['verdict']))
        if s.get('argv') and not s.get('argv_comparison'):
            lines.append('      argv: ' + ' '.join(str(a).replace(str(ROOT), '$ROOT').replace(str(rd), '$DRY') for a in s['argv']))
        if s.get('mask'):
            lines.append('      mask: shape=%s kmax=%.6g/m g4_blob=%s (weight mask on existing grid)' % (s['mask']['shape'], s['mask']['kmax_inverse_m'], s['mask']['g4_file_sha256'][:16]))
        for o in s.get('override_comparison') or []:
            lines.append('      override %s.%s: %s' % (o['where'], o['name'], o['verdict']))
        if s.get('note'):
            lines.append('      note: ' + s['note'].strip())
    with open(rd / 'DRYRUN_PLAN.txt', 'x') as f:
        f.write('\n'.join(lines) + '\n')
    _write_x(rd / 'DRYRUN_REPORT.json', report)
    print(json.dumps(_jsonable(report['summary']), indent=1))
    return 0


_ABSENT = object()


def _override_row(where, name, hard, new):
    if hard is _ABSENT:
        return {'where': where, 'name': name, 'hard_coded': None, 'per_call': str(new), 'verdict': 'OVERRIDE_TARGET_ABSENT'}
    def norm(v):
        if isinstance(v, dict):
            return {str(k): norm(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)):
            return [norm(x) for x in v]
        return str(v) if isinstance(v, Path) else v
    a, b = norm(hard), norm(new)
    if a == b:
        verdict = 'NO_OP_IDENTICAL_VALUE'
    elif isinstance(b, str) and b.startswith('PENDING'):
        verdict = 'PER_CALL_VALUE_PENDING'
    else:
        verdict = 'PER_CALL_VALUE_DIFFERS_FROM_HARDCODED'
    return {'where': where, 'name': name, 'hard_coded': a, 'per_call': b, 'verdict': verdict}


# ============================================================================= NGC3198 (c2v002)
# Configuration only.  No NGC physics is implemented here: the NGC route-A chain is the reviewed
# ngc43 worker -> NGC prep v001 -> NGC binding v001 -> composite adapter -> 0424 solver, executed
# (when a reviewed successor unblocks it) from exact pinned bytes like every DDO stage.
NGC_SCHEMA = 'UNT_GALAXY_M0_FORWARD_CALL_NGC_C2V002'
NGC_RESULT_SCHEMA = 'UNT_GALAXY_M0_FORWARD_RESULT_NGC_C2V002'
NGC_CODE = {
    'worker': (HR / 'ngc43_composite_coupled_root_worker_v001.py', '1b95a4ff333f17cf7bc6ab56b76c4e615e982a298ee1a95fd80f07c8ab6c0ca4'),
    'prep': (HR / 'ngc_actual_initial_source_preparation_v001.py', 'c54c7cc995f0bb59bb5d81a3f1267dba5dae48d116302c9c0438fe7e5a53710f'),
    'binding': (HR / 'ngc_composite_full_coupled_binding_v001.py', '9e9caf83bcbbe259d371e923242cddc9011aa7f9f9830d63479138756d9b1248'),
    'composite': (HC / 'owned_composite_prepared_coupled_gas_adapter_v001.py', '75092cf64cf5293d9e1a5b28b2c909d875c1f5a1b3e9d185f71f065ccff49ec3'),
    'stream': (HC / 'owned_streamed_fourier_per_run_adapter_v001.py', 'cbbc4b968fc189440ddd4f516fb53f07d04a97b638fdf90fd90f50422afb928e'),
    'base': (HR / 'owned_physical_fourier_metric_quadrature_v005.py', '7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491'),
    'prediction': (HC / 'galaxy_coupled_fourier_hi_prediction_v005.py', '54136c71403c90b82f5b150672bf218577bf837c345798ec5f770adf31ba8c72'),
}
NGC_DATA = {
    'profile': (C1 / 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json', 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'),
    'manifest': (C1 / 'NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json', 'a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494'),
    'h2_tail_reduction': (C1 / 'NGC3198_H2_SOURCE_TAIL_REDUCTION_RUN_V001/stdout.txt', '157ede0487beed6658a413ae4db34cae2e819efc58efd292ccc56794ae5917d2'),
    'h2_source': (HR / 'NGC3198_MAIN_SOURCE_ANNULAR_INPUT_V001.json', '84e20bc022a088f7223319638091b65044983412cec09ac1cb0fb21d205aed61'),
    'physical_source_state_binding': (C1 / 'GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json', '7cadac8b66096a9d9942e9861289a1d41bad084e13cd7ba655341eb06e6afae9'),
    'stellar_photometry_nodes': (HR / 'NGC3198_DDO154_STELLAR_PHOTOMETRY_NODES_V001.json', '90657540e9d730c0af4d7a1b7fe66ec827f2c0bbb82f921df1398f23d6ab6935'),
    'source_only_bundle': (C1 / 'NGC3198_SOURCE_ONLY_BUNDLE_CANDIDATE_V001.json', '62abc88f12cb9da99ea1f1ba27c7eab2454553391984a65e2aa87a155fcc1fc1'),
    'review_worker': (HP / 'NGC43_COMPOSITE_ROOT_WORKER_DISTINCT_REVIEW_V001.json', '32736643ff32472c5a00ebab4eb91881be5332508f7f39b31a9e31e5f489c1ca'),
    'review_binding': (HP / 'NGC43_COMPOSITE_H2_BINDING_DISTINCT_REVIEW_V001.json', '23d1d395cf124bb4f71474aca35bff49abeca3f813a6fc46ee35732f3c85c39f'),
    # numerical controls of the candidate NGC seed are carried from the current DDO seed (V002)
    'parameter_seed': (C1 / 'DDO154_STABLE_CACHED_COUPLED_TRIAL_SEED_V002.json', '694eaaaab38547a369ac85c3c3d0b5550d8878753ccafe7bc0e5cdcb79be6680'),
}
# Evidence for the route-A blocker (read-only; nothing here is executed except inert definitions).
NGC_EVIDENCE = {
    'checkpoint_c2v001': (EX / 'resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v001.py', 'a831fe81ef25a065201f0c5d7e2cb4447a7d8cf3712507b1462a09ff4e0d2dd3'),
    'checkpoint_c2v002': (EX / 'resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v002.py', '0bb955ed86c6e71884152c1dd97c41e2d086a4cd2e135f78e9b2716d2e4803c1'),
    'solver_nonfixedsrc': (EX / 'resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_c2v001.py', 'c91c5051ad7fea477a51dc9fbdaae2cdc755cc8186a318aa27627cf9d21651e6'),
    'ddo_stable_binding_v002': (HR / 'ddo_composite_stable_cached_binding_v002.py', 'd81b24b7150c846a5b70c82a8668daaaef53335ced062763980a33cdbc90b6d5'),
    'ddo_precedent_failure': (C1 / 'DDO154_STABLE_CACHED_COUPLED_RUN_V001/attempt_000/failure.json', '3743adff8ba446310e28e074089a1080ba0cabc9d18fa2ba2eae555a7df6f301'),
}
NGC_PREP_MAX_AXIS_NODES = 80  # NGC prep v001 guard (nk>80 refused); not a driver choice

# Every DDO-specific hard-coding of the route-B chain and what the NGC configuration supplies.
# (stage, file key in SCRIPTS/AUX or None for the driver itself, needles located at dry-run, ...)
NGC_ROUTE_B_HARDCODING = [
    ('route_a', 'route_a', ["ddo_actual_initial_source_preparation_v007.py"],
     'Route-A preparation = DDO prep V007: galaxies["DDO154"] profile, 12-row DDO roster, DDO H2/stars.',
     'NGC prep v001 c54c7cc9 (reviewed PASS_SCOPED_CONDITIONAL_SOLVER): galaxies["NGC3198"], 43-row manifest roster, '
     'HI sigma0=11 km/s and Gamma=5/3 (prep line 113), H2 = 10 detected centres + constant core + matched exponential tail '
     '(Rd=1.806 kpc from the pinned tail reduction) at the stellar sech^2 height (counted proxy), analytic stellar rings; '
     'profile geometry 13.8 Mpc / 72 deg.', 'SUPPLIED_FROM_REVIEWED_CODE'),
    ('route_a', 'route_a', ["ddo_composite_stable_cached_binding_v002.py", "'stable_adapter'", "owned_scalar_lapse_inverse_cache_v001.py"],
     'Route-A binding = DDO stable-cached V002: stable lapse HI facade, stable line v002, HI v003, scalar lapse inverse cache, '
     'and the c2v003 checkpoint caller contract (physical_parameters, numerical_controls); observation 66/64 deg.',
     'NGC binding v001 9e9caf83 + worker v001 1b95a4ff exist (72/73 deg, 43 rows) but are clones of the PRE-stable DDO '
     'composite binding/worker v001: no stable HI/line/cache modules and no c2v003 caller contract. They cannot open any '
     'existing checkpoint (see caller_contract_check). The same defect failed DDO154_STABLE_CACHED_COUPLED_RUN_V001.',
     'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('route_a', None, ['DDO154_STABLE_CACHED_COUPLED_TRIAL_SEED_V002.json'],
     'Base seed = DDO seed V002 (694eaaaa): numerical controls + DDO-selected Eref/ell_F/gamma.',
     'No NGC seed exists. c2v002 composes a CANDIDATE seed: DDO V002 numerical controls unchanged, call-spec Eref/ell_F/gamma/s, '
     'call-spec composite grid, call-spec h2_tail_mass_rtol (worker requires it explicitly; no reviewed value exists).',
     'CANDIDATE_COMPOSED_REQUIRES_ROOT_SELECTION'),
    ('reference', 'reference', ["['galaxies']['DDO154']", "'iteration_0004'", "start['iteration']!=4"],
     'Homotopy reference reads galaxies["DDO154"] inline and accepts only route-A iteration 4.',
     'None. Needs a reviewed successor reading galaxies["NGC3198"] (the same profile file holds it) and the converged iteration.',
     'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('reference', 'reference_module', ['sigma=11000.;gamma=5/3', 'range(16)'],
     'Reference module: HI sigma0=11 km/s, Gamma=5/3, 16 angles inline.',
     'Same adopted values as NGC prep v001 (11 km/s, 5/3); 16 angles are numerics. Not galaxy-specific.',
     'COMPATIBLE_SAME_ADOPTED_VALUES'),
    ('body', 'body', ["DDO154_MONOTONE_SOURCE_RECONSTRUCTION_RUN_V001/source.json", "['galaxies']['DDO154']", 'len(R)!=72', '(72,16,8)'],
     'Body: DDO monotone source, galaxies["DDO154"], exactly 72 radii, shape (72,16,8) inline.',
     'None. No NGC monotone-source reconstruction exists; the NGC HI radial roster is 51 annuli x GL order (204 at order 4), not 72.',
     'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('offset', 'offset', ["['galaxies']['DDO154']", 'reshape((72,16,8,10))', '(72,16,8)'],
     'Offset: galaxies["DDO154"] radial domain and (72,16,8) reshapes inline.', 'None.', 'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('fs/rfs/le columns', 'columns_v005', ['0<=i<72', 'iteration_0004'],
     'Column stages v001/v003/v005: radial index range 0..71 inline; iteration 4.', 'None.', 'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('fs/le rotation', 'rotation_v005', ["DDO154_MONOTONE_SOURCE_RECONSTRUCTION_RUN_V001/source.json", 'set(range(72))', '(72,16,nz,10)'],
     'Rotation v001/v005: DDO monotone source pin, complete-72 roster inline.', 'None.', 'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('fs/le feedback', 'feedback_v004', ['(72,16,32)', 'radius.shape!=(72,)'],
     'Native feedback v002/v004: complete 72x16x32 measure inline.', 'None.', 'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('column mean', 'column_mean_v004', ['DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json', 'R.shape!=(72,)', 'list(range(72))'],
     'Column mean V004: DDO 12-row binding (4.04 Mpc radii, sin66/sin64) and 72 columns inline.',
     'None. No NGC 43-row column-mean binding exists (the 43 radii and 72/73 deg exist only in the route-A binding).',
     'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('brackets', None, ['DDO154_REMAINING_FREE_SURFACE_CONTROLS_V001.json', '302500000.0'],
     'Column solver template and FS absolute enthalpy brackets [1.5125e8, 3.025e8] m^2/s^2 are DDO values.',
     'None. NGC column enthalpy scale is unknown until an NGC route-A fixed point exists.', 'BLOCKER_NO_NGC_VALUES'),
    ('entropy', None, ['64 / 121'],
     'Entropy K factor 64/121 was selected on the DDO chain.', 'None (route-B only).', 'NOT_APPLICABLE_ROUTE_B_BLOCKED'),
    ('geometry', None, ["'distance_Mpc': 4.04", "'inclination_deg': 66.0"],
     'Registered geometry 4.04 Mpc / 66 deg (released 64).',
     'Profile NGC3198 geometry 13.8 Mpc / 72 deg (stellar face-on factor 1.0) and NGC binding v001 72/73 deg projection.',
     'SUPPLIED_FROM_REVIEWED_CODE'),
    ('queries', None, ["'n_queries': 12"],
     'Output = 12 DDO rows from the column-mean binding.',
     'Output = 43 rows NGC3198-Q01..Q43 in manifest order from route A (prediction v005 rows); route-B rows unavailable.',
     'SUPPLIED_ROUTE_A_ONLY'),
]


def normalize_k_domain(kd):
    _strict(kd, ('length_kpc', 'scope'), 'k_domain')
    return {'length_kpc': _num(kd.get('length_kpc'), 'k_domain.length_kpc')}


def _base_seed_grid(g):
    path, sha = g['base_seed']
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refusal('base seed pin mismatch')
    return json.loads(raw)['numerical_inputs']['composite_grid_spec']


def _grid_axis(grid):
    import numpy as np
    parts = []
    for lo, hi, n in zip(grid['breaks_inverse_kpc'][:-1], grid['breaks_inverse_kpc'][1:], grid['panel_orders']):
        x, _ = np.polynomial.legendre.leggauss(n)
        parts.append((lo + hi) / 2 + (hi - lo) * x / 2)
    return np.concatenate(parts)


def k_domain_report(grid, length_kpc, refuse=False):
    """k-domain coverage of a composite Gauss grid for a real-space extent L (kpc).
    CHECK (refusable): the smallest positive axis node k_min must satisfy k_min <= 2*pi/L.
    DIAGNOSTIC only (no acceptance threshold, no accuracy certificate): per positive panel,
    the phase L*dk swept across the panel and that phase per node, i.e. how many radians of
    exp(i k x) at |x| = L each Gauss node must carry."""
    import numpy as np
    ax = _grid_axis(grid)
    pos = np.sort(ax[ax > 0])
    need = 2 * math.pi / length_kpc
    ok = bool(len(pos) and pos[0] <= need)
    panels = []
    br, po = grid['breaks_inverse_kpc'], grid['panel_orders']
    for lo, hi, n in zip(br[:-1], br[1:], po):
        if lo < 0:
            continue
        x, _ = np.polynomial.legendre.leggauss(n)
        nodes = (lo + hi) / 2 + (hi - lo) * x / 2
        panels.append({'panel_inverse_kpc': [lo, hi], 'order': n, 'max_node_spacing_inverse_kpc': float(np.max(np.diff(nodes))) if n > 1 else None,
                       'phase_across_panel_rad_at_L': length_kpc * (hi - lo), 'phase_per_node_rad_at_L': length_kpc * (hi - lo) / n})
    rep = {'length_kpc': length_kpc, 'required_kmin_inverse_kpc': need, 'grid_kmin_node_inverse_kpc': float(pos[0]) if len(pos) else None,
           'grid_kmax_inverse_kpc': float(br[-1]), 'nodes_per_axis': int(sum(po)), 'positive_nodes_below_required_kmin': int(np.sum(pos <= need)),
           'kmin_covered': ok, 'positive_panels_DIAGNOSTIC': panels,
           'scope': 'kmin check only; per-panel phase is a DIAGNOSTIC with no accuracy threshold (nonperiodic Gauss cube, '
                    'no cutoff/quadrature error certificate)'}
    if refuse and not ok:
        raise Refusal('k-domain: smallest positive grid node %.6g/kpc exceeds 2pi/L = %.6g/kpc for L = %.6g kpc'
                      % (rep['grid_kmin_node_inverse_kpc'], need, length_kpc))
    return rep


def normalize_ngc_spec(spec):
    _strict(spec, ('schema', 'galaxy', 'label', 'physical', 'coefficients', 'numerics'), 'spec')
    if spec.get('galaxy') != 'NGC3198':
        raise Refusal('schema %s is the NGC3198 configuration only' % NGC_SCHEMA)
    g = GALAXIES['NGC3198']
    phys = spec.get('physical', {})
    _strict(phys, ('Eref_J', 'ell_F_m', 'gamma', 'common_scale_s', 'distance_Mpc', 'inclination_deg'), 'physical')
    geo = g['registered_geometry']
    p = {'Eref_J': _num(phys.get('Eref_J'), 'Eref_J'), 'ell_F_m': _num(phys.get('ell_F_m'), 'ell_F_m'),
         'gamma': _num(phys.get('gamma'), 'gamma'),
         'common_scale_s': _num(phys.get('common_scale_s', 1.0), 'common_scale_s'),
         'distance_Mpc': _num(phys.get('distance_Mpc', geo['distance_Mpc']), 'distance_Mpc'),
         'inclination_deg': _num(phys.get('inclination_deg', geo['inclination_deg']), 'inclination_deg')}
    if p['distance_Mpc'] != geo['distance_Mpc'] or p['inclination_deg'] != geo['inclination_deg']:
        raise Refusal('UNSUPPORTED NGC geometry: only the profile reference 13.8 Mpc / 72 deg is supported. The source radii '
                      'and stellar face-on factor are baked into GALAXY_RADIAL_SOURCE_REFERENCE_V001 (NGC3198 geometry) and '
                      'NGC binding v001 hard-codes the 72/73 deg projection; no reviewed code rescales either.')
    coeff = spec.get('coefficients', None) or {'path': str(g['default_coefficients'][0]), 'sha256': g['default_coefficients'][1]}
    _strict(coeff, ('path', 'sha256'), 'coefficients')
    if (str(coeff.get('path')), coeff.get('sha256')) != (str(g['default_coefficients'][0]), g['default_coefficients'][1]):
        raise Refusal('NGC c2v002: only the default coefficient grid fe5a2f06 (hard-coded in NGC prep v001) is supported')
    num = spec.get('numerics', {})
    _strict(num, ('composite_grid_spec', 'k_domain', 'h2_tail_mass_rtol', 'truncation'), 'numerics')
    tr = num.get('truncation', {'shape': 'cube'})
    _strict(tr, ('shape',), 'truncation')
    if tr.get('shape', 'cube') != 'cube':
        raise Refusal('NGC: route A has no truncation-mask hook; only cube is supported')
    grid = num.get('composite_grid_spec', None)
    if grid is not None:
        _strict(grid, ('version', 'breaks_inverse_kpc', 'panel_orders', 'total_axis_nodes', 'scope'), 'composite_grid_spec')
        br, po = grid.get('breaks_inverse_kpc'), grid.get('panel_orders')
        if not (isinstance(br, list) and isinstance(po, list) and len(br) == len(po) + 1 and len(po) >= 1):
            raise Refusal('composite_grid_spec breaks/panel_orders malformed')
        if any(type(n) is not int or n < 2 for n in po) or grid.get('total_axis_nodes') != sum(po):
            raise Refusal('panel orders must be ints >=2 summing to total_axis_nodes')
        if br[0] != -br[-1] or br[-1] <= 0 or any(b <= a for a, b in zip(br, br[1:])):
            raise Refusal('breaks must strictly partition [-kmax,kmax]')
        # NGC prep v001 guards, checked early (the prep re-checks them itself)
        if sum(po) > NGC_PREP_MAX_AXIS_NODES or sum(po) % 2 or br != [-b for b in br[::-1]] or po != po[::-1]:
            raise Refusal('NGC prep v001 requires <=80 even axis nodes and reflection-symmetric breaks/orders')
    if num.get('k_domain') is None:
        raise Refusal('NGC: numerics.k_domain {length_kpc} is required (the 43 queries reach 44.08 kpc)')
    kd = normalize_k_domain(num['k_domain'])
    k_domain_report(grid if grid is not None else _base_seed_grid({'base_seed': NGC_DATA['parameter_seed']}), kd['length_kpc'], refuse=True)
    tol = num.get('h2_tail_mass_rtol')
    if isinstance(tol, bool) or not isinstance(tol, (int, float)) or not math.isfinite(float(tol)) or tol <= 0:
        raise Refusal('NGC: numerics.h2_tail_mass_rtol (positive finite) is required by the reviewed worker; no reviewed value exists')
    return {'schema': NGC_SCHEMA, 'config': 'NGC3198_C2V002', 'galaxy': 'NGC3198', 'label': spec.get('label', ''), 'physical': p,
            'coefficients': {'path': str(coeff['path']), 'sha256': coeff['sha256']},
            'numerics': {'composite_grid_spec': grid, 'k_domain': kd, 'h2_tail_mass_rtol': float(tol), 'truncation': {'shape': 'cube'}}}


def ngc_seed(nspec):
    """Candidate per-call NGC worker seed: DDO seed V002 numerical controls carried unchanged,
    plus the call's Eref/gamma (times s), ell_F, composite grid and h2_tail_mass_rtol.  Checked
    against the NGC prep v001 signature (exact keyword set).  Not root-selected."""
    import inspect
    path, sha = NGC_DATA['parameter_seed']
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refusal('parameter seed pin mismatch')
    base = json.loads(raw)
    ni = json.loads(json.dumps(base['numerical_inputs']))
    p, s = nspec['physical'], nspec['physical']['common_scale_s']
    grid = nspec['numerics']['composite_grid_spec']
    set_fields = {'Eref_J': s * p['Eref_J'], 'gamma': s * p['gamma'], 'ell_F_m': p['ell_F_m'],
                  'h2_tail_mass_rtol': nspec['numerics']['h2_tail_mass_rtol']}
    if grid is not None:
        set_fields.update(composite_grid_spec=grid, kmax_inverse_kpc=float(grid['breaks_inverse_kpc'][-1]),
                          fourier_points_per_axis=int(grid['total_axis_nodes']))
    provenance = {}
    for k in sorted(set(ni) | set(set_fields)):
        if k in set_fields:
            old = ni.get(k)
            ni[k] = set_fields[k]
            provenance[k] = 'CALL_SPEC' + ('' if canonical(old) != canonical(ni[k]) else ' (equal to DDO seed V002 value)')
        else:
            provenance[k] = 'CARRIED_FROM_DDO_SEED_V002 (numerical control; not NGC-reviewed)'
    if ni['kpc_m'] != KPC_M:
        raise Refusal('seed kpc_m differs from driver constant')
    prep = exec_verified(NGC_CODE['prep'][0], NGC_CODE['prep'][1], 'c2v002_ngc_prep_sig')
    params = set(inspect.signature(prep.prepare_inputs).parameters)
    if set(ni) != params:
        raise Refusal('candidate seed keys differ from NGC prep v001 signature: missing %s extra %s'
                      % (sorted(params - set(ni)), sorted(set(ni) - params)))
    if ni.get('analytic_initial_azimuth') is not True or ni.get('composite_grid_spec') is None:
        raise Refusal('NGC binding v001 requires analytic_initial_azimuth True and a composite grid')
    pins = {str(NGC_DATA[k][0]): NGC_DATA[k][1] for k in ('manifest', 'profile', 'h2_tail_reduction', 'h2_source', 'parameter_seed')}
    seed = {'status': 'C2V002_CANDIDATE_NGC3198_TARGET_FREE_SEED_NOT_ROOT_SELECTED',
            'numerical_inputs': ni,
            'physical': {'Eref_J': ni['Eref_J'], 'ell_F_m': ni['ell_F_m'], 'gamma': ni['gamma'], 'common_scale_s': s,
                         'distance_Mpc': p['distance_Mpc'], 'inclination_deg': p['inclination_deg'],
                         'released_inclination_deg': GALAXIES['NGC3198']['registered_geometry']['released_inclination_deg']},
            'pins': pins,
            'parameter_provenance': provenance,
            'parent_seed': {'path': str(path), 'sha256': sha, 'scale_seed': base.get('scale_seed')},
            'scope': 'Target-free NGC43 provisional circular trial seed. Physical point = DDO seed parameters unless the call '
                     'spec says otherwise; numerical controls carried from DDO seed V002 are DDO-selected, not NGC-reviewed. '
                     'No velocity read; not calibration.'}
    return seed


def ngc_static_pins(nspec):
    pins = {}
    for table in (NGC_CODE, NGC_DATA, NGC_EVIDENCE):
        for key, (path, sha) in table.items():
            pins[str(path)] = verify_pin(path, sha, 'NGC ' + key)
    for key in ('solver', 'checkpoint_module'):
        pins[str(AUX[key][0])] = verify_pin(AUX[key][0], AUX[key][1], key)
    pins[nspec['coefficients']['path']] = verify_pin(nspec['coefficients']['path'], nspec['coefficients']['sha256'], 'coefficients')
    # reviews name exactly these code pins
    rw = json.loads(Path(NGC_DATA['review_worker'][0]).read_text())
    rb = json.loads(Path(NGC_DATA['review_binding'][0]).read_text())
    rb_pins = {x['path']: x['sha256'] for x in rb['sources']}
    review = {'worker_review_verdict': rw['verdict'], 'worker_review_sha_matches': rw['sha256'] == NGC_CODE['worker'][1],
              'binding_review_verdict': rb['verdict'],
              'binding_review_pins_match': all(rb_pins.get(str(NGC_CODE[k][0])) == NGC_CODE[k][1] for k in ('prep', 'binding'))
              and rb_pins.get(str(NGC_DATA['manifest'][0])) == NGC_DATA['manifest'][1]
              and rb_pins.get(str(NGC_DATA['h2_tail_reduction'][0])) == NGC_DATA['h2_tail_reduction'][1],
              'blocking_corrections': rw['blocking_corrections'] + rb['blocking_corrections']}
    w = exec_verified(NGC_CODE['worker'][0], NGC_CODE['worker'][1], 'c2v002_ngc_worker_local')
    local = {k: (str(pth), s) for k, (pth, s) in w.LOCAL.items()}
    review['worker_LOCAL_equals_config'] = all(local.get(k) == (str(NGC_CODE[k][0]), NGC_CODE[k][1]) for k in local) and \
        set(local) == {'prep', 'binding', 'composite', 'stream', 'base', 'prediction'}
    return pins, review


_VELOCITY_KEY_HINTS = ('velocit', 'vobs', 'v_obs', 'vrot', 'v_rot', 'vgas', 'vdisk', 'vbul', 'errv', 'vflat')


def _key_scan(obj, prefix='', hits=None):
    """Key NAMES only (never values) that look like velocity fields."""
    hits = [] if hits is None else hits
    if isinstance(obj, dict):
        for k, v in obj.items():
            kl = str(k).lower()
            if any(h in kl for h in _VELOCITY_KEY_HINTS):
                hits.append(prefix + '/' + str(k))
            _key_scan(v, prefix + '/' + str(k), hits)
    elif isinstance(obj, list):
        for v in obj[:3]:
            _key_scan(v, prefix + '/[]', hits)
    return hits


def ngc_sources_summary():
    """Load the NGC source JSONs (source-only files; no target velocity file is opened) and
    return headers and counts.  The rotmod .dat named in the manifest provenance is NOT opened."""
    out = {}
    load = {k: json.loads(Path(NGC_DATA[k][0]).read_bytes()) for k in
            ('profile', 'manifest', 'h2_source', 'physical_source_state_binding', 'stellar_photometry_nodes', 'source_only_bundle')}
    tail = json.loads(Path(NGC_DATA['h2_tail_reduction'][0]).read_bytes())
    prof = load['profile']['galaxies']['NGC3198']
    gas, st = prof['HI_plus_He'], prof['stellar_reference']
    out['profile_NGC3198'] = {'geometry': prof['geometry'], 'HI_annuli': len(gas['annular_means_Msun_pc2']),
                              'HI_s_edges': len(gas['s_edges_kpc2']), 'HI_support_radius_kpc': gas['support_radius_kpc'],
                              'HI_integrated_mass_Msun': gas['integrated_mass_Msun'], 'HI_helium': gas['helium'],
                              'stellar_nodes': st['node_count'], 'stellar_last_radius_kpc': float(st['radius_kpc'][-1]),
                              'stellar_height_kpc': st['height_kpc'], 'stellar_outer_scale_kpc': st['outer_scale_kpc']}
    m = load['manifest']
    out['manifest'] = {'n_rows': len(m['rows']), 'query_ids': [r['query_id'] for r in m['rows']],
                       'Rad_text': [r['Rad_text'] for r in m['rows']], 'units': sorted({r['Rad_unit'] for r in m['rows']}),
                       'emitted_columns': m['emitted_columns'], 'no_other_columns_emitted': m['no_other_columns_emitted'],
                       'reference_distance_Mpc_text': m['reference_distance']['rotmod_header']['value_text'],
                       'not_included': m['not_included'],
                       'ids_are_Q01_Q43_in_order': [r['query_id'] for r in m['rows']] == ['NGC3198-Q%02d' % i for i in range(1, 44)]}
    src_ok = Path(tail['source']['path']) == Path(NGC_DATA['h2_source'][0]) and tail['source']['sha256'] == NGC_DATA['h2_source'][1]
    rows = load['h2_source']['S1_alternative_and_stellar_median_rows']['rows'][:10]
    out['h2'] = {'tail_source_pin_matches_config': src_ok, 'outer_scale_kpc': tail['outer_scale_kpc'], 'tail_rule': tail['tail'],
                 'detected_centres_used': len(rows),
                 'radius_literals_kpc': [r['radius_kpc_literal']['value'] for r in rows],
                 'helium_already_included': all(r['conventions']['gas_helium']['value'] == 'ALREADY_INCLUDED' for r in rows)}
    for k in ('physical_source_state_binding', 'stellar_photometry_nodes', 'source_only_bundle', 'h2_source'):
        o = load[k]
        out.setdefault('headers', {})[k] = {'schema': o.get('schema'), 'status': o.get('status'), 'top_keys': sorted(o)[:20]}
    out['velocity_like_key_names'] = {k: _key_scan(v) for k, v in load.items()}
    out['not_opened'] = [m['source']['path']]
    return out


def ngc_prep_local_modules():
    """Modules NGC prep v001 loads by path INSIDE prepare_inputs (not module-global pins): it records
    their sha at load and the composite adapter re-verifies that record from bytes; neither checks
    them against a reviewed list.  Reported here with sha from bytes and a scipy scan."""
    import re
    text = Path(NGC_CODE['prep'][0]).read_text()
    prep = exec_verified(NGC_CODE['prep'][0], NGC_CODE['prep'][1], 'c2v002_ngc_prep_locals')
    base = {'HERE': prep.HERE, 'HC': prep.HC, 'HP': prep.HP}
    paths = [base[a] / b for a, b in re.findall(r"\b(HERE|HC|HP)/'([^']+\.py)'", text)] + [prep.KERNEL]
    pat = re.compile(r'^\s*(import\s+scipy|from\s+scipy)', re.M)
    out = []
    for pth in dict.fromkeys(paths):
        ok = Path(pth).is_file()
        out.append({'path': str(pth), 'exists': ok, 'sha256': sha256_file(pth) if ok else None,
                    'scipy_import': bool(ok and pat.search(Path(pth).read_text()))})
    return out


def ngc_caller_contract_check():
    """Deciding evidence for the route-A blocker, using only inert definitions of the real modules
    and a synthetic caller dict (no solver, no checkpoint directory, no project data)."""
    import inspect
    res = {}
    texts = {k: Path(NGC_CODE[k][0]).read_bytes() for k in ('worker', 'binding', 'composite')}
    res['physical_parameters_or_numerical_controls_written_by'] = {
        k: (b'physical_parameters' in t or b'numerical_controls' in t) for k, t in texts.items()}
    res['ddo_stable_binding_v002_writes_them'] = b"identity['physical_parameters']" in Path(NGC_EVIDENCE['ddo_stable_binding_v002'][0]).read_bytes()
    # caller identity keys exactly as the NGC worker builds them, plus binding/adapter additions
    w = texts['worker'].decode()
    built = all(s in w for s in ("caller_identity=dict(", "seed={'path'", "code_pins=pins", "worker={'path'", "boundary_prescription="))
    caller = {'seed': {'path': 'SYNTHETIC', 'sha256': '0' * 64}, 'code_pins': {'/synthetic.py': '0' * 64},
              'worker': {'path': 'SYNTHETIC', 'sha256': '0' * 64}, 'boundary_prescription': 'synthetic',
              'composite_full_driver': {}, 'composite_source_binding': {}}
    cm = exec_verified(AUX['checkpoint_module'][0], AUX['checkpoint_module'][1], 'c2v002_ngc_ckpt_c2v003')
    try:
        cm._identity(solver_file=str(AUX['solver'][0]), inputs={}, caller=caller, fixed=None)
        verdict = 'NO_ERROR (unexpected)'
    except Exception as exc:
        verdict = '%s: %s' % (type(exc).__name__, exc)
    res['c2v003_identity_on_ngc_caller_keys'] = {'worker_builds_these_keys': built, 'caller_keys': sorted(caller), 'result': verdict}
    for k in ('checkpoint_c2v001', 'checkpoint_c2v002'):
        m = exec_verified(NGC_EVIDENCE[k][0], NGC_EVIDENCE[k][1], 'c2v002_ngc_' + k)
        res[k + '_FIXED_SOURCE_SELECTION_IDENTITY'] = getattr(m, 'FIXED_SOURCE_SELECTION_IDENTITY', None)
    s = exec_verified(NGC_EVIDENCE['solver_nonfixedsrc'][0], NGC_EVIDENCE['solver_nonfixedsrc'][1], 'c2v002_ngc_solver_nf')
    res['nonfixedsrc_solver_accepts_fixed_source_fourier_J'] = 'fixed_source_fourier_J' in inspect.signature(s.solve).parameters
    res['adapter_always_passes_fixed_source_fourier_J'] = b"fixed_source_fourier_J=prepared['fixed_source_fourier_J']" in texts['composite']
    prec = json.loads(Path(NGC_EVIDENCE['ddo_precedent_failure'][0]).read_text())
    res['precedent'] = {'run': str(NGC_EVIDENCE['ddo_precedent_failure'][0]), 'type': prec['type'], 'message': prec['message'],
                        'elapsed_seconds': prec['elapsed_seconds'],
                        'note': 'DDO stable-cached binding v001 lacked the same contract; v002 added it and then ran (RUN_V002)'}
    blocked = (verdict.startswith('CheckpointError') and 'physical_parameters' in verdict
               and not any(res['physical_parameters_or_numerical_controls_written_by'].values())
               and res['checkpoint_c2v001_FIXED_SOURCE_SELECTION_IDENTITY'] is not True
               and res['checkpoint_c2v002_FIXED_SOURCE_SELECTION_IDENTITY'] is not True
               and not res['nonfixedsrc_solver_accepts_fixed_source_fourier_J'] and res['adapter_always_passes_fixed_source_fourier_J'])
    res['verdict'] = ('ROUTE_A_BLOCKED: every existing solver/checkpoint pairing fails before any column work '
                      '(fixedsrc+c2v003: caller contract; fixedsrc+c2v001/2: no fixed-source identity; '
                      'non-fixedsrc solver: no fixed_source_fourier_J parameter)') if blocked else 'NOT_DEMONSTRATED'
    res['blocked'] = blocked
    return res


def ngc_route_b_table():
    rows = []
    driver_text = Path(__file__).read_text()
    for stage, key, needles, hard, ngc, status in NGC_ROUTE_B_HARDCODING:
        if key is None:  # the driver's own DDO configuration (lines above the NGC section)
            path, text = Path(__file__), driver_text.split('# ' + '=' * 77 + ' NGC3198 (c2v002)')[0]
        else:
            path = (SCRIPTS.get(key) or AUX.get(key))[0]
            text = Path(path).read_text()
        lines = text.splitlines()
        loc = {n: [i + 1 for i, ln in enumerate(lines) if n in ln][:6] for n in needles}
        rows.append({'stage': stage, 'file': str(path), 'needle_lines': loc, 'ddo_hard_coding': hard,
                     'ngc_equivalent': ngc, 'status': status})
    return rows


def ngc_stage_plan(seed_path, seed_sha, stages_dir):
    d = Path(stages_dir) / '01_route_a_ngc43'
    script, sha = NGC_CODE['worker']
    argv = ['--seed', str(seed_path), '--seed-sha256', seed_sha, '--solver', str(AUX['solver'][0]), '--solver-sha256', AUX['solver'][1],
            '--checkpoint-module', str(AUX['checkpoint_module'][0]), '--checkpoint-module-sha256', AUX['checkpoint_module'][1],
            '--outdir', str(d / 'attempt_000'), '--checkpoint-directory', str(d / 'checkpoint'), '--start-iteration', '0']
    plan = [{'name': 'route_a_ngc43', 'kind': 'route_a_ngc43', 'script': str(script), 'script_sha256': sha, 'argv': argv,
             'command': [PY, '-I', '-B', str(script)] + argv, 'executed': False,
             'status': 'PLANNED_BLOCKED (see caller_contract_check)',
             'cost_estimate': 'ESTIMATE_NOT_MEASURED: DDO route A = 1594 s for 72x8 = 576 gas columns, 12 queries; NGC has up to '
                              '51x4x8 = 1632 gas columns and 43 queries, so roughly 1.3-1.5 h serial if column work dominates'}]
    for name in ('reference', 'body', 'offset', 'fs_columns', 'fs_rotation', 'fs_feedback', 'rfs_columns',
                 'le_columns', 'le_rotation', 'le_feedback', 'le_column_mean'):
        plan.append({'name': name, 'kind': name, 'executed': False, 'status': 'BLOCKED_NO_REVIEWED_NGC_STAGE (see route_b_hardcoding)'})
    return plan


def ngc_read_route_a_result(result_path, finish_path, manifest_path=None):
    """Read a (future) NGC43 route-A result: 43 speeds keyed NGC3198-Q01..Q43 in manifest order,
    validity, and DIAGNOSTIC m>=1 content of the azimuth-resolved trial (no acceptance threshold).
    Reads only the worker's own outputs and the target-free manifest."""
    import numpy as np
    manifest_path = manifest_path or NGC_DATA['manifest'][0]
    man = json.loads(Path(manifest_path).read_text())
    ids = [r['query_id'] for r in man['rows']]
    rad = {r['query_id']: r['Rad_text'] for r in man['rows']}
    reasons = []
    fin = json.loads(Path(finish_path).read_text())
    if fin.get('status') != 'RETURNED_ACTUAL_RESULT':
        reasons.append('worker status %s' % fin.get('status'))
    if sha256_file(result_path) != fin.get('result_sha256'):
        reasons.append('result sha256 differs from worker finish.json')
    x = json.loads(Path(result_path).read_text())['result']['result']
    rows = x['rows']
    if [r['id'] for r in rows] != ids:
        reasons.append('row ids are not the 43 manifest ids in order')
    speeds = [r['speed_km_s'] for r in rows]
    if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in speeds):
        reasons.append('nonfinite speed')
    if x.get('source_fixed_point', {}).get('converged_finite_fixed_point') is not True:
        reasons.append('route-A source fixed point not converged')
    if x.get('predictions_available') is not True:
        reasons.append('predictions_available is not True')
    per_q, gmax = [], {}
    for q in x.get('query_physics', []):
        nodes = q['nodes']
        n = len(nodes)
        phi = np.array([nd['phi_rad'] for nd in nodes])
        v = np.array([nd['v'] for nd in nodes], dtype=float)
        equal = bool(np.allclose(phi, 2 * np.pi * np.arange(n) / n, rtol=0, atol=1e-12))
        F = np.abs(np.fft.rfft(v))
        ratios = {'m%d' % m: (float(F[m] / F[0]) if F[0] > 0 else None) for m in range(1, len(F))}
        for k, val in ratios.items():
            if val is not None:
                gmax[k] = max(gmax.get(k, 0.0), val)
        eul = np.array([nd['Euler_covector_residual_R_phi_z'] for nd in nodes], dtype=float)
        cont = [abs(r) for nd in nodes for r in nd['mass_continuity']['fractional_density_rate_per_s']]
        per_q.append({'id': q['id'], 'n_azimuths': n, 'equal_angle_nodes': equal,
                      'speed_m_s_azimuth_harmonic_ratio': ratios,
                      'speed_m_s_azimuth_range': float(v.max() - v.min()),
                      'Euler_residual_abs_max_R_phi_z': [float(a) for a in np.max(np.abs(eul), axis=0)],
                      'continuity_fractional_rate_abs_max_per_s': float(max(cont)) if cont else None})
    valid = not reasons and len(rows) == 43
    return {'rows': [{'id': r['id'], 'Rad_text_kpc': rad.get(r['id']), 'speed_km_s': r['speed_km_s']} for r in rows],
            'speeds_km_s': {r['id']: r['speed_km_s'] for r in rows}, 'valid': valid, 'reasons': reasons,
            'validity_definition': 'worker RETURNED_ACTUAL_RESULT, result sha matches, 43 manifest ids in order, finite speeds, '
                                   'converged source fixed point, predictions_available',
            'm_ge_1_diagnostics': {'quantity': '|FFT_m(v)|/|FFT_0(v)| of the circular trial speed over the observation azimuths; '
                                               'max |Euler residual| (R,phi,z) and |continuity rate| per query',
                                   'global_max_harmonic_ratio': gmax, 'per_query': per_q, 'status': 'DIAGNOSTIC_ONLY'},
            'dynamics_status': x.get('dynamics_status'), 'accepted_for_calibration': False, 'route': 'ROUTE_A_ONLY (route B blocked)'}


def _ngc_collect(nspec, inputs_dir, writer):
    pins, review = ngc_static_pins(nspec)
    sources = ngc_sources_summary()
    seed = ngc_seed(nspec)
    seed_path, seed_sha = writer(Path(inputs_dir) / 'seed_ngc_c2v002.json', seed)
    grid = nspec['numerics']['composite_grid_spec'] or seed['numerical_inputs']['composite_grid_spec']
    kd = {'call_length_kpc': k_domain_report(grid, nspec['numerics']['k_domain']['length_kpc']),
          'queries_44_08_kpc': k_domain_report(grid, 44.08),
          'HI_support_%.2f_kpc' % sources['profile_NGC3198']['HI_support_radius_kpc']:
              k_domain_report(grid, sources['profile_NGC3198']['HI_support_radius_kpc'])}
    return pins, review, sources, seed, seed_path, seed_sha, kd


def _ngc_blockers(contract):
    return ['NGC3198_ROUTE_A_BLOCKED: ' + contract['verdict'] + '. Needs a reviewed NGC successor of binding/worker v001 '
            '(the NGC analogue of ddo_composite_stable_cached_binding/root_worker_v002).',
            'NGC3198_ROUTE_B_BLOCKED: no reviewed NGC reference/body/offset/column/rotation/feedback/column-mean stage; '
            'every DDO stage hard-codes 72 columns and DDO sources (route_b_hardcoding).']


def ngc_run_blocked(out, nspec, spec_sha, result):
    def writer(p, obj):
        p.parent.mkdir(parents=True, exist_ok=True)
        return p, _write_x(p, obj)
    pins, review, sources, seed, seed_path, seed_sha, kd = _ngc_collect(nspec, out / 'inputs', writer)
    contract = ngc_caller_contract_check()
    plan = ngc_stage_plan(seed_path, seed_sha, out / 'stages')
    _write_x(out / 'start.json', {'schema': NGC_RESULT_SCHEMA, 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
             'pid': os.getpid(), 'driver': str(Path(__file__).resolve()), 'driver_sha256': result['driver_sha256'],
             'call_spec_sha256': spec_sha, 'normalized_spec': nspec, 'static_pins': pins,
             'scope': 'NGC3198 configuration; no stage executed; no velocity read; no score or calibration admission.'})
    result.update(schema=NGC_RESULT_SCHEMA, galaxy='NGC3198', normalized_spec=nspec, executed_stages=0,
                  identity={'seed': {'path': str(seed_path), 'sha256': seed_sha, 'status': seed['status']}},
                  ngc={'review': review, 'sources': sources, 'k_domain': kd, 'caller_contract_check': contract,
                       'stage_plan': plan, 'route_b_hardcoding': ngc_route_b_table(),
                       'output_schema': 'ngc_read_route_a_result(): 43 rows NGC3198-Q01..Q43, valid, m_ge_1_diagnostics'})
    raise Blocked(' | '.join(_ngc_blockers(contract)))


def ngc_dry_run(spec_path, raw, nspec, rd):
    rd = Path(rd).resolve()
    def writer(p, obj):
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            raise Refusal('dry-run input exists: %s' % p)
        b = (json.dumps(_jsonable(obj), indent=1, allow_nan=False) + '\n').encode()
        p.write_bytes(b)
        return p, sha256_bytes(b)
    pins, review, sources, seed, seed_path, seed_sha, kd = _ngc_collect(nspec, rd / 'simulated_call' / 'inputs', writer)
    contract = ngc_caller_contract_check()
    plan = ngc_stage_plan(seed_path, seed_sha, rd / 'simulated_call' / 'stages')
    locals_ = ngc_prep_local_modules()
    roots = [v for v in NGC_CODE.values()] + [AUX['solver'], AUX['checkpoint_module']] + \
        [(x['path'], x['sha256']) for x in locals_ if x['exists']]
    trans = transitive_pins_and_scipy(roots)
    hard = ngc_route_b_table()
    report = {'schema': 'UNT_GALAXY_M0_FORWARD_DRYRUN_NGC_C2V002', 'call_spec': str(spec_path), 'call_spec_sha256': sha256_bytes(raw),
              'driver_sha256': sha256_file(__file__), 'normalized_spec': nspec, 'executed_stages': 0,
              'static_pins': pins, 'review_custody': review, 'transitive_pins': trans, 'prep_local_modules': locals_,
              'coefficient_npz_headers': _npz_headers(nspec['coefficients']['path']), 'sources': sources,
              'seed': {'path': str(seed_path), 'sha256': seed_sha, 'status': seed['status'],
                       'parameter_provenance': seed['parameter_provenance']},
              'k_domain': kd, 'caller_contract_check': contract, 'stage_plan': plan, 'route_b_hardcoding': hard,
              'blockers': _ngc_blockers(contract)}
    report['summary'] = {
        'executed_stages': 0, 'static_pins_verified': len(pins), 'transitive_files_verified': trans['verified_files'],
        'pin_problems': trans['problems'], 'scipy_imports': trans['scipy_imports'] + [x['path'] for x in locals_ if x['scipy_import']],
        'prep_local_modules_missing': [x['path'] for x in locals_ if not x['exists']],
        'reviews': [review['worker_review_verdict'], review['binding_review_verdict']],
        'review_pins_match': review['worker_review_sha_matches'] and review['binding_review_pins_match'] and review['worker_LOCAL_equals_config'],
        'manifest_ids_Q01_Q43_in_order': sources['manifest']['ids_are_Q01_Q43_in_order'],
        'velocity_like_key_names': {k: v for k, v in sources['velocity_like_key_names'].items() if v},
        'k_domain_kmin_covered': {k: v['kmin_covered'] for k, v in kd.items()},
        'route_a_blocked': contract['blocked'], 'route_b_blocked_rows': sum(1 for r in hard if r['status'].startswith('BLOCKER')),
        'seed_sha256': seed_sha}
    lines = ['NGC3198 DRY-RUN PLAN %s  (spec %s)' % (nspec.get('label', ''), report['call_spec_sha256']), '',
             'seed (candidate, not root-selected): %s  sha256 %s' % (seed_path, seed_sha), '']
    for i, s in enumerate(plan, 1):
        lines.append('%02d %-16s %s' % (i, s['name'], s['status']))
        if s.get('command'):
            lines.append('      ' + ' '.join(str(a).replace(str(ROOT), '$ROOT').replace(str(rd), '$DRY') for a in s['command']))
            lines.append('      ' + s['cost_estimate'])
    lines += ['', 'caller contract: ' + contract['verdict'], '      c2v003 on NGC caller keys -> ' + contract['c2v003_identity_on_ngc_caller_keys']['result'],
              '      precedent: %s -> %s' % (contract['precedent']['run'].replace(str(ROOT), '$ROOT'), contract['precedent']['message']), '',
              'k-domain (kmin check; per-panel phase is diagnostic only):']
    for k, v in kd.items():
        lines.append('      %-28s L=%-8.4g need kmin<=%.4g/kpc  grid kmin=%.4g/kpc  covered=%s' % (
            k, v['length_kpc'], v['required_kmin_inverse_kpc'], v['grid_kmin_node_inverse_kpc'], v['kmin_covered']))
    lines += ['', 'route-B DDO hard-coding -> NGC equivalent:']
    for r in hard:
        lines.append('      %-18s %-40s %s' % (r['stage'], r['status'], {n: l for n, l in r['needle_lines'].items()}))
    with open(rd / 'DRYRUN_PLAN.txt', 'x') as f:
        f.write('\n'.join(lines) + '\n')
    _write_x(rd / 'DRYRUN_REPORT.json', report)
    print(json.dumps(_jsonable(report['summary']), indent=1))
    return 0


def main(argv=None):
    import argparse
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == '_stage':
        return stage_main(argv[1])
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('run')
    r.add_argument('--spec', required=True)
    r.add_argument('--outdir', required=True)
    dr = sub.add_parser('dry-run')
    dr.add_argument('--spec', required=True)
    dr.add_argument('--report-dir', required=True)
    a = ap.parse_args(argv)
    if a.cmd == 'run':
        return cmd_run(a.spec, a.outdir)
    return cmd_dry_run(a.spec, a.report_dir)


if __name__ == '__main__':
    sys.exit(main())
