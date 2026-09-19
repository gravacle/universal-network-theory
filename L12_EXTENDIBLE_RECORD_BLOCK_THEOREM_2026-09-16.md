# L12 extendible record-block theorem

Date: 2026-09-16

Status: `STRUCTURAL_THEOREM_PROVED__BOUNDED_RECORD_BLOCK`

## 1. Scope

This note proves an exact statement about the frozen L12 admission operators.
It distinguishes two notions that must not be conflated:

1. **completed lineage:** a sixth acceptance actually occurred during the
   declared one-pass L12 history; and
2. **extendible record membership:** a realized component has actual lower-rank
   ancestry and is non-dark to the family of admissible upper-rank actions.

The first notion applies only to the authenticated strict common-lineage mass.
The theorem below applies to the second notion.

## 2. Frozen basis and admission maps

Let

```text
A = {0,...,11}
Omega = {0,...,23}.
```

The fixed-content basis in sector `q` is labelled by pairs `(S,C)` with

```text
S subset A,
C subset Omega,
|S| = |C| = q.
```

Here `S` is the spent-cell lineage record and `C` is the carrier occupation.
This is the exact basis of
[`THEOREM.md`](DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/THEOREM.md#L3-L6).

For each active site `e in A`, define the accepted insertion map

```text
F_e |S,C> = |S union {e}, C union {e}>   if e not in S union C,
              0                          otherwise.
```

The frozen admission coefficient at `phi = pi/4` is
`-i sin(phi) = -i/sqrt(2)`, so every nonzero `F_e` image is a nonzero
admission channel. The insertion rule is the one used by PLB-1 and the exact
q-sharded implementation; see
[`THEOREM.md`](DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/THEOREM.md#L18-L23)
and
[`Q_SHARDED_TARGET_METHOD_V004.md`](DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/Q_SHARDED_TARGET_METHOD_V004.md#L24-L29).

For fixed `e`, insertion is injective on its domain. Therefore

```text
F_e^dagger F_e = P_e,
```

where `P_e` is the diagonal projector onto basis states for which `e` is both
unspent and carrier-blank.

## 3. Eligibility bound

For a basis vector in sector `q`, its eligible active sites are

```text
E(S,C) = A minus (S union C).
```

Since `|S|=q` and `|C intersect A| <= q`,

```text
|E(S,C)|
  = 12 - |S union (C intersect A)|
 >= 12 - |S| - |C intersect A|
 >= 12 - 2q.
```

Equivalently, as an operator inequality on the q-sector,

```text
sum_(e in A) F_e^dagger F_e >= (12 - 2q) I_q.
```

At L12 this gives

```text
q4: sum_e F_e^dagger F_e >= 4 I_q4,
q5: sum_e F_e^dagger F_e >= 2 I_q5.
```

The q5 result immediately implies

```text
intersection_(e in A) kernel(F_e) = {0}.
```

Thus there is no q5 vector, and no q5 probability-support subspace, that is
dark to every q5-to-q6 admission channel.

## 4. Actual ancestry

The initial lineage is empty. Transport changes `C` but cannot change `S`.
Admission is the only operation that adds a lineage bit, and it adds exactly
one. These facts are proved in PLB-1. Consequently every nonzero realized q5
lineage was produced through five accepted admissions and has an actual q4
ancestor. Every realized q6 lineage similarly has actual q5 and q4 ancestors.

This ancestry statement concerns the executed history. The forward
non-darkness statement concerns the family of frozen admissible actions.

## 5. Exhaustive representation check

An exhaustive census of the canonical masks gives:

```text
q4 basis pairs:  5,259,870; minimum eligible active sites: 4
q5 basis pairs: 33,663,168; minimum eligible active sites: 2
```

The q5 eligibility histogram is

```text
eligible sites  count
2                  16,632
3                 471,240
4               3,769,920
5              11,309,760
6              13,194,720
7               4,900,896
```

The lower bounds are tight. Read-only checks of the Target cache and the
independent Hostile representation confirm that the stored carrier maps
implement the same injective bit insertion. The combinatorial theorem itself
does not depend on floating-point output.

## 6. Exact mass consequence under extendible membership

Define the three rank-resolved roles in the bounded record block by

```text
q4 lower endpoint: realized q4 ancestry + non-dark q4-to-q5 continuation,
q5 bridge:         actual q4 ancestry + non-dark q5-to-q6 continuation,
q6 upper endpoint: actual q4-to-q5-to-q6 ancestry.
```

The endpoint definition intentionally does not require a q6-to-q7
continuation: q6 is the completed upper endpoint of this bounded block.  The
q4 and q5 inequalities above prove the two continuation clauses, while the
executed-history argument proves the ancestry clauses.  Thus every probability
component in the three selected sectors has its corresponding role in an
extendible q4-to-q6 record block. The exact deduplicated sector mass is

```text
q4 = 0.23878787617682787
q5 = 0.20303604727842960
q6 = 0.12774106047802095
sum = 0.56956498393327842 > 0.50.
```

The arithmetic is independently recorded in
[`RECORD_FLOW_BRIDGE_REPORT_V001.json`](DEVELOPMENT_R_L12_RECORD_FLOW_BRIDGE_V001/RECORD_FLOW_BRIDGE_REPORT_V001.json#L477-L485).
Lineage-diagonal observables add over the orthogonal rows rather than creating
interference terms, by PLB-4 in
[`THEOREM.md`](DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/THEOREM.md#L57-L69).

## 7. Nonclaims and proof boundary

This theorem does **not** claim that every q5 history executed a sixth
acceptance during the one-pass L12 chronology. A site absent from `S` may be a
past rejected site, not an unvisited future site. The strict completed-lineage
mass therefore remains `0.11570852222694002`.

It also does not use unrestricted action-graph connectivity as the membership
criterion. The full potential graph may connect many or all grades; aggregating
that maximal component would risk making the `0.50` test vacuous. The selected
central density band, actual ancestry, and rank-specific non-darkness are
essential parts of the candidate predicate.

The present result closes the **structural membership and mass arithmetic**
for the bounded L12 record block. It does not itself calculate finite probe
visibility or a thermodynamic dynamical exponent. The former is independently
authenticated and combined with this theorem by the adopted
[`ARGER-GATE-1`](ARGER_GATE_ADOPTION_2026-09-16.md); the latter is a
separately typed conditional same-model result.

## 8. Preservation statement

This theorem is a read-only deduction from the frozen basis, admission law,
and authenticated sector masses. It does not mutate the L12 evidence.
