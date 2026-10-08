# Independent native-carrier ruler analytical review V001

2026-09-29. Reviewed the complete `NATIVE_CARRIER_RULER_PATHWAY_V001.md`, final SHA-256 `4277871cd49f7e45169f3fd7db0b5d49b9b66651f6b4ac257d794a5230254db8`, against native BS06–BS11 and the accepted subdivision identities. **Accepted; no mathematical/operator correction required.** No numerical worker or fit was run.

## Owned generator and controls

With copying explicitly off and all noncarrier registers blank, the one-fixed-content carrier sector is invariant. Its diagonal is exactly native incidence energy plus `epsilon_psi+lambda_J*d_v`; transfer across an occupied edge is `-t_hop`, and link flips are `-Omega/N`. `J_uv²=P_u+P_v` in this sector, even when mean current is zero. The stated population continuity signs and coefficient `t_hop/hbar` follow directly from `i[H,P_v]/hbar`; no extra factor two is missing.

Compression onto a specified graph gives `epsilon_psi I+lambda_J D-t_hop A`, not an independently chosen mass–spring Laplacian. The off-graph flip images are mutually orthogonal, so the leakage norm is exactly Omega and the Duhamel/survival bounds have the stated absolute scope. Loss of an informative bound at later times is correctly not called actual instability or disconnection.

The native first-order spectral Schur complement has the correct off-diagonal minus sign and compulsory diagonal self-energy. Its derivative is negative semidefinite away from poles, `Sigma'=-H_BI(E-H_II)^(-2)H_IB`. Matching one off-diagonal entry requires `z²=2t_hop²` and leaves a nonzero diagonal correction. The four-vertex reflection-parity eigenvalues and inherited numerical radicals in equation (9) check. This is not the earlier scalar probe's second-order dynamic stiffness.

## Exact graph/preparation checks

Row-major incidence masks map `15 -> 350` and `11 -> 342`. The first is a four-cycle to six-cycle; the second is a four-vertex path to a six-vertex path. L0 retains degree two, so the full initial mean energies are `21.5 -> 31.5` and `15.5 -> 25.5`, including the carrier injection energy 1.5. Initial incidence-flip and carrier-hop images are orthogonal, giving variance `Omega²+t_hop²*d_L0=1.5` in all four preparations. The mean subdivision increment is exactly 10 for these basis/localized inputs, not for every coherent carrier or incidence state.

The note correctly distinguishes this new anchored tree11 experiment from the previous tree7 growth run: an unanchored graph isomorphism also moves the anchor. Results from tree7 cannot be silently reused as the same carrier geometry. The final prospective readout census is the unchanged eleven times `0,1/32,1/16,1/8,1/4,1/2,1,pi/2,2,pi,4`.

## Short-time path census and interference

The old source and reader are opposite bipartite sides. After subdivision their direct edge is absent and no two-hop carrier route connects them. There is exactly one two-Hamiltonian-operation route to reader arrival: flip the absent direct edge, then hop. Its product is `h_new*t_hop`; the propagator contributes `-tau²/(2hbar²)`. Hence the unconditional arrival probability begins `h_new²*t_hop²*tau^4/(4hbar^4)`, or **`tau^4/144`** at the inherited coefficients. Different final incidence configurations must not be coherently added to this probability.

For exact return to the prepared target graph, the leading amplitude is instead third order. It sums the ordinary three-hop routes and the single allowed flip–hop–flip route. All products have the same negative sign. There are two ordinary routes in the six-cycle (one retained old route and one new route), and one in the target tree. Thus equation (11)'s coefficient `-i*t_hop*(q3*t_hop²+h_new²)/(6hbar³)` is correct.

At inherited parameters the joint exact-graph amplitudes are `-i*(11/216)*tau³` for the cycle and `-i*(13/432)*tau³` for the tree. The frozen-graph coefficients are respectively `-i*tau³/24` and `-i*tau³/48`. The virtual flip contribution therefore cannot be reproduced by simply conditioning a full evolution on final graph return. These are leading coefficients, not finite-time dominance claims. Real basis preparations and a real held Hamiltonian make the population probabilities even in time, justifying the probability remainder orders stated in the note.

The C4 and C6 exact frozen-carrier amplitudes in equation (13) check independently from their adjacency spectra. Their short-time coefficients agree with the one-edge and two-length-three-path counts. Their common band edges do not imply identical transfer responses.

## Scientific use

This is a substantive move from an adopted scalar ruler to a native carrier/current observable, while retaining full incidence dynamics and its work. The anticipated numerical test can decide whether the declared connected subdivision changes native transfer and how quantum-incidence shortcuts modify the frozen control. It does not require a galaxy fit or a new hopping normalization.

The carrier is a deliberately prepared one-content state in a held, copying-off sector. Its native dimensionless clock and transfer are not yet meters, physical photon propagation, a universal ruler or a cosmological volume law. Those limitations follow from what the experiment actually includes, not from an additional approval or execution gate.
