#!/usr/bin/env python3
"""Owner-once producer for the Stage 6 blind plan and runnable freeze."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import stat
import sys
from pathlib import Path

from contract_common import (
    FREEZE_SCHEMA,
    FREEZE_STATUS,
    PLAN_SCHEMA,
    Refusal,
    atomic_owner_once_json,
    demand,
    load_pinned_json,
    reconstruct_sector_plan,
    repo_file,
    repo_relative,
    sha256_file,
)


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
SOURCE_FREEZE_SCHEMA = "RELATIONAL_INTERVAL_BLIND_COMPATIBILITY_SOURCE_FREEZE_V001"
SOURCE_FREEZE_STATUS = "CANDIDATE_SOURCES_FROZEN__NO_PHYSICAL_SPECTRUM_EXECUTED"
DEPENDENCY_PINS = {
    "independent_blind_engine": {
        "path": "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001/independent_centerline.py",
        "sha256": "79aec7d5a773f8a7268ae98c6c343201a331e628274a3d225432059dee6b7fa7",
    },
    "independent_blind_method": {
        "path": "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001/METHODOLOGY.md",
        "sha256": "dbe28ec72e64cea10b9e974213277c284ffd20596877a06fdca4ee66ba4075a4",
    },
    "public_accumulation_protocol": {
        "path": "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md",
        "sha256": "d545a4dd0925d4ae47c1231f4f7632c4cdfef14d0864af292f19fd9f6a708d95",
    },
    "public_interval_protocol": {
        "path": "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/PROTOCOL.md",
        "sha256": "db39a11dfb738fe206a5c0b5b34ec5c90ff29385f1d52aa33181814ec162ebb6",
    },
    "sealed_low_spectra": {
        "path": "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001/RESULT.json",
        "sha256": "ebd522411a0e7f67e37d5023fbdea01bc63bdd796ca23020b0d749b414146a05",
    },
}
BLIND_CREDENTIAL_SCHEMA = "BLIND_INTERVAL_EXECUTION_CREDENTIAL_V001"
BLIND_CREDENTIAL_STATUS = "AUTHORIZED_AFTER_BLIND_METHOD_AND_SECTOR_FREEZE"
BLIND_BINDING_SCHEMA = "BLIND_INTERVAL_EXECUTION_BINDING_V001"
ORDERING_MODEL = "TRUSTED_HASH_PINNED_CODE_PATH__NO_WALL_CLOCK_ATTESTATION"
BLIND_RUN_TOKEN = "RUN_HASH_PINNED_BLIND_RELATIONAL_INTERVAL_SPECTRUM_V001"


def produce_plan(args: argparse.Namespace) -> None:
    plan = reconstruct_sector_plan(ROOT, args.manifest, args.manifest_sha256)
    atomic_owner_once_json(ROOT, args.output, plan)


def validate_source_freeze(
    source_freeze_path: Path, source_freeze_sha256: str
) -> dict[str, object]:
    freeze = load_pinned_json(
        source_freeze_path, source_freeze_sha256, "candidate source freeze"
    )
    demand(freeze.get("schema") == SOURCE_FREEZE_SCHEMA, "source freeze schema mismatch")
    demand(freeze.get("status") == SOURCE_FREEZE_STATUS, "source freeze status mismatch")
    demand(
        freeze.get("physical_spectrum_executed") is False,
        "source freeze does not certify the pre-output boundary",
    )
    files = freeze.get("files")
    demand(isinstance(files, dict), "source freeze file census absent")
    expected = {
        "blind_adjudication_entrypoint.py",
        "blind_contract_control.py",
        "blind_index_publisher.py",
        "blind_interval_worker.py",
        "contract_common.py",
        "METHODOLOGY.md",
        "test_stage6_compatibility.py",
    }
    demand(set(files) == expected, "source freeze file census mismatch")
    for name, digest in files.items():
        repo_file(
            ROOT,
            f"{PACKET.name}/{name}",
            digest,
            f"source freeze {name}",
        )
    dependencies = freeze.get("dependencies")
    demand(
        isinstance(dependencies, dict)
        and set(dependencies) == set(DEPENDENCY_PINS),
        "source dependency census mismatch",
    )
    for label, expected_binding in DEPENDENCY_PINS.items():
        binding = dependencies[label]
        demand(
            isinstance(binding, dict)
            and set(binding) == {"path", "sha256"}
            and binding == expected_binding,
            f"source dependency {label} binding mismatch",
        )
        repo_file(
            ROOT,
            binding.get("path"),
            binding.get("sha256"),
            f"source dependency {label}",
        )
    return freeze


def produce_freeze(args: argparse.Namespace) -> None:
    expected_plan = reconstruct_sector_plan(ROOT, args.manifest, args.manifest_sha256)
    supplied_plan = load_pinned_json(args.sector_plan, args.sector_plan_sha256, "sector plan")
    demand(supplied_plan == expected_plan, "sector plan is not the exact manifest reconstruction")
    demand(supplied_plan.get("schema") == PLAN_SCHEMA, "sector plan schema mismatch")
    source_freeze = validate_source_freeze(
        args.source_freeze, args.source_freeze_sha256
    )
    files = source_freeze["files"]
    assert isinstance(files, dict)
    worker_path = PACKET / "blind_interval_worker.py"
    publisher_path = PACKET / "blind_index_publisher.py"
    freeze = {
        "schema": FREEZE_SCHEMA,
        "status": FREEZE_STATUS,
        "manifest_sha256": args.manifest_sha256,
        "manifest_path": repo_relative(ROOT, args.manifest, "accumulation manifest"),
        "planned_sectors": supplied_plan["planned_sectors"],
        "sector_plan_path": repo_relative(ROOT, args.sector_plan, "sector plan"),
        "sector_plan_sha256": args.sector_plan_sha256,
        "source_freeze_path": repo_relative(
            ROOT, args.source_freeze, "candidate source freeze"
        ),
        "source_freeze_sha256": args.source_freeze_sha256,
        "implementation_path": repo_relative(
            ROOT, worker_path, "blind interval worker"
        ),
        "implementation_sha256": files["blind_interval_worker.py"],
        "index_publisher_path": repo_relative(
            ROOT, publisher_path, "blind index publisher"
        ),
        "index_publisher_sha256": files["blind_index_publisher.py"],
        "target_code_or_matrices_imported": False,
        "physical_spectrum_executed_at_freeze": False,
        "guards": {
            "retained_vectors_max": 128,
            "matvecs_max": 2000,
            "wall_seconds_max": 10800,
            "rss_bytes_max": 6 * (1 << 30),
            "checkpoint_dimensions": [16, 32, 64, 96, 128],
        },
        "claim_boundary": (
            "PRE_TARGET_BLIND_METHOD_ONLY__NO_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        ),
    }
    atomic_owner_once_json(ROOT, args.output, freeze)


def _relative_future(path: Path, label: str) -> str:
    root = ROOT.resolve()
    resolved = Path(os.path.abspath(path))
    demand(root in resolved.parents, f"{label}: outside repository")
    return resolved.relative_to(root).as_posix()


def validate_runnable_freeze(
    freeze_path: Path, freeze_sha256: str, length: int, charge: int,
) -> dict[str, object]:
    freeze = load_pinned_json(freeze_path, freeze_sha256, "blind method freeze")
    demand(freeze.get("schema") == FREEZE_SCHEMA, "blind freeze schema mismatch")
    demand(freeze.get("status") == FREEZE_STATUS, "blind freeze status mismatch")
    demand(freeze.get("target_code_or_matrices_imported") is False, "blind freeze imports target bytes")
    planned = freeze.get("planned_sectors")
    demand(isinstance(planned, list), "blind freeze planned sector census malformed")
    normalized: list[list[int]] = []
    for item in planned:
        demand(
            isinstance(item, list) and len(item) == 2
            and all(type(value) is int for value in item),
            "blind freeze planned sector malformed",
        )
        normalized.append([item[0], item[1]])
    demand(
        normalized == [list(pair) for pair in sorted({tuple(item) for item in normalized})],
        "blind freeze planned sector order/census",
    )
    demand([length, charge] in normalized, "blind sector absent from frozen plan")

    source_path = repo_file(
        ROOT, freeze.get("source_freeze_path"), freeze.get("source_freeze_sha256"),
        "blind source freeze",
    )
    source = validate_source_freeze(source_path, str(freeze["source_freeze_sha256"]))
    files = source["files"]
    assert isinstance(files, dict)
    expected_files = {
        "blind_contract_control.py": Path(__file__).resolve(),
        "blind_index_publisher.py": PACKET / "blind_index_publisher.py",
        "blind_interval_worker.py": PACKET / "blind_interval_worker.py",
        "contract_common.py": PACKET / "contract_common.py",
    }
    for name, path in expected_files.items():
        demand(files.get(name) == sha256_file(path), f"blind source/current {name} mismatch")
    demand(
        freeze.get("implementation_path")
        == repo_relative(ROOT, expected_files["blind_interval_worker.py"], "blind worker")
        and freeze.get("implementation_sha256") == files["blind_interval_worker.py"],
        "blind freeze worker binding mismatch",
    )
    demand(
        freeze.get("index_publisher_path")
        == repo_relative(ROOT, expected_files["blind_index_publisher.py"], "blind publisher")
        and freeze.get("index_publisher_sha256") == files["blind_index_publisher.py"],
        "blind freeze publisher binding mismatch",
    )
    plan_path = repo_file(
        ROOT, freeze.get("sector_plan_path"), freeze.get("sector_plan_sha256"),
        "blind sector plan",
    )
    plan = load_pinned_json(plan_path, str(freeze["sector_plan_sha256"]), "blind sector plan")
    demand(plan.get("planned_sectors") == normalized, "blind freeze/plan sector mismatch")
    manifest_path = repo_file(
        ROOT, freeze.get("manifest_path"), freeze.get("manifest_sha256"),
        "accumulation manifest",
    )
    demand(
        reconstruct_sector_plan(ROOT, manifest_path, str(freeze["manifest_sha256"])) == plan,
        "blind plan is not the exact manifest reconstruction",
    )
    return {
        "freeze": freeze,
        "planned_sectors": normalized,
        "paths": {
            "manifest": manifest_path,
            "sector_plan": plan_path,
            "blind_method_freeze": freeze_path.resolve(),
            "blind_source_freeze": source_path,
            "blind_worker": expected_files["blind_interval_worker.py"],
            "blind_control": expected_files["blind_contract_control.py"],
            "blind_publisher": expected_files["blind_index_publisher.py"],
            "contract_common": expected_files["contract_common.py"],
        },
    }


def _authority_bindings(paths: dict[str, Path]) -> dict[str, dict[str, str]]:
    return {
        label: {
            "path": repo_relative(ROOT, path, f"blind credential {label}"),
            "sha256": sha256_file(path),
        }
        for label, path in sorted(paths.items())
    }


def issue_execution_credential(args: argparse.Namespace) -> None:
    validated = validate_runnable_freeze(
        args.freeze, args.freeze_sha256, args.L, args.q,
    )
    physical_output = _relative_future(args.physical_output, "blind physical output")
    authorities = _authority_bindings(validated["paths"])
    credential = {
        "schema": BLIND_CREDENTIAL_SCHEMA,
        "status": BLIND_CREDENTIAL_STATUS,
        "ordering_model": ORDERING_MODEL,
        "claim_boundary": (
            "AUTHENTICATED_TRUSTED_BLIND_CODE_PATH_ONLY__NO_ADVERSARY_"
            "RESISTANT_WALL_CLOCK_ATTESTATION"
        ),
        "authorization_nonce": secrets.token_hex(32),
        "execution_token_sha256": hashlib.sha256(BLIND_RUN_TOKEN.encode("ascii")).hexdigest(),
        "L": args.L,
        "q": args.q,
        "physical_output_path": physical_output,
        "authorities": authorities,
        "planned_sectors": validated["planned_sectors"],
        "creation_order_evidence": {
            "authorities_validated_before_nonce": True,
            "fresh_nonce_bits": 256,
        },
    }
    atomic_owner_once_json(ROOT, args.output, credential)


def validate_execution_credential(
    credential_path: Path, credential_sha256: str, length: int, charge: int,
    physical_output: Path, execution_token: str = BLIND_RUN_TOKEN,
) -> dict[str, object]:
    credential = load_pinned_json(
        credential_path, credential_sha256, "blind execution credential",
    )
    metadata = credential_path.stat()
    demand(
        stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1
        and stat.S_IMODE(metadata.st_mode) == 0o444,
        "blind execution credential owner-once custody",
    )
    demand(set(credential) == {
        "schema", "status", "ordering_model", "claim_boundary",
        "authorization_nonce", "execution_token_sha256", "L", "q",
        "physical_output_path", "authorities", "planned_sectors",
        "creation_order_evidence",
    }, "blind execution credential key census")
    demand(
        credential.get("schema") == BLIND_CREDENTIAL_SCHEMA
        and credential.get("status") == BLIND_CREDENTIAL_STATUS
        and credential.get("ordering_model") == ORDERING_MODEL,
        "blind execution credential identity mismatch",
    )
    nonce = credential.get("authorization_nonce")
    demand(
        isinstance(nonce, str) and len(nonce) == 64
        and set(nonce) <= set("0123456789abcdef"),
        "blind execution credential nonce malformed",
    )
    demand(
        credential.get("execution_token_sha256")
        == hashlib.sha256(execution_token.encode("ascii")).hexdigest(),
        "blind execution token binding mismatch",
    )
    demand(
        type(credential.get("L")) is int and credential["L"] == length
        and type(credential.get("q")) is int and credential["q"] == charge,
        "blind execution sector binding mismatch",
    )
    demand(
        credential.get("physical_output_path")
        == _relative_future(physical_output, "blind physical output"),
        "blind execution output binding mismatch",
    )
    authorities = credential.get("authorities")
    demand(isinstance(authorities, dict), "blind credential authority map absent")
    expected_labels = {
        "manifest", "sector_plan", "blind_method_freeze", "blind_source_freeze",
        "blind_worker", "blind_control", "blind_publisher", "contract_common",
    }
    demand(set(authorities) == expected_labels, "blind credential authority census")
    for label, binding in authorities.items():
        demand(
            isinstance(binding, dict) and set(binding) == {"path", "sha256"},
            f"blind credential {label} binding malformed",
        )
        repo_file(ROOT, binding.get("path"), binding.get("sha256"), f"blind credential {label}")
    freeze_binding = authorities["blind_method_freeze"]
    validated = validate_runnable_freeze(
        ROOT / str(freeze_binding["path"]), str(freeze_binding["sha256"]),
        length, charge,
    )
    demand(
        authorities == _authority_bindings(validated["paths"]),
        "blind credential authority binding mismatch",
    )
    demand(
        credential.get("planned_sectors") == validated["planned_sectors"],
        "blind credential planned-sector mismatch",
    )
    demand(
        credential.get("creation_order_evidence") == {
            "authorities_validated_before_nonce": True, "fresh_nonce_bits": 256,
        },
        "blind credential creation-order evidence mismatch",
    )
    return {
        "schema": BLIND_BINDING_SCHEMA,
        "ordering_model": ORDERING_MODEL,
        "credential_path": repo_relative(ROOT, credential_path, "blind credential"),
        "credential_sha256": credential_sha256,
        "authorization_nonce": nonce,
        "manifest_sha256": authorities["manifest"]["sha256"],
        "sector_plan_sha256": authorities["sector_plan"]["sha256"],
        "blind_method_freeze_sha256": authorities["blind_method_freeze"]["sha256"],
        "blind_source_freeze_sha256": authorities["blind_source_freeze"]["sha256"],
        "blind_worker_sha256": authorities["blind_worker"]["sha256"],
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    subparsers = result.add_subparsers(dest="mode", required=True)
    plan = subparsers.add_parser("produce-plan")
    plan.add_argument("--manifest", type=Path, required=True)
    plan.add_argument("--manifest-sha256", required=True)
    plan.add_argument("--output", type=Path, required=True)
    plan.set_defaults(action=produce_plan)

    freeze = subparsers.add_parser("produce-freeze")
    freeze.add_argument("--manifest", type=Path, required=True)
    freeze.add_argument("--manifest-sha256", required=True)
    freeze.add_argument("--sector-plan", type=Path, required=True)
    freeze.add_argument("--sector-plan-sha256", required=True)
    freeze.add_argument("--source-freeze", type=Path, required=True)
    freeze.add_argument("--source-freeze-sha256", required=True)
    freeze.add_argument("--output", type=Path, required=True)
    freeze.set_defaults(action=produce_freeze)

    credential = subparsers.add_parser("issue-credential")
    credential.add_argument("--freeze", type=Path, required=True)
    credential.add_argument("--freeze-sha256", required=True)
    credential.add_argument("--L", type=int, required=True)
    credential.add_argument("--q", type=int, required=True)
    credential.add_argument("--physical-output", type=Path, required=True)
    credential.add_argument("--output", type=Path, required=True)
    credential.set_defaults(action=issue_execution_credential)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        args.action(args)
    except (Refusal, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
