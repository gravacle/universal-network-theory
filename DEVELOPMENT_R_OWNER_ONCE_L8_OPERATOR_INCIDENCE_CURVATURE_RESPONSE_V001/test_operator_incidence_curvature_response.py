#!/usr/bin/env python3
"""Synthetic analytic and hostile-mutation tests for the paused packet."""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import resource
import sys
import tempfile
import time
import unittest
from pathlib import Path

import operator_incidence_curvature_response as target
import preproduction_verifier as verifier


STARTED = time.perf_counter()
MAX_FIXTURE_STORAGE_BYTES = 0


def directory_bytes(root: Path) -> int:
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


def record_fixture_storage(root: Path) -> None:
    global MAX_FIXTURE_STORAGE_BYTES
    MAX_FIXTURE_STORAGE_BYTES = max(MAX_FIXTURE_STORAGE_BYTES, directory_bytes(root))


def point_mass(support: target.Support, vertex: str) -> dict[str, float]:
    return {name: 1.0 if name == vertex else 0.0 for name in support.vertices}


def uniform_conductance(support: target.Support) -> dict[str, float]:
    return {key: 1.0 for key in support.edge_keys}


class FrozenCustodyTests(unittest.TestCase):
    def test_frozen_bytes_and_full_relocation_verifier(self) -> None:
        result = verifier.verify_all_preproduction_inputs()
        self.assertEqual(
            result["status"],
            "PASS_PREPRODUCTION_INPUT_AUTHENTICATION__L8_PRODUCTION_NOT_RUN",
        )
        self.assertFalse(result["l8_numerical_extraction_run"])
        self.assertFalse(result["response_adapter_present"])
        self.assertEqual([record["L"] for record in result["relocation_checks"]], [4, 8])
        for name, expected in verifier.FROZEN_HASHES.items():
            self.assertEqual(verifier.sha256_file(verifier.PACKET / name), expected)

    def test_strict_json_rejects_duplicate_and_nonfinite_mutations(self) -> None:
        hostile = (
            '{"schema":"x","schema":"y"}',
            '{"value":NaN}',
            '{"value":Infinity}',
            '{"value":-Infinity}',
            '{"value":1e9999}',
        )
        for payload in hostile:
            with self.subTest(payload=payload):
                with self.assertRaises(verifier.VerificationError):
                    verifier.strict_json_loads(payload)

    def test_relocation_rejects_prefix_traversal_and_symlink(self) -> None:
        with self.assertRaises(verifier.VerificationError):
            verifier.relocate_historical_path(
                "/wrong/root/q_00.npy", "q_00.npy"
            )
        with self.assertRaises(verifier.VerificationError):
            verifier.relocate_historical_path(
                verifier.HISTORICAL_ROOT_PREFIX + "../q_00.npy", "../q_00.npy"
            )
        with tempfile.TemporaryDirectory(dir=verifier.PACKET) as temporary_name:
            temporary = Path(temporary_name)
            plain = temporary / "plain.npy"
            plain.write_bytes(b"not an npy")
            link = temporary / "link.npy"
            link.symlink_to(plain)
            relative = str(link.relative_to(verifier.ROOT))
            historical = verifier.HISTORICAL_ROOT_PREFIX + relative
            record_fixture_storage(temporary)
            with self.assertRaises(verifier.VerificationError):
                verifier.relocate_historical_path(historical, relative)

    def test_preproduction_outputs_and_response_adapter_remain_absent(self) -> None:
        self.assertFalse((verifier.PACKET / "L8_OPERATOR_INCIDENCE_CONDUCTANCE_V001.json").exists())
        self.assertFalse((verifier.PACKET / "RESULT.json").exists())
        self.assertFalse(any(
            path.is_file() and "L8_ALL_EVENT_AUTONOMOUS_LINEAGE_RESPONSE" in path.name
            for path in verifier.PACKET.iterdir()
        ))


class SupportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.support = target.build_support(8)

    def test_primitive_support_has_shifted_connectors(self) -> None:
        support = self.support
        self.assertEqual(len(support.vertices), 24)
        self.assertEqual(len(support.admission_edges), 8)
        self.assertEqual(len(support.transport_edges), 24)
        self.assertEqual(len(support.edges), 32)
        connectors = set(support.transport_edges[-8:])
        shifted = {(f"C_{site}", f"C_{8 + (site + 1) % 8}") for site in range(8)}
        aligned = {(f"C_{site}", f"C_{8 + site}") for site in range(8)}
        self.assertEqual(connectors, shifted)
        self.assertNotEqual(connectors, aligned)

    def test_no_pruning_and_connected_unit_metric(self) -> None:
        metric = target.all_pairs_shortest_path(self.support)
        self.assertEqual(set(metric), set(self.support.vertices))
        for edge in self.support.edges:
            self.assertEqual(metric[edge[0]][edge[1]], 1)


class IndependentW1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.support = target.build_support(8)
        cls.metric = target.all_pairs_shortest_path(cls.support)

    def assertRoutesAgree(
        self,
        first: dict[str, float],
        second: dict[str, float],
        places: int = 12,
    ) -> tuple[float, float]:
        complete = target.w1_complete_metric_transport(
            self.support, first, second, self.metric
        )
        transshipment = target.w1_fixed_support_transshipment(
            self.support, first, second
        )
        self.assertAlmostEqual(complete, transshipment, places=places)
        return complete, transshipment

    def test_point_mass_distance_analytic_cases(self) -> None:
        pairs = [
            ("F_0", "C_0"),
            ("F_0", "C_8"),
            ("C_0", "C_4"),
            ("F_3", "F_7"),
        ]
        for left, right in pairs:
            with self.subTest(left=left, right=right):
                complete, _ = self.assertRoutesAgree(
                    point_mass(self.support, left), point_mass(self.support, right)
                )
                self.assertEqual(complete, float(self.metric[left][right]))

    def test_uniform_admission_edge_analytic_value(self) -> None:
        conductance = uniform_conductance(self.support)
        first = target.lazy_measure(self.support, conductance, "F_0")
        second = target.lazy_measure(self.support, conductance, "C_0")
        complete, _ = self.assertRoutesAgree(first, second)
        self.assertAlmostEqual(complete, 0.75, places=14)
        self.assertAlmostEqual(1.0 - complete, 0.25, places=14)

    def test_random_weighted_lazy_measures_agree_on_every_edge(self) -> None:
        generator = random.Random(20260927)
        for case in range(4):
            conductance = {
                key: 10.0 ** generator.uniform(-2.0, 1.0)
                for key in self.support.edge_keys
            }
            for edge in self.support.edges:
                with self.subTest(case=case, edge=edge):
                    self.assertRoutesAgree(
                        target.lazy_measure(self.support, conductance, edge[0]),
                        target.lazy_measure(self.support, conductance, edge[1]),
                        places=11,
                    )

    def test_routes_do_not_call_each_other(self) -> None:
        conductance = uniform_conductance(self.support)
        first = target.lazy_measure(self.support, conductance, "F_1")
        second = target.lazy_measure(self.support, conductance, "C_1")
        original_complete = target.w1_complete_metric_transport
        original_control = target.w1_fixed_support_transshipment
        try:
            target.w1_complete_metric_transport = lambda *_args, **_kwargs: (_ for _ in ()).throw(
                AssertionError("complete route called")
            )
            self.assertAlmostEqual(original_control(self.support, first, second), 0.75)
            target.w1_complete_metric_transport = original_complete
            target.w1_fixed_support_transshipment = lambda *_args, **_kwargs: (_ for _ in ()).throw(
                AssertionError("control route called")
            )
            self.assertAlmostEqual(
                original_complete(self.support, first, second, self.metric), 0.75
            )
        finally:
            target.w1_complete_metric_transport = original_complete
            target.w1_fixed_support_transshipment = original_control

    def test_zero_weighted_degree_is_fail_closed(self) -> None:
        zero = {key: 0.0 for key in self.support.edge_keys}
        with self.assertRaises(target.CurvatureError):
            target.lazy_measure(self.support, zero, "F_0")


class StatisticTests(unittest.TestCase):
    def test_exact_midranks_and_tied_spearman(self) -> None:
        values = [1.0, 1.0, 4.0, 2.0]
        self.assertEqual(target.midranks(values), [1.5, 1.5, 4.0, 3.0])
        self.assertAlmostEqual(target.spearman_midrank(values, values), 1.0)
        self.assertAlmostEqual(
            target.spearman_midrank(values, [-value for value in values]), -1.0
        )

    def test_exact_all_40320_permutations(self) -> None:
        statistic = target.exact_l8_permutation_statistics(
            list(range(8)), list(range(8))
        )
        self.assertEqual(statistic["permutation_count"], math.factorial(8))
        self.assertEqual(statistic["absolute_tail_count"], 2)
        self.assertEqual(statistic["plus_tail_count"], 1)
        self.assertAlmostEqual(statistic["p_abs"], 2.0 / 40320.0)
        self.assertAlmostEqual(statistic["p_plus"], 1.0 / 40320.0)

    def test_zero_variance_is_fail_closed(self) -> None:
        with self.assertRaises(target.CurvatureError):
            target.spearman_midrank([1.0] * 8, list(range(8)))


class AdapterAndPublicationTests(unittest.TestCase):
    def synthetic_response(self) -> dict[str, object]:
        return target.seal_payload({
            "schema": target.RESPONSE_SCHEMA,
            "definition": target.RESPONSE_DEFINITION,
            "labels": list(range(8)),
            "carrier_configuration_tv_by_event": [
                0.08, 0.16, 0.31, 0.29, 0.52, 0.66, 0.61, 0.91,
            ],
            "provenance": {
                "fixture": "SYNTHETIC_TEST_ONLY",
                "not_production": True,
            },
        })

    def test_response_seal_and_hostile_mutations(self) -> None:
        response = self.synthetic_response()
        self.assertEqual(len(target.validate_response_adapter(response)), 8)
        mutations = []
        bad_label = json.loads(json.dumps(response))
        bad_label["labels"][0] = 7
        mutations.append(bad_label)
        bad_range = json.loads(json.dumps(response))
        bad_range["carrier_configuration_tv_by_event"][0] = 1.01
        mutations.append(bad_range)
        missing_provenance = json.loads(json.dumps(response))
        missing_provenance["provenance"] = {}
        mutations.append(missing_provenance)
        bad_seal = json.loads(json.dumps(response))
        bad_seal["seal"] = "0" * 64
        mutations.append(bad_seal)
        for mutation in mutations:
            with self.subTest(keys=mutation.keys()):
                with self.assertRaises(target.CurvatureError):
                    target.validate_response_adapter(mutation)

    def test_synthetic_sealed_adapter_pipeline_including_exact_null(self) -> None:
        support = target.build_support(8)
        actual = uniform_conductance(support)
        product = dict(actual)
        for event, edge in enumerate(support.admission_edges):
            product[target.edge_key(edge)] = 0.25 + 0.08 * event
        conductance = target.seal_payload({
            "schema": target.CONDUCTANCE_SCHEMA,
            "status": "SEALED_L8_CONDUCTANCE_ADAPTER",
            "L": 8,
            "support": support.as_json(),
            "conductance_actual": actual,
            "conductance_same_q_product": product,
            "source": {
                "fixture": "SYNTHETIC_TEST_ONLY",
                "not_an_L8_extraction": True,
            },
            "claim_boundary": verifier.CLAIM_BOUNDARY,
        })
        result = target.analyze_sealed_l8_adapters(
            conductance, self.synthetic_response()
        )
        self.assertEqual(result["statistic"]["permutation_count"], 40320)
        self.assertLessEqual(
            result["controls"]["maximum_solver_disagreement"],
            target.SOLVER_TOLERANCE,
        )
        self.assertEqual(
            result["controls"]["maximum_transport_conductance_difference"], 0.0
        )
        hostile = json.loads(json.dumps(conductance))
        hostile["support"]["transport_edges"][-1] = ["C_7", "C_15"]
        with self.assertRaises(target.CurvatureError):
            target.validate_conductance_adapter(hostile)

    def test_atomic_publication_refuses_overwrite_and_symlink(self) -> None:
        with tempfile.TemporaryDirectory(dir=verifier.PACKET) as temporary_name:
            temporary = Path(temporary_name)
            destination = temporary / "record.json"
            payload = {"schema": "SYNTHETIC_PUBLICATION_TEST", "value": 7}
            record = target.atomic_publish_json(destination, payload)
            first_bytes = destination.read_bytes()
            self.assertEqual(first_bytes, target.canonical_json_bytes(payload) + b"\n")
            self.assertEqual(record["sha256"], hashlib.sha256(first_bytes).hexdigest())
            with self.assertRaises(target.PublicationError):
                target.atomic_publish_json(destination, {"value": 8})
            self.assertEqual(destination.read_bytes(), first_bytes)
            link = temporary / "link.json"
            link.symlink_to(destination)
            with self.assertRaises(target.PublicationError):
                target.atomic_publish_json(link, {"value": 9})
            record_fixture_storage(temporary)

    def test_atomic_publication_rejects_nonfinite_without_residue(self) -> None:
        with tempfile.TemporaryDirectory(dir=verifier.PACKET) as temporary_name:
            temporary = Path(temporary_name)
            destination = temporary / "bad.json"
            with self.assertRaises(target.CurvatureError):
                target.atomic_publish_json(destination, {"value": math.nan})
            self.assertFalse(destination.exists())
            self.assertEqual(list(temporary.iterdir()), [])

    def test_unauthorized_production_refuses_before_any_adapter(self) -> None:
        with self.assertRaises(target.ProductionNotAuthorized):
            target.require_l8_conductance_extraction_authorization()
        with self.assertRaises(target.ProductionNotAuthorized):
            target.require_l8_join_authorization()


class DenseL4DevelopmentTests(unittest.TestCase):
    def test_authenticated_dense_l4_conductance_and_w1_check(self) -> None:
        result = target.run_development_l4_check()
        self.assertEqual(
            result["status"],
            "PASS_AUTHENTICATED_DENSE_L4_DEVELOPMENT_CHECK__NO_L8_INFERENCE",
        )
        self.assertEqual(result["L"], 4)
        self.assertEqual(len(result["support"]["vertices"]), 12)
        self.assertEqual(len(result["support"]["admission_edges"]), 4)
        self.assertEqual(len(result["support"]["transport_edges"]), 12)
        self.assertLessEqual(
            result["controls"]["independent_w1_solver_max_abs"],
            result["controls"]["independent_w1_solver_tolerance"],
        )
        self.assertEqual(
            result["controls"]["transport_conductance_preservation_max_abs"], 0.0
        )
        self.assertFalse(result["controls"]["l8_production_run"])
        self.assertEqual(result["scientific_status"], verifier.UNRESOLVED)
        self.assertEqual(result["claim_boundary"], verifier.CLAIM_BOUNDARY)
        self.assertTrue(all(
            math.isfinite(value)
            for value in result["admission_predictor_actual_minus_product"]
        ))


def maximum_rss_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else value * 1024


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    outcome = unittest.TextTestRunner(verbosity=2).run(suite)
    record = {
        "schema": "L8_OPERATOR_INCIDENCE_CURVATURE_TEST_RESOURCE_OBSERVATION_V001",
        "tests_run": outcome.testsRun,
        "failures": len(outcome.failures),
        "errors": len(outcome.errors),
        "successful": outcome.wasSuccessful(),
        "wall_seconds": time.perf_counter() - STARTED,
        "maximum_rss_bytes": maximum_rss_bytes(),
        "maximum_logical_fixture_storage_bytes": MAX_FIXTURE_STORAGE_BYTES,
        "packet_logical_storage_bytes": directory_bytes(verifier.PACKET),
        "persistent_test_outputs_created": 0,
        "l8_production_run": False,
        "scientific_status": verifier.UNRESOLVED,
        "claim_boundary": verifier.CLAIM_BOUNDARY,
    }
    print("TEST_RESOURCE_JSON=" + json.dumps(record, sort_keys=True, allow_nan=False))
    raise SystemExit(0 if outcome.wasSuccessful() else 1)
