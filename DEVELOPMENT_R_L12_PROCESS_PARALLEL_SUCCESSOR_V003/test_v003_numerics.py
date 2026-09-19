#!/usr/bin/env python3
"""Bounded non-L12 controls for the V003 capacity-only successor."""

from __future__ import annotations

import math

import numpy as np

from repair_kernels import (
    HOSTILE_ROUGH,
    HOSTILE_SHARP,
    TARGET_COARSE,
    TARGET_FINE,
    TARGET_MAX_SUBDIVISIONS,
    hostile,
    hostile_capacity_scope,
    hostile_repair_plan,
    target,
    target_capacity_scope,
    target_repair_plan,
)


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    print(f"PASS {label}")


def main() -> None:
    check(TARGET_COARSE.tolerance == 2.0e-9, "target rough tolerance unchanged")
    check(TARGET_FINE.tolerance == 5.0e-11, "target sharp tolerance unchanged")
    check(TARGET_COARSE.quadrature_nodes == 16, "target rough quadrature unchanged")
    check(TARGET_FINE.quadrature_nodes == 24, "target sharp quadrature unchanged")
    check(TARGET_MAX_SUBDIVISIONS == 256, "target subdivision capacity increased")
    check(HOSTILE_ROUGH.tolerance == 3.0e-9, "hostile rough tolerance unchanged")
    check(HOSTILE_SHARP.tolerance == 8.0e-11, "hostile sharp tolerance unchanged")
    check(HOSTILE_ROUGH.gauss_order == 18, "hostile rough quadrature unchanged")
    check(HOSTILE_SHARP.gauss_order == 28, "hostile sharp quadrature unchanged")

    old_target = (
        target.v004.sealed.COARSE,
        target.v004.sealed.FINE,
        target.v004.v3.MAX_SUBDIVISIONS,
    )
    with target_capacity_scope():
        check(target.v004.sealed.COARSE is TARGET_COARSE, "target rough installed")
        check(target.v004.sealed.FINE is TARGET_FINE, "target sharp installed")
        check(
            target.v004.v3.MAX_SUBDIVISIONS == TARGET_MAX_SUBDIVISIONS,
            "target subdivision ceiling installed",
        )
    check(
        (
            target.v004.sealed.COARSE,
            target.v004.sealed.FINE,
            target.v004.v3.MAX_SUBDIVISIONS,
        )
        == old_target,
        "target capacity scope restores predecessor",
    )

    old_hostile = (hostile.physical.ROUGH, hostile.physical.SHARP)
    with hostile_capacity_scope():
        check(hostile.physical.ROUGH is HOSTILE_ROUGH, "hostile rough installed")
        check(hostile.physical.SHARP is HOSTILE_SHARP, "hostile sharp installed")
    check(
        (hostile.physical.ROUGH, hostile.physical.SHARP) == old_hostile,
        "hostile capacity scope restores predecessor",
    )

    # A small exact carrier checks that the enlarged recurrence computes the
    # same physical endpoint as its predecessor to well inside either bound.
    length = 4
    edges = hostile.physical.hostile_edges(length)
    carrier = hostile.physical.CarrierBlock(length, 2, edges)
    vector = np.zeros((1, len(carrier.words)), dtype=np.complex128)
    vector[0, 0] = 1.0
    old_final, _old_flux, old_record = hostile.legacy.replay.low_memory_evolve_batch(
        carrier, vector, old_hostile[1]
    )
    new_final, _new_flux, new_record = hostile.legacy.replay.low_memory_evolve_batch(
        carrier, vector, HOSTILE_SHARP
    )
    check(bool(old_record["converged"]), "L4 predecessor hostile recurrence converges")
    check(bool(new_record["converged"]), "L4 V003 hostile recurrence converges")
    check(
        float(np.linalg.norm(old_final - new_final)) <= 1.0e-12,
        "L4 hostile endpoint invariant under degree extension",
    )
    del carrier

    target_plan = target_repair_plan(length)
    hostile_plan = hostile_repair_plan(length)
    for label, plan in (("target", target_plan), ("hostile", hostile_plan)):
        check(plan["total_tasks"] > 0, f"{label} denominator positive")
        check(plan["row_windows"] > 0, f"{label} row-window denominator positive")
        check(plan["total_work_units"] > 0, f"{label} work denominator positive")
        check(
            plan["total_tasks"] >= plan["row_windows"],
            f"{label} task census internally ordered",
        )

    check(math.isclose(target.v004.sealed.PHI, math.pi / 4.0), "target admission angle unchanged")
    check(math.isclose(target.v004.sealed.DWELL, math.pi / 2.0), "target route time unchanged")
    check(math.isclose(hostile.physical.ANGLE, math.pi / 4.0), "hostile admission angle unchanged")
    check(math.isclose(hostile.physical.ROUTE_TIME, math.pi / 2.0), "hostile route time unchanged")
    print("PASS V003_BOUNDED_NUMERICAL_CAPACITY_CONTROLS")


if __name__ == "__main__":
    main()
