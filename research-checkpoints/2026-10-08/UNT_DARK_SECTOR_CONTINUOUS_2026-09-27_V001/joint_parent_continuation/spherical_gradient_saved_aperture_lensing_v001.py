"""New finite-aperture common-light prediction using sealed saved fields."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np

HERE = Path(__file__).resolve().parent
STEM = "SPHERICAL_GRADIENT_SAVED_APERTURE_LENSING_V001"
CAP, IMPACTS = 150.0, (5.0, 10.0, 20.0, 50.0)
C = 299792458.0
A0 = 1.0059833281731022e-10
ARCSEC = 180 * 3600 / math.pi


def integrate(r, values, b, nodes, manufactured=None):
    knots = r[(r > b) & (r < CAP)]
    cuts = np.concatenate(([0.0], np.arccosh(knots / b), [math.acosh(CAP / b)]))
    z, weights = np.polynomial.legendre.leggauss(nodes)
    mid, half = (cuts[1:] + cuts[:-1]) / 2, (cuts[1:] - cuts[:-1]) / 2
    u = mid[:, None] + half[:, None] * z
    radius = b * np.cosh(u)
    if manufactured is None:
        field = np.interp(np.log(radius), np.log(r), values)
    else:
        field = manufactured(radius)
    return float(np.sum(half[:, None] * weights * field))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    if not parser.parse_args().execute:
        parser.error("--execute is required")
    output = HERE / (STEM + "_RESULT.json")
    report = HERE / (STEM + "_RESULT.md")
    if output.exists() or report.exists():
        raise FileExistsError("Existing evidence will not be overwritten")
    began = time.perf_counter()
    prior_path = HERE / "SPHERICAL_GRADIENT_FORWARD_V001_RESULT.json"
    if hashlib.sha256(prior_path.read_bytes()).hexdigest() != "657fa06ac5fe875a6ccef405b8061c42eb63f4715ed7878ee16f6836e10682f7":
        raise ValueError("Sealed aggregate digest mismatch")
    prior = json.loads(prior_path.read_text())
    if not prior["all_numerical_controls_pass"] or len(prior["cases"]) != 12:
        raise ValueError("Prior state census/qualification failed")
    custody = {prior_path.name: hashlib.sha256(prior_path.read_bytes()).hexdigest()}
    for name in (Path(__file__).name, STEM + ".md", "SPHERICAL_GRADIENT_COMMON_LENSING_CLOSURE_V001.md"):
        custody[name] = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    checks, rows = [], []

    def check(label, error, threshold):
        checks.append(dict(label=label, error=float(error), threshold=float(threshold), passed=bool(error <= threshold)))

    for old in prior["cases"]:
        p = HERE / old["filename"]
        blob = p.read_bytes()
        digest = hashlib.sha256(blob).hexdigest()
        if digest != old["sha256"]:
            raise ValueError("Saved state seal mismatch: " + p.name)
        custody[p.name] = digest
        case = json.loads(blob)
        if not case["qualified_newton"] or case["status"] != "converged":
            raise ValueError("Saved state not qualified: " + p.name)
        r = np.array(case["r"])
        if not (r[0] < min(IMPACTS) and r[-1] > CAP and np.all(np.diff(r) > 0)):
            raise ValueError("Saved support does not enclose path")
        w = np.array(case["spectral_weights"])
        full_u, local_u = np.array(case["mode_u"]), np.array(case["local_u"])
        # Saved mode axes are (Ns,Nr); authenticate shape before projection.
        if full_u.shape != (len(w), len(r)) or local_u.shape != full_u.shape:
            raise ValueError("Saved field dimensions mismatch")
        source = np.array(case["source_over_r"])
        full = r * (source + w @ full_u)
        local = r * (source + w @ local_u)
        delta = r * (w @ (full_u - local_u))
        label = str(old["mass_Msun"]) + "_" + str(old["index"])
        check("positive_total_" + label, float(max(0, -np.min(full), -np.min(local))), 0)
        check("matched_difference_" + label, float(np.max(np.abs((full-local)-delta) / np.maximum(full, local))), 1e-12)
        for k, read_r in enumerate(case["readouts"]["r"]):
            got = float(np.interp(math.log(read_r), np.log(r), full))
            expected = case["readouts"]["g_full_over_a0"][k]
            check("saved_readout_" + label + "_" + str(read_r), abs(got-expected)/abs(expected), 1e-11)
        rM, lam2 = case["rM_metres"], case["lambda_squared"]
        for b in IMPACTS:
            vals = {}
            for order in (8, 16):
                ints = [integrate(r, f, b, order) for f in (full, local, delta)]
                angles = [4*b*A0*rM*val/C**2 for val in ints]
                vals[order] = (*angles, -b*b*ints[2]/lam2)
            lo, hi = vals[8], vals[16]
            check("quadrature_gradient_" + label + "_" + str(b), abs(lo[3]-hi[3]), 1e-10)
            for idx, tag in ((0,"full"),(1,"local")):
                check("quadrature_" + tag + "_" + label + "_" + str(b), abs(lo[idx]-hi[idx])/abs(hi[idx]), 1e-10)
            zz = math.sqrt(CAP*CAP-b*b)
            newton = 4*A0*rM*b*zz/(C**2*(b*b+0.01)*math.sqrt(CAP*CAP+0.01))
            rows.append(dict(mass_Msun=old["mass_Msun"], case_index=old["index"], impact_over_rM=b,
                             impact_metres=b*rM, path_cap_over_rM=CAP,
                             alpha_full_rad=hi[0], alpha_local_rad=hi[1], delta_alpha_rad=hi[2],
                             alpha_full_arcsec=hi[0]*ARCSEC, delta_alpha_arcsec=hi[2]*ARCSEC,
                             alpha_local_arcsec=hi[1]*ARCSEC,
                             newton_same_Plummer_rad=newton, full_over_Newtonian=hi[0]/newton,
                             delta_over_full=hi[2]/hi[0], A_lens=hi[3],
                             first_gradient_aperture_reference=zz/CAP,
                             weak_metric_scale_a0_rM_over_c2=A0*rM/C**2))
            # Independent manufactured integral, evaluated directly, no field interpolation.
            if old["index"] == 2:
                pure1 = integrate(r, None, b, 16, lambda rr: 1/rr)
                pure2 = integrate(r, None, b, 16, lambda rr: 1/rr**2)
                exact1 = math.atan(zz/b)/b
                exact2 = zz/(b*b*CAP)
                check("manufactured_1r_" + label + "_" + str(b), abs(pure1/exact1-1), 1e-11)
                check("manufactured_1r2_" + label + "_" + str(b), abs(pure2/exact2-1), 1e-11)
                plummer = integrate(r, None, b, 16, lambda rr: rr/(rr*rr+0.01)**1.5)
                exactp = zz/((b*b+0.01)*math.sqrt(CAP*CAP+0.01))
                check("manufactured_Plummer_" + label + "_" + str(b), abs(plummer/exactp-1), 1e-11)
    comparisons = []
    for mass in sorted(set(row["mass_Msun"] for row in rows)):
        for b in IMPACTS:
            selected = {row["case_index"]:row for row in rows if row["mass_Msun"] == mass and row["impact_over_rM"] == b}
            for tag, a, z in (("mesh",0,1),("spectrum",1,2),("boundary",2,3)):
                dif = abs(selected[a]["A_lens"]-selected[z]["A_lens"])
                check(f"{tag}_A_{mass}_{b}",dif,0.02)
                change = max(abs(selected[a][k]-selected[z][k])/abs(selected[z][k]) for k in ("alpha_full_rad","alpha_local_rad"))
                check(f"{tag}_angle_{mass}_{b}",change,1e-3)
                comparisons.append(dict(mass_Msun=mass,impact_over_rM=b,comparison=tag,A_change=dif,total_angle_relative_change=change))
    result = dict(custody=custody,inputs=dict(c_m_s=C,a0_m_s2=A0,path_cap_over_rM=CAP,impact_over_rM=list(IMPACTS)),
                  rows=rows,comparisons=comparisons,checks=checks,numerical_all_pass=all(c["passed"] for c in checks),
                  elapsed_seconds=time.perf_counter()-began,
                  scope="Common leading-weak-metric light projection of all twelve saved prepared gradient spheres; finite path aperture, no PDE rerun, observed lensing fit, exact zero-slip or infinite-tail claim.")
    with output.open("x") as f:
        json.dump(result,f,indent=2,allow_nan=False)
        f.write("\n")
    lines = ["# Same-parent finite-aperture lensing prediction V001","",result["scope"],"",
             f"Numerical controls: {'PASS' if result['numerical_all_pass'] else 'FAIL'} ({len(checks)}). All48 projections and36 prior-grid comparisons retained.","",
             "| Ordinary mass Msun | b/rM | Full angle arcsec | Full / same Plummer baryons | Gradient change % | A_lens |",
             "|---:|---:|---:|---:|---:|---:|"]
    for row in rows:
        if row["case_index"] == 3:
            lines.append(f"| {row['mass_Msun']:.0e} | {row['impact_over_rM']:.0f} | {row['alpha_full_arcsec']:.8g} | {row['full_over_Newtonian']:.8g} | {100*row['delta_over_full']:.8g} | {row['A_lens']:.8g} |")
    lines += ["","Rows show the finest boundary-extension case; every mesh/spectrum/domain arm is retained in JSON. These are prepared-source predictions. The conditional shared metric gives light enhancement without adding an independent halo; an observed joint comparison and the native common cosmological realization remain open.",""]
    with report.open("x") as f:
        f.write("\n".join(lines))
    print(json.dumps(dict(numerical_all_pass=result["numerical_all_pass"],controls=len(checks),rows=len(rows),elapsed_seconds=result["elapsed_seconds"],finest_rows=[r for r in rows if r["case_index"]==3]),indent=2))


if __name__ == "__main__":
    main()
