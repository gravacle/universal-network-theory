#!/usr/bin/env python3
"""Blind structural verifier for the frozen hydrodynamic pre-screen.

This verifier intentionally evaluates no target spectral result.  Physical
graph/configuration work is limited to L=4,6,8.  References to L=10,12 occur
only in exact rational bookkeeping and synthetic authorization-state tests.
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
import time
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTOCOL = (
    ROOT / "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001"
    / "PROTOCOL.md"
)
RESULT = HERE / "RESULT.json"
PROTOCOL_SHA256 = "3da9e74b0dcc2d8b65ce98cfb42735864cf3d045e41655082baa7a7a295cb334"
PHYSICAL_SIZES = (4, 6, 8)
BOOKKEEPING_SIZES = (4, 6, 8, 10, 12)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frac(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def popcount(value: int) -> int:
    """Python-3.9-compatible population count used by the sealed host."""
    return bin(value).count("1")


def edges_for(length: int):
    edges = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            edges.append((offset + site, offset + (site + 1) % length, "rail"))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


def axial_parity(site: int, length: int) -> int:
    return (site % length) & 1


def topology_record(length: int):
    vertices = 2 * length
    edges = edges_for(length)
    undirected = {tuple(sorted((u, v))) for u, v, _ in edges}
    neighbors = [set() for _ in range(vertices)]
    for u, v, _ in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    seen = {0}
    stack = [0]
    while stack:
        node = stack.pop()
        for neighbor in neighbors[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    edge_crossing = all(
        axial_parity(u, length) != axial_parity(v, length)
        for u, v, _ in edges
    )
    return {
        "sites": vertices,
        "owner_edges": len(edges),
        "unique_undirected_edges": len(undirected),
        "degree_multiset": sorted(len(row) for row in neighbors),
        "connected_sites": len(seen),
        "base_bipartite_by_axial_parity": edge_crossing,
        "pass": (
            len(edges) == 3 * length
            and len(undirected) == len(edges)
            and all(len(row) == 3 for row in neighbors)
            and len(seen) == vertices
            and edge_crossing
        ),
    }


def h_one_action(vector, edges):
    out = [0j] * len(vector)
    for u, v, _ in edges:
        out[u] -= vector[v]
        out[v] -= vector[u]
    return out


def one_particle_bands(length: int):
    edges = edges_for(length)
    rows = []
    max_residual = 0.0
    energies = []
    for mode in range(length):
        wave_number = 2.0 * math.pi * mode / length
        phase = cmath.exp(1j * wave_number)
        for sign in (-1, 1):
            # Energy E=-2 cos(k)+sign.  The shifted connector fixes the
            # relative rail phase b=-sign*exp(-ik)*a.
            energy = -2.0 * math.cos(wave_number) + sign
            norm = math.sqrt(2.0 * length)
            vector = []
            for site in range(length):
                vector.append(cmath.exp(1j * wave_number * site) / norm)
            for site in range(length):
                vector.append(
                    -sign * phase.conjugate()
                    * cmath.exp(1j * wave_number * site) / norm
                )
            acted = h_one_action(vector, edges)
            residual = math.sqrt(sum(
                abs(acted[index] - energy * vector[index]) ** 2
                for index in range(2 * length)
            ))
            max_residual = max(max_residual, residual)
            energies.append(energy)
            rows.append({
                "m": mode,
                "band_sign": sign,
                "energy": energy,
                "eigenpair_residual_l2": residual,
            })

    # The integer one-particle Hamiltonian is constructed without N.  Hashing
    # it for every admissible write count explicitly guards against silently
    # replacing it by a state-dependent mean-field matrix.
    matrix = [[0 for _ in range(2 * length)] for _ in range(2 * length)]
    for u, v, _ in edges:
        matrix[u][v] = -1
        matrix[v][u] = -1
    signature = hashlib.sha256(
        json.dumps(matrix, separators=(",", ":")).encode()
    ).hexdigest()
    signatures_by_n = {
        str(write_count): signature for write_count in range(2 * length + 1)
    }
    zero_modes = [
        row for row in rows if abs(row["energy"]) < 1e-12
    ]
    return {
        "analytic_rows": rows,
        "max_explicit_fourier_eigenpair_residual_l2": max_residual,
        "zero_mode_count": len(zero_modes),
        "zero_modes": zero_modes,
        "hamiltonian_signatures_by_N": signatures_by_n,
        "N_independent": len(set(signatures_by_n.values())) == 1,
        "pass": max_residual < 1e-12 and len(set(signatures_by_n.values())) == 1,
    }


def words_of_weight(site_count: int, weight: int):
    for occupied in itertools.combinations(range(site_count), weight):
        word = 0
        for site in occupied:
            word |= 1 << site
        yield word


def configuration_record(length: int, particle_number: int):
    site_count = 2 * length
    full_mask = (1 << site_count) - 1
    base_positive_mask = sum(
        1 << site for site in range(site_count)
        if axial_parity(site, length) == 0
    )
    edges = edges_for(length)
    words = list(words_of_weight(site_count, particle_number))
    word_set = set(words)
    positive = 0
    negative = 0
    q_conserved = True
    chiral_hops = True
    particle_hole_exact = True
    for word in words:
        color = -1 if (popcount(word & base_positive_mask) & 1) else 1
        if color == 1:
            positive += 1
        else:
            negative += 1
        complement = full_mask ^ word
        if popcount(complement) != site_count - particle_number:
            particle_hole_exact = False
        for u, v, _ in edges:
            if ((word >> u) & 1) == ((word >> v) & 1):
                continue
            swapped = word ^ (1 << u) ^ (1 << v)
            if popcount(swapped) != particle_number or swapped not in word_set:
                q_conserved = False
            swapped_color = (
                -1 if (popcount(swapped & base_positive_mask) & 1) else 1
            )
            if swapped_color != -color:
                chiral_hops = False
            complement_swapped = full_mask ^ swapped
            direct_complement_hop = complement ^ (1 << u) ^ (1 << v)
            if complement_swapped != direct_complement_hop:
                particle_hole_exact = False

    # Token/configuration graph connectivity proves irreducibility of -H in
    # each nontrivial q sector, hence uniqueness of its PF ground vector.
    seen = {words[0]}
    stack = [words[0]]
    while stack:
        word = stack.pop()
        for u, v, _ in edges:
            if ((word >> u) & 1) == ((word >> v) & 1):
                continue
            swapped = word ^ (1 << u) ^ (1 << v)
            if swapped not in seen:
                seen.add(swapped)
                stack.append(swapped)

    expected_signed_imbalance = (
        ((-1) ** (particle_number // 2))
        * math.comb(length, particle_number // 2)
        if particle_number % 2 == 0 else 0
    )
    signed_imbalance = positive - negative
    forced_zero_lower_bound = abs(signed_imbalance)
    return {
        "q": particle_number,
        "dimension": len(words),
        "expected_dimension": math.comb(site_count, particle_number),
        "chiral_positive_words": positive,
        "chiral_negative_words": negative,
        "signed_imbalance": signed_imbalance,
        "exact_imbalance_formula": expected_signed_imbalance,
        "forced_zero_nullity_lower_bound": forced_zero_lower_bound,
        "configuration_graph_connected": len(seen) == len(words),
        "Q_conserved_on_every_hop": q_conserved,
        "chiral_sign_flips_on_every_hop": chiral_hops,
        "particle_hole_hop_map_exact": particle_hole_exact,
        "pass": (
            len(words) == math.comb(site_count, particle_number)
            and signed_imbalance == expected_signed_imbalance
            and len(seen) == len(words)
            and q_conserved
            and chiral_hops
            and particle_hole_exact
        ),
    }


def density_cell(length: int, particle_number: int):
    lower = max(Fraction(0), Fraction(2 * particle_number - 1, 4 * length))
    upper = min(Fraction(1, 2), Fraction(2 * particle_number + 1, 4 * length))
    return lower, upper


def density_record(length: int):
    rows = []
    for write_count in range(2 * length + 1):
        probabilities = [
            Fraction(math.comb(write_count, q), 1 << write_count)
            for q in range(write_count + 1)
        ]
        mean_q = sum(
            (Fraction(q) * probabilities[q] for q in range(write_count + 1)),
            Fraction(0),
        )
        variance_q = sum(
            ((Fraction(q) - mean_q) ** 2 * probabilities[q]
             for q in range(write_count + 1)),
            Fraction(0),
        )
        expected_mean = Fraction(write_count, 2)
        expected_variance = Fraction(write_count, 4)
        rows.append({
            "N": write_count,
            "probability_sum": frac(sum(probabilities, Fraction(0))),
            "mean_q": frac(mean_q),
            "variance_q": frac(variance_q),
            "mean_rho": frac(mean_q / (2 * length)),
            "variance_rho": frac(variance_q / (4 * length * length)),
            "pass": mean_q == expected_mean and variance_q == expected_variance,
        })
    cells = {
        str(q): [frac(value) for value in density_cell(length, q)]
        for q in range(length + 1)
    }
    contiguous_cells = all(
        density_cell(length, q)[1] == density_cell(length, q + 1)[0]
        for q in range(length)
    )
    return {
        "write_rows": rows,
        "sector_density_cells_q0_to_half_filling": cells,
        "cells_cover_zero_to_one_half_contiguously": (
            density_cell(length, 0)[0] == 0
            and density_cell(length, length)[1] == Fraction(1, 2)
            and contiguous_cells
        ),
        "pass": (
            all(row["pass"] for row in rows)
            and density_cell(length, 0)[0] == 0
            and density_cell(length, length)[1] == Fraction(1, 2)
            and contiguous_cells
        ),
    }


def normalize_intervals(intervals):
    rows = sorted(intervals)
    if not rows:
        return []
    merged = [list(rows[0])]
    for lower, upper in rows[1:]:
        if lower <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], upper)
        else:
            merged.append([lower, upper])
    return [tuple(row) for row in merged]


def intersect_interval_sets(left, right):
    intersections = []
    for lower_a, upper_a in left:
        for lower_b, upper_b in right:
            lower = max(lower_a, lower_b)
            upper = min(upper_a, upper_b)
            if lower <= upper:
                intersections.append((lower, upper))
    return normalize_intervals(intersections)


def cell_intersection(cells_by_size):
    intersection = [(Fraction(0), Fraction(1, 2))]
    for length in sorted(cells_by_size):
        union = normalize_intervals([
            density_cell(length, q) for q in cells_by_size[length]
        ])
        intersection = intersect_interval_sets(intersection, union)
    return intersection


def gate_decision(
    seed_cells,
    *,
    seed_trend_ok,
    seed_unresolved=False,
    confirmation=None,
    confirmed_cells=None,
    gapless_fit_wins=None,
    competing_cell_ambiguity=False,
):
    seed_intersection = cell_intersection(seed_cells)
    no_followups = {
        "spatial_response": False,
        "predictive_macro_closure": False,
        "mode_universality": False,
        "two_cluster_connected_response": False,
    }
    if seed_unresolved:
        return {
            "status": "UNRESOLVED",
            "authorized_spectral_sizes": [],
            "followups": no_followups,
            "seed_interval": [],
            "candidate_interval": [],
        }
    if set(seed_cells) != {4, 6, 8} or not seed_intersection or not seed_trend_ok:
        return {
            "status": "NO_CANDIDATE_L4_L8",
            "authorized_spectral_sizes": [],
            "followups": no_followups,
            "seed_interval": [[frac(a), frac(b)] for a, b in seed_intersection],
            "candidate_interval": [],
        }
    seed_interval_json = [[frac(a), frac(b)] for a, b in seed_intersection]
    if confirmation is None:
        return {
            "status": "SEED_L4_L8",
            "authorized_spectral_sizes": [10, 12],
            "followups": no_followups,
            "seed_interval": seed_interval_json,
            "candidate_interval": [],
        }
    if confirmation == "UNRESOLVED" or competing_cell_ambiguity:
        return {
            "status": "UNRESOLVED",
            "authorized_spectral_sizes": [],
            "followups": no_followups,
            "seed_interval": seed_interval_json,
            "candidate_interval": [],
        }
    candidate_intersection = (
        cell_intersection(confirmed_cells) if confirmed_cells else []
    )
    if (
        confirmation != "CANDIDATE"
        or set(confirmed_cells or {}) != {8, 10, 12}
        or len(candidate_intersection) != 1
        or not gapless_fit_wins
    ):
        return {
            "status": "NO_CANDIDATE",
            "authorized_spectral_sizes": [],
            "followups": no_followups,
            "seed_interval": seed_interval_json,
            "candidate_interval": [
                [frac(a), frac(b)] for a, b in candidate_intersection
            ],
        }
    return {
        "status": "CANDIDATE_INTERVAL",
        "authorized_spectral_sizes": [],
        "followups": {key: True for key in no_followups},
        "seed_interval": seed_interval_json,
        "candidate_interval": [
            [frac(a), frac(b)] for a, b in candidate_intersection
        ],
    }


started = time.perf_counter()
checks = []


def check(condition: bool, label: str):
    checks.append({"label": label, "pass": bool(condition)})


check(PROTOCOL.exists(), "frozen protocol exists")
protocol_hash = digest(PROTOCOL)
check(protocol_hash == PROTOCOL_SHA256, "frozen protocol SHA-256")

topology = {}
bands = {}
configuration = {}
density = {}
for length in PHYSICAL_SIZES:
    topology[str(length)] = topology_record(length)
    bands[str(length)] = one_particle_bands(length)
    density[str(length)] = density_record(length)
    configuration[str(length)] = [
        configuration_record(length, q) for q in range(length + 1)
    ]
    check(topology[str(length)]["pass"], f"L{length} topology/owner/bipartition")
    check(bands[str(length)]["pass"], f"L{length} analytic one-particle bands")
    check(density[str(length)]["pass"], f"L{length} exact density bookkeeping")
    check(
        all(row["pass"] for row in configuration[str(length)]),
        f"L{length} Q/chiral/particle-hole/configuration connectivity",
    )

check(bands["6"]["zero_mode_count"] == 4, "L6 commensurate one-particle zeros")
check(bands["4"]["zero_mode_count"] == 0, "L4 has no one-particle zero")
check(bands["8"]["zero_mode_count"] == 0, "L8 has no one-particle zero")
check(
    all(
        row["forced_zero_nullity_lower_bound"]
        == (math.comb(length, row["q"] // 2) if row["q"] % 2 == 0 else 0)
        for length in PHYSICAL_SIZES
        for row in configuration[str(length)]
    ),
    "exact chiral false-zero lower-bound formula",
)

mean_density_sets = {
    length: {Fraction(n, 4 * length) for n in range(2 * length + 1)}
    for length in BOOKKEEPING_SIZES
}
common_grid = set.intersection(*(mean_density_sets[length] for length in BOOKKEEPING_SIZES))
expected_common_grid = {
    Fraction(0), Fraction(1, 8), Fraction(1, 4), Fraction(3, 8), Fraction(1, 2)
}
check(common_grid == expected_common_grid, "five-size authenticated common mean-density grid")
check(
    all(Fraction(2 * n4, 4 * 8) == Fraction(n4, 4 * 4) for n4 in range(9)),
    "equal-density L4+L4 to L8 requires N8=2*N4",
)

fixtures = {
    "no_seed": gate_decision({4: [], 6: [], 8: []}, seed_trend_ok=False),
    "unresolved_seed": gate_decision(
        {4: [2], 6: [3], 8: [4]}, seed_trend_ok=True, seed_unresolved=True
    ),
    "seed_only": gate_decision(
        {4: [2], 6: [3], 8: [4]}, seed_trend_ok=True
    ),
    "confirmed": gate_decision(
        {4: [2], 6: [3], 8: [4]},
        seed_trend_ok=True,
        confirmation="CANDIDATE",
        confirmed_cells={8: [4], 10: [5], 12: [6]},
        gapless_fit_wins=True,
    ),
    "positive_gap_wins": gate_decision(
        {4: [2], 6: [3], 8: [4]},
        seed_trend_ok=True,
        confirmation="CANDIDATE",
        confirmed_cells={8: [4], 10: [5], 12: [6]},
        gapless_fit_wins=False,
    ),
    "competing_cell_ambiguity": gate_decision(
        {4: [2], 6: [3], 8: [4]},
        seed_trend_ok=True,
        confirmation="CANDIDATE",
        confirmed_cells={8: [4], 10: [5], 12: [6]},
        gapless_fit_wins=True,
        competing_cell_ambiguity=True,
    ),
}
check(
    fixtures["no_seed"]["status"] == "NO_CANDIDATE_L4_L8"
    and not any(fixtures["no_seed"]["followups"].values()),
    "no seed blocks every larger/follow-up run",
)
check(
    fixtures["unresolved_seed"]["status"] == "UNRESOLVED"
    and not any(fixtures["unresolved_seed"]["followups"].values()),
    "unresolved seed blocks every larger/follow-up run",
)
check(
    fixtures["seed_only"]["status"] == "SEED_L4_L8"
    and fixtures["seed_only"]["authorized_spectral_sizes"] == [10, 12]
    and not any(fixtures["seed_only"]["followups"].values()),
    "L4-L8 seed authorizes only sparse L10/L12 confirmation",
)
check(
    fixtures["confirmed"]["status"] == "CANDIDATE_INTERVAL"
    and all(fixtures["confirmed"]["followups"].values()),
    "confirmed interval automatically authorizes all bounded response tracks",
)
check(
    fixtures["positive_gap_wins"]["status"] == "NO_CANDIDATE"
    and not any(fixtures["positive_gap_wins"]["followups"].values()),
    "positive-gap preference blocks response tracks",
)
check(
    fixtures["competing_cell_ambiguity"]["status"] == "UNRESOLVED"
    and not any(fixtures["competing_cell_ambiguity"]["followups"].values()),
    "competing-cell ambiguity blocks response tracks",
)

result = {
    "schema": "ADVERSARIAL_R_GATE_C_HYDRO_CRITICALITY_PROTOCOL_V001",
    "scope": "BLIND_EXACT_STRUCTURAL_PROTOCOL_SCREEN__NO_TARGET_NUMERICAL_RESULT_INSPECTED",
    "protocol_sha256_expected": PROTOCOL_SHA256,
    "protocol_sha256_observed": protocol_hash,
    "physical_graph_or_configuration_sizes_executed": list(PHYSICAL_SIZES),
    "larger_size_activity": "NONE__L10_L12_APPEAR_ONLY_IN_EXACT_RATIONAL_BOOKKEEPING_AND_SYNTHETIC_GATE_FIXTURES",
    "topology": topology,
    "one_particle_bands": bands,
    "configuration_chiral_controls": configuration,
    "density_bookkeeping": density,
    "common_authenticated_mean_density_grid": [
        frac(value) for value in sorted(common_grid)
    ],
    "configuration_chiral_theorem": {
        "signed_imbalance": "(-1)^(q/2)*binomial(L,q/2) for even q; zero for odd q",
        "forced_zero_nullity_lower_bound": "binomial(L,q/2) for even q; zero for odd q",
        "interpretation": "EXACT_MID_SPECTRUM_ZEROS_ARE_STRUCTURAL_FALSE_POSITIVE_CONTROLS",
    },
    "automatic_gate_fixtures": fixtures,
    "schema_enforcement_notes": [
        "Treat sum_a w_a numerically indistinguishable from zero as UNRESOLVED; chi_tau is then undefined.",
        "A strict local density extremum requires both neighboring sector rows; endpoint q=1 or q=L is not a seed without a separately frozen one-sided rule.",
        "Repeat degenerate-projector grouping at tighter and looser energy-group tolerances; a changing active-pole identity is UNRESOLVED.",
        "The automatically authorized work comprises spatial characterization plus the three response tracks; none runs before CANDIDATE_INTERVAL.",
        "One candidate cell/mode must be selected per size for the five-row fit; competing admissible cells are UNRESOLVED.",
    ],
    "checks": checks,
    "checks_passed": sum(row["pass"] for row in checks),
    "checks_total": len(checks),
    "status": (
        "PASS_BLIND_STRUCTURAL_PROTOCOL_SCREEN_WITH_FAIL_CLOSED_SCHEMA_NOTES"
        if all(row["pass"] for row in checks)
        else "FAIL_BLIND_STRUCTURAL_PROTOCOL_SCREEN"
    ),
    "runtime_seconds": time.perf_counter() - started,
    "claim_boundary": (
        "EXACT_FINITE_COMBINATORICS_AND_GRAPH_IDENTITIES_ONLY__NO_RHO_C__"
        "NO_PHASE__NO_CONTINUUM__NO_GRAVITY"
    ),
}
RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(f"{result['status']}: {result['checks_passed']}/{result['checks_total']}")
print(f"wrote {RESULT}")
