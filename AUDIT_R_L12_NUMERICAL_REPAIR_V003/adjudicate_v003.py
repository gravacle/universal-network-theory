#!/usr/bin/env python3
"""Exact Stage-4 adjudicator for the bounded V003 numerical repair."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE_PATH = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/adjudicate_l12_v001.py"
FREEZE = HERE / "PRE_OUTPUT_FREEZE_V003.json"
CUSTODY = HERE / "EXECUTION_CUSTODY_V003R1.json"
V002_SHARP = (
    ROOT
    / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_EVIDENCE/"
    "L12_PROCESS_PARALLEL_V002/histories/001798__SHARP_SUMMARY.json"
)
TARGET_SCHEMA = "TARGET_CACHED_PREFIX_HISTORY_PROCESS_PARALLEL_V003"
HOSTILE_SCHEMA = "HOSTILE_CACHED_PREFIX_HISTORY_PROCESS_PARALLEL_V003"
WALL_LIMIT = 345600.0
TARGET_SUBDIVISIONS = 256
TARGET_KRYLOV = 96
HOSTILE_DEGREE = 128


class RepairRefusal(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise RepairRefusal(message)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(16 * 2**20), b""):
            value.update(chunk)
    return value.hexdigest()


def load_base():
    specification = importlib.util.spec_from_file_location(
        "frozen_l12_stage4_v001_for_v003", BASE_PATH
    )
    demand(specification is not None and specification.loader is not None,
           "cannot load frozen Stage-4 predecessor")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def canonical_digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def verify_freeze(expected: str, base: Any) -> dict[str, Any]:
    demand(FREEZE.is_file() and digest(FREEZE) == expected,
           "V003 pre-output freeze SHA-256 mismatch")
    value = json.loads(FREEZE.read_text())
    demand(value.get("schema") == "L12_V003_NUMERICAL_REPAIR_PRE_OUTPUT_FREEZE",
           "V003 freeze schema")
    demand(value.get("status") == "FROZEN_BEFORE_V003_HISTORY_PUBLICATION",
           "V003 freeze status")
    demand(value.get("v003_history_outputs_present_at_freeze") is False,
           "V003 pre-output declaration")
    files = value.get("files")
    demand(isinstance(files, dict), "V003 freeze file census")
    for relative, expected_hash in files.items():
        path = (ROOT / relative).resolve()
        demand(path.is_relative_to(ROOT.resolve()) and path.is_file(),
               f"V003 frozen source missing: {relative}")
        demand(digest(path) == expected_hash,
               f"V003 frozen source changed: {relative}")
    demand(files.get(str(BASE_PATH.relative_to(ROOT))) == digest(BASE_PATH),
           "frozen Stage-4 predecessor custody")
    demand(files.get(str(CUSTODY.relative_to(ROOT))) == digest(CUSTODY),
           "V003 execution custody")
    demand(value.get("unchanged_tolerances") == {
        "cross_history_and_terminal_linf": 1e-8,
        "hostile_endpoint_and_tail": 8e-11,
        "target_endpoint": 5e-11,
        "target_residual": 1e-8,
    }, "V003 tolerance freeze")
    demand(value.get("capacity_extension") == {
        "hostile_maximum_degree": HOSTILE_DEGREE,
        "target_maximum_krylov_steps": TARGET_KRYLOV,
        "target_maximum_subdivisions": TARGET_SUBDIVISIONS,
    }, "V003 capacity freeze")
    return value


def normalized_resource(source: dict[str, Any], role: str) -> dict[str, Any]:
    resource = source.get("resource")
    demand(isinstance(resource, dict), f"{role}: resource record")
    demand(resource.get("wall_limit_seconds") == WALL_LIMIT,
           f"{role}: 96-hour wall limit")
    demand(resource.get("passed") is True, f"{role}: resource pass")
    common = {
        "peak_logical_scratch_bytes": resource.get("peak_live_state_bytes"),
        "scratch_limit_bytes": 20 * 2**30,
        "peak_rss_bytes": resource.get("peak_rss_bytes"),
        "rss_limit_bytes": resource.get("rss_limit_bytes"),
        "wall_seconds": resource.get("wall_seconds"),
        "wall_limit_seconds": WALL_LIMIT,
        "passed": True,
    }
    if role == "target":
        common.update({
            "maximum_numerical_workset_bytes": resource.get(
                "maximum_numerical_workset_bytes"
            ),
            "numerical_workset_limit_bytes": 1_000_000_000,
        })
    else:
        common.update({
            "maximum_numerical_allocation_estimate_bytes": resource.get(
                "maximum_numerical_allocation_estimate_bytes"
            ),
            "numerical_workspace_limit_bytes": 1_400_000_000,
        })
    return common


def validate_repair_provenance(source: dict[str, Any], role: str,
                               freeze: dict[str, Any]) -> None:
    repair = source.get("numerical_repair")
    demand(isinstance(repair, dict), f"{role}: numerical repair record")
    demand(repair.get("physical_operator_changed") is False,
           f"{role}: physical operator changed")
    demand(repair.get("predicate_thresholds_changed") is False,
           f"{role}: predicate threshold changed")
    parallel = source.get("parallel_resource")
    demand(isinstance(parallel, dict), f"{role}: parallel resource record")
    demand(parallel.get("numerical_successor") == "V003",
           f"{role}: numerical successor identity")
    demand(parallel.get("physical_operator_changed") is False,
           f"{role}: parallel physics mutation")
    demand(parallel.get("admission_or_route_time_changed") is False,
           f"{role}: time mutation")
    demand(parallel.get("observable_or_threshold_changed") is False,
           f"{role}: observable or threshold mutation")
    sources = parallel.get("source_record")
    demand(isinstance(sources, dict) and sources == freeze.get("v003_source_record"),
           f"{role}: V003 source record")
    source_hash = canonical_digest(sources)
    demand(source.get("successor_source_manifest_sha256") == source_hash,
           f"{role}: V003 source-record digest")
    demand(source.get("launch_authorization_sha256") == source_hash,
           f"{role}: launch binding")
    if role == "target":
        demand(repair.get("target_max_subdivisions") == TARGET_SUBDIVISIONS,
               "target: subdivision capacity")
        demand(repair.get("coarse_checkpoints") == [12, 18, 24, 32, 48, 64, 80]
               and repair.get("fine_checkpoints") == [16, 24, 32, 48, 64, 80, 96],
               "target: checkpoint capacity")
        demand(repair.get("coarse_tolerance") == 2e-9
               and repair.get("fine_tolerance") == 5e-11,
               "target: unchanged tolerances")
    else:
        demand(repair.get("rough_checkpoints") == [16, 24, 32, 48, 64, 80, 96, 112]
               and repair.get("sharp_checkpoints") == [24, 32, 48, 64, 80, 96, 112, 128],
               "hostile: checkpoint capacity")
        demand(repair.get("rough_tolerance") == 3e-9
               and repair.get("sharp_tolerance") == 8e-11,
               "hostile: unchanged tolerances")
        demand(repair.get("sharp_resume_prefix") == 11,
               "hostile: resume-prefix identity")


def project_target(source: dict[str, Any], base: Any,
                   freeze: dict[str, Any]) -> dict[str, Any]:
    demand(source.get("schema") == TARGET_SCHEMA, "target V003 schema")
    validate_repair_provenance(source, "target", freeze)
    value = dict(source)
    value.update({
        "schema": base.TARGET_SCHEMA,
        "representation": base.REPRESENTATION,
        "lineage_authority": base.LINEAGE_AUTHORITY,
        "implementation_sha256": base.EXPECTED_DEPENDENCIES[
            "../DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py"
        ],
        "method_sha256": base.EXPECTED_DEPENDENCIES[
            "../DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/Q_SHARDED_TARGET_METHOD_V004.md"
        ],
        "resource": normalized_resource(source, "target"),
        "v003_process_schema": TARGET_SCHEMA,
    })
    return value


def project_hostile(source: dict[str, Any], base: Any,
                    freeze: dict[str, Any]) -> dict[str, Any]:
    demand(source.get("schema") == HOSTILE_SCHEMA, "hostile V003 schema")
    validate_repair_provenance(source, "hostile", freeze)
    preserved_hash = digest(V002_SHARP)
    demand(freeze.get("hostile_v002_sharp_summary_sha256") == preserved_hash,
           "hostile preserved sharp-summary custody")
    preserved = json.loads(V002_SHARP.read_text()).get("payload")
    demand(isinstance(preserved, dict), "hostile preserved sharp-summary payload")
    rows = source.get("rows")
    demand(isinstance(rows, list) and len(rows) == 12,
           "hostile V003 row census")
    demand(rows[:11] == preserved.get("rows", [])[:11],
           "hostile resumed sharp prefix rows changed")
    demand(source["numerical_repair"].get("resumed_sharp_summary_sha256") == preserved_hash,
           "hostile resumed sharp-summary binding")
    terminal_actual = rows[-1].get("actual_solver")
    demand(isinstance(terminal_actual, dict), "hostile terminal actual solver")
    value = dict(source)
    value.update({
        "schema": base.HOSTILE_SCHEMA,
        "full_dimension": source.get("dimension"),
        "largest_materialized_dimension": source.get("preterminal_dimension"),
        "edge_layout": preserved.get("edge_layout"),
        "representation": base.REPRESENTATION,
        "lineage_authority": base.LINEAGE_AUTHORITY,
        "implementation_sha256": base.EXPECTED_DEPENDENCIES[
            "independent_prefix_history_v003.py"
        ],
        "method_sha256": base.EXPECTED_DEPENDENCIES[
            "V003_L12_EXECUTABLE_METHOD.md"
        ],
        "l10_gate_sha256": base.EXPECTED_DEPENDENCIES["L10_GATE_V002.json"],
        "terminal_support": {
            "child0_entries": terminal_actual.get("terminal_child0_entries"),
            "child1_nonzero_admission_entries": terminal_actual.get(
                "terminal_child1_nonzero_admission_entries"
            ),
            "full_terminal_array_allocated": terminal_actual.get(
                "full_terminal_array_allocated"
            ),
        },
        "resource": normalized_resource(source, "hostile"),
        "v003_process_schema": HOSTILE_SCHEMA,
    })
    return value


def solver_pass_factory(base: Any):
    def solver_pass(record: object, label: str, role: str, terminal: bool) -> None:
        base.demand(isinstance(record, dict), f"{label}: solver record")
        base.demand(record.get("converged") is True, f"{label}: solver unresolved")
        if role == "target":
            for field in (
                "batches", "low_memory_batches", "maximum_krylov_steps",
                "maximum_live_bytes", "maximum_subdivisions", "quadrature_nodes",
            ):
                base.demand(type(record.get(field)) is int and int(record[field]) >= 0,
                            f"{label}: integer {field}")
            base.demand(record["batches"] > 0 and 1 <= record["maximum_subdivisions"] <= TARGET_SUBDIVISIONS,
                        f"{label}: target batch/subdivision census")
            base.demand(record["low_memory_batches"] <= record["batches"],
                        f"{label}: target low-memory batch census")
            base.demand(record["maximum_krylov_steps"] <= TARGET_KRYLOV,
                        f"{label}: target Krylov cap")
            base.demand(record["maximum_live_bytes"] <= 1_000_000_000,
                        f"{label}: target workset cap")
            base.demand(record["quadrature_nodes"] == 24,
                        f"{label}: target quadrature")
            for field in ("maximum_exp_difference", "maximum_residual_indicator"):
                base.demand(base.finite(record.get(field)) and float(record[field]) >= 0.0,
                            f"{label}: finite {field}")
            base.demand(float(record["maximum_exp_difference"]) <= 5e-11,
                        f"{label}: target endpoint comparison")
            base.demand(float(record["maximum_residual_indicator"]) <= 1e-8,
                        f"{label}: target residual indicator")
        else:
            for field in (
                "allocation_limit_bytes", "allocation_vector_slots", "batches",
                "maximum_allocation_estimate_bytes", "maximum_degree",
                "quadrature_group_max", "quadrature_nodes",
            ):
                base.demand(type(record.get(field)) is int and int(record[field]) >= 0,
                            f"{label}: integer {field}")
            base.demand(record.get("algorithm") == "RECURRENCE_REPLAY_GL_GROUPS",
                        f"{label}: hostile algorithm")
            base.demand(record["batches"] > 0 and record["allocation_vector_slots"] == 20,
                        f"{label}: hostile batch/vector census")
            base.demand(record["allocation_limit_bytes"] == 1_400_000_000
                        and record["maximum_allocation_estimate_bytes"] <= 1_400_000_000,
                        f"{label}: hostile allocation cap")
            base.demand(record["maximum_degree"] <= HOSTILE_DEGREE
                        and record["quadrature_group_max"] == 12
                        and record["quadrature_nodes"] == 28,
                        f"{label}: hostile method caps")
            for field in ("maximum_endpoint_difference", "maximum_tail_indicator_32"):
                base.demand(base.finite(record.get(field)) and float(record[field]) >= 0.0,
                            f"{label}: finite {field}")
                base.demand(float(record[field]) <= 8e-11,
                            f"{label}: hostile {field}")
            if terminal and label.endswith("actual"):
                base.demand(record.get("terminal_children_streamed") is True,
                            f"{label}: hostile terminal stream")
                base.demand(record.get("terminal_child0_entries") == math.comb(35, 11),
                            f"{label}: hostile terminal child0 census")
                base.demand(record.get("terminal_child1_nonzero_admission_entries") == math.comb(34, 11),
                            f"{label}: hostile terminal child1 census")
                base.demand(record.get("full_terminal_array_allocated") is False,
                            f"{label}: hostile H12 nonallocation")
    return solver_pass


def resource_pass_factory(base: Any):
    def resource_pass(history: dict[str, Any], role: str) -> bool:
        record = history.get("resource")
        if not isinstance(record, dict):
            return False
        common = (
            type(record.get("peak_logical_scratch_bytes")) is int
            and type(record.get("scratch_limit_bytes")) is int
            and record["scratch_limit_bytes"] == 20 * 2**30
            and 0 <= record["peak_logical_scratch_bytes"] <= record["scratch_limit_bytes"]
            and type(record.get("peak_rss_bytes")) is int
            and type(record.get("rss_limit_bytes")) is int
            and record["rss_limit_bytes"] == 16 * 2**30
            and 0 <= record["peak_rss_bytes"] <= record["rss_limit_bytes"]
            and base.finite(record.get("wall_seconds"))
            and record.get("wall_limit_seconds") == WALL_LIMIT
            and 0.0 <= float(record["wall_seconds"]) <= WALL_LIMIT
            and record.get("passed") is True
        )
        if role == "target":
            return bool(common
                        and type(record.get("maximum_numerical_workset_bytes")) is int
                        and record.get("numerical_workset_limit_bytes") == 1_000_000_000
                        and 0 <= record["maximum_numerical_workset_bytes"] <= 1_000_000_000)
        return bool(common
                    and type(record.get("maximum_numerical_allocation_estimate_bytes")) is int
                    and record.get("numerical_workspace_limit_bytes") == 1_400_000_000
                    and 0 <= record["maximum_numerical_allocation_estimate_bytes"] <= 1_400_000_000)
    return resource_pass


def resolve_target_factory(base: Any):
    def resolve(root: Path, record: dict[str, Any], q: int) -> Path:
        path = Path(str(record.get("path"))).resolve()
        expected = (root / f"prefix_11/q_{q:02d}.npy").resolve()
        base.demand(path == expected and path.is_file(), f"target q{q}: canonical V003 shard")
        base.demand(record.get("shape") == list(base.shape(11, q)), f"target q{q}: shape")
        base.demand(record.get("bytes") == path.stat().st_size, f"target q{q}: bytes")
        base.demand(record.get("sha256") == digest(path), f"target q{q}: SHA-256")
        return path
    return resolve


def resolve_hostile_factory(base: Any):
    def resolve(root: Path, record: dict[str, Any], q: int) -> Path:
        path = Path(str(record.get("path"))).resolve()
        expected = (root / f"prefix_11/q_{q:02d}.c128").resolve()
        expected_bytes = 16 * math.prod(base.shape(11, q))
        base.demand(path == expected and path.is_file(), f"hostile q{q}: resumed V002 shard")
        base.demand(record.get("shape") == list(base.shape(11, q)), f"hostile q{q}: shape")
        base.demand(record.get("bytes") == expected_bytes == path.stat().st_size,
                    f"hostile q{q}: bytes")
        base.demand(record.get("sha256") == digest(path), f"hostile q{q}: SHA-256")
        return path
    return resolve


def run(arguments: argparse.Namespace) -> None:
    base = load_base()
    freeze = verify_freeze(arguments.freeze_sha256, base)
    original_checked = base.checked_result

    def checked(path: Path, expected: str, label: str) -> dict[str, Any]:
        source = original_checked(path, expected, label)
        return (project_target(source, base, freeze) if label == "target"
                else project_hostile(source, base, freeze))

    base.checked_result = checked
    base.solver_pass = solver_pass_factory(base)
    base.resource_pass = resource_pass_factory(base)
    base.resolve_target_shard = resolve_target_factory(base)
    base.resolve_hostile_shard = resolve_hostile_factory(base)
    base.EXECUTION_CUSTODY = CUSTODY
    base.verify_freeze = lambda expected: verify_freeze(expected, base)
    sys.argv = [
        str(BASE_PATH),
        "--target", str(arguments.target),
        "--target-sha256", arguments.target_sha256,
        "--hostile", str(arguments.hostile),
        "--hostile-sha256", arguments.hostile_sha256,
        "--target-terminal-root", str(arguments.target_terminal_root),
        "--hostile-terminal-root", str(arguments.hostile_terminal_root),
        "--freeze-sha256", arguments.freeze_sha256,
        "--blind-output", str(arguments.blind_output),
        "--output", str(arguments.output),
    ]
    base.main()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--target-sha256", required=True)
    parser.add_argument("--hostile", type=Path, required=True)
    parser.add_argument("--hostile-sha256", required=True)
    parser.add_argument("--target-terminal-root", type=Path, required=True)
    parser.add_argument("--hostile-terminal-root", type=Path, required=True)
    parser.add_argument("--freeze-sha256", required=True)
    parser.add_argument("--blind-output", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    try:
        run(parser.parse_args())
    except (RepairRefusal, OSError, ValueError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
