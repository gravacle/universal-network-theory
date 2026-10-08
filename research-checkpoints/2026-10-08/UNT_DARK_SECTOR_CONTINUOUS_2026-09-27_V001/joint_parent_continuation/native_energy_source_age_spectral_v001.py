"""Two 96D eigensolves; complete numerical data, never a spectral certificate."""
import os
import sys

sys.dont_write_bytecode = True
for _thread_key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
                    "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_thread_key] = "1"

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import resource
import signal
import tempfile
import time

import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
PROTOCOL = HERE / "NATIVE_ENERGY_SOURCE_AGE_SPECTRAL_V001_PROTOCOL.md"
FREEZE = HERE / "NATIVE_ENERGY_SOURCE_AGE_SPECTRAL_V001_FROZEN.json"
INTENT = HERE / "NATIVE_ENERGY_SOURCE_AGE_SPECTRAL_V001_INTENT.json"
RESULT = HERE / "NATIVE_ENERGY_SOURCE_AGE_SPECTRAL_V001_RESULTS.json"
AUTONOMOUS = HERE / "NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_RESULTS.json"
DIPOLE = HERE / "NATIVE_ENERGY_DIPOLE_SAVED_STATE_V001_RESULTS.json"
AUTONOMOUS_FREEZE = HERE / "NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_FROZEN.json"
DIPOLE_FREEZE = HERE / "NATIVE_ENERGY_DIPOLE_SAVED_STATE_V001_FROZEN.json"
PINS = {
    AUTONOMOUS.name: "bc35b592f5547e1f5fc566411ec7e8f7175776d20569fbccf0ae3e6457e74fc1",
    AUTONOMOUS_FREEZE.name: "642348d737439d2b87f2abb0f7d0a499955409745554f1bf85cb5b9937474d12",
    DIPOLE.name: "7deab3689642a6600fafabe6bbb3ad000d73464e0df1e9d84cd60c2f39f99b9a",
    DIPOLE_FREEZE.name: "7c02724ec0f9d8aeae549f3ae86bcdb014d1d93dd74455da7b5004e5a25497d9",
    "NATIVE_ENERGY_SOURCE_AGE_AVERAGE_V001.md": "764bb3f333aab4750fcb564c043ad715343dfaf15a5519e9fafa3b7cb18cf4d6",
    "NATIVE_ENERGY_SOURCE_AGE_AVERAGE_REVIEW_V001.md": "5320963e97440a846ba6f7b4c876f83f6fa9eb515c7b0bc5063e66d00742f3b3",
}
CONTRACT = {
    "schema": "native-energy-source-age-spectral-v001",
    "models": ["A", "B"], "endpoints": ["minus", "plus"],
    "times": [0., .01, .02, .04, .08], "dimension": 96,
    "eigensolve_count": 2, "initial_state_count": 4, "saved_state_count": 20,
    "pairs_per_model_and_case": 4560, "hbar": 1.,
    "tolerance": 2e-10, "resolution_half_width_multiplier": 2e-10,
    "cpu_soft_seconds": 60, "cpu_hard_seconds": 65, "wall_seconds": 60,
    "rss_bytes": 512*1024*1024, "max_checks": 4096,
    "max_file_bytes": 32*1024*1024, "threads": 1,
    "propagations": 0, "fits": 0, "physical_time_grid": None,
    "source_order": ["Z_over_gamma0", "minus_volume_force"],
    "source_convention": "PLUS lambda.G; conjugate-energy response is <C>-chi",
    "gamma0": "ell0/(2*c^2), symbolic",
}
FLAGS = {key: False for key in (
    "native_metric_derived", "physical_source_independently_validated",
    "continuous_soft_spectrum_established", "passive_mechanical_mapping_qualified",
    "initial_galaxy_polarization_generated", "vacuum_normalization_predicted",
    "observational_success", "stage3_complete", "exact_degeneracy_certified",
    "rigorous_eigenvalue_intervals", "rigorous_gap_certificate",
    "stationary_preparation_established", "inverse_gap_certificate",
    "source_age_error_bound_numerically_certified", "passivity_certified",
    "physical_readout_window_qualified")}


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_file(name):
    path = (HERE / name).resolve()
    if not path.is_relative_to(PROJECT):
        raise RuntimeError("Input path leaves the sole project root")
    return path


def read_json(path):
    if path.stat().st_size > CONTRACT["max_file_bytes"]:
        raise RuntimeError("Input exceeds the frozen size bound")
    return json.loads(path.read_text())


def identities():
    actual = {name: digest(local_file(name)) for name in PINS}
    if actual != PINS:
        raise RuntimeError("Pinned source/input bytes changed")
    actual[PROTOCOL.name] = digest(PROTOCOL)
    actual[Path(__file__).name] = digest(Path(__file__))
    return actual


def freeze_packet():
    return {"schema": CONTRACT["schema"], "files": identities(),
            "contract": CONTRACT, "qualification_flags": FLAGS}


def atomic_exclusive(path, value):
    """Publish only to a new fixed path; no existing name can be replaced."""
    data = json.dumps(value, indent=2, sort_keys=True, allow_nan=False).encode()+b"\n"
    if len(data) > CONTRACT["max_file_bytes"]:
        raise RuntimeError("Output exceeds the frozen size bound")
    if path.parent != HERE or path not in (FREEZE, INTENT, RESULT):
        raise RuntimeError("Publisher target outside fixed artifact census")
    descriptor, temporary = tempfile.mkstemp(prefix="."+path.name+".", dir=HERE)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary_path, path)
        directory_fd = os.open(HERE, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        temporary_path.unlink(missing_ok=True)


def authenticated_result(path, freeze_path, expected_status, files_key):
    value = read_json(path)
    payload_hash = value.pop("payload_sha256")
    if hashlib.sha256(encode(value)).hexdigest() != payload_hash:
        raise RuntimeError("Inherited result payload mismatch: "+path.name)
    if value["status"] != expected_status or value["failures"]:
        raise RuntimeError("Inherited calculation is not a clean completed result")
    if any(value["physical_promotion_flags"].values()):
        raise RuntimeError("Inherited result unexpectedly promotes physical claims")
    old_freeze = read_json(freeze_path)
    if value["freeze_sha256"] != digest(freeze_path):
        raise RuntimeError("Inherited freeze hash mismatch")
    if value[files_key] != old_freeze["files"]:
        raise RuntimeError("Inherited result/freeze file census mismatch")
    for name, expected in old_freeze["files"].items():
        if digest(local_file(name)) != expected:
            raise RuntimeError("Inherited frozen member changed: "+name)
    return value, payload_hash


def packed(array):
    return {"real": array.real.tolist(), "imag": array.imag.tolist()}


def complex_array(value, shape):
    array = np.asarray(value["real"], dtype=float)+1j*np.asarray(value["imag"], dtype=float)
    if array.shape != shape or not np.all(np.isfinite(array)):
        raise RuntimeError("Invalid saved array")
    return array


def frobenius(array):
    return float(np.sqrt(np.sum(np.abs(array)**2)))


def comm(a, b):
    return a @ b-b @ a


def overlap_groups(values, half_width):
    """Only descriptive connected neighborhoods, NEVER exact degeneracies."""
    groups = []
    for index, value in enumerate(values):
        if groups and value-half_width <= groups[-1]["right"]:
            groups[-1]["indices"].append(index)
            groups[-1]["right"] = max(groups[-1]["right"], float(value+half_width))
        else:
            groups.append({"indices": [index], "left": float(value-half_width),
                           "right": float(value+half_width)})
    for group in groups:
        group["status"] = "UNRESOLVED_NUMERICAL_CLUSTER" if len(group["indices"]) > 1 else "NUMERICALLY_SEPARATED_NOT_CERTIFIED"
        group["exact_degeneracy_asserted"] = False
    return groups


def analyze(context):
    started, cpu_started = time.monotonic(), time.process_time()
    checks, models = [], {}
    context.update({"checks": checks, "models": models, "eigensolves_completed": 0,
                    "initial_states_completed": 0, "saved_states_checked": 0})

    def rss():
        amount = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(amount if sys.platform == "darwin" else amount*1024)

    def guard():
        if time.monotonic()-started > CONTRACT["wall_seconds"]:
            raise RuntimeError("Frozen elapsed-time bound exceeded")
        if rss() > CONTRACT["rss_bytes"] or len(checks) > CONTRACT["max_checks"]:
            raise RuntimeError("Frozen memory/check bound exceeded")

    def ck(name, actual, expected=0., absolute=False):
        guard()
        left, right = np.asarray(actual), np.asarray(expected)
        error = float(np.max(np.abs(left-right)))
        scale = 1. if absolute else max(1., float(np.max(np.abs(left))), float(np.max(np.abs(right))))
        checks.append({"name": name, "residual": error, "scale": scale,
                       "tolerance": CONTRACT["tolerance"],
                       "passed": bool(math.isfinite(error) and error <= CONTRACT["tolerance"]*scale)})

    def require_passes():
        if any(not item["passed"] for item in checks):
            raise RuntimeError("Arithmetic qualification failed; partial evidence retained")

    frozen = read_json(FREEZE)
    if frozen != freeze_packet():
        raise RuntimeError("Prospective spectral freeze mismatch")
    original, original_payload = authenticated_result(
        AUTONOMOUS, AUTONOMOUS_FREEZE, "COMPLETE_CONDITIONAL_APPARATUS_CHECKS", "input_files")
    dipole, dipole_payload = authenticated_result(
        DIPOLE, DIPOLE_FREEZE, "COMPLETE_SAVED_STATE_DISCRIMINATOR", "files")
    context["input_payloads"] = {AUTONOMOUS.name: original_payload, DIPOLE.name: dipole_payload}
    n, eye = CONTRACT["dimension"], np.eye(CONTRACT["dimension"])
    pair_i, pair_j = np.triu_indices(n, 1)
    for label in CONTRACT["models"]:
        guard()
        old = original["models"][label]
        source = dipole["models"][label]
        h = np.asarray(old["hamiltonian_real"], dtype=float)
        if h.shape != (n, n) or not np.all(np.isfinite(h)):
            raise RuntimeError("Invalid saved Hamiltonian")
        energies = {key: complex_array(value, (n, n)) for key, value in source["local_energy_matrices"].items()}
        if set(energies) != {"HQ_midpoint", "HC_midpoint", "hL", "hR"}:
            raise RuntimeError("Local energy partition census changed")
        ck(label+":H_from_complete_partition", sum(energies.values()), h)
        ck(label+":H_symmetric", h, h.T)
        raw_ops = source["source_and_contact_matrices"]
        z = complex_array(raw_ops["Z_over_gamma0"], (n, n))
        beta = complex_array(raw_ops["volume_force"], (n, n))
        mixed = complex_array(raw_ops["mixed_contact_over_gamma0"], (n, n))
        dilation = complex_array(raw_ops["dilation_second_contact"], (n, n))
        operators = {"G0_Z_over_gamma0": z, "G1_minus_volume_force": -beta,
                     "C00_affine_zero": np.zeros((n, n)), "C01_mixed": mixed,
                     "C11_dilation": dilation}
        for name, operator in operators.items():
            ck(label+":"+name+":real", np.imag(operator), absolute=True)
            ck(label+":"+name+":hermitian", operator, operator.conj().T)
        require_passes()
        operators = {name: np.asarray(operator.real, dtype=float) for name, operator in operators.items()}
        values, vectors = np.linalg.eigh(h)  # Exactly once per model; no other eigensolver.
        context["eigensolves_completed"] += 1
        guard()
        if not np.all(np.isfinite(values)) or not np.all(np.isfinite(vectors)):
            raise RuntimeError("Nonfinite eigensolve output")
        # Keep finite raw eigendata even if a subsequent qualification fails.
        models[label] = {"stage": "RAW_EIGENDATA_CAPTURED",
                         "eigenvalues": values.tolist(),
                         "eigenvectors_columns": vectors.tolist()}
        ck(label+":eigenvalue_order", np.maximum(0., -np.diff(values)), absolute=True)
        ck(label+":orthogonality", vectors.T @ vectors, eye)
        ck(label+":H_reconstruction", (vectors*values) @ vectors.T, h)
        for index in range(n):
            ck(label+f":eigenpair:{index}", h @ vectors[:, index], values[index]*vectors[:, index])
        transformed = {name: vectors.T @ operator @ vectors for name, operator in operators.items()}
        for name, operator in operators.items():
            ck(label+":"+name+":basis_reconstruction", vectors @ transformed[name] @ vectors.T, operator)
        require_passes()
        numerical_width = CONTRACT["resolution_half_width_multiplier"]*max(1., float(np.max(np.abs(h))), float(np.max(np.abs(values))))
        clusters = overlap_groups(values, numerical_width)
        cluster_of = {}
        for cluster_index, cluster in enumerate(clusters):
            for index in cluster["indices"]:
                cluster_of[index] = cluster_index
        unresolved = any(len(group["indices"]) > 1 for group in clusters)
        gaps = values[pair_j]-values[pair_i]
        gi = np.stack([transformed["G0_Z_over_gamma0"], transformed["G1_minus_volume_force"]])
        source_pairs = gi[:, pair_i, pair_j].T
        pair_rows = [
            {"i": int(i), "j": int(j), "gap": float(gap),
             "same_unresolved_cluster": bool(cluster_of[int(i)] == cluster_of[int(j)]),
             "overlapping_eigenvalue_neighborhoods": bool(gap <= 2*numerical_width),
             "source_elements": source_pairs[k].tolist()}
            for k, (i, j, gap) in enumerate(zip(pair_i, pair_j, gaps))]
        ck(label+":pair_census", len(pair_rows), CONTRACT["pairs_per_model_and_case"], absolute=True)
        # Sort descriptors only: equal-gap membership remains uncertified.
        gap_order = np.argsort(gaps, kind="stable")
        gap_groups = overlap_groups(gaps[gap_order], 2*numerical_width)
        for group in gap_groups:
            group["pair_indices"] = [int(gap_order[index]) for index in group.pop("indices")]
            group["status"] = "NUMERICAL_TRANSITION_RESOLUTION_GROUP_NOT_EXACT_EQUAL_GAP"
        model = {
            "eigenvalues": values.tolist(), "eigenvectors_columns": vectors.tolist(),
            "numerical_resolution_half_width": numerical_width,
            "energy_resolution_groups": clusters,
            "unresolved_energy_clusters_present": unresolved,
            "neighborhoods_are_rigorous_intervals": False,
            "transformed_operators": {name: op.tolist() for name, op in transformed.items()},
            "operator_frobenius_norm_inputs_uncertified": {name: frobenius(op) for name, op in operators.items()},
            "pair_data": pair_rows, "transition_resolution_groups": gap_groups,
            "cases": {}, "stationary_quantities_withheld": unresolved,
            "stationary_scope": "WITHHELD_UNRESOLVED_ENERGY_CLUSTERS" if unresolved else "UNCERTIFIED_NUMERICAL_NONDEGENERATE_DIAGNOSTIC",
        }
        models[label] = model
        for endpoint in CONTRACT["endpoints"]:
            samples = old["cases"][endpoint]["samples"]
            if [sample["time"] for sample in samples] != CONTRACT["times"]:
                raise RuntimeError("Saved sample census changed")
            initial = complex_array(samples[0]["state"], (n,))
            expected_initial = np.zeros(n, complex)
            expected_initial[16 if endpoint == "minus" else 80] = 1.
            ck(label+":"+endpoint+":actual_initial_vector", initial, expected_initial, absolute=True)
            coefficients = vectors.T @ initial
            density = np.outer(coefficients, coefficients.conj())
            populations = np.abs(coefficients)**2
            ck(label+":"+endpoint+":initial_coefficients_reconstruct", vectors @ coefficients, initial, absolute=True)
            ck(label+":"+endpoint+":initial_density_reconstruct", vectors @ density @ vectors.T,
               np.outer(initial, initial.conj()), absolute=True)
            for name, operator in operators.items():
                ck(label+":"+endpoint+":"+name+":initial_expectation",
                   np.trace(density @ transformed[name]), np.vdot(initial, operator @ initial))
            saved_checks = []
            for sample in samples:
                guard()
                state = complex_array(sample["state"], (n,))
                numeric_coeff = vectors.T @ state
                ck(label+":"+endpoint+":"+str(sample["time"])+":norm", np.vdot(state, state), 1., absolute=True)
                ck(label+":"+endpoint+":"+str(sample["time"])+":numerical_energy_populations",
                   np.abs(numeric_coeff)**2, populations, absolute=True)
                saved_checks.append({"time": sample["time"],
                                     "maximum_population_difference": float(np.max(np.abs(np.abs(numeric_coeff)**2-populations)))})
                context["saved_states_checked"] += 1
            coherences = density[pair_i, pair_j]
            pair_norms = np.abs(coherences)
            ck(label+":"+endpoint+":pure_pair_norm_formula", pair_norms,
               np.sqrt(populations[pair_i]*populations[pair_j]), absolute=True)
            case = {
                "coefficients": packed(coefficients), "full_density_in_numerical_basis": packed(density),
                "diagonal_populations_in_numerical_basis": populations.tolist(),
                "pair_coherences": packed(coherences), "pair_trace_norm_inputs": pair_norms.tolist(),
                "pair_order": "model pair_data; all4560 entries retained",
                "saved_population_checks": saved_checks,
                "rho_d_uncertified": None, "stationary_pair_residues_uncertified": None,
                "inverse_gap_diagnostic": None,
                "withheld_reason": "Numerical neighborhoods do not resolve energy clusters; no dephasing within them or reciprocal evaluation" if unresolved else None,
            }
            model["cases"][endpoint] = case
            if not unresolved:
                if np.any(gaps <= 2*numerical_width):
                    raise RuntimeError("Reciprocal gate inconsistent with numerical cluster census")
                residues = ((populations[pair_i]-populations[pair_j])[:, None, None]
                            *source_pairs[:, :, None]*source_pairs[:, None, :])
                chi0 = 2*np.sum(residues/gaps[:, None, None], axis=0)
                chi2 = 2*np.sum(residues/gaps[:, None, None]**3, axis=0)
                moment = 2*np.sum(gaps[:, None, None]*residues, axis=0)
                rho_diagonal = (vectors*populations) @ vectors.T
                full_g = [operators["G0_Z_over_gamma0"], operators["G1_minus_volume_force"]]
                independent_moment = np.array([[np.trace(rho_diagonal @ comm(left, comm(h, right)))
                                                 for right in full_g] for left in full_g])
                ck(label+":"+endpoint+":stationary_moment_full_matrix", moment, independent_moment)
                ck(label+":"+endpoint+":numerical_diagonal_commutator", comm(h, rho_diagonal))
                contact = np.array([[0., float(np.trace(rho_diagonal @ operators["C01_mixed"]))],
                                    [float(np.trace(rho_diagonal @ operators["C01_mixed"])),
                                     float(np.trace(rho_diagonal @ operators["C11_dilation"]))]])
                residue_norms = np.sqrt(np.sum(residues**2, axis=(1, 2)))
                case["rho_d_uncertified"] = rho_diagonal.tolist()
                case["stationary_pair_residues_uncertified"] = residues.tolist()
                case["inverse_gap_diagnostic"] = {
                    "status": "UNCERTIFIED_NUMERICAL_NONDEGENERATE_DIAGNOSTIC",
                    "chi0": chi0.tolist(), "chi2": chi2.tolist(),
                    "first_moment_matrix": moment.tolist(), "contact_means": contact.tolist(),
                    "contact_minus_chi0": (contact-chi0).tolist(),
                    "minimum_positive_numerical_gap": float(np.min(gaps)),
                    "sum_residue_frobenius_over_gap5": float(np.sum(residue_norms/gaps**5)),
                    "large_T_age_envelope_coefficient": float(4*np.sum(pair_norms/gaps)),
                    "age_bound_formula": "min(2,2*sum(pair_norm*min(1,2/(gap*T)))); T symbolic",
                    "remainder_formula": "2*abs(z)^4*sum5/(1-abs(z/min_gap)^2); abs(z)<min_gap, hbar=1",
                    "numerically_certified": False,
                    "state_physically_dephased_or_formed": False,
                    "pair_residues_are_exact_resolved_lines": False,
                }
            ck(label+":"+endpoint+":case_pair_census", len(coherences), CONTRACT["pairs_per_model_and_case"], absolute=True)
            context["initial_states_completed"] += 1
            require_passes()
    ck("total:eigensolve_census", context["eigensolves_completed"], CONTRACT["eigensolve_count"], absolute=True)
    ck("total:initial_state_census", context["initial_states_completed"], CONTRACT["initial_state_count"], absolute=True)
    ck("total:saved_state_census", context["saved_states_checked"], CONTRACT["saved_state_count"], absolute=True)
    require_passes()
    guard()
    return {
        "schema": CONTRACT["schema"], "status": "COMPLETE_UNCERTIFIED_NUMERICAL_SPECTRAL_DIAGNOSTIC",
        "contract": CONTRACT, "files": frozen["files"], "freeze_sha256": digest(FREEZE),
        "intent_sha256": digest(INTENT), "input_payloads": context["input_payloads"],
        "models": models, "checks": checks, "check_count": len(checks), "failures": [],
        "census": {key: context[key] for key in ("eigensolves_completed", "initial_states_completed", "saved_states_checked")},
        "qualification_flags": FLAGS,
        "finite_readout_data": {
            "age_factor": "exp(-i*(Ei-Ej)*(w0+T/2))*sinc((Ei-Ej)*T/2), hbar=1",
            "sinc_zero_limit": 1., "time_parameters_chosen": False,
            "all_numerical_pair_coherences_retained": True,
            "exact_spectrum_or_continuum_claimed": False,
        },
        "resources": {"elapsed_seconds": time.monotonic()-started,
                      "cpu_seconds": time.process_time()-cpu_started,
                      "maximum_self_rss_bytes": rss(), "numpy_version": np.__version__},
    }


def cpu_limit_handler(signum, frame):
    raise RuntimeError("Frozen CPU soft limit reached")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--freeze", action="store_true")
    mode.add_argument("--run", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.freeze:
        if args.output is not None:
            parser.error("--freeze cannot take --output")
        atomic_exclusive(FREEZE, freeze_packet())
        print(json.dumps({"status": "PROSPECTIVE_FREEZE_CREATED", "path": str(FREEZE), "sha256": digest(FREEZE)}))
        return
    if args.output is not None and (args.output.resolve() != RESULT or RESULT.exists()):
        parser.error("Output must be the fixed previously absent result path")
    if INTENT.exists():
        parser.error("Existing intent forbids silent duplicate execution")
    if read_json(FREEZE) != freeze_packet():
        parser.error("Freeze does not authenticate current inputs/source")
    atomic_exclusive(INTENT, {
        "schema": CONTRACT["schema"], "status": "NUMERICAL_ATTEMPT_INTENT",
        "started_utc": datetime.now(timezone.utc).isoformat(), "pid": os.getpid(),
        "freeze_sha256": digest(FREEZE), "source_sha256": digest(Path(__file__)),
        "output": str(RESULT) if args.output is not None else "stdout",
        "qualification_flags": FLAGS,
    })
    resource.setrlimit(resource.RLIMIT_CPU, (CONTRACT["cpu_soft_seconds"], CONTRACT["cpu_hard_seconds"]))
    signal.signal(signal.SIGXCPU, cpu_limit_handler)
    started, cpu_started = time.monotonic(), time.process_time()
    context = {}
    try:
        result = analyze(context)
    except Exception as exc:
        maximum_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result = {
            "schema": CONTRACT["schema"], "status": "TECHNICAL_OR_ARITHMETIC_FAILURE_RETAINED",
            "error_type": type(exc).__name__, "error": str(exc), "partial_evidence": context,
            "freeze_sha256": digest(FREEZE), "intent_sha256": digest(INTENT),
            "qualification_flags": FLAGS,
            "resources": {"elapsed_seconds": time.monotonic()-started,
                          "cpu_seconds": time.process_time()-cpu_started,
                          "maximum_self_rss_bytes": int(maximum_rss if sys.platform == "darwin" else maximum_rss*1024)},
        }
    result["payload_sha256"] = hashlib.sha256(encode(result)).hexdigest()
    if args.output is None:
        rendered = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
        if len(rendered.encode()) > CONTRACT["max_file_bytes"]:
            raise RuntimeError("Stdout result exceeds the frozen size bound")
        print(rendered)
    else:
        atomic_exclusive(RESULT, result)
        print(json.dumps({"status": result["status"], "path": str(RESULT),
                          "sha256": digest(RESULT), "payload_sha256": result["payload_sha256"],
                          "check_count": result.get("check_count")}))
    if result["status"] != "COMPLETE_UNCERTIFIED_NUMERICAL_SPECTRAL_DIAGNOSTIC":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
