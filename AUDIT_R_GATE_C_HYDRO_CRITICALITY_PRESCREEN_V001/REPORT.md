# Blind independent hostile L4/L6/L8 seed screen

## Disposition

```text
NO_CANDIDATE_L4_L8
```

The independently reconstructed sector rows contain no seed at L4, L6, or
L8.  All `18/18` structural and numerical controls pass, every active pole is
stable under the frozen factor-ten weight-threshold screen, and no row is
unresolved.  The complete numerical core was reproduced exactly in a second
run.

This no-seed disposition stops the protocol before L10/L12 and before every
spatial or macroscopic follow-up.  It is not a theorem that no critical
density exists in a different physical parent or larger family.

After this blind result was frozen, the target packet was opened and
hash-pinned.  The final hostile comparison passes `256/256` with verdict

```text
PASS_HOSTILE_NO_CANDIDATE_L4_L8__STOP_NO_L10_L12
```

It compares all 18 non-vacuum sector rows and 90 core numeric components,
checks all 21 target spectrum hashes, and independently confirms that no
L10/L12 or macroscopic artifact was emitted.  Maximum target-versus-audit
differences are:

| quantity | maximum absolute difference |
|---|---:|
| ground energy | `1.066e-14` |
| `Delta_Q` | `3.553e-14` |
| `Delta_act` | `1.421e-14` |
| `chi_tau` | `4.663e-15` |
| `R_low` | `1.665e-15` |

The target passes `36/36`; this audit passes `256/256`.  Neither has an
unresolved row, threshold switch, seed sector, or candidate interval.

## Independence custody

The frozen protocol SHA-256 is
`3da9e74b0dcc2d8b65ce98cfb42735864cf3d045e41655082baa7a7a295cb334`.
The blind methodology SHA-256 is
`301af100a7648d5773642aece6872bec647d0dceaaec83b79c96e3a5b060cae9`.
The executed V002 code SHA-256 is
`8cf6e3fd5c5e7cc27843bffe8dd1bb54895a980cc540a4379ed495d916295cd7`.
The independent result SHA-256 is
`39625068c0694f3e8e111fc1285af76269fceae6338fa99dc6723ab89b3c71d4`.

The target result was not inspected before the method, code, and independent
result were frozen.  V001 failed closed before result emission when the host
NumPy/Accelerate complex batch product raised a floating-point-status
warning.  `CANDIDATE_FAILURE_V001.json` preserves that event.  V002 changes
only that backend product into four explicit real products; it changes no
operator, sector, threshold, or decision rule.

## Independent finite rows

Each row is `(q, rho, Delta_act, chi_tau, R_low)`.

```text
L4
1  0.125000  2.000000000000  0.395284707521  0.500000000000
2  0.250000  2.463075497383  0.341638044263  0.428094707816
3  0.375000  2.645981058604  0.317001733175  0.386692236910
4  0.500000  2.988994832086  0.291628290136  0.380601985549

L6
1  0.083333  1.000000000000  0.881917103688  0.750000000000
2  0.166667  1.432775714720  0.605628323016  0.668501057211
3  0.250000  1.667371519016  0.520382482559  0.632801772065
4  0.333333  1.842230479633  0.469772940558  0.618498808920
5  0.416667  1.936393471035  0.440047139164  0.588502633854
6  0.500000  2.135581210921  0.405535110433  0.590417241479

L8
1  0.062500  0.585786437627  1.584089449338  0.853553390593
2  0.125000  0.914145763802  0.986479251231  0.784968830264
3  0.187500  1.120212007236  0.797042809501  0.749151132542
4  0.250000  1.266065438740  0.702672515155  0.732829820694
5  0.312500  1.382688542611  0.641938710557  0.724792504673
6  0.375000  1.467715856369  0.602147285183  0.715899284710
7  0.437500  1.496802966818  0.579854287421  0.679290393627
8  0.500000  1.647631701513  0.532236797700  0.687595061305
```

At every size, `Delta_act` increases over the scanned sharp-density sectors
while `chi_tau` decreases.  Consequently no interior sector is a coincident
strict local gap minimum and response-timescale maximum.  Residues remain
well above `1e-6`; absence of a seed is not caused by the activity threshold.

## Structural controls

The audit independently reconstructs:

- `2L` sites, `3L` unique owner edges, and degree three at every site;
- exact carrier-number conservation by every occupied/blank bit swap;
- exact particle-hole graph equivalence by bit complement;
- exact chiral pairing from odd-site-occupancy parity;
- the one-carrier bands `-2*cos(2*pi*m/L) +/- 1`; and
- absence of any write-count argument in the Hamiltonian constructor.

The largest one-carrier band error is `1.333e-15`.  L6 has four exact
one-carrier zero eigenvalues from commensurability; they are retained as the
frozen false-positive control and never enter the ground-to-`n_k` active-gap
decision.

The first full run took `46.288344334 s` and reported `724,680,704` bytes
maximum RSS on the Darwin host.  The exact-core replay took
`37.838549750 s` and reported `725,286,912` bytes.  These are environment
observations, not complexity laws.

## Claim boundary

**Proved inputs/reconstructions:** finite topology and owner census, exact
bit-swap `Q` conservation, particle-hole isomorphism, chiral anticommutation,
one-carrier band formula, and response-momentum selection.

**Adopted:** sharp-sector projection, the `m=1` total-rail density channel,
density cells, activity floor, and seed extrema rule.

**Conditional:** the connected prism parent, source preparation, phase,
clock, and finite numerical representation.

**Empirical/numerically certified:** all displayed finite sector energies,
active gaps, response-time moments, residues, residuals, and resource
observations.

**Open:** any L10/L12 behavior, candidate or unique `rho_c`, spatial decay
transition, macroscopic predictive closure, mode universality, two-cluster
field, thermodynamic/continuum behavior, and gravity.

No continuum, grid, Ward, phase, graviton, emergence, or gravity statement is
made.
