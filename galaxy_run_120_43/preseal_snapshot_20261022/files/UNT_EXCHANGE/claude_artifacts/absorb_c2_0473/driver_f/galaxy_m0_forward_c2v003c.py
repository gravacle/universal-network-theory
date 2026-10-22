"""INERT parameterized clean m=0 ("route B") forward driver, Claude2 lane, dispatch 0466 (c2v003,
from c2v001 75b0c08a; see INTERFACE_V003_DELTA.md).  c2v003 changes ONLY: (1) route-A prep V008
(budget 96) for grids > 80 nodes/axis, V007 kept for <= 80; (2) the declared P-88 grids G3/G4/GR
accepted; (3) mask-fired assertion after the offset stage; (4) CHECK_V001 annotation/trivial fixes.
c2v003b (from c2v003 b052e3ae; see INTERFACE_V003B_DELTA.md) changes ONLY: DDO154 distance_Mpc is a call-spec
nuisance (per-call source profile, monotone source and column-mean binding derived by the formulas that
produced the pinned files); inclination_deg stays registered-only (66 deg), refused with the documented
gas re-deprojection blocker.  At the registered 4.04 Mpc / 66 deg nothing new is planned or written.
c2v003c (from c2v003b 7ce59e05) changes ONLY the four RD1 driver defects (REVIEW_RD1_spec_parameters_V001 F1-F4):
F1 route-A outcome classified from its own result.json (status ROUTE_A_NO_FIXED_POINT with the solver failure,
vs BLOCKED ROUTE_A_ITERATION_NOT_4 naming the converged iteration); F2 run outdir / dry-run report dir made
absolute (os.path.abspath, no symlink resolution) and every planned request path refused if relative; F3 bracket
override keys must be canonical ASCII decimal ('0' or [1-9][0-9]*); F4 route-A custody checks background mu/C.

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
    # c2v003: ddo_actual_initial_source_preparation_v008.py bb05f97452cec43e215fa0853b0674262eb54c75de524b5a640cd984cd137e62
    # differs from V007 only at line 130 (node budget nk>80 -> nk>96); reviewed PASS_SCOPED in
    # CURRENT_SOURCE_ALL_PANEL_DERIVATIVE_AUDIT_REVIEW_V001.json (PREP_V008_REVIEW).  Used ONLY for grids > 80 nodes/axis.
    'prep_v008': (HC / 'ddo_actual_initial_source_preparation_v008.py', 'bb05f97452cec43e215fa0853b0674262eb54c75de524b5a640cd984cd137e62'),
}
PREP_V008_REVIEW = (ROOT / 'helpers/response_packet_audit/CURRENT_SOURCE_ALL_PANEL_DERIVATIVE_AUDIT_REVIEW_V001.json',
                    'aa12d69f4119983fdcfceb4809971ec08c596aeaf5630c85a51823b36332182e')
PREP_V007_MAX_AXIS_NODES = 80  # v007.py:130
PREP_V008_MAX_AXIS_NODES = 96  # v008.py:130
# Grids > 80 nodes/axis are accepted ONLY if (breaks, panel_orders, total) equal one of the declared P-88 grids
# (KMAX_MATRIX_PREREG_V001.json d5acfc2f..., grids G3/G4/GR; specs/wave1 of calibration_prep_c2_0470/kmax_convergence).
_G2_BREAKS = [-2, -1, -0.3, -0.1, -0.03, -0.01, 0, 0.01, 0.03, 0.1, 0.3, 1, 2]
DECLARED_LARGE_GRIDS = {
    'G3': ([-3] + _G2_BREAKS + [3], [6] * 14, 84),
    'G4': ([-4, -3] + _G2_BREAKS + [3, 4], [6] * 16, 96),
    'GR': (list(_G2_BREAKS), [6] + [8] * 10 + [6], 92),
}
# c2v003b: pinned inputs of the per-call DDO154 geometry derivation (read only when distance != registered).
GEOMETRY_PINS = {
    'calibration_input': (HR / 'DDO154_CURRENT_MODEL_CALIBRATION_INPUT_POPULATED_V001.json', '8fff3e433f932947c2725ac7fb769126abb87814e11eeb19723974485e98e5e7'),
    'stellar_3d': (C1 / 'GALAXY_STELLAR_3D_REFERENCE_SOURCE_V001.json', '612dc36529835e233fdda5810636ab8b99924fba9d0117b168aeeb9d1e2c449f'),
    'photometric': (HR / 'STELLAR_PHOTOMETRIC_REFERENCE_MEAN_PROFILE_V001.json', '2f31122d9f2a1e3a3a63560fcd20541e4dfcf235eefca966b2fed644702b8b6a'),
    'source_binding_v003': (C1 / 'GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json', '7cadac8b66096a9d9942e9861289a1d41bad084e13cd7ba655341eb06e6afae9'),
    'monotone_reducer': (HR / 'ddo_monotone_bernstein_source_controls_v002.py', '50edaba79af30cbc3582685861b55bb3eefdbe6fcb002ec1a4187b6913b4f83c'),
}
PROFILE_NAME = 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json'  # literal file name read by prep V007/V008 as C/PROFILE_NAME
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
        'supported': False,
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


class RouteANoFixedPoint(RuntimeError):
    """c2v003c (RD1 F1): the route-A stage returned normally (exit 0, RETURNED_ACTUAL_RESULT) but its own
    result.json records no finite source fixed point (FAILED_SOURCE_PREPARATION, ITERATION_BUDGET_EXHAUSTED, ...).
    A model outcome at this parameter point, NOT a tooling gap; carries the classification record."""

    def __init__(self, message, record):
        RuntimeError.__init__(self, message)
        self.record = record


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
    prepare() forms weighted_response = dk_weight/(2pi)^3 * x_tilde node by node.
    Scope (CHECK_V001 s3 corr. 1): route A, reference and body run UNMASKED (cube G4), so under
    sphere/cylinder the offset stage's real-space total (body full_fields + inverse(masked offset)),
    its reality/lapse/C-eigenvalue guards and the stored updated_base_arrays full_fields_complex,
    Phi0, angular_forcing_dPhi, base_residual_r0 are a MIXED field (cube G4 + masked offset).
    Downstream stages read only radial_nodes_m, K0, Sigma, RdR weights from that file; every
    Fourier packet they consume is masked consistently.  Constraint (s3 corr. 3): the cache
    module's evaluate() calls its closure-local prepare, bypassing the wrapper; only prepare()
    may be relied on (true for offset V003)."""
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


def mask_fired_check(offset_dir, shape, kmax_inverse_m):
    """c2v003 (CHECK_V001 s3 corr. 2): evidence that the mask fired.  Recompute the mask from the
    stored wavevectors of unit_response.npz and offset_prepared.npz and require every row outside
    it to be exactly 0.  Raises StageFailed('MASK_NOT_FIRED ...') otherwise; returns the record."""
    import numpy as np
    rec = {'shape': shape, 'kmax_inverse_m': kmax_inverse_m, 'files': {}}
    axis_waves = None
    for name in ('unit_response.npz', 'offset_prepared.npz'):
        p = Path(offset_dir) / name
        if not p.is_file():
            raise StageFailed('MASK_NOT_FIRED: %s missing' % p)
        with np.load(p, allow_pickle=False) as f:
            w = f['wavevectors'].copy()
            r = f['weighted_responses'].copy()
        if r.ndim < 1 or r.shape[0] != len(w):
            raise StageFailed('MASK_NOT_FIRED: %s rows %s != nodes %d' % (name, r.shape, len(w)))
        if axis_waves is None:
            axis_waves = w
        elif not np.array_equal(axis_waves, w):
            raise StageFailed('MASK_NOT_FIRED: wavevectors differ between offset npz files')
        m = truncation_mask(w, shape, kmax_inverse_m)
        out = m == 0
        flat = r.reshape(len(r), -1)
        bad = int(np.count_nonzero(np.any(flat[out] != 0, axis=1)))
        kept_zero = int(np.count_nonzero(~np.any(flat[~out] != 0, axis=1)))
        rec['files'][name] = {'sha256': sha256_file(p), 'total_nodes': int(len(m)), 'kept_nodes': int(m.sum()),
                              'outside_rows': int(out.sum()), 'outside_rows_nonzero': bad, 'kept_rows_all_zero': kept_zero}
        if bad:
            raise StageFailed('MASK_NOT_FIRED: %s has %d nonzero rows outside the %s mask (kept %d of %d nodes)'
                              % (name, bad, shape, int(m.sum()), len(m)))
    rec['kept_nodes'] = rec['files']['unit_response.npz']['kept_nodes']
    rec['total_nodes'] = rec['files']['unit_response.npz']['total_nodes']
    rec['vacuous'] = rec['kept_nodes'] == rec['total_nodes']
    rec['status'] = 'MASK_FIRED_OUTSIDE_ROWS_EXACTLY_ZERO'
    return rec


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
    # c2v003: replace single (path, sha) entries of a dict global (route-A LOCAL['prep'] only).
    for gname, items in request.get('stage_dict_items', {}).items():
        target = module.__dict__.get(gname)
        if not isinstance(target, dict):
            raise ValueError('Stage dict override target absent: ' + gname)
        for key, pin in items.items():
            old = target.get(key)
            if not (isinstance(old, tuple) and len(old) == 2):
                raise ValueError('Stage dict override entry absent: %s[%s]' % (gname, key))
            if sha256_file(pin['path']) != pin['sha256']:
                raise ValueError('Stage dict override pin mismatch: ' + pin['path'])
            target[key] = (Path(pin['path']), pin['sha256'])
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


def _abs(path, label):
    """c2v003 (CHECK_V001 further defect 3): spec paths must be absolute (stages run with cwd=stage dir)."""
    if not isinstance(path, str) or not Path(path).is_absolute():
        raise Refusal('%s must be an absolute path: %r' % (label, path))
    return path


def _canon_key(key):
    """c2v003c (RD1 F3): an override key is accepted only in the exact form the lookups use (str(int)):
    ASCII '0' or [1-9][0-9]*.  str.isdigit() also accepted '05', '071', Arabic-Indic and superscript digits,
    which were then silently not applied (or raised a bare ValueError)."""
    import re
    return isinstance(key, str) and re.fullmatch('0|[1-9][0-9]*', key) is not None


def normalize_spec(spec):
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
    # c2v003b: any finite positive distance is accepted (derive_geometry).  Inclination stays registered-only.
    if p['inclination_deg'] != geo['inclination_deg']:
        raise Refusal('UNSUPPORTED inclination %r: only the registered %.0f deg is supported (BLOCKED_GAS_REDEPROJECTION). '
                      'The DDO154 gas annuli are extracted IN the %.0f deg plane: extract_source.py bins every sky pixel by '
                      'deprojected radius with y/cos(i) before the annular masses/means exist, so another inclination '
                      'changes the pixel-to-annulus assignment, not a factor on the pinned arrays. No pinned formula or '
                      'route-B stage re-extracts the gas; the stellar cos(i)/cos64 re-facing and the sin(i)/sin64 '
                      'observation map alone would give a mixed-plane source. Distance is supported.'
                      % (p['inclination_deg'], geo['inclination_deg'], geo['inclination_deg']))
    out['physical'] = p
    coeff = spec.get('coefficients', None)
    if coeff is None:
        coeff = {'path': str(g['default_coefficients'][0]), 'sha256': g['default_coefficients'][1]}
    _strict(coeff, ('path', 'sha256'), 'coefficients')
    if not _is_hex64(coeff.get('sha256')) or not isinstance(coeff.get('path'), str):
        raise Refusal('coefficients {path, sha256(64 lowercase hex)} required')
    _abs(coeff['path'], 'coefficients.path')
    out['coefficients'] = {'path': str(Path(coeff['path'])), 'sha256': coeff['sha256']}
    num = spec.get('numerics', {})
    _strict(num, ('composite_grid_spec', 'truncation', 'picard', 'brackets', 'column_workers'), 'numerics')
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
        # c2v003: > 80 nodes/axis only for the declared P-88 grids (route-A prep V008, budget 96).
        if grid['total_axis_nodes'] > PREP_V007_MAX_AXIS_NODES:
            hit = [gid for gid, (b, o, t) in DECLARED_LARGE_GRIDS.items()
                   if br == b and po == o and grid['total_axis_nodes'] == t]
            if not hit or grid['total_axis_nodes'] > PREP_V008_MAX_AXIS_NODES:
                raise Refusal('composite grid with %d nodes/axis > %d is accepted only as a declared P-88 grid %s'
                              % (grid['total_axis_nodes'], PREP_V007_MAX_AXIS_NODES, sorted(DECLARED_LARGE_GRIDS)))
    out_num = {'composite_grid_spec': grid}
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
                if not (_canon_key(idx) and 0 <= int(idx) < g['n_columns'] and isinstance(pair, list) and len(pair) == 2
                        and 0 < _num(pair[0], key) < _num(pair[1], key)):
                    raise Refusal('%s entries must be "index": [lo, hi] (canonical ASCII index, no leading zeros): %r' % (key, idx))
        for ps, table in rule['le_factor_overrides'].items():
            if not (_canon_key(ps) and 1 <= int(ps) <= passes) or not isinstance(table, dict):
                raise Refusal('le_factor_overrides keys must be pass numbers 1..passes (canonical ASCII, no leading zeros): %r' % (ps,))
            for idx, pair in table.items():
                if not (_canon_key(idx) and 0 <= int(idx) < g['n_columns'] and isinstance(pair, list) and len(pair) == 2
                        and 0 < _num(pair[0], 'le override') < _num(pair[1], 'le override')):
                    raise Refusal('le_factor_overrides entries must be "index": [lo, hi] (canonical ASCII index, no leading zeros): %r' % (idx,))
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
                _abs(item.get('path'), label + ' path')
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
        _abs(a.get('attempt_directory'), 'admit.route_a.attempt_directory')
        _abs(a.get('checkpoint_directory'), 'admit.route_a.checkpoint_directory')
        norm_adm['route_a'] = {k: str(a[k]) for k in ('attempt_directory', 'checkpoint_directory', 'identity_sha256', 'result_sha256')}
    if adm.get('reference') is not None:
        if 'route_a' not in norm_adm:
            raise Refusal('admit.reference requires admit.route_a')
        a = adm['reference']
        _strict(a, ('directory', 'start_sha256', 'finish_sha256'), 'admit.reference')
        _abs(a.get('directory'), 'admit.reference.directory')
        norm_adm['reference'] = {k: str(a[k]) for k in ('directory', 'start_sha256', 'finish_sha256')}
    if adm.get('body') is not None:
        if 'reference' not in norm_adm:
            raise Refusal('admit.body requires admit.reference')
        a = adm['body']
        _strict(a, ('directory', 'finish_sha256'), 'admit.body')
        _abs(a.get('directory'), 'admit.body.directory')
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
    if not reusable:
        # c2v003 annotation (CHECK_V001 s2 minor): no stage reads it; only numerical_inputs is consumed.
        seed['c2_changed_fields'] = {
            'driver': 'galaxy_m0_forward_c2v003', 'base_seed_sha256': sha, 'changed': changed,
            'note': ('scale_seed, seed_method, scope, pins, parent_seed and quadrature_selection_evidence are copied '
                     'unchanged from the base seed and describe ITS normalization and grid, not this call; '
                     'numerical_inputs (and the physical mirrors) are the values of this call.')}
    return seed, changed, reusable


# ----------------------------------------------------------------------------- c2v003b per-call geometry
def geometry_active(nspec):
    """True when the call geometry differs from the registered one (then per-call source files are derived)."""
    reg = GALAXIES[nspec['galaxy']]['registered_geometry']
    p = nspec['physical']
    return p['distance_Mpc'] != reg['distance_Mpc'] or p['inclination_deg'] != reg['inclination_deg']


def _pinned_json(path, sha, label):
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refusal('%s pin mismatch: %s' % (label, path))
    return json.loads(raw)


def derive_geometry(gname, D, inc):
    """Per-call DDO154 inputs at distance D [Mpc] (inclination: registered value only, see normalize_spec).
    No producer script of the pinned profile exists on disk; each formula below is the documented rule and is
    GUARDED to reproduce the pinned registered records bitwise before it is applied at D:
      HI (calibration input source_conversion.distance; extract_source.py radii = angle*D, mass ~ D^2):
        lambda = D/4.3 (HI extraction distance); s_edges = (r_4.3*lambda)^2; annular means/controls unchanged;
        integrated mass = fsum(pi*1e6*ds*mean); original mass = fsum(annulus HI mass)*helium*lambda^2.
      stars (STELLAR_PHOTOMETRIC_REFERENCE_MEAN_PROFILE_V001, reference distance 4.04, face-on cos(i)):
        radius = arcsec*(D*1e3)/(arcsec per rad); Sigma = Sigma_64*cos(i)/cos(64) (distance-free);
        Rd and h = Rd/7.3 are angular scales converted with D: x D/4.04; masses x (D/4.04)^2; midplane x 1/(D/4.04).
      observation (column-mean binding): radius_m = r_catalogue*(D/4.04)*kpc_m; physical inclination radians(i).
      monotone source: the pinned reviewed reducer V002 re-run on the per-call HI record (saved sweeps/KKT).
    Returns (profile_obj, monotone_result, binding_obj_without_source_profile, record)."""
    if gname != 'DDO154':
        raise Refusal('per-call geometry is implemented for DDO154 only')
    g = GALAXIES[gname]
    reg = g['registered_geometry']
    if inc != reg['inclination_deg']:
        raise Refusal('inclination %r: BLOCKED_GAS_REDEPROJECTION (see normalize_spec)' % (inc,))
    if not (isinstance(D, float) and math.isfinite(D) and D > 0):
        raise Refusal('distance_Mpc must be a finite positive float')
    prof = _pinned_json(g['profile'][0], g['profile'][1], 'profile')
    cal = _pinned_json(*GEOMETRY_PINS['calibration_input'], 'calibration input')
    s3 = _pinned_json(*GEOMETRY_PINS['stellar_3d'], 'stellar 3D source')['galaxies']['DDO154']
    ph = _pinned_json(*GEOMETRY_PINS['photometric'], 'photometric reference')
    base_bind = _pinned_json(g['column_mean_binding'][0], g['column_mean_binding'][1], 'column-mean binding')
    base_mono = _pinned_json(g['monotone_source'][0], g['monotone_source'][1], 'monotone source')
    old = prof['galaxies']['DDO154']
    na = cal['source_HI']['NA']
    pg = ph['galaxies']['DDO154']
    nodes = [x for x in pg['nodes'] if x['reference_included']]
    D_hi = float(cal['geometry']['source_distance_Mpc'])       # HI extraction distance (4.3)
    D_st = float(pg['distance_Mpc_reference'])                  # photometric reference distance (4.04)
    i_st = float(pg['inclination_deg_reference'])               # photometric face-on reduction inclination (64)
    D_rows = {float(x['reference_distance_Mpc']) for x in cal['response_rows']}
    n = int(na['complete_prefix']['bin_count'])
    if (D_hi != reg['HI_original_distance_Mpc'] or float(na['reference_geometry']['distance_pc']) != D_hi * 1e6
            or D_st != reg['distance_Mpc'] or D_rows != {reg['distance_Mpc']} or i_st != reg['released_inclination_deg']
            or old['geometry']['distance_Mpc'] != reg['distance_Mpc'] or n != len(old['HI_plus_He']['annular_means_Msun_pc2'])
            or len(nodes) != len(s3['radius_kpc'])):
        raise Refusal('geometry source reference values differ from the registered geometry')
    he = float(na['reference_geometry']['helium_factor'])
    r_hi = [float(na['r_lo_kpc'][0])] + [float(x) for x in na['r_hi_kpc'][:n]]
    arcsec_rad = float(ph['normalization']['angular_arcsec_per_radian'])

    def hi_edges(Dx):
        lam = Dx / D_hi
        return lam, [(x * lam) ** 2 for x in r_hi]

    def star_radius(Dx):
        return [float(x['radius_literal']) * (Dx * 1e3) / arcsec_rad for x in nodes]

    def faceon(ix):
        return math.cos(math.radians(ix)) / math.cos(math.radians(i_st))

    def query_rows(Dx):
        return [{'id': x['id'], 'radius_m': float(x['radius_reference_kpc']) * (Dx / float(x['reference_distance_Mpc'])) * KPC_M}
                for x in cal['response_rows']]
    # Guards: the formulas reproduce the pinned registered records bitwise.
    f_reg = faceon(reg['inclination_deg'])
    guards = {
        'hi_edges': hi_edges(reg['distance_Mpc'])[1] == old['HI_plus_He']['s_edges_kpc2'],
        'hi_means': [float(x) * he for x in na['full_annulus']['effective_retained_HI_Msun_pc2'][:n]] == old['HI_plus_He']['annular_means_Msun_pc2'],
        'star_radius': star_radius(D_st) == s3['radius_kpc'] == old['stellar_reference']['radius_kpc'],
        'star_sigma': [s * f_reg for s in s3['surface_density_Msun_pc2']] == old['stellar_reference']['surface_density_Msun_pc2'],
        'star_scales': (s3['outer_scale_kpc'], s3['height_kpc']) == (old['stellar_reference']['outer_scale_kpc'], old['stellar_reference']['height_kpc']),
        'faceon_factor': f_reg == old['geometry']['stellar_faceon_factor_from_64deg'],
        'query_rows': query_rows(reg['distance_Mpc']) == base_bind['query_rows'],
        'binding_inclinations': (base_bind['physical_inclination_rad'], base_bind['released_inclination_rad'])
        == (math.radians(reg['inclination_deg']), math.radians(reg['released_inclination_deg'])),
    }
    if not all(guards.values()):
        raise Refusal('geometry formulas do not reproduce the pinned registered files: %s' % sorted(k for k, v in guards.items() if not v))
    lam, edges = hi_edges(D)
    mu = D / D_st
    f = faceon(inc)
    gas = dict(old['HI_plus_He'])
    gas['s_edges_kpc2'] = edges
    gas['integrated_mass_Msun'] = math.fsum(math.pi * 1e6 * (b - a) * m for a, b, m in zip(edges, edges[1:], gas['annular_means_Msun_pc2']))
    gas['original_retained_mass_scaled_Msun'] = math.fsum(na['full_annulus']['mass_Msun'][:n]) * he * lam ** 2
    gas['relative_mass_pairing_difference'] = (abs(gas['integrated_mass_Msun'] - gas['original_retained_mass_scaled_Msun'])
                                               / gas['original_retained_mass_scaled_Msun'])
    gas['support_radius_kpc'] = r_hi[-1] * lam
    star = dict(old['stellar_reference'])
    star['radius_kpc'] = star_radius(D)
    star['surface_density_Msun_pc2'] = [s * f for s in s3['surface_density_Msun_pc2']]
    star['midplane_density_Msun_pc3'] = [x * f / mu for x in s3['midplane_density_Msun_pc3']]
    star['outer_scale_kpc'] = s3['outer_scale_kpc'] * mu
    star['height_kpc'] = s3['height_kpc'] * mu
    for k in ('mass_within_last_node_Msun', 'assumed_exponential_tail_mass_Msun', 'total_reference_stellar_mass_Msun'):
        star[k] = s3[k] * f * mu ** 2
    geom = dict(old['geometry'])
    geom.update(distance_Mpc=D, inclination_deg=inc, radial_distance_scale=lam, stellar_faceon_factor_from_64deg=f,
                released_velocity_reference_factor=math.sin(math.radians(inc)) / math.sin(math.radians(reg['released_inclination_deg'])))
    note = {'driver': 'galaxy_m0_forward_c2v003b', 'distance_Mpc': D, 'inclination_deg': inc,
            'note': 'Per-call copy; only the DDO154 geometry-dependent fields are re-derived (derive_geometry docstring).'}
    profile = dict(prof)
    profile['galaxies'] = dict(prof['galaxies'], DDO154=dict(old, geometry=geom, HI_plus_He=gas, stellar_reference=star))
    profile['c2_geometry'] = dict(note, base={'path': str(g['profile'][0]), 'sha256': g['profile'][1]})
    red = exec_verified(GEOMETRY_PINS['monotone_reducer'][0], GEOMETRY_PINS['monotone_reducer'][1], 'c2v003b_monotone_reducer')
    mono = red.reduce_source(record=gas, max_sweeps=base_mono['diagnostics']['max_sweeps'],
                             kkt_tolerance=base_mono['diagnostics']['normalized_kkt_tolerance'])
    if mono.get('status') != base_mono['status']:
        raise Refusal('GEOMETRY_MONOTONE_SOURCE_NOT_ADMITTED: reviewed reducer returned %s' % mono.get('status'))
    mono['worker_sha256'] = GEOMETRY_PINS['monotone_reducer'][1]
    mono['model_choice'] = base_mono['model_choice']
    mono['c2_geometry'] = dict(note, base={'path': str(g['monotone_source'][0]), 'sha256': g['monotone_source'][1]})
    binding = dict(base_bind, query_rows=query_rows(D), distance_Mpc=D, physical_inclination_rad=math.radians(inc))
    binding['c2_geometry'] = dict(note, base={'path': str(g['column_mean_binding'][0]), 'sha256': g['column_mean_binding'][1]})
    ctrl = all(mono['source_record'][k] == base_mono['source_record'][k] for k in ('boundary_controls_Msun_pc2', 'middle_controls_Msun_pc2'))
    record = {'distance_Mpc': D, 'inclination_deg': inc, 'hi_lambda_D_over_4p3': lam, 'length_scale_D_over_4p04': mu,
              'stellar_faceon_factor': f, 'registered_formula_guards': guards,
              'monotone_controls_bitwise_equal_to_registered': ctrl,
              'unchanged_numerics': 'seed numerical controls (kpc-valued search/step/limits), composite k grid and column '
                                    'solver template are numerical choices and are NOT rescaled with D',
              'route_a_rows': ('NOT AT CALL GEOMETRY: prep V007/V008 reads the 12 query radii at %.2f Mpc from the calibration '
                               'input and the route-A binding hard-codes radians(66)/radians(64); route-A rows are a '
                               'diagnostic only. The route-B rows use the per-call binding.' % reg['distance_Mpc'])}
    return profile, mono, binding, record


def _write_bytes_x(ctx, path, raw):
    if ctx.mode == 'run':
        with open(path, 'xb') as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
    else:
        if Path(path).exists():
            raise Refusal('dry-run input exists: %s' % path)
        Path(path).write_bytes(raw)
    return sha256_file(path)


def geometry_inputs(ctx, nspec):
    """c2v003b: None at the registered geometry (pinned files; plan unchanged).  Otherwise write the per-call
    inputs under <out>/inputs: geometry_C/{PROFILE_NAME, byte copy of source binding V003} (the prep reads both
    as C/<name>), geometry_monotone_source.json and geometry_column_mean_binding.json."""
    if not geometry_active(nspec):
        return None
    p = nspec['physical']
    profile, mono, binding, record = derive_geometry(nspec['galaxy'], p['distance_Mpc'], p['inclination_deg'])
    gdir = ctx.out / 'inputs' / 'geometry_C'
    gdir.mkdir(parents=True, exist_ok=False)
    ppath, psha = ctx.write_input('geometry_C/' + PROFILE_NAME, profile)
    bpath, bsha = GEOMETRY_PINS['source_binding_v003']
    raw = Path(bpath).read_bytes()
    if sha256_bytes(raw) != bsha or _write_bytes_x(ctx, gdir / Path(bpath).name, raw) != bsha:
        raise Refusal('source binding V003 copy pin mismatch')
    mono['input'] = {'path': str(ppath), 'sha256': psha, 'record': 'galaxies.DDO154.HI_plus_He'}
    mpath, msha = ctx.write_input('geometry_monotone_source.json', mono)
    binding['source_profile'] = {'path': str(ppath), 'sha256': psha}
    cpath, csha = ctx.write_input('geometry_column_mean_binding.json', binding)
    record['files'] = {'C_directory': str(gdir), 'profile': [str(ppath), psha], 'source_binding_v003_copy': [str(gdir / Path(bpath).name), bsha],
                       'monotone_source': [str(mpath), msha], 'column_mean_binding': [str(cpath), csha]}
    return {'C_dir': str(gdir), 'profile': (str(ppath), psha), 'monotone': (str(mpath), msha),
            'binding': (str(cpath), csha), 'record': record}


def _relative_request_paths(req):
    """c2v003c (RD1 F2): every path a stage request hands to the child that is not absolute.  Paths are the
    script, argv values (any value that is not a number, a 64-hex digest or a simulate-mode PENDING token),
    __path__/__pathdict__/__ordered__ path entries of stage globals and module patches, module-patch and
    dict-item paths, and the mask's module paths."""
    found = []

    def chk(v):
        if isinstance(v, (str, Path)) and not str(v).startswith('PENDING') and not Path(str(v)).is_absolute():
            found.append(str(v))

    def val(v):
        if isinstance(v, dict) and len(v) == 1:
            (k, x), = v.items()
            if k == '__path__':
                chk(x)
            elif k in ('__pathdict__', '__ordered__'):
                for item in x:
                    chk(item[0])
    chk(req.get('script'))
    argv = [str(a) for a in req.get('argv', [])]
    for i, a in enumerate(argv):
        if a.startswith('--') or i == 0 or not argv[i - 1].startswith('--'):
            continue
        try:
            float(a)
            continue
        except ValueError:
            pass
        if not _is_hex64(a):
            chk(a)
    for v in (req.get('stage_globals') or {}).values():
        val(v)
    for p in req.get('module_patches') or []:
        chk(p.get('path'))
        for v in (p.get('set') or {}).values():
            val(v)
    for items in (req.get('stage_dict_items') or {}).values():
        for pin in items.values():
            chk(pin.get('path'))
    for key in ('checkpoint_module', 'cache_module'):
        if req.get('mask'):
            chk(req['mask'][key][0])
    return found


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
        self.route_a_outcome = None  # c2v003c (RD1 F1): classification of the route-A result.json (run result only)

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
        for req, d in zip(requests, stage_dirs):  # c2v003c (RD1 F2): every mode, before anything is launched
            bad = _relative_request_paths(req) + ([str(d)] if not Path(d).is_absolute() else [])
            if bad:
                raise Refusal('RELATIVE_PATH_IN_REQUEST %s: stages run with cwd=<stage dir>, so relative paths %s '
                              'would not resolve (use an absolute outdir/report dir and absolute spec paths)' % (req['name'], bad[:5]))
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


ROUTE_A_CONVERGED = 'CONVERGED_FINITE_FIXED_POINT'


def route_a_outcome_record(ra, result_path):
    """c2v003c (RD1 F1): classify a route-A attempt from ITS OWN result.json (worker v002 writes it, exit 0, for
    every solver outcome).  Layout: result.result = prediction v005 return; its source_fixed_point = the solver
    return, whose checkpoint.outcome is the solver outcome token and whose history[-1].iteration is the last
    completed iteration.  Pure: returns the record, raises nothing except StageFailed on an unreadable layout."""
    try:
        pred = ra['result']['result']
        sfp = pred.get('source_fixed_point')
        if not isinstance(sfp, dict):
            raise TypeError('source_fixed_point absent')
        hist = sfp.get('history') or []
        outcome = (sfp.get('checkpoint') or {}).get('outcome')
        conv_flag = sfp.get('converged_finite_fixed_point')
        rec = {'result_path': str(result_path), 'result_sha256': sha256_file(result_path), 'outcome': outcome,
               'converged_finite_fixed_point': conv_flag, 'predictions_available': pred.get('predictions_available'),
               'iterations_completed': [h.get('iteration') for h in hist],
               'last_completed_iteration': hist[-1].get('iteration') if hist else None,
               'reason': pred.get('reason'), 'solver_scope': sfp.get('scope')}
    except (KeyError, TypeError, AttributeError, IndexError) as exc:
        raise StageFailed('ROUTE_A_RESULT_UNREADABLE %s: %s: %s' % (result_path, type(exc).__name__, exc))
    f = sfp.get('failure')
    if isinstance(f, dict):
        rec['failure'] = {k: f.get(k) for k in ('type', 'message', 'iteration', 'column_index', 'stage')}
    if conv_flag is True and outcome == ROUTE_A_CONVERGED and rec['predictions_available'] is True:
        rec['classification'] = 'CONVERGED'
        rec['converged_iteration'] = rec['last_completed_iteration']
    elif conv_flag is not True:
        rec['classification'] = 'ROUTE_A_NO_FIXED_POINT'
        rec['converged_iteration'] = None
    else:
        rec['classification'] = 'INCONSISTENT'
        rec['converged_iteration'] = None
    return rec


def require_route_a_fixed_point(rec):
    """c2v003c (RD1 F1): no fixed point -> RouteANoFixedPoint (its own status); converged at k != 4 ->
    Blocked ROUTE_A_ITERATION_NOT_4 naming k (route-B stages hard-code iteration_0004); converged at 4 -> None."""
    if rec['classification'] == 'ROUTE_A_NO_FIXED_POINT':
        f = rec.get('failure') or {}
        raise RouteANoFixedPoint('ROUTE_A_NO_FIXED_POINT: route-A outcome %s after iterations %s%s (a result at this '
                                 'parameter point, not a tooling gap)' % (
                                     rec['outcome'], rec['iterations_completed'],
                                     '; failure %s: %s (iteration %s, column %s, stage %s)' % (
                                         f.get('type'), f.get('message'), f.get('iteration'), f.get('column_index'), f.get('stage'))
                                     if f else ''), rec)
    if rec['classification'] != 'CONVERGED':
        raise StageFailed('ROUTE_A_RESULT_INCONSISTENT: converged flag %r, outcome %r, predictions_available %r'
                          % (rec['converged_finite_fixed_point'], rec['outcome'], rec['predictions_available']))
    if rec['converged_iteration'] != 4:
        raise Blocked('ROUTE_A_ITERATION_NOT_4: route A converged at iteration %r; route-B stages hard-code '
                      'iteration_0004 (no reviewed successor)' % (rec['converged_iteration'],))


def route_a_custody(cp, seed_sha, coeff_path, call_physical, profile_sha=None, outcome=None):
    """Verify a route-A checkpoint (computed in this call or admitted) from bytes and return
    the per-call identity the route-B stages need.  The route-B stages hard-code
    iteration_0004: any other converged iteration is a BLOCKER (no reviewed successor).
    c2v003c: background mu/C custody (RD1 F4); `outcome` (route_a_outcome_record) is enforced after the
    identity/parameter/coefficient checks and before the iteration_0004 record checks (RD1 F1)."""
    import numpy as np
    cm = exec_verified(AUX['checkpoint_module'][0], AUX['checkpoint_module'][1], 'c2v001_ckpt')
    ident = _read_checkpoint_identity(cm, cp)
    caller = cm.decode(ident['identity']['caller']['record'])
    if caller['seed']['sha256'] != seed_sha:
        raise Blocked('checkpoint caller seed %s is not this call seed %s' % (caller['seed']['sha256'], seed_sha))
    if profile_sha is not None:  # c2v003b: the checkpoint must have been prepared from this call's source profile
        got = sorted(s for p, s in (caller.get('code_pins') or {}).items() if Path(p).name == PROFILE_NAME)
        if got != [profile_sha]:
            raise Blocked('ROUTE_A_GEOMETRY_MISMATCH: checkpoint source profile pins %s, call profile %s' % (got, profile_sha))
    phys = caller['physical_parameters']
    for k in ('Eref_J', 'ell_F_m', 'gamma'):
        if phys.get(k) != call_physical[k]:
            raise Blocked('checkpoint %s differs from call' % k)
    with np.load(coeff_path, allow_pickle=False) as f:
        grid = f['source_hessian_grid'].copy()
        mu = f['background_mu'].copy()  # c2v003c (RD1 F4)
        Cb = f['background_C'].copy()
    dig = ident['identity']['inputs_sha256']['fourier_arguments']
    if cm.digest(grid) != dig['source_hessian_grid']:
        raise Blocked('checkpoint coefficient grid differs from call coefficient grid')
    # c2v003c (RD1 F4): the same two checks offset v003 makes (array equality with the caller mubar/Cbar and the
    # operator-argument digests), made here so a mismatch blocks before the reference and body stages run.
    if not (cm.digest(mu) == dig.get('mubar') and cm.digest(Cb) == dig.get('Cbar')
            and np.array_equal(mu, phys.get('mubar')) and np.array_equal(Cb, phys.get('Cbar'))):
        raise Blocked('ROUTE_A_BACKGROUND_MISMATCH: checkpoint background mu/C differs from call coefficients '
                      '(offset v003 would refuse with Frozen background mismatch)')
    if outcome is not None:
        require_route_a_fixed_point(outcome)
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
            'caller_seed': caller['seed'], 'physical': {k: phys.get(k) for k in ('Eref_J', 'ell_F_m', 'gamma')},
            'prep_code_pins': {p: s for p, s in (caller.get('code_pins') or {}).items()
                               if 'ddo_actual_initial_source_preparation' in p}}  # c2v003: record which prep built route A


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


def require_bracket_source(H, n, tag):
    """c2v003 (CHECK_V001 further defect 1): a missing column is a stage failure, not a bare KeyError."""
    missing = sorted(set(range(n)) - set(H))
    if missing:
        raise StageFailed('%s column(s) %s failed; no bracket source' % (tag, missing[:20]))


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
    # c2v003: route-A prep by node count.  <= 80: V007 exactly as c2v001 (the worker's own LOCAL pin;
    # no override).  81..96 (declared grids only, see normalize_spec): V008 via LOCAL['prep'].
    nk = int(ni['fourier_points_per_axis'])
    if nk <= PREP_V007_MAX_AXIS_NODES:
        prep_key = 'prep'
    elif nk <= PREP_V008_MAX_AXIS_NODES:
        prep_key = 'prep_v008'
        verify_pin(PREP_V008_REVIEW[0], PREP_V008_REVIEW[1], 'prep V008 review')
    else:
        raise Refusal('%d nodes/axis exceeds every reviewed route-A prep budget (%d)' % (nk, PREP_V008_MAX_AXIS_NODES))
    prep_path, prep_sha = AUX[prep_key]
    prep_info = {'path': str(prep_path), 'sha256': prep_sha, 'axis_nodes': nk,
                 'rule': 'V007 for <=%d nodes/axis (unchanged); V008 for %d..%d (review %s)'
                         % (PREP_V007_MAX_AXIS_NODES, PREP_V007_MAX_AXIS_NODES + 1, PREP_V008_MAX_AXIS_NODES, PREP_V008_REVIEW[1][:16])}
    # c2v003b: per-call geometry inputs (None at the registered geometry: pinned files, plan unchanged).
    geo = geometry_inputs(ctx, sp)
    if geo is not None:
        info['geometry'] = geo['record']
    profile_sha = geo['profile'][1] if geo is not None else g['profile'][1]
    src_path, src_sha = geo['monotone'] if geo is not None else g['monotone_source']

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
        prep_set = {}
        if not coeff_default:
            prep_set.update({'COEFFICIENT': {'__path__': coeff_path}, 'COEFFICIENT_SHA': coeff_sha})
        if geo is not None:
            prep_set['C'] = {'__path__': geo['C_dir']}  # c2v003b: prep reads C/PROFILE_NAME and C/<binding V003>
        if prep_set:
            patches.append({'path': str(prep_path), 'sha256': prep_sha, 'set': prep_set})
        req = ctx.request('route_a', 'route_a', [
            '--seed', seed_path, '--seed-sha256', seed_sha, '--solver', AUX['solver'][0], '--solver-sha256', AUX['solver'][1],
            '--checkpoint-module', AUX['checkpoint_module'][0], '--checkpoint-module-sha256', AUX['checkpoint_module'][1],
            '--outdir', att, '--checkpoint-directory', cp, '--start-iteration', '0'], module_patches=patches)
        if prep_key == 'prep_v008':
            req['stage_dict_items'] = {'LOCAL': {'prep': {'path': str(prep_path), 'sha256': prep_sha}}}
        ctx.run_stages([req], [d])
        info['route_a'] = {'mode': 'computed', 'attempt': str(att), 'checkpoint': str(cp)}
    info['route_a']['prep'] = dict(prep_info, role=('used by this call' if info['route_a']['mode'] == 'computed' else
                                                    'expected for this grid; the admitted checkpoint records its own (custody.prep_code_pins)'))
    # c2v003c (RD1 F1): classify the route-A outcome from its own result.json before any iteration-4 verdict.
    att_res = Path(att) / 'result.json'
    ra = json.loads(att_res.read_text()) if att_res.is_file() else None
    ra_outcome = route_a_outcome_record(ra, att_res) if ra is not None else None
    ctx.route_a_outcome = ra_outcome
    if (Path(cp) / 'IDENTITY.json').is_file():
        cust = route_a_custody(cp, seed_sha, coeff_path, call_phys, profile_sha=profile_sha, outcome=ra_outcome)
        if 'route_a' in adm and cust['identity_sha256'] != adm['route_a']['identity_sha256']:
            raise Refusal('admitted checkpoint identity differs from declared')
    else:
        if ra_outcome is not None:
            require_route_a_fixed_point(ra_outcome)
        cust = {'identity_sha256': 'PENDING(route_a identity)', 'start_payload_sha256': 'PENDING',
                'g4_ref': {'file_sha256': 'PENDING'}, 'waves_ref': None}
    info['route_a']['custody'] = cust
    if ra is not None:
        info['route_a']['route_a_rows'] = ra['result']['result']['rows']
        if geo is not None:
            info['route_a']['route_a_rows_scope'] = geo['record']['route_a_rows']  # c2v003b
    ident = cust['identity_sha256']
    reuse_patch = {'path': str(reuse_path), 'sha256': reuse_sha, 'set': {'SEED_SHA': seed_sha, 'IDENTITY': ident}}
    ref_globals = {'SEED_SHA': seed_sha, 'IDENTITY': ident}
    if geo is not None:  # c2v003b: homotopy worker PROFILE (reference stage itself; body/offset read it as reuse.PROFILE)
        for target in (reuse_patch['set'], ref_globals):
            target.update(PROFILE={'__path__': geo['profile'][0]}, PROFILE_SHA=geo['profile'][1])
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
        if json.loads((ref / 'start.json').read_text())['source_custody']['sha256'] != profile_sha:  # c2v003b
            raise Blocked('REFERENCE_GEOMETRY_MISMATCH: admitted reference was not built from this call source profile')
    else:
        d = ctx.stage_dir('reference')
        ref = d / 'reference' if ctx.mode == 'run' else ctx.saved_or('reference', d / 'reference')
        req = ctx.request('reference', 'reference', common + ['--reference-module', AUX['reference_module'][0],
                          '--reference-sha256', AUX['reference_module'][1], '--outdir', ref],
                          stage_globals=ref_globals)
        ctx.run_stages([req], [d])

    # ---------------- body
    if 'body' in adm:
        body = Path(adm['body']['directory'])
        verify_pin(body / 'finish.json', adm['body']['finish_sha256'], 'admitted body finish')
        if src_sha not in json.loads((body / 'start.json').read_text())['input_pins'].values():  # c2v003b
            raise Blocked('BODY_GEOMETRY_MISMATCH: admitted body was not built from this call monotone source')
    else:
        d = ctx.stage_dir('body')
        body = d / 'body' if ctx.mode == 'run' else ctx.saved_or('body', d / 'body')
        data_pins = [[str(ref / 'start.json'), ctx.finish_sha(ref, 'start.json')], [str(ref / 'finish.json'), ctx.finish_sha(ref)],
                     [str(src_path), src_sha]]
        body_globals = {'REFERENCE': {'__path__': str(ref)}, 'DATA_PINS': {'__pathdict__': data_pins}}
        if geo is not None:
            body_globals['SOURCE'] = {'__path__': str(src_path)}  # c2v003b: per-call monotone source
        req = ctx.request('body', 'body', common + ['--outdir', body],
                          stage_globals=body_globals, module_patches=[reuse_patch])
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
    if mask is not None:
        # c2v003 (CHECK_V001 s3 corr. 2): refuse to continue unless the mask demonstrably fired.
        tinfo = {'shape': tr['shape'], 'kmax_inverse_m': kmask_m,
                 'scope': 'route A, reference and body unmasked (cube G4); offset real-space total and '
                          'updated_base_arrays full_fields/Phi0/angular_forcing/r0 are a MIXED field (see truncation_mask)'}
        if ctx.mode == 'run' or ((Path(off) / 'unit_response.npz').is_file() and (Path(off) / 'offset_prepared.npz').is_file()):
            tinfo['mask_check'] = mask_fired_check(off, tr['shape'], kmask_m)
            ctx.event(stage='offset', event='mask_check', kept_nodes=tinfo['mask_check']['kept_nodes'],
                      total_nodes=tinfo['mask_check']['total_nodes'])
        else:
            tinfo['mask_check'] = 'PENDING (offset outputs not present in simulate mode)'
        info['truncation'] = tinfo
    off_fin = ctx.finish_sha(off)
    gl = {'OFFSET_SHA': off_fin}
    # c2v003b: rotation v001/v005 read the monotone source as module globals SOURCE/SOURCE_SHA.
    rot_gl = gl if geo is None else dict(gl, SOURCE={'__path__': str(src_path)}, SOURCE_SHA=src_sha)
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
                    stage_globals=rot_gl, module_patches=[reuse_patch], mask=mask)], [d])
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
            require_bracket_source(H_fs, n, 'fs')
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
            require_bracket_source(H_prev, n, 'rfs' if p == 1 else 'le%d' % (p - 1))
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
                        stage_globals=rot_gl, module_patches=[reuse_patch], mask=mask)], [d])
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
            b_path, b_sha = geo['binding'] if geo is not None else g['column_mean_binding']  # c2v003b
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
    pins[str(PREP_V008_REVIEW[0])] = verify_pin(PREP_V008_REVIEW[0], PREP_V008_REVIEW[1], 'prep V008 review')  # c2v003
    g = GALAXIES[nspec['galaxy']]
    for key in ('base_seed', 'profile', 'monotone_source', 'column_mean_binding', 'solver_template'):
        path, sha = g[key]
        pins[str(path)] = verify_pin(path, sha, key)
    pins[nspec['coefficients']['path']] = verify_pin(nspec['coefficients']['path'], nspec['coefficients']['sha256'], 'coefficients')
    if geometry_active(nspec):  # c2v003b: inputs of the per-call geometry derivation
        for key, (path, sha) in GEOMETRY_PINS.items():
            pins[str(path)] = verify_pin(path, sha, 'geometry ' + key)
    return pins


def transitive_pins_and_scipy():
    """Load each stage script from verified bytes (inert) and verify every (path, sha) it pins;
    scan every pinned .py for a top-level scipy import."""
    import re
    seen, problems, scipy_hits = {}, [], []
    queue = [(str(p), s) for p, s in list(SCRIPTS.values()) + list(AUX.values())]
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
    # c2v003c (RD1 F2): absolute outdir (stage children run with cwd=<stage dir>); abspath, not resolve(), so an
    # absolute outdir is kept byte-for-byte (no symlink rewriting).  A relative monitor/campaign outdir resolves
    # against the driver's inherited cwd, which is the monitor's.
    out = Path(os.path.abspath(outdir))
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
            # c2v003 (CHECK_V001 further defect 2): explicit convergence-bound outcome.
            bnd = nspec['numerics']['picard']['speed_change_bound_km_s']
            chg = final.get('max_abs_change_km_s')
            result['picard_bound_met'] = None if bnd is None or chg is None else bool(chg <= bnd)
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
    except RouteANoFixedPoint as exc:  # c2v003c (RD1 F1): a model outcome, not BLOCKED
        status = 'ROUTE_A_NO_FIXED_POINT'
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
        if ctx.route_a_outcome is not None:  # c2v003c (RD1 F1): outcome + converged iteration, every status
            result['route_a_outcome'] = ctx.route_a_outcome
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
    rd = Path(os.path.abspath(report_dir))  # c2v003c (RD1 F2): planned paths absolute, as in a run
    if rd.exists():
        print('REFUSED: report dir exists', file=sys.stderr)
        return 2
    rd.mkdir(parents=True)
    raw = Path(spec_path).read_bytes()
    nspec = normalize_spec(json.loads(raw))
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
        nspec['coefficients']['sha256'] == g['default_coefficients'][1] and nspec['numerics']['picard']['passes'] == 3 and \
        not geometry_active(nspec)  # c2v003b: saved outputs exist only at the registered geometry
    saved = dict(g['saved_runs']) if repro_like else {}
    ctx = Ctx('simulate', nspec, rd / 'simulated_call', saved_runs=saved)
    info, final = execute_chain(ctx)
    report['identity'] = info
    stages = []
    for rec in ctx.records:
        row = {k: rec.get(k) for k in ('name', 'kind', 'script', 'script_sha256', 'argv', 'stage_globals', 'module_patches', 'mask', 'note')}
        if rec.get('stage_dict_items'):
            row['stage_dict_items'] = rec['stage_dict_items']  # c2v003 (route-A prep V008 only)
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
            if rec.get('stage_globals') or rec.get('module_patches') or rec.get('stage_dict_items'):
                m = exec_verified(rec['script'], rec['script_sha256'], 'c2v001_dry_' + rec['kind'])
                for name, val in (rec.get('stage_globals') or {}).items():
                    ov.append(_override_row(rec['kind'], name, m.__dict__.get(name, _ABSENT), _decode_value(val)))
                for gname, items in (rec.get('stage_dict_items') or {}).items():
                    for key, pin in items.items():
                        hard = (m.__dict__.get(gname) or {}).get(key, _ABSENT)
                        ov.append(_override_row(rec['kind'], '%s[%s]' % (gname, key), hard, (Path(pin['path']), pin['sha256'])))
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
        # c2v003 (CHECK_V001 s1 doc correction): state the count as "n of total" and name the others.
        'overrides_not_noop': ['%s %s.%s: %s' % (x['name'], o['where'], o['name'], o['verdict']) for x in stages
                               for o in (x.get('override_comparison') or []) if o['verdict'] != 'NO_OP_IDENTICAL_VALUE'],
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
            'note': 'prep V007/V008 loads these helper modules by path and RECORDS (does not verify) their SHA256; checked here from bytes'}
    report['summary']['overrides_wording'] = '%d of %d identity overrides are no-ops' % (
        report['summary']['overrides_noop_identical'], report['summary']['overrides_total'])
    report['summary']['route_a_prep'] = info.get('route_a', {}).get('prep')
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
        for gname, items in (s.get('stage_dict_items') or {}).items():
            for key, pin in items.items():
                lines.append('      dict item %s[%s] := %s %s' % (gname, key, Path(pin['path']).name, pin['sha256'][:12]))
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
