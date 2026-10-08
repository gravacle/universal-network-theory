"""Read-only scientific inputs: 20 saved states, no propagation or eigensolve."""
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
PROTOCOL = HERE / "NATIVE_ENERGY_DIPOLE_SAVED_STATE_V001_PROTOCOL.md"
FREEZE = HERE / "NATIVE_ENERGY_DIPOLE_SAVED_STATE_V001_FROZEN.json"
RESULT = HERE / "NATIVE_ENERGY_DIPOLE_SAVED_STATE_V001_RESULTS.json"
INPUT = HERE / "NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_RESULTS.json"
ORIGINAL_FREEZE = HERE / "NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_FROZEN.json"
PINS = {
    INPUT.name: "bc35b592f5547e1f5fc566411ec7e8f7175776d20569fbccf0ae3e6457e74fc1",
    ORIGINAL_FREEZE.name: "642348d737439d2b87f2abb0f7d0a499955409745554f1bf85cb5b9937474d12",
    "NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md": "81b3c455d761667e2645117699e8986c7030290de8b54bc45879112237d2db96",
    "NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_PROTOCOL.md": "724f8d8c4a7bbcc7ce4ba9fa37f750e92d96b732db78ef1cc1347fcd52a7a7d5",
    "native_autonomous_volume_formation_v001.py": "8cdffaded72a83d6117dd0bf61e944d1c5b9f0e8800e4a7f2dd36ff477175317",
    "NATIVE_THERMAL_PACKET_PROTOCOL_V001.md": "08b9d07768c0f6c4c2e635b9affe623f1ca04914d2d53e1524d2a5a013ddf632",
    "native_thermal_packet_v001.py": "380e736479e7dd9a670a10a06410bb27a6e4aff44e8c23f9fe52f03a7a4ff837",
    "../recovered_sources/BS_MICRO_ACTION.md": "00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec",
    "record_addition_compute.py": "4df3bbc8b38ad6b602841b7b28a7a59d37e69d60286f7a2ef11c37ddc150ce10",
    "NATIVE_OPERATIONAL_SOURCE_CLOCK_VOLUME_CANDIDATES_V001.md": "fbddff9520f898bf888600ac62a03729d25b7cf4ad230196b04505f81853304b",
    "NATIVE_SOURCE_BRIDGE_DECISION.md": "c82040f7bebbdefcec4e782f8afb86c6c1c3f2367775f5fd2e6dbbe6159c737a",
    "NATIVE_RULER_SOURCE_AND_NORMAL_FORM_V001.md": "335044ff025cfd831f92ed34574098fb7fe42841047c2b657d40962f6439568c",
}
CONTRACT = {
    "basis_index": "32*Q+16*C+8*rL+4*rR+2*a+c", "dimension": 96, "hbar": 1.,
    "models": ["A", "B"], "endpoints": ["minus", "plus"],
    "times": [0., .01, .02, .04, .08], "state_count": 20,
    "gamma0": "ell0/(2*c^2), symbolic; Ztilde=Z/gamma0",
    "arithmetic_tolerance": 2e-10, "threads": 1,
    "cpu_seconds": 30, "wall_seconds": 60, "rss_bytes": 256*1024*1024,
    "max_checks": 4096, "max_input_bytes": 8*1024*1024,
    "propagations": 0, "eigensolves": 0, "fits": 0,
}
FLAGS = {name: False for name in (
    "native_metric_derived", "physical_source_independently_validated",
    "continuous_soft_spectrum_established", "passive_mechanical_mapping_qualified",
    "initial_galaxy_polarization_generated", "vacuum_normalization_predicted",
    "observational_success", "stage3_complete")}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def identities():
    identities_found = {name: sha(HERE/name) for name in PINS}
    if identities_found != PINS:
        raise RuntimeError("Pinned input/model source changed")
    identities_found[PROTOCOL.name] = sha(PROTOCOL)
    identities_found[Path(__file__).name] = sha(Path(__file__))
    return identities_found


def freeze_packet():
    return {"schema": "native-energy-dipole-saved-state-v001", "files": identities(),
            "contract": CONTRACT, "physical_promotion_flags": FLAGS}


def exclusive_write(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def comm(a, b):
    return a @ b-b @ a


def anti(a, b):
    return a @ b+b @ a


def matrix_json(value):
    return {"real": value.real.tolist(), "imag": value.imag.tolist()}


def analyze(context):
    start, cpu_start = time.monotonic(), time.process_time()
    resource.setrlimit(resource.RLIMIT_CPU, (CONTRACT["cpu_seconds"], CONTRACT["cpu_seconds"]+1))
    frozen = json.loads(FREEZE.read_text())
    if frozen != freeze_packet():
        raise RuntimeError("Discriminator prospective freeze mismatch")
    if INPUT.stat().st_size > CONTRACT["max_input_bytes"]:
        raise RuntimeError("Input size exceeds bound")
    original = json.loads(INPUT.read_text())
    declared_payload = original.pop("payload_sha256")
    if hashlib.sha256(encode(original)).hexdigest() != declared_payload:
        raise RuntimeError("Original scientific payload mismatch")
    if original["status"] != "COMPLETE_CONDITIONAL_APPARATUS_CHECKS" or original["failures"]:
        raise RuntimeError("Input is not a successful conditional apparatus calculation")
    if any(original["physical_promotion_flags"].values()):
        raise RuntimeError("Input has unexpected physical promotion")
    old_freeze = json.loads(ORIGINAL_FREEZE.read_text())
    if original["freeze_sha256"] != sha(ORIGINAL_FREEZE) or original["input_files"] != old_freeze["files"]:
        raise RuntimeError("Original freeze/input identities disagree")
    for name, digest in old_freeze["files"].items():
        if sha(HERE/name) != digest:
            raise RuntimeError("Original nested source identity mismatch: "+name)
    checks, results = [], {}
    context.update({"checks": checks, "models": results, "input_sha256": sha(INPUT),
                    "input_payload_sha256": declared_payload, "freeze_sha256": sha(FREEZE)})

    def rss():
        value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(value if sys.platform == "darwin" else value*1024)

    def guard():
        if time.monotonic()-start > CONTRACT["wall_seconds"] or rss() > CONTRACT["rss_bytes"]:
            raise RuntimeError("Arithmetic resource bound exceeded")
        if len(checks) > CONTRACT["max_checks"]:
            raise RuntimeError("Check census exceeds bound")

    def ck(name, actual, expected=0., absolute=False):
        guard()
        av, ev = np.asarray(actual), np.asarray(expected)
        error = float(np.max(np.abs(av-ev)))
        scale = 1. if absolute else max(1., float(np.max(np.abs(av))), float(np.max(np.abs(ev))))
        checks.append({"name": name, "residual": error, "scale": scale,
                       "tolerance": CONTRACT["arithmetic_tolerance"],
                       "passed": bool(math.isfinite(error) and error <= CONTRACT["arithmetic_tolerance"]*scale)})

    def ex(psi, op, name):
        value = np.vdot(psi, op @ psi)
        ck(name+":real", value.imag, absolute=True)
        return float(value.real)

    identity = np.eye(96, dtype=complex)
    incidence = np.zeros((96, 96), complex)
    xa = np.zeros((96, 96), complex)
    dp, dr, dx, pc = (np.zeros((96, 96), complex) for _ in range(4))
    hq, hc = np.zeros((96, 96), complex), np.zeros((96, 96), complex)
    s_values = np.array([2**(-1/3), 1., 2**(1/3)])
    ruler = np.diag(np.repeat(s_values, 32)).astype(complex)
    inverse_ruler = np.diag(np.repeat(1/s_values, 32)).astype(complex)
    volume = np.diag(np.repeat(s_values**3, 32)).astype(complex)
    inverse_volume = np.diag(np.repeat(s_values**-3, 32)).astype(complex)
    # Independent basis-row construction; no native producer is imported.
    local_held, local_transport, local_copy = [[np.zeros((96, 96), complex) for _ in range(2)] for _ in range(3)]
    for basis in range(96):
        q, remainder = divmod(basis, 32)
        controller, native = divmod(remainder, 16)
        rl, rr, n, carrier = ((native >> bit) & 1 for bit in (3, 2, 1, 0))
        incidence[basis, basis] = n
        xa[basis ^ 2, basis] = 1.
        dp[basis, basis] = 2*carrier-1
        dr[basis, basis] = rr-rl
        dx[basis ^ 4, basis] += 1.
        dx[basis ^ 8, basis] -= 1.
        pc[basis, basis] = controller
        hq[basis, basis] = 2. if q == 1 else 1.
        hc[basis, basis] = 1.
        hc[basis ^ 16, basis] = -1.
        for neighbor in (q-1, q+1):
            if 0 <= neighbor < 3:
                hq[32*neighbor+remainder, basis] = -1.
        for node, record, record_bit in ((0, rl, 8), (1, rr, 4)):
            occupied_carrier = float(carrier == node)
            local_held[node][basis, basis] = (n-1)**2+occupied_carrier+record+2*n+.25*n*occupied_carrier-.5*n*record
            local_held[node][basis ^ 2, basis] = -.5
            local_held[node][basis ^ 1, basis] = -.25*n
            local_transport[node][basis, basis] = .25*n*occupied_carrier
            local_transport[node][basis ^ 1, basis] = -.25*n
            local_copy[node][basis ^ record_bit, basis] = controller
    d0 = (identity+.25*incidence) @ dp+(identity-.5*incidence) @ dr+pc @ dx
    transport = sum(local_transport)
    ck("native:owned_local_difference", local_held[1]-local_held[0]+local_copy[1]-local_copy[0], d0)
    ck("native:transport_difference", local_transport[1]-local_transport[0], .25*incidence @ dp)
    state_count = 0
    for model in CONTRACT["models"]:
        guard()
        if model == "A":
            local = [inverse_ruler @ (local_held[v]+local_copy[v]) for v in range(2)]
            beta = sum(local)
            c_etaeta = beta.copy()
            mixed = np.zeros((96, 96), complex)
            formula_z = d0
            expected_n_moment = inverse_ruler @ xa
        else:
            local = [local_held[v]-local_transport[v]-identity+inverse_ruler @ local_transport[v]+volume+local_copy[v]
                     for v in range(2)]
            beta = inverse_ruler @ transport-6*volume
            c_etaeta = inverse_ruler @ transport+18*volume
            formula_z = (ruler+.25*incidence) @ dp+ruler @ (identity-.5*incidence) @ dr+ruler @ pc @ dx
            mixed = ruler @ (dp+(identity-.5*incidence) @ dr+pc @ dx)
            expected_n_moment = xa
        pieces = {"HQ_midpoint": hq, "HC_midpoint": hc, "hL": local[0], "hR": local[1]}
        h = sum(pieces.values())
        saved_h = np.asarray(original["models"][model]["hamiltonian_real"], dtype=complex)
        ck(model+":independent_H", h, saved_h)
        for name, op in pieces.items():
            ck(model+":"+name+":hermitian", op, op.conj().T)
        difference = local[1]-local[0]
        z = ruler @ difference
        pressure = inverse_volume @ beta/3
        ck(model+":physical_source_formula", z, formula_z)
        ck(model+":source_hermitian", z, z.conj().T)
        ck(model+":pressure_hermitian", pressure, pressure.conj().T)
        if model == "A":
            ck(model+":source_Q_independence", comm(hq, z))
            ck(model+":mixed_contact_zero", mixed)
        else:
            ck(model+":mixed_contact_identity", z-mixed, .25*incidence @ dp)
            # Differentiating the explicit s-linear mixed formula gives itself.
            mixed_second = ruler @ dp+ruler @ (identity-.5*incidence) @ dr+ruler @ pc @ dx
            ck(model+":second_mixed_contact", mixed_second, mixed)
        mz = comm(z, comm(h, z))
        mn = comm(incidence, comm(h, incidence))
        ck(model+":incidence_moment_operator", mn, expected_n_moment)
        ck(model+":dipole_moment_hermitian", mz, mz.conj().T)
        energy_derivatives = {name: 1j*comm(h, op) for name, op in pieces.items()}
        for name, op in pieces.items():
            entering = np.zeros((96, 96), complex)
            for other_name, other in pieces.items():
                current = 1j*comm(other, op)
                reverse = 1j*comm(op, other)
                ck(model+":current_antisymmetry:"+other_name+":"+name, current, -reverse)
                entering += current
            ck(model+":node_ward:"+name, entering, energy_derivatives[name])
        ck(model+":total_energy_ward", sum(energy_derivatives.values()))
        ruler_dot, difference_dot = 1j*comm(h, ruler), 1j*comm(h, difference)
        moving_term = anti(ruler_dot, difference)/2
        energy_term = anti(ruler, difference_dot)/2
        zdot = 1j*comm(h, z)
        ck(model+":moving_ruler_ward", zdot, moving_term+energy_term)
        operators = {"Z_over_gamma0": z, "volume_force": beta, "incidence": incidence}
        contacts = {"dilation_second_contact": c_etaeta, "mixed_contact_over_gamma0": mixed,
                    "pressure_in_energy_over_V0": pressure}
        rows = []
        results[model] = {"rows": rows,
                          "source_and_contact_matrices": {name: matrix_json(op) for name, op in {**operators, **contacts}.items()},
                          "local_energy_matrices": {name: matrix_json(op) for name, op in pieces.items()},
                          "bare_Q_source_commutator_maxabs": float(np.max(np.abs(comm(hq, z))))}
        for endpoint in CONTRACT["endpoints"]:
            samples = original["models"][model]["cases"][endpoint]["samples"]
            if [sample["time"] for sample in samples] != CONTRACT["times"]:
                raise RuntimeError("Saved time census changed")
            for sample in samples:
                guard()
                t = sample["time"]
                tag = model+":"+endpoint+":"+str(t)
                psi = np.asarray(sample["state"]["real"])+1j*np.asarray(sample["state"]["imag"])
                if psi.shape != (96,) or not np.all(np.isfinite(psi)):
                    raise RuntimeError("Invalid saved state")
                ck(tag+":norm", np.vdot(psi, psi), 1.)
                means = {name: ex(psi, op, tag+":"+name) for name, op in operators.items()}
                contact_means = {name: ex(psi, op, tag+":"+name) for name, op in contacts.items()}
                sz, sn = ex(psi, mz, tag+":S_Z"), ex(psi, mn, tag+":S_n")
                ck(tag+":incidence_analytic_moment", sn, ex(psi, expected_n_moment, tag+":S_n_formula"))
                for name, op, moment in (("Z", z, sz), ("n", incidence, sn)):
                    applied = op @ psi
                    independent = 2*(np.vdot(applied, h @ applied).real-np.vdot(op @ applied, h @ psi).real)
                    ck(tag+":"+name+":moment_independent", moment, independent)
                if t == 0.:
                    ck(tag+":initial_dipole_null", sz, absolute=True)
                names = list(operators)
                centered = [(operators[name]-means[name]*identity) @ psi for name in names]
                gram = np.array([[np.vdot(left, right) for right in centered] for left in centered])
                direct = np.array([[np.vdot(psi, operators[left] @ operators[right] @ psi)-means[left]*means[right]
                                    for right in names] for left in names])
                ck(tag+":connected_gram_definition", gram, direct)
                ck(tag+":gram_hermitian", gram, gram.conj().T)
                for j in range(3):
                    ck(tag+f":variance_nonnegative:{j}", max(0., -float(gram[j, j].real)), absolute=True)
                    for k in range(j):
                        excess = abs(gram[j, k])**2-gram[j, j].real*gram[k, k].real
                        ck(tag+f":Cauchy_Schwarz:{j}:{k}", max(0., float(excess)), absolute=True)
                current_means = {name: ex(psi, op, tag+":current:"+name) for name, op in energy_derivatives.items()}
                ck(tag+":sum_energy_currents", sum(current_means.values()), absolute=True)
                moving = ex(psi, moving_term, tag+":ruler_motion")
                internal = ex(psi, energy_term, tag+":local_energy_motion")
                dipole_rate = ex(psi, zdot, tag+":dipole_rate")
                ck(tag+":dipole_ward_expectation", dipole_rate, moving+internal)
                threshold = CONTRACT["arithmetic_tolerance"]
                classification = "positive" if sz > threshold else "negative" if sz < -threshold else "unresolved_at_arithmetic_resolution"
                rows.append({"endpoint": endpoint, "time": t, "means": means, "contact_means": contact_means,
                             "S_Z_over_gamma0_squared": sz, "S_n": sn,
                             "S_Z_raw_sign": "positive" if sz > 0 else "negative" if sz < 0 else "zero",
                             "S_Z_arithmetic_resolution_classification": classification,
                             "gram_operator_order": names, "connected_gram": matrix_json(gram),
                             "symmetric_covariance": gram.real.tolist(),
                             "equal_time_minus_source_response": (-2*gram.imag).tolist(),
                             "response_convention": {
                                 "stored_matrix": "chi_AB=i<[A,B]>=-2 Im Gram_AB; hbar=1",
                                 "minus_source": "H=H0-f B gives delta<A>=+integral chi_AB f",
                                 "acceleration_source": "H=H0+a Z gives delta<A>=-integral chi_AZ a",
                                 "acceleration_response_sign_relative_to_chi": -1},
                             "energy_currents": current_means, "dipole_rate_over_gamma0": dipole_rate,
                             "ruler_motion_contribution": moving, "local_energy_motion_contribution": internal})
                state_count += 1
        moments = [row["S_Z_over_gamma0_squared"] for row in rows]
        results[model]["descriptive_moment_range"] = {"minimum": min(moments), "maximum": max(moments),
                                                      "maximum_minus_minimum": max(moments)-min(moments)}
    ck("complete_state_census", state_count, CONTRACT["state_count"], absolute=True)
    guard()
    failures = [row for row in checks if not row["passed"]]
    return {"schema": frozen["schema"], "status": "COMPLETE_SAVED_STATE_DISCRIMINATOR" if not failures else "FAILED_ARITHMETIC_RETAINED",
            "input_sha256": sha(INPUT), "input_payload_sha256": declared_payload,
            "freeze_sha256": sha(FREEZE), "files": frozen["files"], "contract": CONTRACT,
            "models": results, "checks": checks, "check_count": len(checks), "failures": failures,
            "state_count": state_count, "physical_promotion_flags": FLAGS,
            "interpretation": {"initial_null_is_analytic_control": True,
                               "nonzero_strictly_positive_fixed_moment_cannot_describe_entire_included_history": True,
                               "late_positive_moment_suffices_for_passive_mapping": False,
                               "desired_sign_was_a_pass_gate": False,
                               "observations_or_new_propagations_used": False},
            "resources": {"elapsed_seconds": time.monotonic()-start, "cpu_seconds": time.process_time()-cpu_start,
                          "maximum_self_rss_bytes": rss(), "numpy_version": np.__version__}}


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
        exclusive_write(FREEZE, freeze_packet())
        print(json.dumps({"status": "PROSPECTIVE_FREEZE_CREATED", "path": str(FREEZE), "sha256": sha(FREEZE)}))
        return
    if args.output is not None:
        if args.output.resolve() != RESULT or RESULT.exists():
            parser.error("Output must be the fixed previously absent result file")
    context = {}
    try:
        result = analyze(context)
    except Exception as exc:
        result = {"status": "TECHNICAL_FAILURE_RETAINED", "error_type": type(exc).__name__, "error": str(exc),
                  "partial_evidence": context, "physical_promotion_flags": FLAGS}
    result["payload_sha256"] = hashlib.sha256(encode(result)).hexdigest()
    if args.output is None:
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    else:
        exclusive_write(RESULT, result)
        print(json.dumps({"status": result["status"], "path": str(RESULT), "sha256": sha(RESULT),
                          "payload_sha256": result["payload_sha256"], "check_count": result.get("check_count")}))
    if result["status"] != "COMPLETE_SAVED_STATE_DISCRIMINATOR":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
