# Final hostile audit of the z=1 surface boundary

Date: 2026-09-16

Verdict: `PASS`

## 1. Question audited

This audit asks whether the current z=1 packet imports logical machinery that
was created for a different proof surface. In particular, it checks whether
any earlier gate, adjudicator, fit rule, disposition, numerical active-pole
convention, URM rule, gravity criterion, or alpha argument is a premise of:

1. the conditional physical z=1 theorem; or
2. the repository-internal exact z=1 route.

Raw source and numerical files may be used as provenance only when the object
needed by the argument is defined locally and the imported workflow logic is
not treated as a theorem premise.

This was a read-only hostile review of the packet before this audit note was
added. No other file was modified.

## 2. Audited objects and current hashes

| object | SHA-256 |
|:---|:---|
| `README.md` | `f7b0d99b644e402c58b2d522b4c47f78e3584048591cd2aa4e01a8e5db00c33d` |
| `CONDITIONAL_Z1_BRIDGE_THEOREM.md` | `6353aafed694f2598fb72384bc44e2c1e5bada50262ded73919896141b2ce645` |
| `INTERNAL_Z1_THEOREM_ROUTE.md` | `e85af161082335559a9cc29c4b06090e13f2e403ca69932500bcfd1658b68b2b` |
| `analyze_centerline.py` | `07daf92a84b563fbae1f288528baa71021fe8911953759e91b5f7d68444d2077` |
| `AUDIT_Z1_PRIMARY_PROOF_PATH_2026-09-16.md` | `2f556b2bacba57955b436674d3c1050fa78891ba5a1da69bebf277ce3e45fe4d` |
| `AUDIT_LL_PREMISE_2026-09-16.md` | `88a4f4f848cfc626b899ee83a2d23aaf1665cdac67d108f755f83e2b51b5c278` |
| `AUDIT_INTERNAL_Z1_THEOREM_ROUTE_2026-09-16.md` | `c6554327b694c33518614d7c725addde664ae74f21638b13bd9c73cb1072a567` |
| `EXACT_RESPONSE_SUMRULE_BOUND.md` | `5734cda284e85ae0b51ff60b85664f470a407c95daf91b47835963539398e2f8` |
| `AUDIT_EXACT_RESPONSE_SUMRULE_BOUND.md` | `0b0967ce7c01045c333497969a4931e599717dc385e590951b279f77a0eda4b1` |
| `STAGE6R4_THEOREM_PATH_SPEC.md` | `182a8ca2c1559df618837105b008a056b124ac9adc6dc7f2606729eda8d9cec4` |
| raw `compute_phase_screen.py` provenance | `e9a44977cdea8a2dbb5e6095a7b13b9fe44c156d5ae01b4d5e6bb516dda3a5b7` |

The hashes were recomputed during this audit.

## 3. Conditional theorem boundary

The conditional theorem has the following logical form:

```text
exact locally defined H
  + exact locally defined O_L
  + exact density interval I
  + explicit same-model external premise LL-P
  => conditional physical z=1 on I with thermodynamic probe visibility.
```

The Hamiltonian, density convention, Fourier normalization, observable, rail
relabeling, and interval are stated directly in the packet. The historical
source file is used only to verify the raw edge list, hopping matrix element,
and Fourier-density implementation. No verdict, threshold, fit, or
classification from that source enters the implication.

The finite `pbar>0.50` record-block result is separate and is not a premise of
z=1. The proposed rule joining the record result to the z=1 result is plainly
labeled as a proposal requiring deliberate project adoption. No older surface
supplies that logical arrow.

**Finding:** `PASS`. No earlier workflow machinery is a premise of the
conditional theorem.

## 4. Repository-internal route boundary

The internal route uses only the locally defined Hamiltonian and probe,
translation and rail-exchange symmetry, and direct finite-dimensional
arguments:

- Perron--Frobenius positivity and uniqueness;
- an exact double-commutator first-moment identity;
- elementary token-graph degree bounds;
- a locally derived LSM variational state; and
- positive spectral-measure inequalities.

The route proves exact finite-volume visibility, an all-band first moment of
order `1/L`, and the existence of an `O(1/L)` LSM excitation. It correctly
leaves the uniform probe-visible all-`L` z=1 theorem open.

Its optional discussion of an exact first-support pole group expressly
requires a new residual-independent definition. It does not promote the
historical adaptive numerical floor into an exact observable and does not use
that convention to prove any result.

**Finding:** `PASS`. No earlier workflow machinery is a premise of the exact
internal route.

## 5. Inherited numerical fields are quarantined corroboration

The read-only extractor consumes historical finite-calculation fields named:

```text
Delta_act
R_low
chi_tau
threshold_stable
active_pole_residual_max
```

It also forms a five-size power fit from `Delta_act`. Those quantities retain
the finite calculation's inherited numerical active-pole convention. They are
not silently redefined as an exact all-`L` pole or projector.

This does not create logical leakage because the packet quarantines them as
auxiliary finite-system corroboration:

- the extractor reports status
  `FINITE_NUMERICAL_EVIDENCE_ONLY__NO_THERMODYNAMIC_VERDICT`;
- the README states that the active-pole convention is not the mathematical
  definition of an all-`L` pole;
- the conditional theorem does not use any finite row or finite-size fit as a
  premise; and
- the internal exact route does not use these numerical fields to prove its
  exact statements or close its open theorem.

The extractor compiled and replayed successfully during this audit. Its source
integrity checks passed, all selected finite rows were positive, and all five
reconstructed record-block masses exceeded `0.50`. Those outcomes remain
numerical corroboration only.

**Finding:** the inherited fields are data provenance, not theorem premises.
They are visibly quarantined and do not contaminate either proof path.

## 6. Audit-custody note

`AUDIT_Z1_PRIMARY_PROOF_PATH_2026-09-16.md` pins the earlier README hash
`5dcfef1727573511b76a92036ff1243ba4293591fb1ba575d885f6a25c162017`,
whereas the clarified README audited here has hash
`f7b0d99b644e402c58b2d522b4c47f78e3584048591cd2aa4e01a8e5db00c33d`.
That is audit-document staleness, not logical leakage. This final audit
directly reviewed and pins the clarified README.

## 7. Final disposition

```text
conditional z=1 theorem surface:             PASS
repository-internal exact route surface:     PASS
historical gate/adjudicator premises:        NONE
historical fit as theorem premise:           NONE
historical active-pole rule as theorem:      NONE
inherited finite numerical fields:           QUARANTINED AUXILIARY EVIDENCE
unconditional internal all-L z=1 theorem:    OPEN
```

The packet satisfies the stated surface restriction. Its conditional theorem
and exact internal partial results stand on native definitions and explicitly
identified premises. The remaining all-`L` theorem is left open rather than
filled with machinery from another surface.
