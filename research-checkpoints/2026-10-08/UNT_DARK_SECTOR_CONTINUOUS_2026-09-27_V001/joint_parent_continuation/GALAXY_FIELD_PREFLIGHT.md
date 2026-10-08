# Independent preflight: fixed-density NGC 3198 field calculation

2026-09-28. Source review began before freeze; the final narrow amendments
and frozen identities were then checked read-only. No galaxy solver or
observation-scoring worker was run by this reviewer. This is a prospective
implementation/scoping acceptance, not a galaxy-result acceptance.

## Verdict

**Accepted for the declared four-source development experiment.** The
physical units, exact annular integrals, total-source nonlinear equation,
boundary normalization, fixed comparison choices and completed-iteration
resume path are consistent. The previously requested qualification-identity,
empty-summary and Newtonian-oracle comparison corrections are present.
No further source changes are requested.

Read completely: `galaxy_density.py`, `galaxy_field_compute.py`,
`NGC3198_FIXED_DENSITY_PROTOCOL.md`, the source/outer-gas/input-readiness
reviews and `checkpoint_smoke.py`. This review relies on the separately
recorded primary-table transcription reviews, not a claimed third visual
transcription of the original PDF.

## Units and source integration

The input surface densities are in solar masses per square parsec and
the radial coordinates are kpc. The conversion `10^6` in
`M=2pi*10^6 integral R Sigma dR` is necessary and correctly included.
The code applies helium once to bare H I and does not reapply it to the
already corrected H2 values. H I angular radii are rescaled by distance;
the column-density amplitude is not spuriously rescaled with distance.

On a linear interval starting at radius `a`, with density `S_a` and slope
`s`, the implemented integral over width `w` is exactly

    a*S_a*w+(a*s+S_a)*w^2/2+s*w^3/3.

For an exponential continuation the primitive
`ell*(R+ell)*exp[-(R-R_last)/ell]` has derivative
`-R exp[-(R-R_last)/ell]`. Its lower-minus-upper use and infinite-endpoint
limit are correct. The same declared interpolant therefore supplies both
total masses and every finite-volume annular source, without normalization
to the disputed catalogue total or the observed rotation curve.

The conversion of acceleration is

    a0=3702.81309778964 (km/s)^2/kpc.

With `q=G*M/a0`, the monopole input `q/s^2` is a dimensionless acceleration
in a0 units. The solver potential is represented in a0-times-kpc units;
its radial derivative is `g_R/a0`. Consequently
`v_c^2=R_kpc*a0_kms2_per_kpc*g_R_dimensionless` returns `(km/s)^2`.
The Newtonian ring force is multiplied/divided by that same a0 conversion
when compared to the grid.

The bottom flux is
`2pi*G*10^6/a0 integral R Sigma dR = G*M_annulus/a0` in the cylindrical
convention with the common azimuthal `2pi` omitted. This matches the
upper-half-space sheet jump and the upper monopole flux; there is no
extra full-space factor of two. The source mass check reconstructs this
same normalization explicitly.

## Numerical experiment and scoring

The four H I/H2 endpoint alternatives and all profile measurements are
fixed from baryonic information. The nonlinear equation receives their
total density, not separately transformed component speeds. The adopted
response parameters retain their prior calibration and are not fitted to
this galaxy. Thin coplanar geometry, differing observational reductions,
sharp-edge singularities and unvaried conversion/systematic uncertainties
remain genuine declared limitations.

The grids `N=256,L=255` and `N=320,L=1023` have the same logarithmic spacing:
`log(256)/256=log(1024)/320=log(2)/32`; their inner edges consequently
coincide up to floating-point evaluation. The `N=512,L=255` grid halves
that spacing. Domain and refinement comparisons therefore address distinct
numerical effects at the specified observed radii.

The outer Dirichlet potential is an approximate isolated monopole of the
same total mass. It is not an exact disk boundary. The prospective domain
enlargement comparison is needed and has not been pre-declared successful.
Source mass beyond the grid is reported separately. Newtonian grid versus
ring-oracle comparison also includes the grid's approximate boundary error;
it is not a pure discretization test with exact ring-derived boundaries.

The final source compares each Newtonian result at the five fixed oracle
radii, with signed forces and matching units. It retains the oracle's
successive-height and quadrature differences in the predeclared practical
allowance. That allowance is neither a rigorous uncertainty interval nor
an observational-fit threshold. Source/table values are not altered by it.

All 43 observed rows remain in the result. A negative predicted squared
speed is retained with no fabricated real circular speed. Summaries count
such omissions explicitly, and an entirely empty real-speed subset now
produces null summary values rather than an exception that loses the case.
The nominal error-weighted residual is explicitly descriptive: it does
not incorporate the missing covariance and geometry/conversion systematics.

## Freeze and qualification identity

The galaxy freeze is
`dcb22692af4397c08c8dfb15dc17cddebc1a3e377a02f8b48695197e075c2ef9`.
All 29 named entries match current bytes, including the exact 13 solver
qualification receipts. The runner names the full expected case set and
checks each `(N,extent,eta,newtonian)` tuple, canonical payload, source
freeze, recomputed radial error and refinement relation. It no longer
treats an arbitrary count of thirteen files as qualification.

The ring-oracle result is linked to its source freeze, complete status and
all passed checks before use. That freeze's eleven named source entries
also match current bytes. The physical density helper was already frozen
through that oracle and was not edited during this review.

These hashes establish byte linkage and version identity, not independently
the validity of astronomical observations or the gravitational model.

## Checkpoint and resume scope

After each completed Picard update the real callback stores the field and
history, their hashes, shape, float64 dtype, exact case identity and source
freeze. It flushes a temporary NPZ before atomically replacing only the
same calculation's rolling checkpoint. Loading disables pickle and checks
the stated identities, hashes, dimensions, dtype and field finiteness.
The solver copies histories, requires sequential completed outer indices,
counts resumed updates within the same 300-update allowance and recomputes
convergence on the supplied field.

The separately frozen smoke test used this actual writer/reader, stopped
after five complete updates and resumed. Its authenticated result passes
all seven checks: both routes converge in seventeen total updates and
their maximum field difference is exactly zero. Wrong-case and wrong-freeze
loads were rejected. Result SHA-256:
`70d2d90da642f7f70cdbbc4d21e747f4cca8cf8abe89e21f6207d9fcf4ca5ca8`.
The smoke freeze and all eight source entries still match current bytes.

This qualifies that completed-iteration continuation, not arbitrary
filesystem power-loss recovery or an in-progress PCG checkpoint. An
interrupted inner solve may be repeated from its last completed outer
state. Existing completed/failure results remain exclusive, not overwritten.

## Runtime expectation

The `L=1023,N=320` grid has 1.5625 times the cells and roughly eight times
the maximum cell aspect ratio of the qualified `L=128,N=256` case. The
diagonal-preconditioned solve may therefore be significantly more expensive
or hit its numerical allowance. A precise duration or iteration count
cannot be derived from source inspection. Such a failure would require
numerical diagnosis with the same source/law, not a changed physical
prediction. The rolling outer-state checkpoints are appropriate here.

The preflight establishes readiness of this conditional development test.
Its physical and numerical outcome remains to be read from the completed
galaxy results, not inferred from the qualification or checkpoint tests.
