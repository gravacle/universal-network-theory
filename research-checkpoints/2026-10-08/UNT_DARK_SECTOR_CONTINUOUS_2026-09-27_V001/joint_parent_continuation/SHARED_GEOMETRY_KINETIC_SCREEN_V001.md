# Scalar kinetic test of the shared geometric action

2026-10-03. Analytical continuation of SHARED_GEOMETRY_PREDICTION_V001.md.
This test checks a physical perturbation of the proposed galaxy/expansion
action before an unnecessary background fit. It is not another microscopic
consistency experiment and does not exclude UNT or general network gravity.

## The constructive alternative considered

The first screen fixed eta=1 and failed to accelerate. Holding the old
r=25.5166421 while varying eta also cannot reach the exposed baryonic
expansion reference. Releasing BOTH r and eta removes that second ceiling
objection; this would be a two-constant universal calibration, not an
independently fitted halo and not the original frozen model succeeding.

We considered calibrating H0=73.6 km/s/Mpc and q0=1.5(.334)-1=-.499,
with omega_b=.02235 and the inherited a0. These H0/Omega_m summaries are
already exposed and model-dependent; q0 is calculated from a flat LCDM
reference, not a direct model-independent acceleration measurement. The
question here is whether this action could healthily realize that target,
NOT whether the target by itself observationally excludes the action.
No such fit or new DESI scoring was executed.

Write X0=(cH0/a0)^2, y0=eta X0, Omega_b=omega_b/(H0/100)^2,
B=3 Omega_b X0 and G(y)=F_plus(y)-2yF_plus'(y). Dust conservation would
require

    G(y0,r)=3X0-B,
    y0 G_y(y0,r)=3X0-3B/[2(q0+1)],
    eta=y0/X0,  E'=3/eta-G_y.

These equations are algebraically valid; the new obstruction comes from
the perturbations of precisely the same action.

## Derivation of the physical sign

Expanding the extrinsic-curvature terms on FLRW gives the principal form

    delta Kij delta Kij - lambda_eff (delta K)^2,
    lambda_eff=1-(2 eta/9)G_y.

Indeed the additional trace term is the second derivative of
-2 ell^2 F_plus(eta K^2/(9 ell^2)). With scalar curvature perturbation zeta
and scalar shift beta, the leading short-wavelength expression is
delta Kij=zeta_dot delta_ij-partial_i partial_j beta. Its quadratic form is

    3(1-3lambda) zeta_dot^2
      +2(3lambda-1) zeta_dot Delta beta
      +(1-lambda)(Delta beta)^2.

Eliminating beta yields

    C_zeta zeta_dot^2,
    C_zeta=2(3lambda_eff-1)/(lambda_eff-1).

The ordinary tensor kinetic term has the positive Einstein sign. Thus
1/3<lambda_eff<1 is a negative scalar kinetic sign relative to it. At
lambda=1/3 or1 the reduction is degenerate and cannot be called a pass.
The lapse-gradient coefficient is 2F_plus'(y)>0. At sufficiently short
subhorizon wavelength, eliminating lapse modifies this principal kinetic
coefficient only at subleading order; it does not remove the sign above.

This is conditional on a valid subhorizon effective-theory window in which
these local operators dominate. If no such window is admitted, the saved
action is not a closed prediction for those perturbations: a cutoff or
memory completion must be specified and tested, not invoked after the fact.
This is not an estimate of a decay rate or an unqualified nonlinear
instability theorem, and no ghost from a truncated theory is automatically
attributed to its unknown microscopic parent.

## The coupling constants drop out of this test

Using the background and conservation equations eliminates r and eta:

    lambda_eff,0=1/3+Omega_b/(q0+1).

More generally replace Omega_b by (1+w)Omega_ordinary for a conserved
ordinary fluid. At the stated reference,

    Omega_b = .04125930411153119,
    lambda_eff,0 = .4156872337555513,
    C_zeta = -.845648822135421.

No choice of the two calibration constants changes this result while
retaining those same background targets and this action. For q>-1 and
positive ordinary density, the positive-kinetic branch would require
q+1 < (3/2)Omega_b, or q<-.9381110438 for this baryon fraction. That is a
necessary sign condition, not sufficient stability or an accepted cosmic
history. A phantom branch or a changed matter budget changes the premises.

The standard GR comparator does not inherit this extra scalar kinetic mode;
the singular lambda=1 expression above is not a diagnosis of GR.

## Decision and scope

Do not fit H0 and this q0 merely to display an accelerating H(z) and call
the result viable. The trace-only geometric extension fails this early
stability screen in the specified regime. An additional operator,
constraint, nonlocal memory or changed physical clock can be investigated,
but is a NEW counted completion with a corresponding perturbation test.
The first failed eta=1 case and fixed-r bound remain preserved.

The constructive network-capacity alternative is developed in
NETWORK_CAPACITY_AND_VOLUME_V001.md. Its main unresolved term is the
same-parent evolution coupling capacity to physical volume; identifying
the two by a coordinate convention is not sufficient. Native active
memory is not prohibited by the present local-action exclusion.

An independent internal reviewer derived the calibration and kinetic
relations; the main investigator separately checked the quadratic shift
elimination and arithmetic. No new numerical worker, observational score,
outside review, installation or completed Stage 3 claim is involved.
