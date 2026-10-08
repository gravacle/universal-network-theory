# FY ordered-source symmetry closure V001

Date: 2026-09-27. Analytic review only; no source execution, numerical physics,
hydration, historical edits, or remote work.

**Result:** the inherited finite FY parent supplies its opposite-momentum
residues by an exact antiunitary reality symmetry. This closes the ordering
qualification in the Q4 candidate audit for the contact-free pole correlator.
It does **not** supply the native second-source contact or a bare Hessian.

## 1. Hash-bound premises and custody

Paths are relative to the project root. All four files were resident when
inspected; hashes were measured for this review.

| File | SHA-256 |
| --- | --- |
| `program-worktree/LANE_GRA_FY_F3_Q4_NATIVE_SUPPORT_M1_COMPLETE_H6_RESPONSE_V001/THEOREM.md` | `8db3dd16c36e0205b5c98fc3154e8a2f1876d243c3c1d2068424c1276ee68f28` |
| Same FY folder, `derive_native_support_m1_response.py` | `4273d0cd70b5b91cc335ddf915ba0a220530da8dd7b6403a2828b72a01664806` |
| `program-worktree/LANE_GRA_FO_F3_Q4_FINITE_TT_FOUR_POINT_V001/INDEPENDENT_AUDIT.md` | `84d8c02c3e560198f6a9fae04f5ee81bc72c98354e02f1f58d506a8c3171c453` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/Q4_ACTUAL_PARENT_HESSIAN_CANDIDATE_AUDIT_V001.md` | `04c29a6d4e1dfd6ed30fa816d90b85bb75aa8a26d9bcd4955a63ec9579095032` |

The FO audit owns a connected 180-state legal-flip component with real symmetric
Hamiltonian `H0=-J6 A`, `J6>0`, where A is its nonnegative adjacency matrix.
Translation T is a real permutation preserving that component and commuting
with H0. The dataless FO implementation was not read or replayed: this proof
inherits those audited parent premises, rather than independently recertifying
the component census.

The FY construction has rational real local ledgers, real diagonal insertions,
and the same averaged ring coefficient at `(row,column)` and `(column,row)`
(source around lines 888–918). Its six-channel change of basis is real.
Consequently every local insertion q is real symmetric. Fourier phases are
the only complex factors. Write `Q_+=Q_1`, `Q_-=Q_29`; then
`Q_- = Q_+* = Q_+†`, channel by channel. The complete translated support has
momentum m=1 on Z30, with normalization `1/sqrt(60)` as frozen in FY.

## 2. Exact symmetry and ordered pole kernel

Perron–Frobenius applied to the connected nonnegative A gives a unique,
strictly positive normalized ground vector of H0. Choose it real. Translation
must preserve this unique positive ground vector, so `T|0>=|0>`.
Componentwise complex conjugation K therefore satisfies

`K H0 K = H0`, `K|0>=|0>`, and `K Q_+ K=Q_-`.

This is the finite parent's antiunitary reality symmetry; no identification
with microscopic spin time reversal or spatial inversion is needed.

Let P_delta be the **full-energy** spectral projector at `E0+delta`, delta>0,
including its degeneracies. It is real because H0 is real. A momentum-resolved
projector need not be real: conjugation exchanges its opposite momenta.
Define the Hermitian positive-semidefinite channel matrix

`R_AB(delta)=<0|Q_-A P_delta Q_+B|0>`.

Conjugation gives `R^-_AB=<0|Q_+A P_delta Q_-B|0>=R_AB*`.
For the zero-temperature, infinite-Euclidean-time connected correlator
`G_-+,AB(tau)=<T_tau Q_-A(tau) Q_+B(0)>_c`, its positive-time residue is R_AB;
its negative-time residue is `R^-_BA=R_AB`. Thus, with hbar=1,

`G_-+,AB(i omega) = sum_delta 2 delta R_AB(delta)/(delta^2+omega^2)`.

The opposite ordered block is its complex conjugate. Translation invariance
and `2m=2 != 0 (mod 30)` kill the same-sign blocks `G_++` and `G_--` and the
one-point functions. No accidental degeneracy or real momentum eigenbasis is
assumed. Existing positive-momentum residues therefore determine the entire
contact-free ordered pole kernel, subject to their existing numerical custody.

For Hermitian quadratures

`X=(Q_++Q_-)/sqrt(2)`, `Y=(Q_+-Q_-)/(i sqrt(2))`,

each gap has the real symmetric residue

```
R_real = [ Re R    Im R ]
         [-Im R    Re R ].
```

For real x,y its quadratic form is `(x-i y)† R (x-i y)`, so it is positive
semidefinite and its real rank is twice the complex rank of R. The full
12-real-channel kernel is `sum 2 delta R_real/(delta^2+omega^2)`; the mixed
cosine/sine block must not be silently discarded.

## 3. Source normalization, static response, and contacts

FY fixes `Q_a=-2 H_a` at zero source. For real quadrature sources write

`H[j]=H0-(1/2)j_a Q_a+(1/2)j_a j_b B_ab+O(j^3)`,

where `B_ab=H_ab|0` is an operator. Define **W=log Z**, with an instantaneous
Hamiltonian source and the usual Euclidean evolution convention. Then

`W''_ab(tau,tau')=(1/4)G^Q_ab(tau-tau')-<B_ab> delta(tau-tau')`.

For static sources use `w=lim_(beta->infinity) W/beta=-E0(j)`, so
`w''=(1/4)G^Q(i0)-<B>=-E0''`. This is a generating-functional Hessian, not
the identically normalized susceptibility of a fixed Q observable.

Equivalently, take `H_linear=H0-(j_- Q_+ + j_+ Q_-)/2`, with
`j_-=(j_X-i j_Y)/sqrt(2)` and `j_+=(j_X+i j_Y)/sqrt(2)`. If FY's stored
static matrix is `F=sum_delta R(delta)/delta`, then

`G_-+(i0)=2F`,

`w''_(j+,j-)=F/2` for this deliberately linear probe,

`d<Q_->/d j_-=G_-+(i0)/2=F` for its fixed observable.

The native mixed Hessian instead has the additional
`-<H_(j+,j-)>` contact. If one differentiates the source-dependent observable
`Q(j)=-2H_j`, its response is `2W''`, including the explicit contact.
Temporal/controller or constraint-dependent source prescriptions require their
own corresponding terms; the instantaneous formula does not supply them.

FY's first-source insertion construction does not determine H_ab. In
particular, eliminating states and differentiating Feshbach folds can generate
second-source terms even when a microscopic source was linear. Setting B=0
defines a useful separate probe benchmark, not an authenticated native contact.

An exact nonidentifiability witness is the family
`H_C(j)=H0-j_a Q_a/2+j_a j_b C_ab I/2`, for real symmetric C.
Every member shares H0, all first derivatives at zero, and every source-off Q
correlator, but its W'' differs by `-C_ab`. A translation-invariant paired
opposite-momentum quadratic scalar suffices, so imposing the reality and
translation symmetries does not remove this ambiguity. This does not authorize
adding C to the frozen parent: the original nonlinear source deformation must
choose the actual contact.

## 4. What is and is not completed

The ordered-pole ambiguity is closed analytically for this inherited parent.
No new residues, gaps, exact ranks, or physical observables were computed.
The candidate audit's affine-inverse theorem remains conditional on an exact
complete PSD residue factorization with the stated rank sum. FY's sampled
numerical ranks nominate that case; this symmetry proof does not certify them
exactly or validate numerical grouping/cutoff decisions anew.

Native second-source contacts remain missing. Even a completed source Hessian
and its response inverse would not thereby be a bare Wilsonian Hessian, a new
determinant species count, a continuum heat kernel, or a gravity/dark-sector
prediction. The constructive gain is smaller and exact: no extra opposite-
momentum calculation is needed to complete this finite ordered pole block.

Independent algebra checks: root and the budget-review agent confirmed the
ordering, realification signs, and full-energy-projector qualification.
