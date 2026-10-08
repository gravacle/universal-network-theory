# Intrinsic bond rigidity from the declared nonuniform strain law

2026-10-05 UTC. Prospective bounded constitutive test, frozen before its
numerical worker. A new isotropic physical-bond geometry postulate; not a
native graph derivation, Bose model, observed fit, occupation prescription,
galaxy calculation or cosmological history. The root separately owns the
scalar kinetic/Coulomb energy and relativistic-rest-energy gates.

## Owned construction and scope

Retain a fixed material bond inventory with uniformly distributed reference
unit directions n on the sphere. For a physical material deformation F,
C=F^T F, J=det F>0, V=V0 J, and one complete per-reference-cell energy,

    E(F)=Eref+T0 <(n.C.n)^-1-2(n.C.n)^-1/2>_sphere,
    T0>0, V0>0, Eref constant under this declared deformation.

The two bond terms implement the NEW counted s^-2 kinetic and s^-1 Coulomb
scaling, with U0=-2T0 at the unstrained reference. The fixed material shape
is essential: unconstrained Coulomb ground-state dilation need not have this
volume work. The energy is clamped in its retained material configuration;
full quantum/modal relaxation would require its own state derivatives.
Directions describe geometry, not freely populated modes or halo records.

T0=V0=1 and Eref=2 are ARITHMETIC units for this check, not physical
calibrations. The constant changes no rigidity derivative. It is retained
in every energy evaluation and is not subtracted to obtain a desired sign.
All gravity/source contacts, modal matching, operational probes, formation,
coupled characteristics and any normalization from this energy to the
galaxy law remain unresolved. No old static/optical qualification transfers.

## Exact prestressed derivatives to test

Put h(x)=x^-1-2x^-1/2. At F=s I,

    h'=(s-1)/s^4, h''=(4-3s)/(2s^6),
    E=Eref+T0(s^-2-2s^-1),
    p=2T0(1-s)/(3V0 s^5),
    B=-V dp/dV=2T0(5-4s)/(9V0 s^5).

The material Hessian is

    A_iA,jB=T0 <4h'' (Fn)_i(Fn)_j n_A n_B
                        +2h' delta_ij n_A n_B>.

The second term is the prestress contribution and MUST remain. For unit
material wave covector m and polarization a,

    A:(a tensor m)^2 = T0/s^4 *
      [2(2s-1)|a|^2|m|^2/15+4(4-3s)(a.m)^2/15].

Using physical incremental gradient deltaF F^-1, its moduli are

    G=2T0(2s-1)/(15V0 s^5),
    M=2T0(7-4s)/(15V0 s^5)=B+4G/3.

G is independently the energy curvature of compatible, EXACTLY
volume-preserving simple shear F=s(I+gamma e1 tensor e2). Strong
ellipticity requires G>0 AND M>0, exactly 1/2<s<7/4. Bulk positivity
requires s<5/4. At the two exact acoustic endpoints the zero mode is
classified as marginal, without an arithmetic tolerance altering the sign.
This material Hessian tests spatial strong ellipticity, not relativistic
inertia, a photon-cone bound, healthy coupled gravity or cosmic stability.

## Frozen worker and gates

One tiny, single-thread local NumPy worker owned by observer_cosmography.
No other jobs, old drivers, installs, schedulers or remote execution.
Use s=[.4,.5,.75,1,1.2,1.25,1.5,1.75,2]. These fixed development controls
test both sides of the derived boundaries; none is a fitted state.

Sphere grids: Gauss-Legendre mu orders12,24, each with equally spaced
azimuth counts24,48. Compare normalization, second/fourth angular moments,
isotropic energy, stress, full81-component Hessian, transverse/longitudinal
rank-one forms, physical G/M/B identity and objectivity under a fixed proper
rotation of angle.37. Normalize errors by max(1,abs analytic,abs numeric),
with limit1e-11 for quadrature/analytic controls.

Independently finite-difference the COMPLETE energy for six fixed rank-one
directions, with epsilon/s=[.01,.005,.0025]. Keep determinant-positive
deformations and use two successive Richardson extrapolations. The final
normalized Hessian error gate is2e-7. Apply the same steps to exact simple
shear and its constant determinant, and to a log-volume derivative for B.
Save every error and exact sign separately; a numerical gate is not a
scientific acceptance threshold. No step search or tolerance change.

Freeze this protocol and source before execution. Record their SHA256 plus
the read-only source-anchor SHA values in an exclusive new canonical JSON
receipt. Refuse any existing result. A passing worker means ARITHMETIC
QUALIFIED PENDING ROOT REVIEW. Root must review source and interpretation
before any qualification report; failures and partial receipts stay intact.

## Resident distinctions

POLARIZATION_GENERATED_RIGIDITY_V001 already retires its local A2-generated
smooth static central realization. This construction supplies intrinsic
material bond rigidity even where polarization vanishes and does not rerun
that operator. Native amplitude/phase hopping and strain proposals motivate
retaining material geometry, but do not derive this sphere measure or its
gravitational dictionary. Positive bond rigidity does not repair the root's
NR-rest-energy acceleration bound or select cosmic prestress.

Read anchors: POLARIZATION_GENERATED_RIGIDITY_V001.md;
GALACTIC_SMOOTHNESS_AND_COLD_HISTORY_CONSTRAINT_V001.md;
NATIVE_SINGLE_LINK_STRAIN_COMPLETION_PROPOSAL_V001.md;
HOMOTHETY_COMPRESSION_RESPONSE_V001.md.
