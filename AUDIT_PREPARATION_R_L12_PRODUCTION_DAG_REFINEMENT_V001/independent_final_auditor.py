#!/usr/bin/env python3
"""Independent, fail-closed validators for V012 obligations A23--A27.

The validators accept already parsed records or strict JSON bytes.  They do not
launch workers, create canonical artifacts, import target numerical code, or
perform physics.  ``fixture_mode`` admits only the packet's synthetic absolute
paths; production mode admits only the declared repository canonical paths.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import mmap
import os
import re
import stat
import struct
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Callable, Final

import numpy as np


ROOT: Final[Path] = Path(__file__).resolve().parent.parent
_SYNTHETIC_UPSTREAM_FIXTURE: Callable[
    [str, int], dict[str, object]
] | None = None
ROLES: Final[tuple[str, str]] = ("target_v012", "hostile_v004r4")
ARTIFACT_IDS: Final[tuple[str, ...]] = (
    "A23_POSTRUN_TELEMETRY",
    "A24_TARGET_L12_HISTORY",
    "A25_HOSTILE_L12_HISTORY",
    "A26_FINAL_L12_AUDIT",
    "A27_MUTATION_LEDGER",
)
TOLERANCE: Final[float] = 1.0e-8
RSS_LIMIT: Final[int] = 17_179_869_184
TARGET_MAPPED_LIMIT: Final[int] = 252_944_080
HOSTILE_MAPPED_LIMIT: Final[int] = 252_944_080
WALL_LIMIT: Final[float] = 21_600.0
DISK_MINIMUM: Final[int] = 19_201_889_580
WORKER_IDENTITY_KEYS: Final[set[str]] = {
    "worker_id", "process_id", "process_start_token", "executable_path",
    "executable_sha256", "control_channel_id", "nonce_commitment_sha256",
}
AUTHORITY_INSTANCE_CENSUS: Final[dict[str, int]] = {
    "A01_FREEZE_AND_SOURCE_PACKET": 1,
    "A02_NONPHYSICAL_PREFLIGHT": 1,
    "A03_PREPAYLOAD_AUDIT": 1,
    "A04_UNIVERSAL_CUSTODY_GATE": 1,
    "A05_FIVE_CACHE_SET": 5,
    "A06_POSTBUILD_AUDIT": 1,
    "A07_BASE_PHYSICAL_GATE": 1,
    "A08_PHYSICAL_GATE_AUDIT": 1,
    "A09_CONTROL_AUTHORIZATION": 1,
    "A10_CONTROL_HISTORIES": 3,
    "A11_CONTROL_STAGE_GATE": 1,
    "A12_CONTROL_STAGE_AUDIT": 1,
    "A13_L10_AUTHORIZATION": 1,
    "A14_L10_HISTORY": 1,
    "A15_L10_STAGE_GATE": 1,
    "A16_L10_STAGE_AUDIT": 1,
    "A17_HOSTILE_L12_ELIGIBILITY": 1,
    "A18_L10_CROSS_GATE": 1,
    "A20_SHARED_SCHEDULE_GATE": 1,
    "A21_SHARED_SCHEDULE_AUDIT": 1,
    "A22_TARGET_L12_AUTHORIZATION": 12,
    "A23_POSTRUN_TELEMETRY": 1,
    "A24_TARGET_L12_HISTORY": 1,
    "A25_HOSTILE_L12_HISTORY": 1,
    "A27_MUTATION_LEDGER": 1,
}
A17_SOURCE_LABELS: Final[tuple[str, ...]] = (
    "method", "builder", "consumer", "preflight", "freeze",
    "preflight_result", "independent_audit", "cached_L10_gate",
    "L12_cache_manifest",
)
A17_RECORD_IDENTITIES: Final[
    dict[str, tuple[str, str, str]]
] = {
    "freeze": (
        "AUDIT_R_L12_PREFIX_HISTORY_STORAGE_CACHE_FREEZE_V004R4",
        "status", "FROZEN_BEFORE_CACHE_OR_HISTORY_OUTPUT",
    ),
    "preflight_result": (
        "HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT_V001",
        "classification", "PASS_HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT",
    ),
    "independent_audit": (
        "HOSTILE_V004R4_PREPAYLOAD_AUDIT_V001",
        "classification",
        "PASS_HOSTILE_V004R4_PREPAYLOAD_CONTROL_AND_SHARED_GATE_INTERFACE",
    ),
    "cached_L10_gate": (
        "HOSTILE_V004R4_CACHED_L10_GATE",
        "classification", "PASS_HOSTILE_V004R4_CACHED_L10",
    ),
    "L12_cache_manifest": (
        "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R4",
        "status", "COMPLETE_IMMUTABLE_HASH_PINNED_STORAGE_ONLY_CACHE",
    ),
}
A17_CANONICAL_RELATIVE_PATHS: Final[dict[str, str]] = {
    "method": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_METHOD.md",
    "builder": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/build_cache_v004r4.py",
    "consumer": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/consume_cache_v004r4.py",
    "preflight": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/validate_cache_preflight_v004r4.py",
    "freeze": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_MANIFEST_V004R4.json",
    "preflight_result": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PREFLIGHT_RESULT.json",
    "independent_audit": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_AUDIT_RESULT_V004R4.json",
    "cached_L10_gate": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHED_L10_GATE_V004R4.json",
    "L12_cache_manifest": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS/L12/CACHE_MANIFEST.json",
}
TARGET_BRANCH_CANONICAL_RELATIVE_PATHS: Final[dict[str, str]] = {
    "method": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/METHOD.md",
    "builder": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/build_target_cache.py",
    "consumer": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py",
    "preflight": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/validate_preflight.py",
    "freeze": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/FREEZE.json",
    "preflight_result": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_RESULT_V001.json",
    "independent_audit": "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json",
    "cached_L10_gate": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_V012.json",
    "L12_cache_manifest": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012/L12/CACHE_MANIFEST.json",
}
TARGET_BRANCH_RECORD_IDENTITIES: Final[
    dict[str, tuple[str, str, str]]
] = {
    "freeze": (
        "TARGET_L12_STORAGE_CACHE_FREEZE_V012", "status",
        "FROZEN_BEFORE_NONPHYSICAL_PREFLIGHT_V001_OUTPUT",
    ),
    "preflight_result": (
        "TARGET_L12_STORAGE_CACHE_NONPHYSICAL_PREFLIGHT_V012",
        "classification",
        "PASS_NONPHYSICAL_EXHAUSTIVE_INDEX_ALLOCATION_AND_HARD_LOCK_PREFLIGHT",
    ),
    "independent_audit": (
        "TARGET_V012_PREPAYLOAD_HOSTILE_AUDIT_V001", "classification",
        "PASS_TARGET_V012_PREPAYLOAD_CONTROL_PLANE",
    ),
    "cached_L10_gate": (
        "TARGET_V012_CACHED_L10_GATE", "classification",
        "PASS_TARGET_V012_CACHED_L10",
    ),
    "L12_cache_manifest": (
        "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012", "status",
        "COMPLETE_HASH_PINNED_TARGET_STORAGE_ONLY_CACHE",
    ),
}
AUTHORITY_CANONICAL_RELATIVE_PATHS: Final[dict[tuple[str, int], str]] = {
    ("A01_FREEZE_AND_SOURCE_PACKET", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/FREEZE.json",
    ("A02_NONPHYSICAL_PREFLIGHT", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_RESULT_V001.json",
    ("A03_PREPAYLOAD_AUDIT", 1): "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json",
    ("A04_UNIVERSAL_CUSTODY_GATE", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json",
    ("A06_POSTBUILD_AUDIT", 1): "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/POSTBUILD_PAYLOAD_AUDIT_V001.json",
    ("A07_BASE_PHYSICAL_GATE", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_EXECUTION_GATE_V012.json",
    ("A08_PHYSICAL_GATE_AUDIT", 1): "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_GATE_HOSTILE_AUDIT_V001.json",
    ("A09_CONTROL_AUTHORIZATION", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CONTROL_EXECUTION_AUTHORIZATION_GATE_V012.json",
    ("A11_CONTROL_STAGE_GATE", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_CONTROL_L4_L8_GATE_V012.json",
    ("A12_CONTROL_STAGE_AUDIT", 1): "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json",
    ("A13_L10_AUTHORIZATION", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/L10_EXECUTION_AUTHORIZATION_GATE_V012.json",
    ("A14_L10_HISTORY", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L10.json",
    ("A15_L10_STAGE_GATE", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_V012.json",
    ("A16_L10_STAGE_AUDIT", 1): "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_AUDIT_V001.json",
    ("A18_L10_CROSS_GATE", 1): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_HOSTILE_L10_CROSS_GATE_V001.json",
    ("A20_SHARED_SCHEDULE_GATE", 1): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_SCHEDULE_GATE_V001.json",
    ("A21_SHARED_SCHEDULE_AUDIT", 1): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/TARGET_L12_EXECUTION_GATE_V012.json",
    ("A22_TARGET_L12_AUTHORIZATION", 2): "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_L12_EXECUTION_GATE_V004R4.json",
    ("A22_TARGET_L12_AUTHORIZATION", 3): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_READY_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 4): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_READY_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 5): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_LAUNCH_HANDSHAKE_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 6): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_WORKER_RELEASE_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 7): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_COMMAND_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 8): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_COMMAND_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 9): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_ACK_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 10): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_ACK_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 11): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_COMPLETION_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 12): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_COMPLETION_V001.json",
    ("A23_POSTRUN_TELEMETRY", 1): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_TELEMETRY_V001.json",
    ("A24_TARGET_L12_HISTORY", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L12.json",
    ("A25_HOSTILE_L12_HISTORY", 1): "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json",
    ("A27_MUTATION_LEDGER", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_MUTATION_LEDGER_V001.json",
}
for _instance, _length in enumerate((4, 6, 8, 10, 12), start=1):
    AUTHORITY_CANONICAL_RELATIVE_PATHS[("A05_FIVE_CACHE_SET", _instance)] = (
        f"DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012/L{_length}/CACHE_MANIFEST.json"
    )
for _instance, _length in enumerate((4, 6, 8), start=1):
    AUTHORITY_CANONICAL_RELATIVE_PATHS[("A10_CONTROL_HISTORIES", _instance)] = (
        f"DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L{_length}.json"
    )
if set(AUTHORITY_CANONICAL_RELATIVE_PATHS) != {
    (artifact_id, instance)
    for artifact_id, count in AUTHORITY_INSTANCE_CENSUS.items()
    if artifact_id != "A17_HOSTILE_L12_ELIGIBILITY"
    for instance in range(1, count + 1)
}:
    raise RuntimeError("internal canonical authority path census mismatch")
OBLIGATION_MATRIX_PATH: Final[Path] = (
    ROOT / "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012"
    / "AUDIT_OBLIGATIONS_V001.json"
)
OBLIGATION_MATRIX_RELATIVE: Final[str] = (
    "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/"
    "AUDIT_OBLIGATIONS_V001.json"
)
OBLIGATION_MATRIX_SHA256: Final[str] = (
    "49a1a5901249c0476ebd775d60b9342436e4391a2a97b9c08f1082247b719e77"
)
MUTATION_LEDGER_SCHEMA: Final[str] = (
    "TARGET_V012_PREPAYLOAD_MUTATION_LEDGER_V001"
)
MUTATION_LEDGER_CLASSIFICATION: Final[str] = (
    "PASS_EXECUTED_PREREGISTERED_MUTATION_ASSIGNMENTS"
)
MUTATION_LEDGER_CLAIM: Final[str] = (
    "EXECUTED_PRODUCTION_VALIDATOR_MUTATION_EVIDENCE_ONLY__NO_GATE_CACHE_"
    "HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
)
PRODUCTION_FIXTURE_HOOK: Final[str] = (
    "build_target_cache.validate_audit_obligation_fixture"
)
SOURCE_FILE_KEYS: Final[set[str]] = {
    "METHOD.md", "build_target_cache.py", "consume_target_cache.py",
    "production_obligation_validators.py", "validate_preflight.py",
}
MUTATION_REFUSAL: Final[dict[str, str]] = {
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
MUTATION_ASSIGNMENTS: Final[dict[str, tuple[str, ...]]] = {
    "A23_POSTRUN_TELEMETRY": (
        "M01_MISSING_KEY", "M02_EXTRA_KEY", "M03_WRONG_KEY_SAME_COUNT",
        "M04_DUPLICATE_JSON_KEY", "M05_NONFINITE_JSON", "M06_BOOL_FOR_INT",
        "M07_FLOAT_INT_ALIAS", "M08_INT_FLOAT_ALIAS", "M10_IDENTITY_OR_CLAIM",
        "M11_HASH_OR_PATH", "M12_SYMLINK_OR_WRITABLE", "M13_DESCRIPTOR_TOCTOU",
        "M15_LIST_CENSUS_ORDER", "M16_CROSS_ROLE_ALIAS",
        "M17_PROVENANCE_DROP_SWAP", "M22_RESOURCE_FRESHNESS",
        "M23_HANDSHAKE_TELEMETRY", "M27_L12_CROSS_MISMATCH",
        "M28_PREMATURE_ARTIFACT",
    ),
    "A24_TARGET_L12_HISTORY": (
        "M01_MISSING_KEY", "M02_EXTRA_KEY", "M04_DUPLICATE_JSON_KEY",
        "M05_NONFINITE_JSON", "M06_BOOL_FOR_INT", "M07_FLOAT_INT_ALIAS",
        "M08_INT_FLOAT_ALIAS", "M09_INT_OR_FLOAT_FOR_BOOL",
        "M10_IDENTITY_OR_CLAIM", "M11_HASH_OR_PATH",
        "M12_SYMLINK_OR_WRITABLE", "M13_DESCRIPTOR_TOCTOU",
        "M17_PROVENANCE_DROP_SWAP", "M20_HISTORY_PROJECTION",
        "M21_TERMINAL_SHARD", "M22_RESOURCE_FRESHNESS",
        "M24_UNLOCK_AUDIT_BINDING", "M27_L12_CROSS_MISMATCH",
        "M28_PREMATURE_ARTIFACT",
    ),
    "A25_HOSTILE_L12_HISTORY": (
        "M01_MISSING_KEY", "M02_EXTRA_KEY", "M04_DUPLICATE_JSON_KEY",
        "M05_NONFINITE_JSON", "M06_BOOL_FOR_INT", "M07_FLOAT_INT_ALIAS",
        "M08_INT_FLOAT_ALIAS", "M09_INT_OR_FLOAT_FOR_BOOL",
        "M10_IDENTITY_OR_CLAIM", "M11_HASH_OR_PATH",
        "M12_SYMLINK_OR_WRITABLE", "M13_DESCRIPTOR_TOCTOU",
        "M16_CROSS_ROLE_ALIAS", "M17_PROVENANCE_DROP_SWAP",
        "M20_HISTORY_PROJECTION", "M21_TERMINAL_SHARD",
        "M22_RESOURCE_FRESHNESS", "M24_UNLOCK_AUDIT_BINDING",
        "M27_L12_CROSS_MISMATCH", "M28_PREMATURE_ARTIFACT",
    ),
    "A26_FINAL_L12_AUDIT": (
        "M01_MISSING_KEY", "M02_EXTRA_KEY", "M03_WRONG_KEY_SAME_COUNT",
        "M04_DUPLICATE_JSON_KEY", "M05_NONFINITE_JSON", "M06_BOOL_FOR_INT",
        "M07_FLOAT_INT_ALIAS", "M08_INT_FLOAT_ALIAS",
        "M09_INT_OR_FLOAT_FOR_BOOL", "M10_IDENTITY_OR_CLAIM",
        "M11_HASH_OR_PATH", "M12_SYMLINK_OR_WRITABLE",
        "M13_DESCRIPTOR_TOCTOU", "M14_COUNT_ARITHMETIC",
        "M15_LIST_CENSUS_ORDER", "M16_CROSS_ROLE_ALIAS",
        "M17_PROVENANCE_DROP_SWAP", "M20_HISTORY_PROJECTION",
        "M21_TERMINAL_SHARD", "M22_RESOURCE_FRESHNESS",
        "M23_HANDSHAKE_TELEMETRY", "M24_UNLOCK_AUDIT_BINDING",
        "M25_IMPORT_TARGET_VALIDATOR", "M26_L10_CROSS_MISMATCH",
        "M27_L12_CROSS_MISMATCH", "M28_PREMATURE_ARTIFACT",
    ),
    "A27_MUTATION_LEDGER": tuple(f"M{index:02d}_{name}" for index, name in (
        (1, "MISSING_KEY"), (2, "EXTRA_KEY"), (3, "WRONG_KEY_SAME_COUNT"),
        (4, "DUPLICATE_JSON_KEY"), (5, "NONFINITE_JSON"), (6, "BOOL_FOR_INT"),
        (7, "FLOAT_INT_ALIAS"), (8, "INT_FLOAT_ALIAS"),
        (9, "INT_OR_FLOAT_FOR_BOOL"), (10, "IDENTITY_OR_CLAIM"),
        (11, "HASH_OR_PATH"), (12, "SYMLINK_OR_WRITABLE"),
        (13, "DESCRIPTOR_TOCTOU"), (14, "COUNT_ARITHMETIC"),
        (15, "LIST_CENSUS_ORDER"), (16, "CROSS_ROLE_ALIAS"),
        (17, "PROVENANCE_DROP_SWAP"), (18, "CACHE_CENSUS_SEMANTICS"),
        (19, "STAGE_BYPASS"), (20, "HISTORY_PROJECTION"),
        (21, "TERMINAL_SHARD"), (22, "RESOURCE_FRESHNESS"),
        (23, "HANDSHAKE_TELEMETRY"), (24, "UNLOCK_AUDIT_BINDING"),
        (25, "IMPORT_TARGET_VALIDATOR"), (26, "L10_CROSS_MISMATCH"),
        (27, "L12_CROSS_MISMATCH"), (28, "PREMATURE_ARTIFACT"),
        (29, "WRONG_ABSENCE_VALUE"),
    )),
}


class Refusal(RuntimeError):
    """Controlled final-auditor refusal."""


def _fail(artifact_id: str, detail: str) -> None:
    raise Refusal(f"{artifact_id}: {detail}")


def _strict_json(value: object, artifact_id: str) -> object:
    if type(value) not in (bytes, str):
        return value
    try:
        text = value.decode("utf-8") if type(value) is bytes else value
    except UnicodeDecodeError as error:
        _fail(artifact_id, "malformed UTF-8 JSON")

    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, item in items:
            if key in result:
                _fail(artifact_id, "duplicate JSON key")
            result[key] = item
        return result

    def constant(_token: str) -> object:
        _fail(artifact_id, "nonfinite JSON constant")

    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except Refusal:
        raise
    except (TypeError, ValueError, json.JSONDecodeError) as error:
        raise Refusal(f"{artifact_id}: malformed JSON") from error


def canonical_json_bytes(record: object) -> bytes:
    try:
        return (json.dumps(
            record, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise Refusal("record is not finite canonical JSON") from error


def record_sha256(record: object) -> str:
    return hashlib.sha256(canonical_json_bytes(record)).hexdigest()


def _keys(value: object, expected: set[str], artifact_id: str, label: str) -> dict[str, object]:
    if type(value) is not dict or set(value) != expected or any(type(k) is not str for k in value):
        _fail(artifact_id, f"{label} exact key census mismatch")
    return value


def _string(value: object, artifact_id: str, label: str) -> str:
    if type(value) is not str or not value:
        _fail(artifact_id, f"{label} must be an exact nonempty string")
    return value


def _integer(value: object, artifact_id: str, label: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        _fail(artifact_id, f"{label} must be an exact integer >= {minimum}")
    return value


def _float(value: object, artifact_id: str, label: str, minimum: float = 0.0) -> float:
    if type(value) is not float or not math.isfinite(value) or value < minimum:
        _fail(artifact_id, f"{label} must be an exact finite float >= {minimum}")
    return value


def _boolean(value: object, artifact_id: str, label: str) -> bool:
    if type(value) is not bool:
        _fail(artifact_id, f"{label} must be an exact boolean")
    return value


def _sha(value: object, artifact_id: str, label: str) -> str:
    text = _string(value, artifact_id, label)
    if (
        len(text) != 64
        or any(c not in "0123456789abcdef" for c in text)
        or len(set(text)) == 1
    ):
        _fail(artifact_id, f"{label} must be a lowercase SHA-256")
    return text


def _role_map(value: object, artifact_id: str, label: str) -> dict[str, object]:
    return _keys(value, set(ROLES), artifact_id, label)


def _path(value: object, expected: str, artifact_id: str, label: str) -> str:
    text = _string(value, artifact_id, label)
    if "\x00" in text or not text.startswith("/") or str(Path(text)) != text or text != expected:
        _fail(artifact_id, f"{label} canonical path mismatch")
    return text


def _custody(value: object, artifact_id: str) -> dict[str, object]:
    record = _keys(value, {
        "immutable_ordinary_file", "descriptor_authenticated",
        "rehash_after_validation", "atomically_created_once",
        "canonical_artifact_created_by_fixture",
    }, artifact_id, "custody")
    for key in record:
        _boolean(record[key], artifact_id, f"custody {key}")
    expected = {
        "immutable_ordinary_file": True,
        "descriptor_authenticated": True,
        "rehash_after_validation": True,
        "atomically_created_once": True,
        "canonical_artifact_created_by_fixture": False,
    }
    if record != expected:
        _fail(artifact_id, "custody/creation contract mismatch")
    return record


def _expected_path(role: str, kind: str, fixture_mode: bool, q: int | None = None) -> str:
    if fixture_mode:
        extension = ".c128" if role == "hostile_v004r4" else ".npy"
        suffix = f"/q_{q:02d}{extension}" if q is not None else ""
        return f"/synthetic/{role}/{kind}{suffix}"
    if kind == "telemetry":
        return str(ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_TELEMETRY_V001.json")
    if role == "target_v012":
        if kind == "history":
            return str(ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L12.json")
        assert q is not None
        return str(ROOT / f"DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/L12/sharp/prefix_11/q_{q:02d}.npy")
    if kind == "history":
        return str(ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json")
    assert q is not None
    return str(ROOT / f"AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES/L12/sharp/prefix_11/q_{q:02d}.c128")


def _expected_executable(role: str, fixture_mode: bool) -> str:
    if fixture_mode:
        return {
            "target_v012": "/synthetic/v012/target/consume_target_cache.py",
            "hostile_v004r4": "/synthetic/v004r4/hostile/consume_cache_v004r4.py",
        }[role]
    return str(ROOT / (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py"
        if role == "target_v012"
        else "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/consume_cache_v004r4.py"
    ))


def _history_schema(role: str) -> str:
    return "TARGET_CACHED_PREFIX_HISTORY_V012" if role == "target_v012" else "HOSTILE_CACHED_PREFIX_HISTORY_V004R4"


def _history_basis(role: str) -> str:
    return "TARGET_FIXED_WORDS_LEXICOGRAPHIC_COMBINATION_ORDER" if role == "target_v012" else "REVERSED_COMBINATION__FULL_MASK"


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("ascii")).hexdigest()


def _validate_samples(
    samples_value: object, launch: int, completion: int, expected_peak_rss: int,
    artifact_id: str, role: str, identity: dict[str, object],
) -> None:
    if type(samples_value) is not list or len(samples_value) < 2:
        _fail(artifact_id, f"{role} runtime sample census mismatch")
    epochs: list[int] = []
    rss: list[int] = []
    for sample in samples_value:
        row = _keys(sample, {
            "captured_epoch", "rss_bytes", "process_id",
            "process_start_token", "executable_path", "executable_sha256",
        }, artifact_id, f"{role} runtime sample")
        for key in (
            "process_id", "process_start_token", "executable_path",
            "executable_sha256",
        ):
            if row[key] != identity[key] or type(row[key]) is not type(identity[key]):
                _fail(artifact_id, f"{role} runtime sample identity mismatch")
        epochs.append(_integer(row["captured_epoch"], artifact_id, "sample epoch", 1))
        rss.append(_integer(row["rss_bytes"], artifact_id, "sample RSS", 1))
    if (
        epochs[0] > launch or epochs[-1] < completion
        or epochs != sorted(set(epochs))
    ):
        _fail(artifact_id, f"{role} runtime sample order/boundary mismatch")
    if any(right - left > 60 for left, right in zip(epochs, epochs[1:])):
        _fail(artifact_id, f"{role} runtime sample cadence exceeded")
    if max(rss) != expected_peak_rss:
        _fail(artifact_id, f"{role} reconstructed RSS peak mismatch")


def validate_postrun_telemetry(record: object, *, fixture_mode: bool = False) -> dict[str, object]:
    aid = "A23_POSTRUN_TELEMETRY"
    record = _strict_json(record, aid)
    row = _keys(record, {
        "schema", "classification", "shared_gate_sha256", "schedule_audit_sha256",
        "dual_launch_handshake_sha256", "worker_release_sha256",
        "authorization_sha256_by_role", "worker_identity_by_role",
        "release_command_sha256_by_role", "release_ack_sha256_by_role",
        "completion_sha256_by_role",
        "launch_epoch_by_role",
        "completion_epoch_by_role", "wall_seconds_by_role",
        "peak_rss_bytes_by_role", "rss_peak_semantics",
        "peak_mapped_bytes_by_role",
        "mapped_peak_semantics",
        "runtime_samples_by_role", "free_disk_bytes_samples", "exit_code_by_role",
        "output_path_by_role", "output_sha256_by_role", "claim_boundary",
    }, aid, "telemetry")
    if row["schema"] != "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001" or row["classification"] != "COMPLETE_SHARED_L12_TELEMETRY":
        _fail(aid, "schema/classification mismatch")
    if row["mapped_peak_semantics"] != (
        "CONSERVATIVE_AUTHENTICATION_CACHE_CERTIFICATE__"
        "NOT_OS_VIRTUAL_MEMORY"
    ):
        _fail(aid, "mapped peak semantics mismatch")
    if row["rss_peak_semantics"] != (
        "LAUNCHER_SAMPLED_CURRENT_RSS_AT_MOST_30_SECONDS__"
        "NOT_OS_HIGH_WATER"
    ):
        _fail(aid, "RSS peak semantics mismatch")
    provenance = [
        _sha(row[key], aid, key) for key in (
            "shared_gate_sha256", "schedule_audit_sha256",
            "dual_launch_handshake_sha256", "worker_release_sha256",
        )
    ]
    auth = _role_map(row["authorization_sha256_by_role"], aid, "authorization hashes")
    provenance.extend(_sha(auth[role], aid, f"{role} authorization") for role in ROLES)
    identities = _role_map(row["worker_identity_by_role"], aid, "worker identities")
    command_hashes = _role_map(
        row["release_command_sha256_by_role"], aid, "release command hashes",
    )
    ack_hashes = _role_map(
        row["release_ack_sha256_by_role"], aid, "release ACK hashes",
    )
    completion_hashes = _role_map(
        row["completion_sha256_by_role"], aid, "worker completion hashes",
    )
    uniqueness = {
        key: set() for key in (
            "worker_id", "process_id", "process_start_token",
            "control_channel_id", "nonce_commitment_sha256",
        )
    }
    for role in ROLES:
        identity = _keys(
            identities[role], WORKER_IDENTITY_KEYS, aid,
            f"{role} worker identity",
        )
        _string(identity["worker_id"], aid, f"{role} worker id")
        _integer(identity["process_id"], aid, f"{role} process id", 1)
        for key in (
            "process_start_token", "executable_sha256", "control_channel_id",
            "nonce_commitment_sha256",
        ):
            _sha(identity[key], aid, f"{role} {key}")
        _path(
            identity["executable_path"], _expected_executable(role, fixture_mode),
            aid, f"{role} executable path",
        )
        for key, observed in uniqueness.items():
            if identity[key] in observed:
                _fail(aid, f"cross-role worker identity alias: {key}")
            observed.add(identity[key])
        _sha(command_hashes[role], aid, f"{role} release command hash")
        _sha(ack_hashes[role], aid, f"{role} release ACK hash")
        _sha(completion_hashes[role], aid, f"{role} worker completion hash")
    if len(set(provenance)) != len(provenance):
        _fail(aid, "provenance role/stage alias")
    launch = _role_map(row["launch_epoch_by_role"], aid, "launch epochs")
    completion = _role_map(row["completion_epoch_by_role"], aid, "completion epochs")
    walls = _role_map(row["wall_seconds_by_role"], aid, "wall seconds")
    peak_rss = _role_map(row["peak_rss_bytes_by_role"], aid, "peak RSS")
    peak_mapped = _role_map(row["peak_mapped_bytes_by_role"], aid, "peak mapped")
    samples = _role_map(row["runtime_samples_by_role"], aid, "runtime samples")
    exits = _role_map(row["exit_code_by_role"], aid, "exit codes")
    paths = _role_map(row["output_path_by_role"], aid, "output paths")
    outputs = _role_map(row["output_sha256_by_role"], aid, "output hashes")
    for role in ROLES:
        started = _integer(launch[role], aid, f"{role} launch", 1)
        ended = _integer(completion[role], aid, f"{role} completion", 1)
        wall = _float(walls[role], aid, f"{role} wall")
        rss = _integer(peak_rss[role], aid, f"{role} peak RSS", 1)
        mapped = _integer(peak_mapped[role], aid, f"{role} peak mapped", 1)
        if ended <= started or wall != float(ended - started) or wall > WALL_LIMIT:
            _fail(aid, f"{role} wall reconstruction mismatch")
        mapped_limit = TARGET_MAPPED_LIMIT if role == "target_v012" else HOSTILE_MAPPED_LIMIT
        if rss > RSS_LIMIT or mapped != mapped_limit:
            _fail(aid, f"{role} resource bound exceeded")
        _validate_samples(
            samples[role], started, ended, rss, aid, role, identities[role],
        )
        if _integer(exits[role], aid, f"{role} exit code") != 0:
            _fail(aid, f"{role} exit status is not zero")
        _path(paths[role], _expected_path(role, "history", fixture_mode), aid, f"{role} output")
        _sha(outputs[role], aid, f"{role} output hash")
    if abs(launch[ROLES[0]] - launch[ROLES[1]]) > 60:
        _fail(aid, "dual launch skew exceeded")
    if paths[ROLES[0]] == paths[ROLES[1]] or outputs[ROLES[0]] == outputs[ROLES[1]]:
        _fail(aid, "cross-role output alias")
    disk = row["free_disk_bytes_samples"]
    if type(disk) is not list or len(disk) < 2:
        _fail(aid, "disk sample census mismatch")
    disk_epochs: list[int] = []
    devices: set[int] = set()
    for sample in disk:
        entry = _keys(sample, {"captured_epoch", "workspace_filesystem_device", "free_bytes"}, aid, "disk sample")
        disk_epochs.append(_integer(entry["captured_epoch"], aid, "disk epoch", 1))
        devices.add(_integer(entry["workspace_filesystem_device"], aid, "disk device", 1))
        if _integer(entry["free_bytes"], aid, "free disk", 1) < DISK_MINIMUM:
            _fail(aid, "free disk below threshold")
    if (
        disk_epochs != sorted(set(disk_epochs))
        or disk_epochs[0] > min(launch.values())
        or disk_epochs[-1] < max(completion.values())
        or any(b - a > 60 for a, b in zip(disk_epochs, disk_epochs[1:]))
        or len(devices) != 1
    ):
        _fail(aid, "disk sample order/cadence/device mismatch")
    if row["claim_boundary"] != "POSTRUN_RUNTIME_EVIDENCE_ONLY__NO_FINAL_L12_ADJUDICATION":
        _fail(aid, "claim boundary mismatch")
    return row


ROW_KEYS: Final[set[str]] = {
    "W_n", "actual_norm_error", "actual_solver",
    "admission_bandwidth_residual", "admission_total_content_residual",
    "allow_probability", "bandwidth_after", "blocked_null_state_error",
    "blocked_probability", "connector_delta_l1", "connector_delta_signed",
    "cursor_vertex", "event", "expected_W_from_allow", "lineage_sealed_after",
    "null_norm_error", "null_solver", "q_genesis_after", "q_genesis_before",
    "q_retained_after_admission", "q_retained_after_transport",
    "q_retained_before", "reverse_support_probability", "sector_weights",
    "target_owner_residual", "terminal_children_streamed",
    "transport_genesis_drift", "transport_node_residual_l1",
    "transport_node_residual_linf", "transport_number_drift",
}
SOLVER_KEYS: Final[set[str]] = {
    "batches", "converged", "low_memory_batches", "maximum_exp_difference",
    "maximum_krylov_steps", "maximum_live_bytes", "maximum_residual_indicator",
    "maximum_subdivisions", "quadrature_nodes",
}
HOSTILE_ROW_KEYS: Final[set[str]] = {
    "event", "input_prefix", "input_prefix_dimension",
    "logical_output_prefix_dimension", "terminal_children_streamed",
    "allow_probability", "blocked_probability", "reverse_support_probability",
    "blocked_null_state_error", "W_n", "q_retained_after_transport",
    "q_genesis_after", "sector_weights", "connector_delta_l1",
    "connector_delta_signed", "admission_total_content_residual",
    "admission_bandwidth_residual", "target_owner_residual",
    "transport_node_residual_l1", "transport_node_residual_linf",
    "null_transport_node_residual_l1", "transport_number_drift",
    "null_transport_number_drift", "actual_norm_error", "null_norm_error",
    "actual_solver", "null_solver",
}
HOSTILE_SOLVER_BASE_KEYS: Final[set[str]] = {
    "converged", "batches", "maximum_degree",
    "maximum_endpoint_difference", "maximum_tail_indicator_32", "algorithm",
    "quadrature_group_max", "allocation_vector_slots",
    "maximum_allocation_estimate_bytes", "allocation_limit_bytes",
    "quadrature_nodes", "q_sharded",
}
HOSTILE_SOLVER_TERMINAL_KEYS: Final[set[str]] = (
    HOSTILE_SOLVER_BASE_KEYS | {
        "terminal_children_streamed", "terminal_child0_entries",
        "terminal_child1_nonzero_admission_entries",
        "full_terminal_array_allocated",
    }
)
HOSTILE_COMPARISON_KEYS: Final[set[str]] = {
    "resolved", "classification", "epsilon",
    "maximum_admission_accounting_residual",
    "maximum_node_continuity_residual_l1", "maximum_norm_error",
    "maximum_number_drift", "rough_sharp", "sector",
    "admission_acceptance", "routed_acceptance", "connector_ratio",
}
HOSTILE_RESOURCE_KEYS: Final[set[str]] = {
    "peak_logical_state_plus_cache_bytes", "scratch_limit_bytes",
    "maximum_numerical_allocation_estimate_bytes",
    "numerical_workspace_limit_bytes",
    "authentication_peak_certificate_bytes", "peak_rss_bytes",
    "rss_limit_bytes", "wall_seconds_including_authentication",
    "wall_limit_seconds", "passed",
}
COMPARISON_KEYS: Final[set[str]] = {
    "admission_acceptance", "classification", "coarse_fine", "connector_ratio",
    "epsilon", "resolved", "routed_acceptance", "sector",
}
RESOURCE_KEYS: Final[set[str]] = {
    "peak_live_state_bytes", "cache_payload_bytes", "combined_with_reserve_bytes",
    "scratch_limit_bytes", "maximum_numerical_workset_bytes",
    "numerical_workset_limit_bytes", "terminal_cache_peak_bytes",
    "authentication_cache_peak_bytes", "maximum_cache_window_bytes",
    "mapped_cache_limit_bytes", "peak_rss_bytes", "rss_limit_bytes",
    "wall_seconds", "wall_limit_seconds", "passed",
}
TARGET_HISTORY_KEYS: Final[set[str]] = {
    "schema", "L", "events", "dimension", "preterminal_dimension", "edges",
    "representation", "lineage_authority", "coarse_method", "fine_method",
    "rows", "comparison", "terminal_shards", "cache_manifest_sha256",
    "dual_obstruction_gate_sha256", "physical_execution_gate_sha256",
    "execution_authorization_sha256", "promotion_audit_sha256",
    "cached_control_l4_l8_gate_sha256", "cached_l10_gate_sha256",
    "cached_control_l4_l8_gate_audit_sha256",
    "l10_execution_authorization_gate_sha256", "cached_l10_gate_audit_sha256",
    "target_hostile_l10_cross_gate_sha256",
    "shared_aggregate_schedule_gate_sha256",
    "shared_aggregate_schedule_gate_audit_sha256",
    "target_l12_execution_gate_sha256", "hostile_l12_execution_gate_sha256",
    "dual_l12_launch_handshake_sha256", "dual_l12_worker_release_sha256",
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
}
HOSTILE_HISTORY_KEYS: Final[set[str]] = {
    "schema", "L", "events", "dimension", "preterminal_dimension", "edges",
    "representation", "lineage_authority", "coarse_method", "fine_method",
    "rows", "comparison", "terminal_shards", "cache_manifest_sha256",
    "cache_build_authorization_gate_sha256",
    "l10_execution_authorization_gate_sha256", "postbuild_payload_audit_sha256",
    "target_hostile_l10_cross_gate_sha256",
    "shared_aggregate_schedule_gate_sha256",
    "shared_aggregate_schedule_gate_audit_sha256",
    "hostile_l12_execution_gate_sha256", "dual_l12_launch_handshake_sha256",
    "dual_l12_worker_release_sha256", "resource", "consumer_sha256",
    "builder_sha256", "method_sha256", "preflight_sha256", "freeze_sha256",
    "preflight_result_sha256", "independent_hostile_audit_sha256",
    "claim_boundary",
}
TARGET_HASH_KEYS: Final[set[str]] = {
    key for key in TARGET_HISTORY_KEYS if key.endswith("_sha256")
}
HOSTILE_HASH_KEYS: Final[set[str]] = {
    key for key in HOSTILE_HISTORY_KEYS if key.endswith("_sha256")
}


def _solver(value: object, aid: str, label: str, *, event: int, null: bool) -> None:
    row = _keys(value, SOLVER_KEYS, aid, label)
    if _boolean(row["converged"], aid, f"{label} converged") is not True:
        _fail(aid, f"{label} did not converge")
    batches = _integer(row["batches"], aid, f"{label} batches", 1)
    steps = _integer(row["maximum_krylov_steps"], aid, f"{label} Krylov steps")
    live = _integer(row["maximum_live_bytes"], aid, f"{label} live bytes", 1)
    subdivisions = _integer(row["maximum_subdivisions"], aid, f"{label} subdivisions", 1)
    nodes = _integer(row["quadrature_nodes"], aid, f"{label} quadrature nodes", 1)
    low_memory = _integer(row["low_memory_batches"], aid, f"{label} low-memory batches")
    zero_required = null and event == 1
    if (zero_required and steps != 0) or (not zero_required and steps == 0):
        _fail(aid, f"{label} zero-step justification mismatch")
    for key in ("maximum_exp_difference", "maximum_residual_indicator"):
        _float(row[key], aid, f"{label} {key}")
    if batches < 1 or low_memory > batches or live > 2_000_000_000 or subdivisions < 1 or nodes != 24:
        _fail(aid, f"{label} solver resource/schema mismatch")


def _hostile_solver(
    value: object, aid: str, label: str, *, event: int, actual: bool,
) -> None:
    terminal_actual = event == 12 and actual
    expected = (
        HOSTILE_SOLVER_TERMINAL_KEYS
        if terminal_actual else HOSTILE_SOLVER_BASE_KEYS
    )
    row = _keys(value, expected, aid, label)
    if _boolean(row["converged"], aid, f"{label} converged") is not True:
        _fail(aid, f"{label} did not converge")
    if _integer(row["batches"], aid, f"{label} batches", 1) < 1:
        _fail(aid, f"{label} batch census mismatch")
    if _integer(row["maximum_degree"], aid, f"{label} degree") > 96:
        _fail(aid, f"{label} degree cap exceeded")
    for key in ("maximum_endpoint_difference", "maximum_tail_indicator_32"):
        if _float(row[key], aid, f"{label} {key}") > 8.0e-11:
            _fail(aid, f"{label} convergence tolerance exceeded")
    if (
        row["algorithm"] != "RECURRENCE_REPLAY_GL_GROUPS"
        or _integer(row["quadrature_group_max"], aid, f"{label} quadrature group") != 12
        or _integer(row["allocation_vector_slots"], aid, f"{label} vector slots") != 20
        or _integer(row["allocation_limit_bytes"], aid, f"{label} allocation limit")
        != 1_400_000_000
        or _integer(
            row["maximum_allocation_estimate_bytes"], aid,
            f"{label} allocation estimate",
        ) > 1_400_000_000
        or _integer(row["quadrature_nodes"], aid, f"{label} quadrature nodes") != 28
        or _boolean(row["q_sharded"], aid, f"{label} q-sharded") is not True
    ):
        _fail(aid, f"{label} native Chebyshev method mismatch")
    if terminal_actual and (
        _boolean(
            row["terminal_children_streamed"], aid,
            f"{label} terminal children streamed",
        ) is not True
        or _integer(
            row["terminal_child0_entries"], aid,
            f"{label} terminal child-zero entries",
        ) != math.comb(35, 11)
        or _integer(
            row["terminal_child1_nonzero_admission_entries"], aid,
            f"{label} terminal child-one entries",
        ) != math.comb(34, 11)
        or _boolean(
            row["full_terminal_array_allocated"], aid,
            f"{label} full terminal allocation",
        ) is not False
    ):
        _fail(aid, f"{label} terminal streaming certificate mismatch")


HOSTILE_COARSE_METHOD: Final[dict[str, object]] = {
    "label": "rough", "checkpoints": [16, 24, 32, 48, 64, 80],
    "quadrature_nodes": 18, "tolerance": 3.0e-9,
}
HOSTILE_FINE_METHOD: Final[dict[str, object]] = {
    "label": "sharp", "checkpoints": [24, 32, 48, 64, 80, 96],
    "quadrature_nodes": 28, "tolerance": 8.0e-11,
}


def _minimal_sector_interval(weights: list[float]) -> tuple[int, int, float]:
    candidates: list[tuple[int, float, int, int]] = []
    for lower in range(len(weights)):
        mass = 0.0
        for upper in range(lower, len(weights)):
            mass += weights[upper]
            if mass + 1.0e-15 >= 0.99:
                candidates.append((upper - lower, -mass, lower, upper))
                break
    if not candidates:
        raise Refusal("A25_HOSTILE_L12_HISTORY: no 99-percent sector interval")
    _width, negative_mass, lower, upper = min(candidates)
    return lower, upper, -negative_mass


def _validate_hostile_history(
    record: object, fixture_mode: bool,
) -> dict[str, object]:
    aid = "A25_HOSTILE_L12_HISTORY"
    parsed = _strict_json(record, aid)
    row = _keys(parsed, HOSTILE_HISTORY_KEYS, aid, "hostile history")
    if (
        row["schema"] != "HOSTILE_CACHED_PREFIX_HISTORY_V004R4"
        or _integer(row["L"], aid, "L", 1) != 12
        or _integer(row["events"], aid, "events", 1) != 12
        or _integer(row["dimension"], aid, "dimension", 1) != math.comb(36, 12)
        or _integer(
            row["preterminal_dimension"], aid, "preterminal dimension", 1,
        ) != math.comb(35, 11)
        or _integer(row["edges"], aid, "edge census", 1) != 36
        or row["representation"]
        != "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__AUTHENTICATED_HOSTILE_INDEX_CACHE"
        or row["lineage_authority"]
        != "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING"
        or row["coarse_method"] != HOSTILE_COARSE_METHOD
        or row["fine_method"] != HOSTILE_FINE_METHOD
    ):
        _fail(aid, "hostile history identity/method projection mismatch")
    rows = row["rows"]
    if type(rows) is not list or len(rows) != 12:
        _fail(aid, "hostile history row census mismatch")
    for index, value in enumerate(rows):
        event = index + 1
        event_row = _keys(value, HOSTILE_ROW_KEYS, aid, f"hostile event {event}")
        if (
            _integer(event_row["event"], aid, "event", 1) != event
            or _integer(event_row["input_prefix"], aid, "input prefix") != index
            or _integer(
                event_row["input_prefix_dimension"], aid,
                "input prefix dimension", 1,
            ) != math.comb(24 + index, index)
            or _integer(
                event_row["logical_output_prefix_dimension"], aid,
                "logical output dimension", 1,
            ) != math.comb(25 + index, index + 1)
            or _boolean(
                event_row["terminal_children_streamed"], aid,
                "terminal children streamed",
            ) is not (event == 12)
        ):
            _fail(aid, f"hostile event {event} discrete identity mismatch")
        weights = event_row["sector_weights"]
        if (
            type(weights) is not list or len(weights) != 13
            or any(type(item) is not float or not math.isfinite(item) for item in weights)
        ):
            _fail(aid, f"hostile event {event} sector-weight mismatch")
        for key in HOSTILE_ROW_KEYS - {
            "event", "input_prefix", "input_prefix_dimension",
            "logical_output_prefix_dimension", "terminal_children_streamed",
            "sector_weights", "actual_solver", "null_solver",
        }:
            if type(event_row[key]) is not float or not math.isfinite(event_row[key]):
                _fail(aid, f"hostile event {event} {key} finite-float mismatch")
        _hostile_solver(
            event_row["actual_solver"], aid, f"hostile event {event} actual",
            event=event, actual=True,
        )
        _hostile_solver(
            event_row["null_solver"], aid, f"hostile event {event} null",
            event=event, actual=False,
        )

    comparison = _keys(
        row["comparison"], HOSTILE_COMPARISON_KEYS, aid, "hostile comparison",
    )
    if (
        _boolean(comparison["resolved"], aid, "hostile comparison resolved")
        is not True
        or comparison["classification"] != "RESOLVED_PREFIX_HISTORY_CONTROL"
    ):
        _fail(aid, "hostile comparison identity mismatch")
    rough_sharp = _keys(
        comparison["rough_sharp"],
        {"maximum_disagreement", "observable_linf", "sector_weight_linf"},
        aid, "hostile rough/sharp",
    )
    for key in rough_sharp:
        _float(rough_sharp[key], aid, f"hostile rough/sharp {key}")
    disagreement = max(
        rough_sharp["observable_linf"], rough_sharp["sector_weight_linf"],
    )
    if (
        rough_sharp["maximum_disagreement"] != disagreement
        or _float(comparison["epsilon"], aid, "hostile epsilon")
        != max(1.0e-11, 50.0 * disagreement)
    ):
        _fail(aid, "hostile rough/sharp reconstruction mismatch")
    summary_sources = {
        "maximum_admission_accounting_residual": max(
            abs(event_row[key]) for event_row in rows
            for key in (
                "admission_total_content_residual",
                "admission_bandwidth_residual", "target_owner_residual",
            )
        ),
        "maximum_node_continuity_residual_l1": max(
            abs(event_row[key]) for event_row in rows
            for key in (
                "transport_node_residual_l1",
                "null_transport_node_residual_l1",
            )
        ),
        "maximum_number_drift": max(
            abs(event_row[key]) for event_row in rows
            for key in ("transport_number_drift", "null_transport_number_drift")
        ),
        "maximum_norm_error": max(
            abs(event_row[key]) for event_row in rows
            for key in ("actual_norm_error", "null_norm_error")
        ),
    }
    for key, expected in summary_sources.items():
        if _float(comparison[key], aid, f"hostile {key}") != expected:
            _fail(aid, f"hostile comparison reconstruction mismatch: {key}")
    epsilon = comparison["epsilon"]
    if (
        summary_sources["maximum_admission_accounting_residual"] > 1.0e-10
        or summary_sources["maximum_node_continuity_residual_l1"]
        > max(1.0e-9, 100.0 * epsilon)
        or summary_sources["maximum_number_drift"] > 1.0e-10
        or summary_sources["maximum_norm_error"] > 1.0e-10
        or max(abs(event_row["reverse_support_probability"]) for event_row in rows)
        > 1.0e-11
        or max(abs(event_row["blocked_null_state_error"]) for event_row in rows)
        > 1.0e-11
        or min(event_row["W_n"] for event_row in rows) < -epsilon
        or max(event_row["blocked_probability"] for event_row in rows) <= 1.0e-6
    ):
        _fail(aid, "hostile resolved-comparison physical bounds failed")
    for key in ("admission_acceptance", "connector_ratio", "routed_acceptance"):
        values = comparison[key]
        if (
            type(values) is not list or len(values) != 12
            or any(type(item) is not float or not math.isfinite(item) for item in values)
        ):
            _fail(aid, f"hostile comparison {key} census/type mismatch")
    expected_acceptance = [2.0 * event_row["W_n"] for event_row in rows]
    first_connector = rows[0]["connector_delta_l1"]
    if first_connector <= 0.0:
        _fail(aid, "hostile connector normalization denominator invalid")
    expected_connector = [
        event_row["connector_delta_l1"] / first_connector for event_row in rows
    ]
    expected_routed = [
        min(left, right)
        for left, right in zip(expected_acceptance, expected_connector)
    ]
    for key, expected in (
        ("admission_acceptance", expected_acceptance),
        ("connector_ratio", expected_connector),
        ("routed_acceptance", expected_routed),
    ):
        if any(abs(left - right) > 1.0e-15 for left, right in zip(comparison[key], expected)):
            _fail(aid, f"hostile comparison {key} reconstruction mismatch")
    sector = _keys(
        comparison["sector"],
        {"density_interval", "discarded_mass", "enclosed_mass", "late_events", "q_lower", "q_upper"},
        aid, "hostile sector",
    )
    late_events = list(range(7, 13))
    mean_weights = np.mean(
        np.asarray(
            [rows[event - 1]["sector_weights"] for event in late_events],
            dtype=np.float64,
        ),
        axis=0,
    ).tolist()
    lower, upper, mass = _minimal_sector_interval(mean_weights)
    expected_sector = {
        "late_events": late_events, "q_lower": lower, "q_upper": upper,
        "enclosed_mass": mass, "discarded_mass": 1.0 - mass,
        "density_interval": [
            max(0.0, (lower - 0.5) / 24.0),
            min(1.0, (upper + 0.5) / 24.0),
        ],
    }
    if sector != expected_sector or any(
        type(sector[key]) is not type(expected)
        for key, expected in expected_sector.items()
    ):
        _fail(aid, "hostile sector reconstruction mismatch")

    resource = _keys(
        row["resource"], HOSTILE_RESOURCE_KEYS, aid, "hostile resource",
    )
    exact_resource = {
        "peak_logical_state_plus_cache_bytes": 9_599_886_552,
        "scratch_limit_bytes": 21_474_836_480,
        "numerical_workspace_limit_bytes": 1_400_000_000,
        "authentication_peak_certificate_bytes": 252_944_080,
        "rss_limit_bytes": RSS_LIMIT,
        "wall_limit_seconds": WALL_LIMIT,
        "passed": True,
    }
    if any(
        type(resource[key]) is not type(expected) or resource[key] != expected
        for key, expected in exact_resource.items()
    ):
        _fail(aid, "hostile resource exact fixed field mismatch")
    allocation = max(
        event_row[solver]["maximum_allocation_estimate_bytes"]
        for event_row in rows for solver in ("actual_solver", "null_solver")
    )
    if (
        _integer(
            resource["maximum_numerical_allocation_estimate_bytes"], aid,
            "hostile maximum allocation",
        ) != allocation
        or allocation > resource["numerical_workspace_limit_bytes"]
        or not 0 < _integer(resource["peak_rss_bytes"], aid, "hostile peak RSS")
        <= RSS_LIMIT
        or not 0.0 < _float(
            resource["wall_seconds_including_authentication"], aid,
            "hostile wall seconds",
        ) <= WALL_LIMIT
        or resource["peak_logical_state_plus_cache_bytes"]
        + 1_048_576 != 9_600_935_128
        or resource["peak_logical_state_plus_cache_bytes"]
        >= resource["scratch_limit_bytes"]
    ):
        _fail(aid, "hostile resource reconstruction mismatch")

    shards = row["terminal_shards"]
    if type(shards) is not list or len(shards) != 12:
        _fail(aid, "hostile terminal shard census mismatch")
    shard_hashes: set[str] = set()
    for q, value in enumerate(shards):
        shard = _keys(
            value, {"q", "path", "shape", "bytes", "sha256"}, aid,
            f"hostile terminal q={q}",
        )
        shape = [math.comb(11, q), math.comb(24, q)]
        if (
            _integer(shard["q"], aid, "hostile terminal q") != q
            or type(shard["shape"]) is not list or shard["shape"] != shape
            or any(type(item) is not int for item in shard["shape"])
            or _integer(shard["bytes"], aid, "hostile terminal bytes", 1)
            != math.prod(shape) * 16
        ):
            _fail(aid, "hostile terminal shape/byte reconstruction mismatch")
        _path(
            shard["path"], _expected_path("hostile_v004r4", "terminal", fixture_mode, q),
            aid, "hostile terminal path",
        )
        shard_hashes.add(_sha(shard["sha256"], aid, "hostile terminal hash"))
    if len(shard_hashes) != 12:
        _fail(aid, "hostile terminal shard digest alias")
    history_hashes = [_sha(row[key], aid, key) for key in HOSTILE_HASH_KEYS]
    if len(set(history_hashes)) != len(history_hashes):
        _fail(aid, "hostile provenance digest alias")
    if row["claim_boundary"] != "FINITE_CACHED_HOSTILE_V004R4_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY":
        _fail(aid, "hostile claim boundary mismatch")
    return row


def _finite_tree(value: object, aid: str, label: str) -> None:
    if type(value) is bool or value is None or type(value) is str:
        return
    if type(value) is int:
        return
    if type(value) is float:
        if not math.isfinite(value):
            _fail(aid, f"{label} contains nonfinite float")
        return
    if type(value) is list:
        for index, item in enumerate(value):
            _finite_tree(item, aid, f"{label}[{index}]")
        return
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            _fail(aid, f"{label} has non-string key")
        for key, item in value.items():
            _finite_tree(item, aid, f"{label}.{key}")
        return
    _fail(aid, f"{label} contains unsupported type")


def _validate_history(record: object, role: str, fixture_mode: bool) -> dict[str, object]:
    if role == "hostile_v004r4":
        return _validate_hostile_history(record, fixture_mode)
    aid = "A24_TARGET_L12_HISTORY" if role == "target_v012" else "A25_HOSTILE_L12_HISTORY"
    record = _strict_json(record, aid)
    row = _keys(record, TARGET_HISTORY_KEYS if role == "target_v012" else HOSTILE_HISTORY_KEYS, aid, "history")
    expected_claim = "FINITE_CACHED_TARGET_HISTORY_ONLY__NO_SPECTRUM_CONTINUUM_OR_GRAVITY" if role == "target_v012" else "FINITE_CACHED_HOSTILE_V004R4_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY"
    if row["schema"] != _history_schema(role):
        _fail(aid, "history identity mismatch")
    if _integer(row["L"], aid, "L", 1) != 12 or _integer(row["events"], aid, "events", 1) != 12:
        _fail(aid, "L/event census mismatch")
    if _integer(row["dimension"], aid, "dimension", 1) != math.comb(36, 12) or _integer(row["preterminal_dimension"], aid, "preterminal dimension", 1) != math.comb(35, 11):
        _fail(aid, "history dimension reconstruction mismatch")
    expected_representation = "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__AUTHENTICATED_INDEX_CACHE" if role == "target_v012" else "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__AUTHENTICATED_HOSTILE_INDEX_CACHE"
    if row["representation"] != expected_representation or row["lineage_authority"] != "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING" or _integer(row["edges"], aid, "edge census", 1) != 36:
        _fail(aid, "history representation/basis mismatch")
    _finite_tree(row["coarse_method"], aid, "coarse method")
    _finite_tree(row["fine_method"], aid, "fine method")
    rows = row["rows"]
    if type(rows) is not list or len(rows) != 12:
        _fail(aid, "history row census mismatch")
    for index, item in enumerate(rows):
        event = index + 1
        event_row = _keys(item, ROW_KEYS, aid, f"event {event}")
        if _integer(event_row["event"], aid, "event", 1) != event or _integer(event_row["cursor_vertex"], aid, "cursor vertex") != index:
            _fail(aid, f"event {event} order/cursor mismatch")
        if type(event_row["sector_weights"]) is not list or len(event_row["sector_weights"]) != 13 or any(type(value) is not float or not math.isfinite(value) for value in event_row["sector_weights"]):
            _fail(aid, f"event {event} sector-weight census/type mismatch")
        if type(event_row["terminal_children_streamed"]) is not bool:
            _fail(aid, f"event {event} terminal flag type mismatch")
        for key, value in event_row.items():
            if key in {"event", "cursor_vertex", "sector_weights", "terminal_children_streamed", "actual_solver", "null_solver"}:
                continue
            if type(value) is not float or not math.isfinite(value):
                _fail(aid, f"event {event} {key} exact finite-float mismatch")
        _solver(event_row["actual_solver"], aid, f"event {event} actual solver", event=event, null=False)
        _solver(event_row["null_solver"], aid, f"event {event} null solver", event=event, null=True)
    comparison = _keys(row["comparison"], COMPARISON_KEYS, aid, "comparison")
    for key in ("admission_acceptance", "connector_ratio", "routed_acceptance"):
        if type(comparison[key]) is not list or len(comparison[key]) != 12 or any(type(value) is not float or not math.isfinite(value) for value in comparison[key]):
            _fail(aid, f"comparison {key} census/type mismatch")
    coarse_fine = _keys(comparison["coarse_fine"], {"maximum_disagreement", "observable_linf", "sector_weight_linf"}, aid, "coarse/fine comparison")
    if any(type(value) is not float or not math.isfinite(value) or value > TOLERANCE for value in coarse_fine.values()):
        _fail(aid, "coarse/fine comparison tolerance mismatch")
    sector = _keys(comparison["sector"], {"density_interval", "discarded_mass", "enclosed_mass", "late_events", "q_lower", "q_upper"}, aid, "sector comparison")
    _finite_tree(sector, aid, "sector comparison")
    if _boolean(comparison["resolved"], aid, "comparison resolved") is not True or comparison["classification"] != "RESOLVED_RELATIONAL_HISTORY_L" or _float(comparison["epsilon"], aid, "comparison epsilon") != 1.0e-11:
        _fail(aid, "history comparison mismatch")
    resource = _keys(row["resource"], RESOURCE_KEYS, aid, "resource")
    expected_cache = 826_238_292 if role == "target_v012" else 826_221_912
    expected_combined = 9_600_954_452 if role == "target_v012" else 9_600_935_128
    exact_resources = {
        "peak_live_state_bytes": 8_773_667_584,
        "cache_payload_bytes": expected_cache,
        "combined_with_reserve_bytes": expected_combined,
        "scratch_limit_bytes": 21_474_836_480,
        "numerical_workset_limit_bytes": 1_000_000_000,
        "terminal_cache_peak_bytes": 234_782_536,
        "authentication_cache_peak_bytes": 252_944_080,
        "maximum_cache_window_bytes": 252_944_080,
        "mapped_cache_limit_bytes": 536_870_912,
        "rss_limit_bytes": RSS_LIMIT,
        "wall_limit_seconds": WALL_LIMIT,
    }
    for key, expected in exact_resources.items():
        if type(resource[key]) is not type(expected) or resource[key] != expected:
            _fail(aid, f"resource exact fixed field mismatch: {key}")
    if not 0 < _integer(resource["peak_rss_bytes"], aid, "peak RSS") <= _integer(resource["rss_limit_bytes"], aid, "RSS limit", 1) == RSS_LIMIT:
        _fail(aid, "RSS reconstruction mismatch")
    if not 0.0 < _float(resource["wall_seconds"], aid, "wall seconds") <= _float(resource["wall_limit_seconds"], aid, "wall limit") == WALL_LIMIT or _boolean(resource["passed"], aid, "resource passed") is not True:
        _fail(aid, "resource/wall reconstruction mismatch")
    for key in RESOURCE_KEYS - {"wall_seconds", "wall_limit_seconds", "passed", "peak_rss_bytes", "rss_limit_bytes"}:
        _integer(resource[key], aid, f"resource {key}", 1)
    reconstructed_workset = max(
        solver["maximum_live_bytes"]
        for history_row in rows
        for solver in (history_row["actual_solver"], history_row["null_solver"])
    )
    if resource["combined_with_reserve_bytes"] != resource["peak_live_state_bytes"] + resource["cache_payload_bytes"] + 1_048_576 or resource["combined_with_reserve_bytes"] >= resource["scratch_limit_bytes"] or resource["maximum_numerical_workset_bytes"] != reconstructed_workset or resource["maximum_numerical_workset_bytes"] > resource["numerical_workset_limit_bytes"] or resource["maximum_cache_window_bytes"] > resource["mapped_cache_limit_bytes"]:
        _fail(aid, "resource arithmetic/bound mismatch")
    shards = row["terminal_shards"]
    if type(shards) is not list or len(shards) != 12:
        _fail(aid, "terminal shard census mismatch")
    shard_hashes: set[str] = set()
    for q, item in enumerate(shards):
        shard = _keys(item, {"q", "path", "shape", "bytes", "sha256"}, aid, f"terminal q={q}")
        shape = [math.comb(11, q), math.comb(24, q)]
        if _integer(shard["q"], aid, "terminal q") != q or type(shard["shape"]) is not list or shard["shape"] != shape or any(type(v) is not int for v in shard["shape"]):
            _fail(aid, "terminal shard shape/order mismatch")
        # The native record binds physical NPY bytes.  The V012 writer uses a
        # canonical v1.0 header, which is exactly 128 bytes for every L12 shape.
        if _integer(shard["bytes"], aid, "terminal bytes", 1) != math.prod(shape) * 16 + 128:
            _fail(aid, "terminal shard byte reconstruction mismatch")
        _path(shard["path"], _expected_path(role, "terminal", fixture_mode, q), aid, "terminal shard")
        shard_hashes.add(_sha(shard["sha256"], aid, "terminal shard hash"))
    if len(shard_hashes) != 12:
        _fail(aid, "terminal shard digest alias")
    hash_keys = TARGET_HASH_KEYS if role == "target_v012" else HOSTILE_HASH_KEYS
    for key in hash_keys:
        _sha(row[key], aid, key)
    if role == "target_v012" and (
        row["execution_authorization_sha256"] != row["target_l12_execution_gate_sha256"]
        or row["promotion_audit_sha256"] != row["shared_aggregate_schedule_gate_audit_sha256"]
    ):
        _fail(aid, "target L12 authorization/audit binding mismatch")
    if row["claim_boundary"] != expected_claim:
        _fail(aid, "claim boundary mismatch")
    return row


def validate_target_l12_history(record: object, *, fixture_mode: bool = False) -> dict[str, object]:
    return _validate_history(record, "target_v012", fixture_mode)


def validate_hostile_l12_history(record: object, *, fixture_mode: bool = False) -> dict[str, object]:
    return _validate_history(record, "hostile_v004r4", fixture_mode)


def _rank_in_reversed_basis(width: int, q: int, target_mask: tuple[int, ...]) -> int:
    positions = tuple(width - 1 - value for value in reversed(target_mask))
    rank = 0
    previous = -1
    for index, position in enumerate(positions):
        choose = q - index
        rank += math.comb(width - previous - 1, choose)
        rank -= math.comb(width - position, choose)
        previous = position
    return rank


@lru_cache(maxsize=None)
def _basis_permutation(width: int, q: int) -> np.ndarray:
    if type(width) is not int or type(q) is not int or width < 0 or not 0 <= q <= width:
        raise Refusal("basis permutation parameters invalid")
    count = math.comb(width, q)
    values = np.fromiter(
        (
            _rank_in_reversed_basis(width, q, target_mask)
            for target_mask in itertools.combinations(range(width), q)
        ),
        dtype="<u8", count=count,
    )
    if len(values) != count or len(np.unique(values)) != count or (count and (int(values.min()) != 0 or int(values.max()) != count - 1)):
        raise Refusal("basis permutation is not bijective")
    values.flags.writeable = False
    return values


@lru_cache(maxsize=None)
def basis_permutation_sha256(width: int, q: int) -> str:
    """Hash target-rank -> reversed-combination-rank as tagged little-endian u64."""
    values = _basis_permutation(width, q)
    count = len(values)
    digest = hashlib.sha256()
    digest.update(b"V001_LE_U64_TARGET_RANK_TO_HOSTILE_RANK\0")
    digest.update(struct.pack("<IIQ", width, q, count))
    digest.update(values.tobytes(order="C"))
    return digest.hexdigest()


def _descriptor_sha256(descriptor: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while block := os.pread(descriptor, 16 * 2**20, offset):
        digest.update(block)
        offset += len(block)
    return digest.hexdigest()


def _complete_identity(
    metadata: os.stat_result,
) -> tuple[int, int, int, int, int, int, int]:
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_nlink,
        metadata.st_mode,
    )


def _descriptor_bytes(descriptor: int, size: int, aid: str, label: str) -> bytes:
    if type(size) is not int or size < 0:
        _fail(aid, f"{label} descriptor size is invalid")
    raw = bytearray()
    offset = 0
    while offset < size:
        block = os.pread(descriptor, min(16 * 2**20, size - offset), offset)
        if not block:
            _fail(aid, f"{label} descriptor read was short")
        raw.extend(block)
        offset += len(block)
    return bytes(raw)


def _require_no_symlink_parents(path_text: str, aid: str, label: str) -> None:
    try:
        relative = Path(path_text).relative_to(ROOT)
        current = ROOT
        root_metadata = os.stat(current, follow_symlinks=False)
        if not stat.S_ISDIR(root_metadata.st_mode) or stat.S_ISLNK(
            root_metadata.st_mode
        ):
            _fail(aid, f"{label} repository root is aliased")
        for part in relative.parts[:-1]:
            current /= part
            metadata = os.stat(current, follow_symlinks=False)
            if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
                _fail(aid, f"{label} parent path is aliased")
    except (OSError, TypeError, ValueError) as error:
        if isinstance(error, Refusal):
            raise
        raise Refusal(f"{aid}: {label} parent path is absent/aliased") from error


def _parent_identity(
    path: Path, descriptor: int, aid: str, label: str,
) -> tuple[int, int]:
    _require_no_symlink_parents(str(path / "placeholder"), aid, label)
    try:
        held = os.fstat(descriptor)
        current = os.stat(path, follow_symlinks=False)
    except (OSError, TypeError, ValueError) as error:
        raise Refusal(f"{aid}: {label} canonical parent changed") from error
    if (
        not stat.S_ISDIR(held.st_mode) or not stat.S_ISDIR(current.st_mode)
        or stat.S_ISLNK(current.st_mode)
        or (held.st_dev, held.st_ino) != (current.st_dev, current.st_ino)
    ):
        _fail(aid, f"{label} canonical parent changed")
    return held.st_dev, held.st_ino


@dataclass
class _StableInput:
    descriptor: int
    parent_descriptor: int
    before: tuple[int, int, int, int, int, int, int]
    parent_before: tuple[int, int]
    digest: str
    label: str
    path: str

    def __del__(self) -> None:
        for name in ("descriptor", "parent_descriptor"):
            descriptor = getattr(self, name, -1)
            if type(descriptor) is not int or descriptor < 0:
                continue
            try:
                os.close(descriptor)
            except OSError:
                pass
            setattr(self, name, -1)

    def verify(self) -> None:
        path = Path(self.path)
        _require_no_symlink_parents(
            self.path, "A26_FINAL_L12_AUDIT", self.label,
        )
        if _parent_identity(
            path.parent, self.parent_descriptor,
            "A26_FINAL_L12_AUDIT", self.label,
        ) != self.parent_before:
            _fail(
                "A26_FINAL_L12_AUDIT",
                f"{self.label} canonical parent changed",
            )
        try:
            descriptor_before = os.fstat(self.descriptor)
            path_before = os.stat(
                path.name, dir_fd=self.parent_descriptor,
                follow_symlinks=False,
            )
            observed_digest = _descriptor_sha256(self.descriptor)
            descriptor_after = os.fstat(self.descriptor)
            path_after = os.stat(
                path.name, dir_fd=self.parent_descriptor,
                follow_symlinks=False,
            )
        except (OSError, TypeError, ValueError) as error:
            raise Refusal(
                f"A26_FINAL_L12_AUDIT: {self.label} canonical path changed"
            ) from error
        if _parent_identity(
            path.parent, self.parent_descriptor,
            "A26_FINAL_L12_AUDIT", self.label,
        ) != self.parent_before:
            _fail(
                "A26_FINAL_L12_AUDIT",
                f"{self.label} canonical parent changed",
            )
        if (
            _complete_identity(descriptor_before) != self.before
            or _complete_identity(path_before) != self.before
            or _complete_identity(descriptor_after) != self.before
            or _complete_identity(path_after) != self.before
            or not stat.S_ISREG(descriptor_before.st_mode)
            or not stat.S_ISREG(path_before.st_mode)
            or descriptor_before.st_mode & 0o222
            or descriptor_before.st_nlink != 1
            or observed_digest != self.digest
        ):
            _fail(
                "A26_FINAL_L12_AUDIT",
                f"{self.label} changed during validation",
            )

    def close(self) -> None:
        first_error: BaseException | None = None
        for name in ("descriptor", "parent_descriptor"):
            descriptor = getattr(self, name)
            if descriptor < 0:
                continue
            try:
                os.close(descriptor)
            except BaseException as error:
                if first_error is None:
                    first_error = error
            setattr(self, name, -1)
        if first_error is not None:
            raise first_error

    def verify_and_close(self) -> None:
        first_error: BaseException | None = None
        try:
            self.verify()
        except BaseException as error:
            first_error = error
        finally:
            try:
                self.close()
            except BaseException as error:
                if first_error is None:
                    first_error = error
        if first_error is not None:
            raise first_error


def _open_retained_file(
    path_text: str, digest: str, aid: str, label: str,
) -> _StableInput:
    _require_no_symlink_parents(path_text, aid, label)
    path = Path(path_text)
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        parent_descriptor = os.open(path.parent, parent_flags)
    except (OSError, TypeError, ValueError) as error:
        raise Refusal(f"{aid}: {label} immutable parent absent") from error
    descriptor = -1
    retained: _StableInput | None = None
    try:
        parent_before = _parent_identity(
            path.parent, parent_descriptor, aid, label,
        )
        flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptor = os.open(path.name, flags, dir_fd=parent_descriptor)
        metadata_before = os.fstat(descriptor)
        path_before = os.stat(
            path.name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
        before = _complete_identity(metadata_before)
        if (
            not stat.S_ISREG(metadata_before.st_mode)
            or metadata_before.st_mode & 0o222
            or metadata_before.st_nlink != 1
            or _complete_identity(path_before) != before
        ):
            _fail(aid, f"{label} is not an owner-once immutable ordinary file")
        observed = _descriptor_sha256(descriptor)
        metadata_after = os.fstat(descriptor)
        path_after = os.stat(
            path.name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
        if (
            observed != digest
            or _complete_identity(metadata_after) != before
            or _complete_identity(path_after) != before
            or _parent_identity(path.parent, parent_descriptor, aid, label)
            != parent_before
        ):
            _fail(aid, f"{label} changed during descriptor authentication")
        retained = _StableInput(
            descriptor, parent_descriptor, before, parent_before,
            observed, label, path_text,
        )
        retained.verify()
        return retained
    except BaseException:
        if retained is not None:
            retained.close()
        else:
            if descriptor >= 0:
                os.close(descriptor)
            os.close(parent_descriptor)
        raise


def _open_immutable_json(path_text: str, digest: str, aid: str, label: str) -> tuple[dict[str, object], _StableInput]:
    retained = _open_retained_file(path_text, digest, aid, label)
    try:
        raw = _descriptor_bytes(
            retained.descriptor, retained.before[2], aid, label,
        )
        if hashlib.sha256(raw).hexdigest() != digest:
            _fail(aid, f"{label} bytes/hash mismatch")
        record = _strict_json(raw, aid)
        if type(record) is not dict:
            _fail(aid, f"{label} is not a JSON object")
        if canonical_json_bytes(record) != raw:
            _fail(aid, f"{label} is not exact canonical JSON")
        retained.verify()
        return record, retained
    except BaseException:
        retained.close()
        raise


def _open_immutable_file(
    path_text: str, digest: str, aid: str, label: str,
) -> _StableInput:
    return _open_retained_file(path_text, digest, aid, label)


def _binding(
    value: object, aid: str, label: str, expected_path: str, fixture_mode: bool,
) -> tuple[dict[str, object], str, _StableInput | None]:
    expected_keys = {"path", "sha256", "record"} if fixture_mode else {"path", "sha256"}
    row = _keys(value, expected_keys, aid, label)
    _path(row["path"], expected_path, aid, f"{label} path")
    digest = _sha(row["sha256"], aid, f"{label} hash")
    if fixture_mode:
        if record_sha256(row["record"]) != digest:
            _fail(aid, f"{label} content hash mismatch")
        return row["record"], digest, None
    record, retained = _open_immutable_json(row["path"], digest, aid, label)
    return record, digest, retained


def _npy_layout(descriptor: int, aid: str, label: str) -> tuple[tuple[int, ...], int, int]:
    try:
        with os.fdopen(os.dup(descriptor), "rb") as stream:
            version = np.lib.format.read_magic(stream)
            if version == (1, 0):
                shape, fortran, dtype = np.lib.format.read_array_header_1_0(stream)
            elif version in ((2, 0), (3, 0)):
                shape, fortran, dtype = np.lib.format.read_array_header_2_0(stream)
            else:
                _fail(aid, f"{label} unsupported NPY version")
            offset = stream.tell()
    except (OSError, EOFError, ValueError) as error:
        raise Refusal(f"{aid}: {label} malformed NPY") from error
    if fortran or np.dtype(dtype) != np.dtype("<c16") or len(shape) != 2 or any(type(value) is not int or value <= 0 for value in shape):
        _fail(aid, f"{label} NPY layout mismatch")
    return tuple(shape), offset, math.prod(shape)


def _open_terminal(
    binding: dict[str, object], aid: str, label: str,
) -> _StableInput:
    retained = _open_retained_file(
        binding["path"], binding["sha256"], aid, label,
    )
    try:
        if retained.before[2] != binding["bytes"]:
            _fail(aid, f"{label} immutable terminal byte census mismatch")
        retained.verify()
        return retained
    except BaseException:
        retained.close()
        raise


def _verify_terminal_input(
    retained: _StableInput, binding: dict[str, object],
    aid: str, label: str, q: int,
) -> None:
    if (
        retained.path != binding["path"]
        or retained.digest != binding["sha256"]
        or retained.before[2] != binding["bytes"]
    ):
        _fail(aid, f"{label} terminal q={q} changed during comparison")
    retained.verify()


def _compare_terminal_files(
    target: dict[str, object], hostile: dict[str, object], q: int,
    *, lineage_width: int = 11, carrier_width: int = 24,
) -> float:
    aid = "A26_FINAL_L12_AUDIT"
    target_input: _StableInput | None = None
    hostile_input: _StableInput | None = None
    try:
        target_input = _open_terminal(target, aid, f"target q={q}")
        hostile_input = _open_terminal(hostile, aid, f"hostile q={q}")
        target_fd = target_input.descriptor
        hostile_fd = hostile_input.descriptor
        target_shape, target_offset, target_count = _npy_layout(target_fd, aid, f"target q={q}")
        expected_shape = tuple(target["shape"])
        hostile_shape = tuple(hostile["shape"])
        hostile_offset = 0
        hostile_count = math.prod(hostile_shape)
        if target_shape != expected_shape or hostile_shape != expected_shape:
            _fail(aid, f"terminal q={q} shape mismatch")
        if (
            target_offset != 128 or hostile_offset != 0
            or target["bytes"] != target_offset + 16 * target_count
            or hostile["bytes"] != hostile_offset + 16 * hostile_count
        ):
            _fail(aid, f"terminal q={q} physical/logical byte mismatch")
        rows, columns = expected_shape
        lineage_permutation = _basis_permutation(lineage_width, q)
        carrier_permutation = _basis_permutation(carrier_width, q)
        if len(lineage_permutation) != rows or len(carrier_permutation) != columns:
            _fail(aid, f"terminal q={q} basis-permutation census mismatch")
        maximum = 0.0
        chunk_columns = max(1, (8 * 2**20) // 16)
        hostile_mapping = mmap.mmap(hostile_fd, 0, access=mmap.ACCESS_READ)
        try:
            hostile_matrix = np.ndarray(
                expected_shape, dtype="<c16", buffer=hostile_mapping,
                offset=hostile_offset, order="C",
            )
            for target_row in range(rows):
                hostile_row = int(lineage_permutation[target_row])
                for start in range(0, columns, chunk_columns):
                    stop = min(columns, start + chunk_columns)
                    count = stop - start
                    target_raw = os.pread(
                        target_fd, 16 * count,
                        target_offset + 16 * (target_row * columns + start),
                    )
                    if len(target_raw) != 16 * count:
                        _fail(aid, f"terminal q={q} truncated")
                    target_values = np.frombuffer(target_raw, dtype="<c16")
                    hostile_values = hostile_matrix[
                        hostile_row, carrier_permutation[start:stop]
                    ]
                    if not np.all(np.isfinite(target_values.real)) or not np.all(np.isfinite(target_values.imag)) or not np.all(np.isfinite(hostile_values.real)) or not np.all(np.isfinite(hostile_values.imag)):
                        _fail(aid, f"terminal q={q} contains nonfinite values")
                    if count:
                        maximum = max(maximum, float(np.max(np.abs(target_values - hostile_values))))
            del hostile_matrix
        finally:
            hostile_mapping.close()
        return maximum
    finally:
        try:
            if target_input is not None:
                _verify_terminal_input(
                    target_input, target, aid, "target", q,
                )
        finally:
            try:
                if hostile_input is not None:
                    _verify_terminal_input(
                        hostile_input, hostile, aid, "hostile", q,
                    )
            finally:
                try:
                    if target_input is not None:
                        target_input.close()
                finally:
                    if hostile_input is not None:
                        hostile_input.close()


def _projection_linf(
    target: object, hostile_projection: object, aid: str, label: str,
) -> float:
    if type(target) in (int, float) and type(target) is not bool:
        if type(hostile_projection) not in (int, float) or type(hostile_projection) is bool:
            _fail(aid, f"{label} numeric type mismatch")
        left = float(target)
        right = float(hostile_projection)
        if not math.isfinite(left) or not math.isfinite(right):
            _fail(aid, f"{label} nonfinite projection")
        return abs(left - right)
    if type(target) is bool or type(target) is str:
        if type(hostile_projection) is not type(target) or hostile_projection != target:
            _fail(aid, f"{label} discrete projection mismatch")
        return 0.0
    if type(target) is list:
        if type(hostile_projection) is not list or len(target) != len(hostile_projection):
            _fail(aid, f"{label} list projection mismatch")
        return max(
            (_projection_linf(left, right, aid, f"{label}[{index}]")
             for index, (left, right) in enumerate(zip(target, hostile_projection))),
            default=0.0,
        )
    if type(target) is dict:
        if type(hostile_projection) is not dict or set(target) != set(hostile_projection):
            _fail(aid, f"{label} object projection mismatch")
        return max(
            (_projection_linf(
                target[key], hostile_projection[key], aid, f"{label}.{key}",
            ) for key in target),
            default=0.0,
        )
    _fail(aid, f"{label} unsupported projection type")


def _history_projection_errors(
    target: dict[str, object], hostile: dict[str, object], aid: str,
) -> tuple[float, float]:
    row_maximum = 0.0
    prior_retained = 0.0
    shared = ROW_KEYS & HOSTILE_ROW_KEYS - {
        "actual_solver", "null_solver",
    }
    derived = {
        "bandwidth_after", "cursor_vertex", "expected_W_from_allow",
        "lineage_sealed_after", "q_genesis_before",
        "q_retained_after_admission", "q_retained_before",
        "transport_genesis_drift",
    }
    if shared | derived != ROW_KEYS - {"actual_solver", "null_solver"}:
        _fail(aid, "internal hostile-to-target row projection census mismatch")
    for index, (target_row, hostile_row) in enumerate(
        zip(target["rows"], hostile["rows"]), start=1,
    ):
        projection = {key: hostile_row[key] for key in shared}
        projection.update({
            "bandwidth_after": hostile_row["q_genesis_after"],
            "cursor_vertex": hostile_row["input_prefix"],
            "expected_W_from_allow": 0.5 * hostile_row["allow_probability"],
            "lineage_sealed_after": 12.0 - hostile_row["q_genesis_after"],
            "q_genesis_before": 12.0 - prior_retained,
            "q_retained_after_admission": prior_retained + hostile_row["W_n"],
            "q_retained_before": prior_retained,
            "transport_genesis_drift": 0.0,
        })
        target_projection = {
            key: value for key, value in target_row.items()
            if key not in {"actual_solver", "null_solver"}
        }
        row_maximum = max(
            row_maximum,
            _projection_linf(
                target_projection, projection, aid,
                f"target/hostile event {index}",
            ),
        )
        prior_retained = hostile_row["q_retained_after_transport"]

    target_comparison = target["comparison"]
    hostile_comparison = hostile["comparison"]
    target_projection = {
        key: target_comparison[key] for key in (
            "admission_acceptance", "connector_ratio", "epsilon", "resolved",
            "routed_acceptance", "sector",
        )
    }
    target_projection["resolution_comparison"] = target_comparison["coarse_fine"]
    hostile_projection = {
        key: hostile_comparison[key] for key in (
            "admission_acceptance", "connector_ratio", "epsilon", "resolved",
            "routed_acceptance", "sector",
        )
    }
    hostile_projection["resolution_comparison"] = hostile_comparison["rough_sharp"]
    comparison_maximum = _projection_linf(
        target_projection, hostile_projection, aid,
        "target/hostile comparison",
    )
    return row_maximum, comparison_maximum


def _keyset(value: str) -> set[str]:
    return set(value.split())


# Independently transcribed from the reviewed record contracts.  A26 consumes
# only these exact envelopes plus the predecessor fields reconstructed below;
# it does not import or call the target production validator.
UPSTREAM_AUTHORITY_SHAPES: Final[
    dict[str, tuple[str | None, set[str], tuple[str, object] | None, str | None]]
] = {
    "A01_FREEZE_AND_SOURCE_PACKET": (
        "TARGET_L12_STORAGE_CACHE_FREEZE_V012",
        _keyset("""cache_payload_created claim_boundary current_v004_target_or_hostile_execution_interrupted current_v004_workspace_output_or_cache_read_or_modified files frozen_before_nonphysical_preflight_output hard_locks obstruction_evidence physical_history_executed predecessor_compatibility_custody predecessor_v006_obstruction_custody predecessor_v007_obstruction_custody predecessor_v008_obstruction_custody predecessor_v009_obstruction_custody predecessor_v010_obstruction_custody predecessor_v011_obstruction_custody resource_limits schema sealed_dependencies sealed_input_commit status storage_census_including_offsets_and_full_masks"""),
        ("status", "FROZEN_BEFORE_NONPHYSICAL_PREFLIGHT_V001_OUTPUT"),
        "AUDIT_BOUND_COMPATIBILITY_SUCCESSOR_PRE_PAYLOAD__NO_HISTORY_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
    ),
    "A02_NONPHYSICAL_PREFLIGHT": (
        "TARGET_L12_STORAGE_CACHE_NONPHYSICAL_PREFLIGHT_V012",
        _keyset("""L4_differential allocation_census checks claim_boundary classification compatibility files mutation_ledger physical_cache_payload_created physical_history_executed resource_limits schema"""),
        ("classification", "PASS_NONPHYSICAL_EXHAUSTIVE_INDEX_ALLOCATION_AND_HARD_LOCK_PREFLIGHT"),
        "V012_PORTABLE_NONPHYSICAL_STORAGE_INDEX_PROOF_ONLY__NO_CACHE_PAYLOAD_HISTORY_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
    ),
    "A03_PREPAYLOAD_AUDIT": (
        "TARGET_V012_PREPAYLOAD_HOSTILE_AUDIT_V001",
        _keyset("""absence_census audited_files_sha256 audited_freeze_sha256 audited_packet auditor_role checks checks_passed checks_total claim_boundary classification failures mutation_ledger no_symlinked_inputs payload_or_history_executed preflight_result_sha256 schema sealed_input_commit v005_v006_v007_v008_v009_v010_v011_bytes_preserved"""),
        ("classification", "PASS_TARGET_V012_PREPAYLOAD_CONTROL_PLANE"),
        "V012_PREPAYLOAD_CONTROL_PLANE_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),
    "A04_UNIVERSAL_CUSTODY_GATE": (
        "TARGET_V012_DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE",
        _keyset("""authorized_cache_lengths builder_sha256 claim_boundary classification consumer_sha256 freeze_sha256 hostile_v003_sha256 independent_hostile_audit method_sha256 obstructions preflight_result_sha256 preflight_sha256 preserved_workspace_cross_diagnostic_sha256 preserved_workspace_custody_sha256 runtime_compatibility_obstruction_sha256 schema superseded_v005_cache_manifest_sha256_by_L superseded_v005_dual_gate_sha256 superseded_v007_cache_manifest_sha256_by_L superseded_v007_dual_gate_sha256 superseded_v008_cache_manifest_sha256_by_L superseded_v008_dual_gate_sha256 target_v004_sha256 v006_hostile_audit_obstruction_sha256 v007_runtime_compatibility_obstruction_sha256 v008_postbuild_audit_binding_obstruction_sha256 v009_hostile_audit_obstruction_sha256 v010_audit_record_custody_correction_sha256 v010_hostile_audit_obstruction_sha256 v011_hostile_audit_obstruction_sha256"""),
        ("classification", "AUTHORIZE_TARGET_V012_FRESH_CACHE_AFTER_V005_V006_V007_V008_V009_V010_AND_V011_CONTROL_PLANE_OBSTRUCTIONS"),
        "CONTROL_PLANE_AUTHORIZATION_ONLY__NO_CACHE_HISTORY_OR_PHYSICS_RESULT",
    ),
    "A05_FIVE_CACHE_SET": (
        "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012",
        _keyset("""L basis_order builder_sha256 canonical_cache_root claim_boundary consumer_sha256 dual_obstruction_gate_sha256 edge_layout files freeze_sha256 hamiltonian_exchange_coefficient hostile_v003_freeze_sha256 hostile_v003_method_sha256 hostile_v003_sha256 independent_hostile_audit_sha256 lineage_identity method_sha256 payload preflight_result_sha256 preflight_sha256 preserved_workspace_cross_diagnostic_sha256 preserved_workspace_custody_sha256 production_obligation_validators_sha256 resource_certificates runtime_compatibility_obstruction_sha256 schema status superseded_v005_cache_manifest_sha256_by_L superseded_v005_dual_gate_sha256 superseded_v007_cache_manifest_sha256_by_L superseded_v007_dual_gate_sha256 superseded_v008_cache_manifest_sha256_by_L superseded_v008_dual_gate_sha256 target_v004_freeze_sha256 target_v004_method_sha256 target_v004_original_l12_gate_sha256 target_v004_sha256 v006_hostile_audit_obstruction_sha256 v007_runtime_compatibility_obstruction_sha256 v008_postbuild_audit_binding_obstruction_sha256 v009_hostile_audit_obstruction_sha256 v010_audit_record_custody_correction_sha256 v010_hostile_audit_obstruction_sha256 v011_hostile_audit_obstruction_sha256"""),
        ("status", "COMPLETE_HASH_PINNED_TARGET_STORAGE_ONLY_CACHE"),
        "TARGET_V012_PORTABLE_STORAGE_INDICES_ONLY__NO_HISTORY_SPECTRUM_OR_GRAVITY",
    ),
    "A06_POSTBUILD_AUDIT": (
        "TARGET_V012_POSTBUILD_PAYLOAD_AUDIT_V001",
        _keyset("""audited_packet auditor_role checks checks_passed checks_total claim_boundary classification dual_obstruction_and_compatibility_gate_sha256 failures manifest_sha256_by_L no_symlinked_or_writable_payload_inputs payload_census_by_L physical_gate_or_history_executed prebuild_hostile_audit_sha256 schema sealed_input_commit semantic_cachecontext"""),
        ("classification", "PASS_TARGET_V012_FRESH_STORAGE_CACHE_PAYLOADS"),
        "POSTBUILD_STORAGE_CACHE_AUDIT_ONLY__NO_PHYSICAL_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),
    "A07_BASE_PHYSICAL_GATE": (
        "TARGET_V012_CACHE_PHYSICAL_EXECUTION_GATE",
        _keyset("""authorized_lengths builder_sha256 cache_manifest_sha256_by_L claim_boundary classification consumer_sha256 dual_obstruction_gate_sha256 freeze_sha256 independent_hostile_audit_sha256 method_sha256 original_target_l12_gate_sha256 postbuild_payload_audit preflight_result_sha256 preflight_sha256 preserved_workspace_cross_diagnostic_sha256 preserved_workspace_custody_sha256 runtime_compatibility_obstruction_sha256 schema target_v004_sha256 v006_hostile_audit_obstruction_sha256 v007_runtime_compatibility_obstruction_sha256 v008_postbuild_audit_binding_obstruction_sha256 v009_hostile_audit_obstruction_sha256 v010_audit_record_custody_correction_sha256 v010_hostile_audit_obstruction_sha256 v011_hostile_audit_obstruction_sha256"""),
        ("classification", "AUTHORIZE_TARGET_V012_CACHED_PHYSICAL_EXECUTION"),
        "BASE_PHYSICAL_GATE_BINDING_ONLY__OUTER_HOSTILE_AUDIT_AUTHORIZATION_REQUIRED__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),
    "A08_PHYSICAL_GATE_AUDIT": (
        "TARGET_V012_PHYSICAL_GATE_HOSTILE_AUDIT_V001",
        _keyset("""audited_packet auditor_role base_gate_exact_key_census_passed base_gate_exact_key_census_sha256 checks checks_passed checks_total claim_boundary classification consumer_sha256 failures freeze_sha256 physical_execution_gate_sha256 physical_history_executed postbuild_payload_audit_sha256 schema sealed_input_commit"""),
        ("classification", "PASS_TARGET_V012_PHYSICAL_GATE_BINDINGS"),
        "PHYSICAL_GATE_CONTROL_PLANE_AUDIT_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),
    "A09_CONTROL_AUTHORIZATION": (
        "TARGET_V012_CONTROL_EXECUTION_AUTHORIZATION_GATE_V001",
        _keyset("""authorized_lengths builder_sha256 claim_boundary classification consumer_sha256 freeze_sha256 method_sha256 physical_execution_gate physical_gate_hostile_audit postbuild_payload_audit preflight_result_sha256 schema"""),
        ("classification", "AUTHORIZE_AUDITED_TARGET_V012_CONTROLS_L4_L6_L8"),
        "AUDITED_CONTROL_EXECUTION_AUTHORIZATION_ONLY__NO_L10_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),
    "A11_CONTROL_STAGE_GATE": (
        "TARGET_V012_CACHED_CONTROL_L4_L8_GATE",
        _keyset("""builder_sha256 cache_manifest_sha256_by_L claim_boundary classification consumer_sha256 freeze_sha256 histories independent_hostile_audit_sha256 method_sha256 original_target_l12_gate_sha256 physical_execution_gate_sha256 preflight_result_sha256 preflight_sha256 preserved_workspace_cross_diagnostic_sha256 preserved_workspace_custody_sha256 runtime_compatibility_obstruction_sha256 schema target_v004_sha256 v006_hostile_audit_obstruction_sha256 v007_runtime_compatibility_obstruction_sha256 v008_postbuild_audit_binding_obstruction_sha256 v009_hostile_audit_obstruction_sha256 v010_audit_record_custody_correction_sha256 v010_hostile_audit_obstruction_sha256 v011_hostile_audit_obstruction_sha256"""),
        ("classification", "PASS_TARGET_V012_CACHED_CONTROLS_L4_L6_L8"),
        "FINITE_CACHED_CONTROL_STAGE_ONLY__NO_L10_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),
    "A12_CONTROL_STAGE_AUDIT": (
        "TARGET_V012_CACHED_CONTROL_L4_L8_GATE_AUDIT_V001",
        _keyset("""audited_packet auditor_role canonical_v004_sha256_by_L checks checks_passed checks_total claim_boundary classification failures history_sha256_by_L schema sealed_input_commit stage_gate_sha256"""),
        ("classification", "PASS_INDEPENDENT_TARGET_V012_CACHED_CONTROLS_L4_L8"),
        "FINITE_STAGE_GATE_AUDIT_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY_RESULT",
    ),
    "A13_L10_AUTHORIZATION": (
        "TARGET_V012_L10_EXECUTION_AUTHORIZATION_GATE_V001",
        _keyset("""authorized_length builder_sha256 cached_control_l4_l8_gate_audit_sha256 cached_control_l4_l8_gate_sha256 claim_boundary classification consumer_sha256 freeze_sha256 l10_cache_manifest_sha256 method_sha256 physical_execution_gate_sha256 schema"""),
        ("classification", "AUTHORIZE_AUDITED_TARGET_V012_L10"),
        "FINITE_L10_PROMOTION_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),
    "A15_L10_STAGE_GATE": (
        "TARGET_V012_CACHED_L10_GATE",
        _keyset("""builder_sha256 cache_manifest_sha256_by_L cached_control_l4_l8_gate_sha256 claim_boundary classification consumer_sha256 freeze_sha256 histories independent_hostile_audit_sha256 l10_execution_authorization_gate_sha256 method_sha256 original_target_l12_gate_sha256 physical_execution_gate_sha256 preflight_result_sha256 preflight_sha256 preserved_workspace_cross_diagnostic_sha256 preserved_workspace_custody_sha256 runtime_compatibility_obstruction_sha256 schema target_v004_sha256 v006_hostile_audit_obstruction_sha256 v007_runtime_compatibility_obstruction_sha256 v008_postbuild_audit_binding_obstruction_sha256 v009_hostile_audit_obstruction_sha256 v010_audit_record_custody_correction_sha256 v010_hostile_audit_obstruction_sha256 v011_hostile_audit_obstruction_sha256"""),
        ("classification", "PASS_TARGET_V012_CACHED_L10"),
        "FINITE_CACHED_L10_STAGE_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),
    "A16_L10_STAGE_AUDIT": (
        "TARGET_V012_CACHED_L10_GATE_AUDIT_V001",
        _keyset("""audited_packet auditor_role canonical_v004_sha256_by_L checks checks_passed checks_total claim_boundary classification failures history_sha256_by_L l10_execution_authorization_gate_sha256 schema sealed_input_commit stage_gate_sha256"""),
        ("classification", "PASS_INDEPENDENT_TARGET_V012_CACHED_L10"),
        "FINITE_STAGE_GATE_AUDIT_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY_RESULT",
    ),
    "A17_HOSTILE_L12_ELIGIBILITY": (
        None,
        _keyset("""L12_cache_manifest builder cached_L10_gate consumer freeze independent_audit method preflight preflight_result role"""),
        ("role", "hostile_v004r4"), None,
    ),
    "A18_L10_CROSS_GATE": (
        "TARGET_V012_HOSTILE_V004R4_L10_CROSS_GATE_V001",
        _keyset("""L auditor_role checks checks_passed checks_total claim_boundary classification comparison_policy failures hostile schema sealed_input_commit target"""),
        ("classification", "PASS_EXACT_TARGET_HOSTILE_L10_CROSS_BENCHMARK"),
        "FINITE_L10_TARGET_HOSTILE_CROSS_AUDIT_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    ),
    "A20_SHARED_SCHEDULE_GATE": (
        "V012_DUAL_L12_READINESS_SCHEDULE_V001",
        _keyset("""claim_boundary classification created_epoch expires_epoch l10_cross_gate_sha256 resource_snapshot roles schedule schema telemetry"""),
        ("classification", "READY_FOR_INDEPENDENT_SCHEDULE_AUDIT"),
        "READINESS_AND_RESOURCE_SCHEDULING_ONLY__NO_L12_RELEASE_OR_RESULT",
    ),
    "A21_SHARED_SCHEDULE_AUDIT": (
        "V012_DUAL_L12_READINESS_SCHEDULE_AUDIT_V001",
        _keyset("""auditor_role checks checks_passed checks_total claim_boundary classification failures l10_cross_gate_sha256 schedule_sha256 schema"""),
        ("classification", "PASS_INDEPENDENT_PREAUTHORIZATION_READINESS_AUDIT"),
        "INDEPENDENT_READINESS_AUDIT_ONLY__NO_L12_AUTHORIZATION_RELEASE_OR_RESULT",
    ),
}
A03_AUDITED_FILES: Final[set[str]] = {
    "METHOD.md",
    "build_target_cache.py",
    "consume_target_cache.py",
    "production_obligation_validators.py",
    "validate_preflight.py",
}
UPSTREAM_HISTORY_KEYS: Final[set[str]] = TARGET_HISTORY_KEYS - {
    "dual_l12_launch_handshake_sha256",
    "dual_l12_worker_release_sha256",
    "hostile_l12_execution_gate_sha256",
}
UPSTREAM_HISTORY_STAGE_HASH_KEYS: Final[tuple[str, ...]] = (
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
UPSTREAM_SANCTIONED_NULL_STAGE_HASH_KEYS: Final[
    dict[str, frozenset[str]]
] = {
    "A10_CONTROL_HISTORIES": frozenset(
        UPSTREAM_HISTORY_STAGE_HASH_KEYS
    ),
    "A14_L10_HISTORY": frozenset(
        UPSTREAM_HISTORY_STAGE_HASH_KEYS[3:]
    ),
    "A24_TARGET_L12_HISTORY": frozenset(),
}
UPSTREAM_CANONICAL_V004_HISTORY_SHA256: Final[dict[int, str]] = {
    4: "8bf8f4eb54781c599a9fb3ae407207e08504396128c82e1e838d5b47a1d564b2",
    6: "06ccf6f419b8e743c6aea014c90ba1598786fc5bb28331488cde0f0846215f33",
    8: "affc775a91186883b5dd7c7180340b06105523ad5744c38a470331c1a631868a",
    10: "873e45b6b37654910947711af1d8dc93d0def8ea0ef994587db206ab47b4267c",
}
UPSTREAM_CANONICAL_V004_L10_PATH: Final[Path] = (
    ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/BENCHMARK/"
    "TARGET_V004_QSHARD_L10.json"
)
UPSTREAM_STAGE_AUDIT_CHECKS: Final[dict[str, dict[str, int]]] = {
    "A12_CONTROL_STAGE_AUDIT": {
        "stage_gate_exact_schema": 1,
        "history_records": 3,
        "canonical_v004_projection_records": 3,
        "terminal_shard_records": 18,
        "stable_descriptor_records": 22,
    },
    "A16_L10_STAGE_AUDIT": {
        "stage_gate_exact_schema": 1,
        "history_records": 1,
        "canonical_v004_projection_records": 1,
        "terminal_shard_records": 10,
        "stable_descriptor_records": 12,
    },
}
UPSTREAM_A14_RESOURCE_FIXED: Final[dict[str, int | float | bool]] = {
    "peak_live_state_bytes": 209_972_192,
    "cache_payload_bytes": 44_512_948,
    "combined_with_reserve_bytes": 255_533_716,
    "scratch_limit_bytes": 21_474_836_480,
    "maximum_numerical_workset_bytes": 995_232_768,
    "numerical_workset_limit_bytes": 1_000_000_000,
    "terminal_cache_peak_bytes": 13_818_936,
    "authentication_cache_peak_bytes": 14_874_736,
    "maximum_cache_window_bytes": 14_874_736,
    "mapped_cache_limit_bytes": 536_870_912,
    "rss_limit_bytes": RSS_LIMIT,
    "wall_limit_seconds": WALL_LIMIT,
    "passed": True,
}
UPSTREAM_INHERITED_PHYSICAL_FIELDS: Final[set[str]] = {
    "original_target_l12_gate_sha256",
    "preserved_workspace_custody_sha256",
    "preserved_workspace_cross_diagnostic_sha256",
    "runtime_compatibility_obstruction_sha256",
    "v006_hostile_audit_obstruction_sha256",
    "v007_runtime_compatibility_obstruction_sha256",
    "v008_postbuild_audit_binding_obstruction_sha256",
    "v009_hostile_audit_obstruction_sha256",
    "v010_hostile_audit_obstruction_sha256",
    "v010_audit_record_custody_correction_sha256",
    "v011_hostile_audit_obstruction_sha256",
    "preflight_result_sha256", "independent_hostile_audit_sha256",
    "target_v004_sha256",
}


def _validate_hash_fields(value: object, aid: str, label: str = "record") -> None:
    if type(value) is dict:
        for key, child in value.items():
            if key == "sha256" or key.endswith("_sha256"):
                _sha(child, aid, f"{label}.{key}")
            elif key.endswith("_sha256_by_L"):
                if type(child) is not dict or not child:
                    _fail(aid, f"{label}.{key} hash map mismatch")
                for length, digest in child.items():
                    if type(length) is not str or not length.isdigit():
                        _fail(aid, f"{label}.{key} length key mismatch")
                    _sha(digest, aid, f"{label}.{key}.{length}")
            else:
                _validate_hash_fields(child, aid, f"{label}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            _validate_hash_fields(child, aid, f"{label}[{index}]")


def _upstream_target_history_path(length: int, fixture_mode: bool) -> str:
    if fixture_mode:
        return f"/synthetic/HISTORY_L{length}.json"
    return (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/"
        f"HISTORY_L{length}.json"
    )


def _validate_upstream_stage_gate(
    artifact_id: str, row: dict[str, object], aid: str, fixture_mode: bool,
) -> None:
    lengths = (
        (4, 6, 8) if artifact_id == "A11_CONTROL_STAGE_GATE" else (10,)
    )
    histories = row.get("histories")
    if type(histories) is not list or len(histories) != len(lengths):
        _fail(aid, f"{artifact_id} history census mismatch")
    observed_hashes: dict[str, str] = {}
    for expected_length, value in zip(lengths, histories):
        history = _keys(
            value, {"L", "path", "sha256"}, aid,
            f"{artifact_id} history L{expected_length}",
        )
        if _integer(
            history["L"], aid, f"{artifact_id} history length", 1,
        ) != expected_length:
            _fail(aid, f"{artifact_id} history order mismatch")
        path = _string(
            history["path"], aid, f"{artifact_id} history path",
        )
        expected_path = _upstream_target_history_path(
            expected_length, fixture_mode,
        )
        if (
            "\x00" in path or str(Path(path)) != path
            or path != expected_path
        ):
            _fail(aid, f"{artifact_id} history canonical path mismatch")
        observed_hashes[str(expected_length)] = _sha(
            history["sha256"], aid,
            f"{artifact_id} history L{expected_length} hash",
        )
    manifests = row.get("cache_manifest_sha256_by_L")
    expected_keys = {str(length) for length in lengths}
    if type(manifests) is not dict or set(manifests) != expected_keys:
        _fail(aid, f"{artifact_id} cache-manifest census mismatch")
    for length, digest in manifests.items():
        _sha(digest, aid, f"{artifact_id} cache manifest L{length}")
    if len(set(observed_hashes.values())) != len(observed_hashes):
        _fail(aid, f"{artifact_id} history digest alias")


def _validate_upstream_stage_audit(
    artifact_id: str, row: dict[str, object], aid: str,
) -> None:
    lengths = (
        (4, 6, 8) if artifact_id == "A12_CONTROL_STAGE_AUDIT" else (10,)
    )
    if (
        row.get("auditor_role") != "INDEPENDENT_HOSTILE_STAGE_GATE_REVIEW"
        or row.get("audited_packet")
        != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        or row.get("sealed_input_commit")
        != "42f1ea3301ccf98802c07f3330d52999385cba0b"
    ):
        _fail(aid, f"{artifact_id} audit identity mismatch")
    expected_checks = UPSTREAM_STAGE_AUDIT_CHECKS[artifact_id]
    if row.get("checks") != expected_checks or any(
        type(value) is not int for value in row.get("checks", {}).values()
    ):
        _fail(aid, f"{artifact_id} exact check map mismatch")
    expected_total = sum(expected_checks.values())
    if (
        _integer(row.get("checks_total"), aid, "upstream checks total", 1)
        != expected_total
        or _integer(
            row.get("checks_passed"), aid, "upstream checks passed", 1,
        ) != expected_total
        or row.get("failures") != []
    ):
        _fail(aid, f"{artifact_id} check reconstruction mismatch")
    expected_keys = {str(length) for length in lengths}
    histories = row.get("history_sha256_by_L")
    canonical = row.get("canonical_v004_sha256_by_L")
    if (
        type(histories) is not dict or set(histories) != expected_keys
        or type(canonical) is not dict or set(canonical) != expected_keys
    ):
        _fail(aid, f"{artifact_id} history-map census mismatch")
    for length in lengths:
        key = str(length)
        _sha(histories[key], aid, f"{artifact_id} history L{length}")
        if canonical[key] != UPSTREAM_CANONICAL_V004_HISTORY_SHA256[length]:
            _fail(aid, f"{artifact_id} canonical V004 map mismatch")


def _open_hash_pinned_reference_json(
    path: Path, digest: str, aid: str, label: str,
) -> dict[str, object]:
    """Read a committed reference by stable descriptor and exact byte hash.

    The reviewed V004 reference is deliberately not a live owner-once output:
    its repository mode is 0644.  This reader therefore matches the target
    consumer's ``require_immutable_mode=False`` treatment while retaining
    no-symlink, inode, parent, byte-hash, and before/after stability checks.
    """
    _require_no_symlink_parents(str(path), aid, label)
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    parent_descriptor = -1
    descriptor = -1
    try:
        parent_descriptor = os.open(path.parent, parent_flags)
        parent_before = _parent_identity(
            path.parent, parent_descriptor, aid, label,
        )
        descriptor = os.open(
            path.name,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=parent_descriptor,
        )
        before = os.fstat(descriptor)
        path_before = os.stat(
            path.name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
        identity = _complete_identity(before)
        if (
            not stat.S_ISREG(before.st_mode) or before.st_nlink != 1
            or _complete_identity(path_before) != identity
        ):
            _fail(aid, f"{label} is not an owner-once ordinary file")
        raw = _descriptor_bytes(descriptor, before.st_size, aid, label)
        observed = hashlib.sha256(raw).hexdigest()
        after = os.fstat(descriptor)
        path_after = os.stat(
            path.name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
        if (
            observed != digest or _complete_identity(after) != identity
            or _complete_identity(path_after) != identity
            or _parent_identity(path.parent, parent_descriptor, aid, label)
            != parent_before
        ):
            _fail(aid, f"{label} changed during descriptor authentication")
        record = _strict_json(raw, aid)
        if type(record) is not dict:
            _fail(aid, f"{label} is not a JSON object")
        return record
    except Refusal:
        raise
    except (OSError, TypeError, ValueError) as error:
        raise Refusal(f"{aid}: {label} stable descriptor unavailable") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if parent_descriptor >= 0:
            os.close(parent_descriptor)


def _upstream_canonical_v004_l10(aid: str) -> dict[str, object]:
    return _open_hash_pinned_reference_json(
        UPSTREAM_CANONICAL_V004_L10_PATH,
        UPSTREAM_CANONICAL_V004_HISTORY_SHA256[10], aid,
        "hash-pinned canonical V004 L10 history",
    )


def _validate_upstream_a14_history(
    row: dict[str, object], aid: str, fixture_mode: bool,
) -> None:
    canonical = _upstream_canonical_v004_l10(aid)
    if (
        _integer(row.get("L"), aid, "A14 L", 1) != 10
        or _integer(row.get("events"), aid, "A14 events", 1) != 10
        or _integer(row.get("dimension"), aid, "A14 dimension", 1)
        != math.comb(30, 10)
        or _integer(
            row.get("preterminal_dimension"), aid,
            "A14 preterminal dimension", 1,
        ) != math.comb(29, 9)
        or _integer(row.get("edges"), aid, "A14 edge census", 1) != 30
        or row.get("representation")
        != "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__AUTHENTICATED_INDEX_CACHE"
        or row.get("lineage_authority")
        != "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING"
    ):
        _fail(aid, "A14 history identity/dimension mismatch")
    for key in ("coarse_method", "fine_method"):
        if _projection_linf(
            row.get(key), canonical.get(key), aid, f"A14 {key}",
        ) != 0.0:
            _fail(aid, f"A14 {key} canonical V004 mismatch")
    rows = row.get("rows")
    canonical_rows = canonical.get("rows")
    if (
        type(rows) is not list or len(rows) != 10
        or type(canonical_rows) is not list or len(canonical_rows) != 10
    ):
        _fail(aid, "A14 history row census mismatch")
    for event, (observed, reference) in enumerate(
        zip(rows, canonical_rows), start=1,
    ):
        event_row = _keys(observed, ROW_KEYS, aid, f"A14 event {event}")
        _keys(reference, ROW_KEYS, aid, f"canonical V004 event {event}")
        if (
            _integer(event_row["event"], aid, "A14 event", 1) != event
            or _integer(
                event_row["cursor_vertex"], aid, "A14 cursor vertex",
            ) != event - 1
        ):
            _fail(aid, f"A14 event {event} order/cursor mismatch")
        _solver(
            event_row["actual_solver"], aid,
            f"A14 event {event} actual solver", event=event, null=False,
        )
        _solver(
            event_row["null_solver"], aid,
            f"A14 event {event} null solver", event=event, null=True,
        )
        projected = {
            key: value for key, value in event_row.items()
            if key not in {"actual_solver", "null_solver"}
        }
        canonical_projected = {
            key: value for key, value in reference.items()
            if key not in {"actual_solver", "null_solver"}
        }
        if _projection_linf(
            projected, canonical_projected, aid,
            f"A14 event {event} canonical V004 projection",
        ) > TOLERANCE:
            _fail(aid, f"A14 event {event} canonical V004 mismatch")
    comparison = _keys(
        row.get("comparison"), COMPARISON_KEYS, aid, "A14 comparison",
    )
    if (
        _boolean(comparison.get("resolved"), aid, "A14 comparison resolved")
        is not True
        or _projection_linf(
            comparison, canonical.get("comparison"), aid,
            "A14 comparison canonical V004 projection",
        ) > TOLERANCE
    ):
        _fail(aid, "A14 comparison canonical V004 mismatch")
    resource = _keys(
        row.get("resource"), RESOURCE_KEYS, aid, "A14 resource",
    )
    for key, expected in UPSTREAM_A14_RESOURCE_FIXED.items():
        if type(resource.get(key)) is not type(expected) or resource[key] != expected:
            _fail(aid, f"A14 resource exact mismatch: {key}")
    if (
        not 0 < _integer(resource.get("peak_rss_bytes"), aid, "A14 peak RSS")
        <= RSS_LIMIT
        or not 0.0 < _float(
            resource.get("wall_seconds"), aid, "A14 wall seconds",
        ) <= WALL_LIMIT
        or resource["maximum_numerical_workset_bytes"]
        != max(
            event_row[solver]["maximum_live_bytes"]
            for event_row in rows
            for solver in ("actual_solver", "null_solver")
        )
    ):
        _fail(aid, "A14 resource reconstruction mismatch")
    shards = row.get("terminal_shards")
    canonical_shards = canonical.get("terminal_shards")
    if (
        type(shards) is not list or len(shards) != 10
        or type(canonical_shards) is not list or len(canonical_shards) != 10
    ):
        _fail(aid, "A14 terminal shard census mismatch")
    for q, (value, reference) in enumerate(zip(shards, canonical_shards)):
        shard = _keys(
            value, {"q", "path", "shape", "bytes", "sha256"}, aid,
            f"A14 terminal q={q}",
        )
        expected_path = (
            f"/synthetic/A14_L10_HISTORY/terminal_q{q}.npy"
            if fixture_mode else str(
                ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                f"WORKSPACES/L10/sharp/prefix_09/q_{q:02d}.npy"
            )
        )
        _path(shard.get("path"), expected_path, aid, f"A14 terminal q={q}")
        if (
            _integer(shard.get("q"), aid, "A14 terminal q") != q
            or shard.get("shape") != reference.get("shape")
            or any(type(item) is not int for item in shard.get("shape", []))
            or _integer(
                shard.get("bytes"), aid, "A14 terminal bytes", 1,
            ) != reference.get("bytes")
            or shard.get("sha256") != reference.get("sha256")
        ):
            _fail(aid, f"A14 terminal q={q} canonical V004 mismatch")


def _validate_independent_upstream_record(
    artifact_id: str, value: object, aid: str, fixture_mode: bool = False,
) -> dict[str, object]:
    record = _strict_json(value, aid)
    sanitized_hash_row = None
    if artifact_id in {"A10_CONTROL_HISTORIES", "A14_L10_HISTORY"}:
        row = _keys(record, UPSTREAM_HISTORY_KEYS, aid, artifact_id)
        expected_length = None
        if artifact_id == "A10_CONTROL_HISTORIES":
            if row.get("L") not in (4, 6, 8):
                _fail(aid, "control history length mismatch")
        else:
            expected_length = 10
        if (
            row.get("schema") != "TARGET_CACHED_PREFIX_HISTORY_V012"
            or (expected_length is not None and row.get("L") != expected_length)
            or row.get("claim_boundary")
            != "FINITE_CACHED_TARGET_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY"
        ):
            _fail(aid, f"{artifact_id} identity mismatch")
        sanctioned_nulls = UPSTREAM_SANCTIONED_NULL_STAGE_HASH_KEYS[
            artifact_id
        ]
        for key in UPSTREAM_HISTORY_STAGE_HASH_KEYS:
            if key in sanctioned_nulls:
                if row.get(key) is not None:
                    _fail(aid, f"{artifact_id} stage predecessor mismatch")
            else:
                _sha(row.get(key), aid, f"{artifact_id}.{key}")
        sanitized_hash_row = dict(row)
        for key in sanctioned_nulls:
            sanitized_hash_row.pop(key)
        if artifact_id == "A14_L10_HISTORY":
            _validate_upstream_a14_history(row, aid, fixture_mode)
    elif artifact_id == "A22_TARGET_L12_AUTHORIZATION":
        schema = record.get("schema")
        expected = {
            "TARGET_V012_L12_ONE_WAY_AUTHORIZATION_V001": _keyset("""authorized_length claim_boundary classification consumer_sha256 l10_cross_gate_sha256 l12_cache_manifest_sha256 role schedule_audit_sha256 schedule_sha256 schema"""),
            "HOSTILE_V004R4_L12_ONE_WAY_AUTHORIZATION_V001": _keyset("""authorized_length claim_boundary classification consumer_sha256 l10_cross_gate_sha256 l12_cache_manifest_sha256 role schedule_audit_sha256 schedule_sha256 schema"""),
            "V012_L12_WORKER_READY_V001": _keyset("""blocked_on_release control_channel_id executable_path executable_sha256 nonce_commitment_sha256 output_path process_id process_start_token ready_epoch role schema worker_id workspace_path"""),
            "V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002": _keyset("""authorization_sha256_by_role claim_boundary classification created_epoch launch_skew_seconds_max memory_pressure observed_readiness_skew_seconds ready_sha256_by_role schedule_audit_sha256 schedule_sha256 schema telemetry workers"""),
            "V012_DUAL_L12_WORKER_RELEASE_V002": _keyset("""authorization_sha256_by_role claim_boundary classification handshake_sha256 observed_launch_skew_seconds release_by_role release_epoch_by_role schema"""),
            "V012_L12_WORKER_RELEASE_COMMAND_V001": _keyset("""control_channel_id handshake_sha256 nonce_commitment_sha256 process_id process_start_token release_epoch role schema worker_id worker_release_sha256"""),
            "V012_L12_WORKER_RELEASE_ACK_V001": _keyset("""ack_sha256 control_channel_id nonce_hex process_id process_start_token role schema worker_id"""),
            "V012_L12_WORKER_COMPLETION_V001": _keyset("""blocked_on_orchestrator_close completion_epoch control_channel_id output_path output_sha256 process_id process_start_token role schema worker_id"""),
        }
        if schema not in expected:
            _fail(aid, "A22 schema mismatch")
        row = _keys(record, expected[schema], aid, "A22 record")
    else:
        if artifact_id not in UPSTREAM_AUTHORITY_SHAPES:
            _fail(aid, "unknown independent upstream authority")
        schema, keys, identity, claim = UPSTREAM_AUTHORITY_SHAPES[artifact_id]
        row = _keys(record, keys, aid, artifact_id)
        if schema is not None and row.get("schema") != schema:
            _fail(aid, f"{artifact_id} schema mismatch")
        if identity is not None and row.get(identity[0]) != identity[1]:
            _fail(aid, f"{artifact_id} identity mismatch")
        if claim is not None and row.get("claim_boundary") != claim:
            _fail(aid, f"{artifact_id} claim boundary mismatch")
        if artifact_id in {"A11_CONTROL_STAGE_GATE", "A15_L10_STAGE_GATE"}:
            _validate_upstream_stage_gate(
                artifact_id, row, aid, fixture_mode,
            )
        elif artifact_id in {
            "A12_CONTROL_STAGE_AUDIT", "A16_L10_STAGE_AUDIT",
        }:
            _validate_upstream_stage_audit(artifact_id, row, aid)
        elif artifact_id == "A13_L10_AUTHORIZATION" and _integer(
            row.get("authorized_length"), aid, "A13 authorized length", 1,
        ) != 10:
            _fail(aid, "A13 authorized length mismatch")
    if artifact_id == "A03_PREPAYLOAD_AUDIT":
        audited_files = row.get("audited_files_sha256")
        if type(audited_files) is not dict or set(audited_files) != A03_AUDITED_FILES:
            _fail(aid, "A03 audited file census mismatch")
        for path, digest in audited_files.items():
            _sha(
                digest, aid,
                f"A03_PREPAYLOAD_AUDIT.audited_files_sha256.{path}",
            )
        row = dict(row)
        row.pop("audited_files_sha256")
    _validate_hash_fields(
        sanitized_hash_row if sanitized_hash_row is not None else row,
        aid, artifact_id,
    )
    if "checks_total" in row:
        total = _integer(row["checks_total"], aid, "upstream checks total", 1)
        if (
            _integer(row["checks_passed"], aid, "upstream checks passed", 1)
            != total or row.get("failures") != []
        ):
            _fail(aid, "upstream audit result mismatch")
    return row


def _a17_authority_binding(
    value: object, aid: str, fixture_mode: bool,
) -> tuple[
    str, int, dict[str, object], str, list[_StableInput], list[str],
    dict[str, str],
]:
    expected = {
        "artifact_id", "instance", "sources", "sha256", "record",
        "source_records",
    } if fixture_mode else {
        "artifact_id", "instance", "sources", "sha256",
    }
    row = _keys(value, expected, aid, "A17 composite authority binding")
    if (
        row["artifact_id"] != "A17_HOSTILE_L12_ELIGIBILITY"
        or row["instance"] != 1 or type(row["instance"]) is not int
    ):
        _fail(aid, "A17 composite authority identity mismatch")
    digest = _sha(row["sha256"], aid, "A17 composite authority hash")
    sources = row["sources"]
    if type(sources) is not list or len(sources) != len(A17_SOURCE_LABELS):
        _fail(aid, "A17 nine-source census mismatch")
    source_rows: dict[str, dict[str, object]] = {}
    paths: list[str] = []
    for expected_label, value in zip(A17_SOURCE_LABELS, sources):
        source = _keys(
            value, {"label", "path", "sha256"}, aid,
            f"A17 {expected_label} source",
        )
        if source["label"] != expected_label:
            _fail(aid, "A17 source order/label mismatch")
        path_text = _string(
            source["path"], aid, f"A17 {expected_label} source path",
        )
        if (
            not path_text.startswith("/") or "\x00" in path_text
            or str(Path(path_text)) != path_text
        ):
            _fail(aid, "A17 source canonical path mismatch")
        if not fixture_mode:
            expected_path = str(
                ROOT / A17_CANONICAL_RELATIVE_PATHS[expected_label]
            )
            if path_text != expected_path:
                _fail(aid, "A17 source canonical repository path mismatch")
        source["sha256"] = _sha(
            source["sha256"], aid, f"A17 {expected_label} source hash",
        )
        source_rows[expected_label] = source
        paths.append(path_text)
    if len(set(paths)) != len(paths):
        _fail(aid, "A17 source path alias")

    retained: list[_StableInput] = []
    records: dict[str, dict[str, object]] = {}
    try:
        if fixture_mode:
            source_records = _keys(
                row["source_records"], set(A17_RECORD_IDENTITIES), aid,
                "A17 fixture source records",
            )
            for label in A17_RECORD_IDENTITIES:
                record = _strict_json(source_records[label], aid)
                if type(record) is not dict:
                    _fail(aid, f"A17 {label} fixture record mismatch")
                if record_sha256(record) != source_rows[label]["sha256"]:
                    _fail(aid, f"A17 {label} fixture content hash mismatch")
                records[label] = record
        else:
            for label in A17_SOURCE_LABELS:
                source = source_rows[label]
                if label in A17_RECORD_IDENTITIES:
                    record, held = _open_immutable_json(
                        source["path"], source["sha256"], aid,
                        f"A17 {label}",
                    )
                    records[label] = record
                else:
                    held = _open_immutable_file(
                        source["path"], source["sha256"], aid,
                        f"A17 {label}",
                    )
                retained.append(held)

        branch: dict[str, object] = {"role": "hostile_v004r4"}
        for label in A17_SOURCE_LABELS:
            source = source_rows[label]
            binding = {
                "path": source["path"], "sha256": source["sha256"],
            }
            if label in A17_RECORD_IDENTITIES:
                schema, identity_field, identity_value = (
                    A17_RECORD_IDENTITIES[label]
                )
                record = records[label]
                if (
                    record.get("schema") != schema
                    or record.get(identity_field) != identity_value
                ):
                    _fail(aid, f"A17 {label} internal identity mismatch")
                binding.update({
                    "schema": schema,
                    "identity_field": identity_field,
                    "identity_value": identity_value,
                })
            branch[label] = binding
        _validate_independent_upstream_record(
            "A17_HOSTILE_L12_ELIGIBILITY", branch, aid, fixture_mode,
        )
        if record_sha256(branch) != digest:
            _fail(aid, "A17 composite authority hash mismatch")
        if fixture_mode and row["record"] != branch:
            _fail(aid, "A17 fixture composite reconstruction mismatch")
        freeze = records["freeze"]
        preflight = records["preflight_result"]
        audit = records["independent_audit"]
        cached_l10 = records["cached_L10_gate"]
        manifest = records["L12_cache_manifest"]
        frozen_files = freeze.get("files")
        primary_hashes = {
            label: source_rows[label]["sha256"]
            for label in ("method", "builder", "consumer", "preflight")
        }
        if (
            type(frozen_files) is not dict
            or any(
                frozen_files.get(Path(source_rows[label]["path"]).name)
                != primary_hashes[label]
                for label in primary_hashes
            )
            or freeze.get("cache_payload_created") is not False
            or freeze.get("physical_history_executed") is not False
            or preflight.get("files") != {
                "method_sha256": primary_hashes["method"],
                "builder_sha256": primary_hashes["builder"],
                "consumer_sha256": primary_hashes["consumer"],
                "preflight_sha256": primary_hashes["preflight"],
                "freeze_sha256": source_rows["freeze"]["sha256"],
            }
            or preflight.get("failures") != []
            or audit.get("audited_freeze_sha256")
            != source_rows["freeze"]["sha256"]
            or audit.get("audited_files_sha256") != frozen_files
            or audit.get("preflight_result_sha256")
            != source_rows["preflight_result"]["sha256"]
            or type(audit.get("checks_total")) is not int
            or audit.get("checks_total", 0) <= 0
            or type(audit.get("checks_passed")) is not int
            or audit.get("checks_passed") != audit.get("checks_total")
            or audit.get("failures") != []
            or audit.get("payload_or_history_executed") is not False
            or cached_l10.get("method_sha256") != primary_hashes["method"]
            or cached_l10.get("builder_sha256") != primary_hashes["builder"]
            or cached_l10.get("consumer_sha256") != primary_hashes["consumer"]
            or cached_l10.get("freeze_sha256")
            != source_rows["freeze"]["sha256"]
            or cached_l10.get("preflight_result_sha256")
            != source_rows["preflight_result"]["sha256"]
            or cached_l10.get("independent_hostile_audit_sha256")
            != source_rows["independent_audit"]["sha256"]
            or type(cached_l10.get("cache_manifest_sha256_by_L")) is not dict
            or set(cached_l10["cache_manifest_sha256_by_L"]) != {"10"}
            or manifest.get("L") != 12 or type(manifest.get("L")) is not int
            or manifest.get("method_sha256") != primary_hashes["method"]
            or manifest.get("builder_sha256") != primary_hashes["builder"]
            or manifest.get("consumer_sha256") != primary_hashes["consumer"]
            or manifest.get("preflight_sha256") != primary_hashes["preflight"]
            or manifest.get("freeze_sha256")
            != source_rows["freeze"]["sha256"]
            or manifest.get("preflight_result_sha256")
            != source_rows["preflight_result"]["sha256"]
            or manifest.get("independent_hostile_audit_sha256")
            != source_rows["independent_audit"]["sha256"]
        ):
            _fail(aid, "A17 hostile nine-source lineage mismatch")
        _sha(
            cached_l10["cache_manifest_sha256_by_L"]["10"], aid,
            "A17 hostile L10 cache manifest hash",
        )
        authorization = cached_l10.get("l10_execution_authorization")
        histories = cached_l10.get("histories")
        if (
            type(authorization) is not dict
            or set(authorization) != {
                "path", "sha256", "schema", "identity_field",
                "identity_value",
            }
            or type(histories) is not list or len(histories) != 1
            or type(histories[0]) is not dict
            or set(histories[0]) != {"L", "path", "sha256"}
            or histories[0].get("L") != 10
            or type(histories[0].get("L")) is not int
        ):
            _fail(aid, "A17 cached L10 predecessor projection mismatch")
        expected_authorization_path = (
            "/synthetic/a17/L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json"
            if fixture_mode else str(
                ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
                "L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json"
            )
        )
        expected_history_path = (
            "/synthetic/a17/V004R4_PHYSICAL_OUTPUTS/HISTORY_L10.json"
            if fixture_mode else
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
            "V004R4_PHYSICAL_OUTPUTS/HISTORY_L10.json"
        )
        if (
            authorization.get("path") != expected_authorization_path
            or authorization.get("schema")
            != "HOSTILE_V004R4_L10_EXECUTION_AUTHORIZATION_GATE_V001"
            or authorization.get("identity_field") != "classification"
            or authorization.get("identity_value")
            != "AUTHORIZE_AUDITED_HOSTILE_V004R4_L10"
            or histories[0].get("path") != expected_history_path
        ):
            _fail(aid, "A17 cached L10 canonical predecessor mismatch")
        authorization_sha = _sha(
            authorization.get("sha256"), aid,
            "A17 cached L10 authorization hash",
        )
        history_sha = _sha(
            histories[0].get("sha256"), aid, "A17 cached L10 history hash",
        )
        return (
            "A17_HOSTILE_L12_ELIGIBILITY", 1, branch, digest,
            retained, paths, {
                "l10_execution_authorization_sha256": authorization_sha,
                "history_sha256": history_sha,
            },
        )
    except BaseException:
        _verify_close_authority_inputs(retained)
        raise


def _authority_binding(
    value: object, aid: str, fixture_mode: bool,
) -> tuple[
    str, int, dict[str, object], str, list[_StableInput], list[str],
    dict[str, str],
]:
    if (
        type(value) is dict
        and value.get("artifact_id") == "A17_HOSTILE_L12_ELIGIBILITY"
    ):
        return _a17_authority_binding(value, aid, fixture_mode)
    expected = {"artifact_id", "instance", "path", "sha256", "record"} \
        if fixture_mode else {"artifact_id", "instance", "path", "sha256"}
    row = _keys(value, expected, aid, "authority binding")
    artifact_id = _string(row["artifact_id"], aid, "authority artifact id")
    if artifact_id not in AUTHORITY_INSTANCE_CENSUS:
        _fail(aid, "authority artifact id is outside A01-A25/A27 census")
    instance = _integer(row["instance"], aid, "authority instance", 1)
    if instance > AUTHORITY_INSTANCE_CENSUS[artifact_id]:
        _fail(aid, "authority instance is outside exact census")
    path_text = _string(row["path"], aid, "authority path")
    if (
        not path_text.startswith("/") or "\x00" in path_text
        or str(Path(path_text)) != path_text
        or (
            not fixture_mode
            and ROOT.resolve() not in Path(path_text).resolve().parents
        )
    ):
        _fail(aid, "authority canonical repository path mismatch")
    if not fixture_mode and path_text != str(
        ROOT / AUTHORITY_CANONICAL_RELATIVE_PATHS[(artifact_id, instance)]
    ):
        _fail(aid, "authority owner-once canonical path mismatch")
    digest = _sha(row["sha256"], aid, "authority hash")
    retained: _StableInput | None = None
    if fixture_mode:
        record = _strict_json(row["record"], aid)
        if type(record) is not dict or record_sha256(record) != digest:
            _fail(aid, "authority fixture content hash mismatch")
    else:
        record, retained = _open_immutable_json(
            path_text, digest, aid, f"authority {artifact_id}:{instance}",
        )
    try:
        if artifact_id in ARTIFACT_IDS:
            validate_artifact(artifact_id, record, fixture_mode=fixture_mode)
        else:
            _validate_independent_upstream_record(
                artifact_id, record, aid, fixture_mode,
            )
    except Refusal as error:
        if retained is not None:
            retained.verify_and_close()
        raise Refusal(
            f"{aid}: authority {artifact_id}:{instance} refused: {error}"
        ) from error
    except BaseException:
        if retained is not None:
            retained.verify_and_close()
        raise
    return (
        artifact_id, instance, record, digest,
        [retained] if retained is not None else [], [path_text], {},
    )


def _validate_authority_bundle(
    value: object, aid: str, fixture_mode: bool,
) -> tuple[
    dict[tuple[str, int], dict[str, object]],
    dict[tuple[str, int], str], list[_StableInput],
    dict[tuple[str, int], dict[str, str]],
]:
    if type(value) is not list or len(value) != sum(AUTHORITY_INSTANCE_CENSUS.values()):
        _fail(aid, "authority binding total census mismatch")
    records: dict[tuple[str, int], dict[str, object]] = {}
    digests: dict[tuple[str, int], str] = {}
    retained: list[_StableInput] = []
    metadata: dict[tuple[str, int], dict[str, str]] = {}
    paths: set[str] = set()
    try:
        for binding in value:
            (
                artifact_id, instance, record, digest, held, binding_paths,
                binding_metadata,
            ) = _authority_binding(
                binding, aid, fixture_mode,
            )
            retained.extend(held)
            key = (artifact_id, instance)
            if key in records or paths.intersection(binding_paths):
                _fail(aid, "authority binding instance/path alias")
            records[key] = record
            digests[key] = digest
            metadata[key] = binding_metadata
            paths.update(binding_paths)
        expected = {
            (artifact_id, instance)
            for artifact_id, count in AUTHORITY_INSTANCE_CENSUS.items()
            for instance in range(1, count + 1)
        }
        if set(records) != expected:
            _fail(aid, "authority binding instance census mismatch")
        if not fixture_mode:
            for instance, length in enumerate((4, 6, 8, 10, 12), start=1):
                if records[("A05_FIVE_CACHE_SET", instance)].get("L") != length:
                    _fail(aid, "five-cache authority length/order mismatch")
            for instance, length in enumerate((4, 6, 8), start=1):
                if records[("A10_CONTROL_HISTORIES", instance)].get("L") != length:
                    _fail(aid, "control-history authority length/order mismatch")
        return records, digests, retained, metadata
    except BaseException:
        _verify_close_authority_inputs(retained)
        raise


def _validate_terminal_authority_chain(
    records: dict[tuple[str, int], dict[str, object]],
    digests: dict[tuple[str, int], str], aid: str,
) -> None:
    """Reconstruct A18--A25/A27 from bytes; do not trust declared custody."""
    a18 = digests[("A18_L10_CROSS_GATE", 1)]
    schedule = records[("A20_SHARED_SCHEDULE_GATE", 1)]
    schedule_sha = digests[("A20_SHARED_SCHEDULE_GATE", 1)]
    schedule_audit = records[("A21_SHARED_SCHEDULE_AUDIT", 1)]
    schedule_audit_sha = digests[("A21_SHARED_SCHEDULE_AUDIT", 1)]
    a22 = {
        index: records[("A22_TARGET_L12_AUTHORIZATION", index)]
        for index in range(1, 13)
    }
    a22_hash = {
        index: digests[("A22_TARGET_L12_AUTHORIZATION", index)]
        for index in range(1, 13)
    }
    expected_schemas = {
        1: "TARGET_V012_L12_ONE_WAY_AUTHORIZATION_V001",
        2: "HOSTILE_V004R4_L12_ONE_WAY_AUTHORIZATION_V001",
        3: "V012_L12_WORKER_READY_V001",
        4: "V012_L12_WORKER_READY_V001",
        5: "V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002",
        6: "V012_DUAL_L12_WORKER_RELEASE_V002",
        7: "V012_L12_WORKER_RELEASE_COMMAND_V001",
        8: "V012_L12_WORKER_RELEASE_COMMAND_V001",
        9: "V012_L12_WORKER_RELEASE_ACK_V001",
        10: "V012_L12_WORKER_RELEASE_ACK_V001",
        11: "V012_L12_WORKER_COMPLETION_V001",
        12: "V012_L12_WORKER_COMPLETION_V001",
    }
    if any(a22[index].get("schema") != schema for index, schema in expected_schemas.items()):
        _fail(aid, "A22 authority schema/instance order mismatch")
    if schedule.get("l10_cross_gate_sha256") != a18:
        _fail(aid, "A18->A20 authority mismatch")
    if (
        schedule_audit.get("schedule_sha256") != schedule_sha
        or schedule_audit.get("l10_cross_gate_sha256") != a18
    ):
        _fail(aid, "A20->A21 authority mismatch")
    roles = {1: "target_v012", 2: "hostile_v004r4"}
    for index, role in roles.items():
        authorization = a22[index]
        if (
            authorization.get("role") != role
            or authorization.get("schedule_sha256") != schedule_sha
            or authorization.get("schedule_audit_sha256") != schedule_audit_sha
            or authorization.get("l10_cross_gate_sha256") != a18
        ):
            _fail(aid, "A21->A22 one-way authorization mismatch")
    ready = {"target_v012": a22[3], "hostile_v004r4": a22[4]}
    ready_hash = {"target_v012": a22_hash[3], "hostile_v004r4": a22_hash[4]}
    handshake = a22[5]
    if (
        handshake.get("schedule_sha256") != schedule_sha
        or handshake.get("schedule_audit_sha256") != schedule_audit_sha
        or handshake.get("authorization_sha256_by_role")
        != {"target_v012": a22_hash[1], "hostile_v004r4": a22_hash[2]}
        or handshake.get("workers") != ready
        or handshake.get("ready_sha256_by_role") != ready_hash
    ):
        _fail(aid, "A22 handshake transitive reconstruction mismatch")
    release = a22[6]
    if (
        release.get("handshake_sha256") != a22_hash[5]
        or release.get("authorization_sha256_by_role")
        != handshake.get("authorization_sha256_by_role")
    ):
        _fail(aid, "A22 release transitive reconstruction mismatch")
    for offset, role in enumerate(ROLES):
        command = a22[7 + offset]
        ack = a22[9 + offset]
        worker = ready[role]
        release_row = release["release_by_role"][role]
        expected_identity = {
            key: worker[key] for key in (
                "role", "worker_id", "process_id", "process_start_token",
                "control_channel_id", "nonce_commitment_sha256",
            )
        }
        if (
            {key: command.get(key) for key in expected_identity} != expected_identity
            or {key: release_row.get(key) for key in expected_identity}
            != expected_identity
            or command.get("handshake_sha256") != a22_hash[5]
            or command.get("worker_release_sha256") != a22_hash[6]
            or command.get("release_epoch")
            != release["release_epoch_by_role"][role]
        ):
            _fail(aid, "A22 release-command identity mismatch")
        if any(
            ack.get(key) != worker[key]
            for key in (
                "role", "worker_id", "process_id", "process_start_token",
                "control_channel_id",
            )
        ):
            _fail(aid, "A22 release ACK identity mismatch")
        nonce_hex = ack.get("nonce_hex")
        if type(nonce_hex) is not str or re.fullmatch(r"[0-9a-f]{64}", nonce_hex) is None:
            _fail(aid, "A22 release ACK nonce mismatch")
        nonce = bytes.fromhex(nonce_hex)
        if hashlib.sha256(b"V012_L12_WORKER_NONCE_V001\0" + nonce).hexdigest() \
                != worker["nonce_commitment_sha256"]:
            _fail(aid, "A22 release ACK commitment mismatch")
        expected_ack = hashlib.sha256(
            b"V012_DUAL_L12_RELEASE_ACK_V001\0" + nonce
            + canonical_json_bytes(command)
        ).hexdigest()
        if ack.get("ack_sha256") != expected_ack:
            _fail(aid, "A22 release ACK digest mismatch")
        completion_record = a22[11 + offset]
        if any(
            completion_record.get(key) != worker[key]
            for key in (
                "role", "worker_id", "process_id", "process_start_token",
                "control_channel_id",
            )
        ):
            _fail(aid, "A22 worker completion identity mismatch")
        completed = completion_record.get("completion_epoch")
        if (
            type(completed) is not int
            or not release["release_epoch_by_role"][role] < completed
            <= release["release_epoch_by_role"][role] + int(WALL_LIMIT)
            or completion_record.get("output_path") != worker["output_path"]
            or completion_record.get("blocked_on_orchestrator_close") is not True
        ):
            _fail(aid, "A22 worker completion projection mismatch")
    telemetry = records[("A23_POSTRUN_TELEMETRY", 1)]
    if (
        telemetry.get("shared_gate_sha256") != schedule_sha
        or telemetry.get("schedule_audit_sha256") != schedule_audit_sha
        or telemetry.get("dual_launch_handshake_sha256") != a22_hash[5]
        or telemetry.get("worker_release_sha256") != a22_hash[6]
        or telemetry.get("authorization_sha256_by_role")
        != handshake["authorization_sha256_by_role"]
        or telemetry.get("release_command_sha256_by_role")
        != {"target_v012": a22_hash[7], "hostile_v004r4": a22_hash[8]}
        or telemetry.get("release_ack_sha256_by_role")
        != {"target_v012": a22_hash[9], "hostile_v004r4": a22_hash[10]}
        or telemetry.get("completion_sha256_by_role")
        != {"target_v012": a22_hash[11], "hostile_v004r4": a22_hash[12]}
    ):
        _fail(aid, "A22->A23 telemetry authority mismatch")
    for role in ROLES:
        expected_telemetry_identity = {
            key: ready[role][key] for key in WORKER_IDENTITY_KEYS
        }
        if (
            telemetry.get("worker_identity_by_role", {}).get(role)
            != expected_telemetry_identity
            or telemetry.get("launch_epoch_by_role", {}).get(role)
            != release.get("release_epoch_by_role", {}).get(role)
            or telemetry.get("output_path_by_role", {}).get(role)
            != ready[role].get("output_path")
            or telemetry.get("completion_epoch_by_role", {}).get(role)
            != a22[11 + ROLES.index(role)].get("completion_epoch")
            or telemetry.get("output_sha256_by_role", {}).get(role)
            != a22[11 + ROLES.index(role)].get("output_sha256")
        ):
            _fail(aid, "A22->A23 worker identity/run-window mismatch")
    target = records[("A24_TARGET_L12_HISTORY", 1)]
    hostile = records[("A25_HOSTILE_L12_HISTORY", 1)]
    for history in (target, hostile):
        if (
            history.get("target_hostile_l10_cross_gate_sha256") != a18
            or history.get("shared_aggregate_schedule_gate_sha256") != schedule_sha
            or history.get("shared_aggregate_schedule_gate_audit_sha256")
            != schedule_audit_sha
            or history.get("dual_l12_launch_handshake_sha256") != a22_hash[5]
            or history.get("dual_l12_worker_release_sha256") != a22_hash[6]
        ):
            _fail(aid, "A18-A22->history authority mismatch")
    if (
        target.get("target_l12_execution_gate_sha256") != a22_hash[1]
        or hostile.get("hostile_l12_execution_gate_sha256") != a22_hash[2]
        or telemetry["output_sha256_by_role"]
        != {
            "target_v012": digests[("A24_TARGET_L12_HISTORY", 1)],
            "hostile_v004r4": digests[("A25_HOSTILE_L12_HISTORY", 1)],
        }
    ):
        _fail(aid, "A23-A25 terminal authority mismatch")
    if (
        a22[11].get("output_sha256")
        != digests[("A24_TARGET_L12_HISTORY", 1)]
        or a22[12].get("output_sha256")
        != digests[("A25_HOSTILE_L12_HISTORY", 1)]
    ):
        _fail(aid, "A22 completion to history authority mismatch")


def _target_branch_from_authority(
    records: dict[tuple[str, int], dict[str, object]],
    digests: dict[tuple[str, int], str], fixture_mode: bool, aid: str,
) -> dict[str, object]:
    freeze = records[("A01_FREEZE_AND_SOURCE_PACKET", 1)]
    frozen_files = freeze.get("files")
    if type(frozen_files) is not dict:
        _fail(aid, "A01 target frozen source census absent")
    source_hashes = {
        "method": frozen_files.get("METHOD.md"),
        "builder": frozen_files.get("build_target_cache.py"),
        "consumer": frozen_files.get("consume_target_cache.py"),
        "preflight": frozen_files.get("validate_preflight.py"),
    }
    for label, digest in source_hashes.items():
        _sha(digest, aid, f"target branch {label} hash")
    record_hashes = {
        "freeze": digests[("A01_FREEZE_AND_SOURCE_PACKET", 1)],
        "preflight_result": digests[("A02_NONPHYSICAL_PREFLIGHT", 1)],
        "independent_audit": digests[("A03_PREPAYLOAD_AUDIT", 1)],
        "cached_L10_gate": digests[("A15_L10_STAGE_GATE", 1)],
        "L12_cache_manifest": digests[("A05_FIVE_CACHE_SET", 5)],
    }
    branch: dict[str, object] = {"role": "target_v012"}
    for label in A17_SOURCE_LABELS:
        path = (
            f"/synthetic/target_v012/{label}"
            if fixture_mode else str(
                ROOT / TARGET_BRANCH_CANONICAL_RELATIVE_PATHS[label]
            )
        )
        digest = (
            source_hashes[label]
            if label in source_hashes else record_hashes[label]
        )
        binding: dict[str, object] = {"path": path, "sha256": digest}
        if label in TARGET_BRANCH_RECORD_IDENTITIES:
            schema, identity_field, identity_value = (
                TARGET_BRANCH_RECORD_IDENTITIES[label]
            )
            binding.update({
                "schema": schema,
                "identity_field": identity_field,
                "identity_value": identity_value,
            })
        branch[label] = binding
    return branch


def _validate_upstream_authority_chain(
    records: dict[tuple[str, int], dict[str, object]],
    digests: dict[tuple[str, int], str],
    metadata: dict[tuple[str, int], dict[str, str]],
    aid: str, fixture_mode: bool,
) -> None:
    """Reconstruct the native A01--A18 predecessor bindings from bytes."""
    digest = lambda artifact, instance=1: digests[(artifact, instance)]
    record = lambda artifact, instance=1: records[(artifact, instance)]
    a01, a02, a03, a04 = (digest(f"A0{index}_{name}") for index, name in (
        (1, "FREEZE_AND_SOURCE_PACKET"),
        (2, "NONPHYSICAL_PREFLIGHT"),
        (3, "PREPAYLOAD_AUDIT"),
        (4, "UNIVERSAL_CUSTODY_GATE"),
    ))
    frozen_files = _keys(
        record("A01_FREEZE_AND_SOURCE_PACKET").get("files"),
        A03_AUDITED_FILES, aid, "A01 frozen source files",
    )
    for name, source_sha256 in frozen_files.items():
        _sha(source_sha256, aid, f"A01 frozen source {name}")

    preaudit = record("A03_PREPAYLOAD_AUDIT")
    if (
        preaudit.get("audited_freeze_sha256") != a01
        or preaudit.get("preflight_result_sha256") != a02
    ):
        _fail(aid, "A01/A02->A03 authority mismatch")
    custody = record("A04_UNIVERSAL_CUSTODY_GATE")
    if (
        custody.get("freeze_sha256") != a01
        or custody.get("preflight_result_sha256") != a02
        or custody.get("independent_hostile_audit", {}).get("sha256") != a03
    ):
        _fail(aid, "A01-A03->A04 authority mismatch")

    lengths = (4, 6, 8, 10, 12)
    cache_hashes = {
        str(length): digest("A05_FIVE_CACHE_SET", instance)
        for instance, length in enumerate(lengths, start=1)
    }
    for instance, length in enumerate(lengths, start=1):
        cache = record("A05_FIVE_CACHE_SET", instance)
        if (
            cache.get("L") != length
            or cache.get("freeze_sha256") != a01
            or cache.get("preflight_result_sha256") != a02
            or cache.get("independent_hostile_audit_sha256") != a03
            or cache.get("dual_obstruction_gate_sha256") != a04
        ):
            _fail(aid, "A01-A04->A05 cache authority mismatch")

    postbuild = record("A06_POSTBUILD_AUDIT")
    if (
        postbuild.get("prebuild_hostile_audit_sha256") != a03
        or postbuild.get("dual_obstruction_and_compatibility_gate_sha256") != a04
        or postbuild.get("manifest_sha256_by_L") != cache_hashes
    ):
        _fail(aid, "A03-A05->A06 authority mismatch")
    a06 = digest("A06_POSTBUILD_AUDIT")
    physical = record("A07_BASE_PHYSICAL_GATE")
    if (
        physical.get("freeze_sha256") != a01
        or physical.get("preflight_result_sha256") != a02
        or physical.get("independent_hostile_audit_sha256") != a03
        or physical.get("dual_obstruction_gate_sha256") != a04
        or physical.get("cache_manifest_sha256_by_L") != cache_hashes
        or physical.get("postbuild_payload_audit", {}).get("sha256") != a06
    ):
        _fail(aid, "A01-A06->A07 authority mismatch")
    a07 = digest("A07_BASE_PHYSICAL_GATE")
    physical_audit = record("A08_PHYSICAL_GATE_AUDIT")
    if (
        physical_audit.get("physical_execution_gate_sha256") != a07
        or physical_audit.get("postbuild_payload_audit_sha256") != a06
    ):
        _fail(aid, "A06/A07->A08 authority mismatch")
    a08 = digest("A08_PHYSICAL_GATE_AUDIT")
    controls_authorization = record("A09_CONTROL_AUTHORIZATION")
    if (
        controls_authorization.get("physical_execution_gate", {}).get("sha256") != a07
        or controls_authorization.get("physical_gate_hostile_audit", {}).get("sha256") != a08
        or controls_authorization.get("postbuild_payload_audit", {}).get("sha256") != a06
    ):
        _fail(aid, "A06-A08->A09 authority mismatch")
    a09 = digest("A09_CONTROL_AUTHORIZATION")

    control_hashes: dict[str, str] = {}
    for instance, length in enumerate((4, 6, 8), start=1):
        control = record("A10_CONTROL_HISTORIES", instance)
        if (
            control.get("L") != length
            or control.get("cache_manifest_sha256") != cache_hashes[str(length)]
            or control.get("physical_execution_gate_sha256") != a07
            or control.get("execution_authorization_sha256") != a09
        ):
            _fail(aid, "A05/A07/A09->A10 authority mismatch")
        control_hashes[str(length)] = digest("A10_CONTROL_HISTORIES", instance)
    control_gate = record("A11_CONTROL_STAGE_GATE")
    if (
        control_gate.get("physical_execution_gate_sha256") != a07
        or control_gate.get("cache_manifest_sha256_by_L")
        != {key: cache_hashes[key] for key in ("4", "6", "8")}
        or {
            str(item.get("L")): item.get("sha256")
            for item in control_gate.get("histories", [])
        } != control_hashes
    ):
        _fail(aid, "A05/A07/A10->A11 authority mismatch")
    source_projection = {
        "consumer_sha256": frozen_files["consume_target_cache.py"],
        "builder_sha256": frozen_files["build_target_cache.py"],
        "method_sha256": frozen_files["METHOD.md"],
        "preflight_sha256": frozen_files["validate_preflight.py"],
        "production_obligation_validators_sha256": frozen_files[
            "production_obligation_validators.py"
        ],
        "freeze_sha256": a01,
    }
    if any(
        control_gate.get(key) != value
        for key, value in source_projection.items()
        if key in control_gate
    ) or any(
        control_gate.get(key) != physical.get(key)
        for key in UPSTREAM_INHERITED_PHYSICAL_FIELDS
    ):
        _fail(aid, "A01/A02/A07->A11 source/provenance mismatch")
    a11 = digest("A11_CONTROL_STAGE_GATE")
    control_audit = record("A12_CONTROL_STAGE_AUDIT")
    if (
        control_audit.get("stage_gate_sha256") != a11
        or control_audit.get("history_sha256_by_L") != control_hashes
    ):
        _fail(aid, "A10/A11->A12 authority mismatch")
    a12 = digest("A12_CONTROL_STAGE_AUDIT")
    l10_authorization = record("A13_L10_AUTHORIZATION")
    if (
        l10_authorization.get("physical_execution_gate_sha256") != a07
        or l10_authorization.get("cached_control_l4_l8_gate_sha256") != a11
        or l10_authorization.get("cached_control_l4_l8_gate_audit_sha256") != a12
        or l10_authorization.get("l10_cache_manifest_sha256") != cache_hashes["10"]
    ):
        _fail(aid, "A05/A07/A11/A12->A13 authority mismatch")
    if any(
        l10_authorization.get(key) != value
        for key, value in source_projection.items()
        if key in l10_authorization
    ):
        _fail(aid, "A01->A13 source mismatch")
    a13 = digest("A13_L10_AUTHORIZATION")
    l10_history = record("A14_L10_HISTORY")
    if (
        l10_history.get("cache_manifest_sha256") != cache_hashes["10"]
        or l10_history.get("physical_execution_gate_sha256") != a07
        or l10_history.get("cached_control_l4_l8_gate_sha256") != a11
        or l10_history.get("cached_control_l4_l8_gate_audit_sha256") != a12
        or l10_history.get("execution_authorization_sha256") != a13
        or l10_history.get("l10_execution_authorization_gate_sha256") != a13
    ):
        _fail(aid, "A05/A07/A11-A13->A14 authority mismatch")
    if any(
        l10_history.get(key) != value
        for key, value in source_projection.items()
        if key in l10_history
    ) or any(
        l10_history.get(key) != physical.get(key)
        for key in UPSTREAM_INHERITED_PHYSICAL_FIELDS
    ) or l10_history.get("dual_obstruction_gate_sha256") != a04:
        _fail(aid, "A01/A04/A07->A14 source/provenance mismatch")
    a14 = digest("A14_L10_HISTORY")
    l10_gate = record("A15_L10_STAGE_GATE")
    if (
        l10_gate.get("cache_manifest_sha256_by_L") != {"10": cache_hashes["10"]}
        or l10_gate.get("cached_control_l4_l8_gate_sha256") != a11
        or l10_gate.get("l10_execution_authorization_gate_sha256") != a13
        or l10_gate.get("physical_execution_gate_sha256") != a07
        or l10_gate.get("histories", [{}])[0].get("sha256") != a14
    ):
        _fail(aid, "A05/A07/A11/A13/A14->A15 authority mismatch")
    if any(
        l10_gate.get(key) != value
        for key, value in source_projection.items()
        if key in l10_gate
    ) or any(
        l10_gate.get(key) != physical.get(key)
        for key in UPSTREAM_INHERITED_PHYSICAL_FIELDS
    ):
        _fail(aid, "A01/A02/A07->A15 source/provenance mismatch")
    a15 = digest("A15_L10_STAGE_GATE")
    l10_audit = record("A16_L10_STAGE_AUDIT")
    if (
        l10_audit.get("stage_gate_sha256") != a15
        or l10_audit.get("history_sha256_by_L") != {"10": a14}
        or l10_audit.get("l10_execution_authorization_gate_sha256") != a13
    ):
        _fail(aid, "A13-A15->A16 authority mismatch")
    hostile_eligibility = record("A17_HOSTILE_L12_ELIGIBILITY")
    hostile_l10 = hostile_eligibility.get("cached_L10_gate", {}).get("sha256")
    if type(hostile_l10) is not str:
        _fail(aid, "A17 hostile L10 authority absent")
    cross_gate = record("A18_L10_CROSS_GATE")
    target_projection = cross_gate.get("target")
    hostile_projection = cross_gate.get("hostile")
    if type(target_projection) is not dict or set(target_projection) != {
        "branch", "cached_L10_gate_sha256",
        "cached_L10_gate_audit_sha256", "history_sha256",
    }:
        _fail(aid, "A18 target projection census mismatch")
    if type(hostile_projection) is not dict or set(hostile_projection) != {
        "branch", "cached_L10_gate_sha256",
        "l10_execution_authorization_gate_sha256",
        "independent_prepayload_audit_sha256", "history_sha256",
    }:
        _fail(aid, "A18 hostile projection census mismatch")
    expected_target_branch = _target_branch_from_authority(
        records, digests, fixture_mode, aid,
    )
    hostile_metadata = metadata[("A17_HOSTILE_L12_ELIGIBILITY", 1)]
    if (
        target_projection.get("branch") != expected_target_branch
        or target_projection.get("cached_L10_gate_sha256") != a15
        or target_projection.get("cached_L10_gate_audit_sha256")
        != digest("A16_L10_STAGE_AUDIT")
        or target_projection.get("history_sha256") != a14
        or hostile_projection.get("branch") != hostile_eligibility
        or hostile_projection.get("cached_L10_gate_sha256") != hostile_l10
        or hostile_projection.get("independent_prepayload_audit_sha256")
        != hostile_eligibility.get("independent_audit", {}).get("sha256")
        or hostile_projection.get("l10_execution_authorization_gate_sha256")
        != hostile_metadata.get("l10_execution_authorization_sha256")
        or hostile_projection.get("history_sha256")
        != hostile_metadata.get("history_sha256")
    ):
        _fail(aid, "A14/A17->A18 authority mismatch")


def _validate_final_l12_audit_with_open_inputs(
    record: object, *, fixture_mode: bool,
    authority_guard: list[_StableInput],
) -> dict[str, object]:
    aid = "A26_FINAL_L12_AUDIT"
    record = _strict_json(record, aid)
    row = _keys(record, {
        "schema", "classification", "auditor_role", "authority_bindings",
        "comparison_policy", "history_projection", "terminal_comparisons",
        "checks", "checks_total",
        "checks_passed", "failures", "authority_records_authenticated",
        "custody",
        "claim_boundary",
    }, aid, "final audit")
    if row["schema"] != "TARGET_V012_HOSTILE_V004R4_FINAL_L12_AUDIT_V001" or row["classification"] != "PASS_FINITE_L12_TARGET_HOSTILE_ACCUMULATION" or row["auditor_role"] != "INDEPENDENT_FINAL_L12_AUDITOR":
        _fail(aid, "final audit identity mismatch")
    (
        authority, authority_hashes, authority_inputs, authority_metadata,
    ) = _validate_authority_bundle(row["authority_bindings"], aid, fixture_mode)
    authority_guard.extend(authority_inputs)
    _validate_upstream_authority_chain(
        authority, authority_hashes, authority_metadata, aid, fixture_mode,
    )
    _validate_terminal_authority_chain(authority, authority_hashes, aid)
    telemetry = authority[("A23_POSTRUN_TELEMETRY", 1)]
    target = authority[("A24_TARGET_L12_HISTORY", 1)]
    hostile = authority[("A25_HOSTILE_L12_HISTORY", 1)]
    telemetry_sha = authority_hashes[("A23_POSTRUN_TELEMETRY", 1)]
    target_sha = authority_hashes[("A24_TARGET_L12_HISTORY", 1)]
    hostile_sha = authority_hashes[("A25_HOSTILE_L12_HISTORY", 1)]
    if telemetry["output_sha256_by_role"]["target_v012"] != target_sha or telemetry["output_sha256_by_role"]["hostile_v004r4"] != hostile_sha:
        _fail(aid, "telemetry/history output binding mismatch")
    shared_keys = {
        "target_hostile_l10_cross_gate_sha256",
        "shared_aggregate_schedule_gate_sha256",
        "shared_aggregate_schedule_gate_audit_sha256",
        "hostile_l12_execution_gate_sha256",
        "dual_l12_launch_handshake_sha256",
        "dual_l12_worker_release_sha256",
    }
    for key in shared_keys:
        if target[key] != hostile[key]:
            _fail(aid, f"shared authorization lineage mismatch: {key}")
    lineage_to_telemetry = {
        "shared_aggregate_schedule_gate_sha256": "shared_gate_sha256",
        "shared_aggregate_schedule_gate_audit_sha256": "schedule_audit_sha256",
        "dual_l12_launch_handshake_sha256": "dual_launch_handshake_sha256",
        "dual_l12_worker_release_sha256": "worker_release_sha256",
    }
    for history_key, telemetry_key in lineage_to_telemetry.items():
        if target[history_key] != telemetry[telemetry_key]:
            _fail(aid, f"telemetry authorization binding mismatch: {history_key}")
    if target["target_l12_execution_gate_sha256"] != telemetry["authorization_sha256_by_role"]["target_v012"] or hostile["hostile_l12_execution_gate_sha256"] != telemetry["authorization_sha256_by_role"]["hostile_v004r4"]:
        _fail(aid, "one-way authorization binding mismatch")
    observed_row_error, observed_comparison_error = _history_projection_errors(
        target, hostile, aid,
    )
    history_projection = _keys(row["history_projection"], {
        "mapping", "row_linf_abs_error", "comparison_linf_abs_error",
        "tolerance",
    }, aid, "history projection")
    if (
        history_projection["mapping"]
        != "NATIVE_HOSTILE_V004R3_TO_TARGET_PHYSICAL_FIELDS_V001"
        or _float(
            history_projection["row_linf_abs_error"], aid,
            "history row projection error",
        ) != observed_row_error
        or _float(
            history_projection["comparison_linf_abs_error"], aid,
            "history comparison projection error",
        ) != observed_comparison_error
        or _float(
            history_projection["tolerance"], aid,
            "history projection tolerance",
        ) != TOLERANCE
        or observed_row_error > TOLERANCE
        or observed_comparison_error > TOLERANCE
    ):
        _fail(aid, "native target/hostile history projection mismatch")
    policy = _keys(row["comparison_policy"], {
        "target_basis", "hostile_basis", "projection",
        "permutation_serialization", "tolerance", "nonfinite_refusal",
    }, aid, "comparison policy")
    if policy != {
        "target_basis": "TARGET_FIXED_WORDS_LEXICOGRAPHIC_COMBINATION_ORDER",
        "hostile_basis": "REVERSED_COMBINATION__FULL_MASK",
        "projection": "TARGET_RANK_TO_HOSTILE_RANK_ON_LINEAGE_AND_CARRIER_AXES",
        "permutation_serialization": "V001_TAGGED_LE_U64_TARGET_RANK_TO_HOSTILE_RANK",
        "tolerance": TOLERANCE,
        "nonfinite_refusal": True,
    } or any(type(policy[key]) is not type(expected) for key, expected in {
        "target_basis": "", "hostile_basis": "", "projection": "",
        "permutation_serialization": "", "tolerance": 0.0,
        "nonfinite_refusal": True,
    }.items()):
        _fail(aid, "comparison policy/type mismatch")
    comparisons = row["terminal_comparisons"]
    if type(comparisons) is not list or len(comparisons) != 12:
        _fail(aid, "terminal comparison census mismatch")
    target_shards = target["terminal_shards"]
    hostile_shards = hostile["terminal_shards"]
    for q, item in enumerate(comparisons):
        comparison = _keys(item, {
            "q", "target_sha256", "hostile_sha256",
            "lineage_target_to_hostile_permutation_sha256",
            "carrier_target_to_hostile_permutation_sha256", "linf_abs_error",
        }, aid, f"terminal comparison q={q}")
        if _integer(comparison["q"], aid, "comparison q") != q:
            _fail(aid, "terminal comparison order mismatch")
        target_digest = _sha(comparison["target_sha256"], aid, "target shard hash")
        hostile_digest = _sha(comparison["hostile_sha256"], aid, "hostile shard hash")
        if target_digest != target_shards[q]["sha256"] or hostile_digest != hostile_shards[q]["sha256"] or target_digest == hostile_digest:
            _fail(aid, "terminal target/hostile shard binding or distinctness mismatch")
        if _sha(comparison["lineage_target_to_hostile_permutation_sha256"], aid, "lineage permutation") != basis_permutation_sha256(11, q) or _sha(comparison["carrier_target_to_hostile_permutation_sha256"], aid, "carrier permutation") != basis_permutation_sha256(24, q):
            _fail(aid, "basis permutation hash mismatch")
        reported_error = _float(comparison["linf_abs_error"], aid, "terminal Linf error")
        if not fixture_mode:
            observed_error = _compare_terminal_files(target_shards[q], hostile_shards[q], q)
            if abs(observed_error - reported_error) > 1.0e-15:
                _fail(aid, "reported/observed terminal Linf mismatch")
        if reported_error > TOLERANCE:
            _fail(aid, "terminal comparison tolerance exceeded")
    expected_checks = {
        "postrun_telemetry": 1,
        "complete_l12_histories": 2,
        "terminal_shard_custody": 24,
        "basis_permutation_projections": 24,
        "terminal_numerical_comparisons": 12,
        "native_history_field_projections": 13,
        "transitive_authorization_bindings": sum(AUTHORITY_INSTANCE_CENSUS.values()),
        "independent_auditor_isolation": 1,
    }
    checks = _keys(row["checks"], set(expected_checks), aid, "checks")
    if checks != expected_checks or any(type(value) is not int or value <= 0 for value in checks.values()):
        _fail(aid, "check census mismatch")
    total = sum(expected_checks.values())
    if _integer(row["checks_total"], aid, "checks total", 1) != total or _integer(row["checks_passed"], aid, "checks passed", 1) != total or row["failures"] != []:
        _fail(aid, "check total/failure reconstruction mismatch")
    if _integer(
        row["authority_records_authenticated"], aid,
        "authority records authenticated", 1,
    ) != sum(AUTHORITY_INSTANCE_CENSUS.values()):
        _fail(aid, "authority record authentication census mismatch")
    _custody(row["custody"], aid)
    if row["claim_boundary"] != "FINITE_L12_TARGET_HOSTILE_ACCUMULATION_ONLY__NO_SPECTRUM_Z1_CONTINUUM_EMERGENCE_OR_GRAVITY":
        _fail(aid, "claim boundary mismatch")
    del target_sha, hostile_sha
    return row


def _verify_close_authority_inputs(inputs: list[_StableInput]) -> None:
    first_error: BaseException | None = None
    for retained in inputs:
        try:
            retained.verify_and_close()
        except BaseException as error:
            if first_error is None:
                first_error = error
    if first_error is not None:
        raise first_error


def validate_final_l12_audit(
    record: object, *, fixture_mode: bool = False,
) -> dict[str, object]:
    authority_guard: list[_StableInput] = []
    try:
        return _validate_final_l12_audit_with_open_inputs(
            record, fixture_mode=fixture_mode,
            authority_guard=authority_guard,
        )
    finally:
        _verify_close_authority_inputs(authority_guard)


@lru_cache(maxsize=1)
def _matrix_assignments() -> tuple[tuple[str, str, str], ...]:
    try:
        raw = OBLIGATION_MATRIX_PATH.read_bytes()
    except OSError as error:
        raise Refusal("A27_MUTATION_LEDGER: obligation matrix absent") from error
    if hashlib.sha256(raw).hexdigest() != OBLIGATION_MATRIX_SHA256:
        _fail("A27_MUTATION_LEDGER", "obligation matrix hash mismatch")
    matrix = _strict_json(raw, "A27_MUTATION_LEDGER")
    if type(matrix) is not dict or type(matrix.get("artifacts")) is not list:
        _fail("A27_MUTATION_LEDGER", "obligation matrix artifact census malformed")
    assignments: list[tuple[str, str, str]] = []
    artifact_ids: set[str] = set()
    fixture_ids: set[str] = set()
    assigned_classes: set[str] = set()
    for artifact in matrix["artifacts"]:
        if type(artifact) is not dict:
            _fail("A27_MUTATION_LEDGER", "obligation matrix artifact malformed")
        artifact_id = artifact.get("id")
        fixture = artifact.get("positive_fixture")
        variants = artifact.get("positive_fixture_variants", [])
        fixture_by_class = artifact.get("mutation_fixture_by_class")
        classes = artifact.get("mutation_classes")
        if (
            type(artifact_id) is not str or artifact_id in artifact_ids
            or type(fixture) is not dict or set(fixture) != {"id", "form", "acceptance"}
            or type(fixture.get("id")) is not str or fixture["id"] in fixture_ids
            or type(variants) is not list
            or any(
                type(item) is not dict
                or set(item) != {"id", "form", "acceptance"}
                or type(item.get("id")) is not str
                for item in variants
            )
            or type(classes) is not list or not classes
            or any(type(item) is not str or item not in MUTATION_REFUSAL for item in classes)
            or len(classes) != len(set(classes))
        ):
            _fail("A27_MUTATION_LEDGER", "obligation matrix assignment malformed")
        artifact_ids.add(artifact_id)
        declared_fixture_ids = [fixture["id"], *(
            item["id"] for item in variants
        )]
        if (
            len(declared_fixture_ids) != len(set(declared_fixture_ids))
            or any(item in fixture_ids for item in declared_fixture_ids)
            or (
                fixture_by_class is not None
                and (
                    type(fixture_by_class) is not dict
                    or set(fixture_by_class) != set(classes)
                    or any(
                        type(key) is not str
                        or type(value) is not str
                        or value not in declared_fixture_ids
                        for key, value in fixture_by_class.items()
                    )
                )
            )
            or (variants and fixture_by_class is None)
        ):
            _fail("A27_MUTATION_LEDGER", "obligation fixture variant mapping malformed")
        fixture_ids.update(declared_fixture_ids)
        for mutation_class in classes:
            fixture_id = (
                fixture["id"] if fixture_by_class is None
                else fixture_by_class[mutation_class]
            )
            assignments.append((artifact_id, fixture_id, mutation_class))
            assigned_classes.add(mutation_class)
    if (
        artifact_ids != {
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
            "A22_TARGET_L12_AUTHORIZATION", *ARTIFACT_IDS,
        }
        or len(assignments) != 477
        or assigned_classes != set(MUTATION_REFUSAL)
    ):
        _fail("A27_MUTATION_LEDGER", "obligation matrix coverage mismatch")
    return tuple(assignments)


def _ledger_expected_hook(
    artifact_id: str, fixture_id: str, mutation_class: str,
) -> str:
    custody_hook = {
        "M12_SYMLINK_OR_WRITABLE": "validate_preflight.read_strict_immutable_json",
        "M13_DESCRIPTOR_TOCTOU": "validate_preflight.validate_held_descriptor_identity",
        "M28_PREMATURE_ARTIFACT": "validate_preflight.require_artifacts_absent",
    }.get(mutation_class)
    if custody_hook is not None:
        return custody_hook
    if artifact_id == "A22_TARGET_L12_AUTHORIZATION":
        method = {
            "PF_A22_TARGET_AUTH": "admit_authorization",
            "PF_A22_HOSTILE_AUTH": "admit_authorization",
            "PF_A22_READY": "commit_handshake",
            "PF_A22_HANDSHAKE": "commit_handshake",
            "PF_A22_RELEASE": "release_workers",
            "PF_A22_COMMAND": "admit_release_ack",
            "PF_A22_ACK": "admit_release_ack",
            "PF_A22_COMPLETION": "admit_worker_completion",
        }.get(fixture_id)
        if method is None:
            _fail("A27_MUTATION_LEDGER", "unknown A22 stateful fixture sink")
        return f"dual_launch_coordinator.DualLaunchCoordinator.{method}"
    return PRODUCTION_FIXTURE_HOOK


def _ledger_expected_validator(
    artifact_id: str, fixture_id: str, mutation_class: str,
) -> str:
    hook = _ledger_expected_hook(artifact_id, fixture_id, mutation_class)
    if hook != PRODUCTION_FIXTURE_HOOK:
        return hook
    if artifact_id in ARTIFACT_IDS:
        return {
            "A23_POSTRUN_TELEMETRY": "independent_final_auditor.validate_postrun_telemetry",
            "A24_TARGET_L12_HISTORY": "independent_final_auditor.validate_target_l12_history",
            "A25_HOSTILE_L12_HISTORY": "independent_final_auditor.validate_hostile_l12_history",
            "A26_FINAL_L12_AUDIT": "independent_final_auditor.validate_final_l12_audit",
            "A27_MUTATION_LEDGER": "independent_final_auditor.validate_mutation_ledger",
        }[artifact_id]
    return "production_obligation_validators.validate_record"


def _ledger_expected_refusal(
    artifact_id: str, fixture_id: str, mutation_class: str,
) -> str:
    if artifact_id == "A22_TARGET_L12_AUTHORIZATION":
        native = {
            "M06_BOOL_FOR_INT": "process_id must be an exact integer >= 1",
            "M07_FLOAT_INT_ALIAS": "release command process_id must be an exact integer >= 1",
            "M10_IDENTITY_OR_CLAIM": "worker release ACK schema mismatch",
            "M11_HASH_OR_PATH": "process start token must be a lowercase SHA-256",
            "M17_PROVENANCE_DROP_SWAP": "worker READY hash reconstruction mismatch",
            "M19_STAGE_BYPASS": "handshake authorizations exact key census mismatch",
            "M23_HANDSHAKE_TELEMETRY": "worker release ACK digest mismatch",
            "M24_UNLOCK_AUDIT_BINDING": "release token mismatch",
            "M30_COMPLETION_BOOL_PROCESS_ID": "worker completion process_id must be an exact integer >= 1",
            "M31_COMPLETION_FLOAT_PROCESS_ID": "worker completion process_id must be an exact integer >= 1",
            "M32_COMPLETION_SCHEMA": "worker completion schema mismatch",
            "M33_COMPLETION_OUTPUT_HASH": "worker completion output hash must be a lowercase SHA-256",
            "M34_COMPLETION_WORKER_IDENTITY": "worker completion identity mismatch",
            "M35_COMPLETION_STAGE_BYPASS": "worker completion requires both release ACKs",
            "M36_COMPLETION_EPOCH_WINDOW": "worker completion outside execution wall window",
        }.get(mutation_class)
        if native is not None:
            return native
    return FINAL_NATIVE_MUTATION_REFUSAL.get(
        (artifact_id, mutation_class), MUTATION_REFUSAL[mutation_class],
    )


def validate_mutation_ledger(record: object, *, fixture_mode: bool = False) -> dict[str, object]:
    del fixture_mode
    aid = "A27_MUTATION_LEDGER"
    record = _strict_json(record, aid)
    row = _keys(record, {
        "schema", "classification", "audited_packet", "sealed_input_commit",
        "obligation_matrix_path", "obligation_matrix_sha256", "freeze_sha256",
        "source_sha256", "positive_fixture_sha256_by_id",
        "mutated_fixture_sha256_by_case_id", "validator_module",
        "production_hook", "positive_sink_call_count", "mutation_sink_call_count",
        "case_count", "checks_passed", "checks_total",
        "canonical_artifact_created", "cases", "claim_boundary",
    }, aid, "mutation ledger")
    if (
        row["schema"] != MUTATION_LEDGER_SCHEMA
        or row["classification"] != MUTATION_LEDGER_CLASSIFICATION
        or row["audited_packet"] != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        or row["sealed_input_commit"]
        != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or row["obligation_matrix_path"] != OBLIGATION_MATRIX_RELATIVE
        or row["obligation_matrix_sha256"] != OBLIGATION_MATRIX_SHA256
        or row["production_hook"] != PRODUCTION_FIXTURE_HOOK
    ):
        _fail(aid, "ledger identity mismatch")
    _sha(row["freeze_sha256"], aid, "freeze hash")
    source_hashes = _keys(
        row["source_sha256"], SOURCE_FILE_KEYS, aid, "source hashes",
    )
    for key, value in source_hashes.items():
        _sha(value, aid, f"source hash {key}")
    validator_module = _keys(
        row["validator_module"], {"path", "sha256"}, aid,
        "validator module",
    )
    if validator_module != {
        "path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/production_obligation_validators.py",
        "sha256": source_hashes["production_obligation_validators.py"],
    }:
        _fail(aid, "validator module/source binding mismatch")
    expected_pairs = _matrix_assignments()
    expected_fixture_ids = {fixture_id for _, fixture_id, _ in expected_pairs}
    fixture_hashes = _keys(
        row["positive_fixture_sha256_by_id"], expected_fixture_ids, aid,
        "positive fixture hashes",
    )
    positive_fixture_count = len(expected_fixture_ids)
    if len({_sha(value, aid, "positive fixture hash") for value in fixture_hashes.values()}) != positive_fixture_count:
        _fail(aid, "positive fixture digest alias")
    mutated_hashes = _keys(
        row["mutated_fixture_sha256_by_case_id"],
        {f"MCASE_{index:04d}" for index in range(1, 478)}, aid,
        "mutated fixture hashes",
    )
    if len({_sha(value, aid, "mutated fixture hash") for value in mutated_hashes.values()}) != 477:
        _fail(aid, "mutated fixture digest alias")
    cases = row["cases"]
    if type(cases) is not list or len(cases) != len(expected_pairs):
        _fail(aid, "ledger case census mismatch")
    for index, (case, expected_pair) in enumerate(zip(cases, expected_pairs), start=1):
        item = _keys(case, {
            "case_id", "artifact_id", "fixture_id", "mutation_class",
            "byte_mutation", "expected_refusal", "actual_refusal",
            "positive_fixture_sha256", "mutated_fixture_sha256",
            "mutation_evidence_sha256", "production_hook",
            "validator_function", "production_sink_calls",
            "canonical_artifact_created", "passed",
        }, aid, f"ledger case {index}")
        artifact_id, fixture_id, mutation = expected_pair
        case_id = f"MCASE_{index:04d}"
        expected_refusal = _ledger_expected_refusal(
            artifact_id, fixture_id, mutation,
        )
        if (
            item["case_id"] != case_id or item["artifact_id"] != artifact_id
            or item["fixture_id"] != fixture_id
            or item["mutation_class"] != mutation
            or type(item["byte_mutation"]) is not str or not item["byte_mutation"]
            or item["expected_refusal"] != expected_refusal
            or type(item["actual_refusal"]) is not str
            or not item["actual_refusal"]
            or expected_refusal not in item["actual_refusal"]
            or item["positive_fixture_sha256"] != fixture_hashes[fixture_id]
            or item["mutated_fixture_sha256"] != mutated_hashes[case_id]
            or item["production_hook"]
            != _ledger_expected_hook(artifact_id, fixture_id, mutation)
            or item["validator_function"]
            != _ledger_expected_validator(artifact_id, fixture_id, mutation)
            or _integer(item["production_sink_calls"], aid, "production sink calls", 1) != 1
        ):
            _fail(aid, f"ledger case {index} identity/order mismatch")
        _sha(item["mutation_evidence_sha256"], aid, "mutation evidence hash")
        if _boolean(item["canonical_artifact_created"], aid, "canonical artifact created") is not False or _boolean(item["passed"], aid, "case passed") is not True:
            _fail(aid, f"ledger case {index} verdict mismatch")
    total = len(expected_pairs)
    if (
        _integer(row["positive_sink_call_count"], aid, "positive sink count", 1)
        != positive_fixture_count
        or _integer(row["mutation_sink_call_count"], aid, "mutation sink count", 1) != total
        or _integer(row["case_count"], aid, "case count", 1) != total
        or _integer(row["checks_total"], aid, "checks total", 1) != total
        or _integer(row["checks_passed"], aid, "checks passed", 1) != total
        or _boolean(
            row["canonical_artifact_created"], aid,
            "canonical artifact created",
        ) is not False
    ):
        _fail(aid, "ledger total/failure mismatch")
    if row["claim_boundary"] != MUTATION_LEDGER_CLAIM:
        _fail(aid, "claim boundary mismatch")
    return row


VALIDATORS: Final[dict[str, Callable[..., dict[str, object]]]] = {
    "A23_POSTRUN_TELEMETRY": validate_postrun_telemetry,
    "A24_TARGET_L12_HISTORY": validate_target_l12_history,
    "A25_HOSTILE_L12_HISTORY": validate_hostile_l12_history,
    "A26_FINAL_L12_AUDIT": validate_final_l12_audit,
    "A27_MUTATION_LEDGER": validate_mutation_ledger,
}


def validate_artifact(artifact_id: object, record: object, *, fixture_mode: bool = False) -> dict[str, object]:
    if type(artifact_id) is not str or artifact_id not in VALIDATORS:
        raise Refusal("unknown A23-A27 artifact id")
    if type(fixture_mode) is not bool:
        _fail(artifact_id, "fixture_mode must be an exact boolean")
    return VALIDATORS[artifact_id](record, fixture_mode=fixture_mode)


def _fixture_custody() -> dict[str, object]:
    return {
        "immutable_ordinary_file": True,
        "descriptor_authenticated": True,
        "rehash_after_validation": True,
        "atomically_created_once": True,
        "canonical_artifact_created_by_fixture": False,
    }


def _telemetry_fixture(output_hashes: dict[str, str]) -> dict[str, object]:
    launch = {"target_v012": 2_000_000_010, "hostile_v004r4": 2_000_000_011}
    completion = {"target_v012": 2_000_000_130, "hostile_v004r4": 2_000_000_131}
    identities = {
        role: {
            "worker_id": f"fixture-{role}-worker",
            "process_id": 41001 + index,
            "process_start_token": _h(f"{role}-process-start"),
            "executable_path": _expected_executable(role, True),
            "executable_sha256": _h(f"{role}-executable"),
            "control_channel_id": _h(f"{role}-control-channel"),
            "nonce_commitment_sha256": _h(f"{role}-nonce-commitment"),
        }
        for index, role in enumerate(ROLES)
    }

    def sample(role: str, epoch: int, rss: int) -> dict[str, object]:
        return {
            "captured_epoch": epoch, "rss_bytes": rss,
            **{
                key: identities[role][key] for key in (
                    "process_id", "process_start_token", "executable_path",
                    "executable_sha256",
                )
            },
        }
    return {
        "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
        "classification": "COMPLETE_SHARED_L12_TELEMETRY",
        "shared_gate_sha256": _h("schedule"),
        "schedule_audit_sha256": _h("schedule-audit"),
        "dual_launch_handshake_sha256": _h("handshake"),
        "worker_release_sha256": _h("release"),
        "authorization_sha256_by_role": {
            "target_v012": _h("target-authorization"),
            "hostile_v004r4": _h("hostile-authorization"),
        },
        "worker_identity_by_role": identities,
        "release_command_sha256_by_role": {
            role: _h(f"{role}-release-command") for role in ROLES
        },
        "release_ack_sha256_by_role": {
            role: _h(f"{role}-release-ack") for role in ROLES
        },
        "completion_sha256_by_role": {
            role: _h(f"{role}-worker-completion") for role in ROLES
        },
        "launch_epoch_by_role": launch,
        "completion_epoch_by_role": completion,
        "wall_seconds_by_role": {role: float(completion[role] - launch[role]) for role in ROLES},
        "peak_rss_bytes_by_role": {"target_v012": 16_000_000_000, "hostile_v004r4": 16_100_000_000},
        "rss_peak_semantics": (
            "LAUNCHER_SAMPLED_CURRENT_RSS_AT_MOST_30_SECONDS__"
            "NOT_OS_HIGH_WATER"
        ),
        "peak_mapped_bytes_by_role": {
            "target_v012": TARGET_MAPPED_LIMIT,
            "hostile_v004r4": HOSTILE_MAPPED_LIMIT,
        },
        "mapped_peak_semantics": (
            "CONSERVATIVE_AUTHENTICATION_CACHE_CERTIFICATE__"
            "NOT_OS_VIRTUAL_MEMORY"
        ),
        "runtime_samples_by_role": {
            "target_v012": [
                sample("target_v012", launch["target_v012"], 15_000_000_000),
                sample("target_v012", launch["target_v012"] + 60, 16_000_000_000),
                sample("target_v012", completion["target_v012"], 15_500_000_000),
            ],
            "hostile_v004r4": [
                sample("hostile_v004r4", launch["hostile_v004r4"], 15_100_000_000),
                sample("hostile_v004r4", launch["hostile_v004r4"] + 60, 16_100_000_000),
                sample("hostile_v004r4", completion["hostile_v004r4"], 15_600_000_000),
            ],
        },
        "free_disk_bytes_samples": [
            {"captured_epoch": 2_000_000_010, "workspace_filesystem_device": 17, "free_bytes": DISK_MINIMUM},
            {"captured_epoch": 2_000_000_070, "workspace_filesystem_device": 17, "free_bytes": DISK_MINIMUM},
            {"captured_epoch": 2_000_000_130, "workspace_filesystem_device": 17, "free_bytes": DISK_MINIMUM},
            {"captured_epoch": 2_000_000_131, "workspace_filesystem_device": 17, "free_bytes": DISK_MINIMUM},
        ],
        "exit_code_by_role": {role: 0 for role in ROLES},
        "output_path_by_role": {role: _expected_path(role, "history", True) for role in ROLES},
        "output_sha256_by_role": output_hashes,
        "claim_boundary": "POSTRUN_RUNTIME_EVIDENCE_ONLY__NO_FINAL_L12_ADJUDICATION",
    }


def _solver_fixture(event: int, null: bool) -> dict[str, object]:
    zero = null and event == 1
    return {
        "converged": True,
        "batches": 1,
        "low_memory_batches": 0,
        "maximum_exp_difference": 0.0,
        "maximum_krylov_steps": 0 if zero else event,
        "maximum_live_bytes": 1_000_000 + event,
        "maximum_residual_indicator": 0.0,
        "maximum_subdivisions": 1,
        "quadrature_nodes": 24,
    }


def _target_hash_fixture() -> dict[str, str]:
    result = {key: _h(f"target:{key}") for key in TARGET_HASH_KEYS}
    shared = {
        "target_hostile_l10_cross_gate_sha256": _h("l10-cross"),
        "shared_aggregate_schedule_gate_sha256": _h("schedule"),
        "shared_aggregate_schedule_gate_audit_sha256": _h("schedule-audit"),
        "hostile_l12_execution_gate_sha256": _h("hostile-authorization"),
        "dual_l12_launch_handshake_sha256": _h("handshake"),
        "dual_l12_worker_release_sha256": _h("release"),
        "target_l12_execution_gate_sha256": _h("target-authorization"),
    }
    result.update(shared)
    result["execution_authorization_sha256"] = result["target_l12_execution_gate_sha256"]
    result["promotion_audit_sha256"] = result["shared_aggregate_schedule_gate_audit_sha256"]
    return result


def _hostile_hash_fixture() -> dict[str, str]:
    result = {key: _h(f"hostile:{key}") for key in HOSTILE_HASH_KEYS}
    result.update({
        "target_hostile_l10_cross_gate_sha256": _h("l10-cross"),
        "shared_aggregate_schedule_gate_sha256": _h("schedule"),
        "shared_aggregate_schedule_gate_audit_sha256": _h("schedule-audit"),
        "hostile_l12_execution_gate_sha256": _h("hostile-authorization"),
        "dual_l12_launch_handshake_sha256": _h("handshake"),
        "dual_l12_worker_release_sha256": _h("release"),
    })
    return result


def _history_row_fixture(event: int) -> dict[str, object]:
    row: dict[str, object] = {
        key: 0.0 for key in ROW_KEYS
        if key not in {"actual_solver", "null_solver", "cursor_vertex", "event", "sector_weights", "terminal_children_streamed"}
    }
    retained_before = 0.25 * (event - 1)
    retained_after = retained_before + 0.25
    row.update({
        "actual_solver": _solver_fixture(event, False),
        "null_solver": _solver_fixture(event, True),
        "cursor_vertex": event - 1,
        "event": event,
        "allow_probability": 0.5,
        "blocked_probability": 0.5,
        "W_n": 0.25,
        "expected_W_from_allow": 0.25,
        "connector_delta_l1": 1.0,
        "q_retained_before": retained_before,
        "q_retained_after_admission": retained_after,
        "q_retained_after_transport": retained_after,
        "q_genesis_before": 12.0 - retained_before,
        "q_genesis_after": 12.0 - retained_after,
        "bandwidth_after": 12.0 - retained_after,
        "lineage_sealed_after": retained_after,
        "sector_weights": [1.0] + [0.0] * 12,
        "terminal_children_streamed": event == 12,
    })
    return row


def _hostile_solver_fixture(event: int, actual: bool) -> dict[str, object]:
    solver: dict[str, object] = {
        "converged": True,
        "batches": 1,
        "maximum_degree": event,
        "maximum_endpoint_difference": 0.0,
        "maximum_tail_indicator_32": 0.0,
        "algorithm": "RECURRENCE_REPLAY_GL_GROUPS",
        "quadrature_group_max": 12,
        "allocation_vector_slots": 20,
        "maximum_allocation_estimate_bytes": 1_000_000 + event,
        "allocation_limit_bytes": 1_400_000_000,
        "quadrature_nodes": 28,
        "q_sharded": True,
    }
    if event == 12 and actual:
        solver.update({
            "terminal_children_streamed": True,
            "terminal_child0_entries": math.comb(35, 11),
            "terminal_child1_nonzero_admission_entries": math.comb(34, 11),
            "full_terminal_array_allocated": False,
        })
    return solver


def _hostile_history_row_fixture(event: int) -> dict[str, object]:
    index = event - 1
    row: dict[str, object] = {
        key: 0.0 for key in HOSTILE_ROW_KEYS
        if key not in {
            "event", "input_prefix", "input_prefix_dimension",
            "logical_output_prefix_dimension", "terminal_children_streamed",
            "sector_weights", "actual_solver", "null_solver",
        }
    }
    row.update({
        "event": event,
        "input_prefix": index,
        "input_prefix_dimension": math.comb(24 + index, index),
        "logical_output_prefix_dimension": math.comb(25 + index, index + 1),
        "terminal_children_streamed": event == 12,
        "allow_probability": 0.5,
        "blocked_probability": 0.5,
        "W_n": 0.25,
        "q_retained_after_transport": 0.25 * event,
        "q_genesis_after": 12.0 - 0.25 * event,
        "connector_delta_l1": 1.0,
        "sector_weights": [1.0] + [0.0] * 12,
        "actual_solver": _hostile_solver_fixture(event, True),
        "null_solver": _hostile_solver_fixture(event, False),
    })
    return row


def _hostile_history_fixture() -> dict[str, object]:
    rows = [_hostile_history_row_fixture(event) for event in range(1, 13)]
    comparison = {
        "resolved": True,
        "classification": "RESOLVED_PREFIX_HISTORY_CONTROL",
        "epsilon": 1.0e-11,
        "maximum_admission_accounting_residual": 0.0,
        "maximum_node_continuity_residual_l1": 0.0,
        "maximum_norm_error": 0.0,
        "maximum_number_drift": 0.0,
        "rough_sharp": {
            "maximum_disagreement": 0.0,
            "observable_linf": 0.0,
            "sector_weight_linf": 0.0,
        },
        "sector": {
            "density_interval": [0.0, 1.0 / 48.0],
            "discarded_mass": 0.0,
            "enclosed_mass": 1.0,
            "late_events": list(range(7, 13)),
            "q_lower": 0,
            "q_upper": 0,
        },
        "admission_acceptance": [0.5] * 12,
        "routed_acceptance": [0.5] * 12,
        "connector_ratio": [1.0] * 12,
    }
    result: dict[str, object] = {
        "schema": "HOSTILE_CACHED_PREFIX_HISTORY_V004R4",
        "L": 12,
        "events": 12,
        "dimension": math.comb(36, 12),
        "preterminal_dimension": math.comb(35, 11),
        "edges": 36,
        "representation": "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__AUTHENTICATED_HOSTILE_INDEX_CACHE",
        "lineage_authority": "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING",
        "coarse_method": deepcopy(HOSTILE_COARSE_METHOD),
        "fine_method": deepcopy(HOSTILE_FINE_METHOD),
        "rows": rows,
        "comparison": comparison,
        "terminal_shards": [
            {
                "q": q,
                "path": _expected_path(
                    "hostile_v004r4", "terminal", True, q,
                ),
                "shape": [math.comb(11, q), math.comb(24, q)],
                "bytes": math.comb(11, q) * math.comb(24, q) * 16,
                "sha256": _h(f"hostile-terminal-{q}"),
            }
            for q in range(12)
        ],
        "resource": {
            "peak_logical_state_plus_cache_bytes": 9_599_886_552,
            "scratch_limit_bytes": 21_474_836_480,
            "maximum_numerical_allocation_estimate_bytes": 1_000_012,
            "numerical_workspace_limit_bytes": 1_400_000_000,
            "authentication_peak_certificate_bytes": 252_944_080,
            "peak_rss_bytes": 16_100_000_000,
            "rss_limit_bytes": RSS_LIMIT,
            "wall_seconds_including_authentication": 120.0,
            "wall_limit_seconds": WALL_LIMIT,
            "passed": True,
        },
        "claim_boundary": "FINITE_CACHED_HOSTILE_V004R4_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
    }
    result.update(_hostile_hash_fixture())
    if set(result) != HOSTILE_HISTORY_KEYS:
        raise AssertionError("internal hostile history fixture key census mismatch")
    return result


def _history_fixture(role: str) -> dict[str, object]:
    if role == "hostile_v004r4":
        return _hostile_history_fixture()
    aid = "target" if role == "target_v012" else "hostile"
    comparison = {
        "admission_acceptance": [0.5] * 12,
        "classification": "RESOLVED_RELATIONAL_HISTORY_L",
        "coarse_fine": {
            "maximum_disagreement": 0.0,
            "observable_linf": 0.0,
            "sector_weight_linf": 0.0,
        },
        "connector_ratio": [1.0] * 12,
        "epsilon": 1.0e-11,
        "resolved": True,
        "routed_acceptance": [0.5] * 12,
        "sector": {
            "density_interval": [0.0, 1.0 / 48.0],
            "discarded_mass": 0.0,
            "enclosed_mass": 1.0,
            "late_events": [7, 8, 9, 10, 11, 12],
            "q_lower": 0,
            "q_upper": 0,
        },
    }
    resource = {
        "peak_live_state_bytes": 8_773_667_584,
        "cache_payload_bytes": 826_238_292 if role == "target_v012" else 826_221_912,
        "combined_with_reserve_bytes": 9_600_954_452 if role == "target_v012" else 9_600_935_128,
        "scratch_limit_bytes": 21_474_836_480,
        "maximum_numerical_workset_bytes": 1_000_012,
        "numerical_workset_limit_bytes": 1_000_000_000,
        "terminal_cache_peak_bytes": 234_782_536,
        "authentication_cache_peak_bytes": 252_944_080,
        "maximum_cache_window_bytes": 252_944_080,
        "mapped_cache_limit_bytes": 536_870_912,
        "peak_rss_bytes": 16_000_000_000 if role == "target_v012" else 16_100_000_000,
        "rss_limit_bytes": RSS_LIMIT,
        "wall_seconds": 120.0,
        "wall_limit_seconds": WALL_LIMIT,
        "passed": True,
    }
    result: dict[str, object] = {
        "schema": _history_schema(role),
        "L": 12,
        "events": 12,
        "dimension": math.comb(36, 12),
        "preterminal_dimension": math.comb(35, 11),
        "edges": 36,
        "representation": "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__AUTHENTICATED_INDEX_CACHE" if role == "target_v012" else "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__AUTHENTICATED_HOSTILE_INDEX_CACHE",
        "lineage_authority": "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING",
        "coarse_method": {"epsilon": 1.0e-8, "quadrature_nodes": 24},
        "fine_method": {"epsilon": 1.0e-11, "quadrature_nodes": 24},
        "rows": [_history_row_fixture(event) for event in range(1, 13)],
        "comparison": comparison,
        "terminal_shards": [
            {
                "q": q,
                "path": _expected_path(role, "terminal", True, q),
                "shape": [math.comb(11, q), math.comb(24, q)],
                "bytes": math.comb(11, q) * math.comb(24, q) * 16 + 128,
                "sha256": _h(f"{aid}-terminal-{q}"),
            }
            for q in range(12)
        ],
        "resource": resource,
        "claim_boundary": "FINITE_CACHED_TARGET_HISTORY_ONLY__NO_SPECTRUM_CONTINUUM_OR_GRAVITY" if role == "target_v012" else "FINITE_CACHED_HOSTILE_V004R4_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
    }
    result.update(_target_hash_fixture() if role == "target_v012" else _hostile_hash_fixture())
    if set(result) != (TARGET_HISTORY_KEYS if role == "target_v012" else HOSTILE_HISTORY_KEYS):
        raise AssertionError("internal native history fixture key census mismatch")
    return result


def _fixture_a17_material() -> tuple[
    dict[str, object], list[dict[str, object]],
    dict[str, dict[str, object]], dict[str, str],
]:
    authorization_sha = _h("A17-hostile-L10-authorization")
    history_sha = _h("A17-hostile-L10-history")
    primary_hashes = {
        label: _h(f"A17-source:{label}")
        for label in ("method", "builder", "consumer", "preflight")
    }
    frozen_files = {
        Path(A17_CANONICAL_RELATIVE_PATHS[label]).name: primary_hashes[label]
        for label in primary_hashes
    }
    source_records: dict[str, dict[str, object]] = {
        "freeze": {
            "schema": A17_RECORD_IDENTITIES["freeze"][0],
            "status": A17_RECORD_IDENTITIES["freeze"][2],
            "files": frozen_files,
            "cache_payload_created": False,
            "physical_history_executed": False,
        },
    }
    freeze_sha = record_sha256(source_records["freeze"])
    source_records["preflight_result"] = {
        "schema": A17_RECORD_IDENTITIES["preflight_result"][0],
        "classification": A17_RECORD_IDENTITIES["preflight_result"][2],
        "files": {
            "method_sha256": primary_hashes["method"],
            "builder_sha256": primary_hashes["builder"],
            "consumer_sha256": primary_hashes["consumer"],
            "preflight_sha256": primary_hashes["preflight"],
            "freeze_sha256": freeze_sha,
        },
        "failures": [],
    }
    preflight_sha = record_sha256(source_records["preflight_result"])
    source_records["independent_audit"] = {
        "schema": A17_RECORD_IDENTITIES["independent_audit"][0],
        "classification": A17_RECORD_IDENTITIES["independent_audit"][2],
        "audited_freeze_sha256": freeze_sha,
        "audited_files_sha256": frozen_files,
        "preflight_result_sha256": preflight_sha,
        "checks_total": 1,
        "checks_passed": 1,
        "failures": [],
        "payload_or_history_executed": False,
    }
    audit_sha = record_sha256(source_records["independent_audit"])
    source_records["cached_L10_gate"] = {
        "schema": A17_RECORD_IDENTITIES["cached_L10_gate"][0],
        "classification": A17_RECORD_IDENTITIES["cached_L10_gate"][2],
        "method_sha256": primary_hashes["method"],
        "builder_sha256": primary_hashes["builder"],
        "consumer_sha256": primary_hashes["consumer"],
        "freeze_sha256": freeze_sha,
        "preflight_result_sha256": preflight_sha,
        "independent_hostile_audit_sha256": audit_sha,
        "cache_manifest_sha256_by_L": {"10": _h("A17-L10-manifest")},
        "l10_execution_authorization": {
            "path": "/synthetic/a17/L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json",
            "sha256": authorization_sha,
            "schema": "HOSTILE_V004R4_L10_EXECUTION_AUTHORIZATION_GATE_V001",
            "identity_field": "classification",
            "identity_value": "AUTHORIZE_AUDITED_HOSTILE_V004R4_L10",
        },
        "histories": [{
            "L": 10,
            "path": "/synthetic/a17/V004R4_PHYSICAL_OUTPUTS/HISTORY_L10.json",
            "sha256": history_sha,
        }],
    }
    source_records["L12_cache_manifest"] = {
        "schema": A17_RECORD_IDENTITIES["L12_cache_manifest"][0],
        "status": A17_RECORD_IDENTITIES["L12_cache_manifest"][2],
        "L": 12,
        "method_sha256": primary_hashes["method"],
        "builder_sha256": primary_hashes["builder"],
        "consumer_sha256": primary_hashes["consumer"],
        "preflight_sha256": primary_hashes["preflight"],
        "freeze_sha256": freeze_sha,
        "preflight_result_sha256": preflight_sha,
        "independent_hostile_audit_sha256": audit_sha,
    }
    sources: list[dict[str, object]] = []
    branch: dict[str, object] = {"role": "hostile_v004r4"}
    for label in A17_SOURCE_LABELS:
        digest = (
            record_sha256(source_records[label])
            if label in source_records else primary_hashes[label]
        )
        path = (
            f"/synthetic/a17/{label}/"
            f"{Path(A17_CANONICAL_RELATIVE_PATHS[label]).name}"
        )
        sources.append({"label": label, "path": path, "sha256": digest})
        binding: dict[str, object] = {"path": path, "sha256": digest}
        if label in A17_RECORD_IDENTITIES:
            schema, identity_field, identity_value = (
                A17_RECORD_IDENTITIES[label]
            )
            binding.update({
                "schema": schema,
                "identity_field": identity_field,
                "identity_value": identity_value,
            })
        branch[label] = binding
    return branch, sources, source_records, {
        "l10_execution_authorization_sha256": authorization_sha,
        "history_sha256": history_sha,
    }


def _install_synthetic_upstream_fixture(
    fixture: Callable[[str, int], dict[str, object]],
) -> None:
    """Install a test-only fixture provider; live validators never call it."""
    if not callable(fixture):
        _fail("A26_FINAL_L12_AUDIT", "synthetic fixture provider malformed")
    global _SYNTHETIC_UPSTREAM_FIXTURE
    _SYNTHETIC_UPSTREAM_FIXTURE = fixture


def _synthetic_upstream_fixture() -> Callable[[str, int], dict[str, object]]:
    if _SYNTHETIC_UPSTREAM_FIXTURE is None:
        _fail("A26_FINAL_L12_AUDIT", "synthetic fixture provider not installed")
    return _SYNTHETIC_UPSTREAM_FIXTURE


def _upstream_fixture_records() -> dict[tuple[str, int], dict[str, object]]:
    synthetic_fixture = _synthetic_upstream_fixture()

    records: dict[tuple[str, int], dict[str, object]] = {}
    for artifact_id, count in AUTHORITY_INSTANCE_CENSUS.items():
        if artifact_id in ARTIFACT_IDS or artifact_id == "A22_TARGET_L12_AUTHORIZATION":
            continue
        for instance in range(1, count + 1):
            record = synthetic_fixture(artifact_id)
            if artifact_id == "A05_FIVE_CACHE_SET":
                record["L"] = (4, 6, 8, 10, 12)[instance - 1]
            elif artifact_id == "A10_CONTROL_HISTORIES":
                length = (4, 6, 8)[instance - 1]
                record.update({
                    "L": length,
                    "events": length,
                    "dimension": math.comb(3 * length, length),
                    "preterminal_dimension": math.comb(
                        3 * length - 1, length - 1,
                    ),
                    "edges": 3 * length,
                    "rows": record["rows"][:length],
                    "terminal_shards": record["terminal_shards"][:length],
                })
            records[(artifact_id, instance)] = record

    def item(artifact: str, instance: int = 1) -> dict[str, object]:
        return records[(artifact, instance)]

    def digest(artifact: str, instance: int = 1) -> str:
        return record_sha256(item(artifact, instance))

    a01 = digest("A01_FREEZE_AND_SOURCE_PACKET")
    a02 = digest("A02_NONPHYSICAL_PREFLIGHT")
    fixture_frozen_files = item("A01_FREEZE_AND_SOURCE_PACKET")["files"]
    fixture_source_projection = {
        "consumer_sha256": fixture_frozen_files["consume_target_cache.py"],
        "builder_sha256": fixture_frozen_files["build_target_cache.py"],
        "method_sha256": fixture_frozen_files["METHOD.md"],
        "preflight_sha256": fixture_frozen_files["validate_preflight.py"],
        "production_obligation_validators_sha256": fixture_frozen_files[
            "production_obligation_validators.py"
        ],
        "freeze_sha256": a01,
    }
    item("A03_PREPAYLOAD_AUDIT").update({
        "audited_freeze_sha256": a01,
        "preflight_result_sha256": a02,
    })
    a03 = digest("A03_PREPAYLOAD_AUDIT")
    item("A04_UNIVERSAL_CUSTODY_GATE").update({
        "freeze_sha256": a01,
        "preflight_result_sha256": a02,
    })
    item("A04_UNIVERSAL_CUSTODY_GATE")["independent_hostile_audit"][
        "sha256"
    ] = a03
    a04 = digest("A04_UNIVERSAL_CUSTODY_GATE")
    lengths = (4, 6, 8, 10, 12)
    for instance, length in enumerate(lengths, start=1):
        item("A05_FIVE_CACHE_SET", instance).update({
            "freeze_sha256": a01,
            "preflight_result_sha256": a02,
            "independent_hostile_audit_sha256": a03,
            "dual_obstruction_gate_sha256": a04,
        })
    cache_hashes = {
        str(length): digest("A05_FIVE_CACHE_SET", instance)
        for instance, length in enumerate(lengths, start=1)
    }
    item("A06_POSTBUILD_AUDIT").update({
        "prebuild_hostile_audit_sha256": a03,
        "dual_obstruction_and_compatibility_gate_sha256": a04,
        "manifest_sha256_by_L": cache_hashes,
    })
    a06 = digest("A06_POSTBUILD_AUDIT")
    item("A07_BASE_PHYSICAL_GATE").update({
        **{
            key: value for key, value in fixture_source_projection.items()
            if key in item("A07_BASE_PHYSICAL_GATE")
        },
        "freeze_sha256": a01,
        "preflight_result_sha256": a02,
        "independent_hostile_audit_sha256": a03,
        "dual_obstruction_gate_sha256": a04,
        "cache_manifest_sha256_by_L": cache_hashes,
    })
    for key in (
        "original_target_l12_gate_sha256",
        "preserved_workspace_custody_sha256",
        "preserved_workspace_cross_diagnostic_sha256",
        "runtime_compatibility_obstruction_sha256",
        "v006_hostile_audit_obstruction_sha256",
        "v007_runtime_compatibility_obstruction_sha256",
        "v008_postbuild_audit_binding_obstruction_sha256",
        "v009_hostile_audit_obstruction_sha256",
        "v010_hostile_audit_obstruction_sha256",
        "v010_audit_record_custody_correction_sha256",
        "v011_hostile_audit_obstruction_sha256", "target_v004_sha256",
    ):
        if key in item("A04_UNIVERSAL_CUSTODY_GATE"):
            item("A07_BASE_PHYSICAL_GATE")[key] = item(
                "A04_UNIVERSAL_CUSTODY_GATE"
            )[key]
    item("A07_BASE_PHYSICAL_GATE")["postbuild_payload_audit"]["sha256"] = a06
    a07 = digest("A07_BASE_PHYSICAL_GATE")
    item("A08_PHYSICAL_GATE_AUDIT").update({
        "physical_execution_gate_sha256": a07,
        "postbuild_payload_audit_sha256": a06,
    })
    a08 = digest("A08_PHYSICAL_GATE_AUDIT")
    a09_record = item("A09_CONTROL_AUTHORIZATION")
    a09_record["physical_execution_gate"]["sha256"] = a07
    a09_record["physical_gate_hostile_audit"]["sha256"] = a08
    a09_record["postbuild_payload_audit"]["sha256"] = a06
    a09 = digest("A09_CONTROL_AUTHORIZATION")
    control_hashes: dict[str, str] = {}
    for instance, length in enumerate((4, 6, 8), start=1):
        control = item("A10_CONTROL_HISTORIES", instance)
        control.update({
            "cache_manifest_sha256": cache_hashes[str(length)],
            "physical_execution_gate_sha256": a07,
            "execution_authorization_sha256": a09,
        })
        control_hashes[str(length)] = digest("A10_CONTROL_HISTORIES", instance)
    control_gate = item("A11_CONTROL_STAGE_GATE")
    control_gate.update({
        **{
            key: value for key, value in fixture_source_projection.items()
            if key in control_gate
        },
        "physical_execution_gate_sha256": a07,
        "cache_manifest_sha256_by_L": {
            key: cache_hashes[key] for key in ("4", "6", "8")
        },
    })
    for key in UPSTREAM_INHERITED_PHYSICAL_FIELDS:
        control_gate[key] = item("A07_BASE_PHYSICAL_GATE")[key]
    for history in control_gate["histories"]:
        history["sha256"] = control_hashes[str(history["L"])]
    a11 = digest("A11_CONTROL_STAGE_GATE")
    control_audit = item("A12_CONTROL_STAGE_AUDIT")
    control_audit.update({
        "stage_gate_sha256": a11,
        "history_sha256_by_L": control_hashes,
    })
    a12 = digest("A12_CONTROL_STAGE_AUDIT")
    l10_authorization = item("A13_L10_AUTHORIZATION")
    l10_authorization.update({
        **{
            key: value for key, value in fixture_source_projection.items()
            if key in l10_authorization
        },
        "physical_execution_gate_sha256": a07,
        "cached_control_l4_l8_gate_sha256": a11,
        "cached_control_l4_l8_gate_audit_sha256": a12,
        "l10_cache_manifest_sha256": cache_hashes["10"],
    })
    a13 = digest("A13_L10_AUTHORIZATION")
    l10_history = item("A14_L10_HISTORY")
    l10_history.update({
        **{
            key: value for key, value in fixture_source_projection.items()
            if key in l10_history
        },
        "cache_manifest_sha256": cache_hashes["10"],
        "physical_execution_gate_sha256": a07,
        "cached_control_l4_l8_gate_sha256": a11,
        "cached_control_l4_l8_gate_audit_sha256": a12,
        "execution_authorization_sha256": a13,
        "l10_execution_authorization_gate_sha256": a13,
        "dual_obstruction_gate_sha256": a04,
    })
    for key in UPSTREAM_INHERITED_PHYSICAL_FIELDS:
        l10_history[key] = item("A07_BASE_PHYSICAL_GATE")[key]
    a14 = digest("A14_L10_HISTORY")
    l10_gate = item("A15_L10_STAGE_GATE")
    l10_gate.update({
        **{
            key: value for key, value in fixture_source_projection.items()
            if key in l10_gate
        },
        "cache_manifest_sha256_by_L": {"10": cache_hashes["10"]},
        "cached_control_l4_l8_gate_sha256": a11,
        "l10_execution_authorization_gate_sha256": a13,
        "physical_execution_gate_sha256": a07,
    })
    for key in UPSTREAM_INHERITED_PHYSICAL_FIELDS:
        l10_gate[key] = item("A07_BASE_PHYSICAL_GATE")[key]
    l10_gate["histories"][0]["sha256"] = a14
    a15 = digest("A15_L10_STAGE_GATE")
    item("A16_L10_STAGE_AUDIT").update({
        "stage_gate_sha256": a15,
        "history_sha256_by_L": {"10": a14},
        "l10_execution_authorization_gate_sha256": a13,
    })
    hostile_branch, _sources, _source_records, hostile_metadata = (
        _fixture_a17_material()
    )
    records[("A17_HOSTILE_L12_ELIGIBILITY", 1)] = hostile_branch
    authority_hashes = {
        key: record_sha256(value) for key, value in records.items()
    }
    target_branch = _target_branch_from_authority(
        records, authority_hashes, True, "fixture",
    )
    hostile_l10 = hostile_branch["cached_L10_gate"]["sha256"]
    cross_gate = item("A18_L10_CROSS_GATE")
    cross_gate["target"] = {
        "branch": target_branch,
        "cached_L10_gate_sha256": a15,
        "cached_L10_gate_audit_sha256": digest("A16_L10_STAGE_AUDIT"),
        "history_sha256": a14,
    }
    cross_gate["hostile"] = {
        "branch": hostile_branch,
        "cached_L10_gate_sha256": hostile_l10,
        "l10_execution_authorization_gate_sha256": hostile_metadata[
            "l10_execution_authorization_sha256"
        ],
        "independent_prepayload_audit_sha256": hostile_branch[
            "independent_audit"
        ]["sha256"],
        "history_sha256": hostile_metadata["history_sha256"],
    }
    return records


def _terminal_authority_fixture_records(
    upstream: dict[tuple[str, int], dict[str, object]],
    target: dict[str, object], hostile: dict[str, object],
) -> tuple[dict[tuple[str, int], dict[str, object]], dict[str, object]]:
    synthetic_fixture = _synthetic_upstream_fixture()

    records = deepcopy(upstream)
    a18_sha = record_sha256(records[("A18_L10_CROSS_GATE", 1)])
    schedule = synthetic_fixture("A20_SHARED_SCHEDULE_GATE")
    schedule["l10_cross_gate_sha256"] = a18_sha
    schedule_sha = record_sha256(schedule)
    records[("A20_SHARED_SCHEDULE_GATE", 1)] = schedule
    schedule_audit = synthetic_fixture("A21_SHARED_SCHEDULE_AUDIT")
    schedule_audit["schedule_sha256"] = schedule_sha
    schedule_audit["l10_cross_gate_sha256"] = a18_sha
    schedule_audit_sha = record_sha256(schedule_audit)
    records[("A21_SHARED_SCHEDULE_AUDIT", 1)] = schedule_audit
    authorizations = {
        "target_v012": synthetic_fixture(
            "A22_TARGET_L12_AUTHORIZATION", 0,
        ),
        "hostile_v004r4": synthetic_fixture(
            "A22_TARGET_L12_AUTHORIZATION", 1,
        ),
    }
    for authorization in authorizations.values():
        authorization["schedule_sha256"] = schedule_sha
        authorization["schedule_audit_sha256"] = schedule_audit_sha
        authorization["l10_cross_gate_sha256"] = a18_sha
    auth_hash = {
        role: record_sha256(record)
        for role, record in authorizations.items()
    }
    records[("A22_TARGET_L12_AUTHORIZATION", 1)] = authorizations["target_v012"]
    records[("A22_TARGET_L12_AUTHORIZATION", 2)] = authorizations["hostile_v004r4"]
    nonces = {
        "target_v012": bytes(range(32)),
        "hostile_v004r4": bytes(range(32, 64)),
    }
    ready: dict[str, dict[str, object]] = {}
    for index, role in enumerate(ROLES):
        ready[role] = {
            "schema": "V012_L12_WORKER_READY_V001",
            "role": role,
            "worker_id": f"fixture-{role}-worker",
            "process_id": 41001 + index,
            "process_start_token": _h(f"{role}-process-start"),
            "executable_path": _expected_executable(role, True),
            "executable_sha256": _h(f"{role}-executable"),
            "workspace_path": f"/synthetic/{role}/workspace_L12",
            "output_path": _expected_path(role, "history", True),
            "control_channel_id": _h(f"{role}-control-channel"),
            "nonce_commitment_sha256": hashlib.sha256(
                b"V012_L12_WORKER_NONCE_V001\0" + nonces[role]
            ).hexdigest(),
            "ready_epoch": 2_000_000_000 + index,
            "blocked_on_release": True,
        }
        records[("A22_TARGET_L12_AUTHORIZATION", 3 + index)] = ready[role]
    ready_hash = {role: record_sha256(ready[role]) for role in ROLES}
    handshake = {
        "schema": "V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002",
        "classification": "BOTH_BLOCKED_WORKERS_READY_AFTER_BOTH_L12_AUTHORIZATIONS",
        "created_epoch": 2_000_000_002,
        "schedule_sha256": schedule_sha,
        "schedule_audit_sha256": schedule_audit_sha,
        "authorization_sha256_by_role": auth_hash,
        "memory_pressure": "NORMAL",
        "workers": ready,
        "ready_sha256_by_role": ready_hash,
        "observed_readiness_skew_seconds": 1,
        "launch_skew_seconds_max": 60,
        "telemetry": {
            "path": _expected_path("target_v012", "telemetry", True),
            "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
            "absent_before_release": True,
        },
        "claim_boundary": "IMMUTABLE_PRELAUNCH_HANDSHAKE_ONLY__NO_WORKER_RELEASE_OR_RESULT",
    }
    handshake_sha = record_sha256(handshake)
    records[("A22_TARGET_L12_AUTHORIZATION", 5)] = handshake
    release_epochs = {"target_v012": 2_000_000_010, "hostile_v004r4": 2_000_000_011}
    release = {
        "schema": "V012_DUAL_L12_WORKER_RELEASE_V002",
        "classification": "RELEASE_BOTH_AUTHORIZED_BLOCKED_WORKERS",
        "handshake_sha256": handshake_sha,
        "authorization_sha256_by_role": auth_hash,
        "release_epoch_by_role": release_epochs,
        "observed_launch_skew_seconds": 1,
        "release_by_role": {},
        "claim_boundary": "BARRIER_RELEASE_ONLY__NO_PHYSICAL_RESULT",
    }
    for role in ROLES:
        worker = ready[role]
        release["release_by_role"][role] = {
            key: worker[key] for key in (
                "role", "worker_id", "process_id", "process_start_token",
                "control_channel_id", "nonce_commitment_sha256",
            )
        }
        release["release_by_role"][role]["release_token_sha256"] = hashlib.sha256(
            f"{handshake_sha}:{role}:{release_epochs[role]}".encode("ascii")
        ).hexdigest()
    release_sha = record_sha256(release)
    records[("A22_TARGET_L12_AUTHORIZATION", 6)] = release
    commands: dict[str, dict[str, object]] = {}
    acks: dict[str, dict[str, object]] = {}
    for offset, role in enumerate(ROLES):
        worker = ready[role]
        command = {
            "schema": "V012_L12_WORKER_RELEASE_COMMAND_V001",
            **{
                key: worker[key] for key in (
                    "role", "worker_id", "process_id", "process_start_token",
                    "control_channel_id", "nonce_commitment_sha256",
                )
            },
            "handshake_sha256": handshake_sha,
            "worker_release_sha256": release_sha,
            "release_epoch": release_epochs[role],
        }
        commands[role] = command
        records[("A22_TARGET_L12_AUTHORIZATION", 7 + offset)] = command
        ack = {
            "schema": "V012_L12_WORKER_RELEASE_ACK_V001",
            **{
                key: worker[key] for key in (
                    "role", "worker_id", "process_id", "process_start_token",
                    "control_channel_id",
                )
            },
            "nonce_hex": nonces[role].hex(),
            "ack_sha256": hashlib.sha256(
                b"V012_DUAL_L12_RELEASE_ACK_V001\0" + nonces[role]
                + canonical_json_bytes(command)
            ).hexdigest(),
        }
        acks[role] = ack
        records[("A22_TARGET_L12_AUTHORIZATION", 9 + offset)] = ack
    target.update({
        "target_hostile_l10_cross_gate_sha256": a18_sha,
        "shared_aggregate_schedule_gate_sha256": schedule_sha,
        "shared_aggregate_schedule_gate_audit_sha256": schedule_audit_sha,
        "hostile_l12_execution_gate_sha256": auth_hash["hostile_v004r4"],
        "dual_l12_launch_handshake_sha256": handshake_sha,
        "dual_l12_worker_release_sha256": release_sha,
        "target_l12_execution_gate_sha256": auth_hash["target_v012"],
        "execution_authorization_sha256": auth_hash["target_v012"],
        "promotion_audit_sha256": schedule_audit_sha,
    })
    hostile.update({
        "target_hostile_l10_cross_gate_sha256": a18_sha,
        "shared_aggregate_schedule_gate_sha256": schedule_sha,
        "shared_aggregate_schedule_gate_audit_sha256": schedule_audit_sha,
        "hostile_l12_execution_gate_sha256": auth_hash["hostile_v004r4"],
        "dual_l12_launch_handshake_sha256": handshake_sha,
        "dual_l12_worker_release_sha256": release_sha,
    })
    completion_epochs = {
        "target_v012": 2_000_000_130,
        "hostile_v004r4": 2_000_000_131,
    }
    completions: dict[str, dict[str, object]] = {}
    output_records = {
        "target_v012": target,
        "hostile_v004r4": hostile,
    }
    for offset, role in enumerate(ROLES):
        completions[role] = {
            "schema": "V012_L12_WORKER_COMPLETION_V001",
            "role": role,
            "worker_id": ready[role]["worker_id"],
            "process_id": ready[role]["process_id"],
            "process_start_token": ready[role]["process_start_token"],
            "control_channel_id": ready[role]["control_channel_id"],
            "output_path": ready[role]["output_path"],
            "output_sha256": record_sha256(output_records[role]),
            "completion_epoch": completion_epochs[role],
            "blocked_on_orchestrator_close": True,
        }
        records[("A22_TARGET_L12_AUTHORIZATION", 11 + offset)] = (
            completions[role]
        )
    telemetry = _telemetry_fixture({
        "target_v012": record_sha256(target),
        "hostile_v004r4": record_sha256(hostile),
    })
    telemetry.update({
        "shared_gate_sha256": schedule_sha,
        "schedule_audit_sha256": schedule_audit_sha,
        "dual_launch_handshake_sha256": handshake_sha,
        "worker_release_sha256": release_sha,
        "authorization_sha256_by_role": auth_hash,
        "worker_identity_by_role": {
            role: {
                key: ready[role][key] for key in WORKER_IDENTITY_KEYS
            } for role in ROLES
        },
        "release_command_sha256_by_role": {
            role: record_sha256(commands[role]) for role in ROLES
        },
        "release_ack_sha256_by_role": {
            role: record_sha256(acks[role]) for role in ROLES
        },
        "completion_sha256_by_role": {
            role: record_sha256(completions[role]) for role in ROLES
        },
    })
    # Rebind sample identities after replacing the top-level fixture identities.
    for role in ROLES:
        for sample in telemetry["runtime_samples_by_role"][role]:
            for key in (
                "process_id", "process_start_token", "executable_path",
                "executable_sha256",
            ):
                sample[key] = telemetry["worker_identity_by_role"][role][key]
    records[("A23_POSTRUN_TELEMETRY", 1)] = telemetry
    records[("A24_TARGET_L12_HISTORY", 1)] = target
    records[("A25_HOSTILE_L12_HISTORY", 1)] = hostile
    return records, telemetry


def _fixture_authority_bindings(
    records: dict[tuple[str, int], dict[str, object]],
) -> list[dict[str, object]]:
    bindings: list[dict[str, object]] = []
    for artifact_id, count in AUTHORITY_INSTANCE_CENSUS.items():
        for instance in range(1, count + 1):
            if artifact_id == "A17_HOSTILE_L12_ELIGIBILITY":
                branch, sources, source_records, _metadata = (
                    _fixture_a17_material()
                )
                if records[(artifact_id, instance)] != branch:
                    raise AssertionError("internal A17 fixture branch drift")
                bindings.append({
                    "artifact_id": artifact_id,
                    "instance": instance,
                    "sources": sources,
                    "sha256": record_sha256(branch),
                    "record": branch,
                    "source_records": source_records,
                })
                continue
            bindings.append({
            "artifact_id": artifact_id,
            "instance": instance,
            "path": f"/synthetic/authority/{artifact_id}/{instance:02d}.json",
            "sha256": record_sha256(records[(artifact_id, instance)]),
            "record": records[(artifact_id, instance)],
            })
    return bindings


@lru_cache(maxsize=1)
def _positive_fixture_bundle_cached() -> dict[str, dict[str, object]]:
    target = _history_fixture("target_v012")
    hostile = _history_fixture("hostile_v004r4")
    authority_records, telemetry = _terminal_authority_fixture_records(
        _upstream_fixture_records(), target, hostile,
    )
    expected_checks = {
        "postrun_telemetry": 1,
        "complete_l12_histories": 2,
        "terminal_shard_custody": 24,
        "basis_permutation_projections": 24,
        "terminal_numerical_comparisons": 12,
        "native_history_field_projections": 13,
        "transitive_authorization_bindings": sum(AUTHORITY_INSTANCE_CENSUS.values()),
        "independent_auditor_isolation": 1,
    }
    final = {
        "schema": "TARGET_V012_HOSTILE_V004R4_FINAL_L12_AUDIT_V001",
        "classification": "PASS_FINITE_L12_TARGET_HOSTILE_ACCUMULATION",
        "auditor_role": "INDEPENDENT_FINAL_L12_AUDITOR",
        "authority_bindings": [],
        "comparison_policy": {
            "target_basis": "TARGET_FIXED_WORDS_LEXICOGRAPHIC_COMBINATION_ORDER",
            "hostile_basis": "REVERSED_COMBINATION__FULL_MASK",
            "projection": "TARGET_RANK_TO_HOSTILE_RANK_ON_LINEAGE_AND_CARRIER_AXES",
            "permutation_serialization": "V001_TAGGED_LE_U64_TARGET_RANK_TO_HOSTILE_RANK",
            "tolerance": TOLERANCE,
            "nonfinite_refusal": True,
        },
        "history_projection": {
            "mapping": "NATIVE_HOSTILE_V004R3_TO_TARGET_PHYSICAL_FIELDS_V001",
            "row_linf_abs_error": 0.0,
            "comparison_linf_abs_error": 0.0,
            "tolerance": TOLERANCE,
        },
        "terminal_comparisons": [
            {
                "q": q,
                "target_sha256": target["terminal_shards"][q]["sha256"],
                "hostile_sha256": hostile["terminal_shards"][q]["sha256"],
                "lineage_target_to_hostile_permutation_sha256": basis_permutation_sha256(11, q),
                "carrier_target_to_hostile_permutation_sha256": basis_permutation_sha256(24, q),
                "linf_abs_error": 5.0e-9,
            }
            for q in range(12)
        ],
        "checks": expected_checks,
        "checks_total": sum(expected_checks.values()),
        "checks_passed": sum(expected_checks.values()),
        "failures": [],
        "authority_records_authenticated": sum(AUTHORITY_INSTANCE_CENSUS.values()),
        "custody": _fixture_custody(),
        "claim_boundary": "FINITE_L12_TARGET_HOSTILE_ACCUMULATION_ONLY__NO_SPECTRUM_Z1_CONTINUUM_EMERGENCE_OR_GRAVITY",
    }
    assignments = _matrix_assignments()
    fixture_ids = sorted({fixture_id for _, fixture_id, _ in assignments})
    fixture_hashes = {
        fixture_id: _h(f"combined-positive:{fixture_id}")
        for fixture_id in fixture_ids
    }
    mutated_hashes = {
        f"MCASE_{index:04d}": _h(f"combined-mutant:{index}")
        for index in range(1, len(assignments) + 1)
    }
    cases: list[dict[str, object]] = []
    for index, (artifact_id, fixture_id, mutation) in enumerate(
        assignments, start=1,
    ):
        case_id = f"MCASE_{index:04d}"
        cases.append({
            "case_id": case_id,
            "artifact_id": artifact_id,
            "fixture_id": fixture_id,
            "mutation_class": mutation,
            "byte_mutation": f"synthetic native byte mutation {mutation}",
            "expected_refusal": _ledger_expected_refusal(
                artifact_id, fixture_id, mutation,
            ),
            "actual_refusal": (
                f"{artifact_id}: "
                f"{_ledger_expected_refusal(artifact_id, fixture_id, mutation)}"
            ),
            "positive_fixture_sha256": fixture_hashes[fixture_id],
            "mutated_fixture_sha256": mutated_hashes[case_id],
            "mutation_evidence_sha256": _h(f"combined-evidence:{index}"),
            "production_hook": _ledger_expected_hook(
                artifact_id, fixture_id, mutation,
            ),
            "validator_function": _ledger_expected_validator(
                artifact_id, fixture_id, mutation,
            ),
            "production_sink_calls": 1,
            "canonical_artifact_created": False,
            "passed": True,
        })
    source_hashes = {
        key: _h(f"combined-source:{key}") for key in SOURCE_FILE_KEYS
    }
    ledger = {
        "schema": MUTATION_LEDGER_SCHEMA,
        "classification": MUTATION_LEDGER_CLASSIFICATION,
        "audited_packet": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012",
        "sealed_input_commit": "42f1ea3301ccf98802c07f3330d52999385cba0b",
        "obligation_matrix_path": OBLIGATION_MATRIX_RELATIVE,
        "obligation_matrix_sha256": OBLIGATION_MATRIX_SHA256,
        "freeze_sha256": _h("combined-freeze"),
        "source_sha256": source_hashes,
        "positive_fixture_sha256_by_id": fixture_hashes,
        "mutated_fixture_sha256_by_case_id": mutated_hashes,
        "validator_module": {
            "path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/production_obligation_validators.py",
            "sha256": source_hashes["production_obligation_validators.py"],
        },
        "production_hook": PRODUCTION_FIXTURE_HOOK,
        "positive_sink_call_count": len(fixture_ids),
        "mutation_sink_call_count": len(cases),
        "case_count": len(cases),
        "checks_passed": len(cases),
        "checks_total": len(cases),
        "canonical_artifact_created": False,
        "cases": cases,
        "claim_boundary": MUTATION_LEDGER_CLAIM,
    }
    authority_records[("A27_MUTATION_LEDGER", 1)] = ledger
    final["authority_bindings"] = _fixture_authority_bindings(authority_records)
    return {
        "A23_POSTRUN_TELEMETRY": telemetry,
        "A24_TARGET_L12_HISTORY": target,
        "A25_HOSTILE_L12_HISTORY": hostile,
        "A26_FINAL_L12_AUDIT": final,
        "A27_MUTATION_LEDGER": ledger,
    }


def positive_fixture_bundle() -> dict[str, dict[str, object]]:
    return deepcopy(_positive_fixture_bundle_cached())


def positive_fixture(artifact_id: object) -> dict[str, object]:
    if type(artifact_id) is not str or artifact_id not in ARTIFACT_IDS:
        raise Refusal("unknown A23-A27 fixture id")
    return deepcopy(_positive_fixture_bundle_cached()[artifact_id])


def _duplicate_payload(record: dict[str, object]) -> bytes:
    payload = canonical_json_bytes(record).decode("ascii").strip()
    return ("{\"schema\":\"DUPLICATE\"," + payload[1:] + "\n").encode("ascii")


def _nonfinite_payload(record: dict[str, object]) -> bytes:
    payload = canonical_json_bytes(record).decode("ascii").strip()
    return (payload[:-1] + ",\"nonfinite_probe\":NaN}\n").encode("ascii")


def mutated_fixture(artifact_id: object, mutation_class: object) -> tuple[dict[str, object] | bytes, str, str]:
    if type(artifact_id) is not str or artifact_id not in ARTIFACT_IDS:
        raise Refusal("unknown A23-A27 fixture id")
    if type(mutation_class) is not str or mutation_class not in MUTATION_ASSIGNMENTS[artifact_id]:
        raise Refusal("unassigned mutation class")
    record = positive_fixture(artifact_id)
    def authority_binding(aid: str, instance: int = 1) -> dict[str, object]:
        for binding in record.get("authority_bindings", []):
            if binding.get("artifact_id") == aid and binding.get("instance") == instance:
                return binding
        _fail(str(artifact_id), f"missing fixture authority {aid}:{instance}")
    expected = artifact_id
    description = f"{artifact_id} {mutation_class} synthetic mutation"
    if mutation_class == "M04_DUPLICATE_JSON_KEY":
        return _duplicate_payload(record), expected, description
    if mutation_class == "M05_NONFINITE_JSON":
        return _nonfinite_payload(record), expected, description
    if mutation_class == "M01_MISSING_KEY":
        del record["schema"]
    elif mutation_class == "M02_EXTRA_KEY":
        record["unexpected"] = None
    elif mutation_class == "M03_WRONG_KEY_SAME_COUNT":
        record["wrong_classification"] = record.pop("classification")
    elif mutation_class == "M06_BOOL_FOR_INT":
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["launch_epoch_by_role"]["target_v012"] = True
        elif artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["L"] = True
        else: record["checks_total"] = True
    elif mutation_class == "M07_FLOAT_INT_ALIAS":
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["launch_epoch_by_role"]["target_v012"] = 2_000_000_010.0
        elif artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["events"] = 12.0
        else: record["checks_total"] = float(record["checks_total"])
    elif mutation_class == "M08_INT_FLOAT_ALIAS":
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["wall_seconds_by_role"]["target_v012"] = 120
        elif artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["rows"][0]["W_n"] = 1
        elif artifact_id == "A26_FINAL_L12_AUDIT": record["terminal_comparisons"][0]["linf_abs_error"] = 0
        else: record["cases"][0]["byte_mutation"] = 1
    elif mutation_class == "M09_INT_OR_FLOAT_FOR_BOOL":
        if artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["comparison"]["resolved"] = 1
        elif artifact_id == "A26_FINAL_L12_AUDIT": record["authority_records_authenticated"] = True
        else: record["cases"][0]["passed"] = 1
    elif mutation_class == "M10_IDENTITY_OR_CLAIM":
        record["classification"] = "PASS"
    elif mutation_class == "M11_HASH_OR_PATH":
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["output_path_by_role"]["target_v012"] = None
        elif artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["terminal_shards"][0]["path"] = None
        elif artifact_id == "A26_FINAL_L12_AUDIT": authority_binding("A24_TARGET_L12_HISTORY")["sha256"] = "0" * 64
        else: record["obligation_matrix_sha256"] = "bad"
    elif mutation_class == "M12_SYMLINK_OR_WRITABLE":
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["output_path_by_role"]["target_v012"] = "/synthetic/target_v012/../target_v012/history"
        elif artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["terminal_shards"][0]["path"] = "/synthetic/link/q_00.npy"
        elif artifact_id == "A26_FINAL_L12_AUDIT": record["custody"]["immutable_ordinary_file"] = False
        else: record["validator_module"]["path"] = "/synthetic/writable.py"
    elif mutation_class == "M13_DESCRIPTOR_TOCTOU":
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["output_sha256_by_role"]["target_v012"] = "0" * 64
        elif artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["terminal_shards"][0]["sha256"] = "0" * 64
        elif artifact_id == "A26_FINAL_L12_AUDIT": record["custody"]["rehash_after_validation"] = False
        else: record["validator_module"]["sha256"] = "0" * 64
    elif mutation_class == "M14_COUNT_ARITHMETIC":
        record["checks_total"] += 1
    elif mutation_class == "M15_LIST_CENSUS_ORDER":
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["runtime_samples_by_role"]["target_v012"].reverse()
        elif artifact_id == "A26_FINAL_L12_AUDIT": record["terminal_comparisons"].reverse()
        else: record["cases"].reverse()
    elif mutation_class == "M16_CROSS_ROLE_ALIAS":
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["output_sha256_by_role"]["hostile_v004r4"] = record["output_sha256_by_role"]["target_v012"]
        elif artifact_id == "A25_HOSTILE_L12_HISTORY": record["schema"] = "TARGET_CACHED_PREFIX_HISTORY_V012"
        elif artifact_id == "A26_FINAL_L12_AUDIT":
            target_binding = authority_binding("A24_TARGET_L12_HISTORY")
            hostile_binding = authority_binding("A25_HOSTILE_L12_HISTORY")
            hostile_binding["record"] = deepcopy(target_binding["record"])
            hostile_binding["sha256"] = record_sha256(hostile_binding["record"])
        else: record["positive_fixture_sha256_by_id"]["PF_A25"] = record["positive_fixture_sha256_by_id"]["PF_A24"]
    elif mutation_class in ("M17_PROVENANCE_DROP_SWAP", "M19_STAGE_BYPASS", "M24_UNLOCK_AUDIT_BINDING", "M26_L10_CROSS_MISMATCH"):
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["schedule_audit_sha256"] = record["shared_gate_sha256"]
        elif artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["target_hostile_l10_cross_gate_sha256"] = "0" * 64
        elif artifact_id == "A26_FINAL_L12_AUDIT": authority_binding("A24_TARGET_L12_HISTORY")["record"]["target_hostile_l10_cross_gate_sha256"] = "0" * 64
        else: record["cases"][0]["artifact_id"] = "A19_STAGE_BYPASS"
    elif mutation_class == "M18_CACHE_CENSUS_SEMANTICS":
        record["cases"][0]["byte_mutation"] = False
    elif mutation_class == "M20_HISTORY_PROJECTION":
        if artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["rows"][1]["event"] += 1
        elif artifact_id == "A26_FINAL_L12_AUDIT": authority_binding("A24_TARGET_L12_HISTORY")["record"]["rows"][1]["event"] += 1
        else: record["cases"][0]["fixture_id"] = "PF_BAD"
    elif mutation_class == "M21_TERMINAL_SHARD":
        if artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["terminal_shards"][0]["bytes"] += 16
        elif artifact_id == "A26_FINAL_L12_AUDIT": record["terminal_comparisons"][0]["target_sha256"] = "0" * 64
        else: record["cases"][0]["mutated_fixture_sha256"] = record["cases"][1]["mutated_fixture_sha256"]
    elif mutation_class == "M22_RESOURCE_FRESHNESS":
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["peak_rss_bytes_by_role"]["target_v012"] = RSS_LIMIT + 1
        elif artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["resource"]["peak_rss_bytes"] = RSS_LIMIT + 1
        elif artifact_id == "A26_FINAL_L12_AUDIT": authority_binding("A23_POSTRUN_TELEMETRY")["record"]["peak_rss_bytes_by_role"]["target_v012"] = RSS_LIMIT + 1
        else: record["freeze_sha256"] = "0" * 64
    elif mutation_class == "M23_HANDSHAKE_TELEMETRY":
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["dual_launch_handshake_sha256"] = "0" * 64
        elif artifact_id == "A26_FINAL_L12_AUDIT": authority_binding("A23_POSTRUN_TELEMETRY")["record"]["dual_launch_handshake_sha256"] = "0" * 64
        else: record["cases"][0]["actual_refusal"] = ""
    elif mutation_class == "M25_IMPORT_TARGET_VALIDATOR":
        if artifact_id == "A26_FINAL_L12_AUDIT": record["authority_records_authenticated"] = False
        else: record["cases"][0]["passed"] = False
    elif mutation_class == "M27_L12_CROSS_MISMATCH":
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["output_sha256_by_role"]["hostile_v004r4"] = record["output_sha256_by_role"]["target_v012"]
        elif artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["terminal_shards"][0]["sha256"] = "0" * 64
        elif artifact_id == "A26_FINAL_L12_AUDIT": record["terminal_comparisons"][0]["linf_abs_error"] = 2.0e-8
        else: record["cases"][0]["actual_refusal"] = "A27_MUTATION_LEDGER: wrong"
    elif mutation_class == "M28_PREMATURE_ARTIFACT":
        if artifact_id == "A23_POSTRUN_TELEMETRY": record["classification"] = "PREMATURE_SHARED_L12_TELEMETRY"
        elif artifact_id in ("A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"): record["terminal_shards"][0]["path"] = "/synthetic/premature/q_00.npy"
        elif artifact_id == "A26_FINAL_L12_AUDIT": record["custody"]["atomically_created_once"] = False
        else: record["canonical_artifact_created"] = True
    elif mutation_class == "M29_WRONG_ABSENCE_VALUE":
        record["cases"][0]["canonical_artifact_created"] = True
    else:
        _fail(artifact_id, f"mutation factory has no implementation for {mutation_class}")
    return record, expected, description
