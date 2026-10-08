# A calculated response coefficient, not another fitted halo parameter

2026-09-29. The same retained scalar mode state determines its energy,
pressure and weak-field polarization. For a mode with quadratic stiffness k,
quartic coefficient u, zero-source energy e and averaged pressure p,

    q=1-k*chi=3u(e+p)/(k²+4ue),
    mu_linear=sum(w*q)/sum(w).

The exact fixed-action displacement follows from the variational equation,
not an RMS-curvature approximation. The derivation and independent review
are in `FIXED_ACTION_SUSCEPTIBILITY_CONSTRAINT_V001.md` and its review.

## Completed same-state census

All 36 old returned-action preparations and 3,840 modes were evaluated without
a new trajectory, new population, source reset or fitted parameter. All
42,491 arithmetic checks and 54,600 independent high-precision saved-data
checks pass. The worker took 0.07933 seconds, peak self RSS 26,951,680 bytes.

The response coefficient is positive in every case, ranging from 0.00372502
to 0.0541510. The fixed shared template (row 6) gives mu_linear=0.00385470013,
with unchanged energy 8.77869337e-7 and pressure/energy 0.000609964535.
All 24 old-resolution comparisons are retained; the largest relative change
in mu is 3.24e-11 under spectral refinement and 1.05e-12 under step halving.
Those numerical comparisons are not physical-model uncertainty estimates.

For these fixed actions and a fixed positive gap, the strict small-source
law begins D(g)=mu_linear*g+O(g³). Preparation can therefore change the
low-field response even with the spectrum held fixed. One cannot infer the
whole finite-field galaxy curve from this derivative, or insert a guessed
linear-plus-quadratic interpolation and call it a derived law.

The accompanying conservative joint constraint for this soft band is
mu_linear>=max(0,3(E-15P)/I0), where I0=sum(w). It complements the pressure
bound; neither density, pressure nor the response floor is an independent
knob. Its s<=1 premise must not be silently applied to the new high-gap atom.

## Next use

The centered-turning-point reduction in
`FIXED_ACTION_FINITE_FIELD_REUSE_V001.md` permits a small full finite-field
calculation at the SAME actions. The complete 36-template, seven-field census
is being prepared, including every original held-source anchor as an
independent check. No galaxy fit or gravity boundary solve has yet been done.

All statements here concern a zero-source scalar phase-averaged response.
The isotropic vector response, constrained metric/clock solution and native
physical dictionary remain distinct work, not implied by arithmetic success.

Evidence: `PREPARED_SUSCEPTIBILITY_V001_RESULTS.json`, SHA-256
`0ce518ac17c84f0d116272597f9abb0ee5ab7bd41db8372699203ec9b7b21f40`;
`PREPARED_SUSCEPTIBILITY_V001_REVIEW.md` records the complete independent
audit and source identities. Earlier frozen results are unchanged.
