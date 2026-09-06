# Hostile audit — connected finite-orbit reduction

An independent construction passes without correction. It generates the group from `T` and `S` by generator BFS, builds word orbits without consuming the target partition, and assembles the normalized quotient Hamiltonian by summing every full-basis hopping transition. This is materially distinct from the target's representative multiplicity assembly. It then derives signed oriented-edge orbits from the group action and uses RK4(4096)+Simpson rather than Taylor-10 evolution.

For L4/L6/L8 the group orders are 4/6/8; `T^(L/2)=S^2=1` and `STS=T^-1`. Support and source parity are invariant. Orbit dimensions are 76/720/8356, histograms exactly match the sealed packet, and reduced nonzero counts are 340/5,948/97,684. Direct all-transition matrix elements agree with `(H_orb)_{ba}=-n_ab sqrt(|O_a|/|O_b|)` within floating evaluation `8.89e-16`; Hermiticity mismatch is zero.

The derived oriented-edge quotient has three signed edge orbits at every size. Reconstructed signed currents and all occupations agree with sealed full-state calculations: maximum current differences are `4.52e-14`, `2.68e-13`, `4.23e-13`, and occupation differences are `1.87e-13`, `5.33e-13`, `1.11e-12` for L4/L6/L8. Continuity, norm, energy, number-sector law, and connected correlations agree within the declared numerical envelope.

The orbit identities and quotient formula are exact finite combinatorics. The evolved values and Simpson integrals remain numerical. This is computational compression of a supplied conditional support only: no autonomous support selection, new interaction, physical grid, continuum limit, Ward identity, critical or generic phase, graviton, or gravity follows. No correction required.
