#!/usr/bin/env python3
"""Hostile reconstruction of the finite localized-source response protocol."""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "INDEPENDENT_RESULT.json"
TARGET = ROOT / "DEVELOPMENT_R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_PROTOCOL_V001"
TRAJECTORY = ROOT / "DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001" / "RESULT.json"
TRAJECTORY_AUDIT = ROOT / "AUDIT_R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001" / "RESULT.json"
SOURCE_THEOREM = ROOT / "DEVELOPMENT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001" / "THEOREM.md"
SOURCE_AUDIT = ROOT / "AUDIT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001" / "INDEPENDENT_RESULT.json"
PARENT = ROOT / "DEVELOPMENT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001" / "RESULT.json"
PARENT_AUDIT = ROOT / "AUDIT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001" / "INDEPENDENT_RESULT.json"
SIZES = (6, 8, 10, 12, 14)
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
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def compose(left, right):
    """Compose permutations as left after right."""
    return tuple(left[right[index]] for index in range(len(left)))


def generated_group(length: int):
    """Generate the support group from two graph automorphisms, not a formula list."""
    count = 2 * length

    def vertex(layer, site):
        return layer * length + site % length

    # R interchanges rings and advances the old layer-zero coordinate by two.
    rotation = tuple(
        vertex(1 - layer, site + (2 if layer == 0 else 0))
        for layer in range(2)
        for site in range(length)
    )
    # F fixes marked vertex (0,0) and reflects both rings compatibly with diagonals.
    reflection = tuple(
        vertex(layer, -site if layer == 0 else 2 - site)
        for layer in range(2)
        for site in range(length)
    )
    identity = tuple(range(count))
    group = {identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for generator in (rotation, reflection):
            candidate = compose(generator, current)
            if candidate not in group:
                group.add(candidate)
                queue.append(candidate)
    return group


def cycle_count(permutation):
    seen = set()
    cycles = 0
    for start in range(len(permutation)):
        if start in seen:
            continue
        cycles += 1
        cursor = start
        while cursor not in seen:
            seen.add(cursor)
            cursor = permutation[cursor]
    return cycles


def support_edges(length: int):
    """Build two cyclic internal supports and the owner-once diagonal matching."""
    edges = []
    for layer in range(2):
        for site in range(length):
            edges.append((layer * length + site,
                          layer * length + (site + 1) % length,
                          "internal"))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


def graph_distances(vertex_count: int, edges, source: int):
    neighbors = [set() for _ in range(vertex_count)]
    for left, right, _ in edges:
        neighbors[left].add(right)
        neighbors[right].add(left)
    distances = [None] * vertex_count
    distances[source] = 0
    queue = deque([source])
    while queue:
        left = queue.popleft()
        for right in neighbors[left]:
            if distances[right] is None:
                distances[right] = distances[left] + 1
                queue.append(right)
    return distances, neighbors


if any(digest(path) != expected for path, expected in PINS.items()):
    raise AssertionError("target or antecedent custody mismatch")

target = json.loads((TARGET / "RESULT.json").read_text())
trajectory = json.loads(TRAJECTORY.read_text())
trajectory_audit = json.loads(TRAJECTORY_AUDIT.read_text())
source_theorem = SOURCE_THEOREM.read_text()
source_audit = json.loads(SOURCE_AUDIT.read_text())
parent = json.loads(PARENT.read_text())
parent_audit = json.loads(PARENT_AUDIT.read_text())
protocol = (TARGET / "PROTOCOL.md").read_text()
readme = (TARGET / "README.md").read_text()

# Reconstruct the inherited two-stage parent preparation on pair basis
# |BB>, |Bx>, |xB>, |xx>.  The write produces (|BB>-i|xB>)/sqrt(2), and
# native transfer sends |xB> to i|Bx>, leaving the even tail blank.
root_half = 1.0 / math.sqrt(2.0)
after_write = (root_half, 0j, -1j * root_half, 0j)
after_transfer = (after_write[0], 1j * after_write[2],
                  1j * after_write[1], after_write[3])
expected_parent_pair = (root_half, root_half, 0j, 0j)
parent_pair_error = max(abs(left - right)
                        for left, right in zip(after_transfer, expected_parent_pair))
baseline_tail_q = abs(after_transfer[2]) ** 2 + abs(after_transfer[3]) ** 2
baseline_head_q = abs(after_transfer[1]) ** 2 + abs(after_transfer[3]) ** 2

# A subsequent authenticated write acts on that blank even tail.  It is the
# retained target of the audited map, so no second transfer is part of this
# insertion.  The odd-head baseline factor is unchanged.
local_tail = (root_half, -1j * root_half)
local_norm = sum(abs(value) ** 2 for value in local_tail)
local_delta_q = abs(local_tail[1]) ** 2 - baseline_tail_q
write_flux = 0.0
write_amount = 0.5
write_balance = local_delta_q + write_flux - write_amount

representations = []
profiles = []
support_valid = []
for length in SIZES:
    group = generated_group(length)
    edges = support_edges(length)
    edge_set = {frozenset((left, right)) for left, right, _ in edges}
    automorphisms = all(
        all(frozenset((permutation[left], permutation[right])) in edge_set
            for left, right, _ in edges)
        for permutation in group
    )
    stabilizer = [permutation for permutation in group if permutation[0] == 0]
    source_orbit = {permutation[0] for permutation in group}
    stabilizer_cycles = sorted(cycle_count(permutation) for permutation in stabilizer)
    marked_burnside_sum = sum(1 << cycle_count(permutation)
                              for permutation in stabilizer)
    full_burnside_sum = sum(1 << cycle_count(permutation) for permutation in group)
    distances, neighbors = graph_distances(2 * length, edges, 0)
    shell_counts = Counter(
        (min(distances[left], distances[right]), kind)
        for left, right, kind in edges
    )
    profile = {
        "L": length,
        "site_graph_radius": max(distances),
        "edge_shell_rule": "R_E_EQUALS_MIN_DISTANCE_SOURCE_TO_EITHER_ENDPOINT",
        "edge_shell_counts": [
            {"r": radius, "kind": kind, "edges": count}
            for (radius, kind), count in sorted(shell_counts.items())
        ],
    }
    representation = {
        "L": length,
        "full_group_order": len(group),
        "source_orbit_size": len(source_orbit),
        "marked_stabilizer_order": len(stabilizer),
        "marked_stabilizer_cycle_counts": stabilizer_cycles,
        "marked_burnside_sum": marked_burnside_sum,
        "marked_orbit_dimension": marked_burnside_sum // len(stabilizer),
        "full_invariant_orbit_dimension": full_burnside_sum // len(group),
    }
    representations.append(representation)
    profiles.append(profile)
    support_valid.append(
        automorphisms
        and len(group) == 2 * length
        and source_orbit == set(range(0, 2 * length, 2))
        and len(stabilizer) == 2
        and stabilizer_cycles == [length + 2, 2 * length]
        and len(edges) == 3 * length
        and all(len(adjacency) == 3 for adjacency in neighbors)
        and all(distance is not None for distance in distances)
        and sum(shell_counts.values()) == 3 * length
    )

target_representations = target["marked_source_representation"]
target_representation_projection = [
    {
        "L": row["L"],
        "full_source_preserving_group_order": row["full_group_order"],
        "selected_site_stabilizer_order": row["marked_stabilizer_order"],
        "marked_source_burnside_sum": row["marked_burnside_sum"],
        "marked_source_orbit_dimension": row["marked_orbit_dimension"],
    }
    for row in representations
]

trajectory_rows = {row["L"]: row for row in trajectory["rows"]}
expected_background = [
    {
        "L": length,
        "total_throughput_per_retained": trajectory_rows[length]["absolute_oriented_throughput_per_retained"],
        "connector_throughput_per_retained": trajectory_rows[length]["absolute_connector_throughput_per_retained"],
        "max_abs_connected_edge_correlation": trajectory_rows[length]["max_abs_connected_edge_correlation"],
        "raw_residual_l1_per_component": trajectory_rows[length]["record_ledger_residual_l1_per_component"],
    }
    for length in SIZES
]

execution_gates = set(target["execution_gates"])
claim_classes = target["claim_classes"]
checks = [
    (target["checks_passed"] == target["checks_total"] == 20, "target protocol 20/20"),
    (trajectory["checks_passed"] == trajectory["checks_total"] == 18, "sealed trajectory 18/18"),
    (trajectory_audit["independent_checks"] == "31/31", "sealed trajectory hostile audit"),
    (source_audit["disposition"] == "PASS_AT_CONDITIONAL_SINGLE_HISTORY_WITNESS_SCOPE", "source audit disposition"),
    (source_audit["ledger"] == {"W_R": "1/2", "balance": "0", "boundary_flux_total": "0", "delta_Q_R": "1/2", "raw_source_coefficient": "14441248/6075", "source_pulse": "Phi=pi/4"}, "source audit exact ledger"),
    ("r_0={14441248\\over6075}" in source_theorem.replace(" ", ""), "raw source coefficient identity"),
    (parent["physical_parent_selection"]["source_preparation"] == "F3_MDC_WRITE_PHI_PI_OVER_4_THEN_NATIVE_TRANSFER_THETA_PI_OVER_2", "parent two-stage preparation"),
    (parent["physical_parent_selection"]["prepared_cycle_state"] == "EVEN_TAILS_BLANK__ODD_HEADS_(B_PLUS_X)_OVER_SQRT2", "parent blank even targets"),
    (parent["physical_parent_selection"]["source_status_during_accumulation"] == "OFF", "parent source-off evolution"),
    (parent_audit["disposition"] == "PASS_AFTER_REQUIRED_LEDGER_RECLASSIFICATION", "parent hostile disposition"),
    (parent_pair_error < 1e-15 and baseline_tail_q == 0.0 and abs(baseline_head_q - 0.5) < 1e-15, "independent parent pair map"),
    (abs(local_norm - 1.0) < 1e-15 and abs(local_delta_q - 0.5) < 1e-15, "independent local write state"),
    (abs(write_balance) < 1e-15, "terms-off local ledger"),
    (target["localized_source"]["inserted_site_state"] == "B_MINUS_I_X_OVER_SQRT2", "target local phase"),
    (target["localized_source"]["transport_slice"] == "SOURCE_AND_WRITER_OFF__ORIGINAL_OWNER_ONCE_CONNECTED_SUPPORT_RESTORED", "source/writer removal and support restoration"),
    (all(support_valid), "independent finite support/group reconstruction"),
    (target_representation_projection == target_representations, "marked representation agreement"),
    (profiles == target["radial_partitions"], "finite radial partition agreement"),
    (all(row["source_orbit_size"] == row["L"] > 1 for row in representations), "local marker breaks full invariance"),
    (representations[-1]["marked_orbit_dimension"] == 134250496 and representations[-1]["full_invariant_orbit_dimension"] == 9608050, "L14 marked/full dimensions"),
    (target["background_reference"]["response_rows"] == expected_background, "baseline values pinned without response data"),
    (target["background_reference"]["evidence_class"].endswith("NOT_PROVED_ASYMPTOTE_OR_INVARIANT"), "finite baseline ceiling"),
    (target["differential_observables"]["full_differential_ledger"] == "DELTA_Q_AFTER_PLUS_B_DELTA_J_MINUS_W_R_DELTA_SOURCE_SITE_EQUALS_R_NUM_DIFFERENTIAL", "differential ledger sign"),
    (target["differential_observables"]["global_sum"] == "SUM_I_DELTA_Q_I_AFTER_EQUALS_W_R_EQUALS_ONE_HALF", "owner-once telescope consequence"),
    ("USE_MARKED_SOURCE_OR_EQUIVALENT_NONINVARIANT_SECTOR__FULL_INVARIANT_BASIS_IS_INVALID_FOR_LOCAL_INSERTION" in execution_gates, "noninvariant engine gate"),
    ("MATCH_DIRECT_FULL_SPACE_L6_AND_L8_COMPLETE_Q_AND_J_VECTORS_BEFORE_L10_TO_L14" in execution_gates, "full-space validation gate"),
    ("PASS_SEPARATE_MEMORY_SCREEN_AT_EACH_L__DO_NOT_FORCE_L14" in execution_gates, "per-size resource and L14 stop gate"),
    ("RUN_INDEPENDENT_COARSE_FINE_EVOLUTION_AND_CURRENT_QUADRATURE" in execution_gates, "numerical refinement gate"),
    ("REQUIRE_INDEPENDENT_HOSTILE_AUDIT_BEFORE_PROMOTION" in execution_gates, "hostile promotion gate"),
    (claim_classes["empirical"].endswith("NO_LOCALIZED_RESPONSE_DATA_YET"), "no response result claimed"),
    ("GATE_A_P" in claim_classes["open"], "Gate A-P remains open"),
    (target["not_claimed"] == NOT_CLAIMED, "structured claim ceiling"),
    ("not physical distance" in protocol and "not a physical" in protocol and "boundary reflection" in protocol, "finite support-distance language"),
    ("L14 is not forced" in protocol and "contains no perturbed response data" in protocol, "protocol resource/data ceiling"),
    ("No asymptotic plateau" in readme and "gravity" in readme, "README finite physical ceiling"),
]
failures = [label for passed, label in checks if not passed]

out = {
    "schema": "AUDIT_R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_PROTOCOL_V001",
    "verdict": "PASS__FINITE_PROTOCOL_AUTHENTICATED_NO_RESPONSE_RESULT" if not failures else "FAIL_CLOSED",
    "method": "PINNED_ANTECEDENTS__INDEPENDENT_PAIR_MAP__GENERATOR_CLOSURE__BURNSIDE__GRAPH_BFS__CLAIM_SCREEN",
    "input_sha256": {path.relative_to(ROOT).as_posix(): expected for path, expected in PINS.items()},
    "source_parent_attachment": {
        "parent_pair_after_write": "(BB_MINUS_I_XB)_OVER_SQRT2",
        "parent_pair_after_native_transfer": "B_TAIL_TENSOR_(B_HEAD_PLUS_X_HEAD)_OVER_SQRT2",
        "baseline_even_tail_q": "0",
        "baseline_odd_head_q": "1/2",
        "localized_even_tail_state": "(B_MINUS_I_X)_OVER_SQRT2",
        "localized_delta_q": "1/2",
        "write_amount": "1/2",
        "write_edge_flux": "0",
        "write_balance": "0",
        "second_native_transfer_required": False,
        "reason": "LOCAL_INTERVENTION_WRITES_THE_NOW_BLANK_AUTHENTICATED_EVEN_TAIL_TARGET_AND_THEN_RESTORES_TRANSPORT",
    },
    "differential_ledger": {
        "identity": "DELTA_Q_AFTER_PLUS_B_DELTA_J_MINUS_ONE_HALF_E_SOURCE_EQUALS_DIFFERENTIAL_NUMERICAL_REMAINDER",
        "derivation": "PERTURBED_CONTINUITY_MINUS_BASELINE_CONTINUITY_WITH_DELTA_Q_BEFORE_EQUALS_ONE_HALF_E_SOURCE",
        "owner_once_column_sum": 0,
        "global_number_response": "ONE_HALF_WITHIN_SEPARATELY_CONTROLLED_NUMERICAL_REMAINDER",
        "remainder_status": "RAW_UNASSIGNED__NOT_CALLED_DEFECT",
    },
    "representations": representations,
    "radial_partition_summary": [
        {
            "L": profile["L"],
            "site_graph_radius": profile["site_graph_radius"],
            "owner_once_edge_count": sum(
                row["edges"] for row in profile["edge_shell_counts"]
            ),
            "canonical_json_sha256": canonical_digest(profile),
        }
        for profile in profiles
    ],
    "execution_status": {
        "protocol_only": True,
        "localized_response_data_present": False,
        "full_space_validation_required": [6, 8],
        "larger_sizes_resource_gated": [10, 12, 14],
        "L14_forced": False,
        "Gate_A_P": "OPEN",
    },
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "claim_ceiling": "FINITE_MICROSCOPIC_LOCALIZED_RESPONSE_PROTOCOL_ONLY",
    "not_claimed": NOT_CLAIMED,
}

if OUT.exists():
    if out != json.loads(OUT.read_text()):
        raise AssertionError("saved independent result differs")
else:
    print("INDEPENDENT_RESULT_BEGIN")
    print(json.dumps(out, indent=2, sort_keys=True))
    print("INDEPENDENT_RESULT_END")
if failures:
    raise AssertionError(failures)
print(f"PASS__HOSTILE_GATE_AP_LOCALIZED_PROTOCOL__{len(checks)}/{len(checks)}")
