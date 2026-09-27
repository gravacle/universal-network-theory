#!/usr/bin/env python3

from __future__ import annotations

import math
import unittest

import numpy as np

import target_lineage_scaling as target


class SignedLowRankTests(unittest.TestCase):
    def test_qr_eigensystem_matches_explicit_density(self) -> None:
        rng = np.random.default_rng(20260927)
        actual = rng.normal(size=(9, 5)) + 1.0j * rng.normal(size=(9, 5))
        product = rng.normal(size=(9, 7)) + 1.0j * rng.normal(size=(9, 7))
        actual[:, 4] = actual[:, 1] - 2.0 * actual[:, 2]
        product[:, 6] = product[:, 0]
        actual /= math.sqrt(float(np.sum(np.abs(actual) ** 2)))
        product /= math.sqrt(float(np.sum(np.abs(product) ** 2)))
        observed = target.signed_low_rank_metrics(actual, product)
        difference = actual @ actual.conj().T - product @ product.conj().T
        difference = (difference + difference.conj().T) / 2.0
        expected_trace = 0.5 * float(np.sum(np.abs(np.linalg.eigvalsh(difference))))
        expected_tv = 0.5 * float(np.sum(np.abs(np.diag(difference).real)))
        self.assertLess(abs(observed["carrier_trace_distance"] - expected_trace), 2.0e-14)
        self.assertLess(abs(observed["carrier_configuration_tv"] - expected_tv), 2.0e-14)
        self.assertLess(observed["controls"]["qr_reconstruction"], 2.0e-14)
        self.assertLess(observed["controls"]["reduced_hermiticity"], 2.0e-14)

    def test_zero_difference_is_exact_control(self) -> None:
        factor = np.array(
            [[1.0, 0.0], [0.0, 0.5j], [0.25, -0.25j]], dtype=np.complex128
        )
        observed = target.signed_low_rank_metrics(factor, factor.copy())
        self.assertLess(observed["carrier_trace_distance"], 1.0e-14)
        self.assertEqual(observed["carrier_configuration_tv"], 0.0)


class FactorAdmissionTests(unittest.TestCase):
    LENGTH = 2
    EVENT = 0
    Q = 1

    def setUp(self) -> None:
        values = np.arange(1, 9, dtype=float).reshape(2, 4)
        self.amplitude = values + 1.0j * values[::-1, ::-1]
        self.amplitude = 0.61 * self.amplitude / np.linalg.norm(self.amplitude)

    def explicit_inputs(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        length = self.LENGTH
        lineage_dimension = 1 << length
        carrier_dimension = 1 << (2 * length)
        total = lineage_dimension * carrier_dimension
        lineage_words = target.fixed_words(length, self.Q)
        carrier_words = target.fixed_words(2 * length, self.Q)
        sector_weight = float(np.vdot(self.amplitude, self.amplitude).real)
        rho_s = self.amplitude @ self.amplitude.conj().T
        rho_c = self.amplitude.T @ self.amplitude.conj()
        actual_vector = np.zeros(total, dtype=np.complex128)
        grid = []
        for lineage_index, lineage_word in enumerate(lineage_words):
            for carrier_index, carrier_word in enumerate(carrier_words):
                index = int(lineage_word) * carrier_dimension + int(carrier_word)
                grid.append(index)
                actual_vector[index] = self.amplitude[lineage_index, carrier_index]
        product = np.zeros((total, total), dtype=np.complex128)
        product[np.ix_(grid, grid)] = np.kron(rho_s, rho_c) / sector_weight
        actual = np.outer(actual_vector, actual_vector.conj())

        unitary = np.eye(total, dtype=np.complex128)
        cosine = math.cos(math.pi / 4.0)
        sine = math.sin(math.pi / 4.0)
        for lineage_word in range(lineage_dimension):
            if (lineage_word >> self.EVENT) & 1:
                continue
            for carrier_word in range(carrier_dimension):
                if (carrier_word >> self.EVENT) & 1:
                    continue
                source = lineage_word * carrier_dimension + carrier_word
                destination = (
                    (lineage_word | (1 << self.EVENT)) * carrier_dimension
                    + (carrier_word | (1 << self.EVENT))
                )
                unitary[source, source] = cosine
                unitary[destination, destination] = cosine
                unitary[source, destination] = -1.0j * sine
                unitary[destination, source] = -1.0j * sine
        return unitary, actual, product

    def reduce_carrier(self, density: np.ndarray) -> np.ndarray:
        lineage_dimension = 1 << self.LENGTH
        carrier_dimension = 1 << (2 * self.LENGTH)
        reshaped = density.reshape(
            lineage_dimension,
            carrier_dimension,
            lineage_dimension,
            carrier_dimension,
        )
        return np.einsum("scsd->cd", reshaped, optimize=False)

    def embed_factors(self, blocks: dict[int, list[np.ndarray] | np.ndarray]) -> np.ndarray:
        carrier_dimension = 1 << (2 * self.LENGTH)
        result = np.zeros((carrier_dimension, carrier_dimension), dtype=np.complex128)
        for q, raw in blocks.items():
            factors = raw if isinstance(raw, list) else [raw]
            words = target.fixed_words(2 * self.LENGTH, q)
            for factor in factors:
                result[np.ix_(words, words)] += factor @ factor.conj().T
        return result

    def test_actual_and_product_factors_match_explicit_joint_evolution(self) -> None:
        unitary, actual, product = self.explicit_inputs()
        actual_expected = self.reduce_carrier(unitary @ actual @ unitary.conj().T)
        product_expected = self.reduce_carrier(unitary @ product @ unitary.conj().T)
        actual_blocks = target.actual_admission_factors(
            self.LENGTH, self.EVENT, self.Q, self.amplitude
        )
        product_blocks = target.product_admission_factors(
            self.LENGTH, self.EVENT, self.Q, self.amplitude
        )
        actual_observed = self.embed_factors(actual_blocks)
        product_observed = self.embed_factors(product_blocks)
        self.assertLess(float(np.max(np.abs(actual_observed - actual_expected))), 3.0e-16)
        self.assertLess(float(np.max(np.abs(product_observed - product_expected))), 3.0e-16)


class AuthenticationAndLockTests(unittest.TestCase):
    def test_all_retained_lower_l_shards_authenticate(self) -> None:
        authenticated = target.authenticate_all_inputs()
        self.assertEqual(set(authenticated["histories"]), {"4", "6", "8"})
        self.assertEqual(
            sum(len(record["shards"]) for record in authenticated["histories"].values()),
            18,
        )

    def test_l6_and_l8_execution_remain_locked(self) -> None:
        target.validate_execution_length(4)
        for length in (6, 8):
            with self.assertRaises(target.ScalingError):
                target.validate_execution_length(length)

    def test_authenticated_resume_runtime_is_available(self) -> None:
        _durable, runtime = target.load_resume_runtime()
        self.assertEqual(runtime.IDENTITY_SCHEMA, "L14_RESUMABLE_RUN_IDENTITY_V002")
        self.assertEqual(runtime.RESULT_SCHEMA, "L14_RESUMABLE_TASK_RESULT_V002")


if __name__ == "__main__":
    unittest.main()
