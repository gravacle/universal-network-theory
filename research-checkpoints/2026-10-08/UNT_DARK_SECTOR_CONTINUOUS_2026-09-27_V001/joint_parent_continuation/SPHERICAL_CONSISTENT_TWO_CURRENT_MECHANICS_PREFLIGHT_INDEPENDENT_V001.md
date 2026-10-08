# Independent consistent-inertia mechanics preflight

Source-only verdict: **PASS for the declared bounded exploratory experiment**, not a numerical result or physical qualification. Reviewer: `critical_path_native`, independent of producer author `urm_dark_integration`. No producer imports, numerical jobs, compilation or execution were performed in this review.

## Reviewed identities

- `spherical_consistent_two_current_v001.py`: `a4f0546b1a3082e1eab46adfb9f942353459079830c58188c59a42ad77ff22b0`
- `spherical_consistent_two_current_supervisor_v001.py`: `a7fa3205e9019f52e680c0d7707e4417f4d11077a2a26eca104290d16b1587e6`
- `SPHERICAL_CONSISTENT_TWO_CURRENT_PROTOCOL_V001.md`: `5de363c2545a6bab800ea5a931de334fe0733ed6da184d932fb7cb1562f11bd3`

The complete three files, state-map helper and exact inertia kernel were read. The inherited `Model.rhs`, initial-state method and controls were checked directly, together with the publication helper and resource invocation implementation. The old initializer, readout, integrators and main are not inherited as execution paths.

## Mechanical checks

For `K=p^T M(x)^-1 p/(2 A^2)`, fixed-p differentiation gives `partial_j K=-g_j`, while `xdot=v/A` and `pdot=g+f`. Therefore `Kdot=xdot·f-2HK`; the geometric term is not an additional work supply. The implemented independent directional matrix derivative and kernel geometric force have matching signs and origin treatment. The force inputs remain `-gradW0/A` and the original pressure face kick, with outer traction counted once. The peculiar-acceleration decomposition correctly includes `M^-1(f+g)/A-M^-1(Mdot v)-Hv`, and is explicitly not physical-radius acceleration.

The reused force/work method accesses the new consistent velocities and kinetic energies through `self.read`; it contains neither old face-mass access nor an existing geometric kick. Thus the added `g` does not double-count inertia or expansion work. The ten pressure-on work ledgers remain consistent with the kinetic chain above.

The actual-mesh nonzero-velocity controls keep fixed p in the kinetic directional difference, compare both prescribed finite-difference steps and Richardson combination, and independently contract `Mdot` against v. Per-species normalization avoids hiding the hard current solely through its small total mass; the protocol correctly does not claim relative accuracy for every tiny matrix entry.

## Integration, controls and custody

DOPRI uses each complete high/low endpoint's own A and mesh in the nonlinear physical chart. Stage and both endpoint guards precede acceptance; no invalid endpoint is silently retried as an accuracy failure. The old initial geometry, masses, physical source and zero momenta are retained. Pressure-off retains the same M and g, removes only the pressure kick, and is descriptive rather than energy-qualified. Time refinement remains a four-method finite comparison on one spatial mesh per case, not spatial convergence or an interval error proof.

Caught failures retain available failed-state bytes, completed method journals and reasons. Hard termination may prevent scientific JSON; the supervisor retains invocation streams and marks the case incomplete. Exclusive intents and atomic no-overwrite publication preserve failed and successful attempts. The inherited monitor is used only through its authenticated invocation definition, with the new bounded resources and serial two-case census. No automatic retry, third case or parallel numerical child is introduced.

The inverse consistent mass matrix is generally dense. Sampled guards and the inherited formal speed expression do not certify a finite-grid domain of dependence, CFL theorem or interstage no-crossing. All physical source/formation, observational, continuum and Stage 3 promotion flags remain false. Root execution and subsequent independent saved-result interpretation remain separate gates.
