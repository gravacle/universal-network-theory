#!/usr/bin/env python3
"""Hostile verifier for the finite marked-source L6--L12 response packet."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from collections import defaultdict, deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_GATE_AP_MARKED_SOURCE_ENGINE_V001"
DIRECT = ROOT / "DEVELOPMENT_R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001"
PRIOR_AUDIT = ROOT / "AUDIT_R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001"
PROTOCOL_AUDIT = ROOT / "AUDIT_R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_PROTOCOL_V001"
MPS = HERE / "INDEPENDENT_MPS_OBSERVATION.json"
MPS_SCRIPT = HERE / "independent_mps_response.py"

PINS = {
    TARGET / "README.md": "be30868dd4a750a72e95e6c1071a4f8318fbb228c7f5c4e006a5f76a01f78ef7",
    TARGET / "THEOREM.md": "e9c734cad98d6c5eaefc3ca4c2d43b591135e80e3bd509059fb321af9286d5da",
    TARGET / "RUN_OBSERVATION.md": "7ff7daccad36858443e32842bac741f7d29f021f76582cefa57003944655ecda",
    TARGET / "compute_marked_response.py": "329cdad62c9da6ce78578832022a51b600673d737410bb7da3c716e682efdf3e",
    TARGET / "compile_response.py": "6e93afb1579b594cc9ee8ba9fa1e8fd0c5c6d8cf25f9ba92a014e6e657cedf9d",
    TARGET / "RESULT_L6.json": "2a0d2c957b39b960f8d87b55914efd4a547510e3f2cfc01a2a135a1efb2a967b",
    TARGET / "RESULT_L8.json": "288b007e4a519b1b26e062894c7c42685bf200d924b053c196cefda6014cbcdf",
    TARGET / "RESULT_L10.json": "cdf5dae0b6762ca60e8deefb07ac9f05abf06c7d693cd79415db03e154d6f116",
    TARGET / "RESULT_L12.json": "c7fd23bd73c96df1ca234952cba5d5c3eef5652b1de6f7ea3a0e262ef99c6b8f",
    TARGET / "SCREEN_L14.json": "384c83d26a1a31ac655771d94ee60facfecbb2ec50fd1a9fb08d6a9d6da392b7",
    TARGET / "RESULT.json": "eca3197740059226fa9665fd92b7556a653e698867af3ce6116ba17c3453b538",
    DIRECT / "RESULT_L6.json": "8ae5a0dbaf27b7a1b1bcd0e023b58498920b2cacd0664dc1093df6ac060e900a",
    DIRECT / "RESULT_L8.json": "b73ba9e1c660a5285a075fd8c040c6b04621e4badc0dbecf42483d5c0a1c72fb",
    PRIOR_AUDIT / "INDEPENDENT_RESULT.json": "43d0fc947022b1a316b838c94d1fdc8f659b68b44a8fcb052d1c79c07bce0238",
    PRIOR_AUDIT / "RESULT.json": "45b88fe34d459b81246ed289040a8b9824e45f75caa47b9c0836c2ff7772060a",
    PROTOCOL_AUDIT / "RESULT.json": "5edd62c053e28fa5b17475df533a4e732c29533792ea9da96e5e664b96f003b9",
    MPS_SCRIPT: "df9df1d7948e7d62fac5e815c4452540eae856ffb7a9b665c9bc6fc6979da181",
    MPS: "69b5ec0e6b37b9604a8cbf5a580f4d2351231ad2585b6fda26028879f37ed1aa",
}
BASELINE_PINS = {
    6: "e601f1a206eeb90eb3861587133bfc30ca9974e521a06031b8ee4ca5eff86f14",
    8: "7e4d763138c3090552b7f7a40098c761607653bacb81dfc29bbab7ae4b4f6a63",
    10: "06256f48fb39df0b5121ea01b38893ffeb84ba1bc7f842d22935ccd5279cdcbf",
    12: "154c9195b8ea516e4e637c1f4d66422ab82603163119f9b4451e7c2eb7ff5184",
    14: "e8134d5311b9bdfd62ce7df5988da803b110516606ce905a1bc49bd65cdb5fbe",
}
ROW_NOT_CLAIMED = (
    "LOCALITY_OR_SCALING_LAW__UNIFORM_OR_ASYMPTOTIC_PROFILE__"
    "PHYSICAL_BOUNDARY_REFLECTION__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY"
)
COMPILED_NOT_CLAIMED = (
    "COMPLETE_L6_TO_L14_NUMERICAL_LADDER__L14_RESPONSE__LOCALITY_OR_SCALING_THEOREM__"
    "PHYSICAL_BOUNDARY_REFLECTION__UNIFORM_OR_ASYMPTOTIC_PROFILE__GRID__CONTINUUM__"
    "WARD__PHASE__GRAVITON__GRAVITY"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edges_for(length: int):
    return [
        *((layer * length + site, layer * length + (site + 1) % length, "internal")
          for layer in range(2) for site in range(length)),
        *((site, length + (site + 1) % length, "connector") for site in range(length)),
    ]


def compose(left, right):
    return tuple(left[right[index]] for index in range(len(left)))


def generated_content_group(length: int):
    """Generate the parity-preserving prism group from two graph maps."""
    sites = 2 * length
    rotation = []
    reflection = []
    for layer in range(2):
        for site in range(length):
            if layer == 0:
                rotation.append(length + (site + 2) % length)
                reflection.append((-site) % length)
            else:
                rotation.append(site)
                reflection.append(length + (2 - site) % length)
    identity = tuple(range(sites))
    generators = (tuple(rotation), tuple(reflection))
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            for candidate in (compose(generator, current), compose(current, generator)):
                if candidate not in group:
                    group.add(candidate)
                    frontier.append(candidate)
    return sorted(group), generators


def cycle_count(permutation):
    seen = set()
    count = 0
    for start in range(len(permutation)):
        if start in seen:
            continue
        count += 1
        cursor = start
        while cursor not in seen:
            seen.add(cursor)
            cursor = permutation[cursor]
    return count


def move_word(word, permutation):
    result = 0
    for old, new in enumerate(permutation):
        if (word >> old) & 1:
            result |= 1 << new
    return result


def signed_edge_orbits(edges, stabilizer):
    lookup = {frozenset((u, v)): (index, u, v) for index, (u, v, _) in enumerate(edges)}
    reconstruction = [None] * len(edges)
    representatives = []
    for edge_index, (u, v, _) in enumerate(edges):
        if reconstruction[edge_index] is not None:
            continue
        representative = len(representatives)
        representatives.append(edge_index)
        images = {}
        for permutation in stabilizer:
            moved = (permutation[u], permutation[v])
            target, stored_u, stored_v = lookup[frozenset(moved)]
            sign = 1 if moved == (stored_u, stored_v) else -1
            if target in images and images[target] != sign:
                raise AssertionError("signed current edge orbit is contradictory")
            images[target] = sign
        for target, sign in images.items():
            reconstruction[target] = (representative, sign)
    if any(value is None for value in reconstruction):
        raise AssertionError("signed current edge ownership is incomplete")
    return representatives, reconstruction


def graph_distances(site_count, edges):
    neighbors = [set() for _ in range(site_count)]
    for u, v, _ in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    distances = [None] * site_count
    distances[0] = 0
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in neighbors[u]:
            if distances[v] is None:
                distances[v] = distances[u] + 1
                queue.append(v)
    return neighbors, distances


def independent_l6_quotient_check(stabilizer, edges):
    """Compare direct normalized-orbit projection with the representative rule."""
    full_dimension = 1 << 12
    orbit_id = [-1] * full_dimension
    members = []
    representatives = []
    for word in range(full_dimension):
        if orbit_id[word] >= 0:
            continue
        orbit = sorted({move_word(word, permutation) for permutation in stabilizer})
        index = len(members)
        representatives.append(orbit[0])
        members.append(orbit)
        for image in orbit:
            orbit_id[image] = index
    direct = defaultdict(float)
    representative_rule = defaultdict(float)
    for source, orbit in enumerate(members):
        source_size = len(orbit)
        for word in orbit:
            for u, v, _ in edges:
                if ((word >> u) & 1) == ((word >> v) & 1):
                    continue
                destination = orbit_id[word ^ (1 << u) ^ (1 << v)]
                direct[(source, destination)] -= 1.0 / math.sqrt(
                    source_size * len(members[destination])
                )
        word = representatives[source]
        for u, v, _ in edges:
            if ((word >> u) & 1) == ((word >> v) & 1):
                continue
            destination = orbit_id[word ^ (1 << u) ^ (1 << v)]
            representative_rule[(source, destination)] -= math.sqrt(
                source_size / len(members[destination])
            )
    keys = set(direct) | set(representative_rule)
    formula_linf = max(abs(direct[key] - representative_rule[key]) for key in keys)
    hermitian_linf = max(abs(direct[key] - direct[(key[1], key[0])]) for key in keys)
    histogram = defaultdict(int)
    for orbit in members:
        histogram[len(orbit)] += 1
    return {
        "orbit_dimension": len(members),
        "orbit_size_histogram": {str(size): count for size, count in sorted(histogram.items())},
        "projected_action_formula_linf": formula_linf,
        "projected_action_hermitian_linf": hermitian_linf,
        "projected_action_entries": len(keys),
    }


checks = []


def check(condition, label):
    checks.append((bool(condition), label))


check(all(digest(path) == expected for path, expected in PINS.items()), "all target and audit custody pins")
for length, expected in BASELINE_PINS.items():
    path = ROOT / f"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L{length}_ACCUMULATION_V001" / "RESULT.json"
    check(digest(path) == expected, f"L{length} sealed baseline pin")

protocol_audit = json.loads((PROTOCOL_AUDIT / "RESULT.json").read_text())
prior_summary = json.loads((PRIOR_AUDIT / "RESULT.json").read_text())
prior_independent = json.loads((PRIOR_AUDIT / "INDEPENDENT_RESULT.json").read_text())
check(protocol_audit["independent_checks"] == "35/35", "source-parent protocol hostile audit 35/35")
check(protocol_audit["Gate_A_P"] == "OPEN", "source-parent protocol leaves Gate A-P open")
check(prior_summary["independent_checks"] == "30/30", "direct L6/L8 hostile reconstruction 30/30")
check(prior_summary["Gate_A_P"] == "OPEN", "direct L6/L8 audit leaves Gate A-P open")

records = {
    length: json.loads((TARGET / f"RESULT_L{length}.json").read_text())
    for length in (6, 8, 10, 12)
}
compiled = json.loads((TARGET / "RESULT.json").read_text())
screen = json.loads((TARGET / "SCREEN_L14.json").read_text())
prior_rows = {row["L"]: row for row in prior_independent["rows"]}

expected_orbits = {6: 2176, 8: 33280, 10: 526336, 12: 8396800, 14: 134250496}
expected_edge_orbits = {6: 10, 8: 13, 10: 16, 12: 19, 14: 22}
structural_rows = {}
recompiled_rows = []
for length in (6, 8, 10, 12, 14):
    edges = edges_for(length)
    edge_set = {frozenset((u, v)) for u, v, _ in edges}
    group, generators = generated_content_group(length)
    stabilizer = [permutation for permutation in group if permutation[0] == 0]
    identity = tuple(range(2 * length))
    reflection = next(permutation for permutation in stabilizer if permutation != identity)
    representatives, reconstruction = signed_edge_orbits(edges, stabilizer)
    cycles = [cycle_count(permutation) for permutation in stabilizer]
    orbit_dimension = sum(1 << value for value in cycles) // len(stabilizer)
    fixed_count = sum(1 for site in range(2 * length) if reflection[site] == site)
    check(len(edges) == 3 * length and len(edge_set) == 3 * length, f"L{length} owner-once physical edge census")
    check(len(group) == 2 * length, f"L{length} generated complete content group order")
    check(len(stabilizer) == 2 and compose(reflection, reflection) == identity, f"L{length} exact order-two source stabilizer")
    check(all({frozenset((p[u], p[v])) for u, v, _ in edges} == edge_set for p in group), f"L{length} generated group preserves complete parent support")
    check(all(p[site] % 2 == site % 2 for p in group for site in range(2 * length)), f"L{length} generated group preserves baseline content parity")
    check(fixed_count == 4 and sorted(cycles) == [length + 2, 2 * length], f"L{length} stabilizer fixed-site and cycle census")
    check(orbit_dimension == expected_orbits[length], f"L{length} independent Burnside orbit dimension")
    check(len(representatives) == expected_edge_orbits[length], f"L{length} signed edge orbit census")
    check(len(reconstruction) == 3 * length and all(item is not None for item in reconstruction), f"L{length} signed owner reconstruction complete")
    structural_rows[length] = {
        "full_dimension": 1 << (2 * length),
        "content_group_order": len(group),
        "source_stabilizer_order": len(stabilizer),
        "source_reflection_fixed_sites": fixed_count,
        "source_reflection_cycles": cycle_count(reflection),
        "orbit_dimension": orbit_dimension,
        "signed_edge_orbits": len(representatives),
    }

quotient_control = independent_l6_quotient_check(
    [p for p in generated_content_group(6)[0] if p[0] == 0], edges_for(6)
)
check(quotient_control["orbit_dimension"] == expected_orbits[6], "independent L6 normalized-orbit basis census")
check(quotient_control["orbit_size_histogram"] == {"1": 256, "2": 1920}, "independent L6 orbit histogram")
check(quotient_control["projected_action_formula_linf"] < 1e-14, "independent quotient raw-hop to normalized-writer coefficient")
check(quotient_control["projected_action_hermitian_linf"] < 1e-14, "independent quotient action Hermiticity")

for length, target in records.items():
    edges = edges_for(length)
    site_count = 2 * length
    neighbors, distances = graph_distances(site_count, edges)
    site_records = target["site_records"]
    edge_records = target["edge_records"]
    q0_before = [row["baseline_q_before"] for row in site_records]
    q1_before = [row["perturbed_q_before"] for row in site_records]
    q0 = [row["baseline_q_after"] for row in site_records]
    q1 = [row["perturbed_q_after"] for row in site_records]
    dq = [row["delta_q_after"] for row in site_records]
    j0 = [row["baseline_J"] for row in edge_records]
    j1 = [row["perturbed_J"] for row in edge_records]
    dj = [row["delta_J"] for row in edge_records]
    incidence = [[0.0] * len(edges) for _ in range(site_count)]
    for edge_index, (u, v, _) in enumerate(edges):
        incidence[u][edge_index] = 1.0
        incidence[v][edge_index] = -1.0
    residual0 = [
        q0[site] - q0_before[site]
        + sum(incidence[site][edge] * j0[edge] for edge in range(len(edges)))
        for site in range(site_count)
    ]
    residual1 = [
        q1[site] - q1_before[site]
        + sum(incidence[site][edge] * j1[edge] for edge in range(len(edges)))
        for site in range(site_count)
    ]
    differential = [
        dq[site] + sum(incidence[site][edge] * dj[edge] for edge in range(len(edges)))
        - (0.5 if site == 0 else 0.0)
        for site in range(site_count)
    ]
    controls = target["numerical_controls"]
    basis = target["finite_marked_source_basis"]
    fixed_words = 1 << (length + 2)
    histogram = {"1": fixed_words, "2": ((1 << (2 * length)) - fixed_words) // 2}

    check(target["checks_passed"] == target["checks_total"] == (35 if length <= 8 else 29), f"L{length} target checks pass")
    check(not target["failures"], f"L{length} target failures empty")
    check(len(site_records) == site_count and len(edge_records) == 3 * length, f"L{length} complete q/J vector census")
    check([(row["u"], row["v"], row["kind"]) for row in edge_records] == edges, f"L{length} physical edge order and ownership")
    check(all(len(value) == 3 for value in neighbors) and all(value is not None for value in distances), f"L{length} complete parent connected degree three")
    check(all(row["r"] == distances[row["site"]] for row in site_records), f"L{length} site finite graph distances")
    check(all(row["r"] == min(distances[row["u"]], distances[row["v"]]) for row in edge_records), f"L{length} edge finite graph distances")
    check(max(abs(q1[index] - q0[index] - dq[index]) for index in range(site_count)) == 0.0, f"L{length} complete delta q identity")
    check(max(abs(j1[index] - j0[index] - dj[index]) for index in range(3 * length)) == 0.0, f"L{length} complete delta J identity")
    check(q0_before == [0.0 if site % 2 == 0 else 0.5 for site in range(site_count)], f"L{length} baseline initial record")
    expected_q1_before = q0_before.copy()
    expected_q1_before[0] = 0.5
    check(q1_before == expected_q1_before, f"L{length} authenticated half-record source initial record")
    check(abs(sum(dq) - 0.5) < 2e-8, f"L{length} terminal half-record retention")
    check(abs(sum(abs(value) for value in residual0) - controls["baseline_transport_residual_l1"]) < 4e-14, f"L{length} baseline ledger recomputation")
    check(abs(sum(abs(value) for value in residual1) - controls["perturbed_transport_residual_l1"]) < 4e-14, f"L{length} perturbed ledger recomputation")
    check(abs(sum(abs(value) for value in differential) - controls["full_differential_residual_l1"]) < 4e-14, f"L{length} differential ledger L1 recomputation")
    check(abs(max(abs(value) for value in differential) - controls["full_differential_residual_linf"]) < 4e-14, f"L{length} differential ledger Linf recomputation")
    check(controls["full_differential_residual_l1"] < 3e-8, f"L{length} raw target remainder bounded")
    check(max(controls["occupation_refinement_linf"], controls["current_refinement_linf"]) < 4e-8, f"L{length} target q/J refinement")
    check(max(controls["norm_error_max"], controls["energy_error_max"], controls["energy_imag_abs_max"], controls["number_law_max_change"]) < 2e-7, f"L{length} target numerical invariants")
    check(basis["full_dimension"] == 1 << (2 * length), f"L{length} target full dimension")
    check(basis["stabilizer_order"] == 2 and basis["orbit_dimension"] == expected_orbits[length], f"L{length} target marked basis dimensions")
    check(basis["orbit_size_histogram"] == histogram, f"L{length} target orbit size histogram")
    check(basis["signed_edge_orbits"] == expected_edge_orbits[length], f"L{length} target signed edge orbits")
    check(target["source_write_ledger"] == "DELTA_Q_PLUS_EDGE_FLUX_MINUS_W_R_EQUALS_ONE_HALF_PLUS_ZERO_MINUS_ONE_HALF_EQUALS_ZERO", f"L{length} source write ledger")

    rebuilt_shells = []
    covered = []
    for radius in sorted(set(min(distances[u], distances[v]) for u, v, _ in edges)):
        for kind in ("internal", "connector"):
            indices = [
                index for index, (u, v, edge_kind) in enumerate(edges)
                if edge_kind == kind and min(distances[u], distances[v]) == radius
            ]
            if not indices:
                continue
            values = [dj[index] for index in indices]
            rebuilt_shells.append({
                "r": radius,
                "kind": kind,
                "edge_count": len(indices),
                "edge_indices": indices,
                "signed_sum_delta_J": sum(values),
                "l1_sum_abs_delta_J": sum(abs(value) for value in values),
                "mean_abs_delta_J": sum(abs(value) for value in values) / len(values),
                "max_abs_delta_J": max(abs(value) for value in values),
            })
            covered.extend(indices)
    check(sorted(covered) == list(range(3 * length)), f"L{length} radial partition owner-once")
    check(len(rebuilt_shells) == len(target["radial_edge_profile"]), f"L{length} all radial bins present")
    shell_error = 0.0
    for observed, expected in zip(target["radial_edge_profile"], rebuilt_shells):
        check((observed["r"], observed["kind"], observed["edge_count"], observed["edge_indices"])
              == (expected["r"], expected["kind"], expected["edge_count"], expected["edge_indices"]),
              f"L{length} radial bin identity r{expected['r']} {expected['kind']}")
        for key in ("signed_sum_delta_J", "l1_sum_abs_delta_J", "mean_abs_delta_J", "max_abs_delta_J"):
            shell_error = max(shell_error, abs(observed[key] - expected[key]))
    check(shell_error < 3e-15, f"L{length} every radial bin numerical recomputation")

    summary = target["response_summary"]
    delta_j_l1 = sum(abs(value) for value in dj)
    delta_j_l2_sq = sum(value * value for value in dj)
    weighted_radius = sum(
        min(distances[u], distances[v]) * abs(dj[index])
        for index, (u, v, _) in enumerate(edges)
    ) / delta_j_l1
    connector_indices = [index for index, edge in enumerate(edges) if edge[2] == "connector"]
    check(abs(summary["delta_J_l1"] - delta_j_l1) < 3e-15, f"L{length} response L1 recomputation")
    check(abs(summary["delta_J_linf"] - max(abs(value) for value in dj)) < 3e-15, f"L{length} response Linf recomputation")
    check(abs(summary["mean_edge_radius_abs_delta_J"] - weighted_radius) < 3e-15, f"L{length} mean finite graph radius recomputation")
    check(abs(summary["effective_responding_edge_count"] - delta_j_l1 ** 2 / delta_j_l2_sq) < 3e-13, f"L{length} effective edge count recomputation")
    check(abs(summary["total_absolute_throughput_change"] - (sum(abs(value) for value in j1) - sum(abs(value) for value in j0))) < 3e-15, f"L{length} total throughput recomputation")
    check(abs(summary["connector_absolute_throughput_change"] - (sum(abs(j1[i]) for i in connector_indices) - sum(abs(j0[i]) for i in connector_indices))) < 3e-15, f"L{length} connector throughput recomputation")
    check(target["residual_status"] == "RAW_UNASSIGNED_NUMERICAL_DIFFERENTIAL_LEDGER_TERMS__NOT_CALLED_DEFECTS", f"L{length} raw remainder terminology")
    check(target["profile_status"] == "FINITE_SUPPORT_GRAPH_DISTANCE_ONLY__NOT_PHYSICAL_RADIUS_OR_GRID", f"L{length} finite graph-distance ceiling")
    check(target["scope"] == "FINITE_SUPPORT_GRAPH_PROFILE__NO_PHYSICAL_DISTANCE_OR_CONTINUUM_INFERENCE", f"L{length} scope ceiling")
    check(target["not_claimed"] == ROW_NOT_CLAIMED, f"L{length} prohibited promotion ceiling")
    check("GATE_A_P" in target["claim_classes"]["open"], f"L{length} Gate A-P open")

    if length in (6, 8):
        independent_vectors = prior_rows[length]["vectors"]
        target_vectors = {
            "baseline_q_after": q0,
            "perturbed_q_after": q1,
            "delta_q_after": dq,
            "baseline_J": j0,
            "perturbed_J": j1,
            "delta_J": dj,
        }
        for key, values in target_vectors.items():
            check(max(abs(a - b) for a, b in zip(independent_vectors[key], values)) < 4e-11,
                  f"L{length} complete full-space parity {key}")
        direct_controls = target["numerical_controls"]["direct_full_space_parity"]
        check(max(value for key, value in direct_controls.items() if key != "sha256") < 4e-10,
              f"L{length} target direct-parity controls")

    by_radius_l1 = defaultdict(float)
    by_radius_signed = defaultdict(float)
    by_radius_max = defaultdict(float)
    by_radius_kind = {}
    for shell in rebuilt_shells:
        radius = shell["r"]
        by_radius_l1[radius] += shell["l1_sum_abs_delta_J"]
        by_radius_signed[radius] += shell["signed_sum_delta_J"]
        by_radius_max[radius] = max(by_radius_max[radius], shell["max_abs_delta_J"])
        by_radius_kind[f"r{radius}__{shell['kind']}"] = {
            key: shell[key] for key in (
                "edge_count", "signed_sum_delta_J", "l1_sum_abs_delta_J",
                "mean_abs_delta_J", "max_abs_delta_J"
            )
        }
    farthest = max(by_radius_l1)
    recompiled_rows.append({
        "L": length,
        "delta_q_terminal_sum": summary["delta_q_terminal_sum"],
        "delta_J_l1": summary["delta_J_l1"],
        "delta_J_linf": summary["delta_J_linf"],
        "total_absolute_throughput_change": summary["total_absolute_throughput_change"],
        "connector_absolute_throughput_change": summary["connector_absolute_throughput_change"],
        "mean_edge_radius_abs_delta_J": summary["mean_edge_radius_abs_delta_J"],
        "effective_responding_edge_count": summary["effective_responding_edge_count"],
        "edge_profile_l1_by_radius": {str(radius): by_radius_l1[radius] for radius in sorted(by_radius_l1)},
        "edge_profile_signed_by_radius": {str(radius): by_radius_signed[radius] for radius in sorted(by_radius_signed)},
        "edge_profile_max_by_radius": {str(radius): by_radius_max[radius] for radius in sorted(by_radius_max)},
        "edge_profile_by_radius_and_kind": by_radius_kind,
        "farthest_edge_radius": farthest,
        "farthest_shell_l1": by_radius_l1[farthest],
        "farthest_shell_fraction_of_delta_J_l1": by_radius_l1[farthest] / summary["delta_J_l1"],
        "full_differential_residual_l1": controls["full_differential_residual_l1"],
        "full_differential_residual_linf": controls["full_differential_residual_linf"],
        "baseline_q_reproduction_linf": controls["baseline_q_reproduction_linf"],
        "baseline_current_reproduction_linf": controls["baseline_current_reproduction_linf"],
        "current_refinement_linf": controls["current_refinement_linf"],
    })

check(recompiled_rows == compiled["rows"], "independent exact compilation of every available row")
check(compiled["checks_passed"] == compiled["checks_total"] == 23 and not compiled["failures"], "compiled target 23/23")
check(compiled["not_claimed"] == COMPILED_NOT_CLAIMED, "compiled prohibited promotion ceiling")
check("GATE_A_P" in compiled["claim_classes"]["open"], "compiled Gate A-P open")
check(compiled["L14_status"]["response_row"] is None, "compiled L14 response row absent")

mps = json.loads(MPS.read_text())
check(mps["target_compute_imported"] is False, "MPS target compute not imported")
check(mps["complete_vectors_emitted"] == ["baseline_q_after", "perturbed_q_after", "delta_q_after", "baseline_J", "perturbed_J", "delta_J"], "MPS complete vector output declaration")
check(mps["acceptance"]["disposition"] == "PASS__BOUNDED_APPROXIMATE_CORROBORATION__NOT_EXACT_PARITY", "MPS approximate disposition")
for row in mps["rows"]:
    length = row["L"]
    check(length in (10, 12), f"L{length} MPS row scope")
    check(max(row["target_reproduction_linf"].values()) < mps["acceptance"]["complete_vector_target_linf_ceiling"], f"L{length} independent MPS complete vectors reproduce target")
    check(max(row["coarse_fine_linf"].values()) < mps["acceptance"]["coarse_fine_linf_ceiling"], f"L{length} independent MPS refinement")
    check(min(row["fine_norms"].values()) > mps["acceptance"]["minimum_fine_norm"], f"L{length} independent MPS retained norm")
    check(row["differential_ledger"]["L1"] < mps["acceptance"]["differential_ledger_l1_ceiling"], f"L{length} independent MPS approximate differential ledger")
    check(row["differential_ledger"]["incidence_column_sum_linf"] == 0.0, f"L{length} independent MPS exact owner telescoping")
check(mps["residual_status"] == "RAW_UNASSIGNED_APPROXIMATION_REMAINDER__NOT_CALLED_A_DEFECT", "MPS raw remainder terminology")
check("GATE_A_P" in mps["claim_classes"]["open"] and "EXACT_MPS_EQUALITY" in mps["not_claimed"], "MPS claim ceiling")

full_l14 = 1 << 28
orbit_l14 = (full_l14 + (1 << 16)) // 2
edge_count_l14 = 42
transition_upper = orbit_l14 * edge_count_l14
dominant_payload = {
    "orbit_ids_int32": 4 * full_l14,
    "orbit_representatives_uint32": 4 * orbit_l14,
    "orbit_sizes_uint8": orbit_l14,
    "csr_offsets_int64": 8 * (orbit_l14 + 1),
    "transition_destinations_int32_upper": 4 * transition_upper,
    "transition_coefficients_float64_upper": 8 * transition_upper,
    "transition_current_codes_int8_upper": transition_upper,
    "six_two_history_complex128_vectors": 6 * orbit_l14 * 2 * 16,
}
target_payload = screen["resource_upper_bound"]["payload_bytes_by_array_upper"]
check(screen["checks_passed"] == screen["checks_total"] == 5 and not screen["failures"], "L14 target screen 5/5")
check(screen["full_dimension"] == full_l14 and screen["orbit_dimension"] == orbit_l14, "L14 independent dimensions")
check(screen["signed_edge_orbits"] == expected_edge_orbits[14], "L14 independent signed edge orbits")
check(screen["resource_upper_bound"]["transition_entries_upper"] == transition_upper, "L14 independent transition upper")
check(all(target_payload[key] == value for key, value in dominant_payload.items()), "L14 independent fixed-width array arithmetic")
check(sum(target_payload.values()) == screen["resource_upper_bound"]["raw_numeric_payload_upper_bytes"], "L14 resource total arithmetic")
check(sum(dominant_payload.values()) > screen["resource_upper_bound"]["guard_bytes"], "L14 guard rejected without thread-dependent reduction bytes")
check(screen["decision"] == "NOT_ELIGIBLE_UNDER_CURRENT_UNAGGREGATED_REPRESENTATION" and not screen["resource_upper_bound"]["passes_upper_bound_guard"], "L14 pre-allocation rejection")
check("L14_RESPONSE" in screen["not_claimed"] and compiled["L14_status"]["response_row"] is None, "no L14 response or extrapolation")

compile_run = subprocess.run(
    [sys.executable, str(TARGET / "compile_response.py")],
    cwd=ROOT,
    check=False,
    text=True,
    capture_output=True,
)
check(compile_run.returncode == 0 and "PASS__R_GATE_AP_MARKED_SOURCE_RESPONSE_L6_L12_WITH_L14_GUARD__23/23" in compile_run.stdout,
      "target compiler exact replay")

sealed = json.loads((HERE / "RESULT.json").read_text())
check(sealed["schema"] == "AUDIT_R_GATE_AP_MARKED_SOURCE_RESPONSE_L6_L12_WITH_L14_GUARD_V001", "sealed audit schema")
check(sealed["verdict"] == "PASS__HOSTILE_MARKED_SOURCE_RESPONSE_AUDIT", "sealed audit verdict")
check(sealed["discrepancies"] == [], "sealed discrepancy census empty")
check(sealed["audit_checks"] == "309/309", "sealed audit check count")
check(sealed["target_checks"] == {"L6": "35/35", "L8": "35/35", "L10": "29/29", "L12": "29/29", "compiled": "23/23", "L14_screen": "5/5"}, "sealed target check counts")
check(sealed["Gate_A_P"] == "OPEN", "sealed Gate A-P open")
check(sealed["L14_disposition"]["response_row"] is None and sealed["L14_disposition"]["decision"] == screen["decision"], "sealed L14 no-response disposition")
check(sealed["residual_status"].endswith("NOT_CALLED_DEFECTS") and sealed["profile_status"].endswith("NO_PHYSICAL_DISTANCE_OR_BOUNDARY_MAP"), "sealed terminology and graph-distance ceiling")

failures = [label for passed, label in checks if not passed]
out = {
    "schema": "AUDIT_R_GATE_AP_MARKED_SOURCE_RESPONSE_L6_L12_WITH_L14_GUARD_V001",
    "verdict": "PASS__HOSTILE_MARKED_SOURCE_RESPONSE_AUDIT" if not failures else "FAIL_CLOSED__HOSTILE_MARKED_SOURCE_RESPONSE_AUDIT",
    "target_checks": {"L6": "35/35", "L8": "35/35", "L10": "29/29", "L12": "29/29", "compiled": "23/23", "L14_screen": "5/5"},
    "prior_exact_full_space_parity": {"L6": "COMPLETE_6_VECTOR_PARITY", "L8": "COMPLETE_6_VECTOR_PARITY"},
    "independent_structure": {str(length): structural_rows[length] for length in sorted(structural_rows)},
    "independent_L6_projected_action": quotient_control,
    "independent_L10_L12_numerics": {
        "classification": mps["classification"],
        "acceptance": mps["acceptance"],
        "rows": mps["rows"],
    },
    "L14_disposition": {
        "decision": screen["decision"],
        "dominant_payload_lower_bytes": sum(dominant_payload.values()),
        "target_upper_bytes": screen["resource_upper_bound"]["raw_numeric_payload_upper_bytes"],
        "guard_bytes": screen["resource_upper_bound"]["guard_bytes"],
        "response_row": None,
    },
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_NUMERICAL_AND_APPROXIMATION_REMAINDERS__NOT_CALLED_DEFECTS",
    "profile_status": "FINITE_SUPPORT_GRAPH_DISTANCE_ONLY__NO_PHYSICAL_DISTANCE_OR_BOUNDARY_MAP",
    "Gate_A_P": "OPEN",
    "claim_classes": {
        "proved": "SOURCE_PARENT_AUDIT_CUSTODY__OWNER_ONCE_INCIDENCE_TELESCOPING__ORDER_TWO_STABILIZER__BURNSIDE_DIMENSIONS__SIGNED_EDGE_OWNERSHIP__L14_PREALLOCATION_REJECTION",
        "adopted": "F3_MDC_ALPHA_EQUALS_R0__CANONICAL_LOCAL_SOURCE_LABEL",
        "conditional": "FINITE_SUPPORT__KAPPA__CONTENT__ROUTING__READ__TARGET_AND_MPS_NUMERICAL_REPRESENTATIONS",
        "empirical": "EXACT_L6_L8_FULL_SPACE_PARITY__REFINED_TARGET_L10_L12_ROWS__APPROXIMATE_INDEPENDENT_L10_L12_COMPLETE_VECTOR_CORROBORATION",
        "open": "EXACT_INDEPENDENT_L10_L12_PARITY__L14_RESPONSE_UNDER_A_DIFFERENT_VALIDATED_REPRESENTATION__PHYSICAL_DISTANCE_AND_BOUNDARY__LOCALITY_OR_SCALING_LAW__GATE_A_P",
    },
    "not_claimed": "EXACT_INDEPENDENT_L10_L12_PARITY__COMPLETE_L6_TO_L14_NUMERICAL_LADDER__L14_RESPONSE__LOCALITY_OR_SCALING_THEOREM__PHYSICAL_BOUNDARY_REFLECTION__UNIFORM_OR_ASYMPTOTIC_PROFILE__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
}
print("AUDIT_RESULT_JSON_BEGIN")
print(json.dumps(out, indent=2, sort_keys=True))
print("AUDIT_RESULT_JSON_END")
if failures:
    raise AssertionError(failures)
print(f"PASS__AUDIT_R_GATE_AP_MARKED_SOURCE_RESPONSE_L6_L12_WITH_L14_GUARD__{len(checks)}/{len(checks)}")
