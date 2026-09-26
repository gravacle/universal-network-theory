#!/usr/bin/env python3
"""Independent post-result validation of the frozen L4 continuation.

This implementation imports neither the target continuation nor the historical
parent.  It reconstructs the basis, checkpoint dynamics, comparator,
continuation, partial traces, and observables locally.  Every dense contraction
uses an explicit ``numpy.einsum(..., optimize=False)`` path; Python's matrix
multiplication operator is intentionally absent.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import tempfile
import warnings
from pathlib import Path
from typing import Any, Iterable

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001"
TARGET_RESULT = TARGET / "PHYSICAL_OUTPUTS/L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_RESULT_V001.json"
OUTPUT = HERE / "INDEPENDENT_RESULT.json"

LENGTH = 4
DIMENSION = 495
COARSE_STEPS = 64
FINE_STEPS = 128
ORDER = 12
PHI = math.pi / 4.0
DWELL = math.pi / 2.0
EVENT = 0
VALUE_TOLERANCE = 5.0e-12
CONTROL_TOLERANCE = 1.0e-11
COARSE_FINE_TOLERANCE = 1.0e-8
MINIMUM_EIGENVALUE = -1.0e-10
BASE_TAU = 1.0e-10

EXPECTED = {
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/PROTOCOL.md": "eabe5b1a3e012e00151de24415654bd0b60a473a2e3b39fa395c1f5ec0753a29",
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/FREEZE.json": "606a72692b17b86bd9ad65d9201a861e298cef09e07fadac7d983c34a10b6b28",
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/SOURCE_HASHES.sha256": "844a0458a87ab47c2a744d1859eaa7a16d668309ea2a1ff180f5f4817181c2e3",
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/autonomous_lineage_continuation.py": "77caeb87de267d4b45d14ae14670601f70ce24195a71e50eb5f7d02a455a0808",
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/test_autonomous_lineage_continuation.py": "b07ebb0fb1b3751217f7725840649fa1230c98acc824c73817e138ab169d53c4",
    "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py": "24ea3626fda443dd4ae5076c7766e1aaca77ff5ce9f22c05bae96943fc627d55",
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/PHYSICAL_OUTPUTS/L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_RESULT_V001.json": "ad134b528761c4e865df35678097dab4fb56297c5237a910ca482bac77c0c0dc",
}
EXPECTED_BASIS_SHA256 = "b91eec28486c0c06f9ce8f5ebaf4bd71b24a3fd5a3525650ac9d7023bea8d81f"
EXPECTED_FINE_CHECKPOINT_SHA256 = "52d979329c4a8c643bda90644981e9508f7ec42f65c0dd25310cddbf2074671f"


class AuditFailure(RuntimeError):
    """An authenticated input, finite-arithmetic, or comparison check failed."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def array_sha256(array: np.ndarray, dtype: str) -> str:
    canonical = np.asarray(array, dtype=dtype, order="C")
    return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


def authenticate() -> dict[str, str]:
    observed: dict[str, str] = {}
    for relative, expected in EXPECTED.items():
        actual = sha256_file(ROOT / relative)
        if actual != expected:
            raise AuditFailure(f"custody mismatch for {relative}: {actual} != {expected}")
        observed[relative] = actual
    manifest_lines = (TARGET / "SOURCE_HASHES.sha256").read_text().splitlines()
    for line in manifest_lines:
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        if sha256_file(ROOT / relative) != digest:
            raise AuditFailure(f"nested target source manifest mismatch: {relative}")
    return observed


def require_finite(value: Any, label: str) -> None:
    array = np.asarray(value)
    if not bool(np.all(np.isfinite(array))):
        raise AuditFailure(f"nonfinite value in {label}")


def require_finite_tree(value: Any, label: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            require_finite_tree(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            require_finite_tree(child, f"{label}[{index}]")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(float(value)):
            raise AuditFailure(f"nonfinite scalar in {label}")


def fixed_weight_words(width: int, weight: int) -> np.ndarray:
    values = np.empty(math.comb(width, weight), dtype=np.uint32)
    for index, positions in enumerate(itertools.combinations(range(width), weight)):
        word = 0
        for position in positions:
            word |= 1 << position
        values[index] = word
    return values


def prism_edges() -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for rail in range(2):
        offset = rail * LENGTH
        for site in range(LENGTH):
            edges.append((offset + site, offset + (site + 1) % LENGTH))
    for site in range(LENGTH):
        edges.append((site, LENGTH + (site + 1) % LENGTH))
    return edges


class IndependentParent:
    def __init__(self) -> None:
        self.words = fixed_weight_words(3 * LENGTH, LENGTH)
        self.index = {int(word): index for index, word in enumerate(self.words)}
        self.carrier_words = self.words >> np.uint32(LENGTH)
        self.actions: list[tuple[np.ndarray, np.ndarray]] = []
        for u, v in prism_edges():
            bit_u = ((self.carrier_words >> u) & 1).astype(np.int8)
            bit_v = ((self.carrier_words >> v) & 1).astype(np.int8)
            sources = np.flatnonzero(bit_u != bit_v).astype(np.int32)
            mask = np.uint32((1 << (LENGTH + u)) | (1 << (LENGTH + v)))
            destinations = np.fromiter(
                (self.index[int(word ^ mask)] for word in self.words[sources]),
                dtype=np.int32,
                count=len(sources),
            )
            self.actions.append((sources, destinations))
        self.admissions: list[tuple[np.ndarray, np.ndarray]] = []
        for event in range(LENGTH):
            loaded = ((self.words >> event) & 1) == 1
            blank = ((self.carrier_words >> event) & 1) == 0
            sources = np.flatnonzero(loaded & blank).astype(np.int32)
            mask = np.uint32((1 << event) | (1 << (LENGTH + event)))
            destinations = np.fromiter(
                (self.index[int(word ^ mask)] for word in self.words[sources]),
                dtype=np.int32,
                count=len(sources),
            )
            self.admissions.append((sources, destinations))

    def initial(self) -> np.ndarray:
        state = np.zeros(DIMENSION, dtype=np.complex128)
        state[self.index[(1 << LENGTH) - 1]] = 1.0
        return state

    def admission(self, state: np.ndarray, event: int) -> np.ndarray:
        sources, destinations = self.admissions[event]
        out = state.copy()
        left = state[sources]
        right = state[destinations]
        out[sources] = math.cos(PHI) * left - 1j * math.sin(PHI) * right
        out[destinations] = math.cos(PHI) * right - 1j * math.sin(PHI) * left
        require_finite(out, f"admission event {event}")
        return out

    def h_action(self, state: np.ndarray) -> np.ndarray:
        out = np.zeros_like(state)
        for sources, destinations in self.actions:
            out[sources] -= state[destinations]
        require_finite(out, "Hamiltonian action")
        return out

    def transport(self, state: np.ndarray, steps: int) -> np.ndarray:
        evolved = state.copy()
        step = DWELL / steps
        for _ in range(steps):
            updated = evolved.copy()
            term = evolved.copy()
            for order in range(1, ORDER + 1):
                term = (-1j * step / order) * self.h_action(term)
                updated += term
            evolved = updated
        require_finite(evolved, f"transport {steps}")
        return evolved

    def checkpoint(self, steps: int) -> np.ndarray:
        state = self.initial()
        for event in range(LENGTH):
            state = self.admission(state, event)
            state = self.transport(state, steps)
        return state


def labels(parent: IndependentParent) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    loaded_mask = (1 << LENGTH) - 1
    loaded = parent.words & np.uint32(loaded_mask)
    lineage = np.bitwise_xor(loaded, np.uint32(loaded_mask)).astype(np.int64)
    carrier = parent.carrier_words.astype(np.int64)
    q = np.array([bin(int(word)).count("1") for word in lineage], dtype=np.int8)
    return lineage, carrier, q


def build_arms(parent: IndependentParent, state: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    lineage, carrier, q_values = labels(parent)
    actual = np.zeros((DIMENSION, DIMENSION), dtype=np.complex128)
    product = np.zeros_like(actual)
    for q in range(LENGTH + 1):
        indices = np.flatnonzero(q_values == q)
        s_words = np.unique(lineage[indices])
        c_words = np.unique(carrier[indices])
        lookup = {(int(lineage[i]), int(carrier[i])): int(i) for i in indices}
        grid = np.array(
            [lookup[(int(s), int(c))] for s in s_words for c in c_words],
            dtype=np.int64,
        )
        amplitude = state[grid].reshape(len(s_words), len(c_words))
        p_q = float(np.vdot(amplitude, amplitude).real)
        actual[np.ix_(grid, grid)] = np.einsum(
            "i,j->ij", amplitude.ravel(), amplitude.ravel().conj(), optimize=False
        )
        if p_q > 0.0:
            rho_s = np.einsum("sc,tc->st", amplitude, amplitude.conj(), optimize=False)
            rho_c = np.einsum("sc,sd->cd", amplitude, amplitude.conj(), optimize=False)
            # Independent explicit four-index product; no Kronecker helper.
            product_block = np.einsum(
                "st,cd->sctd", rho_s, rho_c, optimize=False
            ).reshape(len(grid), len(grid)) / p_q
            product[np.ix_(grid, grid)] = product_block
    require_finite(actual, "actual input density")
    require_finite(product, "product input density")
    return actual, product


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
    require_finite(rho_s, "lineage marginal")
    require_finite(rho_c, "carrier marginal")
    return rho_s, rho_c


def admission_unitary(parent: IndependentParent) -> np.ndarray:
    unitary = np.eye(DIMENSION, dtype=np.complex128)
    sources, destinations = parent.admissions[EVENT]
    cosine = math.cos(PHI)
    sine = math.sin(PHI)
    unitary[sources, sources] = cosine
    unitary[destinations, destinations] = cosine
    unitary[sources, destinations] = -1j * sine
    unitary[destinations, sources] = -1j * sine
    return unitary


def transport_unitary(parent: IndependentParent) -> tuple[np.ndarray, dict[str, float]]:
    hamiltonian = np.zeros((DIMENSION, DIMENSION), dtype=float)
    for sources, destinations in parent.actions:
        hamiltonian[sources, destinations] -= 1.0
    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
    reconstructed = np.einsum(
        "ia,a,ja->ij", eigenvectors, eigenvalues, eigenvectors, optimize=False
    )
    unitary = np.einsum(
        "ia,a,ja->ij",
        eigenvectors,
        np.exp(-1j * DWELL * eigenvalues),
        eigenvectors,
        optimize=False,
    )
    gram = np.einsum("ji,jk->ik", unitary.conj(), unitary, optimize=False)
    controls = {
        "hamiltonian_hermiticity": float(np.max(np.abs(hamiltonian - hamiltonian.T))),
        "hamiltonian_reconstruction": float(np.max(np.abs(reconstructed - hamiltonian))),
        "transport_unitarity": float(np.max(np.abs(gram - np.eye(DIMENSION)))),
    }
    require_finite(unitary, "transport unitary")
    require_finite_tree(controls, "transport controls")
    return unitary, controls


def evolve_density(unitary: np.ndarray, density: np.ndarray) -> np.ndarray:
    intermediate = np.einsum("ij,jk->ik", unitary, density, optimize=False)
    evolved = np.einsum("ik,lk->il", intermediate, unitary.conj(), optimize=False)
    require_finite(evolved, "evolved density")
    return evolved


def density_controls(density: np.ndarray) -> dict[str, float]:
    hermitian = 0.5 * (density + density.conj().T)
    values = {
        "trace": abs(float(np.trace(density).real) - 1.0),
        "trace_imaginary": abs(float(np.trace(density).imag)),
        "hermiticity": float(np.max(np.abs(density - density.conj().T))),
        "minimum_eigenvalue": float(np.min(np.linalg.eigvalsh(hermitian))),
    }
    require_finite_tree(values, "density controls")
    return values


def carrier_observables(
    actual: np.ndarray, product: np.ndarray, lineage: np.ndarray, carrier: np.ndarray
) -> dict[str, Any]:
    _, sigma_actual = reduced_marginals(actual, lineage, carrier)
    _, sigma_product = reduced_marginals(product, lineage, carrier)
    difference = 0.5 * (
        sigma_actual - sigma_product + (sigma_actual - sigma_product).conj().T
    )
    trace_distance = 0.5 * float(np.sum(np.abs(np.linalg.eigvalsh(difference))))
    diagonal_actual = np.real(np.diag(sigma_actual))
    diagonal_product = np.real(np.diag(sigma_product))
    configuration_tv = 0.5 * float(np.sum(np.abs(diagonal_actual - diagonal_product)))
    delta_n = np.empty(2 * LENGTH, dtype=float)
    for site in range(2 * LENGTH):
        actual_n = 0.0
        product_n = 0.0
        for word in range(1 << (2 * LENGTH)):
            if (word >> site) & 1:
                actual_n += float(diagonal_actual[word])
                product_n += float(diagonal_product[word])
        delta_n[site] = actual_n - product_n
    sector_actual = np.zeros(LENGTH + 1, dtype=float)
    sector_product = np.zeros(LENGTH + 1, dtype=float)
    for word in range(1 << (2 * LENGTH)):
        q = bin(word).count("1")
        if q <= LENGTH:
            sector_actual[q] += diagonal_actual[word]
            sector_product[q] += diagonal_product[word]
    result = {
        "carrier_trace_distance": trace_distance,
        "carrier_configuration_tv": configuration_tv,
        "carrier_number_sector_tv": 0.5 * float(np.sum(np.abs(sector_actual - sector_product))),
        "occupation_rms": float(np.sqrt(np.mean(delta_n * delta_n))),
        "delta_n": delta_n.tolist(),
        "delta_n_0": float(delta_n[0]),
    }
    require_finite_tree(result, "carrier observables")
    return result


def evaluate_resolution(
    parent: IndependentParent,
    state: np.ndarray,
    admission: np.ndarray,
    transport: np.ndarray,
) -> dict[str, Any]:
    lineage, carrier, q_values = labels(parent)
    actual, product = build_arms(parent, state)
    actual_s, actual_c = reduced_marginals(actual, lineage, carrier)
    product_s, product_c = reduced_marginals(product, lineage, carrier)
    controls: dict[str, float] = {
        "carrier_marginal_equality": float(np.max(np.abs(actual_c - product_c))),
        "lineage_marginal_equality": float(np.max(np.abs(actual_s - product_s))),
        "checkpoint_norm": abs(float(np.vdot(state, state).real) - 1.0),
    }
    controls["q_weight_equality"] = max(
        abs(
            float(np.trace(actual[np.ix_(q_values == q, q_values == q)]).real)
            - float(np.trace(product[np.ix_(q_values == q, q_values == q)]).real)
        )
        for q in range(LENGTH + 1)
    )
    admitted_actual = evolve_density(admission, actual)
    admitted_product = evolve_density(admission, product)
    terminal_actual = evolve_density(transport, admitted_actual)
    terminal_product = evolve_density(transport, admitted_product)
    after_admission = carrier_observables(admitted_actual, admitted_product, lineage, carrier)
    after_transport = carrier_observables(terminal_actual, terminal_product, lineage, carrier)
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
        record = density_controls(density)
        minimum_eigenvalue = min(minimum_eigenvalue, record.pop("minimum_eigenvalue"))
        controls.update({f"{label}_{key}": value for key, value in record.items()})
    require_finite_tree(controls, "resolution controls")
    return {
        "after_admission": after_admission,
        "after_transport": after_transport,
        "controls": controls,
        "minimum_density_eigenvalue": minimum_eigenvalue,
    }


def registered_values(row: dict[str, Any]) -> list[float]:
    values: list[float] = []
    for checkpoint in ("after_admission", "after_transport"):
        record = row[checkpoint]
        for key in (
            "carrier_trace_distance",
            "carrier_configuration_tv",
            "carrier_number_sector_tv",
            "occupation_rms",
            "delta_n_0",
        ):
            values.append(float(record[key]))
        values.extend(float(value) for value in record["delta_n"])
    return values


def normalized_ranges_pass(row: dict[str, Any]) -> bool:
    for checkpoint in ("after_admission", "after_transport"):
        for key in (
            "carrier_trace_distance",
            "carrier_configuration_tv",
            "carrier_number_sector_tv",
            "occupation_rms",
        ):
            value = float(row[checkpoint][key])
            if not (-1.0e-12 <= value <= 1.0 + 1.0e-12):
                return False
    return True


def compare_observables(independent: dict[str, Any], target: dict[str, Any]) -> float:
    maximum = 0.0
    for resolution in ("coarse", "fine"):
        for checkpoint in ("after_admission", "after_transport"):
            left = independent[resolution][checkpoint]
            right = target[resolution][checkpoint]
            for key in (
                "carrier_trace_distance",
                "carrier_configuration_tv",
                "carrier_number_sector_tv",
                "occupation_rms",
                "delta_n_0",
            ):
                maximum = max(maximum, abs(float(left[key]) - float(right[key])))
            maximum = max(
                maximum,
                float(np.max(np.abs(np.asarray(left["delta_n"]) - np.asarray(right["delta_n"])))),
            )
    return maximum


def build_result(captured_warnings: Iterable[warnings.WarningMessage]) -> dict[str, Any]:
    custody = authenticate()
    target = json.loads(TARGET_RESULT.read_text())
    require_finite_tree(target, "target result")
    parent = IndependentParent()
    if len(parent.words) != DIMENSION:
        raise AuditFailure("independent basis dimension mismatch")
    basis_hash = array_sha256(parent.words, "<u4")
    if basis_hash != EXPECTED_BASIS_SHA256:
        raise AuditFailure("independent basis fingerprint mismatch")
    coarse_state = parent.checkpoint(COARSE_STEPS)
    fine_state = parent.checkpoint(FINE_STEPS)
    fine_hash = array_sha256(fine_state, "<c16")
    if fine_hash != EXPECTED_FINE_CHECKPOINT_SHA256:
        raise AuditFailure("independent checkpoint fingerprint mismatch")
    admission = admission_unitary(parent)
    admission_gram = np.einsum("ji,jk->ik", admission.conj(), admission, optimize=False)
    admission_residual = float(np.max(np.abs(admission_gram - np.eye(DIMENSION))))
    transport, operator_controls = transport_unitary(parent)
    operator_controls["admission_unitarity"] = admission_residual
    coarse = evaluate_resolution(parent, coarse_state, admission, transport)
    fine = evaluate_resolution(parent, fine_state, admission, transport)
    independent = {"coarse": coarse, "fine": fine}
    coarse_fine = max(
        abs(left - right)
        for left, right in zip(registered_values(coarse), registered_values(fine))
    )
    maximum_residual = max(
        *(abs(value) for value in operator_controls.values()),
        *(abs(value) for value in coarse["controls"].values()),
        *(abs(value) for value in fine["controls"].values()),
    )
    tau = max(BASE_TAU, 50.0 * coarse_fine, 100.0 * maximum_residual)
    delta_c = float(fine["after_transport"]["carrier_trace_distance"])
    t_dyn = delta_c / tau
    classification = (
        "RESOLVED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION"
        if t_dyn > 1.0
        else "FALSIFIED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION_IN_FIXED_TEST"
    )
    runtime_warnings = [
        {"category": item.category.__name__, "message": str(item.message)}
        for item in captured_warnings
    ]
    target_difference = compare_observables(independent, target)
    controls_pass = (
        not runtime_warnings
        and normalized_ranges_pass(coarse)
        and normalized_ranges_pass(fine)
        and coarse_fine <= COARSE_FINE_TOLERANCE
        and maximum_residual <= CONTROL_TOLERANCE
        and coarse["minimum_density_eigenvalue"] >= MINIMUM_EIGENVALUE
        and fine["minimum_density_eigenvalue"] >= MINIMUM_EIGENVALUE
        and target_difference <= VALUE_TOLERANCE
        and classification == target["classification"]
        and abs(delta_c - float(target["fine"]["after_transport"]["carrier_trace_distance"])) <= VALUE_TOLERANCE
        and abs(float(fine["after_transport"]["occupation_rms"]) - float(target["fine"]["after_transport"]["occupation_rms"])) <= VALUE_TOLERANCE
    )
    result = {
        "schema": "INDEPENDENT_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_VALIDATION_V001",
        "passed": controls_pass,
        "disposition": (
            "PASS_INDEPENDENT_L4_LINEAGE_SENSITIVE_CONTINUATION_VALIDATION"
            if controls_pass
            else "FAIL_INDEPENDENT_L4_LINEAGE_SENSITIVE_CONTINUATION_VALIDATION"
        ),
        "claim_boundary": "L4_SINGLE_REVISIT_LINEAGE_SENSITIVE_CARRIER_MECHANISM_ONLY__NO_SCALING_CURVATURE_GEOMETRY_RGRL_WTC_ALPHA_OR_GRAVITY",
        "custody": custody,
        "independence": {
            "imports_target_implementation": False,
            "imports_historical_parent": False,
            "dense_contraction": "NUMPY_EINSUM_OPTIMIZE_FALSE_ONLY",
            "transport": "INDEPENDENT_HERMITIAN_EIGENSYSTEM_WITH_EXPLICIT_SPECTRAL_CONTRACTION",
            "basis_sha256": basis_hash,
            "fine_checkpoint_sha256": fine_hash,
        },
        "warning_audit": {
            "floating_point_policy": "DIVIDE_OVERFLOW_INVALID_RAISE__UNDERFLOW_IGNORED",
            "captured_warnings": runtime_warnings,
            "accepted_on_faith": False,
        },
        "classification": classification,
        "coarse": coarse,
        "fine": fine,
        "tau": tau,
        "T_dyn": t_dyn,
        "controls": {
            "coarse_fine_maximum": coarse_fine,
            "maximum_residual": maximum_residual,
            "operator_controls": operator_controls,
            "normalized_ranges": normalized_ranges_pass(coarse) and normalized_ranges_pass(fine),
            "target_registered_observable_max_abs_difference": target_difference,
            "target_classification_matches": classification == target["classification"],
        },
        "interpretation": {
            "trace_distance": "COMMON_CARRIER_TRANSPORT_INVARIANT__PRIMARY_LINEAGE_READING_RESPONSE",
            "occupation_profile": "TRANSPORT_SENSITIVE_FIXED_DIAGNOSTIC",
            "scope": "MECHANISM_AT_L4_ONLY",
        },
    }
    require_finite_tree(result, "independent result")
    if not controls_pass:
        raise AuditFailure(json.dumps(result["controls"], sort_keys=True))
    return result


def atomic_write(path: Path, result: dict[str, Any]) -> str:
    if path.exists():
        raise AuditFailure(f"refusing to overwrite {path}")
    rendered = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
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


def main() -> None:
    old = np.seterr(divide="raise", over="raise", invalid="raise", under="ignore")
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = build_result(caught)
        digest = atomic_write(OUTPUT, result)
    finally:
        np.seterr(**old)
    print(json.dumps({"disposition": result["disposition"], "sha256": digest}, sort_keys=True))


if __name__ == "__main__":
    main()
