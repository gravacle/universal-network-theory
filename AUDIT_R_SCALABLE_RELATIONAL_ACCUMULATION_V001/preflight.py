#!/usr/bin/env python3
"""Structural preflight before any scalable relational history output."""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET_DIR = ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
OUT = HERE / "PREFLIGHT_RESULT.json"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


target_code = TARGET_DIR / "compute_seed_history.py"
blind_code = HERE / "blind_seed_history.py"
target = load("relational_seed_target", target_code)
blind = load("relational_seed_blind", blind_code)
protocol = (TARGET_DIR / "PROTOCOL.md").read_text()
target_text = target_code.read_text()
blind_text = blind_code.read_text()

checks: list[dict[str, object]] = []


def check(condition: bool, label: str, detail: object = None) -> None:
    checks.append({"passed": bool(condition), "label": label, "detail": detail})


for length, dimension in ((4, 495), (6, 18564), (8, 735471), (10, 30045015), (12, 1251677700)):
    check(math.comb(3 * length, length) == dimension, f"dimension L{length}")

for forbidden in ("TRACE_L4.json", "HISTORY_L4.json", "HISTORY_L6.json", "HISTORY_L8.json", "SEED_RESULT.json"):
    check(not (TARGET_DIR / forbidden).exists(), f"no target output {forbidden}")
check(not (HERE / "SEED_HOSTILE_RESULT.json").exists(), "no audit comparison output")
check(not (HERE / "RAW_HISTORY").exists(), "no blind raw output directory")

check("import compute_seed_history" not in blind_text, "blind does not import target")
check("ALLOW` is represented" in protocol, "typed ALLOW representation")
check("None of those predicates supplies" in protocol, "predicate generator separation")
check("not an external" in " ".join(protocol.split()).lower(), "no external reservoir statement")
check("not by an added physical global clock" in " ".join(protocol.split()), "relational cursor statement")
check("No truncation" in protocol, "no hidden truncation")
check("EXACT_RELATIONAL_LINEAGE_SCALING_OBSTRUCTION" in protocol, "resource escalation result")

target_l4 = target.Parent(4)
blind_l4 = blind.BlindParent(4)
check(target_l4.dimension == blind_l4.basis.size == 495, "independent L4 basis census")
check(len(target_l4.edges) == len(blind_l4.edge_list) == 12, "independent edge census")
check(len(target_l4.admission_pairs) == len(blind_l4.admissions) == 4, "admission event census")
check(np.all(np.sum(target_l4.incidence, axis=0) == 0), "target incidence telescopes")
check(np.all(np.sum(blind_l4.incidence, axis=0) == 0), "blind incidence telescopes")

rng = np.random.default_rng(20260906)
x = rng.normal(size=495) + 1j * rng.normal(size=495)
y = rng.normal(size=495) + 1j * rng.normal(size=495)
target_hermiticity = abs(np.vdot(x, target_l4.h_action(y)) - np.vdot(target_l4.h_action(x), y))
blind_hermiticity = abs(np.vdot(x, blind_l4.h(y)) - np.vdot(blind_l4.h(x), y))
check(target_hermiticity <= 1.0e-10, "target H Hermitian", float(target_hermiticity))
check(blind_hermiticity <= 1.0e-10, "blind H Hermitian", float(blind_hermiticity))

t0 = target_l4.initial_state()
b0 = blind_l4.start()
check(abs(target_l4.q(t0)) <= 1.0e-15 and abs(target_l4.genesis_q(t0) - 4.0) <= 1.0e-15, "target relational genesis")
check(abs(blind_l4.q(b0)) <= 1.0e-15 and abs(blind_l4.g(b0) - 4.0) <= 1.0e-15, "blind relational genesis")

failures = [row for row in checks if not row["passed"]]
result = {
    "schema": "SCALABLE_RELATIONAL_ACCUMULATION_PREFLIGHT_V001",
    "verdict": "PASS_PREOUTPUT_PREFLIGHT" if not failures else "FAIL_CLOSED_PREOUTPUT_PREFLIGHT",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "target_l4_hermiticity_error": float(target_hermiticity),
    "blind_l4_hermiticity_error": float(blind_hermiticity),
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(result["verdict"])
print(f"checks {result['checks_passed']}/{result['checks_total']}")
if failures:
    for failure in failures:
        print("FAIL", failure["label"], failure["detail"])
    raise SystemExit(1)
