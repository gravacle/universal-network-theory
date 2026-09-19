# URM update impact matrix — 2026-09-15

> **SUPERSEDED PRE-ADOPTION PLANNING MATRIX — 2026-09-16.** Keep the rows below
> as an audit trail of the proposed reconciliation, but do not use their
> Stage-6 or pending-L14 recommendations as current authority. Use
> [`README.md`](README.md), [`PROOF_GUIDE.md`](PROOF_GUIDE.md),
> [`ARGER_GATE_ADOPTION_2026-09-16.md`](ARGER_GATE_ADOPTION_2026-09-16.md),
> and [`L14_RUN_DISPOSITION_2026-09-16.md`](L14_RUN_DISPOSITION_2026-09-16.md).
> L14 is `INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT`.

## Purpose and boundary

This is a preparation document for updating the Universal Record Model (URM).
It does **not** itself alter `MODEL.md`, `GLOSSARY.md`, the ledgers, the register,
the continuation record, or any executable URM surface.

The tracked baseline reviewed here is branch
`integration/post-gate-a-20260915` at commit `42f1ea3`.  Later L12, Stage-5,
Stage-6, record-flow, lineage-support, and L14-scout artifacts are presently
working-tree material after that commit; they require curation and a permanent
commit before a public URM or Zenodo release can cite them by commit identity.

The central update rule is:

> Preserve the rigor and positive content of the authenticated finite
> computations, while preserving their declared ceilings.  An exact finite
> history, an authenticated sector weight, or a finite `z=1`-compatible fit is
> not by itself a continuum limit, an exact asymptotic exponent, an emergence
> theorem, or gravity.

## Classification legend

| Classification | Meaning for the URM update |
|---|---|
| **changes definition** | A term, object, or typed distinction in the model must be added or corrected. |
| **changes status** | A registered question, gate, or result has a new adjudicated state. |
| **changes dependency** | The proof or execution graph has a new prerequisite, obstruction, or authorized successor. |
| **changes interpretation** | The result changes how an existing claim must be read without changing the underlying definition. |
| **evidence-link only** | Existing doctrine is unchanged, but a canonical surface should point to new evidence. |
| **no URM change** | Already represented correctly or operational only; retain as validation/history rather than new theory content. |

Multiple classifications may apply to one row.

## Impact matrix: tracked results after the public `386ee2c` point

| Topic / finding | Governing evidence and tracked commit(s) | Classification | Recommended canonical effect | Claim ceiling that must travel with it |
|---|---|---|---|---|
| Direct Ward shortcut and accumulation horizon through GL6CS | `model/gravity_microscopic_progress.py`; `model/validate_gravity_microscopic_progress.py`; `DEVELOPMENT_G_GL6BR_DIRECT_WARD_SHORTCUT_V001/`; `DEVELOPMENT_G_GL6CS_ACCUMULATION_HORIZON_V001/`; commits `dd5d63e`, `2464ae5` | **no URM change**, **evidence-link only** | Retain the existing V008 microscopic-gravity layer and validator.  Do not rewrite this sealed layer to absorb the later relational program. | This is the declared microscopic-progress frontier, not evidence that the later relational finite-size gate has passed. |
| Gate A L4 baseline, raw-source audit, parity custody, and conditional UV witness | `DEVELOPMENT_G_GATE_A_UV_LEDGER_L4_V001/`; `AUDIT_G_GATE_A_UV_LEDGER_L4_V001/`; commits `db187df`, `ea52b62`, `e7777a0`, `386ee2c` | **changes status**, **evidence-link only** | Append the L4 Gate-A evidence chain to `CURRENT_CONTINUATION.md`, `GRAVITY_VERIFICATION_LEDGER.md`, and the register. | A finite L4 source/response witness is not an accumulated-record or gravity result. |
| Owner-once active seam and stationary carrier seam; Gate A-R closure | `DEVELOPMENT_G_GATE_A_ACTIVE_SEAM_LEDGER_V001/`; `DEVELOPMENT_G_GATE_A_STATIONARY_CARRIER_SEAM_V001/`; `CERTIFICATE_GATE_A_R_RECORD_OWNERSHIP_CONSERVATION_V001/`; commits `ce92d01`, `4e2099d`, `935ea23` | **changes status**, **changes dependency** | Register owner-once/conservation as prerequisites of the accumulation route and record Gate A-R as closed. | Closing record custody authorizes the next bounded calculation; it does not establish macroscopic gravity. |
| Programmed L8 interaction/repetition/ring/parameter/ladder screens | `DEVELOPMENT_R_GATE_B_INTERACTION_STRESS_L8_V001/` and the connected-record development packets associated with commits `53a84ad`, `4585145`, `5c5a2f8`, `062bc32` | **changes status**, **evidence-link only** | Summarize as the first connected-accumulation exploration and retain the individual controls in evidence links. | Programmed finite interactions are route-development evidence, not autonomous emergence. |
| Autonomous connected accumulation L6, L8, L10, L12, and the earlier same-slice L14 trajectory | `DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001/`; commits `a520cfe`, `556b960`, `34ad3b7`, `52cecf6`, `3aa8ae6` | **changes interpretation**, **evidence-link only** | Canonical text must call this the **earlier same-slice raw accumulation trajectory**.  Preserve the finite results and explicitly separate this L14 from the current relational L14 scout. | The `3aa8ae6` L14 result is **not** the present L14 finite-scout gate and must never be used to mark that gate passed.  It supplies no continuum, exact exponent, or gravity claim. |
| Localized write-response protocol through L12 | `DEVELOPMENT_R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_V001/`; `AUDIT_R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_V001/`; commits `df5ad84`, `54eec6c` | **changes status**, **evidence-link only** | Add the finite response checkpoint to the route history and evidence map; preserve the direct-parity versus approximate-corroboration distinction by scale. | L6/L8 direct parity and L10/L12 approximate corroboration are finite response evidence only; L14 was not measured in this checkpoint. |
| Two-body, latency, forward-edge, open-ladder, composition, and criticality controls | Packets associated with commits `1c3e88e`, `7b3a784`, `d3c30fa`, `c81241f`, `57c4c08`, `b0e1d52` | **changes status**, **changes interpretation** | Append each as a route-specific control or obstruction.  The URM narrative should explain why these controls forced the relational pivot. | The L4+L4→L8 composition obstruction and L8 seed null stop their tested formulations; neither is a global no-go for accumulation or gravity. |
| Scoped `ALLOW` / `REQUIRE` / `SELECT` repair | `DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/FORMAL_SCOPE_THEOREM.md`; `LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/THEOREM.md`; `LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/RESULT.md`; commit `4b335b7` | **changes definition**, **changes dependency**, **changes interpretation** | Keep D-4/G-3/H-7/H-8, but refine the α wording as specified below.  Add explicit validator coverage for all three levels. | A host-sector `REQUIRE` is a predicate, not a production or selection mechanism; it does not numerically derive α. |
| Fixed `rho=1/4` centerline rejection through L12 | `DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/`; its audit packet; commit `cd1d8b2` | **changes status**, **changes interpretation** | Register `CENTERLINE_Z1_REJECTED_L4_L12` as the disposition of the fixed-centerline route. | This rejects one finite frozen-centerline formulation; it is not a general `z=1` no-go. |
| Same-port authenticated accumulation obstruction | `DEVELOPMENT_R_AUTHENTICATED_ACCUMULATION_SCREEN_V001/`; its audit packet; commit `2a21705` | **changes status**, **changes dependency** | Record that the same-port formulation has no common L4 sector and is closed in that form. | No-common-sector at L4 stops the same-port formulation only. |
| Intrinsic-admission L4 parent | `DEVELOPMENT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/`; its audit packet; commit `3c8e838` | **changes definition**, **changes dependency** | Add the intrinsic `(w,r)` admission/lineage object and owner accounting to `MODEL.md` and `GLOSSARY.md`; treat this as the entry point to the relational route. | This constructs and authenticates a finite parent relation; it is not a gravity result. |
| Scalable relational accumulation L4–L10 | `DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/`; its audit packet; commits `a0e88ad`, `936e14b`, `9f81115`, `3d2e17c`, `63cc53b`, `4fcaef0` | **changes status**, **changes dependency**, **evidence-link only** | Add the target/hostile finite sequence, bounded-streaming dependency, and the common support interval `[0, 0.375]` to the relational certificate history. | The result is finite through L10; the first L12 route was resource-locked, not scientifically rejected. |
| Exact L12 prefix-lineage representation | `DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/`; its audit packet; commit `42f1ea3` | **changes definition**, **changes dependency**, **evidence-link only** | Define prefix support and injective lineage embedding; register bounded streaming as the representation that makes exact L12 custody possible. | This is an exact representation/computation theorem, not an L12 physics result by itself. |

## Impact matrix: authenticated working-tree results after `42f1ea3`

These rows are scientifically and operationally material, but no publication
surface should cite them as committed repository evidence until curation lands
them on a permanent commit and release tag.

| Topic / finding | Governing working-tree evidence | Classification | Recommended canonical effect | Claim ceiling that must travel with it |
|---|---|---|---|---|
| Stage-1/2 storage, custody, launch recovery, and authorization-state work | `DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/`; `AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/`; the Stage-3 recovery/preparation packets; `STAGE1_ACCOUNT_HANDOFF_PROTOCOL_V001.md` | **changes dependency**, **evidence-link only** | Preserve as reproducibility and custody history in the continuation/verification ledgers; link the final superseding protocol rather than narrating every repair in the theory definition. | Operational recovery establishes provenance and fail-closed execution, not physics.  Failed starts remain part of the history and are not erased. |
| Exact authenticated L12 complete-prefix histories | `AUDIT_R_L12_NUMERICAL_REPAIR_V003/EXACT_ADJUDICATION_V003R1.json`; `AUDIT_R_L12_NUMERICAL_REPAIR_V003_STAGE4R1/STAGE4R1_EXECUTION_RECORD.json` | **changes status**, **evidence-link only** | Add a finite L12 certificate: `PASS_EXACT_L12_COMPLETE_PREFIX_HISTORY_GATE_V001`, 1156/1156 checks, and the target/hostile/blind custody hashes.  Stage-4R1 should be identified as schema projection only. | Maximum observable difference `9.769962616701378e-15`, sector-weight difference `8.326672684688674e-16`, and terminal-amplitude difference `7.946965413254846e-17` authenticate agreement; they do not establish a spectrum, continuum, emergence, or gravity result. |
| Authenticated L4–L12 relational sector manifest | `DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003/AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003R1.json`; `DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003_STAGE5R1/STAGE5R1_EXECUTION_RECORD.json` | **changes status**, **changes dependency** | Register `PASS_RELATIONAL_ACCUMULATION_L4_L12__SPECTRUM_MANIFEST_READY`, its 24 atoms, declared accumulated interval `[1/48, 17/48]`, and Stage-5 authentication. | The Stage-5 bridge is a representation/authentication result; it does not decide the spectrum or the `z=1` gate. |
| Preregistered Stage-6R2 relational interval spectrum | `DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/ADJUDICATION_V002_L12_V003R1_STAGE6R2.json`; `DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_COMPATIBILITY_V001_STAGE6R2/STAGE6R2_EXECUTION_RECORD.json` | **changes status**, **changes interpretation**, **changes dependency** | Register `AUTHENTICATED_RELATIONAL_Z1_REJECTED_L4_L12` and `COMPLETE__PAUSED_BEFORE_STAGE7`.  Record that atoms A020/A021 pass individually, while their connected component fails the preregistered all-scale mass qualification. | Component mass is L4 `0.4675153267117474`, L6 `0.0772162340943762`, L8 `0.07989327507006902`, L10 `0.06569117096176974`, L12 `0.07952876193166904`; failure of the `>=0.5` conjunction is **not** proof that `z=1` is absent or impossible. |
| L12 typed record-flow sidecar | `DEVELOPMENT_R_L12_RECORD_FLOW_BRIDGE_V001/README.md`; `DEVELOPMENT_R_L12_RECORD_FLOW_BRIDGE_V001/RECORD_FLOW_BRIDGE_REPORT_V001.json` | **changes interpretation**, **evidence-link only** | Add the sidecar as a separately typed relational diagnostic: q4→q5 flow `0.088041168266264305`, q5→q6 flow approximately `0.105141414375126`, and deduplicated q4+q5+q6 mass `0.56956498393327842`. | The flow bridge is not a static atom, physical vertex, entanglement claim, or amendment of the frozen Stage-6R2 gate.  Crossing `0.50` under this relation does not authorize Stage 7. |
| Stage-6R3 supplemental record-flow adjudication | `DEVELOPMENT_R_L12_STAGE6R3_RECORD_FLOW_ADJUDICATION_V001/STAGE6R3_SUPPLEMENTAL_ADJUDICATION_V001.json`; its `README.md` and verification log | **changes status**, **changes dependency**, **changes interpretation** | Register `STAGE6R3_RECORD_FLOW_OBSERVED__ORIGINAL_Z1_GATE_REMAINS_REJECTED`; retain `STAGE7_AUTHORIZED=FALSE`.  Record endpoint q4+q6 mass `0.36652893665484882` and the consequent q5 requirement. | The q5 amount `0.13347106334515118` is threshold arithmetic, not an assumed L14 prediction, not a substitute for the Phase-2 reachability conjunction, and not the post-Phase-3 final finite-scout decision. |
| L12 lineage-resolved common support | `DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/LINEAGE_RESOLVED_SUPPORT_REPORT_V001.json` | **changes status**, **changes interpretation**, **evidence-link only** | Register target `0.11570852222694002`, hostile `0.11570852222694036`, conservative support `0.11570852222694002`, required support `0.1334710633451512`, shortfall `0.01776254111821117`, and classification `LINEAGE_RESOLVED_Q5_SUPPORT_BELOW_REQUIRED_THRESHOLD`. | This is a finite, read-only, common-lineage q5 support diagnostic on the declared `pbar` measure.  It does not override Stage-6R2 and is not a measurement of gravity. |
| Exploratory lower-bound progression at L08/L10/L12 | `DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/extract_lower_bound_progression.py` and its authenticated target-cache input; script SHA-256 currently `cb7dfa...` pending a permanent manifest | **evidence-link only**, **no URM change** | If retained, place it in an exploratory diagnostics appendix, with target-cache values L08 `0.0244800482`, L10 `0.0687369678`, and L12 `0.1157085222`.  Do not add it as a gate or headline claim. | The cache is not treated as unreliable: it descends from the rigorously authenticated computation.  The limited role is that this extractor is a target-cache trajectory diagnostic, not a separate target/hostile adjudication or a proof of monotone/asymptotic continuation. |
| Current targeted relational L14 scout | `DEVELOPMENT_R_L14_TARGETED_SCOUT_V003/KERNEL_BINDINGS_RELEASE_V003R3.json` and `L14_SOURCE_BUNDLE_MANIFEST_V003R5.json` for initial Target R5 and untouched Hostile R5; `KERNEL_BINDINGS_RELEASE_V003R6.json`, `L14_SOURCE_BUNDLE_MANIFEST_V003R6.json`, and `EXACT_KERNEL_AUDIT_V003R6.json` for fresh Target R6 | **changes dependency**, **pending status seam** | Keep the machine-readable URM state `PENDING_AUTHENTICATED_RESULT`.  Type Phase 2 only as reachability authorization over the authenticated Phase-1 merge.  Require authenticated Phase-3 q8/q9 evidence and the separate final conservative q-deduplicated actually-passing-sector mass decision before L14 progression admission.  Keep the old same-slice L14 result distinct. | Neither an executing job, a branch-local result, a q5 threshold hit, nor Phase-2 authorization alone is an L14 scientific result.  A pass of the final finite-scout gate is only a finite candidate and next-stage authorization; it is not an exact/asymptotic `z=1` emergence theorem, continuum result, or gravity result. |

## Required α wording

The existing `model/project_model.py` α role and the 2026-09-06 scope repair
contain the right structure, but `ledger/status_ledger.tsv` still carries older
rows that can be read as if the program's historical generic perturbation
magnitude were the physical fine-structure constant.  The canonical update
should use the following typed statement:

1. **ALLOW — generic record formation.**  Finite record formation admits an
   α-bearing electromagnetic sector among a non-singleton family of allowed
   sectors.  Record formation in general does not require one universal
   numerical α for every admissible record or parent.
2. **REQUIRE — an actual visible electromagnetic host.**  Conditional on an
   actual visible compact-`U(1)` host (W), a visible electromagnetic record
   requires an α-bearing coupling in that host, and records in the same
   visible-`U(1)` sector inherit the parent-matched α trajectory.  Thus **this
   universe requires α to reach visible EM**, with its numerical value anchored
   empirically to the observed host.
3. **Not a derivation.**  Host-sector `REQUIRE` and same-sector inheritance do
   not numerically derive, produce, or choose the observed α.  Bare record
   formation does not select a private α.
4. **SELECT remains separate.**  `SELECT_parent` is an independent proposition
   and may not exist.  A complete-universe singleton statement
   `REQUIRE_full(alpha*)` also remains open.

The controlling sources are
`LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/THEOREM.md` §§8–10,
`LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/RESULT.md` under
“ALLOW/REQUIRE/SELECT interpretation,” and
`DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/FORMAL_SCOPE_THEOREM.md` §3.

Consequences for current rows:

- `A-AL` and the “ALPHA SETS THE COST” portion of `A-PR` describe the
  historical perturbation-strength role and must not silently stand in for the
  physical fine-structure α/SAI-AWAI role.
- `H-2` and `D-13` should be superseded or reworded, not erased.  Their old
  anti-import warning remains historically valid for the earlier lattice
  calculation, while the later host-sector inheritance theorem supplies a
  different, explicitly typed physical-α statement.
- Claim G-E in `ledger/claims.tsv` needs the same distinction.  “Alpha sets the
  cost” alone is now too compressed to represent the physical role safely.

## Explicit L14 pending gate

The L14 URM seam must default closed.  A concise canonical form is:

```text
RELATIONAL_L14_STATUS = PENDING_AUTHENTICATED_RESULT

Phase-2 may pass only if:
  (a) Target and Hostile outputs authenticate and satisfy every original
      numerical predicate;
  (b) literal q5 has a consensus hit;
  (c) the physical q6 core has a consensus hit;
  (d) one exactly contiguous consensus-passing atom block covers the former
      L12-q5 density cell [3/16, 11/48); and
  (e) phase1_passing_mass + mass(q8) + mass(q9) >= 0.50.

Only an owner-once Phase-2 pass authorizes Phase 3 for q8/q9.

After Phase 3, the separate final finite-scout gate may pass only if:
  (f) authenticated Target and Hostile Phase-3 q8/q9 evidence exists and still
      satisfies every original numerical predicate;
  (g) each actually passing sector is assigned the lower independently
      computed Target/Hostile mass;
  (h) q identities are deduplicated before summation; and
  (i) the resulting conservative mass is at least 0.50.

Phase-2 authorization is therefore not the final threshold decision and cannot
promote the L14 progression row by itself.
```

Numerical nonconvergence, failed predicates, failed Target/Hostile
authentication, or absence of the authenticated mass ledger are
**obstructions**, not scientific rejections.  The current q5 reference
`0.13347106334515118` is the L12 endpoint-mass shortfall arithmetic; it is not
a substitute for conditions (a)–(e).

If the complete authenticated chain passes the final finite-scout gate,
canonical language must still say **finite L14 candidate/gate pass**.  That
finite decision is not an exact or asymptotic `z=1` emergence theorem.
Promotion to continuum physics or gravity requires separately declared and
closed gates.

## Canonical files and recommended edits

| Canonical surface | Recommended update | Editing discipline |
|---|---|---|
| `MODEL.md` | Add a separate relational-accumulation layer and certificate; add intrinsic admission, lineage, exact L12 status, Stage-6R2 rejection, record-flow sidecar, lineage-support result, and pending L14 seam.  Refine α wording.  Explicitly distinguish the earlier same-slice L14 trajectory from the current relational scout. | Hand-maintained.  Do not mutate the sealed microscopic-progress V008 certificate into a different result. |
| `model/project_model.py` | Expose a concise relational certificate/status method and refine `roles()["ALPHA"]` to the three-level wording. | Executable canonical source; accompany with validators. |
| New `model/relational_accumulation.py` | Recommended separate zero-input, custody-pinned certificate module for finite relational results and gate state. | Prefer immutable artifact hashes and closed status vocabularies over prose-only state. |
| `GLOSSARY.md` | Add **intrinsic admission**, **lineage**, **common-lineage support**, **`pbar_q` measure**, **density atom**, **finite `z=1`-compatible**, and **candidate gate**.  Distinguish the historical α-type perturbation magnitude from physical fine-structure α.  State that finite scale label `L` is not automatically a physical length or continuum limit. | Hand-maintained definitions; cross-link controlling theorem packets. |
| `ledger/status_ledger.tsv` | Append/supersede rows for Gate A-R, intrinsic admission, relational L4–L10, exact L12, Stage 5, Stage-6R2, the flow bridge, Stage-6R3, lineage support, and pending L14.  Supersede/retype `A-AL`, the relevant `A-PR` clause, `H-2`, and `D-13` without deleting history. | Source of truth.  Append rows; never erase historical rows. |
| `STATUS_LEDGER_V001.md` | Regenerate after the TSV update. | **Generated by `ledger/status.py`; never hand edit.** |
| `ledger/claims.tsv` | Keep G-D at `MEMBER-LEVEL-MATCH` unless and until later, separately specified gravity gates close.  Add new evidence anchors/URM location as appropriate.  Rewrite G-E to carry the α typing above. | Source of truth.  Claim stage must not be promoted merely because L14 passes a finite gate. |
| `THE_CLAIMS_V001.md` | Regenerate after the TSV update. | **Generated by `ledger/claims.py`; never hand edit.** |
| `REGISTER_V001.md` | Append the dated journey: original record-level route, its specific obstacles, pivot from the conceptual pre-L4 L02 custody baseline into the computed L4/L6/L8/L10/L12/L14 ladder, failed starts/recoveries, authenticated L12 adjudications, and L14 pending/result. | Manual append-only history; do not rewrite prior entries. |
| `CURRENT_CONTINUATION.md` | Append the missing 2026-09-09–15 chain through authenticated L12, Stage 5/6, sidecars, lineage support, and L14 pending/result. | Hand-maintained; retain operational failures and supersessions. |
| `GRAVITY_VERIFICATION_LEDGER.md` | Append the same chain as verification-grade checkpoints, with exact artifact paths/hashes and explicit exclusions. | Hand-maintained; every positive result carries its ceiling. |
| `ledger/plan.tsv` / `THE_PLAN_V001.md` | If plan tasks are changed, add source rows/status changes and regenerate the plan. | `THE_PLAN_V001.md` is **generated by `ledger/plan.py`; never hand edit.** |
| `RECORD_FIRST_PROOF_EXECUTION_SCHEDULE_STATUS_V001.md` | Mark the 2026-09-09 schedule as historical/superseded or append a terminal disposition and create a current successor. | Do not silently rewrite the locked baseline. |
| `URM_VALIDATION_BASELINE_2026-09-15.md` | Carry this pre-edit validation record into review/release evidence and compare post-edit results against it. | Baseline evidence only.  Do not reclassify inherited failures as regressions caused by the relational update. |

## Recommended executable URM shape

Do not fold the relational program into
`model/gravity_microscopic_progress.py` V008.  A separate module such as
`model/relational_accumulation.py` should expose a compact certificate with at
least:

- authenticated finite L12 history status and custody hashes;
- authenticated L4–L12 manifest identity;
- frozen Stage-6R2 adjudication and `stage7_authorized = false`;
- typed record-flow observation without gate override;
- target/hostile common-lineage q5 support, required threshold, and shortfall;
- current L14 state, initially `PENDING_AUTHENTICATED_RESULT`;
- an explicit list of excluded promotions: `EXACT_Z1`, `CONTINUUM`, `METRIC`,
  `WARD_IDENTITY`, `GRAVITON`, `EINSTEIN_DYNAMICS`, `UNIVERSAL_COUPLING`,
  `NEWTON_G`, `EMERGENCE`, and `GRAVITY`.

`model/project_model.py` can delegate to this certificate rather than
duplicating numbers or prose.

## Required validators

Add `model/validate_relational_accumulation.py` and call it from
`model/validate_urm.py`.  It should fail closed unless it can verify:

1. every pinned artifact path and SHA-256 identity;
2. schema/classification values for the exact L12, Stage-5, Stage-6R2,
   Stage-6R3, and lineage-support artifacts;
3. target/hostile identities and declared numerical tolerances;
4. all 1156 exact-L12 checks and the reported maximum differences;
5. Stage-6R2 component atom membership and per-L masses;
6. exact threshold arithmetic:
   `0.5 - 0.36652893665484882 = 0.13347106334515118` within the declared
   decimal representation;
7. conservative lineage support `0.11570852222694002`, shortfall
   `0.01776254111821117`, and a false threshold predicate;
8. `stage7_authorized = false` at L12;
9. that an L14 progression admission cannot be represented from Phase 2 alone:
   it requires the authenticated owner-once Phase-1 merge and Phase-2
   reachability decision, authenticated target/hostile Phase-3 q8/q9 evidence,
   and the separate final conservative q-deduplicated finite-scout decision;
10. that the earlier same-slice L14 certificate cannot satisfy the current
    relational L14 seam.

Refine `model/validate_gravity_formation_theory.py`, or add a focused roles
validator, to assert the α contract:

- generic record formation `ALLOW`s more than one parent-sector α;
- actual visible same-`U(1)` EM records `REQUIRE` and inherit the host α;
- this does not constitute numerical derivation;
- neither `SELECT_parent` nor complete-universe singleton `REQUIRE` is claimed.

After canonical edits, run at minimum:

```bash
python3 ledger/status.py
python3 ledger/claims.py
python3 ledger/plan.py
python3 model/validate_relational_accumulation.py
python3 model/validate_gravity_formation_theory.py
python3 model/validate_gravity_microscopic_progress.py
python3 model/validate_urm.py
```

Then inspect the generated diffs and run the repository's normal proof,
register, and integrity checks before committing or tagging.

### Inherited validation state

`URM_VALIDATION_BASELINE_2026-09-15.md` records that the aggregate
`model/validate_urm.py` command was already red before this reconciliation.  A
post-edit report must distinguish the following inherited failures from any
new failure:

- the ARROW family is `26/27`, with the F-19 system-only-unitary invariance
  check computing `1.643e-14` against the sealed printed anchor `3.686e-14`;
- the world-observation input chain lacks the local `lakeshore_vsm` adapter
  and `model/checks_lakeshore_vsm.py`, although its core checks are `28/28`
  and this input chain carries zero scientific weight;
- the synthetic gamma-flow input chain cannot construct its fixture because
  `HANDOFF_2026-08-22.md` is absent from this audited checkout; that chain is
  explicitly zero proof weight.

These failures should be repaired only under their own scoped audit.  They
must not be silently changed as part of the relational update, and the release
must not report a clean aggregate URM pass while they remain.  Conversely,
`model/validate_gravity_microscopic_progress.py` is independently green at
`247/247`; none of the inherited aggregate failures invalidates that sealed
certificate.

The post-edit validation record should therefore show both:

1. targeted pass/fail results for every changed or newly added URM surface;
2. an aggregate before/after comparison against
   `URM_VALIDATION_BASELINE_2026-09-15.md`, with inherited failures labelled
   separately from new regressions.

## Non-negotiable promotion ceilings

- Exact finite histories are not a thermodynamic or continuum limit.
- Finite `z=1`-compatible intervals are not an exact asymptotic exponent.
- `AUTHENTICATED_RELATIONAL_Z1_REJECTED_L4_L12` is a rejection under the
  preregistered finite conjunction, not a universal `z=1` no-go.
- `0.11570852222694002` is common-lineage q5 support on the declared finite
  `pbar` measure; it is not gravity.
- A favorable final L14 finite-scout gate would establish a finite candidate
  and authorize a next bounded stage; it is not an exact/asymptotic `z=1`
  emergence theorem and would not alone prove continuum physics or gravity.
- The old same-slice L14 trajectory is not the current L14 scout result.
- The α host-sector requirement/inheritance theorem is not numerical
  derivation or parent selection.
- No continuum, metric identification, Ward identity, graviton, Einstein
  dynamics, universal coupling, numerical `G`, or gravity promotion is earned
  unless its own declared gate closes.
