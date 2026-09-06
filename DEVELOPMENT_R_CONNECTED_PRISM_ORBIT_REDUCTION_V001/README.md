# Connected prism-orbit reduction V001

This packet validates a larger order-`2L` source-preserving finite group for
the supplied connected two-cycle supports. “Prism” names a finite graph
relabeling that makes the automorphisms easy to enumerate. It does not assign
the records to a physical grid or geometry.

Run:

```sh
PYTHONWARNINGS=error python3 -B validate_prism_reduction.py
```

The validator constructs the group, complete word orbits, normalized quotient
Hamiltonian, and signed oriented-edge orbits at L4/L6/L8/L10. It evolves each
reduced state with order-10 Taylor steps and 2,048-panel Simpson integration,
then compares every occupation and signed current with the sealed full-state
or previously audited finite-orbit packets. It must finish with
`PASS__R_CONNECTED_PRISM_ORBIT_REDUCTION__40/40` and preserve canonical
`RESULT.json` within `8e-10`.

Only the finite group/orbit/quotient identities are exact. Evolution and
quadrature remain numerical. The group is not claimed to be the maximal graph
automorphism group. Support, source calibration, kappa, routing, content,
clock, and read remain conditional. No grid, continuum, Ward, critical phase,
graviton, or gravity claim is made.
