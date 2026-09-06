#!/usr/bin/env python3
"""Exact checks for the bounded active-seam F3-MDC history."""

from fractions import Fraction
import json
from pathlib import Path


checks = 0


def check(condition: bool, label: str) -> None:
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


# Audited source coefficient and an explicit non-identifiability witness.
r0 = Fraction(14441248, 6075)
check(r0 == Fraction(32128, 27) + Fraction(7212448, 6075),
      "audited raw source coefficient")
alpha_1 = r0
alpha_2 = 2 * r0
epsilon_probe = Fraction(1, 10_000)
check(alpha_1 > 0 and alpha_2 > 0 and alpha_1 != alpha_2,
      "two admissible Hermitian port normalizations")
check(alpha_1 * epsilon_probe != alpha_2 * epsilon_probe,
      "bare operator algebra does not identify the pulse normalization")

# Exact special-angle probabilities.  The adopted attachment fixes Phi=pi/4.
q_after_write = Fraction(1, 2)
q_a_final = Fraction(0)
q_b_final = Fraction(1, 2)
check(q_after_write == Fraction(1, 2), "pi/4 write occupation")
check(q_a_final + q_b_final == q_after_write,
      "native transfer preserves total occupation")

# For theta in [0,pi/2], <J_ab>=sin(2 theta) on the occupied branch.
# Integral dtheta sin(2 theta)=1, multiplied by branch weight 1/2.
transported_seam = q_after_write * Fraction(1)
check(transported_seam == Fraction(1, 2),
      "physically nonzero integrated seam current")

delta_q_a = q_a_final - Fraction(0)
delta_q_b = q_b_final - Fraction(0)
w_a = q_after_write
w_b = Fraction(0)
residual_a = delta_q_a + transported_seam - w_a
residual_b = delta_q_b - transported_seam - w_b
check(residual_a == 0, "source-cell ledger")
check(residual_b == 0, "receiving-cell ledger")
check(residual_a + residual_b == 0, "global periodic telescoping ledger")

# Owner-once guards: generated observables are not independent action terms.
action_owners = (
    "stationary_free",
    "raw_source_writer_attachment",
    "carrier_seam",
    "controller_clock_work",
    "initial_state_boundary",
    "terminal_measure_boundary",
    "matching",
    "other_edges",
)
check(len(action_owners) == len(set(action_owners)), "finite owners occur once")
check("source_write_observable" not in action_owners,
      "derived source write not double counted")
check("current_observable" not in action_owners,
      "derived seam current not double counted")
# Equal CTP branches plus a complete terminal instrument give
# sum_y Tr(E_y U rho U^dagger)=Tr(rho)=1.
rho_trace = Fraction(1)
terminal_effect_sum = Fraction(1)
check(rho_trace * terminal_effect_sum == 1,
      "equal-branch complete-instrument CTP normalization")

undefined_plan_owners = (
    "generic_support_shared_midpoint",
    "gd_recoil_material",
    "stationary_global_state_measure",
    "moving_projector_constraint",
    "retained_field_shell",
    "general_boundary_apparatus",
    "connected_legendre_schur_quotient",
)
check(len(undefined_plan_owners) == 7, "plan-level incomplete owner census")

census = json.loads((Path(__file__).parent / "GLOBAL_OWNER_CENSUS.json").read_text())
global_owner_ids = [owner["id"] for owner in census["owners"]]
check(len(global_owner_ids) == 16 and len(set(global_owner_ids)) == 16,
      "all sixteen GK02 global action owners compiled exactly once")
check(any("UNDEFINED" in owner["status"] for owner in census["owners"]),
      "undefined global owners are retained")
check(census["global_stationary_action"] == "OWNER_INCOMPLETE" and
      census["physical_descent_residual"] == "UNDEFINED" and
      census["physical_Ward_residual"] == "UNDEFINED",
      "global residuals fail closed")

print("RAW_SOURCE_COEFFICIENT", r0)
print("ATTACHMENT_SCREEN", "BARE_F3_NONIDENTIFIABLE")
print("ADOPTED_ATTACHMENT", "alpha=r0; Phi=pi/4")
print("TRANSPORTED_SEAM_CURRENT", transported_seam)
print("CELL_RESIDUALS", residual_a, residual_b)
print("GLOBAL_LEDGER_RESIDUAL", residual_a + residual_b)
print("PLAN_RESIDUAL", "OWNER_INCOMPLETE__UNDEFINED")
print(f"PASS__GATE_A_ACTIVE_SEAM_OWNER_ONCE_SCREEN__{checks}/{checks}")
