#!/usr/bin/env python3
"""Authorized L4-only hostile execution for the sealed scaling audit source.

This driver must finish and seal the independent output before any target
scaling result is opened.  It has no code path for L6 or L8.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import resource
import sys
import time
import warnings
from pathlib import Path
from typing import Any, Iterable, Mapping

import numpy as np

import independent_scaling_audit as audit


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUTHORIZATION = HERE / "L4_EXECUTION_AUTHORIZATION_V001.json"
EXECUTION_MANIFEST = HERE / "L4_EXECUTION_SOURCE_HASHES.sha256"
OUTPUT_DIR = HERE / "PHYSICAL_OUTPUTS"
RESULT = OUTPUT_DIR / "L4_HOSTILE_RECONSTRUCTION_V001.json"
RESULT_SIDECAR = OUTPUT_DIR / "L4_HOSTILE_RECONSTRUCTION_V001.json.sha256"
EXECUTION_RECORD = HERE / "L4_HOSTILE_EXECUTION_RECORD_V001.json"
RESULT_SEAL = HERE / "L4_HOSTILE_RESULT_SEAL_V001.json"
RESULT_MANIFEST = HERE / "L4_RESULT_HASHES.sha256"

LENGTH = 4
EVENTS = (0, 1, 2, 3)
BASE_TAU = 1.0e-10
DENSE_REFERENCE_TOLERANCE = 1.0e-8
CONTROL_TOLERANCE = 1.0e-9
EXPECTED_CORE_FREEZE_SHA256 = (
    "7eab0fc6be81cad9e7c5e732aac86f1f78dbed60fcbdf8d49387ad304eeb1aae"
)
EXPECTED_CORE_MANIFEST_SHA256 = (
    "883b4fe92a6a73b4d236373aa0a696c5da898177e9dc7f685ed20abfed23fac0"
)


class ExecutionFailure(RuntimeError):
    """An authorization, reconstruction, control, or publication failed."""


def array_sha256(array: np.ndarray, dtype: str) -> str:
    canonical = np.asarray(array, dtype=dtype, order="C")
    return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


def peak_rss_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else value * 1024


def require_finite_tree(value: Any, label: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            require_finite_tree(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            require_finite_tree(child, f"{label}[{index}]")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(float(value)):
            raise ExecutionFailure(f"non-finite scalar in {label}")


def output_paths() -> tuple[Path, ...]:
    return RESULT, RESULT_SIDECAR, EXECUTION_RECORD, RESULT_SEAL, RESULT_MANIFEST


def parse_manifest(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        if relative in entries or not audit.HASH_PATTERN.fullmatch(digest):
            raise ExecutionFailure("invalid or duplicate execution source manifest entry")
        entries[relative] = digest
    return entries


def preflight(require_outputs_absent: bool = True) -> dict[str, Any]:
    core = audit.verify_freeze(ROOT)
    if audit.sha256_file(audit.FREEZE) != EXPECTED_CORE_FREEZE_SHA256:
        raise ExecutionFailure("core source/input freeze identity changed")
    core_manifest = HERE / "SOURCE_HASHES.sha256"
    if audit.sha256_file(core_manifest) != EXPECTED_CORE_MANIFEST_SHA256:
        raise ExecutionFailure("core source manifest identity changed")
    authorization = audit.strict_json_bytes(AUTHORIZATION.read_bytes(), str(AUTHORIZATION))
    expected = {
        "schema": "AUDIT_LINEAGE_SCALING_L4_EXECUTION_AUTHORIZATION_V001",
        "authorization": "EXECUTE_AND_SEAL_HOSTILE_L4_ONLY",
        "L": LENGTH,
        "source_input_freeze_sha256": EXPECTED_CORE_FREEZE_SHA256,
        "source_manifest_sha256": EXPECTED_CORE_MANIFEST_SHA256,
        "target_lane_read_before_hostile_seal_authorized": False,
        "L6_authorized": False,
        "L8_authorized": False,
    }
    for key, value in expected.items():
        if authorization.get(key) != value:
            raise ExecutionFailure(f"authorization mismatch for {key}")
    if authorization.get("driver_sha256") != audit.sha256_file(Path(__file__)):
        raise ExecutionFailure("authorization does not pin this L4 driver")
    manifest = parse_manifest(EXECUTION_MANIFEST)
    required_manifest = {
        AUTHORIZATION.relative_to(ROOT).as_posix(): audit.sha256_file(AUTHORIZATION),
        Path(__file__).resolve().relative_to(ROOT).as_posix(): audit.sha256_file(Path(__file__)),
    }
    if manifest != required_manifest:
        raise ExecutionFailure("L4 execution source manifest mismatch")
    for relative, digest in manifest.items():
        if audit.sha256_file(ROOT / relative) != digest:
            raise ExecutionFailure(f"L4 execution source changed: {relative}")
    if require_outputs_absent:
        existing = [path.relative_to(ROOT).as_posix() for path in output_paths() if path.exists()]
        if existing:
            raise ExecutionFailure(f"refusing to overwrite existing L4 custody: {existing}")
    if core.get("target_lane_read_or_import_authorized") is not False:
        raise ExecutionFailure("core freeze no longer preserves target blindness")
    return authorization


def summarize_methods(records: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    records = list(records)
    if not records:
        return {
            "record_count": 0,
            "all_converged": True,
            "maximum_degree": 0,
            "maximum_endpoint_difference": 0.0,
            "maximum_tail_indicator_32": 0.0,
            "maximum_allocation_estimate_bytes": 0,
        }
    return {
        "record_count": len(records),
        "all_converged": all(bool(record.get("converged")) for record in records),
        "maximum_degree": max(int(record.get("degree", record.get("maximum_degree", 0))) for record in records),
        "maximum_endpoint_difference": max(
            float(record.get("endpoint_difference", record.get("maximum_endpoint_difference", 0.0)))
            for record in records
        ),
        "maximum_tail_indicator_32": max(
            float(record.get("tail_indicator_32", record.get("maximum_tail_indicator_32", 0.0)))
            for record in records
        ),
        "maximum_allocation_estimate_bytes": max(
            int(record.get("allocation_estimate_bytes", record.get("maximum_allocation_estimate_bytes", 0)))
            for record in records
        ),
    }


def factor_trace(block: audit.SignedCarrierBlock, sign: str) -> float:
    factors = block.positive if sign == "positive" else block.negative
    return float(np.sum(np.abs(factors) ** 2))


def per_sector_invariants(
    before: Mapping[int, audit.SignedCarrierBlock],
    after: Mapping[int, audit.SignedCarrierBlock],
) -> tuple[dict[str, Any], float]:
    records: dict[str, Any] = {}
    maximum = 0.0
    for q in range(LENGTH + 1):
        left = before[q]
        right = after[q]
        record = {
            "trace_distance_before": left.trace_distance(),
            "trace_distance_after": right.trace_distance(),
            "positive_trace_before": factor_trace(left, "positive"),
            "positive_trace_after": factor_trace(right, "positive"),
            "negative_trace_before": factor_trace(left, "negative"),
            "negative_trace_after": factor_trace(right, "negative"),
            "signed_trace_before": left.trace(),
            "signed_trace_after": right.trace(),
            "positive_rank_before": left.positive.shape[1],
            "positive_rank_after": right.positive.shape[1],
            "negative_rank_before": left.negative.shape[1],
            "negative_rank_after": right.negative.shape[1],
        }
        record["trace_distance_invariance_error"] = abs(
            record["trace_distance_before"] - record["trace_distance_after"]
        )
        record["positive_trace_invariance_error"] = abs(
            record["positive_trace_before"] - record["positive_trace_after"]
        )
        record["negative_trace_invariance_error"] = abs(
            record["negative_trace_before"] - record["negative_trace_after"]
        )
        maximum = max(
            maximum,
            float(record["trace_distance_invariance_error"]),
            float(record["positive_trace_invariance_error"]),
            float(record["negative_trace_invariance_error"]),
        )
        records[str(q)] = record
    return records, maximum


def reference_difference(observed: Mapping[str, Any], reference: Mapping[str, Any]) -> float:
    scalar_keys = (
        "carrier_trace_distance",
        "carrier_configuration_tv",
        "carrier_number_sector_tv",
        "occupation_rms",
        "delta_n_0",
    )
    difference = max(abs(float(observed[key]) - float(reference[key])) for key in scalar_keys)
    difference = max(
        difference,
        float(np.max(np.abs(np.asarray(observed["delta_n"]) - np.asarray(reference["delta_n"])))),
    )
    return difference


def build_result(runtime_warnings: list[dict[str, str]]) -> dict[str, Any]:
    authorization = preflight(require_outputs_absent=True)
    modules = audit.load_pinned_hostile_v002(ROOT)
    started = time.perf_counter()
    rss_before = peak_rss_bytes()
    basis, preterminal, preterminal_methods = audit.regenerate_preterminal_sharp_in_memory(
        LENGTH, modules
    )
    preterminal_descriptors = []
    for q, block in enumerate(preterminal.blocks):
        preterminal_descriptors.append({
            "q": q,
            "shape": list(block.shape),
            "dtype": np.asarray(block).dtype.str,
            "logical_bytes": int(block.nbytes),
            "sha256_canonical_c16": array_sha256(block, "<c16"),
        })
    terminal, terminal_methods = audit.materialize_terminal_owner_once_checkpoint(
        LENGTH, modules, basis, preterminal
    )
    terminal_descriptors = []
    checkpoint_norm = 0.0
    for q in range(LENGTH + 1):
        block = terminal[q]
        checkpoint_norm += float(np.vdot(block, block).real)
        terminal_descriptors.append({
            "q": q,
            "shape": list(block.shape),
            "dtype": block.dtype.str,
            "logical_bytes": int(block.nbytes),
            "sha256_canonical_c16": array_sha256(block, "<c16"),
            "lineage_words_sha256_u4": array_sha256(
                audit.fixed_weight_words(LENGTH, q), "<u4"
            ),
            "carrier_words_sha256_u4": array_sha256(
                audit.fixed_weight_words(2 * LENGTH, q), "<u4"
            ),
        })

    freeze = audit.strict_json_bytes(audit.FREEZE.read_bytes(), str(audit.FREEZE))
    reference = freeze["dense_l4_independent_reference"]["fine_registered_observables"]
    events: list[dict[str, Any]] = []
    all_transport_methods: list[Mapping[str, Any]] = []
    maximum_control = abs(checkpoint_norm - 1.0)
    all_event_controls_pass = True
    for event in EVENTS:
        admitted, algebra_controls = audit.build_revisit_signed_blocks(terminal, LENGTH, event)
        after_admission = audit.summarize_observables(admitted, LENGTH)
        transported, transport_methods = audit.transport_signed_blocks_with_hostile_v002(
            admitted, modules, LENGTH
        )
        all_transport_methods.extend(transport_methods)
        after_transport = audit.summarize_observables(transported, LENGTH)
        sectors, sector_invariance = per_sector_invariants(admitted, transported)
        trace_invariance = abs(
            float(after_admission["carrier_trace_distance"])
            - float(after_transport["carrier_trace_distance"])
        )
        number_sector_invariance = abs(
            float(after_admission["carrier_number_sector_tv"])
            - float(after_transport["carrier_number_sector_tv"])
        )
        reference_linf = reference_difference(after_transport, reference) if event == 0 else None
        local_controls = max(
            abs(float(algebra_controls["maximum_checkpoint_svd_reconstruction_frobenius"])),
            abs(float(algebra_controls["maximum_discarded_amplitude_frobenius"])),
            abs(float(algebra_controls["maximum_fixed_q_lineage_bit_coherence"])),
            abs(float(algebra_controls["signed_trace_after_admission"])),
            abs(float(algebra_controls["discarded_density_trace_bound"])),
            abs(float(after_transport["signed_trace"])),
            trace_invariance,
            number_sector_invariance,
            sector_invariance,
        )
        maximum_control = max(maximum_control, local_controls)
        tau = max(BASE_TAU, 100.0 * local_controls)
        delta_c = float(after_transport["carrier_trace_distance"])
        t_dyn = delta_c / tau
        controls_pass = (
            local_controls <= CONTROL_TOLERANCE
            and (reference_linf is None or reference_linf <= DENSE_REFERENCE_TOLERANCE)
            and delta_c >= 0.0
            and t_dyn > 1.0
        )
        classification = (
            "RESOLVED_L4_EVENT_LINEAGE_SENSITIVE_CARRIER_CONTINUATION"
            if controls_pass
            else "UNRESOLVED_L4_EVENT_LINEAGE_SENSITIVE_CARRIER_CONTINUATION"
        )
        all_event_controls_pass = all_event_controls_pass and controls_pass
        events.append({
            "event": event,
            "checkpoint": "AFTER_FINAL_OWNER_ONCE_EVENT_TRANSPORT_BEFORE_INDEPENDENT_REVISIT",
            "after_admission": after_admission,
            "after_transport": after_transport,
            "algebra_controls": algebra_controls,
            "per_sector_invariants": sectors,
            "maximum_local_control": local_controls,
            "trace_distance_transport_invariance_error": trace_invariance,
            "number_sector_tv_transport_invariance_error": number_sector_invariance,
            "maximum_per_sector_invariance_error": sector_invariance,
            "dense_independent_L4_reference_linf": reference_linf,
            "tau": tau,
            "T_dyn": t_dyn,
            "controls_pass": controls_pass,
            "classification": classification,
        })

    preterminal_summary = summarize_methods(preterminal_methods)
    terminal_summary = summarize_methods(terminal_methods)
    transport_summary = summarize_methods(all_transport_methods)
    method_pass = all(
        bool(record["all_converged"])
        for record in (preterminal_summary, terminal_summary, transport_summary)
    )
    overall_pass = (
        all_event_controls_pass
        and method_pass
        and not runtime_warnings
        and abs(checkpoint_norm - 1.0) <= CONTROL_TOLERANCE
    )
    elapsed = time.perf_counter() - started
    result = {
        "schema": "INDEPENDENT_L4_ALL_EVENT_LINEAGE_SENSITIVE_SCALING_AUDIT_V001",
        "passed": overall_pass,
        "disposition": (
            "PASS_HOSTILE_L4_ALL_EVENT_LINEAGE_SENSITIVE_RECONSTRUCTION"
            if overall_pass
            else "UNRESOLVED_HOSTILE_L4_ALL_EVENT_LINEAGE_SENSITIVE_RECONSTRUCTION"
        ),
        "classification": (
            "RESOLVED_L4_ALL_EVENT_LINEAGE_SENSITIVE_SCALING_BASELINE"
            if overall_pass
            else "UNRESOLVED_L4_ALL_EVENT_LINEAGE_SENSITIVE_SCALING_BASELINE"
        ),
        "claim_boundary": "INDEPENDENT_L4_ALL_EVENT_FINITE_RESPONSE_BASELINE_ONLY__NO_L6_L8_SCALING_EXPONENT_ALL_L_CURVATURE_GEOMETRY_RGRL_WTC_ALPHA_COSMOLOGY_OR_GRAVITY",
        "L": LENGTH,
        "events": events,
        "fixed_parameters": {
            "angle": "pi/4",
            "dwell": "pi/2",
            "base_tau": BASE_TAU,
            "control_tolerance": CONTROL_TOLERANCE,
            "dense_reference_tolerance": DENSE_REFERENCE_TOLERANCE,
            "revisit_policy": "EACH_EVENT_FROM_THE_SAME_AUTHENTICATED_TERMINAL_CHECKPOINT",
        },
        "custody": {
            "source_input_freeze_sha256": audit.sha256_file(audit.FREEZE),
            "source_manifest_sha256": audit.sha256_file(HERE / "SOURCE_HASHES.sha256"),
            "execution_authorization_sha256": audit.sha256_file(AUTHORIZATION),
            "execution_source_manifest_sha256": audit.sha256_file(EXECUTION_MANIFEST),
            "driver_sha256": audit.sha256_file(Path(__file__)),
            "hostile_v002_sha256": audit.PINNED_HOSTILE_V002[
                "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history_v002.py"
            ],
            "target_lane_read_or_imported": False,
            "target_output_read": False,
            "authorization": authorization["authorization"],
        },
        "checkpoint": {
            "preterminal_prefix": LENGTH - 1,
            "preterminal_shards": preterminal_descriptors,
            "terminal_q_blocks": terminal_descriptors,
            "terminal_norm": checkpoint_norm,
            "terminal_norm_error": abs(checkpoint_norm - 1.0),
            "representation": "HOSTILE_V002_REVERSED_MASKS__MATERIALIZED_FINAL_OWNER_ONCE_Q_BLOCKS",
        },
        "methods": {
            "preterminal": preterminal_summary,
            "terminal_owner_once": terminal_summary,
            "all_revisit_transports": transport_summary,
            "all_converged": method_pass,
        },
        "controls": {
            "all_event_controls_pass": all_event_controls_pass,
            "maximum_control": maximum_control,
            "dense_event0_reference_pass": events[0]["dense_independent_L4_reference_linf"]
            <= DENSE_REFERENCE_TOLERANCE,
            "runtime_warnings": runtime_warnings,
            "floating_point_policy": "DIVIDE_OVERFLOW_INVALID_RAISE__UNDERFLOW_IGNORED",
        },
        "resources": {
            "wall_seconds": elapsed,
            "peak_rss_before_bytes": rss_before,
            "peak_rss_bytes": peak_rss_bytes(),
            "preterminal_logical_bytes": sum(item["logical_bytes"] for item in preterminal_descriptors),
            "terminal_checkpoint_logical_bytes": sum(item["logical_bytes"] for item in terminal_descriptors),
            "persisted_checkpoint_bytes": 0,
            "energy_accounting_assumption": "ENERGY_NOT_METERED__REPORTS_WALL_RSS_AND_LOGICAL_STORAGE_ONLY",
        },
        "runtime": {
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "interpretation": {
            "status": "FINITE_L4_BASELINE_ONLY",
            "physics_reconstruction_incomplete": False,
            "L6_authorized": False,
            "L8_authorized": False,
            "target_reconciliation_performed": False,
        },
    }
    require_finite_tree(result)
    if not overall_pass:
        raise ExecutionFailure(json.dumps(result["controls"], sort_keys=True))
    return result


def publish(result: dict[str, Any]) -> dict[str, str]:
    rendered = audit.canonical_json_bytes(result)
    result_hash = audit.atomic_create(RESULT, rendered)
    relative_result = RESULT.relative_to(ROOT).as_posix()
    sidecar_hash = audit.atomic_create(
        RESULT_SIDECAR,
        f"{result_hash}  {relative_result}\n".encode("utf-8"),
    )
    record = {
        "schema": "AUDIT_LINEAGE_SCALING_L4_HOSTILE_EXECUTION_RECORD_V001",
        "status": "SEALED_HOSTILE_L4_RESULT",
        "result_path": relative_result,
        "result_sha256": result_hash,
        "result_size_bytes": RESULT.stat().st_size,
        "result_sidecar_sha256": sidecar_hash,
        "source_input_freeze_sha256": audit.sha256_file(audit.FREEZE),
        "execution_authorization_sha256": audit.sha256_file(AUTHORIZATION),
        "execution_source_manifest_sha256": audit.sha256_file(EXECUTION_MANIFEST),
        "driver_sha256": audit.sha256_file(Path(__file__)),
        "target_lane_read_or_imported": False,
        "target_output_read": False,
        "L6_executed": False,
        "L8_executed": False,
        "resources": result["resources"],
        "classification": result["classification"],
        "disposition": result["disposition"],
    }
    record_hash = audit.atomic_create(EXECUTION_RECORD, audit.canonical_json_bytes(record))
    seal = {
        "schema": "AUDIT_LINEAGE_SCALING_L4_HOSTILE_RESULT_SEAL_V001",
        "status": "SEALED_BEFORE_TARGET_UNBLINDING",
        "result_sha256": result_hash,
        "result_sidecar_sha256": sidecar_hash,
        "execution_record_sha256": record_hash,
        "source_input_freeze_sha256": audit.sha256_file(audit.FREEZE),
        "driver_sha256": audit.sha256_file(Path(__file__)),
        "target_output_read_before_seal": False,
    }
    seal_hash = audit.atomic_create(RESULT_SEAL, audit.canonical_json_bytes(seal))
    entries = (
        (result_hash, RESULT),
        (sidecar_hash, RESULT_SIDECAR),
        (record_hash, EXECUTION_RECORD),
        (seal_hash, RESULT_SEAL),
    )
    manifest_payload = "".join(
        f"{digest}  {path.relative_to(ROOT).as_posix()}\n" for digest, path in entries
    ).encode("utf-8")
    manifest_hash = audit.atomic_create(RESULT_MANIFEST, manifest_payload)
    return {
        "result_sha256": result_hash,
        "result_sidecar_sha256": sidecar_hash,
        "execution_record_sha256": record_hash,
        "result_seal_sha256": seal_hash,
        "result_manifest_sha256": manifest_hash,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--preflight", action="store_true")
    action.add_argument("--execute", action="store_true")
    arguments = parser.parse_args()
    if arguments.preflight:
        authorization = preflight(require_outputs_absent=True)
        print(json.dumps({
            "status": "PASS_L4_HOSTILE_EXECUTION_PREFLIGHT",
            "authorization_sha256": audit.sha256_file(AUTHORIZATION),
            "driver_sha256": audit.sha256_file(Path(__file__)),
            "authorization": authorization["authorization"],
        }, sort_keys=True))
        return
    old = np.seterr(divide="raise", over="raise", invalid="raise", under="ignore")
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            warning_records: list[dict[str, str]] = []
            # build_result captures no target data; warnings are supplied after
            # the controlled run and are required to remain empty.
            result = build_result(warning_records)
            warning_records.extend(
                {"category": item.category.__name__, "message": str(item.message)}
                for item in caught
            )
            if warning_records:
                raise ExecutionFailure(f"runtime warning refusal: {warning_records}")
        hashes = publish(result)
    finally:
        np.seterr(**old)
    print(json.dumps({
        "status": "PASS_SEALED_HOSTILE_L4_RESULT",
        **hashes,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
