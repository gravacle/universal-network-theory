# Ordinary-baryon alternatives remain viable sensitivity explanations

2026-10-04. Directly projecting the declared extended-gas profiles materially
reduces the nominal lensing type mismatch in several cases. Thus the current
lensing contrast alone does NOT establish failure of the force law or require
a type-dependent network coupling. This is a constructive limitation on our
earlier tension diagnosis, not evidence that these gas profiles exist.

The thirty exposed benchmarks retain all three nominal stellar masses,
10^10, 10^10.5 and 10^11 solar masses. The gas law, stellar shifts and scoring
mask were fixed before execution; no fit selected a preferred case. Below,
each triplet lists all three mass anchors in that order. Q uses the paired
14-component ESD covariance, not fourteen independent errors.

| High/low source treatment | Colour Q14 | Sersic Q14 |
| --- | --- | --- |
| No shifts or added gas | 55.19, 55.19, 55.19 | 46.53, 46.53, 46.53 |
| High-type gas only | 30.82, 20.57, 15.50 | 23.77, 13.62, 12.13 |
| High-type stellar shift only | 30.23, 27.82, 26.47 | 27.57, 25.63, 24.52 |
| High-type gas plus stellar shift | 15.57, 16.81, 28.67 | 12.06, 10.44, 22.51 |
| Equal gas on both types, no stellar shift | 33.00, 32.87, 45.70 | 26.88, 25.30, 37.40 |

For the middle mass anchor, gas plus the declared stellar shift changes
the contrast-only Q7 from 28.085 to 7.616 (colour), and 20.939 to 3.461
(Sersic). These overlap the absolute data and each other; their scores must
not be added. Equal gas preserves zero predicted contrast exactly. The
mass-dependent differences arise from the fixed 100-kpc gas radius, not a
new force-law parameter. Every profile and score is retained in the receipt.

This calculation adds no record halo, dark-particle halo or new lensing a0.
It DOES adopt an unmeasured differential ordinary-gas distribution and
illustrative stellar corrections. Calling those predictions would be wrong.
The study's gas prescription is explicitly approximate; its stellar offsets
are not independently known corrections. Missing source-pair weights and
mass scatter prevent interpreting the three anchors as a catalogue fit.
At the smallest anchor one bin falls below 30 kpc; at the largest, an outer
bin exceeds 300 kpc. Those compact-source/isolation cautions are saved for
each case; no point was removed after seeing a score.
[Source for the benchmark, Brouwer et al. sections 5.2 and 5.4](https://arxiv.org/html/2106.11677v1).

## Numerical evidence and review

All 38 frozen controls passed in 1.09 seconds. The arbitrary spherical mass
profile was projected through its actual force and radial derivative, with
the gas boundary split explicitly. Controls include an independent analytic
Newtonian truncated-isothermal result, zero-gas recovery, and 64/128-point
quadrature. An independent saved-data review reproduced all sixty Q values
within 3.1e-16 scaled difference, and eighteen Newton projection controls
using the alternate deflection-derivative expression within 1.3e-15.
Its first audit attempt used an unnecessarily exact floating-point mass
equality; that failed by rounding. The audit was completed with its existing
1e-14 relative reconstruction allowance. No scientific gate, force code,
input or score was changed, and no force fit was repeated.

Receipt EXTENDED_GAS_ESD_V001_RESULT.json SHA256:
0f55e92215203985cda1345d59917319f2846e66498e3e9602069c14461f145e

The next discriminating observation is a jointly constrained stellar/gas
distribution and ESD for the same selected populations, with source-pair
weights and selection propagated. This calculation shows why that evidence
matters. It is neither a proof of UNT nor a refutation of its effective force
response. Do not optimize more gas knobs against these exposed stacks and
call the improvement predictive superiority.
