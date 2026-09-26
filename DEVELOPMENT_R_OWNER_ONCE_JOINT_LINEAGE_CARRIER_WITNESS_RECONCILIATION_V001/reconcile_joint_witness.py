#!/usr/bin/env python3
"""Fail-closed reconciliation of the sealed target and hostile seed witnesses.

This program does not run either physical implementation.  It authenticates
their sealed artifacts, independently recomputes the frozen comparison and
control gates, and writes one deterministic adjudication record.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence


SCHEMA = "OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_RECONCILIATION_V001"
UNRESOLVED = "OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_UNRESOLVED"
RESOLVED = "RESOLVED_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_L4_L8"
FALSIFIED = "NO_RESOLVED_OWNER_ONCE_JOINT_MEMORY_IN_FIXED_WITNESS_L4_L8"

PACKET = Path(__file__).resolve().parent
DEFAULT_ROOT = PACKET.parent
DEFAULT_OUTPUT = PACKET / "FINAL_DISPOSITION_V001.json"

TARGET_DIR = "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001"
HOSTILE_DIR = "AUDIT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001"

PROTOCOL = f"{TARGET_DIR}/PROTOCOL.md"
TARGET_RESULT = f"{TARGET_DIR}/TARGET_WITNESS_RESULT_V001.json"
TARGET_SEAL = f"{TARGET_DIR}/TARGET_WITNESS_SEAL_V001.json"
HOSTILE_RESULT = f"{HOSTILE_DIR}/HOSTILE_RESULT.json"
HOSTILE_EXECUTION = f"{HOSTILE_DIR}/HOSTILE_EXECUTION_RECORD.json"
HOSTILE_SOURCE_FREEZE = f"{HOSTILE_DIR}/SOURCE_FREEZE.json"
HOSTILE_SOURCE_MANIFEST = f"{HOSTILE_DIR}/SOURCE_HASHES.sha256"
HOSTILE_RESULT_MANIFEST = f"{HOSTILE_DIR}/RESULT_HASHES.sha256"
HOSTILE_RESULT_SINGLE_MANIFEST = f"{HOSTILE_DIR}/HOSTILE_RESULT.sha256"

# These hashes pin the inputs seen by this separately written reconciliation.
# Cross-linked self-reports are also checked below; neither alone is accepted.
PINNED_HASHES = {
    PROTOCOL: "70984a927c30585704622dfd03ee91bf516cd9a5d14474a228d231144e5e513e",
    f"{TARGET_DIR}/README.md": "4e56461d23d79f1e9a6b36b37360a81c265f9ae76763313b21b0dea2421effc7",
    TARGET_RESULT: "c1763b57b3d6a1a61b66f621b563bfc9cf34123d311e04dff2b1ac02061c1ac8",
    TARGET_SEAL: "2549b7d78324b78b15f3b3da818b904020f77c1b3f14324d99f1f864a0af7610",
    f"{TARGET_DIR}/target_joint_witness.py": "390264b88903f2cafa9bd8c7cb73d174a547a7b53d70e4c55020e6af6b94fcb6",
    f"{TARGET_DIR}/test_target_joint_witness.py": "e98116fcd5a783f2819cbaa21ff184706582616e41b6f8ee69695705fffa0de9",
    f"{HOSTILE_DIR}/README.md": "52b2bc398c628ba692052de0614dcfd7541651ae58a781f9ade18424c9b0df9b",
    f"{HOSTILE_DIR}/EXECUTION_COMPATIBILITY_REPAIR.md": "f415f3e0c903712800a18d031656c177ffa468782746538a3d728aea8fd0b9c8",
    HOSTILE_RESULT: "8b9c9cbdf53e857e29756c95d3702a1401cc509f294d162260e12b9b5c49a29c",
    HOSTILE_EXECUTION: "f409a1638c3c18e825e21189fc0d2cd685b07a9a6432271775b7f624e11603a3",
    HOSTILE_SOURCE_FREEZE: "4782e57c123d60ec3c6e6a8fedbcd1fc3fed06918c77d052e64e699593638c8e",
    HOSTILE_SOURCE_MANIFEST: "39c23f9738e97706f6430a70b95e98bd191dc5880944d46bd1ba99cd7c7f1367",
    HOSTILE_RESULT_MANIFEST: "dc4aac4a7968fa0d83d0c37c9cb7b034308db2d1d77ca2605147e27b0d58ac9f",
    HOSTILE_RESULT_SINGLE_MANIFEST: "62de4a7fb982b2ac7571075e2126589ef64332cabd60fecbb094612b268925b5",
    f"{HOSTILE_DIR}/independent_joint_witness.py": "0f861018fe150c662ad8968c0cc6c8f8022c12991c5aebd0bcf73d760aaf19a9",
    f"{HOSTILE_DIR}/test_source_freeze.py": "1d49d5c7260332834ae7b0432f4a9a8b1694a689467571596ab5460a874b742a",
    "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py": "24ea3626fda443dd4ae5076c7766e1aaca77ff5ce9f22c05bae96943fc627d55",
    "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md": "d545a4dd0925d4ae47c1231f4f7632c4cdfef14d0864af292f19fd9f6a708d95",
    "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/PROTOCOL.md": "964237c44690e86636b4d13150bc277d4dfd21ec0f8338105d7b420512f5e7c5",
}

MANDATORY_LENGTHS = (4, 6, 8)
COARSE_STEPS = 64
FINE_STEPS = 128
TAYLOR_ORDER = 12
PHI = math.pi / 4.0
DWELL = math.pi / 2.0

TOLERANCES = {
    "coarse_fine": 1.0e-8,
    "target_independent": 1.0e-8,
    "norm_content": 1.0e-10,
    "probability_marginal": 1.0e-10,
    "charge": 1.0e-10,
    "shuffle": 1.0e-12,
    "sham": 1.0e-12,
    "l4_exhaustive": 1.0e-12,
}
DERIVED_VALUE_TOLERANCE = 5.0e-18
IDENTITY_TOLERANCE = 1.0e-12


class ReconciliationError(RuntimeError):
    """An authentication, schema, or nonfinite-data failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReconciliationError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def strict_json(path: Path) -> Any:
    def reject_constant(value: str) -> None:
        raise ReconciliationError(f"nonstandard numeric constant in {path.name}: {value}")

    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle, parse_constant=reject_constant)
    except (OSError, json.JSONDecodeError) as error:
        raise ReconciliationError(f"cannot read strict JSON {path.name}: {error}") from error
    verify_finite(value, path.name)
    return value


def verify_finite(value: Any, label: str) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            verify_finite(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            verify_finite(child, f"{label}[{index}]")
    elif isinstance(value, float):
        require(math.isfinite(value), f"nonfinite value at {label}")


def numeric(value: Any, label: str) -> float:
    require(isinstance(value, (int, float)) and not isinstance(value, bool), f"non-numeric {label}")
    result = float(value)
    require(math.isfinite(result), f"nonfinite {label}")
    return result


def integer(value: Any, label: str) -> int:
    require(isinstance(value, int) and not isinstance(value, bool), f"non-integer {label}")
    return value


def close(left: Any, right: Any, label: str, tolerance: float = DERIVED_VALUE_TOLERANCE) -> None:
    a = numeric(left, f"{label} left")
    b = numeric(right, f"{label} right")
    require(abs(a - b) <= tolerance, f"{label} mismatch: {a!r} versus {b!r}")


def relative_path(value: Any, label: str) -> str:
    require(isinstance(value, str) and value, f"invalid path at {label}")
    require("\\" not in value, f"non-POSIX path at {label}")
    path = PurePosixPath(value)
    require(not path.is_absolute(), f"absolute path at {label}")
    require(".." not in path.parts and "." not in path.parts, f"non-canonical relative path at {label}")
    return value


def verify_no_runtime_metadata(value: Any, label: str) -> None:
    banned = {"host", "hostname", "timestamp", "timestamps", "generated_at", "created_at", "updated_at"}
    if isinstance(value, Mapping):
        for key, child in value.items():
            lowered = str(key).lower()
            require(lowered not in banned and not lowered.endswith("_timestamp"), f"runtime metadata key at {label}.{key}")
            verify_no_runtime_metadata(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            verify_no_runtime_metadata(child, f"{label}[{index}]")


def verify_dependency(
    record: Mapping[str, Any], expected_path: str, expected_hash: str, label: str
) -> None:
    require(set(record) == {"path", "sha256"}, f"unexpected dependency fields at {label}")
    require(relative_path(record["path"], f"{label}.path") == expected_path, f"wrong path at {label}")
    require(record["sha256"] == expected_hash, f"wrong hash at {label}")


MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})  ([^\x00\r\n]+)$")


def verify_manifest(path: Path, expected_names: set[str]) -> dict[str, str]:
    entries: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise ReconciliationError(f"cannot read manifest {path.name}: {error}") from error
    require(bool(lines), f"empty manifest {path.name}")
    for line_number, line in enumerate(lines, start=1):
        match = MANIFEST_LINE.fullmatch(line)
        require(match is not None, f"malformed {path.name} line {line_number}")
        digest, name = match.groups()
        relative_path(name, f"{path.name}:{line_number}")
        require("/" not in name, f"manifest entry leaves packet directory: {name}")
        require(name not in entries, f"duplicate manifest entry {name}")
        candidate = path.parent / name
        require(candidate.is_file(), f"missing manifest target {name}")
        actual = sha256_file(candidate)
        require(actual == digest, f"manifest hash mismatch for {name}")
        entries[name] = digest
    require(set(entries) == expected_names, f"unexpected entry set in {path.name}")
    return entries


def authenticate_inputs(root: Path) -> dict[str, dict[str, Any]]:
    authenticated: dict[str, dict[str, Any]] = {}
    for relative, expected in sorted(PINNED_HASHES.items()):
        path = root / relative
        require(path.is_file(), f"missing pinned artifact {relative}")
        actual = sha256_file(path)
        require(actual == expected, f"pinned hash mismatch for {relative}")
        authenticated[relative] = {"bytes": path.stat().st_size, "sha256": actual}

    source_entries = verify_manifest(
        root / HOSTILE_SOURCE_MANIFEST,
        {
            "EXECUTION_COMPATIBILITY_REPAIR.md",
            "README.md",
            "SOURCE_FREEZE.json",
            "independent_joint_witness.py",
            "test_source_freeze.py",
        },
    )
    result_entries = verify_manifest(
        root / HOSTILE_RESULT_MANIFEST,
        {
            "HOSTILE_EXECUTION_RECORD.json",
            "HOSTILE_RESULT.json",
            "HOSTILE_RESULT.sha256",
            "SOURCE_FREEZE.json",
            "SOURCE_HASHES.sha256",
        },
    )
    single_entries = verify_manifest(root / HOSTILE_RESULT_SINGLE_MANIFEST, {"HOSTILE_RESULT.json"})
    require(
        source_entries["SOURCE_FREEZE.json"] == result_entries["SOURCE_FREEZE.json"],
        "source/result manifest freeze mismatch",
    )
    require(
        result_entries["HOSTILE_RESULT.json"] == single_entries["HOSTILE_RESULT.json"],
        "hostile result manifests disagree",
    )
    return authenticated


def verify_target_custody(root: Path, target: Mapping[str, Any], seal: Mapping[str, Any]) -> None:
    require(seal.get("schema") == "OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_TARGET_SEAL_V001", "wrong target seal schema")
    require(seal.get("classification") == "TARGET_OWNER_ONCE_JOINT_WITNESS_NUMERICALLY_RESOLVED__AWAITING_INDEPENDENT", "unexpected target seal classification")
    require(seal.get("passed") is True, "target seal does not report pass")
    require(seal.get("final_physical_disposition_authorized") is False, "target seal improperly authorizes final disposition")

    expected_artifacts = {
        "protocol": (PROTOCOL, PINNED_HASHES[PROTOCOL]),
        "target_source": (f"{TARGET_DIR}/target_joint_witness.py", PINNED_HASHES[f"{TARGET_DIR}/target_joint_witness.py"]),
        "target_tests": (f"{TARGET_DIR}/test_target_joint_witness.py", PINNED_HASHES[f"{TARGET_DIR}/test_target_joint_witness.py"]),
        "readme": (f"{TARGET_DIR}/README.md", PINNED_HASHES[f"{TARGET_DIR}/README.md"]),
        "historical_target": (
            "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py",
            PINNED_HASHES["DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py"],
        ),
        "target_result": (TARGET_RESULT, PINNED_HASHES[TARGET_RESULT]),
    }
    artifacts = seal.get("artifacts")
    require(isinstance(artifacts, Mapping) and set(artifacts) == set(expected_artifacts), "target seal artifact set mismatch")
    for name, (relative, digest) in expected_artifacts.items():
        entry = artifacts[name]
        require(isinstance(entry, Mapping), f"invalid target seal entry {name}")
        required_fields = {"path", "sha256", "bytes"} if name == "target_result" else {"path", "sha256"}
        require(set(entry) == required_fields, f"wrong fields in target seal entry {name}")
        verify_dependency({"path": entry["path"], "sha256": entry["sha256"]}, relative, digest, f"target seal {name}")
        if name == "target_result":
            require(integer(entry["bytes"], "target result bytes") == (root / relative).stat().st_size, "target result byte count mismatch")

    rerun = seal.get("deterministic_rerun")
    require(isinstance(rerun, Mapping), "missing target deterministic rerun")
    require(rerun.get("byte_identical") is True, "target rerun was not byte-identical")
    for key in ("primary_sha256", "rerun_sha256"):
        require(rerun.get(key) == PINNED_HASHES[TARGET_RESULT], f"target rerun hash mismatch at {key}")
    expected_bytes = (root / TARGET_RESULT).stat().st_size
    require(rerun.get("primary_bytes") == expected_bytes and rerun.get("rerun_bytes") == expected_bytes, "target rerun byte count mismatch")
    tests = seal.get("synthetic_test_evidence")
    require(isinstance(tests, Mapping), "missing target test evidence")
    require(tests.get("compile_with_warnings_as_errors") is True, "target compile evidence failed")
    require(tests.get("tests_run") == 9 and tests.get("failures") == 0 and tests.get("errors") == 0, "target sealed tests failed")

    require(target.get("schema") == "OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_TARGET_V001", "wrong target result schema")
    require(target.get("classification") == seal.get("classification"), "target result/seal classification mismatch")
    require(target.get("passed") is True, "target result does not pass")
    require(target.get("final_physical_disposition_authorized") is False, "target result improperly authorizes disposition")
    require(target.get("requires_frozen_independent_implementation_and_result") is True, "target omitted independent requirement")
    dependencies = target.get("dependencies")
    require(isinstance(dependencies, Mapping), "missing target dependencies")
    verify_dependency(dependencies["protocol"], PROTOCOL, PINNED_HASHES[PROTOCOL], "target protocol dependency")
    history = "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py"
    verify_dependency(dependencies["historical_target"], history, PINNED_HASHES[history], "target historical dependency")
    source = f"{TARGET_DIR}/target_joint_witness.py"
    verify_dependency(dependencies["target_source"], source, PINNED_HASHES[source], "target source dependency")


def verify_hostile_custody(
    root: Path,
    hostile: Mapping[str, Any],
    source_freeze: Mapping[str, Any],
    execution: Mapping[str, Any],
) -> None:
    require(source_freeze.get("schema") == "HOSTILE_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_SOURCE_FREEZE_V001", "wrong hostile source-freeze schema")
    require(source_freeze.get("disposition") == "HOSTILE_SOURCE_FROZEN_READY", "unexpected hostile source-freeze disposition")
    require(source_freeze.get("authorization_required_for_physical_seed") == "AUTHORIZE_L4_L6_L8_JOINT_WITNESS", "wrong hostile authorization token")
    require(source_freeze.get("mandatory_future_lengths") == list(MANDATORY_LENGTHS), "wrong hostile frozen length set")
    independence = source_freeze.get("independence")
    require(isinstance(independence, Mapping) and all(value is False for value in independence.values()), "hostile pre-output independence declarations fail")
    tests = source_freeze.get("source_tests")
    require(isinstance(tests, Mapping) and tests.get("count") == 10 and tests.get("result") == "PASS", "hostile frozen source tests fail")
    require(tests.get("physical_seed_output_generated") is False, "source-freeze test phase generated seed output")
    protocol = source_freeze.get("protocol")
    verify_dependency(protocol, PROTOCOL, PINNED_HASHES[PROTOCOL], "hostile frozen protocol")
    expected_files = {
        "EXECUTION_COMPATIBILITY_REPAIR.md": PINNED_HASHES[f"{HOSTILE_DIR}/EXECUTION_COMPATIBILITY_REPAIR.md"],
        "README.md": PINNED_HASHES[f"{HOSTILE_DIR}/README.md"],
        "independent_joint_witness.py": PINNED_HASHES[f"{HOSTILE_DIR}/independent_joint_witness.py"],
        "test_source_freeze.py": PINNED_HASHES[f"{HOSTILE_DIR}/test_source_freeze.py"],
    }
    require(source_freeze.get("files") == expected_files, "hostile source-freeze file map mismatch")
    repair = source_freeze.get("repair")
    require(isinstance(repair, Mapping), "missing compatibility repair record")
    require(repair.get("kind") == "BLAS_DIAGNOSTIC_REDUCTION_TO_EXPLICIT_FINITE_SUM", "unexpected compatibility repair")
    require(repair.get("changed_equations_or_parameters") is False, "compatibility repair changed frozen content")
    require(repair.get("failed_attempt_result_written") is False, "failed attempt wrote a result")
    require(repair.get("performed_before_physical_output") is True, "repair chronology failed")

    require(execution.get("schema") == "HOSTILE_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_EXECUTION_RECORD_V001", "wrong hostile execution schema")
    require(execution.get("protocol_sha256") == PINNED_HASHES[PROTOCOL], "execution protocol hash mismatch")
    source_rel = f"{HOSTILE_DIR}/independent_joint_witness.py"
    require(execution.get("source_sha256") == PINNED_HASHES[source_rel], "execution source hash mismatch")
    require(execution.get("result_sha256") == PINNED_HASHES[HOSTILE_RESULT], "execution result hash mismatch")
    execution_independence = execution.get("independence")
    require(isinstance(execution_independence, Mapping) and all(value is False for value in execution_independence.values()), "hostile execution independence declarations fail")
    rerun = execution.get("deterministic_rerun")
    require(isinstance(rerun, Mapping) and rerun.get("byte_identity") is True, "hostile rerun was not byte-identical")
    require(rerun.get("result_sha256") == PINNED_HASHES[HOSTILE_RESULT] and rerun.get("rerun_sha256") == PINNED_HASHES[HOSTILE_RESULT], "hostile rerun hashes mismatch")
    require(rerun.get("size_bytes_each") == (root / HOSTILE_RESULT).stat().st_size, "hostile rerun byte count mismatch")
    execution_tests = execution.get("source_tests")
    require(isinstance(execution_tests, Mapping) and execution_tests.get("count") == 10 and execution_tests.get("result") == "PASS", "hostile execution test evidence fails")
    classification = execution.get("classification")
    require(isinstance(classification, Mapping), "missing hostile execution classification")
    require(classification.get("hostile_internal_conditions_pass") is True, "hostile execution conditions did not pass")
    require(classification.get("final_protocol_classification") == "PENDING_SEPARATE_TARGET_ADJUDICATION", "hostile pre-adjudication boundary violated")
    require(classification.get("standalone_disposition") == "HOSTILE_SEED_CALCULATION_COMPLETE__TARGET_ADJUDICATION_REQUIRED", "wrong hostile standalone disposition")
    execution_repair = execution.get("compatibility_repair")
    require(isinstance(execution_repair, Mapping), "missing hostile execution repair custody")
    require(execution_repair.get("kind") == "BLAS_DIAGNOSTIC_REDUCTION_TO_EXPLICIT_FINITE_SUM", "execution repair kind mismatch")
    require(execution_repair.get("changed_equations_or_parameters") is False, "execution repair changed equations or parameters")
    require(execution_repair.get("failed_attempt_result_written") is False, "execution repair records a failed-attempt result")
    require(execution_repair.get("source_refrozen_before_completed_execution") is True, "hostile source was not refrozen before execution")

    require(hostile.get("schema") == "HOSTILE_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001", "wrong hostile result schema")
    require(hostile.get("disposition") == "HOSTILE_SEED_CALCULATION_COMPLETE__TARGET_ADJUDICATION_REQUIRED", "wrong hostile result disposition")
    hostile_independence = hostile.get("independence")
    require(isinstance(hostile_independence, Mapping) and all(value is False for value in hostile_independence.values()), "hostile result independence declarations fail")
    dependencies = hostile.get("dependencies")
    require(isinstance(dependencies, Mapping), "missing hostile dependencies")
    verify_dependency(dependencies["frozen_witness_protocol"], PROTOCOL, PINNED_HASHES[PROTOCOL], "hostile protocol dependency")
    history_protocol = "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md"
    verify_dependency(dependencies["historical_accumulation_protocol"], history_protocol, PINNED_HASHES[history_protocol], "hostile history dependency")
    prefix_protocol = "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/PROTOCOL.md"
    verify_dependency(dependencies["historical_prefix_protocol"], prefix_protocol, PINNED_HASHES[prefix_protocol], "hostile prefix dependency")
    verify_dependency(dependencies["hostile_source"], source_rel, PINNED_HASHES[source_rel], "hostile source dependency")


def verify_parameters(target: Mapping[str, Any], hostile: Mapping[str, Any]) -> None:
    expected_target = {
        "coarse_steps": COARSE_STEPS,
        "dwell": DWELL,
        "fine_steps": FINE_STEPS,
        "mandatory_lengths": list(MANDATORY_LENGTHS),
        "phi": PHI,
        "taylor_order": TAYLOR_ORDER,
        "tolerances": {
            "charge": TOLERANCES["charge"],
            "coarse_fine": TOLERANCES["coarse_fine"],
            "l4_exhaustive": TOLERANCES["l4_exhaustive"],
            "marginal": TOLERANCES["probability_marginal"],
            "norm": TOLERANCES["norm_content"],
            "sham": TOLERANCES["sham"],
            "shuffle": TOLERANCES["shuffle"],
        },
    }
    expected_hostile = {
        "coarse_substeps": COARSE_STEPS,
        "dwell": DWELL,
        "fine_substeps": FINE_STEPS,
        "l4_exhaustive_tolerance": TOLERANCES["l4_exhaustive"],
        "lengths": list(MANDATORY_LENGTHS),
        "marginal_tolerance": TOLERANCES["probability_marginal"],
        "norm_content_tolerance": TOLERANCES["norm_content"],
        "phi": PHI,
        "sham_tolerance": TOLERANCES["sham"],
        "shuffle_tolerance": TOLERANCES["shuffle"],
        "target_independent_tolerance": TOLERANCES["target_independent"],
        "taylor_order": TAYLOR_ORDER,
    }
    require(target.get("parameters") == expected_target, "target parameters differ from frozen protocol")
    require(hostile.get("parameters") == expected_hostile, "hostile parameters differ from frozen protocol")


def target_evaluations(run: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    events = run.get("events")
    require(isinstance(events, list), "target run events missing")
    output: list[Mapping[str, Any]] = []
    for event in events:
        require(isinstance(event, Mapping), "invalid target event")
        for key in ("before_admission", "after_admission", "after_transport"):
            evaluation = event.get(key)
            require(isinstance(evaluation, Mapping), f"missing target {key}")
            output.append(evaluation)
    return output


def verify_target_schedule(run: Mapping[str, Any], length: int, steps: int) -> None:
    require(run.get("L") == length and run.get("steps") == steps, "target run length/substep mismatch")
    events = run.get("events")
    require(isinstance(events, list) and len(events) == length, "target event count mismatch")
    for index, event in enumerate(events):
        require(event.get("event") == index + 1 and event.get("zero_based_event") == index, "target event order mismatch")
    require(run.get("terminal") == events[-1].get("after_transport"), "target primary terminal checkpoint mismatch")


def target_terminal_disagreement(left: Mapping[str, Any], right: Mapping[str, Any]) -> float:
    values: list[float] = []
    for key in ("w", "w_sham", "D"):
        values.append(abs(numeric(left["registered"][key], f"target coarse {key}") - numeric(right["registered"][key], f"target fine {key}")))
    require(set(left["q_contributions"]) == set(right["q_contributions"]), "target coarse/fine q sets mismatch")
    for q in sorted(left["q_contributions"], key=int):
        for key in ("p_q", "D_q"):
            values.append(abs(numeric(left["q_contributions"][q][key], f"target coarse q{q} {key}") - numeric(right["q_contributions"][q][key], f"target fine q{q} {key}")))
    return max(values, default=0.0)


def target_maximum_residual(runs: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> float:
    values = [
        abs(numeric(evaluation["residuals"][key], f"target residual {key}"))
        for run in runs
        for evaluation in target_evaluations(run)
        for key in keys
        if key in evaluation["residuals"]
    ]
    return max(values, default=0.0)


def verify_witness_identity(w: float, sham: float, witness: float, label: str) -> None:
    require(abs((w - sham) - witness) <= IDENTITY_TOLERANCE, f"D=w-w_sham identity fails at {label}")


def verify_target_terminal(terminal: Mapping[str, Any], length: int, label: str) -> None:
    registered = terminal.get("registered")
    contributions = terminal.get("q_contributions")
    require(isinstance(registered, Mapping) and isinstance(contributions, Mapping), f"missing target terminal data at {label}")
    require(set(contributions) == {str(q) for q in range(length + 1)}, f"target q set mismatch at {label}")
    w = numeric(registered["w"], f"{label}.w")
    sham = numeric(registered["w_sham"], f"{label}.w_sham")
    witness = numeric(registered["D"], f"{label}.D")
    verify_witness_identity(w, sham, witness, label)
    require(abs(sum(numeric(contributions[str(q)]["p_q"], f"{label}.p{q}") for q in range(length + 1)) - numeric(registered["probability"], f"{label}.probability")) <= IDENTITY_TOLERANCE, f"target sector probabilities do not sum at {label}")
    for key, public in (("w_q", "w"), ("w_sham_q", "w_sham"), ("D_q", "D"), ("w_shuffle_q", "w_shuffle")):
        total = sum(numeric(contributions[str(q)][key], f"{label}.q{q}.{key}") for q in range(length + 1))
        require(abs(total - numeric(registered[public], f"{label}.{public}")) <= IDENTITY_TOLERANCE, f"target sector {key} sum fails at {label}")
    negative = terminal.get("negative_controls")
    require(isinstance(negative, Mapping), f"missing target negative controls at {label}")
    require(abs(numeric(negative["sham_replacement_D"], f"{label}.sham replacement")) <= TOLERANCES["sham"], f"target sham replacement fails at {label}")
    require(abs(numeric(negative["sham_replacement_max_sector_D"], f"{label}.sham sector replacement")) <= TOLERANCES["sham"], f"target sham sector replacement fails at {label}")
    require(abs(numeric(negative["shuffle_replacement_w"], f"{label}.shuffle replacement")) <= TOLERANCES["shuffle"], f"target shuffle replacement fails at {label}")


def validate_target_row(row: Mapping[str, Any]) -> dict[str, Any]:
    length = integer(row.get("L"), "target row L")
    coarse = row.get("coarse")
    fine = row.get("fine")
    require(isinstance(coarse, Mapping) and isinstance(fine, Mapping), f"target runs missing at L{length}")
    verify_target_schedule(coarse, length, COARSE_STEPS)
    verify_target_schedule(fine, length, FINE_STEPS)
    verify_target_terminal(coarse["terminal"], length, f"target L{length} coarse terminal")
    verify_target_terminal(fine["terminal"], length, f"target L{length} fine terminal")

    coarse_fine = target_terminal_disagreement(coarse["terminal"], fine["terminal"])
    row_column = max(
        numeric(coarse["terminal"]["residuals"]["row_column_d_inputs"], f"target L{length} coarse row-column"),
        numeric(fine["terminal"]["residuals"]["row_column_d_inputs"], f"target L{length} fine row-column"),
    )
    diagnostic_row_column = target_maximum_residual((coarse, fine), ("row_column_accumulator",))
    target_d = max(coarse_fine, row_column)
    norm_content = target_maximum_residual((coarse, fine), ("state_norm", "total_content"))
    probability_marginal = target_maximum_residual((coarse, fine), ("probability_normalization", "marginal_reconstruction"))
    charge = target_maximum_residual((coarse, fine), ("sharp_sector_QS_minus_QC",))
    shuffle = target_maximum_residual((coarse, fine), ("shuffle_expectation", "l4_permutation_shuffle"))
    sham = target_maximum_residual((coarse, fine), ("sham_self_covariance",))
    l4_exhaustive = target_maximum_residual((coarse, fine), ("l4_exhaustive_streamed", "l4_permutation_shuffle")) if length == 4 else 0.0
    r_l = max(norm_content, probability_marginal, charge)
    tau_target = max(1.0e-9, 50.0 * target_d, 100.0 * r_l)
    derived = {
        "target_coarse_fine_disagreement": coarse_fine,
        "row_column_disagreement": row_column,
        "maximum_diagnostic_row_column_disagreement": diagnostic_row_column,
        "target_d_component": target_d,
        "r_L": r_l,
        "tau_L_target_component": tau_target,
        "maximum_norm_total_content_residual": norm_content,
        "maximum_probability_marginal_residual": probability_marginal,
        "maximum_charge_residual": charge,
        "maximum_shuffle_residual": shuffle,
        "maximum_sham_residual": sham,
        "maximum_l4_exhaustive_residual": l4_exhaustive,
    }
    for key, value in derived.items():
        close(row.get(key), value, f"target L{length} reported {key}")

    expected_conditions = {
        "target_coarse_fine": coarse_fine <= TOLERANCES["coarse_fine"],
        "row_column_accumulators": row_column <= TOLERANCES["coarse_fine"],
        "norm_and_total_content": norm_content <= TOLERANCES["norm_content"],
        "probability_and_marginals": probability_marginal <= TOLERANCES["probability_marginal"],
        "sharp_sector_QS_minus_QC": charge <= TOLERANCES["charge"],
        "shuffle_control": shuffle <= TOLERANCES["shuffle"],
        "sham_control": sham <= TOLERANCES["sham"],
        "l4_exhaustive": length != 4 or l4_exhaustive <= TOLERANCES["l4_exhaustive"],
    }
    require(row.get("conditions") == expected_conditions, f"target L{length} condition report mismatch")
    require(row.get("passed") is all(expected_conditions.values()), f"target L{length} pass flag mismatch")

    if length == 4:
        for resolution, run in (("coarse", coarse), ("fine", fine)):
            exhaustive = run["terminal"].get("l4_exhaustive")
            require(isinstance(exhaustive, Mapping), f"missing target L4 {resolution} exhaustive control")
            require(exhaustive.get("permutation_count") == math.factorial(4), f"target L4 {resolution} did not enumerate 24 permutations")
            require(abs(numeric(exhaustive["streamed_agreement"], f"target L4 {resolution} streamed agreement")) <= TOLERANCES["l4_exhaustive"], f"target L4 {resolution} direct/stream agreement fails")
            require(abs(numeric(exhaustive["w_shuffle"], f"target L4 {resolution} exhaustive shuffle")) <= TOLERANCES["shuffle"], f"target L4 {resolution} exhaustive shuffle fails")

    return {
        "length": length,
        "coarse_fine": coarse_fine,
        "row_column": row_column,
        "diagnostic_row_column": diagnostic_row_column,
        "r_L": r_l,
        "controls_pass": all(expected_conditions.values()),
        "fine_terminal": fine["terminal"],
    }


def flatten_numeric(value: Any, prefix: str = "") -> dict[str, float]:
    output: dict[str, float] = {}
    if isinstance(value, Mapping):
        for key in sorted(value):
            child = f"{prefix}.{key}" if prefix else str(key)
            output.update(flatten_numeric(value[key], child))
    elif isinstance(value, list):
        for index, child_value in enumerate(value):
            output.update(flatten_numeric(child_value, f"{prefix}[{index}]"))
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        output[prefix] = numeric(value, prefix)
    return output


def hostile_resolution_disagreement(coarse: Mapping[str, Any], fine: Mapping[str, Any]) -> float:
    left = flatten_numeric(coarse["checkpoints"])
    right = flatten_numeric(fine["checkpoints"])
    require(set(left) == set(right), "hostile coarse/fine checkpoint schema mismatch")
    return max((abs(left[key] - right[key]) for key in left), default=0.0)


def hostile_max_checkpoint(run: Mapping[str, Any], key: str) -> float:
    return max(
        (abs(numeric(checkpoint["witness"][key], f"hostile checkpoint {key}")) for checkpoint in run["checkpoints"]),
        default=0.0,
    )


def hostile_terminal_control(run: Mapping[str, Any], key: str) -> float:
    value = run["checkpoints"][-1]["witness"]["controls"][key]
    return 0.0 if value is None else abs(numeric(value, f"hostile terminal {key}"))


def hostile_max_control(run: Mapping[str, Any], key: str) -> float:
    values = []
    for checkpoint in run["checkpoints"]:
        value = checkpoint["witness"]["controls"][key]
        if value is not None:
            values.append(abs(numeric(value, f"hostile checkpoint control {key}")))
    return max(values, default=0.0)


def hostile_internal_residual(run: Mapping[str, Any]) -> float:
    values = [
        abs(numeric(run["maximum_absolute_norm_error"], "hostile maximum norm error")),
        abs(numeric(run["maximum_transport_norm_drift"], "hostile maximum norm drift")),
    ]
    for checkpoint in run["checkpoints"]:
        witness = checkpoint["witness"]
        for key in (
            "marginal_reconstruction_residual",
            "normalization_residual",
            "q_identity_residual",
            "total_content_residual",
            "row_column_disagreement",
        ):
            values.append(abs(numeric(witness[key], f"hostile {key}")))
        controls = witness["controls"]
        values.append(abs(numeric(controls["analytic_shuffle_expectation"], "hostile shuffle control")))
        values.append(abs(numeric(controls["sham_self_covariance_residual"], "hostile sham control")))
        for key in ("exhaustive_direct_residual", "exhaustive_shuffle_expectation"):
            if controls[key] is not None:
                values.append(abs(numeric(controls[key], f"hostile {key}")))
    return max(values, default=0.0)


def verify_hostile_schedule(run: Mapping[str, Any], length: int, substeps: int) -> None:
    require(run.get("length") == length and run.get("substeps") == substeps, "hostile run length/substep mismatch")
    checkpoints = run.get("checkpoints")
    require(isinstance(checkpoints, list) and len(checkpoints) == 3 * length, "hostile checkpoint count mismatch")
    expected = [(event, stage) for event in range(length) for stage in ("before_admission", "after_admission", "after_transport")]
    actual = [(checkpoint.get("event"), checkpoint.get("stage")) for checkpoint in checkpoints]
    require(actual == expected, "hostile event/checkpoint order mismatch")


def verify_hostile_terminal(terminal: Mapping[str, Any], length: int, label: str) -> None:
    weights = terminal.get("sector_weights")
    row = terminal.get("row_accumulator")
    column = terminal.get("column_accumulator")
    require(isinstance(weights, list) and len(weights) == length + 1, f"hostile sector weights missing at {label}")
    require(isinstance(row, Mapping) and isinstance(column, Mapping), f"hostile accumulators missing at {label}")
    for accumulator_name, accumulator in (("row", row), ("column", column)):
        for key in ("q_observed", "q_sham", "q_witness"):
            require(isinstance(accumulator.get(key), list) and len(accumulator[key]) == length + 1, f"hostile {accumulator_name} {key} length mismatch at {label}")
        verify_witness_identity(
            numeric(accumulator["observed"], f"{label}.{accumulator_name}.observed"),
            numeric(accumulator["sham"], f"{label}.{accumulator_name}.sham"),
            numeric(accumulator["witness"], f"{label}.{accumulator_name}.witness"),
            f"{label}.{accumulator_name}",
        )
    w = numeric(terminal["w_L"], f"{label}.w_L")
    sham = numeric(terminal["w_L_sham"], f"{label}.w_L_sham")
    witness = numeric(terminal["D_L"], f"{label}.D_L")
    verify_witness_identity(w, sham, witness, label)
    close(w, row["observed"], f"{label} row observed", IDENTITY_TOLERANCE)
    close(sham, row["sham"], f"{label} row sham", IDENTITY_TOLERANCE)
    close(witness, row["witness"], f"{label} row witness", IDENTITY_TOLERANCE)
    require(abs(sum(numeric(value, f"{label}.weight") for value in weights) - 1.0) <= TOLERANCES["probability_marginal"], f"hostile sector normalization fails at {label}")
    controls = terminal.get("controls")
    require(isinstance(controls, Mapping), f"hostile controls missing at {label}")
    require(abs(numeric(terminal["w_L_shuffle"], f"{label}.w_L_shuffle")) <= TOLERANCES["shuffle"], f"hostile shuffle replacement fails at {label}")
    require(abs(numeric(controls["analytic_shuffle_expectation"], f"{label}.analytic shuffle")) <= TOLERANCES["shuffle"], f"hostile analytic shuffle fails at {label}")
    require(abs(numeric(controls["sham_self_covariance_residual"], f"{label}.sham self residual")) <= TOLERANCES["sham"], f"hostile sham replacement fails at {label}")


def validate_hostile_row(row: Mapping[str, Any]) -> dict[str, Any]:
    length = integer(row.get("length"), "hostile row length")
    coarse = row.get("coarse")
    fine = row.get("fine")
    require(isinstance(coarse, Mapping) and isinstance(fine, Mapping), f"hostile runs missing at L{length}")
    verify_hostile_schedule(coarse, length, COARSE_STEPS)
    verify_hostile_schedule(fine, length, FINE_STEPS)
    coarse_terminal = coarse["checkpoints"][-1]["witness"]
    fine_terminal = fine["checkpoints"][-1]["witness"]
    require(row.get("primary_fine_terminal") == fine_terminal, f"hostile L{length} primary terminal mismatch")
    verify_hostile_terminal(coarse_terminal, length, f"hostile L{length} coarse terminal")
    verify_hostile_terminal(fine_terminal, length, f"hostile L{length} fine terminal")

    coarse_fine = hostile_resolution_disagreement(coarse, fine)
    internal_residual = max(hostile_internal_residual(coarse), hostile_internal_residual(fine))
    internal_tau = max(1.0e-9, 50.0 * coarse_fine, 100.0 * internal_residual)
    close(row.get("internal_coarse_fine_disagreement"), coarse_fine, f"hostile L{length} coarse/fine report")
    close(row.get("internal_residual"), internal_residual, f"hostile L{length} residual report")
    close(row.get("internal_tau_lower_bound"), internal_tau, f"hostile L{length} tau report")
    expected_conditions = {
        "coarse_fine_within_1e_8": coarse_fine <= TOLERANCES["target_independent"],
        "l4_exhaustive_direct_within_1e_12": length != 4 or max(hostile_terminal_control(coarse, "exhaustive_direct_residual"), hostile_terminal_control(fine, "exhaustive_direct_residual")) <= TOLERANCES["l4_exhaustive"],
        "l4_exhaustive_shuffle_within_1e_12": length != 4 or max(hostile_terminal_control(coarse, "exhaustive_shuffle_expectation"), hostile_terminal_control(fine, "exhaustive_shuffle_expectation")) <= TOLERANCES["shuffle"],
        "marginals_within_1e_10": max(hostile_max_checkpoint(coarse, "marginal_reconstruction_residual"), hostile_max_checkpoint(fine, "marginal_reconstruction_residual")) <= TOLERANCES["probability_marginal"],
        "norm_within_1e_10": max(abs(numeric(coarse["maximum_absolute_norm_error"], "hostile coarse norm")), abs(numeric(fine["maximum_absolute_norm_error"], "hostile fine norm"))) <= TOLERANCES["norm_content"],
        "normalization_within_1e_10": max(hostile_max_checkpoint(coarse, "normalization_residual"), hostile_max_checkpoint(fine, "normalization_residual")) <= TOLERANCES["probability_marginal"],
        "q_identity_within_1e_10": max(hostile_max_checkpoint(coarse, "q_identity_residual"), hostile_max_checkpoint(fine, "q_identity_residual"), hostile_max_checkpoint(coarse, "total_content_residual"), hostile_max_checkpoint(fine, "total_content_residual")) <= TOLERANCES["norm_content"],
        "sham_negative_control_within_1e_12": max(hostile_terminal_control(coarse, "sham_self_covariance_residual"), hostile_terminal_control(fine, "sham_self_covariance_residual")) <= TOLERANCES["sham"],
    }
    require(row.get("internal_conditions") == expected_conditions, f"hostile L{length} condition report mismatch")
    require(row.get("internal_conditions_pass") is all(expected_conditions.values()), f"hostile L{length} pass flag mismatch")
    require(row.get("target_comparison") == "PENDING_SEPARATE_ADJUDICATION", f"hostile L{length} target boundary violated")
    if length == 4:
        for resolution, terminal in (("coarse", coarse_terminal), ("fine", fine_terminal)):
            controls = terminal["controls"]
            require(isinstance(controls.get("exhaustive_direct"), Mapping), f"missing hostile L4 {resolution} exhaustive direct sum")
            require(abs(numeric(controls["exhaustive_direct_residual"], f"hostile L4 {resolution} direct residual")) <= TOLERANCES["l4_exhaustive"], f"hostile L4 {resolution} direct residual fails")
            require(abs(numeric(controls["exhaustive_shuffle_expectation"], f"hostile L4 {resolution} shuffle")) <= TOLERANCES["shuffle"], f"hostile L4 {resolution} exhaustive shuffle fails")

    protocol_r = max(
        abs(numeric(coarse["maximum_absolute_norm_error"], "hostile coarse norm")),
        abs(numeric(fine["maximum_absolute_norm_error"], "hostile fine norm")),
        abs(numeric(coarse["maximum_transport_norm_drift"], "hostile coarse drift")),
        abs(numeric(fine["maximum_transport_norm_drift"], "hostile fine drift")),
        hostile_max_checkpoint(coarse, "total_content_residual"),
        hostile_max_checkpoint(fine, "total_content_residual"),
        hostile_max_checkpoint(coarse, "normalization_residual"),
        hostile_max_checkpoint(fine, "normalization_residual"),
        hostile_max_checkpoint(coarse, "marginal_reconstruction_residual"),
        hostile_max_checkpoint(fine, "marginal_reconstruction_residual"),
        hostile_max_checkpoint(coarse, "q_identity_residual"),
        hostile_max_checkpoint(fine, "q_identity_residual"),
    )
    row_column = max(
        abs(numeric(coarse_terminal["row_column_disagreement"], f"hostile L{length} coarse row-column")),
        abs(numeric(fine_terminal["row_column_disagreement"], f"hostile L{length} fine row-column")),
    )
    explicit_controls_pass = (
        abs(numeric(coarse_terminal["w_L_shuffle"], "hostile coarse shuffle")) <= TOLERANCES["shuffle"]
        and abs(numeric(fine_terminal["w_L_shuffle"], "hostile fine shuffle")) <= TOLERANCES["shuffle"]
        and max(hostile_max_control(coarse, "analytic_shuffle_expectation"), hostile_max_control(fine, "analytic_shuffle_expectation")) <= TOLERANCES["shuffle"]
        and max(hostile_max_control(coarse, "sham_self_covariance_residual"), hostile_max_control(fine, "sham_self_covariance_residual")) <= TOLERANCES["sham"]
        and max(abs(numeric(coarse["maximum_transport_norm_drift"], "hostile coarse norm drift")), abs(numeric(fine["maximum_transport_norm_drift"], "hostile fine norm drift"))) <= TOLERANCES["norm_content"]
        and row_column <= TOLERANCES["target_independent"]
    )
    return {
        "length": length,
        "coarse_fine": coarse_fine,
        "row_column": row_column,
        "r_L": protocol_r,
        "controls_pass": all(expected_conditions.values()) and explicit_controls_pass,
        "fine_terminal": fine_terminal,
    }


def cross_compare(
    target_terminal: Mapping[str, Any], hostile_terminal: Mapping[str, Any], length: int
) -> tuple[float, str, dict[str, Any]]:
    comparisons: dict[str, Any] = {}
    largest = 0.0
    largest_label = "none"

    def add(label: str, target_value: Any, hostile_value: Any) -> None:
        nonlocal largest, largest_label
        left = numeric(target_value, f"target {label}")
        right = numeric(hostile_value, f"hostile {label}")
        difference = abs(left - right)
        comparisons[label] = {
            "absolute_disagreement": difference,
            "hostile": right,
            "target": left,
        }
        if difference > largest:
            largest = difference
            largest_label = label

    registered = target_terminal["registered"]
    add("w_L", registered["w"], hostile_terminal["w_L"])
    add("w_L_sham", registered["w_sham"], hostile_terminal["w_L_sham"])
    add("D_L", registered["D"], hostile_terminal["D_L"])
    for q in range(length + 1):
        contribution = target_terminal["q_contributions"][str(q)]
        add(f"q_{q}_D", contribution["D_q"], hostile_terminal["row_accumulator"]["q_witness"][q])
        add(f"q_{q}_p", contribution["p_q"], hostile_terminal["sector_weights"][q])
    return largest, largest_label, comparisons


def verify_seal_and_execution_summaries(
    target_seal: Mapping[str, Any],
    target_rows: Mapping[int, Mapping[str, Any]],
    execution: Mapping[str, Any],
    hostile_rows_raw: Sequence[Mapping[str, Any]],
) -> None:
    target_summary = target_seal.get("terminal_target_summary")
    require(isinstance(target_summary, Mapping), "missing target seal terminal summary")
    require(set(target_summary) == {f"L{length}" for length in MANDATORY_LENGTHS}, "target seal summary size set mismatch")
    for length in MANDATORY_LENGTHS:
        summary = target_summary[f"L{length}"]
        row = target_rows[length]
        terminal = row["fine_terminal"]
        expected = {
            "w": terminal["registered"]["w"],
            "w_sham": terminal["registered"]["w_sham"],
            "D": terminal["registered"]["D"],
            "w_shuffle": terminal["registered"]["w_shuffle"],
            "target_d_component": max(row["coarse_fine"], row["row_column"]),
            "r_L": row["r_L"],
            "tau_L_target_component": max(
                1.0e-9,
                50.0 * max(row["coarse_fine"], row["row_column"]),
                100.0 * row["r_L"],
            ),
            "sham_replacement_D": terminal["negative_controls"]["sham_replacement_D"],
            "shuffle_replacement_w": terminal["negative_controls"]["shuffle_replacement_w"],
        }
        require(summary.get("all_target_conditions_passed") is True, f"target seal L{length} condition summary fails")
        for key, value in expected.items():
            close(summary.get(key), value, f"target seal L{length} {key}")

    sizes = execution.get("sizes")
    require(isinstance(sizes, list) and [row.get("length") for row in sizes] == list(MANDATORY_LENGTHS), "hostile execution size summary mismatch")
    hostile_by_length = {row["length"]: row for row in hostile_rows_raw}
    for summary in sizes:
        length = summary["length"]
        row = hostile_by_length[length]
        d_value = row["primary_fine_terminal"]["D_L"]
        tau = row["internal_tau_lower_bound"]
        close(summary.get("D_L"), d_value, f"hostile execution L{length} D")
        close(summary.get("internal_tau_lower_bound"), tau, f"hostile execution L{length} tau")
        close(summary.get("ratio"), abs(numeric(d_value, "hostile summary D")) / numeric(tau, "hostile summary tau"), f"hostile execution L{length} ratio", 1.0e-9)


def protocol_classification(all_conditions_pass: bool, statistic: float | None) -> str:
    if not all_conditions_pass or statistic is None or not math.isfinite(statistic):
        return UNRESOLVED
    return RESOLVED if statistic > 1.0 else FALSIFIED


def reconcile(root: Path) -> dict[str, Any]:
    root = root.resolve()
    authenticated = authenticate_inputs(root)
    target = strict_json(root / TARGET_RESULT)
    target_seal = strict_json(root / TARGET_SEAL)
    hostile = strict_json(root / HOSTILE_RESULT)
    source_freeze = strict_json(root / HOSTILE_SOURCE_FREEZE)
    execution = strict_json(root / HOSTILE_EXECUTION)
    for name, record in (("target result", target), ("hostile result", hostile)):
        require(isinstance(record, Mapping), f"{name} is not an object")
        verify_no_runtime_metadata(record, name)
    verify_target_custody(root, target, target_seal)
    verify_hostile_custody(root, hostile, source_freeze, execution)
    verify_parameters(target, hostile)

    target_rows_raw = target.get("rows")
    hostile_rows_raw = hostile.get("results")
    require(isinstance(target_rows_raw, list) and isinstance(hostile_rows_raw, list), "result rows missing")
    require([row.get("L") for row in target_rows_raw] == list(MANDATORY_LENGTHS), "target mandatory length sequence mismatch")
    require([row.get("length") for row in hostile_rows_raw] == list(MANDATORY_LENGTHS), "hostile mandatory length sequence mismatch")
    target_rows = {row["L"]: validate_target_row(row) for row in target_rows_raw}
    hostile_rows = {row["length"]: validate_hostile_row(row) for row in hostile_rows_raw}
    verify_seal_and_execution_summaries(
        target_seal, target_rows, execution, hostile_rows_raw
    )

    per_size: list[dict[str, Any]] = []
    all_conditions = True
    for length in MANDATORY_LENGTHS:
        target_row = target_rows[length]
        hostile_row = hostile_rows[length]
        cross_max, cross_label, comparisons = cross_compare(
            target_row["fine_terminal"], hostile_row["fine_terminal"], length
        )
        cross_pass = cross_max <= TOLERANCES["target_independent"]
        row_column = max(target_row["row_column"], hostile_row["row_column"])
        d_l = max(target_row["coarse_fine"], cross_max, row_column)
        r_l = max(target_row["r_L"], hostile_row["r_L"])
        tau_l = max(1.0e-9, 50.0 * d_l, 100.0 * r_l)
        d_value = numeric(target_row["fine_terminal"]["registered"]["D"], f"target L{length} D")
        ratio = abs(d_value) / tau_l
        size_conditions = {
            "hostile_internal_and_control_conditions": bool(hostile_row["controls_pass"]),
            "row_column_agreement_within_1e_8": row_column <= TOLERANCES["target_independent"],
            "target_hostile_agreement_within_1e_8": cross_pass,
            "target_internal_and_control_conditions": bool(target_row["controls_pass"]),
        }
        size_pass = all(size_conditions.values())
        all_conditions = all_conditions and size_pass
        per_size.append(
            {
                "D_L": d_value,
                "T_L": ratio,
                "conditions": size_conditions,
                "d_L": d_l,
                "d_components": {
                    "row_column": row_column,
                    "target_64_vs_128": target_row["coarse_fine"],
                    "target_vs_independent": cross_max,
                    "target_vs_independent_largest_field": cross_label,
                },
                "length": length,
                "passed": size_pass,
                "r_L": r_l,
                "r_components": {
                    "hostile": hostile_row["r_L"],
                    "target": target_row["r_L"],
                },
                "target_hostile_comparisons": comparisons,
                "tau_L": tau_l,
                "w_L": numeric(target_row["fine_terminal"]["registered"]["w"], f"target L{length} w"),
                "w_L_sham": numeric(target_row["fine_terminal"]["registered"]["w_sham"], f"target L{length} sham"),
                "w_L_shuffle": numeric(target_row["fine_terminal"]["registered"]["w_shuffle"], f"target L{length} shuffle"),
            }
        )

    statistic = min(row["T_L"] for row in per_size)
    classification = protocol_classification(all_conditions, statistic)
    require(classification == RESOLVED, "sealed records do not produce the expected resolved classification")
    execution_statistic = numeric(execution["classification"]["hostile_internal_statistic"], "execution hostile statistic")
    require(abs(execution_statistic - min(abs(numeric(row["primary_fine_terminal"]["D_L"], "hostile D")) / numeric(row["internal_tau_lower_bound"], "hostile tau") for row in hostile_rows_raw)) <= 1.0e-9, "hostile execution statistic mismatch")

    result = {
        "all_numerical_and_control_conditions_passed": all_conditions,
        "authenticated_inputs": authenticated,
        "custody": {
            "hostile_deterministic_rerun_byte_identical": True,
            "hostile_result_and_manifests_authenticated": True,
            "hostile_source_frozen_before_result_and_authenticated": True,
            "protocol_sha256": PINNED_HASHES[PROTOCOL],
            "target_deterministic_rerun_byte_identical": True,
            "target_result_and_seal_authenticated": True,
        },
        "held_out_L10_L12": {
            "computed_or_opened_by_reconciliation": False,
            "disposition": "NOT_ADJUDICATED",
            "resource_gate_evaluated_by_reconciliation": False,
            "seed_prerequisites_1_through_3_satisfied": True,
        },
        "parameters": {
            "coarse_substeps": COARSE_STEPS,
            "dwell": DWELL,
            "fine_substeps": FINE_STEPS,
            "mandatory_lengths": list(MANDATORY_LENGTHS),
            "phi": PHI,
            "taylor_order": TAYLOR_ORDER,
            "tolerances": TOLERANCES,
        },
        "passed": classification == RESOLVED,
        "per_size": per_size,
        "protocol_classification": classification,
        "reconciliation_disposition": "SEALED_TARGET_HOSTILE_RECONCILIATION_COMPLETE",
        "schema": SCHEMA,
        "scientific_scope": {
            "established": [
                "At L=4,6,8, the frozen owner-once terminal state has a resolved value of the preregistered centered lineage--carrier conditional-covariance witness.",
                "The value is absent from the unconditional carrier marginal and is removed by the sector-matched sham and within-q lineage-shuffle controls.",
                "The conclusion is finite, terminal, same-parent, and specific to the frozen observable and first-pass schedule.",
            ],
            "not_established": [
                "a dynamical readout of the lineage register or future back-reaction",
                "persistence after a revisit",
                "entanglement",
                "held-out L10 or L12",
                "an all-L, thermodynamic, or continuum limit",
                "the ARGER Gate, Record--Geometry Realization Law, alpha, GL6T, spacetime, metric response, Einstein--Hilbert dynamics, or gravity",
            ],
        },
        "T_4_8": statistic,
    }
    verify_finite(result, "reconciliation result")
    return result


def deterministic_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def unresolved_record(error: Exception) -> dict[str, Any]:
    return {
        "error": {"message": str(error), "type": type(error).__name__},
        "passed": False,
        "protocol_classification": UNRESOLVED,
        "reconciliation_disposition": "FAIL_CLOSED",
        "schema": SCHEMA,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="audited-386ee2c root")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="deterministic JSON output")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    protected = {(args.root.resolve() / relative) for relative in PINNED_HASHES}
    output = args.output.resolve()
    if output in protected:
        print("refusing to overwrite a sealed input", file=sys.stderr)
        return 2
    try:
        result = reconcile(args.root)
        status = 0
    except Exception as error:  # The CLI must never turn an audit failure into a pass.
        result = unresolved_record(error)
        status = 1
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(deterministic_json(result), encoding="utf-8")
    print(result["protocol_classification"])
    return status


if __name__ == "__main__":
    raise SystemExit(main())
