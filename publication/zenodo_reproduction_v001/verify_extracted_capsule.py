#!/usr/bin/env python3
"""Verify the archive-local L4--L12 proof and reproduction surface.

Run this only against an extracted capsule root. It performs no network, Git,
cloud, deployment, or numerical-physics action.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree
import zipfile


LINK_LABEL_RE = re.compile(r"!?\[[^\]\n]*\]\(")
NAVIGATION_DOCUMENTS = (
    "README.md",
    "UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md",
    "UNIVERSAL_NETWORK_THEORY_MAJOR_PROOF_INDEX.md",
)
ARGER_EVIDENCE_TOOL = "DEVELOPMENT_R_ARGER_GATE_V001/arger_gate.py"
ARGER_ADOPTION = "ARGER_GATE_ADOPTION_2026-09-16.md"
ALPHA_WITNESS = (
    "alpha/LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/"
    "verify_alpha_sector_inheritance.py"
)
UNT_MAJOR_PROOF_INDEX = "UNIVERSAL_NETWORK_THEORY_MAJOR_PROOF_INDEX.md"
UNT_MAJOR_PROOF_DOCX = "UNIVERSAL_NETWORK_THEORY_MAJOR_PROOF_INDEX.docx"
UNT_CLOSURE_THEOREM = "UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md"
UNT_CLOSURE_DOCX = "UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.docx"
URM_CURRENT_REPORT = "urm/URM_VALIDATION_CURRENT_2026-09-16.md"
ZENODO_ABSTRACT_START = "Universal Network Theory (UNT) fundamentally redefines"
ZENODO_ABSTRACT_END = "\n**Terminology and notation.**"
ZENODO_ABSTRACT_LINKS = (
    (
        "[Intelition Project](https://intelition.org/)",
        "Intelition Project",
        "https://intelition.org/",
    ),
    (
        "['Intelition' changes everything: AI is no longer a tool you invoke]"
        "(https://venturebeat.com/technology/"
        "intelition-changes-everything-ai-is-no-longer-a-tool-you-invoke)",
        "'Intelition' changes everything: AI is no longer a tool you invoke",
        "https://venturebeat.com/technology/"
        "intelition-changes-everything-ai-is-no-longer-a-tool-you-invoke",
    ),
)
CORE_PROOF_HASHES = {
    "UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md": (
        "efc31a92968a30788e64a43395b712942abd9f531c3b77014736bc89b9330308"
    ),
    "ARGER_GATE_ADOPTION_2026-09-16.md": (
        "d58da69f67cef53f54582fc4006c106df55b0456733f970f18162f3401dad1e0"
    ),
    "DEVELOPMENT_R_ARGER_GATE_V001/arger_gate.py": (
        "a5f536b0ea69f24e426216a3c31c97469cdcc850a56e382c2601caa41cf49bd2"
    ),
    "L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md": (
        "2439e1c36a053fccd57155a858d666f9ecbe0e46ded0a79f3ec3b86cb473f5cc"
    ),
    "AUDIT_L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md": (
        "d2404e7503117b3fbdd97220824f2155b45b2cc5b7f2c8e577d86abeb00d6ffd"
    ),
    "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/analyze_centerline.py": (
        "07daf92a84b563fbae1f288528baa71021fe8911953759e91b5f7d68444d2077"
    ),
    "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/AUDIT_EXACT_RESPONSE_SUMRULE_BOUND.md": (
        "0b0967ce7c01045c333497969a4931e599717dc385e590951b279f77a0eda4b1"
    ),
    "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/AUDIT_Z1_PRIMARY_PROOF_PATH_2026-09-16.md": (
        "2f556b2bacba57955b436674d3c1050fa78891ba5a1da69bebf277ce3e45fe4d"
    ),
    "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/EXACT_RESPONSE_SUMRULE_BOUND.md": (
        "5734cda284e85ae0b51ff60b85664f470a407c95daf91b47835963539398e2f8"
    ),
    "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/CONDITIONAL_Z1_BRIDGE_THEOREM.md": (
        "6353aafed694f2598fb72384bc44e2c1e5bada50262ded73919896141b2ce645"
    ),
    "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/AUDIT_FINAL_SURFACE_BOUNDARY_2026-09-16.md": (
        "865e64647cc51b28d750e896459a58fbbce7deed699643282f4ee0569ae43ab0"
    ),
    "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/AUDIT_LL_PREMISE_2026-09-16.md": (
        "88a4f4f848cfc626b899ee83a2d23aaf1665cdac67d108f755f83e2b51b5c278"
    ),
    "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/AUDIT_INTERNAL_Z1_THEOREM_ROUTE_2026-09-16.md": (
        "c6554327b694c33518614d7c725addde664ae74f21638b13bd9c73cb1072a567"
    ),
    "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/INTERNAL_Z1_THEOREM_ROUTE.md": (
        "e85af161082335559a9cc29c4b06090e13f2e403ca69932500bcfd1658b68b2b"
    ),
    "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/README.md": (
        "f7b0d99b644e402c58b2d522b4c47f78e3584048591cd2aa4e01a8e5db00c33d"
    ),
}
LINEAGE_DIAGNOSTIC = "evidence/STRICT_COMMON_LINEAGE_PROGRESSION_V001.json"
LINEAGE_DIAGNOSTIC_SHA256 = (
    "7076440b3c36eae95df8a276ce9494d5c8e0d82715e00e9f790b961278d2e35a"
)
LOWER_LADDER_STDOUT = "L08: 0.0244800482\nL10: 0.0687369678\n"
PROOF_PACKET_CLOSURE_SPEC = "inventory/PROOF_PACKET_LAYOUT_CLOSURE_SPEC.json"
PROOF_PACKET_CLOSURE_VERIFIER = "tools/proof_packet_layout_closure.py"
PROOF_PACKET_MEMBER_COUNT = 58
PROOF_PACKET_PORTABLE_EXPECTED = {
    "alpha_allow_require_scope_repair_v001": (
        "PASS_MECHANICAL__SEMANTIC_HOSTILE_READ_REQUIRED",
        300,
    ),
    "l04_intrinsic_admission_final_hostile_v001": (
        "PASS_FINAL_HOSTILE_INTRINSIC_ADMISSION_L4",
        50,
    ),
    "l12_prefix_lineage_final_audit_v001": (
        "PASS_HOSTILE_SCREEN__EXACT_L12_REPRESENTATION_ONLY__"
        "L12_HISTORY_AWAITS_BENCHMARK",
        40,
    ),
}
PROOF_PACKET_INVENTORY_ONLY = "l04_l10_streamed_preflight_inventory_v001"
URM_CLOSURE_SPEC = "inventory/URM_VALIDATOR_DEPENDENCY_CLOSURE.json"
URM_CLOSURE_VERIFIER = "tools/verify_urm_validator_dependency_closure.py"
URM_PUBLIC_FILE_COUNT = 68
URM_PUBLIC_BYTE_COUNT = 163810488
URM_EXACT_VALIDATORS = (
    (
        "validate_relational_accumulation.py",
        "RELATIONAL_ACCUMULATION_GATE: PASS (176 checks)",
    ),
)
LICENSE_FILES = (
    "LICENSE.txt",
    "LICENSES/Apache-2.0.txt",
    "LICENSES/CC-BY-4.0.txt",
)


class ExtractedCapsuleError(RuntimeError):
    """An extracted capsule did not satisfy its review contract."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_json(path: Path) -> dict:
    def reject_constant(value: str) -> None:
        raise ExtractedCapsuleError(f"non-standard JSON constant in {path}: {value}")

    try:
        value = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ExtractedCapsuleError(f"cannot load JSON {path}: {error}") from error
    if not isinstance(value, dict):
        raise ExtractedCapsuleError(f"JSON root is not an object: {path}")
    return value


def verify_core_proof_path(root: Path) -> tuple[int, str, str]:
    """Authenticate the sealed proof bytes and rerun the native block evidence."""

    for relative, expected in CORE_PROOF_HASHES.items():
        _require_file_hash(root / relative, expected, relative)

    adoption_path = root / ARGER_ADOPTION
    try:
        adoption = adoption_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ExtractedCapsuleError(f"cannot read ARGER adoption record: {error}") from error
    required_markers = (
        "adopts **ARGER Gate 1 (`ARGER-GATE-1`)** as the governing",
        "finite GFT `z=1` verdict is therefore adopted and established",
    )
    missing = [marker for marker in required_markers if marker not in adoption]
    if missing:
        raise ExtractedCapsuleError(
            f"ARGER adoption record is missing required marker(s): {missing}"
        )

    tool_path = root / ARGER_EVIDENCE_TOOL
    if not tool_path.is_file():
        raise ExtractedCapsuleError("native ARGER evidence tool is absent")
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-B", str(tool_path)],
        cwd=root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise ExtractedCapsuleError(
            "native ARGER evidence reconstruction failed: "
            f"returncode={completed.returncode}; stderr={completed.stderr!r}"
        )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise ExtractedCapsuleError(
            f"native ARGER evidence output is not JSON: {error}"
        ) from error
    record_block = result.get("record_block", {})
    gate = result.get("gate", {})
    expected = {
        "status": "PASS__ADOPTED_GOVERNING_FINITE_Z1_ARGER_GATE",
        "l12_majority_margin": "0.06956498393327842",
        "minimum_R_low": "0.4280947078156539",
        "minimum_w_star": "0.5",
    }
    observed = {
        "status": result.get("status"),
        "l12_majority_margin": record_block.get("l12_majority_margin"),
        "minimum_R_low": record_block.get("minimum_R_low"),
        "minimum_w_star": record_block.get("minimum_w_star"),
    }
    if observed != expected:
        raise ExtractedCapsuleError(
            f"native ARGER evidence values changed: {observed!r}"
        )
    if (
        record_block.get("all_sizes_majority") is not True
        or record_block.get("all_sectors_positive_finite_visibility") is not True
        or gate.get("id") != "ARGER-GATE-1"
        or gate.get("name") != "ARGER Gate 1"
        or gate.get("membership") != "PASS"
        or gate.get("majority") != "PASS"
        or gate.get("visibility") != "PASS"
        or gate.get("finite_gft_z1") != "PASS"
    ):
        raise ExtractedCapsuleError("native ARGER evidence predicates changed")
    masses = record_block.get("masses_by_L")
    if not isinstance(masses, dict) or masses.get("12") != "0.56956498393327842":
        raise ExtractedCapsuleError("native ARGER L12 block mass changed")
    return len(CORE_PROOF_HASHES), masses["12"], expected["minimum_R_low"]


def _require_file_hash(path: Path, expected: object, label: str) -> None:
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ExtractedCapsuleError(f"invalid expected hash for {label}")
    if not path.is_file():
        raise ExtractedCapsuleError(f"authenticated closure file is absent: {label}")
    actual = _sha256(path)
    if actual != expected:
        raise ExtractedCapsuleError(
            f"authenticated closure file changed: {label} expected={expected} actual={actual}"
        )


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _markdown_link_targets(text: str):
    """Yield Markdown link destinations, including balanced URL parentheses."""

    position = 0
    while True:
        match = LINK_LABEL_RE.search(text, position)
        if match is None:
            return
        target_start = match.end()
        cursor = target_start
        depth = 1
        while cursor < len(text):
            character = text[cursor]
            if character == "\\" and cursor + 1 < len(text):
                cursor += 2
                continue
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    yield text[target_start:cursor]
                    position = cursor + 1
                    break
            cursor += 1
        else:
            return


def _docx_hyperlink_targets(path: Path) -> set[str]:
    """Read all hyperlink relationship targets from a Word document."""

    relationship_path = "word/_rels/document.xml.rels"
    try:
        with zipfile.ZipFile(path) as archive:
            relationships = ElementTree.fromstring(archive.read(relationship_path))
    except (KeyError, OSError, zipfile.BadZipFile, ElementTree.ParseError) as exc:
        raise ExtractedCapsuleError(
            f"cannot inspect Word hyperlink relationships: {path.name}: {exc}"
        ) from exc
    return {
        relationship.attrib["Target"]
        for relationship in relationships
        if relationship.attrib.get("Type", "").endswith("/hyperlink")
        and "Target" in relationship.attrib
    }


def verify_navigation(root: Path) -> int:
    checked = 0
    for archive_path in NAVIGATION_DOCUMENTS:
        document = root / archive_path
        if not document.is_file():
            raise ExtractedCapsuleError(f"navigation document absent: {archive_path}")
        text = document.read_text(encoding="utf-8")
        for raw_target in _markdown_link_targets(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            relative = Path(unquote(parsed.path))
            if relative.is_absolute():
                raise ExtractedCapsuleError(
                    f"absolute internal link in {archive_path}: {raw_target}"
                )
            resolved = (document.parent / relative).resolve()
            if not _inside(root, resolved):
                raise ExtractedCapsuleError(
                    f"internal link escapes capsule in {archive_path}: {raw_target}"
                )
            if not resolved.is_file():
                raise ExtractedCapsuleError(
                    f"broken internal link in {archive_path}: {raw_target}"
                )
            checked += 1
    return checked


def verify_unt_major_proof_index_and_current_status(root: Path) -> tuple[int, int]:
    """Check the completed-proof catalogue and its qualified current URM report."""

    index_path = root / UNT_MAJOR_PROOF_INDEX
    docx_path = root / UNT_MAJOR_PROOF_DOCX
    theorem_path = root / UNT_CLOSURE_THEOREM
    theorem_docx_path = root / UNT_CLOSURE_DOCX
    report_path = root / URM_CURRENT_REPORT
    if (
        not index_path.is_file()
        or not docx_path.is_file()
        or not theorem_path.is_file()
        or not theorem_docx_path.is_file()
        or not report_path.is_file()
    ):
        raise ExtractedCapsuleError(
            "Universal Network Theory Closure Theorem, Major Proof Index "
            "(Markdown and DOCX), or current URM report is absent"
        )
    for label, publication_docx in (
        ("Closure Theorem", theorem_docx_path),
        ("Major Proof Index", docx_path),
    ):
        if (
            publication_docx.stat().st_size == 0
            or publication_docx.read_bytes()[:4] != b"PK\x03\x04"
        ):
            raise ExtractedCapsuleError(
                f"Universal Network Theory {label} DOCX is not a valid "
                "non-empty Office Open XML publication artifact"
            )
    index_text = index_path.read_text(encoding="utf-8")
    markdown_targets = set(_markdown_link_targets(index_text))
    word_targets = _docx_hyperlink_targets(docx_path)
    missing_word_targets = sorted(markdown_targets - word_targets)
    if missing_word_targets:
        raise ExtractedCapsuleError(
            "Major Proof Index Word hyperlinks differ from Markdown: "
            f"{missing_word_targets}"
        )
    theorem = theorem_path.read_text(encoding="utf-8")
    required_theorem_markers = (
        "**Theorem ID:** `UNT-CLOSURE-V001`",
        "**Theorem `UNT-CLOSURE`.**",
        "finite GFT `z=1` classification",
        "conditional macroscopic gravitational response",
        "QED.",
    )
    missing_theorem = [
        marker for marker in required_theorem_markers if marker not in theorem
    ]
    if missing_theorem:
        raise ExtractedCapsuleError(
            f"Universal Network Theory Closure Theorem is incomplete: {missing_theorem}"
        )
    index = index_path.read_text(encoding="utf-8")
    required_results = {
        "unt_closure": "| Universal Network Theory closure |",
        "l4_intrinsic_admission": "| RFT bounded result — `L = 4` intrinsic admission |",
        "record_laws": "| The Record Laws |",
        "alpha_allow_require": "| Alpha `ALLOW`/`REQUIRE` |",
        "finite_gravity_formation": "| Finite Gravity Formation |",
        "infrared_response": "| Conditional infrared response |",
        "finite_relational_accumulation": "| Finite relational accumulation |",
        "foundational_record_closure": "| Foundational record closure |",
    }
    missing_results = [
        result
        for result, marker in required_results.items()
        if marker not in index
    ]
    required_index_markers = (
        "**capsule executable**",
        "**capsule documentary**",
        "**Git-only**",
        "Target route and the separately implemented",
        "`1156` declared",
        "repository-exact relational dependency closure contains 68 files",
        "complete audited workspace is approximately 59 GB",
        "reconstruction set contains 86 files",
        "full T-51/C-93 design",
        "The two series are complementary measures",
        "ACTVIS(r,W) => REQUIRE_W^sameU1(r, alpha_W(chi)).",
        "authenticates the specific finite evidence required by the ARGER Gate.",
        "The scientific chains pass.",
        "zero-weight historical replay inputs.",
    )
    missing_markers = [marker for marker in required_index_markers if marker not in index]
    if missing_results or missing_markers:
        raise ExtractedCapsuleError(
            "Universal Network Theory Major Proof Index is incomplete: "
            f"results={missing_results} markers={missing_markers}"
        )

    report = report_path.read_text(encoding="utf-8")
    required_report_markers = (
        "T-54 families: `176/176` PASS",
        "current scientific proof surfaces pass their focused validators",
        "Physical-alpha role: `121/121` PASS",
        "Generated proof gate: PASS across `89` claim blocks and `120` distinct cited",
        "Both contracts explicitly carry zero scientific",
        "does not represent a completely green replay",
    )
    missing_report = [marker for marker in required_report_markers if marker not in report]
    if re.search(
        r"Result: exit `1` after `[0-9]+(?:\.[0-9]+)? s`"
        r"(?: reported by the validator)?",
        report,
    ) is None:
        missing_report.append("qualified aggregate exit/duration")
    if missing_report:
        raise ExtractedCapsuleError(
            f"current URM report is missing qualified-status markers: {missing_report}"
        )

    forbidden_unclosed_validators = (
        "urm/model/validate_urm.py",
        "urm/model/validate_alpha_role.py",
        "urm/model/validate_gravity_formation_theory.py",
        "urm/model/validate_gravity_microscopic_progress.py",
    )
    leaked = [path for path in forbidden_unclosed_validators if (root / path).exists()]
    if leaked:
        raise ExtractedCapsuleError(
            f"unclosed validators were packaged as archive-local executables: {leaked}"
        )
    return len(required_results), len(required_report_markers) + 1


def verify_alpha_witness(root: Path) -> int:
    """Run the self-contained alpha algebraic witness/DAG regression."""

    script = root / ALPHA_WITNESS
    if not script.is_file():
        raise ExtractedCapsuleError("self-contained alpha algebraic witness is absent")
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-B", str(script)],
        cwd=script.parent,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    expected_summary = "SUMMARY 41/41 exact checks passed"
    expected_verdict = (
        "VERDICT ALPHA_INHERITANCE_AND_ACTIVE_EM_ALGEBRAIC_WITNESSES_PASS"
    )
    if (
        completed.returncode != 0
        or expected_summary not in completed.stdout
        or expected_verdict not in completed.stdout
    ):
        raise ExtractedCapsuleError(
            "self-contained alpha algebraic witness failed: "
            f"returncode={completed.returncode}; stdout={completed.stdout!r}; "
            f"stderr={completed.stderr!r}"
        )
    return 41


def verify_lower_ladder_reproduction(root: Path) -> tuple[int, str]:
    """Authenticate and execute the original-layout L08/L10 cache closure."""

    tool_path = root / "tools" / "lower_ladder_closure.py"
    if not tool_path.is_file():
        raise ExtractedCapsuleError("lower-ladder closure verifier is absent")
    module_name = "capsule_lower_ladder_closure"
    try:
        spec = importlib.util.spec_from_file_location(module_name, tool_path)
        if spec is None or spec.loader is None:
            raise ExtractedCapsuleError("cannot create lower-ladder verifier import spec")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        result = module.verify_archive(root, sys.executable)
    except ExtractedCapsuleError:
        raise
    except Exception as error:
        raise ExtractedCapsuleError(
            f"lower-ladder extracted reproduction failed: {type(error).__name__}: {error}"
        ) from error
    finally:
        sys.modules.pop(module_name, None)
    if not isinstance(result, dict) or result.get("status") != "VERIFIED_EXTRACTED_LOWER_LADDER":
        raise ExtractedCapsuleError("lower-ladder verifier returned an invalid status")
    if result.get("member_count") != 34:
        raise ExtractedCapsuleError("lower-ladder closure member census changed")
    if result.get("stdout") != LOWER_LADDER_STDOUT:
        raise ExtractedCapsuleError("lower-ladder exact numerical stdout changed")
    return int(result["member_count"]), str(result["stdout"])


def verify_proof_packet_layout_closure(root: Path) -> tuple[int, int, int]:
    """Authenticate four isolated layouts and execute only portable gates."""

    tool_path = root / PROOF_PACKET_CLOSURE_VERIFIER
    spec_path = root / PROOF_PACKET_CLOSURE_SPEC
    if not tool_path.is_file() or not spec_path.is_file():
        raise ExtractedCapsuleError(
            "proof-packet layout closure tool or inventory is absent"
        )
    module_name = "capsule_proof_packet_layout_closure"
    try:
        module_spec = importlib.util.spec_from_file_location(module_name, tool_path)
        if module_spec is None or module_spec.loader is None:
            raise ExtractedCapsuleError(
                "cannot create proof-packet layout verifier import spec"
            )
        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_name] = module
        module_spec.loader.exec_module(module)
        result = module.verify_archive(root, spec_path, run_portable=True)
    except ExtractedCapsuleError:
        raise
    except Exception as error:
        raise ExtractedCapsuleError(
            "proof-packet extracted verification failed: "
            f"{type(error).__name__}: {error}"
        ) from error
    finally:
        sys.modules.pop(module_name, None)

    if (
        not isinstance(result, dict)
        or result.get("status")
        != "VERIFIED_EXTRACTED_PROOF_PACKET_LAYOUT_AND_PORTABLE_GATES"
        or result.get("member_count") != PROOF_PACKET_MEMBER_COUNT
    ):
        raise ExtractedCapsuleError(
            "proof-packet layout verifier returned an invalid status or census"
        )
    executions = result.get("executed_portable_packets")
    if not isinstance(executions, list):
        raise ExtractedCapsuleError("proof-packet execution results are absent")
    by_id = {
        row.get("id"): row
        for row in executions
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    if set(by_id) != set(PROOF_PACKET_PORTABLE_EXPECTED):
        raise ExtractedCapsuleError("proof-packet portable gate set changed")
    for packet_id, (verdict, checks) in PROOF_PACKET_PORTABLE_EXPECTED.items():
        row = by_id[packet_id]
        if (
            row.get("verdict") != verdict
            or row.get("checks_passed") != checks
            or row.get("checks_total") != checks
        ):
            raise ExtractedCapsuleError(
                f"proof-packet portable gate changed: {packet_id}"
            )
    if result.get("inventory_only_packets") != [PROOF_PACKET_INVENTORY_ONLY]:
        raise ExtractedCapsuleError(
            "environment-dependent streamed preflight inventory classification changed"
        )
    return PROOF_PACKET_MEMBER_COUNT, len(by_id), 1


def verify_lineage_diagnostic(root: Path) -> str:
    """Authenticate the compact, non-governing finite-lineage progression."""

    path = root / LINEAGE_DIAGNOSTIC
    _require_file_hash(path, LINEAGE_DIAGNOSTIC_SHA256, LINEAGE_DIAGNOSTIC)
    value = _load_json(path)
    expected_values = {
        "L08": "0.0244800482",
        "L10": "0.0687369678",
        "L12_target": "0.11570852222694002",
        "L12_hostile": "0.11570852222694036",
        "L12_conservative": "0.11570852222694002",
    }
    l12_custody = value.get("source_custody", {}).get("L12_full_workflow", {})
    if (
        value.get("schema") != "STRICT_COMMON_LINEAGE_PROGRESSION_V001"
        or value.get("status") != "PASS__FINITE_COMPUTED_MONOTONIC_PROGRESSION"
        or value.get("measure") != "DECLARED_FINITE_PBAR_Q_COMMON_LINEAGE_SUPPORT"
        or value.get("values") != expected_values
        or value.get("strictly_increasing_through_L12") is not True
        or value.get("capsule_reproduction_scope")
        != (
            "L08_L10_RECOMPUTED__L12_FULL_WORKFLOW_RESULT_AND_CUSTODY_"
            "AUTHENTICATED"
        )
        or l12_custody.get("classification")
        != "FULL_WORKFLOW_COMPUTED__CAPSULE_RESULT_AND_CUSTODY_AUTHENTICATED"
        or l12_custody.get("derivation_sha256")
        != "44be4abb4ba473444915aa2e9cea28d155c0e5645a93ced3664599da8ea865b0"
        or l12_custody.get("sealed_report_sha256")
        != "182a78f3ef11c72d5089a488e85cb9f91e842f1950d3d5a474f7678bfd23ca08"
        or l12_custody.get("verifier_sha256")
        != "03ccd623f3fd441ae3e5732d1fce66184976319b2749a7c6dd7c41e208bbef32"
        or l12_custody.get("review_rerun_status")
        != "PASS__BYTE_IDENTICAL_TO_SEALED_REPORT"
        or l12_custody.get("minimum_runnable_input_files") != 86
        or l12_custody.get("minimum_runnable_input_bytes") != 13485786130
        or l12_custody.get("minimum_runnable_input_gib") != "12.559617"
        or l12_custody.get("audited_workspace_approx_gib") != "58.8"
        or value.get("governing_block_gate_premise") is not False
        or value.get("claim_boundary")
        != "FINITE_DECLARED_EXTRACTION__NO_FIT_NO_FORECAST_NO_ALL_L_CONTINUATION"
    ):
        raise ExtractedCapsuleError("strict common-lineage diagnostic changed")
    return expected_values["L12_conservative"]


def verify_urm_validator_closure(root: Path) -> tuple[int, int, int]:
    """Verify exact dependency bytes and run the focused relational validator.

    Optional provenance dependencies and platform-specific runtime bundles are
    absent by policy. Governing scientific claims are also checked independently
    by the core proof path.
    """

    tool_path = root / URM_CLOSURE_VERIFIER
    spec_path = root / URM_CLOSURE_SPEC
    if not tool_path.is_file() or not spec_path.is_file():
        raise ExtractedCapsuleError("URM validator closure tool or inventory is absent")
    module_name = "capsule_urm_validator_dependency_closure"
    try:
        module_spec = importlib.util.spec_from_file_location(module_name, tool_path)
        if module_spec is None or module_spec.loader is None:
            raise ExtractedCapsuleError("cannot create URM closure verifier import spec")
        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_name] = module
        module_spec.loader.exec_module(module)
        closure = module.load_and_validate_spec(spec_path)
        count, total = module.verify_root(closure, root, "archive-public")
    except ExtractedCapsuleError:
        raise
    except Exception as error:
        raise ExtractedCapsuleError(
            f"URM public closure verification failed: {type(error).__name__}: {error}"
        ) from error
    finally:
        sys.modules.pop(module_name, None)
    if (count, total) != (URM_PUBLIC_FILE_COUNT, URM_PUBLIC_BYTE_COUNT):
        raise ExtractedCapsuleError(
            f"URM public closure census changed: files={count} bytes={total}"
        )

    model_root = root / "urm" / "model"
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    passed = 0
    for script_name, expected_stdout in URM_EXACT_VALIDATORS:
        script = model_root / script_name
        if not script.is_file():
            raise ExtractedCapsuleError(f"packaged URM validator is absent: {script_name}")
        completed = subprocess.run(
            [sys.executable, "-B", script_name],
            cwd=model_root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0 or completed.stdout.strip() != expected_stdout:
            raise ExtractedCapsuleError(
                f"packaged URM validator failed: {script_name}; "
                f"returncode={completed.returncode}; stdout={completed.stdout!r}; "
                f"stderr={completed.stderr!r}"
            )
        passed += 1
    return count, total, passed


def verify_release_licensing(root: Path) -> tuple[int, int]:
    """Verify the file-scoped dual-license declaration and complete texts."""

    for relative in LICENSE_FILES:
        if not (root / relative).is_file():
            raise ExtractedCapsuleError(f"release license file is absent: {relative}")

    notice = (root / "LICENSE.txt").read_text(encoding="utf-8")
    apache = (root / "LICENSES/Apache-2.0.txt").read_text(encoding="utf-8")
    content = (root / "LICENSES/CC-BY-4.0.txt").read_text(encoding="utf-8")
    cff = (root / "CITATION.cff").read_text(encoding="utf-8")
    metadata = _load_json(root / "zenodo_metadata.json")
    build = _load_json(root / "CAPSULE_BUILD.json")
    index = (root / UNT_MAJOR_PROOF_INDEX).read_text(encoding="utf-8")
    abstract_start = index.find(ZENODO_ABSTRACT_START)
    abstract_end = index.find(ZENODO_ABSTRACT_END, abstract_start)
    if abstract_start < 0 or abstract_end < 0:
        raise ExtractedCapsuleError(
            "Major Proof Index no longer has the declared Zenodo abstract boundary"
        )
    expected_description = index[abstract_start:abstract_end].rstrip()
    for markdown_link, _label, _url in ZENODO_ABSTRACT_LINKS:
        if markdown_link not in expected_description:
            raise ExtractedCapsuleError(
                "Major Proof Index no longer contains a declared Zenodo abstract link"
            )
    expected_description_links = [
        {"text": label, "url": url}
        for _markdown_link, label, url in ZENODO_ABSTRACT_LINKS
    ]

    creators = metadata.get("creators")
    if (
        "https://orcid.org/0009-0009-2874-0768" not in cff
        or not isinstance(creators, list)
        or not creators
        or not isinstance(creators[0], dict)
        or creators[0].get("name") != "Mulconrey, Brian"
        or creators[0].get("orcid") != "0009-0009-2874-0768"
    ):
        raise ExtractedCapsuleError("release authorship or ORCID changed")

    notice_markers = (
        "SPDX: Apache-2.0",
        "SPDX: CC-BY-4.0",
        "Third-party components",
    )
    if any(marker not in notice for marker in notice_markers):
        raise ExtractedCapsuleError("release licensing notice changed")
    if "Apache License\n                           Version 2.0" not in apache:
        raise ExtractedCapsuleError("Apache-2.0 license text changed")
    if "Creative Commons Attribution 4.0 International Public License" not in content:
        raise ExtractedCapsuleError("CC-BY-4.0 license text changed")
    licenses = metadata.get("licenses")
    expected_ids = (
        ["Apache-2.0", "CC-BY-4.0"]
        if build.get("release_mode") is True
        else ["@@SOFTWARE_LICENSE_SPDX@@", "@@CONTENT_LICENSE_SPDX@@"]
    )
    if (
        metadata.get("_purpose")
        != "Human-readable checklist for a manual Zenodo deposit; not a direct API payload."
        or metadata.get("title") != "Universal Network Theory"
        or metadata.get("upload_type") != "publication"
        or metadata.get("publication_type") != "preprint"
        or metadata.get("description") != expected_description
        or metadata.get("description_links") != expected_description_links
        or not isinstance(licenses, list)
        or [item.get("id") for item in licenses if isinstance(item, dict)]
        != expected_ids
        or "license" in metadata
    ):
        raise ExtractedCapsuleError("Zenodo publication checklist changed")
    if build.get("release_mode") is True:
        if (
            'license: "Apache-2.0"' not in cff
            or "Software is licensed under Apache-2.0" not in cff
            or "licensed under CC-BY-4.0" not in cff
            or 'preferred-citation:\n  type: article\n  title: "Universal Network Theory"'
            not in cff
            or "  status: preprint" not in cff
        ):
            raise ExtractedCapsuleError("CITATION.cff license declaration changed")
    elif (
        'license: "@@SOFTWARE_LICENSE_SPDX@@"' not in cff
        or "@@CONTENT_LICENSE_SPDX@@" not in cff
    ):
        raise ExtractedCapsuleError("prepublication CITATION.cff license template changed")
    return len(LICENSE_FILES), len(licenses)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="extracted capsule root (defaults to the parent of tools/)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    links = verify_navigation(root)
    proof_results, urm_status_markers = verify_unt_major_proof_index_and_current_status(root)
    core_hashes, block_mass, minimum_visibility = verify_core_proof_path(root)
    alpha_checks = verify_alpha_witness(root)
    lineage_l12 = verify_lineage_diagnostic(root)
    urm_files, urm_bytes, urm_validators = verify_urm_validator_closure(root)
    lower_ladder_members, lower_ladder_stdout = verify_lower_ladder_reproduction(root)
    proof_members, proof_portable, proof_inventory = (
        verify_proof_packet_layout_closure(root)
    )
    license_files, zenodo_rights = verify_release_licensing(root)
    print(lower_ladder_stdout, end="")
    print(
        "EXTRACTED_CAPSULE_OK "
        f"internal_links={links} core_proof_hashes={core_hashes} "
        f"completed_proof_results={proof_results} "
        f"urm_status_markers={urm_status_markers} "
        f"arger_l12_block_mass={block_mass} "
        f"arger_minimum_visibility={minimum_visibility} "
        "arger_gate=ADOPTED_FINITE_BLOCK_Z1 "
        f"urm_closure_files={urm_files} urm_closure_bytes={urm_bytes} "
        f"urm_exact_validators={urm_validators} "
        f"alpha_algebraic_checks={alpha_checks} "
        f"lower_ladder_members={lower_ladder_members} "
        f"proof_packet_members={proof_members} "
        f"proof_portable_gates={proof_portable} "
        f"proof_inventory_only={proof_inventory} "
        f"license_files={license_files} zenodo_rights={zenodo_rights} "
        f"strict_lineage_l12={lineage_l12}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(
            f"EXTRACTED_CAPSULE_FAILURE type={type(error).__name__} message={error}",
            file=sys.stderr,
        )
        raise SystemExit(2)
