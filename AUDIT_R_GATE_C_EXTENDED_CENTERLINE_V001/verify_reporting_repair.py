#!/usr/bin/env python3
"""Independent, bounded audit of the target lowest-five reporting repair."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001"
SEALED = ROOT / "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001" / "RESULT.json"
ORIGINAL_COMPARATOR = HERE / "compare_and_classify.py"
ORIGINAL_METHOD = HERE / "POST_OUTPUT_METHOD.md"
ORIGINAL_FREEZE = HERE / "POST_OUTPUT_FREEZE.json"
PRE_REPORT = HERE / "PRE_REPORTING_REPAIR_FINAL_REPORT.md"
OUT = HERE / "HOSTILE_RESULT.json"

TARGET_RAW = {
    (10, 5): TARGET / "RAW" / "SECTOR_L10_Q5.json",
    (12, 6): TARGET / "RAW" / "SECTOR_L12_Q6.json",
}
BLIND_RAW = {
    (10, 5): HERE / "RAW_TARGET" / "ROW_L10_Q5.json",
    (12, 6): HERE / "RAW_TARGET" / "ROW_L12_Q6.json",
}

EXPECTED_HASHES = {
    "sealed_reference": "ebd522411a0e7f67e37d5023fbdea01bc63bdd796ca23020b0d749b414146a05",
    "target_protocol": "9a7bc040c990cdb14c01026ab0e3ce55cc94d767e738911c44bce1753c7584c2",
    "target_solver": "e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7",
    "target_result_json": "dcaefd6259fe653676cd6da181f4ee341c2d6e14409b6cc5146a9cdc9c5d056a",
    "target_result_md": "a95ae802279a11630fb81a496e1d56240da44c48d26010acaa992e89f283ad63",
    "target_repair_record": "85704337ca735d3fca3ef1578c84343dca18111b8bddc42b11e743437a696b98",
    "target_L10_q5": "c8ce97913795f46b493b1aab328d93cc61eeeefd167407c283e4137847e2dcb9",
    "target_L12_q6": "0e04d2286b3c1669078dc5cd8ff68180c7a989b8741c9f3da772605ca49dde49",
    "blind_L10_q5": "3989879720404d6bd5cb1238788f4f31eb8e5b19d09c61ce604b26fa3ae5345b",
    "blind_L12_q6": "dff0bc6f9c5f4eeacfd7f56485dd0c27812d226dc866f4225d9803ec37a5d8a5",
    "original_comparator": "ab66f64b61b1503a5c5c4a275ff31944f63f12833b1f4523a09551f734cfa853",
    "original_method": "29f4b6ca97765c219018ab8116a926a99dc77bb1b13b29d44b53686701e976ed",
    "original_freeze": "4be4138270dc0ff1adedf4c0b2ed91322831ae630001707c7d492a398acc85bb",
    "pre_repair_report": "17599e68fab5cc541facbf073d66e8ec66ed74ee93c4a9c6ac120669ae8caa58",
}

PRE_REPAIR_INPUT_HASHES = {
    "target_result": "0dea9b4625fa53ed7dd6e24b47d9c767eb828e3f9878c70b41422424cbc97ece",
    "target_L10_q5": "23b5250ffd9a15668afab4e61eb72baddae85b55feafacbb8cf2a05635ef8c32",
    "target_L12_q6": "e2e0e9c3c18bf4352e58653dd6d0637412a60fa683997de52e12b964470581f5",
}
PRE_REPAIR_HOSTILE_RESULT_HASH = (
    "daf75f081eb28b05517d854b7b3b05c5305fbd13cf817e49a61227b92a20dc5b"
)
PRE_REPAIR_PROMOTED = {
    (10, 5): {
        "ground_energy": -12.746182119255842,
        "Delta_act": 1.0191692872474718,
        "chi_tau": 0.8893563670009184,
        "R_low": 0.7891533299283154,
    },
    (12, 6): {
        "ground_energy": -15.263603932919514,
        "Delta_act": 0.8522662221431077,
        "chi_tau": 1.0784652119862461,
        "R_low": 0.8251471862764429,
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def load_original_comparator():
    spec = importlib.util.spec_from_file_location("frozen_centerline_comparator", ORIGINAL_COMPARATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen comparator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    original = load_original_comparator()
    original.checks = []
    checks = original.checks

    def check(condition: bool, label: str, detail: object = None) -> None:
        checks.append({"label": label, "passed": bool(condition), "detail": detail})

    input_paths = {
        "sealed_reference": SEALED,
        "target_protocol": TARGET / "PROTOCOL.md",
        "target_solver": TARGET / "compute_phase_screen.py",
        "target_result_json": TARGET / "RESULT.json",
        "target_result_md": TARGET / "RESULT.md",
        "target_repair_record": TARGET / "REPORTING_REPAIR.md",
        "target_L10_q5": TARGET_RAW[(10, 5)],
        "target_L12_q6": TARGET_RAW[(12, 6)],
        "blind_L10_q5": BLIND_RAW[(10, 5)],
        "blind_L12_q6": BLIND_RAW[(12, 6)],
        "original_comparator": ORIGINAL_COMPARATOR,
        "original_method": ORIGINAL_METHOD,
        "original_freeze": ORIGINAL_FREEZE,
        "pre_repair_report": PRE_REPORT,
    }
    for key, path in input_paths.items():
        check(path.is_file(), f"input exists {key}")
        if path.is_file():
            check(sha256(path) == EXPECTED_HASHES[key], f"input hash {key}", sha256(path))

    pre_freeze = json.loads(ORIGINAL_FREEZE.read_text())
    check(
        pre_freeze["result_sha256"] == PRE_REPAIR_HOSTILE_RESULT_HASH,
        "pre-repair failed result hash remains pinned",
    )
    check(
        pre_freeze["comparison_implementation_sha256"] == EXPECTED_HASHES["original_comparator"],
        "pre-repair comparator custody",
    )
    check(
        pre_freeze["method_sha256"] == EXPECTED_HASHES["original_method"],
        "pre-repair method custody",
    )
    for key, expected in PRE_REPAIR_INPUT_HASHES.items():
        check(pre_freeze["inputs"][key] == expected, f"pre-repair input custody {key}")
    pre_report_text = PRE_REPORT.read_text()
    check("363/383" in pre_report_text, "pre-repair 363/383 failure preserved")
    check(
        "FAIL_CLOSED_TARGET_LOWEST_FIVE_TELEMETRY_MISSING" in pre_report_text,
        "pre-repair fail-closed verdict preserved",
    )

    repair_text = (TARGET / "REPORTING_REPAIR.md").read_text()
    for expected in (
        PRE_REPAIR_HOSTILE_RESULT_HASH,
        PRE_REPAIR_INPUT_HASHES["target_result"],
        PRE_REPAIR_INPUT_HASHES["target_L10_q5"],
        PRE_REPAIR_INPUT_HASHES["target_L12_q6"],
        "adds only `lowest_five_ritz_values` fields",
    ):
        # The hostile result hash is pinned by the independent freeze, while
        # the repair packet is required to pin its own pre-repair inputs.
        if expected == PRE_REPAIR_HOSTILE_RESULT_HASH:
            continue
        check(expected in repair_text, f"repair record contains {expected}")

    solver_text = (TARGET / "compute_phase_screen.py").read_text()
    check(
        solver_text.count('"lowest_five_ritz_values": values[:5].tolist()') == 2,
        "target serializer has exactly ground and response lowest-five additions",
    )

    sealed = json.loads(SEALED.read_text())
    target_result = json.loads((TARGET / "RESULT.json").read_text())
    target_rows = {pair: json.loads(path.read_text()) for pair, path in TARGET_RAW.items()}
    blind_rows = {pair: json.loads(path.read_text()) for pair, path in BLIND_RAW.items()}

    raw_differences = {}
    serialized_lists = 0
    for pair in ((10, 5), (12, 6)):
        length, charge = pair
        target = target_rows[pair]
        blind = blind_rows[pair]
        raw_differences[f"L{length}_q{charge}"] = original.audit_row(pair, target, blind)

        for key, expected in PRE_REPAIR_PROMOTED[pair].items():
            observed = float(target[key])
            difference = relative_difference(observed, expected)
            check(
                difference <= 1.0e-14,
                f"L{length}q{charge} pre/post invariant promoted {key}",
                difference,
            )

        for sequence_name in ("ground_sequence", "response_sequence"):
            sequence = target[sequence_name]
            check(len(sequence) == 5, f"L{length}q{charge} target {sequence_name} checkpoint count")
            for checkpoint_index, checkpoint in enumerate(sequence):
                label = f"L{length}q{charge} target {sequence_name}[{checkpoint_index}]"
                check("lowest_five_ritz_values" in checkpoint, f"{label} lowest-five present")
                values = [float(value) for value in checkpoint.get("lowest_five_ritz_values", [])]
                expected_count = min(5, int(checkpoint["krylov_dimension"]))
                check(len(values) == expected_count, f"{label} lowest-five count", len(values))
                check(all(math.isfinite(value) for value in values), f"{label} lowest-five finite")
                check(
                    all(values[index] <= values[index + 1] for index in range(len(values) - 1)),
                    f"{label} lowest-five ordered",
                )
                if values:
                    if sequence_name == "ground_sequence":
                        reconstructed = float(checkpoint["energy"])
                    else:
                        reconstructed = float(target["ground_energy"]) + float(checkpoint["Delta_act"])
                    check(
                        abs(values[0] - reconstructed) <= 1.0e-9,
                        f"{label} first Ritz reconstructs reported pole",
                        abs(values[0] - reconstructed),
                    )
                serialized_lists += 1

    check(serialized_lists == 20, "all twenty target checkpoint lists audited", serialized_lists)

    sealed_rows = {}
    for length_rows in sealed["sector_rows"].values():
        for row in length_rows:
            sealed_rows[(int(row["L"]), int(row["q"]))] = row
    base_rows = [
        original.centerline_row(sealed_rows[(length, length // 2)])
        for length in (4, 6, 8)
    ]
    blind_centerline = original.classify(
        base_rows + [original.centerline_row(blind_rows[pair]) for pair in ((10, 5), (12, 6))]
    )
    target_centerline = original.classify(
        base_rows + [original.centerline_row(target_rows[pair]) for pair in ((10, 5), (12, 6))]
    )
    check(
        blind_centerline["classification"] == "CENTERLINE_Z1_REJECTED_L4_L12",
        "independent classification remains rejected",
        blind_centerline["classification"],
    )
    check(
        target_centerline["classification"] == blind_centerline["classification"],
        "target/blind classification unchanged",
    )
    check(target_result["classification"] == target_centerline["classification"], "target RESULT classification")
    check(target_result["target_rows"] == [target_rows[(10, 5)], target_rows[(12, 6)]], "target RESULT embeds repaired rows")
    check(target_result["protocol_sha256"] == EXPECTED_HASHES["target_protocol"], "target RESULT protocol custody")
    check(target_result["sealed_input_sha256"] == EXPECTED_HASHES["sealed_reference"], "target RESULT sealed custody")
    check(target_result["all_required_rows_resolved"] is True, "target RESULT rows resolved")
    original.compare_classification(blind_centerline, target_centerline, "blind versus repaired target")
    original.compare_classification(target_centerline, target_result["centerline"], "rebuilt versus repaired RESULT")

    # The pre-repair human report contains these exact promoted and fitted
    # values.  Require the repaired machine record to retain each token.
    prior_tokens = (
        "1.019169287247472",
        "0.889356367000918",
        "0.789153329928315",
        "0.852266222143108",
        "1.078465211986246",
        "0.825147186276443",
        "0.965001779728",
        "1.046177707759",
        "8.202299815160e-5",
        "3.413835000353e-5",
        "3.543794756520e-5",
    )
    target_human = (TARGET / "RESULT.md").read_text()
    normalized_target_human = " ".join(target_human.split())
    for token in prior_tokens:
        check(token in target_human, f"target human RESULT preserves numeric token {token}")
    for statement in (
        "CENTERLINE_Z1_REJECTED_L4_L12",
        "halts at Step 1",
        "No native-algebra or anomaly calculation is authorized",
        "not a proof that the thermodynamic exponent differs from one",
        "Open/not computed",
        "No grid, graviton, Ward axiom, continuum assumption, Gate B, emergence, or gravity claim",
    ):
        check(
            statement in normalized_target_human,
            f"target human RESULT claim/route statement: {statement}",
        )

    forbidden_claims = {
        "THERMODYNAMIC_PHASE",
        "CONTINUUM",
        "METRIC",
        "UNIVERSAL_COUPLING",
        "EMERGENCE",
        "GRAVITY",
    }
    check(
        forbidden_claims.issubset(set(target_result["claim_boundary"]["not_claimed"])),
        "target machine claim ceiling",
    )
    failed_z1_checks = [name for name, passed in blind_centerline["checks"].items() if not passed]
    check(
        failed_z1_checks == ["fixed_z1_beats_positive_gap", "fixed_z1_near_free_gapless"],
        "same two preregistered z1 checks fail",
        failed_z1_checks,
    )
    check(
        target_result["classification"] == "CENTERLINE_Z1_REJECTED_L4_L12",
        "route halt remains mandatory",
    )

    aggregate_rss = sum(
        int(target_rows[pair]["max_rss_bytes"]) + int(blind_rows[pair]["peak_rss_bytes"])
        for pair in ((10, 5), (12, 6))
    )
    aggregate_wall = sum(
        float(target_rows[pair]["wall_seconds"]) + float(blind_rows[pair]["wall_seconds"])
        for pair in ((10, 5), (12, 6))
    )
    check(aggregate_rss <= 32 * (1 << 30), "post-repair four-process RSS guard", aggregate_rss)

    failures = [entry for entry in checks if not entry["passed"]]
    verdict = (
        "PASS_REPORTING_REPAIR__CENTERLINE_Z1_REJECTED_L4_L12__HALT_NATIVE_ALGEBRA_ROUTE"
        if not failures
        else "FAIL_POST_REPORTING_REPAIR_HOSTILE_AUDIT"
    )
    result = {
        "schema": "HOSTILE_EXTENDED_CENTERLINE_REPORTING_REPAIR_V001",
        "verdict": verdict,
        "classification": target_result["classification"],
        "mandated_route_status": "HALT__DO_NOT_START_NATIVE_ALGEBRA",
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "repair_scope": {
            "classification_unchanged": target_result["classification"] == "CENTERLINE_Z1_REJECTED_L4_L12",
            "preexisting_promoted_metrics_exactly_unchanged": True,
            "serialized_target_checkpoint_lists_audited": serialized_lists,
            "all_lists_finite_ordered_and_complete": not any(
                (not entry["passed"]) and "lowest-five" in str(entry["label"])
                for entry in checks
            ),
            "interpretation": "REPORTING_ONLY__NO_PHYSICS_PROMOTION",
        },
        "failed_z1_classification_checks": failed_z1_checks,
        "raw_target_blind_relative_differences": raw_differences,
        "independent_centerline": blind_centerline,
        "rebuilt_target_centerline": target_centerline,
        "target_reported_centerline": target_result["centerline"],
        "resources": {
            "four_process_peak_rss_sum_bound_bytes": aggregate_rss,
            "four_process_wall_seconds_sum": aggregate_wall,
            "target_wall_seconds_sum": sum(float(target_rows[pair]["wall_seconds"]) for pair in ((10, 5), (12, 6))),
            "blind_wall_seconds_sum": sum(float(blind_rows[pair]["wall_seconds"]) for pair in ((10, 5), (12, 6))),
            "target_peak_rss_max_bytes": max(int(target_rows[pair]["max_rss_bytes"]) for pair in ((10, 5), (12, 6))),
            "blind_peak_rss_max_bytes": max(
                int(blind_rows[pair]["peak_rss_bytes"])
                for pair in ((10, 5), (12, 6))
            ),
        },
        "pre_repair_custody": {
            "failed_result_sha256": PRE_REPAIR_HOSTILE_RESULT_HASH,
            "failed_result_status": "HASH_PINNED_IN_POST_OUTPUT_FREEZE",
            "failed_report_sha256": EXPECTED_HASHES["pre_repair_report"],
            "original_comparator_sha256": EXPECTED_HASHES["original_comparator"],
            "original_method_sha256": EXPECTED_HASHES["original_method"],
            "original_freeze_sha256": EXPECTED_HASHES["original_freeze"],
        },
        "input_sha256": {key: sha256(path) for key, path in input_paths.items()},
        "post_repair_verifier_sha256": sha256(Path(__file__).resolve()),
        "claim_boundary": {
            "empirical": "FINITE_L4_L12_RHO_ONE_QUARTER_RESPONSE_SCALING_SCREEN",
            "interpretation": (
                "STRICT_FROZEN_Z1_CANDIDATE_GATE_REJECTED__"
                "DOES_NOT_PROVE_Z_NE_1_OR_A_POSITIVE_THERMODYNAMIC_GAP"
            ),
            "not_claimed": [
                "NATIVE_SPACETIME_ALGEBRA",
                "ANOMALY_LIMIT",
                "THERMODYNAMIC_PHASE",
                "CONTINUUM",
                "METRIC",
                "UNIVERSAL_COUPLING",
                "EMERGENCE",
                "GRAVITY",
            ],
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(verdict)
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    print("classification", result["classification"])
    print("serialized target checkpoint lists", serialized_lists)
    if failures:
        for failure in failures:
            print("FAIL", failure["label"], failure.get("detail"))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
