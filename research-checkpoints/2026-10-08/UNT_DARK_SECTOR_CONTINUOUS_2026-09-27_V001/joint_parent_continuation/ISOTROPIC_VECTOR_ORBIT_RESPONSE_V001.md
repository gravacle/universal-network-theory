# The actual vector weak-field orbit response, with its neutral modes retained

2026-09-29. Exact first-order orbit analysis of the adopted positive central
mechanical mode. This is not a native BS derivation, a new ensemble preparation,
a finite-field galaxy solution or a numerical worker. It supplies the missing
transverse calculation before an isotropic population can use scalar results.

## 1. State and source being varied

Let

    H=|p|^2/(2m)+k|y|^2/2+u|y|^4/4-F dot y,
    m,k,u>0.

At F=0 take the actual bounded straight-line orbit y=y0(t)n, with fixed unit
axis n, zero angular momentum, signed turning amplitude b>0, energy
e=kb^2/2+ub^4/4, and signed-oscillation action

    I=(1/(2pi))oint p_parallel dy0.

Its full period is T; y0(t+T/2)=-y0(t). At zero angular momentum the usual
nonnegative-radius central action is I/2, not I. One must not keep that radial
action fixed while silently adding angular action and call it the same state.

Here I is the fast signed-oscillation action, n is an explicit slow orientation,
and the forced first-order correction is chosen to contain no independently
excited free angular-momentum/ellipticity mode. The periodic construction below
defines this condition. Adding such a neutral homogeneous mode is different
initial data, not something removed by phase averaging. The mass m controls
time and the action-to-amplitude conversion even though the response at specified
b below is independent of m.

Resolve a constant infinitesimal physical mode force F into components along
and perpendicular to n. Per unit corresponding force, the corrections obey

    m xi_parallel_ddot+(k+3u y0^2)xi_parallel=1,
    m xi_perp_ddot+(k+u y0^2)xi_perp=1.                         (1)

The known fixed-I longitudinal particular solution is

    xi_parallel(t)=(k+u y0(t)^2)/(k+ub^2)^2,
    chi_parallel=<xi_parallel>.                              (2)

Its first-order energy/period shift is zero by F-to-minus-F symmetry. The
transverse perturbation also changes the fast action and energy only at second
order; its neutral orientation data still have to be specified separately.

## 2. The rotational zero mode is real, but does not obstruct this source

Set P=T/2. The transverse coefficient in (1) is P-periodic, whereas y0 itself
is a homogeneous solution which is ANTI-periodic over P. Its first-order
Hamiltonian evolution matrix has determinant one. A -1 Floquet multiplier
therefore forces the other multiplier also to be -1, including the possible
Jordan case. There is no +1 multiplier over P.

Consequently a P-periodic constant source has a UNIQUE P-periodic particular
solution. This argument requires no assumption that the full-T rotational
kernel is absent. On the full period the same source satisfies its necessary
Fredholm orthogonality exactly, since integral y0 dt=0. In the harmonic limit
the additional homogeneous solution is also anti-periodic over P, and the
same forced-sector result holds.

Choosing the P-periodic correction fixes the source-driven response without
inverting a rotational zero eigenvalue. An added multiple of y0 is an
infinitesimal axis change and has zero fast mean; it can instead be fixed by
an explicit orientation gauge. A second free transverse solution can carry
nonzero angular momentum and secular rotation. It is excluded by the stated
state prescription, not declared decayed or dynamically forbidden.

This is not automatically the response to an arbitrary abrupt switch-on at an
arbitrary orbital phase. Such a preparation can excite those homogeneous
solutions. The periodic response must be realized by an owned preparation,
slow-source reduction with its initial neutral data, or an explicitly held
orientation experiment; it is not a universal long-time attractor.

## 3. Exact positive transverse quadrature

Choose t=0 at y0=b, and let

    K=k+ub^2,    eta=ub^2/(2K),    0<eta<1/2,
    L(q)=asin(sqrt(q))/[sqrt(q)sqrt(1-q)],  L(0)=1,
    R(y)=L(eta[1-y^2/b^2])/K,       0<=y<=b.

The exact P-periodic even response is

    xi_perp(y)=R(0)+y integral_0^y [R(0)-R(s)]/s^2 ds,            (3)

continued evenly to negative y. The apparent origin singularity is removable:
R(0)-R(s)=O(s^2). A convenient exact mean is

    chi_perp =
       [int_0^b xi_perp(y)/sqrt(e-V(y)) dy]
          /[int_0^b 1/sqrt(e-V(y)) dy],
    V(y)=ky^2/2+uy^4/4.                                       (4)

Use y=b sin(theta) for endpoint-safe numerical evaluation if needed later.
Equations (3)-(4) define a compact integral, not an RMS-stiffness replacement.

Derivation: the Wronskian obeys

    m d/dt[y0 xi_perp_dot-y0_dot xi_perp]=y0.

Reflection symmetry of the P-periodic solution sets its derivative to zero
at the turning point and at the central crossing. On the descending quarter
orbit this gives

    y xi_perp_y-xi_perp=-R(y),
    R(y)=[int_y^b z dz/sqrt(e-V(z))]/[2sqrt(e-V(y))].             (5)

Since e-V=(b^2-y^2)[2k+u(b^2+y^2)]/4, the numerator integrates to an arcsine
and gives the expression above. The even regular solution of (5) is (3).
It has no added odd homogeneous y term and is exactly the selected P-periodic
solution. Its angular momentum at first order is oscillatory with zero mean;
an independent constant angular-momentum homogeneous component is not included.

## 4. Bounds show why the scalar and vector answers differ

The positive representation

    L(q)=int_0^1 [(1-q)(1-q z^2)]^-1/2 dz

shows L'>0 and L''>0. Thus R decreases with |y|, and (3) gives

    xi_perp(y)>=R(0)>1/K>=xi_parallel(y).                     (6)

It also gives L(q)<=1/(1-q) and L'(q)<=1/(1-q)^2. The mean-value theorem in
(3) then bounds

    xi_perp(y)
      <=[L(eta)+eta L'(eta)]/K
      <=1/[K(1-eta)^2]
       =4(k+ub^2)/(2k+ub^2)^2 <1/k.                          (7)

The last strict inequality leaves exactly u^2 b^4 when its positive
denominators are cross-multiplied. These bounds hold even when the original
radial orbit crosses the origin. In particular,

    0<chi_parallel<chi_perp<1/k       (u>0,b>0).               (8)

At b=0, or u=0, both susceptibilities reduce continuously to 1/k. No divergence
is hidden by dropping the rotational zero mode; it belongs to a different
Floquet sector from the selected constant forcing.

With r=ub^2/k small, expansion of (3) gives

    k R(0)=1-2r/3+O(r^2),
    k xi_perp(y)=1-2r/3+r y^2/(3b^2)+O(r^2),
    k chi_perp=1-r/2+O(r^2),
    k chi_parallel=1-3r/2+O(r^2).                            (9)

The unperturbed harmonic mean <y^2>/b^2=1/2 suffices at this order.

## 5. When an isotropic trace is justified, and what it predicts

For a fixed axis the proven first-order tensor is

    chi_ab(n)=chi_perp delta_ab
                   +(chi_parallel-chi_perp)n_a n_b.          (10)

A population with the same action at each orientation, explicitly fixed fast
orientation statistics <n_a n_b>=delta_ab/3, and the selected zero-free-mode
prescription therefore has

    chi_iso=(chi_parallel+2chi_perp)/3,
    k chi_iso=1-5r/6+O(r^2).                                (11)

This includes a properly weighted finite orientation design with the required
second moment; it does not require pretending that one vector is simultaneously
oriented three ways. The population weights must be divided among copies or
ensemble members so that total energy/action measure is unchanged. Fast-phase
uniformity and the absence of correlated free angular-momentum modes are owned
state conditions, not deductions from small pressure.

For the adopted mode coupling F_j=kappa*delta_j*h, k_j=kappa*delta_j^2 and
Kb=kappa sum w_j, the fixed-population zero-field contact deficit becomes

    mu_iso=1-sum_j w_j(kappa delta_j)^2 chi_iso,j/Kb.           (12)

Equations (8)-(11) prove, for occupied positive-weight modes,

    0<mu_iso<mu_scalar.

In the weak-excitation limit its leading deficit is 5/9 of the scalar one,
not zero. This is a local linear coefficient for the named isotropic state,
not a new finite-field interpolation or a galaxy fit. It changes neither its
zero-source orbit energy nor its cold-history pressure requirement.

## 6. The slow torque must not disappear from the model

For fixed fast I and orientation, the second-order averaged source term is

    delta e_av=-[chi_perp F^2
                   +(chi_parallel-chi_perp)(n dot F)^2]/2.    (13)

This is a local fast-orbit effective energy, not proof of an exactly periodic
finite-field orbit for every n. The actual mean torque at this order is

    <y> cross F=(chi_parallel-chi_perp)(n dot F)(n cross F).    (14)

It is generically nonzero. Since chi_perp>chi_parallel, the fast-energy term
favors perpendicular axes, but conservative dynamics does not itself relax
there. A perfectly isotropic initial distribution has zero NET torque while
individual orientations and their correlations can still evolve. A finite
external field does not leave that distribution automatically stationary.

Thus the result applies to the first-order response with retained neutral
initial data and orientation transport slow on the fast averaging window.
It does not commute without qualification with holding finite F for unlimited
time or sending a source turn-on rate to zero across the neutral sector.
The angular momenta/orientations or their phase-space distribution must remain
in the next coupled calculation; pins, collisions or a bath would be additional
physics with their own stress and work.

The minimal numerical follow-up, if requested, is a small deterministic
quadrature/BVP comparison of (3)-(4) against the half-periodic equation (1),
including its homogeneous neutral-sector census and the bounds (6)-(9).
It would not require a new cosmological fit or a large network calculation.
The actual next finite-field isotropic state must then retain its angular
transport rather than borrow the frozen scalar curve.
