"""calibration_region_engine_c2v003a -- Module 1, version 003a (Claude2 lane).

v003a (CHECK_V001 X1, line map in DELTA_V003_V003A.md): write_calibration_record and
verify_calibration_record RECOMPUTE the exploration fingerprint from the run content (exploration.admitted_points
and region.sha256) instead of copying run['exploration_fingerprint']; a run whose reported fingerprint is set
and differs from the recomputed one is refused. Everything else is v003 (sha256 ec509648...51fcc7).

Successor of calibration_region_engine_c2v002 (sha256 248ba5f9...c994c02e05), itself the successor of
calibration_region_engine_c3v001 (sha256 f5613832...0e84e0b).

v003 changes (line map in DELTA_V002_V003.md):
  * S1: every linear-algebra call is preceded by a finite/magnitude guard (_numeric_guard); a scaled
    Jacobian outside the safe range is refused with a NUMERIC_RANGE reason and the run ends
    NUMERIC_RANGE_REFUSED. The simplex and the Lawson loop carry iteration and wall-clock guards; the
    march carries a doubling guard.
  * S2: the linearised repair stays inside span(identified): a step that would leave the box is
    truncated in length (never clipped component-wise), so near-null directions keep the anchor's
    values. The v002 'numerical_rank' repair phase (which moved near-null directions) is removed.
  * S3: identification = relative rule (with an enforced minimum tolerance) OR an absolute rule
    s_i >= z (z = Bonferroni constant 2.865260238532134: a full-box move changes the sigma-scaled
    12-vector by at least one rectangle half-width); identified_by and flags are reported.
  * S4: a clipped Jacobian side shorter than min_step is dropped (one-sided difference reusing f0)
    instead of evaluating a near-duplicate of the seed.
  * S5: identifiability reports are content-checked against the S3 rule.
  * S6: one validity predicate in both modules: ``x is True`` (np.True_ is not True).
  * S10: every public function is wrapped fail-closed (unanticipated exceptions -> ok=False).
  * P34-11: every march side records its boundary cause.
  * P34-15/P34-16: write_calibration_record / verify_calibration_record write a canonical, self-hashed,
    exclusive-create record of EVERY run (any status) and append it to a hash-chained registry; the
    run output carries an exploration_fingerprint that the freeze module recomputes.

v002 description (kept):
DDO154 calibration-region
engine: finite-difference Jacobian at a root-supplied seed, SVD identifiability report, deterministic
exploration of the admitted region (log scan, linearised repair, directional march + bisection, local
Halton design, coarse global design over the computational box, iterated marches) and the
orchestrating ``run_calibration_region``.

What changed against v001 (details and line map in ENGINE_DELTA_NOTES.md):
  * A1: emptiness is never asserted. Outcomes are COMPLETE / BUDGET_EXHAUSTED / NO_ADMITTED_POINT_FOUND
    (emptiness not proven) / NO_VALID_EVALUATION; ``empty_region`` is never True (False when an admitted
    witness exists, None otherwise). The whole evaluation log (seed, Jacobian, repair, march, bisection,
    design, global design) is scanned for admitted entries; every admitted entry is in the admitted set
    and is a candidate march anchor.
  * A2: ``_edge_t`` treats |d_j| <= _BOX_TOL as zero and uses the _BOX_TOL face slack.
  * D7: iterated marches from extreme admitted points until the hull box stops growing
    (``hull_growth_tol``), coarse global Halton design over the computational box, admitted set
    labelled INNER_SAMPLE, ``region_possibly_truncated`` flag with explicit causes.
  * D10 (engine part): every coordinate carries ``units`` and a ``scope`` ('shared' | 'DDO154');
    DDO154-scoped coordinates (its own distance/inclination nuisances) are removed by ``shared_theta``;
    the DDO154 distance box is bound to the region file's ``distance_summary``; the identifiability
    report completes the null space explicitly when coordinates exceed the 12 rows.
  * Review should-fix items (E1/E2/E3 slices of review_0462_0464) on the engine side.

Conventions (unchanged from v001):
  * inert at import: no file I/O, no computation, no environment changes;
  * every public function takes keyword-only arguments with no defaults and returns a dict with at least
    ``ok: bool`` and ``reasons: list[str]``; anticipated bad input returns ``ok=False`` and never raises;
  * exceptions raised by the root-supplied ``forward`` callable are caught, logged and treated as invalid;
  * no numpy object escapes: all returned arrays are plain lists of floats;
  * single-threaded numerics; the module never spawns threads or processes;
  * only DDO154 calibration rows are read; no other galaxy's data is read, referenced or needed.

Standard library + numpy only (no scipy).
"""

import copy
import datetime
import functools
import hashlib
import inspect
import json
import math
import os
import stat
import time

import numpy as np

__all__ = [
    'load_observation_region',
    'make_coordinate_spec',
    'to_natural',
    'to_unit',
    'shared_theta',
    'ddo154_distance_box',
    'direction_box_extent',
    'classify_prediction',
    'finite_difference_jacobian',
    'identifiability_report',
    'explore_region',
    'run_calibration_region',
    'exploration_fingerprint',
    'write_calibration_record',
    'verify_calibration_record',
]

MODULE_NAME = 'calibration_region_engine_c2v003a'
PREDECESSOR = ('calibration_region_engine_c2v003 sha256 ec509648cd7324692fac57d1c710e261555b540c82dddec72aa2384fff51fcc7; '
               'calibration_region_engine_c2v002 sha256 248ba5f909adfce589b11e6e52227b5ce182edd3ce01317b1d063fd994c02e05; '
               'calibration_region_engine_c3v001 sha256 f5613832fcb6e452b4490d56453cce37fb8846e802442407e794f80a6ec84e0b')
CALIBRATION_RECORD_SCHEMA = 'CALIBRATION_RUN_RECORD_C2V003'
CALIBRATION_REGISTRY_SCHEMA = 'CALIBRATION_RUN_REGISTRY_LINE_C2V003'
FINGERPRINT_SCHEMA = 'EXPLORATION_FINGERPRINT_C2V003'
# S3: absolute identification threshold = the Bonferroni constant of the frozen DDO154 rule
# z = Phi^-1(1 - 0.05/24): a full-box move along a direction with s_i >= z changes the sigma-scaled
# 12-vector by at least one rectangle half-width.
ABSOLUTE_IDENTIFICATION_THRESHOLD = 2.865260238532134
IDENTIFICATION_RULE = ('identified iff (s_i > 0 and s_i >= effective_null_tolerance * s_max) or '
                       's_i >= ABSOLUTE_IDENTIFICATION_THRESHOLD (z = 2.865260238532134); '
                       'effective_null_tolerance = max(null_tolerance, MIN_NULL_TOLERANCE, max(m, n) * eps); '
                       'singular values are per unit of u, i.e. per computational box (box-dependent)')
MIN_NULL_TOLERANCE = 1e-6
# P34-11: why a march side stopped (recorded per side; round 0 also in exploration.boundary_cause)
BOUNDARY_CAUSES = {
    'REJECTED_EVALUATION': 'a valid evaluation outside the closed rectangle stopped the march (then bisected)',
    'INVALID_EVALUATION': 'an invalid evaluation stopped the march (then bisected); not evidence of rejection',
    'REJECTED_EVALUATION_AT_BOX_EDGE': 'the exact box-edge evaluation was valid and rejected (then bisected)',
    'INVALID_EVALUATION_AT_BOX_EDGE': 'the exact box-edge evaluation was invalid (then bisected)',
    'COMPUTATIONAL_BOX_EDGE_ADMITTED': 'the exact box-edge evaluation was admitted: the side is limited by the '
                                       'computational box, not by the data',
    'COMPUTATIONAL_BOX_EDGE_AT_LAST_ADMITTED': 'the last admitted point already lies on the box edge',
    'COMPUTATIONAL_BOX_FACE_NO_EVALUATION': 'the anchor lies on a box face with an outward direction: no '
                                            'evaluation, limited by the computational box',
    'DOUBLING_GUARD': 'the doubling guard stopped the march (S1)',
    'UNFINISHED': 'the side did not finish (budget exhausted)',
}
BOUNDS_SEMANTICS = 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'
NGC3198_ACCESS = 'NONE'
PURPOSES = ('seed', 'jacobian', 'repair', 'march', 'bisection', 'design', 'global_design')
EXPECTED_ROW_COUNT = 12
REGION_ROW_FIELDS = (
    'id',
    'reference_radius_kpc',
    'observed_speed_km_s',
    'quoted_random_sigma_km_s',
    'conditional_random_acceptance_low_km_s',
    'conditional_random_acceptance_high_km_s',
)
REGION_TOP_FIELDS = ('statistical_choice', 'distance_summary', 'forward_coordinates')
TRANSFORMS = ('log', 'linear')
ROLES = ('free', 'fixed', 'nuisance')
SCOPES = ('shared', 'DDO154')
SCOPE_ALIASES = {'ddo154_nuisance': 'DDO154'}   # spelling used by prediction_freeze_c2v002
FOREIGN_SCOPES = ('ngc3198_nuisance',)          # another galaxy's own nuisance slots: never enter this engine
SENSITIVITY_MODES = ('NONE', 'BOX_ENDS')   # or {'step_natural': positive float}
ADMITTED_SET_LABEL = 'INNER_SAMPLE'
ADMITTED_SET_STATEMENT = ('INNER_SAMPLE: the admitted points are the evaluated points found admitted by a '
                          'budgeted deterministic search; they are a subset of the admitted region, not its '
                          'boundary, and hull_box is a box over these points, not the region.')
U_SEMANTICS = 'u in [0,1] per varying coordinate: dimensionless fraction of the computational trial box in x'
SINGULAR_VALUE_UNITS = 'sigma-scaled speed (dimensionless, per row sigma) per unit of u (fraction of computational box)'
DISTANCE_BOX_SEMANTICS = ('COMPUTATIONAL_BOX_FROM_REPORTED_CONDITIONAL_68_DISTANCE_SUMMARY_'
                          'NOT_HARD_PHYSICAL_SUPPORT')
EXPLORE_STATUSES = ('COMPLETE', 'BUDGET_EXHAUSTED', 'NO_ADMITTED_POINT_FOUND', 'NO_VALID_EVALUATION')

_BOX_TOL = 1e-12   # tolerance for the "inside [0,1]^n" test; also the _edge_t zero/face slack (A2)
_U_TOL = 1e-9      # tolerance when converting natural -> unit (rounding at the box faces)
_T_TOL = 1e-9      # tolerance on march parameter comparisons
_ZERO_STEP = 1e-15  # a repair displacement below this is "no displacement"
_FACE_TOL = 1e-9   # an admitted u_j within this of 0 or 1 lies on a computational-box face
_SLICE_TOL = 1e-12  # |near-null projection difference| above this means "off the anchor slice"
_ORTHO_TOL = 1e-9  # orthonormality / consistency tolerance for identifiability reports
_REPAIR_RANK_RTOL = 1e-9  # second repair phase uses every direction with s_k > this * s_max
_LAWSON_ITERATIONS = 200  # fixed iteration count of the max-norm (Lawson) repair refinement
_LP_EPS = 1e-12    # simplex pivot / reduced-cost tolerance
_LP_MAX_PIVOTS = 5000
_RAY_DIR_TOL = 1e-9  # two rays whose unit directions agree to this are the same ray
_DIST_MATCH_RTOL = 1e-12  # coordinate box vs distance_summary box, relative
_DIST_CONSISTENCY_RTOL = 1e-9  # distance_summary internal consistency (central vs modulus), relative
_MAX_REL_STEP = 0.5
_LINALG_MAX_ABS = 1e150   # S1: |entries| above this are refused before any numpy.linalg call
_NUMERIC_WALL_SECONDS = 60.0  # S1: wall-clock guard for each pure-numeric loop (simplex, Lawson)
_MAX_MARCH_DOUBLINGS = 64     # S1: doubling guard of one march side


# --------------------------------------------------------------------------
# small validation helpers
# --------------------------------------------------------------------------

class _BudgetExhausted(Exception):
    """Internal control-flow signal for the exploration; never escapes."""


def _fail_closed(fn):
    """S10: an unanticipated exception inside a public function becomes ok=False, never a raise."""
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
            return {'ok': False, 'status': 'INTERNAL_ERROR', 'function': fn.__name__,
                    'reasons': [f'INTERNAL_ERROR (fail-closed): {type(exc).__name__}: {_safe_str(exc)}']}
    return wrapper


def _numeric_guard(arr, label):
    """S1: [] if arr is finite with every |entry| <= _LINALG_MAX_ABS, else [reason]. Never raises."""
    try:
        a = np.asarray(arr, dtype=float)
    except Exception as exc:
        return [f'NUMERIC_RANGE: {label} is not a float array ({type(exc).__name__})']
    if a.size == 0:
        return []
    if not np.all(np.isfinite(a)):
        return [f'NUMERIC_RANGE: {label} has non-finite entries; refused before linear algebra']
    mx = float(np.max(np.abs(a)))
    if mx > _LINALG_MAX_ABS:
        return [f'NUMERIC_RANGE: {label} max |entry| {mx:.3e} exceeds {_LINALG_MAX_ABS:.0e}; refused before '
                f'linear algebra (overflow guard)']
    return []


def _jsonable(obj, where='$'):
    """P34-15: JSON-native deep copy with every dict key a str (int keys -> str), non-finite floats as the
    strings 'inf'/'-inf'/'nan'. Keys therefore sort as strings both before and after a parse."""
    if obj is None or isinstance(obj, (bool, str)):
        return obj
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, (int, np.integer)):
        return int(obj)
    if isinstance(obj, (float, np.floating)):
        v = float(obj)
        if math.isfinite(v):
            return v
        return 'nan' if math.isnan(v) else ('inf' if v > 0 else '-inf')
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(k, str):
                ks = k
            elif isinstance(k, (int, np.integer)) and not isinstance(k, (bool, np.bool_)):
                ks = str(int(k))
            else:
                raise ValueError(f'non-string, non-integer key at {where}: {_safe_str(k)}')
            if ks in out:
                raise ValueError(f'duplicate key after str normalisation at {where}: {ks!r}')
            out[ks] = _jsonable(v, where + '.' + ks)
        return out
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v, f'{where}[{i}]') for i, v in enumerate(obj)]
    if isinstance(obj, np.ndarray):
        return _jsonable(obj.tolist(), where)
    raise ValueError(f'non-JSON type at {where}: {type(obj).__name__}')


def _canonical_bytes(obj):
    """Canonical JSON bytes: keys normalised to str first (P34-15), sorted, compact, no NaN."""
    return json.dumps(_jsonable(obj), sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def _safe_str(x):
    """str(x) that never raises (review E1-N2)."""
    try:
        return str(x)
    except Exception:
        try:
            return f'<unprintable {type(x).__name__}>'
        except Exception:
            return '<unprintable>'


def _is_bool(x):
    return isinstance(x, (bool, np.bool_))


def _is_number(x):
    return (not _is_bool(x)) and isinstance(x, (int, float, np.integer, np.floating))


def _finite_float(x):
    """float(x) if x is a finite real number (not bool), else None."""
    if not _is_number(x):
        return None
    try:
        v = float(x)
    except Exception:
        return None
    if not math.isfinite(v):
        return None
    return v


def _is_int(x):
    return (not _is_bool(x)) and isinstance(x, (int, np.integer))


def _is_true(x):
    """S6: the single validity predicate shared with prediction_freeze_c2v003: ``x is True`` only
    (np.True_, 1, 'True' are not True)."""
    return x is True


def _is_hex64(s):
    if not isinstance(s, str) or len(s) != 64:
        return False
    return all(c in '0123456789abcdefABCDEF' for c in s)


def _floats(seq):
    return [float(v) for v in seq]


def _matrix(arr):
    return [[float(v) for v in row] for row in arr]


def _x_of(transform, v):
    return math.log(v) if transform == 'log' else float(v)


def _v_of(transform, x):
    return math.exp(x) if transform == 'log' else float(x)


def _internal_units(transform, units):
    return f'ln({units})' if transform == 'log' else units


def _normalise_sensitivity(sens):
    """Return (reasons, normalised) for a sensitivity declaration.

    Accepted: 'NONE' | 'BOX_ENDS' | {'step_natural': x}, and the prediction_freeze_c2v002 spellings
    None | {'mode': 'box_ends'} | {'mode': 'step', 'step': x}. Normalised to the first set.
    """
    if sens is None:
        return [], 'NONE'
    if isinstance(sens, dict) and 'mode' in sens:
        if sens.get('mode') == 'box_ends' and set(sens.keys()) == {'mode'}:
            return [], 'BOX_ENDS'
        if sens.get('mode') == 'step' and set(sens.keys()) == {'mode', 'step'}:
            st = _finite_float(sens['step'])
            if st is not None and st > 0:
                return [], {'step_natural': st}
        return ['sensitivity {"mode": ...} must be {"mode": "box_ends"} or {"mode": "step", "step": >0}'], None
    if isinstance(sens, str):
        if sens in SENSITIVITY_MODES:
            return [], sens
        return [f'sensitivity must be one of {SENSITIVITY_MODES} or {{"step_natural": positive float}}'], None
    if isinstance(sens, dict):
        if set(sens.keys()) != {'step_natural'}:
            return ['sensitivity dict must have exactly the key "step_natural"'], None
        st = _finite_float(sens['step_natural'])
        if st is None or not (st > 0):
            return ['sensitivity.step_natural must be a finite positive number'], None
        return [], {'step_natural': st}
    return [f'sensitivity must be one of {SENSITIVITY_MODES} or {{"step_natural": positive float}}'], None


def _validate_coordinate(label, transform, lower, upper, trial_value, role, units, scope, sensitivity):
    """Validate one coordinate. Returns (reasons, normalised_sensitivity, normalised_scope)."""
    reasons = []
    if isinstance(scope, str) and scope in FOREIGN_SCOPES:
        return [f'{label}: scope {scope!r} is another galaxy\'s nuisance slot; it must not be passed to the '
                f'DDO154 calibration engine (D10)'], None, None
    if isinstance(scope, str) and scope in SCOPE_ALIASES:
        scope = SCOPE_ALIASES[scope]
    # isinstance guards first: ndarray/other objects must not reach the `in` tests (review E1-F8/N3)
    if not isinstance(transform, str) or transform not in TRANSFORMS:
        reasons.append(f'{label}: transform must be one of {TRANSFORMS} (a str)')
    if not isinstance(role, str) or role not in ROLES:
        reasons.append(f'{label}: role must be one of {ROLES} (a str)')
    if not isinstance(units, str) or not units.strip():
        reasons.append(f'{label}: units must be a non-empty str (D10: every coordinate carries units)')
    if not isinstance(scope, str) or scope not in SCOPES:
        reasons.append(f'{label}: scope must be one of {SCOPES} (a str)')
    rs, sens = _normalise_sensitivity(sensitivity)
    reasons.extend(f'{label}: {r}' for r in rs)
    lo = _finite_float(lower)
    hi = _finite_float(upper)
    tv = _finite_float(trial_value)
    if lo is None or hi is None:
        reasons.append(f'{label}: lower and upper must be finite numbers')
    if tv is None:
        reasons.append(f'{label}: trial_value must be a finite number')
    if reasons:
        return reasons, None, None
    if transform == 'log' and not (0.0 < lo < hi):
        reasons.append(f'{label}: log transform requires 0 < lower < upper')
    elif transform == 'linear' and not (lo < hi):
        reasons.append(f'{label}: linear transform requires lower < upper')
    if not (lo <= tv <= hi):
        reasons.append(f'{label}: trial_value must lie in [lower, upper]')
    if role == 'free' and scope != 'shared':
        reasons.append(f'{label}: a free coordinate is a shared constant and must have scope "shared"')
    if role == 'nuisance' and scope != 'DDO154':
        reasons.append(f'{label}: a nuisance coordinate of this engine is a DDO154 nuisance and must have '
                       f'scope "DDO154" (D10: other galaxies carry their own nuisance slots)')
    if role != 'fixed' and sens != 'NONE':
        reasons.append(f'{label}: sensitivity declarations apply to fixed coordinates only (varying '
                       f'coordinates are covered by the admitted members and the null directions)')
    if role == 'fixed' and scope == 'DDO154' and sens != 'NONE':
        reasons.append(f'{label}: a DDO154-scoped fixed coordinate never reaches another galaxy forward; '
                       f'its sensitivity must be "NONE"')
    if isinstance(sens, dict) and not reasons:
        st = sens['step_natural']
        if not (lo <= tv - st and tv + st <= hi):
            reasons.append(f'{label}: trial_value +/- sensitivity.step_natural must lie in [lower, upper]')
    return reasons, sens, (scope if not reasons else None)


def _check_spec(spec):
    """Re-validate a coordinate spec dict. Returns (reasons, info) with info None on failure."""
    if not isinstance(spec, dict) or not _is_true(spec.get('ok')):
        return ['spec must be an ok=True dict produced by make_coordinate_spec'], None
    reasons = []
    names = spec.get('names')
    varying = spec.get('varying_names')
    fixed = spec.get('fixed_names')
    for label, val in (('names', names), ('varying_names', varying), ('fixed_names', fixed)):
        if not isinstance(val, list) or not all(isinstance(s, str) for s in val):
            reasons.append(f'spec.{label} must be a list of str')
    if reasons:
        return reasons, None
    if not names or len(set(names)) != len(names):
        reasons.append('spec.names must be non-empty and unique')
    if sorted(varying + fixed) != sorted(names) or (set(varying) & set(fixed)):
        reasons.append('spec.varying_names and spec.fixed_names must partition spec.names')
    if [nm for nm in names if nm in set(varying)] != varying:
        reasons.append('spec.varying_names must follow spec.names order')
    if not varying:
        reasons.append('spec must have at least one varying coordinate')
    for key in ('roles', 'transforms', 'lower', 'upper', 'trial_values', 'units', 'scopes', 'sensitivity'):
        d = spec.get(key)
        if not isinstance(d, dict) or any(nm not in d for nm in names):
            reasons.append(f'spec.{key} must be a dict keyed by every coordinate name')
    if reasons:
        return reasons, None
    coords = {}
    for nm in names:
        tr = spec['transforms'][nm]
        role = spec['roles'][nm]
        lo, hi, tv = spec['lower'][nm], spec['upper'][nm], spec['trial_values'][nm]
        rs, sens, scope_n = _validate_coordinate(f'coordinate {nm!r}', tr, lo, hi, tv, role, spec['units'][nm],
                                                 spec['scopes'][nm], spec['sensitivity'][nm])
        if rs:
            reasons.extend(rs)
            continue
        is_varying = nm in set(varying)
        if (role == 'fixed') == is_varying:
            reasons.append(f'coordinate {nm!r}: role {role!r} inconsistent with varying/fixed lists')
            continue
        coords[nm] = {
            'transform': tr, 'role': role, 'units': spec['units'][nm], 'scope': scope_n,
            'sensitivity': sens,
            'lower': float(lo), 'upper': float(hi), 'trial_value': float(tv),
            'x_lo': _x_of(tr, float(lo)), 'x_hi': _x_of(tr, float(hi)),
            'x_trial': _x_of(tr, float(tv)),
        }
    if reasons:
        return reasons, None
    info = {
        'names': list(names),
        'varying': list(varying),
        'fixed': list(fixed),
        'n': len(varying),
        'coords': coords,
        'x_lo': np.array([coords[nm]['x_lo'] for nm in varying], dtype=float),
        'x_hi': np.array([coords[nm]['x_hi'] for nm in varying], dtype=float),
        'trial_u': np.array([(coords[nm]['x_trial'] - coords[nm]['x_lo']) / (coords[nm]['x_hi'] - coords[nm]['x_lo'])
                             for nm in varying], dtype=float),
    }
    return [], info


def _check_region(region):
    """Re-validate a region dict (from load_observation_region). Returns reasons list."""
    if not isinstance(region, dict) or not _is_true(region.get('ok')):
        return ['region must be an ok=True dict produced by load_observation_region']
    reasons = []
    row_ids = region.get('row_ids')
    if not isinstance(row_ids, list) or not row_ids or not all(isinstance(r, str) and r for r in row_ids):
        return ['region.row_ids must be a non-empty list of str']
    if len(set(row_ids)) != len(row_ids):
        reasons.append('region.row_ids must be unique')
    rect = region.get('rectangles')
    sig = region.get('sigmas')
    if not isinstance(rect, dict) or not isinstance(sig, dict):
        return reasons + ['region.rectangles and region.sigmas must be dicts']
    for rid in row_ids:
        r = rect.get(rid)
        if not isinstance(r, (list, tuple)) or len(r) != 2:
            reasons.append(f'region.rectangles[{rid!r}] must be [low, high]')
            continue
        lo, hi = _finite_float(r[0]), _finite_float(r[1])
        if lo is None or hi is None or not (lo <= hi):
            reasons.append(f'region.rectangles[{rid!r}] must be finite with low <= high')
        s = _finite_float(sig.get(rid))
        if s is None or not (s > 0):
            reasons.append(f'region.sigmas[{rid!r}] must be a finite positive number')
    return reasons


def _check_unit_vector(u, n, label):
    """Validate a unit-coordinate list; returns (reasons, np.array or None)."""
    if isinstance(u, np.ndarray):
        u = u.tolist()
    if not isinstance(u, (list, tuple)):
        return [f'{label} must be a list over the varying coordinates'], None
    if len(u) != n:
        return [f'{label} must have length {n} (number of varying coordinates), got {len(u)}'], None
    vals = []
    for j, x in enumerate(u):
        v = _finite_float(x)
        if v is None:
            return [f'{label}[{j}] must be a finite number'], None
        if v < -_BOX_TOL or v > 1.0 + _BOX_TOL:
            return [f'{label}[{j}] = {v!r} lies outside the unit box [0, 1]'], None
        vals.append(min(1.0, max(0.0, v)))
    return [], np.array(vals, dtype=float)


def _nonneg_int(x, label):
    if not _is_int(x) or x < 0:
        return [f'{label} must be a non-negative integer']
    return []


def _positive_float(x, label):
    v = _finite_float(x)
    if v is None or not (v > 0):
        return [f'{label} must be a finite positive number']
    return []


def _nonneg_float(x, label):
    v = _finite_float(x)
    if v is None or not (v >= 0):
        return [f'{label} must be a finite non-negative number']
    return []


# --------------------------------------------------------------------------
# observation region
# --------------------------------------------------------------------------

@_fail_closed
def load_observation_region(*, path, expected_sha256):
    """Load the frozen DDO154 observation-region file after verifying its byte hash.

    Binds exactly rows[].id, reference_radius_kpc, observed_speed_km_s,
    quoted_random_sigma_km_s, conditional_random_acceptance_low_km_s,
    conditional_random_acceptance_high_km_s, statistical_choice,
    distance_summary, forward_coordinates. Does not alter the rule.
    """
    out = {
        'ok': False, 'sha256': None, 'path': None, 'n_rows': 0, 'row_ids': [],
        'rectangles': {}, 'sigmas': {}, 'observed': {}, 'reference_radius_kpc': {},
        'statistical_choice': None, 'distance_summary': None, 'forward_coordinates': None,
        'bound_row_fields': list(REGION_ROW_FIELDS), 'bound_top_fields': list(REGION_TOP_FIELDS),
        'units': {'reference_radius_kpc': 'kpc', 'observed_speed_km_s': 'km/s', 'sigmas': 'km/s',
                  'rectangles': 'km/s'},
        'reasons': [],
    }
    reasons = out['reasons']
    if not isinstance(path, str) or not path:
        reasons.append('path must be a non-empty str')
        return out
    if not _is_hex64(expected_sha256):
        reasons.append('expected_sha256 must be a 64-character hexadecimal str')
        return out
    try:
        with open(path, 'rb') as fh:
            raw = fh.read()
    except Exception as exc:
        reasons.append(f'cannot read observation-region file: {type(exc).__name__}: {_safe_str(exc)}')
        return out
    actual = hashlib.sha256(raw).hexdigest()
    out['sha256'] = actual
    out['path'] = path
    if actual != expected_sha256.lower():
        reasons.append('SHA256 mismatch between file bytes and expected_sha256; file not parsed')
        return out
    try:
        doc = json.loads(raw.decode('utf-8'))
    except Exception as exc:
        reasons.append(f'observation-region file is not valid UTF-8 JSON: {type(exc).__name__}: {_safe_str(exc)}')
        return out
    if not isinstance(doc, dict):
        reasons.append('observation-region JSON top level must be an object')
        return out
    rows = doc.get('rows')
    if not isinstance(rows, list):
        reasons.append("observation-region 'rows' must be a list")
        return out
    if len(rows) != EXPECTED_ROW_COUNT:
        reasons.append(f'expected exactly {EXPECTED_ROW_COUNT} rows, found {len(rows)}')
    row_ids, rectangles, sigmas, observed, radii = [], {}, {}, {}, {}
    for k, row in enumerate(rows):
        if not isinstance(row, dict):
            reasons.append(f'rows[{k}] is not an object')
            continue
        rid = row.get('id')
        if not isinstance(rid, str) or not rid:
            reasons.append(f'rows[{k}].id must be a non-empty str')
            continue
        if rid in rectangles:
            reasons.append(f'rows[{k}]: duplicate row id {rid!r}')
            continue
        vals = {}
        bad = False
        for field in REGION_ROW_FIELDS[1:]:
            v = _finite_float(row.get(field))
            if v is None:
                reasons.append(f'rows[{k}] ({rid}): {field} missing or not a finite number')
                bad = True
            vals[field] = v
        if bad:
            continue
        lo = vals['conditional_random_acceptance_low_km_s']
        hi = vals['conditional_random_acceptance_high_km_s']
        y = vals['observed_speed_km_s']
        sg = vals['quoted_random_sigma_km_s']
        if not (sg > 0):
            reasons.append(f'rows[{k}] ({rid}): quoted_random_sigma_km_s must be > 0')
        if not (lo < y < hi):
            reasons.append(f'rows[{k}] ({rid}): low < observed < high violated')
        row_ids.append(rid)
        rectangles[rid] = [lo, hi]
        sigmas[rid] = sg
        observed[rid] = y
        radii[rid] = vals['reference_radius_kpc']
    for key in REGION_TOP_FIELDS:
        if key not in doc:
            reasons.append(f"missing top-level field '{key}'")
        else:
            out[key] = json.loads(json.dumps(doc[key]))
    if reasons:
        # fail closed: hand out no derived data from a file that fails validation
        for key in REGION_TOP_FIELDS:
            out[key] = None
        return out
    out['row_ids'] = row_ids
    out['n_rows'] = len(row_ids)
    out['rectangles'] = rectangles
    out['sigmas'] = sigmas
    out['observed'] = observed
    out['reference_radius_kpc'] = radii
    out['ok'] = True
    return out


# --------------------------------------------------------------------------
# coordinates
# --------------------------------------------------------------------------

@_fail_closed
def make_coordinate_spec(*, coordinates):
    """Build the coordinate specification from a list of coordinate dicts.

    Each coordinate: {'name', 'transform': 'log'|'linear', 'lower', 'upper',
    'role': 'free'|'fixed'|'nuisance', 'trial_value', 'units': non-empty str,
    'scope': 'shared'|'DDO154', 'sensitivity': 'NONE'|'BOX_ENDS'|{'step_natural': x}}.
    free => scope 'shared'; nuisance => scope 'DDO154' (DDO154's own nuisances); sensitivity other than
    'NONE' only for shared fixed coordinates. Varying coordinates (free + nuisance) keep the given order;
    fixed coordinates stay at trial_value.
    """
    out = {
        'ok': False, 'names': [], 'varying_names': [], 'fixed_names': [], 'nuisance_names': [],
        'free_names': [], 'roles': {}, 'transforms': {}, 'lower': {}, 'upper': {}, 'trial_values': {},
        'units': {}, 'internal_units': {}, 'scopes': {}, 'sensitivity': {},
        'shared_names': [], 'ddo154_scoped_names': [], 'sensitivity_declared_names': [],
        'varying_index': {}, 'n_total': 0, 'n_varying': 0, 'u_semantics': U_SEMANTICS,
        'bounds_semantics': BOUNDS_SEMANTICS, 'reasons': [],
    }
    reasons = out['reasons']
    if not isinstance(coordinates, (list, tuple)) or not coordinates:
        reasons.append('coordinates must be a non-empty list of coordinate dicts')
        return out
    names, varying, fixed, nuisance, free = [], [], [], [], []
    roles, transforms, lower, upper, trial = {}, {}, {}, {}, {}
    units, iunits, scopes, sens = {}, {}, {}, {}
    for k, c in enumerate(coordinates):
        if not isinstance(c, dict):
            reasons.append(f'coordinates[{k}] is not a dict')
            continue
        nm = c.get('name')
        if not isinstance(nm, str) or not nm:
            reasons.append(f'coordinates[{k}].name must be a non-empty str')
            continue
        if nm in roles:
            reasons.append(f'coordinates[{k}]: duplicate name {nm!r}')
            continue
        missing = [f for f in ('transform', 'lower', 'upper', 'role', 'trial_value', 'units', 'scope',
                               'sensitivity') if f not in c]
        if missing:
            reasons.append(f'coordinates[{k}] ({nm}): missing fields {missing}')
            continue
        rs, sn, scope_n = _validate_coordinate(f'coordinates[{k}] ({nm})', c['transform'], c['lower'], c['upper'],
                                               c['trial_value'], c['role'], c['units'], c['scope'],
                                               c['sensitivity'])
        if rs:
            reasons.extend(rs)
            continue
        names.append(nm)
        roles[nm] = c['role']
        transforms[nm] = c['transform']
        lower[nm] = float(c['lower'])
        upper[nm] = float(c['upper'])
        trial[nm] = float(c['trial_value'])
        units[nm] = c['units']
        iunits[nm] = _internal_units(c['transform'], c['units'])
        scopes[nm] = scope_n
        sens[nm] = copy.deepcopy(sn)
        if c['role'] == 'fixed':
            fixed.append(nm)
        else:
            varying.append(nm)
            if c['role'] == 'nuisance':
                nuisance.append(nm)
            else:
                free.append(nm)
    if not reasons and not varying:
        reasons.append('at least one varying (free or nuisance) coordinate is required')
    if reasons:
        return out
    out.update({
        'names': names, 'varying_names': varying, 'fixed_names': fixed, 'nuisance_names': nuisance,
        'free_names': free, 'roles': roles, 'transforms': transforms, 'lower': lower, 'upper': upper,
        'trial_values': trial, 'units': units, 'internal_units': iunits, 'scopes': scopes, 'sensitivity': sens,
        'shared_names': [nm for nm in names if scopes[nm] == 'shared'],
        'ddo154_scoped_names': [nm for nm in names if scopes[nm] == 'DDO154'],
        'sensitivity_declared_names': [nm for nm in names if sens[nm] != 'NONE'],
        'varying_index': {nm: j for j, nm in enumerate(varying)},
        'n_total': len(names), 'n_varying': len(varying), 'ok': True,
    })
    return out


@_fail_closed
def to_natural(*, spec, u):
    """Map unit coordinates u (list over varying coords, in [0,1]) to natural values.

    theta_natural: dict over every coordinate (fixed coordinates at trial_value);
    theta_internal: list over every coordinate in spec.names order (x = ln v for log, v for linear).
    Both x and v are clamped to the box for both transforms (review E1-F5/N4).
    """
    out = {'ok': False, 'theta_natural': None, 'theta_internal': None, 'u': None, 'reasons': []}
    reasons, info = _check_spec(spec)
    if reasons:
        out['reasons'] = reasons
        return out
    rs, uu = _check_unit_vector(u, info['n'], 'u')
    if rs:
        out['reasons'] = rs
        return out
    x_var = info['x_lo'] + uu * (info['x_hi'] - info['x_lo'])
    vidx = {nm: j for j, nm in enumerate(info['varying'])}
    theta_internal, theta_natural = [], {}
    for nm in info['names']:
        c = info['coords'][nm]
        if nm in vidx:
            x = min(c['x_hi'], max(c['x_lo'], float(x_var[vidx[nm]])))
            try:
                v = _v_of(c['transform'], x)
            except (OverflowError, ValueError):
                out['reasons'] = [f'coordinate {nm!r}: natural value out of floating range']
                return out
            v = min(c['upper'], max(c['lower'], v))  # rounding guard at the box faces (both transforms)
        else:
            x = c['x_trial']
            v = c['trial_value']
        if not (math.isfinite(x) and math.isfinite(v)):
            out['reasons'] = [f'coordinate {nm!r}: non-finite value produced']
            return out
        theta_internal.append(x)
        theta_natural[nm] = float(v)
    out.update({'ok': True, 'theta_natural': theta_natural, 'theta_internal': theta_internal,
                'u': _floats(uu)})
    return out


@_fail_closed
def to_unit(*, spec, theta_natural):
    """Map natural values (dict with every varying coordinate) to unit coordinates in [0,1]."""
    out = {'ok': False, 'u': None, 'bounds_semantics': BOUNDS_SEMANTICS, 'reasons': []}
    spec_reasons, info = _check_spec(spec)
    if spec_reasons:
        out['reasons'] = spec_reasons
        return out
    reasons = out['reasons']   # review E1-F1: appends below now reach the output
    if not isinstance(theta_natural, dict):
        reasons.append('theta_natural must be a dict keyed by coordinate name')
        return out
    u = []
    for nm in info['varying']:
        c = info['coords'][nm]
        v = _finite_float(theta_natural.get(nm))
        if v is None:
            reasons.append(f'theta_natural[{nm!r}] missing or not a finite number')
            continue
        if c['transform'] == 'log' and not (v > 0):
            reasons.append(f'theta_natural[{nm!r}] must be > 0 for a log coordinate')
            continue
        x = _x_of(c['transform'], v)
        uj = (x - c['x_lo']) / (c['x_hi'] - c['x_lo'])
        if uj < -_U_TOL or uj > 1.0 + _U_TOL:
            reasons.append(f'theta_natural[{nm!r}] = {v!r} lies outside the computational trial box '
                           f'[{c["lower"]!r}, {c["upper"]!r}]')
            continue
        u.append(min(1.0, max(0.0, float(uj))))
    if reasons:
        return out
    out['u'] = u
    out['ok'] = True
    return out


@_fail_closed
def shared_theta(*, spec, theta_natural):
    """Strip DDO154-scoped coordinates from a natural-value dict (D10).

    Returns theta_shared over spec.shared_names only. DDO154's own nuisances (its distance, inclination)
    and DDO154-scoped fixed values never reach any other galaxy's forward through this helper; the
    other galaxy's own nuisance slots are supplied by the caller, not by this engine.
    """
    out = {'ok': False, 'theta_shared': None, 'shared_names': [], 'excluded_ddo154_names': [],
           'units': {}, 'reasons': []}
    reasons, info = _check_spec(spec)
    if reasons:
        out['reasons'] = reasons
        return out
    if not isinstance(theta_natural, dict):
        out['reasons'] = ['theta_natural must be a dict keyed by coordinate name']
        return out
    shared, excluded, th = [], [], {}
    for nm in info['names']:
        v = _finite_float(theta_natural.get(nm))
        if v is None:
            out['reasons'].append(f'theta_natural[{nm!r}] missing or not a finite number')
            continue
        if info['coords'][nm]['scope'] == 'shared':
            shared.append(nm)
            th[nm] = v
        else:
            excluded.append(nm)
    if out['reasons']:
        return out
    out.update({'ok': True, 'theta_shared': th, 'shared_names': shared, 'excluded_ddo154_names': excluded,
                'units': {nm: info['coords'][nm]['units'] for nm in shared}})
    return out


def _distance_Mpc_of_modulus(mu):
    return 10.0 ** ((float(mu) - 25.0) / 5.0)


def _modulus_of_distance_Mpc(d):
    return 25.0 + 5.0 * math.log10(float(d))


@_fail_closed
def ddo154_distance_box(*, distance_summary, modulus_half_width_multiple):
    """Computational box for DDO154's distance nuisance from the region file's distance_summary (D10).

    distance_summary: {'modulus_mag', 'distance_central_Mpc', 'reported68_low_Mpc', 'reported68_high_Mpc',
    'scope'}. The box is mu_c - k*(mu_c - mu_lo68) .. mu_c + k*(mu_hi68 - mu_c) in distance modulus,
    mapped to Mpc (k = modulus_half_width_multiple; k = 1 returns the reported 68 values exactly).
    Semantics: a computational box from a reported conditional summary, not hard physical support.
    """
    out = {'ok': False, 'lower': None, 'upper': None, 'central': None, 'units': 'Mpc', 'transform': 'log',
           'modulus_mag': None, 'modulus_low_mag': None, 'modulus_high_mag': None,
           'modulus_half_width_multiple': None, 'summary_scope': None,
           'semantics': DISTANCE_BOX_SEMANTICS, 'reasons': []}
    reasons = out['reasons']
    k = _finite_float(modulus_half_width_multiple)
    if k is None or not (k > 0):
        reasons.append('modulus_half_width_multiple must be a finite positive number')
    if not isinstance(distance_summary, dict):
        reasons.append('distance_summary must be a dict (region.distance_summary)')
        return out
    mu = _finite_float(distance_summary.get('modulus_mag'))
    dc = _finite_float(distance_summary.get('distance_central_Mpc'))
    dl = _finite_float(distance_summary.get('reported68_low_Mpc'))
    dh = _finite_float(distance_summary.get('reported68_high_Mpc'))
    for label, val in (('modulus_mag', mu), ('distance_central_Mpc', dc), ('reported68_low_Mpc', dl),
                       ('reported68_high_Mpc', dh)):
        if val is None:
            reasons.append(f'distance_summary.{label} missing or not a finite number')
    if reasons:
        return out
    if not (0.0 < dl < dc < dh):
        reasons.append('distance_summary must satisfy 0 < reported68_low_Mpc < distance_central_Mpc < reported68_high_Mpc')
        return out
    d_mu = _distance_Mpc_of_modulus(mu)
    if abs(d_mu - dc) > _DIST_CONSISTENCY_RTOL * dc:
        reasons.append(f'distance_summary inconsistent: 10**((modulus-25)/5) = {d_mu!r} Mpc differs from '
                       f'distance_central_Mpc = {dc!r} beyond relative {_DIST_CONSISTENCY_RTOL}')
        return out
    mu_lo = _modulus_of_distance_Mpc(dl)
    mu_hi = _modulus_of_distance_Mpc(dh)
    if k == 1.0:
        lower, upper = dl, dh
    else:
        lower = _distance_Mpc_of_modulus(mu - k * (mu - mu_lo))
        upper = _distance_Mpc_of_modulus(mu + k * (mu_hi - mu))
    if not (0.0 < lower < upper) or not (math.isfinite(lower) and math.isfinite(upper)):
        reasons.append('derived distance box is not a finite positive interval')
        return out
    sc = distance_summary.get('scope')
    out.update({'ok': True, 'lower': float(lower), 'upper': float(upper), 'central': dc, 'modulus_mag': mu,
                'modulus_low_mag': float(mu_lo), 'modulus_high_mag': float(mu_hi),
                'modulus_half_width_multiple': k, 'summary_scope': (_safe_str(sc) if sc is not None else None)})
    return out


# --------------------------------------------------------------------------
# classification
# --------------------------------------------------------------------------

def _sanitize_prediction(raw):
    """Plain, JSON-safe copy of a forward return value (None if it is not a dict)."""
    if not isinstance(raw, dict):
        return None
    speeds = raw.get('speeds_km_s')
    clean_speeds = None
    if isinstance(speeds, dict):
        clean_speeds = {}
        for k, v in speeds.items():
            clean_speeds[_safe_str(k)] = _finite_float(v)
    rsn = raw.get('reasons')
    if isinstance(rsn, (list, tuple)):
        clean_reasons = [_safe_str(r) for r in rsn]
    elif isinstance(rsn, str):
        clean_reasons = [rsn]   # review E1-F9: a str reason is kept, not dropped
    else:
        clean_reasons = []
    return {'speeds_km_s': clean_speeds, 'valid': bool(_is_true(raw.get('valid'))), 'reasons': clean_reasons}


@_fail_closed
def classify_prediction(*, prediction, rectangles, row_ids):
    """Classify a forward return value against the closed rectangles.

    valid: dict with valid is True, every row id present, every value a finite number.
    admitted: True/False when valid (all rows inside [low, high]); None when invalid.
    row_inside[row_id]: True/False where a finite value exists, None otherwise.
    Keys other than the row ids are listed in unexpected_keys with a reason (they do not change validity).
    """
    out = {'ok': False, 'valid': False, 'admitted': None, 'row_inside': {}, 'speeds_km_s': None,
           'outside_rows': [], 'forward_reasons': [], 'unexpected_keys': [], 'reasons': []}
    reasons = out['reasons']
    if not isinstance(row_ids, (list, tuple)) or not row_ids or \
            not all(isinstance(r, str) and r for r in row_ids) or len(set(row_ids)) != len(row_ids):
        reasons.append('row_ids must be a non-empty list of unique str')
        return out
    if not isinstance(rectangles, dict):
        reasons.append('rectangles must be a dict keyed by row id')
        return out
    rect = {}
    for rid in row_ids:
        r = rectangles.get(rid)
        if not isinstance(r, (list, tuple)) or len(r) != 2:
            reasons.append(f'rectangles[{rid!r}] must be [low, high]')
            continue
        lo, hi = _finite_float(r[0]), _finite_float(r[1])
        if lo is None or hi is None or not (lo <= hi):
            reasons.append(f'rectangles[{rid!r}] must be finite with low <= high')
            continue
        rect[rid] = (lo, hi)
    if reasons:
        return out
    out['ok'] = True
    row_inside = {rid: None for rid in row_ids}
    out['row_inside'] = row_inside
    if not isinstance(prediction, dict):
        reasons.append(f'prediction is not a dict (got {type(prediction).__name__}); evaluation invalid')
        return out
    valid = True
    if not _is_true(prediction.get('valid')):
        reasons.append("forward did not report valid is True (S6: the flag must be the bool True; got "
                       f"{type(prediction.get('valid')).__name__})")
        valid = False
    fr = prediction.get('reasons')
    if isinstance(fr, (list, tuple)):
        out['forward_reasons'] = [_safe_str(x) for x in fr]
    elif isinstance(fr, str):
        out['forward_reasons'] = [fr]
    speeds = prediction.get('speeds_km_s')
    if not isinstance(speeds, dict):
        reasons.append("forward 'speeds_km_s' is not a dict")
        return out
    clean = {}
    for rid in row_ids:
        v = _finite_float(speeds.get(rid))
        if v is None:
            reasons.append(f'row {rid!r}: speed missing or not a finite number')
            valid = False
            continue
        clean[rid] = v
        lo, hi = rect[rid]
        row_inside[rid] = bool(lo <= v <= hi)
    extra = [_safe_str(k) for k in speeds.keys() if not (isinstance(k, str) and k in rect)]
    if extra:
        out['unexpected_keys'] = extra
        reasons.append(f'forward returned {len(extra)} key(s) that are not row ids (ignored): {extra[:5]}')
    out['speeds_km_s'] = clean if valid else None
    out['valid'] = valid
    if valid:
        outside = [rid for rid in row_ids if row_inside[rid] is False]
        out['outside_rows'] = outside
        out['admitted'] = (len(outside) == 0)
    return out


# --------------------------------------------------------------------------
# forward evaluation wrapper (the only place forward is called)
# --------------------------------------------------------------------------

def _evaluate_point(*, forward, spec, region, u, purpose, log, counter):
    """Call forward once at unit point u, append the log entry, count the call, return the entry.

    The caller checks the budget before calling. Exceptions from forward, and from handling its return
    value, are caught and recorded; the evaluation is then invalid. A requested u outside [0,1] is clipped
    and the clip is recorded (review E1-N1).
    """
    raw_u = np.asarray(u, dtype=float)
    clipped = np.clip(raw_u, 0.0, 1.0)
    clip_move = float(np.max(np.abs(raw_u - clipped))) if raw_u.size else 0.0
    if not math.isfinite(clip_move):
        clip_move = math.inf
    u_list = _floats(clipped)
    entry = {
        'index': len(log), 'purpose': purpose, 'u': u_list, 'theta_internal': None,
        'theta_natural': None, 'prediction': None, 'valid': False, 'admitted': None,
        'row_inside': {rid: None for rid in region['row_ids']}, 'reasons': [], 'exception': None,
        'u_clip_move': clip_move,
    }
    if clip_move > 0.0:
        entry['reasons'].append(f'requested u clipped onto the unit box (max move {clip_move:.3e})')
    counter['used'] += 1
    nat = to_natural(spec=spec, u=u_list)
    if not nat['ok']:
        entry['reasons'] = ['unit-to-natural conversion failed; forward not called'] + list(nat['reasons'])
        log.append(entry)
        return entry
    entry['theta_internal'] = list(nat['theta_internal'])
    entry['theta_natural'] = dict(nat['theta_natural'])
    raw = None
    try:
        raw = forward(dict(nat['theta_natural']))
    except Exception as exc:  # root-supplied callable failure -> invalid evaluation
        entry['exception'] = f'{type(exc).__name__}: {_safe_str(exc)}'
        entry['reasons'].append('forward raised an exception; evaluation invalid')
        log.append(entry)
        return entry
    try:
        entry['prediction'] = _sanitize_prediction(raw)
        cls = classify_prediction(prediction=raw, rectangles=region['rectangles'], row_ids=region['row_ids'])
        entry['valid'] = bool(cls['valid'])
        entry['admitted'] = cls['admitted']
        entry['row_inside'] = dict(cls['row_inside'])
        entry['reasons'].extend(cls['reasons'])
        if cls['valid'] and entry['prediction'] is not None and \
                isinstance(entry['prediction'].get('speeds_km_s'), dict):
            # logged speeds are exactly the classified speeds (review E1-N5)
            entry['prediction']['speeds_km_s'].update(cls['speeds_km_s'])
    except Exception as exc:  # pathological return object (review E1-F6)
        entry['prediction'] = None
        entry['valid'] = False
        entry['admitted'] = None
        entry['row_inside'] = {rid: None for rid in region['row_ids']}
        entry['exception'] = f'{type(exc).__name__}: {_safe_str(exc)}'
        entry['reasons'].append('handling the forward return value raised; evaluation invalid')
    log.append(entry)
    return entry


def _speeds_vector(entry, row_ids):
    return np.array([entry['prediction']['speeds_km_s'][rid] for rid in row_ids], dtype=float)


def _common_eval_checks(forward, spec, region, log, budget):
    reasons = []
    if not callable(forward):
        reasons.append('forward must be callable')
    rs, info = _check_spec(spec)
    reasons.extend(rs)
    reasons.extend(_check_region(region))
    if not isinstance(log, list):
        reasons.append('log must be a list (entries are appended in place)')
    reasons.extend(_nonneg_int(budget, 'budget'))
    return reasons, info


# --------------------------------------------------------------------------
# Jacobian
# --------------------------------------------------------------------------

@_fail_closed
def finite_difference_jacobian(*, forward, spec, region, u0, rel_step, min_step, max_halvings, budget, log):
    """Central-difference Jacobian d(speeds)/d(u) at the seed u0.

    Column j: sides h_p0 = min(rel_step, 1-u_j), h_m0 = min(rel_step, u_j), clipped once; attempt k uses
    h_p0/2^k and h_m0/2^k (review E2-F3: halving also shrinks a clipped side). A zero side reuses f0.
    If the plus side is invalid the minus side is not evaluated at that step. A non-finite column is a
    failed attempt (E2-F5). A column that never succeeds is in failed_columns with None entries and the
    status is COMPLETE_WITH_FAILED_COLUMNS (ok=False). Every forward call is appended to log.
    """
    out = {
        'ok': False, 'status': None, 'f0': None, 'seed_valid': False, 'seed_admitted': None,
        'seed_log_index': None, 'u0': None, 'jacobian_u': None, 'steps_used': [], 'steps_detail': [],
        'failed_columns': [], 'evaluations_used': 0, 'budget': None, 'row_ids': [], 'varying_names': [],
        'jacobian_units': 'km/s per unit u', 'bounds_semantics': BOUNDS_SEMANTICS, 'reasons': [],
    }
    reasons, info = _common_eval_checks(forward, spec, region, log, budget)
    reasons.extend(_positive_float(rel_step, 'rel_step'))
    reasons.extend(_positive_float(min_step, 'min_step'))
    reasons.extend(_nonneg_int(max_halvings, 'max_halvings'))
    if not reasons and not (float(min_step) <= float(rel_step)):
        reasons.append('min_step must not exceed rel_step')
    if not reasons and float(rel_step) > _MAX_REL_STEP:
        reasons.append(f'rel_step must not exceed {_MAX_REL_STEP} (review E2-F10)')
    if info is not None:
        rs, uu = _check_unit_vector(u0, info['n'], 'u0')
        reasons.extend(rs)
    if reasons:
        out['reasons'] = reasons
        out['status'] = 'INPUT_INVALID'
        return out
    rel_step = float(rel_step)
    min_step = float(min_step)
    n = info['n']
    row_ids = list(region['row_ids'])
    m = len(row_ids)
    out['u0'] = _floats(uu)
    out['budget'] = int(budget)
    out['row_ids'] = row_ids
    out['varying_names'] = list(info['varying'])
    counter = {'used': 0, 'budget': int(budget)}
    reasons = out['reasons']

    def finish(status):
        out['status'] = status
        out['evaluations_used'] = counter['used']
        return out

    # seed
    if counter['used'] >= counter['budget']:
        reasons.append('budget exhausted before the seed evaluation')
        return finish('BUDGET_EXHAUSTED')
    seed = _evaluate_point(forward=forward, spec=spec, region=region, u=uu, purpose='seed', log=log,
                           counter=counter)
    out['seed_log_index'] = seed['index']
    if not seed['valid']:
        reasons.append('seed evaluation invalid: ' + '; '.join(seed['reasons']) +
                       (f' [exception: {seed["exception"]}]' if seed['exception'] else ''))
        return finish('SEED_INVALID')
    out['seed_valid'] = True
    out['seed_admitted'] = seed['admitted']
    f0 = _speeds_vector(seed, row_ids)
    out['f0'] = {rid: float(f0[i]) for i, rid in enumerate(row_ids)}

    J = [[None] * n for _ in range(m)]
    steps_used = [None] * n
    steps_detail = [None] * n
    failed = []
    exhausted = False
    for j in range(n):
        h_p0 = min(rel_step, 1.0 - float(uu[j]))
        h_m0 = min(rel_step, float(uu[j]))
        dropped = []
        # S4 (review T6c): a side clipped below min_step would evaluate a near-duplicate of the seed;
        # it is dropped (one-sided difference reusing f0) instead of costing a forward call.
        if 0.0 < h_p0 < min_step:
            h_p0 = 0.0
            dropped.append('plus')
        if 0.0 < h_m0 < min_step:
            h_m0 = 0.0
            dropped.append('minus')
        halvings = 0
        col_reasons = []
        done = False
        while True:
            scale = 0.5 ** halvings
            h = rel_step * scale
            h_p = h_p0 * scale
            h_m = h_m0 * scale
            if h_p + h_m < min_step:
                col_reasons.append(f'clipped step {h_p + h_m:.3e} below min_step')
                break
            f_p = f_m = None
            p_idx = m_idx = None
            side_reasons = []
            if h_p > 0.0:
                if counter['used'] >= counter['budget']:
                    exhausted = True
                    break
                up = uu.copy()
                up[j] = float(uu[j]) + h_p
                ep = _evaluate_point(forward=forward, spec=spec, region=region, u=up, purpose='jacobian',
                                     log=log, counter=counter)
                p_idx = ep['index']
                if ep['valid']:
                    f_p = _speeds_vector(ep, row_ids)
                else:
                    side_reasons.append(f'+side at step {h_p:.3e} invalid (log index {ep["index"]})')
            else:
                f_p = f0
            if h_m > 0.0 and f_p is not None:
                if counter['used'] >= counter['budget']:
                    exhausted = True
                    break
                um = uu.copy()
                um[j] = float(uu[j]) - h_m
                em = _evaluate_point(forward=forward, spec=spec, region=region, u=um, purpose='jacobian',
                                     log=log, counter=counter)
                m_idx = em['index']
                if em['valid']:
                    f_m = _speeds_vector(em, row_ids)
                else:
                    side_reasons.append(f'-side at step {h_m:.3e} invalid (log index {em["index"]})')
            elif h_m == 0.0:
                f_m = f0
            else:
                side_reasons.append('-side not evaluated because the +side failed at this step')
            if f_p is not None and f_m is not None:
                with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
                    col = (f_p - f_m) / (h_p + h_m)
                if not np.all(np.isfinite(col)):
                    side_reasons.append('non-finite difference column at this step (S1: overflowed quotient '
                                        'is a failed side)')
                else:
                    for i in range(m):
                        J[i][j] = float(col[i])
                    steps_used[j] = float(h)
                    steps_detail[j] = {'nominal_step': float(h), 'plus_step': float(h_p),
                                       'minus_step': float(h_m), 'span': float(h_p + h_m),
                                       'halvings': int(halvings),
                                       'one_sided': bool(h_p == 0.0 or h_m == 0.0),
                                       'asymmetric': bool(h_p != h_m),
                                       'plus_log_index': p_idx, 'minus_log_index': m_idx,
                                       'sides_dropped_below_min_step': list(dropped)}
                    done = True
                    break
            col_reasons.extend(side_reasons)
            if halvings >= int(max_halvings):
                col_reasons.append(f'max_halvings={int(max_halvings)} reached')
                break
            halvings += 1
            if rel_step * 0.5 ** halvings < min_step:
                col_reasons.append(f'halved step {rel_step * 0.5 ** halvings:.3e} below min_step={min_step:.3e}')
                break
        if exhausted:
            reasons.append(f'budget exhausted while evaluating column {j} ({info["varying"][j]})')
            break
        if not done:
            failed.append(j)
            reasons.append(f'column {j} ({info["varying"][j]}) failed: ' + '; '.join(col_reasons))
    out['jacobian_u'] = J
    out['steps_used'] = steps_used
    out['steps_detail'] = steps_detail
    out['failed_columns'] = failed
    if exhausted:
        return finish('BUDGET_EXHAUSTED')
    if failed:
        return finish('COMPLETE_WITH_FAILED_COLUMNS')   # review E2-F8: ok stays False
    out['ok'] = True
    return finish('COMPLETE')


# --------------------------------------------------------------------------
# identifiability
# --------------------------------------------------------------------------

def _fix_signs(vt):
    """Make the first near-largest-magnitude component of each right vector positive.

    Ties within relative 1e-9 of the maximum are broken by the lowest index (review E2-F6).
    """
    vt = np.array(vt, dtype=float, copy=True)
    for k in range(vt.shape[0]):
        mag = np.abs(vt[k])
        mx = float(mag.max()) if mag.size else 0.0
        if mx <= 0.0:
            continue
        idx = int(np.flatnonzero(mag >= mx * (1.0 - 1e-9))[0])
        if vt[k, idx] < 0:
            vt[k] = -vt[k]
    return vt


@_fail_closed
def identifiability_report(*, jacobian_u, sigmas, row_ids, varying_names, null_tolerance):
    """SVD identifiability report of the sigma-scaled Jacobian diag(1/sigma) . J_u.

    v003 rule (S3; IDENTIFICATION_RULE): direction i (row i of right_vectors) is identified iff
    s_i >= effective_tolerance * s_max (relative) OR s_i >= z = 2.865260238532134 (absolute), with
    effective_tolerance = max(null_tolerance, MIN_NULL_TOLERANCE, max(m, n) * eps). identified_by
    records which rule fired; a near-null s_i >= 1 is warned and s_i >= z flagged.
    condition_numbers[i] = s_max / s_i, or the string "inf". S1: a non-finite or out-of-range scaled
    Jacobian is refused before the SVD (reason prefix NUMERIC_RANGE).
    The right-vector basis is complete (n x n). When n > m (more varying coordinates than rows) the
    n - m missing singular values are explicit zeros and their directions span the exact null space;
    this is recorded in null_space_completion (D10). Any None or non-finite input makes the report ok=False.
    """
    out = {
        'ok': False, 'scaled_jacobian': None, 'singular_values': None, 'right_vectors': None,
        'identified': [], 'near_null': [], 'condition_numbers': None, 'null_tolerance': None,
        'effective_null_tolerance': None, 'numerical_rank_floor': None,
        's_max': None, 'n_directions': None, 'row_ids': [], 'varying_names': [],
        'null_space_completion': None, 'near_null_with_sensitivity_ge_1': [],
        'near_null_with_sensitivity_ge_z': [], 'identified_by': None,
        'absolute_identification_threshold': ABSOLUTE_IDENTIFICATION_THRESHOLD,
        'min_null_tolerance': MIN_NULL_TOLERANCE, 'identification_rule': IDENTIFICATION_RULE,
        'numeric_guard': [],
        'singular_value_units': SINGULAR_VALUE_UNITS, 'bounds_semantics': BOUNDS_SEMANTICS, 'reasons': [],
    }
    reasons = out['reasons']
    if not isinstance(row_ids, (list, tuple)) or not row_ids or \
            not all(isinstance(r, str) and r for r in row_ids) or len(set(row_ids)) != len(row_ids):
        reasons.append('row_ids must be a non-empty list of unique str')
    if not isinstance(varying_names, (list, tuple)) or not varying_names or \
            not all(isinstance(r, str) and r for r in varying_names) or \
            len(set(varying_names)) != len(varying_names):
        reasons.append('varying_names must be a non-empty list of unique str')
    tol = _finite_float(null_tolerance)
    if tol is None or not (0.0 <= tol <= 1.0):
        reasons.append('null_tolerance must be a finite number in [0, 1]')
    if reasons:
        return out
    m, n = len(row_ids), len(varying_names)
    if isinstance(jacobian_u, np.ndarray):
        jacobian_u = jacobian_u.tolist()
    if not isinstance(jacobian_u, (list, tuple)) or len(jacobian_u) != m:
        reasons.append(f'jacobian_u must be a list of {m} rows')
        return out
    J = np.zeros((m, n), dtype=float)
    for i, row in enumerate(jacobian_u):
        if isinstance(row, np.ndarray):
            row = row.tolist()
        if not isinstance(row, (list, tuple)) or len(row) != n:
            reasons.append(f'jacobian_u[{i}] must be a list of {n} entries')
            continue
        for j, v in enumerate(row):
            if v is None:
                reasons.append(f'jacobian_u[{i}][{j}] is None (failed column {j}, {varying_names[j]})')
                continue
            fv = _finite_float(v)
            if fv is None:
                reasons.append(f'jacobian_u[{i}][{j}] is not a finite number')
                continue
            J[i, j] = fv
    if not isinstance(sigmas, dict):
        reasons.append('sigmas must be a dict keyed by row id')
        return out
    sig = np.zeros(m, dtype=float)
    for i, rid in enumerate(row_ids):
        s = _finite_float(sigmas.get(rid))
        if s is None or not (s > 0):
            reasons.append(f'sigmas[{rid!r}] must be a finite positive number')
            continue
        sig[i] = s
    if reasons:
        return out
    with np.errstate(over='ignore', invalid='ignore'):
        S = J / sig[:, None]
    # S1: refuse before numpy.linalg when the scaled Jacobian is non-finite or outside the safe range
    # (an overflowed matrix hung np.linalg.svd in review S1).
    g = _numeric_guard(S, 'scaled Jacobian')
    if g:
        out['numeric_guard'] = g
        reasons.extend(g)
        reasons.append('scaled Jacobian is not finite or out of the safe numeric range; report refused (S1)')
        return out
    try:
        _, s, vt = np.linalg.svd(S, full_matrices=True)
    except Exception as exc:
        reasons.append(f'SVD failed: {type(exc).__name__}: {_safe_str(exc)}')
        return out
    if not (np.all(np.isfinite(s)) and np.all(np.isfinite(vt))):
        reasons.append('SVD returned non-finite values; report refused')
        return out
    n_svd = int(len(s))
    s_full = np.zeros(n, dtype=float)
    s_full[:n_svd] = s
    vt = _fix_signs(vt)
    s_max = float(s_full[0]) if n > 0 else 0.0
    floor = float(max(m, n) * np.finfo(float).eps)
    eff = max(tol, MIN_NULL_TOLERANCE, floor)   # S3: enforced minimum tolerance
    if tol < MIN_NULL_TOLERANCE:
        reasons.append(f'NOTE null_tolerance {tol!r} is below MIN_NULL_TOLERANCE {MIN_NULL_TOLERANCE!r}; the '
                       f'minimum is enforced (S3: rounding/FD-artefact singular values must not be identified)')
    identified, near_null, by = _classify_directions(s_full, eff, s_max)
    cond = []
    for i in range(n):
        si = float(s_full[i])
        r = (s_max / si) if si > 0.0 else math.inf
        cond.append(float(r) if math.isfinite(r) else 'inf')
    if s_max <= 0.0:
        reasons.append('scaled Jacobian is identically zero: no direction is identified')
    abs_promoted = [i for i in identified if by[i] == 'absolute']
    if abs_promoted:
        reasons.append(f'NOTE direction(s) {abs_promoted} identified by the absolute rule only (s_i >= z = '
                       f'{ABSOLUTE_IDENTIFICATION_THRESHOLD}); the relative rule alone would have demoted them '
                       f'(S3, review E2-F2)')
    strong = [i for i in near_null if float(s_full[i]) >= 1.0]
    strong_z = [i for i in near_null if float(s_full[i]) >= ABSOLUTE_IDENTIFICATION_THRESHOLD]
    if strong:
        reasons.append(f'WARNING near-null direction(s) {strong} have singular value >= 1 (a full-box move '
                       f'changes the sigma-scaled 12-vector by >= 1, below z): held at the anchor, not marched; '
                       f'box-limited sensitivity is the freeze module\'s D6 task')
    if strong_z:
        reasons.append(f'FLAG near-null direction(s) {strong_z} have singular value >= z (S3)')
    ortho = float(np.max(np.abs(vt @ vt.T - np.eye(n)))) if n else 0.0
    padded = list(range(n_svd, n))
    null_resid = float(max((np.linalg.norm(S @ vt[k]) for k in padded), default=0.0))
    completion = {
        'n_rows': m, 'n_directions': n, 'rank_bound': int(min(m, n)),
        'n_singular_values_from_svd': n_svd, 'padded_indices': padded, 'padded_singular_value': 0.0,
        'basis': 'full_matrices=True right singular vectors (n x n); padded directions span the exact null '
                 'space of the m x n scaled Jacobian and are listed in near_null',
        'orthonormality_error': ortho, 'padded_null_residual_max': null_resid,
    }
    if padded:
        reasons.append(f'n = {n} varying coordinates exceed the {m} rows: directions {padded} are exactly '
                       f'unidentified by these rows (null space completed explicitly)')
    out.update({
        'ok': True, 'scaled_jacobian': _matrix(S), 'singular_values': _floats(s_full),
        'right_vectors': _matrix(vt), 'identified': identified, 'near_null': near_null,
        'condition_numbers': cond, 'null_tolerance': tol, 'effective_null_tolerance': eff,
        'numerical_rank_floor': floor, 's_max': s_max, 'n_directions': n,
        'row_ids': list(row_ids), 'varying_names': list(varying_names),
        'null_space_completion': completion, 'near_null_with_sensitivity_ge_1': strong,
        'near_null_with_sensitivity_ge_z': strong_z, 'identified_by': {int(i): by[i] for i in range(n)},
        'absolute_identification_threshold': ABSOLUTE_IDENTIFICATION_THRESHOLD,
        'min_null_tolerance': MIN_NULL_TOLERANCE, 'identification_rule': IDENTIFICATION_RULE,
    })
    return out


def _classify_directions(s_full, eff, s_max):
    """S3 rule: (identified, near_null, identified_by) from singular values (non-increasing)."""
    identified, near_null, by = [], [], []
    for i in range(len(s_full)):
        si = float(s_full[i])
        rel = bool(s_max > 0.0 and si > 0.0 and si >= eff * s_max)
        absr = bool(si >= ABSOLUTE_IDENTIFICATION_THRESHOLD)
        if rel or absr:
            identified.append(i)
            by.append('both' if (rel and absr) else ('relative' if rel else 'absolute'))
        else:
            near_null.append(i)
            by.append('near_null')
    return identified, near_null, by


# --------------------------------------------------------------------------
# exploration helpers
# --------------------------------------------------------------------------

def _first_primes(count):
    primes = []
    cand = 2
    while len(primes) < count:
        if all(cand % p for p in primes if p * p <= cand):
            primes.append(cand)
        cand += 1
    return primes


def _radical_inverse(index, base):
    result = 0.0
    f = 1.0 / base
    i = int(index)
    while i > 0:
        result += f * (i % base)
        i //= base
        f /= base
    return result


def _edge_t(a, d):
    """Largest t >= 0 with a + t d inside [0,1]^n up to _BOX_TOL (inf if d is zero).

    Review A2 / E2-F1 / E3-M4: components with |d_j| <= _BOX_TOL are treated as zero (rounding-level
    leakage of SVD right vectors), and the face slack is _BOX_TOL, the same tolerance the engine uses
    for "inside the box" (L248/L946 of v001). A genuine outward component at a face still exits at once.
    """
    t_edge = math.inf
    for j in range(len(a)):
        dj = float(d[j])
        aj = float(a[j])
        if dj > _BOX_TOL:
            t_edge = min(t_edge, max(1.0 - aj, _BOX_TOL) / dj)
        elif dj < -_BOX_TOL:
            t_edge = min(t_edge, min(0.0 - aj, -_BOX_TOL) / dj)
    return max(0.0, t_edge)


def _step_fraction_inside(a, d):
    """S2: largest alpha in [0, 1] with a + alpha * d inside [0,1]^n exactly (no face slack); components with
    |d_j| <= _BOX_TOL are inert. The repair truncates its step length by alpha instead of clipping, so the
    step stays in span(identified) and near-null components are not moved."""
    alpha = 1.0
    for j in range(len(a)):
        dj = float(d[j])
        aj = min(1.0, max(0.0, float(a[j])))
        if dj > _BOX_TOL:
            alpha = min(alpha, (1.0 - aj) / dj)
        elif dj < -_BOX_TOL:
            alpha = min(alpha, (0.0 - aj) / dj)
    return max(0.0, alpha)


@_fail_closed
def direction_box_extent(*, u, direction):
    """Extent of the computational box along a unit-space direction through u.

    Returns t_minus <= 0 <= t_plus with u + t * direction inside [0,1]^n for t in [t_minus, t_plus]
    (the same tolerance rule as the march), and the two end points in u. Helper for box-end sensitivity
    displacements along near-null directions (D6 is evaluated by the freeze module, not here).
    """
    out = {'ok': False, 't_minus': None, 't_plus': None, 'u_minus_end': None, 'u_plus_end': None,
           'bounds_semantics': BOUNDS_SEMANTICS, 'reasons': []}
    if isinstance(u, np.ndarray):
        u = u.tolist()
    if not isinstance(u, (list, tuple)) or not u:
        out['reasons'] = ['u must be a non-empty list']
        return out
    rs, uu = _check_unit_vector(u, len(u), 'u')
    if rs:
        out['reasons'] = rs
        return out
    if isinstance(direction, np.ndarray):
        direction = direction.tolist()
    if not isinstance(direction, (list, tuple)) or len(direction) != len(u):
        out['reasons'] = ['direction must be a list with the length of u']
        return out
    dv = []
    for j, x in enumerate(direction):
        v = _finite_float(x)
        if v is None:
            out['reasons'] = [f'direction[{j}] must be a finite number']
            return out
        dv.append(v)
    d = np.array(dv, dtype=float)
    if float(np.max(np.abs(d))) <= _BOX_TOL:
        out['reasons'] = ['direction is zero within tolerance']
        return out
    tp = _edge_t(uu, d)
    tm = -_edge_t(uu, -d)
    out.update({'ok': True, 't_minus': float(tm), 't_plus': float(tp),
                'u_minus_end': _floats(np.clip(uu + tm * d, 0.0, 1.0)),
                'u_plus_end': _floats(np.clip(uu + tp * d, 0.0, 1.0))})
    return out


def _inside_box(p):
    return bool(np.all(p >= -_BOX_TOL) and np.all(p <= 1.0 + _BOX_TOL))


def _point_from_entry(entry):
    # deep copies: mutating a returned point must not change the log (review E2-F12)
    return {
        'u': list(entry['u']), 'theta_internal': copy.deepcopy(entry['theta_internal']),
        'theta_natural': copy.deepcopy(entry['theta_natural']),
        'prediction': copy.deepcopy(entry['prediction']), 'log_index': entry['index'],
        'purpose': entry['purpose'], 'valid': entry['valid'], 'admitted': entry['admitted'],
        'row_inside': copy.deepcopy(entry['row_inside']),
    }


def _check_identifiability(ident, n, m, varying_names, row_ids):
    """Validate an identifiability report against the spec, the region and itself (review E2-F4, E3-F11)."""
    if not isinstance(ident, dict) or not _is_true(ident.get('ok')):
        return ['identifiability must be an ok=True dict from identifiability_report'], None
    reasons = []
    try:
        S = np.array(ident['scaled_jacobian'], dtype=float)
        V = np.array(ident['right_vectors'], dtype=float)
        s = np.array(ident['singular_values'], dtype=float)
    except Exception as exc:
        return [f'identifiability arrays malformed: {type(exc).__name__}: {_safe_str(exc)}'], None
    if S.shape != (m, n):
        reasons.append(f'identifiability.scaled_jacobian must be {m}x{n}')
    if V.shape != (n, n):
        reasons.append(f'identifiability.right_vectors must be {n}x{n}')
    if s.shape != (n,):
        reasons.append(f'identifiability.singular_values must have length {n}')
    if reasons:
        return reasons, None
    if not (np.all(np.isfinite(S)) and np.all(np.isfinite(V)) and np.all(np.isfinite(s))):
        return ['identifiability arrays must be finite'], None
    g = _numeric_guard(S, 'identifiability.scaled_jacobian') + _numeric_guard(s, 'identifiability.singular_values')
    if g:
        return g, None
    if list(ident.get('row_ids') or []) != list(row_ids):
        reasons.append('identifiability.row_ids must equal region.row_ids (same order)')
    if list(ident.get('varying_names') or []) != list(varying_names):
        reasons.append('identifiability.varying_names must equal spec.varying_names (same order)')
    identified = ident.get('identified')
    near_null = ident.get('near_null')
    if not isinstance(identified, list) or not isinstance(near_null, list) or \
            not all(_is_int(k) for k in identified + near_null):
        reasons.append('identifiability.identified and .near_null must be lists of int')
        return reasons, None
    if sorted(identified + near_null) != list(range(n)) or (set(identified) & set(near_null)):
        reasons.append('identifiability.identified and .near_null must partition range(n)')
    if float(np.max(np.abs(V @ V.T - np.eye(n)))) > _ORTHO_TOL:
        reasons.append('identifiability.right_vectors must be orthonormal')
    if np.any(s < 0.0) or np.any(np.diff(s) > _ORTHO_TOL * max(1.0, float(s[0]))):
        reasons.append('identifiability.singular_values must be non-negative and non-increasing')
    smax = float(s[0]) if n else 0.0
    for k in range(n):
        if abs(float(np.linalg.norm(S @ V[k])) - float(s[k])) > _ORTHO_TOL * max(1.0, smax):
            reasons.append(f'identifiability: ||S v_{k}|| differs from singular value {k}')
            break
    eff = _finite_float(ident.get('effective_null_tolerance'))
    if eff is None or not (0.0 <= eff <= 1.0):
        reasons.append('identifiability.effective_null_tolerance missing or invalid')
    elif eff < MIN_NULL_TOLERANCE:
        reasons.append(f'identifiability.effective_null_tolerance {eff!r} is below MIN_NULL_TOLERANCE '
                       f'{MIN_NULL_TOLERANCE!r} (S3)')
    elif not reasons:
        expect, _nn, _by = _classify_directions(s, eff, smax)
        if sorted(int(k) for k in identified) != expect:
            reasons.append('identifiability.identified does not follow from the singular values, '
                           'effective_null_tolerance and the absolute threshold z (S3/S5)')
    if reasons:
        return reasons, None
    for k in identified:
        if not (s[k] > 0.0):
            reasons.append(f'identified direction {k} has non-positive singular value')
    if reasons:
        return reasons, None
    return [], {'S': S, 'V': V, 's': s, 'identified': [int(k) for k in sorted(identified)],
                'near_null': [int(k) for k in sorted(near_null)]}


def _minimax_step(S, V, dirs, r, du):
    """Max-norm (rectangle-metric) refinement of the linearised step on span(V[dirs]) (review E3-F1(b)).

    Lawson-weighted least squares with a fixed iteration count; starts from the L2 step du and replaces it
    only on a strict improvement of max|A c - r|, so an exactly reachable target keeps the L2 step bitwise.
    """
    VI = V[list(dirs)]
    A = S @ VI.T
    mrows = len(r)
    w = np.full(mrows, 1.0 / mrows)
    c = VI @ du
    best = float(np.max(np.abs(A @ c - r)))
    l2_best = best
    if _numeric_guard(A, 'A') or _numeric_guard(r, 'r') or not math.isfinite(best):
        return du, best, l2_best   # S1: no linear algebra outside the safe range; keep the L2 step
    deadline = time.monotonic() + _NUMERIC_WALL_SECONDS   # S1 wall guard
    for _ in range(_LAWSON_ITERATIONS):
        if time.monotonic() > deadline:
            break
        sw = np.sqrt(w)
        try:
            cc = np.linalg.lstsq(A * sw[:, None], r * sw, rcond=None)[0]
        except Exception:
            break
        e = np.abs(A @ cc - r)
        if not np.all(np.isfinite(e)):
            break
        me = float(np.max(e))
        if me < best - 1e-12 * max(1.0, best):
            best, c = me, cc
        tot = float(np.sum(w * e))
        if not (tot > 0.0) or not math.isfinite(tot):
            break
        w = w * e / tot
    return VI.T @ c, best, l2_best


def _lp_max(A, b, w):
    """Maximise w.c subject to A c <= b, c free, with b >= 0 (c = 0 feasible).

    Dense tableau primal simplex with Bland's rule (no cycling); deterministic. Returns (c, status) with
    status 'OPTIMAL', 'UNBOUNDED' or 'ITERATION_LIMIT'.
    """
    M, m = A.shape
    T = np.zeros((M + 1, 2 * m + M + 1), dtype=float)
    T[:M, :m] = A
    T[:M, m:2 * m] = -A
    T[:M, 2 * m:2 * m + M] = np.eye(M)
    T[:M, -1] = np.maximum(b, 0.0)
    T[M, :m] = -w
    T[M, m:2 * m] = w
    basis = list(range(2 * m, 2 * m + M))
    status = 'ITERATION_LIMIT'
    if _numeric_guard(T, 'simplex tableau'):
        return np.zeros(m, dtype=float), 'NUMERIC_RANGE'   # S1: refused before any pivot
    deadline = time.monotonic() + _NUMERIC_WALL_SECONDS   # S1 wall guard
    for _ in range(_LP_MAX_PIVOTS):
        if time.monotonic() > deadline:
            status = 'WALL_LIMIT'
            break
        cand = np.flatnonzero(T[M, :-1] < -_LP_EPS)
        if cand.size == 0:
            status = 'OPTIMAL'
            break
        j = int(cand[0])
        col = T[:M, j]
        pos = col > _LP_EPS
        if not pos.any():
            status = 'UNBOUNDED'
            break
        ratios = np.full(M, math.inf)
        ratios[pos] = T[:M, -1][pos] / col[pos]
        rmin = float(ratios.min())
        rows = np.flatnonzero(pos & (ratios <= rmin + _LP_EPS))
        i = int(min(rows, key=lambda r: basis[r]))
        T[i] = T[i] / T[i, j]
        for r in range(M + 1):
            if r != i and T[r, j] != 0.0:
                T[r] = T[r] - T[r, j] * T[i]
        basis[i] = j
    x = np.zeros(2 * m + M, dtype=float)
    for r, bv in enumerate(basis):
        x[bv] = T[r, -1]
    return x[:m] - x[m:2 * m], status


def _interior_score(entry, row_ids, centre, halfwidth):
    """max_i |f_i - centre_i| / halfwidth_i (<= 1 means admitted); smaller is more interior."""
    f = _speeds_vector(entry, row_ids)
    with np.errstate(divide='ignore', invalid='ignore'):
        q = np.where(halfwidth > 0, np.abs(f - centre) / np.where(halfwidth > 0, halfwidth, 1.0),
                     np.where(np.abs(f - centre) == 0.0, 0.0, np.inf))
    return float(np.max(q))


# --------------------------------------------------------------------------
# exploration
# --------------------------------------------------------------------------

def _explore_impl(*, forward, spec, region, u_anchor, identifiability, repair_iterations, max_repair_step,
                  march_step, bisection_steps, design_count, global_design_count, max_march_rounds,
                  hull_growth_tol, rng_seed, budget, log, anchor_entry):
    out = {
        'ok': False, 'status': None, 'stage_reached': None, 'anchor': None, 'first_admitted_log_index': None,
        'primary_anchor': None, 'admitted_points': [], 'rejected_points': [], 'boundary': {},
        'boundary_detail': {}, 'hull_box': {}, 'unidentified_directions': [], 'identified_directions': [],
        'log_scan': None,
        'repair': {'iterations_requested': None, 'iterations_used': 0, 'steps': [], 'phases': [],
                   'terminated_by': None},
        'design': {'count_requested': None, 'evaluated': 0, 'skipped_outside_box': 0, 'skipped_duplicate': 0,
                   'bases': [], 'first_index': None},
        'global_design': {'count_requested': None, 'evaluated': 0, 'skipped_duplicate': 0, 'bases': [],
                          'first_index': None, 'n_admitted': 0, 'run_before_march': None, 'completed': False},
        'march_rounds': [], 'refinement_status': None, 'hull_history': [], 'hull_growth_tol': None,
        'max_march_rounds': None, 'evaluations_used': 0, 'budget': None,
        'admitted_point_found': False, 'empty_region': None, 'emptiness_proven': False,
        'admitted_set_label': ADMITTED_SET_LABEL, 'admitted_set_statement': ADMITTED_SET_STATEMENT,
        'region_possibly_truncated': None, 'truncation_causes': [], 'box_limited_null_directions': [],
        'near_null_shifted': False, 'flags': [], 'coverage': None,
        'coordinate_units': {}, 'coordinate_ranges': {}, 'n_admitted': 0, 'n_rejected': 0,
        'n_admitted_by_purpose': {}, 'u_semantics': U_SEMANTICS,
        'bounds_semantics': BOUNDS_SEMANTICS, 'reasons': [],
    }
    reasons, info = _common_eval_checks(forward, spec, region, log, budget)
    reasons.extend(_nonneg_int(repair_iterations, 'repair_iterations'))
    reasons.extend(_positive_float(max_repair_step, 'max_repair_step'))
    reasons.extend(_positive_float(march_step, 'march_step'))
    reasons.extend(_nonneg_int(bisection_steps, 'bisection_steps'))
    reasons.extend(_nonneg_int(design_count, 'design_count'))
    reasons.extend(_nonneg_int(global_design_count, 'global_design_count'))
    reasons.extend(_nonneg_int(max_march_rounds, 'max_march_rounds'))
    reasons.extend(_nonneg_float(hull_growth_tol, 'hull_growth_tol'))
    reasons.extend(_nonneg_int(rng_seed, 'rng_seed'))
    idn = None
    if info is not None:
        rs, ua = _check_unit_vector(u_anchor, info['n'], 'u_anchor')
        reasons.extend(rs)
        if not _check_region(region):
            rs, idn = _check_identifiability(identifiability, info['n'], len(region['row_ids']),
                                             info['varying'], region['row_ids'])
            reasons.extend(rs)
    if anchor_entry is not None and not reasons:
        if not isinstance(anchor_entry, dict) or not anchor_entry.get('valid') or \
                len(anchor_entry.get('u', [])) != info['n'] or \
                not np.allclose(np.array(anchor_entry['u'], dtype=float), ua, rtol=0.0, atol=0.0):
            reasons.append('internal: supplied anchor evaluation does not match u_anchor')
    if reasons:
        out['reasons'] = reasons
        return out
    reasons = out['reasons']
    n = info['n']
    row_ids = list(region['row_ids'])
    S, V, s = idn['S'], idn['V'], idn['s']
    ident, near = idn['identified'], idn['near_null']
    s_max = float(s[0]) if n else 0.0
    counter = {'used': 0, 'budget': int(budget)}
    out['budget'] = int(budget)
    out['repair']['iterations_requested'] = int(repair_iterations)
    out['design']['count_requested'] = int(design_count)
    out['global_design']['count_requested'] = int(global_design_count)
    out['hull_growth_tol'] = float(hull_growth_tol)
    out['max_march_rounds'] = int(max_march_rounds)
    out['coordinate_units'] = {nm: info['coords'][nm]['units'] for nm in info['names']}
    max_repair_step = float(max_repair_step)
    march_step = float(march_step)
    hull_growth_tol = float(hull_growth_tol)
    sigma = np.array([region['sigmas'][rid] for rid in row_ids], dtype=float)
    lo_r = np.array([region['rectangles'][rid][0] for rid in row_ids], dtype=float)
    hi_r = np.array([region['rectangles'][rid][1] for rid in row_ids], dtype=float)
    centre = 0.5 * (lo_r + hi_r)
    halfwidth = 0.5 * (hi_r - lo_r)
    trial_u = info['trial_u']
    state = {'a': None, 'primary': None, 'core_done': False}
    used_anchor_indices = set()
    log_start = len(log)
    # boundary (round 0, from the primary anchor) keyed by identified direction index
    boundary = {int(k): {'minus': None, 'plus': None} for k in ident}
    detail = {int(k): {'minus': None, 'plus': None} for k in ident}
    out['boundary'] = boundary
    out['boundary_detail'] = detail
    out['boundary_cause'] = {int(k): {'minus': None, 'plus': None} for k in ident}   # P34-11
    out['boundary_cause_legend'] = BOUNDARY_CAUSES
    all_side_records = []

    def need_budget():
        if counter['used'] >= counter['budget']:
            raise _BudgetExhausted()

    def evaluate(u, purpose):
        return _evaluate_point(forward=forward, spec=spec, region=region, u=u, purpose=purpose, log=log,
                               counter=counter)

    def usable(e):
        """A log entry usable by this exploration: right shape, inside the box."""
        if not isinstance(e, dict) or e.get('purpose') not in PURPOSES:
            return False
        uu_ = e.get('u')
        if not isinstance(uu_, list) or len(uu_) != n:
            return False
        try:
            arr = np.array(uu_, dtype=float)
        except Exception:
            return False
        return bool(np.all(np.isfinite(arr)) and _inside_box(arr))

    def verified_admitted(e):
        """Admitted per the entry AND per re-classification of its logged prediction (A1 log scan)."""
        if not usable(e) or e.get('admitted') is not True or e.get('valid') is not True:
            return False
        try:
            c = classify_prediction(prediction=e.get('prediction'), rectangles=region['rectangles'],
                                    row_ids=row_ids)
        except Exception:
            return False
        return c['admitted'] is True

    def verified_valid(e):
        if not usable(e) or e.get('valid') is not True:
            return False
        try:
            c = classify_prediction(prediction=e.get('prediction'), rectangles=region['rectangles'],
                                    row_ids=row_ids)
        except Exception:
            return False
        return c['valid'] is True

    def admitted_entries():
        return [e for e in log if verified_admitted(e)]

    def already_evaluated(p):
        for e in log:
            if usable(e) and float(np.max(np.abs(np.array(e['u'], dtype=float) - p))) <= _BOX_TOL:
                return True
        return False

    def most_interior(entries):
        best, best_score = None, None
        for e in entries:
            sc = _interior_score(e, row_ids, centre, halfwidth)
            if best is None or sc < best_score:
                best, best_score = e, sc
        return best, best_score

    def set_primary(e, source, score=None):
        state['primary'] = e
        state['a'] = np.array(e['u'], dtype=float)
        used_anchor_indices.add(int(e['index']))
        out['first_admitted_log_index'] = e['index']
        out['primary_anchor'] = {'log_index': e['index'], 'purpose': e['purpose'], 'source': source,
                                 'u': list(e['u']), 'interior_score': score,
                                 'theta_natural': copy.deepcopy(e['theta_natural'])}

    def hull_of(entries):
        a = state['a']
        h = {}
        for k in ident:
            if a is None or not entries:
                h[int(k)] = {'min': None, 'max': None}
                continue
            proj = [float((np.array(e['u'], dtype=float) - a) @ V[k]) for e in entries]
            h[int(k)] = {'min': min(proj), 'max': max(proj)}
        return h

    def direction_summary(k):
        v = V[k]
        a = state['a']
        tp, sp = float(trial_u @ v), float(ua @ v)
        return {'index': int(k), 'vector_u': _floats(v), 'singular_value': float(s[k]),
                'trial_projection': tp, 'seed_projection': sp,
                'trial_differs_from_seed': bool(abs(tp - sp) > _SLICE_TOL),
                'admitted_anchor_projection': (float(a @ v) if a is not None else None),
                'sensitivity': float(np.linalg.norm(S @ v))}

    def march_side(p, d, rec, round0_k=None, round0_side=None):
        """Doubling march from p along d, then bisection. Updates rec in place; returns last admitted t."""
        t_edge = _edge_t(p, d)
        rec['box_edge_t'] = float(t_edge)
        t_last, t_rej, hit_edge = 0.0, None, False
        t = march_step

        def note(tl):
            rec['last_admitted_t'] = float(tl)
            if round0_k is not None:
                boundary[round0_k][round0_side] = float(tl)

        def stop_kind(e):
            return 'INVALID_EVALUATION' if e['valid'] is not True else 'REJECTED_EVALUATION'

        doublings = 0
        cause = None
        while True:
            if t > t_edge:   # review E1-N1: any t beyond the edge goes to the exact edge evaluation
                if t_edge > t_last + _T_TOL:
                    need_budget()
                    e = evaluate(p + t_edge * d, 'march')
                    rec['march_evaluations'] += 1
                    if e['admitted'] is True:
                        t_last, hit_edge = t_edge, True
                        note(t_last)
                        cause = 'COMPUTATIONAL_BOX_EDGE_ADMITTED'
                    else:
                        t_rej = t_edge
                        cause = stop_kind(e) + '_AT_BOX_EDGE'
                else:
                    hit_edge = True
                    if rec['march_evaluations'] == 0 and t_edge <= _T_TOL:
                        rec['closed_at_face_without_evaluation'] = True
                        cause = 'COMPUTATIONAL_BOX_FACE_NO_EVALUATION'
                    else:
                        cause = 'COMPUTATIONAL_BOX_EDGE_AT_LAST_ADMITTED'
                break
            if doublings >= _MAX_MARCH_DOUBLINGS or not math.isfinite(t):   # S1 doubling guard
                cause = 'DOUBLING_GUARD'
                reasons.append(f'march side stopped by the doubling guard ({_MAX_MARCH_DOUBLINGS} doublings; '
                               f'anchor log index {rec["anchor_log_index"]}, direction {rec["direction"]}, '
                               f'{rec["side"]})')
                break
            need_budget()
            e = evaluate(p + t * d, 'march')
            rec['march_evaluations'] += 1
            if e['admitted'] is True:
                t_last = t
                note(t_last)
                t = 2.0 * t
                doublings += 1
            else:
                t_rej = t
                cause = stop_kind(e)
                break
        rec['first_rejected_t'] = t_rej
        rec['hit_box_edge'] = hit_edge
        rec['boundary_cause'] = cause   # P34-11
        rec['first_non_admitted_kind'] = (cause.split('_AT_')[0] if cause and 'EVALUATION' in cause else None)
        note(t_last)
        if t_rej is not None and int(bisection_steps) > 0:
            out['stage_reached'] = 'bisection' if round0_k is not None else 'iterated_march'
            lo, hi = t_last, t_rej
            for _ in range(int(bisection_steps)):
                mid = 0.5 * (lo + hi)
                need_budget()
                e = evaluate(p + mid * d, 'bisection')
                rec['bisection_evaluations'] += 1
                if e['admitted'] is True:
                    lo = mid
                    note(lo)
                else:
                    hi = mid
                rec['first_rejected_t'] = float(hi)
            t_last, t_rej = lo, hi
        note(t_last)
        rec['first_rejected_t'] = (float(t_rej) if t_rej is not None else None)
        rec['complete'] = True
        if round0_k is not None:
            out['boundary_cause'][round0_k][round0_side] = rec['boundary_cause']
        if rec.get('closed_at_face_without_evaluation'):
            reasons.append(f'march side closed at a box face with no evaluation (anchor log index '
                           f'{rec["anchor_log_index"]}, direction {rec["direction"]}, {rec["side"]}): the '
                           f'direction has a genuine outward component at this face')
        return t_last

    def new_side_record(anchor_e, k, side):
        rec = {'anchor_log_index': int(anchor_e['index']), 'kind': 'axis', 'direction': int(k), 'side': side,
               'last_admitted_t': 0.0, 'first_rejected_t': None, 'box_edge_t': None, 'hit_box_edge': False,
               'march_evaluations': 0, 'bisection_evaluations': 0, 'complete': False,
               'closed_at_face_without_evaluation': False, 'boundary_cause': 'UNFINISHED',
               'first_non_admitted_kind': None}
        all_side_records.append(rec)
        return rec

    def global_design(run_before_march):
        out['stage_reached'] = 'global_design'
        g = out['global_design']
        g['run_before_march'] = bool(run_before_march)
        bases = _first_primes(n)
        first_index = int(rng_seed) + 1
        g['bases'] = bases
        g['first_index'] = first_index
        for jj in range(int(global_design_count)):
            idx = first_index + jj
            p = np.array([_radical_inverse(idx, b) for b in bases], dtype=float)
            if already_evaluated(p):
                g['skipped_duplicate'] += 1
                continue
            need_budget()
            e = evaluate(p, 'global_design')
            g['evaluated'] += 1
            if e['admitted'] is True:
                g['n_admitted'] += 1
        g['completed'] = True

    def finalise(status):
        out['status'] = status
        out['ok'] = (status == 'COMPLETE')
        out['evaluations_used'] = counter['used']
        a = state['a']
        adm, rej = [], []
        by_purpose = {}
        for e in log:
            if not usable(e):
                continue
            if verified_admitted(e):
                p = _point_from_entry(e)
                uvec = np.array(e['u'], dtype=float)
                if a is not None:
                    p['identified_projection'] = {int(k): float((uvec - a) @ V[k]) for k in ident}
                    p['near_null_projection'] = {int(k): float(uvec @ V[k]) for k in near}
                    p['on_anchor_slice'] = bool(all(abs(float((uvec - a) @ V[k])) <= _SLICE_TOL for k in near))
                p['interior_score'] = _interior_score(e, row_ids, centre, halfwidth)
                adm.append(p)
                by_purpose[e['purpose']] = by_purpose.get(e['purpose'], 0) + 1
            else:
                rej.append(_point_from_entry(e))
        out['admitted_points'] = adm
        out['rejected_points'] = rej
        out['n_admitted'] = len(adm)
        out['n_rejected'] = len(rej)
        out['n_admitted_by_purpose'] = by_purpose
        out['admitted_point_found'] = bool(adm)
        out['empty_region'] = (False if adm else None)   # A1: never True
        out['emptiness_proven'] = False
        out['hull_box'] = hull_of(admitted_entries()) if a is not None else {int(k): {'min': None, 'max': None}
                                                                            for k in ident}
        out['identified_directions'] = [direction_summary(k) for k in ident]
        out['unidentified_directions'] = [direction_summary(k) for k in near]
        ranges = {}
        for nm in info['varying']:
            vals = [pt['theta_natural'][nm] for pt in adm if isinstance(pt.get('theta_natural'), dict)]
            ranges[nm] = {'min': (min(vals) if vals else None), 'max': (max(vals) if vals else None),
                          'units': info['coords'][nm]['units']}
        out['coordinate_ranges'] = ranges
        # truncation causes (D7)
        causes = []
        if not adm:
            out['region_possibly_truncated'] = None
            out['truncation_causes'] = []
        else:
            if status == 'BUDGET_EXHAUSTED' or out['refinement_status'] == 'BUDGET_EXHAUSTED':
                causes.append('budget_exhausted')
            if out['refinement_status'] not in ('CONVERGED', 'CONVERGED_NO_NEW_EXTREME_ANCHOR'):
                causes.append('hull_convergence_not_verified')
            if any(r.get('hit_box_edge') for r in all_side_records):
                causes.append('march_reached_box_edge')
            if any(any(x <= _FACE_TOL or x >= 1.0 - _FACE_TOL for x in pt['u']) for pt in adm):
                causes.append('admitted_point_on_box_face')
            if int(global_design_count) == 0 or not out['global_design']['completed']:
                causes.append('global_design_not_run')
            if not ident:
                causes.append('no_identified_direction')
            out['region_possibly_truncated'] = bool(causes)
            out['truncation_causes'] = causes
        # near-null directions are never marched; along them the admitted set is limited by the box and by
        # whatever the global design sampled (box-end sensitivity is the freeze module's D6 task)
        out['box_limited_null_directions'] = [int(k) for k in near]
        out['flags'] = ([ADMITTED_SET_LABEL] if adm else []) + \
            (['REGION_POSSIBLY_TRUNCATED'] if out['region_possibly_truncated'] else [])
        out['coverage'] = {
            'admitted_set_label': ADMITTED_SET_LABEL, 'n_admitted': len(adm),
            'refinement_status': out['refinement_status'], 'march_rounds': len(out['march_rounds']),
            'hull_growth_tol': out['hull_growth_tol'],
            'last_round_growth': (out['march_rounds'][-1]['growth'] if out['march_rounds'] else None),
            'global_design_evaluated': out['global_design']['evaluated'],
            'global_design_admitted': out['global_design']['n_admitted'],
            'truncation_causes': list(out['truncation_causes']),
            'box_limited_null_directions': list(out['box_limited_null_directions']),
            'statement': ADMITTED_SET_STATEMENT,
        }
        return out

    try:
        # ---- stage 1: anchor ---------------------------------------------------------
        out['stage_reached'] = 'anchor'
        if anchor_entry is None:
            need_budget()
            anchor_entry = evaluate(ua, 'seed')
        out['anchor'] = {
            'u': list(anchor_entry['u']), 'theta_natural': copy.deepcopy(anchor_entry['theta_natural']),
            'theta_internal': copy.deepcopy(anchor_entry['theta_internal']), 'admitted': anchor_entry['admitted'],
            'valid': anchor_entry['valid'], 'log_index': anchor_entry['index'],
            'prediction': copy.deepcopy(anchor_entry['prediction']),
        }
        if verified_admitted(anchor_entry):
            set_primary(anchor_entry, 'seed', _interior_score(anchor_entry, row_ids, centre, halfwidth))

        # ---- stage 2: whole-log scan (A1) ----------------------------------------------
        out['stage_reached'] = 'log_scan'
        adm0 = admitted_entries()
        out['log_scan'] = {'entries_scanned': len(log), 'entries_before_exploration': log_start,
                           'admitted_log_indices': [int(e['index']) for e in adm0],
                           'valid_count': sum(1 for e in log if verified_valid(e))}
        if state['primary'] is None and adm0:
            e, sc = most_interior(adm0)
            set_primary(e, 'log_scan', sc)
            reasons.append(f'anchor not admitted; the evaluation log already holds admitted entr'
                           f'{"y" if len(adm0) == 1 else "ies"} {[int(x["index"]) for x in adm0]}: '
                           f'primary anchor = most interior one (log index {e["index"]}, purpose {e["purpose"]})')

        # ---- stage 3: linearised repair (only if nothing admitted yet) ----------------
        if state['primary'] is None:
            out['stage_reached'] = 'repair'
            rep = out['repair']
            if not verified_valid(anchor_entry):
                rep['terminated_by'] = 'anchor_invalid'
                reasons.append('anchor evaluation invalid; no valid point from which to repair')
            else:
                # S2 (v003): one phase only, inside span(identified). The v002 'numerical_rank' phase moved
                # near-null directions off the anchor's values and is removed; S3's absolute rule now
                # identifies the directions the data constrain in absolute terms.
                phases = []
                if ident:
                    phases.append(('identified', list(ident)))
                if not phases:
                    rep['terminated_by'] = 'no_direction'
                    reasons.append('anchor not admitted and no identified direction exists; repair impossible '
                                   '(not evidence of emptiness)')
                cur = anchor_entry
                for phase, dirs in phases:
                    P = np.zeros((n, len(row_ids)), dtype=float)
                    for k in dirs:
                        vk = V[k]
                        P += np.outer(vk, S @ vk) / (float(s[k]) ** 2)
                    cap = max_repair_step
                    terminated = None
                    used_here = 0
                    for it in range(int(repair_iterations)):
                        f_cur = _speeds_vector(cur, row_ids)
                        with np.errstate(over='ignore', invalid='ignore'):
                            r = (centre - f_cur) / sigma
                        g = _numeric_guard(r, 'repair residual') + _numeric_guard(P, 'repair projector')
                        if g:   # S1
                            terminated = 'numeric_range'
                            reasons.extend(g)
                            break
                        du = P @ r
                        du, mm_best, l2_best = _minimax_step(S, V, dirs, r, du)
                        norm = float(np.linalg.norm(du))
                        if not math.isfinite(norm):
                            terminated = 'numeric_range'
                            reasons.append('NUMERIC_RANGE: repair step is not finite; stopping the repair (S1)')
                            break
                        if norm > cap:
                            du = du * (cap / norm)
                        u_cur = np.array(cur['u'], dtype=float)
                        # S2: truncate the step LENGTH so the point stays in the box; never clip componentwise
                        alpha = _step_fraction_inside(u_cur, du)
                        u_new = np.clip(u_cur + alpha * du, 0.0, 1.0)   # clip only removes rounding (<= ulp)
                        disp = float(np.max(np.abs(u_new - u_cur))) if n else 0.0
                        if norm <= _ZERO_STEP or disp <= _ZERO_STEP:
                            terminated = 'no_displacement'
                            reasons.append(f'repair phase {phase!r} iteration {it}: linearised step produces no '
                                           f'displacement inside the box (norm {norm:.3e}, truncation {alpha:.3e});'
                                           f' stopping this phase')
                            break
                        need_budget()
                        e = evaluate(u_new, 'repair')
                        used_here += 1
                        rep['iterations_used'] += 1
                        nn = (V[near] @ (u_new - u_cur)) if near else np.zeros(0)
                        nn_max = float(np.max(np.abs(nn))) if nn.size else 0.0
                        rep['steps'].append({
                            'phase': phase, 'iteration': it, 'from_log_index': cur['index'], 'log_index': e['index'],
                            'unclipped_step_norm': norm, 'applied_step_norm': float(np.linalg.norm(u_new - u_cur)),
                            'cap': cap, 'valid': e['valid'], 'admitted': e['admitted'],
                            'step_length_fraction': float(alpha),
                            'max_norm_residual_l2_step': l2_best, 'max_norm_residual_step': mm_best,
                            'near_null_component': _floats(nn), 'near_null_component_max': nn_max,
                        })
                        if nn_max > _SLICE_TOL:
                            out['near_null_shifted'] = True
                            reasons.append(f'repair step at log index {e["index"]} moved near-null direction(s) '
                                           f'{near} by up to {nn_max:.3e} in u (rounding only; S2)')
                        if verified_admitted(e):
                            terminated = 'admitted'
                            set_primary(e, 'repair', _interior_score(e, row_ids, centre, halfwidth))
                            break
                        if e['valid']:
                            cur = e
                            cap = max_repair_step
                        else:
                            cap = 0.5 * min(cap, norm)   # review E3-M3: the retried step is really shorter
                    else:
                        terminated = ('iterations_exhausted' if int(repair_iterations) > 0
                                      else 'no_iterations_requested')
                    rep['phases'].append({'phase': phase, 'directions': [int(k) for k in dirs],
                                          'evaluations': used_here, 'terminated_by': terminated})
                    rep['terminated_by'] = terminated
                    if terminated == 'iterations_exhausted':
                        reasons.append(f'repair phase {phase!r}: repair_iterations={int(repair_iterations)} '
                                       f'reached (not evidence of emptiness)')
                    if state['primary'] is not None:
                        break

        # ---- stage 4: coarse global design before the march when nothing admitted ------
        if state['primary'] is None:
            if int(global_design_count) > 0:
                global_design(True)
            adm1 = admitted_entries()
            if adm1:
                e, sc = most_interior(adm1)
                set_primary(e, 'global_design' if e['purpose'] == 'global_design' else 'log_scan', sc)
            else:
                any_valid = any(verified_valid(e) for e in log)
                if not any_valid:
                    reasons.append('NO_VALID_EVALUATION: no valid evaluation in the whole log; nothing can be '
                                   'said about the admitted region (emptiness not examined)')
                    return finalise('NO_VALID_EVALUATION')
                reasons.append('NO_ADMITTED_POINT_FOUND: no admitted point was found in the whole evaluation log '
                               '(seed, Jacobian, repair' + (', coarse global design' if global_design_count else
                                                            '; global design not requested') +
                               '). This is NOT a proof that the DDO154 admitted region is empty '
                               '(empty_region=None, emptiness_proven=False); it must not be registered as '
                               '"the model family fails DDO154".')
                return finalise('NO_ADMITTED_POINT_FOUND')

        a = state['a']
        primary = state['primary']

        # ---- stage 5: march + bisection along identified directions (round 0) ---------
        for k in ident:
            for side, sgn in (('minus', -1.0), ('plus', 1.0)):
                out['stage_reached'] = 'march'
                d = sgn * V[k]
                rec = new_side_record(primary, k, side)
                detail[int(k)][side] = rec
                boundary[int(k)][side] = 0.0
                march_side(a, d, rec, round0_k=int(k), round0_side=side)

        # ---- stage 6: local Halton design inside the round-0 boundary box -------------
        out['stage_reached'] = 'design'
        m_id = len(ident)
        bases = _first_primes(m_id)
        first_index = int(rng_seed) + 1
        out['design']['bases'] = bases
        out['design']['first_index'] = first_index
        if m_id == 0:
            if int(design_count) > 0:
                reasons.append('no identified direction: local Halton design skipped (every design point would '
                               'coincide with the anchor)')
        else:
            width = {k: (boundary[int(k)]['minus'], boundary[int(k)]['plus']) for k in ident}
            for jj in range(int(design_count)):
                idx = first_index + jj
                p = a.copy()
                for pos, k in enumerate(ident):
                    h = _radical_inverse(idx, bases[pos])
                    bm, bp = width[k]
                    t_k = -bm + h * (bm + bp)
                    p = p + t_k * V[k]
                if not _inside_box(p):
                    out['design']['skipped_outside_box'] += 1
                    continue
                if already_evaluated(p):   # review E3-F8
                    out['design']['skipped_duplicate'] += 1
                    continue
                need_budget()
                evaluate(p, 'design')
                out['design']['evaluated'] += 1

        # ---- stage 7: coarse global design over the computational box (D7) -------------
        if not out['global_design']['completed'] and int(global_design_count) > 0:
            global_design(False)
        elif int(global_design_count) == 0:
            out['global_design']['completed'] = True
        state['core_done'] = True
    except _BudgetExhausted:
        reasons.append(f'BUDGET_EXHAUSTED at stage {out["stage_reached"]!r}: {counter["used"]} of '
                       f'{counter["budget"]} evaluations used; partial results preserved')
        # review E3-F7: an unfinished side is not a boundary
        for k in ident:
            for side in ('minus', 'plus'):
                rec = detail[int(k)][side]
                if rec is None or not rec.get('complete'):
                    boundary[int(k)][side] = None
                    out['boundary_cause'][int(k)][side] = 'UNFINISHED'
        out['refinement_status'] = 'NOT_REACHED'
        return finalise('BUDGET_EXHAUSTED')

    # ---- stage 8: iterated marches from extreme admitted points (D7) ------------------------
    out['stage_reached'] = 'iterated_march'
    hull_now = hull_of(admitted_entries())
    out['hull_history'].append({'after': 'core', 'hull_box': copy.deepcopy(hull_now)})
    if not ident:
        out['refinement_status'] = 'NO_IDENTIFIED_DIRECTION'
    elif int(max_march_rounds) == 0:
        out['refinement_status'] = 'NOT_REQUESTED'
    else:
        out['refinement_status'] = 'ROUNDS_EXHAUSTED'
        try:
            VI = V[list(ident)]
            SVI = S @ VI.T
            zrow = halfwidth / sigma
            A_lp = np.vstack([SVI, -SVI, VI.T, -VI.T])
            rays_done = []

            def extremes_of(adm):
                ext = {}
                for k in ident:
                    proj = [(float((np.array(e['u'], dtype=float) - a) @ V[k]), int(e['index']), e) for e in adm]
                    ext[(int(k), 'minus')] = min(proj, key=lambda x: (x[0], x[1]))
                    ext[(int(k), 'plus')] = min(proj, key=lambda x: (-x[0], x[1]))
                return ext

            for rnd in range(1, int(max_march_rounds) + 1):
                adm = admitted_entries()
                hull_before = hull_of(adm)
                round_rec = {'round': rnd, 'lp_rays': [], 'anchors': [], 'hull_before': hull_before,
                             'hull_after': None, 'growth': None, 'evaluations_before': counter['used'],
                             'evaluations': 0}
                out['march_rounds'].append(round_rec)
                # (a) linearised-polytope rays (review E3-F5): the polytope of the fixed seed Jacobian, re-based
                # at the current extreme admitted point, is maximised along +/-v_k by a small simplex; if its
                # extent beats the hull by more than hull_growth_tol, march from the primary anchor toward it.
                ext0 = extremes_of(adm)
                for kk, k in enumerate(ident):
                    for side, sgn in (('minus', -1.0), ('plus', 1.0)):
                        base = ext0[(int(k), side)][2]
                        ue = np.array(base['u'], dtype=float)
                        qe = (_speeds_vector(base, row_ids) - centre) / sigma
                        b_lp = np.concatenate([zrow - qe, zrow + qe, 1.0 - ue, ue])
                        w_lp = np.zeros(len(ident))
                        w_lp[kk] = sgn
                        c_lp, st = _lp_max(A_lp, b_lp, w_lp)
                        p_star = np.clip(ue + VI.T @ c_lp, 0.0, 1.0)
                        lin_ext = float((p_star - a) @ V[k])
                        cur_ext = hull_before[int(k)]['max' if side == 'plus' else 'min']
                        gain = sgn * (lin_ext - cur_ext)
                        ray = {'direction': int(k), 'side': side, 'base_log_index': int(base['index']),
                               'lp_status': st, 'linearised_extent': lin_ext, 'hull_extent': cur_ext,
                               'linearised_gain': float(gain), 'target_u': _floats(p_star), 'marched': False,
                               'skip_reason': None, 'side_record': None}
                        round_rec['lp_rays'].append(ray)
                        if st != 'OPTIMAL':
                            ray['skip_reason'] = f'linear program {st}'
                            continue
                        if not (gain > hull_growth_tol):
                            ray['skip_reason'] = 'linearised extent does not beat the hull by hull_growth_tol'
                            continue
                        dvec = p_star - a
                        L = float(np.linalg.norm(dvec))
                        if L <= _BOX_TOL:
                            ray['skip_reason'] = 'target coincides with the primary anchor'
                            continue
                        dunit = dvec / L
                        if any(float(np.max(np.abs(dunit - pr))) <= _RAY_DIR_TOL for pr in rays_done):
                            ray['skip_reason'] = 'ray direction already marched'
                            continue
                        rays_done.append(dunit)
                        rec = new_side_record(primary, k, side)
                        rec['kind'] = 'lp_ray'
                        rec['ray_direction_u'] = _floats(dunit)
                        rec['ray_target_t'] = L
                        ray['marched'] = True
                        ray['side_record'] = rec
                        march_side(a, dunit, rec)
                # (b) axis marches from unused admitted entries attaining an extreme projection
                adm = admitted_entries()
                cands, extremes = [], {}
                for (k, side), item in extremes_of(adm).items():
                    li = item[1]
                    extremes.setdefault(li, []).append((int(k), side))
                    if li not in used_anchor_indices and all(c['index'] != li for c in cands):
                        cands.append(item[2])
                if not cands and not any(r['marched'] for r in round_rec['lp_rays']):
                    round_rec['hull_after'] = hull_before
                    round_rec['growth'] = 0.0
                    out['refinement_status'] = 'CONVERGED_NO_NEW_EXTREME_ANCHOR'
                    break
                for c in cands:
                    used_anchor_indices.add(int(c['index']))
                    own = extremes.get(int(c['index']), [])
                    arec = {'log_index': int(c['index']), 'purpose': c['purpose'],
                            'extreme_of': [[k, sd] for k, sd in own], 'sides': []}
                    round_rec['anchors'].append(arec)
                    pc = np.array(c['u'], dtype=float)
                    # outward only, along each direction in which this point is extreme (oblique growth is the
                    # job of the linearised-polytope rays above; this keeps a round at <= 4m sides)
                    for k, side in own:
                        sgn = -1.0 if side == 'minus' else 1.0
                        rec = new_side_record(c, k, side)
                        arec['sides'].append(rec)
                        march_side(pc, sgn * V[k], rec)
                hull_after = hull_of(admitted_entries())
                growth = 0.0
                for k in ident:
                    hb, ha = hull_before[int(k)], hull_after[int(k)]
                    growth = max(growth, ha['max'] - hb['max'], hb['min'] - ha['min'])
                round_rec['hull_after'] = hull_after
                round_rec['growth'] = float(growth)
                round_rec['evaluations'] = counter['used'] - round_rec['evaluations_before']
                out['hull_history'].append({'after': f'round {rnd}', 'hull_box': copy.deepcopy(hull_after)})
                if growth <= hull_growth_tol:
                    out['refinement_status'] = 'CONVERGED'
                    break
        except _BudgetExhausted:
            out['refinement_status'] = 'BUDGET_EXHAUSTED'
            if out['march_rounds']:
                rr = out['march_rounds'][-1]
                rr['evaluations'] = counter['used'] - rr['evaluations_before']
                rr['hull_after'] = hull_of(admitted_entries())
            reasons.append(f'budget exhausted during iterated marches after {counter["used"]} of '
                           f'{counter["budget"]} evaluations: core exploration complete, hull convergence not '
                           f'verified (REGION_POSSIBLY_TRUNCATED)')
    if out['refinement_status'] == 'ROUNDS_EXHAUSTED':
        reasons.append(f'max_march_rounds={int(max_march_rounds)} reached while the hull box was still growing '
                       f'by more than hull_growth_tol={hull_growth_tol!r}')

    # ---- stage 9: summary -----------------------------------------------------------------
    out['stage_reached'] = 'summary'
    if any(abs(float((trial_u - ua) @ V[k])) > _SLICE_TOL for k in near):
        reasons.append('u_anchor differs from the trial values along near-null direction(s); trial_projection '
                       'and seed_projection are both reported (review E3-F3)')
    res = finalise('COMPLETE')
    if res['region_possibly_truncated']:
        reasons.append('REGION_POSSIBLY_TRUNCATED: ' + ', '.join(res['truncation_causes']))
    return res


@_fail_closed
def explore_region(*, forward, spec, region, u_anchor, identifiability, repair_iterations, max_repair_step,
                   march_step, bisection_steps, design_count, global_design_count, max_march_rounds,
                   hull_growth_tol, rng_seed, budget, log):
    """Deterministic exploration of the DDO154 admitted region around u_anchor.

    1. classify the anchor (evaluated here with purpose 'seed');
    2. scan the whole log for admitted entries (re-classified); the most interior one is the primary anchor
       when the anchor is not admitted;
    3. if still nothing admitted: damped linearised repair (fixed seed Jacobian) toward the rectangle centres,
       max-norm refined, first on the identified directions, then on every numerically non-zero direction;
    4. if still nothing admitted: coarse global Halton design over the whole box; if nothing is admitted the
       status is NO_ADMITTED_POINT_FOUND (or NO_VALID_EVALUATION) and emptiness is NOT asserted;
    5. doubling march +/- along each identified direction from the primary anchor, then bisection;
    6. local Halton design inside the round-0 boundary box; 7. global design (if not yet run);
    8. iterated marches from extreme admitted points until the hull box grows by <= hull_growth_tol;
    9. summary: INNER_SAMPLE admitted set, hull box, truncation causes, direction summaries.
    The log passed in may already hold this run's evaluations (they are scanned, step 2).
    """
    return _explore_impl(forward=forward, spec=spec, region=region, u_anchor=u_anchor,
                         identifiability=identifiability, repair_iterations=repair_iterations,
                         max_repair_step=max_repair_step, march_step=march_step,
                         bisection_steps=bisection_steps, design_count=design_count,
                         global_design_count=global_design_count, max_march_rounds=max_march_rounds,
                         hull_growth_tol=hull_growth_tol, rng_seed=rng_seed,
                         budget=budget, log=log, anchor_entry=None)


# --------------------------------------------------------------------------
# orchestration
# --------------------------------------------------------------------------

def _check_distance_binding(spec, region, binding):
    """D10: the DDO154 distance coordinate's box must equal the box derived from region.distance_summary."""
    rec = {'ok': False, 'name': None, 'modulus_half_width_multiple': None, 'derived_box': None,
           'coordinate_box': None, 'semantics': DISTANCE_BOX_SEMANTICS, 'reasons': []}
    rs = rec['reasons']
    if not isinstance(binding, dict) or set(binding.keys()) != {'name', 'modulus_half_width_multiple'}:
        rs.append("ddo154_distance must be a dict with exactly the keys 'name' and 'modulus_half_width_multiple'")
        return rec
    nm = binding['name']
    rec['name'] = nm if isinstance(nm, str) else None
    if not isinstance(nm, str) or nm not in spec['names']:
        rs.append('ddo154_distance.name must name a coordinate of the spec')
        return rec
    box = ddo154_distance_box(distance_summary=region.get('distance_summary'),
                              modulus_half_width_multiple=binding['modulus_half_width_multiple'])
    rec['modulus_half_width_multiple'] = box['modulus_half_width_multiple']
    if not box['ok']:
        rs.extend(box['reasons'])
        return rec
    rec['derived_box'] = {'lower': box['lower'], 'upper': box['upper'], 'central': box['central'],
                          'units': 'Mpc', 'modulus_mag': box['modulus_mag'],
                          'modulus_low_mag': box['modulus_low_mag'], 'modulus_high_mag': box['modulus_high_mag']}
    lo, hi = spec['lower'][nm], spec['upper'][nm]
    rec['coordinate_box'] = {'lower': lo, 'upper': hi, 'trial_value': spec['trial_values'][nm],
                             'units': spec['units'][nm], 'transform': spec['transforms'][nm],
                             'role': spec['roles'][nm], 'scope': spec['scopes'][nm]}
    if spec['units'][nm] != 'Mpc':
        rs.append(f'DDO154 distance coordinate {nm!r} must have units "Mpc"')
    if spec['scopes'][nm] != 'DDO154':
        rs.append(f'DDO154 distance coordinate {nm!r} must have scope "DDO154"')
    if spec['roles'][nm] not in ('nuisance', 'fixed'):
        rs.append(f'DDO154 distance coordinate {nm!r} must be a nuisance (or fixed), not a free shared constant')
    if spec['transforms'][nm] != 'log':
        rs.append(f'DDO154 distance coordinate {nm!r} must use the log transform (log D is linear in the modulus)')
    if abs(lo - box['lower']) > _DIST_MATCH_RTOL * box['lower'] or abs(hi - box['upper']) > _DIST_MATCH_RTOL * box['upper']:
        rs.append(f'DDO154 distance coordinate {nm!r} box [{lo!r}, {hi!r}] differs from the distance_summary box '
                  f'[{box["lower"]!r}, {box["upper"]!r}] (multiple {box["modulus_half_width_multiple"]!r})')
    rec['ok'] = not rs
    return rec


@_fail_closed
def run_calibration_region(*, forward, coordinates, observation_region_path, observation_region_sha256,
                           u_seed, budget, rel_step, min_step, max_halvings, null_tolerance,
                           repair_iterations, max_repair_step, march_step, bisection_steps, design_count,
                           global_design_count, max_march_rounds, hull_growth_tol, ddo154_distance,
                           rng_seed):
    """Orchestrate load -> spec -> distance binding -> Jacobian -> identifiability -> exploration.

    u_seed: list over varying coordinates (an entry None, or u_seed None, means the trial value).
    budget: maximum number of forward evaluations in total. The seed evaluation made for the Jacobian is
    reused as the exploration anchor, and the Jacobian evaluations are scanned by the exploration.
    ddo154_distance: {'name': coordinate name, 'modulus_half_width_multiple': k}; the coordinate's box must
    equal the box derived from the hash-verified region file's distance_summary.
    """
    out = {
        'ok': False, 'status': None, 'stage_reached': None, 'region': None, 'spec': None, 'jacobian': None,
        'identifiability': None, 'exploration': None, 'evaluation_log': [], 'evaluations_used': 0,
        'budget': None, 'u_seed_used': None, 'parameters': None, 'ddo154_distance_binding': None,
        'admitted_point_found': None, 'empty_region': None, 'emptiness_proven': False,
        'admitted_set_label': ADMITTED_SET_LABEL, 'region_possibly_truncated': None, 'truncation_causes': [],
        'flags': [], 'coordinate_units': None, 'shared_names': None, 'ddo154_scoped_names': None,
        'ngc3198_access': NGC3198_ACCESS, 'bounds_semantics': BOUNDS_SEMANTICS, 'module': MODULE_NAME,
        'exploration_fingerprint': None,
        'reasons': [],
    }
    reasons = out['reasons']
    if not callable(forward):
        reasons.append('forward must be callable')
    reasons.extend(_nonneg_int(budget, 'budget'))
    reasons.extend(_positive_float(rel_step, 'rel_step'))
    reasons.extend(_positive_float(min_step, 'min_step'))
    reasons.extend(_nonneg_int(max_halvings, 'max_halvings'))
    tol = _finite_float(null_tolerance)
    if tol is None or not (0.0 <= tol <= 1.0):
        reasons.append('null_tolerance must be a finite number in [0, 1]')
    reasons.extend(_nonneg_int(repair_iterations, 'repair_iterations'))
    reasons.extend(_positive_float(max_repair_step, 'max_repair_step'))
    reasons.extend(_positive_float(march_step, 'march_step'))
    reasons.extend(_nonneg_int(bisection_steps, 'bisection_steps'))
    reasons.extend(_nonneg_int(design_count, 'design_count'))
    reasons.extend(_nonneg_int(global_design_count, 'global_design_count'))
    reasons.extend(_nonneg_int(max_march_rounds, 'max_march_rounds'))
    reasons.extend(_nonneg_float(hull_growth_tol, 'hull_growth_tol'))
    reasons.extend(_nonneg_int(rng_seed, 'rng_seed'))
    if not reasons and float(min_step) > float(rel_step):
        reasons.append('min_step must not exceed rel_step')   # review E3-F6
    if not reasons and float(rel_step) > _MAX_REL_STEP:
        reasons.append(f'rel_step must not exceed {_MAX_REL_STEP}')
    if reasons:
        out['status'] = 'INPUT_INVALID'
        return out
    out['budget'] = int(budget)
    out['parameters'] = {
        'budget': int(budget), 'rel_step': float(rel_step), 'min_step': float(min_step),
        'max_halvings': int(max_halvings), 'null_tolerance': tol, 'repair_iterations': int(repair_iterations),
        'max_repair_step': float(max_repair_step), 'march_step': float(march_step),
        'bisection_steps': int(bisection_steps), 'design_count': int(design_count),
        'global_design_count': int(global_design_count), 'max_march_rounds': int(max_march_rounds),
        'hull_growth_tol': float(hull_growth_tol), 'rng_seed': int(rng_seed),
        'ddo154_distance': copy.deepcopy(ddo154_distance) if isinstance(ddo154_distance, dict) else None,
    }

    out['stage_reached'] = 'load_region'
    region = load_observation_region(path=observation_region_path, expected_sha256=observation_region_sha256)
    out['region'] = region
    if not region['ok']:
        reasons.append('observation region failed to load')
        reasons.extend(region['reasons'])
        out['status'] = 'INPUT_INVALID'
        return out

    out['stage_reached'] = 'spec'
    spec = make_coordinate_spec(coordinates=coordinates)
    out['spec'] = spec
    if not spec['ok']:
        reasons.append('coordinate specification invalid')
        reasons.extend(spec['reasons'])
        out['status'] = 'INPUT_INVALID'
        return out
    out['coordinate_units'] = dict(spec['units'])
    out['shared_names'] = list(spec['shared_names'])
    out['ddo154_scoped_names'] = list(spec['ddo154_scoped_names'])

    out['stage_reached'] = 'distance_binding'
    binding = _check_distance_binding(spec, region, ddo154_distance)
    out['ddo154_distance_binding'] = binding
    if not binding['ok']:
        reasons.append('DDO154 distance coordinate is not bound to region.distance_summary')
        reasons.extend(binding['reasons'])
        out['status'] = 'INPUT_INVALID'
        return out

    n = spec['n_varying']
    trial_u = []
    for nm in spec['varying_names']:
        tr = spec['transforms'][nm]
        x_lo, x_hi = _x_of(tr, spec['lower'][nm]), _x_of(tr, spec['upper'][nm])
        trial_u.append((_x_of(tr, spec['trial_values'][nm]) - x_lo) / (x_hi - x_lo))
    if u_seed is None:
        seed_list = list(trial_u)
    else:
        if isinstance(u_seed, np.ndarray):
            u_seed = u_seed.tolist()
        if not isinstance(u_seed, (list, tuple)) or len(u_seed) != n:
            reasons.append(f'u_seed must be None or a list of length {n} over the varying coordinates')
            out['status'] = 'INPUT_INVALID'
            return out
        seed_list = [trial_u[j] if x is None else x for j, x in enumerate(u_seed)]
    rs, u0 = _check_unit_vector(seed_list, n, 'u_seed')
    if rs:
        reasons.extend(rs)
        out['status'] = 'INPUT_INVALID'
        return out
    out['u_seed_used'] = _floats(u0)

    log = []
    out['evaluation_log'] = log

    def finish(status, ok):
        out['status'] = status
        out['ok'] = bool(ok)
        out['evaluations_used'] = len(log)
        return out

    out['stage_reached'] = 'jacobian'
    jac = finite_difference_jacobian(forward=forward, spec=spec, region=region, u0=_floats(u0),
                                     rel_step=rel_step, min_step=min_step, max_halvings=max_halvings,
                                     budget=int(budget), log=log)
    out['jacobian'] = jac
    if jac['status'] == 'BUDGET_EXHAUSTED':
        reasons.append('budget exhausted during the Jacobian stage; partial results preserved')
        reasons.extend(jac['reasons'])
        return finish('BUDGET_EXHAUSTED', False)
    if jac['status'] == 'SEED_INVALID' or not jac['seed_valid']:
        reasons.append('seed evaluation invalid; no Jacobian (the admitted region was not examined)')
        reasons.extend(jac['reasons'])
        return finish('SEED_INVALID', False)
    if jac['failed_columns']:
        reasons.append('Jacobian has failed columns; exploration not run')
        reasons.extend(jac['reasons'])
        return finish('JACOBIAN_INCOMPLETE', False)
    if not jac['ok']:
        reasons.append('Jacobian stage failed')
        reasons.extend(jac['reasons'])
        return finish('JACOBIAN_FAILED', False)

    out['stage_reached'] = 'identifiability'
    idn = identifiability_report(jacobian_u=jac['jacobian_u'], sigmas=region['sigmas'], row_ids=region['row_ids'],
                                 varying_names=spec['varying_names'], null_tolerance=null_tolerance)
    out['identifiability'] = idn
    if not idn['ok']:
        if idn.get('numeric_guard'):
            reasons.append('identifiability refused before the SVD: the scaled Jacobian is outside the safe '
                           'numeric range (S1); exploration not run')
            reasons.extend(idn['reasons'])
            return finish('NUMERIC_RANGE_REFUSED', False)
        reasons.append('identifiability report failed (incomplete Jacobian or bad input); exploration not run')
        reasons.extend(idn['reasons'])
        return finish('JACOBIAN_INCOMPLETE', False)

    out['stage_reached'] = 'exploration'
    seed_entry = log[jac['seed_log_index']]
    remaining = int(budget) - len(log)
    exp = _explore_impl(forward=forward, spec=spec, region=region, u_anchor=_floats(u0), identifiability=idn,
                        repair_iterations=repair_iterations, max_repair_step=max_repair_step,
                        march_step=march_step, bisection_steps=bisection_steps, design_count=design_count,
                        global_design_count=global_design_count, max_march_rounds=max_march_rounds,
                        hull_growth_tol=hull_growth_tol, rng_seed=rng_seed, budget=remaining, log=log,
                        anchor_entry=seed_entry)
    out['exploration'] = exp
    if exp['status'] is None:
        reasons.append('exploration rejected its inputs')
        reasons.extend(exp['reasons'])
        return finish('EXPLORATION_FAILED', False)
    out['stage_reached'] = f'exploration:{exp["stage_reached"]}'
    out['admitted_point_found'] = exp['admitted_point_found']
    out['empty_region'] = exp['empty_region']
    out['region_possibly_truncated'] = exp['region_possibly_truncated']
    out['truncation_causes'] = list(exp['truncation_causes'])
    out['flags'] = list(exp['flags'])
    fp = exploration_fingerprint(exploration=exp, region_sha256=region['sha256'])
    out['exploration_fingerprint'] = fp['fingerprint'] if fp['ok'] else None
    if exp['status'] != 'COMPLETE' or exp['reasons']:
        reasons.extend(exp['reasons'])
    return finish(exp['status'], exp['ok'])


# --------------------------------------------------------------------------
# P34-16: registration record of every calibration run
# --------------------------------------------------------------------------

def _fingerprint_payload(admitted_points, region_sha256):
    """The object whose canonical bytes are hashed. prediction_freeze_c2v003 builds the same object from
    the admitted points it receives (log_index, u) and the region sha, so the two can be compared."""
    pts = []
    for p in admitted_points:
        pts.append([int(p['log_index']), [float(x) for x in p['u']]])
    pts.sort(key=lambda t: t[0])
    return {'schema': FINGERPRINT_SCHEMA, 'region_sha256': region_sha256, 'admitted': pts}


@_fail_closed
def exploration_fingerprint(*, exploration, region_sha256):
    """sha256 of the canonical admitted set {schema, region_sha256, [[log_index, u], ...] sorted by log_index}.

    It identifies an exploration's admitted set independently of the module that holds it; the freeze module
    recomputes it from the points it was given and stores it in the manifest (calibration_fingerprint)."""
    out = {'ok': False, 'fingerprint': None, 'n_admitted': 0, 'schema': FINGERPRINT_SCHEMA, 'reasons': []}
    if not isinstance(exploration, dict) or not isinstance(exploration.get('admitted_points'), list):
        out['reasons'].append('exploration must be an explore_region / run exploration dict')
        return out
    if not _is_hex64(region_sha256):
        out['reasons'].append('region_sha256 must be a 64-character hexadecimal str')
        return out
    payload = _fingerprint_payload(exploration['admitted_points'], region_sha256.lower())
    out.update({'ok': True, 'fingerprint': hashlib.sha256(_canonical_bytes(payload)).hexdigest(),
                'n_admitted': len(payload['admitted'])})
    return out


def _run_fingerprint(run):
    """X1 (v003a): (fingerprint, None) recomputed from the run CONTENT -- exploration.admitted_points and
    region.sha256 -- or (None, None) when the run has no exploration (INPUT_INVALID, SEED_INVALID, ...), or
    (None, reason) when an exploration is present but cannot be fingerprinted. run['exploration_fingerprint']
    is never read here."""
    ex = run.get('exploration')
    if ex is None:
        return None, None
    if not isinstance(ex, dict) or not isinstance(ex.get('admitted_points'), list):
        return None, 'run.exploration is present but carries no admitted_points list'
    region = run.get('region')
    rsha = region.get('sha256') if isinstance(region, dict) else None
    if not _is_hex64(rsha):
        return None, 'run.exploration is present but run.region.sha256 is not 64-hex'
    fp = exploration_fingerprint(exploration=ex, region_sha256=rsha)
    if not fp.get('ok'):
        return None, 'exploration fingerprint not computable from the run content: %s' % (fp.get('reasons'),)
    return fp['fingerprint'], None


def _read_regular_file(path):
    """(bytes, None) or (None, reason); regular files only, non-blocking open (A4 lesson)."""
    if not isinstance(path, str) or not path:
        return None, 'path must be a non-empty str'
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0))
    except (OSError, ValueError) as exc:
        return None, f'cannot open {path!r}: {type(exc).__name__}: {_safe_str(exc)}'
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            return None, f'not a regular file: {path!r}'
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b)
        return b''.join(chunks), None
    except (OSError, ValueError) as exc:
        return None, f'cannot read {path!r}: {type(exc).__name__}: {_safe_str(exc)}'
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


@_fail_closed
def write_calibration_record(*, run, record_path, registry_path):
    """P34-16: write a registration record of ONE calibration run, whatever its status (COMPLETE, empty,
    BUDGET_EXHAUSTED, INPUT_INVALID, SEED_INVALID, ...), then append it to an append-only registry.

    record_path: exclusive create (never overwritten). Content: canonical JSON (keys as str, P34-15) of
    {schema, created_utc, module, module_file_sha256, status, ok, stage_reached, region_sha256,
    exploration_fingerprint, run (the complete run output including the evaluation log)} plus its own
    self-hash record_sha256 over the body.
    registry_path: one JSON line appended per record {schema, created_utc, record_path, record_file_sha256,
    status, exploration_fingerprint, registry_prefix_sha256 (sha256 of the registry bytes before this line),
    line_sha256}; the prefix hash chains every earlier run, so a deleted or edited earlier line is detectable.
    Log record_file_sha256 externally (FROM_ message) together with the freeze registration.
    v003a (X1): exploration_fingerprint is RECOMPUTED from the run content (exploration.admitted_points and
    region.sha256), never copied from run['exploration_fingerprint']; a run whose reported fingerprint is not
    None and differs from the recomputed one was edited after the engine returned it and is refused.
    The freeze module pins this record (mandatory in prediction_freeze_c2v003a) and recomputes it again.
    """
    out = {'ok': False, 'record_path': None, 'record_file_sha256': None, 'record_sha256': None,
           'registry_path': None, 'registry_line_sha256': None, 'registry_prefix_sha256': None,
           'status': None, 'exploration_fingerprint': None, 'reasons': []}
    reasons = out['reasons']
    if not isinstance(run, dict) or 'status' not in run or 'reasons' not in run:
        reasons.append('run must be a run_calibration_region output (any status)')
        return out
    for label, p in (('record_path', record_path), ('registry_path', registry_path)):
        if not isinstance(p, str) or not p:
            reasons.append(f'{label} must be a non-empty str')
    if reasons:
        return out
    # X1 (v003a): recompute the fingerprint from the run content; never copy the run's own field
    fp_recomputed, fp_err = _run_fingerprint(run)
    if fp_err is not None:
        reasons.append(f'REFUSED (P34-16/X1): {fp_err}')
        return out
    fp_reported = run.get('exploration_fingerprint')
    if fp_reported is not None and fp_reported != fp_recomputed:
        reasons.append(f'REFUSED (P34-16/X1): run exploration_fingerprint {_safe_str(fp_reported)} differs from the '
                       f'fingerprint {fp_recomputed} recomputed from the run content (run edited after the engine)')
        return out
    rp, gp = os.path.abspath(record_path), os.path.abspath(registry_path)
    if rp == gp:
        reasons.append('record_path and registry_path must differ')
        return out
    if os.path.lexists(rp):
        reasons.append(f'REFUSED: record_path already exists (no overwrite): {rp}')
        return out
    for p in (rp, gp):
        if not os.path.isdir(os.path.dirname(p)):
            reasons.append(f'parent directory does not exist: {os.path.dirname(p)}')
    if reasons:
        return out
    prefix = b''
    if os.path.lexists(gp):
        raw, err = _read_regular_file(gp)
        if raw is None:
            reasons.append(f'REFUSED: registry unreadable: {err}')
            return out
        prefix = raw
    me_raw, me_err = _read_regular_file(os.path.realpath(__file__))
    region = run.get('region') if isinstance(run.get('region'), dict) else {}
    body = {
        'schema': CALIBRATION_RECORD_SCHEMA,
        'created_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'module': MODULE_NAME,
        'module_file_sha256': (hashlib.sha256(me_raw).hexdigest() if me_raw is not None else None),
        'status': _safe_str(run.get('status')),
        'ok': bool(run.get('ok') is True),
        'stage_reached': _safe_str(run.get('stage_reached')),
        'region_sha256': region.get('sha256'),
        'exploration_fingerprint': fp_recomputed,
        'ngc3198_access': NGC3198_ACCESS,
        'run': run,
    }
    try:
        body_bytes = _canonical_bytes(body)
    except (ValueError, TypeError, RecursionError) as exc:
        reasons.append(f'run is not canonically serialisable: {type(exc).__name__}: {_safe_str(exc)}')
        return out
    rec = json.loads(body_bytes.decode('utf-8'))
    rec['record_sha256'] = hashlib.sha256(body_bytes).hexdigest()
    payload = _canonical_bytes(rec)
    try:
        with open(rp, 'xb') as fh:
            fh.write(payload)
    except (OSError, ValueError) as exc:
        reasons.append(f'REFUSED: could not create record_path: {type(exc).__name__}: {_safe_str(exc)}')
        return out
    back, err = _read_regular_file(rp)
    if back != payload:
        reasons.append(f'read-back mismatch after writing the record: {err or "bytes differ"}')
        return out
    file_sha = hashlib.sha256(payload).hexdigest()
    line = {'schema': CALIBRATION_REGISTRY_SCHEMA, 'created_utc': body['created_utc'], 'record_path': rp,
            'record_file_sha256': file_sha, 'status': body['status'],
            'exploration_fingerprint': body['exploration_fingerprint'],
            'registry_prefix_sha256': hashlib.sha256(prefix).hexdigest()}
    line['line_sha256'] = hashlib.sha256(_canonical_bytes(line)).hexdigest()
    lb = _canonical_bytes(line) + b'\n'
    try:
        fd = os.open(gp, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
        try:
            st = os.fstat(fd)
            if not stat.S_ISREG(st.st_mode) or st.st_size != len(prefix):
                reasons.append('REFUSED: registry changed or is not a regular file between read and append')
                return out
            os.write(fd, lb)
        finally:
            os.close(fd)
    except (OSError, ValueError) as exc:
        reasons.append(f'RECORD WRITTEN BUT REGISTRY APPEND FAILED: {type(exc).__name__}: {_safe_str(exc)}')
        out.update({'record_path': rp, 'record_file_sha256': file_sha, 'record_sha256': rec['record_sha256']})
        return out
    out.update({'ok': True, 'record_path': rp, 'record_file_sha256': file_sha, 'record_sha256': rec['record_sha256'],
                'registry_path': gp, 'registry_line_sha256': line['line_sha256'],
                'registry_prefix_sha256': line['registry_prefix_sha256'], 'status': body['status'],
                'exploration_fingerprint': body['exploration_fingerprint']})
    return out


@_fail_closed
def verify_calibration_record(*, record_path, registry_path):
    """Verify a calibration record (canonical bytes, self-hash) and, when registry_path is a str, that the
    registry is an unbroken hash chain containing exactly one line for this record's file hash.
    v003a (X1): the exploration fingerprint is recomputed from the recorded run content and must equal the
    stored exploration_fingerprint."""
    out = {'ok': False, 'record_file_sha256': None, 'record_sha256': None, 'status': None,
           'exploration_fingerprint': None, 'exploration_fingerprint_recomputed': None,
           'region_sha256': None, 'registry_lines': None,
           'registry_chain_ok': None, 'reasons': []}
    reasons = out['reasons']
    raw, err = _read_regular_file(record_path)
    if raw is None:
        reasons.append(err)
        return out
    out['record_file_sha256'] = hashlib.sha256(raw).hexdigest()
    try:
        doc = json.loads(raw.decode('utf-8'))
    except Exception as exc:
        reasons.append(f'record is not JSON: {type(exc).__name__}')
        return out
    if not isinstance(doc, dict) or doc.get('schema') != CALIBRATION_RECORD_SCHEMA or 'record_sha256' not in doc:
        reasons.append('not a CALIBRATION_RUN_RECORD_C2V003 document')
        return out
    body = {k: v for k, v in doc.items() if k != 'record_sha256'}
    if hashlib.sha256(_canonical_bytes(body)).hexdigest() != doc['record_sha256']:
        reasons.append('record_sha256 mismatch')
    if _canonical_bytes(doc) != raw:
        reasons.append('record bytes are not canonical')
    out.update({'record_sha256': doc.get('record_sha256'), 'status': doc.get('status'),
                'exploration_fingerprint': doc.get('exploration_fingerprint'),
                'region_sha256': doc.get('region_sha256')})
    # X1 (v003a): recompute the fingerprint from the recorded run content and compare with the stored one
    run = doc.get('run')
    if not isinstance(run, dict):
        reasons.append('record carries no run object')
    else:
        fp_recomputed, fp_err = _run_fingerprint(run)
        out['exploration_fingerprint_recomputed'] = fp_recomputed
        if fp_err is not None:
            reasons.append(f'record run content cannot be fingerprinted: {fp_err}')
        elif fp_recomputed != doc.get('exploration_fingerprint'):
            reasons.append(f'record exploration_fingerprint {_safe_str(doc.get("exploration_fingerprint"))} differs '
                           f'from the fingerprint {fp_recomputed} recomputed from the recorded run content (X1)')
        region = run.get('region')
        if (region.get('sha256') if isinstance(region, dict) else None) != doc.get('region_sha256'):
            reasons.append('record region_sha256 differs from the recorded run.region.sha256')
    if registry_path is not None:
        g, gerr = _read_regular_file(registry_path)
        if g is None:
            reasons.append(f'registry unreadable: {gerr}')
        else:
            lines = g.split(b'\n')
            if lines and lines[-1] == b'':
                lines = lines[:-1]
            prefix = b''
            chain_ok, hits = True, 0
            for ln in lines:
                try:
                    d = json.loads(ln.decode('utf-8'))
                    lsha = d.pop('line_sha256')
                    if hashlib.sha256(_canonical_bytes(d)).hexdigest() != lsha or \
                            d.get('registry_prefix_sha256') != hashlib.sha256(prefix).hexdigest():
                        chain_ok = False
                    if d.get('record_file_sha256') == out['record_file_sha256']:
                        hits += 1
                except Exception:
                    chain_ok = False
                prefix += ln + b'\n'
            out['registry_lines'] = len(lines)
            out['registry_chain_ok'] = chain_ok
            if not chain_ok:
                reasons.append('registry hash chain broken')
            if hits != 1:
                reasons.append(f'record appears {hits} times in the registry (expected exactly 1)')
    out['ok'] = not reasons
    return out
