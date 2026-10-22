"""DDO154 forward adapter, Module A of INTERFACE_0463_V001 (dispatch 0463, Claude3 lane).

Maps a calibration point ``theta`` onto a NEW seed file for the reviewed root
worker ``helpers/recovered_packet_audit/ddo_composite_stable_cached_root_worker_v002.py``
(SHA256 c4cb6826...95a4) and reads a finished worker output directory back into
the forward-style result consumed by the 0462 engine, using exactly the transform
of the pinned evaluator ``helpers/coefficient_method/owned_ddo12_forward_region_evaluator_v001.py``
(SHA256 1784e872...fd0c, lines 35-61) plus the pinned objective
``helpers/response_packet_audit/ddo154_finite_observation_region_objective_v001.py``
(SHA256 c5eac0f5...511b, lines 40-48) that produced
``CODEX1/DDO154_FIRST_CONDITIONAL_CALIBRATION_EVALUATION_RUN_V001/comparison/comparison.json``.

Conventions (INTERFACE_0463_V001 / INTERFACE_0462_V001): inert at import (no I/O,
no computation), keyword-only arguments with no defaults, every public function
returns a dict with ``ok`` and ``reasons`` and fails closed, standard library only
(numpy is not needed, so no numpy object can escape), file pins are SHA256 over
bytes verified before use. Nothing here launches a worker, reads any NGC3198
file, uses the network, deletes anything or overwrites an existing file.

Public API (exactly INTERFACE_0463_V001, Module A):
    exposed_coordinates()
    write_seed(*, base_seed_path, base_seed_sha256, theta, out_path)
    read_result(*, outdir, region_path, region_sha256)
    reproduce_comparison(*, result_json_path, comparison_json_path, region_path, region_sha256)
    make_theta_to_seed(*, base_seed_path, base_seed_sha256)
    make_result_reader(*, region_path, region_sha256)
"""
import copy
import hashlib
import json
import math
import os
import struct

__all__ = ['exposed_coordinates', 'write_seed', 'read_result', 'reproduce_comparison',
           'make_theta_to_seed', 'make_result_reader']

ADAPTER_NAME = 'ddo154_forward_adapter_c3v001'
TRANSFORM_NAME = 'DDO12_PINNED_EVALUATOR_PASSTHROUGH_V001'

ROOT = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'

# Documented sources of the transform and of the seed semantics. These are CITED
# (path, pin, lines) for provenance; this module never loads or executes them.
WORKER = {'path': ROOT + '/helpers/recovered_packet_audit/ddo_composite_stable_cached_root_worker_v002.py',
          'sha256': 'c4cb682669993afbad3c623a010244cc8a31b9fcbacfe44e6bc692bf2d5895a4'}
EVALUATOR = {'path': ROOT + '/helpers/coefficient_method/owned_ddo12_forward_region_evaluator_v001.py',
             'sha256': '1784e87239a58ab013f27090c71c30ddb9e15e5f7380d630b7f573677e4fbd0c',
             'lines': '23-27 (pointer walk), 35-61 (validation and mapping checks), 65-68 (objective call)'}
OBJECTIVE = {'path': ROOT + '/helpers/response_packet_audit/ddo154_finite_observation_region_objective_v001.py',
             'sha256': 'c5eac0f5d019cd861c708f8bd4f63c96d0579757afd29df0653f25161758511b',
             'lines': "12 (IDS), 28-32 (exact ids), 42 (v=float(q['speed_km_s'])), 48 (predicted_catalogue_speed_km_s=v)"}
BINDING = {'path': ROOT + '/helpers/recovered_packet_audit/ddo_composite_stable_cached_binding_v002.py',
           'sha256': 'd81b24b7150c846a5b70c82a8668daaaef53335ced062763980a33cdbc90b6d5',
           'lines': '34 (prepare_inputs(**numerical_inputs)), 104-105 (equal-angle azimuth nodes), 112 (physical 66 deg / released 64 deg hardcoded)'}
PREP = {'path': ROOT + '/helpers/coefficient_method/ddo_actual_initial_source_preparation_v007.py',
        'sha256': 'ac905597b1aa06da3a0178bfa629f6256b78cc87e8b1b05fcea22b3f6df25a42',
        'lines': '36-44 (signature = seed numerical_inputs), 46-49 (positivity), 66-68 (query radii from pinned calibration input), 73-76 (frozen native coefficients), 101 (HI sigma0=11000 m/s, Gamma=5/3 hardcoded), 221 (Eref, ell_F, gamma into Fourier arguments)'}
COEFFICIENT_FREEZE = {'path': ROOT + '/CODEX1/PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz',
                      'sha256': 'fe5a2f065dec8f120c573eeeb6edc0a24a945d2a0fd70e3f29a66cb986e53e4f',
                      'note': 'Frozen native response point (source_hessian_grid, background_mu, background_M, background_C); provisional point from sampler run V004 with failed joint mixing. The 11 native ratios and b are inside this frozen point, not in the seed.'}
COMPARISON_RUN = ROOT + '/CODEX1/DDO154_FIRST_CONDITIONAL_CALIBRATION_EVALUATION_RUN_V001'
REFERENCE_RESULT_SHA256 = '79855e78bc1702b286828f6e7cf123d3e654509a08b395ced40cdbef06b453e0'
REFERENCE_COMPARISON_SHA256 = '0424798dc5d50f1464921831122c6b75cddac1f3934522df225cbc3096681bd1'

# Evaluator mapping constants, exactly as recorded in the comparison run's
# launch.json / receipt.json command line and in comparison.json
# /comparison/forward_mapping_provenance. They are CHECKS in the pinned
# evaluator (radius/distance mapping, physical LOS factor, released harmonic
# deprojection), never applied as rescalings; D=4.04 Mpc gives factor 1.
PREDICTION_POINTER = '/result/result'
DISTANCE_MPC = 4.04
RADIUS_REFERENCE_MPC = 4.04
KPC_M = 3.085677581491367e19
PHYSICAL_INCLINATION_RAD = 1.1519173063162575   # == math.radians(66), binding line 112
RELEASED_INCLINATION_RAD = 1.117010721276371    # == math.radians(64), binding line 112
MAPPING_RELATIVE_TOLERANCE = 1e-12
MAPPING_ABSOLUTE_TOLERANCE = 1e-12
ROW_IDS = tuple('DDO154_SPARC12_%02d' % i for i in range(1, 13))   # objective line 12

# ---------------------------------------------------------------------------
# Seed coordinate declarations (what the seed exposes and what it does not).
# ---------------------------------------------------------------------------
_EXPOSED = (
    {'name': 'Eref_J', 'seed_pointer': '/numerical_inputs/Eref_J', 'units': 'J',
     'role_hint': 'shared_scale', 'exposed': True,
     'note': 'Common positive energy scale E_ref. Worker: seed numerical_inputs -> prep prepare_inputs(Eref_J) -> fourier_arguments Eref (prep line 221) and checkpoint caller identity physical_parameters. Must be finite and > 0 (prep line 46-49). Mirror annotation /physical/Eref_J (not read by the worker) is updated by write_seed and listed in changed_fields.'},
    {'name': 'ell_F_m', 'seed_pointer': '/numerical_inputs/ell_F_m', 'units': 'm',
     'role_hint': 'shared_scale', 'exposed': True,
     'note': 'Common positive length scale ell_F. Worker: seed numerical_inputs -> prep prepare_inputs(ell_F_m) -> fourier_arguments ell_F (prep line 221). Must be finite and > 0. Mirror annotation /physical/ell_F_m updated by write_seed.'},
    {'name': 'gamma', 'seed_pointer': '/numerical_inputs/gamma', 'units': 'dimensionless',
     'role_hint': 'shared_scale', 'exposed': True,
     'note': 'Net gamma coupling (dispatch 0463: native/EH ratio; Gamma_total = gamma*I_R + Gamma_native + Gamma_b, GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15 line 51). Worker: seed numerical_inputs -> prep prepare_inputs(gamma) -> fourier_arguments gamma (prep line 221). Prep requires finite only (sign unconstrained, prep line 49). NOT the HI adiabatic index (that is Gamma=5/3, hardcoded in prep line 101). Mirror annotation /physical/gamma updated by write_seed.'},
)
_MIRROR_POINTERS = {'Eref_J': ['/physical/Eref_J'], 'ell_F_m': ['/physical/ell_F_m'], 'gamma': ['/physical/gamma']}

_UNIT_CONSTANTS = (
    {'name': 'solar_mass_kg', 'seed_pointer': '/numerical_inputs/solar_mass_kg', 'units': 'kg', 'role_hint': 'numerical', 'exposed': False,
     'note': 'Unit constant for surface densities (prep lines 95-96); part of the checkpoint physical identity. Frozen; not a calibration coordinate. Mirror /physical/solar_mass_kg.'},
    {'name': 'kpc_m', 'seed_pointer': '/numerical_inputs/kpc_m', 'units': 'm', 'role_hint': 'numerical', 'exposed': False,
     'note': 'Unit constant kpc in metres; sets query radius_m = radius_reference_kpc*kpc_m (prep). The evaluator radius check uses the same constant 3.085677581491367e19. Frozen. Mirror /physical/kpc_m.'},
)

_NUMERICAL_CONTROLS = (
    ('fourier_points_per_axis', '1'), ('source_gauss_order', '1'), ('source_azimuth_count', '1'),
    ('observation_azimuth_count', '1'), ('hi_max_metric_calls', '1'), ('hi_panels_per_side', '1'),
    ('max_iterations', '1'), ('kmax_inverse_kpc', '1/kpc'), ('pressure_step_kpc', 'kpc'),
    ('azimuth_step_rad', 'rad'), ('hi_search_step_kpc', 'kpc'), ('hi_search_limit_kpc', 'kpc'),
    ('hi_root_tolerance_kpc', 'kpc'), ('hi_log_lapse_tolerance', '1'), ('relaxation', '1'),
    ('source_atol_J', 'J'), ('source_rtol', '1'), ('pressure_atol_Pa_per_m', 'Pa/m'), ('pressure_rtol', '1'),
    ('reality_atol', '1'), ('reality_rtol', '1'), ('relative_singular_floor', '1'), ('hermitian_tolerance', '1'),
    ('solve_rtol', '1'), ('solve_atol', '1'), ('progress_directory', 'path or null'),
    ('analytic_initial_azimuth', 'bool'), ('composite_grid_spec', 'dict'),
)

_NUISANCES = (
    {'name': 'distance_Mpc', 'seed_pointer': None, 'units': 'Mpc', 'role_hint': 'nuisance', 'exposed': False,
     'note': 'No seed field. Query radii are radius_reference_kpc*kpc_m from the pinned calibration input (prep lines 66-68), i.e. the D=4.04 Mpc catalogue radii. The pinned evaluator only CHECKS radius_m == reference_radius_kpc*(D/4.04)*kpc_m with D=4.04 (factor 1); it never rescales. Varying D needs a new query roster (new prep/binding), so it is not variable through this worker, seed or result transform. read_result uses the fixed documented value 4.04.'},
    {'name': 'physical_inclination_rad', 'seed_pointer': None, 'units': 'rad', 'role_hint': 'nuisance', 'exposed': False,
     'note': 'No seed field. Hardcoded math.radians(66) in binding line 112 (worker-side projection los_km_s = v/1000*sin(i_phys)*cos(phi)). The pinned evaluator only CHECKS this with 1.1519173063162575; read_result applies the same check.'},
    {'name': 'released_inclination_rad', 'seed_pointer': None, 'units': 'rad', 'role_hint': 'nuisance', 'exposed': False,
     'note': 'No seed field. Hardcoded math.radians(64) in binding line 112 (worker-side harmonic deprojection giving rows[i].speed_km_s). The pinned evaluator only CHECKS that the weighted harmonic estimate with basis sin(1.117010721276371)*cos(phi) reproduces speed_km_s within 1e-12; it does not recompute the catalogue speed with a different inclination. Not variable without a new binding.'},
    {'name': 'hi_sigma0_m_s', 'seed_pointer': None, 'units': 'm/s', 'role_hint': 'nuisance', 'exposed': False,
     'note': 'Entropy/thermal preparation (K = sigma0^2*rho(0)^(1-Gamma), GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003 static_profile). Hardcoded 11000 m/s in prep line 101; no seed field. Counted preparation choice; not variable without a new prep module.'},
    {'name': 'hi_adiabatic_index', 'seed_pointer': None, 'units': 'dimensionless', 'role_hint': 'nuisance', 'exposed': False,
     'note': 'HI polytropic Gamma = 5/3 hardcoded in prep line 101; no seed field. Distinct from the exposed coupling named gamma.'},
)

_SEED_ANNOTATIONS = (
    {'name': 'scale_seed', 'seed_pointer': '/scale_seed', 'units': 'dimensionless', 'role_hint': 'numerical', 'exposed': False,
     'note': 'Annotation only (seed_method). Not read by the worker (reads numerical_inputs and pins only), the binding or prep. Frozen and copied unchanged.'},
)

# The 15 shared coordinates after the energy quotient (GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md
# line 53: "11 native ratios plus b, Eref, ell_F, gamma_bar (15 coordinates) before source/allocation
# nuisances"). The 12 uniform-energy coordinates are named in
# CODEX1/READINESS_C178_SHARED_CALIBRATION_EXTENSION_V002.json /current_uniform_energy_coordinates
# (Ud, mu0, lambda_J, lambda_R, r, delta_cell, nu, h, t, g, abs(kappa), abs(epsilon_B)); the quotient by
# one energy unit leaves 11 ratios, written here relative to Ud following the *_over_Ud convention of
# CODEX1/GALAXY_RAW_ENERGY_COORDINATE_LIFT_ADOPTION_V001.json. b = beta_native*Ud
# (GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json, "No value chosen here").
_NATIVE_RATIO_NAMES = ('mu0/Ud', 'lambda_J/Ud', 'lambda_R/Ud', 'r/Ud', 'delta_cell/Ud', 'nu/Ud',
                       'h/Ud', 't/Ud', 'g/Ud', 'abs(kappa)/Ud', 'abs(epsilon_B)/Ud')
_NOT_VARIABLE_WITHOUT_NEW_SAMPLER_RUN = _NATIVE_RATIO_NAMES + ('b',)
_SHARED_15_MAPPING = tuple([(n, None) for n in _NATIVE_RATIO_NAMES] +
                           [('b', None), ('Eref', 'Eref_J'), ('ell_F', 'ell_F_m'), ('gamma_bar', 'gamma')])

_FROZEN_TOP_LEVEL = ('/status', '/seed_method', '/physical', '/pins', '/scope', '/parent_seed',
                     '/quadrature_selection_evidence', '/scale_seed')
_REQUIRED_SEED_KEYS = ('numerical_inputs', 'pins', 'physical')


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def _read_bytes(path):
    with open(path, 'rb') as f:
        return f.read()


def _is_hex64(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdefABCDEF' for c in s)


def _path_arg(value, label, reasons):
    try:
        p = os.fspath(value)
    except TypeError:
        reasons.append('%s must be a path string, got %s' % (label, type(value).__name__))
        return None
    if isinstance(p, bytes):
        p = p.decode('utf-8', 'surrogateescape')
    if not isinstance(p, str) or not p:
        reasons.append('%s must be a non-empty path string' % label)
        return None
    return p


def _pin_arg(value, label, reasons):
    if not _is_hex64(value):
        reasons.append('%s must be a 64-hex SHA256 string' % label)
        return None
    return value.lower()


def _load_pinned_json(path, expected_sha256, label, reasons):
    """Read bytes, verify SHA256 BEFORE parsing, then parse. Returns (obj, actual_sha) or (None, actual_sha|None)."""
    try:
        raw = _read_bytes(path)
    except OSError as exc:
        reasons.append('%s unreadable: %s: %s' % (label, type(exc).__name__, exc))
        return None, None
    actual = _sha256_bytes(raw)
    if actual != expected_sha256:
        reasons.append('%s pin mismatch: expected %s, actual %s' % (label, expected_sha256, actual))
        return None, actual
    try:
        obj = json.loads(raw)
    except ValueError as exc:
        reasons.append('%s is not valid JSON: %s' % (label, exc))
        return None, actual
    return obj, actual


def _walk_pointer(obj, pointer):
    """RFC6901-style walk exactly as the evaluator does (lines 24-27)."""
    if not isinstance(pointer, str) or not pointer.startswith('/'):
        raise ValueError('Explicit JSON pointer required')
    cur = obj
    for key in pointer[1:].split('/'):
        key = key.replace('~1', '/').replace('~0', '~')
        cur = cur[int(key)] if isinstance(cur, list) else cur[key]
    return cur


def _get_pointer(obj, pointer):
    cur = obj
    for key in pointer[1:].split('/'):
        key = key.replace('~1', '/').replace('~0', '~')
        cur = cur[int(key)] if isinstance(cur, list) else cur[key]
    return cur


def _set_pointer(obj, pointer, value):
    parts = [k.replace('~1', '/').replace('~0', '~') for k in pointer[1:].split('/')]
    cur = obj
    for key in parts[:-1]:
        cur = cur[int(key)] if isinstance(cur, list) else cur[key]
    last = parts[-1]
    if isinstance(cur, list):
        cur[int(last)] = value
    else:
        if last not in cur:
            raise KeyError('pointer target absent: ' + pointer)
        cur[last] = value


def _leaf_count(obj):
    if isinstance(obj, dict):
        return sum(_leaf_count(v) for v in obj.values()) if obj else 1
    if isinstance(obj, list):
        return sum(_leaf_count(v) for v in obj) if obj else 1
    return 1


def _region_rows(region, reasons):
    """Bind the region rows the way the evaluator/objective do; return list of {id, reference_radius_kpc} or None."""
    if not isinstance(region, dict) or not isinstance(region.get('rows'), list):
        reasons.append('region file lacks a rows list')
        return None
    rows = region['rows']
    try:
        ids = [r['id'] for r in rows]
        out = [{'id': str(r['id']), 'reference_radius_kpc': float(r['reference_radius_kpc'])} for r in rows]
    except (KeyError, TypeError, ValueError) as exc:
        reasons.append('region rows malformed: %s: %s' % (type(exc).__name__, exc))
        return None
    if len(rows) != 12 or tuple(ids) != ROW_IDS:
        reasons.append('Exact frozen DDO154 twelve-row order required (objective line 28)')
        return None
    if any(not math.isfinite(r['reference_radius_kpc']) or r['reference_radius_kpc'] <= 0 for r in out):
        reasons.append('region reference radii must be finite and positive')
        return None
    return out


def _close(x, y):
    # evaluator line 44
    return (math.isfinite(x) and math.isfinite(y) and
            abs(x - y) <= MAPPING_ABSOLUTE_TOLERANCE + MAPPING_RELATIVE_TOLERANCE * max(abs(x), abs(y)))


def _transform(pred, region_rows):
    """Exact re-statement of evaluator lines 35-61 and objective lines 28-48 on the payload at
    PREDICTION_POINTER. Returns a dict with status, valid, reasons, speeds (id -> float, region order),
    mapping_checks and the per-row provenance. Never raises on anticipated bad payloads."""
    out = {'status': None, 'valid': False, 'reasons': [], 'speeds': {}, 'mapping_checks': [],
           'dynamics_status': None, 'predictions_available_semantics': None, 'node_counts': []}
    r = out['reasons']
    if not isinstance(pred, dict):
        out['status'] = 'INPUT_OR_FORWARD_VALIDATION_FAILED_NO_SCORE'
        r.append('prediction payload at %s is not an object' % PREDICTION_POINTER)
        return out
    out['dynamics_status'] = pred.get('dynamics_status')
    out['predictions_available_semantics'] = pred.get('predictions_available_semantics')
    sfp = pred.get('source_fixed_point', {})
    converged = sfp.get('converged_finite_fixed_point') if isinstance(sfp, dict) else None
    # evaluator line 35-36
    if pred.get('predictions_available') is not True or converged is not True:
        out['status'] = 'FORWARD_UNAVAILABLE_NO_SCORE'
        r.append('FORWARD_UNAVAILABLE_NO_SCORE: predictions_available=%r converged_finite_fixed_point=%r reason=%r dynamics_status=%r'
                 % (pred.get('predictions_available'), converged, pred.get('reason'), pred.get('dynamics_status')))
        return out
    try:
        # evaluator line 37
        if pred.get('semantics') != 'TOTAL_OBSERVABLE' or pred.get('units') != 'km/s' or pred.get('inclination_applied_once') is not True:
            raise ValueError('Actual total observable km/s once-projected output required')
        ids = [row['id'] for row in region_rows]
        rows = pred['rows']
        details = pred['query_physics']
        # evaluator line 43
        if [row['id'] for row in rows] != ids or [d['id'] for d in details] != ids:
            raise ValueError('Exact12 ordered query identities required')
        speeds = {}
        for obs, row, d in zip(region_rows, rows, details):
            # evaluator line 47-48
            expected = obs['reference_radius_kpc'] * (DISTANCE_MPC / 4.04) * KPC_M
            if not _close(float(d['radius_m']), expected):
                raise ValueError('Radius/distance mapping mismatch: ' + obs['id'])
            nodes = d['nodes']
            weights = d['normalized_estimator_weights']
            # evaluator line 50
            if not nodes or len(nodes) != len(weights) or not _close(math.fsum(weights), 1.):
                raise ValueError('Actual normalized angular estimator weights required')
            numerator = []
            denominator = []
            for node, w in zip(nodes, weights):
                if not math.isfinite(w) or w < 0:
                    raise ValueError('Invalid actual estimator weight')
                phi = float(node['phi_rad'])
                v = float(node['v'])
                los = float(node['los_km_s'])
                expected_los = v / 1000 * math.sin(PHYSICAL_INCLINATION_RAD) * math.cos(phi)
                if not _close(los, expected_los):
                    raise ValueError('Physical inclination/velocity units mismatch')
                basis = math.sin(RELEASED_INCLINATION_RAD) * math.cos(phi)
                numerator.append(w * basis * los)
                denominator.append(w * basis * basis)
            den = math.fsum(denominator)
            # evaluator line 61
            if den <= 0 or not _close(float(row['speed_km_s']), math.fsum(numerator) / den):
                raise ValueError('Reference deprojection/harmonic mismatch')
            out['mapping_checks'].append({'id': obs['id'], 'actual_radius_m': d['radius_m'], 'expected_radius_m': expected})
            out['node_counts'].append(len(nodes))
            # objective line 42 / 48: the catalogue speed is the worker row speed, unchanged
            v_cat = float(row['speed_km_s'])
            if not math.isfinite(v_cat):
                raise ValueError('Invalid finite row or uncertainty')
            speeds[obs['id']] = v_cat
        if len(speeds) != 12:
            raise ValueError('Exactly one prediction for every authorized DDO row required')
    except Exception as exc:  # anticipated bad payload -> fail closed, no raise
        out['status'] = 'INPUT_OR_FORWARD_VALIDATION_FAILED_NO_SCORE'
        r.append('INPUT_OR_FORWARD_VALIDATION_FAILED_NO_SCORE: %s: %s' % (type(exc).__name__, exc))
        out['speeds'] = {}
        return out
    out['status'] = 'CONDITIONAL_TRIAL_COMPARISON_NOT_ADMITTED'
    out['valid'] = True
    out['speeds'] = speeds
    return out


def _transform_description():
    return {
        'name': TRANSFORM_NAME,
        'prediction_pointer': PREDICTION_POINTER,
        'catalogue_speed_definition': "predicted_catalogue_speed_km_s[id] = float(payload['rows'][i]['speed_km_s']) with payload = result.json at /result/result, after the pinned evaluator's validation checks pass; no rescaling, reprojection or distance mapping is applied to the value (objective line 42/48).",
        'checks_applied_in_order': [
            "payload['predictions_available'] is True and payload['source_fixed_point']['converged_finite_fixed_point'] is True (else FORWARD_UNAVAILABLE_NO_SCORE)",
            "payload['semantics']=='TOTAL_OBSERVABLE', payload['units']=='km/s', payload['inclination_applied_once'] is True",
            "[row['id'] for row in payload['rows']] == region ids == [d['id'] for d in payload['query_physics']] == DDO154_SPARC12_01..12",
            "per row: close(d['radius_m'], reference_radius_kpc*(distance_Mpc/4.04)*kpc_m)",
            "per row: nodes non-empty, len(nodes)==len(normalized_estimator_weights), close(fsum(weights),1)",
            "per node: weight finite and >=0; close(los_km_s, v/1000*sin(physical_inclination_rad)*cos(phi_rad))",
            "per row: den=fsum(w*basis^2) > 0 with basis=sin(released_inclination_rad)*cos(phi_rad); close(speed_km_s, fsum(w*basis*los)/den)",
            "close(x,y) := isfinite(x) and isfinite(y) and |x-y| <= atol + rtol*max(|x|,|y|)",
        ],
        'constants': {'distance_Mpc': DISTANCE_MPC, 'radius_reference_Mpc': RADIUS_REFERENCE_MPC, 'kpc_m': KPC_M,
                      'physical_inclination_rad': PHYSICAL_INCLINATION_RAD, 'released_inclination_rad': RELEASED_INCLINATION_RAD,
                      'mapping_relative_tolerance': MAPPING_RELATIVE_TOLERANCE, 'mapping_absolute_tolerance': MAPPING_ABSOLUTE_TOLERANCE},
        'nuisance_handling': 'distance and inclinations are consistency checks with fixed documented values; they are not applied, not seed fields, and not accepted as theta coordinates (see exposed_coordinates).',
        'documented_source_cited_not_loaded': {'evaluator': dict(EVALUATOR), 'objective': dict(OBJECTIVE), 'comparison_run': COMPARISON_RUN},
    }


def _forward_result(valid, speeds, reasons, provenance, ok):
    return {'ok': bool(ok), 'speeds_km_s': dict(speeds), 'valid': bool(valid), 'reasons': list(reasons), 'provenance': provenance}


def _bitwise_equal(a, b):
    return struct.pack('<d', float(a)) == struct.pack('<d', float(b))


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------
def exposed_coordinates():
    """Static declaration of the seed's variable and frozen coordinates (no I/O)."""
    try:
        coords = []
        for c in _EXPOSED:
            coords.append(copy.deepcopy(c))
        for c in _UNIT_CONSTANTS:
            coords.append(copy.deepcopy(c))
        for name, units in _NUMERICAL_CONTROLS:
            coords.append({'name': name, 'seed_pointer': '/numerical_inputs/' + name, 'units': units,
                           'role_hint': 'numerical', 'exposed': False,
                           'note': 'Numerical control passed verbatim to prep.prepare_inputs(**numerical_inputs) (binding line 34) and bound into the checkpoint identity numerical_controls. Frozen by dispatch 0463 rule 1; copied unchanged.'})
        for c in _NUISANCES:
            coords.append(copy.deepcopy(c))
        for c in _SEED_ANNOTATIONS:
            coords.append(copy.deepcopy(c))
        for n in _NATIVE_RATIO_NAMES:
            coords.append({'name': n, 'seed_pointer': None, 'units': 'dimensionless (native energy ratio)',
                           'role_hint': 'shared_scale', 'exposed': False,
                           'note': 'One of the 11 native ratios after the energy quotient. Frozen inside the pinned native response point ' + COEFFICIENT_FREEZE['path'] + ' (' + COEFFICIENT_FREEZE['sha256'][:8] + '...), which prep loads at lines 73-76; no seed field reads it. Not variable without a new sampler run.'})
        coords.append({'name': 'b', 'seed_pointer': None, 'units': 'native energy (b = beta_native*Ud)',
                       'role_hint': 'shared_scale', 'exposed': False,
                       'note': 'Common positive b declared in GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json ("No value chosen here"). No seed field, no worker argument; it enters only through the frozen native response point. Not variable without a new sampler run.'})
        return {
            'ok': True,
            'coordinates': coords,
            'exposed_names': [c['name'] for c in _EXPOSED],
            'mirror_pointers': copy.deepcopy(_MIRROR_POINTERS),
            'not_variable_without_new_sampler_run': list(_NOT_VARIABLE_WITHOUT_NEW_SAMPLER_RUN),
            'shared_15_mapping': {k: v for k, v in _SHARED_15_MAPPING},
            'shared_15_source': {
                'count_statement': ROOT + '/CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md line 53: "11 native ratios plus b,Eref,ell_F,gamma_bar (15 coordinates) before source/allocation nuisances"',
                'uniform_energy_coordinate_names': ROOT + '/CODEX1/READINESS_C178_SHARED_CALIBRATION_EXTENSION_V002.json /current_uniform_energy_coordinates (12 names; quotient by one energy unit leaves 11 ratios, written relative to Ud as in GALAXY_RAW_ENERGY_COORDINATE_LIFT_ADOPTION_V001.json)',
                'gamma_bar_identification': "Identified with the seed's net coupling numerical_inputs.gamma (dispatch 0463 'native/EH ratio (gamma)'; assembly line 51 Gamma_total = gamma*I_R + ...). The seed contains no other gamma-like coupling. Stated as an identification, not a derivation.",
            },
            'frozen_top_level_pointers': list(_FROZEN_TOP_LEVEL),
            'worker': dict(WORKER),
            'seed_read_by_worker': 'The worker reads seed["numerical_inputs"] (prep arguments and checkpoint physical/numerical identity) and seed["pins"] (verified from bytes before preparation); every other seed field is recorded in start.json and otherwise unread.',
            'nuisance_handling': 'Distance (4.04 Mpc) and inclinations (66/64 deg) are not seed fields; the worker fixes them (binding line 112; prep lines 66-68) and the pinned evaluator only checks them. read_result applies the same checks with the same constants and takes no nuisance arguments; write_seed refuses them as theta names.',
            'transform': _transform_description(),
            'reasons': [],
        }
    except Exception as exc:  # pragma: no cover
        return {'ok': False, 'coordinates': [], 'not_variable_without_new_sampler_run': [], 'shared_15_mapping': {},
                'reasons': ['EXCEPTION: %s: %s' % (type(exc).__name__, exc)]}


def write_seed(*, base_seed_path, base_seed_sha256, theta, out_path):
    """Create a NEW seed at out_path from the pinned base seed with only the exposed fields of theta changed."""
    reasons = []
    result = {'ok': False, 'seed_sha256': None, 'changed_fields': [], 'frozen_field_count': None, 'reasons': reasons,
              'out_path': None, 'base_seed_sha256': None, 'pins_copied': None}
    try:
        bp = _path_arg(base_seed_path, 'base_seed_path', reasons)
        op = _path_arg(out_path, 'out_path', reasons)
        pin = _pin_arg(base_seed_sha256, 'base_seed_sha256', reasons)
        if not isinstance(theta, dict):
            reasons.append('theta must be a dict {coordinate_name: float}')
        if reasons:
            return result
        result['out_path'] = os.path.abspath(op)
        # theta validation against the declared exposed coordinates
        exposed = {c['name']: c for c in _EXPOSED}
        declared_not_exposed = {c['name'] for c in _UNIT_CONSTANTS} | {n for n, _ in _NUMERICAL_CONTROLS} | \
            {c['name'] for c in _NUISANCES} | {c['name'] for c in _SEED_ANNOTATIONS} | set(_NOT_VARIABLE_WITHOUT_NEW_SAMPLER_RUN)
        if not theta:
            reasons.append('theta is empty; at least one exposed coordinate is required')
        values = {}
        for name in sorted(theta, key=lambda k: str(k)):
            if not isinstance(name, str):
                reasons.append('theta key %r is not a string' % (name,))
                continue
            if name not in exposed:
                if name in declared_not_exposed:
                    reasons.append('REFUSED coordinate %r: declared but not exposed (frozen, nuisance handled outside the seed, or not variable without a new sampler run)' % name)
                else:
                    reasons.append('REFUSED unknown coordinate name %r' % name)
                continue
            v = theta[name]
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                reasons.append('theta[%r] must be a float, got %s' % (name, type(v).__name__))
                continue
            fv = float(v)
            if not math.isfinite(fv):
                reasons.append('theta[%r] must be finite' % name)
                continue
            if name in ('Eref_J', 'ell_F_m') and fv <= 0:
                reasons.append('theta[%r] must be > 0 (prep positivity, prep lines 46-49)' % name)
                continue
            values[name] = fv
        if reasons:
            return result
        # out_path must be absent; parent must exist; never create directories or overwrite
        if os.path.lexists(op):
            reasons.append('REFUSED: out_path already exists: ' + op)
            return result
        parent = os.path.dirname(os.path.abspath(op)) or '.'
        if not os.path.isdir(parent):
            reasons.append('REFUSED: parent directory of out_path does not exist: ' + parent)
            return result
        if os.path.abspath(op) == os.path.abspath(bp):
            reasons.append('REFUSED: out_path equals base_seed_path')
            return result
        # base seed: verify pin from bytes before parsing
        base, actual = _load_pinned_json(bp, pin, 'base seed', reasons)
        if base is None:
            return result
        result['base_seed_sha256'] = actual
        if not isinstance(base, dict) or any(k not in base for k in _REQUIRED_SEED_KEYS):
            reasons.append('base seed lacks required keys %r' % (_REQUIRED_SEED_KEYS,))
            return result
        if not isinstance(base['numerical_inputs'], dict) or not isinstance(base['physical'], dict) or not isinstance(base['pins'], dict):
            reasons.append('base seed numerical_inputs/physical/pins must be objects')
            return result
        for name in values:
            for ptr in [exposed[name]['seed_pointer']] + _MIRROR_POINTERS[name]:
                try:
                    old = _get_pointer(base, ptr)
                except (KeyError, IndexError, TypeError):
                    reasons.append('base seed lacks declared field ' + ptr)
                    continue
                if isinstance(old, bool) or not isinstance(old, (int, float)):
                    reasons.append('base seed field %s is not numeric' % ptr)
        if reasons:
            return result
        new = copy.deepcopy(base)
        changed = []
        for name in sorted(values):
            for ptr in [exposed[name]['seed_pointer']] + _MIRROR_POINTERS[name]:
                old = _get_pointer(new, ptr)
                _set_pointer(new, ptr, values[name])
                changed.append({'pointer': ptr, 'old': old, 'new': values[name]})
        # serialize in the base seed's own layout (indent=2, trailing newline; round-trips the base bytes)
        text = json.dumps(new, indent=2, allow_nan=False) + '\n'
        raw = text.encode('utf-8')
        with open(op, 'x', encoding='utf-8') as f:
            f.write(text)
            f.flush()
        written = _read_bytes(op)
        if written != raw:
            reasons.append('written seed bytes differ from intended bytes')
            return result
        result['seed_sha256'] = _sha256_bytes(written)
        result['changed_fields'] = changed
        result['frozen_field_count'] = _leaf_count(base) - len(changed)
        result['pins_copied'] = len(base['pins'])
        result['pins_identical'] = (new['pins'] == base['pins'])
        result['ok'] = True
        return result
    except Exception as exc:
        reasons.append('EXCEPTION: %s: %s' % (type(exc).__name__, exc))
        result['ok'] = False
        return result


def read_result(*, outdir, region_path, region_sha256):
    """Read a worker output directory into a forward-style result using the pinned evaluator's transform."""
    reasons = []
    prov = {'adapter': ADAPTER_NAME, 'outdir': None, 'result_json_path': None, 'result_sha256': None,
            'region_sha256': None, 'transform': _transform_description(), 'status': None,
            'files_present': {}, 'seed_pin': None, 'elapsed_seconds': None, 'accepted_for_calibration': None,
            'dynamics_status': None, 'row_ids': list(ROW_IDS), 'mapping_checks': []}
    try:
        od = _path_arg(outdir, 'outdir', reasons)
        rp = _path_arg(region_path, 'region_path', reasons)
        rpin = _pin_arg(region_sha256, 'region_sha256', reasons)
        if reasons:
            return _forward_result(False, {}, reasons, prov, ok=False)
        prov['outdir'] = os.path.abspath(od)
        region, actual = _load_pinned_json(rp, rpin, 'region', reasons)
        if region is None:
            return _forward_result(False, {}, reasons, prov, ok=False)
        prov['region_sha256'] = actual
        rows = _region_rows(region, reasons)
        if rows is None:
            return _forward_result(False, {}, reasons, prov, ok=False)
        # from here on every outcome is a determination about the directory: ok=True, valid as found
        if not os.path.isdir(od):
            reasons.append('OUTDIR_MISSING: not a directory: ' + od)
            prov['status'] = 'OUTDIR_MISSING'
            return _forward_result(False, {}, reasons, prov, ok=True)
        names = ('start.json', 'progress.jsonl', 'result.json', 'finish.json', 'failure.json')
        prov['files_present'] = {n: os.path.isfile(os.path.join(od, n)) for n in names}
        if prov['files_present']['failure.json']:
            try:
                fail = json.loads(_read_bytes(os.path.join(od, 'failure.json')))
                reasons.append('WORKER_FAILURE: %s: %s' % (fail.get('type'), fail.get('message')))
            except Exception as exc:
                reasons.append('WORKER_FAILURE: failure.json present but unreadable (%s)' % type(exc).__name__)
        rpath = os.path.join(od, 'result.json')
        prov['result_json_path'] = os.path.abspath(rpath)
        if not prov['files_present']['result.json']:
            reasons.append('RESULT_MISSING: no result.json under ' + od)
            prov['status'] = 'RESULT_MISSING'
            return _forward_result(False, {}, reasons, prov, ok=True)
        try:
            raw = _read_bytes(rpath)
        except OSError as exc:
            reasons.append('RESULT_UNREADABLE: %s: %s' % (type(exc).__name__, exc))
            prov['status'] = 'RESULT_UNREADABLE'
            return _forward_result(False, {}, reasons, prov, ok=True)
        prov['result_sha256'] = _sha256_bytes(raw)
        if prov['files_present']['finish.json']:
            try:
                fin = json.loads(_read_bytes(os.path.join(od, 'finish.json')))
                prov['finish_status'] = fin.get('status')
                if fin.get('result_sha256') != prov['result_sha256']:
                    reasons.append('FINISH_RESULT_SHA256_MISMATCH: finish.json %r vs bytes %s' % (fin.get('result_sha256'), prov['result_sha256']))
            except Exception as exc:
                reasons.append('FINISH_UNREADABLE: %s' % type(exc).__name__)
        try:
            packet = json.loads(raw)
        except ValueError as exc:
            reasons.append('RESULT_NOT_JSON: %s' % exc)
            prov['status'] = 'RESULT_NOT_JSON'
            return _forward_result(False, {}, reasons, prov, ok=True)
        if isinstance(packet, dict):
            prov['seed_pin'] = packet.get('seed_pin')
            prov['elapsed_seconds'] = packet.get('elapsed_seconds')
            prov['accepted_for_calibration'] = packet.get('accepted_for_calibration')
        try:
            pred = _walk_pointer(packet, PREDICTION_POINTER)
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            reasons.append('PREDICTION_POINTER_MISSING: %s: %s' % (type(exc).__name__, exc))
            prov['status'] = 'INPUT_OR_FORWARD_VALIDATION_FAILED_NO_SCORE'
            return _forward_result(False, {}, reasons, prov, ok=True)
        t = _transform(pred, rows)
        prov['status'] = t['status']
        prov['dynamics_status'] = t['dynamics_status']
        prov['predictions_available_semantics'] = t['predictions_available_semantics']
        prov['mapping_checks'] = t['mapping_checks']
        prov['node_counts'] = t['node_counts']
        reasons.extend(t['reasons'])
        valid = t['valid'] and not reasons
        return _forward_result(valid, t['speeds'] if valid else {}, reasons, prov, ok=True)
    except Exception as exc:
        reasons.append('EXCEPTION: %s: %s' % (type(exc).__name__, exc))
        return _forward_result(False, {}, reasons, prov, ok=False)


def reproduce_comparison(*, result_json_path, comparison_json_path, region_path, region_sha256):
    """Re-derive the 12 predicted_catalogue_speed_km_s of comparison.json from result.json and compare bitwise."""
    reasons = []
    out = {'ok': False, 'bitwise_equal': False, 'max_abs_diff_km_s': None, 'rows': [], 'reasons': reasons,
           'result_sha256': None, 'comparison_sha256': None, 'region_sha256': None, 'transform': TRANSFORM_NAME,
           'cross_checks': {}, 'mapping_checks_bitwise_equal': None, 'status': None}
    try:
        rp = _path_arg(result_json_path, 'result_json_path', reasons)
        cp = _path_arg(comparison_json_path, 'comparison_json_path', reasons)
        gp = _path_arg(region_path, 'region_path', reasons)
        gpin = _pin_arg(region_sha256, 'region_sha256', reasons)
        if reasons:
            return out
        region, actual = _load_pinned_json(gp, gpin, 'region', reasons)
        if region is None:
            return out
        out['region_sha256'] = actual
        rows = _region_rows(region, reasons)
        if rows is None:
            return out
        try:
            craw = _read_bytes(cp)
            rraw = _read_bytes(rp)
        except OSError as exc:
            reasons.append('unreadable input: %s: %s' % (type(exc).__name__, exc))
            return out
        out['comparison_sha256'] = _sha256_bytes(craw)
        out['result_sha256'] = _sha256_bytes(rraw)
        try:
            comp = json.loads(craw)
            packet = json.loads(rraw)
        except ValueError as exc:
            reasons.append('input is not valid JSON: %s' % exc)
            return out
        if not isinstance(comp, dict) or not isinstance(comp.get('input'), dict) or not isinstance(comp.get('comparison'), dict):
            reasons.append('comparison.json lacks input/comparison objects')
            return out
        cc = out['cross_checks']
        cc['comparison_input_sha256_matches_result_bytes'] = (comp['input'].get('sha256') == out['result_sha256'])
        cc['comparison_prediction_pointer'] = comp['input'].get('prediction_pointer')
        cc['comparison_region_sha256_matches'] = (comp.get('region_sha256') == actual)
        cc['comparison_objective_sha256_matches_documented'] = (comp.get('objective_sha256') == OBJECTIVE['sha256'])
        fmp = comp['comparison'].get('forward_mapping_provenance')
        cc['forward_mapping_provenance_matches_constants'] = bool(isinstance(fmp, dict) and
            fmp.get('distance_Mpc') == DISTANCE_MPC and fmp.get('radius_reference_Mpc') == RADIUS_REFERENCE_MPC and
            fmp.get('physical_inclination_rad') == PHYSICAL_INCLINATION_RAD and
            fmp.get('released_inclination_rad') == RELEASED_INCLINATION_RAD and fmp.get('data_not_reprojected') is True)
        if not cc['comparison_input_sha256_matches_result_bytes']:
            reasons.append('comparison.json input.sha256 %r does not match result.json bytes %s' % (comp['input'].get('sha256'), out['result_sha256']))
        if cc['comparison_prediction_pointer'] != PREDICTION_POINTER:
            reasons.append('comparison.json prediction_pointer %r != %s' % (cc['comparison_prediction_pointer'], PREDICTION_POINTER))
        if not cc['comparison_region_sha256_matches']:
            reasons.append('comparison.json region_sha256 does not match the supplied region pin')
        if not cc['comparison_objective_sha256_matches_documented']:
            reasons.append('comparison.json objective_sha256 differs from the documented objective pin')
        if not cc['forward_mapping_provenance_matches_constants']:
            reasons.append('comparison.json forward_mapping_provenance differs from the documented mapping constants')
        recorded_rows = comp['comparison'].get('rows')
        if not isinstance(recorded_rows, list) or len(recorded_rows) != 12:
            reasons.append('comparison.json comparison.rows must have 12 entries')
            return out
        try:
            recorded = {str(r['id']): r['predicted_catalogue_speed_km_s'] for r in recorded_rows}
        except (KeyError, TypeError) as exc:
            reasons.append('comparison rows malformed: %s' % exc)
            return out
        if [str(r['id']) for r in recorded_rows] != [r['id'] for r in rows]:
            reasons.append('comparison rows are not in the region order')
        try:
            pred = _walk_pointer(packet, PREDICTION_POINTER)
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            reasons.append('PREDICTION_POINTER_MISSING: %s: %s' % (type(exc).__name__, exc))
            return out
        t = _transform(pred, rows)
        out['status'] = t['status']
        reasons.extend(t['reasons'])
        if not t['valid']:
            out['rows'] = [{'id': r['id'], 'reproduced': None, 'recorded': recorded.get(r['id'])} for r in rows]
            return out
        diffs = []
        all_bitwise = True
        for r in rows:
            rid = r['id']
            rep = t['speeds'][rid]
            rec = recorded.get(rid)
            row = {'id': rid, 'reproduced': rep, 'recorded': rec}
            if isinstance(rec, bool) or not isinstance(rec, (int, float)) or not math.isfinite(float(rec)):
                all_bitwise = False
                row['bitwise_equal'] = False
                reasons.append('recorded value for %s is not a finite number' % rid)
            else:
                be = _bitwise_equal(rep, rec)
                row['bitwise_equal'] = be
                row['abs_diff_km_s'] = abs(rep - float(rec))
                diffs.append(row['abs_diff_km_s'])
                all_bitwise = all_bitwise and be
            out['rows'].append(row)
        out['bitwise_equal'] = bool(all_bitwise and len(diffs) == 12)
        out['max_abs_diff_km_s'] = max(diffs) if len(diffs) == 12 else None
        # bonus: the evaluator's recorded radius mapping checks
        checks = fmp.get('checks') if isinstance(fmp, dict) else None
        if isinstance(checks, list) and len(checks) == 12:
            try:
                out['mapping_checks_bitwise_equal'] = all(
                    c['id'] == m['id'] and _bitwise_equal(c['actual_radius_m'], m['actual_radius_m']) and
                    _bitwise_equal(c['expected_radius_m'], m['expected_radius_m'])
                    for c, m in zip(checks, t['mapping_checks']))
            except (KeyError, TypeError):
                out['mapping_checks_bitwise_equal'] = False
        out['ok'] = not reasons
        return out
    except Exception as exc:
        reasons.append('EXCEPTION: %s: %s' % (type(exc).__name__, exc))
        out['ok'] = False
        return out


def make_theta_to_seed(*, base_seed_path, base_seed_sha256):
    """Verify the base pin now and return theta_to_seed(theta, out_path) -> write_seed result."""
    reasons = []
    try:
        bp = _path_arg(base_seed_path, 'base_seed_path', reasons)
        pin = _pin_arg(base_seed_sha256, 'base_seed_sha256', reasons)
        if reasons:
            return {'ok': False, 'theta_to_seed': None, 'reasons': reasons}
        base, actual = _load_pinned_json(bp, pin, 'base seed', reasons)
        if base is None:
            return {'ok': False, 'theta_to_seed': None, 'reasons': reasons, 'actual_sha256': actual}
        if not isinstance(base, dict) or any(k not in base for k in _REQUIRED_SEED_KEYS):
            return {'ok': False, 'theta_to_seed': None, 'reasons': ['base seed lacks required keys %r' % (_REQUIRED_SEED_KEYS,)]}
        bp_abs = os.path.abspath(bp)

        def theta_to_seed(theta, out_path):
            return write_seed(base_seed_path=bp_abs, base_seed_sha256=pin, theta=theta, out_path=out_path)

        return {'ok': True, 'theta_to_seed': theta_to_seed, 'reasons': [], 'base_seed_path': bp_abs,
                'base_seed_sha256': pin, 'exposed_names': [c['name'] for c in _EXPOSED]}
    except Exception as exc:
        return {'ok': False, 'theta_to_seed': None, 'reasons': ['EXCEPTION: %s: %s' % (type(exc).__name__, exc)]}


def make_result_reader(*, region_path, region_sha256):
    """Verify the region pin now and return result_reader(outdir) -> forward-style result."""
    reasons = []
    try:
        rp = _path_arg(region_path, 'region_path', reasons)
        pin = _pin_arg(region_sha256, 'region_sha256', reasons)
        if reasons:
            return {'ok': False, 'result_reader': None, 'reasons': reasons}
        region, actual = _load_pinned_json(rp, pin, 'region', reasons)
        if region is None:
            return {'ok': False, 'result_reader': None, 'reasons': reasons, 'actual_sha256': actual}
        rows = _region_rows(region, reasons)
        if rows is None:
            return {'ok': False, 'result_reader': None, 'reasons': reasons}
        rp_abs = os.path.abspath(rp)

        def result_reader(outdir):
            return read_result(outdir=outdir, region_path=rp_abs, region_sha256=pin)

        return {'ok': True, 'result_reader': result_reader, 'reasons': [], 'region_path': rp_abs,
                'region_sha256': pin, 'row_ids': [r['id'] for r in rows], 'transform': TRANSFORM_NAME}
    except Exception as exc:
        return {'ok': False, 'result_reader': None, 'reasons': ['EXCEPTION: %s: %s' % (type(exc).__name__, exc)]}
