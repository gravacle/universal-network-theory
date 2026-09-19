#!/usr/bin/env python3
"""Persist exact rough/sharp predicates before allowing publication."""

from __future__ import annotations

import math
from typing import Any

from evidence import EvidenceJournal


class UnresolvedComparison(RuntimeError):
    """The frozen comparison predicate refused publication."""


def _predicate(
    name: str,
    value: Any,
    operator: str,
    threshold: Any,
    passed: bool,
) -> dict[str, Any]:
    return {
        "name": name,
        "value": value,
        "operator": operator,
        "threshold": threshold,
        "passed": bool(passed),
    }


def target_diagnostic(
    length: int,
    rough: dict[str, Any],
    sharp: dict[str, Any],
    comparison: dict[str, Any],
) -> dict[str, Any]:
    """Re-evaluate every predicate used by the frozen target summarize()."""
    rows = sharp["rows"]
    epsilon = float(comparison["epsilon"])
    methods = [row[key] for row in rows for key in ("actual_solver", "null_solver")]
    max_accounting = max(
        abs(float(row[key]))
        for row in rows
        for key in (
            "admission_total_content_residual",
            "admission_bandwidth_residual",
            "target_owner_residual",
        )
    )
    minimum_write = min(float(row["W_n"]) for row in rows)
    maximum_reverse = max(float(row["reverse_support_probability"]) for row in rows)
    maximum_node = max(float(row["transport_node_residual_l1"]) for row in rows)
    maximum_norm = max(float(row["actual_norm_error"]) for row in rows)
    maximum_number = max(float(row["transport_number_drift"]) for row in rows)
    maximum_blocked = max(float(row["blocked_probability"]) for row in rows)
    predicates = [
        _predicate(
            "all_actual_and_null_solvers_converged",
            all(bool(method["converged"]) for method in methods),
            "is",
            True,
            all(bool(method["converged"]) for method in methods),
        ),
        _predicate(
            "maximum_admission_accounting_residual",
            max_accounting,
            "<=",
            1.0e-10,
            max_accounting <= 1.0e-10,
        ),
        _predicate(
            "minimum_W_n",
            minimum_write,
            ">=",
            -epsilon,
            minimum_write >= -epsilon,
        ),
        _predicate(
            "maximum_reverse_support_probability",
            maximum_reverse,
            "<=",
            1.0e-11,
            maximum_reverse <= 1.0e-11,
        ),
        _predicate(
            "maximum_transport_node_residual_l1",
            maximum_node,
            "<=",
            max(1.0e-9, 100.0 * epsilon),
            maximum_node <= max(1.0e-9, 100.0 * epsilon),
        ),
        _predicate(
            "maximum_actual_norm_error",
            maximum_norm,
            "<=",
            1.0e-10,
            maximum_norm <= 1.0e-10,
        ),
        _predicate(
            "maximum_transport_number_drift",
            maximum_number,
            "<=",
            1.0e-10,
            maximum_number <= 1.0e-10,
        ),
        _predicate(
            "maximum_blocked_probability",
            maximum_blocked,
            ">",
            1.0e-6,
            maximum_blocked > 1.0e-6,
        ),
    ]
    computed = all(row["passed"] for row in predicates)
    return {
        "schema": "TARGET_ROUGH_SHARP_PRE_GATE_DIAGNOSTIC_V002",
        "L": length,
        "rough_row_count": len(rough["rows"]),
        "sharp_row_count": len(rows),
        "raw_metrics": {
            "reverse_support_probability": maximum_reverse,
            "transport_node_residual_l1": maximum_node,
            "actual_norm_error": maximum_norm,
            "transport_number_drift": maximum_number,
            "admission_accounting_residual": max_accounting,
            "minimum_W_n": minimum_write,
            "blocked_probability": maximum_blocked,
        },
        "predicates": predicates,
        "computed_resolved": computed,
        "reported_resolved": comparison.get("resolved"),
        "reported_classification": comparison.get("classification"),
        "resolved_agrees_with_predicates": comparison.get("resolved") is computed,
        "comparison": comparison,
    }


def hostile_diagnostic(
    length: int,
    rough: dict[str, Any],
    sharp: dict[str, Any],
    comparison: dict[str, Any],
) -> dict[str, Any]:
    """Re-evaluate every predicate used by the frozen hostile compare()."""
    rows = sharp["rows"]
    epsilon = float(comparison["epsilon"])
    methods = [row[key] for row in rows for key in ("actual_solver", "null_solver")]
    maximum_admission = max(
        abs(float(row[key]))
        for row in rows
        for key in (
            "admission_total_content_residual",
            "admission_bandwidth_residual",
            "target_owner_residual",
        )
    )
    maximum_node = max(
        max(
            abs(float(row["transport_node_residual_l1"])),
            abs(float(row["null_transport_node_residual_l1"])),
        )
        for row in rows
    )
    maximum_number = max(
        max(
            abs(float(row["transport_number_drift"])),
            abs(float(row["null_transport_number_drift"])),
        )
        for row in rows
    )
    maximum_norm = max(
        max(abs(float(row["actual_norm_error"])), abs(float(row["null_norm_error"])))
        for row in rows
    )
    maximum_reverse = max(
        abs(float(row["reverse_support_probability"])) for row in rows
    )
    maximum_blocked_null = max(
        abs(float(row["blocked_null_state_error"])) for row in rows
    )
    minimum_write = min(float(row["W_n"]) for row in rows)
    maximum_blocked = max(float(row["blocked_probability"]) for row in rows)
    predicates = [
        _predicate("row_count", len(rows), "==", length, len(rows) == length),
        _predicate(
            "event_sequence",
            [row["event"] for row in rows],
            "==",
            list(range(1, length + 1)),
            [row["event"] for row in rows] == list(range(1, length + 1)),
        ),
        _predicate(
            "terminal_row_streamed",
            rows[-1]["terminal_children_streamed"],
            "is",
            True,
            rows[-1]["terminal_children_streamed"] is True,
        ),
        _predicate(
            "nonterminal_rows_not_streamed",
            all(not row["terminal_children_streamed"] for row in rows[:-1]),
            "is",
            True,
            all(not row["terminal_children_streamed"] for row in rows[:-1]),
        ),
        _predicate(
            "all_actual_and_null_solvers_converged",
            all(bool(method["converged"]) for method in methods),
            "is",
            True,
            all(bool(method["converged"]) for method in methods),
        ),
        _predicate(
            "maximum_admission_accounting_residual",
            maximum_admission,
            "<=",
            1.0e-10,
            maximum_admission <= 1.0e-10,
        ),
        _predicate(
            "maximum_node_continuity_residual_l1",
            maximum_node,
            "<=",
            max(1.0e-9, 100.0 * epsilon),
            maximum_node <= max(1.0e-9, 100.0 * epsilon),
        ),
        _predicate(
            "maximum_number_drift",
            maximum_number,
            "<=",
            1.0e-10,
            maximum_number <= 1.0e-10,
        ),
        _predicate(
            "maximum_norm_error",
            maximum_norm,
            "<=",
            1.0e-10,
            maximum_norm <= 1.0e-10,
        ),
        _predicate(
            "maximum_reverse_support_probability",
            maximum_reverse,
            "<=",
            1.0e-11,
            maximum_reverse <= 1.0e-11,
        ),
        _predicate(
            "maximum_blocked_null_state_error",
            maximum_blocked_null,
            "<=",
            1.0e-11,
            maximum_blocked_null <= 1.0e-11,
        ),
        _predicate(
            "minimum_W_n",
            minimum_write,
            ">=",
            -epsilon,
            minimum_write >= -epsilon,
        ),
        _predicate(
            "maximum_blocked_probability",
            maximum_blocked,
            ">",
            1.0e-6,
            maximum_blocked > 1.0e-6,
        ),
    ]
    computed = all(row["passed"] for row in predicates)
    return {
        "schema": "HOSTILE_ROUGH_SHARP_PRE_GATE_DIAGNOSTIC_V002",
        "L": length,
        "rough_row_count": len(rough["rows"]),
        "sharp_row_count": len(rows),
        "raw_metrics": {
            "reverse_support_probability": maximum_reverse,
            "transport_node_residual_l1": maximum_node,
            "actual_norm_error": maximum_norm,
            "transport_number_drift": maximum_number,
            "admission_accounting_residual": maximum_admission,
            "blocked_null_state_error": maximum_blocked_null,
            "minimum_W_n": minimum_write,
            "blocked_probability": maximum_blocked,
        },
        "predicates": predicates,
        "computed_resolved": computed,
        "reported_resolved": comparison.get("resolved"),
        "reported_classification": comparison.get("classification"),
        "resolved_agrees_with_predicates": comparison.get("resolved") is computed,
        "comparison": comparison,
    }


def persist_target_before_gate(
    evidence: EvidenceJournal,
    length: int,
    rough: dict[str, Any],
    sharp: dict[str, Any],
    comparison: dict[str, Any],
) -> dict[str, Any]:
    diagnostic = target_diagnostic(length, rough, sharp, comparison)
    evidence.comparison(diagnostic)
    return diagnostic


def persist_hostile_before_gate(
    evidence: EvidenceJournal,
    length: int,
    rough: dict[str, Any],
    sharp: dict[str, Any],
    comparison: dict[str, Any],
) -> dict[str, Any]:
    diagnostic = hostile_diagnostic(length, rough, sharp, comparison)
    evidence.comparison(diagnostic)
    return diagnostic


def require_resolved(diagnostic: dict[str, Any]) -> None:
    """Run only after the immutable comparison checkpoint exists."""
    if (
        diagnostic.get("computed_resolved") is not True
        or diagnostic.get("reported_resolved") is not True
        or diagnostic.get("resolved_agrees_with_predicates") is not True
    ):
        failures = [
            row["name"]
            for row in diagnostic.get("predicates", [])
            if row.get("passed") is not True
        ]
        raise UnresolvedComparison(
            "UNRESOLVED_RELATIONAL_HISTORY:" + ",".join(failures or ["reported_flag"])
        )

