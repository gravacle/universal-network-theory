# Planar clock stress and conserved dust: the quadratic source budget

2026-10-05 UTC. Same explicit effective action as
COVARIANT_ONEFORM_CLOCK_V001.md. Independent algebra checks completed for
the filter stress, geometry, cubic acceleration action and canonical dust.
These are not a graph-native derivation or observational verification.

## Corrected return-filter check

An internal review initially substituted lambda1=B1. That substitution is
WRONG and its resulting quadratic wave stresses are withdrawn. The exact
auxiliary equations require B1=f A1 and lambda1=f B1=f^2 A1. The error was
caught before a new numerical run; it did not change the saved exact dust
transfer or short transient, which already use the return filter.

For gamma=mathcalA^2 dx^2+mathcalB^2(dy^2+dz^2), define proper derivative
prime=mathcalA^-1 partial_x, h=(ln mathcalB)', aN=(ln N)', b=B_x/mathcalA,
l=lambda_x/mathcalA, P=lb, C=l'b'+2h^2lb and

    L=2W(b)+2l(aN-b)-2ell^2 C.
    b-ell^2[b''+(aN+2h)b'-2h^2b]=aN,
    l-ell^2[l''+(aN+2h)l'-2h^2l]=F(b).

The exact mixed spatial stresses and normal lapse energy are

    Tx/M^2=L-2bF-4l(aN-b)+8ell^2C
           -2ell^2[P''+(aN+2h)P'],
    Ty/M^2=Tz/M^2=L+4ell^2[(hP)'+(aN+2h)hP],
    rho_acc/(2M^2)=l'+2hl+lb+ell^2C-W.

On a FLRW spatial slice, a single lapse mode n=Nstar cos(kx) has
b_star=f p Nstar, p=k/a, f=(1+ell^2p^2)^-1. At quadratic order:

    Tx/M^2=b_star^2[(3-4f)/2+cos(2kx)/2],
    Ty/M^2=b_star^2[1/2-(5-4f)cos(2kx)/2],
    rho_acc_regular/M^2=b_star^2[1/2+(3-4f)cos(2kx)/2].

The last expression omits div(lambda), including its second-order part.
These are fixed-flat-measure components, NOT the full proper-volume mean.
The full source budget must include geometry, measure, dust and constraints.

## Exact planar geometry and cubic auxiliary action

Use gamma=a^2 diag(exp(2z+4chi),exp(2z-2chi),exp(2z-2chi)), N=1+n,
and contravariant shift U=N^x. Put J=H+zdot-U z_x, Lc=chidot-U chi_x,
D=U_x, Fbg=1+3beta/2. Then

    KijKij-(1+beta)K^2=
      [-6Fbg J^2+6Lc^2+4Fbg JD-4LcD-beta D^2]/N^2,
    R3=a^-2 exp(-2z-4chi)
      [-4z_xx+4chi_xx-2z_x^2+16z_x chi_x-14chi_x^2].

For x-covector components B and lambda, the regular cubic acceleration
action divided by M^2 is the integral of

    a(n+z-4chi)(B^2-2lambda B)+2a(z-4chi)lambda n_x
    -2ell^2/a(n-z-8chi)lambda_x B_x
    +2ell^2/a(z_x+2chi_x)(lambda_x B+lambda B_x).

The nonanalytic cubic term separately is -2/(3a0) integral |B|^3 in these
c=1 covector conventions. It has the odd-harmonic forcing already tested;
it does not supply a mean at second amplitude order. All variations are
taken BEFORE substituting linear auxiliary/metric constraints.

## Ordinary dust owns its current and source work

Write the matter clock as t+v and introduce canonical rest-mass density Pi.
Its exact Hamiltonian action is

    S_d=integral Pi[vdot+1-N W-N^i partial_i v],
    W=sqrt(1+gamma^ij partial_i v partial_j v).

Thus vdot+1=NW+N^i partial_i v and

    Pidot=partial_i[Pi(N gamma^ij partial_j v/W+N^i)].

Periodic total rest mass integral Pi is conserved. The normal projections
are rho_d=Pi W/sqrt(gamma), j_i=-Pi partial_i v/sqrt(gamma), and
Sij=Pi partial_i v partial_j v/[sqrt(gamma)W]. These are different from
setting the perturbation of proper density to zero by hand.

For no-factorial second orders, covariant shift N_i=partial_i Bshift,
Pi=Pibar(1+P1+P2), the dust sources are

    vdot2-n2=(|grad v1|^2/2+grad Bshift1 dot grad v1)/a^2,
    Pdot2=laplacian(v2+Bshift2)/a^2
      +a^-2 div[(P1+n1-2z1)grad v1+(P1-2z1)grad Bshift1].

For single cos amplitudes V,Bs,N,Z,P and theta=V+Bs, these quadratic
sources are p^2(V^2+2Bs V)(1-cos2kx)/4 and
-p^2[(P-2Z)theta+NV]cos2kx, respectively. In the saved four-state
variables V=theta+sigma, Bs=-sigma, Z=-Psi+Hsigma,
P=p^2D/r-3Htheta-3Psi. Contravariant U at second order differs from the
gradient of Bshift2 by its metric cross term; do not mix shift conventions.

Normal dust energy includes

    rho_d2/rhobar=P2-3z2+(9/2)z1^2-3P1z1+|grad v1|^2/(2a^2).

For homogeneous shear the canonical cubic dust action is

    Ld3=-Pibar[(n+P-2z-4chi)|grad v|^2/(2a^2)+P U v_x].

The exact integrated energy obeys

    E_d=integral Pi W,
    Edot_d=-integral sqrt(gamma)[N Kij Sij+j^i D_i N].

For one linear cos mode, Ekin2/Vcoord=Pibar p^2V^2/4 and
Edotkin2+2H Ekin2=Pibar p^2 V N/2. This is lapse work, not creation of
ordinary rest mass. The nonzero mean dust anisotropic stress is
rhobar p^2V^2 diag(1/3,-1/6,-1/6). Homogeneous shear therefore cannot be
discarded unless the FULL equations establish its cancellation.

The immediate next check is the complete projected mean constraint, volume
equation and shear response on the saved trajectory. The2k sector remains
a separate required calculation; a successful mean check does not finish it.
