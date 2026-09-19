#!/usr/bin/env python3
"""Standalone structural validator for the V012 preregistered audit contract.

This program validates only the preparation packet.  It intentionally does not
import or execute any target, hostile, cache, history, or physics module.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import stat
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
MATRIX = HERE / "AUDIT_OBLIGATIONS_V001.json"
METHOD = HERE / "METHODOLOGY.md"

EXPECTED_TOP_KEYS = {
    "schema", "status", "scope", "independence_contract", "fixed_values",
    "shared_profiles", "mutation_catalog", "V011_findings", "V012_checklist",
    "stages", "artifacts", "coverage_requirements",
}
EXPECTED_CHECKLIST = {
    "C01": "bind V011 obstruction",
    "C02": "repair six exact-type classes",
    "C03": "strict duplicate/nonfinite JSON",
    "C04": "exact five-cache census",
    "C05": "stable immutable gate/audit reads",
    "C06": "split universal custody from control auth",
    "C07": "distinct L10 auth",
    "C08": "distinct target and hostile L12 authorizations followed by blocked-worker handshake and release",
    "C09": "exact typed immutable control/L10 stage gates+claim boundaries",
    "C10": "full canonical history/row/comparison/resource/terminal-shard projection",
    "C11": "compare controls/L10 to sealed V004 deterministic fields and tolerances",
    "C12": "histories preserve full unlock/audit hashes",
    "C13": "independently audited hostile L12 eligibility transitively pins all roles",
    "C14": "exact target/hostile L10 cross-gate",
    "C15": "NORMAL resource snapshot and <=60s dual-worker release skew",
    "C16": "exact postrun telemetry and L12 output hashes",
    "C17": "mutation preflight for all above with reconstructed counts",
    "C18": "independent audits prepayload, postbuild, physical gate, L10 cross, final L12",
}
EXPECTED_V011 = {
    "V011-PREPAYLOAD-AUDIT-CHECKS-PASSED-EXACT-TYPE",
    "V011-POSTBUILD-AUDIT-CHECKS-PASSED-EXACT-TYPE",
    "V011-PHYSICAL-GATE-AUDIT-CHECKS-PASSED-EXACT-TYPE",
    "V011-POSTBUILD-NESTED-CENSUS-EXACT-TYPES",
    "V011-PREPAYLOAD-ABSENCE-CENSUS-EXACT-BOOLEANS",
    "V011-OUTER-AUTHORIZED-LENGTHS-EXACT-INTEGERS",
}
RULE_GROUPS = {
    "schema_rules", "type_rules", "value_rules", "provenance_rules",
    "custody_rules", "reconstruction_rules",
}
REQUIRED_PROFILES = {"STRICT_JSON", "IMMUTABLE_DESCRIPTOR", "HASH_LINEAGE"}
A22_MUTATION_FIXTURE_BY_CLASS = {
    "M01_MISSING_KEY": "PF_A22_TARGET_AUTH",
    "M02_EXTRA_KEY": "PF_A22_HOSTILE_AUTH",
    "M03_WRONG_KEY_SAME_COUNT": "PF_A22_READY",
    "M04_DUPLICATE_JSON_KEY": "PF_A22_TARGET_AUTH",
    "M05_NONFINITE_JSON": "PF_A22_HOSTILE_AUTH",
    "M06_BOOL_FOR_INT": "PF_A22_READY",
    "M07_FLOAT_INT_ALIAS": "PF_A22_COMMAND",
    "M10_IDENTITY_OR_CLAIM": "PF_A22_ACK",
    "M11_HASH_OR_PATH": "PF_A22_READY",
    "M12_SYMLINK_OR_WRITABLE": "PF_A22_HANDSHAKE",
    "M13_DESCRIPTOR_TOCTOU": "PF_A22_RELEASE",
    "M17_PROVENANCE_DROP_SWAP": "PF_A22_HANDSHAKE",
    "M19_STAGE_BYPASS": "PF_A22_HANDSHAKE",
    "M23_HANDSHAKE_TELEMETRY": "PF_A22_ACK",
    "M24_UNLOCK_AUDIT_BINDING": "PF_A22_RELEASE",
    "M28_PREMATURE_ARTIFACT": "PF_A22_ACK",
    "M30_COMPLETION_BOOL_PROCESS_ID": "PF_A22_COMPLETION",
    "M31_COMPLETION_FLOAT_PROCESS_ID": "PF_A22_COMPLETION",
    "M32_COMPLETION_SCHEMA": "PF_A22_COMPLETION",
    "M33_COMPLETION_OUTPUT_HASH": "PF_A22_COMPLETION",
    "M34_COMPLETION_WORKER_IDENTITY": "PF_A22_COMPLETION",
    "M35_COMPLETION_STAGE_BYPASS": "PF_A22_COMPLETION",
    "M36_COMPLETION_EPOCH_WINDOW": "PF_A22_COMPLETION",
}
ALLOWED_PREPARATION_FILES = {
    "AUDIT_OBLIGATIONS_V001.json", "METHODOLOGY.md",
    "validate_obligation_spec.py", "VALIDATION_RESULT_V001.json",
    "MANIFEST.sha256",
}
INDEPENDENT_PRODUCTION_FILES = (
    HERE.parent / "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001"
    / "independent_final_auditor.py",
    HERE.parent / "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001"
    / "production_dag_refinement.py",
    HERE.parent / "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001"
    / "production_evidence_orchestrator.py",
    HERE.parent / "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001"
    / "production_dual_l12_launcher.py",
)
CHECKS = 0


class Failure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise Failure(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise Failure(f"duplicate matrix key: {key}")
        result[key] = value
    return result


def reject_constant(token: str) -> object:
    raise Failure(f"nonfinite matrix token: {token}")


def load_matrix() -> dict[str, object]:
    raw = MATRIX.read_bytes()
    value = json.loads(
        raw.decode("utf-8"), object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), "matrix is not an object")
    return value


def validate_independence(matrix: dict[str, object]) -> int:
    contract = matrix["independence_contract"]
    require(isinstance(contract, dict), "independence contract absent")
    forbidden = contract.get("forbidden_import_modules")
    require(isinstance(forbidden, list) and forbidden, "forbidden import census absent")
    require(len(forbidden) == len(set(forbidden)), "duplicate forbidden import module")
    required_forbidden = {
        "build_target_cache", "consume_target_cache", "validate_preflight",
        "production_obligation_validators", "compute_prefix_history_v004",
        "independent_prefix_history_v003",
        "build_cache_v004r4", "consume_cache_v004r4",
        "validate_cache_preflight_v004r4",
    }
    require(required_forbidden.issubset(forbidden), "forbidden import census incomplete")
    for source_path in (Path(__file__), *INDEPENDENT_PRODUCTION_FILES):
        require(source_path.is_file(), f"auditor source absent: {source_path.name}")
        metadata = os.lstat(source_path)
        require(
            stat.S_ISREG(metadata.st_mode)
            and not stat.S_ISLNK(metadata.st_mode)
            and metadata.st_mode & 0o222 == 0,
            f"auditor source is not sealed read-only: {source_path.name}",
        )
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        imported: set[str] = set()
        dynamic_imports = 0
        path_loads = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "__import__"
            ):
                dynamic_imports += 1
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "import_module"
            ):
                dynamic_imports += 1
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "spec_from_file_location"
            ):
                path_loads += 1
        require(
            not imported.intersection(forbidden),
            f"auditor source imports target module: {source_path.name}",
        )
        require(dynamic_imports == 0, f"auditor source uses unbounded dynamic import: {source_path.name}")
        if source_path.name == "production_dag_refinement.py":
            source = source_path.read_text(encoding="utf-8")
            require(
                path_loads == 1
                and "_LOAD_REGISTRY: Final[dict[Path, str]]" in source
                and 'AUTH_MODEL: "track_c_authorization_model"' in source
                and 'LAUNCH_MODEL: "track_c_launch_model"' in source
                and 'HERE / "independent_final_auditor.py": "track_c_final_contract"'
                in source
                and "if _LOAD_REGISTRY.get(path) != name:" in source,
                "production refinement dynamic-load registry is not exact",
            )
        else:
            require(
                path_loads == 0,
                f"unregistered path-based dynamic import: {source_path.name}",
            )
    final_tree = ast.parse(
        INDEPENDENT_PRODUCTION_FILES[0].read_text(encoding="utf-8"),
        filename=str(INDEPENDENT_PRODUCTION_FILES[0]),
    )
    functions = {
        node.name for node in final_tree.body if isinstance(node, ast.FunctionDef)
    }
    require(
        {
            "validate_artifact", "validate_postrun_telemetry",
            "validate_target_l12_history", "validate_hostile_l12_history",
            "validate_final_l12_audit", "validate_mutation_ledger",
            "positive_fixture", "mutated_fixture",
        }.issubset(functions),
        "independent final-auditor public sink census incomplete",
    )
    return len(forbidden) + len(INDEPENDENT_PRODUCTION_FILES) + 4


def validate_stages(matrix: dict[str, object], artifact_stage_ids: set[str]) -> int:
    stages = matrix["stages"]
    require(isinstance(stages, list) and stages, "stage list absent")
    ids = [row.get("id") for row in stages if isinstance(row, dict)]
    require(len(ids) == len(stages) == len(set(ids)), "stage IDs malformed or duplicate")
    seen: set[str] = set()
    for row in stages:
        require(set(row) == {"id", "name", "requires", "permits", "forbids"}, f"stage key census: {row.get('id')}")
        require(isinstance(row["name"], str) and row["name"], f"stage name: {row['id']}")
        require(isinstance(row["requires"], list), f"stage requires: {row['id']}")
        require(set(row["requires"]).issubset(seen), f"stage DAG is not topological: {row['id']}")
        require(isinstance(row["permits"], list) and row["permits"], f"stage permits absent: {row['id']}")
        require(isinstance(row["forbids"], list) and row["forbids"], f"stage forbids absent: {row['id']}")
        seen.add(row["id"])
    require(seen == artifact_stage_ids, "one or more stages lacks an artifact obligation")
    return len(stages)


def validate_artifacts(matrix: dict[str, object]) -> tuple[dict[str, dict[str, object]], dict[str, int]]:
    artifacts = matrix["artifacts"]
    profiles = matrix["shared_profiles"]
    mutations = matrix["mutation_catalog"]
    require(isinstance(artifacts, list) and artifacts, "artifact list absent")
    require(isinstance(profiles, dict) and REQUIRED_PROFILES.issubset(profiles), "required shared profiles absent")
    require(isinstance(mutations, dict) and mutations, "mutation catalog absent")
    by_id: dict[str, dict[str, object]] = {}
    fixture_ids: set[str] = set()
    assigned_mutations: set[str] = set()
    rule_count = 0
    assignment_count = 0
    for row in artifacts:
        require(isinstance(row, dict), "artifact row is not object")
        required_keys = {
            "id", "stage_id", "kind", "canonical_paths", "profiles",
            *RULE_GROUPS, "positive_fixture", "mutation_classes", "maps_to",
        }
        if row.get("id") == "A22_TARGET_L12_AUTHORIZATION":
            required_keys |= {
                "positive_fixture_variants", "mutation_fixture_by_class",
            }
        require(set(row) == required_keys, f"artifact key census mismatch: {row.get('id')}")
        artifact_id = row["id"]
        require(isinstance(artifact_id, str) and artifact_id.startswith("A"), "artifact ID malformed")
        require(artifact_id not in by_id, f"duplicate artifact ID: {artifact_id}")
        require(isinstance(row["kind"], str) and row["kind"], f"artifact kind absent: {artifact_id}")
        require(isinstance(row["canonical_paths"], list) and row["canonical_paths"], f"artifact paths absent: {artifact_id}")
        require(all(isinstance(path, str) and path for path in row["canonical_paths"]), f"artifact path malformed: {artifact_id}")
        row_profiles = row["profiles"]
        require(isinstance(row_profiles, list) and REQUIRED_PROFILES.issubset(row_profiles), f"artifact profiles incomplete: {artifact_id}")
        require(set(row_profiles).issubset(profiles), f"artifact profile undefined: {artifact_id}")
        for group in RULE_GROUPS:
            rules = row[group]
            require(isinstance(rules, list) and rules, f"empty {group}: {artifact_id}")
            require(all(isinstance(rule, str) and rule for rule in rules), f"malformed {group}: {artifact_id}")
            rule_count += len(rules)
        fixture = row["positive_fixture"]
        require(isinstance(fixture, dict) and set(fixture) == {"id", "form", "acceptance"}, f"fixture schema: {artifact_id}")
        require(all(isinstance(fixture[key], str) and fixture[key] for key in fixture), f"fixture content: {artifact_id}")
        require(fixture["id"] not in fixture_ids, f"duplicate fixture ID: {fixture['id']}")
        fixture_ids.add(fixture["id"])
        variants = row.get("positive_fixture_variants", [])
        require(
            isinstance(variants, list)
            and (len(variants) == 7 if artifact_id == "A22_TARGET_L12_AUTHORIZATION" else not variants),
            f"fixture variant census: {artifact_id}",
        )
        for variant in variants:
            require(
                isinstance(variant, dict)
                and set(variant) == {"id", "form", "acceptance"}
                and all(isinstance(variant[key], str) and variant[key] for key in variant),
                f"fixture variant schema/content: {artifact_id}",
            )
            require(variant["id"] not in fixture_ids, f"duplicate fixture ID: {variant['id']}")
            fixture_ids.add(variant["id"])
        row_mutations = row["mutation_classes"]
        require(isinstance(row_mutations, list) and row_mutations, f"mutations absent: {artifact_id}")
        require(len(row_mutations) == len(set(row_mutations)), f"duplicate mutation assignment: {artifact_id}")
        require(set(row_mutations).issubset(mutations), f"undefined mutation: {artifact_id}")
        assigned_mutations.update(row_mutations)
        assignment_count += len(row_mutations)
        mutation_fixture_map = row.get("mutation_fixture_by_class", {})
        if artifact_id == "A22_TARGET_L12_AUTHORIZATION":
            require(
                isinstance(mutation_fixture_map, dict)
                and mutation_fixture_map == A22_MUTATION_FIXTURE_BY_CLASS,
                "A22 mutation/fixture assignment mismatch",
            )
        else:
            require(not mutation_fixture_map, f"unexpected mutation fixture map: {artifact_id}")
        require(isinstance(row["maps_to"], list) and row["maps_to"], f"checklist mapping absent: {artifact_id}")
        by_id[artifact_id] = row
    require(assigned_mutations == set(mutations), "one or more mutation catalog entries is unassigned")
    return by_id, {
        "artifacts": len(artifacts),
        "positive_fixtures": len(fixture_ids),
        "artifact_rule_statements": rule_count,
        "artifact_mutation_assignments": assignment_count,
        "mutation_classes": len(mutations),
    }


def validate_checklist(matrix: dict[str, object], artifacts: dict[str, dict[str, object]]) -> int:
    checklist = matrix["V012_checklist"]
    require(isinstance(checklist, list), "V012 checklist absent")
    observed: dict[str, dict[str, object]] = {}
    for row in checklist:
        require(isinstance(row, dict) and set(row) == {"id", "text", "artifact_ids"}, "checklist row schema")
        require(row["id"] not in observed, f"duplicate checklist ID: {row['id']}")
        observed[row["id"]] = row
    require({key: value["text"] for key, value in observed.items()} == EXPECTED_CHECKLIST, "18-point checklist text/census mismatch")
    for checklist_id, row in observed.items():
        artifact_ids = row["artifact_ids"]
        require(isinstance(artifact_ids, list) and artifact_ids, f"checklist unmapped: {checklist_id}")
        require(len(artifact_ids) == len(set(artifact_ids)), f"duplicate checklist mapping: {checklist_id}")
        require(set(artifact_ids).issubset(artifacts), f"unknown checklist artifact: {checklist_id}")
        for artifact_id in artifact_ids:
            require(checklist_id in artifacts[artifact_id]["maps_to"], f"nonreciprocal checklist mapping: {checklist_id}/{artifact_id}")
    for artifact_id, artifact in artifacts.items():
        require(set(artifact["maps_to"]).issubset(observed), f"unknown artifact checklist mapping: {artifact_id}")
        for checklist_id in artifact["maps_to"]:
            require(artifact_id in observed[checklist_id]["artifact_ids"], f"nonreciprocal artifact mapping: {artifact_id}/{checklist_id}")
    return len(observed)


def validate_v011(matrix: dict[str, object], artifacts: dict[str, dict[str, object]]) -> int:
    findings = matrix["V011_findings"]
    require(isinstance(findings, list), "V011 mapping absent")
    ids = {row.get("id") for row in findings if isinstance(row, dict)}
    require(ids == EXPECTED_V011 and len(findings) == 6, "V011 finding census mismatch")
    profiles = matrix["shared_profiles"]
    mutations = matrix["mutation_catalog"]
    for row in findings:
        require(set(row) == {"id", "required_rules", "required_mutations", "covered_by_artifacts"}, f"V011 row schema: {row.get('id')}")
        require(set(row["required_rules"]).issubset(profiles), f"V011 undefined profile: {row['id']}")
        require(set(row["required_mutations"]).issubset(mutations), f"V011 undefined mutation: {row['id']}")
        require(set(row["covered_by_artifacts"]).issubset(artifacts), f"V011 unknown artifact: {row['id']}")
        for artifact_id in row["covered_by_artifacts"]:
            artifact = artifacts[artifact_id]
            require(set(row["required_rules"]).issubset(artifact["profiles"]), f"V011 profile not assigned: {row['id']}")
            require(set(row["required_mutations"]).issubset(artifact["mutation_classes"]), f"V011 mutation not assigned: {row['id']}")
    expected = matrix["coverage_requirements"]["V011_finding_ids_exact"]
    require(set(expected) == EXPECTED_V011 and len(expected) == 6, "coverage V011 census mismatch")
    return len(findings)


def validate_scope(matrix: dict[str, object]) -> int:
    scope = matrix["scope"]
    require(scope.get("canonical_artifacts_created_by_this_packet") == [], "preparation claims canonical output")
    require("NO_GATE_CACHE_WORKSPACE_HISTORY_PHYSICS" in scope.get("claim_boundary", ""), "preparation claim boundary too broad")
    unexpected = {path.name for path in HERE.iterdir() if path.name not in ALLOWED_PREPARATION_FILES}
    require(not unexpected, f"unexpected preparation artifact(s): {sorted(unexpected)}")
    fixed = matrix["fixed_values"]
    require(fixed.get("supported_lengths") == [4, 6, 8, 10, 12], "five-cache census mismatch")
    require(fixed.get("first_control_authorized_lengths") == [4, 6, 8], "control length census mismatch")
    require(fixed.get("L10_authorized_length") == 10 and fixed.get("L12_authorized_length") == 12, "promotion lengths mismatch")
    target_scratch = fixed.get("target_scratch_minimum_bytes")
    hostile_scratch = fixed.get("hostile_scratch_minimum_bytes")
    hostile_shards = fixed.get("hostile_peak_live_raw_c128_shard_count")
    hostile_headers = fixed.get("hostile_container_header_bytes")
    combined_scratch = fixed.get("workspace_free_minimum_bytes")
    require(type(target_scratch) is int and target_scratch == 9_600_954_452, "target scratch floor mismatch")
    require(type(hostile_scratch) is int and hostile_scratch == 9_600_935_128, "hostile scratch floor mismatch")
    require(
        type(hostile_shards) is int and hostile_shards == 23,
        "hostile raw-c128 peak-live-shard census mismatch",
    )
    require(
        type(hostile_headers) is int and hostile_headers == 0,
        "hostile raw-c128 header mismatch",
    )
    require(
        type(combined_scratch) is int
        and combined_scratch == 19_201_889_580
        and hostile_scratch + hostile_shards * hostile_headers
        == 9_600_935_128
        and combined_scratch == target_scratch + hostile_scratch,
        "combined scratch floor mismatch",
    )
    require(fixed.get("V011_obstruction_sha256") == "0dc595ff78e4fa5d81a42a285d3b74ce93758dd8bb42c836471bd3e3e898e2f6", "V011 digest mismatch")
    require(
        fixed.get("dual_launch_coordinator_manifest_sha256")
        == "a6b6c61fa4e44cb53965b22c0fa0999c612a72cca9c90e31835bda3fa1a3336f",
        "dual-launch coordinator manifest mismatch",
    )
    require(
        fixed.get("dual_launch_coordinator_sha256_by_file")
        == {
            "README.md": "0a4b0694fca19f56c0628c3ad663859ac5697187af151f7e4501ab42f2f477db",
            "RESULT.json": "f7e6774fc8e308a6f601323393976ce0c1af23bfe6338148e18e46773a3ab3f9",
            "VERIFICATION.txt": "171bb3432a19d8a541f1a0ed0f772801c97f9046cb94af4b0d0b4ef1d4f642f1",
            "dual_launch_coordinator.py": "b4934b6603f923ab1039ae4aeb98d477e4ad6813b280e70a0ee1ba3667346406",
            "production_dual_l12_launcher.py": "095f8cd25499ea4f36cba913038cfbdadfe6e56309046370d4eeb03c347c1d71",
            "synthetic_fixtures.py": "ad887cf5a0b06df2f064faf4d31249afdd4899c2c6bb56b3e0336fe59dad8ba4",
            "test_dual_launch_coordinator.py": "49294c74c9c6f4ab9bf3207bf1b80ef12445d448727b51be714c21b0e52aa2c9",
            "test_production_dual_l12_launcher.py": "65baa98c07f3a07dc763b0b5f5619f5b453bdeb7a2ad4109bf96394ce2707d8a",
        },
        "dual-launch coordinator file census mismatch",
    )
    artifacts = {
        row["id"]: row for row in matrix["artifacts"] if isinstance(row, dict)
    }
    a01 = artifacts["A01_FREEZE_AND_SOURCE_PACKET"]
    required_a01_paths = {
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/production_obligation_validators.py",
        *(
            str(path.relative_to(HERE.parent))
            for path in INDEPENDENT_PRODUCTION_FILES
        ),
    }
    require(required_a01_paths.issubset(a01["canonical_paths"]), "A01 production/auditor source census incomplete")
    require(
        any("files census exactly METHOD,builder,consumer,production obligation validator,preflight" in rule for rule in a01["schema_rules"]),
        "A01 five-source freeze rule absent",
    )
    require(
        any("hostile postbuild audit" in rule for rule in a01["schema_rules"]),
        "A01 hostile postbuild absence lock absent",
    )
    a02 = artifacts["A02_NONPHYSICAL_PREFLIGHT"]
    require(
        any("all five frozen source hashes" in rule for rule in a02["provenance_rules"]),
        "A02 five-source binding absent",
    )
    require(
        any("477-case mutation ledger" in rule for rule in a02["provenance_rules"]),
        "A02 exact mutation-ledger binding absent",
    )
    a03 = artifacts["A03_PREPAYLOAD_AUDIT"]
    require(
        any("five frozen source hashes" in rule for rule in a03["provenance_rules"]),
        "A03 five-source binding absent",
    )
    require(
        any("execute one positive and every assigned hostile case" in rule for rule in a02["reconstruction_rules"]),
        "A02 production-sink execution rule absent",
    )
    a27 = artifacts["A27_MUTATION_LEDGER"]
    require(
        a27["canonical_paths"] == [
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            "PREFLIGHT_MUTATION_LEDGER_V001.json"
        ],
        "A27 canonical mutation-ledger path mismatch",
    )
    require(
        any("33 positive production-sink calls and 477 mutation production-sink calls" in rule for rule in a27["value_rules"]),
        "A27 exact expanded production-sink census absent",
    )
    a05 = artifacts["A05_FIVE_CACHE_SET"]
    require(
        a05["canonical_paths"] == [
            f"DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            f"CACHE_PAYLOADS_V012/L{length}/CACHE_MANIFEST.json"
            for length in (4, 6, 8, 10, 12)
        ],
        "A05 exact five-manifest path registry mismatch",
    )
    a10 = artifacts["A10_CONTROL_HISTORIES"]
    require(
        a10["canonical_paths"] == [
            f"DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            f"PHYSICAL_OUTPUTS/HISTORY_L{length}.json"
            for length in (4, 6, 8)
        ],
        "A10 exact control-history path registry mismatch",
    )
    a25 = artifacts["A25_HOSTILE_L12_HISTORY"]
    require(
        any("raw c128 with zero container-header bytes" in rule and "NPY or Krylov relabeling refuses" in rule for rule in a25["value_rules"]),
        "A25 native hostile storage/solver identity rule absent",
    )
    require(
        any("reject target NPY-header arithmetic" in rule for rule in a25["reconstruction_rules"]),
        "A25 independent raw-c128 resource reconstruction absent",
    )
    a22 = artifacts["A22_TARGET_L12_AUTHORIZATION"]
    require(
        a22["canonical_paths"] == [
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/TARGET_L12_EXECUTION_GATE_V012.json",
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_L12_EXECUTION_GATE_V004R4.json",
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_READY_V001.json",
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_READY_V001.json",
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_LAUNCH_HANDSHAKE_V002.json",
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_WORKER_RELEASE_V002.json",
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_COMMAND_V001.json",
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_COMMAND_V001.json",
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_ACK_V001.json",
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_ACK_V001.json",
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_COMPLETION_V001.json",
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_COMPLETION_V001.json",
        ],
        "A22 exact owner-once authority instance registry mismatch",
    )
    require(
        any("exact integrated authority instance census is 12" in rule
            for rule in a22["schema_rules"]),
        "A22 owner-once authority instance census absent",
    )
    a23 = artifacts["A23_POSTRUN_TELEMETRY"]
    require(
        any("CONSERVATIVE_AUTHENTICATION_CACHE_CERTIFICATE__NOT_OS_VIRTUAL_MEMORY"
            in rule for rule in a23["value_rules"]),
        "A23 mapped-certificate semantic boundary absent",
    )
    a26 = artifacts["A26_FINAL_L12_AUDIT"]
    require(
        any("instance census is exactly 42" in rule
            for rule in a26["schema_rules"]),
        "A26 owner-once artifact instance census absent",
    )
    return 24


def main() -> int:
    try:
        matrix = load_matrix()
        require(set(matrix) == EXPECTED_TOP_KEYS, "matrix top-level key census mismatch")
        require(matrix["schema"] == "TARGET_V012_PREREGISTERED_AUDIT_OBLIGATIONS_V001", "matrix schema mismatch")
        require(matrix["status"] == "PREREGISTERED_OBLIGATIONS_ONLY__NO_AUTHORITY_GRANTED", "matrix status mismatch")
        artifacts, counts = validate_artifacts(matrix)
        stage_count = validate_stages(matrix, {row["stage_id"] for row in artifacts.values()})
        checklist_count = validate_checklist(matrix, artifacts)
        finding_count = validate_v011(matrix, artifacts)
        independence_checks = validate_independence(matrix)
        scope_checks = validate_scope(matrix)
        coverage = matrix["coverage_requirements"]
        require(coverage.get("V012_checklist_ids_exact") == list(EXPECTED_CHECKLIST), "coverage checklist census mismatch")
        require(set(coverage.get("required_profiles_per_artifact", [])) == REQUIRED_PROFILES, "coverage profile census mismatch")
        require(set(coverage.get("required_rule_groups_per_artifact", [])) == RULE_GROUPS, "coverage rule-group census mismatch")
        require(all(coverage.get(key) is True for key in (
            "positive_fixture_required_per_artifact", "mutation_class_required_per_artifact",
            "every_stage_requires_artifact", "every_mutation_catalog_entry_requires_assignment",
            "every_artifact_requires_checklist_mapping",
        )), "coverage boolean requirement mismatch")
        result = {
            "schema": "TARGET_V012_AUDIT_OBLIGATION_SPEC_VALIDATION_V001",
            "classification": "PASS_PREREGISTERED_AUDIT_OBLIGATION_SPEC",
            "matrix_sha256": sha256(MATRIX),
            "methodology_sha256": sha256(METHOD),
            "validator_sha256": sha256(Path(__file__)),
            "counts": {
                **counts,
                "stages": stage_count,
                "V011_findings_mapped": finding_count,
                "V012_checklist_items_mapped": checklist_count,
                "independence_checks": independence_checks,
                "scope_checks": scope_checks,
                "structural_checks": CHECKS,
            },
            "target_validator_imported": False,
            "canonical_gate_cache_workspace_history_or_physics_created": False,
            "claim_boundary": "AUDIT_PREPARATION_VALIDATION_ONLY__NO_GATE_CACHE_WORKSPACE_HISTORY_OR_PHYSICS_RESULT",
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (Failure, OSError, UnicodeError, json.JSONDecodeError, SyntaxError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
