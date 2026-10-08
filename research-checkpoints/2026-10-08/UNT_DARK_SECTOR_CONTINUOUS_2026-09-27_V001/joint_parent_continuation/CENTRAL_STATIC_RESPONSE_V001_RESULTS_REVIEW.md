# Independent review: same-state central static response

2026-09-29. **Accepted as a qualified conditional scalar diagnostic.**
All 42 states, 4,614 modal entries and 24 preparation/spectral sensitivities
are retained. The 36 original states still have null center coefficients
because these selected inputs do not own a numeric same-spectrum DeltaU.
All six pulse centers use their actual finite-spectrum baseline, unchanged.

The main constructive result is now quantitative: keeping the stored energy
and phase-equilibrium condition determines both the polarization response and
the central active source. Making a mode cold does not make its static
phase-population response weak. Neither response is an independently tunable
halo density in this calculation.

## Results and their interpretation

| State family | Kcal range | J_static range | J_static/Kcal range |
|---|---:|---:|---:|
| 36 original soft states | 0.00186250–0.02707549 | 0.2222244–0.2238090 | 8.26611–119.31487 |
| Six soft-plus-hard pulse states | 4.41218e-9–1.80029e-5 | 6993.82–1.78962e6 | 3.91061e8–4.05599e14 |

These are the inherited dimensionless scalar quantities, not measured
galactic lengths or time-growth rates. The representative original template6
has Kcal=0.00192734814, J=0.22222909938 and J/Kcal=115.30304005.

In the pulse states, the hard mode supplies more than 99.9602% of Kcal and
99.9968% of J; the soft fraction of the energy is at most 1.84e-10. The soft
sector nevertheless has J approximately 2/9 because every retained mode is
on its **occupied** phase branch, even when its action is very small. That
derivative is not additional stored energy. The strictly empty branch is
different and was not substituted for any occupied mode.

The hard-mode behavior agrees with the independently interpretable harmonic
limit at fixed weighted hard energy E_H and weight beta:

    e_II ~ 3/(4R²),
    J_hard ~ (4/3) beta R⁴,
    Kcal_hard ~ 3 E_H/R⁴.

For these six states, ratios to the displayed leading J and K expressions
are respectively 1.0000017–1.0070795 and 0.9956518–0.9999989. Thus the large
static ratio has a clear source: weak hardening makes the occupied action
strongly responsive to lapse changes, while the polarization nearly cancels
the bare linear contact. This does not establish a finite-radius static
solution or a dynamical instability.

### Owned center signs are retained, not selected

The old finite-spectrum DeltaU values are 13.9518283–13.9520894. In all six
pulse cases they give a negative `E + 3Pi - 2DeltaU`, hence a negative a1
in the regular averaged-scalar expansion `a(r)=a1*r+O(r³)`:

| Hard R | Pulse amplitude | E+3Pi-2DeltaU | a1 |
|---:|---:|---:|---:|
| 32 | 1 | -27.50883525 | -8.117317e6 |
| 32 | 4 | -21.57768681 | -3.995231e5 |
| 64 | 1 | -27.50936147 | -1.298846e8 |
| 64 | 4 | -21.58700757 | -6.371726e6 |
| 128 | 1 | -27.50939438 | -2.078294e9 |
| 128 | 4 | -21.58759478 | -1.019335e8 |

This is an outward, vacuum-dominated **local averaged-center** slope, not an
attractive halo center. The corresponding signed effective central density
includes the polarization divergence and is also negative; it is not equal
to the positive oscillator Hamiltonian energy alone. The full center mass
identity is satisfied. Large coefficients limit the radial extent over which
this local Taylor expansion can be used. No global integration, smooth
microscopic vector-center construction or cosmological boundary matching was
performed. These signs concern these actual finite-spectrum preparations;
no separately calibrated or infinite-gap state was substituted for them.

## Independent saved-data audit

`central_static_saved_audit_v001.py` imports no producer and performs no orbit
quadrature, turning-point calculation, propagation or fit. It authenticates
all 52 members of the new freeze and the selected original result payloads.
The earlier preflight independently traversed 11 inherited manifests,
158 member occurrences and 43 distinct ancestral members.

The saved audit reconstructs every modal contact defect from the original
energy/pressure, every modal J from the original action/frequency and new
e_II, all weighted E/Pi/Kcal/J sums, soft/hard component sums, six center
identities, all 42 dilution associations and 24 signed sensitivity contrasts.
For the original 36 it also compares e_II with the separately saved
compression census. For the six pulse cases, new e_II remains the original
producer's independently controlled quadrature evidence, not a fresh
quadrature by this reviewer.

All 18,942 arithmetic comparisons pass; maximum normalized recombination
difference is 2.62e-15. Absolute differences are also retained: for example,
the largest J/Kcal is about 4.06e14, so a 0.125 absolute sum-rounding difference
is only 3.08e-16 relative. No tolerance was changed or small mode discarded.
The original 114,773 controls all pass, with largest normalized error
3.51e-15. The original run took 0.206816 s and reported 44,040,192 bytes peak
**self** RSS, not whole-job memory.

Maximum relative differences across all retained old preparation/order
comparisons are 2.26e-11 in E, 2.05e-10 in Pi, 3.24e-11 in Kcal,
4.31e-14 in J and 3.24e-11 in J/Kcal. These are comparisons among the
already retained preparations, not new physical tests or a claim of
universal continuum convergence.

## Exact identities and evidence locations

| Artifact | SHA-256 |
|---|---|
| Original result file | `7a930081b22bd902ab8f2e4d8cf3547899901cdfe3597416fa6595576a9c9abf` |
| Original freeze | `385c147a413f59e8636edcdfbbb36bfde8ce55819aae954143191eb235b1fc20` |
| Original payload | `64f6889a363d0b09f31bdeba19561dd8dbbb9573ebe082ecb7a6dfc1045d17d7` |
| Independent saved-audit script | `28c9557a00271a24bfa39081b865bc5f300cd9e1f2db4e85face6b79833ff379` |
| Independent audit payload | `d6728a5bfa708503d6d90351d03ac2aa9ca55f6ab623ba29bf6917299ac578c8` |

The additive receipt is `CENTRAL_STATIC_SAVED_AUDIT_V001.json`; source and
protocol are bound in `CENTRAL_STATIC_RESPONSE_PREFLIGHT_V001.md`. The
producer's compressed transport did not change its decoded result bytes.
No frozen input, source, baseline or criterion was altered by this review.

The next scientific use is to retain these owned stress and response
derivatives in the specified static boundary problem, not to identify J/Kcal
with an empirical radius. The independent clock, vector-state and boundary
conditions still determine whether such a local scalar response can be part
of a physically admissible galaxy solution.
