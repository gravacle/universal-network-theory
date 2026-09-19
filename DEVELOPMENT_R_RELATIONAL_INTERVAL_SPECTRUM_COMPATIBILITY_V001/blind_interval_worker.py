#!/usr/bin/env python3
"""Independent interval worker with the frozen public Stage 6 row contract.

The numerical construction is the previously audited independent centerline
engine.  This wrapper broadens only its L10/L12 charge policy and serializes
the already-adopted public observables and guards.  It never imports target
code or a target matrix.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import resource
import sys
import time
from pathlib import Path

import numpy as np

import blind_contract_control as credential_control
from contract_common import Refusal, atomic_owner_once_json, demand, sha256_file


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
BLIND_ENGINE = ROOT / "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001" / "independent_centerline.py"
BLIND_ENGINE_SHA256 = "79aec7d5a773f8a7268ae98c6c343201a331e628274a3d225432059dee6b7fa7"
BLIND_METHOD = ROOT / "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001" / "METHODOLOGY.md"
BLIND_METHOD_SHA256 = "dbe28ec72e64cea10b9e974213277c284ffd20596877a06fdca4ee66ba4075a4"
RUN_TOKEN = "RUN_HASH_PINNED_BLIND_RELATIONAL_INTERVAL_SPECTRUM_V001"
ALLOWED_SIZES = (10, 12)
CHECKPOINTS = (16, 32, 64, 96, 128)
MAX_KRYLOV = 128
MAX_MATVECS = 2000
MAX_SECONDS = 10_800.0
MAX_RSS_BYTES = 6 * (1 << 30)


def load_blind_engine():
    demand(sha256_file(BLIND_ENGINE) == BLIND_ENGINE_SHA256, "blind engine hash mismatch")
    demand(sha256_file(BLIND_METHOD) == BLIND_METHOD_SHA256, "blind methodology hash mismatch")
    specification = importlib.util.spec_from_file_location(
        "frozen_independent_interval_engine", BLIND_ENGINE
    )
    demand(
        specification is not None and specification.loader is not None,
        "cannot load independent blind engine",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def install_rss_guard() -> list[str]:
    installed: list[str] = []
    for name in ("RLIMIT_AS", "RLIMIT_RSS"):
        guard = getattr(resource, name, None)
        if guard is None:
            continue
        try:
            old_soft, old_hard = resource.getrlimit(guard)
            new_hard = MAX_RSS_BYTES if old_hard < 0 else min(old_hard, MAX_RSS_BYTES)
            resource.setrlimit(guard, (min(MAX_RSS_BYTES, new_hard), new_hard))
            installed.append(name)
        except (OSError, ValueError):
            pass
    return installed


def selected_snapshots(
    snapshots: list[dict[str, object]], final_dimension: int
) -> list[dict[str, object]]:
    selected = [
        snapshot
        for snapshot in snapshots
        if int(snapshot["krylov_dimension"]) in CHECKPOINTS
        or int(snapshot["krylov_dimension"]) == final_dimension
    ]
    demand(bool(selected), "canonical checkpoint sequence is empty")
    expected = sorted(
        {dimension for dimension in CHECKPOINTS if dimension <= final_dimension}
        | {final_dimension}
    )
    demand(
        [int(snapshot["krylov_dimension"]) for snapshot in selected] == expected,
        "canonical checkpoint census mismatch",
    )
    return selected


def ground_sequence(engine, run) -> list[dict[str, object]]:
    snapshots = selected_snapshots(run.snapshots, run.matvecs)
    rows = []
    for snapshot in snapshots:
        rows.append(
            {
                "krylov_dimension": int(snapshot["krylov_dimension"]),
                "energy": float(snapshot["ground_energy"]),
                "residual_estimate": float(snapshot["ground_residual_estimate"]),
                "lowest_five_ritz_values": [
                    float(value) for value in snapshot["lowest_five_ritz_values"]
                ],
            }
        )
    return rows


def threshold_indices(
    values: list[float], ground_energy: float, omegas: list[object]
) -> list[int]:
    result: list[int] = []
    for omega in omegas:
        demand(type(omega) in (int, float) and math.isfinite(float(omega)), "threshold omega unresolved")
        matches = [
            index
            for index, value in enumerate(values)
            if abs((float(value) - ground_energy) - float(omega)) <= 1.0e-9
        ]
        demand(bool(matches), "active threshold pole not retained in lowest five")
        result.append(matches[0])
    return result


def response_sequence(engine, run, ground_energy: float) -> list[dict[str, object]]:
    snapshots = selected_snapshots(run.snapshots, run.matvecs)
    rows = []
    for snapshot in snapshots:
        metrics = snapshot.get("metrics")
        demand(isinstance(metrics, dict) and metrics.get("resolved") is True, "response checkpoint unresolved")
        values = [float(value) for value in snapshot["lowest_five_ritz_values"]]
        indices = threshold_indices(values, ground_energy, metrics["threshold_omegas"])
        demand(len(set(indices)) == 1, "threshold-index identity is unstable")
        rows.append(
            {
                "krylov_dimension": int(snapshot["krylov_dimension"]),
                "lowest_five_ritz_values": values,
                "Delta_act": float(metrics["Delta_act"]),
                "chi_tau": float(metrics["chi_tau"]),
                "R_low": float(metrics["R_low"]),
                "active_ritz_index": indices[1],
                "active_residual_estimate": float(metrics["active_residual_estimate"]),
                "total_weight": float(metrics["total_weight"]),
                "weight_floor": float(metrics["weight_floor"]),
                "threshold_stable": bool(metrics["threshold_stable"]),
                "threshold_indices": indices,
                "resolved": True,
            }
        )
    return rows


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def calculate_canonical_row(length: int, charge: int) -> dict[str, object]:
    demand(length in ALLOWED_SIZES and 1 <= charge <= length, "sector outside L10/L12 positive half-sector")
    engine = load_blind_engine()
    memory_guards = install_rss_guard()
    started = time.perf_counter()
    structural = engine.structural_controls(length)
    bank = engine.build_orbit_bank(length, charge)
    ground_block = engine.build_sparse_block(bank, 0)
    ground_run = engine.krylov(
        ground_block,
        engine.deterministic_ground_start(ground_block.dimension),
        "ground",
    )
    ground_energy, ground_coefficients, ground_residual = engine.reconstruct_ground(
        ground_block, ground_run
    )
    ground_words = engine.expand_to_words(bank, ground_block, ground_coefficients)

    wave_number = 2.0 * math.pi / length
    phases = np.exp(1j * wave_number * np.arange(length))
    response_words = np.zeros(len(bank.words), dtype=np.complex128)
    for row, raw_word in enumerate(bank.words):
        word = int(raw_word)
        diagonal = 0.0j
        for site in range(length):
            diagonal += phases[site] * (
                ((word >> site) & 1) + ((word >> (length + site)) & 1)
            )
        response_words[row] = diagonal * ground_words[row]

    response_block = engine.build_sparse_block(bank, length - 1)
    response_start = engine.project_from_words(bank, response_block, response_words)
    full_norm_squared = float(np.vdot(response_words, response_words).real)
    projected_norm_squared = float(np.vdot(response_start, response_start).real)
    projection_error = abs(full_norm_squared - projected_norm_squared)
    response_run = engine.krylov(
        response_block,
        response_start,
        "response",
        ground_energy=ground_energy,
    )
    final_metrics = response_run.snapshots[-1].get("metrics", {})
    demand(isinstance(final_metrics, dict), "final response metrics absent")
    active_residual = engine.active_actual_residual(
        response_block, response_run, ground_energy
    )
    ground_rows = ground_sequence(engine, ground_run)
    response_rows = response_sequence(engine, response_run, ground_energy)
    final_response = response_rows[-1]
    elapsed = time.perf_counter() - started
    rss = int(engine.peak_rss_bytes())
    failures: list[str] = []
    if structural["owner_edges"] != 3 * length or structural["unique_edges"] != 3 * length:
        failures.append("OWNER_CENSUS")
    if any(degree != 3 for degree in structural["degrees"]):
        failures.append("DEGREE")
    if not structural["bipartite_edges"] or structural["one_carrier_band_linf"] > 1.0e-12:
        failures.append("STRUCTURAL_SPECTRUM")
    if max(ground_block.hermiticity_error, response_block.hermiticity_error) > 1.0e-12:
        failures.append("HERMITICITY")
    if max(ground_run.orthogonality_error, response_run.orthogonality_error) > 1.0e-10:
        failures.append("ORTHOGONALITY")
    if ground_residual > 1.0e-9 or active_residual > 1.0e-9:
        failures.append("RESIDUAL")
    if not final_metrics.get("resolved") or not final_metrics.get("threshold_stable"):
        failures.append("ACTIVE_THRESHOLD")
    if projection_error > 1.0e-9:
        failures.append("RESPONSE_PROJECTION")
    if elapsed > MAX_SECONDS:
        failures.append("WALL_GUARD")
    if rss > MAX_RSS_BYTES:
        failures.append("RSS_GUARD")
    total_matvecs = int(ground_run.matvecs + response_run.matvecs)
    if total_matvecs > MAX_MATVECS:
        failures.append("MATVEC_GUARD")

    if len(response_rows) >= 2:
        previous = response_rows[-2]
        convergence = {
            "Delta_act_relative": relative_difference(float(final_response["Delta_act"]), float(previous["Delta_act"])),
            "chi_tau_relative": relative_difference(float(final_response["chi_tau"]), float(previous["chi_tau"])),
            "R_low_relative": relative_difference(float(final_response["R_low"]), float(previous["R_low"])),
        }
        convergence["resolved"] = (
            convergence["Delta_act_relative"] <= 2.0e-7
            and convergence["chi_tau_relative"] <= 2.0e-7
            and convergence["R_low_relative"] <= 2.0e-6
        )
    else:
        convergence = {
            "Delta_act_relative": 0.0,
            "chi_tau_relative": 0.0,
            "R_low_relative": 0.0,
            "resolved": bool(response_run.breakdown),
            "exact_krylov_termination": bool(response_run.breakdown),
        }
    if not convergence["resolved"]:
        failures.append("RESPONSE_CONVERGENCE")

    return {
        "L": length,
        "q": charge,
        "rho": charge / (2.0 * length),
        "sector_dimension": len(bank.words),
        "translation_orbits": len(bank.orbits),
        "ground_block_dimension": ground_block.dimension,
        "ground_block_nnz": len(ground_block.data),
        "response_block_dimension": response_block.dimension,
        "response_block_nnz": len(response_block.data),
        "ground_energy": ground_energy,
        "ground_residual": ground_residual,
        "ground_block_hermiticity_error": float(ground_block.hermiticity_error),
        "ground_krylov_orthogonality": float(ground_run.orthogonality_error),
        "response_full_norm_squared": full_norm_squared,
        "response_projected_norm_squared": projected_norm_squared,
        "response_projection_error": projection_error,
        "active_actual_residual": active_residual,
        "Delta_act": float(final_response["Delta_act"]),
        "chi_tau": float(final_response["chi_tau"]),
        "R_low": float(final_response["R_low"]),
        "response_block_hermiticity_error": float(response_block.hermiticity_error),
        "response_krylov_orthogonality": float(response_run.orthogonality_error),
        "ground_sequence": ground_rows,
        "response_sequence": response_rows,
        "response_convergence": convergence,
        "threshold_stable": bool(final_response["threshold_stable"]),
        "ground_matvecs": int(ground_run.matvecs),
        "response_matvecs": int(response_run.matvecs),
        "total_matvecs": total_matvecs,
        "wall_seconds": elapsed,
        "max_rss_bytes": rss,
        "memory_guards": memory_guards,
        "unresolved_reasons": failures,
        "status": "RESOLVED" if not failures else "UNRESOLVED",
        "blind_engine_sha256": BLIND_ENGINE_SHA256,
        "claim_boundary": "FINITE_BLIND_SECTOR_ROW_ONLY__NO_SCALING_OR_GRAVITY_RESULT",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int, required=True)
    parser.add_argument("--q", type=int, required=True)
    parser.add_argument("--run-token", required=True)
    parser.add_argument("--credential", type=Path)
    parser.add_argument("--credential-sha256")
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        demand(arguments.run_token == RUN_TOKEN, "literal blind execution token absent")
        demand(
            arguments.credential is not None
            and arguments.credential_sha256 is not None,
            "blind execution credential absent",
        )
        authorization = credential_control.validate_execution_credential(
            arguments.credential, arguments.credential_sha256,
            arguments.L, arguments.q, arguments.output, arguments.run_token,
        )
        row = calculate_canonical_row(arguments.L, arguments.q)
        demand(row["status"] == "RESOLVED", "blind row unresolved")
        row["execution_authorization"] = authorization
        atomic_owner_once_json(ROOT, arguments.output, row)
    except (Refusal, AssertionError, MemoryError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
