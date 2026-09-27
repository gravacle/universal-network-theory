#!/usr/bin/env python3
"""Verify frozen V002 L4 sources, checkpoint custody, and final reconstruction."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
CHECKPOINT = PACKET / "CHECKPOINTS/L4_EVENT00_TARGET_V002R3"
OUTPUT = PACKET / "PHYSICAL_OUTPUTS/L4_TARGET_REPRODUCTION_V002R3.json"
V001_OUTPUT = ROOT / "DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V001/PHYSICAL_OUTPUTS/L4_TARGET_REPRODUCTION_V001.json"
V001_OUTPUT_SHA256 = "509d96ad59268cd75ee3b1275fd095b4b8642d498750e81b9d145374c6ac8c4c"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_hash_list(name: str) -> list[str]:
    lines = (PACKET / name).read_text(encoding="ascii").splitlines()
    require(bool(lines), f"empty {name}")
    paths: list[str] = []
    for line in lines:
        digest, separator, relative = line.partition("  ")
        require(separator == "  " and len(digest) == 64 and all(c in "0123456789abcdef" for c in digest), f"malformed {name}")
        parts = Path(relative)
        require(not parts.is_absolute() and ".." not in parts.parts and str(parts) == relative, f"unsafe {name} route")
        path = PACKET / relative
        require(path.is_file() and not path.is_symlink() and sha256(path) == digest, f"{name} digest: {relative}")
        paths.append(relative)
    require(paths == sorted(set(paths)), f"{name} sorted unique census")
    return paths


def main() -> int:
    sources = verify_hash_list("SOURCE_HASHES.sha256")
    required_sources = {
        "README.md", "frozen_kernel_adapter.py", "hardened_runtime.py",
        "last_task_signal_worker.py", "run_l4_v002.py", "slow_kernel_fixture.py",
        "test_hardened_runtime.py", "verify_packet.py",
    }
    require(set(sources) == required_sources, "V002 source census")
    evidence = verify_hash_list("EVIDENCE_HASHES.sha256")
    observed_evidence = {
        path.relative_to(PACKET).as_posix()
        for path in CHECKPOINT.rglob("*.json")
    }
    observed_evidence.add(OUTPUT.relative_to(PACKET).as_posix())
    require(set(evidence) == observed_evidence, "V002 evidence JSON census")
    require((CHECKPOINT / "OWNER.lock").is_file() and (CHECKPOINT / "OWNER.lock").stat().st_size == 0, "checkpoint owner lock type")
    require(sha256(V001_OUTPUT) == V001_OUTPUT_SHA256, "historical dense L4 target seal")

    import hardened_runtime as hard

    preflight = hard.target.authenticate_all_inputs()
    pool = hard.make_l4_pool(CHECKPOINT)
    pool.verify_complete()
    sectors = [pool.load_completed()[task.task_id] for task in pool.tasks]
    output = hard.target.verify_l4_output(OUTPUT)
    expected = hard.target.build_l4_result(
        sectors, preflight, CHECKPOINT, float(output["resource"]["wall_seconds"]),
    )
    expected["dependencies"].update({
        "hardened_runtime_sha256": sha256(PACKET / "hardened_runtime.py"),
        "hardened_runner_sha256": sha256(PACKET / "run_l4_v002.py"),
        "execution_kernel_adapter_sha256": sha256(PACKET / "frozen_kernel_adapter.py"),
    })
    expected["checkpoint"]["recovery_command"] = (
        "python3 DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V002/run_l4_v002.py"
        " --checkpoint-root DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V002/CHECKPOINTS/L4_EVENT00_TARGET_V002R3"
        " --output DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V002/PHYSICAL_OUTPUTS/L4_TARGET_REPRODUCTION_V002R3.json --resume"
    )
    observed_science = dict(output)
    observed_science.pop("resource")
    expected.pop("resource")
    require(observed_science == expected, "final/checkpoint scientific reconstruction")
    resource = output["resource"]
    require(resource["maximum_sector_wall_seconds"] == max(row["resource"]["wall_seconds"] for row in sectors), "sector wall census")
    require(resource["maximum_sector_peak_rss_bytes"] == max(row["resource"]["peak_rss_bytes"] for row in sectors), "sector RSS census")
    require(resource["authenticated_preterminal_input_bytes"] == 3152, "L4 input bytes")
    require(resource["checkpoint_storage_bytes"] == sum(path.stat().st_size for path in CHECKPOINT.rglob("*") if path.is_file()), "checkpoint bytes")
    old = hard.target.load_json(V001_OUTPUT)
    for key in ("after_admission", "after_transport", "controls", "sector_results"):
        if key == "sector_results":
            normalized = lambda rows: [{field: value for field, value in row.items() if field != "resource"} for row in rows]
            require(normalized(output[key]) == normalized(old[key]), "V001/V002 sector scientific identity")
        else:
            require(output[key] == old[key], f"V001/V002 {key} scientific identity")
    print(f"PASS V002_L4_HARDENED_PACKET: {len(sources)} sources, {len(evidence)} evidence files, 5 sectors, L6/L8 locked")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        print(f"FAIL V002_L4_HARDENED_PACKET: {error}", file=sys.stderr)
        raise SystemExit(1)
