#!/usr/bin/env python3
"""L4-only restart fixture that holds the final in-flight task open."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Mapping

import hardened_runtime as hard


def sector_kernel(task_payload: Mapping[str, Any], context: Mapping[str, Any]) -> dict[str, Any]:
    if task_payload["q_out"] == 4:
        hard.durable.immutable_write_json(
            Path(context["checkpoint_root"]) / "Q4_STARTED.fixture.json",
            {
                "schema": "L4_Q4_INFLIGHT_FIXTURE_V001",
                "task_id": context["task_id"],
                "task_sha256": context["task_sha256"],
            },
        )
        time.sleep(1.0)
    hard.authenticate_frozen_dependencies()
    result = hard.target.sector_kernel(task_payload, context)
    result["task_binding"]["kernel_sha256"] = hard.durable.sha256_file(Path(__file__))
    return result
