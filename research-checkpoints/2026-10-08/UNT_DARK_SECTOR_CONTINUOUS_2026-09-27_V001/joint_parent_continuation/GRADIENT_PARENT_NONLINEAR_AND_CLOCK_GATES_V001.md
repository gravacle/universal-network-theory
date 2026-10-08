# What the spatial-response opening still requires

2026-10-04. Analytic continuation of the changed linear-source gradient
candidate, not a new fitted model or completed cosmology. Independent source
review supports the static identities below. The linearized quadrupole now
also has a successful independent numerical audit (51 checks); its stated
nonlinear ceiling remains intact.

## Static freedoms and a useful nonlinear certificate

The static candidate has the inherited empirical a0 and one uncalibrated
length ell. The old source-saturation ratio r is removed, not retained as a
third static parameter. Quartic potential, critical normalization, spectral
weight 2s ds and J_delta=kappa delta^2 ell^2 are adopted functional assumptions.
The mode inertia and formed-state history are still unbound to physical data.

In radius-independent notation, put z_s=z_e,s+v_s and
a_s=1/(gc^2 s^4), Z_v=integral_0^1 2s v_s ds. Let P_L be the longitudinal
spatial projector, with boundary conditions fixed. Eliminating the Newtonian
potential from the static variational problem gives, up to source-only terms,

    E[v] = integral d^3x { (ell^2/2) integral 2s |grad v_s|^2 ds
           +(1/2) integral 2s |v_s|^2 ds -(1/2)|P_L Z_v|^2
           +integral 2s a_s B4(z_e,s,v_s) ds -gN.Solar dot Z_v },

where B4 is the quartic Bregman difference. The exact identity

    B4(z,v) = [|z+v|^4-|z|^4-4|z|^2 z dot v]/4
            = |z|^2 |v|^2/2 + (z dot v+|v|^2/2)^2

implies, with aT=1+a_s|z_e,s|^2 and I_T=integral 2s/aT ds<1,

    E[v] >= (ell^2/2)||grad v||^2
            +(1-I_T)/2 integral d^3x integral 2s aT |v_s|^2 ds
            - integral d^3x gN.Solar dot Z_v.

The weighted Cauchy inequality and ||P_L||<=1 justify the last step. This is
a coercive strictly convex finite-source, boundary-fixed static problem. It
supports a residual/energy test; it is not proof of healthy relativistic
time evolution, native state selection, or a small Solar quadrupole error.
In particular the origin Hessian is not a bounded observable of this energy
norm. A finite-annulus force/tidal readout and its dual norm must be specified.

For a reconstructed finite-source linear trial v_L, its nonlinear residual is

    r_s=a_s[2(z_e dot v_L)v_L+|v_L|^2 z_e+|v_L|^2 v_L].

The secant inequality

    (|z+e|^2(z+e)-|z|^2 z) dot e >= (3/4)|z|^2 |e|^2

provides an a posteriori coercivity route if the corresponding integral
sup_x integral 2s/[1+(3/4)a_s|z_trial,s(x)|^2] ds is below one.
Neither that spatial certificate nor the finite-annulus dual norm was
computed by the completed Fourier coefficient calculation.

The finite Sun is important: a point-source linear trial has v_s of order
C=GM/(2ell^2) inside lambda_s approximately ell*s^(2/3). Its quartic energy
then has a soft integral proportional to integral ds/s. For a smooth finite
source, modes with lambda_s smaller than the source radius instead have
v_s proportional to s^(4/3), regularizing that integral. Do not interpret a
point-source trial's energy divergence as a demonstrated physical instability
or ignore it when asserting uniform nonlinear accuracy.

## The shared expansion obligation is not removed

With the fully spatial projected gradient completion, homogeneous FLRW has
a_mu=0 and D_i y=0. Reuse the explicitly varied stress from
EXPLICIT_MODE_COSMOLOGY_PATHWAY, not an assigned equation of state:

    m(q_ddot+3H q_dot)+kappa delta^2 q+u4 |q|^2 q=0,
    rho=Cnorm(T+V2+V4+DeltaU),
    p=Cnorm(T-V2-V4-DeltaU).

Zero classical initial modes remain zero. Rapid bounded excitations have
0<=w<=1/3. Slow displaced modes can have negative pressure, but their physical
inertias, occupied spectrum and preparation energy are additional state data.
Linear sourcing and spatial smoothing supply none of that homogeneous driving.
Removing source saturation also makes the old endpoint DeltaU divergent;
keeping its former finite numerical value would be an independent adopted
vacuum budget. An unprojected covariant derivative could have different
H-dependent terms, but is a changed completion, not implied by this model.

The next narrow calculation is a finite-source linear reconstruction and
nonlinear-residual certificate for the Solar observable. Separately, bind
the physical mode clocks and formation energy before claiming shared late
acceleration. A positive static result does not close the expansion, growth,
BBN, lensing or either CMB lane.
