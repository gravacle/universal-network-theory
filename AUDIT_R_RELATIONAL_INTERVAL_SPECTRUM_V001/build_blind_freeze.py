#!/usr/bin/env python3
"""Build the future runnable blind freeze, or fail before writing it."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


EXPECTED_SCHEMA = "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001"
EXPECTED_STATUS = "PASS_RELATIONAL_ACCUMULATION_L4_L12__SPECTRUM_MANIFEST_READY"
EXPECTED_PROTOCOL_SHA256 = "d545a4dd0925d4ae47c1231f4f7632c4cdfef14d0864af292f19fd9f6a708d95"
EXPECTED_SIZES = (4, 6, 8, 10, 12)
PLAN_SCHEMA = "BLIND_RELATIONAL_INTERVAL_SECTOR_PLAN_V001"


class Refusal(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_pinned(path: Path, claimed: str, label: str) -> dict[str, object]:
    if not path.is_file():
        raise Refusal(f"{label} does not exist as a regular file")
    if len(claimed) != 64 or any(ch not in "0123456789abcdef" for ch in claimed):
        raise Refusal(f"{label} SHA-256 must be lowercase hexadecimal")
    actual = sha256_file(path)
    if actual != claimed:
        raise Refusal(f"{label} SHA-256 mismatch")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise Refusal(f"{label} must be a JSON object")
    return data


def reduced_pair(value: object, label: str) -> tuple[int, int]:
    if (
        not isinstance(value, list)
        or len(value) != 2
        or any(isinstance(item, bool) or not isinstance(item, int) for item in value)
    ):
        raise Refusal(f"{label} must be a literal integer pair")
    numerator, denominator = value
    if denominator <= 0 or __import__("math").gcd(numerator, denominator) != 1:
        raise Refusal(f"{label} is not a reduced rational pair")
    return numerator, denominator


def reconstruct_plan(manifest: dict[str, object], manifest_hash: str) -> dict[str, object]:
    if manifest.get("schema") != EXPECTED_SCHEMA or manifest.get("status") != EXPECTED_STATUS:
        raise Refusal("future accumulation manifest is not authenticated and ready")
    if manifest.get("scalable_accumulation_protocol_sha256") != EXPECTED_PROTOCOL_SHA256:
        raise Refusal("accumulation protocol hash mismatch")
    histories = manifest.get("histories")
    atoms = manifest.get("atoms")
    if not isinstance(histories, dict) or set(histories) != {str(L) for L in EXPECTED_SIZES}:
        raise Refusal("manifest history size census is incomplete")
    if not isinstance(atoms, list) or not atoms:
        raise Refusal("manifest atom partition is absent")
    positive: set[tuple[int, int]] = set()
    zero_atoms: list[dict[str, object]] = []
    atom_rows: list[dict[str, object]] = []
    seen_atom_ids: set[str] = set()
    previous_right: tuple[int, int] | None = None
    for ordinal, atom in enumerate(atoms):
        if not isinstance(atom, dict):
            raise Refusal("manifest atom is not an object")
        atom_id = atom.get("atom_id")
        if not isinstance(atom_id, str) or not atom_id or atom_id in seen_atom_ids:
            raise Refusal("atom IDs must be unique nonempty strings")
        seen_atom_ids.add(atom_id)
        interval = atom.get("density_interval")
        if not isinstance(interval, list) or len(interval) != 2:
            raise Refusal("atom density interval must contain two rational endpoints")
        left = reduced_pair(interval[0], f"{atom_id}.left")
        right = reduced_pair(interval[1], f"{atom_id}.right")
        if left[0] * right[1] >= right[0] * left[1]:
            raise Refusal("atom interval is not positive-width")
        if previous_right is not None and previous_right[0] * left[1] != left[0] * previous_right[1]:
            raise Refusal("atom partition is reordered or has a gap")
        previous_right = right
        q_by_L = atom.get("q_by_L")
        if not isinstance(q_by_L, dict) or set(q_by_L) != {str(L) for L in EXPECTED_SIZES}:
            raise Refusal("atom q_by_L census is incomplete")
        normalized: dict[str, int] = {}
        for L in EXPECTED_SIZES:
            q = q_by_L[str(L)]
            if isinstance(q, bool) or not isinstance(q, int) or not 0 <= q <= L:
                raise Refusal("atom sector charge lies outside frozen half-sector")
            normalized[str(L)] = q
            if q == 0:
                zero_atoms.append({"atom_id": atom_id, "L": L, "q": 0})
            else:
                positive.add((L, q))
        atom_rows.append(
            {
                "ordinal": ordinal,
                "atom_id": atom_id,
                "density_interval": interval,
                "q_by_L": normalized,
            }
        )
    return {
        "schema": PLAN_SCHEMA,
        "accumulation_manifest_sha256": manifest_hash,
        "positive_q_sector_plan": [
            {"L": L, "q": q, "rho": [q, 2 * L]} for L, q in sorted(positive)
        ],
        "zero_response_atom_plan": sorted(zero_atoms, key=lambda item: (item["atom_id"], item["L"])),
        "atom_plan": atom_rows,
    }


def repo_relative(repo_root: Path, path: Path) -> str:
    root = repo_root.resolve()
    resolved = path.resolve(strict=True)
    if root not in resolved.parents or not resolved.is_file():
        raise Refusal(f"freeze dependency is outside repository: {path}")
    return resolved.relative_to(root).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--sector-plan", type=Path, required=True)
    parser.add_argument("--sector-plan-sha256", required=True)
    parser.add_argument("--pre-output-freeze", type=Path, required=True)
    parser.add_argument("--pre-output-freeze-sha256", required=True)
    parser.add_argument("--methodology", type=Path, required=True)
    parser.add_argument("--implementation", type=Path, required=True)
    parser.add_argument("--builder", type=Path, required=True)
    parser.add_argument("--self-test", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = load_pinned(args.manifest, args.manifest_sha256, "accumulation manifest")
        expected_plan = reconstruct_plan(manifest, args.manifest_sha256)
        supplied_plan = load_pinned(args.sector_plan, args.sector_plan_sha256, "sector plan")
        if supplied_plan != expected_plan:
            raise Refusal("sector plan is not the exact deterministic manifest reconstruction")
        pre_output = load_pinned(
            args.pre_output_freeze,
            args.pre_output_freeze_sha256,
            "pre-output method freeze",
        )
        if pre_output.get("status") != "BLIND_METHOD_AND_CODE_FROZEN__AWAITING_MANIFEST":
            raise Refusal("pre-output method freeze does not carry the frozen status")
        dependencies = {}
        for name, path in (
            ("methodology", args.methodology),
            ("implementation", args.implementation),
            ("builder", args.builder),
            ("self_test", args.self_test),
        ):
            relative = repo_relative(args.repo_root, path)
            dependencies[name] = {"path": relative, "sha256": sha256_file(path)}
        frozen_files = pre_output.get("files")
        if not isinstance(frozen_files, dict):
            raise Refusal("pre-output freeze file map is absent")
        for name, dependency in dependencies.items():
            if name == "self_test":
                continue
            filename = Path(dependency["path"]).name
            if frozen_files.get(filename) != dependency["sha256"]:
                raise Refusal(f"{name} differs from the pre-output method freeze")
        self_test_result = json.loads(args.self_test.read_text(encoding="utf-8"))
        if (
            not isinstance(self_test_result, dict)
            or self_test_result.get("status") != "PASS_5_OF_5__NO_PHYSICAL_SPECTRUM_EXECUTED"
            or self_test_result.get("physical_spectrum_executed") is not False
            or not isinstance(self_test_result.get("tests"), dict)
            or self_test_result["tests"].get("pre_output_freeze", {}).get("freeze_sha256")
            != args.pre_output_freeze_sha256
        ):
            raise Refusal("self-test result does not pass against the supplied pre-output freeze")
        output = args.output.resolve()
        root = args.repo_root.resolve()
        if root not in output.parents or output.exists():
            raise Refusal("output must be a new repository-local file")
        freeze = {
            "schema": "BLIND_RELATIONAL_INTERVAL_SPECTRUM_FREEZE_V001",
            "status": "BLIND_METHOD_FROZEN_BEFORE_TARGET_SPECTRUM",
            "accumulation_manifest_path": repo_relative(args.repo_root, args.manifest),
            "accumulation_manifest_sha256": args.manifest_sha256,
            "sector_plan_path": repo_relative(args.repo_root, args.sector_plan),
            "sector_plan_sha256": args.sector_plan_sha256,
            "pre_output_method_freeze_path": repo_relative(args.repo_root, args.pre_output_freeze),
            "pre_output_method_freeze_sha256": args.pre_output_freeze_sha256,
            "positive_q_sector_plan": supplied_plan["positive_q_sector_plan"],
            "zero_response_atom_plan": supplied_plan["zero_response_atom_plan"],
            "atom_plan": supplied_plan["atom_plan"],
            "methodology_path": dependencies["methodology"]["path"],
            "methodology_sha256": dependencies["methodology"]["sha256"],
            "implementation_path": dependencies["implementation"]["path"],
            "implementation_sha256": dependencies["implementation"]["sha256"],
            "builder_path": dependencies["builder"]["path"],
            "builder_sha256": dependencies["builder"]["sha256"],
            "self_test_result_path": dependencies["self_test"]["path"],
            "self_test_result_sha256": dependencies["self_test"]["sha256"],
            "guards": {
                "retained_vectors_max": 128,
                "matvecs_max": 2000,
                "wall_seconds_max": 10800,
                "address_space_bytes_max": 6442450944,
                "checkpoint_dimensions": [16, 32, 64, 96, 128],
            },
            "custody_declarations": {
                "independently_implemented": True,
                "target_code_imported": False,
                "target_matrices_imported": False,
                "method_and_code_frozen_before_target_spectrum": True,
            },
            "claim_boundary": "FINITE_STRUCTURAL_SCREEN_ONLY__NO_CONTINUUM_OR_GRAVITY_CLAIM",
        }
        payload = json.dumps(freeze, indent=2, sort_keys=True, allow_nan=False) + "\n"
        # Inputs and output nonexistence are all checked before this atomic create.
        descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
    except (Refusal, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
