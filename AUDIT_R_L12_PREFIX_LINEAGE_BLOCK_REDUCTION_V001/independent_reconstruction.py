#!/usr/bin/env python3
"""Independent hostile reconstruction of the prefix-lineage block theorem."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import struct
from collections import defaultdict
from pathlib import Path


TAG = b"R-PREFIX-LINEAGE-V001\0"
EXPECTED = (1_251_677_700, 417_225_900, 548_354_040, 8_773_664_640, 2_453_288_291)


def subsets(size: int, count: int):
    return list(reversed(list(itertools.combinations(range(size), count))))


def pascal(n: int, k: int, memo={(0, 0): 1}) -> int:
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    key = (n, k)
    if key not in memo:
        memo[key] = pascal(n - 1, k - 1) + pascal(n - 1, k)
    return memo[key]


def dimension(length: int, prefix: int) -> int:
    return sum(pascal(prefix, q) * pascal(2 * length, q) for q in range(prefix + 1))


def hostile_edges(length: int):
    answer = []
    for site in reversed(range(length)):
        answer.append((length + site, length + (site + 1) % length))
    for site in reversed(range(length)):
        answer.append((site, length + (site + 1) % length))
    for site in reversed(range(length)):
        answer.append((site, (site + 1) % length))
    return answer


def basis(length: int, prefix: int):
    for q in range(prefix + 1):
        for lineage in subsets(prefix, q):
            for carrier in subsets(2 * length, q):
                yield frozenset(lineage), frozenset(carrier)


def hostile_admission(event: int, item):
    lineage, carrier = item
    if event in carrier:
        return ((lineage, carrier, 1.0 + 0.0j),)
    root = math.sqrt(0.5)
    return (
        (lineage, carrier, root + 0.0j),
        (lineage | {event}, carrier | {event}, -1.0j * root),
    )


def hostile_transport(length: int, item):
    lineage, carrier = item
    for u, v in hostile_edges(length):
        if (u in carrier) != (v in carrier):
            yield lineage, carrier ^ {u, v}


def canonical_mask(lineage) -> int:
    return sum(1 << value for value in lineage)


def put(target, key, value):
    target[key] = target.get(key, 0.0j) + value


def unit_state(length: int, prefix: int):
    state = {}
    for index, key in enumerate(basis(length, prefix)):
        state[key] = complex((7 * index + 1) % 19 - 9, (13 * index + 4) % 23 - 11)
    scale = math.sqrt(sum(abs(value) ** 2 for value in state.values()))
    return {key: value / scale for key, value in state.items()}


def apply_admission(event: int, state):
    answer = {}
    for key, amplitude in state.items():
        for lineage, carrier, coefficient in hostile_admission(event, key):
            put(answer, (lineage, carrier), coefficient * amplitude)
    return answer


def apply_h(length: int, state):
    answer = {}
    for key, amplitude in state.items():
        for target in hostile_transport(length, key):
            put(answer, target, -amplitude)
    return answer


def polynomial(length: int, state):
    first = apply_h(length, state)
    second = apply_h(length, first)
    answer = dict(state)
    for key, value in first.items():
        put(answer, key, 0.125j * value)
    for key, value in second.items():
        put(answer, key, -0.03125 * value)
    return answer


def split(state, last: int):
    children = ({}, {})
    for key, value in state.items():
        children[int(last in key[0])][key] = value
    return children


def observables(length: int, state):
    norm = sum(abs(value) ** 2 for value in state.values())
    weights = [0.0] * (length + 1)
    occupations = [0.0] * (2 * length)
    for (_, carrier), value in state.items():
        probability = abs(value) ** 2
        weights[len(carrier)] += probability
        for site in carrier:
            occupations[site] += probability
    currents = []
    for u, v in hostile_edges(length):
        flow = 0.0
        for (lineage, carrier), amplitude in state.items():
            if u in carrier and v not in carrier:
                partner = (lineage, carrier ^ {u, v})
                flow += 2.0 * (amplitude.conjugate() * state.get(partner, 0.0j)).imag
        currents.append(flow)
    return norm, weights, occupations, currents


def difference(left, right):
    flat = [abs(left[0] - right[0])]
    for a, b in zip(left[1:], right[1:]):
        flat.extend(abs(x - y) for x, y in zip(a, b))
    return max(flat)


def add_observables(left, right):
    return (
        left[0] + right[0],
        [a + b for a, b in zip(left[1], right[1])],
        [a + b for a, b in zip(left[2], right[2])],
        [a + b for a, b in zip(left[3], right[3])],
    )


def run(target_path: Path, output: Path):
    target = json.loads(target_path.read_text())
    checks = []
    dims = {}
    for length in (4, 6, 8, 10, 12):
        row = []
        for prefix in range(length + 1):
            direct = dimension(length, prefix)
            closed = pascal(2 * length + prefix, prefix)
            checks.append((direct == closed, f"hostile Vandermonde L{length} n{prefix}"))
            row.append(direct)
        dims[str(length)] = row
        checks.append((row[-1] == pascal(3 * length, length), f"hostile full L{length}"))
        checks.append((3 * row[-2] == row[-1], f"hostile one-third L{length}"))

    row12 = dims["12"]
    census = (row12[-1], row12[-2], max(row12[n] + row12[n + 1] for n in range(11)),
              16 * max(row12[n] + row12[n + 1] for n in range(11)),
              sum(row12[:-1]) + sum(row12[1:]))
    checks.append((census == EXPECTED, "hostile exact L12 census"))
    checks.append((target["dimensions"] == dims, "target/hostile dimension table"))

    encodings = set()
    digests = set()
    for mask in range(4096):
        encoded = TAG + struct.pack(">HHQ", 12, 12, mask)
        encodings.add(encoded)
        digests.add(hashlib.sha256(encoded).digest())
    checks.append((len(encodings) == 4096, "hostile canonical lineage injection"))
    checks.append((len(digests) == 4096, "hostile observed digest census"))
    checks.append((target["lineage"]["authoritative_key"] == "FULL_MASK__DIGEST_IS_CUSTODY_ONLY",
                   "digest is not quotient authority"))

    counts = defaultdict(int)
    for length in (4, 6):
        for prefix in range(length):
            items = list(basis(length, prefix))
            checks.append((len(items) == dims[str(length)][prefix],
                           f"hostile exhaustive basis L{length} n{prefix}"))
            keys = {(canonical_mask(lineage), canonical_mask(carrier)) for lineage, carrier in items}
            checks.append((len(keys) == len(items), f"hostile embedding injective L{length} n{prefix}"))
            for item in items:
                lineage, carrier = item
                checks.append((all(bit < prefix for bit in lineage),
                               f"hostile future-lineage exclusion L{length} n{prefix}"))
                checks.append((len(lineage) == len(carrier),
                               f"hostile content L{length} n{prefix}"))
                admission = hostile_admission(prefix, item)
                checks.append((all(len(a) == len(b) for a, b, _ in admission),
                               f"hostile admission content L{length} n{prefix}"))
                checks.append((all(all(bit <= prefix for bit in a) for a, _, _ in admission),
                               f"hostile admission support L{length} n{prefix}"))
                checks.append((abs(sum(abs(c) ** 2 for _, _, c in admission) - 1.0) < 2e-15,
                               f"hostile admission norm L{length} n{prefix}"))
                for moved_lineage, moved_carrier in hostile_transport(length, item):
                    checks.append((moved_lineage == lineage and len(moved_carrier) == len(carrier),
                                   f"hostile transport block L{length} n{prefix}"))
                    counts[f"L{length}_transport_targets"] += 1
            counts[f"L{length}_prefix_states"] += len(items)

    state = unit_state(4, 3)
    admitted = apply_admission(3, state)
    full = polynomial(4, admitted)
    left, right = split(admitted, 3)
    routed_left, routed_right = polynomial(4, left), polynomial(4, right)
    rebuilt = dict(routed_left)
    for key, value in routed_right.items():
        put(rebuilt, key, value)
    all_keys = set(full) | set(rebuilt)
    amplitude_error = max(abs(full.get(key, 0.0j) - rebuilt.get(key, 0.0j)) for key in all_keys)
    observable_error = difference(observables(4, full),
                                  add_observables(observables(4, routed_left), observables(4, routed_right)))
    checks.append((amplitude_error <= 2e-14, "hostile terminal amplitude reconstruction"))
    checks.append((observable_error <= 2e-14, "hostile terminal observable reconstruction"))
    checks.append((abs(target["terminal_control"]["amplitude_linf"]) <= 2e-12,
                   "target terminal amplitude bound"))
    checks.append((abs(target["terminal_control"]["registered_observable_linf"]) <= 2e-12,
                   "target terminal observable bound"))

    failures = [label for passed, label in checks if not passed]
    result = {
        "schema": "AUDIT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001",
        "classification": ("PASS_HOSTILE_EXACT_PREFIX_LINEAGE_REPRESENTATION__L12_HISTORY_NOT_AUTHORIZED"
                           if not failures else "HOSTILE_REJECT_L12_PREFIX_LINEAGE_REDUCTION"),
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "dimensions": dims,
        "L12_census": {
            "full_terminal_dimension": census[0],
            "largest_materialized_dimension": census[1],
            "maximum_adjacent_live_entries": census[2],
            "maximum_adjacent_complex128_bytes": census[3],
            "one_resolution_routed_entries": census[4],
        },
        "canonical_lineages": len(encodings),
        "observed_distinct_digests": len(digests),
        "structural_counts": dict(sorted(counts.items())),
        "terminal_control": {
            "amplitude_linf": amplitude_error,
            "registered_observable_linf": observable_error,
        },
        "target_result_sha256": hashlib.sha256(target_path.read_bytes()).hexdigest(),
        "claim_boundary": "INDEPENDENT_REPRESENTATION_PREFLIGHT_ONLY__NO_L12_HISTORY_SPECTRUM_Z1_OR_GRAVITY",
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["classification"])
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    print(f"terminal amplitude={amplitude_error:.3e} observables={observable_error:.3e}")
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    run(arguments.target, arguments.output)
