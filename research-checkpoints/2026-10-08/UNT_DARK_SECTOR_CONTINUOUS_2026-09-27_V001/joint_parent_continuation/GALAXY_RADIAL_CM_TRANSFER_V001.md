# Published-concentration radial transfer, prospective V001

2026-10-04. Source and protocol only until root reads, freezes and releases.
This follow-up was selected before inspecting the radial V001 outcomes;
its published concentration input and scenarios were not chosen from those
outcomes. It is an exposed, conditional radial-prediction comparison, not
blind validation or a complete LCDM galaxy-formation test.

## Identical sample and inherited predictions

Authenticate the completed `GALAXY_RADIAL_TRANSFER_V001` result, freeze,
tests, all 100 case files, producer and inert halo helper. Also retain their
original SPARC result/freeze hashes. Use exactly the old 100-galaxy census,
94 eligible galaxies, six n<6 exclusions, saved row ordering and exact
inner/outer masks. Do not revise any row, source, distance, inclination,
mass-to-light ratio, force prediction, a0 or r. The 51 original calibration
galaxies remain excluded. Tied split radii remain labelled as before.

Reuse the saved baryonic, network, RAR, unconstrained NFW and ISO predictions
and metrics; never rerun their producers or fits. The full measured baryonic
profile is allowed for every model; only INNER velocities calibrate the new
halo. Quoted velocity errors are retained, not used as fit weights.

## One parameter and an explicit no-response mass convention

Adopt the z=0 NFW concentration relation from Dutton and Maccio (2014),
Eq. 8, for relaxed DMO haloes:

    log10 c = .905 - .101 log10(h M_DMO / (10^12 Msun)) + delta_c,
    h=.671, H0=67.1 km/s/Mpc, fb=.0490/.3175,
    r200_DMO = [G M_DMO/(100 H0^2)]^(1/3), rs=r200_DMO/c,
    m(x)=log(1+x)-x/(1+x),
    v_dark^2(R)=G (1-fb) M_DMO m(R/rs)/[R m(c)],
    v_model^2(R)=b2_saved(R)+v_dark^2(R).

Primary source: https://arxiv.org/html/1402.7073v2 (Table 1, sections 2--4).
The published scatter in log10 concentration is .11 dex. Three fixed
global scenarios are delta_c=0, -.11, +.11, always reported separately.
They are coherent sensitivity scenarios, not individual scatter draws,
probabilistic marginalization or confidence bounds; do not select their
best outcome per galaxy or overall.

The multiplication by (1-fb) is our explicit approximate DMO-to-dark-mass
mapping with no halo response to baryon rearrangement. M_DMO and r200_DMO
are NOT asserted to be the final galaxy's total-matter or dark-only
200-critical mass/radius. Missing baryons are not added as a hidden halo.
No contraction, feedback, abundance matching or baryon-retention model is
introduced. NFW is continued without truncation when R>r200_DMO, and those
rows are flagged. Fit-boundary cases and masses below the approximate
published lower range 10^10/h Msun are flagged, not removed.

Only an explicitly supplied catalogue total baryonic mass can produce a
nominal baryon-budget flag Mbar>fb M_DMO. No total mass is inferred from the
radial acceleration profile. The inherited cases do not supply such a
total, so their budget status is unassessed. This is not a new fit prior.

The only fitted local parameter is log10(M_DMO/Msun) in [8,15]. Include
M_DMO=0 as a separate baryon-only endpoint; never evaluate c(M) there.
Constants for units are G_SI=6.67430e-11, Msun=1.98847e30 kg and
kpc=3.085677581491367e19 m. H0 is converted to km/s/kpc before using the
radius formula with G in kpc (km/s)^2/Msun.

## Fixed numerical procedure and tests

Fit INNER equal-weight velocity SSE on 257 and 513 uniform log-mass grids.
Include the zero endpoint, both finite boundaries and lowest grid value;
refine every strict interior sampled minimum by 80 golden-section steps.
Ties use deterministic inner-loss-only candidate order: zero, lower,
upper, lowest grid, then refined minima in grid order. Retain the full
grids, candidates, both predictions and parameter/domain flags. The finer
grid is the declared representative, not chosen by outer accuracy.

Inherited controls: grid objective discrepancy/max(1,Jfine)<=1e-6;
maximum outer prediction discrepancy/max(1,max|vfine_outer|)<=1e-5;
saved row acceleration/residual identities 1e-12; independent scalar
profile prediction 1e-10 scaled. Disagreement is UNRESOLVED, never an
invitation to select the nicer outer prediction. The search/grid controls
are not proof of uniqueness or global optimality between samples.

Before galaxy fitting, test the concentration pivot and r200 normalization
at 1e-12; independent positive-density NFW quadrature at 2e-11; vector vs
inert normalized-shape predictions at 1e-10; synthetic mass recovery at
1e-4 in log10 mass and inner SSE<=1e-8; zero-endpoint and outer-velocity
mutation invariance exactly. Every actual inner-input digest must also be
unchanged by an outer-velocity mutation. No scientific score pass gate.

## Custody and outputs

Commands are `freeze`, `tests`, and `run` (also default). `freeze` pins the
new source/protocol, all inherited files/cases, scenarios, constants and
common masks, without fitting. Authenticated inert modules are imported
only after their byte hashes match. One process/one BLAS thread; a
55-second invocation budget is checked inside fitting loops. No installs.
Publish tests, galaxy cases and final result exclusively and atomically.
Resume only missing galaxies; an interrupted current galaxy restarts from
its beginning. Preserve exceptional cases as error receipts, not silent
exclusions or automatic altered-method retries. Never edit frozen inputs.

Aggregate only after all 100 census receipts exist. PRIMARY metric:
outer galaxy-balanced velocity MSE; SECONDARY: log10 acceleration MSE.
Average radii within each galaxy, then galaxies equally. Include every
eligible galaxy even when its numerical controls fail, with the aggregate
explicitly unqualified. If any prediction is missing, withhold that
scenario/grid aggregate, not just that galaxy. Preserve common reference
metrics and their original qualification independently of new failures.
Save paired per-galaxy differences against every inherited predictor,
parameters, residuals, numerical controls, boundary/extrapolation counts,
hashes and resource use. No bootstrap, data-selected comparison family,
new calibration, full cosmological success or Stage 3 completion claim.
