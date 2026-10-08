# Finite-field common-phase response: prospective numerical protocol

2026-09-29. New, small rerunnable constitutive screen. Source and protocol are
written before their outcomes. The root agent is the sole numerical producer;
peer review and syntax inspection do not execute the producer. No checkpoint,
galaxy fit, new observation, field-grid solve or automatic follow-on is part of
this worker.

## Question and declared sample

For the explicitly conditional macroscopic alpha-one scalar hard-phase action,
solve the common-phase condition

    omega_R(I,h) = omega_R(I_b,0) exp(-Phi), Phi=ln(N/N_b),

using the same calibrated finite-R parent, scalar quartic mode, soft ground
spectrum, hard weight beta=.005, bounded source and absolute matched DeltaU.
This is not a fixed-action calculation or a choice of a hard radial profile.
The scalar constitutive action remains an adoption, not a derived arbitrary
vector ensemble or an identification with native graph modes.

The authoritative input is the complete 360-row five-gap result preserved in
`FINITE_GAP_SHARED_SCREEN_V002_TRANSPORT.json`. Retain its source-row indices.
Use R=128 and 8192, all four actual finite soft quadratures, and all 18 reference
normalizations: 144 inputs. At each use all nine combinations of physical
g={1e-12,1e-10,1e-8} m/s^2 and Phi={0,-1e-8,-1e-7}: 1,296 rows.

The two gaps were selected openly **after** the preceding full five-gap screen
to contrast its warmer/kpc-scale and very-cold/short-cosmic-scale cases, but
**before** any outcomes of this finite-field calculation. This is an exploratory
diagnostic, not an unused observational preselection, an all-five-gap claim or
a deletion of unfavorable old rows. The accelerations are already exposed
probes; the potentials are illustrative, not fitted galaxy potentials. Four
quadratures and 18 calibrations are not 72 independent observational tests.

## Exact orbit reduction and branch policy

Use the complete equations and sufficient hardening proof in
`FINITE_FIELD_COMMON_PHASE_DENSITY_V001.md`, SHA256
`cb8ec369a4e70f78b0bd54e2142f746bdf414c8982b141ba9027bd4958d7bb59`.
The associated action/stress and matching scope is
`MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md`.

Normalize y=R z, eta=h/R^2, i=I/R^3, e=R^4 epsilon and omega=R Omega.
Turning points are c+-r, where c^3+(1+r^2)c=eta. The endpoint-regular factor
q=2+(z+c)^2+2c^2+r^2 gives exact action, period and weighted moments. Pair
theta and pi-theta on [0,pi/2]. Evaluate odd inverse-half and inverse-three-half
weights by rationalized differences, not subtraction of nearly equal weights.
Reflection parity at eta=0 is imposed exactly and separately checked at finite
positive/negative synthetic eta.

Do not form the small frequency excess by subtracting Omega-1 after rounding.
For offset=q-2, compute

    delta=-mean[offset/(sqrt(q)*(sqrt(2)+sqrt(q)))],
    Omega_excess=-delta/(1+delta),
    target_excess=Omega_b_excess exp(-Phi)+expm1(-Phi).

The cosmic excess is recomputed from the saved exact energy-derived amplitude,
not the rounded saved omega/R. Both excesses are retained. The analytic center
uses the hyperbolic real cubic formula.

The sufficient certificate eta^2<1/12 establishes Omega_r>0 at every positive
r, not merely at sampled radii. Its all-field version uses S/R^2; retain that
margin too. For a certified requested field, a target at or below the exact
minimum frequency is a legitimate **EMPTY** branch. Retain its nonzero ground
energy and source response; it receives no occupied J or action-variation
square. Otherwise solve the unique occupied branch with at most 64 bracket
doublings and 80 bisections, using stable frequency excess throughout. A failed
sufficient certificate is **UNCERTIFIED_BRANCH**, not proof of nonexistence.
A numerical root failure is retained as such, not replaced with a disconnected
root, changed parameters or a dropped row.

At every same-g comparison, independently invert action=I_b on the exact
bracket 0<=r<=sqrt(2 i_b), using 80 bisections. This reference is distinct from
holding the newly solved local I fixed when differentiating. The source has
both explicitly named outputs.

## Response, energy and derivative accounting

Compute M3=<z^3> with its exact covariance derivatives. Use b=eta-M3 and

    i_r=epsilon_r/Omega,
    b_i=-M3_r/i_r,
    deficit_fixed_i=M3_eta-M3_r*i_eta/i_r,
    epsilon_ii=Omega_r/i_r.

The common-phase hard susceptibility adds b_i^2/epsilon_ii. Its alternative
form, M3_eta-M3_r*Omega_eta/Omega_r for the deficit, checks the chain rule;
the Maxwell identity checks b_i against -Omega_eta at fixed action. Direct
action differentiation supplies another identity. No numerical finite
differences of a frequency almost equal to one are used.

Retain stable absolute energy as local minimum plus positive endpoint excess,
and pressure as <z^4>/4+eta*b/2. Check the other endpoint, virial identity,
I omega=e+p and action/kinetic identity. DeltaU is the unchanged saved finite-R
value, never reset by field or population. Source energy here omits the
polarization divergence only because this is a *local constitutive* screen;
it is not being presented as the full gravitating density of a spatial solution.

With B=B_soft+beta R^2 b and F=h'B, retain

    K_T=Kb-F/G,
    K_L=Kb-h''B-h'^2[chi_soft+beta(chi_fixed_i+b_i^2/epsilon_ii)],
    F_Phi=-h' beta R^2 Omega b_i/epsilon_ii,
    J=beta R^4[Omega^2/epsilon_ii+3i Omega].

Small deficits/contact differences are evaluated in separated analytic form,
not by subtracting two values near Kb. Save the same-local-I K_L and its
nonnegative phase square separately. Check partial_G(E+3Pi)=2F-F_Phi on every
occupied primary row. The empty branch instead uses its ground envelope and
zero occupied J. The actual local E, Pi, hard action ratio and all signed
force differences against fixed I_b are saved; no favorable-sign gate exists.
The output `D_normalized` means G-F/Kb and `D_over_G` means 1-F/(Kb G).
The unnormalized vector in the BVP is Kb times this normalized response;
physical normalized acceleration is gstar times `D_normalized`.

Local lengths c^2/gstar sqrt(K_axis/J), when both arguments are positive, are
only frozen local static coefficients. Missing/nonpositive arguments yield
null, with the response and branch status retained. They are not halo radii,
global existence results or stability verdicts. Ellipticity is recorded as an
outcome, not imposed as a numerical-success condition.

## Prospective numerical controls

Primary quadrature: Gauss-Legendre 128 on the paired half interval. Controls:
Gauss-Legendre 64 and composite Simpson 1,024 panels. Each rule separately
solves the phase root and fixed-I_b root, rather than just re-evaluating the
primary root. All requested rows and both comparisons are retained even when
one coefficient has an unfavorable sign.

Use relative arithmetic tolerance 2e-11 and quadrature tolerance 2e-8. Energy
identities scale by positive excitation plus absolute minimum so cancellation
in absolute e is not mistaken for precision. Source/Maxwell identities use
their explicitly retained source/deficit contribution scales. Quadrature
comparisons include i, stable frequency excess, e_II, b_i, deficit, pressure,
excitation, K_T, K_L, F_Phi, J and D/G. Tiny final cancellation can therefore
fail a numerical control; it is not silently reclassified as physical success.
At zero source parity zeros are exact. No claim of relative precision is made
for the inherited rounded Omega_b-1 diagnostic.

Synthetic identities before the census use r=0,eta=0 and r=.2 with
eta=0,+.03,-.03. They check empty-branch complementarity, reflection, energy,
action, Maxwell and chain-rule algebra. Saved-origin controls bind every
selected input to the old I, omega, e_II, pressure, K0 and J. Soft cubic
residuals, the all-radius hardening lower bound, exact census/label controls,
and explicit branch counts are retained. Numerical-failure lists and maxima
are published, not replaced with adjusted gates after outcomes.

## Custody, implementation and publication

`finite_field_phase_response_v001.py` imports no prior scientific producer.
It authenticates the incoming transport bytes, decoded raw length/hash and
single zlib stream, wrapper payload/freeze hashes, all old manifest members
recursively, old full census, and the spectrum/reference receipt. Relative
ancestor paths must resolve uniquely within the project. Its new freeze adds
the exact new code, this protocol, and the settled mathematical references.
Original frozen files are read only and never edited.

The program has only `freeze` and `run` commands. Freeze emits a prospective
JSON snapshot, with no new root solving or quadrature. Run verifies that exact
snapshot before calculations and emits one compressed stdout transport. It
sets numerical-library thread counts to one and disables bytecode writes. No
file writes, subprocesses, downloads, plots, checkpoint or background worker
occur. The root publishes stdout verbatim using apply_patch; numeric JSON must
not be parse/stringify-transcoded into different float spellings before
identity verification. Transport includes raw SHA256/length, compressed data,
summary, and a raw wrapper with canonical payload and freeze identities.

Expected products are `FINITE_FIELD_PHASE_RESPONSE_V001_FROZEN.json` and
`FINITE_FIELD_PHASE_RESPONSE_V001_TRANSPORT.json`, followed by an additive
independent saved-data review. A numerical completion validates these local
equations at the declared points. It does not select formation history or a
cosmological-to-galaxy boundary rule, solve the axisymmetric metric equations,
remove the hard energy from the source, establish native mode ownership, or
compare this common-state candidate to observations.
