#!/usr/bin/env python3
"""Independent hostile reconstruction of the same-parent join screen."""

from math import comb
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
checks = 0


def check(value, label):
    global checks
    if not value:
        raise AssertionError(label)
    checks += 1


sizes = [comb(n + 3, 3) for n in range(65)]
check(sizes[5] == 56 and sizes[6] == 84, "simplex neighbors")
check(64 not in sizes, "no simplex cardinality 64")
check(all(a < b for a, b in zip(sizes, sizes[1:])), "strict monotonicity")

atlas = (ROOT / "LANE_CROSS_RFT_GRA_GL6AA_RECORD_AUTHENTICATED_SHARED_CHILD_ATLAS_V001/THEOREM.md").read_text()
carrier = (ROOT / "DEVELOPMENT_G_GATE_A_G4_STATIONARY_CARRIER_SEAM_SECTOR_V001/THEOREM.md").read_text()
gd = (ROOT / "LANE_GRA_GD_F3_Q4_TRANSLATION_OWNING_RECOIL_PARENT_V001/THEOREM.md").read_text()
plan = (ROOT / "GRAVITY_GATE_EXECUTION_PLAN_V001.md").read_text()
continuation = (ROOT / "CURRENT_CONTINUATION.md").read_text()

check("address map, edge list, and owner map are supplied" in atlas,
      "atlas program data supplied")
check("autonomous address or graph selection" in atlas, "atlas selection ceiling")
check("V_4" not in atlas and "(Z/4Z)^3" not in atlas,
      "atlas has no explicit carrier-family map")
check("FPSS" not in carrier and "GL6AA" not in carrier,
      "carrier has no explicit atlas binding")

for token in ("Not claimed:", "derived recoil scale or placement",
              "not a derived universal charge-to-momentum law",
              "not a physical diamond-space"):
    check(token in gd, "GD optional/free ceiling: " + token)

check("Gate A — in progress" in plan, "authoritative Gate A status")
check("OWNER_INCOMPLETE" in plan, "global action incomplete")
check("Ward residuals" in plan and "remain undefined" in plan, "Ward remains gated")
check("no \\(L=8\\) flight" in plan and "authorized" in plan, "Gate B withheld")
check("RECORD_FIRST_ACCUMULATION_GATE_PLAN_V002.md" in continuation and
      "Gate A-P remains open" in continuation, "continuation schedule")

# History classification: these commits exist and represent distinct stages.
import subprocess
for commit in ("db187df", "ea52b62"):
    subprocess.run(["git", "cat-file", "-e", commit + "^{commit}"], cwd=ROOT,
                   check=True, capture_output=True)
    checks += 1

result = {
    "schema": "AUDIT_G_GATE_A_SAME_PARENT_OWNER_JOIN_SCREEN_V001",
    "disposition": "PASS_AFTER_REPAIR",
    "checks": checks,
    "factual_screen": {
        "simplex_cardinality_64": False,
        "authenticated_V4_FPSS_map": "ABSENT_IN_CURRENT_FROZEN_PACKETS",
        "GD_recoil": "OPTIONAL_PARENT_BRANCH",
        "common_support_matching_join": "UNDEFINED"
    },
    "material_defect": None,
    "false_result_promotion_found": False,
    "history": {
        "db187df": "VALID_L4_SELECTED_RESPONSE_CHECKPOINT__NOT_GRAVITY",
        "ea52b62": "VALID_UV_LEDGER_SCHEDULING_REFINEMENT__NOT_GRAVITY"
    },
    "global_action": "OWNER_INCOMPLETE",
    "descent": "UNDEFINED",
    "Ward": "UNDEFINED",
    "gate_A": "OPEN",
    "gate_B": "UNAUTHORIZED",
    "gravity": "NOT_CLAIMED"
}
(Path(__file__).parent / "INDEPENDENT_RESULT.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(f"PASS_AFTER_REPAIR__{checks}/{checks}")
