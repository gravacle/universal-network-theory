"""Non-load-bearing URM diagnostic for the validated L4 autonomous continuation.

The certificate authenticates both the frozen target output and the independent
no-``@`` contraction-path audit.  It records one finite mechanism: after a
fixed lineage-reading revisit, two inputs with the same separate lineage and
carrier marginals produce distinguishable carrier states.  It does not turn
that L4 mechanism into a scaling, curvature, geometry, or gravity claim.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping


SCHEMA = "WAC_OWNER_ONCE_L4_AUTONOMOUS_CONTINUATION_DIAGNOSTIC_V001"
CLAIM_CLASS = (
    "INDEPENDENTLY_REPRODUCED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION__"
    "NON_LOAD_BEARING"
)
_ROOT = Path(__file__).resolve().parent.parent
_TARGET_PATH = (
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_"
    "CONTINUATION_V001/PHYSICAL_OUTPUTS/"
    "L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_RESULT_V001.json"
)
_TARGET_SHA256 = "ad134b528761c4e865df35678097dab4fb56297c5237a910ca482bac77c0c0dc"
_AUDIT_PACKET = "AUDIT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001"
_INDEPENDENT_PATH = f"{_AUDIT_PACKET}/INDEPENDENT_RESULT.json"
_INDEPENDENT_SHA256 = "86316a114201046f87789884c207ebe4d21356d0405475327e7bce455dd0352e"
_MANIFEST_PATH = f"{_AUDIT_PACKET}/MANIFEST.sha256"
_MANIFEST_SHA256 = "f0244e08f09a2b7073f489b6b89d43c917dc7c718cacb0e3891b719c60af2c10"

EXCLUDED_PROMOTIONS = (
    "OTHER_L_OR_SIZE_PERSISTENCE",
    "FINITE_SIZE_SCALING_OR_THERMODYNAMIC_LIMIT",
    "CURVATURE_OR_RECORD_GEOMETRY",
    "EMERGENT_SPACE_OR_CONTINUUM",
    "FINITE_ARGER_GATE_STATUS",
    "CONDITIONAL_LL_P_DYNAMICAL_Z1",
    "RGRL_OR_WTC_RESPONSE",
    "ALPHA_ALLOW_REQUIRE_OR_SELECT",
    "EINSTEIN_DYNAMICS_OR_GRAVITY",
    "NEWTON_G",
)


class AutonomousContinuationRefusal(RuntimeError):
    """Fail-closed custody or schema refusal."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _root_path(relative: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:
        raise AutonomousContinuationRefusal("non-canonical continuation artifact path")
    path = _ROOT.joinpath(*pure.parts)
    if not path.is_file() or path.is_symlink():
        raise AutonomousContinuationRefusal(
            f"missing regular continuation artifact: {relative}"
        )
    return path


def _strict_json(relative: str, digest: str) -> dict[str, Any]:
    path = _root_path(relative)
    if _sha256(path) != digest:
        raise AutonomousContinuationRefusal(
            f"continuation artifact hash mismatch: {relative}"
        )
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise AutonomousContinuationRefusal(
            f"continuation artifact is not strict JSON: {relative}"
        ) from error
    if not isinstance(value, dict):
        raise AutonomousContinuationRefusal("continuation artifact must be an object")
    return value


def _load_results() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = _root_path(_MANIFEST_PATH)
    if _sha256(manifest) != _MANIFEST_SHA256:
        raise AutonomousContinuationRefusal("independent audit manifest hash mismatch")
    target = _strict_json(_TARGET_PATH, _TARGET_SHA256)
    independent = _strict_json(_INDEPENDENT_PATH, _INDEPENDENT_SHA256)

    if target.get("schema") != "L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_RESULT_V001":
        raise AutonomousContinuationRefusal("target continuation schema mismatch")
    if independent.get("schema") != (
        "INDEPENDENT_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_VALIDATION_V001"
    ):
        raise AutonomousContinuationRefusal("independent continuation schema mismatch")
    expected = "RESOLVED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION"
    if target.get("classification") != expected or independent.get("classification") != expected:
        raise AutonomousContinuationRefusal("continuation classification changed")
    if independent.get("passed") is not True:
        raise AutonomousContinuationRefusal("independent continuation validation did not pass")
    if independent.get("disposition") != (
        "PASS_INDEPENDENT_L4_LINEAGE_SENSITIVE_CONTINUATION_VALIDATION"
    ):
        raise AutonomousContinuationRefusal("independent continuation disposition changed")
    independence = independent.get("independence", {})
    if independence.get("imports_target_implementation") is not False:
        raise AutonomousContinuationRefusal("independent route imported target implementation")
    if independence.get("imports_historical_parent") is not False:
        raise AutonomousContinuationRefusal("independent route imported historical parent")
    if independence.get("dense_contraction") != "NUMPY_EINSUM_OPTIMIZE_FALSE_ONLY":
        raise AutonomousContinuationRefusal("independent contraction route changed")
    controls = independent.get("controls", {})
    if controls.get("target_classification_matches") is not True:
        raise AutonomousContinuationRefusal("target/independent classifications differ")
    if controls.get("target_registered_observable_max_abs_difference") != (
        1.1102230246251565e-16
    ):
        raise AutonomousContinuationRefusal("target/independent agreement changed")
    if target.get("tau") != 1e-10 or independent.get("tau") != 1e-10:
        raise AutonomousContinuationRefusal("continuation numerical scale changed")
    if target["fine"]["after_transport"]["carrier_trace_distance"] != (
        0.14761185701902999
    ):
        raise AutonomousContinuationRefusal("target carrier response changed")
    if independent["fine"]["after_transport"]["carrier_trace_distance"] != (
        0.14761185701903007
    ):
        raise AutonomousContinuationRefusal("independent carrier response changed")
    if independent["warning_audit"]["captured_warnings"] != []:
        raise AutonomousContinuationRefusal("independent warning audit changed")
    if independent["warning_audit"]["accepted_on_faith"] is not False:
        raise AutonomousContinuationRefusal("warning stream was improperly accepted")
    return target, independent


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(child) for key, child in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(child) for child in value)
    return value


def _certificate() -> Mapping[str, Any]:
    target, independent = _load_results()
    target_fine = target["fine"]
    independent_fine = independent["fine"]
    return _freeze(
        {
            "schema": SCHEMA,
            "claim_class": CLAIM_CLASS,
            "custody": {
                "target_result_path": _TARGET_PATH,
                "target_result_sha256": _TARGET_SHA256,
                "independent_result_path": _INDEPENDENT_PATH,
                "independent_result_sha256": _INDEPENDENT_SHA256,
                "audit_manifest_path": _MANIFEST_PATH,
                "audit_manifest_sha256": _MANIFEST_SHA256,
            },
            "classification": independent["classification"],
            "disposition": independent["disposition"],
            "target": {
                "Delta_C": target_fine["after_transport"]["carrier_trace_distance"],
                "occupation_profile_rms": target_fine["after_transport"]["occupation_rms"],
                "T_dyn": target["T_dyn"],
            },
            "independent": {
                "Delta_C": independent_fine["after_transport"]["carrier_trace_distance"],
                "occupation_profile_rms": independent_fine["after_transport"]["occupation_rms"],
                "T_dyn": independent["T_dyn"],
                "captured_warnings": independent["warning_audit"]["captured_warnings"],
                "dense_contraction": independent["independence"]["dense_contraction"],
            },
            "tau": independent["tau"],
            "controls": {
                "initial_carrier_marginal_residual": independent_fine["controls"][
                    "carrier_marginal_equality"
                ],
                "trace_distance_transport_invariance": independent_fine["controls"][
                    "trace_distance_transport_invariance"
                ],
                "target_independent_registered_max_abs_difference": independent[
                    "controls"
                ]["target_registered_observable_max_abs_difference"],
                "coarse_fine_maximum": independent["controls"]["coarse_fine_maximum"],
                "maximum_residual": independent["controls"]["maximum_residual"],
                "warning_audit_accepted_on_faith": independent["warning_audit"][
                    "accepted_on_faith"
                ],
            },
            "interpretation": independent["interpretation"],
            "claim_boundary": (
                "ONE_FIXED_L4_LINEAGE_READING_MECHANISM_ONLY; "
                "TRACE_DISTANCE_TRANSPORT_INVARIANCE_IS_A_CONTROL; "
                "OCCUPATION_PROFILE_RESPONSE_IS_TRANSPORT_SENSITIVE; "
                "NO_SIZE_PERSISTENCE_SCALING_CURVATURE_GEOMETRY_RGRL_WTC_ALPHA_OR_GRAVITY"
            ),
            "excluded_promotions": list(EXCLUDED_PROMOTIONS),
            "urm_role": {
                "load_bearing": False,
                "purpose": "SEPARATELY_REPORTED_AUTHENTICATED_FINITE_MECHANISM",
                "input_to_finite_gate_or_gravity_closure": False,
            },
        }
    )


@dataclass(frozen=True)
class OwnerOnceAutonomousContinuationDiagnostic:
    """Immutable zero-input handle to the independently validated L4 mechanism."""

    claim_class: str = CLAIM_CLASS

    def certificate(self) -> Mapping[str, Any]:
        return _certificate()


def owner_once_autonomous_continuation() -> OwnerOnceAutonomousContinuationDiagnostic:
    """Return the non-load-bearing L4 autonomous-continuation handle."""

    return OwnerOnceAutonomousContinuationDiagnostic()


def owner_once_autonomous_continuation_certificate() -> Mapping[str, Any]:
    """Return its hash-pinned immutable certificate."""

    return _certificate()
