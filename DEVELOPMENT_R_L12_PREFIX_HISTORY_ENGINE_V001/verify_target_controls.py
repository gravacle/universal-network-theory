#!/usr/bin/env python3
"""Hash-pinned comparison of prefix target controls with sealed histories."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SEALED = ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001" / "METHOD_VALIDATION"
EXPECTED = {
    4: ("22b9f88e4f99f8b867523288d93435adf11cce1cb1dbc018fd64733af4c29a9b",
        "53cc89a66f341f6a4c5943c9cf339e762494fbf400296248de93436d58b7c244"),
    6: ("f448bc68771638fcfd42862825077a887dd5ec350e6b352c40ab071110afe024",
        "6f109b4ce7f1f2ec76715438b4e0ec7ecf659ff63d295b55ade925b69bbfa074"),
    8: ("906c2d5c296edd6de1a2e63a512c8cd768c973b92fca2103d6f23dd88356635a",
        "38def243a4cd127e88c776715d27abebecc8bdf1cd7488d9c06b4c5f18d5ef02"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    checks = []
    rows = {}
    for length, (sealed_hash, target_hash) in EXPECTED.items():
        sealed_path = SEALED / f"STREAMED_HISTORY_L{length}.json"
        target_path = HERE / "CONTROL_HISTORY" / f"TARGET_L{length}.json"
        checks.append((digest(sealed_path) == sealed_hash, f"L{length} sealed hash"))
        checks.append((digest(target_path) == target_hash, f"L{length} target hash"))
        old = json.loads(sealed_path.read_text())
        new = json.loads(target_path.read_text())
        numeric_error = 0.0
        sector_error = 0.0
        for left, right in zip(old["rows"], new["rows"]):
            for key in left:
                if key in ("actual_solver", "null_solver", "sector_weights"):
                    continue
                if isinstance(left[key], (int, float)) and isinstance(right.get(key), (int, float)):
                    numeric_error = max(numeric_error, abs(float(left[key]) - float(right[key])))
            sector_error = max(sector_error, float(np.max(np.abs(
                np.asarray(left["sector_weights"]) - np.asarray(right["sector_weights"])
            ))))
        summary_error = max(
            abs(float(a) - float(b))
            for key in ("admission_acceptance", "connector_ratio", "routed_acceptance")
            for a, b in zip(old["comparison"][key], new["comparison"][key])
        )
        old_sector = old["comparison"]["sector"]
        new_sector = new["comparison"]["sector"]
        interval_equal = all(old_sector[key] == new_sector[key] for key in (
            "density_interval", "late_events", "q_lower", "q_upper"
        ))
        interval_mass_error = max(
            abs(float(old_sector[key]) - float(new_sector[key]))
            for key in ("enclosed_mass", "discarded_mass")
        )
        checks.extend((
            (len(old["rows"]) == len(new["rows"]) == length, f"L{length} row census"),
            (new["comparison"]["resolved"] is True, f"L{length} target resolved"),
            (numeric_error <= 1e-8, f"L{length} registered/ledger agreement"),
            (sector_error <= 1e-8, f"L{length} sector agreement"),
            (summary_error <= 1e-8, f"L{length} summary agreement"),
            (interval_equal, f"L{length} interval structural identity"),
            (interval_mass_error <= 1e-8, f"L{length} interval mass agreement"),
        ))
        rows[str(length)] = {
            "maximum_numeric_difference": numeric_error,
            "maximum_sector_difference": sector_error,
            "maximum_summary_difference": summary_error,
            "maximum_interval_mass_difference": interval_mass_error,
            "new_wall_seconds": new["wall_seconds"],
            "new_peak_rss_bytes": new["peak_rss_bytes"],
            "sealed_wall_seconds": old["wall_seconds"],
        }
    failures = [label for passed, label in checks if not passed]
    result = {
        "schema": "R_PREFIX_HISTORY_TARGET_CONTROL_GATE_V001",
        "classification": ("PASS_TARGET_PREFIX_CONTROLS_L4_L8__CROSS_HOSTILE_GATE_REQUIRED"
                           if not failures else "FAIL_TARGET_PREFIX_CONTROLS"),
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "rows": rows,
        "next_gate": "CROSS_TARGET_HOSTILE_CONTROLS_BEFORE_L10",
        "claim_boundary": "TARGET_CONTROLS_ONLY__NO_L10_L12_SPECTRUM_Z1_OR_GRAVITY",
    }
    output = HERE / "TARGET_CONTROL_GATE_V002.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["classification"])
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
