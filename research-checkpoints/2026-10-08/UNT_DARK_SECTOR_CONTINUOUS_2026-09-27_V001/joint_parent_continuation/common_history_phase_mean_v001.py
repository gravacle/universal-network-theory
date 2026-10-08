"""Actual prepared mode energies, exact conservative phase ensemble; no fit."""
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
import disk_solver as law

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT/'COMMON_HISTORY_MECHANISM_V001_RESULTS.json'
FREEZE = ROOT/'COMMON_HISTORY_PHASE_MEAN_V001_FROZEN.json'
OUTPUT = ROOT/'COMMON_HISTORY_PHASE_MEAN_V001_RESULTS.json'


def phase_mean(delta, y, v, h, order):
    star = 2*delta/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/(2*delta**2))/3)
    stiffness = delta**2+3*star**2
    def excess(x):
        return x*x*(stiffness/2+star*x+x*x/4)
    energy = v*v/2+excess(y-star)
    assert np.all(energy > 0)
    roots = []
    for sign in (-1, 1):
        lo = np.zeros_like(delta)
        hi = np.maximum(1., np.sqrt(2*energy/stiffness))
        for _ in range(100):
            bad = excess(sign*hi) < energy
            if not np.any(bad):
                break
            hi[bad] *= 2
        else:
            raise AssertionError('Failed to bracket turning point.')
        for _ in range(90):
            mid = (lo+hi)/2
            below = excess(sign*mid) < energy
            lo = np.where(below, mid, lo)
            hi = np.where(below, hi, mid)
        roots.append(star+sign*(lo+hi)/2)
    a,b = roots
    center, radius = (a+b)/2, (b-a)/2
    x, w = leggauss(order)
    theta = (x+1)*math.pi/2
    weights = w*math.pi/2
    position = center[:, None]+radius[:, None]*np.cos(theta)
    q = (position**2+(a+b)[:, None]*position
         +(2*delta**2+a*a+a*b+b*b)[:, None])
    assert np.all(q > 0) and np.all(a < b)
    measure = weights/np.sqrt(q)
    norm = np.sum(measure, axis=-1)
    def mean(value):
        return np.sum(measure*value, axis=-1)/norm
    ym = mean(position)
    y3m = mean(position**3)
    kin = mean(radius[:, None]**2*np.sin(theta)**2*q/4)
    virm = mean(position*(delta[:, None]**2*position+position**3-delta[:, None]*h))
    mean_excess = mean(
        (position-star[:, None])**2*(stiffness[:, None]/2
            +star[:, None]*(position-star[:, None])+(position-star[:, None])**2/4))
    endpoint_error = np.maximum(abs(excess(a-star)-energy), abs(excess(b-star)-energy))/energy
    energy_error = abs(kin+mean_excess-energy)/energy
    equation_error = abs(delta**2*ym+y3m-delta*h)/(delta*h)
    virial_error = abs(2*kin-virm)/energy
    # Check the polynomial factorization directly against the stable excess form.
    product = radius[:, None]**2*np.sin(theta)**2*q/4
    direct = energy[:, None]-(position-star[:, None])**2*(stiffness[:, None]/2
        +star[:, None]*(position-star[:, None])+(position-star[:, None])**2/4)
    factorization_error = np.max(abs(product-direct)/energy[:, None], axis=-1)
    errors = {'endpoints': float(np.max(endpoint_error)),
        'energy': float(np.max(energy_error)), 'orbit_equation': float(np.max(equation_error)),
        'virial': float(np.max(virial_error)), 'factorization': float(np.max(factorization_error))}
    return {'mean_y': ym.tolist(), 'mean_y3': y3m.tolist(), 'mean_kinetic': kin.tolist(),
        'mode_excitation': energy.tolist(), 'turning_low': a.tolist(), 'turning_high': b.tolist(),
        'periods': (2*math.sqrt(2)*norm).tolist(), 'errors': errors,
        'checks': {k:v <= 2e-8 for k,v in errors.items()}}


def sources():
    paths = [Path(__file__), ROOT/'COMMON_HISTORY_PHASE_MEAN_PROTOCOL_V001.md', SOURCE,
        ROOT/'COMMON_HISTORY_MECHANISM_V001_FROZEN.json', ROOT/'disk_solver.py', law.SHAPE_PATH]
    return {str(p): law.sha(p) for p in paths}


def main():
    import sys
    if sys.argv[1:] == ['freeze']:
        law.save_new(FREEZE, {'files': sources()})
        print('FROZEN; no phase means computed.')
        return
    assert not sys.argv[1:] and not OUTPUT.exists()
    assert json.loads(FREEZE.read_text())['files'] == sources()
    record = json.loads(SOURCE.read_text())
    assert record['freeze_sha256'] == law.sha(ROOT/'COMMON_HISTORY_MECHANISM_V001_FROZEN.json')
    assert record['payload_sha256'] == hashlib.sha256(law.encode(record['payload'])).hexdigest()
    assert all(record['payload']['checks'].values())
    start = time.perf_counter()
    rows = []
    for case in record['payload']['cases']:
        delta = np.array(case['delta'])
        weights = np.array(case['weights'])
        for obs in case['observations']:
            if obs['hold'] != 0:
                continue
            g = obs['g_over_a0']*record['payload']['parameters']['a0_internal']
            gs = record['payload']['parameters']['gs_internal']
            h = g/math.sqrt(1+(g/gs)**2)
            hp = (1+(g/gs)**2)**-1.5
            values = [phase_mean(delta, np.array(obs['y']), np.array(obs['v']), h, n)
                      for n in (64,128,256)]
            forces = [g-hp*np.sum(weights*delta*np.array(v['mean_y']))/case['Kb'] for v in values]
            errors = [abs(forces[i+1]-forces[i])/g for i in (0,1)]
            final = values[-1]
            excitation = float(np.sum(weights*np.array(final['mode_excitation'])))
            source_excitation_error = abs(excitation-obs['excitation'])/(case['Kb']*g*g)
            rows.append({'gap': case['gap'], 'mode_order': case['order'], 'dt': case['dt'],
                'duration': case['duration'], 'g': g, 'g_over_a0': obs['g_over_a0'],
                'phase_mean_D': forces[-1], 'phase_mean_D_over_g': forces[-1]/g,
                'relaxed_D_over_g': obs['D_relaxed']/g,
                'signed_mean_departure_over_g': (forces[-1]-obs['D_relaxed'])/g,
                'prepared_excitation': excitation, 'mean_kinetic':
                    float(np.sum(weights*np.array(final['mean_kinetic']))),
                'quadrature_D_error_over_g': errors,
                'source_excitation_error_in_Kb_g2_units': source_excitation_error,
                'mode_data': final,
                'all_quadrature_checks': [v['checks'] for v in values],
                'checks': {'quadrature': max(errors)<=2e-8,
                    'all_orbit_identities': all(all(v['checks'].values()) for v in values),
                    'source_excitation_preserved': source_excitation_error<=2e-8}})
    payload = {'role': 'Stationary conservative phase comparator of actual clamped preparations, not established equilibration.',
        'rows': rows, 'checks': {'all_rows': all(all(r['checks'].values()) for r in rows)},
        'seconds': time.perf_counter()-start}
    law.save_new(OUTPUT, {'freeze_sha256': law.sha(FREEZE), 'payload': payload,
        'payload_sha256': hashlib.sha256(law.encode(payload)).hexdigest()})
    print(json.dumps({'checks': payload['checks'], 'seconds': payload['seconds'],
        'main_rows': [{k:v for k,v in r.items() if k != 'mode_data'}
                      for r in rows if r['dt']==.005 and r['gap']==.001]}, indent=2))


if __name__ == '__main__':
    main()
