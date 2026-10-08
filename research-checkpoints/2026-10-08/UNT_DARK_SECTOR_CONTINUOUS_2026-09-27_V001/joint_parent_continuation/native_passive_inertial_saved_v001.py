"""Saved-state audit of a declared one-link energy-dipole/ruler source chart.

No propagation, state regeneration, producer import, spectral solve, or source
operation is performed. The 15 scalar rows describe ORIGINAL PRE-SWAP held
states, not the localized states proposed by their parent readout. Only the
three actually saved formed vectors supply new matrix expectations.

P is carrier-right, X=ell*(P-I/2), gamma=ell/(2*c**2), and the published local
allocation gives Z=gamma*((eps_psi+j*n)*(2*P-I)+(eps_r-lambda_R*n)*(qR-qL)).
For held copying-off H, D=[P,[H,P]]=t*n*Xc and
  [P,[H,Z]]=2*gamma*(eps_psi+j)*D.
Thus S_XZ=(eps_psi+j)*S_XX/c**2, S_AB=<[A,[H,B]]>/hbar**2.
This allocation is an adopted source chart, not a unique native stress tensor.
Neither a signed contact nor this identity establishes mass, equivalence,
passivity, a force law, metric distance, or physical gravitational coupling.

CRUCIAL: the clock here is exchange-even GLOBAL A=A_L+A_R. Equal unperturbed
endpoint rates do not make perturbed endpoint clocks equivalent. For symmetric
states, Q=(1-n)*(2*P-I), m=(eps_psi+j)/c**2, ell=c=hbar=1,
  chi_rel_XZ-m*chi_rel_XX = -gamma*j*chi_rel_PQ,
where chi_OB(s)=i*<[O(s),B]>/hbar is response to a MINUS source impulse,
and chi_rel_OB=chi_OB-Odot(s)/nu(s)*Im(chi_AB/A(s)). The first two defect
coefficients vanish; its theta**2 coefficient is
 -gamma*j*h/(2*nu**2)*(t*<Ya*Xc>
   -lambda_R*Pdot/nu*Re(<Xa*A*(2*P-I)>/<A>)).
Ya is STANDARD Pauli Y, opposite the ancestral native copy-current sign.
An ONSET SOURCE STEP is distinct: its fixed-clock initial acceleration is
S_XB/nu**2 for -f*B, and -S_XZ/nu**2 for the adopted +a*Z chart. Here the
global-clock response to these sources has no delay**0 or delay**1 term.

All dimensionless outputs set ell=c=hbar=1, not an SI calibration. The parent
1e-10 allowance checks arithmetic only, not certified roundoff intervals or
outcome-selected zero/passivity criteria. Undefined clocks retain protocol-
time responses. No source controller/readout work or apparatus is supplied.
"""
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
import tempfile
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUTPUT = HERE / "native_passive_inertial_saved_v001_results.json"
TOL, GAMMA, HBAR = 1e-10, .5, 1.
NAMES, AGES = ("native", "feedback_off", "copying_off"), (0., .25, .5, 1., 2.)
PINS = {
    "RECORD_ADDITION_RESULTS.json": "2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a",
    "native_intrinsic_transport_clock_saved_v001_results.json": "0eeccca739e01ca89384cd35c30a9823fe6870d009337169e9801cc962609811",
}
PARAMETERS = dict(h=1., Delta=4., U_d=1., d_star=1., epsilon_psi=1.,
                  epsilon_r=1., epsilon_w=0., t_hop=.5, lambda_R=.5,
                  lambda_J=.25, g=1.)
I2, I = np.eye(2), np.eye(16, dtype=complex)
N2, X2 = np.diag([0., 1.]), np.array([[0., 1.], [1., 0.]])
Y2, A2 = np.array([[0., -1j], [1j, 0.]]), np.array([[0., 0.], [1., 0.]])


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cj(z):
    return dict(real=float(z.real), imag=float(z.imag))


def z(saved):
    return complex(saved["real"], saved["imag"])


def comm(a, b):
    return a @ b - b @ a


def embed(a, position):
    out = np.ones((1, 1), complex)
    for k in range(4):
        out = np.kron(out, a if k == position else I2)
    return out


def terms_tensor(p):
    n, r = embed(N2, 2), embed(N2, 0)+embed(N2, 1)
    return dict(incidence_flip=-p["h"]*embed(X2, 2), incidence_bias=p["Delta"]*n,
        both_endpoint_degree_penalties=2*p["U_d"]*(n-p["d_star"]*I) @ (n-p["d_star"]*I),
        carrier_occupation=p["epsilon_psi"]*I, both_record_storage=p["epsilon_r"]*r,
        both_writer_storage=2*p["epsilon_w"]*I,
        carrier_hopping=-p["t_hop"]*n @ embed(X2, 3),
        record_incidence_feedback=-p["lambda_R"]*n @ r,
        current_squared_feedback=p["lambda_J"]*n @ embed(Y2, 3) @ embed(Y2, 3),
        copy_left=p["g"]*embed(X2, 0), copy_right=p["g"]*embed(X2, 1))


def entries(p):
    """Independent basis-entry construction, order (rL,rR,link,carrier)."""
    h = np.zeros((16, 16), complex)
    diag_z, diag_q, swap = np.zeros(16), np.zeros(16), np.zeros((16, 16))
    for b in range(16):
        left, right, n, carrier = (b >> k & 1 for k in (3, 2, 1, 0))
        h[b, b] = (p["Delta"]*n+2*p["U_d"]*(n-p["d_star"])**2
            +p["epsilon_psi"]+p["epsilon_r"]*(left+right)+2*p["epsilon_w"]
            -p["lambda_R"]*n*(left+right)+p["lambda_J"]*n)
        h[b ^ 2, b] = -p["h"]
        h[b ^ 1, b] = -p["t_hop"]*n
        h[b ^ 8, b], h[b ^ 4, b] = p["g"], p["g"]
        diag_z[b] = GAMMA*((p["epsilon_psi"]+p["lambda_J"]*n)*(2*carrier-1)
            +(p["epsilon_r"]-p["lambda_R"]*n)*(right-left))
        diag_q[b] = (1-n)*(2*carrier-1)
        swap[(right << 3)+(left << 2)+(n << 1)+carrier, b] = 1.
    return h, np.diag(diag_z), np.diag(diag_q), swap


def derivatives(h, observable, count=3):
    out = [observable]
    for _ in range(1, count):
        out.append(1j*comm(h, out[-1])/HBAR)
    return out


def response_operators(h, observable, source):
    return [1j*comm(d, source)/(HBAR*math.factorial(k))
            for k, d in enumerate(derivatives(h, observable))]


def sign(value):
    return "positive" if value > 0 else "negative" if value < 0 else "zero"


def run():
    started = time.perf_counter()
    if OUTPUT.exists() or OUTPUT.is_symlink():
        raise FileExistsError(str(OUTPUT))
    identities = {}
    for name, expected in PINS.items():
        path = HERE/name
        if path.is_symlink() or digest(path) != expected:
            raise RuntimeError("Pinned input differs: "+name)
        identities[str(path.relative_to(ROOT))] = expected
    old, saved = [json.loads((HERE/name).read_text()) for name in PINS]
    for obj, status in ((old, "COMPLETE"), (saved, "COMPLETE_SAVED_ARITHMETIC")):
        if (obj["status"] != status or hashlib.sha256(encoded(obj["payload"])).hexdigest()
                != obj["payload_sha256"] or not all(c["passed"] for c in obj["payload"]["checks"])):
            raise RuntimeError("Parent status, payload, or checks differ")
    identities.update(saved["payload"]["input_and_source_sha256"])
    identities[str(Path(__file__).relative_to(ROOT))] = digest(Path(__file__))
    for relative, expected in identities.items():
        path = ROOT/relative
        if path.is_symlink() or not path.resolve(strict=True).is_relative_to(ROOT) or digest(path) != expected:
            raise RuntimeError("Parent-bound source differs: "+relative)
    frozen_name = str((HERE/"RECORD_ADDITION_FROZEN.json").relative_to(ROOT))
    if old["freeze_sha256"] != identities[frozen_name]:
        raise RuntimeError("Original freeze binding differs")
    if (tuple(saved["payload"]["ages"]) != AGES or saved["payload"]["numerical_allowance"] != TOL
            or tuple(c["name"] for c in saved["payload"]["cases"]) != NAMES
            or tuple(c["name"] for c in old["payload"]["cases"]) != NAMES):
        raise RuntimeError("Changed census or arithmetic allowance")
    checks, scalar_cases, vector_rows = [], [], []

    def check(name, a, b=0.):
        error = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
        checks.append(dict(name=name, residual=error if math.isfinite(error) else None,
            assigned_allowance=TOL, passed=math.isfinite(error) and error <= TOL))

    n, P, A = embed(N2, 2), embed(N2, 3), embed(A2, 0)+embed(A2, 1)
    C, X, Xa, Ya, Xc = 2*P-I, P-I/2, embed(X2, 2), embed(Y2, 2), embed(X2, 3)
    delta_r = embed(N2, 1)-embed(N2, 0)
    for original, case in zip(old["payload"]["cases"], saved["payload"]["cases"]):
        name, p = case["name"], case["parameters"]
        expected = dict(PARAMETERS, **({"lambda_R": 0.} if name == "feedback_off" else
                                     {"g": 0.} if name == "copying_off" else {}))
        if (p != expected or original["parameters"] != expected or original["dimension"] != 16
                or original["formation_duration"] != 1. or case["held_copying_g"] != 0.
                or tuple(r["age"] for r in case["rows"]) != AGES
                or tuple(r["time"] for r in original["hold"]) != AGES):
            raise RuntimeError("Changed preparation: "+name)
        rows = []
        for row, held in zip(case["rows"], original["hold"]):
            tag = name+":"+str(row["age"])+":"
            terms, nu = row["initial_energy_terms"], row["nu"]
            for term, value in terms.items():
                check(tag+"saved_energy:"+term, value, held["energy_terms"][term])
            check(tag+"full_energy", math.fsum(terms.values()), original["held_energy"])
            a, adot, na = z(row["global_A"]), z(row["global_Adot"]), z(row["global_nA"])
            check(tag+"clock_equation", adot, 1j*(p["epsilon_r"]*a-p["lambda_R"]*na))
            if nu is not None:
                check(tag+"actual_phase_rate", nu, (a.conjugate()*adot).imag/abs(a)**2)
            else:
                check(tag+"undefined_clock_only_copyoff", int(name == "copying_off"), 1)
                check(tag+"blank_clock", a)
            sxx = -terms["carrier_hopping"]/HBAR**2
            sxz = (p["epsilon_psi"]+p["lambda_J"])*sxx
            rows.append(dict(age=row["age"], SXX_over_ell_squared=sxx, SXZ=sxz,
                contact_sign=sign(sxx), global_clock_nu=nu,
                minus_X_step_fixed_clock_acceleration=None if nu is None else sxx/nu**2,
                minus_Z_step_fixed_clock_acceleration=None if nu is None else sxz/nu**2,
                plus_Z_step_fixed_clock_acceleration=None if nu is None else -sxz/nu**2,
                plus_Z_step_theta_squared_coefficient=None if nu is None else -sxz/(2*nu**2),
                initial_full_bulk_energy=math.fsum(terms.values()), initial_energy_terms=terms))
        changes = [dict(from_age=a["age"], to_age=b["age"], from_sign=a["contact_sign"],
            to_sign=b["contact_sign"]) for a, b in zip(rows, rows[1:]) if a["contact_sign"] != b["contact_sign"]]
        scalar_cases.append(dict(name=name, parameters=p, rows=rows, adjacent_saved_contact_sign_changes=changes))

        hp = dict(p, g=0.)
        terms = terms_tensor(hp)
        H = sum(terms.values())
        Hb, Zb, Qb, W = entries(hp)
        Z = GAMMA*((p["epsilon_psi"]*I+p["lambda_J"]*n) @ C
                  +(p["epsilon_r"]*I-p["lambda_R"]*n) @ delta_r)
        Q, D, energy_ratio = (I-n) @ C, p["t_hop"]*n @ Xc, p["epsilon_psi"]+p["lambda_J"]
        tag = name+":formed:"
        check(tag+"independent_full_H", H, Hb)
        check(tag+"independent_Z", Z, Zb)
        check(tag+"independent_Q", Q, Qb)
        check(tag+"H_hermitian", H, H.conj().T)
        check(tag+"record_swap_H", comm(H, W))
        check(tag+"record_swap_A", comm(A, W))
        check(tag+"contact_identity", comm(P, comm(H, P)), D)
        check(tag+"mixed_identity", comm(P, comm(H, Z)), 2*GAMMA*energy_ratio*D)
        # Explicit published endpoint allocation retains every held term.
        common = sum(terms[k] for k in ("incidence_flip", "incidence_bias",
            "both_endpoint_degree_penalties", "both_writer_storage", "carrier_hopping"))/2
        local = [common+(p["epsilon_psi"]*I+p["lambda_J"]*n) @ pv
            +(p["epsilon_r"]*I-p["lambda_R"]*n) @ qv
            for pv, qv in ((I-P, embed(N2, 0)), (P, embed(N2, 1)))]
        check(tag+"local_energy_sum", sum(local), H)
        check(tag+"local_energy_dipole", GAMMA*(local[1]-local[0]), Z)
        v = np.array(original["formed_vector"]["real"])+1j*np.array(original["formed_vector"]["imag"])
        if v.shape != (16,):
            raise RuntimeError("Unexpected saved vector shape")
        ex = lambda op: np.vdot(v, op @ v)
        check(tag+"norm", np.vdot(v, v), 1.)
        check(tag+"record_swap_state", W @ v, v)
        for term, op in terms.items():
            check(tag+"energy:"+term, ex(op), original["hold"][0]["energy_terms"][term])
        check(tag+"held_energy", ex(H), original["held_energy"])
        check(tag+"formed_energy", ex(sum(terms_tensor(p).values())), original["formed_energy"])
        check(tag+"quench_work", original["held_energy"]-original["formed_energy"], original["quench_work"])
        clock = case["rows"][0]
        a, na, adot = ex(A), ex(n @ A), ex(1j*comm(H, A))
        for label, actual in (("A", a), ("nA", na), ("Adot", adot)):
            check(tag+"saved_global_"+label, actual, z(clock["global_"+label]))
        nu = None if name == "copying_off" else (a.conjugate()*adot).imag/abs(a)**2
        if nu is not None:
            check(tag+"saved_nu", nu, clock["nu"])
        pdot = float(ex(1j*comm(H, P)).real)
        kernels, kernel_ops = {}, {}
        for label, observable, source in (("PQ", P, Q), ("AQ", A, Q),
                ("XZ", X, Z), ("XX", X, X), ("AZ", A, Z), ("AX", A, X)):
            ops = response_operators(H, observable, source)
            independent = response_operators(Hb, observable, {"PQ": Qb, "AQ": Qb,
                "XZ": Zb, "AZ": Zb}.get(label, X))
            kernel_ops[label], kernels[label] = ops, [ex(op) for op in ops]
            for k in range(3):
                check(tag+label+":independent_order"+str(k), ops[k], independent[k])
        for label in ("PQ", "AQ"):
            for k in (0, 1):
                check(tag+label+":zero_order"+str(k), kernel_ops[label][k])
        check(tag+"PQ_second_operator", kernel_ops["PQ"][2], p["h"]*p["t_hop"]*Ya @ Xc/2)
        check(tag+"AQ_second_operator", kernel_ops["AQ"][2], 1j*p["h"]*p["lambda_R"]*Xa @ A @ C/2)
        even = (I+W)/2
        for k in range(3):
            check(tag+"symmetric_direct_P_defect_order"+str(k),
                even @ (kernel_ops["XZ"][k]-energy_ratio*kernel_ops["XX"][k]
                        +GAMMA*p["lambda_J"]*kernel_ops["PQ"][k]) @ even)
            check(tag+"symmetric_direct_clock_defect_order"+str(k),
                even @ (kernel_ops["AZ"][k]-energy_ratio*kernel_ops["AX"][k]
                        +GAMMA*p["lambda_J"]*kernel_ops["AQ"][k]) @ even)
            for label in ("PQ", "XZ", "XX"):
                check(tag+label+":real_order"+str(k), kernels[label][k].imag)
        for label in ("AZ", "AX"):
            for k in (0, 1):
                check(tag+"global_clock_onset_"+label+str(k), kernels[label][k])
        protocol = [float((kernels["XZ"][k]-energy_ratio*kernels["XX"][k]).real) for k in range(3)]
        check(tag+"defect_initial_zero", protocol[0])
        check(tag+"defect_first_slope_zero", protocol[1])
        rel, reduced, theta2, predicted = None, None, None, None
        if nu is not None:
            # Clock kernels start at order 2: A(s), Pdot(s)/nu(s) need only
            # their initial values at this order. Vanishing lower defect
            # orders likewise make theta**2 = nu**2*s**2 sufficient.
            rel = [protocol[k]-pdot/nu*((kernels["AZ"][k]-energy_ratio*kernels["AX"][k])/a).imag for k in range(3)]
            reduced = [-GAMMA*p["lambda_J"]*(kernels["PQ"][k].real
                -pdot/nu*(kernels["AQ"][k]/a).imag) for k in range(3)]
            check(tag+"direct_relational_defect", rel, reduced)
            theta2 = rel[2]/nu**2
            predicted = -GAMMA*p["lambda_J"]*p["h"]/(2*nu**2)*(p["t_hop"]*ex(Ya @ Xc).real
                -p["lambda_R"]*pdot/nu*(ex(Xa @ A @ C)/a).real)
            check(tag+"theta_squared_formula", theta2, predicted)
        vector_rows.append(dict(name=name, age=0., global_clock_nu=nu, Pdot=pdot,
            A=cj(a), nA=cj(na), Ya_Xc=cj(ex(Ya @ Xc)), Xa_A_C=cj(ex(Xa @ A @ C)),
            protocol_kernel_power_coefficients={key: [cj(value) for value in values] for key, values in kernels.items()},
            protocol_direct_defect_power_coefficients=protocol,
            global_clock_relational_defect_protocol_power_coefficients=rel,
            independently_reduced_relational_defect_coefficients=reduced,
            relational_defect_theta_squared=theta2, predicted_theta_squared=predicted,
            protocol_contribution_to_theta_squared=None if nu is None else protocol[2]/nu**2,
            clock_contribution_to_theta_squared=None if nu is None else (rel[2]-protocol[2])/nu**2,
            protocol_second_coefficient_sign=sign(protocol[2]),
            relational_second_coefficient_sign=None if theta2 is None else sign(theta2)))

    differences = []
    for left in range(3):
        for right in range(left+1, 3):
            for a, b in zip(scalar_cases[left]["rows"], scalar_cases[right]["rows"]):
                differences.append(dict(left=NAMES[left], right=NAMES[right], age=a["age"],
                    SXX_left_minus_right=a["SXX_over_ell_squared"]-b["SXX_over_ell_squared"],
                    minus_X_step_clock_acceleration_left_minus_right=None
                    if a["global_clock_nu"] is None or b["global_clock_nu"] is None else
                    a["minus_X_step_fixed_clock_acceleration"]-b["minus_X_step_fixed_clock_acceleration"]))
    for relative, expected in identities.items():
        if digest(ROOT/relative) != expected:
            raise RuntimeError("Input/source changed during arithmetic: "+relative)
    failures = [item for item in checks if not item["passed"]]
    payload = dict(scope="Follow-on exploratory saved-state arithmetic in a declared source/ruler chart; no new evolution or physical source operation.",
        units=dict(ell=1., c=1., hbar=1., gamma=GAMMA), global_exchange_even_clock_only=True,
        endpoint_perturbed_clocks_equivalent=False, physical_mass_or_gravity_identified=False,
        source_or_pointer_apparatus_supplied=False, roundoff_certified=False,
        source_step_vs_impulse_distinguished=True, no_new_evolution=True,
        original_pre_swap_states=True, aged_vectors_regenerated=False,
        assigned_arithmetic_allowance=TOL, checks=checks, scalar_cases=scalar_cases,
        formed_vector_rows=vector_rows, cross_case_saved_differences=differences,
        input_and_source_sha256=identities)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = dict(status="COMPLETE_SAVED_ARITHMETIC" if not failures else "FAILED_SAVED_ARITHMETIC",
        payload=payload, payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(), failures=failures,
        seconds=time.perf_counter()-started, peak_self_rss_bytes=peak if sys.platform == "darwin" else peak*1024)
    content = (json.dumps(result, sort_keys=True, indent=2, allow_nan=False)+"\n").encode()
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=HERE, prefix=OUTPUT.name+".partial.", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, OUTPUT)
    finally:
        if temporary is not None:
            temporary.unlink()
    print(json.dumps(dict(status=result["status"], path=str(OUTPUT), sha256=digest(OUTPUT),
        bytes=len(content), checks=len(checks), failures=failures, scalar_rows=15, formed_vectors=3,
        source_sha256=digest(Path(__file__)), input_result_sha256=PINS,
        scalar_cases=[dict(name=c["name"], adjacent_saved_contact_sign_changes=c["adjacent_saved_contact_sign_changes"],
            rows=[{key: value for key, value in row.items() if key != "initial_energy_terms"}
                  for row in c["rows"]]) for c in scalar_cases],
        formed_vector_rows=[{key: value for key, value in row.items()
            if key != "protocol_kernel_power_coefficients"} for row in vector_rows],
        cross_case_saved_differences=differences,
        seconds=result["seconds"], peak_self_rss_bytes=result["peak_self_rss_bytes"]),
        sort_keys=True, allow_nan=False))
    return 2 if failures else 0


if __name__ == "__main__":
    raise SystemExit(run())
