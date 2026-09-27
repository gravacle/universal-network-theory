#!/usr/bin/env python3
"""Exact rational construction kill tests, not UNT/cosmology evidence.

All numeric fixtures below are arbitrary small rational test values. None is
an observed abundance, fitted parameter, or proposed physical constant.
"""

from fractions import Fraction as F
import json
from time import perf_counter


def main():
    started = perf_counter()
    checks = 0

    def check(condition, label):
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(label)

    # p = [Q - dot(E)/V]/(3H) follows directly from comoving conservation.
    H, volume, rho = F(2, 7), F(27, 8), F(5, 11)
    pressure = lambda energy_rate, exchange: (
        exchange - energy_rate / volume) / (3 * H)
    check(pressure(F(0), F(0)) == 0, "fixed stored energy is dust if Q=0")
    growth = 3 * H * rho * volume
    check(pressure(growth, F(0)) == -rho, "constant density, no exchange")
    injection = 3 * H * rho
    check(pressure(growth, injection) == 0, "constant density, injected dust")
    check(pressure(growth, F(0)) != pressure(growth, injection),
          "density alone does not determine pressure")
    check(F(0) - injection / (3 * H * rho) == -1,
          "effective dilution w differs from physical dust w")

    # Infinitely many (p,Q) pairs share the same energy/density derivative.
    for shift in (F(-3, 5), F(0), F(4, 9)):
        old_p, old_q = pressure(growth, injection), injection
        new_p, new_q = old_p + shift, old_q + 3 * H * shift
        check(growth / volume + 3 * H * new_p == new_q,
              "density-preserving pressure/exchange degeneracy")

    # Explicit donor budget: injected dust cannot be fed indefinitely.
    donor_initial = F(3, 2)
    affordable_growth = donor_initial / (2 * rho)
    exhausted_growth = donor_initial / rho
    check(donor_initial - rho * affordable_growth > 0, "positive donor stage")
    check(donor_initial - rho * exhausted_growth == 0, "exact exhaustion")
    check(donor_initial - rho * (2 * exhausted_growth) < 0,
          "extrapolation without a donor failure gate is invalid")

    # Fixed density does not identify a coarse-grained count/energy split.
    count, energy_per_item = F(6), F(5, 8)
    for factor in (F(1, 2), F(3), F(7, 4)):
        check((count * factor) * (energy_per_item / factor)
              == count * energy_per_item, "energy/count factorization freedom")

    # Optional four-component maintenance family, in its admitted regime.
    alpha, beta, mu, epsilon = F(2, 5), F(3, 7), F(1, 9), F(4, 3)
    active, maintained, bath_energy = F(5), F(2), F(7, 10)
    flow = alpha * active - beta * maintained
    power = mu * maintained / volume
    transfers = (-epsilon * flow / volume, epsilon * flow / volume,
                 -power, power)
    check(sum(transfers) == 0, "complete transfer budget")
    energy_derivatives = (-epsilon * flow, epsilon * flow,
                          -mu * maintained, mu * maintained - H * bath_energy)
    check(sum(energy_derivatives) == -H * bath_energy,
          "total comoving energy includes radiation expansion work")
    check(energy_derivatives[0] + energy_derivatives[1] == 0,
          "maintenance does not add stored token energy")
    bath_pressure = bath_energy / (3 * volume)
    check(sum(energy_derivatives) + 3 * H * volume * bath_pressure == 0,
          "total covariant background work identity")
    sample_densities = (epsilon * active / volume,
                        epsilon * maintained / volume,
                        donor_initial / volume, bath_energy / volume)
    check(sum(sample_densities) + 3 * bath_pressure > 0,
          "candidate gives deceleration without an inserted negative-pressure sector")

    # A finite-donor jump process needs its acceptance indicator. The
    # deterministic fluid rate above is not its automatic exact mean closure.
    kick = F(1)
    ensemble = ((F(1, 2), F(1), F(0)), (F(1, 2), F(3), F(2)))
    exact_accepted_power = sum(prob * mu * n for prob, n, donor in ensemble
                               if donor >= kick)
    naive_mean_power = sum(prob * mu * n for prob, n, donor in ensemble)
    check(exact_accepted_power != naive_mean_power,
          "finite resource acceptance prevents unjustified moment closure")
    donor, bath = F(2), F(3, 7)
    check(donor >= kick and donor - kick >= 0, "accepted jump is affordable")
    check((donor - kick) + (bath + kick) == donor + bath,
          "every accepted microscopic maintenance jump conserves energy")

    # Stable rate-attractor positions vary with independently free rates.
    ratio_results = []
    for rate_a, rate_b in ((F(1), F(2)), (F(2), F(1)), (F(3), F(5))):
        fixed_fraction = rate_a / (rate_a + rate_b)
        derivative = rate_a * (1 - fixed_fraction) - rate_b * fixed_fraction
        check(derivative == 0, "fixed-fraction equilibrium")
        ratio = fixed_fraction / (1 - fixed_fraction)
        check(ratio == rate_a / rate_b, "ratio equals free rate ratio")
        ratio_results.append(str(ratio))
    check(len(set(ratio_results)) == 3, "free rates change predicted ratio")

    # Exact solution identity uses z=e^[-(alpha+beta)dt]; rational z is a
    # valid finite-time decay factor, not a numerical exponential approximation.
    lam = alpha + beta
    fixed = alpha / lam
    z = F(1, 4)
    initial_fractions = (F(1, 5), F(4, 5))
    final_fractions = []
    for initial in initial_fractions:
        final = fixed + (initial - fixed) * z
        time_derivative = -(initial - fixed) * lam * z
        check(time_derivative == alpha - lam * final,
              "finite-time attractor solution identity")
        final_fractions.append(final)
    check(final_fractions[0] != final_fractions[1],
          "finite-time ratio still depends on initial population")

    # General A0.7 additionally needs an earned energy map. This is NOT an
    # unequal-energy modification of the energy-neutral token dynamics above.
    ratio_one = (F(1) * maintained) / (F(1) * active)
    ratio_two = (F(2) * maintained) / (F(1) * active)
    check(ratio_one != ratio_two, "fixed counts do not fix an unearned energy ratio")

    # Identical comoving dilution with different exchange/pressure is not
    # a proof of identical complete stress, perturbations, or gravity effects.
    elapsed = perf_counter() - started
    print(json.dumps({
        "status": "PASS_CONSTRUCTION_KILL_TEST_IDENTITIES__NOT_UNT_PHYSICS_EVIDENCE",
        "exact_rational_checks": checks,
        "elapsed_seconds": elapsed,
        "arbitrary_fixture_rate_ratios": ratio_results,
        "candidate_result": "finite-resource dust maintenance cannot supply negative pressure",
        "identifiability_result": "density does not identify pressure/exchange; free rates and initial data change ratios",
        "scope": "background bookkeeping and explicit toy only; no cosmological fit or perturbation validation",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
