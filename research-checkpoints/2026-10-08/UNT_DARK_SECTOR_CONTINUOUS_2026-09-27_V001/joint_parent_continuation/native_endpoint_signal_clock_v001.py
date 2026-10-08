"""Prospective same-state 16D endpoint probe; explicit --run, stdout JSON only.

No photon, arrival-time, physical metric, redshift, or expansion is inferred.
Reuses saved writer-formed states; it does NOT run formation or old audits.
Kick: U_alpha=exp(-i alpha p_L), alpha dimensionless, integrated action=hbar*alpha.
All tolerances below are numerical implementation checks, not scientific gates.
"""
import os
import sys

sys.dont_write_bytecode = True
for thread_variable in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
                        "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[thread_variable] = "1"

import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import time

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
NAMES = ("native", "feedback_off", "copying_off")
AGES = (0., .25, .5, 1.)
DELAYS = (1/32, 1/16, 1/8, .25, .5, 1.)
ANGLES = (2**-8, 2**-9, 2**-10)
HBAR = 1.
# Retain the inherited 16D matrix/observable allowance. Centered divisions have
# explicit 1/sin(alpha) amplification; analytic finite-angle identities eliminate
# Taylor truncation from those checks. This is not directed-rounding arithmetic.
TOL = 1e-11
PINS = {
    "record_addition_compute.py": "4df3bbc8b38ad6b602841b7b28a7a59d37e69d60286f7a2ef11c37ddc150ce10",
    "RECORD_ADDITION_RESULTS.json": "2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a",
    "RECORD_ADDITION_FROZEN.json": "4d22da45549f2de78fc0477be6b5f23bc0f58b3598a312e2aa76d8f729ac9ff3",
    "native_phase_clock_v001_results.json": "5992e6daf072b3873670d22c280f4f1592e95a0f250eb703d919d6d548f21206",
    "native_phase_clock_v001_frozen.json": "e01ceac78343ea49d29cebc8b555d77509427d172439339380e6e80c4a4eb70f",
}


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cj(value):
    return {"real": float(value.real), "imag": float(value.imag)}


def ex(state, op):
    return np.vdot(state, op @ state)


def comm(a, b):
    return a @ b - b @ a


def inputs():
    """Read/check saved inputs and source bytes before importing operator helpers."""
    if ROOT != Path("/Users/bgm/Documents/ChatGPT/Universal Network Theory"):
        raise RuntimeError("Wrong project root")
    identities = {}
    for name, expected in PINS.items():
        path = HERE/name
        actual = digest(path)
        if actual != expected:
            raise RuntimeError("Pinned input differs: " + name)
        identities[str(path.relative_to(ROOT))] = actual
    accepted = []
    for result_name, freeze_name in (
        ("RECORD_ADDITION_RESULTS.json", "RECORD_ADDITION_FROZEN.json"),
        ("native_phase_clock_v001_results.json", "native_phase_clock_v001_frozen.json"),
    ):
        result = json.loads((HERE/result_name).read_text())
        freeze = json.loads((HERE/freeze_name).read_text())
        if result["freeze_sha256"] != PINS[freeze_name]:
            raise RuntimeError("Parent freeze binding differs")
        if result["payload_sha256"] != hashlib.sha256(encode(result["payload"])).hexdigest():
            raise RuntimeError("Parent payload binding differs")
        if result["status"] != "COMPLETE" or not all(c["passed"] for c in result["payload"]["checks"]):
            raise RuntimeError("Parent did not pass its own declared checks")
        if tuple(c["name"] for c in result["payload"]["cases"]) != NAMES:
            raise RuntimeError("Parent preparation census differs")
        for relative, expected in freeze["files"].items():
            path = ROOT/relative
            if not path.resolve().is_relative_to(ROOT) or path.is_symlink():
                raise RuntimeError("Source path leaves project or is a symlink")
            actual = digest(path)
            if actual != expected:
                raise RuntimeError("Frozen source differs: " + relative)
            identities[relative] = actual
        accepted.append(result)
    spec = importlib.util.spec_from_file_location("endpoint_owned_16d", HERE/"record_addition_compute.py")
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)  # Definitions only; never native.run().
    identities[str(Path(__file__).relative_to(ROOT))] = digest(Path(__file__))
    return accepted[0], accepted[1], native, identities


def run():
    started = time.perf_counter()
    old, clock, native, identities = inputs()
    checks, cases = [], []

    def check(name, actual, expected=0., tolerance=TOL):
        residual = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
        checks.append(dict(name=name, residual=residual, tolerance=tolerance,
                           passed=bool(math.isfinite(residual) and residual <= tolerance)))

    def real(name, value):
        check(name+":imaginary_part", value.imag)
        return float(value.real)

    o, identity = native.operators(), native.I
    pR, pL = o["carrier_right"], identity-o["carrier_right"]
    aL, aR, n, xC = o["AL"], o["AR"], o["n"], o["XC"]
    yC = -o["YC"]  # Conventional Pauli Y, unlike saved record quadrature.
    swap = np.zeros((16, 16), complex)
    for index in range(16):
        left, right, link, carrier = (index >> 3) & 1, (index >> 2) & 1, (index >> 1) & 1, index & 1
        swap[(right << 3) | (left << 2) | (link << 1) | carrier, index] = 1.
    check("record_swap_unitary", swap.conj().T @ swap, identity)
    check("record_swap_exchanges_clocks", swap @ aL @ swap, aR)
    check("kick_is_projector", pL @ pL, pL)
    check("kick_preserves_record_swap", comm(pL, swap))
    for saved, qualified in zip(old["payload"]["cases"], clock["payload"]["cases"]):
        name, params = saved["name"], saved["parameters"]
        if name != qualified["name"] or params != qualified["parameters"]:
            raise RuntimeError("Clock and state do not share one preparation")
        expected = dict(native.PARAMETERS)
        if name == "feedback_off":
            expected["lambda_R"] = 0.
        if name == "copying_off":
            expected["g"] = 0.
        if params != expected or saved["dimension"] != 16:
            raise RuntimeError("Unexpected inherited parent")
        H, terms = native.hamiltonian(dict(params, g=0.), o)
        Hform, _ = native.hamiltonian(params, o)  # Symmetry only, no formation.
        psi0 = np.array(saved["formed_vector"]["real"])+1j*np.array(saved["formed_vector"]["imag"])
        check(name+":formed_norm", np.vdot(psi0, psi0), 1.)
        check(name+":same_held_energy", ex(psi0, H), saved["held_energy"])
        check(name+":full_energy_term_sum", H, sum(terms.values()))
        check(name+":held_record_swap", comm(H, swap))
        check(name+":formation_record_swap", comm(Hform, swap))
        check(name+":formed_record_swap", swap @ psi0, psi0)
        values, vectors = np.linalg.eigh(H)
        propagators = {}

        def U(duration):
            if duration not in propagators:
                propagators[duration] = (vectors*np.exp(-1j*duration*values/HBAR)) @ vectors.conj().T
            return propagators[duration]

        adot = 1j*comm(H, aR)/HBAR
        pdot = 1j*comm(H, pR)/HBAR
        check(name+":carrier_derivative", pdot, params["t_hop"]*n @ yC/HBAR)
        check(name+":source_first_delay", 1j*comm(pL, pdot), params["t_hop"]*n @ xC/HBAR)
        check(name+":clock_zero_delay_source", comm(pL, aR))
        check(name+":clock_first_delay_source", comm(pL, adot))
        check(name+":clock_second_delay_source", comm(pL, comm(H, comm(H, aR))))
        check(name+":source_work_linear", 1j*comm(pL, H), params["t_hop"]*n @ yC)
        check(name+":source_work_even", -comm(pL, comm(pL, H)), params["t_hop"]*n @ xC)
        bound = qualified["continuous_bounds"][-1]
        defined = name != "copying_off"
        if defined and bound["orientation"] != "positive_whole_window":
            raise RuntimeError("Inherited clock window is not qualified")
        certificate = dict(window=[0., 2.], method="record-only swap transfers saved global certificate; no new grid",
                           local_amplitude_lower_bound=bound["amplitude_lower_bound"]/2 if defined else None,
                           local_phase_numerator_lower_bound=bound["numerator_lower_bound"]/4 if defined else None,
                           phase_rate_lower_bound=bound["phase_rate_lower_bound"] if defined else None,
                           phase_rate_upper_bound=bound["phase_rate_upper_bound"] if defined else None,
                           inherited_numerical_allowance=clock["payload"]["numerical_allowance"],
                           status="positive_whole_window" if defined else "undefined_exact_blank")
        finite_certificates = []
        for alpha in ANGLES:
            # For any pure state and projector kick the trace distance is at most
            # 2|sin(alpha/2)|. This persists under the same subsequent unitary.
            # |delta<a>|<=d, |delta<adot>|<=d*(|epsilon_r|+|lambda_R|)/hbar.
            distance_bound = 2*abs(math.sin(alpha/2))
            adot_norm_bound = (abs(params["epsilon_r"])+abs(params["lambda_R"]))/HBAR
            if defined:
                base_a_max = qualified["moments_M0_M1_M2"][0]/2
                base_ad_max = qualified["moments_M0_M1_M2"][1]/2
                delta_numerator = (base_a_max*distance_bound*adot_norm_bound
                                   +base_ad_max*distance_bound+distance_bound**2*adot_norm_bound)
                amin = certificate["local_amplitude_lower_bound"]-distance_bound
                nmin = certificate["local_phase_numerator_lower_bound"]-delta_numerator
                status = "positive_after_kick_on_inherited_window" if amin > 0 and nmin > 0 else "inconclusive"
            else:
                amin = nmin = None
                status = "undefined_exact_blank"
            finite_certificates.append(dict(alpha=alpha, trace_distance_bound=distance_bound,
                                            amplitude_lower_bound=amin, phase_numerator_lower_bound=nmin,
                                            status=status, scope="both signs; reception times emission..2 only"))
        rows = []
        for age in AGES:
            state = U(age) @ psi0
            at_emit = ex(state, aR)
            check(name+f":emit{age}:local_clock_equality", ex(state, aL), at_emit)
            saved_clock = next(x for x in qualified["ages"] if x["age"] == age)
            check(name+f":emit{age}:saved_global_clock", 2*at_emit,
                  complex(saved_clock["A"]["real"], saved_clock["A"]["imag"]))
            source_slope = real(name+f":emit{age}:slope", ex(state, 1j*comm(pL, pdot)))
            check(name+f":emit{age}:slope_identity", source_slope,
                  params["t_hop"]*ex(state, n @ xC)/HBAR)
            kick_records = {}
            for alpha in ANGLES:
                signed = []
                for sign in (-1, 1):
                    angle = sign*alpha
                    kick = identity+np.expm1(-1j*angle)*pL
                    kicked = kick @ state
                    work = real(name+f":{age}:{angle}:work", ex(kicked, H)-ex(state, H))
                    predicted_work = params["t_hop"]*(math.sin(angle)*ex(state, n @ yC)
                                                        +2*math.sin(angle/2)**2*ex(state, n @ xC))
                    check(name+f":{age}:{angle}:work_identity", work, predicted_work)
                    check(name+f":{age}:{angle}:emission_clock_unchanged", ex(kicked, aR), at_emit)
                    signed.append(dict(alpha=angle, state=kicked, work=work))
                kick_records[alpha] = signed
            for delay in DELAYS:
                receive = age+delay
                if not 0 <= receive <= 2:
                    raise RuntimeError("Reception outside inherited hold window")
                stem = name+f":{age}:{delay}:"
                advance = U(delay)
                endpoint = advance @ state
                direct_endpoint = U(receive) @ psi0
                check(stem+"same_endpoint_state", endpoint, direct_endpoint)
                taylor, _ = native.taylor_propagator(H, delay)
                check(stem+"independent_taylor_state", taylor @ state, endpoint)
                p_end = ex(endpoint, pR)
                a_end = ex(endpoint, aR)
                ad_end = ex(endpoint, adot)
                pd_end = ex(endpoint, pdot)
                check(stem+"local_clock_equality", ex(endpoint, aL), a_end)
                opP = advance.conj().T @ pR @ advance
                opA = advance.conj().T @ aR @ advance
                RP = ex(state, 1j*comm(pL, opP))
                RA = ex(state, 1j*comm(pL, opA))
                DP = ex(state, -comm(pL, comm(pL, opP)))
                DA = ex(state, -comm(pL, comm(pL, opA)))
                rp = real(stem+"R_pR", RP)
                drift = real(stem+"pR_drift", pd_end)
                nu = phase_response = time_response = relational = None
                if defined:
                    if abs(a_end) <= certificate["local_amplitude_lower_bound"]-TOL:
                        raise RuntimeError("Actual local clock violates inherited amplitude certificate")
                    nu = float((a_end.conjugate()*ad_end).imag/abs(a_end)**2)
                    check(stem+"clock_rate_identity", nu,
                          (params["epsilon_r"]-params["lambda_R"]*(ex(endpoint, n @ aR)/a_end).real)/HBAR)
                    phase_response = float((RA/a_end).imag)
                    time_response = -phase_response/nu
                    relational = rp+drift*time_response
                else:
                    check(stem+"blank_A", a_end)
                    check(stem+"blank_R_A", RA)
                if name == "feedback_off":
                    check(stem+"feedback_clock_response_zero", RA)
                    check(stem+"feedback_clock_rate_one", nu, 1.)
                    check(stem+"feedback_relational_equals_fixed_time", relational, rp)
                finite_rows = []
                for alpha in ANGLES:
                    observed = []
                    sine, even = math.sin(alpha), 2*math.sin(alpha/2)**2
                    for kickrow in kick_records[alpha]:
                        angle = kickrow["alpha"]
                        final = advance @ kickrow["state"]
                        pp, aa = ex(final, pR), ex(final, aR)
                        check(stem+f"kick{angle}:probability_identity", pp-p_end,
                              math.sin(angle)*RP+even*DP)
                        check(stem+f"kick{angle}:complex_clock_identity", aa-a_end,
                              math.sin(angle)*RA+even*DA)
                        check(stem+f"kick{angle}:same_energy", ex(final, H), ex(state, H)+kickrow["work"])
                        observed.append(dict(alpha=angle, carrier_right=real(stem+f"kick{angle}:pR", pp),
                                             A_R=cj(aa), work=kickrow["work"],
                                             phase_change=float(np.angle(aa*a_end.conjugate())) if defined else None))
                    minus, plus = observed
                    fd_p = (plus["carrier_right"]-minus["carrier_right"])/(2*sine)
                    av = [complex(x["A_R"]["real"], x["A_R"]["imag"]) for x in observed]
                    fd_a = (av[1]-av[0])/(2*sine)
                    divided_allowance = TOL*(1+1/abs(sine))
                    check(stem+f"alpha{alpha}:sine_centered_R_pR", fd_p, RP, divided_allowance)
                    check(stem+f"alpha{alpha}:sine_centered_R_A", fd_a, RA, divided_allowance)
                    phase_fd = phase_error_bound = None
                    if defined:
                        rr, dd = RA/a_end, DA/a_end
                        zminus, zplus = -sine*rr+even*dd, sine*rr+even*dd
                        if max(abs(zminus), abs(zplus)) >= 1:
                            raise RuntimeError("Finite phase log left its predeclared local branch")
                        # log(1+z)=z-z²/2+R3, |R3|<=|z|³/[3(1-|z|)].
                        phase_error_bound = even*abs(rr*dd)+sum(abs(z)**3/(3*(1-abs(z)))
                                                                               for z in (zminus, zplus))/(2*abs(sine))
                        phase_fd = (plus["phase_change"]-minus["phase_change"])/(2*sine)
                        phase_roundoff = divided_allowance*(1+1/certificate["local_amplitude_lower_bound"])
                        check(stem+f"alpha{alpha}:phase_log_control", phase_fd, phase_response,
                              phase_error_bound+phase_roundoff)
                    finite_rows.append(dict(alpha=alpha, signed=observed, sine_centered_R_pR=fd_p,
                                            sine_centered_R_A=cj(fd_a), roundoff_allowance=divided_allowance,
                                            sine_centered_phase_derivative=phase_fd,
                                            phase_log_truncation_bound=phase_error_bound))
                rows.append(dict(emission_age=age, delay=delay, reception_age=receive,
                                 A_L_emission=cj(at_emit), A_R_reception=cj(a_end),
                                 receiver_phase_rate=nu, carrier_right=real(stem+"baseline_pR", p_end),
                                 carrier_drift=drift, R_pR=rp, R_A_R=cj(RA),
                                 phase_response_per_alpha=phase_response,
                                 equal_phase_time_shift_per_alpha=time_response,
                                 R_rel=relational, source_first_delay_derivative=source_slope,
                                 finite_kicks=finite_rows))
        cases.append(dict(name=name, parameters=params, local_clock_certificate=certificate,
                          finite_kick_clock_certificates=finite_certificates, rows=rows))
    failures = [checkrow for checkrow in checks if not checkrow["passed"]]
    for relative, expected in identities.items():
        if digest(ROOT/relative) != expected:
            raise RuntimeError("Input/source changed during computation: "+relative)
    payload = dict(scope="Same saved writer-formed 16D endpoint signal and record clocks; informational phase kick, not photons, distance, arrival, redshift or expansion.",
                   source="H + hbar*alpha*p_L*delta(t-emission); U=exp(-i alpha p_L)",
                   readout="Infinitesimal receiver-clock endpoint correction; no finite equal-phase root inversion.",
                   hbar=HBAR, emission_ages=AGES, delays=DELAYS, kick_angles=ANGLES, tolerance=TOL,
                   tolerance_scope="Inherited16D roundoff allowance; exact sin/even kick identities; explicit divided-difference amplification and analytic phase-log remainder.",
                   source_identities=identities, cases=cases, checks=checks,
                   count=dict(cases=len(cases), rows=sum(len(case["rows"]) for case in cases),
                              checks=len(checks), failed_checks=len(failures)))
    peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = dict(status="ASSIGNED_CHECKS_PASS_NOT_PHYSICAL_QUALIFICATION" if not failures else "FAILED_ASSIGNED_CHECKS",
                  payload=payload, payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),
                  seconds=time.perf_counter()-started,
                  peak_self_rss_bytes=peak_rss if sys.platform == "darwin" else peak_rss*1024)
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0 if not failures else 2


if __name__ == "__main__":
    if sys.argv[1:] != ["--run"]:
        raise SystemExit("Explicit --run required; stdout JSON only, no output files written")
    raise SystemExit(run())
