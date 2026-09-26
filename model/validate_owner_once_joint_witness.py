#!/usr/bin/env python3
"""Validate the non-load-bearing owner-once L10/L12 URM diagnostic."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import hashlib
import inspect
from types import MappingProxyType

import owner_once_joint_witness as witness
from project_model import URM


passed = 0


def check(condition_or_name, condition=None) -> None:
    global passed
    verdict = condition_or_name if condition is None else condition
    if not verdict:
        raise AssertionError("owner-once joint-witness diagnostic validation failed")
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
    check(tuple(inspect.signature(witness.owner_once_joint_witness).parameters) == ())
    check(tuple(inspect.signature(witness.owner_once_joint_witness_certificate).parameters) == ())
    check(type_error(lambda: witness.owner_once_joint_witness({})))
    check(type_error(lambda: witness.owner_once_joint_witness_certificate(data={})))
    check(type_error(lambda: mutate(witness.owner_once_joint_witness_certificate(), "schema", "changed")))

    handle = witness.owner_once_joint_witness()
    certificate = handle.certificate()
    second = witness.owner_once_joint_witness_certificate()
    check(handle.claim_class == witness.CLAIM_CLASS)
    check(frozen_error(lambda: set_claim_class(handle)))
    check(certificate == second and certificate is not second)
    check(isinstance(certificate, MappingProxyType))
    check(isinstance(certificate["computational_evidence"], MappingProxyType))
    check(isinstance(certificate["sizes"], tuple))
    check(certificate["schema"] == witness.SCHEMA)
    check(certificate["claim_class"] == witness.CLAIM_CLASS)

    custody = certificate["custody"]
    result_path = witness._root_path(custody["recognition_result_path"])
    manifest_path = witness._root_path(custody["manifest_path"])
    check(hashlib.sha256(result_path.read_bytes()).hexdigest() == custody["recognition_result_sha256"])
    check(hashlib.sha256(manifest_path.read_bytes()).hexdigest() == custody["manifest_sha256"])

    evidence = certificate["computational_evidence"]
    check(evidence["recognized"] is True)
    check(
        "owner-once joint witness focused validator (50/50)",
        evidence["status"]
        == "VALID_INDEPENDENTLY_REPRODUCED_FINITE_L10_L12_ASSOCIATION",
    )
    check(evidence["two_sided_T_10_12"] == 32365.88485223031)
    check(evidence["deterministic_numerical_validity_affected_by_timing_gap"] is False)
    check(evidence["independent_source_isolation_preserved"] is True)

    strict = certificate["strict_protocol"]
    check(strict["formal_pass_claimed"] is False)
    check(strict["release_skew_deviation_disclosed"] is True)
    check("NOT_CLAIMED_AS_FORMALLY_PASSED" in strict["status"])

    persistence = certificate["secondary_signed_persistence"]
    check(persistence["pass"] is False)
    check(persistence["D8_floor"] == 0.001963064475535806)
    check("SIGN_REVERSAL_AND_MAGNITUDE_DECLINE" in persistence["status"])

    sizes = certificate["sizes"]
    check(tuple(row["length"] for row in sizes) == (10, 12))
    check(tuple(row["D_L_target"] for row in sizes) == (-0.0003118488593728413, -3.236588485223031e-05))
    check(tuple(row["D_L_hostile"] for row in sizes) == (-0.00031184885937283205, -3.2365884852249583e-05))
    check(all(row["tau_L"] == 1e-9 for row in sizes))
    check(all(row["T_L"] > 1.0 for row in sizes))
    check(all(all(row["conditions"].values()) for row in sizes))
    check(all(row["persistence_pass"] is False for row in sizes))
    check(all(row["sign_relative_to_positive_D8"] == "REVERSED_NEGATIVE" for row in sizes))

    timing = certificate["timing_custody"]
    check(timing["release_observation"]["observed_gap_seconds"] == 10748)
    check(timing["release_observation"]["frozen_maximum_seconds"] == 60)
    check(timing["release_observation"]["within_frozen_maximum"] is False)
    check(timing["interpretation"]["target_was_already_deterministic_and_running_before_hostile_launch"] is True)

    role = certificate["urm_role"]
    check(role["load_bearing"] is False)
    check(role["negative_scientific_result_is_validator_failure"] is False)
    check(role["purpose"] == "SEPARATELY_REPORTED_AUTHENTICATED_DIAGNOSTIC")
    check(tuple(certificate["excluded_promotions"]) == witness.EXCLUDED_PROMOTIONS)
    for marker in ("NO_FORMAL_STRICT_PROTOCOL_PASS_CLAIM", "NO_ALL_L", "GATE", "RGRL", "ALPHA", "GRAVITY"):
        check(marker in certificate["claim_boundary"])

    check(URM.owner_once_joint_witness().claim_class == witness.CLAIM_CLASS)
    check(URM.owner_once_joint_witness_certificate() == certificate)
    print(f"PASS: {passed} owner-once joint-witness diagnostic checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
