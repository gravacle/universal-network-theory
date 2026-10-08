# Full dressed-background matter addition: size-independent bounds V001

2026-10-05 UTC. Constructive continuation of the local proper-bond vacuum
gate, using the same native tuple and full record action. Root analytical
derivation and two independent analytical reviews PASS. No eigensolver,
propagation, producer replay or chosen volume-energy function is needed.

## Compare the same complete background in two conserved carrier sectors

Use the supplied simple q4 support on V=2N vertices, the same local flip h,
degree/storage/record-feedback terms and B/x record alphabet. All record
occupancies are now retained. Let H_vac be the COMPLETE Nc0 Hamiltonian on
this support; E_bg is its actual lowest energy over incidence and records.
The record projectors q_v commute with H_vac, so one background ground
vector may be chosen in a definite record-occupation word. This statement
does not select the filled word, a phase or autonomous record writing.

In the Nc1 one-content sector retain actual carrier energy, current,
hopping and copying, with EP=1, j=1/4, t=1/10, g=1/10:

    H_1 = H_vac tensor I_carrier + EP I
          +j D_n-t A_n+g sum_v P_v X_v.                (1)

D_n is occupied degree on the carrier space, A_n its occupied adjacency,
P_v the carrier-position projector, and X_v the actual B/x record flip.
Define E_1=min spectrum H_1 and Delta_add=E_1-E_bg. This is a difference
of FULL sector ground energies in one finite support, not a bare P-block
eigenvalue, a removed identity or the energy of a chosen vacuum trial.

## Lower bound retains the complete copying operator

For every incidence word, the graph Laplacian D_n-A_n is positive:

    j D_n-t A_n=t(D_n-A_n)+(j-t)D_n >= 0.

The same inequality is an operator inequality in the full graph/carrier
space. Since the P_v are mutually orthogonal and sum to I_carrier,

    ||sum_v P_v X_v||=1.

Thus H_1 >= H_vac tensor I+(EP-|g|)I, and

    Delta_add >= EP-|g| = 9/10.                       (2)

Record/copy noncommutation is retained; no X eigenvalue is imposed on a
background that conserves q. No gap estimate on globally frozen P is used.

## Upper bound uses an actual background ground vector

Take any actual H_vac ground vector in a definite q-word, tensor the
normalized uniform carrier vector u=V^(-1/2)sum_v |v>. Its copying
expectation vanishes: every X_v changes that word. For each occupied edge,
the uniform vector has equal current and hopping matrix elements2/V.
The addition expectation is therefore

    EP+(j-t)<sum_v d_v>/V <= EP+4(j-t)=8/5.

The variational principle gives

    9/10 <= E_1-E_bg <= 8/5.                          (3)

These bounds hold at every finite size and every h in the stated support/
sector, including the new h=.2 and preserved global h=Omega/N families.
They require no factorization of the incidence ground state. In particular,
extensive vacuum dressing does not force a divergent matched matter-addition
energy. The interval is a bound, not a measured mass or an exact pole energy.

## A nonuniform source domain that does not shrink with volume

Keep the complete original node sources and edge midpoint source, with
positive L_v and m_e=(L_u+L_v)/2. Compare the SAME E_bg[L]=min H_vac[L]
to E_1[L]. The extra carrier edge block is

    n_e m_e [j(P_u+P_v)-t T_uv] >= 0,

because its two endpoint eigenvalues are m_e(j+-t)>=0. Its copy term is
g sum_v L_v P_v X_v, and the local carrier term is EP sum_v L_v P_v.
Thus the added operator is bounded below by (EP-|g|) L_min I.

An actual H_vac[L] ground state again permits a definite q-word. Tensoring
u gives an upper expectation

    EP L_avg + [2(j-t)/V] sum_e m_e <n_e>
       <= [EP+4(j-t)] L_avg,

where sum_all_eligible_edges m_e=2 sum_v L_v on q4 support. Therefore

    (9/10)L_min <= E_1[L]-E_bg[L] <= (8/5)L_avg.        (4)

This positive-source addition-energy domain holds independently of volume.
It is a different object from the old small-source absolute P/Q separation,
whose sufficient window shrank with volume. The old proof is preserved,
and its gap/phase conclusion has not been transferred into this family.
For uniform L=ell>0, the full action scales by ell and Delta_add scales
exactly by ell. The bound respects this common-source Ward control.

## Actual native-copy dressing tightens the bound

Use an actual FULL all-record H_vac[L] ground vector psi_q of definite
q-word, rather than a merely fixed-word sector minimum. Define two
orthonormal trial vectors

    Phi0=u tensor psi_q,
    Phi1=V^(-1/2) sum_v |v> tensor X_v psi_q.

This unweighted native-copy trial need not be an invariant dynamical
subspace; at nonuniform L it is not the normalized image of H_copy[L].
The actual record-flip energy above that full background is

    delta_v[L]=(1-2q_v) b_v >= 0,
    b_v=L_v-(1/2) sum_incident_e m_e <n_e>
       =(1-<d_v>/4)L_v-(1/4) sum_u <n_vu>L_u.         (4a)

The lower zero follows from global minimality over ALL record words.
Since <d_v><=4 and L_v>0, summing the triangle inequality gives

    sum_v |b_v|
       <= sum_v (1-<d_v>/4)L_v
          +(1/4) sum_(v,u) <n_vu>L_u
        =sum_v L_v,
    delta_avg<=L_avg.

Set D_L=V^(-1)sum_v L_v<d_v><=4L_avg. The complete two-state compression,
after subtracting that SAME E_bg[L], is exactly

    [[EP L_avg+(j-t)D_L,  g L_avg],
     [g L_avg, EP L_avg+j D_L+delta_avg]].             (4b)

All no-copy cross terms vanish by definite-q orthogonality. Phi1's hopping
expectation is zero: different carrier positions have different flipped
record words. Copy diagonals vanish and its offdiagonal is g L_avg, even
when source weighting takes a vector outside this trial span.

Raising the two diagonal entries bounds its lowest eigenvalue above by
L_avg times the lowest eigenvalue of [[8/5,1/10],[1/10,3]]. The variational
principle therefore sharpens (3),(4) to

    (9/10)L_min <= Delta_add[L]
       <= (23/10-1/sqrt(2)) L_avg.                    (4c)

At uniform L=1 the upper bound is approximately1.59289321881345. This
refinement includes actual copying without an eigensolver or a small-g
expansion. It is still a universal bound, not a phase-selected pole value.

## Source relaxation and physical limits

Neither the upper trial nor the two ground-energy extrema supply a local
quasiparticle pole. Translation/phase selection, momentum chart, finite
local addition residue, lifetime and positive rank-three kinetic curvature
must still be earned in one common reference. A change of lowest-energy
branch or record word cannot be hidden as an analytic probe response.
No independently calibrated proper mass, physical geometry or second probe
has yet been obtained from (3).

On an admitted differentiable isolated ground branch, affine-source
Hellmann-Feynman derivatives compare the actual vertices in both sectors.
For a source direction J, its quadratic relaxation is

    d2 Delta_add/dJ2
       = -2 sum_(a!=0) |<a,1|H_1,J|0,1>|^2/(E_a,1-E_0,1)
         +2 sum_(b!=0) |<b,0|H_vac,J|0,0>|^2/(E_b,0-E_0,0). (5)

This expression assumes the indicated gaps/branches; degeneracies require
the full projected causal response rather than this scalar formula. Direct
second contacts must be added for nonaffine physical sources. The difference
has no universal sign even though each affine-source ground energy is
concave. Do not rename it passive susceptibility or a gravitational field
law without the common source, causal/gradient action and physical binding.

Matched addition subtracts one actual background when defining the probe
energy; whole-action source, mechanical/creation work and donor stress keep
that background energy once. No record halo, fitted E(V), negative pressure,
cosmic count law, healthy3D phase or observational superiority is asserted.
The constructive result is finite positive full addition energy despite
extensive local vacuum dressing, and a concrete next pole/curvature target.
