#!/usr/bin/env python3
"""Exhaustive and mutation checks for authorization_model.py.

The state space is finite: every PASS/PENDING assignment is enumerated.  The
checker also injects negative/invalid predecessor verdicts and malformed API
inputs.  It emits one deterministic JSON record to stdout.
"""

from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path
from typing import Iterable

from authorization_model import (
    PREDECESSORS,
    STAGES,
    Decision,
    Stage,
    State,
    Status,
    advance,
    canonical_route,
    validate_state,
)


ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "authorization_model.py"
CHECKER = Path(__file__).resolve()

# Independent test oracle copied from the route named in this packet's scope.
# It is intentionally not derived from authorization_model.PREDECESSORS: an
# omitted production edge must not silently disappear from the audit oracle.
EXPECTED_PREDECESSOR_NAMES: dict[str, frozenset[str]] = {
    "PREPAYLOAD_AUDIT": frozenset(),
    "CACHE_SET_BUILT": frozenset({"PREPAYLOAD_AUDIT"}),
    "POSTBUILD_AUDIT": frozenset({"CACHE_SET_BUILT"}),
    "BASE_GATE_AUDIT": frozenset({"POSTBUILD_AUDIT"}),
    "CONTROL_L4": frozenset({"BASE_GATE_AUDIT"}),
    "CONTROL_L6": frozenset({"BASE_GATE_AUDIT"}),
    "CONTROL_L8": frozenset({"BASE_GATE_AUDIT"}),
    "CONTROL_STAGE_AUDIT": frozenset(
        {"CONTROL_L4", "CONTROL_L6", "CONTROL_L8"}
    ),
    "L10_AUTHORIZATION": frozenset({"CONTROL_STAGE_AUDIT"}),
    "L10_TARGET_RESULT": frozenset({"L10_AUTHORIZATION"}),
    "L10_HOSTILE_RESULT": frozenset({"L10_AUTHORIZATION"}),
    "L10_CROSS_AUDIT": frozenset(
        {"L10_TARGET_RESULT", "L10_HOSTILE_RESULT"}
    ),
    "L12_SHARED_SCHEDULE": frozenset({"L10_CROSS_AUDIT"}),
    "L12_HOSTILE_ELIGIBILITY": frozenset({"L10_CROSS_AUDIT"}),
    "DUAL_L12_LAUNCH_HANDSHAKE": frozenset(
        {"L12_SHARED_SCHEDULE", "L12_HOSTILE_ELIGIBILITY"}
    ),
    "TARGET_L12_TELEMETRY": frozenset({"DUAL_L12_LAUNCH_HANDSHAKE"}),
    "HOSTILE_L12_TELEMETRY": frozenset({"DUAL_L12_LAUNCH_HANDSHAKE"}),
    "FINAL_ADJUDICATION": frozenset(
        {"TARGET_L12_TELEMETRY", "HOSTILE_L12_TELEMETRY"}
    ),
}


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def state_from_mask(mask: int) -> State:
    return State(
        tuple(
            Status.PASS if mask & (1 << int(stage)) else Status.PENDING
            for stage in STAGES
        )
    )


def mask_from_state(state: State) -> int:
    mask = 0
    for stage in STAGES:
        if state.status(stage) is Status.PASS:
            mask |= 1 << int(stage)
    return mask


def expected_predecessors(stage: Stage) -> frozenset[Stage]:
    return frozenset(Stage[name] for name in EXPECTED_PREDECESSOR_NAMES[stage.name])


def oracle_is_closed(mask: int) -> bool:
    """Independent bitset oracle for predecessor-closed PASS assignments."""
    for stage in STAGES:
        predecessors = expected_predecessors(stage)
        if mask & (1 << int(stage)):
            predecessor_mask = sum(1 << int(item) for item in predecessors)
            if mask & predecessor_mask != predecessor_mask:
                return False
    return True


def transitive_predecessors(stage: Stage) -> frozenset[Stage]:
    found: set[Stage] = set()
    todo = list(expected_predecessors(stage))
    while todo:
        item = todo.pop()
        if item not in found:
            found.add(item)
            todo.extend(expected_predecessors(item))
    return frozenset(found)


def check_graph() -> dict[str, int]:
    check(tuple(int(stage) for stage in STAGES) == tuple(range(len(STAGES))),
          "stage indices are not dense")
    check(set(PREDECESSORS) == set(STAGES), "predecessor key coverage mismatch")
    check(set(EXPECTED_PREDECESSOR_NAMES) == {stage.name for stage in STAGES},
          "independent oracle stage coverage mismatch")
    direct_edges = 0
    transitive_edges = 0
    for stage in STAGES:
        check(PREDECESSORS[stage] == expected_predecessors(stage),
              f"model/oracle predecessor mismatch at {stage.name}")
        direct_edges += len(expected_predecessors(stage))
        check(stage not in transitive_predecessors(stage), f"cycle at {stage.name}")
        transitive_edges += len(transitive_predecessors(stage))
    return {
        "stages": len(STAGES),
        "direct_edges": direct_edges,
        "transitive_edges": transitive_edges,
    }


def check_entire_boolean_state_space() -> tuple[dict[str, int], set[int]]:
    all_masks = 1 << len(STAGES)
    legal_masks: set[int] = set()
    invalid_masks = 0
    invalid_state_action_refusals = 0
    validator_agreements = 0
    for mask in range(all_masks):
        state = state_from_mask(mask)
        actual, _ = validate_state(state)
        expected = oracle_is_closed(mask)
        check(actual == expected, f"validator/oracle disagreement for mask {mask}")
        validator_agreements += 1
        if actual:
            legal_masks.add(mask)
        else:
            invalid_masks += 1
            # Invalid prior state is rejected before every requested stage.
            for probe in STAGES:
                decision = advance(state, probe)
                check(not decision.allowed and decision.next_state is None,
                      f"invalid mask {mask} permitted {probe.name}")
                check(decision.code == "predecessor_inconsistent_state",
                      f"unexpected invalid-state code for mask {mask}")
                invalid_state_action_refusals += 1
    return (
        {
            "boolean_states": all_masks,
            "validator_oracle_agreements": validator_agreements,
            "legal_states": len(legal_masks),
            "invalid_states": invalid_masks,
            "invalid_state_action_refusals": invalid_state_action_refusals,
        },
        legal_masks,
    )


def check_all_actions_from_legal_states(
    legal_masks: set[int],
) -> dict[str, int]:
    attempts = 0
    allowed = 0
    missing_refusals = 0
    duplicate_refusals = 0
    reached_masks = {0}
    queue: deque[int] = deque([0])

    for mask in sorted(legal_masks):
        state = state_from_mask(mask)
        for stage in STAGES:
            attempts += 1
            decision = advance(state, stage)
            predecessor_mask = sum(
                1 << int(item) for item in expected_predecessors(stage)
            )
            stage_bit = 1 << int(stage)
            expected_allowed = not (mask & stage_bit) and (
                mask & predecessor_mask == predecessor_mask
            )
            check(decision.allowed == expected_allowed,
                  f"transition mismatch: mask={mask} stage={stage.name}")
            if expected_allowed:
                allowed += 1
                check(decision.code == "allowed" and decision.next_state is not None,
                      f"allowed transition has bad result: {stage.name}")
                expected_mask = mask | stage_bit
                check(mask_from_state(decision.next_state) == expected_mask,
                      f"non-monotone transition: {stage.name}")
                check(expected_mask in legal_masks,
                      f"transition escaped legal states: {stage.name}")
            elif mask & stage_bit:
                duplicate_refusals += 1
                check(decision.code == "duplicate_transition",
                      f"duplicate not identified: {stage.name}")
            else:
                missing_refusals += 1
                check(decision.code == "missing_predecessor",
                      f"out-of-order not identified: {stage.name}")

    # Independent breadth-first reachability from the empty state.
    while queue:
        mask = queue.popleft()
        state = state_from_mask(mask)
        for stage in STAGES:
            decision = advance(state, stage)
            if decision.allowed:
                check(decision.next_state is not None, "allowed result lacks state")
                next_mask = mask_from_state(decision.next_state)
                if next_mask not in reached_masks:
                    reached_masks.add(next_mask)
                    queue.append(next_mask)
    check(reached_masks == legal_masks, "legal state exists but is unreachable")
    return {
        "legal_state_action_attempts": attempts,
        "allowed_transitions": allowed,
        "missing_predecessor_refusals": missing_refusals,
        "duplicate_transition_refusals": duplicate_refusals,
        "bfs_reachable_states": len(reached_masks),
    }


def replace_status(state: State, stage: Stage, value: object) -> State:
    statuses = list(state.statuses)
    statuses[int(stage)] = value  # type: ignore[assignment]
    return State(tuple(statuses))


def check_negative_predecessors() -> dict[str, int]:
    missing = 0
    negative = 0
    invalid = 0
    global_negative_state_action_refusals = 0
    for stage in STAGES:
        closure = transitive_predecessors(stage)
        closure_mask = sum(1 << int(item) for item in closure)
        ready = state_from_mask(closure_mask)
        allowed = advance(ready, stage)
        check(allowed.allowed, f"canonical ready state refused {stage.name}")

        for predecessor in expected_predecessors(stage):
            absent = replace_status(ready, predecessor, Status.PENDING)
            decision = advance(absent, stage)
            check(not decision.allowed and decision.next_state is None,
                  f"missing predecessor accepted: {stage.name}/{predecessor.name}")
            missing += 1

            for value in (Status.FAIL, Status.INVALID):
                mutant = replace_status(ready, predecessor, value)
                decision = advance(mutant, stage)
                check(not decision.allowed and decision.next_state is None,
                      f"negative predecessor accepted: {stage.name}/{predecessor.name}")
                check(decision.code == "negative_or_invalid_evidence",
                      f"negative predecessor has wrong code: {stage.name}")
                if value is Status.FAIL:
                    negative += 1
                else:
                    invalid += 1

    # The model is globally fail closed: even a negative cell unrelated to the
    # requested action invalidates the prior state before dispatch.
    for poisoned_stage in STAGES:
        for value in (Status.FAIL, Status.INVALID):
            mutant = replace_status(State.initial(), poisoned_stage, value)
            for requested_stage in STAGES:
                decision = advance(mutant, requested_stage)
                check(not decision.allowed and decision.next_state is None,
                      "negative state permitted an unrelated action")
                check(decision.code == "negative_or_invalid_evidence",
                      "negative state did not fail closed before dispatch")
                global_negative_state_action_refusals += 1
    return {
        "direct_missing_predecessor_mutations": missing,
        "direct_failed_predecessor_mutations": negative,
        "direct_invalid_predecessor_mutations": invalid,
        "global_negative_state_action_refusals": (
            global_negative_state_action_refusals
        ),
    }


def check_malformed_inputs() -> dict[str, int]:
    cases: list[tuple[object, object, str]] = [
        (None, Stage.PREPAYLOAD_AUDIT, "state_wrong_type"),
        ({}, Stage.PREPAYLOAD_AUDIT, "state_wrong_type"),
        (State([]), Stage.PREPAYLOAD_AUDIT, "statuses_wrong_type"),  # type: ignore[arg-type]
        (State(tuple()), Stage.PREPAYLOAD_AUDIT, "statuses_wrong_length"),
        (replace_status(State.initial(), Stage.PREPAYLOAD_AUDIT, None),
         Stage.PREPAYLOAD_AUDIT, "status_wrong_type"),
        (replace_status(State.initial(), Stage.PREPAYLOAD_AUDIT, False),
         Stage.PREPAYLOAD_AUDIT, "status_wrong_type"),
        (replace_status(State.initial(), Stage.PREPAYLOAD_AUDIT, 1),
         Stage.PREPAYLOAD_AUDIT, "status_wrong_type"),
        (replace_status(State.initial(), Stage.PREPAYLOAD_AUDIT, "PASS"),
         Stage.PREPAYLOAD_AUDIT, "status_wrong_type"),
        (State.initial(), 0, "stage_wrong_type"),
        (State.initial(), True, "stage_wrong_type"),
        (State.initial(), "PREPAYLOAD_AUDIT", "stage_wrong_type"),
        (State.initial(), None, "stage_wrong_type"),
    ]
    for state, stage, expected_code in cases:
        decision = advance(state, stage)
        check(not decision.allowed and decision.next_state is None,
              f"malformed input permitted: {expected_code}")
        check(decision.code == expected_code,
              f"malformed input code {decision.code}, expected {expected_code}")
    return {"malformed_input_refusals": len(cases)}


def follow_route(
    route: Iterable[Stage], *, require_complete: bool = True
) -> tuple[State, dict[str, int]]:
    state = State.initial()
    reached = {stage.name: 0 for stage in STAGES}
    for position, stage in enumerate(route, start=1):
        decision: Decision = advance(state, stage)
        check(decision.allowed and decision.next_state is not None,
              f"witness route refused at {stage.name}")
        state = decision.next_state
        reached[stage.name] = position
    if require_complete:
        check(all(value is Status.PASS for value in state.statuses),
              "witness route did not reach final complete state")
    return state, reached


def check_required_reachability() -> dict[str, object]:
    _, positions = follow_route(canonical_route())
    initial = State.initial()
    prefix = (
        Stage.PREPAYLOAD_AUDIT,
        Stage.CACHE_SET_BUILT,
        Stage.POSTBUILD_AUDIT,
        Stage.BASE_GATE_AUDIT,
    )
    base_state, _ = follow_route(prefix, require_complete=False)
    independently_enabled = [
        stage.name
        for stage in (Stage.CONTROL_L4, Stage.CONTROL_L6, Stage.CONTROL_L8)
        if advance(base_state, stage).allowed
    ]
    check(len(independently_enabled) == 3,
          "L4/L6/L8 are not independently reachable after the base gate")
    check(advance(initial, Stage.CONTROL_L4).code == "missing_predecessor",
          "L4 unexpectedly reachable from initial state")
    return {
        "l4_l6_l8_independently_enabled_after_base_gate": independently_enabled,
        "l10_authorization_witness_position": positions[Stage.L10_AUTHORIZATION.name],
        "l12_handshake_witness_position": positions[
            Stage.DUAL_L12_LAUNCH_HANDSHAKE.name
        ],
        "final_adjudication_witness_position": positions[
            Stage.FINAL_ADJUDICATION.name
        ],
    }


def main() -> None:
    graph = check_graph()
    state_space, legal_masks = check_entire_boolean_state_space()
    transitions = check_all_actions_from_legal_states(legal_masks)
    predecessor_mutations = check_negative_predecessors()
    malformed = check_malformed_inputs()
    reachability = check_required_reachability()
    result = {
        "schema": "l12_authorization_state_model_check_v1",
        "result": "PASS",
        "scope": "abstract authorization ordering only; no physical compute or authority files",
        "model_sha256": hashlib.sha256(MODEL.read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
        "graph": graph,
        "state_space": state_space,
        "transitions": transitions,
        "predecessor_mutations": predecessor_mutations,
        "malformed_inputs": malformed,
        "reachability": reachability,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
