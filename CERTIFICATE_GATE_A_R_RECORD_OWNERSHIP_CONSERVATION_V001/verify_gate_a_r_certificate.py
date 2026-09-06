#!/usr/bin/env python3
"""Custody and scope verification for the Gate A-R closure certificate."""

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
checks = 0


def check(condition: bool, label: str) -> None:
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


required = {
    "single_target": "DEVELOPMENT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001/verify_single_history_ledger.py",
    "single_audit": "AUDIT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001/INDEPENDENT_RESULT.json",
    "seam_target": "DEVELOPMENT_G_GATE_A_F3_MDC_ACTIVE_SEAM_OWNER_ONCE_V001/verify_active_seam_owner_once.py",
    "seam_audit": "AUDIT_G_GATE_A_F3_MDC_ACTIVE_SEAM_OWNER_ONCE_V001/INDEPENDENT_RESULT.json",
    "g4_target": "DEVELOPMENT_G_GATE_A_G4_STATIONARY_CARRIER_SEAM_SECTOR_V001/verify_stationary_carrier_sector.py",
    "g4_audit": "AUDIT_G_GATE_A_G4_STATIONARY_CARRIER_SEAM_SECTOR_V001/INDEPENDENT_RESULT.json",
    "join_target": "DEVELOPMENT_G_GATE_A_SAME_PARENT_OWNER_JOIN_SCREEN_V001/verify_same_parent_join_screen.py",
    "join_audit": "AUDIT_G_GATE_A_SAME_PARENT_OWNER_JOIN_SCREEN_V001/INDEPENDENT_RESULT.json",
    "schedule": "RECORD_FIRST_ACCUMULATION_GATE_PLAN_V002.md",
    "ledger": "GRAVITY_VERIFICATION_LEDGER.md",
}
paths = {key: REPO / value for key, value in required.items()}
for key, path in paths.items():
    check(path.is_file(), f"required evidence exists: {key}")

single = json.loads(paths["single_audit"].read_text())
seam = json.loads(paths["seam_audit"].read_text())
g4 = json.loads(paths["g4_audit"].read_text())
join = json.loads(paths["join_audit"].read_text())
result = json.loads((HERE / "RESULT.json").read_text())

check(single["disposition"] == "PASS_AT_CONDITIONAL_SINGLE_HISTORY_WITNESS_SCOPE",
      "single-history audit pass")
check(single["ledger"]["balance"] == "0", "single-history exact balance")
check(seam["disposition"] == "PASS_AFTER_REPAIR", "active-seam audit pass")
check(seam["seam_current"] == "1/2" and seam["global_residual"] == "0",
      "active nonzero seam and zero global residual")
check(g4["disposition"] == "PASS_SECTOR_QUALIFIED", "G4 sector audit pass")
check(g4["vertices"] == 64 and g4["owner_once_edges"] == 192 and
      g4["carrier_sector_residual"] == "0", "G4 owner-once census")
check(join["disposition"] == "PASS_AFTER_REPAIR" and join["checks"] == 18,
      "same-parent join hostile pass")
check(join["factual_screen"]["common_support_matching_join"] == "UNDEFINED",
      "cross-family macro join remains open")

schedule = paths["schedule"].read_text()
ledger = paths["ledger"].read_text()
for phrase in (
    "R-B does **not** require `p->2`",
    "record-ledger residual",
    "No M-series behavior is inferred from passing an R-series gate",
):
    check(phrase in schedule, f"record/macro separation: {phrase}")
for phrase in (
    "Gate A-R — RECORD OWNERSHIP AND CONSERVATION: CLOSED",
    "Gate B-R — MICROSCOPIC RECORD ACCUMULATION: AUTHORIZED",
    "Gate A-P — CONTINUUM/MACROSCOPIC RESPONSE: POST-ACCUMULATION, OPEN",
):
    check(phrase in ledger, f"authoritative ledger disposition: {phrase}")

check(result["disposition"] ==
      "GATE_A_R_CLOSED__CONDITIONAL_F3_MDC_RECORD_SCOPE",
      "certificate exact scope")
check(result["gate_B_R"] == "AUTHORIZED" and result["gate_A_P"] == "OPEN",
      "R-B authorized without A-P promotion")
check(result["continuum"] == "NOT_ASSUMED" and
      result["Ward"] == "NOT_DERIVED" and
      result["gravity"] == "NOT_CLAIMED", "macro claim ceiling")

print("GATE_A_R", "CLOSED__CONDITIONAL_F3_MDC_RECORD_SCOPE")
print("GATE_B_R", "AUTHORIZED")
print("GATE_A_P", "OPEN")
print("CONTINUUM_WARD_GRAVITY", "NOT_ASSUMED", "NOT_DERIVED", "NOT_CLAIMED")
print(f"PASS__GATE_A_R_CLOSURE_CERTIFICATE__{checks}/{checks}")
