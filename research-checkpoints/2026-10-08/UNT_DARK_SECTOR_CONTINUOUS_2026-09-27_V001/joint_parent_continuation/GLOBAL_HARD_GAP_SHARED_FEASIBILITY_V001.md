# One shared hard gap: an exact joint feasible region, not separate fits

2026-09-29. Analytical continuation of the cold-history, radiation-asymptote,
high-gap pulse and shared-calibration results. No new numerical state, gap,
fit, propagation or modification of saved evidence. The conclusion is
constructive: the conditional parent has a nonempty large-gap design limit
for finite-duration cold history and an arbitrarily small **positive
asymptotic radiation-coefficient budget**, subject to its owned source and
clock conditions. Its force curve and vacuum are then consequences of the
same choices, not two additional adjustable functions.

This is a proposed global spectral/preparation family, not a native BS gap
derivation or a completed galaxy/FLRW solution. All eighteen inherited
reference/BBN alternatives remain separate conditional rows. Requiring one
design to satisfy their intersection is an optional, explicitly stronger
robustness criterion, not a reason to discard any row.

## 1. State the budget and close the same two shared scales

Retain the fixed soft measure and hard weight beta (the old pulse design
uses beta=.005), one global hard gap R, and Kb=Ws+beta. In the existing
m=u=kappa=1 units, let the actual present state have soft actions I_s and
hard action I_H. Define

    E1=Es+EH,  EH=beta e_R(I_H),
    Qrad=Qs+C beta I_H^(4/3),
    C=[pi/B(1/4,3/2)]^(4/3).

Qrad is the quartic early coefficient, NOT the vacuum endpoint. The latter is

    DeltaU_R(S)=Qvac,s(S)+beta[R^2 ys^2/2+3ys^4/4],
    R^2 ys+ys^3=R S.                                      (1)

For each inherited reference j, the same-state calibration is

    gstar_j=c H0_j sqrt[3 Kb Omega_exc,j/(2 E1)],
    DeltaU_R(S_j)=E1 Omega_Lambda,j/Omega_exc,j.            (2)

Positive E1, Omega_exc and Omega_Lambda give a unique positive S_j. No
abundance or vacuum offset remains free after the state and spectrum are
specified. At fixed E1 and fixed S,

    partial_R DeltaU_R(S)=beta ys^4/R >0,

by the minimum-energy envelope theorem and its stationary root. Thus S_j
decreases as R increases at fixed owned energy, approaching the unique root

    Qvac,s(S_infinity)+beta S_infinity^2/2
                       =E1 Omega_Lambda,j/Omega_exc,j.    (3)

Changing a fixed weight's gap does not change Kb, but DOES change this vacuum
endpoint; (1)-(3) keep that change rather than compensating it away.

Let a declared allowed extra asymptotic coefficient be B_j>0 in present
critical-density units. It could later be obtained from an independently
specified early-universe analysis, or defined as b_j times a radiation
reference, but b_j=1 is NOT chosen here and photon equality is NOT an
observational cutoff. The exact inequality is

    Omega_exc,j Qrad/E1 <= B_j.                          (4)

Any use at an actual epoch also needs the action/clock and state assumptions.
The saved photon ratios alone do not supply this budget.

## 2. Fixed owned EH gives two compatible one-dimensional gap conditions

First consider a design that specifies EH>0 independently of R, with fixed
beta and a fixed soft state. This is NOT the same operation as moving the
gap of one stored pulse while pretending its action and energy stay fixed.
With e1=EH/beta, put

    r1(R)=sqrt(1+4 e1/R^4)-1,
    epsilon(r)=r/2+r^2/4,
    I_H(R)=R^3 f(r1),
    f(r)=(2/pi)r integral cos^2(theta)
                    sqrt[1+r(1+sin^2(theta))/2] dtheta.

The integral is from zero to pi/2. For a declared cold threshold
0<w_c<1/3 and finite A_c, let w(r_c)=w_c and
r_req=f^(-1)[f(r_c)/A_c^3]. The hard population remains cold throughout
1<=A<=A_c exactly when

    R >= R_cold=[EH/(beta epsilon(r_req))]^(1/4).        (5)

The hard coefficient QH(R)=C beta I_H(R)^(4/3) decreases strictly with R:

    d ln QH/d ln R=-(4/3)(1-3w1)/(1+w1),
    QH/EH ~ C[EH/(beta R^4)]^(1/3).                     (6)

Consequently (4) adds another monotone lower-gap condition, with available
hard budget

    QH(R) <= B_j E1/Omega_exc,j - Qs.                   (7)

If its right side is strictly positive, a sufficiently large finite R meets
it. If it is zero or negative, no finite excited hard gap meets it. This is
the fixed soft population's irreducible radiation coefficient, not a failure
of global calibration. No soft mode may be dropped from Qs merely because
its present energy is small. Equations (5) and (7), with R>1, have a common
solution whenever that residual budget is positive. A finite microscopic
maximum R would convert this into a genuine bounded feasible-region test.

The exact finite-A hard energy is

    EH(A;R)=beta R^4 epsilon(f^(-1)[A^3 f(r1)]).         (8)

It decreases with R at fixed present EH. In fact envelope differentiation
at fixed action, followed by the fixed-e1 initial-action derivative, gives

    d ln EH(A;R)/d ln R=4[w1-wA]/(1+w1) <=0.            (9)

Both wA and the hard pressure decrease with R, and EH(A) approaches EH A^3.
For total coldness, however, use the actual inequality

    [Ps(A)+PH(A;R)]/[Es(A)+EH(A;R)] <=w_c.              (10)

One must not infer monotonicity of this mixed ratio solely from the hard
mode: its changing energy weight also changes how it dilutes soft pressure.
A strict large-R sufficient condition is
Ps(A_c)/[Es(A_c)+EH A_c^3]<w_c. In fact endpoint coldness suffices for the
ENTIRE fixed-design history here. If x_i=E_i/E and w=sum x_i w_i, then

    d w/d ln A=sum x_i d w_i/d ln A+3 Var_x(w_i)>=0,

because dE_i/d ln A=3E_i(1+w_i) and every scalar quartic w_i increases
under compression. This does not imply monotonicity in the redesign
parameter R for a mixed state. Alternatively require each component cold.
There is no per-radius action or independently chosen pressure in this test.

## 3. A finite-epoch radiation budget is not a budget on all cold matter

The same positive zero-source parent obeys dE/d ln A=3(E+P), P>=0. Therefore

    E(A)>=A^3 E1,
    Omega_exc,j E(A)/(E1 A^4) >= Omega_exc,j/A.          (11)

Even an arbitrarily hard perfectly cold component has this finite-A total
energy floor. Calling the entire left side 'extra radiation' and bounding it
by photon equality would incorrectly count ordinary matter-like energy as
radiation. A genuinely specified finite-epoch TOTAL density budget must allow
this floor. A budget on the departure from the calibrated dust reference is
instead applied to

    DeltaOmega(A)=Omega_exc,j [E(A)/(E1 A^4)-1/A]>=0.    (12)

Both this excess and the pressure tend to zero in the purely hard large-R
limit at every FIXED finite A. The formal asymptote in (4) concerns the later
backward quartic regime. These distinct comparisons must not be interchanged.
For an actual early expansion constraint retain photons, baryons, other
species and their perturbations with their owned energy/clock assumptions.

## 4. One actual common pulse has a nonempty controlled design limit

Keep the original common pulse form, fixed beta, integer n and positive Hp:

    h(t)=Hp sin^2(pi t/T) cos(Rt),  T=2pi n/R,

starting every scalar mode at rest and returning h to zero. This is ONE
source acting on the entire measure, not an assigned abundance per mode.
Write tau=Rt and y_H=(Hp/R)Y. Its exact hard equation is

    Y''+Y+(Hp^2/R^4)Y^3=sin^2[tau/(2n)] cos(tau),
    0<=tau<=2pi n.                                      (13)

Continuous dependence on this compact time interval proves the R->infinity
linear limit at fixed n,Hp. Its actual endpoint energy therefore tends to

    EH,infinity=beta Cp Hp^2,  Cp=pi^2 n^2/8.            (14)

The soft equations on the same tau interval have coefficients delta^2/R^2
and shrinking forced displacement; their endpoint energies/actions tend
uniformly to zero on the fixed finite soft band. For example set
y_delta=delta Hp Z/R^2: then
Z''+(delta/R)^2 Z+(delta^2 Hp^2/R^6)Z^3 equals the bounded right side of
(13). Z,Z' stay bounded on this fixed interval, so the soft energy vanishes.
The stronger published off-resonant formula is a linear estimate, not needed
as an exact nonlinear bound for this limit. A finite design still needs its
actual pulse output and conserved source-work ledger.

Thus the complete actual pulse family, not a retained old state with its gap
relabeled, has Qrad/E1->0 and P(A)/E(A)->0 for every fixed finite A. Unlike
the fixed-soft-state experiment in section 2, it has no unchanged Qs floor.
Any strictly positive asymptotic budget and finite cold-history interval can
be met parametrically by a sufficiently large R, IF the same matched source
is realizable and the averaging/clock domain is owned. This is not uniform
in unbounded A: every fixed finite occupied quartic spectrum eventually heats.

The bounded-source gate is substantive. h can be realized by
G=h/sqrt(1-h^2/S_j^2) only if Hp<S_j. Its large-R sufficient condition follows
without a fit: since Qvac,s(Hp)+beta Hp^2/2 < Kb Hp^2/2,

    beta Cp (Omega_Lambda,j/Omega_exc,j)>Kb/2            (15)

puts the target in (3) strictly above its value at S=Hp, ensuring
S_infinity>Hp. Strictness gives a margin for large finite R. This condition
must be evaluated for every retained reference, not asserted from a selected
one. If (15) fails it is only the simple sufficient certificate that fails;
the exact inequality using Qvac,s still decides source realizability.

All positive endpoint excitation is paid source work. The pulse time decreases
as 1/R, so supplying finite energy requires increasing power and bandwidth.
No controller capability, native unbounded gap or cosmological production
history follows from this parametric construction. The coherent pulse is
still not an isotropic phase population: any replica/phase preparation and
its subsequent evolution must remain explicit rather than being reset.

## 5. The same design predicts its weak-field law; it cannot retain any curve

For the retained scalar action state the local conditional constitutive law is

    gN=gstar_j D_I(G;S_j),  G=g/gstar_j,
    D_I=G-h'_S(G)[Bs,I(h)+beta R<y_H>_(I_H,h)]/Kb,
    h_S(G)=G/sqrt[1+(G/S_j)^2].                           (16)

The exact scalar zero-field contact deficit is

    mu0=[sum_soft w q_delta+beta q_H]/Kb,
    q_H=3(eH+pH)/(R^4+4eH).

At fixed EH, its hard contribution is approximately 3EH/(Kb R^4); the fixed
soft state's contribution cannot be tuned away by R. A selected isotropic
vector ensemble instead uses the separately derived transverse plus
longitudinal response. It is not legitimate to put the scalar coefficient
into that vector state by declaration. Neither local coefficient by itself
solves the coupled metric/source/clock problem.

For the common-pulse large-R limit with vanishing soft actions, (16) becomes

    D_infinity=G-h'_S[Bs,relaxed(h)+beta h]/Kb.            (17)

Here gstar_j and S_j are already fixed by (2)-(3) with (14). There is no
remaining response amplitude or vacuum subtraction. The infinite relaxed
soft band has deficit 3pi*Asoft*h^2/16. Its excluded upper tail delta>1
is Asoft*h^3/2+O(h^5), so in the ordered zero-lower-cutoff, small-G limit,

    D_infinity=G^2/a0dim+[2/S_j^2-Asoft/(2Kb)]G^3
                                  +O(G^4),
    a0dim=16 Kb/(3pi Asoft),  Asoft=1.                   (18)

The negative cubic term is the inherited upper spectral cutoff, not an
adjustable cancellation of the bounded-source correction. Equation (18)
uses fixed positive S_j. At finite epsilon the removed lower-band deficit
adds a nonpositive remainder whose magnitude is at most
Asoft*epsilon^2*h*h'/(2Kb); this is small relative to the quadratic term
only in the nonuniform window epsilon^2<<h. For quadratic dominance require
epsilon^2<<G<<1, G<<S_j and G<<S_j^2/(2a0dim), keeping both cubic sources
small individually rather than relying on a cancellation. At finite R the
exact law (16) also retains the hard relaxed correction of order
beta*h'*h^3/(Kb R^4) and its excitation-dependent response.

The physical candidate acceleration scale a0dim*gstar_j exists only over
that window. Raising gstar or shrinking S can narrow it; taking a fixed
cutoff's strict G->0 limit is not a flat-rotation prediction.

A transparent future shared inference may calibrate ONE global preparation
scale Hp using a specified independent galactic observable, with every
reference's equations (1)-(2) recomputed. It then predicts the whole finite-
field shape, other galaxies, homogeneous pressure/dilution and the radiation
coefficient using those same parameters. R must meet (5)-(7) or the actual
pulse equivalents, not independently set a cosmic abundance. No such fit or
calibration is performed here. The complete saved states remain unchanged;
all eighteen references remain in the prospective test rather than being
ranked by agreement.

## Exact next solving target

The useful next problem is the finite-dimensional intersection of (1)-(4),
the actual common-pulse state map, the finite-A coldness/budget inequalities,
Hp<S, and a declared physical field/clock window. It is not a new freely
fitted force curve. The input budget, actual source bandwidth/maximum gap,
phase/orientation state and physical clock mapping are not supplied by the
existing output. With these still symbolic, the equations above give an
exact feasible-region specification and a constructive limiting certificate,
not a declaration that the saved six pulses already satisfy the new region.
