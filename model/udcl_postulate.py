"""Refusal-safe URM exposure of the adopted U-DCL working postulate.

This module exposes one program decision, its typed conditional theorem, and the
full transitive axiomatic closure packet. It does not test whether nature obeys
U-DCL, infer DCL from recordhood, select an outcome, derive a Born law,
authenticate A5, or derive gravity. No caller input participates in custody or
in the returned scientific status.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
from types import MappingProxyType
from typing import Any, Mapping, NoReturn


SCHEMA = "WAC_UDCL_WORKING_POSTULATE_CERTIFICATE_V001"
CLAIM_CLASS = "ADOPTED_WORKING_POSTULATE_AND_EXACT_CONDITIONAL_THEOREM_ONLY"
ADOPTION_ID = "URFT-POSTULATE-UDCL-V001"
FORMAL_LANE_ID = "LANE_RFT_UDCL_CONDITIONAL_UNIVERSAL_COVERAGE_V001"
SEALED_SCOPE_LANE_ID = "LANE_RFT_STANDARD_CAUSAL_URFT_SCOPE_V001"
AXIOMATIC_LANE_ID = "LANE_RFT_AXIOMATIC_URFT_CLOSURE_V001"

ADOPTION_SHA256 = "3e795b0220fa5d7c722eb3e4516a96a9f8d813455a3edfe6aca1f764c53fb1ba"
DECISION_SHA256 = "e789c06b80afd62f8d177ad74bc1b17a86b4ca391625002c4a9026b9324f0f90"
DECISION_AUDIT_SHA256 = "1d797071a605ceeb90a7e868c45b71fb8c7c1b05161a229a4e24aad934781dd1"
FORMAL_MANIFEST_SHA256 = "3bfe5cf2614ae0df3775e36084afe4870197c425c01f9de0ada83f34a04de1d3"
SEALED_SCOPE_MANIFEST_SHA256 = "3b78db4a739ba48e1ac5d5fb40a449330ee48ae783d907172fae749188b7ff8c"
SEALED_SCOPE_THEOREM_SHA256 = "6630a1c66f1e414b089dbeed2a29a91a78faa7c1ba3eb68702f16f3307f8c36f"
AXIOMATIC_MANIFEST_SHA256 = "5d61df5ce23d1ceb7996b56be108a6ecf268efdc3f939c6462476db2f6cdb94f"

AUDIT_VERDICT = (
    "ACCEPT_AFTER_TYPED_V002_REPAIR_AS_EXACT_CONDITIONAL_THEOREM__"
    "NATURAL_UDCL_VALIDITY_UNPROVED"
)
VERIFIER_TOTAL = "TOTAL 72/72 PASS"
VERIFIER_VERDICT = (
    "VERDICT TYPED_UDCL_CONDITIONAL_UNIVERSAL_COVERAGE_LOGIC_SCOPE_AND_"
    "CUSTODY_PASS__NATURAL_UDCL_VALIDITY_NOT_TESTED"
)
AXIOMATIC_VERIFIER_TOTAL = "TOTAL 74/74 PASS"
AXIOMATIC_VERIFIER_VERDICT = (
    "VERDICT AXIOMATIC_URFT_LOGICAL_CLOSURE_AND_TRANSITIVE_CUSTODY_PASS"
)
AXIOMATIC_AUDIT_VERDICT = (
    "ACCEPT_AXIOMATIC_URFT_CLOSURE_WITH_TWO_LAYER_SCIENTIFIC_STATUS"
)

_ARTIFACT_SHA256 = {
    "README.md": "291942a1b7c94a64775f210908b76a6c4eab040a3ed4035da285e52c8e5399d2",
    "THEOREM.md": "30cdd93998b556306e72ee7cee9ad434e84d2e7e8ddc08a820c01394895ebc32",
    "TYPED_CLARIFICATION_V002.md": (
        "3570f3a2f5851e9620935b235439b67bc3a4c45420d2f2149c8eeeae4f90b34c"
    ),
    "BOUNDARY.md": "8236ac60203d660721c0f555741e7c05177c8d9f05dc3763eb6aa72c6a87ed41",
    "RESULT.md": "b21d1c2938c11aef99874f49c42023cc383100bb5e4ad92203b34d0b1e0b7830",
    "AUDIT.md": "bd81c3270fcd8e29ee6ec230becebdfbc4a9366e943f72180b819b8e908f608c",
    "INDEPENDENT_AUDIT.md": (
        "bbc4b2fffd9a76cb2026ec6988f60d8102cbad5dc6f69cc64bd0924cf1b9c0da"
    ),
    "DEPENDENCIES.sha256": (
        "3529a91a7134e0d5e1620fd1f44988379c22da79fa474c74131ddc0eaa44d1a9"
    ),
    "verify_udcl_conditional_coverage.py": (
        "e85566481b0b03b7848ff4d72e2539d428f051ad0d09b9c3adb6ee40ede55def"
    ),
    "VERIFICATION.txt": (
        "8898c473e3d7755d88c7bc7f12033aa938a39ad4a9ed837d5cd6cecbca7c3b01"
    ),
}

_AXIOMATIC_ARTIFACT_SHA256 = {
    "README.md": "b295481012a646310e8ca2673e86c3a73392065479171e8cad3f2e13b864eae4",
    "THEOREM.md": "0b2374e648b59091d978ee18ef0a99333c327ac81021ae19f1491e90769d1405",
    "DEPENDENCIES.sha256": "26a55e62bd92c8e2fe3a0494d8f11a5958d0259b174ef83ba9b98d0a028a9370",
    "RESULT.md": "86800cb5c016c141c5643fe320301ff9dbb85d3d8ef75e43a1f8d643d69d9b71",
    "AUDIT.md": "0015f375c32181f43af40730624b73d3fad1c8e8bbcf51978c2860f9222276b9",
    "VERIFICATION.txt": "dfe00ce4738dd58fd74a0d744ae2395b28b398b40a08ebc629d46b13edfb8ef9",
    "verify_axiomatic_urft_closure.py": (
        "ac79663cd126b945bc022c95ba094f40addca4e28e3e24312f70ba9d0f15b77d"
    ),
}

_SEALED_SCOPE_ARTIFACTS = frozenset(
    {
        "README.md",
        "THEOREM.md",
        "COUNTEREXAMPLES.md",
        "RESULT.md",
        "AUDIT.md",
        "verify_standard_causal_scope.py",
        "VERIFICATION.txt",
    }
)

_MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})  ([^\r\n]+)$")
_REPOSITORY_ROOT = Path(__file__).absolute().parent.parent


class UDCLPostulateRefusal(RuntimeError):
    """The adopted decision or conditional theorem failed pinned custody."""


def _refuse(message: str) -> NoReturn:
    raise UDCLPostulateRefusal("U-DCL POSTULATE REFUSES: " + message)


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    try:
        return _sha256_bytes(path.read_bytes())
    except OSError as exc:
        _refuse(f"custody object is unreadable: {path.name}: {exc}")


def _strict_text(path: Path, label: str) -> str:
    try:
        payload = path.read_bytes()
        text = payload.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        _refuse(f"{label} is unreadable or not UTF-8: {exc}")
    if "\r" in text or "\x00" in text:
        _refuse(f"{label} contains forbidden carriage-return or NUL bytes")
    return text


def _declared_root_path(root: Path, relative: str, label: str) -> Path:
    """Return one safe repository-relative custody path without following escapes."""
    posix = PurePosixPath(relative)
    if posix.is_absolute() or ".." in posix.parts or not posix.parts:
        _refuse(f"{label} contains an absolute or escaping path: {relative}")
    candidate = root.joinpath(*posix.parts)
    try:
        candidate.resolve(strict=False).relative_to(root.resolve())
    except (OSError, ValueError):
        _refuse(f"{label} escapes the repository: {relative}")
    return candidate


def _resolve_declared_manifest_item(
    root: Path,
    manifest: Path,
    relative: str,
    expected_sha256: str,
) -> Path:
    """Select exactly one digest-matching root or packet-local manifest target.

    Historical manifests contain both repository-rooted paths and packet-local
    bare names.  A root file with the same bare name must not shadow the packet
    artifact.  The row's declared digest is the discriminator; zero or multiple
    distinct matches are refused.
    """
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        _refuse("manifest item has a malformed SHA-256 digest")
    target = PurePosixPath(relative)
    if target.is_absolute() or not target.parts:
        _refuse(f"manifest item contains an absolute or empty path: {relative}")

    root_resolved = root.resolve()
    raw_candidates = []
    if ".." not in target.parts:
        raw_candidates.append(root.joinpath(*target.parts))
    raw_candidates.append(manifest.parent.joinpath(*target.parts))

    candidates: dict[Path, Path] = {}
    for raw_candidate in raw_candidates:
        try:
            resolved = raw_candidate.resolve(strict=False)
            resolved.relative_to(root_resolved)
        except (OSError, ValueError):
            _refuse(f"manifest item escapes the repository: {relative}")
        candidates[resolved] = raw_candidate

    matches = []
    for resolved, raw_candidate in candidates.items():
        if (
            raw_candidate.is_file()
            and not raw_candidate.is_symlink()
            and _sha256_file(raw_candidate) == expected_sha256
        ):
            matches.append(resolved)
    if len(matches) != 1:
        _refuse(
            "manifest item must match exactly one root-or-packet-local candidate: "
            f"{relative}; matches={len(matches)}"
        )
    return matches[0]


def _parse_manifest(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not text.endswith("\n"):
        _refuse("formal-lane manifest is not newline terminated")
    prefix = FORMAL_LANE_ID + "/"
    for line in text.splitlines():
        match = _MANIFEST_LINE.fullmatch(line)
        if match is None:
            _refuse("formal-lane manifest has a malformed row")
        digest, relative = match.groups()
        posix = PurePosixPath(relative)
        if posix.is_absolute() or ".." in posix.parts or not relative.startswith(prefix):
            _refuse("formal-lane manifest contains an escaping path")
        name = relative[len(prefix):]
        if not name or "/" in name or name in rows:
            _refuse("formal-lane manifest contains a nested or duplicate artifact")
        rows[name] = digest
    if rows != _ARTIFACT_SHA256:
        _refuse("formal-lane manifest is not the exact closed ten-artifact inventory")
    return rows


def _parse_scope_manifest(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not text.endswith("\n"):
        _refuse("sealed-scope manifest is not newline terminated")
    for line in text.splitlines():
        match = _MANIFEST_LINE.fullmatch(line)
        if match is None:
            _refuse("sealed-scope manifest has a malformed row")
        digest, relative = match.groups()
        posix = PurePosixPath(relative)
        if posix.is_absolute() or ".." in posix.parts:
            _refuse("sealed-scope manifest contains an escaping path")
        if not relative or "/" in relative or relative in rows:
            _refuse("sealed-scope manifest contains a nested or duplicate artifact")
        rows[relative] = digest
    if set(rows) != _SEALED_SCOPE_ARTIFACTS:
        _refuse("sealed-scope manifest is not the exact closed seven-artifact inventory")
    return rows


def _parse_axiomatic_manifest(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not text.endswith("\n"):
        _refuse("axiomatic-closure manifest is not newline terminated")
    prefix = AXIOMATIC_LANE_ID + "/"
    for line in text.splitlines():
        match = _MANIFEST_LINE.fullmatch(line)
        if match is None:
            _refuse("axiomatic-closure manifest has a malformed row")
        digest, relative = match.groups()
        posix = PurePosixPath(relative)
        if posix.is_absolute() or ".." in posix.parts or not relative.startswith(prefix):
            _refuse("axiomatic-closure manifest contains an escaping path")
        name = relative[len(prefix):]
        if not name or "/" in name or name in rows:
            _refuse("axiomatic-closure manifest contains a nested or duplicate artifact")
        rows[name] = digest
    if rows != _AXIOMATIC_ARTIFACT_SHA256:
        _refuse("axiomatic-closure manifest is not the exact closed seven-artifact inventory")
    return rows


def _verify_scope_lane(scope_root: Path) -> None:
    if not scope_root.is_dir() or scope_root.is_symlink():
        _refuse("sealed standard-causal lane is absent, non-directory, or symlinked")
    expected_names = set(_SEALED_SCOPE_ARTIFACTS) | {"MANIFEST.sha256"}
    try:
        children = tuple(scope_root.iterdir())
    except OSError as exc:
        _refuse(f"sealed standard-causal lane cannot be enumerated: {exc}")
    if {child.name for child in children} != expected_names:
        _refuse("sealed standard-causal lane is not the exact closed inventory")
    if any(child.is_symlink() or not child.is_file() for child in children):
        _refuse("sealed standard-causal lane contains a symlink or non-file custody object")

    manifest_path = scope_root / "MANIFEST.sha256"
    if _sha256_file(manifest_path) != SEALED_SCOPE_MANIFEST_SHA256:
        _refuse("sealed standard-causal dependency manifest mismatch")
    rows = _parse_scope_manifest(
        _strict_text(manifest_path, "sealed standard-causal manifest")
    )
    for name, expected in rows.items():
        if _sha256_file(scope_root / name) != expected:
            _refuse(f"sealed standard-causal artifact hash mismatch: {name}")
    if rows["THEOREM.md"] != SEALED_SCOPE_THEOREM_SHA256:
        _refuse("sealed standard-causal manifest does not pin the expected theorem")


def _verify_formal_lane(lane_root: Path) -> None:
    if not lane_root.is_dir() or lane_root.is_symlink():
        _refuse("formal U-DCL lane is absent, non-directory, or symlinked")
    expected_names = set(_ARTIFACT_SHA256) | {"MANIFEST.sha256"}
    try:
        children = tuple(lane_root.iterdir())
    except OSError as exc:
        _refuse(f"formal U-DCL lane cannot be enumerated: {exc}")
    if {child.name for child in children} != expected_names:
        _refuse("formal U-DCL lane is not the exact manifest-plus-artifacts inventory")
    if any(child.is_symlink() or not child.is_file() for child in children):
        _refuse("formal U-DCL lane contains a symlink or non-file custody object")

    manifest_path = lane_root / "MANIFEST.sha256"
    if _sha256_file(manifest_path) != FORMAL_MANIFEST_SHA256:
        _refuse("formal U-DCL manifest hash mismatch")
    rows = _parse_manifest(_strict_text(manifest_path, "formal U-DCL manifest"))
    for name, expected in rows.items():
        if _sha256_file(lane_root / name) != expected:
            _refuse(f"formal U-DCL artifact hash mismatch: {name}")


def _verify_axiomatic_lane(lane_root: Path) -> None:
    if not lane_root.is_dir() or lane_root.is_symlink():
        _refuse("axiomatic URFT closure lane is absent, non-directory, or symlinked")
    expected_names = set(_AXIOMATIC_ARTIFACT_SHA256) | {"MANIFEST.sha256"}
    try:
        children = tuple(lane_root.iterdir())
    except OSError as exc:
        _refuse(f"axiomatic URFT closure lane cannot be enumerated: {exc}")
    if {child.name for child in children} != expected_names:
        _refuse("axiomatic URFT closure lane is not the exact closed inventory")
    if any(child.is_symlink() or not child.is_file() for child in children):
        _refuse("axiomatic URFT closure lane contains a symlink or non-file custody object")

    manifest_path = lane_root / "MANIFEST.sha256"
    if _sha256_file(manifest_path) != AXIOMATIC_MANIFEST_SHA256:
        _refuse("axiomatic URFT closure manifest hash mismatch")
    rows = _parse_axiomatic_manifest(
        _strict_text(manifest_path, "axiomatic URFT closure manifest")
    )
    for name, expected in rows.items():
        if _sha256_file(lane_root / name) != expected:
            _refuse(f"axiomatic URFT closure artifact hash mismatch: {name}")


def _run_fresh_verifier(lane_root: Path, expected_stdout: str) -> str:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONPYCACHEPREFIX"] = "/private/tmp/wac-udcl-postulate-pycache"
    try:
        result = subprocess.run(
            [sys.executable, "-I", "-B", str(lane_root / "verify_udcl_conditional_coverage.py")],
            cwd=lane_root.parent,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )
    except (OSError, UnicodeError, subprocess.SubprocessError) as exc:
        _refuse(f"fresh formal verifier execution failed: {exc}")
    if result.returncode != 0:
        _refuse(f"fresh formal verifier returned {result.returncode}")
    if result.stderr:
        _refuse("fresh formal verifier emitted stderr")
    if result.stdout != expected_stdout:
        _refuse("fresh formal verifier differs from the sealed 72/72 transcript")
    return _sha256_bytes(result.stdout.encode("utf-8"))


def _copy_custody_file(source: Path, root: Path, stage_root: Path) -> None:
    """Copy one authenticated repository file to the same staged relative path."""
    try:
        relative = source.resolve(strict=True).relative_to(root.resolve())
    except (OSError, ValueError):
        _refuse(f"axiomatic verifier staging source escapes repository: {source}")
    destination = stage_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2(source, destination)
    except OSError as exc:
        _refuse(f"axiomatic verifier staging failed for {relative}: {exc}")


def _stage_axiomatic_verifier_root(
    root: Path,
    lane_root: Path,
    stage_root: Path,
) -> Path:
    """Stage the sealed verifier with digest-selected dependency targets.

    The sealed verifier predates a repository-root ``README.md`` and resolves
    bare manifest names by existence.  Staging only the uniquely digest-matched
    targets lets those unchanged sealed bytes execute with their original
    packet-local meaning, without rewriting any sealed artifact or manifest.
    """
    root = root.resolve()
    try:
        lane_relative = lane_root.resolve(strict=True).relative_to(root)
    except (OSError, ValueError):
        _refuse("axiomatic verifier lane escapes the repository")
    staged_lane = stage_root / lane_relative
    try:
        shutil.copytree(lane_root, staged_lane)
    except OSError as exc:
        _refuse(f"axiomatic verifier lane staging failed: {exc}")

    dependency_path = lane_root / "DEPENDENCIES.sha256"
    dependency_rows: dict[str, str] = {}
    for line in _strict_text(
        dependency_path,
        "axiomatic verifier dependency ledger",
    ).splitlines():
        match = _MANIFEST_LINE.fullmatch(line)
        if match is None:
            _refuse("axiomatic verifier dependency ledger has a malformed row")
        expected, relative = match.groups()
        if relative in dependency_rows:
            _refuse("axiomatic verifier dependency ledger has a duplicate row")
        dependency_rows[relative] = expected
        source = _declared_root_path(root, relative, "axiomatic dependency ledger")
        if (
            not source.is_file()
            or source.is_symlink()
            or _sha256_file(source) != expected
        ):
            _refuse(f"axiomatic dependency custody mismatch: {relative}")
        _copy_custody_file(source, root, stage_root)

    for relative in sorted(
        item for item in dependency_rows if item.endswith("MANIFEST.sha256")
    ):
        manifest = _declared_root_path(root, relative, "axiomatic dependency ledger")
        seen: set[str] = set()
        for line in _strict_text(
            manifest,
            f"axiomatic dependency manifest {relative}",
        ).splitlines():
            match = _MANIFEST_LINE.fullmatch(line)
            if match is None:
                _refuse(f"axiomatic dependency manifest has a malformed row: {relative}")
            expected, item_relative = match.groups()
            if item_relative in seen:
                _refuse(f"axiomatic dependency manifest has a duplicate row: {relative}")
            seen.add(item_relative)
            source = _resolve_declared_manifest_item(
                root,
                manifest,
                item_relative,
                expected,
            )
            _copy_custody_file(source, root, stage_root)
        if not seen:
            _refuse(f"axiomatic dependency manifest is empty: {relative}")
    return staged_lane


def _run_fresh_axiomatic_verifier(lane_root: Path, expected_stdout: str) -> str:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONPYCACHEPREFIX"] = "/private/tmp/wac-axiomatic-urft-pycache"
    try:
        with tempfile.TemporaryDirectory(prefix="wac-axiomatic-urft-") as temporary:
            stage_root = Path(temporary)
            staged_lane = _stage_axiomatic_verifier_root(
                lane_root.parent,
                lane_root,
                stage_root,
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-B",
                    str(staged_lane / "verify_axiomatic_urft_closure.py"),
                ],
                cwd=stage_root,
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
                check=False,
            )
    except (OSError, UnicodeError, subprocess.SubprocessError) as exc:
        _refuse(f"fresh axiomatic verifier execution failed: {exc}")
    if result.returncode != 0:
        _refuse(f"fresh axiomatic verifier returned {result.returncode}")
    if result.stderr:
        _refuse("fresh axiomatic verifier emitted stderr")
    required_lines = (
        AXIOMATIC_VERIFIER_TOTAL,
        AXIOMATIC_VERIFIER_VERDICT,
        "NATURAL_UDCL_VALIDITY FALSIFIABLE_NOT_EXECUTABLY_PROVED",
        "OUTCOME_SELECTION NOT_A_URFT_PREMISE",
    )
    if any(line not in expected_stdout for line in required_lines):
        _refuse("sealed axiomatic summary lacks a required claim-safe line")
    if any(result.stdout.count(line) != 1 for line in required_lines):
        _refuse("fresh axiomatic verifier lacks an exact required total or verdict")
    if result.stdout.count(" PASS ") != 74 or " FAIL " in result.stdout:
        _refuse("fresh axiomatic verifier did not reproduce exactly 74 passing checks")
    return _sha256_bytes(result.stdout.encode("utf-8"))


@dataclass(frozen=True)
class _Custody:
    adoption_sha256: str
    decision_sha256: str
    decision_audit_sha256: str
    formal_manifest_sha256: str
    formal_audit_sha256: str
    formal_verification_sha256: str
    fresh_verifier_stdout_sha256: str
    sealed_scope_manifest_sha256: str
    axiomatic_manifest_sha256: str
    axiomatic_audit_sha256: str
    axiomatic_verification_sha256: str
    fresh_axiomatic_verifier_stdout_sha256: str


def _verify_custody(root: Path = _REPOSITORY_ROOT) -> _Custody:
    """Verify the adopted decision and theorem.  ``root`` is private/test-only."""
    if not root.is_dir() or root.is_symlink():
        _refuse("repository root is absent, non-directory, or symlinked")

    pinned_root_files = {
        "URFT_UDCL_ADOPTION_V001.md": ADOPTION_SHA256,
        "URFT_UNIVERSAL_DOMAIN_LAW_DECISION_V001.md": DECISION_SHA256,
        "URFT_UNIVERSAL_DOMAIN_LAW_DECISION_V001.AUDIT.md": DECISION_AUDIT_SHA256,
    }
    for relative, expected in pinned_root_files.items():
        path = root / relative
        if not path.is_file() or path.is_symlink() or _sha256_file(path) != expected:
            _refuse(f"root decision custody mismatch: {relative}")

    scope_root = root / SEALED_SCOPE_LANE_ID
    _verify_scope_lane(scope_root)

    lane_root = root / FORMAL_LANE_ID
    _verify_formal_lane(lane_root)
    axiomatic_root = root / AXIOMATIC_LANE_ID
    _verify_axiomatic_lane(axiomatic_root)

    adoption = _strict_text(root / "URFT_UDCL_ADOPTION_V001.md", "adoption record")
    theorem = _strict_text(lane_root / "THEOREM.md", "formal theorem")
    audit = _strict_text(lane_root / "INDEPENDENT_AUDIT.md", "independent formal audit")
    transcript = _strict_text(
        lane_root / "VERIFICATION.txt", "formal verification transcript"
    )
    axiomatic_theorem = _strict_text(
        axiomatic_root / "THEOREM.md", "axiomatic URFT closure theorem"
    )
    axiomatic_audit = _strict_text(
        axiomatic_root / "AUDIT.md", "axiomatic URFT closure audit"
    )
    axiomatic_transcript = _strict_text(
        axiomatic_root / "VERIFICATION.txt", "axiomatic URFT closure transcript"
    )
    if ADOPTION_ID not in adoption or "ADOPTED_AS_WORKING_UNIVERSAL_PHYSICAL_POSTULATE" not in adoption:
        _refuse("adopted status is absent from the adoption record")
    if "Lemma UDCL-L1 -- typed DCL supplies C, S, and J" not in theorem:
        _refuse("typed local DCL-phys-to-C/S/J theorem is absent")
    if "Theorem UDCL-T2 -- conditional universal Coverage-U" not in theorem:
        _refuse("conditional universal theorem is absent")
    if AUDIT_VERDICT not in audit:
        _refuse("accepted conditional-theorem audit verdict is absent")
    if transcript.count(VERIFIER_TOTAL) != 1 or transcript.count(VERIFIER_VERDICT) != 1:
        _refuse("formal transcript lacks the exact 72/72 total or claim-safe verdict")
    if "NATURAL_UDCL_VALIDITY_NOT_TESTED" not in transcript:
        _refuse("formal transcript lacks the natural-validity ceiling")
    if "Theorem AURFT-1 -- universal record-formation coverage" not in axiomatic_theorem:
        _refuse("axiomatic universal closure theorem is absent")
    if "Outcome selection, a Born selector, and collapse are neither premises" not in (
        _strict_text(axiomatic_root / "RESULT.md", "axiomatic URFT closure result")
    ):
        _refuse("axiomatic closure result lacks the outcome-selection ceiling")
    if AXIOMATIC_AUDIT_VERDICT not in axiomatic_audit:
        _refuse("accepted axiomatic-closure audit verdict is absent")
    if (
        axiomatic_transcript.count(AXIOMATIC_VERIFIER_TOTAL) != 1
        or axiomatic_transcript.count(AXIOMATIC_VERIFIER_VERDICT) != 1
    ):
        _refuse("axiomatic transcript lacks the exact 74/74 total or verdict")
    if "NATURAL_UDCL_VALIDITY FALSIFIABLE_NOT_EXECUTABLY_PROVED" not in axiomatic_transcript:
        _refuse("axiomatic transcript lacks the natural-validity ceiling")
    fresh_digest = _run_fresh_verifier(lane_root, transcript)
    fresh_axiomatic_digest = _run_fresh_axiomatic_verifier(
        axiomatic_root, axiomatic_transcript
    )

    # Recheck the decision/dependency and executable custody after reproduction.
    for relative, expected in pinned_root_files.items():
        if _sha256_file(root / relative) != expected:
            _refuse(f"root decision changed during verification: {relative}")
    _verify_scope_lane(scope_root)
    _verify_formal_lane(lane_root)
    _verify_axiomatic_lane(axiomatic_root)

    return _Custody(
        adoption_sha256=ADOPTION_SHA256,
        decision_sha256=DECISION_SHA256,
        decision_audit_sha256=DECISION_AUDIT_SHA256,
        formal_manifest_sha256=FORMAL_MANIFEST_SHA256,
        formal_audit_sha256=_ARTIFACT_SHA256["INDEPENDENT_AUDIT.md"],
        formal_verification_sha256=_ARTIFACT_SHA256["VERIFICATION.txt"],
        fresh_verifier_stdout_sha256=fresh_digest,
        sealed_scope_manifest_sha256=SEALED_SCOPE_MANIFEST_SHA256,
        axiomatic_manifest_sha256=AXIOMATIC_MANIFEST_SHA256,
        axiomatic_audit_sha256=_AXIOMATIC_ARTIFACT_SHA256["AUDIT.md"],
        axiomatic_verification_sha256=_AXIOMATIC_ARTIFACT_SHA256["VERIFICATION.txt"],
        fresh_axiomatic_verifier_stdout_sha256=fresh_axiomatic_digest,
    )


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


def _certificate(custody: _Custody) -> Mapping[str, Any]:
    return _freeze(
        {
            "schema": SCHEMA,
            "claim_class": CLAIM_CLASS,
            "postulate": {
                "adoption_id": ADOPTION_ID,
                "name": "Universal Directed-Composition Law",
                "status": "ADOPTED_WORKING_PHYSICAL_POSTULATE",
                "domain": "ACTUAL_BONA_FIDE_FINITE_MISSION_RECORDS",
                "statement": "FOR_ALL_DOMAIN_RECORDS_DCL_PHYS_R",
                "typed_implementation": "UDCL_TYPED_CLARIFICATION_V002",
                "certificate_predicate": "CERT_DCL_IS_EVIDENTIAL_NOT_ONTIC",
                "natural_validity": "OPEN_AND_FALSIFIABLE",
            },
            "exact_results": {
                "domain_axiom": "DOMAIN_MEMBERSHIP_IMPLIES_REC_R",
                "local_bridge": "DCL_PHYS_R_IMPLIES_C_R_AND_S_R_AND_J_R",
                "per_record": "REC_R_AND_DCL_PHYS_R_IMPLIES_COVERAGE_U_R",
                "universal": "UDCL_IMPLIES_ALL_DOMAIN_RECORDS_HAVE_COVERAGE_U",
                "sound_evidential_bridge": (
                    "CERT_DCL_R_P_WITH_SOUNDNESS_AND_CUSTODY_IMPLIES_DCL_PHYS_R"
                ),
                "theorem_status": "EXACT_CONDITIONAL_ON_ADOPTED_POSTULATE",
                "witness_typing": "ONE_COMMON_K_OR_W_WITNESS_ACROSS_D1_TO_D4",
                "joint_state_status": "D2_SUPPLIES_ONE_JOINT_HISTORY_STATE_NOT_DERIVED_FROM_MARGINALS",
                "axiomatic_closure": (
                    "UDCL_IMPLIES_UNIVERSAL_COVERAGE_WITH_FULL_TRANSITIVE_PROOF_CUSTODY"
                ),
                "axiomatic_closure_status": "74_OF_74_LOGIC_SCOPE_AND_CUSTODY_CHECKS",
            },
            "program_authorizations": {
                "working_postulate_adopted": True,
                "conditional_universal_coverage_theorem": True,
            },
            "scientific_status": {
                "nature_obeys_UDCL": "NOT_ESTABLISHED_BY_THIS_CERTIFICATE",
                "empirical_validation": "NONE_PERFORMED_BY_THIS_CERTIFICATE",
                "caller_input_scientific_weight": "ZERO",
                "single_success_confirms_universal": False,
                "finite_success_collection_proves_universal": False,
                "one_independently_admitted_exception_falsifies": True,
            },
            "nonconsequences": {
                "REC_implies_DCL_phys_without_postulate": False,
                "absence_of_Cert_DCL_implies_not_DCL_phys": False,
                "objective_actualization": False,
                "outcome_selection_or_forcing": False,
                "Born_law": False,
                "authenticated_A5": False,
                "reset_or_universal_sealing_trigger": False,
                "gravity_emergence": False,
                "general_relativity": False,
                "G_or_Lambda": False,
                "U1_or_alpha": False,
            },
            "falsifier": {
                "record_domain_independent_of_DCL_success": True,
                "noncertification_does_not_imply_physical_failure": True,
                "post_hoc_domain_retreat_forbidden": True,
                "ports_categories_and_instruments_frozen_prospectively": True,
                "failure_must_span_every_applicable_category_or_one_independently_exclusive_category": True,
                "negative_fit_without_exhaustive_realization_closure_is_NOT_TESTED": True,
                "refutation_requires_checkable_completeness_theorem": True,
                "refutation_closes_all_allowed_branches_frontiers_states_maps_instruments_and_incidence_realizations": True,
            },
            "custody": {
                "adoption_sha256": custody.adoption_sha256,
                "decision_sha256": custody.decision_sha256,
                "decision_audit_sha256": custody.decision_audit_sha256,
                "formal_lane_id": FORMAL_LANE_ID,
                "formal_manifest_sha256": custody.formal_manifest_sha256,
                "formal_artifact_count": len(_ARTIFACT_SHA256),
                "formal_closed_file_count": len(_ARTIFACT_SHA256) + 1,
                "formal_audit_sha256": custody.formal_audit_sha256,
                "formal_verification_sha256": custody.formal_verification_sha256,
                "fresh_verifier_stdout_sha256": custody.fresh_verifier_stdout_sha256,
                "sealed_scope_manifest_sha256": custody.sealed_scope_manifest_sha256,
                "verifier_total": VERIFIER_TOTAL,
                "verifier_verdict": VERIFIER_VERDICT,
                "audit_verdict": AUDIT_VERDICT,
                "axiomatic_lane_id": AXIOMATIC_LANE_ID,
                "axiomatic_manifest_sha256": custody.axiomatic_manifest_sha256,
                "axiomatic_artifact_count": len(_AXIOMATIC_ARTIFACT_SHA256),
                "axiomatic_closed_file_count": len(_AXIOMATIC_ARTIFACT_SHA256) + 1,
                "axiomatic_audit_sha256": custody.axiomatic_audit_sha256,
                "axiomatic_verification_sha256": custody.axiomatic_verification_sha256,
                "fresh_axiomatic_verifier_stdout_sha256": (
                    custody.fresh_axiomatic_verifier_stdout_sha256
                ),
                "axiomatic_verifier_total": AXIOMATIC_VERIFIER_TOTAL,
                "axiomatic_verifier_verdict": AXIOMATIC_VERIFIER_VERDICT,
                "axiomatic_audit_verdict": AXIOMATIC_AUDIT_VERDICT,
            },
            "executable_scope": {
                "logic_and_scope_checks": "72/72_REPRODUCED",
                "typed_conditional_checks": "72/72_REPRODUCED",
                "axiomatic_transitive_closure_checks": "74/74_REPRODUCED",
                "postulate_machine_proved": False,
                "conditional_theorem_machine_proved": False,
                "documentary_and_finite_logic_regression_only": True,
                "empirical_test_performed": False,
                "statement": "EXECUTABLE_CERTIFIES_ADOPTION_AND_CONDITIONAL_THEOREM_ONLY",
            },
        }
    )


@dataclass(frozen=True)
class UDCLPostulate:
    """Immutable result of one fresh decision/theorem custody check."""

    _custody: _Custody

    @property
    def claim_class(self) -> str:
        return CLAIM_CLASS

    @property
    def manifest_sha256(self) -> str:
        return self._custody.formal_manifest_sha256

    def certificate(self) -> Mapping[str, Any]:
        """Return a fresh recursively immutable claim-bounded certificate."""
        return _certificate(self._custody)


def udcl_postulate() -> UDCLPostulate:
    """Reproduce and expose the adopted postulate and conditional theorem."""
    return UDCLPostulate(_verify_custody())


def udcl_postulate_certificate() -> Mapping[str, Any]:
    """Return the immutable zero-input certificate with open claims preserved."""
    return udcl_postulate().certificate()
