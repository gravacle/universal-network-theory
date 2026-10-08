# Independent review: compression of the same prepared actions

2026-09-28. All 36 original returned-action cases and 3,840 modal entries are
retained. No new population, trajectory, source fit or cosmic normalization.

## Outcome

The same saved state that fixes the held force and zero-source pressure also
fixes a positive common-current adiabatic compression coefficient. It is not
an independently chosen equation-of-state or sound-speed parameter.

| Ramp duration | Source amplitude | Excitation P/E | Compression coefficient |
|---:|---:|---:|---:|
| 8 | 0.0025 | 0.0006099645 | 0.0011225018 |
| 8 | 0.01 | 0.0023011366 | 0.0042078661 |
| 8 | 0.04 | 0.0080195802 | 0.0144182636 |
| 16 | 0.0025 | 0.0017596263 | 0.0032194687 |
| 16 | 0.01 | 0.0060197854 | 0.0108456875 |
| 16 | 0.04 | 0.0172206803 | 0.0299943408 |

These main rows use the unchanged gap=0.001, 128-mode, dt=0.005 preparations;
all other gap/quadrature/time-step rows remain in the result. The coefficient
is dP/dE along the declared **common-current adiabatic compression**, with the
excitation enthalpy in its denominator. The fixed vacuum baseline has zero
derivative and has not been used to make this number artificially small.

## Analytical audit

The period and action normalizations give

    e_II = omega² u K / [2 J (k+u b²)] > 0,
    c_ad² = sum(w I² e_II) / sum(w I omega).

The positive zero-source quartic hardening proof is valid and is not extended
to the previously identified, potentially softening, displaced-source case.
Bounding both logarithmic amplitude derivatives by the pointwise range of
u b²(1+sin²theta)/(2Q) gives the stated rational bounds on I e_II/omega,
strictly between zero and 1/3 at finite positive gap and amplitude.

The stronger pressure bound also checks. The normalized time weight's
logarithmic derivative decreases with sin²theta, whereas sin⁴theta increases;
their covariance is nonpositive. Consequently d ln p/d ln b≤4 and
d ln I/d ln b≥2, giving I²e_II≤2p and therefore

    0 < c_ad² < 1/3,
    c_ad² <= 2P/(E+P).

These are exact properties of the stipulated positive-weight state mixture,
not fitted numerical inequalities.

## Independent numerical audit

The production source, protocol, freeze and result plus original action/state
ancestry were authenticated. All 252 production row gates and the complete
36-row census pass. The production independent real-amplitude derivative
comparison has maximum relative discrepancy 8.41994e-13.

The additive audit used uniform midpoint quadratures at 512 and 1,024 angles,
rather than the production Gauss rules. For **every mode**, it independently
computed d omega/dI by complex-step differentiation of the period and action
at b(1+i epsilon), using epsilon=1e-20 and 1e-25. This avoids both the
production K-integral curvature expression and its real finite-difference
Richardson check. It also avoids subtracting nearly equal full frequencies
in almost harmonic modes. All returned actions, periods, modal curvatures,
bulk sums, enthalpies and both analytical bounds pass; the maximum scaled
discrepancy is 1.99841e-15.

Reproducible audit: `prepared_compression_independent_audit.py` and
`PREPARED_COMPRESSION_INDEPENDENT_REVIEW_DATA.json`.

- Production source SHA-256: `c0034e89ad90fbd5ab3c3a40c95aa04cb30f867add72d790de2c72029b69f7d5`.
- Freeze SHA-256: `1abb2da79b425f7f29d9a48351e0b2a352c90573410b3ad8fe0f265f7aea2db0`.
- Production result SHA-256: `a6fa29a21272c173d7cd3f8c2fa89894f1a3fce482c7ac6818991bff52392a2f`.
- Independent source SHA-256: `203c0b7ff49a84a30d5d92354071754fa1c1f5fdf691c461d8ae47742bc2f52a`.
- Independent result SHA-256: `a3f74cb9256d4f906a0793e91204281bca13bd2b94163f9027362abdae9da507`.

## Physical interpretation and constructive continuation

The prepared mixtures are weakly restoring relative to the quartic 1/3
limit, but that alone is not a cold-clustering result. If these numbers were
identified with a physical fluid c_s²/c², the six square roots would be
approximately 0.034–0.173, not automatically small on galactic scales. The
microscopic spatial principal system, metric/clock constraints and physical
matching have not yet established that identification.

There is a definite same-state cooling route within the adopted finite-band
adiabatic closure. For k_j>0 and common dilution I_j→q I_j,

    e_j = omega0_j I_j + alpha_j I_j² + ...,
    alpha_j = 3u/(8m k_j),
    c_ad²(q) = q [sum(w 2alpha_j I_j²)]/[sum(w omega0_j I_j)] + O(q²).

Thus expansion with q proportional to a^-3 drives this coefficient to zero,
provided the specified adiabatic regime remains valid. It does not require a
new pressure knob or an invented population. This is a conditional asymptotic
consequence, not a demonstration of the actual cosmic initial actions,
expansion history, zero-gap limit, or successful structure formation.
