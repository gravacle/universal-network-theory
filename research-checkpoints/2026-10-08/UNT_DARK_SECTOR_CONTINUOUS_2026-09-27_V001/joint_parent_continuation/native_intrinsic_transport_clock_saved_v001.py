"""Saved-arithmetic coefficient for a proposed, explicitly owned SWAP readout.

At each inherited held age, propose a fresh degenerate pointer in |L> and
an ideal unitary SWAP of pointer and carrier-position qubits. The carrier
then has state |L>; all its old correlations are retained in the pointer,
not erased for free. The environment marginal, n, A and nA are unchanged.
Record-swap symmetry gives local A=A_total/2 and the same initial clock rate.

With copying held off and the inherited Hamiltonian, the right-occupation
probability after the proposed preparation is t_hop**2 * <n> * tau**2/hbar**2
+ O(tau**3). Thus K=t_hop**2*<n>/(hbar**2*nu**2) multiplies theta**2 in
receiver-clock phase theta, with only a generic O(theta**3) remainder claimed.
This is an exact local derivative coefficient, not a finite transit time or
speed. The old [0,2] clock certificate does not transfer to the post-SWAP
trajectory beyond its initial derivative. No SWAP or subsequent propagation
is numerically performed here; only authenticated saved scalars are used.

All held bulk terms are carrier independent except -t_hop*n*X_C; the
current-squared term is lambda_J*n because Y_C**2=I. Post-SWAP hopping energy
is zero, so ideal switching work into the bulk is -saved carrier_hopping.
Fresh-pointer preparation, control implementation and eventual pointer reuse
are resources not computed here; this is not a complete apparatus work cost.

Stdlib only, stdout only, no file writes/imported producer/eigensolve/evolution.
Root alone executes. The 1e-10 allowance is inherited, not outcome-selected.
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
NAMES = ("native", "feedback_off", "copying_off")
AGES = (0., .25, .5, 1., 2.)
HBAR = 1.
ALLOWANCE = 1e-10
PARAMETERS = dict(h=1., Delta=4., U_d=1., d_star=1., epsilon_psi=1.,
                  epsilon_r=1., epsilon_w=0., t_hop=.5, lambda_R=.5,
                  lambda_J=.25, g=1.)
TERM_NAMES = frozenset(("incidence_flip", "incidence_bias",
    "both_endpoint_degree_penalties", "carrier_occupation", "both_record_storage",
    "both_writer_storage", "carrier_hopping", "record_incidence_feedback",
    "current_squared_feedback", "copy_left", "copy_right"))
PINS = {
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
    return dict(real=value.real, imag=value.imag)


def z(value):
    if set(value) != {"real", "imag"}:
        raise RuntimeError("Unexpected complex scalar schema")
    out = complex(value["real"], value["imag"])
    if not math.isfinite(out.real) or not math.isfinite(out.imag):
        raise RuntimeError("Nonfinite saved complex scalar")
    return out


def inputs():
    if ROOT != Path("/Users/bgm/Documents/ChatGPT/Universal Network Theory"):
        raise RuntimeError("Wrong project root")
    identities = {}
    for name, expected in PINS.items():
        path = HERE/name
        if path.is_symlink() or not path.resolve(strict=True).is_relative_to(ROOT):
            raise RuntimeError("Input is linked or outside the project")
        if digest(path) != expected:
            raise RuntimeError("Pinned input differs: "+name)
        identities[str(path.relative_to(ROOT))] = expected
    accepted = []
    for result_name, freeze_name in (
        ("RECORD_ADDITION_RESULTS.json", "RECORD_ADDITION_FROZEN.json"),
        ("native_phase_clock_v001_results.json", "native_phase_clock_v001_frozen.json"),
    ):
        saved = json.loads((HERE/result_name).read_text())
        frozen = json.loads((HERE/freeze_name).read_text())
        if saved["freeze_sha256"] != PINS[freeze_name]:
            raise RuntimeError("Parent freeze binding differs")
        if saved["payload_sha256"] != hashlib.sha256(encode(saved["payload"])).hexdigest():
            raise RuntimeError("Parent payload binding differs")
        if saved["status"] != "COMPLETE" or not saved["payload"]["checks"] or not all(
                item["passed"] for item in saved["payload"]["checks"]):
            raise RuntimeError("Parent did not pass its assigned controls")
        if tuple(case["name"] for case in saved["payload"]["cases"]) != NAMES:
            raise RuntimeError("Parent case census differs")
        for relative, expected in frozen["files"].items():
            path = ROOT/relative
            if path.is_symlink() or not path.resolve(strict=True).is_relative_to(ROOT):
                raise RuntimeError("Frozen path is linked or outside project")
            if digest(path) != expected:
                raise RuntimeError("Frozen source differs: "+relative)
            identities[relative] = expected
        accepted.append(saved)
    if tuple(accepted[1]["payload"]["ages"]) != AGES:
        raise RuntimeError("Clock age census differs")
    if accepted[1]["payload"]["numerical_allowance"] != ALLOWANCE:
        raise RuntimeError("Inherited numerical allowance differs")
    identities[str(Path(__file__).relative_to(ROOT))] = digest(Path(__file__))
    return accepted[0], accepted[1], identities


def run():
    started = time.perf_counter()
    old, clock, identities = inputs()
    checks, cases = [], []

    def check(name, actual, expected=0.):
        residual = abs(actual-expected)
        passed = math.isfinite(residual) and residual <= ALLOWANCE
        checks.append(dict(name=name, residual=residual if math.isfinite(residual) else None,
                           tolerance=ALLOWANCE, passed=passed))

    def yes(name, condition):
        check(name, int(bool(condition)), 1)

    for saved, qualified in zip(old["payload"]["cases"], clock["payload"]["cases"]):
        name, p = saved["name"], saved["parameters"]
        expected = dict(PARAMETERS)
        if name == "feedback_off":
            expected["lambda_R"] = 0.
        if name == "copying_off":
            expected["g"] = 0.
        if p != expected or qualified["parameters"] != expected or qualified["name"] != name:
            raise RuntimeError("Altered preparation/parameter census")
        if saved["dimension"] != 16 or saved["formation_duration"] != 1.:
            raise RuntimeError("Altered original preparation")
        if tuple(row["time"] for row in saved["hold"]) != AGES or tuple(
                row["age"] for row in qualified["ages"]) != AGES:
            raise RuntimeError("Altered held-age census")
        rows = []
        check(name+":formation_to_hold_work", saved["held_energy"]-saved["formed_energy"], saved["quench_work"])
        for held, phase in zip(saved["hold"], qualified["ages"]):
            age = held["time"]
            stem = name+":"+str(age)+":"
            terms = held["energy_terms"]
            if set(terms) != TERM_NAMES or len(held["count_probabilities"]) != 3:
                raise RuntimeError("Altered term or record-count census")
            n, count = held["link_occupation"], held["record_count"]
            probabilities = held["count_probabilities"]
            yes(stem+"occupation_domain", -ALLOWANCE <= n <= 1+ALLOWANCE)
            yes(stem+"record_probability_domain", all(-ALLOWANCE <= v <= 1+ALLOWANCE for v in probabilities))
            check(stem+"record_probability_sum", math.fsum(probabilities), 1.)
            check(stem+"record_count_from_probabilities", math.fsum(i*v for i, v in enumerate(probabilities)), count)
            check(stem+"record_count_fixed_during_hold", count, saved["hold"][0]["record_count"])
            check(stem+"record_storage", terms["both_record_storage"], p["epsilon_r"]*count)
            check(stem+"incidence_bias", terms["incidence_bias"], p["Delta"]*n)
            degree = 2*p["U_d"]*((1-n)*p["d_star"]**2+n*(1-p["d_star"])**2)
            check(stem+"degree_energy", terms["both_endpoint_degree_penalties"], degree)
            check(stem+"current_squared_energy", terms["current_squared_feedback"], p["lambda_J"]*n)
            check(stem+"carrier_occupation_energy", terms["carrier_occupation"], p["epsilon_psi"])
            check(stem+"writer_storage", terms["both_writer_storage"], 2*p["epsilon_w"])
            check(stem+"held_copy_left", terms["copy_left"])
            check(stem+"held_copy_right", terms["copy_right"])
            before = math.fsum(terms.values())
            check(stem+"held_energy_sum", before, saved["held_energy"])
            work = -terms["carrier_hopping"]
            after_terms = dict(terms, carrier_hopping=0.)
            after = math.fsum(after_terms.values())
            check(stem+"swap_work_from_full_energy_difference", after-before, work)
            check(stem+"post_swap_energy_bookkeeping", after, saved["held_energy"]+work)

            A, Adot, nA = z(phase["A"]), z(phase["Adot"]), z(phase["nA"])
            amplitude = abs(A)
            numerator = (A.conjugate()*Adot).imag
            check(stem+"saved_amplitude", amplitude, phase["amplitude"])
            check(stem+"saved_phase_numerator", numerator, phase["phase_numerator"])
            check(stem+"Adot_native_commutator", Adot, 1j*(p["epsilon_r"]*A-p["lambda_R"]*nA)/HBAR)
            local_A, local_Adot, local_nA = A/2, Adot/2, nA/2
            # Local expectations equal half the global ones by the existing
            # record-swap symmetry; no new aged state is reconstructed here.
            nu = detuning_nu = alternative_K = K = None
            time_coefficient = p["t_hop"]**2*n/HBAR**2
            coefficient_from_current_energy = p["t_hop"]**2*terms["current_squared_feedback"]/(HBAR**2*p["lambda_J"])
            check(stem+"transport_time_coefficient_from_current_energy", time_coefficient, coefficient_from_current_energy)
            if name == "copying_off":
                check(stem+"blank_record_count", count)
                check(stem+"blank_A", A)
                check(stem+"blank_Adot", Adot)
                check(stem+"blank_nA", nA)
                yes(stem+"saved_phase_undefined", phase["phase_rate"] is None)
                status = "UNDEFINED_PHASE_CLOCK_K_NULL_NOT_ZERO"
            else:
                yes(stem+"initial_clock_nonzero", amplitude > ALLOWANCE)
                if amplitude <= ALLOWANCE:
                    raise RuntimeError("Unexpected undefined initial clock in "+stem)
                nu = numerator/amplitude**2
                detuning = p["epsilon_r"]-p["lambda_R"]*(nA/A).real
                detuning_nu = detuning/HBAR
                local_nu = (local_A.conjugate()*local_Adot).imag/abs(local_A)**2
                check(stem+"saved_phase_rate", nu, phase["phase_rate"])
                check(stem+"exact_detuning_rate", nu, detuning_nu)
                check(stem+"endpoint_equals_global_initial_rate", local_nu, nu)
                yes(stem+"initial_clock_positive", nu > ALLOWANCE and detuning_nu > ALLOWANCE)
                if nu <= ALLOWANCE or detuning_nu <= ALLOWANCE:
                    raise RuntimeError("Unexpected unoriented initial clock in "+stem)
                K = time_coefficient/nu**2
                alternative_K = p["t_hop"]**2*n/detuning**2
                check(stem+"K_independent_detuning_expression", K, alternative_K)
                numerator_K = p["t_hop"]**2*n*amplitude**4/(HBAR**2*numerator**2)
                check(stem+"K_independent_phase_numerator_expression", K, numerator_K)
                if name == "feedback_off":
                    check(stem+"feedback_off_rate", nu, p["epsilon_r"]/HBAR)
                    check(stem+"feedback_off_K", K, p["t_hop"]**2*n/p["epsilon_r"]**2)
                status = "DEFINED_INITIAL_RELATIONAL_COEFFICIENT_ONLY"
            rows.append(dict(age=age, status=status, K=K, K_detuning_expression=alternative_K,
                nu=nu, nu_detuning_expression=detuning_nu, saved_phase_rate=phase["phase_rate"],
                global_A=cj(A), global_Adot=cj(Adot), global_nA=cj(nA),
                initial_endpoint_A=cj(local_A), initial_endpoint_Adot=cj(local_Adot), initial_endpoint_nA=cj(local_nA),
                global_phase_numerator=numerator, global_amplitude=amplitude,
                link_occupation=n, record_count=count, count_probabilities=probabilities,
                original_carrier_right=held["carrier_right"], post_swap_carrier_right=0.,
                transport_tau_squared_coefficient=time_coefficient,
                transport_probability_initial_second_derivative=2*time_coefficient,
                ideal_swap_bulk_switching_work=work, initial_bulk_energy=before,
                post_swap_bulk_energy=after, initial_energy_terms=terms,
                post_swap_initial_energy_terms=after_terms,
                pointer_internal_energy_change=0., pointer_reset_cost_computed=False,
                post_swap_finite_window_clock_qualified=False))
        cases.append(dict(name=name, parameters=p, held_copying_g=0., rows=rows))
    for relative, expected in identities.items():
        if digest(ROOT/relative) != expected:
            raise RuntimeError("Input/source changed during arithmetic: "+relative)
    failures = [item for item in checks if not item["passed"]]
    payload = dict(scope="Proposed ideal SWAP readout; saved-scalar local derivative and bulk-work arithmetic only, no new physical operation or evolution.",
        preparation="Fresh degenerate pointer |L>; SWAP carrier-position with pointer; retain pointer and its inherited environment correlations; no erasure.",
        caveats=["No implemented controller or total pointer preparation/reuse cost.",
                 "K is not a speed, metric, expansion rate or redshift prediction.",
                 "Only a generic O(theta^3) remainder is claimed.",
                 "Old [0,2] clock certificate does not qualify any post-SWAP finite window.",
                 "Copying-off has undefined K (null), not zero transport."],
        ages=AGES, preparations=NAMES, hbar=HBAR, numerical_allowance=ALLOWANCE,
        checks=checks, cases=cases, input_and_source_sha256=identities,
        code_sha256=digest(Path(__file__)), no_new_evolution_or_eigensolve=True)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = dict(status="COMPLETE_SAVED_ARITHMETIC" if not failures else "FAILED_SAVED_ARITHMETIC",
        payload=payload, payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),
        failures=failures, seconds=time.perf_counter()-started,
        peak_self_rss_bytes=peak if sys.platform == "darwin" else peak*1024)
    print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))
    return 2 if failures else 0


if __name__ == "__main__":
    if sys.argv[1:]:
        raise SystemExit("No arguments: one saved-arithmetic evaluation only")
    raise SystemExit(run())
