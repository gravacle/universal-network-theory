#!/usr/bin/env python3
"""New bounded paired-spectrum reference; no survey or UNT-field reprocessing."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, traceback

AUTHOR_DRAFT = True
J = Path(__file__).resolve().parent
STEM = 'ROOT_NGC3198_PAIRED_SPECTRAL_CONVENTION_V001'
PINS = {
    'NGC3198_FINE_Q3_43_POINT_SAVED_RECAP_V001.json': 'ea6e41a879bab1ed43fa556031ad96ae3535779707af62d30eff061b191fc024',
    'CROSS_U_ORDINARY_GEODESIC_AND_PHOTON_OBSERVATION_BRIDGE_AUDIT_V001.md': 'd5acb4229e79a79b4c394d162d02182973ab12284cf5155158186829a3f2c4bc',
}
C = 299792.458  # km/s
INCLINATION_DEG = 73.0
SYSTEMIC_REFERENCE_KMS = 660.0  # Declared SR reference, not a SPARC re-reduction.
COMMON_STATIC_LOG_FACTOR = 1.0256198871e-6  # Conditional maximum Phi_obs-Phi_em; common reference only.
ABS_CONTROL_KMS = 3e-8  # Cancellation envelope for order-one wavelength ratios.

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def utc():
    return datetime.now(timezone.utc).isoformat()

def publish(suffix, value):
    path = J / (STEM + suffix)
    with path.open('x') as handle:
        json.dump(value, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write('\n')
    path.chmod(0o444)
    return {'name': path.name, 'sha256': sha(path)}

def pair_reference(v, common_factor):
    beta = v / C
    if not math.isfinite(v) or not 0 <= beta < 1 or not common_factor > 0:
        raise ValueError('Finite subluminal rotation and positive reference factor required')
    sini = math.sin(math.radians(INCLINATION_DEG))
    gamma = 1 / math.sqrt(1 - beta * beta)
    q = beta * sini
    plus = common_factor * gamma * (1 + q)
    minus = common_factor * gamma * (1 - q)
    functions = {
        'optical': lambda r: C * (r - 1),
        'radio': lambda r: C * (1 - 1 / r),
        'special_relativistic': lambda r: C * (r * r - 1) / (r * r + 1),
    }
    odd = {name: (fn(plus) - fn(minus)) / (2 * sini) for name, fn in functions.items()}
    normalized_pair = C * (plus - minus) / (plus + minus) / sini
    # Independent algebraic optical/radio expectations; retain raw centroids.
    expected = {'optical': common_factor * gamma * v,
                'radio': v / (common_factor * gamma * (1 - q * q))}
    errors = {name: abs(odd[name] - expected[name]) for name in expected}
    errors['normalized_pair'] = abs(normalized_pair - v)
    if max(errors.values()) > ABS_CONTROL_KMS:
        raise ValueError('Original paired-spectrum control failed: ' + repr(errors))
    return {'lambda_plus_over_rest': plus, 'lambda_minus_over_rest': minus,
            'odd_deprojected_kms': odd,
            'odd_minus_input_kms': {name: value - v for name, value in odd.items()},
            'normalized_pair_kms': normalized_pair, 'controls_absolute_kms': errors}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    if AUTHOR_DRAFT or not args.execute:
        raise SystemExit('Held draft: root release and explicit --execute required')
    started = utc()
    receipt = {'owner_pid': os.getpid(), 'started': started, 'input_sha256': PINS,
               'source_sha256': sha(Path(__file__)), 'status': 'RUNNING'}
    for name, expected in PINS.items():
        if sha(J / name) != expected:
            raise ValueError('Input changed: ' + name)
    data = json.loads((J / next(iter(PINS))).read_text())
    if len(data['rows']) != 43 or data['arm'] != 'FINE_Q3':
        raise ValueError('Authentic 43-row FINE_Q3 context required')
    bsys = SYSTEMIC_REFERENCE_KMS / C
    factor = math.sqrt((1 + bsys) / (1 - bsys))
    branches = {'no_systemic_reference': 1.0,
                'common_SR_systemic_reference': factor,
                'same_systemic_plus_conditional_static_factor': factor * math.exp(COMMON_STATIC_LOG_FACTOR)}
    rows = []
    for row in data['rows']:
        out = {'R_kpc': row['R_kpc'], 'quoted_error_kms': row['quoted_error_kms'],
               'minimum_required_shift_kms': row['signed_minimum_prediction_shift_into_interval_kms']}
        for kind, key in [('saved_prediction', 'Q1_predicted_velocity_kms'),
                          ('observed_speed_reference', 'observed_velocity_kms')]:
            v = row[key]
            out[kind] = {'input_kms': v, 'branches': {name: pair_reference(v, a) for name, a in branches.items()}}
        rows.append(out)
    maxima = {branch: {convention: max(abs(row[kind]['branches'][branch]['odd_minus_input_kms'][convention])
                     for row in rows for kind in ('saved_prediction', 'observed_speed_reference'))
                     for convention in ('optical', 'radio', 'special_relativistic')} for branch in branches}
    maximum_control = max(err for row in rows for kind in ('saved_prediction', 'observed_speed_reference')
                          for ref in row[kind]['branches'].values() for err in ref['controls_absolute_kms'].values())
    result = {'status': 'PASS_REFERENCE_ONLY', 'input_sha256': PINS, 'rows': rows,
              'assumptions': {'c_kms': C, 'inclination_deg': INCLINATION_DEG,
                              'systemic_SR_reference_kms': SYSTEMIC_REFERENCE_KMS,
                              'conditional_common_static_log_factor': COMMON_STATIC_LOG_FACTOR,
                              'wavelength_common_factors': branches},
              'maximum_absolute_convention_change_kms': maxima,
              'maximum_control_absolute_kms': maximum_control,
              'absolute_control_gate_kms': ABS_CONTROL_KMS,
              'physical_flags': {name: False for name in ('SPARC_reprocessed', 'full_metric_supplied',
                                 'UNT_optical_shift_derived', 'galaxy_success', 'joint_superiority')},
              'interpretation': 'Paired ideal axisymmetric spectra only. Common endpoint/systemic/static factors cancel in the normalized pair; published radio/optical/SR convention differences are retained as reference controls. No observed table, source, metric or error is changed. Dynamic/directional transport, line Hamiltonian, clocks, beam and tilted-ring reduction still require actual registration.'}
    receipt['result'] = publish('_RESULT.json', result)
    for name, expected in PINS.items():
        if sha(J / name) != expected:
            raise ValueError('Input changed during reference: ' + name)
    receipt.update(status='CLOSED', closed=utc(), exit_code=0)
    publish('_RECEIPT.json', receipt)
    print(json.dumps({'pid': os.getpid(), 'status': receipt['status'], 'max_control_kms': maximum_control,
                      'max_convention_change_kms': maxima}, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception:
        publish('_FAILURE.json', {'owner_pid': os.getpid(), 'closed': utc(), 'traceback': traceback.format_exc()})
        raise
