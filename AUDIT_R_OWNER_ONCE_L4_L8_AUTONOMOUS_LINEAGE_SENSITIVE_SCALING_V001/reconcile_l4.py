#!/usr/bin/env python3
"""Post-seal target/hostile reconciliation for the authorized L4 result."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Mapping

import independent_scaling_audit as audit_tools


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET_RESULT = (
    ROOT
    / "DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V001"
    / "PHYSICAL_OUTPUTS/L4_TARGET_REPRODUCTION_V001.json"
)
HOSTILE_RESULT = HERE / "PHYSICAL_OUTPUTS/L4_HOSTILE_RECONSTRUCTION_V001.json"
HOSTILE_SEAL = HERE / "L4_HOSTILE_RESULT_SEAL_V001.json"
FREEZE = HERE / "L4_RECONCILIATION_FREEZE_V001.json"
SOURCE_MANIFEST = HERE / "L4_RECONCILIATION_SOURCE_HASHES.sha256"
OUTPUT = HERE / "L4_TARGET_HOSTILE_RECONCILIATION_V001.json"
OUTPUT_SIDECAR = HERE / "L4_TARGET_HOSTILE_RECONCILIATION_V001.json.sha256"
REPORT = HERE / "L4_TARGET_HOSTILE_RECONCILIATION_V001.md"
OUTPUT_MANIFEST = HERE / "L4_RECONCILIATION_OUTPUT_HASHES.sha256"

TARGET_SHA256 = "509d96ad59268cd75ee3b1275fd095b4b8642d498750e81b9d145374c6ac8c4c"
HOSTILE_SHA256 = "8f46b0a64f49591650613c0b2a4f2032156ce96fce8b1267f36fe6d50db61756"
HOSTILE_SEAL_SHA256 = "0add3a7197dcdda0a67e2e6f5469fa28ef5de48a73eed02ee3b13968392dae62"
TOLERANCE = 1.0e-10


class ReconciliationFailure(RuntimeError):
    """A sealed input, comparison, or output-custody check failed."""


def finite(value: Any, label: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            finite(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            finite(child, f"{label}[{index}]")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(float(value)):
            raise ReconciliationFailure(f"non-finite value in {label}")


def load_exact(path: Path, expected_sha256: str) -> dict[str, Any]:
    observed = audit_tools.sha256_file(path)
    if observed != expected_sha256:
        raise ReconciliationFailure(f"sealed input changed: {path}: {observed}")
    value = audit_tools.strict_json_bytes(path.read_bytes(), str(path))
    if not isinstance(value, dict):
        raise ReconciliationFailure(f"sealed input is not a JSON object: {path}")
    finite(value, path.name)
    return value


def comparison(
    field: str,
    target: float,
    hostile: float,
    tolerance: float = TOLERANCE,
) -> dict[str, Any]:
    difference = abs(float(target) - float(hostile))
    return {
        "field": field,
        "target": float(target),
        "hostile": float(hostile),
        "absolute_difference": difference,
        "tolerance": tolerance,
        "passed": difference <= tolerance,
    }


def scalar_and_vector_comparisons(
    target: Mapping[str, Any], hostile: Mapping[str, Any], checkpoint: str
) -> list[dict[str, Any]]:
    records = []
    for key in (
        "carrier_trace_distance",
        "carrier_configuration_tv",
        "carrier_number_sector_tv",
        "occupation_rms",
        "delta_n_0",
    ):
        records.append(comparison(f"{checkpoint}.{key}", target[key], hostile[key]))
    if len(target["delta_n"]) != len(hostile["delta_n"]):
        raise ReconciliationFailure(f"{checkpoint} delta_n length mismatch")
    for index, (left, right) in enumerate(zip(target["delta_n"], hostile["delta_n"])):
        records.append(comparison(f"{checkpoint}.delta_n[{index}]", left, right))
    return records


def target_sector_map(target: Mapping[str, Any]) -> dict[int, Mapping[str, Any]]:
    sectors = {int(record["q_out"]): record for record in target["sector_results"]}
    if sorted(sectors) != list(range(5)):
        raise ReconciliationFailure("target sector census is incomplete")
    return sectors


def semantic_classification(target: Mapping[str, Any], hostile: Mapping[str, Any]) -> dict[str, Any]:
    hostile_event = hostile["events"][0]
    target_pass = (
        target.get("classification") == "PASS_DENSE_L4_TARGET_REPRODUCTION"
        and target.get("status") == "L4_ONLY__L6_L8_EXECUTION_LOCKED"
        and target.get("controls", {}).get("passed") is True
    )
    hostile_pass = (
        hostile_event.get("classification")
        == "RESOLVED_L4_EVENT_LINEAGE_SENSITIVE_CARRIER_CONTINUATION"
        and hostile.get("classification")
        == "RESOLVED_L4_ALL_EVENT_LINEAGE_SENSITIVE_SCALING_BASELINE"
        and hostile.get("disposition")
        == "PASS_HOSTILE_L4_ALL_EVENT_LINEAGE_SENSITIVE_RECONSTRUCTION"
        and hostile_event.get("controls_pass") is True
        and hostile.get("controls", {}).get("all_event_controls_pass") is True
        and hostile.get("passed") is True
    )
    return {
        "target_classification": target.get("classification"),
        "target_status": target.get("status"),
        "hostile_event0_classification": hostile_event.get("classification"),
        "hostile_overall_classification": hostile.get("classification"),
        "hostile_overall_disposition": hostile.get("disposition"),
        "classification_strings_equal": target.get("classification")
        == hostile_event.get("classification"),
        "typed_meaning": "TARGET_REPRODUCES_DENSE_L4__HOSTILE_RESOLVES_THE_SAME_EVENT0_RESPONSE",
        "semantic_disposition_compatible": target_pass and hostile_pass,
    }


def build_reconciliation(target: Mapping[str, Any], hostile: Mapping[str, Any]) -> dict[str, Any]:
    if target.get("schema") != "L4_L8_TARGET_LINEAGE_SENSITIVE_SCALING_RESULT_V001":
        raise ReconciliationFailure("unexpected target schema")
    if hostile.get("schema") != "INDEPENDENT_L4_ALL_EVENT_LINEAGE_SENSITIVE_SCALING_AUDIT_V001":
        raise ReconciliationFailure("unexpected hostile schema")
    if target.get("L") != 4 or hostile.get("L") != 4 or target.get("event") != 0:
        raise ReconciliationFailure("reconciliation is restricted to target L4 event 0")
    event0 = hostile["events"][0]
    if event0.get("event") != 0:
        raise ReconciliationFailure("hostile event zero is not first")

    registered: list[dict[str, Any]] = []
    for checkpoint in ("after_admission", "after_transport"):
        registered.extend(
            scalar_and_vector_comparisons(
                target[checkpoint], event0[checkpoint], checkpoint
            )
        )
    registered.append(comparison("tau", target["tau"], event0["tau"], 0.0))
    # T_dyn = Delta_C / tau.  Propagate the registered Delta_C-scale
    # absolute tolerance through that division instead of incorrectly
    # applying a dimensionless 1e-10 threshold to an O(1e9) quantity.
    t_dyn_tolerance = TOLERANCE / float(target["tau"])
    registered.append(
        comparison("T_dyn", target["T_dyn"], event0["T_dyn"], t_dyn_tolerance)
    )

    sectors_target = target_sector_map(target)
    sector_records: list[dict[str, Any]] = []
    sector_comparisons: list[dict[str, Any]] = []
    for q in range(5):
        target_q = sectors_target[q]
        hostile_q = event0["per_sector_invariants"][str(q)]
        local: list[dict[str, Any]] = []
        for checkpoint, target_phase, hostile_suffix in (
            ("after_admission", target_q["after_admission"], "before"),
            ("after_transport", target_q["after_transport"], "after"),
        ):
            local.extend((
                comparison(
                    f"q{q}.{checkpoint}.carrier_trace_distance",
                    target_phase["carrier_trace_distance"],
                    hostile_q[f"trace_distance_{hostile_suffix}"],
                ),
                comparison(
                    f"q{q}.{checkpoint}.trace_actual",
                    target_phase["trace_actual"],
                    hostile_q[f"positive_trace_{hostile_suffix}"],
                ),
                comparison(
                    f"q{q}.{checkpoint}.trace_product",
                    target_phase["trace_product"],
                    hostile_q[f"negative_trace_{hostile_suffix}"],
                ),
                comparison(
                    f"q{q}.{checkpoint}.signed_trace",
                    float(target_phase["trace_actual"]) - float(target_phase["trace_product"]),
                    hostile_q[f"signed_trace_{hostile_suffix}"],
                ),
            ))
        local.append(comparison(
            f"q{q}.trace_distance_transport_invariance",
            target_q["controls"]["trace_distance_transport_invariance"],
            hostile_q["trace_distance_invariance_error"],
        ))
        sector_comparisons.extend(local)
        sector_records.append({
            "q": q,
            "common_invariant_comparisons": local,
            "all_common_invariants_pass": all(item["passed"] for item in local),
            "target_only_diagnostics_without_presealed_hostile_counterpart": {
                "after_admission_carrier_configuration_tv": target_q["after_admission"][
                    "carrier_configuration_tv"
                ],
                "after_transport_carrier_configuration_tv": target_q["after_transport"][
                    "carrier_configuration_tv"
                ],
                "after_admission_delta_n": target_q["after_admission"]["delta_n"],
                "after_transport_delta_n": target_q["after_transport"]["delta_n"],
                "target_factor_columns_actual": target_q["after_transport"]["controls"][
                    "factor_columns_actual"
                ],
                "target_factor_columns_product": target_q["after_transport"]["controls"][
                    "factor_columns_product"
                ],
                "target_reduced_dimension": target_q["after_transport"]["controls"][
                    "reduced_dimension"
                ],
                "reason_not_compared": "HOSTILE_PRESEAL_RESULT_REGISTERED_AGGREGATE_CONFIGURATION_AND_OCCUPATION_FIELDS_PLUS_SECTOR_TRACE_INVARIANTS__NOT_PER_SECTOR_CONFIGURATION_OR_OCCUPATION",
            },
            "representation_specific_ranks_not_expected_to_match": {
                "target_actual": target_q["after_transport"]["controls"]["factor_columns_actual"],
                "target_product": target_q["after_transport"]["controls"]["factor_columns_product"],
                "hostile_positive": hostile_q["positive_rank_after"],
                "hostile_negative": hostile_q["negative_rank_after"],
            },
        })

    weight_comparisons: list[dict[str, Any]] = []
    for checkpoint, suffix in (("after_admission", "before"), ("after_transport", "after")):
        target_actual = target[checkpoint]["sector_weights_actual"]
        target_product = target[checkpoint]["sector_weights_product"]
        for q in range(5):
            hostile_q = event0["per_sector_invariants"][str(q)]
            weight_comparisons.extend((
                comparison(
                    f"{checkpoint}.sector_weights_actual[{q}]",
                    target_actual[q],
                    hostile_q[f"positive_trace_{suffix}"],
                ),
                comparison(
                    f"{checkpoint}.sector_weights_product[{q}]",
                    target_product[q],
                    hostile_q[f"negative_trace_{suffix}"],
                ),
            ))
    registered.extend(weight_comparisons)
    registered.extend(sector_comparisons)
    maximum_difference = max(item["absolute_difference"] for item in registered)
    maximum_base_scale_difference = max(
        item["absolute_difference"]
        for item in registered
        if item["field"] != "T_dyn"
    )
    maximum_tolerance_fraction = max(
        (
            item["absolute_difference"] / item["tolerance"]
            if item["tolerance"] > 0.0
            else 0.0
        )
        for item in registered
    )
    numerical_pass = all(item["passed"] for item in registered)
    classification = semantic_classification(target, hostile)

    target_rss = max(
        int(target["resource"]["peak_child_rss_bytes"]),
        int(target["resource"]["peak_parent_rss_bytes"]),
    )
    hostile_rss = int(hostile["resources"]["peak_rss_bytes"])
    resources = {
        "target": {
            "wall_seconds": target["resource"]["wall_seconds"],
            "peak_rss_bytes": target_rss,
            "authenticated_preterminal_input_bytes": target["resource"][
                "authenticated_preterminal_input_bytes"
            ],
            "persisted_checkpoint_storage_bytes": target["resource"][
                "checkpoint_storage_bytes"
            ],
            "result_size_bytes": TARGET_RESULT.stat().st_size,
        },
        "hostile": {
            "wall_seconds": hostile["resources"]["wall_seconds"],
            "peak_rss_bytes": hostile_rss,
            "preterminal_logical_bytes": hostile["resources"]["preterminal_logical_bytes"],
            "terminal_checkpoint_logical_bytes": hostile["resources"][
                "terminal_checkpoint_logical_bytes"
            ],
            "persisted_checkpoint_bytes": hostile["resources"]["persisted_checkpoint_bytes"],
            "result_size_bytes": HOSTILE_RESULT.stat().st_size,
            "energy_accounting_assumption": hostile["resources"][
                "energy_accounting_assumption"
            ],
        },
        "comparison": {
            "wall_seconds_hostile_minus_target": float(hostile["resources"]["wall_seconds"])
            - float(target["resource"]["wall_seconds"]),
            "wall_seconds_hostile_over_target": float(hostile["resources"]["wall_seconds"])
            / float(target["resource"]["wall_seconds"]),
            "peak_rss_hostile_minus_target_bytes": hostile_rss - target_rss,
            "peak_rss_hostile_over_target": hostile_rss / target_rss,
            "storage_values_are_not_like_for_like": True,
            "storage_note": "TARGET_RETAINED_A_PERSISTED_RESTART_CHECKPOINT__HOSTILE_USED_IN_MEMORY_CHECKPOINTS_AND_PERSISTED_ONLY_RESULT_CUSTODY",
        },
    }

    audit_only_events = []
    for event in hostile["events"][1:]:
        audit_only_events.append({
            "event": event["event"],
            "classification": event["classification"],
            "controls_pass": event["controls_pass"],
            "after_admission": event["after_admission"],
            "after_transport": event["after_transport"],
            "tau": event["tau"],
            "T_dyn": event["T_dyn"],
            "target_counterpart": "ABSENT_FROM_AUTHORIZED_TARGET_L4_RESULT",
        })

    passed = numerical_pass and classification["semantic_disposition_compatible"]
    result = {
        "schema": "L4_TARGET_HOSTILE_LINEAGE_SENSITIVE_RECONCILIATION_V001",
        "passed": passed,
        "disposition": (
            "PASS_TARGET_HOSTILE_L4_EVENT0_NUMERICAL_RECONCILIATION__AUDIT_ONLY_EVENTS1_3_NOT_CROSS_RECONCILED"
            if passed
            else "FAIL_TARGET_HOSTILE_L4_EVENT0_RECONCILIATION"
        ),
        "claim_boundary": "TARGET_HOSTILE_AGREEMENT_FOR_L4_EVENT0_ONLY__HOSTILE_EVENTS1_3_HAVE_NO_TARGET_COUNTERPART__NO_L6_L8_PERSISTENCE_SCALING_EXPONENT_ALL_L_CURVATURE_GEOMETRY_RGRL_WTC_ALPHA_COSMOLOGY_OR_GRAVITY",
        "input_hashes": {
            "target_result_sha256": TARGET_SHA256,
            "hostile_result_sha256": HOSTILE_SHA256,
            "hostile_result_seal_sha256": HOSTILE_SEAL_SHA256,
        },
        "target_hostile_blinding": {
            "hostile_result_sealed_before_target_read": True,
            "hostile_result_seal_status": "SEALED_BEFORE_TARGET_UNBLINDING",
            "target_event_available": 0,
            "target_events_absent": [1, 2, 3],
        },
        "execution_scope": {
            "target_status": target["status"],
            "target_L": target["L"],
            "target_event": target["event"],
            "hostile_L": hostile["L"],
            "hostile_events": [event["event"] for event in hostile["events"]],
            "L6_executed": False,
            "L8_executed": False,
        },
        "tolerance": TOLERANCE,
        "tolerance_policy": {
            "base_absolute_tolerance": TOLERANCE,
            "tau_tolerance": 0.0,
            "T_dyn_propagated_absolute_tolerance": t_dyn_tolerance,
            "T_dyn_rule": "BASE_ABSOLUTE_TOLERANCE_DIVIDED_BY_EXACT_TAU",
        },
        "registered_comparisons": registered,
        "maximum_registered_absolute_difference": maximum_difference,
        "maximum_non_T_dyn_absolute_difference": maximum_base_scale_difference,
        "maximum_registered_tolerance_fraction": maximum_tolerance_fraction,
        "all_registered_common_fields_pass": numerical_pass,
        "classification_reconciliation": classification,
        "per_sector_reconciliation": sector_records,
        "resources": resources,
        "audit_only_events": audit_only_events,
        "interpretation": {
            "established": "INDEPENDENT_TARGET_HOSTILE_REPRODUCTION_OF_THE_L4_EVENT0_LINEAGE_SENSITIVE_CARRIER_RESPONSE",
            "not_established": [
                "TARGET_HOSTILE_ALL_EVENT_L4_AGREEMENT",
                "L6_OR_L8_PERSISTENCE",
                "FINITE_SIZE_SCALING_EXPONENT",
                "ALL_L_OR_CONTINUUM_RESPONSE",
                "CURVATURE_GEOMETRY_OR_GRAVITY",
            ],
            "per_sector_target_only_diagnostics_affect_gate": False,
            "reason": "THEY_LACKED_PRESEALED_HOSTILE_COUNTERPARTS__AGGREGATE_REGISTERED_OBSERVABLES_AND_COMMON_SECTOR_TRACE_INVARIANTS_ARE_EXACTLY_COMPARED",
        },
    }
    finite(result)
    return result


def report_markdown(result: Mapping[str, Any]) -> str:
    resources = result["resources"]
    lines = [
        "# L4 target/hostile lineage-response reconciliation",
        "",
        f"Disposition: `{result['disposition']}`.",
        "",
        f"Target result SHA-256: `{TARGET_SHA256}`.",
        f"Hostile result SHA-256: `{HOSTILE_SHA256}`.",
        f"Hostile pre-unblinding seal SHA-256: `{HOSTILE_SEAL_SHA256}`.",
        "",
        "## Numerical gate",
        "",
        f"All common registered fields pass with base absolute tolerance `{result['tolerance']:.1e}`. "
        f"The maximum non-`T_dyn` absolute difference is `{result['maximum_non_T_dyn_absolute_difference']:.17g}`.",
        "",
        f"For `T_dyn = Delta_C/tau`, the propagated absolute tolerance is "
        f"`{result['tolerance_policy']['T_dyn_propagated_absolute_tolerance']:.17g}`; "
        f"its raw absolute difference is `{next(item['absolute_difference'] for item in result['registered_comparisons'] if item['field'] == 'T_dyn'):.17g}`. "
        f"The maximum difference/tolerance fraction over positive-tolerance fields is "
        f"`{result['maximum_registered_tolerance_fraction']:.17g}`.",
        "",
        "The target label and hostile label are intentionally not identical strings: the target certifies dense reproduction, while the hostile lane certifies a resolved independent event-0 response. Their typed pass dispositions are compatible.",
        "",
        "## Scope",
        "",
        "The target result contains event 0 only. Hostile events 1--3 are retained as audit-only results and are not cross-reconciled. This establishes no L6/L8 persistence, scaling exponent, all-L result, curvature, geometry, or gravity.",
        "",
        "Per-sector carrier trace distances, actual/product traces, signed traces, and transport invariance agree. Target per-sector configuration-TV and occupation vectors had no pre-sealed hostile counterparts and are reported but excluded from the cross-lane gate.",
        "",
        "## Resources",
        "",
        f"Target: `{resources['target']['wall_seconds']:.9f}` s, `{resources['target']['peak_rss_bytes']}` peak RSS bytes, `{resources['target']['persisted_checkpoint_storage_bytes']}` persisted checkpoint bytes.",
        f"Hostile: `{resources['hostile']['wall_seconds']:.9f}` s, `{resources['hostile']['peak_rss_bytes']}` peak RSS bytes, `{resources['hostile']['persisted_checkpoint_bytes']}` persisted checkpoint bytes, with `{resources['hostile']['terminal_checkpoint_logical_bytes']}` logical terminal-checkpoint bytes held in memory.",
        "",
        "Storage figures are not like-for-like: the target retained restart custody, while the hostile run persisted only result custody. Energy was not metered.",
        "",
    ]
    return "\n".join(lines)


def parse_source_manifest() -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in SOURCE_MANIFEST.read_text().splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        entries[relative] = digest
    return entries


def preflight(require_outputs_absent: bool = True) -> dict[str, Any]:
    freeze = load_exact(FREEZE, audit_tools.sha256_file(FREEZE))
    if freeze.get("schema") != "L4_TARGET_HOSTILE_RECONCILIATION_FREEZE_V001":
        raise ReconciliationFailure("reconciliation freeze schema mismatch")
    expected = {
        "target_result_sha256": TARGET_SHA256,
        "hostile_result_sha256": HOSTILE_SHA256,
        "hostile_result_seal_sha256": HOSTILE_SEAL_SHA256,
        "tolerance": TOLERANCE,
    }
    for key, value in expected.items():
        if freeze.get(key) != value:
            raise ReconciliationFailure(f"reconciliation freeze mismatch: {key}")
    source_entries = {item["path"]: item["sha256"] for item in freeze["sources"]}
    if source_entries != parse_source_manifest():
        raise ReconciliationFailure("reconciliation source manifest differs from freeze")
    for relative, expected_hash in source_entries.items():
        if audit_tools.sha256_file(ROOT / relative) != expected_hash:
            raise ReconciliationFailure(f"reconciliation source changed: {relative}")
    load_exact(TARGET_RESULT, TARGET_SHA256)
    load_exact(HOSTILE_RESULT, HOSTILE_SHA256)
    seal = load_exact(HOSTILE_SEAL, HOSTILE_SEAL_SHA256)
    if (
        seal.get("status") != "SEALED_BEFORE_TARGET_UNBLINDING"
        or seal.get("target_output_read_before_seal") is not False
        or seal.get("result_sha256") != HOSTILE_SHA256
    ):
        raise ReconciliationFailure("hostile result seal does not prove pre-unblinding custody")
    if require_outputs_absent:
        existing = [path.name for path in (OUTPUT, OUTPUT_SIDECAR, REPORT, OUTPUT_MANIFEST) if path.exists()]
        if existing:
            raise ReconciliationFailure(f"refusing to overwrite reconciliation custody: {existing}")
    return freeze


def publish() -> dict[str, str]:
    preflight(require_outputs_absent=True)
    target = load_exact(TARGET_RESULT, TARGET_SHA256)
    hostile = load_exact(HOSTILE_RESULT, HOSTILE_SHA256)
    result = build_reconciliation(target, hostile)
    if not result["passed"]:
        raise ReconciliationFailure("target/hostile reconciliation did not pass")
    output_hash = audit_tools.atomic_create(OUTPUT, audit_tools.canonical_json_bytes(result))
    sidecar_hash = audit_tools.atomic_create(
        OUTPUT_SIDECAR,
        f"{output_hash}  {OUTPUT.relative_to(ROOT).as_posix()}\n".encode(),
    )
    report_hash = audit_tools.atomic_create(REPORT, report_markdown(result).encode())
    entries = (
        (audit_tools.sha256_file(FREEZE), FREEZE),
        (audit_tools.sha256_file(SOURCE_MANIFEST), SOURCE_MANIFEST),
        (output_hash, OUTPUT),
        (sidecar_hash, OUTPUT_SIDECAR),
        (report_hash, REPORT),
    )
    manifest_hash = audit_tools.atomic_create(
        OUTPUT_MANIFEST,
        "".join(
            f"{digest}  {path.relative_to(ROOT).as_posix()}\n" for digest, path in entries
        ).encode(),
    )
    return {
        "reconciliation_sha256": output_hash,
        "reconciliation_sidecar_sha256": sidecar_hash,
        "report_sha256": report_hash,
        "reconciliation_freeze_sha256": audit_tools.sha256_file(FREEZE),
        "reconciliation_source_manifest_sha256": audit_tools.sha256_file(
            SOURCE_MANIFEST
        ),
        "output_manifest_sha256": manifest_hash,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--preflight", action="store_true")
    action.add_argument("--publish", action="store_true")
    arguments = parser.parse_args()
    if arguments.preflight:
        preflight(require_outputs_absent=True)
        print(json.dumps({
            "status": "PASS_L4_RECONCILIATION_PREFLIGHT",
            "target_result_sha256": TARGET_SHA256,
            "hostile_result_sha256": HOSTILE_SHA256,
            "hostile_result_seal_sha256": HOSTILE_SEAL_SHA256,
        }, sort_keys=True))
    else:
        hashes = publish()
        print(json.dumps({"status": "PASS_PUBLISHED_L4_RECONCILIATION", **hashes}, sort_keys=True))


if __name__ == "__main__":
    main()
