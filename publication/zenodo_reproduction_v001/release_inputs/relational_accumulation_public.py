"""Public-release adapter for the exact relational-accumulation source.

The archive retains the byte-exact repository source beside this adapter as
``relational_accumulation_exact.py``.  This module authenticates that source,
loads it, redirects its repository root to the extracted capsule, and changes
only the two cache-manifest checks needed for the path-neutral L08/L10 public
projections.  The projections separately carry the SHA-256 pins of the raw
source manifests; all scientific values and every other dependency remain
under the exact source implementation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
from types import MappingProxyType


_EXACT_SOURCE_SHA256 = (
    "d04ebd84c7dc98bd9d6aafae6c97aaf6430e994797138762be2cc87dcfb8bba4"
)
_EXACT_SOURCE = Path(__file__).resolve().with_name(
    "relational_accumulation_exact.py"
)
try:
    _exact_bytes = _EXACT_SOURCE.read_bytes()
except OSError as exc:  # pragma: no cover - exercised by extracted verifier
    raise ImportError(f"exact relational-accumulation source is unreadable: {exc}") from exc
if hashlib.sha256(_exact_bytes).hexdigest() != _EXACT_SOURCE_SHA256:
    raise ImportError("exact relational-accumulation source SHA-256 mismatch")

# Execute the authenticated exact source in this module namespace.  Its
# functions therefore retain normal module-global mutation semantics used by
# the hostile validator (for example temporary replacements of ``_load_json``
# and ``_root_path``).
exec(compile(_exact_bytes, str(_EXACT_SOURCE), "exec"), globals(), globals())

# ``.../urm/model/this_file.py`` -> extracted URM dependency root.
_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

_PUBLIC_MANIFESTS = MappingProxyType({
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "CACHE_PAYLOADS_V012/L8/CACHE_MANIFEST.json"
    ): MappingProxyType({
        "L": 8,
        "public_sha256":
            "2fa815948b0730fec9062bdb376ad62a668e79d0b76d3698f269b14c465ecbf6",
        "selected_file_count": 8,
        "selected_file_bytes": 63488,
    }),
    (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "CACHE_PAYLOADS_V012/L10/CACHE_MANIFEST.json"
    ): MappingProxyType({
        "L": 10,
        "public_sha256":
            "16fa8a670f41e718c62f0e42f0d9dcca50c22c8349edea0ec423415328b78977",
        "selected_file_count": 12,
        "selected_file_bytes": 1045464,
    }),
})


def _verify_progression_source() -> tuple[str, str]:
    """Authenticate exact inputs plus the two minimal public projections."""

    for relative, expected_source_digest in _PROGRESSION_INPUT_PINS:
        path = _root_path(relative)
        try:
            if not path.is_file() or path.is_symlink():
                _refuse(
                    "progression input is absent, non-file, or symlinked: "
                    f"{relative}"
                )
            raw = path.read_bytes()
        except OSError as exc:
            _refuse(f"progression input is unreadable: {relative}: {exc}")
        observed = hashlib.sha256(raw).hexdigest()
        projection = _PUBLIC_MANIFESTS.get(relative)
        if projection is None:
            if observed != expected_source_digest:
                _refuse(f"progression input SHA-256 mismatch: {relative}")
            continue
        if observed != projection["public_sha256"]:
            _refuse(f"public progression manifest SHA-256 mismatch: {relative}")
        try:
            manifest = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            _refuse(
                f"public progression manifest is not readable JSON: {relative}: {exc}"
            )
        public = manifest.get("public_projection") if isinstance(manifest, dict) else None
        required_fields = {
            "removed_source_leak_fields",
            "schema",
            "selected_file_bytes",
            "selected_file_count",
            "selection",
            "source_manifest_sha256",
        }
        if (
            not isinstance(public, dict)
            or set(public) != required_fields
            or public.get("schema") != "WAC_LOWER_LADDER_CACHE_PROJECTION_V001"
            or public.get("source_manifest_sha256") != expected_source_digest
            or public.get("selected_file_count") != projection["selected_file_count"]
            or public.get("selected_file_bytes") != projection["selected_file_bytes"]
            or public.get("removed_source_leak_fields") != ["/canonical_cache_root"]
            or manifest.get("L") != projection["L"]
            or manifest.get("canonical_cache_root")
            != str(PurePosixPath(relative).parent)
        ):
            _refuse(
                "public progression manifest does not authenticate its exact "
                f"source pin: {relative}"
            )
        files = manifest.get("files")
        if (
            not isinstance(files, list)
            or len(files) != projection["selected_file_count"]
            or sum(
                record.get("bytes", -1)
                for record in files
                if isinstance(record, dict)
            ) != projection["selected_file_bytes"]
        ):
            _refuse(f"public progression manifest ledger changed: {relative}")

    try:
        result = subprocess.run(
            [sys.executable, str(_root_path(_PROGRESSION_SOURCE_PATH))],
            cwd=_REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        _refuse(f"progression extraction could not execute: {exc}")
    if result.returncode != 0:
        _refuse(
            "progression extraction failed: "
            + (result.stderr.strip() or f"exit {result.returncode}")
        )
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    expected = ("L08: 0.0244800482", "L10: 0.0687369678")
    if lines != expected:
        _refuse(f"progression extraction output changed: {lines!r}")
    return expected
