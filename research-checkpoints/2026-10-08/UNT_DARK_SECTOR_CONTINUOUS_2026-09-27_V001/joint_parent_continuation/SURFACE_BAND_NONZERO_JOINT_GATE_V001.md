# Test the same surface band's nonzero field with complete material relaxation

2026-10-05 UTC. Prospective protocol, frozen before execution. The sealed
SURFACE_BAND_ANISOTROPIC_GATE_V001 source-zero failure is retained. This is
a separate branch test of the SAME complete area-plus-band action; it adds
no counterterm, energy subtraction, occupation function or fitted branch.
Observer_cosmography owns only this new protocol, its corresponding worker
and RESULT.json/.md, plus the new exclusive directory
surface_band_nonzero_joint_gate_v001_checkpoints/ for this attempt's small
input manifest, append journal and completed-state JSON files. Root must
review protocol/source before one local
single-threaded numerical process executes. Cap: 512 MiB; no other worker
is started by this agent. Root owns any disjoint native-carrier worker.

## Complete energy and a transparent fixed example

Use the prior declared reference-frame tangent metric, four-state source,
fixed-mass displacement matrix, conserved band census and ground preparation:

    a = sqrt(u^T(E^T F^T F E)^-1u),
    x = eta |F^T b|, eta=d0/Lambda0,
    r = sqrt(a^2+x^2), z=x^2/(r+x),
    E_area = Sigma <|cof(F)n|>, E_band = -B<r+z>,
    E = R+E_area+E_band+V|b|^2/(8piG), V=V0 det F.

Nothing is subtracted from the absolute reference, the source-free band or
the finite-source energy. Critical A_ref=4piG C0 d0^2 Lambda0=1 and
B=V0 C0 Lambda0^3/3 fix 4piG=V0/(3B eta^2). The field term therefore has
coefficient (3B eta^2/2)det(F)|b|^2. Field energy is not independently
normalized after the material coefficients are selected.

Choose BEFORE results B=V0=eta=1, Sigma=8 and R=1. The dimensionless field
coordinate is the physical acceleration multiplied by eta. Then

    E = 1+8<|cof(F)n|>-<r+z>+(3/2)det(F)|b|^2.

This is a transparent constitutive example, not an observational calibration.
At F=I,b=0 it has energy 8, h=7/3, G=31/15 and M=8/15. The previously
defined frozen-material speed squares are 31/35 and 8/35; thus this example
passes those source-zero material gates before any new branch outcome.
That does not retire the sealed anisotropic source-zero failure or qualify
the internal quantum, clock or gravity kinetic block.

## Field-only stationary branch and its limits

For fixed F, critical polarization is

    P = F F^T b <1/(r+x)>/det(F).

Along the largest left singular axis, source stationarity b-P=0 is

    f(x) = lambda_max^2 <1/(sqrt(a^2+x^2)+x)>/det(F) = 1.

The earlier exact nonconformal proof gives f(0)>1. The function decreases
strictly to zero, so each tested anisotropic shape has exactly one positive
x root; its opposite-sign partner has equal energy. The held-shape field
Hessian has positive radial curvature and transverse factors
1-lambda_i^2/lambda_max^2. Degenerate largest singular values give flat
directions. This is held-shape source stability, not material stationarity,
phase formation, a galaxy solution or a homogeneous cosmological solution.

The isotropic reference has b=0 and a degenerate quadratic source block;
its leading positive cubic source energy is retained. No inverse/pseudoinverse
is used to pretend that its zero Hessian is a positive nonzero branch.

## Full strain chart, cubic invariant and exact Hessian

Use the fixed current logarithmic material chart

    F(q)=exp(Q)F0, Q=sum_A q_A S_A.

The five orthonormal tracefree symmetric matrices are

    S1=diag(1,-1,0)/sqrt(2),
    S2=diag(1,1,-2)/sqrt(6),
    S3=(e12+e21)/sqrt(2), S4=(e13+e31)/sqrt(2),
    S5=(e23+e32)/sqrt(2).

The sixth matrix S_V=I/3 makes q_V exactly log(V/Vheld), independently
of the five constant-volume directions. Physical field coordinates b_i
are varied independently. The exact 9 by 9 Hessian includes the exponential
chart curvature (prestress), rather than dropping it at a nonstationary
material state. Its material gradient is retained. It is an energy-curvature
gate in this stated chart, not an inferred sound speed or invariant stability
of an unforced state with a nonzero material gradient.

For tracefree symmetric e, independent angular expansion gives

    <|cof(exp(e))n|> = 1+(4/15)tr(e^2)-(8/63)tr(e^3)+...,
    <a> = 1+(1/15)tr(e^2)+(32/315)tr(e^3)+...,
    <1/a> = 1+(1/15)tr(e^2)-(32/315)tr(e^3)+... .

Hence complete source-zero material energy has cubic coefficient
-(40Sigma+32B)tr(e^3)/315. S2, whose cubic trace is nonzero, tests this
invariant explicitly. The exact finite-strain integral and exponential are
used throughout; the expansion is a control, not the constitutive law.

For the scalar band kernel K=r+x^2/(r+x), useful exact derivatives are

    K_a=a(r+2x)/(r+x)^2, K_x=3x/(r+x),
    Hess(K)=3/[r(r+x)^2] [[x^2,-ax],[-ax,a^2]].

For tangent metric C, q=C^-1u and z_t=u^T C^-1u=a^2,

    (z_t)_A=-q^T C_A q,
    (z_t)_AB=q^T(C_A C^-1 C_B+C_B C^-1 C_A-C_AB)q,
    a_A=(z_t)_A/(2a),
    a_AB=(z_t)_AB/(2a)-(z_t)_A(z_t)_B/(4a^3).

C_A=2E^T F0^T S_A F0 E and
C_AB=2E^T F0^T(S_A S_B+S_B S_A)F0 E retain the complete chart terms.
Source x derivatives come from h=F0^T b, h_A=F0^T S_A b,
h_AB=F0^T(S_A S_B+S_B S_A)b/2 and h_i=F0^T e_i.
The worker differentiates the full area, band and bare field terms before
performing the angular average or field Schur elimination.

When H_bb is positive and invertible, the field-relaxed material Hessian is

    H_red = H_qq-H_qb H_bb^-1 H_bq.

Its full six-dimensional spectrum and five-dimensional tracefree block,
all mixed entries and all material gradients are saved. Independent nested
field minimization along each of the five strain directions checks the
corresponding reduced curvature. Energy is compared with b=0 at the SAME
shape and with the fixed isotropic reference, with no re-zeroing.

## An exact volume support identity, not an acceleration requirement

At a source-stationary field,

    E_field=(3B/2)<z>,
    partial_ln(s) E = 2E_area+B<r-z/2> > 0.

The last expression follows from F->sF, a->a/s, x->sx and the same source
stationarity. This prevents an unforced STATIC material volume minimum in
the stated action/domain, regardless of a favorable shear Schur spectrum.
It does not exclude an expanding cosmic solution: negative pressure and
tension need not satisfy E_s=0. Nor is this static gravitational field-energy
functional automatically the homogeneous FLRW matter stress. Those full
metric/clock and observational questions remain separate.

All material forces, including tracefree ones, are retained. A held-strain
root with a nonzero material gradient requires external reaction/support
in the static interpretation. No support potential is added. Integrability
of b as grad(Phi), clock/metric constraints, boundaries, formation work and
kinetic positivity must be owned before calling a root a formed phase.
Actual supported mechanical stability would also require the real support
potential's second variation. Positive curvature in the chosen strain chart
does not by itself supply that loading premise.

## Frozen worker and numerical gates

The same SO(3) reference-normal/in-plane construction as the sealed gate is
copied as pure mathematical helpers; the old producer is NOT imported or
executed. Its source, protocol and receipt hashes are retained as inputs.
The new source and this prospective protocol are hashed before evaluation.

Two fixed independently shifted reference grids use Gauss--Legendre normal
cosine and uniform normal azimuth and tangent phase:

    low: 24 x 48 x 48, shifts(phi,psi)=(.17,.23), 55296 frames;
    high: 32 x 64 x 64, shifts(phi,psi)=(.31,.47), 131072 frames.

Fixed shapes are F0=diag(exp(epsilon),exp(-epsilon),1), with
epsilon=0,.005,.02,.1,.3,.5. The positive largest-axis source root is
bracketed from x=1 by doubling at most 32 times, then bisected 80 times.
The isotropic control is explicitly b=0. Each grid evaluates its own root
and all exact energy, gradient, joint-Hessian and Schur quantities.

Independent full-energy finite differences use all 9 gradients and all 81
Hessian entries at every state. For the five strain coordinates and log
volume the base step is .002. At a nonzero branch, each field coordinate
uses min(.002,.04|b*|). Three halving levels use centered differences and
the Richardson value (4D_h/2-D_h)/3. The isotropic reference is checked by
its exact source Hessian and fixed strain finite differences; its source
cusp is checked with the prior two-stage extrapolation, not a false
nonzero-branch Schur inverse. All five nested field-relaxed strain curvatures
use base step min(.002,.1epsilon) with three halving levels.

The S2 cubic control uses +/- .02,.01,.005, checks the odd cubic quotient
and quadratic-error Richardson extrapolation against all three independent
cubic coefficients. Normalization, unit/orthogonality and second/fourth
angular moment controls are retained.

Frozen tolerances: exact algebraic identities and source stationarity 2e-11;
normalized cross-grid energies/gradients/Hessians/Schur matrices 2e-6;
normalized finite-difference gradient/Hessian entries 2e-5; nested relaxed
curvatures 5e-5; cubic coefficients 2e-6. Matrices are normalized by
max(1,max|analytic|). Classification uses a 2e-5 eigenvalue margin: positive,
negative or numerically unresolved. Failed checks/near-boundary outcomes
are retained, not repaired by changing grids or parameters.

The receipt separates arithmetic verification, held-field curvature,
material/Schur curvature, nonzero material support gradients and physical
phase qualification. A positive held-field or supported curvature does not
override the source-zero failure or establish an unforced formed phase.

## Custody, execution and next action

The single worker uses OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=
VECLIB_MAXIMUM_THREADS=1 and PYTHONDONTWRITEBYTECODE=1. Its exclusive new
receipt records PID/PPID, execution time, maximum RSS, all checks, complete
small joint matrices and input/source/protocol hashes. It refuses overwrite.
Canonical payload hashing excludes only its own hash field. A failure is
preserved without a repeat. Root preflight approval is required before this
one execution; no numerical process is active when this protocol is saved.

Before the first row, create the exclusive checkpoint directory, seal a
manifest with PID/PPID, input/source/protocol hashes and controls, and begin
an append-only journal. Refuse an existing directory by default; it is
evidence of an attempt to inspect, not permission to discard or resume it.
After each fully evaluated epsilon, seal state_NNN.json with that complete
state, its checks, row elapsed time and peak RSS, then append its raw and
canonical hashes to the journal before starting another row. Preserve all
completed states and a sealed error record if a later row fails. If RSS is
at least 512 MiB after a row, save that row and stop subsequent rows; the
overall receipt retains the peak and failure. No automatic resume or rerun
is added. These are local resumable outputs, not a coordination framework.

If interrupted, inspect the owned process/session and partial output before
any recovery decision. The exact next action is the root's source review,
then the frozen single execution if approved. After completion, interpret
only the checked supported/static branches, preserve the original failure,
and identify the remaining formation, compatibility and full-action work.
No automatic resumption, new scheduler or background continuation is implied.
