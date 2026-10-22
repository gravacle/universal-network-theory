"""prediction_freeze_c2v003g_stage0_c2v001 -- STAGE0-only successor of prediction_freeze_c2v003g_cx3v001.

Predecessor: v003g, sha256 48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405 (slots V003 pin
unchanged). Built for root V006 A142 (r3a ROOT_ITEMS M-14, adopted; prereg r3a section 6.3). Its only behavioural
change: in a Phase-2 freeze STAGE0_GRID_OUTER may read EVALUATED_BEFORE_FREEZE, exactly by the M-14 receipt rule
(every registered STAGE0 member's terminal receipt FINISHED, and this module named as the sealed successor in the
root STAGE0 status record). The successor only PERMITS EVALUATED; it never requires it, and STAGE0 never makes a
freeze refuse (v003g D9 refused a freeze that carried a STAGE0 evaluation). A Phase-1 status record reads
NOT_IN_PHASE_1. The new code is the 'STAGE0 successor' section and the lines marked 'STAGE0 successor'; every other
function and constant is AST-identical to v003g. The v003g module docstring follows unchanged.

prediction_freeze_c2v003g_cx3v001 — root-roster-bound freeze/score successor.

0545/0548: all alternative records and their order equal pinned slots V003.
Radii bind by query ID, with registered kpc units. A60 cut/gap inequalities remain
in metres, matching producer arithmetic; adjacent kpc floats can round to the same
metre float, so ulp-neighbour comparisons need not match a direct kpc comparison.
The production procedure is two-pass: obtain saved member/D1/sensitivity raw
results and their run-produced cuts; root then registers the target-free roster;
evaluate/freeze by replaying those saved results before target access.
STAGE0_GRID_OUTER is non-headline and scores only the root-listed R>=30 kpc rows.
Its currently pinned status is NOT_EVALUATED_BEFORE_FREEZE; evaluated adoption
requires a later root-approved slots/module-pin successor, never a producer flip.

0531: caller-supplied root pins, separate from the forward producer, bind each
slots V003 alternative to the target-free query roster. GL4 Q01/Q02 derive from
reviewed slots bytes; outer-cut contexts bind exact theta and certified cut bytes;
other INVALID reasons require a root-listed gate with exact string-list membership.
The writer records these pins, and verifier and scorer re-read them. The scorer
also requires the same external root pin mapping, logged before targets. These
pins are trusted external authorization inputs. Reading a pinned cut establishes
boundary custody, not physical confinement or cut certification; synthetic rosters
are explicit fixtures and are not adopted production registrations.

0518 arithmetic: all 43 rows remain in the denominator. Registered INVALID nulls
are misses; valid members are finite on every remaining row. Finite-on-INVALID
contradictions refuse even on a valid:false member. A genuine valid:false member
continues as MEMBER_INVALID, is excluded from D1 and the bands, and scores zero.
An empty valid-row set refuses. GL10 remains NOT_EVALUATED by its exact slots
alternative identity. 0535 F1/F2: outer-cut and retained-support gap INVALID rows derive from the same
hard-pinned registered GL-node roster used by the driver, in metres. The exact
outer set is R >= cut; the gap is last retained node < R < cut. Synthetic tests do
not confer scientific launch authority.

Retains v003d calibration-record admission, exact selection, integrity and LADDER
arithmetic, and v003e registered-invalid-as-miss calculations. Supersedes v003e
42a01b048d3e534f37c13cca59400a9c522c7dbb3476a95eeb5e6042adb86cbf.
"""

import datetime
import functools
import hashlib
import inspect
import json
import math
import numbers
import os
import stat

SCHEMA = 'FREEZE_MANIFEST_C2V003G_STAGE0_C2V001'   # STAGE0 successor (M-14): the manifest adds stage0_status
REGISTRATION_SCHEMA = 'FREEZE_REGISTRATION_C2V003G'
MODULE_NAME = 'prediction_freeze_c2v003g_stage0_c2v001'   # STAGE0 successor of prediction_freeze_c2v003g_cx3v001
# D3/A4: the program's target-free NGC3198 query manifest
# (UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json)
PROGRAM_QUERY_MANIFEST_SHA256 = 'a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494'
QM_ROLE_PROGRAM = 'PROGRAM_PIN'
QM_ROLE_SYNTHETIC = 'SYNTHETIC_FIXTURE'
QUERY_MANIFEST_ROLES = (QM_ROLE_PROGRAM, QM_ROLE_SYNTHETIC)
CALIBRATION_RECORD_SCHEMA = 'CALIBRATION_RUN_RECORD_C2V003'   # written by calibration_region_engine_c2v003(a)
FINGERPRINT_SCHEMA = 'EXPLORATION_FINGERPRINT_C2V003'
# X1 (v003a): the DDO154 region file layout, mirrored from the engine's load_observation_region so the
# admission rectangles are re-derived here from the file bytes
REGION_EXPECTED_ROWS = 12
REGION_ROW_NUMERIC_FIELDS = ('reference_radius_kpc', 'observed_speed_km_s', 'quoted_random_sigma_km_s',
                             'conditional_random_acceptance_low_km_s', 'conditional_random_acceptance_high_km_s')
REGION_TOP_FIELDS = ('statistical_choice', 'distance_summary', 'forward_coordinates')
SELECTION_RULE = ('members = for each identified direction (ascending index) the admitted points attaining the '
                  'minimum then the maximum projection (ties -> lowest log_index), then the anchor (the engine '
                  'primary anchor, an admitted entry), then the admitted point nearest the centroid of all '
                  'admitted projections (ties -> lowest log_index), then interior_count evenly spaced remaining '
                  'admitted points by log_index; duplicates are taken once at their first role')
UNITS = 'km/s'
SEMANTICS = 'TOTAL_OBSERVABLE'
ERROR_MODEL = 'CONDITIONAL_QUOTED_SIGMA_DIAGONAL_ONLY'
N_QUERIES = 43

WITHIN_ERROR_RULE = ('per member and per row: valid and |predicted - observed| <= quoted sigma, evaluated as '
                     '|signed_residual / sigma| <= 1; an invalid or unevaluated row never passes; counts are '
                     'over all 43 rows')
HEADLINE_RULE = ('headline = distribution (min/median/max) of the within-error counts of EVERY admitted '
                 'representative member of the PRIMARY alternative, plus the within-error count of the '
                 'REFERENCE MEMBER chosen and frozen before target access; no median or pointwise curve '
                 'is a headline (CURRENT_INSTRUCTIONS L108). All 43 rows remain in the denominator; '
                 'QUERY_INSIDE_INNERMOST_NODE, QUERY_BEYOND_OUTER_GAS_CUT, and '
                 'QUERY_OUTSIDE_RETAINED_SUPPORT are registered INVALID misses when root-rostered.')
REFERENCE_RULE = ('REFERENCE MEMBER = the evaluated member finite on every registered-valid row (registered INVALID rows remain null) and whose projection '
                  'onto the identified right vectors (unit-box u space) is nearest, in Euclidean distance, '
                  'to the centroid of ALL admitted points of the exploration in that subspace; ties -> lowest '
                  'log_index; chosen at freeze time, before target access')
ENVELOPE_LABEL = 'POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE'
SENSITIVITY_LABEL = ('BOX_LIMITED_SENSITIVITY_BAND_FROM_REFERENCE_MEMBER_NOT_A_REALIZABLE_CURVE_'
                     'NOT_HEADLINE')
INNER_SAMPLE = 'INNER_SAMPLE'
BOUNDS_SEMANTICS = 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'
U_UNITS = 'dimensionless unit-box coordinate u in [0, 1] (internal x = ln v for log, v for linear)'
BAND_SCOPE = {
    'headline': ('per-member within-error counts over all 43 rows for the admitted representative members '
                 '(PRIMARY alternative) and the frozen reference member'),
    'pointwise_envelope': ('per-query min/max over the admitted representative members of an INNER_SAMPLE of '
                           'the DDO154 admitted set; varies only the identified directions actually spanned '
                           'by the sample; near-null directions, fixed shared coordinates and NGC3198 '
                           'nuisances are held at their trial values; label ' + ENVELOPE_LABEL),
    'box_limited_sensitivity_band': ('per-query min/max over the reference member and its one-at-a-time '
                                     'displacements along every near-null direction and every '
                                     'sensitivity-declared coordinate to the computational-box ends (or the '
                                     'declared step), without DDO154 re-calibration; limited by the '
                                     'computational box, which is not an empirical bound; label '
                                     + SENSITIVITY_LABEL),
}

FREEZE_COMPLETE = 'FREEZE_COMPLETE'
FREEZE_INCOMPLETE = 'FREEZE_INCOMPLETE'
STATUS_COMPLETE = 'COMPLETE'
STATUS_BUDGET = 'BUDGET_EXHAUSTED'
ALT_EVALUATED = 'EVALUATED_BEFORE_FREEZE'
ALT_NOT_EVALUATED = 'NOT_EVALUATED_BEFORE_FREEZE'
ALT_KINDS = ('state', 'source', 'approximation')

SCOPE_SHARED = 'shared'
SCOPE_DDO = 'ddo154_nuisance'
SCOPE_NGC = 'ngc3198_nuisance'
SCOPE_DDO_FIXED = 'ddo154_fixed'   # v003b (A13): the DDO154 distance as a fixed counted constant, not a nuisance
SCOPES = (SCOPE_SHARED, SCOPE_DDO, SCOPE_NGC, SCOPE_DDO_FIXED)
KINDS = ('distance', 'inclination', 'other')
DISTANCE_REFERENCE_MPC = {SCOPE_DDO: 4.04, SCOPE_NGC: 13.8, SCOPE_DDO_FIXED: 4.04}
COORD_KEYS = frozenset({'name', 'transform', 'lower', 'upper', 'role', 'trial_value', 'units', 'scope',
                        'kind', 'reference_value', 'sensitivity'})

ROLE_ANCHOR = 'anchor'
ROLE_HULL = 'hull_vertex'
ROLE_CENTROID = 'centroid_nearest'
ROLE_INTERIOR = 'interior'
ROLES = (ROLE_HULL, ROLE_ANCHOR, ROLE_CENTROID, ROLE_INTERIOR)

SENS_NULL = 'NEAR_NULL_DIRECTION'
SENS_FIXED = 'FIXED_SHARED_COORDINATE'
SENS_NGC = 'NGC3198_NUISANCE'

# v003b: coordinate modes (root decision A13) and the NGC3198 slot geometry rulings (A16.1 / A16.4)
MODE_D_FIXED = 'DDO154_DISTANCE_FIXED_AT_REGISTERED'
MODE_D_NUISANCE = 'DDO154_DISTANCE_NUISANCE'
COORDINATE_MODES = (MODE_D_FIXED, MODE_D_NUISANCE)
DDO154_REGISTERED_DISTANCE_MPC = 4.04
A13_CONDITION = 'conditional on DDO154 D=4.04 and i=66 (A13/A23)'   # v003c: A23 readings of a miss (D and i)
GEOMETRIC_UNITS = ('Mpc', 'deg')                  # v003c (V8e-3/A23): geometric units need a geometric kind
GEOMETRIC_NAME_TOKENS = ('distance', 'inclination')
SENS_DDO_FIXED = 'DDO154_FIXED_COUNTED_CONSTANT'
FIXED_CONSTANT_STATUS = 'FIXED_COUNTED_CONSTANT_NOT_A_NUISANCE'
GEOMETRY_NOT_EXPOSED = 'GEOMETRY_NOT_EXPOSED'
HEADLINE_CONDITIONS_KEY = 'headline_conditions'
NOTES_SLOT_KEY = 'ngc3198_slot_sensitivity'
NOTES_SA_KEY = 'structural_assumptions'
SA_REQUIRED = ('SA-BH-01', 'SA-REACH-01')
SA_SECTION_A18 = 'A18'
ROOT_A13 = {'id': 'A13', 'section': 'A13 - DDO154 distance fixed at 4.04 Mpc for the headline calibration',
            'file': ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
                     'CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V003_ADDENDUM.md'),
            'sha256': '5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468', 'status': 'FROZEN_PINNED'}
ROOT_A16 = {'ids': ['A16.1', 'A16.4'], 'file_name': 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md',
            'status': 'OPEN_CITED_BY_NAME_NOT_PINNED'}
A13_ADMISSIBILITY = (   # v003c: A13 as corrected by A23 (V004 addendum, open, cited by name, not pinned); verbatim
    'A13 as corrected by A23 (ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md, open, cited by name): '
    'Fixing D_DDO154 = 4.04 Mpc is a counted assumption of the headline calibration, forced by the stage bindings '
    '(run mode at D ≠ 4.04 is BLOCKED). 4.04 Mpc is the registered route-B/catalogue distance; the region '
    'distance_summary central value is 4.0365 Mpc, with conditional 68% interval [3.981, 4.111] Mpc. For exact '
    'admitted sets, the D = 4.04 slice lies inside the projection of the 4-D admitted region. Every freeze member is '
    'an admitted point, and forward_ngc never receives the DDO154 distance. Every computed slice band therefore lies '
    'inside the exact projection envelope, and a member within error on the slice is a member within error of the '
    'projection. Nothing stronger is claimed. The frozen headline (min/median/max of the per-member counts plus the '
    'reference-member count) is not monotone under restriction, so the test is not claimed to be stricter. The '
    'computed INNER_SAMPLE estimates of two different runs are not ordered. A miss on NGC3198 is read as conditional '
    'on D_DDO154 = 4.04 Mpc and i_DDO154 = 66° until the D Jacobian column bounds that effect.')
DISTANCE_ALTERNATIVE = {
    'name': MODE_D_NUISANCE, 'kind': 'calibration_coordinate', 'status': 'NOT_EVALUATED_BEFORE_FREEZE',
    'description': ('DDO154 distance as a nuisance coordinate (the V001 4-coordinate calibration): a sensitivity only, '
                    'never a headline (A13)'),
    'deciding_work': ('stage successor gal_c2v005 + galaxy-config schema V005 (run-mode admission of the per-call DDO154 '
                      'geometry), then the D Jacobian column at two step sizes'),
    'scored': False}
A16_READING = ('A16.1/A16.4: the headline uses the registered NGC3198 geometry; the slot boxes are the declared range of '
               'a sensitivity NOT_EVALUATED_BEFORE_FREEZE. forward_ngc refuses every box-end geometry with '
               'GEOMETRY_NOT_EXPOSED, so the box-limited sensitivity band rows are invalid by design and '
               'conditional_on_trial_values.sensitivity_evaluated true for these slots reads "attempted and refused", '
               'not a zero sensitivity')
ENVELOPE_LABEL_A13 = ENVELOPE_LABEL + '; ' + A13_CONDITION
SENSITIVITY_LABEL_A13 = SENSITIVITY_LABEL + '; ' + A13_CONDITION
BAND_SCOPE_A13 = {k: v + '; ' + A13_CONDITION for k, v in BAND_SCOPE.items()}

# P46 harness FORBIDDEN set (lanes/P46_CODEX2/line_a_prediction_harness_v002.py)
# plus the four target-row names required by INTERFACE_0462_V001.
FORBIDDEN = frozenset({
    'vobs', 'vobs_km_s', 'observed_velocity', 'observed_km_s',
    'error_v_km_s', 'velocity_error', 'chi2', 'residual_km_s',
    'vgas', 'vdisk', 'vbul', 'vgas_km_s', 'vdisk_km_s', 'vbulge_km_s',
    'target_rows', 'targets', 'target_velocity', 'target_velocities',
    # S9: the scorer's own target-derived output names and the P46 row field 'velocity'
    'velocity', 'observed_speed_km_s', 'quoted_sigma_km_s', 'signed_residual_km_s', 'sigma_ratio',
    'fractional_error', 'within_error', 'within_error_count', 'member_within_error_counts',
    'member_within_error_counts_valid_members_only', 'counts_by_member', 'reference_within_error_count',
    'band_overlaps_error_bar', 'band_overlap_count', 'target_rows_sha256',
})
P46_ROW_SHAPE = frozenset({'id', 'velocity', 'sigma'})   # S9: a dict with exactly these keys is refused
_MAX_SCAN_DEPTH = 200   # S10: deeper structures are refused, never recursed

MANIFEST_KEYS = frozenset({
    'schema', 'created_utc', 'freeze_status', 'incomplete_reasons', 'parameter_region', 'admitted_region',
    'coordinates', 'observation_rule', 'query_ids', 'units', 'semantics', 'alternatives', 'members',
    'member_evaluation', 'reference_member', 'pointwise_envelope', 'sensitivity', 'band_scope',
    'conditional_on_trial_values', 'alternative_results', 'headline_rule', 'within_error_rule', 'pins',
    'notes', 'target_velocities_included', 'manifest_sha256', 'input_bindings', 'module', 'row_registration_rosters',
    'stage0_status',   # STAGE0 successor (M-14): the frozen receipt-rule record of STAGE0_GRID_OUTER
})
INPUT_BINDING_KEYS = frozenset({'query_manifest', 'observation_region', 'calibration_record'})
QM_BINDING_KEYS = frozenset({'path', 'sha256', 'role', 'is_program_pin', 'program_pin_sha256', 'query_ids_sha256',
                             'rad_unit'})
MEMBER_KEYS = frozenset({'member_id', 'point_index', 'role', 'log_index', 'u', 'identified_projection',
                         'theta_engine', 'theta_ngc', 'evaluated', 'forward_valid_flag', 'member_valid',
                         'row_valid', 'speeds_km_s', 'row_registration', 'reasons', 'exception'})
MEMBER_EVAL_KEYS = frozenset({'status', 'stage', 'budget', 'evaluations_used', 'n_selected', 'n_evaluated',
                              'n_member_valid'})
ENVELOPE_ROW_KEYS = frozenset({'id', 'band_low_km_s', 'band_high_km_s', 'n_members', 'n_valid', 'valid',
                               'label', 'n_excluded_invalid', 'n_unevaluated'})
REFERENCE_KEYS = frozenset({'member_id', 'log_index', 'rule', 'centroid_identified', 'distance', 'ranking'})
SENS_KEYS = frozenset({'status', 'stage', 'budget', 'evaluations_used', 'reference_member_id',
                       'null_direction_rule', 'evaluations', 'per_query', 'per_target', 'label'})
SENS_ENTRY_KEYS = frozenset({'entry_id', 'kind', 'target', 'side', 'displacement', 'displacement_units',
                             'limited_by', 'u_displaced', 'theta_ngc', 'skipped_zero_displacement',
                             'evaluated', 'forward_valid_flag', 'row_valid', 'speeds_km_s', 'row_registration',
                             'delta_from_reference_km_s', 'linearised_ddo_shift_sigma', 'reasons',
                             'exception'})
SENS_ROW_KEYS = frozenset({'id', 'reference_speed_km_s', 'box_limited_band_low_km_s',
                           'box_limited_band_high_km_s', 'max_abs_delta_km_s', 'n_planned', 'n_valid', 'valid',
                           'label'})
ADMITTED_REGION_KEYS = frozenset({
    'exploration_status', 'exploration_stage_reached', 'admitted_set_label', 'region_possibly_truncated',
    'truncation_evidence', 'engine_coverage_report', 'n_admitted', 'varying_engine_names', 'identified',
    'near_null', 'right_vectors', 'singular_values', 'null_space_complete', 'centroid_identified',
    'projection_range_identified', 'admitted_projections_identified', 'near_null_directions',
    'bounds_semantics', 'unit_coordinate_units',
    # v003 (D2, P34-14, P34-16)
    'selection_rule', 'selection_interior_count', 'selection_anchor_log_index', 'selected_points',
    'observation_region_sha256', 'admission_reverified', 'calibration_fingerprint',
})
PIN_KEYS = frozenset({'path', 'sha256', 'bytes'})
TARGET_ROW_KEYS = frozenset({'id', 'velocity', 'sigma'})
QUERY_MANIFEST_FIELDS = ('query_id', 'data_row_index', 'Rad_text', 'Rad_unit')
REGISTRATION_KEYS = frozenset({'schema', 'created_utc', 'manifest_path', 'expected_manifest_file_sha256',
                               'manifest_sha256_self', 'manifest_bytes', 'note', 'registration_sha256'})

_HULL_BOX_TOL = 1e-6
_ORTHO_TOL = 1e-8
_THETA_REL_TOL = 1e-9
_V_TOL = 1e-12
_FACE_TOL = 1e-9
_ZERO_DISP = 1e-12
_MAX_REASONS = 20
_MAX_REASON_CHARS = 500
# v003d (SF-1 fix 3): the engine's identification rule, re-applied here (calibration_region_engine_c2v003(a/b),
# verbatim constants and text)
ABSOLUTE_IDENTIFICATION_THRESHOLD = 2.865260238532134
MIN_NULL_TOLERANCE = 1e-6
IDENTIFICATION_RULE = ('identified iff (s_i > 0 and s_i >= effective_null_tolerance * s_max) or '
                       's_i >= ABSOLUTE_IDENTIFICATION_THRESHOLD (z = 2.865260238532134); '
                       'effective_null_tolerance = max(null_tolerance, MIN_NULL_TOLERANCE, max(m, n) * eps); '
                       'singular values are per unit of u, i.e. per computational box (box-dependent)')
_FLOAT_EPS = 2.220446049250313e-16   # numpy.finfo(float).eps (the engine's rank floor uses it)
SKIP_ZERO_DISPLACEMENT_REASON = (
    'SKIPPED: zero displacement (v003d rule: a near-null side whose box-limited step s <= 1e-12, or whose largest '
    'coordinate move s * max|d_i| <= 1e-9 because the reference member sits on a computational-box face that a '
    'component above 1e-12 of this direction points out of; a declared coordinate whose target equals its trial '
    'value)')


# --------------------------------------------------------------------------
# Generic helpers (pure, no I/O except where named)
# --------------------------------------------------------------------------

def _is_int(x):
    return isinstance(x, numbers.Integral) and not isinstance(x, bool)


def _is_real(x):
    if isinstance(x, bool) or not isinstance(x, numbers.Real):
        return False
    try:
        return math.isfinite(float(x))
    except (OverflowError, ValueError, TypeError):
        return False


def _is_hex64(s):
    if not isinstance(s, str) or len(s) != 64:
        return False
    return all(c in '0123456789abcdef' for c in s.lower())


def _sha256_hex(raw):
    return hashlib.sha256(raw).hexdigest()


def _safe_str(x):
    """str(x) that never raises (S10)."""
    try:
        return str(x)
    except Exception:
        try:
            return '<unprintable %s>' % type(x).__name__
        except Exception:
            return '<unprintable>'


def _safe_repr(x):
    try:
        return repr(x)
    except Exception:
        return _safe_str(x)


def _fail_closed(fn):
    """S10: an unanticipated exception inside a public function becomes ok=False (scorer: refused=True)."""
    sig = []   # signature computed lazily on the first call (nothing is computed at import)

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # a call that does not match the keyword-only signature is a caller bug and still raises TypeError
        # (interface: keyword-only, no defaults); only failures while executing are converted
        if not sig:
            sig.append(inspect.signature(fn))
        sig[0].bind(*args, **kwargs)
        try:
            return fn(*args, **kwargs)
        except Exception as exc:   # noqa: BLE001 -- fail closed by contract
            return {'ok': False, 'refused': True, 'status': 'INTERNAL_ERROR', 'function': fn.__name__,
                    'reasons': ['INTERNAL_ERROR (fail-closed): %s: %s' % (type(exc).__name__, _safe_str(exc))]}
    return wrapper


def _canonical_bytes(obj):
    """P34-15: canonical JSON over a key-normalised copy (int keys -> str before sorting), so the bytes are
    identical before and after a parse; json.dumps(sort_keys=True) on >= 11 integer keys would otherwise
    sort numerically and re-sort lexicographically after the parse."""
    return json.dumps(_plain(obj, 'canonical'), sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode('utf-8')


def _read_regular(path, require_nonempty):
    """Return (bytes, realpath, None) or (None, None, reason). Never raises, never blocks.

    Only a regular file is read (A4/N01): devices, FIFOs, sockets and directories refuse.
    The descriptor is opened non-blocking and fstat'ed before any read.
    """
    if not isinstance(path, str) or not path:
        return None, None, 'path must be a non-empty string'
    flags = os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0)
    try:
        fd = os.open(path, flags)
    except (OSError, ValueError) as exc:
        return None, None, 'unreadable file %r: %s: %s' % (path, type(exc).__name__, exc)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            return None, None, 'not a regular file: %r' % (path,)
        if require_nonempty and st.st_size == 0:
            return None, None, 'zero-length file refused: %r' % (path,)
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b)
        raw = b''.join(chunks)
    except (OSError, ValueError) as exc:
        return None, None, 'unreadable file %r: %s: %s' % (path, type(exc).__name__, exc)
    finally:
        try:
            os.close(fd)
        except OSError:
            pass
    if require_nonempty and len(raw) == 0:
        return None, None, 'zero-length file refused: %r' % (path,)
    return raw, os.path.realpath(path), None


def _reject_constant(name):
    raise ValueError('non-finite JSON constant %r refused' % name)


def _parse_json_bytes(raw):
    """Return (obj, None) or (None, reason). Refuses NaN/Infinity literals."""
    try:
        return json.loads(raw.decode('utf-8'), parse_constant=_reject_constant), None
    except (ValueError, UnicodeDecodeError, TypeError, RecursionError) as exc:
        return None, 'JSON parse failed: %s: %s' % (type(exc).__name__, exc)


def _plain(obj, where):
    """Return a JSON-native deep copy (dict keys become str). Raises ValueError."""
    if obj is None or isinstance(obj, (bool, str)):
        return obj
    if isinstance(obj, numbers.Integral):
        return int(obj)
    if isinstance(obj, numbers.Real):
        f = float(obj)
        if not math.isfinite(f):
            raise ValueError('non-finite number at %s' % where)
        return f
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(k, str):
                ks = k
            elif _is_int(k):
                ks = str(int(k))
            else:
                raise ValueError('non-string key at %s: %r' % (where, k))
            if ks in out:
                raise ValueError('duplicate key after normalisation at %s: %r' % (where, ks))
            out[ks] = _plain(v, where + '.' + ks)
        return out
    if isinstance(obj, (list, tuple)):
        return [_plain(v, '%s[%d]' % (where, i)) for i, v in enumerate(obj)]
    raise ValueError('non-JSON type at %s: %s' % (where, type(obj).__name__))


def _scan_forbidden(obj, where, hits, reasons):
    """S9/S10: iterative screen. Collects paths of dict keys whose lowercase form is forbidden and of dicts
    whose key set is exactly the P46 target-row shape {id, velocity, sigma}. Depth above _MAX_SCAN_DEPTH or
    a reference cycle is a refusal reason (never a RecursionError)."""
    stack = [(obj, where, 0, ())]
    while stack:
        cur, path, depth, ancestors = stack.pop()
        if not isinstance(cur, (dict, list, tuple)):
            continue
        if id(cur) in ancestors:
            reasons.append('REFUSED: %s contains a reference cycle; cannot be screened' % path)
            continue
        if depth > _MAX_SCAN_DEPTH:
            reasons.append('REFUSED: %s nested deeper than %d levels; cannot be screened' % (path, _MAX_SCAN_DEPTH))
            continue
        anc = ancestors + (id(cur),)
        if isinstance(cur, dict):
            keys = []
            for k in list(cur.keys()):
                ks = _safe_str(k)
                keys.append(ks)
                child = path + '.' + ks
                nk = ''.join(c for c in ks.lower() if c.isalnum())
                normalized_forbidden = {''.join(c for c in k if c.isalnum()) for k in FORBIDDEN}
                target_alias = ('target' in nk and any(t in nk for t in ('velocity', 'velocities', 'speed', 'rows')))
                # This required manifest boolean is a negative assertion, not a target payload.
                negative_assertion = ks == 'target_velocities_included' and cur[k] is False
                if not negative_assertion and (nk in normalized_forbidden or nk.startswith(('observed', 'vobs')) or target_alias):
                    hits.append(child)
                stack.append((cur[k], child, depth + 1, anc))
            if set(x.lower() for x in keys) == P46_ROW_SHAPE:
                hits.append(path + ' (P46 target-row shape {id, velocity, sigma})')
        else:
            for i, v in enumerate(cur):
                stack.append((v, '%s[%d]' % (path, i), depth + 1, anc))


def _safe_scan(obj, where, hits, reasons):
    try:
        _scan_forbidden(obj, where, hits, reasons)
    except Exception as exc:   # S10: a pathological container never escapes
        reasons.append('REFUSED: %s could not be screened: %s' % (where, type(exc).__name__))


def _dot(a, b):
    return math.fsum(x * y for x, y in zip(a, b))


def _median(values):
    vals = sorted(values)
    n = len(vals)
    if n == 0:
        return None
    if n % 2 == 1:
        return float(vals[n // 2])
    return float((vals[n // 2 - 1] + vals[n // 2]) / 2.0)


def _evenly_spaced_indices(m, c):
    """c evenly spaced indices in range(m), end-inclusive; all if c >= m."""
    if c <= 0 or m <= 0:
        return []
    if c >= m:
        return list(range(m))
    if c == 1:
        return [0]
    return [(i * (m - 1)) // (c - 1) for i in range(c)]


def _check_query_ids(query_ids, reasons, require_43):
    if not isinstance(query_ids, (list, tuple)):
        reasons.append('query_ids must be a list')
        return None
    ids = list(query_ids)
    if require_43 and len(ids) != N_QUERIES:
        reasons.append('query_ids must have exactly %d entries, got %d' % (N_QUERIES, len(ids)))
    if not ids:
        reasons.append('query_ids is empty')
    for i, q in enumerate(ids):
        if not isinstance(q, str) or not q:
            reasons.append('query_ids[%d] is not a non-empty string' % i)
    if len(set(q for q in ids if isinstance(q, str))) != len(ids):
        reasons.append('query_ids are not unique')
    return ids


def _cap_reasons(lst):
    out = []
    for r in list(lst)[:_MAX_REASONS]:
        s = str(r)
        out.append(s[:_MAX_REASON_CHARS])
    if len(lst) > _MAX_REASONS:
        out.append('... %d further reasons truncated' % (len(lst) - _MAX_REASONS))
    return out


def _close(a, b):
    return abs(a - b) <= _THETA_REL_TOL * max(1.0, abs(a), abs(b))


def _now_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


# --------------------------------------------------------------------------
# load_query_manifest (v001, unchanged)
# --------------------------------------------------------------------------

@_fail_closed
def load_query_manifest(*, path, expected_sha256):
    """Bind the target-free NGC3198 query manifest: ids and radii only.

    Verifies the byte hash before parsing. Binds only rows[].query_id, data_row_index, Rad_text,
    Rad_unit. Requires 43 unique ids and data_row_index exactly 1..43.
    """
    reasons = []
    out = {'ok': False, 'path': None, 'sha256': None, 'query_ids': [], 'radii_text': {},
           'rad_unit': None, 'reasons': reasons}
    if not isinstance(path, str) or not path:
        reasons.append('path must be a non-empty string')
        return out
    out['path'] = os.path.abspath(path)
    if not _is_hex64(expected_sha256):
        reasons.append('expected_sha256 must be a 64-character hex string')
        return out
    raw, _rp, err = _read_regular(path, True)
    if raw is None:
        reasons.append(err)
        return out
    actual = _sha256_hex(raw)
    out['sha256'] = actual
    if actual != expected_sha256.lower():
        reasons.append('sha256 mismatch: expected %s, actual %s' % (expected_sha256.lower(), actual))
        return out
    doc, err = _parse_json_bytes(raw)
    if doc is None:
        reasons.append(err)
        return out
    if not isinstance(doc, dict) or not isinstance(doc.get('rows'), list):
        reasons.append('manifest must be a JSON object with a rows list')
        return out
    rows = doc['rows']
    if len(rows) != N_QUERIES:
        reasons.append('rows must have exactly %d entries, got %d' % (N_QUERIES, len(rows)))
        return out
    bound = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            reasons.append('rows[%d] is not an object' % i)
            continue
        missing = [f for f in QUERY_MANIFEST_FIELDS if f not in row]
        if missing:
            reasons.append('rows[%d] missing fields %s' % (i, missing))
            continue
        qid, idx, rad_text, rad_unit = (row['query_id'], row['data_row_index'], row['Rad_text'],
                                        row['Rad_unit'])
        if not isinstance(qid, str) or not qid:
            reasons.append('rows[%d].query_id is not a non-empty string' % i)
        if not _is_int(idx):
            reasons.append('rows[%d].data_row_index is not an integer' % i)
        if not isinstance(rad_text, str) or not rad_text:
            reasons.append('rows[%d].Rad_text is not a non-empty string' % i)
        else:
            try:
                if not math.isfinite(float(rad_text)):
                    reasons.append('rows[%d].Rad_text is not finite' % i)
            except ValueError:
                reasons.append('rows[%d].Rad_text does not parse as a number' % i)
        if not isinstance(rad_unit, str) or not rad_unit:
            reasons.append('rows[%d].Rad_unit is not a non-empty string' % i)
        bound.append((idx, qid, rad_text, rad_unit))
    if reasons:
        return out
    if set(int(b[0]) for b in bound) != set(range(1, N_QUERIES + 1)):
        reasons.append('data_row_index values are not exactly 1..%d' % N_QUERIES)
    if len(set(b[1] for b in bound)) != N_QUERIES:
        reasons.append('query_id values are not unique')
    units = set(b[3] for b in bound)
    if len(units) != 1:
        reasons.append('Rad_unit is not uniform across rows: %s' % sorted(units))
    if units != {'kpc'}:
        reasons.append('Rad_unit must be the registered unit kpc')
    if reasons:
        return out
    bound.sort(key=lambda b: int(b[0]))
    out['query_ids'] = [b[1] for b in bound]
    out['radii_text'] = {b[1]: b[2] for b in bound}
    out['rad_unit'] = units.pop()
    out['ok'] = True
    return out


# --------------------------------------------------------------------------
# Coordinate spec (D10: scopes, units, NGC3198 nuisance slots, sensitivity declarations)
# --------------------------------------------------------------------------

def _build_spec(coordinates, reasons):
    """Validate the coordinate list; return the internal spec dict or None (reasons appended)."""
    if not isinstance(coordinates, (list, tuple)) or not coordinates:
        reasons.append('coordinates must be a non-empty list of coordinate dicts')
        return None
    seen = set()
    coords = []
    for k, c in enumerate(coordinates):
        where = 'coordinates[%d]' % k
        if not isinstance(c, dict):
            reasons.append('%s is not a dict' % where)
            continue
        missing = COORD_KEYS - set(c)
        extra = set(_safe_str(x) for x in c) - COORD_KEYS
        if missing or extra:
            reasons.append('%s keys: missing %s, extra %s' % (where, sorted(missing), sorted(extra)))
            continue
        nm = c['name']
        if not isinstance(nm, str) or not nm:
            reasons.append('%s.name must be a non-empty string' % where)
            continue
        where = '%s (%s)' % (where, nm)
        if nm in seen:
            reasons.append('%s duplicate name' % where)
            continue
        seen.add(nm)
        bad = False
        tr = c['transform']
        # S10: type guards first, so ndarray/odd objects never reach an `in` test
        for fld in ('transform', 'role', 'scope', 'kind'):
            if not isinstance(c[fld], str):
                reasons.append('%s.%s must be a str' % (where, fld))
                bad = True
        if bad:
            continue
        if tr not in ('log', 'linear'):
            reasons.append('%s.transform must be log or linear' % where)
            bad = True
        lo, hi, tv = c['lower'], c['upper'], c['trial_value']
        if not (_is_real(lo) and _is_real(hi) and _is_real(tv)):
            reasons.append('%s lower/upper/trial_value must be finite reals' % where)
            bad = True
        else:
            lo, hi, tv = float(lo), float(hi), float(tv)
            if not lo < hi:
                reasons.append('%s requires lower < upper' % where)
                bad = True
            if tr == 'log' and not lo > 0.0:
                reasons.append('%s log transform requires 0 < lower' % where)
                bad = True
            if not (lo <= tv <= hi):
                reasons.append('%s trial_value outside [lower, upper]' % where)
                bad = True
        units = c['units']
        if not isinstance(units, str) or not units.strip():
            reasons.append('%s.units must be a non-empty string (use "dimensionless" if so)' % where)
            bad = True
        scope, role, kind = c['scope'], c['role'], c['kind']
        if scope not in SCOPES:
            reasons.append('%s.scope must be one of %s' % (where, list(SCOPES)))
            bad = True
        if scope == SCOPE_SHARED and role not in ('free', 'fixed'):
            reasons.append('%s shared coordinates must have role free or fixed' % where)
            bad = True
        if scope in (SCOPE_DDO, SCOPE_NGC) and role != 'nuisance':
            reasons.append('%s %s coordinates must have role nuisance' % (where, scope))
            bad = True
        if scope == SCOPE_DDO_FIXED:
            # v003b (A13): the DDO154 distance fixed at its registered value, a counted constant, not a nuisance
            if role != 'fixed':
                reasons.append('%s %s coordinates must have role fixed (A13)' % (where, scope))
                bad = True
            if kind != 'distance':
                reasons.append('%s %s is only the DDO154 distance (kind distance, A13)' % (where, scope))
                bad = True
            if not _is_real(tv) or float(tv) != DDO154_REGISTERED_DISTANCE_MPC:
                reasons.append('%s %s trial_value must be the registered %r Mpc (A13)'
                               % (where, scope, DDO154_REGISTERED_DISTANCE_MPC))
                bad = True
            if c['sensitivity'] is not None:
                reasons.append('%s %s takes no sensitivity: a fixed counted constant; distance as a nuisance is the '
                               'recorded alternative NOT_EVALUATED_BEFORE_FREEZE (A13)' % (where, scope))
                bad = True
        if kind not in KINDS:
            reasons.append('%s.kind must be one of %s' % (where, list(KINDS)))
            bad = True
        if kind == 'other' and ((isinstance(units, str) and units.strip() in GEOMETRIC_UNITS) or
                                any(t in nm.lower() for t in GEOMETRIC_NAME_TOKENS)):
            # v003c (Claude4 R-A V8e-3, root A23): never a geometry relabelled kind 'other' (a DDO154 distance declared
            # shared/fixed/other would reach forward_ngc)
            reasons.append('%s REFUSED (V8e-3/A23): kind other with geometric units %s or a geometric name; a distance '
                           'or inclination must be declared with its own kind and scope (ddo154_fixed, '
                           'ddo154_nuisance, ngc3198_nuisance)' % (where, _safe_repr(units)))
            bad = True
        ref = c['reference_value']
        if ref is not None and not _is_real(ref):
            reasons.append('%s.reference_value must be a finite real or None' % where)
            bad = True
        if kind == 'distance':
            if scope not in DISTANCE_REFERENCE_MPC:
                reasons.append('%s distance coordinates must be ddo154_nuisance, ddo154_fixed or ngc3198_nuisance'
                               % where)
                bad = True
            else:
                if units != 'Mpc':
                    reasons.append('%s distance units must be Mpc' % where)
                    bad = True
                if ref is None or not _is_real(ref) or float(ref) != DISTANCE_REFERENCE_MPC[scope]:
                    reasons.append('%s distance reference_value must be %r Mpc for %s'
                                   % (where, DISTANCE_REFERENCE_MPC[scope], scope))
                    bad = True
        if kind == 'inclination' and units != 'deg':
            reasons.append('%s inclination units must be deg' % where)
            bad = True
        sens = c['sensitivity']
        sens_norm = None
        if sens is not None:
            if not isinstance(sens, dict) or not isinstance(sens.get('mode'), str) or \
                    sens.get('mode') not in ('box_ends', 'step'):
                reasons.append('%s.sensitivity must be None, {"mode": "box_ends"} or {"mode": "step", '
                               '"step": >0}' % where)
                bad = True
            elif sens['mode'] == 'box_ends':
                if set(sens) != {'mode'}:
                    reasons.append('%s.sensitivity box_ends takes no other keys' % where)
                    bad = True
                else:
                    sens_norm = {'mode': 'box_ends'}
            else:
                if set(sens) != {'mode', 'step'} or not _is_real(sens.get('step')) or not float(sens['step']) > 0:
                    reasons.append('%s.sensitivity step requires a finite step > 0 (natural units)' % where)
                    bad = True
                elif _is_real(lo) and _is_real(hi) and _is_real(tv) and \
                        not (float(lo) <= float(tv) - float(sens['step']) and
                             float(tv) + float(sens['step']) <= float(hi)):
                    # D4: one step rule shared with calibration_region_engine_c2v003 (no silent clipping)
                    reasons.append('%s.sensitivity: trial_value +/- step must lie inside [lower, upper] (D4: one '
                                   'step rule in both modules)' % where)
                    bad = True
                else:
                    sens_norm = {'mode': 'step', 'step': float(sens['step'])}
            if not ((scope == SCOPE_SHARED and role == 'fixed') or scope == SCOPE_NGC or scope == SCOPE_DDO_FIXED):
                reasons.append('%s sensitivity may be declared only for fixed shared coordinates and NGC3198 '
                               'nuisances (free and DDO154 coordinates are spanned by calibration)' % where)
                bad = True
        if scope == SCOPE_NGC and sens is None:
            reasons.append('%s NGC3198 nuisances must declare a sensitivity (never silently held)' % where)
            bad = True
        if bad:
            continue
        coords.append({'name': nm, 'transform': tr, 'lower': lo, 'upper': hi, 'role': role, 'trial_value': tv,
                       'units': units, 'scope': scope, 'kind': kind,
                       'reference_value': (float(ref) if ref is not None else None), 'sensitivity': sens_norm})
    if reasons:
        return None
    for scope in (SCOPE_DDO, SCOPE_NGC):
        for kind in ('distance', 'inclination'):
            n = sum(1 for c in coords if c['scope'] == scope and c['kind'] == kind)
            if n > 1:
                reasons.append('%s has %d %s coordinates; at most one allowed' % (scope, n, kind))
            if scope == SCOPE_NGC and n != 1:
                reasons.append('NGC3198 needs its own %s nuisance slot (D10)' % kind)
    ddo_fixed = [c['name'] for c in coords if c['scope'] == SCOPE_DDO_FIXED]
    if ddo_fixed and sum(1 for c in coords if c['scope'] in (SCOPE_DDO, SCOPE_DDO_FIXED) and c['kind'] == 'distance') > 1:
        reasons.append('DDO154 has a fixed distance %s and another distance coordinate; at most one DDO154 distance '
                       '(A13: fixed, or the recorded nuisance alternative)' % ddo_fixed)
    engine = [c for c in coords if c['scope'] != SCOPE_NGC]
    varying = [c['name'] for c in engine if c['role'] != 'fixed']
    if not varying:
        reasons.append('at least one varying engine coordinate (free shared or DDO154 nuisance) is required')
    if reasons:
        return None
    shared = [c['name'] for c in coords if c['scope'] == SCOPE_SHARED]
    ngc = [c['name'] for c in coords if c['scope'] == SCOPE_NGC]
    return {
        'coordinates': coords,
        'by_name': {c['name']: c for c in coords},
        'engine_names': [c['name'] for c in engine],
        'varying_engine': varying,
        'shared_names': shared,
        'ddo_nuisance_names': [c['name'] for c in coords if c['scope'] == SCOPE_DDO],
        'ngc_nuisance_names': ngc,
        'ngc_theta_names': shared + ngc,
        'fixed_shared': [c['name'] for c in coords if c['scope'] == SCOPE_SHARED and c['role'] == 'fixed'],
        'sensitivity_targets': [c['name'] for c in coords if c['sensitivity'] is not None],
        # v003b (A13): the mode is a function of the coordinate list (None = the v003a 4-coordinate behaviour)
        'ddo_fixed_names': ddo_fixed,
        'coordinate_mode': MODE_D_FIXED if ddo_fixed else None,
    }


def _spec_from(spec, reasons):
    if isinstance(spec, dict) and isinstance(spec.get('spec'), dict):
        spec = spec['spec']
    if not isinstance(spec, dict) or 'coordinates' not in spec:
        reasons.append('spec must be the output of make_freeze_coordinate_spec')
        return None
    return _build_spec(spec['coordinates'], reasons)


@_fail_closed
def make_freeze_coordinate_spec(*, coordinates):
    """Validate the full coordinate list (engine coordinates plus NGC3198 nuisance slots).

    Every coordinate: {name, transform, lower, upper, role, trial_value, units, scope, kind,
    reference_value, sensitivity}. scope 'shared' (role free|fixed), 'ddo154_nuisance' (role
    nuisance; passed to the DDO154 engine only, never to forward_ngc) or 'ngc3198_nuisance' (role
    nuisance; never passed to the engine; held at trial_value in members and evaluated for
    sensitivity). kind 'distance' needs units Mpc and reference_value 4.04 (DDO154) or 13.8
    (NGC3198); kind 'inclination' needs units deg. NGC3198 must carry exactly one distance and one
    inclination slot. Returns 'engine_coordinates' (D4: engine-ready nine-field dicts in the engine's
    spellings, NGC3198 slots excluded; pass them to run_calibration_region unchanged) and 'spec'
    (pass it to the other functions). One step rule (D4): trial_value +/- step inside [lower, upper].
    v003b (A13): scope 'ddo154_fixed' (role fixed, kind distance, units Mpc, reference_value and trial_value 4.04,
    sensitivity None; at most one DDO154 distance in all) puts the list in coordinate mode
    DDO154_DISTANCE_FIXED_AT_REGISTERED, reported as 'coordinate_mode' (absent otherwise). Its engine coordinate has
    scope DDO154 and role fixed; it is never passed to forward_ngc. See apply_coordinate_mode.
    """
    reasons = []
    out = {'ok': False, 'spec': None, 'engine_coordinates': [], 'ngc_theta_names': [],
           'bounds_semantics': BOUNDS_SEMANTICS, 'reasons': reasons}
    S = _build_spec(coordinates, reasons)
    if S is None:
        return out
    out['spec'] = {'coordinates': [dict(c, sensitivity=(dict(c['sensitivity']) if c['sensitivity'] else None))
                                   for c in S['coordinates']]}
    # D4: engine-ready dicts in the engine's own spellings (scope 'shared' | 'DDO154'; sensitivity
    # 'NONE' | 'BOX_ENDS' | {'step_natural': x}); NGC3198 slots are never passed to the DDO154 engine.
    out['engine_coordinates'] = [_engine_coordinate(c) for c in S['coordinates'] if c['scope'] != SCOPE_NGC]
    out['ngc_theta_names'] = list(S['ngc_theta_names'])
    if S['coordinate_mode'] is not None:   # v003b (A13): reported only in the fixed-distance mode
        out['coordinate_mode'] = S['coordinate_mode']
    out['ok'] = True
    return out


@_fail_closed
def apply_coordinate_mode(*, coordinates, coordinate_mode):
    """v003b (A13): the freeze coordinate list for an orchestrator coordinate_mode declaration.

    coordinates: the V001 freeze coordinate list (the DDO154 distance a ddo154_nuisance coordinate) plus the NGC3198
    slots. coordinate_mode: the addendum's {'mode', 'free_coordinates', 'fixed_engine_coordinates', ...}.
      * DDO154_DISTANCE_FIXED_AT_REGISTERED: fixed_engine_coordinates must be exactly {<name>: 4.04} naming the single
        DDO154 distance coordinate (trial_value 4.04); its scope becomes 'ddo154_fixed' and its role 'fixed'; nothing
        else changes (box, transform, units, reference_value kept). The engine coordinate then differs from the V001
        one only in role (nuisance -> fixed), as the orchestrator's own mode rule requires.
      * DDO154_DISTANCE_NUISANCE: fixed_engine_coordinates must be empty; the list is returned unchanged.
    In both modes the resulting varying engine names must equal free_coordinates (order included).
    Returns {'ok', 'mode', 'coordinates', 'changed', 'varying_engine_names', 'engine_coordinates', 'reasons'}.
    """
    reasons = []
    out = {'ok': False, 'mode': None, 'coordinates': [], 'changed': [], 'varying_engine_names': [],
           'engine_coordinates': [], 'reasons': reasons}
    if not isinstance(coordinate_mode, dict) or not isinstance(coordinate_mode.get('mode'), str) or \
            coordinate_mode.get('mode') not in COORDINATE_MODES:
        reasons.append('coordinate_mode must be a dict whose mode is one of %s' % list(COORDINATE_MODES))
        return out
    mode = coordinate_mode['mode']
    out['mode'] = mode
    S0 = _build_spec(coordinates, reasons)
    if S0 is None:
        return out
    if S0['coordinate_mode'] is not None:
        reasons.append('apply_coordinate_mode takes the V001 list (DDO154 distance a nuisance); it already holds the '
                       'fixed coordinate(s) %s' % S0['ddo_fixed_names'])
        return out
    fx = coordinate_mode.get('fixed_engine_coordinates')
    free = coordinate_mode.get('free_coordinates')
    new = [dict(c, sensitivity=(dict(c['sensitivity']) if c['sensitivity'] else None)) for c in S0['coordinates']]
    if mode == MODE_D_NUISANCE:
        if fx not in (None, {}):
            reasons.append('coordinate mode %s fixes nothing, got fixed_engine_coordinates %s' % (mode, _safe_repr(fx)))
            return out
    else:
        dd = [c for c in new if c['scope'] == SCOPE_DDO and c['kind'] == 'distance']
        if len(dd) != 1:
            reasons.append('coordinate mode %s needs exactly one ddo154_nuisance distance coordinate, found %d'
                           % (mode, len(dd)))
            return out
        c = dd[0]
        if not isinstance(fx, dict) or len(fx) != 1 or list(fx) != [c['name']] or \
                not _is_real(fx[c['name']]) or float(fx[c['name']]) != DDO154_REGISTERED_DISTANCE_MPC:
            reasons.append('coordinate mode %s must fix exactly {%r: %r}, got %s'
                           % (mode, c['name'], DDO154_REGISTERED_DISTANCE_MPC, _safe_repr(fx)))
            return out
        if c['trial_value'] != DDO154_REGISTERED_DISTANCE_MPC:
            reasons.append('%s trial_value %r is not the registered %r Mpc (A13)'
                           % (c['name'], c['trial_value'], DDO154_REGISTERED_DISTANCE_MPC))
            return out
        c['scope'] = SCOPE_DDO_FIXED
        c['role'] = 'fixed'
    changed = [(a['name'], k) for a, b in zip(S0['coordinates'], new) for k in sorted(set(a) | set(b))
               if a.get(k) != b.get(k)]
    expect = [] if mode == MODE_D_NUISANCE else [(c['name'], 'role'), (c['name'], 'scope')]
    if changed != expect:
        reasons.append('coordinate mode changed %s, expected exactly %s' % (changed, expect))
        return out
    S = _build_spec(new, reasons)
    if S is None:
        return out
    if not isinstance(free, (list, tuple)) or list(free) != S['varying_engine']:
        reasons.append('coordinate_mode.free_coordinates %s differ from the varying engine coordinates %s'
                       % (_safe_repr(free), S['varying_engine']))
        return out
    out['coordinates'] = [dict(c, sensitivity=(dict(c['sensitivity']) if c['sensitivity'] else None))
                          for c in S['coordinates']]
    out['changed'] = [list(x) for x in changed]
    out['varying_engine_names'] = list(S['varying_engine'])
    out['engine_coordinates'] = [_engine_coordinate(c) for c in S['coordinates'] if c['scope'] != SCOPE_NGC]
    out['ok'] = True
    return out


def _mode_labels(S):
    """v003b: (envelope label, sensitivity label, band_scope) of the coordinate mode."""
    if S.get('coordinate_mode') == MODE_D_FIXED:
        return ENVELOPE_LABEL_A13, SENSITIVITY_LABEL_A13, BAND_SCOPE_A13
    return ENVELOPE_LABEL, SENSITIVITY_LABEL, BAND_SCOPE


def _check_run_coordinate_binding(S, run_spec, where, reasons):
    """v003c (Claude4 R-A V8e-3, root A23): bind the freeze coordinates to the calibration run's own coordinates.

    run_spec: the engine's coordinate spec of the run (run_calibration_region output 'spec', also recorded in the
    calibration record's run content). The freeze's engine coordinates (NGC3198 slots excluded) must equal the run's,
    name by name in order, in role and in engine scope ('shared' | 'DDO154'), and no coordinate the calibration scoped
    DDO154 may be among the names passed to forward_ngc. Appends reasons and returns False on any violation."""
    if not isinstance(run_spec, dict) or not isinstance(run_spec.get('names'), list) or \
            not isinstance(run_spec.get('roles'), dict) or not isinstance(run_spec.get('scopes'), dict):
        reasons.append('REFUSED (V8e-3/A23): %s carries no readable coordinate spec (names, roles, scopes); the freeze '
                       'coordinates cannot be bound to the calibration coordinates' % where)
        return False
    names = [_safe_str(x) for x in run_spec['names']]
    got = [(nm, _safe_str(run_spec['roles'].get(nm)), _safe_str(run_spec['scopes'].get(nm))) for nm in names]
    exp = [(c['name'], c['role'], 'shared' if c['scope'] == SCOPE_SHARED else 'DDO154')
           for c in S['coordinates'] if c['scope'] != SCOPE_NGC]
    if got != exp:
        diff = [(g, e) for g, e in zip(got, exp) if g != e][:4]
        reasons.append('REFUSED (V8e-3/A23): the freeze engine coordinates (name, role, scope) differ from those of %s '
                       '(first differences [calibration, freeze]: %s; counts %d vs %d); a calibration coordinate must '
                       'keep its role and scope in the freeze' % (where, _safe_repr(diff), len(got), len(exp)))
        return False
    ddo = set(nm for nm, _r, sc in got if sc == 'DDO154')
    leak = sorted(ddo & set(S['ngc_theta_names']))
    if leak:
        reasons.append('REFUSED (V8e-3/A23, D10): DDO154-scoped calibration coordinate(s) %s would reach forward_ngc'
                       % leak)
        return False
    return True


def _engine_coordinate(c):
    sens = c['sensitivity']
    if sens is None:
        es = 'NONE'
    elif sens['mode'] == 'box_ends':
        es = 'BOX_ENDS'
    else:
        es = {'step_natural': float(sens['step'])}
    return {'name': c['name'], 'transform': c['transform'], 'lower': c['lower'], 'upper': c['upper'],
            'role': c['role'], 'trial_value': c['trial_value'], 'units': c['units'],
            'scope': ('shared' if c['scope'] == SCOPE_SHARED else 'DDO154'), 'sensitivity': es}


def _x_bounds(c):
    if c['transform'] == 'log':
        return math.log(c['lower']), math.log(c['upper'])
    return c['lower'], c['upper']


def _theta_engine_from_u(S, u):
    """Engine theta (every engine coordinate, fixed at trial) from u over varying engine coordinates."""
    theta = {}
    j = 0
    for nm in S['engine_names']:
        c = S['by_name'][nm]
        if c['role'] == 'fixed':
            theta[nm] = c['trial_value']
            continue
        x_lo, x_hi = _x_bounds(c)
        x = x_lo + u[j] * (x_hi - x_lo)
        j += 1
        if c['transform'] == 'log':
            v = min(c['upper'], max(c['lower'], math.exp(x)))
        else:
            v = x
        theta[nm] = float(v)
    return theta


def _u_of_trial(S):
    u = []
    for nm in S['varying_engine']:
        c = S['by_name'][nm]
        x_lo, x_hi = _x_bounds(c)
        xv = math.log(c['trial_value']) if c['transform'] == 'log' else c['trial_value']
        u.append((xv - x_lo) / (x_hi - x_lo))
    return u


def _theta_ngc_from_engine(S, theta_engine):
    """forward_ngc input: shared coordinates from the member plus NGC3198 nuisances at trial.

    DDO154 nuisances are never included (D10)."""
    th = {nm: float(theta_engine[nm]) for nm in S['shared_names']}
    for nm in S['ngc_nuisance_names']:
        th[nm] = S['by_name'][nm]['trial_value']
    return th


# --------------------------------------------------------------------------
# select_representative_points
# --------------------------------------------------------------------------

def _bind_u(u, where, reasons):
    if not isinstance(u, (list, tuple)) or len(u) == 0:
        reasons.append('%s.u must be a non-empty list' % where)
        return None
    vals = []
    for i, x in enumerate(u):
        if not _is_real(x):
            reasons.append('%s.u[%d] is not a finite real' % (where, i))
            return None
        vals.append(float(x))
    return vals


def _bind_theta(theta, where, reasons):
    if not isinstance(theta, dict) or not theta:
        reasons.append('%s.theta_natural must be a non-empty dict' % where)
        return None
    out = {}
    for k, v in theta.items():
        if not isinstance(k, str) or not k:
            reasons.append('%s.theta_natural has a non-string key %r' % (where, k))
            return None
        if not _is_real(v):
            reasons.append('%s.theta_natural[%r] is not a finite real' % (where, k))
            return None
        out[k] = float(v)
    return out


def _resolve_exploration(exploration, reasons):
    """Locate the explore_region dict and the identifiability dict.

    Accepted layouts (first match wins):
      A. run_calibration_region output: {'exploration': {...}, 'identifiability': {...}}
      B. explore_region output with an added 'identifiability' dict
      C. explore_region output with top-level right_vectors / identified / near_null
    """
    if not isinstance(exploration, dict):
        reasons.append('exploration must be a dict')
        return None, None
    ex = exploration
    if 'admitted_points' not in ex and isinstance(ex.get('exploration'), dict):
        ex = ex['exploration']
    ident = None
    for container in (exploration, ex):
        if isinstance(container.get('identifiability'), dict):
            ident = container['identifiability']
            break
    if ident is None:
        ident = ex
    if ident.get('right_vectors') is None:
        reasons.append('direction vectors not found: supply identifiability.right_vectors '
                       '(rows = directions in u-space)')
        return None, None
    return ex, ident


def _bind_index_list(x, label, reasons):
    if not isinstance(x, (list, tuple)):
        reasons.append('%s must be a list of direction indices' % label)
        return None
    out = []
    for k in x:
        if not _is_int(k):
            reasons.append('%s contains a non-integer %r' % (label, k))
            return None
        out.append(int(k))
    if len(set(out)) != len(out):
        reasons.append('%s has duplicates' % label)
        return None
    return sorted(out)


def _centroid(adm_proj, k):
    n = len(adm_proj)
    return [math.fsum(p['projection'][j] for p in adm_proj) / n for j in range(k)]


def _selection_plan(adm, n_ident, anchor_li, interior_count):
    """D2: the selection rule as a pure function of the frozen inputs.

    adm: list of (log_index, identified projection list) for EVERY admitted point. Returns the member list
    [(log_index, role), ...] in member order (SELECTION_RULE). The verifier recomputes it from the
    manifest's admitted_projections_identified, selection_anchor_log_index and selection_interior_count.
    """
    selected = []
    seen = set()

    def take(li, role):
        if li in seen:
            return
        seen.add(li)
        selected.append((li, role))

    for j in range(n_ident):
        proj = [(p[j], li) for li, p in adm]
        pmin = min(proj, key=lambda t: (t[0], t[1]))
        pmax = min(proj, key=lambda t: (-t[0], t[1]))
        take(pmin[1], ROLE_HULL)
        take(pmax[1], ROLE_HULL)
    if anchor_li is not None:
        take(anchor_li, ROLE_ANCHOR)
    n = len(adm)
    centroid = [math.fsum(p[j] for _li, p in adm) / n for j in range(n_ident)]

    def dist(p):
        return math.sqrt(math.fsum((a - b) ** 2 for a, b in zip(p, centroid)))

    cn = min(adm, key=lambda t: (dist(t[1]), t[0]))
    take(cn[0], ROLE_CENTROID)
    remaining = sorted(li for li, _p in adm if li not in seen)
    for j in _evenly_spaced_indices(len(remaining), interior_count):
        take(remaining[j], ROLE_INTERIOR)
    return selected


def _reclassify_admitted(pt, region):
    """P34-14: re-classify an admitted point's logged DDO154 prediction against the closed rectangles.

    Returns None if admitted, else a reason string. Same predicate as the engine: valid is True, every row
    id present with a finite value, and low <= value <= high for every row (closed rectangle)."""
    pred = pt.get('prediction')
    if not isinstance(pred, dict) or pred.get('valid') is not True:
        return 'logged prediction missing or valid is not True'
    sp = pred.get('speeds_km_s')
    if not isinstance(sp, dict):
        return 'logged prediction has no speeds_km_s dict'
    for rid in region['row_ids']:
        v = sp.get(rid)
        if not _is_real(v):
            return 'row %r missing or not finite' % (rid,)
        lo, hi = region['rectangles'][rid]
        if not (float(lo) <= float(v) <= float(hi)):
            return 'row %r = %r outside the closed rectangle [%r, %r]' % (rid, v, lo, hi)
    return None


def _region_from_bytes(path, expected_sha256):
    """X1 (v003a): re-derive the DDO154 admission rectangles from the region file BYTES.

    Returns ({'path', 'sha256', 'row_ids', 'rectangles'}, None) or (None, reason). The sha256 of the bytes must
    equal expected_sha256 before anything is parsed. Validation mirrors the engine's load_observation_region:
    exactly REGION_EXPECTED_ROWS rows, unique non-empty str ids, every row field finite, sigma > 0,
    low < observed < high, and the top-level fields present. Only ids and [low, high] are returned."""
    if not _is_hex64(expected_sha256):
        return None, 'expected region sha256 is not 64-hex'
    raw, real, err = _read_regular(path, True)
    if raw is None:
        return None, err
    actual = _sha256_hex(raw)
    if actual != expected_sha256.lower():
        return None, ('region file %r bytes hash to %s, not %s; not parsed'
                      % (path, actual, expected_sha256.lower()))
    doc, perr = _parse_json_bytes(raw)
    if doc is None:
        return None, 'region file: %s' % perr
    if not isinstance(doc, dict) or not isinstance(doc.get('rows'), list):
        return None, 'region file top level must be an object with a rows list'
    rows = doc['rows']
    if len(rows) != REGION_EXPECTED_ROWS:
        return None, 'region file has %d rows, expected exactly %d' % (len(rows), REGION_EXPECTED_ROWS)
    for key in REGION_TOP_FIELDS:
        if key not in doc:
            return None, 'region file misses the top-level field %r' % key
    row_ids, rect = [], {}
    for k, row in enumerate(rows):
        if not isinstance(row, dict):
            return None, 'region rows[%d] is not an object' % k
        rid = row.get('id')
        if not isinstance(rid, str) or not rid or rid in rect:
            return None, 'region rows[%d].id must be a unique non-empty str' % k
        for field in REGION_ROW_NUMERIC_FIELDS:
            if not _is_real(row.get(field)):
                return None, 'region rows[%d] (%s): %s missing or not finite' % (k, rid, field)
        lo = float(row['conditional_random_acceptance_low_km_s'])
        hi = float(row['conditional_random_acceptance_high_km_s'])
        if not float(row['quoted_random_sigma_km_s']) > 0 or \
                not (lo < float(row['observed_speed_km_s']) < hi):
            return None, 'region rows[%d] (%s): sigma > 0 or low < observed < high violated' % (k, rid)
        row_ids.append(rid)
        rect[rid] = [lo, hi]
    return {'path': real, 'sha256': actual, 'row_ids': row_ids, 'rectangles': rect}, None


def _region_of(exploration):
    """(region, None) with the rectangles re-derived from the region file BYTES when the caller passed a
    run_calibration_region output; (None, None) when the exploration carries no ok region (layout B: the
    writer then refuses); (None, reason) when an ok region is named but its bytes do not re-derive.

    X1 (v003a): only region.path and region.sha256 are taken from the run dict; its rectangles and row_ids are
    never used."""
    reg = exploration.get('region') if isinstance(exploration, dict) else None
    if not isinstance(reg, dict) or reg.get('ok') is not True:
        return None, None
    if not _is_hex64(reg.get('sha256')) or not isinstance(reg.get('path'), str) or not reg.get('path'):
        return None, ('REFUSED (P34-14/X1): exploration.region must name the region file path and sha256 '
                      '(pass the run_calibration_region output)')
    region, why = _region_from_bytes(reg['path'], reg['sha256'])
    if region is None:
        return None, ('REFUSED (P34-14/X1): the admission rectangles could not be re-derived from the region '
                      'file bytes: %s' % why)
    return region, None


def _fingerprint(admitted_lu, region_sha):
    """P34-16: same object and bytes as calibration_region_engine_c2v003.exploration_fingerprint."""
    pts = sorted(([int(li), [float(x) for x in u]] for li, u in admitted_lu), key=lambda t: t[0])
    payload = {'schema': FINGERPRINT_SCHEMA, 'region_sha256': region_sha.lower(), 'admitted': pts}
    return _sha256_hex(_canonical_bytes(payload))


@_fail_closed
def select_representative_points(*, exploration, interior_count, spec):
    """Choose the representative admitted members for NGC3198 propagation.

    SELECTION_RULE (v001 order kept): hull vertices per identified direction, then the anchor, then the
    admitted point nearest the centroid of all admitted points in the identified subspace (role
    'centroid_nearest'), then an evenly spaced interior subset by log_index.

    v003: the anchor is the engine's primary_anchor (always an admitted entry; P34-14), falling back to
    exploration.anchor only when it is admitted; when the caller passes the run_calibration_region output
    (layout A) every admitted point is re-classified against the region's closed rectangles
    (admission_reverified) and the region sha256 and the exploration fingerprint are recorded (P34-16).
    v003a (X1): those closed rectangles are re-derived from the region file BYTES (exploration.region.path,
    sha256 verified against exploration.region.sha256 before parsing); the run dict's rectangles are never used.
    D2: the rule's inputs (interior_count, anchor log_index, every admitted projection) and its output
    (selected_points) are frozen in admitted_region so the verifier can recompute the member set.
    S8: a hull_box that is malformed, inconsistent with right_vectors, missing or empty (v003a) refuses.
    D10: right_vectors must be a COMPLETE orthonormal basis of the varying engine u space and
    identified + near_null must partition it; otherwise the call refuses (NULL_SPACE_NOT_COMPLETE).
    D7: the admitted set is labelled INNER_SAMPLE; region_possibly_truncated is set when the
    exploration did not complete, the engine flags or does not report truncation, or an admitted
    point touches a computational-box face.
    """
    reasons = []
    out = {'ok': False, 'points': [], 'hull_vertex_count': 0, 'interior_count_used': 0,
           'anchor_included': False, 'anchor_source': None, 'centroid_nearest_log_index': None, 'n_admitted': 0,
           'identified_directions': [], 'hull_directions': [], 'hull_box_consistent': None,
           'admission_reverified': False, 'observation_region_sha256': None, 'calibration_fingerprint': None,
           'admitted_region': None, 'reasons': reasons}
    S = _spec_from(spec, reasons)
    if not _is_int(interior_count) or interior_count < 0:
        reasons.append('interior_count must be a non-negative integer')
    if reasons:
        return out
    interior_count = int(interior_count)
    ex, ident = _resolve_exploration(exploration, reasons)
    if ex is None:
        return out
    # v003c (V8e-3/A23): with the run output itself (layout A), bind the freeze coordinates to the run's coordinates
    # before any member exists (the writer and the verifier repeat this on the mandatory calibration record pin)
    if (isinstance(exploration.get('exploration'), dict) or 'spec' in exploration) and \
            not _check_run_coordinate_binding(S, exploration.get('spec'), 'the calibration run', reasons):
        return out
    n = len(S['varying_engine'])

    # D10: explicit, complete basis.
    vnames = ident.get('varying_names')
    if vnames is not None and (not isinstance(vnames, (list, tuple)) or list(vnames) != S['varying_engine']):
        reasons.append('identifiability.varying_names %s differ from the spec varying engine coordinates %r'
                       % (_safe_repr(vnames), S['varying_engine']))
        return out
    rv = ident.get('right_vectors')
    if not isinstance(rv, (list, tuple)) or len(rv) != n:
        reasons.append('NULL_SPACE_NOT_COMPLETE: right_vectors must hold exactly %d direction vectors (one per '
                       'varying engine coordinate), got %s' % (n, len(rv) if isinstance(rv, (list, tuple))
                                                              else type(rv).__name__))
        return out
    V = []
    for k, vec in enumerate(rv):
        v = _bind_u(vec, 'right_vectors[%d]' % k, reasons)
        if v is None:
            return out
        if len(v) != n:
            reasons.append('right_vectors[%d] has length %d, expected %d' % (k, len(v), n))
            return out
        V.append(v)
    for i in range(n):
        for j in range(i, n):
            g = _dot(V[i], V[j])
            if abs(g - (1.0 if i == j else 0.0)) > _ORTHO_TOL:
                reasons.append('NULL_SPACE_NOT_COMPLETE: right_vectors are not orthonormal (<v%d, v%d> = %r)'
                               % (i, j, g))
                return out
    identified = _bind_index_list(ident.get('identified'), 'identified', reasons)
    near_null = _bind_index_list(ident.get('near_null'), 'near_null', reasons)
    if identified is None or near_null is None:
        return out
    if set(identified) & set(near_null) or sorted(identified + near_null) != list(range(n)):
        reasons.append('NULL_SPACE_NOT_COMPLETE: identified %s and near_null %s must partition 0..%d'
                       % (identified, near_null, n - 1))
        return out
    if not identified:
        reasons.append('no identified directions')
        return out
    svals = ident.get('singular_values')
    sv = None
    if svals is not None:
        if not isinstance(svals, (list, tuple)) or not all(_is_real(x) for x in svals) or len(svals) > n:
            reasons.append('singular_values must be a list of at most %d finite reals' % n)
            return out
        sv = [float(x) for x in svals] + [0.0] * (n - len(svals))
        if len(svals) < n:
            reasons.append('NOTE singular_values padded with %d zeros for the completed null space'
                           % (n - len(svals)))
    out['identified_directions'] = list(identified)

    status = ex.get('status')
    stage = ex.get('stage_reached')
    admitted_raw = ex.get('admitted_points')
    if not isinstance(admitted_raw, (list, tuple)) or len(admitted_raw) == 0:
        reasons.append('exploration.admitted_points must be a non-empty list (status %s); an empty or '
                       'unproven region is not a prediction freeze' % (_safe_repr(status),))
        return out
    region, region_err = _region_of(exploration)   # X1: rectangles from the region file bytes, never the run dict
    if region_err is not None:
        reasons.append(region_err)
        return out
    engine_set = set(S['engine_names'])
    admitted = []
    seen_log = set()
    nerr = len(reasons)
    for i, pt in enumerate(admitted_raw):
        where = 'admitted_points[%d]' % i
        if not isinstance(pt, dict):
            reasons.append('%s is not a dict' % where)
            continue
        u = _bind_u(pt.get('u'), where, reasons)
        theta = _bind_theta(pt.get('theta_natural'), where, reasons)
        li = pt.get('log_index')
        if not _is_int(li):
            reasons.append('%s.log_index is not an integer' % where)
            continue
        if u is None or theta is None:
            continue
        if len(u) != n:
            reasons.append('%s.u has length %d, expected %d' % (where, len(u), n))
            continue
        if set(theta) != engine_set:
            reasons.append('%s.theta_natural keys %s differ from the engine coordinates %s'
                           % (where, sorted(theta), sorted(engine_set)))
            continue
        recomputed = _theta_engine_from_u(S, u)
        bad = [nm for nm in S['engine_names'] if not _close(recomputed[nm], theta[nm])]
        if bad:
            reasons.append('%s theta_natural inconsistent with u under the spec transforms for %s'
                           % (where, bad))
            continue
        li = int(li)
        if li in seen_log:
            reasons.append('%s duplicates log_index %d' % (where, li))
            continue
        if region is not None:
            why = _reclassify_admitted(pt, region)
            if why is not None:   # P34-14: a non-admitted point never becomes a member
                reasons.append('%s (log_index %d) is not admitted under the closed rectangles: %s'
                               % (where, li, why))
                continue
        seen_log.add(li)
        proj = [_dot(u, V[k]) for k in identified]
        admitted.append({'u': u, 'theta_natural': theta, 'log_index': li, 'proj': proj})
    if len(reasons) > nerr:
        return out
    N = len(admitted)
    out['n_admitted'] = N
    by_li = {pt['log_index']: pt for pt in admitted}
    adm_proj = [{'log_index': pt['log_index'], 'projection': list(pt['proj'])} for pt in admitted]
    centroid = _centroid(adm_proj, len(identified))
    region_sha = region['sha256'].lower() if region is not None else None
    out['admission_reverified'] = region is not None
    out['observation_region_sha256'] = region_sha
    if region is None:
        reasons.append('NOTE exploration carries no hash-verified region (pass the run_calibration_region output): '
                       'admission not re-verified and the region is not bound; write_freeze_manifest will refuse')
    fp = _fingerprint([(pt['log_index'], pt['u']) for pt in admitted], region_sha) if region_sha else None
    out['calibration_fingerprint'] = fp
    eng_fp = exploration.get('exploration_fingerprint') if isinstance(exploration, dict) else None
    if fp is not None and eng_fp is not None and eng_fp != fp:
        reasons.append('exploration_fingerprint %s reported by the engine differs from the one recomputed from '
                       'the admitted points %s' % (_safe_repr(eng_fp), fp))
        return out

    # S8: hull_box must be well formed and consistent with right_vectors, or the call refuses.
    # X1 (v003a): a missing or empty hull_box is refused, not skipped.
    hull_box = ex.get('hull_box')
    if not isinstance(hull_box, dict) or not hull_box:
        reasons.append('REFUSED (S8/X1): hull_box must be a non-empty dict keyed by identified direction '
                       '(missing or empty hull_box refused, got %s)' % _safe_repr(hull_box)[:80])
        return out
    hull_keys = {}
    for k, box in hull_box.items():
        try:
            kk = int(k) if (not isinstance(k, bool) and (_is_int(k) or isinstance(k, str))) else None
        except (TypeError, ValueError, OverflowError):
            kk = None
        if kk is None or kk in hull_keys or not isinstance(box, dict) or not _is_real(box.get('min')) or \
                not _is_real(box.get('max')):
            reasons.append('REFUSED (S8): hull_box entry %s is malformed' % _safe_repr(k))
            return out
        hull_keys[kk] = (float(box['min']), float(box['max']))
    if set(hull_keys) != set(identified):
        reasons.append('REFUSED (S8): hull_box directions %s differ from the identified directions %s'
                       % (sorted(hull_keys), identified))
        return out

    prange = {}
    for j, k in enumerate(identified):
        proj = [(pt['proj'][j], pt['log_index']) for pt in admitted]
        pmin = min(proj, key=lambda t: (t[0], t[1]))
        pmax = min(proj, key=lambda t: (-t[0], t[1]))
        prange[str(k)] = {'min': float(pmin[0]), 'max': float(pmax[0])}
        out['hull_directions'].append({'direction_index': k, 'min_log_index': pmin[1],
                                       'max_log_index': pmax[1], 'projection_range': float(pmax[0] - pmin[0])})
        if hull_keys:
            lo, hi = hull_keys[k]
            if abs((hi - lo) - (pmax[0] - pmin[0])) > _HULL_BOX_TOL * (1.0 + abs(hi - lo)):
                reasons.append('REFUSED (S8): hull_box[%d] range %r differs from the range %r recomputed from '
                               'right_vectors and the admitted points' % (k, hi - lo, pmax[0] - pmin[0]))
                return out
    out['hull_box_consistent'] = True if hull_keys else None

    # P34-14: the anchor member is the engine's primary anchor (an admitted entry by construction).
    anchor_li, anchor_source = None, None
    pa = ex.get('primary_anchor')
    anchor = ex.get('anchor')
    if isinstance(pa, dict) and _is_int(pa.get('log_index')):
        anchor_li, anchor_source = int(pa['log_index']), 'primary_anchor'
    elif pa is not None and not isinstance(pa, dict):
        reasons.append('primary_anchor is not a dict')
        return out
    elif anchor is None:
        reasons.append('NOTE anchor absent from exploration; not included')
    elif not isinstance(anchor, dict):
        reasons.append('anchor is not a dict')
        return out
    elif anchor.get('admitted') is not True:
        reasons.append('NOTE anchor not admitted and no primary_anchor reported; not included (members are '
                       'admitted points only)')
    else:
        a_li = anchor.get('log_index')
        if _is_int(a_li):
            anchor_li, anchor_source = int(a_li), 'anchor'
        else:
            a_u = _bind_u(anchor.get('u'), 'anchor', reasons)
            if a_u is None:
                return out
            match = next((pt for pt in admitted if pt['u'] == a_u), None)
            if match is None:
                reasons.append('anchor is marked admitted but its u is not among admitted_points')
                return out
            anchor_li, anchor_source = match['log_index'], 'anchor_u'
    if anchor_li is not None and anchor_li not in by_li:
        reasons.append('REFUSED (P34-14): the anchor (log_index %d, from %s) is not among the admitted points'
                       % (anchor_li, anchor_source))
        return out
    out['anchor_included'] = anchor_li is not None
    out['anchor_source'] = anchor_source

    plan = _selection_plan([(pt['log_index'], pt['proj']) for pt in admitted], len(identified), anchor_li,
                           interior_count)
    selected = []
    for li, role in plan:
        pt = by_li[li]
        selected.append({'u': list(pt['u']), 'theta_natural': dict(pt['theta_natural']), 'role': role,
                         'log_index': li, 'identified_projection': list(pt['proj'])})
    out['hull_vertex_count'] = sum(1 for p in selected if p['role'] == ROLE_HULL)
    out['centroid_nearest_log_index'] = min(
        admitted, key=lambda pt: (math.sqrt(math.fsum((a - b) ** 2 for a, b in zip(pt['proj'], centroid))),
                                  pt['log_index']))['log_index']
    out['interior_count_used'] = sum(1 for p in selected if p['role'] == ROLE_INTERIOR)

    # D7 truncation evidence.
    evidence = []
    if status != STATUS_COMPLETE:
        evidence.append('EXPLORATION_STATUS_%s' % (status if isinstance(status, str) else _safe_repr(status)))
    flags = ex.get('flags')
    reported = ('region_possibly_truncated' in ex) or isinstance(flags, (list, tuple))
    engine_flag = (ex.get('region_possibly_truncated') is True or
                   (isinstance(flags, (list, tuple)) and 'REGION_POSSIBLY_TRUNCATED' in flags))
    if engine_flag:
        evidence.append('ENGINE_FLAG_REGION_POSSIBLY_TRUNCATED')
    if not reported:
        evidence.append('ENGINE_COVERAGE_NOT_REPORTED')
    if any(x <= _FACE_TOL or x >= 1.0 - _FACE_TOL for pt in admitted for x in pt['u']):
        evidence.append('ADMITTED_POINT_ON_COMPUTATIONAL_BOX_FACE')
    coverage = ex.get('coverage')
    try:
        coverage = _plain(coverage, 'coverage') if coverage is not None else None
    except (ValueError, TypeError, RecursionError):
        coverage = {'unserialisable': True}

    u_trial = _u_of_trial(S)
    unident = {}
    for d in ex.get('unidentified_directions') or []:
        if isinstance(d, dict) and _is_int(d.get('index')) and _is_real(d.get('sensitivity')):
            unident[int(d['index'])] = float(d['sensitivity'])
    nn_dirs = []
    for k in near_null:
        ddo_sens = unident.get(k, sv[k] if sv is not None else None)
        nn_dirs.append({'index': k, 'vector_u': list(V[k]),
                        'singular_value': (sv[k] if sv is not None else None),
                        'ddo_sensitivity_sigma_per_unit_t': ddo_sens,
                        'trial_projection': _dot(u_trial, V[k])})
    out['admitted_region'] = {
        'exploration_status': status if isinstance(status, str) else _safe_repr(status),
        'exploration_stage_reached': stage if isinstance(stage, str) else _safe_repr(stage),
        'admitted_set_label': INNER_SAMPLE,
        'region_possibly_truncated': bool(evidence),
        'truncation_evidence': evidence,
        'engine_coverage_report': coverage,
        'n_admitted': N,
        'varying_engine_names': list(S['varying_engine']),
        'identified': list(identified),
        'near_null': list(near_null),
        'right_vectors': [list(v) for v in V],
        'singular_values': sv,
        'null_space_complete': True,
        'centroid_identified': centroid,
        'projection_range_identified': prange,
        'admitted_projections_identified': adm_proj,
        'near_null_directions': nn_dirs,
        'bounds_semantics': BOUNDS_SEMANTICS,
        'unit_coordinate_units': U_UNITS,
        'selection_rule': SELECTION_RULE,
        'selection_interior_count': interior_count,
        'selection_anchor_log_index': anchor_li,
        'selected_points': [{'log_index': li, 'role': role} for li, role in plan],
        'observation_region_sha256': region_sha,
        'admission_reverified': region is not None,
        'calibration_fingerprint': fp,
    }
    out['points'] = selected
    out['ok'] = True
    return out


# --------------------------------------------------------------------------
# evaluate_envelopes (per-member arrays; strict validity)
# --------------------------------------------------------------------------

# Synthetic-tested v010 freeze boundary; not a science or certificate acceptance gate.

# 0518/A55: the two existing root-registered row rules. Any additional gate needs
# a separately pinned target-free declaration; this module never invents a rule.
REGISTERED_INVALID_REASONS = frozenset({'QUERY_INSIDE_INNERMOST_NODE', 'QUERY_BEYOND_OUTER_GAS_CUT', 'QUERY_OUTSIDE_RETAINED_SUPPORT'})
INVALID_GATE_SCHEMA = 'REGISTERED_INVALID_ROW_GATE_CX3V001'
# This source fragment is inserted into the immutable v003f module by its builder.
# It uses the module's canonical parser, target screen and regular-file reader.
ROW_ROSTER_SCHEMA = 'ROOT_ROW_REGISTRATION_ROSTER_CX3V001'
ROOT_SLOTS_PATH = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
ROOT_SLOTS_SHA256 = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
ROOT_ROSTER_SCOPE = ('PROGRAM', 'SYNTHETIC_FIXTURE')

def _root_target_screen(doc, where):
    hits, reasons = [], []
    _safe_scan(doc, where, hits, reasons)
    stack = [doc]
    while stack:
        x = stack.pop()
        if isinstance(x, dict):
            for key, value in x.items():
                n = ''.join(c for c in str(key).lower() if c.isalnum())
                if 'target' in n or n.startswith('observed') or n.startswith('vobs'):
                    hits.append(str(key))
                stack.append(value)
        elif isinstance(x, list):
            stack.extend(x)
    if hits or reasons:
        raise ValueError('ROOT_ROSTER_TARGET_FIELDS_REFUSED: ' + where)

def _root_pinned_document(pin, where, screen=True):
    if not isinstance(pin, dict) or set(pin) != {'path', 'sha256'} or not isinstance(pin['path'], str) or not _is_hex64(pin['sha256']):
        raise ValueError('ROOT_ROSTER_PIN_REQUIRED: ' + where)
    raw, real, err = _read_regular(pin['path'], True)
    if raw is None or err or _sha256_hex(raw) != pin['sha256'].lower():
        raise ValueError('ROOT_ROSTER_PIN_MISMATCH: ' + where)
    doc, errors = _parse_json_bytes(raw)
    if errors or not isinstance(doc, dict):
        raise ValueError('ROOT_ROSTER_JSON_REQUIRED: ' + where)
    if screen:
        _root_target_screen(doc, where)
    return doc, {'path': real, 'sha256': _sha256_hex(raw)}

def _exact_string_list(value, where, nonempty=True):
    if not isinstance(value, list) or (nonempty and not value) or not all(isinstance(x, str) and x for x in value) or len(set(value)) != len(value):
        raise ValueError('ROOT_ROSTER_EXACT_STRING_LIST_REQUIRED: ' + where)
    return value

def _root_slots():
    # The existing target-free slots document includes source-citation keys;
    # its exact reviewed byte hash is the authority, not a producer declaration.
    doc, pin = _root_pinned_document({'path': ROOT_SLOTS_PATH, 'sha256': ROOT_SLOTS_SHA256}, 'slots V003', False)
    return doc, pin


REGISTERED_GL_NODES_PATH = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json'
REGISTERED_GL_NODES_SHA256 = 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'

def _registered_gl_nodes(slots):
    """0535 geometry authority is fixed by code/slots pins, never producer input."""
    doc, node_pin = _root_pinned_document({'path': REGISTERED_GL_NODES_PATH,
        'sha256': REGISTERED_GL_NODES_SHA256}, 'registered GL nodes', False)
    if doc.get('schema') != 'NGC_REGISTERED_ROUTE_B_GL_NODES_CX3V001' or doc.get('kpc_m') != 3.085677581491367e19:
        raise ValueError('ROOT_ROSTER_REGISTERED_GL_NODE_SCHEMA')
    config, config_pin = _root_pinned_document(slots['projection_pins']['route_b_config'], 'registered route-B config', False)
    fields = config['fields']
    if fields['radial.source_gauss_order']['value'] != 4 or fields['radial.n_columns']['value'] != 100 or fields['source.profile']['value'] != doc['sources']['profile']:
        raise ValueError('ROOT_ROSTER_REGISTERED_GL_CONFIG_MISMATCH')
    dependencies = [node_pin, config_pin]
    for label, pin in doc['sources'].items():
        if not isinstance(pin, dict) or set(pin) != {'path','sha256'}:
            raise ValueError('ROOT_ROSTER_REGISTERED_GL_SOURCE_PIN')
        raw, real, error = _read_regular(pin['path'], True)
        if error or raw is None or _sha256_hex(raw) != pin['sha256']:
            raise ValueError('ROOT_ROSTER_REGISTERED_GL_SOURCE_MISMATCH: ' + label)
        dependencies.append({'path':real,'sha256':_sha256_hex(raw)})
    for order, count in ((4,100),(10,250)):
        record = doc['orders'][str(order)]
        radii = record['radii_m']
        if record['source_gauss_order'] != order or record['registered_n_columns'] != count or len(radii) != count or not all(_is_real(r) and r > 0 for r in radii) or any(a >= b for a,b in zip(radii,radii[1:])):
            raise ValueError('ROOT_ROSTER_REGISTERED_GL_NODE_SHAPE')
    return doc, dependencies

def _load_row_roster(pin, ids, require_evaluated=False):
    doc, canonical_pin = _root_pinned_document(pin, 'row_registration_roster')
    keys = {'schema', 'scope', 'alternative', 'slots', 'query_manifest', 'query_mapping', 'root_gates', 'outer_cut'}
    if set(doc) != keys or doc['schema'] != ROW_ROSTER_SCHEMA or doc['scope'] not in ROOT_ROSTER_SCOPE:
        raise ValueError('ROOT_ROSTER_SCHEMA_REQUIRED')
    slots, slots_pin = _root_slots()
    supplied_slots, supplied_pin = _root_pinned_document(doc['slots'], 'roster slots', False)
    if supplied_pin['sha256'] != ROOT_SLOTS_SHA256 or supplied_slots != slots:
        raise ValueError('ROOT_ROSTER_SLOTS_V003_REQUIRED')
    alternatives = slots['alternatives']['declared']
    if doc['alternative'] not in alternatives:
        raise ValueError('ROOT_ROSTER_EXACT_SLOTS_ALTERNATIVE_REQUIRED: GL10 aliases are not admitted')
    alt = doc['alternative']
    # STAGE0 successor (M-14): a STAGE0 replay evaluation is permitted here; whether it is frozen is decided only
    # by the receipt rule in write_freeze_manifest (_stage0_freeze_decision), never by this roster read.
    if require_evaluated and alt['status'] != ALT_EVALUATED and alt['name'] != STAGE0_ALTERNATIVE:
        raise ValueError('ROOT_ROSTER_ALTERNATIVE_NOT_EVALUATED: ' + alt['name'])
    qm_doc, qm_pin = _root_pinned_document(doc['query_manifest'], 'roster query manifest')
    qm = load_query_manifest(path=qm_pin['path'], expected_sha256=qm_pin['sha256'])
    if not qm.get('ok') or qm['query_ids'] != list(ids):
        raise ValueError('ROOT_ROSTER_QUERY_MANIFEST_MISMATCH')
    if (doc['scope'] == 'PROGRAM') != (qm_pin['sha256'] == PROGRAM_QUERY_MANIFEST_SHA256):
        raise ValueError('ROOT_ROSTER_QUERY_SCOPE_MISMATCH')
    rows = slots['query_block']['rows']
    mapping = doc['query_mapping']
    expected = [{'query_id': q, 'slots_query_id': s['query_id']} for q, s in zip(ids, rows)]
    if len(ids) != 43 or mapping != expected:
        raise ValueError('ROOT_ROSTER_EXPLICIT_QUERY_MAPPING_REQUIRED')
    if doc['scope'] == 'PROGRAM' and any(x['query_id'] != x['slots_query_id'] for x in mapping):
        raise ValueError('ROOT_ROSTER_PROGRAM_QUERY_ID_MISMATCH')
    # GL10 never evaluates; every currently evaluated slots alternative uses GL4.
    source_invalid = slots['query_block']['invalid_primary_GL4']
    required = {q: {'status': 'INVALID', 'reason': s['primary_GL4']['reason'], 'registration': None}
                for q, s in zip(ids, rows) if s['query_id'] in source_invalid}
    if len(required) != 2 or any(v['reason'] != 'QUERY_INSIDE_INNERMOST_NODE' for v in required.values()):
        raise ValueError('ROOT_ROSTER_GL4_SOURCE_INCONSISTENT')
    radii = {}
    for q in ids:
        value = float(qm['radii_text'][q])
        if not math.isfinite(value) or value <= 0:
            raise ValueError('ROOT_ROSTER_QUERY_RADIUS_INVALID')
        radii[q] = value
    if doc['scope'] == 'PROGRAM' and any(radii[q] != float(s['Rad_text']) for q, s in zip(ids, rows)):
        raise ValueError('ROOT_ROSTER_PROGRAM_RADIUS_MISMATCH')
    deps = [canonical_pin, supplied_pin, slots_pin, qm_pin]
    geometry, geometry_pins = _registered_gl_nodes(slots)
    deps.extend(geometry_pins)
    if alt['name'] == 'STAGE0_GRID_OUTER':
        grid = alt['coefficient_grid_pin']
        raw, real, error = _read_regular(grid['path'], True)
        if error or raw is None or _sha256_hex(raw) != grid['sha256']:
            raise ValueError('ROOT_ROSTER_STAGE0_GRID_PIN_MISMATCH')
        deps.append({'path': real, 'sha256': _sha256_hex(raw)})
    order = 10 if alt['name'] == 'GL10_SOURCE_GAUSS_ORDER' else 4
    gates = {}
    if not isinstance(doc['root_gates'], list):
        raise ValueError('ROOT_ROSTER_GATE_LIST_REQUIRED')
    for gp in doc['root_gates']:
        gd, normalized = _root_pinned_document(gp, 'root-listed gate')
        if gd.get('schema') != INVALID_GATE_SCHEMA or gd.get('registration_status') != 'REGISTERED':
            raise ValueError('ROOT_ROSTER_GATE_REGISTRATION_REQUIRED')
        gr = _exact_string_list(gd.get('registered_reasons'), 'registered_reasons')
        gq = _exact_string_list(gd.get('query_ids'), 'query_ids')
        if any(q not in ids for q in gq):
            raise ValueError('ROOT_ROSTER_GATE_UNKNOWN_QUERY')
        if any(reason in REGISTERED_INVALID_REASONS for reason in gr):
            raise ValueError('ROOT_ROSTER_BUILTIN_REASON_MUST_DERIVE_FROM_RULE')
        for q in gq:
            for reason in gr:
                if (q, reason) in gates:
                    raise ValueError('ROOT_ROSTER_AMBIGUOUS_GATE')
                gates[q, reason] = normalized
        deps.append(normalized)
    cut = doc['outer_cut']
    if not isinstance(cut, dict) or cut.get('mode') not in ('NONE', 'PER_THETA'):
        raise ValueError('ROOT_ROSTER_OUTER_CUT_MODE_REQUIRED')
    contexts = []
    if cut['mode'] == 'NONE':
        if set(cut) != {'mode'}:
            raise ValueError('ROOT_ROSTER_NO_CUT_EXTRA_FIELDS')
    else:
        if set(cut) != {'mode', 'contexts'} or not isinstance(cut['contexts'], list) or not cut['contexts']:
            raise ValueError('ROOT_ROSTER_CUT_CONTEXTS_REQUIRED')
        seen = set()
        for entry in cut['contexts']:
            if not isinstance(entry, dict) or set(entry) != {'theta_ngc', 'cut'}:
                raise ValueError('ROOT_ROSTER_CUT_CONTEXT_SHAPE')
            theta = entry['theta_ngc']
            if not isinstance(theta, dict) or not theta or not all(isinstance(k, str) and _is_real(v) for k, v in theta.items()):
                raise ValueError('ROOT_ROSTER_CUT_THETA_INVALID')
            key = _canonical_bytes(theta)
            if key in seen:
                raise ValueError('ROOT_ROSTER_AMBIGUOUS_CUT_CONTEXT')
            seen.add(key)
            threshold = None
            if entry['cut'] is not None:
                cd, cp = _root_pinned_document(entry['cut'], 'registered outer cut')
                if cd.get('schema') != 'NGC_CANDIDATE_ROSTER_CUT_CX3V001' or cd.get('confinement_status') != 'CERTIFIED_UNCONFINED' or not isinstance(cd.get('classification_evidence'), dict) or not cd['classification_evidence']:
                    raise ValueError('ROOT_ROSTER_REGISTERED_CUT_REQUIRED')
                threshold = cd.get('first_unconfined_R_kpc')
                if not _is_real(threshold) or threshold <= 0:
                    raise ValueError('ROOT_ROSTER_CUT_RADIUS_INVALID')
                deps.append(cp)
            contexts.append((key, threshold))
    return {'pin': canonical_pin, 'document': doc, 'alternative': alt, 'query_manifest': qm_pin,
            'required': required, 'gates': gates, 'radii': radii, 'contexts': contexts,
            'cut_mode': cut['mode'], 'dependencies': deps, 'kpc_m': geometry['kpc_m'],
            'registered_radii_m': geometry['orders'][str(order)]['radii_m']}

def _row_contract(roster, theta):
    required = {q: dict(v) for q, v in roster['required'].items()}
    if roster['cut_mode'] == 'PER_THETA':
        key = _canonical_bytes(theta)
        matches = [radius for th, radius in roster['contexts'] if th == key]
        if len(matches) != 1:
            raise ValueError('ROOT_ROSTER_MISSING_OR_AMBIGUOUS_CUT_THETA')
        cut = matches[0]
        if cut is not None:
            cut_m = cut * roster['kpc_m']
            kept = [r for r in roster['registered_radii_m'] if r < cut_m]
            if not kept:
                raise ValueError('ROOT_ROSTER_NO_RETAINED_ROUTE_B_NODE')
            last_retained_m = kept[-1]
            for q, radius in roster['radii'].items():
                radius_m = radius * roster['kpc_m']
                if radius_m >= cut_m:
                    # F1 requires the exact outer set, even if it overlaps an inner row.
                    required[q] = {'status': 'INVALID', 'reason': 'QUERY_BEYOND_OUTER_GAS_CUT', 'registration': None}
                elif radius_m > last_retained_m:
                    required[q] = {'status': 'INVALID', 'reason': 'QUERY_OUTSIDE_RETAINED_SUPPORT', 'registration': None}
    if len(required) == len(roster['radii']):
        raise ValueError('ROOT_ROSTER_EMPTY_VALID_SET')
    return required

def _authorized_row_registration(roster, required, q, reason):
    if not isinstance(reason, str) or not reason:
        raise ValueError('V010_INVALID_REASON_NOT_REGISTERED: ' + q)
    if q in required:
        if reason != required[q]['reason']:
            raise ValueError('V010_INVALID_REASON_ROW_MISMATCH: ' + q)
        return dict(required[q])
    gate = roster['gates'].get((q, reason))
    if gate is None:
        raise ValueError('V010_INVALID_NOT_ROOT_ROSTERED: ' + q)
    return {'status': 'INVALID', 'reason': reason, 'registration': dict(gate)}

def _root_result_rows(result, ids, roster, theta):
    """Contradictions refuse even for valid:false; provenance is checked only for valid:true."""
    required = _row_contract(roster, theta)
    reasons = []
    rows, speeds = result.get('rows'), result.get('speeds_km_s')
    true_member = result.get('valid') is True
    # A genuine failed member supplies no usable predictions. Missing/partial
    # diagnostics therefore do not need the successful 43-row schema, but supplied
    # values must not contradict mandatory or producer-declared INVALID rows.
    # The root contract above is verified even when every diagnostic is absent.
    if not true_member:
        diagnostic_map = speeds if isinstance(speeds, dict) else {}
        for q in required:
            if diagnostic_map.get(q) is not None:
                reasons.append('V010_FINITE_ON_ROSTER_INVALID_CONTRADICTION: ' + q)
        for row in rows if isinstance(rows, list) else []:
            if not isinstance(row, dict):
                continue
            q = row.get('id')
            speed = row.get('speed_km_s')
            mapped = diagnostic_map.get(q) if isinstance(q, str) else None
            if isinstance(q, str) and q in required and (speed is not None or mapped is not None):
                reasons.append('V010_FINITE_ON_ROSTER_INVALID_CONTRADICTION: ' + q)
            if row.get('valid') is False:
                if speed is not None or mapped is not None:
                    reasons.append('V010_FINITE_ON_INVALID_CONTRADICTION: ' + str(q))
                try:
                    registration = _authorized_row_registration(roster, required, q, row.get('reason'))
                    if row.get('registered_invalid_gate') is not None and row['registered_invalid_gate'] != registration['registration']:
                        reasons.append('V010_PRODUCER_GATE_NOT_ROOT_LISTED: ' + str(q))
                except (ValueError, TypeError) as exc:
                    reasons.append('V010_FAILED_MEMBER_ROW_REGISTRATION_REFUSED: ' + str(exc))
        return reasons
    if not isinstance(rows, list) or len(rows) != len(ids) or [r.get('id') if isinstance(r, dict) else None for r in rows] != list(ids):
        return ['V010_QUERY_ORDER_OR_DUPLICATE_REFUSED']
    if not isinstance(speeds, dict) or set(speeds) != set(ids):
        return ['V010_EXACT_SPEED_MAP_REQUIRED']
    invalid = []
    for row in rows:
        q = row['id'];rv = row.get('valid');speed = row.get('speed_km_s');reason = row.get('reason')
        if q in required and (speed is not None or speeds[q] is not None or rv is not False):
            reasons.append('V010_FINITE_OR_VALID_ON_ROSTER_INVALID_CONTRADICTION: ' + q)
        if rv is False:
            invalid.append(q)
            if speed is not None or speeds[q] is not None:
                reasons.append('V010_FINITE_ON_INVALID_CONTRADICTION: ' + q)
            try:
                registration = _authorized_row_registration(roster, required, q, reason)
                # A producer pin is optional redundant metadata, never authority.
                if row.get('registered_invalid_gate') is not None and row['registered_invalid_gate'] != registration['registration']:
                    reasons.append('V010_PRODUCER_GATE_NOT_ROOT_LISTED: ' + q)
            except ValueError as exc:
                reasons.append(str(exc))
        elif rv is True:
            if reason not in (None, '') or row.get('registered_invalid_gate') is not None:
                reasons.append('V010_VALID_ROW_METADATA_CONTRADICTION: ' + q)
            if true_member and (not _is_real(speed) or not _is_real(speeds[q]) or speed != speeds[q]):
                reasons.append('V010_NONFINITE_VALID_OR_SPEED_DISAGREEMENT: ' + q)
        else:
            reasons.append('V010_ROW_VALID_FLAG_REQUIRED: ' + q)
    if result.get('invalid_rows') != invalid:
        reasons.append('V010_INVALID_QUERY_ROSTER_DISAGREEMENT')
    if true_member and len(invalid) == len(ids):
        reasons.append('V010_EMPTY_REGISTERED_VALID_SET')
    return reasons

def _root_frozen_rows(member, ids, roster):
    if not member.get('evaluated'):
        return
    required = _row_contract(roster, member['theta_ngc'])
    for j, q in enumerate(ids):
        rv, speed, registration = member['row_valid'][j], member['speeds_km_s'][j], member['row_registration'][j]
        if q in required and (rv or speed is not None):
            raise ValueError('ROOT_ROSTER_FINITE_ON_INVALID_FROZEN_ROW: ' + q)
        if member['forward_valid_flag'] is True:
            if rv:
                if not _is_real(speed) or registration is not None:
                    raise ValueError('ROOT_ROSTER_VALID_FROZEN_ROW_MISMATCH: ' + q)
            else:
                expected = _authorized_row_registration(roster, required, q, registration['reason'] if isinstance(registration, dict) else None)
                if speed is not None or registration != expected:
                    raise ValueError('ROOT_ROSTER_INVALID_FROZEN_ROW_MISMATCH: ' + q)
        elif rv or speed is not None or registration is not None:
            raise ValueError('ROOT_ROSTER_FAILED_MEMBER_CARRIES_ROWS')
    if member['forward_valid_flag'] is True and not any(member['row_valid']):
        raise ValueError('ROOT_ROSTER_EMPTY_VALID_SET')

def _root_rosters_for_alternatives(pins, alternatives, ids):
    if _stage0_status_neutral(alternatives) != _root_slots()[0]['alternatives']:   # STAGE0 successor (M-14)
        raise ValueError('ROOT_ROSTERS_EXACT_ORDERED_SLOTS_ALTERNATIVES_REQUIRED: GL10 and all declared alternatives are fixed')
    if not isinstance(pins, dict) or set(pins) != {a['name'] for a in alternatives['declared']}:
        raise ValueError('ROOT_ROSTERS_EXACT_ALTERNATIVE_SET_REQUIRED: GL10/SLOTS identities may not be renamed')
    rosters = {name: _load_row_roster(pin, ids) for name, pin in pins.items()}
    for alternative in alternatives['declared']:
        if rosters[alternative['name']]['alternative'] != _stage0_neutral_record(alternative):
            raise ValueError('ROOT_ROSTER_SLOTS_ALTERNATIVE_MISMATCH: GL10 status/name is bound to slots V003')
    if alternatives['primary'] != _root_slots()[0]['alternatives']['primary']:
        raise ValueError('ROOT_ROSTER_PRIMARY_MISMATCH: GL10 cannot become primary')
    return rosters

def _root_manifest_check(doc):
    rosters = _root_rosters_for_alternatives(doc['row_registration_rosters'], doc['alternatives'], doc['query_ids'])
    input_pins = {(p['path'], p['sha256']) for p in doc['pins']['input_files']}
    qb = doc['input_bindings']['query_manifest']
    for roster in rosters.values():
        if roster['query_manifest'] != {k: qb[k] for k in ('path', 'sha256')}:
            raise ValueError('ROOT_ROSTER_FREEZE_QUERY_BINDING_MISMATCH')
        if any((p['path'], p['sha256']) not in input_pins for p in roster['dependencies']):
            raise ValueError('ROOT_ROSTER_DEPENDENCY_NOT_PINNED')
    primary = rosters[doc['alternatives']['primary']]
    for member in doc['members']:
        _root_frozen_rows(member, doc['query_ids'], primary)
    for entry in doc['sensitivity']['evaluations']:
        _root_frozen_rows(entry, doc['query_ids'], primary)
    for name, result in doc['alternative_results'].items():
        for member in result['members']:
            _root_frozen_rows(member, doc['query_ids'], rosters[name])


def _invalid_registration_ok(q, reason, registration):
    if reason in REGISTERED_INVALID_REASONS and registration is None:
        return True
    if not isinstance(registration, dict) or set(registration) != {'path', 'sha256'} or not _is_hex64(registration.get('sha256')):
        return False
    raw, _real, err = _read_regular(registration['path'], True)
    if raw is None or err or _sha256_hex(raw) != registration['sha256']:
        return False
    doc, errors = _parse_json_bytes(raw)
    hits, reasons = [], []
    _safe_scan(doc, 'registered_invalid_gate', hits, reasons)
    return bool(not errors and not hits and not reasons and isinstance(doc, dict)
                and doc.get('schema') == INVALID_GATE_SCHEMA and doc.get('registration_status') == 'REGISTERED'
                and isinstance(doc.get('registered_reasons'), list) and all(isinstance(x,str) for x in doc['registered_reasons'])
                and isinstance(doc.get('query_ids'), list) and all(isinstance(x,str) for x in doc['query_ids'])
                and reason in doc['registered_reasons'] and q in doc['query_ids'])


def _registered_rows_ok(m, ids):
    regs = m.get('row_registration')
    if not isinstance(regs, list) or len(regs) != len(ids):
        return False
    for q, rv, speed, reg in zip(ids, m['row_valid'], m['speeds_km_s'], regs):
        if rv:
            if not _is_real(speed) or reg is not None:
                return False
        elif reg is not None:
            if not isinstance(reg, dict) or set(reg) != {'status', 'reason', 'registration'} or reg['status'] != 'INVALID' or speed is not None or not _invalid_registration_ok(q, reg['reason'], reg['registration']):
                return False
        elif m['forward_valid_flag'] is True:
            return False
    return True


def _member_contract_valid(m):
    return bool(m['evaluated'] and m['forward_valid_flag'] is True
                and any(m['row_valid']) and all(rv or reg is not None for rv, reg in zip(m['row_valid'], m['row_registration'])))

def _v010_preflight(result, ids, roster, theta):
    reasons, hits = [], []
    _safe_scan(result, 'forward_ngc_result', hits, reasons)
    if hits:
        reasons.append('V010_TARGET_FIELD_REFUSED: ' + ', '.join(hits[:8]))
    # Recognise spellings that the older exact-name screen did not cover.
    stack = [result]
    seen = set()
    while stack:
        obj = stack.pop()
        if isinstance(obj, (dict, list, tuple)):
            if id(obj) in seen:
                continue
            seen.add(id(obj))
        if isinstance(obj, dict):
            for key, value in obj.items():
                norm = ''.join(c for c in str(key).lower() if c.isalnum())
                if ('target' in norm or norm.startswith('observed') or norm.startswith('vobs')):
                    reasons.append('V010_TARGET_FIELD_REFUSED: key ' + str(key))
                stack.append(value)
        elif isinstance(obj, (list, tuple)):
            stack.extend(obj)
    if reasons or not isinstance(result, dict):
        return reasons
    try:
        reasons.extend(_root_result_rows(result, ids, roster, theta))
    except ValueError as exc:
        reasons.append('V010_ROOT_ROSTER_REFUSED: ' + str(exc))
    if reasons or result.get('valid') is not True:
        return reasons
    if result.get('schema') != 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001':
        reasons.append('V010_RESULT_SCHEMA_REQUIRED')
    if result.get('galaxy') != 'NGC3198' or result.get('status') != 'COMPLETED':
        reasons.append('V010_NGC_COMPLETED_REQUIRED')
    if result.get('scored') is not False:
        reasons.append('V010_UNSCORED_REQUIRED')
    for key in ('driver_sha256', 'call_spec_sha256'):
        if not _is_hex64(result.get(key)):
            reasons.append('V010_RESULT_PIN_REQUIRED: ' + key)
    ra = result.get('route_a_outcome') or {}
    if ra.get('classification') != 'CONVERGED' or ra.get('converged_finite_fixed_point') is not True:
        reasons.append('V010_ROUTE_A_CONVERGENCE_REQUIRED')
    ro = ra.get('ro1') or {}
    if ro.get('rule') != 'RO1' or ro.get('armed') is not True or type(ro.get('fired')) is not bool:
        reasons.append('V010_RO1_ARMED_REQUIRED')
    if not _is_hex64(ro.get('worker_sha256')) or not _is_hex64(ro.get('binding_sha256')):
        reasons.append('V010_RO1_PINS_REQUIRED')
    events = ro.get('events')
    if not isinstance(events, list) or bool(events) != bool(ro.get('fired')) or 'inadmissible_record' in ro:
        reasons.append('V010_RO1_EVENT_CONSISTENCY_REQUIRED')
    elif ro.get('fired'):
        if len(events) != 1 or events[0].get('code') != 'ROUTE_A_READOUT_NO_CIRCULAR_BRANCH' or events[0].get('after_convergence') is not True or events[0].get('refusal') not in (
                'NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH',
                'DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed', 'NON_TIMELIKE_COLUMN'):
            reasons.append('V010_RO1_EVENT_REFUSED')
    u = result.get('uv_tail') or {}
    if u.get('schema') != 'UNT_GALAXY_M0_FORWARD_UV_TAIL_C2V010' or u.get('enabled') is not True:
        reasons.append('V010_TAIL_RECORD_REQUIRED')
    if u.get('admissibility') != 'production' or u.get('pending_certificates') != []:
        reasons.append('V010_TAIL_CERTIFICATE_SLOTS_UNFILLED')
    rule = u.get('source_rule')
    if rule not in ('continuum_v001', 'nodes_v001'):
        reasons.append('V010_SOURCE_RULE_REFUSED')
    if rule == 'continuum_v001' and u.get('nodes_ext_context') is not None:
        reasons.append('V010_CONTINUUM_NODES_CONTEXT_REFUSED')
    if rule == 'nodes_v001' and not isinstance(u.get('nodes_ext_context'), dict):
        reasons.append('V010_NODES_CONTEXT_REQUIRED')
    if not _is_hex64((u.get('config') or {}).get('normalized_sha256')):
        reasons.append('V010_TAIL_CONFIG_PIN_REQUIRED')
    stages = u.get('stage_records')
    if not isinstance(stages, list) or not stages:
        reasons.append('V010_TAIL_STAGE_RECORDS_REQUIRED')
    else:
        for stage in stages:
            if not isinstance(stage, dict) or not _is_hex64(stage.get('finish_sha256')) or not _is_hex64(stage.get('state_digest')) or stage.get('production_admissible') is not True or stage.get('test_only_admitted') is True:
                reasons.append('V010_TAIL_STAGE_CUSTODY_REFUSED')
                break
    # The raw result and its provenance must be separately pinned in input_files.
    # This boundary checks schema and fail-closed consumption; it does not certify physics,
    # authenticate the producer, or infer adoption from synthetically populated certificates.
    return reasons


def _call_forward(forward_ngc, theta, ids, roster):
    """0518 D1: finite on every registered-valid row; registered INVALID remains null."""
    preasons=[];exc=None;nq=len(ids);rv=[False]*nq;speeds=[None]*nq;regs=[None]*nq
    try:
        result=forward_ngc(dict(theta))
    except Exception as e:
        exc='%s: %s' % (type(e).__name__, _safe_str(e))
        return None,rv,speeds,['exception raised by forward_ngc: '+exc],exc,regs
    try:
        if not isinstance(result,dict):
            return None,rv,speeds,['forward_ngc returned non-dict'],None,regs
        boundary=_v010_preflight(result,ids,roster,theta)
        if boundary:
            return False,rv,speeds,boundary,None,regs
        flag=result.get('valid') is True
        rr=result.get('reasons',[])
        preasons.extend('forward_ngc reason: '+_safe_str(r) for r in (rr if isinstance(rr,(list,tuple)) else [rr]))
        if not flag:
            preasons.append('forward_ngc valid flag is not True')
            return False,rv,speeds,preasons,None,regs
        for j,row in enumerate(result['rows']):
            if row['valid'] is True:
                rv[j]=True;speeds[j]=float(row['speed_km_s'])
            else:
                regs[j]=_authorized_row_registration(roster,_row_contract(roster,theta),row['id'],row['reason'])
        return True,rv,speeds,preasons,None,regs
    except Exception as e:
        exc='handling forward_ngc return raised %s: %s' % (type(e).__name__,_safe_str(e))
        return None,[False]*nq,[None]*nq,['V010_RESULT_HANDLING_REFUSED: '+exc],exc,[None]*nq



def _pointwise_envelope(members, ids, label=ENVELOPE_LABEL):
    """A3 + P34-06 (v003): a query is valid iff EVERY selected member was evaluated (status COMPLETE) and at
    least one member is valid; the band is the min/max over the VALID members. A member whose evaluation is
    invalid (forward_valid_flag is not True) is excluded and counted in n_excluded_invalid instead of voiding
    every query; it still scores 0 in the headline and is visible in the member arrays."""
    rows = []
    n = len(members)
    n_uneval = sum(1 for m in members if not m['evaluated'])
    for j, q in enumerate(ids):
        vals = [m['speeds_km_s'][j] for m in members if m['row_valid'][j]]
        nv = len(vals)
        n_excl = sum(1 for m in members if m['evaluated'] and not m['row_valid'][j])
        rows.append({'id': q, 'band_low_km_s': (min(vals) if nv else None),
                     'band_high_km_s': (max(vals) if nv else None), 'n_members': n, 'n_valid': nv,
                     'n_excluded_invalid': n_excl, 'n_unevaluated': n_uneval,
                     'valid': bool(n >= 1 and n_uneval == 0 and nv >= 1), 'label': label})
    return rows


@_fail_closed
def evaluate_envelopes(*, forward_ngc, points, spec, query_ids, budget, row_registration_roster=None):
    """Evaluate forward_ngc at every selected member; freeze per-member arrays.

    forward_ngc receives the member's shared coordinates plus the NGC3198 nuisance slots at their
    trial values; DDO154 nuisances are never passed (D10). D1 (0531): a member is valid only if
    valid is True, every root-roster-valid row is finite, registered INVALID rows are null, and the
    valid-row set is nonempty. Genuine valid:false failures are MEMBER_INVALID. status COMPLETE iff every
    selected member was evaluated; budget exhaustion keeps the unevaluated members as evaluated=False
    records. P34-06: a pointwise-envelope query is valid iff the status is COMPLETE and at least one
    member is valid; invalid members are excluded from the band and counted (n_member_invalid).
    D2: pass select_representative_points' points unchanged; the writer refuses any other member set.
    """
    reasons = []
    out = {'ok': False, 'status': None, 'stage': 'ngc_members', 'members': [], 'envelopes': {},
           'pointwise_envelope': [], 'evaluations_used': 0, 'budget': None, 'n_selected': 0,
           'n_evaluated': 0, 'n_member_valid': 0, 'n_member_invalid': 0, 'query_ids': [], 'reasons': reasons}
    if not callable(forward_ngc):
        reasons.append('forward_ngc must be callable')
    S = _spec_from(spec, reasons)
    ids = _check_query_ids(query_ids, reasons, False)
    try:
        roster = _load_row_roster(row_registration_roster, ids or [], require_evaluated=True)
        out['row_registration_roster'] = roster['pin']
    except (ValueError, TypeError, KeyError) as exc:
        reasons.append('ROOT_ROSTER_REFUSED: ' + str(exc))
        return out
    if not _is_int(budget) or budget < 0:
        reasons.append('budget must be a non-negative integer')
    if not isinstance(points, (list, tuple)) or len(points) == 0:
        reasons.append('points must be a non-empty list')
    if reasons:
        return out
    budget = int(budget)
    n = len(S['varying_engine'])
    engine_set = set(S['engine_names'])
    members = []
    seen = set()
    for i, pt in enumerate(points):
        where = 'points[%d]' % i
        if not isinstance(pt, dict):
            reasons.append('%s is not a dict' % where)
            continue
        theta = _bind_theta(pt.get('theta_natural'), where, reasons)
        u = _bind_u(pt.get('u'), where, reasons)
        if theta is None or u is None:
            continue
        if set(theta) != engine_set:
            reasons.append('%s.theta_natural keys differ from the engine coordinates' % where)
            continue
        if len(u) != n:
            reasons.append('%s.u has length %d, expected %d' % (where, len(u), n))
            continue
        li = pt.get('log_index')
        role = pt.get('role')
        if not _is_int(li):
            reasons.append('%s.log_index is not an integer' % where)
            continue
        if int(li) in seen:
            reasons.append('%s duplicates log_index %d' % (where, int(li)))
            continue
        seen.add(int(li))
        if not isinstance(role, str) or role not in ROLES:
            reasons.append('%s.role must be one of %s' % (where, list(ROLES)))
            continue
        proj = pt.get('identified_projection')
        if not isinstance(proj, (list, tuple)) or not proj or not all(_is_real(x) for x in proj):
            reasons.append('%s.identified_projection must be a non-empty list of finite reals '
                           '(use select_representative_points)' % where)
            continue
        members.append({'member_id': 'M%03d' % i, 'point_index': i, 'role': role, 'log_index': int(li),
                        'u': u, 'identified_projection': [float(x) for x in proj], 'theta_engine': theta,
                        'theta_ngc': _theta_ngc_from_engine(S, theta), 'evaluated': False,
                        'forward_valid_flag': None, 'member_valid': False,
                        'row_valid': [False] * len(ids), 'speeds_km_s': [None] * len(ids), 'row_registration': [None] * len(ids),
                        'reasons': [], 'exception': None})
    if reasons:
        return out
    if len(set(len(m['identified_projection']) for m in members)) != 1:
        reasons.append('identified_projection lengths differ across points')
        return out
    used = 0
    for m in members:
        if used >= budget:
            m['reasons'] = ['NOT_EVALUATED: budget %d exhausted' % budget]
            continue
        flag, row_valid, speeds, preasons, exc, row_registration = _call_forward(forward_ngc, m['theta_ngc'], ids, roster)
        used += 1
        m['evaluated'] = True
        m['forward_valid_flag'] = flag
        m['row_valid'] = row_valid
        m['speeds_km_s'] = speeds
        m['row_registration'] = row_registration
        m['member_valid'] = _member_contract_valid(m)
        m['reasons'] = _cap_reasons(preasons)
        m['exception'] = exc
        if any(r.startswith('V010_') for r in preasons):
            reasons.append('FREEZE_CONTRACT_REFUSED: '+m['member_id'])
    if reasons:
        out['members']=members
        return out
    n_eval = sum(1 for m in members if m['evaluated'])
    status = STATUS_COMPLETE if n_eval == len(members) else STATUS_BUDGET
    if status != STATUS_COMPLETE:
        reasons.append('BUDGET_EXHAUSTED: %d of %d selected members evaluated' % (n_eval, len(members)))
    env = _pointwise_envelope(members, ids, _mode_labels(S)[0])
    n_mv = sum(1 for m in members if m['member_valid'])
    if n_eval - n_mv:
        reasons.append('MEMBER_INVALID: %d evaluated member(s) invalid (excluded from the envelope, scored 0): %s'
                       % (n_eval - n_mv, [m['member_id'] for m in members if m['evaluated'] and not m['member_valid']]))
    out.update({'status': status, 'members': members, 'pointwise_envelope': env,
                'envelopes': {r['id']: r for r in env}, 'evaluations_used': used, 'budget': budget,
                'n_selected': len(members), 'n_evaluated': n_eval,
                'n_member_valid': n_mv, 'n_member_invalid': n_eval - n_mv, 'query_ids': list(ids),
                'ok': True})
    return out


# --------------------------------------------------------------------------
# select_reference_member (D5)
# --------------------------------------------------------------------------

def _reference_ranking(members, centroid):
    cands = []
    for m in members:
        if not (m['evaluated'] is True and m['member_valid'] is True):
            continue
        p = m['identified_projection']
        d = math.sqrt(math.fsum((a - b) ** 2 for a, b in zip(p, centroid)))
        cands.append({'member_id': m['member_id'], 'log_index': m['log_index'], 'distance': float(d)})
    cands.sort(key=lambda c: (c['distance'], c['log_index']))
    return cands


@_fail_closed
def select_reference_member(*, selection, evaluation):
    """Apply REFERENCE_RULE to the evaluated members (before any target access)."""
    reasons = []
    out = {'ok': False, 'member_id': None, 'log_index': None, 'rule': REFERENCE_RULE,
           'centroid_identified': None, 'distance': None, 'ranking': [], 'member': None, 'reasons': reasons}
    if not isinstance(selection, dict) or selection.get('ok') is not True or \
            not isinstance(selection.get('admitted_region'), dict):
        reasons.append('selection must be an ok output of select_representative_points')
        return out
    if not isinstance(evaluation, dict) or evaluation.get('ok') is not True or \
            not isinstance(evaluation.get('members'), list):
        reasons.append('evaluation must be an ok output of evaluate_envelopes')
        return out
    centroid = selection['admitted_region']['centroid_identified']
    members = evaluation['members']
    if any(len(m['identified_projection']) != len(centroid) for m in members):
        reasons.append('member projections do not match the centroid dimension')
        return out
    ranking = _reference_ranking(members, centroid)
    out['centroid_identified'] = list(centroid)
    out['ranking'] = ranking
    if not ranking:
        reasons.append('NO_VALID_MEMBER: no evaluated member is finite on every registered-valid row; nothing realizable '
                       'to freeze')
        return out
    best = ranking[0]
    out['member_id'] = best['member_id']
    out['log_index'] = best['log_index']
    out['distance'] = best['distance']
    out['member'] = next(m for m in members if m['member_id'] == best['member_id'])
    out['ok'] = True
    return out


# --------------------------------------------------------------------------
# evaluate_sensitivity (D6)
# --------------------------------------------------------------------------

def _edge_t(a, d):
    """Largest s >= 0 with a + s*d inside [0, 1]^n up to the face slack _V_TOL; components |d_i| <= _V_TOL are
    inert (A2 lesson). v003d (SF-2): the engine's face slack (calibration_region_engine _edge_t): a component above
    _V_TOL pointing out of a face the point sits on limits s to _V_TOL / |d_i| instead of 0."""
    smax = math.inf
    for ai, di in zip(a, d):
        if abs(di) <= _V_TOL:
            continue
        lim = max(1.0 - ai, _V_TOL) / di if di > 0 else min(0.0 - ai, -_V_TOL) / di
        smax = min(smax, lim)
    if not math.isfinite(smax):
        return 0.0
    return max(0.0, smax)


def _bind_null_rule(rule, reasons):
    if not isinstance(rule, dict) or rule.get('mode') not in ('box_ends', 'step'):
        reasons.append('null_direction_rule must be {"mode": "box_ends"} or {"mode": "step", "step_u": >0}')
        return None
    if rule['mode'] == 'box_ends':
        if set(rule) != {'mode'}:
            reasons.append('null_direction_rule box_ends takes no other keys')
            return None
        return {'mode': 'box_ends'}
    if set(rule) != {'mode', 'step_u'} or not _is_real(rule.get('step_u')) or not float(rule['step_u']) > 0:
        reasons.append('null_direction_rule step requires step_u > 0 (unit-box units)')
        return None
    return {'mode': 'step', 'step_u': float(rule['step_u'])}


def _sensitivity_plan(S, ref, nn_dirs, rule):
    """Planned one-at-a-time displacements from the reference member (deterministic order)."""
    plan = []
    u0 = ref['u']
    for d in nn_dirs:
        v = d['vector_u']
        for side, sign in (('minus', -1.0), ('plus', 1.0)):
            vec = [sign * x for x in v]
            t_box = _edge_t(u0, vec)
            if rule['mode'] == 'box_ends':
                t, lim = t_box, 'COMPUTATIONAL_BOX'
            else:
                t = min(rule['step_u'], t_box)
                lim = 'DECLARED_STEP' if rule['step_u'] <= t_box else 'COMPUTATIONAL_BOX'
            ud = [min(1.0, max(0.0, a + t * b)) for a, b in zip(u0, vec)]
            th_eng = _theta_engine_from_u(S, ud)
            ddo = d['ddo_sensitivity_sigma_per_unit_t']
            plan.append({'kind': SENS_NULL, 'target': str(d['index']), 'side': side,
                         'displacement': float(sign * t), 'displacement_units': U_UNITS, 'limited_by': lim,
                         'u_displaced': ud, 'theta_ngc': _theta_ngc_from_engine(S, th_eng),
                         # v003d (SF-2): with the face slack a genuine outward component at a face gives a step of
                         # _V_TOL / |d_i|; the displaced point then equals the reference to _FACE_TOL: still skipped
                         'skipped_zero_displacement': bool(t <= _ZERO_DISP or
                                                           t * max((abs(x) for x in vec), default=0.0) <= _FACE_TOL),
                         'linearised_ddo_shift_sigma': (float(ddo * t) if ddo is not None else None)})
    for nm in S['sensitivity_targets']:
        c = S['by_name'][nm]
        kind = SENS_NGC if c['scope'] == SCOPE_NGC else SENS_FIXED
        for side in ('minus', 'plus'):
            if c['sensitivity']['mode'] == 'box_ends':
                val = c['lower'] if side == 'minus' else c['upper']
                lim = 'COMPUTATIONAL_BOX'
            else:
                step = c['sensitivity']['step']
                raw = c['trial_value'] - step if side == 'minus' else c['trial_value'] + step
                val = min(c['upper'], max(c['lower'], raw))
                lim = 'DECLARED_STEP' if val == raw else 'COMPUTATIONAL_BOX'
            th = dict(ref['theta_ngc'])
            th[nm] = float(val)
            plan.append({'kind': kind, 'target': nm, 'side': side, 'displacement': float(val - c['trial_value']),
                         'displacement_units': c['units'], 'limited_by': lim, 'u_displaced': None,
                         'theta_ngc': th, 'skipped_zero_displacement': bool(val == c['trial_value']),
                         'linearised_ddo_shift_sigma': None})
    for i, p in enumerate(plan):
        p['entry_id'] = 'S%03d' % i
    return plan


def _sensitivity_summary(ref, entries, ids, label=SENSITIVITY_LABEL):
    active = [e for e in entries if not e['skipped_zero_displacement']]
    per_query = []
    for j, q in enumerate(ids):
        r = ref['speeds_km_s'][j] if ref['row_valid'][j] else None
        vals = [e['speeds_km_s'][j] for e in active if e['row_valid'][j]]
        allv = ([r] if r is not None else []) + vals
        valid = bool(allv) and all(e['evaluated'] and (e['row_valid'][j] or e['row_registration'][j] is not None) for e in active)
        if r is not None and vals:
            mad = max(abs(v - r) for v in vals)
        elif r is not None and not active:
            mad = 0.0
        else:
            mad = None
        per_query.append({'id': q, 'reference_speed_km_s': r,
                          'box_limited_band_low_km_s': (min(allv) if allv else None),
                          'box_limited_band_high_km_s': (max(allv) if allv else None),
                          'max_abs_delta_km_s': (float(mad) if mad is not None else None),
                          'n_planned': len(active), 'n_valid': len(vals), 'valid': bool(valid),
                          'label': label})
    per_target = []
    keys = []
    for e in entries:
        k = (e['kind'], e['target'])
        if k not in keys:
            keys.append(k)
    for kind, target in keys:
        es = [e for e in active if e['kind'] == kind and e['target'] == target]
        mads = []
        for j in range(len(ids)):
            if not ref['row_valid'][j] or any(not e['row_valid'][j] for e in es):
                mads.append(None)
            elif not es:
                mads.append(0.0)
            else:
                mads.append(float(max(abs(e['speeds_km_s'][j] - ref['speeds_km_s'][j]) for e in es)))
        per_target.append({'kind': kind, 'target': target, 'max_abs_delta_km_s': mads})
    return per_query, per_target


@_fail_closed
def evaluate_sensitivity(*, forward_ngc, reference, selection, spec, query_ids, null_direction_rule, budget, row_registration_roster=None):
    """D6: evaluate forward_ngc displaced from the reference member, one direction at a time.

    Every near-null direction (unit-box u space, both signs) is displaced to the computational-box
    edge ('box_ends') or by step_u; every coordinate with a declared sensitivity (fixed shared
    coordinates, NGC3198 nuisances) goes to its box ends or trial +/- step. No DDO154 re-check is
    made; linearised_ddo_shift_sigma = DDO154 sensitivity x |t| is recorded for null directions.
    Returns per-query box-limited bands (reported separately from the pointwise envelope) and
    per-target max |delta|.
    """
    reasons = []
    out = {'ok': False, 'status': None, 'stage': 'ngc_sensitivity', 'budget': None, 'evaluations_used': 0,
           'reference_member_id': None, 'null_direction_rule': None, 'evaluations': [], 'per_query': [],
           'per_target': [], 'label': SENSITIVITY_LABEL, 'reasons': reasons}
    if not callable(forward_ngc):
        reasons.append('forward_ngc must be callable')
    S = _spec_from(spec, reasons)
    ids = _check_query_ids(query_ids, reasons, False)
    try:
        roster = _load_row_roster(row_registration_roster, ids or [], require_evaluated=True)
        out['row_registration_roster'] = roster['pin']
    except (ValueError, TypeError, KeyError) as exc:
        reasons.append('ROOT_ROSTER_REFUSED: ' + str(exc))
        return out
    rule = _bind_null_rule(null_direction_rule, reasons)
    if not _is_int(budget) or budget < 0:
        reasons.append('budget must be a non-negative integer')
    if not isinstance(reference, dict) or reference.get('ok') is not True or \
            not isinstance(reference.get('member'), dict):
        reasons.append('reference must be an ok output of select_reference_member')
    if not isinstance(selection, dict) or selection.get('ok') is not True or \
            not isinstance(selection.get('admitted_region'), dict):
        reasons.append('selection must be an ok output of select_representative_points')
    if reasons:
        return out
    sens_label = _mode_labels(S)[1]   # v003b: the A13 condition in the fixed-distance mode
    out['label'] = sens_label
    ref = reference['member']
    if len(ref['speeds_km_s']) != len(ids):
        reasons.append('reference member arrays do not match query_ids')
        return out
    th = _theta_engine_from_u(S, ref['u'])
    bad = [nm for nm in S['engine_names'] if not _close(th[nm], ref['theta_engine'][nm])]
    if bad:
        reasons.append('reference member theta inconsistent with its u under the spec for %s' % bad)
        return out
    plan = _sensitivity_plan(S, ref, selection['admitted_region']['near_null_directions'], rule)
    used = 0
    budget = int(budget)
    entries = []
    for p in plan:
        e = dict(p)
        e.update({'evaluated': False, 'forward_valid_flag': None, 'row_valid': [False] * len(ids),
                  'speeds_km_s': [None] * len(ids), 'row_registration': [None] * len(ids), 'delta_from_reference_km_s': [None] * len(ids),
                  'reasons': [], 'exception': None})
        if e['skipped_zero_displacement']:
            e['reasons'] = [SKIP_ZERO_DISPLACEMENT_REASON]   # v003d (SF-2): the rule, not a guessed cause
        elif used >= budget:
            e['reasons'] = ['NOT_EVALUATED: sensitivity budget %d exhausted' % budget]
        else:
            flag, row_valid, speeds, preasons, exc, row_registration = _call_forward(forward_ngc, e['theta_ngc'], ids, roster)
            used += 1
            e['evaluated'] = True
            e['forward_valid_flag'] = flag
            e['row_valid'] = row_valid
            e['speeds_km_s'] = speeds
            e['row_registration'] = row_registration
            e['delta_from_reference_km_s'] = [
                (float(s - r) if (rv and ok) else None)
                for s, r, rv, ok in zip(speeds, ref['speeds_km_s'], ref['row_valid'], row_valid)]
            e['reasons'] = _cap_reasons(preasons)
            e['exception'] = exc
            if any(r.startswith('V010_') for r in preasons):
                reasons.append('FREEZE_CONTRACT_REFUSED: '+e['entry_id'])
        entries.append(e)
    if reasons:
        return out
    pending = [e for e in entries if not e['skipped_zero_displacement'] and not e['evaluated']]
    status = STATUS_COMPLETE if not pending else STATUS_BUDGET
    if pending:
        reasons.append('BUDGET_EXHAUSTED: %d planned sensitivity evaluations not run' % len(pending))
    per_query, per_target = _sensitivity_summary(ref, entries, ids, sens_label)
    out.update({'ok': True, 'status': status, 'budget': budget, 'evaluations_used': used,
                'reference_member_id': ref['member_id'], 'null_direction_rule': rule, 'evaluations': entries,
                'per_query': per_query, 'per_target': per_target})
    return out


# --------------------------------------------------------------------------
# Manifest structure validation (shared by the writer and the verifier)
# --------------------------------------------------------------------------

def _bind_alternatives(alternatives, reasons):
    """D9: {'primary': name, 'declared': [{name, kind, description, status}]}."""
    if not isinstance(alternatives, dict) or set(alternatives) != {'primary', 'declared'}:
        reasons.append('alternatives must be {"primary": name, "declared": [...]}')
        return None
    try:
        registered = _root_slots()[0]['alternatives']
    except (ValueError, TypeError, KeyError) as exc:
        reasons.append('ROOT_SLOTS_BINDING_REFUSED: ' + str(exc))
        return None
    # STAGE0 successor (M-14): the one tolerated difference is STAGE0's status; _stage0_manifest_check binds it
    # to the receipt rule recomputed from the pinned root bytes.
    if _stage0_status_neutral(alternatives) != registered:
        reasons.append('ROOT_ROSTERS_EXACT_ORDERED_SLOTS_ALTERNATIVES_REQUIRED: GL10 and all declared alternatives are fixed')
        return None
    decl = alternatives['declared']
    if not isinstance(decl, list) or not decl:
        reasons.append('alternatives.declared must be a non-empty list')
        return None
    names = []
    for i, a in enumerate(decl):
        where = 'alternatives.declared[%d]' % i
        if not isinstance(a, dict) or not {'name', 'kind', 'description', 'status'} <= set(a):
            reasons.append('%s lacks the required alternative fields' % where)
            continue
        # Additional metadata is allowed only because the complete exact record
        # was compared to the hard-pinned slots above (0548 STAGE0_GRID_OUTER).
        if not isinstance(a['name'], str) or not a['name']:
            reasons.append('%s.name must be a non-empty string' % where)
        if a['kind'] not in ALT_KINDS:
            reasons.append('%s.kind must be one of %s' % (where, list(ALT_KINDS)))
        if not isinstance(a['description'], str):
            reasons.append('%s.description must be a string' % where)
        if a['status'] not in (ALT_EVALUATED, ALT_NOT_EVALUATED):
            reasons.append('%s.status must be %s or %s' % (where, ALT_EVALUATED, ALT_NOT_EVALUATED))
        names.append(a['name'])
    if reasons:
        return None
    if len(set(names)) != len(names):
        reasons.append('alternative names are not unique')
        return None
    prim = alternatives['primary']
    pd = [a for a in decl if a['name'] == prim]
    if not pd:
        reasons.append('primary alternative %r is not declared' % (prim,))
        return None
    if pd[0]['status'] != ALT_EVALUATED:
        reasons.append('primary alternative %r must be EVALUATED_BEFORE_FREEZE' % (prim,))
        return None
    evaluated = [a['name'] for a in decl if a['status'] == ALT_EVALUATED]
    return {'primary': prim, 'declared': [dict(a) for a in decl], 'evaluated': evaluated,
            'non_primary_evaluated': [x for x in evaluated if x != prim]}


def _incomplete_reasons(admitted_region, member_eval, sensitivity, alt_results):
    r = []
    if admitted_region.get('exploration_status') != STATUS_COMPLETE:
        r.append('EXPLORATION_STATUS_%s' % admitted_region.get('exploration_status'))
    if member_eval.get('status') != STATUS_COMPLETE:
        r.append('PRIMARY_MEMBER_EVALUATION_%s' % member_eval.get('status'))
    if sensitivity.get('status') != STATUS_COMPLETE:
        r.append('SENSITIVITY_%s' % sensitivity.get('status'))
    for name in sorted(alt_results):
        st = alt_results[name].get('member_evaluation', {}).get('status')
        if st != STATUS_COMPLETE:
            r.append('ALTERNATIVE_%s_MEMBER_EVALUATION_%s' % (name, st))
    return r


def _conditional_on_trial(S, admitted_region, sensitivity):
    entries = sensitivity.get('evaluations') or []

    def evaluated(kind, target):
        es = [e for e in entries if e['kind'] == kind and e['target'] == target]
        return bool(es) and all(e['evaluated'] or e['skipped_zero_displacement'] for e in es)

    out = []
    for nm in S['fixed_shared']:
        c = S['by_name'][nm]
        out.append({'kind': SENS_FIXED, 'name': nm, 'trial_value': c['trial_value'], 'units': c['units'],
                    'sensitivity_declared': c['sensitivity'] is not None,
                    'sensitivity_evaluated': (c['sensitivity'] is not None and evaluated(SENS_FIXED, nm))})
    for nm in S['ngc_nuisance_names']:
        c = S['by_name'][nm]
        out.append({'kind': SENS_NGC, 'name': nm, 'trial_value': c['trial_value'], 'units': c['units'],
                    'reference_value': c['reference_value'], 'sensitivity_declared': True,
                    'sensitivity_evaluated': evaluated(SENS_NGC, nm)})
    for d in admitted_region['near_null_directions']:
        out.append({'kind': SENS_NULL, 'name': str(d['index']), 'trial_value': d['trial_projection'],
                    'units': 'dimensionless unit-box projection u.v', 'sensitivity_declared': True,
                    'sensitivity_evaluated': evaluated(SENS_NULL, str(d['index']))})
    for nm in S.get('ddo_fixed_names') or []:   # v003b (A13): the bands are conditional on the fixed DDO154 distance
        c = S['by_name'][nm]
        out.append({'kind': SENS_DDO_FIXED, 'name': nm, 'trial_value': c['trial_value'], 'units': c['units'],
                    'reference_value': c['reference_value'], 'sensitivity_declared': False,
                    'sensitivity_evaluated': False, 'status': FIXED_CONSTANT_STATUS,
                    'alternative': MODE_D_NUISANCE + ' NOT_EVALUATED_BEFORE_FREEZE', 'root_decision': 'A13'})
    return out


def _is_list_of(x, n, pred):
    return isinstance(x, list) and len(x) == n and all(pred(v) for v in x)


def _opt_real(v):
    return v is None or _is_real(v)


def _validate_members(members, S, ids, n_ident, where, reasons, adm_proj=None):
    if not isinstance(members, list) or not members:
        reasons.append('%s must be a non-empty list' % where)
        return False
    nq = len(ids)
    ok = True
    seen_ids, seen_log = set(), set()
    for i, m in enumerate(members):
        w = '%s[%d]' % (where, i)
        if not isinstance(m, dict) or set(m) != MEMBER_KEYS:
            reasons.append('%s keys differ from %s' % (w, sorted(MEMBER_KEYS)))
            ok = False
            continue
        if not isinstance(m['member_id'], str) or m['member_id'] in seen_ids:
            reasons.append('%s.member_id missing or duplicated' % w)
            ok = False
        seen_ids.add(m['member_id'])
        if not _is_int(m['log_index']) or m['log_index'] in seen_log:
            reasons.append('%s.log_index missing or duplicated' % w)
            ok = False
        seen_log.add(m['log_index'])
        if not isinstance(m['role'], str) or m['role'] not in ROLES or not _is_int(m['point_index']):
            reasons.append('%s role/point_index malformed' % w)
            ok = False
        if not _is_list_of(m['u'], len(S['varying_engine']), _is_real):
            reasons.append('%s.u malformed' % w)
            ok = False
        if not _is_list_of(m['identified_projection'], n_ident, _is_real):
            reasons.append('%s.identified_projection malformed' % w)
            ok = False
        elif adm_proj is not None and adm_proj.get(m['log_index']) != m['identified_projection']:
            reasons.append('%s is not an admitted point of admitted_region (log_index/projection mismatch)' % w)
            ok = False
        te, tn = m['theta_engine'], m['theta_ngc']
        if not isinstance(te, dict) or set(te) != set(S['engine_names']) or not all(_is_real(v) for v in te.values()):
            reasons.append('%s.theta_engine keys/values malformed' % w)
            ok = False
            continue
        if not isinstance(tn, dict) or set(tn) != set(S['ngc_theta_names']):
            reasons.append('%s.theta_ngc keys %s must be exactly shared + NGC3198 nuisance names %s (D10: no '
                           'DDO154 nuisance)' % (w, sorted(tn) if isinstance(tn, dict) else tn,
                                                 sorted(S['ngc_theta_names'])))
            ok = False
            continue
        if tn != _theta_ngc_from_engine(S, te):
            reasons.append('%s.theta_ngc is not the shared coordinates plus NGC3198 nuisances at trial' % w)
            ok = False
        if isinstance(m['u'], list) and len(m['u']) == len(S['varying_engine']) and all(_is_real(x) for x in m['u']):
            th = _theta_engine_from_u(S, m['u'])
            if any(not _close(th[nm], te[nm]) for nm in S['engine_names']):
                reasons.append('%s.theta_engine inconsistent with u' % w)
                ok = False
        if not isinstance(m['evaluated'], bool) or not isinstance(m['member_valid'], bool) or \
                not (m['forward_valid_flag'] is None or isinstance(m['forward_valid_flag'], bool)):
            reasons.append('%s evaluated/member_valid/forward_valid_flag malformed' % w)
            ok = False
            continue
        if not _is_list_of(m['row_valid'], nq, lambda v: isinstance(v, bool)) or \
                not _is_list_of(m['speeds_km_s'], nq, _opt_real):
            reasons.append('%s row_valid/speeds_km_s must be lists of %d' % (w, nq))
            ok = False
            continue
        if any(rv and s is None for rv, s in zip(m['row_valid'], m['speeds_km_s'])):
            reasons.append('%s has a valid row without a finite speed' % w)
            ok = False
        if not _registered_rows_ok(m,ids):
            reasons.append('%s registered row contract mismatch' % w)
            ok=False
        if not m['evaluated'] and (any(m['row_valid']) or any(v is not None for v in m['speeds_km_s']+m['row_registration'])):
            reasons.append('%s unevaluated member carries rows' % w)
            ok=False
        if m['member_valid'] != _member_contract_valid(m):
            reasons.append('%s.member_valid inconsistent with registered-valid rows' % w)
            ok=False
        if any(rv and m['forward_valid_flag'] is not True for rv in m['row_valid']):
            reasons.append('%s valid row while forward flag is not True' % w)
            ok = False
        if not isinstance(m['reasons'], list) or not all(isinstance(r, str) for r in m['reasons']) or \
                m['exception'] is not None and not isinstance(m['exception'], str):
            reasons.append('%s reasons/exception malformed' % w)
            ok = False
    return ok


def _validate_member_eval(me, members, where, reasons):
    if not isinstance(me, dict) or set(me) != MEMBER_EVAL_KEYS:
        reasons.append('%s keys differ from %s' % (where, sorted(MEMBER_EVAL_KEYS)))
        return
    n_eval = sum(1 for m in members if m['evaluated'])
    n_valid = sum(1 for m in members if m['member_valid'])
    if me['status'] not in (STATUS_COMPLETE, STATUS_BUDGET) or me['stage'] != 'ngc_members':
        reasons.append('%s status/stage malformed' % where)
    if me['n_selected'] != len(members) or me['n_evaluated'] != n_eval or me['n_member_valid'] != n_valid:
        reasons.append('%s counts inconsistent with the member arrays' % where)
    if (me['status'] == STATUS_COMPLETE) != (n_eval == len(members)):
        reasons.append('%s status inconsistent with evaluated members' % where)
    if not _is_int(me['budget']) or not _is_int(me['evaluations_used']) or me['evaluations_used'] != n_eval:
        reasons.append('%s budget/evaluations_used malformed' % where)


def _validate_envelope(env, members, ids, where, reasons, label=ENVELOPE_LABEL):
    if not isinstance(env, list) or len(env) != len(ids):
        reasons.append('%s must be a list of %d rows' % (where, len(ids)))
        return
    if env != _pointwise_envelope(members, ids, label):
        reasons.append('%s differs from the envelope recomputed from the member arrays' % where)


def _validate_admitted_region(ar, S, reasons, record_ident=None):
    if not isinstance(ar, dict) or set(ar) != ADMITTED_REGION_KEYS:
        reasons.append('admitted_region keys differ from %s' % sorted(ADMITTED_REGION_KEYS))
        return None
    n = len(S['varying_engine'])
    bad = []
    if ar['admitted_set_label'] != INNER_SAMPLE:
        bad.append('admitted_set_label must be INNER_SAMPLE')
    if not isinstance(ar['region_possibly_truncated'], bool) or not isinstance(ar['truncation_evidence'], list) \
            or ar['region_possibly_truncated'] != bool(ar['truncation_evidence']):
        bad.append('region_possibly_truncated must equal bool(truncation_evidence)')
    if (ar['exploration_status'] != STATUS_COMPLETE and
            'EXPLORATION_STATUS_%s' % ar['exploration_status'] not in (ar['truncation_evidence'] or [])):
        bad.append('incomplete exploration must appear in truncation_evidence')
    if ar['varying_engine_names'] != S['varying_engine']:
        bad.append('varying_engine_names differ from the coordinates')
    if ar['null_space_complete'] is not True:
        bad.append('null_space_complete must be True')
    ident, near = ar['identified'], ar['near_null']
    if not isinstance(ident, list) or not isinstance(near, list) or \
            sorted(list(ident) + list(near)) != list(range(n)) or not ident:
        bad.append('identified + near_null must partition 0..n-1 (D10)')
    rv = ar['right_vectors']
    if not isinstance(rv, list) or len(rv) != n or not all(_is_list_of(v, n, _is_real) for v in rv):
        bad.append('right_vectors must be a complete n x n basis (D10)')
    elif any(abs(_dot(rv[i], rv[j]) - (1.0 if i == j else 0.0)) > _ORTHO_TOL for i in range(n) for j in range(n)):
        bad.append('right_vectors are not orthonormal')
    if not isinstance(ident, list) or not _is_list_of(ar['centroid_identified'], len(ident), _is_real):
        bad.append('centroid_identified malformed')
    if not _is_int(ar['n_admitted']) or ar['n_admitted'] < 1:
        bad.append('n_admitted must be >= 1')
    ap = ar['admitted_projections_identified']
    if not isinstance(ap, list) or len(ap) != ar['n_admitted'] or not isinstance(ident, list) or any(
            not isinstance(p, dict) or set(p) != {'log_index', 'projection'} or not _is_int(p['log_index'])
            or not _is_list_of(p['projection'], len(ident), _is_real) for p in ap) or \
            len(set(p['log_index'] for p in ap)) != len(ap):
        bad.append('admitted_projections_identified must list every admitted point once (log_index, projection)')
    else:
        if ar['centroid_identified'] != _centroid(ap, len(ident)):
            bad.append('centroid_identified differs from the centroid recomputed from admitted projections')
        pr = {str(k): {'min': min(p['projection'][j] for p in ap), 'max': max(p['projection'][j] for p in ap)}
              for j, k in enumerate(ident)}
        if ar['projection_range_identified'] != pr:
            bad.append('projection_range_identified differs from the admitted projections')
        # D2: recompute the member selection from the frozen rule inputs
        ic, ali = ar['selection_interior_count'], ar['selection_anchor_log_index']
        if ar['selection_rule'] != SELECTION_RULE or not _is_int(ic) or ic < 0 or \
                not (ali is None or (_is_int(ali) and any(p['log_index'] == ali for p in ap))):
            bad.append('selection_rule / selection_interior_count / selection_anchor_log_index malformed (D2)')
        else:
            plan = _selection_plan([(p['log_index'], p['projection']) for p in ap], len(ident), ali, ic)
            if ar['selected_points'] != [{'log_index': li, 'role': role} for li, role in plan]:
                bad.append('selected_points differ from the selection recomputed from the frozen rule inputs (D2)')
    # P34-14 / P34-16 / D3: the region binding the admission was checked against
    if not _is_hex64(ar['observation_region_sha256']) or ar['admission_reverified'] is not True:
        bad.append('observation_region_sha256 must be the hash-verified DDO154 region and admission_reverified '
                   'True (pass the run_calibration_region output to select_representative_points)')
    if not _is_hex64(ar['calibration_fingerprint']):
        bad.append('calibration_fingerprint missing (P34-16)')
    nnd = ar['near_null_directions']
    if not isinstance(nnd, list) or not isinstance(near, list) or \
            [d.get('index') if isinstance(d, dict) else None for d in nnd] != list(near):
        bad.append('near_null_directions must list every near-null index in order')
    elif isinstance(rv, list) and len(rv) == n:
        for d in nnd:
            if d.get('vector_u') != rv[d['index']] or not _opt_real(d.get('ddo_sensitivity_sigma_per_unit_t')) \
                    or not _is_real(d.get('trial_projection')):
                bad.append('near_null_directions[%r] inconsistent' % d.get('index'))
    if ar['bounds_semantics'] != BOUNDS_SEMANTICS or ar['unit_coordinate_units'] != U_UNITS:
        bad.append('bounds_semantics/unit_coordinate_units text differs')
    # v003d (SF-1 fix 3): IDENTIFICATION_RULE re-applied to the frozen singular values; with the pinned record's
    # identifiability report (writer and verifier) re-applied exactly, and S^T S diagonalised by the frozen basis
    if not bad:
        bad.extend(_identification_rule_reasons(ar, n))
    if not bad and record_ident is not None:
        bad.extend(_record_identifiability_reasons(ar, n, record_ident))
    for b in bad:
        reasons.append('admitted_region: ' + b)
    return None if bad else ar


def _identification_rule_reasons(ar, n):
    """v003d (SF-1 fix 3): necessary form of IDENTIFICATION_RULE on the frozen singular values alone (the effective
    tolerance is not frozen in admitted_region; the exact form needs the record, _record_identifiability_reasons).
    identified iff (s > 0 and s >= eff * s_max) or s >= z with eff >= MIN_NULL_TOLERANCE, hence: every identified s
    is > 0 and (>= z or >= MIN_NULL_TOLERANCE * s_max); every near-null s is < z; and the identified set is an upper
    set of the singular values (every near-null s < every identified s)."""
    ident, near, sv = ar['identified'], ar['near_null'], ar['singular_values']
    if not _is_list_of(sv, n, _is_real) or any(float(x) < 0.0 for x in sv):
        return ['singular_values must be %d finite non-negative reals (IDENTIFICATION_RULE is re-applied to them, '
                'SF-1 fix 3); got %s' % (n, _safe_repr(sv)[:80])]
    s = [float(x) for x in sv]
    smax = s[0] if n else 0.0
    if any(s[i + 1] - s[i] > _ORTHO_TOL * max(1.0, smax) for i in range(n - 1)):
        return ['singular_values must be non-increasing (SF-1 fix 3)']
    out = []
    z = ABSOLUTE_IDENTIFICATION_THRESHOLD
    for k in ident:
        if not (s[k] > 0.0 and (s[k] >= z or s[k] >= MIN_NULL_TOLERANCE * smax)):
            out.append('identified direction %d (s = %r, s_max = %r) is not identified under IDENTIFICATION_RULE for '
                       'any effective tolerance >= MIN_NULL_TOLERANCE %r (SF-1 fix 3)' % (k, s[k], smax,
                                                                                         MIN_NULL_TOLERANCE))
    for k in near:
        if s[k] >= z:
            out.append('near-null direction %d has s = %r >= z = %r: IDENTIFICATION_RULE identifies it (SF-1 fix 3)'
                       % (k, s[k], z))
    if ident and near and max(s[k] for k in near) >= min(s[k] for k in ident):
        out.append('the identified set is not an upper set of the singular values (a near-null s %r >= an identified '
                   's %r): no effective tolerance gives this partition (SF-1 fix 3)'
                   % (max(s[k] for k in near), min(s[k] for k in ident)))
    return out


def _record_identifiability_reasons(ar, n, ident):
    """v003d (SF-1 fix 3): the pinned record's identifiability report re-checked from its own content, and the frozen
    basis bound to it. Pure Python (no numpy): the record's effective tolerance follows the engine formula; its
    partition follows IDENTIFICATION_RULE from its singular values; its right vectors are orthonormal and diagonalise
    the recorded S^T S (S = scaled_jacobian); the frozen right_vectors / singular_values / identified / near_null
    equal the record's."""
    if not isinstance(ident, dict):
        return ['the pinned calibration record carries no identifiability report (SF-1 fix 3)']
    Sm, V, s = ident.get('scaled_jacobian'), ident.get('right_vectors'), ident.get('singular_values')
    if not isinstance(Sm, list) or not Sm or not all(_is_list_of(r, n, _is_real) for r in Sm) or \
            not _is_list_of(V, n, lambda v: _is_list_of(v, n, _is_real)) or not _is_list_of(s, n, _is_real):
        return ['the pinned record identifiability arrays are malformed (scaled_jacobian m x %d, right_vectors and '
                'singular_values of %d) (SF-1 fix 3)' % (n, n)]
    m = len(Sm)
    Sm = [[float(x) for x in r] for r in Sm]
    V = [[float(x) for x in v] for v in V]
    s = [float(x) for x in s]
    out = []
    tol, eff, floor = ident.get('null_tolerance'), ident.get('effective_null_tolerance'), \
        ident.get('numerical_rank_floor')
    exp_floor = float(max(m, n) * _FLOAT_EPS)
    if not (_is_real(tol) and _is_real(eff) and _is_real(floor)) or float(floor) != exp_floor or \
            float(eff) != max(float(tol), MIN_NULL_TOLERANCE, exp_floor):
        out.append('the pinned record effective_null_tolerance %r is not max(null_tolerance %r, MIN_NULL_TOLERANCE '
                   '%r, max(m, n) * eps %r) (SF-1 fix 3)' % (eff, tol, MIN_NULL_TOLERANCE, exp_floor))
        return out
    eff = float(eff)
    smax = s[0]
    z = ABSOLUTE_IDENTIFICATION_THRESHOLD
    expect = [k for k in range(n) if (smax > 0.0 and s[k] > 0.0 and s[k] >= eff * smax) or s[k] >= z]
    rid, rnn = ident.get('identified'), ident.get('near_null')
    if not isinstance(rid, list) or not isinstance(rnn, list) or not all(_is_int(k) for k in rid + rnn) or \
            sorted(int(k) for k in rid) != expect or sorted(int(k) for k in rnn) != \
            [k for k in range(n) if k not in expect]:
        out.append('the pinned record identified %s / near_null %s do not follow IDENTIFICATION_RULE from its '
                   'singular values (expected identified %s) (SF-1 fix 3)' % (_safe_repr(rid)[:60],
                                                                              _safe_repr(rnn)[:60], expect))
        return out
    for i in range(n):
        for j in range(i, n):
            if abs(_dot(V[i], V[j]) - (1.0 if i == j else 0.0)) > _ORTHO_TOL:
                out.append('the pinned record right_vectors are not orthonormal (<v%d, v%d>) (SF-1 fix 3)' % (i, j))
                return out
    SV = [[math.fsum(Sm[r][c] * V[k][c] for c in range(n)) for r in range(m)] for k in range(n)]
    scale = _ORTHO_TOL * max(1.0, smax * smax)
    for k in range(n):
        for l_ in range(k, n):
            g = math.fsum(a * b for a, b in zip(SV[k], SV[l_])) - (s[k] * s[k] if k == l_ else 0.0)
            if abs(g) > scale:
                out.append('the pinned record right_vectors do not diagonalise the recorded S^T S (<S v%d, S v%d> - '
                           'delta s^2 = %r) (SF-1 fix 3)' % (k, l_, g))
                return out
    if [[float(x) for x in v] for v in ar['right_vectors']] != V or [float(x) for x in ar['singular_values']] != s \
            or list(ar['identified']) != expect or list(ar['near_null']) != [k for k in range(n) if k not in expect]:
        out.append('the frozen right_vectors / singular_values / identified / near_null differ from the pinned '
                   'record\'s identifiability report (SF-1 fix 3)')
    return out


def _validate_reference(ref, members, centroid, reasons):
    if not isinstance(ref, dict) or set(ref) != REFERENCE_KEYS:
        reasons.append('reference_member keys differ from %s' % sorted(REFERENCE_KEYS))
        return None
    if ref['rule'] != REFERENCE_RULE:
        reasons.append('reference_member.rule text differs from the frozen rule')
    ranking = _reference_ranking(members, centroid)
    if ref['centroid_identified'] != centroid:
        reasons.append('reference_member.centroid_identified differs from admitted_region')
    if not ranking:
        reasons.append('reference_member: no valid member exists')
        return None
    if ref['ranking'] != ranking or ref['member_id'] != ranking[0]['member_id'] or \
            ref['log_index'] != ranking[0]['log_index'] or ref['distance'] != ranking[0]['distance']:
        reasons.append('reference_member does not follow REFERENCE_RULE (recomputed %s)' % ranking[0])
        return None
    return next(m for m in members if m['member_id'] == ref['member_id'])


def _validate_sensitivity(sens, ref_member, S, ar, ids, reasons):
    if not isinstance(sens, dict) or set(sens) != SENS_KEYS:
        reasons.append('sensitivity keys differ from %s' % sorted(SENS_KEYS))
        return
    bad = []
    sens_label = _mode_labels(S)[1]
    if sens['label'] != sens_label or sens['stage'] != 'ngc_sensitivity':
        bad.append('label/stage text differs')
    if ref_member is None or sens['reference_member_id'] != ref_member['member_id']:
        bad.append('reference_member_id differs from the frozen reference member')
    rule_reasons = []
    rule = _bind_null_rule(sens['null_direction_rule'], rule_reasons)
    if rule is None or rule != sens['null_direction_rule']:
        bad.append('null_direction_rule malformed')
    entries = sens['evaluations']
    if not isinstance(entries, list) or any(not isinstance(e, dict) or set(e) != SENS_ENTRY_KEYS for e in entries):
        bad.append('evaluations entries malformed')
    if bad or ref_member is None:
        for b in bad:
            reasons.append('sensitivity: ' + b)
        return
    plan = _sensitivity_plan(S, ref_member, ar['near_null_directions'], rule)
    plan_keys = ['entry_id', 'kind', 'target', 'side', 'displacement', 'displacement_units', 'limited_by',
                 'u_displaced', 'theta_ngc', 'skipped_zero_displacement', 'linearised_ddo_shift_sigma']
    if len(plan) != len(entries) or any(p[k] != e[k] for p, e in zip(plan, entries) for k in plan_keys):
        bad.append('evaluations do not match the planned displacements recomputed from the reference member '
                   '(every near-null direction and declared coordinate, both sides)')
    nq = len(ids)
    for e in entries:
        if not _is_list_of(e['row_valid'], nq, lambda v: isinstance(v, bool)) or \
                not _is_list_of(e['speeds_km_s'], nq, _opt_real) or \
                not _is_list_of(e['delta_from_reference_km_s'], nq, _opt_real) or \
                not isinstance(e['evaluated'], bool):
            bad.append('entry %s arrays malformed' % e.get('entry_id'))
            continue
        if not e['evaluated'] and (any(e['row_valid']) or any(s is not None for s in e['speeds_km_s'])):
            bad.append('entry %s unevaluated but carries rows' % e['entry_id'])
        if not _registered_rows_ok(e,ids):
            bad.append('entry %s registered row contract mismatch' % e['entry_id'])
        if e['skipped_zero_displacement'] and e['evaluated']:
            bad.append('entry %s skipped but evaluated' % e['entry_id'])
        if any(rv and s is None for rv, s in zip(e['row_valid'], e['speeds_km_s'])):
            bad.append('entry %s valid row without a speed' % e['entry_id'])
        exp_delta = [(float(s - r) if (rv and ok) else None) for s, r, rv, ok in
                     zip(e['speeds_km_s'], ref_member['speeds_km_s'], ref_member['row_valid'], e['row_valid'])]
        if e['evaluated'] and e['delta_from_reference_km_s'] != exp_delta:
            bad.append('entry %s delta_from_reference inconsistent' % e['entry_id'])
    if bad:
        for b in bad:
            reasons.append('sensitivity: ' + b)
        return
    pending = [e for e in entries if not e['skipped_zero_displacement'] and not e['evaluated']]
    if (sens['status'] == STATUS_COMPLETE) != (not pending) or sens['status'] not in (STATUS_COMPLETE, STATUS_BUDGET):
        reasons.append('sensitivity: status inconsistent with pending evaluations')
    if not _is_int(sens['evaluations_used']) or sens['evaluations_used'] != sum(1 for e in entries if e['evaluated']):
        reasons.append('sensitivity: evaluations_used inconsistent')
    pq, pt = _sensitivity_summary(ref_member, entries, ids, sens_label)
    if sens['per_query'] != pq or sens['per_target'] != pt:
        reasons.append('sensitivity: per_query/per_target differ from the values recomputed from evaluations')


def _check_slot_geometry(S, sens, notes, reasons):
    """v003b, root rulings A16.1 / A16.4 (writer and verifier share it).

    Applies when notes carries the A16.1 slot block notes.ngc3198_slot_sensitivity (slots V003 notes_block_for_manifest
    layout); in coordinate mode DDO154_DISTANCE_FIXED_AT_REGISTERED the block is required. Checks:
      * the block: status NOT_EVALUATED_BEFORE_FREEZE, applies_to = the NGC3198 slot names, declared_range = the
        slots' [lower, upper] and trial values (units included), headline_geometry = the slots' trial values (the
        registered geometry: distance 13.8 Mpc; inclination = its reference_value when one is declared), a non-empty
        manifest_reading_note;
      * A16.4: every EVALUATED NGC3198 slot sensitivity entry is a refusal (forward flag not True, no valid row) whose
        reasons carry GEOMETRY_NOT_EXPOSED. A valid box-end result refuses (it would freeze a false zero sensitivity).
    Appends reasons on any violation and returns None; otherwise returns the summary written into headline_conditions
    in the fixed-distance mode. Returns None (no reason) when the block is absent outside that mode: v003a behaviour."""
    block = notes.get(NOTES_SLOT_KEY) if isinstance(notes, dict) else None
    if block is None:
        if S.get('coordinate_mode') == MODE_D_FIXED:
            reasons.append('REFUSED (A16.1): coordinate mode %s requires notes.%s (the slot block of the adopted NGC3198 '
                           'freeze inputs: registered-geometry headline, box sensitivity NOT_EVALUATED_BEFORE_FREEZE)'
                           % (MODE_D_FIXED, NOTES_SLOT_KEY))
        return None
    n0 = len(reasons)
    ngc = list(S['ngc_nuisance_names'])
    if not isinstance(block, dict):
        reasons.append('REFUSED (A16.1): notes.%s must be an object' % NOTES_SLOT_KEY)
        return None
    if block.get('status') != ALT_NOT_EVALUATED:
        reasons.append('REFUSED (A16.1): notes.%s.status must be %s' % (NOTES_SLOT_KEY, ALT_NOT_EVALUATED))
    at = block.get('applies_to')
    if not isinstance(at, list) or not all(isinstance(x, str) for x in at) or len(set(at)) != len(at) or \
            set(at) != set(ngc):
        reasons.append('REFUSED (A16.1): notes.%s.applies_to must list exactly the NGC3198 slots %s'
                       % (NOTES_SLOT_KEY, ngc))
    dr = block.get('declared_range')
    if not isinstance(dr, dict) or set(_safe_str(k) for k in dr) != set(ngc):
        reasons.append('REFUSED (A16.1): notes.%s.declared_range must cover exactly the NGC3198 slots %s'
                       % (NOTES_SLOT_KEY, ngc))
    else:
        for nm in ngc:
            c, e = S['by_name'][nm], dr.get(nm)
            if not isinstance(e, dict) or any(not _is_real(e.get(f)) or float(e.get(f)) != c[f]
                                              for f in ('lower', 'upper', 'trial_value')) or e.get('units') != c['units']:
                reasons.append('REFUSED (A16.1): notes.%s.declared_range[%r] differs from the slot box [%r, %r], trial '
                               '%r %s' % (NOTES_SLOT_KEY, nm, c['lower'], c['upper'], c['trial_value'], c['units']))
    by_kind = {S['by_name'][nm]['kind']: S['by_name'][nm] for nm in ngc}
    hg = block.get('headline_geometry')
    cd, ci = by_kind.get('distance'), by_kind.get('inclination')
    if not isinstance(hg, dict) or cd is None or ci is None or \
            not _is_real(hg.get('distance_Mpc')) or float(hg['distance_Mpc']) != cd['trial_value'] or \
            cd['trial_value'] != DISTANCE_REFERENCE_MPC[SCOPE_NGC] or \
            not _is_real(hg.get('physical_inclination_deg')) or float(hg['physical_inclination_deg']) != ci['trial_value'] \
            or (ci['reference_value'] is not None and ci['trial_value'] != ci['reference_value']):
        reasons.append('REFUSED (A16.1): notes.%s.headline_geometry must equal the slots\' trial values, the registered '
                       'geometry (distance %r Mpc; inclination at its reference_value when declared)'
                       % (NOTES_SLOT_KEY, DISTANCE_REFERENCE_MPC[SCOPE_NGC]))
    rn = block.get('manifest_reading_note')
    if not isinstance(rn, str) or not rn.strip():
        reasons.append('REFUSED (A16.4): notes.%s.manifest_reading_note must explain the invalid-by-design box rows'
                       % NOTES_SLOT_KEY)
    if len(reasons) > n0:
        return None
    entries = sens.get('evaluations') if isinstance(sens, dict) else None
    if not isinstance(entries, list):
        reasons.append('REFUSED (A16.4): sensitivity evaluations missing')
        return None
    box, refused, unevaluated, skipped = [], 0, 0, 0
    for e in entries:
        if not isinstance(e, dict) or e.get('kind') != SENS_NGC:
            continue
        box.append(e.get('entry_id'))
        if e.get('skipped_zero_displacement') is True:
            skipped += 1
            continue
        if e.get('evaluated') is not True:
            unevaluated += 1
            continue
        rv, rr = e.get('row_valid'), e.get('reasons')
        valid_any = e.get('forward_valid_flag') is True or (isinstance(rv, list) and any(x is True for x in rv))
        geo = isinstance(rr, list) and any(isinstance(r, str) and GEOMETRY_NOT_EXPOSED in r for r in rr)
        if valid_any or not geo:
            reasons.append('REFUSED (A16.4): NGC3198 slot sensitivity entry %s (%s %s) %s; forward_ngc must return '
                           'valid=false with reason %s for any geometry other than the registered one (a silently '
                           'ignored D or i would freeze a false zero sensitivity)'
                           % (_safe_repr(e.get('entry_id')), _safe_repr(e.get('target')), _safe_repr(e.get('side')),
                              'returned a valid evaluation' if valid_any else 'was refused without that reason',
                              GEOMETRY_NOT_EXPOSED))
        else:
            refused += 1
    if len(reasons) > n0:
        return None
    pq = sens.get('per_query') if isinstance(sens.get('per_query'), list) else []
    return {'status': ALT_NOT_EVALUATED, 'root_rulings': dict(ROOT_A16, ids=list(ROOT_A16['ids'])),
            'headline_geometry': {nm: S['by_name'][nm]['trial_value'] for nm in ngc},
            'declared_range': {nm: [S['by_name'][nm]['lower'], S['by_name'][nm]['upper']] for nm in ngc},
            'box_end_entries': box, 'n_refused_geometry_not_exposed': refused, 'n_not_evaluated': unevaluated,
            'n_skipped_zero_displacement': skipped,
            'box_limited_band_rows_invalid': sum(1 for r in pq if not (isinstance(r, dict) and r.get('valid') is True)),
            'box_limited_band_rows_total': len(pq), 'reading': A16_READING}


def _headline_conditions(S, alts, a16, notes, reasons):
    """v003b (A13): the module-generated headline_conditions block of the fixed-distance mode (writer and verifier).

    Requires notes.structural_assumptions with SA-BH-01 and SA-REACH-01 (non-empty text_verbatim; A10, A12.2) and an
    entry whose section is A18 (non-empty text_verbatim; A18), refuses a declared alternative DDO154_DISTANCE_NUISANCE
    marked EVALUATED_BEFORE_FREEZE, and needs the A16 summary (a16, from _check_slot_geometry). Appends reasons and
    returns None on any violation."""
    if S.get('coordinate_mode') != MODE_D_FIXED:
        return None
    n0 = len(reasons)
    for a in alts['declared']:
        if a['name'] == MODE_D_NUISANCE and a['status'] == ALT_EVALUATED:
            reasons.append('REFUSED (A13): alternative %s is declared %s; under A13 distance as a nuisance is '
                           'NOT_EVALUATED_BEFORE_FREEZE' % (MODE_D_NUISANCE, ALT_EVALUATED))
    sa = notes.get(NOTES_SA_KEY) if isinstance(notes, dict) else None
    a18 = []
    if not isinstance(sa, dict):
        reasons.append('REFUSED (A10/A12/A18): coordinate mode %s requires notes.%s (SA-BH-01, SA-REACH-01, an A18 '
                       'entry)' % (MODE_D_FIXED, NOTES_SA_KEY))
    else:
        for k in SA_REQUIRED:
            e = sa.get(k)
            if not isinstance(e, dict) or not isinstance(e.get('text_verbatim'), str) or not e['text_verbatim'].strip():
                reasons.append('REFUSED (A10/A12): notes.%s.%s must carry a non-empty text_verbatim' % (NOTES_SA_KEY, k))
        a18 = sorted(k for k, e in sa.items() if isinstance(k, str) and k not in SA_REQUIRED and isinstance(e, dict)
                     and e.get('section') == SA_SECTION_A18 and isinstance(e.get('text_verbatim'), str)
                     and e['text_verbatim'].strip())
        if not a18:
            reasons.append('REFUSED (A18): notes.%s must carry an entry with section %s and a non-empty text_verbatim '
                           '(the A2 in-plane anisotropy limitation, next to SA-REACH-01)' % (NOTES_SA_KEY, SA_SECTION_A18))
    if a16 is None and len(reasons) == n0:
        reasons.append('REFUSED (A16.1): the NGC3198 slot block did not validate')
    if len(reasons) > n0:
        return None
    fixed = []
    for nm in S['ddo_fixed_names']:
        c = S['by_name'][nm]
        fixed.append({'name': nm, 'value': c['trial_value'], 'units': c['units'], 'scope': c['scope'],
                      'role': c['role'], 'kind': c['kind'], 'reference_value': c['reference_value'],
                      'status': FIXED_CONSTANT_STATUS, 'computational_box': [c['lower'], c['upper']],
                      'box_use': 'kept only for the engine binding to region.distance_summary; never sampled'})
    return {'coordinate_mode': MODE_D_FIXED, 'root_decision': dict(ROOT_A13),
            'free_engine_coordinates': list(S['varying_engine']), 'fixed_counted_constants': fixed,
            'band_condition': A13_CONDITION,
            'labelled': ['band_scope (every entry)', 'pointwise_envelope rows',
                         'alternative_results.*.pointwise_envelope rows', 'sensitivity.label',
                         'sensitivity.per_query rows', 'conditional_on_trial_values (' + SENS_DDO_FIXED + ')'],
            'admissibility': A13_ADMISSIBILITY, 'recorded_alternatives': [dict(DISTANCE_ALTERNATIVE)],
            'ngc3198_slot_box_sensitivity': a16, 'structural_assumptions_present': list(SA_REQUIRED) + a18}


def _validate_manifest_structure(doc, reasons):
    """Full structural + internal-consistency check (writer and verifier share it). Fails closed."""
    try:
        _validate_manifest_impl(doc, reasons)
        if not reasons:
            _root_manifest_check(doc)
        if not reasons:
            _stage0_manifest_check(doc, reasons)   # STAGE0 successor (M-14)
    except Exception as exc:   # S10: any malformed content fails closed
        reasons.append('manifest structure malformed: %s: %s' % (type(exc).__name__, _safe_str(exc)))


def _validate_manifest_impl(doc, reasons):
    if not isinstance(doc, dict):
        reasons.append('manifest is not a JSON object')
        return
    keys = set(doc)
    # v003b: headline_conditions is present exactly in the A13 fixed-distance mode (checked once S is built)
    missing, extra = MANIFEST_KEYS - keys, keys - MANIFEST_KEYS - {HEADLINE_CONDITIONS_KEY}
    if missing:
        reasons.append('manifest missing keys %s' % sorted(missing))
    if extra:
        reasons.append('manifest has unexpected keys %s' % sorted(extra))
    if missing:
        return
    for k, v in (('schema', SCHEMA), ('units', UNITS), ('semantics', SEMANTICS),
                 ('within_error_rule', WITHIN_ERROR_RULE), ('headline_rule', HEADLINE_RULE),
                 ('band_scope', BAND_SCOPE)):
        if doc[k] != v and not (k == 'band_scope' and doc[k] == BAND_SCOPE_A13):   # v003b: mode checked below
            reasons.append('%s differs from the frozen value' % k)
    if doc['target_velocities_included'] is not False:
        reasons.append('target_velocities_included is not False')
    if not isinstance(doc['created_utc'], str) or not doc['created_utc']:
        reasons.append('created_utc is not a string')
    if not isinstance(doc['parameter_region'], dict) or not doc['parameter_region'] or \
            doc['parameter_region'].get('bounds_semantics') != BOUNDS_SEMANTICS:
        reasons.append('parameter_region must be a non-empty object carrying bounds_semantics = %s (S11)'
                       % BOUNDS_SEMANTICS)
    if doc['module'] != MODULE_NAME:
        reasons.append('module differs from %s' % MODULE_NAME)
    if not isinstance(doc['observation_rule'], (dict, list, str)):
        reasons.append('observation_rule is not an object, list or string')
    if not _is_hex64(doc['manifest_sha256']) or doc['manifest_sha256'] != doc['manifest_sha256'].lower():
        reasons.append('manifest_sha256 is not a lowercase 64-character hex string')
    ids = _check_query_ids(doc['query_ids'], reasons, True)
    if ids is None or len(ids) != N_QUERIES:
        return
    sreasons = []
    S = _build_spec(doc['coordinates'], sreasons)
    if S is None:
        reasons.extend('coordinates: ' + r for r in sreasons)
        return
    if doc['coordinates'] != S['coordinates']:
        reasons.append('coordinates are not in normalised form')
    # v003b (A13): labels, band_scope and headline_conditions follow the coordinate mode of the frozen coordinates
    env_label, _sens_label, band_scope = _mode_labels(S)
    if doc['band_scope'] != band_scope and doc['band_scope'] in (BAND_SCOPE, BAND_SCOPE_A13):
        reasons.append('band_scope differs from the frozen value of coordinate mode %s' % S['coordinate_mode'])
    if (HEADLINE_CONDITIONS_KEY in doc) != (S['coordinate_mode'] == MODE_D_FIXED):
        reasons.append('%s must be present exactly in coordinate mode %s (here: coordinate mode %s, key present %s)'
                       % (HEADLINE_CONDITIONS_KEY, MODE_D_FIXED, S['coordinate_mode'], HEADLINE_CONDITIONS_KEY in doc))
        return
    ar = _validate_admitted_region(doc['admitted_region'], S, reasons)
    if ar is None:
        return
    areasons = []
    alts = _bind_alternatives(doc['alternatives'], areasons)
    if alts is None:
        reasons.extend('alternatives: ' + r for r in areasons)
        return
    n_ident = len(ar['identified'])
    members = doc['members']
    adm = {p['log_index']: p['projection'] for p in ar['admitted_projections_identified']}
    if not _validate_members(members, S, ids, n_ident, 'members', reasons, adm):
        return
    if _member_order(members) != ar['selected_points']:
        reasons.append('members (log_index, role, order) differ from admitted_region.selected_points (D2: every '
                       'selected representative, and only those, is a member)')
        return
    _validate_member_eval(doc['member_evaluation'], members, 'member_evaluation', reasons)
    _validate_envelope(doc['pointwise_envelope'], members, ids, 'pointwise_envelope', reasons, env_label)
    ref_member = _validate_reference(doc['reference_member'], members, ar['centroid_identified'], reasons)
    _validate_sensitivity(doc['sensitivity'], ref_member, S, ar, ids, reasons)
    altres = doc['alternative_results']
    if not isinstance(altres, dict) or set(altres) != set(alts['non_primary_evaluated']):
        reasons.append('alternative_results keys must be exactly the non-primary EVALUATED_BEFORE_FREEZE '
                       'alternatives %s' % alts['non_primary_evaluated'])
    else:
        for name in sorted(altres):
            a = altres[name]
            w = 'alternative_results[%r]' % name
            if not isinstance(a, dict) or set(a) != {'members', 'member_evaluation', 'pointwise_envelope'}:
                reasons.append('%s must have members, member_evaluation, pointwise_envelope' % w)
                continue
            if _validate_members(a['members'], S, ids, n_ident, w + '.members', reasons, adm):
                if _member_order(a['members']) != ar['selected_points']:
                    reasons.append('%s.members differ from admitted_region.selected_points (D2)' % w)
                _validate_member_eval(a['member_evaluation'], a['members'], w + '.member_evaluation', reasons)
                _validate_envelope(a['pointwise_envelope'], a['members'], ids, w + '.pointwise_envelope', reasons,
                                   env_label)
    if reasons:
        return
    expect = _incomplete_reasons(ar, doc['member_evaluation'], doc['sensitivity'], altres)
    if doc['incomplete_reasons'] != expect:
        reasons.append('incomplete_reasons %r differ from recomputed %r' % (doc['incomplete_reasons'], expect))
    if doc['freeze_status'] != (FREEZE_INCOMPLETE if expect else FREEZE_COMPLETE):
        reasons.append('freeze_status %r inconsistent with incomplete_reasons' % (doc['freeze_status'],))
    if doc['conditional_on_trial_values'] != _conditional_on_trial(S, ar, doc['sensitivity']):
        reasons.append('conditional_on_trial_values differs from the recomputed list')
    # v003b: A16.1/A16.4 slot geometry (any mode, when declared in the notes) and the A13 headline conditions
    a16 = _check_slot_geometry(S, doc['sensitivity'], doc['notes'], reasons)
    if S['coordinate_mode'] == MODE_D_FIXED:
        hc = _headline_conditions(S, alts, a16, doc['notes'], reasons)
        if hc is not None and doc[HEADLINE_CONDITIONS_KEY] != hc:
            reasons.append('headline_conditions differ from the block recomputed from the coordinates, the '
                           'sensitivity and the notes (A13/A16)')
    pins = doc['pins']
    if not isinstance(pins, dict) or set(pins) != {'code_files', 'input_files'}:
        reasons.append('pins must be an object with exactly code_files and input_files')
    else:
        allp = []
        for label in ('code_files', 'input_files'):
            lst = pins[label]
            if not isinstance(lst, list) or not lst:
                reasons.append('pins.%s must be a NON-EMPTY list (A4: vacuous pins refused)' % label)
                continue
            for i, pin in enumerate(lst):
                if not isinstance(pin, dict) or set(pin) != PIN_KEYS:
                    reasons.append('pins.%s[%d] must have exactly path, sha256, bytes' % (label, i))
                    continue
                if not isinstance(pin['path'], str) or not os.path.isabs(pin['path']):
                    reasons.append('pins.%s[%d].path is not an absolute path' % (label, i))
                if not _is_hex64(pin['sha256']) or pin['sha256'] != pin['sha256'].lower():
                    reasons.append('pins.%s[%d].sha256 is not lowercase 64-hex' % (label, i))
                if not _is_int(pin['bytes']) or pin['bytes'] < 1:
                    reasons.append('pins.%s[%d].bytes must be >= 1 (zero-length pins refused)' % (label, i))
                allp.append(pin['path'])
        if len(set(allp)) != len(allp):
            reasons.append('pins contain duplicate paths')
        if not reasons:
            _validate_input_bindings(doc['input_bindings'], ar, ids, pins, reasons)
    hits = []
    _safe_scan(doc, 'manifest', hits, reasons)
    if hits:
        reasons.append('forbidden target field name(s) present: %s' % hits)


def _query_ids_sha256(ids):
    return _sha256_hex(_canonical_bytes(list(ids)))


def _validate_input_bindings(ib, ar, ids, pins, reasons):
    """D3/S12 + P34-14/P34-16: the query manifest and the DDO154 region are bound and pinned in input_files;
    a calibration record is bound (mandatory in v003a), pinned and carries the exploration fingerprint (no I/O
    here; the record content is re-checked from its bytes by _check_calibration_record)."""
    if not isinstance(ib, dict) or set(ib) != INPUT_BINDING_KEYS:
        reasons.append('input_bindings keys differ from %s' % sorted(INPUT_BINDING_KEYS))
        return
    inputs = {(p['path'], p['sha256']) for p in pins['input_files']}
    qm = ib['query_manifest']
    if not isinstance(qm, dict) or set(qm) != QM_BINDING_KEYS:
        reasons.append('input_bindings.query_manifest keys differ from %s' % sorted(QM_BINDING_KEYS))
    else:
        if qm['role'] not in QUERY_MANIFEST_ROLES or not _is_hex64(qm['sha256']) or \
                qm['program_pin_sha256'] != PROGRAM_QUERY_MANIFEST_SHA256 or \
                qm['is_program_pin'] is not (qm['sha256'] == PROGRAM_QUERY_MANIFEST_SHA256) or \
                (qm['role'] == QM_ROLE_PROGRAM) is not qm['is_program_pin']:
            reasons.append('input_bindings.query_manifest role/sha inconsistent (PROGRAM_PIN iff sha256 == %s)'
                           % PROGRAM_QUERY_MANIFEST_SHA256)
        if qm['query_ids_sha256'] != _query_ids_sha256(ids):
            reasons.append('query_ids are not the ids bound from the pinned query manifest (D3/S12)')
        if (qm['path'], qm['sha256']) not in inputs:
            reasons.append('the bound query manifest is not pinned in input_files (D3/A4)')
    reg = ib['observation_region']
    if not isinstance(reg, dict) or set(reg) != {'sha256'} or reg['sha256'] != ar['observation_region_sha256']:
        reasons.append('input_bindings.observation_region must be {sha256} equal to admitted_region.'
                       'observation_region_sha256')
    elif not any(sha == reg['sha256'] for _p, sha in inputs):
        reasons.append('the DDO154 observation-region file (sha %s) is not pinned in input_files'
                       % reg['sha256'])
    cr = ib['calibration_record']
    # X1 (v003a): the calibration record binding is mandatory
    if not isinstance(cr, dict) or set(cr) != {'path', 'sha256', 'exploration_fingerprint'} or \
            not _is_hex64(cr['exploration_fingerprint']) or \
            cr['exploration_fingerprint'] != ar['calibration_fingerprint'] or \
            (cr['path'], cr['sha256']) not in inputs:
        reasons.append('input_bindings.calibration_record is mandatory (X1) and must be a pinned input whose '
                       'exploration_fingerprint equals admitted_region.calibration_fingerprint (P34-16)')


def _check_calibration_record(cdoc, expected_fp, region_sha, region_path, members, reasons):
    """X1 (v003a): content check of the pinned calibration record and re-classification of every member.

    cdoc: the parsed record; expected_fp: the selection's exploration fingerprint (recomputed from the run's
    admitted points by select_representative_points); region_sha / region_path: the pinned DDO154 region file;
    members: [(log_index, u)] of every member.
      1. schema and self-hash (record_sha256 over the canonical body);
      2. the exploration fingerprint is RECOMPUTED from the recorded run content (run.exploration.admitted_points,
         run.region.sha256); it must equal the record's stored exploration_fingerprint and expected_fp;
      3. the admission rectangles are re-derived from the pinned region file BYTES (sha verified);
      4. every admitted point of the record -- hence every member -- is re-classified against those rectangles
         from its recorded DDO154 prediction, and every member (log_index, u) must be a recorded admitted point.
    Appends reasons; returns True when all hold. Never reads the rectangles of any dict."""
    n0 = len(reasons)
    if not isinstance(cdoc, dict) or cdoc.get('schema') != CALIBRATION_RECORD_SCHEMA or \
            not isinstance(cdoc.get('record_sha256'), str):
        reasons.append('REFUSED (P34-16): the pinned calibration record is not a %s document'
                       % CALIBRATION_RECORD_SCHEMA)
        return False
    body = {k: v for k, v in cdoc.items() if k != 'record_sha256'}
    try:
        self_hash = _sha256_hex(_canonical_bytes(body))
    except (ValueError, TypeError, RecursionError) as exc:
        reasons.append('REFUSED (P34-16): the pinned calibration record is not canonically serialisable: %s'
                       % type(exc).__name__)
        return False
    if self_hash != cdoc['record_sha256']:
        reasons.append('REFUSED (P34-16): the pinned calibration record fails its self-hash (record_sha256)')
        return False
    run = cdoc.get('run')
    ex = run.get('exploration') if isinstance(run, dict) else None
    ap = ex.get('admitted_points') if isinstance(ex, dict) else None
    rreg = run.get('region') if isinstance(run, dict) else None
    rsha = rreg.get('sha256') if isinstance(rreg, dict) else None
    if not isinstance(ap, list) or not ap or not _is_hex64(rsha):
        reasons.append('REFUSED (P34-16/X1): the pinned calibration record carries no admitted points or no '
                       'region sha256 in its run content')
        return False
    by_li, lu = {}, []
    for i, p in enumerate(ap):
        if not isinstance(p, dict) or not _is_int(p.get('log_index')) or not isinstance(p.get('u'), list) or \
                not all(_is_real(x) for x in p['u']) or int(p['log_index']) in by_li:
            reasons.append('REFUSED (P34-16/X1): the pinned calibration record admitted_points[%d] is malformed' % i)
            return False
        by_li[int(p['log_index'])] = p
        lu.append((int(p['log_index']), p['u']))
    fp = _fingerprint(lu, rsha)
    if fp != cdoc.get('exploration_fingerprint'):
        reasons.append('REFUSED (P34-16/X1): the pinned calibration record stores exploration_fingerprint %s but '
                       'its run content recomputes to %s' % (_safe_repr(cdoc.get('exploration_fingerprint')), fp))
    if fp != expected_fp:
        reasons.append('REFUSED (P34-16/X1): the pinned calibration record recomputes to exploration_fingerprint '
                       '%s, not the run\'s (selection\'s) %s' % (fp, _safe_repr(expected_fp)))
    if rsha.lower() != region_sha or cdoc.get('region_sha256') != rsha:
        reasons.append('REFUSED (P34-16/X1): the pinned calibration record region sha256 %s differs from the pinned '
                       'DDO154 region file %s' % (_safe_repr(cdoc.get('region_sha256')), region_sha))
    if len(reasons) > n0:
        return False
    region, why = _region_from_bytes(region_path, region_sha)
    if region is None:
        reasons.append('REFUSED (P34-14/X1): the admission rectangles could not be re-derived from the pinned region '
                       'file bytes: %s' % why)
        return False
    bad = []
    for li in sorted(by_li):
        why = _reclassify_admitted(by_li[li], region)
        if why is not None:
            bad.append('log_index %d: %s' % (li, why))
    for li, u in members:
        p = by_li.get(int(li)) if _is_int(li) else None
        if p is None:
            bad.append('member log_index %s is not an admitted point of the pinned calibration record'
                       % _safe_repr(li))
        elif not isinstance(u, (list, tuple)) or not all(_is_real(x) for x in u) or \
                [float(x) for x in p['u']] != [float(x) for x in u]:
            bad.append('member log_index %d: u differs from the recorded admitted point' % int(li))
    if bad:
        reasons.append('REFUSED (P34-14/X1): %d member/admitted point(s) fail the re-classification against the '
                       'rectangles re-derived from the pinned region file bytes: %s' % (len(bad), bad[:5]))
        return False
    return True


def _record_status_reasons(cdoc, ar):
    """v003d (SF-1 fix 2): status, stage and flags of the frozen admitted_region against the pinned record."""
    run = cdoc.get('run')
    ex = run.get('exploration') if isinstance(run, dict) else None
    if not isinstance(ex, dict):
        return ['the pinned calibration record carries no run.exploration']
    out = []
    st = ex.get('status')
    if not (isinstance(st, str) and cdoc.get('status') == run.get('status') == st == ar['exploration_status']):
        out.append('status: record %s / run %s / run exploration %s / frozen exploration_status %s must be equal'
                   % (_safe_repr(cdoc.get('status')), _safe_repr(run.get('status')), _safe_repr(st),
                      _safe_repr(ar['exploration_status'])))
    stage = ex.get('stage_reached')
    if not (isinstance(stage, str) and cdoc.get('stage_reached') == run.get('stage_reached') ==
            'exploration:%s' % stage and ar['exploration_stage_reached'] == stage):
        out.append('stage: record %s / run %s / exploration %s / frozen %s are not one stage'
                   % (_safe_repr(cdoc.get('stage_reached')), _safe_repr(run.get('stage_reached')), _safe_repr(stage),
                      _safe_repr(ar['exploration_stage_reached'])))
    if cdoc.get('ok') is not (run.get('ok') is True):
        out.append('record ok %s differs from the run ok %s' % (_safe_repr(cdoc.get('ok')), _safe_repr(run.get('ok'))))
    flags = ex.get('flags')
    if run.get('flags') != (list(flags) if isinstance(flags, (list, tuple)) else flags) or \
            run.get('region_possibly_truncated') != ex.get('region_possibly_truncated') or \
            run.get('truncation_causes') != list(ex.get('truncation_causes') or []):
        out.append('run flags / region_possibly_truncated / truncation_causes differ from the run exploration\'s')
    ev = ar['truncation_evidence'] if isinstance(ar['truncation_evidence'], list) else []
    engine_flag = (ex.get('region_possibly_truncated') is True or
                   (isinstance(flags, (list, tuple)) and 'REGION_POSSIBLY_TRUNCATED' in flags))
    reported = ('region_possibly_truncated' in ex) or isinstance(flags, (list, tuple))
    if ('ENGINE_FLAG_REGION_POSSIBLY_TRUNCATED' in ev) != engine_flag or \
            ('ENGINE_COVERAGE_NOT_REPORTED' in ev) != (not reported) or \
            (('EXPLORATION_STATUS_%s' % st) in ev) != (st != STATUS_COMPLETE):
        out.append('truncation_evidence %s does not follow the record (engine flag %s, coverage reported %s, status '
                   '%s)' % (_safe_repr(ev)[:120], engine_flag, reported, _safe_repr(st)))
    try:
        cov = _plain(ex.get('coverage'), 'coverage') if ex.get('coverage') is not None else None
    except (ValueError, TypeError, RecursionError):
        cov = {'unserialisable': True}
    if cov != ar['engine_coverage_report']:
        out.append('engine_coverage_report differs from the record\'s exploration coverage')
    return out


def _member_key(m, theta_key):
    return {'log_index': m.get('log_index'), 'role': m.get('role'), 'u': m.get('u'),
            'identified_projection': m.get('identified_projection'), 'theta': m.get(theta_key)}


def _check_record_binds_selection(cdoc, S, ar, region_path, points, member_lists, reasons):
    """v003d (SF-1, writer and verifier): everything select_representative_points freezes must follow from the pinned
    record, not from the caller's dict.
      fix 2: _record_status_reasons (status, stage, flags, coverage);
      fix 3: _validate_admitted_region with the record's identifiability report (IDENTIFICATION_RULE exactly,
             S^T S diagonalised, frozen basis = record basis);
      fix 1: select_representative_points RECOMPUTED from the record's run (region path replaced by the pinned,
             sha-verified region file; interior_count = the frozen selection_interior_count; spec = the freeze
             coordinates): the canonical bytes of the frozen admitted_region must equal the recomputed ones, the
             selection points (writer; None in the verifier) must equal the recomputed points, and every member list
             (log_index, role, u, identified_projection, theta) must equal them in order.
    Appends reasons; returns True when all hold."""
    n0 = len(reasons)
    run = cdoc.get('run')
    if not isinstance(run, dict):
        reasons.append('REFUSED (SF-1): the pinned calibration record carries no run')
        return False
    _validate_admitted_region(ar, S, reasons, record_ident=run.get('identifiability'))
    if len(reasons) > n0:
        reasons.insert(n0, 'REFUSED (SF-1 fix 3): the frozen admitted_region / identifiability does not follow the '
                           'pinned record')
        return False
    st = _record_status_reasons(cdoc, ar)
    if st:
        reasons.append('REFUSED (SF-1 fix 2): the frozen admitted_region disagrees with the pinned calibration '
                       'record: %s' % st[:3])
        return False
    if not isinstance(run.get('region'), dict):
        reasons.append('REFUSED (SF-1 fix 1): the pinned calibration record run carries no region')
        return False
    run2 = dict(run)
    run2['region'] = dict(run['region'], path=region_path)
    sel = select_representative_points(exploration=run2, interior_count=ar['selection_interior_count'],
                                       spec={'coordinates': S['coordinates']})
    if not sel.get('ok'):
        reasons.append('REFUSED (SF-1 fix 1): select_representative_points could not be recomputed from the pinned '
                       'calibration record: %s' % _safe_repr(sel.get('reasons'))[:300])
        return False
    try:
        same = _canonical_bytes(_plain(sel['admitted_region'], 'recomputed')) == _canonical_bytes(_plain(ar, 'frozen'))
    except (ValueError, TypeError, RecursionError) as exc:
        reasons.append('REFUSED (SF-1 fix 1): admitted_region not canonically comparable: %s' % type(exc).__name__)
        return False
    if not same:
        diff = []
        for k in sorted(ADMITTED_REGION_KEYS):
            try:
                if _canonical_bytes(_plain(sel['admitted_region'].get(k), k)) != _canonical_bytes(_plain(ar.get(k), k)):
                    diff.append(k)
            except (ValueError, TypeError, RecursionError):
                diff.append(k)
        reasons.append('REFUSED (SF-1 fix 1): the frozen admitted_region differs from the one select_representative_'
                       'points recomputes from the pinned calibration record (fields %s)' % diff)
        return False
    expect = [_member_key(p, 'theta_natural') for p in sel['points']]
    try:
        exp_bytes = _canonical_bytes(_plain(expect, 'points'))
        if points is not None and \
                _canonical_bytes(_plain([_member_key(p, 'theta_natural') for p in points], 'points')) != exp_bytes:
            reasons.append('REFUSED (SF-1 fix 1): the selection points differ from the points recomputed from the '
                           'pinned calibration record')
            return False
        for label, lst in member_lists:
            if _canonical_bytes(_plain([_member_key(m, 'theta_engine') for m in lst], label)) != exp_bytes:
                reasons.append('REFUSED (SF-1 fix 1): %s (log_index, role, u, identified_projection, theta) differ from '
                               'the points recomputed from the pinned calibration record' % label)
                return False
    except (ValueError, TypeError, RecursionError) as exc:
        reasons.append('REFUSED (SF-1 fix 1): members not canonically comparable: %s' % type(exc).__name__)
        return False
    return True


def _member_order(members):
    return [{'log_index': m['log_index'], 'role': m['role']} for m in members]


# --------------------------------------------------------------------------
# STAGE0 successor (root V006 A142; r3a ROOT_ITEMS M-14; prereg r3a section 6.3) -- the only new behaviour
# --------------------------------------------------------------------------
# STAGE0_GRID_OUTER may read EVALUATED_BEFORE_FREEZE in a Phase-2 freeze, and only by the receipt rule below. Its
# slots V003 record (scope OUTER Q36-Q43, coefficient grid pin, headline false) is unchanged, and so is the slots pin
# (ROOT_SLOTS_PATH / ROOT_SLOTS_SHA256). The successor only PERMITS EVALUATED: every other outcome freezes STAGE0
# NOT_EVALUATED_BEFORE_FREEZE with its codes, and STAGE0 never makes a freeze refuse. The rule reads root-written
# status and receipt bytes only (identities, terminal statuses, times); it never reads an output value.

STAGE0_ALTERNATIVE = 'STAGE0_GRID_OUTER'
STAGE0_STATUS_RECORD_SCHEMA = 'STAGE0_STATUS_RECORD_C2V001'
STAGE0_RECEIPT_SCHEMA = 'STAGE0_TERMINAL_RECEIPT_C2V001'
STAGE0_STATUS_RECORD_KEYS = frozenset({'schema', 'phase', 'alternative', 'sealed_successor', 'step4_start_utc',
                                       'receipts'})
STAGE0_SEALED_SUCCESSOR_KEYS = frozenset({'module_sha256', 'source'})
STAGE0_RECEIPT_ENTRY_KEYS = frozenset({'member_log_index', 'receipt'})
STAGE0_RECEIPT_KEYS = frozenset({'schema', 'alternative', 'member_log_index', 'theta_ngc', 'coefficient_grid_sha256',
                                 'terminal_status', 'written_utc'})
STAGE0_PHASE_1 = 'PHASE_1'
STAGE0_PHASE_2 = 'PHASE_2'
STAGE0_FINISHED = 'FINISHED'
STAGE0_EVALUATED_REFUSED = 'EVALUATED_REFUSED'
STAGE0_NOT_IN_PHASE_1 = 'NOT_IN_PHASE_1'
STAGE0_RECEIPT_NOT_FINISHED = 'STAGE0_RECEIPT_NOT_FINISHED'
STAGE0_NO_SEALED_SUCCESSOR = 'NO_SEALED_SUCCESSOR'
STAGE0_RECEIPTS_AFTER_STEP4 = 'RECEIPTS_AFTER_STEP4'
STAGE0_UTC_FORMATS = ('%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ')
STAGE0_MEMBER_KEYS = frozenset({'member_id', 'log_index', 'receipt', 'custody_ok', 'terminal_status', 'written_utc',
                                'finished', 'before_step4', 'defects'})
STAGE0_BLOCK_KEYS = frozenset({'rule', 'alternative', 'module', 'successor_module_sha256', 'status_record',
                               'status_record_custody_ok', 'phase', 'sealed_successor', 'step4_start_utc', 'members',
                               'rule_a_receipts_finished', 'rule_b_successor_sealed', 'receipts_before_step4',
                               'receipt_refusals', 'evaluation_refusals', 'diagnostics', 'reading', 'reasons',
                               'post_score_exploratory'})
STAGE0_RULE = (
    'M-14 receipt rule (r3a ROOT_ITEMS M-14 = prereg r3a section 6.3; root V006 A142). Phase 1: STAGE0_GRID_OUTER reads '
    'NOT_EVALUATED_BEFORE_FREEZE with NOT_IN_PHASE_1. Phase 2: it is EVALUATED_BEFORE_FREEZE iff (a) every registered '
    'STAGE0 member (one STAGE0 call per PRIMARY member) has exactly one custody-verified terminal receipt reading '
    'FINISHED, (b) the root STAGE0 status record names the sha256 of this module as the sealed successor, every '
    'FINISHED receipt was written no later than the recorded Phase-2 step-4 start (a receipt written at that instant '
    'counts as before), and this successor refuses no STAGE0 record. Otherwise it reads NOT_EVALUATED_BEFORE_FREEZE '
    'with every code that applies (STAGE0_RECEIPT_NOT_FINISHED, NO_SEALED_SUCCESSOR, RECEIPTS_AFTER_STEP4: '
    'exploratory, post-score), or EVALUATED_REFUSED when the receipt rule holds and a STAGE0 record is refused. '
    'Validity booleans and output values never change the status. STAGE0 never makes the freeze refuse and never '
    'enters the headline; when evaluated it is scored on its registered OUTER rows only.')


def _stage0_neutral_record(a):
    """A STAGE0_GRID_OUTER record that reads EVALUATED_BEFORE_FREEZE, with its status put back to the slots V003
    value NOT_EVALUATED_BEFORE_FREEZE; every other value is returned unchanged. Wherever v003g compared a record to
    slots V003 exactly, the successor compares through this, so the only difference ever tolerated is STAGE0's
    status (and _stage0_manifest_check binds that status to the receipt rule)."""
    if isinstance(a, dict) and a.get('name') == STAGE0_ALTERNATIVE and a.get('status') == ALT_EVALUATED:
        return dict(a, status=ALT_NOT_EVALUATED)
    return a


def _stage0_status_neutral(alternatives):
    """The alternatives declaration with _stage0_neutral_record applied to every declared record."""
    if not isinstance(alternatives, dict) or not isinstance(alternatives.get('declared'), list):
        return alternatives
    return dict(alternatives, declared=[_stage0_neutral_record(a) for a in alternatives['declared']])


def _stage0_effective_alternatives(alternatives):
    """The slots alternatives with STAGE0's status EVALUATED_BEFORE_FREEZE (used only once the receipt rule held)."""
    return dict(alternatives, declared=[dict(a, status=ALT_EVALUATED)
                                        if isinstance(a, dict) and a.get('name') == STAGE0_ALTERNATIVE else a
                                        for a in alternatives['declared']])


def _stage0_split_evaluations(alternative_evaluations):
    """(the evaluations without STAGE0, the STAGE0 evaluation or None)."""
    if not isinstance(alternative_evaluations, dict) or STAGE0_ALTERNATIVE not in alternative_evaluations:
        return alternative_evaluations, None
    rest = {k: v for k, v in alternative_evaluations.items() if k != STAGE0_ALTERNATIVE}
    return rest, alternative_evaluations[STAGE0_ALTERNATIVE]


def _stage0_registered():
    """The slots V003 STAGE0_GRID_OUTER record (None if the pinned slots declare none)."""
    for a in _root_slots()[0]['alternatives']['declared']:
        if isinstance(a, dict) and a.get('name') == STAGE0_ALTERNATIVE:
            return a
    return None


def _stage0_self_sha256():
    """sha256 of this module's own file bytes: the sha rule (b) needs the seal entry to pin."""
    raw, _real, _err = _read_regular(os.path.realpath(__file__), True)
    return _sha256_hex(raw) if raw is not None else None


def _stage0_utc(value):
    """A root-recorded UTC time written exactly in one of STAGE0_UTC_FORMATS; None otherwise."""
    if not isinstance(value, str):
        return None
    for fmt in STAGE0_UTC_FORMATS:
        try:
            t = datetime.datetime.strptime(value, fmt)
        except ValueError:
            continue
        if t.strftime(fmt) == value:
            return t
    return None


def _stage0_pin(pin):
    """A well-formed {'path', 'sha256'} pin, normalised to (realpath, lowercase sha256); None otherwise."""
    if isinstance(pin, dict) and set(pin) == {'path', 'sha256'} and isinstance(pin['path'], str) and pin['path'] \
            and _is_hex64(pin['sha256']):
        return {'path': os.path.realpath(pin['path']), 'sha256': pin['sha256'].lower()}
    return None


def _stage0_read(pin, where):
    """(doc, None) for a custody-verified (sha256 from the bytes), target-screened JSON object; (None, code)
    otherwise. A STAGE0 file defect is a code, never a refusal."""
    try:
        doc, _canonical_pin = _root_pinned_document(pin, where)
    except Exception as exc:   # noqa: BLE001
        text = _safe_str(exc)
        if text.startswith('ROOT_ROSTER_PIN_MISMATCH'):
            return None, 'CUSTODY_MISMATCH'
        if text.startswith('ROOT_ROSTER_TARGET_FIELDS_REFUSED'):
            return None, 'TARGET_FIELDS_REFUSED'
        return None, 'MALFORMED'
    return doc, None


def _stage0_same_theta(a, b):
    """Exact theta identity (same keys, equal finite values): the receipt is for this member's call."""
    return bool(isinstance(a, dict) and isinstance(b, dict) and set(a) == set(b)
                and all(_is_real(a[k]) and _is_real(b[k]) and float(a[k]) == float(b[k]) for k in a))


def _stage0_members_of(members):
    """The registered STAGE0 members: one per PRIMARY member, in member order ([] if the list is malformed)."""
    try:
        return [{'member_id': m['member_id'], 'log_index': int(m['log_index']), 'theta_ngc': dict(m['theta_ngc'])}
                for m in members]
    except Exception:   # noqa: BLE001 -- a malformed PRIMARY list refuses elsewhere (v003g checks)
        return []


def _stage0_apply_record(v, members):
    """Fill the verdict v from the status record and its receipts (helper of _stage0_receipt_verdict)."""
    pin = v['status_record']
    if pin is None:
        v['diagnostics'].append('STAGE0_STATUS_RECORD_NOT_SUPPLIED')
        return
    doc, err = _stage0_read(pin, 'STAGE0 status record')
    if doc is None:
        v['diagnostics'].append('STAGE0_STATUS_RECORD_' + err)
        return
    v['status_record_custody_ok'] = True
    if set(doc) != STAGE0_STATUS_RECORD_KEYS or doc['schema'] != STAGE0_STATUS_RECORD_SCHEMA or \
            doc['alternative'] != STAGE0_ALTERNATIVE or doc['phase'] not in (STAGE0_PHASE_1, STAGE0_PHASE_2):
        v['diagnostics'].append('STAGE0_STATUS_RECORD_MALFORMED')
        return
    v['phase'] = doc['phase']
    if doc['phase'] == STAGE0_PHASE_1:
        return   # NOT_IN_PHASE_1: no receipt is read
    ss, st, receipts = doc['sealed_successor'], doc['step4_start_utc'], doc['receipts']
    if not (ss is None or (isinstance(ss, dict) and set(ss) == STAGE0_SEALED_SUCCESSOR_KEYS
                           and _is_hex64(ss['module_sha256']) and isinstance(ss['source'], str)
                           and ss['source'].strip())) \
            or _stage0_utc(st) is None or not isinstance(receipts, list):
        v['diagnostics'].append('STAGE0_STATUS_RECORD_MALFORMED')
        return
    step4 = _stage0_utc(st)
    v['step4_start_utc'] = st
    if ss is None:
        v['diagnostics'].append('STAGE0_SEALED_SUCCESSOR_NOT_NAMED')
    else:
        v['sealed_successor'] = {'module_sha256': ss['module_sha256'].lower(), 'source': ss['source']}
        v['rule_b_successor_sealed'] = v['sealed_successor']['module_sha256'] == v['successor_module_sha256']
        if not v['rule_b_successor_sealed']:
            v['diagnostics'].append('STAGE0_SEALED_SUCCESSOR_IS_NOT_THIS_MODULE')
    registered = _stage0_registered()
    grid = registered.get('coefficient_grid_pin') if isinstance(registered, dict) else None
    grid_sha = grid.get('sha256') if isinstance(grid, dict) else None
    member_lis = set(m['log_index'] for m in members)
    found = {}
    for i, entry in enumerate(receipts):
        li = entry.get('member_log_index') if isinstance(entry, dict) else None
        if not isinstance(entry, dict) or set(entry) != STAGE0_RECEIPT_ENTRY_KEYS or not _is_int(li) or \
                _stage0_pin(entry['receipt']) is None:
            v['receipt_refusals'].append('STAGE0_RECEIPT_ENTRY_MALFORMED: receipts[%d]' % i)
            continue
        if int(li) not in member_lis:
            v['receipt_refusals'].append('STAGE0_RECEIPT_NON_MEMBER: receipts[%d] member_log_index %d' % (i, int(li)))
            continue
        found.setdefault(int(li), []).append(_stage0_pin(entry['receipt']))
    for row, m in zip(v['members'], members):
        got = found.get(m['log_index'], [])
        if not got:
            row['defects'].append('STAGE0_RECEIPT_MISSING')
            continue
        if len(got) > 1:
            row['defects'].append('STAGE0_RECEIPT_DUPLICATE')
            continue
        row['receipt'] = got[0]
        rdoc, rerr = _stage0_read(got[0], 'STAGE0 terminal receipt')
        if rdoc is None:
            row['defects'].append('STAGE0_RECEIPT_' + rerr)
            continue
        row['custody_ok'] = True
        if set(rdoc) != STAGE0_RECEIPT_KEYS or rdoc['schema'] != STAGE0_RECEIPT_SCHEMA or \
                not isinstance(rdoc['terminal_status'], str) or not rdoc['terminal_status'] or \
                _stage0_utc(rdoc['written_utc']) is None:
            row['defects'].append('STAGE0_RECEIPT_MALFORMED')
            continue
        row['terminal_status'] = rdoc['terminal_status']
        row['written_utc'] = rdoc['written_utc']
        if rdoc['alternative'] != STAGE0_ALTERNATIVE or not _is_int(rdoc['member_log_index']) or \
                int(rdoc['member_log_index']) != m['log_index'] or \
                not _stage0_same_theta(rdoc['theta_ngc'], m['theta_ngc']) or \
                not _is_hex64(grid_sha) or rdoc['coefficient_grid_sha256'] != grid_sha:
            row['defects'].append('STAGE0_RECEIPT_IDENTITY_MISMATCH')
            continue
        if rdoc['terminal_status'] != STAGE0_FINISHED:
            row['defects'].append('STAGE0_RECEIPT_TERMINAL_STATUS_NOT_FINISHED')
            continue
        row['finished'] = True
        row['before_step4'] = _stage0_utc(rdoc['written_utc']) <= step4
        if not row['before_step4']:
            row['defects'].append('STAGE0_RECEIPT_WRITTEN_AFTER_STEP4')
    v['rule_a_receipts_finished'] = bool(members) and all(r['finished'] for r in v['members'])
    v['receipts_before_step4'] = all(r['before_step4'] is not False for r in v['members'])


def _stage0_receipt_verdict(record_pin, members):
    """M-14 rule (a), rule (b) and the step-4 timing, from root-written bytes only (no output value is read).

    record_pin: the root STAGE0 status record pin {'path', 'sha256'} (schema STAGE0_STATUS_RECORD_C2V001) or None.
    members: _stage0_members_of(PRIMARY members) -- the registered STAGE0 members, one STAGE0 call per PRIMARY
    member. Every terminal receipt is read from its own bytes (sha256 verified, target-screened) and must name this
    alternative, the member's log_index and exact theta, and the slots V003 STAGE0 coefficient grid sha256. Returns
    the stage0_status fields other than the reading (_stage0_block adds it). Never raises."""
    v = {'successor_module_sha256': _stage0_self_sha256(), 'status_record': _stage0_pin(record_pin),
         'status_record_custody_ok': False, 'phase': None, 'sealed_successor': None, 'step4_start_utc': None,
         'members': [{'member_id': m['member_id'], 'log_index': m['log_index'], 'receipt': None, 'custody_ok': False,
                      'terminal_status': None, 'written_utc': None, 'finished': False, 'before_step4': None,
                      'defects': []} for m in members],
         'rule_a_receipts_finished': False, 'rule_b_successor_sealed': False, 'receipts_before_step4': True,
         'receipt_refusals': [], 'diagnostics': []}
    try:
        _stage0_apply_record(v, members)
    except Exception as exc:   # noqa: BLE001 -- never raises: a defect establishes neither (a) nor (b)
        v['rule_a_receipts_finished'] = v['rule_b_successor_sealed'] = False
        v['diagnostics'].append('STAGE0_RECEIPT_RULE_EXCEPTION: %s' % type(exc).__name__)
    return v


def _stage0_eligible(v):
    """Phase 2, rule (a), rule (b) and the step-4 timing all hold (refusals are judged after this)."""
    return bool(v['phase'] == STAGE0_PHASE_2 and v['rule_a_receipts_finished'] and v['rule_b_successor_sealed']
                and v['receipts_before_step4'])


def _stage0_block(v, evaluation_refusals):
    """The frozen stage0_status block: the receipt verdict plus the M-14 reading and its codes."""
    if v['phase'] == STAGE0_PHASE_1:
        reading, reasons = ALT_NOT_EVALUATED, [STAGE0_NOT_IN_PHASE_1]
    else:
        reasons = []
        if not v['rule_a_receipts_finished']:
            reasons.append(STAGE0_RECEIPT_NOT_FINISHED)
        if not v['rule_b_successor_sealed']:
            reasons.append(STAGE0_NO_SEALED_SUCCESSOR)
        if not v['receipts_before_step4']:
            reasons.append(STAGE0_RECEIPTS_AFTER_STEP4)
        if reasons:
            reading = ALT_NOT_EVALUATED
        elif v['receipt_refusals'] or evaluation_refusals:
            reading = STAGE0_EVALUATED_REFUSED
        else:
            reading = ALT_EVALUATED
    block = dict(v)
    block.update({'rule': STAGE0_RULE, 'alternative': STAGE0_ALTERNATIVE, 'module': MODULE_NAME,
                  'evaluation_refusals': list(evaluation_refusals), 'reading': reading, 'reasons': reasons,
                  'post_score_exploratory': STAGE0_RECEIPTS_AFTER_STEP4 in reasons})
    return block


def _stage0_custody_pins(block):
    """The custody-verified STAGE0 files (status record, member receipts): each must be pinned in input_files."""
    pins = [block['status_record']] if block['status_record_custody_ok'] else []
    return pins + [m['receipt'] for m in block['members'] if m['custody_ok']]


def _stage0_input_files(input_files, block):
    """input_files plus the custody-verified STAGE0 files (realpaths; a file already listed is not added again)."""
    have = set(os.path.realpath(p) for p in input_files if isinstance(p, str) and p)
    extra = [p['path'] for p in _stage0_custody_pins(block) if p['path'] not in have]
    return list(dict.fromkeys(list(input_files) + extra))


def _stage0_evaluation_refusals(ev, selection, spec, ids, roster, roster_pin):
    """Every check v003g applies to a frozen non-primary alternative (writer: ok, query ids, root roster pin, D2
    members; verifier: _validate_members / _validate_member_eval / _validate_envelope; _root_frozen_rows on its
    roster; canonical form; target screen), applied to the STAGE0 evaluation BEFORE it is admitted, plus COMPLETE
    status and member identity with the selection. Any failure is a STAGE0 record refusal (EVALUATED_REFUSED), so an
    admitted STAGE0 cannot make the freeze refuse. Returns the refusal codes ([] = admissible)."""
    try:
        if ev is None:
            return ['STAGE0_EVALUATION_NOT_SUPPLIED']
        if not isinstance(ev, dict) or ev.get('ok') is not True or ev.get('query_ids') != list(ids):
            return ['STAGE0_EVALUATION_NOT_OK']
        if roster is None or ev.get('row_registration_roster') != roster_pin:
            return ['STAGE0_EVALUATION_ROSTER_PIN_MISMATCH']
        if ev.get('status') != STATUS_COMPLETE:
            return ['STAGE0_EVALUATION_NOT_COMPLETE']
        if _canonical_bytes([_member_key(m, 'theta_engine') for m in ev['members']]) != \
                _canonical_bytes([_member_key(p, 'theta_natural') for p in selection['points']]):
            return ['STAGE0_EVALUATION_MEMBERS_NOT_THE_SELECTION']
        reasons = []
        S = _spec_from(spec, reasons)
        if S is None:
            return ['STAGE0_EVALUATION_SPEC_REFUSED']
        ar = selection['admitted_region']
        adm = {p['log_index']: p['projection'] for p in ar['admitted_projections_identified']}
        rec = _plain({'members': ev['members'], 'member_evaluation': _member_eval_record(ev),
                      'pointwise_envelope': ev['pointwise_envelope']}, 'stage0_evaluation')
        if _validate_members(rec['members'], S, ids, len(ar['identified']), 'stage0.members', reasons, adm):
            _validate_member_eval(rec['member_evaluation'], rec['members'], 'stage0.member_evaluation', reasons)
            _validate_envelope(rec['pointwise_envelope'], rec['members'], ids, 'stage0.pointwise_envelope', reasons,
                               _mode_labels(S)[0])
        if reasons:
            return ['STAGE0_EVALUATION_STRUCTURE: ' + _safe_str(reasons[0])[:_MAX_REASON_CHARS]]
        for m in rec['members']:
            _root_frozen_rows(m, list(ids), roster)
        hits = []
        _safe_scan(rec, 'stage0_evaluation', hits, reasons)
        if hits or reasons:
            return ['STAGE0_EVALUATION_TARGET_FIELDS_REFUSED']
        return []
    except Exception as exc:   # noqa: BLE001 -- a refusal of the STAGE0 record, never of the freeze
        return ['STAGE0_EVALUATION_REFUSED: %s: %s' % (type(exc).__name__, _safe_str(exc)[:200])]


def _stage0_freeze_decision(record_pin, evaluation, primary_evaluation, selection, spec, ids, roster, roster_pin):
    """Writer side of M-14. Returns (stage0_status block, admitted). Appends no refusal reason: when STAGE0 is not
    admitted it is frozen NOT_EVALUATED_BEFORE_FREEZE (its reading and codes in the block) and the freeze goes on."""
    members = _stage0_members_of(primary_evaluation.get('members') if isinstance(primary_evaluation, dict) else None)
    v = _stage0_receipt_verdict(record_pin, members)
    refusals = (_stage0_evaluation_refusals(evaluation, selection, spec, ids, roster, roster_pin)
                if _stage0_eligible(v) else [])
    block = _stage0_block(v, refusals)
    return block, block['reading'] == ALT_EVALUATED


def _stage0_manifest_check(doc, reasons):
    """Verifier side of M-14 (writer, verifier and scorer all run it): the frozen stage0_status block must equal the
    block the receipt rule recomputes from the pinned root bytes and the frozen PRIMARY members; STAGE0's declared
    status must follow its reading; an EVALUATED STAGE0 must be COMPLETE; and every custody-verified STAGE0 file must
    be pinned in input_files. The evaluation refusals (EVALUATED_REFUSED) are the writer's record: they are accepted
    only where the receipt rule holds. Appends reasons."""
    block = doc['stage0_status']
    if not isinstance(block, dict) or set(block) != STAGE0_BLOCK_KEYS:
        reasons.append('STAGE0_STATUS_BLOCK_MALFORMED: keys must be %s' % sorted(STAGE0_BLOCK_KEYS))
        return
    if not isinstance(block['members'], list) or \
            any(not isinstance(x, dict) or set(x) != STAGE0_MEMBER_KEYS for x in block['members']):
        reasons.append('STAGE0_STATUS_BLOCK_MALFORMED: member rows must have keys %s' % sorted(STAGE0_MEMBER_KEYS))
        return
    refusals = block['evaluation_refusals']
    if not isinstance(refusals, list) or not all(isinstance(r, str) and r for r in refusals):
        reasons.append('STAGE0_STATUS_BLOCK_MALFORMED: evaluation_refusals must be a list of non-empty strings')
        return
    v = _stage0_receipt_verdict(block['status_record'], _stage0_members_of(doc['members']))
    if refusals and not _stage0_eligible(v):
        reasons.append('STAGE0_STATUS_BLOCK_MISMATCH: evaluation refusals are recorded but the receipt rule does not '
                       'hold')
        return
    if _canonical_bytes(_stage0_block(v, refusals)) != _canonical_bytes(block):
        reasons.append('STAGE0_STATUS_BLOCK_MISMATCH: the frozen stage0_status block differs from the receipt rule '
                       'recomputed from the pinned root bytes')
        return
    evaluated = block['reading'] == ALT_EVALUATED
    status = [a.get('status') for a in doc['alternatives']['declared']
              if isinstance(a, dict) and a.get('name') == STAGE0_ALTERNATIVE]
    if status != [ALT_EVALUATED if evaluated else ALT_NOT_EVALUATED]:
        reasons.append('STAGE0_STATUS_READING_MISMATCH: %s status %s with reading %s'
                       % (STAGE0_ALTERNATIVE, status, block['reading']))
        return
    if evaluated and doc['alternative_results'][STAGE0_ALTERNATIVE]['member_evaluation']['status'] != STATUS_COMPLETE:
        reasons.append('STAGE0_EVALUATION_NOT_COMPLETE: an evaluated STAGE0 must have every member evaluated')
        return
    pinned = set((p['path'], p['sha256']) for p in doc['pins']['input_files'])
    missing = [p['path'] for p in _stage0_custody_pins(block) if (p['path'], p['sha256']) not in pinned]
    if missing:
        reasons.append('STAGE0_CUSTODY_FILE_NOT_PINNED: %s' % missing[:5])


# --------------------------------------------------------------------------
# write_freeze_manifest (+ registration file, D8)
# --------------------------------------------------------------------------

def _pin_files(paths, label, reasons):
    """A4: non-empty list of distinct, regular, non-empty files; sha256 from bytes; realpath recorded."""
    if not isinstance(paths, (list, tuple)) or len(paths) == 0:
        reasons.append('REFUSED: %s must be a non-empty list of paths (vacuous pins refused)' % label)
        return []
    pins = []
    for i, p in enumerate(paths):
        if not isinstance(p, str) or not p:
            reasons.append('%s[%d] is not a non-empty string' % (label, i))
            continue
        raw, real, err = _read_regular(p, True)
        if raw is None:
            reasons.append('REFUSED: %s[%d]: %s' % (label, i, err))
            continue
        pins.append({'path': real, 'sha256': _sha256_hex(raw), 'bytes': len(raw)})
    return pins


def _member_eval_record(ev):
    return {'status': ev['status'], 'stage': 'ngc_members', 'budget': ev['budget'],
            'evaluations_used': ev['evaluations_used'], 'n_selected': ev['n_selected'],
            'n_evaluated': ev['n_evaluated'], 'n_member_valid': ev['n_member_valid']}


@_fail_closed
def write_freeze_manifest(*, out_path, registration_path, parameter_region, observation_rule, spec, selection,
                          alternatives, alternative_evaluations, reference, sensitivity, query_ids, query_manifest,
                          code_files, input_files, notes, allow_incomplete, row_registration_rosters=None,
                          stage0_status_record=None):
    """Write the freeze manifest (canonical JSON, exclusive create) and its registration file.

    Refuses (A3) an incomplete run -- exploration not COMPLETE, any EVALUATED alternative's member
    evaluation not COMPLETE, or sensitivity not COMPLETE -- unless allow_incomplete is True, in
    which case freeze_status FREEZE_INCOMPLETE and the reasons are stamped into the manifest.
    Refuses (A4) empty pin lists, non-regular or zero-length pins, and code_files that omit this
    module. Refuses (D9) alternatives without an evaluated primary, and evaluations that do not
    match the declared EVALUATED set. The reference member must follow REFERENCE_RULE (D5). The
    assembled manifest must pass the same structure check the verifier applies.
    v003:
      * D2: every evaluation's members must be exactly selection['points'] (log_index, role, order);
      * D3/S12/A4: query_manifest = {'path', 'sha256', 'role'}; load_query_manifest must succeed on it,
        query_ids must equal its ids in order, and the file must be in input_files. role 'PROGRAM_PIN'
        requires sha256 == PROGRAM_QUERY_MANIFEST_SHA256 (a2936517...); role 'SYNTHETIC_FIXTURE' requires
        any other sha256 and is stamped in the bytes and echoed by the scorer;
      * the DDO154 observation-region file the selection was re-verified against (sha256 recorded by
        select_representative_points from the run output) must be in input_files;
      * S11: parameter_region must be a non-empty dict with bounds_semantics =
        COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS;
      * P34-16: an input file that is a calibration record (schema CALIBRATION_RUN_RECORD_C2V003) is bound
        and must carry the selection's exploration fingerprint.
    v003a (X1):
      * the calibration record pin is MANDATORY (exactly one record in input_files);
      * the record's exploration fingerprint is recomputed from its run content and must equal both its stored
        value and the selection's (the run's) fingerprint;
      * the admission rectangles are re-derived from the pinned region file BYTES and every member (and every
        admitted point of the record) is re-classified against them from the recorded DDO154 predictions.
    v003d (SF-1): the selection is recomputed from the pinned record's run and must be byte-equal (admitted_region,
    points, every evaluated member list); status, stage and flags are cross-checked against the record; the
    identification rule is re-applied with the record's report (_check_record_binds_selection).
    STAGE0 successor (root V006 A142; r3a ROOT_ITEMS M-14; prereg r3a section 6.3): stage0_status_record is the
    root-written STAGE0 status record pin {'path', 'sha256'} (schema STAGE0_STATUS_RECORD_C2V001) or None. The caller
    passes the slots alternatives unchanged (a STAGE0 status set by the caller is put back to the slots value; it is
    never the caller's to set) and may include a STAGE0_GRID_OUTER replay evaluation in alternative_evaluations. That
    evaluation is frozen, with STAGE0 EVALUATED_BEFORE_FREEZE, only when the receipt rule holds
    (_stage0_receipt_verdict) and it passes every check a frozen alternative must pass
    (_stage0_evaluation_refusals). Otherwise STAGE0 is frozen NOT_EVALUATED_BEFORE_FREEZE (reading
    NOT_EVALUATED_BEFORE_FREEZE or EVALUATED_REFUSED, with its codes, in the manifest's stage0_status block) and the
    freeze goes on: STAGE0 never makes the freeze refuse. The status record and every custody-verified receipt are
    added to input_files.
    After the manifest, writes registration_path (D8) recording the manifest FILE sha256; that
    value must be logged before any target access and passed to score_after_freeze.
    """
    reasons = []
    out = {'ok': False, 'path': None, 'registration_path': None, 'manifest_sha256': None,
           'manifest_file_sha256': None, 'registration_file_sha256': None, 'bytes_written': 0,
           'freeze_status': None, 'incomplete_reasons': [], 'query_manifest_role': None,
           'calibration_record_bound': False, 'reasons': reasons}
    for label, p in (('out_path', out_path), ('registration_path', registration_path)):
        if not isinstance(p, str) or not p:
            reasons.append('%s must be a non-empty string' % label)
    if reasons:
        return out
    out['path'] = os.path.abspath(out_path)
    out['registration_path'] = os.path.abspath(registration_path)
    if out['path'] == out['registration_path']:
        reasons.append('registration_path must differ from out_path')
        return out
    for label, p in (('out_path', out_path), ('registration_path', registration_path)):
        if os.path.lexists(p):
            reasons.append('REFUSED: %s already exists (no overwrite): %s' % (label, os.path.abspath(p)))
        elif not os.path.isdir(os.path.dirname(os.path.abspath(p))):
            reasons.append('parent directory of %s does not exist' % label)
    if not isinstance(allow_incomplete, bool):
        reasons.append('allow_incomplete must be a bool')
    if not isinstance(parameter_region, dict) or not parameter_region or \
            parameter_region.get('bounds_semantics') != BOUNDS_SEMANTICS:
        reasons.append('REFUSED (S11): parameter_region must be a non-empty dict carrying bounds_semantics = %s'
                       % BOUNDS_SEMANTICS)
    if not isinstance(observation_rule, (dict, list, tuple, str)):
        reasons.append('observation_rule must be a dict, list or string')
    S = _spec_from(spec, reasons)
    ids = _check_query_ids(query_ids, reasons, True)
    if reasons:
        return out
    # D3 / S12 / A4: bind the 43 ids to the pinned target-free query manifest
    if not isinstance(query_manifest, dict) or set(query_manifest) != {'path', 'sha256', 'role'}:
        reasons.append('REFUSED (D3): query_manifest must be {"path", "sha256", "role"}')
        return out
    qm_role = query_manifest['role']
    qm_sha = query_manifest['sha256'].lower() if isinstance(query_manifest['sha256'], str) else None
    if not isinstance(qm_role, str) or qm_role not in QUERY_MANIFEST_ROLES or not _is_hex64(qm_sha):
        reasons.append('REFUSED (D3): query_manifest.role must be one of %s and sha256 64-hex'
                       % list(QUERY_MANIFEST_ROLES))
        return out
    if qm_role == QM_ROLE_PROGRAM and qm_sha != PROGRAM_QUERY_MANIFEST_SHA256:
        reasons.append('REFUSED (A4/D3): role PROGRAM_PIN requires the program query manifest sha256 %s, got %s'
                       % (PROGRAM_QUERY_MANIFEST_SHA256, qm_sha))
        return out
    if qm_role == QM_ROLE_SYNTHETIC and qm_sha == PROGRAM_QUERY_MANIFEST_SHA256:
        reasons.append('REFUSED (D3): the program query manifest must be bound with role PROGRAM_PIN')
        return out
    qm = load_query_manifest(path=query_manifest['path'], expected_sha256=qm_sha)
    if not qm.get('ok'):
        reasons.append('REFUSED (D3): query manifest did not load: %s' % qm.get('reasons'))
        return out
    if list(ids) != list(qm['query_ids']):
        reasons.append('REFUSED (D3/S12): query_ids differ from the pinned query manifest ids (order included)')
        return out
    qm_real = os.path.realpath(query_manifest['path'])
    out['query_manifest_role'] = qm_role
    if not isinstance(selection, dict) or selection.get('ok') is not True or \
            not isinstance(selection.get('admitted_region'), dict) or not isinstance(selection.get('points'), list):
        reasons.append('selection must be an ok output of select_representative_points')
        return out
    ar = selection['admitted_region']
    if ar.get('admission_reverified') is not True or not _is_hex64(ar.get('observation_region_sha256')):
        reasons.append('REFUSED (P34-14/D3): the selection was not re-verified against a hash-verified DDO154 '
                       'region; pass the run_calibration_region output to select_representative_points')
        return out
    sel_order = [{'log_index': p['log_index'], 'role': p['role']} for p in selection['points']]
    if sel_order != ar.get('selected_points'):
        reasons.append('REFUSED (D2): selection points differ from its own selected_points')
        return out
    alternatives = _stage0_status_neutral(alternatives)   # STAGE0 successor: the receipt rule sets STAGE0's status
    alts = _bind_alternatives(alternatives, reasons)
    if alts is None:
        return out
    try:
        root_rosters = _root_rosters_for_alternatives(row_registration_rosters, alternatives, ids)
        root_pins = {name: roster['pin'] for name, roster in root_rosters.items()}
        input_files = list(dict.fromkeys(list(input_files) + [p['path'] for r in root_rosters.values() for p in r['dependencies']]))
    except (ValueError, TypeError, KeyError) as exc:
        reasons.append('ROOT_ROSTER_REFUSED: ' + str(exc))
        return out
    # STAGE0 successor (M-14): a STAGE0 evaluation is set aside here and admitted below only by the receipt rule,
    # so D9 binds every other alternative exactly as in v003g and STAGE0 never refuses the freeze.
    alternative_evaluations, stage0_evaluation = _stage0_split_evaluations(alternative_evaluations)
    if not isinstance(alternative_evaluations, dict) or set(alternative_evaluations) != set(alts['evaluated']):
        reasons.append('REFUSED (D9): alternative_evaluations keys %s must equal the EVALUATED_BEFORE_FREEZE '
                       'alternatives %s' % (sorted(alternative_evaluations) if isinstance(alternative_evaluations, dict)
                                            else _safe_repr(alternative_evaluations), alts['evaluated']))
        return out
    for name, ev in alternative_evaluations.items():
        if isinstance(ev, dict) and ev.get('row_registration_roster') != root_pins[name]:
            reasons.append('ROOT_ROSTER_EVALUATION_PIN_MISMATCH: ' + name)
        if not isinstance(ev, dict) or ev.get('ok') is not True or ev.get('query_ids') != list(ids):
            reasons.append('alternative_evaluations[%r] must be an ok evaluate_envelopes output on query_ids' % name)
            continue
        if _member_order(ev['members']) != sel_order:
            reasons.append('REFUSED (D2): alternative_evaluations[%r] members %s are not exactly the selected '
                           'representatives %s (log_index, role, order)'
                           % (name, [m['log_index'] for m in ev['members']], [p['log_index'] for p in sel_order]))
    if not isinstance(reference, dict) or reference.get('ok') is not True:
        reasons.append('reference must be an ok output of select_reference_member')
    if not isinstance(sensitivity, dict) or sensitivity.get('ok') is not True:
        reasons.append('sensitivity must be an ok output of evaluate_sensitivity')
    elif sensitivity.get('row_registration_roster') != root_pins[alts['primary']]:
        reasons.append('ROOT_ROSTER_SENSITIVITY_PIN_MISMATCH')
    if reasons:
        return out
    # STAGE0 successor (M-14): the receipt rule decides STAGE0's status from root-written bytes. The successor only
    # PERMITS EVALUATED_BEFORE_FREEZE; every other outcome freezes STAGE0 NOT_EVALUATED without a refusal.
    stage0, stage0_admitted = _stage0_freeze_decision(
        stage0_status_record, stage0_evaluation, alternative_evaluations[alts['primary']], selection, spec, ids,
        root_rosters.get(STAGE0_ALTERNATIVE), root_pins.get(STAGE0_ALTERNATIVE))
    if stage0_admitted:
        alternatives = _stage0_effective_alternatives(alternatives)
        alts = _bind_alternatives(alternatives, reasons)
        if alts is None:
            return out
        alternative_evaluations = dict(alternative_evaluations)
        alternative_evaluations[STAGE0_ALTERNATIVE] = stage0_evaluation
    input_files = _stage0_input_files(input_files, stage0)
    hits = []
    for label, value in (('parameter_region', parameter_region), ('observation_rule', observation_rule),
                         ('alternatives', alternatives), ('notes', notes)):
        _safe_scan(value, label, hits, reasons)
    if hits:
        reasons.append('REFUSED: forbidden target field name(s) present: %s' % hits)
    if reasons:
        return out

    prim = alternative_evaluations[alts['primary']]
    ref_rec = {k: reference[k] for k in REFERENCE_KEYS}
    sens_rec = {k: sensitivity[k] for k in SENS_KEYS}
    alt_results = {name: {'members': alternative_evaluations[name]['members'],
                          'member_evaluation': _member_eval_record(alternative_evaluations[name]),
                          'pointwise_envelope': alternative_evaluations[name]['pointwise_envelope']}
                   for name in alts['non_primary_evaluated']}
    me = _member_eval_record(prim)
    incomplete = _incomplete_reasons(ar, me, sens_rec, alt_results)
    out['incomplete_reasons'] = list(incomplete)
    if incomplete and not allow_incomplete:
        reasons.append('REFUSED (A3): run is incomplete %s; pass allow_incomplete=True to stamp '
                       'FREEZE_INCOMPLETE' % incomplete)
        return out
    status = FREEZE_INCOMPLETE if incomplete else FREEZE_COMPLETE
    out['freeze_status'] = status
    # v003b: A16.1/A16.4 slot geometry (when declared; required in the A13 mode) and the A13 headline conditions
    a16 = _check_slot_geometry(S, sens_rec, notes, reasons)
    hc = _headline_conditions(S, alts, a16, notes, reasons) if S['coordinate_mode'] == MODE_D_FIXED else None
    if reasons:
        return out

    code_pins = _pin_files(code_files, 'code_files', reasons)
    input_pins = _pin_files(input_files, 'input_files', reasons)
    if reasons:
        return out
    me_path = os.path.realpath(__file__)
    if me_path not in [p['path'] for p in code_pins]:
        reasons.append('REFUSED (A4): code_files must include this freeze module %s' % me_path)
    allp = [p['path'] for p in code_pins + input_pins]
    if len(set(allp)) != len(allp):
        reasons.append('REFUSED: duplicate pin paths')
    if not any(p['path'] == qm_real and p['sha256'] == qm_sha for p in input_pins):
        reasons.append('REFUSED (D3/A4): input_files must include the bound query manifest %s (sha256 %s)'
                       % (qm_real, qm_sha))
    region_sha = ar['observation_region_sha256'].lower()
    region_pins = [p for p in input_pins if p['sha256'] == region_sha]
    if not region_pins:
        reasons.append('REFUSED (D3): input_files must include the DDO154 observation-region file the selection '
                       'was re-verified against (sha256 %s)' % region_sha)
    # P34-16 / X1 (v003a): the calibration record pin is MANDATORY
    rec_pins = []
    for p in input_pins:
        raw, _real, _err = _read_regular(p['path'], True)
        if raw is None or _sha256_hex(raw) != p['sha256'] or CALIBRATION_RECORD_SCHEMA.encode('ascii') not in raw:
            continue
        doc, _perr = _parse_json_bytes(raw)
        if not isinstance(doc, dict) or doc.get('schema') != CALIBRATION_RECORD_SCHEMA:
            continue
        rec_pins.append((p, doc))
    if not rec_pins:
        reasons.append('REFUSED (P34-16/X1): input_files must include the calibration record of this run '
                       '(calibration_region_engine write_calibration_record output); the record pin is mandatory')
    elif len(rec_pins) > 1:
        reasons.append('REFUSED (P34-16): more than one calibration record pinned')
    if reasons:
        return out
    rec_pin, rec_doc = rec_pins[0]
    member_lu = [(p['log_index'], p['u']) for p in selection['points']]
    for ev in alternative_evaluations.values():
        member_lu.extend((m.get('log_index'), m.get('u')) for m in ev['members'])
    if not _check_calibration_record(rec_doc, ar.get('calibration_fingerprint'), region_sha, region_pins[0]['path'],
                                     member_lu, reasons):
        return out
    # v003c (V8e-3/A23): the freeze coordinates bind to the pinned record's own calibration coordinates
    if not _check_run_coordinate_binding(S, (rec_doc.get('run') or {}).get('spec'), 'the pinned calibration record',
                                         reasons):
        return out
    # v003d (SF-1): status/flags, identifiability and the whole selection follow from the pinned record
    if not _check_record_binds_selection(rec_doc, S, ar, region_pins[0]['path'], selection['points'],
                                         [('alternative_evaluations[%r].members' % nm, alternative_evaluations[nm]
                                           ['members']) for nm in sorted(alternative_evaluations)], reasons):
        return out
    cal_binding = {'path': rec_pin['path'], 'sha256': rec_pin['sha256'],
                   'exploration_fingerprint': rec_doc.get('exploration_fingerprint')}
    out['calibration_record_bound'] = True
    input_bindings = {
        'query_manifest': {'path': qm_real, 'sha256': qm_sha, 'role': qm_role,
                           'is_program_pin': qm_sha == PROGRAM_QUERY_MANIFEST_SHA256,
                           'program_pin_sha256': PROGRAM_QUERY_MANIFEST_SHA256,
                           'query_ids_sha256': _query_ids_sha256(ids), 'rad_unit': qm.get('rad_unit')},
        'observation_region': {'sha256': region_sha},
        'calibration_record': cal_binding,
    }
    band_scope = _mode_labels(S)[2]   # v003b: the A13 condition in the fixed-distance mode
    try:
        body = {
            'schema': SCHEMA,
            'module': MODULE_NAME,
            'created_utc': _now_utc(),
            'freeze_status': status,
            'incomplete_reasons': incomplete,
            'parameter_region': parameter_region,
            'admitted_region': ar,
            'coordinates': S['coordinates'],
            'observation_rule': observation_rule,
            'query_ids': list(ids),
            'units': UNITS,
            'semantics': SEMANTICS,
            'alternatives': {'primary': alts['primary'], 'declared': alts['declared']},
            'members': prim['members'],
            'member_evaluation': me,
            'reference_member': ref_rec,
            'pointwise_envelope': prim['pointwise_envelope'],
            'sensitivity': sens_rec,
            'band_scope': band_scope,
            'conditional_on_trial_values': _conditional_on_trial(S, ar, sens_rec),
            'alternative_results': alt_results,
            'headline_rule': HEADLINE_RULE,
            'within_error_rule': WITHIN_ERROR_RULE,
            'pins': {'code_files': code_pins, 'input_files': input_pins},
            'input_bindings': input_bindings,
            'row_registration_rosters': root_pins,
            'stage0_status': stage0,   # STAGE0 successor (M-14)
            'notes': notes,
            'target_velocities_included': False,
            'manifest_sha256': '0' * 64,
        }
        if hc is not None:   # v003b (A13): only in the fixed-distance mode
            body[HEADLINE_CONDITIONS_KEY] = hc
        manifest = _plain(body, 'manifest')
    except (ValueError, TypeError, RecursionError) as exc:
        reasons.append('manifest not canonically serialisable: %s: %s' % (type(exc).__name__, _safe_str(exc)))
        return out
    _validate_manifest_structure(manifest, reasons)
    if reasons:
        reasons.insert(0, 'REFUSED: assembled manifest fails the verifier structure check')
        return out
    del manifest['manifest_sha256']
    try:
        digest = _sha256_hex(_canonical_bytes(manifest))
        manifest['manifest_sha256'] = digest
        payload = _canonical_bytes(manifest)
    except (ValueError, TypeError, RecursionError) as exc:
        reasons.append('manifest not canonically serialisable: %s' % _safe_str(exc))
        return out
    try:
        with open(out_path, 'xb') as fh:
            fh.write(payload)
    except (OSError, ValueError) as exc:
        reasons.append('REFUSED: could not create out_path: %s: %s' % (type(exc).__name__, _safe_str(exc)))
        return out
    raw, real, err = _read_regular(out_path, True)
    if raw is None or raw != payload:
        reasons.append('read-back mismatch after write: %s' % (err or 'bytes differ'))
        return out
    # P34-15 (v003): the writer re-verifies its own bytes (parse -> canonical -> self-hash) before registering
    vchk = {'manifest_sha256_recomputed': None, 'manifest_sha256_recorded': None, 'canonical_bytes_match': None,
            'pins_verified': []}
    vreasons = []
    if _verify_bytes(raw, out_path, vchk, vreasons) is None:
        reasons.append('REFUSED: the written manifest does not re-verify from its own bytes; not registered: %s'
                       % vreasons[:3])
        return out
    file_sha = _sha256_hex(raw)
    out.update({'manifest_sha256': digest, 'manifest_file_sha256': file_sha, 'bytes_written': len(payload)})
    reg = {'schema': REGISTRATION_SCHEMA, 'created_utc': _now_utc(), 'manifest_path': real,
           'expected_manifest_file_sha256': file_sha, 'manifest_sha256_self': digest,
           'manifest_bytes': len(payload),
           'note': ('registered at freeze time, before any NGC3198 target access; score_after_freeze '
                    'refuses unless the caller passes this expected_manifest_file_sha256 and the file '
                    'bytes hash to it')}
    reg['registration_sha256'] = _sha256_hex(_canonical_bytes(reg))
    rpayload = _canonical_bytes(reg)
    try:
        with open(registration_path, 'xb') as fh:
            fh.write(rpayload)
    except (OSError, ValueError) as exc:
        reasons.append('MANIFEST WRITTEN BUT REGISTRATION FAILED (scorer will refuse): %s: %s'
                       % (type(exc).__name__, _safe_str(exc)))
        return out
    out['registration_file_sha256'] = _sha256_hex(rpayload)
    out['ok'] = True
    return out


# --------------------------------------------------------------------------
# verify_freeze_manifest / verify_registration / score_after_freeze
# --------------------------------------------------------------------------

def _verify_bytes(raw, path_label, out, reasons):
    """Verify manifest bytes. Pins are read only after hash, canonical form and structure pass (N01)."""
    doc, err = _parse_json_bytes(raw)
    if doc is None:
        reasons.append(err)
        return None
    if not isinstance(doc, dict):
        reasons.append('manifest is not a JSON object')
        return None
    recorded = doc.get('manifest_sha256')
    out['manifest_sha256_recorded'] = recorded if isinstance(recorded, str) else None
    body = {k: v for k, v in doc.items() if k != 'manifest_sha256'}
    try:
        recomputed = _sha256_hex(_canonical_bytes(body))
        full = _canonical_bytes(doc)
    except (ValueError, TypeError, RecursionError) as exc:
        reasons.append('manifest not canonically serialisable: %s' % exc)
        return None
    out['manifest_sha256_recomputed'] = recomputed
    out['canonical_bytes_match'] = (full == raw)
    if 'manifest_sha256' not in doc:
        reasons.append('manifest_sha256 key absent')
    elif recomputed != recorded:
        reasons.append('manifest_sha256 mismatch: recorded %r, recomputed %s' % (recorded, recomputed))
    if full != raw:
        reasons.append('file bytes are not the canonical JSON of their content')
    if reasons:
        return None
    _validate_manifest_structure(doc, reasons)
    if reasons:
        return None
    for label in ('code_files', 'input_files'):
        for pin in doc['pins'][label]:
            praw, preal, perr = _read_regular(pin['path'], True)
            actual = _sha256_hex(praw) if praw is not None else None
            pok = (actual is not None and actual == pin['sha256'] and len(praw) == pin['bytes']
                   and preal == pin['path'])
            out['pins_verified'].append({'path': pin['path'], 'recorded': pin['sha256'], 'actual': actual,
                                         'ok': bool(pok)})
            if not pok:
                reasons.append('pin mismatch for %r: recorded %r, actual %r%s'
                               % (pin['path'], pin['sha256'], actual, '' if perr is None else ' (%s)' % perr))
    if reasons:
        return None
    # D3/S12 (v003): re-bind the 43 ids to the pinned query manifest from its bytes
    qb = doc['input_bindings']['query_manifest']
    qm = load_query_manifest(path=qb['path'], expected_sha256=qb['sha256'])
    if not qm.get('ok') or list(qm['query_ids']) != list(doc['query_ids']):
        reasons.append('query_ids are not the ids of the pinned query manifest %s (D3/S12): %s'
                       % (qb['path'], qm.get('reasons')))
        return None
    out['query_manifest_role'] = qb['role']
    # P34-16 / X1 (v003a): the bound calibration record (mandatory; the structure check refuses None) is re-read
    # from its bytes, its fingerprint is recomputed from its run content, the rectangles are re-derived from the
    # pinned region file bytes and every member is re-classified against them
    cb = doc['input_bindings']['calibration_record']
    craw, _cr, cerr = _read_regular(cb['path'], True)
    cdoc = _parse_json_bytes(craw)[0] if craw is not None else None
    if craw is None or _sha256_hex(craw) != cb['sha256'] or not isinstance(cdoc, dict):
        reasons.append('bound calibration record %s unreadable or changed since pinning%s'
                       % (cb['path'], '' if cerr is None else ' (%s)' % cerr))
        return None
    region_sha = doc['input_bindings']['observation_region']['sha256']
    region_path = next(p['path'] for p in doc['pins']['input_files'] if p['sha256'] == region_sha)
    members = [(m['log_index'], m['u']) for m in doc['members']]
    for a in doc['alternative_results'].values():
        members.extend((m['log_index'], m['u']) for m in a['members'])
    if not _check_calibration_record(cdoc, doc['admitted_region']['calibration_fingerprint'], region_sha,
                                     region_path, members, reasons):
        return None
    # v003c (V8e-3/A23): the frozen coordinates bind to the bound record's own calibration coordinates
    S = _build_spec(doc['coordinates'], [])   # the structure check above built it already
    if not _check_run_coordinate_binding(S, (cdoc.get('run') or {}).get('spec'), 'the bound calibration record',
                                         reasons):
        return None
    # v003d (SF-1): status/flags, identifiability, the frozen selection and every member follow from the record
    lists = [('members', doc['members'])] + [('alternative_results[%r].members' % nm, a['members'])
                                             for nm, a in sorted(doc['alternative_results'].items())]
    if not _check_record_binds_selection(cdoc, S, doc['admitted_region'], region_path, None, lists, reasons):
        return None
    return doc


def _verify_impl(freeze_manifest_path):
    reasons = []
    out = {'ok': False, 'path': None, 'manifest_file_sha256': None, 'manifest_sha256_recomputed': None,
           'manifest_sha256_recorded': None, 'canonical_bytes_match': None, 'freeze_status': None,
           'query_manifest_role': None, 'pins_verified': [], 'reasons': reasons}
    if not isinstance(freeze_manifest_path, str) or not freeze_manifest_path:
        reasons.append('freeze_manifest_path must be a non-empty string')
        return out, None, None
    out['path'] = os.path.abspath(freeze_manifest_path)
    raw, _real, err = _read_regular(freeze_manifest_path, True)
    if raw is None:
        reasons.append(err)
        return out, None, None
    out['manifest_file_sha256'] = _sha256_hex(raw)
    doc = _verify_bytes(raw, freeze_manifest_path, out, reasons)
    if doc is None:
        return out, None, raw
    out['freeze_status'] = doc['freeze_status']
    out['ok'] = True
    return out, doc, raw


@_fail_closed
def verify_freeze_manifest(*, freeze_manifest_path):
    """Recompute the self-hash and check canonical bytes, the full v003 structure and internal
    consistency (envelope, reference rule, sensitivity plan, freeze status recomputed from the
    member arrays; D1 all-or-nothing rows; D2 selection recomputed from the frozen rule inputs and
    members equal to it; S11 parameter_region label; D3 input bindings), then every pin from bytes
    (regular, non-empty files only), then re-binds the 43 ids to the pinned query manifest via
    load_query_manifest and re-checks a bound calibration record's fingerprint (P34-16).

    Note (D8): a self-consistent re-hashed edit still verifies here; identity against the frozen
    file is established only by score_after_freeze's registered file hash.
    """
    result, _doc, _raw = _verify_impl(freeze_manifest_path)
    return result


def _verify_registration_impl(registration_path):
    reasons = []
    out = {'ok': False, 'path': None, 'registration_file_sha256': None, 'expected_manifest_file_sha256': None,
           'manifest_path': None, 'manifest_sha256_self': None, 'reasons': reasons}
    if not isinstance(registration_path, str) or not registration_path:
        reasons.append('registration_path must be a non-empty string')
        return out
    out['path'] = os.path.abspath(registration_path)
    raw, _real, err = _read_regular(registration_path, True)
    if raw is None:
        reasons.append(err)
        return out
    out['registration_file_sha256'] = _sha256_hex(raw)
    doc, err = _parse_json_bytes(raw)
    if doc is None:
        reasons.append(err)
        return out
    if not isinstance(doc, dict) or set(doc) != REGISTRATION_KEYS:
        reasons.append('registration keys differ from %s' % sorted(REGISTRATION_KEYS))
        return out
    if doc['schema'] != REGISTRATION_SCHEMA:
        reasons.append('registration schema differs')
    try:
        body = {k: v for k, v in doc.items() if k != 'registration_sha256'}
        if _sha256_hex(_canonical_bytes(body)) != doc['registration_sha256']:
            reasons.append('registration_sha256 mismatch')
        if _canonical_bytes(doc) != raw:
            reasons.append('registration bytes are not canonical')
    except (ValueError, TypeError, RecursionError) as exc:
        reasons.append('registration not canonical: %s' % _safe_str(exc))
    if not _is_hex64(doc['expected_manifest_file_sha256']) or not _is_hex64(doc['manifest_sha256_self']):
        reasons.append('registration hashes malformed')
    if reasons:
        return out
    out.update({'expected_manifest_file_sha256': doc['expected_manifest_file_sha256'],
                'manifest_path': doc['manifest_path'], 'manifest_sha256_self': doc['manifest_sha256_self'],
                'ok': True})
    return out


@_fail_closed
def verify_registration(*, registration_path):
    """Check the registration file's self-hash and canonical bytes; return the registered hash."""
    return _verify_registration_impl(registration_path)


def _ladder_row(q, predicted, row_valid, observed, sigma):
    residual = sigma_ratio = fractional = None
    notes = []
    if predicted is not None:
        residual = predicted - observed
        r = residual / sigma
        if math.isfinite(r):
            sigma_ratio = r
        else:
            notes.append('NON_FINITE_SIGMA_RATIO')
        if observed != 0.0:
            f = residual / observed
            if math.isfinite(f):
                fractional = f
            else:
                notes.append('NON_FINITE_FRACTIONAL_ERROR')
    valid = bool(row_valid and predicted is not None)
    within = bool(valid and sigma_ratio is not None and abs(sigma_ratio) <= 1.0)
    return {'id': q, 'observed_speed_km_s': observed, 'predicted_speed_km_s': predicted,
            'quoted_sigma_km_s': sigma, 'signed_residual_km_s': residual, 'sigma_ratio': sigma_ratio,
            'fractional_error': fractional, 'valid': valid, 'within_error': within, 'row_notes': notes}


def _score_members(members, ids, bound):
    scored=[]
    for m in members:
        rows=[]
        for j,q in enumerate(ids):
            row=_ladder_row(q,m['speeds_km_s'][j],m['row_valid'][j],bound[j][0],bound[j][1])
            reg=m['row_registration'][j]
            if reg is not None:
                row.update(status='INVALID',prediction=None,registered_reason=reg['reason'],score_status='INVALID_AS_MISS',tier='MISS_WORST_TIER')
                row['row_notes'].append('INVALID_AS_MISS')
            else:
                row.update(status='VALID' if row['valid'] else 'UNEVALUATED_OR_REFUSED',prediction=row['predicted_speed_km_s'],registered_reason=None,
                           score_status='HIT' if row['within_error'] else 'MISS',tier='WITHIN_ERROR' if row['within_error'] else 'MISS_WORST_TIER')
            rows.append(row)
        invalid_as_miss=[r['id'] for r in rows if r['score_status']=='INVALID_AS_MISS']
        scored.append({'member_id':m['member_id'],'log_index':m['log_index'],'role':m['role'],'evaluated':m['evaluated'],'member_valid':m['member_valid'],
                       'within_error_count':sum(r['within_error'] for r in rows),'invalid_count':sum(not r['valid'] for r in rows),'n_rows':len(rows),
                       'invalid_as_miss':invalid_as_miss,'invalid_as_miss_count':len(invalid_as_miss),'rows':rows})
    return scored




def _alternative_score_scope(alternative, ids, roster):
    """0548 selected rows are root-listed frozen IDs, mapped to fixture IDs explicitly."""
    if alternative['name'] != 'STAGE0_GRID_OUTER':
        return None
    slots = _root_slots()[0]
    registered = next(a for a in slots['alternatives']['declared'] if a['name'] == 'STAGE0_GRID_OUTER')
    if _stage0_neutral_record(alternative) != registered or alternative['headline'] is not False:   # STAGE0 successor
        raise ValueError('STAGE0_EXACT_NON_HEADLINE_RECORD_REQUIRED')
    scope = alternative['scoring_scope']
    rows = slots['query_block']['rows']
    expected = [q['query_id'] for q in rows if float(q['Rad_text']) >= 30.0]
    if scope != {'zone': 'OUTER', 'radius_min_kpc': 30.0, 'radius_min_inclusive': True, 'query_ids': expected}:
        raise ValueError('STAGE0_REGISTERED_OUTER_SCOPE_REQUIRED')
    mapping = {q['slots_query_id']: q['query_id'] for q in roster['document']['query_mapping']}
    selected = [mapping[q] for q in expected]
    if not selected or len(set(selected)) != len(selected) or any(q not in ids for q in selected):
        raise ValueError('STAGE0_OUTER_QUERY_MAPPING_REQUIRED')
    return {'zone': 'OUTER', 'radius_min_kpc': 30.0, 'radius_min_inclusive': True,
            'query_ids': selected, 'registered_query_ids': expected, 'n_rows': len(selected),
            'coefficient_grid_pin': dict(alternative['coefficient_grid_pin']), 'headline': False}

def _score_members_on_rows(members, ids, bound, selected_ids):
    """Score only the selected alternative rows; never compute excluded-row hits."""
    if not isinstance(selected_ids, list) or not selected_ids or len(set(selected_ids)) != len(selected_ids) or any(q not in ids for q in selected_ids):
        raise ValueError('ALTERNATIVE_SCORE_ROW_SET_REQUIRED')
    indexes = [ids.index(q) for q in selected_ids]
    subset = []
    for member in members:
        narrowed = dict(member)
        for key in ('speeds_km_s', 'row_valid', 'row_registration'):
            narrowed[key] = [member[key][j] for j in indexes]
        subset.append(narrowed)
    return _score_members(subset, selected_ids, [bound[j] for j in indexes])

def _distribution(counts):
    if not counts:
        return {'n': 0, 'min': None, 'median': None, 'max': None}
    return {'n': len(counts), 'min': min(counts), 'median': _median(counts), 'max': max(counts)}


def _band_rows(rows_in, low_key, high_key, ids, bound):
    rows = []
    n_overlap = n_invalid = 0
    for j, q in enumerate(ids):
        r = rows_in[j]
        obs, sig = bound[j]
        lo, hi, valid = r[low_key], r[high_key], r['valid']
        overlaps = bool(valid and lo is not None and hi is not None and lo <= obs + sig and hi >= obs - sig)
        n_overlap += overlaps
        n_invalid += (not valid)
        rows.append({'id': q, 'band_low_km_s': lo, 'band_high_km_s': hi, 'valid': bool(valid),
                     'band_overlaps_error_bar': overlaps, 'label': r['label'],
                     'score_status': 'BAND_OVERLAP' if overlaps else 'BAND_MISS' if valid else 'INVALID_AS_MISS',
                     'tier': 'WITHIN_ERROR' if overlaps else 'MISS_WORST_TIER'})
    return rows, n_overlap, n_invalid


@_fail_closed
def score_after_freeze(*, freeze_manifest_path, registration_path, expected_manifest_file_sha256, target_rows, row_registration_rosters=None):
    """Score the frozen members against target rows; refuses unless identity and integrity hold.

    D8: refuses unless the registration file verifies, expected_manifest_file_sha256 (logged before
    target access) equals the registered value AND the manifest file's byte hash, and the manifest
    then fully verifies (self-hash, canonical bytes, structure, pins). Echoes the expected and
    actual file hashes, the self-hash, the registration file hash and a hash of the target rows.
    v003 D8: every computable hash (target rows, actual and registered file sha) is echoed on EVERY
    refusal path. The headline also carries n_members_invalid, query_manifest_role,
    query_manifest_is_program_pin and calibration_record_bound.
    D5: reports every member's LADDER row table and within-error count over all 43 (invalid never
    passes); headline = distribution of PRIMARY member counts + the frozen reference member. The
    pointwise envelope and the box-limited sensitivity band are reported separately and labelled.
    target_rows: 43 dicts {'id', 'velocity', 'sigma'} in manifest order. Writes nothing.
    """
    reasons = []
    out = {'ok': False, 'refused': True, 'n_rows': N_QUERIES, 'error_model': ERROR_MODEL,
           'within_error_rule': WITHIN_ERROR_RULE, 'headline_rule': HEADLINE_RULE,
           'manifest_file_sha256_expected': None, 'manifest_file_sha256_actual': None,
           'manifest_file_sha256_registered': None, 'query_manifest_role': None,
           'manifest_sha256_self': None, 'registration_file_sha256': None, 'target_rows_sha256': None,
           'freeze_status': None, 'incomplete_reasons': None, 'headline': None, 'members': [],
           'pointwise_envelope': None, 'sensitivity': None, 'alternatives': [], 'stage0_status': None,
           'reasons': reasons}
    # D8 (v003): every hash that can be computed is echoed on EVERY path, refusals included. Hashing the
    # supplied rows and the manifest bytes is harmless; nothing is parsed before the identity checks.
    try:
        out['target_rows_sha256'] = _sha256_hex(_canonical_bytes(target_rows))
    except (ValueError, TypeError, RecursionError):
        out['target_rows_sha256'] = None
        reasons.append('NOTE target_rows are not canonically serialisable; target_rows_sha256 is None')
    if isinstance(expected_manifest_file_sha256, str):
        out['manifest_file_sha256_expected'] = expected_manifest_file_sha256.lower()
    raw = None
    if isinstance(freeze_manifest_path, str) and freeze_manifest_path:
        raw, _real, raw_err = _read_regular(freeze_manifest_path, True)
        if raw is not None:
            out['manifest_file_sha256_actual'] = _sha256_hex(raw)
    else:
        raw_err = 'freeze_manifest_path must be a non-empty string'
    reg = _verify_registration_impl(registration_path)
    out['registration_file_sha256'] = reg['registration_file_sha256']
    out['manifest_file_sha256_registered'] = reg.get('expected_manifest_file_sha256')
    if not reg['ok']:
        reasons.append('REFUSED: registration file did not verify')
        reasons.extend(reg['reasons'])
        return out
    if not _is_hex64(expected_manifest_file_sha256):
        reasons.append('REFUSED: expected_manifest_file_sha256 must be a 64-character hex string')
        return out
    expected = expected_manifest_file_sha256.lower()
    if expected != reg['expected_manifest_file_sha256']:
        reasons.append('REFUSED: expected_manifest_file_sha256 %s differs from the registered %s'
                       % (expected, reg['expected_manifest_file_sha256']))
        return out
    if raw is None:
        reasons.append('REFUSED: %s' % raw_err)
        return out
    actual = out['manifest_file_sha256_actual']
    if actual != expected:
        reasons.append('REFUSED (D8): manifest file sha256 %s differs from the registered %s (edited or '
                       'different manifest)' % (actual, expected))
        return out
    vout = {'manifest_sha256_recomputed': None, 'manifest_sha256_recorded': None, 'canonical_bytes_match': None,
            'pins_verified': []}
    vreasons = []
    doc = _verify_bytes(raw, freeze_manifest_path, vout, vreasons)
    out['manifest_sha256_self'] = vout.get('manifest_sha256_recorded')
    if doc is None:
        reasons.append('REFUSED: freeze manifest did not verify')
        reasons.extend(vreasons)
        return out
    out['manifest_sha256_self'] = doc['manifest_sha256']
    if doc['manifest_sha256'] != reg['manifest_sha256_self']:
        reasons.append('REFUSED: manifest self-hash differs from the registered one')
        return out
    ids = list(doc['query_ids'])
    try:
        external = _root_rosters_for_alternatives(row_registration_rosters, doc['alternatives'], ids)
        if {name: roster['pin'] for name, roster in external.items()} != doc['row_registration_rosters']:
            raise ValueError('external root pins differ from frozen root pins')
    except (ValueError, TypeError, KeyError) as exc:
        reasons.append('ROOT_ROSTER_SCORE_BINDING_REFUSED: ' + str(exc))
        return out
    if not isinstance(target_rows, (list, tuple)) or len(target_rows) != N_QUERIES:
        reasons.append('REFUSED: target_rows must be a list of exactly %d rows' % N_QUERIES)
        return out
    bound = []
    for i, row in enumerate(target_rows):
        where = 'target_rows[%d]' % i
        if not isinstance(row, dict) or set(row) != TARGET_ROW_KEYS:
            reasons.append('%s must be a dict with exactly keys id, velocity, sigma' % where)
            continue
        if row['id'] != ids[i]:
            reasons.append('%s id %r does not match manifest query_ids[%d] %r' % (where, row['id'], i, ids[i]))
        if not _is_real(row['velocity']):
            reasons.append('%s.velocity is not a finite real' % where)
        if not _is_real(row['sigma']) or float(row['sigma']) <= 0.0:
            reasons.append('%s.sigma is not a finite real > 0' % where)
        if not reasons:
            bound.append((float(row['velocity']), float(row['sigma'])))
    if reasons:
        reasons.insert(0, 'REFUSED: target_rows rejected')
        return out
    out['freeze_status'] = doc['freeze_status']
    out['incomplete_reasons'] = list(doc['incomplete_reasons'])
    out['query_manifest_role'] = doc['input_bindings']['query_manifest']['role']
    if not doc['input_bindings']['query_manifest']['is_program_pin']:
        reasons.append('NOTE query manifest role SYNTHETIC_FIXTURE: this is not the program NGC3198 manifest '
                       '(a2936517...); the result is not a 120/43 score')
    ar = doc['admitted_region']
    members = _score_members(doc['members'], ids, bound)
    out['members'] = members
    ref_id = doc['reference_member']['member_id']
    ref = next(m for m in members if m['member_id'] == ref_id)
    counts = [m['within_error_count'] for m in members]
    out['headline'] = {
        'statistic': 'DISTRIBUTION_OF_MEMBER_WITHIN_ERROR_COUNTS_PLUS_REFERENCE_MEMBER',
        'alternative': doc['alternatives']['primary'],
        'n_rows': N_QUERIES,
        'n_members': len(members),
        'n_members_evaluated': sum(1 for m in members if m['evaluated']),
        'n_members_valid': sum(1 for m in members if m['member_valid']),
        'member_within_error_counts': _distribution(counts),
        'member_within_error_counts_valid_members_only': _distribution(
            [m['within_error_count'] for m in members if m['member_valid']]),
        'counts_by_member': {m['member_id']: m['within_error_count'] for m in members},
        'reference_member_id': ref_id,
        'reference_member_log_index': ref['log_index'],
        'reference_within_error_count': ref['within_error_count'],
        'reference_invalid_count': ref['invalid_count'],
        'freeze_status': doc['freeze_status'],
        'admitted_set_label': ar['admitted_set_label'],
        'region_possibly_truncated': ar['region_possibly_truncated'],
        'n_members_invalid': sum(1 for m in members if m['evaluated'] and not m['member_valid']),
        'query_manifest_role': doc['input_bindings']['query_manifest']['role'],
        'query_manifest_is_program_pin': doc['input_bindings']['query_manifest']['is_program_pin'],
        'calibration_record_bound': doc['input_bindings']['calibration_record'] is not None,
        'band_scope': doc['band_scope'],
        'note': ('unevaluated or invalid rows count as not within error; no pointwise or median curve is '
                 'a headline'),
    }
    S = _build_spec(doc['coordinates'], [])   # verified above; v003b: labels follow the coordinate mode
    env_label, sens_label, _bs = _mode_labels(S)
    if S['coordinate_mode'] == MODE_D_FIXED:
        out['headline']['band_condition'] = A13_CONDITION
        out['headline']['headline_conditions'] = doc[HEADLINE_CONDITIONS_KEY]
    erows, eov, einv = _band_rows(doc['pointwise_envelope'], 'band_low_km_s', 'band_high_km_s', ids, bound)
    out['pointwise_envelope'] = {'label': env_label, 'rows': erows, 'band_overlap_count': eov,
                                 'invalid_count': einv, 'headline': False}
    sens = doc['sensitivity']
    srows, sov, sinv = _band_rows(sens['per_query'], 'box_limited_band_low_km_s', 'box_limited_band_high_km_s',
                                  ids, bound)
    for r, pq in zip(srows, sens['per_query']):
        r['reference_speed_km_s'] = pq['reference_speed_km_s']
        r['max_abs_delta_km_s'] = pq['max_abs_delta_km_s']
    out['sensitivity'] = {'label': sens_label, 'status': sens['status'], 'rows': srows,
                          'band_overlap_count': sov, 'invalid_count': sinv, 'headline': False,
                          'conditional_on_trial_values': doc['conditional_on_trial_values']}
    alts = []
    for a in doc['alternatives']['declared']:
        rec = {'name': a['name'], 'kind': a['kind'], 'status': a['status'],
               'role': 'PRIMARY' if a['name'] == doc['alternatives']['primary'] else 'NON_PRIMARY'}
        score_scope = _alternative_score_scope(a, ids, external[a['name']])
        if score_scope is not None:
            rec['scoring_scope'] = score_scope
        if rec['role'] == 'PRIMARY':
            rec.update({'scored': True, 'headline': True})
        elif a['status'] == ALT_EVALUATED:
            alternative_members = doc['alternative_results'][a['name']]['members']
            am = (_score_members_on_rows(alternative_members, ids, bound, score_scope['query_ids'])
                  if score_scope is not None else _score_members(alternative_members, ids, bound))
            rec.update({'scored': True, 'headline': False,
                        'member_within_error_counts': _distribution([m['within_error_count'] for m in am]),
                        'members': am,
                        'member_evaluation_status':
                            doc['alternative_results'][a['name']]['member_evaluation']['status']})
        else:
            rec.update({'scored': False, 'headline': False,
                        'note': 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline'})
        alts.append(rec)
    if S['coordinate_mode'] == MODE_D_FIXED:   # v003b (A13): the recorded distance alternative, never scored
        for a in doc[HEADLINE_CONDITIONS_KEY]['recorded_alternatives']:
            alts.append({'name': a['name'], 'kind': a['kind'], 'status': a['status'], 'role': 'NON_PRIMARY',
                         'scored': False, 'headline': False,
                         'note': 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline (A13)'})
    out['alternatives'] = alts
    out['stage0_status'] = doc['stage0_status']   # STAGE0 successor (M-14): the frozen receipt-rule record
    out['refused'] = False
    out['ok'] = True
    return out
