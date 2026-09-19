# A009--A016 z=1 primary proof path

Date: 2026-09-16

Status: `CONDITIONAL_PHYSICAL_Z1__FINITE_EVIDENCE_COMPLETE__INTERNAL_ALL_L_PROOF_OPEN`

This packet isolates the shortest defensible path to `z=1`. It does not use or
disturb the running L14 calculation.

## Evidence boundary

The primary argument uses only:

1. the explicitly defined periodic two-leg hard-core-boson Hamiltonian;
2. the explicitly defined density observable `O_L(k)`;
3. the fixed `A009--A016` density block and its stored probability masses;
4. the independently audited bounded record-membership theorem for that block;
5. direct, hash-pinned finite-sector spectral observations as auxiliary
   corroboration only; and
6. a same-model Luttinger-liquid result, clearly labeled as an external
   physical premise.

It does **not** import earlier adjudication verdicts, stop conditions, fit
gates, adjacent-pair rules, disposition labels, URM claim machinery, gravity
criteria, or alpha arguments. The historical
[`STAGE6R4_THEOREM_PATH_SPEC.md`](STAGE6R4_THEOREM_PATH_SPEC.md) is quarantined
from this proof path because it is workflow machinery, not physics.

Two statements are kept logically separate:

- the Hamiltonian is in a `z=1` phase on the stated density interval under the
  pinned external premise; and
- the fixed record block carries probability mass above `0.50` at all five
  authenticated sizes.

Their conjunction becomes a “majority z=1 record block” only under the native
composition definition stated below. No earlier surface supplies that logical
arrow.

## 1. Exact model and observable

For even `L`, let the vertices be `(a,x)` with rail `a in {0,1}` and
`x in Z/LZ`. In the sector containing `q` hard-core bosons, define

```text
H_L = - sum_(x,a) (b^dagger_(a,x) b_(a,x+1) + h.c.)
      - sum_x     (b^dagger_(0,x) b_(1,x)   + h.c.).
```

Thus the leg and rung hoppings are both one, the boundary is periodic, and the
density convention is `rho=q/(2L)`.

The stored graph uses shifted rung labels. The permutation `x=i-a` maps it
exactly to the graph above and induces a unitary permutation of the occupation
basis. This can be checked directly from the edge list in
[`compute_phase_screen.py`](../DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/compute_phase_screen.py#L81-L89)
and the exchange matrix elements at
[`compute_phase_screen.py`](../DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/compute_phase_screen.py#L175-L200).
Those files are raw provenance for the operator; none of their gates or
classifications is imported.

Use the unnormalized Fourier convention

```text
n_a(k) = sum_(x=0)^(L-1) exp(i k x) n_(a,x),
```

with no `1/sqrt(L)` factor. At `k_L=2 pi/L`, define the z=1 observable in the
standard ladder coordinates by

```text
O_L(k_L) = n_0(k_L) + exp(i k_L) n_1(k_L).
```

The stored implementation of that unnormalized mode is at
[`compute_phase_screen.py`](../DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/compute_phase_screen.py#L466-L474),
in the raw source file with SHA-256
`e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7`.

With `n_s=n_0+n_1` and `n_a=n_0-n_1`, the exact identity is

```text
O_L(k) = (1+exp(i k))/2 n_s(k) + (1-exp(i k))/2 n_a(k).
```

The symmetric coefficient has squared magnitude `cos^2(pi/L)>0`. This proves
that `O_L` contains the total-density channel. It does not, by algebra alone,
prove that the channel has low-energy spectral weight.

## 2. Fixed majority record block

The fixed cells `A009--A016` form the exact half-open interval

```text
I = [7/48,13/48).
```

Their deduplicated sectors and stored `pbar` masses are:

| L | selected q sectors | pbar mass |
|---:|:---|---:|
| 4 | 1--2 | `0.7260206189754993` |
| 6 | 2--3 | `0.5846615608350367` |
| 8 | 2--4 | `0.7373965730354166` |
| 10 | 3--5 | `0.6500987927669427` |
| 12 | 4--6 | `0.5695649839332784` |

Every value is strictly above `0.50`. The exact finite combinatorial
membership result is proved in
[`L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md`](../L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md)
and independently audited in
[`AUDIT_L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md`](../AUDIT_L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md).
The theorem applies separately at `L=4,6,8,10,12`; it is not an all-`L`
continuation theorem.

## 3. Native finite-sector response evidence

For the exact observable above, let

```text
w_j     = ||P_j O_L(k_L)|0>||^2,
S       = sum_(omega_j>0) w_j,
R_low   = w_*/S,
w_*     = weight of the lowest threshold-stable active pole.
```

Hence `w_*=S R_low` is an algebraic identity. It is not a confidence bound.
All 40 atom/size assignments reduce to 13 unique sectors:

| L,q | atoms | S | R_low | w_* |
|:---|:---|---:|---:|---:|
| 4,1 | A009--A011 | `1.0000000000` | `0.5000000000` | `0.5000000000` |
| 4,2 | A012--A016 | `1.6666666667` | `0.4280947078` | `0.7134911797` |
| 6,2 | A009--A012 | `1.4455602200` | `0.6685010572` | `0.9663585353` |
| 6,3 | A013--A016 | `1.7718181839` | `0.6328017721` | `1.1212096865` |
| 8,2 | A009 | `1.3232049426` | `0.7849688303` | `1.0386746360` |
| 8,3 | A010--A013 | `1.5890568291` | `0.7491511325` | `1.1904437232` |
| 8,4 | A014--A016 | `1.7838381848` | `0.7328298207` | `1.3072498171` |
| 10,3 | A009--A010 | `1.4619706788` | `0.8165714982` | `1.1938035875` |
| 10,4 | A011--A014 | `1.6405593775` | `0.7984096120` | `1.3098383761` |
| 10,5 | A015--A016 | `1.7752583347` | `0.7891533299` | `1.4009510263` |
| 12,4 | A009--A011 | `1.5293865686` | `0.8417832706` | `1.2874120277` |
| 12,5 | A012--A015 | `1.6601988638` | `0.8311603547` | `1.3798914765` |
| 12,6 | A016 | `1.7619394740` | `0.8251471863` | `1.4538593994` |

The smallest observed residue is `0.4280947078`; the smallest pole weight is
`0.5`. L4--L8 use complete finite-sector diagonalization. L10/L12 use
independently implemented Target and Blind calculations; across every selected
row and diagnostic neighbor, their maximum relative disagreement is
`3.07e-14`.

These are direct, numerically certified finite-system observations with
residual, projection, threshold-stability, and independent-reproduction
checks. They are not heuristic. They are also not interval-arithmetic proofs
and do not establish `liminf_(L->infinity) w_*(L)>0`. In particular,
`Delta_act`, `R_low`, and `w_*` retain the finite calculation's numerical
active-pole convention. That convention is not imported as the mathematical
definition of an all-`L` pole, and none of these rows is a premise of the
conditional theorem in section 5.

The read-only extractor
[`analyze_centerline.py`](analyze_centerline.py) pins the manifest and data
indices directly. It does not consume any earlier verdict or decision rule.

## 4. Independent finite-size z=1 diagnostics

At the center sector `q=L/2`, the script compares the `O_L` response gap with
the independent charge curvature

```text
Delta_Q(L) = E_0(q+1)+E_0(q-1)-2E_0(q).
```

| L | L Delta_act | L Delta_Q | L Delta_act/(2 pi) | finite K_s estimator |
|---:|---:|---:|---:|---:|
| 4 | `9.852301989532` | `3.402434876961` | `1.568042562468` | `0.723915544736` |
| 6 | `10.004229114110` | `3.300822390538` | `1.592222515334` | `0.757707317333` |
| 8 | `10.128523509927` | `3.285804397155` | `1.612004582827` | `0.770627393303` |
| 10 | `10.191692872475` | `3.277395076103` | `1.622058299129` | `0.777423276399` |
| 12 | `10.227194665717` | `3.272973656908` | `1.627708585012` | `0.781185226173` |

Free-power fits give exponents `0.965001779728` and `1.033649832164` for the
two observables. Their opposite-side convergence is strongly consistent with
`1/L`; a five-point fit is not itself an asymptotic proof. The `K_s` column is
the Luttinger-hydrodynamic estimator

```text
K_s(L) = pi [L Delta_act/(2 pi)] / [2 L Delta_Q].
```

It is meaningful under the Luttinger interpretation and is not used as an
independent theorem premise.

## 5. Conditional thermodynamic z=1 theorem

Adopt the following explicit external premise:

> **LL-P.** For the clean periodic two-leg hard-core-boson ladder with
> `t=t_perp=1` and every density `rho in I`, the thermodynamic low-energy theory
> has one symmetric Luttinger mode with `1/2<=K_s(rho)<=1` and
> `0<v_s(rho)<infinity`, a gapped antisymmetric sector, and
> `omega(k)=v_s(rho)|k|+o(|k|)`.

Crépin, Laflorencie, Roux, and Simon analyze this same model and identify that
phase away from the half-filled rung-Mott line; see
[arXiv:1103.5988](https://arxiv.org/abs/1103.5988) and
[Phys. Rev. B 84, 054517](https://doi.org/10.1103/PhysRevB.84.054517).
Carrasquilla, Becca, and Fabrizio independently corroborate the clean phase
diagram in [arXiv:1102.3339](https://arxiv.org/abs/1102.3339).

The complete interval `I` lies strictly inside `0<rho<1/2`. In the convention
of LL-P, the smooth total density has fixed normalization

```text
delta n_s = -(sqrt(2)/pi) partial_x Phi_s.
```

For the sequence `k_L=2 pi/L`, the symmetric one-phonon contribution to the
defined observable therefore has asymptotic weight

```text
W_L(rho) = 2 K_s(rho) cos^2(pi/L) + o(1),
```

at energy `v_s(rho)|k_L|+o(1/L)`. The leading term tends to `2K_s>=1`.
The `o(1)` term is not treated as an exact finite-L equality or finite-L lower
bound. It proves nonzero thermodynamic residue and linear dispersion under
LL-P. Therefore:

> **Conditional physical conclusion.** Under LL-P, this exact Hamiltonian has
> dynamical exponent `z=1` throughout every density cell in `A009--A016`, and
> the explicitly defined observable sees the symmetric mode in the scaling
> limit.

The detailed derivation is in
[`CONDITIONAL_Z1_BRIDGE_THEOREM.md`](CONDITIONAL_Z1_BRIDGE_THEOREM.md).

## 6. Proposed native composition rule and exact claim boundary

A clean project-level definition could call a block a **majority z=1 record
block at the sampled sizes** only when:

1. one fixed density block has audited bounded record membership at each
   sampled size;
2. its deduplicated stored probability mass is greater than `0.50` at each
   sampled size; and
3. every density in the full block belongs to a `z=1` phase under one stated
   physical premise or internal theorem.

If the project deliberately adopts that definition, then under LL-P
`A009--A016` satisfies it at `L=4,6,8,10,12`. The definition is proposed here
for review; it is not silently inherited from any older surface. The resulting
claim would be a conditional physical result plus authenticated finite record
arithmetic, not an unconditional mathematical derivation of the nonintegrable
ladder phase or an all-`L` record-continuation theorem.

The current status is:

```text
exact finite Hamiltonian/probe identity:       PROVED
A009--A016 bounded record membership:          PROVED; independent audit PASS
A009--A016 pbar mass >0.50 at five sizes:      AUTHENTICATED; dual reconstruction
finite probe visibility in all 13 sectors:     NUMERICALLY CERTIFIED
z=1 on I under same-model LL literature:       CONDITIONAL PHYSICAL THEOREM
unconditional repository-internal all-L z=1:  OPEN
```

The clean internal route and its exact missing theorem are recorded in
[`INTERNAL_Z1_THEOREM_ROUTE.md`](INTERNAL_Z1_THEOREM_ROUTE.md). It derives only
from the Hamiltonian and native probe; in particular, it does not fill the open
line with machinery imported from another surface.

The exact response sum rule and its limitations are recorded in
[`EXACT_RESPONSE_SUMRULE_BOUND.md`](EXACT_RESPONSE_SUMRULE_BOUND.md), with an
independent audit in
[`AUDIT_EXACT_RESPONSE_SUMRULE_BOUND.md`](AUDIT_EXACT_RESPONSE_SUMRULE_BOUND.md).

## Reproduce

```sh
python3 DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/analyze_centerline.py
```
