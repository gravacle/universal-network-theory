#!/usr/bin/env python3
"""Hash-pinned hostile verifier for the intrinsic L4 admission trace."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET_DIR = ROOT / "DEVELOPMENT_R_INTRINSIC_ADMISSION_PARENT_L4_V001"
OUT = HERE / "FINAL_HOSTILE_RESULT.json"

EXPECTED = {
    "protocol": "cabc01e2389b59cf1ce07f111dd072dba2ca23e29d29095ef02a298e1f1eca32",
    "target_code": "d316b28e282719ed3c3f7a93903ccd4150d80657f6fa37e6b318e96cefd4302e",
    "target_trace": "5ccb82f16a4a17f51451d687a9b8d46658becca8a1d16c2676d4ca49c4d9b4a6",
    "target_result": "bf2cadc42b1348b3ca802f956629516c8a3edeed3db6e87362d048cca6726821",
    "audit_method": "dd614c6b3eb931af950b2edd6bae51dd3cd671bebd79414e428852b6351c1702",
    "frozen_method": "65ba49c63599bc167091d83d0ce80f116f23e8b62a18b7a71882c330cfa14b5e",
    "repair_note": "351b0dc4b96abb26f4e849d2c27e4ce35e832c21bbda91c11b6543cb96183beb",
    "frozen_repair": "586d880f183e278ac5a2951ede13f0db96209831c533502d8ffccb5b9aa97e56",
    "audit_code": "9624c9bf0ea08040f76823ec359e2c4abb773c35dd008d9628ec212d88be3f25",
    "audit_trace": "b419ce1d863ffb216ed122b21371e17d8b82216bc24aa1b68ee6b76f5dafd90b",
}

PATHS = {
    "protocol": TARGET_DIR / "PROTOCOL.md",
    "target_code": TARGET_DIR / "compute_l4_trace.py",
    "target_trace": TARGET_DIR / "TRACE_L4.json",
    "target_result": TARGET_DIR / "RESULT.md",
    "audit_method": HERE / "METHODOLOGY.md",
    "frozen_method": HERE / "FROZEN_METHOD.json",
    "repair_note": HERE / "BOUNDED_BACKEND_REPAIR.md",
    "frozen_repair": HERE / "FROZEN_REPAIR.json",
    "audit_code": HERE / "independent_l4_trace.py",
    "audit_trace": HERE / "INDEPENDENT_TRACE_L4.json",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks: list[dict[str, object]] = []


def check(condition: bool, label: str, detail: object = None) -> None:
    checks.append({"passed": bool(condition), "label": label, "detail": detail})


for name, path in PATHS.items():
    check(path.is_file(), f"file exists {name}")
    if path.is_file():
        check(digest(path) == EXPECTED[name], f"hash {name}")

target = json.loads(PATHS["target_trace"].read_text())
audit = json.loads(PATHS["audit_trace"].read_text())
protocol = PATHS["protocol"].read_text()
human = PATHS["target_result"].read_text()
frozen = json.loads(PATHS["frozen_method"].read_text())
repair = json.loads(PATHS["frozen_repair"].read_text())

check(target["classification"] == "PASS_L4_INTRINSIC_ADMISSION__COHERENT_UNWRITING_ELIMINATED_ON_DECLARED_TRACE", "target classification")
check(target["checks_passed"] == target["checks_total"] == 10, "target check census")
check(all(bool(value) for value in target["checks"].values()), "all target checks pass")
check(audit["verdict"] == "PASS_HOSTILE_INTRINSIC_ADMISSION_L4", "audit verdict")
check(audit["checks_passed"] == audit["checks_total"] == 12, "audit check census")
check(all(bool(value) for value in audit["checks"].values()), "all audit checks pass")
check(len(target["rows"]) == len(audit["rows"]) == 4, "event census")
check(target["cursor_path_prefix"] == [0, 1, 2, 3], "relational path prefix")
check(target["reachable_dimension"] == 4096, "complete reachable dimension")

writes = [float(row["W_n"]) for row in target["rows"]]
allows = [float(row["allow_probability"]) for row in target["rows"]]
blocked = [float(row["blocked_probability"]) for row in target["rows"]]
check(min(writes) >= -1.0e-12, "no negative target write")
check(max(blocked) > 0.1, "nonvacuous blocked component")
check(max(float(row["blocked_null_state_error"]) for row in target["rows"]) == 0.0, "blocked components exactly null")
check(max(float(row["reverse_support_probability"]) for row in target["rows"]) == 0.0, "fresh cells no reverse support")
check(max(abs(writes[i] - 0.5 * allows[i]) for i in range(4)) <= 2.0e-15, "write equals half allow probability")
check(float(target["maximum_admission_accounting_residual"]) <= 1.0e-12, "admission accounting guard")
check(max(float(row["transport_node_residual_l1"]) for row in target["rows"]) <= 1.0e-9, "transport node ledger guard")
check(max(float(row["transport_number_drift"]) for row in target["rows"]) <= 1.0e-10, "transport number guard")
check(max(float(row["norm_error_after_transport"]) for row in target["rows"]) <= 1.0e-10, "target norm guard")
check(abs(float(target["final_total_q"]) - 4.0) <= 2.0e-14, "complete content conserved")
check(float(audit["maximum_target_independent_disagreement"]) <= 1.0e-9, "target independent agreement")
check(float(audit["dense_hermiticity_error"]) <= 1.0e-14, "dense Hermiticity guard")
check(float(audit["dense_unitarity_error"]) <= 1.0e-12, "dense unitarity guard")

check(frozen["target_output_existed_at_freeze"] is False, "pre-output method freeze")
check(repair["audit_output_existed_at_repair_freeze"] is False, "pre-audit-output repair freeze")
check(repair["thresholds_or_physics_changed"] is False, "repair changes no threshold or physics")
check("No modal word" in protocol, "predicate generator separation")
check("not an absolute global clock" in protocol, "no absolute-clock claim")
check("not an external reservoir" in " ".join(protocol.split()), "no external reservoir")
check("No grid, privileged boundary, external reservoir" in human, "human claim ceiling")
check("gravity" in target["claim_boundary"]["not_claimed"][-1].lower(), "machine gravity ceiling")

failures = [row for row in checks if not row["passed"]]
verdict = "PASS_FINAL_HOSTILE_INTRINSIC_ADMISSION_L4" if not failures else "FAIL_CLOSED_FINAL_HOSTILE_INTRINSIC_ADMISSION_L4"
result = {
    "schema": "INTRINSIC_ADMISSION_PARENT_L4_FINAL_HOSTILE_V001",
    "verdict": verdict,
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "classification": target["classification"],
    "writes": writes,
    "allow_probabilities": allows,
    "blocked_probabilities": blocked,
    "maximum_target_independent_disagreement": float(audit["maximum_target_independent_disagreement"]),
    "logical_result": "FRESH_INTERNAL_ONE_PASS_ADMISSION_REMOVES_NEGATIVE_WRITE_ON_DECLARED_L4_TRACE",
    "next_gate": "PREREGISTER_SCALABLE_RELATIONAL_ACCUMULATION_HISTORY",
    "claim_boundary": {
        "proved": "FINITE_L4_INTRINSIC_BLOCKED_NULL_AND_NONNEGATIVE_WRITE",
        "not_claimed": ["GENERIC_ACCUMULATION", "BACKGROUND_INDEPENDENCE_THEOREM", "COMMON_SECTOR", "CONTINUUM", "EMERGENCE", "GRAVITY"],
    },
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(verdict)
print(f"checks {result['checks_passed']}/{result['checks_total']}")
if failures:
    for failure in failures:
        print("FAIL", failure["label"], failure["detail"])
    raise SystemExit(1)
