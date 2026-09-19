#!/usr/bin/env python3
"""Publish a target-adjudicator-compatible blind index, owner-once.

All fits and decisions are reconstructed here from the frozen public formulas.
No target module, target worker, or target matrix is imported.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import blind_contract_control as credential_control

from contract_common import (
    FREEZE_SCHEMA,
    FREEZE_STATUS,
    INDEX_SCHEMA,
    SIZES,
    Refusal,
    atomic_owner_once_json,
    demand,
    load_pinned_json,
    repo_file,
    repo_relative,
    sha256_file,
)


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
SEALED_LOW = ROOT / "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001" / "RESULT.json"
SEALED_LOW_SHA256 = "ebd522411a0e7f67e37d5023fbdea01bc63bdd796ca23020b0d749b414146a05"
EXPONENTS = tuple(0.25 + index * (3.75 / 15000.0) for index in range(15001))


def finite(value: object, label: str) -> float:
    demand(type(value) in (int, float) and math.isfinite(float(value)), f"{label}: finite JSON number required")
    return float(value)


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


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
    return (ay * bb - by * ab) / determinant, (by * aa - ay * ab) / determinant


def fit_fixed_z1(lengths: list[float], values: list[float]) -> dict[str, object]:
    first = [1.0 / length for length in lengths]
    second = [1.0 / length**2 for length in lengths]
    solution = solve_two_features(first, second, values)
    if solution is None:
        return {"fit_status": "NO_ADMISSIBLE_PARAMETERS"}
    amplitude, correction = solution
    predicted = [
        amplitude / length + correction / length**2 for length in lengths
    ]
    if amplitude <= 0.0 or any(value <= 0.0 for value in predicted):
        return {"fit_status": "NO_ADMISSIBLE_PARAMETERS"}
    return {
        "fit_status": "RESOLVED",
        "amplitude": amplitude,
        "correction": correction,
        "training_sse": sum(
            (prediction - observed) ** 2
            for prediction, observed in zip(predicted, values)
        ),
    }


def fit_gap_family(
    lengths: list[float], values: list[float], positive_gap: bool
) -> dict[str, object]:
    best: tuple[float, float, float, float] | None = None
    for exponent in EXPONENTS:
        feature = [length ** (-exponent) for length in lengths]
        if positive_gap:
            solution = solve_two_features([1.0] * len(lengths), feature, values)
            if solution is None:
                continue
            gap, amplitude = solution
            if gap <= 0.0 or amplitude <= 0.0:
                continue
            predicted = [gap + amplitude * item for item in feature]
        else:
            denominator = sum(item * item for item in feature)
            amplitude = sum(
                item * observed for item, observed in zip(feature, values)
            ) / denominator
            gap = 0.0
            if amplitude <= 0.0:
                continue
            predicted = [amplitude * item for item in feature]
        error = sum(
            (prediction - observed) ** 2
            for prediction, observed in zip(predicted, values)
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
    demand(all(value > 0.0 for value in values), "log-power fit requires positive values")
    x = [math.log(value) for value in lengths]
    y = [math.log(value) for value in values]
    x_mean, y_mean = sum(x) / len(x), sum(y) / len(y)
    denominator = sum((value - x_mean) ** 2 for value in x)
    demand(denominator > 0.0, "log-power fit is singular")
    slope = sum(
        (left - x_mean) * (right - y_mean) for left, right in zip(x, y)
    ) / denominator
    intercept = y_mean - slope * x_mean
    return {"amplitude": math.exp(intercept), "exponent": -slope}


def relative_sse(observed: float, predicted: float) -> float:
    demand(observed > 0.0 and predicted > 0.0, "held-out fit requires positive values")
    return ((predicted - observed) / observed) ** 2


def held_out_fixed(
    lengths: list[float], values: list[float]
) -> tuple[float, list[dict[str, float]]]:
    total = 0.0
    rows: list[dict[str, float]] = []
    for held in range(len(lengths)):
        fit = fit_fixed_z1(
            [value for index, value in enumerate(lengths) if index != held],
            [value for index, value in enumerate(values) if index != held],
        )
        if fit.get("fit_status") != "RESOLVED":
            return math.inf, rows
        prediction = float(fit["amplitude"]) / lengths[held] + float(
            fit["correction"]
        ) / lengths[held] ** 2
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


def held_out_gap(
    lengths: list[float], values: list[float], positive_gap: bool
) -> tuple[float, list[dict[str, float]]]:
    total = 0.0
    rows: list[dict[str, float]] = []
    for held in range(len(lengths)):
        fit = fit_gap_family(
            [value for index, value in enumerate(lengths) if index != held],
            [value for index, value in enumerate(values) if index != held],
            positive_gap,
        )
        if fit.get("fit_status") != "RESOLVED":
            return math.inf, rows
        prediction = float(fit["Delta_inf"]) + float(fit["amplitude"]) * (
            lengths[held] ** (-float(fit["exponent"]))
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


def relative_range(values: list[float]) -> float:
    mean = sum(values) / len(values)
    demand(mean > 0.0, "relative range requires positive mean")
    return (max(values) - min(values)) / mean


def classify(rows: list[dict[str, object]]) -> dict[str, object]:
    demand([row.get("L") for row in rows] == list(SIZES), "classification size order mismatch")
    lengths = [float(row["L"]) for row in rows]
    gaps = [finite(row.get("Delta_act"), "Delta_act") for row in rows]
    chis = [finite(row.get("chi_tau"), "chi_tau") for row in rows]
    residues = [finite(row.get("R_low"), "R_low") for row in rows]
    demand(all(value > 0.0 for value in gaps + chis + residues), "classification inputs must be positive")
    fixed_score, fixed_rows = held_out_fixed(lengths, gaps)
    gapless_score, gapless_rows = held_out_gap(lengths, gaps, False)
    gapped_score, gapped_rows = held_out_gap(lengths, gaps, True)
    fixed_fit = fit_fixed_z1(lengths, gaps)
    gap_fit = fit_log_power(lengths, gaps)
    inverse_chi_fit = fit_log_power(lengths, [1.0 / value for value in chis])
    z, y = float(gap_fit["exponent"]), float(inverse_chi_fit["exponent"])
    scaled_gap = [length * gap for length, gap in zip(lengths, gaps)]
    scaled_chi = [chi / length for length, chi in zip(lengths, chis)]
    checks = {
        "gap_strictly_decreases": all(gaps[index + 1] < gaps[index] for index in range(4)),
        "chi_strictly_increases": all(chis[index + 1] > chis[index] for index in range(4)),
        "fixed_z1_beats_positive_gap": fixed_score < gapped_score,
        "fixed_z1_near_free_gapless": fixed_score <= 1.25 * gapless_score,
        "z_in_window": 0.90 <= z <= 1.10,
        "y_in_window": 0.90 <= y <= 1.10,
        "exponents_agree": abs(z - y) <= 0.10,
        "tail_scaled_gap_stable": relative_range(scaled_gap[2:]) <= 0.05,
        "tail_scaled_chi_stable": relative_range(scaled_chi[2:]) <= 0.05,
        "residue_nonzero": all(value >= 1.0e-6 for value in residues),
        "tail_residue_stable": relative_range(residues[2:]) <= 0.35,
    }
    passed = all(checks.values())
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
        "tail_scaled_gap_relative_range": relative_range(scaled_gap[2:]),
        "tail_scaled_chi_relative_range": relative_range(scaled_chi[2:]),
        "tail_residue_relative_range": relative_range(residues[2:]),
        "checks": checks,
        "passes": passed,
        "classification": (
            "CENTERLINE_Z1_COMPATIBLE_L4_L12"
            if passed
            else "CENTERLINE_Z1_REJECTED_L4_L12"
        ),
    }


def validate_row(row: dict[str, object], length: int, charge: int) -> None:
    demand(row.get("status") == "RESOLVED", f"L{length}q{charge}: unresolved")
    demand(type(row.get("L")) is int and row["L"] == length, "row L identity")
    demand(type(row.get("q")) is int and row["q"] == charge, "row q identity")
    demand(relative_difference(finite(row.get("rho"), "rho"), charge / (2 * length)) <= 1.0e-15, "row density identity")
    demand(type(row.get("sector_dimension")) is int and row["sector_dimension"] == math.comb(2 * length, charge), "sector dimension")
    for field, limit in (
        ("ground_residual", 1.0e-9),
        ("active_actual_residual", 1.0e-9),
        ("ground_block_hermiticity_error", 1.0e-12),
        ("response_block_hermiticity_error", 1.0e-12),
        ("ground_krylov_orthogonality", 1.0e-10),
        ("response_krylov_orthogonality", 1.0e-10),
        ("response_projection_error", 1.0e-9),
    ):
        demand(0.0 <= finite(row.get(field), field) <= limit, f"{field} guard")
    demand(type(row.get("ground_matvecs")) is int and type(row.get("response_matvecs")) is int and type(row.get("total_matvecs")) is int, "matvec integer contract")
    demand(row["ground_matvecs"] + row["response_matvecs"] == row["total_matvecs"] <= 2000, "matvec reconstruction")
    demand(finite(row.get("wall_seconds"), "wall_seconds") <= 10800.0, "wall guard")
    demand(type(row.get("max_rss_bytes")) is int and row["max_rss_bytes"] <= 6 * (1 << 30), "RSS guard")
    demand(row.get("threshold_stable") is True, "threshold stability")
    demand(finite(row.get("Delta_act"), "Delta_act") > 0.0, "positive gap")
    demand(finite(row.get("chi_tau"), "chi_tau") > 0.0, "positive chi")
    demand(1.0e-6 <= finite(row.get("R_low"), "R_low") <= 1.0 + 1.0e-12, "residue guard")
    full = finite(row.get("response_full_norm_squared"), "full response norm")
    projected = finite(row.get("response_projected_norm_squared"), "projected response norm")
    demand(abs(abs(full - projected) - float(row["response_projection_error"])) <= 1.0e-12, "projection reconstruction")
    for name, matvec_field in (("ground_sequence", "ground_matvecs"), ("response_sequence", "response_matvecs")):
        sequence = row.get(name)
        demand(isinstance(sequence, list) and sequence, f"{name} absent")
        dimensions = [item.get("krylov_dimension") for item in sequence if isinstance(item, dict)]
        demand(all(type(value) is int for value in dimensions), f"{name} dimension types")
        final = int(row[matvec_field])
        expected = sorted({value for value in (16, 32, 64, 96, 128) if value <= final} | {final})
        demand(dimensions == expected, f"{name} checkpoint census")


def low_rows() -> dict[tuple[int, int], dict[str, object]]:
    demand(sha256_file(SEALED_LOW) == SEALED_LOW_SHA256, "sealed low-size spectrum hash mismatch")
    payload = json.loads(SEALED_LOW.read_text(encoding="utf-8"))
    groups = payload.get("sector_rows")
    demand(isinstance(groups, dict), "sealed low-size sector rows absent")
    result: dict[tuple[int, int], dict[str, object]] = {}
    for group in groups.values():
        demand(isinstance(group, list), "sealed low-size row group malformed")
        for row in group:
            demand(isinstance(row, dict), "sealed low-size row malformed")
            pair = (int(row["L"]), int(row["q"]))
            result[pair] = row
    return result


def publish(args: argparse.Namespace) -> None:
    freeze = load_pinned_json(args.freeze, args.freeze_sha256, "blind method freeze")
    demand(freeze.get("schema") == FREEZE_SCHEMA, "blind freeze schema mismatch")
    demand(freeze.get("status") == FREEZE_STATUS, "blind freeze status mismatch")
    demand(freeze.get("target_code_or_matrices_imported") is False, "blind freeze imports target bytes")
    planned = freeze.get("planned_sectors")
    demand(isinstance(planned, list) and planned, "blind planned sector census absent")
    pairs: list[tuple[int, int]] = []
    for item in planned:
        demand(isinstance(item, list) and len(item) == 2 and all(type(value) is int for value in item), "blind planned sector malformed")
        pair = (item[0], item[1])
        demand(pair[0] in (10, 12) and 1 <= pair[1] <= pair[0], "blind planned sector outside domain")
        pairs.append(pair)
    demand(pairs == sorted(set(pairs)), "blind planned sector order/census mismatch")
    plan = repo_file(ROOT, freeze.get("sector_plan_path"), freeze.get("sector_plan_sha256"), "blind sector plan")
    plan_payload = load_pinned_json(plan, str(freeze["sector_plan_sha256"]), "blind sector plan")
    demand(plan_payload.get("planned_sectors") == planned, "freeze/plan sector mismatch")
    rows: dict[tuple[int, int], dict[str, object]] = {}
    bindings: dict[str, dict[str, str]] = {}
    authorization_bindings: dict[str, dict[str, str]] = {}
    validated_authorizations: list[dict[str, object]] = []
    for length, charge in pairs:
        path = args.rows_dir / f"SECTOR_L{length}_Q{charge}.json"
        demand(path.is_file(), f"L{length}q{charge}: row absent")
        stat = path.stat()
        demand(stat.st_nlink == 1 and stat.st_mode & 0o777 == 0o444, f"L{length}q{charge}: owner-once custody")
        row = json.loads(path.read_text(encoding="utf-8"))
        demand(isinstance(row, dict), f"L{length}q{charge}: row object required")
        validate_row(row, length, charge)
        credential_path = (
            args.credentials_dir / f"SECTOR_L{length}_Q{charge}.json"
        )
        demand(
            credential_path.is_file(),
            f"L{length}q{charge}: execution credential absent",
        )
        credential_sha256 = sha256_file(credential_path)
        authorization = credential_control.validate_execution_credential(
            credential_path, credential_sha256, length, charge, path,
        )
        demand(
            row.get("execution_authorization") == authorization,
            f"L{length}q{charge}: row execution authorization mismatch",
        )
        rows[(length, charge)] = row
        key = f"{length}:{charge}"
        bindings[key] = {
            "path": repo_relative(ROOT, path, f"L{length}q{charge} row"),
            "sha256": sha256_file(path),
        }
        authorization_bindings[key] = {
            "path": repo_relative(
                ROOT, credential_path, f"L{length}q{charge} credential",
            ),
            "sha256": credential_sha256,
        }
        validated_authorizations.append(authorization)
    demand(
        len({str(item["authorization_nonce"]) for item in validated_authorizations})
        == len(pairs),
        "blind execution-authorization nonce reuse",
    )
    demand(
        len({str(item["credential_sha256"]) for item in validated_authorizations})
        == len(pairs),
        "blind execution-authorization credential reuse",
    )
    low = low_rows()
    atom_classifications: dict[str, object] = {}
    atoms = plan_payload.get("atoms")
    demand(isinstance(atoms, list) and atoms, "blind atom plan absent")
    for atom in atoms:
        demand(isinstance(atom, dict) and isinstance(atom.get("atom_id"), str), "blind atom malformed")
        qmap = atom.get("q_by_L")
        demand(isinstance(qmap, dict), "blind atom q map absent")
        if any(int(qmap[str(length)]) == 0 for length in SIZES):
            payload = {"status": "ZERO_RESPONSE_NORM__ATOM_NONPASSING", "classification": None}
        else:
            inputs = []
            for length in SIZES:
                charge = int(qmap[str(length)])
                row = low[(length, charge)] if length <= 8 else rows[(length, charge)]
                inputs.append(
                    {
                        "L": length,
                        "rho_anchor": charge / (2 * length),
                        "source_q": [charge],
                        "weights": [1.0],
                        "Delta_act": finite(row.get("Delta_act"), "atom gap"),
                        "chi_tau": finite(row.get("chi_tau"), "atom chi"),
                        "R_low": finite(row.get("R_low"), "atom residue"),
                    }
                )
            payload = {"status": "RESOLVED", "classification": classify(inputs)}
        atom_id = str(atom["atom_id"])
        demand(atom_id not in atom_classifications, "duplicate blind atom ID")
        atom_classifications[atom_id] = payload
    index = {
        "schema": INDEX_SCHEMA,
        "role": "blind",
        "status": "BLIND_COMPLETE__READY_FOR_HOSTILE_ADJUDICATION",
        "manifest_sha256": freeze["manifest_sha256"],
        "method_freeze_path": repo_relative(ROOT, args.freeze, "blind method freeze"),
        "method_freeze_sha256": args.freeze_sha256,
        "implementation_path": freeze["implementation_path"],
        "implementation_sha256": freeze["implementation_sha256"],
        "rows": bindings,
        "execution_authorizations": authorization_bindings,
        "atom_classifications": atom_classifications,
        "claim_boundary": "FINITE_BLIND_INTERVAL_ROWS_ONLY__NO_PROMOTION_OR_GRAVITY_RESULT",
    }
    atomic_owner_once_json(ROOT, args.output, index)


def validate_execution_bound_index(
    index_path: Path, index_sha256: str, expected_manifest_sha256: str,
) -> dict[str, object]:
    """Authenticate every blind row at the adjudication boundary."""
    index = load_pinned_json(index_path, index_sha256, "blind spectrum index")
    demand(index.get("schema") == INDEX_SCHEMA, "blind index schema mismatch")
    demand(
        index.get("role") == "blind"
        and index.get("status")
        == "BLIND_COMPLETE__READY_FOR_HOSTILE_ADJUDICATION"
        and index.get("manifest_sha256") == expected_manifest_sha256,
        "blind index identity mismatch",
    )
    freeze_path = repo_file(
        ROOT, index.get("method_freeze_path"), index.get("method_freeze_sha256"),
        "blind index method freeze",
    )
    freeze = load_pinned_json(
        freeze_path, str(index["method_freeze_sha256"]),
        "blind index method freeze",
    )
    demand(
        freeze.get("schema") == FREEZE_SCHEMA
        and freeze.get("status") == FREEZE_STATUS
        and freeze.get("manifest_sha256") == expected_manifest_sha256,
        "blind index freeze binding mismatch",
    )
    planned = freeze.get("planned_sectors")
    demand(isinstance(planned, list) and planned, "blind index planned sectors absent")
    pairs: list[tuple[int, int]] = []
    for item in planned:
        demand(
            isinstance(item, list) and len(item) == 2
            and all(type(value) is int for value in item),
            "blind index planned sector malformed",
        )
        pairs.append((item[0], item[1]))
    demand(pairs == sorted(set(pairs)), "blind index planned sector census mismatch")
    expected_keys = {f"{length}:{charge}" for length, charge in pairs}
    rows = index.get("rows")
    authorizations = index.get("execution_authorizations")
    demand(
        isinstance(rows, dict) and set(rows) == expected_keys,
        "blind index row census mismatch",
    )
    demand(
        isinstance(authorizations, dict) and set(authorizations) == expected_keys,
        "blind index execution-authorization census mismatch",
    )
    validated: list[dict[str, object]] = []
    for length, charge in pairs:
        key = f"{length}:{charge}"
        row_entry = rows[key]
        credential_entry = authorizations[key]
        demand(
            isinstance(row_entry, dict) and set(row_entry) == {"path", "sha256"},
            f"blind {key} row entry malformed",
        )
        demand(
            isinstance(credential_entry, dict)
            and set(credential_entry) == {"path", "sha256"},
            f"blind {key} execution-authorization entry malformed",
        )
        row_path = repo_file(
            ROOT, row_entry.get("path"), row_entry.get("sha256"),
            f"blind {key} row",
        )
        metadata = row_path.stat()
        demand(
            metadata.st_nlink == 1 and metadata.st_mode & 0o777 == 0o444,
            f"blind {key} row owner-once custody",
        )
        row = load_pinned_json(
            row_path, str(row_entry["sha256"]), f"blind {key} row",
        )
        validate_row(row, length, charge)
        credential_path = repo_file(
            ROOT, credential_entry.get("path"), credential_entry.get("sha256"),
            f"blind {key} execution authorization",
        )
        authorization = credential_control.validate_execution_credential(
            credential_path, str(credential_entry["sha256"]), length, charge,
            row_path,
        )
        demand(
            row.get("execution_authorization") == authorization,
            f"blind {key} row execution authorization mismatch",
        )
        validated.append(authorization)
    demand(
        len({str(item["authorization_nonce"]) for item in validated}) == len(pairs),
        "blind adjudication execution-authorization nonce reuse",
    )
    demand(
        len({str(item["credential_sha256"]) for item in validated}) == len(pairs),
        "blind adjudication execution-authorization credential reuse",
    )
    return index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", type=Path, required=True)
    parser.add_argument("--freeze-sha256", required=True)
    parser.add_argument("--rows-dir", type=Path, required=True)
    parser.add_argument("--credentials-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        publish(arguments)
    except (Refusal, KeyError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
