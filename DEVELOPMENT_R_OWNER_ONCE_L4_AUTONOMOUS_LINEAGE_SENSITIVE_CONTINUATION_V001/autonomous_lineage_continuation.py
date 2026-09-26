#!/usr/bin/env python3
"""Prospectively frozen L4 lineage-sensitive continuation.

The default/preflight path authenticates inputs only.  Scientific evaluation
is guarded by the explicit post-review token and has not been run as part of
the freeze construction.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTOCOL = HERE / "PROTOCOL.md"
FREEZE = HERE / "FREEZE.json"
SOURCE_MANIFEST = HERE / "SOURCE_HASHES.sha256"
PARENT_SOURCE = (
    ROOT
    / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
    / "compute_seed_history.py"
)
OUTPUT = (
    HERE
    / "PHYSICAL_OUTPUTS"
    / "L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_RESULT_V001.json"
)

PROTOCOL_SHA256 = "eabe5b1a3e012e00151de24415654bd0b60a473a2e3b39fa395c1f5ec0753a29"
FREEZE_SHA256 = "606a72692b17b86bd9ad65d9201a861e298cef09e07fadac7d983c34a10b6b28"
PARENT_SHA256 = "24ea3626fda443dd4ae5076c7766e1aaca77ff5ce9f22c05bae96943fc627d55"
CHECKPOINT_SHA256 = "52d979329c4a8c643bda90644981e9508f7ec42f65c0dd25310cddbf2074671f"
BASIS_SHA256 = "b91eec28486c0c06f9ce8f5ebaf4bd71b24a3fd5a3525650ac9d7023bea8d81f"
AUTHORIZATION_TOKEN = "REVIEWED_FREEZE__AUTHORIZE_L4_CONTINUATION_V001"

LENGTH = 4
COARSE_STEPS = 64
FINE_STEPS = 128
EVENT = 0
BASE_TAU = 1.0e-10
COARSE_FINE_LIMIT = 1.0e-8
RESIDUAL_LIMIT = 1.0e-11
MINIMUM_EIGENVALUE = -1.0e-10
NORMALIZED_RANGE_SLOP = 1.0e-12
MANIFEST_PATHS = {
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/FREEZE.json",
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/PROTOCOL.md",
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/README.md",
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/autonomous_lineage_continuation.py",
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/test_autonomous_lineage_continuation.py",
    "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py",
}


class ContinuationFailure(RuntimeError):
    """Frozen-input, numerical-control, or publication failure."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def array_sha256(array: np.ndarray, dtype: str) -> str:
    canonical = np.asarray(array, dtype=dtype, order="C")
    return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


def authenticate_freeze() -> dict[str, dict[str, str]]:
    expected = ((PROTOCOL, PROTOCOL_SHA256), (FREEZE, FREEZE_SHA256), (PARENT_SOURCE, PARENT_SHA256))
    records: dict[str, dict[str, str]] = {}
    for path, digest in expected:
        actual = sha256_file(path)
        if actual != digest:
            raise ContinuationFailure(
                f"source hash mismatch for {path.relative_to(ROOT)}: {actual} != {digest}"
            )
        records[path.name] = {
            "path": str(path.relative_to(ROOT)),
            "sha256": actual,
        }
    manifest_records: dict[str, str] = {}
    for line in SOURCE_MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            digest, relative = line.split("  ", 1)
        except ValueError as error:
            raise ContinuationFailure("malformed source-hash manifest") from error
        manifest_records[relative] = digest
    if set(manifest_records) != MANIFEST_PATHS:
        raise ContinuationFailure("source-hash manifest path census changed")
    for relative, expected_digest in manifest_records.items():
        path = ROOT / relative
        actual_digest = sha256_file(path)
        if actual_digest != expected_digest:
            raise ContinuationFailure(
                f"source manifest mismatch for {relative}: {actual_digest} != {expected_digest}"
            )
    records[SOURCE_MANIFEST.name] = {
        "path": str(SOURCE_MANIFEST.relative_to(ROOT)),
        "sha256": sha256_file(SOURCE_MANIFEST),
    }
    return records


def load_parent() -> ModuleType:
    spec = importlib.util.spec_from_file_location("frozen_l4_seed_parent", PARENT_SOURCE)
    if spec is None or spec.loader is None:
        raise ContinuationFailure("cannot load frozen L4 parent")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if (
        module.PHI != math.pi / 4.0
        or module.KAPPA != math.pi / 2.0
        or module.TAYLOR_ORDER != 12
    ):
        raise ContinuationFailure("frozen parent parameters changed")
    return module


def regenerate_checkpoint(module: ModuleType, steps: int) -> tuple[Any, np.ndarray]:
    parent = module.Parent(LENGTH)
    state = parent.initial_state()
    for event in range(LENGTH):
        state = parent.apply_admission(state, event)
        state, _ = parent.transport(state, steps)
    state = np.asarray(state, dtype=np.complex128)
    if steps == FINE_STEPS:
        if array_sha256(parent.words, "<u4") != BASIS_SHA256:
            raise ContinuationFailure("L4 basis-word fingerprint changed")
        if array_sha256(state, "<c16") != CHECKPOINT_SHA256:
            raise ContinuationFailure("L4 fine checkpoint fingerprint changed")
    return parent, state


def labels(parent: Any) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    words = np.asarray(parent.words, dtype=np.uint32)
    loaded_mask = (1 << LENGTH) - 1
    loaded = words & np.uint32(loaded_mask)
    lineage = np.bitwise_xor(loaded, np.uint32(loaded_mask)).astype(np.int64)
    carrier = (words >> np.uint32(LENGTH)).astype(np.int64)
    q = np.array([bin(int(word)).count("1") for word in lineage], dtype=np.int8)
    return lineage, carrier, q


def reduced_marginals(
    density: np.ndarray, lineage: np.ndarray, carrier: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    rho_s = np.zeros((1 << LENGTH, 1 << LENGTH), dtype=np.complex128)
    rho_c = np.zeros((1 << (2 * LENGTH), 1 << (2 * LENGTH)), dtype=np.complex128)
    for c_word in np.unique(carrier):
        indices = np.flatnonzero(carrier == c_word)
        s_words = lineage[indices]
        rho_s[np.ix_(s_words, s_words)] += density[np.ix_(indices, indices)]
    for s_word in np.unique(lineage):
        indices = np.flatnonzero(lineage == s_word)
        c_words = carrier[indices]
        rho_c[np.ix_(c_words, c_words)] += density[np.ix_(indices, indices)]
    return rho_s, rho_c


def build_sector_arms(parent: Any, state: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    lineage, carrier, q_values = labels(parent)
    dimension = len(state)
    actual = np.zeros((dimension, dimension), dtype=np.complex128)
    product = np.zeros_like(actual)
    weights: dict[str, float] = {}
    for q in range(LENGTH + 1):
        indices = np.flatnonzero(q_values == q)
        s_words = np.unique(lineage[indices])
        c_words = np.unique(carrier[indices])
        index_of = {
            (int(lineage[index]), int(carrier[index])): int(index) for index in indices
        }
        grid = np.array(
            [index_of[(int(s_word), int(c_word))] for s_word in s_words for c_word in c_words],
            dtype=np.int64,
        )
        amplitude = state[grid].reshape(len(s_words), len(c_words))
        p_q = float(np.vdot(amplitude, amplitude).real)
        weights[str(q)] = p_q
        actual[np.ix_(grid, grid)] = np.outer(amplitude.ravel(), amplitude.ravel().conj())
        if p_q > 0.0:
            # Keep these small contractions on an explicit path.  The pinned
            # Accelerate build can emit spurious BLAS status warnings for
            # complex rectangular matmul even when the result is finite.
            rho_s = np.einsum("sc,tc->st", amplitude, amplitude.conj(), optimize=False)
            rho_c = np.einsum("sc,sd->cd", amplitude, amplitude.conj(), optimize=False)
            product[np.ix_(grid, grid)] = np.kron(rho_s, rho_c) / p_q
    return actual, product, weights


def admission_unitary(parent: Any) -> np.ndarray:
    dimension = int(parent.dimension)
    unitary = np.eye(dimension, dtype=np.complex128)
    sources, destinations = parent.admission_pairs[EVENT]
    cosine = math.cos(math.pi / 4.0)
    sine = math.sin(math.pi / 4.0)
    unitary[sources, sources] = cosine
    unitary[destinations, destinations] = cosine
    unitary[sources, destinations] = -1j * sine
    unitary[destinations, sources] = -1j * sine
    return unitary


def admission_unitarity_residual(parent: Any) -> float:
    sources, destinations = parent.admission_pairs[EVENT]
    structural_failure = (
        len(set(map(int, sources))) != len(sources)
        or len(set(map(int, destinations))) != len(destinations)
        or bool(set(map(int, sources)) & set(map(int, destinations)))
    )
    cosine = math.cos(math.pi / 4.0)
    sine = math.sin(math.pi / 4.0)
    block = np.array(
        [[cosine, -1j * sine], [-1j * sine, cosine]], dtype=np.complex128
    )
    gram = np.einsum("ji,jk->ik", block.conj(), block, optimize=False)
    block_residual = float(np.max(np.abs(gram - np.eye(2))))
    return max(float(structural_failure), block_residual)


def transport_unitary(parent: Any) -> tuple[np.ndarray, dict[str, float]]:
    dimension = int(parent.dimension)
    hamiltonian = np.zeros((dimension, dimension), dtype=float)
    for sources, destinations, _ in parent.actions:
        hamiltonian[sources, destinations] -= 1.0
    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
    reconstructed = (eigenvectors * eigenvalues) @ eigenvectors.T
    unitary = (eigenvectors * np.exp(-1j * eigenvalues * (math.pi / 2.0))) @ eigenvectors.T
    identity = np.eye(dimension)
    controls = {
        "hamiltonian_hermiticity": float(np.max(np.abs(hamiltonian - hamiltonian.T))),
        "hamiltonian_reconstruction": float(np.max(np.abs(reconstructed - hamiltonian))),
        "transport_unitarity": float(np.max(np.abs(unitary.conj().T @ unitary - identity))),
    }
    return unitary, controls


def density_controls(density: np.ndarray) -> dict[str, float]:
    hermitian = (density + density.conj().T) / 2.0
    return {
        "trace": abs(float(np.trace(density).real) - 1.0),
        "trace_imaginary": abs(float(np.trace(density).imag)),
        "hermiticity": float(np.max(np.abs(density - density.conj().T))),
        "minimum_eigenvalue": float(np.min(np.linalg.eigvalsh(hermitian))),
    }


def carrier_observables(
    actual: np.ndarray, product: np.ndarray, lineage: np.ndarray, carrier: np.ndarray
) -> dict[str, Any]:
    _, sigma_actual = reduced_marginals(actual, lineage, carrier)
    _, sigma_product = reduced_marginals(product, lineage, carrier)
    difference = (sigma_actual - sigma_product)
    difference = (difference + difference.conj().T) / 2.0
    trace_distance = 0.5 * float(np.sum(np.abs(np.linalg.eigvalsh(difference))))
    diagonal_actual = np.real(np.diag(sigma_actual))
    diagonal_product = np.real(np.diag(sigma_product))
    configuration_tv = 0.5 * float(np.sum(np.abs(diagonal_actual - diagonal_product)))
    occupations_actual = np.array(
        [sum(diagonal_actual[word] for word in range(1 << (2 * LENGTH)) if (word >> site) & 1) for site in range(2 * LENGTH)]
    )
    occupations_product = np.array(
        [sum(diagonal_product[word] for word in range(1 << (2 * LENGTH)) if (word >> site) & 1) for site in range(2 * LENGTH)]
    )
    delta_n = occupations_actual - occupations_product
    sector_actual = np.array(
        [sum(diagonal_actual[word] for word in range(1 << (2 * LENGTH)) if bin(word).count("1") == q) for q in range(LENGTH + 1)]
    )
    sector_product = np.array(
        [sum(diagonal_product[word] for word in range(1 << (2 * LENGTH)) if bin(word).count("1") == q) for q in range(LENGTH + 1)]
    )
    return {
        "carrier_trace_distance": trace_distance,
        "carrier_configuration_tv": configuration_tv,
        "carrier_number_sector_tv": 0.5 * float(np.sum(np.abs(sector_actual - sector_product))),
        "occupation_rms": float(np.sqrt(np.mean(delta_n**2))),
        "delta_n": delta_n.tolist(),
        "delta_n_0": float(delta_n[0]),
    }


def evaluate_resolution(module: ModuleType, steps: int, common: dict[str, Any]) -> dict[str, Any]:
    parent, state = regenerate_checkpoint(module, steps)
    lineage, carrier, _ = labels(parent)
    actual, product, weights = build_sector_arms(parent, state)
    actual_s, actual_c = reduced_marginals(actual, lineage, carrier)
    product_s, product_c = reduced_marginals(product, lineage, carrier)
    input_residuals = {
        "carrier_marginal_equality": float(np.max(np.abs(actual_c - product_c))),
        "lineage_marginal_equality": float(np.max(np.abs(actual_s - product_s))),
        "checkpoint_norm": abs(float(np.vdot(state, state).real) - 1.0),
    }
    _, _, q_values = labels(parent)
    input_residuals["q_weight_equality"] = max(
        abs(
            float(np.trace(actual[np.ix_(q_values == q, q_values == q)]).real)
            - float(np.trace(product[np.ix_(q_values == q, q_values == q)]).real)
        )
        for q in range(LENGTH + 1)
    )
    admitted_actual = common["admission"] @ actual @ common["admission"].conj().T
    admitted_product = common["admission"] @ product @ common["admission"].conj().T
    terminal_actual = common["transport"] @ admitted_actual @ common["transport"].conj().T
    terminal_product = common["transport"] @ admitted_product @ common["transport"].conj().T
    after_admission = carrier_observables(admitted_actual, admitted_product, lineage, carrier)
    after_transport = carrier_observables(terminal_actual, terminal_product, lineage, carrier)
    controls: dict[str, float] = dict(input_residuals)
    controls["trace_distance_transport_invariance"] = abs(
        float(after_admission["carrier_trace_distance"])
        - float(after_transport["carrier_trace_distance"])
    )
    minimum_eigenvalue = 0.0
    for label, density in (
        ("input_actual", actual),
        ("input_product", product),
        ("terminal_actual", terminal_actual),
        ("terminal_product", terminal_product),
    ):
        row = density_controls(density)
        minimum_eigenvalue = min(minimum_eigenvalue, row.pop("minimum_eigenvalue"))
        controls.update({f"{label}_{key}": value for key, value in row.items()})
    return {
        "steps": steps,
        "sector_weights": weights,
        "after_admission": after_admission,
        "after_transport": after_transport,
        "controls": controls,
        "minimum_density_eigenvalue": minimum_eigenvalue,
    }


def registered_values(row: dict[str, Any]) -> list[float]:
    values: list[float] = []
    for checkpoint in ("after_admission", "after_transport"):
        record = row[checkpoint]
        values.extend(float(record[key]) for key in (
            "carrier_trace_distance",
            "carrier_configuration_tv",
            "carrier_number_sector_tv",
            "occupation_rms",
            "delta_n_0",
        ))
        values.extend(float(value) for value in record["delta_n"])
    return values


def normalized_ranges_pass(row: dict[str, Any]) -> bool:
    for checkpoint in ("after_admission", "after_transport"):
        record = row[checkpoint]
        for key in (
            "carrier_trace_distance",
            "carrier_configuration_tv",
            "carrier_number_sector_tv",
            "occupation_rms",
        ):
            value = float(record[key])
            if not (-NORMALIZED_RANGE_SLOP <= value <= 1.0 + NORMALIZED_RANGE_SLOP):
                return False
    return True


def build_result() -> dict[str, Any]:
    dependencies = authenticate_freeze()
    module = load_parent()
    parent, _ = regenerate_checkpoint(module, FINE_STEPS)
    transport, operator_controls = transport_unitary(parent)
    admission = admission_unitary(parent)
    operator_controls["admission_unitarity"] = admission_unitarity_residual(parent)
    common = {"admission": admission, "transport": transport}
    coarse = evaluate_resolution(module, COARSE_STEPS, common)
    fine = evaluate_resolution(module, FINE_STEPS, common)
    coarse_fine = max(abs(a - b) for a, b in zip(registered_values(coarse), registered_values(fine)))
    residual = max(
        *(abs(float(value)) for value in operator_controls.values()),
        *(abs(float(value)) for value in coarse["controls"].values()),
        *(abs(float(value)) for value in fine["controls"].values()),
    )
    tau = max(BASE_TAU, 50.0 * coarse_fine, 100.0 * residual)
    delta_c = float(fine["after_transport"]["carrier_trace_distance"])
    finite_values = all(math.isfinite(value) for value in registered_values(coarse) + registered_values(fine))
    observable_ranges_pass = normalized_ranges_pass(coarse) and normalized_ranges_pass(fine)
    controls_pass = (
        finite_values
        and observable_ranges_pass
        and coarse_fine <= COARSE_FINE_LIMIT
        and residual <= RESIDUAL_LIMIT
        and coarse["minimum_density_eigenvalue"] >= MINIMUM_EIGENVALUE
        and fine["minimum_density_eigenvalue"] >= MINIMUM_EIGENVALUE
    )
    if not controls_pass:
        classification = "L4_LINEAGE_SENSITIVE_CONTINUATION_UNRESOLVED"
    elif delta_c / tau > 1.0:
        classification = "RESOLVED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION"
    else:
        classification = "FALSIFIED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION_IN_FIXED_TEST"
    return {
        "schema": "L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_RESULT_V001",
        "classification": classification,
        "claim_boundary": "L4_SINGLE_REVISIT_MECHANISM_ONLY__NO_SCALING_CURVATURE_GEOMETRY_OR_GRAVITY",
        "dependencies": dependencies,
        "continuation_source_sha256": sha256_file(Path(__file__)),
        "coarse": coarse,
        "fine": fine,
        "controls": {
            "passed": controls_pass,
            "coarse_fine_maximum": coarse_fine,
            "maximum_residual": residual,
            "operators": operator_controls,
            "normalized_observable_ranges": observable_ranges_pass,
        },
        "tau": tau,
        "T_dyn": delta_c / tau,
        "fixed_occupation_profile_response": bool(
            controls_pass and float(fine["after_transport"]["occupation_rms"]) > tau
        ),
    }


def atomic_write_json(path: Path, value: dict[str, Any]) -> str:
    if path.exists():
        raise ContinuationFailure(f"refusing to overwrite existing result: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(rendered)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return sha256_file(path)


def preflight() -> dict[str, Any]:
    return {
        "schema": "L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_PREFLIGHT_V001",
        "authenticated": authenticate_freeze(),
        "scientific_continuation_executed": False,
        "result_exists": OUTPUT.exists(),
        "launch_status": "READY_AFTER_HUMAN_REVIEW_OF_FREEZE",
        "estimated_wall_minutes": "1-5",
        "restart_unit": "WHOLE_TWO_RESOLUTION_L4_COMPARISON",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight", action="store_true")
    group.add_argument("--execute", action="store_true")
    parser.add_argument("--authorization-token", default="")
    arguments = parser.parse_args()
    if arguments.preflight:
        print(json.dumps(preflight(), indent=2, sort_keys=True))
        return
    if arguments.authorization_token != AUTHORIZATION_TOKEN:
        raise ContinuationFailure("post-review authorization token absent or incorrect")
    result = build_result()
    digest = atomic_write_json(OUTPUT, result)
    print(json.dumps({"classification": result["classification"], "sha256": digest}, sort_keys=True))


if __name__ == "__main__":
    main()
