# Independent shared-state and static-closure review

2026-09-29. Read the complete
`SHARED_MODE_INFERENCE_AND_STATIC_CLOSURE_V001.md`, SHA-256
`48dbfeeefc012af2f4d663e1ec37732f9e007efcbbe8fd66bfaced64a4a9a07b`.
Analytical review only: no worker, fit, or change to an earlier result.

**Accepted within the stated effective-parent and averaging assumptions.**

The scales in equations (1)-(3) check directly. Dividing the mode equation
by `kappa*Lambda^2*y*` gives unit quadratic/quartic coefficients; dividing
the energy by `E*=kappa^2*Lambda^4/u4` gives the same dimensionless action.
The stress prefactor is exactly `4 M^2 g*^2/(1-epsilon^2)`. The spectral
normalization A therefore cancels only when its simultaneous contribution to
Kb and C is retained. It is not an independent abundance parameter in this
specified family. The SI conversion and equation (7) also check.

For scalar or vector bounded zero-source orbits, the virial identity gives
`E=2V2+3P`, `P=V4`. Jensen followed by weighted Cauchy-Schwarz gives
`V2^2 <= (sum wbar*s^4)P`. Solving the resulting quadratic inequality in
sqrt(P) yields equations (5)-(6), with the stated continuous E=0 limit.
No inertia or action-distribution assumption enters that inequality beyond
the rapid orbit average and positive fixed quadratic/quartic parent. Its
use on nonadiabatic coherent states, or after altering the spectral moment,
would require a different calculation.

For the radial scalar equilibrium, `Q=mu/N`, `Pi_Q=I` and
`Pi_h=-e_h=Bbar` after summing weights. Thus substituting the boundary-connected
solution of `omega(I,h)=mu/N` into the averaged action is a legitimate
Legendre reduction wherever e_II is nonzero. On the specified positive
e_II branch, the implicit derivative is exactly equation (9). The ground
action boundary and tilted-oscillator softening are not removable by this
change of variables and are correctly retained as branch limitations.

Varying lapse and radial metric before fixing areal coordinates gives

    rho/C = E+DeltaU+aF+div F,
    p_r/C = Pi-DeltaU-aF,
    p_t/C = Pi-DeltaU,     F=Bbar*h'.

These are not the stress of a freely appended perfect fluid. A direct
conservation check is especially useful: `Pi'=-(E+Pi)nu+F*a'`, with
`nu=N'/N`, gives `p_r'/C=-(E+Pi)nu-aF'`. Since
`nu div F=a[F'+2(R'/R)F]`, every term in equation (13) cancels.
The anisotropic `-aF` term and the lapse dependence of Q are essential.
Static zero momentum and time-independent stress also give no immediate
additional clock inconsistency; this is not a proof that an arbitrary
boundary-value solution exists or that the underlying time-dependent clock
problem is stable.

The note correctly separates two distinct state proposals: a zero-source
isotropic vector ensemble and a radial scalar equilibrium. A radial source
does not automatically align the former or erase transverse actions. The
four-parameter count applies only after fixing the template, cutoff, epoch,
ensemble, clock rule and ordinary-source data as stated. In particular zeta
owns real excitation energy, not an absent matter stress. The inherited
relaxed a0 calibration is a diagnostic reference, not already the prediction
of this new excited-state family.

This gives a concrete joint inference target and an exact pre-fit pressure
test. It does not claim native BS binding, formation selection, a galaxy
solution, an independently tested cosmological abundance, or observational
success.
