# Allow/require scope repair: provenance and dependency disposition

## 1. Scope, baseline, and authority

This document records the read-through and dependency dispositions that were
prepared before integration.  The completed target packet applies bounded
changes to live canonical rows and continuation documents, while this
provenance document itself does not alter sealed historical statements,
numerical results, or Gate R-C artifacts.

The repository baseline inspected here is detached commit
`b0e1d5258621f8dda0a9ff29f5869fc1a5a33511` (`2026-09-06`, `Seal
hostile-audited L8 criticality seed null`).  Before this packet was created the
only short-status entry was the untracked
`DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/` draft.  That draft has no
commit provenance and is not treated as an audited result.

The disposition vocabulary is restricted to:

- **PRESERVE** -- the statement survives with its present evidentiary scope;
- **NARROW** -- a valid kernel survives after an explicit domain restriction;
- **REOPEN** -- a target previously excluded or reclassified becomes a
  legitimate conditional question;
- **SUPERSEDE** -- the statement must cease to govern, while remaining intact
  as historical text;
- **HISTORICAL-ONLY** -- retain for chronology or custody, but do not use as a
  live warrant.

These dispositions are now part of the integrated target.  They become
governing only if the independent frozen mechanical and semantic hostile
audits pass; until then the working-tree integration is unpromoted.

## 2. Controlling semantic distinction exposed by the history

The repository contains three different notions that were temporarily
collapsed:

1. `ALLOW_P(x)` is membership of `x` in the admissible set belonging to a
   specified parent `P`.
2. `REQUIRE_D(phi)` is a universal or singleton statement within a declared
   domain `D`; it is a logical quantifier, not a causal production mechanism.
3. `SELECT_P(x)` is a separate law, if one exists, explaining why one allowed
   parent setting or state became actual.

For a **frozen parent** `P`, internal dynamics changes occupancy inside its
fixed admissible state space and does not redefine that space.  For an enlarged
parent with a dynamical carrier label, schematically

```text
H_tilde = direct_sum_c H_c,
```

global dynamics may change `c`; the subsystem then sees a different effective
admissible fiber.  This is still occupancy in the enlarged parent and can be an
effective permission change for the subsystem.  It is not forbidden by the
fixed-parent result.

This distinction is already present internally in the sealed alpha
`ALLOW/REQUIRE/SELECT` ladder.  It is therefore a reconciliation of repository
semantics, not an imported replacement doctrine.

## 3. Chronological provenance map

| Date | Commit provenance | Exact source | What entered the record | Disposition in this repair |
|---|---|---|---|---|
| 2026-08-17 | `31e4fa661c2f6e11c147e97367dfab82ff3ccfbd`, `W-22: both inherited binaries are two-point samples, and what they exclude is a value getting its start` | `REGISTER_V001.md:1958-1985`, especially `1965-1972` | The earliest explicit analysis says allow/require is modal, omits `forbid`, and cannot represent origination, which is generative rather than modal. | **PRESERVE** as the provenance of the independent `SELECT`/origination axis; **HISTORICAL-ONLY** as a complete current type system because it does not yet distinguish domains or occupancy. |
| 2026-08-18 13:24 | `c75a582f805fe0eb349fe07431d0b33cd95848f9`, `X2: chi is a parameter not an observable -- and under allow/require that is not a defect` | `REGISTER_V001.md:4829-4874`; fixed-complex result at `4833-4841`, record/macroscopic split at `4851-4874` | On a fixed complex, `chi` is construction data rather than an operator.  The accompanying interpretation called allow the record-level face and require the macroscopic face. | **PRESERVE** the fixed-complex theorem; **HISTORICAL-ONLY** the record-level/macroscopic two-level interpretation, which was immediately replaced. |
| 2026-08-18 13:27 | `5c01e473a9933ec2fb0bcba230835ef941566e15`, `X2 erratum: allow is potential at every level -- there is no allow-to-require transition` | `REGISTER_V001.md:4878-4912`, especially `4886-4894` | The erratum asserted that require does not exist at any level because Einstein's equations are constraints on admissible data. | **SUPERSEDE.** Constraint equations do not exhaust gravitational dynamics, and `REQUIRE` is used coherently elsewhere as a conditional universal.  Preserve the historical text and its warning against importing record-level backreaction. |
| 2026-08-18 13:41; classified 2026-08-20 | introduced by `59f233aaf9acbe37fd4a68c6456420302a3be554` (`ledger: purge the name from live rows G-3, G-4`); current classification last touched by `f3462c46a6fdf2cd6929d2cc6508c5e046124319` | `ledger/status_ledger.tsv:16`; mirror `STATUS_LEDGER_V001.md:205`; historical basis `REGISTER_V001.md:4878-4912` | `G-3` made the X2 erratum into live doctrine: Gamma is allow at every level and there is no allow-to-require transition. | **SUPERSEDE** the all-level/no-require clause.  **PRESERVE** only the fixed-record-parent capacity reading of Gamma. |
| 2026-08-18 14:00 | `ab97b2d5881c0cddb97dc9875894990188900d60`, `G-4, G-8, G-9: the record-level constraint measured in its own terms` | `REGISTER_V001.md:5045-5075`; `ledger/status_ledger.tsv:39`; mirror `STATUS_LEDGER_V001.md:206` | `G-4` measured the fixed carrier's Gauss constraint algebra as elementary abelian `Z2^(N_V-1)`, exponent two, with exact zero structure coefficients. | **PRESERVE** exactly for the tested record carrier/family.  It is neither a general permission algebra nor a Poincare/Virasoro algebra and gains no anomaly interpretation from this repair. |
| 2026-08-18 14:18-14:19 | RFP introduced by `b8f83e3c3d4747feff4e8705eea795f1b141564b`; D-4 correction by `e7595733762d71993af7dce9a78a5d636d5ae81d`, `D-4: allow/require is a type discipline; F-2 and F-3 were the same error one level down` | `REGISTER_V001.md:5220-5257`; `RECORD_FORMATION_V001.md:17-33`; `ledger/status_ledger.tsv:53-59`; mirrors `STATUS_LEDGER_V001.md:309-314` and `STATUS_LEDGER_V001.md:65` | D-4 generalized the valid fixed-carrier distinction into “dynamics produces occupancies, never permissions,” withdrew F-2 as written, reclassified F-3, and retained the corrected occupancy question as F-7. | **NARROW** D-4 to a frozen parent/fixed fiber.  **PRESERVE** the fixed-carrier F-2-to-F-7 correction and F-7.  **REOPEN** F-3 conditionally for an enlarged parent carrying dynamical carrier variables. |
| 2026-08-19 | `3c86130f4a862fa4a1ddfe41d6393bd0dc40f184`, `H-1 reframed: emergence from records, not identity at the record level`; H-1 live wording subsequently introduced by `f9ba791ac96beb01e9eb0b74e5411faa55b8c735` | `REGISTER_V001.md:6738-6774`; `ledger/status_ledger.tsv:126,132-133`; mirrors `STATUS_LEDGER_V001.md:25,31-32` | H-1 separated record-level identity from collective emergence, explicitly said emergence is not barred by D-4, and recognized that X-2 had been overextended.  H-7 linked carrier origin to emergence; H-8 recorded the foreclosure concern. | **PRESERVE** H-1; **REOPEN** H-7 as an enlarged-parent formation question; **SUPERSEDE** H-8 as a still-open foreclosure claim because T-21 already resolved its concern, while retaining it historically. |
| 2026-08-20 | `04819fea988340a48ddfb1c0a74e3792f8eec045`, `T-35 repairs ...; T-21 done` | `REGISTER_V001.md:9602-9608`; canonical X-2/T-21 wording `ledger/status_ledger.tsv:24`; mirror `STATUS_LEDGER_V001.md:291` | T-21 scoped X-2 to the record level and explicitly left the collective emergence question open under C-77/T-42. | **PRESERVE.** This is the first live scoping repair and already blocks use of X-2 as an emergence no-go. |
| 2026-08-20 | `136d668fbf1cb891a912b35f65739fb4af4957e4`, `solidity verdicts ... TD-1 decided as SHARED ORIGIN`; `3fa632721f0eced24744ba5b456d95c960a423d5`, `D-24 and A-GR4...`; `5b197ad2218fee52b5b726a4dc304fa6aea7b0b6`, `C-77 ... adopted`; later C-77 row last touched by `d41cfe078d4127b255ead542f17392b6c762a2c5` | `REGISTER_V001.md:9523-9563`; `ledger/status_ledger.tsv:245,247-248`; mirrors `STATUS_LEDGER_V001.md:102-103,185` | A-GR3 adopted shared origin, A-GR4 located emergence in boundary-shaping terms, and C-77 defined an open, non-exclusive emergence candidate with no claim that gravity is derived. | **NARROW** only A-GR3's explicit reliance on G-3's overbroad all-level `ALLOW`; **PRESERVE** A-GR3's shared-origin core, A-GR4, C-77, their no-import rule, and their open claim boundary. |
| 2026-08-27 | `a45104db0feb9d8a7883fe19c3878cdde120353b`, `Seal URFT, alpha inheritance, and gravity formation` | `LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/THEOREM.md:406-478`; concise restatement `GRAVITY_FORMATION_CURRENT_PICTURE_V001.md:2226-2238`; application `LANE_CROSS_RFT_ALPHA_GRA_EU_ALPHA_Q4_DIMENSION_LOCK_V001/THEOREM.md:181-190` | The sealed ladder defines finite-record `ALLOW` as set membership, host-sector `REQUIRE` as a conditional universal, complete-universe `REQUIRE` as singleton admissibility, and `SELECT` as a separate possible law explaining actualization. | **PRESERVE** and use as the repository-internal template for the repair.  Its physical alpha claims retain their own existing scopes; the repair imports only its type separation. |
| 2026-09-06 | `b0e1d5258621f8dda0a9ff29f5869fc1a5a33511`, `Seal hostile-audited L8 criticality seed null` | `DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001/PROTOCOL.md:23-58,138-178`; `RESULT.md:1-18,79-93`; `CURRENT_CONTINUATION.md:123-150`; `GRAVITY_VERIFICATION_LEDGER.md:1584-1645` | Gate R-C froze one `N`-independent Hamiltonian, separated authenticated-write weights from sharp-sector diagnostics, and stopped at L8 with no isolated density candidate. | **PRESERVE.** This is a clean example of fixed-parent analysis.  The doctrine repair changes none of its spectra, nulls, stop gates, or claim boundaries. |

### Commit-hash index for abbreviated dependency references

Every abbreviated hash used below resolves uniquely as follows:

| Abbreviation | Full commit hash |
|---|---|
| `59f233a...` | `59f233aaf9acbe37fd4a68c6456420302a3be554` |
| `f3462c4...` | `f3462c46a6fdf2cd6929d2cc6508c5e046124319` |
| `c75a582...` | `c75a582f805fe0eb349fe07431d0b33cd95848f9` |
| `5c01e47...` | `5c01e473a9933ec2fb0bcba230835ef941566e15` |
| `04819fe...` | `04819fea988340a48ddfb1c0a74e3792f8eec045` |
| `e759573...` | `e7595733762d71993af7dce9a78a5d636d5ae81d` |
| `9a6f2a1...` | `9a6f2a10d0f176bc8577118b7bbb2994e5430dd6` |
| `b8f83e3...` | `b8f83e3c3d4747feff4e8705eea795f1b141564b` |
| `653493e...` | `653493e9c2c30a13690dd488ea449134417136df` |
| `c888e76...` | `c888e768b8d24112cc3d7054fc8e31ead9766309` |
| `ab97b2d...` | `ab97b2d5881c0cddb97dc9875894990188900d60` |
| `136d668...` | `136d668fbf1cb891a912b35f65739fb4af4957e4` |
| `3fa6327...` | `3fa632721f0eced24744ba5b456d95c960a423d5` |
| `5b197ad...` | `5b197ad2218fee52b5b726a4dc304fa6aea7b0b6` |
| `9f36510...` | `9f3651021c780aef577af7d6d4543b7fa5643e4e` |
| `d41cfe0...` | `d41cfe078d4127b255ead542f17392b6c762a2c5` |
| `3c86130...` | `3c86130f4a862fa4a1ddfe41d6393bd0dc40f184` |
| `f9ba791...` | `f9ba791ac96beb01e9eb0b74e5411faa55b8c735` |
| `e6cae34...` | `e6cae345185df5b4fc3330ac1bcf937758c7ff8b` |
| `a45104d...` | `a45104db0feb9d8a7883fe19c3878cdde120353b` |
| `53a84ad...` | `53a84ad9ad263d052a9a4ace42fb67c8a34115ff` |
| `7b3a784...` | `7b3a78484d7da8585e2aa1b293b8941e6d20d45c` |
| `d3c30fa...` | `d3c30fac07975bf7546fe7a23e798d06758f0040` |
| `c81241f...` | `c81241f615ada0b66ae25347286071808ecba06c` |
| `57c4c08...` | `57c4c08bccc45dfb7d68919f61a682ddcff73296` |
| `b0e1d52...` | `b0e1d5258621f8dda0a9ff29f5869fc1a5a33511` |

## 4. Exhaustive live dependency disposition

The table below covers every named live dependency in the repair brief.  The
canonical machine-readable row is `ledger/status_ledger.tsv`; the corresponding
`STATUS_LEDGER_V001.md` row is a required live mirror.  `REGISTER_V001.md` is
append-only history and must not be silently rewritten.

| Object | Exact live and historical locations | Present dependency | Disposition and required later canonical action |
|---|---|---|---|
| `G-3` | `ledger/status_ledger.tsv:16`; `STATUS_LEDGER_V001.md:205`; origin/erratum `REGISTER_V001.md:4878-4912`; live-row introduction `59f233a...`, current classification `f3462c4...` | Carries “ALLOW at EVERY level” and “no allow-to-require transition.” A-GR3 cites it explicitly. | **SUPERSEDE.** Append an erratum.  Replacement must retain Gamma's fixed-parent capacity role but withdraw the claim that require does not exist and the claim that gravitational equations are exhausted by constraints. |
| `D-4` | `ledger/status_ledger.tsv:58`; `STATUS_LEDGER_V001.md:65`; derivation `REGISTER_V001.md:5220-5257`; `GLOSSARY.md:64`; commit `e759573...` (glossary echo `9a6f2a...`) | Governs the allow/occupancy split, five-clause typing, F-2, F-3, and T-II.5. | **NARROW.** Add “within a frozen parent/fixed admissible fiber.” Keep clause satisfaction as a carrier predicate. Replace the absolute “never permissions” wording with the scoped theorem and enlarged-parent boundary. The glossary must mirror the scoped wording. |
| `X-2` plus `T-21` | `ledger/status_ledger.tsv:24`; `STATUS_LEDGER_V001.md:291`; `REGISTER_V001.md:4829-4912,6738-6768,9602-9608`; X2 commits `c75a582...`/`5c01e47...`, T-21 commit `04819fe...` | Exact fixed-complex result plus an already-appended record/collective scope boundary. | **PRESERVE** the current T-21-scoped row.  The original macroscopic-face interpretation and its immediate no-require erratum are **HISTORICAL-ONLY** and **SUPERSEDED**, respectively.  X-2 cannot refute a dynamical enlarged parent. |
| `F-2` | `ledger/status_ledger.tsv:53`; `STATUS_LEDGER_V001.md:309`; `RECORD_FORMATION_V001.md:22,31-33`; `REGISTER_V001.md:5244-5257`; introduced `b8f83e3...`, corrected `e759573...` | The original “protection turns on” target is withdrawn and its fixed-carrier occupancy content lives in F-7. | **PRESERVE** the withdrawal/correction for a fixed carrier.  Do not silently reactivate F-2.  A carrier-changing protection onset, if pursued, belongs to the reopened enlarged-parent F-3/T-II.5 question or to a freshly named target. |
| `F-3` | `ledger/status_ledger.tsv:54`; `STATUS_LEDGER_V001.md:310`; `RECORD_FORMATION_V001.md:23,31`; `REGISTER_V001.md:5248`; introduced `b8f83e3...`, reclassified `e759573...` | Reclassified solely because the unscoped D-4 called carrier origination production of a permission. | **REOPEN** conditionally.  It is meaningful only after an enlarged physical parent supplies dynamical carrier variables and an authenticated map between carrier fibers.  This does not establish such a parent. |
| `F-7` | `ledger/status_ledger.tsv:59`; `STATUS_LEDGER_V001.md:314`; `REGISTER_V001.md:5252-5262`; `RECORD_FORMATION_V001.md:22,25,31-38`; commit `e759573...` | Correctly asks which definite record state is occupied on an already record-capable carrier. | **PRESERVE** unchanged.  It is an occupancy/measurement question within a fixed admissible record space and is not replaced by F-3. |
| `T-II.5` | `ledger/status_ledger.tsv:33`; `STATUS_LEDGER_V001.md:305`; inherited by `REGISTER_V001.md:5248`; current row accumulated classifications at `653493e...`, `c888e76...`, `f3462c4...` | “Why the world's Hamiltonian has this topology” is reclassified by unscoped D-4. | **REOPEN** conditionally with F-3.  It requires an enlarged parent that owns the Hamiltonian/carrier variable; it cannot be answered by dynamics internal to the frozen Hamiltonian whose origin is being asked about. |
| `G-4` | `ledger/status_ledger.tsv:39`; `STATUS_LEDGER_V001.md:206`; `REGISTER_V001.md:5045-5075`; commit `ab97b2d...` | Exact fixed-carrier constraint algebra, previously the legitimate record-native remainder after X-6. | **PRESERVE** exactly and keep carrier scope explicit.  It supplies a null/control algebra only; no Poincare, Virasoro, central-extension, or anomaly conclusion follows. |
| `A-GR3` | `ledger/status_ledger.tsv:245`; `STATUS_LEDGER_V001.md:102`; `REGISTER_V001.md:9523-9535`; commit `136d668...` | Shared-origin claim explicitly says it is consistent with G-3's `ALLOW`. | **NARROW** the citation edge, not the shared-origin decision: point to the fixed-parent allow theorem and enlarged-parent emergence opening, not to G-3's all-level/no-require claim. |
| `A-GR4` | `ledger/status_ledger.tsv:247`; `STATUS_LEDGER_V001.md:103`; adoption represented in `REGISTER_V001.md:9543-9555`; commit `3fa6327...` | Boundary-shaping mechanism and explicit warning that record-level behavior need not resemble macroscopic gravity. | **PRESERVE.** It already respects the record/macroscopic distinction and does not require the superseded no-require claim. |
| `C-77` | `ledger/status_ledger.tsv:248`; `STATUS_LEDGER_V001.md:185`; `REGISTER_V001.md:9539-9563`; adopted `5b197ad...`, openness `9f36510...`, current row last touched `d41cfe0...` | Candidate emergence claim, non-exclusive, with imported classical form forbidden and gravity explicitly not derived. | **PRESERVE.** Clarify only that effective permission/carrier change must be derived from an enlarged parent.  None of C-77's finite results is promoted or demoted by this documentary repair. |
| `H-1` | `ledger/status_ledger.tsv:126`; `STATUS_LEDGER_V001.md:25`; `REGISTER_V001.md:6738-6760`; reframe commit `3c86130...`, live claim wording `f9ba791...` | Separates emergence from record-level identity and says D-4 permits cross-level identification. | **PRESERVE.** It is the correct live collective question, still open/partial under its existing evidence. |
| `H-7` | `ledger/status_ledger.tsv:132`; `STATUS_LEDGER_V001.md:31`; `REGISTER_V001.md:6770-6774`; introduced `e6cae34...` | Carrier origin was left open but its prerequisites F-3/T-II.5 remained reclassified. | **REOPEN** as the hard-problem expression of conditional enlarged-parent carrier formation.  Keep it open; the repair supplies no physical parent. |
| `H-8` | `ledger/status_ledger.tsv:133`; `STATUS_LEDGER_V001.md:32`; `REGISTER_V001.md:6761-6768`; commit `3c86130...` | Still marked OPEN even though the current X-2 row says T-21 answered the foreclosure concern. | **SUPERSEDE** as a live open target and retain **HISTORICAL-ONLY** as the concern that caused T-21.  Its resolved content is the scoped X-2 row; the substantive emergence question is H-1/C-77. |
| Later alpha `ALLOW/REQUIRE/SELECT` ladder | `LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/THEOREM.md:406-478`; `GRAVITY_FORMATION_CURRENT_PICTURE_V001.md:2226-2238`; concrete application `LANE_CROSS_RFT_ALPHA_GRA_EU_ALPHA_Q4_DIMENSION_LOCK_V001/THEOREM.md:181-190`; all sealed by `a45104d...` | Already distinguishes set membership, domain-relative necessity, theory-absolute singleton necessity, and independent dynamical selection. | **PRESERVE** and elevate as the internal semantic precedent.  Do not generalize its alpha-specific physical theorem beyond its stated sector; generalize only the type distinctions. |
| Current sealed Gate R-C | Ledger sequence: first interaction/retention stress `GRAVITY_VERIFICATION_LEDGER.md:272-287` (`53a84ad...`); accumulated-write latency `1311-1381` (`7b3a784...`); directed-edge control `1383-1433` (`d3c30fa...`); open-ladder control `1435-1504` (`c81241f...`); composition obstruction `1506-1582` (`57c4c08...`); hydrodynamic seed null `1584-1645` (`b0e1d52...`).  Latest protocol/result: `DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001/PROTOCOL.md:23-58,138-178`; `RESULT.md:1-18,79-93`; continuation `CURRENT_CONTINUATION.md:123-150`. | The sequence consists of bounded conditional fixed-parent transport/retention records, finite controls, a composition obstruction, and a latest `N`-independent `H_L` screen that separates authenticated-write weights from sharp sector density and finds no isolated density candidate.  No listed Gate R-C section contains a literal D-4 dependency. | **PRESERVE** every numerical row, hostile verdict, stop gate, conditional label, and open claim boundary.  These are fixed-parent results and cannot close the reopened enlarged-parent question.  The latest null remains bounded to its parent/channel. |
| Untracked Gate R-C successor draft | `DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/PROTOCOL.md:1-21,77-115,137-154`; no commit provenance | Draft centerline `z=1` screen; explicitly retains the frozen parent and says compatibility would authorize a separate native-operator screen. | **PRESERVE** as quarantined work in progress, not evidence.  Do not execute or commit it as part of this repair; it must be reconsidered after the doctrine packet is hostile-audited. |

## 5. Historical and copied artifacts: no silent edits

The following classes contain echoes of D-4 or allow/require but are not live
canonical authorities and must not be mass-edited:

- `REGISTER_V001.md` is the chronological record.  Its contradictory stages are
  evidence for this repair.  Add a dated erratum later; do not replace
  `REGISTER_V001.md:1965-1980`, `4829-4912`, `5220-5257`, or `6738-6774`.
- `LANE_T29_HDD/VERIFY/gridcheck/STATUS_LEDGER_V001.md` and
  `LANE_T29_HDD/VERIFY/gridcheck/ledger/status_ledger.tsv` are verification
  snapshots, not live ledger copies.  **HISTORICAL-ONLY.**
- `LANE_T36_A/t36a_classification.tsv`,
  `LANE_T36_B/T36_B_CLASSIFICATION.tsv.txt`, and
  `LANE_T36_D_CHECK/T36_consolidated_classification.tsv.txt` are historical
  classification outputs.  **HISTORICAL-ONLY.**
- `HANDOFF_2026-08-17.md`, `HANDOFF_2026-08-20.md`, old W/R lane reports, and
  independent-audit reports preserve the state seen by their authors.
  **HISTORICAL-ONLY** for the doctrine change; append no retrospective repairs
  inside them.
- `LANE_X2_BACKREACTION/` remains the evidence packet for the fixed-complex
  observation.  **PRESERVE** its computation; do not retrofit an enlarged
  parent into it.
- `RECORD_FORMATION_V001.md` is retained byte-identically as historical
  formation custody and is addressed by the dated erratum.  `GLOSSARY.md` is a
  live-facing summary and the integrated target updates its D-4 definition to
  the scoped parent/fiber wording.

## 6. Dependency consequences for the proposed algebraic-scaling route

1. The numerical Gate R-C centerline question is independent of the semantic
   repair and remains merely unexecuted; nothing here changes its frozen rows or
   pass criterion.
2. Allow predicates, universal requirements, characteristic projectors,
   constraint generators, occupancies, and dynamical generators remain distinct
   object types.  No map from a permission predicate to a Hilbert-space operator
   is supplied by the history.
3. `G-4`'s commuting constraint generators may serve as an exact-null control.
   Their zero commutator is not a spacetime algebra or a zero-anomaly result.
4. Any native algebra screen must construct dynamical operators from the
   physical parent independently of the allow/require labels.
5. A `z=1` finite-window candidate, if later obtained, cannot be inserted into
   a zero permission-projector commutator to create a central extension.

## 7. Closure conditions for the integrated target and hostile audit

This provenance lane is an input to the integrated candidate repair.
Promotion must fail closed unless an independent auditor confirms all of the
following on the final target:

1. every live row named in section 4 has one explicit disposition;
2. the frozen-parent theorem and enlarged-parent construction are not
   contradictory;
3. `REQUIRE` is treated as a scoped quantifier, never a synonym for causal
   dynamics;
4. `SELECT` remains a separate, possibly absent law;
5. the fixed-complex X-2 result, F-7 occupancy work, G-4 algebra, and sealed Gate
   R-C numerics are unchanged;
6. F-3, T-II.5, and H-7 are reopened only conditionally, with no physical-parent
   existence claim;
7. A-GR3/A-GR4/C-77 retain their no-import and no-gravity-promotion boundaries;
8. historical and audit artifacts are not silently rewritten; and
9. `ledger/status_ledger.tsv` and `STATUS_LEDGER_V001.md` remain synchronized if
   the governing repair is later adopted.

## 8. Disposition summary

```text
PRESERVE:
  D-1 guard; X-2 at fixed-complex scope plus T-21; F-2 fixed-carrier
  withdrawal/correction; F-7; G-4; A-GR3 shared-origin core; A-GR4; C-77;
  H-1; sealed Gate R-C; later ALLOW/REQUIRE/SELECT ladder.

NARROW:
  D-4 to frozen parent/fixed fiber; A-GR3's dependency on G-3; G-3's
  surviving Gamma-capacity kernel.

REOPEN:
  F-3; T-II.5; H-7 -- all conditional on a complete enlarged physical parent
  with dynamical carrier variables.

SUPERSEDE:
  G-3 as an all-level/no-require doctrine; X2 erratum's “require exists
  nowhere”; H-8 as a still-open foreclosure claim.

HISTORICAL-ONLY:
  the initial record/macroscopic allow-to-require interpretation; W-22 as an
  incomplete type system but preserved origin/SELECT insight; old ledgers,
  classification exports, handoffs, and sealed audit snapshots.
```
