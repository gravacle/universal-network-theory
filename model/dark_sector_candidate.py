"""Zero-input custody surface for the shared dark-sector candidate, not a solver.

This additive URM surface registers work in progress.  Successful custody checks
do not qualify the physical dictionary, produce a cosmological prediction, or
promote any existing UNT theorem.  A later scientifically reviewed checkpoint
must be separately versioned; this snapshot cannot accept caller-supplied
parameters, results, thresholds, or claims of completion.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path, PurePosixPath
import re
from types import MappingProxyType
from typing import Any, Mapping


SCHEMA = "URM_SHARED_DARK_SECTOR_CANDIDATE_V001"
CLAIM_CLASS = "CANDIDATE__PHYSICAL_CLOSURE_AND_SHARED_PREDICTIONS_UNRESOLVED"
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DARK_ROOT = "UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001"
_CANDIDATE_PATH = (
    f"{_DARK_ROOT}/joint_parent_continuation/"
    "DARK_SECTOR_SHARED_MODEL_CANDIDATE_V001.md"
)
_LEDGER_PATH = f"{_DARK_ROOT}/STAGE_1_3_OUTSTANDING_TEST_LEDGER_V008.md"
_SOURCE_PATHS = (_CANDIDATE_PATH, _LEDGER_PATH)
# Exact local-development checkpoint pins, not released-capsule dependencies.
# Missing/malformed pins remain fail-closed, never an instruction to trust live content.
_ARTIFACT_SHA256: Mapping[str, str | None] = MappingProxyType({
    _CANDIDATE_PATH: "d47dc8f31fad8fbeb04f85e247c9b5798afcc739faa2d8a0b8933faf306ac9b3",
    _LEDGER_PATH: "631ef73a29fcebab1e20f4260f75a2e88cd13e8c316b0f8f65e53ec2df88519a",
})

MANDATORY_LANES = (
    ("native_source_clock_volume", "Native source, clock, volume and formation"),
    ("shared_spatial_gravity_state", "Shared spatial gravity and state"),
    ("galaxy_observations_comparison", "Galaxy observations and fair comparison"),
    ("expansion_acoustic_ruler", "Expansion and acoustic ruler"),
    ("observed_lensing", "Observed lensing"),
    ("growth_structure_stability", "Growth, structure and stability"),
    ("merger_morphology_transport", "Merger morphology and transport"),
    ("bbn_recombination", "BBN and recombination"),
    ("cmb_perturbations_observations", "CMB TT, TE, EE and lensing observations"),
    ("network_cmb_thermal_origin", "Separately proposed network CMB thermal origin"),
    ("independent_joint_synthesis", "Independently reviewed joint synthesis"),
)

SHARED_STATE_OBLIGATIONS = (
    "ONE_SPECIFIED_DYNAMICS_AND_PHYSICAL_SOURCE_CLOCK_VOLUME_MAP",
    "ONE_FORMATION_RULE_AND_EXPLICIT_ENVIRONMENTAL_INITIAL_BOUNDARY_DATA",
    "SAME_ENERGY_STATE_FOR_FORCE_VOLUME_WORK_AND_CREATION_WORK",
    "ONE_REGISTERED_UNIVERSAL_PARAMETER_AND_CALIBRATION_LEDGER",
    "NO_INDEPENDENT_HALO_PROFILE_OR_GALAXY_BY_GALAXY_HIDDEN_POPULATION",
    "NO_INDEPENDENT_VACUUM_OFFSET_OR_FITTED_EXPANSION_FUNCTION",
    "NO_RADIUS_BY_RADIUS_PREPARATION_SELECTED_FROM_ROTATION_DATA",
    "FROZEN_JOINT_GALAXY_AND_EXPANSION_PREDICTIONS",
    "INDEPENDENT_NUMERICAL_REVIEW_AND_UNUSED_OBSERVATIONAL_TEST",
)

EXCLUDED_PROMOTIONS = (
    "NATIVE_PHYSICAL_SOURCE_CLOCK_VOLUME_DERIVATION_COMPLETE",
    "REQUIRED_NETWORK_STATE_FORMS_AUTOMATICALLY",
    "SHARED_GALAXY_AND_EXPANSION_EXPLANATION_ESTABLISHED",
    "STAGE_3_COMPLETE",
    "DARK_MATTER_OR_DARK_ENERGY_DOES_NOT_EXIST",
    "INDEPENDENT_DARK_COMPONENTS_RENDERED_SUPERFLUOUS",
    "CMB_THERMAL_ORIGIN_FROM_NETWORK_ESTABLISHED",
    "SUPERIORITY_TO_LCDM_ESTABLISHED",
    "FINITE_ARGER_OR_UNT_CLOSURE_THEOREM_PREMISES_CHANGED",
    "PERMISSION_TO_PUBLISH_OR_RELEASE",
)


class DarkSectorCandidateRefusal(RuntimeError):
    """A missing, unsealed, noncanonical or altered candidate checkpoint."""


def _source_path(relative: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise DarkSectorCandidateRefusal("candidate source path must be a string")
    pure = PurePosixPath(relative)
    if (pure.is_absolute() or pure.as_posix() != relative
            or any(part in (".", "..") for part in pure.parts)):
        raise DarkSectorCandidateRefusal("noncanonical candidate source path")
    root = _PROJECT_ROOT.resolve()
    path = root
    for part in pure.parts:
        path = path / part
        if path.is_symlink():
            raise DarkSectorCandidateRefusal("symlink in candidate source path")
    if not path.is_file() or not path.resolve().is_relative_to(root):
        raise DarkSectorCandidateRefusal("missing regular candidate source")
    return path


def _custody() -> list[dict[str, str]]:
    if set(_ARTIFACT_SHA256) != set(_SOURCE_PATHS):
        raise DarkSectorCandidateRefusal("candidate custody set changed")
    result = []
    for relative in _SOURCE_PATHS:
        expected = _ARTIFACT_SHA256[relative]
        if not isinstance(expected, str) or re.fullmatch(r"[0-9a-f]{64}", expected) is None:
            raise DarkSectorCandidateRefusal("candidate checkpoint has not been sealed")
        try:
            raw = _source_path(relative).read_bytes()
        except OSError as error:
            raise DarkSectorCandidateRefusal("cannot read candidate checkpoint") from error
        actual = hashlib.sha256(raw).hexdigest()
        if actual != expected:
            raise DarkSectorCandidateRefusal("candidate checkpoint hash mismatch")
        result.append({"path": relative, "sha256": actual})
    return result


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(child) for key, child in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(child) for child in value)
    return value


def _certificate() -> Mapping[str, Any]:
    custody = _custody()
    return _freeze({
        "schema": SCHEMA,
        "claim_class": CLAIM_CLASS,
        "checkpoint_status": "CANDIDATE_NOT_PHYSICALLY_CLOSED",
        "custody": custody,
        "physical_closure": {
            "source_clock_volume_map": "UNRESOLVED",
            "network_state_formation": "UNRESOLVED",
            "shared_energy_force_volume_creation_work": "UNRESOLVED",
            "derived_adopted_calibrated_inventory_required": True,
            "universal_calibration_is_allowed_but_not_independent_prediction": True,
        },
        "same_state_cross_domain_gate": {
            "status": "UNQUALIFIED_PENDING_DERIVATION_AND_TEST",
            "prediction_ready": False,
            "passed": False,
            "obligations": SHARED_STATE_OBLIGATIONS,
            "same_state_meaning": (
                "ONE_MODEL_AND_FORMATION_RULE_WITH_EXPLICIT_ENVIRONMENTAL_DATA; "
                "NOT_IDENTICAL_MICROSTATES_IN_DIFFERENT_GALAXIES_AND_COSMOLOGY"
            ),
        },
        "mandatory_lanes": [
            {"id": lane_id, "label": label, "overall_status": "OPEN"}
            for lane_id, label in MANDATORY_LANES
        ],
        "required_lane_count": len(MANDATORY_LANES),
        "cmb_lanes_are_distinct": True,
        "stage_3_complete": False,
        "dark_components_superfluous": False,
        "empirical_superiority_established": False,
        "claim_boundary": (
            "CUSTODY_AND_SCOPED_CANDIDATE_STATUS_ONLY; NO_SOLVER_EXECUTION; "
            "NO_EMPIRICAL_VALIDATION_OR_THEOREM_PROMOTION"
        ),
        "excluded_promotions": EXCLUDED_PROMOTIONS,
        "urm_role": {
            "load_bearing_for_existing_closure": False,
            "input_to_finite_gate_or_gravity_closure": False,
            "purpose": "ADDITIVE_SHARED_DARK_SECTOR_RESEARCH_CANDIDATE",
            "scientific_solver_executed": False,
            "custody_pass_is_scientific_pass": False,
        },
    })


@dataclass(frozen=True, init=False)
class DarkSectorCandidate:
    """Immutable zero-input handle; every certificate call rechecks custody."""

    claim_class: str = CLAIM_CLASS

    def certificate(self) -> Mapping[str, Any]:
        return _certificate()


def dark_sector_candidate() -> DarkSectorCandidate:
    """Expose the scoped candidate after authenticating its fixed checkpoint."""
    _custody()
    return DarkSectorCandidate()


def dark_sector_candidate_certificate() -> Mapping[str, Any]:
    """Return an immutable candidate-status certificate, never a physics verdict."""
    return _certificate()
