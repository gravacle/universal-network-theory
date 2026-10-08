"""Prospective exact 16D native record-addition test; root is sole worker."""
import os
import sys

sys.dont_write_bytecode = True
for key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"

import hashlib
import json
import math
from pathlib import Path
import resource
import time
import tempfile

import numpy as np

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent
TOL = 1e-11
HOLD_TIMES = (0., .25, .5, 1., 2.)
PARAMETERS = dict(h=1., Delta=4., U_d=1., d_star=1., epsilon_psi=1.,
                  epsilon_r=1., epsilon_w=0., t_hop=.5, lambda_R=.5,
                  lambda_J=.25, g=1.)
SOURCES = (
    HERE / "RECORD_ADDITION_PROTOCOL.md",
    Path(__file__).resolve(),
    HERE / "NATIVE_TEMPORAL_KERNEL.md",
    HERE.parent / "recovered_sources/BS_MICRO_ACTION.md",
    WORKSPACE / "UNT_RECORD_TO_GEOMETRY_MINIMAL_JOIN_2026-09-27_V001/compute_join.py",
)
I2 = np.eye(2)
X2 = np.array([[0., 1.], [1., 0.]])
Z2 = np.diag([1., -1.])
N2 = np.diag([0., 1.])
# Native copy-current convention i(|B><x|-|x><B|), minus Pauli Y.
Y2 = np.array([[0., 1j], [-1j, 0.]])
RAISE2 = np.array([[0., 0.], [1., 0.]])
I = np.eye(16)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode()


def save_new(name, value):
    content = json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+"\n"
    with tempfile.NamedTemporaryFile(mode="w",dir=HERE,prefix=name+".partial.",delete=False) as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
        temporary = Path(handle.name)
    os.link(temporary,HERE/name)
    temporary.unlink()


def embed(matrix, factor):
    out = np.array([[1. + 0j]])
    for index in range(4):
        out = np.kron(out, matrix if index == factor else I2)
    return out


def comm(a, b):
    return a @ b - b @ a


def vector_json(v):
    return {"real": v.real.tolist(), "imag": v.imag.tolist()}


def operators():
    return dict(QL=embed(N2, 0), QR=embed(N2, 1), n=embed(N2, 2),
                XL=embed(X2, 0), XR=embed(X2, 1), Xa=embed(X2, 2),
                Za=embed(Z2, 2), XC=embed(X2, 3), YL=embed(Y2, 0),
                YR=embed(Y2, 1), YC=embed(Y2, 3),
                AL=embed(RAISE2, 0), AR=embed(RAISE2, 1),
                carrier_right=embed(N2, 3))


def hamiltonian(p, o):
    r = o["QL"] + o["QR"]
    degree = o["n"] - p["d_star"] * I
    terms = {
        "incidence_flip": -p["h"] * o["Xa"],
        "incidence_bias": p["Delta"] * o["n"],
        "both_endpoint_degree_penalties": 2 * p["U_d"] * degree @ degree,
        "carrier_occupation": p["epsilon_psi"] * I,
        "both_record_storage": p["epsilon_r"] * r,
        "both_writer_storage": 2 * p["epsilon_w"] * I,
        "carrier_hopping": -p["t_hop"] * o["n"] @ o["XC"],
        "record_incidence_feedback": -p["lambda_R"] * o["n"] @ r,
        "current_squared_feedback": p["lambda_J"] * o["n"] @ o["YC"] @ o["YC"],
        "copy_left": p["g"] * o["XL"],
        "copy_right": p["g"] * o["XR"],
    }
    return sum(terms.values()), terms


def spectral_propagator(h, duration):
    values, vectors = np.linalg.eigh(h)
    return (vectors * np.exp(-1j * duration * values)) @ vectors.conj().T


def taylor_propagator(h, duration):
    """Scaled Taylor recurrence, independently of eigenvectors/eigenvalues."""
    a = -1j * duration * h
    norm = float(np.linalg.norm(a, ord=np.inf))
    squarings = max(0, math.ceil(math.log2(norm / .5))) if norm else 0
    a = a / (2 ** squarings)
    scaled_norm = float(np.linalg.norm(a, ord=np.inf))
    result = I.astype(complex).copy()
    term = I.astype(complex).copy()
    magnitude = 1.
    for order in range(1, 201):
        term = term @ a / order
        result += term
        magnitude *= scaled_norm / order
        tail = math.exp(scaled_norm) * magnitude * scaled_norm / (order + 1)
        if tail <= 1e-18:
            break
    else:
        raise ArithmeticError("Taylor tail did not meet the frozen criterion")
    for _ in range(squarings):
        result = result @ result
    return result, dict(order=order, squarings=squarings,
                        exact_arithmetic_tail_bound=tail)


def run():
    started = time.perf_counter()
    freeze_path = HERE / "RECORD_ADDITION_FROZEN.json"
    frozen = json.loads(freeze_path.read_text())
    expected_files = {str(path.relative_to(WORKSPACE)): digest(path) for path in SOURCES}
    if frozen["files"] != expected_files:
        raise RuntimeError("Source freeze mismatch; no numerical run performed")
    checks, cases = [], []

    def check(name, a, b=0., tolerance=TOL):
        error = float(np.max(np.abs(np.asarray(a) - np.asarray(b))))
        checks.append(dict(name=name, residual=error, tolerance=tolerance,
                           passed=bool(math.isfinite(error) and error <= tolerance)))

    def truth(name, condition):
        check(name, 0. if condition else 1., tolerance=0.)

    def ex(v, a, label):
        value = np.vdot(v, a @ v)
        check(label + ":real", value.imag)
        return float(value.real)

    o = operators()
    r = o["QL"] + o["QR"]
    counts = [(I-o["QL"]) @ (I-o["QR"]),
              o["QL"] @ (I-o["QR"]) + (I-o["QL"]) @ o["QR"],
              o["QL"] @ o["QR"]]
    initial = I[:, 0].astype(complex)
    for label, changes in (("native", {}), ("feedback_off", {"lambda_R": 0.}),
                           ("copying_off", {"g": 0.})):
        p = dict(PARAMETERS, **changes)
        hf, tf = hamiltonian(p, o)
        hh, th = hamiltonian(dict(p, g=0.), o)
        tag = label + ":"
        check(tag+"formation_hermitian", hf, hf.conj().T)
        check(tag+"hold_hermitian", hh, hh.conj().T)
        for name, term in tf.items():
            check(tag+name+":hermitian", term, term.conj().T)
        compact = 3*I + r - o["Xa"] + (2.25*I-p["lambda_R"]*r-.5*o["XC"]) @ o["n"]
        check(tag+"compact_hold", hh, compact)
        check(tag+"count_resolution", sum(counts), I)
        check(tag+"held_count_commutes", comm(hh, r))
        check(tag+"held_left_record_commutes", comm(hh, o["QL"]))
        check(tag+"held_right_record_commutes", comm(hh, o["QR"]))
        check(tag+"carrier_X_conserved_in_formation", comm(hf, o["XC"]))
        check(tag+"record_source_double_commutator", comm(r, comm(hf, r)),
              -p["g"]*(o["XL"]+o["XR"]))
        check(tag+"record_source_first_commutator", comm(hf, r),
              -1j*p["g"]*(o["YL"]+o["YR"]))
        check(tag+"incidence_source_double_commutator", comm(o["n"], comm(hf, o["n"])),
              p["h"]*o["Xa"])
        projectors, spectrum, analytical_values = [], [], []
        reconstruction = np.zeros((16, 16), complex)
        for count in range(3):
            for s in (1, -1):
                x = 2.25-p["lambda_R"]*count-.5*s
                d = math.hypot(x, 2.)
                for beta in (-1, 1):
                    energy = 3+count+(x+beta*d)/2
                    proj = counts[count] @ ((I-beta*(2*o["Xa"]+x*o["Za"])/d)/2) @ ((I+s*o["XC"])/2)
                    rank = (1, 2, 1)[count]
                    stem = tag+f"R{count}:s{s}:beta{beta}"
                    check(stem+":projector", proj @ proj, proj)
                    check(stem+":rank", np.trace(proj), rank)
                    check(stem+":energy", hh @ proj, energy*proj)
                    check(stem+":record_count", r @ proj, count*proj)
                    projectors.append(proj)
                    analytical_values.extend([energy]*rank)
                    reconstruction += energy*proj
                    spectrum.append(dict(R=count, s=s, beta=beta, energy=energy,
                                         multiplicity=rank, x=x, gap=d))
        check(tag+"full_projector_resolution", sum(projectors), I)
        for left in range(len(projectors)):
            for right in range(left):
                check(tag+f"orthogonal:{left}:{right}", projectors[left] @ projectors[right])
        check(tag+"full_spectral_reconstruction", reconstruction, hh)
        check(tag+"full_eigenvalue_multiset", sorted(analytical_values), np.linalg.eigvalsh(hh))
        addition = []
        energies = {(row["R"], row["s"], row["beta"]): row["energy"] for row in spectrum}
        for s in (1, -1):
            x = 2.25-.5*s
            gaps = [math.hypot(x-p["lambda_R"]*count, 2.) for count in range(3)]
            for beta in (-1, 1):
                e = [energies[count, s, beta] for count in range(3)]
                curvature = e[2]-2*e[1]+e[0]
                predicted = beta*(gaps[2]-2*gaps[1]+gaps[0])/2
                check(tag+f"curvature_formula:{s}:{beta}", curvature, predicted)
                if p["lambda_R"]:
                    truth(tag+f"curvature_sign:{s}:{beta}", beta*curvature > 0.)
                    rad = (math.sqrt(89)-math.sqrt(113) if s == 1
                           else math.sqrt(145)-math.sqrt(185))
                    check(tag+f"first_addition_radical:{s}:{beta}", e[1]-e[0], .75+beta*rad/8)
                else:
                    check(tag+f"feedback_off_curvature:{s}:{beta}", curvature)
                addition.append(dict(s=s, beta=beta, E0=e[0], E1=e[1], E2=e[2],
                                     first_addition=e[1]-e[0], second_addition=e[2]-e[1],
                                     second_difference=curvature))
        uf = spectral_propagator(hf, 1.)
        ut, detail = taylor_propagator(hf, 1.)
        check(tag+"formation_unitarity", uf.conj().T @ uf, I)
        check(tag+"formation_taylor_unitarity", ut.conj().T @ ut, I)
        check(tag+"formation_cross_method", uf, ut)
        formed = uf @ initial
        check(tag+"formed_norm", np.vdot(formed, formed), 1.)
        e_initial = ex(initial, hf, tag+"initial_energy")
        check(tag+"initial_energy_value", e_initial, 3.)
        e_form = ex(formed, hf, tag+"formed_energy")
        check(tag+"formation_energy_conservation", e_form, e_initial)
        work = ex(formed, hh-hf, tag+"quench_work")
        copy_mean = ex(formed, o["XL"]+o["XR"], tag+"copy_mean")
        check(tag+"quench_work_formula", work, -p["g"]*copy_mean)
        e_hold = ex(formed, hh, tag+"held_initial_energy")
        check(tag+"quench_energy_ledger", e_hold, e_initial+work)
        band_weights = []
        for row, proj in zip(spectrum, projectors):
            weight = ex(formed, proj, tag+f"weight:{row['R']}:{row['s']}:{row['beta']}")
            truth(tag+f"weight_positive:{row['R']}:{row['s']}:{row['beta']}", weight >= -TOL)
            band_weights.append(dict(**row, weight=weight))
        check(tag+"weights_sum", sum(row["weight"] for row in band_weights), 1.)
        check(tag+"prepared_energy_from_all_bands", sum(row["weight"]*row["energy"] for row in band_weights), e_hold)
        instantaneous = []
        for side in ("L", "R"):
            a, blank = o["A"+side], I-o["Q"+side]
            cost_op = blank @ (p["epsilon_r"]*I-p["lambda_R"]*o["n"])
            actual_op = a.conj().T @ hh @ a-blank @ hh @ blank
            check(tag+"instantaneous_addition_identity:"+side, actual_op, cost_op)
            probability = ex(formed, blank, tag+"blank_probability:"+side)
            numerator = ex(formed, actual_op, tag+"addition_work_numerator:"+side)
            expected = p["epsilon_r"]*probability-p["lambda_R"]*ex(formed, blank @ o["n"], tag+"blank_link:"+side)
            check(tag+"instantaneous_prepared_work:"+side, numerator, expected)
            instantaneous.append(dict(endpoint=side, blank_probability=probability,
                                      unnormalized_addition_work=numerator,
                                      conditional_cost=numerator/probability if probability > TOL else None))
        current = p["g"]*ex(formed, o["YL"]+o["YR"], tag+"current_formula")
        check(tag+"production_current", ex(formed, 1j*comm(hf, r), tag+"current_operator"), current)
        record_slope = -p["g"]*copy_mean
        check(tag+"record_response_slope", ex(formed, comm(r, comm(hf, r)), tag+"record_slope_operator"), record_slope)
        incidence_slope = p["h"]*ex(formed, o["Xa"], tag+"incidence_slope_formula")
        hold = []
        formed_count = ex(formed, r, tag+"formed_count")
        for duration in HOLD_TIMES:
            uh = spectral_propagator(hh, duration)
            uth, td = taylor_propagator(hh, duration)
            ht = tag+f"hold{duration}:"
            check(ht+"cross_method", uh, uth)
            check(ht+"unitarity", uh.conj().T @ uh, I)
            check(ht+"taylor_unitarity", uth.conj().T @ uth, I)
            state = uh @ formed
            check(ht+"norm", np.vdot(state, state), 1.)
            check(ht+"energy_conservation", ex(state, hh, ht+"energy"), e_hold)
            count = ex(state, r, ht+"record_count")
            check(ht+"record_conservation", count, formed_count)
            check(ht+"carrier_X", ex(state, o["XC"], ht+"carrier_X_mean"))
            terms = {name: ex(state, term, ht+name) for name, term in th.items()}
            check(ht+"term_energy_sum", sum(terms.values()), e_hold)
            count_probabilities = [ex(state, proj, ht+f"count_probability:{i}") for i, proj in enumerate(counts)]
            check(ht+"count_probability_sum", sum(count_probabilities), 1.)
            if not p["g"]:
                check(ht+"copying_off_records_blank", count_probabilities, [1., 0., 0.])
            hold.append(dict(time=duration, count_probabilities=count_probabilities,
                             record_count=count, link_occupation=ex(state, o["n"], ht+"link_mean"),
                             carrier_right=ex(state, o["carrier_right"], ht+"carrier_right"),
                             energy_terms=terms, taylor=td))
        cases.append(dict(name=label, parameters=p, dimension=16,
                          formed_vector=vector_json(formed), formation_duration=1.,
                          formation_taylor=detail, initial_energy=e_initial,
                          formed_energy=e_form, quench_work=work, held_energy=e_hold,
                          actual_record_current_at_switch_before_quench=current,
                          actual_record_retarded_initial_slope_before_quench=record_slope,
                          actual_incidence_retarded_initial_slope_at_switch=incidence_slope,
                          spectrum_and_actual_weights=band_weights,
                          lower_band_weight=sum(row["weight"] for row in band_weights if row["beta"] == -1),
                          eigenbranch_addition_diagnostics=addition,
                          instantaneous_addition_diagnostics=instantaneous, hold=hold))
    failures = [row for row in checks if not row["passed"]]
    payload = dict(scope="New invariant 16D native two-record preparation; all bands retained; no clock EOS or volume claim.",
                   tolerance=TOL, cases=cases, checks=checks)
    result = dict(status="COMPLETE" if not failures else "FAILED", payload=payload,
                  freeze_sha256=digest(freeze_path), payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(),
                  seconds=time.perf_counter()-started,
                  peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    save_new("RECORD_ADDITION_RESULTS.json", result)
    print(json.dumps(dict(status=result["status"], checks=len(checks), failures=failures,
                          seconds=result["seconds"], cases=[dict(name=c["name"],
                          quench_work=c["quench_work"], lower_band_weight=c["lower_band_weight"],
                          record_count=c["hold"][0]["record_count"]) for c in cases]), allow_nan=False))


if __name__ == "__main__":
    if sys.argv[1:] == ["freeze"]:
        save_new("RECORD_ADDITION_FROZEN.json", dict(files={str(path.relative_to(WORKSPACE)): digest(path) for path in SOURCES}))
    elif sys.argv[1:]:
        raise SystemExit("Use freeze or no arguments.")
    else:
        run()
