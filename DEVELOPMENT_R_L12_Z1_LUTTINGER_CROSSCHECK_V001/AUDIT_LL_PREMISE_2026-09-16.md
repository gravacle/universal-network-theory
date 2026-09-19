# Independent audit of the clean-ladder Luttinger premise

Date: 2026-09-16

Status: `PASS__CONDITIONAL_EXTERNAL_PHYSICS_PREMISE_VERIFIED`

## 1. Scope and pinned inputs

This audit asks whether the external many-body result used by the conditional
`z=1` bridge concerns the same Hamiltonian, density convention, density domain,
low-energy mode, and observable channel as the repository calculation. It also
checks the normalization of the claimed low-energy density-pole weight.

The audited repository inputs are:

- [`CONDITIONAL_Z1_BRIDGE_THEOREM.md`](CONDITIONAL_Z1_BRIDGE_THEOREM.md),
  SHA-256
  `6353aafed694f2598fb72384bc44e2c1e5bada50262ded73919896141b2ce645`;
- [`compute_phase_screen.py`](../DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/compute_phase_screen.py),
  SHA-256
  `e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7`.

Both digests were recomputed before this audit was written and matched the
pinned values above.

The primary external source is:

- F. Crepin, N. Laflorencie, G. Roux, and P. Simon, "Phase diagram of
  hard-core bosons on clean and disordered two-leg ladders: Mott
  insulator--Luttinger liquid--Bose glass," *Physical Review B* **84**,
  054517 (2011),
  [DOI 10.1103/PhysRevB.84.054517](https://doi.org/10.1103/PhysRevB.84.054517),
  [`arXiv:1103.5988v1`](https://arxiv.org/abs/1103.5988v1).

## 2. Same-model and density-convention check

Equation (1.1) of Crepin *et al.* is the clean hard-core-boson ladder

\[
 H=-t\sum_{x,a}(b^\dagger_{a,x}b_{a,x+1}+\mathrm{h.c.})
   -t_\perp\sum_x(b^\dagger_{0,x}b_{1,x}+\mathrm{h.c.})-\mu N .
\]

The source implementation has two periodic rail cycles and connector edges
`(site, L+(site+1) mod L)`. Relabeling the lower rail by `x=i-1` preserves its
cycle and sends every shifted connector to an ordinary rung. The source then
assigns matrix element `-1` whenever a hard-core occupation is exchanged across
an edge. Therefore its fixed-`q` operator is exactly the paper's clean ladder at
`t=t_perp=1`. The paper's `-mu N` term is a scalar in a fixed-`q` sector and
does not alter the eigenvectors or within-sector excitation energies.

The paper defines its per-site filling as

\[
 \rho={N\over 2L}.
\]

The repository uses `N=q`, so its `rho=q/(2L)` is the identical convention;
there is no per-rung versus per-site factor mismatch.

**Finding:** `PASS` -- this is a same-model identification, not an analogy.

## 3. Phase domain and mode content

Crepin *et al.* combine bosonization and renormalization-group analysis with
QMC and DMRG. Their abstract, Section V, and Figs. 2 and 20 identify the clean
ladder away from the half-filled rung-Mott line as a one-mode Luttinger liquid.
Interchain hopping locks and gaps the antisymmetric field, while the remaining
gapless mode is the symmetric sector. They report

\[
 {1\over2}\mathrel{\le}K_s(\rho)\mathrel{\le}1.
\]

The equal-coupling point `t_perp=t` is treated directly in their QMC results.
Their Eq. (5.15) and Fig. 19 identify a finite sound velocity with the linear
branch of the excitation spectrum, including `t_perp=t`. The paper separately
notes `z=2` at the zero-density vacuum endpoint and a gap at `rho=1/2`; neither
endpoint lies in the audited interval

\[
 I=[7/48,13/48)=[0.145833\ldots,0.270833\ldots).
\]

Indeed, the closure of `I` is a compact subset of `(0,1/2)`. Thus the precise
external premise needed by the bridge is supported on the whole proposed cell
union:

\[
 \omega_s(k)=v_s(\rho)|k|+o(|k|),\qquad
 0<v_s(\rho)<\infty,
\]

with one gapless symmetric mode and a gapped antisymmetric sector.

**Finding:** `PASS` as an adopted field-theory/QMC/DMRG phase premise.

## 4. Symmetric-density pole and normalization

The paper does not directly tabulate the repository's finite-volume dynamical
structure factor. The residue statement is instead a consequence of the
operator normalization in its Eqs. (3.10), (3.14), and (3.17).

For each leg, the smooth density fluctuation is

\[
 \delta n_a(x)=-{1\over\pi}\partial_x\Phi_a(x).
\]

With `Phi_s=(Phi_0+Phi_1)/sqrt(2)`, the total smooth density is therefore

\[
 \delta n_s(x)=-{\sqrt2\over\pi}\partial_x\Phi_s(x).       \tag{A1}
\]

For the explicit positive-frequency convention

\[
 S_s(k,\omega)={1\over L}\sum_{m>0}
   |\langle m|n_s(k)|0\rangle|^2
   \delta(\omega-E_m+E_0),                                 \tag{A2}
\]

canonical quantization of the paper's Gaussian symmetric action gives

\[
 S_s(k,\omega)={K_s|k|\over\pi}
   \delta(\omega-v_s|k|)+o(|k|).                            \tag{A3}
\]

Consequently, because the repository Fourier operator has no `1/sqrt(L)`
normalization, the unnormalized symmetric-pole weight is

\[
 \sum_{m\in 1s}|\langle m|n_s(k)|0\rangle|^2
   ={LK_s|k|\over\pi}+o(L|k|).                              \tag{A4}
\]

The exact stored probe after the lower-rail relabeling is

\[
 O_L(k)=n_0(k)+e^{ik}n_1(k)
       ={1+e^{ik}\over2}n_s(k)+{1-e^{ik}\over2}n_a(k).      \tag{A5}
\]

At `k_L=2 pi/L`, its symmetric coefficient has squared magnitude
`cos^2(pi/L)`. The symmetric and antisymmetric densities have opposite rail
parity, so the antisymmetric term cannot cancel a symmetric-sector pole.
Equations (A4)--(A5) therefore yield

\[
 W_L(\rho)=2K_s(\rho)\cos^2(\pi/L)+o(1).                   \tag{A6}
\]

The leading term is strictly positive for every audited `L>=4` and tends to
`2K_s>=1`. This proves nonzero thermodynamic scaling-limit visibility of the
linear symmetric mode under the adopted Luttinger premise.

As an independent normalization check, the prediction formed from the frozen
finite-size `K_s` estimator approaches the observed lowest-pole weight:

| L | `2 K_s cos^2(pi/L)` | observed `S R_low` | relative difference |
|---:|---:|---:|---:|
| 4 | `0.723915544736` | `0.713491179693` | `-1.440%` |
| 6 | `1.136560976000` | `1.121209686522` | `-1.351%` |
| 8 | `1.315543248876` | `1.307249817077` | `-0.630%` |
| 10 | `1.406371918828` | `1.400951026296` | `-0.385%` |
| 12 | `1.457711477100` | `1.453859399398` | `-0.264%` |

This convergence is corroboration, not a premise of the derivation.

**Finding:** `PASS` for nonzero asymptotic residue with the exact stored phase
and unnormalized Fourier convention.

## 5. Verdict and exact claim ceiling

The pinned conditional theorem correctly represents the external literature:

```text
same clean t=t_perp=1 ladder
  + rho=N/(2L) and I subset (0,1/2)
  + adopted one-mode symmetric Luttinger phase on I
  + exact nonzero symmetric component of O_L
  => conditional z=1 and nonzero thermodynamic density-pole visibility on I.
```

This audit does **not** convert the premise into a rigorous
repository-internal theorem. Crepin *et al.* establish the phase using field
theory, RG, QMC, and DMRG; they do not supply a mathematical all-`L` proof or
an exact atomwise lower bound on finite-volume pole weight. Equation (A6) is
asymptotic and must not be presented as an exact equality at
`L=4,6,8,10,12`.

Nothing in this audit establishes gravity, continuum spacetime, a metric,
universal stress coupling, or any retroactive change to a frozen Stage6
adjudication. Its verified conclusion is the explicitly conditional physical
`z=1` bridge and no stronger claim.
