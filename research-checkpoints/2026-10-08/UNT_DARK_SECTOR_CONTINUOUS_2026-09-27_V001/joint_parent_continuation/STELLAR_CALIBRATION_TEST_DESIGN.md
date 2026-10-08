# Fixed stellar-calibration comparison — additive design, not executed

## Question and one new source identity

Does substituting the independently specified **3.6-micron M/L=0.5 convention**
for Leroy's K-band-derived convention change the existing residual pattern at
the unchanged gravitational law? This is a post-exposure source-consistency
experiment, not a blind prediction, a new fit, or an assertion that M/L=0.5 is
the true stellar mass. The four original outcomes must remain unchanged.

Use only the source identity `ML36_CAL_HI1_H21_V001`, with both existing gas
exponential-tail choices retained. Read, without rounding,

```
c = PHOTOMETRIC_SOURCE_COMPARISON.json[
    "same_imaging_same_geometry_mass_conversion_ratio"]
  = 1.2567828155112788.
```

The audited arithmetic is `c=(0.5 * 10^4 * 10^(0.4*3.24)/280.9)/280`.
The many output digits describe this arithmetic, not observational precision
of the rounded published coefficient 280. No velocity determines `c`.

Define the entire source, including core and tail, by

```
Sigma_new = Sigma_HI,He + Sigma_H2,He + c Sigma_star,Leroy.
M_new     = M_HI,He + M_H2,He + c M_star,Leroy.
```

Keep all radii, interpolation knots, gas helium factors, stellar tail length
3.2 kpc, HI tail length, H2 tail length 2.7 kpc, coplanar thin geometry, distance
13.8 Mpc, `a0`, and the already frozen constitutive shape parameter unchanged.
This scales the **Leroy profile**, not the resident SPARC brightness profile.
Do not apply `cos(73)/cos(72)`, switch inclination, replace the radial shape,
or renormalize to a rounded catalogue mass. It is specifically the
same-imaging/same-geometry convention comparison from the retained audit.

## What follows without another PDE

Let `M0` be the original HI1/H21 total and `Ms` its original stellar mass. Then
`M_new/M0=1+(c-1)Ms/M0`, approximately 1.129 for the saved source. The ideal
continuum isolated deep-law asymptote therefore has

```
v_infinity,new / v_infinity,old = [1+(c-1)Ms/M0]^(1/4),
```

approximately a **3.1% increase**, not a decrease. Raising this mass cannot
repair a genuine *asymptotic* outer overprediction. This statement is
conditional on the ideal deep-law window and finite isolated baryonic mass;
it is not a proof that the observed last radius has attained that asymptote.
Physical finite-gap/thermal/pinning limits remain separate.

More generally the spherical fixed-radius relation is
`f(g)=G M/(a0 R^2)`, hence `dg/dc=G Ms/[a0 R^2 f'(g)]>0`. That proves the same
direction for the spherical diagnostic, **not** for every radius of a disk.
Increasing a nonnegative source orders potentials under the appropriate
common Dirichlet comparison problem, but does not order their radial
derivatives. Here the boundary mass also changes. It would be incorrect to
infer a universal pointwise increase of the actual disk rotation curve from
ellipticity or from the scalar monotonicity of `f` alone.

The Newtonian disk has an exact, cheaper statement:

```
Phi_N,new = Phi_N,gas + c Phi_N,star,
g_NR,new  = g_NR,old + (c-1) g_NR,star.
```

The frozen ring result already stores signed component fields at all five
oracle radii, all three heights, and both quadrature orders. These determine
the recalibrated Newtonian oracle by arithmetic alone. Thus its sign and
change at these radii need no new Newtonian PDE or quadrature. Preserve any
outward component; do not replace it with an unsigned mass contribution.

There is no corresponding nonlinear superposition identity. Nor is multiplying
the entire old speed by `sqrt(c)` or `c^(1/4)` valid: only the stellar part was
scaled, and the source is a disk in a law with a transition scale. A complete
finite-radius answer about repairing an inner deficit, worsening an outer
excess, or changing the radial shape needs the new nonlinear field.

## Smallest safe implementation

Do not edit or monkey-patch any frozen module. A small additive runner can
reuse `disk_solver.f/inverse`, `axisymmetric_disk_v002.mesh/solve`, and the
existing density primitives. Its source constructor should create fresh
objects, for example:

```python
old = galaxy_density.profiles(True, True)
components = dict(old)
p = old["stars"]
components["stars"] = galaxy_density.Profile(p.r.copy(), c*p.s, p.tail)
```

Never mutate `old` arrays. Use the returned `components` consistently in all
four places: exact annular bottom flux, component masses, monopole boundary
mass `q=G M_new/a0`, and the source identity/result ledger. Retain the old
same-law boundary quadrature and solver, not an old boundary with the new
source. The optional starting potential may be the corresponding old solution
after provenance checks; this is only a numerical initial guess. A fresh
mass-consistent smooth initial guess is simpler and avoids hidden dependence.

The old `galaxy_field_compute.run_case` cannot directly accept this source:
it hard-codes density construction, filenames, reference cases, and its
freeze. Reuse its reviewed pattern in a narrowly named additive driver,
without invoking its `main` or replacing its module globals.

For a scientifically qualified new nonlinear curve use precisely the same
three cases as before:

```
ML36_CAL_HI1_H21_V001_N256_L255_Newton0
ML36_CAL_HI1_H21_V001_N320_L1023_Newton0
ML36_CAL_HI1_H21_V001_N512_L255_Newton0
```

There is only one new source and no calibration grid. The three cases retain
the existing resolution/domain qualification rather than assuming it transfers
unchanged across sources. Use the inherited source-mass error `<=1e-13`, flux
balance `<=2e-6`, residual `<=1e-9`, zero clipped faces, and `<2%` radial-force
changes at the existing `R>=2 kpc` comparison radii. No new observational or
sign-based acceptance gate is appropriate. Failed cases and checkpoints are
preserved under the new identity; they cannot overwrite original cases.

### Independent Newtonian oracle without new integration

Authenticate the original ring freeze, complete result, source hashes and
payload before using its HI1/H21 component ledger. At each original height
and order form

```
g_new(z,order) = g_old(z,order) + (c-1) g_star(z,order).
```

Apply the original two linear-height extrapolations **after** this composition,
retaining both estimates and the 48/96 differences. Scale stellar mass and
omitted-tail mass by `c`; gas masses are identical. The same positive mass
tail bounds remain valid with the new summed omitted mass. This is an
independent-of-FV **recombined qualified oracle**, not a fresh independent
numerical implementation or independent statistical measurement.

No additional Newtonian PDE is necessary for this source-only oracle or for
testing the change of the nonlinear predicted curve. If the new source is
also to receive the full same-domain solenoidal decomposition from
`DISK_RESPONSE_DIAGNOSTIC.md`, add **one** separately named `N512/L255/Newton1`
case and check it against the recalibrated five-point oracle with the original
allowance. The old total Newtonian grid alone cannot be rescaled correctly;
its stellar component grid was not saved. Do not pair a changed nonlinear
source with the old-source Newtonian grid.

## Prospective custody and comparison

Before any new worker, save source code and protocol and freeze their hashes
alongside the exact calibration JSON/script, its retained input hashes, the
complete HI1/H21 originals, the old numerical qualification, ring source and
result, raw density ancestors, and unchanged law/shape/velocity inputs. Verify
the calibration JSON's `source_sha256` and `input_sha256` against their actual
files; it is not itself a pre-existing numerical freeze. Do not run the
source-audit script merely to regenerate a potentially changed scalar.

Report all 43 original radii and inherited `R>=0,2,8 kpc` summaries, paired
old/new signed accelerations, speeds when real, and signed residual changes.
Keep the original observational geometry and uncertainty caveats. The outcome
can establish sensitivity to this one independently specified stellar
convention; it cannot establish that this convention is preferred by an
independent measurement, or turn the already exposed galaxy into a held-out
validation. The proposal has not been frozen or executed.
