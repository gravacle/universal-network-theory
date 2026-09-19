#!/usr/bin/env python3
"""Authenticate and merge independent target/hostile L14 branch results."""

from __future__ import annotations

import argparse
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence, Tuple

from branch_runner import BRANCH_SCHEMA, finite_decimal
from durable_evidence import EvidenceError, immutable_write_json, load_json, sha256_file


OUTPUT_SCHEMA = "L14_TARGETED_SCOUT_SOLVER_RESULT_V001"
SECTOR_MASS_TOLERANCE = Decimal("1e-8")


def relative_difference(left: Decimal, right: Decimal) -> Decimal:
    return abs(left - right) / max(abs(left), abs(right), Decimal("1e-300"))


def number(value: Any, label: str) -> Decimal:
    if isinstance(value, bool):
        raise EvidenceError("{} is boolean".format(label))
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as error:
        raise EvidenceError("{} is not numeric".format(label)) from error
    if not result.is_finite():
        raise EvidenceError("{} is not finite".format(label))
    return result


def identity(payload: Mapping[str, Any]) -> Tuple[Any, ...]:
    return (
        payload.get("length"),
        payload.get("phase"),
        tuple(payload.get("computed_sectors", [])),
    )


def atom_map(payload: Mapping[str, Any]) -> Dict[str, Mapping[str, Any]]:
    atoms = payload.get("atoms")
    if not isinstance(atoms, list):
        raise EvidenceError("branch atoms absent")
    mapped: Dict[str, Mapping[str, Any]] = {}
    for atom in atoms:
        if not isinstance(atom, dict) or not isinstance(atom.get("atom_id"), str):
            raise EvidenceError("malformed branch atom")
        if atom["atom_id"] in mapped:
            raise EvidenceError("duplicate branch atom: {}".format(atom["atom_id"]))
        mapped[atom["atom_id"]] = atom
    return mapped


def authenticate_branch(payload: Mapping[str, Any], expected_branch: str) -> None:
    if payload.get("schema") != BRANCH_SCHEMA or payload.get("branch") != expected_branch:
        raise EvidenceError("{} branch identity failed".format(expected_branch))
    validation = payload.get("numerical_validation")
    if not isinstance(validation, dict) or not validation:
        raise EvidenceError("{} numerical validation absent".format(expected_branch))
    required = (
        "all_actual_and_null_solvers_converged",
        "residual_l1_within_original_bound",
        "actual_norm_error_within_original_bound",
        "transport_number_drift_within_original_bound",
        "rough_sharp_agreement_within_original_bound",
    )
    failures = sorted(key for key in required if validation.get(key) is not True)
    if failures:
        raise EvidenceError("{} original predicates failed: {}".format(expected_branch, failures))
    comparison = payload.get("comparison_evidence")
    if not isinstance(comparison, dict):
        raise EvidenceError("{} comparison evidence absent".format(expected_branch))
    raw_metrics = comparison.get("raw_metrics")
    thresholds = comparison.get("predicate_thresholds")
    required_metrics = (
        "reverse_support_probability",
        "transport_node_residual_l1",
        "actual_norm_error",
        "transport_number_drift",
    )
    if not isinstance(raw_metrics, dict) or not isinstance(thresholds, dict):
        raise EvidenceError("{} comparison metrics or thresholds absent".format(expected_branch))
    for metric in required_metrics:
        finite_decimal(raw_metrics.get(metric), "{} raw metric {}".format(expected_branch, metric))
        if metric not in thresholds or thresholds[metric] is None:
            raise EvidenceError("{} predicate threshold absent for {}".format(expected_branch, metric))


def merge(target_path: Path, hostile_path: Path) -> Dict[str, Any]:
    target = load_json(target_path)
    hostile = load_json(hostile_path)
    authenticate_branch(target, "target")
    authenticate_branch(hostile, "hostile")
    if identity(target) != identity(hostile):
        raise EvidenceError("target/hostile phase identity mismatch")

    target_masses = target.get("sector_masses")
    hostile_masses = hostile.get("sector_masses")
    if not isinstance(target_masses, dict) or not isinstance(hostile_masses, dict):
        raise EvidenceError("sector mass ledger absent")
    if set(target_masses) != set(hostile_masses):
        raise EvidenceError("target/hostile mass sectors mismatch")
    merged_masses: Dict[str, str] = {}
    mass_differences: Dict[str, str] = {}
    for q in sorted(target_masses, key=int):
        target_mass = number(target_masses[q], "target mass q={}".format(q))
        hostile_mass = number(hostile_masses[q], "hostile mass q={}".format(q))
        difference = abs(target_mass - hostile_mass)
        if difference > SECTOR_MASS_TOLERANCE:
            raise EvidenceError(
                "target/hostile sector mass mismatch at q={}: |{} - {}| = {} > {}".format(
                    q, target_mass, hostile_mass, difference, SECTOR_MASS_TOLERANCE
                )
            )
        # Use the lower independently computed mass so the threshold gate can
        # never benefit from numerical disagreement between the branches.
        merged_masses[str(int(q))] = str(min(target_mass, hostile_mass))
        mass_differences[str(int(q))] = str(difference)

    targets = atom_map(target)
    hostiles = atom_map(hostile)
    if set(targets) != set(hostiles):
        raise EvidenceError("target/hostile atom census mismatch")
    merged_atoms = []
    for atom_id in sorted(targets):
        left = targets[atom_id]
        right = hostiles[atom_id]
        for field in ("q", "density_interval"):
            if left.get(field) != right.get(field):
                raise EvidenceError("atom {} {} mismatch".format(atom_id, field))
        left_geometry = left.get("geometry")
        right_geometry = right.get("geometry")
        if not isinstance(left_geometry, dict) or not isinstance(right_geometry, dict):
            raise EvidenceError("atom {} geometry absent".format(atom_id))
        geometry_differences = {}
        for coordinate in ("z", "y"):
            difference = relative_difference(
                number(left_geometry.get(coordinate), "target {} {}".format(atom_id, coordinate)),
                number(right_geometry.get(coordinate), "hostile {} {}".format(atom_id, coordinate)),
            )
            if difference > Decimal("1e-9"):
                raise EvidenceError("atom {} target/hostile {} mismatch: {}".format(atom_id, coordinate, difference))
            geometry_differences[coordinate] = str(difference)
        if left_geometry.get("passes_window") != right_geometry.get("passes_window"):
            raise EvidenceError("atom {} target/hostile window decision mismatch".format(atom_id))

        left_response = left.get("l14_response")
        right_response = right.get("l14_response")
        if not isinstance(left_response, dict) or not isinstance(right_response, dict):
            raise EvidenceError("atom {} L14 response evidence absent".format(atom_id))
        response_differences = {}
        for field, tolerance in (
            ("ground_energy", Decimal("2e-8")),
            ("Delta_act", Decimal("2e-8")),
            ("chi_tau", Decimal("5e-7")),
            ("R_low", Decimal("5e-6")),
        ):
            difference = relative_difference(
                number(left_response.get(field), "target {} {}".format(atom_id, field)),
                number(right_response.get(field), "hostile {} {}".format(atom_id, field)),
            )
            if difference > tolerance:
                raise EvidenceError("atom {} L14 target/hostile {} mismatch: {} > {}".format(atom_id, field, difference, tolerance))
            response_differences[field] = str(difference)
        for field in (
            "L", "q", "rho", "sector_dimension", "translation_orbits",
            "ground_block_dimension", "ground_block_nnz",
            "response_block_dimension", "response_block_nnz",
        ):
            if left_response.get(field) != right_response.get(field):
                raise EvidenceError("atom {} L14 response {} identity mismatch".format(atom_id, field))

        merged_atoms.append(
            {
                "atom_id": atom_id,
                "q": left["q"],
                "density_interval": left["density_interval"],
                "target": left_geometry,
                "blind": right_geometry,
                "target_blind_geometry_relative_differences": geometry_differences,
                "target_blind_l14_response_relative_differences": response_differences,
            }
        )

    return {
        "schema": OUTPUT_SCHEMA,
        "length": target["length"],
        "phase": target["phase"],
        "computed_sectors": target["computed_sectors"],
        "sector_masses": merged_masses,
        "validation": {
            "all_original_numerical_predicates_pass": True,
            "target_blind_authenticated": True,
            "sector_mass_absolute_difference_within_1e-8": True,
            "target_blind_l14_response_within_original_bounds": True,
        },
        "sector_mass_absolute_differences": mass_differences,
        "atoms": merged_atoms,
        "provenance": {
            "target": {"path": str(target_path.resolve()), "sha256": sha256_file(target_path)},
            "hostile": {"path": str(hostile_path.resolve()), "sha256": sha256_file(hostile_path)},
            "merge_policy": "EXACT_ATOM_INTERVAL_IDENTITY__ORIGINAL_NUMERICAL_TARGET_BLIND_RULES__CONSERVATIVE_MINIMUM_SECTOR_MASS__NO_OVERRIDE",
            "sector_mass_tolerance": str(SECTOR_MASS_TOLERANCE),
        },
    }


def main(argv: Sequence[str] = ()) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--hostile", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv or sys.argv[1:])
    payload = merge(args.target, args.hostile)
    immutable_write_json(args.output, payload)
    print("L14_MERGE_COMPLETE output={} sha256={}".format(args.output, sha256_file(args.output)), flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("L14_MERGE_FAILURE type={} message={}".format(type(error).__name__, error), file=sys.stderr, flush=True)
        raise SystemExit(2)
