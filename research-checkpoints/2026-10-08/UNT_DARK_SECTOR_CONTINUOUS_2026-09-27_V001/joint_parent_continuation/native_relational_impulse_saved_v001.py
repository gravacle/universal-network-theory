"""Read authenticated original scalars; no SWAP, kick, evolution or eigensolve.

All three inherited preparations and all five ages are retained. The source
is an action-normalized incidence kick, not an energy-dipole gravity source.
The exploratory algebra was inspected before this reproducibility calculation;
it is not a blind experiment or newly unused evidence. Numerical consistency
uses the unchanged inherited 1e-10 allowance. Constancy/sign is not a pass gate.
Stdlib only; stdout only. Root executes one small worker at a time.
"""
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
INPUT = HERE / "native_intrinsic_transport_clock_saved_v001_results.json"
PIN = "0eeccca739e01ca89384cd35c30a9823fe6870d009337169e9801cc962609811"
NAMES = ("native", "feedback_off", "copying_off")
AGES = (0., .25, .5, 1., 2.)
TOL = 1e-10


def encode(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    started = time.perf_counter()
    if ROOT != Path("/Users/bgm/Documents/ChatGPT/Universal Network Theory"):
        raise RuntimeError("Wrong project root")
    if sha(INPUT) != PIN:
        raise RuntimeError("Pinned saved result changed")
    saved = json.loads(INPUT.read_text())
    p = saved["payload"]
    if saved["status"] != "COMPLETE_SAVED_ARITHMETIC" or saved["failures"]:
        raise RuntimeError("Input arithmetic incomplete")
    if hashlib.sha256(encode(p)).hexdigest() != saved["payload_sha256"]:
        raise RuntimeError("Input payload digest differs")
    if not p["checks"] or not all(c["passed"] for c in p["checks"]):
        raise RuntimeError("Input checks incomplete")
    identities = dict(p["input_and_source_sha256"])
    identities[str(INPUT.relative_to(ROOT))] = PIN
    identities[str(Path(__file__).relative_to(ROOT))] = sha(Path(__file__))
    for relative, expected in identities.items():
        path = ROOT / relative
        if path.is_symlink() or not path.resolve(strict=True).is_relative_to(ROOT) or sha(path) != expected:
            raise RuntimeError("Changed or out-of-project ancestor: " + relative)
    if tuple(p["ages"]) != AGES or tuple(c["name"] for c in p["cases"]) != NAMES:
        raise RuntimeError("Changed census")
    if p["numerical_allowance"] != TOL or p["hbar"] != 1.:
        raise RuntimeError("Changed allowance or units")
    checks, cases = [], []

    def ck(label, a, b):
        error = abs(a-b)
        checks.append(dict(label=label, error=error, allowance=TOL,
                           passed=math.isfinite(error) and error <= TOL))

    for case in p["cases"]:
        name, pars = case["name"], case["parameters"]
        if tuple(r["age"] for r in case["rows"]) != AGES:
            raise RuntimeError("Changed row census")
        rows = []
        for row in case["rows"]:
            stem = name + ":" + str(row["age"])
            # These are the original state's terms, not its proposed SWAP.
            flip = row["initial_energy_terms"]["incidence_flip"]
            X = -flip/pars["h"]
            S_time = pars["h"]*X  # hbar=1, dimensionless action kick.
            ck(stem+":energy_identity", S_time, -flip)
            def z(key):
                value = row[key]
                return complex(value["real"], value["imag"])
            A, Adot, nA = z("global_A"), z("global_Adot"), z("global_nA")
            ck(stem+":clock_commutator", Adot, 1j*(pars["epsilon_r"]*A-pars["lambda_R"]*nA))
            nu = slope = None
            if name == "copying_off":
                ck(stem+":undefined_clock_amplitude", A, 0.)
                if row["nu"] is not None:
                    raise RuntimeError("Undefined clock received a rate")
            else:
                if abs(A) <= TOL:
                    raise RuntimeError("Unexpected zero clock")
                nu = (A.conjugate()*Adot).imag/abs(A)**2
                ck(stem+":saved_rate", nu, row["nu"])
                ck(stem+":detuning_rate", nu, pars["epsilon_r"]-pars["lambda_R"]*(nA/A).real)
                if nu <= TOL:
                    raise RuntimeError("Unexpected nonpositive inherited clock")
                slope = S_time/nu
                ck(stem+":slope_reconstruction", slope*nu, S_time)
                if name == "feedback_off":
                    ck(stem+":feedback_off_clock", nu, 1.)
            rows.append(dict(age=row["age"], X=X, original_flip_energy=flip,
                action_kick_slope_protocol_time=S_time, native_clock_rate=nu,
                action_kick_slope_measured_phase=slope,
                defined=slope is not None))
        slopes = [r["action_kick_slope_measured_phase"] for r in rows if r["defined"]]
        cases.append(dict(name=name, rows=rows,
            relational_range=None if not slopes else [min(slopes), max(slopes)],
            relational_spread=None if not slopes else max(slopes)-min(slopes)))
    for relative, expected in identities.items():
        if sha(ROOT/relative) != expected:
            raise RuntimeError("Ancestor changed during arithmetic")
    failures = [c for c in checks if not c["passed"]]
    payload = dict(cases=cases, checks=checks, input_and_source_sha256=identities,
        scope="Original saved states; local measured-phase incidence-kick derivative only.",
        no_new_evolution_eigensolve_or_intervention=True, hbar=1., allowance=TOL,
        gravity_source_identified=False, finite_kick_window_qualified=False,
        source_or_clock_recalibrated=False, constancy_is_not_an_arithmetic_pass_gate=True)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(json.dumps(dict(status="COMPLETE_SAVED_ARITHMETIC" if not failures else "FAILED_SAVED_ARITHMETIC",
        payload=payload, payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),
        failures=failures, seconds=time.perf_counter()-started,
        peak_self_rss_bytes=peak if sys.platform == "darwin" else 1024*peak), sort_keys=True, indent=2))
    return 2 if failures else 0


if __name__ == "__main__":
    if sys.argv[1:]:
        raise SystemExit("No arguments")
    raise SystemExit(run())
