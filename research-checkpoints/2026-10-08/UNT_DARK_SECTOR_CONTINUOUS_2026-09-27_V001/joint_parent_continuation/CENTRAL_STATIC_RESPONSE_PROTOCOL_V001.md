# Same-state central static response: prospective census V001

2026-09-29. Inert source and protocol before any new outcome. The worker is
stdout-only: the parent saves the `freeze` output before running `run`. It
performs saved-state arithmetic and fixed orbit quadrature, not preparation,
time evolution, a radial integration, a fit, or state selection.

## Census and absolute-energy scope

Retain all 36 original returned-action states and the six fine high-gap pulse
states, in their inherited order. Use their actual zero-source modal energies,
actions and spectral weights, not an equilibrium replacement. Compare all 42
against the inverse-scale-factor-one rows of the saved homogeneous census.
The original 36 additionally retain their independently saved susceptibility
and compression readouts. Original spectral-order and preparation-step
differences remain separate sensitivity comparisons, not new preparations.

The six pulse states have an authenticated finite-spectrum `DeltaU`; retain it
unchanged. The original returned-state records preserve a baseline convention
but do not supply a numeric same-finite-spectrum `DeltaU` in these inputs.
Their signed center coefficient is therefore null, not assigned a zero or an
infinite-gap/cosmologically rematched baseline. No baryon source is invented.

## Exact formulas and new numerical work

In the inherited dimensionless scalar units kappa=u=m=1, write k=delta^2,
e=k b^2/2+b^4/4 and use the cancellation-safe positive root

    b^2=4e/[k+sqrt(k^2+4e)].

For theta in [0,pi/2], q=k+b^2(1+sin^2(theta))/2, define

    j=integral q^(-1/2) dtheta,
    l=integral (1+sin^2(theta)) q^(-3/2) dtheta,
    omega=pi/(2j),
    e_II=omega^2*l/[2j(k+b^2)].

The same positive quadrature gives action, mean y^2 and
Pi_mode=<y^4>/4. For the actual stored action I,

    d=3(e+Pi_mode)/(delta^4+4e),
    chi_B=delta^2*(delta^2+<y^2>)/(delta^4+4e),
    Kcal=sum w*d,
    J_static=sum w*(omega^2/e_II+3I*omega),
    E=sum w*e,  Pi=sum w*Pi_mode.

Thus Kcal is accumulated from positive deficits, not by subtracting two
nearly equal aggregate susceptibilities. Each occupied mode is retained;
there is no cutoff on a small action or small deficit. The existing scalar
identity d+chi_B=1, virial and action-pressure identities are controls.

Primary orbit rule is Gauss-Legendre 128 on the displayed endpoint-safe angle
interval; GL64 is the fixed order comparison. Independent composite Simpson
1024 panels evaluates the same smooth positive integrals. No new turning-point
root, action inversion, derivative finite difference or dynamical integration
is needed. Maximum temporary matrix is 129 by 1025. All 42 states and both
comparison rules remain in the output through errors and aggregate readouts.

For an occupied positive-hardening branch the static phase constraint
N*omega=constant gives d(E+3Pi)/d ln N=-J_static. The diagnostic squared static
wave number is J_static/Kcal. It is NOT a dynamical growth rate, a selected
halo radius, or a proof of an isotropic-vector closure. At strictly zero action
an unoccupied copy held on its minimum does not acquire an artificial
repopulation contribution. The occupied I->0+ limit and exactly empty copy
are distinct; harmonic e_II=0 does not permit division by zero.

For the six finite-spectrum pulse states only, with no ordinary matter:

    active_center_source=E+3Pi-2DeltaU,
    a1=active_center_source/(3Kcal),
    s2=-a1+(Pi-DeltaU)/Kb,
    rho_center/C=E+DeltaU+3(Kb-Kcal)*a1=-3Kb*s2.

Retain both signs, including outward/vacuum-dominated center slopes. These are
regular averaged-scalar center coefficients, not a constructed smooth radial
microscopic vector center. Annulus interpretation and state/clock transport
qualifications remain those of `POLARIZED_STATIC_RADIAL_REDUCTION_V001.md`.

## Fixed controls and tolerances

Before outcomes: analytic/arithmetic identities have normalized tolerance
2e-11; GL64/128, Simpson/GL128 and inherited modal/aggregate comparisons have
relative tolerance 2e-8. Pressure and action-pressure residuals are normalized
by positive modal energy, not tiny pressure. Curvature, action, frequency,
deficit and J comparisons use their positive primary magnitudes, with only a
fixed 1e-300 underflow floor. Every absolute error is retained alongside its
normalized maximum. There is no gate on a desired center sign or scale.

Synthetic controls, not additional physical states: finite-gap b=0 gives the
positive-quartic limiting e_II=3/(4delta^2); u=0 gives exactly harmonic e_II=0;
pure quartic delta=0 at b={.25,1,3} gives Pi=e/3,
I*omega=4e/3, e_II=omega/(3I) and modal J=8e. The exact zero-action static
repopulation rule is recorded separately from an occupied limiting branch.
All 42 states must match the inherited census and have positive saved actions.

## Custody and output

Authenticate exact result-file pins, payload checksums, matched freeze files
and every inherited manifest member inside this project. Do not import or
execute ancestral producer modules. Freeze this source, this protocol, the
analytical identities and the entire authenticated input lineage. The worker
writes no file; `run` requires a byte-matching saved prospective snapshot.

Output includes each state identity, E/Pi, Kb/Kcal, J and J/Kcal, positive
modal deficits/e_II/J, soft-versus-hard contributions, the six owned center
coefficients, comparison errors and all failed controls. A failure exits
nonzero and is preserved, never repaired by dropping modes or changing a
tolerance. Target output is below 1 MiB. No physical source/time/volume scale
is inferred by this arithmetic, and no galaxy data are read.
