# Regional expansion must obey the action's weighted budget

2026-10-05 UTC. New exact analytical identities for the declared constant-
trace, preferred-foliation, weighted Bochner one-form action. Independently
checked by internal variation review. No numerical job or fitted state.
The fixed endpoint Lambda remains separate; W(0)=0 is not changed.

Notation: Fbg=1+3beta/2>0; A_i=D_i ln N; B=L_N^-1 A;
lambda=L_N^-1 F(B); C=D_jlambda_i D^jB^i; F(B)=partial W/partial B.
All integrals use the spatial proper measure. Averages below use one
periodic preferred slice with positive lapse. Finite boundary fluxes are
shown explicitly where needed. An independent unit-vector theory is not
covered by these preferred-foliation variations.

## Exact lapse-weighted energy, including boundary work

The action's normal energy is

    rho_A=2M^2[div lambda+lambda dot B+ell^2 C-W].

Using L_N B=A and integration by parts,

    integral N rho_A/(2M^2)
      =-integral N W
       +surface_integral N[lambda_nu+ell^2 lambda^i D_nu B_i].

Thus, on a periodic slice, integral N rho_A=-2M^2 integral N W<=0 when
W>=0. This also follows by a uniform rescaling of N in the acceleration
action: A and L_N do not change, while its measure scales linearly.

This is not inconsistent with a positive UNWEIGHTED regular quadratic
energy piece. Correlations between lapse and the linear divergence term
contribute at the same order. Positive flat-wave energy cannot be inserted
as an independently assigned positive cosmological density.

Self-adjointness does not itself remove surface work. An isolated finite
galaxy/void region must supply actual auxiliary boundary conditions, a
matching exterior and the corresponding boundary action/work. An arbitrary
boundary profile is not a source-selected state or a free cosmic reservoir.

## Exact active source and its different weighting

Put

    J^i=lambda^i div B+B^i div lambda
        -lambda^j D_j B^i-B^j D_j lambda^i-D^i(lambda dot B).

The complete connection/filter stress satisfies

    rho_A+T_A=2M^2[2W-B dot F+2ell^2C
                    +N^-1 div{N(lambda+ell^2J)}].

Consequently

    integral N^2(rho_A+T_A)/(2M^2)
      =integral N^2[2W-B dot F+2ell^2C-(lambda+ell^2J)dot A]
       +surface_integral N^2(lambda+ell^2J)_nu.

For N-weighting instead, the periodic divergence integrates away and leaves
integral N(2W-B dot F+2ell^2C). N and N^2 are NOT interchangeable.
No general sign is assigned to the curved nonlinear filtered C or J terms.

## Hamiltonian, trace evolution and domain volume

Let sigma^2=sigma_ij sigma^ij, K=trace Kij and
partial_perp=N^-1(partial_t-U^iD_i). The exact local equations are

    M^2[Fbg K^2/3+R3/2-sigma^2/2-Lambda]=rho_d+rho_A,
    Fbg partial_perp K=-(rho+T)/(2M^2)+Lambda-sigma^2
                       -Fbg K^2/3+D^2N/N.

Define H_D=(1/3)d ln V_D/dt=<NK>/3, not <K>/3. On the periodic domain,

    3 addot_D/a_D=<K(partial_t-U dot D)N>+(2/3)Var(NK)
       -<N^2 sigma^2>/Fbg-<|DN|^2>/Fbg
       -<N^2(rho+T)>/(2M^2Fbg)+Lambda<N^2>/Fbg.

The time-lapse correlation is retained; fixing a convenient time coordinate
does not turn H_D into an observed Hubble rate. Null rays and conserved
dust observers use PLANAR_DUST_OBSERVER_OPTICS_V001, not a volume relabeling.

Writing <Y>_N=integral NY/integral N, the periodic weighted Hamiltonian is

    3Fbg[H_D/<N>]^2=<rho_d>_N/M^2+Lambda-<R3>_N/2
                    +<sigma^2>_N/2-(Fbg/3)Var_N(K)-2<W>_N.

This exposes the remaining physical obligations: actual curvature, shear,
lapse, ordinary matter and boundary/state selection. They cannot be replaced
by a freely chosen void fraction or an independent extra clock abundance.

## A restricted but decisive local-gradient sign

For ell=0, B=A and lambda=F(B). The acceleration-sector active source and
the integrated lapse-gradient term COMBINED become

    Fbg^-1 <N^2[2b F(b)-2W(b)-b^2]>.

If F(b)=[1-mu(b/a0)]b, W(0)=0 and mu is nonnegative/nondecreasing, then

    2bF-2W-b^2
      =2[integral_0^b mu(s/a0)s ds-mu(b/a0)b^2]
      <=-mu(b/a0)b^2<=0.

Thus this local gradient contribution cannot itself supply positive domain
acceleration. This does NOT bound the expansion-variance/time-lapse terms,
the full curved filtered completion or observer-inferred acceleration.
It is not an all-UNT no-go. Changing W's additive constant would add/change
a vacuum term and must be counted rather than hidden as an energy convention.

Next: constrain the remaining variance/shear through the SAME momentum
equation before choosing a regional realization. No longer perturbative
trajectory or optical fit is justified merely by having more stable numerics.

## Momentum constraint: variance and shear cannot be chosen independently

The following two restrictions and curved extension were independently
checked after the preceding identities. With expanding-positive K and
normal matter momentum j_i=-Pi v_i/sqrt(gamma), shift variation gives

    D_j sigma^j_i-(2Fbg/3)D_iK=-j_i/M^2.

The acceleration/filter action has no independent shift dependence. On a
flat periodic slice, N=1, j=0, each nonzero Fourier mode requires

    sigma_ij=Fbg(k_i k_j/k^2-delta_ij/3)deltaK+sigma_TT,
    <sigma^2> >= (2Fbg^2/3)Var(K).

The scalar and transverse-traceless pieces are orthogonal. Homogeneous
shear also contributes nonnegatively. Consequently the kinematic variance
contribution obeys

    Q_D=(2/3)Var(K)-<sigma^2>/Fbg
       <=(2/3)(1-Fbg)Var(K)<=0 for beta>=0.

This is an instantaneous flat-slice restriction, not a general backreaction
theorem. In particular N=1 at one instant does not establish Ndot=0.

For longitudinal momentum j_i=i k_i J, the scalar coefficient becomes
Fbg deltaK-3J/(2M^2). A physical small-velocity estimate is

    [3|J|/(2M^2)]/[Fbg|deltaK|]
      ~ (9/2)[rho_normal/(3M^2Fbg H^2)](H/p)(H/|deltaK|)|v|.

This shows the small-tilt/subhorizon suppression at low density. It is not
a rigorous bound on arbitrary density-velocity Fourier convolutions, dense
regions or momentum-carrying boundaries.

## The filtered small-lapse check has the same unfavorable sign

On a fixed flat slice with n=Nstar cos(px), f=(1+ell^2p^2)^-1,

    <N^2(rho_A+T_A)>/M^2
      =p^2 Nstar^2(f^2-2f^3)+O(Nstar^3).

This includes the lapse weighting of the linear divergence, not merely
the regular unweighted stress. Combining it with the lapse-gradient term
in the domain equation yields

    -p^2 Nstar^2(1-f)(2f^2+f+1)/(2Fbg)+O(Nstar^3).

Its quadratic part is nonpositive. This is only the specified lapse-plus-
acceleration contribution; the complete evolving geometry is not frozen by
this control, and no sign of every higher-order term is claimed.

## A constructive curvature-scale opening, not a selected solution

On a CLOSED constant-curvature slice, Ric_ij=2kappa gamma_ij, N=1, j=0,
consider an actual nonconstant Laplacian eigenmode Delta deltaK=-p^2deltaK.
The scalar shear is (D_iD_j-gamma_ij Delta/3)chi, with

    chi=-Fbg deltaK/(p^2-3kappa),
    <sigma^2>=(2Fbg^2/3)[p^2/(p^2-3kappa)]Var(K)+<sigma_TT^2>.

These follow from the momentum constraint and integrated Bochner identity.
For negative kappa, positive scalar kinematic contribution requires

    3|kappa|>(Fbg-1)p^2.

For beta=.5 this is p R_curvature<2, or wavelength>pi R_curvature.
Thus curvature-scale regional modes remain an opening; ordinary short-
wavelength clumping is not enough in this restricted state. The compact
hyperbolic geometry must actually admit the mode; a flat Fourier box does
not acquire a curvature spectrum by changing a coefficient. p=0 is the
mean, and p^2=3kappa>0 is a singular constraint case, not an allowed large
response. Finite regions add matching/boundary terms.

None of this selects a native regional state, establishes positive total
acceleration, or provides observer-inferred accelerated distances. Positive
dust density, lapse evolution, curvature evolution, ordinary mass, boundary
work and the early-universe limit must still close. Specifying a favorable
variance/curvature history independently would add the very freedom the
shared-model test is intended to avoid.

## The curvature and expansion budgets must be satisfied together

Further independent review gives, on the instantaneous N=1, A=0 slice,

    H_D^2=(rho_bar/M^2+Lambda-R_bar/2)/(3Fbg)-Q_D/6.

Positive kinematic Q_D lowers instantaneous H_D^2 at fixed ordinary density,
curvature and endpoint. Relative to the homogeneous same-density reference,

    -R_bar=6Fbg(H_D^2-H_ref^2)+Fbg Q_D.

Thus larger H_D and positive Q_D require sufficiently negative mean
curvature in this restricted slice. A positive acceleration contribution
is not an independent positive expansion-energy reservoir. Ndot remains
an evolution question even when N=1 at this instant.

There is also an exact limitation of the existing periodic plane code.
For gamma=A^2 dx^2+B^2(dy^2+dz^2),

    sqrt(gamma) R3=-4(B B_x/A)_x+2 B_x^2/A,
    R_bar=2 integral B_x^2/A / integral A B^2 >=0.

This holds at finite amplitude; pointwise negative curvature is possible,
but negative proper-volume mean curvature is not. A finite boundary retains
the surface derivative. A lapse-weighted mean instead has

    integral N sqrt(gamma) R3
      =2 integral N B_x^2/A+4 integral N_x B B_x/A,

which has no such sign. That possibility requires the actual lapse/stress
correlations, not an independently chosen curvature reservoir. The next
state test must change geometry explicitly rather than extend the plane run.
