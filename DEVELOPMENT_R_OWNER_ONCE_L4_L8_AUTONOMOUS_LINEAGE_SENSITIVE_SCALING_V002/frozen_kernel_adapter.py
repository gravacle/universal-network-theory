#!/usr/bin/env python3
"""Run the byte-sealed V001 L4 scientific kernel after an additive Git commit.

The V001 kernel itself remains byte-for-byte unchanged. This adapter replaces
only its fixed-HEAD authentication with the V002 frozen-parent/tree/dependency
check; it records its own hash as the process-pool execution kernel.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import hardened_runtime as hard


def sector_kernel(task_payload: Mapping[str, Any], context: Mapping[str, Any]) -> dict[str, Any]:
    hard.authenticate_frozen_dependencies()
    result = hard.target.sector_kernel(task_payload, context)
    result["task_binding"]["kernel_sha256"] = hard.durable.sha256_file(Path(__file__))
    return result
