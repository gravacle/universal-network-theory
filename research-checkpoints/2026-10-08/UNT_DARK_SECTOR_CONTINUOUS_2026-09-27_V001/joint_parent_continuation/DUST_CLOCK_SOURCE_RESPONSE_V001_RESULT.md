# Ordinary matter generates an optical response in the declared clock model

2026-10-05 UTC. New local-pole and short-time source calculations. Internal
independent equation/source reviews completed; not external peer review or
an observational cosmology. The full program and all eleven lanes stay open.

## What was actually learned

The constant-trace beta=.5 example has finite-scale enhanced ordinary-source
gravity. It does not require an additional homogeneous dust species for this
linear effect. The positive growing branch is bounded in the ultraviolet;
it is gravitational growth, not a scalar ghost or the common-filter UV failure.

All 853 local-pole controls qualify in the complete V002 result. The initial
V001 attempt failed during NumPy-boolean serialization; its source and partial
JSON remain. A separately documented wrapper fixed serialization only.

| Epoch a | Largest sampled s/H | Physical inverse wavenumber | Actual wavelength | E-folding time |
| --- | ---: | ---: | ---: | ---: |
| .1 | 141.995 | 17.783 kpc | 111.733 kpc | .0191604 Gyr |
| .3 | 216.600 | 30.000 kpc | 188.496 kpc | .0574288 Gyr |
| 1 | 128.477 | 56.234 kpc | 353.329 kpc | .191678 Gyr |

These are fixed-background instantaneous poles, not accumulated cosmic growth
or a selected spectrum. The receipt field `growth_inverse_Gyr` means 1/s in
Gyr, NOT a rate in Gyr^-1. Its deep-field amplitude screen is asymptotic and
cannot be used at high q where its own allowed amplitude leaves that regime.

## A source evolution, not just an eigenvector

The next test kept beta, ell100pc, omega_b=.02235, the inherited endpoint and
the prepared ordinary contrast Delta_i=1e-8 fixed. It evolved from a=.1 to
.10512711, with zero ordinary velocity, relative tilt and instantaneous
comoving Poisson clock contribution initially. This is NOT a native or
primordial growing-mode state. The same predicted scalar potential governs
matter and Weyl lensing at the retained order.

| Comoving k (Mpc^-1) | Ordinary contrast growth | Potential growth | Potential / bare-G potential of SAME evolved ordinary density | Largest estimated constitutive correction fraction |
| --- | ---: | ---: | ---: | ---: |
| .01 | 1.002515 | 2.16464 | 2.26991 | 1.01e-8 |
| .1 | 1.069663 | 122.667 | 120.558 | 3.40e-6 |
| 1 | 8.439832 | 17773.6 | 2213.89 | .002607 |

The absolute potentials are only of order 1e-12. These large RATIOS are not
observed enhancement factors, inferred halo masses, or acceptable cosmological
growth predictions. No extra population was selected to obtain them.

The first correction uses the actual nonanalytic deep-field constitutive
term and its generated odd harmonics. It is not a full nonlinear solution.
In V001, 91/95 controls passed; four failed harmonic-tail gates at k=.01,.1.
V002 extended only these unresolved sums with unchanged criteria, and all
40 new controls pass. It also adds the stricter time-uniform tail-amplitude
check. The k=1 result remains the qualified V001 calculation; no needless
repeat. Correction fractions use interval peak amplitudes, not pointwise
relative errors at waveform zeros. A formal infinite-tail theorem is not
claimed merely from refinement.

V001 took6.7407s, V00222.3236s. No numerical worker remains active. Their
physical metric/density/velocity/constitutive working screens pass, but the
heuristic omitted-metric ratio is NOT a covariant remainder bound. A maximum
acceleration cannot serve as a lower local stiffness bound at wave nodes.
The controls check implementation and refinement, not all action remainders.

## What this does and does not establish

This is a constructive, source-driven dynamical signal in a conditional
modified interaction model. It improves on simply assigning a halo response
or an arbitrary independent source abundance. It does not yet show acceptable
structure formation, correct lensing observations, averaged acceleration,
or a native network formation law. Fast amplification may itself create an
observational problem once physically selected seeds are used.

A zero-mean linear mode cannot change homogeneous expansion at first order.
The next decisive calculation is conservation-complete quadratic source work:
fix the curved vector filter, vary its lapse and spatial metric, include
ordinary-dust advection and Einstein/trace sources, and retain mean plus2k
response and homogeneous shear. Those terms must be tested on the saved
trajectory before increasing its amplitude or extending its duration.

## Durable evidence

- Local-pole complete V002 JSON SHA256:
  1d6e9f9afc69e732781d6d13761fd89c349d027707c32ed5ed41def679e25a87
- Short transient V001 JSON SHA256:
  489364c23fca12b5b9bbf3fa10774f4f36b1f574ccfe6a25af14bc6202d2ada7
- Short transient refined V002 JSON SHA256:
  46914954e00cbb76340c72612fae40bcd4ba9d7f7a55945b939b7dfc6f62e221

Frozen protocols, sources, failed attempts and repair/refinement notes sit
beside these receipts. No observational threshold or model parameter changed.
