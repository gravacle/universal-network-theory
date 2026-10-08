"""Saved-only independent A/B audit. No producer import, propagation or eigensolve."""
import os
import sys

sys.dont_write_bytecode = True
for audit_thread_key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
                         "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[audit_thread_key] = "1"

import argparse
import hashlib
import json
import math
from pathlib import Path
import resource
import time

import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = Path(__file__).resolve()
RESULT = HERE / "NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_RESULTS.json"
FREEZE = HERE / "NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_FROZEN.json"
OUTPUT = HERE / "NATIVE_AUTONOMOUS_VOLUME_FORMATION_SAVED_AUDIT_V001.json"
RESULT_SHA = "bc35b592f5547e1f5fc566411ec7e8f7175776d20569fbccf0ae3e6457e74fc1"
FREEZE_SHA = "642348d737439d2b87f2abb0f7d0a499955409745554f1bf85cb5b9937474d12"
PAYLOAD_SHA = "72924b4c87ee437f2e273c67b06685a2394fae762210c84ac55d4af3be6bbb89"
TIMES = [0., .01, .02, .04, .08]
FLAGS = {
    "physical_volume_mapping_qualified": False, "source_equals_metric_strain": False,
    "gravity_derived": False, "vacuum_density_predicted": False,
    "passive_quartic_continuum_derived": False,
    "native_state_formation_for_galaxies_qualified": False,
    "observational_validation": False, "stage3_complete": False,
}
PINS = {
    "../recovered_sources/BS_MICRO_ACTION.md": "00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec",
    "record_addition_compute.py": "4df3bbc8b38ad6b602841b7b28a7a59d37e69d60286f7a2ef11c37ddc150ce10",
    "NATIVE_OPERATIONAL_SOURCE_CLOCK_VOLUME_CANDIDATES_V001.md": "fbddff9520f898bf888600ac62a03729d25b7cf4ad230196b04505f81853304b",
    "NATIVE_SOURCE_BRIDGE_DECISION.md": "c82040f7bebbdefcec4e782f8afb86c6c1c3f2367775f5fd2e6dbbe6159c737a",
    "NATIVE_RULER_SOURCE_AND_NORMAL_FORM_V001.md": "335044ff025cfd831f92ed34574098fb7fe42841047c2b657d40962f6439568c",
    "NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_PROTOCOL.md": "724f8d8c4a7bbcc7ce4ba9fa37f750e92d96b732db78ef1cc1347fcd52a7a7d5",
    "native_autonomous_volume_formation_v001.py": "8cdffaded72a83d6117dd0bf61e944d1c5b9f0e8800e4a7f2dd36ff477175317",
}
CONTRACT = {
    "basis": ["Q_minus_zero_plus", "formation_controller_0_1", "record_L", "record_R", "incidence", "carrier_left_right"],
    "dimensions": [3, 2, 2, 2, 2, 2], "hbar": 1., "J": 1., "Omega": 1., "g": 1., "Eb": 2.,
    "q_definition": "[-log(2)/3,0,+log(2)/3]",
    "native_parameters": {"h": 1., "Delta": 4., "Ud": 1., "dstar": 1.,
                          "epsilon_carrier": 1., "epsilon_record": 1., "epsilon_writer": 0.,
                          "t": .5, "lambda_R": .5, "lambda_J": .25},
    "times": TIMES, "cases": [["A", "minus"], ["A", "plus"], ["B", "minus"], ["B", "plus"]],
    "tolerance_operator": 2e-11, "tolerance_propagator": 5e-11,
    "tolerance_energy_current": 5e-10, "tolerance_coefficient": 2e-10,
    "taylor_scaled_tail": 1e-18, "taylor_max_order": 128,
    "resource": {"cpu_seconds": 30, "wall_seconds": 60, "rss_bytes": 268435456,
                 "max_checks": 4096, "threads": 1},
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def self_rss():
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(peak if sys.platform == "darwin" else peak * 1024)


def audit():
    started = time.monotonic()
    cpu_started = time.process_time()
    resource.setrlimit(resource.RLIMIT_CPU, (30, 31))
    checks, files = [], {}

    def guard():
        if time.monotonic() - started > 60 or self_rss() > 268435456 or len(checks) > 6000:
            raise RuntimeError("Saved-only audit resource guard reached")

    def equal(name, actual, expected):
        guard()
        checks.append({"name": name, "passed": bool(actual == expected), "kind": "exact"})

    def close(name, actual, expected=0., tol=2e-11, scaled=False):
        guard()
        a, b = np.asarray(actual), np.asarray(expected)
        delta = float(np.max(np.abs(a-b)))
        scale = max(1., float(np.max(np.abs(a))), float(np.max(np.abs(b)))) if scaled else 1.
        checks.append({"name": name, "passed": bool(math.isfinite(delta) and delta <= tol*scale),
                       "kind": "arithmetic", "residual": delta, "scale": scale,
                       "tolerance": tol, "limit": tol*scale, "scaled_residual": delta/scale})

    def authenticate(path, expected):
        actual = digest(path)
        files[str(path.relative_to(HERE))] = actual
        if actual != expected:
            raise RuntimeError("Input identity mismatch: " + path.name)
        equal("file:"+path.name, actual, expected)

    authenticate(RESULT, RESULT_SHA)
    authenticate(FREEZE, FREEZE_SHA)
    data = json.loads(RESULT.read_text())
    frozen = json.loads(FREEZE.read_text())
    without_payload = dict(data)
    supplied_payload = without_payload.pop("payload_sha256")
    recomputed = hashlib.sha256(canonical(without_payload)).hexdigest()
    equal("payload:supplied", supplied_payload, PAYLOAD_SHA)
    equal("payload:recomputed", recomputed, PAYLOAD_SHA)
    equal("freeze:files", frozen["files"], PINS)
    for filename, expected in PINS.items():
        authenticate(HERE / filename, expected)
    equal("result:files", data["input_files"], PINS)
    equal("result:freeze", data["freeze_sha256"], FREEZE_SHA)
    equal("freeze:contract", frozen["contract"], CONTRACT)
    equal("result:contract", data["contract"], CONTRACT)
    equal("freeze:flags", frozen["physical_promotion_flags"], FLAGS)
    equal("result:flags", data["physical_promotion_flags"], FLAGS)
    equal("result:schema", data["schema"], "native-autonomous-volume-formation-v001")
    equal("freeze:schema", frozen["schema"], data["schema"])
    equal("result:status", data["status"], "COMPLETE_CONDITIONAL_APPARATUS_CHECKS")
    equal("result:failure_list", data["failures"], [])
    equal("producer:checks", data["check_count"], 864)
    equal("producer:check_list_length", len(data["checks"]), 864)
    for ix, saved in enumerate(data["checks"]):
        equal(f"producer:recorded_pass:{ix}", saved["passed"], True)
        equal(f"producer:recorded_gate:{ix}",
              math.isfinite(saved["residual"]) and saved["residual"] <= saved["limit"], True)
        close(f"producer:gate_arithmetic:{ix}", saved["limit"], saved["tolerance"]*saved["scale"])
    for field, ceiling in (("elapsed_seconds", 60), ("cpu_seconds", 30), ("maximum_self_rss_bytes", 268435456)):
        value = data["resources"][field]
        equal("producer:resource:"+field, math.isfinite(value) and 0 <= value <= ceiling, True)

    # Separate basis-action implementation, without Kronecker assembly or importing helpers.
    nh = np.zeros((16, 16)); nt = np.zeros((16, 16)); nk = np.zeros((16, 16))
    record = np.zeros(16); incidence = np.zeros(16); arrival = np.zeros(16)
    for col in range(16):
        left, right, active, car = ((col >> bit) & 1 for bit in (3, 2, 1, 0))
        rr = left + right
        record[col], incidence[col], arrival[col] = rr, active, car
        nh[col, col] = 3 + rr + active*(2.25-.5*rr)
        nh[col ^ 2, col] = -1.
        nh[col ^ 1, col] = -.5*active
        nt[col, col] = .25*active
        nt[col ^ 1, col] = -.5*active
        nk[col ^ 8, col] = nk[col ^ 4, col] = 1.
    volumes = [.5, 1., 2.]
    q_values = [-math.log(2)/3, 0., math.log(2)/3]
    factors = [2**(1/3), 1., 2**(-1/3)]
    observable_diagonals = {name: np.zeros(96) for name in (
        "record_count", "incidence", "carrier_right", "formation_controller_on",
        "volume_over_V0", "record_count_over_volume", "Q_minus", "Q_zero", "Q_plus")}
    transport_observable = np.zeros((96, 96))
    for col in range(96):
        qi, rest = divmod(col, 32)
        ci, ni = divmod(rest, 16)
        for name, arr in (("record_count", record), ("incidence", incidence), ("carrier_right", arrival)):
            observable_diagonals[name][col] = arr[ni]
        observable_diagonals["formation_controller_on"][col] = ci
        observable_diagonals["volume_over_V0"][col] = volumes[qi]
        observable_diagonals["record_count_over_volume"][col] = record[ni]/volumes[qi]
        observable_diagonals[("Q_minus", "Q_zero", "Q_plus")[qi]][col] = 1.
        transport_observable[qi*32+ci*16:qi*32+ci*16+16, col] = nt[:, ni]
    ops = {name: np.diag(values) for name, values in observable_diagonals.items()}
    ops["native_transport"] = transport_observable

    def components_for(model):
        names = ["volume_controller", "formation_controller", "formation_interaction"]
        names += ["native_scaled"] if model == "A" else ["native_remainder", "transport", "volume_baseline"]
        answer = {name: np.zeros((96, 96)) for name in names}
        for col in range(96):
            qi, rest = divmod(col, 32)
            ci, ni = divmod(rest, 16)
            base = qi*32+ci*16
            answer["volume_controller"][col, col] = 2 if qi == 1 else 1
            for neighbour in (qi-1, qi+1):
                if 0 <= neighbour <= 2:
                    answer["volume_controller"][neighbour*32+rest, col] = -1.
            answer["formation_controller"][col, col] = 1.
            answer["formation_controller"][qi*32+(1-ci)*16+ni, col] = -1.
            multiplier = factors[qi] if model == "A" else 1.
            answer["formation_interaction"][base:base+16, col] = ci*multiplier*nk[:, ni]
            if model == "A":
                answer["native_scaled"][base:base+16, col] = factors[qi]*nh[:, ni]
            else:
                answer["native_remainder"][base:base+16, col] = nh[:, ni]-nt[:, ni]
                answer["native_remainder"][col, col] -= 2.
                answer["transport"][base:base+16, col] = factors[qi]*nt[:, ni]
                answer["volume_baseline"][col, col] = 2*volumes[qi]
        return answer

    def moment(psi, operator, tag):
        z = np.vdot(psi, operator @ psi)
        close(tag+":imaginary", z.imag)
        return float(z.real)

    def coefficients(h, op, index):
        # Binomial closed form of ad_H^n, using powers applied to one basis vector.
        initial = np.eye(96)[:, index]
        powers = [initial]
        for _ in range(4):
            powers.append(h @ powers[-1])
        out = {}
        for degree in range(5):
            value = sum((-1)**k*math.comb(degree, k)*np.vdot(powers[degree-k], op @ powers[k])
                        for k in range(degree+1))
            out[str(degree)] = (1j**degree)*value/math.factorial(degree)
        return out

    summaries = {}
    equal("models:census", sorted(data["models"]), ["A", "B"])
    for model in ("A", "B"):
        stored = data["models"][model]
        parts = components_for(model)
        h = sum(parts.values())
        close(model+":matrix", stored["hamiltonian_real"], h)
        close(model+":matrix_symmetric", h, h.T)
        equal(model+":component_census", sorted(stored["components_real"]), sorted(parts))
        for name, matrix in parts.items():
            close(model+":component:"+name, stored["components_real"][name], matrix)
            close(model+":component_symmetric:"+name, matrix, matrix.T)
        equal(model+":case_census", sorted(stored["cases"]), ["minus", "plus"])
        coeffs, summary_cases = {}, {}
        for label, qi in (("minus", 0), ("plus", 2)):
            tag = model+":"+label
            case = stored["cases"][label]
            index = qi*32+16
            pcoeff = coefficients(h, ops["Q_zero"], index)
            rcoeff = coefficients(h, ops["record_count"], index)
            coeffs[label] = (pcoeff, rcoeff)
            for family, recombined in (("recoil_coefficients", pcoeff), ("record_coefficients", rcoeff)):
                equal(tag+":"+family+":degree_census", sorted(case[family]), ["0", "1", "2", "3", "4"])
                for degree in range(5):
                    close(tag+":"+family+":"+str(degree), case[family][str(degree)], recombined[str(degree)], 2e-10, True)
            close(tag+":q", case["q"], q_values[qi])
            close(tag+":volume", case["volume_over_V0"], volumes[qi])
            initial_energy = 2+3*factors[qi] if model == "A" else 3+2*volumes[qi]
            close(tag+":initial_energy", case["initial_energy"], initial_energy, 5e-10, True)
            d2 = ((factors[qi]-1)**2*12-6*(factors[qi]-1)+1 if model == "A"
                  else (2*volumes[qi]-3)**2)
            close(tag+":detuning_square", case["detuning_second_moment"], d2, 2e-10, True)
            close(tag+":recoil_second_oracle", pcoeff["2"], 1., 2e-10, True)
            close(tag+":recoil_fourth_oracle", pcoeff["4"], -d2/12-2/3, 2e-10, True)
            close(tag+":record_second_oracle", rcoeff["2"], 2*factors[qi]**2 if model == "A" else 2., 2e-10, True)
            equal(tag+":time_census", [sample["time"] for sample in case["samples"]], TIMES)
            sample_summaries = []
            for sample in case["samples"]:
                t = sample["time"]
                st = tag+":"+str(t)
                psi = np.array(sample["state"]["real"])+1j*np.array(sample["state"]["imag"])
                equal(st+":state_dimension", list(psi.shape), [96])
                close(st+":norm", np.vdot(psi, psi), 1.)
                if t == 0:
                    close(st+":initial_state", psi, np.eye(96)[:, index], 5e-11)
                equal(st+":readout_census", sorted(sample["readouts"]), sorted(ops))
                readings = {}
                for name, operator in ops.items():
                    readings[name] = moment(psi, operator, st+":"+name)
                    close(st+":readout:"+name, sample["readouts"][name], readings[name])
                qprob = [readings["Q_"+name] for name in ("minus", "zero", "plus")]
                close(st+":Q_sum", sum(qprob), 1.)
                equal(st+":Q_positivity", min(qprob) >= -2e-11, True)
                energy = moment(psi, h, st+":total_energy")
                close(st+":total_energy", sample["total_energy"], energy, 5e-10, True)
                close(st+":energy_conservation", energy, initial_energy, 5e-10, True)
                equal(st+":energy_census", sorted(sample["component_energies"]), sorted(parts))
                equal(st+":current_census", sorted(sample["component_currents"]), sorted(parts))
                energies, currents = {}, {}
                hpsi = h @ psi
                for name, operator in parts.items():
                    epsi = operator @ psi
                    energies[name] = float(np.vdot(psi, epsi).real)
                    # i<[H,Ha]> = -2 Im <H psi|Ha psi>, no commutator matrix copied.
                    currents[name] = -2*float(np.vdot(hpsi, epsi).imag)
                    close(st+":component_energy:"+name, sample["component_energies"][name], energies[name], 5e-10, True)
                    close(st+":component_current:"+name, sample["component_currents"][name], currents[name], 5e-10, True)
                close(st+":energy_sum", sum(energies.values()), energy, 5e-10, True)
                close(st+":current_sum", sum(currents.values()), 0., 5e-10, True)
                close(st+":recoil_remainder", sample["recoil_truncated_t4_signed_remainder"],
                      readings["Q_zero"]-(pcoeff["2"].real*t*t+pcoeff["4"].real*t**4))
                close(st+":record_remainder", sample["records_truncated_t2_signed_remainder"],
                      readings["record_count"]-rcoeff["2"].real*t*t)
                # Authenticate Taylor scalar metadata only; no Taylor/eigen propagation rerun.
                norm = abs(t)*float(np.max(np.sum(np.abs(h), axis=1)))
                squares = max(0, math.ceil(math.log2(norm/.5))) if norm else 0
                x = norm/2**squares
                scalar = 1.
                for order in range(1, 129):
                    scalar *= x/order
                    tail = math.exp(x)*scalar*x/(order+1)
                    if tail <= 1e-18:
                        break
                grown_tail = tail
                for _ in range(squares):
                    grown_tail *= 2+grown_tail
                meta = sample["taylor_metadata"]
                equal(st+":Taylor_order", meta["order"], order)
                equal(st+":Taylor_squarings", meta["squarings"], squares)
                close(st+":Taylor_norm", meta["scaled_infinity_norm"], x)
                equal(st+":Taylor_tail_bound", 0 <= meta["scaled_exact_arithmetic_tail"] <= 1e-18, True)
                close(st+":Taylor_tail", meta["scaled_exact_arithmetic_tail"], tail, 1e-30)
                close(st+":Taylor_grown_tail", meta["propagated_exact_arithmetic_tail"], grown_tail, 1e-29)
                sample_summaries.append({"time": t, "Q_zero": readings["Q_zero"], "record_count": readings["record_count"],
                                         "volume_over_V0": readings["volume_over_V0"],
                                         "record_count_over_volume": readings["record_count_over_volume"],
                                         "energy_defect": energy-initial_energy,
                                         "component_current_sum": sum(currents.values())})
            summary_cases[label] = {"initial_energy": initial_energy, "recoil_t4": float(pcoeff["4"].real),
                                    "record_t2": float(rcoeff["2"].real), "samples": sample_summaries}
        contrast = float((coeffs["minus"][0]["4"]-coeffs["plus"][0]["4"]).real)
        formula = (factors[0]-factors[2])*(2.5-factors[0]-factors[2]) if model == "A" else -.25
        ratio = float((coeffs["minus"][1]["2"]/coeffs["plus"][1]["2"]).real)
        close(model+":contrast_formula", contrast, formula, 2e-10, True)
        close(model+":saved_contrast", stored["recoil_t4_contrast"], contrast, 2e-10, True)
        close(model+":saved_predicted_contrast", stored["predicted_recoil_t4_contrast"], formula, 2e-10, True)
        close(model+":record_ratio", stored["record_t2_ratio"], ratio, 2e-10, True)
        close(model+":record_ratio_oracle", ratio, 2**(4/3) if model == "A" else 1., 2e-10, True)
        contrasts = stored["finite_time_recoil_contrasts"]
        equal(model+":contrast_times", [row["time"] for row in contrasts], TIMES)
        for ix, t in enumerate(TIMES):
            value = summary_cases["minus"]["samples"][ix]["Q_zero"]-summary_cases["plus"]["samples"][ix]["Q_zero"]
            close(model+":finite_contrast:"+str(t), contrasts[ix]["minus_minus_plus"], value)
        summaries[model] = {"cases": summary_cases, "recoil_t4_contrast": contrast, "record_t2_ratio": ratio}
    guard()
    arithmetic = [row for row in checks if row["kind"] == "arithmetic"]
    failed = [row for row in checks if not row["passed"]]
    return {"schema": "native-autonomous-volume-formation-saved-audit-v001",
            "status": "PASS_SAVED_ONLY_AUDIT" if not failed else "FAILED_SAVED_ONLY_AUDIT",
            "audit_source_sha256": digest(SOURCE), "authenticated_files": files,
            "producer_payload_sha256": recomputed, "checks": checks,
            "check_count": len(checks), "failures": failed,
            "maximum_absolute_residual": max(row["residual"] for row in arithmetic),
            "maximum_scaled_residual": max(row["scaled_residual"] for row in arithmetic),
            "maximum_fraction_of_limit": max(row["residual"]/row["limit"] for row in arithmetic),
            "summaries": summaries, "physical_promotion_flags": FLAGS,
            "scope": {"producer_imported": False, "propagation_rerun": False, "eigensolver_used": False,
                      "unsaved_propagator_and_method_residuals_independently_recomputed": False,
                      "description": "Explicit basis assembly and saved-state arithmetic; original method-check residuals authenticated only."},
            "resources": {"elapsed_seconds": time.monotonic()-started, "cpu_seconds": time.process_time()-cpu_started,
                          "maximum_self_rss_bytes": self_rss()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is not None and args.output.resolve() != OUTPUT:
        parser.error("Only the fixed audit output path is accepted")
    if OUTPUT.exists():
        parser.error("Audit output already exists; no work started")
    result = audit()
    result["payload_sha256"] = hashlib.sha256(canonical(result)).hexdigest()
    if args.output is None:
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    else:
        with OUTPUT.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2, sort_keys=True, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        print(json.dumps({"status": result["status"], "path": str(OUTPUT), "sha256": digest(OUTPUT),
                          "payload_sha256": result["payload_sha256"], "check_count": result["check_count"],
                          "failure_count": len(result["failures"]),
                          "maximum_scaled_residual": result["maximum_scaled_residual"],
                          "maximum_fraction_of_limit": result["maximum_fraction_of_limit"]}))
    if result["failures"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
