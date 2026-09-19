#!/usr/bin/env python3
"""Test-only upstream fixture bridge; never imported by the A26 production path."""

from __future__ import annotations

import importlib.util
import sys
from functools import lru_cache
from pathlib import Path
from typing import Final


ROOT: Final[Path] = Path(__file__).resolve().parent.parent
FIXTURE_SOURCE: Final[Path] = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
    / "production_obligation_validators.py"
)


@lru_cache(maxsize=1)
def _module():
    specification = importlib.util.spec_from_file_location(
        "synthetic_target_fixture_source_only", FIXTURE_SOURCE,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("synthetic fixture source loader absent")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def fixture(artifact_id: str, variant: int = 0) -> dict[str, object]:
    """Return a target-generated positive used against the independent sink."""
    return _module().positive_fixture(artifact_id, variant)
