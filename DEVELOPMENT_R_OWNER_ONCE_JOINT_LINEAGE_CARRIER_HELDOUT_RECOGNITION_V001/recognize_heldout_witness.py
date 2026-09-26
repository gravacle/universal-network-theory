#!/usr/bin/env python3
"""Independent, non-destructive recognition of the completed L10/L12 run.

This module reads only the two immutable atomic result JSON files and the
post-run timing observation in this packet.  It authenticates the result
bytes, recomputes the frozen numerical diagnostics, and keeps three questions
separate:

1. whether the deterministic target and hostile computations agree;
2. whether the original strict protocol is formally claimed as passed; and
3. whether the later signed no-decline persistence prediction passed.

It does not edit or reinterpret any frozen or sealed historical artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping


SCHEMA = "OWNER_ONCE_HELDOUT_L10_L12_RECOGNITION_V001"
TIMING_SCHEMA = "OWNER_ONCE_HELDOUT_L10_L12_TIMING_OBSERVATION_V001"
PACKET = Path(__file__).resolve().parent
DEFAULT_ROOT = PACKET.parent
DEFAULT_RESULT = PACKET / "RECOGNITION_RESULT_V001.json"

TARGET_PATH = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_HELDOUT_TARGET_V001/"
    "PHYSICAL_OUTPUTS/TARGET_HELDOUT_WITNESS_RESULT_V001.json"
)
HOSTILE_PATH = (
    "AUDIT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_HELDOUT_V001/"
    "PHYSICAL_OUTPUTS/HOSTILE_HELDOUT_WITNESS_RESULT_V001.json"
)
PROTOCOL_PATH = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_HELDOUT_EXECUTION_V001/"
    "PROTOCOL.md"
)
PERSISTENCE_FREEZE_PATH = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_PERSISTENCE_FREEZE_V001/"
    "BLINDED_SECONDARY_ANALYSIS_FREEZE.md"
)
PERSISTENCE_ADDENDUM_PATH = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_PERSISTENCE_FREEZE_V001/"
    "PRE_UNBLINDING_INTERPRETATION_AND_SCALE_ADDENDUM.md"
)
SEED_RESULT_PATH = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_RECONCILIATION_V001/"
    "FINAL_DISPOSITION_V001.json"
)
TIMING_PATH = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_HELDOUT_RECOGNITION_V001/"
    "CUSTODY_TIMING_OBSERVATION_V001.json"
)
TIMING_OBSERVATION_SHA256 = (
    "b0c95e975fda7b0110dddca7b48a030f80eb29faeab9bb83189db765296149f2"
)

PINNED_INPUT_HASHES = {
    TARGET_PATH: "804b3dda5ebed693ceee26afdedc754602b02a3e8eb7482539f64016d2b54b4b",
    HOSTILE_PATH: "7e1d1c68dfc50fade4acbe3d39ef04b22394872832ce0475847a1098cfc045f9",
    PROTOCOL_PATH: "8250e17405067deabbfe7dc4ff00864d26bef66cabfeef628f9f6df63829d9a7",
    PERSISTENCE_FREEZE_PATH: "2e6134297e959b35df1dcd9d28b314c12996ccf5762634738318f023382a7943",
    PERSISTENCE_ADDENDUM_PATH: "a5cdda7bd6988a57cc5cdbe31c7099c37f32dddbcfcd4ac834942e37f65871de",
    SEED_RESULT_PATH: "2ce9852ef40d16d50b7a6553d0173e041c9cfdcc59925819f900f21f8a684f14",
}

LENGTHS = (10, 12)
AGREEMENT_TOLERANCE = 1.0e-8
PERSISTENCE_FLOOR = 0.001963064475535806
MAXIMUM_RELEASE_SKEW_SECONDS = 60


class RecognitionError(RuntimeError):
    """Input authentication, schema, or recomputation failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RecognitionError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _verify_finite(value: Any, label: str) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            _verify_finite(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _verify_finite(child, f"{label}[{index}]")
    elif isinstance(value, float):
        require(math.isfinite(value), f"nonfinite value at {label}")


def strict_json(path: Path) -> Any:
    def reject_constant(value: str) -> None:
        raise RecognitionError(f"nonstandard constant {value!r} in {path}")

    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle, parse_constant=reject_constant)
    except (OSError, json.JSONDecodeError) as error:
        raise RecognitionError(f"cannot read strict JSON {path}: {error}") from error
    _verify_finite(value, path.name)
    return value


def number(value: Any, label: str) -> float:
    require(
        isinstance(value, (int, float)) and not isinstance(value, bool),
        f"non-numeric {label}",
    )
    result = float(value)
    require(math.isfinite(result), f"nonfinite {label}")
    return result


def authenticate_inputs(root: Path) -> dict[str, dict[str, Any]]:
    authenticated: dict[str, dict[str, Any]] = {}
    for relative, expected in sorted(PINNED_INPUT_HASHES.items()):
        path = root / relative
        require(path.is_file(), f"missing pinned input {relative}")
        actual = sha256_file(path)
        require(actual == expected, f"hash mismatch for {relative}")
        authenticated[relative] = {
            "bytes": path.stat().st_size,
            "sha256": actual,
        }
    return authenticated


def _target_terminal(target: Mapping[str, Any], length: int, resolution: str) -> Mapping[str, Any]:
    row = target["lengths"][str(length)]
    return row["coarse"]["terminal"] if resolution == "coarse" else row["fine"]


def _hostile_row(hostile: Mapping[str, Any], length: int) -> Mapping[str, Any]:
    rows = [row for row in hostile["results"] if row.get("L") == length]
    require(len(rows) == 1, f"hostile L{length} row count is not one")
    return rows[0]


def _target_resolution_disagreement(
    coarse: Mapping[str, Any], fine: Mapping[str, Any]
) -> tuple[float, str]:
    values: list[tuple[float, str]] = []
    for key in ("probability", "w", "w_sham", "D", "w_shuffle"):
        values.append(
            (
                abs(number(coarse["registered"][key], key) - number(fine["registered"][key], key)),
                f"registered.{key}",
            )
        )
    require(set(coarse["q_contributions"]) == set(fine["q_contributions"]), "target q sets differ")
    for q in sorted(coarse["q_contributions"], key=int):
        for key in ("p_q", "w_q", "w_sham_q", "D_q", "w_shuffle_q"):
            values.append(
                (
                    abs(
                        number(coarse["q_contributions"][q][key], f"coarse q{q} {key}")
                        - number(fine["q_contributions"][q][key], f"fine q{q} {key}")
                    ),
                    f"q_{q}.{key}",
                )
            )
    return max(values, default=(0.0, "none"))


def _cross_disagreement(
    target_fine: Mapping[str, Any], hostile_fine: Mapping[str, Any], length: int
) -> tuple[float, str, dict[str, dict[str, float]]]:
    comparisons: dict[str, dict[str, float]] = {}

    def add(label: str, left: Any, right: Any) -> None:
        target_value = number(left, f"target {label}")
        hostile_value = number(right, f"hostile {label}")
        comparisons[label] = {
            "absolute_disagreement": abs(target_value - hostile_value),
            "hostile": hostile_value,
            "target": target_value,
        }

    registered = target_fine["registered"]
    add("w_L", registered["w"], hostile_fine["w_L"])
    add("w_L_sham", registered["w_sham"], hostile_fine["w_L_sham"])
    add("D_L", registered["D"], hostile_fine["D_L"])
    hostile_sectors = {int(row["q"]): row for row in hostile_fine["sectors"]}
    require(set(hostile_sectors) == set(range(length + 1)), f"hostile L{length} q set mismatch")
    for q in range(length + 1):
        contribution = target_fine["q_contributions"][str(q)]
        add(f"q_{q}_D", contribution["D_q"], hostile_sectors[q]["witness"])
        add(f"q_{q}_p", contribution["p_q"], hostile_sectors[q]["sector_weight"])
    label, row = max(
        comparisons.items(), key=lambda item: item[1]["absolute_disagreement"]
    )
    return row["absolute_disagreement"], label, comparisons


def _target_residual(coarse: Mapping[str, Any], fine: Mapping[str, Any]) -> float:
    keys = (
        "state_norm",
        "probability_normalization",
        "marginal_reconstruction",
        "sharp_sector_QS_minus_QC",
        "total_content",
    )
    return max(
        abs(number(record["residuals"][key], f"target {key}"))
        for record in (coarse, fine)
        for key in keys
    )


def _hostile_diagnostics(record: Mapping[str, Any]) -> Iterable[float]:
    for key in (
        "marginal_reconstruction_residual",
        "normalization_residual",
        "q_identity_residual",
        "row_column_disagreement",
        "total_content_residual",
    ):
        yield abs(number(record[key], f"hostile {key}"))
    for key in (
        "analytic_shuffle_expectation",
        "sham_self_covariance_residual",
        "maximum_shuffle_identity_residual",
        "sham_negative_control_D",
    ):
        yield abs(number(record["controls"][key], f"hostile controls {key}"))


def _hostile_residual(row: Mapping[str, Any]) -> float:
    regeneration = row["rough_regeneration"]
    values = list(_hostile_diagnostics(row["coarse"]))
    values.extend(_hostile_diagnostics(row["fine"]))
    values.extend(
        (
            abs(number(regeneration["maximum_norm_error"], "hostile regeneration norm")),
            abs(
                number(
                    regeneration["maximum_blocked_null_state_error"],
                    "hostile blocked-null error",
                )
            ),
        )
    )
    return max(values, default=0.0)


def _row_column_disagreement(
    target_coarse: Mapping[str, Any],
    target_fine: Mapping[str, Any],
    hostile_row: Mapping[str, Any],
) -> float:
    return max(
        abs(number(target_coarse["residuals"]["row_column_accumulator"], "target coarse row/column")),
        abs(number(target_fine["residuals"]["row_column_accumulator"], "target fine row/column")),
        abs(number(hostile_row["coarse"]["row_column_disagreement"], "hostile coarse row/column")),
        abs(number(hostile_row["fine"]["row_column_disagreement"], "hostile fine row/column")),
    )


def _capacity(target_fine: Mapping[str, Any], length: int) -> float:
    return sum(
        number(row["p_q"], f"L{length} q{q} p")
        * (int(q) / length)
        * (1.0 - int(q) / length)
        for q, row in target_fine["q_contributions"].items()
    )


def _verify_branch_headers(target: Mapping[str, Any], hostile: Mapping[str, Any]) -> None:
    require(target.get("schema") == "OWNER_ONCE_HELDOUT_TARGET_JOINT_WITNESS_RAW_V001", "wrong target schema")
    require(target.get("status") == "SEALED_TARGET_L10_L12_RAW_COMPLETE", "target is not atomically complete")
    require(target.get("all_target_internal_numerical_and_control_conditions_passed") is True, "target controls failed")
    require(hostile.get("schema") == "OWNER_ONCE_HELDOUT_HOSTILE_JOINT_WITNESS_RAW_V001", "wrong hostile schema")
    require(hostile.get("disposition") == "HOSTILE_HELDOUT_L10_L12_COMPLETE__RECONCILIATION_REQUIRED", "hostile is not atomically complete")
    independence = hostile.get("independence", {})
    require(
        all(independence.get(key) is False for key in (
            "target_arrays_read", "target_code_imported", "target_matrices_read", "target_result_values_read"
        )),
        "hostile independence declaration failed",
    )


def recognize(root: Path = DEFAULT_ROOT) -> dict[str, Any]:
    root = root.resolve()
    authenticated = authenticate_inputs(root)
    target = strict_json(root / TARGET_PATH)
    hostile = strict_json(root / HOSTILE_PATH)
    timing_path = root / TIMING_PATH
    require(
        sha256_file(timing_path) == TIMING_OBSERVATION_SHA256,
        "timing observation hash mismatch",
    )
    timing = strict_json(timing_path)
    require(isinstance(target, Mapping) and isinstance(hostile, Mapping), "atomic result is not an object")
    require(isinstance(timing, Mapping) and timing.get("schema") == TIMING_SCHEMA, "wrong timing observation")
    _verify_branch_headers(target, hostile)

    release_gap = int(timing["release_observation"]["observed_gap_seconds"])
    maximum_gap = int(timing["release_observation"]["frozen_maximum_seconds"])
    require(release_gap == 10_748 and maximum_gap == MAXIMUM_RELEASE_SKEW_SECONDS, "unexpected timing observation")
    chronology = timing["chronology"]
    target_launch = int(chronology["target_scratch_birth_epoch_seconds"])
    hostile_launch = int(chronology["hostile_scratch_birth_epoch_seconds"])
    hostile_output = int(chronology["hostile_atomic_output_birth_epoch_seconds"])
    target_output = int(chronology["target_atomic_output_birth_epoch_seconds"])
    require(hostile_launch - target_launch == release_gap, "timing gap arithmetic mismatch")
    require(target_launch < hostile_launch < hostile_output < target_output, "chronology order mismatch")

    sizes: list[dict[str, Any]] = []
    all_controls = True
    for length in LENGTHS:
        target_coarse = _target_terminal(target, length, "coarse")
        target_fine = _target_terminal(target, length, "fine")
        hostile_row = _hostile_row(hostile, length)
        hostile_fine = hostile_row["fine"]
        target_resolution, target_resolution_field = _target_resolution_disagreement(
            target_coarse, target_fine
        )
        cross, cross_field, _comparisons = _cross_disagreement(
            target_fine, hostile_fine, length
        )
        row_column = _row_column_disagreement(
            target_coarse, target_fine, hostile_row
        )
        d_value = max(target_resolution, cross, row_column)
        target_r = _target_residual(target_coarse, target_fine)
        hostile_r = _hostile_residual(hostile_row)
        r_value = max(target_r, hostile_r)
        tau = max(1.0e-9, 50.0 * d_value, 100.0 * r_value)
        target_d = number(target_fine["registered"]["D"], f"target L{length} D")
        hostile_d = number(hostile_fine["D_L"], f"hostile L{length} D")
        statistic = abs(target_d) / tau
        lower = min(target_d, hostile_d) - tau
        capacity = _capacity(target_fine, length)
        size_controls = {
            "hostile_internal_conditions_pass": hostile_row["internal_conditions_pass"] is True,
            "row_column_agreement_within_1e_8": row_column <= AGREEMENT_TOLERANCE,
            "target_hostile_agreement_within_1e_8": cross <= AGREEMENT_TOLERANCE,
            "target_internal_conditions_pass": target["lengths"][str(length)]["target_internal_numerics"]["all_target_internal_conditions_passed"] is True,
        }
        all_controls = all_controls and all(size_controls.values())
        sizes.append(
            {
                "B_L": capacity,
                "D_L_hostile": hostile_d,
                "D_L_target": target_d,
                "D_lower_signed": lower,
                "T_L": statistic,
                "absolute_target_hostile_D_disagreement": abs(target_d - hostile_d),
                "conditions": size_controls,
                "d_L": d_value,
                "d_components": {
                    "row_column": row_column,
                    "target_coarse_fine": target_resolution,
                    "target_coarse_fine_largest_field": target_resolution_field,
                    "target_vs_hostile": cross,
                    "target_vs_hostile_largest_field": cross_field,
                },
                "eta_L_target": target_d / capacity,
                "length": length,
                "magnitude_fraction_of_D8": abs(target_d) / PERSISTENCE_FLOOR,
                "persistence_floor": PERSISTENCE_FLOOR,
                "persistence_pass": lower >= PERSISTENCE_FLOOR,
                "r_L": r_value,
                "r_components": {"hostile": hostile_r, "target": target_r},
                "sign_relative_to_positive_D8": "REVERSED_NEGATIVE",
                "tau_L": tau,
                "w_L_target": number(target_fine["registered"]["w"], f"target L{length} w"),
                "w_L_sham_target": number(target_fine["registered"]["w_sham"], f"target L{length} sham"),
            }
        )

    primary_statistic = min(row["T_L"] for row in sizes)
    numerical_reproduction = all_controls and primary_statistic > 1.0
    persistence_pass = all(row["persistence_pass"] for row in sizes)
    require(numerical_reproduction, "completed outputs do not reproduce a resolved two-sided witness")
    require(not persistence_pass, "unexpected signed persistence pass")

    return {
        "authenticated_inputs": authenticated,
        "claim_boundary": (
            "FINITE_EXACT_L10_L12_OWNER_ONCE_JOINT_LINEAGE_CARRIER_ASSOCIATION_ONLY__"
            "NO_FORMAL_STRICT_PROTOCOL_PASS_CLAIM__NO_ALL_L_THERMODYNAMIC_GATE_RGRL_ALPHA_"
            "GEOMETRY_CONTINUUM_OR_GRAVITY_PROMOTION"
        ),
        "computational_evidence": {
            "deterministic_numerical_validity_affected_by_timing_gap": False,
            "independent_source_isolation_preserved": True,
            "recognized": numerical_reproduction,
            "status": "VALID_INDEPENDENTLY_REPRODUCED_FINITE_L10_L12_ASSOCIATION",
            "target_was_deterministic_and_running_before_hostile_launch": True,
            "two_sided_T_10_12": primary_statistic,
        },
        "policy_adjudication": {
            "future_rule": (
                "GATE_ON_VALUE_ACCESS_AND_IMPLEMENTATION_INDEPENDENCE;_BIND_LAUNCH_RECEIPTS;"
                "TREAT_WALL_CLOCK_SKEW_AS_METADATA_UNLESS_A_SCIENTIFIC_RATIONALE_IS_FROZEN"
            ),
            "release_skew_rule_role": "ANTI_CONTAMINATION_AND_BLINDING_SAFEGUARD__OPERATIONAL_NOT_SCIENTIFIC",
            "reason_timing_does_not_bias_this_result": (
                "BOTH_BRANCHES_WERE_SOURCE_ISOLATED;NEITHER_FINAL_VALUE_EXISTED_AT_EITHER_LAUNCH;"
                "TARGET_WAS_ALREADY_RUNNING_BEFORE_HOSTILE_LAUNCH;ATOMIC_FINAL_OUTPUTS;"
                "INDEPENDENT_NUMERICAL_AGREEMENT"
            ),
        },
        "schema": SCHEMA,
        "secondary_signed_persistence": {
            "D8_floor": PERSISTENCE_FLOOR,
            "pass": persistence_pass,
            "status": "FAIL__SIGN_REVERSAL_AND_MAGNITUDE_DECLINE_AT_L10_AND_L12",
        },
        "sizes": sizes,
        "strict_protocol": {
            "formal_pass_claimed": False,
            "release_skew_deviation_disclosed": True,
            "status": "NOT_CLAIMED_AS_FORMALLY_PASSED__RELEASE_SKEW_DEVIATION",
        },
        "timing_custody": timing,
    }


def canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def validate_expected(root: Path = DEFAULT_ROOT, expected: Path = DEFAULT_RESULT) -> dict[str, Any]:
    computed = recognize(root)
    recorded = strict_json(expected)
    require(recorded == computed, "recorded recognition result differs from recomputation")
    require(expected.read_bytes() == canonical_bytes(recorded), "recognition result is not canonical JSON")
    return computed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--expected", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--print", action="store_true", dest="print_result")
    args = parser.parse_args()
    result = validate_expected(args.root, args.expected)
    if args.print_result:
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    else:
        print("PASS: recognition result authenticates and recomputes exactly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
