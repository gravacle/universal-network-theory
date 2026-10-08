"""Small saved-state phase-clock census; explicit freeze then run only."""
import os
import sys
sys.dont_write_bytecode = True
for key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import tempfile
import time
import numpy as np

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent
PREFIX = "native_phase_clock_v001_"
AGES = (0., .25, .5, 1., 2.)
INTERVALS = (512, 1024)
NAMES = ("native", "feedback_off", "copying_off")
TOL = 1e-11
ALLOWANCE = 1e-10
ANCESTORS = (
    ("RECORD_ADDITION_RESULTS.json", "2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a",
     "RECORD_ADDITION_FROZEN.json", "4d22da45549f2de78fc0477be6b5f23bc0f58b3598a312e2aa76d8f729ac9ff3"),
    ("native_writer_pulse_results.json", "ca023664cd9798999198ff3999b918a95613798d30ce1d434a318669697c49ea",
     "native_writer_pulse_frozen.json", "9dde274111747690e7cfab23cd6f184ba6a5db6388a00b59f4d658e393564092"),
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def save_new(name, value):
    with tempfile.NamedTemporaryFile(mode="w", dir=HERE, prefix=name+".partial.", delete=False) as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+"\n")
        handle.flush()
        os.fsync(handle.fileno())
        temporary = Path(handle.name)
    os.link(temporary, HERE/name)
    temporary.unlink()


def inputs():
    sources = [Path(__file__).resolve(), HERE/"NATIVE_PHASE_CLOCK_PROTOCOL_V001.md",
               HERE/"NATIVE_PHASE_CLOCK_CANDIDATE_V001.md", HERE/"NATIVE_SOURCE_BRIDGE_DECISION.md",
               HERE/"NATIVE_WRITER_PULSE_RESULT.md"]
    results = []
    for result_name, result_hash, freeze_name, freeze_hash in ANCESTORS:
        result_path, freeze_path = HERE/result_name, HERE/freeze_name
        if digest(result_path) != result_hash or digest(freeze_path) != freeze_hash:
            raise RuntimeError("Ancestor byte authentication failed")
        result, freeze = json.loads(result_path.read_text()), json.loads(freeze_path.read_text())
        if result["freeze_sha256"] != freeze_hash or result["payload_sha256"] != hashlib.sha256(encoded(result["payload"])).hexdigest():
            raise RuntimeError("Ancestor payload/freeze link failed")
        if result["status"] != "COMPLETE" or not all(c["passed"] for c in result["payload"]["checks"]):
            raise RuntimeError("Ancestor did not qualify")
        if tuple(c["name"] for c in result["payload"]["cases"]) != NAMES:
            raise RuntimeError("Ancestor census differs")
        for relative, expected in freeze["files"].items():
            path = WORKSPACE/relative
            if digest(path) != expected:
                raise RuntimeError("Ancestor source differs: "+relative)
            sources.append(path)
        sources.extend((result_path, freeze_path))
        results.append(result)
    snapshot = dict(files={str(p.relative_to(WORKSPACE)): digest(p) for p in sources},
                    ages=AGES, interval_counts=INTERVALS, preparations=NAMES,
                    tolerance=TOL, continuous_bound_allowance=ALLOWANCE)
    return results, snapshot


def complex_json(value):
    return dict(real=float(value.real), imag=float(value.imag))


def mean(psi, operator):
    return np.vdot(psi, operator @ psi)


def run():
    started = time.perf_counter()
    results, snapshot = inputs()
    freeze_path = HERE/(PREFIX+"frozen.json")
    if encoded(json.loads(freeze_path.read_text())) != encoded(snapshot):
        raise RuntimeError("New source freeze differs")
    spec = importlib.util.spec_from_file_location("owned_native_phase_matrix", HERE/"record_addition_compute.py")
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    identity, o = native.I, native.operators()
    a_op, r = o["AL"]+o["AR"], o["QL"]+o["QR"]
    n_a = o["n"] @ a_op
    checks, cases = [], []

    def check(name, actual, expected=0., tolerance=TOL):
        error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
        checks.append(dict(name=name, residual=error, tolerance=tolerance,
                           passed=bool(math.isfinite(error) and error <= tolerance)))

    count_projectors = [(identity-o["QL"]) @ (identity-o["QR"]),
                        o["QL"] @ (identity-o["QR"])+(identity-o["QL"]) @ o["QR"],
                        o["QL"] @ o["QR"]]
    for saved, pulse in zip(results[0]["payload"]["cases"], results[1]["payload"]["cases"]):
        name, p = saved["name"], saved["parameters"]
        expected = dict(native.PARAMETERS)
        if name == "feedback_off":
            expected["lambda_R"] = 0.
        if name == "copying_off":
            expected["g"] = 0.
        if p != expected or p != pulse["parameters"] or tuple(x["age"] for x in pulse["ages"]) != AGES:
            raise RuntimeError("Unexpected preparation or age census")
        psi = np.array(saved["formed_vector"]["real"])+1j*np.array(saved["formed_vector"]["imag"])
        h, _ = native.hamiltonian(dict(p, g=0.), o)
        adot_op = 1j*native.comm(h, a_op)
        check(name+":norm", mean(psi, identity), 1.)
        check(name+":held_energy", mean(psi, h), saved["held_energy"])
        check(name+":raising_commutator", adot_op, 1j*(p["epsilon_r"]*a_op-p["lambda_R"]*n_a))
        sectors = {}
        for row in saved["spectrum_and_actual_weights"]:
            count, s, beta = row["R"], row["s"], row["beta"]
            x = 2.25-p["lambda_R"]*count-.5*s
            d = math.hypot(x, 2.)
            energy = 3+count+(x+beta*d)/2
            proj = count_projectors[count] @ ((identity-beta*(2*o["Xa"]+x*o["Za"])/d)/2) @ ((identity+s*o["XC"])/2)
            key = (count, s, beta)
            sectors[key] = (energy, proj)
            check(name+f":energy:{key}", energy, row["energy"])
            check(name+f":projector:{key}", proj @ proj, proj)
            check(name+f":rank:{key}", np.trace(proj), (1, 2, 1)[count])
            check(name+f":eigenprojector:{key}", h @ proj, energy*proj)
        check(name+":projector_resolution", sum(pj for _, pj in sectors.values()), identity)
        check(name+":H_reconstruction", sum(e*pj for e, pj in sectors.values()), h)
        for j, (key, (_, pj)) in enumerate(sectors.items()):
            for key2 in list(sectors)[:j]:
                check(name+f":orthogonal:{key}:{key2}", pj @ sectors[key2][1])
        lines, reconstructed_a, reconstructed_na = [], np.zeros_like(h), np.zeros_like(h)
        for count in (0, 1):
            for s in (1, -1):
                for beta in (-1, 1):
                    for gamma in (-1, 1):
                        ei, pi = sectors[(count, s, beta)]
                        ef, pf = sectors[(count+1, s, gamma)]
                        block_a, block_na = pf @ a_op @ pi, pf @ n_a @ pi
                        reconstructed_a += block_a
                        reconstructed_na += block_na
                        lines.append(dict(R=count, s=s, beta=beta, gamma=gamma, omega=ef-ei,
                                          coefficient=complex_json(mean(psi, block_a)),
                                          n_coefficient=complex_json(mean(psi, block_na))))
        check(name+":all_A_blocks", reconstructed_a, a_op)
        check(name+":all_nA_blocks", reconstructed_na, n_a)
        omega = np.array([v["omega"] for v in lines])
        coeff = np.array([complex(v["coefficient"]["real"], v["coefficient"]["imag"]) for v in lines])
        ncoeff = np.array([complex(v["n_coefficient"]["real"], v["n_coefficient"]["imag"]) for v in lines])
        moments = [float(np.sum(np.abs(coeff)*np.abs(omega)**k)) for k in range(3)]

        def signals(times):
            phase = np.exp(1j*np.outer(np.asarray(times), omega))
            return phase @ coeff, phase @ (1j*omega*coeff), phase @ ncoeff

        e, eigenvectors = np.linalg.eigh(h)
        age_rows = []
        for age, old_age in zip(AGES, pulse["ages"]):
            aa, ad, zz = [v[0] for v in signals([age])]
            u_eigh = (eigenvectors*np.exp(-1j*age*e)) @ eigenvectors.conj().T
            u_taylor, detail = native.taylor_propagator(h, age)
            for method, u in (("eigh", u_eigh), ("taylor", u_taylor)):
                state = u @ psi
                check(name+f":{age}:{method}:A", mean(state, a_op), aa)
                check(name+f":{age}:{method}:Adot", mean(state, adot_op), ad)
                check(name+f":{age}:{method}:nA", mean(state, n_a), zz)
            check(name+f":{age}:saved_K", 2*aa.real, old_age["initial_K"])
            check(name+f":{age}:saved_Y", 2*aa.imag, old_age["initial_Ysum"])
            check(name+f":{age}:conditional_rate_identity", ad, 1j*(p["epsilon_r"]*aa-p["lambda_R"]*zz))
            numerator = float((aa.conjugate()*ad).imag)
            age_rows.append(dict(age=age, amplitude=abs(aa), A=complex_json(aa), Adot=complex_json(ad),
                                 nA=complex_json(zz), phase_numerator=numerator,
                                 phase_rate=numerator/abs(aa)**2 if name != "copying_off" and abs(aa)>ALLOWANCE else None,
                                 taylor=detail))
        bounds = []
        for intervals in INTERVALS:
            times = np.linspace(0., 2., intervals+1)
            aa, ad, zz = signals(times)
            amp, numerator = np.abs(aa), np.imag(np.conj(aa)*ad)
            check(name+f":grid{intervals}:Adot_identity", ad, 1j*(p["epsilon_r"]*aa-p["lambda_R"]*zz))
            check(name+f":grid{intervals}:amplitude_identity", 2*np.real(np.conj(aa)*ad),
                  2*p["lambda_R"]*np.imag(np.conj(aa)*zz))
            step = 2/intervals
            lower_a = float(np.min(amp))-moments[1]*step/2-ALLOWANCE
            lower_n = float(np.min(numerator))-moments[0]*moments[2]*step/2-ALLOWANCE
            upper_n = float(np.max(numerator))+moments[0]*moments[2]*step/2+ALLOWANCE
            if name == "copying_off":
                check(name+":blank_R_support", r @ psi)
                check(name+f":grid{intervals}:blank_A", aa)
                orientation = "undefined_exact_blank"
            elif lower_a > 0 and lower_n > 0:
                orientation = "positive_whole_window"
            elif lower_a > 0 and upper_n < 0:
                orientation = "negative_whole_window"
            else:
                orientation = "inconclusive"
            lower_rate = upper_rate = winding_step_bound = None
            lifted = None
            if name != "copying_off" and lower_a > 0:
                max_a = moments[0]+ALLOWANCE
                lower_rate = min(lower_n/lower_a**2, lower_n/max_a**2)
                upper_rate = max(upper_n/lower_a**2, upper_n/max_a**2)
                winding_step_bound = moments[1]*step/lower_a
                if winding_step_bound < math.pi:
                    phase = np.unwrap(np.angle(aa))
                    lifted = [dict(age=age, phase=float(phase[round(age/step)]),
                                   phase_elapsed=float((phase[round(age/step)]-phase[0])/p["epsilon_r"])) for age in AGES]
            if name == "feedback_off":
                initial_a = sum(coeff)
                check(name+f":grid{intervals}:analytic_phase", aa, initial_a*np.exp(1j*times))
                check(name+f":grid{intervals}:unit_rate", numerator, amp**2)
            bounds.append(dict(intervals=intervals, samples=intervals+1, step=step,
                               minimum_sample_amplitude=float(np.min(amp)),
                               minimum_sample_numerator=float(np.min(numerator)), maximum_sample_numerator=float(np.max(numerator)),
                               amplitude_lower_bound=lower_a, numerator_lower_bound=lower_n, numerator_upper_bound=upper_n,
                               phase_rate_lower_bound=lower_rate, phase_rate_upper_bound=upper_rate,
                               orientation=orientation, no_hidden_winding_step_bound=winding_step_bound,
                               inherited_lifted_phases=lifted))
        cases.append(dict(name=name, parameters=p, moments_M0_M1_M2=moments,
                          spectral_lines=lines, ages=age_rows, continuous_bounds=bounds))
    failures = [x for x in checks if not x["passed"]]
    payload = dict(scope="Native saved-state local phase candidate only; no physical clock/metric calibration or new formation.",
                   ages=AGES, interval_counts=INTERVALS, numerical_allowance=ALLOWANCE,
                   tolerance=TOL, checks=checks, cases=cases)
    result = dict(status="COMPLETE" if not failures else "FAILED", payload=payload,
                  payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(), freeze_sha256=digest(freeze_path),
                  seconds=time.perf_counter()-started, peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    save_new(PREFIX+"results.json", result)
    print(json.dumps(dict(status=result["status"], checks=len(checks), failures=failures,
                         seconds=result["seconds"], peak_self_rss_bytes=result["peak_self_rss_bytes"],
                         decisions=[dict(name=c["name"], bounds=c["continuous_bounds"][-1]) for c in cases]), allow_nan=False))


if __name__ == "__main__":
    if sys.argv[1:] == ["freeze"]:
        _, snapshot = inputs()
        save_new(PREFIX+"frozen.json", snapshot)
    elif sys.argv[1:] == ["run"]:
        run()
    else:
        raise SystemExit("Explicit freeze or run required")
