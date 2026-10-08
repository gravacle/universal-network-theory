"""Fixed exposed gas benchmarks; not a fitted catalogue population model."""
import json
import math
import pathlib
import sys
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
import effective_esd_forward_v001 as base
from disk_solver import sha, save_new, inverse, SHAPE_PATH

ROOT = pathlib.Path(__file__).resolve().parent
STEM = 'EXTENDED_GAS_ESD_V001'
INPUT = ROOT/'INVERSE_ESD_CALIBRATION_V001_RESULT.json'
RH = 100000*base.PC


def hashes():
    paths = [pathlib.Path(__file__), ROOT/(STEM+'.md'), INPUT,
             ROOT/'effective_esd_forward_v001.py', ROOT/'disk_solver.py', SHAPE_PATH]
    return {str(p): sha(p) for p in paths}


def compact(stellar):
    return stellar*(1+10**(6.63-.69*np.log10(stellar)))


def projected(radius, mc, mh, a0, order=64, newton=False):
    nodes, weights = leggauss(order)
    output = []
    for radius_i in np.atleast_1d(radius):
        boundary = math.acos(radius_i/RH) if radius_i < RH else 0.
        cuts = [0., boundary, math.pi/2] if boundary else [0., math.pi/2]
        total = 0.
        for lo, hi in zip(cuts[:-1], cuts[1:]):
            theta = lo+(nodes+1)*(hi-lo)/2
            weight = weights*(hi-lo)/2
            cosine = np.cos(theta)
            rad = radius_i/cosine
            gas_fraction = np.minimum(rad/RH, 1.)
            mass = mc+mh*gas_fraction
            m = np.where(rad < RH, mh*rad/RH/mass, 0.)
            gn = base.G*mass/rad**2
            if newton:
                grav, derivative = gn, np.ones_like(gn)
            else:
                dimensionless = inverse(gn/a0)
                grav = a0*dimensionless
                derivative = 1/base.flux_derivative(dimensionless)
            assert np.all(grav > 0) and np.all(derivative > 0)
            total += np.sum(weight*cosine*(grav+(2-m)*gn*derivative))
        output.append(total/(2*math.pi*base.G)*base.SI_TO_ESD)
    return np.asarray(output)


def analytic_newton(radius, mc, mh):
    answer = []
    for rad in np.atleast_1d(radius):
        if rad >= RH:
            gas = mh/(math.pi*rad**2)
        else:
            # Rationalized Rh-sqrt(Rh^2-r^2) for the small-radius limit.
            root = math.sqrt(RH*RH-rad*rad)
            gas = mh/(math.pi*RH*rad**2)*(rad*rad/(RH+root)+rad/2*math.acos(rad/RH))
        answer.append((mc/(math.pi*rad**2)+gas)*base.SI_TO_ESD)
    return np.array(answer)


def qvalue(residual, covariance):
    white = np.linalg.solve(np.linalg.cholesky(covariance), residual)
    return float(white@white)


def main():
    if sys.argv[1:] == ['freeze']:
        save_new(ROOT/(STEM+'_FROZEN.json'), {'files': hashes()})
        return
    assert not sys.argv[1:]
    assert json.loads((ROOT/(STEM+'_FROZEN.json')).read_text())['files'] == hashes()
    assert sha(INPUT) == 'bf4280d4d9cc40c87ef616e84d4cf6c02def610554d62d1ca4af0115be6e36d7'
    start = time.perf_counter()
    source = json.loads(INPUT.read_text())
    a0 = source['force_a0_si']
    controls = {}

    def check(name, discrepancy, tolerance):
        controls[name] = {'value': float(discrepancy), 'tolerance': tolerance,
                          'pass': bool(discrepancy <= tolerance)}

    test_r = RH*np.array([.01, .1, .3, .8, .99, 1., 1.01, 2., 10.])
    test_mc, test_mh = 1.5e10*base.MSUN, 1e10*base.MSUN
    numerical = projected(test_r, test_mc, test_mh, a0, newton=True)
    check('newton_truncated_gas', np.max(abs(numerical/analytic_newton(test_r, test_mc, test_mh)-1)), 1e-8)
    numerical_gas = projected(test_r, 0., test_mh, a0, newton=True)
    check('newton_gas_only', np.max(abs(numerical_gas/analytic_newton(test_r, 0., test_mh)-1)), 1e-8)
    cases = []
    for kind, shift in [('Color', .167), ('Sersic', .141)]:
        observed = source['splits'][kind]
        gbar = np.array(observed['gbar_primary'])
        for nominal_star in (1e10, 10**10.5, 1e11):
            nominal_mass = compact(nominal_star)*base.MSUN
            radius = np.sqrt(base.G*nominal_mass/gbar)
            low = projected(radius, nominal_mass, 0., a0)
            check(f'{kind}_{nominal_star}_compact', np.max(abs(low/base.esd(gbar, 'inherited_calibrated', a0)-1)), 1e-8)
            for delta in (0., shift):
                true_star = nominal_star*10**delta
                mc = compact(true_star)*base.MSUN
                for hot_fraction in (0., 1.):
                    mh = hot_fraction*true_star*base.MSUN
                    high = projected(radius, mc, mh, a0, 64)
                    fine = projected(radius, mc, mh, a0, 128)
                    case_id = f'{kind}_logM{math.log10(nominal_star):.1f}_delta{delta}_hot{hot_fraction}'
                    check(case_id+'_quadrature', np.max(abs(high/fine-1)), 1e-7)
                    if delta == hot_fraction == 0.:
                        check(case_id+'_zero_contrast', np.max(abs(high/low-1)), 1e-12)
                    cases.append({'id': case_id, 'kind': kind,
                        'nominal_stellar_msun': nominal_star, 'nominal_compact_msun': nominal_mass/base.MSUN,
                        'high_stellar_shift_dex': delta, 'high_hot_to_stellar': hot_fraction,
                        'low_hot_to_stellar': 0.,
                        'high_compact_msun': mc/base.MSUN, 'high_hot_msun': mh/base.MSUN,
                        'radius_kpc': (radius/base.PC/1000).tolist(),
                        'below_30kpc': (radius < 30000*base.PC).tolist(),
                        'above_300kpc': (radius > 300000*base.PC).tolist(),
                        'low_esd': low.tolist(), 'high_esd': high.tolist(),
                        'high_over_low': (high/low).tolist(),
                        'predicted_difference': (high-low).tolist()})
            equal = next(c.copy() for c in cases if c['kind'] == kind
                         and c['nominal_stellar_msun'] == nominal_star
                         and c['high_stellar_shift_dex'] == 0.
                         and c['high_hot_to_stellar'] == 1.)
            equal.update({'id': f'{kind}_logM{math.log10(nominal_star):.1f}_equal_hot',
                          'low_hot_to_stellar': 1., 'low_esd': equal['high_esd'][:],
                          'high_over_low': np.ones(7).tolist(),
                          'predicted_difference': np.zeros(7).tolist()})
            cases.append(equal)
    if not all(c['pass'] for c in controls.values()):
        save_new(ROOT/(STEM+'_CONTROL_FAILURE.json'), {'files': hashes(), 'controls': controls})
        raise RuntimeError('Frozen controls failed; no scores computed.')
    transform = np.concatenate([-np.eye(7), np.eye(7)], axis=1)
    for case in cases:
        data = source['splits'][case['kind']]
        observed = np.array(data['paired_esd'])
        covariance = np.array(data['paired_covariance'])
        prediction = np.array(case['low_esd']+case['high_esd'])
        residual = prediction-observed
        contrast_covariance = transform@covariance@transform.T
        case['paired_14_Q'] = qvalue(residual, covariance)
        case['contrast_7_Q'] = qvalue(transform@residual, contrast_covariance)
    result = {'files': hashes(), 'force_a0_si': a0, 'gas_radius_kpc': 100.,
              'controls': controls, 'cases': cases, 'new_force_fit_parameters': 0,
              'benchmark_choices_not_predictions': ['nominal mass', 'stellar shift', 'gas fraction',
                  'fixed truncated isothermal gas shape/radius', 'all added gas assigned to high type'],
              'interpretation': 'exposed fixed-benchmark sensitivity; not fitted gas evidence or catalogue likelihood',
              'seconds': time.perf_counter()-start}
    save_new(ROOT/(STEM+'_RESULT.json'), result)
    print(json.dumps({'checks': len(controls), 'seconds': result['seconds'],
          'cases': [{k: c[k] for k in ('id', 'paired_14_Q', 'contrast_7_Q')} for c in cases]}, indent=2))


if __name__ == '__main__':
    main()
