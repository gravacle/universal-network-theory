#!/usr/bin/env python3
"""Owner-once L4 target reproduction with V002 hardened checkpoint controls."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import hardened_runtime as hard


PACKET = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-root", type=Path, default=PACKET / "CHECKPOINTS" / "L4_EVENT00_TARGET_V002R3")
    parser.add_argument("--output", type=Path, default=PACKET / "PHYSICAL_OUTPUTS" / "L4_TARGET_REPRODUCTION_V002R3.json")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    target = hard.target
    require_root = PACKET.parent.resolve()
    checkpoint = args.checkpoint_root.resolve()
    output = args.output.resolve()
    if not checkpoint.is_relative_to(require_root) or not output.is_relative_to(require_root):
        raise hard.durable.EvidenceError("checkpoint/output must remain in the development clone")
    target.load_resume_runtime = lambda: (hard.durable, hard.runtime_adapter)
    original_build = target.build_l4_result

    def build_with_hardened_custody(sectors, preflight, checkpoint_root, elapsed):
        result = original_build(sectors, preflight, checkpoint_root, elapsed)
        result["dependencies"].update({
            "hardened_runtime_sha256": hard.durable.sha256_file(PACKET / "hardened_runtime.py"),
            "hardened_runner_sha256": hard.durable.sha256_file(Path(__file__)),
            "execution_kernel_adapter_sha256": hard.durable.sha256_file(PACKET / "frozen_kernel_adapter.py"),
        })
        relative_checkpoint = checkpoint.relative_to(require_root)
        relative_output = output.relative_to(require_root)
        result["checkpoint"]["recovery_command"] = (
            "python3 " + str(Path(__file__).relative_to(require_root))
            + " --checkpoint-root " + str(relative_checkpoint)
            + " --output " + str(relative_output) + " --resume"
        )
        return result

    target.build_l4_result = build_with_hardened_custody
    if output.exists():
        if not args.resume:
            raise hard.durable.EvidenceError("existing final requires explicit --resume verification")
        pool = hard.make_l4_pool(checkpoint)
        pool.bind_identity(resume=True)
        pool.verify_complete()
        sectors = [pool.load_completed()[task.task_id] for task in pool.tasks]
        preflight = target.authenticate_all_inputs()
        existing = target.verify_l4_output(output)
        expected = build_with_hardened_custody(
            sectors, preflight, checkpoint, float(existing["resource"]["wall_seconds"]),
        )
        expected.pop("resource")
        observed = dict(existing)
        observed.pop("resource")
        if observed != expected:
            raise hard.durable.EvidenceError("existing final differs from verified checkpoint reconstruction")
        print("PASS_VERIFIED_EXISTING_L4_FINAL")
        return 0
    target.run_l4(output, checkpoint, args.resume)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (hard.durable.EvidenceError, hard.target.ScalingError, RuntimeError, ValueError) as error:
        print(f"FAIL V002 target L4: {error}", file=sys.stderr)
        raise SystemExit(1)
