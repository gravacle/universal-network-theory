#!/usr/bin/env python3
"""Independent post-output centerline comparison and frozen z=1 classification."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
METHOD = HERE / "POST_OUTPUT_METHOD.md"
SEALED = ROOT / "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001" / "RESULT.json"
TARGET_DIR = ROOT / "DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001"
TARGET_PROTOCOL = TARGET_DIR / "PROTOCOL.md"
TARGET_RESULT = TARGET_DIR / "RESULT.json"
TARGET_RAW = {
    (10, 5): TARGET_DIR / "RAW" / "SECTOR_L10_Q5.json",
    (12, 6): TARGET_DIR / "RAW" / "SECTOR_L12_Q6.json",
}
BLIND_RAW = {
    (10, 5): HERE / "RAW_TARGET" / "ROW_L10_Q5.json",
    (12, 6): HERE / "RAW_TARGET" / "ROW_L12_Q6.json",
}
OUT = HERE / "HOSTILE_RESULT.json"

EXPECTED_HASHES = {
    "sealed_reference": "ebd522411a0e7f67e37d5023fbdea01bc63bdd796ca23020b0d749b414146a05",
    "target_protocol": "9a7bc040c990cdb14c01026ab0e3ce55cc94d767e738911c44bce1753c7584c2",
    "target_result": "0dea9b4625fa53ed7dd6e24b47d9c767eb828e3f9878c70b41422424cbc97ece",
    "target_L10_q5": "23b5250ffd9a15668afab4e61eb72baddae85b55feafacbb8cf2a05635ef8c32",
    "target_L12_q6": "e2e0e9c3c18bf4352e58653dd6d0637412a60fa683997de52e12b964470581f5",
    "blind_L10_q5": "3989879720404d6bd5cb1238788f4f31eb8e5b19d09c61ce604b26fa3ae5345b",
    "blind_L12_q6": "dff0bc6f9c5f4eeacfd7f56485dd0c27812d226dc866f4225d9803ec37a5d8a5",
}

LENGTHS = (4, 6, 8, 10, 12)
PAIRS = ((10, 5), (12, 6))
EXPONENT_GRID = tuple(0.25 + index * (3.75 / 15000.0) for index in range(15001))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


checks: list[dict[str, object]] = []


def check(condition: bool, label: str, detail: object = None) -> None:
    checks.append({"label": label, "passed": bool(condition), "detail": detail})


def solve_two_features(
    first: list[float], second: list[float], values: list[float]
) -> tuple[float, float] | None:
    aa = sum(value * value for value in first)
    ab = sum(left * right for left, right in zip(first, second))
    bb = sum(value * value for value in second)
    ay = sum(feature * value for feature, value in zip(first, values))
    by = sum(feature * value for feature, value in zip(second, values))
    determinant = aa * bb - ab * ab
    if determinant == 0.0:
        return None
    return (
        (ay * bb - by * ab) / determinant,
        (by * aa - ay * ab) / determinant,
    )


def fit_fixed_z1(lengths: list[float], values: list[float]) -> dict[str, object]:
    first = [1.0 / length for length in lengths]
    second = [1.0 / length**2 for length in lengths]
    solution = solve_two_features(first, second, values)
    if solution is None:
        return {"fit_status": "NO_ADMISSIBLE_PARAMETERS"}
    amplitude, correction = solution
    prediction = [
        amplitude / length + correction / length**2 for length in lengths
    ]
    if amplitude <= 0.0 or any(value <= 0.0 for value in prediction):
        return {"fit_status": "NO_ADMISSIBLE_PARAMETERS"}
    return {
        "fit_status": "RESOLVED",
        "amplitude": amplitude,
        "correction": correction,
        "training_sse": sum(
            (predicted - observed) ** 2
            for predicted, observed in zip(prediction, values)
        ),
    }


def fit_gap_family(
    lengths: list[float], values: list[float], positive_gap: bool
) -> dict[str, object]:
    best: tuple[float, float, float, float] | None = None
    for exponent in EXPONENT_GRID:
        feature = [length ** (-exponent) for length in lengths]
        if positive_gap:
            solution = solve_two_features([1.0] * len(lengths), feature, values)
            if solution is None:
                continue
            gap, amplitude = solution
            if gap <= 0.0 or amplitude <= 0.0:
                continue
            prediction = [gap + amplitude * value for value in feature]
        else:
            denominator = sum(value * value for value in feature)
            amplitude = sum(
                value * observed for value, observed in zip(feature, values)
            ) / denominator
            gap = 0.0
            if amplitude <= 0.0:
                continue
            prediction = [amplitude * value for value in feature]
        error = sum(
            (predicted - observed) ** 2
            for predicted, observed in zip(prediction, values)
        )
        candidate = (error, gap, amplitude, exponent)
        if best is None or candidate[0] < best[0]:
            best = candidate
    if best is None:
        return {"fit_status": "NO_ADMISSIBLE_PARAMETERS"}
    error, gap, amplitude, exponent = best
    return {
        "fit_status": "RESOLVED",
        "training_sse": error,
        "Delta_inf": gap,
        "amplitude": amplitude,
        "exponent": exponent,
    }


def fit_log_power(lengths: list[float], values: list[float]) -> dict[str, float]:
    x = [math.log(value) for value in lengths]
    y = [math.log(value) for value in values]
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    slope = sum(
        (left - x_mean) * (right - y_mean) for left, right in zip(x, y)
    ) / sum((left - x_mean) ** 2 for left in x)
    intercept = y_mean - slope * x_mean
    return {"amplitude": math.exp(intercept), "exponent": -slope}


def held_out_fixed_z1(
    lengths: list[float], values: list[float]
) -> tuple[float, list[dict[str, float]]]:
    total = 0.0
    rows: list[dict[str, float]] = []
    for held in range(len(lengths)):
        train_lengths = [value for index, value in enumerate(lengths) if index != held]
        train_values = [value for index, value in enumerate(values) if index != held]
        fit = fit_fixed_z1(train_lengths, train_values)
        if fit.get("fit_status") != "RESOLVED":
            return math.inf, rows
        prediction = (
            float(fit["amplitude"]) / lengths[held]
            + float(fit["correction"]) / lengths[held] ** 2
        )
        if prediction <= 0.0:
            return math.inf, rows
        error = (prediction - values[held]) / values[held]
        total += error**2
        rows.append(
            {
                "held_L": int(lengths[held]),
                "observed": values[held],
                "predicted": prediction,
                "relative_error": error,
            }
        )
    return total, rows


def held_out_gap_family(
    lengths: list[float], values: list[float], positive_gap: bool
) -> tuple[float, list[dict[str, float]]]:
    total = 0.0
    rows: list[dict[str, float]] = []
    for held in range(len(lengths)):
        train_lengths = [value for index, value in enumerate(lengths) if index != held]
        train_values = [value for index, value in enumerate(values) if index != held]
        fit = fit_gap_family(train_lengths, train_values, positive_gap)
        if fit.get("fit_status") != "RESOLVED":
            return math.inf, rows
        prediction = float(fit["Delta_inf"]) + float(fit["amplitude"]) * (
            lengths[held] ** (-float(fit["exponent"]))
        )
        error = (prediction - values[held]) / values[held]
        total += error**2
        rows.append(
            {
                "held_L": int(lengths[held]),
                "observed": values[held],
                "predicted": prediction,
                "relative_error": error,
            }
        )
    return total, rows


def relative_range(values: list[float]) -> float:
    return (max(values) - min(values)) / (sum(values) / len(values))


def classify(rows: list[dict[str, object]]) -> dict[str, object]:
    lengths = [float(row["L"]) for row in rows]
    gaps = [float(row["Delta_act"]) for row in rows]
    chis = [float(row["chi_tau"]) for row in rows]
    residues = [float(row["R_low"]) for row in rows]
    fixed_score, fixed_rows = held_out_fixed_z1(lengths, gaps)
    gapless_score, gapless_rows = held_out_gap_family(lengths, gaps, False)
    gapped_score, gapped_rows = held_out_gap_family(lengths, gaps, True)
    fixed_fit = fit_fixed_z1(lengths, gaps)
    gap_fit = fit_log_power(lengths, gaps)
    inverse_chi_fit = fit_log_power(lengths, [1.0 / value for value in chis])
    z = float(gap_fit["exponent"])
    y = float(inverse_chi_fit["exponent"])
    scaled_gap = [length * gap for length, gap in zip(lengths, gaps)]
    scaled_chi = [chi / length for length, chi in zip(lengths, chis)]
    tail_gap = scaled_gap[2:]
    tail_chi = scaled_chi[2:]
    tail_residue = residues[2:]
    tests = {
        "gap_strictly_decreases": all(
            gaps[index + 1] < gaps[index] for index in range(len(gaps) - 1)
        ),
        "chi_strictly_increases": all(
            chis[index + 1] > chis[index] for index in range(len(chis) - 1)
        ),
        "fixed_z1_beats_positive_gap": fixed_score < gapped_score,
        "fixed_z1_near_free_gapless": fixed_score <= 1.25 * gapless_score,
        "z_in_window": 0.90 <= z <= 1.10,
        "y_in_window": 0.90 <= y <= 1.10,
        "exponents_agree": abs(z - y) <= 0.10,
        "tail_scaled_gap_stable": relative_range(tail_gap) <= 0.05,
        "tail_scaled_chi_stable": relative_range(tail_chi) <= 0.05,
        "residue_nonzero": all(value >= 1.0e-6 for value in residues),
        "tail_residue_stable": relative_range(tail_residue) <= 0.35,
    }
    passes = all(tests.values())
    return {
        "rows": rows,
        "L_times_Delta": scaled_gap,
        "chi_over_L": scaled_chi,
        "gap_power_fit": gap_fit,
        "fixed_z1_fit": fixed_fit,
        "chi_power_exponent_y": y,
        "fixed_z1_heldout_sse_relative": fixed_score,
        "gapless_heldout_sse_relative": gapless_score,
        "positive_gap_heldout_sse_relative": gapped_score,
        "fixed_z1_heldout_rows": fixed_rows,
        "gapless_heldout_rows": gapless_rows,
        "positive_gap_heldout_rows": gapped_rows,
        "tail_scaled_gap_relative_range": relative_range(tail_gap),
        "tail_scaled_chi_relative_range": relative_range(tail_chi),
        "tail_residue_relative_range": relative_range(tail_residue),
        "checks": tests,
        "passes": passes,
        "classification": (
            "CENTERLINE_Z1_COMPATIBLE_L4_L12"
            if passes
            else "CENTERLINE_Z1_REJECTED_L4_L12"
        ),
    }


def centerline_row(row: dict[str, object]) -> dict[str, object]:
    return {
        "L": int(row["L"]),
        "rho_anchor": 0.25,
        "source_q": [int(row["q"])],
        "weights": [1.0],
        "Delta_act": float(row["Delta_act"]),
        "chi_tau": float(row["chi_tau"]),
        "R_low": float(row["R_low"]),
    }


def final_ground_energy(row: dict[str, object], target: bool) -> float:
    final = row["ground_sequence"][-1]
    return float(final["energy"] if target else final["ground_energy"])


def final_response_metrics(row: dict[str, object], target: bool) -> dict[str, object]:
    final = row["response_sequence"][-1]
    return final if target else final["metrics"]


def audit_row(
    pair: tuple[int, int], target: dict[str, object], blind: dict[str, object]
) -> dict[str, object]:
    length, charge = pair
    exact_keys = (
        "L",
        "q",
        "rho",
        "sector_dimension",
        "translation_orbits",
        "ground_block_dimension",
        "ground_block_nnz",
        "response_block_dimension",
        "response_block_nnz",
    )
    for key in exact_keys:
        check(target[key] == blind[key], f"L{length}q{charge} exact raw {key}")

    tolerances = {
        "ground_energy": 2.0e-8,
        "Delta_act": 2.0e-8,
        "chi_tau": 5.0e-7,
        "R_low": 5.0e-6,
    }
    differences: dict[str, float] = {}
    for key, tolerance in tolerances.items():
        difference = relative_difference(float(target[key]), float(blind[key]))
        differences[key] = difference
        check(
            difference <= tolerance,
            f"L{length}q{charge} target/blind {key}",
            difference,
        )

    target_weight = float(target["response_full_norm_squared"])
    blind_weight = float(blind["response_total_weight"])
    weight_difference = relative_difference(target_weight, blind_weight)
    floor_difference = relative_difference(
        float(target["response_sequence"][-1]["weight_floor"]),
        float(blind["weight_floor"]),
    )
    differences["response_weight"] = weight_difference
    differences["weight_floor"] = floor_difference
    check(weight_difference <= 2.0e-8, f"L{length}q{charge} response weight")
    check(floor_difference <= 2.0e-8, f"L{length}q{charge} weight floor")

    for label, row in (("target", target), ("blind", blind)):
        prefix = f"L{length}q{charge} {label}"
        check(row["status"] == "RESOLVED", f"{prefix} resolved")
        check(bool(row["threshold_stable"]), f"{prefix} threshold stable")
        check(float(row["ground_residual"]) <= 1.0e-9, f"{prefix} ground residual")
        check(float(row["active_actual_residual"]) <= 1.0e-9, f"{prefix} active residual")
        ground_orth = float(
            row[
                "ground_krylov_orthogonality"
                if label == "target"
                else "ground_krylov_orthogonality_error"
            ]
        )
        response_orth = float(
            row[
                "response_krylov_orthogonality"
                if label == "target"
                else "response_krylov_orthogonality_error"
            ]
        )
        check(ground_orth <= 1.0e-10, f"{prefix} ground orthogonality")
        check(response_orth <= 1.0e-10, f"{prefix} response orthogonality")
        check(float(row["ground_block_hermiticity_error"]) <= 1.0e-12, f"{prefix} ground Hermiticity")
        check(float(row["response_block_hermiticity_error"]) <= 1.0e-12, f"{prefix} response Hermiticity")
        check(float(row["response_projection_error"]) <= 1.0e-9, f"{prefix} projection closure")
        if label == "target":
            check(not row["memory_guards"], f"{prefix} memory guards clear")
            check(float(row["max_rss_bytes"]) <= 6 * (1 << 30), f"{prefix} RSS guard")
        else:
            check(not row["failures"], f"{prefix} failure list clear")
            check(float(row["peak_rss_bytes"]) <= 6 * (1 << 30), f"{prefix} RSS guard")
            check(float(row["response_momentum_covariance_error"]) <= 1.0e-9, f"{prefix} momentum covariance")
            controls = row["structural_controls"]
            check(int(controls["owner_edges"]) == 3 * length, f"{prefix} owner census")
            check(int(controls["unique_edges"]) == 3 * length, f"{prefix} owner uniqueness")
            check(all(int(value) == 3 for value in controls["degrees"]), f"{prefix} degree three")
            check(bool(controls["bipartite_edges"]), f"{prefix} bipartite")
            check(float(controls["one_carrier_band_linf"]) <= 1.0e-12, f"{prefix} one-carrier bands")
        check(int(row["total_matvecs"]) <= 2000, f"{prefix} matvec guard")
        check(float(row["wall_seconds"]) <= 3 * 60 * 60, f"{prefix} wall guard")

    # Independently recompute final checkpoint stability.
    for label, row in (("target", target), ("blind", blind)):
        ground_sequence = row["ground_sequence"]
        response_sequence = row["response_sequence"]
        check(len(ground_sequence) >= 2, f"L{length}q{charge} {label} ground checkpoints")
        check(len(response_sequence) >= 2, f"L{length}q{charge} {label} response checkpoints")
        ground_difference = relative_difference(
            float(
                ground_sequence[-1]["energy"]
                if label == "target"
                else ground_sequence[-1]["ground_energy"]
            ),
            float(
                ground_sequence[-2]["energy"]
                if label == "target"
                else ground_sequence[-2]["ground_energy"]
            ),
        )
        check(ground_difference <= 2.0e-10, f"L{length}q{charge} {label} ground stable")
        final_metrics = final_response_metrics(row, label == "target")
        previous_metrics = (
            response_sequence[-2]
            if label == "target"
            else response_sequence[-2]["metrics"]
        )
        check(
            relative_difference(
                float(final_metrics["Delta_act"]),
                float(previous_metrics["Delta_act"]),
            )
            <= 2.0e-7,
            f"L{length}q{charge} {label} gap stable",
        )
        check(
            relative_difference(
                float(final_metrics["chi_tau"]), float(previous_metrics["chi_tau"])
            )
            <= 2.0e-7,
            f"L{length}q{charge} {label} chi stable",
        )
        check(
            relative_difference(
                float(final_metrics["R_low"]), float(previous_metrics["R_low"])
            )
            <= 2.0e-6,
            f"L{length}q{charge} {label} residue stable",
        )

    # Lowest-five telemetry belongs to the blind method.  The first Ritz value
    # reconstructs the reported ground and active response pole.
    for sequence_name in ("ground_sequence", "response_sequence"):
        sequence = blind[sequence_name]
        for checkpoint in sequence:
            values = [float(value) for value in checkpoint["lowest_five_ritz_values"]]
            expected_count = min(5, int(checkpoint["krylov_dimension"]))
            check(len(values) == expected_count, f"L{length}q{charge} {sequence_name} lowest-five count")
            check(all(math.isfinite(value) for value in values), f"L{length}q{charge} {sequence_name} lowest-five finite")
            check(all(values[index] <= values[index + 1] for index in range(len(values) - 1)), f"L{length}q{charge} {sequence_name} lowest-five ordered")
    ground_first = float(blind["ground_sequence"][-1]["lowest_five_ritz_values"][0])
    response_first = float(blind["response_sequence"][-1]["lowest_five_ritz_values"][0])
    check(abs(ground_first - float(blind["ground_energy"])) <= 1.0e-9, f"L{length}q{charge} lowest ground reconstruction")
    check(abs(response_first - (float(blind["ground_energy"]) + float(blind["Delta_act"]))) <= 1.0e-9, f"L{length}q{charge} lowest response reconstruction")

    # The authorized protocol requires the lowest five values to be reported,
    # not merely held transiently inside the target Krylov calculation.  The
    # target raw currently serializes only E0 for ground checkpoints and only
    # response metrics for response checkpoints.  Fail this reporting defect
    # closed even though the promoted pole metrics can still be reconstructed.
    for sequence_name in ("ground_sequence", "response_sequence"):
        for checkpoint_index, checkpoint in enumerate(target[sequence_name]):
            check(
                "lowest_five_ritz_values" in checkpoint,
                (
                    f"TARGET_TELEMETRY_LOWEST_FIVE L{length}q{charge} "
                    f"{sequence_name}[{checkpoint_index}]"
                ),
            )
    return differences


def compare_classification(
    observed: dict[str, object], expected: dict[str, object], label: str
) -> None:
    check(observed["checks"] == expected["checks"], f"{label} Boolean decisions")
    check(bool(observed["passes"]) == bool(expected["passes"]), f"{label} aggregate pass")
    scalar_keys = (
        "chi_power_exponent_y",
        "fixed_z1_heldout_sse_relative",
        "gapless_heldout_sse_relative",
        "positive_gap_heldout_sse_relative",
        "tail_scaled_gap_relative_range",
        "tail_scaled_chi_relative_range",
        "tail_residue_relative_range",
    )
    for key in scalar_keys:
        difference = relative_difference(float(observed[key]), float(expected[key]))
        check(difference <= 1.0e-9, f"{label} fitted scalar {key}", difference)
    for key in ("L_times_Delta", "chi_over_L"):
        for index, (left, right) in enumerate(zip(observed[key], expected[key])):
            difference = relative_difference(float(left), float(right))
            check(difference <= 1.0e-9, f"{label} {key}[{index}]", difference)
    for fit_name, fit_keys in (
        ("gap_power_fit", ("amplitude", "exponent")),
        ("fixed_z1_fit", ("amplitude", "correction", "training_sse")),
    ):
        if "fit_status" in observed[fit_name] or "fit_status" in expected[fit_name]:
            check(
                observed[fit_name].get("fit_status") == expected[fit_name].get("fit_status"),
                f"{label} {fit_name} status",
            )
        for key in fit_keys:
            difference = relative_difference(
                float(observed[fit_name][key]), float(expected[fit_name][key])
            )
            check(difference <= 1.0e-9, f"{label} {fit_name} {key}", difference)
    for family in (
        "fixed_z1_heldout_rows",
        "gapless_heldout_rows",
        "positive_gap_heldout_rows",
    ):
        for index, (left, right) in enumerate(zip(observed[family], expected[family])):
            check(int(left["held_L"]) == int(right["held_L"]), f"{label} {family}[{index}] L")
            for key in ("observed", "predicted", "relative_error"):
                difference = relative_difference(float(left[key]), float(right[key]))
                check(difference <= 1.0e-8, f"{label} {family}[{index}] {key}", difference)


def main() -> None:
    input_paths = {
        "sealed_reference": SEALED,
        "target_protocol": TARGET_PROTOCOL,
        "target_result": TARGET_RESULT,
        "target_L10_q5": TARGET_RAW[(10, 5)],
        "target_L12_q6": TARGET_RAW[(12, 6)],
        "blind_L10_q5": BLIND_RAW[(10, 5)],
        "blind_L12_q6": BLIND_RAW[(12, 6)],
    }
    for key, path in input_paths.items():
        check(path.is_file(), f"input exists {key}")
        if path.is_file():
            check(sha256(path) == EXPECTED_HASHES[key], f"input hash {key}")

    sealed = json.loads(SEALED.read_text())
    target_result = json.loads(TARGET_RESULT.read_text())
    target_rows = {pair: json.loads(path.read_text()) for pair, path in TARGET_RAW.items()}
    blind_rows = {pair: json.loads(path.read_text()) for pair, path in BLIND_RAW.items()}

    raw_differences = {
        f"L{length}_q{charge}": audit_row(
            (length, charge), target_rows[(length, charge)], blind_rows[(length, charge)]
        )
        for length, charge in PAIRS
    }
    aggregate_rss = sum(
        int(target_rows[pair]["max_rss_bytes"]) + int(blind_rows[pair]["peak_rss_bytes"])
        for pair in PAIRS
    )
    aggregate_wall_sum = sum(
        float(target_rows[pair]["wall_seconds"]) + float(blind_rows[pair]["wall_seconds"])
        for pair in PAIRS
    )
    check(aggregate_rss <= 32 * (1 << 30), "four-process aggregate RSS guard", aggregate_rss)

    sealed_rows: dict[tuple[int, int], dict[str, object]] = {}
    for length_rows in sealed["sector_rows"].values():
        for row in length_rows:
            sealed_rows[(int(row["L"]), int(row["q"]))] = row
    base = [centerline_row(sealed_rows[(length, length // 2)]) for length in (4, 6, 8)]
    blind_input_rows = base + [centerline_row(blind_rows[pair]) for pair in PAIRS]
    target_input_rows = base + [centerline_row(target_rows[pair]) for pair in PAIRS]
    blind_classification = classify(blind_input_rows)
    target_reconstruction = classify(target_input_rows)

    check(
        blind_classification["classification"] == target_reconstruction["classification"],
        "target/blind exact classification",
    )
    check(
        target_result["classification"] == target_reconstruction["classification"],
        "target RESULT classification",
    )
    check(target_result["protocol_sha256"] == EXPECTED_HASHES["target_protocol"], "target RESULT protocol custody")
    check(target_result["sealed_input_sha256"] == EXPECTED_HASHES["sealed_reference"], "target RESULT sealed custody")
    check(target_result["all_required_rows_resolved"] is True, "target RESULT rows resolved")
    check(target_result["target_rows"] == [target_rows[pair] for pair in PAIRS], "target RESULT embeds raw rows exactly")
    compare_classification(blind_classification, target_reconstruction, "blind versus rebuilt target")
    compare_classification(target_reconstruction, target_result["centerline"], "rebuilt versus target RESULT")

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
        "target claim ceiling",
    )

    classification = str(blind_classification["classification"])
    route_halt = classification == "CENTERLINE_Z1_REJECTED_L4_L12"
    check(route_halt, "frozen classification mandates route halt", classification)
    failed_z1_checks = [
        name for name, passed in blind_classification["checks"].items() if not passed
    ]
    failures = [row for row in checks if not row["passed"]]
    telemetry_failures = [
        row for row in failures if str(row["label"]).startswith("TARGET_TELEMETRY_LOWEST_FIVE")
    ]
    substantive_failures = [row for row in failures if row not in telemetry_failures]
    if route_halt and telemetry_failures and not substantive_failures:
        verdict = (
            "FAIL_CLOSED_TARGET_LOWEST_FIVE_TELEMETRY_MISSING__"
            "CLASSIFICATION_REPRODUCED_CENTERLINE_Z1_REJECTED_L4_L12__"
            "HALT_NATIVE_ALGEBRA_ROUTE"
        )
    elif not failures and route_halt:
        verdict = "PASS_HOSTILE_CENTERLINE_Z1_REJECTED_L4_L12__HALT_NATIVE_ALGEBRA_ROUTE"
    else:
        verdict = "FAIL_HOSTILE_CENTERLINE_COMPARISON"
    result = {
        "schema": "HOSTILE_EXTENDED_CENTERLINE_COMPARISON_V001",
        "verdict": verdict,
        "classification": classification,
        "mandated_route_status": (
            "HALT__DO_NOT_START_NATIVE_ALGEBRA"
            if route_halt
            else "CONDITIONAL_ON_HOSTILE_PASS"
        ),
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "substantive_comparison_failures": substantive_failures,
        "target_lowest_five_telemetry_failures": telemetry_failures,
        "required_target_repair": (
            "REPORTING_ONLY__SERIALIZE_LOWEST_FIVE_RITZ_VALUES_AT_EVERY_TARGET_"
            "GROUND_AND_RESPONSE_CHECKPOINT__RERUN_L10_Q5_AND_L12_Q6__VERIFY_"
            "ALL_PREEXISTING_PROMOTED_METRICS_AND_RESOURCE_GUARDS_UNCHANGED__"
            "REBUILD_RESULT_AND_REPEAT_HOSTILE_COMPARISON"
        ),
        "failed_z1_classification_checks": failed_z1_checks,
        "raw_target_blind_relative_differences": raw_differences,
        "independent_centerline": blind_classification,
        "rebuilt_target_centerline": target_reconstruction,
        "target_reported_centerline": target_result["centerline"],
        "resources": {
            "four_process_peak_rss_sum_bound_bytes": aggregate_rss,
            "four_process_wall_seconds_sum": aggregate_wall_sum,
            "target_wall_seconds_sum": sum(float(target_rows[pair]["wall_seconds"]) for pair in PAIRS),
            "blind_wall_seconds_sum": sum(float(blind_rows[pair]["wall_seconds"]) for pair in PAIRS),
            "target_peak_rss_max_bytes": max(int(target_rows[pair]["max_rss_bytes"]) for pair in PAIRS),
            "blind_peak_rss_max_bytes": max(int(blind_rows[pair]["peak_rss_bytes"]) for pair in PAIRS),
        },
        "input_sha256": {key: sha256(path) for key, path in input_paths.items()},
        "post_output_method_sha256": sha256(METHOD),
        "comparison_implementation_sha256": sha256(Path(__file__).resolve()),
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
                "GRAVITY",
            ],
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(verdict)
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    print("classification", classification)
    print("failed z1 checks", ",".join(failed_z1_checks))
    if failures:
        for failure in failures:
            print("FAIL", failure["label"], failure.get("detail"))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
