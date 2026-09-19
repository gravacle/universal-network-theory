#!/usr/bin/env python3
"""Deterministic non-physics kernel used only for V002 fault tests."""

import time
from pathlib import Path

from durable_evidence import immutable_write_json, sha256_file


MASSES = {"4": "0.160", "5": "0.203", "6": "0.150", "7": "0.120", "8": "0.100", "9": "0.050"}
INTERVALS = {
    4: [[1, 6], [3, 16]],
    5: [[3, 16], [11, 56]],
    6: [[11, 56], [11, 48]],
    7: [[11, 48], [1, 4]],
    8: [[1, 4], [15, 56]],
    9: [[15, 56], [2, 7]],
}


def prepare_phase(branch, phase, request, context):
    artifact = Path(context["checkpoint_root"]) / "artifacts" / "preparation.json"
    immutable_write_json(
        artifact,
        {
            "schema": "L14_FIXTURE_PREPARATION_V002",
            "branch": branch,
            "phase": phase,
            "run_id": request["run_id"],
            "shared_root": context["shared_root"],
        },
    )
    return {
        "fixture_prepared": True,
        "artifacts": [
            {"path": str(artifact.resolve()), "sha256": sha256_file(artifact), "bytes": artifact.stat().st_size}
        ],
    }


def build_task_plan(branch, phase, request, context):
    del branch, context
    repeat = int(request.get("fixture", {}).get("repeat", 1))
    sleep_seconds = float(request.get("fixture", {}).get("sleep_seconds", 0.0))
    tasks = []
    for q in request["sectors"]:
        for replica in range(repeat):
            tasks.append(
                {
                    "task_id": "q{:02d}_r{:03d}".format(q, replica),
                    "payload": {
                        "q": q,
                        "replica": replica,
                        "sleep_seconds": sleep_seconds,
                        "interval": INTERVALS[q],
                    },
                    "work_units": q + 1,
                }
            )
    return tasks


def run_task(task_payload, context):
    time.sleep(float(task_payload.get("sleep_seconds", 0.0)))
    artifact = Path(context["checkpoint_root"]) / "artifacts" / (context["task_id"] + ".json")
    immutable_write_json(
        artifact,
        {
            "schema": "L14_FIXTURE_ARTIFACT_V002",
            "task_id": context["task_id"],
            "task_sha256": context["task_sha256"],
            "q": task_payload["q"],
            "replica": task_payload["replica"],
        },
    )
    return {
        "q": task_payload["q"],
        "replica": task_payload["replica"],
        "interval": task_payload["interval"],
        "artifacts": [
            {"path": str(artifact.resolve()), "sha256": sha256_file(artifact), "bytes": artifact.stat().st_size}
        ],
    }


def reduce_results(branch, phase, request, results, context):
    del context
    first_by_q = {}
    for result in results:
        first_by_q.setdefault(result["q"], result)
    atoms = []
    for q in request["sectors"]:
        geometry_shift = 2.0e-12 if branch == "hostile" else 0.0
        atoms.append(
            {
                "atom_id": "A{:03d}".format(q),
                "q": q,
                "density_interval": first_by_q[q]["interval"],
                "geometry": {
                    "resolved": True,
                    "z": 1.0 + geometry_shift,
                    "y": 1.0 - geometry_shift,
                    "passes_window": True,
                },
                "l14_response": {
                    "L": 14,
                    "q": q,
                    "rho": q / 28.0,
                    "sector_dimension": 100 + q,
                    "translation_orbits": 10 + q,
                    "ground_block_dimension": 10 + q,
                    "ground_block_nnz": 20 + q,
                    "response_block_dimension": 10 + q,
                    "response_block_nnz": 20 + q,
                    "ground_energy": -1.0,
                    "Delta_act": 0.5,
                    "chi_tau": 1.0,
                    "R_low": 0.25,
                },
            }
        )
    return {
        "schema": "L14_SCOUT_BRANCH_RESULT_V002",
        "length": 14,
        "branch": branch,
        "phase": phase,
        "computed_sectors": request["sectors"],
        "sector_masses": MASSES,
        "numerical_validation": {
            "all_actual_and_null_solvers_converged": True,
            "residual_l1_within_original_bound": True,
            "actual_norm_error_within_original_bound": True,
            "transport_number_drift_within_original_bound": True,
            "rough_sharp_agreement_within_original_bound": True,
        },
        "comparison_evidence": {
            "raw_metrics": {
                "reverse_support_probability": "0.75",
                "transport_node_residual_l1": "1e-13",
                "actual_norm_error": "1e-14",
                "transport_number_drift": "1e-15"
            },
            "predicate_thresholds": {
                "reverse_support_probability": {"comparison": "fixture-only"},
                "transport_node_residual_l1": "1e-10",
                "actual_norm_error": "1e-10",
                "transport_number_drift": "1e-10"
            }
        },
        "atoms": atoms,
        "fixture_only": True,
    }
