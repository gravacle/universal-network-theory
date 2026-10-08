"""Fixed analytic necessary gates; no PDE solve, fit, or measured galaxy claim."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STEM = 'GRADIENT_RESPONSE_COMPATIBILITY_V001'
AU = 149597870700.0
PC = 648000 * AU / math.pi
GM = 1.32712440018e20
A0 = 1.0059833281731022e-10
GC = 3 * math.pi / 8 * A0
CENTURY = 36525 * 86400
MAS = math.pi / (180 * 3600 * 1000)
SEMIMAJOR = 9.53707032 * AU
ECC = .05415060
SOURCE_RADIUS_BOUND = 1e9
NA = math.sqrt(GM / SEMIMAJOR)


def rate_mas_cy(accel):
    return -accel * math.sqrt(1 - ECC**2) / NA * CENTURY / MAS


def plateau_error(ell):
    # Separate endpoint bounds also cover every R on the orbit.
    rlo, rhi = SEMIMAJOR * (1 - ECC), SEMIMAJOR * (1 + ECC)
    c = GM / (2 * ell**2)
    x, b = rhi / ell, c / GC
    cut = x * b
    eta = SOURCE_RADIUS_BOUND**2 / (3 * rlo**2)
    if cut >= 1:
        return 1.0
    return min(1.0, eta + x + x*x/4 + cut*(1.25 + math.log(1/cut)))


def main():
    inputs = dict(GMsolar=GM, a0=A0, gc=GC, AU=AU, pc=PC,
                  century_seconds=CENTURY, Saturn_a=SEMIMAJOR, Saturn_e=ECC,
                  source_radius_upper=SOURCE_RADIUS_BOUND,
                  historical_intervals_mas_cy={'C1': [1.2-5, 1.2+5],
                                               'C2': [.05-.20, .05+.20]},
                  illustration_lengths_pc=[1, 10, 100],
                  galaxy_scale_illustrations=[[1e7, 2], [1e9, 10], [1e11, 50]])
    checks = []
    def check(label, value):
        checks.append({'name': label, 'pass': bool(value)})
        assert value, label
    check('zero_acceleration_zero_precession', rate_mas_cy(0) == 0)
    check('inward_acceleration_retrograde', rate_mas_cy(1) < 0)
    check('parsec_AU_definition', math.isclose(PC / AU, 648000/math.pi))
    check('Kepler_n_times_a', math.isclose(NA, math.sqrt(GM/SEMIMAJOR**3)*SEMIMAJOR))
    intervals = []
    for name, (lo, hi) in inputs['historical_intervals_mas_cy'].items():
        ceiling = lo / rate_mas_cy(1)
        length = math.sqrt(GM / (2 * ceiling))
        check(name+'_negative_endpoint_backsubstitution',
              math.isclose(rate_mas_cy(ceiling), lo, rel_tol=1e-14))
        check(name+'_length_backsubstitution',
              math.isclose(GM/(2*length**2), ceiling, rel_tol=1e-14))
        intervals.append(dict(criterion=name, interval=[lo, hi],
                              conditional_monopole_ceiling_m_s2=ceiling,
                              constant_plateau_lower_ell_pc=length/PC,
                              plateau_relative_error_bound=plateau_error(length),
                              gaussian_sigma=False))
    lengths = []
    for pc in inputs['illustration_lengths_pc']:
        ell = pc * PC
        c = GM/(2*ell**2)
        eps = plateau_error(ell)
        rate = rate_mas_cy(c)
        lengths.append(dict(ell_pc=pc, inward_plateau_m_s2=c,
                            precession_mas_cy=rate,
                            force_relative_error_bound=eps,
                            precession_relative_error_bound=eps/ECC,
                            precession_interval_mas_cy=sorted([rate*(1-eps/ECC),
                                                             rate*(1+eps/ECC)]),
                            isolated_exterior_tracer_fraction_bound_at_point1pc=.1**2/(2*pc**2)))
        check('finite_control_'+str(pc), 0 <= eps < 1 and eps/ECC < 1)
    galaxies = []
    for mass, rkpc in inputs['galaxy_scale_illustrations']:
        gm, radius = GM*mass, rkpc*1000*PC
        rm = math.sqrt(gm/A0)
        gn = gm/radius**2
        target = math.sqrt(gm*A0)/radius
        delta = target-gn
        check('positive_illustrative_enhancement_'+str(mass), delta > 0)
        upper = math.sqrt(gm/(2*delta))
        check('amplitude_bound_backsubstitution_'+str(mass),
              math.isclose(gm/(2*upper**2), delta, rel_tol=1e-14))
        galaxies.append(dict(illustrative_baryon_mass_solar=mass, radius_kpc=rkpc,
                             rM_over_R=rm/radius, gN=gn, adopted_target_total=target,
                             adopted_enhancement=delta, necessary_upper_ell_pc=upper/PC,
                             measured_galaxy=False))
    source = [Path(__file__), ROOT/(STEM+'.md')]
    output = dict(inputs=inputs, custody={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                          for p in source},
                  checks=checks, all_pass=all(c['pass'] for c in checks),
                  historical_monopole_gate=intervals,
                  length_illustrations=lengths, galaxy_scale_illustrations=galaxies,
                  scope='Isolated static analytic necessary gates only; external-field and cosmology unresolved.')
    with (ROOT/(STEM+'_RESULT.json')).open('x') as f:
        json.dump(output, f, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
