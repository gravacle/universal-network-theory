#!/usr/bin/env python3
"""Pre-output verifier for the exact owner-once prefix-lineage block."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import struct
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DOMAIN = b"R-PREFIX-LINEAGE-V001\0"
LENGTHS = (4, 6, 8, 10, 12)
CONTROL_LENGTHS = (4, 6)
EXPECTED_L12 = {
    "full_terminal_dimension": 1_251_677_700,
    "largest_materialized_dimension": 417_225_900,
    "maximum_adjacent_live_entries": 548_354_040,
    "maximum_adjacent_complex128_bytes": 8_773_664_640,
    "one_resolution_routed_entries": 2_453_288_291,
}


def popcount(word: int) -> int:
    return bin(word).count("1")


def colex_rank(word: int) -> int:
    rank = 0
    index = 1
    bit = 0
    value = word
    while value:
        if value & 1:
            rank += math.comb(bit, index)
            index += 1
        value >>= 1
        bit += 1
    return rank


def colex_unrank(width: int, weight: int, rank: int) -> int:
    if not 0 <= rank < math.comb(width, weight):
        raise ValueError("colex rank outside block")
    word = 0
    remainder = rank
    ceiling = width - 1
    for index in range(weight, 0, -1):
        chosen = ceiling
        while math.comb(chosen, index) > remainder:
            chosen -= 1
        word |= 1 << chosen
        remainder -= math.comb(chosen, index)
        ceiling = chosen - 1
    if remainder:
        raise AssertionError("colex inverse remainder")
    return word


def colex_words(width: int, weight: int):
    for rank in range(math.comb(width, weight)):
        yield colex_unrank(width, weight, rank)


def edges(length: int) -> list[tuple[int, int]]:
    answer = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            answer.append((offset + site, offset + (site + 1) % length))
    answer.extend((site, length + (site + 1) % length) for site in range(length))
    return answer


def prefix_dimension(length: int, prefix: int) -> int:
    direct = sum(math.comb(prefix, q) * math.comb(2 * length, q)
                 for q in range(prefix + 1))
    vandermonde = math.comb(2 * length + prefix, prefix)
    if direct != vandermonde:
        raise AssertionError("prefix Vandermonde identity")
    return direct


def lineage_encoding(length: int, prefix: int, full_mask: int) -> bytes:
    if full_mask >> prefix:
        raise ValueError("future lineage bit is not zero")
    return DOMAIN + struct.pack(">HHQ", length, prefix, full_mask)


def lineage_digest(length: int, prefix: int, full_mask: int) -> str:
    return hashlib.sha256(lineage_encoding(length, prefix, full_mask)).hexdigest()


def prefix_basis(length: int, prefix: int):
    for q in range(prefix + 1):
        for lineage in colex_words(prefix, q):
            for carrier in colex_words(2 * length, q):
                yield lineage, carrier


def admit_basis(prefix: int, lineage: int, carrier: int):
    if (carrier >> prefix) & 1:
        return ((lineage, carrier, 1.0 + 0.0j),)
    c = math.cos(math.pi / 4.0)
    s = math.sin(math.pi / 4.0)
    return (
        (lineage, carrier, c + 0.0j),
        (lineage | (1 << prefix), carrier | (1 << prefix), -1.0j * s),
    )


def transport_targets(length: int, lineage: int, carrier: int):
    for u, v in edges(length):
        if ((carrier >> u) & 1) != ((carrier >> v) & 1):
            yield lineage, carrier ^ (1 << u) ^ (1 << v)


def add(target: dict[tuple[int, int], complex], key: tuple[int, int], value: complex):
    target[key] = target.get(key, 0.0j) + value


def normalize(state: dict[tuple[int, int], complex]):
    norm = math.sqrt(sum(abs(value) ** 2 for value in state.values()))
    return {key: value / norm for key, value in state.items()}


def admit_state(prefix: int, state: dict[tuple[int, int], complex]):
    out: dict[tuple[int, int], complex] = {}
    for (lineage, carrier), amplitude in state.items():
        for new_lineage, new_carrier, coefficient in admit_basis(prefix, lineage, carrier):
            add(out, (new_lineage, new_carrier), coefficient * amplitude)
    return out


def h_state(length: int, state: dict[tuple[int, int], complex]):
    out: dict[tuple[int, int], complex] = {}
    for (lineage, carrier), amplitude in state.items():
        for key in transport_targets(length, lineage, carrier):
            add(out, key, -amplitude)
    return out


def transport_polynomial(length: int, state: dict[tuple[int, int], complex]):
    first = h_state(length, state)
    second = h_state(length, first)
    out = dict(state)
    for key, value in first.items():
        add(out, key, 0.125j * value)
    for key, value in second.items():
        add(out, key, -0.03125 * value)
    return out


def split_last(state: dict[tuple[int, int], complex], last: int):
    children = ({}, {})
    for key, value in state.items():
        children[(key[0] >> last) & 1][key] = value
    return children


def registered(length: int, state: dict[tuple[int, int], complex]):
    norm = sum(abs(value) ** 2 for value in state.values())
    sectors = [0.0] * (length + 1)
    occupation = [0.0] * (2 * length)
    for (_, carrier), value in state.items():
        probability = abs(value) ** 2
        sectors[popcount(carrier)] += probability
        for site in range(2 * length):
            if (carrier >> site) & 1:
                occupation[site] += probability
    currents = []
    for u, v in edges(length):
        value = 0.0
        for (lineage, carrier), amplitude in state.items():
            if ((carrier >> u) & 1) and not ((carrier >> v) & 1):
                partner = (lineage, carrier ^ (1 << u) ^ (1 << v))
                value += 2.0 * (amplitude.conjugate() * state.get(partner, 0.0j)).imag
        currents.append(value)
    return {"norm": norm, "sectors": sectors, "occupation": occupation, "currents": currents}


def max_registered_difference(left, right) -> float:
    values = [abs(left["norm"] - right["norm"])]
    for key in ("sectors", "occupation", "currents"):
        values.extend(abs(a - b) for a, b in zip(left[key], right[key]))
    return max(values)


def add_registered(left, right):
    return {
        "norm": left["norm"] + right["norm"],
        "sectors": [a + b for a, b in zip(left["sectors"], right["sectors"])],
        "occupation": [a + b for a, b in zip(left["occupation"], right["occupation"])],
        "currents": [a + b for a, b in zip(left["currents"], right["currents"])],
    }


def deterministic_state(length: int, prefix: int):
    state = {}
    for index, key in enumerate(prefix_basis(length, prefix)):
        real = (index * 17 + 3) % 29 - 14
        imag = (index * 11 + 5) % 31 - 15
        state[key] = complex(real, imag)
    return normalize(state)


def main(output: Path) -> None:
    checks: list[tuple[bool, str]] = []
    dimensions = {}
    for length in LENGTHS:
        row = [prefix_dimension(length, prefix) for prefix in range(length + 1)]
        dimensions[str(length)] = row
        checks.append((row[-1] == math.comb(3 * length, length), f"L{length} full dimension"))
        checks.append((row[-2] * 3 == row[-1], f"L{length} preterminal one-third identity"))

    l12 = dimensions["12"]
    routed = sum(l12[:-1]) + sum(l12[1:])
    adjacent = max(l12[index] + l12[index + 1] for index in range(11))
    census = {
        "full_terminal_dimension": l12[-1],
        "largest_materialized_dimension": l12[-2],
        "maximum_adjacent_live_entries": adjacent,
        "maximum_adjacent_complex128_bytes": adjacent * 16,
        "one_resolution_routed_entries": routed,
    }
    checks.append((census == EXPECTED_L12, "L12 frozen resource census"))

    encodings = set()
    digests = set()
    for mask in range(1 << 12):
        encoding = DOMAIN + struct.pack(">HHQ", 12, 12, mask)
        encodings.add(encoding)
        digests.add(hashlib.sha256(encoding).digest())
    checks.append((len(encodings) == 4096, "L12 canonical lineage encodings injective"))
    checks.append((len(digests) == 4096, "L12 observed SHA256 custody digests distinct"))

    rank_checks = 0
    for width in range(1, 17):
        for weight in range(width + 1):
            for rank in range(math.comb(width, weight)):
                word = colex_unrank(width, weight, rank)
                if popcount(word) != weight or word >= (1 << width) or colex_rank(word) != rank:
                    raise AssertionError("colex round trip")
                rank_checks += 1
    for weight in range(13):
        count = math.comb(24, weight)
        probes = sorted({0, count // 7, count // 3, count // 2, max(0, count - 2), count - 1})
        for rank in probes:
            word = colex_unrank(24, weight, rank)
            checks.append((colex_rank(word) == rank, f"width24 q{weight} combinadic probe {rank}"))

    structural_counts = defaultdict(int)
    for length in CONTROL_LENGTHS:
        edge_list = edges(length)
        for prefix in range(length):
            observed = 0
            for lineage, carrier in prefix_basis(length, prefix):
                observed += 1
                checks.append((lineage >> prefix == 0, f"L{length} prefix{prefix} future bits zero #{observed}"))
                checks.append((popcount(lineage) == popcount(carrier), f"L{length} prefix{prefix} content #{observed}"))
                encoded = lineage_encoding(length, prefix, lineage)
                checks.append((encoded.endswith(struct.pack(">Q", lineage)), f"L{length} prefix{prefix} lineage roundtrip #{observed}"))
                outputs = admit_basis(prefix, lineage, carrier)
                checks.append((all(new_lineage >> (prefix + 1) == 0 for new_lineage, _, _ in outputs),
                               f"L{length} prefix{prefix} admission support #{observed}"))
                checks.append((all(popcount(new_lineage) == popcount(new_carrier)
                                   for new_lineage, new_carrier, _ in outputs),
                               f"L{length} prefix{prefix} admission content #{observed}"))
                expected_norm = sum(abs(coefficient) ** 2 for _, _, coefficient in outputs)
                checks.append((abs(expected_norm - 1.0) <= 2e-15,
                               f"L{length} prefix{prefix} admission isometry #{observed}"))
                for new_lineage, new_carrier in transport_targets(length, lineage, carrier):
                    checks.append((new_lineage == lineage and popcount(new_carrier) == popcount(carrier),
                                   f"L{length} prefix{prefix} transport block #{observed}"))
                    structural_counts[f"L{length}_transport_targets"] += 1
            checks.append((observed == prefix_dimension(length, prefix),
                           f"L{length} prefix{prefix} exhaustive basis census"))
            structural_counts[f"L{length}_prefix_states"] += observed
            structural_counts[f"L{length}_edges"] = len(edge_list)

    control = deterministic_state(4, 3)
    admitted = admit_state(3, control)
    transported = transport_polynomial(4, admitted)
    child0, child1 = split_last(admitted, 3)
    routed0 = transport_polynomial(4, child0)
    routed1 = transport_polynomial(4, child1)
    reconstructed = dict(routed0)
    for key, value in routed1.items():
        add(reconstructed, key, value)
    all_keys = set(transported) | set(reconstructed)
    amplitude_difference = max(abs(transported.get(key, 0.0j) - reconstructed.get(key, 0.0j))
                               for key in all_keys)
    observable_difference = max_registered_difference(
        registered(4, transported),
        add_registered(registered(4, routed0), registered(4, routed1)),
    )
    checks.append((amplitude_difference <= 2e-14, "terminal direct-sum amplitude reconstruction"))
    checks.append((observable_difference <= 2e-14, "terminal registered-observable additivity"))

    free = shutil.disk_usage(ROOT).free
    resource = {
        "observed_free_scratch_bytes": free,
        "new_free_scratch_gate_bytes": 20 * 2**30,
        "scratch_gate_pass": free >= 20 * 2**30,
        "future_rss_limit_bytes": 16 * 2**30,
        "future_wall_limit_seconds_per_method": 6 * 3600,
        "terminal_amplitude_window_bytes": 512 * 2**20,
        "target_krylov_limit_bytes": 1_000_000_000,
        "hostile_krylov_limit_bytes": 1_400_000_000,
        "carrier_exchange_cache_limit_bytes": 2 * 2**30,
        "sealed_L10_target_seconds": 2045.204301958,
        "sealed_L10_hostile_seconds": 1420.728120167,
        "projected_L12_target_seconds": 2045.204301958 * routed / (20 * 30_045_015),
        "projected_L12_hostile_seconds": 1420.728120167 * routed / (20 * 30_045_015),
        "projection_status": "ADOPTED_ROUTED_ENTRY_RATIO_ONLY__L10_REDUCED_BENCHMARK_REQUIRED",
    }
    checks.append((resource["scratch_gate_pass"], "new reduced-representation scratch gate"))
    checks.append((resource["projected_L12_target_seconds"] < resource["future_wall_limit_seconds_per_method"],
                   "planning target projection below wall guard"))
    checks.append((resource["projected_L12_hostile_seconds"] < resource["future_wall_limit_seconds_per_method"],
                   "planning hostile projection below wall guard"))

    failures = [label for passed, label in checks if not passed]
    result = {
        "schema": "R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_PREFLIGHT_V001",
        "classification": ("PASS_EXACT_PREFIX_LINEAGE_REPRESENTATION__L12_HISTORY_NOT_AUTHORIZED"
                           if not failures else "L12_PREFIX_LINEAGE_REDUCTION_REJECTED"),
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "dimensions": dimensions,
        "L12_census": census,
        "lineage": {
            "authoritative_key": "FULL_MASK__DIGEST_IS_CUSTODY_ONLY",
            "canonical_encodings": len(encodings),
            "observed_distinct_sha256_digests": len(digests),
            "digest_domain_hex": DOMAIN.hex(),
        },
        "combinadic_roundtrips_exhaustive_width_le_16": rank_checks,
        "structural_counts": dict(sorted(structural_counts.items())),
        "terminal_control": {
            "amplitude_linf": amplitude_difference,
            "registered_observable_linf": observable_difference,
        },
        "resource": resource,
        "claim_boundary": "REPRESENTATION_PREFLIGHT_ONLY__NO_L12_HISTORY_SPECTRUM_Z1_OR_GRAVITY",
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["classification"])
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    print(f"L12 materialized={census['largest_materialized_dimension']} adjacent_bytes={census['maximum_adjacent_complex128_bytes']}")
    print(f"terminal amplitude={amplitude_difference:.3e} observables={observable_difference:.3e}")
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    main(arguments.output)
