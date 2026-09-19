#!/usr/bin/env python3
"""Fail-closed driver for a later hash-pinned relational interval spectrum."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import subprocess
import sys
import tempfile
import time
from decimal import Decimal
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FREEZE = HERE / "FREEZE.json"
SIZES = (4, 6, 8, 10, 12)
LARGE_SIZES = (10, 12)
MANIFEST_SCHEMA = "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001"
MANIFEST_STATUS = "PASS_RELATIONAL_ACCUMULATION_L4_L12__SPECTRUM_MANIFEST_READY"
EXECUTION_TOKEN = "RUN_HASH_PINNED_RELATIONAL_INTERVAL_SPECTRUM_V001"
ACCUMULATION_PROTOCOL = ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001" / "PROTOCOL.md"
ACCUMULATION_PROTOCOL_SHA256 = "d545a4dd0925d4ae47c1231f4f7632c4cdfef14d0864af292f19fd9f6a708d95"
SEALED_LOW = ROOT / "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001" / "RESULT.json"
SEALED_LOW_SHA256 = "ebd522411a0e7f67e37d5023fbdea01bc63bdd796ca23020b0d749b414146a05"
TARGET_ENGINE = ROOT / "DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001" / "compute_phase_screen.py"
TARGET_ENGINE_SHA256 = "e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7"
TARGET_WORKER = HERE / "target_interval_worker.py"
TARGET_WORKER_SHA256 = "6bd6ac5d286a08c007b1dc9c2fb87721b456ece5afc08ddb13f000e1f225c40b"
CREDENTIAL_CONTROL = HERE / "execution_credential.py"
CREDENTIAL_CONTROL_SHA256 = "31b86f56c9691721224bf0359a9e354566a34370f8c00703369d382f30cdd3f3"
CLASSIFIER = ROOT / "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001" / "compare_and_classify.py"
CLASSIFIER_SHA256 = "ab66f64b61b1503a5c5c4a275ff31944f63f12833b1f4523a09551f734cfa853"
MAX_KRYLOV = 128
KRYLOV_CHECKPOINTS = (16, 32, 64, 96, 128)
MAX_MATVECS = 2000
MAX_SECTOR_SECONDS = 3 * 60 * 60
MAX_SECTOR_RSS = 6 * (1 << 30)
MAX_WAVE_RSS = 32 * (1 << 30)
MAX_PARALLEL_WORKERS = 4
HEX = set("0123456789abcdef")
HISTORY_OBSERVABLE_FIELDS = (
    "W_n",
    "allow_probability",
    "blocked_probability",
    "reverse_support_probability",
    "connector_delta_l1",
    "connector_delta_signed",
    "q_retained_after_transport",
    "q_genesis_after",
)


class FailClosed(RuntimeError):
    pass


def load_credential_control():
    specification = importlib.util.spec_from_file_location(
        "frozen_target_execution_credential", CREDENTIAL_CONTROL,
    )
    demand(
        specification is not None and specification.loader is not None,
        "cannot load target execution credential control",
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise FailClosed(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_digest(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def checked_repo_file(raw: object, expected: object, label: str) -> Path:
    demand(isinstance(raw, str) and raw, f"{label}: path missing")
    demand(valid_digest(expected), f"{label}: invalid SHA-256")
    path = (ROOT / raw).resolve()
    demand(path.is_relative_to(ROOT.resolve()), f"{label}: path escapes repository")
    demand(path.is_file(), f"{label}: file missing")
    demand(sha256(path) == expected, f"{label}: SHA-256 mismatch")
    return path


def ratio_pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def parse_fraction(value: object, label: str) -> Fraction:
    demand(isinstance(value, list) and len(value) == 2, f"{label}: expected [numerator,denominator]")
    numerator, denominator = value
    demand(type(numerator) is int and type(denominator) is int and denominator > 0, f"{label}: invalid rational")
    result = Fraction(numerator, denominator)
    demand(value == ratio_pair(result), f"{label}: rational must be reduced with positive denominator")
    return result


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def numeric_match(left: object, right: object, tolerance: float) -> bool:
    if not finite_json_number(left) or not finite_json_number(right):
        return False
    a, b = float(left), float(right)
    if math.isnan(a) or math.isnan(b):
        return False
    if math.isinf(a) or math.isinf(b):
        return a == b
    return relative_difference(a, b) <= tolerance


def finite_json_number(value: object) -> bool:
    return type(value) in (int, float, Decimal) and math.isfinite(float(value))


def exact_numeric_zero(value: object) -> bool:
    if type(value) is Decimal:
        return value.is_finite() and value == 0
    return (
        type(value) in (int, float)
        and math.isfinite(float(value))
        and float(value) == 0.0
    )


def exact_json_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, list):
        return len(left) == len(right) and all(exact_json_equal(a, b) for a, b in zip(left, right))
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(exact_json_equal(left[key], right[key]) for key in left)
    return left == right


def history_event_rows(history: dict[str, object], length: int) -> list[dict[str, object]]:
    demand(type(history.get("L")) is int and history["L"] == length, f"L{length}: history size mismatch")
    comparison = history.get("comparison")
    demand(isinstance(comparison, dict) and comparison.get("resolved") is True, f"L{length}: history unresolved")
    rows = history.get("rows")
    demand(isinstance(rows, list) and len(rows) == length, f"L{length}: event census mismatch")
    demand(all(isinstance(row, dict) and type(row.get("event")) is int for row in rows), f"L{length}: invalid event identifier")
    by_event = {row["event"]: row for row in rows}
    demand(set(by_event) == set(range(1, length + 1)), f"L{length}: events must be exactly 1..L")
    return [by_event[event] for event in range(1, length + 1)]


def full_weight_matrix(history: dict[str, object], length: int) -> list[list[float]]:
    matrix = []
    for event, row in enumerate(history_event_rows(history, length), start=1):
        weights = row.get("sector_weights")
        demand(
            isinstance(weights, list)
            and len(weights) in (length + 1, 2 * length + 1),
            f"L{length}: invalid sector-weight vector length at event {event}",
        )
        if len(weights) == 2 * length + 1:
            tail = weights[length + 1:]
            demand(
                all(exact_numeric_zero(value) for value in tail),
                f"L{length}: nonzero or invalid q>L sector-weight tail at event {event}",
            )
            weights = weights[:length + 1]
        demand(all(finite_json_number(x) and float(x) >= -1.0e-12 for x in weights), f"L{length}: non-finite/negative sector weight")
        demand(abs(sum(float(x) for x in weights) - 1.0) <= 1.0e-9, f"L{length}: sector weights not normalized")
        matrix.append([float(weight) for weight in weights])
    return matrix


def late_weight_matrix(history: dict[str, object], length: int) -> list[list[float]]:
    return full_weight_matrix(history, length)[math.ceil(length / 2) - 1 :]


def reconstructed_pbar(history: dict[str, object], length: int) -> list[float]:
    matrix = late_weight_matrix(history, length)
    accum = [sum(row[q] for row in matrix) / len(matrix) for q in range(length + 1)]
    demand(abs(sum(accum) - 1.0) <= 1.0e-9, f"L{length}: pbar not normalized")
    return accum


def shortest_interval(weights: list[float]) -> tuple[int, int, float]:
    candidates: list[tuple[int, float, int, int]] = []
    for lower in range(len(weights)):
        mass = 0.0
        for upper in range(lower, len(weights)):
            mass += weights[upper]
            if mass >= 0.99:
                candidates.append((upper - lower, -mass, lower, upper))
    demand(bool(candidates), "no contiguous 99% sector interval")
    width, negative_mass, lower, upper = min(candidates)
    del width
    return lower, upper, -negative_mass


def density_envelope(length: int, lower: int, upper: int) -> tuple[Fraction, Fraction]:
    return max(Fraction(0), Fraction(2 * lower - 1, 4 * length)), min(Fraction(1), Fraction(2 * upper + 1, 4 * length))


def q_at_density(length: int, value: Fraction) -> int:
    shifted = 2 * length * value + Fraction(1, 2)
    charge = shifted.numerator // shifted.denominator
    return min(length, max(0, charge))


def atom_partition(common: tuple[Fraction, Fraction]) -> list[dict[str, object]]:
    lower, upper = common
    demand(lower < upper, "I_acc is empty or boundary-only")
    boundaries = {lower, upper}
    for length in SIZES:
        for q in range(length):
            boundary = Fraction(2 * q + 1, 4 * length)
            if lower < boundary < upper:
                boundaries.add(boundary)
    ordered = sorted(boundaries)
    atoms = []
    for index, (left, right) in enumerate(zip(ordered, ordered[1:])):
        demand(left < right, "non-positive atom width")
        midpoint = (left + right) / 2
        atoms.append({
            "atom_id": f"A{index:03d}",
            "density_interval": [ratio_pair(left), ratio_pair(right)],
            "q_by_L": {str(length): q_at_density(length, midpoint) for length in SIZES},
        })
    return atoms


def validate_manifest(path: Path | None, expected_sha256: str | None) -> dict[str, object]:
    demand(path is not None, "--manifest is required")
    demand(valid_digest(expected_sha256), "--manifest-sha256 must be an explicit lowercase SHA-256")
    path = path.resolve()
    demand(path.is_file(), "manifest file missing")
    demand(sha256(path) == expected_sha256, "manifest SHA-256 mismatch")
    manifest = json.loads(path.read_text())
    demand(manifest.get("schema") == MANIFEST_SCHEMA, "manifest schema mismatch")
    demand(manifest.get("status") == MANIFEST_STATUS, "manifest not authorized for spectrum")
    demand(manifest.get("accumulation_protocol_sha256") == ACCUMULATION_PROTOCOL_SHA256, "accumulation protocol custody mismatch")
    histories = manifest.get("histories")
    demand(isinstance(histories, dict) and set(histories) == {str(x) for x in SIZES}, "manifest must contain exactly L4,L6,L8,L10,L12")
    reconstructed: dict[int, list[float]] = {}
    envelopes: dict[int, tuple[Fraction, Fraction]] = {}
    for length in SIZES:
        entry = histories[str(length)]
        demand(isinstance(entry, dict), f"L{length}: history entry invalid")
        target_path = checked_repo_file(entry.get("target_history_path"), entry.get("target_history_sha256"), f"L{length} target history")
        blind_path = checked_repo_file(entry.get("blind_history_path"), entry.get("blind_history_sha256"), f"L{length} blind history")
        audit_path = checked_repo_file(entry.get("hostile_audit_path"), entry.get("hostile_audit_sha256"), f"L{length} hostile audit")
        demand(entry.get("hostile_verdict") == "PASS", f"L{length}: hostile verdict is not PASS")
        audit_text = audit_path.read_text()
        demand("PASS" in audit_text, f"L{length}: hostile audit lacks a PASS record")
        demand(
            str(entry["target_history_sha256"]) in audit_text and str(entry["blind_history_sha256"]) in audit_text,
            f"L{length}: hostile audit does not bind both history hashes",
        )
        declared_sector_disagreement = entry.get("max_target_blind_sector_weight_difference")
        demand(type(declared_sector_disagreement) in (int, float) and 0.0 <= float(declared_sector_disagreement) <= 1.0e-8, f"L{length}: target/blind sector-weight disagreement exceeds 1e-8")
        declared_observable_disagreement = entry.get("max_target_blind_history_observable_difference")
        demand(type(declared_observable_disagreement) in (int, float) and 0.0 <= float(declared_observable_disagreement) <= 1.0e-8, f"L{length}: target/blind history-observable disagreement exceeds 1e-8")
        target_history = json.loads(target_path.read_text(), parse_float=Decimal)
        blind_history = json.loads(blind_path.read_text(), parse_float=Decimal)
        demand(type(target_history.get("dimension")) is int and int(target_history["dimension"]) > 0, f"L{length}: invalid target dimension")
        demand(target_history.get("dimension") == blind_history.get("dimension"), f"L{length}: target/blind dimension mismatch")
        target_rows = history_event_rows(target_history, length)
        blind_rows = history_event_rows(blind_history, length)
        target_matrix = full_weight_matrix(target_history, length)
        blind_matrix = full_weight_matrix(blind_history, length)
        target_pbar = reconstructed_pbar(target_history, length)
        blind_pbar = reconstructed_pbar(blind_history, length)
        measured_sector = max(
            abs(target_matrix[event][q] - blind_matrix[event][q])
            for event in range(len(target_matrix))
            for q in range(length + 1)
        )
        measured_observable = 0.0
        for event, (target_row, blind_row) in enumerate(zip(target_rows, blind_rows), start=1):
            for field in HISTORY_OBSERVABLE_FIELDS:
                target_value = target_row.get(field)
                blind_value = blind_row.get(field)
                demand(finite_json_number(target_value), f"L{length}: target {field} invalid at event {event}")
                demand(finite_json_number(blind_value), f"L{length}: blind {field} invalid at event {event}")
                measured_observable = max(measured_observable, abs(float(target_value) - float(blind_value)))
        demand(measured_sector <= 1.0e-8, f"L{length}: measured target/blind sector-weight mismatch")
        demand(abs(measured_sector - float(declared_sector_disagreement)) <= 1.0e-12, f"L{length}: declared sector-weight mismatch does not reconstruct")
        demand(measured_observable <= 1.0e-8, f"L{length}: measured target/blind history-observable mismatch")
        demand(abs(measured_observable - float(declared_observable_disagreement)) <= 1.0e-12, f"L{length}: declared history-observable mismatch does not reconstruct")
        declared_pbar = entry.get("pbar_q")
        demand(isinstance(declared_pbar, list) and len(declared_pbar) == length + 1, f"L{length}: pbar_q length")
        demand(all(finite_json_number(value) for value in declared_pbar), f"L{length}: pbar_q contains nonnumeric value")
        demand(max(abs(float(a) - float(b)) for a, b in zip(declared_pbar, target_pbar)) <= 1.0e-12, f"L{length}: pbar_q does not reconstruct")
        lower, upper, _ = shortest_interval(target_pbar)
        blind_lower, blind_upper, _ = shortest_interval(blind_pbar)
        demand((blind_lower, blind_upper) == (lower, upper), f"L{length}: target/blind 99% intervals differ")
        demand(exact_json_equal(entry.get("q_interval"), [lower, upper]), f"L{length}: q_interval does not reconstruct")
        envelope = density_envelope(length, lower, upper)
        declared_envelope = entry.get("density_envelope")
        demand(isinstance(declared_envelope, list) and len(declared_envelope) == 2, f"L{length}: density envelope missing")
        demand((parse_fraction(declared_envelope[0], f"L{length} envelope lower"), parse_fraction(declared_envelope[1], f"L{length} envelope upper")) == envelope, f"L{length}: density envelope mismatch")
        reconstructed[length] = target_pbar
        envelopes[length] = envelope
    common = (max(x[0] for x in envelopes.values()), min(x[1] for x in envelopes.values()))
    demand(common[0] < common[1], "no positive-width L4-L12 common accumulation interval")
    declared_common = manifest.get("I_acc")
    demand(isinstance(declared_common, list) and len(declared_common) == 2, "I_acc missing")
    demand((parse_fraction(declared_common[0], "I_acc lower"), parse_fraction(declared_common[1], "I_acc upper")) == common, "I_acc does not reconstruct")
    expected_atoms = atom_partition(common)
    demand(exact_json_equal(manifest.get("atoms"), expected_atoms), "atom partition/q map is not exact and complete")
    return {
        "manifest": manifest,
        "path": path,
        "sha256": expected_sha256,
        "pbar": reconstructed,
        "common": common,
        "atoms": expected_atoms,
    }


def verify_freeze() -> None:
    demand(FREEZE.is_file(), "FREEZE.json missing")
    freeze = json.loads(FREEZE.read_text())
    demand(freeze.get("schema") == "RELATIONAL_INTERVAL_SPECTRUM_PRE_OUTPUT_FREEZE_V001", "freeze schema mismatch")
    demand(freeze.get("status") == "FROZEN_PRE_OUTPUT__NO_PHYSICAL_SPECTRUM_EXECUTED", "freeze status mismatch")
    demand(freeze.get("physical_spectrum_outputs_present_at_freeze") is False, "freeze does not certify pre-output state")
    demand(
        freeze.get("execution_order_claim_boundary")
        == "AUTHENTICATED_TRUSTED_CODE_PATH_ORDERING_ONLY__NO_ADVERSARY_RESISTANT_WALL_CLOCK_ATTESTATION",
        "freeze execution-order claim boundary mismatch",
    )
    expected_dependencies = {
        str(ACCUMULATION_PROTOCOL.relative_to(ROOT)): ACCUMULATION_PROTOCOL_SHA256,
        str(SEALED_LOW.relative_to(ROOT)): SEALED_LOW_SHA256,
        str(TARGET_ENGINE.relative_to(ROOT)): TARGET_ENGINE_SHA256,
        str(CLASSIFIER.relative_to(ROOT)): CLASSIFIER_SHA256,
    }
    demand(exact_json_equal(freeze.get("dependencies"), expected_dependencies), "freeze dependency census mismatch")
    files = freeze.get("files")
    demand(isinstance(files, dict) and set(files) == {
        "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/PROTOCOL.md",
        "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/execution_credential.py",
        "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/interval_spectrum_driver.py",
        "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/target_interval_worker.py",
        "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/test_execution_credential.py",
    }, "freeze packet-file census mismatch")
    for relative, digest in files.items():
        checked_repo_file(relative, digest, f"freeze {relative}")
    demand(sha256(ACCUMULATION_PROTOCOL) == ACCUMULATION_PROTOCOL_SHA256, "upstream accumulation protocol changed")
    demand(sha256(SEALED_LOW) == SEALED_LOW_SHA256, "sealed low-size spectra changed")
    demand(sha256(TARGET_ENGINE) == TARGET_ENGINE_SHA256, "target spectrum engine changed")
    demand(sha256(TARGET_WORKER) == TARGET_WORKER_SHA256, "target interval adapter changed")
    demand(sha256(CREDENTIAL_CONTROL) == CREDENTIAL_CONTROL_SHA256, "target execution credential control changed")
    demand(sha256(CLASSIFIER) == CLASSIFIER_SHA256, "frozen classifier changed")


def validate_large_row(row: dict[str, object], length: int, charge: int) -> list[str]:
    errors: list[str] = []
    def row_check(condition: bool, label: str) -> None:
        if not condition:
            errors.append(label)
    integer_fields = (
        "L",
        "q",
        "sector_dimension",
        "translation_orbits",
        "ground_block_dimension",
        "ground_block_nnz",
        "response_block_dimension",
        "response_block_nnz",
        "ground_matvecs",
        "response_matvecs",
        "total_matvecs",
        "max_rss_bytes",
    )
    real_fields = (
        "rho",
        "wall_seconds",
        "ground_energy",
        "ground_residual",
        "ground_block_hermiticity_error",
        "ground_krylov_orthogonality",
        "response_full_norm_squared",
        "response_projected_norm_squared",
        "response_projection_error",
        "active_actual_residual",
        "Delta_act",
        "chi_tau",
        "R_low",
        "response_block_hermiticity_error",
        "response_krylov_orthogonality",
    )
    for field in integer_fields:
        row_check(type(row.get(field)) is int and int(row[field]) >= 0, f"{field} exact nonnegative integer")
    for field in real_fields:
        row_check(finite_json_number(row.get(field)), f"{field} exact finite number")
    for field in set(real_fields) - {"ground_energy"}:
        if finite_json_number(row.get(field)):
            row_check(float(row[field]) >= 0.0, f"{field} nonnegative")
    for field in ("response_full_norm_squared", "response_projected_norm_squared", "Delta_act", "chi_tau", "R_low"):
        if finite_json_number(row.get(field)):
            row_check(float(row[field]) > 0.0, f"{field} strictly positive")
    if finite_json_number(row.get("R_low")):
        row_check(float(row["R_low"]) <= 1.0 + 1.0e-12, "R_low probability upper bound")
    for sequence_name in ("ground_sequence", "response_sequence"):
        sequence = row.get(sequence_name)
        row_check(isinstance(sequence, list) and bool(sequence), f"{sequence_name} missing")
        if not isinstance(sequence, list):
            continue
        dimensions = []
        for index, checkpoint in enumerate(sequence):
            prefix = f"{sequence_name}[{index}]"
            row_check(isinstance(checkpoint, dict), f"{prefix} checkpoint object")
            if not isinstance(checkpoint, dict):
                continue
            row_check(type(checkpoint.get("krylov_dimension")) is int, f"{prefix} Krylov dimension exact integer")
            if type(checkpoint.get("krylov_dimension")) is int:
                dimensions.append(checkpoint["krylov_dimension"])
            values = checkpoint.get("lowest_five_ritz_values")
            row_check(isinstance(values, list) and all(finite_json_number(value) for value in values), f"{prefix} lowest-five exact finite numbers")
            if sequence_name == "ground_sequence":
                for field in ("energy", "residual_estimate"):
                    row_check(finite_json_number(checkpoint.get(field)), f"{prefix} {field} exact finite number")
                if finite_json_number(checkpoint.get("residual_estimate")):
                    row_check(float(checkpoint["residual_estimate"]) >= 0.0, f"{prefix} residual estimate nonnegative")
            else:
                for field in ("Delta_act", "R_low", "active_residual_estimate", "chi_tau", "total_weight", "weight_floor"):
                    row_check(finite_json_number(checkpoint.get(field)), f"{prefix} {field} exact finite number")
                    if finite_json_number(checkpoint.get(field)):
                        row_check(float(checkpoint[field]) >= 0.0, f"{prefix} {field} nonnegative")
                for field in ("Delta_act", "R_low", "chi_tau", "total_weight", "weight_floor"):
                    if finite_json_number(checkpoint.get(field)):
                        row_check(float(checkpoint[field]) > 0.0, f"{prefix} {field} strictly positive")
                if finite_json_number(checkpoint.get("R_low")):
                    row_check(float(checkpoint["R_low"]) <= 1.0 + 1.0e-12, f"{prefix} R_low probability upper bound")
                row_check(type(checkpoint.get("active_ritz_index")) is int, f"{prefix} active index exact integer")
                threshold_indices = checkpoint.get("threshold_indices")
                threshold_identity = (
                    isinstance(threshold_indices, list)
                    and len(threshold_indices) == 3
                    and all(type(value) is int and value >= 0 for value in threshold_indices)
                    and len(set(threshold_indices)) == 1
                    and type(checkpoint.get("active_ritz_index")) is int
                    and all(value == checkpoint["active_ritz_index"] for value in threshold_indices)
                )
                row_check(threshold_identity, f"{prefix} threshold-index identity")
                row_check(checkpoint.get("resolved") is True, f"{prefix} resolved checkpoint")
                row_check(type(checkpoint.get("threshold_stable")) is bool, f"{prefix} threshold stability exact Boolean")
                if type(checkpoint.get("threshold_stable")) is bool:
                    row_check(checkpoint["threshold_stable"] is threshold_identity, f"{prefix} threshold stability reconstruction")
                if finite_json_number(row.get("response_projected_norm_squared")) and all(
                    finite_json_number(checkpoint.get(field)) for field in ("total_weight", "weight_floor", "active_residual_estimate")
                ):
                    row_check(
                        relative_difference(float(checkpoint["total_weight"]), float(row["response_projected_norm_squared"])) <= 1.0e-12,
                        f"{prefix} total-weight reconstruction",
                    )
                    reconstructed_floor = max(
                        1.0e-12 * float(checkpoint["total_weight"]),
                        100.0 * float(checkpoint["active_residual_estimate"]) ** 2 * float(row["response_projected_norm_squared"]),
                    )
                    row_check(
                        relative_difference(float(checkpoint["weight_floor"]), reconstructed_floor) <= 1.0e-12,
                        f"{prefix} weight-floor reconstruction",
                    )
                    row_check(
                        float(checkpoint["R_low"]) * float(checkpoint["total_weight"])
                        > 10.0 * float(checkpoint["weight_floor"]),
                        f"{prefix} threshold-support feasibility",
                    )
        if len(dimensions) == len(sequence) and dimensions:
            expected_dimensions = sorted({value for value in KRYLOV_CHECKPOINTS if value <= dimensions[-1]} | {dimensions[-1]})
            row_check(dimensions == expected_dimensions, f"{sequence_name} checkpoint census")
    convergence = row.get("response_convergence")
    row_check(isinstance(convergence, dict), "response convergence object")
    if isinstance(convergence, dict):
        row_check(type(convergence.get("resolved")) is bool, "response convergence resolved exact Boolean")
        for field in ("Delta_act_relative", "chi_tau_relative", "R_low_relative"):
            if field in convergence:
                row_check(finite_json_number(convergence[field]), f"response convergence {field} exact finite number")
        if "exact_krylov_termination" in convergence:
            row_check(type(convergence["exact_krylov_termination"]) is bool, "response exact-termination exact Boolean")
    if errors:
        return errors
    row_check(int(row.get("L", -1)) == length and int(row.get("q", -1)) == charge, "sector identity")
    row_check(1 <= charge <= length, "positive half-sector charge")
    row_check(relative_difference(float(row.get("rho", math.inf)), charge / (2 * length)) <= 1.0e-15, "density identity")
    row_check(int(row["sector_dimension"]) == math.comb(2 * length, charge), "sector-dimension reconstruction")
    row_check(0 < int(row["translation_orbits"]) <= int(row["sector_dimension"]), "translation-orbit bounds")
    for prefix in ("ground", "response"):
        dimension = int(row[f"{prefix}_block_dimension"])
        nonzeros = int(row[f"{prefix}_block_nnz"])
        row_check(0 < dimension <= int(row["translation_orbits"]), f"{prefix} block-dimension bounds")
        row_check(dimension <= nonzeros <= dimension * dimension, f"{prefix} block-nnz bounds")
    row_check(row.get("status") == "RESOLVED", "row unresolved")
    row_check(isinstance(row.get("unresolved_reasons"), list) and not row["unresolved_reasons"], "unresolved reason list")
    row_check(int(row["ground_matvecs"]) + int(row["response_matvecs"]) == int(row["total_matvecs"]), "matvec total reconstruction")
    row_check(int(row["ground_matvecs"]) == int(row["ground_sequence"][-1]["krylov_dimension"]), "ground matvec/checkpoint reconstruction")
    row_check(int(row["response_matvecs"]) == int(row["response_sequence"][-1]["krylov_dimension"]), "response matvec/checkpoint reconstruction")
    row_check(int(row.get("total_matvecs", MAX_MATVECS + 1)) <= MAX_MATVECS, "matvec guard")
    row_check(float(row.get("wall_seconds", math.inf)) <= MAX_SECTOR_SECONDS, "wall guard")
    row_check(int(row.get("max_rss_bytes", MAX_SECTOR_RSS + 1)) <= MAX_SECTOR_RSS, "RSS guard")
    row_check(float(row.get("ground_residual", math.inf)) <= 1.0e-9, "ground residual")
    row_check(float(row.get("active_actual_residual", math.inf)) <= 1.0e-9, "active residual")
    row_check(float(row.get("ground_block_hermiticity_error", math.inf)) <= 1.0e-12, "ground Hermiticity")
    row_check(float(row.get("response_block_hermiticity_error", math.inf)) <= 1.0e-12, "response Hermiticity")
    row_check(float(row.get("ground_krylov_orthogonality", math.inf)) <= 1.0e-10, "ground orthogonality")
    row_check(float(row.get("response_krylov_orthogonality", math.inf)) <= 1.0e-10, "response orthogonality")
    row_check(float(row.get("response_projection_error", math.inf)) <= 1.0e-9, "projection closure")
    reconstructed_projection_error = abs(float(row["response_full_norm_squared"]) - float(row["response_projected_norm_squared"]))
    row_check(abs(float(row["response_projection_error"]) - reconstructed_projection_error) <= 1.0e-12, "projection-error reconstruction")
    row_check(row.get("threshold_stable") is True, "threshold stability")
    row_check(float(row.get("R_low", 0.0) or 0.0) >= 1.0e-6, "low-pole residue")
    convergence = row.get("response_convergence", {})
    row_check(isinstance(convergence, dict) and convergence.get("resolved") is True, "response convergence")
    ground_sequence = row.get("ground_sequence")
    response_sequence = row.get("response_sequence")
    if isinstance(ground_sequence, list) and ground_sequence:
        if len(ground_sequence) >= 2:
            ground_drift = relative_difference(float(ground_sequence[-1]["energy"]), float(ground_sequence[-2]["energy"]))
            row_check(ground_drift <= 2.0e-10, "ground last-pair stability")
        else:
            row_check(
                int(row["ground_matvecs"]) == int(ground_sequence[-1]["krylov_dimension"]) < MAX_KRYLOV,
                "ground exact-termination evidence",
            )
            row_check(float(row.get("ground_residual", math.inf)) <= 1.0e-9, "ground exact-termination residual")
        row_check(abs(float(row.get("ground_energy", math.inf)) - float(ground_sequence[-1]["energy"])) <= 1.0e-9, "top-level ground reconstruction")
    else:
        row_check(False, "ground last-pair unavailable")
    if isinstance(response_sequence, list) and response_sequence:
        final_response = response_sequence[-1]
        row_check(row.get("threshold_stable") is final_response.get("threshold_stable"), "top-level threshold reconstruction")
        if len(response_sequence) >= 2:
            previous_response = response_sequence[-2]
            reconstructed_drifts = {
                "Delta_act_relative": relative_difference(float(final_response["Delta_act"]), float(previous_response["Delta_act"])),
                "chi_tau_relative": relative_difference(float(final_response["chi_tau"]), float(previous_response["chi_tau"])),
                "R_low_relative": relative_difference(float(final_response["R_low"]), float(previous_response["R_low"])),
            }
            row_check(reconstructed_drifts["Delta_act_relative"] <= 2.0e-7, "Delta last-pair stability")
            row_check(reconstructed_drifts["chi_tau_relative"] <= 2.0e-7, "chi last-pair stability")
            row_check(reconstructed_drifts["R_low_relative"] <= 2.0e-6, "R_low last-pair stability")
            if isinstance(convergence, dict):
                for key, observed in reconstructed_drifts.items():
                    row_check(abs(float(convergence.get(key, math.inf)) - observed) <= 1.0e-12, f"reported {key} reconstruction")
        else:
            row_check(isinstance(convergence, dict) and convergence.get("exact_krylov_termination") is True, "response exact-termination marker")
            row_check(
                int(row["response_matvecs"]) == int(final_response["krylov_dimension"]) < MAX_KRYLOV,
                "response exact-termination evidence",
            )
            row_check(float(row.get("active_actual_residual", math.inf)) <= 1.0e-9, "response exact-termination residual")
        for key in ("Delta_act", "chi_tau", "R_low"):
            row_check(abs(float(row.get(key, math.inf)) - float(final_response[key])) <= 1.0e-9, f"top-level {key} reconstruction")
    else:
        row_check(False, "response last-pair unavailable")
    for sequence_name in ("ground_sequence", "response_sequence"):
        sequence = row.get(sequence_name)
        row_check(isinstance(sequence, list) and bool(sequence), f"{sequence_name} missing")
        if not isinstance(sequence, list):
            continue
        for index, checkpoint in enumerate(sequence):
            values = checkpoint.get("lowest_five_ritz_values") if isinstance(checkpoint, dict) else None
            prefix = f"{sequence_name}[{index}]"
            row_check(0 < int(checkpoint.get("krylov_dimension", -1)) <= MAX_KRYLOV, f"{prefix} Krylov dimension")
            row_check(isinstance(values, list), f"{prefix} lowest-five missing")
            if not isinstance(values, list):
                continue
            row_check(len(values) == min(5, int(checkpoint.get("krylov_dimension", -1))), f"{prefix} lowest-five count")
            row_check(all(finite_json_number(x) for x in values), f"{prefix} lowest-five finite")
            row_check(all(float(a) <= float(b) for a, b in zip(values, values[1:])), f"{prefix} lowest-five ordered")
            if values:
                if sequence_name == "ground_sequence":
                    expected = float(checkpoint.get("energy", math.inf))
                    actual = float(values[0])
                else:
                    active = int(checkpoint.get("active_ritz_index", -1))
                    row_check(0 <= active < len(values), f"{prefix} active index not retained")
                    if not 0 <= active < len(values):
                        continue
                    expected = float(row.get("ground_energy", math.inf)) + float(checkpoint.get("Delta_act", math.inf))
                    actual = float(values[active])
                row_check(abs(actual - expected) <= 1.0e-9, f"{prefix} pole reconstruction")
        if sequence:
            final = sequence[-1]
            row_check(
                len(final.get("lowest_five_ritz_values", [])) == min(5, int(final.get("krylov_dimension", -1))),
                f"{sequence_name} final lowest-five",
            )
    return errors


def selected_large_pairs(atoms: list[dict[str, object]]) -> list[tuple[int, int]]:
    return sorted({
        (length, int(atom["q_by_L"][str(length)]))
        for atom in atoms
        for length in LARGE_SIZES
        if int(atom["q_by_L"][str(length)]) > 0
    })


def checked_external_file(path: Path | None, digest: str | None, label: str) -> Path:
    demand(path is not None and path.is_file(), f"{label}: file missing")
    demand(valid_digest(digest) and sha256(path) == digest, f"{label}: SHA-256 mismatch")
    return path.resolve()


def validate_blind_freeze(path: Path | None, digest: str | None, manifest_sha: str, pairs: list[tuple[int, int]]) -> dict[str, object]:
    freeze_path = checked_external_file(path, digest, "blind method freeze")
    demand(freeze_path.is_relative_to(ROOT.resolve()), "blind method freeze must be repository-relative")
    freeze = json.loads(freeze_path.read_text())
    demand(freeze.get("schema") == "RELATIONAL_INTERVAL_BLIND_METHOD_FREEZE_V001", "blind freeze schema mismatch")
    demand(freeze.get("status") == "BLIND_METHOD_FROZEN_BEFORE_TARGET_SPECTRUM", "blind method was not frozen before target")
    demand(freeze.get("manifest_sha256") == manifest_sha, "blind freeze manifest binding mismatch")
    demand(freeze.get("target_code_or_matrices_imported") is False, "blind method imports target bytes")
    demand(freeze.get("planned_sectors") == [list(pair) for pair in pairs], "blind freeze sector plan mismatch")
    implementation = checked_repo_file(freeze.get("implementation_path"), freeze.get("implementation_sha256"), "blind implementation")
    demand(sha256(implementation) not in {TARGET_ENGINE_SHA256, TARGET_WORKER_SHA256}, "blind implementation is target code")
    return freeze


def credential_expectations() -> dict[str, tuple[Path, str]]:
    return {
        "worker": (TARGET_WORKER, TARGET_WORKER_SHA256),
        "driver": (Path(__file__).resolve(), sha256(Path(__file__).resolve())),
        "engine": (TARGET_ENGINE, TARGET_ENGINE_SHA256),
        "control": (CREDENTIAL_CONTROL, CREDENTIAL_CONTROL_SHA256),
        "target_freeze": (FREEZE, sha256(FREEZE)),
    }


def validate_target_execution_binding(
    row: dict[str, object], pair: tuple[int, int], output: Path,
    credential_path: Path, credential_sha256: str,
) -> dict[str, object]:
    control = load_credential_control()
    expected = credential_expectations()
    try:
        binding = control.validate_execution_credential(
            ROOT,
            credential_path,
            credential_sha256,
            pair[0],
            pair[1],
            output,
            expected["worker"],
            expected["driver"],
            expected["engine"],
            expected["control"],
            expected["target_freeze"],
            EXECUTION_TOKEN,
        )
    except control.CredentialRefusal as error:
        raise FailClosed(f"L{pair[0]}q{pair[1]}: target execution credential: {error}") from error
    demand(
        exact_json_equal(row.get("execution_authorization"), binding),
        f"L{pair[0]}q{pair[1]}: row execution-authorization binding",
    )
    return binding


def process_rss_bytes(pid: int) -> int:
    completed = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True, check=False)
    demand(completed.returncode == 0 and bool(completed.stdout.strip()), f"live RSS telemetry unavailable for pid {pid}")
    try:
        return int(completed.stdout.strip().splitlines()[-1]) * 1024
    except ValueError as error:
        raise FailClosed(f"invalid live RSS telemetry for pid {pid}") from error


def execute_target(
    validated: dict[str, object],
    output_dir: Path,
    authorization: str | None,
    blind_freeze: Path | None,
    blind_freeze_sha256: str | None,
) -> None:
    demand(authorization == EXECUTION_TOKEN, "physical spectrum execution token absent")
    resolved_output = output_dir.resolve()
    demand(resolved_output.is_relative_to(HERE), "target output must remain inside this packet")
    demand(not resolved_output.exists() or not any(resolved_output.iterdir()), "target output directory must be absent or empty")
    raw_dir = resolved_output / "RAW"
    authorization_dir = resolved_output / "AUTHORIZATION"
    pairs = selected_large_pairs(validated["atoms"])
    blind_freeze_record = validate_blind_freeze(
        blind_freeze, blind_freeze_sha256, validated["sha256"], pairs,
    )
    raw_dir.mkdir(parents=True, exist_ok=True)
    authorization_dir.mkdir(parents=True, exist_ok=True)

    control = load_credential_control()
    expected = credential_expectations()
    authority_paths = {
        "manifest": validated["path"],
        "sector_plan": ROOT / str(blind_freeze_record["sector_plan_path"]),
        "blind_method_freeze": blind_freeze.resolve(),
        "blind_source_freeze": ROOT / str(blind_freeze_record["source_freeze_path"]),
        "target_source_freeze": FREEZE,
        "target_driver": Path(__file__).resolve(),
        "target_worker": TARGET_WORKER,
        "target_engine": TARGET_ENGINE,
        "credential_control": CREDENTIAL_CONTROL,
    }
    credentials: dict[tuple[int, int], tuple[Path, str]] = {}
    for length, charge in pairs:
        physical_output = raw_dir / f"SECTOR_L{length}_Q{charge}.json"
        credential_path = authorization_dir / f"SECTOR_L{length}_Q{charge}.json"
        try:
            credential_sha256 = control.issue_execution_credential(
                ROOT,
                credential_path,
                length,
                charge,
                physical_output,
                authority_paths,
                expected["worker"],
                expected["driver"],
                expected["engine"],
                expected["control"],
                expected["target_freeze"],
                EXECUTION_TOKEN,
            )
        except control.CredentialRefusal as error:
            raise FailClosed(
                f"L{length}q{charge}: execution credential refusal: {error}"
            ) from error
        credentials[(length, charge)] = (credential_path, credential_sha256)

    completed_rows = []
    for start in range(0, len(pairs), MAX_PARALLEL_WORKERS):
        wave = pairs[start:start + MAX_PARALLEL_WORKERS]
        environment = os.environ.copy()
        environment.update({"VECLIB_MAXIMUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1"})
        processes = []
        try:
            for length, charge in wave:
                output = raw_dir / f"SECTOR_L{length}_Q{charge}.json"
                credential_path, credential_sha256 = credentials[(length, charge)]
                process = subprocess.Popen(
                    [
                        sys.executable, "-B", str(TARGET_WORKER),
                        "--L", str(length), "--q", str(charge),
                        "--credential", str(credential_path),
                        "--credential-sha256", credential_sha256,
                        "--output", str(output),
                    ],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=environment,
                )
                processes.append(((length, charge), output, process, time.monotonic()))
            while any(process.poll() is None for _, _, process, _ in processes):
                live = [(process, started) for _, _, process, started in processes if process.poll() is None]
                rss = []
                for process, _ in live:
                    try:
                        rss.append(process_rss_bytes(process.pid))
                    except FailClosed:
                        if process.poll() is None:
                            raise
                        rss.append(0)
                over_wall = any(time.monotonic() - started > MAX_SECTOR_SECONDS for _, started in live)
                if any(value > MAX_SECTOR_RSS for value in rss) or sum(rss) > MAX_WAVE_RSS or over_wall:
                    raise FailClosed("live spectrum resource guard exceeded")
                time.sleep(0.1)
        except BaseException:
            for _, _, process, _ in processes:
                if process.poll() is None:
                    process.kill()
            for _, _, process, _ in processes:
                process.wait()
            raise
        results = []
        for pair, output, process, _ in processes:
            stdout, stderr = process.communicate()
            demand(process.returncode == 0 and output.is_file(), f"L{pair[0]}q{pair[1]}: worker failed: {(stderr or stdout)[-500:]}")
            row = json.loads(output.read_text())
            errors = validate_large_row(row, *pair)
            demand(not errors, f"L{pair[0]}q{pair[1]}: " + "; ".join(errors))
            credential_path, credential_sha256 = credentials[pair]
            validate_target_execution_binding(
                row, pair, output, credential_path, credential_sha256,
            )
            results.append((pair, output, row))
        demand(sum(int(row["max_rss_bytes"]) for _, _, row in results) <= MAX_WAVE_RSS, "wave peak-RSS sum guard")
        completed_rows.extend(results)
    index = {
        "schema": "RELATIONAL_INTERVAL_SPECTRUM_INDEX_V001",
        "role": "target",
        "manifest_sha256": validated["sha256"],
        "worker_sha256": TARGET_WORKER_SHA256,
        "engine_sha256": TARGET_ENGINE_SHA256,
        "blind_method_freeze_path": str(blind_freeze.resolve().relative_to(ROOT.resolve())),
        "blind_method_freeze_sha256": blind_freeze_sha256,
        "rows": {f"{length}:{charge}": {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)} for (length, charge), path, _ in completed_rows},
        "execution_authorizations": {
            f"{length}:{charge}": {
                "path": str(path.relative_to(ROOT)), "sha256": digest,
            }
            for (length, charge), (path, digest) in credentials.items()
        },
        "status": "TARGET_COMPLETE__INDEPENDENT_BLIND_AND_ADJUDICATION_REQUIRED",
        "claim_boundary": "FINITE_NUMERICAL_TARGET_ROWS_ONLY__NO_PROMOTION",
    }
    (resolved_output / "SPECTRUM_INDEX.json").write_text(json.dumps(index, indent=2, sort_keys=True) + "\n")
    print(index["status"])


def load_index(path: Path | None, digest: str | None, role: str, manifest_sha: str, pairs: list[tuple[int, int]]) -> tuple[dict[tuple[int, int], dict[str, object]], dict[str, object], dict[tuple[int, int], str]]:
    demand(path is not None and valid_digest(digest), f"{role} index path and SHA-256 required")
    demand(path.is_file() and sha256(path) == digest, f"{role} index custody mismatch")
    index = json.loads(path.read_text())
    demand(index.get("schema") == "RELATIONAL_INTERVAL_SPECTRUM_INDEX_V001", f"{role} index schema")
    demand(index.get("role") == role and index.get("manifest_sha256") == manifest_sha, f"{role} index binding")
    expected_status = (
        "TARGET_COMPLETE__INDEPENDENT_BLIND_AND_ADJUDICATION_REQUIRED"
        if role == "target"
        else "BLIND_COMPLETE__READY_FOR_HOSTILE_ADJUDICATION"
    )
    demand(index.get("status") == expected_status, f"{role} index status")
    if role == "target":
        demand(index.get("worker_sha256") == TARGET_WORKER_SHA256, "target index adapter custody")
        demand(index.get("engine_sha256") == TARGET_ENGINE_SHA256, "target index engine custody")
        validate_blind_freeze(
            ROOT / str(index["blind_method_freeze_path"]),
            index.get("blind_method_freeze_sha256"),
            manifest_sha,
            pairs,
        )
        authorization_entries = index.get("execution_authorizations")
        demand(
            isinstance(authorization_entries, dict)
            and set(authorization_entries) == {f"{a}:{b}" for a, b in pairs},
            "target index execution-authorization census mismatch",
        )
    else:
        freeze_path = checked_repo_file(index.get("method_freeze_path"), index.get("method_freeze_sha256"), "blind index method freeze")
        freeze = validate_blind_freeze(freeze_path, index.get("method_freeze_sha256"), manifest_sha, pairs)
        implementation = checked_repo_file(index.get("implementation_path"), index.get("implementation_sha256"), "blind index implementation")
        demand(index.get("implementation_path") == freeze.get("implementation_path"), "blind index/freeze implementation path mismatch")
        demand(index.get("implementation_sha256") == freeze.get("implementation_sha256"), "blind index/freeze implementation hash mismatch")
        demand(sha256(implementation) not in {TARGET_ENGINE_SHA256, TARGET_WORKER_SHA256}, "blind index implementation is target code")
    rows = index.get("rows")
    demand(isinstance(rows, dict) and set(rows) == {f"{a}:{b}" for a, b in pairs}, f"{role} index sector set mismatch")
    loaded = {}
    digests = {}
    target_authorizations: list[dict[str, object]] = []
    for pair in pairs:
        entry = rows[f"{pair[0]}:{pair[1]}"]
        row_path = checked_repo_file(entry.get("path"), entry.get("sha256"), f"{role} L{pair[0]}q{pair[1]}")
        row = json.loads(row_path.read_text())
        errors = validate_large_row(row, *pair)
        demand(not errors, f"{role} L{pair[0]}q{pair[1]}: " + "; ".join(errors))
        if role == "target":
            entry = index["execution_authorizations"][f"{pair[0]}:{pair[1]}"]
            demand(
                isinstance(entry, dict) and set(entry) == {"path", "sha256"},
                f"target L{pair[0]}q{pair[1]} execution-authorization entry",
            )
            credential_path = checked_repo_file(
                entry.get("path"), entry.get("sha256"),
                f"target L{pair[0]}q{pair[1]} execution authorization",
            )
            target_authorizations.append(
                validate_target_execution_binding(
                    row, pair, row_path, credential_path, str(entry["sha256"]),
                )
            )
        loaded[pair] = row
        digests[pair] = str(entry["sha256"])
    if role == "target":
        demand(
            len({str(item["authorization_nonce"]) for item in target_authorizations})
            == len(pairs),
            "target execution-authorization nonce reuse",
        )
        demand(
            len({str(item["credential_sha256"]) for item in target_authorizations})
            == len(pairs),
            "target execution-authorization credential reuse",
        )
    return loaded, index, digests


def load_classifier():
    spec = importlib.util.spec_from_file_location("frozen_interval_classifier", CLASSIFIER)
    demand(spec is not None and spec.loader is not None, "cannot load frozen classifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compare_classifications(left: dict[str, object], right: dict[str, object], label: str) -> None:
    demand(exact_json_equal(left.get("checks"), right.get("checks")), f"{label}: Boolean decisions mismatch")
    demand(exact_json_equal(left.get("passes"), right.get("passes")), f"{label}: aggregate decision mismatch")
    demand(exact_json_equal(left.get("classification"), right.get("classification")), f"{label}: classification mismatch")
    for key in (
        "chi_power_exponent_y",
        "fixed_z1_heldout_sse_relative",
        "gapless_heldout_sse_relative",
        "positive_gap_heldout_sse_relative",
        "tail_scaled_gap_relative_range",
        "tail_scaled_chi_relative_range",
        "tail_residue_relative_range",
    ):
        demand(numeric_match(left[key], right[key], 1.0e-9), f"{label}: {key} mismatch")
    for key in ("L_times_Delta", "chi_over_L"):
        demand(len(left[key]) == len(right[key]), f"{label}: {key} length mismatch")
        for index, (a, b) in enumerate(zip(left[key], right[key])):
            demand(numeric_match(a, b, 1.0e-9), f"{label}: {key}[{index}] mismatch")
    for fit_name, fit_keys in (
        ("gap_power_fit", ("amplitude", "exponent")),
        ("fixed_z1_fit", ("amplitude", "correction", "training_sse")),
    ):
        demand(left[fit_name].get("fit_status") == right[fit_name].get("fit_status"), f"{label}: {fit_name} status mismatch")
        if left[fit_name].get("fit_status", "RESOLVED") == "RESOLVED":
            for key in fit_keys:
                demand(numeric_match(left[fit_name][key], right[fit_name][key], 1.0e-9), f"{label}: {fit_name}.{key} mismatch")
    for family in ("fixed_z1_heldout_rows", "gapless_heldout_rows", "positive_gap_heldout_rows"):
        demand(len(left[family]) == len(right[family]), f"{label}: {family} length mismatch")
        for index, (a, b) in enumerate(zip(left[family], right[family])):
            demand(type(a.get("held_L")) is int and type(b.get("held_L")) is int and a["held_L"] == b["held_L"], f"{label}: {family}[{index}] size mismatch")
            for key in ("observed", "predicted", "relative_error"):
                demand(numeric_match(a[key], b[key], 1.0e-8), f"{label}: {family}[{index}].{key} mismatch")


def adjacent_pair(values: set[int]) -> bool:
    return any(value + 1 in values for value in values)


def adjudicate(validated: dict[str, object], target_index: Path | None, target_sha: str | None, blind_index: Path | None, blind_sha: str | None, output: Path) -> None:
    pairs = selected_large_pairs(validated["atoms"])
    target, target_metadata, target_digests = load_index(target_index, target_sha, "target", validated["sha256"], pairs)
    blind, blind_metadata, blind_digests = load_index(blind_index, blind_sha, "blind", validated["sha256"], pairs)
    demand(
        target_metadata.get("blind_method_freeze_sha256") == blind_metadata.get("method_freeze_sha256"),
        "target and blind indices do not share the pre-target blind-method freeze",
    )
    demand(
        target_metadata.get("blind_method_freeze_path") == blind_metadata.get("method_freeze_path"),
        "target and blind indices name different blind-method freezes",
    )
    low = json.loads(SEALED_LOW.read_text())
    low_rows = {(int(row["L"]), int(row["q"])): row for group in low["sector_rows"].values() for row in group}
    classifier = load_classifier()
    blind_atom_payload = blind_metadata.get("atom_classifications")
    demand(
        isinstance(blind_atom_payload, dict)
        and set(blind_atom_payload) == {str(atom["atom_id"]) for atom in validated["atoms"]},
        "blind index does not contain the complete independent atom classification census",
    )
    atom_results = []
    for atom in validated["atoms"]:
        qmap = {int(k): int(v) for k, v in atom["q_by_L"].items()}
        differences = {}
        failures = []
        target_rows = []
        blind_rows = []
        for length in SIZES:
            charge = qmap[length]
            if charge == 0:
                failures.append(f"L{length}q0: ZERO_RESPONSE_NORM__ATOM_NONPASSING")
                continue
            if length <= 8:
                row = low_rows[(length, charge)]
                if not all(finite_json_number(row.get(key)) for key in ("Delta_act", "chi_tau", "R_low")):
                    failures.append(f"L{length}q{charge}: low-size response unresolved")
                normalized = {"L": length, "rho_anchor": charge / (2 * length), "source_q": [charge], "weights": [1.0], **{key: row.get(key) for key in ("Delta_act", "chi_tau", "R_low")}}
                target_rows.append(normalized)
                blind_rows.append(dict(normalized))
                continue
            left, right = target[(length, charge)], blind[(length, charge)]
            for key in ("L", "q", "rho", "sector_dimension", "translation_orbits", "ground_block_dimension", "ground_block_nnz", "response_block_dimension", "response_block_nnz"):
                demand(left.get(key) == right.get(key), f"L{length}q{charge}: target/blind {key} identity mismatch")
            limits = {
                "ground_energy": 2.0e-8,
                "Delta_act": 2.0e-8,
                "chi_tau": 5.0e-7,
                "R_low": 5.0e-6,
                "response_full_norm_squared": 2.0e-8,
            }
            differences[str(length)] = {}
            for key, limit in limits.items():
                difference = relative_difference(float(left[key]), float(right[key]))
                differences[str(length)][key] = difference
                demand(difference <= limit, f"L{length}q{charge}: target/blind {key} mismatch")
            floor_difference = relative_difference(
                float(left["response_sequence"][-1]["weight_floor"]),
                float(right["response_sequence"][-1]["weight_floor"]),
            )
            differences[str(length)]["weight_floor"] = floor_difference
            demand(floor_difference <= 2.0e-8, f"L{length}q{charge}: target/blind weight_floor mismatch")
            common = {"L": length, "rho_anchor": charge / (2 * length), "source_q": [charge], "weights": [1.0]}
            target_rows.append({**common, **{key: float(left[key]) for key in ("Delta_act", "chi_tau", "R_low")}})
            blind_rows.append({**common, **{key: float(right[key]) for key in ("Delta_act", "chi_tau", "R_low")}})
        classification = None
        blind_classification = None
        independent_payload = blind_atom_payload[str(atom["atom_id"])]
        demand(isinstance(independent_payload, dict), f"{atom['atom_id']}: blind classification payload invalid")
        if not failures:
            classification = classifier.classify(target_rows)
            blind_classification = classifier.classify(blind_rows)
            demand(independent_payload.get("status") == "RESOLVED", f"{atom['atom_id']}: blind classification unresolved")
            declared_blind = independent_payload.get("classification")
            demand(isinstance(declared_blind, dict), f"{atom['atom_id']}: blind classification missing")
            compare_classifications(classification, blind_classification, f"{atom['atom_id']} target/blind reconstruction")
            compare_classifications(blind_classification, declared_blind, f"{atom['atom_id']} blind independent payload")
            if not classification["passes"]:
                failures.append("preregistered z=1 conjunction rejected")
        else:
            demand(
                independent_payload.get("status") == "ZERO_RESPONSE_NORM__ATOM_NONPASSING"
                and independent_payload.get("classification") is None,
                f"{atom['atom_id']}: blind zero-response disposition mismatch",
            )
        atom_results.append({"atom": atom, "passes": not failures, "failures": failures, "target_blind_relative_differences": differences, "target_classification": classification, "blind_classification": blind_classification})

    components = []
    current = []
    for index, result in enumerate(atom_results + [{"passes": False}]):
        if result["passes"]:
            current.append(index)
        elif current:
            charges = {length: {int(validated["atoms"][i]["q_by_L"][str(length)]) for i in current} for length in SIZES}
            masses = {str(length): sum(validated["pbar"][length][q] for q in charges[length]) for length in SIZES}
            qualifies = adjacent_pair(charges[10]) and adjacent_pair(charges[12]) and all(value >= 0.50 for value in masses.values())
            components.append({"atom_indices": current, "q_by_L": {str(k): sorted(v) for k, v in charges.items()}, "pbar_mass_by_L": masses, "qualifies": qualifies})
            current = []
    candidate = any(component["qualifies"] for component in components)
    disposition = "AUTHENTICATED_RELATIONAL_Z1_INTERVAL_CANDIDATE" if candidate else "AUTHENTICATED_RELATIONAL_Z1_REJECTED_L4_L12"
    result = {
        "schema": "RELATIONAL_INTERVAL_SPECTRUM_ADJUDICATION_V001",
        "manifest_sha256": validated["sha256"],
        "target_index_sha256": target_sha,
        "blind_index_sha256": blind_sha,
        "classification": disposition,
        "atom_results": atom_results,
        "passing_components": components,
        "claim_boundary": {"empirical": "FINITE_AUTHENTICATED_INTERVAL_RESPONSE_ONLY", "not_claimed": ["THERMODYNAMIC_PHASE", "EXACT_Z1", "CONTINUUM", "METRIC", "UNIVERSAL_COUPLING", "EMERGENCE", "GRAVITY"]},
    }
    resolved_output = output.resolve()
    demand(resolved_output.is_relative_to(HERE), "adjudication output must remain inside this packet")
    demand(not resolved_output.exists(), "adjudication output already exists")
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    resolved_output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(disposition)


def self_test() -> None:
    demand(shortest_interval([0.005, 0.99, 0.005])[:2] == (1, 1), "shortest interval self-test")
    demand(shortest_interval([0.9899999999995, 0.0100000000005])[:2] == (0, 1), "strict 99-percent coverage self-test")
    demand(density_envelope(4, 0, 4) == (Fraction(0), Fraction(9, 16)), "density envelope self-test")
    atoms = atom_partition((Fraction(0), Fraction(3, 8)))
    demand(atoms and atoms[0]["density_interval"][0] == [0, 1] and atoms[-1]["density_interval"][1] == [3, 8], "atom partition self-test")
    demand(all(atom["density_interval"][1] == atoms[index + 1]["density_interval"][0] for index, atom in enumerate(atoms[:-1])), "atom adjacency self-test")
    selected = selected_large_pairs(atoms)
    demand(selected and all(charge > 0 for _, charge in selected), "zero-response sector exclusion self-test")
    synthetic_history = {
        "L": 4,
        "comparison": {"resolved": True},
        "rows": [
            {"event": event, "sector_weights": [0.005, 0.99, 0.005, 0.0, 0.0]}
            for event in range(1, 5)
        ],
    }
    demand(max(abs(a - b) for a, b in zip(reconstructed_pbar(synthetic_history, 4), [0.005, 0.99, 0.005, 0.0, 0.0])) <= 1.0e-15, "late-window pbar self-test")
    expanded_history = json.loads(json.dumps(synthetic_history))
    for row in expanded_history["rows"]:
        row["sector_weights"].extend([0.0] * 4)
    demand(
        full_weight_matrix(expanded_history, 4)
        == full_weight_matrix(synthetic_history, 4),
        "expanded zero-tail projection self-test",
    )
    nonzero_tail_history = json.loads(json.dumps(expanded_history))
    nonzero_tail_history["rows"][0]["sector_weights"][5] = 1.0e-30
    try:
        full_weight_matrix(nonzero_tail_history, 4)
    except FailClosed as error:
        demand(
            "nonzero or invalid q>L sector-weight tail" in str(error),
            "expanded nonzero-tail refusal message self-test",
        )
    else:
        raise AssertionError("expanded nonzero-tail history did not fail closed")
    underflow_tail_history = json.loads(json.dumps(expanded_history))
    underflow_tail_history["rows"][0]["sector_weights"][5] = Decimal("1e-400")
    try:
        full_weight_matrix(underflow_tail_history, 4)
    except FailClosed as error:
        demand(
            "nonzero or invalid q>L sector-weight tail" in str(error),
            "expanded underflow-tail refusal message self-test",
        )
    else:
        raise AssertionError("expanded underflow-tail history did not fail closed")
    wrong_length_history = json.loads(json.dumps(synthetic_history))
    wrong_length_history["rows"][0]["sector_weights"].extend([0.0] * 3)
    try:
        full_weight_matrix(wrong_length_history, 4)
    except FailClosed as error:
        demand(
            "invalid sector-weight vector length" in str(error),
            "wrong sector-weight length refusal message self-test",
        )
    else:
        raise AssertionError("wrong sector-weight length history did not fail closed")
    demand(not valid_digest("0" * 63) and valid_digest("0" * 64), "digest self-test")
    physical_fixture = json.loads(
        (ROOT / "DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001" / "VALIDATION" / "SECTOR_L8_Q4.json").read_text()
    )
    demand(not validate_large_row(physical_fixture, 8, 4), "known physical-row fixture self-test")
    for field in (
        "total_matvecs",
        "wall_seconds",
        "max_rss_bytes",
        "ground_residual",
        "active_actual_residual",
        "ground_block_hermiticity_error",
        "response_block_hermiticity_error",
        "ground_krylov_orthogonality",
        "response_krylov_orthogonality",
        "response_projection_error",
    ):
        boolean_row = json.loads(json.dumps(physical_fixture))
        boolean_row[field] = False
        demand(validate_large_row(boolean_row, 8, 4), f"physical-row Boolean refusal self-test: {field}")
    boolean_row = json.loads(json.dumps(physical_fixture))
    boolean_row["response_sequence"][-1]["lowest_five_ritz_values"][0] = False
    demand(
        any("lowest-five exact finite numbers" in error for error in validate_large_row(boolean_row, 8, 4)),
        "checkpoint Boolean refusal self-test",
    )
    threshold_row = json.loads(json.dumps(physical_fixture))
    threshold_row["response_sequence"][-1]["threshold_indices"] = [1, 1, 1]
    demand(
        any("threshold-index identity" in error for error in validate_large_row(threshold_row, 8, 4)),
        "active/threshold binding refusal self-test",
    )
    projection_row = json.loads(json.dumps(physical_fixture))
    projection_row["response_full_norm_squared"] += 1.0
    demand(
        "projection-error reconstruction" in validate_large_row(projection_row, 8, 4),
        "projection reconstruction refusal self-test",
    )
    single_ground_row = json.loads(json.dumps(physical_fixture))
    single_ground_row["ground_sequence"] = single_ground_row["ground_sequence"][-1:]
    demand(
        any("checkpoint census" in error for error in validate_large_row(single_ground_row, 8, 4)),
        "single-ground-checkpoint refusal self-test",
    )
    matvec_row = json.loads(json.dumps(physical_fixture))
    matvec_row["ground_matvecs"] = matvec_row["response_matvecs"] = matvec_row["total_matvecs"] = 0
    demand(
        any("matvec/checkpoint reconstruction" in error for error in validate_large_row(matvec_row, 8, 4)),
        "matvec/checkpoint refusal self-test",
    )
    weight_row = json.loads(json.dumps(physical_fixture))
    weight_row["response_sequence"][-1]["total_weight"] += 0.1
    demand(
        any("total-weight reconstruction" in error for error in validate_large_row(weight_row, 8, 4)),
        "response-weight refusal self-test",
    )
    duplicate_row = json.loads(json.dumps(physical_fixture))
    duplicate_row["ground_sequence"].append(dict(duplicate_row["ground_sequence"][-1]))
    duplicate_row["response_sequence"].append(dict(duplicate_row["response_sequence"][-1]))
    demand(
        any("checkpoint census" in error for error in validate_large_row(duplicate_row, 8, 4)),
        "duplicate-checkpoint refusal self-test",
    )
    zero_response_row = json.loads(json.dumps(physical_fixture))
    zero_response_row["response_full_norm_squared"] = 0.0
    zero_response_row["response_projected_norm_squared"] = 0.0
    zero_response_row["response_projection_error"] = 0.0
    for checkpoint in zero_response_row["response_sequence"]:
        checkpoint["total_weight"] = 0.0
        checkpoint["weight_floor"] = 0.0
    demand(
        any("strictly positive" in error for error in validate_large_row(zero_response_row, 8, 4)),
        "zero-response-channel refusal self-test",
    )
    residue_row = json.loads(json.dumps(physical_fixture))
    residue_row["R_low"] = 2.0
    residue_row["response_sequence"][-1]["R_low"] = 2.0
    residue_row["response_sequence"][-2]["R_low"] = 2.0
    demand(
        any("R_low probability upper bound" in error for error in validate_large_row(residue_row, 8, 4)),
        "residue-probability refusal self-test",
    )
    infeasible_floor_row = json.loads(json.dumps(physical_fixture))
    infeasible_floor_row["response_sequence"][-1]["active_residual_estimate"] = 1.0
    infeasible_floor_row["response_sequence"][-1]["weight_floor"] = (
        100.0 * infeasible_floor_row["response_projected_norm_squared"]
    )
    demand(
        any("threshold-support feasibility" in error for error in validate_large_row(infeasible_floor_row, 8, 4)),
        "threshold-support refusal self-test",
    )
    zero_dimension_row = json.loads(json.dumps(physical_fixture))
    for field in (
        "sector_dimension",
        "translation_orbits",
        "ground_block_dimension",
        "ground_block_nnz",
        "response_block_dimension",
        "response_block_nnz",
    ):
        zero_dimension_row[field] = 0
    demand(
        any("dimension" in error or "orbit" in error or "nnz" in error for error in validate_large_row(zero_dimension_row, 8, 4)),
        "zero-dimension refusal self-test",
    )
    try:
        validate_manifest(None, None)
    except FailClosed as error:
        demand("--manifest is required" in str(error), "manifest refusal message self-test")
    else:
        raise AssertionError("missing manifest did not fail closed")
    with tempfile.TemporaryDirectory(dir=HERE) as temporary:
        temporary_path = Path(temporary)
        path = temporary_path / "row.json"
        path.write_text("{}\n")
        demand(valid_digest(sha256(path)), "temporary hash self-test")
        try:
            execute_target({"atoms": atoms}, Path(temporary) / "out", None, None, None)
        except FailClosed as error:
            demand("execution token absent" in str(error), "execution-token refusal self-test")
        else:
            raise AssertionError("missing execution token did not fail closed")

        histories = {}
        envelopes = {}
        for length in SIZES:
            projected_weights = [0.0] * (length + 1)
            projected_weights[0] = 0.005
            projected_weights[length // 2] = 0.995
            weights = list(projected_weights)
            if length in (4, 6, 8):
                weights.extend([0.0] * length)
            history = {
                "L": length,
                "dimension": 1 << length,
                "comparison": {"resolved": True},
                "rows": [
                    {
                        "event": event,
                        "sector_weights": weights,
                        **{field: float(event) / length for field in HISTORY_OBSERVABLE_FIELDS},
                    }
                    for event in range(1, length + 1)
                ],
            }
            target_history = temporary_path / f"target_L{length}.json"
            blind_history = temporary_path / f"blind_L{length}.json"
            audit = temporary_path / f"audit_L{length}.txt"
            target_history.write_text(json.dumps(history, sort_keys=True) + "\n")
            blind_history.write_text(json.dumps(history, sort_keys=True) + "\n")
            target_history_sha = sha256(target_history)
            blind_history_sha = sha256(blind_history)
            audit.write_text(f"PASS synthetic custody only\ntarget {target_history_sha}\nblind {blind_history_sha}\n")
            lower = upper = length // 2
            envelope = density_envelope(length, lower, upper)
            envelopes[length] = envelope
            histories[str(length)] = {
                "target_history_path": str(target_history.relative_to(ROOT)),
                "target_history_sha256": target_history_sha,
                "blind_history_path": str(blind_history.relative_to(ROOT)),
                "blind_history_sha256": blind_history_sha,
                "hostile_audit_path": str(audit.relative_to(ROOT)),
                "hostile_audit_sha256": sha256(audit),
                "hostile_verdict": "PASS",
                "max_target_blind_sector_weight_difference": 0.0,
                "max_target_blind_history_observable_difference": 0.0,
                "pbar_q": projected_weights,
                "q_interval": [lower, upper],
                "density_envelope": [ratio_pair(envelope[0]), ratio_pair(envelope[1])],
            }
        common = (max(value[0] for value in envelopes.values()), min(value[1] for value in envelopes.values()))
        manifest = {
            "schema": MANIFEST_SCHEMA,
            "status": MANIFEST_STATUS,
            "accumulation_protocol_sha256": ACCUMULATION_PROTOCOL_SHA256,
            "histories": histories,
            "I_acc": [ratio_pair(common[0]), ratio_pair(common[1])],
            "atoms": atom_partition(common),
        }
        manifest_path = temporary_path / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        validated = validate_manifest(manifest_path, sha256(manifest_path))
        demand(validated["common"] == common and validated["atoms"] == manifest["atoms"], "full manifest reconstruction self-test")
        bad_manifest = dict(manifest)
        bad_manifest["atoms"] = manifest["atoms"][:-1]
        bad_path = temporary_path / "bad_manifest.json"
        bad_path.write_text(json.dumps(bad_manifest, indent=2, sort_keys=True) + "\n")
        try:
            validate_manifest(bad_path, sha256(bad_path))
        except FailClosed as error:
            demand("atom partition" in str(error), "incomplete atom refusal self-test")
        else:
            raise AssertionError("incomplete atom manifest did not fail closed")
        altered_history = json.loads(blind_history.read_text())
        altered_history["rows"][0][HISTORY_OBSERVABLE_FIELDS[0]] += 1.0e-7
        blind_history.write_text(json.dumps(altered_history, sort_keys=True) + "\n")
        histories[str(SIZES[-1])]["blind_history_sha256"] = sha256(blind_history)
        audit.write_text(
            f"PASS synthetic custody only\ntarget {histories[str(SIZES[-1])]['target_history_sha256']}\n"
            f"blind {histories[str(SIZES[-1])]['blind_history_sha256']}\n"
        )
        histories[str(SIZES[-1])]["hostile_audit_sha256"] = sha256(audit)
        altered_manifest_path = temporary_path / "altered_history_manifest.json"
        altered_manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        try:
            validate_manifest(altered_manifest_path, sha256(altered_manifest_path))
        except FailClosed as error:
            demand("history-observable mismatch" in str(error), "event-level observable refusal self-test")
        else:
            raise AssertionError("event-level observable mismatch did not fail closed")
        altered_history["rows"][0][HISTORY_OBSERVABLE_FIELDS[0]] -= 1.0e-7
        altered_history["rows"][0]["sector_weights"][0] += 1.0e-7
        altered_history["rows"][0]["sector_weights"][length // 2] -= 1.0e-7
        blind_history.write_text(json.dumps(altered_history, sort_keys=True) + "\n")
        histories[str(SIZES[-1])]["blind_history_sha256"] = sha256(blind_history)
        audit.write_text(
            f"PASS synthetic custody only\ntarget {histories[str(SIZES[-1])]['target_history_sha256']}\n"
            f"blind {histories[str(SIZES[-1])]['blind_history_sha256']}\n"
        )
        histories[str(SIZES[-1])]["hostile_audit_sha256"] = sha256(audit)
        sector_altered_manifest_path = temporary_path / "altered_sector_manifest.json"
        sector_altered_manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        try:
            validate_manifest(sector_altered_manifest_path, sha256(sector_altered_manifest_path))
        except FailClosed as error:
            demand("sector-weight mismatch" in str(error), "early-window sector refusal self-test")
        else:
            raise AssertionError("early-window sector mismatch did not fail closed")
    print("PASS_SYNTHETIC_SELF_TESTS__NO_PHYSICAL_SPECTRUM")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=("verify-freeze", "self-test", "preflight", "execute-target", "adjudicate"))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--manifest-sha256")
    parser.add_argument("--authorization")
    parser.add_argument("--blind-freeze", type=Path)
    parser.add_argument("--blind-freeze-sha256")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--target-index", type=Path)
    parser.add_argument("--target-index-sha256")
    parser.add_argument("--blind-index", type=Path)
    parser.add_argument("--blind-index-sha256")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.mode == "self-test":
        self_test()
        return
    verify_freeze()
    if args.mode == "verify-freeze":
        print("PASS_FREEZE_CUSTODY__NO_PHYSICAL_SPECTRUM")
        return
    validated = validate_manifest(args.manifest, args.manifest_sha256)
    if args.mode == "preflight":
        print(json.dumps({"status": "READY", "manifest_sha256": validated["sha256"], "I_acc": [ratio_pair(x) for x in validated["common"]], "atoms": len(validated["atoms"]), "large_sectors": [list(x) for x in selected_large_pairs(validated["atoms"])]}, sort_keys=True))
    elif args.mode == "execute-target":
        demand(args.output_dir is not None, "--output-dir required")
        execute_target(
            validated,
            args.output_dir,
            args.authorization,
            args.blind_freeze,
            args.blind_freeze_sha256,
        )
    else:
        demand(args.output is not None, "--output required")
        adjudicate(validated, args.target_index, args.target_index_sha256, args.blind_index, args.blind_index_sha256, args.output)


if __name__ == "__main__":
    try:
        main()
    except FailClosed as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        raise SystemExit(2)
