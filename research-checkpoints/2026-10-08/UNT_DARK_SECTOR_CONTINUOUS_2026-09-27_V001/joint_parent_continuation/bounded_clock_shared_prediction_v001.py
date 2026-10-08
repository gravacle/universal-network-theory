"""Small deterministic arithmetic check of the frozen bounded-clock note.

No astronomical fit, native formation, full perturbation or observational test.
Uses only the standard library; one process and no external data.
"""
from pathlib import Path
import cmath
import hashlib
import json
import math
import resource
import time


BASE = Path(__file__).resolve().parent
PROTOCOL = BASE / 'BOUNDED_CLOCK_SHARED_PREDICTION_V001.md'
OUTPUT = BASE / 'BOUNDED_CLOCK_SHARED_PREDICTION_V001_RESULT.json'
EPSILONS = (1e-2, 1e-4, 1e-6, 1e-8)
CHARGES = (0., 1e-8, 1e-4, .01, .1, 1., 10., 1e4, 1e12, 1e30)


def pressure_excess_numerator(s):
    # Series avoids subtraction of two O(s) quantities when their
    # difference is O(s^2). Valid for real or complex s near zero.
    if abs(s) < .01:
        return sum((-1)**j * (j-1)/j * s**j for j in range(2, 20))
    return (cmath.log(1+s) if isinstance(s, complex) else math.log1p(s)) - s/(1+s)


def quantities(eps, s):
    D = 1/eps - math.log1p(1/eps)
    q = cmath.sqrt(1+eps*s/(1+s)) if isinstance(s, complex) else math.sqrt(1+eps*s/(1+s))
    d = 2*q*s/(eps*D)
    p = pressure_excess_numerator(s)/D
    r = q*d-p
    cs2 = eps*s/(2+(4+3*eps)*s+2*(1+eps)*s*s)
    return q, d, p, r, cs2


def charge_root(eps, d):
    if d == 0:
        return 0.
    D = 1/eps - math.log1p(1/eps)
    hi = d*eps*D/2
    lo = hi/math.sqrt(1+eps)
    for _ in range(100):
        mid = (lo+hi)/2
        if mid == lo or mid == hi:
            break
        if quantities(eps, mid)[1] > d:
            hi = mid
        else:
            lo = mid
    return (lo+hi)/2


def main():
    started = time.monotonic()
    controls, rows = [], []

    def check(name, error, tolerance):
        controls.append(dict(name=name, error=float(error), tolerance=tolerance,
                             passed=bool(math.isfinite(error) and error <= tolerance)))

    c = 299792458.
    mpc = 3.085677581491367e22
    G = 6.67430e-11
    solar_mass = 1.98847e30
    Hv = 60.06409376657703*1000/mpc
    a0 = 1.2e-10
    KB = 1.
    rM = math.sqrt(G*1e11*solar_mass/a0)
    for eps in EPSILONS:
        D = 1/eps - math.log1p(1/eps)
        rootL = math.sqrt(1+eps)
        delta = eps/(rootL+1)
        S = 4/(eps*eps*D)
        maximum = delta/(3*rootL+1)
        s_max = 1/rootL
        check(f'{eps}: maximum', abs(quantities(eps, s_max)[4]/maximum-1), 2e-12)
        check(f'{eps}: eps_over_8_bound', max(0., maximum/(eps/8)-1), 2e-12)
        points = []
        for target_d in CHARGES:
            s = charge_root(eps, target_d)
            q, d, p, r, cs2 = quantities(eps, s)
            check(f'{eps}:{target_d}: charge', abs(d-target_d)/max(target_d, 1e-300), 2e-13)
            check(f'{eps}:{target_d}: excess_lower', max(0., d-r)/max(d, 1e-300), 2e-12)
            check(f'{eps}:{target_d}: excess_upper', max(0., r-rootL*d)/max(d, 1e-300), 2e-12)
            check(f'{eps}:{target_d}: pressure_bounds', max(0., -p, p-delta*d)/max(d, 1e-300), 2e-12)
            check(f'{eps}:{target_d}: sound_bounds', max(0., -cs2, cs2-maximum)/max(maximum, 1e-300), 2e-12)
            check(f'{eps}:{target_d}: Legendre', abs(r+p-q*d)/max(d, 1.), 2e-12)
            points.append(dict(d=target_d, s=s, Q_over_Q0=q,
                               pressure_excess_over_A=p, density_excess_over_A=r,
                               excess_to_conserved_dust=(r/d if d else 1.),
                               total_w=(-1+p)/(1+r), cs_ad_squared=cs2))
        for s in (1e-3, .1, 1., 10., 1e3):
            q, d, p, r, cs2 = quantities(eps, s)
            u = eps*s/(1+s)
            q_u = math.sqrt(1+u)
            fp = 2*q_u*u/(eps*(eps-u))
            independent_d = fp/D
            independent_p = (-u/eps-math.log1p(-u/eps))/D
            independent_r = q_u*independent_d-independent_p
            check(f'{eps}:{s}: independent_u_rho', abs(independent_r-r)/max(abs(r), 1e-300), 1e-10)
            h = 1e-24
            _, _, p_complex, r_complex, _ = quantities(eps, s+1j*h)
            derivative_ratio = p_complex.imag/r_complex.imag
            check(f'{eps}:{s}: complex_pressure_derivative', abs(derivative_ratio/cs2-1), 1e-10)
        Lmu = c/Hv*math.sqrt((2-KB)/(3*S))
        RC = (rM*Lmu*Lmu)**(1/3)
        rows.append(dict(eps=eps, D=D, S=S, max_cs_ad_squared=maximum,
                         uniform_dust_relative_upper=delta,
                         max_adiabatic_speed_km_s=c*math.sqrt(maximum)/1000,
                         L_mu_Mpc=Lmu/mpc, R_C_scale_kpc=RC/mpc*1000,
                         exact_product_S_max_cs_squared=S*maximum,
                         charge_samples=points))
    result = dict(
        protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        scope='Algebra and illustrative dimensions only; no fit, full stability or observational score.',
        fixed_dimensions=dict(c_m_s=c, G_SI=G, solar_mass_kg=solar_mass,
                              M_b_solar_masses=1e11, Hv_km_s_Mpc=60.06409376657703,
                              a0_m_s2=a0, KB=KB, rM_kpc=rM/mpc*1000),
        rows=rows, controls=controls,
        all_controls_passed=all(x['passed'] for x in controls),
        elapsed_seconds=time.monotonic()-started,
        max_self_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    )
    # Exclusive creation preserves earlier evidence if mistakenly re-run.
    with OUTPUT.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps(dict(all_controls_passed=result['all_controls_passed'],
                          failed=[x for x in controls if not x['passed']],
                          rows=[{k:v for k,v in x.items() if k != 'charge_samples'} for x in rows],
                          elapsed_seconds=result['elapsed_seconds'],
                          max_self_RSS_bytes=result['max_self_RSS_bytes']), indent=2))
    if not result['all_controls_passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
