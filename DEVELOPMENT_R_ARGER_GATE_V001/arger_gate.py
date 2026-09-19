#!/usr/bin/env python3
"""Verify and apply the adopted finite ARGER Gate.

The verifier consumes the pure Hamiltonian/probe evidence path, the exact
bounded record-block theorem, and its hostile audit.
"""

from __future__ import annotations

from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent

NATIVE_ANALYZER = Path(
    "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/analyze_centerline.py"
)
NATIVE_ANALYZER_SHA256 = (
    "07daf92a84b563fbae1f288528baa71021fe8911953759e91b5f7d68444d2077"
)
THEOREM = Path("L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md")
THEOREM_SHA256 = "2439e1c36a053fccd57155a858d666f9ecbe0e46ded0a79f3ec3b86cb473f5cc"
AUDIT = Path("AUDIT_L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md")
AUDIT_SHA256 = "d2404e7503117b3fbdd97220824f2155b45b2cc5b7f2c8e577d86abeb00d6ffd"
ADOPTION = Path("ARGER_GATE_ADOPTION_2026-09-16.md")

EXPECTED_MASSES = {
    "4": "0.7260206189754993",
    "6": "0.5846615608350367",
    "8": "0.7373965730354166",
    "10": "0.6500987927669427",
    "12": "0.56956498393327842",
}
EXPECTED_SECTORS = (
    (4, 1), (4, 2),
    (6, 2), (6, 3),
    (8, 2), (8, 3), (8, 4),
    (10, 3), (10, 4), (10, 5),
    (12, 4), (12, 5), (12, 6),
)
EXPECTED_MINIMUM_R_LOW = 0.4280947078156539
EXPECTED_MINIMUM_W_STAR = 0.5


class EvidenceError(RuntimeError):
    """A pinned input or adopted Gate predicate failed."""


def _pinned_text(path: Path, digest: str) -> str:
    full_path = ROOT / path
    if not full_path.is_file() or full_path.is_symlink():
        raise EvidenceError(f"missing, non-file, or symlinked input: {path}")
    payload = full_path.read_bytes()
    observed = hashlib.sha256(payload).hexdigest()
    if observed != digest:
        raise EvidenceError(
            f"SHA-256 mismatch for {path}: expected {digest}, got {observed}"
        )
    return payload.decode("utf-8")


def _native_result() -> dict[str, Any]:
    analyzer_path = ROOT / NATIVE_ANALYZER
    _pinned_text(NATIVE_ANALYZER, NATIVE_ANALYZER_SHA256)
    spec = importlib.util.spec_from_file_location("wac_z1_native_analyzer", analyzer_path)
    if spec is None or spec.loader is None:
        raise EvidenceError("could not load the native finite-evidence analyzer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        module.main()
    value = json.loads(buffer.getvalue())
    if not isinstance(value, dict) or value.get("schema") != "Z1_NATIVE_FINITE_EVIDENCE_V001":
        raise EvidenceError("unexpected native finite-evidence output")
    return value


def build_evidence() -> dict[str, Any]:
    theorem = _pinned_text(THEOREM, THEOREM_SHA256)
    audit = _pinned_text(AUDIT, AUDIT_SHA256)
    adoption_path = ROOT / ADOPTION
    if not adoption_path.is_file() or adoption_path.is_symlink():
        raise EvidenceError("the ARGER Gate adoption record is absent")
    adoption = adoption_path.read_text()

    if "Status: `EXACT_STRUCTURAL_THEOREM_PROVED" not in theorem:
        raise EvidenceError("the exact structural-theorem marker is absent")
    if "Disposition: `PASS`" not in audit or THEOREM_SHA256 not in audit:
        raise EvidenceError("the hostile audit does not pass and bind the theorem")
    if "ADOPTED__GOVERNING_FINITE_ARGER_GATE" not in adoption:
        raise EvidenceError("the governing ARGER Gate adoption marker is absent")

    native = _native_result()
    band = native["record_band"]
    visibility = native["finite_selected_sector_visibility"]
    observed_masses = band["masses_by_L"]
    if band.get("all_sizes_cross_half") is not True:
        raise EvidenceError("the native record block does not cross one half")
    for length, expected in EXPECTED_MASSES.items():
        observed = float(observed_masses[length])
        if abs(observed - float(expected)) > 5.0e-16:
            raise EvidenceError(f"record-block mass mismatch at L{length}")

    rows = visibility["rows"]
    observed_sectors = tuple((int(row["L"]), int(row["q"])) for row in rows)
    if observed_sectors != EXPECTED_SECTORS:
        raise EvidenceError("the 13-sector block identity changed")
    if visibility.get("all_selected_rows_positive") is not True:
        raise EvidenceError("a selected sector lacks positive finite visibility")
    if abs(float(visibility["minimum_R_low"]) - EXPECTED_MINIMUM_R_LOW) > 5.0e-16:
        raise EvidenceError("the global minimum R_low changed")
    if abs(float(visibility["minimum_w_star"]) - EXPECTED_MINIMUM_W_STAR) > 5.0e-16:
        raise EvidenceError("the global minimum pole weight changed")

    return {
        "schema": "WAC_ARGER_GATE_EVIDENCE_V001",
        "status": "PASS__ADOPTED_GOVERNING_FINITE_Z1_ARGER_GATE",
        "custody": {
            "native_finite_analyzer": {
                "path": str(NATIVE_ANALYZER),
                "sha256": NATIVE_ANALYZER_SHA256,
            },
            "structural_theorem": {"path": str(THEOREM), "sha256": THEOREM_SHA256},
            "hostile_audit": {"path": str(AUDIT), "sha256": AUDIT_SHA256},
            "adoption_record": {"path": str(ADOPTION)},
        },
        "record_block": {
            "atoms": [f"A{index:03d}" for index in range(9, 17)],
            "density_interval": "[7/48,13/48)",
            "masses_by_L": EXPECTED_MASSES,
            "all_sizes_majority": True,
            "unique_sectors": [[length, charge] for length, charge in EXPECTED_SECTORS],
            "all_sectors_positive_finite_visibility": True,
            "minimum_R_low": "0.4280947078156539",
            "minimum_w_star": "0.5",
            "l12_majority_margin": "0.06956498393327842",
        },
        "gate": {
            "id": "ARGER-GATE-1",
            "name": "ARGER Gate 1",
            "membership": "PASS",
            "majority": "PASS",
            "visibility": "PASS",
            "finite_gft_z1": "PASS",
        },
        "separate_claims": {
            "conditional_same_model_dynamical_z1": "SEE_PINNED_LL_P_THEOREM",
            "premise_free_uniform_all_L_z1": "OPEN_STRONGER_RESULT_NOT_GATE_REQUIREMENT",
            "alpha_write_cost": "HYPOTHESIS_NOT_ESTABLISHED",
        },
    }


def main() -> None:
    print(json.dumps(build_evidence(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
