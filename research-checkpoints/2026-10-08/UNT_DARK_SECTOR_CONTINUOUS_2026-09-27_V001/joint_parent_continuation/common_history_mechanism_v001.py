"""Full clamped parent, one shared history; no physical clock or galaxy fit."""
import os
for _name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
import disk_solver as law

ROOT = Path(__file__).resolve().parent
FREEZE = ROOT/'COMMON_HISTORY_MECHANISM_V001_FROZEN.json'
OUTPUT = ROOT/'COMMON_HISTORY_MECHANISM_V001_RESULTS.json'
A0 = 8/(3*math.pi)
AMPLITUDES = np.array([.0025, .01, .04])
GS = law.GS_INT


def ramp(s, order=64):
    s = np.asarray(s)
    x, w = leggauss(order)
    nodes = (x+1)/2
    normalization = np.sum(w*np.exp(-1/(nodes*(1-nodes))))/2
    clipped = np.clip(s, 0., 1.)
    u = clipped[..., None]*nodes
    exponent = np.divide(-1., u*(1-u), out=np.full_like(u, -np.inf),
                         where=(u > 0)&(u < 1))
    f = clipped*np.sum(w*np.exp(exponent), axis=-1)/(2*normalization)
    f = np.where(s >= 1, 1., np.where(s <= 0, 0., f))
    exponent = np.divide(-1., clipped*(1-clipped), out=np.full_like(clipped, -np.inf),
                         where=(clipped > 0)&(clipped < 1))
    derivative = np.exp(exponent)/normalization
    return f, derivative


def equilibrium(delta, h):
    return 2*delta/math.sqrt(3)*np.sinh(
        np.arcsinh(3*math.sqrt(3)*h/(2*delta**2))/3)


def simulate(gap, order, dt, duration):
    nodes, weights = leggauss(order)
    delta = gap+(nodes+1)*(1-gap)/2
    weights = weights*(1-gap)/2*delta
    kb = (1-gap**2)/2
    assert abs(np.sum(weights)/kb-1) < 1e-13
    gs = AMPLITUDES[:, None]
    end = duration+16
    steps = round(end/dt)
    assert abs(steps*dt-end) < 1e-12
    times = np.arange(2*steps+1)*dt/2
    f, fp = ramp(times/duration)
    g = f[:, None]*AMPLITUDES
    gdot = fp[:, None]*AMPLITUDES/duration
    h = g/np.sqrt(1+(g/GS)**2)
    hp = (1+(g/GS)**2)**-1.5
    y = np.zeros((3, order))
    v = y.copy()
    work = np.zeros(3)
    final_h = gs/np.sqrt(1+(gs/GS)**2)
    relaxed_y = equilibrium(delta, final_h)

    def potential(positions, external, internal):
        return (kb*(external**2-internal**2)/2
                +np.sum(weights*(.5*(delta*positions-internal[:, None])**2
                                  +.25*positions**4), axis=-1))

    relaxed_energy = potential(relaxed_y, AMPLITUDES, final_h[:, 0])
    relaxed_b = np.sum(weights*delta*relaxed_y, axis=-1)
    final_hp = (1+(AMPLITUDES/GS)**2)**-1.5
    relaxed_d = AMPLITUDES-final_hp*relaxed_b/kb
    energy_scale = kb*AMPLITUDES**2
    yscale = final_h[:, 0]
    max_work_error = np.zeros(3)
    max_energy_bound_ratio = np.zeros(3)
    max_force_bound_ratio = np.zeros(3)
    min_excitation = np.full(3, np.inf)
    snapshots = []
    observation_steps = {round((duration+hold)/dt): hold for hold in (0, 8, 16)}

    def rhs(pos, vel, index):
        acceleration = delta*h[index, :, None]-delta**2*pos-pos**3
        b = np.sum(weights*delta*pos, axis=-1)
        force = kb*g[index]-hp[index]*b
        return vel, acceleration, force*gdot[index]

    for step in range(1, steps+1):
        i = 2*(step-1)
        a = rhs(y, v, i)
        b = rhs(y+dt*a[0]/2, v+dt*a[1]/2, i+1)
        c = rhs(y+dt*b[0]/2, v+dt*b[1]/2, i+1)
        d = rhs(y+dt*c[0], v+dt*c[1], i+2)
        y += dt/6*(a[0]+2*b[0]+2*c[0]+d[0])
        v += dt/6*(a[1]+2*b[1]+2*c[1]+d[1])
        work += dt/6*(a[2]+2*b[2]+2*c[2]+d[2])
        kinetic = np.sum(weights*v*v/2, axis=-1)
        energy = kinetic+potential(y, g[i+2], h[i+2])
        max_work_error = np.maximum(max_work_error, abs(energy-work)/energy_scale)
        if step*dt >= duration:
            bvalue = np.sum(weights*delta*y, axis=-1)
            dvalue = AMPLITUDES-final_hp*bvalue/kb
            excitation = energy-relaxed_energy
            min_excitation = np.minimum(min_excitation, excitation/energy_scale)
            max_energy_bound_ratio = np.maximum(max_energy_bound_ratio,
                excitation/(kb*yscale**2/2))
            max_force_bound_ratio = np.maximum(max_force_bound_ratio,
                abs(dvalue-relaxed_d)/(final_hp*yscale))
        if step in observation_steps:
            for j, amplitude in enumerate(AMPLITUDES):
                snapshots.append({'g_over_a0': float(amplitude/A0),
                    'hold': observation_steps[step], 'time': step*dt,
                    'D': float(dvalue[j]), 'D_relaxed': float(relaxed_d[j]),
                    'D_over_g': float(dvalue[j]/amplitude),
                    'D_relaxed_over_g': float(relaxed_d[j]/amplitude),
                    'signed_departure_over_g': float((dvalue[j]-relaxed_d[j])/amplitude),
                    'kinetic': float(kinetic[j]), 'energy': float(energy[j]),
                    'work': float(work[j]), 'relaxed_energy': float(relaxed_energy[j]),
                    'excitation': float(excitation[j]), 'B': float(bvalue[j]),
                    'y': y[j].tolist(), 'v': v[j].tolist()})
    checks = {'finite': bool(np.all(np.isfinite(y)) and np.all(np.isfinite(v))),
        'work_ledger': bool(np.max(max_work_error) <= 2e-7),
        'nonnegative_excitation': bool(np.min(min_excitation) >= -2e-7),
        'energy_envelope': bool(np.max(max_energy_bound_ratio) <= 1+2e-7),
        'force_envelope': bool(np.max(max_force_bound_ratio) <= 1+2e-7)}
    return {'gap': gap, 'order': order, 'dt': dt, 'duration': duration, 'Kb': kb,
        'delta': delta.tolist(), 'weights': weights.tolist(), 'checks': checks,
        'max_work_identity_error_in_Kb_G2_units': max_work_error.tolist(),
        'min_hold_excitation_in_Kb_G2_units': min_excitation.tolist(),
        'max_hold_energy_bound_ratio': max_energy_bound_ratio.tolist(),
        'max_hold_force_bound_ratio': max_force_bound_ratio.tolist(),
        'relaxed_force_difference_from_full_band_over_g':
            ((relaxed_d-law.f(AMPLITUDES/A0)*A0)/AMPLITUDES).tolist(),
        'observations': snapshots}


def source_census():
    paths = [Path(__file__), ROOT/'COMMON_HISTORY_MECHANISM_PROTOCOL_V001.md',
        ROOT/'RESPONSE_HISTORY_RADIAL_TEST_V001.md', ROOT/'disk_solver.py',
        law.SHAPE_PATH, law.SHAPE_PATH.parent/'SHAPE_REFERENCE_FROZEN.json']
    return {str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p): law.sha(p)
            for p in paths}


def main():
    import sys
    if sys.argv[1:] == ['freeze']:
        law.save_new(FREEZE, {'files': source_census(), 'time_is_uncalibrated': True})
        print('FROZEN; no trajectories run.')
        return
    assert not sys.argv[1:] and not OUTPUT.exists()
    assert json.loads(FREEZE.read_text())['files'] == source_census()
    reference = json.loads(law.SHAPE_PATH.read_text())
    assert reference['freeze_sha256'] == law.sha(law.SHAPE_PATH.parent/'SHAPE_REFERENCE_FROZEN.json')
    assert reference['payload_sha256'] == hashlib.sha256(law.encode(reference['payload'])).hexdigest()
    start = time.perf_counter()
    ramp_difference = float(np.max(abs(ramp(np.linspace(0, 1, 641), 64)[0]
                                     -ramp(np.linspace(0, 1, 641), 128)[0])))
    cases = [simulate(gap, order, dt, duration)
        for gap in (.001, .002) for duration in (8, 16)
        for order, dt in ((64, .01), (128, .01), (128, .005))]
    differences = []
    for i in range(0, len(cases), 3):
        for ia, ib, label in ((0,1,'quadrature'), (1,2,'time_step')):
            left, right = cases[i+ia], cases[i+ib]
            errors = []
            for a,b in zip(left['observations'], right['observations']):
                assert (a['g_over_a0'], a['hold']) == (b['g_over_a0'], b['hold'])
                g = a['g_over_a0']*A0
                errors.extend([abs(a['D']-b['D'])/g,
                    abs(a['energy']-b['energy'])/(left['Kb']*g*g),
                    abs(a['work']-b['work'])/(left['Kb']*g*g)])
            differences.append({'gap': left['gap'], 'duration': left['duration'],
                'type': label, 'max_scaled_error': max(errors), 'pass': max(errors)<=2e-6})
    checks = {'ramp_quadrature': ramp_difference < 1e-12,
              'all_trajectory_checks': all(all(c['checks'].values()) for c in cases),
              'all_resolution_checks': all(d['pass'] for d in differences)}
    payload = {'role': 'Conditional clamped mechanical mechanism test; not dynamic gravity or native UNT matching.',
        'parameters': {'kappa': 1, 'u4': 1, 'A': 1, 'Lambda': 1, 'm': 1,
            'a0_internal': A0, 'gs_internal': GS, 'time_unit': 'UNCALIBRATED'},
        'ramp_quadrature_max_difference': ramp_difference, 'cases': cases,
        'resolution_comparisons': differences, 'checks': checks,
        'seconds': time.perf_counter()-start,
        'peak_self_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    law.save_new(OUTPUT, {'freeze_sha256': law.sha(FREEZE), 'payload': payload,
        'payload_sha256': hashlib.sha256(law.encode(payload)).hexdigest()})
    print(json.dumps({'checks': checks, 'seconds': payload['seconds'],
        'comparisons': differences, 'fine_cases': [{k:v for k,v in c.items()
            if k in ('gap','duration','checks','max_work_identity_error_in_Kb_G2_units',
                     'max_hold_energy_bound_ratio','max_hold_force_bound_ratio')}
            for c in cases if c['dt']==.005]}, indent=2))


if __name__ == '__main__':
    main()
