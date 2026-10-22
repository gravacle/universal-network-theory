"""prediction_freeze_c3v001 -- Module 2 of INTERFACE_0462_V001 (Claude3 lane, dispatch 0462).

NGC3198 43-query prediction freeze packager and post-freeze scorer.

Public API (keyword-only arguments, no defaults; every function returns a dict
with at least ``ok: bool`` and ``reasons: list[str]``):

    load_query_manifest(*, path, expected_sha256)
    select_representative_points(*, exploration, interior_count)
    evaluate_envelopes(*, forward_ngc, points, query_ids, budget)
    write_freeze_manifest(*, out_path, parameter_region, alternatives, observation_rule,
                          envelopes, query_ids, code_files, input_files, notes)
    verify_freeze_manifest(*, freeze_manifest_path)
    score_after_freeze(*, freeze_manifest_path, target_rows)

Invariants:
  * inert at import: no file I/O, no computation, no environment changes;
  * standard library only; no numpy objects are created or returned;
  * never reads any NGC3198 velocity. The only NGC3198 file it opens is the
    target-free query manifest (ids and radii). Target rows reach this module
    only through ``score_after_freeze``, which writes nothing to disk;
  * fails closed: anticipated bad input returns ok=False instead of raising;
    exceptions raised by the root-supplied ``forward_ngc`` are caught and
    logged as invalid evaluations;
  * canonical JSON is json.dumps(obj, sort_keys=True, separators=(',', ':'),
    allow_nan=False); every file hash is SHA256 over raw bytes;
  * the freeze manifest is written with exclusive create (never overwrites),
    carries ``target_velocities_included: False`` unconditionally, and refuses
    any forbidden target field name (lowercase compare, any depth).
"""

import datetime
import hashlib
import json
import math
import numbers
import os

SCHEMA = 'FREEZE_MANIFEST_C3V001'
UNITS = 'km/s'
SEMANTICS = 'TOTAL_OBSERVABLE'
ERROR_MODEL = 'CONDITIONAL_QUOTED_SIGMA_DIAGONAL_ONLY'
WITHIN_ERROR_RULE = ('valid and |velocity - observed| <= quoted sigma (central value); '
                     'band overlap is reported separately and is not the headline')
N_QUERIES = 43

# P46 harness FORBIDDEN set (lanes/P46_CODEX2/line_a_prediction_harness_v002.py)
# plus the four target-row names required by INTERFACE_0462_V001.
FORBIDDEN = frozenset({
    'vobs', 'vobs_km_s', 'observed_velocity', 'observed_km_s',
    'error_v_km_s', 'velocity_error', 'chi2', 'residual_km_s',
    'vgas', 'vdisk', 'vbul', 'vgas_km_s', 'vdisk_km_s', 'vbulge_km_s',
    'target_rows', 'targets', 'target_velocity', 'target_velocities',
})

MANIFEST_KEYS = frozenset({
    'schema', 'created_utc', 'parameter_region', 'alternatives', 'observation_rule',
    'query_ids', 'units', 'semantics', 'predictions', 'pins', 'notes',
    'target_velocities_included', 'within_error_rule', 'manifest_sha256',
})
PREDICTION_KEYS = frozenset({'id', 'velocity', 'band_low', 'band_high', 'n_points', 'n_valid', 'valid'})
ENVELOPE_KEYS = frozenset({'min', 'max', 'central', 'n_points', 'n_valid', 'valid'})
PIN_KEYS = frozenset({'path', 'sha256'})
TARGET_ROW_KEYS = frozenset({'id', 'velocity', 'sigma'})
QUERY_MANIFEST_FIELDS = ('query_id', 'data_row_index', 'Rad_text', 'Rad_unit')

ROLE_ANCHOR = 'anchor'
ROLE_HULL = 'hull_vertex'
ROLE_INTERIOR = 'interior'

STATUS_COMPLETE = 'COMPLETE'
STATUS_BUDGET = 'BUDGET_EXHAUSTED'

_HULL_BOX_TOL = 1e-6


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
    return all(c in '0123456789abcdefABCDEF' for c in s)


def _sha256_hex(raw):
    return hashlib.sha256(raw).hexdigest()


def _canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def _read_bytes(path):
    """Return (bytes, None) or (None, reason). Never raises."""
    if not isinstance(path, str) or not path:
        return None, 'path must be a non-empty string'
    try:
        with open(path, 'rb') as fh:
            return fh.read(), None
    except (OSError, ValueError) as exc:
        return None, 'unreadable file %r: %s: %s' % (path, type(exc).__name__, exc)


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


def _scan_forbidden(obj, where, hits):
    """Collect 'where' paths of dict keys whose lowercase form is forbidden (any depth)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            ks = str(k)
            child = where + '.' + ks
            if ks.lower() in FORBIDDEN:
                hits.append(child)
            _scan_forbidden(v, child, hits)
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            _scan_forbidden(v, '%s[%d]' % (where, i), hits)


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


# --------------------------------------------------------------------------
# load_query_manifest
# --------------------------------------------------------------------------

def load_query_manifest(*, path, expected_sha256):
    """Bind the target-free NGC3198 query manifest: ids and radii only.

    Verifies the byte hash before parsing. Binds only rows[].query_id,
    data_row_index, Rad_text, Rad_unit. Requires 43 unique ids and
    data_row_index exactly 1..43. Nothing else in the file is read into the
    returned dict.
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
    raw, err = _read_bytes(path)
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
        qid = row['query_id']
        idx = row['data_row_index']
        rad_text = row['Rad_text']
        rad_unit = row['Rad_unit']
        if not isinstance(qid, str) or not qid:
            reasons.append('rows[%d].query_id is not a non-empty string' % i)
        if not _is_int(idx):
            reasons.append('rows[%d].data_row_index is not an integer' % i)
        if not isinstance(rad_text, str) or not rad_text:
            reasons.append('rows[%d].Rad_text is not a non-empty string' % i)
        else:
            try:
                rv = float(rad_text)
                if not math.isfinite(rv):
                    reasons.append('rows[%d].Rad_text is not finite' % i)
            except ValueError:
                reasons.append('rows[%d].Rad_text does not parse as a number' % i)
        if not isinstance(rad_unit, str) or not rad_unit:
            reasons.append('rows[%d].Rad_unit is not a non-empty string' % i)
        bound.append((idx, qid, rad_text, rad_unit))
    if reasons:
        return out
    idx_set = set(int(b[0]) for b in bound)
    if idx_set != set(range(1, N_QUERIES + 1)):
        reasons.append('data_row_index values are not exactly 1..%d' % N_QUERIES)
    if len(set(b[1] for b in bound)) != N_QUERIES:
        reasons.append('query_id values are not unique')
    units = set(b[3] for b in bound)
    if len(units) != 1:
        reasons.append('Rad_unit is not uniform across rows: %s' % sorted(units))
    if reasons:
        return out
    bound.sort(key=lambda b: int(b[0]))
    out['query_ids'] = [b[1] for b in bound]
    out['radii_text'] = {b[1]: b[2] for b in bound}
    out['rad_unit'] = units.pop()
    out['ok'] = True
    return out


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
    """Locate the explore_region dict and the identified direction vectors.

    Accepted layouts (first match wins):
      A. run_calibration_region output: {'exploration': {...}, 'identifiability': {...}}
      B. explore_region output with an added 'identifiability' dict
         ({'right_vectors': [...], 'identified': [...]})
      C. explore_region output with top-level 'right_vectors' (and optional 'identified')
    """
    if not isinstance(exploration, dict):
        reasons.append('exploration must be a dict')
        return None, None, None
    ex = exploration
    if 'admitted_points' not in ex and isinstance(ex.get('exploration'), dict):
        ex = ex['exploration']
    ident = None
    for container in (exploration, ex):
        if isinstance(container.get('identifiability'), dict):
            ident = container['identifiability']
            break
    if ident is not None:
        right_vectors = ident.get('right_vectors')
        identified = ident.get('identified')
    else:
        right_vectors = ex.get('right_vectors')
        identified = ex.get('identified')
    if right_vectors is None:
        reasons.append('direction vectors not found: supply identifiability.right_vectors '
                       '(rows = directions in u-space)')
        return None, None, None
    return ex, right_vectors, identified


def select_representative_points(*, exploration, interior_count):
    """Choose the representative admitted points for envelope propagation.

    Order: all hull vertices (per identified direction the admitted points
    attaining the min and the max projection u.v_k; ties -> lowest log_index),
    then the anchor (only if admitted), then a deterministic interior subset of
    the remaining admitted points sorted by log_index (interior_count
    end-inclusive evenly spaced indices; all if fewer). Duplicates by
    log_index are removed, first occurrence wins.
    """
    reasons = []
    out = {'ok': False, 'points': [], 'hull_vertex_count': 0, 'interior_count_used': 0,
           'anchor_included': False, 'n_admitted': 0, 'identified_directions': [],
           'hull_directions': [], 'hull_box_consistent': None, 'reasons': reasons}
    if not _is_int(interior_count) or interior_count < 0:
        reasons.append('interior_count must be a non-negative integer')
        return out
    interior_count = int(interior_count)
    ex, right_vectors, identified = _resolve_exploration(exploration, reasons)
    if ex is None:
        return out
    if ex.get('empty_region') is True:
        reasons.append('exploration reports empty_region=True; no admitted points')
    admitted_raw = ex.get('admitted_points')
    if not isinstance(admitted_raw, (list, tuple)) or len(admitted_raw) == 0:
        reasons.append('exploration.admitted_points must be a non-empty list')
        return out
    admitted = []
    n = None
    seen_log = set()
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
        if n is None:
            n = len(u)
        elif len(u) != n:
            reasons.append('%s.u has length %d, expected %d' % (where, len(u), n))
            continue
        li = int(li)
        if li in seen_log:
            reasons.append('%s duplicates log_index %d' % (where, li))
            continue
        seen_log.add(li)
        admitted.append({'u': u, 'theta_natural': theta, 'log_index': li})
    if reasons:
        return out
    out['n_admitted'] = len(admitted)

    # Direction vectors.
    if not isinstance(right_vectors, (list, tuple)) or len(right_vectors) == 0:
        reasons.append('right_vectors must be a non-empty list of direction vectors')
        return out
    vectors = []
    for k, vec in enumerate(right_vectors):
        v = _bind_u(vec, 'right_vectors[%d]' % k, reasons)
        if v is None:
            continue
        if len(v) != n:
            reasons.append('right_vectors[%d] has length %d, expected %d' % (k, len(v), n))
            continue
        vectors.append(v)
    if reasons:
        return out

    hull_box = ex.get('hull_box')
    hull_keys = None
    if hull_box is not None:
        if not isinstance(hull_box, dict):
            reasons.append('hull_box must be a dict keyed by direction index')
            return out
        hull_keys = {}
        for k, box in hull_box.items():
            try:
                kk = int(k) if not isinstance(k, bool) else None
            except (TypeError, ValueError):
                kk = None
            if kk is None or (isinstance(k, str) and str(kk) != k.strip()):
                reasons.append('hull_box key %r is not a direction index' % (k,))
                continue
            if not isinstance(box, dict) or not _is_real(box.get('min')) or not _is_real(box.get('max')):
                reasons.append('hull_box[%r] must carry finite min and max' % (k,))
                continue
            hull_keys[kk] = (float(box['min']), float(box['max']))
        if reasons:
            return out
    if identified is None:
        if hull_keys is None:
            reasons.append('neither identifiability.identified nor hull_box present; '
                           'cannot determine identified directions')
            return out
        ident_list = sorted(hull_keys)
    else:
        if not isinstance(identified, (list, tuple)):
            reasons.append('identified must be a list of direction indices')
            return out
        ident_list = []
        for k in identified:
            if not _is_int(k):
                reasons.append('identified contains a non-integer %r' % (k,))
                continue
            ident_list.append(int(k))
        if reasons:
            return out
        ident_list = sorted(set(ident_list))
        if hull_keys is not None and set(hull_keys) != set(ident_list):
            reasons.append('hull_box keys %s do not match identified directions %s'
                           % (sorted(hull_keys), ident_list))
            return out
    if not ident_list:
        reasons.append('no identified directions')
        return out
    for k in ident_list:
        if k < 0 or k >= len(vectors):
            reasons.append('identified direction %d out of range for %d right_vectors' % (k, len(vectors)))
    if reasons:
        return out
    out['identified_directions'] = list(ident_list)

    # Hull vertices.
    selected = []
    selected_log = set()

    def _take(pt, role):
        if pt['log_index'] in selected_log:
            return False
        selected_log.add(pt['log_index'])
        selected.append({'u': list(pt['u']), 'theta_natural': dict(pt['theta_natural']),
                         'role': role, 'log_index': pt['log_index']})
        return True

    consistent = True if hull_keys is not None else None
    for k in ident_list:
        v = vectors[k]
        proj = [(_dot(pt['u'], v), pt['log_index'], i) for i, pt in enumerate(admitted)]
        pmin = min(proj, key=lambda t: (t[0], t[1]))
        pmax = min(proj, key=lambda t: (-t[0], t[1]))
        out['hull_directions'].append({
            'direction_index': k,
            'min_log_index': pmin[1], 'max_log_index': pmax[1],
            'projection_range': float(pmax[0] - pmin[0]),
        })
        if hull_keys is not None:
            lo, hi = hull_keys[k]
            rng_box = hi - lo
            rng_here = pmax[0] - pmin[0]
            if abs(rng_box - rng_here) > _HULL_BOX_TOL * (1.0 + abs(rng_box)):
                consistent = False
                reasons.append('WARNING hull_box[%d] range %r differs from recomputed range %r'
                               % (k, rng_box, rng_here))
        _take(admitted[pmin[2]], ROLE_HULL)
        _take(admitted[pmax[2]], ROLE_HULL)
    out['hull_box_consistent'] = consistent
    out['hull_vertex_count'] = len(selected)

    # Anchor.
    anchor = ex.get('anchor')
    if anchor is None:
        reasons.append('anchor absent from exploration; not included')
    elif not isinstance(anchor, dict):
        reasons.append('anchor is not a dict')
        return out
    elif anchor.get('admitted') is not True:
        reasons.append('anchor not admitted; not included (envelopes cover admitted points only)')
    else:
        a_li = anchor.get('log_index')
        match = None
        if _is_int(a_li):
            for pt in admitted:
                if pt['log_index'] == int(a_li):
                    match = pt
                    break
            if match is None:
                reasons.append('anchor.log_index %d not among admitted_points' % int(a_li))
                return out
        else:
            a_u = _bind_u(anchor.get('u'), 'anchor', reasons)
            if a_u is None:
                return out
            for pt in admitted:
                if pt['u'] == a_u:
                    match = pt
                    break
            if match is None:
                reasons.append('anchor is marked admitted but its u is not among admitted_points')
                return out
        out['anchor_included'] = True
        _take(match, ROLE_ANCHOR)

    # Interior subset.
    remaining = sorted((pt for pt in admitted if pt['log_index'] not in selected_log),
                       key=lambda pt: pt['log_index'])
    for j in _evenly_spaced_indices(len(remaining), interior_count):
        _take(remaining[j], ROLE_INTERIOR)
    out['interior_count_used'] = sum(1 for p in selected if p['role'] == ROLE_INTERIOR)
    out['points'] = selected
    out['ok'] = True
    return out


# --------------------------------------------------------------------------
# evaluate_envelopes
# --------------------------------------------------------------------------

def _bind_forward_result(result, exc, query_ids, preasons):
    """Return (speeds_plain|None, point_valid, per_query_ok dict)."""
    per_query_ok = {q: False for q in query_ids}
    if exc is not None:
        preasons.append('exception raised by forward_ngc: ' + exc)
        return None, False, per_query_ok
    if not isinstance(result, dict):
        preasons.append('forward_ngc returned %s, not a dict' % type(result).__name__)
        return None, False, per_query_ok
    flag = result.get('valid')
    flag_ok = flag is True
    if not flag_ok:
        preasons.append('forward_ngc valid flag is not True (got %r)' % (flag,))
    rr = result.get('reasons')
    if isinstance(rr, (list, tuple)):
        for r in rr:
            preasons.append('forward_ngc reason: %s' % (r,))
    speeds = result.get('speeds_km_s')
    if not isinstance(speeds, dict):
        preasons.append('speeds_km_s is not a dict')
        return None, False, per_query_ok
    plain = {}
    n_bad = 0
    for q in query_ids:
        if q not in speeds:
            preasons.append('missing id %s' % q)
            plain[q] = None
            n_bad += 1
            continue
        v = speeds[q]
        if _is_real(v):
            plain[q] = float(v)
            per_query_ok[q] = flag_ok
        else:
            preasons.append('non-finite or non-real value for %s: %r' % (q, v))
            plain[q] = None
            n_bad += 1
    extra = [k for k in speeds if k not in per_query_ok]
    if extra:
        preasons.append('%d extra ids ignored' % len(extra))
    point_valid = flag_ok and n_bad == 0
    return plain, point_valid, per_query_ok


def evaluate_envelopes(*, forward_ngc, points, query_ids, budget):
    """Evaluate forward_ngc at every representative point and build per-query envelopes.

    A point is valid iff the callable returned a dict with valid is True, every
    query id present, every value a finite real. A point contributes a value
    for query q iff its valid flag is True and its value for q is a finite
    real. A query is valid iff at least one point was evaluated and every
    evaluated point contributed a finite value for it. central = median over
    contributing points. Each call consumes one unit of budget; exhaustion
    stops evaluation with status='BUDGET_EXHAUSTED' and partial results kept.
    """
    reasons = []
    out = {'ok': False, 'status': None, 'per_point': [], 'envelopes': {}, 'evaluations_used': 0,
           'evaluation_log': [], 'points_total': 0, 'points_evaluated': 0, 'reasons': reasons}
    if not callable(forward_ngc):
        reasons.append('forward_ngc must be callable')
    ids = _check_query_ids(query_ids, reasons, False)
    if not _is_int(budget) or budget < 0:
        reasons.append('budget must be a non-negative integer')
    if not isinstance(points, (list, tuple)) or len(points) == 0:
        reasons.append('points must be a non-empty list')
    if reasons:
        return out
    budget = int(budget)
    bound = []
    for i, pt in enumerate(points):
        where = 'points[%d]' % i
        if not isinstance(pt, dict):
            reasons.append('%s is not a dict' % where)
            continue
        theta = _bind_theta(pt.get('theta_natural'), where, reasons)
        if theta is None:
            continue
        u = pt.get('u')
        u_plain = None
        if u is not None:
            u_plain = _bind_u(u, where, reasons)
            if u_plain is None:
                continue
        role = pt.get('role')
        li = pt.get('log_index')
        bound.append({'theta_natural': theta, 'u': u_plain,
                      'role': role if isinstance(role, str) else None,
                      'log_index': int(li) if _is_int(li) else None})
    if reasons:
        return out
    out['points_total'] = len(bound)

    used = 0
    status = STATUS_COMPLETE
    contributions = {q: [] for q in ids}
    for pi, pt in enumerate(bound):
        if used >= budget:
            status = STATUS_BUDGET
            reasons.append('budget %d exhausted before point %d of %d' % (budget, pi, len(bound)))
            break
        theta = dict(pt['theta_natural'])
        exc = None
        result = None
        preasons = []
        try:
            result = forward_ngc(theta)
        except Exception as e:  # root-supplied callable: catch, log, treat as invalid
            exc = '%s: %s' % (type(e).__name__, e)
        used += 1
        speeds, point_valid, per_query_ok = _bind_forward_result(result, exc, ids, preasons)
        for q in ids:
            if per_query_ok[q]:
                contributions[q].append(speeds[q])
        out['per_point'].append({'point_index': pi, 'valid': point_valid, 'speeds_km_s': speeds,
                                 'reasons': list(preasons), 'exception': exc})
        out['evaluation_log'].append({
            'index': used - 1, 'purpose': 'ngc3198_envelope', 'point_index': pi,
            'role': pt['role'], 'log_index': pt['log_index'], 'u': pt['u'],
            'theta_natural': dict(pt['theta_natural']), 'prediction': speeds,
            'valid': point_valid, 'reasons': list(preasons), 'exception': exc,
        })
    out['evaluations_used'] = used
    out['points_evaluated'] = used
    envelopes = {}
    for q in ids:
        vals = contributions[q]
        n_valid = len(vals)
        valid = used >= 1 and n_valid == used
        envelopes[q] = {
            'min': float(min(vals)) if n_valid else None,
            'max': float(max(vals)) if n_valid else None,
            'central': _median(vals) if n_valid else None,
            'n_points': used, 'n_valid': n_valid, 'valid': bool(valid),
        }
    out['envelopes'] = envelopes
    out['status'] = status
    out['ok'] = True
    return out


# --------------------------------------------------------------------------
# write_freeze_manifest
# --------------------------------------------------------------------------

def _pin_files(paths, label, reasons):
    if not isinstance(paths, (list, tuple)):
        reasons.append('%s must be a list of paths' % label)
        return []
    pins = []
    for i, p in enumerate(paths):
        if not isinstance(p, str) or not p:
            reasons.append('%s[%d] is not a non-empty string' % (label, i))
            continue
        raw, err = _read_bytes(p)
        if raw is None:
            reasons.append('%s[%d]: %s' % (label, i, err))
            continue
        pins.append({'path': os.path.abspath(p), 'sha256': _sha256_hex(raw)})
    return pins


def _bind_envelope(q, env, reasons):
    where = 'envelopes[%r]' % q
    if not isinstance(env, dict):
        reasons.append('%s is not a dict' % where)
        return None
    missing = ENVELOPE_KEYS - set(env)
    if missing:
        reasons.append('%s missing keys %s' % (where, sorted(missing)))
        return None
    valid = env['valid']
    if not isinstance(valid, bool):
        reasons.append('%s.valid is not a bool' % where)
        return None
    n_points, n_valid = env['n_points'], env['n_valid']
    if not _is_int(n_points) or not _is_int(n_valid) or n_points < 0 or n_valid < 0 or n_valid > n_points:
        reasons.append('%s n_points/n_valid must be non-negative ints with n_valid <= n_points' % where)
        return None
    vals = {}
    for key in ('min', 'max', 'central'):
        v = env[key]
        if v is None:
            vals[key] = None
        elif _is_real(v):
            vals[key] = float(v)
        else:
            reasons.append('%s.%s is not a finite real or None' % (where, key))
            return None
    if valid:
        if n_valid != n_points or n_points < 1:
            reasons.append('%s valid=True requires n_valid == n_points >= 1' % where)
            return None
        if any(vals[k] is None for k in ('min', 'max', 'central')):
            reasons.append('%s valid=True requires finite min/max/central' % where)
            return None
    if all(vals[k] is not None for k in ('min', 'max', 'central')):
        if not (vals['min'] <= vals['central'] <= vals['max']):
            reasons.append('%s requires min <= central <= max' % where)
            return None
    elif any(vals[k] is not None for k in ('min', 'max', 'central')):
        reasons.append('%s min/max/central must be all None or all finite' % where)
        return None
    return {'id': q, 'velocity': vals['central'], 'band_low': vals['min'], 'band_high': vals['max'],
            'n_points': int(n_points), 'n_valid': int(n_valid), 'valid': valid}


def write_freeze_manifest(*, out_path, parameter_region, alternatives, observation_rule,
                          envelopes, query_ids, code_files, input_files, notes):
    """Write the hash-pinned freeze manifest as canonical JSON bytes (exclusive create).

    Refuses if out_path exists, if any forbidden key appears at any depth in
    any supplied value, if envelopes does not cover exactly query_ids (43), or
    if any listed file is unreadable. 'target_velocities_included': False is
    always written; no target velocity ever enters this function.
    """
    reasons = []
    out = {'ok': False, 'path': None, 'manifest_sha256': None, 'bytes_written': 0, 'reasons': reasons}
    if not isinstance(out_path, str) or not out_path:
        reasons.append('out_path must be a non-empty string')
        return out
    out['path'] = os.path.abspath(out_path)
    if os.path.lexists(out_path):
        reasons.append('REFUSED: out_path already exists (no overwrite): %s' % out['path'])
        return out
    parent = os.path.dirname(out['path'])
    if not os.path.isdir(parent):
        reasons.append('parent directory does not exist: %s' % parent)
        return out
    if not isinstance(parameter_region, dict):
        reasons.append('parameter_region must be a dict')
    if not isinstance(alternatives, (dict, list, tuple, str)):
        reasons.append('alternatives must be a dict, list or string')
    if not isinstance(observation_rule, (dict, list, tuple, str)):
        reasons.append('observation_rule must be a dict, list or string')
    if not isinstance(envelopes, dict):
        reasons.append('envelopes must be a dict keyed by query_id')
    ids = _check_query_ids(query_ids, reasons, True)
    if reasons:
        return out

    # Forbidden key scan over every supplied value (any depth, lowercase compare).
    hits = []
    for label, value in (('parameter_region', parameter_region), ('alternatives', alternatives),
                         ('observation_rule', observation_rule), ('envelopes', envelopes),
                         ('notes', notes)):
        _scan_forbidden(value, label, hits)
    if hits:
        reasons.append('REFUSED: forbidden target field name(s) present: %s' % hits)
        return out

    # Envelope coverage: exactly query_ids.
    env_keys = set(envelopes)
    id_set = set(ids)
    if env_keys != id_set:
        reasons.append('REFUSED: envelopes do not cover exactly query_ids (missing %s, extra %s)'
                       % (sorted(id_set - env_keys), sorted(str(k) for k in env_keys - id_set)))
        return out
    predictions = []
    for q in ids:
        row = _bind_envelope(q, envelopes[q], reasons)
        if row is not None:
            predictions.append(row)
    if reasons:
        return out

    # Pins from bytes, absolute paths.
    code_pins = _pin_files(code_files, 'code_files', reasons)
    input_pins = _pin_files(input_files, 'input_files', reasons)
    if reasons:
        return out

    try:
        manifest = {
            'schema': SCHEMA,
            'created_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'parameter_region': _plain(parameter_region, 'parameter_region'),
            'alternatives': _plain(alternatives, 'alternatives'),
            'observation_rule': _plain(observation_rule, 'observation_rule'),
            'query_ids': list(ids),
            'units': UNITS,
            'semantics': SEMANTICS,
            'predictions': predictions,
            'pins': {'code_files': code_pins, 'input_files': input_pins},
            'notes': _plain(notes, 'notes'),
            'target_velocities_included': False,
            'within_error_rule': WITHIN_ERROR_RULE,
        }
        hits = []
        _scan_forbidden(manifest, 'manifest', hits)
        if hits:
            reasons.append('REFUSED: forbidden target field name(s) present: %s' % hits)
            return out
        body = _canonical_bytes(manifest)
    except (ValueError, TypeError) as exc:
        reasons.append('manifest not canonically serialisable: %s: %s' % (type(exc).__name__, exc))
        return out
    digest = _sha256_hex(body)
    manifest['manifest_sha256'] = digest
    try:
        payload = _canonical_bytes(manifest)
    except (ValueError, TypeError) as exc:
        reasons.append('manifest not canonically serialisable: %s' % exc)
        return out
    try:
        with open(out_path, 'xb') as fh:
            fh.write(payload)
    except (OSError, ValueError) as exc:
        reasons.append('REFUSED: could not create out_path: %s: %s' % (type(exc).__name__, exc))
        return out
    out['manifest_sha256'] = digest
    out['bytes_written'] = len(payload)
    # Read-back check of the bytes just written.
    raw, err = _read_bytes(out_path)
    if raw is None or raw != payload:
        reasons.append('read-back mismatch after write: %s' % (err or 'bytes differ'))
        return out
    out['ok'] = True
    return out


# --------------------------------------------------------------------------
# verify_freeze_manifest / score_after_freeze
# --------------------------------------------------------------------------

def _validate_manifest_structure(doc, reasons):
    if not isinstance(doc, dict):
        reasons.append('manifest is not a JSON object')
        return
    keys = set(doc)
    missing = MANIFEST_KEYS - keys
    extra = keys - MANIFEST_KEYS
    if missing:
        reasons.append('manifest missing keys %s' % sorted(missing))
    if extra:
        reasons.append('manifest has unexpected keys %s' % sorted(extra))
    if missing:
        return
    if doc['schema'] != SCHEMA:
        reasons.append('schema is %r, expected %r' % (doc['schema'], SCHEMA))
    if doc['units'] != UNITS:
        reasons.append('units is %r, expected %r' % (doc['units'], UNITS))
    if doc['semantics'] != SEMANTICS:
        reasons.append('semantics is %r, expected %r' % (doc['semantics'], SEMANTICS))
    if doc['target_velocities_included'] is not False:
        reasons.append('target_velocities_included is not False')
    if doc['within_error_rule'] != WITHIN_ERROR_RULE:
        reasons.append('within_error_rule text differs from the frozen rule')
    if not isinstance(doc['created_utc'], str) or not doc['created_utc']:
        reasons.append('created_utc is not a string')
    if not isinstance(doc['parameter_region'], dict):
        reasons.append('parameter_region is not an object')
    if not isinstance(doc['alternatives'], (dict, list, str)):
        reasons.append('alternatives is not an object, list or string')
    if not isinstance(doc['observation_rule'], (dict, list, str)):
        reasons.append('observation_rule is not an object, list or string')
    if not _is_hex64(doc['manifest_sha256']):
        reasons.append('manifest_sha256 is not a 64-character hex string')
    ids = _check_query_ids(doc['query_ids'], reasons, True)
    preds = doc['predictions']
    if not isinstance(preds, list) or len(preds) != N_QUERIES:
        reasons.append('predictions must be a list of %d rows' % N_QUERIES)
    elif ids is not None and len(ids) == N_QUERIES:
        for i, row in enumerate(preds):
            where = 'predictions[%d]' % i
            if not isinstance(row, dict):
                reasons.append('%s is not an object' % where)
                continue
            if set(row) != PREDICTION_KEYS:
                reasons.append('%s keys %s differ from %s' % (where, sorted(row), sorted(PREDICTION_KEYS)))
                continue
            if row['id'] != ids[i]:
                reasons.append('%s id %r does not match query_ids[%d] %r' % (where, row['id'], i, ids[i]))
            valid = row['valid']
            if not isinstance(valid, bool):
                reasons.append('%s.valid is not a bool' % where)
                continue
            n_points, n_valid = row['n_points'], row['n_valid']
            if (not _is_int(n_points) or not _is_int(n_valid) or n_points < 0 or n_valid < 0
                    or n_valid > n_points):
                reasons.append('%s n_points/n_valid malformed' % where)
                continue
            vals = {}
            bad = False
            for key in ('velocity', 'band_low', 'band_high'):
                v = row[key]
                if v is None:
                    vals[key] = None
                elif _is_real(v):
                    vals[key] = float(v)
                else:
                    reasons.append('%s.%s is not a finite real or None' % (where, key))
                    bad = True
            if bad:
                continue
            none_count = sum(1 for k in vals if vals[k] is None)
            if none_count not in (0, 3):
                reasons.append('%s velocity/band_low/band_high must be all None or all finite' % where)
                continue
            if none_count == 0 and not (vals['band_low'] <= vals['velocity'] <= vals['band_high']):
                reasons.append('%s requires band_low <= velocity <= band_high' % where)
            if valid and (none_count != 0 or n_valid != n_points or n_points < 1):
                reasons.append('%s valid=True requires finite values and n_valid == n_points >= 1' % where)
    pins = doc['pins']
    if not isinstance(pins, dict) or set(pins) != {'code_files', 'input_files'}:
        reasons.append('pins must be an object with exactly code_files and input_files')
    else:
        for label in ('code_files', 'input_files'):
            lst = pins[label]
            if not isinstance(lst, list):
                reasons.append('pins.%s is not a list' % label)
                continue
            for i, pin in enumerate(lst):
                if not isinstance(pin, dict) or set(pin) != PIN_KEYS:
                    reasons.append('pins.%s[%d] must have exactly path and sha256' % (label, i))
                    continue
                if not isinstance(pin['path'], str) or not pin['path']:
                    reasons.append('pins.%s[%d].path is not a non-empty string' % (label, i))
                if not _is_hex64(pin['sha256']):
                    reasons.append('pins.%s[%d].sha256 is not a 64-character hex string' % (label, i))
    hits = []
    _scan_forbidden(doc, 'manifest', hits)
    if hits:
        reasons.append('forbidden target field name(s) present: %s' % hits)


def _verify_impl(freeze_manifest_path):
    reasons = []
    out = {'ok': False, 'path': None, 'manifest_sha256_recomputed': None,
           'manifest_sha256_recorded': None, 'canonical_bytes_match': None,
           'pins_verified': [], 'reasons': reasons}
    if not isinstance(freeze_manifest_path, str) or not freeze_manifest_path:
        reasons.append('freeze_manifest_path must be a non-empty string')
        return out, None
    out['path'] = os.path.abspath(freeze_manifest_path)
    raw, err = _read_bytes(freeze_manifest_path)
    if raw is None:
        reasons.append(err)
        return out, None
    doc, err = _parse_json_bytes(raw)
    if doc is None:
        reasons.append(err)
        return out, None
    if not isinstance(doc, dict):
        reasons.append('manifest is not a JSON object')
        return out, None
    recorded = doc.get('manifest_sha256')
    out['manifest_sha256_recorded'] = recorded if isinstance(recorded, str) else None
    # Self-hash: canonical JSON of everything with 'manifest_sha256' absent.
    body = {k: v for k, v in doc.items() if k != 'manifest_sha256'}
    try:
        recomputed = _sha256_hex(_canonical_bytes(body))
        full = _canonical_bytes(doc)
    except (ValueError, TypeError) as exc:
        reasons.append('manifest not canonically serialisable: %s' % exc)
        return out, None
    out['manifest_sha256_recomputed'] = recomputed
    out['canonical_bytes_match'] = (full == raw)
    if 'manifest_sha256' not in doc:
        reasons.append('manifest_sha256 key absent')
    elif recomputed != recorded:
        reasons.append('manifest_sha256 mismatch: recorded %r, recomputed %s' % (recorded, recomputed))
    if full != raw:
        reasons.append('file bytes are not the canonical JSON of their content')
    _validate_manifest_structure(doc, reasons)
    # Pins, every one, from bytes.
    pins = doc.get('pins')
    if isinstance(pins, dict):
        for label in ('code_files', 'input_files'):
            lst = pins.get(label)
            if not isinstance(lst, list):
                continue
            for pin in lst:
                if not isinstance(pin, dict):
                    continue
                path = pin.get('path')
                rec = pin.get('sha256')
                praw, perr = _read_bytes(path) if isinstance(path, str) else (None, 'path is not a string')
                actual = _sha256_hex(praw) if praw is not None else None
                pok = actual is not None and isinstance(rec, str) and actual == rec.lower()
                out['pins_verified'].append({'path': path, 'recorded': rec, 'actual': actual, 'ok': bool(pok)})
                if not pok:
                    reasons.append('pin mismatch for %r: recorded %r, actual %r%s'
                                   % (path, rec, actual, '' if perr is None else ' (%s)' % perr))
    if reasons:
        return out, None
    out['ok'] = True
    return out, doc


def verify_freeze_manifest(*, freeze_manifest_path):
    """Recompute the manifest self-hash and every pin from bytes; check structure.

    ok=True only if: the file parses, its bytes equal the canonical JSON of
    its content, the recorded manifest_sha256 equals the recomputed one, the
    structure matches FREEZE_MANIFEST_C3V001 (43 ordered predictions, no
    forbidden key at any depth, target_velocities_included False), and every
    pinned file hashes to its recorded SHA256.
    """
    result, _doc = _verify_impl(freeze_manifest_path)
    return result


def score_after_freeze(*, freeze_manifest_path, target_rows):
    """Score frozen predictions against target rows; refuses unless the manifest verifies.

    target_rows: 43 dicts {'id', 'velocity', 'sigma'} in manifest order (the
    P46 observation schema). Any id/order mismatch, non-finite value or
    sigma <= 0 refuses. Invalid predictions are never within error. Counts are
    over all 43 rows. Writes nothing to disk.
    """
    reasons = []
    out = {'ok': False, 'refused': True, 'rows': [], 'within_error_count': None,
           'band_overlap_count': None, 'invalid_count': None, 'n_rows': N_QUERIES,
           'manifest_sha256': None, 'error_model': ERROR_MODEL, 'reasons': reasons}
    ver, doc = _verify_impl(freeze_manifest_path)
    out['manifest_sha256'] = ver.get('manifest_sha256_recorded')
    if not ver['ok'] or doc is None:
        reasons.append('REFUSED: freeze manifest did not verify')
        reasons.extend(ver['reasons'])
        return out
    ids = list(doc['query_ids'])
    preds = doc['predictions']
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
        if len(reasons) == 0:
            bound.append((float(row['velocity']), float(row['sigma'])))
    if reasons:
        reasons.insert(0, 'REFUSED: target_rows rejected')
        return out
    rows = []
    n_within = 0
    n_overlap = 0
    n_invalid = 0
    for i, q in enumerate(ids):
        pred = preds[i]
        observed, sigma = bound[i]
        valid = pred['valid'] is True and pred['velocity'] is not None
        predicted = float(pred['velocity']) if pred['velocity'] is not None else None
        band_low = float(pred['band_low']) if pred['band_low'] is not None else None
        band_high = float(pred['band_high']) if pred['band_high'] is not None else None
        residual = None
        sigma_ratio = None
        fractional = None
        within = False
        overlaps = False
        if predicted is not None:
            residual = predicted - observed
            sigma_ratio = residual / sigma
            fractional = (residual / observed) if observed != 0.0 else None
        if valid:
            within = abs(sigma_ratio) <= 1.0
            overlaps = (band_low <= observed + sigma) and (band_high >= observed - sigma)
        if not valid:
            n_invalid += 1
        if within:
            n_within += 1
        if overlaps:
            n_overlap += 1
        rows.append({
            'id': q,
            'observed_speed_km_s': observed,
            'predicted_speed_km_s': predicted,
            'band_low_km_s': band_low,
            'band_high_km_s': band_high,
            'quoted_sigma_km_s': sigma,
            'signed_residual_km_s': residual,
            'sigma_ratio': sigma_ratio,
            'fractional_error': fractional,
            'valid': bool(valid),
            'within_error': bool(within),
            'band_overlaps_error_bar': bool(overlaps),
        })
    out['rows'] = rows
    out['within_error_count'] = n_within
    out['band_overlap_count'] = n_overlap
    out['invalid_count'] = n_invalid
    out['refused'] = False
    out['ok'] = True
    return out
