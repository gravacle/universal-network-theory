#!/usr/bin/env python3
"""Small, dependency-free primitives for immutable L14 evidence.

The final-name publication operation is owner-once: a temporary file is fsynced,
hard-linked into its final pathname, and the containing directory is fsynced.
An existing final pathname is accepted only when its bytes are identical.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional


SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


class EvidenceError(RuntimeError):
    """An immutable evidence or durability invariant failed."""


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fsync_directory(path: Path) -> None:
    descriptor = os.open(str(path), os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def ensure_safe_name(name: str, label: str = "name") -> str:
    if not SAFE_NAME.fullmatch(name):
        raise EvidenceError("unsafe {}: {!r}".format(label, name))
    return name


def immutable_write_bytes(path: Path, data: bytes, mode: int = 0o444) -> str:
    """Publish *data* at *path* without replacing an existing final file."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    expected = sha256_bytes(data)
    if path.exists():
        actual = sha256_file(path)
        if actual != expected:
            raise EvidenceError("immutable collision at {}: {} != {}".format(path, actual, expected))
        return actual

    descriptor, temporary_name = tempfile.mkstemp(prefix=".{}-".format(path.name), dir=str(path.parent))
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(str(temporary), mode)
        try:
            os.link(str(temporary), str(path))
        except FileExistsError:
            actual = sha256_file(path)
            if actual != expected:
                raise EvidenceError("immutable race collision at {}".format(path))
        fsync_directory(path.parent)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass

    actual = sha256_file(path)
    if actual != expected:
        raise EvidenceError("post-publication digest mismatch at {}".format(path))
    return actual


def immutable_write_json(path: Path, payload: Any) -> str:
    return immutable_write_bytes(Path(path), canonical_json_bytes(payload))


def load_json(path: Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_artifact(path: Path, expected_sha256: str, expected_bytes: Optional[int] = None) -> None:
    path = Path(path)
    if not path.is_file():
        raise EvidenceError("missing artifact: {}".format(path))
    if expected_bytes is not None and path.stat().st_size != expected_bytes:
        raise EvidenceError("artifact byte-size mismatch: {}".format(path))
    actual = sha256_file(path)
    if actual != expected_sha256:
        raise EvidenceError("artifact SHA-256 mismatch at {}: {} != {}".format(path, actual, expected_sha256))


class AppendOnlyJournal:
    """An event journal whose entries are individually immutable JSON files."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.sequence = self._discover_last_sequence()

    def _discover_last_sequence(self) -> int:
        maximum = 0
        for path in self.root.glob("*.json"):
            try:
                maximum = max(maximum, int(path.name.split("__", 1)[0]))
            except (ValueError, IndexError):
                raise EvidenceError("malformed journal entry name: {}".format(path))
        return maximum

    def append(self, event: str, payload: Mapping[str, Any]) -> Path:
        ensure_safe_name(event, "event")
        self.sequence += 1
        path = self.root / "{:08d}__{}.json".format(self.sequence, event)
        body: Dict[str, Any] = {
            "schema": "L14_APPEND_ONLY_EVENT_V002",
            "sequence": self.sequence,
            "event": event,
            "payload": dict(payload),
        }
        immutable_write_json(path, body)
        return path

    def entries(self) -> Iterable[Dict[str, Any]]:
        for path in sorted(self.root.glob("*.json")):
            yield load_json(path)


class DurableMirror:
    """Copy immutable evidence to local storage or an S3 prefix.

    Numerical checkpoint artifacts must already live beneath the persistent
    checkpoint root. The mirror is a second copy, not the primary commit.
    """

    def __init__(self, destination: Optional[str]) -> None:
        self.destination = destination.rstrip("/") if destination else None

    @property
    def enabled(self) -> bool:
        return bool(self.destination)

    def publish(self, source: Path, relative_name: str) -> None:
        if not self.destination:
            return
        source = Path(source)
        if not source.is_file():
            raise EvidenceError("cannot mirror missing file: {}".format(source))
        relative = Path(relative_name)
        if relative.is_absolute() or ".." in relative.parts:
            raise EvidenceError("unsafe mirror relative path: {}".format(relative_name))
        if self.destination.startswith("s3://"):
            without_scheme = self.destination[5:]
            bucket, separator, prefix = without_scheme.partition("/")
            if not bucket:
                raise EvidenceError("malformed S3 mirror destination")
            key = "/".join(part for part in (prefix.rstrip("/"), relative.as_posix()) if part)
            digest = sha256_file(source)
            if source.stat().st_size > 5 * 1024 * 1024 * 1024:
                raise EvidenceError("owner-once S3 evidence upload is limited to 5 GiB: {}".format(source))
            command = [
                "aws",
                "s3api",
                "put-object",
                "--bucket",
                bucket,
                "--key",
                key,
                "--body",
                str(source),
                "--if-none-match",
                "*",
                "--server-side-encryption",
                "AES256",
                "--metadata",
                "sha256={}".format(digest),
            ]
            completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if completed.returncode == 0:
                return
            head = subprocess.run(
                ["aws", "s3api", "head-object", "--bucket", bucket, "--key", key, "--output", "json"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if head.returncode == 0:
                try:
                    remote = json.loads(head.stdout)
                except json.JSONDecodeError as error:
                    raise EvidenceError("cannot parse S3 owner-once verification") from error
                metadata = remote.get("Metadata", {})
                if metadata.get("sha256") == digest and int(remote.get("ContentLength", -1)) == source.stat().st_size:
                    return
            raise EvidenceError("S3 mirror failed for {}: {}".format(source, completed.stderr.strip()))

        destination_root = Path(self.destination).expanduser().resolve()
        target = destination_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if sha256_file(target) != sha256_file(source):
                raise EvidenceError("mirror collision at {}".format(target))
            return
        temporary = target.parent / (".{}-copy".format(target.name))
        if temporary.exists():
            temporary.unlink()
        shutil.copyfile(str(source), str(temporary))
        with temporary.open("rb") as handle:
            os.fsync(handle.fileno())
        os.chmod(str(temporary), 0o444)
        try:
            os.link(str(temporary), str(target))
        except FileExistsError:
            if sha256_file(target) != sha256_file(source):
                raise EvidenceError("mirror race collision at {}".format(target))
        finally:
            temporary.unlink()
        fsync_directory(target.parent)
