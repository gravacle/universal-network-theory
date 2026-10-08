"""Inert until explicit freeze/run: native saved-state writer-pulse test."""
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
import platform
import resource
import tempfile
import time

import numpy as np

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent
PREFIX = "native_writer_pulse_"
AGES = (0., .25, .5, 1., 2.)
DURATIONS = (.08, .04, .02, .01)
AMPLITUDES = (.01, .005)
NAMES = ("native", "feedback_off", "copying_off")
TOL = 1e-11
RAW_ALLOWANCE = 1e-12
OLD_RESULT = HERE / "RECORD_ADDITION_RESULTS.json"
OLD_FREEZE = HERE / "RECORD_ADDITION_FROZEN.json"
OLD_RESULT_SHA256 = "2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a"
OLD_FREEZE_SHA256 = "4d22da45549f2de78fc0477be6b5f23bc0f58b3598a312e2aa76d8f729ac9ff3"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode()


def save_new(name, value):
    content = json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"
    with tempfile.NamedTemporaryFile(mode="w", dir=HERE, prefix=name+".partial.",
                                     delete=False) as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
        temporary = Path(handle.name)
    os.link(temporary, HERE / name)
    temporary.unlink()


def authenticated_input():
    if digest(OLD_RESULT) != OLD_RESULT_SHA256 or digest(OLD_FREEZE) != OLD_FREEZE_SHA256:
        raise RuntimeError("Authenticated old result/freeze bytes differ; no pulse run")
    freeze = json.loads(OLD_FREEZE.read_text())
    for relative, expected in freeze["files"].items():
        if digest(WORKSPACE / relative) != expected:
            raise RuntimeError("Old source custody mismatch: " + relative)
    result = json.loads(OLD_RESULT.read_text())
    if result["freeze_sha256"] != digest(OLD_FREEZE):
        raise RuntimeError("Old result-to-freeze link mismatch")
    if result["payload_sha256"] != hashlib.sha256(encoded(result["payload"])).hexdigest():
        raise RuntimeError("Old payload digest mismatch")
    if result["status"] != "COMPLETE" or not all(c["passed"] for c in result["payload"]["checks"]):
        raise RuntimeError("Old qualification did not pass")
    if tuple(c["name"] for c in result["payload"]["cases"]) != NAMES:
        raise RuntimeError("Unexpected preparation census")
    return result, freeze


def snapshot():
    _, old = authenticated_input()
    sources = [Path(__file__).resolve(), HERE / "NATIVE_WRITER_PULSE_PROTOCOL.md",
               HERE / "NATIVE_RECORD_PHASE_PATHWAY.md", OLD_RESULT, OLD_FREEZE]
    sources.extend(WORKSPACE / name for name in old["files"])
    files = {str(path.relative_to(WORKSPACE)): digest(path) for path in sources}
    return dict(files=files, ages=AGES, durations=DURATIONS, amplitudes=AMPLITUDES,
                preparations=NAMES, tolerance=TOL, raw_response_allowance=RAW_ALLOWANCE)


def source_module():
    spec = importlib.util.spec_from_file_location("owned_record_addition", HERE / "record_addition_compute.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # Only definitions; its worker is under __main__.
    return module


def comm(a, b):
    return a @ b - b @ a


def mean(v, a):
    return float(np.vdot(v, a @ v).real)


def stable_change(base, changed, observable):
    """Avoid subtracting two order-one expectation values."""
    delta = changed - base
    return float((2*np.vdot(base, observable @ delta) +
                  np.vdot(delta, observable @ delta)).real)


def propagator(e, v, duration):
    return (v * np.exp(-1j * duration * e)) @ v.conj().T


def spectral_tangent(e, v, k, duration):
    """Exact derivative d exp[-i(H+epsilon*K)t]/d epsilon at zero."""
    gap = e[:, None] - e[None, :]
    average = (e[:, None] + e[None, :]) / 2
    kernel = -1j*duration*np.exp(-1j*duration*average)*np.sinc(duration*gap/(2*np.pi))
    return v @ (kernel * (v.conj().T @ k @ v)) @ v.conj().T


def tangent_taylor(h, k, duration):
    """Independent coupled power series for U and its source derivative."""
    a, b = -1j*duration*h, -1j*duration*k
    bound = float(np.linalg.norm(a, np.inf) + np.linalg.norm(b, np.inf))
    identity = np.eye(len(h), dtype=complex)
    term, derivative_term = identity.copy(), np.zeros_like(h, dtype=complex)
    total, derivative = term.copy(), derivative_term.copy()
    magnitude = 1.
    for order in range(1, 201):
        derivative_term = (a @ derivative_term + b @ term) / order
        term = a @ term / order
        total += term
        derivative += derivative_term
        magnitude *= bound / order
        tail = math.exp(bound)*magnitude*bound/(order+1)
        if tail <= 1e-18:
            return total, derivative, dict(order=order, exact_arithmetic_block_tail=tail)
    raise ArithmeticError("Tangent Taylor tail criterion not reached")


def kubo_operator(e, v, k, observable, duration, order):
    """Plus-source derivative i integral [K(s),O(t)] ds, not a stationary approximation."""
    nodes, weights = np.polynomial.legendre.leggauss(order)
    endpoint = propagator(e, v, duration)
    ot = endpoint.conj().T @ observable @ endpoint
    answer = np.zeros_like(k, dtype=complex)
    for node, weight in zip(nodes, weights):
        us = propagator(e, v, duration*(node+1)/2)
        ks = us.conj().T @ k @ us
        answer += 1j*duration*weight/2 * comm(ks, ot)
    return answer


def response_coefficients(h, k, observable, count=8):
    unperturbed = observable.copy()
    derivative = np.zeros_like(observable, dtype=complex)
    coefficients = []
    for order in range(1, count+1):
        derivative = comm(h, derivative) + comm(k, unperturbed)
        unperturbed = comm(h, unperturbed)
        coefficients.append((1j**order)/math.factorial(order)*derivative)
    return coefficients


def run():
    started = time.perf_counter()
    frozen_path = HERE / (PREFIX + "frozen.json")
    frozen = json.loads(frozen_path.read_text())
    if encoded(frozen) != encoded(snapshot()):
        raise RuntimeError("New source/input freeze mismatch; no pulse run")
    old, _ = authenticated_input()
    native = source_module()
    identity = native.I
    o = native.operators()
    k, r = o["XL"] + o["XR"], o["QL"] + o["QR"]
    observables = {"K": k, "R": r}
    k_norm = float(np.linalg.norm(k, 2))
    checks, cases = [], []

    def check(name, actual, expected=0., tolerance=TOL):
        residual = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
        checks.append(dict(name=name, residual=residual, tolerance=tolerance,
                           passed=bool(math.isfinite(residual) and residual <= tolerance)))

    def truth(name, condition):
        check(name, 0. if condition else 1., tolerance=0.)

    for saved in old["payload"]["cases"]:
        name, p = saved["name"], saved["parameters"]
        expected = dict(native.PARAMETERS)
        if name == "feedback_off":
            expected["lambda_R"] = 0.
        if name == "copying_off":
            expected["g"] = 0.
        if p != expected or tuple(row["time"] for row in saved["hold"]) != AGES:
            raise RuntimeError("Preparation coefficients or age census changed")
        psi = np.array(saved["formed_vector"]["real"]) + 1j*np.array(saved["formed_vector"]["imag"])
        h, _ = native.hamiltonian(dict(p, g=0.), o)
        e, v = np.linalg.eigh(h)
        width = float(e[-1]-e[0])
        check(name+":input_norm", np.vdot(psi, psi), 1.)
        check(name+":held_energy", mean(psi, h), saved["held_energy"])
        dc = comm(k, comm(h, k))
        dc_formula = 4*(identity-p["lambda_R"]*o["n"]) @ (identity-r)
        check(name+":double_commutator", dc, dc_formula)
        check(name+":record_first_response", 1j*comm(k, r), o["YL"]+o["YR"])
        check(name+":held_record_null", comm(h, r))
        coefficients = {key: response_coefficients(h, k, obs) for key, obs in observables.items()}
        check(name+":K_first_coefficient", coefficients["K"][0])
        check(name+":K_second_coefficient", coefficients["K"][1], -dc/2)
        check(name+":R_first_coefficient", coefficients["R"][0], o["YL"]+o["YR"])
        cache = {}
        for duration in DURATIONS:
            u0 = propagator(e, v, duration)
            du = spectral_tangent(e, v, k, duration)
            ut, dut, detail = tangent_taylor(h, k, duration)
            stem = name+f":tau{duration}"
            check(stem+":U_taylor", u0, ut, RAW_ALLOWANCE)
            check(stem+":tangent_taylor", du, dut, RAW_ALLOWANCE)
            check(stem+":tangent_unitarity", du.conj().T @ u0+u0.conj().T @ du)
            response = {}
            tails = {}
            for key, obs in observables.items():
                exact = du.conj().T @ obs @ u0 + u0.conj().T @ obs @ du
                q8 = kubo_operator(e, v, k, obs, duration, 8)
                q16 = kubo_operator(e, v, k, obs, duration, 16)
                check(stem+":"+key+":Kubo8", q8, exact)
                check(stem+":"+key+":Kubo16", q16, exact)
                check(stem+":"+key+":Kubo_orders", q8, q16)
                check(stem+":"+key+":Hermitian_response", exact, exact.conj().T)
                series = sum(c*duration**(index+1) for index, c in enumerate(coefficients[key]))
                tail = (2*k_norm*np.linalg.norm(obs, 2)*duration*math.exp(width*duration)
                        *(width*duration)**8/math.factorial(8))
                check(stem+":"+key+":series8", exact, series, float(tail)+TOL)
                response[key], tails[key] = exact, float(tail)
            pulses = {}
            for amplitude in AMPLITUDES:
                for sign in (-1, 1):
                    epsilon = sign*amplitude
                    hp = h+epsilon*k
                    ep, vp = np.linalg.eigh(hp)
                    up = propagator(ep, vp, duration)
                    upt, _ = native.taylor_propagator(hp, duration)
                    check(stem+f":pulse{epsilon}:Taylor", up, upt, RAW_ALLOWANCE)
                    check(stem+f":pulse{epsilon}:unitary", up.conj().T @ up, identity)
                    pulses[epsilon] = up
            cache[duration] = dict(u0=u0, response=response, tail=tails, pulses=pulses, taylor=detail)
        ages = []
        for saved_age in saved["hold"]:
            age = saved_age["time"]
            uh = propagator(e, v, age)
            uht, _ = native.taylor_propagator(h, age)
            stem = name+f":age{age}"
            check(stem+":hold_taylor", uh, uht)
            state = uh @ psi
            check(stem+":saved_count", mean(state, r), saved_age["record_count"])
            check(stem+":saved_link", mean(state, o["n"]), saved_age["link_occupation"])
            slope = mean(state, dc)
            saved_slope = 4*(1-saved_age["record_count"]-p["lambda_R"]*saved_age["link_occupation"]
                             -saved_age["energy_terms"]["record_incidence_feedback"])
            check(stem+":saved_slope_formula", slope, saved_slope)
            truth(stem+":known_slope_sign", slope > 0 if name == "copying_off" else slope < 0)
            actual_coefficients = {key: [mean(state, c) for c in values]
                                   for key, values in coefficients.items()}
            pulse_rows, response_rows = [], []
            for duration in DURATIONS:
                data = cache[duration]
                baseline = data["u0"] @ state
                changes = {}
                for epsilon, up in data["pulses"].items():
                    end = up @ state
                    tag = stem+f":tau{duration}:epsilon{epsilon}"
                    delta = {key: stable_change(baseline, end, obs) for key, obs in observables.items()}
                    work_on = epsilon*mean(state, k)
                    work_off = -epsilon*mean(end, k)
                    energy_change = stable_change(baseline, end, h)
                    check(tag+":pulse_energy", mean(end, h+epsilon*k), mean(state, h+epsilon*k))
                    check(tag+":full_switch_work", energy_change, work_on+work_off)
                    check(tag+":state_norm", np.vdot(end, end), 1.)
                    changes[epsilon] = delta
                    pulse_rows.append(dict(duration=duration, epsilon=epsilon, change=delta,
                                           work_on=work_on, work_off=work_off,
                                           net_work=work_on+work_off, held_energy_change=energy_change))
                for key, obs in observables.items():
                    exact = mean(state, data["response"][key])
                    norm_o = float(np.linalg.norm(obs, 2))
                    central = []
                    for amplitude in AMPLITUDES:
                        raw = (changes[amplitude][key]-changes[-amplitude][key])/2
                        value = raw/amplitude
                        bound = norm_o*(2*k_norm*duration)**3*amplitude**2/6
                        check(stem+f":tau{duration}:{key}:central{amplitude}",
                              raw, amplitude*exact, amplitude*bound+RAW_ALLOWANCE)
                        central.append(dict(amplitude=amplitude, derivative=value,
                                            error=value-exact, analytic_error_bound=bound,
                                            derivative_roundoff_allowance=RAW_ALLOWANCE/amplitude))
                    richardson = (4*central[1]["derivative"]-central[0]["derivative"])/3
                    rich_bound = norm_o*(2*k_norm*duration)**5*AMPLITUDES[0]**4/288
                    rich_round = (4*RAW_ALLOWANCE/AMPLITUDES[1]+RAW_ALLOWANCE/AMPLITUDES[0])/3
                    check(stem+f":tau{duration}:{key}:amplitude_Richardson", richardson, exact,
                          rich_bound+rich_round)
                    power = 2 if key == "K" else 1
                    lead = actual_coefficients[key][power-1]
                    normalized = exact/duration**power
                    lead_bound = sum(abs(c)*duration**(index+1-power)
                                     for index, c in enumerate(actual_coefficients[key]) if index+1 > power)
                    lead_bound += data["tail"][key]/duration**power
                    check(stem+f":tau{duration}:{key}:leading_with_remainder", normalized, lead,
                          lead_bound+TOL/duration**power)
                    if key == "K" and duration == DURATIONS[-1]:
                        # The inherited state fixes a nonzero sign; no sign is selected from new output.
                        truth(stem+":short_pulse_K_sign", central[1]["derivative"]*lead > 0)
                        truth(stem+":short_pulse_K_resolved",
                              abs(AMPLITUDES[1]*central[1]["derivative"]) > 10*RAW_ALLOWANCE)
                        truth(stem+":positive_pulse_K_sign", changes[AMPLITUDES[1]]["K"]*lead > 0)
                        truth(stem+":positive_pulse_K_resolved",
                              abs(changes[AMPLITUDES[1]]["K"]) > 10*RAW_ALLOWANCE)
                    if name == "copying_off" and key == "R":
                        check(stem+f":tau{duration}:blank_R_linear_null", exact)
                    response_rows.append(dict(duration=duration, observable=key, exact_linear_response=exact,
                                              central=central, amplitude_Richardson=richardson,
                                              amplitude_Richardson_error=richardson-exact,
                                              leading_power=power, leading_coefficient=lead,
                                              normalized_linear_response=normalized,
                                              normalized_leading_error=normalized-lead,
                                              normalized_remainder_bound=lead_bound))
            convergence = {}
            for key in observables:
                rows = [row for row in response_rows if row["observable"] == key]
                errors = [row["normalized_leading_error"] for row in rows]
                convergence[key] = [dict(coarse_duration=DURATIONS[i], fine_duration=DURATIONS[i+1],
                                         ratio=errors[i]/errors[i+1] if abs(errors[i+1]) > 1e-9 else None)
                                    for i in range(len(DURATIONS)-1)]
            ages.append(dict(age=age, initial_K=mean(state, k), record_count=mean(state, r),
                             initial_Ysum=mean(state, o["YL"]+o["YR"]), copy_kernel_initial_slope=slope,
                             response_series_coefficients=actual_coefficients, responses=response_rows,
                             duration_convergence_diagnostic=convergence, pulses=pulse_rows))
        cases.append(dict(name=name, parameters=p, ages=ages))
    failures = [row for row in checks if not row["passed"]]
    payload = dict(scope="Same native 16D saved preparations; full nonstationary writer response and switching work; no clock EOS/volume claim.",
                   ages=AGES, durations=DURATIONS, amplitudes=AMPLITUDES, cases=cases, checks=checks,
                   environment=dict(python=sys.version, numpy=np.__version__, platform=platform.platform()))
    result = dict(status="COMPLETE" if not failures else "FAILED", payload=payload,
                  payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(),
                  freeze_sha256=digest(frozen_path), seconds=time.perf_counter()-started,
                  peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    save_new(PREFIX+"results.json", result)
    print(json.dumps(dict(status=result["status"], checks=len(checks), failures=failures,
                          seconds=result["seconds"], pulse_count=sum(len(a["pulses"]) for c in cases for a in c["ages"])) ))


if __name__ == "__main__":
    if sys.argv[1:] == ["freeze"]:
        save_new(PREFIX+"frozen.json", snapshot())
    elif sys.argv[1:] == ["run"]:
        run()
    else:
        raise SystemExit("Explicit freeze or run required; importing this file does not propagate.")
