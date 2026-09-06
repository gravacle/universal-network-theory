#!/usr/bin/env python3
"""Independent L14 Burnside and fixed-width arithmetic reconstruction."""

from collections import Counter
import json
from pathlib import Path

L = 14
N = 2 * L
E = 3 * L
ROOT = Path(__file__).resolve().parent
CANON = ROOT / "RESULT.json"


def action(reflection: int, shift: int):
    """Act in prism coordinates (p=i-layer), then return native indices."""
    permutation = []
    for layer in range(2):
        for native in range(L):
            prism = (native - layer) % L
            out_layer = layer ^ (shift & 1)
            out_prism = (reflection * prism + shift) % L
            permutation.append(out_layer * L + (out_prism + out_layer) % L)
    return tuple(permutation)


def cycles(permutation):
    unseen = set(range(N))
    answer = []
    while unseen:
        start = min(unseen)
        cursor = start
        size = 0
        while cursor in unseen:
            unseen.remove(cursor)
            size += 1
            cursor = permutation[cursor]
        assert cursor == start
        answer.append(size)
    return tuple(sorted(answer))


group = [action(sign, shift) for sign in (1, -1) for shift in range(L)]
assert len(group) == len(set(group)) == 28
census = Counter(cycles(g) for g in group)
expected = Counter({
    (14, 14): 6,
    (7, 7, 7, 7): 6,
    (2,) * 14: 8,
    (1, 1, 1, 1) + (2,) * 12: 7,
    (1,) * 28: 1,
})
assert census == expected
fixed_sum = sum(multiplicity * 2 ** len(shape) for shape, multiplicity in census.items())
orbits, remainder = divmod(fixed_sum, len(group))
assert remainder == 0

# One deterministic swap attempt per owner-once edge per representative gives
# an allocation ceiling, before duplicate destinations or zero terms collapse.
transition_slots = orbits * E
full_words = 2 ** N
arrays = {
    "orbit_ids_int32": full_words * 4,
    "orbit_representatives_uint32": orbits * 4,
    "orbit_sizes_uint8": orbits,
    "csr_row_offsets_int64": (orbits + 1) * 8,
    "transition_destinations_int32_upper": transition_slots * 4,
    "transition_coefficients_float64_upper": transition_slots * 8,
    "two_raw_current_kernels_upper": 2 * (full_words // 2) * (4 + 4 + 8),
    "six_complex128_work_vectors": 6 * orbits * 16,
    "stream_block_allowance": (2 ** 20) * 64,
}
payload = sum(arrays.values())

observed = {
    "schema": "AUDIT_R_CONNECTED_L14_FEASIBILITY_SCREEN_V001",
    "classification": "INDEPENDENT_ENGINEERING_SCREEN_AUDIT__NO_L14_ACCUMULATION",
    "group_order": len(group),
    "cycle_census": [
        {"cycle_lengths": list(shape), "multiplicity": census[shape],
         "fixed_words_per_element": 2 ** len(shape)}
        for shape in sorted(census, key=lambda x: (len(x), x))
    ],
    "burnside_fixed_word_sum": fixed_sum,
    "orbit_dimension": orbits,
    "owner_once_edges_per_representative": E,
    "transition_slots_upper": transition_slots,
    "transition_ceiling_interpretation": "ALLOCATION_UPPER_BOUND__NOT_ACTUAL_DISTINCT_OR_NONZERO_QUOTIENT_NNZ",
    "payload_bytes_by_array": arrays,
    "raw_numeric_payload_upper_bytes": payload,
    "raw_numeric_payload_upper_gib": payload / 2 ** 30,
    "declared_capacity_bytes": 48 * 2 ** 30,
    "raw_payload_headroom_bytes": 48 * 2 ** 30 - payload,
    "decision": "PASS__GUARDED_IMPLEMENTATION_TRIAL_ELIGIBILITY_ONLY",
    "not_certified": ["L14_EXECUTION", "L14_PROCESS_RSS", "L14_RUNTIME", "L14_ACCUMULATION", "GRID", "CONTINUUM", "WARD", "PHASE", "GRAVITON", "GRAVITY"],
}
assert observed == json.loads(CANON.read_text())
print("PASS__INDEPENDENT_L14_FEASIBILITY_RECONSTRUCTION")
