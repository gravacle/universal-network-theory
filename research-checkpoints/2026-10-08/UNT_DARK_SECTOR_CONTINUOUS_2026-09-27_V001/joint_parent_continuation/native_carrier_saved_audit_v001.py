"""Independent saved-data arithmetic audit; no model import or propagation."""
import cmath
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEM = 'NATIVE_CARRIER_RULER_V001'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main():
    frozen_path = HERE / (STEM + '_FROZEN.json')
    result_path = HERE / (STEM + '_RESULTS.json')
    frozen = json.loads(frozen_path.read_text())
    outer = json.loads(result_path.read_text())
    p = outer['payload']
    assert outer['status'] == 'COMPLETE'
    assert outer['freeze_sha256'] == sha(frozen_path)
    assert outer['payload_sha256'] == hashlib.sha256(canon(p)).hexdigest()
    assert len(frozen['files']) == 7
    for name, wanted in frozen['files'].items():
        path = (HERE / name).resolve()
        path.relative_to(HERE.parent.parent)
        assert sha(path) == wanted, name
    assert p['parameters'] == frozen['parameters']
    assert p['configuration'] == frozen['configuration']
    assert len(p['checks']) == 513
    assert len({c['name'] for c in p['checks']}) == 513
    assert all(c['passed'] and math.isfinite(c['residual']) and
               0 <= c['residual'] <= c['tolerance'] for c in p['checks'])
    times = [0., 1/32, 1/16, 1/8, 1/4, 1/2, 1., math.pi/2, 2., math.pi, 4.]
    expected = {(n, g, t) for n in (2, 3) for g in ('cycle', 'tree') for t in times}
    assert len(p['cases']) == 44
    assert {(r['n'], r['graph_type'], r['age']) for r in p['cases']} == expected
    maxima, count = {}, 0

    def near(key, actual, wanted=0., tol=2e-11):
        nonlocal count
        error = abs(actual-wanted)
        assert math.isfinite(error) and error <= tol, (key, actual, wanted, error)
        maxima[key] = max(maxima.get(key, 0.), error)
        count += 1

    def positive(key, value, tol=2e-11):
        near(key, max(0., -value), tol=tol)

    groups = {}
    for row in p['cases']:
        n, g, age = row['n'], row['graph_type'], row['age']
        graph = ({'cycle': 15, 'tree': 11} if n == 2 else {'cycle': 350, 'tree': 342})[g]
        assert row['mask'] == graph
        o, f = row['readout'], row['frozen_control']
        pops, edges = o['carrier_populations'], o['edge_currents']
        assert len(pops) == 2*n and len(edges) == n*n
        near('population_sum', sum(pops), o['norm'])
        near('normalization', o['norm'], 1.)
        near('source_return', pops[0], o['source_return'])
        near('reader_arrival', pops[n], o['reader_arrival'])
        near('new_population', (pops[2]+pops[5]) if n == 3 else 0., o['new_carrier_population'])
        for x in pops:
            positive('population_positive', x)
        flow = [0.] * (2*n)
        for edge, e in enumerate(edges):
            u, v = edge//n, n+edge%n
            assert (e['edge'], e['left'], e['right']) == (edge, u, v)
            near('current_normalization', e['current'], .5*e['mean_nJ'])
            flow[u] -= e['current']; flow[v] += e['current']
        for recombined, saved, derivative in zip(flow, o['current_flow'], o['population_derivative']):
            near('current_flow', recombined, saved)
            near('continuity', recombined, derivative)
        near('conserved_carrier_current', sum(flow))
        near('conserved_carrier_derivative', sum(o['population_derivative']))
        near('continuity_residual', max(abs(a-b) for a,b in zip(flow,o['population_derivative'])), o['current_continuity_residual'])
        expected_energy = (21.5 if g == 'cycle' else 15.5) + (10. if n == 3 else 0.)
        near('energy', o['energy'], expected_energy, 2e-8)
        near('variance', o['energy_variance'], 1.5, 2e-8)
        near('component_ledger', sum(o['component_energies'].values()), o['energy'])
        near('component_residual', sum(o['component_energies'].values())-o['energy'], o['component_energy_residual'])
        near('onsite_energy', o['component_energies']['carrier_onsite'], o['norm'])
        exact, back, conn, joint = (o[k] for k in ('exact_graph_probability', 'backbone_probability', 'connected_probability', 'joint_exact_graph_reader_probability'))
        for x in (exact, back, conn, joint):
            positive('probability_positive', x); positive('probability_upper', o['norm']-x)
        positive('set_exact_backbone', back-exact)
        positive('set_backbone_connected', conn-back)
        positive('joint_subset_graph', exact-joint)
        positive('joint_subset_reader', o['reader_arrival']-joint)
        amp = o['full_state_return_amplitude']
        return_sq = amp['real']**2+amp['imag']**2
        positive('return_subset_source', o['source_return']-return_sq)
        positive('return_subset_graph', exact-return_sq)
        graph_bound = min(1., age*age)
        backbone_bound = min(1., bin(graph).count('1')*age*age/(n*n))
        near('graph_bound_formula', row['graph_leakage_upper_bound'], graph_bound)
        near('backbone_bound_formula', row['backbone_leakage_upper_bound'], backbone_bound)
        positive('graph_bound', exact-(1-graph_bound))
        positive('backbone_bound', back-(1-backbone_bound))
        positive('state_bound', age-f['native_state_error'], 2e-9)
        near('frozen_norm', sum(f['carrier_populations']), 1.)
        near('frozen_source', f['source_return'], f['carrier_populations'][0])
        near('frozen_reader', f['reader_arrival'], f['carrier_populations'][n])
        if g == 'cycle':
            s = age/2
            arrival = .5j*math.sin(2*s) if n == 2 else 1j*(math.sin(2*s)-2*math.sin(s))/3
            returned = math.cos(s)**2 if n == 2 else (math.cos(2*s)+2*math.cos(s))/3
            phase = cmath.exp(-1j*((20 if n == 2 else 30)+1.5)*age)
            near('cycle_reader_formula', f['reader_arrival'], abs(arrival)**2)
            near('cycle_source_formula', f['source_return'], returned**2)
            near('cycle_full_return_formula', complex(f['full_state_return_amplitude']['real'], f['full_state_return_amplitude']['imag']), phase*returned)
        ratios = row['finite_time_asymptotic_ratios']
        if n == 3 and age:
            near('ratio_arrival', ratios['arrival_over_tau4'], o['reader_arrival']/age**4)
            near('ratio_joint', ratios['joint_arrival_over_tau6'], joint/age**6)
            near('ratio_frozen', ratios['frozen_arrival_over_tau6'], f['reader_arrival']/age**6)
        else:
            assert ratios is None
        groups.setdefault(f'N{n}_{g}', []).append(row)
    assert len(p['method_diagnostics']) == 22
    for m in p['method_diagnostics']:
        n, age = m['n'], m['age']
        near('gershgorin_center', m['center'], sum(m['gershgorin'])/2)
        near('gershgorin_radius', m['radius'], (m['gershgorin'][1]-m['gershgorin'][0])/2)
        for name, error in zip(('cycle','tree'), m['dual_vector_errors']):
            r = next(r for r in groups[f'N{n}_{name}'] if r['age'] == age)
            near('dual_crossreference', r['dual_vector_error'], error)
            positive('dual_gate', 2e-9-error)
        if age:
            t = m['taylor']; x=t['substep_norm']; k=t['terms']
            tail=math.exp((k+1)*math.log(x)-math.lgamma(k+2)-math.log1p(-x/(k+2)))
            near('taylor_substep_tail', t['substep_tail'], tail, 1e-30)
            near('taylor_product_tail', t['product_tail'], math.expm1(t['substeps']*math.log1p(tail)), 1e-28)
            assert x <= .75 and tail < 1e-19
            c=m['chebyshev']; z=m['radius']*age; degree=c['degree']; samples=c['fft_samples']
            assert samples >= max(64,4*(degree+1)) and samples & (samples-1) == 0
            for label, first, multiplier in [('truncation',degree+1,2),('alias',samples-degree,4*(degree+1))]:
                logbound=math.log(multiplier)+first*math.log(z/2)-math.lgamma(first+1)+z*z/(4*(first+1))-math.log1p(-z/(2*(first+1)))
                near('chebyshev_log_bounds', c[label]['log_bound'], logbound, 3e-12)
                assert not c[label]['exact_zero'] and c[label]['underflow'] == (logbound <= -745)
            assert c['truncation']['bound'] < 1e-18
    for r in p['schur_controls']:
        z=r['carrier_energy']-1.5
        expected=[[.25*z/(z*z-.25), -.125/(z*z-.25)],[-.125/(z*z-.25), .25*z/(z*z-.25)]]
        for a,b in zip(sum(r['endpoint_self_energy'],[]),sum(expected,[])):
            near('schur_formula',a,b)
    summaries={}
    for name, rows in groups.items():
        summaries[name]={
            'sampled_min_exact_graph': min((r['readout']['exact_graph_probability'],r['age']) for r in rows),
            'sampled_min_connected': min((r['readout']['connected_probability'],r['age']) for r in rows),
            'sampled_max_native_frozen_state_error': max((r['frozen_control']['native_state_error'],r['age']) for r in rows),
            'age1_arrival':next(r['readout']['reader_arrival'] for r in rows if r['age']==1),
            'age4_arrival':next(r['readout']['reader_arrival'] for r in rows if r['age']==4),
            'smallest_positive_age_ratios':rows[1]['finite_time_asymptotic_ratios']}
    result=dict(status='PASS_SAVED_DATA_AUDIT', audit_source_sha256=sha(Path(__file__)),
                result_sha256=sha(result_path), freeze_sha256=sha(frozen_path),
                payload_sha256=outer['payload_sha256'], authenticated_inputs=frozen['files'],
                scientific_rows=44, original_checks=513, independent_arithmetic_checks=count,
                independent_maxima=maxima, summaries=summaries,
                worst_recorded_check=max(p['checks'],key=lambda c:c['residual']),
                max_dual_vector_error=max(r['dual_vector_error'] for r in p['cases']),
                wall_seconds=p['wall_seconds'], peak_self_rss_bytes=p['peak_rss_bytes'],
                scope='No propagation or matrix-worker rerun; saved amplitudes/currents cannot reconstruct raw states.')
    print(json.dumps(result,sort_keys=True,allow_nan=False))


if __name__ == '__main__':
    main()
