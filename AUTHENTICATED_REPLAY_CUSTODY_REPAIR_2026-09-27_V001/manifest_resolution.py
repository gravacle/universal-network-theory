"""Explicit path bases for the seven historically pinned AURFT manifests.

No hash-based search or root/local fallback is permitted. A root README is not
a candidate for a manifest explicitly declared local. Unregistered, mixed-base,
duplicate, traversing, symlinked, missing, or hash-disagreeing custody is refused.
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path, PurePosixPath
import re
from types import MappingProxyType


MANIFEST_BASES = MappingProxyType({
    "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/MANIFEST.sha256": "local",
    "LANE_RFT_RECORD_TO_CTS_NONIMPLICATION_V001/MANIFEST.sha256": "local",
    "LANE_RFT_STANDARD_CAUSAL_URFT_SCOPE_V001/MANIFEST.sha256": "local",
    "LANE_RFT_FINITE_HAMILTONIAN_BOUNDARY_CLOSURE_V001/MANIFEST.sha256": "local",
    "LANE_RFT_CAUCHY_TIME_SLICE_ONTIC_COVERAGE_V001/MANIFEST.sha256": "root",
    "LANE_RFT_FINITE_MISSION_FAITHFUL_ADMISSION_V001/MANIFEST.sha256": "root",
    "LANE_RFT_UDCL_CONDITIONAL_UNIVERSAL_COVERAGE_V001/MANIFEST.sha256": "root",
})


class CustodyRefusal(ValueError):
    """The finite declared manifest schema or pinned file cannot be satisfied."""


def _confined_file(root: Path, path: Path) -> Path:
    try:
        suffix = path.relative_to(root)
    except ValueError as exc:
        raise CustodyRefusal("path outside the declared root") from exc
    current = root
    for component in suffix.parts:
        current /= component
        if current.is_symlink():
            raise CustodyRefusal(f"symlinked custody: {path}")
    if not path.is_file() or root not in path.resolve().parents:
        raise CustodyRefusal(f"missing or escaping custody: {path}")
    return path


def resolve_manifest_item(root: Path, manifest: Path, relative: str) -> Path:
    root = root.resolve()
    try:
        manifest_name = manifest.relative_to(root).as_posix()
    except ValueError as exc:
        raise CustodyRefusal("manifest outside the declared root") from exc
    scope = MANIFEST_BASES.get(manifest_name)
    if scope is None:
        raise CustodyRefusal(f"manifest has no declared base: {manifest_name}")
    _confined_file(root, manifest)
    entries = {}
    targets = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})\s+(.+)", line)
        if match is None:
            raise CustodyRefusal("malformed manifest entry")
        expected, name = match.groups()
        parts = PurePosixPath(name)
        if (parts.is_absolute() or ".." in parts.parts or "\\" in name
                or parts.as_posix() != name or name in entries):
            raise CustodyRefusal(f"ambiguous, duplicate, or unsafe manifest entry: {name}")
        if scope == "local":
            if len(parts.parts) != 1:
                raise CustodyRefusal("local schema accepts packet-local filenames only")
            candidate = manifest.parent / name
        else:
            prefix = manifest.parent.relative_to(root).as_posix() + "/"
            if not name.startswith(prefix):
                raise CustodyRefusal("root schema requires an explicit owning-packet prefix")
            candidate = root / name
        if candidate in targets:
            raise CustodyRefusal("multiple entries resolve to one candidate")
        targets.add(candidate)
        entries[name] = (candidate, expected)
    if relative not in entries:
        raise CustodyRefusal(f"item is not uniquely declared: {relative}")
    candidate, expected = entries[relative]
    _confined_file(root, candidate)
    if sha256(candidate.read_bytes()).hexdigest() != expected:
        raise CustodyRefusal(f"hash disagreement at the declared location: {candidate}")
    return candidate
