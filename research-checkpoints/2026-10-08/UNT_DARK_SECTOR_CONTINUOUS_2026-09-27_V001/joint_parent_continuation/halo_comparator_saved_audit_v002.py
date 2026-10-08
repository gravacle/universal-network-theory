"""Independent saved-parameter arithmetic audit; no optimizer or PDE imports."""
import hashlib
import json
import math
from pathlib import Path
import statistics

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def kernel(model, x):
    # Independent convergent series, not the frozen Horner implementation.
    if x < .2:
        if model == 'NFW':
            return math.fsum(((-1.)**j)*(j+1)/(j+2)*x**(j+1) for j in range(36))
        return math.fsum(((-1.)**j)*x**(2*j+2)/(2*j+3) for j in range(24))
    if model == 'NFW':
        return (math.log1p(x)-x/(1+x))/x
    return 1-math.atan(x)/x


def shape(model, radii, pivot, candidate):
    ell = candidate['logscale']
    if ell is None:
        lower = candidate['kind'] == 'zero_scale_limit'
        exponent = (-1 if lower else 1) if model == 'NFW' else (0 if lower else 2)
        return [(r/pivot)**exponent for r in radii]
    scale = pivot*math.exp(ell)
    den = kernel(model, pivot/scale)
    return [kernel(model, r/scale)/den for r in radii]


def run():
    frozen_path = HERE/'HALO_COMPARATOR_V002_FROZEN.json'
    freeze = json.loads(frozen_path.read_text())
    freeze_sha = sha(frozen_path)
    inputs = {str(frozen_path.relative_to(HERE)): freeze_sha}
    assert all(sha(ROOT/n) == h for n, h in freeze['files'].items())
    max_error, count = {}, 0

    def check(label, actual, expected, tol=1e-9):
        nonlocal count
        error = abs(actual-expected)/max(1., abs(actual), abs(expected))
        count += 1
        max_error[label] = max(max_error.get(label, 0.), error)
        assert math.isfinite(error) and error <= tol, (label, actual, expected, error)

    def load(name, require_freeze=True):
        path = HERE/name
        inputs[name] = sha(path)
        record = json.loads(path.read_text())
        assert hashlib.sha256(encode(record['payload'])).hexdigest() == record['payload_sha256']
        if require_freeze:
            assert record['freeze_sha256'] == freeze_sha
        return record

    tests = load('HALO_COMPARATOR_V002_TESTS.json')
    assert tests['status'] == 'COMPLETE' and all(c['passed'] for c in tests['payload']['checks'])
    ddo = load('external_ddo154_v001/ROTATION_COMPARISON.json', False)['payload']
    sources, categories = [], {}
    observed_fit_count = 0
    for index, stem in enumerate(freeze['config']['stems']):
        record = load(f'HALO_COMPARATOR_V002_SOURCE_{index:02}.json')
        p = record['payload']
        assert record['status'] == 'COMPLETE' and all(c['passed'] for c in p['checks'])
        assert record['synthetic_result_sha256'] == inputs['HALO_COMPARATOR_V002_TESTS.json']
        assert p['source_index'] == index and p['source'] == stem
        rows = p['original_rows']
        if index < 7:
            old = [load(stem+f'_N512_L255_Newton{n}.json', False)['payload'] for n in (0, 1)]
            assert old[0]['component_masses_Msun'] == old[1]['component_masses_Msun']
            expected = [dict(radius=x['R'], observed=x['velocity'], error=x['error'],
                             baryon_v2=y['velocity_squared'], network=x['prediction'])
                        for x, y in zip(old[0]['comparison'], old[1]['comparison'])]
        else:
            key = 'NA' if index == 7 else 'RO'
            expected = [dict(radius=x['R_kpc'], observed=x['observed_velocity_kms'],
                             error=x['quoted_error_kms'], baryon_v2=x['newtonian']['velocity_squared_kms2'],
                             network=x['candidate']['prediction_kms']) for x in ddo['models'][key]['comparison']]
        assert rows == expected and len(rows) == (43 if index < 7 else 12)
        r = [x['radius'] for x in rows]
        y = [x['observed'] for x in rows]
        b = [x['baryon_v2'] for x in rows]
        assert all(r[i] < r[i+1] for i in range(len(r)-1))
        check('pivot', p['pivot'], statistics.median(r), 0.)
        pivot = p['pivot']

        def scores(prediction, cut):
            ids = [i for i, radius in enumerate(r) if radius >= cut]
            residual = [prediction[i]-y[i] for i in ids]
            sse = math.fsum(x*x for x in residual)
            quoted = math.fsum(((prediction[i]-y[i])/rows[i]['error'])**2 for i in ids)
            return dict(count=len(ids), rms=math.sqrt(sse/len(ids)) if ids else None,
                        mean=math.fsum(residual)/len(ids) if ids else None,
                        velocity_sse=sse, quoted_error_sse=quoted)

        def summaries(prediction, saved):
            for cut in (0., 2., 8.):
                result = scores(prediction, cut)
                for key, value in result.items():
                    if value is None:
                        assert saved[str(cut)][key] is None
                    else:
                        check('summary_'+key, value, saved[str(cut)][key])

        summaries([x['network'] for x in rows], p['network_summary'])
        summaries([math.sqrt(x) for x in b], p['newtonian_summary'])
        census = {(f['model'], f['fit_radius_min'], f['weighting']) for f in p['fits']}
        assert len(p['fits']) == 8 and census == {(m, cut, w) for m in ('NFW', 'ISO')
                                                for cut in (0., 2.) for w in ('equal', 'quoted_error')}
        concise = []
        for f in p['fits']:
            observed_fit_count += 1
            cut = f['fit_radius_min']
            ids = [i for i, radius in enumerate(r) if radius >= cut]
            assert f['fitted_row_indices'] == ids
            weight = [1. if f['weighting'] == 'equal' else 1/x['error']**2 for x in rows]
            for field in ('halo_v2', 'halo_velocity', 'prediction', 'residual'):
                assert len(f[field]) == len(rows)
            for level, grid in (('coarse_profile', 257), ('fine_profile', 513)):
                profile = f[level]
                assert profile['grid_count'] == profile['grid_census'] == grid
                assert len(profile['grid_digest']) == 64
                assert profile['pivot'] == pivot and profile['logscale_bounds'] == [-20., 20.]
                assert profile['amplitude_bisections'] == 96 and profile['golden_iterations'] == 80
                assert len(profile['candidates']) == profile['sampled_local_bracket_count']+4
                assert {x['kind'] for x in profile['candidates'][:4]} == {
                    'finite_lower_boundary', 'finite_upper_boundary', 'zero_scale_limit', 'infinite_scale_limit'}
                selected = profile['selected']
                check('selected_is_minimum', selected['sse'], min(x['sse'] for x in profile['candidates']))
                for candidate in profile['candidates']:
                    s = shape(f['model'], r, pivot, candidate)
                    amplitude = candidate['amplitude']
                    assert amplitude >= 0
                    pred = [math.sqrt(bb+amplitude*ss) for bb, ss in zip(b, s)]
                    score = math.fsum(weight[i]*(pred[i]-y[i])**2 for i in ids)
                    check('candidate_score', score, candidate['sse'])
                    gradient = math.fsum(weight[i]*s[i]*(1-y[i]/pred[i]) for i in ids)
                    check('amplitude_gradient', gradient, candidate['amplitude_gradient'], 1e-8)
                    if not candidate['amplitude_boundary']:
                        check('interior_gradient_zero', gradient, 0., 1e-8)
                    else:
                        assert gradient >= -1e-8
                check('newtonian_fit_score', profile['newtonian_sse'], math.fsum(
                    weight[i]*(math.sqrt(b[i])-y[i])**2 for i in ids))
                assert selected['sse'] <= profile['newtonian_sse']+1e-8*max(1., selected['sse'])
            small, fine = f['coarse_profile']['selected'], f['fine_profile']['selected']
            check('grid_minimum_agreement', small['sse'], fine['sse'], 1e-6)
            s = shape(f['model'], r, pivot, fine)
            halo = [fine['amplitude']*v for v in s]
            pred = [math.sqrt(bb+hh) for bb, hh in zip(b, halo)]
            for i in range(len(rows)):
                check('halo_v2', halo[i], f['halo_v2'][i])
                check('halo_speed', math.sqrt(halo[i]), f['halo_velocity'][i])
                check('full_prediction', pred[i], f['prediction'][i])
                check('signed_residual', pred[i]-y[i], f['residual'][i])
            summaries(pred, f['summaries'])
            categories[fine['kind']] = categories.get(fine['kind'], 0)+1
            statistic = 'velocity_sse' if f['weighting'] == 'equal' else 'quoted_error_sse'
            concise.append(dict(model=f['model'], cut=cut, weighting=f['weighting'],
                kind=fine['kind'], scale=fine['scale'], amplitude=fine['amplitude'],
                halo_fit_rms=f['summaries'][str(cut)]['rms'],
                halo_fit_score=fine['sse'], network_fit_score=p['network_summary'][str(cut)][statistic],
                halo_beats_network=fine['sse'] < p['network_summary'][str(cut)][statistic],
                outermost_prediction=f['prediction'][-1]))
        sources.append(dict(index=index, source=stem, seconds=record['seconds'],
                            peak_self_rss_bytes=record['peak_self_rss_bytes'],
                            saved_check_count=len(p['checks']), network=p['network_summary'],
                            newtonian=p['newtonian_summary'], fits=concise))
    assert observed_fit_count == 72
    return dict(status='COMPLETE_SAVED_ARITHMETIC_AUDIT', source_count=9, fit_count=72,
                independent_check_count=count, maximum_scaled_errors=max_error,
                selected_candidate_categories=categories, synthetic_check_count=len(tests['payload']['checks']),
                input_sha256=inputs, script_sha256=sha(Path(__file__)), sources=sources,
                scope='Saved parameters evaluated independently; no fit or PDE rerun, no grid-digest regeneration.')


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, allow_nan=False))
