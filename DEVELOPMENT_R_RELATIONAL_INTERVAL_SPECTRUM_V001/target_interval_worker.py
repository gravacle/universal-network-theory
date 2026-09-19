#!/usr/bin/env python3
"""Frozen adapter exposing the audited sparse worker to interval-selected rows."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ENGINE = ROOT / "DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001" / "compute_phase_screen.py"
ENGINE_SHA256 = "e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7"
CREDENTIAL_CONTROL = HERE / "execution_credential.py"
CREDENTIAL_CONTROL_SHA256 = "31b86f56c9691721224bf0359a9e354566a34370f8c00703369d382f30cdd3f3"
TARGET_DRIVER = HERE / "interval_spectrum_driver.py"
TARGET_FREEZE = HERE / "FREEZE.json"
EXECUTION_TOKEN = "RUN_HASH_PINNED_RELATIONAL_INTERVAL_SPECTRUM_V001"
ALLOWED_SIZES = (10, 12)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_engine():
    if sha256(ENGINE) != ENGINE_SHA256:
        raise RuntimeError("frozen sparse response engine hash mismatch")
    spec = importlib.util.spec_from_file_location("frozen_interval_response_engine", ENGINE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen sparse response engine")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_credential_control():
    if sha256(CREDENTIAL_CONTROL) != CREDENTIAL_CONTROL_SHA256:
        raise RuntimeError("target execution credential control hash mismatch")
    specification = importlib.util.spec_from_file_location(
        "frozen_worker_execution_credential", CREDENTIAL_CONTROL,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load target execution credential control")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def credential_expectations() -> dict[str, tuple[Path, str]]:
    return {
        "worker": (Path(__file__).resolve(), sha256(Path(__file__).resolve())),
        "driver": (TARGET_DRIVER, sha256(TARGET_DRIVER)),
        "engine": (ENGINE, ENGINE_SHA256),
        "control": (CREDENTIAL_CONTROL, CREDENTIAL_CONTROL_SHA256),
        "target_freeze": (TARGET_FREEZE, sha256(TARGET_FREEZE)),
    }


def run_physical(
    length: int,
    charge: int,
    credential: Path,
    credential_sha256: str,
    output: Path,
    *,
    repo_root: Path = ROOT,
    expectations: dict[str, tuple[Path, str]] | None = None,
    engine_loader=load_engine,
) -> None:
    if length not in ALLOWED_SIZES or not 1 <= charge <= length:
        raise RuntimeError("physical sector outside the positive L10/L12 domain")
    control = load_credential_control()
    expected = credential_expectations() if expectations is None else expectations
    try:
        authorization = control.validate_execution_credential(
            repo_root,
            credential,
            credential_sha256,
            length,
            charge,
            output,
            expected["worker"],
            expected["driver"],
            expected["engine"],
            expected["control"],
            expected["target_freeze"],
            EXECUTION_TOKEN,
        )
    except (control.CredentialRefusal, OSError, ValueError) as error:
        raise RuntimeError(f"target execution credential refused: {error}") from error
    engine = engine_loader()
    # The imported implementation's only row restriction is a protocol policy
    # table.  This packet replaces that table with the complete positive-q
    # interval domain while leaving every graph, block, Krylov, response,
    # residual, and serializer function byte-identical and hash-pinned.
    engine.TARGET_ROWS = {
        size: tuple(range(1, size + 1)) for size in ALLOWED_SIZES
    }
    engine.worker(length, charge, output)
    row = json.loads(output.read_text())
    native_rss = int(row["max_rss_bytes"])
    if sys.platform.startswith("linux"):
        row["max_rss_native"] = native_rss
        row["max_rss_bytes"] = native_rss * 1024
        row["rss_unit_normalization"] = "LINUX_RUSAGE_KIB_TO_BYTES"
    else:
        row["rss_unit_normalization"] = "DARWIN_RUSAGE_BYTES"
    row["execution_authorization"] = authorization
    output.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int)
    parser.add_argument("--q", type=int)
    parser.add_argument("--credential", type=Path)
    parser.add_argument("--credential-sha256")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        engine = load_engine()
        assert engine.MAX_KRYLOV == 128
        assert engine.SECTOR_SECONDS_LIMIT == 3 * 60 * 60
        assert engine.RSS_LIMIT_BYTES == 6 * (1 << 30)
        assert '"lowest_five_ritz_values": values[:5].tolist()' in ENGINE.read_text()
        print("PASS_INTERVAL_ADAPTER_CUSTODY__NO_PHYSICAL_SPECTRUM")
        return
    if (
        args.L not in ALLOWED_SIZES or args.q is None or args.output is None
        or args.credential is None or args.credential_sha256 is None
    ):
        parser.error(
            "physical worker requires L in {10,12}, q, credential, "
            "credential SHA-256, and output"
        )
    if not 1 <= args.q <= args.L:
        parser.error("q must be a positive half-sector charge no larger than L")
    run_physical(
        args.L, args.q, args.credential, args.credential_sha256, args.output,
    )


if __name__ == "__main__":
    main()
