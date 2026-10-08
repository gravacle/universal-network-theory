# Exact local Coulomb Born contact and the remaining FY contact gap

Date: 2026-09-27. Read-only source inspection and hand algebra; no source
execution, numerical physics, hydration, remote work, or historical edits.

**New result:** the existing conditional FU Coulomb family determines its local
mutual-pair Born contact exactly in deformation-distance coordinates. The
unknown second-order FY strain chart is a coordinate/path-acceleration issue
for this subterm, not a missing radial constitutive law. The complete FY
contact nevertheless remains uncomputed and under-specified elsewhere.

## 1. What the resident source actually fixes

FU theorem equations FU15–24 assume the full local family

`H_pair(F)=(Ud/2) sum_(a<b) [n_ab^T F^T F n_ab]^(-1/2) P_ab`,

where `P_ab=Z_a Z_b`, and n_ab is the unit sibling root. The law is not merely
a first-order Taylor jet: the ideal fixed-coupling central kernel is explicitly
`g(x)=x^(-1/2)`. It is, however, an **assumed conditional physical completion**
of the local degree-pair block, not an independently derived distance law of
the original distance-free F3 action. FU's audit retains the unresolved global
shared-link, charge/field, boundary, and physical-length premises.

FU17 freezes only `F(j)=I-j/2+O(j^2)`. FV-PURE freezes the *complete nonidentity
first derivative*. Neither statement fixes every quadratic term in the full
source-deformed Hamiltonian. Resident FX audit code also carries base and first
derivative packets, not second-source packets. The earlier FS verifier
explicitly retains `O(j^2)` contacts without determining them.

## 2. Determined contact in Gram coordinates

Use the positive deformation Gram matrix `C=F^T F`, near `C=I`. This is an
explicit coordinate for local squared distances, not an emergent spacetime
metric. For symmetric variations S,T set `r_ab(S)=n_ab^T S n_ab`. Then

`D_C H_pair[S]=-(Ud/4) sum r_ab(S) P_ab`,

`B_pair^C[S,T]=D_C^2 H_pair[S,T]`

`              =(3Ud/8) sum r_ab(S) r_ab(T) P_ab`.

These follow directly from `g'(1)=-1/2` and `g''(1)=3/4` and are exact local
operator derivatives of the already displayed conditional family. No arbitrary
linear probe or new fitted radial coefficient was inserted.

The j chart has `D_j C[S]=-S`. Its contact therefore obeys the exact chain rule

`B_pair^j[S,T]=B_pair^C[S,T]`

`              -(Ud/4) sum n_ab^T C''_j[S,T] n_ab P_ab`.

The second line is geometric coordinate/path acceleration multiplied by the
first derivative. It is not an independent missing Coulomb interaction. A
declared Gram-linear path `C=I-j` makes it zero, but that choice must not be
retroactively attributed to FY's first-order-only j convention.

As a cross-check in F coordinates, for matrix variations A,B at F=I,

`D_F^2 H_pair[A,B]=(Ud/2) sum [3(n·A n)(n·B n)-(A n)·(B n)] P_ab`.

With `F'_j[S]=-S/2`, the j Hessian is consequently

`(Ud/8) sum [3 r_ab(S)r_ab(T)-(S n_ab)·(T n_ab)] P_ab`

`  -(Ud/2) sum n_ab^T F''_j[S,T] n_ab P_ab`.

This equals the Gram-coordinate chain rule. Different accelerated strain paths
can share the same FY Q operator and have different ordinary second
derivatives, without contradicting their common local constitutive family.

## 3. Exact local witness and sign boundary

Label the tetrahedral rays as FU01:
`n1=(+++)/sqrt(3)`, `n2=(+--)/sqrt(3)`,
`n3=(-+-)/sqrt(3)`, `n4=(--+)/sqrt(3)`.
Take the unnormalized traceless direction `S=diag(1,-1,0)` in C coordinates.
The roots 14 and 23 have `r(S)=0`; the other four have `r(S)^2=1/4`. Hence

`B_pair^C[S,S]=(3Ud/32)(P12+P13+P24+P34)`.

On the local ice state occupying links 1 and 4 (or its complement), all four
displayed pair eigenvalues are -1, so this contact is `-3Ud/8`. On ice states
occupying 1 and 2 or 1 and 3 (and their complements), it is zero. Thus this
is a nonidentity contact already at the local block; it cannot generally be
dismissed as a reference constant. Positive scalar `g''(1)` does **not** make
the operator-valued Born matrix positive: the pair operators have signed
eigenvalues. This subterm alone gives no full stability or response verdict.

## 4. Precisely what still prevents a native FY Hessian

1. The chart or actual driven path must be specified through second order, or
   the full response must consistently be posed in the declared C coordinates.
2. The unchanged one-edge hopping source needs its actual nonlinear amplitude
   law. Its first derivative does not fix its second derivative.
3. Identity/self/reference derivatives and any allowed residual, common-mode,
   boundary, controller, and port contacts must be retained once. FV-PURE's
   first-derivative restriction cannot eliminate terms starting at second order.
4. The fixed Feshbach map and endpoint/fold prescription must be differentiated
   twice: numerator second derivatives, paired first insertions, every virtual
   gap second derivative, and all generated folds contribute. The local Born
   operator above is not that completed ice-effective contact.
5. The same native spatial support, source normalization, and real cosine/sine
   convention must be used before combining contacts with the FY pole kernel.

In the preceding closure note's convention `W=log Z`, the completed kernel is
`W''=G_Q/4-<H''>`, not the Born term alone. None of the foregoing derives a
spacetime metric, a bare Hessian, or a gravity/dark-sector effect.

## 5. Resident-source custody

All paths below are relative to `program-worktree/`. Files were checked with
`ls -lO` before reading. Dataless BS/FW/FX primary files were skipped; no
historical verifier or imported code was run.

| Source | SHA-256 |
| --- | --- |
| `LANE_GRA_FU_F3_Q4_PAIR_RESOLVED_MAXWELL_DPAR_DERIVATION_V001/THEOREM.md` (full read; FU15–24) | `f088346f72861b3b11ae737fe6b882d43da9e747fc1d1d1f6bd446a7fd2b6272` |
| Same FU folder, `INDEPENDENT_HOSTILE_AUDIT.md` (full read) | `6f859779566177b5999cfe02c01cd569c5bd7b0b4ec2b21b0b3e79ebf26f9277` |
| `LANE_GRA_FV_F3_Q4_COULOMB_DPAR_PROJECTED_SOURCE_RANK_V001/INDEPENDENT_HOSTILE_AUDIT/INDEPENDENT_HOSTILE_AUDIT.md` (section 2) | `3801fd9ba6ba3c0fe80c9f4792abfdeb6dd7c37c7145663be05b4d56f8160723` |
| `LANE_GRA_FS_F3_Q4_COMPLETE_SOURCE_RANK_AUDIT_V001/verify_complete_source_rank_audit.py` (lines 299–370) | `67791b0804cb0f465eb41a73051e6d439679357c32931e37c835c7308423dc63` |
| `LANE_GRA_FX_F3_Q4_COULOMB_COMPLETE_H6_SOURCE_RESPONSE_V001/INDEPENDENT_HOSTILE_AUDIT/audit_complete_h6_source.py` (lines 316–436) | `c637c49df10920f25655b2127fc17f6225b8f5aa9e2d4cb19a158fb5702d3aeb` |
