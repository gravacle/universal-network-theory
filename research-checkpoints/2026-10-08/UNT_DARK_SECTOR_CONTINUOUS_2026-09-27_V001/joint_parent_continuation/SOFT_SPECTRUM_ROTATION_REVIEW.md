# Independent review: soft-spectrum rotation selector

2026-09-28. Analytical review of `SOFT_SPECTRUM_ROTATION_SELECTOR.md`;
no propagation, fit, source edit or new spectrum was generated.

The stated result is correct for the specified relaxed classical parent,
`V_delta=kappa*(g-delta*y)^2/2+u*y^4/4`, positive constant `kappa,u`, and
`nu(delta)=A*delta^alpha` on `(0,Lambda)`. It is not yet a derivation from
the native BS action or its actual prepared quantum response.

With `b=(alpha+1)/4` and `-1<alpha<3`, the minimum's change of variables
gives the positive integral stated in the note. Independently reducing its
three beta functions gives

    I(b)=12*B(3b,1-b)/[(2b+1)*(2b+2)],
    W ~ 3*B(3b,1-b)/[4*(2b+1)*(2b+2)]
        *A*kappa^(1-b)*u^b*|g|^(2+2b).

Consequently `F~g*|g|^(2b)` and its exponent is `(alpha+3)/2`. The
`alpha=1` coefficient is exactly `pi*A*sqrt(kappa*u)/16` in the energy.
For finite upper cutoff, the first omitted tail is explicitly

    -A*u*Lambda^(alpha-3)*g^4/[4*(3-alpha)].

This follows either from the incomplete-beta tail or from the large-delta
minimum `V_delta~u*g^4/(4*delta^4)`. The existing bounded-source completion
adds `+K_b*g^4/(2*g_s^2)` at this order; replacing `g` by `h(g)` in the
nonanalytic leading term first changes order `g^(4+2b)`. Neither analytic
quartic contribution changes the leading selector within the stated open
interval. At `alpha=3` the tail is logarithmic, above it the cutoff-dependent
quartic term leads, and at/below `alpha=-1` the infrared contact/number
integral needs a different prescription. A finite lower cutoff also changes
the true small-source limit. The note correctly keeps these regimes separate.

For the declared isolated spherical interface, `F(g)/K_b=GM/r^2`, the
circular-speed exponent is

    v ~ r^[(alpha-1)/(2*(alpha+3))].

Thus flat limiting speed selects `alpha=1` in this parent class, not a
universal statement about every network or finite disk radius. Transforming
`lambda=kappa*delta^2` also correctly gives

    rho_lambda=A/[2*kappa^((alpha+1)/2)]*lambda^((alpha-1)/2).

The needed low positive stiffness density is constant, with the specified
source weights. A mere eigenvalue count does not establish the contact,
source overlap, positive quartic energy, actual state, relaxation window,
volume normalization or controlled treatment of cross-mode interactions.
An internal two-dimensional counting analogy does not determine physical
space's dimension. These interpretation limits are retained correctly.

**Review outcome:** coefficient, exponents, endpoint regimes and physical
scope accepted. No mathematical correction to the reviewed note is needed.
