# A cross-observable prediction of the ordinary-gas explanation

2026-10-04. Every one of the thirty frozen lensing gas benchmarks now has
an explicit foreground fast-radio-burst dispersion prediction. No gas,
force or electron-column parameter was fitted. This is a way to distinguish
the ordinary-gas alternative from a force-law change, not a new UNT success.

For the adopted truncated density Mh/(4pi Rh r^2), a full background sightline
at physical impact b<Rh has

    DM_observer = Mh acos(b/Rh) /
      [2pi Rh b mu_e m_p (1+z_l) (pc_in_metres*10^6)],

in pc cm^-3. The formula is zero beyond the specified100-kpc truncation.
This does not imply real gas ends there. We deliberately do not extrapolate
the singular profile through b=0 or use it for embedded FRB host paths.
mu_e=1.14 is an adopted fully ionized composition; DM counts free electrons,
not gas temperature. An ionization change must be counted, not used silently
to hide the predicted column. Clumping affects scatter and selection but
does not turn this linear column integral into an n_e^2 measurement.

One solar mass per square parsec gives35.4948031/(1+z_l) pc cm^-3. The middle
unshifted gas mass10^10.5 solar masses at50kpc gives37.4148076/(1+z_l).
The high-type stellar-shift cases inherit larger hot masses, and the equal-
gas cases predict nonzero absolute columns but exactly zero type difference.
The full saved curves cover seven fixed impact parameters and each case's
actual seven lensing radii, for redshifts0,.03,.2. Foreground/Milky-Way, host,
cold-gas, stellar and correlated-environment electron contributions are not
included or fitted away.

## Available observations and the real mapping limitation

Shirasaki et al.'s 2026 foreground study uses133 localized FRBs and2MASS.
Its appendix gives five excess-DM bins, diagonal errors AND four full
correlation matrices. The first two N1 measurements are18.2+/-44.8 and
29.7+/-73.7 pc cm^-3. The selected galaxies are not the isolated colour/
Sersic lens samples used here. Their radial pair-weighted stellar masses,
types and environment contribution are needed to predict that estimator.
The study's halo-gas inference additionally uses HOD/TNG modelling; it is
not a direct bound on our assumed hot-to-stellar mass ratio.
[Primary paper and appendix](https://arxiv.org/html/2601.21336v1).

An initial internal source review incorrectly reported that the covariance
was unavailable. Root inspected the appendix, found equations30–33, and
the reviewer confirmed the correction. Missing covariance is NOT a blocker.
The genuine missing link is the prediction-to-sample map, including random
subtraction and correlated foreground structure. Do not import this initial
review error into future handoffs.

A generic fixed-mass overlay is possible, even with a descriptive covariance
score, but would not adjudicate the lensing populations. No such score was
used to claim a gas detection, exclusion or UNT superiority. A matched test
would use the actual weighted mean of this kernel at each foreground's
stellar mass, type, redshift and physical impact, with independently handled
other electron components. It could remove a major lensing ambiguity without
requiring a new dark-halo or gravitational-response fit.

## Reproducibility

Producer: extended_gas_dispersion_v001.py, with its pre-execution specification
in the module docstring. All88 controls passed in .012seconds, including
independent line-of-sight quadrature, projected mass, redshift factors and
equal-column cases. Independent source/saved-output review found no blocker;
it did not rerun the numerical worker. Input masses and radius choices are
unchanged from the frozen gas receipt.

EXTENDED_GAS_DISPERSION_V001_RESULT.json SHA256:
3671dd06b0142260ae710a2fc45f5b88f8b3049573067f9bf7e7335e2fd00c11
