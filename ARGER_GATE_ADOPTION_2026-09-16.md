# Adoption of the UNT finite ARGER Gate

Date: 2026-09-16

Status: `ADOPTED__GOVERNING_FINITE_ARGER_GATE`

## 1. Decision

The project adopts **ARGER Gate 1 (`ARGER-GATE-1`)** as the governing finite
Gate for the `A009--A016` record envelope. ARGER is the record-formation
process

```text
ALLOW -> REQUIRE -> GATE -> EM -> RECORD.
```

`ARGER-GATE-1` names the versioned criterion applied at its GATE stage. It is
not a second process, a bridge mechanism, or a redefinition of ARGER.

For this versioned Gate, an authenticated finite envelope passes exactly when:

1. every selected sector has **exact bounded record membership** under the
   declared record-formation law;
2. the envelope's **deduplicated authenticated probability mass is greater
   than `0.50`**; and
3. every unique selected sector has **strictly positive authenticated finite
   probe visibility**.

A passing envelope realizes the UNT **finite GFT `z=1` standard**. This is a
project-native finite Gate and a declared physical classification rule. Its
claim boundary is fixed by this adoption record.

The constituent sector rows authenticate membership and visibility, while the
Gate evaluates the complete deduplicated finite domain and its global mass.
No conjunction of independent sector verdicts replaces that collective
evaluation.

The exact membership theorem uses *record block* as a mathematical label for
that bounded graded domain. The label does not add a block mechanism or stage
to ARGER. Earlier evidence packets that predate this adoption remain historical
evidence; this record does not alter their sealed calculations, hashes, audits,
or stated proof boundaries.

## 2. Applied evidence

The exact membership theorem is
[`L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md`](L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md),
with independent passing audit
[`AUDIT_L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md`](AUDIT_L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md).
It proves bounded record roles at every authenticated size

```text
L in {4,6,8,10,12}.
```

After repeated atom assignments are deduplicated, the authenticated masses
are:

| L | selected sectors | deduplicated mass |
|---:|:---|---:|
| 4 | `q1--q2` | `0.7260206189754993` |
| 6 | `q2--q3` | `0.5846615608350367` |
| 8 | `q2--q4` | `0.7373965730354166` |
| 10 | `q3--q5` | `0.6500987927669427` |
| 12 | `q4--q6` | `0.56956498393327842` |

Every mass is strictly greater than `0.50`.

The shared L08/L10/L12 finite-domain values decrease
`0.7373965730354166 -> 0.6500987927669427 -> 0.56956498393327842` while
remaining above one half. ARGER-GATE-1 therefore establishes the adopted phase
classification at every authenticated size; these data do not identify a
first below-to-above threshold crossing at L12. The separately reported
strict common-lineage diagnostic measures a narrower object and rises over
the same sizes.

The 40 atom/size assignments reduce to these 13 unique sector rows:

```text
(L4,q1),  (L4,q2),
(L6,q2),  (L6,q3),
(L8,q2),  (L8,q3),  (L8,q4),
(L10,q3), (L10,q4), (L10,q5),
(L12,q4), (L12,q5), (L12,q6).
```

Every row has strictly positive authenticated finite probe visibility. The
global minimum over all 13 rows is

```text
R_low = 0.4280947078156539 > 0.
```

The native reconstruction and checks are recorded in
[`DEVELOPMENT_R_ARGER_GATE_V001`](DEVELOPMENT_R_ARGER_GATE_V001/README.md).
Accordingly, every premise of ARGER-GATE-1 is met, and the authenticated
`A009--A016` envelope passes the finite ARGER Gate at L4, L6, L8, L10, and
L12. The finite GFT `z=1` verdict is therefore adopted and established on this
bounded evidence surface.

## 3. Separate dynamical-exponent typing

The finite GFT `z=1` verdict and the dynamical-exponent theorem remain
separately typed:

- The adopted ARGER-GATE-1 verdict follows from exact bounded membership,
  majority mass, and finite visibility across all 13 authenticated sectors.
- The separately documented
  [`conditional same-model theorem`](DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/CONDITIONAL_Z1_BRIDGE_THEOREM.md)
  supports physical dynamical exponent `z=1` on the declared density interval
  under the pinned LL-P premise.
- A premise-free, repository-internal uniform all-`L` response theorem remains
  a stronger open result, as documented in
  [`INTERNAL_Z1_THEOREM_ROUTE.md`](DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/INTERNAL_Z1_THEOREM_ROUTE.md).
  It is not a condition of the adopted finite block Gate.

The conditional LL-P theorem supports the physical interpretation of the
finite Gate classification without being imported as a Gate premise. The
open all-`L` theorem neither blocks nor weakens the finite verdict actually
adopted here.

## 4. Explicit nonconsequences

This adoption does not establish:

- a premise-free uniform all-`L` dynamical theorem;
- uniform all-`L` continuation of record membership or majority mass;
- a parameter-free numerical derivation of `G`;
- a numerical derivation or selection of alpha; or
- an identification of the exact L12 majority margin
  `0.06956498393327842` with an alpha-regulated write cost, binding energy,
  mass defect, or spectral residue.

The alpha interpretations and the possible physical meaning of the majority
margin remain hypotheses for separately typed investigation.
