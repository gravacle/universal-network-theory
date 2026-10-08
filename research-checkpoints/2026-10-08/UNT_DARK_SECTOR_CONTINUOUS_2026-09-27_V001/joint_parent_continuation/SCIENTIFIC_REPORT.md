# From a network-response mechanism to galaxy and expansion tests

2026-09-28. Additive continuation after Frontier V031. This report separates
the specified mechanical/covariant candidate from its still-developing native
record construction. Original sources, failures, and result packets remain.

## What the calculation is testing

The question is whether ordinary matter, acting through a network-derived
gravitational response, can explain the behavior otherwise attributed to
additional dark matter and dark energy. No dark halo is added to these galaxy
calculations. The current candidate is a positive classical mechanical model
with an explicitly adopted soft-mode distribution and saturated source map;
its complete derivation from the native UNT record Hamiltonian is not assumed.

The same response is tested in two roles. Its derivative sets the stationary
galaxy field; its energy integral sets a cosmological stress once an absolute
energy-reference condition and covariant coupling are supplied. This makes
the joint construction more restrictive than independently choosing a galaxy
interpolation and a cosmological pressure function.

## 1. An actual disk calculation, not a spherical shortcut

The NGC3198 calculation solves the nonlinear axisymmetric field equation with
measured stellar and gas profiles. The source has the same ordinary matter
in its Newtonian control and its conditional network-response calculation.
There is no velocity fit in the frozen experiment. NGC3198 is exposed
development data, not a held-out prediction; the acceleration scale and the
second scale's cosmic reference were already calibrated in the preceding work.

The numerical method was tested against exact nonspherical Kuzmin solutions,
then against an independently implemented Newtonian ring integral for the
actual source. A failed large-domain solver attempt was preserved and repaired
by changing only the iterative linear solver, not the physical law or accuracy
requirements. Completed cases and authenticated iteration checkpoints support
restart; an actual stopped/resumed small solve reproduced the uninterrupted
field exactly.

Four original source variants retain or truncate the measured endpoint
continuations of HI and H2. Each receives coarse, remote-boundary, fine-grid,
and same-source Newtonian calculations. All 43 observed radii are retained.
The endpoint choices alter total mass by less than one percent, so this is
a specific tail-sensitivity test, not the complete observational error budget.

All 16 original cases completed and passed their numerical checks. Across
the four source variants, velocity RMS residuals beyond 2 kpc are
63.40–63.57 km/s for ordinary-matter Newtonian gravity and 11.04–11.22 km/s
for the candidate. The HI1/H21 reference gives 63.43 versus 11.14 km/s.
Its maximum fine-grid force change is 0.423%, and its remote-boundary
change is 0.00984%; all five independent Newtonian force checks pass.
The complete four-variant synthesis and custody review are in
`GALAXY_FIELD_RESULTS_REVIEW.md`.

![All four prescribed source variants, all 43 radii](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NGC3198_FIXED_SOURCE_COMPARISON.png>)

The figure's narrow variant spans are not confidence intervals. All-radius
RMS is 13.10–13.23 km/s for the candidate; the unresolved inner region is
visible rather than removed. The source comparison does not conceal that
the outer curve rises above the measured velocities.

The improvement addresses the missing gravitational support directly. The
remaining intermediate-radius shortfall, central excess and outer excess are residuals of the candidate,
not additional evidence merely because they have a particular sign. Their
radial structure tells us which source and response assumptions to examine.
This is not a fitted-dark-halo comparison or a statistical model-selection
claim. The quoted measurement errors omit important source/geometry systematics
and covariance; nominal sums of squared error units are not full likelihoods.

## 2. Identify the source of the remaining mismatch

`DISK_RESPONSE_DIAGNOSTIC.md` defines a no-refit decomposition of the saved
fields into the response's departure from its deep asymptote, vertical-field
projection, Newtonian disk-versus-monopole geometry, and the remaining nonlocal
field/boundary contribution. Signed velocity-squared terms add back exactly
to each residual. This is a defined diagnostic partition, not a unique causal
decomposition; it retains hard-edge warnings and numerical shifts. The
completed postprocessing covers all four models and 172 rows; all 700
bookkeeping/consistency checks passed.

At 44.08 kpc in the HI1/H21 reference, the ideal far-field flat speed is
149.61 km/s, compared with 149 km/s observed there, but the actual disk
calculation gives 168.69 km/s. In the specified velocity-squared partition,
the disk-versus-total-mass-monopole term is +3411.98 (km/s)^2, the law-shape
term is +1679.23, the remaining field term +1116.73, and vertical projection
-135.09; the flat-reference residual contributes +183.28. Their sum is the
actual +6256.13 residual. The largest term in this partition is therefore
finite-radius source geometry, not a wrong total-mass flat asymptote alone.
This identifies a useful source/geometry investigation; the asymptotic
coincidence does not replace the real disk prediction or validate it.

An independent photometric audit found that two published mass-to-light labels
of 0.5 are not equivalent. Leroy's K-band conversion corresponds to effective
3.6-micron M/L 0.39784, while the comparison SPARC convention uses 0.5 in that
band. The fixed conversion changes stellar density by a factor 1.2567828155.
It explains most of the difference between their 3–8 kpc annular stellar masses,
but not every local profile difference. It was not applied to the original four
models, nor inferred by optimizing their velocity residuals.

The separately specified source-calibration test is now complete: four further
qualified cases change only that conversion, keeping law, distance, gas, radii
and geometry unchanged. Its fine-grid network RMS beyond 2 kpc improves from
11.14382 to 9.57703 km/s, compared with 57.01660 km/s for its own increased-mass
Newtonian control. The all-radius network RMS worsens from 13.17366 to 13.78953,
and the R>=8 RMS worsens from 10.34278 to 12.16396. At 44.08 kpc the prediction
rises from 168.69241 to 172.79223 km/s, against 149 observed. All outcomes remain;
the true stellar conversion has not been inferred from this comparison.

Raising stellar mass raises the ideal far-field flat speed by about 3.1%;
the solved finite-disk result confirms that this particular source substitution
improves much of the 2–20 kpc curve but is not the solution to the outer excess.
It supplies no license to combine component-wise nonlinear force rescalings.
The complete source-specific results and the recombined independent Newtonian
oracle are in `STELLAR_CALIBRATION_RESULTS.json` and its case files.

The same four illustrative radii used in the original disk decomposition
show both directions of change; all 43 rows remain in the numerical result:

| Radius (kpc) | Observed (km/s) | Original response | Fixed stellar-convention substitution |
|---:|---:|---:|---:|
| 5.78 | 137 | 125.67 | 136.05 |
| 12.05 | 156 | 146.09 | 156.00 |
| 24.03 | 150 | 150.76 | 157.67 |
| 44.08 | 149 | 168.69 | 172.79 |

Distance has a useful exact constraint: with the complete angular source and
all physical lengths scaled consistently, this field equation gives
`v_D(theta)=sqrt(D/D0)*v_0(theta)`. Distance alone changes the amplitude, not
the shape. A separate, explicitly in-sample diagnostic is reported below;
none of the frozen field calculations uses its fitted distance.

The modern HALOGAS column-density map has now been independently decoded and
qualified as a source-only fixed-plane contrast. Its companion moment-zero
map verifies the historical column conversion to 2.31e-7 relative precision;
the column image's stale brightness-unit header is not applied a second time.
Both 4x4 and 8x8 pixel partitions, 40-arcsec and 120-arcsec annuli, both
geometric halves, all signed emission and all zero/missing-area categories
are retained. All 63 extraction checks pass. No rotation values enter this
extraction, and no new force prediction is implied by it.

The map's retained H I falls faster in the outer disk than the old adopted
profile. Its geometry-selected complete annuli extend through 136.48475 kpc
and contain 1.023059e10 solar masses of bare retained H I, versus 1.112805e10
in the old source over the same extent. Another 0.19384% of the map's retained
mass lies outside this complete prefix, including far-map emission that
must not simply be assigned to an enormous NGC3198 disk. Those pixels remain
in the output ledger rather than being discarded from the evidence.

![Source-only old and modern hydrogen comparison](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/halogas_source_candidate/OLD_MODERN_HI_COMPARISON.png>)

This is a declared 72-degree, 215-degree fixed-plane reconstruction, not
the published warped-ring model. Mask replacement matters: for example,
about 44% of the finite sky area in the 40.14–48.17 kpc coarse annulus is
zero/replaced. Its retained mean 0.07916 solar masses/pc² is not a precise
measurement that omitted gas is absent. Both resolution products and their
limitations must accompany any subsequent mass-conservative source
substitution. No new gas-tail shape or velocity-selected aperture is fitted.

The two source substitutions are now complete. Each uses a continuous,
nonnegative, exactly bin-mass-preserving profile and the same fixed calibrated
stars and molecular gas. Both include the geometry-selected complete prefix;
neither is chosen for its rotation residual. Eight new field/control cases,
438 source checks, 170 independent ring checks and 62 field checks pass.
All 344 observed-radius rows remain, with no negative-force row omitted.

| Source at fixed 13.8 Mpc | Network RMS, all 43 radii | Network RMS, R>=2 kpc | Same-source Newtonian RMS, R>=2 kpc | Predicted speed at 44.08 kpc |
|---|---:|---:|---:|---:|
| Calibrated old gas | 13.79 | 9.58 | 57.02 | 172.79 |
| Modern retained H I, 40 arcsec | 14.41 | 10.56 | 56.80 | 166.43 |
| Modern retained H I, 120 arcsec | 14.36 | 10.46 | 56.77 | 165.70 |

All speeds and RMS residuals in this table are km/s. The final observed speed
is 149 km/s. The modern source lowers that particular excess by 6.36–7.10 km/s,
but modestly worsens the aggregate curve residuals. These are distinct
outcomes, both retained. Maximum fine/coarse force changes are 0.709% and
0.438%; remote-domain changes are below 0.009%. Their independent Newtonian
ring discrepancies are 0.145% and 0.051%. Thus this source substitution has a
resolved mixed effect, rather than completing the radial explanation.

![Same-law gas-source contrasts and same-source Newtonian controls](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NGC3198_HI_SOURCE_CONTRAST.png>)

`HALOGAS_FIELD_RESULTS_REVIEW.md` independently authenticates and reconstructs
the complete saved-data comparison. The two representations are source
sensitivity tests, not an uncertainty band, and their planar gas source is
not a joint reconstruction of the modern warped gas and velocity tracer.

`DISTANCE_ONLY_DIAGNOSTIC.json` then exposes the exact one-amplitude fit for
all seven completed source choices, using all 43 rows, equal and quoted-error
inverse-variance weights, and both positive-distance and 12.3–15.3 Mpc bounds.
For the modern 40/120-arcsec sources, equal weights give 12.3506/12.3342 Mpc;
quoted-error weights give 12.7962/12.7555 Mpc. The bounded solutions coincide
with the unbounded ones. The equal-weight all-radius RMS improves to
12.3610/12.2422 km/s, while the final predictions remain 157.447/156.649 km/s.
Distance helps the amplitude but cannot repair shape. These are exposed-data
fits, not new predictions, a determination of the true distance, or full
likelihoods: source/geometry covariance remains unmodeled. Changing distance
scales all physical lengths together; it leaves angular surface densities
fixed, not the three-dimensional volume density.
An amplitude-independent illustration makes the remaining target explicit:
the predicted outer/middle speed ratio, using the rows at original radii
44.08 and 12.05 kpc, is 1.06962/1.07121 for the two modern representations,
versus the observed 0.95513. No common distance multiplier changes that ratio.
`DISTANCE_ONLY_DIAGNOSTIC_REVIEW.md` independently checks all 28 fits and the
complete summary/figure census.

## 3. A stronger joint dark-energy consequence

`FULL_RESPONSE_PRESSURE.md` and its independent review derive an exact result
for the same candidate response in the explicitly adopted preferred-foliation
action. Write `Y=A_mu A^mu`, `J_Y=mu(sqrt(Y))-1`, and impose the existing
high-field reference condition `J(infinity)=0`. Then

    J(Y) = integral_Y^infinity [1-mu(sqrt(y))] dy > 0.

For a finite regular proper-volume slice with zero intrinsic boundary flux,
let `j=<J>` and `u=<Y(1-mu)>`. Its complete normal energy and pressure trace are

    rho_bar = M²(j+2u),
    p_bar   = -M²(j+2u/3),
    rho_bar+3p_bar = -2M²j < 0.

The particular bounded mechanical source additionally implies `J>Y(1-mu)`
pointwise, giving the stronger result

    -1 <= p_bar/rho_bar < -5/9.

Thus the same response that supplies extra galactic pull has an accelerating-sign
complete stress, without an independently fitted `w(a)` function. Two independent
analytical reviews agree. The upper endpoint is a controlled high-field limit,
not an inferred cosmological equation of state. The stress can be anisotropic;
the pressure here is one-third of its spatial trace.

The absolute reference is essential. Galaxy forces fix the derivative of J,
not its additive constant; `J+C` changes the cosmological conclusion while
leaving those forces unchanged. The previous two-scale reference solve also
used a cosmological input, so its amplitude is not a new independent prediction.
An arbitrary finite galaxy box has a boundary term and does not obey the
zero-flux cosmological average automatically. A stress inequality is not a
solution of the averaged Einstein equations: matter, shear, lapse, curvature
and their correlations must remain in an actual expansion calculation.

The actual homogeneous K=0 background and its linear scalar equations were
also derived in `K0_FLRW_SCALAR_DECISION.md`. The aligned background contributes
the matched constant; weak vacuum-subtracted disturbances have radiationlike
trace pressure, not a new positive homogeneous dust component. The nonzero-k
de Sitter scalar has positive quadratic kinetic energy at the specified sign,
but no quadratic restoring term. This does not establish arbitrary-background
or uniform zero-wavenumber stability.

An explicit extension now keeps the SAME positive-inertia response coordinates
instead of eliminating them before the cosmological calculation.
`EXPLICIT_MODE_COSMOLOGY_PATHWAY.md` specifies a covariant action whose static
elimination returns exactly the frozen J(Y), without adding another contact
or a fitted cosmological fluid. On its aligned homogeneous branch the physical
mode coordinates obey

    m(q_ddot+3H*q_dot)+kappa*delta²*q+u4*|q|²*q=0.

Varying the lapse and spatial scale gives their energy and pressure directly.
Rapid quadratic-dominated excitations redshift as a^-3, while quartic-dominated
ones redshift as a^-4. The inherited matched vacuum contribution remains in
the same action. This is a concrete way for the same network-response
coordinates to have both a static gravitational role and a cosmological
energy-carrying role; it is not an additional empirical prediction of their
abundance. Exactly unexcited homogeneous classical modes stay unexcited.
Their physical inertias, prepared energy, production history and coupled
metric/clock stability must come from native matching. Assigning an arbitrary
excitation amplitude to reproduce missing cosmic matter would not close that
requirement, and previously counted energy cannot be counted again.

The first coupled metric/clock consistency test is also now explicit.
`FINITE_MODE_CONSTRAINED_RESPONSE.md` retains lapse and shift constraints for
a finite positive set of those modes. Its N-1 internal longitudinal
frequencies are positive and interlace the individual mode frequencies;
the remaining static polarization is conserved. On the actual unexcited
de Sitter branch, internal modes and physical normal tilt decay. The signed
linear polarization density scales as a^-3 but has zero periodic mean, so
it must not be mistaken for a derived homogeneous dust abundance. Root's
independent ADM, determinant and physical-tilt check is recorded in
`FINITE_MODE_CONSTRAINED_RESPONSE_REVIEW.md`. This closes a specific
finite-band linear consistency question, not the zero-gap continuum,
excited-background or nonlinear stability questions.

## 4. What native records have established

The source-strength bridge now has an exact operator constraint. For the
ports-off BS incidence Hamiltonian, with `n_e=(1-Z_e)/2`,

    [n_e,[H,n_f]] = h_N delta_ef X_e.

It fixes the initial retarded response slope in the actual prepared state.
The specified linear incidence source has exactly zero explicit contact term;
physical strain/volume contact terms require an owned coupling. A positive
mechanical inertia cannot simply be assigned independently of this spectral
weight, state, and physical source normalization.

A fresh exact 16-dimensional native record-addition calculation passed 1,042
checks, including an independent Taylor propagator, full spectral projectors,
source work and switching work. The actual prepared state retains both lower
and upper bands. Lower-band record additions show binding curvature, while
upper-band curvature has the opposite sign. Copying off freezes the local
record counts but does not erase their effects on incidence and motion.
More records do not by themselves mean greater coherent incidence response.

`NATIVE_RECORD_PHASE_PATHWAY.md` resolves the actual writer-referenced probe.
For the already owned copy source `H=H_hold+delta_g*K`, `K=X_L+X_R`, its
exact short-delay susceptibility slope is
`4< (epsilon_r-lambda_R*n)(1-R) >/hbar^2`. It is -0.86738 in the saved native
formed state but +3.12598 in the blank-record control. Thus a short copying
pulse has an explicitly predicted opposite response sign in those states,
even while the held record-count self-response vanishes. All adjacent-count
transition lines and the full nonstationary two-time kernel are specified;
the smallest coupled gap is 0.55502 in the inherited units. A separate neutral
endpoint-relative phase is retained, not confused with a zero-frequency
copying pole. This active prepared response cannot be replaced by a passive
ground-state susceptibility without changing the question.

The direct small writer-pulse test is complete: all 240 prescribed pulses
and 1,631 numerical checks pass, with the predicted signs in all 15
preparation/age states. Spectral evolution, independent Taylor evolution,
the full nonstationary Kubo response and source-work accounting agree.
The largest switching-work discrepancy is 7.02e-15 in the inherited units.
In the native preparation, record count remains 1.31434 during hold, yet
the same short positive pulse changes that count by +7.49922e-5 at age zero
and -6.73927e-5 at age two. The response therefore depends on retained phase
and age beyond the count. The feedback-off formed control also has this
qualitative behavior: it is not uniquely caused by incidence feedback.
These are predictions verified inside the specified native model, not an
experimental gravity measurement or a proof of global information loss.
See `NATIVE_WRITER_PULSE_RESULT.md` and its complete saved evidence.

The native volume-increment analysis derived exact blank-node addition work,
including the change of all old `Omega/N` incidence couplings. It also proved
that the specified blank positive-bias ground branch has only O(1) occupied
links at large N, so it cannot silently serve as an already formed connected
macroscopic geometry. The actual formation state remains the relevant target.

Node-count energy alone cannot fix physical pressure. Along a proposed
`V=2N*v_cell` path, insertion work combines chemical and volume work. Distinct
off-path source couplings can agree on all those energies and yield different
pressure. The constructive next ingredient is an explicit autonomous creation
and physical-volume/source coupling, with its work ledger, rather than a new
name for a fitted cosmological constant. Constant-rate node creation would
not by itself accelerate a scale factor proportional to `N^(1/3)`.

## 5. The linked light-bending test

`WEAK_FIELD_LENSING_PATHWAY.md` derives the stationary weak-field metric of
the adopted action, with minimal coupling of ordinary matter and an aligned
clock. Its two leading metric potentials are equal: the same potential that
sets stellar motion sets light deflection. There is no separately selectable
lensing enhancement. In the ideal isolated deep-field limit this predicts
physical bending `2*pi*v_flat²/c²`, tied to the same flat-speed normalization.
Environmental and cosmological matching remain explicit assumptions, and
an observed reduced angle also requires actual lens/source distances.

The first saved-field postprocessor retained all 20 original/calibrated field
cases and all 300 specified rays; its preset census does not include the two
new modern-gas sources. Its result is preserved as
`SAVED_POTENTIAL_LENSING_RESULTS.json`, with status
`FAILED_NUMERICAL_CONTROLS`: five central Newtonian projected-mass checks missed
the unchanged 1% target by producing 5.00–5.52% discrepancies. The other 7,640
checks passed. No angle in this version is promoted as a fully qualified
lensing prediction. No observed lensing data were fitted or tested.

Independent diagnosis isolates the error to the linearly interpolated
subtracted spherical reference. For the original HI1/H21 source at 2.7 kpc,
direct projection of the full saved field is -0.220% from the exact Newtonian
projected-mass identity; the reference-interpolation defect adds +5.739%,
yielding the recorded +5.518%. The additive repair improves the
radial interpolation of the same saved potential. It changes no field solve,
physical parameter, source, ray census, exterior assumption or acceptance
threshold. The original failure remains.

The separately frozen V002 repair has now completed and passed: all 246
synthetic interpolation/integration controls and 2,245 newly computed
real-field checks pass, alongside 5,400 explicitly reused unchanged spherical
checks. All 20 cases and 300 rays remain. The worst of 25 Newtonian
projected-mass discrepancies is now 0.02866%, well within the original 1%
target. Maximum candidate mesh and domain changes are 0.00809% and 0.15171%.
This qualifies the specified saved-field reconstruction; it does not turn
the adopted isolated exterior or metric/clock completion into measured facts.

Across the complete case/ray set, candidate physical bending magnitudes are
0.12234–0.37145 arcsec and ordinary-matter Newtonian magnitudes are
0.02644–0.13953 arcsec. The 75 matched fine-field candidate/Newtonian ratios
range from 2.169 to 12.435. For example, the fixed stellar-calibration source
at impact 43.7 kpc gives 0.34514 arcsec face-on, 0.37143 along the 72-degree
major axis and 0.35211 along its minor axis; its same-source Newtonian values
are 0.03174, 0.03565 and 0.03028. These are physical bending predictions,
not measured reduced angles or fits to observed lensing. No extra halo or
independent lensing-strength parameter was supplied. The numerical audit is
`SAVED_POTENTIAL_LENSING_V002_RESULTS_REVIEW.md`; all source variants, signed
components, exterior contributions and failed V001 evidence are preserved.

## 6. Scientific path forward

The new `SOFT_SPECTRUM_ROTATION_SELECTOR.md` gives a precise native target.
Within the stated elastic parent, a soft-mode density `nu(delta)~delta^alpha`
with -1<alpha<3 produces force exponent `(alpha+3)/2` and isolated far-field
speed `v~r^[(alpha-1)/(2(alpha+3))]`. Flat rotation therefore selects alpha=1:
a constant weighted density of small positive stiffness eigenvalues. The
coefficient and exponent have been independently derived. This does not
identify physical space with a two-dimensional internal mode count. Native
source overlaps, contact, quartic stabilization and prepared-state dynamics
must produce the spectrum together; an eigenvalue histogram alone is not enough.

`FINITE_TIME_SOFT_RESPONSE_PATHWAY.md` makes the static-to-dynamic bridge
more constructive. The dominant modes occupy a source-dependent finite band;
their excluded relaxed force has an explicit positive bound. Their positive
inertias generate a calculable conservative source inertia, logarithmic in
the scale separation for the flat-curve spectrum. A sufficiently smooth
common-source ramp can prepare a finite positive-gap classical band near its
minimum without adding damping. The resulting force window requires both
the appropriate weighted spectrum and a measured source/state/time history.
An abrupt step instead has a derived oscillatory linear response at fixed
finite time; merely running longer is not equivalent to preparing the static
branch. These are properties of the same conditional mechanical parent,
not yet a measurement of the native network's physical clock or inertia.

The additive `RESPONSE_HISTORY_RADIAL_TEST_V001.md` now sharpens that path.
For one monotone, fixed-direction source ramp from zero mechanical excitation,
the exact subsequent clamped-force error obeys
`|D_actual-D_relaxed| <= G/[1+(G/g_s)^2]^2` at every hold age. Its high-field
ceiling falls as `G^-3`; with constant mode inertia the dominant low-field
response time instead grows as `G^-1/2`. These provide a common-history test,
not a different adjustable age at each galactic radius. A proved early
positive-response window and an explicit later negative-response example
show that the desired lag sign must be predicted, not assumed. This local
constitutive calculation has been independently reviewed; the coupled
metric/clock constraints are still required before using it in a galaxy.
No new finite-age galaxy fit or propagation was performed.

The stellar-calibration comparison, modern outer-HI extraction and both
mass-conservative source substitutions are complete. Their source/tracer
geometry and omitted-signal assumptions remain visible. The distance-only
diagnostic is also complete and leaves a radial-shape target.
The linked stationary lensing forward prediction is numerically qualified
within its declared reconstruction and exterior assumptions; comparison
against actual lensing observations remains a separate task.
Use these results to choose a source-consistent
held-out galaxy test, retaining the common law rather than adjusting a function
for each galaxy. In parallel construct the native phase/current and volume
coupling needed by the covariant equations. Then test expansion, structure and
lensing with that same construction and explicit initial data.

The external **DDO 154** transfer is now complete under
`external_ddo154_v001/SCIENTIFIC_RESULT.md`. All eight fixed-source field jobs
pass. With no local halo or velocity fit, the unchanged law reduces all-row
RMS to 4.7793/4.6921 km/s, versus 22.5159/22.5533 km/s for its own baryonic
Newtonian controls. All 12 valid primary SPARC samples are retained, and
mesh/domain tests also pass at every scored radius. Inner/middle residuals
are small, but the final four points remain systematically high; at the last
point the candidate predicts 56.1125/55.8303 km/s versus 45.5 observed, equivalent
to 52.09%/50.56% excess acceleration. No parameter was optimized against these
data. The full visually checked curve and all original evidence are retained.

This is an explicitly cross-product comparison: fixed-plane original THINGS
gas plus Leroy stellar sources versus the separately compiled SPARC rotation
data, with fixed distance-only radius conversion and no inclination fit.
The original THINGS sampled-curve endpoint remains unverified; that modern
kinematic cross-check and matched warped geometry remain useful next inputs.
H2 omission, retained-mask/exterior flux, stellar-tail and catalogue-aperture
inconsistency, pressure treatment and covariance are explicit limitations,
not fitted corrections. The two sources agree closely but are not independent
observations. Public kinematic summaries were exposed before scoring, so this
is an out-of-program prospective transfer, not a blind test.

The current NGC 3198 residual-size audit is saved in
`RESIDUAL_SIZE_AND_TRANSFER_GATE_V001.md`: all 43 rows give 14.36–14.41 km/s
RMS, about 9.8% of the median observed speed; the supplemental R >= 2 kpc
summary gives 10.46–10.56 km/s, about 7.1%. Its same-source Newtonian
R >= 2 kpc mismatch is 56.77–56.80 km/s. At 44.08 kpc the remaining speed
excess is 16.70–17.43 km/s, corresponding to 23.67–24.76% excess acceleration.
The coherent outer excess is substantially larger than measured mesh/domain
changes. These descriptive comparisons do not supply an observational
covariance or a fit significance.

The current constructive conclusion is specific: a shared mechanical response
can replace most of this galaxy's baryon-only missing support and constrain an
accelerating-sign stress in the same conditional model. Completing the dark
program requires both native matching and broader independent observation;
one improved rotation curve is not the entire case.

## 7. Prepared response: a new theorem, not a chosen correction

The next continuation directly tests the recurring outer excess. The saved
point estimates do not identify one common onset acceleration: the terminal
positive-residual bracket is 0.393–0.474 a0 for NGC3198 and 0.138–0.146 a0
for DDO154. These are descriptive sign brackets, not transition confidence
intervals. All samples and both correlated source representations remain.
See `CROSS_GALAXY_ACCELERATION_DIAGNOSTIC_V001_REVIEW.md`.

The common-history test now propagates the full nonlinear mechanical modes
from rest under the same smooth ramp, with three amplitudes, two durations,
two matched finite cutoffs and numerical refinement. All 108 stored states
retain source work and excitation. Independent velocity-Verlet propagation
checks the RK4 result. Instantaneous forces ring and can change sign; a
selected favorable observing phase cannot define the correction.

The long-time orbit means are instead calculated from each mode's actual
deposited energy, without resetting or thermalizing it. All 36 mean cases
pass independent orbit-integral checks. The clean V003 output preserves the
V001/V002 serialization failures and reproduces every V002 scientific field.
The six main mean responses exceed their relaxed values.

`COMMON_HISTORY_MEAN_SCALING_V001.md` strengthens this numerical finding to
an exact theorem for the scalar clamped parent. Any nonnegative monotone
source ramp from rest confines the subsequent orbit to nonnegative coordinates.
The mean oscillator equation and Jensen's inequality then give
`mean(y)<=y_relaxed`, hence `D_mean>=D_relaxed`, strictly for retained excitation.
This is a mean-polarization result, not a statement about every instantaneous
force or every native active preparation.

More strongly, after the held infinite-time mean, any uniformly bounded-duration
such ramp has the SAME deep-continuum coefficient at constant positive inertia:

    C_prepared = 0.951821896774069,
    C_relaxed  = 3*pi/16 = 0.589048622548086,
    C_prepared/C_relaxed = 1.61586303802343.

The quadratic low-field response survives; its coefficient changes without
using galaxy data or selecting a per-radius age. A proved bound places this
ratio strictly between sqrt(2) and 5*sqrt(2)/4. Independent quadrature reproduces
the definite integral. The limits are essential: average first, then take a
soft-continuum window with delta_min/sqrt(H) tending to zero. Fixed finite
observation time still has the earlier linear response; a fixed nonzero lower
gap has a different strict weak-field limit. The theorem does not establish
that a galaxy reaches the mean or that its native response has this inertia.

The correct next physical link retains the energy as well as the mean force.
`PREPARED_STATE_FORCE_VOLUME_CONSEQUENCES_V001.md` shows exactly why integrating
this prepared-force curve cannot silently replace the previous vacuum matching:
across different preparations, `dE/dh=-P+sum(weight*omega*dI/dh)`. The actions I
change, and that term is compulsory. All original acceleration scales, the
matched constant and the galaxy fields remain unchanged. No saved disk speed
has been rescaled by the new coefficient.

## 8. Coupled gravity and cosmological closure

`COUPLED_SPHERICAL_RESPONSE_PATHWAY_V001.md` now gives an explicit 1+1
Hamiltonian retaining gravity, the preferred clock, radial modes and a conserved
ordinary-dust current. Its lapse variation includes both polarization-divergence
and acceleration terms. The same action also has an exact geodesic-clock,
unexcited GR-plus-matched-vacuum branch during nontrivial matter evolution.
An enhanced stationary branch therefore requires a physical preparation rule;
it does not follow from baryonic density alone.

`COSMOLOGY_CLOSURE_TEST_V001.md` derives the corresponding zero-charge growth
equation and a curvature-independent background invariant. Its 18-case
arithmetic retains the previously used cosmological reference and two expressly
conditional standard-BBN baryon estimates. The vacuum-plus-unexcited-baryon
branch does not recover that reference history. This is a conditional closure
test, not a new cosmological likelihood or an exclusion of every network theory.
It identifies the required formation/energy calculation instead of supplying
an adjustable mode abundance.

`FIXED_ACTION_MODE_INTERFACE_V001.md` derives a common state description:
the same orbit energy e(I,h) fixes mean response, frequency, action transport
and homogeneous pressure. It also supplies a required stationary momentum
balance, `sum(weight*I*radial_derivative(N*omega))=0` in the stated static
scalar setting. Independently averaged local forces alone do not meet this
condition. Coordinate-potential positivity also does not guarantee convex
phase energy; tilted soft modes can have a decreasing frequency with action.

The first shared-state energy/pressure calculation is complete. Every one of
the 36 saved end-ramp cases was continued by conserving its actual actions
during an ideal fixed-volume adiabatic return to zero source. All 3,840 modal
entries were independently checked. The six main preparations have positive
remaining energy and mean p/e between 0.000610 and 0.01722. The return extracts
some preparation work; the complete cycle work equals the energy retained.
No temperature, population or pressure was independently adjusted. These are
low-pressure outputs of a specified state map, not a sound-speed, clustering,
cosmic-abundance or finite-duration unloading result. See
`PREPARED_ACTION_RETURN_V001_REVIEW.md` for the complete census and ledger.

The constructive advance is now more specific than an outer-delay suggestion:
there is a proved conservative mean-response effect, a calculated universal
limiting coefficient, and coupled constraint/energy equations in which to test
it. Native source/clock/volume matching and formation-state selection still have
to connect these conditional results to actual galaxy and cosmic evolution.

## 9. A native record clock and its actual internal response

The saved native record state now supplies a qualified local phase readout.
For the preselected raising observable A=A_L+A_R, its amplitude is nonzero
and its phase advances on the whole inherited hold interval [0,2], not just
at selected samples. Both interpolation grids certify the sign under the
declared 1e-10 numerical allowance. At the finer grid the amplitude is at
least 0.9163300 and phase rate is bounded between 0.6699443 and 0.9724974;
the total phase advance is 1.7483062 radians. Record count remains conserved.
Feedback-off has an exactly unit-rate phase; copying-off has no phase signal.
All 518 worker checks and 279 independent checks pass. See
`NATIVE_PHASE_CLOCK_RESULT_V001.md` and `NATIVE_PHASE_CLOCK_V001_REVIEW.md`.

The same clock has then been used to express the original incidence-source
response internally, retaining the clock's own response. An incidence impulse
leaves A and its first derivative unchanged immediately; its clock shift begins
at quadratic delay. For a fixed integrated native-time impulse, the initial
response per phase increment is h*mean(Xa)/(hbar^2*phase_rate), with one clock
Jacobian. All 15 original state/age rows were checked, not newly prepared.
The native values range from 0.4427937 to 1.1714509: a changing clock alone
does not make this response a state-independent canonical source moment.
The higher-delay timing correction changes sign with the actual incidence
drift. All 284 production and 245 independent comparisons pass; see
`NATIVE_RELATIONAL_SLOPE_V001_REVIEW.md`.

These calculations make a concrete native temporal/source interface available.
They neither identify physical seconds nor replace the required spatially
consistent metric/volume map. The native cell and the conditional mechanical
parent remain distinct models until their source/state map is derived.

## 10. The same mechanical state fixes compression and late dilution

The returned-action calculation has now been extended to its compression
response, using every one of the 36 existing cases and all 3,840 modes. No
population, pressure, temperature or abundance was selected afresh. In the
already adopted common-current adiabatic closure,

    E=sum(weight*e(I)),  P=sum(weight*(I*omega-e)),
    c_ad^2 = sum(weight*I^2*e_II)/sum(weight*I*omega).

For the zero-source positive harmonic-plus-quartic potential, exact period
integrals prove e_II>0 and the stronger bounds

    0 < c_ad^2 < 1/3,
    c_ad^2 <= 2P/(E+P).

Low excitation pressure thus limits this compression response rather than
leaving a second free parameter. The six main numerical coefficients are
0.00112250, 0.00420787, 0.01441826 (duration 8) and 0.00321947, 0.01084569,
0.02999434 (duration 16), in ascending source-amplitude order. Independent
midpoint quadrature and complex-step differentiation reproduce all modal
and mixture results with maximum scaled discrepancy 2.00e-15. See
`PREPARED_ACTION_COMPRESSION_DERIVATION_V001.md` and
`PREPARED_COMPRESSION_V001_REVIEW.md`.

There is also an exact asymptotic route to matter-like dilution under this
same state law. With finite positive gaps, fixed coefficients and a valid
common adiabatic expansion, set q=(a_ref/a)^3 and retain I_j(q)=q I_j0. In
the inherited unit-inertia potential,

    e_j(I)=delta_j*I+3I^2/(8delta_j^2)+O(I^3),
    M=sum(weight*delta*I0),  B=sum(weight*3I0^2/(8delta^2)),
    E(q)=M q+B q^2+O(q^3),
    P(q)=B q^2+O(q^3),
    c_ad^2(q)=(2B/M)q+O(q^2).

Thus the same excitation approaches a^-3 energy dilution and decreasing
compression response; the fixed vacuum baseline is unchanged. The derivation
does not assume a fresh cold population. Its finite-gap and adiabatic conditions
are essential: it is not a result for an unqualified zero-gap limit or a
prediction of the actual cosmic initial actions.

This is a thermodynamic coefficient of the stipulated scalar common-current
closure, not yet a native spatial propagation speed or successful structure
formation. If directly identified with a physical c_s^2/c^2, the current six
values would imply speeds of roughly 0.034–0.173 c; they cannot be described
as cosmologically cold merely because they are below 1/3. The conditional
cooling law supplies a route to test, not an independently adjusted sound speed.

## 11. Exact native mechanics, rather than a fitted constant inertia

The measured state dependence now has a constructive native description.
`NATIVE_CANONICAL_INCIDENCE_CLOSURE_V001.md` derives the exact compact
spin-phase Hamiltonian of each conserved record-count/carrier-X sector of
the owned held single-link cell. With its actual conditional Bloch radius r,

    m=(1-mean(Z))/2,  Q=sqrt(r^2-(1-2m)^2),  p=hbar*theta,
    H_sector=3+R+(x-f)*m-h*Q*cos(p/hbar),
    H_sector,pp=h*mean(X)/hbar^2.

Its canonical equations reproduce the full conditional density-matrix
expectation dynamics for every prescribed existing incidence source f(t).
The changing source moment is thus the curvature of the already owned
Hamiltonian, not a constant mass chosen to fit selected ages. Mixed conditional
states, weights, chart poles and complete source work are retained. In the
weighted total action the canonical momentum is P_j=w_j*p_j; omitting this
normalization would give the wrong response strength. The lower and upper
stationary spin orientations both have the exact elliptic precession frequency,
so negative momentum curvature alone is not an instability diagnosis.

This analytical closure received two independent algebraic checks without
another numerical simulation. It is exact for the specified incidence channel,
not an independent-spin approximation to a general multi-link network. The
record clock still needs its coherent off-diagonal sector matrices; the link
azimuth is not silently substituted for the measured record phase. The original
diagnostic second source contact remains zero. Physical strain/volume matching
and a justified many-link or continuum limit remain separate derivations.
