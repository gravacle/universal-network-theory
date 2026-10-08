# A finite-time pathway to the soft-spectrum force

2026-09-28. Analytical continuation of
`SOFT_SPECTRUM_ROTATION_SELECTOR.md` and the resident
`joint_parent_dynamics/MECHANICAL_STATE_AND_RATE.md`. No numerical worker,
new native coefficient, dissipative term or frozen-file edit.

## Result

The cubic relaxed energy is carried by adjustment modes near a definite
source-dependent scale, not by an unspecified collection of infinitely slow
modes. Their finite-time response can be tested. The same positive mode
inertias also generate a calculable **conservative source inertia**; for the
flat-curve spectrum and constant mode mass it grows logarithmically as the
source weakens. This supplies a sharper time-window test than merely asking
whether one mode has time to oscillate.

A finite, positive-gap band admits a common smooth source ramp that prepares
its classical minimum arbitrarily closely, without damping or resetting.
That is a conditional preparation mechanism, not a claim that the actual
native prepared state already equals that minimum. Initial excitation,
excluded-mode force and all switching work remain measurable obligations.

## 1. Which modes carry the force?

Use the same externally clamped scalar source `g>0`, or the radial coordinate
of the vector parent at fixed source direction:

    H_delta = p_delta^2/[2 m(delta)]
              +kappa*(g-delta*y_delta)^2/2+u*y_delta^4/4,
    m(delta), kappa, u > 0,
    nu(delta)=A*delta^alpha,  -1<alpha<3.

Weights multiply both kinetic and potential energies; `m(delta)` is the
inertia per mode in that convention. It is not inferred from a density of
stiffness eigenvalues. In the bounded-source completion, this section's g is
the internal magnitude h; the complete external source energy still includes
`K_b*(g_external^2-h^2)/2`. Near the origin h equals g_external to leading
order, but the distinction matters outside that window.

At the unique minimum, define

    delta_g=(u/kappa)^(1/4)*sqrt(g),
    s=delta/delta_g,  z=delta*y_*/g,
    s^4=z^3/(1-z),  0<z<1.

The exact mode force is `F_delta=kappa*g*(1-z)`. Thus, in the continuum,

    F_*(g)=A*kappa*g*delta_g^(alpha+1)
            *integral s^alpha*(1-z(s)) ds.                       (1)

The ideal endpoints are zero and infinity. With `b=(alpha+1)/4`, the
integral equals `C_alpha=3 B(3b,1-b)/[4(2b+1)]`. For alpha=1,
`C_1=3*pi/16` and `F_*~C_F*g^2`, where
`C_F=3*pi*A*sqrt(kappa*u)/16`.

There are explicit force-tail bounds. Since `0<1-z<1` and
`1-z=z^3/s^4<=s^-4`, the relaxed contribution outside
`epsilon*delta_g <= delta <= S*delta_g`, with `epsilon<1<S`, is at most

    [epsilon^(alpha+1)/(alpha+1)+S^(alpha-3)/(3-alpha)]/C_alpha

of the ideal continuum force. At alpha=1 this is

    relative relaxed tail <= 8/(3*pi)*(epsilon^2+S^-2).           (2)

Consequently a finite band can capture any declared fraction of the cubic
response. This is a positive-weight bound, not a cancellation-sensitive fit.
It does **not** license dropping arbitrary unprepared tail coordinates:
hard modes have small *relaxed net force* because two large terms cancel,
and an excited or lagging hard mode can upset that cancellation. Section 5
gives an actual-state force certificate for the tails.

## 2. Exact frequencies and finite-size limit

The radial tangent stiffness and source derivative of the minimum are

    k_rad=kappa*delta^2+3u*y_*^2
         =kappa*delta^2*(3-2z)/z,
    omega_rad^2=k_rad/m(delta),
    dy_*/dg=kappa*delta/k_rad=z/[delta*(3-2z)].                   (3)

For each transverse coordinate of the vector parent,

    k_trans=kappa*delta^2+u*y_*^2=kappa*delta^2/z,
    omega_trans^2=k_trans/m(delta).                             (4)

Source rotations therefore require a transverse response check as well as
the fixed-direction radial calculation. These are response frequencies, not
decay rates. No friction or bath has been specified.

For constant m introduce

    omega_g^2=kappa*delta_g^2/m=sqrt(kappa*u)*g/m.

Then `omega_rad^2/omega_g^2=s^2*(3-2z)/z` and
`omega_trans^2/omega_g^2=s^2/z`. For very soft modes,

    y_* ~ (kappa*delta*g/u)^(1/3),
    omega_rad^2 ~ 3*kappa^(2/3)*u^(1/3)*delta^(2/3)*g^(2/3)/m,
    omega_trans^2 ~ omega_rad^2/3.                              (5)

For hard modes, both approach `kappa*delta^2/m`. The modes near delta_g
therefore respond on an order `omega_g^-1 ~ g^-1/2` time, while the ideal
zero-delta tail remains arbitrarily slow for constant m. For a different
owned positive m(delta), equations (3)-(4), not this constant-m exponent,
are the applicable screen. For example, if locally `m~delta^eta`, the
very-soft frequency scales as `delta^(1/3-eta/2)` at fixed g.

A true finite-size lower cutoff changes the strict static limit. With its
contact consistently restricted to the same modes and
`g << g_gap=sqrt(kappa/u)*delta_min^2`,

    F_*(g)=A*u*g^3 *integral_delta_min^Lambda delta^(alpha-4) ddelta
            +higher orders.

At alpha=1 the leading coefficient is
`A*u*(delta_min^-2-Lambda^-2)/2`. It is cubic force, not the quadratic
continuum force. Keeping the old zero-cutoff contact while deleting its
soft response would instead manufacture an extra linear term; that is not
the same finite-mode parent. The desired intermediate interval requires
`delta_min << delta_g << Lambda`, with its actual weighted spectrum smooth
enough on that band. A finite set of widely spaced lines is not a continuum
merely because its smallest frequency is low.

## 3. The source inertia is derived, not supplied as another clock function

Linearize about a fixed minimum at nonzero g. For a small Fourier component
of the *same radial source*, a single mode has retarded force kernel

    R_delta(omega)=kappa
        -(kappa*delta)^2/[k_rad-m(delta)*(omega+i0)^2].           (6)

This retains the compulsory contact and the complete driven oscillator.
It displays resonant forced motion, not equilibration. For a finite band
and frequencies uniformly below its tangent frequencies, expansion gives

    R_total(omega)=F_*'(g)-omega^2*M_rad(g)+higher orders,
    M_rad(g)=integral nu(delta)*m(delta)*(dy_*/dg)^2 ddelta >0.  (7)

For a frequency ratio `|omega|<=theta*min(omega_rad)`, `theta<1`, the
error after the displayed omega-squared term is bounded by
`omega^4*integral nu*m*(dy_*/dg)^2/omega_rad^2 /(1-theta^2)`.
No such uniform spectral-gap assertion is made at zero cutoff.

There is a useful exact expression for alpha=1 and constant m. Let
`z_min,z_max` correspond to delta_min,Lambda at this g. Direct substitution
in (7) gives

    M_rad=(A*m/4)
       *[-ln(1-z)+(3/2)ln((3-2z)/3)]_(z_min)^(z_max).           (8)

For transverse source variations, the pullback mass instead is

    M_trans=integral nu*m*(y_*/g)^2 ddelta
           =(A*m/4)*[z^2-z-ln(1-z)]_(z_min)^(z_max).           (9)

In the continuum window,

    M_rad ~ A*m*[ln(Lambda/delta_g)-(3/8)ln3],
    M_trans ~ A*m*ln(Lambda/delta_g).                         (10)

These masses are positive exact integrals; the asymptotic expressions must
not be extrapolated outside their large scale separation. The soft endpoint
of (8) is integrable at fixed g even though its minimum frequency is zero.
That fact by itself does not justify the entire frequency expansion through
resonances; one first controls a finite band and its excluded response.

The same result follows by retaining the kinetic energy along the moving
minimum. To leading slow-drive order, for fixed source direction,

    L_effective=(1/2)M_rad(g)*g_dot^2-W_*(g),
    F_required=F_*(g)+M_rad*g_ddot+(1/2)M_rad'(g)*g_dot^2+... . (11)

It also follows directly by solving the mode displacement as
`y=y_*-m*y_*ddot/k_rad+...` in the full source force. Equation (11)
is a conservative derivative correction from the specified parent. It is
not a new fitted K(Q), a physical proper-time identification or autonomous
volume production. A source kinetic term already present in a full parent
must additionally be retained. In the bounded-source model the radial
pullback mass for the external source is `h'(g_external)^2*M_rad(h)`;
the complete static source derivative includes its identity/contact term.

For small radial modulations, comparison of inertia to static response gives
the sharper constant-m screen

    T^2 >> M_rad/F_*'
        ~ [8/(3*pi)]*omega_g^-2*ln(Lambda/delta_g).             (12)

Here T is the physical source variation scale, not the computer runtime.
For order-one fractional source changes, evaluate both terms in (11)
against F_*; their scales are comparable to, but not identical with, the
linear-modulation test. In a galaxy the relevant source history must be
specified in the actual network frame. An orbit period cannot automatically
be used as that history if the source field is stationary in that frame.

## 4. A conservative preparation route exists at finite cutoff

Assume a finite set, or a compact positive-cutoff band with uniformly
bounded positive m and coefficients. Prepare each classical coordinate at
the zero-source minimum with zero momentum. This is an explicitly declared
preparation, not a statement about the previously formed native state.
Drive the common source as `g(t)=G*f(t/T)`, where f increases smoothly from
zero to one and is constant in neighborhoods of both endpoints. No
mode-specific counterdiabatic force or new interaction is added.

Every clamped minimum is unique and the mode curvature is at least
`kappa*delta_min^2`. Define the trial trajectory

    y_trial=y_*(g(t))-m*y_*ddot/k_rad.

On a fixed band its leading lag is O(T^-2); substitution in the exact mode
equation leaves an O(T^-4) residual. This follows because the correction's
second derivative and its quadratic nonlinear remainder are both that
order. Flat endpoint derivatives make the trial coincide with the desired
initial and final minimum and zero momentum.

One can control the actual solution, not only the trial residual. For
`w=y-y_trial`, use the positive relative energy

    E_w=m*w_dot^2/2+V(y_trial+w,g)-V(y_trial,g)-V_y(y_trial,g)*w.

Its exact derivative is

    E_w_dot=-residual*w_dot
       +[V_y(y_trial+w)-V_y(y_trial)-V_yy(y_trial)*w]*y_trial_dot.

The explicit source terms cancel in the bracket. Uniform convexity controls
w squared by E_w; on the bounded small-error interval the second term is
O(T^-1)*E_w. The resulting energy inequality bounds sqrt(E_w) by a constant
times the time integral of the O(T^-4) residual, namely O(T^-3). A
small-error bootstrap closes for sufficiently large T on this fixed band.
Thus the source ends with O(T^-3) residual displacement/velocity and
O(T^-6) excitation energy above its new minimum. Constants depend on the
chosen band, G and masses; they are not uniform as delta_min goes to zero.

After the ramp those errors oscillate; they do not decay. Nevertheless this
gives a legitimate conservative way of approaching the classical static
force to a prescribed tolerance. Its work is exactly the complete energy
change: relaxed potential increase plus remaining kinetic/potential
excitation. Initial nonzero actions are not removed by making this ramp
slow. A quantum ground-state preparation or thermal ensemble has different
conditions, already kept separate in `MECHANICAL_STATE_AND_RATE.md`.

## 5. An actual-state force certificate and the noncommuting limits

For any coordinates and momenta at a clamped g, define E_ex as their total
energy above the classical minimum. Convexity and Cauchy-Schwarz give

    E_ex >= (1/2) integral nu*kappa*delta^2*(y-y_*)^2 ddelta,
    |F_actual-F_*|^2 <= 2*K_b*E_ex,
    K_b=kappa*integral nu.                                  (13)

The same inequality applies separately to an omitted band with its own
contact and excitation energy. It is a sufficient, possibly loose bound,
but it makes discarding arbitrary soft or hard states unnecessary. For a
band initially at y=p=0, followed by one source step and subsequent hold,
`E_ex<=K_band*g^2/2`, so its force error is at most `K_band*g` for the
entire closed evolution. For the soft alpha=1 band below epsilon*delta_g,
that is at most `8*epsilon^2/(3*pi)` times the ideal cubic-law force.
If that band is actually omitted from a representation, comparison with the
ideal full relaxed law must include both its relaxed force tail and its
actual-state lag allowance; they are distinct errors. In this example each
can be bounded by `8*epsilon^2/(3*pi)`, so their sum, not either one alone,
is the corresponding conservative total allowance.
For a different history or initial state, use its actual energy; the
one-step bound does not transfer without its work ledger.

A fixed finite observation time cannot be silently exchanged with static
minimization. For example, take constant m, alpha=1, delta_min=0, initially
y=p=0, and step to small g. With `c=sqrt(kappa/m)`, the exact linear term is

    F(t)=A*kappa*g*[Lambda*sin(c*Lambda*t)/(c*t)
                      +(cos(c*Lambda*t)-1)/(c*t)^2]+O(g^3).   (14)

At t=0 its continuous value is `K_b*g`. It follows from
`y_delta=(g/delta)*(1-cos(c*delta*t))+O(g^3)`. For generic fixed finite t,
the leading force is linear and oscillatory, not proportional to g|g|.
The bounded-source completion has the same linear term at the origin.

Dephasing can make this continuum *linear coefficient* tend to zero at long
times. It does not remove the injected oscillator energy or prove that a
finite-amplitude step reaches the nonlinear minimum. A finite discrete
network instead retains its finite sum of oscillations. Therefore neither
an unqualified t-to-infinity limit nor a long numerical run is equivalent
to relaxed-state preparation.

The constructive order is: select a physical finite band and state accuracy,
control its actual source history/energy, and establish an intermediate
source interval. For constant m a useful small-radial-modulation screen,
with its frequencies below the controlled band's poles, combines

    delta_min << delta_g << Lambda,
    T^2 >> (8/(3*pi))*[m/(sqrt(kappa*u)*g)]*ln(Lambda/delta_g),

with the exact band-frequency and actual-state error tests above.
This is not an unconditional necessary condition for every source history:
a stationary source and specially controlled cancellations require their
own assessment. Previously
derived quantum/thermal floors and the bounded-source correction ceiling
must fit inside the same interval; none is erased by the present classical
time analysis.

## 6. The next native measurements are specific

The smallest useful native result is not another source-free eigenvalue
histogram. In one actual prepared network and one physically identified
deformation/source, determine together:

1. The complete contact, source insertions and weighted positive stiffness
   spectrum, including whether `k_delta=kappa*delta^2` and source overlap
   `b_delta=kappa*delta` arise from the same energy. The quartic coefficients
   and cross-mode couplings test the separable approximation.
2. The pole frequencies and residues of that source's actual retarded
   response. For this mechanical parent they must agree with
   `b_delta^2/[k_delta-m(delta)*(omega+i0)^2]`, including the contact and
   the positivity/state assumptions. Frequencies plus stiffness fix inertia;
   a density of states alone does not. The native double-commutator sum rules
   constrain the same total oscillator strength.
3. Finite-size delta_min and the weighted spectral coverage around delta_g;
   the measured source history, calibrated time and actual excitation energy
   determine equations (2), (12), and (13) without fitting a relaxation time
   to the desired galaxy curve.

The newly qualified native writer-pulse response demonstrates how to make
an actual-state source/time measurement, but its record-copy source is not
automatically this spatial deformation. Its negative prepared response
weights cannot be silently replaced by a passive oscillator population.
A same-parent source/coordinate reduction or a different owned active
mechanism must establish that link.

This is a concrete solution pathway: a source-coupled soft spectrum with its
own inertia, preparation and physical clock can yield a controlled galaxy
force window. The displayed conditions decide that window once those native
quantities are supplied; they do not invent them or add a dark component.
