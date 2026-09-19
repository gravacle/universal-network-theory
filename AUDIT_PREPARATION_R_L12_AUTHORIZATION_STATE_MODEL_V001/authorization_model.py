#!/usr/bin/env python3
"""Pure, bounded authorization-state model for the proposed V012 route.

This module deliberately has no filesystem, subprocess, numerical-compute, or
target-code dependencies.  A state is an 18-cell tuple whose cells are strict
Status enum members.  The only successful transition changes one PENDING cell
to PASS after validating the entire prior state and all direct predecessors.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Final


class Status(Enum):
    PENDING = "PENDING"
    PASS = "PASS"
    FAIL = "FAIL"
    INVALID = "INVALID"


class Stage(IntEnum):
    PREPAYLOAD_AUDIT = 0
    CACHE_SET_BUILT = 1
    POSTBUILD_AUDIT = 2
    BASE_GATE_AUDIT = 3
    CONTROL_L4 = 4
    CONTROL_L6 = 5
    CONTROL_L8 = 6
    CONTROL_STAGE_AUDIT = 7
    L10_AUTHORIZATION = 8
    L10_TARGET_RESULT = 9
    L10_HOSTILE_RESULT = 10
    L10_CROSS_AUDIT = 11
    L12_SHARED_SCHEDULE = 12
    L12_HOSTILE_ELIGIBILITY = 13
    DUAL_L12_LAUNCH_HANDSHAKE = 14
    TARGET_L12_TELEMETRY = 15
    HOSTILE_L12_TELEMETRY = 16
    FINAL_ADJUDICATION = 17


STAGES: Final[tuple[Stage, ...]] = tuple(Stage)

# These are direct proof obligations, not merely a suggested execution order.
PREDECESSORS: Final[dict[Stage, frozenset[Stage]]] = {
    Stage.PREPAYLOAD_AUDIT: frozenset(),
    Stage.CACHE_SET_BUILT: frozenset({Stage.PREPAYLOAD_AUDIT}),
    Stage.POSTBUILD_AUDIT: frozenset({Stage.CACHE_SET_BUILT}),
    Stage.BASE_GATE_AUDIT: frozenset({Stage.POSTBUILD_AUDIT}),
    Stage.CONTROL_L4: frozenset({Stage.BASE_GATE_AUDIT}),
    Stage.CONTROL_L6: frozenset({Stage.BASE_GATE_AUDIT}),
    Stage.CONTROL_L8: frozenset({Stage.BASE_GATE_AUDIT}),
    Stage.CONTROL_STAGE_AUDIT: frozenset(
        {Stage.CONTROL_L4, Stage.CONTROL_L6, Stage.CONTROL_L8}
    ),
    Stage.L10_AUTHORIZATION: frozenset({Stage.CONTROL_STAGE_AUDIT}),
    Stage.L10_TARGET_RESULT: frozenset({Stage.L10_AUTHORIZATION}),
    Stage.L10_HOSTILE_RESULT: frozenset({Stage.L10_AUTHORIZATION}),
    Stage.L10_CROSS_AUDIT: frozenset(
        {Stage.L10_TARGET_RESULT, Stage.L10_HOSTILE_RESULT}
    ),
    Stage.L12_SHARED_SCHEDULE: frozenset({Stage.L10_CROSS_AUDIT}),
    Stage.L12_HOSTILE_ELIGIBILITY: frozenset({Stage.L10_CROSS_AUDIT}),
    Stage.DUAL_L12_LAUNCH_HANDSHAKE: frozenset(
        {Stage.L12_SHARED_SCHEDULE, Stage.L12_HOSTILE_ELIGIBILITY}
    ),
    Stage.TARGET_L12_TELEMETRY: frozenset(
        {Stage.DUAL_L12_LAUNCH_HANDSHAKE}
    ),
    Stage.HOSTILE_L12_TELEMETRY: frozenset(
        {Stage.DUAL_L12_LAUNCH_HANDSHAKE}
    ),
    Stage.FINAL_ADJUDICATION: frozenset(
        {Stage.TARGET_L12_TELEMETRY, Stage.HOSTILE_L12_TELEMETRY}
    ),
}


@dataclass(frozen=True)
class State:
    statuses: tuple[Status, ...]

    @classmethod
    def initial(cls) -> "State":
        return cls(tuple(Status.PENDING for _ in STAGES))

    def status(self, stage: Stage) -> Status:
        return self.statuses[int(stage)]


@dataclass(frozen=True)
class Decision:
    allowed: bool
    code: str
    next_state: State | None


def validate_state(state: object) -> tuple[bool, str]:
    """Fail closed on malformed, negative, or predecessor-inconsistent state."""
    if type(state) is not State:
        return False, "state_wrong_type"
    if type(state.statuses) is not tuple:
        return False, "statuses_wrong_type"
    if len(state.statuses) != len(STAGES):
        return False, "statuses_wrong_length"
    for value in state.statuses:
        if type(value) is not Status:
            return False, "status_wrong_type"
        if value in (Status.FAIL, Status.INVALID):
            return False, "negative_or_invalid_evidence"
    for stage in STAGES:
        if state.status(stage) is Status.PASS:
            for predecessor in PREDECESSORS[stage]:
                if state.status(predecessor) is not Status.PASS:
                    return False, "predecessor_inconsistent_state"
    return True, "valid"


def advance(state: object, stage: object) -> Decision:
    """Attempt one monotone authorization transition; refuse on any ambiguity."""
    valid, code = validate_state(state)
    if not valid:
        return Decision(False, code, None)
    if type(stage) is not Stage:
        return Decision(False, "stage_wrong_type", None)

    assert type(state) is State  # narrowed by validate_state
    if state.status(stage) is not Status.PENDING:
        return Decision(False, "duplicate_transition", None)

    missing = tuple(
        predecessor
        for predecessor in PREDECESSORS[stage]
        if state.status(predecessor) is not Status.PASS
    )
    if missing:
        return Decision(False, "missing_predecessor", None)

    statuses = list(state.statuses)
    statuses[int(stage)] = Status.PASS
    next_state = State(tuple(statuses))
    valid_next, next_code = validate_state(next_state)
    if not valid_next:
        return Decision(False, f"internal_{next_code}", None)
    return Decision(True, "allowed", next_state)


def canonical_route() -> tuple[Stage, ...]:
    """One witness route; sibling controls/results/telemetry may commute."""
    return (
        Stage.PREPAYLOAD_AUDIT,
        Stage.CACHE_SET_BUILT,
        Stage.POSTBUILD_AUDIT,
        Stage.BASE_GATE_AUDIT,
        Stage.CONTROL_L4,
        Stage.CONTROL_L6,
        Stage.CONTROL_L8,
        Stage.CONTROL_STAGE_AUDIT,
        Stage.L10_AUTHORIZATION,
        Stage.L10_TARGET_RESULT,
        Stage.L10_HOSTILE_RESULT,
        Stage.L10_CROSS_AUDIT,
        Stage.L12_SHARED_SCHEDULE,
        Stage.L12_HOSTILE_ELIGIBILITY,
        Stage.DUAL_L12_LAUNCH_HANDSHAKE,
        Stage.TARGET_L12_TELEMETRY,
        Stage.HOSTILE_L12_TELEMETRY,
        Stage.FINAL_ADJUDICATION,
    )
