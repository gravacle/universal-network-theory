#!/usr/bin/env python3
"""Validate the non-load-bearing L4 autonomous-continuation diagnostic."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import hashlib
import inspect
from types import MappingProxyType

import owner_once_autonomous_continuation as continuation
from project_model import URM


passed = 0


def check(condition_or_name, condition=None) -> None:
    global passed
    verdict = condition_or_name if condition is None else condition
    if not verdict:
        raise AssertionError("owner-once autonomous-continuation validation failed")
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
    check(tuple(inspect.signature(continuation.owner_once_autonomous_continuation).parameters) == ())
    check(
        tuple(
            inspect.signature(
                continuation.owner_once_autonomous_continuation_certificate
            ).parameters
        )
        == ()
    )
    check(type_error(lambda: continuation.owner_once_autonomous_continuation({})))
    check(
        type_error(
            lambda: continuation.owner_once_autonomous_continuation_certificate(data={})
        )
    )
    check(
        type_error(
            lambda: mutate(
                continuation.owner_once_autonomous_continuation_certificate(),
                "schema",
                "changed",
            )
        )
    )

    handle = continuation.owner_once_autonomous_continuation()
    certificate = handle.certificate()
    second = continuation.owner_once_autonomous_continuation_certificate()
    check(handle.claim_class == continuation.CLAIM_CLASS)
    check(frozen_error(lambda: set_claim_class(handle)))
    check(certificate == second and certificate is not second)
    check(isinstance(certificate, MappingProxyType))
    check(isinstance(certificate["target"], MappingProxyType))
    check(isinstance(certificate["excluded_promotions"], tuple))
    check(certificate["schema"] == continuation.SCHEMA)
    check(certificate["claim_class"] == continuation.CLAIM_CLASS)

    custody = certificate["custody"]
    for path_key, digest_key in (
        ("target_result_path", "target_result_sha256"),
        ("independent_result_path", "independent_result_sha256"),
        ("audit_manifest_path", "audit_manifest_sha256"),
    ):
        path = continuation._root_path(custody[path_key])
        check(hashlib.sha256(path.read_bytes()).hexdigest() == custody[digest_key])

    check(
        "autonomous L4 continuation focused validator",
        certificate["classification"]
        == "RESOLVED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION",
    )
    check(
        certificate["disposition"]
        == "PASS_INDEPENDENT_L4_LINEAGE_SENSITIVE_CONTINUATION_VALIDATION"
    )
    check(certificate["tau"] == 1e-10)
    check(certificate["target"]["Delta_C"] == 0.14761185701902999)
    check(certificate["independent"]["Delta_C"] == 0.14761185701903007)
    check(certificate["independent"]["T_dyn"] == 1476118570.1903007)
    check(
        certificate["independent"]["occupation_profile_rms"]
        == 0.006009875541368592
    )
    check(certificate["independent"]["captured_warnings"] == ())
    check(
        certificate["independent"]["dense_contraction"]
        == "NUMPY_EINSUM_OPTIMIZE_FALSE_ONLY"
    )

    controls = certificate["controls"]
    check(controls["initial_carrier_marginal_residual"] == 6.938893903907228e-18)
    check(controls["trace_distance_transport_invariance"] == 1.1102230246251565e-16)
    check(
        controls["target_independent_registered_max_abs_difference"]
        == 1.1102230246251565e-16
    )
    check(controls["coarse_fine_maximum"] == 1.2490009027033011e-15)
    check(controls["maximum_residual"] == 4.6629367034256575e-15)
    check(controls["warning_audit_accepted_on_faith"] is False)

    interpretation = certificate["interpretation"]
    check(interpretation["scope"] == "MECHANISM_AT_L4_ONLY")
    check("TRANSPORT_INVARIANT" in interpretation["trace_distance"])
    check("TRANSPORT_SENSITIVE" in interpretation["occupation_profile"])

    role = certificate["urm_role"]
    check(role["load_bearing"] is False)
    check(role["input_to_finite_gate_or_gravity_closure"] is False)
    check(role["purpose"] == "SEPARATELY_REPORTED_AUTHENTICATED_FINITE_MECHANISM")
    check(tuple(certificate["excluded_promotions"]) == continuation.EXCLUDED_PROMOTIONS)
    for marker in (
        "ONE_FIXED_L4",
        "INVARIANCE_IS_A_CONTROL",
        "TRANSPORT_SENSITIVE",
        "NO_SIZE_PERSISTENCE",
        "CURVATURE",
        "GEOMETRY",
        "RGRL_WTC",
        "ALPHA",
        "GRAVITY",
    ):
        check(marker in certificate["claim_boundary"])

    check(
        URM.owner_once_autonomous_continuation().claim_class
        == continuation.CLAIM_CLASS
    )
    check(URM.owner_once_autonomous_continuation_certificate() == certificate)
    print(f"PASS: {passed} owner-once autonomous-continuation diagnostic checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
