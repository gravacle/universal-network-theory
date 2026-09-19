#!/usr/bin/env python3
"""Independent exact Hostile L14 q4-q9 scout kernel."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import geometry


def prepare_phase(branch, phase, request, context):
    if branch != "hostile":
        raise ValueError("Hostile kernel received non-Hostile branch")
    return geometry.prepare_phase(branch, phase, request, context)


def build_task_plan(branch, phase, request, context):
    if branch != "hostile":
        raise ValueError("Hostile kernel received non-Hostile branch")
    return geometry.build_task_plan(branch, phase, request, context)


def run_task(task_payload, context):
    return geometry.run_task("hostile", task_payload, context)


def reduce_results(branch, phase, request, results, context):
    if branch != "hostile":
        raise ValueError("Hostile kernel received non-Hostile branch")
    return geometry.reduce_results(branch, phase, request, results, context)

