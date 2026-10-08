# The same excitation fixes a low-field contact defect

2026-09-29. Exact analytical result for the radial scalar sector of the existing
positive harmonic-plus-quartic parent. No new fit, propagation, state reset,
or change to the frozen spectral density. The pressure bound alone must not be
used to exclude joint recalibration of the excited-state model.

## 1. Exact susceptibility, including the displaced orbit

Consider a single scalar oscillator, with physical proper time and momentum,

    H=p²/(2m)+k y²/2+u y^4/4-F y,
    m,k,u>0,  I=(1/(2pi))*oint p dy.

At F=0 let its energy be e>=0 and positive turning amplitude b, so

    e=k b²/2+u b^4/4,
    k²+4u e=(k+u b²)².

The fixed-action energy is even in F, by y->-y. Therefore e_F=0 and the
period's first F derivative vanishes at zero source. Choose phase zero at the
positive turning point. The first displacement xi(t)=partial_F y(t)|I obeys

    m xi_ddot+(k+3u y0(t)²)xi=1,
    xi(0)=1/(k+u b²),  xi_dot(0)=0.                       (1)

The turning-point derivative follows by differentiating
V(b)-F b=e(I,F): V'(b)b_F-b=0. It is not a prescription that b remains fixed.

There is an elementary exact solution. Energy conservation for the unforced
orbit gives

    m (y0²)_ddot=4e-4k y0²-3u y0^4,
    xi(t)=[k+u y0(t)²]/[k²+4u e].                         (2)

Substitution into (1) cancels both the quadratic and quartic terms and matches
both initial conditions. Thus this includes the changing shape of the orbit;
it does NOT replace an oscillator by its RMS curvature. Because T_F=0, the
average can be differentiated over the unperturbed period:

    chi_y = partial_F <y>|I,F=0 = -e_FF|I,F=0
          =[k+u<y0²>]/[k²+4u e].                         (3)

It is positive. For e>0,

    k/(k+u b²)² <= chi_y <= 1/(k+u b²) < 1/k.             (4)

The conservative bounds use 0<=<y²><=b²; an actual nonzero periodic orbit
does not sit at either constant endpoint. At e=0, chi_y=1/k by continuity.
The inertia cancels from this quasistatic period average, not from the
finite-frequency response or the conditions permitting that average.

The fixed-energy and fixed-action derivatives of the MEAN DISPLACEMENT happen
to agree to first order at F=0: <y>(e,0)=0 for every e and I_F(e,0)=0.
This parity fact does not make the energy derivatives interchangeable. The
identity -e_FF=chi is the fixed-action derivative; differentiating an energy
that one has artificially held constant would give zero and is incorrect.
At nonzero F, or across preparations with different actions, the distinction
returns explicitly through e_I dI and the already documented work ledger.

## 2. A directly usable expression from saved energy and pressure

Let p denote the zero-source orbit-averaged intrinsic pressure, not momentum.
The exact virial identities are

    p=u<y^4>/4,   e=k<y²>+3p.

Consequently the loss of the relaxed susceptibility is

    q := 1-k chi_y = 3u(e+p)/(k²+4u e).                  (5)

This is evaluable from the existing returned-state modal energies and
pressures, with no new trajectory or angle quadrature. It ties the physical
stress of an excited mode to its scalar source response. It is not another
independent parameter called a response floor.

In the actual parent k_delta=kappa delta² and F_delta=kappa delta h. Because
(kappa delta)²/k_delta=kappa and Kb=kappa sum w_delta,

    mu_linear = 1-(1/Kb)*partial_h Bbar|h=0
              = sum w_delta q_delta / sum w_delta.        (6)

The bounded source has h(0)=0, h'(0)=1 and h''(0)=0, so it changes neither
this linear coefficient nor the contact cancellation. For a fixed positive
finite band and fixed actions,

    D(g)=mu_linear*g+O(g³),
    0<mu_linear<1

whenever a positive spectral weight is excited with finite energy. The exact
zero-action state instead has zero linear defect. A genuine positive floor
gives a very-low-field inverse-square spherical tail, with G/mu_linear, not an
infinite-range flat rotation law. This is a conditional stationary scalar
statement, not the result of the coupled metric/clock initial-value problem.

No limit order has been exchanged. The original quadratic deep response uses
a soft continuum in its stated regime; a fixed positive gap already changes
the strict zero-field expansion. Fixed actions, a source-dependent prepared
family, and a zero-gap limit are different operations. The previously derived
1.615863 quench-family coefficient cannot replace (6).

## 3. A distribution-independent constraint on a cold scalar state

Use the dimensionless units of
`SHARED_MODE_INFERENCE_AND_STATIC_CLOSURE_V001.md`, with s<=1, k=s², u=1,
positive weights wbar, and I0=sum wbar. Write E=sum wbar e and P=sum wbar p.
Equation (5) becomes

    q_s=3(e_s+p_s)/(s^4+4e_s),
    I0*mu_linear=sum wbar q_s.                            (7)

The per-mode Jensen inequality gives

    (e_s-3p_s)² <= 4s^4 p_s.

Together with (7) it implies q_s e_s<=12p_s: after multiplying the positive
denominator the needed inequality is
e_s²-15e_s p_s<=4s^4 p_s, which is weaker than the displayed Jensen bound.
Now use the exact identity q_s s^4=3(e_s+p_s)-4q_s e_s and s^4<=1:

    I0*mu_linear >= sum wbar q_s s^4 >= 3E-45P,
    boxed: mu_linear >= max(0, 3(E-15P)/I0).              (8)

This is a conservative necessary bound, not a sharp characterization of all
states. It is informative when P/E<1/15. It complements, rather than replaces,
the independently derived pressure floor

    P >= E²/[sqrt(S4+3E)+sqrt(S4)]²,
    S4=sum wbar s^4.                                      (9)

An arbitrary hot energy concentration need not have a large integrated contact
defect: the pressure qualification in (8) matters. No distribution-independent
claim that total energy alone fixes mu is made. Conversely, prescribing a
cold density and a separate zero response defect is incompatible with (8).

For the same modal stored data, (5), (8) and (9) define a small no-fit feasible
region check. The exact coordinate energy and pressure are retained; no
temperature, abundance or per-radius weight is introduced.

## 4. What changing g* can and cannot accomplish

At fixed physical homogeneous excitation density,

    E=(3/4)(1-epsilon²)*Omega_exc*(c H0/gstar_SI)².

Increasing g* therefore lowers the dimensionless energy requirement as g*^-2.
It can relax the inherited-scale pressure bound. This is why the old relaxed
calibration is not a universal exclusion of the new excited-state family.
But the SAME g* also changes the gravitational response and matched vacuum;
it cannot be varied only in the cosmological density conversion.

For a fixed positive band and a fixed action-shape family j_s=zeta*j*_s,
the controlled uniformly harmonic small-zeta limit is

    e_s=s j_s+O(j_s²),
    p_s=3j_s²/(8s²)+higher orders,
    q_s=3j_s/s³+O(j_s²),
    E=zeta sum wbar s j*_s+O(zeta²),
    mu_linear=(3zeta/I0)sum wbar j*_s/s³+O(zeta²).         (10)

Thus if only zeta is adjusted to retain the same physical homogeneous density
in that regime, both E and the resulting floor decrease as g*^-2. The floor
cannot be independently increased to cancel whatever change the relaxed
galaxy scale makes. Outside this uniformly harmonic limit the exact equations
(5)-(7), not (10), apply; the low-gap modes often leave that limit first.

The zero-cutoff relaxed deep scale is a0=8g*/(3pi). Raising g* raises that
reference enhancement scale; excitation creates a competing positive linear
term. Whether the FULL finite-field, boundary-determined excited response can
match galaxies while meeting (8)-(9) is a genuine shared-parameter question.
The signs alone settle neither compatibility nor exclusion. A finite-band
ultralow-field expansion is not a substitute for a whole observed radial
range, and the existing disk outputs must not be rescaled to impersonate it.

The minimum useful test before modifying the spectrum is therefore to retain
the spectrum and actual action template, compute its stress and contact defect
together, and solve the same coupled scalar boundary problem with its shared
parameters. A viable parameter region would then face independent galaxies,
redshift evolution and the full clock/growth/lensing equations. Failure should
identify which shared constraint fails; it should not trigger independent
fitting of I(r), a response floor and cosmic density.

## 5. Scalar and vector scope

Equation (1) is the longitudinal variational problem of a scalar radial orbit.
An isotropic ensemble of VECTOR oscillators includes a different transverse
operator, m d²/dt²+k+u y0², and rotational/angular state information. It is not
obtained by inserting an RMS curvature or by dividing the scalar answer by
three. The scalar susceptibility and (8) are not asserted for that complete
vector ensemble without deriving its response tensor and state transport.

The pressure bound (9) itself does extend to bounded vector orbits through the
same virial and |y| moment inequalities. The distinction lets this exact scalar
test proceed without claiming it has already solved the shared isotropic
cosmological-state-to-galaxy interface. All source work, the old DeltaU baseline
and the momentum/clock constraints remain those of the adopted parent.
