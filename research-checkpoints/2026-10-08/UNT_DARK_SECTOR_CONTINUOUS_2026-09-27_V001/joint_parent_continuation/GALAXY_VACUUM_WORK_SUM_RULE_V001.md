# Test an absolute expansion scale from the galaxy response

2026-10-05 UTC. A proposed effective hypothesis, not an adopted native UNT
law. It changes the polarization to the already used RAR comparator and
adds an explicit physical energy-reference premise. No dark-energy amplitude
is fitted in this screen, and no old source/galaxy calculation is rerun.

The empirical relation is from
[McGaugh, Lelli and Schombert](https://arxiv.org/pdf/1609.05917).
Use its resident galaxy-only calibrated a0, not a cosmologically adjusted
value. Interpreting that relation as a local static constitutive law is an
additional premise; an exact nonspherical field calculation is not inherited
from the radial empirical relation.

## The proposed connection has a definite numerical prediction

In c=1 units, put x=sqrt(g_N/a0),

    g/a0=f(x)=x^2/(1-exp(-x)),
    polarization F(g)/a0=s(x)=x^2/(exp(x)-1), f=x^2+s,
    W'(g)=F(g).

The extra premise is W(infinity)=0: the high-acceleration response has zero
absolute gravitational energy in this convention. This is a PHYSICAL
reference assumption, not a freely harmless constant shift once gravity is
included. The galaxy law alone cannot establish it. Nevertheless it makes
an explicit cross-domain prediction:

    integral_0^infinity F dg / a0^2
      = integral s f' dx
      =2 integral x^3/(exp(x)-1) dx+[s^2/2]_0^infinity
      =2pi^4/15,
    W(0)=-(2pi^4/15)a0^2,
    Lambda_eff=-2W(0)=(4pi^4/15)a0^2,
    H_infinity=[2pi^2/sqrt(45Fbg)] a0/c.

The vacuum normalization uses the existing action: acceleration contributes
+2M^2 W and a cosmological constant contributes -M^2 Lambda. The proper
SI interpretation of W has a0/c^2 as its inverse-length scale. The displayed
H expression restores c. A spatial filter leaves homogeneous B=0 unchanged.

## A dynamics check before any claimed unification

Static ellipticity is not the full health condition of this clock action.
RAR has mu=1-exp(-x)>0 and d g_N/dg=2x/f'(x)>0. But its polarization
derivative epsilon=F'(g)=s'(x)/f'(x) becomes negative at the nonzero root

    (2-x) exp(x)=2.

For the declared positive constant-beta parent, a local longitudinal
principal-symbol calculation gives, when background variation is slow
relative to the perturbation and the filter symbol is applicable,

    omega^2/p^2=[1/(f_filter^2 epsilon)-1]/(3+2/beta).

Negative epsilon makes this clock-gradient branch unstable even while the
static force equation remains elliptic. The detailed allowed-wavelength
window and nonlocal/background qualifications must be retained; a general
claim about every MOND or scalar-tensor completion would be false.

More generally, a smooth nonzero nonnegative polarization with finite total
integral over [0,infinity) must decrease somewhere. It cannot simultaneously
have F'>=0 everywhere. Thus a finite high-field work reference is not an
automatic stable completion of this particular direct-polarization clock
action. Different kinetic/constraint structure would be a new model.

## Frozen arithmetic check

Read a0 values only from GALAXY_RADIAL_TRANSFER_V001_FROZEN.json. The primary
case is rar_calibrated; inherited_calibrated is a labeled scale comparison.
Evaluate the work with independent direct and integrated-by-parts integrands,
256/512-point Gauss quadrature on [0,60], against2pi^4/15 at relative1e-10.
The omitted tail is exponentially small and bounded separately. Find the
nonzero turnover by80 bisections on [1,2], equation residual <=1e-12.
Print static and principal coefficients at x=[.01,.1,.3,1,2,3,10,20] and
ell p=[0,1,10]; no fitted or deleted points. The beta=.5 stability calculation
is distinct from an Fbg=1 homogeneous normalization control.

Report H_infinity and the dust-plus-vacuum H_today illustration using the
already adopted omega_b=.02235. These are predictions conditional on this
changed hypothesis, not measured Hubble rates, a distance fit, an early-
universe success or a native energy derivation. Keep any failed stability
result separate from numerical qualification.
