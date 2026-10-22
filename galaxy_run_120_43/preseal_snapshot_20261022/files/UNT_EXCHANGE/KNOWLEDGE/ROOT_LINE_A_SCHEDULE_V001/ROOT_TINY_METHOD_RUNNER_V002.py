"""Source-only root method harness, immutable V002. Not executed by author.
No native result/physical verdict; downstream launch requires separate review.
External supervisor owns wall/RSS/storage limits. A cap is not enforced here.
"""
import argparse
import hashlib
import json
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone

SOURCES = {
    "p58": ("/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0169_2026-10-13_P58-writer-map-source-v002.py",
            "d808ff469c06812c7b049eb2a0981f941cc26237cf9471d0d893110c0b29e640"),
    "cost": ("/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0115_2026-10-13_P59-P60-rational-cost-source.py",
             "aa4318e62377437c3158e8bec3cfafb4a4ebdda5241126bdd08285862a09ee73"),
}


def encode(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, dict):
        if any(not isinstance(k, str) for k in value):
            return {"exact_key_value_pairs": [[encode(k), encode(v)] for k, v in value.items()]}
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    if value is None or type(value) in (str, int, float, bool):
        return value
    raise TypeError("Unsupported output type: " + type(value).__name__)


def save(output, name, value):
    # x mode and a new output directory preserve failures and refuse collisions.
    with (output / name).open("x") as stream:
        json.dump(encode(value), stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


def p58_controls(module):
    result = module["proposed_method_controls"](tol=1e-10)
    complex_case = module["audit_population_map"](
        [[0, 1j], [-1j, 0]], [0, 1], 0.3, [1], tol=1e-10)
    witness = complex_case["same_probability_witness"]
    checks = dict(result["checks"])
    checks["complex_phase_witness"] = (
        witness is not None and witness["probability_defect"] < 1e-10
        and abs(witness["energy_difference"]) < 1e-10
        and abs(witness["q_rate_plus"] + witness["q_rate_minus"]) < 1e-10
        and abs(witness["q_rate_plus"]) > 0.9)
    return {"raw_builtin": result, "raw_complex": complex_case,
            "checks": checks, "all_checks": all(checks.values())}


def cost_controls(module):
    mixed = module["edge_mixed_cost"]
    bound = module["fixed_word_defect_bound"]
    cluster = module["isolated_cluster_sufficient_bound"]
    raw = {
        "n0": mixed(4, 0, 1, 1, 0),
        "n1": mixed(4, 0, 1, 1, 1),
        "h0": mixed(4, 0, 1, 0, 0),
        "r0": mixed(4, 0, 0, 1, 0),
        "symmetric_q": mixed(4, 1, 1, 1, 0),
        "word_bound": bound(3, 12, 3, 1, 2, [0, 0, 1, 1], [0, 1, 0, 1]),
        "inconclusive": bound(2, 8, 3, 1, 2, [0], [1]),
        "cluster": cluster(1, 4, 1),
        "cluster_inconclusive": cluster(1, 2, 1),
    }
    # Independently stated scalar expected fractions; no full-H certificate.
    expected_n0 = {(0, 0): Fraction(-1,4), (0, 1): Fraction(-1,3),
                   (1, 0): Fraction(-1,3), (1, 1): Fraction(-1,2)}
    expected_n1 = {(0, 0): Fraction(-1,4), (0, 1): Fraction(-1,5),
                   (1, 0): Fraction(-1,5), (1, 1): Fraction(-1,6)}
    checks = {
        "n0_arms": raw["n0"]["arms"] == expected_n0,
        "n0_mixed": raw["n0"]["mixed_cost"] == Fraction(-1,12),
        "n1_arms": raw["n1"]["arms"] == expected_n1,
        "n1_mixed": raw["n1"]["mixed_cost"] == Fraction(-1,60),
        "h0": raw["h0"]["mixed_cost"] == 0,
        "r0": raw["r0"]["mixed_cost"] == 0,
        "even_piece_survives": raw["symmetric_q"]["mixed_cost"] == Fraction(-1,30),
        "word_bound": raw["word_bound"]["delta"] == 1
                      and raw["word_bound"]["off_ice_lower_bound"] == 2,
        "zero_bound_inconclusive": raw["inconclusive"]["status"] == "INCONCLUSIVE"
                                   and raw["inconclusive"]["off_ice_lower_bound"] is None,
        "cluster": raw["cluster"]["bound"] == 1,
        "cluster_inconclusive": raw["cluster_inconclusive"]["status"] == "INCONCLUSIVE",
    }
    refusals = {}
    for name, call in [
        ("pole", lambda: mixed(2, 0, 1, 1, 0)),
        ("float", lambda: mixed(4.0, 0, 1, 1, 0)),
        ("nonbinary", lambda: mixed(4, 0, 1, 1, 2)),
        ("bad_word", lambda: bound(3, 12, 3, 1, 2, [0], [0,1])),
        ("negative_norm", lambda: cluster(1,4,-1)),
    ]:
        try:
            value = call()
        except (ValueError, TypeError) as error:
            refusals[name] = {"refused": True, "exception": type(error).__name__, "message": str(error)}
        else:
            refusals[name] = {"refused": False, "unexpected_return": value}
        checks["refuses_" + name] = refusals[name]["refused"]
    return {"raw": raw, "expected_n0": expected_n0, "expected_n1": expected_n1,
            "refusals": refusals, "checks": checks, "all_checks": all(checks.values())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=sorted(SOURCES))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    path, pin = SOURCES[args.kind]
    source = Path(path).read_bytes()
    if hashlib.sha256(source).hexdigest() != pin:
        raise ValueError("Pinned source changed; refuse before import")
    args.output.mkdir(exist_ok=False)
    save(args.output, "START.json", {
        "utc": datetime.now(timezone.utc).isoformat(), "kind": args.kind,
        "source": path, "sha256": pin, "scope": "TINY_METHOD_ONLY",
        "native_ensemble": "UNDETERMINED", "physical_acceptance": False,
        "supervisor_caps_required": True})
    module = {"__name__": "reviewed_method_module", "__file__": path}
    try:
        exec(compile(source, path, "exec"), module)
        result = p58_controls(module) if args.kind == "p58" else cost_controls(module)
        save(args.output, "RESULT.json", result)
        save(args.output, "FINISH.json", {
            "utc": datetime.now(timezone.utc).isoformat(),
            "status": "METHOD_CHECKS_PASS" if result["all_checks"] else "METHOD_CHECKS_FAIL",
            "physical_acceptance": False})
    except Exception as error:
        save(args.output, "FAILURE.json", {"exception": type(error).__name__, "message": str(error)})
        raise
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
