"""calibration_region_engine_c3v001 -- Module 1 of dispatch 0462 (Claude3 lane, V001).

DDO154 calibration-region engine implementing INTERFACE_0462_V001.md:
finite-difference Jacobian at a root-supplied seed, SVD identifiability
report, deterministic exploration of the identified subspace (linearised
repair, directional march + bisection, Halton design) and the orchestrating
``run_calibration_region``.

Conventions (frozen interface):
  * inert at import: no file I/O, no computation, no environment changes;
  * every public function takes keyword-only arguments with no defaults and
    returns a dict with at least ``ok: bool`` and ``reasons: list[str]``;
    anticipated bad input returns ``ok=False`` and never raises;
  * exceptions raised by the root-supplied ``forward`` callable are caught,
    logged in the evaluation log and treated as invalid evaluations;
  * no numpy object escapes: all returned arrays are plain lists of floats;
  * single-threaded numerics; the module never spawns threads or processes;
  * no NGC3198 data is read, referenced or needed anywhere in this module.

Standard library + numpy only (no scipy).
"""

import hashlib
import json
import math

import numpy as np

__all__ = [
    'load_observation_region',
    'make_coordinate_spec',
    'to_natural',
    'to_unit',
    'classify_prediction',
    'finite_difference_jacobian',
    'identifiability_report',
    'explore_region',
    'run_calibration_region',
]

MODULE_NAME = 'calibration_region_engine_c3v001'
BOUNDS_SEMANTICS = 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'
NGC3198_ACCESS = 'NONE'
PURPOSES = ('seed', 'jacobian', 'repair', 'march', 'bisection', 'design')
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

_BOX_TOL = 1e-12   # tolerance for the "inside [0,1]^n" test of computed points
_U_TOL = 1e-9      # tolerance when converting natural -> unit (rounding at the box faces)
_T_TOL = 1e-9      # tolerance on march parameter comparisons
_ZERO_STEP = 1e-15  # a repair displacement below this is "no displacement"


# --------------------------------------------------------------------------
# small validation helpers
# --------------------------------------------------------------------------

class _BudgetExhausted(Exception):
    """Internal control-flow signal for the exploration; never escapes."""


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
    return x is True or (isinstance(x, np.bool_) and bool(x))


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


def _validate_coordinate(label, transform, lower, upper, trial_value, role):
    reasons = []
    if transform not in TRANSFORMS:
        reasons.append(f'{label}: transform must be one of {TRANSFORMS}')
    if role not in ROLES:
        reasons.append(f'{label}: role must be one of {ROLES}')
    lo = _finite_float(lower)
    hi = _finite_float(upper)
    tv = _finite_float(trial_value)
    if lo is None or hi is None:
        reasons.append(f'{label}: lower and upper must be finite numbers')
    if tv is None:
        reasons.append(f'{label}: trial_value must be a finite number')
    if reasons:
        return reasons
    if transform == 'log' and not (0.0 < lo < hi):
        reasons.append(f'{label}: log transform requires 0 < lower < upper')
    elif transform == 'linear' and not (lo < hi):
        reasons.append(f'{label}: linear transform requires lower < upper')
    if not (lo <= tv <= hi):
        reasons.append(f'{label}: trial_value must lie in [lower, upper]')
    return reasons


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
    for key in ('roles', 'transforms', 'lower', 'upper', 'trial_values'):
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
        rs = _validate_coordinate(f'coordinate {nm!r}', tr, lo, hi, tv, role)
        if rs:
            reasons.extend(rs)
            continue
        is_varying = nm in set(varying)
        if (role == 'fixed') == is_varying:
            reasons.append(f'coordinate {nm!r}: role {role!r} inconsistent with varying/fixed lists')
            continue
        coords[nm] = {
            'transform': tr, 'role': role,
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


# --------------------------------------------------------------------------
# observation region
# --------------------------------------------------------------------------

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
        reasons.append(f'cannot read observation-region file: {type(exc).__name__}: {exc}')
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
        reasons.append(f'observation-region file is not valid UTF-8 JSON: {type(exc).__name__}: {exc}')
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

def make_coordinate_spec(*, coordinates):
    """Build the coordinate specification from a list of coordinate dicts.

    Each coordinate: {'name', 'transform': 'log'|'linear', 'lower', 'upper',
    'role': 'free'|'fixed'|'nuisance', 'trial_value'}. Varying coordinates
    (free + nuisance) keep the given order; fixed coordinates stay at trial_value.
    roles/transforms/lower/upper/trial_values are returned as dicts keyed by name.
    """
    out = {
        'ok': False, 'names': [], 'varying_names': [], 'fixed_names': [], 'nuisance_names': [],
        'free_names': [], 'roles': {}, 'transforms': {}, 'lower': {}, 'upper': {}, 'trial_values': {},
        'varying_index': {}, 'n_total': 0, 'n_varying': 0,
        'bounds_semantics': BOUNDS_SEMANTICS, 'reasons': [],
    }
    reasons = out['reasons']
    if not isinstance(coordinates, (list, tuple)) or not coordinates:
        reasons.append('coordinates must be a non-empty list of coordinate dicts')
        return out
    names, varying, fixed, nuisance, free = [], [], [], [], []
    roles, transforms, lower, upper, trial = {}, {}, {}, {}, {}
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
        missing = [f for f in ('transform', 'lower', 'upper', 'role', 'trial_value') if f not in c]
        if missing:
            reasons.append(f'coordinates[{k}] ({nm}): missing fields {missing}')
            continue
        rs = _validate_coordinate(f'coordinates[{k}] ({nm})', c['transform'], c['lower'], c['upper'],
                                  c['trial_value'], c['role'])
        if rs:
            reasons.extend(rs)
            continue
        names.append(nm)
        roles[nm] = c['role']
        transforms[nm] = c['transform']
        lower[nm] = float(c['lower'])
        upper[nm] = float(c['upper'])
        trial[nm] = float(c['trial_value'])
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
        'trial_values': trial, 'varying_index': {nm: j for j, nm in enumerate(varying)},
        'n_total': len(names), 'n_varying': len(varying), 'ok': True,
    })
    return out


def to_natural(*, spec, u):
    """Map unit coordinates u (list over varying coords, in [0,1]) to natural values.

    theta_natural: dict over every coordinate (fixed coordinates at trial_value);
    theta_internal: list over every coordinate in spec.names order (x = ln v for log, v for linear).
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
            x = float(x_var[vidx[nm]])
            v = _v_of(c['transform'], x)
            if c['transform'] == 'log':
                v = min(c['upper'], max(c['lower'], v))  # rounding guard at the box faces
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


def to_unit(*, spec, theta_natural):
    """Map natural values (dict with every varying coordinate) to unit coordinates in [0,1]."""
    out = {'ok': False, 'u': None, 'reasons': []}
    reasons, info = _check_spec(spec)
    if reasons:
        out['reasons'] = reasons
        return out
    if not isinstance(theta_natural, dict):
        out['reasons'] = ['theta_natural must be a dict keyed by coordinate name']
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
            clean_speeds[str(k)] = _finite_float(v)
    rsn = raw.get('reasons')
    clean_reasons = [str(r) for r in rsn] if isinstance(rsn, (list, tuple)) else []
    return {'speeds_km_s': clean_speeds, 'valid': bool(_is_true(raw.get('valid'))), 'reasons': clean_reasons}


def classify_prediction(*, prediction, rectangles, row_ids):
    """Classify a forward return value against the closed rectangles.

    valid: dict with valid is True, every row id present, every value a finite number.
    admitted: True/False when valid (all rows inside [low, high]); None when invalid.
    row_inside[row_id]: True/False where a finite value exists, None otherwise.
    """
    out = {'ok': False, 'valid': False, 'admitted': None, 'row_inside': {}, 'speeds_km_s': None,
           'outside_rows': [], 'forward_reasons': [], 'reasons': []}
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
        reasons.append('prediction is not a dict; evaluation invalid')
        return out
    valid = True
    if not _is_true(prediction.get('valid')):
        reasons.append("forward did not report valid is True")
        valid = False
    fr = prediction.get('reasons')
    if isinstance(fr, (list, tuple)):
        out['forward_reasons'] = [str(x) for x in fr]
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

    The caller checks the budget before calling. Exceptions from forward are caught and
    recorded; the evaluation is then invalid.
    """
    u_list = _floats(np.clip(np.asarray(u, dtype=float), 0.0, 1.0))
    entry = {
        'index': len(log), 'purpose': purpose, 'u': u_list, 'theta_internal': None,
        'theta_natural': None, 'prediction': None, 'valid': False, 'admitted': None,
        'row_inside': {rid: None for rid in region['row_ids']}, 'reasons': [], 'exception': None,
    }
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
        entry['exception'] = f'{type(exc).__name__}: {exc}'
        entry['reasons'].append('forward raised an exception; evaluation invalid')
        log.append(entry)
        return entry
    entry['prediction'] = _sanitize_prediction(raw)
    cls = classify_prediction(prediction=raw, rectangles=region['rectangles'], row_ids=region['row_ids'])
    entry['valid'] = bool(cls['valid'])
    entry['admitted'] = cls['admitted']
    entry['row_inside'] = dict(cls['row_inside'])
    entry['reasons'].extend(cls['reasons'])
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

def finite_difference_jacobian(*, forward, spec, region, u0, rel_step, min_step, max_halvings, budget, log):
    """Central-difference Jacobian d(speeds)/d(u) at the seed u0.

    Column j starts with step rel_step (u units) clipped to the box on each side
    (a side clipped to zero reuses the seed value f0). If either evaluated side is
    invalid, the step is halved (at most max_halvings times, never below min_step)
    and both sides are re-evaluated. A column that never succeeds is listed in
    failed_columns and its entries are None. Every forward call is appended to log.
    """
    out = {
        'ok': False, 'status': None, 'f0': None, 'seed_valid': False, 'seed_admitted': None,
        'seed_log_index': None, 'u0': None, 'jacobian_u': None, 'steps_used': [], 'steps_detail': [],
        'failed_columns': [], 'evaluations_used': 0, 'budget': None, 'row_ids': [], 'varying_names': [],
        'bounds_semantics': BOUNDS_SEMANTICS, 'reasons': [],
    }
    reasons, info = _common_eval_checks(forward, spec, region, log, budget)
    reasons.extend(_positive_float(rel_step, 'rel_step'))
    reasons.extend(_positive_float(min_step, 'min_step'))
    reasons.extend(_nonneg_int(max_halvings, 'max_halvings'))
    if not reasons and not (float(min_step) <= float(rel_step)):
        reasons.append('min_step must not exceed rel_step')
    if info is not None:
        rs, uu = _check_unit_vector(u0, info['n'], 'u0')
        reasons.extend(rs)
    if reasons:
        out['reasons'] = reasons
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
        h = rel_step
        halvings = 0
        col_reasons = []
        done = False
        while True:
            h_p = min(h, 1.0 - float(uu[j]))
            h_m = min(h, float(uu[j]))
            if h_p + h_m < min_step:
                col_reasons.append(f'clipped step {h_p + h_m:.3e} below min_step')
                break
            f_p = f_m = None
            side_reasons = []
            if h_p > 0.0:
                if counter['used'] >= counter['budget']:
                    exhausted = True
                    break
                up = uu.copy()
                up[j] = float(uu[j]) + h_p
                ep = _evaluate_point(forward=forward, spec=spec, region=region, u=up, purpose='jacobian',
                                     log=log, counter=counter)
                if ep['valid']:
                    f_p = _speeds_vector(ep, row_ids)
                else:
                    side_reasons.append(f'+side at step {h_p:.3e} invalid (log index {ep["index"]})')
            else:
                f_p = f0
            if h_m > 0.0:
                if counter['used'] >= counter['budget']:
                    exhausted = True
                    break
                um = uu.copy()
                um[j] = float(uu[j]) - h_m
                em = _evaluate_point(forward=forward, spec=spec, region=region, u=um, purpose='jacobian',
                                     log=log, counter=counter)
                if em['valid']:
                    f_m = _speeds_vector(em, row_ids)
                else:
                    side_reasons.append(f'-side at step {h_m:.3e} invalid (log index {em["index"]})')
            else:
                f_m = f0
            if f_p is not None and f_m is not None:
                col = (f_p - f_m) / (h_p + h_m)
                for i in range(m):
                    J[i][j] = float(col[i])
                steps_used[j] = float(h)
                steps_detail[j] = {'nominal_step': float(h), 'plus_step': float(h_p),
                                   'minus_step': float(h_m), 'halvings': int(halvings),
                                   'one_sided': bool(h_p == 0.0 or h_m == 0.0)}
                done = True
                break
            col_reasons.extend(side_reasons)
            if halvings >= int(max_halvings):
                col_reasons.append(f'max_halvings={int(max_halvings)} reached')
                break
            halvings += 1
            h = 0.5 * h
            if h < min_step:
                col_reasons.append(f'halved step {h:.3e} below min_step={min_step:.3e}')
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
    out['ok'] = True
    return finish('COMPLETE')


# --------------------------------------------------------------------------
# identifiability
# --------------------------------------------------------------------------

def _fix_signs(vt):
    """Make the largest-magnitude component of each right vector positive (deterministic SVD signs)."""
    vt = np.array(vt, dtype=float, copy=True)
    for k in range(vt.shape[0]):
        idx = int(np.argmax(np.abs(vt[k])))
        if vt[k, idx] < 0:
            vt[k] = -vt[k]
    return vt


def identifiability_report(*, jacobian_u, sigmas, row_ids, varying_names, null_tolerance):
    """SVD identifiability report of the sigma-scaled Jacobian diag(1/sigma) . J_u.

    Direction i (row i of right_vectors) is identified iff s_i >= null_tolerance * s_max,
    otherwise near-null. condition_numbers[i] = s_max / s_i ("inf" if s_i == 0).
    Any None entry in jacobian_u makes the report ok=False.
    """
    out = {
        'ok': False, 'scaled_jacobian': None, 'singular_values': None, 'right_vectors': None,
        'identified': [], 'near_null': [], 'condition_numbers': None, 'null_tolerance': None,
        's_max': None, 'n_directions': None, 'row_ids': [], 'varying_names': [], 'reasons': [],
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
    S = J / sig[:, None]
    try:
        _, s, vt = np.linalg.svd(S, full_matrices=True)
    except Exception as exc:
        reasons.append(f'SVD failed: {type(exc).__name__}: {exc}')
        return out
    s_full = np.zeros(n, dtype=float)
    s_full[:len(s)] = s
    vt = _fix_signs(vt)
    s_max = float(s_full[0]) if n > 0 else 0.0
    identified, near_null, cond = [], [], []
    for i in range(n):
        si = float(s_full[i])
        if s_max > 0.0 and si >= tol * s_max and si > 0.0:
            identified.append(i)
        else:
            near_null.append(i)
        cond.append(float(s_max / si) if si > 0.0 else 'inf')
    if s_max <= 0.0:
        reasons.append('scaled Jacobian is identically zero: no direction is identified')
    out.update({
        'ok': True, 'scaled_jacobian': _matrix(S), 'singular_values': _floats(s_full),
        'right_vectors': _matrix(vt), 'identified': identified, 'near_null': near_null,
        'condition_numbers': cond, 'null_tolerance': tol, 's_max': s_max, 'n_directions': n,
        'row_ids': list(row_ids), 'varying_names': list(varying_names),
    })
    return out


# --------------------------------------------------------------------------
# exploration
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
    """Largest t >= 0 with a + t d inside [0,1]^n (inf if d == 0)."""
    t_edge = math.inf
    for j in range(len(a)):
        dj = float(d[j])
        if dj > 0.0:
            t_edge = min(t_edge, (1.0 - float(a[j])) / dj)
        elif dj < 0.0:
            t_edge = min(t_edge, (0.0 - float(a[j])) / dj)
    return max(0.0, t_edge)


def _inside_box(p):
    return bool(np.all(p >= -_BOX_TOL) and np.all(p <= 1.0 + _BOX_TOL))


def _point_from_entry(entry):
    return {
        'u': list(entry['u']), 'theta_internal': entry['theta_internal'], 'theta_natural': entry['theta_natural'],
        'prediction': entry['prediction'], 'log_index': entry['index'], 'purpose': entry['purpose'],
        'valid': entry['valid'], 'admitted': entry['admitted'], 'row_inside': entry['row_inside'],
    }


def _check_identifiability(ident, n, m):
    """Validate an identifiability report against n varying coordinates and m rows."""
    if not isinstance(ident, dict) or not _is_true(ident.get('ok')):
        return ['identifiability must be an ok=True dict from identifiability_report'], None
    reasons = []
    try:
        S = np.array(ident['scaled_jacobian'], dtype=float)
        V = np.array(ident['right_vectors'], dtype=float)
        s = np.array(ident['singular_values'], dtype=float)
    except Exception as exc:
        return [f'identifiability arrays malformed: {type(exc).__name__}: {exc}'], None
    if S.shape != (m, n):
        reasons.append(f'identifiability.scaled_jacobian must be {m}x{n}')
    if V.shape != (n, n):
        reasons.append(f'identifiability.right_vectors must be {n}x{n}')
    if s.shape != (n,):
        reasons.append(f'identifiability.singular_values must have length {n}')
    if not (np.all(np.isfinite(S)) and np.all(np.isfinite(V)) and np.all(np.isfinite(s))):
        reasons.append('identifiability arrays must be finite')
    identified = ident.get('identified')
    near_null = ident.get('near_null')
    if not isinstance(identified, list) or not isinstance(near_null, list) or \
            not all(_is_int(k) for k in identified + near_null):
        reasons.append('identifiability.identified and .near_null must be lists of int')
    elif sorted(identified + near_null) != list(range(n)) or (set(identified) & set(near_null)):
        reasons.append('identifiability.identified and .near_null must partition range(n)')
    if reasons:
        return reasons, None
    for k in identified:
        if not (s[k] > 0.0):
            reasons.append(f'identified direction {k} has non-positive singular value')
    if reasons:
        return reasons, None
    return [], {'S': S, 'V': V, 's': s, 'identified': [int(k) for k in identified],
                'near_null': [int(k) for k in near_null]}


def _explore_impl(*, forward, spec, region, u_anchor, identifiability, repair_iterations, max_repair_step,
                  march_step, bisection_steps, design_count, rng_seed, budget, log, anchor_entry):
    out = {
        'ok': False, 'status': None, 'stage_reached': None, 'anchor': None, 'first_admitted_log_index': None,
        'admitted_points': [], 'rejected_points': [], 'boundary': {}, 'boundary_detail': {}, 'hull_box': {},
        'unidentified_directions': [], 'identified_directions': [],
        'repair': {'iterations_requested': None, 'iterations_used': 0, 'steps': []},
        'design': {'count_requested': None, 'evaluated': 0, 'skipped_outside_box': 0, 'bases': [],
                   'first_index': None},
        'evaluations_used': 0, 'budget': None, 'empty_region': False, 'n_admitted': 0, 'n_rejected': 0,
        'bounds_semantics': BOUNDS_SEMANTICS, 'reasons': [],
    }
    reasons, info = _common_eval_checks(forward, spec, region, log, budget)
    reasons.extend(_nonneg_int(repair_iterations, 'repair_iterations'))
    reasons.extend(_positive_float(max_repair_step, 'max_repair_step'))
    reasons.extend(_positive_float(march_step, 'march_step'))
    reasons.extend(_nonneg_int(bisection_steps, 'bisection_steps'))
    reasons.extend(_nonneg_int(design_count, 'design_count'))
    reasons.extend(_nonneg_int(rng_seed, 'rng_seed'))
    idn = None
    if info is not None:
        rs, ua = _check_unit_vector(u_anchor, info['n'], 'u_anchor')
        reasons.extend(rs)
        if not _check_region(region):
            rs, idn = _check_identifiability(identifiability, info['n'], len(region['row_ids']))
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
    counter = {'used': 0, 'budget': int(budget)}
    out['budget'] = int(budget)
    out['repair']['iterations_requested'] = int(repair_iterations)
    out['design']['count_requested'] = int(design_count)
    max_repair_step = float(max_repair_step)
    march_step = float(march_step)
    sigma = np.array([region['sigmas'][rid] for rid in row_ids], dtype=float)
    centre = np.array([0.5 * (region['rectangles'][rid][0] + region['rectangles'][rid][1]) for rid in row_ids],
                      dtype=float)
    admitted, rejected = [], []
    state = {'a': None}
    # boundary keyed by identified direction index; a side stays None until it is determined
    boundary = {int(k): {'minus': None, 'plus': None} for k in ident}
    detail = {int(k): {'minus': None, 'plus': None} for k in ident}
    out['boundary'] = boundary
    out['boundary_detail'] = detail

    def need_budget():
        if counter['used'] >= counter['budget']:
            raise _BudgetExhausted()

    def evaluate(u, purpose):
        e = _evaluate_point(forward=forward, spec=spec, region=region, u=u, purpose=purpose, log=log,
                            counter=counter)
        (admitted if e['admitted'] is True else rejected).append(_point_from_entry(e))
        return e

    def direction_summary(k):
        v = V[k]
        return {'index': int(k), 'vector_u': _floats(v), 'singular_value': float(s[k]),
                'trial_projection': float(ua @ v),
                'admitted_anchor_projection': (float(state['a'] @ v) if state['a'] is not None else None),
                'sensitivity': float(np.linalg.norm(S @ v))}

    def finalise(status, ok):
        out['status'] = status
        out['ok'] = bool(ok)
        out['evaluations_used'] = counter['used']
        out['admitted_points'] = admitted
        out['rejected_points'] = rejected
        out['n_admitted'] = len(admitted)
        out['n_rejected'] = len(rejected)
        hull = {}
        a = state['a']
        for k in ident:
            if a is None or not admitted:
                hull[int(k)] = {'min': None, 'max': None}
                continue
            proj = [float((np.array(p['u'], dtype=float) - a) @ V[k]) for p in admitted]
            hull[int(k)] = {'min': min(proj), 'max': max(proj)}
        out['hull_box'] = hull
        out['identified_directions'] = [direction_summary(k) for k in ident]
        out['unidentified_directions'] = [direction_summary(k) for k in near]
        return out

    try:
        # ---- stage 1: anchor ---------------------------------------------------------
        out['stage_reached'] = 'anchor'
        if anchor_entry is None:
            need_budget()
            anchor_entry = evaluate(ua, 'seed')
        else:
            (admitted if anchor_entry['admitted'] is True else rejected).append(_point_from_entry(anchor_entry))
        out['anchor'] = {
            'u': list(anchor_entry['u']), 'theta_natural': anchor_entry['theta_natural'],
            'theta_internal': anchor_entry['theta_internal'], 'admitted': anchor_entry['admitted'],
            'valid': anchor_entry['valid'], 'log_index': anchor_entry['index'],
            'prediction': anchor_entry['prediction'],
        }
        first = anchor_entry if anchor_entry['admitted'] is True else None
        if first is None and not anchor_entry['valid']:
            reasons.append('anchor evaluation invalid; no valid point from which to repair: ' +
                           '; '.join(anchor_entry['reasons']))
            return finalise('ANCHOR_INVALID', False)

        # ---- stage 2: linearised repair ----------------------------------------------
        if first is None:
            out['stage_reached'] = 'repair'
            if not ident:
                reasons.append('anchor not admitted and no identified direction exists; repair impossible')
            else:
                # pseudo-inverse of the scaled Jacobian restricted to identified directions:
                # S = sum_k s_k u_k v_k^T  =>  S^+_I = sum_k v_k u_k^T / s_k  with u_k = S v_k / s_k
                P = np.zeros((n, len(row_ids)), dtype=float)
                for k in ident:
                    vk = V[k]
                    P += np.outer(vk, S @ vk) / (float(s[k]) ** 2)
                cur = anchor_entry
                cap = max_repair_step
                for it in range(int(repair_iterations)):
                    f_cur = _speeds_vector(cur, row_ids)
                    r = (centre - f_cur) / sigma
                    du = P @ r
                    norm = float(np.linalg.norm(du))
                    if norm > cap:
                        du = du * (cap / norm)
                    u_cur = np.array(cur['u'], dtype=float)
                    u_new = np.clip(u_cur + du, 0.0, 1.0)
                    disp = float(np.max(np.abs(u_new - u_cur))) if n else 0.0
                    if norm <= _ZERO_STEP or disp <= _ZERO_STEP:
                        reasons.append(f'repair iteration {it}: linearised step produces no displacement '
                                       f'(norm {norm:.3e}); stopping')
                        break
                    need_budget()
                    e = evaluate(u_new, 'repair')
                    out['repair']['iterations_used'] = it + 1
                    out['repair']['steps'].append({
                        'iteration': it, 'from_log_index': cur['index'], 'log_index': e['index'],
                        'unclipped_step_norm': norm, 'applied_step_norm': float(np.linalg.norm(u_new - u_cur)),
                        'cap': cap, 'valid': e['valid'], 'admitted': e['admitted'],
                    })
                    if e['admitted'] is True:
                        first = e
                        break
                    if e['valid']:
                        cur = e
                        cap = max_repair_step
                    else:
                        cap = 0.5 * cap  # retry from the last valid point with a shorter step
                if first is None:
                    reasons.append(f'no admitted point after {out["repair"]["iterations_used"]} repair evaluation(s)')
            if first is None:
                reasons.append('NO_ADMITTED_POINT: no admitted point found by the anchor/repair procedure '
                               '(DDO154 calibration rows only; not target tuning)')
                out['empty_region'] = True
                return finalise('NO_ADMITTED_POINT', True)

        a = np.array(first['u'], dtype=float)
        state['a'] = a
        out['first_admitted_log_index'] = first['index']

        # ---- stage 3: march + bisection along identified directions --------------------
        for k in ident:
            for side, sgn in (('minus', -1.0), ('plus', 1.0)):
                out['stage_reached'] = 'march'
                d = sgn * V[k]
                t_edge = _edge_t(a, d)
                t_last, t_rej, hit_edge = 0.0, None, False
                n_march, n_bis = 0, 0
                rec = {'last_admitted_t': 0.0, 'first_rejected_t': None, 'box_edge_t': float(t_edge),
                       'hit_box_edge': False, 'march_evaluations': 0, 'bisection_evaluations': 0,
                       'complete': False}
                detail[int(k)][side] = rec
                boundary[int(k)][side] = 0.0
                t = march_step
                while True:
                    if t > t_edge + _T_TOL:
                        # next doubling point leaves the box: verify the box-edge point itself
                        if t_edge > t_last + _T_TOL:
                            need_budget()
                            e = evaluate(a + t_edge * d, 'march')
                            n_march += 1
                            rec['march_evaluations'] = n_march
                            if e['admitted'] is True:
                                t_last, hit_edge = t_edge, True
                            else:
                                t_rej = t_edge
                        else:
                            hit_edge = True
                        break
                    need_budget()
                    e = evaluate(a + t * d, 'march')
                    n_march += 1
                    rec['march_evaluations'] = n_march
                    if e['admitted'] is True:
                        t_last = t
                        boundary[int(k)][side] = t_last
                        rec['last_admitted_t'] = t_last
                        t = 2.0 * t
                    else:
                        t_rej = t
                        break
                rec['first_rejected_t'] = t_rej
                rec['hit_box_edge'] = hit_edge
                boundary[int(k)][side] = t_last
                rec['last_admitted_t'] = t_last
                if t_rej is not None and int(bisection_steps) > 0:
                    out['stage_reached'] = 'bisection'
                    lo, hi = t_last, t_rej
                    for _ in range(int(bisection_steps)):
                        mid = 0.5 * (lo + hi)
                        need_budget()
                        e = evaluate(a + mid * d, 'bisection')
                        n_bis += 1
                        rec['bisection_evaluations'] = n_bis
                        if e['admitted'] is True:
                            lo = mid
                            boundary[int(k)][side] = lo
                            rec['last_admitted_t'] = lo
                        else:
                            hi = mid
                        rec['first_rejected_t'] = hi
                    t_last, t_rej = lo, hi
                boundary[int(k)][side] = float(t_last)
                rec['last_admitted_t'] = float(t_last)
                rec['first_rejected_t'] = (float(t_rej) if t_rej is not None else None)
                rec['complete'] = True

        # ---- stage 4: Halton design inside the boundary box ----------------------------
        out['stage_reached'] = 'design'
        m_id = len(ident)
        bases = _first_primes(m_id)
        first_index = int(rng_seed) + 1
        out['design']['bases'] = bases
        out['design']['first_index'] = first_index
        if m_id == 0:
            if int(design_count) > 0:
                reasons.append('no identified direction: Halton design skipped (every design point would '
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
                need_budget()
                evaluate(p, 'design')
                out['design']['evaluated'] += 1

        # ---- stage 5: summary -----------------------------------------------------------
        out['stage_reached'] = 'summary'
        return finalise('COMPLETE', True)
    except _BudgetExhausted:
        reasons.append(f'BUDGET_EXHAUSTED at stage {out["stage_reached"]!r}: {counter["used"]} of '
                       f'{counter["budget"]} evaluations used; partial results preserved')
        return finalise('BUDGET_EXHAUSTED', False)


def explore_region(*, forward, spec, region, u_anchor, identifiability, repair_iterations, max_repair_step,
                   march_step, bisection_steps, design_count, rng_seed, budget, log):
    """Deterministic exploration of the identified subspace around u_anchor.

    1. classify the anchor (evaluated here with purpose 'seed');
    2. if not admitted, damped Gauss-Newton repair with the fixed scaled seed Jacobian restricted to
       the identified directions, toward the rectangle centres in sigma units;
    3. from the first admitted point, doubling march +/- along each identified direction then bisection;
    4. Halton design (bases 2,3,5,...; first index rng_seed+1) inside the boundary box;
    5. hull box over admitted points and the unidentified directions with their sensitivities.
    Budget exhaustion returns status 'BUDGET_EXHAUSTED' with everything evaluated so far.
    """
    return _explore_impl(forward=forward, spec=spec, region=region, u_anchor=u_anchor,
                         identifiability=identifiability, repair_iterations=repair_iterations,
                         max_repair_step=max_repair_step, march_step=march_step,
                         bisection_steps=bisection_steps, design_count=design_count, rng_seed=rng_seed,
                         budget=budget, log=log, anchor_entry=None)


# --------------------------------------------------------------------------
# orchestration
# --------------------------------------------------------------------------

def run_calibration_region(*, forward, coordinates, observation_region_path, observation_region_sha256,
                           u_seed, budget, rel_step, min_step, max_halvings, null_tolerance,
                           repair_iterations, max_repair_step, march_step, bisection_steps, design_count,
                           rng_seed):
    """Orchestrate load -> spec -> Jacobian -> identifiability -> exploration under one budget.

    u_seed: list over varying coordinates (an entry None, or u_seed None, means the trial value).
    budget: maximum number of forward evaluations in total. The seed evaluation made for the
    Jacobian is reused as the exploration anchor (no second forward call at the same point).
    """
    out = {
        'ok': False, 'status': None, 'stage_reached': None, 'region': None, 'spec': None, 'jacobian': None,
        'identifiability': None, 'exploration': None, 'evaluation_log': [], 'evaluations_used': 0,
        'budget': None, 'u_seed_used': None, 'parameters': None,
        'ngc3198_access': NGC3198_ACCESS, 'bounds_semantics': BOUNDS_SEMANTICS, 'module': MODULE_NAME,
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
    reasons.extend(_nonneg_int(rng_seed, 'rng_seed'))
    if reasons:
        out['status'] = 'INPUT_INVALID'
        return out
    out['budget'] = int(budget)
    out['parameters'] = {
        'budget': int(budget), 'rel_step': float(rel_step), 'min_step': float(min_step),
        'max_halvings': int(max_halvings), 'null_tolerance': tol, 'repair_iterations': int(repair_iterations),
        'max_repair_step': float(max_repair_step), 'march_step': float(march_step),
        'bisection_steps': int(bisection_steps), 'design_count': int(design_count), 'rng_seed': int(rng_seed),
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
        reasons.append('seed evaluation invalid; no Jacobian')
        reasons.extend(jac['reasons'])
        return finish('SEED_INVALID', False)
    if not jac['ok']:
        reasons.append('Jacobian stage failed')
        reasons.extend(jac['reasons'])
        return finish('JACOBIAN_FAILED', False)

    out['stage_reached'] = 'identifiability'
    idn = identifiability_report(jacobian_u=jac['jacobian_u'], sigmas=region['sigmas'], row_ids=region['row_ids'],
                                 varying_names=spec['varying_names'], null_tolerance=null_tolerance)
    out['identifiability'] = idn
    if not idn['ok']:
        reasons.append('identifiability report failed (incomplete Jacobian or bad input); exploration not run')
        reasons.extend(idn['reasons'])
        return finish('JACOBIAN_INCOMPLETE', False)

    out['stage_reached'] = 'exploration'
    seed_entry = log[jac['seed_log_index']]
    remaining = int(budget) - len(log)
    exp = _explore_impl(forward=forward, spec=spec, region=region, u_anchor=_floats(u0), identifiability=idn,
                        repair_iterations=repair_iterations, max_repair_step=max_repair_step,
                        march_step=march_step, bisection_steps=bisection_steps, design_count=design_count,
                        rng_seed=rng_seed, budget=remaining, log=log, anchor_entry=seed_entry)
    out['exploration'] = exp
    if exp['status'] is None:
        reasons.append('exploration rejected its inputs')
        reasons.extend(exp['reasons'])
        return finish('EXPLORATION_FAILED', False)
    out['stage_reached'] = f'exploration:{exp["stage_reached"]}'
    if exp['status'] != 'COMPLETE':
        reasons.extend(exp['reasons'])
    return finish(exp['status'], exp['ok'])
