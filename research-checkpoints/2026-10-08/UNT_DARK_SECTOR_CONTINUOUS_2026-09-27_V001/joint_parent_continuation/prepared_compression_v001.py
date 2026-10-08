"""Compression of the SAME returned actions; no abundance or source fitting."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import json
import math
from pathlib import Path
import sys
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
import disk_solver as law

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'PREPARED_ACTION_RETURN_V001_RESULTS.json'
OLD_FREEZE = ROOT / 'PREPARED_ACTION_RETURN_V001_FROZEN.json'
STATES = ROOT / 'COMMON_HISTORY_MECHANISM_V001_RESULTS.json'
FREEZE = ROOT / 'PREPARED_COMPRESSION_V001_FROZEN.json'
OUTPUT = ROOT / 'PREPARED_COMPRESSION_V001_RESULTS.json'
OLD_HASH = 'b8a0efd517e9492aa2546f83eb7cc81bb3a5553e22ff847f5c6f736b545b9678'


def authenticate():
    assert law.sha(OLD) == OLD_HASH
    old = json.loads(OLD.read_text())
    assert old['freeze_sha256'] == law.sha(OLD_FREEZE)
    assert old['payload_sha256'] == hashlib.sha256(law.encode(old['payload'])).hexdigest()
    assert all(old['payload']['checks'].values())
    files = json.loads(OLD_FREEZE.read_text())['files']
    for name, expected in files.items():
        assert law.sha(Path(name)) == expected, name
    paths = [Path(__file__), ROOT / 'PREPARED_COMPRESSION_PROTOCOL_V001.md',
             OLD, OLD_FREEZE, STATES, ROOT / 'disk_solver.py', law.SHAPE_PATH]
    files.update({str(p): law.sha(p) for p in paths})
    return old['payload'], json.loads(STATES.read_text())['payload'], files


def quadrature(delta, b, order):
    x, w = leggauss(order)
    theta = (x+1)*math.pi/4
    weight = w*math.pi/4
    s2 = np.sin(theta)**2
    q = delta[:, None]**2 + b[:, None]**2*(1+s2)/2
    j = np.sum(weight/np.sqrt(q), axis=-1)
    k = np.sum(weight*(1+s2)/q**1.5, axis=-1)
    omega = math.pi/(2*j)
    t = b[:, None]**2*(1+s2)/(2*delta[:, None]**2)
    root = np.sqrt(1+t)
    deficit = 2/math.pi*np.sum(weight*t/(root*(1+root)), axis=-1)
    # Compute omega-delta without cancellation for almost harmonic modes.
    frequency_shift = deficit*math.pi/(2*j)
    action = 2/math.pi*b*b*np.sum(weight*np.cos(theta)**2*np.sqrt(q), axis=-1)
    energy = delta*delta*b*b/2+b**4/4
    curvature = omega*omega*k/(2*j*(delta*delta+b*b))
    return action, omega, energy, curvature, frequency_shift


def relative(a, b):
    return float(np.max(np.abs(np.asarray(a)/np.asarray(b)-1)))


def main():
    old, states, sources = authenticate()
    if sys.argv[1:] == ['freeze']:
        law.save_new(FREEZE, {'files': sources, 'orders': [64, 128],
                              'difference_steps': [1e-3, 5e-4]})
        print('Frozen; no compression result computed.')
        return
    assert not sys.argv[1:] and not OUTPUT.exists()
    assert json.loads(FREEZE.read_text())['files'] == sources
    indexed = {(c['gap'], c['order'], c['dt'], c['duration']): c
               for c in states['cases']}
    start = time.perf_counter()
    rows = []
    for row in old['rows']:
        case = indexed[(row['gap'], row['mode_order'], row['dt'], row['duration'])]
        delta = np.array(case['delta'])
        weights = np.array(case['weights'])
        md = row['mode_data']
        action = np.array(md['action'])
        b = np.array(md['zero_source_turning_amplitude'])
        energy = np.array(md['zero_source_energy'])
        pressure = np.array(md['zero_source_pressure'])
        answers = []
        raw = []
        for order in (64, 128):
            aa, omega, ee, curvature, shift = quadrature(delta, b, order)
            raw.append((aa, omega, ee, curvature, shift))
            enthalpy = float(np.sum(weights*action*omega))
            bulk = float(np.sum(weights*action**2*curvature))
            answers.append({'order': order, 'energy_curvature': curvature.tolist(),
                'modal_c_ad_squared': (action*curvature/omega).tolist(),
                'enthalpy': enthalpy, 'bulk_response': bulk,
                'c_ad_squared': bulk/enthalpy})
        aa, omega, ee, curvature, shift = raw[-1]
        inherited_error = max(relative(aa, action), relative(ee, energy),
            relative(2*math.pi/omega, md['zero_source_period']),
            float(np.max(abs(action*omega-ee-pressure)/energy)))
        quad_error = max(relative(x, y) for x, y in zip(raw[0], raw[1]))
        differences = []
        for eps in (1e-3, 5e-4):
            ap, _, _, _, sp = quadrature(delta, b*np.exp(eps), 128)
            am, _, _, _, sm = quadrature(delta, b*np.exp(-eps), 128)
            differences.append((sp-sm)/(ap-am))
        extrapolated = (4*differences[1]-differences[0])/3
        derivative_error = relative(extrapolated, curvature)
        # Retain a frequency-scaled error alongside the stricter relative one.
        frequency_scale = np.maximum(omega/action, curvature)
        scaled_derivative_error = float(np.max(abs(extrapolated-curvature)/frequency_scale))
        ratio = b*b/(delta*delta)
        modal = action*curvature/omega
        lower = ratio*(ratio+1)/((ratio+2)*(3*ratio+2))
        upper = ratio*(ratio+2)/((ratio+1)*(3*ratio+4))
        checks = {'inherited_identities': inherited_error <= 2e-8,
                  'quadrature': quad_error <= 2e-8,
                  'derivative_relative': derivative_error <= 2e-7,
                  'positive': bool(np.all(curvature > 0)),
                  'analytic_modal_bounds': bool(np.all(modal >= lower-2e-8)
                       and np.all(modal <= upper+2e-8) and np.all(upper < 1/3)),
                  'mixture_bound': 0 < answers[-1]['c_ad_squared'] < 1/3,
                  'low_pressure_bulk_bound': bool(np.all(action**2*curvature <= 2*pressure+2e-8*energy)
                       and answers[-1]['c_ad_squared'] <= 2*row['return_w']/(1+row['return_w'])+2e-8)}
        rows.append({k: row[k] for k in ('gap', 'mode_order', 'dt', 'duration', 'g', 'g_over_a0')} |
            {'return_w': row['return_w'], 'quadratures': answers,
             'c_ad_squared': answers[-1]['c_ad_squared'],
             'inherited_scaled_error': inherited_error,
             'quadrature_relative_error': quad_error,
             'derivative_relative_error': derivative_error,
             'derivative_frequency_scaled_error': scaled_derivative_error,
             'checks': checks})
    payload = {'scope': 'Same-action zero-source common-current adiabatic compression only.',
               'rows': rows, 'checks': {'all_36_rows': len(rows) == 36,
                    'all_checks': all(all(r['checks'].values()) for r in rows)},
               'seconds': time.perf_counter()-start}
    law.save_new(OUTPUT, {'freeze_sha256': law.sha(FREEZE), 'payload': payload,
        'payload_sha256': hashlib.sha256(law.encode(payload)).hexdigest()})
    print(json.dumps({'checks': payload['checks'], 'seconds': payload['seconds'],
        'max_derivative_error': max(r['derivative_relative_error'] for r in rows),
        'main': [{k: r[k] for k in ('duration', 'g_over_a0', 'return_w', 'c_ad_squared')}
                 for r in rows if r['gap'] == .001 and r['dt'] == .005]}, indent=2))


if __name__ == '__main__':
    main()
