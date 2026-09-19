#!/usr/bin/env python3
"""Fail-closed validator for the domain-alpha ALLOW/REQUIRE/SELECT surface."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
import hashlib
import inspect
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import MappingProxyType
from unittest import mock

import alpha_role as alpha
from project_model import URM


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
passed = 0


def check(condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError("alpha-role validation failed")
    passed += 1


def refused(callable_object) -> bool:
    try:
        callable_object()
    except alpha.AlphaRoleRefusal:
        return True
    return False


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


def copy_custody_root(destination: Path) -> None:
    for pin in alpha._TEXT_ARTIFACTS:
        target = destination.joinpath(*Path(pin.path).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / pin.path, target)


def main() -> int:
    check(alpha.SCHEMA == "WAC_ALPHA_ALLOW_REQUIRE_SELECT_CERTIFICATE_V003")
    check(alpha.ROLE_ID == "A-AL2")
    check(alpha.CLAIM_CLASS.endswith("DOMAIN_SELECTION_OPEN"))
    check(alpha.OFFICIAL_DISPOSITION.endswith("FULL_UNIVERSE_ALPHA_CARDINALITY_OPEN"))
    check(tuple(inspect.signature(alpha.alpha_role).parameters) == ())
    check(tuple(inspect.signature(alpha.alpha_role_certificate).parameters) == ())
    check(type_error(lambda: alpha.alpha_role({})))
    check(type_error(lambda: alpha.alpha_role_certificate(value="1/137")))
    check(refused(lambda: alpha._root_path("../outside")))
    check(refused(lambda: alpha._root_path("/absolute")))
    check(refused(lambda: alpha._root_path("")))

    evidence = alpha._verify_evidence()
    check(tuple(evidence) == tuple(pin.label for pin in alpha._TEXT_ARTIFACTS))
    check(len(evidence) == len(alpha._TEXT_ARTIFACTS) == 7)
    for pin in alpha._TEXT_ARTIFACTS:
        path = alpha._root_path(pin.path)
        check(path.is_file() and not path.is_symlink())
        check(hashlib.sha256(path.read_bytes()).hexdigest() == pin.sha256)
        check(all(marker in evidence[pin.label] for marker in pin.required_markers))

    handle = alpha.alpha_role()
    certificate = handle.certificate()
    second = alpha.alpha_role_certificate()
    check(isinstance(handle, alpha.AlphaRole))
    check(handle.claim_class == alpha.CLAIM_CLASS)
    check(frozen_error(lambda: set_claim_class(handle)))
    check(certificate == second and certificate is not second)
    check(isinstance(certificate, MappingProxyType))
    check(isinstance(certificate["ALLOW"], MappingProxyType))
    check(isinstance(certificate["ALLOW"]["witness_domain_alpha_values"], tuple))
    check(type_error(lambda: mutate(certificate, "schema", "changed")))
    check(type_error(lambda: mutate(certificate["REQUIRE"], "status", "changed")))
    check(tuple(certificate) == (
        "schema",
        "claim_class",
        "role_id",
        "official_disposition",
        "custody",
        "typed_vocabulary",
        "ALLOW",
        "REQUIRE",
        "SELECT",
        "claim_ceilings",
        "executable_scope",
    ))
    check(certificate["schema"] == alpha.SCHEMA)
    check(certificate["claim_class"] == alpha.CLAIM_CLASS)
    check(certificate["role_id"] == "A-AL2")
    check(certificate["official_disposition"] == alpha.OFFICIAL_DISPOSITION)

    custody = certificate["custody"]
    check(custody["artifact_count"] == 7)
    check(tuple(row["label"] for row in custody["artifacts"]) ==
          tuple(pin.label for pin in alpha._TEXT_ARTIFACTS))
    check(tuple(row["path"] for row in custody["artifacts"]) ==
          tuple(pin.path for pin in alpha._TEXT_ARTIFACTS))
    check(tuple(row["sha256"] for row in custody["artifacts"]) ==
          tuple(pin.sha256 for pin in alpha._TEXT_ARTIFACTS))
    check(tuple(row["kind"] for row in custody["artifacts"]).count(
        "AUTHORITATIVE_TEXT"
    ) == 6)
    check(tuple(row["kind"] for row in custody["artifacts"]).count(
        "EXECUTABLE_ALGEBRAIC_WITNESS_REGRESSION"
    ) == 1)

    vocabulary = certificate["typed_vocabulary"]
    check(vocabulary["ALLOW"] == "MEMBERSHIP_IN_DECLARED_DOMAIN_ATTAINABLE_SET")
    check(vocabulary["REQUIRE"] == "DOMAIN_RELATIVE_UNIVERSAL_CONDITION")
    check(vocabulary["SELECT"] == "SEPARATELY_SUPPLIED_DYNAMICAL_ACTUALIZATION_LAW")

    allowed = certificate["ALLOW"]
    check(allowed["status"] ==
          "PROVED_EXACT_ACTIVE_EM_CONSTRUCTION_INTERVAL_AND_NONSINGLETON")
    check(allowed["domain"] == "FINITE_ACTIVE_EM_TOY_RECORD_WORLDS")
    interval = allowed["construction_scoped_interval"]
    check(isinstance(interval, MappingProxyType))
    check(interval["status"] ==
          "PROVED_EXACT_ANALYTIC_FOR_DECLARED_IDEAL_ACTIVE_EM_PACKET")
    check(interval["set"] ==
          "I_chi intersect ((-ln(1-delta))/(4*pi*B^2), infinity)")
    check(interval["conditions"] ==
          "B^2>0; 0<=delta<1; asserted alpha lies in I_chi")
    check(interval["zero_floor_specialization"] == "I_chi intersect (0, infinity)")
    check(interval["read_contrast"] == "1-exp(-4*pi*alpha*B^2)")
    check(interval["optional_mean_energy_upper_bound"] ==
          "alpha<=E_max/(4*pi*hbar*omega*B^2)")
    check(interval["complete_universe_interval_proved"] is False)
    check(interval["gft_majority_gate"] is False)
    check(allowed["cardinality_lower_bound"] == 2)
    check(allowed["witness_domain_alpha_values"] == ("9/(400*pi)", "9/(100*pi)"))
    check(allowed["witness_read_contrasts"] == ("1/2", "15/16"))
    check(allowed["fixed_controls"] is True)
    check(allowed["alpha_vertex_load_bearing"] is True)
    check(allowed["algebraic_witness_regression_checks"] == 41)
    check(allowed["algebraic_witness_regression_proves_physical_premises"] is False)
    check(allowed["complete_universe_nonsingleton_proved"] is False)

    required = certificate["REQUIRE"]
    check(required["status"] ==
          "PROVED_EXACT_CONDITIONAL_GOVERNING_DOMAIN_ALPHA_REQUIREMENT")
    check(required["governing_domain_precondition"] ==
          "GOVERNING_DOMAIN_ANCESTRY_AND_ALPHA_VALUE_INDEPENDENTLY_ESTABLISHED")
    check(required["record_precondition"] == "ACTVIS_AND_SAI1_THROUGH_SAI8")
    check(required["conclusion"] ==
          "REQUIRE_GOVERNING_DOMAIN_ALPHA_AND_UNIQUE_RG_MATCHING_TRAJECTORY")
    check(required["physical_interpretation"] ==
          "CONSTITUTIVE_DOMAIN_IDENTITY")
    check(required["domain_alpha_value_source"] ==
          "INDEPENDENT_MEASUREMENT_OR_DECLARED_GOVERNING_DOMAIN_DATA")
    check(required["private_same_sector_alpha_allowed"] is False)
    check(required["different_alpha_within_same_governing_domain_allowed"] is False)
    check(required["changing_alpha_defines_different_domain_structure"] is True)
    check(required["governing_domain_value_derived_by_requirement"] is False)
    check(required["governing_domain_ancestry_derived_by_certificate"] is False)

    selected = certificate["SELECT"]
    check(selected["status"] == "OPEN")
    check(selected["governing_domain_selector_supplied"] is False)
    check(selected["numerical_value_selector_supplied"] is False)
    check(selected["realized_occupancy_is_selection_proof"] is False)
    check(selected["complete_universe_singleton_requirement"] == "OPEN")

    ceilings = certificate["claim_ceilings"]
    check(set(ceilings) == {
        "numerical_one_over_137_derived",
        "parameter_free_alpha_prediction",
        "complete_universe_alpha_interval",
        "cavity_half_contrast_is_gravity_gate",
        "governing_domain_ancestry_from_bare_recordhood",
        "governing_domain_emergence",
        "alpha_required_for_every_actvis_record_in_governing_domain",
        "alpha_required_without_established_domain_ancestry",
        "gravity_emergence",
        "einstein_gravity",
        "numerical_G",
    })
    check(ceilings["alpha_required_for_every_actvis_record_in_governing_domain"] is True)
    check(not any(
        value for key, value in ceilings.items()
        if key != "alpha_required_for_every_actvis_record_in_governing_domain"
    ))
    check(certificate["executable_scope"]["caller_arguments"] == 0)
    check(certificate["executable_scope"]["empirical_fit_performed"] is False)
    check(certificate["executable_scope"]["new_physics_calculated"] is False)
    check(certificate["executable_scope"][
        "documentary_theorem_and_audit_regression_only"
    ] is True)

    witness = subprocess.run(
        [
            sys.executable,
            str(ROOT / "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001" /
                "verify_alpha_sector_inheritance.py"),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    check(witness.returncode == 0)
    check("SUMMARY 41/41 exact checks passed" in witness.stdout)
    check("SCOPE algebraic examples and a small DAG/cut only" in witness.stdout)

    public_names = {name for name in dir(URM) if name.startswith("alpha_role")}
    check(public_names == {"alpha_role", "alpha_role_certificate"})
    check(tuple(inspect.signature(URM.alpha_role).parameters) == ())
    check(tuple(inspect.signature(URM.alpha_role_certificate).parameters) == ())
    check(type_error(lambda: URM.alpha_role(True)))
    check(type_error(lambda: URM.alpha_role_certificate(packet={})))
    delegated = URM.alpha_role()
    delegated_certificate = URM.alpha_role_certificate()
    check(isinstance(delegated, alpha.AlphaRole))
    check(delegated_certificate == certificate and delegated_certificate is not certificate)

    project_source = (HERE / "project_model.py").read_text(encoding="utf-8")
    check("return alpha_role()" in project_source)
    check("return alpha_role_certificate()" in project_source)
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
    check("validate_alpha_role.py" in validate_source)
    check(bool(overall_assignments))
    check(any(
        isinstance(node, ast.Name) and node.id == "alpha_role_ok"
        for node in ast.walk(overall_assignments[-1].value)
    ))

    with mock.patch.object(alpha, "_sha256_bytes", return_value="0" * 64):
        check(refused(alpha.alpha_role_certificate))

    with tempfile.TemporaryDirectory(prefix="wac-alpha-role-") as temporary:
        temporary_root = Path(temporary)
        copy_custody_root(temporary_root)
        with mock.patch.object(alpha, "_REPOSITORY_ROOT", temporary_root):
            check(alpha.alpha_role_certificate() == certificate)

            theorem = temporary_root / alpha._TEXT_ARTIFACTS[0].path
            theorem.write_text(theorem.read_text(encoding="utf-8") + "mutation\n",
                               encoding="utf-8")
            check(refused(alpha.alpha_role_certificate))
            shutil.copy2(ROOT / alpha._TEXT_ARTIFACTS[0].path, theorem)

            result = temporary_root / alpha._TEXT_ARTIFACTS[1].path
            result.unlink()
            check(refused(alpha.alpha_role_certificate))
            shutil.copy2(ROOT / alpha._TEXT_ARTIFACTS[1].path, result)

            audit_pin = next(
                pin for pin in alpha._TEXT_ARTIFACTS
                if pin.label == "sector_inheritance_audit"
            )
            audit = temporary_root / audit_pin.path
            audit.unlink()
            audit.symlink_to(ROOT / audit_pin.path)
            check(refused(alpha.alpha_role_certificate))

    with tempfile.TemporaryDirectory(prefix="wac-alpha-parser-") as temporary:
        parser_root = Path(temporary)
        marker_path = parser_root / "marker.md"
        marker_path.write_text("safe text\n", encoding="utf-8")
        marker_pin = alpha._TextPin(
            "marker",
            "marker.md",
            hashlib.sha256(marker_path.read_bytes()).hexdigest(),
            ("required marker",),
        )
        with mock.patch.object(alpha, "_REPOSITORY_ROOT", parser_root):
            check(refused(lambda: alpha._load_text(marker_pin)))

        cr_path = parser_root / "cr.md"
        cr_path.write_bytes(b"bad\r\n")
        cr_pin = alpha._TextPin(
            "cr", "cr.md", hashlib.sha256(cr_path.read_bytes()).hexdigest(), ()
        )
        with mock.patch.object(alpha, "_REPOSITORY_ROOT", parser_root):
            check(refused(lambda: alpha._load_text(cr_pin)))

        binary_path = parser_root / "binary.md"
        binary_path.write_bytes(b"\xff")
        binary_pin = alpha._TextPin(
            "binary",
            "binary.md",
            hashlib.sha256(binary_path.read_bytes()).hexdigest(),
            (),
        )
        with mock.patch.object(alpha, "_REPOSITORY_ROOT", parser_root):
            check(refused(lambda: alpha._load_text(binary_pin)))

    print(f"ALPHA_ROLE: PASS ({passed} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
