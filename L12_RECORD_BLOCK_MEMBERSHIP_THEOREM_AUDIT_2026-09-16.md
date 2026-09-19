# L12 record-block membership theorem audit

Date: 2026-09-16

Status: `SUPERSEDED_IN_PART__REALIZED_LINEAGE_REFUTED__ALLOW_NON_DARK_THEOREM_PROVED`

> **2026-09-16 correction.** Sections 3 and 7 correctly reject the claim that
> positive aggregate flows prove one *already completed* common lineage. They
> are too broad where they appear to reject every possible whole-q5 membership
> theorem. Including the complete frozen family of admission operators yields
> an exact no-dark result: every q5 basis component has at least two nonzero
> admissible q6 actions and every realized q5 component has actual q4 ancestry.
> The corrected theorem, its proof, and its strict nonclaims are recorded in
> [`L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md`](L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md).
> That corrected theorem closes structural q5 membership and the
> `0.56956498393327842` mass arithmetic. The adopted `ARGER-GATE-1` now uses
> those results together with independently authenticated finite probe
> visibility; the legacy atomwise route described later in this audit is not
> part of the governing argument.

> **Historical-method note.** Sections 1, 6, and 7 below document the question
> originally posed by a now-retired Stage-6 route. Their gate-replacement
> framing is retained as project history only. It creates no current proof
> obligation and has no authority over `ARGER-GATE-1`.

## 1. Question audited

Stage-6R3 identifies a theorem path requiring an independently audited
record-block membership theorem that both:

1. justifies whole-sector `pbar` aggregation from typed sector flow; and
2. replaces or implies the original endpoint/full-conjunction rule.

See
[`stage6r3_supplemental_adjudicator.py`](DEVELOPMENT_R_L12_STAGE6R3_RECORD_FLOW_ADJUDICATION_V001/stage6r3_supplemental_adjudicator.py#L454-L461).

The candidate inference is:

```text
positive q4 -> q5 flow
+ positive q5 -> q6 flow
+ q4/q5/q6 sector membership
=> all q4+q5+q6 pbar mass belongs to one admissible record block
=> 0.56956498393327842 > 0.50.
```

The arithmetic conclusion is correct if the membership and gate-replacement
premises are proved. This audit asks whether those premises follow from the
frozen L12 definitions and authenticated evidence.

## 2. Frozen facts

The authenticated sector means are:

```text
q4 = 0.23878787617682787
q5 = 0.20303604727842960
q6 = 0.12774106047802095
sum = 0.56956498393327842
```

The record-flow sidecar independently authenticates positive aggregate
`q4 -> q5` and `q5 -> q6` terminal flows. See
[`RECORD_FLOW_BRIDGE_REPORT_V001.json`](DEVELOPMENT_R_L12_RECORD_FLOW_BRIDGE_V001/RECORD_FLOW_BRIDGE_REPORT_V001.json#L477-L485)
and its
[`certified_sector_flow_edges`](DEVELOPMENT_R_L12_RECORD_FLOW_BRIDGE_V001/RECORD_FLOW_BRIDGE_REPORT_V001.json#L538-L562).

The exact Target q5 event-window mean is resolved by canonical lineage into:

```text
strict in-window fifth and sixth acceptance       0.11570852222694002
pre-window fifth, in-window sixth acceptance      0.0042711400583841505
no sixth acceptance by event 12                   0.08305638499310529
observed q5 pbar                                  0.20303604727842960
```

The displayed terms reproduce the observed mean within the report's maximum
decomposition residual of `5.83e-16`. Target and Hostile strict support differ
by only `3.47e-16`. See
[`LINEAGE_RESOLVED_SUPPORT_REPORT_V001.json`](DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/LINEAGE_RESOLVED_SUPPORT_REPORT_V001.json#L1753-L1805)
and its
[`threshold_adjudication`](DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/LINEAGE_RESOLVED_SUPPORT_REPORT_V001.json#L1826-L1836).

Thus the q5 mean consists of approximately:

```text
strict common lineage                 56.9892%
pre-window entry/common exit           2.1036%
right-censored at event 12             40.9072%
```

"Right-censored" is not a failed history. It means only that a sixth
acceptance has not occurred within the declared L12 horizon.

## 3. The whole-sector inference does not follow

The exact prefix-lineage representation keeps each lineage mask as a distinct
row. Transport changes only the carrier configuration, never the lineage mask;
admission creates distinct stay and accepted child rows; and observables add
over orthogonal rows rather than merging them. See
[`THEOREM.md`](DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/THEOREM.md#L8-L69).

A minimal countermodel therefore exists inside the declared direct-sum
structure. Write the q5 space as

```text
H5 = H_in direct-sum H_out direct-sum H_dark.
```

Let q4 feed `H_in`, let a different orthogonal subspace `H_out` feed q6, and
place arbitrary q5 probability in `H_dark`. Both aggregate sector-flow edges
are positive while their common-lineage intersection is zero. Even if
`H_in = H_out`, the mass in `H_dark` remains unconstrained.

The authenticated L12 decomposition is a concrete witness against the still
stronger statement that every q5 history has already realized both boundaries:
`0.08305638499310529` of q5 `pbar` is explicitly classified as having no sixth
acceptance by event 12. The category is defined by the fifth and sixth
acceptance events in
[`l12_lineage_resolved_support.py`](DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/l12_lineage_resolved_support.py#L348-L370),
and the three categories are checked against the observed q5 ledger in the
same program.

Therefore:

- positive typed sector connectivity does not prove common-lineage
  intersection;
- a common-lineage intersection, if present, would not prove membership of the
  entire q5 sector; and
- canonical lineage orthogonality supports exact accounting but does not turn
  distinct histories into one lineage.

The proposed whole-sector record-block membership theorem is consequently not
derivable under the current definitions. Calling all q5 mass admissible would
be a new aggregation rule, not a theorem extracted from the frozen evidence.

## 4. Strongest valid conditional continuation lemma

Define:

```text
S = 0.11570852222694002  strict common-lineage pbar support
R = 0.13347106334515118  q5 support required with the q4+q6 endpoints
N = 0.08305638499310529  no-exit-by-event-12 q5 pbar mass
delta = R - S = 0.01776254111821116
```

The following implication is valid:

> If an exact continuation on the same history probability space preserves the
> pre-event lineage weights and authenticates a subset of the right-censored
> q5 histories with existing `pbar` residence mass at least `delta`, and every
> history in that subset subsequently undergoes its sixth acceptance, then the
> extended common-lineage support reaches `R`.

This requires eventual-exit certification for `21.3861%` of `N`. If the
pre-window-entry/common-exit category is first admitted by an explicit rule,
the remaining gap becomes `0.0134914010598270095`, or `16.2437%` of `N`.

For one proposed fresh admission at `phi = pi/4`, the accepted mass is one half
of the lineage-weighted norm on carrier columns blank at the selected target.
Closing the strict shortfall in that one step would therefore require an
authenticated eligible blank-projector norm of at least:

```text
2 * delta = 0.03552508223642232.
```

If every right-censored component were eligible and blank, the algebraic
diagnostic would be:

```text
S + N/2 = 0.157236714723492665
q4 + q6 + S + N/2 = 0.523765651378341485.
```

Those numbers are favorable, but the blank-target premise is not supplied by
the L12 lineage label. Admission acts only on blank carrier columns; occupied
target states are exact kernel states. See
[`Q_SHARDED_TARGET_METHOD_V004.md`](DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/Q_SHARDED_TARGET_METHOD_V004.md#L24-L29)
and the exact row split in
[`l12_lineage_resolved_support.py`](DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/l12_lineage_resolved_support.py#L325-L345).

An appended tensor-product blank target would make the half split true by
construction. That would be a new prepared extension, not a consequence of the
existing L12 boundary.

## 5. Why this is not an L13 or L14 result

The frozen L12 parent stops after exactly `L` transitions, before a loaded cell
can be revisited. Changing `L` changes the periodic prism, the carrier census,
the Hilbert space, and the transport Hamiltonian from the start. The present
artifacts contain no exact L12-to-L13 or L12-to-L14 state embedding that
preserves both dynamics and the declared `pbar` measure. See
[`PROTOCOL.md`](DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md#L19-L47).

The L12 storage method also streams the terminal children without creating a
post-event `H_L` array; it retains the preterminal `H_(L-1)` shards. See
[`Q_SHARDED_TARGET_METHOD_V004.md`](DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/Q_SHARDED_TARGET_METHOD_V004.md#L37-L41).

Finally, the reporting window itself depends on `L`:

```text
H_L = {n : ceil(L/2) <= n <= L}.
```

L12 uses events 6--12. A different size has a different history and reporting
window. Consequently `S + N/2` is neither an L13 nor an L14 `pbar` result. At
most, under the explicit new blank-extension premise, it is a
future-conditioned L12 boundary diagnostic.

## 6. Historical Stage-6 question (superseded)

The frozen Stage-6 protocol first requires every atom to pass the complete
spectral and numerical conjunction. Only then are adjacent passing atoms
grouped and tested for mass at least `0.50`. See
[`PROTOCOL.md`](DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/PROTOCOL.md#L173-L201).

At L12:

- endpoint A011 fails exponent agreement and both tail-stability predicates;
- endpoint A016 fails both fixed-z1 model-selection predicates; and
- no q5 atom passes the original full conjunction.

These are spectral/model-selection failures, not mass failures. They are
recorded in
[`STAGE6R3_SUPPLEMENTAL_ADJUDICATION_V001.json`](DEVELOPMENT_R_L12_STAGE6R3_RECORD_FLOW_ADJUDICATION_V001/STAGE6R3_SUPPLEMENTAL_ADJUDICATION_V001.json#L32-L42)
and its
[`stage7_gate`](DEVELOPMENT_R_L12_STAGE6R3_RECORD_FLOW_ADJUDICATION_V001/STAGE6R3_SUPPLEMENTAL_ADJUDICATION_V001.json#L257-L268).

That was the conclusion under the retired atomwise classifier. It is not the
current Gate. The exact bounded-membership theorem, majority mass, and
independently authenticated positive finite visibility are now evaluated by
`ARGER-GATE-1` as one complete finite domain.

## 7. Historical verdict and current disposition

### Verdict

1. **Refuted as phrased:** the entire q5 sector does not constitute one already
   realized common q4-to-q6 lineage under the declared lineage definition.
2. **Not derivable from typed flow:** positive aggregate q4-to-q5 and q5-to-q6
   edges do not imply whole-sector record-block membership.
3. **Conditionally valid:** enough right-censored mass exists to close the
   numerical shortfall if an exact continuation theorem certifies the required
   subset on a commensurable measure.
4. **Historically open under the retired route:** a physical continuation or
   embedding theorem and fixed-target blank-norm lower bound. Neither is a
   prerequisite for the adopted bounded-block Gate.

### Superseded consequence for the former L14 scout

At the time of this audit, the L14 calculation remained the active route for
the retired classifier. That operational statement is superseded by the
terminal L14 disposition and adoption of `ARGER-GATE-1`; it is not current advice.

### Research target exposed by the audit

The useful theorem target is narrower and sharper than whole-sector
identification:

> Prove, on a single authenticated probability measure and without changing
> the parent dynamics, a lower bound of at least
> `0.01776254111821116` on right-censored L12 q5 residence mass that must later
> undergo a sixth acceptance.

This remains an optional stronger completed-lineage research target. It is not
a missing premise of the adopted finite block `z=1` result.

## 8. Preservation statement

This audit is a read-only interpretation of existing authenticated artifacts.
It does not mutate the lineage-resolved report or any L12 cache.
