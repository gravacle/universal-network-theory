# Linear-source spatial-response candidate: a necessary cross-scale gate

2026-10-04. Changed effective hypothesis, selected after both qualified Solar
failures. This is an analytic compatibility calculation, not a new adopted
cosmology, physical formation calculation, or observational fit.

## Explicit change and freedoms

Replace the inherited bounded source by h(g)=g and add positive polarization
gradient energy J_delta |grad y_delta|^2/2, with
J_delta=kappa delta^2 ell^2. Retain the positive quartic mode potential and
the density nu(delta)=A delta on (0,Lambda). This adds one universal physical
length AND a spectral-dependence assumption. The source function has changed;
the old galaxy scores cannot simply be assigned to the new model. The static
deep-field normalization is inherited, a0=1.0059833281731022e-10 m/s^2, with
gc=(3 pi/8)a0. No native derivation of ell or a finite response history exists.

The original bounded-source vacuum endpoint is lost: at large uniform g,
P/Kb=(3/5)gc^(2/3)g^(1/3)+O(g^(-1/3)), and the endpoint work grows as
(9/20)Kb gc^(2/3)gs^(4/3). Sending gs to infinity is not a finite prediction
of cosmic vacuum energy. Spatial gradients vanish on homogeneous fields.
A separately selected vacuum/clock abundance would be an additional input,
not elimination of the independent expansion assumption.

## Isolated spherical equations and exact conditional bound

Put z_delta=delta y_delta, Z=(2/Lambda^2) integral delta z_delta ddelta,
a_delta=u4/(kappa delta^4). For the isolated, static, radial branch,

    -ell^2 (z_delta''+2 z_delta'/R-2 z_delta/R^2)
         +z_delta-Z+a_delta z_delta^3 = GM(R)/R^2,
    g-gN=Z.

Assume a regular finite source, isolated decay, and an existing bounded
solution. A global mode/radius maximum principle gives

    0 <= z_delta <= C = GMtot/(2 ell^2),     0 <= Delta g <= C.

At a maximum above C, the vector radial Laplacian contributes at least
2 ell^2 z/R^2, z-Z>=0, and the cubic is nonnegative, contradicting the source
bound. A negative minimum similarly contradicts the positive source. The
bound is uniform in a positive lower mode cutoff. Its continuum extension
assumes the bounded limiting solution exists; this is not an existence proof.

A required measured enhancement Delta g therefore implies
ell^2 <= GMtot/(2 Delta g). For a compact deep-field source the asymptotic
target Delta g approximately sqrt(GM a0)/R implies R >= 2 ell^2/rM.
This is a necessary amplitude condition, not a guarantee of a rotation curve.
For any exterior tracer, Delta g/gN <= R^2/(2 ell^2) on this branch.
This is not yet a comparable-mass binary or a Galactic external-field result.

## Finite-source and zero-gap Solar plateau control

For a finite spherical source the reaction-free particular solution outside
the source is z_mass=C[1-<s^2>_M/(3R^2)]; a uniform sphere gives the factor
Rstar^2/(5R^2). The true central value is zero, not C.

For each fixed mode, set L_delta=ell/sqrt(1+a_delta C^2). The full reaction
is bounded by C/L_delta^2. The regular Green representation, evaluated also
at R0=2L_delta, bounds its exterior homogeneous coefficient by C/L_delta.
Thus the fractional deficit of each mode is no larger than

    min(1, eta_star + R/L_delta + R^2/(4 L_delta^2)),
    eta_star=<s^2>_M/(3R^2).

No local-quartic-equilibrium approximation is used for the soft modes. With
x=R/ell and b=C/gc, split the normalized spectral coordinate t=(delta/Lambda)^2
at t_cut=x b. Since a_delta C^2=b^2/t^2, sqrt(1+b^2/t^2)<=1+b/t gives, for
0<x b<1,

    0 <= 1-Z/C <= min(1,
       eta_star + x + x^2/4 + x b [5/4 + log(1/(x b))]).

The dropped terms are nonnegative upper-bound slack. This controls both soft
spectral weight and hard-mode matching. It remains an ISOLATED static bound;
the Galactic external field, time dependence and a relativistic metric are
not silently included. Root checked the split-integral algebra independently
of the source reviewer. No new physical solver has been run for this parent.

## Historical observational arithmetic, fixed before evaluation

Use the Saturn J2000 mean elements a=9.53707032 AU, e=.05415060 from the
[NASA fact sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/saturnfact.html).
Use GMsolar=1.32712440018e20 m^3/s^2, AU=149597870700 m, a Julian century
36525 days, and parsec=648000 AU/pi. The source-size upper bound uses a
declared compact spherical Solar model with Rstar<=1e9 m, not a measured
density profile or a corona model. Its mass moment is bounded by Rstar^2.

An inward constant acceleration gives

    <dot varpi> = -C sqrt(1-e^2)/(n a),    n=sqrt(GM/a^3).

Use [Fienga et al. INPOP15a Table 1](https://arxiv.org/html/1601.00947v1):
C1 has Saturn interval 1.2 +/- 5.0 mas/century; C2 .05 +/- .20.
C1 is the primary historical benchmark; C2 is a separately reported sensitivity
to their residual-acceptance criterion. These are NOT Gaussian sigma values,
independent datasets, or a current strongest bound. Do not average them.
For an inward anomaly their negative endpoints give acceleration ceilings;
the constant-plateau approximation yields a conditional lower length.
Full ephemeris refitting and external-field predictions remain required.
The new arithmetic does not reuse the Cassini quadrupole uncertainty as a
monopole bound. Planetary inferred precession is not a raw acceleration datum.

Report three round length illustrations, ell=1,10,100 pc, with plateau and
precession errors bounded at peri/aphelion. A uniform bound epsilon on the
force's relative deviation gives a conservative relative precession error
<=epsilon/e by Gauss averaging. No scenario is fitted or selected as the model.

For scale comparison ONLY, report three declared compact baryonic benchmarks
(M/Msolar,R/kpc)=(1e7,2),(1e9,10),(1e11,50). Their target is the explicitly
adopted deep-field total acceleration sqrt(GM a0)/R, minus gN. They are not
observed galaxies and must not be scored as successful predictions. Compute
the necessary upper length and rM/R; a nonempty formal interval is feasibility
of this gate only, not simultaneous Solar/galaxy validation.

The associated short standard-library script will save exclusive output,
source/protocol hashes, all input values and elementary identity checks.
No new fit, PDE solve, external-data download or tolerance tuning is involved.

## Next physical decision

If even the necessary window is empty, this shared length is unpromising in
the declared regime. If nonempty, derive the external-field response from this
new action and its validity bounds before a bounded numerical prediction;
then test the same fixed length against an unused observable. Do not launch
a blind length sweep. A healthy photon/clock completion, native scale/state
bridge and shared expansion mechanism remain indispensable separate work.
