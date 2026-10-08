"""Custody/summary/refusal controls; all temporary fixtures are non-scientific."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import hashlib
import inspect
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import MappingProxyType
from unittest import mock

import dark_sector_progress as progress


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


def run_dark_sector_progress_checks(check, *, include_urm: bool = True) -> None:
    """Read the actual checkpoint, then isolate all negative controls in temp files."""
    certificate = progress.dark_sector_progress_certificate()
    handle = progress.dark_sector_progress()
    for function in (progress.dark_sector_progress, progress.dark_sector_progress_certificate):
        check(f"zero-input {function.__name__}", not inspect.signature(function).parameters)
        check(f"refuse caller data {function.__name__}", _raises(TypeError, lambda function=function: function({})))
        check(f"refuse fitted dial {function.__name__}", _raises(TypeError, lambda function=function: function(a0=1)))
    check("constructor rejects promoted classification", _raises(TypeError, lambda: progress.DarkSectorProgress(claim_class="PROVED")))
    check("handle is frozen", _raises(FrozenInstanceError, lambda: setattr(handle, "claim_class", "PROVED")))
    check("handle/direct certificate equivalence", handle.certificate() == certificate)
    check("fixed progress schema", certificate["schema"] == "URM_DARK_SECTOR_PROGRESS_V001")
    check("fixed candidate classification", certificate["claim_class"] == progress.CLAIM_CLASS)
    check("fixed V077 V018 snapshot", dict(certificate["checkpoint"]) == {"frontier": "V077", "outstanding_ledger": "V018"})
    check("deeply immutable output", _deeply_immutable(certificate))
    check("top-level mutation refused", _raises(TypeError, lambda: _set(certificate, "schema", "PROVED")))
    check("nested physical promotion refused", _raises(TypeError, lambda: _set(certificate["physical_promotion_flags"], "stage_3_complete", True)))
    check("nested recorded-result mutation refused", _raises(TypeError, lambda: _set(certificate["recorded_evidence"]["spatial"], "recorded_failed_groups", -1)))
    lanes = certificate["mandatory_lanes"]
    check("eleven mandatory lanes", certificate["required_lane_count"] == len(lanes) == 11)
    check("eleven unique lane identities", len({row["id"] for row in lanes}) == 11)
    check("fixed lane order", tuple(row["id"] for row in lanes) == progress.MANDATORY_LANES)
    check("all lanes open", all(row["overall_status"] == "OPEN" for row in lanes))
    check("two CMB lanes remain distinct", {"cmb_perturbations_observations", "network_cmb_thermal_origin"}.issubset(row["id"] for row in lanes))
    check("all promotion flags present", set(certificate["physical_promotion_flags"]) == set(progress.PROMOTION_FLAGS))
    check("all physical promotion flags false", all(value is False for value in certificate["physical_promotion_flags"].values()))
    performed = certificate["verification_performed_by_this_call"]
    check("eleven direct hashes checked", performed["direct_artifact_sha256_count"] == 11)
    check("two canonical payloads checked", performed["canonical_payload_sha256_count"] == 2)
    for key in ("all_transitive_sources_authenticated", "manifest_children_rehashed",
                "numerical_checks_recomputed", "scientific_producer_executed", "observations_retested"):
        check(f"no implied replay {key}", performed[key] is False)
    spatial = certificate["recorded_evidence"]["spatial"]
    check("spatial recorded scalar census", spatial["recorded_numerical_entries"] == 141446)
    check("spatial recorded groups/failures", (spatial["recorded_check_groups"], spatial["recorded_failed_groups"]) == (1338, 0))
    check("hard-gap parameters are not radii", spatial["hard_gap_parameters"] == (128, 8192) and spatial["spatial_domain_outer_face"] == 8)
    check("same-author numerical boundary", spatial["independently_authored_numerical_reproduction"] is False)
    check("spatial physical flags false", all(value is False for value in spatial["qualification"].values()))
    helium = certificate["recorded_evidence"]["helium"]
    check("signed atomic witness retained", helium["atomic_step_imported_difference_before"] < 0 < helium["atomic_step_imported_difference_after"])
    check("unchanged resolution-location import", helium["resolution_imported_difference_before"] == helium["resolution_imported_difference_after"])
    check("thermal failures retained", helium["original_two_thermal_failures_preserved"] is True and helium["thermal_qualified"] is False)
    check("no corrected CLASS derivatives claimed", helium["corrected_CLASS_derivatives_computed"] is False)
    check("no borrowed old CLASS error prediction", helium["historical_CLASS_error_is_prediction_for_new_curve"] is False)
    cu = certificate["recorded_evidence"]["gl6cu"]
    check("GL6CU selected versus enumerated census", (cu["recorded_enumerated_supports"], cu["recorded_selected_nonbare_jets"]) == (4096, 3904))
    check("GL6CU inactive cycles retained", cu["recorded_inactive_cycles_not_differentiated"] == 192)
    check("GL6CU compact not full coefficient export", cu["recorded_stencil_classes"] == 1654 and cu["full_coefficient_export"] is False)
    check("GL6CU not 96D A/B parent", cu["same_parent_as_native_96D_AB"] is False)
    check("GL6CU physical response remains incomplete", all(cu[key] is False for key in ("stationary_connected_response_completed", "physical_source_embedding_completed", "ward_1pi_completed")))
    for key in ("portable_release_capsule", "load_bearing_for_existing_theorems", "candidate_v001_replaced", "custody_pass_is_scientific_pass"):
        check(f"nonpromoting URM role {key}", certificate["urm_role"][key] is False)
    check("direct evidence exact path set", tuple(row["path"] for row in certificate["custody"]) == progress._SOURCE_PATHS)
    originals = {relative: progress._source_path(relative).read_bytes() for relative in progress._SOURCE_PATHS}
    for relative, raw in originals.items():
        check(f"real evidence identity {relative}", hashlib.sha256(raw).hexdigest() == progress._ARTIFACT_SHA256[relative])

    # Copy already-authenticated bytes only. Nothing in the research tree is edited.
    with TemporaryDirectory(prefix="urm-dark-progress-") as scratch:
        root = Path(scratch)
        for relative, raw in originals.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        with mock.patch.object(progress, "_PROJECT_ROOT", root):
            check("isolated byte-copy positive control", progress.dark_sector_progress_certificate() == certificate)
            for relative in ("../outside.md", "/absolute.md", "a/../b.md", "a//b.md", "./a.md", "", "unregistered.md", None):
                check(f"refuse noncanonical/unowned path {relative!r}", _raises(progress.DarkSectorProgressRefusal, lambda relative=relative: progress._source_path(relative)))
            first = root / progress._SOURCE_PATHS[0]
            first.write_bytes(originals[progress._SOURCE_PATHS[0]] + b"changed")
            check("mutation refused even through old handle", _raises(progress.DarkSectorProgressRefusal, handle.certificate))
            first.write_bytes(originals[progress._SOURCE_PATHS[0]])
            moved = first.with_name("held-original.md")
            first.rename(moved)
            check("missing source refused", _raises(progress.DarkSectorProgressRefusal, progress.dark_sector_progress_certificate))
            first.symlink_to(moved)
            check("matching-byte leaf symlink refused", _raises(progress.DarkSectorProgressRefusal, progress.dark_sector_progress_certificate))
            first.unlink()
            moved.rename(first)
            directory = first.parent
            relocated = directory.with_name(directory.name + "-held")
            directory.rename(relocated)
            directory.symlink_to(relocated, target_is_directory=True)
            check("ancestor symlink refused", _raises(progress.DarkSectorProgressRefusal, progress.dark_sector_progress_certificate))
            directory.unlink()
            relocated.rename(directory)
            for bad in (None, "", "0" * 63, "A" * 64):
                pins = dict(progress._ARTIFACT_SHA256)
                pins[progress._SOURCE_PATHS[0]] = bad
                with mock.patch.object(progress, "_ARTIFACT_SHA256", pins):
                    check(f"malformed pin refused {bad!r}", _raises(progress.DarkSectorProgressRefusal, progress.dark_sector_progress_certificate))
            with mock.patch.object(progress, "_ARTIFACT_SHA256", {}):
                check("missing custody set refused", _raises(progress.DarkSectorProgressRefusal, progress.dark_sector_progress_certificate))
            with mock.patch.object(progress, "_ARTIFACT_SHA256", {**progress._ARTIFACT_SHA256, "extra": "0" * 64}):
                check("expanded custody set refused", _raises(progress.DarkSectorProgressRefusal, progress.dark_sector_progress_certificate))
            with mock.patch.object(progress, "MANDATORY_LANES", (progress.MANDATORY_LANES[0],) * 11):
                check("duplicate lane census refused", _raises(progress.DarkSectorProgressRefusal, progress.dark_sector_progress_certificate))

            # Synthetic repinned fixtures test semantic refusal beyond byte custody.
            # They are never accepted as scientific evidence or written outside temp.
            def malformed_result(relative, mutate, *, repin_payload=True):
                wrapper = json.loads(originals[relative])
                mutate(wrapper["payload"])
                encoded = json.dumps(wrapper["payload"], sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
                payload_digest = hashlib.sha256(encoded).hexdigest()
                if repin_payload:
                    wrapper["payload_sha256"] = payload_digest
                changed = json.dumps(wrapper, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
                path = root / relative
                path.write_bytes(changed)
                pins = {**progress._ARTIFACT_SHA256, relative: hashlib.sha256(changed).hexdigest()}
                payload_pins = dict(progress._PAYLOAD_SHA256)
                if repin_payload:
                    payload_pins[relative] = payload_digest
                try:
                    with mock.patch.object(progress, "_ARTIFACT_SHA256", pins), mock.patch.object(progress, "_PAYLOAD_SHA256", payload_pins):
                        return _raises(progress.DarkSectorProgressRefusal, progress.dark_sector_progress_certificate)
                finally:
                    path.write_bytes(originals[relative])

            check("canonical payload mutation refused", malformed_result(progress._SPATIAL, lambda payload: _set(payload, "status", "changed"), repin_payload=False))
            check("repinned false scalar census refused", malformed_result(progress._SPATIAL, lambda payload: _set(payload, "numerical_entry_count", 1)))
            check("boolean not accepted as integer count", malformed_result(progress._SPATIAL, lambda payload: _set(payload, "failed_check_groups", False)))
            check("repinned spatial promotion refused", malformed_result(progress._SPATIAL, lambda payload: _set(payload["qualification"], "formation", True)))
            check("repinned missing group refused", malformed_result(progress._SPATIAL, lambda payload: payload["checks"].pop()))
            check("repinned failed group refused", malformed_result(progress._SPATIAL, lambda payload: _set(payload["checks"][0], "passed", False)))
            check("repinned helium qualification refused", malformed_result(progress._HELIUM, lambda payload: _set(payload, "thermal_qualified", True)))
            check("repinned CLASS prediction refused", malformed_result(progress._HELIUM, lambda payload: _set(payload, "corrected_CLASS_derivatives_computed", True)))
            check("repinned thermal waiver refused", malformed_result(progress._HELIUM, lambda payload: _set(payload, "thermal_failure_waived", True)))
            check("repinned witness selection refused", malformed_result(progress._HELIUM, lambda payload: _set(payload["pairs"][0]["location"], "index", 0)))
            check("positive fixture restored", progress.dark_sector_progress_certificate() == certificate)

    check("real evidence unchanged after fixtures", progress.dark_sector_progress_certificate() == certificate)
    if include_urm:
        from project_model import URM
        check("URM zero-input progress", not inspect.signature(URM.dark_sector_progress).parameters)
        check("URM zero-input progress certificate", not inspect.signature(URM.dark_sector_progress_certificate).parameters)
        check("URM handle delegation", URM.dark_sector_progress().certificate() == certificate)
        check("URM certificate delegation", URM.dark_sector_progress_certificate() == certificate)
        check("URM refuses parameter injection", _raises(TypeError, lambda: URM.dark_sector_progress_certificate(parameters={})))
        check("old candidate schema preserved", URM.dark_sector_candidate_certificate()["schema"] == "URM_SHARED_DARK_SECTOR_CANDIDATE_V001")

