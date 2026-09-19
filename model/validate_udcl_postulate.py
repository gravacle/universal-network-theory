#!/usr/bin/env python3
"""Thirty-four bounded custody, claim-ceiling, and URM checks for U-DCL."""

from __future__ import annotations

import ast
import hashlib
import inspect
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
from unittest import mock

import udcl_postulate as udp
from project_model import URM


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANE = ROOT / udp.FORMAL_LANE_ID
AXIOMATIC_LANE = ROOT / udp.AXIOMATIC_LANE_ID


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refused(callable_object) -> bool:
    try:
        callable_object()
    except udp.UDCLPostulateRefusal:
        return True
    return False


def type_error(callable_object) -> bool:
    try:
        callable_object()
    except TypeError:
        return True
    return False


def set_item(mapping, key, value) -> None:
    mapping[key] = value


def copy_custody_root(destination: Path) -> None:
    for name in (
        "URFT_UDCL_ADOPTION_V001.md",
        "URFT_UNIVERSAL_DOMAIN_LAW_DECISION_V001.md",
        "URFT_UNIVERSAL_DOMAIN_LAW_DECISION_V001.AUDIT.md",
    ):
        shutil.copy2(ROOT / name, destination / name)
    shutil.copytree(
        ROOT / udp.SEALED_SCOPE_LANE_ID,
        destination / udp.SEALED_SCOPE_LANE_ID,
    )
    shutil.copytree(ROOT / udp.FORMAL_LANE_ID, destination / udp.FORMAL_LANE_ID)
    shutil.copytree(ROOT / udp.AXIOMATIC_LANE_ID, destination / udp.AXIOMATIC_LANE_ID)


def main() -> int:
    checks = 0

    def check(condition: bool) -> None:
        nonlocal checks
        assert condition
        checks += 1

    check(udp.SCHEMA == "WAC_UDCL_WORKING_POSTULATE_CERTIFICATE_V001")  # 1
    check(udp.CLAIM_CLASS.endswith("CONDITIONAL_THEOREM_ONLY"))  # 2
    check(udp.ADOPTION_ID == "URFT-POSTULATE-UDCL-V001")  # 3
    check(
        udp.FORMAL_MANIFEST_SHA256 == digest(LANE / "MANIFEST.sha256")
        and udp.AXIOMATIC_MANIFEST_SHA256
        == digest(AXIOMATIC_LANE / "MANIFEST.sha256")
    )  # 4
    alpha_manifest = ROOT / "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001" / "MANIFEST.sha256"
    alpha_readme_digest = next(
        line.split(maxsplit=1)[0]
        for line in alpha_manifest.read_text(encoding="utf-8").splitlines()
        if line.endswith("  README.md")
    )
    check(
        udp._resolve_declared_manifest_item(
            ROOT,
            alpha_manifest,
            "README.md",
            alpha_readme_digest,
        )
        == alpha_manifest.parent / "README.md"
    )  # 5
    with tempfile.TemporaryDirectory(prefix="wac-udcl-resolver-") as temporary:
        resolver_root = Path(temporary)
        resolver_lane = resolver_root / "LANE"
        resolver_lane.mkdir()
        resolver_manifest = resolver_lane / "MANIFEST.sha256"
        resolver_manifest.write_text("placeholder\n", encoding="utf-8")
        payload = b"same bytes\n"
        expected = hashlib.sha256(payload).hexdigest()
        (resolver_root / "README.md").write_bytes(payload)
        (resolver_lane / "README.md").write_bytes(payload)
        multiple_refused = refused(
            lambda: udp._resolve_declared_manifest_item(
                resolver_root,
                resolver_manifest,
                "README.md",
                expected,
            )
        )
        zero_refused = refused(
            lambda: udp._resolve_declared_manifest_item(
                resolver_root,
                resolver_manifest,
                "README.md",
                "0" * 64,
            )
        )
    check(multiple_refused and zero_refused)  # 6
    check(
        set(udp._ARTIFACT_SHA256) | {"MANIFEST.sha256"} == {p.name for p in LANE.iterdir()}
        and set(udp._AXIOMATIC_ARTIFACT_SHA256) | {"MANIFEST.sha256"}
        == {p.name for p in AXIOMATIC_LANE.iterdir()}
    )  # 7

    custody = udp._verify_custody(ROOT)
    check(
        custody.adoption_sha256 == digest(ROOT / "URFT_UDCL_ADOPTION_V001.md")
        and custody.decision_sha256 == digest(ROOT / "URFT_UNIVERSAL_DOMAIN_LAW_DECISION_V001.md")
        and custody.decision_audit_sha256 == digest(ROOT / "URFT_UNIVERSAL_DOMAIN_LAW_DECISION_V001.AUDIT.md")
        and custody.formal_manifest_sha256 == digest(LANE / "MANIFEST.sha256")
        and custody.formal_audit_sha256 == digest(LANE / "INDEPENDENT_AUDIT.md")
        and custody.formal_verification_sha256 == digest(LANE / "VERIFICATION.txt")
        and custody.axiomatic_manifest_sha256 == digest(AXIOMATIC_LANE / "MANIFEST.sha256")
        and custody.axiomatic_audit_sha256 == digest(AXIOMATIC_LANE / "AUDIT.md")
        and custody.axiomatic_verification_sha256
        == digest(AXIOMATIC_LANE / "VERIFICATION.txt")
    )  # 8
    check(
        len(custody.fresh_verifier_stdout_sha256) == 64
        and len(custody.fresh_axiomatic_verifier_stdout_sha256) == 64
    )  # 9

    result = udp.udcl_postulate()
    check(isinstance(result, udp.UDCLPostulate))  # 8
    check(result.claim_class == udp.CLAIM_CLASS and result.manifest_sha256 == udp.FORMAL_MANIFEST_SHA256)  # 9
    certificate = result.certificate()
    check(certificate["schema"] == udp.SCHEMA and certificate["claim_class"] == udp.CLAIM_CLASS)  # 10
    check(
        certificate["postulate"]["status"] == "ADOPTED_WORKING_PHYSICAL_POSTULATE"
        and certificate["postulate"]["domain"] == "ACTUAL_BONA_FIDE_FINITE_MISSION_RECORDS"
        and certificate["postulate"]["natural_validity"] == "OPEN_AND_FALSIFIABLE"
    )  # 11
    check(
        certificate["exact_results"]["domain_axiom"] == "DOMAIN_MEMBERSHIP_IMPLIES_REC_R"
        and certificate["exact_results"]["local_bridge"] == "DCL_PHYS_R_IMPLIES_C_R_AND_S_R_AND_J_R"
        and certificate["exact_results"]["universal"] == "UDCL_IMPLIES_ALL_DOMAIN_RECORDS_HAVE_COVERAGE_U"
        and certificate["exact_results"]["sound_evidential_bridge"]
        == "CERT_DCL_R_P_WITH_SOUNDNESS_AND_CUSTODY_IMPLIES_DCL_PHYS_R"
        and certificate["exact_results"]["theorem_status"] == "EXACT_CONDITIONAL_ON_ADOPTED_POSTULATE"
        and certificate["exact_results"]["axiomatic_closure"]
        == "UDCL_IMPLIES_UNIVERSAL_COVERAGE_WITH_FULL_TRANSITIVE_PROOF_CUSTODY"
    )  # 12
    check(dict(certificate["program_authorizations"]) == {
        "working_postulate_adopted": True,
        "conditional_universal_coverage_theorem": True,
    })  # 13
    check(
        certificate["scientific_status"]["nature_obeys_UDCL"] == "NOT_ESTABLISHED_BY_THIS_CERTIFICATE"
        and certificate["scientific_status"]["empirical_validation"]
        == "NONE_PERFORMED_BY_THIS_CERTIFICATE"
        and certificate["scientific_status"]["caller_input_scientific_weight"] == "ZERO"
    )  # 14
    check(
        certificate["scientific_status"]["single_success_confirms_universal"] is False
        and certificate["scientific_status"]["finite_success_collection_proves_universal"] is False
        and certificate["scientific_status"]["one_independently_admitted_exception_falsifies"] is True
    )  # 15
    check(certificate["nonconsequences"] and not any(certificate["nonconsequences"].values()))  # 16
    check(certificate["falsifier"] and all(certificate["falsifier"].values()))  # 17
    check(
        certificate["executable_scope"]["postulate_machine_proved"] is False
        and certificate["executable_scope"]["conditional_theorem_machine_proved"] is False
        and certificate["executable_scope"]["documentary_and_finite_logic_regression_only"] is True
        and certificate["executable_scope"]["empirical_test_performed"] is False
        and certificate["executable_scope"]["axiomatic_transitive_closure_checks"]
        == "74/74_REPRODUCED"
    )  # 18

    certificate_again = result.certificate()
    check(certificate_again == certificate and certificate_again is not certificate)  # 19
    check(type_error(lambda: set_item(certificate, "schema", "bad")))  # 20
    check(type_error(lambda: set_item(certificate["nonconsequences"], "gravity_emergence", True)))  # 21
    check(
        tuple(inspect.signature(udp.udcl_postulate).parameters) == ()
        and tuple(inspect.signature(udp.udcl_postulate_certificate).parameters) == ()
    )  # 22
    check(
        type_error(lambda: udp.udcl_postulate(True))
        and type_error(lambda: udp.udcl_postulate_certificate(packet={}))
    )  # 23

    public_names = {name for name in dir(URM) if name.startswith("udcl_postulate")}
    check(public_names == {"udcl_postulate", "udcl_postulate_certificate"})  # 24
    check(
        tuple(inspect.signature(URM.udcl_postulate).parameters) == ()
        and tuple(inspect.signature(URM.udcl_postulate_certificate).parameters) == ()
    )  # 25
    delegated = URM.udcl_postulate()
    check(isinstance(delegated, udp.UDCLPostulate))  # 26
    delegated_certificate = URM.udcl_postulate_certificate()
    check(delegated_certificate == certificate and delegated_certificate is not certificate)  # 27
    check(
        type_error(lambda: URM.udcl_postulate(True))
        and type_error(lambda: URM.udcl_postulate_certificate(packet={}))
    )  # 28

    project_source = (HERE / "project_model.py").read_text(encoding="utf-8")
    check(
        "return udcl_postulate()" in project_source
        and "return udcl_postulate_certificate()" in project_source
    )  # 29
    validate_source = (HERE / "validate_urm.py").read_text(encoding="utf-8")
    tree = ast.parse(validate_source)
    overall_assignments = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "overall" for target in node.targets)
    ]
    check(
        "validate_udcl_postulate.py" in validate_source
        and bool(overall_assignments)
        and any(
            isinstance(node, ast.Name) and node.id == "udcl_postulate_ok"
            for node in ast.walk(overall_assignments[-1].value)
        )
        and "natural validity open" in validate_source
    )  # 30

    refusal_cases = []
    with mock.patch.object(udp, "_sha256_file", return_value="0" * 64):
        refusal_cases.append(refused(udp.udcl_postulate))
    with tempfile.TemporaryDirectory(prefix="wac-udcl-audit-") as temporary:
        temporary_root = Path(temporary)

        symlink_root = temporary_root / "scope-symlink"
        symlink_root.mkdir()
        copy_custody_root(symlink_root)
        scope_audit = symlink_root / udp.SEALED_SCOPE_LANE_ID / "AUDIT.md"
        scope_audit.unlink()
        scope_audit.symlink_to(ROOT / udp.SEALED_SCOPE_LANE_ID / "AUDIT.md")
        refusal_cases.append(refused(lambda: udp._verify_custody(symlink_root)))

        formal_race_root = temporary_root / "formal-race"
        formal_race_root.mkdir()
        copy_custody_root(formal_race_root)

        def alter_formal_after_fresh(lane_root: Path, expected_stdout: str) -> str:
            (lane_root / "BOUNDARY.md").write_text("altered after fresh run\n", encoding="utf-8")
            return hashlib.sha256(expected_stdout.encode("utf-8")).hexdigest()

        with mock.patch.object(udp, "_run_fresh_verifier", side_effect=alter_formal_after_fresh):
            refusal_cases.append(refused(lambda: udp._verify_custody(formal_race_root)))

        scope_race_root = temporary_root / "scope-race"
        scope_race_root.mkdir()
        copy_custody_root(scope_race_root)

        def alter_scope_after_fresh(lane_root: Path, expected_stdout: str) -> str:
            scope_result = scope_race_root / udp.SEALED_SCOPE_LANE_ID / "RESULT.md"
            scope_result.write_text("altered after fresh run\n", encoding="utf-8")
            return hashlib.sha256(expected_stdout.encode("utf-8")).hexdigest()

        with mock.patch.object(udp, "_run_fresh_verifier", side_effect=alter_scope_after_fresh):
            refusal_cases.append(refused(lambda: udp._verify_custody(scope_race_root)))

        axiomatic_tamper_root = temporary_root / "axiomatic-tamper"
        axiomatic_tamper_root.mkdir()
        copy_custody_root(axiomatic_tamper_root)
        (axiomatic_tamper_root / udp.AXIOMATIC_LANE_ID / "RESULT.md").write_text(
            "altered axiomatic result\n", encoding="utf-8"
        )
        refusal_cases.append(refused(lambda: udp._verify_custody(axiomatic_tamper_root)))
    check(all(refusal_cases))  # 31
    bad_result = SimpleNamespace(returncode=0, stdout="different\n", stderr="")
    with mock.patch.object(udp.subprocess, "run", return_value=bad_result):
        check(refused(udp.udcl_postulate))  # 32

    assert checks == 34
    print("UDCL_POSTULATE_URM_CHECKS: 34/34 PASS — NATURAL VALIDITY OPEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
