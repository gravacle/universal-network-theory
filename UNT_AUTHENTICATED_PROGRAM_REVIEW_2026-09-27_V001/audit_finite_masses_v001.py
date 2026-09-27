#!/usr/bin/env python3
"""Read-only re-summation of the frozen L4--L12 majority-mass evidence.

Uses the Python standard library only. It authenticates one manifest and ten
stored histories, independently reapplies the exact midpoint sector rule,
and averages the selected late-event probabilities with Decimal arithmetic.
It does not evolve a state, reconstruct missing inputs, or validate all of
ARGER-GATE-1. JSON goes to stdout; no files are created or modified.
"""

import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


MANIFEST = "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003/AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003R1.json"
MANIFEST_SHA256 = "292124df4e1d349827753145ce1dd4be32e073db6d657f30737227edd488184a"
SIZES = (4, 6, 8, 10, 12)
ATOM_IDS = tuple("A%03d" % number for number in range(9, 17))
EXPECTED_RANKS = {4: [1, 2], 6: [2, 3], 8: [2, 3, 4], 10: [3, 4, 5], 12: [4, 5, 6]}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strict_object(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, "duplicate JSON key: " + key)
        value[key] = item
    return value


def reject_constant(value):
    raise ValueError("nonfinite JSON value: " + value)


def read_authenticated(root, relative, expected_sha256):
    route = Path(relative)
    require(not route.is_absolute() and ".." not in route.parts, "unsafe input route")
    require(route.as_posix() == relative, "noncanonical input route")
    path = root
    for part in route.parts:
        path = path / part
        require(not path.is_symlink(), "symlink input route: " + relative)
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    require(digest == expected_sha256, "input hash mismatch: " + relative)
    parsed = json.loads(raw, parse_float=Decimal, parse_constant=reject_constant,
                        object_pairs_hook=strict_object)
    return parsed, {"path": relative, "sha256": digest, "bytes": len(raw)}


def audit(root):
    manifest, receipt = read_authenticated(root, MANIFEST, MANIFEST_SHA256)
    inputs = [receipt]
    atoms = [atom for atom in manifest["atoms"] if atom["atom_id"] in ATOM_IDS]
    require([atom["atom_id"] for atom in atoms] == list(ATOM_IDS), "atom census/order")
    intervals = [(Fraction(*atom["density_interval"][0]),
                  Fraction(*atom["density_interval"][1])) for atom in atoms]
    require(intervals[0][0] == Fraction(7, 48) and intervals[-1][1] == Fraction(13, 48),
            "selected envelope endpoints")
    for index, (lower, upper) in enumerate(intervals):
        require(lower < upper, "empty/reversed atom")
        if index:
            require(intervals[index - 1][1] == lower, "noncontiguous selected atoms")

    rows = []
    with localcontext() as ctx:
        ctx.prec = 50
        for length in SIZES:
            independently_mapped = []
            for atom, (lower, upper) in zip(atoms, intervals):
                midpoint = (lower + upper) / 2
                shifted = 2 * length * midpoint + Fraction(1, 2)
                rank = min(length, max(0, shifted.numerator // shifted.denominator))
                require(rank == atom["q_by_L"][str(length)], "midpoint sector mismatch")
                independently_mapped.append(rank)
            ranks = sorted(set(independently_mapped))
            require(ranks == EXPECTED_RANKS[length], "selected rank set")
            history_binding = manifest["histories"][str(length)]
            masses = {}
            for branch in ("target", "blind"):
                history, receipt = read_authenticated(
                    root, history_binding[branch + "_history_path"],
                    history_binding[branch + "_history_sha256"])
                inputs.append(receipt)
                late = [row for row in history["rows"] if row["event"] >= (length + 1) // 2]
                expected_events = list(range((length + 1) // 2, length + 1))
                require([row["event"] for row in late] == expected_events,
                        "late-event census/order: L%d %s" % (length, branch))
                total = Decimal(0)
                for event in late:
                    weights = event["sector_weights"]
                    # Seed histories retain the full carrier-number array;
                    # later streamed histories trim it at owner-once q <= L.
                    expected_weight_count = 2 * length + 1 if length <= 8 else length + 1
                    require(len(weights) == expected_weight_count, "sector weight census")
                    selected = [Decimal(weights[q]) for q in ranks]
                    require(all(weight.is_finite() and weight >= 0 for weight in selected),
                            "invalid probability")
                    total += sum(selected, Decimal(0))
                mass = total / Decimal(len(late))
                require(Decimal("0.5") < mass <= Decimal(1), "majority mass failed")
                masses[branch] = mass
            rows.append({
                "L": length,
                "selected_q": ranks,
                "late_events": expected_events,
                "target_mass": str(masses["target"]),
                "blind_mass": str(masses["blind"]),
                "absolute_difference": str(abs(masses["target"] - masses["blind"])),
                "both_strictly_above_half": True,
            })
    return {
        "schema": "UNT_INDEPENDENT_FINITE_MASS_REVIEW_V001",
        "status": "PASS_STORED_HISTORY_MIDPOINT_MAP_AND_MAJORITY_MASSES",
        "root": str(root),
        "decimal_precision": 50,
        "atom_ids": list(ATOM_IDS),
        "inputs": inputs,
        "rows": rows,
        "maximum_target_blind_difference": str(max(Decimal(row["absolute_difference"]) for row in rows)),
        "new_physics_run": False,
        "files_written": 0,
        "claim_ceiling": "STORED_FINITE_HISTORY_ARITHMETIC_ONLY__NO_NEW_EVOLUTION_VISIBILITY_ALL_L_OR_GRAVITY_PROOF",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="repository root holding the authenticated manifest/histories")
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    try:
        result = audit(root)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
        print(json.dumps({"schema": "UNT_INDEPENDENT_FINITE_MASS_REVIEW_V001",
                          "status": "FAIL", "error": str(error), "files_written": 0},
                         sort_keys=True, allow_nan=False))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
