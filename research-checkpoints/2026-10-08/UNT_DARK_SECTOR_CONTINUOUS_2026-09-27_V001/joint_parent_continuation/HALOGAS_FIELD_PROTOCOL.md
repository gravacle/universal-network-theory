# Two retained-H I source contrasts V001

Prospective implementation; no new force result was used in these choices.
The original NGC3198 cases, completed fixed stellar-calibration comparison,
HALOGAS map and radial extraction have already been viewed. This is explicitly
a post-exposure, independently sourced **source-sensitivity experiment**, not
a blind galaxy prediction or a fit. All inherited files remain unchanged.

## Source identities and the one changed component

Carry both identities, with no choice based on velocities:

- `HALOGAS40_ML36_RETAINED_V001`: 8x8 extraction, 40-arcsec annuli.
- `HALOGAS120_ML36_RETAINED_V001`: 8x8 extraction, 120-arcsec annuli.

Use only the contiguous conservative-complete prefix of each frozen profile:
51 and 17 bins respectively, ending at the same 136.4847475059566-kpc edge.
These are geometry-defined support choices, not a surface-density threshold,
velocity cut, detected-edge inference, or identification of all retained
emission as belonging to NGC3198. Preserve the full/included/excluded signed
bare-H I ledger, included negative-pixel contribution, and zero-retention bins.
Do not divide by footprint coverage, clip negative pixels, fill discarded
mask regions, or redistribute excluded flux. A genuinely negative net input
bin is rejected by this nonnegative representation rather than repaired.

For each bin set `s=R^2`, `mean=M/(pi*1e6*Delta_s)`, endpoint controls
`d0=mean0`, `di=min(mean_(i-1),mean_i)`, `dN=0`, and middle control
`bi=3*mean_i-di-d_(i+1)`. With `t=(s-s_i)/Delta_s`, use

```
Sigma(t)=di*(1-t)^2 + 2*bi*t*(1-t) + d_(i+1)*t^2.
F(t)=di*(t-t^2+t^3/3)+bi*(t^2-2*t^3/3)+d_(i+1)*t^3/3.
integral R*Sigma(R)dR = Delta_s/2 * [F(t_b)-F(t_a)].
```

`halogas_density.py` exposes the same `sigma` and exact `integral` interface,
radial knots, and `tail=None`; it has no slope API. This C0 representation is
continuous, nonnegative, regular at the center and continuously zero at its
outer edge. It need not be C1 or monotone and can overshoot its bin mean by
up to a factor three. It adds a representation choice, not spatial resolution
or new observations. Zero-retention bins remain identically zero.

Multiply the entire included bare-H I representation by 1.36 exactly once.
The new component remains named `HI_He`. Use exactly the same full Leroy
stellar profile and H21 molecular profile as completed control
`ML36_CAL_HI1_H21_V001`. The stellar multiplier is read from the authenticated
photometric comparison and fixed at `1.2567828155112788`; apply it to both
core and entire stellar tail. H2 already contains its inherited helium
convention and is not multiplied again. The original distance, fixed plane,
constitutive curve, `a0`, and shape parameter remain unchanged.

The support convention sets this retained-emission contrast to zero outside
the complete aperture; it does not establish that true gas is absent there
or that masked gas is absent inside. See the frozen representation proposal
and `halogas_source_candidate/HALOGAS_SOURCE_TRACER_CONTEXT.md`. The latter
also records why retaining the same 43 inherited velocities is **not** a joint
HALOGAS source-plus-tracer/warp/thickness reconstruction. No new rotation
points or paper-fit targets are imported. Both modeled gas distributions
remain planar, despite the physical source's known geometric complications.

## Source qualification and independent ring oracle

After freeze, before any PDE, save both source qualifications. Verify every
input annular mass against the analytic integral (`1e-12*max(1,mass)`), and
independently integrate the degree-five polynomial `R*Sigma(R)` using three
Gauss points **in R**, for each full bin and its central three-quarter
subinterval, at the same tolerance. Check shared endpoints exactly, control
nonnegativity exactly, the `3*mean` bound at `1e-14*max(1,mean)`, exact zero
intervals, regular central derivative, and exterior zero. Check the complete
HI+He mass, full/included/excluded ledger, unchanged H2 and calibrated stars,
and shared 40/120 included mass at relative `1e-13`. Save all bin masses,
controls and independent quadratures, not just a pass flag.

Evaluate a **fresh** independent-of-FV Newtonian ring oracle for each source.
Reuse the immutable `galaxy_ring_oracle.field`, not its old source factory,
slope helper, or original `main`. The qualified AGM kernels and their original
analytic/direct-angular controls are inherited through authenticated results.
Use signed forces at the five inherited radii 2.7, 8.7, 20.7, 35.7, 43.7 kpc.
For each source/radius set `z0=min(0.2, nearest_knot_distance/4)` in kpc and
evaluate heights `z0,z0/2,z0/4`, with orders 48 and 96 at every height.
Each radius must be more than `1e-10` kpc from a density knot. Do not use the
piecewise-linear source slope routine with the Bernstein source.

Retain all component potentials, signed forces, quadrature/omitted masses,
force and potential tail bounds, both orders, and both extrapolations
`2*g(z/2)-g(z)`. Inherit without retuning: force and potential order difference
`<=1e-8*max(1,abs(order96))`; component mass closure relative `<=1e-9`;
extrapolation change `<=1e-3*max(1,abs(fine))`; and final-height omitted-tail
force bound `<=1e-10*max(1,abs(fine))`. These are numerical checks, not
observational gates. Publish all ten oracle cases before the field queue.

## Eight-case queue and genuine restart support

For each source in the stated 40 then 120 order run these same four jobs:

| N | domain extent (kpc) | equation |
|---:|---:|---|
| 256 | 255 | inherited nonlinear law |
| 320 | 1023 | inherited nonlinear law |
| 512 | 255 | inherited nonlinear law |
| 512 | 255 | Newtonian |

Use the immutable `axisymmetric_disk_v002` solver and its original mesh,
operator, spherical boundary quadrature and PCG criteria. No global functions
are replaced. The supplied source determines every exact annular bottom flux,
component mass, total mass, boundary monopole and smooth initial monopole.
No velocity-conditioned starting field, parameters or stopping rule is used.

Each case has a distinct source-prefixed name, checkpoint and result. Reuse
the authenticated checkpoint writer/loader from `galaxy_field_compute.py`.
Checkpoints save the actual field and completed iteration history after each
completed outer update, with case/freeze/field/history identities. On restart,
verify those identities and preserve the total 300-outer-iteration allowance;
the solver independently recomputes convergence. This is not a wall-clock
cutoff or a reset of completed work. Completed results are authenticated and
reused. Only the exact new case's rolling checkpoint is replaceable; completed
outputs use exclusive atomic publication. Any failed qualification/result is
preserved and stops this frozen attempt, with no tolerance fitting or overwrite.

Retain the full potential matrix, full radial-force array, exact masses,
complete history, signed force and signed velocity-squared values at all 43
observed radii. Negative force is retained, with undefined real circular speed
reported as null, not absolute-valued or silently removed. Summaries for
`R>=0,2,8 kpc` disclose any such exclusions and contain descriptive RMS, mean,
maximum residual and nominal squared quoted-error units; none is a pass gate.
Pair each row with the **completed calibrated** control at the same grid,
domain and equation, retaining signed force, v-squared and speed differences.
Do not substitute the earlier uncalibrated control or add a matched-solenoidal
decomposition in this queue.

Numerical gates are unchanged: relative annular-source mass error `<=1e-13`,
identity of qualified masses and unchanged stars/H2 at `1e-13`, nonlinear
residual `<=1e-9`, global flux error `<=2e-6`, no clipped faces, and convergence.
The remote-domain and N512 nonlinear cases each compare to the same source's
N256/L255 baseline, requiring `<2%` force change at inherited radii `R>=2`.
The N512 Newtonian result must match its own fresh ring oracle at all five
radii within

```
0.02*max(1,abs(reference)) + abs(fine_extrap-coarse_extrap)
                           + abs(last_height_order96-last_height_order48).
```

No case, representation or residual is selected for scientific favorability.

## Custody and execution boundary

`halogas_field_compute.py freeze` only validates existing inputs and publishes
the new specification; normal invocation verifies it before any new work.
The manifest includes both additive sources and this protocol, the fixed
source/tracer context and representation proposal, extraction result plus its
canonical seal/freeze and recursively authenticated raw-map/protocol/source
ancestors, photometric calibration provenance, all inherited physical and
numerical helpers, recursively linked numerical/source freezes and qualified
results, and all completed calibrated comparison cases. Original payloads and
case identities are authenticated in addition to file hashes. The extraction
result has fixed SHA-256
`44b359abbcae5c0c61b26d3adc515a716fd6d45795fcecff3004189814230b2c`.

New source qualification, oracle, each field case, and final eight-case index
are separately published with the new freeze and canonical payload hashes.
Numerical libraries are single-threaded. Root reviews, freezes and runs the
one-worker queue; merely importing these modules does not start a calculation.
No inherited frozen source, result or checkpoint is edited. This protocol
does not turn the adopted constitutive law into a native UNT derivation or
convert a source-only contrast into a full galaxy inference.
