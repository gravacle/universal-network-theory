# Independent audit of the A009--A016 z=1 primary proof path

Date: 2026-09-16

Verdict: **PASS**

## 1. Scope

This audit reviewed the z=1 proof packet as an independent, read-only evidence
surface. It checked:

1. whether the primary argument imports a verdict, gate, stop rule, claim label,
   or other logical machinery from an earlier proof surface;
2. whether the finite Hamiltonian and density observable are defined locally and
   match their pinned raw implementation;
3. whether thermodynamic Luttinger-liquid residue is kept distinct from the
   finite-sector numerical observations;
4. whether conditional physical `z=1` is kept logically separate from the
   finite `pbar>0.50` record-mass result;
5. whether the proposed rule joining those two propositions is clearly only a
   proposal requiring deliberate adoption; and
6. whether the finite extractor independently reproduces the stated 13-sector
   observations from directly pinned sources.

This audit did not use L14, alter a prior adjudication, adopt the proposed
composition rule, or make a gravity or alpha claim.

## 2. Audited objects

| object | SHA-256 |
|:---|:---|
| `README.md` | `5dcfef1727573511b76a92036ff1243ba4293591fb1ba575d885f6a25c162017` |
| `CONDITIONAL_Z1_BRIDGE_THEOREM.md` | `6353aafed694f2598fb72384bc44e2c1e5bada50262ded73919896141b2ce645` |
| `STAGE6R4_THEOREM_PATH_SPEC.md` | `182a8ca2c1559df618837105b008a056b124ac9adc6dc7f2606729eda8d9cec4` |
| `EXACT_RESPONSE_SUMRULE_BOUND.md` | `5734cda284e85ae0b51ff60b85664f470a407c95daf91b47835963539398e2f8` |
| `analyze_centerline.py` | `07daf92a84b563fbae1f288528baa71021fe8911953759e91b5f7d68444d2077` |

The raw implementation file cited for the graph, hopping operator, and density
mode was also checked directly:

| provenance object | SHA-256 |
|:---|:---|
| `../DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/compute_phase_screen.py` | `e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7` |

The digest matches the value pinned in all three documents that consume the
observable convention.

## 3. Cross-surface separation

**PASS.** The primary proof path does not consume an earlier adjudication
verdict, closure contract, stop condition, fit gate, adjacent-pair rule,
disposition label, registrar rule, URM rule, gravity criterion, or alpha
argument. Historical source locations are used only as raw data or operator
provenance.

`STAGE6R4_THEOREM_PATH_SPEC.md` is explicitly quarantined as a compatibility
sketch. It says that it is not a z=1 proof input, defines no implementation, and
issues no verdict. Its surviving six items are stated only as physics hypotheses
or source-integrity requirements and are independently restated in the primary
documents.

The exact operator is defined locally as the clean periodic two-leg hard-core-
boson ladder with `t=t_perp=1`. The stored shifted-rung representation is joined
to it by the explicit permutation `x=i-a`; no orbit-reduction or historical
classification is used as a premise.

The observable is also local and unambiguous:

```text
n_a(k) = sum_(x=0)^(L-1) exp(i k x) n_(a,x),
O_L(k_L) = n_0(k_L) + exp(i k_L) n_1(k_L),
k_L = 2 pi/L,
```

with no `1/sqrt(L)` factor. The raw implementation at lines 466--474 of the
pinned source agrees with this unnormalized convention before the exact
lower-rail relabeling.

## 4. Thermodynamic and finite residue boundary

**PASS.** The conditional theorem derives

```text
W_L(rho) = 2 K_s(rho) cos^2(pi/L) + o(1)
```

under the explicitly pinned same-model Luttinger-liquid premise. It states that
this is an asymptotic scaling statement, not an exact equality or lower bound at
`L=4,6,8,10,12`, and assigns no sign to the finite-size correction.

The finite-sector `R_low` and `w_*` observations are reported separately as
numerically certified finite evidence. They are not substituted for the
thermodynamic premise and are not used to assert a uniform all-`L` residue
bound. Conversely, the external Luttinger premise is not used to rewrite the
finite numerical rows as exact finite-volume theorems.

## 5. Separation of z=1 from record mass

**PASS.** The packet proves two distinct implications:

```text
same-model LL premise + exact model/domain/probe identities
  => conditional physical z=1 on I=[7/48,13/48)
     with thermodynamic probe visibility;
```

and, separately,

```text
audited bounded membership of A009--A016
  + authenticated deduplicated pbar arithmetic
  => record-block mass >0.50 at L=4,6,8,10,12.
```

The `0.50` threshold is not presented as the definition or derivation of the
dynamical exponent. The Luttinger result is not presented as a proof of record
membership or record mass.

## 6. Proposed composition rule

**PASS.** `README.md` labels “majority z=1 record block at the sampled sizes” as
a proposed project-level definition. It uses conditional language (`could`,
`if the project deliberately adopts`, and `proposed here for review`) and says
that no earlier surface supplies the logical arrow.

The conditional theorem likewise says that joining the physical and record
propositions requires an explicit native definition and points to the proposal
for deliberate review. Therefore this packet does not silently adopt the rule
and does not currently promote the two separate results into a combined
project-level claim.

## 7. Independent finite-sector replay

The hash-pinned script was executed during the audit. It returned schema
`Z1_NATIVE_FINITE_EVIDENCE_V001` and status
`FINITE_NUMERICAL_EVIDENCE_ONLY__NO_THERMODYNAMIC_VERDICT`. All source-integrity
checks passed. The 40 atom/size assignments reduce to the following 13 unique
sectors:

| L,q | atoms | S | R_low | w_* |
|:---|:---|---:|---:|---:|
| 4,1 | A009--A011 | `0.9999999999999991` | `0.5` | `0.49999999999999956` |
| 4,2 | A012--A016 | `1.6666666666666674` | `0.4280947078156539` | `0.7134911796927568` |
| 6,2 | A009--A012 | `1.4455602199717286` | `0.6685010572113367` | `0.9663585353137529` |
| 6,3 | A013--A016 | `1.7718181838576859` | `0.6328017720650394` | `1.1212096865222034` |
| 8,2 | A009 | `1.3232049426289088` | `0.7849688302643845` | `1.0386746360154664` |
| 8,3 | A010--A013 | `1.5890568290853657` | `0.7491511325423341` | `1.190443723183432` |
| 8,4 | A014--A016 | `1.7838381847509381` | `0.7328298206936398` | `1.3072498170774978` |
| 10,3 | A009--A010 | `1.4619706787690285` | `0.8165714981791816` | `1.1938035874564608` |
| 10,4 | A011--A014 | `1.6405593774662413` | `0.7984096120373475` | `1.309838376087054` |
| 10,5 | A015--A016 | `1.7752583346798239` | `0.7891533299283154` | `1.4009510262955789` |
| 12,4 | A009--A011 | `1.52938656856366` | `0.8417832705849726` | `1.2874120276742462` |
| 12,5 | A012--A015 | `1.6601988638189955` | `0.8311603546876659` | `1.3798914765038564` |
| 12,6 | A016 | `1.7619394740448788` | `0.8251471862764429` | `1.4538593993975275` |

Every selected row has positive `S`, `R_low`, and `w_*`. The minimum observed
`R_low` is `0.4280947078156539`; the minimum observed `w_*` is
`0.49999999999999956`.

For L10/L12, independently implemented Target and Blind rows were checked for
every selected sector and every diagnostic neighbor. The maximum relative
disagreement over all compared fields is `3.067982884076874e-14`. The five
reconstructed record-block masses are:

| L | deduplicated pbar mass |
|---:|---:|
| 4 | `0.7260206189754993` |
| 6 | `0.5846615608350367` |
| 8 | `0.7373965730354166` |
| 10 | `0.6500987927669427` |
| 12 | `0.5695649839332784` |

All five are strictly greater than `0.50`.

## 8. Exact claim boundary and remaining obligations

The audit supports the packet's current claim boundary:

```text
exact finite Hamiltonian/probe identity:       PROVED
A009--A016 bounded record membership:          PROVED; independent audit PASS
A009--A016 pbar mass >0.50 at five sizes:      AUTHENTICATED; dual reconstruction
finite probe visibility in all 13 sectors:     NUMERICALLY CERTIFIED
z=1 on I under same-model LL literature:       CONDITIONAL PHYSICAL THEOREM
unconditional repository-internal all-L z=1:  OPEN
```

The following obligations remain open:

1. a repository-internal proof of the Luttinger-liquid premise for this
   nonintegrable ladder, if an unconditional internal `z=1` theorem is required;
2. a uniform all-`L` record-membership and record-mass continuation theorem;
3. an analytic or interval-certified finite-`L` residue bound, if one is desired
   independently of the thermodynamic premise; and
4. explicit project review and adoption of the proposed native composition
   definition before any combined “majority z=1 record block” claim is made.

No gravity, alpha, all-`L` record-continuation, or unconditional internal
Luttinger-phase claim is earned by this packet.

