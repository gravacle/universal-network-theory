"""Post-result independent midpoint quadratures; no evolution or fitted state."""
import os
for _key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_key] = '1'
import hashlib
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'PREPARED_ACTION_RETURN_INDEPENDENT_REVIEW_DATA.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main():
    assert not OUTPUT.exists(), 'Keep earlier review data.'
    seen = {}

    def freeze(path):
        path = path.resolve()
        if str(path) in seen:
            return
        seen[str(path)] = sha(path)
        f = json.loads(path.read_text())
        for name, digest in f['files'].items():
            member = (path.parent / name).resolve()
            assert sha(member) == digest, str(member)
            seen[str(member)] = digest
            if member.name.endswith('_FROZEN.json'):
                # It has already been hashed, but its transitive members still need checking.
                del seen[str(member)]
                freeze(member)

    def load(stem):
        result_path = ROOT / (stem + '_RESULTS.json')
        freeze_path = ROOT / (stem + '_FROZEN.json')
        freeze(freeze_path)
        result = json.loads(result_path.read_text())
        assert result['freeze_sha256'] == sha(freeze_path)
        assert result['payload_sha256'] == hashlib.sha256(encode(result['payload'])).hexdigest()
        assert all(result['payload']['checks'].values())
        seen[str(result_path)] = sha(result_path)
        return result['payload']

    result = load('PREPARED_ACTION_RETURN_V001')
    states = load('COMMON_HISTORY_MECHANISM_V001')
    phase = load('COMMON_HISTORY_PHASE_MEAN_V003')
    def key(row):
        return (row['gap'], row.get('mode_order', row.get('order')), row['dt'],
                row['duration'], row['g_over_a0'])
    state_index = {}
    for c in states['cases']:
        for o in c['observations']:
            if o['hold'] == 0:
                state_index[key({**c, 'g_over_a0': o['g_over_a0']})] = (c, o)
    phase_index = {key(r): r for r in phase['rows']}
    assert len(result['rows']) == len(phase_index) == len(state_index) == 36
    rows = []
    for r in result['rows']:
        c, o = state_index[key(r)]
        p = phase_index[key(r)]
        delta = np.asarray(c['delta']); weights = np.asarray(c['weights'])
        low = np.asarray(p['mode_data']['turning_low'])
        high = np.asarray(p['mode_data']['turning_high'])
        b = np.asarray(r['mode_data']['zero_source_turning_amplitude'])
        saved_action = np.asarray(r['mode_data']['action'])
        saved_energy = np.asarray(r['mode_data']['zero_source_energy'])
        assert np.all(saved_action > 0) and np.all(saved_energy > 0)
        evaluations = []
        for n in (512, 1024):
            theta = (np.arange(n) + .5) * math.pi / n
            radius = (high - low) / 2
            y = (high + low)[:, None] / 2 + radius[:, None] * np.cos(theta)
            q = y*y + (low + high)[:, None]*y + (
                2*delta*delta + low*low + low*high + high*high)[:, None]
            held_action = radius*radius / math.sqrt(2) * np.mean(
                np.sin(theta)**2*np.sqrt(q), axis=1)
            angle = theta/2
            ss = np.sin(angle)**2
            stiff = delta[:, None]**2 + b[:, None]**2*(1+ss)/2
            returned_action = b*b*np.mean(np.cos(angle)**2*np.sqrt(stiff), axis=1)
            period = 2*math.pi*np.mean(1/np.sqrt(stiff), axis=1)
            energy = .5*(delta*b)**2 + .25*b**4
            pressure = held_action*2*math.pi/period - energy
            qmean = .25*b**4*np.mean(ss**2/np.sqrt(stiff), axis=1)/np.mean(
                1/np.sqrt(stiff), axis=1)
            errors = {
                'held_action': float(np.max(abs(held_action/saved_action-1))),
                'unique_return_inverse': float(np.max(abs(returned_action/held_action-1))),
                'zero_source_period': float(np.max(abs(period/np.asarray(r['mode_data']['zero_source_period'])-1))),
                'zero_source_energy': float(np.max(abs(energy/saved_energy-1))),
                'zero_source_pressure': float(np.max(abs(pressure-np.asarray(r['mode_data']['zero_source_pressure']))/energy)),
                'virial_pressure': float(np.max(abs(pressure-qmean)/energy)),
                'original_action_kinetic': float(np.max(abs(held_action*2*math.pi/np.asarray(p['mode_data']['periods'])
                    -2*np.asarray(p['mode_data']['mean_kinetic']))/np.asarray(p['mode_data']['mode_excitation'])))
            }
            evaluations.append({'midpoint_nodes': n, 'errors': errors,
                'energy_sum': float(weights @ energy), 'pressure_sum': float(weights @ pressure),
                'min_modal_p_over_e': float(np.min(pressure/energy)),
                'max_modal_p_over_e': float(np.max(pressure/energy))})
        final = evaluations[-1]
        G = r['g']; gs = states['parameters']['gs_internal']
        h = G/math.sqrt(1+(G/gs)**2)
        y = np.asarray(o['y']); v = np.asarray(o['v'])
        intrinsic = float(weights @ (.5*v*v+.5*delta*delta*y*y+.25*y**4-delta*h*y))
        preparation = .5*c['Kb']*G*G + intrinsic
        remaining = final['energy_sum']; returned = remaining-preparation
        ledger = {
            'held_intrinsic': abs(intrinsic-r['held_intrinsic_energy'])/(c['Kb']*G*G),
            'preparation': abs(preparation-r['preparation_work'])/(c['Kb']*G*G),
            'original_saved_energy': abs(preparation-o['energy'])/(c['Kb']*G*G),
            'return': abs(returned-r['adiabatic_return_work'])/(c['Kb']*G*G),
            'cycle': abs(preparation+returned-remaining)/(c['Kb']*G*G),
            'saved_final_energy': abs(remaining-r['return_energy'])/remaining,
            'saved_final_pressure': abs(final['pressure_sum']-r['return_pressure'])/remaining,
            'saved_final_w': abs(final['pressure_sum']/remaining-r['return_w'])}
        assert max(ledger.values()) < 2e-8
        assert max(v for e in evaluations for v in e['errors'].values()) < 2e-8
        assert final['min_modal_p_over_e'] >= -2e-8
        assert final['max_modal_p_over_e'] <= 1/3+2e-8
        rows.append({'key': list(key(r)), 'evaluations': evaluations, 'ledger': ledger,
            'return_w': final['pressure_sum']/remaining,
            'preparation_work': preparation, 'adiabatic_return_work': returned,
            'return_energy': remaining})
    output = {'role': 'Post-existing-result midpoint audit; not a new physical preparation.',
        'script_sha256': sha(Path(__file__)), 'input_sha256': seen, 'rows': rows,
        'checks': {'all_36_cases': len(rows) == 36, 'all_checks_pass': True},
        'max_midpoint_identity_error': max(v for r in rows for e in r['evaluations'] for v in e['errors'].values()),
        'max_ledger_error': max(v for r in rows for v in r['ledger'].values())}
    with OUTPUT.open('x') as stream:
        json.dump(output, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')
    print(json.dumps({k: v for k, v in output.items() if k not in ('rows', 'input_sha256')}, indent=2))


if __name__ == '__main__':
    main()
