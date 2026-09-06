#!/usr/bin/env python3
"""Guarded fixed-width L14 connected BS09 accumulation on the same finite slice."""

from __future__ import annotations

import json
import math
import os
import resource
import sys
import time
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from numba import get_num_threads, njit, prange


LENGTH = 14
SITES = 2 * LENGTH
FULL_DIMENSION = 1 << SITES
ORBIT_DIMENSION = 9_608_050
COMPONENTS = LENGTH * LENGTH // 2
KAPPA = math.pi / 2.0
TAYLOR_ORDER = 10
COARSE_STEPS = 512
FINE_STEPS = 1024
GUARD_BYTES = 40 * (1 << 30)
ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).with_name("RESULT.json")
STARTED = time.perf_counter()

# Importing the hostile-audited engine intentionally replays its canonical
# L4/L6/L8/L10 40/40 suite before exposing the implementation functions.
sys.path.insert(0, str(ROOT))
from DEVELOPMENT_R_CONNECTED_FIXED_WIDTH_ENGINE_V001 import validate_engine as engine  # noqa: E402


@njit
def count_unassigned(values):
    count = 0
    for value in values:
        if value < 0:
            count += 1
    return count


@njit(parallel=True)
def h_apply_into(x, out, offsets, destinations, coefficients):
    # The hostile-audited unaggregated quotient is real symmetric after row
    # aggregation.  Reading each stored source row as its equal destination
    # row removes scatter races and preserves each row's fixed summation order.
    for row in prange(x.size):
        value = 0.0j
        for cursor in range(offsets[row], offsets[row + 1]):
            value += coefficients[cursor] * x[destinations[cursor]]
        out[row] = value


@njit(parallel=True)
def representative_current_rows(
    x,
    offsets,
    destinations,
    coefficients,
    current_codes,
    internal_rows,
    connector_rows,
):
    for source in prange(x.size):
        source_value = x[source]
        internal_row = 0.0
        connector_row = 0.0
        for cursor in range(offsets[source], offsets[source + 1]):
            code = current_codes[cursor]
            sign = code if abs(code) == 1 else code // 2
            contribution = (
                np.conjugate(x[destinations[cursor]])
                * (1.0j * sign * coefficients[cursor])
                * source_value
            ).real
            if abs(code) == 1:
                internal_row += contribution
            else:
                connector_row += contribution
        internal_rows[source] = internal_row
        connector_rows[source] = connector_row


def rss_bytes():
    observed = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(observed if sys.platform == "darwin" else observed * 1024)


def phase(label, extra=None):
    payload = {
        "phase": label,
        "elapsed_seconds": time.perf_counter() - STARTED,
        "max_rss_bytes": rss_bytes(),
    }
    if extra:
        payload.update(extra)
    print("PHASE__" + json.dumps(payload, sort_keys=True), flush=True)


def guard_allocation(label, requested_bytes):
    observed = rss_bytes()
    if observed + requested_bytes >= GUARD_BYTES:
        raise MemoryError(
            f"{label}: observed RSS plus requested fixed-width bytes reaches the 40 GiB guard"
        )


phase("LOWER_SIZE_ENGINE_REPLAY_COMPLETE")
group = engine.prism_group(LENGTH)
edges = engine.edges_for(LENGTH)
edge_set = {frozenset((u, v)) for u, v, _ in edges}
if len(group) != 2 * LENGTH or len(set(group)) != 2 * LENGTH:
    raise AssertionError("L14 finite group is not faithful")
if any({frozenset((p[u], p[v])) for u, v, _ in edges} != edge_set for p in group):
    raise AssertionError("L14 group does not preserve support")
if any(p[site] % 2 != site % 2 for p in group for site in range(SITES)):
    raise AssertionError("L14 group does not preserve source parity")
edge_representatives, reconstruction = engine.edge_reconstruction(edges, group)
if len(edge_representatives) != 2:
    raise AssertionError("L14 signed edge orbit count differs")
site_images = [{p[site] for p in group} for site in range(SITES)]
if any(site_images[site] != set(range(site % 2, SITES, 2)) for site in range(SITES)):
    raise AssertionError("L14 parity site orbits are not transitive")
if engine.burnside_dimension(group) != ORBIT_DIMENSION:
    raise AssertionError("L14 Burnside dimension differs from audited screen")

low_table, high_table = engine.chunk_tables(group, LENGTH)
orbit_bytes = 4 * FULL_DIMENSION + 4 * ORBIT_DIMENSION + ORBIT_DIMENSION
guard_allocation("orbit arrays", orbit_bytes)
orbit_ids = np.full(FULL_DIMENSION, -1, np.int32)
representatives = np.empty(ORBIT_DIMENSION, np.uint32)
sizes = np.empty(ORBIT_DIMENSION, np.uint8)
observed_orbits = engine.build_orbits(
    orbit_ids,
    representatives,
    sizes,
    low_table,
    high_table,
    (1 << LENGTH) - 1,
    LENGTH,
)
if observed_orbits != ORBIT_DIMENSION:
    raise AssertionError("compiled orbit count differs from Burnside count")
if count_unassigned(orbit_ids) != 0:
    raise AssertionError("word orbit map is incomplete")
unique_sizes, size_counts = np.unique(sizes, return_counts=True)
orbit_histogram = {str(int(key)): int(value) for key, value in zip(unique_sizes, size_counts)}
if int(np.dot(unique_sizes.astype(np.int64), size_counts)) != FULL_DIMENSION:
    raise AssertionError("orbit-size census does not cover full word space")
del low_table, high_table
phase("ORBIT_PARTITION_COMPLETE", {"orbit_dimension": ORBIT_DIMENSION, "orbit_histogram": orbit_histogram})

edge_u = np.array([u for u, _, _ in edges], np.uint8)
edge_v = np.array([v for _, v, _ in edges], np.uint8)
edge_kind = np.array([kind for _, _, kind in edges], np.uint8)
edge_codes = np.array([(representative + 1) * sign for representative, sign in reconstruction], np.int8)
guard_allocation("transition row offsets", 8 * (ORBIT_DIMENSION + 1))
offsets = engine.count_transitions(representatives, edge_u, edge_v)
transition_entries = int(offsets[-1])
transition_array_bytes = transition_entries * (4 + 8 + 1)
guard_allocation("transition arrays", transition_array_bytes)
destinations, coefficients, current_codes = engine.fill_transitions(
    representatives, sizes, orbit_ids, offsets, edge_u, edge_v, edge_codes
)
transition_payload_bytes = int(
    offsets.nbytes + destinations.nbytes + coefficients.nbytes + current_codes.nbytes
)
del orbit_ids
phase(
    "TRANSITION_BUILD_COMPLETE",
    {
        "unaggregated_transition_entries": transition_entries,
        "transition_payload_bytes": transition_payload_bytes,
    },
)

even_mask = sum(1 << site for site in range(0, SITES, 2))
psi0 = np.zeros(ORBIT_DIMENSION, np.complex128)
valid_source_orbits = (representatives & even_mask) == 0
psi0[valid_source_orbits] = (
    np.sqrt(sizes[valid_source_orbits].astype(np.float64)) / math.sqrt(1 << LENGTH)
)
del sizes
current_internal_rows = np.empty(ORBIT_DIMENSION, np.float64)
current_connector_rows = np.empty(ORBIT_DIMENSION, np.float64)


def H(x):
    out = np.empty_like(x)
    h_apply_into(x, out, offsets, destinations, coefficients)
    return out


def currents(x):
    representative_current_rows(
        x,
        offsets,
        destinations,
        coefficients,
        current_codes,
        current_internal_rows,
        current_connector_rows,
    )
    internal = float(np.sum(current_internal_rows)) / (2 * LENGTH)
    connector = float(np.sum(current_connector_rows)) / LENGTH
    representative_values = (internal, connector)
    return np.array(
        [sign * representative_values[representative] for representative, sign in reconstruction]
    )


guard_allocation("state work vectors", 6 * ORBIT_DIMENSION * 16)
benchmark_started = time.perf_counter()
hpsi0 = H(psi0)
# The first call includes compilation. Time a warmed action separately.
benchmark_started = time.perf_counter()
hpsi0_warm = H(psi0)
h_action_seconds = time.perf_counter() - benchmark_started
probe = psi0 + 0.125j * hpsi0
probe_gather = H(probe)
probe_scatter = engine.h_apply(probe, offsets, destinations, coefficients)
gather_scatter_linf = float(np.max(np.abs(probe_gather - probe_scatter)))
audit_current_probe = engine.representative_currents(
    probe, offsets, destinations, coefficients, current_codes, 2 * LENGTH, LENGTH
)
trial_current_probe = currents(probe)
# Reconstructed current arrays contain signs for all 42 edges. Compare the
# two representative entries with the serial audited operator calculation.
trial_current_probe = (trial_current_probe[edge_representatives[0]], trial_current_probe[edge_representatives[1]])
parallel_current_crosscheck_linf = float(
    np.max(np.abs(np.array(trial_current_probe) - np.array(audit_current_probe)))
)
source_norm_error = float(abs(np.vdot(psi0, psi0).real - 1.0))
source_energy_imag = float(abs(np.vdot(psi0, hpsi0).imag))
source_currents_linf = float(np.max(np.abs(currents(psi0))))
if float(np.max(np.abs(hpsi0 - hpsi0_warm))) != 0.0:
    raise AssertionError("warmed gather action differs")
phase(
    "STRUCTURAL_ACTION_SCREEN_COMPLETE",
    {
        "h_action_seconds": h_action_seconds,
        "source_norm_error": source_norm_error,
        "source_energy_imag": source_energy_imag,
        "source_currents_linf": source_currents_linf,
        "gather_scatter_linf": gather_scatter_linf,
        "parallel_current_crosscheck_linf": parallel_current_crosscheck_linf,
        "numba_threads": get_num_threads(),
    },
)

if os.environ.get("STRUCTURE_ONLY") == "1":
    print("PASS__R_CONNECTED_L14_STRUCTURE_TRIAL__NO_EVOLUTION", flush=True)
    print(f"OBSERVED_RUNTIME_SECONDS={time.perf_counter() - STARTED:.9f}", flush=True)
    print(f"OBSERVED_MAX_RSS_BYTES={rss_bytes()}", flush=True)
    raise SystemExit(0)


def evolve(step_count, label):
    step = KAPPA / step_count
    psi = psi0.copy()
    out = np.empty_like(psi)
    term = np.empty_like(psi)
    work = np.empty_like(psi)
    integrated = currents(psi)
    for index in range(1, step_count + 1):
        np.copyto(out, psi)
        np.copyto(term, psi)
        for order in range(1, TAYLOR_ORDER + 1):
            h_apply_into(term, work, offsets, destinations, coefficients)
            work *= -1.0j * step / order
            out += work
            term, work = work, term
        psi, out = out, psi
        weight = 1.0 if index == step_count else (4.0 if index % 2 else 2.0)
        integrated += weight * currents(psi)
        if index % 64 == 0 or index == step_count:
            phase(f"{label}_PROGRESS", {"step": index, "steps": step_count})
    return psi.copy(), integrated * step / 3.0


psi_coarse, currents_coarse = evolve(COARSE_STEPS, "COARSE")
psi, integrated_currents = evolve(FINE_STEPS, "FINE")
state_refinement_linf = float(np.max(np.abs(psi - psi_coarse)))
current_refinement_linf = float(np.max(np.abs(integrated_currents - currents_coarse)))

q_even, q_odd, both_internal, both_connector, number_law = engine.diagonal_data(
    psi, representatives, even_mask, edge_u, edge_v, edge_kind, LENGTH
)
q_even_coarse, q_odd_coarse, _, _, _ = engine.diagonal_data(
    psi_coarse, representatives, even_mask, edge_u, edge_v, edge_kind, LENGTH
)
q0_even, q0_odd, _, _, number_law0 = engine.diagonal_data(
    psi0, representatives, even_mask, edge_u, edge_v, edge_kind, LENGTH
)
q1 = np.array([q_even if site % 2 == 0 else q_odd for site in range(SITES)])
q1_coarse = np.array(
    [q_even_coarse if site % 2 == 0 else q_odd_coarse for site in range(SITES)]
)
q0 = np.array([q0_even if site % 2 == 0 else q0_odd for site in range(SITES)])
occupation_refinement_linf = float(np.max(np.abs(q1 - q1_coarse)))

incidence = np.zeros((SITES, len(edges)))
for edge_index, (u, v, _) in enumerate(edges):
    incidence[u, edge_index] = 1.0
    incidence[v, edge_index] = -1.0
if not np.all(np.isfinite(integrated_currents)) or not np.all(np.isfinite(currents_coarse)):
    raise AssertionError("integrated currents are not finite")
# Use the explicit owner-edge sum here.  The first completed evolution attempt
# failed closed when Accelerate surfaced a stale floating-status warning in the
# equivalent tiny matrix product under PYTHONWARNINGS=error.
balance = np.zeros(SITES)
balance_coarse = np.zeros(SITES)
for edge_index, (u, v, _) in enumerate(edges):
    balance[u] += integrated_currents[edge_index]
    balance[v] -= integrated_currents[edge_index]
    balance_coarse[u] += currents_coarse[edge_index]
    balance_coarse[v] -= currents_coarse[edge_index]
residual = q1 - q0 + balance
residual_coarse = q1_coarse - q0 + balance_coarse
correlations = np.array([
    both_internal - q1[u] * q1[v] if kind == 0 else both_connector - q1[u] * q1[v]
    for u, v, kind in edges
])
kinds = np.array([kind for _, _, kind in edges])
connector_mask = kinds == 1
internal_mask = ~connector_mask
throughput_component = float(np.sum(np.abs(integrated_currents)))
connector_throughput_component = float(np.sum(np.abs(integrated_currents[connector_mask])))
this_global = COMPONENTS * throughput_component
hpsi = H(psi)


def lower_result(length):
    if length == 4:
        packet = json.loads(
            (ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001" / "RESULT.json").read_text()
        )
        return next(row for row in packet["rows"] if row["kappa"] == KAPPA)
    return json.loads(
        (ROOT / f"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L{length}_ACCUMULATION_V001" / "RESULT.json").read_text()
    )


comparators = {}
for length, retained in ((4, 16.0), (6, 54.0), (8, 128.0), (10, 250.0), (12, 432.0)):
    lower = lower_result(length)
    lower_global = lower["absolute_oriented_throughput_global"]
    lower_connector_global = lower["absolute_connector_throughput_global"]
    comparators[f"L14_over_L{length}"] = {
        "throughput_total": this_global / lower_global,
        "throughput_per_retained_record": (this_global / 686.0) / (lower_global / retained),
        "connector_throughput": (COMPONENTS * connector_throughput_component) / lower_connector_global,
        "connector_throughput_per_retained_record":
            ((COMPONENTS * connector_throughput_component) / 686.0)
            / (lower_connector_global / retained),
    }

sites_per_layer = COMPONENTS * LENGTH
census = {
    "L": LENGTH,
    "sites_global": COMPONENTS * SITES,
    "sites_per_F3_layer": sites_per_layer,
    "possible_F3_links": sites_per_layer * sites_per_layer,
    "components": COMPONENTS,
    "sites_per_component": SITES,
    "internal_edges_per_component": 2 * LENGTH,
    "connector_edges_per_component": LENGTH,
    "selected_edges_global_owner_once": COMPONENTS * len(edges),
    "prepared_source_lineages": sites_per_layer,
    "expected_retained_global": sites_per_layer // 2,
}
checks = [
    (FULL_DIMENSION == 268435456 and ORBIT_DIMENSION == 9608050, "basis census"),
    (len(group) == 28 and sum(int(key) * value for key, value in orbit_histogram.items()) == FULL_DIMENSION, "group orbit census"),
    (transition_entries <= ORBIT_DIMENSION * len(edges), "unaggregated transition ceiling"),
    (len(edge_representatives) == 2, "signed edge orbit census"),
    (len(edges) == 42 and np.sum(connector_mask) == 14, "component edge census"),
    (census["sites_global"] == 2744 and census["selected_edges_global_owner_once"] == 4116, "global site/edge census"),
    (source_norm_error < 2.0e-12 and source_energy_imag < 2.0e-12, "source normalization"),
    (source_currents_linf < 2.0e-12, "source currents"),
    (gather_scatter_linf < 2.0e-12, "gather/scatter action crosscheck"),
    (parallel_current_crosscheck_linf < 2.0e-12, "parallel/serial current crosscheck"),
    (int(np.sum(np.abs(integrated_currents[internal_mask]) > 1.0e-10)) == 28, "all internal currents active"),
    (int(np.sum(np.abs(integrated_currents[connector_mask]) > 1.0e-10)) == 14, "all connector currents active"),
    (connector_throughput_component > 1.0e-6, "nonzero connector throughput"),
    (abs(COMPONENTS * np.sum(q1) - 686.0) < 2.0e-7, "global retained total"),
    (state_refinement_linf < 3.0e-8, "state refinement"),
    (occupation_refinement_linf < 3.0e-8, "occupation refinement"),
    (current_refinement_linf < 3.0e-8, "current refinement"),
    (float(np.sum(np.abs(residual))) < 1.5e-8, "fine ledger L1"),
    (float(np.max(np.abs(residual))) < 1.5e-9, "fine ledger Linf"),
    (float(np.sum(np.abs(residual))) <= float(np.sum(np.abs(residual_coarse))) + 6.0e-10, "ledger refinement nonworsening"),
    (abs(np.vdot(psi, psi).real - 1.0) < 1.5e-8, "norm"),
    (abs(np.vdot(psi, hpsi).real - np.vdot(psi0, hpsi0).real) < 1.5e-7, "energy"),
    (abs(np.vdot(psi, hpsi).imag) < 1.5e-8, "energy reality"),
    (float(np.max(np.abs(number_law - number_law0))) < 1.5e-8, "number law"),
    (all(item["throughput_total"] > 0 for item in comparators.values()), "total comparators"),
    (all(item["throughput_per_retained_record"] > 0 for item in comparators.values()), "per-retained comparators"),
    (all(item["connector_throughput_per_retained_record"] > 0 for item in comparators.values()), "connector comparators"),
    (rss_bytes() < GUARD_BYTES, "resource guard"),
]
failures = [label for passed, label in checks if not passed]
out = {
    "schema": "R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION_V001",
    "classification": "CONDITIONAL_CONNECTED_SUPPORT__UNIFORM_F3_MDC_SOURCE__AUTONOMOUS_SIMULTANEOUS_BS09__EXACT_ORDER_2L_FIXED_WIDTH_FINITE_ORBIT_BASIS__REFINED_NUMERICAL_CURRENT_INTEGRATION",
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
    "census": census,
    "finite_orbit_basis": {
        "full_dimension": FULL_DIMENSION,
        "finite_group_order": len(group),
        "orbit_dimension": ORBIT_DIMENSION,
        "orbit_size_histogram": orbit_histogram,
        "unaggregated_transition_entries": transition_entries,
        "transition_payload_bytes": transition_payload_bytes,
        "signed_edge_orbits": len(edge_representatives),
        "storage_status": "FIXED_WIDTH_OWNER_ONCE_TRANSITIONS__REPEATED_DESTINATIONS_NOT_AGGREGATED",
    },
    "parameters": {
        "kappa": KAPPA,
        "taylor_order": TAYLOR_ORDER,
        "coarse_steps": COARSE_STEPS,
        "fine_steps": FINE_STEPS,
    },
    "q_before": q0.tolist(),
    "q_after": q1.tolist(),
    "integrated_oriented_currents": integrated_currents.tolist(),
    "active_internal_supports_per_component": int(np.sum(np.abs(integrated_currents[internal_mask]) > 1.0e-10)),
    "active_connector_supports_per_component": int(np.sum(np.abs(integrated_currents[connector_mask]) > 1.0e-10)),
    "absolute_oriented_throughput_per_component": throughput_component,
    "absolute_oriented_throughput_global": this_global,
    "absolute_connector_throughput_per_component": connector_throughput_component,
    "absolute_connector_throughput_global": COMPONENTS * connector_throughput_component,
    "expected_retained_per_component": float(np.sum(q1)),
    "expected_retained_global": float(COMPONENTS * np.sum(q1)),
    "max_abs_connected_edge_correlation": float(np.max(np.abs(correlations))),
    "record_ledger_residual_l1_per_component": float(np.sum(np.abs(residual))),
    "record_ledger_residual_linf_per_component": float(np.max(np.abs(residual))),
    "record_ledger_residual_l1_global_bound": float(COMPONENTS * np.sum(np.abs(residual))),
    "coarse_record_ledger_residual_l1_per_component": float(np.sum(np.abs(residual_coarse))),
    "state_refinement_linf": state_refinement_linf,
    "occupation_refinement_linf": occupation_refinement_linf,
    "current_refinement_linf": current_refinement_linf,
    "norm_error": float(abs(np.vdot(psi, psi).real - 1.0)),
    "energy_error": float(abs(np.vdot(psi, hpsi).real - np.vdot(psi0, hpsi0).real)),
    "energy_imag_abs": float(abs(np.vdot(psi, hpsi).imag)),
    "number_law_max_change": float(np.max(np.abs(number_law - number_law0))),
    "gather_scatter_linf": gather_scatter_linf,
    "parallel_current_crosscheck_linf": parallel_current_crosscheck_linf,
    "comparators": comparators,
    "owner_once_action": "H_EQUALS_MINUS_T_SUM_OVER_4116_UNIQUE_EDGES_T_E__98_IDENTICAL_CONNECTED_COMPONENTS",
    "ctp_bookkeeping": "ONE_DEFORMATION_SOURCE_PER_UNIQUE_EDGE__Z_0_0_EQUALS_ONE",
    "support_status": "CONDITIONAL_FIXED_CONNECTED_PROGRAM__NOT_AUTONOMOUSLY_SELECTED",
    "source_status": "UNIFORM_RIGHT_HEADS_AND_BLANK_LEFT_TAILS__NO_EXTRA_ROUTING_ASYMMETRY",
    "parameter_status": "KAPPA_EQUALS_PI_OVER_TWO_IS_CONDITIONAL__T_AND_TAU_NOT_SELECTED",
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_RECORD_LEDGER_RESIDUALS__NOT_CALLED_DEFECTS",
    "not_claimed": "EXACT_TIME_EVOLUTION__EXACT_CURRENT_QUADRATURE__MONOTONICITY__CONVERGENCE__LIMIT__FIT__SCALING_LAW__GENERIC_CONNECTED_PHASE__GRID__CONTINUUM__WARD__GRAVITY",
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
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 4.0e-9:
            raise AssertionError(f"canonical float differs at {path}")
    elif observed != canonical:
        raise AssertionError(f"canonical value differs at {path}")


if OUT.exists():
    compatible(out, json.loads(OUT.read_text()))
else:
    print("RESULT_JSON_BEGIN")
    print(json.dumps(out, indent=2, sort_keys=True))
    print("RESULT_JSON_END")
if failures:
    raise AssertionError(failures)
print(f"PASS__R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION__{len(checks)}/{len(checks)}")
print(f"OBSERVED_RUNTIME_SECONDS={time.perf_counter() - STARTED:.9f}")
print(f"OBSERVED_MAX_RSS_BYTES={rss_bytes()}")
