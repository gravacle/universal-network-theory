"""Frozen, no-fit unit/algebra test; does not import or rerun old drivers."""
from pathlib import Path
import hashlib
import json
import math
import time


def main():
    start = time.perf_counter()
    base = Path(__file__).resolve().parent
    target = base / "TRACE_REGULATOR_CLOCK_V001_RESULT.json"
    if target.exists():
        raise SystemExit("Refusing to overwrite an existing result")
    au = 149597870700.0
    pc = 648000.0 * au / math.pi
    light = 299792458.0
    year = 365.25 * 86400.0
    ell = 100.0 * pc
    lmin = 10.0 * au
    lgal = 1000.0 * pc
    tdiag = 1e10 * year
    qmax, qgal = ell / lmin, ell / lgal
    controls = []

    def check(name, actual, expected, tol, scale=1.0):
        err = abs(actual - expected) / max(abs(expected), scale)
        controls.append(dict(name=name, error=err, tolerance=tol,
                             passed=bool(err <= tol)))

    def cone(q):
        return (q*q + 2.0) / (q*q * (3.0*q*q + 4.0)**2)

    def group(q):
        return q * (3.0*q*q + 4.0) / math.sqrt(q*q + 2.0)

    def phase(q):
        return q * math.sqrt(q*q + 2.0)

    for beta in (1e-6, 0.1, 1.0, -1.0):
        a, b, d = -6.0-9.0*beta, 4.0+6.0*beta, -beta
        schur = a - b*b/(4.0*d)
        check(f"shift_schur_{beta}", schur,
              2.0*(2.0+3.0*beta)/beta, 2e-12)
        for alpha in (0.1, 1.0, 1.9):
            nratio = -2.0/alpha
            grad = 2.0+4.0*nratio+alpha*nratio*nratio
            check(f"lapse_schur_{beta}_{alpha}", grad,
                  -2.0*(2.0-alpha)/alpha, 2e-12)
    for q in (0.01, 0.1, 1.0, 10.0, 100.0):
        step = q * 1e-5
        def omega_dim(x):
            return x*x*math.sqrt(x*x+2.0)
        derivative = (omega_dim(q+step)-omega_dim(q-step))/(2*step)
        check(f"group_derivative_{q}", derivative, group(q), 2e-8,
              scale=1e-20)

    bmax = cone(qmax)
    beta_max = 2.0*bmax/(1.0-3.0*bmax)
    omega_gal = light/lgal * math.sqrt(bmax) * phase(qgal)
    response_yr = 1.0/(omega_gal*year)
    vg_gal = light*math.sqrt(bmax)*group(qgal)
    group_crossing_yr = lgal/(vg_gal*year)
    bmin_response = (lgal/(light*tdiag*phase(qgal)))**2
    beta_min_response = 2.0*bmin_response/(1.0-3.0*bmin_response)
    check("solar_group_cone_saturation", math.sqrt(bmax)*group(qmax),
          1.0, 2e-12)
    check("beta_B_inverse", beta_max/(2.0+3.0*beta_max), bmax,
          2e-12, scale=1e-100)
    check("inverse_frequency_units", response_yr,
          (lgal/light/year)/math.sqrt(bmax*qgal*qgal*(qgal*qgal+2.0)),
          2e-12)
    check("response_target_saturation",
          light/lgal*math.sqrt(bmin_response)*phase(qgal)*tdiag,
          1.0, 2e-12)
    low, high = 1e-8, qmax
    for _ in range(160):
        mid = math.sqrt(low*high)
        if cone(mid) > bmin_response:
            low = mid
        else:
            high = mid
    qcut = math.sqrt(low*high)
    check("cutoff_cone_root", cone(qcut), bmin_response, 2e-12,
          scale=1e-100)
    rows = []
    for beta in (-1.0, -0.5, 0.1, 1.0):
        rows.append(dict(beta=beta,
                         scalar_kinetic_coefficient=(2+3*beta)/beta,
                         homogeneous_H2_coefficient=1+1.5*beta,
                         Gcosmo_over_G=1/(1+1.5*beta)))
    custody = {}
    for name in (Path(__file__).name, "TRACE_REGULATOR_CLOCK_V001.md"):
        custody[name] = hashlib.sha256((base/name).read_bytes()).hexdigest()
    result = dict(
        status="CONTROLS_PASS" if all(c["passed"] for c in controls) else "FAILED",
        scope="Conditional zero-field linear dynamics; optional matter-cone bound, not a formation or observational exclusion theorem.",
        units=dict(AU_m=au, pc_m=pc, c_m_s=light, Julian_year_s=year),
        frozen_scales=dict(ell_pc=100, Lmin_AU=10, Lgal_pc=1000,
                           target_inverse_frequency_years=1e10, k_convention="1/L"),
        qmax=qmax, qgal=qgal, B_max_from_group_cone=bmax,
        beta_max_from_group_cone=beta_max,
        minimum_inverse_frequency_years=response_yr,
        maximum_group_speed_at_Lgal_m_s=vg_gal,
        minimum_group_crossing_years=group_crossing_yr,
        B_min_from_response_target=bmin_response,
        beta_min_from_response_target=beta_min_response,
        required_B_ratio=bmin_response/bmax,
        group_speed_at_Lmin_if_response_target_over_c=math.sqrt(bmin_response)*group(qmax),
        required_minimum_validity_length_pc=ell/qcut/pc,
        background_sign_examples=rows, controls=controls, custody=custody,
        elapsed_seconds=time.perf_counter()-start)
    with target.open("x") as handle:
        json.dump(result, handle, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({k: v for k,v in result.items()
                      if k not in ("units", "controls", "custody", "background_sign_examples")}, indent=2))
    print("controls", sum(c["passed"] for c in controls), "/", len(controls))


if __name__ == "__main__":
    main()
