"""Zero-input URM certificate for authenticated finite relational accumulation.

This module authenticates the compact L12 adjudication chain and the adopted
ARGER Gate. The Gate classifies the
complete A009--A016 record block at the five authenticated finite sizes from
the pure native Hamiltonian/probe evidence path.

The authenticated construction through L12 completes the finite GFT ``z=1``
Gate classification returned here. Same-model dynamical ``z=1`` is a separately typed
supplementary theorem under the explicit LL-P premise.  The L14 scout is closed
as ``INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT``.  This module does not rerun
the numerical physics, accept caller data, or supply the separately typed
infrared-response theorem or a numerical derivation of G.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
from types import MappingProxyType
from typing import Any, Mapping, NoReturn


SCHEMA = "WAC_RELATIONAL_ACCUMULATION_CERTIFICATE_V004"
CLAIM_CLASS = (
    "AUTHENTICATED_FINITE_RELATIONAL_ACCUMULATION_THROUGH_L12__"
    "GOVERNING_ARGER_GATE_PASS__L14_INCOMPLETE_PRESERVED__"
    "STRICT_NO_PROMOTION_CEILINGS"
)
L14_STATUS = "INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT"
ARGER_GATE_ID = "ARGER-GATE"
ARGER_GATE_NAME = "ARGER Gate"
ARCHIVAL_ARGER_GATE_ID = "ARGER-GATE-1"
ARCHIVAL_ARGER_GATE_NAME = "ARGER Gate 1"
FINITE_Z1_STANDARD = "FINITE_DISCRETE_GFT_Z1__ARGER_GATE_V001"
ARGER_GATE_ADOPTION = "USER_ADOPTED_GOVERNING_2026-09-16"

EXCLUDED_PROMOTIONS = (
    "EXACT_OR_ASYMPTOTIC_DYNAMIC_Z1",
    "PREMISE_FREE_ALL_L_DYNAMIC_Z1",
    "UNIVERSAL_ALL_L_RECORD_BLOCK",
    "CONTINUUM_OR_EINSTEIN_GRAVITY",
    "EMPIRICAL_GRAVITATIONAL_LAW",
    "NEW_METRIC_OR_SPACETIME_DERIVATION_FROM_THIS_GATE",
    "NEW_WARD_OR_RGRL_DERIVATION_FROM_THIS_GATE",
    "UNIVERSAL_COUPLING_FROM_THIS_GATE",
    "NEWTON_G",
)

_REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

_PROGRESSION_SOURCE_PATH = (
    "DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/"
    "extract_lower_bound_progression.py"
)
_PROGRESSION_SOURCE_SHA256 = (
    "9f60224cc131a04616528f60a268fd228813ddfe6f86b468d5a25840021aa11e"
)
_PROGRESSION_INPUT_PINS = (
    (
        _PROGRESSION_SOURCE_PATH,
        _PROGRESSION_SOURCE_SHA256,
    ),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "CACHE_PAYLOADS_V012/L8/CACHE_MANIFEST.json",
        "d33ea5911dacf8c33aebe9f88f85d5ea8db754221fee5f80d4c2d440009e5ade",
    ),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "WORKSPACES/L8/sharp/prefix_07/q_04.npy",
        "c8fbb818c5005285c156e39be8ad10798e68db88b204f6c9b093f5ced44bb4ff",
    ),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "WORKSPACES/L8/sharp/prefix_07/q_05.npy",
        "e8d29e2ca8562dded4aad93096c1dedb6e8cc4dceaf8371e1b2d14b66225b688",
    ),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "WORKSPACES/L8/sharp/prefix_07/q_06.npy",
        "424aa29da3d574a8d537c5205d936baf5c371699c20277fa5799939801d11382",
    ),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "WORKSPACES/L8/sharp/prefix_07/q_07.npy",
        "0d4471d7dc7c7a62cc325ded89d7c5cd5c6799326ba93ecce1fcd0be3ae48588",
    ),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "CACHE_PAYLOADS_V012/L10/CACHE_MANIFEST.json",
        "80f52efaa4b455c7d68f4abef4b413a65c5a81633ec25f30c87fbbb4f2b3e743",
    ),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "WORKSPACES/L10/sharp/prefix_09/q_04.npy",
        "7b6e968c19f7e8b8e2571fb27c5eb86a50bc6e8cb7214b88d809ffdd9eb7abb9",
    ),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "WORKSPACES/L10/sharp/prefix_09/q_05.npy",
        "a7e73852921ee0d166d788535c13fe2eba4bbad5e38d2b0e22894781314c6172",
    ),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "WORKSPACES/L10/sharp/prefix_09/q_06.npy",
        "bc4ceb2ec2299c41f7e0bc355f4e3e6bf3d1937c4218501e9b1468029b9182ee",
    ),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "WORKSPACES/L10/sharp/prefix_09/q_07.npy",
        "16baf3e6843003ae247a8d882273646cbaf91c65e18379f3c3e5d92b0cf75e18",
    ),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "WORKSPACES/L10/sharp/prefix_09/q_08.npy",
        "b6f13e471c840ec3fde9d1e6920d27b51b67173b93dc0b46370c083a67405cae",
    ),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "WORKSPACES/L10/sharp/prefix_09/q_09.npy",
        "b89691d68e67ea20b2390625fa7415a243bd3c4f2e17db439f554fa4603a4d73",
    ),
)
_LOWER_BOUND_PROGRESSION = (
    ("L08", 0.0244800482, "AUTHENTICATED_TARGET_CACHE_DIAGNOSTIC"),
    ("L10", 0.0687369678, "AUTHENTICATED_TARGET_CACHE_DIAGNOSTIC"),
    (
        "L12_TARGET",
        0.11570852222694002,
        "FULL_WORKFLOW_AUTHENTICATED_TARGET_RECONSTRUCTION",
    ),
    (
        "L12_HOSTILE",
        0.11570852222694036,
        "FULL_WORKFLOW_INDEPENDENT_HOSTILE_RECONSTRUCTION",
    ),
    (
        "L12_CONSERVATIVE",
        0.11570852222694002,
        "FULL_WORKFLOW_SEPARATE_FINITE_DIAGNOSTIC",
    ),
)

_RECORD_BLOCK_ATOMS = tuple(f"A{index:03d}" for index in range(9, 17))
_RECORD_BLOCK_INTERVAL = ((7, 48), (13, 48))
_RECORD_BLOCK_Q_BY_L = (
    (4, (1, 2)),
    (6, (2, 3)),
    (8, (2, 3, 4)),
    (10, (3, 4, 5)),
    (12, (4, 5, 6)),
)
_RECORD_BLOCK_MASS_BY_L = (
    (4, "0.7260206189754993"),
    (6, "0.5846615608350367"),
    (8, "0.7373965730354166"),
    (10, "0.6500987927669427"),
    (12, "0.56956498393327842"),
)
_FINITE_VISIBILITY_UNIQUE_SECTORS = 13
_FINITE_VISIBILITY_MINIMUM_R_LOW = "0.4280947078156539"


@dataclass(frozen=True)
class _ArtifactPin:
    label: str
    path: str
    sha256: str
    required_fields: tuple[tuple[str, Any], ...]


@dataclass(frozen=True)
class _TextArtifactPin:
    label: str
    path: str
    sha256: str
    required_markers: tuple[str, ...]


_ARTIFACTS = (
    _ArtifactPin(
        "exact_l12",
        "AUDIT_R_L12_NUMERICAL_REPAIR_V003/EXACT_ADJUDICATION_V003R1.json",
        "cf5fcd1b30793a57970cde8bf31008cfcb2a2b9337d94dbc2f18aef862e777c1",
        (),
    ),
    _ArtifactPin(
        "manifest",
        (
            "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003/"
            "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003R1.json"
        ),
        "292124df4e1d349827753145ce1dd4be32e073db6d657f30737227edd488184a",
        (("schema", "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001"),),
    ),
    _ArtifactPin(
        "strict_progression",
        (
            "DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/"
            "STRICT_COMMON_LINEAGE_PROGRESSION_V001.json"
        ),
        "7076440b3c36eae95df8a276ce9494d5c8e0d82715e00e9f790b961278d2e35a",
        (
            ("schema", "STRICT_COMMON_LINEAGE_PROGRESSION_V001"),
            ("status", "PASS__FINITE_COMPUTED_MONOTONIC_PROGRESSION"),
        ),
    ),
)

_GOVERNING_ARTIFACTS = _ARTIFACTS

_TEXT_ARTIFACTS = (
    _TextArtifactPin(
        "arger_gate_adoption",
        "ARGER_GATE_ADOPTION_2026-09-16.md",
        "d58da69f67cef53f54582fc4006c106df55b0456733f970f18162f3401dad1e0",
        (
            "The project adopts **ARGER Gate 1 (`ARGER-GATE-1`)** as the governing",
            "A passing envelope realizes the UNT **finite GFT `z=1` standard**",
        ),
    ),
    _TextArtifactPin(
        "arger_gate_verifier",
        "DEVELOPMENT_R_ARGER_GATE_V001/arger_gate.py",
        "a5f536b0ea69f24e426216a3c31c97469cdcc850a56e382c2601caa41cf49bd2",
        (
            "The verifier consumes the pure Hamiltonian/probe evidence path",
            '"name": "ARGER Gate 1"',
            '"status": "PASS__ADOPTED_GOVERNING_FINITE_Z1_ARGER_GATE"',
        ),
    ),
    _TextArtifactPin(
        "record_block_theorem",
        "L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md",
        "2439e1c36a053fccd57155a858d666f9ecbe0e46ded0a79f3ec3b86cb473f5cc",
        (
            "# L4--L12 extendible record-envelope theorem",
            "All five authenticated numerical sums exceed `0.50`",
        ),
    ),
    _TextArtifactPin(
        "record_block_theorem_audit",
        "AUDIT_L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md",
        "d2404e7503117b3fbdd97220824f2155b45b2cc5b7f2c8e577d86abeb00d6ffd",
        (
            "Disposition: `PASS`",
            "2439e1c36a053fccd57155a858d666f9ecbe0e46ded0a79f3ec3b86cb473f5cc",
        ),
    ),
    _TextArtifactPin(
        "finite_z1_analyzer",
        (
            "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/"
            "analyze_centerline.py"
        ),
        "07daf92a84b563fbae1f288528baa71021fe8911953759e91b5f7d68444d2077",
        (
            '"schema": "Z1_NATIVE_FINITE_EVIDENCE_V001"',
            '"minimum_R_low"',
        ),
    ),
    _TextArtifactPin(
        "finite_z1_audit",
        (
            "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/"
            "AUDIT_Z1_PRIMARY_PROOF_PATH_2026-09-16.md"
        ),
        "2f556b2bacba57955b436674d3c1050fa78891ba5a1da69bebf277ce3e45fe4d",
        (
            "Verdict: **PASS**",
            "minimum observed\n`R_low` is `0.4280947078156539`",
        ),
    ),
    _TextArtifactPin(
        "conditional_dynamic_z1",
        (
            "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/"
            "CONDITIONAL_Z1_BRIDGE_THEOREM.md"
        ),
        "6353aafed694f2598fb72384bc44e2c1e5bada50262ded73919896141b2ce645",
        ("LL-P", "conditional physical z=1"),
    ),
    _TextArtifactPin(
        "conditional_dynamic_z1_audit",
        (
            "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/"
            "AUDIT_LL_PREMISE_2026-09-16.md"
        ),
        "88a4f4f848cfc626b899ee83a2d23aaf1665cdac67d108f755f83e2b51b5c278",
        (
            "Status: `PASS__CONDITIONAL_EXTERNAL_PHYSICS_PREMISE_VERIFIED`",
            "conditional z=1",
        ),
    ),
    _TextArtifactPin(
        "historical_internal_z1_route",
        (
            "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/"
            "INTERNAL_Z1_THEOREM_ROUTE.md"
        ),
        "e85af161082335559a9cc29c4b06090e13f2e403ca69932500bcfd1658b68b2b",
        ("probe-visible all-L z=1 response:   OPEN",),
    ),
)


class RelationalAccumulationRefusal(RuntimeError):
    """A pinned relational artifact or closed status predicate failed."""


def _refuse(message: str) -> NoReturn:
    raise RelationalAccumulationRefusal(
        "RELATIONAL ACCUMULATION REFUSES: " + message
    )


def _root_path(relative: str) -> Path:
    posix = PurePosixPath(relative)
    if posix.is_absolute() or not posix.parts or ".." in posix.parts:
        _refuse(f"unsafe custody path: {relative}")
    path = _REPOSITORY_ROOT.joinpath(*posix.parts)
    try:
        path.relative_to(_REPOSITORY_ROOT)
    except ValueError:
        _refuse(f"custody path escapes repository: {relative}")
    return path


def _load_json(pin: _ArtifactPin) -> dict[str, Any]:
    path = _root_path(pin.path)
    try:
        if not path.is_file() or path.is_symlink():
            _refuse(f"custody object is absent, non-file, or symlinked: {pin.path}")
        raw = path.read_bytes()
    except OSError as exc:
        _refuse(f"custody object is unreadable: {pin.path}: {exc}")
    if hashlib.sha256(raw).hexdigest() != pin.sha256:
        _refuse(f"SHA-256 mismatch: {pin.path}")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _refuse(f"custody object is not canonical readable JSON: {pin.path}: {exc}")
    if not isinstance(value, dict):
        _refuse(f"custody object must contain a JSON object: {pin.path}")
    for field, expected in pin.required_fields:
        if value.get(field) != expected:
            _refuse(f"unexpected {field} in {pin.path}")
    return value


def _load_decimal_json(pin: _ArtifactPin) -> dict[str, Any]:
    path = _root_path(pin.path)
    try:
        if not path.is_file() or path.is_symlink():
            _refuse(f"custody object is absent, non-file, or symlinked: {pin.path}")
        raw = path.read_bytes()
    except OSError as exc:
        _refuse(f"custody object is unreadable: {pin.path}: {exc}")
    if hashlib.sha256(raw).hexdigest() != pin.sha256:
        _refuse(f"SHA-256 mismatch: {pin.path}")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            parse_float=Decimal,
            parse_int=int,
            parse_constant=lambda token: _refuse(
                f"non-finite JSON token {token} in {pin.path}"
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _refuse(f"custody object is not canonical readable JSON: {pin.path}: {exc}")
    if not isinstance(value, dict):
        _refuse(f"custody object must contain a JSON object: {pin.path}")
    return value


def _load_text(pin: _TextArtifactPin) -> str:
    path = _root_path(pin.path)
    try:
        if not path.is_file() or path.is_symlink():
            _refuse(f"custody object is absent, non-file, or symlinked: {pin.path}")
        raw = path.read_bytes()
    except OSError as exc:
        _refuse(f"custody object is unreadable: {pin.path}: {exc}")
    if hashlib.sha256(raw).hexdigest() != pin.sha256:
        _refuse(f"SHA-256 mismatch: {pin.path}")
    try:
        value = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        _refuse(f"custody object is not UTF-8 text: {pin.path}: {exc}")
    for marker in pin.required_markers:
        if marker not in value:
            _refuse(f"required marker is absent from {pin.path}: {marker}")
    return value


def _verify_progression_source() -> tuple[str, str]:
    """Authenticate and replay the finite L08/L10 cache extraction."""
    for relative, expected_digest in _PROGRESSION_INPUT_PINS:
        path = _root_path(relative)
        try:
            if not path.is_file() or path.is_symlink():
                _refuse(
                    "progression input is absent, non-file, or symlinked: "
                    f"{relative}"
                )
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            _refuse(f"progression input is unreadable: {relative}: {exc}")
        if digest != expected_digest:
            _refuse(f"progression input SHA-256 mismatch: {relative}")

    try:
        result = subprocess.run(
            [sys.executable, str(_root_path(_PROGRESSION_SOURCE_PATH))],
            cwd=_REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        _refuse(f"progression extraction could not execute: {exc}")
    if result.returncode != 0:
        _refuse(
            "progression extraction failed: "
            + (result.stderr.strip() or f"exit {result.returncode}")
        )
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    expected = ("L08: 0.0244800482", "L10: 0.0687369678")
    if lines != expected:
        _refuse(f"progression extraction output changed: {lines!r}")
    return expected


def _expect(condition: bool, message: str) -> None:
    if not condition:
        _refuse(message)


def _verify_governing_arger_gate(
    pins: Mapping[str, _ArtifactPin],
    text_evidence: Mapping[str, str],
) -> dict[str, Any]:
    """Reconstruct the ARGER Gate directly from its declared native premises."""
    manifest = _load_decimal_json(pins["manifest"])

    _expect(
        "EXACT_STRUCTURAL_THEOREM_PROVED" in
        text_evidence["record_block_theorem"],
        "record-block theorem status changed",
    )
    _expect(
        "Disposition: `PASS`" in text_evidence["record_block_theorem_audit"],
        "record-block theorem audit is not PASS",
    )
    _expect(
        "The project adopts **ARGER Gate 1 (`ARGER-GATE-1`)** as the governing"
        in text_evidence["arger_gate_adoption"],
        "ARGER-GATE-1 adoption marker changed",
    )
    verifier_path = _root_path(
        next(
            pin.path
            for pin in _TEXT_ARTIFACTS
            if pin.label == "arger_gate_verifier"
        )
    )
    try:
        spec = importlib.util.spec_from_file_location(
            "wac_pure_arger_gate", verifier_path
        )
        if spec is None or spec.loader is None:
            _refuse("could not load the pure ARGER Gate verifier")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        pure = module.build_evidence()
    except RelationalAccumulationRefusal:
        raise
    except Exception as exc:
        _refuse(f"pure ARGER Gate verification failed: {exc}")

    _expect(
        isinstance(pure, dict)
        and pure.get("schema") == "WAC_ARGER_GATE_EVIDENCE_V001"
        and pure.get("status") ==
        "PASS__ADOPTED_GOVERNING_FINITE_Z1_ARGER_GATE",
        "pure ARGER Gate verifier did not return its passing evidence schema",
    )
    pure_gate = pure.get("gate", {})
    _expect(
        pure_gate.get("id") == ARCHIVAL_ARGER_GATE_ID
        and pure_gate.get("membership") == "PASS"
        and pure_gate.get("majority") == "PASS"
        and pure_gate.get("visibility") == "PASS"
        and pure_gate.get("finite_gft_z1") == "PASS",
        "archival ARGER-GATE-1 predicate result changed",
    )
    pure_block = pure.get("record_block", {})
    _expect(
        tuple(pure_block.get("atoms", ())) == _RECORD_BLOCK_ATOMS
        and pure_block.get("density_interval") == "[7/48,13/48)",
        "pure record-block identity changed",
    )

    expected_sectors = tuple(
        (length, q)
        for length, charges in _RECORD_BLOCK_Q_BY_L
        for q in charges
    )
    pure_sectors = tuple(
        tuple(row) for row in pure_block.get("unique_sectors", ())
    )
    _expect(
        pure_sectors == expected_sectors
        and len(pure_sectors) == _FINITE_VISIBILITY_UNIQUE_SECTORS,
        "pure 13-sector block identity changed",
    )
    _expect(
        pure_block.get("all_sizes_majority") is True
        and pure_block.get("all_sectors_positive_finite_visibility") is True,
        "pure block majority or finite visibility predicate failed",
    )
    _expect(
        pure_block.get("minimum_R_low") == _FINITE_VISIBILITY_MINIMUM_R_LOW
        and pure_block.get("minimum_w_star") == "0.5",
        "pure finite-visibility minimum changed",
    )

    atoms = {
        row.get("atom_id"): row
        for row in manifest.get("atoms", ())
        if row.get("atom_id") in _RECORD_BLOCK_ATOMS
    }
    _expect(
        tuple(sorted(atoms)) == _RECORD_BLOCK_ATOMS,
        "A009--A016 manifest envelope is incomplete",
    )
    expected_masses = dict(_RECORD_BLOCK_MASS_BY_L)
    pure_masses = pure_block.get("masses_by_L", {})
    size_rows: list[dict[str, Any]] = []

    for length, expected_q in _RECORD_BLOCK_Q_BY_L:
        selected_q = tuple(
            sorted(
                {
                    int(atoms[atom_id]["q_by_L"][str(length)])
                    for atom_id in _RECORD_BLOCK_ATOMS
                }
            )
        )
        _expect(selected_q == expected_q, f"record-block q set changed at L{length}")

        mass = Decimal(str(pure_masses.get(str(length), "NaN")))
        _expect(
            mass == Decimal(expected_masses[length]),
            f"record-block mass changed at L{length}",
        )
        _expect(mass > Decimal("0.50"), f"record-block majority failed at L{length}")
        size_rows.append(
            {
                "L": length,
                "selected_q": selected_q,
                "deduplicated_pbar_mass": expected_masses[length],
                "majority_threshold": "0.50",
                "majority_pass": True,
            }
        )

    _expect(
        "conditional physical z=1" in text_evidence["conditional_dynamic_z1"]
        and "probe-visible all-L z=1 response:   OPEN" in
        text_evidence["historical_internal_z1_route"],
        "conditional theorem or historical-route custody changed",
    )
    return {
        "atoms": _RECORD_BLOCK_ATOMS,
        "density_interval": _RECORD_BLOCK_INTERVAL,
        "sizes": tuple(size_rows),
        "unique_sector_count": len(pure_sectors),
        "minimum_R_low": pure_block["minimum_R_low"],
        "minimum_w_star": pure_block["minimum_w_star"],
        "visibility_evidence_roles": (
            "L4_L8_COMPLETE_FINITE_SECTOR_DIAGONALIZATION",
            "L10_L12_INDEPENDENT_TARGET_BLIND_RECONSTRUCTION",
        ),
        "all_sizes_majority": True,
        "all_selected_sectors_positive_finite_visibility": True,
        "pure_gate_schema": pure["schema"],
        "pure_gate_status": pure["status"],
    }


def _verify_current_base(evidence: Mapping[str, dict[str, Any]]) -> None:
    """Verify the exact L12, manifest, and strict-progression current base."""
    exact = evidence["exact_l12"]
    _expect(exact.get("checks_passed") == exact.get("checks_total") == 1156,
            "exact L12 must retain all 1156 checks")
    _expect(exact.get("failures") == [], "exact L12 reports failures")
    _expect(
        exact.get("maximum_target_hostile_sector_weight_difference")
        == 8.326672684688674e-16
        and exact.get("maximum_target_hostile_terminal_amplitude_difference")
        == 7.946965413254846e-17
        and exact.get("tolerance") == 1e-8,
        "exact L12 numerical agreement changed",
    )

    manifest = evidence["manifest"]
    _expect(len(manifest.get("atoms", ())) == 24, "Stage-5 manifest atom count changed")
    _expect(manifest.get("I_acc") == [[1, 48], [17, 48]],
            "Stage-5 accumulated interval changed")

    progression = evidence["strict_progression"]
    extraction = progression.get("extraction", {})
    _expect(
        extraction.get("path") == _PROGRESSION_SOURCE_PATH
        and extraction.get("sha256") == _PROGRESSION_SOURCE_SHA256
        and tuple(extraction.get("stdout", ())) == (
            "L08: 0.0244800482",
            "L10: 0.0687369678",
        ),
        "strict common-lineage extraction custody changed",
    )
    values = progression.get("values", {})
    expected_values = {
        "L08": "0.0244800482",
        "L10": "0.0687369678",
        "L12_target": "0.11570852222694002",
        "L12_hostile": "0.11570852222694036",
        "L12_conservative": "0.11570852222694002",
    }
    _expect(values == expected_values, "strict common-lineage values changed")
    _expect(
        Decimal(values["L08"]) < Decimal(values["L10"])
        < Decimal(values["L12_conservative"])
        and progression.get("strictly_increasing_through_L12") is True,
        "strict common-lineage progression is not increasing through L12",
    )
    _expect(
        progression.get("governing_block_gate_premise") is False
        and "NO_FIT_NO_FORECAST_NO_ALL_L_CONTINUATION"
        in progression.get("claim_boundary", ""),
        "strict common-lineage diagnostic boundary changed",
    )
    source_custody = progression.get("source_custody", {})
    pinned_progression_inputs = dict(_PROGRESSION_INPUT_PINS)
    expected_l08_shards = {
        f"q_{q:02d}.npy": pinned_progression_inputs[
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            f"WORKSPACES/L8/sharp/prefix_07/q_{q:02d}.npy"
        ]
        for q in range(4, 8)
    }
    expected_l10_shards = {
        f"q_{q:02d}.npy": pinned_progression_inputs[
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            f"WORKSPACES/L10/sharp/prefix_09/q_{q:02d}.npy"
        ]
        for q in range(4, 10)
    }
    l12_custody = source_custody.get("L12_full_workflow", {})
    _expect(
        source_custody.get("L08_cache_manifest_sha256")
        == pinned_progression_inputs[
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            "CACHE_PAYLOADS_V012/L8/CACHE_MANIFEST.json"
        ]
        and source_custody.get("L08_terminal_shard_sha256")
        == expected_l08_shards
        and source_custody.get("L10_cache_manifest_sha256")
        == pinned_progression_inputs[
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            "CACHE_PAYLOADS_V012/L10/CACHE_MANIFEST.json"
        ]
        and source_custody.get("L10_terminal_shard_sha256")
        == expected_l10_shards
        and l12_custody == {
            "classification": (
                "FULL_WORKFLOW_COMPUTED__CAPSULE_RESULT_AND_CUSTODY_"
                "AUTHENTICATED"
            ),
            "derivation_path": (
                "DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/"
                "l12_lineage_resolved_support.py"
            ),
            "derivation_sha256": (
                "44be4abb4ba473444915aa2e9cea28d155c0e5645a93ced3664599da8ea865b0"
            ),
            "sealed_report_path": (
                "DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/"
                "LINEAGE_RESOLVED_SUPPORT_REPORT_V001.json"
            ),
            "sealed_report_sha256": (
                "182a78f3ef11c72d5089a488e85cb9f91e842f1950d3d5a474f7678bfd23ca08"
            ),
            "verifier_path": (
                "DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/"
                "verify_lineage_resolved_support.py"
            ),
            "verifier_sha256": (
                "03ccd623f3fd441ae3e5732d1fce66184976319b2749a7c6dd7c41e208bbef32"
            ),
            "review_rerun_date": "2026-09-18",
            "review_rerun_status": "PASS__BYTE_IDENTICAL_TO_SEALED_REPORT",
            "minimum_runnable_input_files": 86,
            "minimum_runnable_input_bytes": 13485786130,
            "minimum_runnable_input_gib": "12.559617",
            "audited_workspace_approx_gib": "58.8",
            "capsule_scope": (
                "METHOD_RESULT_AND_CRYPTOGRAPHIC_CUSTODY_INCLUDED__"
                "GENERATED_INPUT_ARRAYS_NOT_DUPLICATED"
            ),
        }
        and progression.get("capsule_reproduction_scope")
        == (
            "L08_L10_RECOMPUTED__L12_FULL_WORKFLOW_RESULT_AND_CUSTODY_"
            "AUTHENTICATED"
        ),
        "strict common-lineage L12 custody changed",
    )


def _verify_governing_evidence() -> dict[str, dict[str, Any]]:
    """Verify only evidence that governs the adopted ARGER Gate certificate."""
    _verify_progression_source()
    evidence = {pin.label: _load_json(pin) for pin in _GOVERNING_ARTIFACTS}
    pins = {pin.label: pin for pin in _GOVERNING_ARTIFACTS}
    text_evidence = {pin.label: _load_text(pin) for pin in _TEXT_ARTIFACTS}
    _verify_current_base(evidence)
    evidence["governing_arger_gate"] = _verify_governing_arger_gate(
        pins, text_evidence
    )
    return evidence



def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _governing_certificate(
    evidence: dict[str, dict[str, Any]],
) -> Mapping[str, Any]:
    exact = evidence["exact_l12"]
    manifest = evidence["manifest"]
    progression = evidence["strict_progression"]
    arger_gate = evidence["governing_arger_gate"]

    return _freeze(
        {
            "schema": SCHEMA,
            "claim_class": CLAIM_CLASS,
            "definitions": {
                "intrinsic_admission": (
                    "ALLOW(w,r)=1 iff cell_w=R and target_r=B; the accepted pair "
                    "carries depleted bandwidth and sealed (w,r) lineage, with "
                    "owner-once content transfer"
                ),
                "prefix_support": (
                    "after n fresh admissions, lineage support obeys "
                    "S subset {0,...,n-1}"
                ),
                "lineage": (
                    "the cryptographically retained ancestry coordinate used for "
                    "injective common-ancestry support"
                ),
                "pbar_q": "late-event arithmetic mean of complete q-sector weights",
                "density_atom": (
                    "one half-open density interval with an authenticated q label at "
                    "each declared finite L"
                ),
                "finite_discrete_gft_z1": (
                    "the adopted ARGER Gate classification of one complete "
                    "finite record block; it is not an exact or asymptotic "
                    "dynamical exponent"
                ),
                "dynamic_z1": (
                    "the scaling statement omega(k)=v|k|+o(|k|); in this "
                    "certificate it is conditional on LL-P and supplementary "
                    "to the completed finite Gate classification"
                ),
            },
            "custody": {
                "scope": "GOVERNING_ARGER_GATE_ONLY",
                "artifact_count": (
                    len(_GOVERNING_ARTIFACTS) + len(_TEXT_ARTIFACTS)
                ),
                "artifacts": tuple(
                    {
                        "label": pin.label,
                        "path": pin.path,
                        "sha256": pin.sha256,
                        "kind": "JSON",
                    }
                    for pin in _GOVERNING_ARTIFACTS
                ) + tuple(
                    {
                        "label": pin.label,
                        "path": pin.path,
                        "sha256": pin.sha256,
                        "kind": "TEXT_OR_SOURCE",
                    }
                    for pin in _TEXT_ARTIFACTS
                ),
            },
            "exact_l12": {
                "checks_passed": exact["checks_passed"],
                "checks_total": exact["checks_total"],
                "maximum_sector_weight_difference":
                    exact["maximum_target_hostile_sector_weight_difference"],
                "maximum_terminal_amplitude_difference":
                    exact["maximum_target_hostile_terminal_amplitude_difference"],
                "tolerance": exact["tolerance"],
            },
            "authenticated_manifest": {
                "schema": manifest["schema"],
                "status": manifest["status"],
                "atom_count": len(manifest["atoms"]),
                "accumulated_interval": manifest["I_acc"],
                "finite_sizes": tuple(
                    length for length, _ in _RECORD_BLOCK_Q_BY_L
                ),
            },
            "governing_arger_gate": {
                "gate_id": ARGER_GATE_ID,
                "canonical_name": ARGER_GATE_NAME,
                "archival_implementation_id": ARCHIVAL_ARGER_GATE_ID,
                "archival_implementation_name": ARCHIVAL_ARGER_GATE_NAME,
                "standard": FINITE_Z1_STANDARD,
                "adoption": ARGER_GATE_ADOPTION,
                "governing": True,
                "classified_object": "COMPLETE_A009_A016_BOUNDED_RECORD_BLOCK",
                "atoms": arger_gate["atoms"],
                "density_interval": arger_gate["density_interval"],
                "finite_sizes": tuple(row["L"] for row in arger_gate["sizes"]),
                "sizes": arger_gate["sizes"],
                "predicates": {
                    "bounded_extendible_record_membership": True,
                    "independent_structural_audit": "PASS",
                    "deduplicated_mass_strictly_above_one_half_at_each_size":
                        arger_gate["all_sizes_majority"],
                    "every_selected_sector_positive_finite_visibility":
                        arger_gate[
                            "all_selected_sectors_positive_finite_visibility"
                        ],
                },
                "finite_visibility": {
                    "unique_sector_count": arger_gate["unique_sector_count"],
                    "minimum_R_low": arger_gate["minimum_R_low"],
                    "minimum_w_star": arger_gate["minimum_w_star"],
                    "evidence_roles": arger_gate["visibility_evidence_roles"],
                    "meaning": (
                        "AUTHENTICATED_FINITE_VISIBILITY_PREMISE_"
                        "COMPLETE_THROUGH_L12"
                    ),
                },
                "pure_verifier": {
                    "schema": arger_gate["pure_gate_schema"],
                    "status": arger_gate["pure_gate_status"],
                },
                "decision": "PASS_FINITE_DISCRETE_GFT_Z1_L4_L12",
                "l12_decision": "PASS_FINITE_DISCRETE_GFT_Z1",
                "claim_boundary": (
                    "GOVERNING_ARGER_GATE_FINITE_CLASSIFICATION__NOT_EXACT_OR_"
                    "ASYMPTOTIC_DYNAMIC_Z1__NO_CONTINUUM_OR_EINSTEIN_"
                    "GRAVITY_OR_EMPIRICAL_LAW_OR_NUMERICAL_G_PROMOTION"
                ),
            },
            "gravity_formation_boundary": {
                "finite_discrete_phase":
                    "ESTABLISHED_UNDER_ADOPTED_ARGER_GATE",
                "finite_gate_proof_obligation": "COMPLETE_THROUGH_L12",
                "conditional_rgrl_wtc_infrared_response":
                    "SEPARATE_EXISTING_GFT_LAYER_UNCHANGED",
                "continuum_einstein_or_empirical_gravity_from_this_gate": False,
                "numerical_g_from_this_gate": False,
            },
            "dynamic_z1": {
                "same_model_ll_p": {
                    "status": "CONDITIONAL_PHYSICAL_THEOREM",
                    "premise_id": "LL-P",
                    "density_interval": _RECORD_BLOCK_INTERVAL,
                    "conclusion": (
                        "DYNAMIC_EXPONENT_Z1_AND_NONZERO_THERMODYNAMIC_"
                        "PROBE_VISIBILITY_ON_A009_A016"
                    ),
                    "independent_of_finite_arger_gate_decision": True,
                },
                "relationship_to_finite_gate":
                    "SUPPLEMENTARY_NOT_AN_UNFINISHED_GATE_REQUIREMENT",
                "finite_arger_gate_is_dynamic_exponent_proof": False,
            },
            "strict_common_lineage_progression": {
                "schema": progression["schema"],
                "status": progression["status"],
                "measure": progression["measure"],
                "source_path": _PROGRESSION_SOURCE_PATH,
                "source_sha256": _PROGRESSION_SOURCE_SHA256,
                "verified_inputs": tuple(
                    {"path": path, "sha256": digest}
                    for path, digest in _PROGRESSION_INPUT_PINS
                ),
                "table": tuple(
                    {
                        "scale": label,
                        "support": value,
                        "authority": authority,
                    }
                    for label, value, authority in _LOWER_BOUND_PROGRESSION
                ) + (
                    {
                        "scale": "L14",
                        "support": L14_STATUS,
                        "authority": (
                            "PRESERVED_INCOMPLETE_RUN__NO_L14_VALUE_OR_"
                            "SCIENTIFIC_ADJUDICATION"
                        ),
                    },
                ),
                "strictly_increasing_through_l12": True,
                "capsule_reproduction_scope": progression[
                    "capsule_reproduction_scope"
                ],
                "l12_full_workflow_custody": progression["source_custody"][
                    "L12_full_workflow"
                ],
                "governing_arger_gate_premise": False,
                "fit_performed": False,
                "monotone_continuation_theorem": False,
                "asymptotic_extrapolation_theorem": False,
                "l14_value_inferred": False,
                "claim_boundary": progression["claim_boundary"],
            },
            "relational_l14": {
                "status": L14_STATUS,
                "authenticated_final_report": None,
                "scientific_result": None,
                "l14_value": None,
                "branch_results_complete": False,
                "resumable_from_preservation": False,
                "preserved_rough_events": {
                    "target_v003r6_clean_restart": "1--13_OF_14",
                    "hostile_v003r5": "1--12_OF_14",
                    "superseded_target_v003r5": "1--9_OF_14",
                },
                "preservation": {
                    "target_archive_sha256": (
                        "02cdbd0ce0e6a66bb3a5440d05cb9b9f3686906d491ed5c5857fc5f64d51af22"
                    ),
                    "target_manifest_verified_files": 1109,
                    "hostile_archive_sha256": (
                        "f9042afa8e4d901a0533900129b983ff140dbb2306c3738c0eab9c28c0615d46"
                    ),
                    "hostile_manifest_verified_files": 863,
                    "states_cache_scratch_inflight_preserved": False,
                },
                "closed_scout_protocol": {
                    "governing": False,
                    "phase2_decision": None,
                    "phase3_result": None,
                    "final_gate_decision": None,
                    "status": "CLOSED_WITHOUT_SCIENTIFIC_ADJUDICATION",
                },
                "l14_progression_admission": {
                    "status": L14_STATUS,
                    "admitted": False,
                    "reason": "NO_COMPLETED_TARGET_HOSTILE_RESULTS_OR_FINAL_GATE",
                },
                "scientific_consequence": (
                    "NO_L14_PASS_REJECTION_OR_VALUE__NO_CHANGE_TO_GOVERNING_"
                    "L4_L12_ARGER_GATE"
                ),
            },
            "excluded_promotions": EXCLUDED_PROMOTIONS,
            "executable_scope": {
                "caller_arguments": 0,
                "physics_recalculated": False,
                "external_result_accepted": False,
                "scientific_output": (
                    "PINNED_GOVERNING_FINITE_ARGER_GATE_CERTIFICATE_AND_"
                    "CLOSED_INCOMPLETE_L14_DISPOSITION"
                ),
            },
        }
    )



@dataclass(frozen=True)
class RelationalAccumulation:
    """Immutable handle for the current governing finite ARGER Gate."""

    @property
    def claim_class(self) -> str:
        return CLAIM_CLASS

    def certificate(self) -> Mapping[str, Any]:
        return _governing_certificate(_verify_governing_evidence())



def relational_accumulation() -> RelationalAccumulation:
    """Verify the current ARGER Gate evidence and return its zero-input handle."""
    _verify_governing_evidence()
    return RelationalAccumulation()


def relational_accumulation_certificate() -> Mapping[str, Any]:
    """Return the governing finite relational certificate."""
    return relational_accumulation().certificate()
