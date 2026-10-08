# Gapped empty-incidence configuration locality V001

2026-10-05 UTC. NEW exact consequence of the complete frozen C8 blocks and
occupied-incidence memory law. This derives a range bound without a solver,
producer import, new acquisition, fitted potential or support term. It is
locality in the empty-sector carrier configuration graph at fixed real
spectral arguments, not an assertion about physical body separation or the
full occupied propagator. The adopted RGRL/WTC effective route is preserved.

## The actual positive empty operator

Copies are off, q is conserved, u=lambda s with s=q0+q4=0,1,2 and
lambda=1/2. Keep t=1/10, j=1/4 and h=1/5. Remove only the disclosed common
scalar A_R sum(q) when defining zbar; restore it for absolute energies,
source/work/count contacts and coherent cross-q readouts.

At zbar=19/2 in the one-carrier reference and zbar=11 in the ordered tagged
two-carrier sector, the empty block obeys exactly

    H_e0+uI-zbar I = D_u-t A_open,
    D_u(x)=b+j d(x)+u,
    b=3/2 (reference), b=1 (tagged).                    (1)

Here A_open is the unweighted adjacency matrix of the allowed single-hop
configurations after removing edge0--4. The degree d(x) counts those actual
allowed hops, including hard-core exclusion. For one carrier, d=1 or2. For
ordered tagged pairs, d=Bcut_open is between1 and4. Explicitly its diagonal
is 2-(1/2)P_adj-(1/4)C_04+u, agreeing with1+j Bcut_open+u; no tagged direct
current is discarded. Therefore

    Dmin >=7/4+u (reference), >=5/4+u (tagged).          (2)

These are diagonal bounds, separately from the stronger spectral gap
controls used by the completed resolvent packet. They require no new matrix
or spectrum evaluation.

## A degree-linked Neumann bound

Set P=t D_u^(-1) A_open and B=t D_u^(-1/2) A_open D_u^(-1/2).
P is nonnegative and similar to the real symmetric B. Its row sum is
t d/(b+j d+u), increasing with d for the positive b+u here. Perron bounds
and symmetry give ||B||_2 <=rho_u with

    rho_u <= (1/5)/(2+u) (reference),
    rho_u <= (2/5)/(2+u) (tagged).                     (3)

At u=0 these are1/10 and1/5. The cruder independent max-degree/Dmin bounds
4/35 and8/25 are also valid; the linked degree ratio in(3) is sharper.
All three nonnegative loadings have rho_u<1. Hence

    G_u=(H_e0+uI-zbar I)^(-1)
       =D_u^(-1/2) sum_(m>=0) B^m D_u^(-1/2),
    R_u=-G_u,    Sigma_u=-h^2 G_u.                     (4)

Every term has nonnegative entries. Thus the empty inverse is entrywise
nonnegative, while Sigma_u is entrywise nonpositive in this fixed native
configuration basis. This statement is stronger than negative
semidefiniteness and does not extend to arbitrary basis changes.

Let ell(x,y) be shortest-path distance in that empty configuration graph.
All (B^m)_xy vanish for m<ell. Bounding the remaining terms by their operator
norm gives

    |Sigma_u(x,y)| <= h^2 rho_u^ell /
                  [sqrt(D_u(x)D_u(y)) (1-rho_u)]
               <= h^2 rho_u^ell /[Dmin (1-rho_u)].      (5)

There is no hidden physical-length conversion in ell. For distinct
components all these entries are exactly zero, rather than a small
exponential tail.

For u_j>u_i the same scalar-loading identity gives

    Sigma_uj-Sigma_ui=(u_j-u_i) h^2 G_uj G_ui.           (6)

This is entrywise nonnegative. Since G_ui-G_uj is that positive product,
the increment is also entrywise bounded by h^2 G_ui and inherits(5) with
the weaker loading u_i. Raising the empty cost reduces the magnitude of
each subthreshold virtual entry. It does not determine the sign of a
vacuum-matched 0/1/2-carrier energy contrast or a force.

## Which configurations are disconnected

The empty one-carrier path has node order(0,5,1,6,2,7,3,4). In the tagged
empty sector, two distinct labelled carriers cannot pass each other on this
open path. Its56 configurations split into the28 with tag1 preceding tag2
and the28 with the opposite order. Sigma and its loading increments have
exactly zero entries between those components.

The occupied C8 restores edge0--4. Its ordered-pair configuration graph is
connected: the vacant sites permit motion around the seam and connect the
two open-path order classes. The complete112D carrier/incidence block is
therefore connected. Empty-sector component zeros must not be transferred
to the full occupied resolvent or to the complete released-edge dynamics.

The bound concerns the real arguments in(1), below the empty threshold.
It neither bounds a full occupied inverse at a pole nor supplies exponential
decay in physical time, irreversibility, a continuum correlation length,
or an all-native exclusion of long-range response. A different spectral
gap, support or phase requires its own range analysis. All q sectors and
their correlations remain owned; replacing s by a mean is not this law.

## The next separation-dependent physical question

The smallest force criterion would use the SAME complete action and
independently specified recorded-body insertions to define

    W_conn(R)=W_AB(R)-W_A(R)-W_B(R)+W_0(R),
    F_conn(R)=-partial_R W_conn(R).                     (7)

W is a ground energy on an owned ground branch, or free energy at an owned
temperature and ensemble. R must be a physical separation in a supplied
common ruler/chart, with actual H_total,R, references, charged-record
apparatus, census, return and support contacts retained in all four terms.
No fitted potential is introduced by(7). A translated preparation on a
fixed H instead adds Tr[(partial_R rho_R)H] and tests preparation work; it
does not by itself produce a force law. The present vacancy-coherent tagged
insertion is not automatically a pair of localized, separated bodies.

The adopted RGRL/WTC common-metric working premise can supply the physical
chart for an effective-network test without first proving microscopic RF3.
It still needs one declared common constitutive state/source action and
absolute reference. Equations(1)-(6) localize what this particular frozen
finite-gap virtual channel supplies. They do not assign an environmental
halo of records or select a favorable new displacement/support law.

## Frozen ancestry

All listed current bytes were authenticated before saving this note. The
matrix bundles are cited as already authenticated inputs; they were not
opened or acted on for this derivation. Paths are relative to the sole
project root.

| Input | SHA256 |
|---|---|
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_OCCUPIED_INCIDENCE_MEMORY_LAW_V001.md | 9239dcce75623cee38dd2ca4df78686b4d75f87d4baa975139549a29f15a0f26 |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001.md | 68b4a61ded02e9e6ecdfcf1819680d519f794eb8e3ba08b5b7a1ba329ed1aab9 |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/floating_return_c8_tagged_probe_reaction_v001.py | 778ff1615b0ab38c964ca4feb40b756c0df04771103afc953871c12c890e26c0 |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/floating_return_c8_tagged_probe_reaction_v001_checkpoints/reaction_eigensystems.npz | 06432406fd969f8ec3c8d93a606207ff5c4bd1ce0deb0281b87e41e190ebcc1a |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001.md | 8f3dc32381e76a4e6badfe23fff6c8bdd4830cb32ed0aff99b1aef57eba5ce5b |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/floating_return_c8_retained_record_geometry_v001_checkpoints/release_eigensystems.npz | 4dd6c3d1a4d69761e8fb4ecb7755113f81d41473129614a0df9a8f0bcff09ebc |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/FLOATING_RETURN_C8_RECORD_INTERACTION_RESOLVENT_V001.md | ebbfb9fb4c206696daf275fe95f49abbda1c26213f697cf04cfd235c5436ae13 |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/floating_return_c8_record_interaction_resolvent_v001.py | 75e5cba71872e49f1639b85404d58767c2b7b63224cf5232e1345bd90c428634 |
| UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_COMMON_METRIC_SOURCE_RESIDUAL_V001.md | 665545ea6e674105e77b5977eecf9fd37287f19d7f1b273be8116867d2fc4bad |
| program-worktree/GRAVITY_RECORD_FIRST_WORKING_THEORY_CLOSURE_V001.md | cf9229586268f054b473b1641085ebafc3bca01fa0691a191cbda923ae1fa7f2 |
