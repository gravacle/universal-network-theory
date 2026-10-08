"""Bounded arithmetic check; outputs are new evidence, never overwrites."""
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "STRUCTURED_NETWORK_CELL_WORK_V001_RESULT.json"
NOTE = ROOT / "STRUCTURED_NETWORK_CELL_WORK_V001.md"
if OUT.exists():
    raise SystemExit("Existing result preserved; do not rerun completed science")
started = time.perf_counter()
A0 = 1.0059833281731022e-10
GM_SUN = 1.32712440018e20
C = 299792458.0
TOL = 1e-7
checks = []


def check(name, value, limit=TOL):
    checks.append({"name": name, "error_or_violation": float(value),
                   "limit": limit, "pass": bool(math.isfinite(value) and value <= limit)})


def closed(L):
    t = L ** -3
    s = math.sqrt(1-t)
    # atanh(s)=log((1+s)/sqrt(t)); avoids 1-s cancellation.
    arct = math.log1p(s)-0.5*math.log(t)
    return (2*arct/3, 2*(arct-s)/3, s)


def quadrature(L, n):
    # Analytic inner monomials, independent outer integration. Break near u=1
    # at logarithmic spacings to resolve L^-3 without millions of nodes.
    z, w = np.polynomial.legendre.leggauss(n)
    s = math.sqrt(1-L**-3)
    cuts = sorted(set([0., s] + [1-10.**(-j) for j in range(1,11)
                               if 0 < 1-10.**(-j) < s]))
    qa = qi = 0.
    for lo, hi in zip(cuts[:-1], cuts[1:]):
        u = lo+(hi-lo)*(z+1)/2
        ww = (hi-lo)*w/2
        qa += float(np.dot(ww, (2/3)*u*u/(1-u*u)))
        qi += float(np.dot(ww, (2/3)*u**4/(1-u*u)))
    return 2*s/3+qa, 2*s**3/9+qi


geometries = []
for L in [10.,100.,1000.]:
    a, i, s = closed(L)
    coarse, fine = quadrature(L,128), quadrature(L,256)
    for k, label in enumerate(["potential", "binding_integral"]):
        ref = [a,i][k]
        check(f"L{L}_{label}_quadrature", abs(fine[k]-ref)/max(1.,abs(ref)))
        check(f"L{L}_{label}_refinement", abs(fine[k]-coarse[k])/max(1.,abs(ref)))
    h=1e-4
    di=(closed(L*math.exp(h))[1]-closed(L*math.exp(-h))[1])/(2*h)
    check(f"L{L}_dI_dlnL", abs(di-s))
    # E/(M B)=-2I/3; pressure in M B/V units is -d(E/MB)/dlnV.
    de=(-2/3)*(closed(L*math.exp(h/3))[1]-closed(L*math.exp(-h/3))[1])/(2*h)
    check(f"L{L}_pressure_work", abs(-de-2*s/9))
    geometries.append({"R_over_b":L,"A":a,"I":i,"s":s})

cases=[]
for mass in [1e7,1e9,1e11]:
    gm=GM_SUN*mass
    B=math.sqrt(gm*A0)
    rm=math.sqrt(gm/A0)
    for geometry in geometries:
        L,a,i,s=[geometry[k] for k in ["R_over_b","A","I","s"]]
        potential=B*a/C**2
        binding=-(2/3)*B*i/C**2
        pressure=(2/9)*B*s/C**2
        check(f"M{mass}_L{L}_binding_bound", max(0.,-binding-potential),0.)
        check(f"M{mass}_L{L}_nonpositive_binding", max(0.,binding),0.)
        check(f"M{mass}_L{L}_deep_source", max(0.,s/100-.01),0.)
        cases.append({"mass_nominal_solar":mass,"R_over_b":L,
                      "core_b_m":100*rm,"cell_R_m":L*100*rm,
                      "v_flat_m_per_s":math.sqrt(B),
                      "max_g_over_a0":s/100,
                      "potential_range_over_c2":potential,
                      "binding_over_Mc2":binding,
                      "fixed_core_pressure_over_rest_density":pressure,
                      "fixed_core_total_acceleration_source_over_rest":1+binding+3*pressure,
                      "comoving_total_acceleration_source_over_rest":1+binding})

result={"kind":"conditional_quasistatic_cell_work_not_covariant_cosmology",
        "a0_m_s2":A0,"GM_nominal_sun_m3_s2":GM_SUN,
        "physical_fits":0,"new_numerical_tolerance":TOL,
        "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "pre_execution_note_sha256":hashlib.sha256(NOTE.read_bytes()).hexdigest(),
        "geometries":geometries,"cases":cases,"checks":checks,
        "all_controls_pass":all(c["pass"] for c in checks),
        "elapsed_seconds":time.perf_counter()-started}
with OUT.open("x") as f:
    json.dump(result,f,indent=2,allow_nan=False)
    f.write("\n")
print(json.dumps({"output":str(OUT),"checks":len(checks),
                  "all_controls_pass":result["all_controls_pass"],
                  "max_potential_fraction":max(x["potential_range_over_c2"] for x in cases),
                  "most_negative_binding_fraction":min(x["binding_over_Mc2"] for x in cases),
                  "min_total_acceleration_source":min(x["fixed_core_total_acceleration_source_over_rest"] for x in cases),
                  "elapsed_seconds":result["elapsed_seconds"]},indent=2))
if not result["all_controls_pass"]:
    raise SystemExit(1)
