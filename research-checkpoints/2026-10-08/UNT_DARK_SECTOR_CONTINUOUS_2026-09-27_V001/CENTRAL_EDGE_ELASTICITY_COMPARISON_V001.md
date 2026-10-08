# Conditional central-edge elasticity comparison V001

2026-09-27. Construct ID: `UNT_ELASTIC_COMPARISON_CENTRAL_EDGE_V001`.

Exploratory comparison only: a fixed-topology network embedded in three
Euclidean spatial dimensions, with actual displacement/strain and central
edge energies. This is not an adopted UNT law, a replacement for the primary
construct, an actual-parent calculation, or a numerical result. It supplies
no abundance, formation history, emergent metric or gravity law.

**Result:** edge-derived rigidity can make longitudinal and transverse
acoustic stiffness positive despite negative pressure and negative bulk
modulus. Affine acoustic stability does not establish free-volume stability,
survival of internal relaxation, a kinetic law, or relativistic causality.

## 1. Microscopic prestress and the affine result

At a reference configuration with volume V, write each edge vector as
ell_e n_e and define the energy under deformation gradient F by

    E(F)=sum_e U_e(|F ell_e n_e|),
    S=sum_e ell_e U'_e/V,       B=sum_e ell_e^2 U''_e/V.

The exact Cartesian edge-displacement Hessian is

    H_e=U''_e n_e n_e^T+(U'_e/ell_e)(I-n_e n_e^T).

The transverse term is geometric prestress; dropping it changes the result.
Assemble node Hessians through the signed edge-node incidence operator.
Force balance must be checked separately: a Hessian by itself does not
establish that the reference configuration is an equilibrium.

For affine response, assume isotropy of the relevant weighted second and
fourth direction moments. Isotropic stress alone is insufficient. The Hessian
of E(F)/V at F=I then is

    A_ijkl=(B-S)/15 (delta_ij delta_kl+delta_ik delta_jl
                    +delta_il delta_jk)
           +S/3 delta_ik delta_jl.

Uniform dilation and exactly volume-preserving simple shear give

    p=-S/3,
    K=-V dp/dV=(B-2S)/9,
    mu=(B+4S)/15.

The pressure derivative follows the same fixed-edge, affinely dilated family.
For a unit propagation direction m, the rank-one acoustic tensor is

    Q_ik=A_ijkl m_j m_l
        =mu delta_ik+2(B-S)/15 m_i m_k,
    Q_T=mu,       Q_L=K+4mu/3=(3B+2S)/15.

These are stiffnesses, not speeds. A symmetric infinitesimal-strain Hessian
without its prestress/volume corrections is not a substitute for Q.
Positive Q_T,Q_L establish isotropic rank-one strong ellipticity for this
affine continuum, not every microscopic mode or every boundary ensemble.

In particular, K<0 remains negative curvature of E(V)+p_ext V at a
stationary fixed-pressure equilibrium: d^2E/dV^2=K/V. Positive acoustic
stiffness does not resolve that uniform-volume instability. A cosmological
scale degree of freedom would require its own specified dynamics.

## 2. Homogeneous edge powers and the inertia assumption

For U_e=kappa_e ell_e^r, kappa_e>0, fixed r>0, set rho_b=E/V. Then

    p=-r rho_b/3,
    K=r(r-3)rho_b/9,
    mu=r(r+3)rho_b/15,
    Q_L=r(3r-1)rho_b/15.

Along affine dilation ell proportional to a, rho_b is proportional to
a^(r-3). The longitudinal stiffness is positive for r>1/3 even though
K<0 for 0<r<3. This explicitly derives rigidity from edges rather than
inserting a free positive shear parameter.

A Newtonian kinetic energy would supply a separately specified mass matrix.
For the following comparison only, **adopt** the relativistic elastic
inertial density rho+p, with c=1 and positive enthalpy. The wave formulas are

    c_T^2=mu/(rho+p),       c_L^2=(K+4mu/3)/(rho+p).

This is an additional physical completion, not a consequence of the static
edge Hamiltonian. See [Battye and Moss, equations 43-46](https://arxiv.org/pdf/astro-ph/0703744).
With rho=rho_b it yields:

| Edge law | w=p/rho_b | mu/rho_b | c_T^2 | c_L^2 |
| --- | --- | --- | --- | --- |
| r=1 | -1/3 | 4/15 | 2/5 | 1/5 |
| r=2 | -2/3 | 2/3 | 2 | 2 |

The stringlike r=1 shear agrees with the explicit affine isotropic string
calculation in [Battye et al., equations 11-17](https://arxiv.org/pdf/hep-th/0501244).
Quadratic edges are not membranes: the latter source obtains a different
shear response for membranes despite the same dilation exponent. The r=2
edge-only affine model has positive stiffness but fails the adopted causal
speed test. No relativistic completion is established by this comparison.

## 3. Tied rest energy: a conditional finite window

Add fixed positive rest energy M with rho_m=M/V, and require one shared
material displacement. It contributes inertia but no static elastic modulus.
For rho=rho_m+rho_b and f=rho_b/rho,

    p/rho=-rf/3,
    c_T^2=r(r+3)f/[5(3-rf)],
    c_L^2=r(3r-1)f/[5(3-rf)].

Independently moving matter cannot silently supply this inertia: its relative
modes and coupling would have to be included. Under a further, explicitly
conditional standard-Friedmann interpretation, this component accelerates
when rho+3p<0, or rf>1. For r=2 both squared speeds are 2f/(3-2f), so

    causal and accelerating:  1/2<f<=3/4.

Since rho_b/rho_m=E_b/M is proportional to a^2, this means
1<E_b/M<=3 and an available window of at most (ln 3)/2 in ln a. The lower
endpoint is open. Continued expansion of this unchanged law eventually
leaves the causal window; the calculation supplies no transition mechanism.
For r=1, adding nonnegative rest energy cannot produce acceleration under
that same conditional Friedmann criterion.

## 4. Relaxation and boundaries are decisive tests

Allowing stable internal coordinates to relax gives the quasistatic Schur
complement

    C_rel=C_aff-Xi^T H_int^+ Xi/V,

with compatible zero modes removed. If a forcing component couples to an
uncontrolled zero mode, this formula does not certify a finite relaxed
modulus. At finite frequency, internal inertia must also be retained.
Nonaffine response can therefore reduce the affine rigidity; an affine
causality bound is not a universal bound for relaxed solids. The microscopic
relaxation correction is developed in
[Zaccone and Scossa-Romano](https://arxiv.org/pdf/1102.0162).

There is an immediate finite-free-network obstruction. For the positive
homogeneous potentials above, Euler's identity gives

    sum_i x_i dot grad_i E=sum_e ell_e U'_e=rE>0

at every noncollapsed configuration. Hence a finite unpinned Euclidean
network containing only these edges cannot have all node forces zero.
Fixed graph topology alone does not prevent contraction. Adding constant
rest energy does not alter this identity. This argument does not exclude
infinite or periodic-winding networks, additional constraints/interactions,
or an explicitly evolving geometric background.

A fixed periodic cell or externally pinned boundary is a physical
restriction, not free support; dilation can require controller work.
The distinction between free-standing total stress and fixed-cell prestress
is explicit in [Bose et al., section III](https://arxiv.org/pdf/1812.00611).

## Smallest falsifiable next test and ownership

For a declared candidate cell: first verify force balance with internal nodes
unpinned; then assemble the full prestress Hessian, relax the allowed internal
coordinates, and form the acoustic problem using the declared kinetic term.
Check both longitudinal and transverse stability and speeds, with boundary
and cell work included. Failure of equilibrium or relaxed stability rejects
that candidate before any cosmological interpretation.

The inspected BS block parent supplies no adopted Cartesian displacement,
central length potential or corresponding kinetic mass/inertial mapping for
this comparison. These equations therefore cannot be run as an actual-BS
test without introducing and labeling a new physical candidate. No such
candidate was adopted, no infrastructure was changed, and no numerical
experiment was performed here.

## 5. Exact necessary bound for positive mixtures of edge powers

Root derivation, independently checked by the elasticity reviewer. This is a
bound inside the affine comparison class above, not a bound on UNT or all
elastic media. Allow a sum of fixed edge powers with nonnegative component
energies E_alpha and exponents r_alpha, and optional nonnegative tied rest
energy represented by r_0=0. Require the relevant weighted angular moments
to be isotropic for each component, one common material displacement, the
adopted relativistic inertial density, and no omitted negative binding,
reference, kinetic, source or boundary contributions to the total energy.
The powers and coefficients are fixed, not adjusted along the history.
This branch has no internal reweighting, bond creation or rearrangement during
the constitutive derivative. If occupied-link expectations are used as bond
weights, they are fixed for that derivative; an evolving quantum state needs
its additional dynamical response and cannot silently inherit these moduli.

At a given scale define positive total density rho and normalized weights

    f_alpha=E_alpha/E_total,   sum_alpha f_alpha=1,
    x=sum_alpha f_alpha r_alpha=-3p/rho,
    y=sum_alpha f_alpha r_alpha^2.

The variance identity gives

    y-x^2=sum_alpha f_alpha(r_alpha-x)^2 >= 0.

The same complete affine derivatives then give

    mu/rho=(y+3x)/15,      K/rho=(y-3x)/9,
    rho+p=rho(1-x/3),
    c_T^2=(y+3x)/[5(3-x)],
    c_L^2=(3y-x)/[5(3-x)].

These expressions do not assume constant total w during expansion: in a
mixture, the f_alpha generally evolve. On the unchanged fixed-power branch,

    d f_alpha/d ln a=f_alpha(r_alpha-x),
    d x/d ln a=y-x^2,
    d ln rho/d ln a=x-3.

Differentiating p=-rho x/3 therefore yields the displayed K, without a
constant-w shortcut. It also predicts d w/d ln a=-(y-x^2)/3<=0 on this
branch. With a finite positive mixture whose largest populated exponent is
greater than sqrt(31)-4, sufficiently continued affine expansion eventually
crosses the bound below; another stability condition may fail earlier. This
is an internal-history prediction, not an observational test or a claim that
the original microscopic network obeys this fixed-power branch.

Positive enthalpy requires x<3.
The adopted common-cone, nondispersive transverse condition c_T^2<=1 implies

    y+8x<=15.

Combining it with the variance inequality yields x^2+8x-15<=0. Hence on
the accelerating-sign branch x>1,

    1 < x <= sqrt(31)-4,
    (4-sqrt(31))/3 <= w < -1/3.

The lower w bound is approximately -0.5226. Adding tied rest mass or mixing
positive powers cannot drive this unchanged affine class toward w=-1 while
preserving that adopted wave-speed condition. Equality requires zero
exponent variance and x=sqrt(31)-4: all nonzero energy lies at that exponent,
with no positive r=0 rest contribution. It is an algebraic sharp boundary,
not a demonstrated physical network state or an empirical exclusion.

This condition is necessary, not sufficient. One must also impose

    y+3x>=0,       3y-x>=0,       3y+4x<=15,

for the remaining nonnegative-stiffness and longitudinal-speed conditions,
as well as actual force balance, valid inertia, microscopic/relaxed stability,
and the stated boundary conditions. At the algebraic equality above the
longitudinal inequalities do hold, so they do not remove that mathematical
boundary; they can exclude other mixtures inside the displayed w interval.

The limit applies to these nondispersive relativistic characteristic speeds
in their declared continuum regime. A finite-frequency phase velocity is not
automatically a fundamental signal-front speed. No general microscopic
causality theorem has been derived from an instantaneous edge potential.

Signed binding energies invalidate the nonnegative-weight step. Nonaffine
relaxation changes the affine modulus and can evade this bound; additional
fields, topology changes, noncentral interactions, different inertia or a
network-derived volume term also change the tested model. Those are specific
new mechanisms to derive and test, not permission to retune the current one.
