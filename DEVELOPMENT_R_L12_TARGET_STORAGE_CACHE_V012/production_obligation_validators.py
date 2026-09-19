#!/usr/bin/env python3
"""Exact native-schema dispatch for V012 production audit obligations.

Production sinks call ``validate_record(..., fixture_mode=False)`` after their
context-dependent custody checks.  The preflight feeds deterministic records
with the same native top-level schemas and calls the same validators with
``fixture_mode=True``.  That flag changes only canonical fixture paths in the
independent A23--A27 validators; it never selects a weaker schema contract.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import stat
import sys
import types
from functools import lru_cache
from pathlib import Path
from typing import Final, NamedTuple


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
FINAL_AUDITOR_PATH: Final[Path] = (
    ROOT / "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001"
    / "independent_final_auditor.py"
)
FINAL_AUDITOR_SHA256: Final[str] = (
    "cb1681c870b8382d9e7a83bec9df0830699d7b1015ed19b24360a3dbd4ae207e"
)
TARGET_ARTIFACT_IDS: Final[tuple[str, ...]] = (
    "A01_FREEZE_AND_SOURCE_PACKET", "A02_NONPHYSICAL_PREFLIGHT",
    "A03_PREPAYLOAD_AUDIT", "A04_UNIVERSAL_CUSTODY_GATE",
    "A05_FIVE_CACHE_SET", "A06_POSTBUILD_AUDIT",
    "A07_BASE_PHYSICAL_GATE", "A08_PHYSICAL_GATE_AUDIT",
    "A09_CONTROL_AUTHORIZATION", "A10_CONTROL_HISTORIES",
    "A11_CONTROL_STAGE_GATE", "A12_CONTROL_STAGE_AUDIT",
    "A13_L10_AUTHORIZATION", "A14_L10_HISTORY",
    "A15_L10_STAGE_GATE", "A16_L10_STAGE_AUDIT",
    "A17_HOSTILE_L12_ELIGIBILITY", "A18_L10_CROSS_GATE",
    "A20_SHARED_SCHEDULE_GATE", "A21_SHARED_SCHEDULE_AUDIT",
    "A22_TARGET_L12_AUTHORIZATION",
)
FINAL_ARTIFACT_IDS: Final[tuple[str, ...]] = (
    "A23_POSTRUN_TELEMETRY", "A24_TARGET_L12_HISTORY",
    "A25_HOSTILE_L12_HISTORY", "A26_FINAL_L12_AUDIT",
    "A27_MUTATION_LEDGER",
)
ARTIFACT_IDS: Final[tuple[str, ...]] = TARGET_ARTIFACT_IDS + FINAL_ARTIFACT_IDS
FROZEN_SOURCE_FILENAMES: Final[tuple[str, ...]] = (
    "METHOD.md", "build_target_cache.py", "consume_target_cache.py",
    "production_obligation_validators.py", "validate_preflight.py",
)
MUTATION_EXPECTED_REFUSAL: Final[dict[str, str]] = {
    "M01_MISSING_KEY": "exact key census mismatch",
    "M02_EXTRA_KEY": "exact key census mismatch",
    "M03_WRONG_KEY_SAME_COUNT": "exact key census mismatch",
    "M04_DUPLICATE_JSON_KEY": "duplicate JSON key",
    "M05_NONFINITE_JSON": "nonfinite JSON constant",
    "M06_BOOL_FOR_INT": "exact integer mismatch",
    "M07_FLOAT_INT_ALIAS": "exact integer mismatch",
    "M08_INT_FLOAT_ALIAS": "exact float mismatch",
    "M09_INT_OR_FLOAT_FOR_BOOL": "exact boolean mismatch",
    "M10_IDENTITY_OR_CLAIM": "identity/claim mismatch",
    "M11_HASH_OR_PATH": "path/hash mismatch",
    "M12_SYMLINK_OR_WRITABLE": "immutable ordinary file mismatch",
    "M13_DESCRIPTOR_TOCTOU": "descriptor path identity drift",
    "M14_COUNT_ARITHMETIC": "counter reconstruction mismatch",
    "M15_LIST_CENSUS_ORDER": "ordered census mismatch",
    "M16_CROSS_ROLE_ALIAS": "cross-role alias mismatch",
    "M17_PROVENANCE_DROP_SWAP": "provenance mismatch",
    "M18_CACHE_CENSUS_SEMANTICS": "cache census/semantics mismatch",
    "M19_STAGE_BYPASS": "stage predecessor mismatch",
    "M20_HISTORY_PROJECTION": "history projection mismatch",
    "M21_TERMINAL_SHARD": "terminal-shard mismatch",
    "M22_RESOURCE_FRESHNESS": "resource/freshness mismatch",
    "M23_HANDSHAKE_TELEMETRY": "launch/telemetry mismatch",
    "M24_UNLOCK_AUDIT_BINDING": "unlock/audit binding mismatch",
    "M25_IMPORT_TARGET_VALIDATOR": "target-validator import mismatch",
    "M26_L10_CROSS_MISMATCH": "L10 cross-projection mismatch",
    "M27_L12_CROSS_MISMATCH": "L12 cross-projection mismatch",
    "M28_PREMATURE_ARTIFACT": "premature canonical artifact mismatch",
    "M29_WRONG_ABSENCE_VALUE": "absence census mismatch",
    "M30_COMPLETION_BOOL_PROCESS_ID": "worker completion process_id type mismatch",
    "M31_COMPLETION_FLOAT_PROCESS_ID": "worker completion process_id type mismatch",
    "M32_COMPLETION_SCHEMA": "worker completion schema mismatch",
    "M33_COMPLETION_OUTPUT_HASH": "worker completion output hash mismatch",
    "M34_COMPLETION_WORKER_IDENTITY": "worker completion identity mismatch",
    "M35_COMPLETION_STAGE_BYPASS": "worker completion stage mismatch",
    "M36_COMPLETION_EPOCH_WINDOW": "worker completion epoch mismatch",
}

FINAL_NATIVE_MUTATION_REFUSAL: Final[
    dict[tuple[str, str], str]
] = {
    ("A23_POSTRUN_TELEMETRY", "M06_BOOL_FOR_INT"):
        "target_v012 launch must be an exact integer >= 1",
    ("A23_POSTRUN_TELEMETRY", "M07_FLOAT_INT_ALIAS"):
        "target_v012 launch must be an exact integer >= 1",
    ("A23_POSTRUN_TELEMETRY", "M08_INT_FLOAT_ALIAS"):
        "target_v012 wall must be an exact finite float >= 0.0",
    ("A23_POSTRUN_TELEMETRY", "M10_IDENTITY_OR_CLAIM"):
        "schema/classification mismatch",
    ("A23_POSTRUN_TELEMETRY", "M11_HASH_OR_PATH"):
        "target_v012 output must be an exact nonempty string",
    ("A23_POSTRUN_TELEMETRY", "M15_LIST_CENSUS_ORDER"):
        "target_v012 runtime sample order/boundary mismatch",
    ("A23_POSTRUN_TELEMETRY", "M16_CROSS_ROLE_ALIAS"):
        "cross-role output alias",
    ("A23_POSTRUN_TELEMETRY", "M17_PROVENANCE_DROP_SWAP"):
        "provenance role/stage alias",
    ("A23_POSTRUN_TELEMETRY", "M22_RESOURCE_FRESHNESS"):
        "target_v012 resource bound exceeded",
    ("A23_POSTRUN_TELEMETRY", "M23_HANDSHAKE_TELEMETRY"):
        "dual_launch_handshake_sha256 must be a lowercase SHA-256",
    ("A23_POSTRUN_TELEMETRY", "M27_L12_CROSS_MISMATCH"):
        "cross-role output alias",
    ("A24_TARGET_L12_HISTORY", "M06_BOOL_FOR_INT"):
        "L must be an exact integer >= 1",
    ("A24_TARGET_L12_HISTORY", "M07_FLOAT_INT_ALIAS"):
        "events must be an exact integer >= 1",
    ("A24_TARGET_L12_HISTORY", "M08_INT_FLOAT_ALIAS"):
        "event 1 W_n exact finite-float mismatch",
    ("A24_TARGET_L12_HISTORY", "M09_INT_OR_FLOAT_FOR_BOOL"):
        "comparison resolved must be an exact boolean",
    ("A24_TARGET_L12_HISTORY", "M10_IDENTITY_OR_CLAIM"):
        "history exact key census mismatch",
    ("A24_TARGET_L12_HISTORY", "M11_HASH_OR_PATH"):
        "terminal shard must be an exact nonempty string",
    ("A24_TARGET_L12_HISTORY", "M17_PROVENANCE_DROP_SWAP"):
        "target_hostile_l10_cross_gate_sha256 must be a lowercase SHA-256",
    ("A24_TARGET_L12_HISTORY", "M20_HISTORY_PROJECTION"):
        "event 2 order/cursor mismatch",
    ("A24_TARGET_L12_HISTORY", "M21_TERMINAL_SHARD"):
        "terminal shard byte reconstruction mismatch",
    ("A24_TARGET_L12_HISTORY", "M22_RESOURCE_FRESHNESS"):
        "RSS reconstruction mismatch",
    ("A24_TARGET_L12_HISTORY", "M24_UNLOCK_AUDIT_BINDING"):
        "target_hostile_l10_cross_gate_sha256 must be a lowercase SHA-256",
    ("A24_TARGET_L12_HISTORY", "M27_L12_CROSS_MISMATCH"):
        "terminal shard hash must be a lowercase SHA-256",
    ("A25_HOSTILE_L12_HISTORY", "M06_BOOL_FOR_INT"):
        "L must be an exact integer >= 1",
    ("A25_HOSTILE_L12_HISTORY", "M07_FLOAT_INT_ALIAS"):
        "events must be an exact integer >= 1",
    ("A25_HOSTILE_L12_HISTORY", "M08_INT_FLOAT_ALIAS"):
        "hostile event 1 W_n finite-float mismatch",
    ("A25_HOSTILE_L12_HISTORY", "M09_INT_OR_FLOAT_FOR_BOOL"):
        "hostile comparison resolved must be an exact boolean",
    ("A25_HOSTILE_L12_HISTORY", "M10_IDENTITY_OR_CLAIM"):
        "hostile history exact key census mismatch",
    ("A25_HOSTILE_L12_HISTORY", "M11_HASH_OR_PATH"):
        "hostile terminal path must be an exact nonempty string",
    ("A25_HOSTILE_L12_HISTORY", "M16_CROSS_ROLE_ALIAS"):
        "hostile history identity/method projection mismatch",
    ("A25_HOSTILE_L12_HISTORY", "M17_PROVENANCE_DROP_SWAP"):
        "target_hostile_l10_cross_gate_sha256 must be a lowercase SHA-256",
    ("A25_HOSTILE_L12_HISTORY", "M20_HISTORY_PROJECTION"):
        "hostile event 2 discrete identity mismatch",
    ("A25_HOSTILE_L12_HISTORY", "M21_TERMINAL_SHARD"):
        "hostile terminal shape/byte reconstruction mismatch",
    ("A25_HOSTILE_L12_HISTORY", "M22_RESOURCE_FRESHNESS"):
        "hostile resource reconstruction mismatch",
    ("A25_HOSTILE_L12_HISTORY", "M24_UNLOCK_AUDIT_BINDING"):
        "target_hostile_l10_cross_gate_sha256 must be a lowercase SHA-256",
    ("A25_HOSTILE_L12_HISTORY", "M27_L12_CROSS_MISMATCH"):
        "hostile terminal hash must be a lowercase SHA-256",
    ("A26_FINAL_L12_AUDIT", "M06_BOOL_FOR_INT"):
        "checks total must be an exact integer >= 1",
    ("A26_FINAL_L12_AUDIT", "M07_FLOAT_INT_ALIAS"):
        "checks total must be an exact integer >= 1",
    ("A26_FINAL_L12_AUDIT", "M08_INT_FLOAT_ALIAS"):
        "terminal Linf error must be an exact finite float >= 0.0",
    ("A26_FINAL_L12_AUDIT", "M09_INT_OR_FLOAT_FOR_BOOL"):
        "authority records authenticated must be an exact integer >= 1",
    ("A26_FINAL_L12_AUDIT", "M10_IDENTITY_OR_CLAIM"):
        "final audit identity mismatch",
    ("A26_FINAL_L12_AUDIT", "M11_HASH_OR_PATH"):
        "authority hash must be a lowercase SHA-256",
    ("A26_FINAL_L12_AUDIT", "M14_COUNT_ARITHMETIC"):
        "check total/failure reconstruction mismatch",
    ("A26_FINAL_L12_AUDIT", "M15_LIST_CENSUS_ORDER"):
        "terminal comparison order mismatch",
    ("A26_FINAL_L12_AUDIT", "M16_CROSS_ROLE_ALIAS"):
        "authority A25_HOSTILE_L12_HISTORY:1 refused: "
        "A25_HOSTILE_L12_HISTORY: hostile history exact key census mismatch",
    ("A26_FINAL_L12_AUDIT", "M17_PROVENANCE_DROP_SWAP"):
        "authority fixture content hash mismatch",
    ("A26_FINAL_L12_AUDIT", "M20_HISTORY_PROJECTION"):
        "authority fixture content hash mismatch",
    ("A26_FINAL_L12_AUDIT", "M21_TERMINAL_SHARD"):
        "target shard hash must be a lowercase SHA-256",
    ("A26_FINAL_L12_AUDIT", "M22_RESOURCE_FRESHNESS"):
        "authority fixture content hash mismatch",
    ("A26_FINAL_L12_AUDIT", "M23_HANDSHAKE_TELEMETRY"):
        "authority fixture content hash mismatch",
    ("A26_FINAL_L12_AUDIT", "M24_UNLOCK_AUDIT_BINDING"):
        "authority fixture content hash mismatch",
    ("A26_FINAL_L12_AUDIT", "M26_L10_CROSS_MISMATCH"):
        "authority fixture content hash mismatch",
    ("A26_FINAL_L12_AUDIT", "M27_L12_CROSS_MISMATCH"):
        "terminal comparison tolerance exceeded",
    ("A27_MUTATION_LEDGER", "M06_BOOL_FOR_INT"):
        "checks total must be an exact integer >= 1",
    ("A27_MUTATION_LEDGER", "M07_FLOAT_INT_ALIAS"):
        "checks total must be an exact integer >= 1",
    ("A27_MUTATION_LEDGER", "M08_INT_FLOAT_ALIAS"):
        "ledger case 1 identity/order mismatch",
    ("A27_MUTATION_LEDGER", "M09_INT_OR_FLOAT_FOR_BOOL"):
        "case passed must be an exact boolean",
    ("A27_MUTATION_LEDGER", "M10_IDENTITY_OR_CLAIM"):
        "ledger identity mismatch",
    ("A27_MUTATION_LEDGER", "M11_HASH_OR_PATH"):
        "ledger identity mismatch",
    ("A27_MUTATION_LEDGER", "M14_COUNT_ARITHMETIC"):
        "ledger total/failure mismatch",
    ("A27_MUTATION_LEDGER", "M15_LIST_CENSUS_ORDER"):
        "ledger case 1 identity/order mismatch",
    ("A27_MUTATION_LEDGER", "M16_CROSS_ROLE_ALIAS"):
        "positive fixture digest alias",
    ("A27_MUTATION_LEDGER", "M17_PROVENANCE_DROP_SWAP"):
        "ledger case 1 identity/order mismatch",
    ("A27_MUTATION_LEDGER", "M18_CACHE_CENSUS_SEMANTICS"):
        "ledger case 1 identity/order mismatch",
    ("A27_MUTATION_LEDGER", "M19_STAGE_BYPASS"):
        "ledger case 1 identity/order mismatch",
    ("A27_MUTATION_LEDGER", "M20_HISTORY_PROJECTION"):
        "ledger case 1 identity/order mismatch",
    ("A27_MUTATION_LEDGER", "M21_TERMINAL_SHARD"):
        "ledger case 1 identity/order mismatch",
    ("A27_MUTATION_LEDGER", "M22_RESOURCE_FRESHNESS"):
        "freeze hash must be a lowercase SHA-256",
    ("A27_MUTATION_LEDGER", "M23_HANDSHAKE_TELEMETRY"):
        "ledger case 1 identity/order mismatch",
    ("A27_MUTATION_LEDGER", "M24_UNLOCK_AUDIT_BINDING"):
        "ledger case 1 identity/order mismatch",
    ("A27_MUTATION_LEDGER", "M26_L10_CROSS_MISMATCH"):
        "ledger case 1 identity/order mismatch",
    ("A27_MUTATION_LEDGER", "M27_L12_CROSS_MISMATCH"):
        "ledger case 1 identity/order mismatch",
    ("A27_MUTATION_LEDGER", "M29_WRONG_ABSENCE_VALUE"):
        "ledger case 1 verdict mismatch",
}


class Refusal(RuntimeError):
    """Controlled production-contract refusal."""


class NativeSpec(NamedTuple):
    schema: str | None
    keys: frozenset[str]
    identity: tuple[tuple[str, object], ...]
    claim: str | None


def _fs(*items: str) -> frozenset[str]:
    return frozenset(items)


SOURCE_HASH_KEYS = _fs(
    "consumer_sha256", "builder_sha256", "preflight_sha256",
    "method_sha256", "freeze_sha256", "target_v004_sha256",
    "original_target_l12_gate_sha256", "preserved_workspace_custody_sha256",
    "preserved_workspace_cross_diagnostic_sha256",
    "runtime_compatibility_obstruction_sha256",
    "v006_hostile_audit_obstruction_sha256",
    "v007_runtime_compatibility_obstruction_sha256",
    "v008_postbuild_audit_binding_obstruction_sha256",
    "v009_hostile_audit_obstruction_sha256",
    "v010_hostile_audit_obstruction_sha256",
    "v010_audit_record_custody_correction_sha256",
    "v011_hostile_audit_obstruction_sha256", "preflight_result_sha256",
    "independent_hostile_audit_sha256",
)
HISTORY_KEYS = _fs(
    "schema", "L", "events", "dimension", "preterminal_dimension", "edges",
    "representation", "lineage_authority", "coarse_method", "fine_method",
    "rows", "comparison", "terminal_shards", "cache_manifest_sha256",
    "dual_obstruction_gate_sha256", "physical_execution_gate_sha256",
    "execution_authorization_sha256", "promotion_audit_sha256",
    "cached_control_l4_l8_gate_sha256", "cached_l10_gate_sha256",
    "cached_control_l4_l8_gate_audit_sha256",
    "l10_execution_authorization_gate_sha256", "cached_l10_gate_audit_sha256",
    "target_hostile_l10_cross_gate_sha256",
    "shared_aggregate_schedule_gate_sha256", "target_l12_execution_gate_sha256",
    "shared_aggregate_schedule_gate_audit_sha256",
    "original_target_l12_gate_sha256", "preserved_workspace_custody_sha256",
    "preserved_workspace_cross_diagnostic_sha256",
    "runtime_compatibility_obstruction_sha256",
    "v006_hostile_audit_obstruction_sha256",
    "v007_runtime_compatibility_obstruction_sha256",
    "v008_postbuild_audit_binding_obstruction_sha256",
    "v009_hostile_audit_obstruction_sha256",
    "v010_hostile_audit_obstruction_sha256",
    "v010_audit_record_custody_correction_sha256",
    "v011_hostile_audit_obstruction_sha256", "preflight_result_sha256",
    "independent_hostile_audit_sha256", "resource", "consumer_sha256",
    "builder_sha256", "method_sha256", "freeze_sha256", "target_v004_sha256",
    "production_obligation_validators_sha256",
    "claim_boundary",
)
HISTORY_STAGE_HASH_KEYS: Final[tuple[str, ...]] = (
    "cached_control_l4_l8_gate_sha256",
    "cached_control_l4_l8_gate_audit_sha256",
    "l10_execution_authorization_gate_sha256",
    "cached_l10_gate_sha256",
    "cached_l10_gate_audit_sha256",
    "target_hostile_l10_cross_gate_sha256",
    "shared_aggregate_schedule_gate_sha256",
    "shared_aggregate_schedule_gate_audit_sha256",
    "target_l12_execution_gate_sha256",
)
SANCTIONED_NULL_STAGE_HASH_KEYS: Final[
    dict[str, frozenset[str]]
] = {
    "A10_CONTROL_HISTORIES": frozenset(HISTORY_STAGE_HASH_KEYS),
    "A14_L10_HISTORY": frozenset(HISTORY_STAGE_HASH_KEYS[3:]),
    "A24_TARGET_L12_HISTORY": frozenset(),
}
STAGE_BASE_KEYS = SOURCE_HASH_KEYS | _fs(
    "schema", "classification", "physical_execution_gate_sha256",
    "cache_manifest_sha256_by_L", "histories", "claim_boundary",
)
STAGE_AUDIT_KEYS = _fs(
    "schema", "classification", "auditor_role", "audited_packet",
    "sealed_input_commit", "stage_gate_sha256", "history_sha256_by_L",
    "canonical_v004_sha256_by_L", "checks", "checks_passed", "checks_total",
    "failures", "claim_boundary",
)


TARGET_SPECS: Final[dict[str, tuple[NativeSpec, ...]]] = {
    "A01_FREEZE_AND_SOURCE_PACKET": (NativeSpec(
        "TARGET_L12_STORAGE_CACHE_FREEZE_V012",
        _fs(
            "schema", "status", "frozen_before_nonphysical_preflight_output",
            "cache_payload_created", "physical_history_executed",
            "current_v004_target_or_hostile_execution_interrupted",
            "current_v004_workspace_output_or_cache_read_or_modified",
            "sealed_input_commit", "files", "sealed_dependencies",
            "obstruction_evidence", "predecessor_compatibility_custody",
            "predecessor_v006_obstruction_custody",
            "predecessor_v007_obstruction_custody",
            "predecessor_v008_obstruction_custody",
            "predecessor_v009_obstruction_custody",
            "predecessor_v010_obstruction_custody",
            "predecessor_v011_obstruction_custody", "hard_locks",
            "storage_census_including_offsets_and_full_masks", "resource_limits",
            "claim_boundary",
        ),
        (("status", "FROZEN_BEFORE_NONPHYSICAL_PREFLIGHT_V001_OUTPUT"),),
        "AUDIT_BOUND_COMPATIBILITY_SUCCESSOR_PRE_PAYLOAD__NO_HISTORY_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
    ),),
    "A02_NONPHYSICAL_PREFLIGHT": (NativeSpec(
        "TARGET_L12_STORAGE_CACHE_NONPHYSICAL_PREFLIGHT_V012",
        _fs(
            "schema", "classification", "physical_cache_payload_created",
            "physical_history_executed", "checks", "L4_differential",
            "allocation_census", "resource_limits", "files", "mutation_ledger",
            "compatibility", "claim_boundary",
        ),
        (("classification", "PASS_NONPHYSICAL_EXHAUSTIVE_INDEX_ALLOCATION_AND_HARD_LOCK_PREFLIGHT"),),
        "V012_PORTABLE_NONPHYSICAL_STORAGE_INDEX_PROOF_ONLY__NO_CACHE_PAYLOAD_HISTORY_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
    ),),
    "A03_PREPAYLOAD_AUDIT": (NativeSpec(
        "TARGET_V012_PREPAYLOAD_HOSTILE_AUDIT_V001",
        _fs(
            "schema", "classification", "auditor_role", "audited_packet",
            "sealed_input_commit", "audited_freeze_sha256", "audited_files_sha256",
            "preflight_result_sha256", "checks", "checks_passed", "checks_total",
            "failures", "mutation_ledger", "no_symlinked_inputs",
            "v005_v006_v007_v008_v009_v010_v011_bytes_preserved",
            "absence_census", "payload_or_history_executed", "claim_boundary",
        ), (("classification", "PASS_TARGET_V012_PREPAYLOAD_CONTROL_PLANE"),),
        "V012_PREPAYLOAD_CONTROL_PLANE_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),),
    "A04_UNIVERSAL_CUSTODY_GATE": (NativeSpec(
        "TARGET_V012_DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE",
        _fs(
            "schema", "classification", "method_sha256", "builder_sha256",
            "consumer_sha256", "preflight_sha256", "freeze_sha256",
            "target_v004_sha256", "hostile_v003_sha256",
            "preserved_workspace_custody_sha256",
            "preserved_workspace_cross_diagnostic_sha256",
            "runtime_compatibility_obstruction_sha256",
            "superseded_v005_dual_gate_sha256",
            "superseded_v005_cache_manifest_sha256_by_L", "authorized_cache_lengths",
            "v006_hostile_audit_obstruction_sha256", "preflight_result_sha256",
            "v007_runtime_compatibility_obstruction_sha256",
            "superseded_v007_dual_gate_sha256",
            "superseded_v007_cache_manifest_sha256_by_L",
            "v008_postbuild_audit_binding_obstruction_sha256",
            "superseded_v008_dual_gate_sha256",
            "superseded_v008_cache_manifest_sha256_by_L",
            "v009_hostile_audit_obstruction_sha256",
            "v010_hostile_audit_obstruction_sha256",
            "v010_audit_record_custody_correction_sha256",
            "v011_hostile_audit_obstruction_sha256", "independent_hostile_audit",
            "obstructions", "claim_boundary",
        ), (("classification", "AUTHORIZE_TARGET_V012_FRESH_CACHE_AFTER_V005_V006_V007_V008_V009_V010_AND_V011_CONTROL_PLANE_OBSTRUCTIONS"),),
        "CONTROL_PLANE_AUTHORIZATION_ONLY__NO_CACHE_HISTORY_OR_PHYSICS_RESULT",
    ),),
    "A05_FIVE_CACHE_SET": (NativeSpec(
        "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012",
        _fs(
            "schema", "status", "L", "basis_order", "lineage_identity",
            "edge_layout", "hamiltonian_exchange_coefficient", "files", "payload",
            "resource_certificates", "builder_sha256", "consumer_sha256",
            "preflight_sha256", "method_sha256", "freeze_sha256",
            "production_obligation_validators_sha256",
            "dual_obstruction_gate_sha256", "target_v004_sha256",
            "target_v004_original_l12_gate_sha256", "hostile_v003_sha256",
            "target_v004_method_sha256", "target_v004_freeze_sha256",
            "hostile_v003_method_sha256", "hostile_v003_freeze_sha256",
            "preserved_workspace_custody_sha256",
            "preserved_workspace_cross_diagnostic_sha256",
            "runtime_compatibility_obstruction_sha256",
            "v006_hostile_audit_obstruction_sha256",
            "v007_runtime_compatibility_obstruction_sha256",
            "v008_postbuild_audit_binding_obstruction_sha256",
            "v009_hostile_audit_obstruction_sha256",
            "v010_hostile_audit_obstruction_sha256",
            "v010_audit_record_custody_correction_sha256",
            "v011_hostile_audit_obstruction_sha256", "preflight_result_sha256",
            "independent_hostile_audit_sha256", "superseded_v005_dual_gate_sha256",
            "superseded_v005_cache_manifest_sha256_by_L",
            "superseded_v007_dual_gate_sha256",
            "superseded_v007_cache_manifest_sha256_by_L",
            "superseded_v008_dual_gate_sha256",
            "superseded_v008_cache_manifest_sha256_by_L",
            "canonical_cache_root", "claim_boundary",
        ), (("status", "COMPLETE_HASH_PINNED_TARGET_STORAGE_ONLY_CACHE"),),
        "TARGET_V012_PORTABLE_STORAGE_INDICES_ONLY__NO_HISTORY_SPECTRUM_OR_GRAVITY",
    ),),
    "A06_POSTBUILD_AUDIT": (NativeSpec(
        "TARGET_V012_POSTBUILD_PAYLOAD_AUDIT_V001",
        _fs(
            "schema", "classification", "auditor_role", "audited_packet",
            "sealed_input_commit", "prebuild_hostile_audit_sha256",
            "dual_obstruction_and_compatibility_gate_sha256", "manifest_sha256_by_L",
            "payload_census_by_L", "checks", "checks_passed", "checks_total",
            "failures", "no_symlinked_or_writable_payload_inputs",
            "semantic_cachecontext", "physical_gate_or_history_executed",
            "claim_boundary",
        ), (("classification", "PASS_TARGET_V012_FRESH_STORAGE_CACHE_PAYLOADS"),),
        "POSTBUILD_STORAGE_CACHE_AUDIT_ONLY__NO_PHYSICAL_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),),
    "A07_BASE_PHYSICAL_GATE": (NativeSpec(
        "TARGET_V012_CACHE_PHYSICAL_EXECUTION_GATE",
        SOURCE_HASH_KEYS | _fs(
            "schema", "classification", "dual_obstruction_gate_sha256",
            "authorized_lengths", "cache_manifest_sha256_by_L",
            "postbuild_payload_audit", "claim_boundary",
        ), (("classification", "AUTHORIZE_TARGET_V012_CACHED_PHYSICAL_EXECUTION"),),
        "BASE_PHYSICAL_GATE_BINDING_ONLY__OUTER_HOSTILE_AUDIT_AUTHORIZATION_REQUIRED__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),),
    "A08_PHYSICAL_GATE_AUDIT": (NativeSpec(
        "TARGET_V012_PHYSICAL_GATE_HOSTILE_AUDIT_V001",
        _fs(
            "schema", "classification", "auditor_role", "audited_packet",
            "sealed_input_commit", "physical_execution_gate_sha256",
            "base_gate_exact_key_census_passed", "base_gate_exact_key_census_sha256",
            "postbuild_payload_audit_sha256", "consumer_sha256", "freeze_sha256",
            "checks", "checks_passed", "checks_total", "failures",
            "physical_history_executed", "claim_boundary",
        ), (("classification", "PASS_TARGET_V012_PHYSICAL_GATE_BINDINGS"),),
        "PHYSICAL_GATE_CONTROL_PLANE_AUDIT_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),),
    "A09_CONTROL_AUTHORIZATION": (NativeSpec(
        "TARGET_V012_CONTROL_EXECUTION_AUTHORIZATION_GATE_V001",
        _fs(
            "schema", "classification", "authorized_lengths",
            "physical_execution_gate", "physical_gate_hostile_audit",
            "postbuild_payload_audit", "consumer_sha256", "builder_sha256",
            "method_sha256", "freeze_sha256", "preflight_result_sha256",
            "claim_boundary",
        ), (("classification", "AUTHORIZE_AUDITED_TARGET_V012_CONTROLS_L4_L6_L8"),),
        "AUDITED_CONTROL_EXECUTION_AUTHORIZATION_ONLY__NO_L10_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),),
    "A10_CONTROL_HISTORIES": (NativeSpec(
        "TARGET_CACHED_PREFIX_HISTORY_V012", HISTORY_KEYS, (),
        "FINITE_CACHED_TARGET_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
    ),),
    "A11_CONTROL_STAGE_GATE": (NativeSpec(
        "TARGET_V012_CACHED_CONTROL_L4_L8_GATE", STAGE_BASE_KEYS,
        (("classification", "PASS_TARGET_V012_CACHED_CONTROLS_L4_L6_L8"),),
        "FINITE_CACHED_CONTROL_STAGE_ONLY__NO_L10_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),),
    "A12_CONTROL_STAGE_AUDIT": (NativeSpec(
        "TARGET_V012_CACHED_CONTROL_L4_L8_GATE_AUDIT_V001", STAGE_AUDIT_KEYS,
        (("classification", "PASS_INDEPENDENT_TARGET_V012_CACHED_CONTROLS_L4_L8"),),
        "FINITE_STAGE_GATE_AUDIT_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY_RESULT",
    ),),
    "A13_L10_AUTHORIZATION": (NativeSpec(
        "TARGET_V012_L10_EXECUTION_AUTHORIZATION_GATE_V001",
        _fs(
            "schema", "classification", "authorized_length",
            "physical_execution_gate_sha256", "cached_control_l4_l8_gate_sha256",
            "cached_control_l4_l8_gate_audit_sha256", "l10_cache_manifest_sha256",
            "consumer_sha256", "builder_sha256", "method_sha256", "freeze_sha256",
            "claim_boundary",
        ), (("classification", "AUTHORIZE_AUDITED_TARGET_V012_L10"),),
        "FINITE_L10_PROMOTION_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),),
    "A14_L10_HISTORY": (NativeSpec(
        "TARGET_CACHED_PREFIX_HISTORY_V012", HISTORY_KEYS, (),
        "FINITE_CACHED_TARGET_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
    ),),
    "A15_L10_STAGE_GATE": (NativeSpec(
        "TARGET_V012_CACHED_L10_GATE",
        STAGE_BASE_KEYS | _fs(
            "cached_control_l4_l8_gate_sha256",
            "l10_execution_authorization_gate_sha256",
        ), (("classification", "PASS_TARGET_V012_CACHED_L10"),),
        "FINITE_CACHED_L10_STAGE_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),),
    "A16_L10_STAGE_AUDIT": (NativeSpec(
        "TARGET_V012_CACHED_L10_GATE_AUDIT_V001",
        STAGE_AUDIT_KEYS | _fs("l10_execution_authorization_gate_sha256"),
        (("classification", "PASS_INDEPENDENT_TARGET_V012_CACHED_L10"),),
        "FINITE_STAGE_GATE_AUDIT_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY_RESULT",
    ),),
    "A17_HOSTILE_L12_ELIGIBILITY": (NativeSpec(
        None,
        _fs(
            "role", "method", "builder", "consumer", "preflight", "freeze",
            "preflight_result", "independent_audit", "cached_L10_gate",
            "L12_cache_manifest",
        ), (("role", "hostile_v004r4"),), None,
    ),),
    "A18_L10_CROSS_GATE": (NativeSpec(
        "TARGET_V012_HOSTILE_V004R4_L10_CROSS_GATE_V001",
        _fs(
            "schema", "classification", "auditor_role", "sealed_input_commit",
            "L", "target", "hostile", "comparison_policy", "checks",
            "checks_passed", "checks_total", "failures", "claim_boundary",
        ), (("classification", "PASS_EXACT_TARGET_HOSTILE_L10_CROSS_BENCHMARK"),),
        "FINITE_L10_TARGET_HOSTILE_CROSS_AUDIT_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),),
    "A20_SHARED_SCHEDULE_GATE": (NativeSpec(
        "V012_DUAL_L12_READINESS_SCHEDULE_V001",
        _fs(
            "schema", "classification", "created_epoch", "expires_epoch",
            "l10_cross_gate_sha256", "resource_snapshot", "schedule", "roles",
            "telemetry", "claim_boundary",
        ), (("classification", "READY_FOR_INDEPENDENT_SCHEDULE_AUDIT"),),
        "READINESS_AND_RESOURCE_SCHEDULING_ONLY__NO_L12_RELEASE_OR_RESULT",
    ),),
    "A21_SHARED_SCHEDULE_AUDIT": (NativeSpec(
        "V012_DUAL_L12_READINESS_SCHEDULE_AUDIT_V001",
        _fs(
            "schema", "classification", "auditor_role", "schedule_sha256",
            "l10_cross_gate_sha256", "checks", "checks_total", "checks_passed",
            "failures", "claim_boundary",
        ), (("classification", "PASS_INDEPENDENT_PREAUTHORIZATION_READINESS_AUDIT"),),
        "INDEPENDENT_READINESS_AUDIT_ONLY__NO_L12_AUTHORIZATION_RELEASE_OR_RESULT",
    ),),
    "A22_TARGET_L12_AUTHORIZATION": (
        NativeSpec(
            "TARGET_V012_L12_ONE_WAY_AUTHORIZATION_V001",
            _fs(
                "schema", "classification", "role", "authorized_length",
                "schedule_sha256", "schedule_audit_sha256", "l10_cross_gate_sha256",
                "consumer_sha256", "l12_cache_manifest_sha256", "claim_boundary",
            ), (("classification", "AUTHORIZE_TARGET_V012_L12_AFTER_SCHEDULE_AUDIT"), ("role", "target_v012")),
            "ONE_WAY_FINITE_L12_EXECUTION_AUTHORIZATION_ONLY__NO_LAUNCH_OR_RESULT",
        ),
        NativeSpec(
            "HOSTILE_V004R4_L12_ONE_WAY_AUTHORIZATION_V001",
            _fs(
                "schema", "classification", "role", "authorized_length",
                "schedule_sha256", "schedule_audit_sha256", "l10_cross_gate_sha256",
                "consumer_sha256", "l12_cache_manifest_sha256", "claim_boundary",
            ), (("classification", "AUTHORIZE_HOSTILE_V004R4_L12_AFTER_SCHEDULE_AUDIT"), ("role", "hostile_v004r4")),
            "ONE_WAY_FINITE_L12_EXECUTION_AUTHORIZATION_ONLY__NO_LAUNCH_OR_RESULT",
        ),
        NativeSpec(
            "V012_L12_WORKER_READY_V001",
            _fs(
                "schema", "role", "worker_id", "process_id",
                "process_start_token", "executable_path", "executable_sha256",
                "workspace_path", "output_path", "control_channel_id",
                "nonce_commitment_sha256", "ready_epoch",
                "blocked_on_release",
            ), (), None,
        ),
        NativeSpec(
            "V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002",
            _fs(
                "schema", "classification", "created_epoch", "schedule_sha256",
                "schedule_audit_sha256", "authorization_sha256_by_role",
                "ready_sha256_by_role", "memory_pressure", "workers",
                "observed_readiness_skew_seconds", "launch_skew_seconds_max",
                "telemetry", "claim_boundary",
            ), (("classification", "BOTH_BLOCKED_WORKERS_READY_AFTER_BOTH_L12_AUTHORIZATIONS"),),
            "IMMUTABLE_PRELAUNCH_HANDSHAKE_ONLY__NO_WORKER_RELEASE_OR_RESULT",
        ),
        NativeSpec(
            "V012_DUAL_L12_WORKER_RELEASE_V002",
            _fs(
                "schema", "classification", "handshake_sha256",
                "authorization_sha256_by_role", "release_epoch_by_role",
                "observed_launch_skew_seconds", "release_by_role", "claim_boundary",
            ), (("classification", "RELEASE_BOTH_AUTHORIZED_BLOCKED_WORKERS"),),
            "BARRIER_RELEASE_ONLY__NO_PHYSICAL_RESULT",
        ),
        NativeSpec(
            "V012_L12_WORKER_RELEASE_COMMAND_V001",
            _fs(
                "schema", "role", "worker_id", "process_id",
                "process_start_token", "control_channel_id",
                "nonce_commitment_sha256", "handshake_sha256",
                "worker_release_sha256", "release_epoch",
            ), (), None,
        ),
        NativeSpec(
            "V012_L12_WORKER_RELEASE_ACK_V001",
            _fs(
                "schema", "role", "worker_id", "process_id",
                "process_start_token", "control_channel_id", "nonce_hex",
                "ack_sha256",
            ), (), None,
        ),
        NativeSpec(
            "V012_L12_WORKER_COMPLETION_V001",
            _fs(
                "schema", "role", "worker_id", "process_id",
                "process_start_token", "control_channel_id", "output_path",
                "output_sha256", "completion_epoch",
                "blocked_on_orchestrator_close",
            ), (), None,
        ),
    ),
}


def _fail(artifact_id: str, detail: str) -> None:
    raise Refusal(f"{artifact_id}: {detail}")


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _sha(value: object) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
        and len(set(value)) > 1
    )


def canonical_json_bytes(record: object) -> bytes:
    try:
        return (json.dumps(
            record, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise Refusal("record is not finite canonical JSON") from error


@lru_cache(maxsize=1)
def _final_auditor():
    if not FINAL_AUDITOR_PATH.is_file():
        raise Refusal("A23-A27 independent final-auditor module absent")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(FINAL_AUDITOR_PATH, flags)
    except OSError as error:
        raise Refusal("A23-A27 independent final-auditor custody unavailable") from error
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_mode & 0o222:
            raise Refusal("A23-A27 independent final-auditor is not sealed read-only")
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            raw = stream.read()
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity = lambda item: (
        item.st_dev, item.st_ino, item.st_size,
        item.st_mtime_ns, item.st_ctime_ns,
    )
    if identity(before) != identity(after):
        raise Refusal("A23-A27 independent final-auditor descriptor drift")
    if hashlib.sha256(raw).hexdigest() != FINAL_AUDITOR_SHA256:
        raise Refusal("A23-A27 independent final-auditor hash mismatch")
    module_name = "v012_independent_final_auditor"
    module = types.ModuleType(module_name)
    module.__file__ = str(FINAL_AUDITOR_PATH)
    module.__package__ = None
    sys.modules[module_name] = module
    try:
        exec(compile(raw, str(FINAL_AUDITOR_PATH), "exec"), module.__dict__)
        module._install_synthetic_upstream_fixture(positive_fixture)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    return module


def _binding(label: str) -> dict[str, str]:
    return {"path": f"/synthetic/{label}.json", "sha256": _h(label)}


V004_L10_REFERENCE_PATH: Final[Path] = (
    ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001"
    / "BENCHMARK/TARGET_V004_QSHARD_L10.json"
)
V004_L10_REFERENCE_SHA256: Final[str] = (
    "873e45b6b37654910947711af1d8dc93d0def8ea0ef994587db206ab47b4267c"
)
V004_IMPLEMENTATION_SHA256: Final[str] = (
    "c626cabd09eeea41f63513f7218a82b5418b767bad0d2aace66f0a9feac8a1f7"
)
SCRATCH_LIMIT: Final[int] = 20 * 2**30
OVERHEAD_RESERVE: Final[int] = 2**20
MAPPED_CACHE_LIMIT: Final[int] = 512 * 2**20
NUMERICAL_WORKSET_LIMIT: Final[int] = 1_000_000_000
RSS_LIMIT: Final[int] = 17_179_869_184
WALL_LIMIT: Final[float] = 108_000.0
HISTORY_TOLERANCE: Final[float] = 1.0e-8


def _operator_q_bytes(length: int, q: int) -> int:
    edge_pairs = 3 * length * (
        math.comb(2 * length - 2, q - 1) if q else 0
    )
    return (
        4 * math.comb(2 * length, q) + 8 * edge_pairs
        + 8 * (3 * length + 1)
    )


def _payload_bytes(length: int) -> int:
    operator = sum(_operator_q_bytes(length, q) for q in range(length + 1))
    admission = sum(
        8 * math.comb(2 * length - 1, q)
        for event in range(length) for q in range(event + 1)
    )
    lineage_masks = sum(4 * 2**prefix for prefix in range(length))
    lineage_maps = sum(8 * 2**prefix for prefix in range(length - 1))
    return operator + admission + lineage_masks + lineage_maps


def _maximum_state_bytes(length: int) -> int:
    dimensions = [
        sum(
            math.comb(prefix, q) * math.comb(2 * length, q)
            for q in range(prefix + 1)
        )
        for prefix in range(length)
    ]
    return 16 * max(
        dimensions[index] + dimensions[index + 1]
        for index in range(length - 1)
    )


def _maximum_state_file_bytes(length: int) -> int:
    return _maximum_state_bytes(length) + 128 * (2 * length - 1)


def _carrier_word_bytes(length: int, q: int) -> int:
    return 4 * math.comb(2 * length, q)


def _admission_pair_bytes(length: int, q: int) -> int:
    return 8 * math.comb(2 * length - 1, q)


def _terminal_cache_peak_bytes(length: int) -> int:
    return max(
        _operator_q_bytes(length, q + 1)
        + _carrier_word_bytes(length, q)
        + _admission_pair_bytes(length, q)
        for q in range(length)
    )


def _authentication_cache_peak_bytes(length: int) -> int:
    all_carrier_words = sum(
        _carrier_word_bytes(length, q) for q in range(length + 1)
    )
    largest_nonword_operator = max(
        _operator_q_bytes(length, q) - _carrier_word_bytes(length, q)
        for q in range(length + 1)
    )
    largest_admission_pair = max(
        _admission_pair_bytes(length, q) for q in range(length)
    )
    return (
        all_carrier_words + largest_nonword_operator
        + largest_admission_pair
    )


@lru_cache(maxsize=1)
def _v004_l10_reference() -> dict[str, object]:
    try:
        raw = V004_L10_REFERENCE_PATH.read_bytes()
        value = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal("sealed V004 L10 reference unavailable") from error
    if (
        hashlib.sha256(raw).hexdigest() != V004_L10_REFERENCE_SHA256
        or type(value) is not dict
    ):
        raise Refusal("sealed V004 L10 reference hash/schema mismatch")
    return value


def _a14_fixture_resource() -> dict[str, object]:
    reference = _v004_l10_reference()
    length = 10
    peak_state = _maximum_state_file_bytes(length)
    workset = reference["resource"]["maximum_numerical_workset_bytes"]
    payload = _payload_bytes(length)
    terminal = _terminal_cache_peak_bytes(length)
    authentication = _authentication_cache_peak_bytes(length)
    return {
        "peak_live_state_bytes": peak_state,
        "cache_payload_bytes": payload,
        "combined_with_reserve_bytes": peak_state + payload + OVERHEAD_RESERVE,
        "scratch_limit_bytes": SCRATCH_LIMIT,
        "maximum_numerical_workset_bytes": workset,
        "numerical_workset_limit_bytes": NUMERICAL_WORKSET_LIMIT,
        "terminal_cache_peak_bytes": terminal,
        "authentication_cache_peak_bytes": authentication,
        "maximum_cache_window_bytes": max(terminal, authentication),
        "mapped_cache_limit_bytes": MAPPED_CACHE_LIMIT,
        "peak_rss_bytes": reference["resource"]["peak_rss_bytes"],
        "rss_limit_bytes": RSS_LIMIT,
        "wall_seconds": reference["resource"]["wall_seconds"],
        "wall_limit_seconds": WALL_LIMIT,
        "passed": True,
    }


def _a18_fixture_projection(role: str) -> dict[str, object]:
    if role not in {"target_v012", "hostile_v004r4"}:
        raise AssertionError("A18 fixture role is not registered")
    source_keys = ("method", "builder", "consumer", "preflight")
    record_keys = (
        "freeze", "preflight_result", "independent_audit", "cached_L10_gate",
        "L12_cache_manifest",
    )
    branch: dict[str, object] = {
        "role": role,
        **{
            key: _binding(f"A18_L10_CROSS_GATE:{role}:{key}")
            for key in source_keys
        },
    }
    for key in record_keys:
        branch[key] = {
            **_binding(f"A18_L10_CROSS_GATE:{role}:{key}"),
            "schema": f"FIXTURE_A18_{role}_{key}_SCHEMA".upper(),
            "identity_field": (
                "status" if key in {"freeze", "L12_cache_manifest"}
                else "classification"
            ),
            "identity_value": f"FIXTURE_A18_{role}_{key}_IDENTITY".upper(),
        }
    if role == "target_v012":
        return {
            "branch": branch,
            "cached_L10_gate_sha256": _h("A18:target:cached-L10-gate"),
            "cached_L10_gate_audit_sha256": _h("A18:target:cached-L10-audit"),
            "history_sha256": _h("A18:target:history"),
        }
    return {
        "branch": branch,
        "cached_L10_gate_sha256": _h("A18:hostile:cached-L10-gate"),
        "l10_execution_authorization_gate_sha256": _h(
            "A18:hostile:L10-authorization"
        ),
        "independent_prepayload_audit_sha256": _h(
            "A18:hostile:prepayload-audit"
        ),
        "history_sha256": _h("A18:hostile:history"),
    }


def _value_for_key(artifact_id: str, key: str, index: int) -> object:
    if key == "schema":
        raise AssertionError("schema is supplied by the native specification")
    if key == "claim_boundary":
        raise AssertionError("claim is supplied by the native specification")
    if artifact_id == "A14_L10_HISTORY":
        reference = _v004_l10_reference()
        if key in {"coarse_method", "fine_method", "rows", "comparison"}:
            return copy.deepcopy(reference[key])
        if key == "terminal_shards":
            return [
                {
                    **{
                        field: copy.deepcopy(item[field])
                        for field in ("q", "shape", "bytes", "sha256")
                    },
                    "path": (
                        "/synthetic/A14_L10_HISTORY/terminal_"
                        f"q{item['q']}.npy"
                    ),
                }
                for item in reference["terminal_shards"]
            ]
        if key == "resource":
            return _a14_fixture_resource()
        if key == "representation":
            return (
                "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_"
                "MASKS__AUTHENTICATED_INDEX_CACHE"
            )
        if key == "lineage_authority":
            return "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING"
    if artifact_id in {
        "A12_CONTROL_STAGE_AUDIT", "A16_L10_STAGE_AUDIT",
    }:
        if key == "auditor_role":
            return "INDEPENDENT_HOSTILE_STAGE_GATE_REVIEW"
        if key == "audited_packet":
            return "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
    if key == "sealed_input_commit":
        return "42f1ea3301ccf98802c07f3330d52999385cba0b"
    if key == "L":
        if artifact_id == "A10_CONTROL_HISTORIES":
            return 8
        return 10 if artifact_id in {"A14_L10_HISTORY", "A18_L10_CROSS_GATE"} else 12
    if key == "events":
        if artifact_id == "A10_CONTROL_HISTORIES":
            return 8
        return 10 if artifact_id == "A14_L10_HISTORY" else 12
    if key == "dimension":
        length = 8 if artifact_id == "A10_CONTROL_HISTORIES" else 10 if artifact_id == "A14_L10_HISTORY" else 12
        return math.comb(3 * length, length)
    if key == "preterminal_dimension":
        length = 8 if artifact_id == "A10_CONTROL_HISTORIES" else 10 if artifact_id == "A14_L10_HISTORY" else 12
        return math.comb(3 * length - 1, length - 1)
    if key == "edges":
        if artifact_id == "A10_CONTROL_HISTORIES":
            return 24
        return 30 if artifact_id == "A14_L10_HISTORY" else 36
    if key in {"authorized_length"}:
        return 10 if artifact_id == "A13_L10_AUTHORIZATION" else 12
    if key in {"authorized_lengths", "authorized_cache_lengths"}:
        return [4, 6, 8] if artifact_id == "A09_CONTROL_AUTHORIZATION" else [4, 6, 8, 10, 12]
    if key == "histories":
        lengths = [4, 6, 8] if artifact_id == "A11_CONTROL_STAGE_GATE" else [10]
        return [
            {"L": length, "path": f"/synthetic/HISTORY_L{length}.json", "sha256": _h(f"{artifact_id}:history:{length}")}
            for length in lengths
        ]
    if key in {"checks"}:
        if artifact_id in {"A12_CONTROL_STAGE_AUDIT", "A16_L10_STAGE_AUDIT"}:
            return {"history_projection": 1, "terminal_shards": 1, "provenance": 1}
        if artifact_id == "A18_L10_CROSS_GATE":
            return {
                "l10_cross_projection": 1, "terminal_shards": 1,
                "provenance": 1, "unlock_audit_binding": 1,
            }
        if artifact_id == "A21_SHARED_SCHEDULE_AUDIT":
            return {
                "resource_freshness": 1, "handshake_telemetry": 1,
                "l10_cross_projection": 1, "provenance": 1,
            }
        return {"schema": 1, "deep_types": 1, "provenance": 1}
    if key in {"checks_total", "checks_passed"}:
        return 4 if artifact_id in {
            "A18_L10_CROSS_GATE", "A21_SHARED_SCHEDULE_AUDIT",
        } else 3
    if key == "failures":
        return []
    if key in {
        "frozen_before_nonphysical_preflight_output", "no_symlinked_inputs",
        "v005_v006_v007_v008_v009_v010_v011_bytes_preserved",
        "no_symlinked_or_writable_payload_inputs", "base_gate_exact_key_census_passed",
    }:
        return True
    if key in {
        "cache_payload_created", "physical_history_executed",
        "current_v004_target_or_hostile_execution_interrupted",
        "current_v004_workspace_output_or_cache_read_or_modified",
        "payload_or_history_executed", "physical_gate_or_history_executed",
        "physical_cache_payload_created",
    }:
        return False
    if key == "audited_files_sha256":
        return {
            name: _h(f"{artifact_id}:{name}")
            for name in FROZEN_SOURCE_FILENAMES
        }
    if key.endswith("sha256"):
        return _h(f"{artifact_id}:{key}:{index}")
    if key.endswith("sha256_by_L") or key in {
        "manifest_sha256_by_L", "history_sha256_by_L",
        "canonical_v004_sha256_by_L", "cache_manifest_sha256_by_L",
        "superseded_v005_cache_manifest_sha256_by_L",
        "superseded_v007_cache_manifest_sha256_by_L",
        "superseded_v008_cache_manifest_sha256_by_L",
    }:
        lengths = (
            (4, 6, 8)
            if artifact_id in {"A11_CONTROL_STAGE_GATE", "A12_CONTROL_STAGE_AUDIT"}
            else (10,)
            if artifact_id in {"A15_L10_STAGE_GATE", "A16_L10_STAGE_AUDIT"}
            else (4, 6, 8, 10, 12)
        )
        return {
            str(length): _h(f"{artifact_id}:{key}:{length}")
            for length in lengths
        }
    if key in {
        "method", "builder", "consumer", "preflight", "freeze",
        "preflight_result", "independent_audit", "cached_L10_gate",
        "L12_cache_manifest", "physical_execution_gate", "physical_gate_hostile_audit",
        "postbuild_payload_audit", "independent_hostile_audit",
    }:
        return _binding(f"{artifact_id}:{key}")
    if key == "files":
        if artifact_id == "A01_FREEZE_AND_SOURCE_PACKET":
            return {
                name: _h(f"{artifact_id}:{name}") for name in (
                    "METHOD.md", "build_target_cache.py", "consume_target_cache.py",
                    "production_obligation_validators.py", "validate_preflight.py",
                )
            }
        return []
    if key in {"absence_census", "hard_locks"}:
        return {"authorization": False, "cache": False, "history": False, "telemetry": False}
    if key in {"sealed_dependencies", "obstruction_evidence", "obstructions"}:
        return []
    if key.startswith("predecessor_") and key.endswith("custody"):
        return _binding(f"{artifact_id}:{key}")
    if key == "storage_census_including_offsets_and_full_masks":
        return {"lengths": [4, 6, 8, 10, 12], "file_count": 1100, "full_canonical_masks": True}
    if key in {"resource_limits", "resource_certificates", "resource", "resource_snapshot"}:
        return {
            "memory_pressure": "NORMAL", "available_memory_bytes": 34_865_626_528,
            "workspace_free_disk_bytes": 19_201_889_580, "captured_age_seconds": 0,
            "passed": True,
        }
    if key == "allocation_census":
        return [{"L": length, "file_count": count} for length, count in ((4, 62), (6, 121), (8, 200), (10, 299), (12, 418))]
    if key == "L4_differential":
        return {"maximum_h_error": 0.0, "maximum_signed_current_error": 0.0}
    if key == "mutation_ledger":
        return {"path": "/synthetic/PREFLIGHT_MUTATION_LEDGER_V001.json", "sha256": _h(f"{artifact_id}:ledger")}
    if key == "compatibility":
        return {"superseded_v011_payloads_consumed": False}
    if key == "edge_layout":
        return [[0, 1, "forward"]]
    if key == "hamiltonian_exchange_coefficient":
        return -1
    if key == "payload":
        return {"file_count": 1, "total_bytes": 16}
    if key == "payload_census_by_L":
        return {str(length): {"file_count": 1, "total_bytes": 16} for length in (4, 6, 8, 10, 12)}
    if key == "semantic_cachecontext":
        return {"L4": {"descriptor_count": 62}, "L12": {"descriptor_count": 418}}
    if key == "rows":
        length = (
            8 if artifact_id == "A10_CONTROL_HISTORIES"
            else 10 if artifact_id == "A14_L10_HISTORY" else 12
        )
        return [
            {"event": event, "owner": event, "norm": 1.0}
            for event in range(1, length + 1)
        ]
    if key == "comparison":
        return {"resolved": True, "tolerance": 1.0e-8, "maximum_error": 0.0}
    if key == "terminal_shards":
        length = (
            8 if artifact_id == "A10_CONTROL_HISTORIES"
            else 10 if artifact_id == "A14_L10_HISTORY" else 12
        )
        return [
            {
                "q": q,
                "path": f"/synthetic/{artifact_id}/terminal_q{q}.npy",
                "shape": [math.comb(3 * length - 1, length - 1)],
                "bytes": 16 * math.comb(3 * length - 1, length - 1) + 128,
                "sha256": _h(f"{artifact_id}:terminal:{q}"),
                "mode": 0o444,
            }
            for q in range(length)
        ]
    if key == "comparison_policy":
        return {"absolute_tolerance": 1.0e-8, "nonfinite_refusal": True}
    if artifact_id == "A18_L10_CROSS_GATE" and key in {"target", "hostile"}:
        return _a18_fixture_projection(
            "target_v012" if key == "target" else "hostile_v004r4"
        )
    if key in {"target", "hostile"}:
        return {"role": key, "history_sha256": _h(f"{artifact_id}:{key}:history")}
    if key in {"created_epoch", "expires_epoch"}:
        return 100 if key == "created_epoch" else 200
    if key == "schedule":
        return {"launch_skew_seconds_max": 60, "release_only_after_both_l12_authorizations": True}
    if key == "roles":
        return {
            role: {
                "role": role, "ready_for_blocked_worker_start": True,
                "executable_sha256": _h(f"{artifact_id}:{role}:executable"),
            }
            for role in ("target_v012", "hostile_v004r4")
        }
    if key == "telemetry":
        return {"path": "/synthetic/telemetry.json", "absent_before_release": True}
    if key == "authorization_sha256_by_role":
        return {role: _h(f"{artifact_id}:{role}:authorization") for role in ("target_v012", "hostile_v004r4")}
    if key == "workers":
        return {role: {"role": role, "blocked_on_release": True} for role in ("target_v012", "hostile_v004r4")}
    if key in {"observed_readiness_skew_seconds", "launch_skew_seconds_max", "observed_launch_skew_seconds"}:
        return 30 if key != "launch_skew_seconds_max" else 60
    if key == "memory_pressure":
        return "NORMAL"
    if key == "release_epoch_by_role":
        return {"target_v012": 150, "hostile_v004r4": 160}
    if key == "release_by_role":
        return {role: {"role": role, "release_token_sha256": _h(f"{artifact_id}:{role}:release")} for role in ("target_v012", "hostile_v004r4")}
    if key == "role":
        return "hostile_v004r4"
    if key == "canonical_cache_root":
        return "/synthetic/target-cache/L12"
    if key in {"basis_order", "lineage_identity", "representation", "lineage_authority", "coarse_method", "fine_method", "auditor_role", "audited_packet"}:
        return f"FIXTURE_{key.upper()}"
    return {}


def _a22_records() -> tuple[dict[str, object], ...]:
    """Construct the eight exact, mutually bound launch-control forms."""
    target_authorization = _native_fixture("A22_TARGET_L12_AUTHORIZATION", 0)
    hostile_authorization = _native_fixture("A22_TARGET_L12_AUTHORIZATION", 1)

    def ready(role: str, ordinal: int) -> dict[str, object]:
        return {
            "schema": "V012_L12_WORKER_READY_V001",
            "role": role,
            "worker_id": f"fixture-{role}",
            "process_id": 40_000 + ordinal,
            "process_start_token": _h(f"A22:{role}:process-start"),
            "executable_path": f"/synthetic/{role}/worker.py",
            "executable_sha256": _h(f"A22:{role}:executable"),
            "workspace_path": f"/synthetic/{role}/workspace",
            "output_path": f"/synthetic/{role}/workspace/HISTORY_L12.json",
            "control_channel_id": f"fixture-channel-{ordinal}",
            "nonce_commitment_sha256": _h(f"A22:{role}:nonce-commitment"),
            "ready_epoch": 120 + ordinal,
            "blocked_on_release": True,
        }

    target_ready = ready("target_v012", 1)
    hostile_ready = ready("hostile_v004r4", 2)
    authorization_hashes = {
        "target_v012": hashlib.sha256(
            canonical_json_bytes(target_authorization)
        ).hexdigest(),
        "hostile_v004r4": hashlib.sha256(
            canonical_json_bytes(hostile_authorization)
        ).hexdigest(),
    }
    ready_hashes = {
        "target_v012": hashlib.sha256(canonical_json_bytes(target_ready)).hexdigest(),
        "hostile_v004r4": hashlib.sha256(canonical_json_bytes(hostile_ready)).hexdigest(),
    }
    handshake = {
        "schema": "V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002",
        "classification": "BOTH_BLOCKED_WORKERS_READY_AFTER_BOTH_L12_AUTHORIZATIONS",
        "created_epoch": 123,
        "schedule_sha256": target_authorization["schedule_sha256"],
        "schedule_audit_sha256": target_authorization["schedule_audit_sha256"],
        "authorization_sha256_by_role": authorization_hashes,
        "ready_sha256_by_role": ready_hashes,
        "memory_pressure": "NORMAL",
        "workers": {
            "target_v012": target_ready,
            "hostile_v004r4": hostile_ready,
        },
        "observed_readiness_skew_seconds": 1,
        "launch_skew_seconds_max": 60,
        "telemetry": {
            "path": "/synthetic/parallel/telemetry.json",
            "absent_before_release": True,
        },
        "claim_boundary": (
            "IMMUTABLE_PRELAUNCH_HANDSHAKE_ONLY__NO_WORKER_RELEASE_OR_RESULT"
        ),
    }
    handshake_hash = hashlib.sha256(canonical_json_bytes(handshake)).hexdigest()
    release_epochs = {"target_v012": 130, "hostile_v004r4": 131}
    release_rows: dict[str, dict[str, object]] = {}
    for role, worker in handshake["workers"].items():
        epoch = release_epochs[role]
        release_rows[role] = {
            "role": role,
            "worker_id": worker["worker_id"],
            "process_id": worker["process_id"],
            "process_start_token": worker["process_start_token"],
            "control_channel_id": worker["control_channel_id"],
            "nonce_commitment_sha256": worker["nonce_commitment_sha256"],
            "release_token_sha256": hashlib.sha256(
                f"{handshake_hash}:{role}:{epoch}".encode("ascii")
            ).hexdigest(),
        }
    release = {
        "schema": "V012_DUAL_L12_WORKER_RELEASE_V002",
        "classification": "RELEASE_BOTH_AUTHORIZED_BLOCKED_WORKERS",
        "handshake_sha256": handshake_hash,
        "authorization_sha256_by_role": authorization_hashes,
        "release_epoch_by_role": release_epochs,
        "observed_launch_skew_seconds": 1,
        "release_by_role": release_rows,
        "claim_boundary": "BARRIER_RELEASE_ONLY__NO_PHYSICAL_RESULT",
    }
    release_hash = hashlib.sha256(canonical_json_bytes(release)).hexdigest()
    command = {
        "schema": "V012_L12_WORKER_RELEASE_COMMAND_V001",
        "role": "target_v012",
        "worker_id": target_ready["worker_id"],
        "process_id": target_ready["process_id"],
        "process_start_token": target_ready["process_start_token"],
        "control_channel_id": target_ready["control_channel_id"],
        "nonce_commitment_sha256": target_ready["nonce_commitment_sha256"],
        "handshake_sha256": handshake_hash,
        "worker_release_sha256": release_hash,
        "release_epoch": release_epochs["target_v012"],
    }
    nonce = bytes.fromhex("31" * 32)
    target_ready["nonce_commitment_sha256"] = hashlib.sha256(
        b"V012_L12_WORKER_NONCE_V001\0" + nonce
    ).hexdigest()
    # Rebuild the downstream records after installing the authenticated nonce.
    ready_hashes["target_v012"] = hashlib.sha256(
        canonical_json_bytes(target_ready)
    ).hexdigest()
    handshake["ready_sha256_by_role"] = ready_hashes
    handshake_hash = hashlib.sha256(canonical_json_bytes(handshake)).hexdigest()
    release["handshake_sha256"] = handshake_hash
    for role, row in release_rows.items():
        worker = handshake["workers"][role]
        row["nonce_commitment_sha256"] = worker["nonce_commitment_sha256"]
        row["release_token_sha256"] = hashlib.sha256(
            f"{handshake_hash}:{role}:{release_epochs[role]}".encode("ascii")
        ).hexdigest()
    release_hash = hashlib.sha256(canonical_json_bytes(release)).hexdigest()
    command.update({
        "nonce_commitment_sha256": target_ready["nonce_commitment_sha256"],
        "handshake_sha256": handshake_hash,
        "worker_release_sha256": release_hash,
    })
    ack = {
        "schema": "V012_L12_WORKER_RELEASE_ACK_V001",
        "role": "target_v012",
        "worker_id": target_ready["worker_id"],
        "process_id": target_ready["process_id"],
        "process_start_token": target_ready["process_start_token"],
        "control_channel_id": target_ready["control_channel_id"],
        "nonce_hex": nonce.hex(),
        "ack_sha256": hashlib.sha256(
            b"V012_DUAL_L12_RELEASE_ACK_V001\0"
            + nonce + canonical_json_bytes(command)
        ).hexdigest(),
    }
    completion = {
        "schema": "V012_L12_WORKER_COMPLETION_V001",
        "role": "target_v012",
        "worker_id": target_ready["worker_id"],
        "process_id": target_ready["process_id"],
        "process_start_token": target_ready["process_start_token"],
        "control_channel_id": target_ready["control_channel_id"],
        "output_path": target_ready["output_path"],
        "output_sha256": _h("A22:target_v012:history-output"),
        "completion_epoch": release_epochs["target_v012"] + 100,
        "blocked_on_orchestrator_close": True,
    }
    return (
        target_authorization, hostile_authorization, target_ready, handshake,
        release, command, ack, completion,
    )


def _native_fixture(artifact_id: str, variant: int = 0) -> dict[str, object]:
    if artifact_id == "A22_TARGET_L12_AUTHORIZATION" and variant >= 2:
        return copy.deepcopy(_a22_records()[variant])
    spec = TARGET_SPECS[artifact_id][variant]
    record = {
        key: _value_for_key(artifact_id, key, index)
        for index, key in enumerate(sorted(spec.keys))
        if key not in {"schema", "claim_boundary"}
    }
    if spec.schema is not None:
        record["schema"] = spec.schema
    for key, value in spec.identity:
        record[key] = value
    if spec.claim is not None:
        record["claim_boundary"] = spec.claim
    if artifact_id == "A06_POSTBUILD_AUDIT":
        # Exercise the production A06 check census itself.  Keeping the
        # legitimate no_-prefixed integer first also makes the existing exact
        # bool/int, float/int, and count-arithmetic mutations target this
        # regression directly.
        record["checks"] = {
            "no_physical_execution_paths": 8,
            "cachecontext_clean_close_lengths": 2,
            "cachecontext_descriptor_reauthentication_lengths": 2,
            "cachecontext_full_semantic_lengths": 2,
            "cachecontext_zero_length_arrays": 4,
            "descriptor_stability_records": 1100,
            "dual_gate_authorizations": 5,
            "file_hash_byte_shape_dtype_records": 1100,
            "frozen_source_files": 5,
            "manifest_file_records": 1100,
            "manifest_identity_records": 5,
            "manifest_provenance_fields": 135,
            "payload_directories": 5,
            "prebuild_hostile_audit": 1,
            "resource_certificate_records": 5,
            "zero_length_q0_records": 10,
        }
        record["checks_total"] = sum(record["checks"].values())
        record["checks_passed"] = record["checks_total"]
    if artifact_id in {
        "A12_CONTROL_STAGE_AUDIT", "A16_L10_STAGE_AUDIT",
    }:
        lengths = (4, 6, 8) if artifact_id.startswith("A12_") else (10,)
        terminal_count = sum(lengths)
        record["canonical_v004_sha256_by_L"] = {
            str(length): CANONICAL_V004_HISTORY_SHA256[length]
            for length in lengths
        }
        record["checks"] = {
            "stage_gate_exact_schema": 1,
            "history_records": len(lengths),
            "canonical_v004_projection_records": len(lengths),
            "terminal_shard_records": terminal_count,
            "stable_descriptor_records": (
                1 + len(lengths) + terminal_count
            ),
        }
        record["checks_total"] = sum(record["checks"].values())
        record["checks_passed"] = record["checks_total"]
    if artifact_id in {
        "A10_CONTROL_HISTORIES", "A14_L10_HISTORY",
    }:
        for key in SANCTIONED_NULL_STAGE_HASH_KEYS[artifact_id]:
            record[key] = None
    return record


def _spec_for_record(artifact_id: str, record: dict[str, object]) -> NativeSpec:
    variants = TARGET_SPECS[artifact_id]
    if artifact_id == "A17_HOSTILE_L12_ELIGIBILITY":
        return variants[0]
    schema = record.get("schema")
    for spec in variants:
        if schema == spec.schema:
            return spec
    _fail(artifact_id, "identity/claim mismatch")


def _walk_native(
    value: object, artifact_id: str, *, within_checks: bool = False,
    at_record_root: bool = True,
) -> None:
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            _fail(artifact_id, "exact key census mismatch")
        checks = value.get("checks")
        if checks is not None:
            if type(checks) is not dict or not checks or any(type(item) is not int or item <= 0 for item in checks.values()):
                _fail(artifact_id, "exact integer mismatch")
            if "checks_total" in value and type(value["checks_total"]) is not int:
                _fail(artifact_id, "exact integer mismatch")
            if "checks_passed" in value and type(value["checks_passed"]) is not int:
                _fail(artifact_id, "exact integer mismatch")
            if "checks_total" in value and value["checks_total"] != sum(checks.values()):
                _fail(artifact_id, "counter reconstruction mismatch")
            if "checks_passed" in value and value["checks_passed"] != value.get("checks_total"):
                _fail(artifact_id, "counter reconstruction mismatch")
        for key, item in value.items():
            lower = key.lower()
            sanctioned_null_hash = (
                at_record_root
                and item is None
                and key in SANCTIONED_NULL_STAGE_HASH_KEYS.get(
                    artifact_id, frozenset()
                )
            )
            if lower.endswith("_bytes") or lower == "bytes":
                if type(item) is not int:
                    _fail(artifact_id, "exact integer mismatch")
                if item < 0:
                    _fail(artifact_id, "resource/freshness mismatch")
            if lower in {
                "l", "events", "dimension", "preterminal_dimension", "edges",
                "authorized_length", "checks_total", "checks_passed",
                "file_count", "total_bytes", "created_epoch", "expires_epoch",
                "captured_age_seconds", "observed_readiness_skew_seconds",
                "observed_launch_skew_seconds", "launch_skew_seconds_max",
                "hamiltonian_exchange_coefficient", "process_id",
                "ready_epoch", "release_epoch",
            } and type(item) is not int:
                _fail(artifact_id, "exact integer mismatch")
            if lower in {"file_count", "total_bytes"} and type(item) is int and item <= 0:
                _fail(artifact_id, "cache census/semantics mismatch")
            if lower in {
                "tolerance", "absolute_tolerance", "maximum_error",
                "maximum_abs_difference", "wall_limit_seconds",
            } and type(item) is not float:
                _fail(artifact_id, "exact float mismatch")
            if lower == "wall_seconds" and type(item) is not (
                int if artifact_id in {
                    "A01_FREEZE_AND_SOURCE_PACKET",
                    "A02_NONPHYSICAL_PREFLIGHT",
                } else float
            ):
                _fail(artifact_id, "exact numeric policy mismatch")
            boolean_named = lower in {
                "resolved", "passed", "passes", "bypassed", "authenticated",
                "nonfinite_refusal", "blocked_on_release",
                "ready_for_blocked_worker_start", "absent_before_release",
                "release_only_after_both_l12_authorizations",
                "physical_cache_payload_created", "base_gate_exact_key_census_passed",
            } or lower.endswith((
                "_consumed", "_executed", "_preserved",
                "_interrupted", "_modified",
            )) or (lower.startswith("no_") and not within_checks)
            if boolean_named:
                if type(item) is not bool:
                    _fail(artifact_id, "exact boolean mismatch")
            if (
                (lower == "sha256" or lower.endswith("_sha256"))
                and not (
                    artifact_id == "A03_PREPAYLOAD_AUDIT"
                    and lower == "audited_files_sha256"
                )
                and not sanctioned_null_hash
                and not _sha(item)
            ):
                _fail(artifact_id, "path/hash mismatch")
            if lower == "audited_files_sha256":
                if (
                    artifact_id != "A03_PREPAYLOAD_AUDIT"
                    or type(item) is not dict
                    or set(item) != set(FROZEN_SOURCE_FILENAMES)
                    or any(not _sha(digest) for digest in item.values())
                ):
                    _fail(artifact_id, "path/hash mismatch")
            if lower.endswith("_sha256_by_l") and type(item) is dict and any(not _sha(digest) for digest in item.values()):
                _fail(artifact_id, "provenance mismatch")
            if lower in {
                "physical_history_executed", "payload_or_history_executed",
                "physical_gate_or_history_executed", "cache_payload_created",
                "physical_cache_payload_created",
            }:
                if type(item) is not bool:
                    _fail(artifact_id, "exact boolean mismatch")
                if item is not False:
                    _fail(artifact_id, "absence census mismatch")
            if lower == "failures" and item != []:
                _fail(artifact_id, "counter reconstruction mismatch")
            if lower == "absence_census" and (
                type(item) is not dict
            ):
                _fail(artifact_id, "absence census mismatch")
            if lower == "absence_census":
                if any(type(absent) is not bool for absent in item.values()):
                    _fail(artifact_id, "exact boolean mismatch")
                if any(absent is not False for absent in item.values()):
                    _fail(artifact_id, "absence census mismatch")
            if lower in {"resource", "resource_limits", "resource_snapshot", "resource_certificates"} and type(item) is dict:
                if "memory_pressure" in item and item["memory_pressure"] != "NORMAL":
                    _fail(artifact_id, "resource/freshness mismatch")
                if "captured_age_seconds" in item and (
                    type(item["captured_age_seconds"]) is not int
                    or not 0 <= item["captured_age_seconds"] <= 300
                ):
                    _fail(artifact_id, "resource/freshness mismatch")
                if "workspace_free_disk_bytes" in item and (
                    type(item["workspace_free_disk_bytes"]) is not int
                    or item["workspace_free_disk_bytes"] < 19_201_889_580
                ):
                    _fail(artifact_id, "resource/freshness mismatch")
                if "passed" in item and item["passed"] is not True:
                    if type(item["passed"]) is not bool:
                        _fail(artifact_id, "exact boolean mismatch")
                    _fail(artifact_id, "resource/freshness mismatch")
            if lower == "edge_layout" and (
                type(item) is not list or not item
                or any(
                    type(edge) is not list or len(edge) != 3
                    or type(edge[0]) is not int or type(edge[1]) is not int
                    or type(edge[2]) is not str
                    for edge in item
                )
            ):
                _fail(artifact_id, "ordered census mismatch")
            if lower == "path" and (type(item) is not str or not item or "\x00" in item or ".." in Path(item).parts):
                _fail(artifact_id, "path/hash mismatch")
            _walk_native(
                item, artifact_id, within_checks=(lower == "checks"),
                at_record_root=False,
            )
    elif type(value) is list:
        for item in value:
            _walk_native(item, artifact_id, at_record_root=False)
    elif type(value) is float and not math.isfinite(value):
        _fail(artifact_id, "nonfinite JSON constant")
    elif type(value) not in (str, int, float, bool, type(None)):
        _fail(artifact_id, "unsupported native JSON value")


PHYSICAL_GATE_PATH: Final[Path] = HERE / "PHYSICAL_EXECUTION_GATE_V012.json"
FREEZE_PATH: Final[Path] = HERE / "FREEZE.json"
DUAL_GATE_PATH: Final[Path] = HERE / "DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json"
PREFLIGHT_RESULT_PATH: Final[Path] = HERE / "PREFLIGHT_RESULT_V001.json"
CACHE_ROOT: Final[Path] = HERE / "CACHE_PAYLOADS_V012"
PHYSICAL_OUTPUT_ROOT: Final[Path] = HERE / "PHYSICAL_OUTPUTS"
WORKSPACE_ROOT: Final[Path] = HERE / "WORKSPACES"
CONTROL_GATE_PATH: Final[Path] = HERE / "CACHED_CONTROL_L4_L8_GATE_V012.json"
CONTROL_AUDIT_PATH: Final[Path] = (
    ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012"
    / "CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json"
)
L10_AUTHORIZATION_PATH: Final[Path] = (
    HERE / "L10_EXECUTION_AUTHORIZATION_GATE_V012.json"
)
L10_GATE_PATH: Final[Path] = HERE / "CACHED_L10_GATE_V012.json"
L10_AUDIT_PATH: Final[Path] = (
    ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012"
    / "CACHED_L10_GATE_AUDIT_V001.json"
)
CANONICAL_V004_HISTORY_PATHS: Final[dict[int, Path]] = {
    4: ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001"
       / "CONTROL_HISTORY/TARGET_V004_L4.json",
    6: ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001"
       / "CONTROL_HISTORY/TARGET_V004_L6.json",
    8: ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001"
       / "CONTROL_HISTORY/TARGET_V004_L8.json",
    10: V004_L10_REFERENCE_PATH,
}
CANONICAL_V004_HISTORY_SHA256: Final[dict[int, str]] = {
    4: "8bf8f4eb54781c599a9fb3ae407207e08504396128c82e1e838d5b47a1d564b2",
    6: "06ccf6f419b8e743c6aea014c90ba1598786fc5bb28331488cde0f0846215f33",
    8: "affc775a91186883b5dd7c7180340b06105523ad5744c38a470331c1a631868a",
    10: V004_L10_REFERENCE_SHA256,
}


def _path_sha256(path: Path, artifact_id: str, label: str) -> str:
    try:
        if path.is_symlink() or not path.is_file():
            _fail(artifact_id, f"{label} path/hash mismatch")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise Refusal(f"{artifact_id}: {label} path/hash mismatch") from error
    return digest


def _file_record(path: Path, artifact_id: str, label: str) -> dict[str, object]:
    try:
        raw = path.read_bytes()
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=lambda pairs: _exact_pairs(
                pairs, artifact_id, label,
            ),
            parse_constant=lambda token: _reject_nonfinite(
                token, artifact_id,
            ),
        )
    except Refusal:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal(f"{artifact_id}: {label} path/hash mismatch") from error
    if type(value) is not dict:
        _fail(artifact_id, f"{label} exact key census mismatch")
    return value


def _exact_pairs(
    pairs: list[tuple[str, object]], artifact_id: str, label: str,
) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            _fail(artifact_id, f"{label} duplicate JSON key")
        value[key] = item
    return value


def _reject_nonfinite(token: str, artifact_id: str) -> object:
    _fail(artifact_id, f"nonfinite JSON constant: {token}")


def _live_source_values(artifact_id: str) -> tuple[dict[str, object], str]:
    physical = _file_record(
        PHYSICAL_GATE_PATH, artifact_id, "base physical gate",
    )
    if not SOURCE_HASH_KEYS.issubset(physical):
        _fail(artifact_id, "base physical gate provenance mismatch")
    return (
        {key: physical[key] for key in SOURCE_HASH_KEYS},
        _path_sha256(
            PHYSICAL_GATE_PATH, artifact_id, "base physical gate",
        ),
    )


def _expect_values(
    artifact_id: str, record: dict[str, object], expected: dict[str, object],
    detail: str,
) -> None:
    if any(
        record.get(key) != value
        or type(record.get(key)) is not type(value)
        for key, value in expected.items()
    ):
        _fail(artifact_id, detail)


def _stage_lengths(artifact_id: str) -> tuple[int, ...]:
    return (4, 6, 8) if artifact_id.startswith(("A11_", "A12_")) else (10,)


def _history_relative_path(length: int) -> str:
    return (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/"
        f"HISTORY_L{length}.json"
    )


def _stage_checks(lengths: tuple[int, ...]) -> dict[str, int]:
    terminal_count = sum(lengths)
    return {
        "stage_gate_exact_schema": 1,
        "history_records": len(lengths),
        "canonical_v004_projection_records": len(lengths),
        "terminal_shard_records": terminal_count,
        "stable_descriptor_records": 1 + len(lengths) + terminal_count,
    }


def _validate_stage_gate_contract(
    artifact_id: str, record: dict[str, object], fixture_mode: bool,
) -> None:
    lengths = _stage_lengths(artifact_id)
    histories = record.get("histories")
    if type(histories) is list:
        observed_lengths = [
            row.get("L") for row in histories if type(row) is dict
        ]
        if (
            len(histories) != len(lengths)
            or (
                len(observed_lengths) == len(histories)
                and all(type(length) is int for length in observed_lengths)
                and observed_lengths != list(lengths)
            )
        ):
            _fail(artifact_id, "ordered census mismatch")
    if (
        type(histories) is not list
        or any(
            type(row) is not dict
            or set(row) != {"L", "path", "sha256"}
            for row in histories
        )
    ):
        _fail(artifact_id, "history projection mismatch")
    expected_paths = {
        length: (
            f"/synthetic/HISTORY_L{length}.json"
            if fixture_mode else _history_relative_path(length)
        )
        for length in lengths
    }
    if any(
        type(row["L"]) is not int or row["L"] != length
        or row["path"] != expected_paths[length]
        for row, length in zip(histories, lengths)
    ):
        _fail(artifact_id, "history projection mismatch")
    if fixture_mode:
        return
    source, physical_sha = _live_source_values(artifact_id)
    _expect_values(
        artifact_id, record, source,
        "stage gate required source provenance mismatch",
    )
    if record.get("physical_execution_gate_sha256") != physical_sha:
        _fail(artifact_id, "stage predecessor mismatch")
    expected_cache = {
        str(length): _path_sha256(
            CACHE_ROOT / f"L{length}/CACHE_MANIFEST.json",
            artifact_id, f"L{length} cache manifest",
        )
        for length in lengths
    }
    if record.get("cache_manifest_sha256_by_L") != expected_cache:
        _fail(artifact_id, "cache census/semantics mismatch")
    for row, length in zip(histories, lengths):
        expected = _path_sha256(
            PHYSICAL_OUTPUT_ROOT / f"HISTORY_L{length}.json",
            artifact_id, f"L{length} history",
        )
        if row["sha256"] != expected:
            _fail(artifact_id, "history projection mismatch")
    if artifact_id == "A15_L10_STAGE_GATE":
        if (
            record.get("cached_control_l4_l8_gate_sha256")
            != _path_sha256(CONTROL_GATE_PATH, artifact_id, "control gate")
            or record.get("l10_execution_authorization_gate_sha256")
            != _path_sha256(
                L10_AUTHORIZATION_PATH, artifact_id, "L10 authorization",
            )
        ):
            _fail(artifact_id, "unlock/audit binding mismatch")


def _validate_stage_audit_contract(
    artifact_id: str, record: dict[str, object], fixture_mode: bool,
) -> None:
    lengths = _stage_lengths(artifact_id)
    checks = _stage_checks(lengths)
    total = sum(checks.values())
    if (
        record.get("auditor_role") != "INDEPENDENT_HOSTILE_STAGE_GATE_REVIEW"
        or record.get("audited_packet")
        != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        or record.get("sealed_input_commit")
        != "42f1ea3301ccf98802c07f3330d52999385cba0b"
    ):
        _fail(artifact_id, "identity/claim mismatch")
    observed_checks = record.get("checks")
    if (
        type(observed_checks) is dict
        and "terminal_shard_records" in observed_checks
        and (
            type(observed_checks["terminal_shard_records"]) is not int
            or observed_checks["terminal_shard_records"]
            != checks["terminal_shard_records"]
        )
    ):
        _fail(artifact_id, "terminal-shard mismatch")
    if (
        observed_checks != checks
        or record.get("checks_total") != total
        or type(record.get("checks_total")) is not int
        or record.get("checks_passed") != total
        or type(record.get("checks_passed")) is not int
        or record.get("failures") != []
    ):
        _fail(artifact_id, "counter reconstruction mismatch")
    if fixture_mode:
        return
    stage_path = CONTROL_GATE_PATH if lengths == (4, 6, 8) else L10_GATE_PATH
    expected_histories = {
        str(length): _path_sha256(
            PHYSICAL_OUTPUT_ROOT / f"HISTORY_L{length}.json",
            artifact_id, f"L{length} history",
        )
        for length in lengths
    }
    if record.get("stage_gate_sha256") != _path_sha256(
        stage_path, artifact_id, "stage gate",
    ):
        _fail(artifact_id, "unlock/audit binding mismatch")
    if record.get("history_sha256_by_L") != expected_histories:
        _fail(artifact_id, "history projection mismatch")
    if record.get("canonical_v004_sha256_by_L") != {
        str(length): CANONICAL_V004_HISTORY_SHA256[length]
        for length in lengths
    }:
        _fail(artifact_id, "provenance mismatch")
    if artifact_id == "A16_L10_STAGE_AUDIT" and (
        record.get("l10_execution_authorization_gate_sha256")
        != _path_sha256(
            L10_AUTHORIZATION_PATH, artifact_id, "L10 authorization",
        )
    ):
        _fail(artifact_id, "unlock/audit binding mismatch")


def _validate_l10_authorization_contract(
    artifact_id: str, record: dict[str, object], fixture_mode: bool,
) -> None:
    if type(record.get("authorized_length")) is not int:
        _fail(artifact_id, "exact integer mismatch")
    if record["authorized_length"] != 10:
        _fail(artifact_id, "history projection mismatch")
    if fixture_mode:
        return
    source, physical_sha = _live_source_values(artifact_id)
    expected = {
        "physical_execution_gate_sha256": physical_sha,
        "cached_control_l4_l8_gate_sha256": _path_sha256(
            CONTROL_GATE_PATH, artifact_id, "control gate",
        ),
        "cached_control_l4_l8_gate_audit_sha256": _path_sha256(
            CONTROL_AUDIT_PATH, artifact_id, "control audit",
        ),
        "l10_cache_manifest_sha256": _path_sha256(
            CACHE_ROOT / "L10/CACHE_MANIFEST.json",
            artifact_id, "L10 cache manifest",
        ),
        **{
            key: source[key]
            for key in (
                "consumer_sha256", "builder_sha256", "method_sha256",
                "freeze_sha256",
            )
        },
    }
    _expect_values(
        artifact_id, record, expected,
        "L10 authorization predecessor/provenance mismatch",
    )


def _projection_close(
    observed: object, reference: object, artifact_id: str, label: str,
    tolerance: float = HISTORY_TOLERANCE,
) -> None:
    if type(reference) in (bool, str, type(None)):
        if type(observed) is not type(reference) or observed != reference:
            _fail(artifact_id, f"{label} history projection mismatch")
        return
    if type(reference) is int:
        if type(observed) is not int or observed != reference:
            _fail(artifact_id, f"{label} history projection mismatch")
        return
    if type(reference) is float:
        if (
            type(observed) is not float or not math.isfinite(observed)
            or abs(observed - reference) > tolerance
        ):
            _fail(artifact_id, f"{label} history projection mismatch")
        return
    if type(reference) is list:
        if type(observed) is not list or len(observed) != len(reference):
            _fail(artifact_id, f"{label} history projection mismatch")
        for index, (item, expected) in enumerate(zip(observed, reference)):
            _projection_close(
                item, expected, artifact_id, f"{label}[{index}]", tolerance,
            )
        return
    if type(reference) is dict:
        if type(observed) is not dict or set(observed) != set(reference):
            _fail(artifact_id, f"{label} history projection mismatch")
        for key, expected in reference.items():
            _projection_close(
                observed[key], expected, artifact_id,
                f"{label}.{key}", tolerance,
            )
        return
    _fail(artifact_id, f"{label} history projection mismatch")


def _validate_solver(
    solver: object, artifact_id: str, event: int, role: str,
) -> None:
    expected_keys = {
        "batches", "converged", "low_memory_batches",
        "maximum_exp_difference", "maximum_krylov_steps",
        "maximum_live_bytes", "maximum_residual_indicator",
        "maximum_subdivisions", "quadrature_nodes",
    }
    if type(solver) is not dict or set(solver) != expected_keys:
        _fail(artifact_id, "history solver exact key census mismatch")
    integer_fields = (
        "batches", "low_memory_batches", "maximum_krylov_steps",
        "maximum_live_bytes", "maximum_subdivisions", "quadrature_nodes",
    )
    expected_zero = role == "null_solver" and event == 1
    if (
        solver["converged"] is not True
        or any(type(solver[key]) is not int or solver[key] < 0 for key in integer_fields)
        or solver["batches"] <= 0
        or (
            solver["maximum_krylov_steps"] != 0
            if expected_zero else solver["maximum_krylov_steps"] <= 0
        )
        or not 0 < solver["maximum_live_bytes"] <= NUMERICAL_WORKSET_LIMIT
        or solver["maximum_subdivisions"] <= 0
        or solver["quadrature_nodes"] != 24
        or any(
            type(solver[key]) is not float
            or not math.isfinite(solver[key]) or solver[key] < 0.0
            for key in (
                "maximum_exp_difference", "maximum_residual_indicator",
            )
        )
    ):
        _fail(artifact_id, "history solver type/convergence mismatch")


def _validate_l10_history_contract(
    artifact_id: str, record: dict[str, object], fixture_mode: bool,
) -> None:
    reference = _v004_l10_reference()
    if (
        record.get("representation")
        != "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__AUTHENTICATED_INDEX_CACHE"
        or record.get("lineage_authority")
        != "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING"
    ):
        _fail(artifact_id, "history projection mismatch")
    _projection_close(
        record.get("coarse_method"), reference.get("coarse_method"),
        artifact_id, "coarse method", 0.0,
    )
    _projection_close(
        record.get("fine_method"), reference.get("fine_method"),
        artifact_id, "fine method", 0.0,
    )
    rows = record.get("rows")
    reference_rows = reference.get("rows")
    if (
        type(rows) is not list or type(reference_rows) is not list
        or len(rows) != 10 or len(reference_rows) != 10
    ):
        _fail(artifact_id, "history projection mismatch")
    for event, (row, expected) in enumerate(
        zip(rows, reference_rows), start=1,
    ):
        if type(row) is not dict or set(row) != set(expected):
            _fail(artifact_id, "history projection mismatch")
        _validate_solver(row.get("actual_solver"), artifact_id, event, "actual_solver")
        _validate_solver(row.get("null_solver"), artifact_id, event, "null_solver")
        _projection_close(
            {
                key: value for key, value in row.items()
                if key not in {"actual_solver", "null_solver"}
            },
            {
                key: value for key, value in expected.items()
                if key not in {"actual_solver", "null_solver"}
            },
            artifact_id, f"event {event}",
        )
    _projection_close(
        record.get("comparison"), reference.get("comparison"),
        artifact_id, "comparison",
    )
    terminal = record.get("terminal_shards")
    expected_terminal = reference.get("terminal_shards")
    if (
        type(terminal) is not list or type(expected_terminal) is not list
        or len(terminal) != 10
    ):
        _fail(artifact_id, "terminal-shard mismatch")
    for q, (item, expected) in enumerate(zip(terminal, expected_terminal)):
        if (
            type(item) is not dict
            or set(item) != {"q", "path", "shape", "bytes", "sha256"}
            or type(item.get("q")) is not int or item["q"] != q
            or item.get("shape") != expected.get("shape")
            or type(item.get("shape")) is not list
            or any(type(value) is not int for value in item["shape"])
            or type(item.get("bytes")) is not int
            or item["bytes"] != expected.get("bytes")
            or item.get("sha256") != expected.get("sha256")
        ):
            _fail(artifact_id, "terminal-shard mismatch")
        expected_path = (
            f"/synthetic/A14_L10_HISTORY/terminal_q{q}.npy"
            if fixture_mode else str(
                WORKSPACE_ROOT / "L10/sharp/prefix_09" / f"q_{q:02d}.npy"
            )
        )
        if item.get("path") != expected_path:
            _fail(artifact_id, "path/hash mismatch")
        if not fixture_mode:
            path = Path(expected_path)
            if (
                path.stat().st_size != item["bytes"]
                or _path_sha256(path, artifact_id, f"terminal shard q={q}")
                != item["sha256"]
            ):
                _fail(artifact_id, "terminal-shard mismatch")
    resource = record.get("resource")
    expected_resource_keys = {
        "peak_live_state_bytes", "cache_payload_bytes",
        "combined_with_reserve_bytes", "scratch_limit_bytes",
        "maximum_numerical_workset_bytes", "numerical_workset_limit_bytes",
        "terminal_cache_peak_bytes", "authentication_cache_peak_bytes",
        "maximum_cache_window_bytes", "mapped_cache_limit_bytes",
        "peak_rss_bytes", "rss_limit_bytes", "wall_seconds",
        "wall_limit_seconds", "passed",
    }
    if type(resource) is not dict or set(resource) != expected_resource_keys:
        _fail(artifact_id, "resource/freshness mismatch")
    exact_resource = _a14_fixture_resource()
    for key in (
        "peak_live_state_bytes", "cache_payload_bytes",
        "combined_with_reserve_bytes", "scratch_limit_bytes",
        "maximum_numerical_workset_bytes", "numerical_workset_limit_bytes",
        "terminal_cache_peak_bytes", "authentication_cache_peak_bytes",
        "maximum_cache_window_bytes", "mapped_cache_limit_bytes",
        "rss_limit_bytes", "wall_limit_seconds", "passed",
    ):
        if resource.get(key) != exact_resource[key] or type(resource.get(key)) is not type(exact_resource[key]):
            _fail(artifact_id, "resource/freshness mismatch")
    if (
        type(resource.get("peak_rss_bytes")) is not int
        or not 0 < resource["peak_rss_bytes"] <= RSS_LIMIT
        or type(resource.get("wall_seconds")) is not float
        or not math.isfinite(resource["wall_seconds"])
        or not 0.0 < resource["wall_seconds"] <= WALL_LIMIT
    ):
        _fail(artifact_id, "resource/freshness mismatch")
    if fixture_mode:
        return
    source, physical_sha = _live_source_values(artifact_id)
    expected = {
        **{key: source[key] for key in SOURCE_HASH_KEYS if key in record},
        "physical_execution_gate_sha256": physical_sha,
        "dual_obstruction_gate_sha256": _path_sha256(
            DUAL_GATE_PATH, artifact_id, "dual obstruction gate",
        ),
        "cache_manifest_sha256": _path_sha256(
            CACHE_ROOT / "L10/CACHE_MANIFEST.json",
            artifact_id, "L10 cache manifest",
        ),
        "execution_authorization_sha256": _path_sha256(
            L10_AUTHORIZATION_PATH, artifact_id, "L10 authorization",
        ),
        "promotion_audit_sha256": _path_sha256(
            CONTROL_AUDIT_PATH, artifact_id, "control audit",
        ),
        "cached_control_l4_l8_gate_sha256": _path_sha256(
            CONTROL_GATE_PATH, artifact_id, "control gate",
        ),
        "cached_control_l4_l8_gate_audit_sha256": _path_sha256(
            CONTROL_AUDIT_PATH, artifact_id, "control audit",
        ),
        "l10_execution_authorization_gate_sha256": _path_sha256(
            L10_AUTHORIZATION_PATH, artifact_id, "L10 authorization",
        ),
        "production_obligation_validators_sha256": _path_sha256(
            Path(__file__).resolve(), artifact_id, "production validator",
        ),
    }
    _expect_values(
        artifact_id, record, expected,
        "history predecessor/provenance mismatch",
    )


def _validate_a11_a16_contract(
    artifact_id: str, record: dict[str, object], fixture_mode: bool,
) -> None:
    if artifact_id in {"A11_CONTROL_STAGE_GATE", "A15_L10_STAGE_GATE"}:
        _validate_stage_gate_contract(artifact_id, record, fixture_mode)
    elif artifact_id in {"A12_CONTROL_STAGE_AUDIT", "A16_L10_STAGE_AUDIT"}:
        _validate_stage_audit_contract(artifact_id, record, fixture_mode)
    elif artifact_id == "A13_L10_AUTHORIZATION":
        _validate_l10_authorization_contract(artifact_id, record, fixture_mode)
    elif artifact_id == "A14_L10_HISTORY":
        _validate_l10_history_contract(artifact_id, record, fixture_mode)


def _validate_a22_record(record: dict[str, object]) -> None:
    """Validate intrinsic launch-record invariants without filesystem authority."""
    schema = record.get("schema")
    roles = {"target_v012", "hostile_v004r4"}
    role = record.get("role")
    if schema in {
        "TARGET_V012_L12_ONE_WAY_AUTHORIZATION_V001",
        "HOSTILE_V004R4_L12_ONE_WAY_AUTHORIZATION_V001",
    }:
        expected_role = (
            "target_v012" if schema.startswith("TARGET_")
            else "hostile_v004r4"
        )
        if record.get("authorized_length") != 12 or role != expected_role:
            _fail("A22_TARGET_L12_AUTHORIZATION", "stage predecessor mismatch")
        return
    if schema == "V012_L12_WORKER_READY_V001":
        if (
            role not in roles
            or type(record.get("worker_id")) is not str
            or not record["worker_id"]
            or type(record.get("control_channel_id")) is not str
            or not record["control_channel_id"]
            or type(record.get("process_id")) is not int
            or record["process_id"] <= 0
            or type(record.get("ready_epoch")) is not int
            or record["ready_epoch"] <= 0
            or record.get("blocked_on_release") is not True
            or not _sha(record.get("process_start_token"))
            or not _sha(record.get("executable_sha256"))
            or not _sha(record.get("nonce_commitment_sha256"))
        ):
            _fail("A22_TARGET_L12_AUTHORIZATION", "launch/telemetry mismatch")
        for key in ("executable_path", "workspace_path", "output_path"):
            value = record.get(key)
            if (
                type(value) is not str or not value
                or not Path(value).is_absolute()
                or str(Path(value)) != value
                or ".." in Path(value).parts
            ):
                _fail("A22_TARGET_L12_AUTHORIZATION", "path/hash mismatch")
        return
    if schema == "V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002":
        workers = record.get("workers")
        ready_hashes = record.get("ready_sha256_by_role")
        auth_hashes = record.get("authorization_sha256_by_role")
        if type(auth_hashes) is not dict or set(auth_hashes) != roles:
            _fail("A22_TARGET_L12_AUTHORIZATION", "stage predecessor mismatch")
        if (
            type(workers) is not dict or set(workers) != roles
            or type(ready_hashes) is not dict or set(ready_hashes) != roles
            or any(not _sha(value) for value in auth_hashes.values())
            or len(set(auth_hashes.values())) != 2
            or record.get("memory_pressure") != "NORMAL"
        ):
            _fail("A22_TARGET_L12_AUTHORIZATION", "cross-role alias mismatch")
        identities: dict[str, set[object]] = {
            "process_id": set(), "worker_id": set(),
            "control_channel_id": set(), "nonce_commitment_sha256": set(),
        }
        epochs: dict[str, int] = {}
        for expected_role in sorted(roles):
            worker = workers[expected_role]
            if type(worker) is not dict or worker.get("role") != expected_role:
                _fail("A22_TARGET_L12_AUTHORIZATION", "cross-role alias mismatch")
            _validate_target("A22_TARGET_L12_AUTHORIZATION", worker)
            if ready_hashes[expected_role] != hashlib.sha256(
                canonical_json_bytes(worker)
            ).hexdigest():
                _fail("A22_TARGET_L12_AUTHORIZATION", "provenance mismatch")
            epochs[expected_role] = worker["ready_epoch"]
            for key in identities:
                identities[key].add(worker[key])
        if any(len(values) != 2 for values in identities.values()):
            _fail("A22_TARGET_L12_AUTHORIZATION", "cross-role alias mismatch")
        skew = abs(epochs["target_v012"] - epochs["hostile_v004r4"])
        if (
            type(record.get("created_epoch")) is not int
            or record["created_epoch"] < max(epochs.values())
            or type(record.get("launch_skew_seconds_max")) is not int
            or record["launch_skew_seconds_max"] != 60
            or type(record.get("observed_readiness_skew_seconds")) is not int
            or record["observed_readiness_skew_seconds"] != skew
            or skew > record["launch_skew_seconds_max"]
        ):
            _fail("A22_TARGET_L12_AUTHORIZATION", "launch/telemetry mismatch")
        return
    if schema == "V012_DUAL_L12_WORKER_RELEASE_V002":
        auth_hashes = record.get("authorization_sha256_by_role")
        epochs = record.get("release_epoch_by_role")
        releases = record.get("release_by_role")
        if (
            type(auth_hashes) is not dict or set(auth_hashes) != roles
            or any(not _sha(value) for value in auth_hashes.values())
            or len(set(auth_hashes.values())) != 2
            or type(epochs) is not dict or set(epochs) != roles
            or any(type(value) is not int or value <= 0 for value in epochs.values())
            or type(releases) is not dict or set(releases) != roles
            or not _sha(record.get("handshake_sha256"))
        ):
            _fail("A22_TARGET_L12_AUTHORIZATION", "stage predecessor mismatch")
        for expected_role in roles:
            row = releases[expected_role]
            if (
                type(row) is not dict
                or set(row) != {
                    "role", "worker_id", "process_id", "process_start_token",
                    "control_channel_id", "nonce_commitment_sha256",
                    "release_token_sha256",
                }
                or row.get("role") != expected_role
                or type(row.get("worker_id")) is not str or not row["worker_id"]
                or type(row.get("process_id")) is not int or row["process_id"] <= 0
                or type(row.get("control_channel_id")) is not str
                or not row["control_channel_id"]
                or not _sha(row.get("process_start_token"))
                or not _sha(row.get("nonce_commitment_sha256"))
                or row.get("release_token_sha256") != hashlib.sha256(
                    f"{record['handshake_sha256']}:{expected_role}:{epochs[expected_role]}".encode("ascii")
                ).hexdigest()
            ):
                _fail("A22_TARGET_L12_AUTHORIZATION", "unlock/audit binding mismatch")
        skew = abs(epochs["target_v012"] - epochs["hostile_v004r4"])
        if (
            type(record.get("observed_launch_skew_seconds")) is not int
            or record["observed_launch_skew_seconds"] != skew or skew > 60
        ):
            _fail("A22_TARGET_L12_AUTHORIZATION", "launch/telemetry mismatch")
        return
    if schema == "V012_L12_WORKER_RELEASE_COMMAND_V001":
        if (
            role not in roles
            or type(record.get("worker_id")) is not str or not record["worker_id"]
            or type(record.get("process_id")) is not int or record["process_id"] <= 0
            or type(record.get("control_channel_id")) is not str
            or not record["control_channel_id"]
            or type(record.get("release_epoch")) is not int
            or record["release_epoch"] <= 0
            or any(not _sha(record.get(key)) for key in (
                "process_start_token", "nonce_commitment_sha256",
                "handshake_sha256", "worker_release_sha256",
            ))
        ):
            _fail("A22_TARGET_L12_AUTHORIZATION", "unlock/audit binding mismatch")
        return
    if schema == "V012_L12_WORKER_RELEASE_ACK_V001":
        nonce = record.get("nonce_hex")
        if (
            role not in roles
            or type(record.get("worker_id")) is not str or not record["worker_id"]
            or type(record.get("process_id")) is not int or record["process_id"] <= 0
            or type(record.get("control_channel_id")) is not str
            or not record["control_channel_id"]
            or not _sha(record.get("process_start_token"))
            or not _sha(record.get("ack_sha256"))
            or type(nonce) is not str or len(nonce) != 64
            or any(character not in "0123456789abcdef" for character in nonce)
        ):
            _fail("A22_TARGET_L12_AUTHORIZATION", "launch/telemetry mismatch")
        return
    if schema == "V012_L12_WORKER_COMPLETION_V001":
        output_path = record.get("output_path")
        if (
            role not in roles
            or type(record.get("worker_id")) is not str
            or not record["worker_id"]
            or type(record.get("process_id")) is not int
            or record["process_id"] <= 0
            or not _sha(record.get("process_start_token"))
            or type(record.get("control_channel_id")) is not str
            or not record["control_channel_id"]
            or type(output_path) is not str
            or not output_path
            or not Path(output_path).is_absolute()
            or str(Path(output_path)) != output_path
            or ".." in Path(output_path).parts
            or not _sha(record.get("output_sha256"))
            or type(record.get("completion_epoch")) is not int
            or record["completion_epoch"] <= 0
            or record.get("blocked_on_orchestrator_close") is not True
        ):
            _fail("A22_TARGET_L12_AUTHORIZATION", "launch/telemetry mismatch")
        return


def _first_fixture_difference(
    actual: object, expected: object, path: tuple[str, ...] = (),
) -> tuple[str, ...] | None:
    if type(actual) is not type(expected):
        return path
    if type(expected) is dict:
        if set(actual) != set(expected):
            return path
        for key in sorted(expected):
            difference = _first_fixture_difference(
                actual[key], expected[key], path + (key,),
            )
            if difference is not None:
                return difference
        return None
    if type(expected) is list:
        if len(actual) != len(expected):
            return path
        for index, (left, right) in enumerate(zip(actual, expected)):
            difference = _first_fixture_difference(
                left, right, path + (str(index),),
            )
            if difference is not None:
                return difference
        return None
    return None if actual == expected else path


def _fixture_variant(artifact_id: str, record: dict[str, object]) -> int:
    schema = record.get("schema")
    for index, spec in enumerate(TARGET_SPECS[artifact_id]):
        if spec.schema == schema:
            return index
    return 0


def _validate_fixture_projection(
    artifact_id: str, record: dict[str, object],
) -> None:
    """Reconstruct a synthetic record against its frozen native projection.

    This is not a mutation-label oracle: the first differing native field alone
    determines the refusal class.  Production paths perform the same binding
    against authenticated predecessors before calling this schema validator.
    """
    if artifact_id == "A22_TARGET_L12_AUTHORIZATION":
        return
    expected = _native_fixture(artifact_id, _fixture_variant(artifact_id, record))
    path = _first_fixture_difference(record, expected)
    if path is None:
        return
    joined = ".".join(path).lower()
    leaf = path[-1].lower() if path else ""
    if "absence_census" in joined or leaf in {
        "physical_history_executed", "physical_cache_payload_created",
        "payload_or_history_executed", "physical_gate_or_history_executed",
    }:
        _fail(artifact_id, "absence census mismatch")
    if "handshake" in joined or "telemetry" in joined or "launch" in joined:
        _fail(artifact_id, "launch/telemetry mismatch")
    if "resource" in joined or "epoch" in leaf:
        _fail(artifact_id, "resource/freshness mismatch")
    if "terminal_shard" in joined:
        _fail(artifact_id, "terminal-shard mismatch")
    if artifact_id == "A18_L10_CROSS_GATE" and (
        joined.startswith("target.") or joined.startswith("hostile.")
        or "comparison" in joined
    ):
        _fail(artifact_id, "L10 cross-projection mismatch")
    if leaf in {"authorized_lengths", "authorized_cache_lengths"} or (
        "edge_layout" in joined
    ):
        _fail(artifact_id, "ordered census mismatch")
    if ("history" in joined or "histories" in joined) or leaf in {
        "l", "events", "dimension", "preterminal_dimension", "edges",
        "rows", "comparison",
    }:
        _fail(artifact_id, "history projection mismatch")
    if "compatibility" in joined or "predecessor" in joined or "physical_execution_gate." in joined or leaf in {
        "dual_obstruction_gate_sha256", "schedule_sha256",
        "physical_execution_gate_sha256", "sealed_input_commit",
    } or leaf.startswith(("v006_", "v007_", "v008_", "v009_", "v010_", "v011_")):
        _fail(artifact_id, "stage predecessor mismatch")
    if any(token in joined for token in (
        "execution_authorization", "promotion_audit", "stage_gate_sha256",
        "gate_audit_sha256", "unlock_audit_binding",
        "physical_gate_hostile_audit", "release_only_after_both",
    )):
        _fail(artifact_id, "unlock/audit binding mismatch")
    if leaf == "l10_cross_gate_sha256" or "l10_cross_projection" in joined:
        _fail(artifact_id, "L10 cross-projection mismatch")
    if leaf == "provenance":
        _fail(artifact_id, "provenance mismatch")
    if joined.startswith("checks.") or leaf in {
        "checks", "checks_total", "checks_passed", "failures",
    }:
        _fail(artifact_id, "counter reconstruction mismatch")
    if leaf in {"role", "auditor_role"} or "independent_hostile_audit" in joined:
        _fail(artifact_id, "cross-role alias mismatch")
    if artifact_id == "A17_HOSTILE_L12_ELIGIBILITY":
        if joined.startswith("l12_cache_manifest."):
            _fail(
                artifact_id,
                "cache census/semantics mismatch"
                if leaf == "path" else "L12 cross-projection mismatch",
            )
        if joined.startswith("cached_l10_gate."):
            _fail(
                artifact_id,
                "history projection mismatch"
                if leaf == "path" else "L10 cross-projection mismatch",
            )
        if joined.startswith("independent_audit."):
            _fail(artifact_id, "unlock/audit binding mismatch")
        if joined.startswith("preflight_result."):
            _fail(artifact_id, "stage predecessor mismatch")
    if "sha256" in leaf or leaf in {
        "files", "method", "builder", "consumer", "preflight", "freeze",
        "independent_audit", "cached_l10_gate", "l12_cache_manifest",
    }:
        _fail(artifact_id, "provenance mismatch")
    if any(token in joined for token in (
        "payload", "cache", "lineage", "admission", "offset", "mask",
    )):
        _fail(artifact_id, "cache census/semantics mismatch")
    if leaf in {"classification", "status", "schema", "claim_boundary", "auditor_role"}:
        _fail(artifact_id, "identity/claim mismatch")
    _fail(artifact_id, "provenance mismatch")


def _validate_target(
    artifact_id: str, record: object, *, fixture_mode: bool = False,
) -> dict[str, object]:
    if type(record) is not dict:
        _fail(artifact_id, "exact key census mismatch")
    spec = _spec_for_record(artifact_id, record)
    if set(record) != spec.keys:
        _fail(artifact_id, "exact key census mismatch")
    for key, expected in spec.identity:
        if record.get(key) != expected or type(record.get(key)) is not type(expected):
            _fail(
                artifact_id,
                (
                    "cross-role alias mismatch"
                    if record.get(key) == "target_v012"
                    else "identity/claim mismatch"
                )
                if artifact_id == "A17_HOSTILE_L12_ELIGIBILITY" and key == "role"
                else "identity/claim mismatch",
            )
    if spec.claim is not None and record.get("claim_boundary") != spec.claim:
        _fail(artifact_id, "identity/claim mismatch")
    _walk_native(record, artifact_id)
    if artifact_id in {
        "A11_CONTROL_STAGE_GATE",
        "A12_CONTROL_STAGE_AUDIT",
        "A13_L10_AUTHORIZATION",
        "A14_L10_HISTORY",
        "A15_L10_STAGE_GATE",
        "A16_L10_STAGE_AUDIT",
    }:
        _validate_a11_a16_contract(artifact_id, record, fixture_mode)
    for key in ("authorized_lengths", "authorized_cache_lengths"):
        if key in record:
            values = record[key]
            if type(values) is not list:
                _fail(artifact_id, "ordered census mismatch")
            if any(type(value) is not int for value in values):
                _fail(artifact_id, "exact integer mismatch")
            if values != sorted(set(values)):
                _fail(artifact_id, "ordered census mismatch")
    if "histories" in record:
        rows = record["histories"]
        lengths = [row.get("L") for row in rows if type(row) is dict]
        if len(lengths) != len(rows) or any(type(value) is not int for value in lengths) or lengths != sorted(set(lengths)):
            _fail(artifact_id, "ordered census mismatch")
        expected_lengths = (
            [4, 6, 8] if artifact_id == "A11_CONTROL_STAGE_GATE"
            else [10] if artifact_id == "A15_L10_STAGE_GATE"
            else None
        )
        if expected_lengths is not None and lengths != expected_lengths:
            _fail(artifact_id, "ordered census mismatch")
    for key in (
        "history_sha256_by_L", "canonical_v004_sha256_by_L",
        "cache_manifest_sha256_by_L", "manifest_sha256_by_L",
        "payload_census_by_L",
    ):
        if key in record:
            value = record[key]
            expected_keys = (
                {"4", "6", "8"}
                if artifact_id in {"A11_CONTROL_STAGE_GATE", "A12_CONTROL_STAGE_AUDIT"}
                else {"10"}
                if artifact_id in {"A15_L10_STAGE_GATE", "A16_L10_STAGE_AUDIT"}
                else {"4", "6", "8", "10", "12"}
            )
            if type(value) is not dict or set(value) != expected_keys:
                _fail(artifact_id, "ordered census mismatch")
    if artifact_id == "A05_FIVE_CACHE_SET" and (type(record.get("L")) is not int or record["L"] not in (4, 6, 8, 10, 12)):
        _fail(artifact_id, "cache census/semantics mismatch")
    if artifact_id in {"A10_CONTROL_HISTORIES", "A14_L10_HISTORY"}:
        sanctioned_nulls = SANCTIONED_NULL_STAGE_HASH_KEYS[artifact_id]
        for key in HISTORY_STAGE_HASH_KEYS:
            value = record.get(key)
            if key in sanctioned_nulls:
                if value is not None:
                    _fail(artifact_id, "stage predecessor mismatch")
            elif not _sha(value):
                _fail(artifact_id, "path/hash mismatch")
        length = record.get("L")
        allowed = (4, 6, 8) if artifact_id == "A10_CONTROL_HISTORIES" else (10,)
        if (
            type(length) is not int or length not in allowed
            or record.get("events") != length
            or type(record.get("events")) is not int
            or record.get("dimension") != math.comb(3 * length, length)
            or type(record.get("dimension")) is not int
            or record.get("preterminal_dimension")
            != math.comb(3 * length - 1, length - 1)
            or type(record.get("preterminal_dimension")) is not int
            or record.get("edges") != 3 * length
            or type(record.get("edges")) is not int
        ):
            _fail(artifact_id, "history projection mismatch")
        rows = record.get("rows")
        if (
            type(rows) is not list or len(rows) != length
            or [row.get("event") for row in rows if type(row) is dict]
            != list(range(1, length + 1))
        ):
            _fail(artifact_id, "ordered census mismatch")
        shards = record.get("terminal_shards")
        if (
            type(shards) is not list or len(shards) != length
            or [row.get("q") for row in shards if type(row) is dict]
            != list(range(length))
        ):
            _fail(artifact_id, "terminal-shard mismatch")
    if artifact_id == "A17_HOSTILE_L12_ELIGIBILITY" and record.get("role") != "hostile_v004r4":
        _fail(artifact_id, "cross-role alias mismatch")
    if artifact_id == "A18_L10_CROSS_GATE" and (
        type(record.get("L")) is not int or record.get("L") != 10
    ):
        _fail(artifact_id, "history projection mismatch")
    if artifact_id == "A18_L10_CROSS_GATE":
        target = record.get("target")
        hostile = record.get("hostile")
        target_keys = {
            "branch", "cached_L10_gate_sha256",
            "cached_L10_gate_audit_sha256", "history_sha256",
        }
        hostile_keys = {
            "branch", "cached_L10_gate_sha256",
            "l10_execution_authorization_gate_sha256",
            "independent_prepayload_audit_sha256", "history_sha256",
        }
        branch_keys = {
            "role", "method", "builder", "consumer", "preflight", "freeze",
            "preflight_result", "independent_audit", "cached_L10_gate",
            "L12_cache_manifest",
        }
        target_branch = target.get("branch") if type(target) is dict else None
        hostile_branch = hostile.get("branch") if type(hostile) is dict else None
        source_binding_keys = {"path", "sha256"}
        record_binding_keys = {
            "path", "sha256", "schema", "identity_field", "identity_value",
        }
        source_binding_names = ("method", "builder", "consumer", "preflight")
        record_binding_names = (
            "freeze", "preflight_result", "independent_audit",
            "cached_L10_gate", "L12_cache_manifest",
        )
        branch_binding_names = source_binding_names + record_binding_names
        if (
            type(target) is not dict or type(hostile) is not dict
            or set(target) != target_keys or set(hostile) != hostile_keys
            or type(target_branch) is not dict
            or type(hostile_branch) is not dict
            or set(target_branch) != branch_keys
            or set(hostile_branch) != branch_keys
            or target_branch.get("role") != "target_v012"
            or hostile_branch.get("role") != "hostile_v004r4"
            or any(
                type(branch.get(name)) is not dict
                or set(branch[name]) != source_binding_keys
                for branch in (target_branch, hostile_branch)
                for name in source_binding_names
            )
            or any(
                type(branch.get(name)) is not dict
                or set(branch[name]) != record_binding_keys
                or branch[name].get("identity_field")
                not in {"status", "classification"}
                for branch in (target_branch, hostile_branch)
                for name in record_binding_names
            )
            or len({
                target_branch[name]["path"] for name in branch_binding_names
            }) != len(branch_binding_names)
            or len({
                target_branch[name]["sha256"] for name in branch_binding_names
            }) != len(branch_binding_names)
            or len({
                hostile_branch[name]["path"] for name in branch_binding_names
            }) != len(branch_binding_names)
            or len({
                hostile_branch[name]["sha256"] for name in branch_binding_names
            }) != len(branch_binding_names)
            or not {
                target_branch[name]["path"] for name in branch_binding_names
            }.isdisjoint({
                hostile_branch[name]["path"] for name in branch_binding_names
            })
            or not {
                target_branch[name]["sha256"] for name in branch_binding_names
            }.isdisjoint({
                hostile_branch[name]["sha256"] for name in branch_binding_names
            })
            or target.get("cached_L10_gate_sha256")
            == hostile.get("cached_L10_gate_sha256")
            or target.get("history_sha256") == hostile.get("history_sha256")
        ):
            _fail(artifact_id, "cross-role alias mismatch")
    if artifact_id == "A20_SHARED_SCHEDULE_GATE":
        roles = record.get("roles")
        if type(roles) is not dict or set(roles) != {
            "target_v012", "hostile_v004r4",
        }:
            _fail(artifact_id, "ordered census mismatch")
        if any(
            type(value) is not dict or value.get("role") != role
            for role, value in roles.items()
        ):
            _fail(artifact_id, "cross-role alias mismatch")
        if any(
            value.get("ready_for_blocked_worker_start") is not True
            for value in roles.values()
        ):
            _fail(artifact_id, "stage predecessor mismatch")
    if artifact_id == "A22_TARGET_L12_AUTHORIZATION":
        _validate_a22_record(record)
    if fixture_mode:
        _validate_fixture_projection(artifact_id, record)
    return record


def validate_record(
    artifact_id: object, record: object, *, mutation_class: str,
    fixture_mode: bool = False,
) -> dict[str, object]:
    """Dispatch a parsed native record to the same exact production validator."""
    if type(artifact_id) is not str or artifact_id not in ARTIFACT_IDS:
        raise Refusal("unknown V012 production obligation artifact")
    if type(mutation_class) is not str or not mutation_class:
        raise Refusal("production obligation mutation identity malformed")
    if artifact_id in TARGET_ARTIFACT_IDS:
        return _validate_target(
            artifact_id, record, fixture_mode=fixture_mode,
        )
    final_auditor = _final_auditor()
    try:
        return final_auditor.validate_artifact(
            artifact_id, record, fixture_mode=fixture_mode,
        )
    except final_auditor.Refusal as error:
        raise Refusal(str(error)) from error


def positive_fixture(artifact_id: object, variant: int = 0) -> dict[str, object]:
    if type(artifact_id) is not str or artifact_id not in ARTIFACT_IDS:
        raise Refusal("unknown V012 fixture artifact")
    if type(variant) is not int or variant < 0:
        raise Refusal("fixture variant malformed")
    if artifact_id in TARGET_ARTIFACT_IDS:
        if variant >= len(TARGET_SPECS[artifact_id]):
            raise Refusal("fixture variant out of range")
        return copy.deepcopy(_native_fixture(artifact_id, variant))
    if variant != 0:
        raise Refusal("final-auditor fixture variant out of range")
    return _final_auditor().positive_fixture(artifact_id)


VALIDATOR_FUNCTION_BY_ARTIFACT: Final[dict[str, str]] = {
    **{
        artifact_id: "production_obligation_validators.validate_record"
        for artifact_id in TARGET_ARTIFACT_IDS
    },
    "A23_POSTRUN_TELEMETRY": "independent_final_auditor.validate_postrun_telemetry",
    "A24_TARGET_L12_HISTORY": "independent_final_auditor.validate_target_l12_history",
    "A25_HOSTILE_L12_HISTORY": "independent_final_auditor.validate_hostile_l12_history",
    "A26_FINAL_L12_AUDIT": "independent_final_auditor.validate_final_l12_audit",
    "A27_MUTATION_LEDGER": "independent_final_auditor.validate_mutation_ledger",
}


def _find_first(record: object, predicate) -> tuple[dict[str, object], str] | None:
    if type(record) is dict:
        for key, value in record.items():
            if predicate(key, value):
                return record, key
            found = _find_first(value, predicate)
            if found is not None:
                return found
    elif type(record) is list:
        for value in record:
            found = _find_first(value, predicate)
            if found is not None:
                return found
    return None


def _mutate_hash(
    record: dict[str, object], artifact_id: str, mutation_class: str,
) -> None:
    found = _find_first(record, lambda key, value: key.endswith("sha256") and type(value) is str)
    if found is None:
        raise Refusal("native fixture has no digest to mutate")
    # A distinct malformed digest per registered artifact/class proves the
    # 477 receipts are distinct executed mutations, not aliased replays.
    found[0][found[1]] = _h(f"{artifact_id}:{mutation_class}:invalid")[:-1]


def _replace_named_value(
    record: dict[str, object], names: tuple[str, ...], value: object,
) -> bool:
    for name in names:
        found = _find_first(record, lambda key, item, wanted=name: key == wanted)
        if found is not None:
            found[0][found[1]] = value
            return True
    return False


def _replace_named_hash(
    record: dict[str, object], names: tuple[str, ...], label: str,
) -> bool:
    return _replace_named_value(record, names, _h(label))


def _find_integer_slot(
    value: object,
) -> tuple[dict[str, object] | list[object], str | int] | None:
    if type(value) is dict:
        for key, item in value.items():
            if type(item) is int and key not in {
                "checks_total", "checks_passed",
            }:
                return value, key
            found = _find_integer_slot(item)
            if found is not None:
                return found
    elif type(value) is list:
        for index, item in enumerate(value):
            if type(item) is int:
                return value, index
            found = _find_integer_slot(item)
            if found is not None:
                return found
    return None


def _exact_integer_target(
    record: dict[str, object],
) -> tuple[dict[str, object] | list[object], str | int] | None:
    generic = _find_integer_slot(record)
    if generic is not None:
        return generic
    for key in (
        "checks_total", "L", "events", "authorized_length", "created_epoch",
        "observed_launch_skew_seconds", "observed_readiness_skew_seconds",
        "process_id", "ready_epoch", "release_epoch", "file_count",
        "captured_age_seconds",
    ):
        found = _find_first(
            record, lambda candidate, value, expected=key:
            candidate == expected and type(value) is int,
        )
        if found is not None:
            return found
    checks = _find_first(
        record, lambda key, value: key == "checks" and type(value) is dict,
    )
    if checks is not None and checks[0][checks[1]]:
        nested = checks[0][checks[1]]
        first = next(iter(nested))
        return nested, first
    return _find_integer_slot(record)


def mutated_fixture(
    artifact_id: object, mutation_class: object, variant: int = 0,
) -> tuple[dict[str, object] | bytes, str, str]:
    """Return a native-schema mutation and its artifact-specific refusal prefix."""
    if type(artifact_id) is not str or artifact_id not in ARTIFACT_IDS:
        raise Refusal("unknown V012 fixture artifact")
    if type(mutation_class) is not str or not mutation_class:
        raise Refusal("mutation class malformed")
    if type(variant) is not int or variant < 0:
        raise Refusal("mutation fixture variant malformed")
    if artifact_id in FINAL_ARTIFACT_IDS:
        if variant != 0:
            raise Refusal("final-auditor mutation fixture variant out of range")
        value, _expectation, description = _final_auditor().mutated_fixture(
            artifact_id, mutation_class,
        )
        return value, MUTATION_EXPECTED_REFUSAL[mutation_class], description
    record = positive_fixture(artifact_id, variant)
    description = f"{artifact_id} {mutation_class} native-schema mutation"
    if mutation_class == "M04_DUPLICATE_JSON_KEY":
        raw = canonical_json_bytes(record).decode("ascii").strip()
        duplicated_key = next(iter(record))
        prefix = json.dumps(duplicated_key, ensure_ascii=True) + ":null,"
        return ("{" + prefix + raw[1:] + "\n").encode("ascii"), MUTATION_EXPECTED_REFUSAL[mutation_class], description
    if mutation_class == "M05_NONFINITE_JSON":
        raw = canonical_json_bytes(record).decode("ascii").strip()
        return (raw[:-1] + ",\"nonfinite_probe\":NaN}\n").encode("ascii"), MUTATION_EXPECTED_REFUSAL[mutation_class], description
    if artifact_id == "A22_TARGET_L12_AUTHORIZATION" and mutation_class in {
        "M10_IDENTITY_OR_CLAIM", "M17_PROVENANCE_DROP_SWAP",
        "M19_STAGE_BYPASS", "M23_HANDSHAKE_TELEMETRY",
        "M24_UNLOCK_AUDIT_BINDING",
    }:
        if mutation_class == "M10_IDENTITY_OR_CLAIM":
            record["schema"] = "V012_L12_WORKER_RELEASE_ACK_UNAUTHENTICATED"
        elif mutation_class == "M17_PROVENANCE_DROP_SWAP":
            record["ready_sha256_by_role"]["target_v012"] = _h(
                "A22:wrong-ready-provenance"
            )
        elif mutation_class == "M19_STAGE_BYPASS":
            del record["authorization_sha256_by_role"]["target_v012"]
        elif mutation_class == "M23_HANDSHAKE_TELEMETRY":
            record["ack_sha256"] = _h("A22:wrong-release-ack")
        else:
            record["release_by_role"]["target_v012"][
                "release_token_sha256"
            ] = _h("A22:wrong-release-token")
    elif artifact_id == "A17_HOSTILE_L12_ELIGIBILITY" and mutation_class in {
        "M16_CROSS_ROLE_ALIAS", "M17_PROVENANCE_DROP_SWAP",
        "M18_CACHE_CENSUS_SEMANTICS", "M19_STAGE_BYPASS",
        "M20_HISTORY_PROJECTION", "M24_UNLOCK_AUDIT_BINDING",
        "M26_L10_CROSS_MISMATCH", "M27_L12_CROSS_MISMATCH",
    }:
        if mutation_class == "M16_CROSS_ROLE_ALIAS":
            record["role"] = "target_v012"
        elif mutation_class == "M17_PROVENANCE_DROP_SWAP":
            record["method"]["sha256"] = _h("A17:wrong-method-provenance")
        elif mutation_class == "M18_CACHE_CENSUS_SEMANTICS":
            record["L12_cache_manifest"]["path"] = "/synthetic/hostile/cache/L11.json"
        elif mutation_class == "M19_STAGE_BYPASS":
            record["preflight_result"]["sha256"] = _h("A17:wrong-preflight-stage")
        elif mutation_class == "M20_HISTORY_PROJECTION":
            record["cached_L10_gate"]["path"] = "/synthetic/hostile/CACHED_L9_GATE.json"
        elif mutation_class == "M24_UNLOCK_AUDIT_BINDING":
            record["independent_audit"]["sha256"] = _h("A17:wrong-audit-unlock")
        elif mutation_class == "M26_L10_CROSS_MISMATCH":
            record["cached_L10_gate"]["sha256"] = _h("A17:wrong-l10-cross")
        else:
            record["L12_cache_manifest"]["sha256"] = _h("A17:wrong-l12-cross")
    elif mutation_class == "M01_MISSING_KEY":
        if "claim_boundary" in record:
            del record["claim_boundary"]
        else:
            del record["role"]
    elif mutation_class == "M02_EXTRA_KEY":
        record["unregistered_authority"] = True
    elif mutation_class == "M03_WRONG_KEY_SAME_COUNT":
        key = "classification" if "classification" in record else "status" if "status" in record else "role"
        record[f"wrong_{key}"] = record.pop(key)
    elif mutation_class == "M06_BOOL_FOR_INT":
        found = _exact_integer_target(record)
        if found is None:
            found = _find_first(record, lambda key, value: key.endswith("sha256"))
        if found is None: _fail(artifact_id, "no exact-type mutation target")
        found[0][found[1]] = True
    elif mutation_class == "M07_FLOAT_INT_ALIAS":
        found = _exact_integer_target(record)
        if found is None:
            found = _find_first(record, lambda key, value: key.endswith("sha256"))
        if found is None: _fail(artifact_id, "no exact-type mutation target")
        value = found[0][found[1]]
        found[0][found[1]] = float(value) if type(value) is int else 1.0
    elif mutation_class == "M08_INT_FLOAT_ALIAS":
        found = _find_first(record, lambda key, value: type(value) is float)
        if found is None:
            found = _find_first(record, lambda key, value: key.endswith("sha256"))
            if found is None: _fail(artifact_id, "no float mutation target")
            found[0][found[1]] = 0
        else:
            found[0][found[1]] = int(found[0][found[1]])
    elif mutation_class == "M09_INT_OR_FLOAT_FOR_BOOL":
        found = _find_first(record, lambda key, value: type(value) is bool)
        if found is None:
            found = _find_first(record, lambda key, value: key in {"role", "classification", "status"})
        if found is None: _fail(artifact_id, "no exact boolean mutation target")
        found[0][found[1]] = 1
    elif mutation_class == "M10_IDENTITY_OR_CLAIM":
        if "claim_boundary" in record: record["claim_boundary"] = "PASS_UNBOUNDED_PHYSICS_OVERCLAIM"
        else: record["role"] = "UNRECOGNIZED_NATIVE_ROLE"
    elif mutation_class == "M11_HASH_OR_PATH":
        _mutate_hash(record, artifact_id, mutation_class)
    elif mutation_class in {"M12_SYMLINK_OR_WRITABLE", "M13_DESCRIPTOR_TOCTOU", "M28_PREMATURE_ARTIFACT"}:
        # These three classes are executed by the preflight's production
        # filesystem-custody/absence hooks, not represented as JSON aliases.
        return record, MUTATION_EXPECTED_REFUSAL[mutation_class], description
    elif mutation_class == "M14_COUNT_ARITHMETIC":
        if "checks_total" in record:
            record["checks_total"] += 1
        elif "checks" in record:
            first_check = next(iter(record["checks"]))
            record["checks"][first_check] += 1
        else:
            _mutate_hash(record, artifact_id, mutation_class)
    elif mutation_class == "M15_LIST_CENSUS_ORDER":
        key = "authorized_lengths" if "authorized_lengths" in record else "authorized_cache_lengths" if "authorized_cache_lengths" in record else "histories" if "histories" in record else None
        if key is not None:
            if len(record[key]) > 1:
                record[key] = list(reversed(record[key]))
            elif record[key]:
                record[key] = [copy.deepcopy(record[key][0]), copy.deepcopy(record[key][0])]
            else:
                _mutate_hash(record, artifact_id, mutation_class)
        elif type(record.get("rows")) is list and record["rows"]:
            record["rows"] = list(reversed(record["rows"]))
        elif "payload_census_by_L" in record:
            record["payload_census_by_L"]["5"] = record[
                "payload_census_by_L"
            ].pop("4")
        elif "history_sha256_by_L" in record:
            first = sorted(record["history_sha256_by_L"])[0]
            record["history_sha256_by_L"]["5"] = record[
                "history_sha256_by_L"
            ].pop(first)
        elif artifact_id == "A20_SHARED_SCHEDULE_GATE":
            record["roles"]["hostile_alias"] = record["roles"].pop(
                "hostile_v004r4"
            )
        elif record.get("edge_layout"):
            record["edge_layout"][0] = None
        else:
            _mutate_hash(record, artifact_id, mutation_class)
    elif mutation_class == "M16_CROSS_ROLE_ALIAS":
        if artifact_id == "A18_L10_CROSS_GATE":
            record["hostile"]["history_sha256"] = record["target"]["history_sha256"]
        elif artifact_id == "A20_SHARED_SCHEDULE_GATE":
            record["roles"]["hostile_v004r4"]["role"] = "target_v012"
        elif "auditor_role" in record:
            record["auditor_role"] = "target_v012"
        elif "independent_hostile_audit" in record:
            record["independent_hostile_audit"]["path"] = (
                "/synthetic/target-role-alias.json"
            )
        else:
            record["role"] = "target_v012"
    elif mutation_class == "M17_PROVENANCE_DROP_SWAP":
        if artifact_id == "A01_FREEZE_AND_SOURCE_PACKET":
            record["files"]["METHOD.md"] = _h("A01:wrong-method-provenance")
        elif artifact_id in {
            "A12_CONTROL_STAGE_AUDIT", "A16_L10_STAGE_AUDIT",
        }:
            first = sorted(record["canonical_v004_sha256_by_L"])[0]
            record["canonical_v004_sha256_by_L"][first] = _h(
                f"{artifact_id}:wrong-reference-provenance"
            )
        elif artifact_id in {
            "A18_L10_CROSS_GATE", "A21_SHARED_SCHEDULE_AUDIT",
        }:
            record["checks"]["provenance"] += 1
            record["checks_total"] += 1
            record["checks_passed"] += 1
        elif artifact_id == "A20_SHARED_SCHEDULE_GATE":
            record["roles"]["target_v012"]["executable_sha256"] = _h(
                "A20:wrong-executable-provenance"
            )
        elif not _replace_named_hash(
            record,
            ("method_sha256", "builder_sha256", "consumer_sha256",
             "freeze_sha256", "preflight_result_sha256", "schedule_audit_sha256",
             "prebuild_hostile_audit_sha256"),
            f"{artifact_id}:wrong-provenance",
        ):
            found = _find_first(
                record, lambda key, value: key == "sha256" and type(value) is str,
            )
            if found is None:
                _fail(artifact_id, "no provenance mutation target")
            found[0][found[1]] = _h(f"{artifact_id}:wrong-provenance")
    elif mutation_class == "M19_STAGE_BYPASS":
        if artifact_id == "A02_NONPHYSICAL_PREFLIGHT":
            record["compatibility"]["superseded_v011_payloads_consumed"] = True
        elif artifact_id in {
            "A20_SHARED_SCHEDULE_GATE", "A21_SHARED_SCHEDULE_AUDIT",
        }:
            if artifact_id == "A20_SHARED_SCHEDULE_GATE":
                record["roles"]["target_v012"][
                    "ready_for_blocked_worker_start"
                ] = False
            else:
                record["schedule_sha256"] = _h(
                    f"{artifact_id}:wrong-stage-schedule"
                )
        elif artifact_id == "A09_CONTROL_AUTHORIZATION":
            record["physical_execution_gate"]["sha256"] = _h(
                "A09:wrong-stage-predecessor"
            )
        elif not _replace_named_hash(
            record,
            ("dual_obstruction_gate_sha256", "physical_execution_gate_sha256",
             "cached_control_l4_l8_gate_audit_sha256", "l10_cross_gate_sha256",
             "schedule_sha256", "v011_hostile_audit_obstruction_sha256"),
            f"{artifact_id}:wrong-stage-predecessor",
        ):
            record["sealed_input_commit"] = "0" * 40
    elif mutation_class == "M24_UNLOCK_AUDIT_BINDING":
        if artifact_id in {
            "A18_L10_CROSS_GATE", "A21_SHARED_SCHEDULE_AUDIT",
        }:
            record["checks"]["unlock_audit_binding"] += 1
            record["checks_total"] += 1
            record["checks_passed"] += 1
        elif artifact_id == "A20_SHARED_SCHEDULE_GATE":
            record["schedule"]["release_only_after_both_l12_authorizations"] = False
        elif not _replace_named_hash(
            record,
            ("execution_authorization_sha256", "promotion_audit_sha256",
             "l10_execution_authorization_gate_sha256",
             "cached_control_l4_l8_gate_audit_sha256",
             "stage_gate_sha256", "physical_execution_gate_sha256"),
            f"{artifact_id}:wrong-unlock-audit",
        ):
            binding = record.get("physical_gate_hostile_audit")
            if type(binding) is dict and "sha256" in binding:
                binding["sha256"] = _h(f"{artifact_id}:wrong-unlock-audit")
            else:
                _fail(artifact_id, "no unlock/audit mutation target")
    elif mutation_class == "M25_IMPORT_TARGET_VALIDATOR":
        # The preflight executes this assignment against its real independent-
        # source AST sink.  The native record stays unchanged deliberately.
        pass
    elif mutation_class == "M26_L10_CROSS_MISMATCH":
        if artifact_id == "A18_L10_CROSS_GATE":
            record["target"]["history_sha256"] = _h("A18:wrong-l10-cross")
        elif not _replace_named_hash(
            record, ("l10_cross_gate_sha256",),
            f"{artifact_id}:wrong-l10-cross",
        ):
            _fail(artifact_id, "no L10 cross mutation target")
    elif mutation_class == "M27_L12_CROSS_MISMATCH":
        if not _replace_named_hash(
            record, ("target_l12_execution_gate_sha256", "handshake_sha256"),
            f"{artifact_id}:wrong-l12-cross",
        ):
            _fail(artifact_id, "no L12 cross mutation target")
    elif mutation_class == "M18_CACHE_CENSUS_SEMANTICS":
        if "L" in record: record["L"] = 11
        elif "payload_census_by_L" in record: record["payload_census_by_L"]["4"]["file_count"] = -1
        else: _mutate_hash(record, artifact_id, mutation_class)
    elif mutation_class == "M20_HISTORY_PROJECTION":
        if "dimension" in record: record["dimension"] += 1
        elif "L" in record: record["L"] += 1
        elif "history_sha256_by_L" in record:
            first = sorted(record["history_sha256_by_L"])[0]
            record["history_sha256_by_L"][first] = _h(
                f"{artifact_id}:wrong-history-projection"
            )
        elif type(record.get("histories")) is list and record["histories"]:
            record["histories"][0]["sha256"] = _h(
                f"{artifact_id}:wrong-history-projection"
            )
        else: _mutate_hash(record, artifact_id, mutation_class)
    elif mutation_class == "M21_TERMINAL_SHARD":
        if record.get("terminal_shards"):
            record["terminal_shards"][0]["sha256"] = _h(
                f"{artifact_id}:wrong-terminal-shard"
            )
        elif "checks" in record and "terminal_shards" in record["checks"]:
            record["checks"]["terminal_shards"] += 1
            record["checks_total"] += 1
            record["checks_passed"] += 1
        else:
            _fail(artifact_id, "no terminal-shard mutation target")
    elif mutation_class == "M22_RESOURCE_FRESHNESS":
        resource = record.get("resource_snapshot") or record.get("resource") or record.get("resource_limits")
        if type(resource) is dict and "memory_pressure" in resource:
            resource["memory_pressure"] = "WARNING"
        elif "checks" in record and "resource_freshness" in record["checks"]:
            record["checks"]["resource_freshness"] += 1
            record["checks_total"] += 1
            record["checks_passed"] += 1
        else:
            _fail(artifact_id, "no resource/freshness mutation target")
    elif mutation_class == "M23_HANDSHAKE_TELEMETRY":
        if "observed_launch_skew_seconds" in record:
            record["observed_launch_skew_seconds"] = 61
        elif artifact_id == "A20_SHARED_SCHEDULE_GATE":
            record["schedule"]["launch_skew_seconds_max"] = 61
        elif "checks" in record and "handshake_telemetry" in record["checks"]:
            record["checks"]["handshake_telemetry"] += 1
            record["checks_total"] += 1
            record["checks_passed"] += 1
        else:
            _fail(artifact_id, "no launch/telemetry mutation target")
    elif mutation_class == "M29_WRONG_ABSENCE_VALUE":
        absence = record.get("absence_census")
        if type(absence) is dict and absence: absence[next(iter(absence))] = True
        elif "physical_history_executed" in record: record["physical_history_executed"] = True
        else: _fail(artifact_id, "no absence mutation target")
    else:
        _fail(artifact_id, f"mutation factory has no implementation for {mutation_class}")
    return record, MUTATION_EXPECTED_REFUSAL[mutation_class], description
