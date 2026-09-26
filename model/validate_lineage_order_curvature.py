#!/usr/bin/env python3
"""Validate the non-load-bearing L8 lineage-order curvature diagnostic."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import hashlib
import inspect
from types import MappingProxyType

import lineage_order_curvature as curvature
from project_model import URM


passed = 0


def check(condition_or_name, condition=None) -> None:
    global passed
    verdict = condition_or_name if condition is None else condition
    if not verdict:
        raise AssertionError("lineage-order curvature diagnostic validation failed")
    passed += 1


def type_error(callable_object) -> bool:
    try:
        callable_object()
    except TypeError:
        return True
    return False


def frozen_error(callable_object) -> bool:
    try:
        callable_object()
    except FrozenInstanceError:
        return True
    return False


def mutate(mapping, key, value) -> None:
    mapping[key] = value


def set_claim_class(handle) -> None:
    handle.claim_class = "changed"


def main() -> int:
    check(tuple(inspect.signature(curvature.lineage_order_curvature).parameters) == ())
    check(
        tuple(
            inspect.signature(curvature.lineage_order_curvature_certificate).parameters
        )
        == ()
    )
    check(type_error(lambda: curvature.lineage_order_curvature({})))
    check(type_error(lambda: curvature.lineage_order_curvature_certificate(data={})))
    check(
        type_error(
            lambda: mutate(
                curvature.lineage_order_curvature_certificate(), "schema", "changed"
            )
        )
    )

    handle = curvature.lineage_order_curvature()
    certificate = handle.certificate()
    second = curvature.lineage_order_curvature_certificate()
    check(handle.claim_class == curvature.CLAIM_CLASS)
    check(frozen_error(lambda: set_claim_class(handle)))
    check(certificate == second and certificate is not second)
    check(isinstance(certificate, MappingProxyType))
    check(isinstance(certificate["statistic"], MappingProxyType))
    check(isinstance(certificate["edge_curvature"], tuple))
    check(certificate["schema"] == curvature.SCHEMA)
    check(certificate["claim_class"] == curvature.CLAIM_CLASS)

    custody = certificate["custody"]
    result_path = curvature._root_path(custody["result_path"])
    manifest_path = curvature._root_path(custody["manifest_path"])
    check(hashlib.sha256(result_path.read_bytes()).hexdigest() == custody["result_sha256"])
    check(
        hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        == custody["manifest_sha256"]
    )

    check(
        "lineage-order curvature controlled-null focused validator",
        certificate["classification"]
        == "NO_RESOLVED_LINEAGE_ORDER_CURVATURE_RECORD_ASSOCIATION_L8",
    )
    check(certificate["passed_positive_prediction"] is False)
    check(
        certificate["graph_ceiling"]
        == "FINITE_SCHEDULE_DERIVED_DIAGNOSTIC__NOT_SPACETIME_CURVATURE_OR_GRAVITY"
    )

    statistic = certificate["statistic"]
    check(statistic["rho_observed"] == 0.1543033499620919)
    check(statistic["p_plus"] == 0.3619047619047619)
    check(statistic["plus_count"] == 14592)
    check(statistic["p_minus"] == 0.6571428571428571)
    check(statistic["minus_count"] == 26496)
    check(statistic["permutations"] == 40320)

    check(tuple(certificate["edge_curvature"]) == (0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5))
    check(
        tuple(certificate["node_curvature"])
        == (0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.25, 0.5)
    )
    check(len(certificate["record_concentration"]) == 8)
    check(certificate["record_concentration"][0] == 0.5000000000000001)
    check(certificate["record_concentration"][-1] == 0.41409397429266154)

    controls = certificate["controls"]
    check(abs(controls["lineage_probability_sum"] - 1.0) < 1e-12)
    check(controls["wall_seconds"] < 300.0)
    check(controls["peak_rss_bytes"] < 536870912)
    check(len(controls["shard_hashes"]) == 8)
    check(len(controls["input_hashes"]) == 7)
    check(len(controls["source_hashes"]) == 3)

    role = certificate["urm_role"]
    check(role["load_bearing"] is False)
    check(role["controlled_null_is_validator_failure"] is False)
    check(role["purpose"] == "SEPARATELY_REPORTED_FROZEN_FINITE_DIAGNOSTIC")
    check(tuple(certificate["excluded_promotions"]) == curvature.EXCLUDED_PROMOTIONS)
    for marker in (
        "NO_RESOLVED_ASSOCIATION",
        "RICHER_GRAPHS",
        "NO_EMERGENT_SPACE",
        "GEOMETRY",
        "GRAVITY",
    ):
        check(marker in certificate["claim_boundary"])

    check(URM.lineage_order_curvature().claim_class == curvature.CLAIM_CLASS)
    check(URM.lineage_order_curvature_certificate() == certificate)
    print(f"PASS: {passed} lineage-order curvature diagnostic checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
