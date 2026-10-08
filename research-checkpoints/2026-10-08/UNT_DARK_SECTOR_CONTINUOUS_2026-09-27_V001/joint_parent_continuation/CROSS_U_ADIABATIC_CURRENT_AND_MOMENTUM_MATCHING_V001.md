# S_cross constructive adiabatic current and momentum matching V001

2026-10-06 UTC. Analytical continuation of V003 Eq5; both native and
observer reviews independently checked the raw ADM/current signs and
angular contacts. Root independently checked gauge cancellation, the
compatibility reduction and the disk phase-current sign. No operator or
trajectory evaluated. This is a conditional physical particular solution,
not a choice of an extra current profile or a completed galaxy history.

Use g=M²C, actual P(X), physical q=omega/N and n=P_X(q). A fully sourced
spherical static family has N(r;a),L(r;a),z_j(r;a), R=r. D=partial_ln a
holds the declared ordinary-source law/parameters, not a fitted halo.
Outer omega=Qbar(a), Dlnomega=−3sbar. Then

    Dln n=(−3sbar−DlnN)/s, s=cs²(q),
    Pi0=Lr²n, DPi0=Pi0[DlnL−3sbar/s−DlnN/s],
    Fflux(r)=−integral_0^r DPi0 dr.

For partial_t=H D and Hdot=O(H²), write chi=H chi1,beta=H beta1,
phi=integral omega dt+H psi1, p1=psi1'/L. Retain all native velocities.
Define the local geometric acceleration ar=N'/(NL), not empirical a0,

    e_j=z_j'/L, Z=sum w_j z_j, T=M²KB ar+gZ,
    I=sum w_j e_j²/omega_j², Bt=sum w_j(Dz_j)e_j/omega_j²,
    K=(T'+2T/r)/L+g ell²sum w_j[e_j²+2z_j²/(L²r²)],
    AU=K−gI,
    F=[DT−g sum w_j(omega_j^-2−ell²)(Dz_j)e_j]/N.

The exact O(H) raw current, projected-U and ADM momentum rows are

    (n/q+g)p1+gq chi1+(Ln/N)beta1=−Fflux/(Nr²),
    gq p1+(AU+gq²)chi1−(L/N)AU beta1=−F,
    [2M²(ln NL)'/(NLr)−gLI/N]beta1−AU chi1+n p1
                     =2M²DlnL/(NLr)−gBt/N+j_ordinary,1.

The centrifugal coefficient2 here is spherical, distinct from the disk
vector coefficient1. Unit/mode/mixed metric reactions remain included.
Independent modal Euler rows have no O(H) position correction on this
slow branch, but actual canonical momenta are

    Pi_j/H=Lr²g w_j{[Dz_j/N+(chi1/L−beta1/N)z_j']/omega_j²
                                       −ell²chi1 e_j}.

No native mode is reset. Independent fast homogeneous/incoming packets
are different retained states, not silently discarded evidence.

The raw three-row system has a time-slicing gauge on a FULL static
Einstein family. Let zeta=chi1−Lbeta1/N and pi=p1+qLbeta1/N. The two
physical current/U corrections satisfy

    (n/q+g)pi+gq zeta=−Fflux/(Nr²),
    gq pi+(AU+gq²)zeta=−F,
    determinant=(n/q+g)AU+gnq.

The determinant must be explicitly nonzero; positivity is not automatic.
Only the full static identity
2M²(ln NL)'/(L²r)=nq+K+rho_o+pr_o permits cancellation of beta in momentum,
with j_o,1=(rho_o+pr_o)Lbeta1/N+hat j_o,1. The remaining Ward compatibility is

    2M²DlnL/(Lr)+N hat j_o,1
         =DT+g ell²sum w_j(Dz_j)e_j−qFflux/r².

Its temporal-inertia terms cancel. A shift choice cannot repair a failed
compatibility. For a valid family, choose beta with the inherited outer
frame, then recover chi1=zeta+Lbeta1/N and psi1'=L(pi−qLbeta1/N).

At a worldtube with rbdot=H nu and no excess relative influx, require

    Fflux(rb)−nu Pi0(rb)=nbar rb²(rb−nu).

Failure needs actual computed excess exterior flux or compensation. The
finite wall of the current disk screen is not already this junction.
O(H) changes X only at O(H²), so cannot rescue a leading pressure-band failure.

For an axisymmetric disk, continuity itself gives the concrete scalar row

    partial_i[N sqrt(gamma)(n/q+g)gamma^ij partial_j psi1]
       =D(sqrt(gamma)n)
          −partial_i[N sqrt(gamma)gq u1^i+beta1^i sqrt(gamma)n].

The phase coefficient is positive; Neumann data require the actual
integral flux compatibility. The full projected-U equation supplies u1,
including Maxwell curl-curl and mode-gradient/inertia contacts, jointly
with Einstein momentum. Do not fit a poloidal streamfunction. The weak
background-subtracted disk is not a full static Einstein family: retain
its raw momentum and actual FLRW extrinsic/background contacts, rather
than imposing the full-static identity on flat geometry with cosmic charge.

Inputs: protected V003 action e08b7166…, current/Hilbert78 110b2f23…,
ADM94 cafaff53…, and retarded/background note78d369ef…; their full seals
are retained in the existing parent packets and continuation log.
No formation, exterior, full-metric, primordial or superiority gate closes.
