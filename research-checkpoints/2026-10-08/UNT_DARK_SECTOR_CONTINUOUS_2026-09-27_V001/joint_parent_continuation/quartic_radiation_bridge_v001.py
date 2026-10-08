"""Prospective arithmetic for the proposed radiation-like phase-clock repair.

Reuse the ALREADY DERIVED quartic EOS, not a new cosmological trajectory.
For each completed bounded-clock development normalization, replace only
P(Q) by the preserved quartic P=A(q^4-2q^2). Calibrate its charge to the
SAME present clock excess exactly; do not fit early radiation independently.
Compare its forced a^-4 coefficient to ordinary radiation at3 and.03MeV,
using the already exposed ideal thermal/entropy assumptions. Separately
solve the charge that would compensate the specified rG at each endpoint,
and report its implied present clock excess. This inverse arithmetic is
calibration, NOT a native prediction or a single fit across both epochs.

Controls before execution: exact present-density and charge inversion
relative residuals <=2e-12; finite large-charge asymptotic agreement <=1e-8
at a=1e-8 and1e-10. No observational acceptance threshold or new likelihood.
Sources pinned by hashes; exclusive output. Standard library, one worker.
"""
from pathlib import Path
import hashlib
import json
import math
import resource
import time

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / 'QUARTIC_RADIATION_BRIDGE_V001_RESULT.json'


def solve_u(charge):
    lo, hi = 0.0, max(1.0, charge**(2/3))
    while hi * math.sqrt(1 + hi) < charge:
        hi *= 2
    for _ in range(160):
        mid = (lo + hi) / 2
        if mid in (lo, hi):
            break
        if mid * math.sqrt(1 + mid) < charge:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    start = time.monotonic()
    c, G, kb, h = 299792458.0, 6.67430e-11, 1.380649e-23, 6.62607015e-34
    hbar, ev = h/(2*math.pi), 1.602176634e-19
    h0 = 73600.0 / 3.085677581491367e22
    t0, gs0 = 2.7255, 43/11
    ge0 = 2 + 5.25*(4/11)**(4/3)
    histories, controls = [], []
    for label, rG, oa, oc in (
        ('original_development', .25, .7, .2875),
        ('standard_thermal_calibrated_benchmark', .98, .7, .251),
    ):
        critical = 3*h0*h0*c*c/(8*math.pi*G*rG)
        ratio = oc/oa
        u0 = 2*ratio/(4 + math.sqrt(16 + 12*ratio))
        charge = u0*math.sqrt(1 + u0)
        rad_coefficient = 3*oa*charge**(4/3)
        controls.append(abs(oa*(4*u0+3*u0*u0)/oc-1) <= 2e-12)
        asymptotic_checks = []
        for a in (1e-8, 1e-10):
            target = charge/a**3
            u = solve_u(target)
            density = oa*(1+4*u+3*u*u)
            residual = abs(u*math.sqrt(1+u)/target-1)
            asymptotic_error = abs(density*a**4/rad_coefficient-1)
            controls.extend((residual <= 2e-12, asymptotic_error <= 1e-8))
            asymptotic_checks.append(dict(a=a, charge_relative_error=residual,
                                          asymptotic_relative_error=asymptotic_error))
        thermal = []
        for tmev, ge, gs in ((3., 10.75, 10.75), (.03, ge0, gs0)):
            kT = tmev*1e6*ev
            a = kb*t0/kT*(gs0/gs)**(1/3)
            radiation = math.pi**2*ge*kT**4/(30*hbar**3*c**3)
            extra = critical*rad_coefficient/a**4
            wanted_ratio = 1/rG-1
            wanted_coeff = wanted_ratio*radiation*a**4/critical
            wanted_charge = (wanted_coeff/(3*oa))**.75
            wanted_u = solve_u(wanted_charge)
            wanted_oc = oa*(4*wanted_u+3*wanted_u*wanted_u)
            controls.append(abs(wanted_u*math.sqrt(1+wanted_u)/wanted_charge-1) <= 2e-12)
            thermal.append(dict(T_MeV=tmev, g_energy=ge, g_entropy=gs, a=a,
                                extra_over_ordinary_radiation=extra/radiation,
                                H_over_reference=math.sqrt(rG*(1+extra/radiation)),
                                required_extra_over_ordinary=wanted_ratio,
                                inverse_required_charge=wanted_charge,
                                inverse_implied_present_clock_excess=wanted_oc,
                                inverse_fraction_of_declared_excess=wanted_oc/oc))
        histories.append(dict(label=label, rG=rG, omega_A=oa, omega_excess_now=oc,
                              quartic_u_now=u0, conserved_charge=charge,
                              asymptotic_radiation_coefficient=rad_coefficient,
                              asymptotic_controls=asymptotic_checks, thermal_rows=thermal))
    paths = [BASE/'BOUNDED_CLOCK_SHARED_PREDICTION_V001.md',
             BASE/'SHARED_GRAVITY_NORMALIZATION_V001_RESULT.json',
             BASE/'CHARGED_CLOCK_BBN_CALIBRATED_V001_RESULT.json']
    result = dict(scope='Conditional arithmetic of a specified EOS change; not a native radiation mechanism or abundance computation.',
                  self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  input_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                  histories=histories, controls_count=len(controls), all_controls_passed=all(controls),
                  elapsed_seconds=time.monotonic()-start,
                  peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUTPUT.open('x') as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps(result, indent=2))
    if not all(controls):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
