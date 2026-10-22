"""ngc3198_forward_adapter_c3v001.py -- Module B of INTERFACE_0463_V001 (Claude3 lane, dispatch 0463).

theta -> seed mapping and result reader for the never-launched NGC43 root worker
  R/helpers/recovered_packet_audit/ngc43_composite_coupled_root_worker_v001.py
  SHA256 1b95a4ff333f17cf7bc6ab56b76c4e615e982a298ee1a95fd80f07c8ab6c0ca4
with R = /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13.

Public API (frozen by INTERFACE_0463_V001, Module B; six functions, reproduce_comparison replaced by
check_query_binding):
  exposed_coordinates()
  write_seed(*, base_seed_path, base_seed_sha256, theta, out_path)
  read_result(*, outdir, region_path, region_sha256)        # region = the target-free query manifest
  check_query_binding(*, manifest_path, manifest_sha256)
  make_theta_to_seed(*, base_seed_path, base_seed_sha256)
  make_result_reader(*, region_path, region_sha256)
Addition beyond the six (documented in NGC_ADAPTER_NOTES_0463_V001.md):
  seed_admissibility(*, seed_path, seed_sha256)              # read-only worker-admissibility report

Conventions: Python 3.12, standard library only (no numpy object is created or returned), inert at
import, keyword-only arguments without defaults, every public function returns {ok, reasons, ...} and
fails closed, canonical JSON = json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False),
every pin is SHA256 over bytes and is verified before use.  Nothing here reads an NGC3198 velocity,
runs a worker, uses the network or deletes anything.

What the worker reads from its seed (worker lines 61-66):
  seed['numerical_inputs']                     -> passed as **prep_arguments to prepare_inputs(...)
  seed['numerical_inputs']['h2_tail_mass_rtol'] -> explicit positive finite non-bool (worker line 62-64)
  seed['pins']                                 -> {path: sha256}, each verified from bytes (worker 65-66)
Nothing else in the seed is read by the worker, the binding or the prep module; 'physical' is a mirror
block (present in the DDO V002 seed) that is kept consistent with numerical_inputs by write_seed.

Result layout bound by read_result (worker line 101-102, binding line 83, prediction module v005 line
221-224):
  <outdir>/result.json = {result: <binding output>, seed_pin, input_pins, elapsed_seconds,
                          accepted_for_calibration: false, scope}
  <binding output>     = {result: <prediction output>, H2_custody, binding_custody, source_pins, ...}
  <prediction output>  = {rows: [{id, speed_km_s}] * 43, units: 'km/s', semantics: 'TOTAL_OBSERVABLE',
                          predictions_available: true, ...}
  <outdir>/finish.json = {status: 'RETURNED_ACTUAL_RESULT', result_path, result_sha256, elapsed_seconds}
  <outdir>/start.json  = {seed, input_pins, worker_pin, ...}
Speeds are read as speed_km_s = /result/result/rows[i]/speed_km_s (identity transform; the 72-degree
physical / 73-degree released projection and the /1000 to km/s are applied inside the worker chain).
"""

import hashlib
import json
import math
import os

ROOT = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'

WORKER_PATH = ROOT + '/helpers/recovered_packet_audit/ngc43_composite_coupled_root_worker_v001.py'
WORKER_SHA256 = '1b95a4ff333f17cf7bc6ab56b76c4e615e982a298ee1a95fd80f07c8ab6c0ca4'
BINDING_PATH = ROOT + '/helpers/recovered_packet_audit/ngc_composite_full_coupled_binding_v001.py'
BINDING_SHA256 = '9e9caf83bcbbe259d371e923242cddc9011aa7f9f9830d63479138756d9b1248'
PREP_PATH = ROOT + '/helpers/recovered_packet_audit/ngc_actual_initial_source_preparation_v001.py'
PREP_SHA256 = 'c54c7cc995f0bb59bb5d81a3f1267dba5dae48d116302c9c0438fe7e5a53710f'
MANIFEST_PATH = ROOT + '/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json'
MANIFEST_SHA256 = 'a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494'
DISTINCT_REVIEW_PATH = ROOT + '/helpers/response_packet_audit/NGC43_COMPOSITE_ROOT_WORKER_DISTINCT_REVIEW_V001.json'
DISTINCT_REVIEW_SHA256 = '32736643ff32472c5a00ebab4eb91881be5332508f7f39b31a9e31e5f489c1ca'

QUERY_COUNT = 43
QUERY_IDS = tuple('NGC3198-Q%02d' % i for i in range(1, QUERY_COUNT + 1))
MANIFEST_SCHEMA = 'NGC3198_TARGET_FREE_QUERY_MANIFEST_V001'
MANIFEST_COLUMNS = ('data_row_index', 'query_id', 'source_line_number', 'Rad_text', 'Rad_unit')
SMALLEST_QUERY_RADIUS_KPC = 0.32  # manifest row 1 (Q01); prediction module requires 0 < pressure_step < R

# Keyword-only signature of prepare_inputs in the NGC prep module (read with ast; order as declared).
NUMERICAL_INPUT_KEYS = (
    'h2_tail_mass_rtol', 'Eref_J', 'ell_F_m', 'gamma', 'solar_mass_kg', 'kpc_m', 'kmax_inverse_kpc',
    'fourier_points_per_axis', 'source_gauss_order', 'source_azimuth_count', 'observation_azimuth_count',
    'pressure_step_kpc', 'azimuth_step_rad', 'hi_search_step_kpc', 'hi_search_limit_kpc',
    'hi_root_tolerance_kpc', 'hi_log_lapse_tolerance', 'hi_max_metric_calls', 'hi_panels_per_side',
    'max_iterations', 'relaxation', 'source_atol_J', 'source_rtol', 'pressure_atol_Pa_per_m',
    'pressure_rtol', 'reality_atol', 'reality_rtol', 'relative_singular_floor', 'hermitian_tolerance',
    'solve_rtol', 'solve_atol', 'progress_directory', 'analytic_initial_azimuth', 'composite_grid_spec')
# progress_directory may be null (prep default None; binding excludes it from the checkpoint identity).
NULLABLE_INPUT_KEYS = ('progress_directory',)
PHYSICAL_MIRROR_KEYS = ('Eref_J', 'ell_F_m', 'gamma', 'solar_mass_kg', 'kpc_m')
EXPOSED_NAMES = ('Eref_J', 'ell_F_m', 'gamma')
POSITIVE_SCALARS = ('Eref_J', 'ell_F_m', 'solar_mass_kg', 'kpc_m', 'kmax_inverse_kpc', 'pressure_step_kpc',
                    'azimuth_step_rad', 'hi_search_step_kpc', 'hi_search_limit_kpc', 'hi_root_tolerance_kpc')
INTEGER_ORDERS = ('fourier_points_per_axis', 'source_gauss_order', 'source_azimuth_count',
                  'observation_azimuth_count')
FINITE_NUMBERS = ('hi_log_lapse_tolerance', 'hi_max_metric_calls', 'hi_panels_per_side', 'max_iterations',
                  'relaxation', 'source_atol_J', 'source_rtol', 'pressure_atol_Pa_per_m', 'pressure_rtol',
                  'reality_atol', 'reality_rtol', 'relative_singular_floor', 'hermitian_tolerance',
                  'solve_rtol', 'solve_atol')

RESULT_TRANSFORM = ('identity: speeds_km_s[id] = float(result.json:/result/result/rows[i]/speed_km_s) with '
                    'rows[i].id == manifest rows[i].query_id; no distance, inclination or estimator rescaling '
                    'is applied by the reader (the 72-degree physical / 73-degree released projection and the '
                    '/1000 to km/s are applied inside the worker chain: binding line 71-72, prediction v005 '
                    'line 196-215); same convention as the DDO evaluator, which uses v = float(row[speed_km_s]).')

MODULE_INFO = {
    'module': 'ngc3198_forward_adapter_c3v001',
    'interface': 'INTERFACE_0463_V001 Module B',
    'worker': {'path': WORKER_PATH, 'sha256': WORKER_SHA256},
    'binding': {'path': BINDING_PATH, 'sha256': BINDING_SHA256},
    'prep': {'path': PREP_PATH, 'sha256': PREP_SHA256},
    'manifest': {'path': MANIFEST_PATH, 'sha256': MANIFEST_SHA256},
    'distinct_review': {'path': DISTINCT_REVIEW_PATH, 'sha256': DISTINCT_REVIEW_SHA256},
    'launched_ngc_result_exists': False,
}


# ----------------------------------------------------------------------------------------------------
# helpers (private)
# ----------------------------------------------------------------------------------------------------

def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def _is_hex_sha256(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s)


def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _is_finite_number(x):
    return _is_number(x) and math.isfinite(float(x))


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _verify_pin(path, expected, label, reasons):
    """Verify SHA256 over bytes. Appends a reason and returns None on failure, else the actual digest."""
    if not isinstance(path, str) or not path:
        reasons.append('%s: path must be a non-empty string' % label)
        return None
    if not _is_hex_sha256(expected):
        reasons.append('%s: expected sha256 must be 64 lowercase hex characters' % label)
        return None
    if not os.path.isfile(path):
        reasons.append('%s: file not found: %s' % (label, path))
        return None
    try:
        actual = _sha256_file(path)
    except OSError as exc:
        reasons.append('%s: unreadable: %s (%s)' % (label, path, exc))
        return None
    if actual != expected:
        reasons.append('%s: PIN_MISMATCH %s expected %s got %s' % (label, path, expected, actual))
        return None
    return actual


def _reject_nonfinite_constant(name):
    raise ValueError('non-finite JSON constant %s' % name)


def _load_json_bytes(path, label, reasons):
    """Parse JSON from a file, refusing NaN/Infinity constants. Returns the object or None."""
    try:
        with open(path, 'rb') as f:
            raw = f.read()
    except OSError as exc:
        reasons.append('%s: unreadable: %s (%s)' % (label, path, exc))
        return None
    try:
        return json.loads(raw.decode('utf-8'), parse_constant=_reject_nonfinite_constant)
    except (ValueError, UnicodeDecodeError) as exc:
        reasons.append('%s: invalid JSON: %s (%s)' % (label, path, exc))
        return None


def _leaf_count(obj):
    if isinstance(obj, dict):
        return sum(_leaf_count(v) for v in obj.values()) if obj else 1
    if isinstance(obj, list):
        return sum(_leaf_count(v) for v in obj) if obj else 1
    return 1


def _deep_copy_json(obj):
    return json.loads(_canonical(obj))


def _check_manifest_object(m, reasons):
    """Structural checks on the parsed target-free manifest. Returns the binding list or None."""
    if not isinstance(m, dict):
        reasons.append('manifest: top level is not an object')
        return None
    if m.get('schema') != MANIFEST_SCHEMA:
        reasons.append('manifest: schema is not %s' % MANIFEST_SCHEMA)
    if m.get('object') != 'NGC3198':
        reasons.append('manifest: object is not NGC3198')
    cols = m.get('emitted_columns')
    if not isinstance(cols, list) or tuple(cols) != MANIFEST_COLUMNS:
        reasons.append('manifest: emitted_columns differ from %s' % (MANIFEST_COLUMNS,))
    if m.get('no_other_columns_emitted') is not True:
        reasons.append('manifest: no_other_columns_emitted is not true')
    if m.get('rad_unit') != 'kpc':
        reasons.append('manifest: rad_unit is not kpc')
    rows = m.get('rows')
    if not isinstance(rows, list) or len(rows) != QUERY_COUNT:
        reasons.append('manifest: rows is not a list of %d' % QUERY_COUNT)
        return None
    binding = []
    previous = None
    seen = set()
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            reasons.append('manifest: row %d is not an object' % i)
            return None
        extra = set(r) - set(MANIFEST_COLUMNS)
        if extra:
            # target-free guard: a row carrying any column outside the emitted five is refused unread
            reasons.append('manifest: row %d carries non-emitted columns %s' % (i, sorted(extra)))
            return None
        missing = set(MANIFEST_COLUMNS) - set(r)
        if missing:
            reasons.append('manifest: row %d lacks columns %s' % (i, sorted(missing)))
            return None
        qid = r['query_id']
        if qid != QUERY_IDS[i]:
            reasons.append('manifest: row %d query_id %r is not %r' % (i, qid, QUERY_IDS[i]))
        if qid in seen:
            reasons.append('manifest: duplicate query_id %r' % qid)
        seen.add(qid)
        if r['data_row_index'] != i + 1:
            reasons.append('manifest: row %d data_row_index %r is not %d' % (i, r['data_row_index'], i + 1))
        if r['Rad_unit'] != 'kpc':
            reasons.append('manifest: row %d Rad_unit is not kpc' % i)
        text = r['Rad_text']
        try:
            radius = float(text) if isinstance(text, str) else float('nan')
        except ValueError:
            radius = float('nan')
        if not math.isfinite(radius) or radius <= 0:
            reasons.append('manifest: row %d Rad_text %r is not a finite positive number' % (i, text))
        elif previous is not None and radius <= previous:
            reasons.append('manifest: row %d radius %r not strictly increasing' % (i, text))
        previous = radius if math.isfinite(radius) else previous
        binding.append({'query_id': qid, 'worker_index': i, 'data_row_index': r['data_row_index'],
                        'Rad_text': text, 'radius_kpc': radius, 'source_line_number': r['source_line_number']})
    if 'velocit' not in str(m.get('not_included', '')).lower():
        reasons.append('manifest: not_included does not state that velocities are absent')
    return binding


def _load_pinned_manifest(path, expected_sha, reasons):
    """Verify the manifest pin from bytes, require the pinned V001 bytes, parse and check. Returns binding."""
    actual = _verify_pin(path, expected_sha, 'manifest', reasons)
    if actual is None:
        return None
    if actual != MANIFEST_SHA256:
        reasons.append('manifest: bytes are not the pinned NGC3198_TARGET_FREE_QUERY_MANIFEST_V001 (%s); the '
                       'worker prep reads that file by fixed path, so another manifest cannot bind its rows'
                       % MANIFEST_SHA256)
        return None
    m = _load_json_bytes(path, 'manifest', reasons)
    if m is None:
        return None
    binding = _check_manifest_object(m, reasons)
    if binding is None or reasons:
        return None
    return binding


def _seed_schema(seed, reasons):
    """Schema the worker needs: numerical_inputs with all prep keys, pins dict. Returns True if ok."""
    if not isinstance(seed, dict):
        reasons.append('seed: top level is not an object')
        return False
    ni = seed.get('numerical_inputs')
    if not isinstance(ni, dict):
        reasons.append('seed: numerical_inputs is not an object (worker line 62)')
        return False
    missing = [k for k in NUMERICAL_INPUT_KEYS if k not in ni]
    if missing:
        reasons.append('seed: numerical_inputs lacks prep keys %s (prepare_inputs(**prep_arguments) would '
                       'raise TypeError)' % missing)
    extra = [k for k in ni if k not in NUMERICAL_INPUT_KEYS]
    if extra:
        reasons.append('seed: numerical_inputs carries keys unknown to prepare_inputs %s (TypeError)' % extra)
    pins = seed.get('pins')
    if not isinstance(pins, dict):
        reasons.append('seed: pins is not an object (worker line 65)')
    else:
        for p, s in pins.items():
            if not isinstance(p, str) or not _is_hex_sha256(s):
                reasons.append('seed: pins entry %r is not path -> 64-hex sha256' % (p,))
    phys = seed.get('physical')
    if phys is not None and not isinstance(phys, dict):
        reasons.append('seed: physical is present but not an object')
    return not reasons


def _verify_seed_pins(seed, reasons):
    """Verify every seed['pins'] entry from bytes (the worker does the same at line 65-66)."""
    count = 0
    for p, s in seed['pins'].items():
        if _verify_pin(p, s, 'seed pin', reasons) is not None:
            count += 1
    return count


def _admissibility(seed):
    """Worker/binding/prep admission checks that can be decided from the seed alone.

    Returns (admissible, missing_inputs, problems). missing_inputs lists required keys that are null;
    problems lists values that the worker chain would reject. Checks mirror worker lines 62-64,
    binding line 31-32, prep lines 46-56 and 137-146 (composite grid), prediction v005 line 115-117
    (0 < pressure_step < R, 0 < azimuth_step < pi) and 46-49 (non-negative pressure tolerances).
    Checks that live only inside modules not read here (HI free-boundary budgets, composite solver
    controls) are limited to finiteness."""
    ni = seed['numerical_inputs']
    missing = [k for k in NUMERICAL_INPUT_KEYS if k not in NULLABLE_INPUT_KEYS and ni.get(k) is None]
    problems = []

    def present(k):
        return k in ni and ni[k] is not None

    h2 = ni.get('h2_tail_mass_rtol')
    if present('h2_tail_mass_rtol') and not (_is_finite_number(h2) and h2 > 0):
        problems.append('h2_tail_mass_rtol must be a positive finite non-bool number (worker line 62-64)')
    for k in POSITIVE_SCALARS:
        if present(k) and not (_is_finite_number(ni[k]) and ni[k] > 0):
            problems.append('%s must be a positive finite number (prep line 46-49)' % k)
    if present('gamma') and not _is_finite_number(ni['gamma']):
        problems.append('gamma must be a finite number (prep line 49)')
    for k in INTEGER_ORDERS:
        if present(k) and not (_is_int(ni[k]) and ni[k] >= 2):
            problems.append('%s must be an int >= 2 (prep line 50-53)' % k)
    nk = ni.get('fourier_points_per_axis')
    if _is_int(nk) and nk % 2:
        problems.append('fourier_points_per_axis must be even (prep line 54-55)')
    for k in ('source_azimuth_count', 'observation_azimuth_count'):
        if _is_int(ni.get(k)) and ni[k] < 4:
            problems.append('%s must be >= 4 (prep line 56-57)' % k)
    for k in FINITE_NUMBERS:
        if present(k) and not _is_finite_number(ni[k]):
            problems.append('%s must be a finite number' % k)
    for k in ('pressure_atol_Pa_per_m', 'pressure_rtol'):
        if _is_finite_number(ni.get(k)) and ni[k] < 0:
            problems.append('%s must be >= 0 (prediction v005 line 48-49)' % k)
    ps = ni.get('pressure_step_kpc')
    if _is_finite_number(ps) and not (0 < ps < SMALLEST_QUERY_RADIUS_KPC):
        problems.append('pressure_step_kpc must satisfy 0 < step < %s kpc (smallest manifest radius; '
                        'prediction v005 line 115-117)' % SMALLEST_QUERY_RADIUS_KPC)
    az = ni.get('azimuth_step_rad')
    if _is_finite_number(az) and not (0 < az < math.pi):
        problems.append('azimuth_step_rad must lie in (0, pi) (prediction v005 line 116)')
    pd = ni.get('progress_directory')
    if pd is not None and not isinstance(pd, str):
        problems.append('progress_directory must be null or a string')
    if present('analytic_initial_azimuth') and ni['analytic_initial_azimuth'] is not True:
        problems.append('analytic_initial_azimuth must be exactly true (binding line 31-32)')
    spec = ni.get('composite_grid_spec')
    if present('composite_grid_spec'):
        if not isinstance(spec, dict):
            problems.append('composite_grid_spec must be an object (binding line 31-32, prep line 137-146)')
        else:
            breaks = spec.get('breaks_inverse_kpc')
            orders = spec.get('panel_orders')
            kmax = ni.get('kmax_inverse_kpc')
            if not (isinstance(breaks, list) and breaks and all(_is_finite_number(b) for b in breaks)):
                problems.append('composite_grid_spec.breaks_inverse_kpc must be a non-empty list of finite numbers')
            elif not (isinstance(orders, list) and orders and all(_is_int(n) and n >= 2 for n in orders)):
                problems.append('composite_grid_spec.panel_orders must be a non-empty list of ints >= 2')
            else:
                if len(breaks) != len(orders) + 1:
                    problems.append('composite_grid_spec: len(breaks) must equal len(panel_orders)+1')
                if any(breaks[j + 1] <= breaks[j] for j in range(len(breaks) - 1)):
                    problems.append('composite_grid_spec: breaks must be strictly increasing')
                if _is_finite_number(kmax) and (breaks[0] != -kmax or breaks[-1] != kmax):
                    problems.append('composite_grid_spec: breaks must span exactly [-kmax_inverse_kpc, kmax_inverse_kpc]')
                if [-b for b in reversed(breaks)] != list(breaks) or list(reversed(orders)) != list(orders):
                    problems.append('composite_grid_spec: breaks/orders must have signed reflection symmetry')
                if _is_int(nk):
                    if sum(orders) != nk or nk > 80:
                        problems.append('composite_grid_spec: sum(panel_orders) must equal fourier_points_per_axis <= 80')
                    if spec.get('total_axis_nodes') != nk:
                        problems.append('composite_grid_spec.total_axis_nodes must equal fourier_points_per_axis')
    return (not missing and not problems), missing, problems


def _coordinate_table():
    def entry(name, pointer, units, role, exposed, note, mirrors=None):
        d = {'name': name, 'seed_pointer': pointer, 'units': units, 'role_hint': role, 'exposed': exposed,
             'note': note}
        if mirrors:
            d['mirror_pointers'] = list(mirrors)
        return d
    rows = [
        entry('h2_tail_mass_rtol', '/numerical_inputs/h2_tail_mass_rtol', 'dimensionless', 'numerical', False,
              'NGC-only key; H2 tail mass arithmetic tolerance (worker line 62-64, prep line 81, 239); frozen.'),
        entry('Eref_J', '/numerical_inputs/Eref_J', 'J', 'shared_scale', True,
              'Shared reference energy; prep passes it as fourier_arguments[Eref] (prep line 276); must be > 0.',
              ['/physical/Eref_J']),
        entry('ell_F_m', '/numerical_inputs/ell_F_m', 'm', 'shared_scale', True,
              'Shared register length; fourier_arguments[ell_F] (prep line 276); must be > 0.',
              ['/physical/ell_F_m']),
        entry('gamma', '/numerical_inputs/gamma', 'seed-native (not declared by the worker chain)', 'shared_scale',
              True, 'Shared net gamma; fourier_arguments[gamma] (prep line 276); prep requires finiteness only.',
              ['/physical/gamma']),
        entry('solar_mass_kg', '/numerical_inputs/solar_mass_kg', 'kg', 'numerical', False,
              'Unit conversion constant (prep line 108); frozen.', ['/physical/solar_mass_kg']),
        entry('kpc_m', '/numerical_inputs/kpc_m', 'm', 'numerical', False,
              'Unit conversion constant (prep line 107, binding line 69); frozen.', ['/physical/kpc_m']),
    ]
    numerical = [
        ('kmax_inverse_kpc', 'kpc^-1', 'Fourier cube cutoff (prep line 130); frozen.'),
        ('fourier_points_per_axis', 'count', 'Even Gauss order per axis, <= 80 with a composite grid; frozen.'),
        ('source_gauss_order', 'count', 'Source quadrature order >= 2; frozen.'),
        ('source_azimuth_count', 'count', 'Source azimuth nodes >= 4; frozen.'),
        ('observation_azimuth_count', 'count', 'Observation azimuth nodes >= 4 (binding line 76-77); frozen.'),
        ('pressure_step_kpc', 'kpc', 'Radial pressure stencil, 0 < step < 0.32 kpc (Q01); frozen.'),
        ('azimuth_step_rad', 'rad', 'Azimuth stencil in (0, pi); frozen.'),
        ('hi_search_step_kpc', 'kpc', 'HI free-boundary search step; frozen.'),
        ('hi_search_limit_kpc', 'kpc', 'HI free-boundary search limit; frozen.'),
        ('hi_root_tolerance_kpc', 'kpc', 'HI free-boundary root tolerance; frozen.'),
        ('hi_log_lapse_tolerance', 'as in seed', 'HI column tolerance; frozen.'),
        ('hi_max_metric_calls', 'count', 'HI column metric-call budget; frozen.'),
        ('hi_panels_per_side', 'count', 'HI column panels; frozen.'),
        ('max_iterations', 'count', 'Composite source iteration cap (binding line 55); frozen.'),
        ('relaxation', 'dimensionless', 'Composite source relaxation (binding line 55); frozen.'),
        ('source_atol_J', 'J', 'Source convergence absolute tolerance (binding line 56); frozen.'),
        ('source_rtol', 'dimensionless', 'Source convergence relative tolerance (binding line 56); frozen.'),
        ('pressure_atol_Pa_per_m', 'Pa/m', 'Pressure derivative absolute tolerance >= 0; frozen.'),
        ('pressure_rtol', 'dimensionless', 'Pressure derivative relative tolerance >= 0; frozen.'),
        ('reality_atol', 'as in seed', 'Reality check absolute tolerance (binding line 44); frozen.'),
        ('reality_rtol', 'dimensionless', 'Reality check relative tolerance (binding line 44); frozen.'),
        ('relative_singular_floor', 'dimensionless', 'Fourier solve singular floor (prep line 279); frozen.'),
        ('hermitian_tolerance', 'dimensionless', 'Fourier solve Hermitian tolerance (prep line 280); frozen.'),
        ('solve_rtol', 'dimensionless', 'Fourier residual relative tolerance (prep line 280); frozen.'),
        ('solve_atol', 'as in seed', 'Fourier residual absolute tolerance (prep line 281); frozen.'),
        ('progress_directory', 'path or null', 'Optional progress directory (prep default None); frozen.'),
        ('analytic_initial_azimuth', 'bool', 'Must be exactly true (binding line 31-32); frozen.'),
        ('composite_grid_spec', 'object', 'Composite Gauss panel spec (prep line 137-146); frozen.'),
    ]
    for name, units, note in numerical:
        rows.append(entry(name, '/numerical_inputs/' + name, units, 'numerical', False, note))
    # Nuisances the worker does not read from the seed (no seed field is invented for them).
    rows.append(entry('distance_Mpc', None, 'Mpc', 'nuisance', False,
                      'Not a seed field. Query radii enter in kpc from the target-free manifest (prep line 65-66) '
                      'and the source geometry carries distance_Mpc 13.8 in CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json '
                      '/galaxies/NGC3198/geometry (pinned by the prep at run time). Not applied by read_result either: '
                      'no pinned NGC evaluator defines a distance transform. Not variable without a new prep/binding version.'))
    rows.append(entry('inclination_deg', None, 'deg', 'nuisance', False,
                      'Not a seed field. Hard-coded in the binding: physical_inclination=radians(72), '
                      'released_inclination=radians(73), orientation=+1 (binding line 71-72). Not applied by read_result. '
                      'Not variable without a new binding version.'))
    rows.append(entry('entropy_K', None, 'SI (K_SI)', 'nuisance', False,
                      'Not a seed field. The HI polytropic K follows from sigma0_m_s=11000 and gamma=5/3 hard-coded in the '
                      'prep hi_options (prep line 113); adiabatic_K_transport=True is a diagnostic only (binding line 80). '
                      'Not variable without a new prep version.'))
    return rows


def _shared_15_mapping():
    """11 native ratios + b, Eref, ell_F, gamma_bar (15 coordinates; CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md
    line 53). The 11 native ratios and b live in the frozen native coefficient file the prep pins
    (CODEX1/PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz, fe5a2f06...e53e4f, prep line 19-20, 83-88);
    their individual names are not enumerated in the material read here, so they carry placeholder labels."""
    m = {'native_ratio_%02d' % i: None for i in range(1, 12)}
    m['b'] = None
    m['Eref'] = 'Eref_J'
    m['ell_F'] = 'ell_F_m'
    m['gamma_bar'] = 'gamma'
    return m


# ----------------------------------------------------------------------------------------------------
# public API
# ----------------------------------------------------------------------------------------------------

def exposed_coordinates():
    """Declare which seed fields theta may change. The declaration is bound to the worker, binding, prep
    and manifest bytes; if any of those pins fails from bytes the declaration is refused."""
    reasons = []
    for path, sha, label in ((WORKER_PATH, WORKER_SHA256, 'worker'), (BINDING_PATH, BINDING_SHA256, 'binding'),
                             (PREP_PATH, PREP_SHA256, 'prep'), (MANIFEST_PATH, MANIFEST_SHA256, 'manifest')):
        _verify_pin(path, sha, label, reasons)
    coordinates = _coordinate_table()
    mapping = _shared_15_mapping()
    out = {
        'ok': not reasons,
        'coordinates': coordinates,
        'exposed_names': list(EXPOSED_NAMES),
        'not_variable_without_new_sampler_run': ['b'] + ['native_ratio_%02d' % i for i in range(1, 12)],
        'not_variable_without_new_worker_version': ['distance_Mpc', 'inclination_deg', 'entropy_K',
                                                    'hi_sigma0_m_s (11000, prep line 113)',
                                                    'hi_Gamma (5/3, prep line 113)'],
        'shared_15_mapping': mapping,
        'shared_15_source': 'CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md line 53: exact energy-unit quotient '
                            'leaves 11 native ratios plus b, Eref, ell_F, gamma_bar (15 coordinates) before '
                            'source/allocation nuisances. gamma_bar -> seed gamma is an identification by name '
                            '(prep passes seed gamma as fourier_arguments[gamma] next to Eref and ell_F).',
        'nuisance_handling': 'Distance and inclination are neither seed fields nor reader arguments for NGC43: '
                             'inclination is hard-coded in the binding (72/73 degrees), distance sits in the pinned '
                             'source reference geometry (13.8 Mpc) with manifest radii in kpc. read_result applies '
                             'the identity transform only.',
        'result_transform': RESULT_TRANSFORM,
        'seed_fields_read_by_worker': ['/numerical_inputs (all keys, passed as **prep_arguments)',
                                       '/numerical_inputs/h2_tail_mass_rtol (explicit admission check)',
                                       '/pins (every entry verified from bytes)'],
        'worker': dict(MODULE_INFO['worker']),
        'reasons': reasons,
    }
    return out


def write_seed(*, base_seed_path, base_seed_sha256, theta, out_path):
    """Derive a new seed from a pinned base seed, changing only the exposed fields named in theta.

    Refuses: base pin mismatch, non-NGC43 seed schema, unverifiable seed pins, unknown theta name,
    non-finite / non-positive values, existing out_path, out_path equal to the base, and a derived seed
    the worker would reject (null or invalid required numerical inputs). Nothing is written on refusal.
    The base seed is never modified."""
    reasons = []
    if not isinstance(theta, dict):
        return {'ok': False, 'seed_sha256': None, 'changed_fields': [], 'frozen_field_count': 0,
                'reasons': ['theta must be a dict {coordinate_name: float}']}
    if not isinstance(out_path, str) or not out_path:
        return {'ok': False, 'seed_sha256': None, 'changed_fields': [], 'frozen_field_count': 0,
                'reasons': ['out_path must be a non-empty string']}
    if os.path.lexists(out_path):
        reasons.append('out_path exists; a derived seed is never overwritten: %s' % out_path)
    if isinstance(base_seed_path, str) and os.path.isfile(base_seed_path) and \
            os.path.realpath(out_path) == os.path.realpath(base_seed_path):
        reasons.append('out_path resolves to the base seed; the base is never edited')
    parent = os.path.dirname(os.path.abspath(out_path))
    if not os.path.isdir(parent):
        reasons.append('out_path parent directory does not exist: %s' % parent)
    base_sha = _verify_pin(base_seed_path, base_seed_sha256, 'base seed', reasons)
    if reasons:
        return {'ok': False, 'seed_sha256': None, 'changed_fields': [], 'frozen_field_count': 0, 'reasons': reasons}
    base = _load_json_bytes(base_seed_path, 'base seed', reasons)
    if base is None or not _seed_schema(base, reasons):
        return {'ok': False, 'seed_sha256': None, 'changed_fields': [], 'frozen_field_count': 0, 'reasons': reasons}
    pin_count = _verify_seed_pins(base, reasons)
    # theta validation
    for name, value in theta.items():
        if name not in EXPOSED_NAMES:
            reasons.append('UNKNOWN_COORDINATE %r: exposed names are %s' % (name, list(EXPOSED_NAMES)))
            continue
        if not _is_finite_number(value):
            reasons.append('theta[%r] must be a finite non-bool number' % name)
            continue
        if name in ('Eref_J', 'ell_F_m') and value <= 0:
            reasons.append('theta[%r] must be > 0 (prep line 46-49)' % name)
    if reasons:
        return {'ok': False, 'seed_sha256': None, 'changed_fields': [], 'frozen_field_count': 0, 'reasons': reasons}
    # apply
    new = _deep_copy_json(base)
    changed = []
    for name in sorted(theta):
        value = float(theta[name])
        old = new['numerical_inputs'][name]
        new['numerical_inputs'][name] = value
        changed.append({'pointer': '/numerical_inputs/' + name, 'old': old, 'new': value})
        phys = new.get('physical')
        if isinstance(phys, dict) and name in phys:
            changed.append({'pointer': '/physical/' + name, 'old': phys[name], 'new': value})
            phys[name] = value
    admissible, missing, problems = _admissibility(new)
    if not admissible:
        if missing:
            reasons.append('WORKER_INADMISSIBLE: null required numerical inputs %s' % missing)
        for p in problems:
            reasons.append('WORKER_INADMISSIBLE: ' + p)
        return {'ok': False, 'seed_sha256': None, 'changed_fields': changed, 'frozen_field_count': 0,
                'worker_admissible': False, 'missing_inputs': missing, 'reasons': reasons}
    try:
        text = _canonical(new)
    except ValueError as exc:
        return {'ok': False, 'seed_sha256': None, 'changed_fields': changed, 'frozen_field_count': 0,
                'reasons': ['derived seed is not canonical-JSON serializable: %s' % exc]}
    try:
        with open(out_path, 'x', encoding='utf-8') as f:
            f.write(text)
            f.flush()
    except OSError as exc:
        return {'ok': False, 'seed_sha256': None, 'changed_fields': changed, 'frozen_field_count': 0,
                'reasons': ['could not create out_path exclusively: %s (%s)' % (out_path, exc)]}
    seed_sha = _sha256_file(out_path)
    written = _load_json_bytes(out_path, 'written seed', reasons)
    if written is None or _canonical(written) != text:
        reasons.append('written seed does not round-trip; refuse')
        return {'ok': False, 'seed_sha256': seed_sha, 'changed_fields': changed, 'frozen_field_count': 0,
                'reasons': reasons}
    return {'ok': True, 'seed_sha256': seed_sha, 'changed_fields': changed,
            'frozen_field_count': _leaf_count(base) - len(changed), 'out_path': out_path,
            'base_seed_sha256': base_sha, 'seed_pins_verified': pin_count, 'worker_admissible': True,
            'missing_inputs': [], 'format': 'canonical JSON (sort_keys, compact separators, no NaN)',
            'reasons': []}


def read_result(*, outdir, region_path, region_sha256):
    """Read <outdir>/result.json written by the NGC43 worker and return the 43 speeds keyed by query id
    in manifest order. region_path is the target-free query manifest (its pinned V001 bytes).

    Forward-style result: {ok, speeds_km_s, valid, reasons, provenance}. valid is True only if finish.json
    reports RETURNED_ACTUAL_RESULT with result_sha256 equal to the bytes of result.json, start.json carries
    the pinned worker hash, result.json has the bound layout, predictions_available is true, the 43 rows
    carry exactly the manifest ids in manifest order and every speed is a finite float."""
    reasons = []
    provenance = {'transform': 'identity', 'transform_detail': RESULT_TRANSFORM, 'manifest_sha256': None,
                  'result_path': None, 'result_sha256': None, 'finish_sha256': None, 'start_sha256': None,
                  'seed_pin': None, 'worker_pin': None, 'accepted_for_calibration': None}
    binding = _load_pinned_manifest(region_path, region_sha256, reasons)
    if binding is None:
        return {'ok': False, 'speeds_km_s': {}, 'valid': False, 'reasons': reasons, 'provenance': provenance}
    provenance['manifest_sha256'] = MANIFEST_SHA256
    if not isinstance(outdir, str) or not os.path.isdir(outdir):
        reasons.append('outdir is not a directory: %r' % (outdir,))
        return {'ok': False, 'speeds_km_s': {}, 'valid': False, 'reasons': reasons, 'provenance': provenance}
    ids = [b['query_id'] for b in binding]
    result_path = os.path.join(outdir, 'result.json')
    finish_path = os.path.join(outdir, 'finish.json')
    start_path = os.path.join(outdir, 'start.json')
    failure_path = os.path.join(outdir, 'failure.json')
    provenance['result_path'] = result_path
    if os.path.isfile(failure_path):
        fail = _load_json_bytes(failure_path, 'failure.json', reasons)
        if isinstance(fail, dict):
            reasons.append('WORKER_FAILURE: %s: %s' % (fail.get('type'), fail.get('message')))
        else:
            reasons.append('WORKER_FAILURE: failure.json present')
    if not os.path.isfile(result_path):
        reasons.append('RESULT_MISSING: %s' % result_path)
        return {'ok': True, 'speeds_km_s': {}, 'valid': False, 'reasons': reasons, 'provenance': provenance}
    try:
        result_sha = _sha256_file(result_path)
    except OSError as exc:
        reasons.append('result.json unreadable: %s' % exc)
        return {'ok': True, 'speeds_km_s': {}, 'valid': False, 'reasons': reasons, 'provenance': provenance}
    provenance['result_sha256'] = result_sha
    # finish.json: written by the worker only after result.json; carries the result hash.
    if not os.path.isfile(finish_path):
        reasons.append('FINISH_JSON_MISSING: worker did not record completion')
    else:
        try:
            provenance['finish_sha256'] = _sha256_file(finish_path)
        except OSError as exc:
            reasons.append('finish.json unreadable: %s' % exc)
        fin = _load_json_bytes(finish_path, 'finish.json', reasons)
        if isinstance(fin, dict):
            if fin.get('status') != 'RETURNED_ACTUAL_RESULT':
                reasons.append('finish.json status is %r, not RETURNED_ACTUAL_RESULT' % (fin.get('status'),))
            if fin.get('result_sha256') != result_sha:
                reasons.append('finish.json result_sha256 %r differs from result.json bytes %s'
                               % (fin.get('result_sha256'), result_sha))
        elif fin is not None:
            reasons.append('finish.json is not an object')
    # start.json: carries the worker's own hash; the result must come from the pinned worker bytes.
    if not os.path.isfile(start_path):
        reasons.append('START_JSON_MISSING: worker start record absent')
    else:
        try:
            provenance['start_sha256'] = _sha256_file(start_path)
        except OSError as exc:
            reasons.append('start.json unreadable: %s' % exc)
        st = _load_json_bytes(start_path, 'start.json', reasons)
        if isinstance(st, dict):
            provenance['worker_pin'] = st.get('worker_pin') if isinstance(st.get('worker_pin'), str) else None
            if st.get('worker_pin') != WORKER_SHA256:
                reasons.append('start.json worker_pin %r is not the pinned NGC43 worker %s'
                               % (st.get('worker_pin'), WORKER_SHA256))
        elif st is not None:
            reasons.append('start.json is not an object')
    top = _load_json_bytes(result_path, 'result.json', reasons)
    speeds = {}
    if top is not None:
        if not isinstance(top, dict) or not isinstance(top.get('result'), dict):
            reasons.append('result.json: /result is not an object (worker line 101)')
        else:
            if isinstance(top.get('seed_pin'), str):
                provenance['seed_pin'] = top['seed_pin']
            else:
                reasons.append('result.json: /seed_pin missing or not a string')
            if isinstance(top.get('accepted_for_calibration'), bool):
                provenance['accepted_for_calibration'] = top['accepted_for_calibration']
            if top.get('accepted_for_calibration') is not False:
                reasons.append('result.json: /accepted_for_calibration is not false (worker line 102)')
            pred = top['result'].get('result')
            if not isinstance(pred, dict):
                reasons.append('result.json: /result/result is not an object (binding line 83)')
            else:
                if pred.get('predictions_available') is not True:
                    reasons.append('PREDICTIONS_NOT_AVAILABLE: %s' % (pred.get('reason') or 'predictions_available is not true'))
                if pred.get('units') != 'km/s':
                    reasons.append('result.json: /result/result/units is %r, not km/s' % (pred.get('units'),))
                rows = pred.get('rows')
                if not isinstance(rows, list):
                    reasons.append('result.json: /result/result/rows is not a list')
                else:
                    if len(rows) != QUERY_COUNT:
                        reasons.append('ROW_COUNT %d != %d' % (len(rows), QUERY_COUNT))
                    seen = []
                    for i, row in enumerate(rows):
                        if not isinstance(row, dict) or set(row) != {'id', 'speed_km_s'}:
                            reasons.append('row %d is not {id, speed_km_s}' % i)
                            continue
                        rid = row['id']
                        seen.append(rid)
                        if i < QUERY_COUNT and rid != ids[i]:
                            reasons.append('ORDER: row %d id %r is not manifest id %r' % (i, rid, ids[i]))
                        v = row['speed_km_s']
                        if rid not in ids:
                            reasons.append('UNKNOWN_ID %r at row %d' % (rid, i))
                        elif not _is_finite_number(v):
                            reasons.append('NONFINITE_SPEED for %r at row %d: %r' % (rid, i, v))
                        elif rid in speeds:
                            reasons.append('DUPLICATE_ID %r at row %d' % (rid, i))
                        else:
                            speeds[rid] = float(v)
                    for rid in ids:
                        if rid not in seen:
                            reasons.append('MISSING_ID %r' % rid)
    ordered = {rid: speeds[rid] for rid in ids if rid in speeds}
    valid = not reasons and len(ordered) == QUERY_COUNT
    return {'ok': True, 'speeds_km_s': ordered, 'valid': valid, 'reasons': reasons, 'provenance': provenance}


def check_query_binding(*, manifest_path, manifest_sha256):
    """Verify the target-free manifest from bytes and bind worker row index <-> query id by radius text.

    The prep builds queries = [{id: row.query_id, radius_kpc: float(row.Rad_text)} for row in manifest.rows]
    (prep line 65-66); the prediction module emits rows in that order with rows[i].id = queries[i].id
    (prediction v005 line 210, 221). So worker_index i <-> manifest rows[i] <-> query_id NGC3198-Q(i+1)."""
    reasons = []
    actual = _verify_pin(manifest_path, manifest_sha256, 'manifest', reasons)
    if actual is None:
        return {'ok': False, 'query_ids': [], 'binding': [], 'reasons': reasons}
    m = _load_json_bytes(manifest_path, 'manifest', reasons)
    binding = _check_manifest_object(m, reasons) if m is not None else None
    if binding is None or reasons:
        return {'ok': False, 'query_ids': [], 'binding': [], 'reasons': reasons}
    return {'ok': True,
            'query_ids': [b['query_id'] for b in binding],
            'binding': binding,
            'manifest_sha256': actual,
            'matches_pinned_v001': actual == MANIFEST_SHA256,
            'rad_unit': 'kpc',
            'worker_binding_basis': 'prep line 65-66 builds queries in manifest row order with radius_kpc=float(Rad_text); '
                                    'prediction v005 line 210/221 emits rows[i]={id: queries[i].id, speed_km_s} in the '
                                    'same order; binding line 74-75 requires exactly 43 queries.',
            'no_velocity_read': True,
            'reasons': []}


def make_theta_to_seed(*, base_seed_path, base_seed_sha256):
    """Bind a base seed (pin verified from bytes, schema and worker admissibility checked) and return
    theta_to_seed(theta, out_path) -> write_seed result. A base the worker would reject yields ok=False."""
    reasons = []
    if _verify_pin(base_seed_path, base_seed_sha256, 'base seed', reasons) is None:
        return {'ok': False, 'theta_to_seed': None, 'reasons': reasons}
    base = _load_json_bytes(base_seed_path, 'base seed', reasons)
    if base is None or not _seed_schema(base, reasons):
        return {'ok': False, 'theta_to_seed': None, 'reasons': reasons}
    _verify_seed_pins(base, reasons)
    admissible, missing, problems = _admissibility(base)
    if not admissible:
        if missing:
            reasons.append('WORKER_INADMISSIBLE base: null required numerical inputs %s' % missing)
        reasons.extend('WORKER_INADMISSIBLE base: ' + p for p in problems)
    if reasons:
        return {'ok': False, 'theta_to_seed': None, 'missing_inputs': missing, 'reasons': reasons}
    path = base_seed_path
    sha = base_seed_sha256

    def theta_to_seed(theta=None, out_path=None, **kw):
        if theta is None and 'theta' in kw:
            theta = kw['theta']
        if out_path is None and 'out_path' in kw:
            out_path = kw['out_path']
        return write_seed(base_seed_path=path, base_seed_sha256=sha, theta=theta, out_path=out_path)

    return {'ok': True, 'theta_to_seed': theta_to_seed, 'base_seed_path': path, 'base_seed_sha256': sha,
            'exposed_names': list(EXPOSED_NAMES), 'reasons': []}


def make_result_reader(*, region_path, region_sha256):
    """Bind the target-free manifest (pin verified from bytes, must be the pinned V001 bytes) and return
    result_reader(outdir) -> forward-style result."""
    reasons = []
    binding = _load_pinned_manifest(region_path, region_sha256, reasons)
    if binding is None:
        return {'ok': False, 'result_reader': None, 'reasons': reasons}
    path = region_path
    sha = region_sha256

    def result_reader(outdir=None, **kw):
        if outdir is None and 'outdir' in kw:
            outdir = kw['outdir']
        return read_result(outdir=outdir, region_path=path, region_sha256=sha)

    return {'ok': True, 'result_reader': result_reader, 'query_ids': [b['query_id'] for b in binding],
            'region_sha256': sha, 'transform': RESULT_TRANSFORM, 'reasons': []}


def seed_admissibility(*, seed_path, seed_sha256):
    """Read-only report: does this seed have the NGC43 schema, do its pins verify from bytes, and would the
    worker/binding/prep admission checks pass? Addition beyond the six interface functions."""
    reasons = []
    actual = _verify_pin(seed_path, seed_sha256, 'seed', reasons)
    if actual is None:
        return {'ok': False, 'worker_admissible': False, 'missing_inputs': [], 'problems': [],
                'pins_verified': 0, 'pin_count': 0, 'reasons': reasons}
    seed = _load_json_bytes(seed_path, 'seed', reasons)
    if seed is None or not _seed_schema(seed, reasons):
        return {'ok': False, 'worker_admissible': False, 'missing_inputs': [], 'problems': [],
                'pins_verified': 0, 'pin_count': 0, 'reasons': reasons}
    pin_reasons = []
    verified = _verify_seed_pins(seed, pin_reasons)
    admissible, missing, problems = _admissibility(seed)
    return {'ok': True, 'seed_sha256': actual, 'schema_ok': True,
            'worker_admissible': admissible and not pin_reasons,
            'missing_inputs': missing, 'problems': problems,
            'pins_verified': verified, 'pin_count': len(seed['pins']), 'pin_failures': pin_reasons,
            'exposed_values': {k: seed['numerical_inputs'].get(k) for k in EXPOSED_NAMES},
            'status': seed.get('status'), 'reasons': []}
