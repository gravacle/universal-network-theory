# A retained hard-mode state has a calculable cold-history capacity

2026-09-29. Analytical follow-through of the same positive harmonic-plus-quartic
parent, not a new numerical run, parameter fit, spectrum replacement or state
selection. The six saved pulse states retain their actual gaps, weights and
actions. All equations below use their inherited m=kappa=u4=1 units.

## 1. One dimensionless amplitude determines the whole history

For an unforced hard mode of gap R>0 and turning amplitude b, define

    r=b^2/R^2,
    epsilon(r)=r/2+r^2/4,
    f(r)=(2/pi)r integral_0^(pi/2)
                      cos^2(theta) sqrt[1+r(1+sin^2(theta))/2] dtheta.

Then exactly

    e=R^4 epsilon(r),        I=R^3 f(r),
    omega=R*pi/(2j(r)),
    j(r)=integral_0^(pi/2) [1+r(1+sin^2(theta))/2]^-1/2 dtheta.       (1)

f is strictly increasing because I_e=1/omega>0 and epsilon'>0. Conservation
of a^3 I at inverse scale factor A=a^-1 therefore fixes a unique amplitude:

    f(r_A)=A^3 f(r_1).                                            (2)

Neither its pressure nor its nonlinear frequency is another adjustable input.
Using normalized time weight proportional to q^-1/2, q=1+r(1+t)/2,
t=sin^2(theta), let M4(r)=<t^2>_r. The exact averaged pressure ratio is

    w(r)=p/e=r M4(r)/(2+r).                                       (3)

This is strictly increasing for r>0. To see this without a numerical grid, put
v(t)=(1+t)/q. Differentiating normalized time weights gives

    d ln M4/dr=-(1/4)[<v>_(t^2-weighted)-<v>_r].

v is increasing, with range

    v(1)-v(0)=2/[(1+r)(2+r)].

The bracket is nonnegative and no greater than this range. Consequently

    d ln w/dr >= 2/[r(2+r)]-1/[2(1+r)(2+r)]
                =(4+3r)/[2r(1+r)(2+r)] >0.                        (4)

The harmonic and quartic virial limits give w(0)=0 and w(infinity)=1/3.
Thus every definitional cold threshold 0<w_c<1/3 selects a unique r_c through
w(r_c)=w_c. Such a threshold is not itself an observational bound.

## 2. Exact capacity and the useful small-pressure scaling

For a FIXED retained action I_1 and gap R, coldness throughout 1<=A'<=A is
equivalent to the single endpoint condition

    A^3 I_1/R^3 <= f(r_c).                                       (5)

Written as a design inequality, R>=A[I_1/f(r_c)]^(1/3). This does not authorize
changing the gap of a saved state at no cost: changing its Hamiltonian is a
different preparation with a source-work and matched-baseline ledger.

Alternatively suppose a prospective design specifies its present weighted
hard-mode excitation E_H1=beta R^4 epsilon(r_1), with the SAME known hard
weight beta (the saved pulses use .005). Define

    r_req=f^-1[f(r_c)/A^3].

The exact capacity condition is

    R >= [E_H1/(beta epsilon(r_req))]^(1/4).                       (6)

At the earlier endpoint alone, specified E_H(A) is cold only if
R>=[E_H(A)/(beta epsilon(r_c))]^(1/4). Replacing E_H(A) by E_H1*A^3 without
qualification would be circular; the exact same-state energy is given by (2).

In the controlled cold regime,

    f(r)=r/2+5r^2/32+O(r^3),
    w(r)=3r/16+O(r^2)=3e/(8R^4)+O(e^2/R^8).

Hence, while the earlier state is also cold,

    w(A)=A^3 w(1)[1+small nonlinear corrections],
    R^4 >= approximately 3 E_H1 A^3/(8 beta w_c).                 (7)

The full exact condition (6), rather than (7), applies near the transition.
At A=1101 the action amplification is exactly 1,334,633,301. Illustratively,
maintaining w_c=.01 in the cold approximation requires present w roughly below
7.49e-12, not merely below .01 today. These are arithmetic consequences of an
explicit threshold and scale factor, not a cosmological fit or new numerical
evaluation of any stored pulse. The frozen dilution census tests the six
actual states without changing them.

## 3. What broadening or continuously supplying a population can change

A distribution of hard gaps can postpone its aggregate pressure transition,
but does not remove the cost. The existing distribution-independent bound,
with E=sum w_j e_j, P=sum w_j p_j and S4=sum w_j delta_j^4, is

    E <= 2 sqrt(S4 P)+3P.

Thus P/E<=w_c<1/3 requires

    E <= 4S4 w_c/(1-3w_c)^2.                                    (8)

Also E(A)>=A^3 E(1). A NECESSARY cold-history condition is therefore

    S4 >= A^3 E(1)(1-3w_c)^2/(4w_c).                             (9)

It is weaker than the exact single-mode condition and is not sufficient. In a
finite hard band of total weight beta and maximum gap R_max, its contribution
to S4 is at most beta R_max^4. Any spectrum change must carry its same-parent
contact and matched-DeltaU ledger. Redistributing a FIXED total weight among
gaps retains Kb but generally changes DeltaU; adding weight changes Kb as well.
Neither is an independently compensating fit parameter, and the enlarged
parent cannot silently inherit its old soft-only matching.

Every fixed finite set of occupied quartic modes eventually approaches
w=1/3 under unlimited backward adiabatic compression. Indeed each e(I) tends
to a constant times I^(4/3), so E(A) tends to a constant times A^4. This is an
asymptotic statement about the named adiabatic model, not an extrapolation
through an epoch in which its clock separation fails.

Continuous CREATION is different from a continuous spectrum. If a specified
physical formation process introduces action at rate J_j,

    dot I_j+3H I_j=J_j,
    dot E+3H(E+P)=sum w_j omega_j J_j       (h=0).                 (10)

The right side is source work. A reservoir must lose that energy; prescribing
an arbitrary J_j(a) from the desired cosmology would not be a prediction. A
late actual formation event can invalidate backward extrapolation of today's
constant a^3I, but its earlier state, reservoir and radiation/stress then have
to be evolved, not erased. Neither (8) nor (10) is evidence that native BS
dynamics produces the proposed spectrum or population.

## 4. Coherent force cancellation is a separate, constructive state question

At h=0 a symmetric orbit has <y>=<dot y>=0, yet one actual coherent scalar
pulse retains B(t)=sum w_j delta_j y_j(t) and its large derivative. Small
pressure does not suppress those coherent terms. There are explicit NEW
ensemble constructions which cancel their mean without removing energy:

* Uniform independent phase populations give ensemble <B>=<dot B>=0. With
  N_j independent copies sharing total weight w_j, the scalar variances are

      Var B=sum_j (w_j^2/N_j) delta_j^2 <y_j^2>,
      Var dot B=sum_j (w_j^2/N_j) delta_j^2 <dot y_j^2>.           (11)

  These formulas require the stated independent phases; they do not hold for
  the same common coherent pulse. The stronger clock derivative may demand
  more averaging copies even when the mean is zero.

* At the vector-parent level, an equally weighted antipodal set of radial
  orbits along the three coordinate axes has zero vector B and dot B and
  isotropic second moments at h=0. Divide each original weight among the six
  oriented copies, so total energy/action measure is not multiplied by six.
  Opposite pairs remain opposite in the unforced symmetric mode equations.
  This is an explicit ensemble/replica state, not six simultaneous directions
  of one classical vector, and not what the old single-direction pulse made.

* A genuinely continuous finite frequency band with integrable amplitudes can
  dephase the aggregate Fourier harmonics; its characteristic dephasing time
  is of order the inverse frequency width. Finite discrete populations have
  residual fluctuations and recurrences. A spectrum or phase distribution
  introduced for that purpose requires its own preparation and matching ledger.

None of these constructions removes positive orbit energy or the pressure
capacity in (5)-(9). Pairing can remove the source's first moment but not its
isotropic oscillating pressure, or establish rapid averaging against a physical
Hubble/clock time. At nonzero galactic h the paired trajectories are no longer
opposites: their finite-field vector response and the coupled momentum/clock
conditions must be recomputed from the actual state. No scalar force curve is
silently promoted to that isotropic-vector closure.

The productive next discriminator is therefore already the fixed 42-state
dilution census: retain its actual energy, pressure and physical-rate conditions.
If a genuinely isotropic population is pursued next, specify the common
preparation and finite-copy/phase correlations first, with no per-radius
action tuning. Cold storage, coherent cancellation and autonomous formation
are distinct calculable requirements of one model, not interchangeable names.
