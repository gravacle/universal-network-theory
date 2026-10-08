# Static source response at the first degree tie

2026-09-30. Exact analytic continuation of the projected matching source
bound. No spectra, numerical run, additional interaction, coefficient retuning
or physical-volume assignment. The preceding notes remain unchanged.

## Result and scope

For the complete node-energy source inside the first-tie projected matching
model, all nonzero ground-to-excited transitions occupy two explicitly known
standard-representation blocks. A Perron comparison bounds every such gap
from below. Combined with the exact weight bound, this gives

    chi_anchor(0) <= Omega (N+1)/(sqrt(2) N^(3/2)).       (1)

Thus the anchored static susceptibility, not only its finite-time weight,
vanishes as N grows at fixed Omega and source normalization. Merely replacing
the strict regular phase by the first-order matching ladder does not evade
that conclusion within PHP. For an arbitrary bounded extended profile the
upper bound is instead O(Omega sqrt(N)); this result must not be misreported
as a uniform O(1) static bound for every profile.

The model is exactly PHP, not an already controlled full-parent low-energy
reduction. Full-parent source dressing, projection errors, absolute work,
physical positions/volume and preparation remain separate obligations.

## Exact family and stationary source

Retain every assumption and local energy in
`NATIVE_DEGREE_TIE_PROJECTED_SOURCE_BOUND_V001.md`: uniform held records,
carriers blank, ports off, kappa=0, N>=2, h=Omega/N, Omega>0 and U>0 fixed.
P contains all matchings of the complete bipartite candidate-edge set. Write

    H_P=C_N P-h S,
    S=sum_ij P X_ij P,
    T_u=P sum_v u_v h_v P
       =-(h/2) sum_ij(u_i^L+u_j^R)P X_ij P              (2)

for sum_v u_v=0 in the previously adopted affine lapse chart. All absolute
onsite constants remain in C_N and the original local energies; centering,
not deleting absolute energy, gives (2). The raw second contact in this
projected affine chart is zero. The unique positive ground |0> is invariant
under G=S_N(left) x S_N(right) and layer exchange. No evolved blank state or
formation attractor is substituted for this ground.

Let P_m project onto matchings of size m and let

    D_m=N!^2/[m!(N-m)!^2].

The normalized invariant vector at each m is the uniform sum over D_m graphs.
On these N+1 singlets the adjacency A0 has zero diagonal and off-diagonals

    a_m=(N-m)sqrt(m+1),   0<=m<N.                     (3)

Every matching is connected to the empty graph by deletion. Perron uniqueness
therefore places the full projected ground in this invariant block. Define
lambda0=rho(A0)>0; E_0=C_N-h lambda0.

## The entire node source occupies two standard blocks

Right permutations act transitively on matchings with a fixed occupied left
subset A of size m. The right-trivial subspace at fixed m is consequently the
permutation module on those m-subsets. For 1<=m<=N-1 its left-standard
representation occurs once: its multiplicity is the dimension of the
standard representation invariant under the subset stabilizer
S_m x S_(N-m). Such a vector is constant separately on A and its complement,
and its zero total sum leaves one dimension. At m=0,N this dimension is zero.

A concrete fixed-anchor representative is

    f_m(G)=1_(left vertex i is matched)-m/N,
    |F_m>=sum_(G of size m) f_m(G)|G>,
    ||F_m||^2=D_m m(N-m)/N^2.                          (4)

Varying i spans one standard copy with its single relation sum_i f_m=0.
Different m are orthogonal. The corresponding right-standard/left-trivial
block follows by exchanging the layers. These two G representations are
inequivalent, including N=2, and are orthogonal.

This identifies exactly the source sector, rather than assuming a radial gap
is sufficient. Each left-node source applied to the invariant ground is
right-trivial and transforms as the left permutation representation, which
contains only a singlet and a standard component. Both singlets have zero
transition weight: the uniform source is H_P and the opposite-layer source
is the zero operator on P. The same statement holds on the right. No
standard-times-standard or other representation can be reached by (2).

There is also a direct amplitude check. Write the ground amplitude on every
m-matching as phi_m>0, and use phi outside 0,...,N equal to zero. The ground
equation on a size-m graph is

    m phi_(m-1)+(N-m)^2 phi_(m+1)=lambda0 phi_m.

For the centered left anchor u_i=1-1/N, other left u=-1/N, right u=0,

    (T_anchor|0>)(G)
      =-(h/2)[phi_(m-1)-(N-m)phi_(m+1)] f_m(G).         (5)

Indeed, a matched anchor has one removable edge, while an unmatched anchor
has N-m possible additions. The ground equation subtracts their mean. At
m=0,N the source vector is exactly zero. Equation (5) explicitly exhausts
the anchor source into the invariant standard subspace (4).

## Exact standard adjacency and its gap comparison

For m=1,...,N-2, counting additions and removals gives

    P_m S|F_(m+1)>=(N-m)(N-m-1)|F_m>,
    P_(m+1) S|F_m>=m|F_(m+1)>.

For example, in an m-matching with the anchor unmatched, N-m additions
match that anchor, while the remaining (N-m)(N-m-1) additions do not.
Subtracting (m+1)/N for each target gives the first coefficient in this
display. The matched case fixes the same coefficient. The norm ratio from
(4) is (N-m)(N-m-1)/m, so normalization yields the symmetric block

    b_m=sqrt[m(N-m)(N-m-1)],   1<=m<=N-2.              (6)

There is no diagonal and no coupling to m=0,N. The entire left-standard
adjacency is this (N-1)-by-(N-1) block A1 tensored with the identity on its
N-1 polarizations; the right-standard block is identical.
For the gap argument, the explicitly closed span (4)--(6) and source action
(5) already suffice, independently of a classification of other irreducible
subspaces of the projected model.

On its interior links,

    (b_m/a_m)^2
      =m(N-m-1)/[(m+1)(N-m)]
      =1-N/[(m+1)(N-m)]
      <=(N-1)^2/(N+1)^2,                              (7)

because (m+1)(N-m)<=(N+1)^2/4. Pad A1 with zero rows/columns at m=0,N.
This gives a nonnegative matrix B on the same coordinates as A0, satisfying
0<=B<=r_N A0 entrywise, with r_N=(N-1)/(N+1). Spectral-radius monotonicity
for nonnegative matrices gives rho(A1)<=r_N lambda0. Every source-visible
excited eigenvalue therefore obeys the exact gap bound

    Delta_source >= h[lambda0-rho(A1)]
                 >=2h lambda0/(N+1).                  (8)

This does not assert that all other G sectors have the same gap. They do not
contribute to the node-source spectral measure. For N=2, A1 is the single
zero entry at m=1, so the padding and bound hold without any interior b_m.
The endpoints have not been replaced by nonexistent standard states.

No unknown eigenvalue is needed for a convenient explicit lower bound.
A normalized vector supported equally on adjacent singlet levels p,p+1
has Rayleigh quotient a_p. Taking p=floor(N/2), valid for every N>=2,

    lambda0>=a_p=(N-p)sqrt(p+1)>=N^(3/2)/(2sqrt(2)),
    Delta_source>=delta_N:=Omega sqrt(N)/[sqrt(2)(N+1)]. (9)

This is a variational lower bound, not an asserted asymptotic equality for
either the gap or lambda0. The factor h=Omega/N has not been retuned.

## Static susceptibility and physical normalization

Let dmu_u be the positive ground-state measure of T_u in PHP. The preceding
note proves

    W_u=integral dmu_u=w_N Q_u,
    w_N<=Omega^2/[4(N-1)],
    Q_u=sum_L(u-mean_L u)^2+sum_R(u-mean_R u)^2.

All its support has Delta>=delta_N by the exact source exhaustion above.
For the PLUS source H_P+theta T_u, chi_u(0) denotes the positive convention
with delta<T_u>=-chi_u(0) delta theta in the static response. Thus

    0<=chi_u(0)=2 integral dmu_u/Delta
      <=2W_u/delta_N
      <=Omega (N+1) Q_u/[sqrt(2)(N-1)sqrt(N)].           (10)

For Q_anchor=(N-1)/N this is (1). For |u_v|<=1, Q_u<=2N gives

    chi_u(0)<=sqrt(2) Omega sqrt(N)(N+1)/(N-1).          (11)

The prior fixed-time and positive-imaginary-frequency bounds also remain
valid; no pointwise bound at an undamped real-frequency resonance is implied.
This ground-state susceptibility is the negative ground-energy curvature
in the stated affine chart, not a prediction for a nonstationary state or
a curvature with omitted physical contact terms.

If a separately calibrated physical profile x_v and volume V_N are supplied,
the acceleration source is Z=sum_v x_v h_v/c^2, and (10) becomes

    chi_Z(0)/V_N
      <=Omega (N+1) Q_x/[sqrt(2)(N-1)sqrt(N)c^4 V_N].    (12)

For fixed calibrated anchor length ell, chi_Z(0)<=ell^2 times (1)/c^4.
For extended |x_v|<=R_N, the bound is O(Omega sqrt(N)R_N^2/(c^4 V_N)).
IF V_N is proportional to N and R_N stays bounded, this density vanishes
as N^(-1/2). IF instead R_N is proportional to N^(1/3), the same upper bound
can grow as N^(1/6); no vanishing static density follows for that different
conditional physical scaling. Neither volume law nor dimension is derived.

## Exact next decision

This closes the previously open anchored inverse-gap loophole in the exact
projected matching model; no spectrum histogram is needed. A claimed rescue
from the full parent must now demonstrate a source-relevant contribution
outside this projection, or controlled corrections that alter this bound,
with the same source and complete contacts. The bare 2U excluded-degree gap
does not supply that uniform theorem. Formation into the assumed stationary
state, physical clock/geometry calibration, absolute volume work and pressure
remain unproved; none is settled by (1) or by setting kappa=0.

Source ancestry: `NATIVE_DEGREE_SWITCH_CHANNEL_V001.md`, section6;
`NATIVE_DEGREE_TIE_PROJECTED_SOURCE_BOUND_V001.md`, equations (1)--(11);
and the same local energy and affine source convention of
`NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md`. Equations (4)--(10) are the new
analytic standard-sector and inverse-gap derivation, not reused numerical
evidence or a statement about the full-parent spectrum.
