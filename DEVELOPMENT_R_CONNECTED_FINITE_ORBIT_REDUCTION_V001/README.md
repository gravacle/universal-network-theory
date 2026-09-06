# Connected finite-orbit reduction V001

This packet validates an exact finite automorphism-orbit basis for the
conditional connected two-cycle supports. It is computational compression of
the already declared finite records, not a physical grid, continuum limit, or
new dynamics.

Run:

```sh
PYTHONWARNINGS=error python3 -B validate_orbit_reduction.py
```

The validator constructs the finite group, orbit partition, reduced
Hamiltonian, source state, representative current kernels, and symmetry
reconstruction independently at L4, L6, and L8. It evolves each reduced state
with the same order-10/2,048-step numerical rule and compares every occupation
and signed current with the sealed full-state packets. It must finish with
`PASS__R_CONNECTED_FINITE_ORBIT_REDUCTION__27/27` and preserve canonical
`RESULT.json` within `5e-10`.

`numba` is used only to execute the explicitly constructed finite sparse sums.
The reduction identities are finite combinatorics. Support, kappa, source
calibration, routing, content, clock, and read remain conditional. No scaling,
phase, continuum, Ward, graviton, or gravity claim is made.
