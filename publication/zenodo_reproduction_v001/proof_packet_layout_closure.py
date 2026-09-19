#!/usr/bin/env python3
"""Build and verify portable, original-layout proof packets.

This module is deliberately independent of the capsule manifest and builder.
It closes three historical verifier layouts without rewriting their source
bytes:

* the allow/require (alpha-scope) mechanical audit;
* the final hostile L4 intrinsic-admission verifier; and
* the final L12 prefix-lineage representation audit.

Each packet is sourced from the exact Git revision that sealed it, is copied
under an isolated original-layout root, and is executed only in a disposable
writable copy.  The environment-dependent L4--L10 streamed preflight is
inventoried and authenticated, but is never promoted to a portable pass.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence


SCHEMA = "WAC_PROOF_PACKET_LAYOUT_CLOSURE_V001"
ARCHIVE_ROOT = PurePosixPath("reproduction/proof_packets")
HERE = Path(__file__).resolve().parent
SOURCE_SPEC = HERE / "PROOF_PACKET_LAYOUT_CLOSURE_SPEC.json"
EXTRACTED_SPEC = HERE.parent / "inventory" / "PROOF_PACKET_LAYOUT_CLOSURE_SPEC.json"
if SOURCE_SPEC.is_file():
    DEFAULT_REPOSITORY_ROOT = HERE.parents[1]
    DEFAULT_SPEC = SOURCE_SPEC
else:
    DEFAULT_REPOSITORY_ROOT = HERE.parent
    DEFAULT_SPEC = EXTRACTED_SPEC

ALPHA_ID = "alpha_allow_require_scope_repair_v001"
L4_ID = "l04_intrinsic_admission_final_hostile_v001"
L12_ID = "l12_prefix_lineage_final_audit_v001"
STREAMED_ID = "l04_l10_streamed_preflight_inventory_v001"

PACKET_ORDER = (ALPHA_ID, L4_ID, L12_ID, STREAMED_ID)

REVISIONS = {
    ALPHA_ID: "4b335b7ff527a3e468e0c69f56ae77814bb17e7d",
    L4_ID: "3c8e8385a1113941b545276410e7bc2e340e2a84",
    L12_ID: "42f1ea3301ccf98802c07f3330d52999385cba0b",
    STREAMED_ID: "9f81115b251f207e4f54a09b489f705202d2377b",
}

ALPHA_VERIFIER = PurePosixPath(
    "AUDIT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/verify_scope_repair.py"
)
ALPHA_MANIFEST = PurePosixPath(
    "DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/TARGET_MANIFEST.json"
)
ALPHA_FROZEN = PurePosixPath(
    "AUDIT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/FROZEN_METHOD.json"
)
ALPHA_FIXED_INPUTS = {
    ALPHA_VERIFIER,
    ALPHA_MANIFEST,
    ALPHA_FROZEN,
    PurePosixPath("AUDIT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/METHODOLOGY.md"),
    PurePosixPath(
        "AUDIT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/TARGET_MANIFEST_SCHEMA.json"
    ),
}

L4_VERIFIER = PurePosixPath(
    "AUDIT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/verify_final.py"
)
L4_INPUTS = {
    L4_VERIFIER,
    PurePosixPath(
        "AUDIT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/BOUNDED_BACKEND_REPAIR.md"
    ),
    PurePosixPath(
        "AUDIT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/FROZEN_METHOD.json"
    ),
    PurePosixPath(
        "AUDIT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/FROZEN_REPAIR.json"
    ),
    PurePosixPath(
        "AUDIT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/INDEPENDENT_TRACE_L4.json"
    ),
    PurePosixPath("AUDIT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/METHODOLOGY.md"),
    PurePosixPath(
        "AUDIT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/independent_l4_trace.py"
    ),
    PurePosixPath("DEVELOPMENT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/PROTOCOL.md"),
    PurePosixPath("DEVELOPMENT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/RESULT.md"),
    PurePosixPath("DEVELOPMENT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/TRACE_L4.json"),
    PurePosixPath(
        "DEVELOPMENT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/compute_l4_trace.py"
    ),
}
L4_OUTPUT = PurePosixPath(
    "AUDIT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/FINAL_HOSTILE_RESULT.json"
)

L12_VERIFIER = PurePosixPath(
    "AUDIT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/verify_audit.py"
)
L12_FROZEN = PurePosixPath(
    "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/FROZEN_MANIFEST.json"
)
L12_FROZEN_V002 = PurePosixPath(
    "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/"
    "FROZEN_MANIFEST_V002.json"
)
L12_TARGET = PurePosixPath(
    "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/PREFLIGHT_RESULT.json"
)
L12_HOSTILE = PurePosixPath(
    "AUDIT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/HOSTILE_RESULT.json"
)
L12_FIXED_INPUTS = {
    L12_VERIFIER,
    L12_FROZEN,
    L12_FROZEN_V002,
    L12_TARGET,
    L12_HOSTILE,
    PurePosixPath("DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/PROTOCOL.md"),
    PurePosixPath("DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/THEOREM.md"),
}
L12_ABSENCES = (
    PurePosixPath(
        "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/"
        "RAW_HISTORY/PREFIX_HISTORY_L12.json"
    ),
    PurePosixPath(
        "AUDIT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/"
        "RAW_HISTORY/BLIND_PREFIX_HISTORY_L12.json"
    ),
    PurePosixPath(
        "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/SPECTRUM_L12.json"
    ),
    PurePosixPath(
        "AUDIT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/SPECTRUM_L12.json"
    ),
)
L12_OUTPUT = PurePosixPath(
    "AUDIT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/FINAL_AUDIT_RESULT.json"
)

STREAMED_VERIFIER = PurePosixPath(
    "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/verify_streamed_methods.py"
)
STREAMED_INPUTS = {
    STREAMED_VERIFIER,
    PurePosixPath(
        "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/"
        "METHOD_VALIDATION/BLIND_STREAMED_HISTORY_L4.json"
    ),
    PurePosixPath(
        "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/"
        "METHOD_VALIDATION/BLIND_STREAMED_HISTORY_L6.json"
    ),
    PurePosixPath(
        "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/"
        "METHOD_VALIDATION/BLIND_STREAMED_HISTORY_L8.json"
    ),
    PurePosixPath(
        "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/blind_streamed_history.py"
    ),
    PurePosixPath(
        "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compare_L10_history.py"
    ),
    PurePosixPath(
        "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/BLOCK_KERNEL_BENCHMARK.json"
    ),
    PurePosixPath(
        "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/"
        "METHOD_VALIDATION/STREAMED_HISTORY_L4.json"
    ),
    PurePosixPath(
        "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/"
        "METHOD_VALIDATION/STREAMED_HISTORY_L6.json"
    ),
    PurePosixPath(
        "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/"
        "METHOD_VALIDATION/STREAMED_HISTORY_L8.json"
    ),
    PurePosixPath("DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md"),
    PurePosixPath(
        "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/RAW_HISTORY/HISTORY_L4.json"
    ),
    PurePosixPath(
        "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/RAW_HISTORY/HISTORY_L6.json"
    ),
    PurePosixPath(
        "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/RAW_HISTORY/HISTORY_L8.json"
    ),
    PurePosixPath(
        "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/STREAMED_METHOD_FREEZE.md"
    ),
    PurePosixPath(
        "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/benchmark_block_kernel.py"
    ),
    PurePosixPath(
        "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_streamed_history.py"
    ),
}

BYTE_LEAK_PATTERNS: tuple[tuple[str, re.Pattern[bytes]], ...] = (
    (
        "local_path",
        re.compile(rb"/(?:Users|home|root|var/folders)/[^\x00\r\n\t \"']+", re.I),
    ),
    (
        "local_path",
        re.compile(rb"[A-Za-z]:\\\\Users\\\\[^\x00\r\n\t \"']+", re.I),
    ),
    ("local_path", re.compile(rb"file://", re.I)),
    ("cloud_reference", re.compile(rb"arn:aws(?:-us-gov|-cn)?:", re.I)),
    ("cloud_reference", re.compile(rb"s3://", re.I)),
    ("cloud_reference", re.compile(rb"amazonaws\.com", re.I)),
    (
        "cloud_reference",
        re.compile(rb"\b(?:i|vpc|subnet|sg)-[0-9a-f]{8,17}\b", re.I),
    ),
    ("credential", re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    (
        "credential",
        re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
    (
        "email",
        re.compile(rb"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    ),
)


class Refusal(RuntimeError):
    """A source, archive, layout, leakage, or execution predicate failed."""


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_relative(value: str | PurePosixPath) -> PurePosixPath:
    raw = str(value)
    if not raw or "\x00" in raw or "\\" in raw:
        raise Refusal(f"unsafe relative path: {raw!r}")
    path = PurePosixPath(raw)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise Refusal(f"unsafe relative path: {raw!r}")
    return path


def strict_json_bytes(data: bytes, label: str) -> Mapping[str, Any]:
    def reject_constant(value: str) -> None:
        raise Refusal(f"non-standard JSON numeric constant in {label}: {value}")

    def unique_object(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise Refusal(f"duplicate JSON key in {label}: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal(f"{label} is not strict UTF-8 JSON: {error}") from error
    if not isinstance(value, Mapping):
        raise Refusal(f"{label} must contain a JSON object")
    return value


def leakage_classes(data: bytes) -> list[str]:
    return sorted(
        {label for label, pattern in BYTE_LEAK_PATTERNS if pattern.search(data)}
    )


def require_no_leakage(data: bytes, label: str) -> None:
    findings = leakage_classes(data)
    if findings:
        raise Refusal(f"release leakage in {label}: {', '.join(findings)}")


def _run_git(repository_root: Path, arguments: Sequence[str]) -> bytes:
    command = ["git", "-C", str(repository_root), *arguments]
    try:
        process = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            env={**os.environ, "LC_ALL": "C"},
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Refusal(f"cannot run Git command {arguments!r}: {error}") from error
    if process.returncode:
        detail = process.stderr.decode("utf-8", "replace").strip()
        raise Refusal(f"Git command failed {arguments!r}: {detail}")
    return process.stdout


def require_repository(repository_root: Path) -> Path:
    root = repository_root.resolve()
    top = Path(
        _run_git(root, ("rev-parse", "--show-toplevel"))
        .decode("utf-8")
        .strip()
    ).resolve()
    if top != root:
        raise Refusal(f"repository root mismatch: expected {root}, Git reports {top}")
    return root


def git_blob(repository_root: Path, revision: str, relative: str | PurePosixPath) -> bytes:
    path = normalized_relative(relative)
    resolved = (
        _run_git(repository_root, ("rev-parse", "--verify", f"{revision}^{{commit}}"))
        .decode("ascii")
        .strip()
    )
    if resolved != revision:
        raise Refusal(f"revision does not resolve exactly: {revision} -> {resolved}")
    return _run_git(repository_root, ("cat-file", "blob", f"{revision}:{path}"))


def packet_archive_prefix(packet_id: str) -> PurePosixPath:
    return ARCHIVE_ROOT / packet_id / "original_layout"


def _alpha_inputs(repository_root: Path) -> set[PurePosixPath]:
    revision = REVISIONS[ALPHA_ID]
    manifest = strict_json_bytes(
        git_blob(repository_root, revision, ALPHA_MANIFEST), str(ALPHA_MANIFEST)
    )
    frozen = strict_json_bytes(
        git_blob(repository_root, revision, ALPHA_FROZEN), str(ALPHA_FROZEN)
    )
    artifacts = manifest.get("artifacts")
    historical = frozen.get("historical_hashes")
    if not isinstance(artifacts, list) or not artifacts:
        raise Refusal("alpha TARGET_MANIFEST artifacts must be a non-empty list")
    if not isinstance(historical, Mapping) or not historical:
        raise Refusal("alpha FROZEN_METHOD historical_hashes must be a non-empty object")
    inputs = set(ALPHA_FIXED_INPUTS)
    for row in artifacts:
        if not isinstance(row, Mapping) or not isinstance(row.get("path"), str):
            raise Refusal("invalid alpha TARGET_MANIFEST artifact row")
        relative = normalized_relative(row["path"])
        data = git_blob(repository_root, revision, relative)
        if digest_bytes(data) != row.get("sha256"):
            raise Refusal(f"alpha TARGET_MANIFEST hash mismatch: {relative}")
        inputs.add(relative)
    for raw_path, expected in historical.items():
        relative = normalized_relative(str(raw_path))
        data = git_blob(repository_root, revision, relative)
        if digest_bytes(data) != expected:
            raise Refusal(f"alpha historical hash mismatch: {relative}")
        inputs.add(relative)

    audit_dir = PurePosixPath("AUDIT_ALLOW_REQUIRE_SCOPE_REPAIR_V001")
    frozen_hashes = {
        audit_dir / "METHODOLOGY.md": frozen.get("methodology_sha256"),
        audit_dir / "TARGET_MANIFEST_SCHEMA.json": frozen.get("schema_sha256"),
        audit_dir / "verify_scope_repair.py": frozen.get("verifier_sha256"),
    }
    for relative, expected in frozen_hashes.items():
        if digest_bytes(git_blob(repository_root, revision, relative)) != expected:
            raise Refusal(f"alpha frozen audit dependency mismatch: {relative}")
    return inputs


def _l12_inputs(repository_root: Path) -> set[PurePosixPath]:
    revision = REVISIONS[L12_ID]
    inputs = set(L12_FIXED_INPUTS)
    manifest1 = strict_json_bytes(
        git_blob(repository_root, revision, L12_FROZEN), str(L12_FROZEN)
    )
    manifest2 = strict_json_bytes(
        git_blob(repository_root, revision, L12_FROZEN_V002), str(L12_FROZEN_V002)
    )
    for label, manifest in (("V001", manifest1), ("V002", manifest2)):
        files = manifest.get("files")
        if not isinstance(files, Mapping) or not files:
            raise Refusal(f"L12 {label} frozen files must be a non-empty object")
        for raw_path in files:
            inputs.add(normalized_relative(str(raw_path)))
    return inputs


def packet_inputs(repository_root: Path, packet_id: str) -> set[PurePosixPath]:
    if packet_id == ALPHA_ID:
        return _alpha_inputs(repository_root)
    if packet_id == L4_ID:
        return set(L4_INPUTS)
    if packet_id == L12_ID:
        return _l12_inputs(repository_root)
    if packet_id == STREAMED_ID:
        return set(STREAMED_INPUTS)
    raise Refusal(f"unknown packet id: {packet_id}")


def member_record(
    repository_root: Path, packet_id: str, relative: PurePosixPath
) -> dict[str, Any]:
    revision = REVISIONS[packet_id]
    data = git_blob(repository_root, revision, relative)
    require_no_leakage(data, f"{packet_id}:{relative}")
    prefix = packet_archive_prefix(packet_id)
    return {
        "archive_path": str(prefix / relative),
        "bytes": len(data),
        "path": str(relative),
        "sha256": digest_bytes(data),
    }


def _sealed_output(
    repository_root: Path,
    packet_id: str,
    relative: PurePosixPath,
    verdict: str,
    checks_passed: int,
    checks_total: int,
) -> dict[str, Any]:
    data = git_blob(repository_root, REVISIONS[packet_id], relative)
    require_no_leakage(data, f"sealed output {packet_id}:{relative}")
    return {
        "bytes": len(data),
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "path": str(relative),
        "sha256": digest_bytes(data),
        "verdict": verdict,
    }


def expected_spec(repository_root: Path) -> dict[str, Any]:
    root = require_repository(repository_root)
    packets: list[dict[str, Any]] = []
    total_members = 0
    total_bytes = 0
    for packet_id in PACKET_ORDER:
        members = [
            member_record(root, packet_id, relative)
            for relative in sorted(packet_inputs(root, packet_id), key=str)
        ]
        member_bytes = sum(int(row["bytes"]) for row in members)
        total_members += len(members)
        total_bytes += member_bytes
        base: dict[str, Any] = {
            "archive_prefix": str(packet_archive_prefix(packet_id)),
            "id": packet_id,
            "member_count": len(members),
            "members": members,
            "source_revision": REVISIONS[packet_id],
            "total_bytes": member_bytes,
        }
        if packet_id == ALPHA_ID:
            base.update(
                {
                    "absence_predicates": [],
                    "classification": "REVISION_PINNED_ORIGINAL_LAYOUT_PORTABLE_GATE",
                    "execution": {
                        "expected_checks_passed": 300,
                        "expected_checks_total": 300,
                        "expected_verdict": "PASS_MECHANICAL__SEMANTIC_HOSTILE_READ_REQUIRED",
                        "manifest_argument": str(ALPHA_MANIFEST),
                        "mode": "PYTHON_VERIFIER_WITH_ROOT_ARGUMENT",
                        "verifier": str(ALPHA_VERIFIER),
                    },
                    "outputs_written": [],
                    "portable_capsule_gate": True,
                    "source_policy": (
                        "ALL_BYTES_FROM_THE_ISOLATED_HISTORICAL_PASS_COMMIT__"
                        "LATER_LIVE_LEDGER_EDITS_ARE_NOT_SUBSTITUTED"
                    ),
                }
            )
        elif packet_id == L4_ID:
            base.update(
                {
                    "absence_predicates": [],
                    "classification": "ORIGINAL_LAYOUT_PORTABLE_GATE_WRITES_DISPOSABLE_OUTPUT",
                    "execution": {
                        "expected_checks_passed": 50,
                        "expected_checks_total": 50,
                        "expected_verdict": "PASS_FINAL_HOSTILE_INTRINSIC_ADMISSION_L4",
                        "mode": "PYTHON_VERIFIER",
                        "verifier": str(L4_VERIFIER),
                    },
                    "outputs_written": [
                        _sealed_output(
                            root,
                            packet_id,
                            L4_OUTPUT,
                            "PASS_FINAL_HOSTILE_INTRINSIC_ADMISSION_L4",
                            50,
                            50,
                        )
                    ],
                    "portable_capsule_gate": True,
                    "required_sibling_repairs": [
                        "AUDIT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/BOUNDED_BACKEND_REPAIR.md",
                        "AUDIT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/FROZEN_REPAIR.json",
                    ],
                    "source_policy": "ALL_BYTES_FROM_THE_FINAL_HOSTILE_SEAL_COMMIT",
                }
            )
        elif packet_id == L12_ID:
            base.update(
                {
                    "absence_predicates": [
                        {"expected": "absent", "path": str(path)}
                        for path in L12_ABSENCES
                    ],
                    "classification": (
                        "ORIGINAL_LAYOUT_PORTABLE_GATE_WRITES_DISPOSABLE_OUTPUT_"
                        "WITH_PRESERVED_ABSENCE_PREDICATES"
                    ),
                    "execution": {
                        "expected_checks_passed": 40,
                        "expected_checks_total": 40,
                        "expected_verdict": (
                            "PASS_HOSTILE_SCREEN__EXACT_L12_REPRESENTATION_ONLY__"
                            "L12_HISTORY_AWAITS_BENCHMARK"
                        ),
                        "mode": "PYTHON_VERIFIER",
                        "verifier": str(L12_VERIFIER),
                    },
                    "outputs_written": [
                        _sealed_output(
                            root,
                            packet_id,
                            L12_OUTPUT,
                            (
                                "PASS_HOSTILE_SCREEN__EXACT_L12_REPRESENTATION_ONLY__"
                                "L12_HISTORY_AWAITS_BENCHMARK"
                            ),
                            40,
                            40,
                        )
                    ],
                    "portable_capsule_gate": True,
                    "required_freezes": [str(L12_FROZEN), str(L12_FROZEN_V002)],
                    "source_policy": "ALL_BYTES_FROM_THE_FINAL_PREFIX_LINEAGE_AUDIT_COMMIT",
                }
            )
        else:
            base.update(
                {
                    "absence_predicates": [],
                    "classification": (
                        "ENVIRONMENT_DEPENDENT_HISTORICAL_PREFLIGHT_INVENTORY_ONLY"
                    ),
                    "execution": {
                        "mode": "DO_NOT_EXECUTE_AS_A_PORTABLE_CAPSULE_GATE",
                        "verifier": str(STREAMED_VERIFIER),
                    },
                    "nonportable_reason": (
                        "the historical verdict directly tests "
                        "shutil.disk_usage(extraction_root).free < 60 GiB"
                    ),
                    "outputs_written": [
                        {
                            "path": (
                                "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/"
                                "STREAMED_METHOD_PREFLIGHT_RESULT.json"
                            ),
                            "status": "environment-dependent; not regenerated",
                        }
                    ],
                    "portable_capsule_gate": False,
                    "source_policy": "AUTHENTICATED_INVENTORY_ONLY",
                }
            )
        packets.append(base)

    return {
        "archive_layout": {
            "isolation_rule": (
                "each verifier receives a separate repository root so duplicate root-relative "
                "names cannot alias across historical packets"
            ),
            "original_basename_rule": (
                "every archive member retains its complete original repository-relative path "
                "beneath the packet's original_layout directory"
            ),
            "root": str(ARCHIVE_ROOT),
            "verification_rule": (
                "authenticate archive bytes, copy each portable packet to a writable temporary "
                "tree, execute there, and leave archive bytes unchanged"
            ),
        },
        "claim_boundary": (
            "LAYOUT_HASH_AND_PORTABLE_VERIFIER_CLOSURE_ONLY__NO_NEW_ALPHA_L4_L12_"
            "HISTORY_SPECTRUM_CONTINUUM_EMERGENCE_GRAVITY_OR_L14_RESULT"
        ),
        "leakage_scan": {
            "classes": [
                "cloud_reference",
                "credential",
                "email",
                "local_path",
            ],
            "finding_count": 0,
            "status": "PASS_NO_RELEASE_LEAKAGE_IN_AUTHENTICATED_SOURCE_MEMBERS",
        },
        "member_count": total_members,
        "packets": packets,
        "private_l12_release_evidence": (
            "OUT_OF_SCOPE__USE_THE_SEPARATE_RELEASE_SPECIFIC_SANITIZER_VERIFIER__"
            "NO_PRIVATE_RAW_L12_ARTIFACT_IS_INCLUDED_HERE"
        ),
        "schema": SCHEMA,
        "total_bytes": total_bytes,
    }


def load_checked_spec(spec_path: Path) -> Mapping[str, Any]:
    try:
        data = spec_path.read_bytes()
    except OSError as error:
        raise Refusal(f"cannot read checked specification {spec_path}: {error}") from error
    return strict_json_bytes(data, str(spec_path))


def verify_source(repository_root: Path, spec_path: Path = DEFAULT_SPEC) -> dict[str, Any]:
    expected = expected_spec(repository_root)
    checked = load_checked_spec(spec_path)
    if checked != expected:
        raise Refusal("checked proof-packet specification does not match pinned sources")
    return {
        "member_count": expected["member_count"],
        "packet_count": len(expected["packets"]),
        "status": "VERIFIED_PINNED_PROOF_PACKET_SOURCE_CLOSURE",
        "total_bytes": expected["total_bytes"],
    }


def _stable_file(path: Path) -> bytes:
    try:
        before = path.stat()
    except OSError as error:
        raise Refusal(f"cannot stat extracted member {path}: {error}") from error
    if not stat.S_ISREG(before.st_mode) or path.is_symlink():
        raise Refusal(f"extracted member is not a non-symlink regular file: {path}")
    try:
        data = path.read_bytes()
    except OSError as error:
        raise Refusal(f"cannot read extracted member {path}: {error}") from error
    after = path.stat()
    identity1 = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    identity2 = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    if identity1 != identity2 or len(data) != before.st_size:
        raise Refusal(f"extracted member changed while read: {path}")
    return data


def _packet_by_id(spec: Mapping[str, Any], packet_id: str) -> Mapping[str, Any]:
    rows = [row for row in spec["packets"] if row.get("id") == packet_id]
    if len(rows) != 1:
        raise Refusal(f"specification packet census is not one for {packet_id}")
    return rows[0]


def _archive_packet_root(archive_root: Path, packet: Mapping[str, Any]) -> Path:
    relative = normalized_relative(str(packet["archive_prefix"]))
    return archive_root.joinpath(*relative.parts)


def _actual_relative_files(root: Path) -> set[str]:
    if not root.is_dir():
        raise Refusal(f"missing packet original-layout root: {root}")
    result: set[str] = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise Refusal(f"symlink forbidden in extracted packet: {path}")
        if path.is_file():
            result.add(path.relative_to(root).as_posix())
        elif not path.is_dir():
            raise Refusal(f"unsupported extracted packet member: {path}")
    return result


def authenticate_archive_packet(
    archive_root: Path, packet: Mapping[str, Any]
) -> dict[str, bytes]:
    packet_root = _archive_packet_root(archive_root, packet)
    expected_paths = {str(row["path"]) for row in packet["members"]}
    actual_paths = _actual_relative_files(packet_root)
    if actual_paths != expected_paths:
        missing = sorted(expected_paths - actual_paths)
        extra = sorted(actual_paths - expected_paths)
        raise Refusal(
            f"packet member-set mismatch {packet['id']}: missing={missing} extra={extra}"
        )
    authenticated: dict[str, bytes] = {}
    for row in packet["members"]:
        relative = normalized_relative(str(row["path"]))
        path = packet_root.joinpath(*relative.parts)
        data = _stable_file(path)
        if len(data) != row["bytes"] or digest_bytes(data) != row["sha256"]:
            raise Refusal(f"packet member authentication failed {packet['id']}:{relative}")
        require_no_leakage(data, f"extracted {packet['id']}:{relative}")
        authenticated[str(relative)] = data
    for predicate in packet.get("absence_predicates", []):
        if predicate.get("expected") != "absent":
            raise Refusal(f"unknown absence predicate in packet {packet['id']}")
        relative = normalized_relative(str(predicate["path"]))
        if packet_root.joinpath(*relative.parts).exists():
            raise Refusal(f"required absence violated {packet['id']}:{relative}")
    return authenticated


def _write_original_layout(root: Path, authenticated: Mapping[str, bytes]) -> None:
    for raw_path, data in authenticated.items():
        relative = normalized_relative(raw_path)
        target = root.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def _run_portable_packet(
    packet: Mapping[str, Any], authenticated: Mapping[str, bytes]
) -> dict[str, Any]:
    if packet.get("portable_capsule_gate") is not True:
        raise Refusal(f"refusing to execute inventory-only packet {packet['id']}")
    execution = packet["execution"]
    verifier = normalized_relative(str(execution["verifier"]))
    with tempfile.TemporaryDirectory(prefix=f"wac-proof-{packet['id']}-") as temporary:
        root = Path(temporary) / "repository"
        root.mkdir()
        _write_original_layout(root, authenticated)
        command = [sys.executable, str(root.joinpath(*verifier.parts))]
        if execution["mode"] == "PYTHON_VERIFIER_WITH_ROOT_ARGUMENT":
            manifest = normalized_relative(str(execution["manifest_argument"]))
            command.extend((str(manifest), "--root", str(root)))
        elif execution["mode"] != "PYTHON_VERIFIER":
            raise Refusal(f"unknown portable execution mode for {packet['id']}")
        try:
            process = subprocess.run(
                command,
                cwd=root,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C"},
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise Refusal(f"portable verifier could not run {packet['id']}: {error}") from error
        stdout = process.stdout.decode("utf-8", "replace")
        stderr = process.stderr.decode("utf-8", "replace")
        if process.returncode:
            raise Refusal(
                f"portable verifier failed {packet['id']} rc={process.returncode}; "
                f"stdout={stdout!r}; stderr={stderr!r}"
            )

        outputs = packet.get("outputs_written", [])
        output_paths = {str(row["path"]) for row in outputs}
        expected_after = set(authenticated) | output_paths
        actual_after = _actual_relative_files(root)
        if actual_after != expected_after:
            raise Refusal(
                f"portable verifier wrote unexpected paths {packet['id']}: "
                f"{sorted(actual_after - expected_after)}"
            )
        for relative, before in authenticated.items():
            after = _stable_file(root / relative)
            if after != before:
                raise Refusal(f"portable verifier changed source bytes {packet['id']}:{relative}")
        for predicate in packet.get("absence_predicates", []):
            relative = normalized_relative(str(predicate["path"]))
            if root.joinpath(*relative.parts).exists():
                raise Refusal(
                    f"portable verifier violated absence predicate {packet['id']}:{relative}"
                )

        if outputs:
            if len(outputs) != 1:
                raise Refusal(f"unsupported output census for {packet['id']}")
            row = outputs[0]
            output_path = root / str(row["path"])
            output_data = _stable_file(output_path)
            if len(output_data) != row["bytes"] or digest_bytes(output_data) != row["sha256"]:
                raise Refusal(f"portable verifier output mismatch {packet['id']}")
            report = strict_json_bytes(output_data, f"generated output {packet['id']}")
        else:
            report = strict_json_bytes(process.stdout, f"stdout {packet['id']}")

        verdict = report.get("verdict", report.get("classification"))
        if verdict != execution["expected_verdict"]:
            raise Refusal(f"portable verifier verdict mismatch {packet['id']}: {verdict}")
        if report.get("checks_passed") != execution["expected_checks_passed"]:
            raise Refusal(f"portable verifier passed-check census mismatch {packet['id']}")
        if report.get("checks_total") != execution["expected_checks_total"]:
            raise Refusal(f"portable verifier total-check census mismatch {packet['id']}")
        return {
            "checks_passed": report["checks_passed"],
            "checks_total": report["checks_total"],
            "id": packet["id"],
            "verdict": verdict,
        }


def verify_archive(
    archive_root: Path, spec_path: Path = DEFAULT_SPEC, run_portable: bool = True
) -> dict[str, Any]:
    spec = load_checked_spec(spec_path)
    if spec.get("schema") != SCHEMA:
        raise Refusal(f"unexpected proof-packet specification schema: {spec.get('schema')}")
    executions: list[dict[str, Any]] = []
    inventory_only: list[str] = []
    for packet_id in PACKET_ORDER:
        packet = _packet_by_id(spec, packet_id)
        authenticated = authenticate_archive_packet(archive_root, packet)
        if packet.get("portable_capsule_gate") is True:
            if run_portable:
                executions.append(_run_portable_packet(packet, authenticated))
        else:
            if packet["execution"]["mode"] != "DO_NOT_EXECUTE_AS_A_PORTABLE_CAPSULE_GATE":
                raise Refusal(f"inventory-only packet has executable gate mode: {packet_id}")
            inventory_only.append(packet_id)
    return {
        "executed_portable_packets": executions,
        "inventory_only_packets": inventory_only,
        "member_count": spec["member_count"],
        "status": (
            "VERIFIED_EXTRACTED_PROOF_PACKET_LAYOUT_AND_PORTABLE_GATES"
            if run_portable
            else "VERIFIED_EXTRACTED_PROOF_PACKET_LAYOUT"
        ),
    }


def materialize(
    repository_root: Path,
    archive_root: Path,
    spec_path: Path = DEFAULT_SPEC,
    run_portable: bool = True,
) -> dict[str, Any]:
    root = require_repository(repository_root)
    verify_source(root, spec_path)
    spec = load_checked_spec(spec_path)
    if archive_root.exists() and any(archive_root.iterdir()):
        raise Refusal(f"materialization destination is not empty: {archive_root}")
    archive_root.mkdir(parents=True, exist_ok=True)
    for packet in spec["packets"]:
        revision = str(packet["source_revision"])
        for member in packet["members"]:
            relative = normalized_relative(str(member["path"]))
            archive = normalized_relative(str(member["archive_path"]))
            data = git_blob(root, revision, relative)
            if len(data) != member["bytes"] or digest_bytes(data) != member["sha256"]:
                raise Refusal(f"source changed during materialization: {packet['id']}:{relative}")
            target = archive_root.joinpath(*archive.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    return verify_archive(archive_root, spec_path, run_portable=run_portable)


def write_spec(repository_root: Path, spec_path: Path = DEFAULT_SPEC) -> dict[str, Any]:
    spec = expected_spec(repository_root)
    spec_path.write_bytes(canonical_json(spec))
    return {
        "member_count": spec["member_count"],
        "path": str(spec_path),
        "status": "WROTE_PROOF_PACKET_LAYOUT_CLOSURE_SPEC",
        "total_bytes": spec["total_bytes"],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository-root", type=Path, default=DEFAULT_REPOSITORY_ROOT
    )
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("write-spec")
    subparsers.add_parser("verify-source")
    materialize_parser = subparsers.add_parser("materialize")
    materialize_parser.add_argument("destination", type=Path)
    materialize_parser.add_argument("--no-run", action="store_true")
    archive_parser = subparsers.add_parser("verify-archive")
    archive_parser.add_argument("archive_root", type=Path)
    archive_parser.add_argument("--no-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "write-spec":
            result = write_spec(args.repository_root, args.spec)
        elif args.command == "verify-source":
            result = verify_source(args.repository_root, args.spec)
        elif args.command == "materialize":
            result = materialize(
                args.repository_root,
                args.destination,
                args.spec,
                run_portable=not args.no_run,
            )
        else:
            result = verify_archive(
                args.archive_root,
                args.spec,
                run_portable=not args.no_run,
            )
    except Refusal as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(canonical_json(result).decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
