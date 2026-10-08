"""Necessary isolated bound; no solve, halo input, fit, or old-driver import."""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np


def main():
    start = time.perf_counter()
    base = Path(__file__).resolve().parent
    output = base / "COMPACT_DWARF_ISOLATED_BOUND_V001_RESULT.json"
    if output.exists():
        raise SystemExit("Existing result preserved; refusing overwrite/repeat")
    pc = 648000.0*149597870700.0/math.pi
    gm_sun, ell, a, ap = 1.3271244e20, 100*pc, 28*pc, 67*pc
    fraction = ap*ap/(ap*ap+a*a)
    controls = []

    def check(name, value, expected, tolerance, scale=1.0):
        error = abs(value-expected)/max(abs(expected), scale)
        controls.append(dict(name=name, error=float(error), tolerance=tolerance,
                             passed=bool(math.isfinite(error) and error <= tolerance)))

    quadratures = {}
    for count in (64, 128, 256):
        nodes, weights = np.polynomial.legendre.leggauss(count)
        quadratures[count] = ((nodes+1)/2, weights/2)
    kernel_rows = []
    for x in (.01, .1, 1., 10., 100.):
        values = []
        for count in (64,128):
            u, w = quadratures[count]
            values.append(float(2*np.dot(w, u*(-np.expm1(-x*u)))))
        closed = 1+2*((1+x)*math.exp(-x)-1)/(x*x)
        check(f"kernel_closed_{x}", values[-1], closed, 2e-10,
              scale=1e-20)
        check(f"kernel_refinement_{x}", values[0], values[1], 2e-10,
              scale=1e-20)
        check(f"kernel_interval_{x}", max(0., -values[-1], values[-1]-1),
              0., 2e-12)
        kernel_rows.append(dict(x=x, normalized_extra_force=values[-1]))
    u,w = quadratures[256]
    radius = u/(1-u)
    jac = 1/(1-u)**2
    check("Plummer_mean_radius",
          float(np.dot(w,3*radius**3/(1+radius*radius)**2.5*jac)), 2., 2e-9)
    check("Plummer_Newton_virial",
          float(np.dot(w,3*radius**4/(1+radius*radius)**4*jac)),
          3*math.pi/32, 2e-9)
    rap = ap/a
    check("Plummer_aperture",
          float(np.dot(w,2*rap*u/(1+(rap*u)**2)**2))*rap,
          fraction, 2e-9)
    rows = []
    for mass in (340.,1020.,3400.):
        gm = gm_sun*mass
        newton = 3*math.pi*gm/(32*a)
        extra = a*gm/(2*ell*ell)
        total = newton+extra
        required = (3700.0**2)*fraction-newton
        ceiling = math.sqrt(a*gm/(2*required)) if required > 0 else None
        if ceiling is not None:
            check(f"necessary_ceiling_inverse_{mass}",
                  math.sqrt((newton+a*gm/(2*ceiling*ceiling))/fraction),
                  3700.0, 2e-12)
        if rows:
            check(f"linear_mass_scaling_{mass}", total/rows[0]["total_second_moment_upper_m2_s2"],
                  mass/340., 2e-12)
        rows.append(dict(M_nominal_solar=mass, M_to_L_nominal=mass/340,
                         anomalous_force_upper_m_s2=gm/(4*ell*ell),
                         Newton_second_moment_m2_s2=newton,
                         extra_second_moment_upper_m2_s2=extra,
                         total_second_moment_upper_m2_s2=total,
                         global_LOS_upper_km_s=math.sqrt(total)/1000,
                         aperture_LOS_upper_km_s=math.sqrt(total/fraction)/1000,
                         necessary_ell_ceiling_pc_for_3p7_km_s=ceiling/pc if ceiling is not None else None))
    result = dict(status="CONTROLS_PASS" if all(c["passed"] for c in controls) else "FAILED",
                  scope="All regular outward isolated spherical fixed-state solutions satisfying the comparison hypotheses; necessary virial bound, not existence or a likelihood exclusion.",
                  inputs=dict(ell_pc=100,a_pc=28,aperture_pc=67,
                              nominal_luminosity=340,GM_nominal_sun=gm_sun,
                              external_field=0,source_dark_mass_used=False,
                              exposed_reference_sigma_km_s=3.7),
                  aperture_fraction=fraction, rows=rows, kernel_rows=kernel_rows,
                  controls=controls, control_count=len(controls),
                  custody={name:hashlib.sha256((base/name).read_bytes()).hexdigest()
                           for name in (Path(__file__).name,
                                        "COMPACT_DWARF_ISOLATED_BOUND_V001.md",
                                        "COMPACT_DWARF_FILTER_TEST_V001_RESULT.json")},
                  elapsed_seconds=time.perf_counter()-start)
    with output.open("x") as handle:
        json.dump(result,handle,indent=2,allow_nan=False)
        handle.write("\n")
    print(json.dumps({k:result[k] for k in ("status","rows","control_count","elapsed_seconds")},indent=2))
    if result["status"] != "CONTROLS_PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
