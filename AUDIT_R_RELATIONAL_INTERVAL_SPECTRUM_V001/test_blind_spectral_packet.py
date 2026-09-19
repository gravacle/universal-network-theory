#!/usr/bin/env python3
"""Non-physical self-tests for the independently frozen blind method."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

import independent_spectrum_engine as engine


PACKET = Path(__file__).resolve().parent
REPO = PACKET.parent
STATIC_FREEZE = PACKET / "PRE_OUTPUT_METHOD_FREEZE.json"
FILES = (
    "METHODOLOGY.md",
    "independent_spectrum_engine.py",
    "build_blind_freeze.py",
    "test_blind_spectral_packet.py",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def syntax_test() -> dict[str, object]:
    parsed = []
    for name in FILES:
        path = PACKET / name
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            parsed.append(name)
    return {"status": "PASS", "parsed": parsed}


def freeze_test() -> dict[str, object]:
    freeze = json.loads(STATIC_FREEZE.read_text(encoding="utf-8"))
    require(freeze["status"] == "BLIND_METHOD_AND_CODE_FROZEN__AWAITING_MANIFEST", "bad static freeze")
    for name in FILES:
        require(freeze["files"][name] == sha256(PACKET / name), f"static freeze mismatch: {name}")
    return {"status": "PASS", "freeze_sha256": sha256(STATIC_FREEZE)}


def synthetic_test() -> dict[str, object]:
    edges = engine.prism_edges(4)
    require(len(edges) == 12, "L4 prism edge census")
    degree = [0] * 8
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    require(degree == [3] * 8, "L4 prism degree census")
    table = engine.build_transition_table(4, 1)
    require(table.basis.size == 8, "q1 basis dimension")
    require(table.nonzero_count == 24, "q1 directed nonzero census")
    started = __import__("time").monotonic()
    operator = engine.GuardedHamiltonian(table, started)
    dense = np.column_stack(
        [operator(np.eye(8, dtype=np.complex128)[:, column]) for column in range(8)]
    )
    require(float(np.max(np.abs(dense - dense.conj().T))) <= 1e-15, "synthetic Hermiticity")
    exact = np.linalg.eigvalsh(dense)
    require(abs(float(exact[0]) + 3.0) <= 1e-12, "synthetic q1 ground energy")
    row = engine.sector_spectrum(4, 1, synthetic=True)
    require(row["status"] == "RESOLVED_POSITIVE_RESPONSE_SECTOR", "synthetic response status")
    require(row["ground_block_dimension"] == 2, "q1 momentum-zero block dimension")
    require(row["block_dimension"] == 2, "q1 momentum-one block dimension")
    require(abs(float(row["ground_energy"]) + 3.0) <= 1e-12, "Lanczos ground mismatch")
    require(abs(float(row["Delta_act"]) - 2.0) <= 1e-10, "momentum-one response gap mismatch")
    require(float(row["hermiticity_error"]) <= 1e-12, "Hermiticity guard")
    row_q2 = engine.sector_spectrum(4, 2, synthetic=True)
    require(row_q2["status"] == "RESOLVED_POSITIVE_RESPONSE_SECTOR", "q2 response status")
    require(float(row_q2["response_projection_error"]) <= 1e-12, "q2 projection closure")
    require(1e-6 <= float(row_q2["R_low"]) <= 1.0 + 1e-12, "q2 residue range")
    return {
        "status": "PASS",
        "L": 4,
        "q": 1,
        "dimension": 8,
        "ground_energy": row["ground_energy"],
        "response_gap": row["Delta_act"],
        "q2_response_gap": row_q2["Delta_act"],
    }


def custody_test() -> dict[str, object]:
    implementation = (PACKET / "independent_spectrum_engine.py").read_text(encoding="utf-8")
    tree = ast.parse(implementation)
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    allowed_roots = {
        "__future__", "argparse", "hashlib", "json", "math", "os", "resource",
        "sys", "time", "dataclasses", "itertools", "pathlib", "typing", "numpy",
    }
    require(all(name.split(".")[0] in allowed_roots for name in imports), "unexpected implementation import")
    forbidden = (
        "target_interval_worker",
        "interval_spectrum_driver",
        "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001",
        "np.load",
        "numpy.load",
        ".npy",
        ".npz",
    )
    require(all(term not in implementation for term in forbidden), "target code/matrix custody violation")
    return {"status": "PASS", "imports": sorted(imports), "forbidden_terms_absent": list(forbidden)}


def missing_manifest_test() -> dict[str, object]:
    builder = PACKET / "build_blind_freeze.py"
    with tempfile.TemporaryDirectory(prefix="blind-freeze-refusal-") as temporary:
        base = Path(temporary)
        output = base / "must_not_exist.json"
        missing = base / "missing.json"
        command = [
            sys.executable,
            str(builder),
            "--repo-root", str(REPO),
            "--manifest", str(missing),
            "--manifest-sha256", "0" * 64,
            "--sector-plan", str(missing),
            "--sector-plan-sha256", "0" * 64,
            "--pre-output-freeze", str(STATIC_FREEZE),
            "--pre-output-freeze-sha256", sha256(STATIC_FREEZE),
            "--methodology", str(PACKET / "METHODOLOGY.md"),
            "--implementation", str(PACKET / "independent_spectrum_engine.py"),
            "--builder", str(builder),
            "--self-test", str(PACKET / "test_blind_spectral_packet.py"),
            "--output", str(output),
        ]
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        require(completed.returncode == 2, "missing manifest was not refused")
        require(not output.exists(), "builder touched output before validating inputs")
        require(completed.stderr.startswith("REFUSED:"), "missing-manifest refusal not explicit")
    return {"status": "PASS", "returncode": 2, "output_created": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result: dict[str, object] = {
        "schema": "BLIND_RELATIONAL_INTERVAL_SPECTRUM_SELF_TEST_V001",
        "physical_spectrum_executed": False,
        "tests": {},
    }
    try:
        result["tests"] = {
            "syntax": syntax_test(),
            "pre_output_freeze": freeze_test(),
            "synthetic_prism": synthetic_test(),
            "custody": custody_test(),
            "fail_closed_missing_manifest": missing_manifest_test(),
        }
        result["status"] = "PASS_5_OF_5__NO_PHYSICAL_SPECTRUM_EXECUTED"
    except Exception as error:
        result["status"] = "FAIL"
        result["error"] = f"{type(error).__name__}: {error}"
    payload = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0 if result["status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
