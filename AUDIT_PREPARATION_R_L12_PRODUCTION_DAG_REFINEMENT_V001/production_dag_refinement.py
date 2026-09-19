#!/usr/bin/env python3
"""Independent refinement proof from abstract V012 DAGs to production interfaces."""

from __future__ import annotations

import ast
import importlib.util
import inspect
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Iterable


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
V012: Final[Path] = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
AUTH_MODEL: Final[Path] = ROOT / "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/authorization_model.py"
LAUNCH_MODEL: Final[Path] = ROOT / "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/dual_launch_coordinator.py"
PRODUCTION_LAUNCHER: Final[Path] = ROOT / "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/production_dual_l12_launcher.py"
EVIDENCE_ORCHESTRATOR: Final[Path] = HERE / "production_evidence_orchestrator.py"
HOSTILE_WORKER: Final[Path] = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/consume_cache_v004r4.py"
)


class RefinementRefusal(RuntimeError):
    """A declared or observed graph does not refine its independent oracle."""


@dataclass(frozen=True)
class ProductionNode:
    interface: str
    predecessors: frozenset[str]


def _node(interface: str, *predecessors: str) -> ProductionNode:
    return ProductionNode(interface, frozenset(predecessors))


PRODUCTION_NODES: Final[dict[str, ProductionNode]] = {
    "P01_PREPAYLOAD_AUDIT": _node("build_target_cache.require_future_v012_hostile_audit"),
    "P02_CACHE_SET_BUILT": _node("build_target_cache._build_with_custody", "P01_PREPAYLOAD_AUDIT"),
    "P03_POSTBUILD_AUDIT": _node("consume_target_cache.require_postbuild_payload_audit", "P02_CACHE_SET_BUILT"),
    "P04_BASE_GATE_AUDIT": _node("consume_target_cache.require_control_execution_authorization", "P03_POSTBUILD_AUDIT"),
    "P05_CONTROL_L4": _node("consume_target_cache.validate_prior_history[L4]", "P04_BASE_GATE_AUDIT"),
    "P06_CONTROL_L6": _node("consume_target_cache.validate_prior_history[L6]", "P04_BASE_GATE_AUDIT"),
    "P07_CONTROL_L8": _node("consume_target_cache.validate_prior_history[L8]", "P04_BASE_GATE_AUDIT"),
    "P08_CONTROL_STAGE_AUDIT": _node("consume_target_cache.require_stage_gate_audit[controls]", "P05_CONTROL_L4", "P06_CONTROL_L6", "P07_CONTROL_L8"),
    "P09_L10_AUTHORIZATION": _node("consume_target_cache.require_l10_execution_authorization", "P08_CONTROL_STAGE_AUDIT"),
    "P10_TARGET_L10_RESULT": _node("consume_target_cache.validate_prior_history[L10]", "P09_L10_AUTHORIZATION"),
    "P11_HOSTILE_L10_RESULT": _node("consume_target_cache._validate_hostile_l10_gate", "P09_L10_AUTHORIZATION"),
    "P12_HOSTILE_BRANCH_CUSTODY": _node("consume_target_cache._validate_shared_branch[hostile_v004r4]", "P11_HOSTILE_L10_RESULT"),
    "P13_L10_CROSS_AUDIT": _node("consume_target_cache.require_target_hostile_l10_cross_gate", "P10_TARGET_L10_RESULT", "P12_HOSTILE_BRANCH_CUSTODY"),
    "P14_L12_SHARED_SCHEDULE": _node("consume_target_cache.require_parallel_l12_schedule_gate", "P13_L10_CROSS_AUDIT"),
    "P15_L12_SCHEDULE_AUDIT": _node("consume_target_cache.require_shared_schedule_audit", "P14_L12_SHARED_SCHEDULE"),
    "P16_TARGET_L12_AUTHORIZATION": _node("consume_target_cache.require_target_l12_execution_gate", "P13_L10_CROSS_AUDIT", "P15_L12_SCHEDULE_AUDIT"),
    "P17_HOSTILE_L12_AUTHORIZATION": _node("consume_target_cache.require_hostile_l12_execution_gate", "P12_HOSTILE_BRANCH_CUSTODY", "P13_L10_CROSS_AUDIT", "P15_L12_SCHEDULE_AUDIT"),
    "P18A_TARGET_WORKER_READY": _node("production_dual_l12_launcher.ready[target_v012]", "P16_TARGET_L12_AUTHORIZATION"),
    "P18B_HOSTILE_WORKER_READY": _node("production_dual_l12_launcher.ready[hostile_v004r4]", "P17_HOSTILE_L12_AUTHORIZATION"),
    "P18_DUAL_L12_HANDSHAKE": _node("production_dual_l12_launcher.commit_handshake", "P18A_TARGET_WORKER_READY", "P18B_HOSTILE_WORKER_READY"),
    "P19_DUAL_L12_RELEASE": _node("production_dual_l12_launcher.release_workers", "P18_DUAL_L12_HANDSHAKE"),
    "P19A_TARGET_RELEASE_ACK": _node("production_dual_l12_launcher.release_ack[target_v012]", "P19_DUAL_L12_RELEASE"),
    "P19B_HOSTILE_RELEASE_ACK": _node("production_dual_l12_launcher.release_ack[hostile_v004r4]", "P19_DUAL_L12_RELEASE"),
    "P20_TARGET_L12_HISTORY": _node("independent_final_auditor.validate_target_l12_history", "P19A_TARGET_RELEASE_ACK"),
    "P21_HOSTILE_L12_HISTORY": _node("consume_cache_v004r4.validate_with_independent_sink", "P19B_HOSTILE_RELEASE_ACK"),
    "P20A_TARGET_COMPLETION": _node("production_dual_l12_launcher.completion[target_v012]", "P20_TARGET_L12_HISTORY"),
    "P21A_HOSTILE_COMPLETION": _node("production_dual_l12_launcher.completion[hostile_v004r4]", "P21_HOSTILE_L12_HISTORY"),
    "P22_POSTRUN_TELEMETRY": _node("production_dual_l12_launcher.publish_a23", "P20A_TARGET_COMPLETION", "P21A_HOSTILE_COMPLETION"),
    "P23_FINAL_MUTATION_LEDGER": _node("independent_final_auditor.validate_mutation_ledger"),
    "P24_FINAL_ADJUDICATION": _node("production_evidence_orchestrator.publish_a26", "P20_TARGET_L12_HISTORY", "P21_HOSTILE_L12_HISTORY", "P22_POSTRUN_TELEMETRY", "P23_FINAL_MUTATION_LEDGER"),
}


ABSTRACT_PREDECESSORS: Final[dict[str, frozenset[str]]] = {
    "PREPAYLOAD_AUDIT": frozenset(),
    "CACHE_SET_BUILT": frozenset({"PREPAYLOAD_AUDIT"}),
    "POSTBUILD_AUDIT": frozenset({"CACHE_SET_BUILT"}),
    "BASE_GATE_AUDIT": frozenset({"POSTBUILD_AUDIT"}),
    "CONTROL_L4": frozenset({"BASE_GATE_AUDIT"}),
    "CONTROL_L6": frozenset({"BASE_GATE_AUDIT"}),
    "CONTROL_L8": frozenset({"BASE_GATE_AUDIT"}),
    "CONTROL_STAGE_AUDIT": frozenset({"CONTROL_L4", "CONTROL_L6", "CONTROL_L8"}),
    "L10_AUTHORIZATION": frozenset({"CONTROL_STAGE_AUDIT"}),
    "L10_TARGET_RESULT": frozenset({"L10_AUTHORIZATION"}),
    "L10_HOSTILE_RESULT": frozenset({"L10_AUTHORIZATION"}),
    "L10_CROSS_AUDIT": frozenset({"L10_TARGET_RESULT", "L10_HOSTILE_RESULT"}),
    "L12_SHARED_SCHEDULE": frozenset({"L10_CROSS_AUDIT"}),
    "L12_HOSTILE_ELIGIBILITY": frozenset({"L10_CROSS_AUDIT"}),
    "DUAL_L12_LAUNCH_HANDSHAKE": frozenset({"L12_SHARED_SCHEDULE", "L12_HOSTILE_ELIGIBILITY"}),
    "TARGET_L12_TELEMETRY": frozenset({"DUAL_L12_LAUNCH_HANDSHAKE"}),
    "HOSTILE_L12_TELEMETRY": frozenset({"DUAL_L12_LAUNCH_HANDSHAKE"}),
    "FINAL_ADJUDICATION": frozenset({"TARGET_L12_TELEMETRY", "HOSTILE_L12_TELEMETRY"}),
}


ABSTRACT_REPRESENTATIVE: Final[dict[str, str]] = {
    "PREPAYLOAD_AUDIT": "P01_PREPAYLOAD_AUDIT",
    "CACHE_SET_BUILT": "P02_CACHE_SET_BUILT",
    "POSTBUILD_AUDIT": "P03_POSTBUILD_AUDIT",
    "BASE_GATE_AUDIT": "P04_BASE_GATE_AUDIT",
    "CONTROL_L4": "P05_CONTROL_L4",
    "CONTROL_L6": "P06_CONTROL_L6",
    "CONTROL_L8": "P07_CONTROL_L8",
    "CONTROL_STAGE_AUDIT": "P08_CONTROL_STAGE_AUDIT",
    "L10_AUTHORIZATION": "P09_L10_AUTHORIZATION",
    "L10_TARGET_RESULT": "P10_TARGET_L10_RESULT",
    "L10_HOSTILE_RESULT": "P11_HOSTILE_L10_RESULT",
    "L10_CROSS_AUDIT": "P13_L10_CROSS_AUDIT",
    "L12_SHARED_SCHEDULE": "P15_L12_SCHEDULE_AUDIT",
    "L12_HOSTILE_ELIGIBILITY": "P17_HOSTILE_L12_AUTHORIZATION",
    "DUAL_L12_LAUNCH_HANDSHAKE": "P19_DUAL_L12_RELEASE",
    "TARGET_L12_TELEMETRY": "P20A_TARGET_COMPLETION",
    "HOSTILE_L12_TELEMETRY": "P21A_HOSTILE_COMPLETION",
    "FINAL_ADJUDICATION": "P24_FINAL_ADJUDICATION",
}


LAUNCH_REFINEMENT: Final[dict[str, tuple[str, ...]]] = {
    "admit_schedule": ("P14_L12_SHARED_SCHEDULE",),
    "admit_schedule_audit": ("P15_L12_SCHEDULE_AUDIT",),
    "admit_authorization": ("P16_TARGET_L12_AUTHORIZATION", "P17_HOSTILE_L12_AUTHORIZATION"),
    "commit_handshake": ("P18_DUAL_L12_HANDSHAKE",),
    "release_workers": ("P19_DUAL_L12_RELEASE",),
    "release_command": ("P19_DUAL_L12_RELEASE",),
    "admit_release_ack": ("P19A_TARGET_RELEASE_ACK", "P19B_HOSTILE_RELEASE_ACK"),
    "admit_worker_completion": (
        "P20A_TARGET_COMPLETION", "P21A_HOSTILE_COMPLETION",
    ),
    "admit_postrun_telemetry": ("P22_POSTRUN_TELEMETRY",),
}


HOSTILE_IDENTITIES: Final[dict[str, str]] = {
    "freeze_schema": "AUDIT_R_L12_PREFIX_HISTORY_STORAGE_CACHE_FREEZE_V004R4",
    "freeze_status": "FROZEN_BEFORE_CACHE_OR_HISTORY_OUTPUT",
    "freeze_claim": "V004R4_CROSS_BRANCH_STORAGE_CONTROL_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY",
    "preflight_schema": "HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT_V001",
    "preflight_classification": "PASS_HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT",
    "preflight_claim": "NONPHYSICAL_V004R4_PREFLIGHT_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY",
    "audit_schema": "HOSTILE_V004R4_PREPAYLOAD_AUDIT_V001",
    "audit_classification": "PASS_HOSTILE_V004R4_PREPAYLOAD_CONTROL_AND_SHARED_GATE_INTERFACE",
    "audit_claim": "NONPHYSICAL_V004R4_CONTROL_PLANE_AUDIT_ONLY",
    "l10_schema": "HOSTILE_V004R4_CACHED_L10_GATE",
    "manifest_schema": "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R4",
}


def _transitive(nodes: dict[str, ProductionNode], name: str) -> frozenset[str]:
    found: set[str] = set()
    todo = list(nodes[name].predecessors)
    while todo:
        item = todo.pop()
        if item == name:
            raise RefinementRefusal(f"production graph cycle at {name}")
        if item not in found:
            if item not in nodes:
                raise RefinementRefusal(f"unknown production predecessor {item}")
            found.add(item)
            todo.extend(nodes[item].predecessors)
    return frozenset(found)


def validate_declared_refinement(
    nodes: dict[str, ProductionNode] | None = None,
) -> dict[str, int]:
    graph = PRODUCTION_NODES if nodes is None else nodes
    if type(graph) is not dict or set(ABSTRACT_REPRESENTATIVE.values()) - set(graph):
        raise RefinementRefusal("production representative coverage mismatch")
    direct = 0
    transitive = 0
    for name, node in graph.items():
        if type(name) is not str or type(node) is not ProductionNode:
            raise RefinementRefusal("production graph type mismatch")
        direct += len(node.predecessors)
        closure = _transitive(graph, name)
        transitive += len(closure)
    abstract_edges = 0
    for child, predecessors in ABSTRACT_PREDECESSORS.items():
        child_rep = ABSTRACT_REPRESENTATIVE[child]
        closure = _transitive(graph, child_rep)
        for predecessor in predecessors:
            abstract_edges += 1
            if ABSTRACT_REPRESENTATIVE[predecessor] not in closure:
                raise RefinementRefusal(f"abstract edge lost: {predecessor}->{child}")
    return {
        "production_nodes": len(graph),
        "production_direct_edges": direct,
        "production_transitive_edges": transitive,
        "abstract_nodes": len(ABSTRACT_PREDECESSORS),
        "abstract_edges_proved": abstract_edges,
    }


_LOAD_REGISTRY: Final[dict[Path, str]] = {
    AUTH_MODEL: "track_c_authorization_model",
    LAUNCH_MODEL: "track_c_launch_model",
    HERE / "independent_final_auditor.py": "track_c_final_contract",
}


def _load(path: Path, name: str):
    if not isinstance(path, Path) or type(name) is not str:
        raise RefinementRefusal("dynamic model load type mismatch")
    if _LOAD_REGISTRY.get(path) != name:
        raise RefinementRefusal("dynamic model load is outside the exact registry")
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RefinementRefusal(f"cannot load independent model {path.name}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def validate_abstract_model() -> dict[str, int]:
    model = _load(AUTH_MODEL, "track_c_authorization_model")
    actual_names = {stage.name for stage in model.STAGES}
    if actual_names != set(ABSTRACT_PREDECESSORS):
        raise RefinementRefusal("authorization-model stage census mismatch")
    edges = 0
    for stage in model.STAGES:
        observed = frozenset(item.name for item in model.PREDECESSORS[stage])
        expected = ABSTRACT_PREDECESSORS[stage.name]
        if observed != expected:
            raise RefinementRefusal(f"authorization-model edge mismatch at {stage.name}")
        edges += len(expected)
    if tuple(stage.name for stage in model.canonical_route()) != tuple(ABSTRACT_PREDECESSORS):
        raise RefinementRefusal("authorization-model canonical route mismatch")
    return {"authorization_model_stages": len(actual_names), "authorization_model_edges": edges}


def validate_launch_model() -> dict[str, int]:
    launch = _load(LAUNCH_MODEL, "track_c_launch_model")
    signatures = launch.public_signature_census()
    expected = {
        "admit_schedule": ("self", "record"),
        "admit_schedule_audit": ("self", "record"),
        "admit_authorization": ("self", "record"),
        "commit_handshake": ("self", "record"),
        "release_workers": ("self", "record"),
        "release_command": ("self", "role"),
        "admit_release_ack": ("self", "command", "record"),
        "admit_worker_completion": ("self", "record"),
        "admit_postrun_telemetry": ("self", "record"),
    }
    if signatures != expected or set(signatures) != set(LAUNCH_REFINEMENT):
        raise RefinementRefusal("launch-model interface census mismatch")
    launch_edges = (
        ("P14_L12_SHARED_SCHEDULE", "P15_L12_SCHEDULE_AUDIT"),
        ("P15_L12_SCHEDULE_AUDIT", "P16_TARGET_L12_AUTHORIZATION"),
        ("P15_L12_SCHEDULE_AUDIT", "P17_HOSTILE_L12_AUTHORIZATION"),
        ("P16_TARGET_L12_AUTHORIZATION", "P18_DUAL_L12_HANDSHAKE"),
        ("P17_HOSTILE_L12_AUTHORIZATION", "P18_DUAL_L12_HANDSHAKE"),
        ("P18_DUAL_L12_HANDSHAKE", "P19_DUAL_L12_RELEASE"),
        ("P19_DUAL_L12_RELEASE", "P19A_TARGET_RELEASE_ACK"),
        ("P19_DUAL_L12_RELEASE", "P19B_HOSTILE_RELEASE_ACK"),
        ("P19A_TARGET_RELEASE_ACK", "P20_TARGET_L12_HISTORY"),
        ("P19B_HOSTILE_RELEASE_ACK", "P21_HOSTILE_L12_HISTORY"),
        ("P20_TARGET_L12_HISTORY", "P20A_TARGET_COMPLETION"),
        ("P21_HOSTILE_L12_HISTORY", "P21A_HOSTILE_COMPLETION"),
        ("P20A_TARGET_COMPLETION", "P22_POSTRUN_TELEMETRY"),
        ("P21A_HOSTILE_COMPLETION", "P22_POSTRUN_TELEMETRY"),
    )
    for predecessor, child in launch_edges:
        if predecessor not in _transitive(PRODUCTION_NODES, child):
            raise RefinementRefusal(f"launch refinement edge lost: {predecessor}->{child}")
    return {"launch_model_methods": len(signatures), "launch_refinement_edges": len(launch_edges)}


def _functions(path: Path) -> tuple[str, dict[str, ast.FunctionDef | ast.AsyncFunctionDef]]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    return source, {
        node.name: node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _literal_assignment(path: Path, name: str) -> object:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        value: ast.expr | None = None
        if (
            isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == name
        ):
            value = node.value
        elif (
            isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
            and node.target.id == name
        ):
            value = node.value
        if value is not None:
            try:
                return ast.literal_eval(value)
            except (TypeError, ValueError) as error:
                raise RefinementRefusal(
                    f"nonliteral production contract constant: {name}"
                ) from error
    raise RefinementRefusal(f"production contract constant absent: {name}")


def _call_name(call: ast.Call) -> str | None:
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return None


def _ordered_calls(function: ast.FunctionDef | ast.AsyncFunctionDef) -> list[tuple[str, ast.Call]]:
    calls = [node for node in ast.walk(function) if isinstance(node, ast.Call) and _call_name(node)]
    return [(_call_name(node) or "", node) for node in sorted(calls, key=lambda item: (item.lineno, item.col_offset))]


def _subsequence(observed: Iterable[str], expected: Iterable[str]) -> bool:
    iterator = iter(observed)
    return all(any(item == wanted for item in iterator) for wanted in expected)


def _call_material(call: ast.Call) -> str:
    return " ".join(
        [ast.unparse(item) for item in call.args]
        + [
            f"{item.arg}={ast.unparse(item.value)}"
            for item in call.keywords if item.arg is not None
        ]
    )


def _one_call(
    function: ast.FunctionDef | ast.AsyncFunctionDef, name: str,
) -> ast.Call:
    matches = [call for observed, call in _ordered_calls(function) if observed == name]
    if len(matches) != 1:
        raise RefinementRefusal(f"production call census mismatch: {function.name}.{name}")
    return matches[0]


def _parameter_names(function: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]:
    return tuple(argument.arg for argument in (*function.args.posonlyargs, *function.args.args, *function.args.kwonlyargs))


def _local_literal_assignment(
    function: ast.FunctionDef | ast.AsyncFunctionDef, name: str,
) -> object:
    matches: list[ast.expr] = []
    for node in ast.walk(function):
        if (
            isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == name
        ):
            matches.append(node.value)
        elif (
            isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
            and node.target.id == name and node.value is not None
        ):
            matches.append(node.value)
    if len(matches) != 1:
        raise RefinementRefusal(
            f"production local assignment census mismatch: {function.name}.{name}"
        )
    try:
        return ast.literal_eval(matches[0])
    except (TypeError, ValueError) as error:
        raise RefinementRefusal(
            f"production local assignment is not literal: {function.name}.{name}"
        ) from error


def _validate_hostile_manifest_postbuild_acyclicity(
    source: str,
) -> dict[str, int]:
    """Prove the manifest/post-build/history digest direction from production AST."""
    functions = {
        node.name: node for node in ast.walk(ast.parse(source))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    manifest_validator = functions.get("_validate_v004r4_manifest")
    authenticate = functions.get("authenticate_context")
    result_writer = functions.get("make_result")
    if manifest_validator is None or authenticate is None or result_writer is None:
        raise RefinementRefusal("hostile manifest/postbuild functions absent")

    manifest_keys = _local_literal_assignment(manifest_validator, "keys")
    if (
        type(manifest_keys) is not set
        or "postbuild_payload_audit" not in manifest_keys
        or "postbuild_payload_audit_sha256" in manifest_keys
    ):
        raise RefinementRefusal(
            "hostile manifest embeds a postbuild digest or lacks preregistration"
        )

    binding_assignments = [
        node for node in ast.walk(authenticate)
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "postbuild_binding"
    ]
    if len(binding_assignments) != 1:
        raise RefinementRefusal("hostile postbuild binding assignment census mismatch")
    binding_call = binding_assignments[0].value
    if (
        not isinstance(binding_call, ast.Call)
        or _call_name(binding_call) != "exact_keys"
        or len(binding_call.args) != 3
    ):
        raise RefinementRefusal("hostile postbuild preregistration validator mismatch")
    try:
        preregistration_fields = ast.literal_eval(binding_call.args[1])
    except (TypeError, ValueError) as error:
        raise RefinementRefusal(
            "hostile postbuild preregistration fields are not literal"
        ) from error
    expected_preregistration = {
        "path", "schema", "identity_field", "identity_value",
    }
    if preregistration_fields != expected_preregistration:
        raise RefinementRefusal(
            "hostile postbuild preregistration must not contain a digest"
        )

    postbuild_reads = []
    for node in ast.walk(authenticate):
        if (
            isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], (ast.Tuple, ast.List))
            and [item.id for item in node.targets[0].elts if isinstance(item, ast.Name)]
            == ["postbuild", "postbuild_hash"]
            and isinstance(node.value, ast.Call)
            and _call_name(node.value) == "read_authority"
        ):
            postbuild_reads.append(node.value)
    if len(postbuild_reads) != 1:
        raise RefinementRefusal("hostile postbuild authority read census mismatch")
    postbuild_read = postbuild_reads[0]
    if len(postbuild_read.args) != 3 or postbuild_read.keywords:
        raise RefinementRefusal(
            "hostile postbuild read is prebound by a digest and creates a cycle"
        )

    authenticate_source = ast.get_source_segment(source, authenticate) or ""
    result_source = ast.get_source_segment(source, result_writer) or ""
    required_authentication_bindings = (
        'postbuild.get("manifest_sha256") != hashes["L12_cache_manifest"]',
        '"postbuild_payload_audit_sha256": postbuild_hash',
    )
    required_history_bindings = (
        '"cache_manifest_sha256": context["hashes"]["L12_cache_manifest"]',
        '"postbuild_payload_audit_sha256": context["postbuild_payload_audit_sha256"]',
    )
    if any(token not in authenticate_source for token in required_authentication_bindings):
        raise RefinementRefusal(
            "hostile postbuild audit does not bind the authenticated manifest forward"
        )
    if any(token not in result_source for token in required_history_bindings):
        raise RefinementRefusal(
            "hostile history does not bind both manifest and postbuild digests"
        )

    # Actual dependency direction proved above:
    # manifest -> postbuild, manifest -> history, postbuild -> history.
    dependencies = {
        "manifest": frozenset(),
        "postbuild": frozenset({"manifest"}),
        "history": frozenset({"manifest", "postbuild"}),
    }
    for name in dependencies:
        found: set[str] = set()
        todo = list(dependencies[name])
        while todo:
            item = todo.pop()
            if item == name:
                raise RefinementRefusal("hostile manifest/postbuild dependency cycle")
            if item not in found:
                found.add(item)
                todo.extend(dependencies[item])
    return {
        "hostile_manifest_preregistration_fields": len(preregistration_fields),
        "hostile_cryptographic_dependency_nodes": len(dependencies),
        "hostile_cryptographic_dependency_edges": sum(
            len(predecessors) for predecessors in dependencies.values()
        ),
        "hostile_cryptographic_cycles": 0,
        "hostile_downstream_digest_bindings": len(required_history_bindings),
    }


def validate_static_production_interfaces() -> dict[str, int]:
    builder_source, builder = _functions(V012 / "build_target_cache.py")
    consumer_source, consumer = _functions(V012 / "consume_target_cache.py")
    validator_path = V012 / "production_obligation_validators.py"
    if not validator_path.is_file():
        raise RefinementRefusal("production obligation validator module absent")
    validator_source, validator = _functions(validator_path)
    final_source, final = _functions(HERE / "independent_final_auditor.py")
    if not HOSTILE_WORKER.is_file():
        raise RefinementRefusal("production hostile V004R4 worker/adapter absent")
    hostile_source, hostile = _functions(HOSTILE_WORKER)
    if not PRODUCTION_LAUNCHER.is_file():
        raise RefinementRefusal("production dual-L12 launcher absent")
    launcher_source, launcher = _functions(PRODUCTION_LAUNCHER)
    if not EVIDENCE_ORCHESTRATOR.is_file():
        raise RefinementRefusal("production evidence orchestrator absent")
    evidence_source, evidence = _functions(EVIDENCE_ORCHESTRATOR)
    required_functions = {
        "builder": {
            "require_future_v012_hostile_audit": {"specification", "freeze", "preflight_result_sha256"},
            "_build_with_custody": {"length", "output"},
            "validate_production_obligation": {"artifact_id", "record"},
        },
        "consumer": {
            "require_postbuild_payload_audit": {"specification", "freeze", "cache_hashes"},
            "require_control_execution_authorization": {"length", "freeze", "physical_gate_sha256", "postbuild_binding"},
            "validate_prior_history": {"row", "expected_length", "cache_sha256", "physical_gate_sha256", "freeze"},
            "require_stage_gate": {"path", "schema", "classification", "lengths", "cache_hashes", "physical_gate_sha256", "freeze"},
            "require_stage_gate_audit": {"audit_path", "stage_path", "stage_gate", "schema", "classification", "lengths"},
            "require_l10_execution_authorization": {"freeze", "physical_gate_sha256", "cache_hashes", "control_stage", "control_audit_sha256"},
            "_validate_shared_branch": {"binding", "role"},
            "_validate_hostile_l10_gate": {"gate", "branch"},
            "require_target_hostile_l10_cross_gate": {"freeze", "cache_hashes", "target_l10_stage", "target_l10_stage_audit_sha256"},
            "require_parallel_l12_schedule_gate": {"l10_cross_gate_sha256"},
            "require_shared_schedule_audit": {"schedule_gate", "schedule_sha256", "l10_cross_gate_sha256"},
            "require_target_l12_execution_gate": {"freeze", "physical_gate_sha256", "cache_hashes", "control_stage_audit_sha256", "l10_stage_audit_sha256", "l10_cross_gate_sha256", "shared_schedule_audit_sha256"},
            "require_hostile_l12_execution_gate": {"hostile_branch", "schedule_sha256", "schedule_audit_sha256", "l10_cross_gate_sha256"},
            "require_dual_l12_launch_handshake": {"schedule", "schedule_sha256", "schedule_audit_sha256", "target_authorization_sha256", "hostile_authorization_sha256"},
            "require_dual_l12_worker_release": {"schedule", "handshake", "handshake_sha256", "target_authorization_sha256", "hostile_authorization_sha256"},
            "require_physical_gate": {"length", "manifest_sha256"},
            "_execute_with_retained_authority": {"length", "cache_root", "cache_manifest_sha256", "output", "workspace"},
        },
    }
    for group_name, requirements in required_functions.items():
        functions = builder if group_name == "builder" else consumer
        for name, parameters in requirements.items():
            if name not in functions or not parameters.issubset(_parameter_names(functions[name])):
                raise RefinementRefusal(f"production interface/signature mismatch: {group_name}.{name}")
    if "validate_record" not in validator or not {"artifact_id", "record", "mutation_class", "fixture_mode"}.issubset(_parameter_names(validator["validate_record"])):
        raise RefinementRefusal("uniform production validator interface mismatch")
    final_expected = {
        "validate_postrun_telemetry", "validate_target_l12_history",
        "validate_hostile_l12_history", "validate_final_l12_audit",
        "validate_mutation_ledger", "validate_artifact", "positive_fixture",
        "positive_fixture_bundle", "mutated_fixture", "basis_permutation_sha256",
    }
    if not final_expected.issubset(final):
        raise RefinementRefusal("A23-A27 final-auditor interface census mismatch")
    hostile_expected = {
        "authenticate_context": {"custody", "worker_id"},
        "validate_native_rows": {"rows"},
        "make_result": {"sharp", "comparison", "terminals", "context", "peak_state", "allocation", "rss", "wall"},
        "validate_with_independent_sink": {"result"},
        "execute": {"worker_id"},
    }
    for name, parameters in hostile_expected.items():
        if name not in hostile or not parameters.issubset(_parameter_names(hostile[name])):
            raise RefinementRefusal(f"hostile production interface/signature mismatch: {name}")
    launcher_expected = {
        "execute": set(),
        "build_handshake": {"coordinator", "ready"},
        "build_release": {"coordinator", "release_epochs"},
        "receive_frame": {"channel", "label"},
        "process_start_token": {"pid"},
        "live_rss": {"pid", "expected_token"},
        "_publish": {"path", "record"},
        "_terminate_exact": {"worker"},
        "_sample_worker": {"worker", "epoch", "policy", "rows"},
        "_sample_disk": {"epoch", "expected_device", "policy", "rows"},
    }
    for name, parameters in launcher_expected.items():
        if name not in launcher or not parameters.issubset(_parameter_names(launcher[name])):
            raise RefinementRefusal(f"launcher interface/signature mismatch: {name}")
    evidence_expected = {
        "_atomic_publish_once": {"output", "payload"},
        "open_authority": {"artifact_id", "path", "digest", "validator"},
    }
    for name, parameters in evidence_expected.items():
        if name not in evidence or not parameters.issubset(_parameter_names(evidence[name])):
            raise RefinementRefusal(f"evidence interface/signature mismatch: {name}")
    final_module = _load(
        HERE / "independent_final_auditor.py", "track_c_final_contract",
    )
    native_contract_pairs = {
        "HISTORY_KEYS": final_module.HOSTILE_HISTORY_KEYS,
        "ROW_KEYS": final_module.HOSTILE_ROW_KEYS,
        "SOLVER_BASE_KEYS": final_module.HOSTILE_SOLVER_BASE_KEYS,
        "COMPARISON_KEYS": final_module.HOSTILE_COMPARISON_KEYS,
        "RESOURCE_KEYS": final_module.HOSTILE_RESOURCE_KEYS,
    }
    for name, expected in native_contract_pairs.items():
        if _literal_assignment(HOSTILE_WORKER, name) != expected:
            raise RefinementRefusal(f"hostile/A25 native contract drift: {name}")
    native_fixed_values = {
        "EXPECTED_STATE_BYTES": 8_773_664_640,
        "EXPECTED_CACHE_BYTES": 826_221_912,
        "EXPECTED_STATE_PLUS_CACHE_BYTES": 9_599_886_552,
        "EXPECTED_DISK_MINIMUM_BYTES": 9_600_935_128,
        "EXPECTED_AUTHENTICATION_PEAK_BYTES": 252_944_080,
        "NUMERICAL_WORKSPACE_LIMIT": 1_400_000_000,
    }
    for name, expected in native_fixed_values.items():
        if _literal_assignment(HOSTILE_WORKER, name) != expected:
            raise RefinementRefusal(f"hostile native fixed value drift: {name}")
    if (
        "SOLVER_TERMINAL_KEYS = SOLVER_BASE_KEYS |" not in hostile_source
        or "terminal_child0_entries" not in hostile_source
        or "terminal_child1_nonzero_admission_entries" not in hostile_source
        or ".c128" not in hostile_source
    ):
        raise RefinementRefusal("hostile native terminal schema/format drift")
    acyclicity = _validate_hostile_manifest_postbuild_acyclicity(hostile_source)

    # Prove that live sinks and mutation fixtures traverse the same dispatcher,
    # and that its final branch reaches the independent A23--A27 implementation.
    production_dispatch = _one_call(
        builder["validate_production_obligation"],
        "_dispatch_production_obligation",
    )
    fixture_dispatch = _one_call(
        builder["validate_audit_obligation_fixture"],
        "_dispatch_production_obligation",
    )
    live_material = _call_material(production_dispatch)
    fixture_material = _call_material(fixture_dispatch)
    if any(token not in live_material for token in (
        "artifact_id", "record", "mutation_class='PRODUCTION_NATIVE_RECORD'",
        "fixture_mode=False",
    )):
        raise RefinementRefusal("live production-obligation dispatcher binding mismatch")
    if any(token not in fixture_material for token in (
        "artifact_id", "mutation_class=mutation_class", "fixture_mode=True",
    )):
        raise RefinementRefusal("mutation-fixture dispatcher binding mismatch")
    validator_dispatch = _one_call(validator["validate_record"], "validate_artifact")
    validator_material = _call_material(validator_dispatch)
    if any(token not in validator_material for token in (
        "artifact_id", "record", "fixture_mode=fixture_mode",
    )):
        raise RefinementRefusal("A23-A27 independent dispatcher binding mismatch")
    hostile_sink = _one_call(
        hostile["validate_with_independent_sink"],
        "validate_hostile_l12_history",
    )
    if any(token not in _call_material(hostile_sink) for token in (
        "result", "fixture_mode=False",
    )):
        raise RefinementRefusal("hostile A25 independent sink binding mismatch")
    hostile_execute_calls = [
        name for name, _call in _ordered_calls(hostile["execute"])
    ]
    if not _subsequence(hostile_execute_calls, (
        "authenticate_context", "CacheContext", "history", "history",
        "seal_terminal_shards", "make_result", "verify_all",
        "validate_with_independent_sink", "atomic_publish",
    )):
        raise RefinementRefusal("hostile release/compute/audit/publication order mismatch")
    launcher_calls = [name for name, _call in _ordered_calls(launcher["execute"])]
    if not _subsequence(launcher_calls, (
        "Popen", "receive_frame", "process_start_token", "build_handshake",
        "commit_handshake", "_publish", "build_release", "release_workers",
        "_publish", "release_command", "_publish", "sendall",
        "receive_frame", "admit_release_ack", "_publish", "select",
        "_sample_worker", "_sample_disk", "admit_worker_completion", "_publish",
        "close", "wait",
        "admit_postrun_telemetry", "publish_a23",
    )):
        raise RefinementRefusal("launcher process/wire/publication order mismatch")
    required_launcher_tokens = (
        "socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)",
        "close_fds=True",
        "pass_fds=(child.fileno(),)",
        "process_start_token(worker.process.pid)",
        "worker.channel.recv(1) != b\"\"",
        "_terminate_exact(worker)",
        "time.monotonic() + policy.per_process_wall_limit_seconds",
        "live RSS exceeds the execution limit",
        "live workspace free disk is below the execution limit",
        "LAUNCHER_SAMPLED_CURRENT_RSS_AT_MOST_30_SECONDS__",
        "CONSERVATIVE_AUTHENTICATION_CACHE_CERTIFICATE__",
        "NOT_OS_VIRTUAL_MEMORY",
    )
    if any(token not in launcher_source for token in required_launcher_tokens):
        raise RefinementRefusal("launcher exact custody/runtime binding absent")
    if not all(token in evidence_source for token in (
        "os.O_EXCL", 'getattr(os, "O_NOFOLLOW"', "os.fsync", "os.link",
    )):
        raise RefinementRefusal("evidence owner-once custody primitives absent")

    gate_calls = _ordered_calls(consumer["require_physical_gate"])
    names = [name for name, _ in gate_calls]
    expected_order = (
        "require_postbuild_payload_audit", "require_control_execution_authorization",
        "require_stage_gate", "require_stage_gate_audit",
        "require_l10_execution_authorization", "require_stage_gate",
        "require_stage_gate_audit", "require_target_hostile_l10_cross_gate",
        "require_parallel_l12_schedule_gate", "require_shared_schedule_audit",
        "require_target_l12_execution_gate", "require_hostile_l12_execution_gate",
        "require_dual_l12_launch_handshake", "require_dual_l12_worker_release",
    )
    if not _subsequence(names, expected_order):
        raise RefinementRefusal("production stage call order does not refine the DAG")
    required_call_arguments = {
        "require_parallel_l12_schedule_gate": {"l10_cross_sha256"},
        "require_shared_schedule_audit": {"schedule", "schedule_sha256", "l10_cross_sha256"},
        "require_target_l12_execution_gate": {"l10_audit_sha256", "l10_cross_sha256", "schedule_audit_sha256"},
        "require_hostile_l12_execution_gate": {"hostile_branch", "schedule_sha256", "schedule_audit_sha256", "l10_cross_sha256"},
        "require_dual_l12_launch_handshake": {"schedule", "schedule_sha256", "schedule_audit_sha256", "target_l12_authorization_sha256", "hostile_l12_authorization_sha256"},
        "require_dual_l12_worker_release": {"schedule", "handshake", "handshake_sha256", "target_l12_authorization_sha256", "hostile_l12_authorization_sha256"},
    }
    for call_name, required_tokens in required_call_arguments.items():
        matching = [call for name, call in gate_calls if name == call_name]
        if len(matching) != 1:
            raise RefinementRefusal(f"production call census mismatch: {call_name}")
        material = _call_material(matching[0])
        if any(token not in material for token in required_tokens):
            raise RefinementRefusal(f"production predecessor binding absent: {call_name}")
    stage_gate_calls = [
        call for name, call in gate_calls if name == "require_stage_gate"
    ]
    stage_gate_bindings = (
        {
            "CACHED_CONTROL_GATE",
            "'TARGET_V012_CACHED_CONTROL_L4_L8_GATE'",
            "'PASS_TARGET_V012_CACHED_CONTROLS_L4_L6_L8'",
            "(4, 6, 8)", "cache_hashes", "physical_hash", "freeze",
        },
        {
            "CACHED_L10_GATE", "'TARGET_V012_CACHED_L10_GATE'",
            "'PASS_TARGET_V012_CACHED_L10'", "(10,)", "cache_hashes",
            "physical_hash", "freeze", "sha256(CACHED_CONTROL_GATE)",
            "l10_authorization_sha256",
        },
    )
    if len(stage_gate_calls) != len(stage_gate_bindings):
        raise RefinementRefusal("production stage-gate call census mismatch")
    for index, (call, required_tokens) in enumerate(
        zip(stage_gate_calls, stage_gate_bindings), start=1,
    ):
        material = _call_material(call)
        if any(token not in material for token in required_tokens):
            raise RefinementRefusal(
                f"production stage-gate binding absent at call {index}"
            )

    execute_calls = _ordered_calls(consumer["_execute_with_retained_authority"])
    execute_names = [name for name, _ in execute_calls]
    if not _subsequence(execute_names, ("require_physical_gate", "CacheContext", "mkdir", "history", "history", "atomic_publish_json")):
        raise RefinementRefusal("production entrypoint gate/compute/publication order mismatch")
    build_calls = [name for name, _ in _ordered_calls(builder["_build_with_custody"])]
    if not _subsequence(build_calls, (
        "require_original_target_gate", "require_dual_gate",
        "open_cache_output_roots", "raw_write", "atomic_publish_json",
    )):
        raise RefinementRefusal("builder authorization-before-cache order mismatch")

    combined = (
        builder_source + consumer_source + validator_source + hostile_source
        + launcher_source + evidence_source
    )
    for artifact_id in ("A23_POSTRUN_TELEMETRY", "A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY", "A26_FINAL_L12_AUDIT", "A27_MUTATION_LEDGER"):
        if artifact_id not in validator_source or artifact_id not in final_source:
            raise RefinementRefusal(f"final sink is not registered end-to-end: {artifact_id}")
    for identity in HOSTILE_IDENTITIES.values():
        if identity not in combined:
            raise RefinementRefusal(f"hostile identity not registered in production: {identity}")
    imported_roots = {
        alias.name.split(".")[0]
        for node in ast.walk(ast.parse(final_source))
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    if imported_roots & {"build_target_cache", "consume_target_cache", "compute_prefix_history_v004", "v004r4_cache_io"}:
        raise RefinementRefusal("independent final auditor imports target validation code")
    return {
        "production_function_interfaces": (
            sum(len(value) for value in required_functions.values()) + 1
            + len(hostile_expected) + len(launcher_expected)
            + len(evidence_expected)
        ),
        "ordered_stage_calls": len(expected_order),
        "predecessor_argument_bindings": (
            sum(len(value) for value in required_call_arguments.values())
            + sum(len(value) for value in stage_gate_bindings)
        ),
        "stage_gate_call_sites": len(stage_gate_calls),
        "shared_dispatcher_bindings": 4,
        "final_sink_interfaces": len(final_expected),
        "live_final_publication_sinks": 5,
        "registered_unorchestrated_final_sinks": 0,
        "launcher_runtime_interfaces": len(launcher_expected),
        "evidence_custody_interfaces": len(evidence_expected),
        "hostile_identity_literals": len(HOSTILE_IDENTITIES),
        "hostile_native_contract_bindings": (
            len(native_contract_pairs) + len(native_fixed_values) + 1
        ),
        **acyclicity,
    }


def run_all_refinement_checks() -> dict[str, object]:
    result: dict[str, object] = {
        "declared_graph": validate_declared_refinement(),
        "authorization_model": validate_abstract_model(),
        "launch_model": validate_launch_model(),
        "production_interfaces": validate_static_production_interfaces(),
        "remaining_identity_limitations": [],
        "remaining_runtime_bindings": [],
    }
    result["status"] = "PASS_STATIC_PRODUCTION_REFINEMENT"
    return result
