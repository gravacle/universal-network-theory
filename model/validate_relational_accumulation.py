#!/usr/bin/env python3
"""Fail-closed validator for the current ARGER Gate public URM surface."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from decimal import Decimal
import hashlib
import inspect
from types import MappingProxyType

import relational_accumulation as ra
from project_model import URM


passed = 0


def check(condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError("relational accumulation validation failed")
    passed += 1


def chk(name: str, condition: bool) -> None:
    """Expose a proof-catalogue gate name without changing the frozen check count."""
    if not condition:
        raise AssertionError(name)


def type_error(callable_object) -> bool:
    try:
        callable_object()
    except TypeError:
        return True
    return False


def refused(callable_object) -> bool:
    try:
        callable_object()
    except ra.RelationalAccumulationRefusal:
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


def validate_pins(pins, rows, json_count: int) -> None:
    check(tuple(row["label"] for row in rows) == tuple(pin.label for pin in pins))
    for index, (pin, row) in enumerate(zip(pins, rows)):
        path = ra._root_path(pin.path)
        check(path.is_file() and not path.is_symlink())
        check(hashlib.sha256(path.read_bytes()).hexdigest() == pin.sha256)
        check(row["path"] == pin.path and row["sha256"] == pin.sha256)
        check(row["kind"] == ("JSON" if index < json_count else "TEXT_OR_SOURCE"))


def main() -> int:
    check(tuple(inspect.signature(ra.relational_accumulation).parameters) == ())
    check(tuple(inspect.signature(
        ra.relational_accumulation_certificate
    ).parameters) == ())
    check(type_error(lambda: ra.relational_accumulation({})))
    check(type_error(lambda: ra.relational_accumulation_certificate(data={})))
    check(refused(lambda: ra._root_path("../outside")))

    handle = ra.relational_accumulation()
    certificate = handle.certificate()
    second = ra.relational_accumulation_certificate()
    check(handle.claim_class == ra.CLAIM_CLASS)
    check(frozen_error(lambda: set_claim_class(handle)))
    check(certificate == second and certificate is not second)
    check(certificate["exact_l12"] is not second["exact_l12"])
    check(isinstance(certificate, MappingProxyType))
    check(isinstance(certificate["governing_arger_gate"], MappingProxyType))
    check(isinstance(certificate["governing_arger_gate"]["sizes"], tuple))
    check(isinstance(certificate["strict_common_lineage_progression"], MappingProxyType))
    check(isinstance(certificate["strict_common_lineage_progression"]["table"], tuple))
    check(type_error(lambda: mutate(certificate, "schema", "changed")))

    check(tuple(certificate) == (
        "schema",
        "claim_class",
        "definitions",
        "custody",
        "exact_l12",
        "authenticated_manifest",
        "governing_arger_gate",
        "gravity_formation_boundary",
        "dynamic_z1",
        "strict_common_lineage_progression",
        "relational_l14",
        "excluded_promotions",
        "executable_scope",
    ))
    check(certificate["schema"] == ra.SCHEMA)
    check(certificate["claim_class"] == ra.CLAIM_CLASS)

    public_pins = ra._GOVERNING_ARTIFACTS + ra._TEXT_ARTIFACTS
    check(certificate["custody"]["scope"] == "GOVERNING_ARGER_GATE_ONLY")
    check(certificate["custody"]["artifact_count"] == len(public_pins) == 12)
    check(all(pin.label != "l14_disposition" for pin in public_pins))
    check(all(pin.path != "L14_RUN_DISPOSITION_2026-09-16.md"
              for pin in public_pins))
    validate_pins(
        public_pins,
        certificate["custody"]["artifacts"],
        len(ra._GOVERNING_ARTIFACTS),
    )

    exact = certificate["exact_l12"]
    check(exact["checks_passed"] == exact["checks_total"] == 1156)
    check(exact["maximum_sector_weight_difference"] == 8.326672684688674e-16)
    check(exact["maximum_terminal_amplitude_difference"] == 7.946965413254846e-17)
    check(exact["tolerance"] == 1e-8)

    manifest = certificate["authenticated_manifest"]
    check(manifest["schema"] == "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001")
    check(manifest["status"] ==
          "PASS_RELATIONAL_ACCUMULATION_L4_L12__SPECTRUM_MANIFEST_READY")
    check(manifest["atom_count"] == 24)
    check(manifest["accumulated_interval"] == ((1, 48), (17, 48)))
    check(manifest["finite_sizes"] == (4, 6, 8, 10, 12))

    progression = certificate["strict_common_lineage_progression"]
    check(progression["schema"] == "STRICT_COMMON_LINEAGE_PROGRESSION_V001")
    check(progression["status"] == "PASS__FINITE_COMPUTED_MONOTONIC_PROGRESSION")
    check(progression["measure"] == "DECLARED_FINITE_PBAR_Q_COMMON_LINEAGE_SUPPORT")
    check(progression["source_path"] == ra._PROGRESSION_SOURCE_PATH)
    check(progression["source_sha256"] == ra._PROGRESSION_SOURCE_SHA256)
    check(tuple(
        (row["path"], row["sha256"]) for row in progression["verified_inputs"]
    ) == ra._PROGRESSION_INPUT_PINS)
    values = {row["scale"]: row["support"] for row in progression["table"]}
    check(values["L08"] == 0.0244800482)
    check(values["L10"] == 0.0687369678)
    check(values["L12_TARGET"] == 0.11570852222694002)
    check(values["L12_HOSTILE"] == 0.11570852222694036)
    check(values["L12_CONSERVATIVE"] == 0.11570852222694002)
    check(values["L14"] == ra.L14_STATUS)
    check(values["L08"] < values["L10"] < values["L12_CONSERVATIVE"])
    check(progression["strictly_increasing_through_l12"] is True)
    check(
        progression["capsule_reproduction_scope"]
        == (
            "L08_L10_RECOMPUTED__L12_FULL_WORKFLOW_RESULT_AND_CUSTODY_"
            "AUTHENTICATED"
        )
    )
    l12_custody = progression["l12_full_workflow_custody"]
    check(
        l12_custody["review_rerun_status"]
        == "PASS__BYTE_IDENTICAL_TO_SEALED_REPORT"
    )
    check(l12_custody["minimum_runnable_input_files"] == 86)
    check(l12_custody["minimum_runnable_input_bytes"] == 13485786130)
    check(l12_custody["minimum_runnable_input_gib"] == "12.559617")
    check(l12_custody["audited_workspace_approx_gib"] == "58.8")
    check(progression["governing_arger_gate_premise"] is False)
    check(progression["fit_performed"] is False)
    check(progression["monotone_continuation_theorem"] is False)
    check(progression["asymptotic_extrapolation_theorem"] is False)
    check(progression["l14_value_inferred"] is False)

    gate = certificate["governing_arger_gate"]
    check(gate["gate_id"] == ra.ARGER_GATE_ID == "ARGER-GATE")
    check(gate["canonical_name"] == ra.ARGER_GATE_NAME == "ARGER Gate")
    check(
        gate["archival_implementation_id"]
        == ra.ARCHIVAL_ARGER_GATE_ID
        == "ARGER-GATE-1"
    )
    check(
        gate["archival_implementation_name"]
        == ra.ARCHIVAL_ARGER_GATE_NAME
        == "ARGER Gate 1"
    )
    check(gate["standard"] == ra.FINITE_Z1_STANDARD)
    check(gate["adoption"] == ra.ARGER_GATE_ADOPTION)
    check(gate["governing"] is True)
    check(gate["classified_object"] == "COMPLETE_A009_A016_BOUNDED_RECORD_BLOCK")
    check(gate["atoms"] == tuple(f"A{index:03d}" for index in range(9, 17)))
    check(gate["density_interval"] == ((7, 48), (13, 48)))
    check(gate["finite_sizes"] == (4, 6, 8, 10, 12))
    expected_rows = (
        (4, (1, 2), "0.7260206189754993"),
        (6, (2, 3), "0.5846615608350367"),
        (8, (2, 3, 4), "0.7373965730354166"),
        (10, (3, 4, 5), "0.6500987927669427"),
        (12, (4, 5, 6), "0.56956498393327842"),
    )
    check(tuple(
        (row["L"], row["selected_q"], row["deduplicated_pbar_mass"])
        for row in gate["sizes"]
    ) == expected_rows)
    for row in gate["sizes"]:
        check(Decimal(row["deduplicated_pbar_mass"]) > Decimal("0.50"))
        check(row["majority_threshold"] == "0.50")
        check(row["majority_pass"] is True)
    predicates = gate["predicates"]
    check(predicates["bounded_extendible_record_membership"] is True)
    check(predicates["independent_structural_audit"] == "PASS")
    check(predicates[
        "deduplicated_mass_strictly_above_one_half_at_each_size"
    ] is True)
    check(predicates["every_selected_sector_positive_finite_visibility"] is True)
    chk(
        "ARGER Gate evidence premises pass",
        predicates["bounded_extendible_record_membership"] is True
        and predicates["independent_structural_audit"] == "PASS"
        and predicates[
            "deduplicated_mass_strictly_above_one_half_at_each_size"
        ] is True
        and predicates["every_selected_sector_positive_finite_visibility"] is True,
    )
    visibility = gate["finite_visibility"]
    check(visibility["unique_sector_count"] == 13)
    check(visibility["minimum_R_low"] == "0.4280947078156539")
    check(visibility["minimum_w_star"] == "0.5")
    check(gate["pure_verifier"] == {
        "schema": "WAC_ARGER_GATE_EVIDENCE_V001",
        "status": "PASS__ADOPTED_GOVERNING_FINITE_Z1_ARGER_GATE",
    })
    check(gate["decision"] == "PASS_FINITE_DISCRETE_GFT_Z1_L4_L12")
    check(gate["l12_decision"] == "PASS_FINITE_DISCRETE_GFT_Z1")
    chk(
        "Authenticated record block passes the ARGER Gate",
        gate["decision"] == "PASS_FINITE_DISCRETE_GFT_Z1_L4_L12"
        and gate["l12_decision"] == "PASS_FINITE_DISCRETE_GFT_Z1",
    )

    gate_text = {pin.label: ra._load_text(pin) for pin in ra._TEXT_ARTIFACTS}
    direct_gate = ra._verify_governing_arger_gate(
        {pin.label: pin for pin in ra._GOVERNING_ARTIFACTS}, gate_text
    )
    check(direct_gate["pure_gate_status"] ==
          "PASS__ADOPTED_GOVERNING_FINITE_Z1_ARGER_GATE")

    boundary = certificate["gravity_formation_boundary"]
    check(
        boundary["finite_discrete_phase"] ==
        "ESTABLISHED_UNDER_ADOPTED_ARGER_GATE"
        and boundary["finite_gate_proof_obligation"] == "COMPLETE_THROUGH_L12"
    )
    check(boundary["conditional_rgrl_wtc_infrared_response"] ==
          "SEPARATE_EXISTING_GFT_LAYER_UNCHANGED")
    check(boundary["continuum_einstein_or_empirical_gravity_from_this_gate"] is False)
    check(boundary["numerical_g_from_this_gate"] is False)

    dynamic = certificate["dynamic_z1"]
    check(dynamic["same_model_ll_p"]["status"] == "CONDITIONAL_PHYSICAL_THEOREM")
    check(dynamic["same_model_ll_p"]["premise_id"] == "LL-P")
    check(dynamic["relationship_to_finite_gate"] ==
          "SUPPLEMENTARY_NOT_AN_UNFINISHED_GATE_REQUIREMENT")
    check(dynamic["finite_arger_gate_is_dynamic_exponent_proof"] is False)

    l14 = certificate["relational_l14"]
    check(l14["status"] == ra.L14_STATUS ==
          "INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT")
    check(l14["authenticated_final_report"] is None)
    check(l14["scientific_result"] is None)
    check(l14["l14_value"] is None)
    check(l14["branch_results_complete"] is False)
    check(l14["resumable_from_preservation"] is False)
    check(l14["closed_scout_protocol"]["status"] ==
          "CLOSED_WITHOUT_SCIENTIFIC_ADJUDICATION")
    check(l14["l14_progression_admission"]["admitted"] is False)

    check(certificate["excluded_promotions"] == ra.EXCLUDED_PROMOTIONS)
    check(certificate["executable_scope"]["caller_arguments"] == 0)
    check(certificate["executable_scope"]["physics_recalculated"] is False)
    check(certificate["executable_scope"]["external_result_accepted"] is False)

    # Refuse every undeclared JSON dependency while the public Gate runs.
    original_load_json = ra._load_json
    allowed_labels = {pin.label for pin in ra._GOVERNING_ARTIFACTS}
    observed_labels = []

    def current_only(pin):
        if pin.label not in allowed_labels:
            ra._refuse(f"simulated undeclared JSON dependency: {pin.label}")
        observed_labels.append(pin.label)
        return original_load_json(pin)

    try:
        ra._load_json = current_only
        isolated = ra.relational_accumulation_certificate()
        check(isolated["governing_arger_gate"]["decision"] ==
              "PASS_FINITE_DISCRETE_GFT_Z1_L4_L12")
        check(isolated["strict_common_lineage_progression"][
            "governing_arger_gate_premise"
        ] is False)
        check(set(observed_labels) == allowed_labels)
    finally:
        ra._load_json = original_load_json

    # L14 is informational scope and is not a custody input.
    original_root_path = ra._root_path

    def without_l14_disposition(relative):
        if relative == "L14_RUN_DISPOSITION_2026-09-16.md":
            ra._refuse("simulated unavailable L14 disposition")
        return original_root_path(relative)

    try:
        ra._root_path = without_l14_disposition
        without_l14 = ra.relational_accumulation_certificate()
        check(without_l14["governing_arger_gate"]["decision"] ==
              "PASS_FINITE_DISCRETE_GFT_Z1_L4_L12")
        check(without_l14["relational_l14"]["status"] == ra.L14_STATUS)
    finally:
        ra._root_path = original_root_path

    check(tuple(inspect.signature(URM.relational_accumulation).parameters) == ())
    check(tuple(inspect.signature(
        URM.relational_accumulation_certificate
    ).parameters) == ())
    delegated = URM.relational_accumulation_certificate()
    check(delegated == certificate and delegated is not certificate)

    role = URM().roles()["GRAVITY"]
    check("passes the finite ARGER Gate" in role)
    check("PASS_FINITE_DISCRETE_GFT_Z1_L4_L12" in role)
    check("construction through L12 completes the evidence obligation" in role)
    check("INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT" in role)
    check("conditional dynamical-z=1 theorem is supplementary" in role)

    print(f"RELATIONAL_ACCUMULATION_GATE: PASS ({passed} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
