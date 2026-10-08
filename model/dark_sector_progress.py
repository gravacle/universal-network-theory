"""V077/V018 local-development evidence snapshot, never a dark-sector solver.

This zero-input surface adds freshness without retargeting the older candidate
or any theorem. It authenticates direct artifacts and two canonical receipts;
recorded numerical checks are not replayed. The paired research tree is an
intentional local-development dependency, not a portable release capsule.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from types import MappingProxyType
from typing import Any, Mapping


SCHEMA = "URM_DARK_SECTOR_PROGRESS_V001"
CLAIM_CLASS = "CANDIDATE__RECORDED_FINITE_PROGRESS_WITH_ALL_PHYSICAL_GATES_OPEN"
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_D = "UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001"
_J = f"{_D}/joint_parent_continuation"
_K = f"{_J}/class_candidate_v001"
_U = "program-worktree"
_CU = f"{_U}/LANE_CROSS_RFT_GRA_GL6CU_COMPLETE_SIX_PAIR_H6_SOURCE_JET_V002"
_CU_AUDIT = f"{_U}/AUDIT_G_GL6CU_COMPLETE_SIX_PAIR_H6_SOURCE_JET_V002"
_SPATIAL = f"{_J}/SPHERICAL_CONSISTENT_SAVED_AUDIT_V001_RESULTS.json"
_HELIUM = f"{_K}/CLASS_THERMAL_HELIUM_CACHE_ATTRIBUTION_V001_RESULTS.json"
_SOURCE_PATHS = (
    f"{_D}/FRONTIER_UPDATE_V077.md",
    f"{_D}/STAGE_1_3_OUTSTANDING_TEST_LEDGER_V018.md",
    _SPATIAL,
    f"{_J}/SPHERICAL_CONSISTENT_SAVED_AUDIT_RESULT_REVIEW_INDEPENDENT_V001.md",
    _HELIUM,
    f"{_K}/CLASS_THERMAL_HELIUM_CACHE_ATTRIBUTION_RESULT_INDEPENDENT_V001.md",
    f"{_CU}/THEOREM.md",
    f"{_CU}/RESULT.md",
    f"{_CU}/MANIFEST.sha256",
    f"{_CU_AUDIT}/AUDIT_REPORT.md",
    f"{_CU_AUDIT}/TARGET.sha256",
)
_ARTIFACT_SHA256 = MappingProxyType(dict(zip(_SOURCE_PATHS, (
    "6602f4d878db5ef76b11b0dc743100ed6c104ee8bb6e9fc54c52180272c388b9",
    "b04825d09275a136f934eb65a2b359a83c305f176b6ca0335d0b6527d0117727",
    "c1e732f755ae485dfa1183d837ba183637f487005827c47f798727d77214438f",
    "622658b49533f2a1c5c2a05b97fdf1601080d86a1dde2a69975bfc42ecb2a0c3",
    "77788ba66e35ce27aaf0570e638230c880af5c06845cb46231144f4d44f342fe",
    "05dd5f75b9cef055929def34ba73e10f1accd6d0296b4dc9764d0feb6e41ef76",
    "fddcf486f9037c756c00cc90b6226014c27dda2f04ea5546355059b346140542",
    "79eb391a4e834f957d0ccff174ccb634e1f897cdda05519b468a977c2aace263",
    "58f313b1053756473fa8bfd1ff23b25e2f1740b1903bb366771e26cd3b3c89ec",
    "dc4a837c58d209be6117dc23a8300fd753784c23f01d15eac78a6b62ca3e2e01",
    "1e2a37949b8d68de18a9302086d90f96f967ae03ca1e58d065f6676bdff09ccc",
), strict=True)))
_PAYLOAD_SHA256 = MappingProxyType({
    _SPATIAL: "9b1f3f3d252cbd806eca2e7a505651f9f63bab28c5e42f5d6d56d0fdf67a5ce5",
    _HELIUM: "39f00acffde6da7cd2b752d12783878eada96fc4e0fd79f614a34de3a7453a2b",
})

# Independent fixed census, not an alias that could silently track a later API.
MANDATORY_LANES = (
    "native_source_clock_volume", "shared_spatial_gravity_state",
    "galaxy_observations_comparison", "expansion_acoustic_ruler",
    "observed_lensing", "growth_structure_stability",
    "merger_morphology_transport", "bbn_recombination",
    "cmb_perturbations_observations", "network_cmb_thermal_origin",
    "independent_joint_synthesis",
)
PROMOTION_FLAGS = (
    "physical_source_clock_volume_derived", "native_state_formation_derived",
    "shared_energy_force_volume_creation_work_closed",
    "same_state_galaxy_expansion_predictions_ready", "trajectory_qualified",
    "continuum_qualified", "physical_metric_ward_closed",
    "observations_qualified", "cmb_thermal_derivatives_qualified",
    "cmb_perturbations_qualified", "network_cmb_thermal_origin_established",
    "empirical_superiority_established", "dark_components_superfluous",
    "dark_matter_or_dark_energy_nonexistence_established", "stage_3_complete",
    "existing_theorem_promoted", "publication_authorized",
)


class DarkSectorProgressRefusal(RuntimeError):
    """Missing, mutated, redirected, malformed or promoting evidence."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise DarkSectorProgressRefusal(message)


def _source_path(relative: str) -> Path:
    _require(isinstance(relative, str) and bool(relative), "invalid source path")
    pure = PurePosixPath(relative)
    _require(not pure.is_absolute() and pure.as_posix() == relative
             and not any(part in (".", "..") for part in pure.parts),
             "noncanonical source path")
    _require(relative in _SOURCE_PATHS, "unregistered source path")
    root = _PROJECT_ROOT.resolve()
    path = root
    for part in pure.parts:
        path = path / part
        _require(not path.is_symlink(), "symlink in source path")
    _require(path.is_file() and path.resolve().is_relative_to(root),
             "missing regular evidence file")
    return path


def _custody() -> tuple[list[dict[str, str]], dict[str, bytes]]:
    _require(len(_SOURCE_PATHS) == len(set(_SOURCE_PATHS)) == 11,
             "changed artifact census")
    _require(set(_ARTIFACT_SHA256) == set(_SOURCE_PATHS), "changed custody set")
    custody, raw = [], {}
    for relative in _SOURCE_PATHS:
        expected = _ARTIFACT_SHA256[relative]
        _require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
                 "unsealed evidence identity")
        try:
            content = _source_path(relative).read_bytes()
        except OSError as error:
            raise DarkSectorProgressRefusal("unreadable evidence file") from error
        actual = hashlib.sha256(content).hexdigest()
        _require(actual == expected, "evidence hash mismatch")
        raw[relative] = content
        custody.append({"path": relative, "sha256": actual})
    return custody, raw


def _reject_constant(value: str) -> None:
    raise DarkSectorProgressRefusal(f"nonfinite JSON token: {value}")


def _receipt(raw: bytes, relative: str) -> dict[str, Any]:
    try:
        wrapper = json.loads(raw, parse_constant=_reject_constant)
        _require(type(wrapper) is dict and set(wrapper) == {"payload", "payload_sha256"},
                 "malformed wrapped receipt")
        payload = wrapper["payload"]
        _require(type(payload) is dict, "malformed payload")
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                               allow_nan=False).encode()
        digest = hashlib.sha256(canonical).hexdigest()
        _require(digest == wrapper["payload_sha256"] == _PAYLOAD_SHA256[relative],
                 "canonical receipt mismatch")
        return payload
    except (ValueError, TypeError, KeyError, UnicodeError) as error:
        raise DarkSectorProgressRefusal("malformed result receipt") from error


def _exact(value: Any, expected: Any, name: str) -> None:
    _require(type(value) is type(expected) and value == expected,
             f"changed recorded field: {name}")


def _recorded_summaries(raw: Mapping[str, bytes]) -> dict[str, Any]:
    spatial = _receipt(raw[_SPATIAL], _SPATIAL)
    helium = _receipt(raw[_HELIUM], _HELIUM)
    for key, expected in {
        "schema": "SPHERICAL_CONSISTENT_SAVED_AUDIT_V001",
        "status": "SAVED_ARITHMETIC_CHECKS_PASSED",
        "complete_saved_census": True, "numerical_entry_count": 141446,
        "failed_check_groups": 0, "all_saved_arithmetic_checks_passed": True,
        "reconstruction_checks_passed": True, "mandatory_lanes_open": 11,
        "trajectory_rerun": False, "independently_authored_reproduction": False,
    }.items():
        _exact(spatial.get(key), expected, f"spatial/{key}")
    qualification = spatial.get("qualification")
    _require(type(qualification) is dict and set(qualification) == {
        "Stage3_complete", "continuum", "formation", "full_metric",
        "observations", "physical_source", "trajectory"}, "changed spatial scope keys")
    _require(all(value is False for value in qualification.values()), "spatial promotion refused")
    checks = spatial.get("checks")
    _require(type(checks) is list and len(checks) == 1338, "changed saved group census")
    _require(all(type(row) is dict and row.get("passed") is True for row in checks),
             "saved spatial failure or malformed group")
    for key, expected in {
        "schema": "CLASS_THERMAL_HELIUM_CACHE_ATTRIBUTION_V001",
        "status": "SAVED_HELIUM_CACHE_ATTRIBUTION_COMPLETE",
        "thermal_qualified": False, "corrected_CLASS_derivatives_computed": False,
        "thermal_failure_waived": False, "Stage3_complete": False,
        "qualification": False, "propagation_allowed": False,
        "changed_interpolator": False, "new_locations_selected": False,
    }.items():
        _exact(helium.get(key), expected, f"helium/{key}")
    pairs = helium.get("pairs")
    _require(type(pairs) is list and len(pairs) == 2, "changed helium pair census")
    try:
        indexed = {row["location"]["pair"]: row for row in pairs}
        _require(set(indexed) == {"resolution", "atomic_step"}, "changed helium witnesses")
        for name, index in (("resolution", 726), ("atomic_step", 470)):
            _exact(indexed[name]["location"]["index"], index, f"helium/{name}/index")
            _exact(indexed[name]["orientation"], "quarter_minus_half", f"helium/{name}/orientation")
    except (KeyError, TypeError) as error:
        raise DarkSectorProgressRefusal("malformed helium witness") from error
    return {
        "spatial": {
            "recorded_status": spatial["status"], "recorded_numerical_entries": 141446,
            "recorded_check_groups": 1338, "recorded_failed_groups": 0,
            "hard_gap_parameters": (128, 8192), "spatial_domain_outer_face": 8,
            "recorded_states": 40, "recorded_fine_snapshots": 8,
            "review_kind": "INDEPENDENT_SOURCE_AND_SAVED_RESULT_REVIEW",
            "independently_authored_numerical_reproduction": False,
            "qualification": qualification,
            "adopted_inputs": ("EOS", "PHYSICAL_FORCE_LAW", "INITIAL_STATE", "FINITE_MESH"),
        },
        "helium": {
            "recorded_status": helium["status"],
            "orientation": "quarter_minus_half",
            "atomic_step_imported_difference_before": indexed["atomic_step"]["before_imported_difference"],
            "atomic_step_imported_difference_after": indexed["atomic_step"]["after_imported_difference"],
            "resolution_imported_difference_before": indexed["resolution"]["before_imported_difference"],
            "resolution_imported_difference_after": indexed["resolution"]["after_imported_difference"],
            "review_kind": "INDEPENDENT_CUSTODY_AND_SAVED_RESULT_INTERPRETATION",
            "corrected_CLASS_derivatives_computed": False, "thermal_qualified": False,
            "original_two_thermal_failures_preserved": True,
            "historical_CLASS_error_is_prediction_for_new_curve": False,
            "resolution_comparator_caveat": (
                "QUARTER_MINUS_HALF_AT_RESOLUTION_LOCATION_IS_NOT_THE_ORIGINAL_"
                "SMOKE64_MINUS_SMOKE128_RESOLUTION_TEST"
            ),
        },
        "gl6cu": {
            "recorded_status": "SELECTED_F3_Q4_H6_SOURCE_JET_INVENTORY_CLOSED",
            "scope": "FIXED_PLUS_SOURCE_EFFECTIVE_HAMILTONIAN_FIRST_AND_MIXED_SECOND_JETS",
            "recorded_raw_source_coordinates": 768,
            "recorded_enumerated_supports": 4096, "recorded_selected_nonbare_jets": 3904,
            "recorded_inactive_cycles_not_differentiated": 192,
            "recorded_stencil_classes": 1654, "full_coefficient_export": False,
            "review_kind": "ARCHIVED_HOSTILE_AUDIT_REPORTED_NOT_REEXECUTED_HERE",
            "same_parent_as_native_96D_AB": False,
            "stationary_connected_response_completed": False,
            "physical_source_embedding_completed": False, "ward_1pi_completed": False,
        },
    }


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(child) for key, child in value.items()})
    if isinstance(value, (tuple, list)):
        return tuple(_freeze(child) for child in value)
    return value


def _certificate() -> Mapping[str, Any]:
    custody, raw = _custody()
    try:
        summaries = _recorded_summaries(raw)
    except (KeyError, TypeError) as error:
        raise DarkSectorProgressRefusal("malformed recorded summary") from error
    _require(len(MANDATORY_LANES) == len(set(MANDATORY_LANES)) == 11,
             "changed mandatory lane census")
    return _freeze({
        "schema": SCHEMA, "claim_class": CLAIM_CLASS,
        "checkpoint": {"frontier": "V077", "outstanding_ledger": "V018"},
        "checkpoint_status": "RECORDED_FINITE_PROGRESS_NOT_PHYSICALLY_CLOSED",
        "custody": custody,
        "verification_performed_by_this_call": {
            "direct_artifact_sha256_count": 11, "canonical_payload_sha256_count": 2,
            "saved_summary_shape_and_scope_checked": True,
            "all_transitive_sources_authenticated": False,
            "manifest_children_rehashed": False, "numerical_checks_recomputed": False,
            "scientific_producer_executed": False, "observations_retested": False,
        },
        "recorded_evidence": summaries,
        "mandatory_lanes": tuple({"id": name, "overall_status": "OPEN"} for name in MANDATORY_LANES),
        "required_lane_count": 11, "cmb_lanes_are_distinct": True,
        "physical_promotion_flags": {name: False for name in PROMOTION_FLAGS},
        "unresolved_inputs": (
            "PHYSICAL_SOURCE_CLOCK_VOLUME_DICTIONARY", "NATIVE_FORMATION_RULE_AND_STATE",
            "COMPLETE_SOURCE_AND_SWITCHING_WORK", "SAME_STATE_CROSS_DOMAIN_PREDICTIONS",
            "INDEPENDENT_UNUSED_OBSERVATIONAL_COMPARISON",
        ),
        "failures_preserved_at_checkpoint": (
            "SPHERICAL_QUADRATURE_V001_FAILURES_NOT_WAIVED_BY_EXACT_KERNEL",
            "SPHERICAL_DRIVER_V001_SYNTAX_FAILURE_PRESERVED",
            "THERMAL_RESOLUTION_AND_ATOMIC_STEP_FAILURES_NOT_WAIVED",
            "C2_SYNTHETIC_V002_BUILD_FAILURE_NO_PRODUCTION_QUALIFICATION",
        ),
        "urm_role": {
            "local_development_only": True, "portable_release_capsule": False,
            "load_bearing_for_existing_theorems": False,
            "candidate_v001_replaced": False, "custody_pass_is_scientific_pass": False,
        },
    })


@dataclass(frozen=True, init=False)
class DarkSectorProgress:
    """Zero-input immutable handle; each read authenticates the fixed snapshot."""

    claim_class: str = CLAIM_CLASS

    def certificate(self) -> Mapping[str, Any]:
        return _certificate()


def dark_sector_progress() -> DarkSectorProgress:
    _certificate()
    return DarkSectorProgress()


def dark_sector_progress_certificate() -> Mapping[str, Any]:
    return _certificate()
