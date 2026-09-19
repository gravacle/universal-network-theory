# Conditional physical z=1 theorem on A009--A016

Date: 2026-09-16

Status: `CONDITIONAL_ON_PINNED_SAME_MODEL_LL_PREMISE__INTERNAL_ALL_L_PROOF_OPEN`

## 1. Scope and evidence boundary

This note proves a conditional statement about one explicitly defined
Hamiltonian and observable. It then reports, separately, the independently
audited record-block mass. It imports no prior adjudication verdict, gate,
stop condition, fit predicate, adjacent-pair rule, disposition label, URM
rule, gravity criterion, or alpha argument.

Historical source files are cited only to establish the stored operator and
data provenance. Their workflow logic is not a theorem premise.

## 2. Exact finite model

For even `L`, let

```text
V_L = {(a,x): a in {0,1}, x in Z/LZ}.
```

On the hard-core occupation basis with exactly `q` particles, define

\[
H_{L,q}=-\sum_{x,a}(b^\dagger_{a,x}b_{a,x+1}+\mathrm{h.c.})
        -\sum_x(b^\dagger_{0,x}b_{1,x}+\mathrm{h.c.}).       \tag{1}
\]

The stored graph has two periodic rails and shifted connectors. The vertex
permutation `x=i-a` maps those connectors to the rungs of (1), while preserving
each rail cycle. Its induced occupation-basis permutation is unitary. The raw
edge construction is visible in
[`compute_phase_screen.py`](../DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/compute_phase_screen.py#L81-L89),
and its hard-core exchange matrix element is `-1` at
[`compute_phase_screen.py`](../DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/compute_phase_screen.py#L175-L200).

Therefore the stored finite operator is exactly (1), with periodic boundary,
`t=t_perp=1`, and density convention

\[
\rho={q\over 2L}.                                          \tag{2}
\]

A chemical-potential term is scalar in a fixed-`q` sector and changes neither
the eigenvectors nor the excitation gaps used here.

## 3. Exact observable

Use the unnormalized convention

\[
n_a(k)=\sum_{x=0}^{L-1}e^{ikx}n_{a,x},                   \tag{3}
\]

with no `1/sqrt(L)` factor. At `k_L=2 pi/L`, define

\[
O_L(k_L)=n_0(k_L)+e^{ik_L}n_1(k_L).                       \tag{4}
\]

This is the stored total-rail Fourier mode expressed after the same lower-rail
relabeling. Its raw implementation is at
[`compute_phase_screen.py`](../DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/compute_phase_screen.py#L466-L474)
in the source file with SHA-256
`e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7`.
Put `n_s=n_0+n_1` and `n_a=n_0-n_1`. Direct algebra gives

\[
O_L(k)=c_s(k)n_s(k)+c_a(k)n_a(k),                         \tag{5}
\]

where

\[
c_s(k)={1+e^{ik}\over2},\qquad c_a(k)={1-e^{ik}\over2}.   \tag{6}
\]

Consequently

\[
|c_s(k_L)|^2=\cos^2(\pi/L)>0.                             \tag{7}
\]

Equation (7) proves that the observable contains the symmetric density
channel. It does not alone prove spectral weight at low energy.

## 4. Fixed density interval

The manifest cells are:

| atom | exact density cell |
|:---|:---|
| A009 | `[7/48,5/32)` |
| A010 | `[5/32,7/40)` |
| A011 | `[7/40,3/16)` |
| A012 | `[3/16,5/24)` |
| A013 | `[5/24,7/32)` |
| A014 | `[7/32,9/40)` |
| A015 | `[9/40,11/48)` |
| A016 | `[11/48,13/48)` |

They are adjacent and have exact union

\[
I=[7/48,13/48).                                           \tag{8}
\]

The source manifest is
[`AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003R1.json`](../DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003/AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003R1.json),
SHA-256
`292124df4e1d349827753145ce1dd4be32e073db6d657f30737227edd488184a`.

Since `0<7/48<13/48<1/2`, every density in every cell lies strictly away from
the vacuum and the half-filled rung-Mott line.

## 5. Pinned external physical premise

The conditional premise is:

> **LL-P.** For the clean periodic two-leg hard-core-boson ladder (1), with
> `t=t_perp=1`, each fixed density `rho in I` has a thermodynamic low-energy
> theory consisting of one gapless symmetric Luttinger mode and a gapped
> antisymmetric sector. Its parameters satisfy `1/2<=K_s(rho)<=1` and
> `0<v_s(rho)<infinity`, and the symmetric dispersion is
> `omega(k)=v_s(rho)|k|+o(|k|)`.

The content pin is F. Crépin, N. Laflorencie, G. Roux, and P. Simon,
“Phase diagram of hard-core bosons on clean and disordered two-leg ladders:
Mott insulator--Luttinger liquid--Bose glass,”
[`arXiv:1103.5988v1`](https://arxiv.org/abs/1103.5988v1), published as
[*Phys. Rev. B* **84**, 054517 (2011)](https://doi.org/10.1103/PhysRevB.84.054517).
The paper uses density `N/(2L)`, identifies one gapless symmetric mode away
from half filling, and gives `K_s` between `1/2` and `1` with a finite sound
velocity.

J. Carrasquilla, F. Becca, and M. Fabrizio independently corroborate the clean
phase domain in [`arXiv:1102.3339v1`](https://arxiv.org/abs/1102.3339v1),
published as
[*Phys. Rev. B* **83**, 245101 (2011)](https://doi.org/10.1103/PhysRevB.83.245101).

LL-P is established many-body physics supported by bosonization, RG, QMC, and
DMRG. It is not presented as a rigorous mathematical theorem proved in this
repository.

## 6. Conditional probe visibility and z=1

In the normalization of LL-P, the smooth total density is

\[
\delta n_s(x)=-{\sqrt2\over\pi}\partial_x\Phi_s(x).       \tag{9}
\]

Canonical quantization of the Gaussian symmetric mode gives, for each fixed
`rho in I`,

\[
\|P_{1s}(k)n_s(k)|0\rangle\|^2
 ={L K_s(\rho)|k|\over\pi}+o(L|k|),                       \tag{10}
\]

at energy

\[
\omega_s(k)=v_s(\rho)|k|+o(|k|).                         \tag{11}
\]

The symmetric and antisymmetric operators have opposite rail parity, so the
antisymmetric term in (5) cannot cancel the symmetric pole. Combining
(5)--(7) with (10), at `k_L=2 pi/L`, yields

\[
W_L(\rho)=2K_s(\rho)\cos^2(\pi/L)+o(1).                  \tag{12}
\]

The leading term tends to `2K_s(rho)>=1`. Thus, for each fixed `rho in I`,
the scaling-limit residue is nonzero and the observed mode has energy
proportional to `1/L`.

Equation (12) is asymptotic. It is not an exact equality or lower bound at
`L=4,6,8,10,12`, and no sign is assigned to its finite-size correction.

### Conditional theorem

Under LL-P, the exact Hamiltonian (1) has dynamical exponent

\[
z=1                                                       \tag{13}
\]

for every fixed density `rho in I`, and the explicitly defined observable
`O_L(k_L)` has nonzero overlap with its symmetric low-energy mode in the
thermodynamic scaling limit.

This conclusion follows from the same-model identity, not analogy to a
different Hamiltonian.

## 7. Independent finite-size observations

For a finite sector, define

\[
w_j=\|P_jO_L(k_L)|0\rangle\|^2,\quad
S=\sum_{\omega_j>0}w_j,\quad
R_{\rm low}={w_*\over S}.                                \tag{14}
\]

The 40 atom/size assignments reduce to 13 distinct sectors. Direct spectral
calculation gives:

| L,q | S | R_low | w_* |
|:---|---:|---:|---:|
| 4,1 | `1.0000000000` | `0.5000000000` | `0.5000000000` |
| 4,2 | `1.6666666667` | `0.4280947078` | `0.7134911797` |
| 6,2 | `1.4455602200` | `0.6685010572` | `0.9663585353` |
| 6,3 | `1.7718181839` | `0.6328017721` | `1.1212096865` |
| 8,2 | `1.3232049426` | `0.7849688303` | `1.0386746360` |
| 8,3 | `1.5890568291` | `0.7491511325` | `1.1904437232` |
| 8,4 | `1.7838381848` | `0.7328298207` | `1.3072498171` |
| 10,3 | `1.4619706788` | `0.8165714982` | `1.1938035875` |
| 10,4 | `1.6405593775` | `0.7984096120` | `1.3098383761` |
| 10,5 | `1.7752583347` | `0.7891533299` | `1.4009510263` |
| 12,4 | `1.5293865686` | `0.8417832706` | `1.2874120277` |
| 12,5 | `1.6601988638` | `0.8311603547` | `1.3798914765` |
| 12,6 | `1.7619394740` | `0.8251471863` | `1.4538593994` |

All weights are positive. The smallest `R_low` is `0.4280947078`; the
smallest `w_*` is `0.5`. L4--L8 are complete finite diagonalizations.
L10/L12 have independent Target and Blind realizations, agreeing on the
consumed observables to at worst `3.07e-14` relative.

These facts establish numerical finite-L visibility in every selected sector.
They do not establish a uniform thermodynamic lower bound. They independently
corroborate, but are not substituted for, LL-P.

The direct hash and numerical checks are reproduced by
[`analyze_centerline.py`](analyze_centerline.py).

## 8. Separate record-block result

The bounded record-membership theorem and its independent hostile audit are:

- [`L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md`](../L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md)
- [`AUDIT_L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md`](../AUDIT_L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md)

After sector deduplication, the authenticated masses are:

| L | selected q | pbar mass |
|---:|:---|---:|
| 4 | 1--2 | `0.7260206189754993` |
| 6 | 2--3 | `0.5846615608350367` |
| 8 | 2--4 | `0.7373965730354166` |
| 10 | 3--5 | `0.6500987927669427` |
| 12 | 4--6 | `0.5695649839332784` |

Every value is above `0.50`. This is an authenticated finite record result,
not a dynamical-exponent theorem.

## 9. Composition and exact ceiling

The present packet has proved the following implication:

```text
LL-P
  + exact identity with the clean t=t_perp=1 ladder
  + exact full-cell inclusion I subset (0,1/2)
  + exact symmetric component of O_L
  => conditional physical z=1 on I with thermodynamic probe visibility.
```

Separately:

```text
audited bounded membership of A009--A016
  + authenticated deduplicated pbar arithmetic
  => record-block mass >0.50 at L=4,6,8,10,12.
```

A project-level “majority z=1 record block” statement requires an explicit
native definition joining those two propositions. It must not be inherited
from a historical gate. A proposed definition is recorded in
[`README.md`](README.md#L224-L245) for deliberate review.

The open obligations are:

- a repository-internal proof of LL-P for this nonintegrable ladder;
- a uniform all-`L` record-membership/mass continuation theorem; and
- an analytic or interval-certified finite-L residue bound, if one is desired
  independently of the thermodynamic premise.

No gravity or alpha claim follows from this theorem.
