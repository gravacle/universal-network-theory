#!/usr/bin/env python3
"""Independent premise reconstruction for the Gate A-R certificate."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
checks = 0


def check(value, label):
    global checks
    if not value:
        raise AssertionError(label)
    checks += 1


def load(path):
    return json.loads((ROOT / path).read_text())


single = load("AUDIT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001/INDEPENDENT_RESULT.json")
seam = load("AUDIT_G_GATE_A_F3_MDC_ACTIVE_SEAM_OWNER_ONCE_V001/INDEPENDENT_RESULT.json")
g4 = load("AUDIT_G_GATE_A_G4_STATIONARY_CARRIER_SEAM_SECTOR_V001/INDEPENDENT_RESULT.json")
join = load("AUDIT_G_GATE_A_SAME_PARENT_OWNER_JOIN_SCREEN_V001/INDEPENDENT_RESULT.json")
cert = load("CERTIFICATE_GATE_A_R_RECORD_OWNERSHIP_CONSERVATION_V001/RESULT.json")

check(single["ledger"]["balance"] == "0", "single-history balance")
check(seam["disposition"] == "PASS_AFTER_REPAIR", "active seam audit")
check(seam["seam_current"] == "1/2" and seam["global_residual"] == "0",
      "active transport ledger")
check(seam["attachment"].startswith("CONDITIONAL"), "conditional attachment")
check(g4["disposition"] == "PASS_SECTOR_QUALIFIED", "G4 qualified")
check((g4["vertices"], g4["owner_once_edges"]) == (64, 192), "G4 census")
check(g4["carrier_sector_residual"] == "0", "G4 residual")
check(join["disposition"] == "PASS_AFTER_REPAIR" and join["checks"] == 18,
      "hostile join reconstruction 18/18")
check(join["factual_screen"]["common_support_matching_join"] == "UNDEFINED",
      "cross-family join absent")
check(join["factual_screen"]["GD_recoil"] == "OPTIONAL_PARENT_BRANCH",
      "recoil optional")
check(cert["join_screen"] == "PASS__28/28", "target join screen 28/28")
check("ADOPTED_ALPHA_EQUALS_R0" in cert["attachment"], "alpha=r0 rides closure")
check(cert["gate_B_R"] == "AUTHORIZED" and cert["gate_A_P"] == "OPEN",
      "R-B versus A-P split")
check(cert["continuum"] == "NOT_ASSUMED" and cert["Ward"] == "NOT_DERIVED" and
      cert["gravity"] == "NOT_CLAIMED", "claim ceiling")

schedule = (ROOT / "RECORD_FIRST_ACCUMULATION_GATE_PLAN_V002.md").read_text()
ledger = (ROOT / "GRAVITY_VERIFICATION_LEDGER.md").read_text()
continuation = (ROOT / "CURRENT_CONTINUATION.md").read_text()
check("No M-series behavior is inferred from passing an R-series gate" in schedule,
      "schedule separation")
check("An absent optional macro degree of freedom creates no record-ledger debt" in schedule,
      "optional macro not debt")
check("Gate A-R — RECORD OWNERSHIP AND CONSERVATION: CLOSED" in ledger,
      "ledger A-R closed")
check("Gate A-P — CONTINUUM/MACROSCOPIC RESPONSE: POST-ACCUMULATION, OPEN" in ledger,
      "ledger A-P open")
check("Gate B-R `L=8` microscopic\nrecord accumulation is authorized" in continuation,
      "continuation R-B authorization")

# Repaired authority consistency: the old global-action gap is explicitly A-P
# and blocks only B-P/M-series, while B-R remains authorized.
check("Gate A-P remains open" in continuation, "A-P qualification")
check("does not block authorized Gate B-R microscopic accumulation" in continuation,
      "B-R remains authorized")
check("blocks only\nGate B-P/M-series macro-response promotion" in continuation,
      "only macro promotion blocked")
check("optional recoil branch" in continuation and
      "not prerequisites\nfor Gate B-R record accumulation" in continuation,
      "join and recoil qualification")
check("Plan-level Gate A remains open" not in continuation and
      "do not launch Gate B" not in continuation, "stale directives removed")

result = {
    "schema": "AUDIT_CERTIFICATE_GATE_A_R_RECORD_OWNERSHIP_CONSERVATION_V001",
    "disposition": "PASS_AFTER_REPAIR",
    "checks": checks,
    "certificate_premises": "PASS_AT_CONDITIONAL_RECORD_SCOPE",
    "join_counts": {"target": "28/28", "hostile_reconstruction": "18/18"},
    "cross_family_join": "ABSENT__NOT_RECORD_PARENT_DEBT",
    "GD_recoil": "OPTIONAL__NOT_RECORD_PARENT_DEBT",
    "attachment": "ADOPTED_ALPHA_EQUALS_R0__NOT_BARE_F3_DERIVED",
    "gate_B_R": "AUTHORIZED",
    "gate_A_P": "OPEN",
    "M_series": "NOT_PROMOTED",
    "continuum_Ward_gravity": "NOT_PROMOTED",
    "material_issue": None
}
(Path(__file__).parent / "INDEPENDENT_RESULT.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(f"PASS_AFTER_REPAIR__{checks}/{checks}")
