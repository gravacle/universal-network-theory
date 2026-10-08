# Finite-gap shared calibration and the first static existence screen

2026-09-29. Analytical continuation of the explicitly conditional
`MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md`. No numerical science, new fit,
observational cutoff, selected reference row or frozen-file edit.

## 1. A consistent finite-R state and calibration

Use the inherited dimensionless kappa=u4=m=1 convention, a retained soft
quadrature (delta_j,w_j), one hard atom of weight beta and gap R, and

    Ws=sum_soft w_j,   Kb=Ws+beta.

The NEW macroscopic candidate has unexcited soft background and one occupied
scalar hard constitutive state of action I_b>0. It is not the complete old
coherent pulse: that pulse also contained actual soft excitation and phases.
A calibration of this named effective state must not be reported as a
reproduction of that preparation. Its action is one shared cosmic datum,
not an independently fitted galactic density function.

At zero source let e=e_R(I_b,0), p=I_b*omega-e and E=beta*e. The physical
energy-density scale and corresponding mass density are

    S_stress=gstar_SI^2/(4*pi*G*Kb),
    rho_exc_mass=S_stress*E/c^2.                            (1)

For any inherited positive reference H0, Omega_exc, Omega_Lambda, the exact
same-state calibration is

    gstar_SI=c*H0*sqrt[3*Kb*Omega_exc/(2*E)],
    DeltaU_R(S)=E*Omega_Lambda/Omega_exc,
    gs_SI=gstar_SI*S.                                      (2)

Equivalently, fixing ONE shared gstar first determines
E=3*Kb*Omega_exc*(cH0)^2/(2*gstar^2), and the unique positive zero-source
action follows from e_R(I_b,0)=E/beta. This is the same parameterization,
not an extra abundance freedom. If the exposed historical acceleration
scale is used to set gstar through the formal soft coefficient
16*Kb/(3*pi), that choice remains an exposed calibration of that coefficient;
it is not proof that the finite-gap, phase-equilibrium galaxy force equals
the old relaxed curve or reproduces an observed acceleration relation.

The finite endpoint in (2) is

    DeltaU_R(S)=sum_soft w_j[delta_j^2*y_j^2/2+3*y_j^4/4]
                    +beta[R^2*y_H^2/2+3*y_H^4/4],
    delta_j^2*y_j+y_j^3=delta_j*S,
    R^2*y_H+y_H^3=R*S.                                    (3)

It is strictly increasing from zero to infinity, because its derivative is
sum w_j delta_j*y_j+beta*R*y_H>0. Thus (2) has one positive S, not a tunable
vacuum offset. The finite hard term is NOT beta*S^2/2. At fixed S it rises
with R, with derivative beta*y_H^4/R, approaching that harmonic endpoint.
At fixed E the calibrated S decreases toward the previously studied limit.
The finite spectrum and its DeltaU are recomputed together.

The source-time scale tau_star is not fixed by this static calibration.
It remains a counted physical-clock input for omega_phys=omega/tau_star
and for the averaging/history domain. Neither a fitted radius nor an
independent vacuum adjustment is introduced by (1)-(3).

## 2. Exact zero-source static coefficients

The hard scalar orbit has turning amplitude b, r=b^2/R^2 and

    chi=e/R^4=r/2+r^2/4,
    I_b=R^3 f(r),  omega=R*Omega(r),
    cI2=I_b*e_II/omega,  0<cI2<1/3,
    w=p/e.

The original positive endpoint-safe period/action integrals determine all
these quantities, including positive e_II; none is a new fit parameter.
The exact source susceptibility deficit is

    q=1-chi_B(I_b,0)=3(e+p)/(R^4+4e)
                       =3*chi*(1+w)/(1+4*chi).               (4)

At g=0 the mixed derivative B_I vanishes by source parity. All soft ground
modes cancel their corresponding contact exactly. Consequently the common
transverse/longitudinal static Jacobian and the occupied lapse response are

    K0=beta*q >0,
    Jstatic=beta[omega^2/e_II+3*I_b*omega]
           =beta*I_b*omega*(1/cI2+3)>0,

    K0/Jstatic = 3*cI2/[(R^4+4e)(1+3*cI2)].                  (5)

The hard weight cancels from this last dimensionless ratio but remains in
the shared physical calibration. Empty I=0 copies do not receive the
occupied omega^2/e_II term. The occupied I_b>0 limit can be singular; it
must not be confused with deleting the hard population.

Equation (5) uses the static PHASE-EQUILIBRIUM response, not an independent
fluid density profile. Linearizing N*omega=mu at h=0 gives

    delta I/I_b=−Phi/cI2,   Phi=delta ln N,
    delta(E+3Pi)=−Jstatic*Phi.                              (6)

Thus weak metric alone does not imply a small density perturbation. The
linear expansion around the cosmic state also requires |Phi|/cI2 small.
If this fails, solve the nonlinear state relation in the BVP; do not
retain a nominally smooth hard component or extend (6) outside its domain.

## 3. Physical static response length, with all factors of c

In physical spatial coordinates, acceleration is c^2*grad(Phi). The
background-subtracted linear lapse equation becomes

    K0 Laplacian(Phi)+(gstar_SI^2/c^4)Jstatic*Phi
                     =4*pi*G*Kb*delta(rho_b+S_b)/c^2,       (7)

where ordinary rho_b,S_b on this line are mass-density-equivalent units.
The homogeneous vacuum was subtracted using its background equations, not
deleted from the action. Define

    kJ^2=(gstar_SI^2/c^4)*Jstatic/K0,
    ellJ=1/kJ=(c^2/gstar_SI)*sqrt(K0/Jstatic).                (8)

ellJ is the inverse STATIC response wave number; its wavelength is 2*pi*ellJ.
A Dirichlet ball's first homogeneous threshold is radius pi*ellJ. These are
not automatically a halo radius, a dynamical growth rate or a sound horizon.
If polarization were omitted while retaining the same active Jstatic,
the length would instead contain Kb. Their ratio is sqrt(K0/Kb), so ignoring
polarization can radically change this screen even when pressure is small.

Eliminating gstar with the excitation calibration (2), and writing
fH=beta/Kb, gives the exact useful common-scale identity

    (H0*ellJ/c)^2 = [2*fH/Omega_exc]
                       *chi*cI2/[(1+4*chi)(1+3*cI2)].       (9)

The scale cannot be selected independently after the cosmic state has been
fixed. In the cold limit,

    w=3chi/8+O(chi^2),  cI2=3chi/4+O(chi^2),
    K0=3*beta*chi[1+O(chi)],
    Jstatic=(4/3)*beta*R^4[1+O(chi)],
    ellJ=(3*c^2/(2*gstar_SI))*sqrt(e)/R^4[1+O(chi)],
    H0*ellJ/c=chi*sqrt[3*fH/(2*Omega_exc)]*[1+O(chi)].        (10)

At fixed calibrated E and gstar, increasing the global gap makes this
static length shrink as R^-4. The ideal hard-dust cosmological limit is
therefore not a uniform, automatically regular limit of the aligned static
galaxy branch. This is a concrete reason to test a finite gap, not a reason
to disallow the network density from clustering.

## 4. Cold history directly bounds the same static length

For the stipulated adiabatic homogeneous history, I(A)=A^3 I_b. If a
separately specified coldness requirement is w(A)<=w_c, let w(r_c)=w_c and

    x=f(r_c)/A^3.

Then f(r_b)<=x. Since f(r)>=r/2,

    chi_b<=x+x^2.                                          (11)

There is an exact useful upper bound, not merely a cold expansion.
The previously proved compression inequality is cI2<=2w/(1+w).
The time-weighted fourth moment satisfies M4(r)<=M4(0)=3/8, so

    cI2<=2w<=3r/[4(2+r)]<=3chi/4.

Inserting this into (9) yields

    H0*ellJ/c <=sqrt[3*fH/(2*Omega_exc)]*chi
              <=sqrt[3*fH/(2*Omega_exc)]*(x+x^2).             (12)

No numerical w_c, epoch or observational exclusion is selected here. The
same actual history can instead be reported at all already inherited epochs
without imposing a new success threshold. At a physically supplied early
constraint, (11)-(12) become a direct restriction on the static state; gap,
pressure history and galactic response length cannot be separately tuned.
The adiabatic/rapid-mode condition must hold over that history; (12) is not
a claim that it holds arbitrarily far back for an unspecified tau_star.

## 5. A rigorous cheap necessary-condition screen

For a specified finite matching domain with zero peculiar-potential
Dirichlet data, let lambda1>0 and v1>0 be the lowest eigenvalue/eigenfunction
of minus its Laplacian. Suppose the source in (7) is nonnegative and not
identically zero, and the proposed near-background attractive branch has
Phi<=0 everywhere. Green's identity gives

    (kJ^2-lambda1) integral v1*Phi
                         = integral v1*(ordinary source/K0)>0.

It follows necessarily that

    kJ^2<lambda1.                                         (13)

At equality the Fredholm compatibility fails for that positive source;
above it the linear solution cannot remain everywhere attractive. This is
stronger than observing that the principal part is elliptic, and introduces
no observational tolerance. For nonzero prescribed boundary data subtract
a compatible lift first; the sign theorem requires its resulting source to
have the stated sign. An arbitrary numerical box must not be substituted
for a physical matching surface or tuned to pass (13).

Failure of (13) is NOT a no-go for the nonlinear common model. It excludes
this particular small-contrast, everywhere-attractive linear branch with
those boundaries. Nonlinear predicted network concentration, another
physically specified clock/state branch or a time-dependent solution can
be the required continuation. Conversely passing (13) does not establish
the nonlinear finite-field ellipticity, branch accessibility or formation.

This screen can be calculated before a disk solve: report the exact
calibrated I_b,S,K0,Jstatic,ellJ and cI2 for every retained spectrum/reference
choice, with cold-history ratios and no selected favorable row. If a physical
matching domain is already declared, evaluate (13). Otherwise report ellJ
and the boundary dependence rather than inventing a radius cut. The same
table should expose whether the contemplated potential depth lies outside
the linear-density regime in (6).

One additional finite-field algebraic check costs no galaxy integration.
On an occupied branch continuously connected to I=0 with e_II>0 throughout
that connection, the phase frequency must exceed its empty boundary value,

    mu/N > omega0(h)=sqrt(R^2+3*y0(h)^2),
    R^2*y0+y0^3=R*h.                                      (14)

Use equality for that admissible boundary I=0, not an arbitrary clipping
rule. A disconnected convex segment beyond a finite-h softening/fold need
not obey (14); its full branch and energy comparison remain required.
For small I_b/R^3 and h/R^2, the leading continuation is

    I approximately I_b−(4R^3/3)*Phi−2h^2/R.                (15)

Thus the source-induced frequency shift can compete with the very small
intrinsic pressure shift. It must be computed from the same field and
branch, not omitted to infer clustering from (6) alone. The exact e_II and
longitudinal/transverse constitutive eigenvalues remain the subsequent
finite-field tests specified in the BVP.

## Evidence and scope

Read-source SHA-256 identities:

- `MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md`:
  `64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3`.
- `GLOBAL_HARD_GAP_SHARED_FEASIBILITY_V001.md`:
  `683bf955a6f70b39cb4a247c01c309db0580faae5b8b06acdd742ca9510bb08d`.
- `GLOBAL_GAP_LIMIT_CALIBRATION_PROTOCOL_V001.md`:
  `72c7893d1659c3143bdb968157c2f8b0bd74b703e15db4999121afdec6f00e7f`.
- `PREPARED_ACTION_COMPRESSION_DERIVATION_V001.md`:
  `4e95a23d32367941948deb088e7f192b1f5269923d216c802586376d7d950d33`.
- `HARD_MODE_COLD_HISTORY_CONSTRAINT_V001.md`:
  `c4f80c78a6af1fadb472bc6bef9d3fb54302cc9b00ef0ae728a149b70b0bf067`.

These are equations for the named conditional finite-gap macrostate. They
do not reclassify a coherent pulse as an isotropic state, fix an unowned
microscopic clock, manufacture a halo density, or assert an empirical pass.
They provide the calibrated coefficients and a necessary branch test needed
to progress to the same-parent galaxy existence calculation.
