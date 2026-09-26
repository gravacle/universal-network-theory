#!/usr/bin/env python3
"""Atomic production orchestrator for the target L10/L12 held-out witness.

The orchestrator has no result-dependent branch between L10 and L12 and
publishes no partial scientific JSON.  Production execution is authorized
only by the exact frozen target token and a fresh neutral full-gate receipt
bound to the resource-preflight telemetry.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import resource
import shutil
import stat
import sys
import time
from pathlib import Path
from typing import Callable, Mapping

import heldout_target_adapter as target


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCHEMA = "OWNER_ONCE_HELDOUT_TARGET_JOINT_WITNESS_RAW_V001"
STATUS = "SEALED_TARGET_L10_L12_RAW_COMPLETE"
NEUTRAL_RECEIPT_SCHEMA = "OWNER_ONCE_HELDOUT_NEUTRAL_FULL_GATE_RECEIPT_V001"
NEUTRAL_RECEIPT_CLASSIFICATION = "PASS_NEUTRAL_FULL_GATE_PREOUTPUT"
TARGET_SCRATCH_RELATIVE = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_"
    "HELDOUT_TARGET_V001/PHYSICAL_SCRATCH/TARGET_V001"
)
TARGET_OUTPUT_RELATIVE = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_"
    "HELDOUT_TARGET_V001/PHYSICAL_OUTPUTS/TARGET_HELDOUT_WITNESS_RESULT_V001.json"
)
CONTROL_TELEMETRY_PARENT_RELATIVE = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_"
    "HELDOUT_TARGET_V001/CONTROL_PLANE_TELEMETRY"
)
CONTROL_RECEIPT_PARENT_RELATIVE = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_"
    "HELDOUT_TARGET_V001/CONTROL_PLANE_RECEIPTS"
)
LOCAL_SOURCE_MANIFEST = HERE / "SOURCE_HASHES.sha256"
LOCAL_SOURCE_CENSUS = {
    "PRODUCTION_SOURCE_FREEZE_V001.json",
    "README.md",
    "SYNTHETIC_FREEZE_V001.json",
    "SYNTHETIC_REVIEW.md",
    "TARGET_V003_CAPACITY_PROFILE.json",
    "heldout_target_adapter.py",
    "neutral_gate_receipt.py",
    "target_production_orchestrator.py",
    "test_heldout_target_adapter.py",
    "test_production_guards.py",
}


class LiveResourceGuard:
    """Fail-closed live wall/RSS/scratch monitor for one target transaction."""

    def __init__(
        self,
        *,
        root: Path,
        scratch_root: Path,
        monotonic: Callable[[], float] = time.monotonic,
        rss_probe: Callable[[], int] | None = None,
        wall_limit_seconds: int = 345_600,
        rss_limit_bytes: int = 17_179_869_184,
        scratch_limit_bytes: int = 20 * 2**30,
    ):
        # Preserve the caller's canonical spelling (notably /var versus
        # /private/var on macOS) so component-wise no-symlink checks compare
        # paths within the same namespace.
        self.root = root.absolute()
        self.scratch_root = scratch_root
        self.monotonic = monotonic
        self.started = monotonic()
        self.last_full_check = -math.inf
        self.wall_limit_seconds = wall_limit_seconds
        self.rss_limit_bytes = rss_limit_bytes
        self.scratch_limit_bytes = scratch_limit_bytes
        self.rss_probe = rss_probe or self._peak_rss_bytes

    @staticmethod
    def _peak_rss_bytes() -> int:
        value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        return value if sys.platform == "darwin" else value * 1024

    def _scratch_bytes(self) -> int:
        if not self.scratch_root.exists():
            return 0
        total = 0
        for directory, names, files in os.walk(self.scratch_root, followlinks=False):
            base = Path(directory)
            if base.is_symlink():
                raise target.HeldoutRefusal("scratch directory became a symlink")
            for name in names:
                path = base / name
                if path.is_symlink():
                    raise target.HeldoutRefusal("scratch child directory is a symlink")
            for name in files:
                path = base / name
                opened = os.stat(path, follow_symlinks=False)
                if not stat.S_ISREG(opened.st_mode):
                    raise target.HeldoutRefusal("scratch contains a nonregular file")
                total += opened.st_size
        return total

    def check(self, stage: str, *, force: bool = False) -> None:
        elapsed = self.monotonic() - self.started
        if elapsed < 0 or elapsed > self.wall_limit_seconds:
            raise target.HeldoutRefusal(
                f"EXACT_JOINT_WITNESS_SCALING_OBSTRUCTION: wall gate at {stage}"
            )
        rss = self.rss_probe()
        if rss < 0 or rss > self.rss_limit_bytes:
            raise target.HeldoutRefusal(
                f"EXACT_JOINT_WITNESS_SCALING_OBSTRUCTION: RSS gate at {stage}"
            )
        if not force and elapsed - self.last_full_check < 5.0:
            return
        target.require_no_symlink_chain(self.scratch_root, self.root)
        scratch = self._scratch_bytes()
        if scratch > self.scratch_limit_bytes:
            raise target.HeldoutRefusal(
                f"EXACT_JOINT_WITNESS_SCALING_OBSTRUCTION: scratch gate at {stage}"
            )
        self.last_full_check = elapsed


def validate_local_source_manifest(root: Path = ROOT) -> dict[str, str]:
    if LOCAL_SOURCE_MANIFEST.is_symlink() or not LOCAL_SOURCE_MANIFEST.is_file():
        raise target.HeldoutRefusal("target local source manifest absent")
    observed: dict[str, str] = {}
    for line in LOCAL_SOURCE_MANIFEST.read_text(encoding="ascii").splitlines():
        parts = line.split("  ")
        if len(parts) != 2 or len(parts[0]) != 64:
            raise target.HeldoutRefusal("malformed target local source manifest")
        digest, name = parts
        if name in observed or name not in LOCAL_SOURCE_CENSUS:
            raise target.HeldoutRefusal("unexpected target local source member")
        path = HERE / name
        if target.sha256_file(path) != digest:
            raise target.HeldoutRefusal(f"target local source drift: {name}")
        observed[name] = digest
    if set(observed) != LOCAL_SOURCE_CENSUS:
        raise target.HeldoutRefusal("target local source census mismatch")
    return observed


def _validate_neutral_receipt(
    receipt_path: Path,
    telemetry_path: Path,
    *,
    root: Path,
    now_epoch_seconds: int,
) -> tuple[dict[str, object], dict[str, object]]:
    receipt = target.strict_json(receipt_path)
    required = {
        "classification",
        "concurrent_release_deadline_epoch_seconds",
        "expires_epoch_seconds",
        "full_gate_validation",
        "gate_input_census_sha256",
        "gate_resource_sha256",
        "gate_sha256",
        "gate_validator_sha256",
        "issued_epoch_seconds",
        "maximum_release_skew_seconds",
        "protocol_sha256",
        "schema",
        "selected_schedule",
        "telemetry_sha256",
        "witness_values_computed_or_opened",
    }
    if set(receipt) != required:
        raise target.HeldoutRefusal("neutral receipt key census mismatch")
    gate = target.strict_json(
        root / target.HELDOUT_GATE_RELATIVE_PATH,
        target.HELDOUT_GATE_SHA256,
    )
    telemetry = target.strict_json(telemetry_path)
    expected_validation = {
        "classification": "PASS_HELDOUT_INPUT_AND_RESOURCE_GATE_PREOUTPUT",
        "full_shard_hashes_verified": True,
        "input_histories_verified": 4,
        "schema": "OWNER_ONCE_HELDOUT_GATE_VALIDATION_V001",
        "terminal_shard_bytes_verified": 13_671_711_776,
        "terminal_shards_verified": 44,
        "witness_values_computed_or_opened": False,
    }
    issued = receipt.get("issued_epoch_seconds")
    expires = receipt.get("expires_epoch_seconds")
    if (
        receipt.get("schema") != NEUTRAL_RECEIPT_SCHEMA
        or receipt.get("classification") != NEUTRAL_RECEIPT_CLASSIFICATION
        or receipt.get("protocol_sha256") != target.HELDOUT_PROTOCOL_SHA256
        or receipt.get("gate_sha256") != target.HELDOUT_GATE_SHA256
        or receipt.get("gate_validator_sha256") != target.HELDOUT_GATE_VALIDATOR_SHA256
        or receipt.get("full_gate_validation") != expected_validation
        or receipt.get("witness_values_computed_or_opened") is not False
        or type(issued) is not int
        or type(expires) is not int
        or expires - issued != int(gate["resource_gate"]["telemetry_max_age_seconds"])
        or now_epoch_seconds < issued
        or now_epoch_seconds > expires
        or receipt.get("gate_input_census_sha256")
        != target.canonical_digest(gate["inputs"])
        or receipt.get("gate_resource_sha256")
        != target.canonical_digest(gate["resource_gate"])
        or receipt.get("telemetry_sha256") != target.sha256_file(telemetry_path)
    ):
        raise target.HeldoutRefusal("neutral full-gate receipt failed")
    schedule = receipt.get("selected_schedule")
    if schedule != telemetry.get("selected_schedule"):
        raise target.HeldoutRefusal("neutral receipt/telemetry schedule mismatch")
    if receipt.get("maximum_release_skew_seconds") != 60:
        raise target.HeldoutRefusal("neutral receipt release-skew gate changed")
    deadline = receipt.get("concurrent_release_deadline_epoch_seconds")
    if schedule == "CONCURRENT_TARGET_AND_HOSTILE":
        if type(deadline) is not int or deadline != issued + 60 or now_epoch_seconds > deadline:
            raise target.HeldoutRefusal("concurrent release-skew gate failed")
    elif schedule == "SEQUENTIAL_TARGET_THEN_HOSTILE":
        if deadline is not None:
            raise target.HeldoutRefusal("sequential receipt has a concurrent deadline")
    else:
        raise target.HeldoutRefusal("neutral receipt selected invalid schedule")
    return receipt, telemetry


def _safe_runtime_paths(
    telemetry: Mapping[str, object], root: Path
) -> tuple[Path, Path]:
    if telemetry.get("target_scratch_root") != TARGET_SCRATCH_RELATIVE:
        raise target.HeldoutRefusal("target scratch root is not the frozen target root")
    if telemetry.get("target_output_path") != TARGET_OUTPUT_RELATIVE:
        raise target.HeldoutRefusal("target output path is not the frozen target path")
    raw_paths = [
        telemetry.get(name)
        for name in (
            "target_scratch_root",
            "hostile_scratch_root",
            "target_output_path",
            "hostile_output_path",
        )
    ]
    if any(not isinstance(item, str) for item in raw_paths):
        raise target.HeldoutRefusal("telemetry runtime path type mismatch")
    paths = [root / str(item) for item in raw_paths]
    resolved = [target.require_no_symlink_chain(path, root) for path in paths]
    if len(set(resolved)) != 4:
        raise target.HeldoutRefusal("scratch/output paths alias")
    return paths[0], paths[2]


def _require_control_path(path: Path, expected_parent_relative: str, root: Path) -> None:
    expected_parent = (root / expected_parent_relative).resolve(strict=False)
    target.require_no_symlink_chain(path, root)
    if path.resolve(strict=False).parent != expected_parent:
        raise target.HeldoutRefusal("control-plane file is outside its frozen root")


def _target_input_census(root: Path) -> dict[str, object]:
    census: dict[str, object] = {}
    for length, binding in target.HISTORY_BINDINGS.items():
        history = target.authenticate_retained_history(
            length,
            root=root,
            verify_payload_hashes=False,
        )
        census[str(length)] = {
            "history_path": binding.history_relative_path,
            "history_sha256": binding.history_sha256,
            "terminal_shard_count": len(history.shards),
            "terminal_shard_manifest_sha256": binding.terminal_manifest_sha256,
            "terminal_shard_total_bytes": binding.terminal_total_bytes,
            "terminal_shards": [
                {
                    "bytes": item.byte_count,
                    "path": target.repository_relative(item.path, root),
                    "q": item.q,
                    "sha256": item.sha256,
                    "shape": list(item.shape),
                }
                for item in history.shards
            ],
        }
    return census


def _maximum_disagreement(coarse: Mapping[str, object], fine: Mapping[str, object]) -> float:
    values: list[float] = []
    for stream in ("registered",):
        for key in ("probability", "w", "w_sham", "D", "w_shuffle"):
            values.append(abs(float(coarse[stream][key]) - float(fine[stream][key])))
    for q in coarse["q_contributions"]:
        for key in ("p_q", "w_q", "w_sham_q", "D_q", "w_shuffle_q"):
            values.append(
                abs(
                    float(coarse["q_contributions"][q][key])
                    - float(fine["q_contributions"][q][key])
                )
            )
    return target.finite(max(values, default=0.0), "target coarse/fine disagreement")


def _target_numerical_record(
    coarse: Mapping[str, object], fine: Mapping[str, object]
) -> dict[str, object]:
    disagreement = _maximum_disagreement(coarse, fine)
    row_column = max(
        float(coarse["residuals"]["row_column_accumulator"]),
        float(fine["residuals"]["row_column_accumulator"]),
    )
    r_value = max(
        float(record["residuals"][key])
        for record in (coarse, fine)
        for key in (
            "state_norm",
            "probability_normalization",
            "marginal_reconstruction",
            "sharp_sector_QS_minus_QC",
            "total_content",
        )
    )
    d_component = max(disagreement, row_column)
    tau_component = max(1.0e-9, 50.0 * d_component, 100.0 * r_value)
    conditions = {
        "target_coarse_fine_disagreement_le_1e_8": disagreement <= 1.0e-8,
        "norm_and_total_content_residual_le_1e_10": max(
            float(record["residuals"][key])
            for record in (coarse, fine)
            for key in ("state_norm", "total_content")
        ) <= 1.0e-10,
        "probability_and_marginal_reconstruction_le_1e_10": max(
            float(record["residuals"][key])
            for record in (coarse, fine)
            for key in ("probability_normalization", "marginal_reconstruction")
        ) <= 1.0e-10,
        "sharp_sector_QS_minus_QC_le_1e_10": max(
            float(record["residuals"]["sharp_sector_QS_minus_QC"])
            for record in (coarse, fine)
        ) <= 1.0e-10,
        "shuffle_expectation_le_1e_12": max(
            float(record["residuals"]["shuffle_expectation"])
            for record in (coarse, fine)
        ) <= 1.0e-12,
        "sham_self_covariance_le_1e_12": max(
            float(record["residuals"]["sham_self_covariance"])
            for record in (coarse, fine)
        ) <= 1.0e-12,
    }
    return {
        "all_target_internal_conditions_passed": all(conditions.values()),
        "conditions": conditions,
        "r_L_target_component": target.finite(r_value, "target r component"),
        "row_column_disagreement": target.finite(row_column, "row/column disagreement"),
        "target_coarse_fine_disagreement": disagreement,
        "target_internal_d_L_component": target.finite(
            d_component, "target d component"
        ),
        "target_internal_tau_L_component": target.finite(
            tau_component, "target tau component"
        ),
    }


def build_raw_result(
    components: Mapping[str, Mapping[str, object]],
    *,
    root: Path,
    local_sources: Mapping[str, str],
    transitive_sources: Mapping[str, str],
) -> dict[str, object]:
    length_records: dict[str, object] = {}
    for length in (10, 12):
        raw = components[str(length)]
        coarse_component = raw["coarse"]
        fine = raw["fine"]
        coarse = coarse_component["terminal"]
        numerical = _target_numerical_record(coarse, fine)
        length_records[str(length)] = {
            "coarse": coarse_component,
            "fine": fine,
            "target_internal_numerics": numerical,
        }
    all_passed = all(
        bool(length_records[str(length)]["target_internal_numerics"][
            "all_target_internal_conditions_passed"
        ])
        for length in (10, 12)
    )
    result = {
        "all_target_internal_numerical_and_control_conditions_passed": all_passed,
        "claim_boundary": (
            "TARGET_RAW_L10_L12_ONLY__NO_TARGET_HOSTILE_RECONCILIATION_"
            "GATE_RGRL_ALPHA_THERMODYNAMIC_CONTINUUM_OR_GRAVITY_RESULT"
        ),
        "fixed_parameters": {
            "checkpoint": "AFTER_FINAL_OWNER_ONCE_EVENT_TRANSPORT_BEFORE_REVISIT",
            "event_schedules": {"10": list(range(10)), "12": list(range(12))},
            "phi": "pi/4",
            "target_v003_capacity_profile_sha256":
                target.TARGET_V003_CAPACITY_PROFILE_SHA256,
        },
        "heldout_gate_sha256": target.HELDOUT_GATE_SHA256,
        "heldout_protocol_sha256": target.HELDOUT_PROTOCOL_SHA256,
        "implementation": {
            "local_source_manifest_sha256": target.sha256_file(
                LOCAL_SOURCE_MANIFEST
            ),
            "local_sources": dict(sorted(local_sources.items())),
            "target_transitive_sources": dict(sorted(transitive_sources.items())),
        },
        "lengths": length_records,
        "neutral_gate_validation": {
            "classification": "PASS_NEUTRAL_FULL_GATE_PREOUTPUT",
            "full_shard_hashes_verified": True,
            "input_histories_verified": 4,
            "terminal_shard_bytes_verified": 13_671_711_776,
            "terminal_shards_verified": 44,
            "witness_values_computed_or_opened_by_gate": False,
        },
        "role": "target",
        "schema": SCHEMA,
        "seed_authority_sha256": target.SEED_DISPOSITION_SHA256,
        "status": STATUS,
        "target_input_census": _target_input_census(root),
    }
    target.canonical_json_bytes(result)
    return result


def _atomic_write(output: Path, result: Mapping[str, object], root: Path) -> str:
    target.require_no_symlink_chain(output.parent, root)
    if output.exists() or output.is_symlink():
        raise target.HeldoutRefusal("target output already exists")
    raw = target.canonical_json_bytes(result)
    temporary = output.parent / f".{output.name}.{os.getpid()}.tmp"
    if temporary.exists() or temporary.is_symlink():
        raise target.HeldoutRefusal("target temporary output already exists")
    descriptor = os.open(
        temporary,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
        0o400,
    )
    try:
        written = 0
        while written < len(raw):
            count = os.write(descriptor, raw[written:])
            if count <= 0:
                raise target.HeldoutRefusal("short target output write")
            written += count
        os.fsync(descriptor)
    except BaseException:
        os.close(descriptor)
        temporary.unlink(missing_ok=True)
        raise
    else:
        os.close(descriptor)
    if output.exists() or output.is_symlink():
        temporary.unlink(missing_ok=True)
        raise target.HeldoutRefusal("target output appeared during atomic write")
    os.replace(temporary, output)
    parent_descriptor = os.open(output.parent, os.O_RDONLY)
    try:
        os.fsync(parent_descriptor)
    finally:
        os.close(parent_descriptor)
    digest = hashlib.sha256(raw).hexdigest()
    if target.sha256_file(output, require_readonly=True) != digest:
        raise target.HeldoutRefusal("target output seal verification failed")
    return digest


def _production_component_runner(
    length: int,
    mode: str,
    scratch_root: Path,
    root: Path,
    monitor: LiveResourceGuard,
) -> dict[str, object]:
    if mode == "coarse":
        return target._run_coarse_whole_history(
            length,
            scratch_root / f"rough_L{length}",
            root=root,
            monitor=monitor,
        )
    if mode == "fine":
        return target._run_fine_terminal_from_retained(
            length,
            root=root,
            monitor=monitor,
        )
    raise target.HeldoutRefusal(f"unknown target component mode: {mode}")


def run_atomic_target(
    *,
    authorization: str | None,
    telemetry_path: Path,
    neutral_receipt_path: Path,
    root: Path = ROOT,
    now: Callable[[], float] = time.time,
    monotonic: Callable[[], float] = time.monotonic,
    component_runner: Callable[[int, str, Path, Path, LiveResourceGuard], dict[str, object]]
    | None = None,
    rss_probe: Callable[[], int] | None = None,
) -> dict[str, object]:
    target.require_execution_authorization(authorization)
    started_epoch = int(now())
    _require_control_path(
        telemetry_path, CONTROL_TELEMETRY_PARENT_RELATIVE, root
    )
    _require_control_path(
        neutral_receipt_path, CONTROL_RECEIPT_PARENT_RELATIVE, root
    )
    target.authenticate_heldout_protocol(root)
    target.authenticate_seed_authority(root)
    local_sources = validate_local_source_manifest(root)
    transitive_sources = target.authenticate_target_transitive_sources(root)
    _receipt, telemetry = _validate_neutral_receipt(
        neutral_receipt_path,
        telemetry_path,
        root=root,
        now_epoch_seconds=started_epoch,
    )
    scratch_root, output = _safe_runtime_paths(telemetry, root)
    if output.exists() or output.is_symlink():
        raise target.HeldoutRefusal("target output pre-exists")
    scratch_parent = scratch_root.parent
    target.require_no_symlink_chain(scratch_parent, root)
    scratch_parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    target.require_no_symlink_chain(scratch_parent, root)
    if scratch_root.exists() or scratch_root.is_symlink():
        raise target.HeldoutRefusal("target scratch root pre-exists")
    scratch_root.mkdir(mode=0o700)
    output.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    target.require_no_symlink_chain(output.parent, root)
    monitor = LiveResourceGuard(
        root=root,
        scratch_root=scratch_root,
        monotonic=monotonic,
        rss_probe=rss_probe,
    )
    monitor.check("transaction-start", force=True)
    runner = component_runner or _production_component_runner

    # Fixed, unconditional schedule.  Result values are neither inspected nor
    # serialized until both sizes and both resolutions have completed.
    components: dict[str, dict[str, object]] = {"10": {}, "12": {}}
    for length in (10, 12):
        for mode in ("coarse", "fine"):
            if output.exists() or output.is_symlink():
                raise target.HeldoutRefusal("target output appeared before completion")
            monitor.check(f"before-{mode}-L{length}", force=True)
            components[str(length)][mode] = runner(
                length, mode, scratch_root, root, monitor
            )
            monitor.check(f"after-{mode}-L{length}", force=True)

    # No target value influenced the mandatory L12 execution above.
    target.authenticate_target_transitive_sources(root, monitor=monitor)
    target.authenticate_seed_authority(root)
    result = build_raw_result(
        components,
        root=root,
        local_sources=local_sources,
        transitive_sources=transitive_sources,
    )
    monitor.check("before-atomic-publication", force=True)
    _atomic_write(output, result, root)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--telemetry", type=Path, required=True)
    parser.add_argument("--neutral-receipt", type=Path, required=True)
    args = parser.parse_args()
    try:
        run_atomic_target(
            authorization=args.authorization,
            telemetry_path=args.telemetry,
            neutral_receipt_path=args.neutral_receipt,
        )
        print("SEALED_TARGET_L10_L12_RAW_COMPLETE")
        return 0
    except target.HeldoutRefusal as error:
        print(f"REFUSED: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
