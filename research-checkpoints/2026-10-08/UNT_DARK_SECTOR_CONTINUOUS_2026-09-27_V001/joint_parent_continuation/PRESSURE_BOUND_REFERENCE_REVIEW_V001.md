# Pressure reference V001: independent result review

2026-09-29. Accepted. All 16 frozen inputs, the outer result/freeze link and
canonical payload hash authenticate. All **18 reference rows, 54 capacities,
14 synthetic controls and 256 distinct passing numerical checks** are retained.
No fit, trajectory, parameter adjustment or additional physical worker was run
by this reviewer.

| Artifact | SHA-256 |
|---|---|
| Numerical source | `dfc71a4c322968dee059dacc4a39618517eafb8ea6366afefdeaf94597c4a054` |
| Protocol | `03a71221388687d0f4c5d3f96d4b6ec63d6fa0ad30ea2856f80be0a22596199e` |
| Freeze | `32b71c0ea59f33961ea5c9e22f37ce8eddf6565588f790c43587842eaf19f486` |
| Result | `7a8eabdb5f1925799ccb44f8c790e48df008e26a35929afb1bf872c299acd99c` |
| Canonical payload | `e1cc91e3d3e585bfde83c860b54f4febdc3ae99a8697341e203216dae5bec358` |
| Independent audit source | `a7f0660a8862380e72833329f49b7b8f8f90bf51ff1a70e20661d802ade56633` |

`pressure_bound_saved_audit_v001.py` independently recombines every saved row
using 48-digit Decimal arithmetic, a different quadratic-root expression,
`Omega_b=omega_b/(H0/100)²`, and a high-precision pi. It also checks every
capacity and synthetic fixture. **333 independent arithmetic checks pass**;
the largest relative difference is `1.7764e-15` (a synthetic inverse), and
the largest physical pressure-floor difference is `6.9249e-16`. The exact
declared saturated fixture is reconstructed from its gap powers; rounded
binary fixture values are not incorrectly assumed to be exact decimals.
Full small audit data are saved separately. Numerical source/protocol and
earlier evidence were not edited.

The inherited-reference result is strong but specific:

- Across all eighteen reference cases, the dimensionless excitation energy
  required by the old background budget is approximately **3.5360–9.6724**.
- The corresponding distribution-independent bound is
  **`p_exc/rho_exc >= 0.2595904103–0.2864928043`**, with each bound attached to
  its own row, not a single universal fitted value.
- At the central theoretical-BBN reference, `E=5.6415794625`,
  `P_floor=1.5425035287`, and `w_floor=0.2734169640`.

This applies to **all rapidly averaged bounded zero-source states of the
specified positive quadratic-plus-quartic spectrum at the inherited relaxed
calibration**, not merely the saved action template. The proof uses the actual
energy and spectral fourth moment, so neither redistributing mode actions nor
changing the inertia can make that required energy arbitrarily cold while
holding the other premises fixed. It rules out treating an arbitrarily large
excitation abundance as pressureless within that reference completion.

The old source's assumptions are retained verbatim here: “Late-time flat
zero-excitation baryon+dust/vacuum diagnostic; radiation omitted here only.”
The new excitation target is its missing reference budget, not an independent
measurement of missing matter. Its vacuum was already cosmologically
calibrated, the a0-to-gstar conversion is the inherited RELAXED calibration,
and the baryon benchmarks import standard BBN. Measurement/nuclear-error
metadata remain in every row but **were not propagated** into a confidence
region or likelihood. Illustrative wmax=.001,.01,.1 capacities are definitions,
not observational coldness limits.

A newly calibrated excited-state model may change the shared gstar and must
recompute both its galaxy response and expansion/stress; the old calibrated
curve cannot simultaneously be retained without that calculation. A different
spectral shape changes the moment and force/volume relation together. Coherent
nonadiabatic states do not obey this rapid-virial bound and need their actual
evolving stress. Therefore this result is not a statistical rejection of UNT,
all shared-state models, or every network explanation.

Reported worker cost: **0.01150437499745749 seconds**, **22,790,144 bytes peak
self RSS** (about 21.73 MiB); not an aggregate-memory measurement. No numerical
or interpretation defect was found within the declared scope.
