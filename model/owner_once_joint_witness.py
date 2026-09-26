"""Non-load-bearing URM diagnostic for the completed owner-once L10/L12 run.

The diagnostic authenticates the separate recognition packet.  It reports a
valid independently reproduced finite association, the disclosed launch-skew
deviation, and the failed signed no-decline prediction without converting any
of those facts into Gate, RGRL/WTC, alpha, geometry, continuum, or gravity
evidence.  A scientifically negative persistence result is valid evidence and
therefore does not make the URM validator fail.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping


SCHEMA = "WAC_OWNER_ONCE_JOINT_WITNESS_DIAGNOSTIC_V001"
CLAIM_CLASS = (
    "AUTHENTICATED_FINITE_L10_L12_JOINT_LINEAGE_CARRIER_ASSOCIATION__"
    "SIGNED_PERSISTENCE_FAIL__NON_LOAD_BEARING"
)
_ROOT = Path(__file__).resolve().parent.parent
_PACKET = "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_HELDOUT_RECOGNITION_V001"
_RESULT_PATH = f"{_PACKET}/RECOGNITION_RESULT_V001.json"
_RESULT_SHA256 = "f0ad9ec906d9185cdbf3f2aa45e1e84cc652ccf77ed7793868b5ab27655b39a1"
_MANIFEST_PATH = f"{_PACKET}/MANIFEST.sha256"
_MANIFEST_SHA256 = "c22d2c13556d7c5ad5d806d7eee17a3b8fae5dfa4aefcac80494f18ae4c12dde"

EXCLUDED_PROMOTIONS = (
    "FORMAL_STRICT_HELDOUT_PROTOCOL_PASS",
    "POSITIVE_NO_DECLINE_PERSISTENCE",
    "ALL_L_OR_THERMODYNAMIC_PERSISTENCE",
    "FINITE_ARGER_GATE_STATUS",
    "DYNAMICAL_Z1",
    "RGRL_OR_WTC_RESPONSE",
    "ALPHA_ALLOW_REQUIRE_OR_SELECT",
    "RECORD_CURVATURE_OR_GEOMETRY",
    "CONTINUUM_OR_EINSTEIN_GRAVITY",
    "NEWTON_G",
)


class OwnerOnceJointWitnessRefusal(RuntimeError):
    """Fail-closed custody or schema refusal."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _root_path(relative: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:
        raise OwnerOnceJointWitnessRefusal("non-canonical diagnostic artifact path")
    path = _ROOT.joinpath(*pure.parts)
    if not path.is_file() or path.is_symlink():
        raise OwnerOnceJointWitnessRefusal(f"missing regular diagnostic artifact: {relative}")
    return path


def _load_result() -> dict[str, Any]:
    result_path = _root_path(_RESULT_PATH)
    manifest_path = _root_path(_MANIFEST_PATH)
    if _sha256(result_path) != _RESULT_SHA256:
        raise OwnerOnceJointWitnessRefusal("recognition result hash mismatch")
    if _sha256(manifest_path) != _MANIFEST_SHA256:
        raise OwnerOnceJointWitnessRefusal("recognition manifest hash mismatch")
    try:
        result = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise OwnerOnceJointWitnessRefusal("recognition result is not strict JSON") from error
    if result.get("schema") != "OWNER_ONCE_HELDOUT_L10_L12_RECOGNITION_V001":
        raise OwnerOnceJointWitnessRefusal("recognition result schema mismatch")
    evidence = result.get("computational_evidence", {})
    strict = result.get("strict_protocol", {})
    persistence = result.get("secondary_signed_persistence", {})
    if evidence.get("recognized") is not True:
        raise OwnerOnceJointWitnessRefusal("recognized computational evidence is absent")
    if strict.get("formal_pass_claimed") is not False:
        raise OwnerOnceJointWitnessRefusal("strict protocol was improperly promoted")
    if persistence.get("pass") is not False:
        raise OwnerOnceJointWitnessRefusal("signed persistence outcome changed")
    return result


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(child) for key, child in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(child) for child in value)
    return value


def _certificate() -> Mapping[str, Any]:
    result = _load_result()
    return _freeze(
        {
            "schema": SCHEMA,
            "claim_class": CLAIM_CLASS,
            "custody": {
                "manifest_path": _MANIFEST_PATH,
                "manifest_sha256": _MANIFEST_SHA256,
                "recognition_result_path": _RESULT_PATH,
                "recognition_result_sha256": _RESULT_SHA256,
            },
            "computational_evidence": result["computational_evidence"],
            "strict_protocol": result["strict_protocol"],
            "secondary_signed_persistence": result["secondary_signed_persistence"],
            "sizes": result["sizes"],
            "timing_custody": result["timing_custody"],
            "policy_adjudication": result["policy_adjudication"],
            "claim_boundary": result["claim_boundary"],
            "excluded_promotions": list(EXCLUDED_PROMOTIONS),
            "urm_role": {
                "load_bearing": False,
                "negative_scientific_result_is_validator_failure": False,
                "purpose": "SEPARATELY_REPORTED_AUTHENTICATED_DIAGNOSTIC",
            },
        }
    )


@dataclass(frozen=True)
class OwnerOnceJointWitnessDiagnostic:
    """Immutable zero-input handle to the separately reported diagnostic."""

    claim_class: str = CLAIM_CLASS

    def certificate(self) -> Mapping[str, Any]:
        return _certificate()


def owner_once_joint_witness() -> OwnerOnceJointWitnessDiagnostic:
    """Return the non-load-bearing owner-once diagnostic handle."""

    return OwnerOnceJointWitnessDiagnostic()


def owner_once_joint_witness_certificate() -> Mapping[str, Any]:
    """Return its hash-pinned immutable certificate."""

    return _certificate()
