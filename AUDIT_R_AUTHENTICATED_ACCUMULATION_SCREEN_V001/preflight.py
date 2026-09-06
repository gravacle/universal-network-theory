#!/usr/bin/env python3
"""Pre-output structural and method-custody verification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from blind_history import BlindCarrier


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET_DIR = ROOT / "DEVELOPMENT_R_AUTHENTICATED_ACCUMULATION_SCREEN_V001"
TARGET_CODE = TARGET_DIR / "compute_authenticated_history.py"
PROTOCOL = TARGET_DIR / "PROTOCOL.md"
FREEZE = HERE / "FROZEN_METHOD.json"
OUT = HERE / "PREFLIGHT_RESULT.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


freeze = json.loads(FREEZE.read_text())
checks: list[dict[str, object]] = []


def check(condition: bool, label: str, detail: object = None) -> None:
    checks.append({"passed": bool(condition), "label": label, "detail": detail})


paths = {
    "PROTOCOL.md": PROTOCOL,
    "compute_authenticated_history.py": TARGET_CODE,
    "METHODOLOGY.md": HERE / "METHODOLOGY.md",
    "blind_history.py": HERE / "blind_history.py",
    "preflight.py": HERE / "preflight.py",
    "compare_seed.py": HERE / "compare_seed.py",
}
for name, path in paths.items():
    check(digest(path) == freeze["files"][name], f"frozen hash {name}")

target_source = TARGET_CODE.read_text()
blind_source = (HERE / "blind_history.py").read_text()
check("AUDIT_R_AUTHENTICATED_ACCUMULATION_SCREEN_V001" not in target_source, "target does not import audit packet")
check("compute_authenticated_history" not in blind_source, "blind does not import target")

for length in (4, 6):
    # Import target only in this pre-output cross-method verifier.
    namespace: dict[str, object] = {
        "__name__": "target_preflight_import",
        "__file__": str(TARGET_CODE),
    }
    exec(compile(TARGET_CODE.read_text(), str(TARGET_CODE), "exec"), namespace)
    target = namespace["Carrier"](length)
    blind = BlindCarrier(length)
    check(target.dimension == blind.dimension, f"dimension L{length}")
    check(target.edges == blind.edges, f"edge owner order L{length}")
    check(len(target.edges) == 3 * length, f"owner census L{length}")
    check(np.all(np.sum(target.incidence, axis=0) == 0), f"target incidence telescopes L{length}")
    check(np.all(np.sum(blind.incidence, axis=0) == 0), f"blind incidence telescopes L{length}")
    for edge_index, (active, mask, _) in enumerate(target.actions):
        source, destination = blind.pairs[edge_index]
        blind_active = np.sort(np.concatenate((source, destination)).astype(np.uint32))
        check(np.array_equal(np.sort(active), blind_active), f"action support L{length} edge{edge_index}")
        check(np.array_equal(np.sort(active ^ mask), blind_active), f"action image L{length} edge{edge_index}")
    vacuum = target.vacuum()
    written_target = target.apply_write(vacuum)
    written_blind = blind.write(blind.blank())
    check(float(np.max(np.abs(written_target - written_blind))) <= 2.0e-16, f"write vector L{length}")
    check(abs(target.q_expectation(written_target) - 0.5) <= 2.0e-16, f"first W one half L{length}")
    check(float(np.max(np.abs(target.h_action(written_target) - blind.h(written_blind)))) <= 2.0e-16, f"Hamiltonian action L{length}")
    check(float(np.max(np.abs(target.currents(vacuum)))) == 0.0, f"target real-state zero currents L{length}")
    check(float(np.max(np.abs(blind.current(blind.blank())))) == 0.0, f"blind real-state zero currents L{length}")

target_raw = sorted((TARGET_DIR / "RAW_HISTORY").glob("*.json")) if (TARGET_DIR / "RAW_HISTORY").exists() else []
blind_raw = sorted((HERE / "RAW_HISTORY").glob("*.json")) if (HERE / "RAW_HISTORY").exists() else []
check(not target_raw, "no target history output before freeze", [path.name for path in target_raw])
check(not blind_raw, "no blind history output before freeze", [path.name for path in blind_raw])

failures = [row for row in checks if not row["passed"]]
result = {
    "schema": "AUTHENTICATED_ACCUMULATION_PREFLIGHT_V001",
    "verdict": "PASS_PREOUTPUT_METHOD_FROZEN" if not failures else "FAIL_PREOUTPUT",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "frozen_method_sha256": digest(FREEZE),
    "claim_boundary": "STRUCTURAL_AND_METHOD_READINESS_ONLY__NO_TARGET_HISTORY",
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(result["verdict"])
print(f"checks {result['checks_passed']}/{result['checks_total']}")
if failures:
    for failure in failures:
        print("FAIL", failure["label"], failure["detail"])
    raise SystemExit(1)
