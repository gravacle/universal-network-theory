# Mode stiffness cannot erase the bounded-source contact

2026-10-05 UTC. New analytical gate for an explicit hybrid of the existing
bounded-source parent and positive MODE-gradient stiffness. No fit, old
Solar rerun, native-law adoption or full nonlinear solution. Two independent
analytical reviewers derived the same contact and susceptibility identities.

Keep h(g)=g/sqrt(1+|g|²/gs²), positive quartic modes, the old spectrum and
critical normalization. Add J_delta=κ delta² ell² in the mode gradient energy.
Unlike FILTERED_SOURCE_SHARED_CANDIDATE_V001, the physical input and its
direct contact are NOT filtered. Uniform gradients vanish, so this hybrid
retains the old finite uniform work DIFFERENCE, conditionally on the same
absolute high-field matching. Its r still used an expansion calibration;
this is not an independent cosmological prediction or matter-era repair.

At fixed nonzero external e n, let B_e=∫ν κdelta y_e, b_e=|B_e|/Kb,
and H_delta be the positive mode-potential Hessian. Eliminating the linear
mode perturbation gives the exact clamped-background tensor

    K(k)=C-Dh^T [∫ν(κdelta)²
                  (H_delta+κdelta²ell²k² I)^-1 ddelta] Dh,
    C_ij=Kb delta_ij-B_e,l partial_i partial_j h_l.

This C is the full source contact, not a separately adjustable coefficient.
The normalized K/Kb is the linear gravitational-flux Hessian. With
q=kell>0, H_delta>=0 and ∫νκ=Kb give the SOFT-SPECTRUM-UNIFORM bound

    0 <= C-K(k) <= Kb ||Dh||²/q² I <= Kb/q² I.

Consequently K tends to C, not Kb I. Suppressing mode adjustment is not
the same operation as suppressing the contact. The old held-polarization
nonlinear Solar diagnostic already failed; its Q2 must NOT be assigned to
this finite-gradient hybrid without a full coupled solution/error bound.

## Anisotropy survives at every q in the frozen external state

Put F=(1+e²/gs²)^-1/2, α=F, β=F³, gc=3πa0/8 and normalized spectral
coordinate s=delta/Lambda. Positive external t_s obeys

    t_s+t_s³=h(e)/(gc s²),
    W_T(q)=∫0¹2s ds/(1+t_s²+q²),
    W_L(q)=∫0¹2s ds/(1+3t_s²+q²).

The exact normalized tensor eigenvalues are

    K_T/Kb=1+b_e eF³/gs²-F² W_T(q),
    K_L/Kb=1+3b_e eF⁵/gs²-F⁶ W_L(q).

They recover the old relaxed local Hessian at q=0. At q->infinity they
recover the saved frozen contact eigenvalues, C_T/Kb=1.00262376180768 and
C_L/Kb=1.00780750904458 at the inherited primary external field.
Since W_T>=W_L>=0 and F²>=F⁶,

    (K_L-K_T)/Kb >= b_e eF³(3F²-1)/gs² >0

whenever e²/gs²<2. The frozen primary e/gs is about .09, so this includes
EVERY wavenumber of its linearized background. A positive mode stiffness
cannot cancel that anisotropy. The tensor is not Newtonian even if its
mode response has become small. This is a linear constitutive result, not
an observational likelihood or a full nonlinear Solar no-go.

As a bounded diagnostic independent of a new quadrature, use q=100 and the
already saved enclosures x=(e/gs)² in(.008,.009), local transverse μ in
(.67,.69). The contacts satisfy C_T/Kb-1=(1-μ)x>.00248 and C_L>C_T.
The uniform susceptibility bound then certifies

    lambda_min(K/Kb-I) > .00248-.0001 = .00238.

No new numerical worker is required for this large-margin inequality. It
does not compare solar observables. For ell100pc, q100 has wavelength
2πpc; linearization still requires a genuinely small source perturbation
about the Galactic background. Near the real Sun that condition fails.

The nonzero anisotropic high-k limit leaves an anisotropic1/k² point-source
Green singularity. A finite point-source origin quadrupole integral cannot
be borrowed from the linear-source or filtered-input candidate. Finite
ordinary sources and nonlinear central matching must be retained.

## A structural restriction and a possible full coupled test

For a nonzero external polarization, exact high-k Newtonian recovery at
every e would require both h''=0 and h'/e-h/e²=0: h=const*e. A nontrivial
globally bounded radial h cannot obey that everywhere. Isotropy alone
requires h''=h'/e-h/e², with global solutions h=e(c1+c2 ln e), which also
cannot be nontrivially bounded on(0,infinity). Isolated cancellations at
chosen backgrounds would be new constitutive premises, not a general cure.

A useful next nonlinear route, if needed, is an a posteriori test of the
SAVED frozen Solar trial g0, not its rerun. Set z_delta=delta y_delta,
a_delta=u4/(κdelta⁴), Z=∫2s z_s ds. The exact hybrid mode equation is

    (-ell²Delta+1)z_delta+a_delta|z_delta|²z_delta=h(g).

Vector monotonicity and Kato comparison on the decaying branch imply
|z_delta-z_e,delta| <= S_ell |h(g)-h_e| uniformly in the soft spectrum.
This bounds the MODE response to a verified frozen trial, with field
residual -Dh(g0)^T deltaZ. It is NOT yet an error bound for the coupled
field or finite-shell Q. A complete dual/coercivity estimate, verified trial
tail and retained boundaries must convert that residual to the observable
before claiming a full finite-gradient failure. No guessed GM envelope is
substituted for a verified trial bound.

## Recover the successful distinction without repeating it

V130's existing filtered-input law uses b=Sg and D=g-SF(Sg), with both
reciprocal filters derived from the action. Its high-k Hessian is
I-(1+q²)^-2 Q and tends to I. Its completed nonlinear Gaussian-source
certificate and conditional endpoint preservation are retained; neither is
new evidence from this note. Its missing matter-era history, formation,
causal/metric completion and expansion exposure remain. Do not rerun it.

Anchors: ENVIRONMENTAL_RESPONSE_AFTER_SOLAR_TEST_V001.md;
SOLAR_FROZEN_POLARIZATION_V001.md and qualified result/audit;
GRADIENT_RESPONSE_COMPATIBILITY_V001.md;
FILTERED_SOURCE_SHARED_CANDIDATE_V001.md;
FILTERED_SOURCE_NONLINEAR_BOUND_V001.md; frontierV130. All eleven lanes OPEN.
