# Native record-mediated interaction: a certified sign counterexample

2026-09-27. Exact finite algebra and a norm bound; no numerical run, edge
pinning, new interaction, ground-state preparation or physical force claim.

**Result:** one fixed admissible N=2 BS Hamiltonian has a strictly positive
same-layer binary record crosscost in an occupied background and a strictly
negative opposite-layer crosscost in the blank background, with all four
native link flips nonzero. Thus ground-state relaxation does not guarantee
universally negative record crossinteractions.

Source: the recovered [BS microscopic action](recovered_sources/BS_MICRO_ACTION.md),
SHA256 `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`,
BS01, BS06, BS09-BS13. This is a newly specified graph-only parameter example
inside that action family, not the parameter set or formed state of an earlier
test. No coefficient is retuned between record patterns.

## 1. One complete four-link restriction

There are two left nodes L0,L1 and two right nodes R0,R1. All four possible
links remain dynamical qubits, with n_e=(I-Z_e)/2. Put d_v=sum_(e incident v)n_e.
Record occupations q_v are fixed binary sector labels; occupied records may
use the same fixed content. All formation/copy couplings are off, carriers,
writers and reservoir spectators are blank, and ports are zero. Set, in one
common energy unit,

    N=2, U_d=1, lambda_R=1, Delta=3, d_star=7/8,
    epsilon_r=3, t_hop=0, lambda_J=0,
    h=h_N=1/64, Omega=N h=1/32.

Blank spectator storage contributes zero. The full nonconstant restriction is

    H_h(q)=sum_v(d_v-7/8)^2+3 sum_e n_e
           -sum_(e=u v)n_e(q_u+q_v)+3 sum_v q_v
           -h sum_(four edges)X_e.

The record-storage term and all degree penalties are retained. These choices
satisfy BS13 with delta_E=1:

    Delta=2lambda_R+|t_hop|+delta_E,
    epsilon_r>lambda_R N,       U_d>=0, lambda_J>=0, Omega>0.

The original seed permits real d_star; no integrality requirement is imposed
on that coefficient. Graph degrees and record occupations remain integers.
No graph configuration is removed from the 16-dimensional link Hilbert space.

Let E_h(q) be the lowest graph energy in the specified record sector, including
its storage term. This is a conditional spectral energy, not the energy of a
demonstrated prepared ground state. For two initially blank probe records u,v
and a fixed background b, define the discrete crosscost

    J_uv(b;h)=E_h(b+e_u+e_v)-E_h(b+e_u)-E_h(b+e_v)+E_h(b).

Positive J means that the second insertion costs more in the presence of the
first, relative to the same background. It does not yet mean a spatial force.

## 2. Exact zero-flip minimization, without a matching constraint

Temporarily set h=0 only to establish an exact reference energy. Since each
node has two possible incident links,

    H_0(q)=C+3 sum_v q_v
       +sum_(e=u v)[3/2-(q_u+q_v)]n_e
       +2 sum_v n_(v,first) n_(v,second),
    C=49/16.

This follows by expanding all four degree squares. The edge coefficient is
3/2 for two blank endpoints, 1/2 for one occupied endpoint, and -1/2 for
two occupied endpoints. The final term is the native degree penalty, not an
added exclusion rule.

Any positive-coefficient occupied edge can be removed to lower the energy:
its removal also reduces or leaves unchanged every nonnegative pair penalty.
Among the remaining negative-coefficient edges, if any vertex has degree two,
removing a conflicted edge changes the energy by

    +1/2-2m<=-3/2,

where m>=1 counts its endpoints having degree two. Thus a minimizer must be
a matching. Each retained matching edge lowers the energy by 1/2, so the
minimizer is a maximum matching among occupied-record endpoints. This is an
optimization conclusion over the full graph space, not imposed edge pinning.

If R_L and R_R are the numbers of occupied records in the two layers, the
induced possible-link graph is complete bipartite and the exact energy is

    E_0(q)=C+3(R_L+R_R)-(1/2)min(R_L,R_R).

This formula is for binary q only; it is not a continuous fractional-count
interpolation. Some minimizing configurations are degenerate. No uniqueness
assumption is needed for this energy result or the continuation below.

### Same-layer competition

Fix the background q_R0=1, q_R1=0 and take probes L0,L1. Their energies
minus the common C are

    background: 3;
    either single probe: 11/2;
    both probes: 17/2.

Hence

    J_(L0,L1)(q_R0=1;0)=17/2-11/2-11/2+3=+1/2.

Either single probe can gain the -1/2 matching energy with R0. When both
are present, they compete for that one favorable endpoint; the degree penalty
prevents receiving that gain twice in the minimizing configuration.

### Opposite-layer contrast

With blank background, take probes L0,R0. The energies minus C are 0,3,3,11/2,
so

    J_(L0,R0)(blank;0)=11/2-3-3=-1/2.

The backgrounds differ and are explicit. The first result is an effective
pair crosscost in a third record's presence, not a positive vacuum two-body
coefficient or proof of a pairwise-additive effective theory.

## 3. Certified persistence with every link flip active

Return to the single fixed choice h=1/64. The perturbation is exactly

    V_h=-h sum_(four edges)X_e,       ||V_h||=4h=1/16.

The variational eigenvalue bound gives |E_h(q)-E_0(q)|<=4h separately for
every q, even when a zero-flip minimum is degenerate. The triangle inequality
for the four energies in J therefore gives

    |J_uv(b;h)-J_uv(b;0)|<=16h=1/4.

Consequently the nonzero-flip native Hamiltonian obeys the rigorous intervals

    1/4 <= J_(L0,L1)(q_R0=1;1/64) <= 3/4,
   -3/4 <= J_(L0,R0)(blank;1/64) <= -1/4.

These are certificates, not fitted values or numerical diagonalization.
The whole range 0<h<1/32 preserves both strict signs by the same bound.

Individual record insertion remains strictly positive. For any still-blank
node v and any other fixed record pattern, the exact operator difference is

    H_h(q+e_v)-H_h(q)=3I-d_v,
    I<=3I-d_v<=3I.

Thus 1<=E_h(q+e_v)-E_h(q)<=3. A positive crosscost is not produced by
negative-energy storage, a missing reference energy or a change of coefficients.

## What the example establishes

Ground energy is concave in independently interpolated affine source
coefficients. Negative semidefiniteness of a differentiable Hessian constrains
quadratic forms, not the sign of each off-diagonal entry. The positive binary
crosscost here is compatible with that fact; no local Hessian value is inferred
by treating the binary minimum formula as a smooth count function.

This example excludes a universal-sign inference from the native record-link
coupling or from concavity alone. It does not identify either sign with a
gravitational force. Record occupations are conserved on this hold, and neither
physical separation nor relative record motion has been supplied. Existing
carrier transport can provide a separately specified response test, but its
current is not already the derivative of these conditional ground energies.
No cooling, irreversible equilibration, physical metric or dark-sector claim
is added. The counterexample needs no numerical extension to establish its
stated finite-h signs.
