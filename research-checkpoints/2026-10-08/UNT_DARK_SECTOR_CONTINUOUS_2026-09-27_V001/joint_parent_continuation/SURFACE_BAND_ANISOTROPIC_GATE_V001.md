# Freeze the same surface band's anisotropic source and material Hessians

2026-10-05 UTC. Prospective analytical and numerical protocol, frozen before
execution. Owned by observer_cosmography; root owns a disjoint native worker.
At most one small worker executes this protocol, with single-threaded NumPy
on this Mac. No macrohistory, likelihood, fit, installation, overwrite,
ledger edit or other job is authorized here. Root reviews the saved source
before execution. Existing proposal and all other artifacts remain unchanged.

The source anchor is SURFACE_BAND_SHARED_ACTION_PROPOSAL_V001.md. This is
one necessary new gate for that same conditional candidate, not an adopted
UNT model, a favorable replacement or a claimed observational result.

## Actual anisotropic constitutive and source choices

Retain physical surface patches and their reference material normals. For
each reference normal n choose orthonormal reference tangents E=(t1,t2),
and a reference in-plane unit direction u. Write k=Eu and

    C_t = E^T F^T F E,
    a(F,n,u) = sqrt(u^T C_t^-1 u),
    D(F,b) = d0 F^T b,
    x(F,b) = (d0/Lambda0)|F^T b|.

The source block is the same four-state singlet--triplet Hamiltonian, with
gap Delta0 a and source vector D. All its ground states, reference band
labels and mode counts are retained. The reference angular average is over
an isotropic material normal and a uniform in-plane direction; it is NOT a
newly isotropized physical-angle measure after deformation.

Conserving that census gives the full band energy

    E_band(F,b) = -B < [(a^2+x^2)^(3/2)-|x|^3]/a^2 >,
    B = V0 C0 Lambda0^3/3.

At b=0 it is -B<a>. No reference is reset with shape or volume. For stable
floating-point evaluation of the same exact formula, use

    r = sqrt(a^2+x^2),
    [(a^2+x^2)^(3/2)-|x|^3]/a^2 = r+x^2/(r+|x|).

This explicitly owns the anisotropic band dispersion, the fixed-mass
displacement port and the original gap/cutoff labels. It does not prove a
native two-dimensional carrier, that port's microscopic matrix element,
quantum ground preparation, ordinary clock/ruler calibration, full source
kinetics or the gravitational coupling. A physical surface tension remains
an independently counted amplitude. All those costs from the source anchor
are retained. Sliding, reconnection, creation or reoccupation are not added.

## Independent prospective material formulas

For F=s exp(e), with e symmetric and tracefree, let k and n be orthogonal
unit reference vectors. Expansion before angular elimination gives

    a = s^-1 [1-k.e.k+k.e^2.k-2(k.e.n)^2-(k.e.k)^2/2+...].

The isotropic orthogonal-frame moments yield

    <a> = s^-1 [1+tr(e^2)/15+...],
    <1/a> = s [1+tr(e^2)/15+...].

The full material F-Hessian at sI, including prestress, is

    A_band,ij,kl = -B/(15s^3)
       [delta_ij delta_kl+delta_ik delta_jl+6 delta_il delta_jk].

Its rank-one contraction is

    A_band:(v tensor m)^2
      = -B/(15s^3)[|v|^2|m|^2+7(v.m)^2].

Consequently, with V=V0s^3,

    p_band = -B/(3Vs),
    G_band = -B/(15Vs),
    K_band = -4B/(9Vs),
    M_band = K_band+4G_band/3 = -8B/(15Vs),
    h_band = rho_band+p_band = -4B/(3Vs).

The frozen isotropic physical area action from the anchor has

    E_area(F) = Sigma < |cof(F)n| >,
    A_area,ij,kl = Sigma/15
       [4delta_ik delta_jl-6delta_il delta_jk+4delta_ij delta_kl].

Combining that area sector, this band and a retained constant R gives

    hV = R+Sigma s^2/3-4B/(3s),
    GV = [4Sigma s^2-B/s]/15,
    MV = [2Sigma s^2-8B/s]/15.

For positive B,Sigma and R>=0, positive M is equivalent to Sigma s^3>4B
and implies positive G, h and complete energy. The transverse material
front obeys G<=h exactly when

    15Rs+Sigma s^3 >= 19B.

The longitudinal material front obeys M<=h automatically for R>=0 and
Sigma s^3>4B. These are frozen-material Hessian/inertia checks, NOT the
full acceleration-coupled internal quantum, clock or gravity front speeds.
The separate q.a kinetic gate from the anchor is not retired by them.

## Source tensor that tests a previously unchecked assumption

Take the reference critical calibration A_ref=4piG C0 d0^2 Lambda0=1.
Expanding the SAME complete band energy at b=0 gives

    chi(F) = F F^T <1/a>/det(F).

The bare quadratic field stiffness is I-chi. At F=sI, chi=I exactly,
recovering the previously derived conserved critical normalization. For
volume-preserving F=diag(exp(epsilon),exp(-epsilon),1), however,

    chi_x = 1+2epsilon+(32/15)epsilon^2+...,
    chi_y = 1-2epsilon+(32/15)epsilon^2+...,
    chi_z = 1+(2/15)epsilon^2+... .

Thus a stretched axis is prospectively supercritical already at first
order. This must be tested, not assumed away by selecting a new D(F), G(F),
identity function or physical-angle measure. If confirmed, the b=0 weak
field block has a negative bare quadratic direction, even if its material
elastic block passes. That is a failure of this candidate's source-zero
state under the declared anisotropic deformation. It is not a theorem
against every physical surface action or against UNT research.

## Frozen quadrature, steps, controls and gates

Both quadratures use float64 Gauss--Legendre normal cosine mu and uniform
azimuth phi and tangent phase psi. Set

    n=(sqrt(1-mu^2)cos(phi),sqrt(1-mu^2)sin(phi),mu),
    t1=(mu cos(phi),mu sin(phi),-sqrt(1-mu^2)),
    t2=(-sin(phi),cos(phi),0),
    k=cos(psi)t1+sin(psi)t2,
    l=-sin(psi)t1+cos(psi)t2.

Use E=(k,l), u=(1,0), which integrates the same in-plane direction census.
The normalized weights are w_mu/(2N_phi N_psi). Two independently shifted
product grids are frozen:

    low:  N_mu=8,  N_phi=16, N_psi=16,
          phi index shift=.17, psi index shift=.23 (2048 frames);
    high: N_mu=16, N_phi=32, N_psi=32,
          phi index shift=.31, psi index shift=.47 (16384 frames).

No random sampling is used. Unit, orthogonality, normalization and isotropic
second/fourth moment controls precede the constitutive checks.

Dimensionless arithmetic controls set B=V0=d0/Lambda0=1 and 4piG=1/3,
consistent with C0=3 and d0=Lambda0=1, hence A_ref=1. These are unit choices,
not a physical calibration. All-dimensional formulas above remain the
interpretation. Freeze the following finite controls:

- Isotropic stretches s=.75,1,2.
- Isotropic source magnitudes b=0,.01,.1,1,10 along a coordinate axis.
- All 81 entries of each band and area F-Hessian at the three s controls,
  and all 9 stress entries, using relative F steps .004,.002,.001.
  Centered differences are extrapolated as (4D_h/2-D_h)/3.
- Homogeneous pressure and K controls use the same centered halving steps
  in log(s). K=(E_loglog-3E_log)/(9V).
- Isochoric e=diag(epsilon,-epsilon,0), with epsilon=.02,.01,.005,
  tests both angular-series coefficients by quadratic-error extrapolation.
- Shape-source controls use epsilon=+/- .001,.002,.005,.01,.02,.05.
  Both grids evaluate chi and the eigenvalues of I-chi.
- Source Hessian directional controls use axes and normalized pairwise axis
  sums, for the undeformed state, epsilon=.02 and a fixed left rotation of
  that shape through angle .37 about (1,2,3)/sqrt(14).
  Centered source steps .004,.002,.001 are extrapolated first by
  L_h=2D_h/2-D_h to remove the |b|^3 cusp error, then by
  (4L_h/2-L_h)/3. The exact analytic tensor is the comparator.
- Combined material controls set s=B=V0=1 and (Sigma,R)=(1,0),(4,0),
  (8,0),(8,1),(19,0),(32,0). Boundary states are retained and are not
  divided by zero enthalpy. They illustrate the exact stated inequalities.

Frozen absolute/normalized tolerances: analytic identities and cross-grid
agreement 2e-11; finite-difference stress/Hessian and angular-series
coefficients 2e-7. Matrix errors are normalized by max(1,max|analytic|).
No tolerances, grids, sample points or calibration change after execution.
Every check, including any failure, is retained in the receipt.

The arithmetic pass and scientific finding are separate. Correctly
detecting negative eigenvalues verifies the numerical gate but FAILS the
candidate's anisotropic source-zero positive-stiffness requirement. No
success label may conflate these outcomes.

## Custody and resumability

The worker source hashes itself, this protocol and the source anchor before
evaluation. The exclusive new JSON receipt records those hashes, PID/PPID,
time, maximum resident memory, every check and compact complete results.
Its canonical payload hash excludes the hash field itself. The source
refuses to overwrite an existing receipt. A failed receipt is preserved.
Only the exclusively owned RESULT.md report may then be added; the receipt
and prospective protocol remain unchanged after execution.

If interrupted before a receipt exists, inspect the owned process/session
and partial artifact before deciding a rerun. No rerun is authorized merely
by a quiet chat. If the job completes, no background work or automatic
resumption is implied. Root alone reconciles the existing continuation log
and ledger with the sealed receipt and independent source review.
