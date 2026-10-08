# Independent finite-mode constraint review

Read the full `FINITE_MODE_CONSTRAINED_RESPONSE.md`, including its expanding
de Sitter and physical-clock-tilt sections. The displayed finite-band scalar
result is accepted. No worker or old-source edit was needed.

In the local zero-curvature comparison, the shift fixes `zeta_dot=0` and the
lapse gives `zeta=-S/K_b`; therefore `S_dot=0`. After both constraints, the
energy is positive on the tangent subspace `b^T z=0`. Weighted
Cauchy–Schwarz gives `sigma^T K sigma-S^2/K_b>=0`, with equality only along
`delta_j sigma_j=constant`. That equality direction is static, not a freely
drifting zero oscillator. It is incorrect to replace this constrained
system by a clamped-source `K_b-chi=0` dispersion relation.

The bordered determinant has degree N−1 and positive roots. Distinct poles
give one root between each adjacent pair. At a repeated pole of multiplicity
r, r−1 source-orthogonal modes remain there; the scalar rational function's
visible zeros alone would miss them. The note retains this qualification,
the N=1 case, and the positive mass/stiffness of the transverse oscillators.

On exact de Sitter, the shift gives `n=zeta_dot/H`. The remaining Einstein
spatial terms cancel by the displayed boundary integration at constant H.
The retained cyclic coupling is proportional to `a^2 zeta_dot S/H`, giving
conserved `a^2 S/H` and hence `S proportional to a^-2`. For
`x0=(S/K_b)/delta`, `x0_ddot+3H x0_dot=-2H^2 x0`; this verifies the positive
`2H^2 B^T M x0` tangent-forcing sign. All finite positive tangent eigenvalues
give decaying homogeneous exponents; resonance at `Omega^2=2H^2` gives
`t a^-2`, not growth.

The acceleration coupling's lapse variation has sign `-C div B`, so its
linear energy density is `+C div B`. With the stated real Fourier phase,
this is `-C(k/a)S`. Zero momentum and anisotropic stress then give
`Phi=Psi=aS/(K_b k)`, decaying as a^-1. On a periodic domain this is signed,
zero-mean polarization density, not a positive missing-matter abundance.

The physical normal tilt resolves the possible growing coordinate lapse:
`v_dot+Hv=ell-(k/a)Phi`. Combining `zeta=-Psi-H pi`,
`n=Phi-pi_dot`, and `Psi_dot+H Phi=0` verifies that it is the same solution,
not a gauge-based dismissal. A finite-band mode with exponent s contributes
`exp(st)/(s+H)`, or `t exp(-Ht)` at resonance; both decay. Very slow finite
modes decay slowly, with no uniform decay as the smallest frequency tends
to zero. The algebraic slow-response limit recovers exactly the previous
`j=-1` positive de Sitter reduced action, fixing the contact normalization.

This supplies a constructive finite-band **linear vacuum scalar** stability
result for the specified common action and positive-J0 background. It does
not establish nonlinear foliation regularity, a uniform gapless-continuum
norm, an excited-background/matter-sector stability theorem, spatial sound
speed, native mode production or an observational cosmology. Those limits
are explicit in the reviewed derivation rather than hidden in the word
“stable.”
