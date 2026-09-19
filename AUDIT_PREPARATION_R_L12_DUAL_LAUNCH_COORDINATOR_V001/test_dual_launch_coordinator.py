#!/usr/bin/env python3
"""Independent callability, DAG, immutability, and refusal tests."""

from __future__ import annotations

import ast
import itertools
import math
import unittest
from copy import deepcopy
from pathlib import Path

from dual_launch_coordinator import (
    ROLES,
    DualLaunchCoordinator,
    LaunchPolicy,
    Refusal,
    RolePaths,
    parse_strict_json,
    public_signature_census,
    release_ack_sha256,
)
from synthetic_fixtures import EPOCH, fresh_bundle, valid_coordinator_through


class CoordinatorTests(unittest.TestCase):
    def coordinator(self, bundle: dict[str, object]) -> DualLaunchCoordinator:
        return DualLaunchCoordinator(bundle["policy"], bundle["evaluation_epoch"])

    def apply(self, coordinator: DualLaunchCoordinator, bundle: dict[str, object], name: str):
        methods = {
            "schedule": coordinator.admit_schedule,
            "schedule_audit": coordinator.admit_schedule_audit,
            "target_authorization": coordinator.admit_authorization,
            "hostile_authorization": coordinator.admit_authorization,
            "handshake": coordinator.commit_handshake,
            "release": coordinator.release_workers,
            "target_ack": lambda _record: coordinator.admit_release_ack(
                bundle["release_commands"]["target_v012"],
                bundle["release_acks"]["target_v012"],
            ),
            "hostile_ack": lambda _record: coordinator.admit_release_ack(
                bundle["release_commands"]["hostile_v004r4"],
                bundle["release_acks"]["hostile_v004r4"],
            ),
            "target_completion": lambda _record: coordinator.admit_worker_completion(
                bundle["completions"]["target_v012"],
            ),
            "hostile_completion": lambda _record: coordinator.admit_worker_completion(
                bundle["completions"]["hostile_v004r4"],
            ),
            "telemetry": coordinator.admit_postrun_telemetry,
        }
        return methods[name](bundle.get(name))

    def assert_refusal_without_mutation(self, coordinator, call, *args):
        before = coordinator.state_snapshot()
        with self.assertRaises(Refusal):
            call(*args)
        self.assertEqual(before, coordinator.state_snapshot())

    def test_public_api_signatures_are_exact_and_callable(self):
        expected = {
            "admit_schedule": ("self", "record"),
            "admit_schedule_audit": ("self", "record"),
            "admit_authorization": ("self", "record"),
            "commit_handshake": ("self", "record"),
            "release_workers": ("self", "record"),
            "release_command": ("self", "role"),
            "admit_release_ack": ("self", "command", "record"),
            "admit_worker_completion": ("self", "record"),
            "admit_postrun_telemetry": ("self", "record"),
        }
        self.assertEqual(public_signature_census(), expected)
        self.assertEqual(valid_coordinator_through().stage, "TELEMETRY_ACCEPTED")

    def test_both_authorization_sibling_orders_pass(self):
        for auth_order in (
            ("target_authorization", "hostile_authorization"),
            ("hostile_authorization", "target_authorization"),
        ):
            bundle = fresh_bundle()
            coordinator = self.coordinator(bundle)
            self.apply(coordinator, bundle, "schedule")
            self.apply(coordinator, bundle, "schedule_audit")
            for name in auth_order:
                self.apply(coordinator, bundle, name)
            self.apply(coordinator, bundle, "handshake")
            decision = self.apply(coordinator, bundle, "release")
            self.assertEqual(set(decision.release_token_sha256_by_role), set(ROLES))
            self.apply(coordinator, bundle, "target_ack")
            self.apply(coordinator, bundle, "hostile_ack")
            self.apply(coordinator, bundle, "target_completion")
            self.apply(coordinator, bundle, "hostile_completion")
            self.apply(coordinator, bundle, "telemetry")
            self.assertEqual(coordinator.stage, "TELEMETRY_ACCEPTED")

    def test_all_eight_exact_topological_orders_complete(self):
        completed = []
        for auth_order, ack_order, completion_order in itertools.product(
            itertools.permutations(("target_authorization", "hostile_authorization")),
            itertools.permutations(("target_ack", "hostile_ack")),
            itertools.permutations(("target_completion", "hostile_completion")),
        ):
            order = (
                "schedule", "schedule_audit", *auth_order, "handshake", "release",
                *ack_order, *completion_order, "telemetry",
            )
            bundle = fresh_bundle()
            coordinator = self.coordinator(bundle)
            for name in order:
                self.apply(coordinator, bundle, name)
            if coordinator.stage == "TELEMETRY_ACCEPTED":
                completed.append(order)
        self.assertEqual(len(completed), 8)

    def test_every_action_at_every_canonical_boundary_is_state_safe(self):
        names = (
            "schedule", "schedule_audit", "target_authorization",
            "hostile_authorization", "handshake", "release", "target_ack",
            "hostile_ack", "target_completion", "hostile_completion", "telemetry",
        )
        canonical = (
            "schedule", "schedule_audit", "target_authorization",
            "hostile_authorization", "handshake", "release", "target_ack",
            "hostile_ack", "target_completion", "hostile_completion", "telemetry",
        )
        for boundary in range(len(canonical) + 1):
            for candidate in names:
                bundle = fresh_bundle()
                coordinator = self.coordinator(bundle)
                for name in canonical[:boundary]:
                    self.apply(coordinator, bundle, name)
                before = coordinator.state_snapshot()
                try:
                    self.apply(coordinator, bundle, candidate)
                except Refusal:
                    self.assertEqual(before, coordinator.state_snapshot())

    def test_duplicate_nodes_and_duplicate_role_refuse_without_mutation(self):
        bundle = fresh_bundle()
        coordinator = self.coordinator(bundle)
        self.apply(coordinator, bundle, "schedule")
        self.assert_refusal_without_mutation(
            coordinator, coordinator.admit_schedule, bundle["schedule"]
        )
        self.apply(coordinator, bundle, "schedule_audit")
        self.assert_refusal_without_mutation(
            coordinator, coordinator.admit_schedule_audit, bundle["schedule_audit"]
        )
        self.apply(coordinator, bundle, "target_authorization")
        self.assert_refusal_without_mutation(
            coordinator, coordinator.admit_authorization,
            bundle["target_authorization"],
        )

    def test_schedule_freshness_is_rechecked_at_every_live_admission(self):
        stages = (
            ("schedule_audit", "admit_schedule_audit"),
            ("target_authorization", "admit_authorization"),
            ("handshake", "commit_handshake"),
            ("release", "release_workers"),
            ("target_ack", "admit_release_ack"),
        )
        predecessors = {
            "schedule_audit": "schedule",
            "target_authorization": "schedule_audit",
            "handshake": "hostile_authorization",
            "release": "handshake",
            "target_ack": "release",
        }
        for stage, method_name in stages:
            bundle = fresh_bundle()
            coordinator = valid_coordinator_through(predecessors[stage])
            coordinator._constructed_monotonic -= (
                coordinator.policy.maximum_schedule_age_seconds + 301
            )
            if stage == "target_ack":
                args = (
                    bundle["release_commands"]["target_v012"],
                    bundle["release_acks"]["target_v012"],
                )
            else:
                args = (bundle[stage],)
            self.assert_refusal_without_mutation(
                coordinator, getattr(coordinator, method_name), *args,
            )
        coordinator = valid_coordinator_through("release")
        coordinator._constructed_monotonic -= (
            coordinator.policy.maximum_schedule_age_seconds + 301
        )
        self.assert_refusal_without_mutation(
            coordinator, coordinator.release_command, "target_v012",
        )
        coordinator = valid_coordinator_through("hostile_completion")
        coordinator._constructed_monotonic -= (
            coordinator.policy.per_process_wall_limit_seconds
        )
        coordinator.admit_postrun_telemetry(fresh_bundle()["telemetry"])
        self.assertEqual(coordinator.stage, "TELEMETRY_ACCEPTED")

    def test_schedule_refusal_matrix(self):
        mutations = []
        base = fresh_bundle()["schedule"]
        for path, value in (
            (("resource_snapshot", "memory_pressure"), "WARN"),
            (("resource_snapshot", "available_memory_bytes"), 34_865_626_527),
            (("resource_snapshot", "host_physical_memory_bytes"), 47_999_999_999),
            (("resource_snapshot", "workspace_free_disk_bytes"), 19_201_889_579),
            (("resource_snapshot", "workspace_filesystem_device"), True),
            (("resource_snapshot", "passes"), 1),
            (("roles", "target_v012", "worker_executable_path"), None),
            (("roles", "target_v012", "workspace_path"), "relative/workspace"),
            (("roles", "target_v012", "output_path"), "/synthetic/v012/x/../out"),
            (("telemetry", "absent_at_schedule_capture"), False),
            (("schedule", "mapped_peak_limit_bytes_by_role", "target_v012"),
             252_944_080.0),
            (("created_epoch",), float(EPOCH - 100)),
            (("expires_epoch",), EPOCH + 201),
        ):
            mutant = deepcopy(base)
            cursor = mutant
            for key in path[:-1]:
                cursor = cursor[key]
            cursor[path[-1]] = value
            mutations.append(mutant)
        missing = deepcopy(base)
        del missing["telemetry"]
        mutations.append(missing)
        extra = deepcopy(base)
        extra["unexpected"] = None
        mutations.append(extra)
        alias = deepcopy(base)
        alias["roles"]["hostile_v004r4"]["workspace_path"] = \
            alias["roles"]["target_v012"]["workspace_path"]
        mutations.append(alias)
        for mutant in mutations:
            bundle = fresh_bundle()
            coordinator = self.coordinator(bundle)
            self.assert_refusal_without_mutation(coordinator, coordinator.admit_schedule, mutant)

    def test_audit_and_authorization_refusal_matrix(self):
        bundle = fresh_bundle()
        coordinator = self.coordinator(bundle)
        self.apply(coordinator, bundle, "schedule")
        for mutation in (
            ("schedule_sha256", "0" * 64),
            ("checks_total", 11.0),
            ("failures", ["invented"]),
        ):
            mutant = deepcopy(bundle["schedule_audit"])
            mutant[mutation[0]] = mutation[1]
            self.assert_refusal_without_mutation(
                coordinator, coordinator.admit_schedule_audit, mutant
            )
        self.apply(coordinator, bundle, "schedule_audit")
        for role_key in ("target_authorization", "hostile_authorization"):
            for key, value in (
                ("authorized_length", True),
                ("schedule_audit_sha256", "1" * 64),
                ("l10_cross_gate_sha256", "2" * 64),
                ("consumer_sha256", None),
            ):
                mutant = deepcopy(bundle[role_key])
                mutant[key] = value
                self.assert_refusal_without_mutation(
                    coordinator, coordinator.admit_authorization, mutant
                )
            circular = deepcopy(bundle[role_key])
            circular["dual_launch_handshake_sha256"] = "3" * 64
            self.assert_refusal_without_mutation(
                coordinator, coordinator.admit_authorization, circular
            )

    def test_handshake_refusal_matrix_and_original_mutation_isolated(self):
        bundle = fresh_bundle()
        coordinator = self.coordinator(bundle)
        for name in (
            "schedule", "schedule_audit", "target_authorization", "hostile_authorization",
        ):
            self.apply(coordinator, bundle, name)
        base = bundle["handshake"]
        mutants = []
        wrong_auth = deepcopy(base)
        wrong_auth["authorization_sha256_by_role"]["target_v012"] = "0" * 64
        mutants.append(wrong_auth)
        one_role = deepcopy(base)
        del one_role["workers"]["hostile_v004r4"]
        mutants.append(one_role)
        alias_pid = deepcopy(base)
        alias_pid["workers"]["hostile_v004r4"]["process_id"] = 41001
        mutants.append(alias_pid)
        not_blocked = deepcopy(base)
        not_blocked["workers"]["target_v012"]["blocked_on_release"] = False
        mutants.append(not_blocked)
        wrong_path_type = deepcopy(base)
        wrong_path_type["workers"]["target_v012"]["workspace_path"] = ["bad"]
        mutants.append(wrong_path_type)
        pressure = deepcopy(base)
        pressure["memory_pressure"] = "WARN"
        mutants.append(pressure)
        skew = deepcopy(base)
        skew["workers"]["target_v012"]["ready_epoch"] = EPOCH - 60
        skew["workers"]["hostile_v004r4"]["ready_epoch"] = EPOCH + 10
        skew["observed_readiness_skew_seconds"] = 70
        mutants.append(skew)
        false_skew = deepcopy(base)
        false_skew["observed_readiness_skew_seconds"] = 9
        mutants.append(false_skew)
        for mutant in mutants:
            self.assert_refusal_without_mutation(
                coordinator, coordinator.commit_handshake, mutant
            )
        original = deepcopy(base)
        digest = coordinator.commit_handshake(original)
        original["workers"]["target_v012"]["process_id"] = 99999
        self.assertEqual(coordinator.accepted_sha256("handshake"), digest)
        self.assertEqual(
            coordinator.accepted_record("handshake")["workers"]["target_v012"]["process_id"],
            41001,
        )

    def test_release_refusal_matrix(self):
        bundle = fresh_bundle()
        premature = valid_coordinator_through("hostile_authorization")
        self.assert_refusal_without_mutation(
            premature, premature.release_workers, bundle["release"]
        )
        coordinator = valid_coordinator_through("handshake")
        base = bundle["release"]
        mutants = []
        wrong_handshake = deepcopy(base)
        wrong_handshake["handshake_sha256"] = "0" * 64
        mutants.append(wrong_handshake)
        wrong_auth = deepcopy(base)
        wrong_auth["authorization_sha256_by_role"]["hostile_v004r4"] = "1" * 64
        mutants.append(wrong_auth)
        before_handshake = deepcopy(base)
        before_handshake["release_epoch_by_role"] = {
            "target_v012": EPOCH, "hostile_v004r4": EPOCH + 1,
        }
        before_handshake["observed_launch_skew_seconds"] = 1
        mutants.append(before_handshake)
        false_skew = deepcopy(base)
        false_skew["observed_launch_skew_seconds"] = 2
        mutants.append(false_skew)
        wrong_token = deepcopy(base)
        wrong_token["release_by_role"]["target_v012"]["release_token_sha256"] = "2" * 64
        mutants.append(wrong_token)
        wrong_pid_type = deepcopy(base)
        wrong_pid_type["release_by_role"]["target_v012"]["process_id"] = 41001.0
        mutants.append(wrong_pid_type)
        for mutant in mutants:
            self.assert_refusal_without_mutation(
                coordinator, coordinator.release_workers, mutant
            )

    def test_release_command_and_nonce_ack_refusal_matrix(self):
        bundle = fresh_bundle()
        coordinator = valid_coordinator_through("release")
        for role in ROLES:
            self.assertEqual(
                coordinator.release_command(role),
                bundle["release_commands"][role],
            )
        cases = []
        for role in ROLES:
            command = bundle["release_commands"][role]
            ack = bundle["release_acks"][role]
            wrong_command = deepcopy(command)
            wrong_command["worker_release_sha256"] = "0" * 64
            cases.append((wrong_command, ack))
            wrong_nonce = deepcopy(ack)
            wrong_nonce["nonce_hex"] = "0" * 64
            cases.append((command, wrong_nonce))
            wrong_ack = deepcopy(ack)
            wrong_ack["ack_sha256"] = "1" * 64
            cases.append((command, wrong_ack))
            wrong_pid = deepcopy(ack)
            wrong_pid["process_id"] += 100
            cases.append((command, wrong_pid))
            float_epoch_command = deepcopy(command)
            float_epoch_command["release_epoch"] = float(
                command["release_epoch"]
            )
            float_epoch_ack = deepcopy(ack)
            nonce = bytes.fromhex(float_epoch_ack["nonce_hex"])
            float_epoch_ack["ack_sha256"] = release_ack_sha256(
                nonce, float_epoch_command,
            )
            cases.append((float_epoch_command, float_epoch_ack))
        for command, ack in cases:
            coordinator = valid_coordinator_through("release")
            self.assert_refusal_without_mutation(
                coordinator, coordinator.admit_release_ack, command, ack,
            )
        coordinator = valid_coordinator_through("release")
        command = bundle["release_commands"]["target_v012"]
        ack = bundle["release_acks"]["target_v012"]
        coordinator.admit_release_ack(command, ack)
        self.assert_refusal_without_mutation(
            coordinator, coordinator.admit_release_ack, command, ack,
        )

    def test_deleted_or_cross_role_swapped_ack_cannot_unlock_telemetry(self):
        bundle = fresh_bundle()
        coordinator = valid_coordinator_through("release")
        coordinator.admit_release_ack(
            bundle["release_commands"]["target_v012"],
            bundle["release_acks"]["target_v012"],
        )
        self.assert_refusal_without_mutation(
            coordinator, coordinator.admit_postrun_telemetry,
            bundle["telemetry"],
        )
        swapped = deepcopy(bundle["release_acks"]["hostile_v004r4"])
        swapped["role"] = "target_v012"
        self.assert_refusal_without_mutation(
            coordinator, coordinator.admit_release_ack,
            bundle["release_commands"]["hostile_v004r4"], swapped,
        )

    def test_completion_refusal_matrix_and_both_are_required(self):
        bundle = fresh_bundle()
        premature = valid_coordinator_through("target_ack")
        self.assert_refusal_without_mutation(
            premature, premature.admit_worker_completion,
            bundle["completions"]["target_v012"],
        )
        coordinator = valid_coordinator_through("hostile_ack")
        base = bundle["completions"]["target_v012"]
        for key, value in (
            ("process_id", float(base["process_id"])),
            ("output_path", bundle["policy"].hostile.output),
            ("output_sha256", "not-a-hash"),
            ("completion_epoch", bundle["release"]["release_epoch_by_role"]["target_v012"]),
            ("blocked_on_orchestrator_close", 1),
        ):
            mutant = deepcopy(base)
            mutant[key] = value
            self.assert_refusal_without_mutation(
                coordinator, coordinator.admit_worker_completion, mutant,
            )
        coordinator.admit_worker_completion(base)
        self.assert_refusal_without_mutation(
            coordinator, coordinator.admit_worker_completion, base,
        )
        self.assert_refusal_without_mutation(
            coordinator, coordinator.admit_postrun_telemetry, bundle["telemetry"],
        )

    def test_telemetry_refusal_matrix(self):
        bundle = fresh_bundle()
        premature = valid_coordinator_through("release")
        self.assert_refusal_without_mutation(
            premature, premature.admit_postrun_telemetry, bundle["telemetry"]
        )
        coordinator = valid_coordinator_through("hostile_completion")
        base = bundle["telemetry"]
        mutants = []
        cases = (
            (("dual_launch_handshake_sha256",), "0" * 64),
            (("launch_epoch_by_role", "target_v012"), EPOCH + 10),
            (("completion_epoch_by_role", "target_v012"), EPOCH + 11),
            (("wall_seconds_by_role", "target_v012"), math.nan),
            (("wall_seconds_by_role", "target_v012"), 100),
            (("peak_rss_bytes_by_role", "target_v012"), 17_179_869_185),
            (("rss_peak_semantics",), "OS_HIGH_WATER"),
            (("peak_mapped_bytes_by_role", "target_v012"), 252_944_081),
            (("mapped_peak_semantics",), "OS_VIRTUAL_MEMORY"),
            (("runtime_samples_by_role", "target_v012", 1, "rss_bytes"), 15_999_999_999),
            (("runtime_samples_by_role", "target_v012", 1, "process_id"), 99999),
            (("worker_identity_by_role", "target_v012", "executable_sha256"), "0" * 64),
            (("worker_identity_by_role", "target_v012", "process_id"), 41001.0),
            (("release_ack_sha256_by_role", "target_v012"), "0" * 64),
            (("runtime_samples_by_role", "hostile_v004r4", 1, "captured_epoch"), EPOCH + 73),
            (("exit_code_by_role", "target_v012"), False),
            (("output_path_by_role", "target_v012"), None),
            (("output_sha256_by_role", "target_v012"), "not-a-hash"),
            (("free_disk_bytes_samples", 0, "free_bytes"), 19_201_889_579),
            (("free_disk_bytes_samples", 1, "workspace_filesystem_device"), 18),
            (("free_disk_bytes_samples", 1, "captured_epoch"), EPOCH + 72),
        )
        for path, value in cases:
            mutant = deepcopy(base)
            cursor = mutant
            for key in path[:-1]:
                cursor = cursor[key]
            cursor[path[-1]] = value
            mutants.append(mutant)
        missing_role = deepcopy(base)
        del missing_role["output_sha256_by_role"]["hostile_v004r4"]
        mutants.append(missing_role)
        for mutant in mutants:
            self.assert_refusal_without_mutation(
                coordinator, coordinator.admit_postrun_telemetry, mutant
            )

    def test_strict_json_duplicate_and_nonfinite_refuse(self):
        for text in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}'):
            with self.assertRaises(Refusal):
                parse_strict_json(text)
        self.assertEqual(parse_strict_json('{"a":1}'), {"a": 1})

    def test_module_has_no_process_launch_or_file_write_calls(self):
        directory = Path(__file__).resolve().parent
        for filename in ("dual_launch_coordinator.py", "synthetic_fixtures.py"):
            tree = ast.parse((directory / filename).read_text(encoding="utf-8"))
            imported = {
                alias.name.split(".")[0]
                for node in ast.walk(tree)
                if isinstance(node, (ast.Import, ast.ImportFrom))
                for alias in node.names
            }
            self.assertTrue({"subprocess", "multiprocessing", "socket"}.isdisjoint(imported))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    self.assertNotIn(node.func.attr, {
                        "write", "write_text", "write_bytes", "open", "fork", "spawn", "Popen",
                    })

    def test_policy_rejects_malformed_or_aliased_paths(self):
        bundle = fresh_bundle()
        policy = bundle["policy"]
        with self.assertRaises(Refusal):
            DualLaunchCoordinator({}, EPOCH)
        with self.assertRaises(Refusal):
            DualLaunchCoordinator(
                LaunchPolicy(
                    target={}, hostile=policy.hostile,
                    telemetry_path=policy.telemetry_path,
                ),
                EPOCH,
            )
        with self.assertRaises(Refusal):
            DualLaunchCoordinator(
                LaunchPolicy(
                    target=RolePaths(123, policy.target.workspace, policy.target.output,
                                     policy.target.mapped_peak_limit_bytes),
                    hostile=policy.hostile,
                    telemetry_path=policy.telemetry_path,
                ),
                EPOCH,
            )
        with self.assertRaises(Refusal):
            DualLaunchCoordinator(
                LaunchPolicy(
                    target=policy.target,
                    hostile=RolePaths(
                        policy.hostile.executable, policy.target.workspace,
                        policy.hostile.output, policy.hostile.mapped_peak_limit_bytes,
                    ),
                    telemetry_path=policy.telemetry_path,
                ),
                EPOCH,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
