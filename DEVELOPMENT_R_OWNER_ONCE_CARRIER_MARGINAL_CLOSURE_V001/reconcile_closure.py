#!/usr/bin/env python3
"""Fail-closed reconciliation of the target and hostile CMC-1 packets."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "CARRIER_MARGINAL_CLOSURE_DISPOSITION_V001.json"

PASS = "PASS_EXACT_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE__FINITE_ACCUMULATION_SCOPE_ONLY"
FAIL = "OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_REJECTED_OR_UNRESOLVED"
TOLERANCE = 2.0e-10

ARTIFACTS = {
    "theorem": (
        HERE / "THEOREM.md",
        "2850e32eae9c84a194047877219de681995850e5c4c86c24690654d202524584",
    ),
    "protocol": (
        HERE / "PROTOCOL.md",
        "81010287548dc44ddfa291765727a6a5bca001570d6a93accd78ff0dd151c76d",
    ),
    "historical_target": (
        ROOT
        / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
        / "compute_seed_history.py",
        "24ea3626fda443dd4ae5076c7766e1aaca77ff5ce9f22c05bae96943fc627d55",
    ),
    "target_source": (
        ROOT / "DEVELOPMENT_R_LINEAGE_CARRIER_REDUCTION_V001" / "verify_carrier_reduction.py",
        "22bee481680f921a8a36ff0ad6bd620a9db1897ad5de6b33f0553eb60ad3fcf6",
    ),
    "target_tests": (
        ROOT / "DEVELOPMENT_R_LINEAGE_CARRIER_REDUCTION_V001" / "test_carrier_reduction.py",
        "f5ee9c8c1339056a446b2c02728702e560aa9d3ef968a498063eb4fb536e7ece",
    ),
    "target_primary_result": (
        ROOT
        / "DEVELOPMENT_R_LINEAGE_CARRIER_REDUCTION_V001"
        / "CARRIER_REDUCTION_RESULT_V001.json",
        "b2892fd12b938838499502c2fcc3635068127e3ee8f673bc36b06b53086d1612",
    ),
    "target_l8_result": (
        ROOT
        / "DEVELOPMENT_R_LINEAGE_CARRIER_REDUCTION_V001"
        / "CARRIER_REDUCTION_L8_RESULT_V001.json",
        "5c3cc403cf7aa493893636e6d682394a51ec9b43caa135adb72fb835ff2fb12c",
    ),
    "hostile_source": (
        ROOT
        / "AUDIT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001"
        / "hostile_carrier_closure.py",
        "cd01ea7d09a913aa5101e2dc6f40b9bd6c306e9018cff992c6a1e92956517456",
    ),
    "hostile_tests": (
        ROOT
        / "AUDIT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001"
        / "test_hostile_carrier_closure.py",
        "fd03d59bc83acb6874382364ab89b3368d5eb1e7b61b35c056fc6ec8a2438f3f",
    ),
    "hostile_result": (
        ROOT
        / "AUDIT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001"
        / "HOSTILE_RESULT.json",
        "80eb6830337514192e732c400f97fc74b07b2b973db01d0e74305ae632e50b35",
    ),
    "hostile_narrative": (
        ROOT
        / "AUDIT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001"
        / "INDEPENDENT_HOSTILE_AUDIT.md",
        "5e1514152538695e6be2e26954ca240000eaa8ce31108a7ab5abb53c4225a920",
    ),
}


class ReconciliationFailure(RuntimeError):
    """A frozen reconciliation predicate failed."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReconciliationFailure(message)


def require_finite_tree(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            require_finite_tree(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            require_finite_tree(item, f"{path}[{index}]")
    elif isinstance(value, float):
        require(math.isfinite(value), f"nonfinite value at {path}")


def authenticate_artifacts() -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    for label, (path, expected) in ARTIFACTS.items():
        require(path.is_file(), f"missing artifact: {label}")
        actual = sha256_file(path)
        require(actual == expected, f"SHA-256 mismatch for {label}: {actual}")
        records[label] = {
            "path": str(path.relative_to(ROOT)),
            "sha256": actual,
        }
    return records


def load_json(label: str) -> dict[str, Any]:
    path = ARTIFACTS[label][0]
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{label} is not a JSON object")
    require_finite_tree(value, label)
    return value


def validate_parameters(parameters: dict[str, Any], hostile: bool = False) -> None:
    require(parameters["lengths"] == [4, 6], "mandatory lengths are not exactly L4/L6")
    require(parameters["phi"] == math.pi / 4.0, "phi mismatch")
    require(parameters["dwell"] == math.pi / 2.0, "dwell mismatch")
    require(parameters["taylor_order"] == 12, "Taylor order mismatch")
    step_key = "transport_substeps" if hostile else "transport_steps"
    require(parameters[step_key] == 16, "transport substep mismatch")
    require(parameters["equivalence_tolerance"] == TOLERANCE, "equivalence tolerance mismatch")
    control_key = "control_tolerance" if hostile else "numerical_control_tolerance"
    require(parameters[control_key] == TOLERANCE, "control tolerance mismatch")


def validate_target(target: dict[str, Any]) -> dict[str, float]:
    require(target["schema"] == "LINEAGE_CARRIER_REDUCTION_VERIFIER_V001", "target schema mismatch")
    require(target["classification"] == "CARRIER_REDUCTION_VERIFIED_FINITE", "target classification mismatch")
    require(target["passed"] is True, "target did not pass")
    require(target["primary_protocol_passed"] is True, "target primary protocol did not pass")
    require(target["supplemental_l8_passed"] is False, "primary target is mislabeled supplemental")
    require(target["mandatory_protocol_lengths"] == [4, 6], "target mandatory lengths mismatch")
    validate_parameters(target["parameters"])
    rows = target["rows"]
    require([row["L"] for row in rows] == [4, 6], "target rows are not exactly L4/L6")
    for row in rows:
        require(row["passed"] is True, f"target L{row['L']} failed")
        require(len(row["events"]) == row["L"], f"target L{row['L']} event coverage mismatch")
        require(row["maximum_equivalence_disagreement"] <= TOLERANCE, f"target L{row['L']} equivalence failure")
        require(row["maximum_numerical_control_error"] <= TOLERANCE, f"target L{row['L']} control failure")
    deps = target["dependencies"]
    require(deps["verifier_sha256"] == ARTIFACTS["target_source"][1], "target source binding mismatch")
    require(deps["historical_target"]["sha256"] == ARTIFACTS["historical_target"][1], "historical target binding mismatch")
    require(deps["frozen_documents"]["theorem"]["sha256"] == ARTIFACTS["theorem"][1], "target theorem binding mismatch")
    require(deps["frozen_documents"]["protocol"]["sha256"] == ARTIFACTS["protocol"][1], "target protocol binding mismatch")
    return {
        f"L{row['L']}_equivalence": row["maximum_equivalence_disagreement"]
        for row in rows
    } | {
        f"L{row['L']}_control": row["maximum_numerical_control_error"]
        for row in rows
    }


def validate_supplemental_l8(result: dict[str, Any]) -> dict[str, float]:
    require(result["classification"] == "SUPPLEMENTAL_L8_CARRIER_REDUCTION_VERIFIED_FINITE", "L8 classification mismatch")
    require(result["passed"] is True, "supplemental L8 did not pass")
    require(result["primary_protocol_passed"] is False, "L8 improperly marked as primary")
    require(result["supplemental_l8_passed"] is True, "L8 supplemental flag missing")
    require(result["parameters"]["lengths"] == [8], "supplemental result is not exactly L8")
    require([row["L"] for row in result["rows"]] == [8], "supplemental rows are not exactly L8")
    row = result["rows"][0]
    require(row["L"] == 8 and row["passed"] is True, "supplemental L8 row failed")
    require(len(row["events"]) == 8, "supplemental L8 event coverage mismatch")
    require(row["maximum_equivalence_disagreement"] <= TOLERANCE, "supplemental L8 equivalence failure")
    require(row["maximum_numerical_control_error"] <= TOLERANCE, "supplemental L8 control failure")
    deps = result["dependencies"]
    require(deps["verifier_sha256"] == ARTIFACTS["target_source"][1], "supplemental source binding mismatch")
    require(deps["historical_target"]["sha256"] == ARTIFACTS["historical_target"][1], "supplemental historical target binding mismatch")
    require(deps["frozen_documents"]["theorem"]["sha256"] == ARTIFACTS["theorem"][1], "supplemental theorem binding mismatch")
    require(deps["frozen_documents"]["protocol"]["sha256"] == ARTIFACTS["protocol"][1], "supplemental protocol binding mismatch")
    return {
        "L8_equivalence": row["maximum_equivalence_disagreement"],
        "L8_control": row["maximum_numerical_control_error"],
    }


def validate_hostile(hostile: dict[str, Any]) -> dict[str, float]:
    require(hostile["schema"] == "HOSTILE_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001", "hostile schema mismatch")
    require(hostile["disposition"] == PASS, "hostile disposition mismatch")
    require(
        hostile["independence"]
        == {
            "historical_matrix_imports": False,
            "target_matrix_imports": False,
            "target_result_values_read": False,
            "target_verifier_imports": False,
        },
        "hostile independence declaration failed",
    )
    validate_parameters(hostile["parameters"], hostile=True)
    rows = hostile["results"]
    require([row["length"] for row in rows] == [4, 6], "hostile rows are not exactly L4/L6")
    for row in rows:
        length = row["length"]
        require(row["passed"] is True, f"hostile L{length} failed")
        require(len(row["events"]) == length, f"hostile L{length} event coverage mismatch")
        require(row["maximum_full_reduced_disagreement"] <= TOLERANCE, f"hostile L{length} equivalence failure")
        require(row["maximum_absolute_norm_control_error"] <= TOLERANCE, f"hostile L{length} control failure")
        require(row["maximum_fresh_lineage_probability"] <= TOLERANCE, f"hostile L{length} freshness failure")
    deps = hostile["dependencies"]
    require(deps["hostile_source"]["sha256"] == ARTIFACTS["hostile_source"][1], "hostile source binding mismatch")
    require(deps["candidate_theorem"]["sha256"] == ARTIFACTS["theorem"][1], "hostile theorem binding mismatch")
    require(deps["candidate_protocol"]["sha256"] == ARTIFACTS["protocol"][1], "hostile protocol binding mismatch")
    return {
        f"L{row['length']}_equivalence": row["maximum_full_reduced_disagreement"]
        for row in rows
    } | {
        f"L{row['length']}_control": row["maximum_absolute_norm_control_error"]
        for row in rows
    }


def build_disposition() -> dict[str, Any]:
    authenticated = authenticate_artifacts()
    target = load_json("target_primary_result")
    l8 = load_json("target_l8_result")
    hostile = load_json("hostile_result")
    return {
        "schema": "OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_RECONCILIATION_V001",
        "disposition": PASS,
        "artifacts": authenticated,
        "frozen_thresholds": {
            "maximum_full_reduced_disagreement": TOLERANCE,
            "maximum_absolute_norm_control_error": TOLERANCE,
            "maximum_fresh_lineage_probability": TOLERANCE,
        },
        "target_primary_maxima": validate_target(target),
        "target_supplemental_maxima": validate_supplemental_l8(l8),
        "hostile_maxima": validate_hostile(hostile),
        "logical_basis": {
            "analytic_theorem_sha256": ARTIFACTS["theorem"][1],
            "finite_target": "mandatory L4/L6 plus supplemental L8",
            "finite_hostile": "independent mandatory L4/L6",
        },
        "scope": (
            "exact unconditional carrier marginal for the frozen finite owner-once "
            "accumulation pass while lineage outcomes remain unread"
        ),
        "excluded": [
            "lineage postselection or lineage-conditioned observables",
            "a revisit or lineage-dependent schedule",
            "a future record-reading Hamiltonian or measurement",
            "Gate or Record--Geometry Realization Law conclusions",
            "alpha, continuum, thermodynamic-limit, or gravity conclusions",
        ],
    }


def main() -> int:
    try:
        result = build_disposition()
    except (KeyError, IndexError, TypeError, ValueError, OSError, ReconciliationFailure) as error:
        failure = {
            "schema": "OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_RECONCILIATION_V001",
            "disposition": FAIL,
            "reason": str(error),
        }
        rendered = json.dumps(failure, indent=2, sort_keys=True, allow_nan=False) + "\n"
        OUTPUT.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 1
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(result["disposition"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
