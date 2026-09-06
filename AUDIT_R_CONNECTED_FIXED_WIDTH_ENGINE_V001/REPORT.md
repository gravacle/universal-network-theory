# Hostile audit report: connected fixed-width engine V001

## Verdict

**PASS; target unchanged.** The engine is authorized only as a guarded numerical implementation candidate for an L14 trial. This audit does not authorize an L14 result or any physics promotion.

## Independent attacks

The audit reconstructed the order-eight L4 action from full group images, without importing target functions. Every one of the 256 words was assigned exactly once to 55 orbits, and independently emulated two-chunk permutation tables agreed word-for-word with direct 8-bit permutations.

The 330 active unaggregated transitions were assembled separately. For a deterministic complex invariant test vector, their normalized action agreed with direct projection of the full 256-word owner-once Hamiltonian to numerical roundoff. Repeated destinations therefore change storage form only; aggregation recovers the same operator.

The byte-sized orbit-size array is safe only as structural storage. On the audited NumPy build, `sqrt(uint8)` does produce `float16`; explicit conversion to `float64` before the square root exactly reproduces `sqrt(|O|)/sqrt(2^L)` in float64. The disclosed pre-result attempt failed closed at this implementation defect, and no failed value appears in the result.

## Signed-current formula

The audit derived both signed edge orbits from the finite permutation action, formed the target-style signed sum over all unaggregated owner-once transitions, divided only by the finite orbit cardinalities (`2L` internal and `L` connector), and reconstructed all 12 oriented L4 edge currents. These values agree directly with the corresponding full-word current operators on an arbitrary invariant complex vector. This test uses no incidence balance, continuity equation, record-ledger residual, or Ward identity. The reduction is a finite symmetry/operator identity only.

## Lower-size parity and custody

The target replays `40/40`. A separately implemented and previously hostile-audited generator-BFS/destination-normalized quotient with RK4(4096)+Simpson reproduces every sealed L4/L6/L8/L10 occupation and oriented current; the present audit also checks each maximum connected-edge correlation against its sealed result. Target files, sealed lower-size results, and the independent implementation/results are SHA-256 pinned by `verify_audit.py`.

The claim classes are sound: orbit construction and finite operator equivalences are exact; evolution, quadrature, currents, correlations, and tolerances are numerical; source/support/`kappa`/routing/content/clock/read remain conditional. No continuity or Ward axiom, autonomous support, grid, continuum, phase, graviton, gravity, scaling, convergence, fit, or complexity law is inserted.

No target correction was required.
