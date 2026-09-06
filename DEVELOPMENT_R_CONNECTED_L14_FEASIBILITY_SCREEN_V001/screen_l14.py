#!/usr/bin/env python3
"""Exact structural and fixed-width-payload screen for the same-slice L14 run."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


LENGTH = 14
SITES = 2 * LENGTH
EDGES = 3 * LENGTH
GROUP_ORDER = 2 * LENGTH
FULL_DIMENSION = 1 << SITES
DECLARED_CAPACITY_BYTES = 48 * (1 << 30)
STREAM_BLOCK_WORDS = 1 << 20
ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).with_name("RESULT.json")
L12_RESULT = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L12_ACCUMULATION_V001" / "RESULT.json"
L12_SCRIPT = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L12_ACCUMULATION_V001" / "compute_connected_l12.py"
L12_OBSERVATION = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L12_ACCUMULATION_V001" / "RUN_OBSERVATION.md"
PRISM_RESULT = ROOT / "DEVELOPMENT_R_CONNECTED_PRISM_ORBIT_REDUCTION_V001" / "RESULT.json"
PRISM_THEOREM = ROOT / "DEVELOPMENT_R_CONNECTED_PRISM_ORBIT_REDUCTION_V001" / "THEOREM.md"
PINNED_HASHES = {
    L12_RESULT: "154c9195b8ea516e4e637c1f4d66422ab82603163119f9b4451e7c2eb7ff5184",
    L12_SCRIPT: "ec75d74a4517d457504306a5b83433d4061a510aa0d699d74e600575130a6805",
    L12_OBSERVATION: "05514fada531ead89cdbffa8f407cd04b32675a98c5e7c4bf93b5b27966195ea",
    PRISM_RESULT: "f4b7079f085d63de94fa3f35f5e862e05b94b482386d999818d0a33c86821af1",
    PRISM_THEOREM: "d7608c1dca4f44a70e2695596cba6bf0049cdd4c79919c5131ea705c20514a71",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edges_for(length: int):
    out = []
    for layer in range(2):
        for site in range(length):
            out.append((layer * length + site, layer * length + (site + 1) % length, "internal"))
    for site in range(length):
        out.append((site, length + (site + 1) % length, "connector"))
    return out


def prism_group(length: int):
    out = []
    for epsilon in (1, -1):
        for shift in range(length):
            swap = shift % 2
            permutation = []
            for layer in range(2):
                for site in range(length):
                    prism_site = (site - layer) % length
                    moved_layer = layer ^ swap
                    moved_prism_site = (epsilon * prism_site + shift) % length
                    moved_site = (moved_prism_site + moved_layer) % length
                    permutation.append(moved_layer * length + moved_site)
            out.append(tuple(permutation))
    return out


def cycle_lengths(permutation):
    seen = set()
    lengths = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        cursor = start
        length = 0
        while cursor not in seen:
            seen.add(cursor)
            length += 1
            cursor = permutation[cursor]
        lengths.append(length)
    return tuple(sorted(lengths))


def signed_edge_orbits(edges, group):
    lookup = {frozenset((u, v)): (index, u, v) for index, (u, v, _) in enumerate(edges)}
    reconstruction = [None] * len(edges)
    representatives = []
    for edge_index, (u, v, _) in enumerate(edges):
        if reconstruction[edge_index] is not None:
            continue
        representative = len(representatives)
        representatives.append(edge_index)
        observed = {}
        for permutation in group:
            moved_u, moved_v = permutation[u], permutation[v]
            target, stored_u, stored_v = lookup[frozenset((moved_u, moved_v))]
            sign = 1 if (moved_u, moved_v) == (stored_u, stored_v) else -1
            if target in observed and observed[target] != sign:
                raise AssertionError("signed edge orbit has contradictory orientations")
            observed[target] = sign
        for target, sign in observed.items():
            reconstruction[target] = (representative, sign)
    if any(item is None for item in reconstruction):
        raise AssertionError("signed edge reconstruction is incomplete")
    return representatives, reconstruction


group = prism_group(LENGTH)
edges = edges_for(LENGTH)
edge_set = {frozenset((u, v)) for u, v, _ in edges}
support_preserved = all(
    {frozenset((permutation[u], permutation[v])) for u, v, _ in edges} == edge_set
    for permutation in group
)
source_parity_preserved = all(
    permutation[site] % 2 == site % 2
    for permutation in group
    for site in range(SITES)
)
edge_representatives, edge_reconstruction = signed_edge_orbits(edges, group)

cycle_type_counter = Counter(cycle_lengths(permutation) for permutation in group)
burnside_sum = sum(multiplicity * (1 << len(lengths)) for lengths, multiplicity in cycle_type_counter.items())
if burnside_sum % GROUP_ORDER:
    raise AssertionError("Burnside sum is not divisible by group order")
orbit_dimension = burnside_sum // GROUP_ORDER
cycle_types = [
    {
        "cycle_lengths": list(lengths),
        "cycles": len(lengths),
        "fixed_words_per_element": 1 << len(lengths),
        "multiplicity": multiplicity,
    }
    for lengths, multiplicity in sorted(cycle_type_counter.items(), key=lambda item: (len(item[0]), item[0]))
]

# This is an explicit candidate layout, not the payload of the current L12
# Python-list builder.  Each representative produces at most one transition
# per owner-once edge; duplicates may remain unaggregated without changing H.
transition_entries_upper = orbit_dimension * EDGES
payload = {
    "orbit_ids_int32": 4 * FULL_DIMENSION,
    "orbit_representatives_uint32": 4 * orbit_dimension,
    "orbit_sizes_uint8": orbit_dimension,
    "csr_row_offsets_int64": 8 * (orbit_dimension + 1),
    "transition_destinations_int32_upper": 4 * transition_entries_upper,
    "transition_coefficients_float64_upper": 8 * transition_entries_upper,
    "two_raw_current_kernels_upper": 2 * (FULL_DIMENSION // 2) * (4 + 4 + 8),
    "six_complex128_work_vectors": 6 * orbit_dimension * 16,
    "stream_block_allowance": 64 * STREAM_BLOCK_WORDS,
}
payload_upper = sum(payload.values())

l12_result = json.loads(L12_RESULT.read_text())
prism_result = json.loads(PRISM_RESULT.read_text())
l12_observation_text = L12_OBSERVATION.read_text()
rss_match = re.search(r"maximum resident set.*?`([0-9,]+)`", l12_observation_text, re.DOTALL)
runtime_match = re.search(r"wall time observed.*?`([0-9.]+) s`", l12_observation_text, re.DOTALL)
if not rss_match or not runtime_match:
    raise AssertionError("sealed L12 resource observation did not parse")
l12_rss = int(rss_match.group(1).replace(",", ""))
l12_runtime = float(runtime_match.group(1))
l12_orbit_dimension = l12_result["finite_orbit_basis"]["orbit_dimension"]

components = LENGTH * LENGTH // 2
sites_per_layer = components * LENGTH
census = {
    "L": LENGTH,
    "components": components,
    "sites_per_component": SITES,
    "sites_global": components * SITES,
    "sites_per_F3_layer": sites_per_layer,
    "possible_F3_links": sites_per_layer * sites_per_layer,
    "selected_edges_global_owner_once": components * EDGES,
    "prepared_source_lineages": sites_per_layer,
    "expected_retained_global": sites_per_layer // 2,
}

expected_cycle_types = Counter({
    (14, 14): 6,
    (7, 7, 7, 7): 6,
    (2,) * 14: 8,
    (1, 1, 1, 1) + (2,) * 12: 7,
    (1,) * 28: 1,
})
hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in PINNED_HASHES}
checks = [
    (hashes == {path.relative_to(ROOT).as_posix(): value for path, value in PINNED_HASHES.items()}, "sealed input hashes"),
    (len(group) == GROUP_ORDER and len(set(group)) == GROUP_ORDER, "faithful group order"),
    (support_preserved, "support preservation"),
    (source_parity_preserved, "source parity preservation"),
    (len(edges) == EDGES and sum(kind == "connector" for _, _, kind in edges) == LENGTH, "edge census"),
    (len(edge_representatives) == 2 and all(item is not None for item in edge_reconstruction), "signed edge orbit census"),
    (cycle_type_counter == expected_cycle_types, "permutation cycle census"),
    (burnside_sum == 269025400, "Burnside fixed-word sum"),
    (orbit_dimension == 9608050, "exact orbit dimension"),
    (FULL_DIMENSION == 268435456, "full word dimension"),
    (orbit_dimension < (1 << 31) and FULL_DIMENSION <= (1 << 32), "fixed-width index eligibility"),
    (transition_entries_upper == 403538100, "transition entry ceiling"),
    (payload_upper == 11325552642, "candidate fixed-width payload arithmetic"),
    (payload_upper < DECLARED_CAPACITY_BYTES, "candidate raw payload below declared capacity"),
    (DECLARED_CAPACITY_BYTES - payload_upper == 40214054910, "raw payload headroom arithmetic"),
    (census["sites_global"] == 2744 and census["selected_edges_global_owner_once"] == 4116, "global finite census"),
    (l12_orbit_dimension == 704370 and l12_rss == 2399076352, "sealed L12 structural/resource input"),
    (prism_result["checks_passed"] == prism_result["checks_total"] == 40, "sealed prism validation input"),
]
failures = [label for passed, label in checks if not passed]

out = {
    "schema": "R_CONNECTED_L14_FEASIBILITY_SCREEN_V001",
    "classification": "EXACT_FINITE_STRUCTURAL_COUNT__CONDITIONAL_FIXED_WIDTH_IMPLEMENTATION_PAYLOAD_SCREEN__NO_L14_EVOLUTION",
    "scope": "SAME_MICROSCOPIC_RECORD_SLICE__ENGINEERING_FEASIBILITY_ONLY",
    "sealed_inputs_sha256": hashes,
    "census": census,
    "finite_group": {
        "order": GROUP_ORDER,
        "cycle_types": cycle_types,
        "burnside_fixed_word_sum": burnside_sum,
        "full_dimension": FULL_DIMENSION,
        "orbit_dimension": orbit_dimension,
        "signed_edge_orbits": len(edge_representatives),
    },
    "candidate_fixed_width_layout": {
        "transition_entries_upper": transition_entries_upper,
        "payload_bytes_by_array": payload,
        "raw_numeric_payload_upper_bytes": payload_upper,
        "raw_numeric_payload_upper_gib": payload_upper / (1 << 30),
        "declared_host_capacity_bytes": DECLARED_CAPACITY_BYTES,
        "declared_host_capacity_gib": DECLARED_CAPACITY_BYTES / (1 << 30),
        "raw_payload_headroom_bytes": DECLARED_CAPACITY_BYTES - payload_upper,
        "raw_payload_headroom_gib": (DECLARED_CAPACITY_BYTES - payload_upper) / (1 << 30),
        "status": "CAPACITY_NECESSARY_CONDITION_PASSES__PROCESS_RSS_NOT_CERTIFIED",
    },
    "sealed_L12_observation": {
        "orbit_dimension": l12_orbit_dimension,
        "observed_runtime_seconds": l12_runtime,
        "observed_max_rss_bytes": l12_rss,
        "observed_max_rss_gib": l12_rss / (1 << 30),
        "full_dimension_ratio_L14_over_L12": FULL_DIMENSION / (1 << 24),
        "orbit_dimension_ratio_L14_over_L12": orbit_dimension / l12_orbit_dimension,
        "interpretation": "INPUT_ONLY__NO_RUNTIME_OR_RSS_EXTRAPOLATION",
    },
    "screen_decision": "ELIGIBLE_FOR_GUARDED_FIXED_WIDTH_IMPLEMENTATION_TRIAL__NOT_AN_L14_ACCUMULATION_RESULT",
    "required_next_controls": [
        "NO_PYTHON_OBJECT_LISTS_PROPORTIONAL_TO_TRANSITION_COUNT",
        "PHASED_FIXED_WIDTH_ALLOCATION",
        "LIVE_RSS_AND_RUNTIME_LOGGING",
        "ABORT_BEFORE_DECLARED_CAPACITY",
        "INDEPENDENT_HOSTILE_AUDIT_BEFORE_RESULT_PROMOTION",
    ],
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "claim_classes": {
        "proved": "FINITE_GROUP_SUPPORT_AND_SOURCE_PARITY_PRESERVATION__CYCLE_CENSUS__BURNSIDE_ORBIT_COUNT__ARRAY_BYTE_ARITHMETIC",
        "adopted": "INHERITED_F3_MDC_ALPHA_EQUALS_R0__SAME_CONNECTED_COMPONENT_FAMILY",
        "conditional": "SOURCE__SUPPORT__KAPPA__CONTENT__ROUTING__CLOCK__READ__FIXED_WIDTH_CANDIDATE_LAYOUT",
        "empirical": "SEALED_L12_SINGLE_HOST_RUNTIME_AND_RSS_ONLY",
        "open": "L14_CONSTRUCTION__L14_PROCESS_RSS__L14_RUNTIME__L14_EVOLUTION__L14_RECORD_LEDGER",
    },
    "not_claimed": "L14_EXECUTION_FEASIBILITY_GUARANTEE__COMPLEXITY_LAW__MONOTONICITY__CONVERGENCE__LIMIT__FIT__SCALING_LAW__AUTONOMOUS_SUPPORT__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
}


def compatible(observed, canonical, path="root"):
    if isinstance(canonical, dict):
        if not isinstance(observed, dict) or set(observed) != set(canonical):
            raise AssertionError(f"canonical keys differ at {path}")
        for key in canonical:
            compatible(observed[key], canonical[key], f"{path}.{key}")
    elif isinstance(canonical, list):
        if not isinstance(observed, list) or len(observed) != len(canonical):
            raise AssertionError(f"canonical list differs at {path}")
        for index, (left, right) in enumerate(zip(observed, canonical)):
            compatible(left, right, f"{path}[{index}]")
    elif isinstance(canonical, float):
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 1.0e-12:
            raise AssertionError(f"canonical float differs at {path}")
    elif observed != canonical:
        raise AssertionError(f"canonical value differs at {path}")


compatible(out, json.loads(OUT.read_text()))
if failures:
    raise AssertionError(failures)
print(f"PASS__R_CONNECTED_L14_FEASIBILITY_SCREEN__{len(checks)}/{len(checks)}")
