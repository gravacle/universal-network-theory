#!/usr/bin/env python3
"""Narrow, parent-only persistent evidence for the V002 L12 replay."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import threading
from pathlib import Path
from typing import Any

import numpy as np


SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


class EvidenceRefusal(RuntimeError):
    """A durable evidence path could not be created exactly once."""


def normalize(value: Any) -> Any:
    """Convert parent reductions to canonical JSON without changing values."""
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, dict):
        return {str(key): normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return "unknown" if math.isinf(value) else "nan"
    return value


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(normalize(value), sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def atomic_immutable_json(path: Path, value: Any) -> str:
    """Create one fsynced, read-only JSON checkpoint without replacement."""
    if path.exists() or path.is_symlink():
        raise EvidenceRefusal(f"evidence checkpoint already exists: {path}")
    payload = canonical_json_bytes(value)
    temporary = path.parent / f".{path.name}.tmp.{os.getpid()}.{threading.get_ident()}"
    descriptor = os.open(
        temporary,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
        0o600,
    )
    linked = False
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = -1
        temporary.chmod(0o444)
        os.link(temporary, path, follow_symlinks=False)
        linked = True
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        expected = hashlib.sha256(payload).hexdigest()
        if observed != expected:
            raise EvidenceRefusal(f"evidence hash mismatch: {path}")
        return observed
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary.exists():
            temporary.unlink()
        if linked and path.stat().st_mode & 0o222:
            raise EvidenceRefusal(f"evidence remained writable: {path}")


class EvidenceJournal:
    """Write append-only checkpoint files from one branch parent."""

    def __init__(self, root: Path, branch: str):
        if branch not in {"target", "hostile"}:
            raise ValueError("branch must be target or hostile")
        if not root.is_absolute() or root.exists() or root.is_symlink():
            raise EvidenceRefusal("evidence root must be a fresh absolute path")
        self.root = root
        self.branch = branch
        self._sequence = 0
        self._lock = threading.Lock()
        root.mkdir(parents=True, exist_ok=False)
        for category in ("progress", "histories", "comparison", "lifecycle"):
            (root / category).mkdir(exist_ok=False)
        self.write(
            "lifecycle",
            "JOURNAL_OPEN",
            {
                "schema": "L12_PROCESS_PARALLEL_PARENT_EVIDENCE_V002",
                "branch": branch,
                "parent_pid": os.getpid(),
            },
        )

    def write(self, category: str, label: str, payload: Any) -> dict[str, Any]:
        if category not in {"progress", "histories", "comparison", "lifecycle"}:
            raise EvidenceRefusal("invalid evidence category")
        if not SAFE_NAME.fullmatch(label):
            raise EvidenceRefusal("unsafe evidence label")
        with self._lock:
            self._sequence += 1
            name = f"{self._sequence:06d}__{label}.json"
            path = self.root / category / name
            record = {
                "schema": "L12_PROCESS_PARALLEL_CHECKPOINT_V002",
                "sequence": self._sequence,
                "branch": self.branch,
                "category": category,
                "label": label,
                "payload": payload,
            }
            digest = atomic_immutable_json(path, record)
        print(
            "L12_CHECKPOINT "
            f"branch={self.branch} category={category} label={label} "
            f"sequence={self._sequence} sha256={digest} path={path}",
            flush=True,
        )
        return {"path": str(path), "sha256": digest, "sequence": self._sequence}

    def progress(self, label: str, payload: Any) -> dict[str, Any]:
        return self.write("progress", label, payload)

    def history(self, phase: str, value: dict[str, Any]) -> dict[str, Any]:
        if phase not in {"rough", "sharp"}:
            raise EvidenceRefusal("history phase must be rough or sharp")
        return self.write("histories", f"{phase.upper()}_SUMMARY", value)

    def comparison(self, value: dict[str, Any]) -> dict[str, Any]:
        return self.write("comparison", "PRE_GATE_COMPARISON", value)

