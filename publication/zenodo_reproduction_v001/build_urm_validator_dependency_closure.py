#!/usr/bin/env python3
"""Build the exact, compact dependency closure for the focused URM validators.

This is an inventory tool, not a scientific validator.  It follows the exact
hash-pinned custody surfaces that the validators read, records their bytes and
repository-relative locations, and refuses if any declared hash no longer
matches.  It never calls a numerical solver or a validator ``main`` function.
"""

from __future__ import annotations

import argparse
import ast
from collections import defaultdict
import hashlib
import importlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any, Iterable


SCHEMA = "wac_urm_validator_dependency_closure_v001"
DEFAULT_SPEC_NAME = "urm_validator_dependency_closure.json"
ARCHIVE_DEPENDENCY_ROOT = "urm"
SHA256 = re.compile(r"[0-9a-f]{64}")
KNOWN_STDLIB_IMPORTS = {
    "__future__",
    "argparse",
    "ast",
    "collections",
    "dataclasses",
    "decimal",
    "fractions",
    "hashlib",
    "importlib",
    "inspect",
    "json",
    "pathlib",
    "posixpath",
    "re",
    "shutil",
    "subprocess",
    "sys",
    "tempfile",
    "types",
    "typing",
}

VALIDATORS = {
    "relational_accumulation": {
        "entrypoint": "model/validate_relational_accumulation.py",
        "model_sources": (
            "model/relational_accumulation.py",
            "model/project_model.py",
            "model/grounded.py",
        ),
        "urm_methods": (
            "relational_accumulation",
            "relational_accumulation_certificate",
        ),
    },
}

EXPECTED_TOP_LEVEL_IMPORTS = {
    "model/validate_relational_accumulation.py": {
        "local": {"relational_accumulation", "project_model"},
        "external": set(),
    },
    "model/relational_accumulation.py": {"local": set(), "external": set()},
    "model/project_model.py": {"local": {"grounded"}, "external": {"numpy"}},
    "model/grounded.py": {"local": set(), "external": {"numpy"}},
}

RUNTIME_ARTIFACTS: tuple[dict[str, str], ...] = ()

GATE_LOW_RESULT = (
    "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001/RESULT.json",
    "ebd522411a0e7f67e37d5023fbdea01bc63bdd796ca23020b0d749b414146a05",
)
GATE_INDEXES = (
    (
        "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/"
        "RUN_V002_L12_V003R1_STAGE6R2/SPECTRUM_INDEX.json",
        "157e9ae1a54a77dfeef51287dd0d479bc4126a3181388ea2a4bafc22728de749",
    ),
    (
        "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_COMPATIBILITY_V001/"
        "RUN_V002_L12_V003R1_STAGE6R2/SPECTRUM_INDEX.json",
        "f57488d2286df964599885d42556f1ea509ca41ab69f46dfaa78125efcf66994",
    ),
)
GATE_INDEX_ROW_KEYS = (
    "10:3",
    "10:4",
    "10:5",
    "10:6",
    "12:4",
    "12:5",
    "12:6",
    "12:7",
)
PROGRESSION_CACHE_LAYOUT = (
    (8, 7, range(4, 8)),
    (10, 9, range(4, 10)),
)
PUBLIC_PROJECTION_STATUS = (
    "PUBLIC_PROJECTION_AUTHENTICATES_EXACT_SOURCE_PIN__"
    "RAW_PATH_BEARING_BYTES_OMITTED"
)
PUBLIC_PROJECTIONS = (
    {
        "exact_repository_path": (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            "CACHE_PAYLOADS_V012/L8/CACHE_MANIFEST.json"
        ),
        "public_substitute_repository_path": (
            "publication/zenodo_reproduction_v001/release_inputs/"
            "L08_CACHE_MANIFEST_MINIMAL_PUBLIC.json"
        ),
        "projection_kind": "path_neutral_cache_manifest",
        "path_rewrites": 1,
    },
    {
        "exact_repository_path": (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            "CACHE_PAYLOADS_V012/L10/CACHE_MANIFEST.json"
        ),
        "public_substitute_repository_path": (
            "publication/zenodo_reproduction_v001/release_inputs/"
            "L10_CACHE_MANIFEST_MINIMAL_PUBLIC.json"
        ),
        "projection_kind": "path_neutral_cache_manifest",
        "path_rewrites": 1,
    },
    {
        "exact_repository_path": "model/relational_accumulation.py",
        "public_substitute_repository_path": (
            "publication/zenodo_reproduction_v001/release_inputs/"
            "relational_accumulation_public.py"
        ),
        "projection_kind": "public_manifest_authentication_adapter",
        "path_rewrites": 1,
    },
)


class ClosureError(RuntimeError):
    """The dependency inventory is incomplete, ambiguous, or hash-inconsistent."""


def _safe_relative(value: str) -> str:
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or "." in path.parts
        or ".." in path.parts
        or "\\" in value
    ):
        raise ClosureError(f"unsafe repository-relative path: {value!r}")
    normalized = path.as_posix()
    if normalized != value:
        raise ClosureError(f"non-canonical repository-relative path: {value!r}")
    return normalized


def _file(repo_root: Path, relative: str) -> Path:
    relative = _safe_relative(relative)
    path = repo_root.joinpath(*PurePosixPath(relative).parts)
    if path.is_symlink() or not path.is_file():
        raise ClosureError(f"dependency is absent, non-file, or symlinked: {relative}")
    return path


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_hash(repo_root: Path, relative: str, expected: str) -> None:
    if SHA256.fullmatch(expected) is None:
        raise ClosureError(f"invalid expected SHA-256 for {relative}: {expected!r}")
    observed = _digest(_file(repo_root, relative))
    if observed != expected:
        raise ClosureError(
            f"hash mismatch for {relative}: expected {expected}, observed {observed}"
        )


def _top_level_imports(path: Path) -> tuple[set[str], set[str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.as_posix())
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".", 1)[0])
    local_modules = {Path(item).stem for item in EXPECTED_TOP_LEVEL_IMPORTS}
    stdlib = KNOWN_STDLIB_IMPORTS
    local = names & local_modules
    external = names - local - stdlib
    return local, external


def _urm_calls(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.as_posix())
    return {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "URM"
    }


def _assert_import_surface(repo_root: Path) -> None:
    for relative, expected in EXPECTED_TOP_LEVEL_IMPORTS.items():
        observed_local, observed_external = _top_level_imports(_file(repo_root, relative))
        if observed_local != expected["local"] or observed_external != expected["external"]:
            raise ClosureError(
                f"top-level import surface changed for {relative}: "
                f"local={sorted(observed_local)}, external={sorted(observed_external)}"
            )
    for validator_id, row in VALIDATORS.items():
        observed = _urm_calls(_file(repo_root, row["entrypoint"]))
        expected = set(row["urm_methods"])
        if observed != expected:
            raise ClosureError(
                f"URM delegation surface changed for {validator_id}: {sorted(observed)}"
            )


def _import_relational_module(repo_root: Path) -> Any:
    model_path = (repo_root / "model").as_posix()
    sys.path.insert(0, model_path)
    try:
        return importlib.import_module("relational_accumulation")
    finally:
        if sys.path[0] == model_path:
            sys.path.pop(0)


def _relational_dependencies(repo_root: Path, ra: Any) -> set[str]:
    """Return the exact governing ARGER Gate closure and native Gate inputs."""

    paths: set[str] = set()

    def add(relative: str, expected: str) -> str:
        relative = _safe_relative(relative)
        _assert_hash(repo_root, relative, expected)
        paths.add(relative)
        return relative

    for pin in ra._GOVERNING_ARTIFACTS:
        add(pin.path, pin.sha256)
    for pin in ra._TEXT_ARTIFACTS:
        add(pin.path, pin.sha256)
    for relative, expected in ra._PROGRESSION_INPUT_PINS:
        add(relative, expected)

    # The authenticated progression program resolves its compact admission and
    # lineage arrays through the two pinned cache manifests.  They are runtime
    # dependencies even though their hashes live in those manifests rather
    # than in the calling model module, so traverse that exact finite surface.
    for length, prefix, q_values in PROGRESSION_CACHE_LAYOUT:
        manifest_relative = (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            f"CACHE_PAYLOADS_V012/L{length}/CACHE_MANIFEST.json"
        )
        try:
            manifest = json.loads(
                _file(repo_root, manifest_relative).read_text(encoding="utf-8")
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ClosureError(
                f"cannot read progression cache manifest {manifest_relative}: {exc}"
            ) from exc
        records = manifest.get("files") if isinstance(manifest, dict) else None
        if not isinstance(records, list):
            raise ClosureError(
                f"progression cache manifest has no file ledger: {manifest_relative}"
            )
        by_name: dict[str, dict[str, Any]] = {}
        for record in records:
            if not isinstance(record, dict) or not isinstance(record.get("path"), str):
                raise ClosureError(
                    f"malformed progression cache record: {manifest_relative}"
                )
            name = record["path"]
            if name in by_name:
                raise ClosureError(
                    f"duplicate progression cache record {name}: {manifest_relative}"
                )
            by_name[name] = record
        manifest_parent = PurePosixPath(manifest_relative).parent.as_posix()
        for q in q_values:
            for name in (
                f"admission_n_{prefix:02d}_q_{q:02d}_blank.i32",
                f"lineage_n_{prefix:02d}_q_{q:02d}_words.u32",
            ):
                record = by_name.get(name)
                if record is None or not isinstance(record.get("sha256"), str):
                    raise ClosureError(
                        f"progression cache dependency absent: {manifest_relative}:{name}"
                    )
                add(f"{manifest_parent}/{name}", record["sha256"])

    add(*GATE_LOW_RESULT)
    native_prefixes = tuple(
        f"{PurePosixPath(relative).parent.as_posix()}/"
        for relative, _expected in GATE_INDEXES
    )
    for index_relative, index_sha256 in GATE_INDEXES:
        add(index_relative, index_sha256)
        try:
            index = json.loads(_file(repo_root, index_relative).read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ClosureError(f"cannot read native Gate index {index_relative}: {exc}") from exc
        rows = index.get("rows") if isinstance(index, dict) else None
        if not isinstance(rows, dict):
            raise ClosureError(f"native Gate index has no row map: {index_relative}")
        for key in GATE_INDEX_ROW_KEYS:
            row = rows.get(key)
            if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
                raise ClosureError(
                    f"native Gate index row changed at {index_relative}:{key}"
                )
            add(row["path"], row["sha256"])

    for relative in paths:
        lowered = relative.lower()
        stage6_named_native_input = (
            "stage6" in lowered
            and relative.startswith(native_prefixes)
            and (
                relative.endswith("/SPECTRUM_INDEX.json")
                or "/RAW/SECTOR_" in relative
            )
        )
        if "stage6" in lowered and not stage6_named_native_input:
            raise ClosureError(
                f"retired Stage-6 artifact entered focused closure: {relative}"
            )
        if any(
            marker in lowered
            for marker in (
                "record_flow",
                "record-flow",
                "connected_record_trajectory_l4_l14",
                "l14_targeted_scout",
            )
        ):
            raise ClosureError(f"retired artifact entered focused closure: {relative}")
    return paths


def _kind(relative: str, source_paths: set[str]) -> str:
    if relative in source_paths:
        if Path(relative).name.startswith("validate_"):
            return "validator_source"
        return "model_source"
    name = Path(relative).name
    if name == "SEAL.sha256":
        return "custody_seal"
    if name in {"MANIFEST.sha256", "DEPENDENCIES.sha256", "AUDITED_TARGETS.sha256"}:
        return "custody_hash_list"
    return "custody_data"


def _entry(repo_root: Path, relative: str, required_by: Iterable[str], kind: str) -> dict[str, Any]:
    path = _file(repo_root, relative)
    return {
        "archive_path": f"{ARCHIVE_DEPENDENCY_ROOT}/{relative}",
        "kind": kind,
        "repository_path": relative,
        "required_by": sorted(set(required_by)),
        "sha256": _digest(path),
        "size_bytes": path.stat().st_size,
    }


def _public_projection_conflicts(
    repo_root: Path,
    entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Authenticate the three narrow public substitutions.

    The repository closure remains pinned to the original bytes.  The public
    archive replaces the two raw, path-bearing manifests and installs a small
    adapter at the original model-module path.  The byte-exact model source is
    separately retained in the archive and authenticated by that adapter.
    """

    by_repository = {row["repository_path"]: row for row in entries}
    conflicts: list[dict[str, Any]] = []
    for projection in PUBLIC_PROJECTIONS:
        exact_relative = projection["exact_repository_path"]
        exact = by_repository.get(exact_relative)
        if exact is None:
            raise ClosureError(
                f"public projection exact dependency is absent: {exact_relative}"
            )
        public_relative = projection["public_substitute_repository_path"]
        public_path = _file(repo_root, public_relative)
        public_raw = public_path.read_bytes()
        try:
            public_text = public_raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ClosureError(
                f"public projection is not UTF-8: {public_relative}"
            ) from exc
        if re.search(r"/(?:Users|home|root|private/tmp)/", public_text):
            raise ClosureError(
                f"public projection contains a private absolute path: {public_relative}"
            )

        if projection["projection_kind"] == "path_neutral_cache_manifest":
            try:
                public = json.loads(public_text)
                exact_manifest = json.loads(
                    _file(repo_root, exact_relative).read_text(encoding="utf-8")
                )
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ClosureError(
                    f"cannot parse cache-manifest projection {public_relative}: {exc}"
                ) from exc
            metadata = public.get("public_projection") if isinstance(public, dict) else None
            if (
                not isinstance(metadata, dict)
                or metadata.get("schema")
                != "WAC_LOWER_LADDER_CACHE_PROJECTION_V001"
                or metadata.get("source_manifest_sha256") != exact["sha256"]
                or metadata.get("removed_source_leak_fields")
                != ["/canonical_cache_root"]
                or public.get("canonical_cache_root")
                != PurePosixPath(exact_relative).parent.as_posix()
            ):
                raise ClosureError(
                    f"cache projection does not authenticate exact source: {public_relative}"
                )
            exact_records = {
                row.get("path"): row
                for row in exact_manifest.get("files", [])
                if isinstance(row, dict) and isinstance(row.get("path"), str)
            }
            public_records = public.get("files")
            if not isinstance(public_records, list) or any(
                not isinstance(row, dict)
                or exact_records.get(row.get("path")) != row
                for row in public_records
            ):
                raise ClosureError(
                    f"cache projection file ledger is not an exact subset: {public_relative}"
                )
            if (
                metadata.get("selected_file_count") != len(public_records)
                or metadata.get("selected_file_bytes")
                != sum(int(row["bytes"]) for row in public_records)
            ):
                raise ClosureError(
                    f"cache projection census changed: {public_relative}"
                )
        else:
            exact_sha_marker = f'"{exact["sha256"]}"'
            manifest_conflicts = [
                row for row in conflicts
                if row["exact_repository_path"].endswith("CACHE_MANIFEST.json")
            ]
            if exact_sha_marker not in public_text or any(
                f'"{row["public_substitute_sha256"]}"' not in public_text
                for row in manifest_conflicts
            ):
                raise ClosureError(
                    "public relational adapter does not pin the exact source and "
                    "both manifest projections"
                )
            try:
                compile(public_text, public_relative, "exec")
            except SyntaxError as exc:
                raise ClosureError(
                    f"public relational adapter is not valid Python: {exc}"
                ) from exc

        conflicts.append(
            {
                "affected_validators": exact["required_by"],
                "exact_archive_path": exact["archive_path"],
                "exact_repository_path": exact_relative,
                "exact_sha256": exact["sha256"],
                "exact_size_bytes": exact["size_bytes"],
                "existing_public_archive_path": exact["archive_path"],
                "path_rewrites": projection["path_rewrites"],
                "public_substitute_repository_path": public_relative,
                "public_substitute_sha256": hashlib.sha256(public_raw).hexdigest(),
                "public_substitute_size_bytes": len(public_raw),
                "status": PUBLIC_PROJECTION_STATUS,
            }
        )
    return sorted(conflicts, key=lambda row: row["exact_repository_path"])


def build_spec(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    _assert_import_surface(repo_root)
    ra = _import_relational_module(repo_root)
    relational_data = _relational_dependencies(repo_root, ra)

    per_validator: dict[str, set[str]] = {}
    for validator_id, metadata in VALIDATORS.items():
        per_validator[validator_id] = {
            metadata["entrypoint"],
            *metadata["model_sources"],
        }
    per_validator["relational_accumulation"].update(relational_data)

    consumers: dict[str, set[str]] = defaultdict(set)
    for validator_id, paths in per_validator.items():
        for relative in paths:
            consumers[relative].add(validator_id)

    source_paths = {
        row["entrypoint"] for row in VALIDATORS.values()
    } | {
        relative
        for row in VALIDATORS.values()
        for relative in row["model_sources"]
    }
    entries = [
        _entry(repo_root, relative, consumers[relative], _kind(relative, source_paths))
        for relative in sorted(consumers)
    ]

    runtime_rows = []
    for template in RUNTIME_ARTIFACTS:
        row = dict(template)
        _assert_hash(repo_root, row["repository_path"], row["sha256"])
        row["required_by"] = sorted(VALIDATORS)
        row["size_bytes"] = _file(repo_root, row["repository_path"]).stat().st_size
        runtime_rows.append(row)

    validator_rows = []
    for validator_id in sorted(VALIDATORS):
        paths = per_validator[validator_id]
        validator_rows.append(
            {
                "dependency_count": len(paths),
                "dependency_total_bytes": sum(
                    _file(repo_root, relative).stat().st_size for relative in paths
                ),
                "entrypoint": f"{ARCHIVE_DEPENDENCY_ROOT}/{VALIDATORS[validator_id]['entrypoint']}",
                "id": validator_id,
                "repository_entrypoint": VALIDATORS[validator_id]["entrypoint"],
                "urm_methods_exercised": list(VALIDATORS[validator_id]["urm_methods"]),
            }
        )

    conflicts = _public_projection_conflicts(repo_root, entries)
    total_bytes = sum(row["size_bytes"] for row in entries)
    runtime_total = sum(row["size_bytes"] for row in runtime_rows)
    return {
        "archive_dependency_root": ARCHIVE_DEPENDENCY_ROOT,
        "closure_entry_count": len(entries),
        "closure_total_bytes": total_bytes,
        "entries": entries,
        "external_imports": ["numpy"],
        "generation_policy": (
            "HASH_PINNED_REPOSITORY_EXACT_CLOSURE__NO_NUMERICAL_VALIDATOR_OR_"
            "PHYSICS_EXECUTION"
        ),
        "runtime_artifact_count": len(runtime_rows),
        "runtime_artifact_total_bytes": runtime_total,
        "runtime_artifacts": runtime_rows,
        "sanitized_conflict_count": len(conflicts),
        "sanitized_conflicts": conflicts,
        "schema": SCHEMA,
        "validators": validator_rows,
    }


def canonical_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().with_name(DEFAULT_SPEC_NAME),
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="refuse unless the existing output is byte-for-byte current",
    )
    args = parser.parse_args(argv)
    payload = canonical_bytes(build_spec(args.repo_root))
    if args.check:
        try:
            observed = args.output.read_bytes()
        except OSError as exc:
            raise ClosureError(f"cannot read closure spec {args.output}: {exc}") from exc
        if observed != payload:
            raise ClosureError(f"dependency closure spec is stale: {args.output}")
        print(f"URM_VALIDATOR_CLOSURE_SPEC_CURRENT sha256={hashlib.sha256(payload).hexdigest()}")
        return 0
    args.output.write_bytes(payload)
    print(
        "URM_VALIDATOR_CLOSURE_SPEC_WRITTEN "
        f"path={args.output} bytes={len(payload)} sha256={hashlib.sha256(payload).hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ClosureError as exc:
        print(f"URM_VALIDATOR_CLOSURE_REFUSAL {exc}", file=sys.stderr)
        raise SystemExit(2)
