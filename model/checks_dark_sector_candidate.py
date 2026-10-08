"""Small custody/scope controls. Synthetic fixtures have zero scientific weight."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import hashlib
import inspect
from pathlib import Path
from tempfile import TemporaryDirectory
from types import MappingProxyType
from unittest import mock

import dark_sector_candidate as candidate


def _raises(error_type, call) -> bool:
    try:
        call()
    except error_type:
        return True
    return False


def _set(mapping, key, value) -> None:
    mapping[key] = value


def _deeply_immutable(value) -> bool:
    if isinstance(value, MappingProxyType):
        return all(_deeply_immutable(child) for child in value.values())
    if isinstance(value, tuple):
        return all(_deeply_immutable(child) for child in value)
    return isinstance(value, (str, int, float, bool, type(None)))


def run_dark_sector_candidate_checks(check, *, include_urm: bool = True) -> None:
    """Run real checkpoint checks and isolated synthetic refusal controls."""
    certificate = candidate.dark_sector_candidate_certificate()
    handle = candidate.dark_sector_candidate()
    check("candidate zero-input handle", not inspect.signature(candidate.dark_sector_candidate).parameters)
    check("candidate zero-input certificate", not inspect.signature(candidate.dark_sector_candidate_certificate).parameters)
    check("candidate rejects data", _raises(TypeError, lambda: candidate.dark_sector_candidate({})))
    check("candidate rejects fitted parameters", _raises(TypeError, lambda: candidate.dark_sector_candidate_certificate(a0=1)))
    check("constructor cannot override classification", _raises(TypeError, lambda: candidate.DarkSectorCandidate(claim_class="PROVED")))
    check("candidate handle immutable", _raises(FrozenInstanceError, lambda: setattr(handle, "claim_class", "PROVED")))
    check("candidate handle equals direct certificate", handle.certificate() == certificate)
    check("candidate schema", certificate["schema"] == candidate.SCHEMA)
    check("candidate scoped class", certificate["claim_class"] == candidate.CLAIM_CLASS)
    check("candidate certificate immutable", isinstance(certificate, MappingProxyType))
    check("entire certificate deeply immutable", _deeply_immutable(certificate))
    check("nested gate immutable", isinstance(certificate["same_state_cross_domain_gate"], MappingProxyType))
    check("candidate cannot mutate stage", _raises(TypeError, lambda: _set(certificate, "stage_3_complete", True)))
    check("candidate cannot mutate gate", _raises(TypeError, lambda: _set(certificate["same_state_cross_domain_gate"], "passed", True)))
    check("candidate unclosed", certificate["checkpoint_status"] == "CANDIDATE_NOT_PHYSICALLY_CLOSED")
    check("all eleven required lanes retained", certificate["required_lane_count"] == 11)
    lanes = certificate["mandatory_lanes"]
    check("eleven unique lane identities", len(lanes) == len({row["id"] for row in lanes}) == 11)
    check("lane order and identities", tuple(row["id"] for row in lanes) == tuple(row[0] for row in candidate.MANDATORY_LANES))
    check("no required lane silently closed", all(row["overall_status"] == "OPEN" for row in lanes))
    check("distinct CMB obligations", certificate["cmb_lanes_are_distinct"] is True and {"cmb_perturbations_observations", "network_cmb_thermal_origin"}.issubset(row["id"] for row in lanes))
    for key in ("source_clock_volume_map", "network_state_formation", "shared_energy_force_volume_creation_work"):
        check(f"unresolved {key}", certificate["physical_closure"][key] == "UNRESOLVED")
    gate = certificate["same_state_cross_domain_gate"]
    check("shared-state gate unqualified", gate["status"] == "UNQUALIFIED_PENDING_DERIVATION_AND_TEST")
    check("shared-state gate does not pass", gate["passed"] is False)
    check("shared-state predictions not ready", gate["prediction_ready"] is False)
    check("all shared-state obligations retained", gate["obligations"] == candidate.SHARED_STATE_OBLIGATIONS)
    for key in ("stage_3_complete", "dark_components_superfluous", "empirical_superiority_established"):
        check(f"no promotion {key}", certificate[key] is False)
    for key in ("load_bearing_for_existing_closure", "input_to_finite_gate_or_gravity_closure", "scientific_solver_executed", "custody_pass_is_scientific_pass"):
        check(f"non-load-bearing {key}", certificate["urm_role"][key] is False)
    check("all explicit ceilings retained", certificate["excluded_promotions"] == candidate.EXCLUDED_PROMOTIONS)
    check("custody source set exact", tuple(row["path"] for row in certificate["custody"]) == candidate._SOURCE_PATHS)
    for row in certificate["custody"]:
        check(f"real source hash {row['path']}", hashlib.sha256(candidate._source_path(row["path"]).read_bytes()).hexdigest() == row["sha256"])

    # Isolated file-control fixture: no scientific source is changed or trusted.
    with TemporaryDirectory(prefix="urm-dark-custody-") as scratch:
        root = Path(scratch)
        hashes = {}
        for index, relative in enumerate(candidate._SOURCE_PATHS):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(f"synthetic custody control {index}\n".encode())
            hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        with mock.patch.object(candidate, "_PROJECT_ROOT", root), mock.patch.object(candidate, "_ARTIFACT_SHA256", hashes):
            control = candidate.dark_sector_candidate_certificate()
            check("synthetic matching custody positive control", len(control["custody"]) == 2)
            check("synthetic custody cannot promote science", control["dark_components_superfluous"] is False and control["stage_3_complete"] is False)
            for relative in ("../outside.md", "/absolute.md", "a/../b.md", "a//b.md", "./a.md", ""):
                check(f"refuse noncanonical path {relative!r}", _raises(candidate.DarkSectorCandidateRefusal, lambda relative=relative: candidate._source_path(relative)))
            check("refuse nonstring path", _raises(candidate.DarkSectorCandidateRefusal, lambda: candidate._source_path(None)))
            first = root / candidate._SOURCE_PATHS[0]
            saved = first.read_bytes()
            first.write_bytes(saved + b"tampered")
            check("refuse altered authoritative source", _raises(candidate.DarkSectorCandidateRefusal, candidate.dark_sector_candidate_certificate))
            first.write_bytes(saved)
            moved = first.with_name("synthetic-saved.md")
            first.rename(moved)
            check("refuse missing authoritative source", _raises(candidate.DarkSectorCandidateRefusal, candidate.dark_sector_candidate_certificate))
            first.symlink_to(moved)
            check("refuse leaf symlink even to matching bytes", _raises(candidate.DarkSectorCandidateRefusal, candidate.dark_sector_candidate_certificate))
            first.unlink()
            moved.rename(first)
            directory = first.parent
            relocated = directory.with_name(directory.name + "-relocated")
            directory.rename(relocated)
            directory.symlink_to(relocated, target_is_directory=True)
            check("refuse directory symlink", _raises(candidate.DarkSectorCandidateRefusal, candidate.dark_sector_candidate_certificate))
            directory.unlink()
            relocated.rename(directory)
            for bad in (None, "", "0" * 63, "A" * 64):
                changed = dict(hashes)
                changed[candidate._SOURCE_PATHS[0]] = bad
                with mock.patch.object(candidate, "_ARTIFACT_SHA256", changed):
                    check(f"refuse unsealed malformed digest {bad!r}", _raises(candidate.DarkSectorCandidateRefusal, candidate.dark_sector_candidate_certificate))
            with mock.patch.object(candidate, "_ARTIFACT_SHA256", {candidate._SOURCE_PATHS[0]: hashes[candidate._SOURCE_PATHS[0]]}):
                check("refuse incomplete custody set", _raises(candidate.DarkSectorCandidateRefusal, candidate.dark_sector_candidate_certificate))
            with mock.patch.object(candidate, "_ARTIFACT_SHA256", {**hashes, "extra.md": "0" * 64}):
                check("refuse expanded custody set", _raises(candidate.DarkSectorCandidateRefusal, candidate.dark_sector_candidate_certificate))
            check("positive control restored after mutations", candidate.dark_sector_candidate_certificate() == control)

    check("real custody unaffected by controls", candidate.dark_sector_candidate_certificate() == certificate)
    if include_urm:
        from project_model import URM
        check("URM zero-input candidate", not inspect.signature(URM.dark_sector_candidate).parameters)
        check("URM zero-input certificate", not inspect.signature(URM.dark_sector_candidate_certificate).parameters)
        check("URM candidate delegates", URM.dark_sector_candidate().certificate() == certificate)
        check("URM certificate delegates", URM.dark_sector_candidate_certificate() == certificate)
        check("URM refuses calibration injection", _raises(TypeError, lambda: URM.dark_sector_candidate_certificate(parameters={})))
