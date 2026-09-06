#!/usr/bin/env python3
"""Pinned verifier for the hostile localized-source protocol audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_PROTOCOL_V001"
TRAJECTORY = ROOT / "DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001" / "RESULT.json"
TRAJECTORY_AUDIT = ROOT / "AUDIT_R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001" / "RESULT.json"
SOURCE_THEOREM = ROOT / "DEVELOPMENT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001" / "THEOREM.md"
SOURCE_AUDIT = ROOT / "AUDIT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001" / "INDEPENDENT_RESULT.json"
PARENT = ROOT / "DEVELOPMENT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001" / "RESULT.json"
PARENT_AUDIT = ROOT / "AUDIT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001" / "INDEPENDENT_RESULT.json"
NOT_CLAIMED = (
    "ASYMPTOTIC_OR_INVARIANT_PLATEAU_THEOREM__LOCALIZED_RESPONSE_RESULT__"
    "L14_RESPONSE_FEASIBILITY__SCALING_LAW__PHYSICAL_GRID_OR_DISTANCE__"
    "CONTINUUM__WARD__CRITICAL_OR_GENERIC_PHASE__GRAVITON__GRAVITY"
)

PINS = {
    TARGET / "PROTOCOL.md": "df80a38b3902120902012ab46be9dee1854cf25b7113641227b0fdc5a9b2c8a5",
    TARGET / "README.md": "8853f9193b98a19f66aad6ed7caad898e9eb032d8b672fbb4cbc7a2c63cfd07a",
    TARGET / "RESULT.json": "315efc89e91ccb2816787716f7a724e76f292a9a689a11f80f18f4dd337deb90",
    TARGET / "verify_protocol.py": "6a51d2ea0f559e7ad373e125529df972b58b85b8d84dad4144d486ee4c202aa7",
    TRAJECTORY: "8a69f780a372ae436ef2fe458af80f7fa1ba70d8c93b21d91524c6e9819d753d",
    TRAJECTORY_AUDIT: "c42a94533d9d9795370bb0a997e19b21267d3fc78a4e681f2e07bc83ff6d68a5",
    SOURCE_THEOREM: "113ca9798fe60a4afe7bada091d675ebb71608cab30f53b22bbc8ae59d10a06b",
    SOURCE_AUDIT: "560023054d53f171edaf6c20e8f932056a4c9adae09929c443a905e5974aedba",
    PARENT: "d5c12520518c54dce228e9aa28b860980685276f84aa52aa065b8c6e1e8d0bb4",
    PARENT_AUDIT: "e19faa594ce1710e251ae0c89d4cedeae4b43216d60105b95979b48f55426bc7",
    HERE / "README.md": "8158de7a1995ea8709fa46d9b5b6fac3e8f632da425629c8d9d6e827471b9ea9",
    HERE / "REPORT.md": "72df906efa62274bdf8ee138b0769f8bdc40227188594ab9e7adf7de9351d8e4",
    HERE / "RESULT.md": "22e67bb358d8aa518703411ff5fe5852763a3ee455f1a56cf62b0febdd7bd846",
    HERE / "RESULT.json": "5edd62c053e28fa5b17475df533a4e732c29533792ea9da96e5e664b96f003b9",
    HERE / "INDEPENDENT_RESULT.json": "561c614601f95086ca7cbd65d47bd9945eeead27e2308cb8d11cf4e5794b1372",
    HERE / "independent_reconstruction.py": "b24a764871fa9d9aea760839c318aa3b42a6186d9eb1a4fbede791b2f0a4ccb9",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


checks = []


def check(condition, label):
    checks.append((bool(condition), label))


check(all(digest(path) == expected for path, expected in PINS.items()), "all custody pins")
target = json.loads((TARGET / "RESULT.json").read_text())
trajectory = json.loads(TRAJECTORY.read_text())
trajectory_audit = json.loads(TRAJECTORY_AUDIT.read_text())
source_audit = json.loads(SOURCE_AUDIT.read_text())
parent = json.loads(PARENT.read_text())
parent_audit = json.loads(PARENT_AUDIT.read_text())
independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
summary = json.loads((HERE / "RESULT.json").read_text())

check(target["checks_passed"] == target["checks_total"] == 20, "target protocol 20/20")
check(trajectory["checks_passed"] == trajectory["checks_total"] == 18, "trajectory target 18/18")
check(trajectory_audit["independent_checks"] == "31/31", "trajectory hostile audit 31/31")
check(source_audit["ledger"]["W_R"] == "1/2" and source_audit["ledger"]["balance"] == "0", "source exact ledger")
check(parent["physical_parent_selection"]["prepared_cycle_state"].startswith("EVEN_TAILS_BLANK"), "parent even target blank")
check(parent["physical_parent_selection"]["source_status_during_accumulation"] == "OFF", "parent source off")
check(parent_audit["disposition"] == "PASS_AFTER_REQUIRED_LEDGER_RECLASSIFICATION", "parent hostile audit")

check(independent["checks_passed"] == independent["checks_total"] == 35, "independent reconstruction 35/35")
check(not independent["failures"], "independent failure list empty")
check(independent["verdict"] == "PASS__FINITE_PROTOCOL_AUTHENTICATED_NO_RESPONSE_RESULT", "independent verdict")
check(summary["verdict"] == independent["verdict"], "summary verdict")
check(summary["target_checks"] == "20/20" and summary["independent_checks"] == "35/35", "summary check custody")

attachment = independent["source_parent_attachment"]
check(attachment["parent_pair_after_write"] == "(BB_MINUS_I_XB)_OVER_SQRT2", "parent write phase")
check(attachment["parent_pair_after_native_transfer"] == "B_TAIL_TENSOR_(B_HEAD_PLUS_X_HEAD)_OVER_SQRT2", "parent transfer phase")
check(attachment["baseline_even_tail_q"] == "0" and attachment["baseline_odd_head_q"] == "1/2", "parent pair occupations")
check(attachment["localized_even_tail_state"] == "(B_MINUS_I_X)_OVER_SQRT2", "localized target state")
check(attachment["localized_delta_q"] == attachment["write_amount"] == "1/2", "localized write amount")
check(attachment["write_edge_flux"] == attachment["write_balance"] == "0", "terms-off write ledger")
check(not attachment["second_native_transfer_required"], "no second transfer required")
check(target["localized_source"]["transport_slice"].startswith("SOURCE_AND_WRITER_OFF"), "target source/writer off")

ledger = independent["differential_ledger"]
check(ledger["owner_once_column_sum"] == 0, "incidence telescope")
check("MINUS_ONE_HALF_E_SOURCE" in ledger["identity"], "differential initial-source term")
check(ledger["remainder_status"] == "RAW_UNASSIGNED__NOT_CALLED_DEFECT", "differential remainder status")
check(target["differential_observables"]["full_differential_ledger"].startswith("DELTA_Q_AFTER_PLUS_B_DELTA_J_MINUS_W_R"), "target differential ledger")
check(target["differential_observables"]["global_sum"].endswith("ONE_HALF"), "target global number response")

expected_dimensions = {
    6: (12, 6, 2, 430, 2176),
    8: (16, 8, 2, 4435, 33280),
    10: (20, 10, 2, 53764, 526336),
    12: (24, 12, 2, 704370, 8396800),
    14: (28, 14, 2, 9608050, 134250496),
}
for row in independent["representations"]:
    length = row["L"]
    observed = (
        row["full_group_order"], row["source_orbit_size"],
        row["marked_stabilizer_order"], row["full_invariant_orbit_dimension"],
        row["marked_orbit_dimension"],
    )
    check(observed == expected_dimensions[length], f"L{length} independent dimensions")
    check(row["marked_stabilizer_cycle_counts"] == [length + 2, 2 * length], f"L{length} stabilizer cycles")
check([row["marked_source_orbit_dimension"] for row in target["marked_source_representation"]]
      == [expected_dimensions[length][-1] for length in (6, 8, 10, 12, 14)], "target marked dimensions")
check(all(row["source_orbit_size"] > 1 for row in independent["representations"]), "local state outside full invariant sector")

radial = independent["radial_partition_summary"]
check([row["site_graph_radius"] for row in radial] == [4, 5, 6, 7, 8], "independent support radii")
check([row["owner_once_edge_count"] for row in radial] == [18, 24, 30, 36, 42], "independent edge census")
check([row["canonical_json_sha256"] for row in radial]
      == [canonical_digest(profile) for profile in target["radial_partitions"]], "independent radial profile hashes")
check(all(sum(item["edges"] for item in profile["edge_shell_counts"]) == 3 * profile["L"]
          for profile in target["radial_partitions"]), "target shell completeness")

status = independent["execution_status"]
check(status["protocol_only"] and not status["localized_response_data_present"], "protocol has no response data")
check(status["full_space_validation_required"] == [6, 8], "L6/L8 full-space gate")
check(status["larger_sizes_resource_gated"] == [10, 12, 14] and not status["L14_forced"], "larger-size resource gates")
check(status["Gate_A_P"] == summary["Gate_A_P"] == "OPEN", "Gate A-P open")
check(target["background_reference"]["evidence_class"].endswith("NOT_PROVED_ASYMPTOTE_OR_INVARIANT"), "finite baseline status")
check(target["claim_classes"]["empirical"].endswith("NO_LOCALIZED_RESPONSE_DATA_YET"), "empirical baseline only")
check("PER_SIZE_RESOURCE_ELIGIBILITY" in target["claim_classes"]["open"], "resource eligibility open")
check("REQUIRE_INDEPENDENT_HOSTILE_AUDIT_BEFORE_PROMOTION" in target["execution_gates"], "promotion audit gate")
check(target["not_claimed"] == independent["not_claimed"] == summary["not_claimed"] == NOT_CLAIMED, "structured claim ceiling")

report = (HERE / "REPORT.md").read_text()
result_md = (HERE / "RESULT.md").read_text()
readme = (HERE / "README.md").read_text()
check("no response result" in report and "Gate" in report and "A-P remain open" in report, "report status ceiling")
check("not called a" in report and "defect" in report and "raw and unassigned" in readme, "raw remainder labels")
check("not a physical boundary reflection" in report and "finite support-graph" in report, "finite distance ceiling")
check("L14 is explicitly not forced" in report and "full-space" in report and "L6/L8" in report, "report execution gates")
check(all(term in report for term in ("scaling", "physical grid", "continuum", "Ward", "phase", "graviton", "gravity")), "report physical claim ceiling")
check("35/35" in result_md and "20/20" in result_md and "Gate A-P" in result_md, "result check/status custody")

failures = [label for passed, label in checks if not passed]
if failures:
    raise AssertionError(failures)
print(f"PASS__GATE_AP_LOCALIZED_PROTOCOL_HOSTILE_AUDIT__{len(checks)}/{len(checks)}")
