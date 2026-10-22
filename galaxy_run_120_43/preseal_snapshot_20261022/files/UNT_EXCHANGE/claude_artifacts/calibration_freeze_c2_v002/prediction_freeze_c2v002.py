"""prediction_freeze_c2v002 -- Module 2 v002 (Claude2 lane), superseding prediction_freeze_c3v001.

NGC3198 43-query prediction freeze packager and post-freeze scorer.

Changes against v001 are listed in FREEZE_DELTA_NOTES.md (same folder). They fix Claude4 0023
A3 (partial envelopes frozen as valid) and A4 (vacuous pins), and implement the Claude2 contract
decisions D5 (per-member headline + reference member), D6 (null/fixed-direction sensitivity),
D8 (registered file hash), D9 (alternatives policy) and D10 (NGC3198 nuisance slots, units,
explicit null-space completion) on the freeze/scorer side.

Public API (keyword-only arguments, no defaults; every function returns a dict with at least
``ok: bool`` and ``reasons: list[str]``):

    load_query_manifest(*, path, expected_sha256)                                   [v001, unchanged]
    make_freeze_coordinate_spec(*, coordinates)                                     [new, D10]
    select_representative_points(*, exploration, interior_count, spec)              [D5/D7/D10]
    evaluate_envelopes(*, forward_ngc, points, spec, query_ids, budget)             [A3/D5/D10]
    select_reference_member(*, selection, evaluation)                               [new, D5]
    evaluate_sensitivity(*, forward_ngc, reference, selection, spec, query_ids,
                         null_direction_rule, budget)                               [new, D6]
    write_freeze_manifest(*, out_path, registration_path, parameter_region, observation_rule,
                          spec, selection, alternatives, alternative_evaluations, reference,
                          sensitivity, query_ids, code_files, input_files, notes,
                          allow_incomplete)                                         [A3/A4/D5-D10]
    verify_freeze_manifest(*, freeze_manifest_path)                                 [A4/D8]
    verify_registration(*, registration_path)                                       [new, D8]
    score_after_freeze(*, freeze_manifest_path, registration_path,
                       expected_manifest_file_sha256, target_rows)                  [D5/D8]

Invariants (kept from v001):
  * inert at import: no file I/O, no computation, no environment changes;
  * standard library only; no numpy objects are created or returned;
  * never reads any NGC3198 velocity. The only NGC3198 file it opens is the target-free query
    manifest. Target rows reach this module only through ``score_after_freeze``, which writes
    nothing to disk;
  * fails closed: anticipated bad input returns ok=False instead of raising; exceptions raised by
    the root-supplied ``forward_ngc`` are caught and logged as invalid evaluations;
  * canonical JSON is json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False);
    every file hash is SHA256 over raw bytes;
  * manifest and registration are written with exclusive create (never overwrite), carry
    ``target_velocities_included: False`` and refuse any forbidden target field name.
"""

import datetime
import hashlib
import json
import math
import numbers
import os
import stat

SCHEMA = 'FREEZE_MANIFEST_C2V002'
REGISTRATION_SCHEMA = 'FREEZE_REGISTRATION_C2V002'
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
                 'is a headline (CURRENT_INSTRUCTIONS L108)')
REFERENCE_RULE = ('REFERENCE MEMBER = the evaluated member whose 43 rows are all valid and whose projection '
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
SCOPES = (SCOPE_SHARED, SCOPE_DDO, SCOPE_NGC)
KINDS = ('distance', 'inclination', 'other')
DISTANCE_REFERENCE_MPC = {SCOPE_DDO: 4.04, SCOPE_NGC: 13.8}
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

# P46 harness FORBIDDEN set (lanes/P46_CODEX2/line_a_prediction_harness_v002.py)
# plus the four target-row names required by INTERFACE_0462_V001.
FORBIDDEN = frozenset({
    'vobs', 'vobs_km_s', 'observed_velocity', 'observed_km_s',
    'error_v_km_s', 'velocity_error', 'chi2', 'residual_km_s',
    'vgas', 'vdisk', 'vbul', 'vgas_km_s', 'vdisk_km_s', 'vbulge_km_s',
    'target_rows', 'targets', 'target_velocity', 'target_velocities',
})

MANIFEST_KEYS = frozenset({
    'schema', 'created_utc', 'freeze_status', 'incomplete_reasons', 'parameter_region', 'admitted_region',
    'coordinates', 'observation_rule', 'query_ids', 'units', 'semantics', 'alternatives', 'members',
    'member_evaluation', 'reference_member', 'pointwise_envelope', 'sensitivity', 'band_scope',
    'conditional_on_trial_values', 'alternative_results', 'headline_rule', 'within_error_rule', 'pins',
    'notes', 'target_velocities_included', 'manifest_sha256',
})
MEMBER_KEYS = frozenset({'member_id', 'point_index', 'role', 'log_index', 'u', 'identified_projection',
                         'theta_engine', 'theta_ngc', 'evaluated', 'forward_valid_flag', 'member_valid',
                         'row_valid', 'speeds_km_s', 'reasons', 'exception'})
MEMBER_EVAL_KEYS = frozenset({'status', 'stage', 'budget', 'evaluations_used', 'n_selected', 'n_evaluated',
                              'n_member_valid'})
ENVELOPE_ROW_KEYS = frozenset({'id', 'band_low_km_s', 'band_high_km_s', 'n_members', 'n_valid', 'valid',
                               'label'})
REFERENCE_KEYS = frozenset({'member_id', 'log_index', 'rule', 'centroid_identified', 'distance', 'ranking'})
SENS_KEYS = frozenset({'status', 'stage', 'budget', 'evaluations_used', 'reference_member_id',
                       'null_direction_rule', 'evaluations', 'per_query', 'per_target', 'label'})
SENS_ENTRY_KEYS = frozenset({'entry_id', 'kind', 'target', 'side', 'displacement', 'displacement_units',
                             'limited_by', 'u_displaced', 'theta_ngc', 'skipped_zero_displacement',
                             'evaluated', 'forward_valid_flag', 'row_valid', 'speeds_km_s',
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


def _canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


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


def _safe_scan(obj, where, hits, reasons):
    try:
        _scan_forbidden(obj, where, hits)
    except RecursionError:
        reasons.append('REFUSED: %s nested too deeply to screen' % where)


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
        extra = set(str(x) for x in c) - COORD_KEYS
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
        if kind not in KINDS:
            reasons.append('%s.kind must be one of %s' % (where, list(KINDS)))
            bad = True
        ref = c['reference_value']
        if ref is not None and not _is_real(ref):
            reasons.append('%s.reference_value must be a finite real or None' % where)
            bad = True
        if kind == 'distance':
            if scope not in DISTANCE_REFERENCE_MPC:
                reasons.append('%s distance coordinates must be ddo154_nuisance or ngc3198_nuisance' % where)
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
            if not isinstance(sens, dict) or sens.get('mode') not in ('box_ends', 'step'):
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
                else:
                    sens_norm = {'mode': 'step', 'step': float(sens['step'])}
            if not ((scope == SCOPE_SHARED and role == 'fixed') or scope == SCOPE_NGC):
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
    }


def _spec_from(spec, reasons):
    if isinstance(spec, dict) and isinstance(spec.get('spec'), dict):
        spec = spec['spec']
    if not isinstance(spec, dict) or 'coordinates' not in spec:
        reasons.append('spec must be the output of make_freeze_coordinate_spec')
        return None
    return _build_spec(spec['coordinates'], reasons)


def make_freeze_coordinate_spec(*, coordinates):
    """Validate the full coordinate list (engine coordinates plus NGC3198 nuisance slots).

    Every coordinate: {name, transform, lower, upper, role, trial_value, units, scope, kind,
    reference_value, sensitivity}. scope 'shared' (role free|fixed), 'ddo154_nuisance' (role
    nuisance; passed to the DDO154 engine only, never to forward_ngc) or 'ngc3198_nuisance' (role
    nuisance; never passed to the engine; held at trial_value in members and evaluated for
    sensitivity). kind 'distance' needs units Mpc and reference_value 4.04 (DDO154) or 13.8
    (NGC3198); kind 'inclination' needs units deg. NGC3198 must carry exactly one distance and one
    inclination slot. Returns 'engine_coordinates' (the six-field dicts for the engine, NGC3198
    slots excluded) and 'spec' (pass it to the other functions).
    """
    reasons = []
    out = {'ok': False, 'spec': None, 'engine_coordinates': [], 'ngc_theta_names': [],
           'bounds_semantics': BOUNDS_SEMANTICS, 'reasons': reasons}
    S = _build_spec(coordinates, reasons)
    if S is None:
        return out
    out['spec'] = {'coordinates': [dict(c, sensitivity=(dict(c['sensitivity']) if c['sensitivity'] else None))
                                   for c in S['coordinates']]}
    out['engine_coordinates'] = [{k: c[k] for k in ('name', 'transform', 'lower', 'upper', 'role', 'trial_value')}
                                 for c in S['coordinates'] if c['scope'] != SCOPE_NGC]
    out['ngc_theta_names'] = list(S['ngc_theta_names'])
    out['ok'] = True
    return out


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


def select_representative_points(*, exploration, interior_count, spec):
    """Choose the representative admitted members for NGC3198 propagation.

    v001 order kept (hull vertices per identified direction, then the anchor if admitted, then an
    evenly spaced interior subset by log_index), with one addition: the admitted point nearest the
    centroid of all admitted points in the identified subspace (role 'centroid_nearest') is
    inserted after the anchor so the reference-member rule can choose it.

    D10: right_vectors must be a COMPLETE orthonormal basis of the varying engine u space and
    identified + near_null must partition it; otherwise the call refuses (NULL_SPACE_NOT_COMPLETE).
    D7: the admitted set is labelled INNER_SAMPLE; region_possibly_truncated is set when the
    exploration did not complete, the engine flags or does not report truncation, or an admitted
    point touches a computational-box face.
    """
    reasons = []
    out = {'ok': False, 'points': [], 'hull_vertex_count': 0, 'interior_count_used': 0,
           'anchor_included': False, 'centroid_nearest_log_index': None, 'n_admitted': 0,
           'identified_directions': [], 'hull_directions': [], 'hull_box_consistent': None,
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
    n = len(S['varying_engine'])

    # D10: explicit, complete basis.
    vnames = ident.get('varying_names')
    if vnames is not None and list(vnames) != S['varying_engine']:
        reasons.append('identifiability.varying_names %r differ from the spec varying engine coordinates %r'
                       % (vnames, S['varying_engine']))
        return out
    rv = ident.get('right_vectors')
    if not isinstance(rv, (list, tuple)) or len(rv) != n:
        reasons.append('NULL_SPACE_NOT_COMPLETE: right_vectors must hold exactly %d direction vectors (one per '
                       'varying engine coordinate), got %s' % (n, len(rv) if isinstance(rv, (list, tuple)) else rv))
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
        reasons.append('exploration.admitted_points must be a non-empty list (status %r); an empty or '
                       'unproven region is not a prediction freeze' % (status,))
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
        seen_log.add(li)
        proj = [_dot(u, V[k]) for k in identified]
        admitted.append({'u': u, 'theta_natural': theta, 'log_index': li, 'proj': proj})
    if len(reasons) > nerr:
        return out
    N = len(admitted)
    out['n_admitted'] = N
    adm_proj = [{'log_index': pt['log_index'], 'projection': list(pt['proj'])} for pt in admitted]
    centroid = _centroid(adm_proj, len(identified))

    hull_box = ex.get('hull_box')
    hull_keys = None
    if isinstance(hull_box, dict) and hull_box:
        hull_keys = {}
        for k, box in hull_box.items():
            try:
                kk = int(k) if not isinstance(k, bool) else None
            except (TypeError, ValueError):
                kk = None
            if kk is None or not isinstance(box, dict) or not _is_real(box.get('min')) or \
                    not _is_real(box.get('max')):
                continue
            hull_keys[kk] = (float(box['min']), float(box['max']))

    selected = []
    selected_log = set()

    def _take(pt, role):
        if pt['log_index'] in selected_log:
            return False
        selected_log.add(pt['log_index'])
        selected.append({'u': list(pt['u']), 'theta_natural': dict(pt['theta_natural']), 'role': role,
                         'log_index': pt['log_index'], 'identified_projection': list(pt['proj'])})
        return True

    consistent = True if hull_keys else None
    prange = {}
    for j, k in enumerate(identified):
        proj = [(pt['proj'][j], pt['log_index'], i) for i, pt in enumerate(admitted)]
        pmin = min(proj, key=lambda t: (t[0], t[1]))
        pmax = min(proj, key=lambda t: (-t[0], t[1]))
        prange[str(k)] = {'min': float(pmin[0]), 'max': float(pmax[0])}
        out['hull_directions'].append({'direction_index': k, 'min_log_index': pmin[1],
                                       'max_log_index': pmax[1], 'projection_range': float(pmax[0] - pmin[0])})
        if hull_keys and k in hull_keys:
            lo, hi = hull_keys[k]
            if abs((hi - lo) - (pmax[0] - pmin[0])) > _HULL_BOX_TOL * (1.0 + abs(hi - lo)):
                consistent = False
                reasons.append('WARNING hull_box[%d] range %r differs from recomputed range %r'
                               % (k, hi - lo, pmax[0] - pmin[0]))
        _take(admitted[pmin[2]], ROLE_HULL)
        _take(admitted[pmax[2]], ROLE_HULL)
    out['hull_box_consistent'] = consistent
    out['hull_vertex_count'] = len(selected)

    anchor = ex.get('anchor')
    if anchor is None:
        reasons.append('NOTE anchor absent from exploration; not included')
    elif not isinstance(anchor, dict):
        reasons.append('anchor is not a dict')
        return out
    elif anchor.get('admitted') is not True:
        reasons.append('NOTE anchor not admitted; not included (members are admitted points only)')
    else:
        a_li = anchor.get('log_index')
        match = None
        if _is_int(a_li):
            match = next((pt for pt in admitted if pt['log_index'] == int(a_li)), None)
            if match is None:
                reasons.append('anchor.log_index %d not among admitted_points' % int(a_li))
                return out
        else:
            a_u = _bind_u(anchor.get('u'), 'anchor', reasons)
            if a_u is None:
                return out
            match = next((pt for pt in admitted if pt['u'] == a_u), None)
            if match is None:
                reasons.append('anchor is marked admitted but its u is not among admitted_points')
                return out
        out['anchor_included'] = True
        _take(match, ROLE_ANCHOR)

    def _dist(pt):
        return math.sqrt(math.fsum((a - b) ** 2 for a, b in zip(pt['proj'], centroid)))

    cn = min(admitted, key=lambda pt: (_dist(pt), pt['log_index']))
    out['centroid_nearest_log_index'] = cn['log_index']
    _take(cn, ROLE_CENTROID)

    remaining = sorted((pt for pt in admitted if pt['log_index'] not in selected_log),
                       key=lambda pt: pt['log_index'])
    for j in _evenly_spaced_indices(len(remaining), interior_count):
        _take(remaining[j], ROLE_INTERIOR)
    out['interior_count_used'] = sum(1 for p in selected if p['role'] == ROLE_INTERIOR)

    # D7 truncation evidence.
    evidence = []
    if status != STATUS_COMPLETE:
        evidence.append('EXPLORATION_STATUS_%s' % status)
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
    except (ValueError, RecursionError):
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
        'exploration_status': status if isinstance(status, str) else repr(status),
        'exploration_stage_reached': stage if isinstance(stage, str) else repr(stage),
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
    }
    out['points'] = selected
    out['ok'] = True
    return out


# --------------------------------------------------------------------------
# evaluate_envelopes (per-member arrays; strict validity)
# --------------------------------------------------------------------------

def _call_forward(forward_ngc, theta, ids):
    """Call forward_ngc once; return (flag, row_valid list, speeds list, reasons, exception)."""
    preasons = []
    exc = None
    result = None
    try:
        result = forward_ngc(dict(theta))
    except Exception as e:  # root-supplied callable: catch, log, treat as invalid
        exc = '%s: %s' % (type(e).__name__, e)
    nq = len(ids)
    row_valid = [False] * nq
    speeds = [None] * nq
    if exc is not None:
        preasons.append('exception raised by forward_ngc: ' + exc)
        return None, row_valid, speeds, preasons, exc
    if not isinstance(result, dict):
        preasons.append('forward_ngc returned %s, not a dict' % type(result).__name__)
        return None, row_valid, speeds, preasons, exc
    flag = result.get('valid')
    flag_ok = flag is True
    if not flag_ok:
        preasons.append('forward_ngc valid flag is not True (got %r)' % (flag,))
    rr = result.get('reasons')
    if isinstance(rr, (list, tuple)):
        for r in rr:
            preasons.append('forward_ngc reason: %s' % (r,))
    sp = result.get('speeds_km_s')
    if not isinstance(sp, dict):
        preasons.append('speeds_km_s is not a dict')
        return flag_ok, row_valid, speeds, preasons, exc
    for j, q in enumerate(ids):
        if q not in sp:
            preasons.append('missing id %s' % q)
            continue
        v = sp[q]
        if _is_real(v):
            speeds[j] = float(v)
            row_valid[j] = flag_ok
        else:
            preasons.append('non-finite or non-real value for %s: %r' % (q, v))
    idset = set(ids)
    extra = [k for k in sp if k not in idset]
    if extra:
        preasons.append('%d extra ids ignored' % len(extra))
    return flag_ok, row_valid, speeds, preasons, exc


def _pointwise_envelope(members, ids):
    """Strict A3 rule: a query is valid iff EVERY selected member was evaluated and valid at it."""
    rows = []
    n = len(members)
    for j, q in enumerate(ids):
        vals = [m['speeds_km_s'][j] for m in members if m['row_valid'][j]]
        nv = len(vals)
        rows.append({'id': q, 'band_low_km_s': (min(vals) if nv else None),
                     'band_high_km_s': (max(vals) if nv else None), 'n_members': n, 'n_valid': nv,
                     'valid': bool(n >= 1 and nv == n), 'label': ENVELOPE_LABEL})
    return rows


def evaluate_envelopes(*, forward_ngc, points, spec, query_ids, budget):
    """Evaluate forward_ngc at every selected member; freeze per-member arrays.

    forward_ngc receives the member's shared coordinates plus the NGC3198 nuisance slots at their
    trial values; DDO154 nuisances are never passed (D10). A row is valid iff the call returned a
    dict with valid is True and a finite value for that id; a member is valid iff all its rows
    are. A pointwise-envelope query is valid iff EVERY selected member was evaluated and valid
    there (A3). status COMPLETE iff every selected member was evaluated; budget exhaustion keeps
    the unevaluated members as evaluated=False records.
    """
    reasons = []
    out = {'ok': False, 'status': None, 'stage': 'ngc_members', 'members': [], 'envelopes': {},
           'pointwise_envelope': [], 'evaluations_used': 0, 'budget': None, 'n_selected': 0,
           'n_evaluated': 0, 'n_member_valid': 0, 'query_ids': [], 'reasons': reasons}
    if not callable(forward_ngc):
        reasons.append('forward_ngc must be callable')
    S = _spec_from(spec, reasons)
    ids = _check_query_ids(query_ids, reasons, False)
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
        if role not in ROLES:
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
                        'row_valid': [False] * len(ids), 'speeds_km_s': [None] * len(ids),
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
        flag, row_valid, speeds, preasons, exc = _call_forward(forward_ngc, m['theta_ngc'], ids)
        used += 1
        m['evaluated'] = True
        m['forward_valid_flag'] = flag
        m['row_valid'] = row_valid
        m['speeds_km_s'] = speeds
        m['member_valid'] = bool(all(row_valid))
        m['reasons'] = _cap_reasons(preasons)
        m['exception'] = exc
    n_eval = sum(1 for m in members if m['evaluated'])
    status = STATUS_COMPLETE if n_eval == len(members) else STATUS_BUDGET
    if status != STATUS_COMPLETE:
        reasons.append('BUDGET_EXHAUSTED: %d of %d selected members evaluated' % (n_eval, len(members)))
    env = _pointwise_envelope(members, ids)
    out.update({'status': status, 'members': members, 'pointwise_envelope': env,
                'envelopes': {r['id']: r for r in env}, 'evaluations_used': used, 'budget': budget,
                'n_selected': len(members), 'n_evaluated': n_eval,
                'n_member_valid': sum(1 for m in members if m['member_valid']), 'query_ids': list(ids),
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
        reasons.append('NO_VALID_MEMBER: no evaluated member has all 43 rows valid; nothing realizable '
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
    """Largest s >= 0 with a + s*d inside [0, 1]^n; components |d_i| <= _V_TOL are inert (A2 lesson)."""
    smax = math.inf
    for ai, di in zip(a, d):
        if abs(di) <= _V_TOL:
            continue
        lim = (1.0 - ai) / di if di > 0 else (0.0 - ai) / di
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
                         'skipped_zero_displacement': bool(t <= _ZERO_DISP),
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


def _sensitivity_summary(ref, entries, ids):
    active = [e for e in entries if not e['skipped_zero_displacement']]
    per_query = []
    for j, q in enumerate(ids):
        r = ref['speeds_km_s'][j] if ref['row_valid'][j] else None
        vals = [e['speeds_km_s'][j] for e in active if e['row_valid'][j]]
        allv = ([r] if r is not None else []) + vals
        valid = r is not None and len(vals) == len(active)
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
                          'label': SENSITIVITY_LABEL})
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


def evaluate_sensitivity(*, forward_ngc, reference, selection, spec, query_ids, null_direction_rule, budget):
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
                  'speeds_km_s': [None] * len(ids), 'delta_from_reference_km_s': [None] * len(ids),
                  'reasons': [], 'exception': None})
        if e['skipped_zero_displacement']:
            e['reasons'] = ['SKIPPED: zero displacement (reference already at this box face / trial value)']
        elif used >= budget:
            e['reasons'] = ['NOT_EVALUATED: sensitivity budget %d exhausted' % budget]
        else:
            flag, row_valid, speeds, preasons, exc = _call_forward(forward_ngc, e['theta_ngc'], ids)
            used += 1
            e['evaluated'] = True
            e['forward_valid_flag'] = flag
            e['row_valid'] = row_valid
            e['speeds_km_s'] = speeds
            e['delta_from_reference_km_s'] = [
                (float(s - r) if (rv and ok) else None)
                for s, r, rv, ok in zip(speeds, ref['speeds_km_s'], ref['row_valid'], row_valid)]
            e['reasons'] = _cap_reasons(preasons)
            e['exception'] = exc
        entries.append(e)
    pending = [e for e in entries if not e['skipped_zero_displacement'] and not e['evaluated']]
    status = STATUS_COMPLETE if not pending else STATUS_BUDGET
    if pending:
        reasons.append('BUDGET_EXHAUSTED: %d planned sensitivity evaluations not run' % len(pending))
    per_query, per_target = _sensitivity_summary(ref, entries, ids)
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
    decl = alternatives['declared']
    if not isinstance(decl, list) or not decl:
        reasons.append('alternatives.declared must be a non-empty list')
        return None
    names = []
    for i, a in enumerate(decl):
        where = 'alternatives.declared[%d]' % i
        if not isinstance(a, dict) or set(a) != {'name', 'kind', 'description', 'status'}:
            reasons.append('%s must have exactly name, kind, description, status' % where)
            continue
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
        if m['role'] not in ROLES or not _is_int(m['point_index']):
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
                m['forward_valid_flag'] not in (None, True, False):
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
        if not m['evaluated'] and (any(m['row_valid']) or any(s is not None for s in m['speeds_km_s'])):
            reasons.append('%s unevaluated member carries rows' % w)
            ok = False
        if m['member_valid'] != (m['evaluated'] and all(m['row_valid'])):
            reasons.append('%s.member_valid inconsistent with its rows' % w)
            ok = False
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


def _validate_envelope(env, members, ids, where, reasons):
    if not isinstance(env, list) or len(env) != len(ids):
        reasons.append('%s must be a list of %d rows' % (where, len(ids)))
        return
    if env != _pointwise_envelope(members, ids):
        reasons.append('%s differs from the envelope recomputed from the member arrays' % where)


def _validate_admitted_region(ar, S, reasons):
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
    for b in bad:
        reasons.append('admitted_region: ' + b)
    return None if bad else ar


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
    if sens['label'] != SENSITIVITY_LABEL or sens['stage'] != 'ngc_sensitivity':
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
    pq, pt = _sensitivity_summary(ref_member, entries, ids)
    if sens['per_query'] != pq or sens['per_target'] != pt:
        reasons.append('sensitivity: per_query/per_target differ from the values recomputed from evaluations')


def _validate_manifest_structure(doc, reasons):
    """Full structural + internal-consistency check (writer and verifier share it). Fails closed."""
    try:
        _validate_manifest_impl(doc, reasons)
    except (TypeError, KeyError, AttributeError, IndexError, ValueError, RecursionError) as exc:
        reasons.append('manifest structure malformed: %s: %s' % (type(exc).__name__, exc))


def _validate_manifest_impl(doc, reasons):
    if not isinstance(doc, dict):
        reasons.append('manifest is not a JSON object')
        return
    keys = set(doc)
    missing, extra = MANIFEST_KEYS - keys, keys - MANIFEST_KEYS
    if missing:
        reasons.append('manifest missing keys %s' % sorted(missing))
    if extra:
        reasons.append('manifest has unexpected keys %s' % sorted(extra))
    if missing:
        return
    for k, v in (('schema', SCHEMA), ('units', UNITS), ('semantics', SEMANTICS),
                 ('within_error_rule', WITHIN_ERROR_RULE), ('headline_rule', HEADLINE_RULE),
                 ('band_scope', BAND_SCOPE)):
        if doc[k] != v:
            reasons.append('%s differs from the frozen value' % k)
    if doc['target_velocities_included'] is not False:
        reasons.append('target_velocities_included is not False')
    if not isinstance(doc['created_utc'], str) or not doc['created_utc']:
        reasons.append('created_utc is not a string')
    if not isinstance(doc['parameter_region'], dict):
        reasons.append('parameter_region is not an object')
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
    _validate_member_eval(doc['member_evaluation'], members, 'member_evaluation', reasons)
    _validate_envelope(doc['pointwise_envelope'], members, ids, 'pointwise_envelope', reasons)
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
            if _validate_members(a['members'], S, ids, n_ident, w + '.members', reasons):
                _validate_member_eval(a['member_evaluation'], a['members'], w + '.member_evaluation', reasons)
                _validate_envelope(a['pointwise_envelope'], a['members'], ids, w + '.pointwise_envelope', reasons)
    if reasons:
        return
    expect = _incomplete_reasons(ar, doc['member_evaluation'], doc['sensitivity'], altres)
    if doc['incomplete_reasons'] != expect:
        reasons.append('incomplete_reasons %r differ from recomputed %r' % (doc['incomplete_reasons'], expect))
    if doc['freeze_status'] != (FREEZE_INCOMPLETE if expect else FREEZE_COMPLETE):
        reasons.append('freeze_status %r inconsistent with incomplete_reasons' % (doc['freeze_status'],))
    if doc['conditional_on_trial_values'] != _conditional_on_trial(S, ar, doc['sensitivity']):
        reasons.append('conditional_on_trial_values differs from the recomputed list')
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
    hits = []
    _safe_scan(doc, 'manifest', hits, reasons)
    if hits:
        reasons.append('forbidden target field name(s) present: %s' % hits)


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


def write_freeze_manifest(*, out_path, registration_path, parameter_region, observation_rule, spec, selection,
                          alternatives, alternative_evaluations, reference, sensitivity, query_ids, code_files,
                          input_files, notes, allow_incomplete):
    """Write the freeze manifest (canonical JSON, exclusive create) and its registration file.

    Refuses (A3) an incomplete run -- exploration not COMPLETE, any EVALUATED alternative's member
    evaluation not COMPLETE, or sensitivity not COMPLETE -- unless allow_incomplete is True, in
    which case freeze_status FREEZE_INCOMPLETE and the reasons are stamped into the manifest.
    Refuses (A4) empty pin lists, non-regular or zero-length pins, and code_files that omit this
    module. Refuses (D9) alternatives without an evaluated primary, and evaluations that do not
    match the declared EVALUATED set. The reference member must follow REFERENCE_RULE (D5). The
    assembled manifest must pass the same structure check the verifier applies.
    After the manifest, writes registration_path (D8) recording the manifest FILE sha256; that
    value must be logged before any target access and passed to score_after_freeze.
    """
    reasons = []
    out = {'ok': False, 'path': None, 'registration_path': None, 'manifest_sha256': None,
           'manifest_file_sha256': None, 'registration_file_sha256': None, 'bytes_written': 0,
           'freeze_status': None, 'incomplete_reasons': [], 'reasons': reasons}
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
    if not isinstance(parameter_region, dict):
        reasons.append('parameter_region must be a dict')
    if not isinstance(observation_rule, (dict, list, tuple, str)):
        reasons.append('observation_rule must be a dict, list or string')
    S = _spec_from(spec, reasons)
    ids = _check_query_ids(query_ids, reasons, True)
    if reasons:
        return out
    if not isinstance(selection, dict) or selection.get('ok') is not True:
        reasons.append('selection must be an ok output of select_representative_points')
        return out
    alts = _bind_alternatives(alternatives, reasons)
    if alts is None:
        return out
    if not isinstance(alternative_evaluations, dict) or set(alternative_evaluations) != set(alts['evaluated']):
        reasons.append('REFUSED (D9): alternative_evaluations keys %s must equal the EVALUATED_BEFORE_FREEZE '
                       'alternatives %s' % (sorted(alternative_evaluations) if isinstance(alternative_evaluations, dict)
                                            else alternative_evaluations, alts['evaluated']))
        return out
    for name, ev in alternative_evaluations.items():
        if not isinstance(ev, dict) or ev.get('ok') is not True or ev.get('query_ids') != list(ids):
            reasons.append('alternative_evaluations[%r] must be an ok evaluate_envelopes output on query_ids' % name)
    if not isinstance(reference, dict) or reference.get('ok') is not True:
        reasons.append('reference must be an ok output of select_reference_member')
    if not isinstance(sensitivity, dict) or sensitivity.get('ok') is not True:
        reasons.append('sensitivity must be an ok output of evaluate_sensitivity')
    if reasons:
        return out
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
    ar = selection['admitted_region']
    me = _member_eval_record(prim)
    incomplete = _incomplete_reasons(ar, me, sens_rec, alt_results)
    out['incomplete_reasons'] = list(incomplete)
    if incomplete and not allow_incomplete:
        reasons.append('REFUSED (A3): run is incomplete %s; pass allow_incomplete=True to stamp '
                       'FREEZE_INCOMPLETE' % incomplete)
        return out
    status = FREEZE_INCOMPLETE if incomplete else FREEZE_COMPLETE
    out['freeze_status'] = status

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
    if reasons:
        return out
    try:
        manifest = _plain({
            'schema': SCHEMA,
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
            'band_scope': BAND_SCOPE,
            'conditional_on_trial_values': _conditional_on_trial(S, ar, sens_rec),
            'alternative_results': alt_results,
            'headline_rule': HEADLINE_RULE,
            'within_error_rule': WITHIN_ERROR_RULE,
            'pins': {'code_files': code_pins, 'input_files': input_pins},
            'notes': notes,
            'target_velocities_included': False,
            'manifest_sha256': '0' * 64,
        }, 'manifest')
    except (ValueError, TypeError, RecursionError) as exc:
        reasons.append('manifest not canonically serialisable: %s: %s' % (type(exc).__name__, exc))
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
        reasons.append('manifest not canonically serialisable: %s' % exc)
        return out
    try:
        with open(out_path, 'xb') as fh:
            fh.write(payload)
    except (OSError, ValueError) as exc:
        reasons.append('REFUSED: could not create out_path: %s: %s' % (type(exc).__name__, exc))
        return out
    raw, real, err = _read_regular(out_path, True)
    if raw is None or raw != payload:
        reasons.append('read-back mismatch after write: %s' % (err or 'bytes differ'))
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
                       % (type(exc).__name__, exc))
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
    return doc


def _verify_impl(freeze_manifest_path):
    reasons = []
    out = {'ok': False, 'path': None, 'manifest_file_sha256': None, 'manifest_sha256_recomputed': None,
           'manifest_sha256_recorded': None, 'canonical_bytes_match': None, 'freeze_status': None,
           'pins_verified': [], 'reasons': reasons}
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


def verify_freeze_manifest(*, freeze_manifest_path):
    """Recompute the self-hash and check canonical bytes, the full v002 structure and internal
    consistency (envelope, reference rule, sensitivity plan, freeze status recomputed from the
    member arrays) and then every pin from bytes (regular, non-empty files only).

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
    except (ValueError, TypeError) as exc:
        reasons.append('registration not canonical: %s' % exc)
    if not _is_hex64(doc['expected_manifest_file_sha256']) or not _is_hex64(doc['manifest_sha256_self']):
        reasons.append('registration hashes malformed')
    if reasons:
        return out
    out.update({'expected_manifest_file_sha256': doc['expected_manifest_file_sha256'],
                'manifest_path': doc['manifest_path'], 'manifest_sha256_self': doc['manifest_sha256_self'],
                'ok': True})
    return out


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
    scored = []
    for m in members:
        rows = [_ladder_row(q, m['speeds_km_s'][j], m['row_valid'][j], bound[j][0], bound[j][1])
                for j, q in enumerate(ids)]
        scored.append({'member_id': m['member_id'], 'log_index': m['log_index'], 'role': m['role'],
                       'evaluated': m['evaluated'], 'member_valid': m['member_valid'],
                       'within_error_count': sum(1 for r in rows if r['within_error']),
                       'invalid_count': sum(1 for r in rows if not r['valid']), 'n_rows': len(rows),
                       'rows': rows})
    return scored


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
                     'band_overlaps_error_bar': overlaps, 'label': r['label']})
    return rows, n_overlap, n_invalid


def score_after_freeze(*, freeze_manifest_path, registration_path, expected_manifest_file_sha256, target_rows):
    """Score the frozen members against target rows; refuses unless identity and integrity hold.

    D8: refuses unless the registration file verifies, expected_manifest_file_sha256 (logged before
    target access) equals the registered value AND the manifest file's byte hash, and the manifest
    then fully verifies (self-hash, canonical bytes, structure, pins). Echoes the expected and
    actual file hashes, the self-hash, the registration file hash and a hash of the target rows.
    D5: reports every member's LADDER row table and within-error count over all 43 (invalid never
    passes); headline = distribution of PRIMARY member counts + the frozen reference member. The
    pointwise envelope and the box-limited sensitivity band are reported separately and labelled.
    target_rows: 43 dicts {'id', 'velocity', 'sigma'} in manifest order. Writes nothing.
    """
    reasons = []
    out = {'ok': False, 'refused': True, 'n_rows': N_QUERIES, 'error_model': ERROR_MODEL,
           'within_error_rule': WITHIN_ERROR_RULE, 'headline_rule': HEADLINE_RULE,
           'manifest_file_sha256_expected': None, 'manifest_file_sha256_actual': None,
           'manifest_sha256_self': None, 'registration_file_sha256': None, 'target_rows_sha256': None,
           'freeze_status': None, 'incomplete_reasons': None, 'headline': None, 'members': [],
           'pointwise_envelope': None, 'sensitivity': None, 'alternatives': [], 'reasons': reasons}
    if isinstance(expected_manifest_file_sha256, str):
        out['manifest_file_sha256_expected'] = expected_manifest_file_sha256.lower()
    reg = _verify_registration_impl(registration_path)
    out['registration_file_sha256'] = reg['registration_file_sha256']
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
    if not isinstance(freeze_manifest_path, str) or not freeze_manifest_path:
        reasons.append('REFUSED: freeze_manifest_path must be a non-empty string')
        return out
    raw, _real, err = _read_regular(freeze_manifest_path, True)
    if raw is None:
        reasons.append('REFUSED: %s' % err)
        return out
    actual = _sha256_hex(raw)
    out['manifest_file_sha256_actual'] = actual
    if actual != expected:
        reasons.append('REFUSED (D8): manifest file sha256 %s differs from the registered %s (edited or '
                       'different manifest)' % (actual, expected))
        return out
    vout = {'manifest_sha256_recomputed': None, 'manifest_sha256_recorded': None, 'canonical_bytes_match': None,
            'pins_verified': []}
    vreasons = []
    doc = _verify_bytes(raw, freeze_manifest_path, vout, vreasons)
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
        out['target_rows_sha256'] = _sha256_hex(_canonical_bytes(_plain(target_rows, 'target_rows')))
    except (ValueError, TypeError, RecursionError):
        out['target_rows_sha256'] = None
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
        'band_scope': doc['band_scope'],
        'note': ('unevaluated or invalid rows count as not within error; no pointwise or median curve is '
                 'a headline'),
    }
    erows, eov, einv = _band_rows(doc['pointwise_envelope'], 'band_low_km_s', 'band_high_km_s', ids, bound)
    out['pointwise_envelope'] = {'label': ENVELOPE_LABEL, 'rows': erows, 'band_overlap_count': eov,
                                 'invalid_count': einv, 'headline': False}
    sens = doc['sensitivity']
    srows, sov, sinv = _band_rows(sens['per_query'], 'box_limited_band_low_km_s', 'box_limited_band_high_km_s',
                                  ids, bound)
    for r, pq in zip(srows, sens['per_query']):
        r['reference_speed_km_s'] = pq['reference_speed_km_s']
        r['max_abs_delta_km_s'] = pq['max_abs_delta_km_s']
    out['sensitivity'] = {'label': SENSITIVITY_LABEL, 'status': sens['status'], 'rows': srows,
                          'band_overlap_count': sov, 'invalid_count': sinv, 'headline': False,
                          'conditional_on_trial_values': doc['conditional_on_trial_values']}
    alts = []
    for a in doc['alternatives']['declared']:
        rec = {'name': a['name'], 'kind': a['kind'], 'status': a['status'],
               'role': 'PRIMARY' if a['name'] == doc['alternatives']['primary'] else 'NON_PRIMARY'}
        if rec['role'] == 'PRIMARY':
            rec.update({'scored': True, 'headline': True})
        elif a['status'] == ALT_EVALUATED:
            am = _score_members(doc['alternative_results'][a['name']]['members'], ids, bound)
            rec.update({'scored': True, 'headline': False,
                        'member_within_error_counts': _distribution([m['within_error_count'] for m in am]),
                        'members': am,
                        'member_evaluation_status':
                            doc['alternative_results'][a['name']]['member_evaluation']['status']})
        else:
            rec.update({'scored': False, 'headline': False,
                        'note': 'NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline'})
        alts.append(rec)
    out['alternatives'] = alts
    out['refused'] = False
    out['ok'] = True
    return out
