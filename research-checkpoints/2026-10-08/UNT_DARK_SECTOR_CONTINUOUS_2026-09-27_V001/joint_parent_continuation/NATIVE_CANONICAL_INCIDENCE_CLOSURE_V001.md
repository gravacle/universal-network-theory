# The native incidence channel already has an exact canonical mechanics

2026-09-28. Analytical reconstruction of the OWNED held Hamiltonian, not a
new source law, fitted mass, passive-state replacement or numerical suite.

## Result

The changing native incidence-source moment has an exact mechanical
explanation: it is the momentum curvature of a compact spin-phase
Hamiltonian. No constant oscillator mass is needed. This representation
reproduces the full driven incidence expectation for any prescribed owned
source H-f(t)n, including the source kick and its state-dependent initial
response. The coefficients and state are the existing native ones.

It is an exact canonical representation of qubit expectation dynamics on
fixed-radius unitary orbits, not a replacement of quantum measurement
statistics by classical point statistics. The record-clock observable still
requires cross-sector coherences, which this incidence-only reduction must
not discard when addressing the clock.

## 1. Exact sectors, including mixed conditional link states

The held Hamiltonian and incidence source commute with total record count R
and carrier X_C. For R=0,1,2 and s=+/-1, put

    Pi_Rs=P_R*(I+sX_C)/2,
    x_Rs=9/4-lambda_R*R-s/2,
    H_Rs(f)=(3+R)I-hX+(x_Rs-f)n.                         (1)

The record multiplicity at fixed R is 1,2,1. For an arbitrary actual density
matrix, w_Rs=Tr(Pi_Rs rho) is constant under every prescribed incidence
source. Where w>0, trace the diagonal block over its record multiplicity and
divide by w to obtain its normalized 2x2 link density matrix sigma. It evolves
exactly under (1), even if it was mixed or entangled with the record factor.
No assumption that it occupies the lower band is made.

Write

    sigma=(I+Xbar*X+Ybar*Y+Zbar*Z)/2,
    r²=Xbar²+Ybar²+Zbar²,     0<=r<=1.

Y here is conventional link Pauli Y, not the opposite-sign record quadrature.
The Bloch radius r is constant because sigma evolves unitarily. Blocks with
w=0 have no conditional state; r=0 is a stationary maximally mixed point,
not an angle-carrying oscillator. Neither case permits division by w or r.

All incidence observables and their driven histories depend only on these
diagonal conditional link matrices. The incidence source is block diagonal,
so coherences between R or s sectors cannot enter those readouts. This is an
exact closure for that specified channel, not a general removal of coherence.
Its domain is this OWNED SINGLE-LINK held cell and sources preserving R,s.
In a multi-link network, degree penalties and carrier dynamics can entangle
links; independent Bloch-sphere equations then need additional correlators
and do not follow from this result. The full network Hamiltonian has not been
replaced by independent spins.

## 2. A canonical chart and its signs

For a nonzero-radius sector away from its link-Z poles, define

    m=(1-Zbar)/2,
    Q(m)=sqrt(r²-(1-2m)²),
    Xbar=Q*cos(theta),    Ybar=Q*sin(theta),
    q=m,    p=hbar*theta,    {m,p}=1.                     (2)

The normalized sector Hamiltonian is exactly its energy expectation:

    H_sector(m,p;f)=3+R+(x-f)*m-h*Q(m)*cos(p/hbar).        (3)

Hamilton's equations give

    m_dot=h*Q*sin(theta)/hbar=h*Ybar/hbar,
    theta_dot=-(x-f)/hbar
                  +2h*(1-2m)*cos(theta)/(hbar*Q).         (4)

They imply, without approximation,

    Xbar_dot=(x-f)*Ybar/hbar,
    Ybar_dot=[2h*Zbar-(x-f)*Xbar]/hbar,
    Zbar_dot=-2h*Ybar/hbar,                               (5)

which are precisely the von Neumann/Pauli equations for (1). Equivalently
the chart gives {Xbar,Ybar}=2Zbar/hbar and its cyclic counterparts, reproducing
the quantum commutator means for these linear observables. This fixes the
symplectic orientation; replacing p by -hbar*theta with the same bracket
would have the wrong incidence drift and impulse sign.

The domain is (1-r)/2<m<(1+r)/2, with p periodic modulo 2pi*hbar. For pure
states r=1 the endpoints are m=0,1; mixed states have a smaller interval.
Q=0 makes theta undefined and (4) singular as coordinates, but (5) remains
smooth. Use another sphere chart or the density matrix through such a pole;
there is no physical reset or loss of unitary evolution. The fixed-r sphere
has symplectic area 2pi*hbar*r. Formation with copying enabled changes R
blocks and is outside this held-sector reduction.

## 3. Weights and the source moment must be normalized together

For multiple occupied sectors the measured incidence is B=sum_j w_j*m_j
and the energy is sum_j w_j*H_j. The weights are constant trace probabilities,
not new material populations or physical-volume densities. Use canonical
P_j=w_j*p_j, so

    {m_j,P_k}=delta_jk,
    H_total=sum_j w_j*H_j(m_j,P_j/w_j;f),
    B=sum_j w_j*m_j.                                     (6)

Then m_dot is the same normalized evolution (4), not w times too slow.
Using p_j as canonical while also multiplying its Hamiltonian by w_j would
be incorrect. One may equivalently use q_j=w_j*m_j and p_j as canonical.

The owned negative-sign impulse H-eta*n*delta(t-w) shifts

    p_j -> p_j+eta,    P_j -> P_j+w_j*eta,
    theta_j -> theta_j+eta/hbar.                          (7)

This agrees with U=exp(+i eta n/hbar):
Xbar -> Xbar*cos(alpha)-Ybar*sin(alpha),
Ybar -> Ybar*cos(alpha)+Xbar*sin(alpha), alpha=eta/hbar.
Every sector receives the same source angle; weights do not supply a second
factor of w to the physical response.

In particular,

    H_sector,pp=h*Xbar/hbar²,
    H_total,PjPj=(h*Xbar_j/hbar²)/w_j,
    d(delta B_dot)/deta|0=sum_j w_j*h*Xbar_j/hbar²
                         =h*<X_a>/hbar².                 (8)

Thus the exact quantum identity [n,[H,n]]=hX_a and all the measured changing
first moments have an already-owned canonical realization. No fit to those
moments was used. The negative-source impulse convention is essential in
relating a classical Poisson response to the quantum retarded sign.

For a regular prescribed f(t), inclusive source work is
d<H(f)>/dt=-f_dot*B. With endpoints at f=0 the change of held energy can also
be written integral f*B_dot dt. For the ideal kick, the finite held-energy
change follows directly from (7):

    Delta E_hold=h*sum_j w_j[(1-cos(alpha))*Xbar_j
                                      +sin(alpha)*Ybar_j]. (9)

These are the same source/work conventions, not energy created by a change
of phase coordinates. The constants 3+R and the full weights remain in (6).

## 4. What the changing momentum curvature means

All sampled ages in the relational census have positive total source moment.
The exact expression (8), however, can change sign on other states. This is
a coordinate curvature on a compact fixed-Bloch-radius orbit, not by itself
a negative microscopic norm or an instability of the unitary dynamics.

An exact stability check makes that distinction concrete. At either
stationary Bloch direction along or against the held energy axis, write

    d=sqrt((x-f)²+4h²),    Q=2h*r/d.

For r>0 and h>0, H_mp=0 and H_mm*H_pp=d²/hbar². At the lower-energy point
both diagonal curvatures are positive; at the upper-energy point both are
negative. Both have elliptic linear precession frequency d/hbar. A negative
H_pp alone is therefore not a proof of exponential instability.

A fixed-positive-mass quartic channel with a fixed linear coordinate source
has a state-independent canonical source moment. It cannot be identified
with (1)-(8) over this full evolving native census by default: the native
cosine curvature and compact phase space are different. A positive-mass
oscillator expansion can still be a separately justified local or
coarse-grained limit near an appropriate branch. Its source, state range,
weights and omitted corrections must be derived rather than supplied by a
constant fit. The observed positive moments do not themselves establish that
limit or its proposed soft-spectrum law.

## 5. Preserve the record phase and the physical matching boundary

The successful writer-referenced clock candidate uses A_L+A_R, which changes
record count. It depends on off-diagonal sector matrices. In a fixed basis
their exact evolution remains

    i*hbar*rho_dot_ab=(H_a(0)-f*n)*rho_ab
                              -rho_ab*(H_b(0)-f*n).       (10)

Here H_a(0), H_b(0) are the zero-source sector matrices, so the source is
included exactly once.
The appropriate record-raising matrix contracts these blocks to give <A>.
The diagonal Bloch variables and weights cannot reconstruct their relative
phases. A complete joint incidence/record-clock description therefore keeps
these coherent blocks, or simply the already owned full 16-state density
matrix. The incidence azimuth theta in (2) is NOT automatically the record
phase arg<A> or the covariant clock field T.

Finally, the existing diagnostic source H-fn has exactly zero second source
contact. Equation (3) preserves that fact; no seagull or identity contact is
added. Its mechanical state dependence does not determine the separately
unbound physical strain/source conversion, absolute volume derivative or
metric clock normalization in NATIVE_SOURCE_BRIDGE_DECISION.md.

The constructive advance is an exact alternative to unjustified constant-mass
matching: the original native incidence channel already supplies its own
canonical, state-dependent mechanics and work ledger. The source/volume and
coherent record-clock matching can now be required to preserve that mechanics,
rather than replacing the actual state to make a passive model convenient.
