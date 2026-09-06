#!/usr/bin/env python3
"""Target L4 trace for the intrinsic relational admission parent."""

from __future__ import annotations

import hashlib
import json
import math
import platform
import resource
import sys
import time
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
OUT = HERE / "TRACE_L4.json"
PHI = math.pi / 4.0
KAPPA = math.pi / 2.0
TAYLOR_ORDER = 12
TRANSPORT_STEPS = 512
LENGTH = 4
SITES = 8
DONORS = 4
TARGETS = (0, 1, 2, 3)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edges() -> list[tuple[int, int, str]]:
    answer: list[tuple[int, int, str]] = []
    for rail in range(2):
        offset = rail * LENGTH
        for site in range(LENGTH):
            answer.append((offset + site, offset + (site + 1) % LENGTH, f"rail_{rail + 1}"))
    for site in range(LENGTH):
        answer.append((site, LENGTH + (site + 1) % LENGTH, "connector"))
    return answer


WORDS = np.arange(1 << SITES, dtype=np.uint16)
DONOR_WORDS = np.arange(1 << DONORS, dtype=np.uint8)


def bit_counts(words: np.ndarray, width: int) -> np.ndarray:
    work = words.copy()
    result = np.zeros(len(words), dtype=np.uint8)
    for _ in range(width):
        result += (work & 1).astype(np.uint8)
        work >>= 1
    return result


CARRIER_COUNTS = bit_counts(WORDS, SITES)
DONOR_COUNTS = bit_counts(DONOR_WORDS, DONORS)
EDGE_LIST = edges()
ACTIONS: list[tuple[np.ndarray, np.uint16, np.ndarray]] = []
for u, v, _ in EDGE_LIST:
    bit_u = ((WORDS >> u) & 1).astype(np.int8)
    bit_v = ((WORDS >> v) & 1).astype(np.int8)
    active = np.flatnonzero(bit_u != bit_v).astype(np.uint16)
    ACTIONS.append((active, np.uint16((1 << u) | (1 << v)), (bit_v[active] - bit_u[active]).astype(np.int8)))

INCIDENCE = np.zeros((SITES, len(EDGE_LIST)), dtype=np.int8)
for edge_index, (u, v, _) in enumerate(EDGE_LIST):
    INCIDENCE[u, edge_index] = 1
    INCIDENCE[v, edge_index] = -1


def initial_state() -> np.ndarray:
    state = np.zeros((1 << DONORS, 1 << SITES), dtype=np.complex128)
    state[(1 << DONORS) - 1, 0] = 1.0
    return state


def norm(state: np.ndarray) -> float:
    return float(np.vdot(state, state).real)


def retained_q(state: np.ndarray) -> float:
    probability = np.abs(state) ** 2
    return float(np.sum(probability * CARRIER_COUNTS[np.newaxis, :]))


def genesis_q(state: np.ndarray) -> float:
    probability = np.abs(state) ** 2
    return float(np.sum(probability * DONOR_COUNTS[:, np.newaxis]))


def donor_loaded_probability(state: np.ndarray, donor: int) -> float:
    loaded = ((DONOR_WORDS >> donor) & 1) == 1
    return float(np.sum(np.abs(state[loaded, :]) ** 2))


def occupations(state: np.ndarray) -> np.ndarray:
    probability = np.abs(state) ** 2
    return np.array([
        float(np.sum(probability[:, ((WORDS >> site) & 1) == 1]))
        for site in range(SITES)
    ])


def allow_and_blocked(state: np.ndarray, donor: int, target: int) -> tuple[float, float, float]:
    loaded = ((DONOR_WORDS >> donor) & 1) == 1
    spent = ~loaded
    blank = ((WORDS >> target) & 1) == 0
    occupied = ~blank
    allow = float(np.sum(np.abs(state[np.ix_(loaded, blank)]) ** 2))
    blocked = float(np.sum(np.abs(state[np.ix_(loaded, occupied)]) ** 2))
    reverse = float(np.sum(np.abs(state[np.ix_(spent, occupied)]) ** 2))
    return allow, blocked, reverse


def apply_admission(state: np.ndarray, donor: int, target: int) -> np.ndarray:
    out = state.copy()
    loaded_rows = np.flatnonzero(((DONOR_WORDS >> donor) & 1) == 1).astype(np.uint8)
    blank_columns = np.flatnonzero(((WORDS >> target) & 1) == 0).astype(np.uint16)
    spent_rows = loaded_rows ^ np.uint8(1 << donor)
    occupied_columns = blank_columns ^ np.uint16(1 << target)
    ready_blank = state[np.ix_(loaded_rows, blank_columns)]
    spent_occupied = state[np.ix_(spent_rows, occupied_columns)]
    cosine = math.cos(PHI)
    sine = math.sin(PHI)
    out[np.ix_(loaded_rows, blank_columns)] = cosine * ready_blank - 1j * sine * spent_occupied
    out[np.ix_(spent_rows, occupied_columns)] = cosine * spent_occupied - 1j * sine * ready_blank
    return out


def blocked_null_error(state: np.ndarray, donor: int, target: int) -> float:
    loaded = ((DONOR_WORDS >> donor) & 1) == 1
    occupied = ((WORDS >> target) & 1) == 1
    projected = np.zeros_like(state)
    projected[np.ix_(loaded, occupied)] = state[np.ix_(loaded, occupied)]
    return float(np.linalg.norm(apply_admission(projected, donor, target) - projected))


def h_action(state: np.ndarray) -> np.ndarray:
    out = np.zeros_like(state)
    for active, mask, _ in ACTIONS:
        out[:, active] -= state[:, active ^ mask]
    return out


def currents(state: np.ndarray) -> np.ndarray:
    answer = np.empty(len(ACTIONS), dtype=float)
    for index, (active, mask, sign) in enumerate(ACTIONS):
        answer[index] = float(np.sum(
            np.conjugate(state[:, active])
            * (1j * sign[np.newaxis, :])
            * state[:, active ^ mask]
        ).real)
    return answer


def taylor_step(state: np.ndarray, step: float) -> np.ndarray:
    updated = state.copy()
    term = state.copy()
    for order in range(1, TAYLOR_ORDER + 1):
        term = (-1j * step / order) * h_action(term)
        updated += term
    return updated


def transport(state: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    step = KAPPA / TRANSPORT_STEPS
    current_integral = currents(state)
    evolved = state.copy()
    for index in range(1, TRANSPORT_STEPS + 1):
        evolved = taylor_step(evolved, step)
        weight = 1 if index == TRANSPORT_STEPS else (4 if index % 2 else 2)
        current_integral += weight * currents(evolved)
    current_integral *= step / 3.0
    return evolved, current_integral


def run() -> dict[str, object]:
    started = time.perf_counter()
    state = initial_state()
    rows: list[dict[str, object]] = []
    for event, target in enumerate(TARGETS, start=1):
        donor = event - 1
        before = state
        allow, blocked, reverse = allow_and_blocked(before, donor, target)
        null_error = blocked_null_error(before, donor, target)
        q_before = retained_q(before)
        g_before = genesis_q(before)
        b_before = g_before
        lineage_before = DONORS - g_before
        target_occ_before = occupations(before)[target]
        donor_before = donor_loaded_probability(before, donor)

        admitted = apply_admission(before, donor, target)
        q_admitted = retained_q(admitted)
        g_admitted = genesis_q(admitted)
        b_admitted = g_admitted
        lineage_admitted = DONORS - g_admitted
        target_occ_admitted = occupations(admitted)[target]
        donor_admitted = donor_loaded_probability(admitted, donor)
        write = q_admitted - q_before

        transported, integrated_current = transport(admitted)
        occupation_admitted = occupations(admitted)
        occupation_after = occupations(transported)
        transport_residual = occupation_after - occupation_admitted + INCIDENCE @ integrated_current
        q_after = retained_q(transported)
        g_after = genesis_q(transported)

        accounting = {
            "total_content_residual": (q_admitted - q_before) + (g_admitted - g_before),
            "bandwidth_cost_residual": (b_admitted - b_before) + write,
            "lineage_cost_residual": (lineage_admitted - lineage_before) - write,
            "target_owner_residual": (target_occ_admitted - target_occ_before) - write,
            "donor_owner_residual": (donor_admitted - donor_before) + write,
        }
        rows.append({
            "event": event,
            "cursor_vertex": target,
            "genesis_cell": donor,
            "allow_probability": allow,
            "blocked_probability": blocked,
            "reverse_support_probability": reverse,
            "blocked_null_state_error": null_error,
            "W_n": write,
            "expected_W_from_allow": (math.sin(PHI) ** 2) * allow,
            "q_retained_before": q_before,
            "q_retained_after_admission": q_admitted,
            "q_retained_after_transport": q_after,
            "q_genesis_before": g_before,
            "q_genesis_after": g_after,
            "bandwidth_before": b_before,
            "bandwidth_after": b_admitted,
            "lineage_sealed_before": lineage_before,
            "lineage_sealed_after": lineage_admitted,
            "admission_accounting": accounting,
            "transport_node_residual_l1": float(np.sum(np.abs(transport_residual))),
            "transport_node_residual_linf": float(np.max(np.abs(transport_residual))),
            "transport_number_drift": abs(q_after - q_admitted),
            "transport_genesis_drift": abs(g_after - g_admitted),
            "norm_error_after_admission": abs(norm(admitted) - 1.0),
            "norm_error_after_transport": abs(norm(transported) - 1.0),
            "retained_density_after_transport": q_after / SITES,
            "integrated_edge_currents": integrated_current.tolist(),
        })
        state = transported

    max_accounting = max(
        abs(float(value))
        for row in rows
        for value in row["admission_accounting"].values()
    )
    checks = {
        "owner_edge_census_12": len(EDGE_LIST) == 12,
        "incidence_columns_telescope": bool(np.all(np.sum(INCIDENCE, axis=0) == 0)),
        "all_writes_nonnegative": min(float(row["W_n"]) for row in rows) >= -1.0e-12,
        "blocked_attempts_exactly_null": max(float(row["blocked_null_state_error"]) for row in rows) <= 1.0e-12,
        "fresh_cells_have_no_reverse_support": max(float(row["reverse_support_probability"]) for row in rows) <= 1.0e-12,
        "admission_accounting_closes": max_accounting <= 1.0e-12,
        "transport_ledger_closes": max(float(row["transport_node_residual_l1"]) for row in rows) <= 1.0e-9,
        "norms_close": max(float(row["norm_error_after_transport"]) for row in rows) <= 1.0e-10,
        "transport_number_closes": max(float(row["transport_number_drift"]) for row in rows) <= 1.0e-10,
        "nonvacuous_dynamic_blocking": max(float(row["blocked_probability"]) for row in rows) > 1.0e-6,
    }
    classification = (
        "PASS_L4_INTRINSIC_ADMISSION__COHERENT_UNWRITING_ELIMINATED_ON_DECLARED_TRACE"
        if all(checks.values())
        else "FAIL_CLOSED_L4_INTRINSIC_ADMISSION_TRACE"
    )
    return {
        "schema": "INTRINSIC_ADMISSION_PARENT_L4_TRACE_V001",
        "classification": classification,
        "L": LENGTH,
        "retained_sites": SITES,
        "reachable_dimension": (1 << SITES) * (1 << DONORS),
        "genesis_cluster_size": DONORS,
        "cursor_path_prefix": list(TARGETS),
        "phi": "pi/4",
        "kappa": "pi/2",
        "transport_steps": TRANSPORT_STEPS,
        "taylor_order": TAYLOR_ORDER,
        "rows": rows,
        "checks": checks,
        "checks_passed": sum(bool(value) for value in checks.values()),
        "checks_total": len(checks),
        "maximum_admission_accounting_residual": max_accounting,
        "final_retained_q": retained_q(state),
        "final_genesis_q": genesis_q(state),
        "final_total_q": retained_q(state) + genesis_q(state),
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "protocol_sha256": sha256(HERE / "PROTOCOL.md"),
        "implementation_sha256": sha256(Path(__file__)),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "claim_boundary": {
            "proved_if_pass": "FINITE_L4_ONE_PASS_INTRINSIC_ADMISSION_NULLS_BLOCKED_COMPONENTS_AND_HAS_NO_NEGATIVE_W",
            "not_claimed": [
                "GENERIC_MONOTONE_ACCUMULATION",
                "BACKGROUND_INDEPENDENCE_THEOREM",
                "COMMON_ACCUMULATION_SECTOR",
                "Z_EQUALS_ONE",
                "CONTINUUM",
                "EMERGENCE",
                "GRAVITY",
            ],
        },
    }


if __name__ == "__main__":
    result = run()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["classification"])
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    for row in result["rows"]:
        print(
            f"n={row['event']} v={row['cursor_vertex']} "
            f"allow={row['allow_probability']:.12g} "
            f"blocked={row['blocked_probability']:.12g} W={row['W_n']:.12g}"
        )
    if not all(result["checks"].values()):
        raise SystemExit(1)
