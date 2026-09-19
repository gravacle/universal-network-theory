#!/usr/bin/env python3
"""Strictly authenticate and test an L12 q4--q5--q6 atom bridge.

Only explicit atom-ID-to-atom-ID edge arrays or per-atom adjacency arrays are
accepted.  Sector proximity, density intervals, array order, and atom-ID order
never create edges.  If no explicit atom-level topology is present, analysis
stops before endpoint traversal or probability-mass aggregation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from collections import deque
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_ADJUDICATION = (
    ROOT
    / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001"
    / "ADJUDICATION_V002_L12_V003R1_STAGE6R2.json"
)
DEFAULT_MANIFEST = (
    ROOT
    / "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003"
    / "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003R1.json"
)
DEFAULT_TARGET_HISTORY = (
    ROOT
    / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
    / "PHYSICAL_OUTPUTS"
    / "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
)
DEFAULT_HOSTILE_HISTORY = (
    ROOT
    / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
    / "V004R4_PHYSICAL_OUTPUTS"
    / "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
)
DEFAULT_TARGET_CACHE_MANIFEST = (
    ROOT
    / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
    / "CACHE_PAYLOADS_V012"
    / "L12"
    / "CACHE_MANIFEST.json"
)
DEFAULT_HOSTILE_CACHE_MANIFEST = (
    ROOT
    / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
    / "V004R4_CACHE_PAYLOADS"
    / "L12"
    / "CACHE_MANIFEST.json"
)
DEFAULT_ADJUDICATION_SHA256 = "43c7c19daaf24902d2699c337851eca35a03c3db69f8e3f55f3b0142f87e137d"
DEFAULT_MANIFEST_SHA256 = "292124df4e1d349827753145ce1dd4be32e073db6d657f30737227edd488184a"
DEFAULT_TARGET_HISTORY_SHA256 = "079499e7b989e1ba45b1c397882c8638106be149ccb994058a3703b235736764"
DEFAULT_HOSTILE_HISTORY_SHA256 = "cbac18fd5033f83e4eadbfb16b46c89584455987e0b75fa6a33a33821246851c"
DEFAULT_TARGET_CACHE_MANIFEST_SHA256 = "c8efb9b36ab18a3727aab4548109256640c92b63c121a07d9993999e4c570d6a"
DEFAULT_HOSTILE_CACHE_MANIFEST_SHA256 = "1640607ea32c63a4af2139dc19a863e47b2fac5603656d059016710c774bceec"

SCHEMA = "L12_STRICT_TOPOLOGY_BRIDGE_V001"
LENGTH = 12
DEFAULT_LOWER = Decimal("0.90")
DEFAULT_UPPER = Decimal("1.10")
DEFAULT_THRESHOLD = Decimal("0.50")

ID_KEYS = ("atom_id", "component_id", "node_id", "id")
NODE_RELATION_KEYS = (
    "neighbors",
    "neighbours",
    "links",
    "adjacencies",
    "adjacency",
    "connections",
    "orbit_relations",
)
GLOBAL_EDGE_KEYS = (
    "edges",
    "edge_layout",
    "links",
    "adjacencies",
    "connections",
    "relations",
)
ALL_RELATION_KEYS = frozenset(NODE_RELATION_KEYS) | frozenset(GLOBAL_EDGE_KEYS)
EDGE_ENDPOINT_KEYS = (
    ("source", "target"),
    ("from", "to"),
    ("u", "v"),
    ("left", "right"),
    ("node1", "node2"),
    ("a", "b"),
)


class AnalysisRefusal(RuntimeError):
    """Input data cannot support the requested analysis."""


@dataclass(frozen=True)
class InputDocument:
    label: str
    path: Path
    sha256: str
    payload: Any


@dataclass(frozen=True)
class Atom:
    atom_id: str
    q: int | None = None
    interval: tuple[Fraction, Fraction] | None = None
    target_z: Decimal | None = None
    target_y: Decimal | None = None
    blind_z: Decimal | None = None
    blind_y: Decimal | None = None

    def passes(self, lower: Decimal, upper: Decimal, source: str) -> bool:
        target = _pair_in_window(self.target_z, self.target_y, lower, upper)
        blind = _pair_in_window(self.blind_z, self.blind_y, lower, upper)
        if source == "target":
            return target
        if source == "blind":
            return blind
        return target and blind


@dataclass(frozen=True)
class Discovery:
    candidate_arrays: tuple["EdgeSource", ...]
    authenticated_edge_arrays: tuple["EdgeSource", ...]
    accepted_explicit_edges: tuple[tuple[str, str], ...]
    rejected_relation_items: int


@dataclass(frozen=True)
class EdgeSource:
    input_label: str
    input_path: str
    json_path: str
    key: str
    kind: str
    accepted_edges: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class BridgeResult:
    path: tuple[str, ...] | None
    q4_endpoints: tuple[str, ...]
    q6_endpoints: tuple[str, ...]
    q4_q5_contacts: Mapping[str, tuple[str, ...]]
    q6_q5_contacts: Mapping[str, tuple[str, ...]]
    shared_direct_q5_nodes: tuple[str, ...]


def validate_sha256(value: str, label: str) -> str:
    normalized = value.strip().lower()
    if len(normalized) != 64 or any(character not in "0123456789abcdef" for character in normalized):
        raise AnalysisRefusal(f"{label}: expected SHA-256 must be 64 hexadecimal characters")
    return normalized


def authenticate_json(path: Path, expected_sha256: str, label: str) -> InputDocument:
    """Hash and parse the same immutable byte snapshot."""

    expected = validate_sha256(expected_sha256, label)
    try:
        before = path.stat()
        if not stat.S_ISREG(before.st_mode):
            raise AnalysisRefusal(f"{label}: input is not a regular file: {path}")
        raw = path.read_bytes()
        after = path.stat()
    except OSError as error:
        raise AnalysisRefusal(f"{label}: cannot read {path}: {error}") from error
    identity_before = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    identity_after = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    if identity_before != identity_after:
        raise AnalysisRefusal(f"{label}: input changed while being authenticated: {path}")
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected:
        raise AnalysisRefusal(
            f"{label}: SHA-256 mismatch for {path}; expected={expected} actual={actual}"
        )
    try:
        payload = json.loads(raw.decode("utf-8"), parse_float=Decimal)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AnalysisRefusal(f"{label}: authenticated bytes are not valid UTF-8 JSON: {error}") from error
    return InputDocument(label=label, path=path, sha256=actual, payload=payload)


def decimal_value(value: Any) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        result = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None
    return result if result.is_finite() else None


def _pair_in_window(
    z: Decimal | None,
    y: Decimal | None,
    lower: Decimal,
    upper: Decimal,
) -> bool:
    return z is not None and y is not None and lower <= z <= upper and lower <= y <= upper


def rational(value: Any) -> Fraction | None:
    if (
        isinstance(value, Sequence)
        and not isinstance(value, (str, bytes))
        and len(value) == 2
        and type(value[0]) is int
        and type(value[1]) is int
        and value[1] != 0
    ):
        return Fraction(value[0], value[1])
    return None


def interval_value(value: Any) -> tuple[Fraction, Fraction] | None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 2:
        return None
    left, right = rational(value[0]), rational(value[1])
    if left is None or right is None or not left < right:
        return None
    return left, right


def classification_zy(value: Any) -> tuple[Decimal | None, Decimal | None]:
    if not isinstance(value, Mapping):
        return None, None
    gap_fit = value.get("gap_power_fit")
    z = gap_fit.get("exponent") if isinstance(gap_fit, Mapping) else value.get("z")
    y = value.get("chi_power_exponent_y", value.get("y"))
    return decimal_value(z), decimal_value(y)


def direct_zy(value: Mapping[str, Any]) -> tuple[Decimal | None, Decimal | None]:
    z, y = decimal_value(value.get("z")), decimal_value(value.get("y"))
    if z is not None and y is not None:
        return z, y
    geometry = value.get("geometry")
    if isinstance(geometry, Mapping):
        return decimal_value(geometry.get("z")), decimal_value(geometry.get("y"))
    return None, None


def q_value(value: Mapping[str, Any]) -> int | None:
    qmap = value.get("q_by_L")
    if isinstance(qmap, Mapping):
        raw = qmap.get(str(LENGTH), qmap.get(LENGTH))
        if type(raw) is int:
            return raw
    for key in ("q", "sector", "charge"):
        raw = value.get(key)
        if type(raw) is int:
            return raw
        if isinstance(raw, str):
            cleaned = raw.lower().removeprefix("q=").removeprefix("q")
            if cleaned.isdigit():
                return int(cleaned)
    return None


def object_id(value: Mapping[str, Any]) -> str | None:
    for key in ID_KEYS:
        raw = value.get(key)
        if isinstance(raw, (str, int)) and not isinstance(raw, bool):
            text = str(raw)
            if text:
                return text
    return None


def merge_atom(current: Atom | None, incoming: Atom) -> Atom:
    if current is None:
        return incoming
    fields: dict[str, Any] = {"atom_id": current.atom_id}
    for name in (
        "q",
        "interval",
        "target_z",
        "target_y",
        "blind_z",
        "blind_y",
    ):
        old, new = getattr(current, name), getattr(incoming, name)
        if old is not None and new is not None and old != new:
            raise AnalysisRefusal(f"{current.atom_id}: conflicting {name} across JSON inputs")
        fields[name] = old if old is not None else new
    return Atom(**fields)


def atoms_from_adjudication(payload: Any) -> dict[str, Atom]:
    if not isinstance(payload, Mapping) or not isinstance(payload.get("atom_results"), list):
        return {}
    atoms: dict[str, Atom] = {}
    for entry in payload["atom_results"]:
        if not isinstance(entry, Mapping) or not isinstance(entry.get("atom"), Mapping):
            continue
        raw = entry["atom"]
        atom_id = object_id(raw)
        if atom_id is None:
            continue
        target_z, target_y = classification_zy(entry.get("target_classification"))
        blind_z, blind_y = classification_zy(entry.get("blind_classification"))
        atoms[atom_id] = Atom(
            atom_id=atom_id,
            q=q_value(raw),
            interval=interval_value(raw.get("density_interval")),
            target_z=target_z,
            target_y=target_y,
            blind_z=blind_z,
            blind_y=blind_y,
        )
    return atoms


def discover_atom_objects(payload: Any) -> dict[str, Atom]:
    """Find generic node/component objects outside the Stage-6 schema."""

    result: dict[str, Atom] = {}

    def walk(value: Any) -> None:
        if isinstance(value, Mapping):
            atom_id = object_id(value)
            has_atom_signal = (
                q_value(value) is not None
                or interval_value(value.get("density_interval")) is not None
                or any(key in value for key in NODE_RELATION_KEYS)
                or (decimal_value(value.get("z")) is not None and decimal_value(value.get("y")) is not None)
            )
            if atom_id is not None and has_atom_signal:
                z, y = direct_zy(value)
                target_z, target_y = classification_zy(value.get("target"))
                blind_z, blind_y = classification_zy(value.get("blind"))
                if target_z is None:
                    target_z, target_y = z, y
                if blind_z is None:
                    blind_z, blind_y = z, y
                incoming = Atom(
                    atom_id=atom_id,
                    q=q_value(value),
                    interval=interval_value(value.get("density_interval")),
                    target_z=target_z,
                    target_y=target_y,
                    blind_z=blind_z,
                    blind_y=blind_y,
                )
                result[atom_id] = merge_atom(result.get(atom_id), incoming)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(payload)
    return result


def merge_atoms(payloads: Sequence[Any]) -> dict[str, Atom]:
    atoms: dict[str, Atom] = {}
    for payload in payloads:
        for source in (atoms_from_adjudication(payload), discover_atom_objects(payload)):
            for atom_id, atom in source.items():
                atoms[atom_id] = merge_atom(atoms.get(atom_id), atom)
    return atoms


def reference_id(value: Any) -> str | None:
    if isinstance(value, (str, int)) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, Mapping):
        return object_id(value) or next(
            (
                str(value[key])
                for key in ("target", "to", "neighbor", "neighbour", "ref")
                if isinstance(value.get(key), (str, int)) and not isinstance(value.get(key), bool)
            ),
            None,
        )
    return None


def edge_pair(value: Any) -> tuple[str, str] | None:
    if (
        isinstance(value, Sequence)
        and not isinstance(value, (str, bytes))
        and len(value) in (2, 3)
    ):
        left, right = reference_id(value[0]), reference_id(value[1])
        return (left, right) if left is not None and right is not None else None
    if isinstance(value, Mapping):
        for left_key, right_key in EDGE_ENDPOINT_KEYS:
            left, right = reference_id(value.get(left_key)), reference_id(value.get(right_key))
            if left is not None and right is not None:
                return left, right
    return None


def discover_explicit_topology(
    documents: Sequence[InputDocument], atom_ids: set[str]
) -> Discovery:
    candidate_arrays: list[EdgeSource] = []
    edges: set[tuple[str, str]] = set()
    rejected = 0

    def accept(left: str, right: str) -> bool:
        nonlocal rejected
        if left == right or left not in atom_ids or right not in atom_ids:
            rejected += 1
            return False
        edges.add(tuple(sorted((left, right))))
        return True

    def child_path(parent: str, key: Any) -> str:
        text = str(key)
        return f"{parent}.{text}" if text.replace("_", "").isalnum() else f"{parent}[{text!r}]"

    def walk(value: Any, document: InputDocument, path: str) -> None:
        nonlocal rejected
        if isinstance(value, Mapping):
            node = object_id(value)
            for key, child in value.items():
                normalized = str(key).lower()
                location = child_path(path, key)
                if normalized in ALL_RELATION_KEYS and isinstance(child, list):
                    local_edges: set[tuple[str, str]] = set()
                    if node is not None and normalized in NODE_RELATION_KEYS:
                        for item in child:
                            neighbor = reference_id(item)
                            if neighbor is None:
                                rejected += 1
                            elif accept(node, neighbor):
                                local_edges.add(tuple(sorted((node, neighbor))))
                    else:
                        for item in child:
                            pair = edge_pair(item)
                            if pair is None:
                                rejected += 1
                            elif accept(*pair):
                                local_edges.add(tuple(sorted(pair)))
                    candidate_arrays.append(
                        EdgeSource(
                            input_label=document.label,
                            input_path=str(document.path),
                            json_path=location,
                            key=str(key),
                            kind=(
                                "per_atom_adjacency_array"
                                if node is not None and normalized in NODE_RELATION_KEYS
                                else "global_edge_array"
                            ),
                            accepted_edges=tuple(sorted(local_edges)),
                        )
                    )
                elif normalized in ALL_RELATION_KEYS and isinstance(child, Mapping):
                    local_edges = set()
                    direct_pair = edge_pair(child)
                    if direct_pair is not None:
                        if accept(*direct_pair):
                            local_edges.add(tuple(sorted(direct_pair)))
                        kind = "single_edge_mapping"
                    elif node is not None and normalized in NODE_RELATION_KEYS:
                        for neighbor_raw in child:
                            neighbor = reference_id(neighbor_raw)
                            if neighbor is None:
                                rejected += 1
                            elif accept(node, neighbor):
                                local_edges.add(tuple(sorted((node, neighbor))))
                        kind = "per_atom_adjacency_mapping"
                    else:
                        for left_raw, right_values in child.items():
                            nested_pair = edge_pair(right_values)
                            if nested_pair is not None:
                                if accept(*nested_pair):
                                    local_edges.add(tuple(sorted(nested_pair)))
                                continue
                            left = reference_id(left_raw)
                            if left is None or left not in atom_ids:
                                rejected += 1
                                continue
                            if isinstance(right_values, list):
                                candidates = right_values
                            elif isinstance(right_values, Mapping):
                                candidates = list(right_values)
                            else:
                                candidates = [right_values]
                            for right_raw in candidates:
                                right = reference_id(right_raw)
                                if right is None:
                                    rejected += 1
                                elif accept(left, right):
                                    local_edges.add(tuple(sorted((left, right))))
                        kind = "global_adjacency_mapping"
                    candidate_arrays.append(
                        EdgeSource(
                            input_label=document.label,
                            input_path=str(document.path),
                            json_path=location,
                            key=str(key),
                            kind=kind,
                            accepted_edges=tuple(sorted(local_edges)),
                        )
                    )
                elif normalized in ALL_RELATION_KEYS:
                    candidate_arrays.append(
                        EdgeSource(
                            input_label=document.label,
                            input_path=str(document.path),
                            json_path=location,
                            key=str(key),
                            kind=f"rejected_non_array_or_mapping_{type(child).__name__}",
                            accepted_edges=(),
                        )
                    )
                walk(child, document, location)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, document, f"{path}[{index}]")

    for document in documents:
        walk(document.payload, document, "$")
    authenticated = tuple(source for source in candidate_arrays if source.accepted_edges)
    return Discovery(
        candidate_arrays=tuple(candidate_arrays),
        authenticated_edge_arrays=authenticated,
        accepted_explicit_edges=tuple(sorted(edges)),
        rejected_relation_items=rejected,
    )


def adjacency(atom_ids: Iterable[str], edges: Iterable[tuple[str, str]]) -> dict[str, set[str]]:
    graph = {atom_id: set() for atom_id in atom_ids}
    for left, right in edges:
        graph[left].add(right)
        graph[right].add(left)
    return graph


def shortest_q5_path(
    graph: Mapping[str, set[str]],
    atoms: Mapping[str, Atom],
    entries: Iterable[str],
    exits: set[str],
) -> list[str] | None:
    queue: deque[str] = deque()
    parent: dict[str, str | None] = {}
    for node in sorted(set(entries)):
        if atoms[node].q == 5:
            queue.append(node)
            parent[node] = None
    found: str | None = None
    while queue:
        node = queue.popleft()
        if node in exits:
            found = node
            break
        for neighbor in sorted(graph[node]):
            if atoms[neighbor].q == 5 and neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)
    if found is None:
        return None
    path = [found]
    while parent[path[-1]] is not None:
        path.append(str(parent[path[-1]]))
    return list(reversed(path))


def trace_bridge(
    atoms: Mapping[str, Atom],
    graph: Mapping[str, set[str]],
    lower: Decimal,
    upper: Decimal,
    source: str,
) -> BridgeResult:
    q4 = tuple(
        sorted(
            atom.atom_id
            for atom in atoms.values()
            if atom.q == 4 and atom.passes(lower, upper, source)
        )
    )
    q6 = tuple(
        sorted(
            atom.atom_id
            for atom in atoms.values()
            if atom.q == 6 and atom.passes(lower, upper, source)
        )
    )
    q4_contacts = {
        endpoint: tuple(sorted(node for node in graph[endpoint] if atoms[node].q == 5))
        for endpoint in q4
    }
    q6_contacts = {
        endpoint: tuple(sorted(node for node in graph[endpoint] if atoms[node].q == 5))
        for endpoint in q6
    }
    direct = tuple(
        sorted(
            set(node for nodes in q4_contacts.values() for node in nodes)
            & set(node for nodes in q6_contacts.values() for node in nodes)
        )
    )
    best: tuple[str, ...] | None = None
    for left in q4:
        for right in q6:
            middle = shortest_q5_path(
                graph,
                atoms,
                q4_contacts[left],
                set(q6_contacts[right]),
            )
            if middle is None:
                continue
            candidate = tuple([left] + middle + [right])
            if best is None or (len(candidate), candidate) < (len(best), best):
                best = candidate
    return BridgeResult(
        path=best,
        q4_endpoints=q4,
        q6_endpoints=q6,
        q4_q5_contacts=q4_contacts,
        q6_q5_contacts=q6_contacts,
        shared_direct_q5_nodes=direct,
    )


def sector_masses(payloads: Sequence[Any]) -> tuple[dict[int, Decimal], str]:
    for payload in payloads:
        if isinstance(payload, Mapping):
            histories = payload.get("histories")
            if isinstance(histories, Mapping):
                history = histories.get(str(LENGTH), histories.get(LENGTH))
                if isinstance(history, Mapping) and isinstance(history.get("pbar_q"), list):
                    return (
                        {q: Decimal(str(value)) for q, value in enumerate(history["pbar_q"])},
                        "histories[12].pbar_q",
                    )
            raw = payload.get("sector_masses")
            if isinstance(raw, Mapping):
                parsed: dict[int, Decimal] = {}
                for key, value in raw.items():
                    try:
                        parsed[int(key)] = Decimal(str(value))
                    except (InvalidOperation, TypeError, ValueError):
                        continue
                if parsed:
                    return parsed, "sector_masses"
    raise AnalysisRefusal("no L12 sector probability-mass ledger found")


def json_safe(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, Fraction):
        return [value.numerator, value.denominator]
    if isinstance(value, Mapping):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set)):
        return [json_safe(item) for item in value]
    return value


def edge_source_json(source: EdgeSource) -> dict[str, Any]:
    return {
        "input_label": source.input_label,
        "input_path": source.input_path,
        "json_path": source.json_path,
        "key": source.key,
        "kind": source.kind,
        "accepted_edge_count": len(source.accepted_edges),
        "accepted_edges": [list(edge) for edge in source.accepted_edges],
    }


def build_report(
    documents: Sequence[InputDocument],
    lower: Decimal,
    upper: Decimal,
    threshold: Decimal,
    geometry_source: str,
) -> dict[str, Any]:
    payloads = [document.payload for document in documents]
    atoms = merge_atoms(payloads)
    if not atoms:
        raise AnalysisRefusal("no atom/component records discovered")
    incomplete = sorted(
        atom.atom_id
        for atom in atoms.values()
        if atom.q is None
        or atom.target_z is None
        or atom.target_y is None
        or atom.blind_z is None
        or atom.blind_y is None
    )
    discovery = discover_explicit_topology(documents, set(atoms))
    explicit_edges = discovery.accepted_explicit_edges
    report: dict[str, Any] = {
        "schema": SCHEMA,
        "classification": None,
        "L": LENGTH,
        "adjacency_mode": "authenticated_explicit_atom_edges_only",
        "geometry_source": geometry_source,
        "geometry_window": {"z": [str(lower), str(upper)], "y": [str(lower), str(upper)]},
        "inputs": [
            {
                "label": document.label,
                "path": str(document.path),
                "sha256": document.sha256,
            }
            for document in documents
        ],
        "analyzer": {
            "path": str(Path(__file__).resolve()),
            "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
        "schema_discovery": {
            "atom_count": len(atoms),
            "incomplete_atoms": incomplete,
            "candidate_relation_fields": [
                edge_source_json(source) for source in discovery.candidate_arrays
            ],
            "authenticated_edge_fields": [
                edge_source_json(source) for source in discovery.authenticated_edge_arrays
            ],
            "authenticated_edge_field_count": len(discovery.authenticated_edge_arrays),
            "accepted_explicit_edges": [list(edge) for edge in explicit_edges],
            "accepted_explicit_edge_count": len(explicit_edges),
            "rejected_relation_items": discovery.rejected_relation_items,
        },
        "endpoints": None,
        "bridge": {
            "contiguous": False,
            "path": None,
            "path_sectors": None,
        },
        "mass": None,
        "authentication_failure": None,
        "interpretation": "EXPLICIT_ATOM_GRAPH_CONNECTIVITY_ONLY__NOT_A_QUANTUM_ENTANGLEMENT_PROOF",
        "claim_boundary": (
            "READ_ONLY_L12_EXPLORATORY_GRAPH_TRAVERSAL__NO_CHANGE_TO_FROZEN_STAGE6_GATE_"
            "NO_PHASE_CONTINUUM_GRAVITY_OR_ENTANGLEMENT_CLAIM"
        ),
    }
    if not explicit_edges:
        report["classification"] = "AUTHENTICATION_FAILURE"
        report["authentication_failure"] = (
            "AUTHENTICATION_FAILURE: No explicit atom-level topology found in schema."
        )
        return report

    graph = adjacency(atoms, explicit_edges)
    bridge = trace_bridge(atoms, graph, lower, upper, geometry_source)
    report["endpoints"] = {
        "passing_q4": list(bridge.q4_endpoints),
        "passing_q6": list(bridge.q6_endpoints),
        "q4_q5_contacts": {key: list(value) for key, value in bridge.q4_q5_contacts.items()},
        "q6_q5_contacts": {key: list(value) for key, value in bridge.q6_q5_contacts.items()},
        "shared_direct_q5_nodes": list(bridge.shared_direct_q5_nodes),
    }
    if bridge.path is None:
        report["classification"] = "NO_AUTHENTICATED_Q4_Q5_Q6_BRIDGE"
        return report

    report["classification"] = "TOPOLOGICALLY_CONTIGUOUS_Q4_Q5_Q6"
    report["bridge"] = {
        "contiguous": True,
        "path": list(bridge.path),
        "path_sectors": [atoms[node].q for node in bridge.path],
    }
    masses, mass_source = sector_masses(payloads)
    missing_mass = sorted(q for q in (4, 5, 6) if q not in masses)
    if missing_mass:
        raise AnalysisRefusal(f"mass absent for triad sectors {missing_mass}")
    triad_mass = sum((masses[q] for q in (4, 5, 6)), Decimal(0))
    report["mass"] = {
        "source": mass_source,
        "q4": str(masses[4]),
        "q5": str(masses[5]),
        "q6": str(masses[6]),
        "deduplicated_q4_q5_q6": str(triad_mass),
        "threshold": str(threshold),
        "threshold_crossed": triad_mass >= threshold,
    }
    return report


def owner_once_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        payload = (
            json.dumps(json_safe(value), indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            if written <= 0:
                raise AnalysisRefusal("owner-once output write made no progress")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
    finally:
        os.close(descriptor)


def print_report(report: Mapping[str, Any]) -> None:
    discovery = report["schema_discovery"]
    print("L12 STRICT TOPOLOGY BRIDGE ANALYSIS")
    print("Input authentication:")
    for item in report["inputs"]:
        print(f"  {item['label']}: sha256={item['sha256']} path={item['path']}")
    print(f"Schema discovery: atoms={discovery['atom_count']}")
    for source in discovery["candidate_relation_fields"]:
        status = "AUTHENTICATED" if source["accepted_edge_count"] else "REJECTED"
        print(
            "  {} relation field: input={} json_path={} key={} kind={} accepted_edges={}".format(
                status,
                source["input_path"],
                source["json_path"],
                source["key"],
                source["kind"],
                source["accepted_edge_count"],
            )
        )
    if report["authentication_failure"] is not None:
        print(report["authentication_failure"])
        return

    endpoints = report["endpoints"]
    bridge = report["bridge"]
    print(f"Passing q=4 endpoints: {endpoints['passing_q4']}")
    print(f"Passing q=6 endpoints: {endpoints['passing_q6']}")
    print(f"q4 -> q5 contacts: {endpoints['q4_q5_contacts']}")
    print(f"q6 -> q5 contacts: {endpoints['q6_q5_contacts']}")
    print(f"Shared direct q5 nodes: {endpoints['shared_direct_q5_nodes']}")
    print(f"Classification: {report['classification']}")
    if bridge["path"] is None:
        print("Block: Not Topologically Contiguous")
        print("Exact bridge path: NONE")
        print("Mass aggregation: NOT AUTHORIZED (no authenticated bridge)")
        return

    print("Block: Topologically Contiguous")
    print("Exact bridge path: " + " -> ".join(bridge["path"]))
    print("Path sectors: " + " -> ".join(f"q={q}" for q in bridge["path_sectors"]))
    mass = report["mass"]
    print(
        "Deduplicated triad mass: q4={} + q5={} + q6={} = {}".format(
            mass["q4"], mass["q5"], mass["q6"], mass["deduplicated_q4_q5_q6"]
        )
    )
    print(
        "Threshold {} crossed by authenticated bridge: {}".format(
            mass["threshold"], str(mass["threshold_crossed"]).upper()
        )
    )
    print(f"Interpretation: {report['interpretation']}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adjudication", type=Path, default=DEFAULT_ADJUDICATION)
    parser.add_argument("--adjudication-sha256", default=DEFAULT_ADJUDICATION_SHA256)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--manifest-sha256", default=DEFAULT_MANIFEST_SHA256)
    parser.add_argument("--target-history", type=Path, default=DEFAULT_TARGET_HISTORY)
    parser.add_argument("--target-history-sha256", default=DEFAULT_TARGET_HISTORY_SHA256)
    parser.add_argument("--hostile-history", type=Path, default=DEFAULT_HOSTILE_HISTORY)
    parser.add_argument("--hostile-history-sha256", default=DEFAULT_HOSTILE_HISTORY_SHA256)
    parser.add_argument(
        "--target-cache-manifest", type=Path, default=DEFAULT_TARGET_CACHE_MANIFEST
    )
    parser.add_argument(
        "--target-cache-manifest-sha256", default=DEFAULT_TARGET_CACHE_MANIFEST_SHA256
    )
    parser.add_argument(
        "--hostile-cache-manifest", type=Path, default=DEFAULT_HOSTILE_CACHE_MANIFEST
    )
    parser.add_argument(
        "--hostile-cache-manifest-sha256", default=DEFAULT_HOSTILE_CACHE_MANIFEST_SHA256
    )
    parser.add_argument("--topology", type=Path, action="append", default=[])
    parser.add_argument(
        "--topology-sha256",
        action="append",
        default=[],
        help="required once for each --topology file, in the same order",
    )
    parser.add_argument("--geometry-source", choices=("consensus", "target", "blind"), default="consensus")
    parser.add_argument("--lower", default="0.90")
    parser.add_argument("--upper", default="1.10")
    parser.add_argument("--threshold", default="0.50")
    parser.add_argument("--json-output", type=Path)
    arguments = parser.parse_args(argv)
    try:
        lower, upper = Decimal(arguments.lower), Decimal(arguments.upper)
        threshold = Decimal(arguments.threshold)
        if not lower.is_finite() or not upper.is_finite() or lower > upper:
            raise AnalysisRefusal("geometry window is invalid")
        if not threshold.is_finite() or not Decimal(0) <= threshold <= Decimal(1):
            raise AnalysisRefusal("threshold must lie in [0,1]")
        if len(arguments.topology) != len(arguments.topology_sha256):
            raise AnalysisRefusal(
                "each --topology file requires one matching --topology-sha256 value"
            )
        documents = [
            authenticate_json(
                arguments.adjudication.expanduser().resolve(),
                arguments.adjudication_sha256,
                "adjudication",
            ),
            authenticate_json(
                arguments.manifest.expanduser().resolve(),
                arguments.manifest_sha256,
                "manifest",
            ),
            authenticate_json(
                arguments.target_history.expanduser().resolve(),
                arguments.target_history_sha256,
                "target_history",
            ),
            authenticate_json(
                arguments.hostile_history.expanduser().resolve(),
                arguments.hostile_history_sha256,
                "hostile_history",
            ),
            authenticate_json(
                arguments.target_cache_manifest.expanduser().resolve(),
                arguments.target_cache_manifest_sha256,
                "target_cache_manifest",
            ),
            authenticate_json(
                arguments.hostile_cache_manifest.expanduser().resolve(),
                arguments.hostile_cache_manifest_sha256,
                "hostile_cache_manifest",
            ),
        ]
        for index, (path, digest) in enumerate(
            zip(arguments.topology, arguments.topology_sha256), start=1
        ):
            documents.append(
                authenticate_json(
                    path.expanduser().resolve(), digest, f"topology[{index}]"
                )
            )
        report = build_report(
            documents,
            lower,
            upper,
            threshold,
            arguments.geometry_source,
        )
        print_report(report)
        if arguments.json_output is not None:
            output = arguments.json_output.expanduser().resolve()
            owner_once_json(output, report)
            print(f"JSON report: {output}")
        return 0 if report["bridge"]["contiguous"] else 20
    except (AnalysisRefusal, InvalidOperation, OSError, ValueError) as error:
        print(f"L12_TOPOLOGY_BRIDGE_REFUSAL {type(error).__name__}: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
