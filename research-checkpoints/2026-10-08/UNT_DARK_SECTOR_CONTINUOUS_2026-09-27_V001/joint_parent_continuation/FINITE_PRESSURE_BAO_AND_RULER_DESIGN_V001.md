# Same-state finite-pressure expansion and acoustic-ruler decision

2026-09-29. Prospective continuation of the adopted scalar alpha-one action,
not a native metric/photon derivation. No numerical producer was run for this
note. Preserve every BBN inverse point and all five reference backgrounds;
do not select a point using BAO or rename the exposed data as a holdout.

## 1. Exact reduction: four source copies, one homogeneous history

At zero source the declared scalar current gives I(A)=A^3 I1 exactly, where
A=a^-1=1+z. This is an equation of the adopted fluid action; it does not prove
that native microscopic phases remain adiabatic or isotropize. The quadratic
plus quartic mode has e_R=R^2 b^2/2+b^4/4 and p=I omega-e. With the inverse's
unchanged definitions,

    L=3 Kb(c Hcal)^2/(2 gstar^2), E1=L Omega_exc, e1=E1/beta,
    I1=[Delta fnu L Omega_gamma/(beta C4)]^(3/4),
    I1/e1^(3/4)=[Delta fnu Omega_gamma/(C4 Omega_exc)]^(3/4).       (1)

Consequently the normalized history e(A)/e1, w(A), cI2(A) is independent of
the four soft-spectrum/quadrature copies at fixed (omega_b,Delta,background).
Their physical R,S,gstar, local reaction and galaxy predictions are NOT
identical. Compute homogeneous histories once, retain all 1,340 state labels
and their mapping to the 335 distinct inverse point/background combinations.
These are the entire saved 67-point census, not a new posterior sample.

For positive finite R put r=b^2/R^2. A universal positive quadrature gives

    f(r)=I/R^3=(2/pi)r integral_0^(pi/2) cos^2 t sqrt(q) dt,
    q=1+(r/2)(1+sin^2 t), J=integral q^-1/2 dt,
    omega/R=Omega=pi/(2J), f'=(1+r)/(2 Omega),
    e/R^4=r/2+r^2/4, p/R^4=(r^2/4)<sin^4 t>_(q^-1/2),
    cI2=f Omega integral[(1+sin^2 t)q^-3/2]dt/[2J(1+r)].          (2)

Solve f(r(A))=A^3 f(r1). This is unique. An efficient exact change of
integration variable is t=log(r/r1): log A=[t+log((f/r)/(f1/r1))]/3 and
d log A/dt=r f'/(3f). Its derivative lies between 1/3 and 1/2, so the
endpoint bracket is 2 log A <= t <= 3 log A. No cosmological ODE is required.
The Delta=0 inverse row is the separately retained R->infinity dust limit,
not a finite empty state. For it e(A)/e1=A^3 and cI2=0 exactly.

Exact controls and interpretation:

    A^3 <= e(A)/e1 <= A^4,
    d log[e(A)/(e1 A^3)]/d log A=3w(A),
    d log e_R(A^3 I1)/d log R|e1=4[w1-w(A)]/(1+w1)<=0.           (3)

The last equality includes recalibration of I1 at fixed present energy. A
larger gap therefore lowers the past energy and H, and increases a sound
horizon at a FIXED endpoint. It does not predict the endpoint's shift.

## 2. One explicitly imported ordinary-radiation history

Retain the reference physical dust/vacuum coefficients, not just their sum:

    H(A)^2/Hcal^2 = Omega_b A^3 + Omega_exc e(A)/e1
                  +Omega_Lambda+Omega_gamma(1+fnu*3.044)A^4.    (4)

Omega_b=omega_b/(Hcal/100)^2 and Omega_exc=Omega_m-Omega_b.
T0=2.72548 K and Omega_gamma remain the saved photon receipt. The 3.044
massless ordinary-neutrino convention is the declared late, post-annihilation
reference associated with the pinned PRIMAT interface, not an independently
measured low-redshift neutrino density. No neutrino mass is inferred here.
Equation (4) is used only through A_cut=10^7, a declared post-annihilation
thermal approximation. It is not the PRIMAT fixed-heating proxy through
annihilation, nor a recomputation of altered neutrino decoupling. The inverse
Delta labels specify the SAME conserved scalar state, not an additional
radiation species on top of it.

With these physical coefficients H(1)/Hcal=sqrt(1+Omega_r). Do not subtract
Omega_r from the matched vacuum or describe Hcal as the radiation-completed
present rate. Preserve the old radiation-omitted comparator separately.

## 3. Closed BAO shape test; acoustic endpoint still exposed

Use the same pinned DESI DR2 13-vector and full covariance as
DESI_BAO_SHAPE_PROTOCOL_V001.md. The last pair at z=2.33 is DH,DM. The data,
old scores and comparator have already been exposed. These are template-
inferred distances, not model-independent raw observations. At each retained
state compute dM=integral dz/(H/Hcal), dH=Hcal/H,
dV=(z dM^2 dH)^(1/3), and profile ONLY

    B=max[0,(d^T C^-1 y)/(d^T C^-1 d)]=c/(Hcal r_drag).          (5)

No refit of Omega_m, omega_b, R, galaxy density, temperature or helium is
allowed in this follow-on. B is one exposed nuisance per conditional point,
not a ruler prediction. Keep all component residuals and the matched
same-background dust/ordinary-radiation comparator; the old zero-radiation
score remains a historical control, not overwritten.

For ordinary tightly coupled photons/baryons, independently of hard cI2,

    Rb(A)=3 Omega_b/(4 Omega_gamma A),
    r_gamma(A_d)=c integral_(A_d)^infinity dA/[H sqrt(3(1+Rb))],
    r_H(A)=c integral_A^infinity sqrt(cI2) dA/H.                (6)

The latter is the hard fluid's propagation-scale interface, not a Jeans or
CMB transfer function. Save both at A={1,11,101,501,1101,3001,10001}; also
save the descriptive w={.01,.1,.3} crossings, without interpreting those
thresholds as data or acceptance criteria. Report crossings outside the
integrated domain rather than extrapolating a thermal history.

Invert r_gamma(A_req)=c/(Hcal B) only as a REQUIRED drag epoch. Because the
early tail is bounded rather than invented, return an allowed A_req interval,
or a precise outside-domain status. This question is useful before atomic
evolution: what endpoint would the exposed BAO scale require of the SAME
state? It is not a prediction or test of actual recombination.

For A>=A_cut, positive ordinary energy and the retained scalar give
H^2/Hcal^2 >= Omega_b A^3+q4 A^4, q4=Delta fnu Omega_gamma. Both sound speeds
are <=c/sqrt(3). Therefore an omitted tail is between zero and

    2c/[sqrt(3)Hcal A_cut
        (sqrt(q4+Omega_b/A_cut)+sqrt(q4))].                    (7)

The hard dust lower bound gives the additional upper bound
2c/[sqrt(3)Hcal sqrt(Omega_m A_cut)]; take the smaller. For Delta=0 the hard
sound tail is exactly zero. These bounds require the adopted scalar/current
and conserved baryons to persist; no native ultraviolet completion follows.
They avoid extending a^-4 photons through electron annihilation silently.

## 4. Shortest route from required to predicted ruler

A targeted project filename/content inventory found no resident HyRec,
Recfast or other atomic recombination implementation. A concrete public
route exists: the authors' [HYREC-2 repository](https://github.com/nanoomlee/HYREC-2)
contains standalone C and atomic tables. Its
[history.c](https://raw.githubusercontent.com/nanoomlee/HYREC-2/master/history.c)
accepts a supplied H(z) array in rec_build_history; the stock command instead
uses its internal standard background. Supply our qualified H in s^-1 via a
tiny separate driver. Retain the authors' source/data unchanged except an
explicit local build variant selecting FULL. Do not run the stock executable
or insert our energy as standard CDM. The default SWIFT correction is fitted
around a restricted standard-cosmology region; its
[methods paper](https://arxiv.org/abs/2007.14114v2) does not qualify arbitrary
new H(z). FULL is the justified first external calculation here.

Before that distinct run, pin one upstream commit and source receipt: five
C/header pairs hyrectools, helium, hydrogen, history, energy_injection;
Alpha_inf.dat, R_inf.dat, two_photon_tables.dat and fit_swift.dat (the allocator
loads the latter even in FULL); README/readme and input example for provenance.
The published build uses a C compiler and libm, not SciPy or a package install.
The existing /usr/bin/clang path was found without executing the compiler;
no download, compilation, installation or producer execution was performed.
The README explicitly invites compilation and scientific use/citation; no
separate license text was visible in the inspected repository listing or
source headers, and the web PDF fetch failed. Preserve that unresolved
redistribution/license metadata; do not invent an open-source license.

This is the standalone authors' history interface, NOT the present
[CLASS HyRec wrapper](https://raw.githubusercontent.com/lesgourg/class_public/master/external/HyRec2020/wrap_hyrec.c),
which explicitly rejects FULL. The compile-time MODEL must be FULL before
allocation, since it changes the radiative-transfer storage and timestep.
The external array contract in the inspected history.c is Nz entries at
z_i=i*zmax/Nz; it is not the logarithmic output grid and not an arbitrary
background table. Its interpolation refuses queries outside the covered
range. Check the actual first/last requested z and all range guards against
the pinned revision before execution, and refine this H grid independently.
Initialize every ordinary/injection field even when its physical injection
is zero; do not assume the malloc'ed parameter structure is zero-filled.

Required driver inputs are this H(z), omega_b,T0, atomic helium mass fraction,
zero extra energy injection, and fixed atomic constants. The BBN score uses
the table's nucleon YpBBN column, whereas HyRec's nH0/fHe conversion uses the
atomic mass convention. Read the existing table's atomic column3 at the SAME
inverse point; do not substitute column4 unannounced. Validate H-array grid,
units and interpolation independently; test the source's standard reference,
FULL timestep refinement and supplied/internal same-H agreement before new
rulers. Retain atomic-table range errors rather than extrapolating them.

From ne(z), determine the drag depth

    tau_drag(z)=integral_0^z c sigmaT ne(z') /
                         [(1+z')H(z')Rb(z')] dz', tau_drag(z_d)=1. (8)

This is the [CLASS thermodynamics source](https://raw.githubusercontent.com/lesgourg/class_public/master/source/thermodynamics.c)
convention. Thomson visibility, its peak, and photon optical-depth unity are
different endpoints. A low-redshift reionization convention or explicit
small-tail bound is also needed for (8). Once z_d and r_drag are qualified,
remove B from (5) and score the predicted 13-vector without a ruler fit.

## 5. What this does and does not decide

The [DESI analysis](https://arxiv.org/html/2503.14738v3) defines BAO distances
relative to the drag ruler. Its standard early-universe ruler fitting formula
is not reused for this new history. Nor are z=1101 or 147 Mpc imposed.
The present calculation tests finite-pressure late shape and supplies a
specific atomic endpoint demand. The next local HyRec adapter closes the
ordinary-physics ruler, conditional on the declared thermal/neutrino history
and BBN-proxy helium; it does not retroactively qualify exact scalar BBN.

Root's FINITE_GAP_CMB_PERTURBATION_DISCRIMINATOR_V001.md supplies the separate
Q=0 hard-fluid perturbation equations. Primordial mode/cross-correlations,
ordinary neutrino stress, photon/baryon collisions, recombination and
projection are still required for spectra. No constant free-streaming or
constant-fluid Neff posterior is imported. A homogeneous sound horizon is
not a CMB fit, and this conventional-photon branch does not produce or explain
the photons in the separate continuous-network thermal-origin proposals.
