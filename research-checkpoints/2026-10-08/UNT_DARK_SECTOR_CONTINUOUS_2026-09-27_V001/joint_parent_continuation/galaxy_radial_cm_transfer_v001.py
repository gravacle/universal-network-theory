"""Frozen-input, one-parameter published-c(M) radial comparison; no run on import.

Source-only until root release. The selected follow-up precedes inspection of
the V001 radial outcomes. No old force prediction or old fit is recomputed.
"""
import os
import sys
sys.dont_write_bytecode = True
for _key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_key] = '1'
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
STEM = 'GALAXY_RADIAL_CM_TRANSFER_V001'
PREVIOUS = 'GALAXY_RADIAL_TRANSFER_V001'
PINS = {
    'galaxy_radial_transfer_v001.py': '84ea2863dc1f832f1c36a0f8b17b2c2037407876c8ef78867a3748a2d2e0da93',
    'halo_profile_fitter_v001.py': 'e8bc0d90c68fd81a5a78525870c19f4d97b3e1bf8bebb1820fa40b4098201df1',
    PREVIOUS+'_FROZEN.json': '1c6a13d71acd9b12ae6549a04a29520e57a4e2a93eb5e98a9825f9d2b8ed5219',
    PREVIOUS+'_RESULT.json': '77883bc7e0da4ceaf1d623ba835be6dc3c0666dd0b56d0b00aa36e551247f7c0',
    PREVIOUS+'_TESTS.json': 'c0efceee95ee425c799c2b3bce0da8fe1d9db1fcc320942988489971e31c96c1',
    'SPARC_EFFECTIVE_TRANSFER_V001_RESULT.json': 'f8502c04a3f17655172b2f589b48d1eebaa7c46bb64ad9950fd10d34ceb23aa9',
    'SPARC_EFFECTIVE_TRANSFER_V001_FROZEN.json': 'a3cf6c736a647877eb6a2daba06b5f481e00b5c63f8b23b3d831b8d31bada549',
}
SCENARIOS = (('central', 0.), ('minus_0p11', -.11), ('plus_0p11', .11))
GRIDS = (257, 513)
BOUNDS = (8., 15.)
KPC, MSUN, G_SI = 3.085677581491367e19, 1.98847e30, 6.67430e-11
G = G_SI*MSUN/(KPC*1e6)  # kpc (km/s)^2 / Msun
H0, LITTLE_H, FB = 67.1/1000., .671, .0490/.3175  # H0 in km/s/kpc
DEADLINE = math.inf
old = radial = np = None


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_authenticated():
    global old, radial, np
    for name, expected in PINS.items():
        if sha(ROOT/name) != expected:
            raise RuntimeError('Changed pinned input: '+name)
    for name in ('halo_profile_fitter_v001', 'galaxy_radial_transfer_v001'):
        spec = importlib.util.spec_from_file_location(name, ROOT/(name+'.py'))
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        if name == 'halo_profile_fitter_v001':
            old = module
        else:
            radial = module
    np = radial.np


def budget():
    if time.perf_counter() >= DEADLINE:
        raise TimeoutError('55-second invocation budget; resume missing galaxy')


def inputs():
    previous = json.loads((ROOT/(PREVIOUS+'_RESULT.json')).read_text())
    previous_freeze = json.loads((ROOT/(PREVIOUS+'_FROZEN.json')).read_text())
    tests = json.loads((ROOT/(PREVIOUS+'_TESTS.json')).read_text())
    assert previous['census'] == 100 and previous['eligible'] == 94
    assert previous['freeze'] == previous_freeze
    assert tests['passed'] and all(c['passed'] for c in tests['controls'])
    assert tests['freeze_sha256'] == PINS[PREVIOUS+'_FROZEN.json']
    assert previous['synthetic_tests_sha256'] == PINS[PREVIOUS+'_TESTS.json']
    _, _, groups, source_freeze = radial.inputs()
    assert source_freeze == previous_freeze  # Includes the original protocol byte hash.
    cases, census = [], []
    for i, (name, rows) in enumerate(groups):
        filename = f'galaxy_{i:03d}.json'
        path = ROOT/(PREVIOUS+'_CASES')/filename
        expected = previous['case_sha256'][filename]
        if sha(path) != expected:
            raise RuntimeError('Changed inherited case: '+filename)
        case = json.loads(path.read_text())
        assert case['index'] == i and case['name'] == name
        assert case['freeze_sha256'] == PINS[PREVIOUS+'_FROZEN.json']
        assert case['rows_sha256'] == radial.digest(rows) == radial.digest(case['rows'])
        assert case['n'] == len(rows) and case['n_inner'] == len(rows)//2
        if case['n'] >= 6:
            assert case['inner_indices'] == list(range(case['n_inner']))
            assert case['outer_indices'] == list(range(case['n_inner'], case['n']))
        cases.append(case)
        census.append(dict(index=i, name=name, n=case['n'], eligible=case['n'] >= 6,
            n_inner=case['n_inner'], inner_indices=case.get('inner_indices'),
            outer_indices=case.get('outer_indices'), rows_sha256=case['rows_sha256'],
            inherited_case_sha256=expected))
    assert sum(c['eligible'] for c in census) == 94
    freeze = dict(files={**PINS, Path(__file__).name: sha(__file__),
                        STEM+'.md': sha(ROOT/(STEM+'.md'))},
        inherited_case_sha256=previous['case_sha256'], census=census,
        scenarios=[dict(name=name, delta_c=value) for name, value in SCENARIOS],
        constants=dict(G_SI=G_SI, Msun_kg=MSUN, kpc_m=KPC, h=LITTLE_H,
                       H0_km_s_Mpc=H0*1000., omega_b=.0490, omega_m=.3175,
                       log10_mass_bounds=list(BOUNDS), grids=list(GRIDS), golden_iterations=80),
        source_exclusions=source_freeze['inherited_excluded_rows'],
        source_invalid=source_freeze['inherited_central_invalid'],
        a0_si=source_freeze['a0_si'], inherited_r=source_freeze['inherited_r'],
        prior_calibration_galaxies=source_freeze['previous_calibration_galaxies'],
        selection='Follow-up selected before inspecting V001 radial outcomes; no outer selection.')
    return previous, cases, freeze


def parameters(logmass, delta_c):
    logmass = np.atleast_1d(np.asarray(logmass, dtype=float))
    mass = 10.**logmass
    concentration = 10.**(.905-.101*(logmass+math.log10(LITTLE_H)-12.)+delta_c)
    r200 = (G*mass/(100*H0*H0))**(1/3)
    return mass, concentration, r200


def halo_v2(radius, logmass, delta_c):
    """Mass-by-radius matrix. Zero halo is handled outside this function."""
    radius = np.asarray(radius, dtype=float)
    mass, c, r200 = parameters(logmass, delta_c)
    logc = np.log(c)
    logx = np.log(radius)[None, :]+logc[:, None]-np.log(r200)[:, None]
    logmx = logx+old._log_kernel_and_slope('NFW', logx)[0]
    logmc = logc+old._log_kernel_and_slope('NFW', logc)[0]
    result = np.exp(math.log(G*(1-FB))+np.log(mass)[:, None]
                    -np.log(radius)[None, :]+logmx-logmc[:, None])
    if np.any(~np.isfinite(result)) or np.any(result <= 0):
        raise ValueError('Invalid halo prediction; no clipping')
    return result


def scalar_halo_v2(radius, logmass, delta_c):
    """Independent inherited normalized-speed implementation."""
    mass, c, r200 = (float(x[0]) for x in parameters([logmass], delta_c))
    return G*(1-FB)*mass/r200*old.shape('NFW', radius, -math.log(c), r200)


def profile(radius, b2, observed, delta_c, count):
    """Accept only inner arrays. Single fitted parameter; no outer access."""
    budget()
    grid = np.linspace(*BOUNDS, count)
    candidates, controls = [], []

    def objective(logmass):
        budget()
        pred = np.sqrt(b2[None, :]+halo_v2(radius, logmass, delta_c))
        return np.sum((pred-observed[None, :])**2, axis=1)

    losses = objective(grid)
    for i in (0, count//2, count-1):
        fast = np.sqrt(b2+halo_v2(radius, [grid[i]], delta_c)[0])
        slow = np.sqrt(b2+scalar_halo_v2(radius, grid[i], delta_c))
        radial.check(controls, f'scalar_prediction_{i}', radial.relative(fast, slow), 1e-10)
    zero_loss = float(np.sum((np.sqrt(b2)-observed)**2))
    candidates.append(dict(kind='zero_halo_boundary', log10_mass_msun=None,
                           mass_dmo_msun=0., concentration=None, r200_dmo_kpc=None,
                           rs_kpc=None, inner_sse=zero_loss))

    def keep(logmass, kind, **extra):
        mass, c, r200 = (float(x[0]) for x in parameters([logmass], delta_c))
        candidates.append(dict(kind=kind, log10_mass_msun=float(logmass), mass_dmo_msun=mass,
            concentration=c, r200_dmo_kpc=r200, rs_kpc=r200/c,
            inner_sse=float(objective([logmass])[0]), **extra))

    keep(BOUNDS[0], 'finite_lower_boundary')
    keep(BOUNDS[1], 'finite_upper_boundary')
    keep(float(grid[int(np.argmin(losses))]), 'lowest_sampled_grid')
    minima = np.flatnonzero((losses[1:-1] < losses[:-2]) & (losses[1:-1] < losses[2:]))+1
    for index in minima:
        left, right = float(grid[index-1]), float(grid[index+1])
        bracket = [left, right]
        ratio = (math.sqrt(5)-1)/2
        c, d = right-ratio*(right-left), left+ratio*(right-left)
        fc, fd = float(objective([c])[0]), float(objective([d])[0])
        for _ in range(80):
            if fc <= fd:
                right, d, fd = d, c, fc
                c = right-ratio*(right-left)
                fc = float(objective([c])[0])
            else:
                left, c, fc = c, d, fd
                d = left+ratio*(right-left)
                fd = float(objective([d])[0])
        trials = [float(grid[index]), left, right, c, d, (left+right)/2]
        trial = min(trials, key=lambda x: float(objective([x])[0]))
        keep(trial, 'strict_sampled_local_minimum', grid_index=int(index),
             initial_bracket=bracket, final_bracket=[left, right], golden_iterations=80)
    selected = dict(min(candidates, key=lambda x: x['inner_sse']))
    selected.update(zero_halo=selected['mass_dmo_msun'] == 0,
        finite_mass_boundary=selected['log10_mass_msun'] in BOUNDS,
        concentration_extrapolated_low=(selected['mass_dmo_msun'] < 1e10/LITTLE_H
                                       if selected['mass_dmo_msun'] > 0 else None))
    return dict(delta_c=delta_c, grid_count=count, selected=selected, candidates=candidates,
                grid=dict(log10_mass_msun=grid.tolist(), inner_sse=losses.tolist()), controls=controls)


def predict(fitted, radius, b2):
    chosen = fitted['selected']
    return (np.sqrt(b2) if chosen['zero_halo'] else
            np.sqrt(b2+halo_v2(radius, [chosen['log10_mass_msun']], fitted['delta_c'])[0]))


def fit_split(radius, b2, observed, inner_indices, delta_c, count):
    return profile(radius[inner_indices], b2[inner_indices], observed[inner_indices], delta_c, count)


def synthetic_tests():
    controls = []
    nodes, weights = np.polynomial.legendre.leggauss(128)
    nodes, weights = (nodes+1)/2, weights/2
    radii = np.geomspace(.1, 30., 24)
    b2, inner = 200.+15*radii, np.arange(12)
    for name, delta in SCENARIOS:
        mass, c, r200 = (float(x[0]) for x in parameters([12-math.log10(LITTLE_H)], delta))
        radial.check(controls, name+'_concentration_pivot', abs(c/10**(.905+delta)-1), 1e-12)
        radial.check(controls, name+'_radius_definition', abs(100*H0*H0*r200**3/(G*mass)-1), 1e-12)
        radial.check(controls, name+'_mass_at_r200',
            abs(halo_v2(np.array([r200]), [math.log10(mass)], delta)[0, 0]*r200/(G*(1-FB)*mass)-1), 1e-12)
        truth = 11.3
        mass, c, r200 = (float(x[0]) for x in parameters([truth], delta))
        x = radii*c/r200
        positive_m = lambda xx: xx**2*np.sum(weights[None, :]*nodes[None, :]
                                /(1+np.atleast_1d(xx)[:, None]*nodes[None, :])**2, axis=1)
        quadrature = G*(1-FB)*mass/radii*positive_m(x)/positive_m(np.array([c]))[0]
        radial.check(controls, name+'_positive_density_quadrature',
                     radial.relative(halo_v2(radii, [truth], delta)[0], quadrature), 2e-11)
        observed = np.sqrt(b2+quadrature)
        fitted = fit_split(radii, b2, observed, inner, delta, 257)
        radial.check(controls, name+'_recovery_sse', fitted['selected']['inner_sse'], 1e-8)
        radial.check(controls, name+'_recovery_log10_mass',
                     abs(fitted['selected']['log10_mass_msun']-truth), 1e-4)
        changed = observed.copy()
        changed[12:] *= 100+np.arange(12)
        again = fit_split(radii, b2, changed, inner, delta, 257)
        radial.check(controls, name+'_outer_leakage', 0. if radial.digest(fitted) == radial.digest(again) else 1., 0.)
        zero = fit_split(radii, b2, .9*np.sqrt(b2), inner, delta, 257)
        radial.check(controls, name+'_zero_endpoint', 0. if zero['selected']['zero_halo'] else 1., 0.)
        controls.extend(fitted['controls']+again['controls']+zero['controls'])
    return controls


def references(case):
    result = dict(case['fixed'])
    for model, fits in case['halo_fits'].items():
        for fitted in fits:
            result[f'{model}_{fitted["grid_count"]}'] = fitted['readout']
    return result


def one_case(case, freeze_hash, output):
    start = time.perf_counter()
    output.update(index=case['index'], name=case['name'], n=case['n'], n_inner=case['n_inner'],
        rows=case['rows'], rows_sha256=case['rows_sha256'], freeze_sha256=freeze_hash,
        inherited_status=case['status'], inherited_case_sha256=sha(
            ROOT/(PREVIOUS+'_CASES')/f'galaxy_{case["index"]:03d}.json'),
        controls=[], cm_fits={}, references=references(case))
    if case['n'] < 6:
        return output | dict(status='EXCLUDED_LT6', reason=case['reason'], seconds=time.perf_counter()-start)
    radius, observed, errors, gbar, gobs = (np.asarray([row[key] for row in case['rows']]) for key in
        ('R_kpc', 'vobs_kms', 'evobs_kms', 'gbar_si', 'gobs_si'))
    if any(np.any(~np.isfinite(x)) or np.any(x <= 0) for x in (radius, observed, errors, gbar, gobs)):
        raise ValueError('Inherited positive finite row premise failed')
    b2 = gbar*radius/radial.CONV
    inner, outer = np.asarray(case['inner_indices']), np.asarray(case['outer_indices'])
    n = case['n_inner']
    output.update(inner_indices=inner.tolist(), outer_indices=outer.tolist(),
                  split_radius_tied=case['split_radius_tied'])
    radial.check(output['controls'], 'saved_gobs_identity',
                 float(np.max(abs(radial.CONV*observed**2/radius/gobs-1))), 1e-12)
    for name, item in output['references'].items():
        pred = np.asarray(item['prediction_kms'])
        recovered = radial.metrics(pred, radius, observed, errors, n)
        for key in ('residual_kms', 'residual_dex', 'gpred_si'):
            radial.check(output['controls'], name+'_saved_'+key,
                         radial.relative(recovered[key], item[key], floor=0. if key == 'gpred_si' else 1.), 1e-12)
    fitting_input = lambda vv: dict(radius=radius[inner].tolist(), b2=b2[inner].tolist(), observed=vv[inner].tolist())
    output['inner_input_sha256'] = radial.digest(fitting_input(observed))
    changed = observed.copy()
    changed[outer] *= 100+np.arange(len(outer))
    radial.check(output['controls'], 'outer_mutation_inner_identity',
        0. if radial.digest(fitting_input(changed)) == output['inner_input_sha256'] else 1., 0.)
    catalogue_total = case.get('catalogue_total_baryon_mass_msun')
    if catalogue_total is not None and (not math.isfinite(catalogue_total) or catalogue_total < 0):
        raise ValueError('Invalid explicit catalogue baryonic total')
    output['catalogue_total_baryon_mass_msun'] = catalogue_total
    output['baryon_budget_scope'] = ('Explicit catalogue total, not a fit prior' if catalogue_total is not None
                                    else 'UNASSESSED: inherited inputs have no catalogue total; radial field is not a total mass')
    output['paired_outer_differences'] = {}
    for name, delta in SCENARIOS:
        fits = [fit_split(radius, b2, observed, inner, delta, count) for count in GRIDS]
        predictions = [predict(fit, radius, b2) for fit in fits]
        for fit, pred in zip(fits, predictions):
            output['controls'].extend(fit['controls'])
            radial.check(output['controls'], f'{name}_{fit["grid_count"]}_inner_objective',
                         radial.relative(float(np.sum((pred[inner]-observed[inner])**2)), fit['selected']['inner_sse']), 1e-10)
            fit['readout'] = radial.metrics(pred, radius, observed, errors, n)
            r200 = fit['selected']['r200_dmo_kpc']
            fit['rows_beyond_r200_dmo'] = None if r200 is None else np.flatnonzero(radius > r200).tolist()
            fit['outer_rows_beyond_r200_dmo'] = None if r200 is None else outer[radius[outer] > r200].tolist()
            fit['nominal_baryon_budget_exceeded'] = (None if catalogue_total is None else
                                                   catalogue_total > FB*fit['selected']['mass_dmo_msun'])
            output['paired_outer_differences'][f'{name}_{fit["grid_count"]}'] = {
                refname: {metric: fit['readout']['outer'][metric]-ref['outer'][metric]
                          for metric in ('velocity_mse', 'logg_mse')}
                for refname, ref in output['references'].items()}
        radial.check(output['controls'], name+'_grid_objective',
                     radial.relative(fits[0]['selected']['inner_sse'], fits[1]['selected']['inner_sse']), 1e-6)
        radial.check(output['controls'], name+'_outer_prediction_refinement',
                     radial.relative(predictions[0][outer], predictions[1][outer]), 1e-5)
        output['cm_fits'][name] = fits
    return output | dict(status='QUALIFIED' if all(c['passed'] for c in output['controls']) else 'UNRESOLVED_CONTROLS',
                         seconds=time.perf_counter()-start)


def aggregate(cases, freeze, hashes, previous):
    eligible = [c for c in cases if c['n'] >= 6]
    summaries, flags = {}, {}
    for name, _ in SCENARIOS:
        for i, count in enumerate(GRIDS):
            key = f'{name}_{count}'
            items = [case['cm_fits'].get(name, [None, None])[i] for case in eligible]
            summaries[key] = ({metric: float(np.mean([item['readout']['outer'][metric] for item in items]))
                               for metric in ('velocity_mse', 'logg_mse')} if all(x is not None for x in items) else None)
            if all(x is not None for x in items):
                flags[key] = dict(galaxies=len(items), zero_halo=sum(x['selected']['zero_halo'] for x in items),
                    finite_mass_boundary=sum(x['selected']['finite_mass_boundary'] for x in items),
                    below_calibrated_mass=sum(x['selected']['concentration_extrapolated_low'] is True for x in items),
                    any_outer_beyond_r200=sum(bool(x['outer_rows_beyond_r200_dmo']) for x in items),
                    baryon_budget_assessed=sum(x['nominal_baryon_budget_exceeded'] is not None for x in items),
                    baryon_budget_exceeded=sum(x['nominal_baryon_budget_exceeded'] is True for x in items))
    return dict(status='QUALIFIED_COMPLETE_CENSUS' if all(c['status'] in ('QUALIFIED', 'EXCLUDED_LT6') for c in cases)
                else 'UNRESOLVED_COMPLETE_CENSUS', freeze=freeze, case_sha256=hashes, census=len(cases), eligible=len(eligible),
        excluded=[dict(name=c['name'], reason=c['reason']) for c in cases if c['n'] < 6],
        outcomes=[dict(index=c['index'], name=c['name'], status=c['status']) for c in cases],
        outer_galaxy_balanced_MSE=summaries, boundary_and_domain_frequencies=flags,
        inherited_reference_status=previous['status'],
        inherited_reference_outer_galaxy_balanced_MSE=previous['outer_galaxy_balanced_MSE'],
        inherited_reference_numerical_failures=previous['numerical_failures'],
        paired_per_galaxy=[dict(name=c['name'], differences=c.get('paired_outer_differences')) for c in eligible],
        numerical_failures={c['name']: dict(status=c['status'], reason=c.get('reason'),
            controls=[x for x in c['controls'] if not x['passed']]) for c in eligible if c['status'] != 'QUALIFIED'},
        summed_case_seconds=sum(c.get('seconds', 0.) for c in cases),
        interpretation='Three separate fixed concentration scenarios, one fitted inner mass each; exposed conditional radial transfer, not full LCDM.')


def main():
    global DEADLINE
    started = time.perf_counter()
    DEADLINE = started+55.
    load_authenticated()
    previous, inherited, freeze = inputs()
    frozen_path = ROOT/(STEM+'_FROZEN.json')
    command = sys.argv[1:]
    if command == ['freeze']:
        radial.publish(frozen_path, freeze)
        print(json.dumps(dict(status='FROZEN', sha256=sha(frozen_path), census=100, eligible=94)))
        return
    if command not in ([], ['run'], ['tests']):
        raise ValueError('Use freeze, tests, or run/default')
    if json.loads(frozen_path.read_text()) != freeze:
        raise RuntimeError('Freeze differs')
    frozen_hash = sha(frozen_path)
    testpath = ROOT/(STEM+'_TESTS.json')
    if not testpath.exists():
        controls = synthetic_tests()
        radial.publish(testpath, dict(freeze_sha256=frozen_hash, controls=controls,
            passed=all(c['passed'] for c in controls), seconds=time.perf_counter()-started))
    tests = json.loads(testpath.read_text())
    if tests['freeze_sha256'] != frozen_hash or not tests['passed'] or not all(c['passed'] for c in tests['controls']):
        raise RuntimeError('Synthetic qualification failed/mismatched; receipt preserved')
    if command == ['tests']:
        print(json.dumps(dict(status='TESTS_PASSED', checks=len(tests['controls']), sha256=sha(testpath))))
        return
    target = ROOT/(STEM+'_RESULT.json')
    if target.exists() or target.is_symlink():
        raise FileExistsError(target)
    directory = ROOT/(STEM+'_CASES')
    directory.mkdir(exist_ok=True)
    completed, paused = [], None
    for case in inherited:
        path = directory/f'galaxy_{case["index"]:03d}.json'
        if path.exists() or path.is_symlink():
            prior = json.loads(path.read_text())
            if (prior['freeze_sha256'] != frozen_hash or prior['rows_sha256'] != case['rows_sha256']
                    or prior['inherited_case_sha256'] != previous['case_sha256'][path.name]
                    or prior['index'] != case['index'] or prior['name'] != case['name']):
                raise RuntimeError('Existing companion case identity differs')
            continue
        partial = {}
        try:
            budget()
            result = one_case(case, frozen_hash, partial)
        except TimeoutError:
            paused = dict(index=case['index'], name=case['name'])
            break
        except Exception as exc:
            result = partial or dict(index=case['index'], name=case['name'], n=case['n'],
                n_inner=case['n_inner'], rows=case['rows'], rows_sha256=case['rows_sha256'],
                inherited_case_sha256=previous['case_sha256'][path.name], freeze_sha256=frozen_hash,
                controls=[], cm_fits={}, references={})
            result.update(status='ERROR', reason=f'{type(exc).__name__}: {exc}')
        radial.publish(path, result)
        completed.append(dict(index=case['index'], name=case['name'], status=result['status']))
    paths = [directory/f'galaxy_{i:03d}.json' for i in range(100)]
    if all(path.exists() for path in paths):
        cases = [json.loads(path.read_text()) for path in paths]
        result = aggregate(cases, freeze, {path.name: sha(path) for path in paths}, previous)
        result.update(synthetic_tests_sha256=sha(testpath), last_invocation_seconds=time.perf_counter()-started,
                      peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        radial.publish(target, result)
        print(json.dumps(dict(status=result['status'], path=str(target), sha256=sha(target),
            eligible=result['eligible'], outer_galaxy_balanced_MSE=result['outer_galaxy_balanced_MSE'])))
    else:
        print(json.dumps(dict(status='PARTIAL_RESUMABLE', completed_this_invocation=completed,
            completed_census=sum(path.exists() for path in paths), paused_before_completion=paused,
            seconds=time.perf_counter()-started, next_command='same script run; no source changes')))


if __name__ == '__main__':
    main()
