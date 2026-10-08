"""Exact saved-state incidence/clock derivative census; freeze before run."""
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
PREFIX = "native_relational_slope_v001_"
AGES = (0., .25, .5, 1., 2.)
TOL = 1e-11
CLOCK_RESULT = "native_phase_clock_v001_results.json"
CLOCK_FREEZE = "native_phase_clock_v001_frozen.json"
CLOCK_RESULT_HASH = "5992e6daf072b3873670d22c280f4f1592e95a0f250eb703d919d6d548f21206"
CLOCK_FREEZE_HASH = "e01ceac78343ea49d29cebc8b555d77509427d172439339380e6e80c4a4eb70f"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    answer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(answer)
    return answer


def save_new(name, value):
    with tempfile.NamedTemporaryFile(mode="w", dir=HERE, prefix=name+".partial.", delete=False) as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+"\n")
        handle.flush()
        os.fsync(handle.fileno())
        temporary = Path(handle.name)
    os.link(temporary, HERE/name)
    temporary.unlink()


def inputs():
    clock = module("owned_clock_auth", HERE/"native_phase_clock_v001_compute.py")
    ancestors, old_snapshot = clock.inputs()
    if digest(HERE/CLOCK_RESULT) != CLOCK_RESULT_HASH or digest(HERE/CLOCK_FREEZE) != CLOCK_FREEZE_HASH:
        raise RuntimeError("Clock byte authentication failed")
    result = json.loads((HERE/CLOCK_RESULT).read_text())
    freeze = json.loads((HERE/CLOCK_FREEZE).read_text())
    if encoded(freeze) != encoded(old_snapshot):
        raise RuntimeError("Clock source authentication failed")
    if result["freeze_sha256"] != CLOCK_FREEZE_HASH or result["payload_sha256"] != hashlib.sha256(encoded(result["payload"])).hexdigest():
        raise RuntimeError("Clock payload/freeze link failed")
    if result["status"] != "COMPLETE" or not all(x["passed"] for x in result["payload"]["checks"]):
        raise RuntimeError("Clock qualification did not pass")
    files = dict(freeze["files"])
    for path in (Path(__file__).resolve(), HERE/"NATIVE_RELATIONAL_SLOPE_PROTOCOL_V001.md",
                 HERE/"NATIVE_RELATIONAL_RESPONSE_DERIVATION_V001.md", HERE/CLOCK_RESULT, HERE/CLOCK_FREEZE):
        files[str(path.relative_to(WORKSPACE))] = digest(path)
    return ancestors[0], result, dict(files=files, ages=AGES, tolerance=TOL,
                                     source="H-eta*n*delta(native_time-w); eta has action units")


def cj(value):
    return dict(real=float(value.real), imag=float(value.imag))


def run():
    started = time.perf_counter()
    old, clock, snapshot = inputs()
    freeze_path = HERE/(PREFIX+"frozen.json")
    if encoded(json.loads(freeze_path.read_text())) != encoded(snapshot):
        raise RuntimeError("New source freeze mismatch")
    native = module("owned_relational_matrices", HERE/"record_addition_compute.py")
    o, identity = native.operators(), native.I
    n, x, z = o["n"], o["Xa"], o["Za"]
    y = -native.embed(native.Y2, 2)  # Link conventional Pauli Y.
    a, r = o["AL"]+o["AR"], o["QL"]+o["QR"]
    comm = native.comm
    checks, cases = [], []

    def check(name, actual, expected=0., tolerance=TOL):
        error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
        checks.append(dict(name=name, residual=error, tolerance=tolerance,
                           passed=bool(math.isfinite(error) and error <= tolerance)))

    def ex(state, op):
        return np.vdot(state, op @ state)

    def summary(rows, key):
        values = [v[key] for v in rows if v[key] is not None]
        if not values:
            return dict(defined_rows=0, minimum=None, maximum=None, spread=None,
                        all_positive=None, constant_compatible=None)
        lo, hi = min(values), max(values)
        return dict(defined_rows=len(values), minimum=lo, maximum=hi, spread=hi-lo,
                    all_positive=bool(lo>TOL), constant_compatible=bool(hi-lo<=2*TOL),
                    positive_constant_compatible=bool(lo>TOL and hi-lo<=2*TOL))

    for saved, qualified in zip(old["payload"]["cases"], clock["payload"]["cases"]):
        name, p = saved["name"], saved["parameters"]
        if name != qualified["name"] or p != qualified["parameters"] or tuple(v["age"] for v in qualified["ages"]) != AGES:
            raise RuntimeError("Saved census differs")
        if name != "copying_off" and not all(v["orientation"] == "positive_whole_window" for v in qualified["continuous_bounds"]):
            raise RuntimeError("Qualified phase domain differs")
        h, _ = native.hamiltonian(dict(p, g=0.), o)
        psi = np.array(saved["formed_vector"]["real"])+1j*np.array(saved["formed_vector"]["imag"])
        b = 2.25*identity-p["lambda_R"]*r-.5*o["XC"]
        d = p["epsilon_r"]*identity-p["lambda_R"]*n
        adot = 1j*comm(h, a)
        mdot_op = 1j*comm(h, n)
        ann0 = 1j*comm(a, n)
        ann1 = -comm(comm(h, a), n)
        ann2 = -1j*comm(comm(h, comm(h, a)), n)
        nn1 = -comm(comm(h, n), n)
        nn2 = -1j*comm(comm(h, comm(h, n)), n)
        check(name+":held_A_commutator", comm(h, a), d @ a)
        check(name+":held_n_commutator", comm(h, n), -1j*p["h"]*y)
        check(name+":A_source_zero_delay", ann0)
        check(name+":A_source_first_delay", ann1)
        check(name+":A_source_second_delay", ann2, -1j*p["lambda_R"]*p["h"]*x @ a)
        check(name+":incidence_first_delay", nn1, p["h"]*x)
        check(name+":incidence_second_delay", nn2, p["h"]*b @ y)
        check(name+":incidence_double_H", comm(h, comm(h, n)), -2*p["h"]**2*z+p["h"]*b @ x)
        rows = []
        for age, old_age, clock_age in zip(AGES, saved["hold"], qualified["ages"]):
            if old_age["time"] != age:
                raise RuntimeError("Old hold age changed")
            state = native.spectral_propagator(h, age) @ psi
            aa, derivative, xa = ex(state, a), ex(state, adot), ex(state, x @ a)
            n_mean, x_mean, drift = ex(state, n), ex(state, x), ex(state, mdot_op)
            slope = p["h"]*x_mean
            nn_second, an_second = ex(state, nn2), ex(state, ann2)
            stem = name+f":{age}:"
            for label, value in (("n_real", n_mean), ("X_real", x_mean), ("drift_real", drift),
                                 ("slope_real", slope), ("nn_second_real", nn_second)):
                check(stem+label, value.imag)
            check(stem+"norm", ex(state, identity), 1.)
            check(stem+"saved_n", n_mean, old_age["link_occupation"])
            check(stem+"saved_flip_strength", slope, -old_age["energy_terms"]["incidence_flip"])
            check(stem+"saved_A", aa, complex(clock_age["A"]["real"], clock_age["A"]["imag"]))
            check(stem+"saved_Adot", derivative, complex(clock_age["Adot"]["real"], clock_age["Adot"]["imag"]))
            check(stem+"drift_formula", drift, p["h"]*ex(state, y))
            check(stem+"slope_commutator", slope, ex(state, nn1))
            check(stem+"An_second_formula", an_second, -1j*p["lambda_R"]*p["h"]*xa)
            check(stem+"nn_second_formula", nn_second, p["h"]*ex(state, b @ y))
            nu = ratio = phase_slope = phase_shift = timing_shift = timing_incidence = None
            if name == "copying_off":
                check(stem+"blank_A", aa)
                check(stem+"blank_An_second", an_second)
            else:
                nu = float(clock_age["phase_rate"])
                check(stem+"saved_phase_rate", (aa.conjugate()*derivative).imag/abs(aa)**2, nu)
                ratio = xa/aa
                phase_slope = float(slope.real/nu)
                phase_shift = float((an_second/aa).imag/2)
                timing_shift = -phase_shift/nu
                timing_incidence = float(drift.real*timing_shift)
                check(stem+"phase_shift_formula", phase_shift, -p["lambda_R"]*p["h"]*ratio.real/2)
                check(stem+"time_shift_formula", timing_shift, p["lambda_R"]*p["h"]*ratio.real/(2*nu))
                if name == "feedback_off":
                    check(stem+"feedback_zero_clock_backreaction", an_second)
                    check(stem+"feedback_unit_clock", nu, 1.)
            rows.append(dict(age=age, phase_rate=nu, incidence=float(n_mean.real), X=float(x_mean.real),
                             incidence_drift=float(drift.real), XA=cj(xa), XA_over_A=cj(ratio) if ratio is not None else None,
                             laboratory_initial_slope=float(slope.real), equal_phase_initial_slope=phase_slope,
                             incidence_second_delay_derivative=float(nn_second.real), A_second_delay_derivative=cj(an_second),
                             phase_shift_tau2_per_impulse=phase_shift, readout_time_shift_tau2_per_impulse=timing_shift,
                             incidence_timing_correction_tau2_per_impulse=timing_incidence))
        cases.append(dict(name=name, parameters=p, rows=rows,
                          laboratory_summary=summary(rows, "laboratory_initial_slope"),
                          phase_summary=summary(rows, "equal_phase_initial_slope")))
    all_rows = [row for case in cases for row in case["rows"]]
    failures = [row for row in checks if not row["passed"]]
    payload = dict(scope="Exact saved-state short-delay derivatives; integrated native-time incidence impulse; no fixed mass fitted or physical clock conversion.",
                   ages=AGES, tolerance=TOL, cases=cases, checks=checks,
                   pooled_phase_summary=summary(all_rows, "equal_phase_initial_slope"),
                   pooled_scope="Descriptive only: feedback_off changes its Hamiltonian; each preparation has its own fixed-parent summary.")
    result = dict(status="COMPLETE" if not failures else "FAILED", payload=payload,
                  payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(), freeze_sha256=digest(freeze_path),
                  seconds=time.perf_counter()-started, peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    save_new(PREFIX+"results.json", result)
    print(json.dumps(dict(status=result["status"], checks=len(checks), failures=failures,
                         seconds=result["seconds"], peak_self_rss_bytes=result["peak_self_rss_bytes"],
                         cases=[dict(name=c["name"], laboratory=c["laboratory_summary"], phase=c["phase_summary"]) for c in cases]), allow_nan=False))


if __name__ == "__main__":
    if sys.argv[1:] == ["freeze"]:
        _, _, snapshot = inputs()
        save_new(PREFIX+"frozen.json", snapshot)
    elif sys.argv[1:] == ["run"]:
        run()
    else:
        raise SystemExit("Explicit freeze or run required")
