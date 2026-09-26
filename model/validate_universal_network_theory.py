#!/usr/bin/env python3
"""Focused fail-closed validator for the top-level UNT typed composition."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
import hashlib
import inspect
from pathlib import Path
import shutil
import tempfile
from types import MappingProxyType
from unittest import mock

from project_model import URM
import universal_network_theory as unt


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
passed = 0


def check(condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError("Universal Network Theory closure validation failed")
    passed += 1


def type_error(callable_object) -> bool:
    try:
        callable_object()
    except TypeError:
        return True
    return False


def refused(callable_object) -> bool:
    try:
        callable_object()
    except unt.UniversalNetworkTheoryRefusal:
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
    check(tuple(inspect.signature(unt.universal_network_theory).parameters) == ())
    check(tuple(inspect.signature(
        unt.universal_network_theory_certificate
    ).parameters) == ())
    check(type_error(lambda: unt.universal_network_theory({})))
    check(type_error(lambda: unt.universal_network_theory_certificate(data={})))

    theorem_path = ROOT / unt.THEOREM_PATH
    check(theorem_path.is_file() and not theorem_path.is_symlink())
    check(hashlib.sha256(theorem_path.read_bytes()).hexdigest() == unt.THEOREM_SHA256)

    handle = unt.universal_network_theory()
    certificate = handle.certificate()
    second = unt.universal_network_theory_certificate()
    check(handle.claim_class == unt.CLAIM_CLASS)
    check(handle.theorem_sha256 == unt.THEOREM_SHA256)
    check(frozen_error(lambda: set_claim_class(handle)))
    check(certificate == second and certificate is not second)
    check(certificate["typed_composition"] is not second["typed_composition"])
    check(isinstance(certificate, MappingProxyType))
    check(isinstance(certificate["typed_composition"], MappingProxyType))
    check(isinstance(
        certificate["typed_composition"]["finite_gravity_formation"]["finite_sizes"],
        tuple,
    ))
    check(type_error(lambda: mutate(certificate, "schema", "changed")))

    check(tuple(certificate) == (
        "schema",
        "theorem_id",
        "claim_class",
        "disposition",
        "custody",
        "typed_composition",
        "type_boundary",
        "claim_ceilings",
        "executable_scope",
    ))
    check(certificate["schema"] == unt.SCHEMA)
    check(certificate["theorem_id"] == unt.THEOREM_ID == "UNT-CLOSURE-V001")
    check(certificate["claim_class"] == unt.CLAIM_CLASS)
    check(certificate["disposition"] == unt.DISPOSITION)
    check(certificate["custody"]["theorem_path"] == unt.THEOREM_PATH)
    check(certificate["custody"]["theorem_sha256"] == unt.THEOREM_SHA256)
    check(certificate["custody"]["component_schemas"] == {
        "universal_record_coverage": unt.udcl.SCHEMA,
        "domain_alpha_requirement": unt.alpha.SCHEMA,
        "finite_gravity_formation": unt.relational.SCHEMA,
        "conditional_gravitational_response": unt.gft.SCHEMA,
    })

    composed = certificate["typed_composition"]
    check(composed["operator"] ==
          "EXACT_TYPED_CONJUNCTION_WITHOUT_PROOF_TYPE_PROMOTION")
    check("domain_alpha_requirement" in composed)
    check("visible_parent_alpha_identity" not in composed)

    coverage = composed["universal_record_coverage"]
    check(coverage["proof_type"] == "EXACT_CONDITIONAL_ON_ADOPTED_UDCL_POSTULATE")
    check(coverage["domain"] == "ACTUAL_BONA_FIDE_FINITE_MISSION_RECORDS")
    check(coverage["conclusion"] ==
          "UDCL_IMPLIES_ALL_DOMAIN_RECORDS_HAVE_COVERAGE_U")
    check(coverage["natural_udcl_validity_established"] is False)

    alpha = composed["domain_alpha_requirement"]
    check(alpha["allow_proof_type"] ==
          "PROVED_EXACT_ACTIVE_EM_CONSTRUCTION_INTERVAL_AND_NONSINGLETON")
    check(alpha["allow_interval"] ==
          "I_chi intersect ((-ln(1-delta))/(4*pi*B^2), infinity)")
    check(alpha["require_proof_type"] ==
          "PROVED_EXACT_CONDITIONAL_GOVERNING_DOMAIN_ALPHA_REQUIREMENT")
    check(alpha["governing_domain_precondition"] ==
          "GOVERNING_DOMAIN_ANCESTRY_AND_ALPHA_VALUE_INDEPENDENTLY_ESTABLISHED")
    check(alpha["record_precondition"] == "ACTVIS_AND_SAI1_THROUGH_SAI8")
    check(alpha["conclusion"] ==
          "REQUIRE_GOVERNING_DOMAIN_ALPHA_AND_UNIQUE_RG_MATCHING_TRAJECTORY")
    check(alpha["select_status"] == "OPEN")

    finite = composed["finite_gravity_formation"]
    check(finite["proof_type"] ==
          "AUTHENTICATED_FINITE_RESULT_UNDER_ADOPTED_ARGER_GATE")
    check(finite["gate_id"] == "ARGER-GATE")
    check(finite["classified_object"] == "COMPLETE_A009_A016_BOUNDED_RECORD_BLOCK")
    check(finite["finite_sizes"] == (4, 6, 8, 10, 12))
    check(finite["unique_selected_sector_count"] == 13)
    check(finite["minimum_R_low"] == "0.4280947078156539")
    check(finite["decision"] == "PASS_FINITE_DISCRETE_GFT_Z1_L4_L12")
    check(finite["finite_gate_proof_obligation"] == "COMPLETE_THROUGH_L12")
    check(finite["continuum_or_einstein_gravity_from_finite_gate"] is False)

    dynamic = composed["conditional_dynamic_z1"]
    check(dynamic["proof_type"] == "CONDITIONAL_PHYSICAL_THEOREM")
    check(dynamic["premise_id"] == "LL-P")
    check(dynamic["density_interval"] == ((7, 48), (13, 48)))
    check(dynamic["independent_of_finite_arger_gate_decision"] is True)

    response = composed["record_conditioned_geometry_and_response"]
    check(response["proof_type"] == "EXACT_CONDITIONAL_WORKING_THEORY_IMPLICATION")
    check(response["rgrl_status"] ==
          "ADOPTED_WORKING_RECORD_GEOMETRY_REALIZATION_POSTULATE")
    check(response["rgrl_clauses"] == ("RGRL-A", "RGRL-B", "RGRL-C"))
    check(response["four_dimensional_record_conditioned_geometry"] ==
          "EXACT_INSIDE_ADOPTED_RGRL_A")
    check(response["complete_local_spatial_metric_deformation_ancestry"] ==
          "EXACT_INSIDE_ADOPTED_RGRL_B_C")
    check(response["metric_deformation_ancestry_kind"] ==
          "OFFSHELL_FORMAL_SPATIAL_METRIC_TANGENT")
    check(response["wtc_premises"] == unt._WTC_PREMISES)
    check(response["response_status"] == "EXACT_AXIOMATIC_WORKING_THEORY_CLOSURE")
    check(response["common_physical_metric"] ==
          "EXACT_UNDER_WTC_H3_SAME_METRIC_IDENTIFICATION_NOT_RGRL_A_ALONE")
    check(response["leading_nonlinear_Einstein_response"] ==
          "EXACT_UNDER_WTC_H3_H4_IN_DECLARED_LOCAL_METRIC_ONLY_TWO_DERIVATIVE_CLASS")
    check(response["nature_obeys_RGRL_established"] is False)
    check(response["parameter_free_numerical_G_derived"] is False)

    boundary = certificate["type_boundary"]
    check(boundary == {
        "finite_arger_and_rgrl_wtc_are_separately_typed": True,
        "finite_arger_gate_discharges_all_rgrl_wtc_premises": False,
        "l12_finite_gate_directly_implies_einstein_equation": False,
        "conditional_response_requires_declared_rgrl_wtc_premises": True,
        "composition_adds_new_physical_premise": False,
        "composition_changes_component_proof_status": False,
    })
    check("governing_domain_or_alpha_selected" in certificate["claim_ceilings"])
    check("visible_parent_or_alpha_selected" not in certificate["claim_ceilings"])
    check(not any(certificate["claim_ceilings"].values()))
    check(certificate["executable_scope"]["caller_arguments"] == 0)
    check(certificate["executable_scope"]["physics_recalculated"] is False)
    check(certificate["executable_scope"]["empirical_test_performed"] is False)
    check(certificate["executable_scope"]
          ["new_deduction_beyond_pinned_typed_composition"] is False)

    theorem_text = unt._load_theorem()
    check("The finite Gate classification and the infrared response theorem are independent" in
          theorem_text)
    check(all(marker in theorem_text for marker in (
        "Coverage-U for whichever admissible actual record is supplied by the parent",
        "every `ACTVIS` record in that typed governing domain.",
        "No implication from a finite ARGER Gate pass to satisfaction of RGRL or",
    )))
    check("under `WTC-H1` through `WTC-H5`" in theorem_text)

    check(tuple(inspect.signature(URM.universal_network_theory).parameters) == ())
    check(tuple(inspect.signature(
        URM.universal_network_theory_certificate
    ).parameters) == ())
    check(type_error(lambda: URM.universal_network_theory(True)))
    check(type_error(lambda: URM.universal_network_theory_certificate(data={})))
    delegated = URM.universal_network_theory()
    delegated_certificate = URM.universal_network_theory_certificate()
    check(isinstance(delegated, unt.UniversalNetworkTheory))
    check(delegated_certificate == certificate and delegated_certificate is not certificate)

    public_names = {
        name for name in dir(URM) if name.startswith("universal_network_theory")
    }
    check(public_names == {
        "universal_network_theory",
        "universal_network_theory_certificate",
    })
    project_source = (HERE / "project_model.py").read_text(encoding="utf-8")
    check("return universal_network_theory()" in project_source)
    check("return universal_network_theory_certificate()" in project_source)

    validate_source = (HERE / "validate_urm.py").read_text(encoding="utf-8")
    tree = ast.parse(validate_source)
    overall_assignments = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "overall"
            for target in node.targets
        )
    ]
    check("validate_universal_network_theory.py" in validate_source)
    check(bool(overall_assignments))
    check(any(
        isinstance(node, ast.Name) and node.id == "universal_network_theory_ok"
        for node in ast.walk(overall_assignments[-1].value)
    ))

    with tempfile.TemporaryDirectory(prefix="wac-unt-theorem-") as temporary:
        temporary_root = Path(temporary)
        copied = temporary_root / unt.THEOREM_PATH
        shutil.copy2(theorem_path, copied)
        with mock.patch.object(unt, "_REPOSITORY_ROOT", temporary_root):
            check(unt._load_theorem() == theorem_text)
            copied.write_text(theorem_text + "\ntampered\n", encoding="utf-8")
            check(refused(unt._load_theorem))

            marker_removed = theorem_text.replace(
                "No implication from a finite ARGER Gate pass to satisfaction of RGRL or",
                "A finite ARGER Gate pass establishes RGRL and WTC",
            )
            copied.write_text(marker_removed, encoding="utf-8")
            replacement_sha256 = hashlib.sha256(copied.read_bytes()).hexdigest()
            with mock.patch.object(unt, "THEOREM_SHA256", replacement_sha256):
                check(refused(unt._load_theorem))

    with mock.patch.object(
        unt.relational,
        "relational_accumulation_certificate",
        side_effect=unt.relational.RelationalAccumulationRefusal("simulated"),
    ):
        check(refused(unt.universal_network_theory_certificate))

    print(f"UNIVERSAL_NETWORK_THEORY_CLOSURE_GATE: PASS ({passed} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
