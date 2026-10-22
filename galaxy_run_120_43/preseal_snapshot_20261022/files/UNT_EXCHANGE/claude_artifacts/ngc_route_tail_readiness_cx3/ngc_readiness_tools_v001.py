"""Inert readiness helpers. No solver, launcher, target loader, or network access."""
import copy
import hashlib
import json
import math
from pathlib import Path


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def write_x(path, obj):
    with Path(path).open('x') as f:
        f.write(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + '\n')


def truncate_roster(columns, query_rows):
    """Apply A14 C3 to a complete, certified confinement classification.

    Each column supplies id, R_kpc, HI_mass_kg and confinement. Numerical
    failures or unknown classifications are not evidence of unconfinement.
    All azimuths at and beyond the first unconfined radius are dropped;
    original quadrature weights/masses are retained without renormalization.
    This computes a candidate cut only, not a new fixed point.
    """
    if not columns or len({c['id'] for c in columns}) != len(columns):
        raise ValueError('ROSTER_EMPTY_OR_DUPLICATE')
    for c in columns:
        if c['confinement'] not in ('CONFINED', 'CERTIFIED_UNCONFINED'):
            raise ValueError('CONFINEMENT_UNDECIDED')
        if not math.isfinite(c['R_kpc']) or c['R_kpc'] < 0:
            raise ValueError('INVALID_RADIUS')
        if not math.isfinite(c['HI_mass_kg']) or c['HI_mass_kg'] < 0:
            raise ValueError('INVALID_HI_MASS')
    total = math.fsum(c['HI_mass_kg'] for c in columns)
    if total <= 0:
        raise ValueError('NO_POSITIVE_HI_MASS')
    cut = min((c['R_kpc'] for c in columns if c['confinement'] == 'CERTIFIED_UNCONFINED'), default=None)
    kept = [copy.deepcopy(c) for c in columns if cut is None or c['R_kpc'] < cut]
    dropped = [c for c in columns if cut is not None and c['R_kpc'] >= cut]
    rows = copy.deepcopy(query_rows)
    if len({r['id'] for r in rows}) != len(rows):
        raise ValueError('DUPLICATE_QUERY')
    for r in rows:
        if not math.isfinite(r['radius_kpc']) or r['radius_kpc'] < 0:
            raise ValueError('INVALID_QUERY_RADIUS')
        if cut is not None and r['radius_kpc'] > cut:
            r.update(valid=False, speed_km_s=None, invalid_reason='QUERY_BEYOND_FIRST_UNCONFINED_RADIUS')
    return {
        'schema': 'NGC_CANDIDATE_ROSTER_CUT_CX3V001',
        'status': 'CANDIDATE_CUT_NOT_A_FIXED_POINT',
        'first_unconfined_R_kpc': cut,
        'last_kept_R_kpc': max((c['R_kpc'] for c in kept), default=None),
        'dropped_HI_mass_fraction': math.fsum(c['HI_mass_kg'] for c in dropped) / total,
        'HI_mass_kg_before': total,
        'columns_kept': len(kept), 'columns_dropped': len(dropped),
        'kept_columns': kept, 'query_rows': rows,
        'source_rebuild_required': bool(dropped),
        'fixed_point_confinement_recheck_required': bool(dropped),
        'assumption': 'SA-TRUNC-01: omitted gas field not evaluated; no renormalization',
    }


def validate_result(result):
    if result.get('galaxy') != 'NGC3198' or result.get('status') != 'COMPLETED':
        raise ValueError('NOT_COMPLETED_NGC_RESULT')
    rows = result.get('rows', [])
    expected = [f'NGC3198-Q{i:02d}' for i in range(1, 44)]
    if [r.get('id') for r in rows] != expected:
        raise ValueError('ROW_ROSTER_NOT_EXACT_43')
    speeds = result.get('speeds_km_s', {})
    if set(speeds) != set(expected):
        raise ValueError('SPEED_ROSTER_NOT_EXACT_43')
    for r in rows:
        v = r.get('speed_km_s')
        if speeds[r['id']] != v:
            raise ValueError('ROW_SPEED_MAP_DISAGREEMENT')
        if r.get('valid') is False:
            if v is not None:
                raise ValueError('INVALID_ROW_HAS_SPEED')
        elif not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v):
            raise ValueError('NONFINITE_ROW')
    passes = result.get('passes', [])
    if not passes or [p.get('pass') for p in passes] != list(range(1, len(passes)+1)):
        raise ValueError('PASS_ROSTER_GAP')
    if result.get('final_pass') != len(passes) or passes[-1].get('rows') != rows:
        raise ValueError('FINAL_PASS_DISAGREEMENT')


def compare_ngc_results(parent, new, gate='TAIL_OFF_IDENTITY'):
    """Strict result-assembly comparison, distinct from physical tail convergence.

    TAIL_OFF_IDENTITY: first v010 NGC route-B result against a v009 parent
    with the same physical input and admitted route-A state. EMPTY_TAIL_IDENTITY
    additionally permits the explicitly declared empty tail metadata. Nonempty
    tail differences cannot establish parent identity and are refused here.
    Stage NPZ custody is checked separately by compare_stage_arrays.
    """
    failures = []
    try:
        validate_result(parent)
        validate_result(new)
    except ValueError as exc:
        return {'verdict': 'FAIL', 'failures': [str(exc)]}
    if gate not in ('TAIL_OFF_IDENTITY', 'EMPTY_TAIL_IDENTITY'):
        raise ValueError('UNKNOWN_GATE')
    def contains_tail(obj):
        if isinstance(obj, dict):
            return any(k in ('uv_tail', 'uv_tail_tap') or contains_tail(v) for k, v in obj.items())
        return isinstance(obj, list) and any(contains_tail(v) for v in obj)
    if contains_tail(parent):
        failures.append('V009_PARENT_HAS_STRAY_TAIL')
    if gate == 'TAIL_OFF_IDENTITY' and contains_tail(new):
        failures.append('TAIL_OFF_STRAY_TAIL')
    if gate == 'EMPTY_TAIL_IDENTITY':
        u = new.get('uv_tail', {})
        if u.get('domain_empty_all_stages') is not True:
            failures.append('NONEMPTY_TAIL_NOT_AN_IDENTITY_TEST')
        for rec in u.get('stage_records', []):
            if rec.get('empty') is not True:
                failures.append('NONEMPTY_STAGE_TAIL')
    science = ('status', 'valid', 'reasons', 'galaxy', 'final_pass', 'picard_bound_met',
               'rows', 'speeds_km_s', 'invalid_rows', 'headline_rule', 'alternative_label')
    for key in science:
        if parent.get(key) != new.get(key):
            failures.append('RESULT_DIFFERENCE:' + key)
    for i, (a, b) in enumerate(zip(parent['passes'], new['passes']), 1):
        for key in ('pass', 'rows', 'invalid_rows', 'max_abs_change_km_s',
                    'column_failures', 'rotation_positive', 'minimum_rotation_square',
                    'nonpositive_indices', 'nonaxisymmetric_residual_maxima', 'residual_units'):
            if a.get(key) != b.get(key):
                failures.append(f'PASS_DIFFERENCE:{i}:{key}')
    if len(parent['passes']) != len(new['passes']):
        failures.append('PASS_COUNT_DIFFERENCE')
    if parent.get('normalized_spec') != new.get('normalized_spec'):
        # Identity tests must use the same normalized physical input. Tail and
        # label are the only permitted per-spec differences, and tail only for
        # the explicit empty-tail gate.
        a, b = copy.deepcopy(parent.get('normalized_spec')), copy.deepcopy(new.get('normalized_spec'))
        if not isinstance(a, dict) or not isinstance(b, dict):
            failures.append('SPEC_MISSING')
        else:
            a.pop('label', None); b.pop('label', None)
            if gate == 'EMPTY_TAIL_IDENTITY':
                b.get('numerics', {}).pop('uv_tail', None)
            if a != b:
                failures.append('SPEC_DIFFERENCE')
    ra = new.get('route_a_outcome', {}).get('ro1', {})
    if ra.get('fired') is not False:
        failures.append('RO1_FIRED_OR_MISSING_IN_IDENTITY')
    if not isinstance(ra.get('armed'), bool):
        failures.append('RO1_ARMED_MISSING')
    return {'verdict': 'PASS_RESULT_ASSEMBLY_EQUAL' if not failures else 'FAIL',
            'gate': gate, 'failures': failures,
            'scope': 'Result assembly only; stage arrays and source custody require separate checks; no fixed-point claim.'}


def compare_stage_arrays(parent_path, new_path):
    import numpy as np
    with np.load(parent_path, allow_pickle=False) as a, np.load(new_path, allow_pickle=False) as b:
        if sorted(a.files) != sorted(b.files):
            return False
        return all(a[k].dtype == b[k].dtype and a[k].shape == b[k].shape and
                   a[k].tobytes() == b[k].tobytes() for k in a.files)
