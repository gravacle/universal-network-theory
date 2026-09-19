#!/usr/bin/env python3
"""Nonphysical compatibility, refusal, and complete-stage preflight for V004R3."""

from __future__ import annotations

import ast
import copy
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

import build_hostile_v004r3_cache as builder
import independent_prefix_history as physical
import independent_prefix_history_v003 as v3
import independent_prefix_history_v004r3 as consumer
import v004r3_common as common


OUTPUT = common.HERE / "V004R3_CACHE_PREFLIGHT_RESULT.json"


class Counter:
    def __init__(self) -> None: self.value = 0
    def require(self, condition: bool, label: str) -> None:
        self.value += 1
        if not condition: raise AssertionError(label)
    def refuses(self, function, label: str) -> None:
        self.value += 1
        try: function()
        except (common.Refusal, OSError, KeyError, TypeError): return
        raise AssertionError(label)


COUNT = Counter()


def freeze_syntax_runtime() -> dict[str, object]:
    freeze = common.validate_freeze()
    for role, path in common.FREEZE_FILES.items():
        COUNT.require(common.sha256(path) == freeze["files"][role], f"frozen role {role}")
        if path.suffix == ".py": ast.parse(path.read_text(encoding="utf-8"), filename=str(path)); COUNT.require(True, f"syntax {role}")
    for relative, digest in common.R2_CUSTODY.items():
        COUNT.require(common.sha256(common.REPO / relative) == digest, f"V004R2 preserved {relative}")
    COUNT.require(sys.version_info[:2] == (3, 9), "current Python runtime changed from audited environment")
    return {"status": "PASS", "python": sys.version.split()[0], "freeze_sha256": common.sha256(common.FREEZE),
            "preserved_v004r2_files": len(common.R2_CUSTODY)}


def exact_index_resource_regression() -> dict[str, object]:
    rank_checks = 0
    for width in range(17):
        for q in range(width + 1):
            words = physical.reverse_masks(width, q)
            COUNT.require(len(words) == math.comb(width, q), "rank basis census")
            for index, word in enumerate(words):
                COUNT.require(v3.reverse_rank(width, q, int(word)) == index, "reverse rank")
                rank_checks += 1
    rng = np.random.default_rng(14441248); edges = physical.hostile_edges(4); differential = 0
    for q in range(5):
        words, offsets, sources, targets = builder.algorithms.operator_arrays(4, q, edges)
        direct = physical.CarrierBlock(4, q, edges)
        cached = consumer.r2consumer.legacy.CachedCarrier(4, q, edges, words, offsets, sources, targets)
        vector = rng.normal(size=(3, len(words))) + 1j * rng.normal(size=(3, len(words)))
        COUNT.require(np.array_equal(words, direct.words.astype("<u4")), "words differential")
        COUNT.require(np.array_equal(cached.multiply(vector), direct.multiply(vector)), "H differential")
        COUNT.require(np.array_equal(cached.currents(vector), direct.currents(vector)), "J differential")
        differential += 3
    for length in common.SUPPORTED:
        COUNT.require(common.calculated_storage(length) == common.FROZEN_STORAGE[str(length)], f"L{length} storage")
        COUNT.require(len(common.expected_specs(length)) == common.FROZEN_STORAGE[str(length)]["array_file_count"], f"L{length} file census")
    return {"status": "PASS", "rank_checks": rank_checks, "L4_H_current_exact_checks": differential,
            "storage_rows": len(common.SUPPORTED)}


def solver() -> dict[str, object]:
    return {"converged": True, "batches": 1, "maximum_degree": 1,
            "maximum_endpoint_difference": 0.0, "maximum_tail_indicator_32": 0.0,
            "algorithm": "RECURRENCE_REPLAY_GL_GROUPS",
            "quadrature_group_max": consumer.r2consumer.legacy.replay.QUADRATURE_GROUP,
            "allocation_vector_slots": consumer.r2consumer.legacy.replay.ALLOCATION_VECTOR_SLOTS,
            "maximum_allocation_estimate_bytes": 0,
            "allocation_limit_bytes": common.NUMERICAL_WORKSPACE_LIMIT}


def history(length: int, cache_hash: str, prerequisites: dict[str, str], freeze: dict[str, object]) -> dict[str, object]:
    rows = []
    for event in range(length):
        row = {key: 0.0 for key in consumer.ROW_KEYS}
        row.update({"event": event + 1, "input_prefix": event,
                    "input_prefix_dimension": math.comb(2 * length + event, event),
                    "logical_output_prefix_dimension": math.comb(2 * length + event + 1, event + 1),
                    "terminal_children_streamed": event == length - 1,
                    "sector_weights": [0.0] * (length + 1), "actual_solver": solver(), "null_solver": solver()})
        rows.append(row)
    comparison = {"resolved": True, "classification": "RESOLVED_PREFIX_HISTORY_CONTROL", "epsilon": 1e-11,
                  "maximum_admission_accounting_residual": 0.0, "maximum_node_continuity_residual_l1": 0.0,
                  "maximum_norm_error": 0.0, "maximum_number_drift": 0.0,
                  "rough_sharp": {"maximum_disagreement": 0.0, "observable_linf": 0.0, "sector_weight_linf": 0.0},
                  "sector": {"density_interval": [0.0, 1.0], "discarded_mass": 0.0, "enclosed_mass": 1.0,
                             "late_events": [], "q_lower": 0, "q_upper": length},
                  "admission_acceptance": [1.0] * length, "routed_acceptance": [1.0] * length,
                  "connector_ratio": [1.0] * length}
    terminal = [{"q": q, "path": f"prefix_{length - 1:02d}/q_{q:02d}.c128",
                 "shape": [math.comb(length - 1, q), math.comb(2 * length, q)],
                 "logical_bytes": 16 * math.comb(length - 1, q) * math.comb(2 * length, q)}
                for q in range(length)]
    return {"schema": "INDEPENDENT_STORAGE_CACHED_PREFIX_HISTORY_V004R3", "L": length,
            "representation": "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_MASKS__IMMUTABLE_STORAGE_INDEX_CACHE",
            "rows": rows, "comparison": comparison, "terminal_shards": terminal,
            "cache_manifest_path": str(common.cache_root(length) / "CACHE_MANIFEST.json"),
            "cache_manifest_sha256": cache_hash,
            "semantic_cache_authentication_checks": consumer.semantic_check_count(length),
            "prerequisite_hashes": prerequisites,
            "resource": {"peak_logical_state_plus_cache_bytes": common.FROZEN_STORAGE[str(length)]["actual_cache_array_bytes"],
                         "scratch_limit_bytes": common.SCRATCH_LIMIT,
                         "maximum_numerical_allocation_estimate_bytes": 0,
                         "numerical_workspace_limit_bytes": common.NUMERICAL_WORKSPACE_LIMIT,
                         "authentication_peak_certificate_bytes": common.FROZEN_STORAGE["12"]["authentication_peak_bytes"],
                         "peak_rss_bytes": 0, "rss_limit_bytes": common.RSS_LIMIT,
                         "wall_seconds_including_authentication": 0.0,
                         "wall_limit_seconds": common.WALL_LIMIT, "passed": True},
            "implementation_sha256": freeze["files"]["consumer"], "method_sha256": freeze["files"]["method"],
            "freeze_sha256": common.sha256(common.FREEZE),
            "claim_boundary": "INDEPENDENT_FINITE_CACHED_PREFIX_HISTORY_ONLY__NO_CONTINUUM_OR_GRAVITY"}


def stage_comparison(schema: str, bindings: dict[str, object]) -> dict[str, object]:
    return {"schema": schema, "classification": "PASS", "resolved": True,
            "history_bindings": bindings, "checks_passed": 1, "checks_total": 1,
            "maximum_observable_difference": 0.0, "maximum_sector_weight_difference": 0.0,
            "tolerance": 1e-8, "claim_boundary": "FINITE_SAME_PATH_COMPARISON_ONLY"}


def expect_mutation_rejected(value, mutate, validate, label: str, rejected: list[str]) -> None:
    bad = copy.deepcopy(value); mutate(bad)
    COUNT.refuses(lambda: validate(bad), f"accepted mutation {label}"); rejected.append(label)


def staged_gate_adversarial() -> dict[str, object]:
    freeze = common.validate_freeze(); dual = "d" * 64
    caches = {str(L): chr(97 + index) * 64 for index, L in enumerate(common.SUPPORTED)}
    control_caches = {str(L): caches[str(L)] for L in common.CONTROL_LENGTHS}
    control_exec = {"schema": "HOSTILE_V004R3_CONTROL_EXECUTION_GATE",
                    "classification": "AUTHORIZE_HOSTILE_V004R3_CONTROLS_L4_L8",
                    "authorized_lengths": list(common.CONTROL_LENGTHS), "cache_manifest_sha256_by_L": control_caches,
                    "output_path_by_L": {str(L): str(common.history_output(L)) for L in common.CONTROL_LENGTHS},
                    "workspace_path_by_L": {str(L): str(common.workspace_root(L)) for L in common.CONTROL_LENGTHS},
                    **consumer.base_gate_hashes(freeze, dual), "claim_boundary": "CONTROL_EXECUTION_AUTHORIZATION_ONLY"}
    consumer.validate_control_execution_document(control_exec, control_caches, freeze, dual); COUNT.require(True, "valid control execution")
    rejected: list[str] = []
    for label, mutate in (("control_output_path", lambda x: x["output_path_by_L"].update({"4": "/tmp/x"})),
                          ("control_cache_hash", lambda x: x["cache_manifest_sha256_by_L"].update({"6": "0" * 64})),
                          ("control_extra_key", lambda x: x.update(extra=True)),
                          ("control_dual_prerequisite", lambda x: x.update(dual_gate_sha256="0" * 64))):
        expect_mutation_rejected(control_exec, mutate,
            lambda x: consumer.validate_control_execution_document(x, control_caches, freeze, dual), label, rejected)
    control_exec_hash = "e" * 64
    control_prereq = {"dual_gate_sha256": dual, "control_execution_gate_sha256": control_exec_hash}
    control_histories = {str(L): (str(L)[0] * 64, history(L, caches[str(L)], control_prereq, freeze))
                         for L in common.CONTROL_LENGTHS}
    bindings = {str(L): consumer.history_binding(L, control_histories[str(L)][0], caches[str(L)]) for L in common.CONTROL_LENGTHS}
    control_compare = stage_comparison("HOSTILE_V004R3_CONTROL_COMPARISON", bindings)
    control_compare_hash = "f" * 64
    control_gate = {"schema": "HOSTILE_V004R3_CONTROL_PASS_GATE",
                    "classification": "PASS_HOSTILE_V004R3_CACHED_CONTROLS_L4_L8",
                    "histories": bindings,
                    "comparison_report": {"path": str(common.CONTROL_COMPARISON), "sha256": control_compare_hash},
                    "prerequisites": control_prereq, **consumer.base_gate_hashes(freeze, dual),
                    "claim_boundary": "FINITE_CONTROL_PASS_ONLY"}
    validate_control = lambda x: consumer.validate_control_pass_document(
        x, control_histories, control_compare_hash, control_compare, control_caches,
        control_exec_hash, freeze, dual)
    validate_control(control_gate); COUNT.require(True, "valid control pass")
    partial = {"schema": "INDEPENDENT_STORAGE_CACHED_PREFIX_HISTORY_V004R3", "L": 4,
               "cache_manifest_sha256": caches["4"], "comparison": {"resolved": True}, "resource": {"passed": True}}
    COUNT.refuses(lambda: consumer.validate_history_document(partial, 4, caches["4"], control_prereq, freeze),
                  "V004R2 blocking partial history accepted"); rejected.append("blocking_partial_history")
    for label, mutate in (("control_history_hash", lambda x: x["histories"]["4"].update(sha256="0" * 64)),
                          ("control_prerequisite", lambda x: x["prerequisites"].update(control_execution_gate_sha256="0" * 64)),
                          ("control_comparison_path", lambda x: x["comparison_report"].update(path="/tmp/x"))):
        expect_mutation_rejected(control_gate, mutate, validate_control, label, rejected)
    for label, mutate in (("history_missing_row_field", lambda x: x["rows"][0].pop("W_n")),
                          ("history_consumer_hash", lambda x: x.update(implementation_sha256="0" * 64)),
                          ("history_prerequisite", lambda x: x["prerequisite_hashes"].update(dual_gate_sha256="0" * 64)),
                          ("history_resource_pass", lambda x: x["resource"].update(passed=False)),
                          ("history_resource_limit", lambda x: x["resource"].update(rss_limit_bytes=1)),
                          ("history_terminal_path", lambda x: x["terminal_shards"][0].update(path="elsewhere")),
                          ("history_unresolved", lambda x: x["comparison"].update(resolved=False)),
                          ("history_nonfinite", lambda x: x["rows"][0].update(W_n=float("nan")))):
        value = control_histories["4"][1]
        expect_mutation_rejected(value, mutate,
            lambda x: consumer.validate_history_document(x, 4, caches["4"], control_prereq, freeze), label, rejected)
    for label, mutate in (("control_comparison_zero_zero", lambda x: x.update(checks_passed=0, checks_total=0)),
                          ("control_comparison_binding", lambda x: x.update(history_bindings={})),
                          ("control_comparison_over_tolerance", lambda x: x.update(maximum_observable_difference=2e-8))):
        expect_mutation_rejected(control_compare, mutate,
            lambda x: consumer.validate_comparison_document(x, "HOSTILE_V004R3_CONTROL_COMPARISON", bindings), label, rejected)
    control_hash = "1" * 64
    l10_exec = {"schema": "HOSTILE_V004R3_L10_EXECUTION_GATE", "classification": "AUTHORIZE_HOSTILE_V004R3_L10",
                "authorized_length": 10, "cache_manifest_sha256": caches["10"],
                "output_path": str(common.history_output(10)), "workspace_path": str(common.workspace_root(10)),
                "prerequisites": {"dual_gate_sha256": dual, "control_pass_gate_sha256": control_hash},
                **consumer.base_gate_hashes(freeze, dual), "claim_boundary": "L10_EXECUTION_AUTHORIZATION_ONLY"}
    validate_l10_exec = lambda x: consumer.validate_l10_execution_document(x, caches["10"], control_hash, freeze, dual)
    validate_l10_exec(l10_exec); COUNT.require(True, "valid L10 execution")
    for label, mutate in (("L10_exec_cache", lambda x: x.update(cache_manifest_sha256="0" * 64)),
                          ("L10_exec_control", lambda x: x["prerequisites"].update(control_pass_gate_sha256="0" * 64)),
                          ("L10_exec_workspace", lambda x: x.update(workspace_path="/tmp/x"))):
        expect_mutation_rejected(l10_exec, mutate, validate_l10_exec, label, rejected)
    l10_exec_hash = "2" * 64
    l10_prereq = {"dual_gate_sha256": dual, "control_pass_gate_sha256": control_hash,
                  "L10_execution_gate_sha256": l10_exec_hash}
    l10_history = history(10, caches["10"], l10_prereq, freeze); l10_history_hash = "3" * 64
    l10_binding = consumer.history_binding(10, l10_history_hash, caches["10"])
    l10_compare = stage_comparison("HOSTILE_V004R3_L10_COMPARISON", {"10": l10_binding}); l10_compare_hash = "4" * 64
    l10_gate = {"schema": "HOSTILE_V004R3_L10_PASS_GATE", "classification": "PASS_HOSTILE_V004R3_CACHED_L10",
                "history": l10_binding, "comparison_report": {"path": str(common.L10_COMPARISON), "sha256": l10_compare_hash},
                "prerequisites": l10_prereq, **consumer.base_gate_hashes(freeze, dual),
                "claim_boundary": "FINITE_L10_PASS_ONLY"}
    validate_l10 = lambda x: consumer.validate_l10_pass_document(x, l10_history_hash, l10_history,
        l10_compare_hash, l10_compare, caches["10"], control_hash, l10_exec_hash, freeze, dual)
    validate_l10(l10_gate); COUNT.require(True, "valid L10 pass")
    for label, mutate in (("L10_pass_history_hash", lambda x: x["history"].update(sha256="0" * 64)),
                          ("L10_pass_comparison_hash", lambda x: x["comparison_report"].update(sha256="0" * 64)),
                          ("L10_pass_exec_prerequisite", lambda x: x["prerequisites"].update(L10_execution_gate_sha256="0" * 64))):
        expect_mutation_rejected(l10_gate, mutate, validate_l10, label, rejected)
    COUNT.refuses(lambda: consumer.validate_comparison_document(
        dict(l10_compare, checks_passed=0, checks_total=0), "HOSTILE_V004R3_L10_COMPARISON", {"10": l10_binding}),
        "L10 0/0 comparison accepted"); rejected.append("L10_comparison_zero_zero")
    l10_hash = "5" * 64; target_hash = "6" * 64; parallel_hash = "7" * 64
    parallel_gate = {"schema": "HOSTILE_V004R3_PARALLEL_L12_EXECUTION_GATE",
        "classification": "AUTHORIZE_CONTEMPORANEOUS_TARGET_V005_HOSTILE_V004R3_L12",
        "authorized_length": 12,
        "schedule": {"mode": common.PARALLEL_L12_CERTIFICATE["execution_mode"],
                     "target_role": "TARGET_V005", "hostile_role": "HOSTILE_V004R3",
                     "launch_skew_seconds_max": 60, "launch_only_after_both_L10_pass": True},
        "resource_certificate": common.PARALLEL_L12_CERTIFICATE,
        "telemetry": {"path": str(common.PARALLEL_L12_TELEMETRY),
                      "required_fields": common.PARALLEL_L12_CERTIFICATE["telemetry_required_fields"],
                      "must_be_absent_before_launch": True, "sample_interval_seconds_max": 60},
        "prerequisites": {"dual_gate_sha256": dual, "control_pass_gate_sha256": control_hash,
                          "hostile_L10_pass_gate_sha256": l10_hash, "target_gate_sha256": target_hash},
        **consumer.base_gate_hashes(freeze, dual),
        "claim_boundary": "PARALLEL_L12_SCHEDULING_AND_RESOURCE_AUTHORIZATION_ONLY"}
    validate_parallel = lambda x: consumer.validate_parallel_l12_document(x, control_hash, l10_hash,
                                                                           target_hash, freeze, dual)
    validate_parallel(parallel_gate); COUNT.require(True, "valid parallel L12 gate")
    for label, mutate in (("parallel_combined_peak", lambda x: x["resource_certificate"].update(combined_conservative_rss_plus_mapped_peak_bytes=1)),
                          ("parallel_per_process_limit", lambda x: x["resource_certificate"].update(per_process_rss_limit_bytes=1)),
                          ("parallel_L10_prerequisite", lambda x: x["prerequisites"].update(hostile_L10_pass_gate_sha256="0" * 64)),
                          ("parallel_telemetry_path", lambda x: x["telemetry"].update(path="/tmp/x")),
                          ("parallel_launch_order", lambda x: x["schedule"].update(launch_only_after_both_L10_pass=False))):
        expect_mutation_rejected(parallel_gate, mutate, validate_parallel, label, rejected)
    l12_gate = {"schema": "HOSTILE_V004R3_L12_EXECUTION_GATE", "classification": "AUTHORIZE_HOSTILE_V004R3_L12",
                "authorized_length": 12, "cache_manifest_sha256": caches["12"],
                "output_path": str(common.history_output(12)), "workspace_path": str(common.workspace_root(12)),
                "prerequisites": {"dual_gate_sha256": dual, "control_pass_gate_sha256": control_hash,
                                  "L10_pass_gate_sha256": l10_hash, "target_gate_sha256": target_hash,
                                  "parallel_L12_execution_gate_sha256": parallel_hash},
                "target_prerequisite": {"path": str(common.REPO / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/TARGET_L12_GATE_V004.json"),
                                        "sha256": target_hash, "classification": "PASS_TARGET_Q_SHARDED_L4_L10_GATE_V004",
                                        "checks_passed": 273, "checks_total": 273},
                **consumer.base_gate_hashes(freeze, dual), "claim_boundary": "L12_EXECUTION_AUTHORIZATION_ONLY"}
    validate_l12 = lambda x: consumer.validate_l12_execution_document(x, caches["12"], control_hash, l10_hash,
                                                                       target_hash, freeze, dual, parallel_hash)
    validate_l12(l12_gate); COUNT.require(True, "valid L12 execution")
    for label, mutate in (("L12_target_zero", lambda x: x["target_prerequisite"].update(checks_passed=0, checks_total=0)),
                          ("L12_target_hash", lambda x: x["target_prerequisite"].update(sha256="0" * 64)),
                          ("L12_target_chain", lambda x: x["prerequisites"].update(target_gate_sha256="0" * 64)),
                          ("L12_L10_chain", lambda x: x["prerequisites"].update(L10_pass_gate_sha256="0" * 64)),
                          ("L12_parallel_chain", lambda x: x["prerequisites"].update(parallel_L12_execution_gate_sha256="0" * 64)),
                          ("L12_output_path", lambda x: x.update(output_path="/tmp/x"))):
        expect_mutation_rejected(l12_gate, mutate, validate_l12, label, rejected)
    return {"status": "PASS", "valid_stage_documents": 5,
            "rejected_adversarial_cases": len(rejected), "rejected_cases": rejected}


def dual_manifest_and_hard_locks() -> dict[str, object]:
    dual = common.valid_dual_gate_template(); common.validate_dual_gate_data(dual); COUNT.require(True, "valid dual")
    rejected = 0
    for mutate in (lambda x: x["obstruction_records"][1].update(role="target"),
                   lambda x: x.update(consumer_sha256="0" * 64),
                   lambda x: x.update(authorized_lengths=[4]),
                   lambda x: x.update(extra=True)):
        bad = copy.deepcopy(dual); mutate(bad); COUNT.refuses(lambda value=bad: common.validate_dual_gate_data(value), "dual mutation"); rejected += 1
    specs = common.expected_specs(4); manifest = {"files": [dict(row, sha256="0" * 64) for row in specs],
        "array_file_count": len(specs), "manifest_inclusive_file_count": len(specs) + 1,
        "payload": common.FROZEN_STORAGE["4"]}
    common.validate_manifest_record_census(manifest, 4); COUNT.require(True, "valid manifest")
    for mutate in (lambda x: x["files"].pop(), lambda x: x["files"][0].update(path="../x"),
                   lambda x: x.update(array_file_count=0)):
        bad = copy.deepcopy(manifest); mutate(bad); COUNT.refuses(lambda value=bad: common.validate_manifest_record_census(value, 4), "manifest mutation"); rejected += 1
    gates = (common.DUAL_GATE, common.CONTROL_EXECUTION_GATE, common.CONTROL_GATE,
             common.L10_EXECUTION_GATE, common.L10_GATE, common.L12_EXECUTION_GATE,
             common.PARALLEL_L12_GATE)
    paths = (common.CACHE_PARENT, common.HISTORY_PARENT, common.WORKSPACE_PARENT)
    COUNT.require(all(not path.exists() for path in gates + paths), "future gate/output exists")
    build = subprocess.run([sys.executable, str(common.BUILDER), "--length", "4"], cwd=common.HERE,
                           capture_output=True, text=True, check=False)
    consume = subprocess.run([sys.executable, str(common.CONSUMER), "execute", "--length", "4"], cwd=common.HERE,
                             capture_output=True, text=True, check=False)
    COUNT.require(build.returncode == consume.returncode == 2, "hard lock return code")
    COUNT.require(all(not path.exists() for path in paths), "hard lock created output")
    with tempfile.TemporaryDirectory(prefix="v004r3-runtime-") as temporary:
        root = Path(temporary); root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            spec = {"path": "probe.u32", "dtype": "<u4", "shape": [2], "bytes": 8,
                    "kind": "runtime_probe", "role": "probe"}
            record = builder.raw_write(root_fd, root, spec, np.asarray([1, 2], dtype="<u4"))
            COUNT.require(record["bytes"] == 8 and len(record["sha256"]) == 64,
                          "runtime stable-write probe failed")
            COUNT.require((root / "probe.u32").lstat().st_mode & 0o222 == 0,
                          "runtime stable-write mode failed")
        finally:
            os.close(root_fd)
    return {"status": "PASS", "dual_manifest_mutations_rejected": rejected,
            "future_gates_absent": len(gates), "builder_returncode": 2, "consumer_returncode": 2,
            "cache_workspace_history_created": False, "runtime_stable_write_probe": "PASS_ON_CURRENT_PYTHON"}


def main() -> int:
    if OUTPUT.exists(): raise FileExistsError("refuse overwrite V004R3 preflight")
    result: dict[str, object] = {"schema": "HOSTILE_V004R3_STRICT_STAGED_GATE_NONPHYSICAL_PREFLIGHT",
        "cache_payload_created": False, "physical_history_executed": False,
        "V004R2_bytes_modified": False, "tests": {}}
    try:
        result["tests"] = {"freeze_syntax_runtime": freeze_syntax_runtime(),
                           "exact_index_resource_regression": exact_index_resource_regression(),
                           "staged_gate_adversarial": staged_gate_adversarial(),
                           "dual_manifest_hard_locks": dual_manifest_and_hard_locks()}
        result["checks_passed"] = COUNT.value; result["checks_total"] = COUNT.value
        result["classification"] = "PASS_V004R3_STRICT_STAGED_GATE_PREFLIGHT__ALL_PHYSICAL_MODES_LOCKED"
    except Exception as error:
        result["checks_passed"] = max(0, COUNT.value - 1); result["checks_total"] = COUNT.value
        result["classification"] = "FAIL_V004R3_STRICT_STAGED_GATE_PREFLIGHT"
        result["error"] = f"{type(error).__name__}: {error}"
    fd = os.open(OUTPUT, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
    return 0 if result["classification"].startswith("PASS") else 2


if __name__ == "__main__": raise SystemExit(main())
