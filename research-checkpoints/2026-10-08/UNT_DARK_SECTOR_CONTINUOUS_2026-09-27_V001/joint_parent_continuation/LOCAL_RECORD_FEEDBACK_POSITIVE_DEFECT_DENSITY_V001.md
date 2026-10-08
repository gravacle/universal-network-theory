# Fixed local interaction requires a dressed degree-two reference

2026-10-05 UTC. New volume-uniform analytical consequence of the same
supplied periodic q4 parent, Nc0 and occupied records q_v=1. No new state,
formation rule, physical space, Hamiltonian action or spectrum is calculated.
This complements the completed overlapping-star bounds.

Let P_v project onto degree d_v=2 and Q_v=1-P_v. Write r_v=<Q_v> and
p=V^(-1)sum_v r_v, distinguishing r from record occupation q. The full
ground energy is E0=<D>-h<sum_e X_e>, D=sum_v D_v>=0, h=1/5.

For every edge incident at v, a single flip changes d_v by one, so
P_v X_e P_v=0. For any normalized state, mixed states by purification,

    <X_e>=<Q_v X_e>+<P_v X_e Q_v>,
    |<X_e>| <= sqrt(r_v)+sqrt[r_v(1-r_v)] <=2sqrt(r_v).

These are Cauchy-Schwarz inequalities; no independent vertex state is
assumed. Sum the four incident edges at every vertex and divide the two
endpoint owners, then apply concavity of sqrt:

    <sum_e X_e>/V <= sum_e |<X_e>|/V
                   <=4 average_v sqrt(r_v) <=4sqrt(p).

The independently derived blank-BOND matching trial, with all records
occupied, has full energy density -c=(5-sqrt29)/20<0. The actual sector
ground therefore obeys E0/V<=-c. Combining this with D>=0 gives

    c <=-E0/V <=h<sum_e X_e>/V <=4h sqrt(p),
    p >=c^2/(16h^2)=(27-5sqrt29)/128>0.                 (1)

The exact lower constant is about .00057949972130843627926, with that
display rounded down using the sealed rational sqrt certificate. Thus
expected bare degree defects grow at least proportionally to V at this
fixed local coupling. This is stronger than a bound on merely leaving the
whole all-degree-two subspace, which could be caused by O(1) defects.

Because D_v>=Q_v/2 and delta_v^2>=Q_v,

    <sum_v D_v>/V >=(27-5sqrt29)/256,
    <sum_v delta_v^2>/V >=(27-5sqrt29)/128.

Together with the independently audited star upper bounds the sector
ground has a rigorous, deliberately broad local-defect envelope:

| ground observable per vertex | lower, rounded down | upper, rounded up |
|---|---:|---:|
| bare nonice projector | .00057949972130843627926 | .73681426844465455951 |
| delta squared | .00057949972130843627926 | .73681426844465455951 |
| actual positive D_v | .00028974986065421813963 | .36840713422232727976 |

The exact formulas and Fraction endpoints control these displays. The
bound concerns a ground state, or a state with the same energy upper
bound; it is not imposed on an arbitrary evolving preparation.

Finite zero-point degree mixing is compatible with a dressed quantum
liquid. It neither excludes nor establishes that phase, proves thermal
or irreversible defect production, measures a global bare-P overlap,
selects the occupied-record sector over all others, or forms the graph.
It supplies no transverse spectral weight, physical metric, matter pole,
gravity coefficient, strain law or expansion history. A bare degree-two
projection cannot replace the current finite-h ground reference.

Inputs, unchanged in joint_parent_continuation:

- LOCAL_RECORD_FEEDBACK_3D_STAR_BOUND_V001.md:
  8e5b84074549afaa29813b2510416f408302dd86e8160597312cd677fed9c8d8.
- LOCAL_RECORD_FEEDBACK_3D_STAR_BOUND_V001_RESULT.json:
  29880da6f2e69a7f1319827b2516cd6cf47d58567b8a9ed4cb98229d6a781aab.
- LOCAL_RECORD_FEEDBACK_3D_STAR_BOUND_V001_RECEIPT.json:
  84a7cee9782a30123e71f0fd986c6a2fdeef8f2e5ee9001f1aa8f777fff26b88.

Root and two independent reviewers derived (1) before this note was
saved. Only saved scalar Fraction arithmetic supplies the displays; no
producer, matrix action, eigensolve, inertia or evolution was replayed.
