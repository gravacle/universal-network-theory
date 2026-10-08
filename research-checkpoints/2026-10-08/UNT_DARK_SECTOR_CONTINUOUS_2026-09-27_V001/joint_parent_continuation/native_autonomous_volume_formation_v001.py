"""Prospective 96D A/B apparatus; root alone freezes/runs this producer."""
import os
import sys

sys.dont_write_bytecode = True
for _key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "1"

import argparse
import hashlib
import json
import math
from pathlib import Path
import resource
import time

import numpy as np

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_PROTOCOL.md"
FREEZE = HERE / "NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_FROZEN.json"
RESULT = HERE / "NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_RESULTS.json"
PINS = {
    "../recovered_sources/BS_MICRO_ACTION.md": "00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec",
    "record_addition_compute.py": "4df3bbc8b38ad6b602841b7b28a7a59d37e69d60286f7a2ef11c37ddc150ce10",
    "NATIVE_OPERATIONAL_SOURCE_CLOCK_VOLUME_CANDIDATES_V001.md": "fbddff9520f898bf888600ac62a03729d25b7cf4ad230196b04505f81853304b",
    "NATIVE_SOURCE_BRIDGE_DECISION.md": "c82040f7bebbdefcec4e782f8afb86c6c1c3f2367775f5fd2e6dbbe6159c737a",
    "NATIVE_RULER_SOURCE_AND_NORMAL_FORM_V001.md": "335044ff025cfd831f92ed34574098fb7fe42841047c2b657d40962f6439568c",
}
CONTRACT = {
    "basis": ["Q_minus_zero_plus", "formation_controller_0_1", "record_L", "record_R", "incidence", "carrier_left_right"],
    "dimensions": [3, 2, 2, 2, 2, 2], "hbar": 1.0,
    "J": 1.0, "Omega": 1.0, "g": 1.0, "Eb": 2.0,
    "q_definition": "[-log(2)/3,0,+log(2)/3]",
    "native_parameters": {"h": 1., "Delta": 4., "Ud": 1., "dstar": 1.,
                          "epsilon_carrier": 1., "epsilon_record": 1.,
                          "epsilon_writer": 0., "t": .5, "lambda_R": .5, "lambda_J": .25},
    "times": [0., .01, .02, .04, .08],
    "cases": [["A", "minus"], ["A", "plus"], ["B", "minus"], ["B", "plus"]],
    "tolerance_operator": 2e-11, "tolerance_propagator": 5e-11,
    "tolerance_energy_current": 5e-10, "tolerance_coefficient": 2e-10,
    "taylor_scaled_tail": 1e-18, "taylor_max_order": 128,
    "resource": {"cpu_seconds": 30, "wall_seconds": 60, "rss_bytes": 256*1024*1024,
                 "max_checks": 4096, "threads": 1},
}
FLAGS = {name: False for name in (
    "physical_volume_mapping_qualified", "source_equals_metric_strain", "gravity_derived",
    "vacuum_density_predicted", "passive_quartic_continuum_derived",
    "native_state_formation_for_galaxies_qualified", "observational_validation", "stage3_complete")}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def identities():
    found = {name: sha(HERE / name) for name in PINS}
    if found != PINS:
        raise RuntimeError("Resident source identity mismatch")
    found[PROTOCOL.name] = sha(PROTOCOL)
    found[Path(__file__).name] = sha(Path(__file__))
    return found


def freeze_packet():
    return {"schema": "native-autonomous-volume-formation-v001", "files": identities(),
            "contract": CONTRACT, "physical_promotion_flags": FLAGS}


def exclusive_write(path, payload):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def comm(a, b):
    return a @ b - b @ a


def magnitude(value):
    return float(np.max(np.abs(np.asarray(value))))


def vector_json(v):
    return {"real": v.real.tolist(), "imag": v.imag.tolist()}


def produce(context):
    started = time.monotonic()
    cpu_started = time.process_time()
    resource.setrlimit(resource.RLIMIT_CPU, (CONTRACT["resource"]["cpu_seconds"],
                                            CONTRACT["resource"]["cpu_seconds"] + 1))
    frozen = json.loads(FREEZE.read_text())
    if frozen != freeze_packet():
        raise RuntimeError("Prospective freeze mismatch")
    checks = []
    context.update({"freeze_sha256": sha(FREEZE), "input_files": frozen["files"],
                    "contract": CONTRACT, "checks": checks, "models": {}})

    def rss_bytes():
        value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(value if sys.platform == "darwin" else value * 1024)

    def guard():
        if time.monotonic() - started > CONTRACT["resource"]["wall_seconds"]:
            raise RuntimeError("Elapsed resource bound exceeded")
        if rss_bytes() > CONTRACT["resource"]["rss_bytes"]:
            raise RuntimeError("RSS resource bound exceeded")
        if len(checks) > CONTRACT["resource"]["max_checks"]:
            raise RuntimeError("Check-count resource bound exceeded")

    def check(name, actual, expected=0., tolerance=None, scaled=False):
        guard()
        tolerance = CONTRACT["tolerance_operator"] if tolerance is None else tolerance
        error = magnitude(np.asarray(actual) - np.asarray(expected))
        scale = max(1., magnitude(actual), magnitude(expected)) if scaled else 1.
        checks.append({"name": name, "residual": error, "scale": scale,
                       "tolerance": tolerance, "limit": tolerance * scale,
                       "passed": bool(math.isfinite(error) and error <= tolerance * scale)})

    def expect(psi, operator, name):
        value = np.vdot(psi, operator @ psi)
        check(name + ":real", value.imag)
        return float(value.real)

    i2 = np.eye(2)
    x2 = np.array([[0., 1.], [1., 0.]])
    n2 = np.diag([0., 1.])
    y2 = np.array([[0., -1j], [1j, 0.]])
    i16, i32, i96 = np.eye(16), np.eye(32), np.eye(96)

    def embed(matrix, factor):
        value = np.ones((1, 1), complex)
        for index in range(4):
            value = np.kron(value, matrix if index == factor else i2)
        return value

    ql, qr, n, carrier = (embed(n2, j) for j in range(4))
    xl, xr, xa, xc = (embed(x2, j) for j in range(4))
    yc = embed(y2, 3)
    r, k = ql + qr, xl + xr
    native_terms = {
        "incidence_flip": -xa,
        "incidence_bias": 4*n,
        "both_degree_penalties": 2*(n-i16) @ (n-i16),
        "carrier_occupation": i16,
        "record_storage": r,
        "carrier_hopping": -.5*n @ xc,
        "record_incidence_feedback": -.5*n @ r,
        "current_squared_feedback": .25*n @ yc @ yc,
    }
    hh = sum(native_terms.values())
    compact = 3*i16+r-xa+n @ (2.25*i16-.5*r-.5*xc)
    transport = n @ (.25*i16-.5*xc)
    check("native:term_reconstruction", hh, compact)
    check("native:full_transport", transport,
          native_terms["carrier_hopping"]+native_terms["current_squared_feedback"])
    check("native:incidence_strength", comm(n, comm(hh, n)), xa)
    native_blank = np.zeros(16, complex)
    native_blank[0] = 1.
    check("native:blank_transport", transport @ native_blank, 0.)
    check("native:formation_mean", np.vdot(native_blank, (hh+k) @ native_blank), 3.)
    check("native:formation_second_moment", np.vdot(native_blank, (hh+k) @ (hh+k) @ native_blank), 12.)

    q_values = np.array([-math.log(2)/3, 0., math.log(2)/3])
    volumes = np.exp(3*q_values)
    check("volume:labels", volumes, [.5, 1., 2.])
    hq = np.zeros((3, 3))
    for left, right in ((0, 1), (1, 2)):
        difference = np.eye(3)[left]-np.eye(3)[right]
        hq += CONTRACT["J"]*np.outer(difference, difference)
    hc = CONTRACT["Omega"]*(i2-x2)
    native_observables = {"record_count": r, "incidence": n, "carrier_right": carrier,
                          "native_transport": transport}
    observables = {name: np.kron(np.eye(6), op) for name, op in native_observables.items()}
    observables["formation_controller_on"] = np.kron(np.eye(3), np.kron(n2, i16))
    observables["volume_over_V0"] = np.kron(np.diag(volumes), i32)
    observables["record_count_over_volume"] = np.kron(np.diag(1/volumes), np.kron(i2, r))
    for index, label in enumerate(("minus", "zero", "plus")):
        projector = np.diag([float(j == index) for j in range(3)])
        observables["Q_"+label] = np.kron(projector, i32)
        check("projector:"+label, observables["Q_"+label] @ observables["Q_"+label],
              observables["Q_"+label])
    p0 = observables["Q_zero"]
    env_blank = np.zeros(32, complex)
    env_blank[16] = 1.

    def taylor_u(h, duration):
        matrix = -1j*duration*h
        original_norm = float(np.linalg.norm(matrix, ord=np.inf))
        squares = max(0, math.ceil(math.log2(original_norm/.5))) if original_norm else 0
        matrix /= 2**squares
        x = float(np.linalg.norm(matrix, ord=np.inf))
        value, term, scalar_term = i96.astype(complex).copy(), i96.astype(complex).copy(), 1.
        for order in range(1, CONTRACT["taylor_max_order"]+1):
            term = term @ matrix/order
            value += term
            scalar_term *= x/order
            tail = math.exp(x)*scalar_term*x/(order+1)
            if tail <= CONTRACT["taylor_scaled_tail"]:
                break
        else:
            raise RuntimeError("Taylor order bound reached")
        propagated_tail = tail
        for _ in range(squares):
            value = value @ value
            propagated_tail *= 2+propagated_tail
        return value, {"order": order, "squarings": squares,
                       "scaled_infinity_norm": x, "scaled_exact_arithmetic_tail": tail,
                       "propagated_exact_arithmetic_tail": propagated_tail}

    def coefficients(h, op, psi, label):
        nested = op.copy()
        nested_values = {0: np.vdot(psi, op @ psi)}
        vectors = [psi]
        for degree in range(1, 5):
            nested = comm(h, nested)
            nested_values[degree] = (1j**degree)*np.vdot(psi, nested @ psi)/math.factorial(degree)
            vectors.append((-1j)*(h @ vectors[-1])/degree)
        answer = {}
        for degree in range(5):
            separate = sum(np.vdot(vectors[j], op @ vectors[degree-j]) for j in range(degree+1))
            check(label+f":coefficient:{degree}:independent", nested_values[degree], separate,
                  CONTRACT["tolerance_coefficient"], scaled=True)
            check(label+f":coefficient:{degree}:real", nested_values[degree].imag,
                  tolerance=CONTRACT["tolerance_coefficient"])
            if degree % 2:
                check(label+f":coefficient:{degree}:even_time", nested_values[degree],
                      tolerance=CONTRACT["tolerance_coefficient"])
            answer[str(degree)] = float(nested_values[degree].real)
        return answer

    models = context["models"]
    for model in ("A", "B"):
        guard()
        components = {"volume_controller": np.kron(hq, i32),
                      "formation_controller": np.kron(np.eye(3), np.kron(hc, i16))}
        blocks = []
        if model == "A":
            components["native_scaled"] = np.kron(np.diag(np.exp(-q_values)), np.kron(i2, hh))
            components["formation_interaction"] = np.kron(np.diag(np.exp(-q_values)),
                                                            CONTRACT["g"]*np.kron(n2, k))
            for q in q_values:
                blocks.append(math.exp(-q)*(np.kron(i2, hh)+CONTRACT["g"]*np.kron(n2, k)))
        else:
            components["native_remainder"] = np.kron(np.eye(6), hh-transport-2*i16)
            components["transport"] = np.kron(np.diag(np.exp(-q_values)), np.kron(i2, transport))
            components["volume_baseline"] = np.kron(np.diag(2*volumes), i32)
            components["formation_interaction"] = np.kron(np.eye(3), CONTRACT["g"]*np.kron(n2, k))
            for q, volume in zip(q_values, volumes):
                blocks.append(np.kron(i2, hh-transport-2*i16+math.exp(-q)*transport+2*volume*i16)
                              +CONTRACT["g"]*np.kron(n2, k))
        h = sum(components.values())
        direct = (np.kron(hq, i32)+np.kron(np.eye(3), np.kron(hc, i16))).astype(complex)
        for index, block in enumerate(blocks):
            direct[index*32:(index+1)*32, index*32:(index+1)*32] += block
        check(model+":independent_block_assembly", h, direct)
        check(model+":reference_native_source", blocks[1], np.kron(i2, hh)+CONTRACT["g"]*np.kron(n2, k))
        for name, op in {"total": h, **components}.items():
            check(model+":"+name+":hermitian", op, op.conj().T)
            check(model+":"+name+":real", np.asarray(op).imag)
        values, vectors = np.linalg.eigh(h)
        check(model+":spectral_reconstruction", (vectors*values) @ vectors.conj().T, h)
        currents = {name: 1j*comm(h, op) for name, op in components.items()}
        check(model+":sum_current_operator", sum(currents.values()),
              tolerance=CONTRACT["tolerance_energy_current"])
        propagators = {}
        for t in CONTRACT["times"]:
            guard()
            spectral = (vectors*np.exp(-1j*t*values)) @ vectors.conj().T
            series, metadata = taylor_u(h, t)
            check(model+f":t{t}:propagator_methods", spectral, series, CONTRACT["tolerance_propagator"])
            check(model+f":t{t}:spectral_unitarity", spectral.conj().T @ spectral, i96)
            check(model+f":t{t}:taylor_unitarity", series.conj().T @ series, i96)
            propagators[t] = (spectral, series, metadata)
        cases = {}
        context["in_progress"] = {"model": model, "cases": cases}
        for q_index, label in ((0, "minus"), (2, "plus")):
            psi0 = np.zeros(96, complex)
            psi0[q_index*32+16] = 1.
            tag = model+":"+label
            initial_energy = expect(psi0, h, tag+":initial_energy")
            expected_initial = (2+3*math.exp(-q_values[q_index]) if model == "A"
                                else 3+2*volumes[q_index])
            check(tag+":initial_energy_formula", initial_energy, expected_initial,
                  CONTRACT["tolerance_energy_current"], scaled=True)
            recoil = coefficients(h, p0, psi0, tag+":recoil")
            records = coefficients(h, observables["record_count"], psi0, tag+":records")
            detuning = blocks[q_index]-blocks[1]-CONTRACT["J"]*i32
            detuning_second = expect(env_blank, detuning @ detuning, tag+":detuning_second_moment")
            predicted_fourth = -CONTRACT["J"]**2*detuning_second/12-2*CONTRACT["J"]**4/3
            predicted_record_second = 2*CONTRACT["g"]**2*(math.exp(-2*q_values[q_index]) if model == "A" else 1.)
            for suffix, actual, expected in (("recoil_0", recoil["0"], 0.),
                                            ("recoil_2", recoil["2"], CONTRACT["J"]**2),
                                            ("recoil_4", recoil["4"], predicted_fourth),
                                            ("records_0", records["0"], 0.),
                                            ("records_2", records["2"], predicted_record_second)):
                check(tag+":"+suffix, actual, expected, CONTRACT["tolerance_coefficient"], scaled=True)
            samples = []
            context["in_progress"].update({"endpoint": label, "samples": samples,
                                           "recoil_coefficients": recoil, "record_coefficients": records})
            for t in CONTRACT["times"]:
                guard()
                spectral, series, metadata = propagators[t]
                psi, psi_series = spectral @ psi0, series @ psi0
                sample_tag = tag+f":t{t}"
                check(sample_tag+":state_methods", psi, psi_series, CONTRACT["tolerance_propagator"])
                check(sample_tag+":norm", np.vdot(psi, psi), 1.)
                readouts = {name: expect(psi, op, sample_tag+":"+name) for name, op in observables.items()}
                q_probs = [readouts["Q_"+part] for part in ("minus", "zero", "plus")]
                check(sample_tag+":probability_sum", sum(q_probs), 1.)
                check(sample_tag+":probability_lower", max(0., -min(q_probs)))
                energy = expect(psi, h, sample_tag+":energy")
                energies = {name: expect(psi, op, sample_tag+":energy:"+name) for name, op in components.items()}
                flows = {name: expect(psi, op, sample_tag+":current:"+name) for name, op in currents.items()}
                tangent = -1j*h @ psi
                for name, op in components.items():
                    derivative = 2*float(np.vdot(tangent, op @ psi).real)
                    check(sample_tag+":current_tangent:"+name, flows[name], derivative,
                          CONTRACT["tolerance_energy_current"], scaled=True)
                check(sample_tag+":total_energy_conservation", energy, initial_energy,
                      CONTRACT["tolerance_energy_current"], scaled=True)
                check(sample_tag+":component_energy_sum", sum(energies.values()), energy,
                      CONTRACT["tolerance_energy_current"], scaled=True)
                check(sample_tag+":component_current_sum", sum(flows.values()),
                      tolerance=CONTRACT["tolerance_energy_current"], scaled=True)
                samples.append({"time": t, "state": vector_json(psi), "readouts": readouts,
                                "total_energy": energy, "component_energies": energies,
                                "component_currents": flows, "taylor_metadata": metadata,
                                "recoil_truncated_t4_signed_remainder": readouts["Q_zero"]-(recoil["2"]*t*t+recoil["4"]*t**4),
                                "records_truncated_t2_signed_remainder": readouts["record_count"]-records["2"]*t*t})
            cases[label] = {"q": float(q_values[q_index]), "volume_over_V0": float(volumes[q_index]),
                            "initial_energy": initial_energy, "recoil_coefficients": recoil,
                            "record_coefficients": records, "detuning_second_moment": detuning_second,
                            "samples": samples}
        a, b = 2**(1/3), 2**(-1/3)
        predicted_contrast = (a-b)*(2.5-a-b) if model == "A" else -.25
        measured_contrast = cases["minus"]["recoil_coefficients"]["4"]-cases["plus"]["recoil_coefficients"]["4"]
        check(model+":recoil_contrast_t4", measured_contrast, predicted_contrast,
              CONTRACT["tolerance_coefficient"], scaled=True)
        record_ratio = cases["minus"]["record_coefficients"]["2"]/cases["plus"]["record_coefficients"]["2"]
        check(model+":record_t2_ratio", record_ratio, 2**(4/3) if model == "A" else 1.,
              CONTRACT["tolerance_coefficient"], scaled=True)
        models[model] = {"hamiltonian_real": h.real.tolist(),
                         "components_real": {name: op.real.tolist() for name, op in components.items()},
                         "cases": cases, "recoil_t4_contrast": measured_contrast,
                         "predicted_recoil_t4_contrast": predicted_contrast,
                         "record_t2_ratio": record_ratio,
                         "finite_time_recoil_contrasts": [
                             {"time": left["time"], "minus_minus_plus": left["readouts"]["Q_zero"]-right["readouts"]["Q_zero"]}
                             for left, right in zip(cases["minus"]["samples"], cases["plus"]["samples"])]}
    guard()
    context.pop("in_progress", None)
    failed = [row for row in checks if not row["passed"]]
    return {"schema": frozen["schema"], "status": "COMPLETE_CONDITIONAL_APPARATUS_CHECKS" if not failed else "FAILED_CHECKS_RETAINED",
            "freeze_sha256": sha(FREEZE), "input_files": frozen["files"], "contract": CONTRACT,
            "models": models, "checks": checks, "check_count": len(checks), "failures": failed,
            "physical_promotion_flags": FLAGS,
            "resources": {"elapsed_seconds": time.monotonic()-started, "cpu_seconds": time.process_time()-cpu_started,
                          "maximum_self_rss_bytes": rss_bytes(), "numpy_version": np.__version__, "python_version": sys.version}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--freeze", action="store_true")
    modes.add_argument("--run", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.freeze:
        if args.output is not None:
            parser.error("--freeze does not accept --output")
        exclusive_write(FREEZE, freeze_packet())
        print(json.dumps({"status": "PROSPECTIVE_FREEZE_CREATED", "path": str(FREEZE), "sha256": sha(FREEZE)}))
        return
    if args.output is not None:
        if args.output.resolve() != RESULT:
            parser.error("Only the fixed, previously absent result path is accepted")
        if RESULT.exists():
            parser.error("Result already exists; no numerical work started")
    context = {}
    try:
        result = produce(context)
    except Exception as exc:
        result = {"schema": "native-autonomous-volume-formation-v001", "status": "TECHNICAL_FAILURE_RETAINED",
                  "error_type": type(exc).__name__, "error": str(exc), "physical_promotion_flags": FLAGS,
                  "partial_evidence": context}
    result["payload_sha256"] = hashlib.sha256(encode(result)).hexdigest()
    if args.output is None:
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    else:
        exclusive_write(RESULT, result)
        print(json.dumps({"status": result["status"], "path": str(RESULT), "sha256": sha(RESULT),
                          "payload_sha256": result["payload_sha256"], "check_count": result.get("check_count"),
                          "failure_count": len(result.get("failures", []))}))
    if result["status"] != "COMPLETE_CONDITIONAL_APPARATUS_CHECKS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
