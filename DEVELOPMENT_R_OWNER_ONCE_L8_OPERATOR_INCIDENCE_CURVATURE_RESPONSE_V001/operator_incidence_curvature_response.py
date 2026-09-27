#!/usr/bin/env python3
"""Pre-production implementation for the frozen operator-incidence packet.

The only live numerical command in this migration packet is the authenticated
dense L4 development check.  L8 extraction and joining remain fail-closed
because FREEZE.json says execution_authorized=false and the separately sealed
L8 response adapter does not exist.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import math
import os
import resource
import stat
import sys
import tempfile
import time
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from preproduction_verifier import (
    CLAIM_BOUNDARY,
    FROZEN_HASHES,
    PACKET,
    ROOT,
    SOURCE_RECORDS,
    UNRESOLVED,
    VerificationError,
    read_authenticated,
    safe_repository_file,
    sha256_file,
    strict_json_load,
    verify_all_preproduction_inputs,
    verify_freeze_and_manifest,
)


ALPHA = 0.5
SOLVER_TOLERANCE = 1.0e-11
COMPARISON_GUARD = 1.0e-12
MASS_TOLERANCE = 1.0e-14
RESPONSE_SCHEMA = "L8_ALL_EVENT_AUTONOMOUS_LINEAGE_RESPONSE_V001"
RESPONSE_DEFINITION = "POST_TRANSPORT_CARRIER_CONFIGURATION_TV_ACTUAL_VS_SAME_Q_PRODUCT"
CONDUCTANCE_SCHEMA = "L8_OPERATOR_INCIDENCE_CONDUCTANCE_V001"


class CurvatureError(RuntimeError):
    """Invalid graph, measure, solver, adapter, or development-check state."""


class PublicationError(RuntimeError):
    """Atomic publication could not meet the no-overwrite contract."""


class ProductionNotAuthorized(RuntimeError):
    """The frozen L8 production gates are not open."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CurvatureError(message)


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=True,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise CurvatureError(f"value is not canonical finite JSON: {error}") from error


def seal_payload(payload: dict[str, Any]) -> dict[str, Any]:
    require("seal" not in payload, "payload already contains a seal")
    sealed = dict(payload)
    sealed["seal"] = hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    return sealed


def validate_embedded_seal(payload: dict[str, Any]) -> None:
    require(isinstance(payload, dict), "sealed payload must be an object")
    seal = payload.get("seal")
    require(isinstance(seal, str) and len(seal) == 64, "seal must be a SHA-256 hex string")
    require(all(character in "0123456789abcdef" for character in seal), "seal is not lowercase hex")
    unsealed = {key: value for key, value in payload.items() if key != "seal"}
    expected = hashlib.sha256(canonical_json_bytes(unsealed)).hexdigest()
    require(seal == expected, "embedded canonical JSON seal mismatch")


def atomic_publish_json(path: Path, payload: Any) -> dict[str, Any]:
    """Publish complete JSON atomically and refuse every overwrite race.

    A same-directory temporary file is flushed and fsynced, then hard-linked
    into the final name.  Creating the final hard link is atomic and fails if
    anything already occupies the name; unlike os.replace it cannot overwrite.
    """
    destination = path.absolute()
    parent = destination.parent
    require(parent.is_dir(), f"publication parent does not exist: {parent}")
    require(not parent.is_symlink(), f"publication parent may not be a symlink: {parent}")
    require(destination.suffix == ".json", "publication target must have a .json suffix")
    if os.path.lexists(destination):
        raise PublicationError(f"refuse to overwrite existing target: {destination}")
    body = canonical_json_bytes(payload) + b"\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=parent
    )
    temporary = Path(temporary_name)
    published = False
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            stream.write(body)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, destination, follow_symlinks=False)
        published = True
        directory_fd = os.open(parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except FileExistsError as error:
        raise PublicationError(f"concurrent target creation; no overwrite performed: {destination}") from error
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    require(published and destination.is_file() and not destination.is_symlink(),
            "atomic publication did not produce a plain file")
    require(destination.read_bytes() == body, "published bytes failed immediate verification")
    return {
        "path": str(destination),
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "atomic": True,
        "overwrite_permitted": False,
        "method": "FSYNC_TEMP_THEN_ATOMIC_SAME_DIRECTORY_HARD_LINK",
    }


@dataclass(frozen=True)
class Support:
    length: int
    vertices: tuple[str, ...]
    admission_edges: tuple[tuple[str, str], ...]
    transport_edges: tuple[tuple[str, str], ...]

    @property
    def edges(self) -> tuple[tuple[str, str], ...]:
        return self.admission_edges + self.transport_edges

    @property
    def edge_keys(self) -> tuple[str, ...]:
        return tuple(edge_key(edge) for edge in self.edges)

    def as_json(self) -> dict[str, Any]:
        return {
            "L": self.length,
            "vertices": list(self.vertices),
            "admission_edges": [list(edge) for edge in self.admission_edges],
            "transport_edges": [list(edge) for edge in self.transport_edges],
            "metric": "UNIT_SHORTEST_PATH_ON_FIXED_UNPRUNED_SUPPORT",
        }


def edge_key(edge: tuple[str, str]) -> str:
    return f"{edge[0]}--{edge[1]}"


def _load_frozen_parent_module() -> types.ModuleType:
    relative = "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py"
    expected_bytes, expected_hash = SOURCE_RECORDS[relative]
    source_path = safe_repository_file(relative)

    def execute_authenticated(path: Path) -> types.ModuleType:
        source = path.read_bytes()
        module = types.ModuleType("_authenticated_compute_seed_history")
        module.__file__ = str(path)
        code = compile(source, str(path), "exec")
        exec(code, module.__dict__)
        return module

    module = read_authenticated(source_path, expected_hash, expected_bytes, execute_authenticated)
    require(callable(getattr(module, "prism_edges", None)), "frozen parent lacks prism_edges")
    require(callable(getattr(module, "Parent", None)), "frozen parent lacks Parent")
    return module


def build_support(length: int, parent_module: types.ModuleType | None = None) -> Support:
    """Recover support directly from the authenticated primitive graph source."""
    require(type(length) is int and length >= 3, "support length must be an integer >= 3")
    module = parent_module if parent_module is not None else _load_frozen_parent_module()
    raw_edges = module.prism_edges(length)
    require(isinstance(raw_edges, list) and len(raw_edges) == 3 * length,
            "prism_edges returned the wrong edge census")
    expected_connectors = {
        (site, length + (site + 1) % length) for site in range(length)
    }
    seen_connectors: set[tuple[int, int]] = set()
    transport: list[tuple[str, str]] = []
    raw_undirected: set[frozenset[int]] = set()
    for record in raw_edges:
        require(isinstance(record, tuple) and len(record) == 3, "malformed primitive prism edge")
        u, v, kind = record
        require(type(u) is int and type(v) is int and isinstance(kind, str),
                "primitive prism edge types")
        require(0 <= u < 2 * length and 0 <= v < 2 * length and u != v,
                "primitive prism endpoint range")
        undirected = frozenset((u, v))
        require(undirected not in raw_undirected, "duplicate primitive prism edge")
        raw_undirected.add(undirected)
        if kind == "connector":
            seen_connectors.add((u, v))
        transport.append((f"C_{u}", f"C_{v}"))
    require(seen_connectors == expected_connectors,
            "primitive connector matching is not the frozen shifted matching")
    aligned = {(site, length + site) for site in range(length)}
    require(seen_connectors != aligned, "aligned rungs are prohibited")
    vertices = tuple(
        [f"F_{event}" for event in range(length)]
        + [f"C_{site}" for site in range(2 * length)]
    )
    admissions = tuple((f"F_{event}", f"C_{event}") for event in range(length))
    support = Support(length, vertices, admissions, tuple(transport))
    require(len(support.vertices) == 3 * length, "support vertex census")
    require(len(support.edges) == 4 * length, "support edge census")
    require(len(set(support.edge_keys)) == len(support.edges), "support edge keys are not unique")
    adjacency = support_adjacency(support)
    reached = {vertices[0]}
    queue = collections.deque([vertices[0]])
    while queue:
        for neighbor in adjacency[queue.popleft()]:
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    require(reached == set(vertices), "support graph is disconnected")
    return support


def support_adjacency(support: Support) -> dict[str, tuple[str, ...]]:
    adjacency: dict[str, list[str]] = {vertex: [] for vertex in support.vertices}
    for u, v in support.edges:
        require(u in adjacency and v in adjacency and u != v, "invalid support edge")
        adjacency[u].append(v)
        adjacency[v].append(u)
    return {vertex: tuple(neighbors) for vertex, neighbors in adjacency.items()}


def all_pairs_shortest_path(support: Support) -> dict[str, dict[str, int]]:
    adjacency = support_adjacency(support)
    distances: dict[str, dict[str, int]] = {}
    for source in support.vertices:
        found = {source: 0}
        queue = collections.deque([source])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor not in found:
                    found[neighbor] = found[current] + 1
                    queue.append(neighbor)
        require(len(found) == len(support.vertices), "fixed support metric is disconnected")
        distances[source] = found
    return distances


def validate_conductance(support: Support, conductance: dict[str, float]) -> dict[str, float]:
    require(isinstance(conductance, dict), "conductance must be an object")
    require(set(conductance) == set(support.edge_keys), "conductance edge census mismatch")
    answer: dict[str, float] = {}
    for key in support.edge_keys:
        value = conductance[key]
        require(type(value) in {int, float} and not isinstance(value, bool),
                f"conductance is not numeric: {key}")
        number = float(value)
        require(math.isfinite(number) and number >= 0.0, f"invalid conductance: {key}")
        answer[key] = number
    return answer


def lazy_measure(
    support: Support,
    conductance: dict[str, float],
    vertex: str,
    alpha: float = ALPHA,
) -> dict[str, float]:
    require(vertex in support.vertices, f"unknown support vertex: {vertex}")
    require(0.0 <= alpha < 1.0 and math.isfinite(alpha), "invalid idleness")
    values = validate_conductance(support, conductance)
    incident: list[tuple[str, float]] = []
    for edge, key in zip(support.edges, support.edge_keys):
        u, v = edge
        if u == vertex:
            incident.append((v, values[key]))
        elif v == vertex:
            incident.append((u, values[key]))
    weighted_degree = math.fsum(weight for _, weight in incident)
    require(math.isfinite(weighted_degree) and weighted_degree > 0.0,
            f"zero total weighted degree at {vertex}")
    measure = {name: 0.0 for name in support.vertices}
    measure[vertex] = alpha
    for neighbor, weight in incident:
        measure[neighbor] += (1.0 - alpha) * weight / weighted_degree
    require(abs(math.fsum(measure.values()) - 1.0) <= 5.0e-15,
            f"lazy measure normalization failure at {vertex}")
    return measure


def _positive_measure(measure: dict[str, float], order: Sequence[str]) -> tuple[list[str], list[float]]:
    require(set(measure) == set(order), "measure vertex census mismatch")
    names: list[str] = []
    masses: list[float] = []
    for name in order:
        value = measure[name]
        require(type(value) in {int, float} and not isinstance(value, bool), "measure mass type")
        mass = float(value)
        require(math.isfinite(mass) and mass >= -MASS_TOLERANCE, "invalid measure mass")
        if mass > MASS_TOLERANCE:
            names.append(name)
            masses.append(mass)
    total = math.fsum(masses)
    require(abs(total - 1.0) <= 1.0e-12, "measure is not normalized")
    masses = [mass / total for mass in masses]
    return names, masses


def w1_complete_metric_transport(
    support: Support,
    first: dict[str, float],
    second: dict[str, float],
    distances: dict[str, dict[str, int]] | None = None,
) -> float:
    """Complete-metric route: independent transportation-simplex solver."""
    metric = distances if distances is not None else all_pairs_shortest_path(support)
    sources, supply = _positive_measure(first, support.vertices)
    targets, demand = _positive_measure(second, support.vertices)
    m, n = len(sources), len(targets)
    costs = [[float(metric[sources[i]][targets[j]]) for j in range(n)] for i in range(m)]

    allocation = [[0.0 for _ in range(n)] for _ in range(m)]
    remaining_supply = list(supply)
    remaining_demand = list(demand)
    positive_basis: set[tuple[int, int]] = set()
    i = j = 0
    while i < m and j < n:
        value = min(remaining_supply[i], remaining_demand[j])
        if value > MASS_TOLERANCE:
            allocation[i][j] = value
            positive_basis.add((i, j))
        remaining_supply[i] = max(0.0, remaining_supply[i] - value)
        remaining_demand[j] = max(0.0, remaining_demand[j] - value)
        row_done = remaining_supply[i] <= MASS_TOLERANCE
        column_done = remaining_demand[j] <= MASS_TOLERANCE
        if row_done:
            i += 1
        if column_done:
            j += 1
        require(row_done or column_done, "transport initialization did not progress")

    # Positive northwest-corner cells form a forest.  Add deterministic zero
    # basics without cycles until the basis is one bipartite spanning tree.
    parent = list(range(m + n))

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(left: int, right: int) -> bool:
        root_left, root_right = find(left), find(right)
        if root_left == root_right:
            return False
        parent[root_right] = root_left
        return True

    basis: set[tuple[int, int]] = set()
    for row, column in sorted(positive_basis):
        require(union(row, m + column), "positive transport basis contains a cycle")
        basis.add((row, column))
    for row in range(m):
        for column in range(n):
            if len(basis) == m + n - 1:
                break
            if union(row, m + column):
                basis.add((row, column))
        if len(basis) == m + n - 1:
            break
    require(len(basis) == m + n - 1, "could not complete transportation basis")

    for _iteration in range(10000):
        u: list[float | None] = [None] * m
        v: list[float | None] = [None] * n
        u[0] = 0.0
        changed = True
        while changed:
            changed = False
            for row, column in basis:
                if u[row] is not None and v[column] is None:
                    v[column] = costs[row][column] - u[row]
                    changed = True
                elif v[column] is not None and u[row] is None:
                    u[row] = costs[row][column] - v[column]
                    changed = True
        require(all(value is not None for value in u + v), "transport basis disconnected")
        entering: tuple[int, int] | None = None
        for row in range(m):
            for column in range(n):
                if (row, column) in basis:
                    continue
                reduced = costs[row][column] - float(u[row]) - float(v[column])
                if reduced < -1.0e-13:
                    entering = (row, column)  # Bland's first-index pivot rule.
                    break
            if entering is not None:
                break
        if entering is None:
            break

        enter_row, enter_column = entering
        graph: dict[int, list[tuple[int, tuple[int, int]]]] = {
            node: [] for node in range(m + n)
        }
        for cell in basis:
            row, column = cell
            graph[row].append((m + column, cell))
            graph[m + column].append((row, cell))
        start, goal = m + enter_column, enter_row
        queue = collections.deque([start])
        predecessor: dict[int, tuple[int, tuple[int, int]]] = {}
        seen = {start}
        while queue and goal not in seen:
            node = queue.popleft()
            for neighbor, cell in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    predecessor[neighbor] = (node, cell)
                    queue.append(neighbor)
        require(goal in seen, "transport pivot cycle path missing")
        reverse_path: list[tuple[int, int]] = []
        cursor = goal
        while cursor != start:
            previous, cell = predecessor[cursor]
            reverse_path.append(cell)
            cursor = previous
        path = list(reversed(reverse_path))  # column endpoint back to entering row.
        require(len(path) % 2 == 1, "transport pivot path parity")
        minus_cells = path[0::2]
        theta = min(allocation[row][column] for row, column in minus_cells)
        require(theta >= -MASS_TOLERANCE, "negative transportation pivot")
        theta = max(0.0, theta)
        allocation[enter_row][enter_column] += theta
        for index, (row, column) in enumerate(path):
            if index % 2 == 0:
                allocation[row][column] -= theta
                if abs(allocation[row][column]) <= MASS_TOLERANCE:
                    allocation[row][column] = 0.0
            else:
                allocation[row][column] += theta
        leaving_candidates = sorted(
            cell for cell in minus_cells if allocation[cell[0]][cell[1]] <= MASS_TOLERANCE
        )
        require(leaving_candidates, "transport pivot has no leaving cell")
        basis.add(entering)
        basis.remove(leaving_candidates[0])
    else:  # pragma: no cover - a guard against implementation regressions.
        raise CurvatureError("transportation simplex iteration cap exceeded")

    for row in range(m):
        require(abs(math.fsum(allocation[row]) - supply[row]) <= 2.0e-12,
                "transportation row marginal mismatch")
    for column in range(n):
        require(abs(math.fsum(allocation[row][column] for row in range(m)) - demand[column])
                <= 2.0e-12, "transportation column marginal mismatch")
    value = math.fsum(
        allocation[row][column] * costs[row][column]
        for row in range(m)
        for column in range(n)
    )
    require(math.isfinite(value) and value >= -1.0e-12, "invalid complete-metric W1")
    return max(0.0, value)


@dataclass
class _ResidualArc:
    to: int
    reverse: int
    capacity: float
    cost: float


def w1_fixed_support_transshipment(
    support: Support,
    first: dict[str, float],
    second: dict[str, float],
) -> float:
    """Fixed-support route: independently coded residual graph transshipment."""
    first_names, first_mass = _positive_measure(first, support.vertices)
    second_names, second_mass = _positive_measure(second, support.vertices)
    first_by_name = dict(zip(first_names, first_mass))
    second_by_name = dict(zip(second_names, second_mass))
    imbalance = [
        first_by_name.get(vertex, 0.0) - second_by_name.get(vertex, 0.0)
        for vertex in support.vertices
    ]
    require(abs(math.fsum(imbalance)) <= 2.0e-12, "transshipment imbalance does not sum to zero")

    vertex_index = {vertex: index for index, vertex in enumerate(support.vertices)}
    count = len(support.vertices)
    source, sink = count, count + 1
    graph: list[list[_ResidualArc]] = [[] for _ in range(count + 2)]

    def add_arc(start: int, end: int, capacity: float, cost: float) -> None:
        forward = _ResidualArc(end, len(graph[end]), capacity, cost)
        backward = _ResidualArc(start, len(graph[start]), 0.0, -cost)
        graph[start].append(forward)
        graph[end].append(backward)

    # Each primitive undirected edge supplies two unit-cost directions.  These
    # are not complete-metric arcs, and this code shares no optimizer with the
    # transportation-simplex route above.
    for left, right in support.edges:
        u, v = vertex_index[left], vertex_index[right]
        add_arc(u, v, 1.0, 1.0)
        add_arc(v, u, 1.0, 1.0)
    required_flow = 0.0
    for index, value in enumerate(imbalance):
        if value > MASS_TOLERANCE:
            add_arc(source, index, value, 0.0)
            required_flow += value
        elif value < -MASS_TOLERANCE:
            add_arc(index, sink, -value, 0.0)

    delivered = 0.0
    total_cost = 0.0
    nodes = len(graph)
    for _iteration in range(10000):
        if delivered + 5.0e-14 >= required_flow:
            break
        distance = [math.inf] * nodes
        previous_node = [-1] * nodes
        previous_arc = [-1] * nodes
        distance[source] = 0.0
        # Bellman-Ford deliberately handles negative residual cancellation arcs.
        for _ in range(nodes - 1):
            changed = False
            for start in range(nodes):
                if not math.isfinite(distance[start]):
                    continue
                for arc_index, arc in enumerate(graph[start]):
                    if arc.capacity <= MASS_TOLERANCE:
                        continue
                    candidate = distance[start] + arc.cost
                    if candidate < distance[arc.to] - 1.0e-14:
                        distance[arc.to] = candidate
                        previous_node[arc.to] = start
                        previous_arc[arc.to] = arc_index
                        changed = True
            if not changed:
                break
        require(math.isfinite(distance[sink]), "fixed-support transshipment cannot route all mass")
        increment = required_flow - delivered
        cursor = sink
        while cursor != source:
            start = previous_node[cursor]
            arc_index = previous_arc[cursor]
            require(start >= 0 and arc_index >= 0, "broken transshipment predecessor chain")
            increment = min(increment, graph[start][arc_index].capacity)
            cursor = start
        require(increment > MASS_TOLERANCE, "zero transshipment augmentation")
        cursor = sink
        while cursor != source:
            start = previous_node[cursor]
            arc_index = previous_arc[cursor]
            arc = graph[start][arc_index]
            arc.capacity -= increment
            graph[cursor][arc.reverse].capacity += increment
            cursor = start
        delivered += increment
        total_cost += increment * distance[sink]
    else:  # pragma: no cover
        raise CurvatureError("fixed-support transshipment iteration cap exceeded")
    require(abs(delivered - required_flow) <= 2.0e-12, "incomplete transshipment flow")
    require(math.isfinite(total_cost) and total_cost >= -1.0e-12, "invalid transshipment W1")
    return max(0.0, total_cost)


def curvature_for_conductance(
    support: Support,
    conductance: dict[str, float],
) -> dict[str, Any]:
    values = validate_conductance(support, conductance)
    metric = all_pairs_shortest_path(support)
    curvatures: dict[str, float] = {}
    w1_complete: dict[str, float] = {}
    w1_transshipment: dict[str, float] = {}
    maximum_disagreement = 0.0
    for edge, key in zip(support.edges, support.edge_keys):
        first = lazy_measure(support, values, edge[0])
        second = lazy_measure(support, values, edge[1])
        complete = w1_complete_metric_transport(support, first, second, metric)
        control = w1_fixed_support_transshipment(support, first, second)
        disagreement = abs(complete - control)
        require(disagreement <= SOLVER_TOLERANCE,
                f"independent W1 solver disagreement at {key}: {disagreement}")
        maximum_disagreement = max(maximum_disagreement, disagreement)
        w1_complete[key] = complete
        w1_transshipment[key] = control
        curvatures[key] = 1.0 - complete
    return {
        "curvature": curvatures,
        "w1_complete_metric_transport": w1_complete,
        "w1_fixed_support_transshipment": w1_transshipment,
        "maximum_solver_disagreement": maximum_disagreement,
        "solver_tolerance": SOLVER_TOLERANCE,
    }


def analyze_conductance_pair(
    support: Support,
    actual: dict[str, float],
    product: dict[str, float],
) -> dict[str, Any]:
    actual_values = validate_conductance(support, actual)
    product_values = validate_conductance(support, product)
    transport_difference = max(
        abs(actual_values[edge_key(edge)] - product_values[edge_key(edge)])
        for edge in support.transport_edges
    )
    require(transport_difference <= 1.0e-13,
            "actual/product carrier transport conductances differ")
    actual_bundle = curvature_for_conductance(support, actual_values)
    product_bundle = curvature_for_conductance(support, product_values)
    predictor = [
        actual_bundle["curvature"][edge_key(edge)]
        - product_bundle["curvature"][edge_key(edge)]
        for edge in support.admission_edges
    ]
    require(all(math.isfinite(value) for value in predictor), "nonfinite curvature predictor")
    return {
        "actual": actual_bundle,
        "same_q_product": product_bundle,
        "admission_predictor_actual_minus_product": predictor,
        "maximum_transport_conductance_difference": transport_difference,
        "maximum_solver_disagreement": max(
            actual_bundle["maximum_solver_disagreement"],
            product_bundle["maximum_solver_disagreement"],
        ),
    }


def midranks(values: Sequence[float]) -> list[float]:
    require(len(values) > 1, "at least two values are required for ranks")
    numeric = [float(value) for value in values]
    require(all(math.isfinite(value) for value in numeric), "rank input contains nonfinite value")
    order = sorted(range(len(numeric)), key=lambda index: (numeric[index], index))
    ranks = [0.0] * len(numeric)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and numeric[order[end]] == numeric[order[start]]:
            end += 1
        rank = ((start + 1) + end) / 2.0
        for position in range(start, end):
            ranks[order[position]] = rank
        start = end
    return ranks


def spearman_midrank(first: Sequence[float], second: Sequence[float]) -> float:
    require(len(first) == len(second) and len(first) > 1, "Spearman vector size mismatch")
    left, right = midranks(first), midranks(second)
    left_mean = math.fsum(left) / len(left)
    right_mean = math.fsum(right) / len(right)
    covariance = math.fsum(
        (left[index] - left_mean) * (right[index] - right_mean)
        for index in range(len(left))
    )
    left_square = math.fsum((value - left_mean) ** 2 for value in left)
    right_square = math.fsum((value - right_mean) ** 2 for value in right)
    require(left_square > 0.0 and right_square > 0.0, "zero-variance Spearman rank vector")
    rho = covariance / math.sqrt(left_square * right_square)
    require(math.isfinite(rho) and -1.0 - 1.0e-14 <= rho <= 1.0 + 1.0e-14,
            "invalid Spearman correlation")
    return max(-1.0, min(1.0, rho))


def exact_l8_permutation_statistics(
    predictor: Sequence[float],
    response: Sequence[float],
    guard: float = COMPARISON_GUARD,
) -> dict[str, Any]:
    require(len(predictor) == 8 and len(response) == 8,
            "the frozen exact null requires exactly eight labels")
    require(math.isfinite(guard) and guard >= 0.0, "invalid comparison guard")
    observed = spearman_midrank(predictor, response)
    absolute_count = 0
    plus_count = 0
    minus_count = 0
    minimum = math.inf
    maximum = -math.inf
    count = 0
    for permutation in itertools.permutations(tuple(float(value) for value in response)):
        rho = spearman_midrank(predictor, permutation)
        count += 1
        minimum = min(minimum, rho)
        maximum = max(maximum, rho)
        if abs(rho) + guard >= abs(observed):
            absolute_count += 1
        if rho + guard >= observed:
            plus_count += 1
        if rho - guard <= observed:
            minus_count += 1
    require(count == math.factorial(8) == 40320, "incomplete exact permutation census")
    return {
        "rho": observed,
        "permutation_count": count,
        "p_abs": absolute_count / count,
        "p_plus": plus_count / count,
        "p_minus": minus_count / count,
        "absolute_tail_count": absolute_count,
        "plus_tail_count": plus_count,
        "minus_tail_count": minus_count,
        "minimum_permuted_rho": minimum,
        "maximum_permuted_rho": maximum,
        "comparison_guard": guard,
        "rank_convention": "EXACT_MIDRANK",
    }


def validate_response_adapter(adapter: dict[str, Any]) -> list[float]:
    require(isinstance(adapter, dict) and set(adapter) == {
        "schema", "definition", "labels", "carrier_configuration_tv_by_event",
        "provenance", "seal",
    }, "response adapter top-level key census")
    require(adapter["schema"] == RESPONSE_SCHEMA, "response adapter schema")
    require(adapter["definition"] == RESPONSE_DEFINITION, "response definition")
    require(adapter["labels"] == list(range(8)), "response labels")
    require(isinstance(adapter["provenance"], dict) and adapter["provenance"],
            "response provenance must be a nonempty object")
    values = adapter["carrier_configuration_tv_by_event"]
    require(isinstance(values, list) and len(values) == 8, "response vector size")
    response: list[float] = []
    for value in values:
        require(type(value) in {int, float} and not isinstance(value, bool), "response value type")
        number = float(value)
        require(math.isfinite(number) and 0.0 <= number <= 1.0, "response TV range")
        response.append(number)
    validate_embedded_seal(adapter)
    return response


def validate_conductance_adapter(adapter: dict[str, Any]) -> tuple[Support, dict[str, float], dict[str, float]]:
    require(isinstance(adapter, dict) and set(adapter) == {
        "schema", "status", "L", "support", "conductance_actual",
        "conductance_same_q_product", "source", "claim_boundary", "seal",
    }, "conductance adapter top-level key census")
    require(adapter["schema"] == CONDUCTANCE_SCHEMA, "conductance adapter schema")
    require(adapter["status"] == "SEALED_L8_CONDUCTANCE_ADAPTER", "conductance adapter status")
    require(adapter["L"] == 8 and type(adapter["L"]) is int, "conductance adapter L")
    require(adapter["claim_boundary"] == CLAIM_BOUNDARY, "conductance adapter claim boundary")
    require(isinstance(adapter["source"], dict) and adapter["source"],
            "conductance source provenance")
    support = build_support(8)
    require(adapter["support"] == support.as_json(), "conductance support does not match primitive source")
    actual = validate_conductance(support, adapter["conductance_actual"])
    product = validate_conductance(support, adapter["conductance_same_q_product"])
    validate_embedded_seal(adapter)
    return support, actual, product


def analyze_sealed_l8_adapters(
    conductance_adapter: dict[str, Any],
    response_adapter: dict[str, Any],
) -> dict[str, Any]:
    support, actual, product = validate_conductance_adapter(conductance_adapter)
    response = validate_response_adapter(response_adapter)
    analysis = analyze_conductance_pair(support, actual, product)
    predictor = analysis["admission_predictor_actual_minus_product"]
    statistic = exact_l8_permutation_statistics(predictor, response)
    product_admission = [
        analysis["same_q_product"]["curvature"][edge_key(edge)]
        for edge in support.admission_edges
    ]
    product_control_rho = spearman_midrank(product_admission, response)
    classification = (
        "RESOLVED_L8_OPERATOR_INCIDENCE_CURVATURE_RESPONSE_ASSOCIATION"
        if abs(statistic["rho"]) >= 0.5 and statistic["p_abs"] <= 0.05
        else "NO_RESOLVED_L8_OPERATOR_INCIDENCE_CURVATURE_RESPONSE_ASSOCIATION"
    )
    return {
        "schema": "L8_OPERATOR_INCIDENCE_CURVATURE_RESPONSE_RESULT_V001",
        "status": classification,
        "predictor": predictor,
        "response": response,
        "statistic": statistic,
        "secondary_product_arm_admission_curvature_rho": product_control_rho,
        "controls": {
            "maximum_transport_conductance_difference": analysis[
                "maximum_transport_conductance_difference"
            ],
            "maximum_solver_disagreement": analysis["maximum_solver_disagreement"],
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _dense_l4_conductances(
    parent: Any,
    state: Any,
    support: Support,
) -> tuple[dict[str, float], dict[str, float]]:
    # NumPy belongs to the authenticated dense source; both W1 solvers above
    # remain dependency-free standard-Python implementations.
    import numpy as np

    probability = np.abs(state) ** 2
    require(abs(float(np.sum(probability)) - 1.0) <= 2.0e-12, "dense L4 state norm")
    actual: dict[str, float] = {}
    product: dict[str, float] = {}
    carrier_words = parent.carrier_words
    for event, edge in enumerate(support.admission_edges):
        genesis_loaded = ((parent.words >> event) & 1) == 1
        carrier_occupied = ((carrier_words >> event) & 1) == 1
        actual_value = float(np.sum(probability[genesis_loaded != carrier_occupied]))
        product_value = 0.0
        for q in range(parent.sites + 1):
            sector = parent.carrier_counts == q
            sector_mass = float(np.sum(probability[sector]))
            if sector_mass <= 1.0e-16:
                continue
            loaded_mass = float(np.sum(probability[sector & genesis_loaded]))
            spent_mass = sector_mass - loaded_mass
            occupied_mass = float(np.sum(probability[sector & carrier_occupied]))
            blank_mass = sector_mass - occupied_mass
            product_value += (
                loaded_mass * blank_mass + spent_mass * occupied_mass
            ) / sector_mass
        actual[edge_key(edge)] = actual_value
        product[edge_key(edge)] = product_value
    primitive_edges = list(parent.edges)
    require(len(primitive_edges) == len(support.transport_edges), "dense primitive edge census")
    for primitive, edge in zip(primitive_edges, support.transport_edges):
        u, v, _kind = primitive
        occupied_u = ((carrier_words >> u) & 1) == 1
        occupied_v = ((carrier_words >> v) & 1) == 1
        value = float(np.sum(probability[occupied_u != occupied_v]))
        actual[edge_key(edge)] = value
        product[edge_key(edge)] = value
    return validate_conductance(support, actual), validate_conductance(support, product)


def _maximum_rss_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    # macOS reports bytes; Linux and most BSD-derived CI environments report KiB.
    return value if sys.platform == "darwin" else value * 1024


def run_development_l4_check() -> dict[str, Any]:
    """Reconstruct and analyze only the authenticated dense L4 checkpoint."""
    started = time.perf_counter()
    rss_before = _maximum_rss_bytes()
    freeze = verify_freeze_and_manifest()
    require(freeze["execution_authorized"] is False, "development must not open L8 production")
    module = _load_frozen_parent_module()
    support = build_support(4, module)
    parent = module.Parent(4)
    state = parent.initial_state()
    for event in range(4):
        state = parent.apply_admission(state, event)
        state, _currents = parent.transport(state, module.FINE_STEPS)
    actual, product = _dense_l4_conductances(parent, state, support)
    analysis = analyze_conductance_pair(support, actual, product)
    wall = time.perf_counter() - started
    result: dict[str, Any] = {
        "schema": "L4_OPERATOR_INCIDENCE_CURVATURE_DEVELOPMENT_CHECK_V001",
        "status": "PASS_AUTHENTICATED_DENSE_L4_DEVELOPMENT_CHECK__NO_L8_INFERENCE",
        "L": 4,
        "checkpoint": "POST_EVENT_3_ADMISSION_AND_TRANSPORT__COMPLETED_OWNER_ONCE_L4",
        "sources": {
            "dense_parent": {
                "path": "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py",
                "sha256": SOURCE_RECORDS[
                    "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py"
                ][1],
            },
            "freeze_sha256": FROZEN_HASHES["FREEZE.json"],
        },
        "support": support.as_json(),
        "conductance_actual": actual,
        "conductance_same_q_product": product,
        "admission_curvature_actual": [
            analysis["actual"]["curvature"][edge_key(edge)]
            for edge in support.admission_edges
        ],
        "admission_curvature_same_q_product": [
            analysis["same_q_product"]["curvature"][edge_key(edge)]
            for edge in support.admission_edges
        ],
        "admission_predictor_actual_minus_product": analysis[
            "admission_predictor_actual_minus_product"
        ],
        "controls": {
            "transport_conductance_preservation_max_abs": analysis[
                "maximum_transport_conductance_difference"
            ],
            "independent_w1_solver_max_abs": analysis["maximum_solver_disagreement"],
            "independent_w1_solver_tolerance": SOLVER_TOLERANCE,
            "support_source_called_at_L4": True,
            "l8_production_run": False,
        },
        "runtime": {
            "wall_seconds": wall,
            "maximum_rss_bytes": max(rss_before, _maximum_rss_bytes()),
            "scratch_storage_bytes": 0,
            "persistent_output_bytes_before_optional_publication": 0,
        },
        "scientific_status": UNRESOLVED,
        "development_ceiling": "L4_DENSE_IMPLEMENTATION_CHECK_ONLY__NO_L8_RESPONSE_OPENED",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    result["runtime"]["canonical_record_bytes"] = len(canonical_json_bytes(result)) + 1
    return result


def require_l8_conductance_extraction_authorization() -> None:
    freeze = verify_freeze_and_manifest()
    if freeze["execution_authorized"] is not True:
        raise ProductionNotAuthorized(
            "FREEZE.json execution_authorized=false; L8 conductance extraction remains NO_GO"
        )


def require_l8_join_authorization() -> None:
    freeze = verify_freeze_and_manifest()
    if freeze["execution_authorized"] is not True:
        raise ProductionNotAuthorized(
            "FREEZE.json execution_authorized=false; L8 curvature/response join remains NO_GO"
        )
    raise ProductionNotAuthorized(
        "no sealed L8 response adapter is registered; production cannot proceed"
    )


def require_l8_production_authorization() -> None:
    """Backward-compatible combined guard used by pre-production callers."""
    require_l8_join_authorization()


def _load_sealed_json(path: Path) -> dict[str, Any]:
    mode = os.lstat(path).st_mode
    require(stat.S_ISREG(mode) and not stat.S_ISLNK(mode), "adapter must be a plain regular file")
    value = strict_json_load(path)
    require(isinstance(value, dict), "adapter top level must be an object")
    return value


def _print_json(payload: Any) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--check-freeze", action="store_true",
                         help="authenticate frozen bytes and relocated L4/L8 shard custody only")
    actions.add_argument("--development-l4-check", action="store_true",
                         help="run the authenticated dense L4-only conductance/W1 check")
    actions.add_argument("--production-l8-conductance", action="store_true",
                         help="guarded L8 extraction entry point; currently refuses before shard use")
    actions.add_argument("--production-join", action="store_true",
                         help="guarded production entry point; currently refuses before reading adapters")
    parser.add_argument("--conductance", type=Path)
    parser.add_argument("--response", type=Path)
    parser.add_argument("--output", type=Path,
                        help="optional atomic no-overwrite JSON output (development or future production)")
    arguments = parser.parse_args(argv)

    if arguments.check_freeze:
        require(arguments.output is None, "freeze checks do not publish output")
        _print_json(verify_all_preproduction_inputs())
        return 0
    if arguments.development_l4_check:
        require(arguments.conductance is None and arguments.response is None,
                "development L4 check accepts no adapters")
        result = run_development_l4_check()
        if arguments.output is not None:
            publication = atomic_publish_json(arguments.output, result)
            result = dict(result)
            result["publication"] = publication
        _print_json(result)
        return 0

    if arguments.production_l8_conductance:
        require(arguments.conductance is None and arguments.response is None,
                "L8 extraction guard accepts no input adapters")
        require_l8_conductance_extraction_authorization()
        raise ProductionNotAuthorized(
            "this migration packet intentionally has no executable L8 extraction path"
        )

    # The frozen authorization check is intentionally first: no adapter is
    # opened, parsed, or inferred while the packet remains unauthorized.
    require_l8_join_authorization()
    require(arguments.conductance is not None and arguments.response is not None,
            "production join requires both sealed adapters")
    result = analyze_sealed_l8_adapters(
        _load_sealed_json(arguments.conductance),
        _load_sealed_json(arguments.response),
    )
    require(arguments.output is not None, "production result requires an explicit output")
    publication = atomic_publish_json(arguments.output, result)
    _print_json({"result": result, "publication": publication})
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        CurvatureError,
        FileNotFoundError,
        OSError,
        ProductionNotAuthorized,
        PublicationError,
        VerificationError,
    ) as error:
        print(f"FAIL operator-incidence curvature preproduction: {error}", file=sys.stderr)
        raise SystemExit(1)
