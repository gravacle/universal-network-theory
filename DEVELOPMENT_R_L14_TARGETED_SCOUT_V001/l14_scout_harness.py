#!/usr/bin/env python3
"""Fail-closed two-phase orchestration for a targeted L14 geometry scout.

The numerical solver is intentionally an external adapter.  It receives an
owner-once JSON request through ``--request`` and must publish an owner-once
JSON result through ``--output``.  This harness never substitutes estimates
for numerical output and never opens q=8 or q=9 unless the Phase-2 gate passes.

Important density correction
----------------------------
The L12 q=5 cell is [3/16, 11/48).  At L14 this density support is divided by
the q=5/q=6 boundary 11/56.  Therefore a literal L14-q=5 test is not a test of
the whole former L12-q=5 void.  The gate reports literal q=5 status, but also
requires a consensus-passing, contiguous atom block to cover the exact former
L12-q=5 density support.  This prevents a q-label shift from creating a false
bridge result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


LENGTH = 14
PHASE1_SECTORS = (4, 5, 6, 7)
PHASE3_SECTORS = (8, 9)
ALL_SCOUT_SECTORS = PHASE1_SECTORS + PHASE3_SECTORS
GEOMETRY_MIN = Decimal("0.90")
GEOMETRY_MAX = Decimal("1.10")
DEFAULT_THRESHOLD = Decimal("0.50")
DEFAULT_WALL_SECONDS = 96 * 3600
L12_Q5_SUPPORT = (Fraction(3, 16), Fraction(11, 48))
L14_Q5_Q6_BOUNDARY = Fraction(11, 56)
REQUEST_SCHEMA = "L14_TARGETED_SCOUT_SOLVER_REQUEST_V001"
RESULT_SCHEMA = "L14_TARGETED_SCOUT_SOLVER_RESULT_V001"
REPORT_SCHEMA = "L14_TARGETED_SCOUT_GATE_REPORT_V001"


class ScoutRefusal(RuntimeError):
    """The adapter output or orchestration contract failed closed."""


@dataclass(frozen=True)
class Geometry:
    resolved: bool
    z: Decimal
    y: Decimal


@dataclass(frozen=True)
class Atom:
    atom_id: str
    q: int
    interval: Tuple[Fraction, Fraction]
    target: Geometry
    blind: Geometry

    def passes(self, lower: Decimal, upper: Decimal) -> bool:
        return (
            self.target.resolved
            and self.blind.resolved
            and lower <= self.target.z <= upper
            and lower <= self.target.y <= upper
            and lower <= self.blind.z <= upper
            and lower <= self.blind.y <= upper
        )


@dataclass(frozen=True)
class PhaseResult:
    phase: str
    sectors: Tuple[int, ...]
    masses: Mapping[int, Decimal]
    atoms: Tuple[Atom, ...]
    source_path: Path
    source_sha256: str


@dataclass(frozen=True)
class GateDecision:
    proceed: bool
    reasons: Tuple[str, ...]
    q5_has_passing_atom: bool
    q6_has_passing_atom: bool
    bridge_support_contiguously_covered: bool
    phase1_passing_sectors: Tuple[int, ...]
    phase1_passing_mass: Decimal
    unopened_tail_upper_bound: Decimal
    optimistic_total_upper_bound: Decimal
    passing_blocks: Tuple[Tuple[str, ...], ...]


def decimal_value(value: Any, label: str) -> Decimal:
    if isinstance(value, bool):
        raise ScoutRefusal("{} must be numeric, not boolean".format(label))
    try:
        result = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ScoutRefusal("{} is not a finite decimal".format(label)) from exc
    if not result.is_finite():
        raise ScoutRefusal("{} is not finite".format(label))
    return result


def fraction_value(value: Any, label: str) -> Fraction:
    if not isinstance(value, list) or len(value) != 2:
        raise ScoutRefusal("{} must be [numerator, denominator]".format(label))
    if type(value[0]) is not int or type(value[1]) is not int or value[1] <= 0:
        raise ScoutRefusal("{} must be a positive-denominator integer pair".format(label))
    fraction = Fraction(value[0], value[1])
    if fraction.numerator != value[0] or fraction.denominator != value[1]:
        raise ScoutRefusal("{} must be reduced".format(label))
    return fraction


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def owner_once_json(path: Path, value: Any) -> None:
    """Publish one durable JSON file without overwriting prior evidence."""

    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(path, flags, 0o400)
    try:
        payload = canonical_json(value)
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            if written <= 0:
                raise ScoutRefusal("owner-once write made no progress")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
    finally:
        os.close(descriptor)


def load_json(path: Path) -> Mapping[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle, parse_float=Decimal)
    except (OSError, json.JSONDecodeError) as exc:
        raise ScoutRefusal("cannot read JSON {}: {}".format(path, exc)) from exc
    if not isinstance(value, Mapping):
        raise ScoutRefusal("{} must contain a JSON object".format(path))
    return value


def parse_geometry(value: Any, label: str) -> Geometry:
    if not isinstance(value, Mapping):
        raise ScoutRefusal("{} geometry object absent".format(label))
    resolved = value.get("resolved")
    if type(resolved) is not bool:
        raise ScoutRefusal("{}.resolved must be boolean".format(label))
    return Geometry(
        resolved=resolved,
        z=decimal_value(value.get("z"), "{}.z".format(label)),
        y=decimal_value(value.get("y"), "{}.y".format(label)),
    )


def parse_atom(value: Any, allowed_sectors: Set[int], ordinal: int) -> Atom:
    label = "atoms[{}]".format(ordinal)
    if not isinstance(value, Mapping):
        raise ScoutRefusal("{} must be an object".format(label))
    atom_id = value.get("atom_id")
    q = value.get("q")
    interval = value.get("density_interval")
    if not isinstance(atom_id, str) or not atom_id:
        raise ScoutRefusal("{}.atom_id absent".format(label))
    if type(q) is not int or q not in allowed_sectors:
        raise ScoutRefusal("{}.q lies outside computed sectors".format(label))
    if not isinstance(interval, list) or len(interval) != 2:
        raise ScoutRefusal("{}.density_interval malformed".format(label))
    left = fraction_value(interval[0], "{}.density_interval.left".format(label))
    right = fraction_value(interval[1], "{}.density_interval.right".format(label))
    if not left < right:
        raise ScoutRefusal("{}.density_interval is empty or reversed".format(label))
    return Atom(
        atom_id=atom_id,
        q=q,
        interval=(left, right),
        target=parse_geometry(value.get("target"), "{}.target".format(label)),
        blind=parse_geometry(value.get("blind"), "{}.blind".format(label)),
    )


def validate_atoms(atoms: Sequence[Atom]) -> None:
    ids = [atom.atom_id for atom in atoms]
    if len(ids) != len(set(ids)):
        raise ScoutRefusal("duplicate atom_id in phase result")
    ordered = sorted(atoms, key=lambda atom: (atom.interval[0], atom.interval[1], atom.atom_id))
    for previous, current in zip(ordered, ordered[1:]):
        if current.interval[0] < previous.interval[1]:
            raise ScoutRefusal(
                "overlapping atom intervals: {} and {}".format(previous.atom_id, current.atom_id)
            )


def parse_phase_result(path: Path, expected_phase: str, expected_sectors: Tuple[int, ...]) -> PhaseResult:
    payload = load_json(path)
    if payload.get("schema") != RESULT_SCHEMA:
        raise ScoutRefusal("{} schema mismatch".format(path))
    if payload.get("length") != LENGTH or payload.get("phase") != expected_phase:
        raise ScoutRefusal("{} phase identity mismatch".format(path))
    raw_sectors = payload.get("computed_sectors")
    if not isinstance(raw_sectors, list) or tuple(raw_sectors) != expected_sectors:
        raise ScoutRefusal("{} computed sector census mismatch".format(path))
    validation = payload.get("validation")
    if not isinstance(validation, Mapping):
        raise ScoutRefusal("{} validation object absent".format(path))
    if validation.get("all_original_numerical_predicates_pass") is not True:
        raise ScoutRefusal("{} has unresolved or failed numerical predicates".format(path))
    if validation.get("target_blind_authenticated") is not True:
        raise ScoutRefusal("{} target/blind authentication did not pass".format(path))

    raw_masses = payload.get("sector_masses")
    if not isinstance(raw_masses, Mapping):
        raise ScoutRefusal("{} sector_masses absent".format(path))
    masses: Dict[int, Decimal] = {}
    for raw_q, raw_mass in raw_masses.items():
        try:
            q = int(raw_q)
        except (TypeError, ValueError) as exc:
            raise ScoutRefusal("{} has malformed sector key".format(path)) from exc
        if str(q) != str(raw_q):
            raise ScoutRefusal("{} sector key must be canonical integer text".format(path))
        mass = decimal_value(raw_mass, "sector_masses[{}]".format(q))
        if not Decimal(0) <= mass <= Decimal(1):
            raise ScoutRefusal("sector q={} mass lies outside [0,1]".format(q))
        masses[q] = mass
    required_mass_sectors = set(ALL_SCOUT_SECTORS if expected_phase == "bridge" else PHASE3_SECTORS)
    if not required_mass_sectors <= set(masses):
        raise ScoutRefusal(
            "{} missing mass-ledger sectors {}".format(path, sorted(required_mass_sectors - set(masses)))
        )
    if sum((masses[q] for q in required_mass_sectors), Decimal(0)) > Decimal(1) + Decimal("1e-12"):
        raise ScoutRefusal("partial sector masses exceed total probability one")

    raw_atoms = payload.get("atoms")
    if not isinstance(raw_atoms, list):
        raise ScoutRefusal("{} atoms array absent".format(path))
    atoms = tuple(
        parse_atom(value, set(expected_sectors), ordinal)
        for ordinal, value in enumerate(raw_atoms)
    )
    validate_atoms(atoms)
    unresolved = [
        atom.atom_id
        for atom in atoms
        if not atom.target.resolved or not atom.blind.resolved
    ]
    if unresolved:
        raise ScoutRefusal(
            "{} contains unresolved geometry atoms: {}".format(path, unresolved)
        )
    return PhaseResult(
        phase=expected_phase,
        sectors=expected_sectors,
        masses=masses,
        atoms=atoms,
        source_path=path.resolve(),
        source_sha256=sha256_file(path),
    )


def passing_atoms(
    atoms: Iterable[Atom], lower: Decimal = GEOMETRY_MIN, upper: Decimal = GEOMETRY_MAX
) -> List[Atom]:
    return [atom for atom in atoms if atom.passes(lower, upper)]


def passing_blocks(atoms: Iterable[Atom]) -> List[List[Atom]]:
    """Return maximal exactly touching blocks among consensus-passing atoms."""

    ordered = sorted(atoms, key=lambda atom: (atom.interval[0], atom.interval[1]))
    if not ordered:
        return []
    blocks: List[List[Atom]] = [[ordered[0]]]
    for atom in ordered[1:]:
        if atom.interval[0] == blocks[-1][-1].interval[1]:
            blocks[-1].append(atom)
        else:
            blocks.append([atom])
    return blocks


def block_covers(block: Sequence[Atom], support: Tuple[Fraction, Fraction]) -> bool:
    return bool(block) and block[0].interval[0] <= support[0] and block[-1].interval[1] >= support[1]


def sum_unique_mass(sectors: Iterable[int], masses: Mapping[int, Decimal]) -> Decimal:
    unique = set(sectors)
    missing = unique - set(masses)
    if missing:
        raise ScoutRefusal("mass absent for sectors {}".format(sorted(missing)))
    return sum((masses[q] for q in unique), Decimal(0))


def evaluate_phase2(
    phase1: PhaseResult,
    threshold: Decimal = DEFAULT_THRESHOLD,
    lower: Decimal = GEOMETRY_MIN,
    upper: Decimal = GEOMETRY_MAX,
) -> GateDecision:
    matches = passing_atoms(phase1.atoms, lower, upper)
    blocks = passing_blocks(matches)
    q5_hit = any(atom.q == 5 for atom in matches)
    q6_hit = any(atom.q == 6 for atom in matches)
    bridge_covered = any(block_covers(block, L12_Q5_SUPPORT) for block in blocks)
    passing_q = tuple(sorted({atom.q for atom in matches}))
    phase1_mass = sum_unique_mass(passing_q, phase1.masses)
    tail_upper = sum_unique_mass(PHASE3_SECTORS, phase1.masses)
    optimistic = phase1_mass + tail_upper

    reasons: List[str] = []
    if not q5_hit:
        reasons.append("L14_Q5_STERILE")
    if not q6_hit:
        reasons.append("L12_Q5_DENSITY_CORE_STERILE_AT_L14_Q6")
    if not bridge_covered:
        reasons.append("NO_CONTIGUOUS_COVERAGE_OF_L12_Q5_DENSITY_SUPPORT")
    if optimistic < threshold:
        reasons.append("Q8_Q9_CANNOT_REACH_THRESHOLD_EVEN_IF_BOTH_PASS")
    return GateDecision(
        proceed=not reasons,
        reasons=tuple(reasons),
        q5_has_passing_atom=q5_hit,
        q6_has_passing_atom=q6_hit,
        bridge_support_contiguously_covered=bridge_covered,
        phase1_passing_sectors=passing_q,
        phase1_passing_mass=phase1_mass,
        unopened_tail_upper_bound=tail_upper,
        optimistic_total_upper_bound=optimistic,
        passing_blocks=tuple(tuple(atom.atom_id for atom in block) for block in blocks),
    )


def request_payload(phase: str, sectors: Tuple[int, ...], resume: Optional[PhaseResult]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "schema": REQUEST_SCHEMA,
        "length": LENGTH,
        "phase": phase,
        "sectors": list(sectors),
        "mass_ledger_sectors": list(ALL_SCOUT_SECTORS if phase == "bridge" else PHASE3_SECTORS),
        "geometry_history_sizes": [4, 6, 8, 10, 12, 14],
        "geometry_window": {"z": ["0.90", "1.10"], "y": ["0.90", "1.10"]},
        "classification_policy": "TARGET_AND_BLIND_CONSENSUS",
        "numerical_policy": "ALL_ORIGINAL_PREDICATES_MUST_PASS_NO_OVERRIDE",
        "probability_policy": "DEDUPLICATE_BY_Q_BEFORE_SUM",
    }
    if resume is not None:
        payload["resume"] = {
            "phase1_result_path": str(resume.source_path),
            "phase1_result_sha256": resume.source_sha256,
        }
    return payload


def run_solver(
    solver: Path,
    request: Path,
    output: Path,
    log_path: Path,
    wall_seconds: int,
) -> None:
    if output.exists() or output.is_symlink():
        raise ScoutRefusal("solver output already exists: {}".format(output))
    command = ([sys.executable, "-B", str(solver)] if solver.suffix == ".py" else [str(solver)])
    command.extend(["--request", str(request), "--output", str(output)])
    started = time.monotonic()
    log_descriptor = os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        with os.fdopen(log_descriptor, "w", encoding="utf-8", closefd=True) as log_handle:
            log_descriptor = -1
            log_handle.write("L14_SCOUT_SOLVER_COMMAND {}\n".format(json.dumps(command)))
            log_handle.flush()
            try:
                completed = subprocess.run(
                    command,
                    cwd=str(solver.resolve().parent),
                    stdout=log_handle,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=wall_seconds,
                    check=False,
                )
            except subprocess.TimeoutExpired as exc:
                log_handle.write(
                    "\nL14_SCOUT_SOLVER_WALL_CEILING_EXCEEDED elapsed_seconds={:.6f}\n".format(
                        time.monotonic() - started
                    )
                )
                log_handle.flush()
                os.fsync(log_handle.fileno())
                os.fchmod(log_handle.fileno(), 0o444)
                raise ScoutRefusal(
                    "solver exceeded {} second wall ceiling".format(wall_seconds)
                ) from exc
            log_handle.write(
                "\nL14_SCOUT_SOLVER_EXIT return_code={} elapsed_seconds={:.6f}\n".format(
                    completed.returncode, time.monotonic() - started
                )
            )
            log_handle.flush()
            os.fsync(log_handle.fileno())
            os.fchmod(log_handle.fileno(), 0o444)
    finally:
        if log_descriptor >= 0:
            os.close(log_descriptor)
    if completed.returncode != 0:
        raise ScoutRefusal("solver returned {} (see {})".format(completed.returncode, log_path))
    if not output.is_file():
        raise ScoutRefusal("solver returned success without publishing {}".format(output))


def decimal_text(value: Decimal) -> str:
    return format(value, ".16g")


def fraction_text(value: Fraction) -> str:
    return "{}/{}".format(value.numerator, value.denominator)


def print_phase2(decision: GateDecision, threshold: Decimal) -> None:
    print(
        "L14_SCOUT_GATE_Q5 status={} note=literal_L14_q5".format(
            "PASSING_ATOM_PRESENT" if decision.q5_has_passing_atom else "STERILE"
        ),
        flush=True,
    )
    print(
        "L14_SCOUT_GATE_DENSITY_CORE l12_q5_support=[{},{}) split_at_L14={} "
        "q6_status={} contiguous_coverage={}".format(
            fraction_text(L12_Q5_SUPPORT[0]),
            fraction_text(L12_Q5_SUPPORT[1]),
            fraction_text(L14_Q5_Q6_BOUNDARY),
            "PASSING_ATOM_PRESENT" if decision.q6_has_passing_atom else "STERILE",
            str(decision.bridge_support_contiguously_covered).lower(),
        ),
        flush=True,
    )
    print(
        "L14_SCOUT_GATE_MASS passing_sectors={} phase1_deduplicated_mass={} "
        "q8_q9_max_additional_mass={} optimistic_total_upper_bound={} threshold={}".format(
            list(decision.phase1_passing_sectors),
            decimal_text(decision.phase1_passing_mass),
            decimal_text(decision.unopened_tail_upper_bound),
            decimal_text(decision.optimistic_total_upper_bound),
            decimal_text(threshold),
        ),
        flush=True,
    )
    print("L14_SCOUT_GATE_BLOCKS {}".format([list(block) for block in decision.passing_blocks]), flush=True)
    if decision.proceed:
        print("L14_SCOUT_DECISION PROCEED phase3_sectors=[8,9]", flush=True)
    else:
        print("L14_SCOUT_DECISION HALT reasons={}".format(list(decision.reasons)), flush=True)


def report_value(
    classification: str,
    phase1: PhaseResult,
    decision: GateDecision,
    threshold: Decimal,
    phase3: Optional[PhaseResult] = None,
) -> Dict[str, Any]:
    value: Dict[str, Any] = {
        "schema": REPORT_SCHEMA,
        "classification": classification,
        "length": LENGTH,
        "threshold": str(threshold),
        "phase1": {"path": str(phase1.source_path), "sha256": phase1.source_sha256},
        "gate": {
            "proceed": decision.proceed,
            "reasons": list(decision.reasons),
            "q5_has_passing_atom": decision.q5_has_passing_atom,
            "q6_has_passing_atom": decision.q6_has_passing_atom,
            "bridge_support": [
                [L12_Q5_SUPPORT[0].numerator, L12_Q5_SUPPORT[0].denominator],
                [L12_Q5_SUPPORT[1].numerator, L12_Q5_SUPPORT[1].denominator],
            ],
            "bridge_support_contiguously_covered": decision.bridge_support_contiguously_covered,
            "phase1_passing_sectors": list(decision.phase1_passing_sectors),
            "phase1_passing_mass": str(decision.phase1_passing_mass),
            "unopened_tail_upper_bound": str(decision.unopened_tail_upper_bound),
            "optimistic_total_upper_bound": str(decision.optimistic_total_upper_bound),
            "passing_blocks": [list(block) for block in decision.passing_blocks],
        },
        "claim_boundary": "TARGETED_FINITE_L14_SCOUT_ONLY__NO_LIMIT_CONTINUUM_GRAVITY_OR_STAGE7_CLAIM",
    }
    if phase3 is not None:
        value["phase3"] = {"path": str(phase3.source_path), "sha256": phase3.source_sha256}
    return value


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--solver", type=Path, help="adapter receiving --request and --output")
    parser.add_argument("--phase1-result", type=Path, help="authenticate/evaluate existing Phase-1 output")
    parser.add_argument("--phase3-result", type=Path, help="authenticate/evaluate existing Phase-3 output")
    parser.add_argument("--threshold", type=str, default="0.50")
    parser.add_argument("--wall-seconds", type=int, default=DEFAULT_WALL_SECONDS)
    parser.add_argument("--preflight", action="store_true", help="print contract without creating files or launching")
    args = parser.parse_args(argv)

    threshold = decimal_value(args.threshold, "threshold")
    if not Decimal(0) <= threshold <= Decimal(1):
        raise ScoutRefusal("threshold must lie in [0,1]")
    if args.wall_seconds <= 0 or args.wall_seconds > DEFAULT_WALL_SECONDS:
        raise ScoutRefusal("wall-seconds must lie in (0, 345600]")
    if args.preflight:
        print(
            "L14_SCOUT_PREFLIGHT phase1={} phase3={} bridge_support=[{},{}) "
            "l14_split={} threshold={} launch_attempted=false".format(
                list(PHASE1_SECTORS), list(PHASE3_SECTORS),
                fraction_text(L12_Q5_SUPPORT[0]), fraction_text(L12_Q5_SUPPORT[1]),
                fraction_text(L14_Q5_Q6_BOUNDARY), decimal_text(threshold),
            )
        )
        return 0

    workspace = args.workspace.expanduser().resolve()
    if workspace.exists() or workspace.is_symlink():
        raise ScoutRefusal("workspace allocation is not fresh: {}".format(workspace))
    workspace.mkdir(parents=True, exist_ok=False)

    solver = args.solver.expanduser().resolve() if args.solver else None
    if solver is not None and not solver.is_file():
        raise ScoutRefusal("solver adapter is not a regular file: {}".format(solver))
    if args.phase1_result:
        phase1_path = args.phase1_result.expanduser().resolve()
    else:
        if solver is None:
            raise ScoutRefusal("--solver or --phase1-result is required")
        phase1_path = workspace / "PHASE1_RESULT.json"
        request1 = workspace / "PHASE1_REQUEST.json"
        owner_once_json(request1, request_payload("bridge", PHASE1_SECTORS, None))
        print("L14_SCOUT_PHASE1_START sectors={}".format(list(PHASE1_SECTORS)), flush=True)
        run_solver(solver, request1, phase1_path, workspace / "PHASE1_SOLVER.log", args.wall_seconds)
    phase1 = parse_phase_result(phase1_path, "bridge", PHASE1_SECTORS)
    print("L14_SCOUT_PHASE1_COMPLETE sha256={}".format(phase1.source_sha256), flush=True)

    decision = evaluate_phase2(phase1, threshold)
    print_phase2(decision, threshold)
    if not decision.proceed:
        owner_once_json(
            workspace / "GATE_REPORT.json",
            report_value("HALT__L14_BRIDGE_HYPOTHESIS_REJECTED", phase1, decision, threshold),
        )
        return 20

    if args.phase3_result:
        phase3_path = args.phase3_result.expanduser().resolve()
    else:
        if solver is None:
            owner_once_json(
                workspace / "GATE_REPORT.json",
                report_value("AUTHORIZED_PHASE3__NOT_EXECUTED", phase1, decision, threshold),
            )
            return 10
        phase3_path = workspace / "PHASE3_RESULT.json"
        request3 = workspace / "PHASE3_REQUEST.json"
        owner_once_json(request3, request_payload("conditional_tail", PHASE3_SECTORS, phase1))
        print("L14_SCOUT_PHASE3_START sectors={}".format(list(PHASE3_SECTORS)), flush=True)
        run_solver(solver, request3, phase3_path, workspace / "PHASE3_SOLVER.log", args.wall_seconds)
    phase3 = parse_phase_result(phase3_path, "conditional_tail", PHASE3_SECTORS)
    for q in PHASE3_SECTORS:
        if phase3.masses[q] != phase1.masses[q]:
            raise ScoutRefusal("q={} mass changed across phase boundary".format(q))

    combined_atoms = tuple(phase1.atoms) + tuple(phase3.atoms)
    validate_atoms(combined_atoms)
    combined_matches = passing_atoms(combined_atoms)
    final_q = tuple(sorted({atom.q for atom in combined_matches}))
    final_mass = sum_unique_mass(final_q, phase1.masses)
    print(
        "L14_SCOUT_FINAL passing_sectors={} deduplicated_mass={} threshold={} verdict={}".format(
            list(final_q), decimal_text(final_mass), decimal_text(threshold),
            "MEETS_OR_EXCEEDS" if final_mass >= threshold else "BELOW",
        ),
        flush=True,
    )
    final_classification = (
        "COMPLETE__L14_SCOUT_THRESHOLD_MET"
        if final_mass >= threshold
        else "COMPLETE__L14_SCOUT_THRESHOLD_NOT_MET"
    )
    report = report_value(final_classification, phase1, decision, threshold, phase3)
    report["final_passing_sectors"] = list(final_q)
    report["final_deduplicated_mass"] = str(final_mass)
    report["final_threshold_met"] = final_mass >= threshold
    report["final_passing_blocks"] = [
        [atom.atom_id for atom in block] for block in passing_blocks(combined_matches)
    ]
    owner_once_json(workspace / "GATE_REPORT.json", report)
    return 0 if final_mass >= threshold else 21


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ScoutRefusal as exc:
        print("L14_SCOUT_REFUSAL {}".format(exc), file=sys.stderr, flush=True)
        raise SystemExit(2)
