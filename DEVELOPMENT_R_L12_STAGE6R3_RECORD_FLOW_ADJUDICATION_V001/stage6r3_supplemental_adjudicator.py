#!/usr/bin/env python3
"""Owner-once Stage-6R3 supplemental adjudication of the L12 flow sidecar.

The script preserves the frozen Stage-6R2 result.  It evaluates two proposed
mass laws separately:

1. whole-sector connectivity: include all q5 mass once q4--q5--q6 sector
   connectivity is authenticated;
2. conservative flow support: include only q5 mass proven to belong to a
   common q4--q5--q6 lineage.

Arithmetic is never confused with admissibility.  The script fails closed on
unadopted gate rules, different probability measures, and absent lineage
intersection evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Mapping, Sequence


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LENGTH = 12
LATE_EVENT_FIRST = math.ceil(LENGTH / 2)
LATE_EVENTS = tuple(range(LATE_EVENT_FIRST, LENGTH + 1))
MASS_THRESHOLD = Decimal("0.50")
GEOMETRY_LOWER = Decimal("0.90")
GEOMETRY_UPPER = Decimal("1.10")
NUMERIC_TOLERANCE = Decimal("1e-12")
SCHEMA = "L12_STAGE6R3_RECORD_FLOW_SUPPLEMENTAL_ADJUDICATION_V001"

DEFAULT_STAGE6 = (
    ROOT
    / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001"
    / "ADJUDICATION_V002_L12_V003R1_STAGE6R2.json"
)
DEFAULT_FLOW_REPORT = (
    ROOT
    / "DEVELOPMENT_R_L12_RECORD_FLOW_BRIDGE_V001"
    / "RECORD_FLOW_BRIDGE_REPORT_V001.json"
)
DEFAULT_TARGET_HISTORY = (
    ROOT
    / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
    / "PHYSICAL_OUTPUTS"
    / "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
)
DEFAULT_PROTOCOL = ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001" / "PROTOCOL.md"
DEFAULT_DRIVER = (
    ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001" / "interval_spectrum_driver.py"
)
DEFAULT_MANIFEST_BUILDER = (
    ROOT / "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V001" / "build_sector_manifest.py"
)
DEFAULT_OUTPUT = HERE / "STAGE6R3_SUPPLEMENTAL_ADJUDICATION_V001.json"

PINNED_SHA256 = {
    "stage6r2": "43c7c19daaf24902d2699c337851eca35a03c3db69f8e3f55f3b0142f87e137d",
    "flow_report": "4a02db3eaea066a4c65bce921fcfaaffcc7e731b057d06f4c50180b6e38b40a6",
    "target_history": "079499e7b989e1ba45b1c397882c8638106be149ccb994058a3703b235736764",
    "protocol": "db39a11dfb738fe206a5c0b5b34ec5c90ff29385f1d52aa33181814ec162ebb6",
    "driver": "2e8fede6cbfae9444f39d9e329347237915e42282ad9b667cd2631f3c5c8d9ad",
    "manifest_builder": "97ad7e9fa5469b824aa2694aee83a1dc3c328928b38971aff4433f1c40ae38b9",
}


class Refusal(RuntimeError):
    """Authenticated inputs cannot support this supplemental adjudication."""


@dataclass(frozen=True)
class Artifact:
    label: str
    path: Path
    sha256: str
    raw: bytes
    json: Mapping[str, Any] | None


def hash_regular_file(path: Path) -> tuple[str, tuple[int, int, int, int], bytes]:
    try:
        before = path.stat()
        if not stat.S_ISREG(before.st_mode):
            raise Refusal(f"not a regular file: {path}")
        raw = path.read_bytes()
        after = path.stat()
    except OSError as error:
        raise Refusal(f"cannot read {path}: {error}") from error
    before_id = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    after_id = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    if before_id != after_id:
        raise Refusal(f"file changed during authentication: {path}")
    return hashlib.sha256(raw).hexdigest(), after_id, raw


def authenticate(path: Path, expected_sha256: str, label: str, parse_json: bool) -> Artifact:
    actual, identity, raw = hash_regular_file(path)
    if actual != expected_sha256:
        raise Refusal(
            f"{label} SHA-256 mismatch: expected={expected_sha256} actual={actual} path={path}"
        )
    payload: Mapping[str, Any] | None = None
    if parse_json:
        try:
            decoded = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise Refusal(f"{label} is not valid UTF-8 JSON: {error}") from error
        if not isinstance(decoded, Mapping):
            raise Refusal(f"{label} top level is not an object")
        payload = decoded
    final = path.stat()
    if (final.st_dev, final.st_ino, final.st_size, final.st_mtime_ns) != identity:
        raise Refusal(f"{label} changed during parsing: {path}")
    return Artifact(label, path.resolve(), actual, raw, payload)


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise Refusal(message)


def decimal_value(value: Any, label: str) -> Decimal:
    if isinstance(value, bool):
        raise Refusal(f"{label} is boolean, not numeric")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as error:
        raise Refusal(f"{label} is not decimal: {value!r}") from error
    if not result.is_finite():
        raise Refusal(f"{label} is not finite")
    return result


def reconstruct_late_pbar(history: Mapping[str, Any]) -> dict[str, Any]:
    demand(history.get("L") == LENGTH, "target history is not L12")
    comparison = history.get("comparison")
    demand(
        isinstance(comparison, Mapping) and comparison.get("resolved") is True,
        "target history is unresolved",
    )
    rows = history.get("rows")
    demand(isinstance(rows, list) and len(rows) == LENGTH, "target history row census is not 12")
    by_event: dict[int, list[Decimal]] = {}
    for row in rows:
        demand(isinstance(row, Mapping), "target history contains a non-object row")
        event = row.get("event")
        weights = row.get("sector_weights")
        demand(type(event) is int and 1 <= event <= LENGTH, "target history event is invalid")
        demand(event not in by_event, f"duplicate target history event {event}")
        demand(isinstance(weights, list) and len(weights) == LENGTH + 1, f"event {event} sector census invalid")
        parsed = [decimal_value(value, f"event {event} q={q} weight") for q, value in enumerate(weights)]
        demand(all(value >= -NUMERIC_TOLERANCE for value in parsed), f"event {event} negative weight")
        demand(abs(sum(parsed, Decimal(0)) - Decimal(1)) <= Decimal("1e-9"), f"event {event} not normalized")
        by_event[event] = parsed
    demand(tuple(sorted(by_event)) == tuple(range(1, LENGTH + 1)), "target history event sequence incomplete")
    pbar = [
        sum((by_event[event][q] for event in LATE_EVENTS), Decimal(0)) / Decimal(len(LATE_EVENTS))
        for q in range(LENGTH + 1)
    ]
    demand(abs(sum(pbar, Decimal(0)) - Decimal(1)) <= Decimal("1e-9"), "reconstructed pbar not normalized")
    return {
        "definition": "arithmetic mean of sector_weights over events 6 through 12",
        "events": list(LATE_EVENTS),
        "event_count": len(LATE_EVENTS),
        "pbar_q": [str(value) for value in pbar],
        "normalization": str(sum(pbar, Decimal(0))),
    }


def classification_geometry(classification: Any) -> tuple[Decimal, Decimal] | None:
    if not isinstance(classification, Mapping):
        return None
    gap = classification.get("gap_power_fit")
    if not isinstance(gap, Mapping) or "exponent" not in gap or "chi_power_exponent_y" not in classification:
        return None
    return (
        decimal_value(gap["exponent"], "geometry z"),
        decimal_value(classification["chi_power_exponent_y"], "geometry y"),
    )


def in_geometry_window(pair: tuple[Decimal, Decimal] | None) -> bool:
    return pair is not None and all(GEOMETRY_LOWER <= value <= GEOMETRY_UPPER for value in pair)


def atom_audit(stage6: Mapping[str, Any]) -> dict[str, Any]:
    demand(
        stage6.get("classification") == "AUTHENTICATED_RELATIONAL_Z1_REJECTED_L4_L12",
        "Stage-6R2 predecessor is not the pinned rejection",
    )
    rows = stage6.get("atom_results")
    demand(isinstance(rows, list) and len(rows) == 24, "Stage-6R2 atom census is not 24")
    by_id: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        demand(isinstance(row, Mapping) and isinstance(row.get("atom"), Mapping), "malformed Stage-6 atom")
        atom_id = row["atom"].get("atom_id")
        demand(isinstance(atom_id, str) and atom_id not in by_id, "malformed or duplicate atom ID")
        by_id[atom_id] = row

    def describe(atom_id: str) -> dict[str, Any]:
        demand(atom_id in by_id, f"Stage-6 endpoint {atom_id} absent")
        row = by_id[atom_id]
        qmap = row["atom"].get("q_by_L")
        demand(isinstance(qmap, Mapping) and type(qmap.get("12")) is int, f"{atom_id} L12 q absent")
        target_pair = classification_geometry(row.get("target_classification"))
        blind_pair = classification_geometry(row.get("blind_classification"))
        target = row.get("target_classification")
        blind = row.get("blind_classification")
        target_failed = (
            sorted(key for key, value in target.get("checks", {}).items() if value is False)
            if isinstance(target, Mapping)
            else []
        )
        blind_failed = (
            sorted(key for key, value in blind.get("checks", {}).items() if value is False)
            if isinstance(blind, Mapping)
            else []
        )
        return {
            "atom_id": atom_id,
            "q_at_L12": qmap["12"],
            "target_z_y": [str(value) for value in target_pair] if target_pair else None,
            "blind_z_y": [str(value) for value in blind_pair] if blind_pair else None,
            "target_blind_geometry_window_pass": in_geometry_window(target_pair) and in_geometry_window(blind_pair),
            "original_stage6_atom_pass": row.get("passes") is True,
            "target_full_classifier_pass": isinstance(target, Mapping) and target.get("passes") is True,
            "blind_full_classifier_pass": isinstance(blind, Mapping) and blind.get("passes") is True,
            "target_failed_checks": target_failed,
            "blind_failed_checks": blind_failed,
            "stage6_failures": row.get("failures"),
        }

    endpoints = [describe("A011"), describe("A016")]
    demand(endpoints[0]["q_at_L12"] == 4 and endpoints[1]["q_at_L12"] == 6, "endpoint sectors changed")
    demand(all(item["target_blind_geometry_window_pass"] for item in endpoints), "endpoint geometry window no longer passes")
    q5: list[dict[str, Any]] = []
    for atom_id, row in sorted(by_id.items()):
        qmap = row["atom"].get("q_by_L")
        if not isinstance(qmap, Mapping) or qmap.get("12") != 5:
            continue
        target_pair = classification_geometry(row.get("target_classification"))
        blind_pair = classification_geometry(row.get("blind_classification"))
        q5.append(
            {
                "atom_id": atom_id,
                "target_blind_geometry_window_pass": in_geometry_window(target_pair) and in_geometry_window(blind_pair),
                "original_stage6_atom_pass": row.get("passes") is True,
            }
        )
    demand(q5, "no q5 atoms in Stage-6R2")
    return {
        "predecessor_classification": stage6["classification"],
        "endpoints": endpoints,
        "q5_atoms": q5,
        "q5_geometry_window_pass_count": sum(item["target_blind_geometry_window_pass"] for item in q5),
        "q5_original_stage6_pass_count": sum(item["original_stage6_atom_pass"] for item in q5),
        "both_endpoints_pass_original_full_gate": all(item["original_stage6_atom_pass"] for item in endpoints),
    }


def flow_audit(report: Mapping[str, Any]) -> dict[str, Any]:
    demand(report.get("status") == "PASS", "record-flow sidecar status is not PASS")
    demand(
        report.get("classification") == "AUTHENTICATED_L12_RECORD_FLOW_SECTOR_BRIDGE",
        "record-flow sidecar classification changed",
    )
    topology = report.get("typed_topology")
    mass = report.get("mass")
    conclusion = report.get("conclusion")
    demand(isinstance(topology, Mapping) and isinstance(mass, Mapping), "record-flow topology or mass absent")
    demand(isinstance(conclusion, Mapping), "record-flow conclusion absent")
    demand(
        topology.get("exact_bridge_path") == ["A011", "L12:Q04", "L12:Q05", "L12:Q06", "A016"],
        "record-flow typed path changed",
    )
    demand(topology.get("contiguous_under_record_flow") is True, "record-flow path not contiguous")
    edges = topology.get("certified_sector_flow_edges")
    demand(isinstance(edges, list) and len(edges) == 2, "record-flow edge census is not two")
    expected = ["L12:Q04->L12:Q05", "L12:Q05->L12:Q06"]
    for edge, name in zip(edges, expected):
        demand(isinstance(edge, Mapping) and edge.get("edge") == name and edge.get("certified") is True, f"flow edge {name} not certified")
        demand(edge.get("target_positive") is True and edge.get("hostile_positive") is True, f"flow edge {name} not independently positive")
        demand(edge.get("cross_branch_agreement") is True, f"flow edge {name} lacks cross-branch agreement")
    demand(conclusion.get("stage6_frozen_result_modified") is False, "flow sidecar claims a Stage-6 overwrite")
    return {
        "typed_path": topology["exact_bridge_path"],
        "edges": [
            {
                "edge": edge["edge"],
                "target_flow": str(decimal_value(edge["target_transferred_norm_squared"], "target flow")),
                "hostile_flow": str(decimal_value(edge["hostile_transferred_norm_squared"], "hostile flow")),
                "certified": True,
            }
            for edge in edges
        ],
        "mass": {
            "q4": str(decimal_value(mass.get("q4"), "q4 mass")),
            "q5": str(decimal_value(mass.get("q5"), "q5 mass")),
            "q6": str(decimal_value(mass.get("q6"), "q6 mass")),
            "triad": str(decimal_value(mass.get("deduplicated_q4_q5_q6"), "triad mass")),
        },
    }


def evaluate_rules(atoms: Mapping[str, Any], flow: Mapping[str, Any], pbar: Mapping[str, Any]) -> dict[str, Any]:
    pbar_values = [decimal_value(value, f"pbar q={q}") for q, value in enumerate(pbar["pbar_q"])]
    flow_mass = flow["mass"]
    declared_masses: dict[int, Decimal] = {}
    reconstruction_differences: dict[str, str] = {}
    for q, observed in ((4, pbar_values[4]), (5, pbar_values[5]), (6, pbar_values[6])):
        declared = decimal_value(flow_mass[f"q{q}"], f"sidecar q{q} mass")
        demand(abs(observed - declared) <= NUMERIC_TOLERANCE, f"sidecar q{q} mass does not match reconstructed pbar")
        declared_masses[q] = declared
        reconstruction_differences[f"q{q}"] = str(abs(observed - declared))
    q4, q5, q6 = declared_masses[4], declared_masses[5], declared_masses[6]
    endpoint_mass = q4 + q6
    required_q5 = max(Decimal(0), MASS_THRESHOLD - endpoint_mass)
    triad = q4 + q5 + q6
    flow_values = [decimal_value(edge["target_flow"], "flow value") for edge in flow["edges"]]
    bottleneck = min(flow_values)
    naive_supported_total = endpoint_mass + bottleneck
    q5_required_fraction = required_q5 / q5 if q5 > 0 else Decimal("Infinity")

    original_endpoint_pass = bool(atoms["both_endpoints_pass_original_full_gate"])
    q5_full_pass_count = int(atoms["q5_original_stage6_pass_count"])
    whole_admissible = False
    conservative_commensurable = False
    common_lineage_proven = False
    return {
        "shared_arithmetic": {
            "mass_source": "authenticated Stage-5 pbar_q values carried by the flow sidecar",
            "independent_history_reconstruction_absolute_difference": reconstruction_differences,
            "q4_plus_q6_endpoint_sector_mass": str(endpoint_mass),
            "additional_q5_mass_required_for_0_50": str(required_q5),
            "fraction_of_q5_required": str(q5_required_fraction),
        },
        "whole_sector_connectivity_rule": {
            "rule": "include all q5 pbar mass when the typed q4--q5--q6 sector graph is connected",
            "record_flow_graph_connected": True,
            "deduplicated_mass": str(triad),
            "arithmetic_threshold_crossed": triad >= MASS_THRESHOLD,
            "preregistered_by_stage6_protocol": False,
            "endpoints_pass_original_stage6_full_conjunction": original_endpoint_pass,
            "q5_atoms_passing_original_stage6_full_conjunction": q5_full_pass_count,
            "admissible_as_stage6_candidate": whole_admissible,
            "classification": "ARITHMETIC_PASS__UNADOPTED_AGGREGATION_AND_ENDPOINT_RULES",
            "reason": (
                "The frozen protocol groups only fully passing adjacent density atoms. "
                "A011 and A016 pass the exploratory z/y window but fail the original full "
                "classifier, and no q5 atom passes. Sector-flow connectivity is not a "
                "preregistered substitute for those predicates."
            ),
        },
        "conservative_flow_support_rule": {
            "rule": "include only q5 mass authenticated as common q4--q5--q6 lineage support",
            "pbar_measure": "late-event mean of complete sector weights over events 6--12",
            "flow_measure": "source-sector component norm transferred at terminal event 12",
            "same_measure_or_conversion_theorem_authenticated": conservative_commensurable,
            "common_lineage_intersection_authenticated": common_lineage_proven,
            "certified_supported_q5_mass": None,
            "certified_total_mass": None,
            "threshold_disposition": "UNRESOLVED_FAIL_CLOSED",
            "diagnostic_only_if_measures_were_assumed_commensurable": {
                "minimum_of_two_terminal_flows": str(bottleneck),
                "q4_plus_q6_plus_flow_minimum": str(naive_supported_total),
                "threshold_crossed": naive_supported_total >= MASS_THRESHOLD,
                "shortfall": str(max(Decimal(0), MASS_THRESHOLD - naive_supported_total)),
                "not_a_gate_value": True,
            },
            "reason": (
                "The two terminal flows originate in different prefix sectors and are "
                "simultaneous components of event 12. The sidecar contains no atom- or "
                "lineage-resolved intersection proving that the same q5 mass links both "
                "edges. Terminal component norms also cannot be added to late-event pbar "
                "without an authenticated conversion law."
            ),
        },
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    artifacts = {
        "stage6r2": authenticate(args.stage6r2, PINNED_SHA256["stage6r2"], "stage6r2", True),
        "flow_report": authenticate(args.flow_report, PINNED_SHA256["flow_report"], "flow_report", True),
        "target_history": authenticate(args.target_history, PINNED_SHA256["target_history"], "target_history", True),
        "protocol": authenticate(args.protocol, PINNED_SHA256["protocol"], "protocol", False),
        "driver": authenticate(args.driver, PINNED_SHA256["driver"], "driver", False),
        "manifest_builder": authenticate(
            args.manifest_builder,
            PINNED_SHA256["manifest_builder"],
            "manifest_builder",
            False,
        ),
    }
    stage6 = artifacts["stage6r2"].json
    flow_report = artifacts["flow_report"].json
    target_history = artifacts["target_history"].json
    assert stage6 is not None and flow_report is not None and target_history is not None
    pbar = reconstruct_late_pbar(target_history)
    atoms = atom_audit(stage6)
    flow = flow_audit(flow_report)
    rules = evaluate_rules(atoms, flow, pbar)
    whole = rules["whole_sector_connectivity_rule"]
    conservative = rules["conservative_flow_support_rule"]
    demand(whole["arithmetic_threshold_crossed"] is True, "whole-sector diagnostic no longer crosses 0.50")
    demand(whole["admissible_as_stage6_candidate"] is False, "unadopted whole-sector rule became admissible")
    demand(conservative["threshold_disposition"] == "UNRESOLVED_FAIL_CLOSED", "conservative rule did not fail closed")
    return {
        "schema": SCHEMA,
        "status": "COMPLETE_FAIL_CLOSED_SUPPLEMENTAL_ADJUDICATION",
        "classification": "STAGE6R3_RECORD_FLOW_OBSERVED__ORIGINAL_Z1_GATE_REMAINS_REJECTED",
        "authenticated_inputs": [
            {"label": artifact.label, "path": str(artifact.path), "sha256": artifact.sha256}
            for artifact in artifacts.values()
        ],
        "predecessor": {
            "classification": stage6["classification"],
            "modified": False,
        },
        "probability_semantics": {
            "pbar": pbar,
            "record_flow": {
                "event": 12,
                "definition": "sin(pi/4)^2 times selected prefix_11 source-sector norm squared",
                "composed_lineage_intersection_present": False,
            },
            "direct_addition_authorized": False,
        },
        "atom_gate_audit": atoms,
        "flow_sidecar_audit": flow,
        "aggregation_rules": rules,
        "stage7_gate": {
            "authorized": False,
            "classification": "NOT_AUTHORIZED_FROM_STAGE6R3",
            "blocking_conditions": [
                "whole-sector membership is not an adopted Stage-6 rule",
                "A011 and A016 fail the original full Stage-6 conjunction despite passing z/y",
                "no q5 atom passes the original full Stage-6 conjunction",
                "terminal flow norms are not proven commensurable with late-event pbar mass",
                "no common q5 lineage intersection is preserved",
            ],
        },
        "closure_options": [
            {
                "option": "THEOREM_PATH",
                "requirement": (
                    "prove and independently audit a record-block membership theorem that "
                    "both replaces the original endpoint/full-conjunction rule and justifies "
                    "whole-sector pbar aggregation from typed sector flow"
                ),
                "new_numerical_solve_required": False,
            },
            {
                "option": "NUMERICAL_LINEAGE_PATH",
                "requirement": (
                    "compute authenticated event-6--12 lineage-resolved q5 support with a "
                    "common q4-to-q6 intersection on the same pbar measure"
                ),
                "new_numerical_solve_required": True,
            },
            {
                "option": "NEXT_SIZE_PATH",
                "requirement": (
                    "run a preregistered L14 scout for fully passing q5-region density atoms; "
                    "do not use the present sidecar as a Stage-6 pass"
                ),
                "new_numerical_solve_required": True,
            },
        ],
        "claim_boundary": (
            "FINITE_L12_SUPPLEMENTAL_ADJUDICATION_ONLY__NO_RELAXATION_OR_OVERWRITE_OF_"
            "STAGE6R2__NO_STAGE7_AUTHORIZATION__NO_EXACT_Z1_CONTINUUM_GRAVITY_OR_"
            "ENTANGLEMENT_CLAIM"
        ),
        "script": {
            "path": str(Path(__file__).resolve()),
            "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--stage6r2", type=Path, default=DEFAULT_STAGE6)
    result.add_argument("--flow-report", type=Path, default=DEFAULT_FLOW_REPORT)
    result.add_argument("--target-history", type=Path, default=DEFAULT_TARGET_HISTORY)
    result.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    result.add_argument("--driver", type=Path, default=DEFAULT_DRIVER)
    result.add_argument("--manifest-builder", type=Path, default=DEFAULT_MANIFEST_BUILDER)
    result.add_argument("--output", type=Path, default=None)
    return result


def print_summary(report: Mapping[str, Any]) -> None:
    rules = report["aggregation_rules"]
    shared = rules["shared_arithmetic"]
    whole = rules["whole_sector_connectivity_rule"]
    conservative = rules["conservative_flow_support_rule"]
    diagnostic = conservative["diagnostic_only_if_measures_were_assumed_commensurable"]
    print(f"CLASSIFICATION={report['classification']}")
    print(
        "WHOLE_SECTOR_RULE "
        f"mass={whole['deduplicated_mass']} arithmetic_pass={str(whole['arithmetic_threshold_crossed']).upper()} "
        f"stage6_admissible={str(whole['admissible_as_stage6_candidate']).upper()}"
    )
    print(
        "CONSERVATIVE_RULE "
        f"required_q5={shared['additional_q5_mass_required_for_0_50']} "
        f"certified_q5={conservative['certified_supported_q5_mass']} "
        f"disposition={conservative['threshold_disposition']}"
    )
    print(
        "NON_GATE_DIAGNOSTIC "
        f"endpoint_plus_flow_min={diagnostic['q4_plus_q6_plus_flow_minimum']} "
        f"crossed={str(diagnostic['threshold_crossed']).upper()} "
        f"shortfall={diagnostic['shortfall']}"
    )
    print(f"STAGE7_AUTHORIZED={str(report['stage7_gate']['authorized']).upper()}")


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        report = build_report(args)
        rendered = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
        if args.output is not None:
            if args.output.exists():
                raise Refusal(f"refuse to overwrite existing output: {args.output}")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(rendered)
                stream.flush()
                os.fsync(stream.fileno())
            print(f"REPORT_PATH={args.output.resolve()}")
            print(f"REPORT_SHA256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")
        print_summary(report)
        return 0
    except (Refusal, OSError, KeyError, TypeError, ValueError) as error:
        print(f"AUTHENTICATION_FAILURE: {error}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
