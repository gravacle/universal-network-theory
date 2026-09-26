"""Non-load-bearing URM diagnostic for the frozen L8 lineage-order curvature test.

The diagnostic authenticates the controlled-null packet and exposes its exact
finite result without treating the schedule-derived path as emergent space.
The registered positive association was not resolved: rho is about 0.1543 and
the exact positive-tail permutation probability is about 0.3619.  That null is
scientific evidence about one prospectively frozen graph construction, not a
failure of the validator and not evidence for geometry or gravity.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping


SCHEMA = "WAC_L8_LINEAGE_ORDER_OLLIVIER_RICCI_DIAGNOSTIC_V001"
CLAIM_CLASS = (
    "CONTROLLED_NULL_L8_FORMATION_ORDER_OLLIVIER_RICCI__"
    "NO_RESOLVED_ASSOCIATION__NON_LOAD_BEARING"
)
_ROOT = Path(__file__).resolve().parent.parent
_PACKET = "DEVELOPMENT_R_L8_LINEAGE_ORDER_OLLIVIER_RICCI_V001"
_RESULT_PATH = f"{_PACKET}/RESULT.json"
_RESULT_SHA256 = "102e302e9e8f17c612b4461842237212d6b51814b7d27ba18d2112e57106d7a6"
_MANIFEST_PATH = f"{_PACKET}/MANIFEST.sha256"
_MANIFEST_SHA256 = "c0d99f8781f2c1be20ebafcb289116d63534caee0fcce22f8ca26e8538313a2b"

EXCLUDED_PROMOTIONS = (
    "POSITIVE_FORMATION_ORDER_CURVATURE_RECORD_ASSOCIATION",
    "OPPOSITE_SIGN_FORMATION_ORDER_CURVATURE_RECORD_ASSOCIATION",
    "RICHER_LINEAGE_GRAPH_NULL",
    "OTHER_SIZE_OR_REFINEMENT_RESULT",
    "EMERGENT_SPATIAL_METRIC",
    "SPACETIME_RICCI_CURVATURE",
    "RECORD_CONDITIONED_GEOMETRY",
    "RGRL_OR_WTC_RESPONSE",
    "GRAVITY_OR_EINSTEIN_DYNAMICS",
    "NEWTON_G",
)


class LineageOrderCurvatureRefusal(RuntimeError):
    """Fail-closed custody or schema refusal."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _root_path(relative: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:
        raise LineageOrderCurvatureRefusal("non-canonical curvature artifact path")
    path = _ROOT.joinpath(*pure.parts)
    if not path.is_file() or path.is_symlink():
        raise LineageOrderCurvatureRefusal(
            f"missing regular curvature artifact: {relative}"
        )
    return path


def _load_result() -> dict[str, Any]:
    result_path = _root_path(_RESULT_PATH)
    manifest_path = _root_path(_MANIFEST_PATH)
    if _sha256(result_path) != _RESULT_SHA256:
        raise LineageOrderCurvatureRefusal("curvature result hash mismatch")
    if _sha256(manifest_path) != _MANIFEST_SHA256:
        raise LineageOrderCurvatureRefusal("curvature manifest hash mismatch")
    try:
        result = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LineageOrderCurvatureRefusal("curvature result is not strict JSON") from error
    if result.get("schema") != "L8_LINEAGE_ORDER_OLLIVIER_RICCI_RESULT_V001":
        raise LineageOrderCurvatureRefusal("curvature result schema mismatch")
    if result.get("classification") != (
        "NO_RESOLVED_LINEAGE_ORDER_CURVATURE_RECORD_ASSOCIATION_L8"
    ):
        raise LineageOrderCurvatureRefusal("curvature disposition changed")
    if result.get("passed_positive_prediction") is not False:
        raise LineageOrderCurvatureRefusal("positive prediction was improperly promoted")
    statistic = result.get("statistic", {})
    if statistic.get("rho_observed") != 0.1543033499620919:
        raise LineageOrderCurvatureRefusal("registered rho changed")
    if statistic.get("p_plus") != 0.3619047619047619:
        raise LineageOrderCurvatureRefusal("registered positive-tail probability changed")
    if result.get("graph_ceiling") != (
        "FINITE_SCHEDULE_DERIVED_DIAGNOSTIC__NOT_SPACETIME_CURVATURE_OR_GRAVITY"
    ):
        raise LineageOrderCurvatureRefusal("graph ceiling changed")
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
                "result_path": _RESULT_PATH,
                "result_sha256": _RESULT_SHA256,
            },
            "classification": result["classification"],
            "passed_positive_prediction": result["passed_positive_prediction"],
            "graph_ceiling": result["graph_ceiling"],
            "edge_curvature": result["edge_curvature"],
            "node_curvature": result["node_curvature"],
            "record_concentration": result["record_concentration"],
            "statistic": result["statistic"],
            "controls": result["controls"],
            "claim_boundary": (
                "NO_RESOLVED_ASSOCIATION_ON_THE_FROZEN_L8_FORMATION_ORDER_PATH; "
                "DOES_NOT_RULE_OUT_PROSPECTIVELY_EARNED_RICHER_GRAPHS; "
                "NO_EMERGENT_SPACE_GEOMETRY_SPACETIME_CURVATURE_OR_GRAVITY"
            ),
            "excluded_promotions": list(EXCLUDED_PROMOTIONS),
            "urm_role": {
                "load_bearing": False,
                "controlled_null_is_validator_failure": False,
                "purpose": "SEPARATELY_REPORTED_FROZEN_FINITE_DIAGNOSTIC",
            },
        }
    )


@dataclass(frozen=True)
class LineageOrderCurvatureDiagnostic:
    """Immutable zero-input handle to the separately reported L8 null."""

    claim_class: str = CLAIM_CLASS

    def certificate(self) -> Mapping[str, Any]:
        return _certificate()


def lineage_order_curvature() -> LineageOrderCurvatureDiagnostic:
    """Return the non-load-bearing L8 formation-order curvature diagnostic."""

    return LineageOrderCurvatureDiagnostic()


def lineage_order_curvature_certificate() -> Mapping[str, Any]:
    """Return its hash-pinned immutable certificate."""

    return _certificate()
