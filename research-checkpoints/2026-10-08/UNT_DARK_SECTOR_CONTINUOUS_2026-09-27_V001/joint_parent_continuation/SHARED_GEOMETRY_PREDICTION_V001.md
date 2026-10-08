# Shared galaxy and expansion prediction

2026-10-03. Prediction-led continuation under the V007 handoff. This note
specifies an effective physical candidate, a discriminating consequence,
and its limits. It is not a microscopic UNT derivation. No added halo of
records is used. The original prepared-mode parent, its failures, and the
recent active joint-work result remain separate and unchanged.

## The physical bridge being tested

The inherited static response has two scales, not one. In its internal
normalization, kappa=u=Lambda=A=1, Kb=1/2 and aI=8/(3 pi). At source h,

    delta^2 z_delta + z_delta^3 = delta h,
    P(h) = integral_0^1 delta^2 z_delta ddelta,
    h(g) = g / sqrt[1+(g/gs)^2],
    mu(g) = 1 - P(h) h'(g)/(Kb g).

Internal accelerations are converted using a0/aI. The only physical force
scales are a0 and r=gs/a0. Here z_delta is a relaxed auxiliary coordinate,
not extra matter. The inherited quartic energy fixes this function; it is
not a newly fitted MOND interpolation. In the adopted static metric limit,

    div[mu(|grad Phi|) grad Phi] = 4 pi G rho_b.

Thus mu approaches g/a0 at small g, approaches 1 at large g, and gives
v_flat^4=G Mb a0 for an isolated spherical asymptotic field. A low visible
density does not itself determine g or the prepared state. This effective
candidate uses local geometry as its environmental variable; the proposed
dense-to-sparse network mechanism has not derived that identification.

The old model linked the integral of this response to a constant vacuum
term by an adopted absolute high-field matching. It did not determine a
cosmic state from galaxies. Here we instead test an explicit geometric
continuation of the SAME response, with no independent constant energy.

## One action and its measurement conventions

Use length units for time (x0=c t) and signature -+++. Adopt a preferred
foliation T with lapse N, spatial metric gamma_ij and extrinsic curvature
K_ij; K is its trace and a_i=D_i ln N. These are supplied effective fields,
not established graph observables. Let ell=a0/c^2 and

    S = (M^2/2) integral N sqrt(gamma) d^4x
        [ R3 + Kij Kij - K^2 + 2 ell^2 F(X) ] + S_b + S_r,
    X = [a_i a^i - eta K^2/9]/ell^2,
    F_plus(y) = integral_0^y [1-mu(a0 sqrt(v))] dv,
    F(X>=0)=F_plus(X),   F(X<0)=-F_plus(-X).

M has the usual Einstein normalization in c=1 units. Restore the physical
matter coupling by the measured G in the static equation above. Ordinary
matter and photons couple minimally to this metric; proper time is d tau,
rulers measure spatial proper length, and volume is integral sqrt(gamma).
Redshift and distance in the homogeneous branch have their usual metric
definitions, 1+z=a_today/a_emit and D_M=c integral dz/H for flat geometry.
No alternative thermometry, redshift convention or record-count volume is
silently substituted. Those would require different observable equations.

The coefficient eta=1 is the first minimal screen: equal dimensionless
weights of proper acceleration and Hubble rate. This is an adopted choice,
not a symmetry derivation. Also retain eta>0 as an explicitly counted
one-parameter extension, without selecting a favorable value after a
failed eta=1 test. The odd extension and F(0)=0 are fixed functional and
absolute-energy assumptions. Adding a constant or changing the negative-X
branch changes the model. Preferred-field modified gravity has antecedents;
see [Zlosnik, Ferreira and Starkman](https://arxiv.org/abs/astro-ph/0607411).
This note makes no novelty claim for that broad construction.

Evolution is defined by varying this action with respect to N, shift,
gamma and T, together with ordinary matter equations. For the screening
branches use an isolated stationary galaxy aligned with T, and a flat
expanding FLRW solution aligned with T. Independent foliation initial data
and a dynamical selection of these branches remain unresolved; their
existence must not be presented as native formation. A stationary effective
constitutive limit is being assumed, not imposed on the active microscopic
state found in the joint-work test. F is only C1 at X=0; full evolution,
crossing regularity and perturbative stability have NOT been demonstrated.

In proper seconds the lapse variation, performed before setting N=1, gives

    y = eta (c H/a0)^2,
    E_eta(y) = 3y/eta - F_plus(y) + 2y F_plus'(y),
    8 pi G rho = (a0/c)^2 E_eta(y),
    rho_dot = -3H(rho+p/c^2),
    q = -1 + 3(1+w) E_eta/(2y E_eta'),  w=p/(rho c^2).

The last expression applies where E_eta'>0 and matter is conserved. The
geometric effective density is (a0/c)^2[F_plus-2yF_plus']/(8 pi G);
its pressure follows from the same field equations, equivalently from its
continuity equation on a solution. It is not independent dust or a fitted
expansion history. Inhomogeneous source work belongs to this action; no
constant rescaling of a source-free Hamiltonian derives its normalization.

## Freedoms and prior exposure

There are TWO adjustable universal force scales (a0,r) in the eta=1
screen, THREE if eta is released. G and c are external measured constants.
Zero independently fitted halo profiles, vacuum offsets, excitation
abundances or expansion functions are included. The inherited spectral
shape, saturation function, odd extension, metric coupling, flat geometry,
stationary closure and foliation are adopted functional/state premises,
not six additional measured successes. Their alternatives are real model
freedom even when no continuous coefficients are fitted in this screen.

Baryonic density, stellar mass conversion, gas geometry, distances and
inclinations are external inputs/nuisances. The homogeneous matter/radiation
densities and initial cosmological branch also need physical input. Free
foliation/memory histories cannot be introduced later without counting and
evolving them. BAO retains one extra amplitude c/(H0 rd) unless rd is
predicted. The old two-parameter-per-galaxy halo comparisons are in-sample
benchmarks, not automatically predictive superiority. No new fit is made.

The exposed reference uses a0=1.2e-10 m/s^2 and r=25.51664211557329.
The latter was SOLVED from H0=73.6 km/s/Mpc and Omega_Lambda=.666, NOT from
galaxies. NGC3198, DDO154, DESI13 and the inherited BBN baryon densities
have already been examined. A calculation using them below is development
or a conditional consequence, not fresh observational validation.

## Discriminating predictions and analytic decision

Define Q(r)=integral_0^gs P(s) ds/(Kb aI^2), with gs=r aI internally.
The static constitutive law gives the exact low-field curvature relation

    x=g/a0,   mu=x+b x^2+O(x^3),
    b=2/r^2-64/(9 pi^2),
    r=sqrt[2/(b+64/(9 pi^2))],
    Hv=(a0/c) sqrt[2Q(r)/3].

Hv is the old matched vacuum scale and a useful normalization here, not
the new model's H0. This model instead predicts the full E_eta equation.
Its cross-domain restriction is especially simple:

    0<F_plus'(y)<1,  0<F_plus(y)<y,
    F_plus(infinity)=2Q(r),
    H^2 < 8 pi G rho/3 + Hv^2       (finite eta>0, y>0).

Therefore a measured ordinary density and Hubble rate impose a lower
bound on r, hence an upper bound on b, regardless of eta. A galaxy-only
inference incompatible with this bound rejects this action family for the
stated source/geometry assumptions. It does not reject every network model.
Conversely, calibrating r with expansion and then quoting Hv as a galaxy
prediction is circular. The inherited baryon-plus-vacuum ceilings
61.8409--61.8967 km/s/Mpc already fall below the exposed 73.6 reference;
the new inequality shows that changing eta alone cannot repair that gap.
These numbers retain their old model-dependent interpretation; they are
not independent raw measurements or a new observational likelihood.

The eta=1 screen gives a stronger no-acceleration result. Concavity of the
polarization implies F_plus''<0. With E=3y-F_plus+2yF_plus',

    2y E'-3E = 3(F_plus-y)-4yF_plus'+4y^2 F_plus'' < 0,
    E'=4-d(g mu)/dg >= 23/9 > 0.

The derivative bound follows from P<Kb h and P'>0:
d(g mu)/dg <= 1+max_z[3z/(1+z)^3]=13/9. Hence q>0 for conserved
ordinary w>=0 matter at every positive density. This specific minimal
closure fails the intended accelerated-expansion target, even though it
retains the conditional galaxy law. No numerical tolerance is involved.

For the larger eta family a positive vacuum root requires

    eta >= eta_crit = 3/max_y[(F_plus-2yF_plus')/y] > 3.

Equality is a tangent constraint root with E_eta'=0, not a certified stable
universe. Counting this new coefficient does not remove the absolute
ceiling above. Independent reviewers checked the lapse variation, signs,
parameter elimination and inequalities; this is internal mathematical
review, not independent empirical confirmation.

## What galaxy data must actually determine

The leading BTFR fixes a0, not r. At fixed a0,

    d ln Hv/db = -r^3 Q'(r)/(8Q(r)),
    0 <= mu_r(g)-mu_infinity(g) <= 2[g/(r a0)]^2.

Thus finite-precision data compatible with the r=infinity limit cannot
bound Hv above. Close to b=-64/(9 pi^2), Hv scales as
[b+64/(9 pi^2)]^(-1/3): the inference becomes ill conditioned. Comparing
only named parameter counts would hide this absence of predictive leverage.
The empirical RAR interpolation has asymptotic b=-1, outside this parent's
domain; that rejects exact identification with the interpolation, not the
underlying observations. An actual disk calculation must use the complete
field including its vertical component and source nuisances.

## Bounded numerical calculation fixed before execution

The companion shared_geometry_prediction_v001.py will quantify ONLY these
new physical consequences, not rerun the old observational scores. Use r
in {4,8,16,25.51664211557329,32,64,128}; compute Q, b, sensitivity, and the
eta threshold. Use the two already exposed baryon densities omega_b=.02166
and .02235 to translate H0=73.6 into necessary r and b bounds. These are
conditional development benchmarks, not fits or withheld tests.

Reuse authenticated mechanical roots. Compare 128/256 quadrature results
within 1e-7 scaled absolute error; independently compare flux to the exact
closed law, derivative to centered differences and curvature extrapolation
within 1e-6. Locate the maximum on logarithmic grids of 513/1025 points
then refine all sampled local maxima; agreement must be within 1e-7.
The eta thresholds are numerical estimates, not rigorous interval bounds.
Use combined scale max(1,abs(value)) for these numerical controls. A control
failure means the affected numerical estimate is unresolved; do not loosen
tolerances to make it pass. The analytic exclusions above stand separately.

This is one small serial worker and one result JSON; no framework, survey
fit or microscopic job is required. Next, assess galaxy-only r leverage
using the saved full disk fields, with the derivative of the outer boundary
and the actual discrete Jacobian. Do not mistake the frozen-mu Picard matrix
for that Jacobian. If it cannot constrain r, seek a predeclared observable
sensitive to the saturation scale rather than importing its cosmic value.
All eleven Stage 3 lanes, including the two distinct CMB inquiries, remain
open. Full photon/lensing, formation, stability and early-universe evidence
cannot be inferred from these background equations.
