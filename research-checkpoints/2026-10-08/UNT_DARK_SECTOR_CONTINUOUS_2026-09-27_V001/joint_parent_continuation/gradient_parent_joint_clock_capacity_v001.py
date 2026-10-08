"""New shared-clock diagnostic; retained existing physics, no refit or rerun."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np

HERE = Path(__file__).resolve().parent
STEM = "GRADIENT_PARENT_JOINT_CLOCK_CAPACITY_V001"


def capacity(alpha):
    return alpha**6 / 27 if alpha <= 1 else alpha**4 / 36 + alpha**2 / 18 - 5 / 108


def modes(beta, theta, nodes, steps):
    z, weights = np.polynomial.legendre.leggauss(nodes)
    s, w = (z + 1) / 2, weights / 2
    x, v = np.zeros(nodes), np.zeros(nodes)
    dt = theta / steps

    def accel(q):
        return s * beta - s * s * q - q**3

    for _ in range(steps):
        a1 = accel(x)
        q2, v2 = x + dt * v / 2, v + dt * a1 / 2
        a2 = accel(q2)
        q3, v3 = x + dt * v2 / 2, v + dt * a2 / 2
        a3 = accel(q3)
        q4, v4 = x + dt * v3, v + dt * a3
        a4 = accel(q4)
        x = x + dt * (v + 2 * v2 + 2 * v3 + v4) / 6
        v = v + dt * (a1 + 2 * a2 + 2 * a3 + a4) / 6
    mu = 1 - 2 * np.dot(w, s * s * x) / beta
    e0 = beta * beta / 2
    energy = e0 + np.dot(2 * s * w, v * v / 2 + s * s * x * x / 2 + x**4 / 4 - s * beta * x)
    return s, x, v, float(mu), float((energy - e0) / e0)


def static(beta, nodes):
    z, weights = np.polynomial.legendre.leggauss(nodes)
    s, w = (z + 1) / 2, weights / 2
    low = np.zeros(nodes)
    high = np.cbrt(s * beta)
    for _ in range(90):
        mid = (low + high) / 2
        above = s * s * mid + mid**3 > s * beta
        high = np.where(above, mid, high)
        low = np.where(above, low, mid)
    x = (low + high) / 2
    residual = np.max(np.abs(s * s * x + x**3 - s * beta) / (s * beta))
    return float(1 - 2 * np.dot(w, s * s * x) / beta), float(residual)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if not args.execute:
        parser.error("--execute is required")
    result_path = HERE / (STEM + "_RESULT.json")
    report_path = HERE / (STEM + "_RESULT.md")
    if result_path.exists() or report_path.exists():
        raise FileExistsError("Existing evidence will not be overwritten")
    started = time.perf_counter()
    pc = 648000 * 149597870700 / math.pi
    year = 365.25 * 86400
    H = 70000 / (1e6 * pc)
    c = 299792458.0
    a0 = 1.0059833281731022e-10
    gc = 3 * math.pi * a0 / 8
    chi, target = 3.0, 0.7
    factor = (2 / 3) * (gc / (c * H))**2
    # For alpha>1, the ceiling is quadratic in z=alpha^2.
    # Determine branch from the normalized ceiling at alpha=1 first.
    if target <= factor / 27:
        alpha = (27 * target / factor)**(1 / 6)
    else:
        z = -1 + math.sqrt(8 / 3 + 36 * target / factor)
        alpha = math.sqrt(z)
    omega = chi * H / alpha
    checks = []

    def check(label, error, threshold):
        checks.append(dict(label=label, error=float(error), threshold=float(threshold), passed=bool(error <= threshold)))

    check("budget_ceiling_backsubstitution", abs(factor * capacity(alpha) / target - 1), 1e-13)
    cases = []
    for beta in (0.01, 0.1, 1.0):
        sm96, sr96 = static(beta, 96)
        sm192, sr192 = static(beta, 192)
        check(f"static_spectral_{beta}", abs(sm96 - sm192), 1e-8)
        check(f"static_cubic_{beta}", max(sr96, sr192), 1e-12)
        for age in (1, 5, 10):
            theta = omega * age * 1e9 * year
            readings = []
            # Match spectral rules at each age; change time independently on96.
            for nodes, steps in ((48, 512), (96, 256), (96, 512), (96, 1024), (192, 1024)):
                s, x, v, mu, drift = modes(beta, theta, nodes, steps)
                readings.append(dict(nodes=nodes, steps=steps, mu_age=mu, complete_energy_relative_drift=drift))
                check(f"energy_{beta}_{age}_{nodes}_{steps}", abs(drift), 1e-8)
                if nodes == 96:
                    if steps == 256:
                        coarse = (x, v, mu)
                    elif steps == 512:
                        middle = (x, v, mu)
                    else:
                        fine = (x, v, mu)
            for label, old, new in (("coarse_middle", coarse, middle), ("middle_fine", middle, fine)):
                check(f"time_mu_{beta}_{age}_{label}", abs(old[2] - new[2]), 1e-8)
                # beta is the fixed amplitude normalization, not an outcome floor.
                check(f"time_state_{beta}_{age}_{label}", max(float(np.max(np.abs(old[0] - new[0]))), float(np.max(np.abs(old[1] - new[1])))) / beta, 1e-8)
            check(f"spectral_48_96_{beta}_{age}", abs(readings[0]["mu_age"] - readings[2]["mu_age"]), 1e-8)
            check(f"spectral_96_192_{beta}_{age}", abs(readings[3]["mu_age"] - readings[4]["mu_age"]), 1e-8)
            response = 1-readings[-1]["mu_age"]
            check(f"independent_conservative_response_bound_{beta}_{age}", max(0.0, -response, response-theta*theta/4), 1e-10)
            cases.append(dict(beta=beta, source_g_over_a0=beta * gc / a0, age_Gyr=age, theta=theta,
                              mu_age=readings[-1]["mu_age"], mu_static=sm192,
                              all_slower_clock_response_upper_bound=theta*theta/4,
                              age_response_over_static_response=(1-readings[-1]["mu_age"])/(1-sm192), readings=readings))
    # Small theta avoids cancellation in the exact independent linear control.
    for age in (1, 5, 10):
        theta = omega * age * 1e9 * year
        exact = 2 * (math.sin(theta) / theta + (math.cos(theta) - 1) / theta**2)
        *_, measured, _ = modes(1e-7, theta, 96, 1024)
        check(f"weak_source_exact_linear_{age}", abs(measured - exact), 1e-10)
    inputs = [Path(__file__), HERE / (STEM + ".md"), HERE / "GRADIENT_PARENT_CLOCK_SCREEN_V001.md",
              HERE / "EXPLICIT_MODE_COSMOLOGY_PATHWAY.md", HERE / "LINEAR_SOURCE_GALAXY_REFERENCE_V001.md"]
    result = dict(custody={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
                  fixed_inputs=dict(a0_m_s2=a0, H_illustration_km_s_Mpc=70, H_s_inverse=H, chi=chi,
                                    target_slow_potential_fraction=target, c_light_m_s=c, pc_m=pc, year_s=year),
                  shared_clock=dict(gc_m_s2=gc, density_factor=factor, alpha_min=alpha,
                                    fastest_budget_compatible_omega_s_inverse=omega,
                                    inverse_omega_Gyr=1/(omega*year*1e9), omega_over_H=omega/H,
                                    corresponding_mode_speed_at_100pc_m_s=100*pc*omega),
                  cases=cases, checks=checks, numerical_all_pass=all(x["passed"] for x in checks),
                  elapsed_seconds=time.perf_counter()-started,
                  scope="Declared constant-inertia slow-curvature budget and local zero-state source step. No cosmological occupation, spatial galaxy solve, observational fit, or global UNT exclusion.")
    with result_path.open("x") as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write("\n")
    lines = ["# Shared-clock application result V001", "", result["scope"], "",
             f"Numerical controls: {'PASS' if result['numerical_all_pass'] else 'FAIL'} ({len(checks)}).",
             f"Fastest budget-compatible omega/H: {omega/H:.9g}; inverse frequency: {1/(omega*year*1e9):.9g}Gyr.", "",
             "| g/gc | Age Gyr | D/g actual | D/g static | Actual/static polarization |", "|---|---:|---:|---:|---:|"]
    for row in cases:
        lines.append(f"| {row['beta']} | {row['age_Gyr']} | {row['mu_age']:.9g} | {row['mu_static']:.9g} | {row['age_response_over_static_response']:.9g} |")
    lines += ["", "The assumed slow potential budget is a ceiling, not a formed population. This exact local step preparation retains conservative excitation. Its response must not be presented as an observed galaxy or a theorem covering every state or source history.", ""]
    with report_path.open("x") as f:
        f.write("\n".join(lines))
    print(json.dumps(dict(numerical_all_pass=result["numerical_all_pass"], checks=len(checks), elapsed_seconds=result["elapsed_seconds"], shared_clock=result["shared_clock"], cases=[{k:r[k] for k in ("beta","age_Gyr","mu_age","mu_static","age_response_over_static_response")} for r in cases]), indent=2))


if __name__ == "__main__":
    main()
