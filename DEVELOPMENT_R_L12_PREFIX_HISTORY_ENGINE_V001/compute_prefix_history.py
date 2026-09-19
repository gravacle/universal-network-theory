#!/usr/bin/env python3
"""Exact owner-once prefix allocation with the sealed target carrier solver."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import resource
import sys
import time
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE_DIR = ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
sys.path.insert(0, str(BASE_DIR))
import compute_streamed_history as sealed  # noqa: E402


SUPPORTED = (4, 6, 8, 10)
SEALED_BATCH_BYTES = 1_000_000_000
RSS_LIMIT = 4 * 2**30
WALL_LIMIT = 2 * 3600.0


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PrefixParent:
    def __init__(self, length: int):
        self.length = length
        self.sites = 2 * length
        self.edges = sealed.graph(length)
        self.connector_indices = [index for index, edge in enumerate(self.edges)
                                  if edge[2] == "connector"]
        self.incidence = np.zeros((self.sites, len(self.edges)), dtype=np.int8)
        for edge_index, (u, v, _) in enumerate(self.edges):
            self.incidence[u, edge_index] = 1
            self.incidence[v, edge_index] = -1
        self.sectors = [sealed.Sector(length, q, self.edges) for q in range(length + 1)]
        self.lineage_words = {}
        self.lineage_lookup = {}

    def rows(self, prefix: int, q: int) -> np.ndarray:
        key = (prefix, q)
        if key not in self.lineage_words:
            self.lineage_words[key] = sealed.fixed_words(prefix, q)
            self.lineage_lookup[key] = {
                int(word): index for index, word in enumerate(self.lineage_words[key])
            }
        return self.lineage_words[key]

    def blank(self):
        return [np.ones((1, 1), dtype=np.complex128)]

    @staticmethod
    def copy(state):
        return [block.copy() for block in state]

    @staticmethod
    def norm(state) -> float:
        return float(sum(np.vdot(block, block).real for block in state))

    def weights(self, state) -> np.ndarray:
        result = np.zeros(self.length + 1)
        for q, block in enumerate(state):
            result[q] = float(np.vdot(block, block).real)
        return result

    def retained(self, state) -> float:
        return float(np.dot(np.arange(self.length + 1), self.weights(state)))

    def remaining(self, state) -> float:
        return float(self.length - self.retained(state))

    def occupations(self, state) -> np.ndarray:
        answer = np.zeros(self.sites)
        for q, block in enumerate(state):
            if q == 0:
                continue
            probability = np.sum(np.abs(block) ** 2, axis=0)
            words = self.sectors[q].words
            for site in range(self.sites):
                answer[site] += float(np.sum(probability[((words >> site) & 1) == 1]))
        return answer

    def predicates(self, state, event: int):
        allow = blocked = reverse = 0.0
        for q, block in enumerate(state):
            lineages = self.rows(event, q)
            carriers = self.sectors[q].words
            loaded_rows = np.flatnonzero(((lineages >> event) & 1) == 0)
            spent_rows = np.flatnonzero(((lineages >> event) & 1) == 1)
            blank = np.flatnonzero(((carriers >> event) & 1) == 0)
            occupied = np.flatnonzero(((carriers >> event) & 1) == 1)
            if len(loaded_rows) and len(blank):
                view = block[np.ix_(loaded_rows, blank)]
                allow += float(np.vdot(view, view).real)
            if len(loaded_rows) and len(occupied):
                view = block[np.ix_(loaded_rows, occupied)]
                blocked += float(np.vdot(view, view).real)
            if len(spent_rows) and len(occupied):
                view = block[np.ix_(spent_rows, occupied)]
                reverse += float(np.vdot(view, view).real)
        return allow, blocked, reverse

    def admit(self, state, event: int):
        new_prefix = event + 1
        result = [
            np.zeros((len(self.rows(new_prefix, q)), len(self.sectors[q].words)),
                     dtype=np.complex128)
            for q in range(new_prefix + 1)
        ]
        cosine = math.cos(sealed.PHI)
        sine = math.sin(sealed.PHI)
        for q, old in enumerate(state):
            old_lineages = self.rows(event, q)
            stay_rows = np.fromiter(
                (self.lineage_lookup[(new_prefix, q)][int(word)] for word in old_lineages),
                dtype=np.int32, count=len(old_lineages),
            )
            result[q][stay_rows, :] = old
            blank = np.flatnonzero(((self.sectors[q].words >> event) & 1) == 0).astype(np.int32)
            if len(blank):
                result[q][np.ix_(stay_rows, blank)] *= cosine
                accepted_rows = np.fromiter(
                    (self.lineage_lookup[(new_prefix, q + 1)][int(word) | (1 << event)]
                     for word in old_lineages),
                    dtype=np.int32, count=len(old_lineages),
                )
                accepted_columns = np.fromiter(
                    (self.sectors[q + 1].lookup[int(self.sectors[q].words[column]) | (1 << event)]
                     for column in blank),
                    dtype=np.int32, count=len(blank),
                )
                result[q + 1][np.ix_(accepted_rows, accepted_columns)] = -1.0j * sine * old[:, blank]
        return result


def route(parent: PrefixParent, state, resolution):
    total = np.zeros(len(parent.edges))
    summary = {
        "converged": True,
        "batches": 0,
        "maximum_krylov_steps": 0,
        "maximum_exp_difference": 0.0,
        "maximum_residual_indicator": 0.0,
        "quadrature_nodes": resolution.quadrature_nodes,
    }
    for q, block in enumerate(state):
        columns = block.shape[1]
        maximum = max(resolution.checkpoints)
        rows_per_batch = max(1, int(SEALED_BATCH_BYTES // (maximum * columns * 16)))
        rows_per_batch = min(rows_per_batch, block.shape[0])
        for lower in range(0, block.shape[0], rows_per_batch):
            upper = min(block.shape[0], lower + rows_per_batch)
            evolved, current, record = sealed.propagate_batch(
                parent.sectors[q], block[lower:upper], resolution
            )
            block[lower:upper] = evolved
            total += current
            summary["converged"] = summary["converged"] and bool(record["converged"])
            summary["batches"] += 1
            summary["maximum_krylov_steps"] = max(
                summary["maximum_krylov_steps"], int(record["steps"])
            )
            if math.isfinite(float(record["exp_difference"])):
                summary["maximum_exp_difference"] = max(
                    summary["maximum_exp_difference"], float(record["exp_difference"])
                )
            summary["maximum_residual_indicator"] = max(
                summary["maximum_residual_indicator"], float(record["residual_indicator"])
            )
    return total, summary


def history(length: int, resolution):
    parent = PrefixParent(length)
    state = parent.blank()
    rows = []
    for event in range(length):
        before = state
        allow, blocked, reverse = parent.predicates(before, event)
        q_before = parent.retained(before)
        g_before = parent.remaining(before)
        occupation_before = parent.occupations(before)
        admitted = parent.admit(before, event)
        q_admitted = parent.retained(admitted)
        g_admitted = parent.remaining(admitted)
        occupation_admitted = parent.occupations(admitted)
        write = q_admitted - q_before
        actual_current, actual_solver = route(parent, admitted, resolution)
        null_current, null_solver = route(parent, before, resolution)
        occupation_after = parent.occupations(admitted)
        q_after = parent.retained(admitted)
        delta = actual_current - null_current
        transport_residual = occupation_after - occupation_admitted + parent.incidence @ actual_current
        rows.append({
            "event": event + 1,
            "cursor_vertex": event,
            "allow_probability": allow,
            "blocked_probability": blocked,
            "reverse_support_probability": reverse,
            "blocked_null_state_error": 0.0,
            "W_n": write,
            "expected_W_from_allow": (math.sin(sealed.PHI) ** 2) * allow,
            "q_retained_before": q_before,
            "q_retained_after_admission": q_admitted,
            "q_retained_after_transport": q_after,
            "q_genesis_before": g_before,
            "q_genesis_after": parent.remaining(admitted),
            "bandwidth_after": g_admitted,
            "lineage_sealed_after": length - g_admitted,
            "sector_weights": parent.weights(admitted).tolist(),
            "connector_delta_l1": float(np.sum(np.abs(delta[parent.connector_indices]))),
            "connector_delta_signed": float(np.sum(delta[parent.connector_indices])),
            "admission_total_content_residual": (q_admitted - q_before) + (g_admitted - g_before),
            "admission_bandwidth_residual": (g_admitted - g_before) + write,
            "target_owner_residual": (occupation_admitted[event] - occupation_before[event]) - write,
            "transport_node_residual_l1": float(np.sum(np.abs(transport_residual))),
            "transport_node_residual_linf": float(np.max(np.abs(transport_residual))),
            "transport_number_drift": abs(q_after - q_admitted),
            "transport_genesis_drift": abs(parent.remaining(admitted) - g_admitted),
            "actual_norm_error": abs(parent.norm(admitted) - 1.0),
            "null_norm_error": abs(parent.norm(before) - 1.0),
            "actual_solver": actual_solver,
            "null_solver": null_solver,
        })
        state = admitted
    return {"rows": rows, "dimension": math.comb(3 * length, length), "edges": len(parent.edges)}


def worker(length: int, output: Path):
    if output.exists():
        raise FileExistsError(f"refuse overwrite: {output}")
    if length == 12:
        raise RuntimeError("L12 hard lock: terminal/memory supplement and L10 benchmark required")
    if length not in SUPPORTED:
        raise ValueError(f"supported sizes: {SUPPORTED}")
    if sealed.KRYLOV_STORAGE_BYTES != 1_400_000_000:
        raise AssertionError("sealed base target changed")
    sealed.KRYLOV_STORAGE_BYTES = SEALED_BATCH_BYTES
    started = time.perf_counter()
    coarse = history(length, sealed.COARSE)
    fine = history(length, sealed.FINE)
    comparison = sealed.summarize(length, coarse, fine)
    result = {
        "schema": "R_PREFIX_LINEAGE_HISTORY_ENGINE_TARGET_V001",
        "L": length,
        "dimension": fine["dimension"],
        "events": length,
        "edges": fine["edges"],
        "representation": "EXACT_OWNER_ONCE_PREFIX_LINEAGE_ROWS__FULL_TERMINAL_CONTROL_LTE_L10",
        "coarse_method": sealed.COARSE.__dict__,
        "fine_method": sealed.FINE.__dict__,
        "rows": fine["rows"],
        "comparison": comparison,
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "method_sha256": digest(Path(__file__)),
        "sealed_base_sha256": digest(BASE_DIR / "compute_streamed_history.py"),
        "physical_protocol_sha256": digest(BASE_DIR / "PROTOCOL.md"),
        "representation_protocol_sha256": digest(
            ROOT / "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001" / "PROTOCOL.md"
        ),
        "claim_boundary": "FINITE_PREFIX_HISTORY_CONTROL_OR_L10_BENCHMARK_ONLY__NO_L12",
    }
    if length == 10:
        result["resource_guards"] = {
            "rss_limit_bytes": RSS_LIMIT,
            "wall_limit_seconds": WALL_LIMIT,
            "rss_pass": result["peak_rss_bytes"] <= RSS_LIMIT,
            "wall_pass": result["wall_seconds"] <= WALL_LIMIT,
        }
        if not all(result["resource_guards"].values()):
            comparison["resolved"] = False
            comparison["classification"] = "PREFIX_L10_RESOURCE_GATE_FAILED"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(comparison["classification"])
    print(f"L={length} wall={result['wall_seconds']:.6f}s rss={result['peak_rss_bytes']}")
    print(f"difference={comparison['coarse_fine']['maximum_disagreement']:.3e}")
    if not comparison["resolved"]:
        raise SystemExit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    worker(args.worker, args.output)
