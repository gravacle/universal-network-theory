# First environment dependent transport coefficient with a reference clock

2026-10-03 UTC. Prospective exact arithmetic calculation. Extend the new
fourth-order onset algebra to the first following even order, without a
time evolution, fitted window or parameter scan. This asks whether active
record feedback contributes to an environment-dependent relational response.
It does not assume that the response is gravitational or has the desired sign.

## Fixed states and controls

Use N=2, vertices (L0,L1,R0,R1)=(0,1,2,3), edges in order
(0,2),(0,3),(1,2),(1,3). Initial carrier0, target2, all records blank,
all writers occupied in the same content, fragment ports off. Compare
initial graph13 (a path) and15 (the cycle). Source0 has degree1 or2;
target2 and reference-clock1 have degree2 in both. The initial carrier
is distance2 from clock1. These are supplied, distinct preparations, not
equal-energy states or a pure isolation of density from all topology.

Keep Delta=4, Ud=d*=epsilon_psi=epsilon_r=1, epsilon_w=0, h=1/2,
t=1/2, j=1/4, g_wr=1. There are exactly eight arms: graph13/15,
uniform g_psi_r=0/1, and lambda_R=1/2 or the explicit zero-feedback control.
Retain every native link, hopping, current-square, record and copy term.
The complete initial energies are61/4 and43/2 for the two graphs, independent
of copy/feedback arm because the records are blank. Changing preparation
has not become free merely because its energy is listed.

## Exact coefficients and relational conversion

Reuse the authenticated Fraction operator of
native_active_record_transport_onset_v001.py, SHA256
6cef7370e4a2d3c53f56006dbd713e43c4e13ce31f120b3665e43f1800d990d3.
The zero-feedback control adds back (1/2)*sum_v d_v*r_v to that operator.
Compute H^k|initial> for k=0 through5. With v_k=H^k|initial>, target
projector T_2 and real coefficients,

    P2=<v1|T_2|v1>,
    P4=<v2|T_2|v2>/4-<v1|T_2|v3>/3,
    P6=<v3|T_2|v3>/36+<v1|T_2|v5>/60-<v2|T_2|v4>/24.

Use the SAME fixed reference B_1=(Z_1-iY_1)/2 in every arm, including
lambda_R=0; do not redress or fit its axis. Calculate the nested-commutator
expectations C_k=<ad_H^k B_1> through5, so beta^(k)(0)=i^k*C_k.
Obtain theta=arg(beta)=nu*x+a3*x^3+a5*x^5+... by the formal logarithm
of beta/beta(0). Its initial amplitude is1/2 and nu=2 in all eight arms,
but its later coefficients need not be equal. Local inversion is enough
for Taylor coefficients; no finite observation interval is thereby certified.

For the arrival expansion in that actual reference phase,

    K2=P2/nu^2,
    K4=P4/nu^4-2*P2*a3/nu^5,
    K6=P6/nu^6-4*P4*a3/nu^7
           +P2*(7*a3^2/nu^8-2*a5/nu^7).

For each graph and feedback choice report the uniform-copy on-minus-off
contrasts in P4,P6,K4,K6. Then take the graph15-minus-graph13 contrast
of those contrasts, and finally its native-feedback-minus-zero-feedback
contrast. Preserve all component values; neither a nonzero result nor any
particular sign is a computational pass requirement. This last interaction
contrast is not a unique separation of all geometry, energy and clock effects.
Save each of the three displayed K6 contributions separately. Their products
can give a nonzero interaction contrast without isolating a unique microscopic
feedback term. Report raw P6 beside the relational result. The supplied graph
change is degree/connectivity-sensitive, not a measured physical density.

## Checks and limits

Use exact rational equality, not a tolerance chosen after the result.
Check the eight complete initial energies, Hermitian moments, P2=1/4,
beta(0)=1/2, nu=2, and the already derived P4 copy contrast -1/24.
The remote K4 contrast is expected to remain -1/384; retain actual a3.
Crosscheck the overlapping graph15/native-feedback low-order values against
native_active_record_transport_onset_v001_results.json, SHA256
7dd5e9f265029226403be69db392ff60a26139d620cf63ee52dc2324c78cde5b.
Those powers are intermediates for a new sixth-order calculation, not a
replay of any previous propagated history. Report any failed exact equality.

One root-owned standard-library worker, sparse1024-dimensional support,
no eigenvalue solver, installs or fit. Bound the job by120 seconds and256 MiB;
the coefficients, not a long sampled trajectory, are the output. Save source,
input identities, all rational results and exit/runtime information once.
A detected environment-sensitive coefficient is not a derivation of BTFR,
a0, mass, distance, lensing, accelerated expansion or Stage3 completion.
